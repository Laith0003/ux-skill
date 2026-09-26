"""Import CSS custom properties in their own names.

What is read: custom properties set on the root (`:root`, `html`, `:host`,
and Tailwind's `@theme` block), on a theme selector (`[data-theme="dark"]`,
`.dark`, `[dir="rtl"]`, or several of them joined on the root), and inside
the preference media queries prefers-color-scheme, prefers-contrast and
prefers-reduced-motion. Each property becomes a token whose path is its
name without the leading dashes, so the system keeps its names; a
`var(--x)` value is an alias to x.

Modes: the attributes and media queries this engine writes (data-theme,
data-contrast, data-density, dir, data-motion and the three preference
queries) map to its own axes. A right to left subtree (`[lang|="ar"]`, or
`:root :is([dir="rtl"], [lang|="ar"])` as tokens.css writes it) is the
direction axis too. `:root:not([data-theme="light"])` outside a media query
opens the dark scheme, and Imported.scheme records which scheme a file
opens.

A dark scheme is read wherever stylesheets keep it: `[data-theme="dark"]`,
`.dark`, `[data-mode="dark"]`, any other attribute whose name says it
themes the page (data-theme, data-mode, data-color-scheme, data-scheme,
matched as whole segments) set to dark, and
`@media (prefers-color-scheme: dark)`, with an attribute value quoted
either way or bare. An attribute with another name set to dark
(`[data-sidebar=dark]`) themes a region, so it is the scheme only when
written on :root or html; elsewhere it is not read, and the report says
so. A selector list is the root when each member is the root or a theme
selector at its base value (`:root, [data-x=light]`). The media types
screen and all are dropped from a query: `@media screen and
(prefers-color-scheme: dark)` is the dark scheme, and `@media screen`
alone is read as the base, since it holds wherever the page is on screen.

A property set more than once in one context is read only when every
value reads the same; two spellings of one value (#fff, #FFFFFF) are
noted, and values that differ are all listed under "Not read".
Each property a dark rule sets is paired by name with the one on the root
and read as scheme:dark; a dark rule written in a form this engine does not
write is named under notes with the pairing.

What the write-back gives back: Imported.forms records, for each axis the
file switches in a form this engine does not write, the selector as the
file writes it (`.dark` alone, `:root.dark`, `html.dark`), with the media
query when the file uses that too, or the media query alone (an empty
selector) when the file sets the axis only there; Imported.scheme records
which scheme it opens. export.to_css given both writes each such axis in
exactly those forms and adds no selector of its own for it. A color
mapped into sRGB keeps its spelling in Token.extensions and is written
back in it while the token holds the value it was read as. write_css
does all this and opens the file with a comment that lists every entry
not read, with its fix, and every such color. Not given back: comments,
component rules, the order and grouping of rules, and the file's own
forms for this engine's attributes (data-theme and the rest are written
on :root); color-scheme is added to each scheme rule, and a key that
joins a form with no root to one of this engine's attributes is written
on :root.

Tailwind's dark variant is read where the stylesheet declares it:
`@custom-variant dark (...)` names the selectors its dark: utilities switch
on, and a rule on any of them sets scheme:dark. `@variant dark { ... }`
nested in a rule is read on that selector, or under prefers-color-scheme,
where the variant switches when no custom variant is declared. A custom
variant with no property set under it is noted: its dark values live in
markup.

Any other theme selector becomes an axis of its own, named after it
(`.compact` is the axis class-compact, off and on; `[data-brand="alt"]` is
data-brand, base and alt), and Imported.forms records the selector. Mapping
such an axis to one of ours is the naming adapter's job.

The viewport is not a mode. A root property whose value is a var()
reference and that a min-width media query sets again is a switch between
other properties: it is named under notes and not made a token, since each
value it switches between is read where it is defined. A size written as
calc(var(--a) * var(--scale)), where such a switch sets --scale to plain
numbers, reads as var(--a) with a note: its value from the first
breakpoint up when --scale is 1 there, otherwise its unscaled value.

An oklch() or oklab() color outside sRGB is mapped into sRGB by CSS Color 4
gamut mapping and listed under "Mapped into sRGB", never refused.

Nested rules (CSS Nesting) are rules of their own, read to any depth:
`&` stands for the parent, any other selector is a descendant of it, and
a nested @media adds to the parent's media. A nested rule never folds
into its parent, so a component nested in :root is a component.

What is not read, each with the fix: properties set on components or under
other media queries, a property set only under a mode, values with no
single reading (values_in), references to a property the file does not
define, and a selector list naming more than one mode.
"""
from __future__ import annotations

import re
from bisect import bisect_right
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from engine.foundations.errors import InputError
from engine.foundations.export import to_css
from engine.foundations.modes import AXES, CSS_AXES, join
from engine.foundations.tokens import Token, TokenSet
from engine.io.report import Imported, ImportReport, Item, Mapped, Source, read_source
from engine.io.values_in import GamutMapped, NotRead, css_alias, read_value, split_top

# The scheme a stylesheet opens (export.SCHEME_DEFAULTS): it follows the
# system when prefers-color-scheme sets the dark values, opens dark when
# :not([data-theme="light"]) sets them outside a media query, and opens
# light when only a dark selector ([data-theme="dark"], .dark) does.
SYSTEM, LIGHT, DARK = "system", "light", "dark"

