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
