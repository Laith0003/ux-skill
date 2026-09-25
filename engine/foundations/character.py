"""Character: the continuous quantities every foundation reads from the
seven axes.

Each function is a pure, continuous function of the axes. The hues also
read the brand hue, weighted by the brand's chroma (hue_weight), so a grey
brand, whose hue is noise, steers nothing. status_seed and neutral_tint are
continuous in the brand color; support_hue turns toward its anchor the
short way and so flips direction where its offset hue sits opposite the
anchor, and a grey brand's accent comes from the axes (see its docstring).
The brand's lightness and chroma weigh its role (brand_fill_evidence) and
the cost of black text on it (black_text_cost).
No function looks up an industry, a keyword or a band:
a foundation that needs a discrete choice (a face, a pill corner, a brand
role) takes it from one of these quantities, so two briefs that differ on
an axis differ in the output.

INFLUENCE says which axes reach which foundation. For every pair a test
names one visible quantity in the built tokens (the neutrals' b, the
status chroma, the card padding and so on), moves the axis from 0 to 1
with the others at 0.5, and requires that quantity to move one way only
and by at least a stated amount, so a mapping cannot quietly drop an axis
while another token in the same foundation still moves.
"""
from __future__ import annotations

import math
from types import MappingProxyType
from typing import Dict, Mapping, Optional, Tuple

from engine.synthesizer.axes import AxisValues