# Root selectors: a property set here is the base value.
ROOTS = (":root", "html", ":host", "@theme")
# Media features this engine writes, and the axis value each one sets.
MEDIA_AXES: Dict[str, Tuple[str, str]] = {
    "(prefers-color-scheme: dark)": ("scheme", "dark"),
    "(prefers-contrast: more)": ("contrast", "high"),
    "(prefers-reduced-motion: reduce)": ("motion", "reduced"),
}
# Selectors this engine does not write that stylesheets switch the scheme
# with, and the scheme each one sets. Any other attribute set to dark or
# light ([data-mode=dark], [data-color-scheme="dark"]) sets it too.
SCHEME_SELECTORS: Dict[str, str] = {
    ".dark": "dark",
    ".light": "light",
    '[data-mode="dark"]': "dark",
    '[data-mode="light"]': "light",
}
_ATTR_AXES = {attr: axis for axis, (attr, _) in CSS_AXES.items()}
# An attribute value in double quotes, in single quotes or bare.
_VALUE = r"""=(?:"([^"]*)"|'([^']*)'|([A-Za-z0-9_-]+))"""
_ATTR = re.compile(r"\[([a-z][a-z0-9-]*)" + _VALUE + r"\]")
_NOT = re.compile(r":not\(\[([a-z][a-z0-9-]*)" + _VALUE + r"\]\)")
# An attribute whose name says it themes the page (data-theme, data-mode,
# data-color-scheme, data-scheme, or one of them after a page-wide word such
# as data-app-theme): set to dark or light anywhere, it is the scheme. The
# word is matched as whole segments, so a region's theme (data-code-theme)
# or another word (data-model) is not. Another attribute set to dark
# (data-sidebar) is the scheme only on the root.
THEME_ATTR = re.compile(r"(?:data-)?(?:(?:app|page|site|ui|bs)-)?(?:color-)?"
                        r"(?:theme|mode|scheme)")
# A selector that names a scheme in a form the importer does not read.
_SCHEMEISH = re.compile(r"""\.(?:dark|light)\b|=\s*["']?(?:dark|light)\b""")
# Media types that leave a preference query meaning what it says on screen.
_MEDIA_TYPES = ("screen", "all", "only screen", "only all")
_CLASS = re.compile(r"\.([a-z][a-z0-9-]*)")
# Tailwind's dark variant: `@custom-variant dark (...)` or its block form,
# and the query its dark: utilities follow when a file declares none.
_CUSTOM_DARK = re.compile(r"@custom-variant\s+dark\s*([({])")
_THEME_TOKEN = re.compile(r"\.[a-z][a-z0-9-]*|\[[a-z][a-z0-9-]*" + _VALUE + r"\]")
DARK_MEDIA = CSS_AXES["scheme"][1]
# An Arabic language selector: right to left, the direction axis at rtl.
_LANG = re.compile(r'\[lang\|="ar"\]')
# Subtrees inside the root that read right to left.
RTL_SUBTREES = ('[dir="rtl"]', '[lang|="ar"]', ':is([dir="rtl"], [lang|="ar"])',
                ':is([lang|="ar"], [dir="rtl"])')
# A viewport query: a width from which a value holds.
_MIN_WIDTH = re.compile(r"\(min-width: ?([0-9.]+(?:px|rem|em))\)")
# Any width query, for the message a value under one gets.
_WIDTH = re.compile(r"\((?:min|max)-width\s*:")
# A size that a viewport switch scales.
_SCALED = re.compile(r"calc\(\s*var\(--([A-Za-z0-9_-]+)\)\s*\*\s*var\(--([A-Za-z0-9_-]+)\)\s*\)")


@dataclass(frozen=True)
class Declaration:
    name: str
    value: str
    line: int


@dataclass(frozen=True)
class Rule:
    """One style rule: its selector text, the media queries around it
    (outermost first) and its custom property declarations."""
    selector: str
    media: Tuple[str, ...]
    declarations: Tuple[Declaration, ...]
    line: int
    # How the file writes a rule the importer moved (one under @variant dark).
    label: str = ""


def _blank_comments(text: str) -> str:
    """Comments replaced by spaces, newlines kept, so offsets and lines hold."""
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _matching(text: str, start: int, name: str) -> int:
    """The offset of the } closing the { at `start`."""
    depth, quote = 0, ""
    for i in range(start, len(text)):
        ch = text[i]
        if quote:
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    raise InputError(f"{name} has a block opened on line {_line(text, start)} that never "
                     "closes; add the missing } and import it again")


def _body(text: str, start: int, end: int, name: str, every: bool = False,
          line: Optional[Callable[[int], int]] = None
          ) -> Tuple[Tuple[Declaration, ...], List[Tuple[str, int, int]]]:
    """The custom property declarations between `start` and `end` (with
    `every`, every declaration, and each @apply as a declaration named
    @apply), and the blocks nested there as (prelude, offset of their {,
    offset of their }). A nested block is cut out, so it never swallows the
    declaration after it; a custom property whose value holds braces keeps
    them. `line` gives an offset's line (parse_css passes an index, so a
    long stylesheet is not counted from its start for every declaration)."""
    out: List[Declaration] = []
    nested: List[Tuple[str, int, int]] = []
    if line is None:
        def line(at: int) -> int:
            return _line(text, at)

    def declaration(a: int, b: int) -> None:
        part = text[a:b]
        stripped = part.strip()
        at = a + len(part) - len(part.lstrip())
        if every and stripped.startswith("@apply"):
            out.append(Declaration("@apply", stripped[len("@apply"):].strip(), line(at)))
        elif (every or stripped.startswith("--")) and ":" in stripped:
            prop, _, value = stripped.partition(":")
            out.append(Declaration(prop.strip(), value.strip(), line(at)))

    i = seg = start
    depth, quote = 0, ""
    while i < end:
        ch = text[i]
        if quote:
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and ch == ";":
            declaration(seg, i)
            seg = i + 1
        elif depth == 0 and ch == "{":
            close = _matching(text, i, name)
            if not text[seg:i].strip().startswith("--"):
                nested.append((" ".join(text[seg:i].split()), i, close))
                seg = close + 1
            i = close + 1
            continue
        i += 1
    declaration(seg, end)
    return tuple(out), nested


