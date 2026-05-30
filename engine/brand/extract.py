"""Brand extraction -> a travelling brand profile (brand.md + brand.json).

When ux-skill redesigns an EXISTING site, it must honor that site's identity
instead of imposing the engine's house style. This module turns raw brand
signals captured from the live page into a structured BrandProfile that:

  1. travels through the pipeline (discover -> synthesize -> generate) as a hard
     anchor, so output uses THEIR logo + colors + type, and
  2. is scored against by the linter/rating (brand fidelity), so an output that
     drifts off-brand cannot pass.

Two hard-won rules (see references/process/brand-extraction.md):
  * COLOR comes from the LOGO, not the most-painted CSS. The logo's dominant
    non-neutral color is the primary; CSS chrome colors are secondary.
  * TYPE comes from the LOGO's letterform style, and known DEFAULT fonts
    (Roboto/Inter/system-ui/...) are rejected rather than preserved -- a default
    is the absence of a brand choice.

Signal capture (reading the live DOM, sampling logo pixels, reading the logo's
type style) is I/O + vision done by the caller. This module is the deterministic
normalize + render half: signals dict -> BrandProfile -> markdown. Python 3.9+.
"""
from __future__ import annotations

import colorsys
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# Known default / theme fonts: their presence signals the ABSENCE of a type
# choice, so they must not be preserved as the brand display face (rule 4).
_DEFAULT_FONTS = {
    "roboto", "roboto flex", "inter", "arial", "helvetica", "helvetica neue",
    "system-ui", "-apple-system", "blinkmacsystemfont", "open sans", "lato",
    "segoe ui", "source sans pro", "source sans 3", "noto sans", "pt sans",
    "verdana", "tahoma", "sans-serif", "serif",
}

# The engine's own house colors (clay/blurple). They must NEVER leak into a
# client brand, so build_profile always lists the ones that are not the brand's
# primary under `colors_to_avoid`. Duplicated here as a literal (not imported
# from fidelity.py) on purpose: fidelity.py imports BrandProfile from this
# module, so importing back would be a circular import. These are a fixed spec
# value -- the same two hexes fidelity's HOUSE_COLORS gates against.
_ENGINE_HOUSE_HEXES = ["#cc785c", "#5e6ad2"]


def _hex_to_hsv(hexstr: Optional[str]):
    if not isinstance(hexstr, str):
        return None
    s = hexstr.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        return None
    try:
        r = int(s[0:2], 16) / 255.0
        g = int(s[2:4], 16) / 255.0
        b = int(s[4:6], 16) / 255.0
    except ValueError:
        return None
    h, sat, val = colorsys.rgb_to_hsv(r, g, b)
    return (h * 360.0, sat, val)


def hue_family(hexstr: str) -> str:
    """Coarse hue family for a hex color (neutral when desaturated)."""
    hsv = _hex_to_hsv(hexstr)
    if not hsv:
        return "unknown"
    h, s, v = hsv
    if s < 0.12 or v < 0.06:
        return "neutral"
    bins = [(15, "red"), (45, "orange"), (70, "yellow"), (160, "green"),
            (200, "teal"), (240, "blue"), (290, "violet"), (340, "magenta"), (360, "red")]
    for hi, name in bins:
        if h < hi:
            return name
    return "red"


def _font_name(family: Optional[str]) -> str:
    """First real family from a CSS font-family stack."""
    if not family:
        return ""
    first = family.split(",")[0].strip().strip('"').strip("'").strip()
    return "" if first.lower() in {"system-ui", "ui-sans-serif", "-apple-system"} else first


def _is_default_font(name: str) -> bool:
    return bool(name) and name.lower() in _DEFAULT_FONTS


def _hexes(raw) -> List[str]:
    out: List[str] = []
    for c in (raw or []):
        hx = c.get("hex") if isinstance(c, dict) else c
        if isinstance(hx, str) and _hex_to_hsv(hx) and hx not in out:
            out.append(hx)
    return out


