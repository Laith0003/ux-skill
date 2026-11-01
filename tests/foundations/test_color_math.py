import re

import pytest

from engine.foundations.color_math import (
    contrast, hex_to_oklch, hex_to_rgb, oklch_to_hex, rgb_to_hex)
from engine.synthesizer.core import _contrast_ratio


def test_hex_roundtrip():
    assert rgb_to_hex(hex_to_rgb("#1a2b3c")) == "#1A2B3C"


@pytest.mark.parametrize(
    "bad", ["#12345", "#GGGGGG", "#abcdef00", "", "##abc", "#-1-1-1", None])
def test_hex_to_rgb_rejects_invalid_input(bad):
    with pytest.raises(ValueError, match=re.escape(repr(bad))):
        hex_to_rgb(bad)


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
    L, C, H = hex_to_oklch(out)
    assert abs(H - 140) <= 2
    assert abs(L - 0.7) <= 0.01


def test_oklch_to_hex_clamps_negative_chroma():
    assert oklch_to_hex(0.6, -0.1, 30) == oklch_to_hex(0.6, 0.0, 30)


def test_oklch_to_hex_rejects_non_finite():
    with pytest.raises(ValueError):
        oklch_to_hex(float("nan"), 0.1, 30)


def test_hex_to_oklch_pinned_red_reference():
    # Reference values (the well-known oklch(62.8% 0.2577 29.23) for pure
    # red) are quoted to 4 decimals for L/C but only 2 for H. The true H is
    # 29.233885..., which rounds to 29.23 at 2dp but is 3.9e-3 away from the
    # literal figure, so H needs a slightly wider band than L/C to hold the
    # same rounded reference without loosening what it pins.
    L, C, H = hex_to_oklch("#FF0000")
    assert L == pytest.approx(0.6280, abs=1e-3)
    assert C == pytest.approx(0.2577, abs=1e-3)
    assert H == pytest.approx(29.23, abs=5e-3)


def test_contrast_matches_known_values_and_synthesizer():
    assert contrast("#FFFFFF", "#000000") == pytest.approx(21.0, abs=0.01)
    assert contrast("#777777", "#FFFFFF") == pytest.approx(4.48, abs=0.01)
    for a, b in [("#6B4423", "#FAF6F2"), ("#3366FF", "#FFFFFF")]:
        assert contrast(a, b) == pytest.approx(
            _contrast_ratio(hex_to_rgb(a), hex_to_rgb(b)), abs=1e-9)


def test_gamut_map_oklch_follows_css_color_4():
    from engine.foundations.color_math import gamut_map_oklch

    # In gamut: the plain conversion, not mapped, no distance to speak of.
    hx, dist, mapped = gamut_map_oklch(0.5, 0.1, 250)
    assert (hx, mapped) == (oklch_to_hex(0.5, 0.1, 250), False) and dist < 0.005
    # Lightness at or past the ends is white or black.
    assert gamut_map_oklch(1.2, 0.3, 30)[0] == "#FFFFFF"
    assert gamut_map_oklch(-0.1, 0.3, 30)[0] == "#000000"
    # Out of gamut: mapped, lightness and hue kept, the same answer every time.
    first = gamut_map_oklch(0.623, 0.214, 259.815)
    assert first[2] is True and first == gamut_map_oklch(0.623, 0.214, 259.815)
    L, C, H = hex_to_oklch(first[0])
    assert abs(L - 0.623) < 0.01 and abs(H - 259.815) < 3 and C < 0.214
    with pytest.raises(ValueError):
        gamut_map_oklch(float("nan"), 0.1, 0)