def _nest(parent: str, child: str) -> str:
    """A nested rule's selector: `&` stands for the parent, and a selector
    without `&` is a descendant of it (CSS Nesting)."""
    parents = [":root" if p == "@theme" else p for p in split_top(parent, ",")]
    return ", ".join(c.replace("&", p) if "&" in c else f"{p} {c}"
                     for p in parents for c in split_top(child, ","))


def parse_css(text: str, name: str = "the stylesheet", every: bool = False) -> List[Rule]:
    """Every style rule in `text`, with the media queries around it.
    @layer and @theme blocks are read through; other at-rules are kept as
    media so the importer can name them. A rule nested in a rule is a rule
    of its own, read to any depth: its selector joins the parent's (`&` is
    the parent, anything else a descendant), and a nested @media or other
    at-rule adds to the parent's media. A rule keeps its custom property
    declarations, or with `every` all its declarations, as the codebase
    scanner reads them."""
    text = _blank_comments(text)
    rules: List[Rule] = []
    starts = [0] + [m.end() for m in re.finditer("\n", text)]

    def line(at: int) -> int:
        return bisect_right(starts, at)

    def rule(selector: str, media: Tuple[str, ...], brace: int, close: int) -> None:
        declarations, nested = _body(text, brace + 1, close, name, every, line)
        rules.append(Rule(selector, media, declarations, line(brace)))
        for prelude, start, end in nested:
            if prelude.startswith("@media"):
                rule(selector, media + (prelude[len("@media"):].strip(),), start, end)
            elif prelude.startswith("@layer"):
                rule(selector, media, start, end)
            elif prelude.startswith("@"):
                rule(selector, media + (prelude,), start, end)
            else:
                rule(_nest(selector, prelude), media, start, end)

    def block(start: int, end: int, media: Tuple[str, ...]) -> None:
        i = start
        while i < end:
            brace = text.find("{", i, end)
            semi = text.find(";", i, end)
            if brace == -1:
                return
            if semi != -1 and semi < brace:  # a statement such as @import
                i = semi + 1
                continue
            prelude = " ".join(text[i:brace].split())
            close = _matching(text, brace, name)
            if prelude.startswith("@media"):
                block(brace + 1, close, media + (prelude[len("@media"):].strip(),))
            elif prelude.startswith("@layer"):
                block(brace + 1, close, media)
            elif prelude.startswith("@theme"):
                rule("@theme", media, brace, close)
            elif prelude.startswith("@"):
                block(brace + 1, close, media + (prelude,))
            else:
                rule(prelude, media, brace, close)
            i = close + 1

    block(0, len(text), ())
    return rules


class _Modes:
    """Turns selectors and media into contexts. The attributes and media
    this engine writes map to its axes, and so do the dark selectors in
    SCHEME_SELECTORS; any other theme selector becomes an axis of its own
    when it is registered."""

    def __init__(self) -> None:
        self.custom: Dict[str, Tuple[str, str]] = {}
        self.forms: Dict[str, Tuple[str, str]] = {}
        self.ours: List[str] = []
        # Axes set outside a media query by :not([attr="base"]).
        self.unpinned: List[str] = []
        # Axes set by a preference media query.
        self.by_media: List[str] = []
        # Axes set outside a media query by an attribute this engine writes.
        self.attributed: List[str] = []
        # The last value refused for an imported axis: (axis, its value, refused).
        self.refused: Optional[Tuple[str, str, str]] = None

    @staticmethod
    def parse(sel: str, dark: Tuple[str, ...] = ()) -> Optional[List[Tuple[str, str, str]]]:
        """(axis, value, form) for each part of one selector: form "" for
        an attribute this engine writes, ":not" for one set by
        :not([attr="base"]), and the selector text for any other, with the
        root it is written on when there is one (`.dark` alone, `:root.dark`
        or `html.dark`), so it is written back as the file has it; None when
        it is not a root or theme selector."""
        rest, rooted, prefix = sel, False, ""
        for root in ROOTS:
            if rest.startswith(root):
                rest, rooted = rest[len(root):], root != "@theme"
                prefix = root if rooted else ""
                break
        parts: List[Tuple[str, str, str]] = []
        while rest:
            if rest[0].isspace():
                if rest.strip() not in RTL_SUBTREES:
                    return None
                parts.append(("direction", "rtl", ""))
                break
            m = _NOT.match(rest) or _LANG.match(rest) or _ATTR.match(rest) or _CLASS.match(rest)
            if not m:
                return None
            token = m.group(0)
            own = prefix + token
            if m.re is _CLASS:
                parts.append(("scheme", SCHEME_SELECTORS.get(token, "dark"), own)
                             if token in SCHEME_SELECTORS or token in dark
                             else (f"class-{m.group(1)}", "on", own))
            elif m.re is _LANG:
                parts.append(("direction", "rtl", ""))
            else:
                attr = m.group(1)
                value = next(g for g in m.groups()[1:] if g is not None)
                axis = _ATTR_AXES.get(attr)
                if m.re is _NOT:
                    if axis is None or len(AXES[axis]) != 2 or value != AXES[axis][0]:
                        return None
                    parts.append((axis, AXES[axis][1], ":not"))
                elif f'[{attr}="{value}"]' in dark:
                    parts.append(("scheme", "dark", own))
                elif axis is not None and value in AXES[axis]:
                    parts.append((axis, value, ""))
                elif value in AXES["scheme"]:
                    if not (rooted or THEME_ATTR.fullmatch(attr)):
                        return None
                    parts.append(("scheme", value, own))
                else:
                    parts.append((attr, value, own))
            rest = rest[len(token):]
        return parts

    def register(self, parts: List[Tuple[str, str, str]],
                 media: Dict[str, str]) -> Optional[Dict[str, str]]:
        """The non-base pairs the parts set, registering new axes; None when
        an attribute axis meets a second value (split it into its own
        selector). :not([attr="base"]) inside the media query of its own
        axis is the media form and adds nothing; outside one it sets the
        other value. A dark selector this engine does not write sets the
        scheme and is kept in forms, the first one met."""
        pairs: Dict[str, str] = {}
        for axis, value, form in parts:
            if axis in AXES:
                if axis not in self.ours:
                    self.ours.append(axis)
                if form == ":not":
                    if axis in media:
                        continue
                    if axis not in self.unpinned:
                        self.unpinned.append(axis)
                elif form == "" and value != AXES[axis][0] and axis not in self.attributed:
                    self.attributed.append(axis)
                if value != AXES[axis][0]:
                    pairs[axis] = value
                    if form not in ("", ":not"):
                        self.forms.setdefault(axis, (form, ""))
                continue
            if axis not in self.custom:
                self.custom[axis] = ("off", "on") if axis.startswith("class-") \
                    else ("base", value)
                self.forms[axis] = (form, "")
            if self.custom[axis][1] != value:
                self.refused = (axis, self.custom[axis][1], value)
                return None
            pairs[axis] = value
        return pairs

    @staticmethod
    def media(media: Tuple[str, ...]) -> Optional[Dict[str, str]]:
        """The pairs the preference media queries around a rule set, or None
        when one of them is a query this engine does not read."""
        pairs: Dict[str, str] = {}
        for query in media:
            for part in (p.strip() for p in query.split(" and ")):
                part = re.sub(r"\s*:\s*", ": ", part)
                if part.lower() in _MEDIA_TYPES:
                    continue
                if part not in MEDIA_AXES:
                    return None
                axis, value = MEDIA_AXES[part]
                pairs[axis] = value
        return pairs

    def register_media(self, pairs: Dict[str, str]) -> None:
        """Registers the axes a rule read under media queries sets."""
        for axis in pairs:
            if axis not in self.ours:
                self.ours.append(axis)
            if axis not in self.by_media:
                self.by_media.append(axis)

    def axes(self) -> Dict[str, Tuple[str, str]]:
        ours = {a: AXES[a] for a in AXES if a in self.ours}
        return {**ours, **self.custom}

    def scheme(self) -> str:
        """The scheme the stylesheet opens."""
        if "scheme" not in self.ours or "scheme" in self.by_media:
            return SYSTEM
        return DARK if "scheme" in self.unpinned else LIGHT

    def finish(self) -> None:
        """A scheme kept in a selector of the file's own that the file also
        sets under prefers-color-scheme is written back in both forms. An
        axis the file sets only under its preference media query is
        recorded with no selector, so it is written back under the query
        alone."""
        if "scheme" in self.forms and "scheme" in self.by_media:
            self.forms["scheme"] = (self.forms["scheme"][0], CSS_AXES["scheme"][1])
        for axis in self.by_media:
            if axis not in self.forms and axis not in self.attributed \
                    and axis not in self.unpinned:
                self.forms[axis] = ("", CSS_AXES[axis][1])