@dataclass
class BrandProfile:
    source: str = ""
    name: str = ""
    tagline: str = ""                                          # standard frontmatter (req in the open spec)
    language: str = "en"                                       # standard frontmatter
    logo: Dict[str, Any] = field(default_factory=dict)         # {url, alt}
    logo_style: str = ""                                       # vision read of the wordmark
    primary: str = ""                                          # from LOGO pixels (rule 3)
    primary_family: str = ""
    primary_source: str = ""                                   # "logo" | "css" | "brand-md"
    secondary: List[str] = field(default_factory=list)
    colors_to_avoid: List[str] = field(default_factory=list)   # house colors + signals; spec "colors to avoid"
    fonts: Dict[str, str] = field(default_factory=dict)        # display/body/type_personality/display_source
    photography: Dict[str, Any] = field(default_factory=dict)  # {mood[list], subjects[list], avoid[list]}
    style_keywords: List[str] = field(default_factory=list)    # spec Visual>Style design keywords
    tonal: Dict[str, Any] = field(default_factory=dict)        # {rules[list], we_say[list], we_never_say[list]}
    imagery: List[str] = field(default_factory=list)
    voice: str = ""
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_profile(signals: Dict[str, Any]) -> BrandProfile:
    """Normalize captured signals into a BrandProfile. Deterministic.

    Signal keys (all optional): source/url, name, logo{url/src,alt},
    logo_colors[{hex,score}] (sampled from the logo image), brand_colors/colors
    (from CSS), logo_type_style/logo_style (vision read of the wordmark),
    fonts{display,h1,h2,body}, imagery[url], voice.
    """
    p = BrandProfile()
    p.source = signals.get("source", "") or signals.get("url", "")
    p.notes = []

    logo = signals.get("logo") or {}
    if logo:
        p.logo = {"url": logo.get("url") or logo.get("src") or "", "alt": logo.get("alt") or ""}

    name = signals.get("name") or ""
    if not name and p.logo.get("alt"):
        name = p.logo["alt"]
    if name:
        name = name.replace("logo", "").replace("Logo", "").strip(" -_|")
        p.name = " ".join(w.capitalize() if w.islower() else w for w in name.split())

    # --- Color: the LOGO wins; CSS is supporting (rule 3) ---
    logo_hexes = _hexes(signals.get("logo_colors"))
    css_hexes = _hexes(signals.get("brand_colors") or signals.get("colors"))
    primary = (next((h for h in logo_hexes if hue_family(h) != "neutral"), None)
               or next((h for h in css_hexes if hue_family(h) != "neutral"), None)
               or (logo_hexes[0] if logo_hexes else (css_hexes[0] if css_hexes else "")))
    p.primary = primary
    p.primary_family = hue_family(primary) if primary else ""
    p.primary_source = "logo" if primary in logo_hexes else ("css" if primary else "")
    seen = set()
    p.secondary = [h for h in (logo_hexes + css_hexes)
                   if h != primary and not (h in seen or seen.add(h))][:4]
    if css_hexes and logo_hexes and p.primary_source == "logo":
        p.notes.append("Primary taken from the logo, not the most-painted CSS color.")

    # --- Type: the LOGO style drives it; default fonts are rejected (rule 4) ---
    p.logo_style = signals.get("logo_type_style") or signals.get("logo_style") or ""
    fonts = signals.get("fonts") or {}
    site_display = _font_name(fonts.get("display") or fonts.get("h1") or fonts.get("h2"))
    site_body = _font_name(fonts.get("body"))
    if site_display and not _is_default_font(site_display):
        display, display_source = site_display, "site"
    else:
        display, display_source = "", "logo-style"
        if site_display:
            p.notes.append("Rejected default site font '%s'; pick type matching the logo style." % site_display)
    body = site_body if (site_body and not _is_default_font(site_body)) else ""
    p.fonts = {
        "display": display,
        "body": body,
        "type_personality": p.logo_style,      # what generation matches when display is deferred
        "display_source": display_source,        # "site" | "logo-style"
        "site_stack": fonts.get("h1") or fonts.get("body") or "",
    }

    p.imagery = list(signals.get("imagery") or [])
    p.voice = signals.get("voice", "")

    # --- Standard-spec fields the engine can honestly fill (rest stay empty) ---
    p.tagline = signals.get("tagline", "") or ""
    p.language = signals.get("language") or "en"

    # colors_to_avoid: ALWAYS list the engine's house colors that are not this
    # brand's primary (so the engine's own style can never leak in), then append
    # any caller-supplied avoid colors. Deterministic, dedup'd in order.
    avoid: List[str] = []

    def _avoid(hx: str) -> None:
        if isinstance(hx, str) and hx and hx not in avoid:
            avoid.append(hx)

    for house in _ENGINE_HOUSE_HEXES:
        if house != primary:
            _avoid(house)
    for hx in _hexes(signals.get("colors_to_avoid")):
        _avoid(hx)
    p.colors_to_avoid = avoid

    # photography.mood: derived from the same voice + logo-style descriptor words
    # image_search_terms mines (deterministic token/stopword pass). subjects/avoid
    # are author-only -- fill from signals when present, else leave empty.
    photo_signals = signals.get("photography") or {}
    p.photography = {
        "mood": _descriptor_words(p.voice, p.logo_style),
        "subjects": list(photo_signals.get("subjects") or signals.get("photography_subjects") or []),
        "avoid": list(photo_signals.get("avoid") or signals.get("photography_avoid") or []),
    }

    # style_keywords: logo-style words (filtered, dedup) + any caller-supplied.
    style_kw: List[str] = list(_descriptor_words("", p.logo_style))
    for kw in (signals.get("style_keywords") or []):
        kw = (kw or "").strip() if isinstance(kw, str) else ""
        if kw and kw not in style_kw:
            style_kw.append(kw)
    p.style_keywords = style_kw

    # tonal: author-only voice rules -- carry through from signals, else empty.
    tonal_signals = signals.get("tonal") or {}
    if tonal_signals:
        p.tonal = {
            "rules": list(tonal_signals.get("rules") or []),
            "we_say": list(tonal_signals.get("we_say") or []),
            "we_never_say": list(tonal_signals.get("we_never_say") or []),
        }
    else:
        p.tonal = {}

    return p


