"""An 11-step OKLCH ramp with the seed anchored at 500.

Lighter steps interpolate lightness from the anchor up toward L_TOP and bleed
chroma; darker steps interpolate down toward L_BOTTOM. Hue is held constant.

With the current BAND, L_TOP and MIN_STEP, only the dark side ever widens
past its constant: a retuned or near-BAND[0] anchor can sit within
5 * MIN_STEP of L_BOTTOM, but no anchor ever sits within 5 * MIN_STEP of
L_TOP, since BAND[1] + 5 * MIN_STEP == L_TOP exactly. The light-side widen
and the dark-side floor are kept as defensive guards; they only start doing
real work if BAND, L_TOP or L_BOTTOM change.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from engine.foundations.color_math import hex_to_oklch, hex_to_rgb, oklch_to_hex, rgb_to_hex

STEPS = (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950)
ANCHOR = 500
L_TOP, L_BOTTOM = 0.975, 0.16
BAND = (0.30, 0.80)
# Minimum lightness gap between adjacent stops. A seed retuned near the
# dark band edge (BAND[0]) would otherwise crush the dark side of the ramp
# toward L_BOTTOM, so dark_end widens past the constant once the anchor
# sits within 5 * MIN_STEP of it. light_end's symmetric widen and dark_end's
# 0.02 floor are defensive only: with BAND = (0.30, 0.80), L_TOP = 0.975 and
# L_BOTTOM = 0.16, light_end is always exactly L_TOP (0.80 + 5 * 0.035 ==
# 0.975) and the floor never binds (0.30 - 5 * 0.035 == 0.125, well above
# 0.02); neither does anything unless BAND or L_TOP is changed later.
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
