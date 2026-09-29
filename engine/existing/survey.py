"""What a project's own code says about its design system, beside the
token files' names: token stylesheets found by what they hold, the color
the code paints buttons and links with, the languages its templates set,
a face kept for data and figures, and each token two sources set to
different values.

Deterministic and offline. Reads only the files detect's bounded walk
found; never writes.
"""
from __future__ import annotations

import re
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
_ROOTS = (":root", "html", ":host", "@theme")
# A theme selector: classes, attributes and :not()/:where() groups, on a root or alone.
_THEME_SEL = re.compile(
    r"^(?::root|html|:host)?(?:\.[A-Za-z][\w-]*|\[[\w-]+(?:\s*[~|^$*]?=\s*(?:\"[^\"]*\"|"
    r"'[^']*'|[\w-]+))?\]|:not\([^()]*\)|:where\([^()]*\))+$")
TEMPLATE_SUFFIXES = (".html", ".htm", ".blade.php", ".jsx", ".tsx", ".vue", ".svelte",
                     ".astro", ".erb", ".twig")
STYLE_SUFFIXES = (".css", ".scss", ".pcss")


def read_text(path: Path, limit: int = 400_000) -> str:
    try:
        return path.read_bytes()[:limit].decode("utf-8", errors="ignore")
    except OSError:
        return ""


def is_template(path: Path) -> bool:
    return path.name.lower().endswith(TEMPLATE_SUFFIXES)


def in_product(path: Path, base: Path) -> bool:
    """False for a file under a folder of examples, docs or tests."""
    parts = [p.lower() for p in path.relative_to(base).parts[:-1]]
    joined = "/".join(parts)
    return not (set(parts) & NOT_PRODUCT_DIRS or any(
        joined == d or joined.startswith(d + "/") for d in NOT_PRODUCT_DIRS if "/" in d))


def _rules(text: str, every: bool = False) -> List[Any]:
    from engine.foundations.errors import InputError
    from engine.io.css_in import parse_css  # engine.io imports this package
    try:
        return parse_css(text, every=every)
    except (InputError, ValueError):
        return []


def _members(selector: str) -> List[str]:
    from engine.io.values_in import split_top
    return [m.strip() for m in split_top(selector, ",") if m.strip()]


def _themed(selector: str) -> bool:
    return all(m in _ROOTS or _THEME_SEL.match(m) for m in _members(selector))


def _rooted(selector: str) -> bool:
    return all(m in _ROOTS for m in _members(selector))


def css_token_file(name: str, text: str) -> bool:
    """True when a stylesheet is a token source by what it holds: mostly
    custom properties set on the root or a theme selector, or, in a file
    named as an app's main stylesheet, a theme block of its own."""
    if "--" not in text:
        return False
    rules = _rules(text, every=True)
    theme = sum(1 for r in rules if _themed(r.selector)
                for d in r.declarations if d.name.startswith("--"))
    if theme < _MIN_THEME_PROPS:
        return False
    total = sum(len(r.declarations) for r in rules)
    return theme * 2 >= total or (bool(_MAIN_CSS.match(name)) and theme >= _MIN_MAIN_THEME_PROPS)


# ------------------------------------------------------------------ buttons and links

_BUTTON_SEL = re.compile(r"(?:^|[\s,>+~(])(?:a|button)(?=$|[\s,:.\[>+~)])"
                         r"|[.#][\w-]*(?:btn|button|link|cta)[\w-]*", re.I)
_TAG = re.compile(r"<([A-Za-z][\w.:-]*)\b([^<>]*?)/?>", re.S)
_BUTTON_TAG = re.compile(r"^(?:a|button|link|x-button|x-link|nuxtlink|routerlink|"
                         r"[\w.:-]*button)$", re.I)
_CLASS_ATTR = re.compile(r"\bclass(?:Name)?\s*=\s*(?:\{\s*)?([\"'`])(.*?)\1", re.S)
_UTILITIES = ("bg", "text", "border", "ring", "outline", "fill", "stroke", "decoration")


def _stem(name: str) -> str:
    """A token's name as a utility names it: --color-accent is accent,
    brand.primary is brand-primary."""
    flat = re.sub(r"[^A-Za-z0-9]+", "-", name.lstrip("-")).strip("-").lower()
    for lead in ("colors-", "color-"):
        if flat.startswith(lead):
            return flat[len(lead):]
    return flat