# A section the engine cannot honestly extract still gets its H3 header (so the
# file is a valid, complete-shaped standard brand.md) with this placeholder.
_NOT_EXTRACTED = "(not extracted -- author or inherit)"


def render_md(p: BrandProfile) -> str:
    """Render a BrandProfile as a VALID open-standard brand.md (thebrandmd/brand.md).

    YAML frontmatter (name/tagline/version/language[+type]) -> ``# {name}`` -> a
    one-line brand-fidelity-gate anchor warning -> the three H2 layers (Strategy,
    Voice, Visual) each with its H3 sections. The VISUAL layer is the rich one
    (this is the extraction engine's strength); Strategy/Voice emit their headers
    and fill only what extraction can honestly know, with a short placeholder for
    sections that need a human author. Deterministic: same profile -> same bytes.
    """
    name = p.name or "untitled"
    lines: List[str] = []

    # --- YAML frontmatter (simple, dependency-light; matches our parser) -------
    lines += [
        "---",
        "name: %s" % name,
        "tagline: %s" % (p.tagline or ""),
        "version: 1",
        "language: %s" % (p.language or "en"),
        "type: master",
        "---",
        "",
        "# %s" % name,
        "",
        # SINGLE-LINE anchor warning. MUST keep both substrings so it stays our
        # enforcement note (tests + maintainers grep for them).
        ("> Brand anchor: generation MUST use this brand's logo, primary color, and "
         "type; drifting to a house style fails the brand-fidelity gate."),
        "",
    ]

    # --- ## Strategy -----------------------------------------------------------
    overview = "%s%s" % (
        ("%s. " % name) if p.name else "",
        ("Source: %s." % p.source) if p.source else "Extracted brand anchor.",
    )
    lines += [
        "## Strategy",
        "",
        "### Overview",
        overview.strip(),
        "",
        "### Positioning",
        _NOT_EXTRACTED,
        "",
        "### Personality",
        _NOT_EXTRACTED,
        "",
        "### Promise",
        _NOT_EXTRACTED,
        "",
        "### Guardrails",
        _NOT_EXTRACTED,
        "",
    ]

    # --- ## Voice --------------------------------------------------------------
    identity = p.voice or _NOT_EXTRACTED
    tagline_block = ("- %s" % p.tagline) if p.tagline else _NOT_EXTRACTED
    lines += [
        "## Voice",
        "",
        "### Identity",
        identity,
        "",
        "### Tagline & Slogans",
        tagline_block,
        "",
        "### Message Pillars",
        _NOT_EXTRACTED,
        "",
        "### Phrases",
        _NOT_EXTRACTED,
        "",
        "### Tonal Rules",
    ]
    tonal = p.tonal or {}
    rules = list(tonal.get("rules") or [])
    we_say = list(tonal.get("we_say") or [])
    we_never = list(tonal.get("we_never_say") or [])
    if rules:
        lines += [""]
        lines += ["- %s" % r for r in rules]
    if we_say or we_never:
        lines += [
            "",
            "| We Say | We Never Say |",
            "| --- | --- |",
        ]
        for i in range(max(len(we_say), len(we_never))):
            left = we_say[i] if i < len(we_say) else ""
            right = we_never[i] if i < len(we_never) else ""
            lines += ["| %s | %s |" % (left, right)]
    if not (rules or we_say or we_never):
        lines += ["", _NOT_EXTRACTED]
    lines += [""]

    # --- ## Visual (the rich, extraction-driven layer) -------------------------
    lines += [
        "## Visual",
        "",
        "### Colors",
        "",
    ]
    # Primary FIRST (round-trip contract: first hex in this section -> primary).
    if p.primary:
        lines += ["- **Primary:** `%s` -- hue %s, source %s. Drives the palette and CTA."
                  % (p.primary, p.primary_family or "n/a", p.primary_source or "n/a")]
    else:
        lines += ["- **Primary:** (none captured)"]
    # Secondary lines NEXT (each carries its hex; round-trip -> secondary list).
    if p.secondary:
        for hx in p.secondary:
            lines += ["- **Secondary:** `%s` -- hue %s." % (hx, hue_family(hx))]
    else:
        lines += ["- **Secondary:** (none captured)"]
    # Colors to avoid LAST. The word "avoid" on the line is the round-trip marker
    # that flips every hex from here on into colors_to_avoid (never secondary).
    if p.colors_to_avoid:
        avoid_hexes = " ".join("`%s`" % h for h in p.colors_to_avoid)
        lines += ["- **Colors to avoid:** %s -- engine house colors / off-brand; never use these."
                  % avoid_hexes]
    else:
        lines += ["- **Colors to avoid:** (none)"]
    lines += [""]

    # Typography. A deferred display/body font uses the _NOT_EXTRACTED sentinel in
    # the value slot (with the logo-style guidance as trailing context) so the
    # parser's placeholder guard skips it -- no real font name is invented.
    lines += ["### Typography", ""]
    if p.fonts.get("display"):
        lines += ["- **Display:** %s -- weight bold. Kept; distinctive, not a default."
                  % p.fonts["display"]]
    else:
        lines += ["- **Display:** %s -- weight bold. Match the logo style: %s "
                  "(the site font was a default and was rejected)."
                  % (_NOT_EXTRACTED, p.fonts.get("type_personality") or p.logo_style or "n/a")]
    if p.fonts.get("body"):
        lines += ["- **Body:** %s -- weight regular. Usage: body copy." % p.fonts["body"]]
    else:
        lines += ["- **Body:** %s -- weight regular. A clean, readable companion to "
                  "the display face." % _NOT_EXTRACTED]
    lines += ["- **Mono:** a neutral monospace -- weight regular. Usage: code / data."]
    lines += ["", "Logo type personality: %s." % (p.logo_style or "n/a"), ""]

    # Photography.
    photo = p.photography or {}
    mood = list(photo.get("mood") or [])
    subjects = list(photo.get("subjects") or [])
    p_avoid = list(photo.get("avoid") or [])
    lines += ["### Photography", ""]
    lines += ["- **Mood:** %s" % (", ".join(mood) if mood else _NOT_EXTRACTED)]
    lines += ["- **Subjects:** %s" % (", ".join(subjects) if subjects else _NOT_EXTRACTED)]
    lines += ["- **Avoid:** %s" % (", ".join(p_avoid) if p_avoid
                                   else "random/generic stock, AI-slop clutter")]
    lines += [""]

    # Style.
    lines += ["### Style", ""]
    if p.style_keywords:
        lines += ["- **Design keywords:** %s" % ", ".join(p.style_keywords)]
    else:
        lines += ["- **Design keywords:** %s" % _NOT_EXTRACTED]
    lines += ["- **Reference brands:** %s" % _NOT_EXTRACTED]
    lines += ["- **Direction:** primary from the logo, type from the logo style; "
              "let the client level up without inheriting a house style."]
    lines += [""]

    return "\n".join(lines)


