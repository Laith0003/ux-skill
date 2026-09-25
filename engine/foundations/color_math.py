"""Color math for the foundations engine: hex, OKLCH, WCAG contrast.

OKLab/OKLCH conversion follows Björn Ottosson's published matrices. The
contrast formula is WCAG 2.x and matches engine.synthesizer exactly (a test
pins them together so the two never drift).
"""
from __future__ import annotations

import math
import re
from typing import Tuple

RGB = Tuple[int, int, int]

_HEX_COLOR_RE = re.compile(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")


def hex_to_rgb(h: str) -> RGB:
    if isinstance(h, str):
        m = _HEX_COLOR_RE.fullmatch(h.strip())
    else:
        m = None
    if not m:
        raise ValueError(
            f"{h!r} is not a hex color. Use #RRGGBB or #RGB, for example #3366FF.")
    s = m.group(1)
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def rgb_to_hex(rgb: RGB) -> str:
    return "#" + "".join(f"{max(0, min(255, int(round(c)))):02X}" for c in rgb)


def _to_linear(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _from_linear(c: float) -> float:
    c = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return c * 255.0


def hex_to_oklch(h: str) -> Tuple[float, float, float]:
    r, g, b = (_to_linear(c) for c in hex_to_rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360 if C > 1e-7 else 0.0
    return L, C, H


def _oklch_to_linear(L: float, C: float, H: float):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def oklch_to_hex(L: float, C: float, H: float) -> str:
    """OKLCH to sRGB hex. Out-of-gamut colors keep L and H and lose chroma
    (binary search) instead of clipping channels, so hue does not shift."""
    if not (math.isfinite(L) and math.isfinite(C) and math.isfinite(H)):
        raise ValueError(
            f"oklch_to_hex requires finite L, C, H; got L={L!r}, C={C!r}, H={H!r}.")
    L = max(0.0, min(1.0, L))
    C = max(0.0, C)
    lo, hi = 0.0, C
    rgb = _oklch_to_linear(L, C, H)
    if any(c < -1e-6 or c > 1 + 1e-6 for c in rgb):
        for _ in range(30):
            mid = (lo + hi) / 2
            if any(c < -1e-6 or c > 1 + 1e-6 for c in _oklch_to_linear(L, mid, H)):
                hi = mid
            else:
                lo = mid
        rgb = _oklch_to_linear(L, lo, H)
    return rgb_to_hex(tuple(_from_linear(max(0.0, min(1.0, c))) for c in rgb))


# CSS Color 4 gamut mapping (css-color-4, "binary search gamut mapping"):
# a just noticeable difference in OKLab, and the chroma resolution.
_GAMUT_JND = 0.02
_GAMUT_EPSILON = 0.0001
_IN_GAMUT = 1e-6
# A color that moves less than this (about one 8-bit step) sits outside sRGB
# only by float noise or rounding in how it was written: not reported.
_REPORT_FLOOR = 0.002


def oklab_to_oklch(L: float, a: float, b: float) -> Tuple[float, float, float]:
    """OKLab to OKLCH, the hue in degrees from 0 to 360."""
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def _linear_to_oklab(rgb) -> Tuple[float, float, float]:
    r, g, b = rgb
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def _oklch_to_oklab(L: float, C: float, H: float) -> Tuple[float, float, float]:
    return L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))


def _in_gamut(rgb) -> bool:
    return all(-_IN_GAMUT <= c <= 1 + _IN_GAMUT for c in rgb)


def _clip(rgb) -> Tuple[float, float, float]:
    return tuple(max(0.0, min(1.0, c)) for c in rgb)


def gamut_map_oklch(L: float, C: float, H: float) -> Tuple[str, float, bool]:
    """(hex, OKLab distance from the color asked for, mapped) for an OKLCH
    color, by CSS Color 4 gamut mapping: a color outside sRGB keeps its
    lightness and hue and loses chroma (binary search) until clipping it
    moves it less than a just noticeable difference (deltaE OK 0.02).
    Lightness at or past 1 is white and at or below 0 is black.
    Deterministic. Raises ValueError for a value that is not finite."""
    if not (math.isfinite(L) and math.isfinite(C) and math.isfinite(H)):
        raise ValueError(
            f"gamut_map_oklch requires finite L, C, H; got L={L!r}, C={C!r}, H={H!r}.")
    C = max(0.0, C)
    origin = _oklch_to_oklab(L, C, H)
    if L >= 1 or L <= 0:
        rgb = (1.0, 1.0, 1.0) if L >= 1 else (0.0, 0.0, 0.0)
        mapped = C > 0 or L > 1 or L < 0
    else:
        rgb = _oklch_to_linear(L, C, H)
        mapped = not _in_gamut(rgb)
        if mapped:
            rgb = _gamut_search(L, C, H)
    rgb = _clip(rgb)
    hx = rgb_to_hex(tuple(_from_linear(c) for c in rgb))
    got = _linear_to_oklab(tuple(_to_linear(c) for c in hex_to_rgb(hx)))
    distance = math.dist(origin, got)
    return hx, distance, mapped and distance > _REPORT_FLOOR


def _gamut_search(L: float, C: float, H: float) -> Tuple[float, float, float]:
    """The CSS Color 4 binary search on chroma, in linear sRGB."""
    def delta(chroma: float, clipped) -> float:
        return math.dist(_oklch_to_oklab(L, chroma, H), _linear_to_oklab(clipped))

    clipped = _clip(_oklch_to_linear(L, C, H))
    if delta(C, clipped) < _GAMUT_JND:
        return clipped
    lo, hi, lo_in_gamut = 0.0, C, True
    while hi - lo > _GAMUT_EPSILON:
        chroma = (lo + hi) / 2
        current = _oklch_to_linear(L, chroma, H)
        if lo_in_gamut and _in_gamut(current):
            lo = chroma
            continue
        clipped = _clip(current)
        e = delta(chroma, clipped)
        if e < _GAMUT_JND:
            if _GAMUT_JND - e < _GAMUT_EPSILON:
                return clipped
            lo_in_gamut = False
            lo = chroma
        else:
            hi = chroma
    return clipped


# WCAG 2.x fixes this threshold at 0.03928, not sRGB's own 0.04045, and this
# is deliberate: it keeps _luminance pinned to engine/synthesizer's
# _relative_luminance so contrast() never drifts from the synthesizer's own
# gate. For 8-bit input the two thresholds classify every channel value the
# same way anyway (both land between 10/255 and 11/255), so nobody should
# "fix" one of these numbers to match the other; they are independently
# correct for what each function does.
def _luminance(h: str) -> float:
    r, g, b = hex_to_rgb(h)

    def lin(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def luminance(h: str) -> float:
    """WCAG relative luminance of a hex color, 0 (black) to 1 (white)."""
    return _luminance(h)


def oklab_distance(a: str, b: str) -> float:
    """Euclidean distance between two hex colors in OKLab: 0 for the same
    color, about 0.02 for a just visible step, 1 for black to white."""
    la, ca, ha = hex_to_oklch(a)
    lb, cb, hb = hex_to_oklch(b)
    ax, ay = ca * math.cos(math.radians(ha)), ca * math.sin(math.radians(ha))
    bx, by = cb * math.cos(math.radians(hb)), cb * math.sin(math.radians(hb))
    return math.sqrt((la - lb) ** 2 + (ax - bx) ** 2 + (ay - by) ** 2)
