"""Measure what a codebase actually uses: every value written in CSS
(plain, SCSS or Less, nested rules and at-rules included, and <style>
blocks), in style attributes (HTML, Blade, Vue, Svelte, Astro), in JSX
style props and in Tailwind classes. Each use records its file, line,
property, the family it belongs to (color, space, radius, border,
type-size, leading, tracking, weight, font, shadow, duration, motion, z),
whether it names a token or writes a raw value, and the state it applies
in.

A raw value is kept in one canonical form (a color as #RRGGBB, a length in
px, a duration in ms) beside the text as written, so the drift report can
tell a value written many ways. Values are read by the importers' value
reader (values_in), so an out-of-gamut oklch() is mapped into sRGB, never
refused; a value with no single reading is not a use. A var() reference is
a use of the token it names, or "missing" when the system has no such
token. A custom property, SCSS or Less variable set in the app's own CSS is
a definition, not a raw use, and so is an @font-face or @property block.

A Tailwind class names a token when the system has one in the class's theme
namespace, in the names the Tailwind importer gives them (bg-ink reads
color-ink from a v4 @theme, or colors.ink from a v3 theme exported as
JSON); a numeric spacing class reads the v4 --spacing step. An arbitrary
class (p-[13px]) is a raw value, and a bare value Tailwind writes as it is
(z-10, duration-150, border-2) is raw too. A value class that names no
token is listed apart in unknown_classes; a class that sets a keyword
(text-center, border-solid) is not a value. Variants are states: hover,
focus, active and disabled (group- and peer- forms included), and dark:
records the scheme as the importers name it, scheme:dark. CSS records the
same from its selectors and queries. A state joins the scheme first:
"scheme:dark,hover".

The scanner only reads files and never runs code. It walks folders sorted,
skips SKIP_DIRS and hidden folders, the paths in `exclude` (the system's
own source), and reports in Scan.skipped each file it does not read: one
larger than MAX_BYTES, a binary file, text that is not UTF-8, a minified
build file and a stylesheet whose blocks do not close.
"""
from __future__ import annotations

import os
import re
from bisect import bisect_right
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

from engine.foundations.errors import InputError, _brief_text
from engine.foundations.tokens import TokenSet
from engine.foundations.values import TYPES, dimension_px, duration_ms
from engine.io.css_in import _without_not, parse_css
from engine.io.values_in import NotRead, read_value, split_top

SKIP_DIRS = ("node_modules", ".git", "dist", "build", "vendor", ".next", "out", "coverage",
             ".venv", "venv", "__pycache__", ".nuxt", ".svelte-kit", ".turbo", ".cache",
             "bower_components", "target", ".output", "storage")
CSS_EXT = (".css", ".scss", ".less")
MARKUP_EXT = (".html", ".htm", ".php", ".vue", ".svelte", ".astro")
SCRIPT_EXT = (".jsx", ".tsx", ".js", ".ts", ".mjs", ".cjs")
# A file larger than this is build output or data, not code a person writes.
MAX_BYTES = 1_000_000

# CSS property -> the family a length in it belongs to.
_LENGTH_FAMILY = [
    (re.compile(r"(margin|padding|gap|row-gap|column-gap|inset)(-.*)?$"), "space"),
    (re.compile(r"border(-.*)?-radius$"), "radius"),
    (re.compile(r"(border|outline)(-(block|inline|top|right|bottom|left)(-(start|end))?)?"
                r"(-width)?$"), "border"),
    (re.compile(r"font-size$"), "type-size"),
    (re.compile(r"letter-spacing$"), "tracking"),
    (re.compile(r"line-height$"), "leading"),
]
# Properties a color is written in.
_COLOR_PROPS = re.compile(r"(color|background(-color|-image)?|border(-.*)?(-color)?|"
                          r"outline(-color)?|fill|stroke|text-decoration(-color)?|"
                          r"box-shadow|text-shadow|filter|backdrop-filter|mask(-image)?|"
                          r"border-image(-source)?|column-rule(-color)?|.*-color)$")