# --- INPUT side: parse a standard brand.md (thebrandmd/brand.md) -------------
# The engine is dependency-light, so the YAML frontmatter is read with a simple
# line parse (no yaml dep) and the body is split by H2/H3 headers with regex.
_HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
_H2_SPLIT_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_H3_SPLIT_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)


def _split_sections(body: str, header_re) -> Dict[str, str]:
    """Map header-title (lowercased) -> the text under it, up to the next header.

    Last-writer-wins on duplicate titles. Titles are normalized to lowercase so
    lookups are case-insensitive. The text before the first header is dropped.
    """
    out: Dict[str, str] = {}
    matches = list(header_re.finditer(body))
    for i, m in enumerate(matches):
        title = m.group(1).strip().lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out[title] = body[start:end]
    return out


def _parse_frontmatter(text: str) -> Dict[str, str]:
    """Read a leading ``---`` ... ``---`` YAML block as flat key->value strings.

    Simple line parse (``key: value``); no yaml dependency. Values are stripped
    of surrounding quotes. Returns {} when there is no frontmatter block.
    """
    fm: Dict[str, str] = {}
    s = text.lstrip("﻿").lstrip()
    if not s.startswith("---"):
        return fm
    lines = s.splitlines()
    if not lines or lines[0].strip() != "---":
        return fm
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip().strip('"').strip("'").strip()
        if key:
            fm[key] = value
    return fm


