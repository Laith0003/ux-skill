"""Brand-fidelity scoring -- does generated output honor the extracted brand?

When ux-skill redesigns an EXISTING site, the output must use THAT brand's
primary color, carry its logo, match its type, and NOT drift to the engine's own
house style. ``score_brand_fidelity`` checks a rendered page against a
``BrandProfile`` and returns a 0-100 score plus per-check findings.

It is both SCORED and GATED (canonical rule 7): a **hard floor** trips when a
brand with a primary exists but the output drops the primary or the logo --
``passed=False`` regardless of the numeric score. Everything is deterministic and
offline; the same (html, profile) always returns the same result.

Public surface
--------------
``score_brand_fidelity(html_text, profile, css_text="", base_dir=None) -> dict``
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from engine.brand.extract import BrandProfile, hue_family
from engine.existing import css_custom_properties, normalize_hex


# The engine's own house colors. If a brand's primary differs from these and one
# of them shows up in the output, that is the engine's style leaking in (the exact
# dogfood failure: clay #cc785c shipped for an amber brand).
HOUSE_COLORS = {
    "#cc785c": "clay (Claude house color)",
    "#5e6ad2": "blurple (Linear house color)",
}

# Per-check weights toward the 0-100 score. Sum = 100.
_CHECK_WEIGHTS = {
    "primary_used": 35,
    "logo_present": 30,
    "type_matches": 20,
    "no_house_drift": 15,
}

_FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}{]+)", re.IGNORECASE)
_DISPLAY_CTX_RE = re.compile(
    r"(?:--font-display|--display-font|\bh1\b|\bh2\b|\bh3\b|\.display|\.headline|\.hero)",
    re.IGNORECASE,
)


def _norm_hex(h: Optional[str]) -> str:
    if not isinstance(h, str):
        return ""
    s = h.strip().lower()
    if not s.startswith("#"):
        s = "#" + s
    return s


def _hex_present(html_lower: str, hexstr: str) -> bool:
    """Case-insensitive: is this hex color used anywhere in the html/inline CSS?

    Matches the full 6-digit form and, when the color collapses, the 3-digit
    shorthand (e.g. #ffcc00 -> #fc0) so a shorthand author isn't missed.
    """
    hx = _norm_hex(hexstr)
    if len(hx) != 7:
        # only handle canonical 6-digit brand hexes; anything else: substring try
        return bool(hx) and hx in html_lower
    if hx in html_lower:
        return True
    r, g, b = hx[1:3], hx[3:5], hx[5:7]
    if r[0] == r[1] and g[0] == g[1] and b[0] == b[1]:
        short = "#" + r[0] + g[0] + b[0]
        if short in html_lower:
            return True
    return False


def _logo_present(html: str, html_lower: str, profile: BrandProfile) -> bool:
    """Logo url present, OR the brand name appears in a header/logo context."""
    logo_url = (profile.logo or {}).get("url") or ""
    if logo_url and logo_url.lower() in html_lower:
        return True
    name = (profile.name or "").strip()
    if not name:
        return False
    name_l = name.lower()
    # Header / nav / logo-classed regions where a wordmark legitimately lives.
    region_res = [
        re.compile(r"<header\b[^>]*>(.*?)</header>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<nav\b[^>]*>(.*?)</nav>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<title\b[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<[^>]*\b(?:class|id|aria-label|alt)\s*=\s*['\"][^'\"]*\b(?:logo|brand|wordmark)\b[^'\"]*['\"][^>]*>(.*?)</[a-z0-9]+>",
                   re.IGNORECASE | re.DOTALL),
    ]
    for rex in region_res:
        for m in rex.finditer(html):
            if name_l in m.group(1).lower():
                return True
    # Also: brand name used as an alt/aria-label/title value on a logo-ish element.
    attr_re = re.compile(
        r"<[^>]*\b(?:class|id)\s*=\s*['\"][^'\"]*\b(?:logo|brand|wordmark)\b[^'\"]*['\"][^>]*\b(?:alt|aria-label|title)\s*=\s*['\"]([^'\"]+)['\"]",
        re.IGNORECASE)
    for m in attr_re.finditer(html):
        if name_l in m.group(1).lower():
            return True
    # And an <img> whose alt names the brand (a common logo pattern).
    img_alt_re = re.compile(r"<img\b[^>]*\balt\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
    for m in img_alt_re.finditer(html):
        if name_l in m.group(1).lower():
            return True
    return False


def _rejected_default_family(profile: BrandProfile) -> str:
    """The default font that extraction rejected (only when type was deferred).

    Returns the first family from ``fonts['site_stack']`` when the display source
    is 'logo-style' (i.e. a default was rejected). Empty when nothing to check.
    """
    fonts = profile.fonts or {}
    if fonts.get("display_source") != "logo-style":
        return ""
    stack = fonts.get("site_stack") or ""
    first = stack.split(",")[0].strip().strip('"').strip("'").strip()
    return first


def _family_used_as_display(html: str, html_lower: str, family: str) -> bool:
    """Is ``family`` used as a DISPLAY font (heading/display context) in output?

    Conservative: flags when the family appears in a font-family declaration that
    is in a display/heading context (a :root display token, or an h1/h2/h3/.hero/
    .display/.headline rule). Plain body usage elsewhere does not trip it.
    """
    fam = family.strip().lower()
    if not fam:
        return False
    for m in _FONT_FAMILY_RE.finditer(html):
        decl = m.group(1).lower()
        if fam not in decl:
            continue
        # Look back a small window for a display/heading context cue.
        start = m.start()
        window = html_lower[max(0, start - 200):start + len(m.group(0))]
        if _DISPLAY_CTX_RE.search(window):
            return True
    # Inline on a heading element: <h1 ... style="font-family: Family">
    inline_head_re = re.compile(
        r"<h[1-3]\b[^>]*style\s*=\s*['\"][^'\"]*font-family\s*:\s*([^;'\"]+)",
        re.IGNORECASE)
    for m in inline_head_re.finditer(html):
        if fam in m.group(1).lower():
            return True
    return False


_IMPORT_RE = re.compile(
    r"@import\s+(?:url\(\s*)?['\"]?([^'\")\s;]+)['\"]?\s*\)?\s*([^;]*);?", re.IGNORECASE)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_COLOR_LITERAL_RE = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|(?:rgba?|hsla?|oklch|oklab|color)\([^)]*\)", re.IGNORECASE)
_VAR_REF_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,\s*((?:[^()]|\([^()]*\))*))?\)")
_PSEUDO_RE = re.compile(r"::?[A-Za-z-]+(?:\((?:[^()]|\([^()]*\))*\))?")
_COMPOUND_RE = re.compile(r"(\*|[A-Za-z][\w-]*)|\.([\w-]+)|#([\w-]+)|\[\s*([\w:-]+)[^\]]*\]")
_GROUPING_AT_RULES = ("@media", "@supports", "@layer", "@container", "@document", "@scope")
_PRESENTATION_ATTRS = ("fill", "stroke", "color", "bgcolor", "stop-color")
_MAX_LINKED = 50


class _Element:
    __slots__ = ("tag", "id", "classes", "attrs")

    def __init__(self, tag: str, attrs: Dict[str, str]):
        self.tag = tag
        self.id = attrs.get("id", "")
        self.classes = set((attrs.get("class") or "").split())
        self.attrs = attrs


class _PageParser(HTMLParser):
    """Elements, <link> tags and <style> blocks of a page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: List[_Element] = []
        self.links: List[Dict[str, str]] = []
        self.styles: List[Tuple[Dict[str, str], str]] = []
        self._style: Optional[Dict[str, str]] = None
        self._buf: List[str] = []
        self._template = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() == "template":
            self._template += 1
        # Content of a <template>, and a hidden element, paint nothing on the page.
        hidden = "hidden" in a or re.search(r"display\s*:\s*none", a.get("style", ""), re.I)
        if not self._template and not hidden:
            self.elements.append(_Element(tag.lower(), a))
        if tag.lower() == "link":
            self.links.append(a)
        elif tag.lower() == "style":
            self._style, self._buf = a, []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self._style is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "template" and self._template:
            self._template -= 1
        if tag.lower() == "style" and self._style is not None:
            self.styles.append((self._style, "".join(self._buf)))
            self._style = None


def _media_off(media: str) -> bool:
    """A media query that never applies on a screen: "not all", or print
    and speech only."""
    m = re.sub(r"\s+", " ", (media or "").strip().lower())
    return m == "not all" or bool(re.match(r"^(?:only )?(?:print|speech)\b", m))


def _read_local(ref: str, rel_to: Path, base: Path, seen: set) -> Optional[Tuple[Path, str]]:
    ref = ref.strip().split("?")[0].split("#")[0]
    if not ref or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", ref, re.IGNORECASE):
        return None
    path = (base / ref.lstrip("/")) if ref.startswith("/") else (rel_to / ref)
    try:
        path = path.resolve()
        path.relative_to(base)   # outside the page's folder: not this page's CSS
    except (OSError, ValueError):
        return None
    if path in seen or len(seen) >= _MAX_LINKED or not path.is_file():
        return None
    seen.add(path)
    try:
        return path, path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def _page_stylesheets(page: "_PageParser", css_text: str, base_dir: Optional[Any],
                      root: Optional[Any] = None) -> List[str]:
    """The CSS that applies to the page, comments removed: inline <style>
    blocks, ``css_text``, and, when ``base_dir`` (the page's folder) is
    given, the local stylesheets the page links (rel="stylesheet", not
    alternate, not disabled, not print or media="not all") and the local
    files they import. Links resolve against the page's folder and must stay
    inside ``root`` (the project, default the page's folder); a leading "/"
    starts at ``root``. Remote URLs are not read."""
    page_dir = Path(base_dir).expanduser().resolve() if base_dir is not None else None
    base = Path(root).expanduser().resolve() if root is not None else page_dir
    seen: set = set()
    out: List[str] = []

    def add(text: str, rel_to: Optional[Path]) -> None:
        clean = _CSS_COMMENT_RE.sub("", text or "")
        out.append(clean)
        if base is None or rel_to is None:
            return
        for ref, media in _IMPORT_RE.findall(clean):
            if _media_off(media):
                continue
            got = _read_local(ref, rel_to, base, seen)
            if got:
                add(got[1], got[0].parent)

    for attrs, text in page.styles:
        if not _media_off(attrs.get("media", "")):
            add(text, page_dir)
    if css_text:
        add(css_text, page_dir)
    if base is not None and page_dir is not None:
        for link in page.links:
            rel = set((link.get("rel") or "").lower().split())
            if "stylesheet" not in rel or "alternate" in rel or "disabled" in link:
                continue
            if _media_off(link.get("media", "")):
                continue
            got = _read_local(link.get("href", ""), page_dir, base, seen)
            if got:
                add(got[1], got[0].parent)
    return out


def _style_rules(css: str) -> List[Tuple[str, str]]:
    """(selector, declarations) for every style rule. Grouping at-rules
    (@media, @supports, @layer, ...) are opened; other at-rules skipped."""
    rules: List[Tuple[str, str]] = []
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        prelude = css[i:j].rsplit(";", 1)[-1].rsplit("}", 1)[-1].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if prelude.startswith("@"):
            name = prelude.split(None, 1)[0].lower()
            if name in _GROUPING_AT_RULES and not (name == "@media" and _media_off(prelude[6:])):
                rules.extend(_style_rules(body))
        elif prelude:
            rules.append((prelude, body))
        i = k
    return rules


def _declarations(body: str) -> List[Tuple[str, str]]:
    out = []
    for decl in re.sub(r"\{[^{}]*\}", "", body).split(";"):
        if ":" in decl:
            prop, value = decl.split(":", 1)
            out.append((prop.strip().lower(), value.strip()))
    return out


def _expand(value: str, props: Dict[str, str], used: List[str], depth: int = 0) -> str:
    """``value`` with every var() replaced by what it resolves to; the
    custom properties followed are appended to ``used``."""
    if depth > 24:
        return value

    def sub(m: "re.Match[str]") -> str:
        name, fallback = m.group(1), m.group(2)
        if name in props:
            used.append(name)
            return _expand(props[name], props, used, depth + 1)
        return _expand(fallback or "", props, used, depth + 1)

    return _VAR_REF_RE.sub(sub, value)


def _paints(value: str, target: str, props: Dict[str, str]) -> Tuple[bool, List[str]]:
    used: List[str] = []
    expanded = _expand(value, props, used)
    hit = any(normalize_hex(c) == target for c in _COLOR_LITERAL_RE.findall(expanded))
    carried = [n for n in used if any(
        normalize_hex(c) == target
        for c in _COLOR_LITERAL_RE.findall(_expand(props[n], props, [])))]
    return hit, carried


def _compound_matches(compound: str, el: "_Element") -> bool:
    parts = _COMPOUND_RE.findall(compound)
    if not parts:
        return False
    for tag, cls, ident, attr in parts:
        if tag and tag != "*" and tag.lower() != el.tag:
            return False
        if cls and cls not in el.classes:
            return False
        if ident and ident != el.id:
            return False
        if attr and attr.lower() not in el.attrs:
            return False
    return True


def _selector_matches(selector: str, elements: List["_Element"]) -> bool:
    """True when some element of the page matches the selector's subject
    (its last compound). Pseudo-classes and pseudo-elements are dropped.
    :root (and html) is the page itself; a subject that is only a state
    pseudo-class, such as :focus-visible or :hover, names no element."""
    for single in selector.split(","):
        bare = _PSEUDO_RE.sub("", single).strip()
        compounds = [c for c in re.split(r"\s*[>+~]\s*|\s+", bare) if c]
        if not compounds:
            if re.fullmatch(r"\s*:root\s*", single) and elements:
                return True
            continue
        if any(_compound_matches(compounds[-1], el) for el in elements):
            return True
    return False


def _primary_use(page: "_PageParser", sheets: List[str],
                 primary: str) -> Tuple[bool, str, List[str]]:
    """Whether an element of the page is painted with the primary, where,
    and the custom properties that carried it. Counts a normal declaration
    (not a custom-property definition) in a rule whose selector matches an
    element, an inline style attribute, or a color attribute such as an SVG
    fill; the value may reach the primary through var() chains."""
    target = normalize_hex(primary)
    if not target:
        return False, "", []
    props = css_custom_properties("\n".join(sheets))
    for el in page.elements:
        for decl in (el.attrs.get("style") or "").split(";"):
            if ":" not in decl:
                continue
            prop, value = decl.split(":", 1)
            if prop.strip().startswith("--") or prop.strip().lower() == "content":
                continue
            hit, used = _paints(value, target, props)
            if hit:
                return True, "an inline style on <%s>" % el.tag, used
        for attr in _PRESENTATION_ATTRS:
            if normalize_hex(el.attrs.get(attr, "")) == target:
                return True, "the %s attribute of <%s>" % (attr, el.tag), []
    for sheet in sheets:
        for selector, body in _style_rules(sheet):
            for prop, value in _declarations(body):
                if prop.startswith("--") or prop == "content":
                    continue   # a definition, or a string that paints nothing
                hit, used = _paints(value, target, props)
                if hit and _selector_matches(selector, page.elements):
                    return True, "%s { %s }" % (selector.strip(), prop), used
    return False, "", []


def score_brand_fidelity(html_text: str, profile: BrandProfile, css_text: str = "",
                         base_dir: Optional[Any] = None,
                         root: Optional[Any] = None) -> Dict[str, Any]:
    """Score how faithfully ``html_text`` honors ``profile``. Deterministic.

    The page is read with its styles: inline ``<style>``, ``css_text``, and,
    when ``base_dir`` (the page's folder) is given, every local stylesheet the
    page links or imports. Custom properties are resolved, so a token-driven
    page that paints the primary through ``var(--brand-primary)`` passes.
    ``root`` is the project folder: links resolve against the page's folder
    and may reach anywhere inside ``root``, such as ``../css/`` from ``en/``.

    Returns ``{score, passed, findings}`` where findings is a list of
    ``{check, severity, ok, detail}``. The hard floor (rule 7): if the profile
    has a primary and the output is missing that primary OR missing the logo,
    ``passed`` is False regardless of the numeric score.
    """
    html = _HTML_COMMENT_RE.sub("", html_text or "")
    html_lower = html.lower()
    page = _PageParser()
    try:
        page.feed(html)
        page.close()
    except Exception:  # a malformed page still gets scored on what parsed
        pass
    sheets = _page_stylesheets(page, css_text, base_dir, root)
    corpus = "\n".join([html] + sheets)
    corpus_lower = corpus.lower()
    findings: List[Dict[str, Any]] = []
    earned = 0

    has_primary = bool((profile.primary or "").strip())

    # (a) PRIMARY USED -------------------------------------------------------
    # Counted only where an element of the page is painted with it: a matched
    # rule, an inline style or a color attribute. A stylesheet that only
    # defines the primary, a comment, or a selector nothing matches does not count.
    primary_ok, where, carriers = (False, "", [])
    if has_primary:
        primary_ok, where, carriers = _primary_use(page, sheets, profile.primary)
    if has_primary:
        via = (" through %s" % " then ".join(dict.fromkeys(carriers))) if carriers else ""
        findings.append({
            "check": "primary_used",
            "severity": "critical",
            "ok": primary_ok,
            "detail": ("Brand primary %s paints the page at %s%s." % (profile.primary, where, via))
            if primary_ok else
            ("Brand primary %s paints no element of the page. Use it in a rule whose selector "
             "matches an element, an inline style or a color attribute (a definition alone "
             "does not count); if the page links its CSS, pass the page's folder as "
             "base_dir." % profile.primary),
        })
        if primary_ok:
            earned += _CHECK_WEIGHTS["primary_used"]
    else:
        # No brand primary to honor: this check is not applicable; credit it so a
        # brand-less profile isn't penalized for something it never had.
        earned += _CHECK_WEIGHTS["primary_used"]
        findings.append({
            "check": "primary_used", "severity": "critical", "ok": True,
            "detail": "No brand primary captured; primary-color check not applicable.",
        })

    # (b) LOGO PRESENT -------------------------------------------------------
    logo_url = (profile.logo or {}).get("url") or ""
    has_logo_anchor = bool(logo_url or (profile.name or "").strip())
    logo_ok = bool(has_logo_anchor and _logo_present(html, html_lower, profile))
    if has_logo_anchor:
        findings.append({
            "check": "logo_present",
            "severity": "critical",
            "ok": logo_ok,
            "detail": "Brand logo / wordmark is present in a header/logo context."
            if logo_ok else
            "Brand logo / wordmark is MISSING -- carry the logo url or the brand "
            "name in a header/nav/logo context.",
        })
        if logo_ok:
            earned += _CHECK_WEIGHTS["logo_present"]
    else:
        earned += _CHECK_WEIGHTS["logo_present"]
        findings.append({
            "check": "logo_present", "severity": "critical", "ok": True,
            "detail": "No brand logo or name captured; logo check not applicable.",
        })

    # (c) TYPE MATCHES -------------------------------------------------------
    rejected = _rejected_default_family(profile)
    if rejected:
        drift = _family_used_as_display(corpus, corpus_lower, rejected)
        type_ok = not drift
        findings.append({
            "check": "type_matches",
            "severity": "high",
            "ok": type_ok,
            "detail": ("Output does not fall back to the rejected default display "
                       "font '%s'." % rejected) if type_ok else
            ("Output uses the REJECTED default font '%s' as a display face -- pick "
             "type matching the logo style instead." % rejected),
        })
        if type_ok:
            earned += _CHECK_WEIGHTS["type_matches"]
    else:
        # Type was kept (distinctive) or no site stack to reject: not applicable.
        earned += _CHECK_WEIGHTS["type_matches"]
        findings.append({
            "check": "type_matches", "severity": "high", "ok": True,
            "detail": "No rejected default font to guard against; type check not "
                      "applicable.",
        })

    # (d) NO HOUSE-STYLE DRIFT ----------------------------------------------
    primary_norm = _norm_hex(profile.primary)
    leaked: List[str] = []
    for hx, label in HOUSE_COLORS.items():
        if hx == primary_norm:
            continue  # the brand's primary legitimately equals a house color
        if _hex_present(corpus_lower, hx):
            leaked.append("%s %s" % (hx, label))
    drift_ok = not leaked
    findings.append({
        "check": "no_house_drift",
        "severity": "high",
        "ok": drift_ok,
        "detail": "No engine house colors leaked into the output."
        if drift_ok else
        ("Engine house color(s) leaked in: %s -- the brand primary %s must drive "
         "the palette, not the engine's style." % ("; ".join(leaked),
                                                    profile.primary or "n/a")),
    })
    if drift_ok:
        earned += _CHECK_WEIGHTS["no_house_drift"]

    score = max(0, min(100, int(round(earned))))

    # Hard floor (rule 7): if a profile with a primary exists and the output drops
    # the primary OR the logo, it FAILS outright -- no matter the numeric score.
    passed = not (has_primary and (not primary_ok or not logo_ok))

    return {"score": score, "passed": passed, "findings": findings}


# --- Imagery presence (richness) -- a SIBLING to brand fidelity --------------
# A full page must carry REAL imagery: a raster <img>/<picture>/<video>, a real
# background photo, or a SUBSTANTIAL inline SVG illustration. Icon-sized SVGs
# (Lucide/Heroicons-style, sub-100px / tiny viewBox) do NOT count -- a wall of
# cards with only tiny icons is still a text-wall. This is deliberately NOT folded
# into score_brand_fidelity's weighted score: a page can honor the brand's
# color/logo/type perfectly and still ship as a text-wall. Imagery presence is
# *richness*, not brand-honoring -- keep the two scores honest by keeping them
# separate. (The data/anti-patterns.json `imagery-mandatory-missing` rule is the
# live linter backstop; this is the structural check P7 wiring will call.)

_FULLPAGE_RE = re.compile(r"<(?:body|html)\b", re.IGNORECASE)
_REAL_IMG_RE = re.compile(r"<(?:img|picture|video)\b", re.IGNORECASE)
_REAL_BG_RE = re.compile(
    r"url\(\s*['\"]?[^)'\"]+\.(?:png|jpe?g|webp|avif|gif)", re.IGNORECASE)
_SVG_OPEN_RE = re.compile(r"<svg\b[^>]*>", re.IGNORECASE)
_SVG_DIM_RE = re.compile(
    r"\s(?:width|height)\s*=\s*['\"]?\s*([1-9]\d{2,})", re.IGNORECASE)
_SVG_VIEWBOX_RE = re.compile(
    r"viewBox\s*=\s*['\"]\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)", re.IGNORECASE)
_ICON_PX = 100  # below this an inline SVG reads as an icon, not as imagery


def _svg_is_illustration(open_tag: str) -> bool:
    """True if an <svg> open tag is illustration-scale (>= _ICON_PX), not an icon."""
    if _SVG_DIM_RE.search(open_tag):
        return True
    m = _SVG_VIEWBOX_RE.search(open_tag)
    if m:
        try:
            return float(m.group(1)) >= _ICON_PX or float(m.group(2)) >= _ICON_PX
        except ValueError:
            return False
    return False


def score_imagery(html_text: str) -> Dict[str, Any]:
    """Does a FULL page carry real imagery, or is it a text-wall? Deterministic.

    Returns ``{ok, kind, score, detail}`` with ``kind`` in {fragment, image,
    bg-photo, illustration-svg, icons-only, none}. Component fragments (no
    <body>/<html>) are exempt (ok=True) -- not every partial needs art. Icons are
    NOT imagery: a page whose only visuals are sub-100px SVGs fails.
    """
    html = html_text or ""
    if not _FULLPAGE_RE.search(html):
        return {"ok": True, "kind": "fragment", "score": 100,
                "detail": "Component fragment (no <body>); imagery check not applicable."}
    if _REAL_IMG_RE.search(html):
        return {"ok": True, "kind": "image", "score": 100,
                "detail": "Page carries a real image / picture / video."}
    if _REAL_BG_RE.search(html):
        return {"ok": True, "kind": "bg-photo", "score": 100,
                "detail": "Page carries a real background photo."}
    svgs = _SVG_OPEN_RE.findall(html)
    if any(_svg_is_illustration(tag) for tag in svgs):
        return {"ok": True, "kind": "illustration-svg", "score": 100,
                "detail": "Page carries a substantial inline SVG illustration."}
    if svgs:
        return {"ok": False, "kind": "icons-only", "score": 0,
                "detail": ("Only icon-sized inline SVGs (< %dpx) and no real image -- a "
                           "wall of cards with tiny icons still reads as a text-wall. Add "
                           "real imagery (client assets first, then curated stock)." % _ICON_PX)}
    return {"ok": False, "kind": "none", "score": 0,
            "detail": ("Page ships zero imagery -- no image, picture/video, real background "
                       "photo, or illustration. The biggest richness failure.")}