_NUMBER_FAMILY = {"z-index": "z", "line-height": "leading", "font-weight": "weight"}
# A property a var() to a token the system lacks is placed by.
_PROP_FAMILY = {"box-shadow": "shadow", "font-family": "font", "font-weight": "weight",
                "z-index": "z", "transition-duration": "duration",
                "animation-duration": "duration", "transition-delay": "duration",
                "animation-delay": "duration", "transition-timing-function": "motion",
                "animation-timing-function": "motion"}
_WEIGHT_WORDS = {"normal": 400, "bold": 700}
# React's style props that take a plain number (any other number is px).
_UNITLESS = frozenset((
    "animationIterationCount", "aspectRatio", "borderImageOutset", "borderImageSlice",
    "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns",
    "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea",
    "gridRow", "gridRowEnd", "gridRowSpan", "gridRowStart", "gridColumn", "gridColumnEnd",
    "gridColumnSpan", "gridColumnStart", "fontWeight", "lineClamp", "lineHeight", "opacity",
    "order", "orphans", "scale", "tabSize", "widows", "zIndex", "zoom", "fillOpacity",
    "floodOpacity", "stopOpacity", "strokeDasharray", "strokeDashoffset", "strokeMiterlimit",
    "strokeOpacity", "strokeWidth"))

# States: CSS pseudo-classes and attributes, and Tailwind variants.
_CSS_STATE = re.compile(r":(hover|active|focus-visible|focus-within|focus|disabled)(?![\w-])"
                        r"|\[(disabled|aria-disabled)[\]=]")
_STATES = {"hover": "hover", "active": "active", "focus": "focus", "focus-visible": "focus",
           "focus-within": "focus", "disabled": "disabled", "aria-disabled": "disabled"}
DARK = "scheme:dark"
_DARK_SELECTOR = re.compile(r"""\.dark(?![\w-])|\[class~=["']?dark["']?\]|"""
                            r"""\[[\w-]*(?:theme|mode|scheme)[\w-]*\s*=\s*["']?dark["']?\s*\]""")
_DARK_MEDIA = re.compile(r"prefers-color-scheme\s*:\s*dark")

# Tailwind: utility prefix -> the theme namespaces its value may name, with
# the family of a token found in each (v4 @theme names first, then v3 theme
# keys), and the family a value read from an arbitrary class gets by type.
_C = (("color", "color"), ("colors", "color"))
_Namespaces = Tuple[Tuple[str, str], ...]
_UTILITIES: List[Tuple[re.Pattern, _Namespaces, Dict[str, str]]] = [
    (re.compile(r"bg"), _C + (("backgroundColor", "color"),), {"color": "color"}),
    (re.compile(r"text"), _C + (("textColor", "color"), ("text", "type-size"),
                                ("fontSize", "type-size")),
     {"color": "color", "dimension": "type-size"}),
    (re.compile(r"border(-[xytrblse])?"), _C + (("borderColor", "color"),
                                                ("borderWidth", "border")),
     {"color": "color", "dimension": "border"}),
    (re.compile(r"ring|outline"), _C + (("ringColor", "color"), ("outlineColor", "color"),
                                        ("ringWidth", "border"), ("outlineWidth", "border")),
     {"color": "color", "dimension": "border"}),
    (re.compile(r"fill|stroke|decoration|accent|caret|divide(-[xy])?|from|via|to|placeholder"),
     _C, {"color": "color"}),
    (re.compile(r"(p|m)[xytrblse]?|gap(-[xy])?|space-[xy]|inset(-[xy])?"),
     (("spacing", "space"),), {"dimension": "space"}),
    (re.compile(r"rounded(-([trblse]|tl|tr|br|bl|ss|se|es|ee))?"),
     (("radius", "radius"), ("borderRadius", "radius")), {"dimension": "radius"}),
    (re.compile(r"shadow"), (("shadow", "shadow"), ("boxShadow", "shadow")) + _C,
     {"shadow": "shadow", "color": "color"}),
    (re.compile(r"font"), (("font", "font"), ("fontFamily", "font"), ("font-weight", "weight"),
                           ("fontWeight", "weight")), {"fontFamily": "font", "number": "weight"}),
    (re.compile(r"leading"), (("leading", "leading"), ("lineHeight", "leading")),
     {"dimension": "leading", "number": "leading"}),
    (re.compile(r"tracking"), (("tracking", "tracking"), ("letterSpacing", "tracking")),
     {"dimension": "tracking"}),
    (re.compile(r"ease"), (("ease", "motion"), ("transitionTimingFunction", "motion")),
     {"cubicBezier": "motion"}),
    (re.compile(r"duration"), (("duration", "duration"), ("transitionDuration", "duration")),
     {"duration": "duration"}),
    (re.compile(r"z"), (("z", "z"), ("zIndex", "z")), {"number": "z"}),
]
# Classes that set a keyword, not a value: never listed as unknown.
_KEYWORD_CLASS = re.compile(
    r"text-(left|center|right|justify|start|end|wrap|nowrap|balance|pretty|ellipsis|clip)"
    r"|(border|outline|decoration|divide)(-[xytrblse])?-(solid|dashed|dotted|double|hidden|none"
    r"|wavy|collapse|separate)|border-spacing(-.*)?"
    r"|bg-(fixed|local|scroll|cover|contain|auto|center|top|bottom|left|right|none|repeat.*"
    r"|no-repeat|clip-.*|origin-.*|blend-.*|gradient-.*|linear-.*|radial.*|conic.*|[a-z]+-top"
    r"|[a-z]+-bottom)"
    r"|[a-z-]+-(transparent|current|inherit|none|auto|initial)|rounded(-[a-z]+)?-(none|full)"
    r"|ring-(inset|offset(-.*)?)|outline-offset(-.*)?|decoration-(from-font|clone|slice)"
    r"|(space|divide)-[xy]-reverse|ring|outline|shadow-inner")