def _paint_patterns(name: str) -> Tuple[re.Pattern, re.Pattern]:
    """(a var() reference to the token, a utility class that paints with it)."""
    var = "--" + re.sub(r"[^A-Za-z0-9-]+", "-", name.lstrip("-")).strip("-")
    stem = _stem(name)
    whole = [re.escape(stem)] if stem.startswith(("bg-", "text-", "border-")) else []
    utility = "|".join(whole + [f"(?:{'|'.join(_UTILITIES)})-{re.escape(stem)}"])
    return (re.compile(r"var\(\s*" + re.escape(var) + r"\s*[,)]", re.I),
            re.compile(r"(?<![\w-])(?:" + utility + r")(?![\w-])", re.I))


def button_paints(names: Sequence[str], files: Sequence[Path]) -> Dict[str, int]:
    """For each color token name, how often the code paints a button or a
    link with it: a var() reference or an @apply in a rule whose selector
    names a, button, a btn, link or cta class, and a utility class or a
    var() in the attributes of an a, a button or an element whose class
    names btn or button."""
    patterns = {n: _paint_patterns(n) for n in names}
    counts = {n: 0 for n in names}
    for path in files:
        low = path.name.lower()
        if low.endswith(STYLE_SUFFIXES):
            text = read_text(path)
            if "{" not in text:
                continue
            for rule in _rules(text, every=True):
                if not _BUTTON_SEL.search(rule.selector):
                    continue
                body = " ".join(f"{d.name}: {d.value}" for d in rule.declarations)
                for n, (var, util) in patterns.items():
                    counts[n] += len(var.findall(body)) + sum(
                        len(util.findall(d.value)) for d in rule.declarations
                        if d.name == "@apply")
        elif is_template(path):
            text = read_text(path)
            for m in _TAG.finditer(text):
                tag, attrs = m.group(1), m.group(2)
                cls = " ".join(c.group(2) for c in _CLASS_ATTR.finditer(attrs))
                if not (_BUTTON_TAG.match(tag) or re.search(r"(?<![\w-])(?:btn|button)",
                                                            cls, re.I)):
                    continue
                for n, (var, util) in patterns.items():
                    counts[n] += len(var.findall(attrs)) + len(util.findall(cls))
    return counts


# ------------------------------------------------------------------ languages

_HTML_LANG = re.compile(r"<html\b[^>]*?\blang\s*=\s*\{?\s*['\"]([A-Za-z]{2,3})(?:[-_][A-Za-z0-9-]+)?"
                        r"['\"]", re.I)
_RTL = re.compile(r"\bdir\s*=\s*\{?\s*['\"]rtl['\"]", re.I)
_ARABIC = re.compile("[\\u0600-\\u06FF\\u0750-\\u077F\\u08A0-\\u08FF\\uFB50-\\uFDFF\\uFE70-\\uFEFF]")
# Arabic letters a template holds before its text counts as Arabic: a
# language switcher's own name for Arabic is fewer.
_MIN_ARABIC = 10


def languages(files: Sequence[Path]) -> Tuple[List[str], bool]:
    """(the languages the project's pages and templates set, most used
    first; True when any of them sets dir="rtl"). A page or template counts
    once for the language its <html lang> names, and once for Arabic when
    its text holds Arabic script, so a Blade view or a JSX page with a
    dynamic lang still counts."""
    counts: Dict[str, List[int]] = {}
    rtl_any = False
    for order, path in enumerate(files):
        if not is_template(path):
            continue
        text = read_text(path, 200_000)
        rtl = bool(_RTL.search(text))
        rtl_any = rtl_any or rtl
        found = []
        m = _HTML_LANG.search(text[:20_000])
        if m:
            found.append(m.group(1).lower())
        if "ar" not in found and len(_ARABIC.findall(text)) >= _MIN_ARABIC:
            found.append("ar")
        for lang in found:
            rec = counts.setdefault(lang, [0, 0, order])
            rec[0] += 1
            if rtl and (lang == "ar" or len(found) == 1):
                rec[1] += 1
    ranked = [lang for lang, _ in sorted(counts.items(),
                                         key=lambda kv: (-kv[1][0], -kv[1][1], kv[1][2]))]
    return ranked, rtl_any


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
        for rule in _rules(read_text(path), every=True):
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


