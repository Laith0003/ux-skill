"""Character: every axis reaches every foundation it should, continuously,
over a range wide enough to see; the quantities keep their documented
ranges; and industry words written with spaces."""
import functools
import math

import pytest

from engine.foundations import build_system, character, fonts
from engine.foundations.build import FOUNDATIONS
from engine.foundations.color_math import hex_to_oklch
from engine.synthesizer.axes import AXIS_NAMES, AxisValues, compute_axes

from tests.foundations.trials import MID


def _px(v):
    return v["value"] * (16 if v.get("unit") == "rem" else 1)


def _b(hx):
    _, chroma, hue = hex_to_oklch(hx[:7])
    return chroma * math.sin(math.radians(hue))


def _alpha(hx):
    return int(hx[7:9], 16)


def _status_chroma(ts):
    return sum(hex_to_oklch(ts.resolve(f"color.{s}.500"))[1]
               for s in character.STATUS_HUES) / len(character.STATUS_HUES)


# For every axis-to-foundation pair in INFLUENCE, the visible quantities
# that must move as the axis goes from 0 to 1 with the others at 0.5 (brand
# #3366FF unless a fifth item names another): (what, read from the built
# tokens, direction, least total move). Direction 1: it never falls along
# the sweep; -1: it never rises. The least move is ours, about two thirds of
# what the engine moves it. The neutral b is read on a grey brand: the brand
# sets the neutrals' temperature first and warmth only leans them, least
# for a saturated brand (decisions/neutrals-follow-the-brand.md).
QUANTITIES = {
    ("warmth", "color"): (
        ("neutral b of a grey brand, cool to warm",
         lambda ts: _b(ts.resolve("color.neutral.500")), 1, 0.012, "#808080"),
        ("info hue, turning toward the warm hue",
         lambda ts: character.hue_delta(245.0, hex_to_oklch(ts.resolve("color.info.500"))[2]),
         -1, 12.0)),
    ("warmth", "imagery"): (
        ("brand wash alpha", lambda ts: _alpha(ts.resolve("imagery.tint")), 1, 40),),
    ("contrast", "color"): (("mean status chroma", _status_chroma, 1, 0.06),),
    ("contrast", "type"): (
        ("hero size px", lambda ts: _px(ts.resolve("type.text.hero")["fontSize"]), 1, 40),),
    ("contrast", "elevation"): (
        ("card shadow alpha", lambda ts: _alpha(ts.resolve("elevation.card")[0]["color"]),
         1, 25),),
    ("contrast", "border"): (
        ("focus ring px", lambda ts: _px(ts.resolve("border.focus-ring.width")), 1, 1),),
    ("density", "space"): (
        ("card padding px", lambda ts: _px(ts.resolve("space.card.padding")), -1, 12),),
    ("density", "layout"): (
        ("desktop region gap px", lambda ts: _px(ts.resolve("layout.region-gap.desktop")),
         -1, 48),),
    ("density", "type"): (
        ("body line height", lambda ts: ts.resolve("type.text.body")["lineHeight"], -1, 0.08),),
    ("geometry", "radius"): (
        ("control radius px", lambda ts: _px(ts.resolve("radius.control")), 1, 8),),
    ("geometry", "imagery"): (
        ("card image ratio", lambda ts: ts.resolve("imagery.ratio.card"), -1, 0.15),),
    ("formality", "radius"): (
        ("control radius px", lambda ts: _px(ts.resolve("radius.control")), -1, 4),),
    ("formality", "type"): (
        ("label tracking px", lambda ts: ts.resolve("type.tracking.label")["value"], 1, 0.6),),
    ("formality", "elevation"): (
        ("card shadow alpha", lambda ts: _alpha(ts.resolve("elevation.card")[0]["color"]),
         -1, 8),),
    ("formality", "motion"): (
        ("expressive overshoot", lambda ts: ts.resolve("motion.expressive.curve")[1], -1, 0.2),),
    ("formality", "imagery"): (
        ("card image ratio", lambda ts: ts.resolve("imagery.ratio.card"), 1, 0.15),),
    ("motion", "motion"): (
        ("expressive overshoot", lambda ts: ts.resolve("motion.expressive.curve")[1], 1, 0.3),
        ("reveal duration ms", lambda ts: ts.resolve("motion.reveal.duration")["value"],
         1, 100)),
    ("motion", "color"): (
        ("mean status soft fill chroma, a calm brief quieter",
         lambda ts: sum(hex_to_oklch(ts.resolve(f"color.status.{s}.soft"))[1]
                        for s in character.STATUS_HUES) / len(character.STATUS_HUES), 1, 0.009),),
    ("type_personality", "type"): (
        ("display face's type personality",
         lambda ts: fonts.BY_FAMILY[ts.resolve("type.face.display")[0]].place[3], 1, 0.5),),
}