_NUMERIC = re.compile(r"\d+(\.\d+)?")
# Utilities Tailwind writes with no value (border, rounded, shadow).
_BARE = re.compile(r"border(-[xytrblse])?|rounded(-[a-z]+)?|shadow|ring|outline|divide-[xy]")
# Tailwind's type hints in an arbitrary value, and the type each one reads.
_HINT_KINDS = {"color": "color", "length": "dimension", "size": "dimension",
               "number": "number", "family-name": "fontFamily", "shadow": "shadow",
               "line-width": "dimension"}
_REST = re.compile(r"[A-Za-z0-9._-]*")
_TYPE_HINT = re.compile(r"([a-z][a-z-]*):(?!//)")

# Markup and scripts.
_ATTR_START = re.compile(r"(?<![\w$-])(:|v-bind:|x-bind:)?(className|class:list|class|style)"
                         r"\s*=\s*")
_STYLE_DIRECTIVE = re.compile(r"""(?<![\w-])style:([a-z-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')""")
_OBJ_ENTRY = re.compile(r"""(?:([A-Za-z_$][\w$]*)|'([\w-]+)'|"([\w-]+)")\s*:\s*"""
                        r"""(?:'([^'\n]*)'|"([^"\n]*)"|(-?(?:\d+\.?\d*|\.\d+))(?![\w.%]))""")
_JS_STRING = re.compile(r""""((?:[^"\\\n]|\\.)*)"|'((?:[^'\\\n]|\\.)*)'|`((?:[^`\\]|\\.)*)`""",
                        re.S)
_STYLE_BLOCK = re.compile(r"<style\b([^>]*)>(.*?)</style\s*>", re.S | re.I)
_PREPROCESSED = re.compile(r"""lang\s*=\s*["']?(scss|sass|less)""", re.I)
_MARKUP_COMMENT = re.compile(r"<!--.*?-->|\{\{--.*?--\}\}", re.S)
_LINE_COMMENT = re.compile(r"(^|[\s;{}])(//[^\n]*)", re.M)
_IMPORTANT = re.compile(r"\s*!important\s*$", re.I)


@dataclass(frozen=True)
class Usage:
    file: str
    line: int
    prop: str      # the CSS property, or the utility class without its variants
    family: str    # "" when the property puts a token in no family (a width)
    kind: str      # "token", "raw" or "missing" (a var() to a token the system lacks)
    value: str     # the token path, the raw value in its canonical form, or --name
    text: str      # as written
    state: str     # "", "hover", "active", "focus", "disabled", "scheme:dark" or both joined

    def where(self) -> str:
        return f"{self.file}:{self.line}"


@dataclass
class Scan:
    usages: List[Usage] = field(default_factory=list)
    files: int = 0
    # (file, line, class) for value classes that name no token
    unknown_classes: List[Tuple[str, int, str]] = field(default_factory=list)
    # (file, why it was not read, with the fix)
    skipped: List[Tuple[str, str]] = field(default_factory=list)


