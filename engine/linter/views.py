"""Channel views of a source file, so each lint rule reads only what it judges.

A rule names one or more channels in ``detection.target``. The linter runs the
rule's regex over the view for each channel and maps every match back to the
line and column of the original file.

Channels
--------
``raw``      the file exactly as written.
``code``     comments and data URI payloads blanked. In JSX, Astro and Svelte
             files, ``className`` becomes ``class``, class expressions become
             ``class="..."`` and style objects become ``style="css"``.
``markup``   ``code`` without the bodies of ``<style>`` and ``<script>``
             elements. Empty for stylesheets.
``css``      every CSS region: stylesheets, ``<style>`` bodies, ``style``
             attributes, JSX ``style`` and ``sx`` objects (camelCase keys,
             numbers as px), Vue ``:style`` objects and CSS-in-JS templates.
``classes``  every class list: ``class`` and ``className`` values, strings in
             class expressions, Vue ``:class`` bindings, ``@apply`` lists and
             class-like string literals in scripts.
``text``     visible copy: text nodes outside code elements, copy attributes
             (alt, title, aria-label, placeholder) and sentence-like string
             literals in scripts.

The scanners are tolerant: malformed input never raises, it only narrows what
a channel sees.
"""
from __future__ import annotations

import re
from bisect import bisect_right
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

CHANNELS = ("raw", "code", "markup", "css", "classes", "text")

CSS_EXTS = {"css", "scss", "sass", "less"}
JSX_EXTS = {"jsx", "tsx", "js", "ts", "mjs", "cjs"}
MD_EXTS = {"md", "markdown", "mdx"}

# Elements whose text is code or sample output, never UI copy.
CODE_ELEMENTS = {"code", "pre", "kbd", "samp", "var", "script", "style"}
RAW_ELEMENTS = {"script", "style"}
COPY_ATTRS = {
    "alt", "title", "aria-label", "aria-description", "aria-placeholder",
    "aria-roledescription", "placeholder", "label", "summary",
}
CLASS_ATTRS = {"class", "classname", "class:list", ":class", "v-bind:class"}
STYLE_ATTRS = {"style", "sx", ":style", "v-bind:style"}
# Attributes whose expression strings are never copy.
NON_COPY_ATTRS = CLASS_ATTRS | STYLE_ATTRS | {
    "href", "src", "srcset", "id", "key", "to", "for", "htmlfor", "name",
    "type", "role", "rel", "target", "d", "viewbox", "fill", "stroke",
    "xmlns", "action", "method", "as", "lang", "dir", "ref", "slot",
}

# React adds "px" to numbers for every property except these.
UNITLESS = {
    "animation-iteration-count", "aspect-ratio", "border-image-outset",
    "border-image-slice", "border-image-width", "box-flex", "box-flex-group",
    "box-ordinal-group", "column-count", "columns", "flex", "flex-grow",
    "flex-positive", "flex-shrink", "flex-negative", "flex-order", "font-weight",
    "grid-area", "grid-row", "grid-row-end", "grid-row-span", "grid-row-start",
    "grid-column", "grid-column-end", "grid-column-span", "grid-column-start",
    "line-clamp", "line-height", "opacity", "order", "orphans", "scale",
    "tab-size", "widows", "z-index", "zoom", "fill-opacity", "flood-opacity",
    "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-miterlimit",
    "stroke-opacity", "stroke-width",
}
_CSS_IN_JS_TAG = re.compile(
    r"(?:\bstyled\s*(?:\.\s*[\w$]+|\([^()]*\))(?:\s*\.\s*attrs\s*\([^()]*\))?"
    r"(?:\s*<[^`<>]*>)?|\b(?:css|keyframes|createGlobalStyle|injectGlobal|globalStyle)"
    r"(?:\s*<[^`<>]*>)?)\s*$"
)
_IMPORT_BEFORE = re.compile(r"(?:\bfrom|\bimport|\brequire\s*\(|\bimport\s*\()\s*$")
_CLASS_TOKEN = re.compile(r"^!?[a-z0-9@\[\-][\w\-:/.\[\]()%#&>*=,'\"+~!]*$")
_WORD = re.compile(r"[^\W\d_]{2,}")
_WS = re.compile(r"\s")
_REGEX_PREV = set("(,=:[!&|?{};+-*%<>~^")
_REGEX_PREV_WORDS = {"return", "typeof", "case", "do", "else", "in", "of", "void", "yield", "await"}
_JSX_PREV = set("(,=:?{}[;&|>!")
_JSX_PREV_WORDS = {"return", "yield", "default", "else", "case", "await"}


# ---------------------------------------------------------------------------
# Offset-mapped text
# ---------------------------------------------------------------------------

class View:
    """A derived text plus a map from its offsets back to the original file."""

    __slots__ = ("text", "_starts", "_origs", "_exact")

    def __init__(self, text: str, starts: List[int], origs: List[int], exact: List[bool]):
        self.text = text
        self._starts = starts
        self._origs = origs
        self._exact = exact

    def orig(self, pos: int) -> int:
        if not self._starts:
            return 0
        i = bisect_right(self._starts, pos) - 1
        if i < 0:
            i = 0
        if self._exact[i]:
            return self._origs[i] + (pos - self._starts[i])
        return self._origs[i]