def dark_variant(text: str) -> Optional[Tuple[str, int, str, Tuple[str, ...]]]:
    """(where Tailwind's dark variant switches, line, the variant as
    written, every selector it switches on) from a `@custom-variant dark`
    declaration: for each comma member of each :where() or :is() group,
    the class or attribute that names dark, else the one that opens the
    member, never what a :not() names (an attribute as `[attr="value"]`;
    see _scheme_token), each once and the first as where, or the
    prefers-color-scheme query. Where
    is "" when the variant names no such selector (`&:where(:not(.light),
    ...)` names only what dark is not). None when the file declares no dark
    variant."""
    text = _blank_comments(text)
    m = _CUSTOM_DARK.search(text)
    if not m:
        return None
    start = m.start(1)
    end = text.find(";", start) if m.group(1) == "(" else _matching(text, start, "the file")
    body = text[start + 1:end if end != -1 else len(text)].strip()
    if m.group(1) == "(" and body.endswith(")"):
        body = body[:-1]
    # The block form is named by the selector before its own block.
    shown = body.split("{", 1)[0] if m.group(1) == "{" else body
    line, written = _line(text, m.start()), " ".join(shown.split())
    if "prefers-color-scheme" in body:
        return DARK_MEDIA, line, written, (DARK_MEDIA,)
    selectors: List[str] = []
    for member in _variant_members(body):
        found = _scheme_token(member)
        if found is None:
            continue
        attr = _ATTR.fullmatch(found)
        value = next((g for g in attr.groups()[1:] if g is not None), "") if attr else ""
        selector = f'[{attr.group(1)}="{value}"]' if attr else found
        if selector not in selectors:
            selectors.append(selector)
    if not selectors:
        return "", line, written, ()
    return selectors[0], line, written, tuple(selectors)


_GROUP = re.compile(r":(where|is|not)\(")


def _variant_members(body: str) -> List[str]:
    """The comma members of a dark variant's selector: those inside each of
    its top-level :where() and :is() groups (never inside a :not()), or a
    top-level member itself when it has no such group."""
    out: List[str] = []
    for outer in split_top(body, ","):
        groups, i = [], 0
        while True:
            m = _GROUP.search(outer, i)
            if not m:
                break
            depth, end = 0, len(outer)
            for j in range(m.end() - 1, len(outer)):
                depth += {"(": 1, ")": -1}.get(outer[j], 0)
                if depth == 0:
                    end = j
                    break
            if m.group(1) != "not":
                groups.append(outer[m.end():end])
            i = end + 1
        out += [p for g in groups for p in split_top(g, ",")] if groups else [outer]
    return [p.strip() for p in out if p.strip()]


def _names_dark(token: str) -> bool:
    """True for a class with dark as a word of its name (.dark, .theme-dark)
    or a theme attribute set to dark ([data-theme=dark])."""
    attr = _ATTR.fullmatch(token)
    if attr:
        value = next(g for g in attr.groups()[1:] if g is not None)
        return value.lower() == "dark" and bool(THEME_ATTR.fullmatch(attr.group(1)))
    return "dark" in token.lstrip(".").lower().split("-")