def _norm(name: str) -> str:
    return ".".join(p for p in re.split(r"[.\-/_ ]+", name.lower()) if p)


def canonical(kind: str, value: Any) -> str:
    """One text per value, whatever way it was written."""
    if kind == "dimension":
        return f"{round(dimension_px(value), 4):g}px"
    if kind == "duration":
        return f"{round(duration_ms(value), 4):g}ms"
    if kind == "number":
        return f"{value:g}"
    if kind == "fontFamily":
        return ", ".join(value)
    return TYPES[kind].css(value)


def _join_state(scheme: str, state: str) -> str:
    return ",".join(s for s in (scheme, state) if s)


def _selector_state(selector: str, media: Tuple[str, ...]) -> str:
    """The state a rule applies in: its scheme and its interaction state,
    each taken only when every selector in the list has it (what a :not()
    names is where the rule is not)."""
    members = [_without_not(m) for m in split_top(selector, ",")] or [""]
    dark = any(_DARK_MEDIA.search(m) or m == "@variant dark" for m in media) \
        or all(_DARK_SELECTOR.search(m) for m in members)
    states = set()
    for m in members:
        found = _CSS_STATE.search(m)
        states.add(_STATES[found.group(1) or found.group(2)] if found else "")
    return _join_state(DARK if dark else "", states.pop() if len(states) == 1 else "")


def _variants(cls: str) -> Tuple[List[str], str]:
    """A class's variants and its utility, split on ':' outside brackets."""
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(cls):
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth -= 1
        elif ch == ":" and depth == 0:
            parts.append(cls[start:i])
            start = i + 1
    return parts, cls[start:]


def _merge_state(outer: str, inner: str) -> str:
    """A class's state inside a rule's (an @apply): dark when either is,
    and the class's own interaction state before the rule's."""
    outer_parts, inner_parts = outer.split(","), inner.split(",")
    scheme = DARK if DARK in outer_parts + inner_parts else ""
    states = [s for s in inner_parts + outer_parts if s and s != DARK]
    return _join_state(scheme, states[0] if states else "")


def _variant_state(variants: List[str]) -> str:
    scheme, state = "", ""
    for v in variants:
        v = re.sub(r"^(group|peer)-", "", v.split("/", 1)[0])
        if v == "dark":
            scheme = DARK
        elif v in _STATES and not state:
            state = _STATES[v]
    return _join_state(scheme, state)


def _top_vars(value: str) -> List[Tuple[str, int, int]]:
    """(name, start, end) of each var() at the top of `value`; a var() in
    another's fallback belongs to it."""
    out, i = [], 0
    while True:
        at = value.find("var(", i)
        if at == -1:
            return out
        depth, end = 0, len(value)
        for j in range(at + 3, len(value)):
            depth += {"(": 1, ")": -1}.get(value[j], 0)
            if depth == 0:
                end = j + 1
                break
        m = re.match(r"var\(\s*--([A-Za-z0-9_-]+)", value[at:])
        if m and (at == 0 or not (value[at - 1].isalnum() or value[at - 1] in "-_")):
            out.append((m.group(1), at, end))
        i = end


def _prefix_splits(utility: str) -> Iterator[Tuple[str, str]]:
    """(prefix, rest) for the whole utility and each '-' it could split at,
    longest prefix first (rounded-t-lg tries rounded-t, then rounded)."""
    parts = utility.split("-")
    for n in range(len(parts), 0, -1):
        yield "-".join(parts[:n]), "-".join(parts[n:])


class _Lines:
    """Offsets to line numbers in one text."""

    def __init__(self, text: str) -> None:
        self.starts = [0] + [m.end() for m in re.finditer("\n", text)]

    def __call__(self, pos: int) -> int:
        return bisect_right(self.starts, pos)


