"""Character: the continuous quantities every foundation reads from the
seven axes.

Each function is a pure, continuous function of the axes. The hues also
read the brand hue: status_seed is continuous in it, while neutral_tint
and support_hue turn toward their anchor the short way and so flip
direction where the brand sits opposite the anchor (see each docstring).
No function looks up an industry, a keyword or a band:
a foundation that needs a discrete choice (a face, a pill corner, a brand
role) takes it from one of these quantities, so two briefs that differ on
an axis differ in the output.

INFLUENCE says which axes reach which foundation. A test moves each axis
from 0 to 1 with the others at 0.5 and requires every foundation it names
to change, so a mapping cannot quietly drop an axis.
"""
from __future__ import annotations

import math
from types import MappingProxyType
from typing import Dict, Mapping, Tuple

from engine.synthesizer.axes import AxisValues

# axis -> the foundations it must move (tests/foundations/test_character.py).
INFLUENCE: Mapping[str, Tuple[str, ...]] = MappingProxyType({
    "warmth": ("color", "imagery"),
    "contrast": ("color", "type", "elevation", "border"),
    "density": ("space", "layout", "type"),
    "geometry": ("radius", "imagery"),
    "formality": ("radius", "type", "elevation", "motion", "imagery"),
    "motion": ("motion",),
    "type_personality": ("type",),
})

WARM_HUE, COOL_HUE = 70.0, 250.0
# Status hues and how far harmonizing may move each, in OKLCH degrees.
STATUS_HUES: Mapping[str, float] = MappingProxyType(
    {"danger": 25.0, "warning": 75.0, "success": 150.0, "info": 245.0})
STATUS_BAND = 12.0
# Within this many degrees of a status hue's opposite the brand lean fades
# to zero, so a brand there pulls neither way and the hue has no seam.
STATUS_FADE = 15.0
STATUS_L = 0.58


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def hue_delta(from_h: float, to_h: float) -> float:
    """Signed shortest turn from one hue to another, -180 to 180."""
    return (to_h - from_h + 180.0) % 360.0 - 180.0


def mix_hue(a: float, b: float, t: float) -> float:
    """The hue t of the way from a to b along the shorter arc."""
    return (a + hue_delta(a, b) * t) % 360.0


def roundness(axes: AxisValues) -> float:
    """0 is sharp, 1 is soft enough for pill controls. Geometry sets it;
    a playful brand rounds up and a formal one squares off."""
    return clamp(axes.geometry + 0.4 * (0.5 - axes.formality))


def depth(axes: AxisValues) -> float:
    """Surface treatment: 0 is flat with hairline edges, 0.5 soft, 1 deep
    shadows. Contrast sets it; formality flattens it."""
    return clamp(axes.contrast + 0.3 * (0.5 - axes.formality))


def warm_pull(axes: AxisValues) -> float:
    """How far warmth pulls neutrals off the brand hue, 0 at warmth 0.5
    and 1 at either end."""
    return abs(axes.warmth - 0.5) * 2.0


def neutral_tint(axes: AxisValues, brand_hue: float) -> Tuple[float, float]:
    """(hue, chroma) of the neutral seed. At warmth 0.5 the neutrals take
    the brand hue at a whisper of chroma; toward either end they move to a
    warm or a cool hue and gain chroma, so a warm brand gets cream and a
    cool one blue grey. Continuous in the axes; in the brand hue it turns
    the short way to the anchor, so away from warmth 0.5 it flips direction
    where the brand sits opposite the anchor (a warm brief with a brand
    near 250, a cool one with a brand near 70)."""
    t = warm_pull(axes)
    anchor = WARM_HUE if axes.warmth >= 0.5 else COOL_HUE
    return mix_hue(brand_hue, anchor, 0.8 * t), 0.008 + 0.022 * t


def status_seed(status: str, axes: AxisValues, brand_hue: float) -> Tuple[float, float, float]:
    """(L, C, H) of one status seed. The hue leans a quarter of the way
    toward the brand and toward warm or cool with warmth, never more than
    STATUS_BAND from its own hue, so danger stays red. The brand lean fades
    to zero within STATUS_FADE degrees of the status hue's opposite, so the
    hue is continuous in the brand hue too. Chroma follows the contrast
    axis: a muted brand gets quiet status colors."""
    base = STATUS_HUES[status]
    d = hue_delta(base, brand_hue)
    lean = 0.25 * d * clamp((180.0 - abs(d)) / STATUS_FADE)
    anchor = WARM_HUE if axes.warmth >= 0.5 else COOL_HUE
    lean += 0.2 * warm_pull(axes) * hue_delta(base, anchor)
    hue = (base + clamp(lean, -STATUS_BAND, STATUS_BAND)) % 360.0
    return STATUS_L, 0.07 + 0.11 * axes.contrast, hue


