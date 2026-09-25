"""Structural checks that run after a rule's regex has matched.

A regex finds the candidate. Some rules then need the structure around it to
decide whether the candidate is a real finding: the element that holds it, the
CSS rule block it sits in, or the files it names. A rule opts in with
``"post": "<check name>"`` in its ``detection`` block.

Each check has the signature ``check(ctx, view, match, start) -> bool`` and
returns True when the hit is a real finding. ``ctx`` is a ``FileContext`` that
caches per-file structure, so a file with thousands of hits is still parsed
once.
"""
from __future__ import annotations

import re
from bisect import bisect_right
from html import unescape as html_unescape
from functools import lru_cache
from itertools import combinations
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

from engine.linter.views import FileViews, Tag, View

# ---------------------------------------------------------------------------
# Element ranges
# ---------------------------------------------------------------------------


def _merge(intervals: List[Tuple[int, int]]) -> Tuple[List[int], List[int]]:
    """Merge overlapping intervals; returns parallel start and end lists."""
    starts: List[int] = []
    ends: List[int] = []
    for s, e in sorted(intervals):
        if starts and s <= ends[-1]:
            ends[-1] = max(ends[-1], e)
        else:
            starts.append(s)
            ends.append(e)
    return starts, ends


def _covered(ranges: Tuple[List[int], List[int]], pos: int) -> bool:
    starts, ends = ranges
    i = bisect_right(starts, pos) - 1
    return i >= 0 and starts[i] < pos < ends[i]


VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr",
}


class FileContext:
    """Per-file structure shared by every rule that lints the file."""

    def __init__(self, path: Path, text: str, views: FileViews) -> None:
        self.path = path
        self.text = text
        self.views = views
        self._low: Optional[str] = None
        self._ranges: Dict[str, Tuple[List[int], List[int]]] = {}
        self._cache: Dict[str, object] = {}

    @property
    def low(self) -> str:
        if self._low is None:
            self._low = self.text.lower()
        return self._low

    def cached(self, key: str, build: Callable[[], object]) -> object:
        if key not in self._cache:
            self._cache[key] = build()
        return self._cache[key]

    def element_ranges(self, name: str) -> Tuple[List[int], List[int]]:
        """Merged spans of every ``<name>`` element. An element that is never
        closed runs to the end of the file."""
        name = name.lower()
        if name not in self._ranges:
            low = self.low
            n = re.escape(name)
            token = re.compile(r"<(?:(/)" + n + r"\b|" + n + r"(?=[\s>]))")
            stack: List[int] = []
            spans: List[Tuple[int, int]] = []
            for m in token.finditer(low):
                if m.group(1):
                    if stack:
                        spans.append((stack.pop(), m.start()))
                else:
                    stack.append(m.start())
            spans.extend((s, len(low)) for s in stack)
            self._ranges[name] = _merge(spans)
        return self._ranges[name]

    def element_end(self, tag: Tag) -> int:
        """Offset of the closing tag that ends ``tag``'s element. A void or
        self-closing element ends with its own tag."""
        name = tag.name.lower()
        if name in VOID_ELEMENTS or self.text[max(0, tag.end - 2):tag.end] == "/>":
            return tag.end
        key = "tokens:" + name

        def build() -> Tuple[List[int], List[bool]]:
            pos: List[int] = []
            closing: List[bool] = []
            for m in re.finditer(r"<(/?)" + re.escape(name) + r"(?=[\s>/])", self.low):
                pos.append(m.start())
                closing.append(bool(m.group(1)))
            return pos, closing
        pos, closing = self.cached(key, build)  # type: ignore[misc]
        i = bisect_right(pos, tag.start)
        depth = 1
        while i < len(pos):
            depth += -1 if closing[i] else 1
            if depth == 0:
                return pos[i]
            i += 1
        return len(self.text)

    def tree(self) -> Tuple[List[Tag], List[int], List[int]]:
        """Named tags in source order, the end of each element, and the index
        of each element's parent (-1 at the top)."""
        def build() -> Tuple[List[Tag], List[int], List[int]]:
            tags = sorted((t for t in self.views.scan.tags if t.name), key=lambda t: t.start)
            ends = [self.element_end(t) for t in tags]
            parents: List[int] = []
            stack: List[int] = []
            for i, t in enumerate(tags):
                while stack and ends[stack[-1]] <= t.start:
                    stack.pop()
                parents.append(stack[-1] if stack else -1)
                if ends[i] > t.end:
                    stack.append(i)
            return tags, ends, parents
        return self.cached("tree", build)  # type: ignore[return-value]

    def inside(self, pos: int, names: Sequence[str]) -> bool:
        """True when ``pos`` sits inside an element named in ``names``."""
        return any(_covered(self.element_ranges(n), pos) for n in names)

    # Tags

    def tags_by_start(self) -> Dict[int, Tag]:
        return self.cached("tags", lambda: {t.start: t for t in self.views.scan.tags})  # type: ignore[return-value]

    def tag_at(self, pos: int) -> Optional[Tag]:
        """The tag whose attribute list contains ``pos``."""
        tags: List[Tag] = self.cached("tag_list", lambda: sorted(self.views.scan.tags, key=lambda t: t.start))  # type: ignore[assignment]
        starts: List[int] = self.cached("tag_starts", lambda: [t.start for t in tags])  # type: ignore[assignment]
        i = bisect_right(starts, pos) - 1
        if i >= 0 and tags[i].start <= pos < tags[i].end:
            return tags[i]
        return None


def attr_values(text: str, tag: Tag) -> Dict[str, Tuple[str, str]]:
    """Lowercased attribute name to (kind, value) for one tag."""
    out: Dict[str, Tuple[str, str]] = {}
    for a in tag.attrs:
        out.setdefault(a.name.lower(), (a.kind, text[a.vstart:a.vend].strip()))
    return out


def _dynamic(name: str, kind: str) -> bool:
    return kind == "expr" or name.startswith((":", "v-bind:"))


def _ids(ctx: FileContext) -> Tuple[Set[str], Set[str]]:
    """Static id values and dynamic id expressions declared in the file."""
    def build() -> Tuple[Set[str], Set[str]]:
        static: Set[str] = set()
        dynamic: Set[str] = set()
        for tag in ctx.views.scan.tags:
            for a in tag.attrs:
                low = a.name.lower()
                if low not in ("id", ":id", "v-bind:id"):
                    continue
                value = ctx.text[a.vstart:a.vend].strip()
                if not value:
                    continue
                (dynamic if _dynamic(low, a.kind) else static).add(value)
        return static, dynamic
    return ctx.cached("ids", build)  # type: ignore[return-value]


def _label_targets(ctx: FileContext) -> Tuple[Set[str], Set[str]]:
    """Values of ``for`` and ``htmlFor`` on every ``<label>``."""
    def build() -> Tuple[Set[str], Set[str]]:
        static: Set[str] = set()
        dynamic: Set[str] = set()
        for tag in ctx.views.scan.tags:
            if tag.name.lower() != "label":
                continue
            for a in tag.attrs:
                low = a.name.lower()
                if low not in ("for", "htmlfor", ":for", "v-bind:for", ":htmlfor"):
                    continue
                value = ctx.text[a.vstart:a.vend].strip()
                if value:
                    (dynamic if _dynamic(low, a.kind) else static).add(value)
        return static, dynamic
    return ctx.cached("label_for", build)  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# placeholder-as-label
# ---------------------------------------------------------------------------

_EMPTY_EXPR = {"", '""', "''", "``", "undefined", "null", "false"}


def _names_something(kind: str, value: str) -> bool:
    """True when an attribute value is a non-empty name."""
    if kind == "none":
        return False
    value = value.strip()
    if kind == "expr":
        return value not in _EMPTY_EXPR
    return bool(value)


def _id_tags(ctx: FileContext) -> Dict[str, Tag]:
    def build() -> Dict[str, Tag]:
        out: Dict[str, Tag] = {}
        for tag in ctx.views.scan.tags:
            for a in tag.attrs:
                if a.name.lower() == "id" and a.kind == "str":
                    out.setdefault(ctx.text[a.vstart:a.vend].strip(), tag)
        return out
    return ctx.cached("id_tags", build)  # type: ignore[return-value]


def _has_text(ctx: FileContext, tag: Tag) -> bool:
    """True when an element carries a name: text content or aria-label."""
    attrs = attr_values(ctx.text, tag)
    if "aria-label" in attrs and _names_something(*attrs["aria-label"]):
        return True
    return _visible_len(ctx.text[tag.end:ctx.element_end(tag)]) > 0