def _hexes_in(text: str) -> List[str]:
    """All hex colors in ``text``, lowercased and expanded to 6 digits, in order."""
    out: List[str] = []
    for raw in _HEX_RE.findall(text):
        s = raw.lstrip("#").lower()
        if len(s) == 3:
            s = "".join(c * 2 for c in s)
        hx = "#" + s
        out.append(hx)
    return out


def _strip_md_emphasis(s: str) -> str:
    """Drop list/markdown chrome from a one-line value (-, *, **bold**, `code`)."""
    s = s.strip().lstrip("-*").strip()
    return s.replace("**", "").replace("`", "").strip()


def parse_brand_md(text: str) -> BrandProfile:
    """Parse an open-standard brand.md string into a BrandProfile (the INPUT side).

    Robust to sparse / missing sections -- returns what is present and never
    raises. Reads the YAML frontmatter (name/tagline/language/version) and the
    ``## Visual`` layer (Colors -> primary/secondary/colors_to_avoid, Typography
    -> fonts.display/body, Photography/Style -> photography/style_keywords) plus
    ``## Voice`` > ``### Tonal Rules`` -> tonal. ``primary_source`` is set to
    "brand-md" to mark the provenance. Deterministic.
    """
    text = text or ""
    p = BrandProfile()
    p.primary_source = "brand-md"

    fm = _parse_frontmatter(text)
    p.name = fm.get("name", "") or ""
    p.tagline = fm.get("tagline", "") or ""
    p.language = fm.get("language") or "en"
    p.source = "brand-md"

    h2 = _split_sections(text, _H2_SPLIT_RE)

    # --- Visual layer (the rich one) ---
    visual = h2.get("visual", "")
    vis_h3 = _split_sections(visual, _H3_SPLIT_RE) if visual else {}

    # Colors: first hex -> primary; hexes before an "avoid" line -> secondary;
    # every hex on/after the first line containing "avoid" -> colors_to_avoid.
    colors_text = vis_h3.get("colors", "")
    if colors_text:
        primary = ""
        secondary: List[str] = []
        avoid: List[str] = []
        in_avoid = False
        for line in colors_text.splitlines():
            if "avoid" in line.lower():
                in_avoid = True
            for hx in _hexes_in(line):
                if in_avoid:
                    if hx not in avoid:
                        avoid.append(hx)
                elif not primary:
                    primary = hx
                elif hx != primary and hx not in secondary:
                    secondary.append(hx)
        p.primary = primary
        p.primary_family = hue_family(primary) if primary else ""
        p.secondary = secondary
        p.colors_to_avoid = avoid

    # Typography: display font (rejected if a known default), body font.
    typ_text = vis_h3.get("typography", "")
    if typ_text:
        display = ""
        body = ""
        for line in typ_text.splitlines():
            low = line.lower()
            value = _font_value_from_line(line)
            # Skip a missing value, a placeholder ("(not extracted ...)"), or a
            # known default font -- none of those is a real brand display face.
            if not value or value.startswith("(") or _is_default_font(value):
                continue
            if "display" in low and not display:
                display = value
            elif "body" in low and not body:
                body = value
        fonts: Dict[str, str] = {}
        if display:
            fonts["display"] = display
        if body:
            fonts["body"] = body
        if fonts:
            p.fonts = fonts

    # Photography: mood / subjects / avoid lists from the labelled lines.
    photo_text = vis_h3.get("photography", "")
    if photo_text:
        photo: Dict[str, Any] = {}
        mood = _csv_after_label(photo_text, "mood")
        subjects = _csv_after_label(photo_text, "subjects")
        p_avoid = _csv_after_label(photo_text, "avoid")
        if mood:
            photo["mood"] = mood
        if subjects:
            photo["subjects"] = subjects
        if p_avoid:
            photo["avoid"] = p_avoid
        if photo:
            p.photography = photo

    # Style: design keywords.
    style_text = vis_h3.get("style", "")
    if style_text:
        kws = _csv_after_label(style_text, "design keywords")
        if not kws:
            kws = _csv_after_label(style_text, "keywords")
        if kws:
            p.style_keywords = kws

    # --- Voice layer -> tonal rules + We Say / We Never Say table ---
    voice = h2.get("voice", "")
    if voice:
        voice_h3 = _split_sections(voice, _H3_SPLIT_RE)
        # Identity feeds our `voice` field when present.
        identity = (voice_h3.get("identity", "") or "").strip()
        if identity and identity != _NOT_EXTRACTED:
            p.voice = identity
        tonal_text = voice_h3.get("tonal rules", "")
        if tonal_text:
            tonal = _parse_tonal(tonal_text)
            if tonal:
                p.tonal = tonal

    return p