# ------------------------------------------------------------------ disagreements

_IMPORT = re.compile(r"@import\s+(?:url\(\s*)?[\"']([^\"']+)[\"']")
_LINK = re.compile(r"<link\b[^>]*?\bhref\s*=\s*[\"']([^\"']+\.css)(?:\?[^\"']*)?[\"']", re.I)


def token_key(name: str) -> str:
    """A token's name in one form across formats: --color-primary and
    color.primary are color-primary."""
    return re.sub(r"[^a-z0-9]+", "-", name.lstrip("-").lower()).strip("-")


def _loose(key: str) -> str:
    for lead in ("colors-", "color-"):
        if key.startswith(lead):
            return key[len(lead):]
    return key


def _css_root_values(text: str) -> Dict[str, Tuple[str, int]]:
    """name -> (value, specificity) of each custom property set on the root
    outside any media query; :root, :host and @theme outrank html, and a
    later declaration of equal rank wins, as in the cascade."""
    out: Dict[str, Tuple[str, int]] = {}
    for rule in _rules(text):
        if rule.media or not _rooted(rule.selector):
            continue
        rank = max(0 if m == "html" else 1 for m in _members(rule.selector))
        for d in rule.declarations:
            if d.name not in out or rank >= out[d.name][1]:
                out[d.name] = (d.value.strip(), rank)
    return out