def input_has_no_name(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An input is named by a ``<label for>`` that matches its id, a wrapping
    ``<label>``, a non-empty ``aria-label``, or ``aria-labelledby`` that
    points to another element in the file that has text. An id on its own
    names nothing. A component (``<Input>``) is named by a non-empty
    ``label`` prop, which it renders as a label."""
    tag = ctx.tags_by_start().get(start)
    if tag is None:
        return True
    attrs = attr_values(ctx.text, tag)
    if tag.name[:1].isupper() and "label" in attrs and _names_something(*attrs["label"]):
        return False
    for key in ("aria-label", ":aria-label", "v-bind:aria-label"):
        if key in attrs and _names_something(*attrs[key]):
            return False
    own_id = attrs.get("id", ("", ""))[1]
    static_ids, dynamic_ids = _ids(ctx)
    for key in ("aria-labelledby", ":aria-labelledby", "v-bind:aria-labelledby"):
        if key in attrs:
            kind, value = attrs[key]
            if _dynamic(key, kind):
                if value in dynamic_ids and value != attrs.get("id", ("", ""))[1]:
                    return False
                continue
            refs = value.split()
            targets = _id_tags(ctx)
            if refs and all(r != own_id and r in targets and _has_text(ctx, targets[r]) for r in refs):
                return False
    static_for, dynamic_for = _label_targets(ctx)
    for key in ("id", ":id", "v-bind:id"):
        if key in attrs:
            kind, value = attrs[key]
            if value and value in (dynamic_for if _dynamic(key, kind) else static_for):
                return False
    return not ctx.inside(start, ("label",))


# ---------------------------------------------------------------------------
# inline-svg-no-aria
# ---------------------------------------------------------------------------

def _truthy_hidden(ctx: FileContext, tag: Tag) -> bool:
    for a in tag.attrs:
        if a.name.lower() in ("aria-hidden", ":aria-hidden"):
            value = ctx.text[a.vstart:a.vend].strip().strip("'\"").lower()
            return a.kind == "none" or value in ("true", "")
    return False


def _hidden_ranges(ctx: FileContext) -> Tuple[List[int], List[int]]:
    def build() -> Tuple[List[int], List[int]]:
        spans = [
            (tag.start, ctx.element_end(tag)) for tag in ctx.views.scan.tags
            if tag.name and _truthy_hidden(ctx, tag)
        ]
        return _merge(spans)
    return ctx.cached("hidden", build)  # type: ignore[return-value]


def svg_not_hidden(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An SVG inside an ``aria-hidden="true"`` ancestor is hidden already."""
    return not _covered(_hidden_ranges(ctx), start)


# ---------------------------------------------------------------------------
# CSS rule blocks
# ---------------------------------------------------------------------------

@dataclass
class Block:
    start: int                  # offset of the opening brace in the view
    end: int                    # offset of the closing brace
    selectors: List[str]
    atrules: Tuple[str, ...]
    body: str                   # own declarations, nested blocks left out


def _split_top(s: str, sep: str = ",") -> List[str]:
    out: List[str] = []
    depth = 0
    cur: List[str] = []
    for c in s:
        if c in "([":
            depth += 1
        elif c in ")]":
            depth = max(0, depth - 1)
        if c == sep and depth == 0:
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
    out.append("".join(cur).strip())
    return [x for x in out if x]


def css_blocks(text: str) -> List[Block]:
    """Every ``{ }`` block in a CSS view, with nested selectors resolved."""
    blocks: List[Block] = []
    stack: List[dict] = []
    seg = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in "\"'":
            j = text.find(c, i + 1)
            i = n if j == -1 else j + 1
            continue
        if c == "{":
            prelude = " ".join(text[seg:i].split())
            parent = stack[-1] if stack else None
            if prelude.startswith("@"):
                sels = parent["selectors"] if parent else []
                atrules = (parent["atrules"] if parent else ()) + (prelude.lower(),)
            else:
                own = _split_top(prelude)
                psel = parent["selectors"] if parent else []
                if psel:
                    sels = [s.replace("&", p) if "&" in s else p + " " + s for p in psel for s in own]
                else:
                    sels = own
                atrules = parent["atrules"] if parent else ()
            stack.append({"start": i, "selectors": sels, "atrules": atrules, "decls": []})
            seg = i + 1
        elif c == ";":
            if stack:
                stack[-1]["decls"].append(text[seg:i])
            seg = i + 1
        elif c == "}":
            if stack:
                top = stack.pop()
                top["decls"].append(text[seg:i])
                blocks.append(Block(top["start"], i, top["selectors"], top["atrules"],
                                    ";".join(top["decls"])))
            seg = i + 1
        i += 1
    while stack:
        top = stack.pop()
        top["decls"].append(text[seg:n])
        blocks.append(Block(top["start"], n, top["selectors"], top["atrules"], ";".join(top["decls"])))
    blocks.sort(key=lambda b: b.start)
    return blocks


def _blocks(ctx: FileContext, view: View) -> Tuple[List[Block], List[int]]:
    def build() -> Tuple[List[Block], List[int]]:
        blocks = css_blocks(view.text)
        return blocks, [b.start for b in blocks]
    return ctx.cached("blocks:%d" % id(view), build)  # type: ignore[return-value]


def block_at(ctx: FileContext, view: View, pos: int) -> Optional[Block]:
    """The innermost block whose braces enclose ``pos``. Blocks are sorted by
    their opening brace, so the first enclosing block found walking back is
    the innermost one."""
    blocks, starts = _blocks(ctx, view)
    i = bisect_right(starts, pos) - 1
    while i >= 0:
        b = blocks[i]
        if b.start < pos <= b.end:
            return b
        i -= 1
    return None


# Selector anatomy

@lru_cache(maxsize=4096)
def compounds(selector: str) -> List[str]:
    """Split a complex selector into its compound selectors."""
    out: List[str] = []
    depth = 0
    cur: List[str] = []
    i = 0
    s = selector.strip()
    while i < len(s):
        c = s[i]
        if c in "([":
            depth += 1
        elif c in ")]":
            depth = max(0, depth - 1)
        if depth == 0 and (c.isspace() or c in ">+~"):
            if cur:
                out.append("".join(cur))
                cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    if cur:
        out.append("".join(cur))
    return out


@lru_cache(maxsize=4096)
def pseudos(compound: str) -> List[Tuple[str, str]]:
    """Top-level pseudo-classes of a compound as (name, argument)."""
    out: List[Tuple[str, str]] = []
    i = 0
    n = len(compound)
    while i < n:
        c = compound[i]
        if c == "\\":
            i += 2
            continue
        if c == "[":
            j = compound.find("]", i)
            i = n if j == -1 else j + 1
            continue
        if c == ":":
            j = i + 1
            if j < n and compound[j] == ":":
                j += 1
            k = j
            while k < n and (compound[k].isalnum() or compound[k] == "-"):
                k += 1
            name = compound[j:k].lower()
            arg = ""
            if k < n and compound[k] == "(":
                depth = 0
                m = k
                while m < n:
                    if compound[m] == "(":
                        depth += 1
                    elif compound[m] == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    m += 1
                arg = compound[k + 1:m]
                k = m + 1
            out.append((name, arg))
            i = k
            continue
        i += 1
    return out


def _strip_pseudos(compound: str) -> str:
    out: List[str] = []
    i = 0
    n = len(compound)
    while i < n:
        c = compound[i]
        if c == "\\":
            out.append(compound[i:i + 2])
            i += 2
            continue
        if c == "[":
            j = compound.find("]", i)
            j = n if j == -1 else j + 1
            out.append(compound[i:j])
            i = j
            continue
        if c == ":":
            k = i + 1
            if k < n and compound[k] == ":":
                k += 1
            while k < n and (compound[k].isalnum() or compound[k] == "-"):
                k += 1
            if k < n and compound[k] == "(":
                depth = 0
                while k < n:
                    if compound[k] == "(":
                        depth += 1
                    elif compound[k] == ")":
                        depth -= 1
                        if depth == 0:
                            k += 1
                            break
                    k += 1
            i = k
            continue
        out.append(c)
        i += 1
    return "".join(out)


_TOKEN = re.compile(r"\.((?:[\w-]|\\.)+)|#((?:[\w-]|\\.)+)|\[([^\]]*)\]")


@lru_cache(maxsize=4096)
def tokens(compound: str) -> FrozenSet[str]:
    """Tag, classes, ids and attribute tests of a compound, pseudos left out."""
    bare = _strip_pseudos(compound)
    out: Set[str] = set()
    head = re.match(r"[A-Za-z][\w-]*", bare)
    if head:
        out.add(head.group(0).lower())
    for m in _TOKEN.finditer(bare):
        if m.group(1):
            out.add("." + m.group(1))
        elif m.group(2):
            out.add("#" + m.group(2))
        else:
            out.add("[" + re.sub(r"[\s'\"]", "", m.group(3)).lower() + "]")
    return frozenset(out)


def _focus_kind(compound: str) -> str:
    """"self" when the compound matches its own focus state, "ancestor" when it
    matches focus inside it, "" otherwise."""
    kind = ""
    for name, arg in pseudos(compound):
        if name in ("focus", "focus-visible"):
            return "self"
        if name in ("is", "where") and re.search(r":focus(?:-visible)?\b(?!-within)", arg):
            return "self"
        if name == "focus-within" or (name == "has" and ":focus" in arg):
            kind = "ancestor"
    return kind


# ---------------------------------------------------------------------------
# outline-none-no-focus-visible
# ---------------------------------------------------------------------------

_ZERO = re.compile(r"^-?0(?:\.0+)?(?:px|em|rem|%)?$")
_NO_PAINT = {"none", "hidden", "transparent", "initial", "unset"}
_RING_CLASS = re.compile(
    r"(?:^|\s)(?:[\w-]+:)*focus(?:-visible|-within)?:"
    r"(?:ring|shadow|border)(?!-(?:none|0|offset|transparent)\b)(?:-[\w\[\]#().,/%-]+)?(?=\s|$)",
    re.I,
)


def _declarations(body: str) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for part in body.split(";"):
        if ":" in part:
            prop, value = part.split(":", 1)
            out.append((prop.strip().lower(), value.replace("!important", "").strip().lower()))
    return out


def _paints(value: str) -> bool:
    """True when a shorthand value draws something visible."""
    words = value.split()
    if not words:
        return False
    if any(w in _NO_PAINT for w in words):
        return False
    return not all(_ZERO.match(w) for w in words)


_LENGTH = re.compile(r"^-?(?:\d+\.?\d*|\.\d+)(?:px|em|rem|%)?$")


def _shadow_has_size(value: str) -> bool:
    """A shadow draws only when one layer has a non-zero blur or spread;
    ``0 0 0 0 #06c`` paints nothing. Offsets alone count too."""
    for layer in _split_top(value):
        lengths = [w for w in layer.split() if _LENGTH.match(w)]
        if not lengths or any(not _ZERO.match(w) for w in lengths):
            return True
    return False


def ring_kind(body: str) -> str:
    """"outline" or "other" when a block's own declarations draw a visible
    focus indicator; "" when they do not. ``outline: none``, ``border: 0``,
    ``box-shadow: none`` and transparent colors draw nothing."""
    kind = ""
    for prop, value in _declarations(body):
        if prop == "outline" or prop == "outline-style":
            if _paints(value):
                return "outline"
        elif prop == "box-shadow":
            if _paints(value) and _shadow_has_size(value):
                kind = kind or "other"
        elif prop.startswith("border") and not re.search(r"radius|image|collapse|spacing", prop):
            if _paints(value):
                kind = kind or "other"
    return kind


def _specificity(selector: str) -> Tuple[int, int, int]:
    ids = classes = tags = 0
    for part in compounds(selector):
        for name, arg in pseudos(part):
            if name in ("not", "is", "has"):
                inner = [_specificity(x) for x in _split_top(arg)]
                if inner:
                    top = max(inner)
                    ids, classes, tags = ids + top[0], classes + top[1], tags + top[2]
            elif name != "where":
                classes += 1
        for tok in tokens(part):
            if tok.startswith("#"):
                ids += 1
            elif tok.startswith((".", "[")):
                classes += 1
            else:
                tags += 1
    return ids, classes, tags


def _sub(ring: FrozenSet[str], removal: FrozenSet[str]) -> bool:
    """A ring compound covers a removal compound when its tokens are a subset:
    it is as general or more. An empty compound (``:focus-visible``, ``*``)
    covers any element; specificity then decides who wins."""
    return ring <= removal


def _covers(ring: List[FrozenSet[str]], removal: List[FrozenSet[str]]) -> bool:
    """Right-to-left match: the ring's subject covers the removal's subject and
    every ring ancestor covers some removal ancestor, in order."""
    if not ring or not removal or not _sub(ring[-1], removal[-1]):
        return False
    j = len(removal) - 2
    for r in reversed(ring[:-1]):
        while j >= 0 and not r <= removal[j]:
            j -= 1
        if j < 0:
            return False
        j -= 1
    return True


@dataclass
class Ring:
    kind: str                       # "self" or "ancestor"
    cond: FrozenSet[str]            # @media, @supports and @container around the ring
    important: bool                 # the ring's outline is !important
    paint: str                      # "outline" or "other"
    toks: List[FrozenSet[str]]      # tokens per compound
    spec: Tuple[int, int, int]
    at: int                         # block offset, for source order
    anchor: int = -1                # ancestor rings: compound index of the anchor
    within: bool = False            # :focus-within (the anchor may be the element itself)
    inner: Optional[FrozenSet[str]] = None  # :has() argument subject tokens


_IMPORTANT_OUTLINE = re.compile(r"(?:^|;)\s*outline(?:-style)?\s*:[^;]*!\s*important", re.I)
_ALT = re.compile(r":(?:is|where|matches)\(", re.I)


def _conditions(block: Block) -> FrozenSet[str]:
    return frozenset(a for a in block.atrules if a.startswith(("@media", "@supports", "@container")))


@lru_cache(maxsize=4096)
def _alternatives(selector: str) -> Tuple[str, ...]:
    """Expand ``:is()`` and ``:where()`` into one selector per argument, so
    ``:where(.btn, .icon-btn):focus-visible`` is read as two rings."""
    m = _ALT.search(selector)
    if not m:
        return (selector,)
    depth = 0
    for k in range(m.end() - 1, len(selector)):
        if selector[k] == "(":
            depth += 1
        elif selector[k] == ")":
            depth -= 1
            if depth == 0:
                break
    else:
        return (selector,)
    out: List[str] = []
    for arg in _split_top(selector[m.end():k]):
        out.extend(_alternatives(selector[:m.start()] + arg + selector[k + 1:]))
        if len(out) >= 16:
            break
    return tuple(out) or (selector,)


def _rings(ctx: FileContext, view: View) -> Tuple[Dict[FrozenSet[str], List[Ring]], Dict[str, List[Ring]], List[Ring]]:
    """Focus rings in the view, indexed once per file: self rings by the set
    of every token in their selector, ancestor rings by anchor token, plus
    every ancestor ring."""
    def build():
        by_tokens: Dict[FrozenSet[str], List[Ring]] = {}
        by_anchor: Dict[str, List[Ring]] = {}
        ancestors: List[Ring] = []
        for b in _blocks(ctx, view)[0]:
            if not b.selectors:
                continue
            paint = ring_kind(b.body)
            if not paint:
                continue
            cond = _conditions(b)
            important = bool(_IMPORTANT_OUTLINE.search(b.body))
            for sel, alt in ((x, y) for x in b.selectors for y in _alternatives(x)):
                parts = compounds(alt)
                if not parts:
                    continue
                toks = [tokens(x) for x in parts]
                if _focus_kind(parts[-1]) == "self":
                    ring = Ring("self", cond, important, paint, toks, _specificity(sel), b.start)
                    by_tokens.setdefault(frozenset().union(*toks), []).append(ring)
                    continue
                last = len(parts) - 1
                if _focus_kind(parts[last]) != "ancestor" or not toks[last]:
                    continue
                inner = None
                within = False
                for name, arg in pseudos(parts[last]):
                    if name == "focus-within":
                        within = True
                    elif name == "has" and ":focus" in arg:
                        first = _split_top(arg)[:1]
                        sub = compounds(first[0].lstrip(">+~ ")) if first else []
                        inner = (tokens(sub[-1]) if sub else frozenset()) or None
                ring = Ring("ancestor", cond, important, paint, toks, _specificity(sel), b.start, last, within, inner)
                ancestors.append(ring)
                for key in toks[last]:
                    by_anchor.setdefault(key, []).append(ring)
        return by_tokens, by_anchor, ancestors
    return ctx.cached("rings:%d" % id(view), build)  # type: ignore[return-value]


def _tag_tokens(ctx: FileContext, tag: Tag) -> FrozenSet[str]:
    out = {tag.name.lower()}
    for a in tag.attrs:
        low = a.name.lower()
        if a.kind != "str" or low.startswith(":"):
            continue
        value = ctx.text[a.vstart:a.vend]
        if low in ("class", "classname"):
            out.update("." + c for c in value.split())
        elif low == "id":
            out.add("#" + value.strip())
    return frozenset(out)


def _plain(toks: FrozenSet[str]) -> FrozenSet[str]:
    return frozenset(t for t in toks if not t.startswith("["))


def _matching_elements(ctx: FileContext, removal: List[FrozenSet[str]]) -> List[int]:
    """Indexes of the markup elements the removal selector matches."""
    tags, _ends, parents = ctx.tree()
    want = [_plain(t) for t in removal]
    out: List[int] = []
    for i, tag in enumerate(tags):
        if not want[-1] <= _tag_tokens(ctx, tag):
            continue
        j = len(want) - 2
        k = parents[i]
        while j >= 0 and k >= 0:
            if want[j] <= _tag_tokens(ctx, tags[k]):
                j -= 1
            k = parents[k]
        if j < 0:
            out.append(i)
    return out


def _markup_wraps(ctx: FileContext, ring: Ring, matched: List[int]) -> bool:
    """True when every element the removal matches sits inside an element
    the ring's anchor matches (or is one, for ``:focus-within``)."""
    if not matched:
        return False
    tags, _ends, parents = ctx.tree()
    anchor = _plain(ring.toks[ring.anchor])
    for i in matched:
        k = i if ring.within else parents[i]
        while k >= 0 and not anchor <= _tag_tokens(ctx, tags[k]):
            k = parents[k]
        if k < 0:
            return False
    return True


def _removal_has_ring(ctx: FileContext, view: View, selector: str, at: int,
                      cond: FrozenSet[str] = frozenset(), important: bool = False) -> bool:
    parts = compounds(selector)
    if not parts:
        return False
    removal = [tokens(x) for x in parts]
    spec = _specificity(selector)
    by_tokens, by_anchor, ancestors = _rings(ctx, view)

    def applies(ring: Ring) -> bool:
        # A ring inside a media query the removal is not in (print, dark
        # theme, a breakpoint) leaves the removal bare elsewhere.
        if not ring.cond <= cond:
            return False
        return not (important and ring.paint == "outline" and not ring.important)
    # A ring that covers the removal uses only tokens the removal has, so
    # rings are looked up by every subset of the removal's tokens.
    pool = sorted(frozenset().union(*removal))
    if len(pool) <= 10:
        keys = (frozenset(c) for n in range(len(pool) + 1) for c in combinations(pool, n))
        self_rings = [r for k in keys for r in by_tokens.get(k, ())]
    else:
        self_rings = [r for rs in by_tokens.values() for r in rs]
    for ring in self_rings:
        if not applies(ring) or not _covers(ring.toks, removal):
            continue
        if ring.paint == "outline" and (ring.spec, ring.at) < (spec, at):
            continue  # the removal is more specific (or later) and wins
        return True

    def inner_ok(ring: Ring) -> bool:
        return applies(ring) and (ring.inner is None or _sub(ring.inner, removal[-1]))
    candidates = {id(r): r for t in set().union(*removal) for r in by_anchor.get(t, ())}
    last = len(removal) - 1
    for ring in candidates.values():
        anchor = ring.toks[ring.anchor]
        if not inner_ok(ring):
            continue
        if any(anchor <= removal[k] for k in range(last + (1 if ring.within else 0))):
            return True
    if ctx.views.scan.tags and ancestors:
        matched = _matching_elements(ctx, removal)
        for ring in ancestors:
            if inner_ok(ring) and _markup_wraps(ctx, ring, matched):
                return True
    return False


def outline_without_ring(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Decide per rule block. A removed outline passes only when a focus rule
    that covers the whole removal selector draws a visible ring (outline,
    box-shadow or border), or a ``:focus-within`` or ``:has(:focus-visible)``
    rule on an ancestor of that same element does."""
    tag = ctx.tag_at(start)
    if tag is not None:
        # Inline style: only the element's own classes can add a ring.
        for a in tag.attrs:
            if a.name.lower() in ("class", "classname", ":class") and _RING_CLASS.search(ctx.text[a.vstart:a.vend]):
                return False
        return True
    block = block_at(ctx, view, match.start())
    if block is None or not block.selectors:
        return True
    own_ring = bool(ring_kind(block.body))
    cond = _conditions(block)
    important = bool(_IMPORTANT_OUTLINE.search(block.body))
    for sel in block.selectors:
        if re.search(r":not\(\s*:focus-visible\s*\)", sel):
            continue  # removed only for mouse focus: the keyboard ring stays
        for alt in _alternatives(sel):
            parts = compounds(alt)
            if own_ring and parts and _focus_kind(parts[-1]):
                continue
            key = "removal:%d:%s:%s:%s" % (id(view), alt, sorted(cond), important)
            if not ctx.cached(key, lambda alt=alt: _removal_has_ring(ctx, view, alt, block.start, cond, important)):
                return True
    return False


# ---------------------------------------------------------------------------
# hover-only-card-actions
# ---------------------------------------------------------------------------

_HOVER_MEDIA = re.compile(r"\(\s*hover\s*:\s*hover\s*\)|\(\s*any-hover\s*:\s*hover\s*\)", re.I)
_OPACITY_0 = re.compile(r"opacity\s*:\s*0(?![.\d])", re.I)
_OPACITY_1 = re.compile(r"opacity\s*:\s*1(?![.\d])", re.I)


def _in_hover_media(block: Optional[Block]) -> bool:
    return block is not None and any(_HOVER_MEDIA.search(a) for a in block.atrules if a.startswith("@media"))


def hover_only_reveal(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Actions hidden until hover pass when the hiding sits inside
    ``@media (hover: hover)``, or when a focus rule on the same card reveals
    them too."""
    hover_block = block_at(ctx, view, match.end() - 1)
    hidden = _OPACITY_0.search(match.group(0))
    hidden_block = block_at(ctx, view, match.start() + hidden.start()) if hidden else None
    if hidden_block is None and hover_block is not None:
        bases = {" ".join(s.replace(":hover", " ").split()) for s in hover_block.selectors}
        for b in _blocks(ctx, view)[0]:
            if _OPACITY_0.search(b.body) and any(" ".join(s.split()) in bases for s in b.selectors):
                hidden_block = b
                break
    if _in_hover_media(hidden_block or hover_block):
        return False
    if hover_block is None:
        return True
    hover_sels = [compounds(s) for s in hover_block.selectors if ":hover" in s]
    for b in _blocks(ctx, view)[0]:
        if not _OPACITY_1.search(b.body):
            continue
        for sel in b.selectors:
            parts = compounds(sel)
            focus_at = [p for p in parts if _focus_kind(p)]
            if not parts or not focus_at:
                continue
            for hs in hover_sels:
                if not hs or not (tokens(hs[-1]) & tokens(parts[-1])):
                    continue
                if any(tokens(f) & tokens(h) for f in focus_at for h in hs):
                    return False
    return True


# ---------------------------------------------------------------------------
# imagery-mandatory-missing
# ---------------------------------------------------------------------------

_TAGS = re.compile(r"<[^>]*>")


def _visible_len(s: str) -> int:
    return len("".join(_TAGS.sub(" ", s).split()))


def _region(low: str, name: str) -> Optional[Tuple[int, int]]:
    m = re.search(r"<" + name + r"\b[^>]*>", low)
    if not m:
        return None
    close = low.rfind("</" + name)
    return m.end(), (close if close > m.end() else len(low))


def _content_share(ctx: FileContext, spans: List[Tuple[int, int]], text: str, s: int, e: int) -> int:
    starts, ends = _merge([(max(a, s), min(b, e)) for a, b in spans if b > s and a < e])
    return sum(_visible_len(text[a:b]) for a, b in zip(starts, ends))


_CTA = re.compile(
    r"<(?:a|button)\b[^>]*(?:\bclass\s*=\s*[\"'][^\"']*\b(?:btn|button|cta)\b"
    r"|\bhref\s*=\s*[\"'][^\"']*(?:sign-?up|register|get-started|start|trial|demo|pricing|contact|book))",
    re.I,
)


def _page_text(ctx: FileContext) -> str:
    """The file lowercased, with comments, scripts and styles blanked in
    place so offsets still match the file."""
    def build() -> str:
        chars = list(ctx.low)
        for a, b in list(ctx.views.scan.blanks) + [(x, y) for _, x, y in ctx.views.scan.raw]:
            chars[a:b] = " " * (b - a)
        return "".join(chars)
    return ctx.cached("page_text", build)  # type: ignore[return-value]


def _has_hero(low: str) -> bool:
    """An h1 followed by a call to action (a button-styled link or button, or
    a sign-up, trial, demo, pricing or contact link) before the next h2 or
    form. A form's own submit button is not a hero."""
    m = re.search(r"<h1\b", low)
    if not m:
        return False
    nxt = re.search(r"<(?:h2|form)\b", low[m.end():])
    stop = m.end() + (nxt.start() if nxt else 2000)
    return bool(_CTA.search(low, m.end(), min(stop, m.end() + 2000)))


def _sidebars(ctx: FileContext) -> List[Tuple[int, int]]:
    """Navigation columns beside the content: an ``<aside>``, or a ``<nav>``
    or ``role="navigation"`` inside ``<main>`` or named as a sidebar or table
    of contents, holding three or more links, not inside a header, footer,
    section or article."""
    tags, ends, parents = ctx.tree()
    out: List[Tuple[int, int]] = []
    for i, tag in enumerate(tags):
        name = tag.name.lower()
        attrs = attr_values(ctx.text, tag)
        is_nav = name == "nav" or attrs.get("role", ("", ""))[1].lower() == "navigation"
        if name != "aside" and not is_nav:
            continue
        chain = []
        k = parents[i]
        while k >= 0:
            chain.append(tags[k].name.lower())
            k = parents[k]
        if {"header", "footer", "section", "article"} & set(chain):
            continue
        named = re.search(r"side|toc|docs", attrs.get("class", ("", ""))[1] + " " + attrs.get("id", ("", ""))[1], re.I)
        if name != "aside" and "main" not in chain and not named:
            continue
        links = sum(1 for t in tags[i + 1:] if t.start < ends[i] and t.name.lower() == "a")
        if links >= 3:
            out.append((tag.start, ends[i]))
    return out


def document_or_app_surface(ctx: FileContext) -> bool:
    """True when the page is a document or an app surface, not a landing page.

    1. A page with no text (a single-page app root) or ``role="application"``
       is an app.
    2. A hero (an h1 followed by a call to action) makes it a landing page.
    3. A sidebar or table of contents beside the content makes it a docs page
       or an app shell.
    4. Otherwise, with navigation left out, the page is a document or app when
       one article, form, table, code listing, list or grid holds at least 60
       percent of the main text, or those regions do together. A form that
       wraps several sections is the page itself and does not count."""
    def build() -> bool:
        low = _page_text(ctx)
        s, e = _region(low, "main") or _region(low, "body") or (0, len(low))
        if not _visible_len(low[s:e]) or re.search(r"role\s*=\s*[\"']?application\b", low):
            return True
        if _has_hero(low[s:e]):
            return False
        side = _sidebars(ctx)
        if side:
            return True
        chars = list(low)
        for name in ("nav", "header", "footer"):
            for a, b in zip(*ctx.element_ranges(name)):
                if s <= a < e:
                    chars[a:b] = " " * (b - a)
        low = "".join(chars)
        total = _visible_len(low[s:e])
        if not total:
            return True
        grids = [
            (t.start, ctx.element_end(t)) for t in ctx.views.scan.tags
            if re.fullmatch(r"grid|treegrid|listbox|log", attr_values(ctx.text, t).get("role", ("", ""))[1].lower())
        ]
        regions: List[Tuple[int, int]] = list(grids)
        for name in ("article", "form", "table", "pre", "ul", "ol"):
            for a, b in zip(*ctx.element_ranges(name)):
                if not s <= a < e:
                    continue
                if name == "form" and len(re.findall(r"<section\b", low[a:b])) >= 2:
                    continue  # a form wrapping the page's sections is the page
                if name != "article":
                    regions.append((a, b))
                if _visible_len(low[a:min(b, e)]) >= 0.6 * total:
                    return True
        for a, b in grids:
            if s <= a < e and _visible_len(low[a:min(b, e)]) >= 0.6 * total:
                return True
        return _content_share(ctx, regions, low, s, e) >= 0.6 * total
    return bool(ctx.cached("doc_surface", build))


def page_needs_imagery(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    return not document_or_app_surface(ctx)


# ---------------------------------------------------------------------------
# css-import-render-blocking
# ---------------------------------------------------------------------------

_IMPORT_URL = re.compile(r"@import\s+(?:url\(\s*)?[\"']?([^\"')\s;]+)", re.I)
_TOKEN_NAME = re.compile(r"(?:^|[/_.-])(?:design-?)?(?:tokens?|variables|vars|custom-properties)(?:[/_.-]|$)", re.I)
_CUSTOM_PROP = re.compile(r"--[\w-]+\s*:[^;{}]*;?")


# Declarations a token file carries besides custom properties: color-scheme,
# which the engine writes with every scheme so native controls follow it, and
# the descriptors of an @property rule. Neither styles an element.
_TOKEN_EXTRAS = re.compile(r"(?<![\w-])(?:color-scheme|syntax|inherits|initial-value)\s*:[^;{}]*;?", re.I)


def _custom_properties_only(css: str) -> bool:
    """True when a stylesheet only defines tokens: custom properties, with
    color-scheme and @property descriptors, under any selector or @media."""
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    if "--" not in css:
        return False
    rest = _CUSTOM_PROP.sub(" ", css)
    rest = _TOKEN_EXTRAS.sub(" ", rest)
    rest = re.sub(r"[^{};]*\{", " ", rest)
    rest = rest.replace("}", " ").replace(";", " ")
    return not rest.strip()


def token_definitions(ctx: FileContext) -> Optional[Tuple[List[int], List[int]]]:
    """The custom-property definitions of a token layer, as merged spans of
    the original file; None when the file is not a token layer.

    A token layer is a stylesheet made mostly of custom-property definitions:
    at least three, and at least nine in ten of its declarations
    (color-scheme and @property descriptors left out), so a page stylesheet
    padded with custom properties is still a page stylesheet. Content decides, never the file name, so
    a client's own tokens file and the engine's tokens.css are read the same
    way, and a page's stylesheet with a few custom properties is not one."""
    def build() -> Optional[Tuple[List[int], List[int]]]:
        if ctx.views.kind != "css":
            return None
        view = ctx.views.get("css")
        if view is None or "--" not in view.text:
            return None
        custom = other = 0
        for block in _blocks(ctx, view)[0]:
            for prop, _value in _declarations(block.body):
                if prop.startswith("--"):
                    custom += 1
                elif prop not in ("color-scheme", "syntax", "inherits", "initial-value") and prop:
                    other += 1
        if custom < 3 or custom < 9 * other:
            return None
        spans = [(view.orig(m.start()), view.orig(max(m.start(), m.end() - 1)) + 1)
                 for m in re.finditer(r"(?<![\w-])--[\w-]+\s*:[^;{}]*", view.text)]
        return _merge(spans)
    return ctx.cached("token_definitions", build)  # type: ignore[return-value]


def in_spans(spans: Tuple[List[int], List[int]], pos: int) -> bool:
    starts, ends = spans
    i = bisect_right(starts, pos) - 1
    return i >= 0 and starts[i] <= pos < ends[i]


def import_blocks_render(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A local stylesheet of design tokens (custom properties only) may be
    imported; any other ``@import`` serializes a render-blocking fetch."""
    m = _IMPORT_URL.match(view.text, match.start())
    if not m:
        return True
    url = m.group(1)
    if re.match(r"[a-z][a-z0-9+.-]*:|//", url, re.I):
        return True
    path = url.split("?", 1)[0].split("#", 1)[0]
    try:
        target = (ctx.path.parent / path) if not path.startswith("/") else None
        if target is not None and target.is_file() and target.stat().st_size <= 512_000:
            # The content decides when it can be read: a tokens.css with
            # ordinary rules in it is not a token file.
            return not _custom_properties_only(target.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        pass
    return not _TOKEN_NAME.search(Path(path).name.rsplit(".", 1)[0])


# ---------------------------------------------------------------------------
# decorative-accent-ruler
# ---------------------------------------------------------------------------
# An eyebrow is text only. The ornament beside it takes many forms: a
# pseudo-element with a size or a border, an empty span or i, an edge on the
# label, a background line, an SVG line or dot, or a dash typed into the
# text. The regex passes find the candidates (named groups tell them apart)
# and these checks decide. Real separators stay clean: an hr, table rules, a
# card's own edge, a full-width underline, list markers and icon glyphs.

_EYEBROW = re.compile(
    r"(?:^|[_-])(?:eyebrow|kicker|overline|pre-?title|pre-?heading|super-?head(?:ing|line)?"
    r"|section-label|section-tag)(?:$|[_-])"
    r"|(?-i:(?<=[a-z])(?:Eyebrow|Kicker|Overline|Pretitle)(?![a-z]))", re.I)
_TRACKED = re.compile(r"^tracking-(?:wide|wider|widest|\[[\d.]+(?:em|rem|px)\])$")
_ICONISH = re.compile(
    r"(?:^|[_-])(?:icon|ico|glyph|symbol|emoji|avatar|flag|logo|sr-only|visually-hidden|spinner"
    r"|arrow|chevron|caret)(?:$|[_-])"
    r"|^(?:fa|fas|far|fab|fal|fad|bi|ph|ri|mdi|la|lucide|material-symbols[\w-]*|material-icons)$"
    r"|^(?:fa|bi|ph|ri|mdi|la|lucide|i)-", re.I)
# Selectors that draw a control or an icon out of pseudo-elements: their short
# bars are glyph strokes, not ornament.
_CONTROLISH = re.compile(
    r"burger|menu|toggle|icon|close|check|chevron|arrow|caret|spinner|loader|loading|radio"
    r"|switch|slider|thumb|handle|progress|track|knob|tick|cross|plus|minus|bullet|marker"
    r"|step|timeline|legend|swatch|status|item", re.I)
_DASHES = set("\u2014\u2013\u2015\u2012\u2010\u2011-\u2022\u00b7\u25cf\u25aa\u25a0\u2219~\u2500\u2501")
_CSS_STRING = re.compile(r"\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)'", re.S)
_CSS_ESCAPE = re.compile(r"\\([0-9a-fA-F]{1,6})\s?|\\(.)", re.S)
_THIN_VAR = re.compile(r"^var\(\s*--[\w-]*(?:border|line|rule|stroke|hairline|divider|separator)", re.I)
_SHORT_VAR = re.compile(r"^var\(\s*--[\w-]*(?:space|size|gap|spacing|inset)", re.I)
_LENGTH_VALUE = re.compile(r"^(-?\d*\.?\d+)(px|rem|em|ch)?$")
_WIDTHS = ("width", "inline-size", "min-width", "min-inline-size")
_HEIGHTS = ("height", "block-size", "min-height", "min-block-size")
_BLOCK_SIDES = ("border-top", "border-bottom", "border-block-start", "border-block-end",
                "border-block")
_DRAWS = _WIDTHS + _HEIGHTS + ("border", "background", "background-color", "background-image",
                               "box-shadow", "outline")
_SHAPES = ("line", "path", "rect", "circle", "ellipse", "polyline", "polygon")
_SVG_OPAQUE = ("use", "image", "text", "foreignobject")


def _css_string(value: str) -> Optional[str]:
    """The text a ``content`` value renders, escapes resolved; None when the
    value holds no string (``none``, ``counter()``, ``attr()``)."""
    parts = _CSS_STRING.findall(value)
    if not parts or re.search(r"\b(?:counter|counters|attr|url)\(", value):
        return None

    def unescape(s: str) -> str:
        return _CSS_ESCAPE.sub(lambda m: chr(int(m.group(1), 16)) if m.group(1) else m.group(2), s)
    return "".join(unescape(a or b) for a, b in parts)


def _dashy(s: str) -> bool:
    s = s.strip()
    return bool(s) and all(c in _DASHES or c.isspace() for c in s)


def _length_px(value: str) -> Optional[float]:
    m = _LENGTH_VALUE.match(value.strip())
    if not m:
        return None
    n = float(m.group(1))
    unit = m.group(2) or ("px" if n == 0 else "")
    if unit == "px":
        return n
    if unit in ("rem", "em"):
        return n * 16
    if unit == "ch":
        return n * 8
    return None


def _thin(value: str) -> bool:
    px = _length_px(value)
    if px is not None:
        return 0 < px <= 4
    return bool(_THIN_VAR.match(value.strip()))


def _short(value: str) -> bool:
    px = _length_px(value)
    if px is not None:
        return 6 <= px <= 160
    return bool(_SHORT_VAR.match(value.strip()))


def _decl_map(body: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for prop, value in _declarations(body):
        out[prop] = value
    return out


def _first(decls: Dict[str, str], props: Sequence[str]) -> Optional[str]:
    for p in props:
        if p in decls:
            return decls[p]
    return None


def _full_bleed(decls: Dict[str, str]) -> bool:
    """The pseudo-element spans its box: an overlay, an edge or a full-width
    underline, not a short mark."""
    zero = lambda p: p in decls and all(_ZERO.match(w) for w in decls[p].split())  # noqa: E731
    if zero("inset") or zero("inset-inline"):
        return True
    if (zero("left") and zero("right")) or (zero("inset-inline-start") and zero("inset-inline-end")):
        return True
    width = _first(decls, ("width", "inline-size"))
    return bool(width and re.match(r"^(?:100%|100vw|auto|fit-content|max-content|stretch)$", width))


def _painted(decls: Dict[str, str]) -> bool:
    for p in ("background", "background-color", "background-image"):
        if p in decls and _paints(decls[p]) and decls[p] not in ("none",):
            return True
    return False


def _draws_line(decls: Dict[str, str]) -> bool:
    """A short horizontal line: a thin, short painted box, or a short box with
    a painted block-side border."""
    if any(p.startswith("animation") for p in decls):
        return False
    if re.search(r"rotate|skew|matrix", decls.get("transform", "")) or "rotate" in decls:
        return False
    if _full_bleed(decls):
        return False
    flex = decls.get("flex", "").split()
    width = _first(decls, _WIDTHS) or decls.get("flex-basis") or (flex[2] if len(flex) == 3 else None)
    height = _first(decls, _HEIGHTS)
    thin = height is not None and _thin(height)
    if width is None or not (_short(width) or (thin and width.startswith(("var(", "calc(")))):
        return False
    if thin and (_painted(decls) or "border" in decls):
        return True
    flat = height is None or _thin(height) or _length_px(height) == 0
    return flat and any(p in decls and _paints(decls[p]) for p in _BLOCK_SIDES)


def _subject(selector: str) -> str:
    parts = compounds(selector)
    return parts[-1] if parts else ""


def _pseudo_element(compound: str) -> bool:
    return bool(re.search(r"::?(?:before|after)\b", compound, re.I))


def _is_eyebrow_compound(compound: str) -> bool:
    return any(t.startswith(".") and _EYEBROW.search(t[1:]) for t in tokens(compound))


def _controlish(compound: str) -> bool:
    toks = tokens(compound)
    return "li" in toks or any(_CONTROLISH.search(t) for t in toks if t[:1] in ".#[")


def _pseudo_ruler(decls: Dict[str, str], selector: str) -> bool:
    subject = _subject(selector)
    if not _pseudo_element(subject):
        return False
    content = decls.get("content")
    if content is None:
        return False
    rendered = _css_string(content)
    if rendered is None:
        return False
    if _is_eyebrow_compound(subject):
        if _dashy(rendered):
            return True
        if _full_bleed(decls) or any(p in decls for p in ("mask", "-webkit-mask", "mask-image",
                                                          "-webkit-mask-image")):
            return False
        return not rendered.strip() and any(
            p in decls and (not p.startswith(("border", "background", "box-shadow", "outline"))
                            or _paints(decls[p])) for p in _DRAWS)
    if rendered.strip() or _controlish(subject):
        return False
    return _draws_line(decls)


def _edge_ruler(prop: str, value: str, decls: Dict[str, str]) -> bool:
    """A side edge or a background line drawn on the label itself."""
    if prop.startswith("border"):
        if prop.endswith("-color"):
            return False
        if prop.endswith("-width"):
            px = _length_px(value)
            return px is None or px > 0
        if prop.endswith("-style"):
            return value.strip() not in ("none", "hidden")
        return _paints(value)
    if prop == "box-shadow":
        m = re.search(r"\binset\s+(-?[\d.]+)[a-z%]*\s+(-?[\d.]+)", value)
        return bool(m) and float(m.group(1)) != 0 and float(m.group(2)) == 0
    repeat = "no-repeat" in value or "no-repeat" in decls.get("background-repeat", "")
    if "url(" in value and "gradient(" not in value:
        return repeat
    if "gradient(" not in value:
        return False
    size = decls.get("background-size", "")
    if any(_thin(w) for w in size.split()):
        return True
    return repeat


def accent_ruler(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    groups = match.groupdict()
    if groups.get("pseudo"):
        brace = view.text.find("{", match.end())
        block = block_at(ctx, view, brace + 1) if brace != -1 else None
        if block is None:
            return False
        decls = _decl_map(block.body)
        return any(_pseudo_ruler(decls, s) for s in block.selectors)
    if groups.get("edge"):
        block = block_at(ctx, view, match.start())
        if block is None or not any(_is_eyebrow_compound(_subject(s)) and not _pseudo_element(_subject(s))
                                    for s in block.selectors):
            return False
        prop = match.group("edge").split(":")[0].strip().lower()
        rest = view.text[match.end():]
        value = re.split(r"[;}]", rest, maxsplit=1)[0].replace("!important", "").strip().lower()
        return _edge_ruler(prop, value, _decl_map(block.body))
    if groups.get("eyebrow"):
        return start in _ruled_eyebrows(ctx)
    return True


def _class_list(ctx: FileContext, tag: Tag) -> List[str]:
    out: List[str] = []
    for a in tag.attrs:
        if a.name.lower() in ("class", "classname") and a.kind == "str":
            out.extend(ctx.text[a.vstart:a.vend].split())
    return out


def _bare(cls: str) -> str:
    return cls.rsplit(":", 1)[-1] if not cls.startswith("[") else cls


def _named_eyebrow(classes: List[str]) -> bool:
    return any(_EYEBROW.search(c) for c in classes if ":" not in c)


def _utility_eyebrow(classes: List[str]) -> bool:
    bare = [_bare(c) for c in classes]
    return "uppercase" in bare and any(_TRACKED.match(b) for b in bare)


_NOT_EYEBROW_TAGS = {"th", "td", "a", "button", "label", "li", "ul", "ol", "tr"}
_HEADING_TAG = re.compile(r"^h[1-6]$")


def _heads_a_heading(ctx: FileContext, i: int) -> bool:
    """An uppercase, tracked label is an eyebrow when a heading follows it, or
    the row that holds it, or when it sits in an hgroup or header with one."""
    tags, ends, parents = ctx.tree()
    if tags[i].name.lower() in _NOT_EYEBROW_TAGS:
        return False
    kids = _children(ctx)
    k = i
    for _ in range(2):
        sibs = kids.get(parents[k], [])
        at = sibs.index(k)
        if at + 1 < len(sibs) and _HEADING_TAG.match(tags[sibs[at + 1]].name.lower()):
            return True
        k = parents[k]
        if k < 0:
            break
    k = parents[i]
    while k >= 0:
        if tags[k].name.lower() in ("hgroup", "header"):
            return any(_HEADING_TAG.match(tags[j].name.lower())
                       for j in range(i + 1, len(tags)) if tags[j].start < ends[k])
        k = parents[k]
    return False


def _utility_ruler(classes: List[str]) -> bool:
    """Tailwind forms on the label: a side border, or a pseudo-element drawn
    with before: or after: utilities."""
    for c in classes:
        parts = c.split(":")
        bare = parts[-1]
        if re.match(r"^border-(?:l|r|s|e|x)(?:-(?!0\b|transparent\b|none\b)\S+)?$", bare):
            return True
        if any(p in ("before", "after") for p in parts[:-1]) and re.match(
                r"^(?:content-|w-|h-|size-|border|bg-|inline-block$|block$)", bare):
            return True
    return False


def _children(ctx: FileContext) -> Dict[int, List[int]]:
    def build() -> Dict[int, List[int]]:
        _tags, _ends, parents = ctx.tree()
        out: Dict[int, List[int]] = {}
        for i, p in enumerate(parents):
            out.setdefault(p, []).append(i)
        return out
    return ctx.cached("children", build)  # type: ignore[return-value]


def _close_end(ctx: FileContext, tags: List[Tag], ends: List[int], i: int) -> int:
    """Offset just past the element's closing tag, or past its own tag when it
    is void or self-closing. ``ends`` holds where the closing tag starts."""
    if not ctx.text.startswith("</", ends[i]):
        return max(tags[i].end, ends[i])
    k = ctx.text.find(">", ends[i])
    return len(ctx.text) if k == -1 else k + 1


def _blank(s: str) -> bool:
    return not re.sub(r"<!--.*?-->|&nbsp;|&#160;", " ", s, flags=re.S).strip()


def _svg_number(value: str) -> Optional[float]:
    m = re.match(r"^\s*(-?\d*\.?\d+)", value)
    return float(m.group(1)) if m else None


def _line_svg(ctx: FileContext, tags: List[Tag], ends: List[int], j: int) -> bool:
    """An SVG that draws one straight line or one dot."""
    attrs = attr_values(ctx.text, tags[j])
    box = attrs.get("viewbox", ("", ""))[1].replace(",", " ").split()
    if len(box) == 4:
        try:
            w, h = float(box[2]), float(box[3])
            if 0 < min(w, h) <= 4 and max(w, h) >= 6:
                return True
        except ValueError:
            pass
    inner = [k for k in range(j + 1, len(tags)) if tags[k].start < ends[j]]
    names = [tags[k].name.lower() for k in inner]
    if any(n in _SVG_OPAQUE for n in names):
        return False
    shapes = [k for k in inner if tags[k].name.lower() in _SHAPES]
    if len(shapes) != 1:
        return False
    k = shapes[0]
    name = tags[k].name.lower()
    a = {n: v for n, (_kind, v) in attr_values(ctx.text, tags[k]).items()}
    if name in ("line", "circle", "ellipse"):
        return True
    if name == "rect":
        w, h = _svg_number(a.get("width", "")), _svg_number(a.get("height", ""))
        if w is None or h is None:
            return False
        return min(w, h) <= 4 or max(w, h) <= 12
    if name == "polyline":
        return len(re.findall(r"-?\d*\.?\d+", a.get("points", ""))) == 4
    if name == "path":
        d = a.get("d", "").strip()
        num = r"(-?\d*\.?\d+)"
        m = re.match(r"^[Mm]\s*" + num + r"[\s,]+" + num + r"\s*(?:([HhVv])\s*" + num
                     + r"|[Ll]\s*" + num + r"[\s,]+" + num + r")\s*[Zz]?\s*$", d)
        if not m:
            return False
        if m.group(3):
            return True
        return m.group(1) == m.group(5) or m.group(2) == m.group(6)
    return False


def _ornament(ctx: FileContext, tags: List[Tag], ends: List[int], j: int) -> bool:
    """An empty span or i, or an SVG line or dot: a mark with no words."""
    tag = tags[j]
    name = tag.name.lower()
    attrs = attr_values(ctx.text, tag)
    if name == "svg":
        return not any(_ICONISH.search(_bare(c)) for c in _class_list(ctx, tag)) \
            and _line_svg(ctx, tags, ends, j)
    if name == "img":
        w, h = _svg_number(attrs.get("width", ("", ""))[1]), _svg_number(attrs.get("height", ("", ""))[1])
        shaped = w is not None and h is not None and 0 < min(w, h) <= 4 and max(w, h) >= 6
        return "alt" in attrs and not attrs["alt"][1] and (
            shaped or bool(re.search(r"(?:^|[/_-])(?:line|rule|dash|stroke)[\w-]*\.\w+$",
                                     attrs.get("src", ("", ""))[1])))
    if name not in ("span", "i", "div", "b", "em", "small"):
        return False
    if ends[j] > tag.end and not _blank(ctx.text[tag.end:ends[j]]):
        return False
    if any(k == "id" or k.startswith(("data-lucide", "data-icon", "data-feather", "data-slot",
                                      "data-bind", "data-text", "data-value", "data-field",
                                      "aria-label", "aria-live", "role", "x-", "v-", ":", "@"))
           for k in attrs):
        return False
    return not any(_ICONISH.search(_bare(c)) for c in _class_list(ctx, tag))


def _ruled_eyebrows(ctx: FileContext) -> Set[int]:
    """Start offsets of eyebrow elements drawn with an ornament beside them."""
    def build() -> Set[int]:
        tags, ends, parents = ctx.tree()
        kids = _children(ctx)
        out: Set[int] = set()
        for i, tag in enumerate(tags):
            classes = _class_list(ctx, tag)
            if not classes or not (_named_eyebrow(classes)
                                   or (_utility_eyebrow(classes) and _heads_a_heading(ctx, i))):
                continue
            if _utility_ruler(classes):
                out.add(tag.start)
                continue
            inner = ctx.text[tag.end:ends[i]] if ends[i] > tag.end else ""
            own = kids.get(i, [])
            if not own and _blank(inner) and tag.name.lower() in ("span", "i"):
                out.add(tag.start)
                continue
            if own:
                first, last = own[0], own[-1]
                if _blank(ctx.text[tag.end:tags[first].start]) and _ornament(ctx, tags, ends, first):
                    out.add(tag.start)
                    continue
                if _blank(ctx.text[_close_end(ctx, tags, ends, last):ends[i]]) and _ornament(ctx, tags, ends, last):
                    out.add(tag.start)
                    continue
            words = html_unescape(re.sub(r"<[^>]*>", " ", inner)).strip()
            if len(words) > 1 and ((words[0] in _DASHES and words[1].isspace())
                                   or (words[-1] in _DASHES and words[-2].isspace())):
                out.add(tag.start)
                continue
            sibs = kids.get(parents[i], [])
            at = sibs.index(i)
            if at > 0:
                prev = sibs[at - 1]
                if _blank(ctx.text[_close_end(ctx, tags, ends, prev):tag.start]) and _ornament(ctx, tags, ends, prev):
                    out.add(tag.start)
                    continue
            if at + 1 < len(sibs):
                nxt = sibs[at + 1]
                if _blank(ctx.text[_close_end(ctx, tags, ends, i):tags[nxt].start]) and _ornament(ctx, tags, ends, nxt):
                    out.add(tag.start)
        return out
    return ctx.cached("ruled_eyebrows", build)  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# nav-equal-hamburger-desktop
# ---------------------------------------------------------------------------
# A menu button is found in any language: by a menu word in its name, class,
# id or icon, by the hamburger glyph, or by structure (aria-expanded with
# aria-controls naming the site navigation). It passes when anything hides it,
# or an ancestor, at desktop width: the hidden attribute, a Tailwind,
# Bootstrap, Bulma or Foundation breakpoint class, an inline style, or any
# CSS rule in the file or in a local stylesheet it links or imports, read
# with its media queries at DESKTOP_WIDTH.

DESKTOP_WIDTH = 1280
_MENU_WORD = re.compile(
    r"menu|menú|menü|hamburger|burger|navigation|nav[_-]*(?:toggl|btn|button|open|trigger)"
    r"|navbar-toggler|drawer|offcanvas|off-canvas|(?:ال)?قائمة|منو"
    r"|תפריט|メニュー|菜单|菜單|選單"
    r"|меню|메뉴|मेनू|เมนู"
    r"|trình đơn|menyu", re.I)
_CLOSE_WORD = re.compile(
    r"(?<!\w)(?:close|dismiss|إغلاق|اغلاق|schlie|cerrar|fermer|fechar|chiudi"
    r"|閉じる|关闭|關閉|закрыть|닫기"
    r"|बंद|ปิด|đóng|tutup|kapat|sluit)", re.I)
_BURGER_GLYPH = re.compile(r"☰|&#9776;|&#x2630;", re.I)
_SR_ONLY = re.compile(r"<(\w+)[^>]*class\s*=\s*[\"'][^\"']*(?:sr-only|visually-hidden|screen-reader)[^\"']*[\"'][^>]*>.*?</\1>",
                      re.I | re.S)
_TW_BREAKPOINTS = {"sm": 640, "md": 768, "lg": 1024, "xl": 1280, "2xl": 1536}
_BS_BREAKPOINTS = {"sm": 576, "md": 768, "lg": 992, "xl": 1200, "xxl": 1400}
_SHOWN = r"(?:block|flex|inline-flex|inline-block|inline|grid|inline-grid|table|contents)"


def _bp_px(prefix: str) -> Optional[float]:
    if prefix in _TW_BREAKPOINTS:
        return _TW_BREAKPOINTS[prefix]
    m = re.match(r"^min-\[(\d*\.?\d+)(px|rem|em)\]$", prefix)
    if m:
        return float(m.group(1)) * (1 if m.group(2) == "px" else 16)
    return None


def _classes_hide(classes: List[str], ancestors: List[List[str]]) -> bool:
    """A breakpoint class hides the element at desktop width."""
    shown_from: List[float] = []
    hidden_base = False
    for c in classes:
        parts = c.split(":")
        util, prefixes = parts[-1], parts[:-1]
        if not prefixes:
            if util in ("hidden", "invisible"):
                hidden_base = True
            continue
        if len(prefixes) != 1:
            continue
        px = _bp_px(prefixes[0])
        if px is None:
            continue
        if util in ("hidden", "invisible") and px <= DESKTOP_WIDTH:
            return True
        if re.fullmatch(_SHOWN, util):
            shown_from.append(px)
    if hidden_base and not any(px <= DESKTOP_WIDTH for px in shown_from):
        return True
    for c in classes:
        m = re.fullmatch(r"d-(sm|md|lg|xl|xxl)-none", c)
        if m and _BS_BREAKPOINTS[m.group(1)] <= DESKTOP_WIDTH:
            return True
        if re.fullmatch(r"hide-for-(?:medium|large)(?:-up)?|show-for-small-only|uk-hidden@(?:s|m|l)|navbar-burger", c):
            return True
    if "navbar-toggler" in classes:
        for anc in ancestors:
            for c in anc:
                m = re.fullmatch(r"navbar-expand(?:-(sm|md|lg|xl|xxl))?", c)
                if m and (m.group(1) is None or _BS_BREAKPOINTS[m.group(1)] <= DESKTOP_WIDTH):
                    return True
    return False


def _media_px(value: str) -> Optional[float]:
    m = re.match(r"^\s*(\d*\.?\d+)\s*(px|rem|em)?\s*$", value)
    if not m:
        return None
    return float(m.group(1)) * (16 if m.group(2) in ("rem", "em") else 1)


def _feature_true(feature: str, width: float) -> bool:
    f = feature.strip().lower()
    m = re.fullmatch(r"(min|max)-width\s*:\s*(.+)", f)
    if m:
        px = _media_px(m.group(2))
        if px is None:
            return False
        return px <= width if m.group(1) == "min" else px >= width
    m = re.fullmatch(r"width\s*(>=|>|<=|<)\s*(.+)", f) or None
    if m:
        px = _media_px(m.group(2))
        if px is None:
            return False
        return {">=": width >= px, ">": width > px, "<=": width <= px, "<": width < px}[m.group(1)]
    m = re.fullmatch(r"(.+?)\s*(>=|>|<=|<)\s*width", f)
    if m:
        px = _media_px(m.group(1))
        if px is None:
            return False
        return {">=": px >= width, ">": px > width, "<=": px <= width, "<": px < width}[m.group(2)]
    m = re.fullmatch(r"(.+?)\s*(<=|<)\s*width\s*(<=|<)\s*(.+)", f)
    if m:
        lo, hi = _media_px(m.group(1)), _media_px(m.group(4))
        if lo is None or hi is None:
            return False
        return (lo <= width if m.group(2) == "<=" else lo < width) and \
            (width <= hi if m.group(3) == "<=" else width < hi)
    return f in ("hover: hover", "hover:hover", "pointer: fine", "pointer:fine", "any-hover: hover",
                 "orientation: landscape", "prefers-reduced-motion: no-preference",
                 "prefers-color-scheme: light", "prefers-contrast: no-preference")


def _media_true(query: str, width: float = DESKTOP_WIDTH) -> bool:
    """Whether a media query list holds on a desktop screen of ``width``."""
    for q in _split_top(query):
        q = q.strip().lower()
        negate = q.startswith("not ")
        if negate or q.startswith("only "):
            q = q.split(" ", 1)[1]
        feats = re.findall(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)", q)
        media_type = re.sub(r"\([^()]*\)", " ", q).replace(" and ", " ").split()
        ok = all(t in ("screen", "all", "and") for t in media_type)
        ok = ok and all(_feature_true(f, width) for f in feats)
        if ok != negate:
            return True
    return False


def _applies(atrules: Tuple[str, ...]) -> bool:
    for at in atrules:
        if at.startswith("@media"):
            if not _media_true(at[len("@media"):]):
                return False
        elif at.startswith(("@container", "@document", "@page", "@font-face", "@keyframes")):
            return False
    return True


def _linked_sheets(ctx: FileContext) -> List[Tuple[str, str]]:
    """(media query, css text) of every local stylesheet the file links or
    imports, one @import level deep."""
    def build() -> List[Tuple[str, str]]:
        out: List[Tuple[str, str]] = []
        seen: Set[Path] = set()

        def read(ref: str, media: str, base: Path, depth: int) -> None:
            ref = ref.split("?", 1)[0].split("#", 1)[0]
            if not ref or re.match(r"[a-z][a-z0-9+.-]*:|//", ref, re.I) or ref.startswith("/"):
                return
            target = (base / ref)
            try:
                key = target.resolve()
                if key in seen or not target.is_file() or target.stat().st_size > 1_000_000:
                    return
                seen.add(key)
                css = target.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                return
            css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
            if depth < 1:
                for m in re.finditer(r"@import\s+(?:url\(\s*)?[\"']?([^\"')\s;]+)[\"']?\s*\)?\s*([^;]*);", css, re.I):
                    read(m.group(1), m.group(2).strip(), target.parent, depth + 1)
            out.append((media, css))

        base = ctx.path.parent
        for tag in sorted(ctx.views.scan.tags, key=lambda t: t.start):
            if tag.name.lower() != "link":
                continue
            a = attr_values(ctx.text, tag)
            if "stylesheet" in a.get("rel", ("", ""))[1].lower().split() and "href" in a:
                read(a["href"][1], a.get("media", ("", ""))[1], base, 0)
        for m in re.finditer(r"""\bimport\s+(?:[\w{}\s,*]+\s+from\s+)?["']([^"']+\.(?:css|scss))["']""", ctx.text):
            if ".module." not in m.group(1):
                read(m.group(1), "", base, 0)
        return out
    return ctx.cached("linked_sheets", build)  # type: ignore[return-value]


def _hiding_rules(ctx: FileContext) -> List[Tuple[List[FrozenSet[str]], bool, bool]]:
    """Every rule that sets display or visibility and holds at desktop width,
    in cascade order: (subject token sets, hides, important)."""
    def build() -> List[Tuple[List[FrozenSet[str]], bool, bool]]:
        sheets = list(_linked_sheets(ctx))
        own = ctx.views.get("css")
        if own is not None and own.text:
            sheets.append(("", own.text))
        out: List[Tuple[List[FrozenSet[str]], bool, bool]] = []
        for media, css in sheets:
            if media and media.lower() not in ("all", "screen") and not _media_true(media):
                continue
            for block in css_blocks(css):
                if not block.selectors or not _applies(block.atrules):
                    continue
                subjects: List[FrozenSet[str]] = []
                for sel in block.selectors:
                    subject = _subject(sel)
                    if any(name not in ("not", "is", "where") for name, _arg in pseudos(subject)):
                        continue
                    toks = tokens(subject)
                    if any(t[:1] in ".#[" for t in toks):
                        subjects.append(toks)
                if not subjects:
                    continue
                for part in block.body.split(";"):
                    if ":" not in part:
                        continue
                    prop, value = part.split(":", 1)
                    prop = prop.strip().lower()
                    if prop not in ("display", "visibility"):
                        continue
                    important = "!important" in value
                    v = value.replace("!important", "").strip().lower()
                    hides = v == "none" if prop == "display" else v in ("hidden", "collapse")
                    shows = prop == "display" or v == "visible"
                    if hides or shows:
                        out.append((subjects, hides, important))
        return out
    return ctx.cached("hiding_rules", build)  # type: ignore[return-value]


def _element_tokens(ctx: FileContext, tag: Tag) -> FrozenSet[str]:
    out = {tag.name.lower()}
    for a in tag.attrs:
        low = a.name.lower()
        if low.startswith((":", "@", "v-", "x-")) or a.kind == "expr":
            continue
        value = ctx.text[a.vstart:a.vend]
        if low in ("class", "classname"):
            out.update("." + c for c in value.split())
            continue
        if low == "id":
            out.add("#" + value.strip())
        out.add("[" + low + "]")
        out.add("[" + low + "=" + re.sub(r"[\s'\"]", "", value).lower() + "]")
    return frozenset(out)


def _css_hides(ctx: FileContext, tag: Tag) -> bool:
    mine = _element_tokens(ctx, tag)
    hidden = None
    hidden_important = None
    for subjects, hides, important in _hiding_rules(ctx):
        if not any(s <= mine for s in subjects):
            continue
        if important:
            hidden_important = hides
        else:
            hidden = hides
    if hidden_important is not None:
        return hidden_important
    return bool(hidden)


def _hidden_at_desktop(ctx: FileContext, i: int) -> bool:
    tags, _ends, parents = ctx.tree()
    chain: List[int] = []
    k = i
    while k >= 0:
        chain.append(k)
        k = parents[k]
    ancestors = [_class_list(ctx, tags[k]) for k in chain[1:]]
    for n, k in enumerate(chain):
        tag = tags[k]
        a = attr_values(ctx.text, tag)
        if "hidden" in a and a["hidden"][1].lower() not in ("false", "until-found"):
            return True
        style = a.get("style", ("", ""))[1].lower().replace(" ", "")
        if "display:none" in style or "visibility:hidden" in style:
            return True
        if _classes_hide(_class_list(ctx, tag), ancestors[n:]):
            return True
        if _css_hides(ctx, tag):
            return True
    return False


def _menu_button(ctx: FileContext, i: int) -> bool:
    """A button that opens the site's menu, told apart in any language."""
    tags, ends, _parents = ctx.tree()
    tag = tags[i]
    a = attr_values(ctx.text, tag)
    inner = ctx.text[tag.end:ends[i]] if ends[i] > tag.end else ""
    words = html_unescape(re.sub(r"<[^>]*>", " ", _SR_ONLY.sub(" ", inner))).strip()
    names = " ".join(v for k, (_kind, v) in a.items()
                     if k in ("aria-label", "title", "class", "classname", "id", "aria-controls",
                              "data-toggle", "data-bs-toggle", "data-target", "data-bs-target"))
    spoken = " ".join(v for k, (_kind, v) in a.items() if k in ("aria-label", "title"))
    if _CLOSE_WORD.search(spoken + " " + words):
        return False
    # Visible words: up to three, one of them a menu word ("Menu", "Open
    # menu", "القائمة"); a button with other words is a dropdown or an action.
    if words and not _BURGER_GLYPH.search(words) and not (
            len(words.split()) <= 3 and _MENU_WORD.search(words)):
        return False
    inner_attrs = " ".join(re.findall(r"(?:href|class|id)\s*=\s*[\"']([^\"']*)", inner))
    if _MENU_WORD.search(names) or _MENU_WORD.search(inner_attrs) or _BURGER_GLYPH.search(inner):
        return True
    if "aria-expanded" not in a or "aria-controls" not in a:
        return False
    target = _id_tags(ctx).get(a["aria-controls"][1].split()[0] if a["aria-controls"][1] else "")
    if target is None:
        return False
    t = attr_values(ctx.text, target)
    if target.name.lower() == "nav" or t.get("role", ("", ""))[1].lower() in ("navigation", "menu", "menubar"):
        return True
    return ctx.text.count("<a ", target.end, ctx.element_end(target)) >= 3


def hamburger_on_desktop(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    tags, _ends, _parents = ctx.tree()
    index = ctx.cached("tree_index", lambda: {t.start: n for n, t in enumerate(tags)})
    i = index.get(start)  # type: ignore[union-attr]
    if i is None:
        return False
    name = tags[i].name.lower()
    a = attr_values(ctx.text, tags[i])
    if name != "button" and a.get("role", ("", ""))[1].lower() != "button" and not re.search(
            r"hamburger|burger|menu-toggle|nav-toggle", a.get("class", a.get("classname", ("", "")))[1], re.I):
        return False
    return _menu_button(ctx, i) and not _hidden_at_desktop(ctx, i)


# ---------------------------------------------------------------------------
# screen-reader-only-without-class
# ---------------------------------------------------------------------------

_HREF_ID = re.compile(r"\bhref\s*=\s*['\"]#([^'\"\s]+)['\"]", re.I)


def skip_link(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A skip link is the first link to its target, placed before the element
    with that id. Judged by position, not by link text, so every language is
    treated the same."""
    href = _HREF_ID.search(match.group(0))
    if not href:
        return False
    target = href.group(1)
    first = re.search(r"<a\b[^>]*\bhref\s*=\s*['\"]#" + re.escape(target) + r"['\"]", view.text, re.I)
    if first is None or first.start() != match.start():
        return False
    anchor = re.search(r"\bid\s*=\s*['\"]" + re.escape(target) + r"['\"]", view.text)
    return anchor is None or anchor.start() > match.start()


POST_CHECKS: Dict[str, Callable[[FileContext, View, re.Match, int], bool]] = {
    "input-has-no-name": input_has_no_name,
    "svg-not-hidden": svg_not_hidden,
    "outline-without-ring": outline_without_ring,
    "hover-only-reveal": hover_only_reveal,
    "page-needs-imagery": page_needs_imagery,
    "import-blocks-render": import_blocks_render,
    "skip-link": skip_link,
    "accent-ruler": accent_ruler,
    "hamburger-on-desktop": hamburger_on_desktop,
}