def _font_value_from_line(line: str) -> str:
    """Extract the font name from a Typography bullet like ``- **Display:** X -- ...``.

    Takes the text after the first colon (or the whole bullet when there is no
    label), then the part before a ``--`` qualifier, stripped of markdown chrome.
    Returns the first family from a comma stack. Empty when nothing usable.
    """
    s = line
    if ":" in s:
        s = s.split(":", 1)[1]
    # Cut a trailing ``-- usage`` qualifier (en/em dash rendered as "--").
    s = re.split(r"\s--\s|\s—\s|\s–\s", s)[0]
    s = _strip_md_emphasis(s)
    # First family from a CSS-style stack.
    s = s.split(",")[0].strip().strip('"').strip("'").strip()
    return s


def _csv_after_label(text: str, label: str) -> List[str]:
    """Comma-split values from the first line whose label matches ``label``.

    Matches a bullet like ``- **Mood:** a, b, c`` (label case-insensitive).
    Drops a ``(not extracted ...)`` / ``(none)`` placeholder. Order preserved.
    """
    label_l = label.lower()
    for line in text.splitlines():
        low = line.lower()
        if label_l not in low:
            continue
        if ":" not in line:
            continue
        value = line.split(":", 1)[1]
        value = _strip_md_emphasis(value)
        if not value or value.lower().startswith("(not extracted") or value.lower() == "(none)":
            return []
        parts = [v.strip() for v in value.split(",")]
        return [v for v in parts if v]
    return []