@functools.lru_cache(maxsize=None)
def _sweep(axis, brand="#3366FF"):
    return tuple(build_system(AxisValues(**dict(MID, **{axis: i / 10})), brand).tokens
                 for i in range(11))


def test_influence_names_every_axis_and_real_foundations():
    assert set(character.INFLUENCE) == set(AXIS_NAMES)
    names = {f.name for f in FOUNDATIONS}
    assert all(set(roots) <= names for roots in character.INFLUENCE.values())
    reached = {r for roots in character.INFLUENCE.values() for r in roots}
    assert reached == names


def test_every_influence_pair_names_a_quantity():
    pairs = {(a, r) for a, roots in character.INFLUENCE.items() for r in roots}
    assert set(QUANTITIES) == pairs


@pytest.mark.parametrize("axis, root", sorted(QUANTITIES))
def test_each_axis_moves_a_named_quantity_one_way_and_far_enough(axis, root):
    """Not only that some token under the root changes: each named quantity
    moves one way along the whole sweep, by at least the stated amount."""
    for what, read, direction, least, *brand in QUANTITIES[(axis, root)]:
        values = [direction * read(ts) for ts in _sweep(axis, *brand)]
        steps = [b - a for a, b in zip(values, values[1:])]
        assert min(steps) >= -1e-9, (axis, root, what, values)
        assert values[-1] - values[0] >= least, (axis, root, what, values)


@pytest.mark.parametrize("fn", [character.roundness, character.depth, character.overshoot,
                                character.regularity, character.technical])
def test_derived_quantities_stay_in_range_and_are_continuous(fn):
    values = [fn(AxisValues(*[i / 20] * 7)) for i in range(21)]
    assert all(0.0 <= v <= 1.0 for v in values)
    assert all(abs(b - a) <= 0.1 for a, b in zip(values, values[1:]))


def test_the_neutral_tint_turns_warm_or_cool_without_a_jump_at_the_middle():
    hues = [character.neutral_tint(AxisValues(w / 20, *[0.5] * 6), 264.0) for w in range(21)]
    assert hues[10] == pytest.approx((264.0, 0.008))
    # a brand with a hue holds back half the lean
    most = character.NEUTRAL_C[0] + character.LEAN_C * (1 - character.BRAND_HOLD)
    assert all(chroma <= most + 1e-12 for _, chroma in hues)
    assert abs(hues[9][0] - hues[11][0]) < 30


def test_status_hues_stay_inside_their_band_for_any_brand():
    for status, base in character.STATUS_HUES.items():
        for brand_hue in range(0, 360, 15):
            for warmth in (0.0, 0.5, 1.0):
                _, _, h = character.status_seed(status, AxisValues(warmth, *[0.5] * 6),
                                                float(brand_hue))
                assert abs(character.hue_delta(base, h)) <= character.STATUS_BAND + 1e-9


@pytest.mark.parametrize("axes, want", [
    (AxisValues(*[0.5] * 7), "fill"),
    (AxisValues(0.7, 0.4, 0.5, 0.75, 0.7, 0.1, 0.7), "accent"),
    (AxisValues(0.35, 0.5, 0.6, 0.4, 0.95, 0.25, 0.4), "edge"),
])
def test_the_brand_role_is_the_highest_score_and_fill_wins_a_tie(axes, want):
    assert character.brand_role(axes) == want


@pytest.mark.parametrize("fn, low, high", [
    (character.display_weight, 300, 800), (character.heading_weight, 500, 700)])