def _scheme_token(member: str) -> Optional[str]:
    """Where one member of a dark variant switches: the class or attribute
    in its chain that names dark (.dark in `.theme .dark .card`,
    [data-theme=dark] in `.content[data-theme=dark]`), else the first one
    of the compound that opens it; what a :not() names is never taken, so
    `:not(.light) .content` gives None. In `.dark .app`, .app is an element
    inside dark, not the scheme."""
    chain = [c for c in split_top(re.sub(r"\s*[>+~]\s*", " ", member), " ")
             if c.strip() not in ("", "&", "*")]
    compounds = [[t.group(0) for t in _THEME_TOKEN.finditer(_without_not(c))] for c in chain]
    named = next((t for tokens in compounds for t in tokens if _names_dark(t)), None)
    if named is not None:
        return named
    return compounds[0][0] if compounds and compounds[0] else None


def _without_not(text: str) -> str:
    """`text` with every :not(...) group cut out, its parentheses matched
    at any depth (`:not(:is(.light, .light *))`): what a :not() names is
    where dark is not."""
    while True:
        at = text.find(":not(")
        if at == -1:
            return text
        depth, i = 0, at + len(":not")
        for i in range(at + len(":not"), len(text)):
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            if depth == 0:
                break
        text = text[:at] + text[i + 1:]


def _on_dark_variant(rule: Rule, dark_at: str, every: Tuple[str, ...] = ()) -> Rule:
    """A rule nested under `@variant dark`, moved to where the variant
    switches: the prefers-color-scheme query, or each selector it names
    (`every`, else `dark_at`) joined onto the rule's own."""
    if "@variant dark" not in rule.media:
        return rule
    media = tuple(m for m in rule.media if m != "@variant dark")
    label = " ".join([*(f"@media {m}" for m in media), rule.selector, "@variant dark"])
    if not dark_at:  # the variant names no dark selector: left for the importer to name
        return Rule(rule.selector, rule.media, rule.declarations, rule.line, label)
    if dark_at.startswith("("):
        return Rule(rule.selector, media + (dark_at,), rule.declarations, rule.line, label)
    selector = ", ".join((":root" if s == "@theme" else s) + d
                         for s in split_top(rule.selector, ",") for d in every or (dark_at,))
    return Rule(selector, media, rule.declarations, rule.line, label)


def _ours(sel: str, parts: List[Tuple[str, str, str]]) -> bool:
    """True when a selector that sets the scheme is one this engine writes:
    :root with data-theme, or with :not([data-theme="light"])."""
    return sel.startswith(":root") and any(
        axis == "scheme" and form in ("", ":not") for axis, _, form in parts)


def _base(selector: str) -> bool:
    """True when every selector in the list is the root, or a theme selector
    at its base value (`:root, :host`, `:root, [data-x=light]`)."""
    for one in split_top(selector, ","):
        parts = _Modes.parse(one)
        if parts is None or any(a not in AXES or v != AXES[a][0] for a, v, _ in parts):
            return False
    return True


def _reading(text: str) -> Any:
    """What a value text reads as, for telling two spellings of one value
    from two values; None when it has no single reading."""
    try:
        alias = css_alias(text)
        return ("alias", alias[0]) if alias else read_value(text)
    except NotRead:
        return None


def _clashes(prop: str, by_key: Dict[Tuple[Tuple[str, str], ...], List[Tuple[str, int]]],
             axes: Dict[str, Tuple[str, str]], name: str
             ) -> Tuple[List[Tuple[int, Item]], List[Tuple[int, Item]]]:
    """For a property set more than once in one context: a Not read item
    per context whose values read differently, naming every value, and a
    note per context whose values are spellings of one value."""
    clashed: List[Tuple[int, Item]] = []
    spelled: List[Tuple[int, Item]] = []
    for key, entries in by_key.items():
        distinct: List[Tuple[str, int]] = []
        for value, line in entries:
            if all(" ".join(value.split()) != " ".join(v.split()) for v, _ in distinct):
                distinct.append((value, line))
        if len(distinct) < 2:
            continue
        where = join(dict(key), axes) or "the base mode"
        last = distinct[-1][1]
        listed = [f"{v} on line {n}" for v, n in distinct]
        text = (" and ".join(listed) if len(listed) == 2
                else ", ".join(listed[:-1]) + " and " + listed[-1])
        readings = [_reading(v) for v, _ in distinct]
        if None in readings or any(r != readings[0] for r in readings):
            both = "both" if len(listed) == 2 else "all"
            clashed.append((last, Item(f"{name}:{last}", prop, (
                f"is {text}, {both} in {where}; keep one, or make them agree"))))
        else:
            spelled.append((last, Item(f"{name}:{last}", prop, (
                f"is {text}, both in {where}: two spellings of one value, read as one"
                if len(listed) == 2 else
                f"is {text}, all in {where}: spellings of one value, read as one"))))
    return clashed, spelled


def _viewport(rules: List[Rule]) -> Dict[str, List[Tuple[str, str, int]]]:
    """Root properties a min-width media query sets: name -> [(width, value,
    line)], the root value first with width ""."""
    root: Dict[str, Tuple[str, int]] = {}
    tiers: Dict[str, List[Tuple[str, str, int]]] = {}
    for rule in rules:
        if not _base(rule.selector):
            continue
        widths = [_MIN_WIDTH.fullmatch(m.strip()) for m in rule.media]
        if not rule.media:
            for d in rule.declarations:
                root.setdefault(d.name, (d.value, d.line))
        elif len(widths) == 1 and widths[0]:
            for d in rule.declarations:
                tiers.setdefault(d.name, []).append((widths[0].group(1), d.value, d.line))
    return {name: [("", *root[name])] + tiers[name] for name in tiers
            if name in root and _aliases(root[name][0])}


