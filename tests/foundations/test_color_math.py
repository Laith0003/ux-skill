import pytest

from engine.foundations.color_math import (
    contrast, hex_to_oklch, hex_to_rgb, oklch_to_hex, rgb_to_hex)
from engine.synthesizer.core import _contrast_ratio


def test_hex_roundtrip():
    assert rgb_to_hex(hex_to_rgb("#1a2b3c")) == "#1A2B3C"


@pytest.mark.parametrize("h", ["#FFFFFF", "#000000", "#E61428", "#1F9D55", "#6B4423", "#3366FF"])
def test_oklch_roundtrip_within_one_unit(h):
    back = hex_to_rgb(oklch_to_hex(*hex_to_oklch(h)))
    assert all(abs(a - b) <= 1 for a, b in zip(back, hex_to_rgb(h)))


def test_white_and_black_lightness():
    assert hex_to_oklch("#FFFFFF")[0] == pytest.approx(1.0, abs=1e-3)
    assert hex_to_oklch("#000000")[0] == pytest.approx(0.0, abs=1e-3)


def test_out_of_gamut_is_clamped_not_broken():
    out = oklch_to_hex(0.7, 0.5, 140)
    assert out.startswith("#") and len(out) == 7


def test_contrast_matches_known_values_and_synthesizer():
    assert contrast("#FFFFFF", "#000000") == pytest.approx(21.0, abs=0.01)
    assert contrast("#777777", "#FFFFFF") == pytest.approx(4.48, abs=0.01)
    for a, b in [("#6B4423", "#FAF6F2"), ("#3366FF", "#FFFFFF")]:
        assert contrast(a, b) == pytest.approx(
            _contrast_ratio(hex_to_rgb(a), hex_to_rgb(b)), abs=1e-9)