def test_weights_span_their_range_in_hundreds(fn, low, high):
    corners = (AxisValues(0.5, 0.0, 0.5, 0.5, 1.0, 0.5, 0.5),
               AxisValues(0.5, 1.0, 0.5, 0.5, 0.0, 0.5, 0.5))
    seen = {fn(AxisValues(*[i / 10] * 7)) for i in range(11)} | {fn(a) for a in corners}
    assert min(seen) == low and max(seen) == high and all(w % 100 == 0 for w in seen)


def test_industry_words_with_spaces_read_as_the_hyphenated_industry():
    assert compute_axes({"industry": "developer tools"}) == \
        compute_axes({"industry": "developer-tools"})


def test_a_status_hue_has_no_seam_where_the_brand_sits_opposite_it():
    for status in character.STATUS_HUES:
        for warmth in (0.0, 0.5, 1.0):
            axes = AxisValues(warmth, *[0.5] * 6)
            hues = [character.status_seed(status, axes, i / 4)[2] for i in range(1441)]
            steps = [abs(character.hue_delta(a, b)) for a, b in zip(hues, hues[1:])]
            assert max(steps) <= 1.0, status


def test_the_brand_lean_holds_away_from_the_opposite_hue_and_is_zero_on_it():
    axes = AxisValues(*[0.5] * 7)
    assert character.status_seed("info", axes, 265.0)[2] == pytest.approx(245.0 + 5.0)
    assert character.status_seed("danger", axes, 265.0)[2] == pytest.approx(13.0)
    assert character.status_seed("danger", axes, 205.0)[2] == pytest.approx(25.0)


def _grid():
    return [AxisValues(*v) for v in
            [(w, c, d, 0.5, f, 0.5, 0.5) for w in (0, 0.5, 1) for c in (0, 0.3, 0.7, 1)
             for d in (0, 1) for f in (0, 0.4, 1)]]


def test_support_hue_is_a_hue():
    for axes in _grid():
        for brand_hue in range(0, 360, 30):
            for brand_chroma in (0.0, 0.02, 0.1):
                hue = character.support_hue(axes, float(brand_hue), brand_chroma)
                assert 0.0 <= hue < 360.0


def test_display_tracking_is_tight_and_bounded():
    values = [character.display_tracking(a) for a in _grid()]
    assert min(values) == pytest.approx(-0.048) and max(values) == pytest.approx(-0.003)


def test_label_tracking_opens_with_formality():
    values = [character.label_tracking(a) for a in _grid()]
    assert min(values) == pytest.approx(0.01) and max(values) == pytest.approx(0.07)


def test_scale_ratio_stays_in_its_documented_range():
    values = [character.scale_ratio(a) for a in _grid()]
    assert min(values) == pytest.approx(1.095) and max(values) == pytest.approx(1.355)


def test_icon_stroke_never_falls_as_the_display_weight_rises():
    by_weight = {}
    for axes in _grid():
        by_weight.setdefault(character.display_weight(axes), set()).add(character.icon_stroke(axes))
    assert all(len(s) == 1 for s in by_weight.values())
    strokes = [by_weight[w].pop() for w in sorted(by_weight)]
    assert sorted(by_weight) == [300, 400, 500, 600, 700, 800]
    assert strokes == [1.25, 1.5, 1.75, 1.75, 2.0, 2.25]


def test_mix_hue_takes_the_shorter_arc_and_stays_a_hue():
    assert character.mix_hue(350.0, 10.0, 0.5) == pytest.approx(0.0)
    assert character.mix_hue(10.0, 350.0, 0.25) == pytest.approx(5.0)
    assert character.mix_hue(40.0, 100.0, 0.0) == 40.0
    assert character.mix_hue(40.0, 100.0, 1.0) == 100.0
    for a in range(0, 360, 45):
        for b in range(0, 360, 45):
            assert 0.0 <= character.mix_hue(float(a), float(b), 0.3) < 360.0


def test_log_position_runs_zero_to_one():
    assert character.log_position(12, 12, 48) == 0.0
    assert character.log_position(48, 12, 48) == 1.0
    assert character.log_position(24, 12, 48) == pytest.approx(0.5)
    assert character.log_position(6, 12, 48) == 0.0
    assert character.log_position(96, 12, 48) == 1.0
    assert character.log_position(20, 12, 12) == 0.0


