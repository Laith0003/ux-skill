import pytest

from engine.foundations.color_math import hex_to_oklch
from engine.foundations.ramp import ANCHOR, STEPS, ramp


@pytest.mark.parametrize("seed", ["#6B4423", "#3366FF", "#E61428", "#1F9D55", "#7C3AED"])
def test_anchor_is_the_seed(seed):
    r = ramp(seed)
    assert list(r.stops) == list(STEPS)
    assert r.stops[ANCHOR] == seed.upper() and not r.retuned


@pytest.mark.parametrize("seed", ["#6B4423", "#3366FF", "#FFE066", "#0B1020"])
def test_lightness_strictly_decreases(seed):
    ls = [hex_to_oklch(h)[0] for h in ramp(seed).stops.values()]
    assert all(a > b for a, b in zip(ls, ls[1:]))


@pytest.mark.parametrize("seed", ["#FFE066", "#0B1020"])
def test_extreme_seed_is_retuned_with_a_note(seed):
    r = ramp(seed)
    assert r.retuned and seed.upper() in r.note and r.stops[ANCHOR] != seed.upper()


def test_deterministic():
    assert ramp("#3366FF").stops == ramp("#3366FF").stops


def test_malformed_hex_raises_value_error():
    with pytest.raises(ValueError):
        ramp("#12345")
