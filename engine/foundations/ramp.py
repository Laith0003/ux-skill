"""An 11-step OKLCH ramp with the seed anchored at 500.

Lighter steps interpolate lightness from the anchor up to L_TOP and bleed
chroma; darker steps interpolate down to L_BOTTOM. Hue is held constant.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from engine.foundations.color_math import hex_to_oklch, oklch_to_hex

STEPS = (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950)
ANCHOR = 500
L_TOP, L_BOTTOM = 0.975, 0.16
BAND = (0.30, 0.80)
# Position of each step between the anchor (0) and the end of its side (1).
_LIGHT = {400: 0.2, 300: 0.4, 200: 0.6, 100: 0.8, 50: 1.0}
_DARK = {600: 0.2, 700: 0.4, 800: 0.6, 900: 0.8, 950: 1.0}


@dataclass
class RampResult:
    stops: Dict[int, str] = field(default_factory=dict)
    retuned: bool = False
    note: str = ""


def ramp(seed_hex: str) -> RampResult:
    seed = seed_hex.upper()
    L, C, H = hex_to_oklch(seed)
    result = RampResult()
    if BAND[0] <= L <= BAND[1]:
        anchor_hex = seed
    else:
        L = min(max(L, BAND[0]), BAND[1])
        anchor_hex = oklch_to_hex(L, C, H)
        result.retuned = True
        result.note = (f"{seed} is too {'light' if hex_to_oklch(seed)[0] > BAND[1] else 'dark'} "
                       f"to anchor a ramp at 500; 500 retuned to {anchor_hex}, same hue and chroma.")
    for step in STEPS:
        if step == ANCHOR:
            result.stops[step] = anchor_hex
        elif step in _LIGHT:
            f = _LIGHT[step]
            result.stops[step] = oklch_to_hex(L + (L_TOP - L) * f, C * (1 - 0.75 * f), H)
        else:
            f = _DARK[step]
            result.stops[step] = oklch_to_hex(L - (L - L_BOTTOM) * f, C * (1 - 0.35 * f), H)
    return result