@pytest.mark.parametrize("args, name", [((0, 12, 48), "size"), ((-4, 12, 48), "size"),
                                        ((24, 0, 48), "low"), ((24, -1, 48), "low")])
def test_log_position_names_the_argument_and_the_fix(args, name):
    with pytest.raises(ValueError, match=rf"^log_position: {name} must be above 0"):
        character.log_position(*args)


def test_a_whitespace_industry_reads_as_no_industry():
    assert compute_axes({"industry": "   "}) == compute_axes({})


@pytest.mark.parametrize("brand_hue", [30.0, 60.0, 144.0, 265.0])
@pytest.mark.parametrize("warmth, anchor", [(0.1, character.COOL_HUE),
                                            (0.9, character.WARM_HUE)])
def test_the_neutral_tint_keeps_the_brand_temperature_whatever_the_warmth(
        brand_hue, warmth, anchor):
    """A blue brand with a warm brief keeps a cool grey, a brown brand with a
    cool brief a warm one: the brand sets the temperature and warmth only
    leans it (decisions/neutrals-follow-the-brand.md)."""
    axes = AxisValues(warmth, *[0.5] * 6)
    hue, chroma = character.neutral_tint(axes, brand_hue)
    assert abs(character.hue_delta(brand_hue, hue)) <= 40.0
    assert chroma <= character.NEUTRAL_C[0] + character.LEAN_C * (1 - character.BRAND_HOLD)


def test_a_grey_brand_s_neutrals_lean_to_the_anchor_at_either_end():
    for warmth, anchor in ((0.0, character.COOL_HUE), (1.0, character.WARM_HUE)):
        for brand_hue in range(0, 360, 15):
            hue, chroma = character.neutral_tint(AxisValues(warmth, *[0.5] * 6),
                                                 float(brand_hue), 0.0)
            assert hue == pytest.approx(anchor) and chroma == pytest.approx(character.LEAN_C)


def test_the_neutral_seed_is_continuous_in_the_brand_hue():
    from engine.foundations.color_math import oklab_distance, oklch_to_hex
    for warmth in (0.0, 0.3, 0.45, 0.55, 0.7, 1.0):
        axes = AxisValues(warmth, *[0.5] * 6)
        seeds = [oklch_to_hex(0.55, *reversed(character.neutral_tint(axes, i / 4)))
                 for i in range(1441)]
        assert max(oklab_distance(a, b) for a, b in zip(seeds, seeds[1:])) <= 0.004, warmth


def test_a_grey_brand_steers_no_hue():
    """An achromatic brand has no stable hue: #808080 reads 0 degrees and
    #7F8080 197. Its hue must not lean the neutrals or the status colors."""
    mid = AxisValues(*[0.5] * 7)
    assert character.hue_weight(0.0) == 0.0 and character.hue_weight(0.2) == 1.0
    assert character.neutral_tint(mid, 197.0, 0.0)[1] == 0.0
    for status, base in character.STATUS_HUES.items():
        for brand_hue in (0.0, 106.0, 197.0):
            assert character.status_seed(status, mid, brand_hue, 0.0)[2] == pytest.approx(base)


def test_a_grey_brand_takes_its_support_hue_from_the_axes():
    """At chroma 0 the brand hue is noise and the accent hue is the axes'
    alone; from HUE_CHROMA up the brand-led hue is kept exactly."""
    for warmth in (0.0, 0.25, 0.5, 0.75, 1.0):
        for contrast in (0.0, 0.5, 1.0):
            axes = AxisValues(warmth, contrast, *[0.5] * 5)
            grey = {character.support_hue(axes, float(h), 0.0) for h in range(0, 360, 15)}
            assert grey == {character.axes_support_hue(axes)}
            for h in range(0, 360, 15):
                offset = 30.0 + 150.0 * contrast
                anchor = character.WARM_HUE if warmth >= 0.5 else character.COOL_HUE
                led = character.mix_hue((h + offset) % 360.0, anchor,
                                        0.3 * character.warm_pull(axes))
                quiet = character.coolness(float(h)) / character.QUIET_COOLNESS
                for chroma in (character.HUE_CHROMA, 0.2):
                    got = character.support_hue(axes, float(h), chroma)
                    # a warm brand keeps its brand-led hue; a cool one stays in
                    # its family (decisions/support-in-the-brand-family.md)
                    if quiet <= 0.0 and not character.banned_pair(float(h), led):
                        assert got == led
                    elif quiet >= 1.0:
                        assert abs(character.hue_delta(float(h), got)) \
                            <= character.FAMILY_SPAN + 1e-6
    assert character.axes_support_hue(AxisValues(0.0, *[0.5] * 6)) == character.GREY_ACCENT[0]
    assert character.axes_support_hue(AxisValues(1.0, *[0.5] * 6)) == character.GREY_ACCENT[1]


