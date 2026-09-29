"""What a project's own code says about its design system, beside the
token files' names: token stylesheets found by what they hold, the color
the code paints buttons and links with, the languages its templates and
locale files set, a face kept for data and figures, and each token two
sources set to different values.

Deterministic and offline. Reads only the files detect's bounded walk
found; never writes.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

# Folders that hold examples of a system, not the product's own: a token
# file found there by its content is not the project's system.
NOT_PRODUCT_DIRS = frozenset((
    "docs", "doc", "examples", "example", "samples", "sample", "fixtures", "fixture",
    "tests", "test", "__tests__", "spec", "specs", "demo", "demos", "stories",
    "storybook-static", "coverage", "public/vendor"))
# A stylesheet named as an app's main one: a theme block of its own there
# is a token source even beside component rules.
_MAIN_CSS = re.compile(r"^(?:app|main|globals?|styles?|index|site|base|theme|tokens?|"
                       r"variables|vars|root)\.(?:css|scss|pcss)$", re.I)
_MIN_THEME_PROPS = 3
_MIN_MAIN_THEME_PROPS = 6
STYLE_SUFFIXES = (".css", ".scss", ".pcss")
TEMPLATE_SUFFIXES = (".html", ".htm", ".blade.php", ".jsx", ".tsx", ".vue", ".svelte",
                     ".astro", ".erb", ".twig")
# A custom property declaration, the cheap test before a stylesheet is parsed.
_DECLARES = re.compile(r"--[A-Za-z0-9_-]+\s*:")
# One simple selector of a compound: a class, an attribute, or a :not()
# or :where() group.
_SIMPLE = re.compile(r"\.([A-Za-z][\w-]*)|\[([\w-]+)(?:\s*[~|^$*]?=\s*(?:\"[^\"]*\"|'[^']*'|"
                     r"[\w-]+))?\]|:not\([^()]*\)|:where\([^()]*\)")
# A class that names a theme (.dark, .theme-x, .light-mode), and an
# attribute that switches one (data-theme, data-mode, data-color-scheme,
# the engine's own data-density, data-contrast, data-motion, dir and lang).
_THEME_CLASS = re.compile(r"(?:^|-)(?:theme|dark|light|mode|scheme)(?:$|-)", re.I)
# Words that make a theme-named class a widget: .theme-toggle, .dark-switch.
_WIDGET_WORDS = frozenset(("toggle", "switch", "switcher", "box", "button", "btn", "picker",
                           "menu", "icon", "card", "panel", "modal", "badge", "tab", "tabs",
                           "link", "label", "input", "select", "dropdown", "tooltip", "popover",
                           "bar", "nav", "item", "banner", "preview", "sample", "swatch"))
# A selector that names a scheme: .dark, .light-mode, [data-theme=dark].
_SCHEME_NAMED = re.compile(r"(?:^|[.\-])(?:dark|light)(?:$|[\-.\[:\s])"
                           r"|=\s*[\"']?(?:dark|light)\b", re.I)
_THEME_ATTR = re.compile(r"^(?:(?:data-)?(?:[a-z]+-)?(?:theme|mode|scheme)|data-density|"
                         r"data-contrast|data-motion|dir|lang)$", re.I)


def read_text(path: Path, limit: int = 400_000) -> str:
    try:
        return path.read_bytes()[:limit].decode("utf-8", errors="ignore")
    except OSError:
        return ""


def is_template(path: Path) -> bool:
    return path.name.lower().endswith(TEMPLATE_SUFFIXES)


def is_style(path: Path) -> bool:
    low = path.name.lower()
    return low.endswith(STYLE_SUFFIXES) and not low.endswith(".min.css")


def in_product(path: Path, base: Path) -> bool:
    """False for a file under a folder of examples, docs or tests."""
    parts = [p.lower() for p in path.relative_to(base).parts[:-1]]
    joined = "/".join(parts)
    return not (set(parts) & NOT_PRODUCT_DIRS or any(
        joined == d or joined.startswith(d + "/") for d in NOT_PRODUCT_DIRS if "/" in d))


def declares(text: str) -> bool:
    """True when a stylesheet declares a custom property, not only uses one."""
    return bool(_DECLARES.search(text))


def _rules(text: str) -> Tuple[Any, ...]:
    """Every rule of a stylesheet with all its declarations, parsed once
    for every reader here (a stylesheet is read for tokens, paints, the
    data face and disagreements)."""
    return _parsed(text)


@lru_cache(maxsize=512)
def _parsed(text: str) -> Tuple[Any, ...]:
    from engine.foundations.errors import InputError
    from engine.io.css_in import parse_css  # engine.io imports this package
    try:
        return tuple(parse_css(text, every=True))
    except (InputError, ValueError):
        return ()


def _members(selector: str) -> List[str]:
    from engine.io.values_in import split_top
    return [m.strip() for m in split_top(selector, ",") if m.strip()]


def _theme_member(member: str) -> bool:
    """True for the root, or a compound of theme classes and attributes on
    the root or alone. A class or attribute of any other name on its own
    (.dp, [data-size]) is a component, whatever properties it holds."""
    if _is_root(member):
        return True
    rest, rooted = member, False
    root = _root_prefix(member)
    if root and root != "@theme":
        rest, rooted = member.strip()[len(root):], True
    if not rest:
        return rooted
    pos = 0
    while pos < len(rest):
        m = _SIMPLE.match(rest, pos)
        if not m:
            return False
        if not rooted and ((m.group(1) and (not _THEME_CLASS.search(m.group(1)) or set(
                m.group(1).lower().split("-")) & _WIDGET_WORDS))
                           or (m.group(2) and not _THEME_ATTR.match(m.group(2)))):
            return False
        pos = m.end()
    return True


def _themed(selector: str) -> bool:
    return all(_theme_member(m) for m in _members(selector))


def _rooted(selector: str) -> bool:
    return all(_is_root(m) for m in _members(selector))


def _is_root(member: str) -> bool:
    from engine.io.css_in import is_root  # engine.io imports this package
    return is_root(member)


def _root_prefix(member: str) -> str:
    from engine.io.css_in import root_prefix  # engine.io imports this package
    return root_prefix(member)


def _specificity(member: str) -> Tuple[int, int, int]:
    from engine.io.css_in import specificity  # engine.io imports this package
    return specificity(member)


def css_token_file(name: str, text: str) -> bool:
    """True when a stylesheet is a token source by what it holds: mostly
    custom properties set on the root or a theme selector, or, in a file
    named as an app's main stylesheet, a theme block of its own. A widget
    or component stylesheet (`.dp { --dp-bg: ... }`) is not one."""
    if not declares(text):
        return False
    rules = _rules(text)
    # Theme selectors off the root count only in a file that sets the root
    # or names a scheme: a widget's [data-mode=compact] block is its own.
    themed = [r for r in rules if _themed(r.selector)]
    if not any(_rooted(r.selector) or _SCHEME_NAMED.search(r.selector) for r in themed):
        return False
    theme = sum(1 for r in themed for d in r.declarations if d.name.startswith("--"))
    if theme < _MIN_THEME_PROPS:
        return False
    total = sum(len(r.declarations) for r in rules)
    return theme * 2 >= total or (bool(_MAIN_CSS.match(name)) and theme >= _MIN_MAIN_THEME_PROPS)


# ------------------------------------------------------------------ buttons and links

_BUTTON_SEL = re.compile(r"(?:^|[\s,>+~(])button(?=$|[\s,:.\[>+~)])"
                         r"|[.#][\w-]*(?:btn|button|cta)[\w-]*", re.I)
_LINK_SEL = re.compile(r"(?:^|[\s,>+~(])a(?=$|[\s,:.\[>+~)])|[.#][\w-]*link[\w-]*", re.I)
# A state pseudo-class: what it paints is not the resting fill.
_STATE_PSEUDO = re.compile(r":(?:hover|focus|focus-visible|focus-within|active|visited|"
                           r"disabled|checked|target)\b", re.I)
_TAG = re.compile(r"<([A-Za-z][\w.:-]*)\b([^<>]*?)/?>", re.S)
_BUTTON_TAG = re.compile(r"^(?:button|x-button|[\w.:-]*button)$", re.I)
_LINK_TAG = re.compile(r"^(?:a|link|x-link|nuxtlink|routerlink|[\w.:-]*link)$", re.I)
_CLASS_ATTR = re.compile(r"\bclass(?:Name)?\s*=\s*(?:\{\s*)?([\"'`])(.*?)\1", re.S)
# Calls whose string arguments are class lists: cva, clsx, cn and the like.
_CLASS_CALL = re.compile(r"\b(?:cva|clsx|cn|cx|classnames|classNames|twMerge|twJoin|tv)\s*\(")
_STRING = re.compile(r"\"([^\"\\\n]*)\"|'([^'\\\n]*)'|`([^`\\]*)`")
# Variants a resting fill may carry: the viewport, the scheme and direction.
_RESTING_VARIANTS = frozenset(("sm", "md", "lg", "xl", "2xl", "dark", "light", "rtl", "ltr",
                               "print"))


def _stem(name: str) -> str:
    """A token's name as a utility names it: --color-accent is accent,
    brand.primary is brand-primary."""
    flat = re.sub(r"[^A-Za-z0-9]+", "-", name.lstrip("-")).strip("-").lower()
    for lead in ("colors-", "color-"):
        if flat.startswith(lead):
            return flat[len(lead):]
    return flat


def _resting(classes: str) -> List[str]:
    """The utilities of a class list that hold at rest: without a state
    variant (hover:, focus:, group-hover:), their opacity and ! left off."""
    out = []
    for token in re.split(r"[\s\"'`{}(),]+", classes):
        if not token:
            continue
        *variants, util = token.split(":")
        if any(v.lower() not in _RESTING_VARIANTS for v in variants):
            continue
        out.append(util.lstrip("!").split("/")[0].lower())
    return out


def _class_calls(text: str) -> List[Tuple[int, str]]:
    """(offset, the class strings) of each cva, clsx or cn call in a file."""
    out = []
    for m in _CLASS_CALL.finditer(text):
        depth, end = 0, len(text)
        for i in range(m.end() - 1, min(len(text), m.end() + 20_000)):
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            if depth == 0:
                end = i
                break
        strings = [next(g for g in s.groups() if g is not None)
                   for s in _STRING.finditer(text, m.end(), end)]
        out.append((m.start(), " ".join(strings)))
    return out


def button_paints(names: Sequence[str], files: Sequence[Path]) -> Dict[str, int]:
    """For each color token name, how often the code paints a button or a
    link with it at rest: a background (and, on a link, a color) set with
    var() in a rule for a button or a link with no state pseudo-class, and
    a bg- utility (a text- one on a link) with no state variant, in the
    class of a button or a link element or in a cva, clsx or cn call of a
    button or link component. Hover and focus paints are not counted."""
    counts = {n: 0 for n in names}
    stems = {n: _stem(n) for n in names}
    vars_ = {n: re.compile(r"var\(\s*--" + re.escape(
        re.sub(r"[^A-Za-z0-9-]+", "-", n.lstrip("-")).strip("-")) + r"\s*[,)]", re.I)
        for n in names}

    def utilities(classes: str, link: bool) -> None:
        for util in _resting(classes):
            for n, stem in stems.items():
                own = stem if stem.startswith(("bg-", "text-")) else ""
                if util in (f"bg-{stem}", own) or (link and util == f"text-{stem}"):
                    counts[n] += 1

    for path in files:
        low = path.name.lower()
        if is_style(path):
            text = read_text(path)
            if "{" not in text:
                continue
            for rule in _rules(text):
                button = bool(_BUTTON_SEL.search(rule.selector))
                link = bool(_LINK_SEL.search(rule.selector))
                if not (button or link) or _STATE_PSEUDO.search(rule.selector):
                    continue
                for d in rule.declarations:
                    prop = d.name.lower()
                    if d.name == "@apply":
                        utilities(d.value, link)
                    elif prop in ("background", "background-color") or (link and prop == "color"):
                        for n, var in vars_.items():
                            counts[n] += len(var.findall(d.value))
        elif is_template(path):
            text = read_text(path)
            for m in _TAG.finditer(text):
                tag, attrs = m.group(1), m.group(2)
                cls = " ".join(c.group(2) for c in _CLASS_ATTR.finditer(attrs))
                link = bool(_LINK_TAG.match(tag))
                if not (link or _BUTTON_TAG.match(tag)
                        or re.search(r"(?<![\w-])(?:btn|button)", cls, re.I)):
                    continue
                utilities(cls, link)
            component = re.search(r"button|btn|link", low)
            for at, strings in _class_calls(text):
                named = re.search(r"(\w+)\s*=\s*$", text[max(0, at - 60):at])
                what = (named.group(1) if named else "") + " " + low
                if component or re.search(r"button|btn|link", what, re.I):
                    utilities(strings, bool(re.search(r"link", what, re.I)))
    return counts


# ------------------------------------------------------------------ languages

_HTML_LANG = re.compile(r"<html\b[^>]*?\blang\s*=\s*\{?\s*['\"]([A-Za-z]{2,3})(?:[-_][A-Za-z0-9-]+)?"
                        r"['\"]", re.I)
_PAGE_RTL = re.compile(r"<(?:html|body)\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*?\bdir\s*=\s*\{?\s*"
                       r"['\"]rtl['\"]", re.I)
_ANY_RTL = re.compile(r"\bdir\s*=\s*\{?\s*['\"]rtl['\"]", re.I)
# dir set from the locale, such as dir={isArabic ? "rtl" : "ltr"}.
_DYNAMIC_RTL = re.compile(r"\bdir\s*=\s*\{[^{}]*['\"]rtl['\"][^{}]*\}", re.I)
_ARABIC = re.compile("[\\u0600-\\u06FF\\u0750-\\u077F\\u08A0-\\u08FF\\uFB50-\\uFDFF\\uFE70-\\uFEFF]")
# Arabic letters a template holds before its text counts as Arabic: a
# language switcher's own name for Arabic is fewer.
_MIN_ARABIC = 10
# Folders that hold a locale's strings: lang/ar.json, messages/ar.json,
# locales/ar/common.json, resources/lang/ar/auth.php.
LOCALE_DIRS = frozenset(("lang", "langs", "locale", "locales", "messages", "i18n",
                         "translations", "translation", "l10n"))
_LOCALE = re.compile(r"^([a-z]{2,3})(?:[-_][A-Za-z]{2,4})?$")
_LOCALE_SUFFIXES = (".json", ".php", ".yml", ".yaml", ".po", ".js", ".ts")


def locale_of(path: Path) -> str:
    """The language a locale file holds (ar for lang/ar.json or
    locales/ar/common.json), or ""."""
    parts = [p.lower() for p in path.parts]
    if not path.name.lower().endswith(_LOCALE_SUFFIXES) or len(parts) < 2:
        return ""
    stem = path.name.split(".")[0].lower()
    if parts[-2] in LOCALE_DIRS and _LOCALE.match(stem):
        return _LOCALE.match(stem).group(1)
    if len(parts) >= 3 and parts[-3] in LOCALE_DIRS and _LOCALE.match(parts[-2]):
        return _LOCALE.match(parts[-2]).group(1)
    return ""


def languages(files: Sequence[Path]) -> Tuple[List[str], bool]:
    """(the languages the project sets, most used first; True when its
    pages read right to left). A page or template counts once for the
    language its <html lang> names, and once for Arabic when its text holds
    Arabic script, so a Blade view or a JSX page with a dynamic lang still
    counts. Languages that only locale files hold (lang/ar.json) follow,
    most files first. Right to left is dir="rtl" on <html> or <body>, on
    anything in a page whose text is Arabic, or set from the locale when
    Arabic is one of the languages; a language switcher's dir does not
    count."""
    counts: Dict[str, List[int]] = {}
    locales: Dict[str, List[int]] = {}
    rtl = dynamic = False
    for order, path in enumerate(files):
        lang = locale_of(path)
        if lang:
            rec = locales.setdefault(lang, [0, order])
            rec[0] += 1
            continue
        if not is_template(path):
            continue
        text = read_text(path, 200_000)
        found = []
        m = _HTML_LANG.search(text[:20_000])
        if m:
            found.append(m.group(1).lower())
        arabic = len(_ARABIC.findall(text)) >= _MIN_ARABIC
        if "ar" not in found and arabic:
            found.append("ar")
        here = bool(_PAGE_RTL.search(text) or (arabic and _ANY_RTL.search(text)))
        rtl = rtl or here
        dynamic = dynamic or bool(_DYNAMIC_RTL.search(text))
        for lang in found:
            rec = counts.setdefault(lang, [0, 0, order])
            rec[0] += 1
            if here and (lang == "ar" or len(found) == 1):
                rec[1] += 1
    ranked = [lang for lang, _ in sorted(counts.items(),
                                         key=lambda kv: (-kv[1][0], -kv[1][1], kv[1][2]))]
    ranked += [lang for lang, _ in sorted(locales.items(), key=lambda kv: (-kv[1][0], kv[1][1]))
               if lang not in ranked]
    return ranked, rtl or (dynamic and "ar" in ranked)


# ------------------------------------------------------------------ the data face

DATA_WORDS = frozenset(("mono", "monospace", "code", "data", "numeric", "numbers", "number",
                        "num", "nums", "figures", "figure", "tabular", "metric", "metrics",
                        "table", "stat", "stats", "digits", "digit"))
_DATA_SEL = re.compile(r"(?:^|[\s,>+~(])(?:table|td|th|thead|tbody|tfoot|output|data)"
                       r"(?=$|[\s,:.\[>+~)])|[.#\[][\w-]*(?:numeric|number|figure|metric|stat|"
                       r"kpi|amount|price|tabular|digit)[\w-]*", re.I)
_DATA_TAG = re.compile(r"^(?:table|td|th|tr|thead|tbody|tfoot|dd|output|data)$", re.I)
_DATA_CLASS = re.compile(r"(?<![\w-])(?:metric|stat|kpi|amount|price|figure|number|numeric)",
                         re.I)
_FONT_CLASS = re.compile(r"(?<![\w-])font-([a-z][\w-]*)")


def data_face(styles: Sequence[Path], files: Sequence[Path],
              family: Callable[[str], str]) -> Tuple[str, str]:
    """(the face the code sets on tables, figures and metrics, where it is
    set) or ("", ""). Read from a font-family in a rule whose selector names
    a table cell or a numeric class, then from a font-* utility on a table
    or a metric element whose --font-* token the system defines. `family`
    turns a value (a var() or a list) into the face's name."""
    for path in styles:
        for rule in _rules(read_text(path)):
            if not _DATA_SEL.search(rule.selector):
                continue
            for d in rule.declarations:
                if d.name.lower() == "font-family":
                    face = family(d.value)
                    if face:
                        return face, f"{rule.selector} in {path.name}"
    for path in files:
        if not is_template(path):
            continue
        for m in _TAG.finditer(read_text(path, 200_000)):
            cls = " ".join(c.group(2) for c in _CLASS_ATTR.finditer(m.group(2)))
            if not (_DATA_TAG.match(m.group(1)) or _DATA_CLASS.search(cls)):
                continue
            for f in _FONT_CLASS.finditer(cls):
                face = family(f"var(--font-{f.group(1)})")
                if face:
                    return face, f"font-{f.group(1)} on <{m.group(1)}> in {path.name}"
    return "", ""