# axis -> the foundations it must move; each pair's quantity is in
# tests/foundations/test_character.py (QUANTITIES).
INFLUENCE: Mapping[str, Tuple[str, ...]] = MappingProxyType({
    "warmth": ("color", "imagery"),
    "contrast": ("color", "type", "elevation", "border"),
    "density": ("space", "layout", "type"),
    "geometry": ("radius", "imagery"),
    "formality": ("radius", "type", "elevation", "motion", "imagery"),
    "motion": ("motion", "color"),
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
# Brand chroma at and above which the brand hue counts in full. Below it the
# hue's pull shrinks in proportion, to nothing at grey, where the hue is
# noise (#808080 reads 0 degrees, #7F8080 197).
HUE_CHROMA = 0.04
# The neutral seed's chroma: a whisper of the brand's own hue, NEUTRAL_C[0],
# weighted by the brand's chroma. Warmth only leans it: toward the warm or
# cool anchor by up to LEAN_C at warmth 0 or 1, and a brand with a hue holds
# back BRAND_HOLD of that lean, so the brand sets the temperature first.
NEUTRAL_C = (0.008, 0.030)
LEAN_C = 0.010
BRAND_HOLD = 0.5
# Chroma at and below SAT_CHROMA[0] reads as grey; at SAT_CHROMA[1] and above
# a brand reads fully saturated (saturation()).
SAT_CHROMA = (0.03, 0.12)
# How far a brand must stand from white (the page) and from black (ink), in
# OKLab distance, to carry a fill: none at REACH[0] and below, in full at
# REACH[1] and above (reach()).
REACH = (0.04, 0.12)
# How much the brand's own fill evidence adds to the fill score, and how
# much its absence adds to accent and edge (brand_role_scores). A lead of 1
# is at least any accent or edge score the axes can reach, so a brand with
# full evidence fills the action whatever the brief.
BRAND_LEAD = 1.0
BRAND_ARGUE = 0.25
# Black text on a fill costs up to BLACK_TEXT_COST in naturalness, measured
# in OKLab distance like a move off the brand, on a saturated fill at or
# below NATURAL_L[0], falling to nothing at NATURAL_L[1], where black on a
# bright color reads as the color's own look (black_text_cost). The most it
# costs equals the identity distance (color.IDENTITY_DISTANCE), so white text
# never pulls a fill further from the brand than that.
BLACK_TEXT_COST = 0.12
NATURAL_L = (0.60, 0.72)
# On a dark page black text on a mid tone reads muddier, so the same cost
# runs from full at NATURAL_L_DARK[0] to nothing at NATURAL_L_DARK[1]: the
# dark factor of one continuous rule.
NATURAL_L_DARK = (0.72, 0.84)
# A cool brand's supporting accent stays in its own family (support_seed):
# up to FAMILY_SPAN degrees from the brand hue, moved by warmth and held in
# by formality, at a share of the supporting chroma from SUPPORT_QUIET for a
# muted brief to SUPPORT_QUIET + SUPPORT_LOUD for a bold one.
FAMILY_SPAN = 30.0
SUPPORT_QUIET = 0.35
SUPPORT_LOUD = 0.45
# The coolness from which a brand's supporting accent stays wholly in its
# family; below it the brand-led accent returns in proportion, all of it on
# the warm side.
QUIET_COOLNESS = 2.0 / 3.0
# The pairings anti-slop bans, as hue arcs, each [start, end) in OKLCH
# degrees (banned_pair): a blue brand with a purple or pink accent, a purple
# brand with a blue one, and a cool brand (coolness BANNED_COOL and up) with
# a pink one.
BLUE_ARC, PURPLE_ARC, PINK_ARC = (215.0, 285.0), (285.0, 330.0), (330.0, 380.0)
BANNED_COOL = 0.75
# A grey brand's supporting accent hue at warmth 0 and at warmth 1: violet
# to rose, the one arc of the wheel that keeps STATUS_CLEARANCE from every
# status hue at every warmth (39 degrees at the least).
GREY_ACCENT = (285.0, 355.0)
STATUS_CLEARANCE = 30.0


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def hue_delta(from_h: float, to_h: float) -> float:
    """Signed shortest turn from one hue to another, -180 to 180."""
    return (to_h - from_h + 180.0) % 360.0 - 180.0


def mix_hue(a: float, b: float, t: float) -> float:
    """The hue t of the way from a to b along the shorter arc."""
    return (a + hue_delta(a, b) * t) % 360.0


def hue_weight(chroma: float) -> float:
    """How much a brand hue counts, 0 for grey to 1 at HUE_CHROMA and above,
    in proportion between."""
    return clamp(chroma / HUE_CHROMA)


def ab_mix(h1: float, c1: float, h2: float, c2: float, t: float) -> Tuple[float, float]:
    """(hue, chroma) t of the way from (h1, c1) to (h2, c2) on a straight
    line in the OKLab a/b plane. Between two far hues the path runs close to
    grey instead of around the wheel, so it never passes through a third
    hue, and it is continuous in both ends."""
    if t <= 0.0:
        return h1 % 360.0, c1
    if t >= 1.0:
        return h2 % 360.0, c2
    a = (1 - t) * c1 * math.cos(math.radians(h1)) + t * c2 * math.cos(math.radians(h2))
    b = (1 - t) * c1 * math.sin(math.radians(h1)) + t * c2 * math.sin(math.radians(h2))
    chroma = math.hypot(a, b)
    return (math.degrees(math.atan2(b, a)) % 360.0 if chroma > 1e-12 else h2 % 360.0), chroma


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


def neutral_tint(axes: AxisValues, brand_hue: float,
                 brand_chroma: float = HUE_CHROMA) -> Tuple[float, float]:
    """(hue, chroma) of the neutral seed: the brand's temperature first,
    leaned by warmth. The brand's own hue sits at a whisper of chroma
    (NEUTRAL_C[0], weighted by hue_weight, so a grey brand gives true grey).
    Warmth adds a lean toward the warm or the cool anchor in the OKLab a/b
    plane, up to LEAN_C at warmth 0 or 1 and nothing at 0.5. For a brand
    with a hue the lean runs along the brand's own hue axis only (its
    projection there), at 1 - BRAND_HOLD of its size: a warm brief deepens
    or thins the whisper toward grey, and never turns it through a third
    hue. So a grey brand in a warm industry gets a grey with a trace of
    sand, a blue brand with a warm tone a thinner blue grey, and an orange
    brand with a cool brief a thinner warm grey, never rose. Continuous in
    the axes and in the brand color: the lean is zero where the anchor
    switches, and hue_weight blends the free lean into the projected one."""
    weight = hue_weight(brand_chroma)
    anchor = WARM_HUE if axes.warmth >= 0.5 else COOL_HUE
    size = LEAN_C * warm_pull(axes)
    ux, uy = math.cos(math.radians(brand_hue)), math.sin(math.radians(brand_hue))
    fx, fy = size * math.cos(math.radians(anchor)), size * math.sin(math.radians(anchor))
    along = (fx * ux + fy * uy) * (1.0 - BRAND_HOLD)
    whisper = NEUTRAL_C[0] * weight
    a = whisper * ux + (1.0 - weight) * fx + weight * along * ux
    b = whisper * uy + (1.0 - weight) * fy + weight * along * uy
    chroma = math.hypot(a, b)
    if chroma < 1e-12:
        return brand_hue % 360.0, 0.0
    return math.degrees(math.atan2(b, a)) % 360.0, chroma


def status_seed(status: str, axes: AxisValues, brand_hue: float,
                brand_chroma: float = HUE_CHROMA) -> Tuple[float, float, float]:
    """(L, C, H) of one status seed. The hue leans a quarter of the way
    toward the brand and toward warm or cool with warmth, never more than
    STATUS_BAND from its own hue, so danger stays red. The brand lean fades
    to zero within STATUS_FADE degrees of the status hue's opposite, so the
    hue is continuous in the brand hue too, and scales with hue_weight, so a
    grey brand leans nothing. Chroma follows the contrast axis: a muted
    brand gets quiet status colors."""
    base = STATUS_HUES[status]
    d = hue_delta(base, brand_hue)
    lean = 0.25 * d * clamp((180.0 - abs(d)) / STATUS_FADE) * hue_weight(brand_chroma)
    anchor = WARM_HUE if axes.warmth >= 0.5 else COOL_HUE
    lean += 0.2 * warm_pull(axes) * hue_delta(base, anchor)
    hue = (base + clamp(lean, -STATUS_BAND, STATUS_BAND)) % 360.0
    return STATUS_L, 0.07 + 0.11 * axes.contrast, hue


def energy(axes: AxisValues) -> float:
    """How loud and lively the system is, 0 to 1: the contrast axis and,
    less, the motion axis. A calm, muted brief sits near 0."""
    return clamp(0.6 * axes.contrast + 0.4 * axes.motion)


def status_soft(axes: AxisValues) -> float:
    """The share of its ramp step's chroma a status soft fill keeps, 0.3
    for a calm, muted system to 1 for a loud, lively one, so a calm brief
    gets quiet info, success, warning and danger fills."""
    return round(0.3 + 0.7 * energy(axes), 4)


def dark_band_chroma(axes: AxisValues) -> float:
    """The most chroma a section band takes in dark mode, 0.02 for a muted
    system to 0.08 for a bold one: a dark band is a quiet tint of the
    brand, never a saturated slab."""
    return round(0.02 + 0.06 * axes.contrast, 4)


def light_band_chroma(axes: AxisValues) -> float:
    """The most chroma a section band takes in light mode, 0.015 for a
    muted system to 0.06 for a bold one: a light band spans a whole
    section, so a muted system gets a pale tint of the brand, never a loud
    slab of it."""
    return round(0.015 + 0.045 * axes.contrast, 4)


# The landing display size at body 16px: LANDING_DISPLAY_PX[0] for a
# muted, formal system, rising by up to LANDING_DISPLAY_PX[1] with contrast
# and playfulness.
LANDING_DISPLAY_PX = (56.0, 48.0)


def landing_display_px(axes: AxisValues) -> float:
    """The headline size of a landing page at body 16px, 56 to 104px: bold
    systems go large, and a formal one holds back a little. Contrast counts
    three fifths and playfulness two fifths, so the size is continuous in
    both; the type scale keeps it above the hero."""
    low, span = LANDING_DISPLAY_PX
    return low + span * (0.6 * axes.contrast + 0.4 * (1.0 - axes.formality))


def axes_support_hue(axes: AxisValues) -> float:
    """The supporting accent's hue when the brand has none: violet at
    warmth 0, rose at warmth 1, orchid between, in proportion to warmth
    (GREY_ACCENT). The status hues sit at 25, 75, 150 and 245 degrees and
    lean up to STATUS_BAND with warmth; only the arc from violet to rose
    keeps STATUS_CLEARANCE from all four, so the accent stays on it and
    never reads as danger, warning, success or info."""
    cool, warm = GREY_ACCENT
    return (cool + (warm - cool) * axes.warmth) % 360.0


def saturation(chroma: float) -> float:
    """0 for a grey brand (SAT_CHROMA[0] and below) to 1 for a saturated one
    (SAT_CHROMA[1] and above), in proportion between."""
    return clamp((chroma - SAT_CHROMA[0]) / (SAT_CHROMA[1] - SAT_CHROMA[0]))


def reach(lightness: float, chroma: float) -> float:
    """How far a brand stands apart from the page and from ink, 0 to 1: its
    OKLab distance from the nearer of white and black, 0 at REACH[0] and
    below, 1 at REACH[1] and above, in proportion between. A saturated
    yellow or navy stands well apart from both; a near white tint or a near
    black does not."""
    near = min(math.hypot(1.0 - lightness, chroma), math.hypot(lightness, chroma))
    return clamp((near - REACH[0]) / (REACH[1] - REACH[0]))


def brand_fill_evidence(lightness: float, chroma: float) -> float:
    """How strongly the brand color argues for filling the main action, 0
    to 1: saturated, and standing apart from the page and from ink (reach).
    A near grey, a near white tint or a near black brand argues for accent
    or edge instead; a saturated yellow or navy does not. The text on the
    fill never argues against it here: white or black always reaches 4.58:1
    (the square root of 21) on any color, and the fidelity rule picks
    which."""
    return round(saturation(chroma) * reach(lightness, chroma), 6)


def black_text_cost(lightness: float, chroma: float, dark: bool = False) -> float:
    """What black text on a fill costs in naturalness, in OKLab distance: up
    to BLACK_TEXT_COST on a saturated fill at NATURAL_L[0] or darker,
    nothing on a grey fill or one at NATURAL_L[1] or lighter, in proportion
    between; on a dark page the same ramp sits at NATURAL_L_DARK. The
    fidelity rule weighs it against a move off the brand."""
    lo, hi = NATURAL_L_DARK if dark else NATURAL_L
    return BLACK_TEXT_COST * saturation(chroma) * clamp((hi - lightness) / (hi - lo))


def coolness(hue: float) -> float:
    """How cool a hue reads, 0 to 1: 1 within about 50 degrees of the cool
    anchor (blue and violet), 0.5 a quarter turn away (green, pink), 0 on
    the warm side."""
    return clamp(0.5 + 0.75 * math.cos(math.radians(hue - COOL_HUE)))


def _in_arc(hue: float, arc: Tuple[float, float]) -> bool:
    lo, hi = arc
    return lo <= hue % 360.0 < hi or lo <= hue % 360.0 + 360.0 < hi


def banned_pair(brand_hue: float, support_hue: float) -> bool:
    """Whether a brand hue and a supporting hue make a pairing anti-slop
    bans: a blue brand with a purple or pink accent, a purple brand with a
    blue one, or a cool brand with a pink one (the arcs above)."""
    return (_in_arc(brand_hue, BLUE_ARC)
            and (_in_arc(support_hue, PURPLE_ARC) or _in_arc(support_hue, PINK_ARC))) \
        or (_in_arc(brand_hue, PURPLE_ARC) and _in_arc(support_hue, BLUE_ARC)) \
        or (coolness(brand_hue) >= BANNED_COOL and _in_arc(support_hue, PINK_ARC))


def clear_of_banned(brand_hue: float, hue: float) -> float:
    """The hue itself when it forms no banned pairing with the brand, else
    the first hue that does not on the short arc from it back toward the
    brand hue, in quarter degrees: the edge of the banned arc it sits in, so
    the hue slides along that edge instead of jumping."""
    step = 0.25 if hue_delta(hue, brand_hue) >= 0 else -0.25
    for i in range(1441):
        h = (hue + i * step) % 360.0
        if not banned_pair(brand_hue, h):
            return h
    return brand_hue % 360.0


def _brand_led_support(axes: AxisValues, brand_hue: float) -> float:
    """The support hue a bold, warm or muted brand gets: analogous for a
    muted brand, close to complementary for a bold one, pulled warm or cool
    with warmth."""
    offset = 30.0 + 150.0 * axes.contrast
    anchor = WARM_HUE if axes.warmth >= 0.5 else COOL_HUE
    return mix_hue((brand_hue + offset) % 360.0, anchor, 0.3 * warm_pull(axes))


def family_hue(axes: AxisValues, brand_hue: float) -> float:
    """A cool brand's supporting hue inside its own family: up to
    FAMILY_SPAN degrees from the brand hue, toward higher hues as warmth
    rises and lower as it falls, held closer by formality."""
    return (brand_hue + FAMILY_SPAN * (2.0 * axes.warmth - 1.0)
            * (1.0 - 0.5 * axes.formality)) % 360.0


def support_seed(axes: AxisValues, brand_hue: float,
                 brand_chroma: float) -> Tuple[float, float, float]:
    """(L, C, H) of the supporting accent's seed. A warm brand keeps its
    brand-led accent (_brand_led_support). A cool brand's accent moves in a
    straight line in the OKLab a/b plane to its own family (family_hue, at
    a share of the chroma that contrast raises from SUPPORT_QUIET), as far
    as the brand is cool, in full from QUIET_COOLNESS up, and its hue reads
    (hue_weight). So warmth, formality and contrast still move a cool
    brand's accent, inside its family. That hue counts by hue_weight against
    axes_support_hue, and whatever results is slid out of any banned
    pairing with the brand (clear_of_banned). Chroma is 0.9 of the brand's,
    between 0.06 and 0.16, times the share the lean keeps, times hue_weight:
    an identity with no hue gains none, so a grey brand's accent is a
    neutral step and a nearly grey brand's nearly one."""
    weight = hue_weight(brand_chroma)
    quiet = clamp(coolness(brand_hue) / QUIET_COOLNESS) * weight
    led, share = ab_mix(_brand_led_support(axes, brand_hue), 1.0, family_hue(axes, brand_hue),
                        SUPPORT_QUIET + SUPPORT_LOUD * axes.contrast, quiet)
    hue = ab_mix(axes_support_hue(axes), 1.0, led, 1.0, weight)[0]
    if weight > 0.0:
        # a grey brand's hue is noise and its accent has no chroma to pair
        hue = clear_of_banned(brand_hue, hue)
    return 0.6, min(0.16, max(0.06, 0.9 * brand_chroma)) * share * weight, hue


def support_hue(axes: AxisValues, brand_hue: float, brand_chroma: float) -> float:
    """The supporting accent's hue (support_seed). The warm or cool pull
    turns the short way, so it flips direction where the offset hue sits
    opposite the anchor."""
    return support_seed(axes, brand_hue, brand_chroma)[2]


def brand_role_scores(axes: AxisValues, brand: Optional[float] = None) -> Dict[str, float]:
    """How well each brand role fits. fill: the brand is the action color.
    accent: the brand marks text and links, actions are ink. edge: the brand
    draws edges and rules, actions are ink. The axes score each role; the
    brand's own evidence (brand_fill_evidence, when given) adds BRAND_LEAD
    times itself to fill and BRAND_ARGUE times its absence to accent and
    edge. The brand leads: at full evidence fill wins whatever the axes, and
    accent or edge win only where the brand is very light, very dark or near
    grey, or where a formal brief meets a brand that cannot carry a fill.
    The highest score wins; a brief may name the role instead."""
    scores = {
        "fill": 0.4 * axes.contrast + 0.35 * (1 - axes.formality) + 0.25 * axes.warmth,
        "accent": 0.45 * axes.formality + 0.3 * (1 - axes.contrast)
        + 0.25 * axes.type_personality,
        "edge": 0.5 * axes.formality + 0.3 * (1 - axes.warmth) + 0.2 * (1 - axes.geometry),
    }
    if brand is not None:
        scores["fill"] += BRAND_LEAD * brand
        scores["accent"] += BRAND_ARGUE * (1 - brand)
        scores["edge"] += BRAND_ARGUE * (1 - brand)
    return scores


def brand_role(axes: AxisValues, brand: Optional[float] = None) -> str:
    scores = brand_role_scores(axes, brand)
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
    """Icon stroke on a 24 unit grid, 1.25 to 2.25 in quarters, never
    lighter as the display weight rises (500 and 600 share 1.75)."""
    return round((1.25 + (display_weight(axes) - 300) / 500.0) * 4) / 4


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