class _Builder:
    def __init__(self) -> None:
        self.chunks: List[str] = []
        self.starts: List[int] = []
        self.origs: List[int] = []
        self.exact: List[bool] = []
        self.n = 0

    def add(self, s: str, orig: int, exact: bool = True) -> None:
        if not s:
            return
        self.chunks.append(s)
        self.starts.append(self.n)
        self.origs.append(orig)
        self.exact.append(exact)
        self.n += len(s)

    def build(self) -> View:
        return View("".join(self.chunks), self.starts, self.origs, self.exact)


def _blank(s: str) -> str:
    """Same length, newlines kept, everything else a space."""
    return re.sub(r"[^\n]", " ", s)


def _apply_edits(text: str, edits: List[Tuple[int, int, Optional[str]]]) -> View:
    """Apply non-overlapping edits. ``None`` as replacement blanks the span.

    When edits overlap, the one that starts first (and is longest) wins.
    """
    b = _Builder()
    pos = 0
    for s, e, rep in sorted(edits, key=lambda x: (x[0], -x[1])):
        if s < pos or e <= s:
            continue
        b.add(text[pos:s], pos)
        if rep is None:
            b.add(_blank(text[s:e]), s)
        else:
            b.add(rep, s, exact=False)
        pos = e
    b.add(text[pos:], pos)
    return b.build()


# ---------------------------------------------------------------------------
# Scan records
# ---------------------------------------------------------------------------

@dataclass
class Attr:
    name: str
    start: int          # start of the attribute name
    vstart: int         # start of the value content (inside quotes / braces)
    vend: int
    kind: str           # "str", "expr" or "none"
    end: int            # end of the whole attribute (after closing quote/brace)


@dataclass
class Tag:
    name: str
    start: int
    end: int            # end of the opening tag
    attrs: List[Attr] = field(default_factory=list)


@dataclass
class Template:
    start: int
    end: int
    tag: str
    parts: List[Tuple[int, int]]
    exprs: List[Tuple[int, int]]