# ------------------------------------------------------------------ the dark scheme


def dark_scheme(base: Path, styles: Sequence[Path]) -> List[Dict[str, Any]]:
    """Where the project keeps its dark values, wherever it lives: each
    stylesheet rule that sets custom properties under a dark selector
    ([data-theme=dark], .dark, the root written twice before one) or under
    prefers-color-scheme: dark, as {path, line, selector, properties}, one
    entry per file and selector, in the order the files are given."""
    from engine.io.css_in import _Modes  # engine.io imports this package
    out: Dict[Tuple[Path, str], Dict[str, Any]] = {}
    for path in styles:
        for rule in _rules(read_text(path)):
            props = [d for d in rule.declarations if d.name.startswith("--")]
            if not props:
                continue
            by_media = any(re.search(r"prefers-color-scheme\s*:\s*dark", m) for m in rule.media)
            named = any(("scheme", "dark") in [(a, v) for a, v, _ in _Modes.parse(m) or []]
                        for m in _members(rule.selector))
            if not (by_media or named):
                continue
            shown = rule.selector.strip()
            if by_media:
                shown = " ".join([*(f"@media {m}" for m in rule.media), shown])
            key = (path, shown)
            if key not in out:
                out[key] = {"path": path.relative_to(base).as_posix(), "line": rule.line,
                            "selector": shown, "properties": 0}
            out[key]["properties"] += len(props)
    return list(out.values())


