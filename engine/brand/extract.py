"""Brand extraction -> a travelling brand profile (brand.md + brand.json).

When ux-skill redesigns an EXISTING site, it must honor that site's identity
instead of imposing the engine's house style. This module turns raw brand
signals captured from the live page (logo, colors, fonts, imagery) into a
structured BrandProfile that:

  1. travels through the pipeline (discover -> synthesize -> generate) as a hard
     anchor, so output uses THEIR logo + colors + type, and
  2. is scored against by the linter/rating (brand fidelity), so an output that
     drifts off-brand cannot pass.

Signal capture (reading the live DOM/screenshot) is I/O done by the caller
(browser eval, CSS parse, or CV on a screenshot). This module is the
deterministic normalize + render half: signals dict -> BrandProfile -> markdown.
No network, no LLM. Run with Python 3.9+.
"""
from __future__ import annotations

import colorsys
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Hue classification (shared concept with the recommender's anti-slop band)
# ---------------------------------------------------------------------------
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
    bins = [
        (15, "red"), (45, "orange"), (70, "yellow"), (160, "green"),
        (200, "teal"), (240, "blue"), (290, "violet"), (340, "magenta"),
        (360, "red"),
    ]
    for hi, name in bins:
        if h < hi:
            return name
    return "red"


def _font_name(family: Optional[str]) -> str:
    """First real family from a CSS font-family stack ('"Roboto Flex", ...' -> 'Roboto Flex')."""
    if not family:
        return ""
    first = family.split(",")[0].strip().strip('"').strip("'").strip()
    generic = {"system-ui", "sans-serif", "serif", "monospace", "ui-sans-serif",
               "-apple-system", "blinkmacsystemfont"}
    return "" if first.lower() in generic else first


# ---------------------------------------------------------------------------
# Brand profile
# ---------------------------------------------------------------------------
@dataclass
class BrandProfile:
    source: str = ""
    name: str = ""
    logo: Dict[str, Any] = field(default_factory=dict)        # {url, alt}
    primary: str = ""                                          # brand primary hex
    primary_family: str = ""                                   # hue family of primary
    secondary: List[str] = field(default_factory=list)         # supporting brand hexes
    fonts: Dict[str, str] = field(default_factory=dict)        # {display, body, stack}
    imagery: List[str] = field(default_factory=list)           # on-brand image URLs
    voice: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_profile(signals: Dict[str, Any]) -> BrandProfile:
    """Normalize captured signals into a BrandProfile. Deterministic.

    Expected (all optional) signal keys:
      source, name, logo{src/url,alt}, brand_colors[{hex,score}] or colors[hex],
      fonts{h1,h2,body,button} or {display,body}, imagery[url], voice.
    """
    p = BrandProfile()
    p.source = signals.get("source", "") or signals.get("url", "")

    logo = signals.get("logo") or {}
    if logo:
        p.logo = {"url": logo.get("url") or logo.get("src") or "",
                  "alt": logo.get("alt") or ""}
    # brand name: explicit, else derive from logo alt ("... logo" -> "...")
    name = signals.get("name") or ""
    if not name and p.logo.get("alt"):
        name = p.logo["alt"]
    if name:
        name = name.replace("logo", "").replace("Logo", "").strip(" -_|")
        p.name = " ".join(w.capitalize() if w.islower() else w for w in name.split())

    # colors: accept [{hex,score}] (sorted by score) or [hex]
    raw = signals.get("brand_colors") or signals.get("colors") or []
    hexes: List[str] = []
    for c in raw:
        hx = c.get("hex") if isinstance(c, dict) else c
        if isinstance(hx, str) and _hex_to_hsv(hx) and hx not in hexes:
            hexes.append(hx)
    # primary = first non-neutral; fall back to first
    primary = next((h for h in hexes if hue_family(h) != "neutral"), hexes[0] if hexes else "")
    p.primary = primary
    p.primary_family = hue_family(primary) if primary else ""
    p.secondary = [h for h in hexes if h != primary][:4]

    fonts = signals.get("fonts") or {}
    display = _font_name(fonts.get("display") or fonts.get("h1") or fonts.get("h2"))
    body = _font_name(fonts.get("body"))
    stack = fonts.get("h1") or fonts.get("body") or fonts.get("display") or ""
    p.fonts = {"display": display, "body": body or display, "stack": stack}

    p.imagery = list(signals.get("imagery") or [])
    p.voice = signals.get("voice", "")
    return p


def render_md(p: BrandProfile) -> str:
    """Render the travelling brand.md anchor."""
    sec = " ".join("`%s`" % h for h in p.secondary) or "(none captured)"
    imgs = "\n".join("- %s" % u for u in p.imagery) or "- (none captured — source on-brand by temperature)"
    lines = [
        "# Brand anchor — %s" % (p.name or "untitled"),
        "",
        "> This file is the source brand. It travels to every step (synthesize ->",
        "> generate) and is scored by the linter/rating. The output MUST use this",
        "> brand's logo, primary color, and type. Drifting to a house style fails.",
        "",
        "- **Source:** %s" % (p.source or "n/a"),
        "- **Logo:** %s%s" % (p.logo.get("url", "(none)"),
                              (" — alt: %s" % p.logo["alt"]) if p.logo.get("alt") else ""),
        "",
        "## Colors",
        "- **Primary:** `%s`  (hue family: %s)" % (p.primary or "n/a", p.primary_family or "n/a"),
        "- **Secondary:** %s" % sec,
        "",
        "## Type",
        "- **Display:** %s" % (p.fonts.get("display") or "n/a"),
        "- **Body:** %s" % (p.fonts.get("body") or "n/a"),
        "- **Source stack:** `%s`" % (p.fonts.get("stack") or "n/a"),
        "",
        "## Imagery",
        imgs,
        "",
        "## Voice",
        p.voice or "(preserve the source site's existing human copy; do not rewrite unless asked)",
        "",
    ]
    return "\n".join(lines)