def support_hue(axes: AxisValues, brand_hue: float) -> float:
    """The supporting accent's hue: analogous for a muted brand, close to
    complementary for a bold one, pulled warm or cool with warmth. The pull
    turns the short way, so it flips direction where the offset hue sits
    opposite the anchor."""
    offset = 30.0 + 150.0 * axes.contrast
    anchor = WARM_HUE if axes.warmth >= 0.5 else COOL_HUE
    return mix_hue((brand_hue + offset) % 360.0, anchor, 0.3 * warm_pull(axes))


def brand_role_scores(axes: AxisValues) -> Dict[str, float]:
    """How well each brand role fits the axes. fill: the brand is the
    action color. accent: the brand marks text and links, actions are ink.
    edge: the brand draws edges and rules, actions are ink. The highest
    score wins; a brief may name the role instead."""
    return {
        "fill": 0.4 * axes.contrast + 0.35 * (1 - axes.formality) + 0.25 * axes.warmth,
        "accent": 0.45 * axes.formality + 0.3 * (1 - axes.contrast)
        + 0.25 * axes.type_personality,
        "edge": 0.5 * axes.formality + 0.3 * (1 - axes.warmth) + 0.2 * (1 - axes.geometry),
    }


def brand_role(axes: AxisValues) -> str:
    scores = brand_role_scores(axes)
    return max(("fill", "accent", "edge"), key=lambda k: (round(scores[k], 6), k == "fill"))


def display_weight(axes: AxisValues) -> int:
    """The display face's weight, 300 to 800 in steps of 100: bold and
    playful brands go heavy, muted and formal ones go light."""
    raw = 300 + 500 * (0.55 * axes.contrast + 0.45 * (1 - axes.formality))
    return int(round(raw / 100.0)) * 100


def heading_weight(axes: AxisValues) -> int:
    """The text face's heading weight, 500 to 700."""
    return int(round((500 + 200 * axes.contrast) / 100.0)) * 100


def display_tracking(axes: AxisValues) -> float:
    """Letter spacing of the largest display size, in em: tighter for a
    bold brand, more open for a formal one."""
    return round(-(0.005 + 0.035 * axes.contrast) * (1.2 - 0.6 * axes.formality), 4)


def label_tracking(axes: AxisValues) -> float:
    """Letter spacing of small labels and metadata, in em: formal labels
    open up."""
    return round(0.01 + 0.06 * axes.formality, 4)


def scale_ratio(axes: AxisValues) -> float:
    """The type scale ratio, 1.095 to 1.355: 1.125 for a muted, open brand
    to 1.355 for a bold one; a dense system tightens it by up to 0.03."""
    return round(1.125 + 0.23 * axes.contrast - 0.03 * axes.density, 4)


def icon_stroke(axes: AxisValues) -> float:
    """Icon stroke on a 24 unit grid, 1.25 to 2.5 in quarters, a quarter
    heavier for each 100 of display weight."""
    return round((1.25 + (display_weight(axes) - 300) / 400.0) * 4) / 4


def overshoot(axes: AxisValues) -> float:
    """How far motion curves overshoot, 0 to 1: lively brands bounce,
    formal ones hold it back."""
    return round(clamp(axes.motion * (1.0 - 0.6 * axes.formality)), 4)


def regularity(axes: AxisValues) -> float:
    """How regular generated art is: formal art sits on a grid, playful art
    scatters."""
    return clamp(0.2 + 0.8 * axes.formality)


def technical(axes: AxisValues) -> float:
    """How technical the type reads, 0 to 1: geometric and cool."""
    return clamp(0.5 * (1 - axes.type_personality) + 0.5 * (1 - axes.warmth))


def log_position(size: float, low: float, high: float) -> float:
    """Where `size` sits between low and high on a log scale, 0 to 1.
    size and low must be above 0."""
    if size <= 0:
        raise ValueError(f"log_position: size must be above 0, got {size}; "
                         "pass a positive size")
    if low <= 0:
        raise ValueError(f"log_position: low must be above 0, got {low}; "
                         "pass a positive lower bound")
    if high <= low:
        return 0.0
    return clamp(math.log(size / low) / math.log(high / low))