# ------------------------------------------------------------------ disagreements

_IMPORT = re.compile(r"@import\s+(?:url\(\s*)?[\"']([^\"']+)[\"']\s*\)?([^;]*);")
_LINK = re.compile(r"<link\b[^>]*?\bhref\s*=\s*[\"']([^\"']+\.css)(?:\?[^\"']*)?[\"']", re.I)
_LAYER_BLOCK = re.compile(r"@layer\b[^{};]*\{")
# (layered, specificity): a declaration outside any cascade layer beats
# one inside a layer, whatever their order and specificity; then the more
# specific selector wins (:root outranks html, :root:root and html:root
# outrank :root), as the browser decides.
Rank = Tuple[int, Tuple[int, int, int]]
# (value, rank, line, selector) of one custom property in a stylesheet.
Set_ = Tuple[str, Rank, int, str]


def token_key(name: str) -> str:
    """A token's name in one form across formats: --color-primary and
    color.primary are color-primary."""
    return re.sub(r"[^a-z0-9]+", "-", name.lstrip("-").lower()).strip("-")


def _loose(key: str) -> str:
    for lead in ("colors-", "color-"):
        if key.startswith(lead):
            return key[len(lead):]
    return key


def _layered_lines(text: str) -> List[Tuple[int, int]]:
    """The line ranges inside @layer blocks."""
    from engine.io.css_in import _blank_comments, _matching  # engine.io imports this package
    blank = _blank_comments(text)
    out = []
    for m in _LAYER_BLOCK.finditer(blank):
        try:
            end = _matching(blank, m.end() - 1, "the stylesheet")
        except ValueError:
            continue
        out.append((blank.count("\n", 0, m.start()) + 1, blank.count("\n", 0, end) + 1))
    return out