def test_the_axes_support_hue_is_continuous_in_warmth():
    hues = [character.axes_support_hue(AxisValues(i / 400, *[0.5] * 6)) for i in range(401)]
    assert max(abs(character.hue_delta(a, b)) for a, b in zip(hues, hues[1:])) <= 0.5


def test_a_grey_brands_accent_keeps_clear_of_every_status_hue():
    """At every warmth, and whatever the other axes, a grey brand's accent
    sits at least STATUS_CLEARANCE from each of the four status hues the
    same system gets, so it never reads as danger or info."""
    for i in range(1001):
        for contrast in (0.0, 1.0):
            axes = AxisValues(i / 1000, contrast, *[0.5] * 5)
            accent = character.support_hue(axes, 0.0, 0.0)
            for status in character.STATUS_HUES:
                hue = character.status_seed(status, axes, 0.0, 0.0)[2]
                assert abs(character.hue_delta(accent, hue)) >= character.STATUS_CLEARANCE, \
                    (i / 1000, status, accent, hue)


@pytest.mark.parametrize("warmth", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_a_grey_brands_built_accent_is_a_neutral_step_that_reads_as_no_status(warmth):
    """An identity with no hue gains none: the accent is a neutral step,
    with too little chroma to read as any hue, a status hue included
    (decisions/grey-support-is-neutral.md)."""
    from engine.foundations.color_math import hex_to_oklch
    ts = build_system(AxisValues(warmth, *[0.5] * 6), "#808080").tokens
    assert hex_to_oklch(ts.resolve("color.support.500"))[1] <= 0.01


# M3.5c item 4: a tone word's formality weight also reaches geometry and
# type personality, continuously: playful words round the corners and
# humanize the type, formal words sharpen the corners.
@pytest.mark.parametrize("word", ["playful", "casual", "friendly", "irreverent"])
def test_a_playful_word_rounds_the_corners_and_humanizes_the_type(word):
    a = compute_axes({"tone": [word]})
    assert a.geometry > 0.5 and a.type_personality > 0.5, (word, a)


@pytest.mark.parametrize("word", ["corporate", "serious", "professional", "clinical"])
def test_a_formal_word_sharpens_the_corners(word):
    assert compute_axes({"tone": [word]}).geometry < 0.5, word


def test_the_reach_is_in_proportion_to_the_word_weight():
    """playful moves formality by -0.30 and casual by -0.25, so playful moves
    geometry six fifths as far: a continuous weight, not a word table."""
    playful = compute_axes({"tone": ["playful"]}).geometry - 0.5
    casual = compute_axes({"tone": ["casual"]}).geometry - 0.5
    assert casual > 0 and abs(playful / casual - 0.30 / 0.25) < 1e-9


def test_a_word_without_a_formality_weight_leaves_geometry_alone():
    for word in ("warm", "bold", "calm", "dense"):
        assert compute_axes({"tone": [word]}).geometry == 0.5, word


def test_a_playful_brief_is_rounder_than_a_formal_one_in_the_built_corners():
    """The trial restaurant (warm, playful) had exactly the formal clinic's
    control and card corners."""
    def corners(brief):
        ts = build_system(compute_axes(brief), "#E85D04").tokens
        return tuple(_px(ts.resolve(r)) for r in ("radius.control", "radius.card"))
    playful = corners({"tone": ["warm", "playful"]})
    formal = corners({"industry": "healthcare", "tone": ["calm", "reassuring"]})
    assert playful[1] > formal[1] and playful[0] >= formal[0], (playful, formal)
