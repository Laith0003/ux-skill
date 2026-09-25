"""Generated brand art: deterministic, decorative, and shaped by the axes."""
import re

import pytest

from engine.foundations import build_system
from engine.foundations.art import FILES, art_files, weights
from engine.synthesizer.axes import AxisValues


def axes(**kw):
    values = dict(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


def draw(a, brand="#3366FF"):
    return art_files(build_system(a, brand).tokens, a, brand)


def rects(svg):
    return [dict(re.findall(r'(\w+)="([^"]*)"', r)) for r in re.findall(r"<rect [^>]*/>", svg)]


def test_three_decorative_files_with_no_title():
    files = draw(axes())
    assert tuple(files) == FILES
    for text in files.values():
        assert text.startswith("<!-- Decorative brand art")
        assert 'aria-hidden="true"' in text and 'focusable="false"' in text
        prose = text.replace("<!--", "").replace("-->", "").replace("var(--", "")
        assert "<title" not in text and "--" not in prose


def test_the_same_inputs_draw_the_same_art():
    assert draw(axes()) == draw(axes())
    assert draw(axes()) != draw(axes(), "#E85D04")


def test_geometry_rounds_squares_into_circles():
    sharp = rects(draw(axes(geometry=0.0, formality=1.0))["art/shapes.svg"])
    soft = rects(draw(axes(geometry=1.0, formality=0.0))["art/shapes.svg"])
    assert sharp and all(r["rx"] == "0" for r in sharp)
    assert soft and all(float(r["rx"]) * 2 == pytest.approx(float(r["width"]), abs=0.2)
                        for r in soft)


def test_formality_draws_more_smaller_and_more_regular_shapes():
    formal = rects(draw(axes(formality=1.0))["art/shapes.svg"])
    playful = rects(draw(axes(formality=0.0))["art/shapes.svg"])
    assert len(formal) > len(playful)
    assert max(float(r["width"]) for r in formal) < max(float(r["width"]) for r in playful)
    assert all(r["transform"].startswith("rotate(0 ") for r in formal)


def test_warmth_leans_the_palette_on_the_brand_and_support_accents():
    cool, warm = weights(axes(warmth=0.0)), weights(axes(warmth=1.0))
    assert warm[0] > cool[0] and warm[1] > cool[1] and warm[2] < cool[2]


def test_colors_follow_the_page_inline_and_fall_back_to_light():
    ts = build_system(axes(), "#3366FF").tokens
    svg = draw(axes())["art/pattern.svg"]
    light = ts.resolve("color.decorative.brand", "scheme:light")
    assert f"var(--color-decorative-brand, {light})" in svg