class _Scanner:
    def __init__(self, ts: TokenSet) -> None:
        self.index: Dict[str, Tuple[str, str]] = {}
        for t in ts.tokens():
            self.index.setdefault(_norm(t.path), (t.path, t.type))
        self.result = Scan()
        self._found: List[Tuple[int, int, int, Usage]] = []
        self._unknown: List[Tuple[int, int, int, Tuple[str, int, str]]] = []
        self._seq = 0
        self.file = ""

    def token(self, name: str) -> Optional[Tuple[str, str]]:
        return self.index.get(_norm(name))

    # Collecting ----------------------------------------------------------

    def begin(self, file: str) -> None:
        self.file, self._found, self._unknown = file, [], []

    def end(self) -> None:
        self._found.sort(key=lambda f: f[:3])
        self._unknown.sort(key=lambda f: f[:3])
        self.result.usages.extend(f[3] for f in self._found)
        self.result.unknown_classes.extend(f[3] for f in self._unknown)

    def add(self, at: Tuple[int, int], prop: str, family: str, kind: str, value: str,
            text: str, state: str) -> None:
        self._seq += 1
        self._found.append((at[0], at[1], self._seq,
                            Usage(self.file, at[0], prop, family, kind, value, text, state)))

    def unknown(self, at: Tuple[int, int], cls: str) -> None:
        self._seq += 1
        self._unknown.append((at[0], at[1], self._seq, (self.file, at[0], cls)))

    # Values --------------------------------------------------------------

    @staticmethod
    def family_of(prop: str, kind: Optional[str]) -> str:
        """The family a value of `kind` in `prop` belongs to ("" for none);
        kind None is a var() to a token the system lacks."""
        if kind == "color":
            return "color" if _COLOR_PROPS.match(prop) else ""
        if kind in ("dimension", None):
            if kind is None and _COLOR_PROPS.match(prop) and not prop.endswith("width") \
                    and prop not in _PROP_FAMILY:
                return "color"
            for pattern, family in _LENGTH_FAMILY:
                if pattern.match(prop):
                    return family
            if kind is None:
                return _PROP_FAMILY.get(prop, _NUMBER_FAMILY.get(prop, ""))
            return ""
        if kind == "number":
            return _NUMBER_FAMILY.get(prop, "")
        if kind == "duration":
            return "duration"
        if kind == "cubicBezier":
            return "motion"
        if kind == "fontFamily":
            return "font" if prop == "font-family" else ""
        if kind == "shadow":
            return "shadow" if prop == "box-shadow" else ""
        return ""

    def token_family(self, prop: str, kind: str) -> str:
        """The family of a token of type `kind` used in `prop`."""
        return {"color": "color", "fontFamily": "font", "fontWeight": "weight",
                "shadow": "shadow", "duration": "duration",
                "cubicBezier": "motion"}.get(kind) or self.family_of(prop, kind)

    def var(self, at: Tuple[int, int], prop: str, name: str, text: str, state: str,
            family: str = "") -> None:
        found = self.token(name)
        if found is None:
            self.add(at, prop, family or self.family_of(prop, None), "missing", f"--{name}",
                     text, state)
        else:
            self.add(at, prop, family or self.token_family(prop, found[1]), "token", found[0],
                     text, state)

    def declaration(self, at: Tuple[int, int], prop: str, value: str, state: str) -> None:
        prop = prop.strip()
        if prop == "@apply":
            self.classes(at, value, state, lines=None)
            return
        if not prop.startswith("--"):
            prop = prop.lower()
        value = _IMPORTANT.sub("", value.strip())
        refs = _top_vars(value)
        for name, a, b in refs:
            self.var(at, prop, name, value[a:b], state)
        if prop.startswith(("--", "$", "@")):
            return
        plain = value
        for _, a, b in reversed(refs):
            plain = plain[:a] + " " + plain[b:]
        plain = plain.strip()
        if not plain:
            return
        if prop in ("box-shadow", "font-family"):
            try:
                kind, literal = read_value(plain)
            except NotRead:
                kind = ""
            family = self.family_of(prop, kind)
            if family:
                self.add(at, prop, family, "raw", canonical(kind, literal), plain, state)
                return
            if prop == "font-family":
                return
        if prop == "font-weight" and plain.lower() in _WEIGHT_WORDS:
            self.add(at, prop, "weight", "raw", str(_WEIGHT_WORDS[plain.lower()]), plain, state)
            return
        for chunk in split_top(plain):
            for part in split_top(chunk, " "):
                self.raw(at, prop, part, state)

    def raw(self, at: Tuple[int, int], prop: str, text: str, state: str,
            colors_only: bool = False) -> None:
        try:
            kind, literal = read_value(text)
        except NotRead:
            # A color inside a function the reader does not read (a gradient,
            # drop-shadow()) is still a color written there.
            f = re.match(r"[a-z-]+\((.*)\)$", text, re.I | re.S)
            if f and _COLOR_PROPS.match(prop):
                for chunk in split_top(f.group(1)):
                    for part in split_top(chunk, " "):
                        self.raw(at, prop, part, state, colors_only=True)
            return
        if colors_only and kind != "color":
            return
        family = self.family_of(prop, kind)
        if family:
            self.add(at, prop, family, "raw", canonical(kind, literal), text, state)

    # Stylesheets ---------------------------------------------------------

    def css(self, text: str, first_line: int = 0, pos: int = 0,
            line_comments: bool = False) -> None:
        """A stylesheet; with `line_comments` (SCSS, Less) // starts a comment."""
        if line_comments:
            text = _LINE_COMMENT.sub(lambda m: m.group(1) + " " * len(m.group(2)), text)
        for rule in parse_css(text, self.file, every=True):
            state = _selector_state(rule.selector, rule.media)
            for d in rule.declarations:
                self.declaration((d.line + first_line, pos), d.name, d.value, state)

    # Tailwind ------------------------------------------------------------

    def classes(self, at: Tuple[int, int], text: str, state: str = "",
                lines: Optional[Callable[[int], int]] = None, offset: int = 0) -> None:
        """Each class in `text`. With `lines`, each class takes the line of
        its own offset (offset + its place in text); else all take `at`."""
        for m in re.finditer(r"\S+", text):
            where = (lines(offset + m.start()), offset + m.start()) if lines else at
            self.utility(where, m.group(0), state)

    def utility(self, at: Tuple[int, int], cls: str, outer: str) -> None:
        variants, utility = _variants(cls)
        state = _merge_state(outer, _variant_state(variants))
        utility = utility.strip("!")
        if utility.startswith("[") and utility.endswith("]") and ":" in utility:
            prop, _, value = utility[1:-1].partition(":")
            if re.fullmatch(r"-?-?[a-z][a-z-]*", prop):
                self.declaration(at, prop, value.replace("_", " "), state)
            return
        bare = utility.removeprefix("-")
        for prefix, rest in _prefix_splits(bare):
            for pattern, spaces, kinds in _UTILITIES:
                if pattern.fullmatch(prefix):
                    self.value_class(at, cls, utility, prefix, rest, spaces, kinds, state)
                    return

    def value_class(self, at: Tuple[int, int], cls: str, utility: str, prefix: str,
                    rest: str, spaces: _Namespaces, kinds: Dict[str, str],
                    state: str) -> None:
        if rest.startswith("(") and rest.endswith(")"):
            ref = re.fullmatch(r"\(\s*(?:([a-z-]+):)?--([A-Za-z0-9_-]+)\s*\)", rest)
            if ref:
                self.var(at, utility, ref.group(2), rest, state,
                         family=self._family_for(kinds, ref.group(2), ref.group(1) or ""))
            return
        if rest.startswith("[") and rest.endswith("]"):
            self.arbitrary(at, cls, utility, rest[1:-1].replace("_", " "), kinds, state)
            return
        name = re.sub(r"/(\d+|\[[^\]]*\])$", "", rest)
        if not _REST.fullmatch(name) or not name and not _BARE.fullmatch(prefix):
            return
        for space, family in spaces:
            if not name and family == "color":
                continue
            for candidate in ((f"{space}.{name}", f"{space}.{name}.DEFAULT") if name
                              else (space, f"{space}.DEFAULT")):
                found = self.token(candidate)
                if found is not None:
                    self.add(at, utility, family, "token", found[0], cls, state)
                    return
        if ("spacing", "space") in spaces and _NUMERIC.fullmatch(name) \
                and self.token("spacing"):
            self.add(at, utility, "space", "token", self.token("spacing")[0], cls, state)
            return
        literal = self._bare(prefix, name, spaces)
        if literal is not None:
            kind, value = literal
            self.add(at, utility, kinds.get(kind, ""), "raw", value, cls, state)
            return
        if _KEYWORD_CLASS.fullmatch(utility.lstrip("-")) or (
                _NUMERIC.fullmatch(name) and spaces == _C):
            return
        self.unknown(at, cls)

    @staticmethod
    def _bare(prefix: str, name: str, spaces: _Namespaces) -> Optional[Tuple[str, str]]:
        """A value Tailwind writes as it is, when no token names it: white
        and black, z-10, duration-150, border-2, and a bare border (1px)."""
        if name in ("white", "black") and ("color", "color") in spaces:
            return "color", "#FFFFFF" if name == "white" else "#000000"
        numeric = _NUMERIC.fullmatch(name)
        if prefix == "z" and numeric:
            return "number", f"{float(name):g}"
        if prefix == "duration" and numeric:
            return "duration", f"{float(name):g}ms"
        if prefix.startswith("border") or prefix in ("ring", "outline"):
            if numeric and name.isdigit():
                return "dimension", f"{name}px"
            if not name and prefix.startswith("border"):
                return "dimension", "1px"
        return None

    def _family_for(self, kinds: Dict[str, str], name: str, hint: str = "") -> str:
        """The family of a class that references --name: by its type hint
        (text-[length:var(--x)]), by the token's type when the system has
        it, else the class's one family; Tailwind reads an unhinted var()
        in a class that takes a color as a color."""
        if hint:
            return kinds.get(_HINT_KINDS.get(hint, ""), "")
        found = self.token(name)
        if found is not None and found[1] in kinds:
            return kinds[found[1]]
        families = set(kinds.values())
        if "color" in families:
            return "color"
        return families.pop() if len(families) == 1 else ""

    def arbitrary(self, at: Tuple[int, int], cls: str, utility: str, text: str,
                  kinds: Dict[str, str], state: str) -> None:
        hint = _TYPE_HINT.match(text)
        if hint and not text.startswith("var("):
            text = text[hint.end():]
        refs = _top_vars(text)
        if len(refs) == 1 and refs[0][1] == 0 and refs[0][2] == len(text):
            self.var(at, utility, refs[0][0], text, state,
                     family=self._family_for(kinds, refs[0][0], hint.group(1) if hint else ""))
            return
        try:
            kind, literal = read_value(text)
        except NotRead:
            return
        family = kinds.get(kind, "")
        if family:
            self.add(at, utility, family, "raw", canonical(kind, literal), cls, state)

    # Markup and scripts --------------------------------------------------

    def style_attr(self, lines: _Lines, start: int, text: str) -> None:
        pos = 0
        for decl in split_top(text, ";"):
            at = text.find(decl, pos) if decl else pos
            pos = at + len(decl)
            if ":" in decl:
                prop, _, value = decl.partition(":")
                self.declaration((lines(start + at), start + at), prop, value, "")

    def style_object(self, lines: _Lines, start: int, body: str) -> None:
        for m in _OBJ_ENTRY.finditer(body):
            key = m.group(1) or m.group(2) or m.group(3)
            prop = key if key.startswith("--") else \
                re.sub(r"([A-Z])", lambda c: "-" + c.group(1).lower(), key)
            number = m.group(6)
            if number is not None:
                text = number if key in _UNITLESS or float(number) == 0 else f"{number}px"
            else:
                text = m.group(4) if m.group(4) is not None else m.group(5)
            at = start + m.start()
            self.declaration((lines(at), at), prop, text, "")

    def class_expression(self, lines: _Lines, start: int, body: str) -> None:
        for m in _JS_STRING.finditer(body):
            g = next(i for i in (1, 2, 3) if m.group(i) is not None)
            text = re.sub(r"\$\{[^}]*\}", lambda x: " " * len(x.group(0)), m.group(g))
            self.classes((0, 0), text, lines=lines, offset=start + m.start(g))

    def markup(self, text: str, markup: bool) -> None:
        text = _MARKUP_COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
        lines = _Lines(text)
        if markup:
            for m in _STYLE_BLOCK.finditer(text):
                self.css(m.group(2), lines(m.start(2)) - 1, m.start(2),
                         line_comments=bool(_PREPROCESSED.search(m.group(1))))
            text = _STYLE_BLOCK.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
        for m in _ATTR_START.finditer(text):
            bound, name, i = bool(m.group(1)), m.group(2), m.end()
            if i >= len(text):
                continue
            opener = text[i]
            if opener in "\"'":
                close = text.find(opener, i + 1)
                if close == -1:
                    continue
                body, start = text[i + 1:close], i + 1
                expression = bound or name == "class:list"
            elif opener == "{":
                close = _matching_brace(text, i)
                if close == -1:
                    continue
                body, start, expression = text[i + 1:close], i + 1, True
            else:
                continue
            if name == "style":
                inner = body.strip()
                if expression and inner.startswith("{"):
                    self.style_object(lines, start, body)
                elif not expression:
                    self.style_attr(lines, start, body)
            elif expression:
                self.class_expression(lines, start, body)
            else:
                self.classes((0, 0), body, lines=lines, offset=start)
        for m in _STYLE_DIRECTIVE.finditer(text):
            g = 2 if m.group(2) is not None else 3
            at = m.start()
            self.declaration((lines(at), at), m.group(1), m.group(g), "")