def _aliases(text: str) -> bool:
    """True when `text` is one var() reference."""
    try:
        return css_alias(text) is not None
    except NotRead:
        return False


def _number(text: str, root: Dict[str, str]) -> Optional[str]:
    """The plain number `text` comes to, following var() references through
    the root's properties, or None when it is not one."""
    seen: List[str] = []
    while True:
        try:
            alias = css_alias(text)
        except NotRead:
            return None
        if alias is None:
            break
        if alias[0] in seen or f"--{alias[0]}" not in root:
            return None
        seen.append(alias[0])
        text = root[f"--{alias[0]}"]
    try:
        kind, _ = read_value(text)
    except NotRead:
        return None
    return text.strip() if kind == "number" else None


def _switch_text(values: List[Tuple[str, str, int]]) -> str:
    first, *rest = values
    return ", then ".join([first[1]] + [f"{v} from {w}" for w, v, _ in rest])


def _scaled_note(text: str, size: str, factor: str, steps: List[Tuple[str, str]]) -> str:
    """The note on a size that a viewport scale multiplies: read as its
    value from the first breakpoint up when the scale is 1 there, else as
    its unscaled value."""
    width = steps[1][0]
    if all(float(v) == 1 for _, v in steps[1:]):
        return (f"is {text}, and {factor} is 1 from {width} up, so it was read as "
                f"var(--{size}), its value from {width} up; below {width} {factor} scales it")
    scale = ", then ".join([steps[0][1]] + [f"{v} from {w}" for w, v in steps[1:]])
    return (f"is {text}, and {factor} scales it with the viewport ({scale}), so it was read "
            f"as var(--{size}), its unscaled value; the viewport is not a mode, so the scale "
            "is not a token")


_COMPONENT = ("is set on {sel}, not on the root or a theme selector; a property set on a "
              "component is not a system token; move it to :root if it is one")
_UNREAD_SCHEME = ("is set on {sel}, a scheme selector in a form this importer does not read; "
                  'write the dark values under .dark, [data-theme="dark"] or @media '
                  "(prefers-color-scheme: dark) on :root")


def _outside_message(selector: str, options: List[Any], shown: str = "") -> str:
    """Why a rule outside the root and theme selectors is not read: a scheme
    selector in a form not read, or a component. `shown` is the rule as the
    file writes it, when the importer moved it."""
    for one, parts in zip(split_top(selector, ","), options):
        for m in _ATTR.finditer(one) if parts is None else ():
            attr, value = m.group(1), next(g for g in m.groups()[1:] if g is not None)
            if value in AXES["scheme"] and attr not in _ATTR_AXES \
                    and not THEME_ATTR.fullmatch(attr):
                return (f"is set on {selector}, which sets {value} on {attr}, a name that does "
                        "not say it themes the page; write it on :root or html to make it the "
                        "page scheme, or keep it in the component it themes")
        bare = re.sub(r"\([^()]*\)", "()", one)
        if parts is None and _SCHEMEISH.search(one) and (
                " " not in bare.strip() or bare.strip().endswith(" *")):
            return _UNREAD_SCHEME.format(sel=shown or selector)
    return _COMPONENT.format(sel=shown or selector)


def _media_message(media: Tuple[str, ...]) -> str:
    queries = " and ".join(m if m.startswith("@") else f"@media {m}" for m in media)
    if any(re.search(r"prefers-color-scheme\s*:\s*light", m) for m in media):
        return (f"is set under {queries}; light is the base scheme, so its values belong on "
                ":root")
    reads = ("which is not a mode the engine reads; it reads prefers-color-scheme, "
             "prefers-contrast and prefers-reduced-motion")
    if all(_WIDTH.search(m) and not m.startswith("@") for m in media):
        return (f"is set under {queries}, {reads}, so keep viewport values in the layout "
                "breakpoints")
    return f"is set under {queries}, {reads}, so set it on the root or under one of those"


