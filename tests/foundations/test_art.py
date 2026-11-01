"""Generated brand art: deterministic, decorative, continuous in the axes,
and composed: three layers with a focal shape, open space on one side,
area by palette weight, and a tile that repeats on an even lattice."""
import itertools
import math
import re

import pytest

from engine.foundations import build_system
from engine.foundations.art import (
    FILES, HERO, PALETTE, TILE, accent_side, art_files, digest, hero, play, tile, tile_side,
    weights)
from engine.synthesizer.axes import AxisValues

BRAND, SUPPORT, NEUTRAL = PALETTE
W, H = HERO


def axes(**kw):
    values = dict(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


def draw(a, brand="#3366FF"):
    return art_files(build_system(a, brand).tokens, a, brand)


def rects(svg):
    return [dict(re.findall(r'([\w-]+)="([^"]*)"', r)) for r in re.findall(r"<rect [^>]*/>", svg)]


# Every combination of the three axes art reads, at five points each.
SWEEP = [axes(warmth=w, geometry=g, formality=f)
         for w, g, f in itertools.product((0.0, 0.25, 0.5, 0.75, 1.0), repeat=3)]


def box(s):
    """(left, top, right, bottom) of the box around a shape as turned."""
    c, si = abs(math.cos(math.radians(s.turn))), abs(math.sin(math.radians(s.turn)))
    hw, hh = (s.w * c + s.h * si) / 2, (s.w * si + s.h * c) / 2
    return s.cx - hw, s.cy - hh, s.cx + hw, s.cy + hh


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


@pytest.mark.parametrize("a", SWEEP)
def test_the_hero_is_never_empty_and_draws_back_mid_and_accent(a):
    shapes = hero(a)
    assert [s.role for s in shapes[:2]] == [NEUTRAL, BRAND]
    assert len(shapes) == 2 + accent_side(a) ** 2
    assert all(s.role == SUPPORT for s in shapes[2:])
    # The focal shape is the largest saturated shape.
    assert shapes[1].area > max(s.area for s in shapes[2:])
    assert len(tile(a)) >= tile_side(a) ** 2 >= 4


@pytest.mark.parametrize("a", SWEEP)
def test_the_focal_shape_is_whole_and_a_phone_crop_keeps_it(a):
    shapes = hero(a)
    left, top, right, bottom = box(shapes[1])
    # preserveAspectRatio xMaxYMid slice: a 9:16 box shows the right
    # 9/16 of the height.
    assert left >= W - H * 9 / 16 and right <= W and top >= 0 and bottom <= H
    for s in shapes:
        l, t, r, b = box(s)
        # Nothing is cropped by the canvas, the left third stays open for a
        # heading, and a 16:9 crop (the middle 675 of 800) keeps every shape.
        assert l >= W / 3 - 10 and r <= W and t >= (H - W * 9 / 16) / 2 and b <= H - (
            H - W * 9 / 16) / 2, (s, a)
    svg = draw(a)["art/shapes.svg"]
    assert 'preserveAspectRatio="xMaxYMid slice"' in svg


@pytest.mark.parametrize("a", SWEEP)
def test_drawn_area_follows_the_palette_weights(a):
    shapes = hero(a)
    total = sum(s.area for s in shapes)
    share = {role: sum(s.area for s in shapes if s.role == role) / total for role in PALETTE}
    assert (share[BRAND], share[SUPPORT], share[NEUTRAL]) == pytest.approx(weights(a), abs=1e-9)


def test_the_weights_are_sixty_thirty_ten_at_the_middle_and_warmth_moves_them():
    assert weights(axes()) == pytest.approx((0.30, 0.10, 0.60))
    cool, warm = weights(axes(warmth=0.0)), weights(axes(warmth=1.0))
    assert warm[0] > cool[0] and warm[1] > cool[1] and warm[2] < cool[2]
    assert all(sum(weights(a)) == pytest.approx(1.0) for a in SWEEP)


@pytest.mark.parametrize("a", [x for x in SWEEP if x.formality == 1.0])
def test_formal_art_sits_on_its_lines(a):
    back, focal, *accents = hero(a)
    assert all(s.turn == 0 for s in (back, focal, *accents))
    # The plane's upper corner meets the focal shape's center.
    assert back.cx + back.w / 2 == pytest.approx(focal.cx)
    assert back.cy - back.h / 2 == pytest.approx(focal.cy)
    # The accents are an even grid whose outer edge lines up with the
    # focal shape's, a clear gap below it.
    xs = sorted({round(s.cx, 6) for s in accents})
    ys = sorted({round(s.cy, 6) for s in accents})
    assert len(xs) == len(ys) == 3
    assert xs[1] - xs[0] == pytest.approx(xs[2] - xs[1]) == pytest.approx(ys[1] - ys[0])
    assert max(s.cx + s.w / 2 for s in accents) == pytest.approx(focal.cx + focal.w / 2)
    gap = min(s.cy - s.h / 2 for s in accents) - (focal.cy + focal.h / 2)
    assert gap > 20
    # Accents never touch each other.
    assert xs[1] - xs[0] > accents[0].w


def test_playful_art_is_fewer_larger_turned_shapes():
    formal, playful = hero(axes(formality=1.0)), hero(axes(formality=0.0))
    assert len(playful) == 3 < len(formal)
    assert max(s.area for s in playful[2:]) > 4 * max(s.area for s in formal[2:])
    assert all(s.turn != 0 for s in playful) and play(axes(formality=0.0)) == 1.0
    # A playful accent is a capsule, a silhouette of its own.
    assert playful[2].w > 1.5 * playful[2].h


def test_nearly_formal_art_shows_no_turn_that_reads_as_a_mistake():
    for f in (0.65, 0.8, 0.95):
        assert all(s.turn == 0 for s in hero(axes(formality=f)))
        assert all(s.turn == 0 for s in tile(axes(formality=f)))
    assert play(axes(formality=0.5)) < 0.1


@pytest.mark.parametrize("axis", ["warmth", "geometry", "formality", "contrast"])
@pytest.mark.parametrize("at", [0.13, 0.41, 0.58, 0.87])
def test_art_is_continuous_in_every_axis(axis, at):
    a, b = axes(**{axis: at}), axes(**{axis: at + 0.001})
    for draw_fn in (hero, tile):
        one, two = draw_fn(a), draw_fn(b)
        assert len(one) == len(two)
        for s, t in zip(one, two):
            assert max(abs(s.cx - t.cx), abs(s.cy - t.cy), abs(s.w - t.w), abs(s.h - t.h),
                       abs(s.turn - t.turn)) < 2.0


def test_geometry_alone_rounds_every_layer():
    sharp = rects(draw(axes(geometry=0.0, formality=0.9))["art/shapes.svg"])
    soft = rects(draw(axes(geometry=1.0, formality=0.1))["art/shapes.svg"])
    assert sharp and all(r["rx"] == "0" for r in sharp)
    assert soft and all(float(r["rx"]) * 2 == pytest.approx(
        min(float(r["width"]), float(r["height"])), abs=0.2) for r in soft)
    mid_low = hero(axes(geometry=0.3))
    mid_high = hero(axes(geometry=0.7))
    assert all(p.round_ < q.round_ for p, q in zip(mid_low, mid_high))
    # Each layer keeps its own silhouette: the plane squarer, the focal
    # shape and the accents rounder.
    back, focal, accent = mid_low[0], mid_low[1], mid_low[2]
    assert back.round_ < focal.round_ < accent.round_


def test_the_neutral_is_the_quiet_color():
    svg = draw(axes())["art/shapes.svg"]
    for r in rects(svg):
        quiet = "fill-opacity" in r["style"]
        assert quiet == ("--color-decorative-neutral" in r["style"])


def test_the_tile_is_an_even_lattice_that_repeats_without_seams():
    for a in SWEEP:
        n, pitch = tile_side(a), TILE / tile_side(a)
        shapes = tile(a)
        home = [s for s in shapes if 0 <= s.cx < TILE and 0 <= s.cy < TILE]
        assert len(home) == n * n
        drop = pitch / 2 * play(a)
        for s in home:
            row = round(s.cy / pitch - 0.5)
            col = (s.cx - drop * (row % 2)) / pitch - 0.5
            assert col == pytest.approx(round(col)) and s.cy == pytest.approx((row + 0.5) * pitch)
        # Every shape that crosses an edge has its copy on the far side.
        keys = {(round(s.cx, 3), round(s.cy, 3)) for s in shapes}
        for s in home:
            l, t, r, b = box(s)
            for dx, crosses in ((TILE, l < 0), (-TILE, r > TILE)):
                if crosses:
                    assert (round(s.cx + dx, 3), round(s.cy, 3)) in keys
            for dy, crosses in ((TILE, t < 0), (-TILE, b > TILE)):
                if crosses:
                    assert (round(s.cx, 3), round(s.cy + dy, 3)) in keys
        # Each color takes its share of the cells, give or take one.
        for role, w in zip(PALETTE, weights(a)):
            assert abs(sum(s.role == role for s in home) - w * n * n) <= 1


def test_the_tile_has_an_intrinsic_size_so_it_repeats_at_240px():
    svg = draw(axes())["art/pattern.svg"]
    assert f'viewBox="0 0 {TILE} {TILE}" width="{TILE}" height="{TILE}"' in svg
    assert "preserveAspectRatio" not in svg


def test_the_gradient_id_carries_a_digest_of_the_inputs():
    one = draw(axes())["art/gradient.svg"]
    ids = re.findall(r'id="([^"]+)"', one)
    assert ids == [f"uxs-art-{digest(axes(), '#3366FF')}-wash"]
    assert re.fullmatch(r"uxs-art-[0-9a-f]{8}-wash", ids[0])
    assert f'url(#{ids[0]})' in one and 'id="brand"' not in one
    two = draw(axes(warmth=0.2))["art/gradient.svg"]
    assert re.findall(r'id="([^"]+)"', two) != ids
    assert digest(axes(), "#3366ff") == digest(axes(), "#3366FF")
    # The other two files carry no id at all.
    files = draw(axes())
    assert "id=" not in files["art/shapes.svg"] and "id=" not in files["art/pattern.svg"]


def test_colors_follow_the_page_inline_and_fall_back_to_light():
    ts = build_system(axes(), "#3366FF").tokens
    svg = draw(axes())["art/pattern.svg"]
    light = ts.resolve("color.decorative.brand", "scheme:light")
    assert f"var(--color-decorative-brand, {light})" in svg
