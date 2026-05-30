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
``score_brand_fidelity(html_text, profile) -> dict``
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from engine.brand.extract import BrandProfile, hue_family


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


def score_brand_fidelity(html_text: str, profile: BrandProfile) -> Dict[str, Any]:
    """Score how faithfully ``html_text`` honors ``profile``. Deterministic.

    Returns ``{score, passed, findings}`` where findings is a list of
    ``{check, severity, ok, detail}``. The hard floor (rule 7): if the profile
    has a primary and the output is missing that primary OR missing the logo,
    ``passed`` is False regardless of the numeric score.
    """
    html = html_text or ""
    html_lower = html.lower()
    findings: List[Dict[str, Any]] = []
    earned = 0

    has_primary = bool((profile.primary or "").strip())

    # (a) PRIMARY USED -------------------------------------------------------
    primary_ok = bool(has_primary and _hex_present(html_lower, profile.primary))
    if has_primary:
        findings.append({
            "check": "primary_used",
            "severity": "critical",
            "ok": primary_ok,
            "detail": ("Brand primary %s is used in the output." % profile.primary)
            if primary_ok else
            ("Brand primary %s is MISSING from the output -- it must drive the "
             "palette/CTA." % profile.primary),
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
        drift = _family_used_as_display(html, html_lower, rejected)
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
        if _hex_present(html_lower, hx):
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
