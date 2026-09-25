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
    r"(?:outline|ring|shadow|border)(?!-(?:none|0|offset|transparent)\b)(?:-[\w\[\]#().,/%-]+)?(?=\s|$)",
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
            if _paints(value):
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
    it is as general or more. An empty compound covers only an empty one."""
    return ring <= removal if ring else not removal


def _covers(ring: List[FrozenSet[str]], removal: List[FrozenSet[str]]) -> bool:
    """Right-to-left match: the ring's subject covers the removal's subject and
    every ring ancestor covers some removal ancestor, in order."""
    if not ring or not removal or not _sub(ring[-1], removal[-1]):
        return False
    j = len(removal) - 2
    for r in reversed(ring[:-1]):
        while j >= 0 and not (r and r <= removal[j]):
            j -= 1
        if j < 0:
            return False
        j -= 1
    return True


@dataclass
class Ring:
    kind: str                       # "self" or "ancestor"
    paint: str                      # "outline" or "other"
    toks: List[FrozenSet[str]]      # tokens per compound
    spec: Tuple[int, int, int]
    at: int                         # block offset, for source order
    anchor: int = -1                # ancestor rings: compound index of the anchor
    within: bool = False            # :focus-within (the anchor may be the element itself)
    inner: Optional[FrozenSet[str]] = None  # :has() argument subject tokens


def _rings(ctx: FileContext, view: View) -> Tuple[Dict[FrozenSet[str], List[Ring]], Dict[str, List[Ring]], List[Ring]]:
    """Focus rings in the view, indexed once per file: self rings by the set
    of every token in their selector, ancestor rings by anchor token, plus
    every ancestor ring."""
    def build():
        by_tokens: Dict[FrozenSet[str], List[Ring]] = {}
        by_anchor: Dict[str, List[Ring]] = {}
        ancestors: List[Ring] = []
        for b in _blocks(ctx, view)[0]:
            if not b.selectors or any(a.startswith("@media") and "print" in a for a in b.atrules):
                continue
            paint = ring_kind(b.body)
            if not paint:
                continue
            for sel in b.selectors:
                parts = compounds(sel)
                if not parts:
                    continue
                toks = [tokens(x) for x in parts]
                if _focus_kind(parts[-1]) == "self":
                    ring = Ring("self", paint, toks, _specificity(sel), b.start)
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
                        inner = tokens(sub[-1]) if sub else frozenset()
                ring = Ring("ancestor", paint, toks, _specificity(sel), b.start, last, within, inner)
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


def _removal_has_ring(ctx: FileContext, view: View, selector: str, at: int) -> bool:
    parts = compounds(selector)
    if not parts:
        return False
    removal = [tokens(x) for x in parts]
    spec = _specificity(selector)
    by_tokens, by_anchor, ancestors = _rings(ctx, view)
    shielded = any(name == "not" and ":focus-visible" in arg for p in parts for name, arg in pseudos(p))
    # A ring that covers the removal uses only tokens the removal has, so
    # rings are looked up by every subset of the removal's tokens.
    pool = sorted(frozenset().union(*removal))
    if len(pool) <= 10:
        keys = (frozenset(c) for n in range(len(pool) + 1) for c in combinations(pool, n))
        self_rings = [r for k in keys for r in by_tokens.get(k, ())]
    else:
        self_rings = [r for rs in by_tokens.values() for r in rs]
    for ring in self_rings:
        if not _covers(ring.toks, removal):
            continue
        if ring.paint == "outline" and not shielded and (ring.spec, ring.at) < (spec, at):
            continue  # the removal is more specific (or later) and wins
        return True
    inner_ok = lambda ring: ring.inner is None or _sub(ring.inner, removal[-1])  # noqa: E731
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
    for sel in block.selectors:
        parts = compounds(sel)
        if own_ring and parts and _focus_kind(parts[-1]):
            continue
        key = "removal:%d:%s" % (id(view), sel)
        if not ctx.cached(key, lambda sel=sel: _removal_has_ring(ctx, view, sel, block.start)):
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


def document_or_app_surface(ctx: FileContext) -> bool:
    """True when the page's main content is a document or an app surface:
    one article, form, table, code listing or grid holds most of the visible
    text of ``<main>`` (or ``<body>``), or forms, tables, listings and grids
    together do. Section counts and the mere presence of a form decide
    nothing, so a landing page built from divs still needs imagery."""
    def build() -> bool:
        # Same offsets as the file, with comments, scripts and styles blanked.
        low = list(ctx.low)
        for a, b in list(ctx.views.scan.blanks) + [(x, y) for _, x, y in ctx.views.scan.raw]:
            low[a:b] = " " * (b - a)
        low = "".join(low)
        s, e = _region(low, "main") or _region(low, "body") or (0, len(low))
        total = _visible_len(low[s:e])
        if not total:
            return False
        grids = [
            (t.start, ctx.element_end(t)) for t in ctx.views.scan.tags
            if re.fullmatch(r"grid|treegrid|application", attr_values(ctx.text, t).get("role", ("", ""))[1].lower())
        ]
        app: List[Tuple[int, int]] = list(grids)
        for name in ("article", "form", "table", "pre"):
            spans = list(zip(*ctx.element_ranges(name)))
            for a, b in spans:
                if s <= a < e and _visible_len(low[a:min(b, e)]) >= 0.6 * total:
                    return True
            if name != "article":
                app.extend(spans)
        for a, b in grids:
            if s <= a < e and _visible_len(low[a:min(b, e)]) >= 0.6 * total:
                return True
        return _content_share(ctx, app, low, s, e) >= 0.6 * total
    return bool(ctx.cached("doc_surface", build))


def page_needs_imagery(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    return not document_or_app_surface(ctx)


# ---------------------------------------------------------------------------
# css-import-render-blocking
# ---------------------------------------------------------------------------

_IMPORT_URL = re.compile(r"@import\s+(?:url\(\s*)?[\"']?([^\"')\s;]+)", re.I)
_TOKEN_NAME = re.compile(r"(?:^|[/_.-])(?:design-?)?(?:tokens?|variables|vars|custom-properties)(?:[/_.-]|$)", re.I)
_CUSTOM_PROP = re.compile(r"--[\w-]+\s*:[^;{}]*;?")


def _custom_properties_only(css: str) -> bool:
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    if "--" not in css:
        return False
    rest = _CUSTOM_PROP.sub(" ", css)
    rest = re.sub(r"[^{};]*\{", " ", rest)
    rest = rest.replace("}", " ").replace(";", " ")
    return not rest.strip()


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
}
