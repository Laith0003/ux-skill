"""Character: the continuous quantities every foundation reads from the
axes, and industry words written with spaces."""
import pytest

from engine.foundations import character
from engine.synthesizer.axes import AxisValues, compute_axes


@pytest.mark.parametrize("fn", [character.roundness, character.depth, character.overshoot,
                                character.regularity, character.technical])
def test_derived_quantities_stay_in_range_and_are_continuous(fn):
    values = [fn(AxisValues(*[i / 20] * 7)) for i in range(21)]
    assert all(0.0 <= v <= 1.0 for v in values)
    assert all(abs(b - a) <= 0.1 for a, b in zip(values, values[1:]))


def test_the_neutral_tint_turns_warm_or_cool_without_a_jump_at_the_middle():
    hues = [character.neutral_tint(AxisValues(w / 20, *[0.5] * 6), 264.0) for w in range(21)]
    assert hues[10] == (264.0, 0.008)
    assert hues[0][1] == hues[20][1] == pytest.approx(0.03)
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
            assert 0.0 <= character.support_hue(axes, float(brand_hue)) < 360.0


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