@dataclass
class Scan:
    blanks: List[Tuple[int, int]] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)
    texts: List[Tuple[int, int]] = field(default_factory=list)
    raw: List[Tuple[str, int, int]] = field(default_factory=list)
    strings: List[Tuple[int, int]] = field(default_factory=list)
    templates: List[Template] = field(default_factory=list)
    applies: List[Tuple[int, int]] = field(default_factory=list)
    css_blocks: List[Tuple[int, int]] = field(default_factory=list)
    # Template expressions inside HTML text or attributes ({{ }}, {!! !!}, {x}).
    exprs: List[Tuple[int, int]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CSS_TOKEN = re.compile(r"/\*|//|\"|'|url\(|@apply\b", re.I)


_DATA_URI = re.compile(r"data:[\w/+.-]*(?:;[\w=.+-]+)*,", re.I)


def _mask_data_uri(text: str, s: int, e: int, scan: Scan) -> None:
    """Blank the payload of every data URI inside ``text[s:e]``.

    A URI that starts the span runs to the span end (the span is already a
    string or ``url()`` body). A URI embedded deeper, such as
    ``bg-[url('data:...')]`` in a class list, ends at the quote or
    parenthesis that opened it.
    """
    if "data:" not in text[s:e].lower():
        return
    closers = {"'": "'", '"': '"', "(": ")"}
    pos = s
    while pos < e:
        m = _DATA_URI.search(text, pos, e)
        if not m:
            return
        k = m.end()
        stop = e
        if text[s:m.start()].strip():
            opener = text[m.start() - 1]
            if opener in closers:
                j = text.find(closers[opener], k, e)
                stop = e if j == -1 else j
        if stop > k:
            scan.blanks.append((k, stop))
        pos = max(stop, k)


def scan_css(text: str, start: int, end: int, scan: Scan, line_comments: bool) -> None:
    scan.css_blocks.append((start, end))
    pos = start
    while pos < end:
        m = _CSS_TOKEN.search(text, pos, end)
        if not m:
            return
        i = m.start()
        tok = m.group(0)
        if tok == "/*":
            j = text.find("*/", i + 2, end)
            j = end if j == -1 else j + 2
            scan.blanks.append((i, j))
            pos = j
        elif tok == "//":
            if line_comments and (i == 0 or text[i - 1] != ":"):
                j = text.find("\n", i, end)
                j = end if j == -1 else j
                scan.blanks.append((i, j))
                pos = j
            else:
                pos = i + 2
        elif tok in ("\"", "'"):
            j = _string_end(text, i, tok, end, multiline=False)
            _mask_data_uri(text, i + 1, j - 1, scan)
            pos = j
        elif tok.lower() == "url(":
            k = i + 4
            while k < end and text[k] in " \t":
                k += 1
            if k < end and text[k] in "\"'":
                pos = k
                continue
            j = text.find(")", k, end)
            j = end if j == -1 else j
            _mask_data_uri(text, k, j, scan)
            pos = j + 1
        else:  # @apply
            j = i + len(tok)
            while j < end and text[j] not in ";}\n":
                j += 1
            scan.applies.append((i + len(tok), j))
            pos = j


def _string_end(text: str, i: int, q: str, end: int, multiline: bool) -> int:
    """Index just past the closing quote of the string opened at ``i``."""
    k = i + 1
    while k < end:
        c = text[k]
        if c == "\\":
            k += 2
            continue
        if c == q:
            return k + 1
        if c == "\n" and not multiline:
            return k
        k += 1
    return end


def _paren_end(text: str, i: int, end: int) -> int:
    """Index just past the ``)`` that balances the ``(`` at ``i``."""
    depth = 0
    k = i
    while k < end:
        c = text[k]
        if c in "\"'":
            k = _string_end(text, k, c, end, multiline=False)
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return k + 1
        k += 1
    return end


# ---------------------------------------------------------------------------
# JavaScript, TypeScript and JSX
# ---------------------------------------------------------------------------

_JS_INTEREST = re.compile(r"[\"'`/{}<]")
_TAG_NAME = re.compile(r"[A-Za-z][\w.:\-]*")
_ATTR_NAME = re.compile(r"[^\s=/>{}\"'<]+")
_CHILD_INTEREST = re.compile(r"[<{]")
_HTML_CHILD_INTEREST = re.compile(r"<|\{\{|\{!!|\{")
_BLADE_CHILD_INTEREST = re.compile(r"<|\{\{|\{!!|\{|(?<![\w@.])@(?=[A-Za-z])")
_BLADE_DIRECTIVE = re.compile(r"@([A-Za-z]\w*)[ \t]*")


class _Scanner:
    """Scanner for JS-family code, JSX and HTML-family markup."""

    def __init__(self, text: str, scan: Scan, braces: bool = True,
                 vue: bool = False, blade: bool = False) -> None:
        self.t = text
        self.n = len(text)
        self.s = scan
        self.braces = braces      # "{...}" in markup is an expression
        self.vue = vue            # "{{ }}" in text, ":attr" values are JS
        self.blade = blade        # "{{-- --}}", "{{ }}", "{!! !!}"
        self.code_depth = 0       # inside <code>, <pre> and friends

    # Helpers

    def _prev_sig(self, i: int) -> Tuple[str, str]:
        """Previous non-space character and the word that ends there."""
        k = i - 1
        t = self.t
        while k >= 0 and t[k] in " \t\r\n":
            k -= 1
        if k < 0:
            return "", ""
        c = t[k]
        if c.isalnum() or c in "_$":
            j = k
            while j >= 0 and (t[j].isalnum() or t[j] in "_$"):
                j -= 1
            return c, t[j + 1:k + 1]
        return c, ""

    def _is_jsx_start(self, i: int) -> bool:
        t = self.t
        if i + 1 >= self.n:
            return False
        nxt = t[i + 1]
        if not (nxt.isalpha() or nxt == ">"):
            return False
        c, word = self._prev_sig(i)
        if word:
            if word not in _JSX_PREV_WORDS:
                return False
        elif c and c not in _JSX_PREV:
            return False
        if nxt == ">":
            return True
        m = _TAG_NAME.match(t, i + 1)
        if not m:
            return False
        k = m.end()
        while k < self.n and t[k] in " \t":
            k += 1
        # "<T," and "<T extends" are TypeScript generics, not elements.
        if k < self.n and t[k] == ",":
            return False
        if t.startswith("extends ", k):
            return False
        return True

    def _is_regex(self, i: int) -> bool:
        c, word = self._prev_sig(i)
        if word:
            return word in _REGEX_PREV_WORDS
        return c == "" or c in _REGEX_PREV

    def _regex_end(self, i: int) -> int:
        t = self.t
        k = i + 1
        in_class = False
        while k < self.n:
            c = t[k]
            if c == "\\":
                k += 2
                continue
            if c == "\n":
                return -1
            if c == "[":
                in_class = True
            elif c == "]":
                in_class = False
            elif c == "/" and not in_class:
                k += 1
                while k < self.n and t[k].isalpha():
                    k += 1
                return k
            k += 1
        return -1

    # JS mode

    def js(self, pos: int, end: int, stop_on_brace: bool, jsx: bool = True) -> int:
        """Scan JS from ``pos``. With ``stop_on_brace`` return just past the
        ``}`` that closes the enclosing expression."""
        t = self.t
        depth = 0
        while pos < end:
            m = _JS_INTEREST.search(t, pos, end)
            if not m:
                return end
            i = m.start()
            c = t[i]
            if c == "{":
                depth += 1
                pos = i + 1
            elif c == "}":
                if depth == 0 and stop_on_brace:
                    return i + 1
                depth = max(0, depth - 1)
                pos = i + 1
            elif c in "\"'":
                j = _string_end(t, i, c, end, multiline=False)
                self.s.strings.append((i + 1, max(i + 1, j - 1)))
                _mask_data_uri(t, i + 1, max(i + 1, j - 1), self.s)
                pos = j
            elif c == "`":
                pos = self.template(i, end)
            elif c == "/":
                nx = t[i + 1] if i + 1 < end else ""
                if nx == "/":
                    j = t.find("\n", i, end)
                    j = end if j == -1 else j
                    self.s.blanks.append((i, j))
                    pos = j
                elif nx == "*":
                    j = t.find("*/", i + 2, end)
                    j = end if j == -1 else j + 2
                    self.s.blanks.append((i, j))
                    pos = j
                elif self._is_regex(i):
                    j = self._regex_end(i)
                    pos = j if j != -1 else i + 1
                else:
                    pos = i + 1
            elif c == "<" and jsx and self._is_jsx_start(i):
                pos = self.element(i, end)
            else:
                pos = i + 1
        return end

    def template(self, i: int, end: int) -> int:
        t = self.t
        k = i + 1
        seg = k
        parts: List[Tuple[int, int]] = []
        exprs: List[Tuple[int, int]] = []
        tag = t[max(0, i - 120):i]
        while k < end:
            c = t[k]
            if c == "\\":
                k += 2
                continue
            if c == "`":
                parts.append((seg, k))
                self.s.templates.append(Template(i, k + 1, tag, parts, exprs))
                return k + 1
            if c == "$" and k + 1 < end and t[k + 1] == "{":
                parts.append((seg, k))
                j = self.js(k + 2, end, stop_on_brace=True)
                exprs.append((k, j))
                k = seg = j
                continue
            k += 1
        parts.append((seg, end))
        self.s.templates.append(Template(i, end, tag, parts, exprs))
        return end

    # Markup

    def open_tag(self, i: int, end: int) -> Tuple[Optional[Tag], int, bool]:
        """Parse ``<name attrs>`` at ``i``. Returns (tag, pos, self_closing)."""
        t = self.t
        m = _TAG_NAME.match(t, i + 1)
        name = m.group(0) if m else ""
        pos = m.end() if m else i + 1
        tag = Tag(name, i, pos)
        while pos < end:
            while pos < end and t[pos] in " \t\r\n":
                pos += 1
            if pos >= end:
                break
            c = t[pos]
            if c == ">":
                tag.end = pos + 1
                self.s.tags.append(tag)
                return tag, pos + 1, False
            if c == "/" and pos + 1 < end and t[pos + 1] == ">":
                tag.end = pos + 2
                self.s.tags.append(tag)
                return tag, pos + 2, True
            if c == "{" and self.braces:
                pos = self.js(pos + 1, end, stop_on_brace=True)
                continue
            if (self.blade or self.vue) and t.startswith(("{{", "{!!"), pos):
                close = "}}" if t.startswith("{{", pos) else "!!}"
                j = t.find(close, pos + 2, end)
                j = end if j == -1 else j + len(close)
                self.s.exprs.append((pos, j))
                self.js(pos + 2, max(pos + 2, j - len(close)), stop_on_brace=False, jsx=False)
                pos = j
                continue
            am = _ATTR_NAME.match(t, pos)
            if not am:
                pos += 1
                continue
            aname = am.group(0)
            astart = pos
            pos = am.end()
            k = pos
            while k < end and t[k] in " \t\r\n":
                k += 1
            if k < end and t[k] == "=":
                k += 1
                while k < end and t[k] in " \t\r\n":
                    k += 1
                if k >= end:
                    break
                q = t[k]
                if q in "\"'":
                    j = t.find(q, k + 1, end)
                    j = end if j == -1 else j
                    tag.attrs.append(Attr(aname, astart, k + 1, j, "str", min(end, j + 1)))
                    _mask_data_uri(t, k + 1, j, self.s)
                    if self.vue and (aname.startswith((":", "@", "v-"))):
                        self.js(k + 1, j, stop_on_brace=False, jsx=False)
                    elif self.braces or self.blade:
                        self._inline_exprs(k + 1, j)
                    pos = min(end, j + 1)
                elif q == "{" and self.braces:
                    j = self.js(k + 1, end, stop_on_brace=True)
                    tag.attrs.append(Attr(aname, astart, k + 1, max(k + 1, j - 1), "expr", j))
                    pos = j
                else:
                    j = k
                    while j < end and t[j] not in " \t\r\n>":
                        if t[j] == "/" and j + 1 < end and t[j + 1] == ">":
                            break
                        j += 1
                    tag.attrs.append(Attr(aname, astart, k, j, "str", j))
                    pos = j
            else:
                tag.attrs.append(Attr(aname, astart, pos, pos, "none", pos))
        tag.end = end
        self.s.tags.append(tag)
        return tag, end, True

    def _inline_exprs(self, s: int, e: int) -> None:
        """Record ``{{ }}``/``{x}`` expressions inside an attribute value."""
        t = self.t
        k = s
        while k < e:
            if t.startswith("{{", k):
                j = t.find("}}", k + 2, e)
                j = e if j == -1 else j + 2
                self.s.exprs.append((k, j))
                self.js(k + 2, max(k + 2, j - 2), stop_on_brace=False, jsx=False)
                k = j
            elif t[k] == "{" and self.braces:
                j = self.js(k + 1, e, stop_on_brace=True)
                self.s.exprs.append((k, j))
                k = j
            else:
                k += 1

    def raw_body(self, name: str, pos: int, end: int) -> int:
        t = self.t
        close = re.compile(r"</\s*" + re.escape(name) + r"\s*>", re.I).search(t, pos, end)
        body_end = close.start() if close else end
        self.s.raw.append((name.lower(), pos, body_end))
        return close.end() if close else end

    def _text(self, s: int, e: int) -> None:
        if e > s and self.code_depth == 0:
            self.s.texts.append((s, e))

    def _enter(self, name: str) -> None:
        if name.lower() in CODE_ELEMENTS:
            self.code_depth += 1

    def _leave(self, name: str) -> None:
        if name.lower() in CODE_ELEMENTS and self.code_depth:
            self.code_depth -= 1

    def element(self, i: int, end: int) -> int:
        """JSX element at ``i``; returns the position after it."""
        t = self.t
        if i + 1 < end and t[i + 1] == ">":
            name, pos = "", i + 2
        else:
            tag, pos, self_closing = self.open_tag(i, end)
            name = tag.name if tag else ""
            if self_closing:
                return pos
            if name.lower() in RAW_ELEMENTS:
                return self.raw_body(name, pos, end)
        self._enter(name)
        try:
            while pos < end:
                m = _CHILD_INTEREST.search(t, pos, end)
                if not m:
                    self._text(pos, end)
                    return end
                k = m.start()
                self._text(pos, k)
                if t[k] == "{":
                    pos = self.js(k + 1, end, stop_on_brace=True)
                    continue
                if t.startswith("</", k):
                    j = t.find(">", k, end)
                    return end if j == -1 else j + 1
                if t.startswith("<!--", k):
                    j = t.find("-->", k, end)
                    j = end if j == -1 else j + 3
                    self.s.blanks.append((k, j))
                    pos = j
                    continue
                if k + 1 < end and (t[k + 1].isalpha() or t[k + 1] == ">"):
                    pos = self.element(k, end)
                    continue
                pos = k + 1
            return end
        finally:
            self._leave(name)

    def html(self, pos: int, end: int) -> None:
        """Flat scan of HTML-family markup (HTML, Vue, Svelte, Blade, Astro)."""
        t = self.t
        text_start = pos
        interest = _BLADE_CHILD_INTEREST if self.blade else _HTML_CHILD_INTEREST
        while pos < end:
            m = interest.search(t, pos, end)
            if not m:
                break
            k = m.start()
            tok = m.group(0)
            if tok == "@":
                dm = _BLADE_DIRECTIVE.match(t, k)
                self._text(text_start, k)
                j = dm.end() if dm else k + 1
                if dm and dm.group(1) == "php" and not t.startswith("(", j):
                    close = t.find("@endphp", j, end)
                    close = end if close == -1 else close
                    self.js(j, close, stop_on_brace=False, jsx=False)
                    j = min(end, close + len("@endphp"))
                elif j < end and t[j] == "(":
                    j = _paren_end(t, j, end)
                    self.js(dm.end() if dm else k, j, stop_on_brace=False, jsx=False)
                self.s.exprs.append((k, j))
                pos = text_start = j
                continue
            if tok == "{{" and self.blade and t.startswith("{{--", k):
                j = t.find("--}}", k + 4, end)
                j = end if j == -1 else j + 4
                self._text(text_start, k)
                self.s.blanks.append((k, j))
                pos = text_start = j
                continue
            if tok in ("{{", "{!!") and (self.vue or self.blade):
                close = "}}" if tok == "{{" else "!!}"
                j = t.find(close, k + len(tok), end)
                j = end if j == -1 else j + len(close)
                self._text(text_start, k)
                self.s.exprs.append((k, j))
                self.js(k + len(tok), max(k + len(tok), j - len(close)), stop_on_brace=False, jsx=False)
                pos = text_start = j
                continue
            if tok == "{" and self.braces:
                self._text(text_start, k)
                j = self.js(k + 1, end, stop_on_brace=True)
                self.s.exprs.append((k, j))
                pos = text_start = j
                continue
            if tok == "<":
                if t.startswith("<!--", k):
                    self._text(text_start, k)
                    j = t.find("-->", k, end)
                    j = end if j == -1 else j + 3
                    self.s.blanks.append((k, j))
                    pos = text_start = j
                    continue
                if t.startswith("<?", k):
                    self._text(text_start, k)
                    j = t.find("?>", k, end)
                    j = end if j == -1 else j + 2
                    pos = text_start = j
                    continue
                if t.startswith("<!", k):
                    self._text(text_start, k)
                    j = t.find(">", k, end)
                    pos = text_start = end if j == -1 else j + 1
                    continue
                if t.startswith("</", k):
                    self._text(text_start, k)
                    nm = _TAG_NAME.match(t, k + 2)
                    if nm:
                        self._leave(nm.group(0))
                    j = t.find(">", k, end)
                    pos = text_start = end if j == -1 else j + 1
                    continue
                if k + 1 < end and t[k + 1].isalpha():
                    self._text(text_start, k)
                    tag, pos, self_closing = self.open_tag(k, end)
                    text_start = pos
                    if tag and not self_closing:
                        low = tag.name.lower()
                        if low in RAW_ELEMENTS:
                            pos = text_start = self.raw_body(tag.name, pos, end)
                        else:
                            self._enter(tag.name)
                    continue
            pos = k + 1
        self._text(text_start, end)


# ---------------------------------------------------------------------------
# Style objects
# ---------------------------------------------------------------------------

_KEY = re.compile(r"\s*(?:\.\.\.[^,}]*|\[[^\]]*\]|\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)'|([\w$-]+))\s*")
_NUMBER = re.compile(r"-?(?:\d+\.?\d*|\.\d+)$")


def _kebab(key: str) -> str:
    if key.startswith("--"):
        return key
    out = re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), key)
    if out.startswith(("webkit-", "moz-", "ms-")):
        out = "-" + out
    return out


