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
    seen = {fn(AxisValues(*[i / 10] * 7)) for i in range(11)}
    assert min(seen) >= low and max(seen) <= high and all(w % 100 == 0 for w in seen)


def test_industry_words_with_spaces_read_as_the_hyphenated_industry():
    assert compute_axes({"industry": "developer tools"}) == \
        compute_axes({"industry": "developer-tools"})