def _matching_brace(text: str, start: int) -> int:
    """The offset of the } closing the { at `start`, skipping strings, or
    -1 when it never closes."""
    depth, quote, i = 0, "", start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            quote = "" if ch == quote else quote
        elif ch in "\"'`":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _files(roots: Sequence[Path], skip: set) -> Iterator[Tuple[Path, Path]]:
    for root in roots:
        if root.is_file():
            if root.resolve() not in skip:
                yield root, root.parent
            continue
        for folder, dirs, names in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
            for name in sorted(names):
                if name.lower().endswith(CSS_EXT + MARKUP_EXT + SCRIPT_EXT):
                    p = Path(folder) / name
                    if not skip or p.resolve() not in skip:
                        yield p, root


def scan(roots: Sequence[Any], ts: TokenSet, exclude: Iterable[Any] = ()) -> Scan:
    """Every use of a value under `roots` (files or folders), matched
    against the tokens of `ts`. Folders in SKIP_DIRS and hidden folders are
    not read; nor is any path in `exclude` (the system's own source file).
    Raises InputError for a root that does not exist."""
    paths = [Path(r).expanduser() for r in roots]
    for p in paths:
        if not p.exists():
            raise InputError(f"{p} does not exist; pass the folder that holds the product's "
                             "code, or one of its files")
    skip = {Path(e).expanduser().resolve() for e in exclude}
    scanner = _Scanner(ts)
    result = scanner.result
    for path, root in _files(paths, skip):
        rel = path.relative_to(root).as_posix()
        name = path.name.lower()
        why = _unread(path, name)
        if why:
            result.skipped.append((rel, why))
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            why = f"cannot be read ({exc.strerror or exc}); check its permissions and scan again"
            result.skipped.append((rel, why))
            continue
        if b"\x00" in data[:8192]:
            result.skipped.append((rel, "is a binary file, not code; nothing to read"))
            continue
        try:
            text = _brief_text(data)
        except UnicodeDecodeError:
            result.skipped.append((rel, "is not UTF-8 text; save it as UTF-8 and scan again"))
            continue
        scanner.begin(rel)
        try:
            if name.endswith(CSS_EXT):
                scanner.css(text, line_comments=not name.endswith(".css"))
            else:
                scanner.markup(text, markup=not name.endswith(SCRIPT_EXT))
        except InputError as exc:
            result.skipped.append((rel, str(exc).replace("import it again", "scan again")))
            continue
        scanner.end()
        result.files += 1
    return result


def _unread(path: Path, name: str) -> str:
    """Why a file is not read, or ""."""
    if not name.endswith(CSS_EXT + MARKUP_EXT + SCRIPT_EXT):
        return ("is not a stylesheet, markup or script file; pass a folder, or a file ending in "
                + ", ".join(CSS_EXT + MARKUP_EXT + SCRIPT_EXT))
    if re.search(r"[.-]min\.(css|js|mjs|cjs)$", name):
        return "is a minified build file; scan its source instead"
    try:
        size = path.stat().st_size
    except OSError as exc:
        return f"cannot be read ({exc.strerror or exc}); check its permissions and scan again"
    if size > MAX_BYTES:
        return (f"is {size:,} bytes, larger than {MAX_BYTES:,}, so it is build output or data; "
                "scan the source it was built from")
    return ""