def _context(selector: str) -> str:
    """The theme a rule sets: "" for the root, else its selector without
    the root, quotes or spaces ([data-theme=dark] for :root[data-theme="dark"])."""
    if _rooted(selector):
        return ""
    parts = []
    for m in _members(selector):
        root = _root_prefix(m)
        if root and root != "@theme" and len(m.strip()) > len(root):
            m = m.strip()[len(root):]
        parts.append(re.sub(r"[\"'\s]", "", m))
    return ", ".join(sorted(parts))


def css_values(text: str, layered: bool = False) -> Dict[Tuple[str, str], Set_]:
    """(theme, name) -> (value, rank, line, selector) of each custom
    property a stylesheet sets on the root or a theme selector outside any
    media query, the cascade's last word within the file. `layered` when
    the file itself is imported into a layer."""
    if not declares(text):
        return {}
    layers = _layered_lines(text)
    out: Dict[Tuple[str, str], Set_] = {}
    for rule in _rules(text):
        if rule.media or not rule.declarations or not _themed(rule.selector):
            continue
        inside = layered or any(a <= rule.line <= b for a, b in layers)
        spec = max(_specificity(m) for m in _members(rule.selector))
        rank = (0 if inside else 1, spec)
        ctx = _context(rule.selector)
        for d in rule.declarations:
            if not d.name.startswith("--"):
                continue
            key = (ctx, d.name)
            if key not in out or rank >= out[key][1]:
                out[key] = (d.value.strip(), rank, d.line, rule.selector.strip())
    return out


