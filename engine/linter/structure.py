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
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple

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
        """Offset of the closing tag that ends ``tag``'s element."""
        name = tag.name.lower()
        if self.text[max(0, tag.end - 2):tag.end] == "/>":
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

def input_has_no_name(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An input is named by a ``<label for>`` that matches its id, a wrapping
    ``<label>``, ``aria-label``, or ``aria-labelledby`` that points to an id
    in the file. An id on its own names nothing."""
    tag = ctx.tags_by_start().get(start)
    if tag is None:
        return True
    attrs = attr_values(ctx.text, tag)
    if tag.name[:1].isupper() and "label" in attrs:
        return False  # a component that renders its own <label> from the prop
    for key in ("aria-label", ":aria-label", "v-bind:aria-label"):
        if key in attrs and attrs[key][1]:
            return False
    static_ids, dynamic_ids = _ids(ctx)
    for key in ("aria-labelledby", ":aria-labelledby", "v-bind:aria-labelledby"):
        if key in attrs:
            kind, value = attrs[key]
            if _dynamic(key, kind):
                if value in dynamic_ids:
                    return False
            elif value and all(ref in static_ids for ref in value.split()):
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


def tokens(compound: str) -> Set[str]:
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
    return out


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


def _share(a: Set[str], b: Set[str]) -> bool:
    return bool(a & b) or (not a and not b)


# ---------------------------------------------------------------------------
# outline-none-no-focus-visible
# ---------------------------------------------------------------------------

_RING = re.compile(
    r"(?:^|[;{\s])(?:outline\s*:\s*(?!\s*(?:none|0)\s*(?:!important\s*)?(?:;|$))"
    r"|outline-(?:style|width|color)\s*:"
    r"|box-shadow\s*:\s*(?!\s*none\b)"
    r"|border(?:-[a-z]+)*\s*:)",
    re.I,
)
_RING_CLASS = re.compile(r"(?:^|\s)(?:[\w-]+:)*focus(?:-visible|-within)?:(?:outline|ring|shadow|border)", re.I)


def _focus_rings(ctx: FileContext, view: View) -> List[Tuple[str, List[str]]]:
    """(kind, compounds) for every focus selector whose block draws a ring."""
    def build() -> List[Tuple[str, List[str]]]:
        out: List[Tuple[str, List[str]]] = []
        for b in _blocks(ctx, view)[0]:
            if not b.selectors or not _RING.search(b.body):
                continue
            for sel in b.selectors:
                parts = compounds(sel)
                if not parts:
                    continue
                if _focus_kind(parts[-1]) == "self":
                    out.append(("self", parts))
                elif any(_focus_kind(p) == "ancestor" for p in parts):
                    out.append(("ancestor", parts))
        return out
    return ctx.cached("rings:%d" % id(view), build)  # type: ignore[return-value]


def _tag_tokens(ctx: FileContext, tag: Tag) -> Set[str]:
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
    return out


def _wraps_in_markup(ctx: FileContext, anchor: Set[str], subject: Set[str]) -> bool:
    """True when the file's own markup puts an element matching ``subject``
    inside an element matching ``anchor``."""
    anchor = {t for t in anchor if not t.startswith("[")}
    subject = {t for t in subject if not t.startswith("[")}
    if not anchor:
        return False

    def build() -> bool:
        tags: List[Tag] = ctx.cached("tag_list", lambda: sorted(ctx.views.scan.tags, key=lambda t: t.start))  # type: ignore[assignment]
        for i, outer in enumerate(tags):
            if not outer.name or not anchor <= _tag_tokens(ctx, outer):
                continue
            end = ctx.element_end(outer)
            for inner in tags[i + 1:]:
                if inner.start >= end:
                    break
                if subject <= _tag_tokens(ctx, inner):
                    return True
        return False
    return bool(ctx.cached("wraps:%s|%s" % (sorted(anchor), sorted(subject)), build))


def _selector_has_ring(ctx: FileContext, view: View, selector: str) -> bool:
    parts = compounds(selector)
    if not parts:
        return False
    subject = tokens(parts[-1])
    for kind, ring in _focus_rings(ctx, view):
        if kind == "self":
            if _share(tokens(ring[-1]), subject):
                return True
            continue
        for p in ring:
            if _focus_kind(p) != "ancestor":
                continue
            anchor = tokens(p)
            if anchor and any(anchor & tokens(c) for c in parts):
                return True
            if anchor and _wraps_in_markup(ctx, anchor, subject):
                return True
    return False


def outline_without_ring(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Decide per rule block. A removed outline passes only when the same
    selector, or a ``:focus-within`` or ``:has(:focus-visible)`` rule on an
    ancestor, draws a visible ring (outline, box-shadow or border)."""
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
    own_ring = bool(_RING.search(block.body))
    for sel in block.selectors:
        parts = compounds(sel)
        if own_ring and parts and _focus_kind(parts[-1]):
            continue
        if not _selector_has_ring(ctx, view, sel):
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


def _outside(ranges: Tuple[List[int], List[int]], positions: List[int]) -> List[int]:
    return [p for p in positions if not _covered(ranges, p)]


def document_or_app_surface(ctx: FileContext) -> bool:
    """True when the page's main content is a document or an app surface:
    one article or form that holds most of the main content, or a page with
    fewer than two sections whose content is a form, article, table, code
    listing or grid. The mere presence of a form, pre or table decides
    nothing."""
    def build() -> bool:
        code = ctx.views.get("code")
        low = (code.text if code is not None else ctx.text).lower()
        region = _region(low, "main") or _region(low, "body") or (0, len(low))
        s, e = region
        body = low[s:e]
        total = _visible_len(body)
        for name in ("article", "form"):
            starts, ends = ctx.element_ranges(name)
            for a, b in zip(starts, ends):
                if s <= a and b <= e and total and _visible_len(low[a:b]) >= 0.7 * total:
                    return True
        articles = ctx.element_ranges("article")
        sections = _outside(articles, [s + m.start() for m in re.finditer(r"<section\b", body)])
        if len(sections) >= 2:
            return False
        return bool(re.search(r"<(?:form|article|table|pre)\b|role\s*=\s*[\"']?(?:grid|treegrid|application)\b", body))
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
    if _TOKEN_NAME.search(Path(path).name.rsplit(".", 1)[0]):
        return False
    try:
        target = (ctx.path.parent / path) if not path.startswith("/") else None
        if target is not None and target.is_file() and target.stat().st_size <= 512_000:
            return not _custom_properties_only(target.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        pass
    return True


# ---------------------------------------------------------------------------
# screen-reader-only-without-class
# ---------------------------------------------------------------------------

def first_link(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A skip link is the first link in the body; match on that position
    rather than on the link text, so every language is treated the same."""
    def build() -> int:
        body = re.search(r"<body\b[^>]*>", view.text, re.I)
        first = re.compile(r"<a\b", re.I).search(view.text, body.end() if body else 0)
        return first.start() if first else -1
    return match.start() == ctx.cached("first_link:%d" % id(view), build)


POST_CHECKS: Dict[str, Callable[[FileContext, View, re.Match, int], bool]] = {
    "input-has-no-name": input_has_no_name,
    "svg-not-hidden": svg_not_hidden,
    "outline-without-ring": outline_without_ring,
    "hover-only-reveal": hover_only_reveal,
    "page-needs-imagery": page_needs_imagery,
    "import-blocks-render": import_blocks_render,
    "first-link": first_link,
}