def import_css(text: str, source: Source) -> Imported:
    """The custom properties a stylesheet sets, as tokens in their own
    names, and the report. A class or attribute selector this engine does
    not write, other than a dark selector, counts as a theme selector only
    when every property it sets is also set on the root: it switches
    existing tokens, as a mode does."""
    name = Path(source.path).name
    variant = dark_variant(text)
    dark_at = variant[0] if variant else DARK_MEDIA
    every = variant[3] if variant and dark_at and not dark_at.startswith("(") else ()
    # The dark variant's selectors this engine does not already read as dark.
    variant_on = tuple(d for d in every
                       if [(a, v) for a, v, _ in _Modes.parse(d) or []] != [("scheme", "dark")])
    rules = [_on_dark_variant(r, dark_at, every) for r in parse_css(text, source.path)]
    modes = _Modes()
    switches = _viewport(rules)
    root_values: Dict[str, str] = {}
    for r in rules:
        if not r.media and _base(r.selector):
            for d in r.declarations:
                root_values.setdefault(d.name, d.value)
    # Switches between plain numbers: a scale factor, name -> [(width, number)].
    factors: Dict[str, List[Tuple[str, str]]] = {}
    for prop, steps in switches.items():
        numbers = [_number(v, root_values) for _, v, _ in steps]
        if len(steps) > 1 and all(n is not None for n in numbers):
            factors[prop] = [(w, n) for (w, _, _), n in zip(steps, numbers)]
    root_names = set(root_values)
    # property -> {sorted non-base pairs: (value text, line)}, in the order read
    found: Dict[str, Dict[Tuple[Tuple[str, str], ...], Tuple[str, int]]] = {}
    not_read: List[Tuple[int, Item]] = []
    notes: List[Tuple[int, Item]] = []
    # Dark rules in a form this engine does not write: (line, label, properties).
    paired: List[Tuple[int, str, List[str]]] = []
    # property -> context -> every (value, line) set there, in the order read.
    seen: Dict[str, Dict[Tuple[Tuple[str, str], ...], List[Tuple[str, int]]]] = {}
    entries = 0
    for rule in rules:
        if not rule.declarations:  # a rule with no custom property sets no mode
            continue
        media = modes.media(rule.media)
        options = [_Modes.parse(s, variant_on) for s in split_top(rule.selector, ",")]
        custom = any(axis not in AXES for o in options if o for axis, _, _ in o)
        outside = any(o is None for o in options)
        component = outside or (
            custom and not all(d.name in root_names for d in rule.declarations))
        keys = set()
        modes.refused = None
        if media is not None and not component:
            modes.register_media(media)
            for o in options:
                pairs = modes.register(o, media)
                keys.add(None if pairs is None else tuple(sorted({**media, **pairs}.items())))
        dark = [p for p in rule.declarations if p.name not in switches] if (
            len(keys) == 1 and None not in keys and ("scheme", "dark") in next(iter(keys))
            and not all(_ours(s, o) for s, o in zip(split_top(rule.selector, ","), options)
                        if o is not None)) else []
        if dark:
            label = rule.label or " ".join([*(f"@media {m}" for m in rule.media),
                                            rule.selector])
            form = next((f for o in options if o for a, _, f in o
                         if a == "scheme" and f not in ("", ":not")),
                        "@media" if "scheme" in (media or {}) else "")
            paired.append((rule.line, label, [d.name for d in dark], form))
        for d in rule.declarations:
            entries += 1
            if d.name in switches:
                continue
            if d.name.endswith("*"):
                notes.append((d.line, Item(f"{name}:{d.line}", d.name, "clears Tailwind's default "
                              f"values in the {d.name} namespace; the system holds only what "
                              "this file sets")))
                continue
            item = None
            shown = rule.label or rule.selector
            if outside:
                item = _outside_message(rule.selector, options, rule.label)
            elif component:
                item = _COMPONENT.format(sel=shown)
            elif "@variant dark" in rule.media:  # the custom variant names no dark selector
                item = (f"is set under {shown}, and @custom-variant dark, declared as "
                        f"{variant[2]}, names no dark selector, only what dark is not; name one "
                        "in it, such as "
                        "&:where(.dark, .dark *) or &:where([data-theme=dark], "
                        "[data-theme=dark] *), and set the dark values under that selector")
            elif media is None:
                item = _media_message(rule.media)
            elif modes.refused:
                axis, held, value = modes.refused
                item = (f"is set under {shown}, but [{axis}] already switches to "
                        f"{held}; an imported axis has one value besides its base, so give "
                        f"{value} an attribute of its own")
            elif len(keys) > 1 or None in keys:
                item = (f"is set under {shown}, which names more than one mode; split "
                        "it into one rule per mode")
            if item:
                not_read.append((d.line, Item(f"{name}:{d.line}", d.name, item)))
                continue
            key = next(iter(keys))
            found.setdefault(d.name, {}).setdefault(key, (d.value, d.line))
            seen.setdefault(d.name, {}).setdefault(key, []).append((d.value, d.line))
    modes.finish()

    for prop, values in switches.items():
        at = values[0][2]
        notes.append((at, Item(f"{name}:{at}", prop, f"switches with the viewport "
                                                     f"({_switch_text(values)}); the viewport is "
                                                     "not a mode, so it was not made a token, and "
                                                     "each property it points at is read as its "
                                                     "own token")))
    axes = modes.axes()
    if variant and not dark_at:
        notes.append((variant[1], Item(f"{name}:{variant[1]}", "@custom-variant dark", (
            f"is declared as {variant[2]}, which names no dark selector, only what dark is "
            "not, so no value is read as the dark scheme through it; name one, such as "
            "&:where(.dark, .dark *), and set the dark values under that selector"))))
    elif variant and "scheme" not in axes:
        where = f"@media {dark_at}" if dark_at.startswith("(") else ", ".join(every)
        notes.append((variant[1], Item(f"{name}:{variant[1]}", "@custom-variant dark", (
            f"puts Tailwind's dark: variant on {where}, and this file sets no custom property "
            "there, so it holds no dark scheme; dark: utilities in markup are not theme values. "
            f"Set the dark values under {where} to read them"))))
    # path -> [(context key, kind or "alias", value, line)] in the order read
    values: Dict[str, List[Tuple[str, str, Any, int]]] = {}
    mapped: List[Tuple[int, Mapped]] = []
    # path -> context -> a color outside sRGB as the file writes it
    originals: Dict[str, Dict[str, str]] = {}
    for prop, by_key in found.items():
        path = prop[2:]
        line = min(line for _, line in by_key.values())
        if () not in by_key:
            under = ", ".join(sorted({modes.forms.get(a, (f"{a}:{v}", ""))[0]
                                      for key in by_key for a, v in key}))
            not_read.append((line, Item(f"{name}:{line}", prop, f"is set only under {under}; "
                             "give it a value on :root too, so the base mode has one, or import "
                             "it together with the file that sets its base value")))
            continue
        clashed, own_notes = _clashes(prop, seen[prop], axes, name)
        if clashed:
            not_read += clashed
            continue
        read: List[Tuple[str, str, Any, int]] = []
        own_mapped: List[Tuple[int, Mapped]] = []
        own_original: Dict[str, str] = {}
        # One note on the scaled value per property, beside any spelling note.
        scaled_noted = False
        try:
            for key, (value_text, at) in by_key.items():
                if re.search(r"!\s*important\s*$", value_text, re.I):
                    raise NotRead("is marked !important; drop !important, since a token holds "
                                  "only the value")
                scaled = _SCALED.fullmatch(value_text.strip())
                if scaled and f"--{scaled.group(2)}" in factors:
                    size, factor = scaled.group(1), f"--{scaled.group(2)}"
                    if not scaled_noted:
                        scaled_noted = True
                        own_notes.append((at, Item(f"{name}:{at}", prop, _scaled_note(
                            value_text.strip(), size, factor, factors[factor]))))
                    value_text = f"var(--{size})"
                alias = css_alias(value_text)
                if alias is not None:
                    read.append((join(dict(key), axes), "alias", alias[0], at))
                    if alias[1]:
                        own_notes.append((at, Item(f"{name}:{at}", prop, f"its fallback "
                                          f"{alias[1]} was left out; the reference holds the "
                                          "value")))
                else:
                    gamut: List[GamutMapped] = []
                    kind, value = read_value(value_text, gamut)
                    read.append((join(dict(key), axes), kind, value, at))
                    own_mapped += [(at, Mapped.of(f"{name}:{at}", prop, g)) for g in gamut]
                    if gamut and kind == "color":
                        own_original[join(dict(key), axes)] = value_text.strip()
        except NotRead as exc:
            not_read.append((line, Item(f"{name}:{line}", prop, str(exc))))
            continue
        values[path] = read
        notes += own_notes
        mapped += own_mapped
        if own_original:
            originals[path] = own_original

    def drop(path: str, at: int, why: str) -> None:
        nonlocal notes, mapped
        not_read.append((at, Item(f"{name}:{at}", f"--{path}", why)))
        notes = [n for n in notes if n[1].name != f"--{path}"]
        mapped = [m for m in mapped if m[1].name != f"--{path}"]
        originals.pop(path, None)
        del values[path]

    # A reference to a property that was not read, or not defined, is not read.
    changed = True
    while changed:
        changed = False
        for path in list(values):
            gone = next(((v, at) for _, k, v, at in values[path] if k == "alias"
                         and v not in values), None)
            if gone is None:
                continue
            target, at = gone
            why = (f"references --{target}, which was not read; fix --{target} and import "
                   "again") if f"--{target}" in found or f"--{target}" in switches else (
                f"references --{target}, which this file does not define; define it or write "
                "the value, or import it together with the file that defines it")
            drop(path, at, why)
            changed = True

    def kind_of(path: str, seen: Tuple[str, ...] = ()) -> str:
        """Literals decide a type; an alias takes its target's."""
        literal = next((k for _, k, _, _ in values[path] if k != "alias"), "")
        if literal or path in seen:
            return literal
        return next((got for _, k, v, _ in values[path]
                     for got in [kind_of(v, seen + (path,))] if got), "")

    kinds = {path: kind_of(path) for path in values}
    ts = TokenSet(axes)
    for path, read in list(values.items()):
        kind = kinds[path]
        odd = next((k for _, k, _, _ in read if k not in ("alias", kind)), None)
        if odd or not kind:
            at = read[0][3]
            drop(path, at, f"holds a {kind} in one mode and a {odd} in another; give it one "
                           "type" if odd else "references only itself; give it a value")
            continue
        written = {ctx: ("{" + v + "}" if k == "alias" else v) for ctx, k, v, _ in read}
        mode_values = {ctx: v for ctx, v in written.items() if ctx}
        aliased = any(k == "alias" for _, k, _, _ in read)
        token = Token(path, kind, written[""], modes=mode_values,
                      layer="semantic" if aliased or mode_values else "primitive")
        if path in originals:
            # The spelling the file used, and what it was read as, so the
            # write-back gives the spelling back while the value holds.
            token.extensions = {"original": originals[path],
                                "read_as": {ctx: token.modes[ctx] if ctx else token.value
                                            for ctx in originals[path]}}
        ts.add(token)
    written_as = modes.forms.get("scheme")
    for line, label, props, form in paired:
        read_here = [p for p in props if ts.has(p[2:])]
        if read_here:
            count = (f"{len(read_here)} properties were" if len(read_here) > 1
                     else "1 property was")
            back = ""
            if written_as and form != written_as[0] and not (form == "@media" and written_as[1]):
                back = f"; it is written back as {written_as[0]}"
            notes.append((line, Item(f"{name}:{line}", label, (
                f"is the dark scheme; {count} paired by name with the root's and read as "
                f"scheme:dark ({', '.join(read_here)}){back}"))))
    report = ImportReport.of(source, ts, entries=entries)
    report.notes = [i for _, i in sorted(notes, key=lambda x: x[0])]
    report.not_read = [i for _, i in sorted(not_read, key=lambda x: x[0])]
    report.mapped = [i for _, i in sorted(mapped, key=lambda x: x[0])]
    return Imported(ts, report, dict(modes.forms), modes.scheme())