def _parse_tonal(text: str) -> Dict[str, Any]:
    """Parse a Tonal Rules block: bullet rules + a We Say | We Never Say table."""
    rules: List[str] = []
    we_say: List[str] = []
    we_never: List[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) < 2:
                continue
            left, right = cells[0], cells[1]
            low_left = left.lower()
            # Skip the header row and the --- separator row.
            if low_left in ("we say", "") and right.lower() in ("we never say", ""):
                continue
            if set(left) <= set("-: ") and set(right) <= set("-: "):
                continue
            if left:
                we_say.append(left)
            if right:
                we_never.append(right)
        elif stripped.startswith(("-", "*")):
            rule = _strip_md_emphasis(stripped)
            if rule and not rule.lower().startswith("(not extracted"):
                rules.append(rule)
    out: Dict[str, Any] = {}
    if rules:
        out["rules"] = rules
    if we_say:
        out["we_say"] = we_say
    if we_never:
        out["we_never_say"] = we_never
    return out


# Voice words too generic to seed an image search with.
_VOICE_STOP = {
    "the", "and", "for", "with", "our", "your", "this", "that", "are", "but",
    "not", "you", "all", "can", "out", "use", "who", "how", "why", "its",
    "a", "an", "of", "to", "is", "it", "we", "be", "or", "on", "in", "as",
}
_TOKEN_RE_VOICE = re.compile(r"[a-z]+")
# Type-jargon from a logo-style read that does not help an IMAGE search.
_TYPE_NOISE = {
    "sans", "serif", "wordmark", "letterform", "letterforms", "typeface",
    "font", "type", "display", "weight", "italic", "uppercase", "lowercase",
    "grotesk", "grotesque", "slab", "mono",
}


def _descriptor_words(*sources: str) -> List[str]:
    """Mood/keyword words mined from voice + logo-style text. Deterministic.

    Same token/stopword pass image_search_terms uses for its brand-led terms:
    lowercase word tokens, drop generic voice stopwords and type jargon, keep
    words longer than 2 chars, dedup in first-seen order. Used to fill
    photography.mood and style_keywords from the descriptor text the caller
    captured (the logo's letterform personality is brand voice expressed as type).
    """
    src = " ".join((s or "") for s in sources).strip().lower()
    out: List[str] = []
    for word in _TOKEN_RE_VOICE.findall(src):
        if (word not in _VOICE_STOP and word not in _TYPE_NOISE
                and len(word) > 2 and word not in out):
            out.append(word)
    return out


# Hue family -> a color word usable in an image search query.
_FAMILY_SEARCH_WORD = {
    "red": "warm red", "orange": "warm amber", "yellow": "golden",
    "green": "deep green", "teal": "teal", "blue": "cool blue",
    "violet": "violet", "magenta": "magenta", "neutral": "monochrome",
}

# 7-axis temperature -> mood words for curated stock search. Each axis contributes
# at most one word, chosen by whether the axis reads low or high. Deterministic.
_AXIS_SEARCH_WORDS = {
    "warmth":           ("cool toned", "warm toned"),
    "contrast":         ("soft light", "high contrast"),
    "density":          ("minimal negative space", "rich detailed"),
    "geometry":         ("angular geometric", "soft organic"),
    "formality":        ("candid casual", "polished editorial"),
    "motion":           ("still calm", "dynamic motion"),
    "type_personality": ("technical precise", "editorial human"),
}


