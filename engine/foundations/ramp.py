"""An 11-step OKLCH ramp with the seed anchored at 500.

Lighter steps interpolate lightness from the anchor up toward L_TOP and bleed
chroma; darker steps interpolate down toward L_BOTTOM. Hue is held constant.
When the anchor sits close enough to L_TOP or L_BOTTOM that MIN_STEP could
not be kept, that side's end widens past the constant instead.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from engine.foundations.color_math import hex_to_oklch, hex_to_rgb, oklch_to_hex, rgb_to_hex

STEPS = (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950)
ANCHOR = 500
L_TOP, L_BOTTOM = 0.975, 0.16
BAND = (0.30, 0.80)
# Minimum lightness gap between adjacent stops. A seed retuned near a band
# edge would otherwise crush the far side of the ramp toward L_TOP or
# L_BOTTOM, so the interpolation end on that side widens past the constant
# when the anchor sits close to it.
MIN_STEP = 0.035
# Position of each step between the anchor (0) and the end of its side (1).
_LIGHT = {400: 0.2, 300: 0.4, 200: 0.6, 100: 0.8, 50: 1.0}
_DARK = {600: 0.2, 700: 0.4, 800: 0.6, 900: 0.8, 950: 1.0}


@dataclass
class RampResult:
    stops: Dict[int, str] = field(default_factory=dict)
    retuned: bool = False
    note: str = ""


def ramp(seed_hex: str) -> RampResult:
    seed = rgb_to_hex(hex_to_rgb(seed_hex))
    seed_L, C, H = hex_to_oklch(seed)
    L = seed_L
    result = RampResult()
    if BAND[0] <= L <= BAND[1]:
        anchor_hex = seed
    else:
        L = min(max(L, BAND[0]), BAND[1])
        anchor_hex = oklch_to_hex(L, C, H)
        result.retuned = True
        anchor_C = hex_to_oklch(anchor_hex)[1]
        chroma_note = ("same hue, chroma reduced to fit sRGB"
                        if C - anchor_C > 0.005 else "same hue and chroma")
        result.note = (f"{seed} is too {'light' if seed_L > BAND[1] else 'dark'} "
                       f"to anchor a ramp at 500; 500 retuned to {anchor_hex}, {chroma_note}.")
    dark_end = max(0.02, min(L_BOTTOM, L - 5 * MIN_STEP))
    light_end = min(0.995, max(L_TOP, L + 5 * MIN_STEP))
    for step in STEPS:
        if step == ANCHOR:
            result.stops[step] = anchor_hex
        elif step in _LIGHT:
            f = _LIGHT[step]
            result.stops[step] = oklch_to_hex(L + (light_end - L) * f, C * (1 - 0.75 * f), H)
        else:
            f = _DARK[step]
            result.stops[step] = oklch_to_hex(L - (L - dark_end) * f, C * (1 - 0.35 * f), H)
    return result
