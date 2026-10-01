"""The display line-height floor the lint holds a page to is the least the
engine builds: 1.12 at 40px falling to 0.92 at 160px and above, at any
contrast, with Arabic at least 0.15 above Latin."""
import itertools

import pytest

from engine.foundations import build_system
from engine.foundations.typography import (ARABIC_DISPLAY_GAP, DISPLAY_LEAD, DISPLAY_LEAD_PX,
                                           display_leading, display_leading_floor)
from engine.synthesizer.axes import AxisValues


def test_the_floor_runs_from_the_top_leading_to_the_bold_end():
    assert display_leading_floor(DISPLAY_LEAD_PX[0]) == DISPLAY_LEAD[0]
    assert display_leading_floor(DISPLAY_LEAD_PX[1]) == DISPLAY_LEAD[2]
    assert display_leading_floor(400) == DISPLAY_LEAD[2]
    sizes = [40, 48, 60, 80, 96, 120, 160, 240]
    floors = [display_leading_floor(px) for px in sizes]
    assert floors == sorted(floors, reverse=True)


@pytest.mark.parametrize("px", [40, 64, 120, 200])
def test_arabic_sits_the_display_gap_above_latin(px):
    assert display_leading_floor(px, arabic=True) == round(
        display_leading_floor(px) + ARABIC_DISPLAY_GAP, 2)


@pytest.mark.parametrize("px", [40, 72, 110, 160])
def test_the_floor_is_the_display_leading_at_full_contrast(px):
    bold = AxisValues(0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5)
    assert display_leading_floor(px) == display_leading(bold, px)
    calm = AxisValues(0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5)
    assert display_leading(calm, px) >= display_leading_floor(px)


CORNERS = [AxisValues(w, c, 0.5, 0.5, f, m, 0.5)
           for w, c, f, m in itertools.product((0.1, 0.9), repeat=4)]


@pytest.mark.parametrize("axes", CORNERS[::3])
def test_no_built_display_style_falls_under_the_floor(axes):
    ts = build_system(axes, "#3366FF").tokens
    for role in ("type.text.display", "type.text.hero", "type.text.display-caps"):
        for mode, arabic in (("direction:ltr", False), ("direction:rtl", True)):
            v = ts.resolve(role, mode)
            size = v["fontSize"]
            px = size["value"] * (1 if size["unit"] == "px" else 16)
            assert v["lineHeight"] >= display_leading_floor(px, arabic=arabic) - 0.005, (
                role, mode, px, v["lineHeight"])