def _packages(base: Path, files: Sequence[Path]) -> Dict[str, Path]:
    """Workspace package name -> its folder, from the package.json files
    the walk found."""
    out: Dict[str, Path] = {}
    for path in files:
        if path.name != "package.json" or path.parent == base:
            continue
        try:
            name = json.loads(read_text(path, 200_000)).get("name")
        except (ValueError, AttributeError):
            continue
        if isinstance(name, str) and name:
            out.setdefault(name, path.parent)
    return out


def _resolve(path: Path, ref: str, base: Path, packages: Dict[str, Path]) -> Optional[Path]:
    """The file an @import names: relative to the importing file, or a
    package name (@scope/pkg/file.css) through node_modules or a workspace
    package. None when it cannot be found."""
    cands = []
    if ref.startswith((".", "/")):
        cands.append(path.parent / ref)
    else:
        bits = ref.split("/")
        name = "/".join(bits[:2]) if ref.startswith("@") else bits[0]
        rest = "/".join(bits[2:] if ref.startswith("@") else bits[1:])
        folder = path.parent
        while True:
            cands.append(folder / "node_modules" / ref)
            if folder == base or base not in folder.parents:
                break
            folder = folder.parent
        if name in packages and rest:
            cands.append(packages[name] / rest)
        cands.append(path.parent / ref)
    for cand in cands:
        try:
            if cand.is_file():
                return cand.resolve()
        except OSError:
            continue
    return None