def _value_end(text: str, pos: int, end: int) -> int:
    """End of a JS value starting at ``pos``: next top-level ``,`` or ``}``."""
    depth = 0
    k = pos
    while k < end:
        c = text[k]
        if c in "\"'":
            k = _string_end(text, k, c, end, multiline=False)
            continue
        if c == "`":
            k += 1
            while k < end and text[k] != "`":
                k += 2 if text[k] == "\\" else 1
            k += 1
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                return k
            depth -= 1
        elif c == "," and depth == 0:
            return k
        k += 1
    return end


def style_object(text: str, start: int, end: int) -> List[Tuple[str, str, int, bool]]:
    """Parse a JS object literal ``{...}`` spanning ``text[start:end]``.

    Returns ``(property, value, offset, static)`` declarations. Nested objects
    (selectors, breakpoints) are flattened. ``static`` is False when the value
    is computed at runtime.
    """
    out: List[Tuple[str, str, int, bool]] = []
    k = text.find("{", start, end)
    if k == -1:
        return out
    _object_into(text, k + 1, end, out, 0)
    return out


def _object_into(text: str, pos: int, end: int, out: list, depth: int) -> int:
    while pos < end:
        while pos < end and text[pos] in " \t\r\n,":
            pos += 1
        if pos >= end or text[pos] == "}":
            return pos + 1
        m = _KEY.match(text, pos, end)
        if not m or m.end() == pos:
            pos = _value_end(text, pos, end) + 1
            continue
        key = m.group(1) or m.group(2) or m.group(3)
        key_at = pos + (len(m.group(0)) - len(m.group(0).lstrip()))
        pos = m.end()
        if pos < end and text[pos] == "?":
            pos += 1
        if not key or pos >= end or text[pos] != ":":
            # shorthand, spread or method: skip to the next entry
            pos = _value_end(text, pos, end) + 1
            continue
        pos += 1
        while pos < end and text[pos] in " \t\r\n":
            pos += 1
        if pos < end and text[pos] == "{" and depth < 8:
            pos = _object_into(text, pos + 1, end, out, depth + 1)
            continue
        vend = _value_end(text, pos, end)
        raw = text[pos:vend].strip()
        raw = re.sub(r"\s+as\s+[\w.<>\[\]\s|]+$", "", raw)
        prop = _kebab(key)
        value, static = _js_value(raw, prop)
        if value is not None:
            out.append((prop, value, key_at, static))
        pos = vend + 1
    return end