def write_css(imported: Imported) -> str:
    """An imported stylesheet written back as CSS in the forms the file
    used (Imported.forms and Imported.scheme; see export.to_css), with a
    header comment that lists every entry the import did not read, with
    how to write it so it can be read, and every color outside sRGB, which
    is written in the file's own spelling. Nothing is dropped silently."""
    report = imported.report
    lines = [f"Written back from {Path(report.source.path).name}."]
    if report.not_read:
        n = len(report.not_read)
        lines.append(f"{n} {'entry was' if n == 1 else 'entries were'} not read on the way in "
                     f"and {'is' if n == 1 else 'are'} not below; each with how to write it so "
                     "it can be read:")
        lines += [f"  {i.where} {i.name}: {i.message}" for i in report.not_read]
    if report.mapped:
        lines.append("Colors outside sRGB are written below as the file wrote them; the checks "
                     "read each as the sRGB color named:")
        lines += [f"  {m.where} {m.name}: {m.original}, read as {m.hex}" for m in report.mapped]
    return to_css(imported.tokens, scheme=imported.scheme, forms=imported.forms, header=lines)


def read_css(path: Any, label: str = "--from") -> Imported:
    """Read and import a CSS file."""
    source, text = read_source(path, "css", label)
    return import_css(text, source)