def _key_line(text: str, name: str) -> int:
    """The line a token file or document writes a token on: each segment of
    its path found as a key after the one before it (1 when not found)."""
    at = 0
    for seg in [s for s in re.split(r"[.]", name) if s]:
        m = re.search(r"[\"'`]" + re.escape(seg) + r"[\"'`]", text[at:])
        if not m:
            m = re.search(re.escape(seg), text[at:])
            if not m:
                return text.count("\n", 0, at) + 1 if at else 1
        at += m.start()
    return text.count("\n", 0, at) + 1


# One file's word on a token: (path, name as written, value as written,
# reading, kind, rank, line, selector).
_Row = Tuple[Path, str, str, str, str, Rank, int, str]


def disagreements(base: Path, css_paths: Sequence[Path], token_docs: Sequence[Tuple[Path, Any]],
                  md_paths: Sequence[Path], files: Sequence[Path],
                  reading: Callable[[str, Dict[str, str]], str],
                  flatten: Callable[[Any], Dict[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Each token two sources set to different values: stylesheets (every
    one that sets custom properties on the root or a theme, an app's main
    stylesheet among its component rules included, the root written twice
    as :root:root or html:root read as the root), token files and a
    hand-written MASTER.md or DESIGN.md palette. Each entry names the token
    (and the theme, for a value set under one), every file with its value
    and line, the file that wins in the cascade ("" when these files do not
    decide it) and why, with both files and lines. `files` is the walk, for
    pages, package names and node_modules; `reading` turns a value into
    what it reads as, given the properties around it; `flatten` reads a
    token document."""
    css_paths = [p.resolve() for p in css_paths]
    rel = {p: p.relative_to(base).as_posix() for p in [*css_paths, *(p for p, _ in token_docs),
                                                        *md_paths]}
    texts = {p: read_text(p) for p in css_paths}
    packages = _packages(base, files)
    order = _load_order(css_paths, texts, files, base, packages)
    css = {p: css_values(texts[p], p in order.layered) for p in css_paths}
    union: Dict[str, str] = {}
    for values in css.values():
        for (ctx, name), row in values.items():
            if not ctx:
                union.setdefault(name, row[0])
    # key -> every file's word on it
    found: Dict[Tuple[str, str], List[_Row]] = {}
    for path, values in css.items():
        own = {n: row[0] for (c, n), row in values.items() if not c}
        props = {**union, **own}
        for (ctx, name), (value, rank, line, selector) in values.items():
            found.setdefault((ctx, token_key(name)), []).append(
                (path, name, value, reading(value, props), "css", rank, line, selector))
    for path, doc in token_docs:
        text = read_text(path, 2_000_000)
        for name, tok in flatten(doc).items():
            value = tok.get("value")
            if isinstance(value, (str, int, float)) and not isinstance(value, bool):
                shown = str(value)
                found.setdefault(("", token_key(name)), []).append(
                    (path, name, shown, reading(shown, union), "tokens", (0, (0, 0, 0)),
                     _key_line(text, name), ""))
    loose: Dict[str, List[Tuple[str, str]]] = {}
    for key in found:
        if not key[0]:
            loose.setdefault(_loose(key[1]), []).append(key)
    for path in md_paths:
        from engine.io.markdown_in import import_markdown  # engine.io imports this package
        from engine.io.report import Source
        text = read_text(path)
        try:
            imported = import_markdown([(path.name, text)],
                                       Source(str(path), "markdown", "0" * 64, 0))
        except (ValueError, TypeError):
            continue
        for tok in imported.tokens.tokens():
            if tok.type != "color" or not isinstance(tok.value, str) or tok.value.startswith("{"):
                continue
            for key in loose.get(_loose(token_key(tok.path)), []):
                found[key].append((path, tok.path, tok.value, reading(tok.value, union), "md",
                                   (0, (0, 0, 0)), _key_line(text, tok.path), ""))

    out: List[Dict[str, Any]] = []
    for (ctx, _), entries in found.items():
        by_file: Dict[Path, _Row] = {}
        for e in entries:
            by_file[e[0]] = e  # a file's last word on the token
        if len(by_file) < 2 or len({e[3] for e in by_file.values()}) < 2:
            continue
        rows = list(by_file.values())
        wins, why = _winner(rows, order, rel)
        name = next((e[1] for e in rows if e[4] == "css"), rows[0][1])
        shown = f"{name} under {ctx}" if ctx else name
        listed = [f"{e[2]} in {rel[e[0]]}:{e[6]}" for e in rows]
        said = " and ".join(listed) if len(listed) == 2 else (
            ", ".join(listed[:-1]) + " and " + listed[-1])
        entry: Dict[str, Any] = {"token": name}
        if ctx:
            entry["theme"] = ctx
        entry.update({"values": [{"path": rel[e[0]], "line": e[6], "token": e[1], "value": e[2],
                                  **({"selector": e[7]} if e[7] else {})} for e in rows],
                      "wins": rel[wins] if wins else "",
                      "why": f"{shown} is {said}; {why}"})
        out.append(entry)
    return out


class _Order:
    """How the stylesheets load: for each, the ones it loads after (those
    it imports at any depth and those a page links before it), the ones it
    imports, the imports it names that could not be resolved, and the files
    imported into a cascade layer."""

    def __init__(self) -> None:
        self.after: Dict[Path, set] = {}
        self.imports: Dict[Path, set] = {}
        self.unresolved: Dict[Path, List[str]] = {}
        # Imports that resolve to a stylesheet outside the compared set.
        self.outside: Dict[Path, List[Tuple[str, str]]] = {}
        self.layered: set = set()


def _load_order(css_paths: Sequence[Path], texts: Dict[Path, str], files: Sequence[Path],
                base: Path, packages: Dict[str, Path]) -> _Order:
    from engine.io.css_in import _blank_comments  # engine.io imports this package
    order = _Order()
    direct: Dict[Path, set] = {}
    for p in css_paths:
        direct[p] = set()
        order.unresolved[p] = []
        order.outside[p] = []
        for ref, tail in _IMPORT.findall(_blank_comments(texts[p])):
            if re.match(r"^[a-z][a-z0-9+.-]*:", ref, re.I):
                continue
            target = _resolve(p, ref, base, packages)
            if target is None:
                if ref.lower().endswith(STYLE_SUFFIXES):
                    order.unresolved[p].append(ref)
                continue
            if target in texts:
                direct[p].add(target)
                if re.search(r"\blayer\b", tail):
                    order.layered.add(target)
            elif ref.lower().endswith(STYLE_SUFFIXES):
                try:
                    shown = target.relative_to(base).as_posix()
                except ValueError:
                    shown = target.name
                order.outside[p].append((ref, shown))
    for p in css_paths:
        seen, stack = set(), list(direct[p])
        while stack:
            q = stack.pop()
            if q not in seen:
                seen.add(q)
                stack += list(direct.get(q, ()))
        order.after[p] = set(seen)
        order.imports[p] = set(seen)
    by_name: Dict[str, List[Path]] = {}
    for p in css_paths:
        by_name.setdefault(p.name, []).append(p)
    for page in files:
        if not is_template(page):
            continue
        linked: List[Path] = []
        for href in _LINK.findall(read_text(page, 200_000)):
            try:
                cand = (page.parent / href).resolve()
            except OSError:
                continue
            if cand not in texts:
                named = by_name.get(Path(href).name, [])
                cand = named[0] if len(named) == 1 else cand
            if cand in texts and cand not in linked:
                linked.append(cand)
        for i, p in enumerate(linked):
            order.after[p] |= set(linked[:i])
    return order


def _at(e: _Row, rel: Dict[Path, str]) -> str:
    return f"{rel[e[0]]}:{e[6]}"


def _winner(rows: List[_Row], order: _Order,
            rel: Dict[Path, str]) -> Tuple[Optional[Path], str]:
    """The file whose value the page shows, and why, naming the winner and
    each loser by file and line; (None, why) when these files do not
    decide it."""
    styles = [e for e in rows if e[4] == "css"]
    if not styles:
        tokens = [e for e in rows if e[4] == "tokens"]
        if len(tokens) == 1:
            return tokens[0][0], (f"{rel[tokens[0][0]]} wins: it is the token file the system is "
                                  "built from, and the document only describes it, so correct "
                                  "the document or the token")
        return None, ("no stylesheet sets it, and the token files do not say which one the build "
                      "reads last; keep one value")
    top = max(e[5] for e in styles)
    ranked = [e for e in styles if e[5] == top]
    others = [e for e in rows if e not in ranked]
    why_rank = ""
    low = [e for e in styles if e[5] < top]
    if low:
        if any(e[5][0] < top[0] for e in low):
            why_rank = ("it is set outside any cascade layer, which beats the value inside a "
                        f"layer in {', '.join(_at(e, rel) for e in low if e[5][0] < top[0])} "
                        "whatever the order")
        else:
            sel = ranked[0][7]
            why_rank = (f"it sets it on {sel}, which outranks "
                        + ", ".join(f"{e[7]} in {_at(e, rel)}" for e in low)
                        + " whatever the order")
    if len(ranked) == 1:
        win = ranked[0]
        why = why_rank or "it is the only stylesheet that sets it; the page shows its value"
    else:
        last = [e for e in ranked
                if all(o[0] in order.after[e[0]] for o in ranked if o is not e)]
        if not last:
            names = " and ".join(_at(e, rel) for e in ranked)
            lost = [(rel[e[0]], ref) for e in ranked for ref in order.unresolved.get(e[0], [])]
            if lost:
                where, ref = lost[0]
                return None, (f"{names} set it with equal weight, and {where} imports {ref}, "
                              "which could not be resolved here, so which one the page loads "
                              "last is not known; keep one value")
            away = [(rel[e[0]], ref, target) for e in ranked
                    for ref, target in order.outside.get(e[0], [])]
            if away:
                where, ref, target = away[0]
                return None, (f"{names} set it with equal weight, and {where} imports {ref}, "
                              f"which resolves to {target}, not to either of these files, so "
                              "which one the page loads last is not known; keep one value, or "
                              "import the file the system keeps")
            return None, (f"{names} set it with equal weight and neither loads the other, so the "
                          "stylesheet the page loads last wins; keep one value, or import one "
                          "file from the other so the order is written down")
        win = last[0]
        undone = [e for e in ranked if e[0] != win[0]]
        at = ", ".join(_at(e, rel) for e in undone)
        how = ("imports" if all(o[0] in order.imports[win[0]] for o in ranked if o[0] != win[0])
               else "loads after")
        why = (f"it {how} {', '.join(rel[e[0]] for e in undone)} and sets it again after, which "
               f"silently undoes the value at {at}; remove the second declaration at "
               f"{_at(win, rel)}, or change it at {at}")
        if why_rank:
            why = f"{why}; {why_rank}"
    tail = ""
    # Only a file that says another value than the page shows is named.
    differ = [e for e in others if e[3] != win[3]]
    docs = [_at(e, rel) for e in differ if e[4] == "md"]
    tokens = [_at(e, rel) for e in differ if e[4] == "tokens"]
    if tokens:
        tail += (f"; {', '.join(tokens)} holds another value, which reaches the page only "
                 "through a build that writes it into a stylesheet, so make them agree")
    if docs:
        tail += (f"; {', '.join(docs)} only describes the palette, so correct the document or "
                 "the token")
    return win[0], f"{_at(win, rel)} wins: {why}{tail}"