def _js_value(raw: str, prop: str) -> Tuple[Optional[str], bool]:
    if not raw:
        return None, False
    if raw[0] in "\"'" and raw[-1] == raw[0] and len(raw) >= 2:
        return raw[1:-1], True
    if raw[0] == "`" and raw[-1] == "`":
        body = raw[1:-1]
        dynamic = "${" in body
        return re.sub(r"\$\{[^}]*\}", "0", body), not dynamic
    if _NUMBER.match(raw):
        if prop in UNITLESS or prop.startswith("--") or raw in ("0", "-0"):
            return raw, True
        return raw + "px", True
    return None, False


def style_css(decls: List[Tuple[str, str, int, bool]]) -> str:
    return "; ".join(f"{p}: {v}" for p, v, _, _ in decls)


# ---------------------------------------------------------------------------
# File views
# ---------------------------------------------------------------------------

def file_kind(path_name: str) -> str:
    """Scanner family for a file name: css, jsx, astro, vue, svelte, blade,
    md or html."""
    name = path_name.lower()
    ext = name.rsplit(".", 1)[-1] if "." in name else ""
    if ext in CSS_EXTS:
        return "css"
    if ext in JSX_EXTS:
        return "jsx"
    if ext in MD_EXTS:
        return "md"
    if ext == "php":
        return "blade"
    if ext in ("astro", "vue", "svelte"):
        return ext
    return "html"