def image_search_terms(profile: "BrandProfile",
                       temperature: Optional[Dict[str, Any]] = None) -> List[str]:
    """Deterministic, on-brand search-term suggestions for sourcing curated stock.

    Per canonical rule 8 (imagery is mandatory and real): use the client's own
    assets first, then fill with curated Unsplash/Pexels chosen to match the brand
    and the 7-axis temperature. This helper turns the brand (name / hue family /
    voice) plus an optional ``temperature`` (the synthesizer's 7 axes, each 0..1)
    into concrete search phrases a sourcing step can run. It does NOT fetch
    anything -- the engine never calls the network. Same input -> same output.

    ``temperature`` accepts either a dict of axis->value (0..1) or an object with
    an ``.axes`` attribute (e.g. a synthesized system). Unknown shapes are ignored.
    """
    terms: List[str] = []

    def _add(t: str) -> None:
        t = (t or "").strip()
        if t and t not in terms:
            terms.append(t)

    # Brand-led terms: voice + logo-style descriptors, then a brand-color word.
    # (The logo's letterform personality is brand voice expressed as type, so it
    #  is a legitimate, deterministic source of mood words for sourcing imagery.)
    for word in _descriptor_words(getattr(profile, "voice", "") or "",
                                  getattr(profile, "logo_style", "") or ""):
        _add(word)

    fam = (getattr(profile, "primary_family", "") or "").strip().lower()
    if fam and fam not in ("", "unknown"):
        _add("%s palette" % _FAMILY_SEARCH_WORD.get(fam, fam))

    # Temperature-led mood terms (the 7-axis read).
    axes: Dict[str, Any] = {}
    if isinstance(temperature, dict):
        axes = temperature
    elif temperature is not None and hasattr(temperature, "axes"):
        maybe = getattr(temperature, "axes")
        if isinstance(maybe, dict):
            axes = maybe
    for axis, (low_word, high_word) in _AXIS_SEARCH_WORDS.items():
        if axis in axes:
            try:
                v = float(axes[axis])
            except (TypeError, ValueError):
                continue
            _add(high_word if v >= 0.5 else low_word)

    # Always anchor on real, on-brand photography rather than generic stock.
    had_specific = bool(terms)
    _add("authentic product photography")
    if not had_specific:
        # Nothing brand- or temperature-specific landed; still give a usable,
        # non-generic baseline keyed to "real, on-brand."
        _add("real environment editorial")

    return terms


def anchor_recommendation(recommendation: Dict[str, Any], profile: BrandProfile) -> Dict[str, Any]:
    """Override a recommendation's palette + type with the extracted brand, so
    generation uses THEIR colors / logo / type instead of the engine's pick.

    The palette's neutral roles and structure stay; the brand hues replace the
    primary/accent and the brand's logo + type personality are attached as hard
    directives for the build step. This is how brand.md 'anchors' generation
    (rule 2 in references/process/brand-extraction.md).
    """
    rec = dict(recommendation)
    pal = dict(rec.get("palette") or {})
    colors = dict(pal.get("colors") or {})
    if profile.primary:
        colors["primary"] = profile.primary
        colors["accent"] = profile.primary          # the brand color drives the CTA
    if profile.secondary:
        colors["secondary"] = profile.secondary[0]
    if colors:
        pal["colors"] = colors
    pal["brand_anchored"] = True
    rec["palette"] = pal
    rec["brand"] = {
        "name": profile.name,
        "logo": profile.logo,
        "primary": profile.primary,
        "primary_family": profile.primary_family,
        "secondary": profile.secondary,
    }
    rec["type_directive"] = {
        "match_logo_style": profile.logo_style,
        "reject_defaults": True,
        "display": profile.fonts.get("display"),
        "display_source": profile.fonts.get("display_source"),
    }
    return rec
