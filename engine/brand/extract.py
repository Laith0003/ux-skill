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
    logo: Dict[str, Any] = field(default_factory=dict)         # {url, alt}
    logo_style: str = ""                                       # vision read of the wordmark
    primary: str = ""                                          # from LOGO pixels (rule 3)
    primary_family: str = ""
    primary_source: str = ""                                   # "logo" | "css"
    secondary: List[str] = field(default_factory=list)
    fonts: Dict[str, str] = field(default_factory=dict)        # display/body/type_personality/display_source
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
    return p


def render_md(p: BrandProfile) -> str:
    sec = " ".join("`%s`" % h for h in p.secondary) or "(none captured)"
    imgs = "\n".join("- %s" % u for u in p.imagery) or "- (none captured -- source real, on-brand imagery by temperature)"
    notes = "\n".join("- %s" % n for n in p.notes) or "- (none)"
    if p.fonts.get("display"):
        type_line = "- **Display:** %s (kept -- distinctive, not a default)" % p.fonts["display"]
    else:
        type_line = "- **Display:** pick a font matching the logo style: **%s** (site font was a default, rejected)" % (p.fonts.get("type_personality") or "n/a")
    lines = [
        "# Brand anchor -- %s" % (p.name or "untitled"),
        "",
        "> Source brand. Travels to synthesize -> generate and is scored by the",
        "> linter/rating. Output MUST use this brand's logo, primary color, and type.",
        "> Drifting to a house style fails the brand-fidelity gate.",
        "",
        "- **Source:** %s" % (p.source or "n/a"),
        "- **Logo:** %s%s" % (p.logo.get("url", "(none)"),
                              (" -- alt: %s" % p.logo["alt"]) if p.logo.get("alt") else ""),
        "",
        "## Colors  (primary from the LOGO, not CSS chrome)",
        "- **Primary:** `%s`  (hue: %s, source: %s)" % (p.primary or "n/a", p.primary_family or "n/a", p.primary_source or "n/a"),
        "- **Secondary:** %s" % sec,
        "",
        "## Type  (from the logo's letterform style; defaults rejected)",
        type_line,
        "- **Body:** %s" % (p.fonts.get("body") or "clean readable companion to the display face"),
        "- **Logo type personality:** %s" % (p.logo_style or "n/a"),
        "",
        "## Imagery  (mandatory, real, on-brand)",
        imgs,
        "",
        "## Voice",
        p.voice or "(preserve the source site's existing human copy; do not rewrite unless asked)",
        "",
        "## Extraction notes",
        notes,
        "",
    ]
    return "\n".join(lines)