def _is_class_like(s: str) -> bool:
    if "://" in s or s.startswith(("/", "./", "../", "data:", "#", "@")):
        return False
    toks = s.split()
    if len(toks) == 1 and re.search(r"\.[a-z0-9]{2,5}$", s):
        return False
    if not toks:
        return False
    if not all(_CLASS_TOKEN.match(t) for t in toks):
        return False
    return any(("-" in t or ":" in t) for t in toks)


def _is_sentence(s: str) -> bool:
    return bool(_WS.search(s.strip())) and bool(_WORD.search(s)) and not _is_class_like(s)


class FileViews:
    """Lazily built channel views of one file."""

    def __init__(self, name: str, text: str) -> None:
        self.name = name
        self.text = text
        self.kind = file_kind(name)
        self._scan: Optional[Scan] = None
        self._cache: Dict[str, Optional[View]] = {}

    # Scanning

    @property
    def scan(self) -> Scan:
        if self._scan is None:
            self._scan = self._do_scan()
        return self._scan

    def _do_scan(self) -> Scan:
        t = self.text
        n = len(t)
        s = Scan()
        kind = self.kind
        if kind == "css":
            scan_css(t, 0, n, s, line_comments=self.name.lower().endswith((".scss", ".sass", ".less")))
            return s
        if kind == "md":
            return s
        if kind == "jsx":
            jsx = not self.name.lower().endswith((".ts", ".mts", ".cts"))
            _Scanner(t, s, braces=True).js(0, n, stop_on_brace=False, jsx=jsx)
        else:
            start = 0
            if kind == "astro":
                m = re.match(r"\s*---[ \t]*\n", t)
                if m:
                    close = t.find("\n---", m.end())
                    fm_end = n if close == -1 else close + 4
                    _Scanner(t, s).js(m.end(), min(n, close if close != -1 else n),
                                      stop_on_brace=False, jsx=False)
                    start = fm_end
            sc = _Scanner(
                t, s,
                braces=kind in ("astro", "svelte"),
                vue=kind == "vue",
                blade=kind == "blade",
            )
            sc.html(start, n)
            for name, bs, be in list(s.raw):
                if name == "style":
                    scan_css(t, bs, be, s, line_comments=False)
                elif name == "script":
                    _Scanner(t, s).js(bs, be, stop_on_brace=False, jsx=False)
        return s

    # Channels

    def get(self, channel: str) -> Optional[View]:
        if channel not in self._cache:
            builder = getattr(self, "_v_" + channel, None)
            self._cache[channel] = builder() if builder else None
        return self._cache[channel]

    def _v_raw(self) -> View:
        return View(self.text, [0], [0], [True])

    def _code_edits(self) -> List[Tuple[int, int, Optional[str]]]:
        edits: List[Tuple[int, int, Optional[str]]] = [(a, b, None) for a, b in self.scan.blanks]
        if self.kind in ("jsx", "astro", "svelte"):
            for tag in self.scan.tags:
                for a in tag.attrs:
                    low = a.name.lower()
                    if low == "classname" and a.kind == "str":
                        edits.append((a.start, a.start + len(a.name), "class"))
                    elif low in ("classname", "class", "class:list") and a.kind == "expr":
                        joined = " ".join(self.text[x:y] for x, y in self._strings_in(a.vstart, a.vend))
                        edits.append((a.start, a.end, 'class="%s"' % joined.replace('"', "'")))
                    elif low in ("style", "sx") and a.kind == "expr":
                        css = self._attr_css(a, static_only=True)
                        edits.append((a.start, a.end, '%s="%s"' % (low, css.replace('"', "'"))))
        return edits

    def _v_code(self) -> View:
        if self.kind == "md":
            return self._md_view()
        return _apply_edits(self.text, self._code_edits())

    def _v_markup(self) -> Optional[View]:
        if self.kind == "css":
            return None
        if self.kind == "md":
            return self._md_view()
        edits = self._code_edits()
        edits.extend((bs, be, None) for _, bs, be in self.scan.raw)
        # Server-side template expressions are code, not markup: "->" in
        # {{ $user->name }} is not an arrow in a link label.
        for es, ee in self.scan.exprs:
            if self.text.startswith(("{{", "{!!", "@"), es):
                edits.append((es + 1, max(es + 1, ee - 1), None))
        return _apply_edits(self.text, edits)

    def _md_view(self) -> View:
        edits: List[Tuple[int, int, Optional[str]]] = []
        for m in re.finditer(r"(?ms)^(```|~~~).*?^\1[^\n]*$|`[^`\n]+`|<!--.*?-->", self.text):
            edits.append((m.start(), m.end(), None))
        return _apply_edits(self.text, edits)

    def _strings_in(self, s: int, e: int) -> List[Tuple[int, int]]:
        out = [(a, b) for a, b in self.scan.strings if s <= a and b <= e]
        for tpl in self.scan.templates:
            if s <= tpl.start and tpl.end <= e:
                out.extend(tpl.parts)
        out.sort()
        return out

    def _attr_css(self, a: Attr, static_only: bool = False) -> str:
        """CSS text of a style attribute expression. With ``static_only``,
        values computed at runtime are left out."""
        t = self.text
        inner = t[a.vstart:a.vend].strip()
        if inner.startswith("`"):
            if static_only and "${" in inner:
                return ""
            return re.sub(r"\$\{[^}]*\}", "0", inner.strip("`"))
        if inner.startswith(("\"", "'")):
            return inner[1:-1]
        return style_css([d for d in style_object(t, a.vstart, a.vend) if d[3]])

    def _v_css(self) -> View:
        b = _Builder()
        sc = self.scan
        t = self.text
        if self.kind == "css":
            code = self.get("code")
            assert code is not None
            return code
        if self.kind == "md":
            return b.build()
        blanked = _apply_edits(t, [(x, y, None) for x, y in sc.blanks]).text
        for name, bs, be in sc.raw:
            if name == "style":
                b.add(blanked[bs:be], bs)
                b.add("\n", be, exact=False)
        for tag in sc.tags:
            for a in tag.attrs:
                low = a.name.lower()
                if low not in STYLE_ATTRS:
                    continue
                sel = tag.name or "_"
                if a.kind == "str" and not low.startswith((":", "v-bind")):
                    b.add(sel + " { ", a.start, exact=False)
                    b.add(blanked[a.vstart:a.vend], a.vstart)
                    b.add(" }\n", a.vend, exact=False)
                elif a.kind == "expr" or low.startswith((":", "v-bind")):
                    inner = t[a.vstart:a.vend].strip()
                    if inner.startswith("`"):
                        b.add(sel + " { ", a.start, exact=False)
                        b.add(self._attr_css(a), a.vstart, exact=False)
                        b.add(" }\n", a.vend, exact=False)
                        continue
                    decls = style_object(t, a.vstart, a.vend)
                    if not decls:
                        continue
                    b.add(sel + " {\n", a.start, exact=False)
                    for prop, value, at, _static in decls:
                        b.add("  %s: %s;\n" % (prop, value), at, exact=False)
                    b.add("}\n", a.vend, exact=False)
        for tpl in sorted(sc.templates, key=lambda tp: tp.start):
            if _CSS_IN_JS_TAG.search(tpl.tag):
                b.add("_ {\n", tpl.start, exact=False)
                for (ps, pe), nxt in zip(tpl.parts, tpl.exprs + [None]):
                    b.add(blanked[ps:pe], ps)
                    if nxt is not None:
                        b.add("0", nxt[0], exact=False)
                b.add("\n}\n", tpl.end, exact=False)
        return b.build()

    def _v_classes(self) -> View:
        b = _Builder()
        sc = self.scan
        t = self.text

        def seg(pieces: List[Tuple[int, int]], at: int) -> None:
            pieces = [p for p in pieces if p[1] > p[0]]
            if not pieces:
                return
            b.add('class="', at, exact=False)
            for i, (x, y) in enumerate(pieces):
                if i:
                    b.add(" ", x, exact=False)
                b.add(t[x:y].replace('"', "'"), x)
            b.add('"\n', pieces[-1][1], exact=False)

        in_attr: List[Tuple[int, int]] = []
        for tag in sc.tags:
            for a in tag.attrs:
                low = a.name.lower()
                if a.kind == "expr" or low.startswith((":", "v-bind", "@", "v-")):
                    in_attr.append((a.vstart, a.vend))
                if low not in CLASS_ATTRS:
                    continue
                if a.kind == "str" and not low.startswith((":", "v-bind")):
                    seg([(a.vstart, a.vend)], a.vstart)
                else:
                    seg(self._strings_in(a.vstart, a.vend), a.vstart)
        for x, y in sc.applies:
            seg([(x, y)], x)
        if self.kind in ("jsx", "astro", "vue", "svelte", "html", "blade"):
            in_attr.sort()
            starts = [p[0] for p in in_attr]
            for x, y in self._script_strings():
                i = bisect_right(starts, x) - 1
                if i >= 0 and in_attr[i][0] <= x and y <= in_attr[i][1]:
                    continue
                if _is_class_like(t[x:y]):
                    seg([(x, y)], x)
        return b.build()

    def _script_strings(self) -> List[Tuple[int, int]]:
        """String literals and template parts outside CSS-in-JS templates."""
        sc = self.scan
        css_tpls = [(tp.start, tp.end) for tp in sc.templates if _CSS_IN_JS_TAG.search(tp.tag)]
        t = self.text
        out: List[Tuple[int, int]] = [
            (a, b) for a, b in sc.strings if not _IMPORT_BEFORE.search(t, max(0, a - 40), max(0, a - 1))
        ]
        for tp in sc.templates:
            if (tp.start, tp.end) in css_tpls:
                continue
            out.extend(tp.parts)
        if css_tpls:
            out = [p for p in out if not any(a <= p[0] and p[1] <= b for a, b in css_tpls)]
        out.sort()
        return out

    def _v_text(self) -> View:
        b = _Builder()
        sc = self.scan
        t = self.text
        if self.kind == "md":
            return self._md_view()
        if self.kind == "css":
            return b.build()
        blank_exprs = sorted(sc.exprs)
        segs: List[Tuple[int, int]] = []

        def add_cut(x: int, y: int) -> None:
            """Add ``text[x:y]`` minus the template expressions inside it."""
            pos = x
            for es, ee in blank_exprs:
                if ee <= pos or es >= y:
                    continue
                if es > pos:
                    segs.append((pos, es))
                pos = max(pos, ee)
            if pos < y:
                segs.append((pos, y))

        for x, y in sc.texts:
            add_cut(x, y)
        non_copy: List[Tuple[int, int]] = []
        for tag in sc.tags:
            meta_copy = tag.name.lower() == "meta" and any(
                a.name.lower() in ("name", "property")
                and re.search(r"description|title|og:|twitter:", t[a.vstart:a.vend], re.I)
                for a in tag.attrs
            )
            for a in tag.attrs:
                low = a.name.lower()
                if a.kind == "str" and (low in COPY_ATTRS or (meta_copy and low == "content")):
                    add_cut(a.vstart, a.vend)
                elif low.lstrip(":") in COPY_ATTRS:
                    continue
                elif low in NON_COPY_ATTRS or low.startswith(("data-", "on", ":", "@", "v-", "x-")):
                    non_copy.append((a.vstart, a.vend))
        for tpl in sc.templates:
            if _CSS_IN_JS_TAG.search(tpl.tag):
                non_copy.append((tpl.start, tpl.end))
        non_copy.sort()
        starts = [p[0] for p in non_copy]
        for x, y in self._script_strings():
            i = bisect_right(starts, x) - 1
            if i >= 0 and non_copy[i][0] <= x and y <= non_copy[i][1]:
                continue
            if _is_sentence(t[x:y]):
                segs.append((x, y))
        for x, y in sorted(segs):
            if t[x:y].strip():
                b.add(t[x:y], x)
                b.add("\n\n", y, exact=False)
        return b.build()


_QUOTE_OPEN = ("\"", "'", "“", "‘", "«", "&ldquo;", "&lsquo;", "&quot;", "&laquo;", "&#8220;")
_QUOTE_CLOSE = ("\"", "'", "”", "’", "»", "&rdquo;", "&rsquo;", "&quot;", "&raquo;", "&#8221;")


def is_mention(text: str, s: int, e: int) -> bool:
    """True when ``text[s:e]`` is wrapped in quotation marks: a mention of the
    phrase, not a use of it."""
    before = text[max(0, s - 8):s]
    after = text[e:e + 8]
    return before.endswith(_QUOTE_OPEN) and after.startswith(_QUOTE_CLOSE)
