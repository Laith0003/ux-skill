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


# The lint reads the page the way a browser would.

from engine.foundations import to_css  # noqa: E402
from engine.linter.core import lint_text  # noqa: E402

RULE = "display-line-height-under-floor"
LOUD = AxisValues(0.7, 0.9, 0.5, 0.7, 0.1, 0.9, 0.5)
CALM = AxisValues(0.4, 0.2, 0.4, 0.3, 0.8, 0.2, 0.6)


def _page(css, body="<h1>Night market</h1>", lang="en"):
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>Page</title>'
            f"<style>{css}</style></head><body>{body}</body></html>")


def _lines(text, rule=RULE, name="page.html"):
    return [f.line for f in lint_text(name, text) if f.rule_id == rule]


def _system(axes=LOUD, arabic=True):
    return to_css(build_system(axes, "#3366FF", arabic=arabic).tokens)


@pytest.mark.parametrize("size", ["var(--type-text-hero-font-size)",
                                  "var(--type-text-display-font-size)"])
def test_a_size_bound_to_the_engines_system_is_read(size):
    css = _system() + "\nh1{font-size:%s;line-height:.5}" % size
    assert _lines(_page(css))


def test_an_arabic_display_does_not_pass_on_a_latin_leading_token():
    sys_ = build_system(LOUD, "#3366FF").tokens
    latin = sys_.resolve("type.leading.latin.step-10", "")
    css = _system() + "\n:lang(ar) h1{font-size:200px;line-height:%s}" % latin
    assert _lines(_page(css))
    arabic = sys_.resolve("type.leading.arabic.step-10", "")
    css = _system() + "\n:lang(ar) h1{font-size:200px;line-height:%s}" % arabic
    assert not _lines(_page(css))


def test_a_phone_size_is_held_to_the_floor_of_the_desktop_size_it_comes_from():
    css = "@media (max-width:480px){h1{font-size:58px;line-height:.93}}"
    assert not _lines(_page(css))
    css = "@media (max-width:480px){h1{font-size:58px;line-height:.85}}"
    assert _lines(_page(css))


def test_a_shorthand_then_a_longhand_reads_the_last_line_height():
    assert _lines(_page("h1{font:700 80px/1.2 serif;line-height:.8}"))
    assert not _lines(_page("h1{line-height:.8;font:700 80px/1.2 serif}"))


def test_a_negated_rtl_context_is_latin_and_each_selector_is_judged_alone():
    assert not _lines(_page("html:not([dir=rtl]) h1{font-size:80px;line-height:1.05}"))
    assert not _lines(_page("h1, .x{font-size:80px;line-height:1.05}"))
    assert _lines(_page("h1, [dir=rtl] .x{font-size:80px;line-height:1.05}"))


def test_tailwind_display_sizes_without_leading_read_tailwinds_default_of_one():
    assert _lines(_page("", '<h1 class="text-6xl">Night market</h1>'))
    assert not _lines(_page("", '<h1 class="text-9xl">Night market</h1>'))


@pytest.mark.parametrize("decl", [
    "text-transform:uppercase;font-size:var(--type-text-display-caps-font-size)",
    "text-transform:uppercase;font-size:7.5rem",
    "font-size:120px;text-transform:uppercase"])
def test_a_calm_system_reports_display_capitals_in_any_spelling(decl):
    css = _system(CALM, arabic=False) + "\n.p{%s}" % decl
    assert _lines(_page(css, '<h1 class="p">Night</h1>'), rule="all-caps-large")


def test_a_loud_system_keeps_its_capitals_display_bound_by_var():
    css = (_system(LOUD, arabic=False) + "\n.p{text-transform:uppercase;"
           "font-size:var(--type-text-display-caps-font-size);"
           "letter-spacing:var(--type-text-display-caps-letter-spacing)}")
    assert not _lines(_page(css, '<h1 class="p">Night</h1>'), rule="all-caps-large")


def test_small_capitals_labels_in_rem_stay_quiet():
    css = _system(CALM, arabic=False) + "\n.l{text-transform:uppercase;font-size:0.75rem}"
    assert not _lines(_page(css, '<p class="l">New</p>'), rule="all-caps-large")