def _imports(path: Path, text: str, base: Path) -> List[Path]:
    out = []
    for ref in _IMPORT.findall(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", ref, re.I):
            continue
        try:
            cand = (path.parent / ref).resolve()
            cand.relative_to(base)
        except (OSError, ValueError):
            continue
        out.append(cand)
    return out


def disagreements(base: Path, css_paths: Sequence[Path], token_docs: Sequence[Tuple[Path, Any]],
                  md_paths: Sequence[Path], pages: Sequence[Path],
                  reading: Callable[[str, Dict[str, str]], str],
                  flatten: Callable[[Any], Dict[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Each token two sources set to different values: stylesheets, token
    files and a hand-written MASTER.md or DESIGN.md palette. Each entry
    names the token, every file with its value, the file that wins in the
    cascade ("" when these files do not decide it) and why. `reading`
    turns a value into what it reads as, given the properties around it;
    `flatten` reads a token document."""
    rel = {p: p.relative_to(base).as_posix() for p in [*css_paths, *(p for p, _ in token_docs),
                                                        *md_paths]}
    css: Dict[Path, Dict[str, Tuple[str, int]]] = {}
    texts: Dict[Path, str] = {}
    for path in css_paths:
        texts[path] = read_text(path)
        css[path] = _css_root_values(texts[path])
    union: Dict[str, str] = {}
    for values in css.values():
        for name, (value, _) in values.items():
            union.setdefault(name, value)
    # key -> [(path, name as written, value as written, reading, kind, rank)]
    found: Dict[str, List[Tuple[Path, str, str, str, str, int]]] = {}
    for path, values in css.items():
        own = {n: v for n, (v, _) in values.items()}
        props = {**union, **own}
        for name, (value, rank) in values.items():
            found.setdefault(token_key(name), []).append(
                (path, name, value, reading(value, props), "css", rank))
    for path, doc in token_docs:
        for name, tok in flatten(doc).items():
            value = tok.get("value")
            if isinstance(value, (str, int, float)) and not isinstance(value, bool):
                text = str(value)
                found.setdefault(token_key(name), []).append(
                    (path, name, text, reading(text, union), "tokens", 0))
    loose: Dict[str, List[str]] = {}
    for key in found:
        loose.setdefault(_loose(key), []).append(key)
    for path in md_paths:
        from engine.io.markdown_in import import_markdown  # engine.io imports this package
        from engine.io.report import Source
        try:
            imported = import_markdown([(path.name, read_text(path))],
                                       Source(str(path), "markdown", "0" * 64, 0))
        except (ValueError, TypeError):
            continue
        for tok in imported.tokens.tokens():
            if tok.type != "color" or not isinstance(tok.value, str) or tok.value.startswith("{"):
                continue
            for key in loose.get(_loose(token_key(tok.path)), []):
                found[key].append((path, tok.path, tok.value, reading(tok.value, union), "md", 0))

    later, imported = _load_order(css_paths, texts, pages, base)
    out: List[Dict[str, Any]] = []
    for key, entries in found.items():
        by_file: Dict[Path, Tuple[Path, str, str, str, str, int]] = {}
        for e in entries:
            by_file[e[0]] = e  # a file's last word on the token
        if len(by_file) < 2 or len({e[3] for e in by_file.values()}) < 2:
            continue
        rows = list(by_file.values())
        wins, why = _winner(rows, later, imported, rel)
        name = next((e[1] for e in rows if e[4] == "css"), rows[0][1])
        listed = [f"{e[2]} in {rel[e[0]]}" for e in rows]
        said = " and ".join(listed) if len(listed) == 2 else (
            ", ".join(listed[:-1]) + " and " + listed[-1])
        out.append({"token": name,
                    "values": [{"path": rel[e[0]], "token": e[1], "value": e[2]} for e in rows],
                    "wins": rel[wins] if wins else "",
                    "why": f"{name} is {said}; {why}"})
    return out


def _load_order(css_paths: Sequence[Path], texts: Dict[Path, str], pages: Sequence[Path],
                base: Path) -> Tuple[Dict[Path, set], Dict[Path, set]]:
    """(for each stylesheet the stylesheets it loads after: those it
    imports at any depth and those a page links before it; for each the
    ones it imports)."""
    direct = {p: {q for q in _imports(p, texts[p], base) if q in texts} for p in css_paths}
    after: Dict[Path, set] = {}
    for p in css_paths:
        seen, stack = set(), list(direct[p])
        while stack:
            q = stack.pop()
            if q not in seen:
                seen.add(q)
                stack += list(direct.get(q, ()))
        after[p] = set(seen)
    imported = {p: set(s) for p, s in after.items()}
    by_name = {}
    for p in css_paths:
        by_name.setdefault(p.name, []).append(p)
    for page in pages:
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
            after[p] |= set(linked[:i])
    return after, imported


def _winner(rows: List[Tuple[Path, str, str, str, str, int]], later: Dict[Path, set],
            imported: Dict[Path, set], rel: Dict[Path, str]) -> Tuple[Optional[Path], str]:
    """The file whose value the page shows, and why; (None, why) when these
    files do not decide it."""
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
    if len(ranked) < len(styles):
        low = [rel[e[0]] for e in styles if e[5] < top]
        why_rank = (f"it sets it on :root, which outranks html in {', '.join(low)} whatever "
                    "the order")
    else:
        why_rank = ""
    if len(ranked) == 1:
        win = ranked[0][0]
        why = why_rank or "it is the only stylesheet that sets it; the page shows its value"
    else:
        last = [e for e in ranked if all(o[0] in later[e[0]] for o in ranked if o is not e)]
        if not last:
            names = " and ".join(rel[e[0]] for e in ranked)
            return None, (f"{names} set it with equal weight and neither loads the other, so the "
                          "stylesheet the page loads last wins; keep one value, or import one "
                          "file from the other so the order is written down")
        win = last[0][0]
        undone = [rel[e[0]] for e in ranked if e[0] != win]
        how = ("imports" if all(o[0] in imported[win] for o in ranked if o[0] != win)
               else "loads after")
        why = (f"it {how} {', '.join(undone)} and sets it again after, which silently undoes "
               f"the value there; remove the second declaration, or change it in "
               f"{', '.join(undone)}")
    tail = ""
    docs = [rel[e[0]] for e in others if e[4] == "md"]
    tokens = [rel[e[0]] for e in others if e[4] == "tokens"]
    if tokens:
        tail += (f"; {', '.join(tokens)} holds another value, which reaches the page only "
                 "through a build that writes it into a stylesheet, so make them agree")
    if docs:
        tail += (f"; {', '.join(docs)} only describes the palette, so correct the document or "
                 "the token")
    return win, f"{rel[win]} wins: {why}{tail}"
