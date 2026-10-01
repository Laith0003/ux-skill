"""The categorical palette: hues for nominal data (chart series, order
states, segments, tags), each with a soft fill, a strong tone, text for the
fill and the page, and text on the strong tone. The hues start on the brand
and step round the wheel, neighbors differ in lightness too, and every
pairing holds in light, dark and high contrast."""
import dataclasses
import itertools

import pytest

from engine.foundations import character
from engine.foundations.color import (
    CATEGORY_ROLES, COLOR_CONTEXTS, PAIRINGS, generate_color)
from engine.foundations.color_math import contrast, hex_to_oklch, oklab_distance, oklch_to_hex
from engine.foundations.gate import required
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5,
                  formality=0.5, motion=0.5, type_personality=0.5)
SEEDS = ["#6B4423", "#3366FF", "#E61428", "#FFD400", "#1F9D55", "#7C3AED", "#13ECDA",
         "#04122E", "#808080"]
N = character.CATEGORY_COUNT
PARTS = ("soft", "strong", "text", "on-strong")


def _with(**kw) -> AxisValues:
    return dataclasses.replace(AXES, **kw)


def _hue_gap(a: float, b: float) -> float:
    return abs(character.hue_delta(a, b))


def test_there_are_six_categories_with_four_parts_each():
    assert N == 6
    assert CATEGORY_ROLES == tuple(f"color.category.{k}.{p}" for k in range(1, N + 1)
                                   for p in PARTS)


@pytest.mark.parametrize("seed", SEEDS)
def test_every_category_role_resolves_in_every_context(seed):
    ts = generate_color(AXES, seed).tokens
    for role in CATEGORY_ROLES:
        for mode in COLOR_CONTEXTS:
            assert ts.resolve(role, mode).startswith("#"), (role, mode)


@pytest.mark.parametrize("seed", SEEDS)
def test_category_pairings_hold_in_every_context(seed):
    ts = generate_color(AXES, seed).tokens
    pairs = [p for p in PAIRINGS if p.fg.startswith("color.category.")]
    assert pairs, "no category pairing is declared"
    for p in pairs:
        for mode in COLOR_CONTEXTS:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= required(p, mode)[0], f"{seed}: {p.fg} on {p.bg} ({mode}) {ratio:.2f}"


def test_the_pairings_cover_each_part():
    pairs = {(p.fg, p.bg) for p in PAIRINGS}
    for k in range(1, N + 1):
        c = f"color.category.{k}"
        assert (f"{c}.text", f"{c}.soft") in pairs
        assert (f"{c}.text", "color.surface.page") in pairs
        assert (f"{c}.text", "color.surface.card") in pairs
        assert (f"{c}.on-strong", f"{c}.strong") in pairs
        assert (f"{c}.strong", "color.surface.page") in pairs
        assert (f"{c}.strong", "color.surface.card") in pairs


def test_the_first_category_sits_on_a_saturated_brand_hue():
    for seed in ("#3366FF", "#E61428", "#1F9D55", "#7C3AED"):
        _, _, brand_h = hex_to_oklch(seed)
        _, _, h = character.category_seed(0, AXES, brand_h, 0.15)
        assert _hue_gap(h, brand_h) < 1e-6, seed


def test_the_seeds_step_evenly_round_the_wheel():
    seeds = [character.category_seed(k, AXES, 40.0, 0.15) for k in range(N)]
    for (_, _, a), (_, _, b) in zip(seeds, seeds[1:]):
        assert abs(_hue_gap(a, b) - 360.0 / N) < 1e-6


def test_neighbors_differ_in_lightness_as_well_as_hue():
    seeds = [character.category_seed(k, AXES, 40.0, 0.15) for k in range(N)]
    for (la, _, _), (lb, _, _) in zip(seeds, seeds[1:]):
        assert abs(la - lb) >= 0.08


@pytest.mark.parametrize("seed", SEEDS)
def test_the_strong_tones_stand_apart_from_each_other(seed):
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        tones = [ts.resolve(f"color.category.{k}.strong", mode) for k in range(1, N + 1)]
        for a, b in itertools.combinations(tones, 2):
            assert oklab_distance(a, b) >= 0.06, (seed, mode, a, b)


def test_a_grey_brand_takes_its_start_from_warmth():
    cool = character.category_seed(0, _with(warmth=0.0), 0.0, 0.0)[2]
    warm = character.category_seed(0, _with(warmth=1.0), 0.0, 0.0)[2]
    assert _hue_gap(cool, warm) > 30.0
    assert abs(cool - character.axes_support_hue(_with(warmth=0.0))) < 1e-6


def test_the_hues_move_continuously_with_the_brand():
    prev = None
    for tenth in range(0, 3601):
        h = tenth / 10.0
        cur = character.category_seed(0, AXES, h, 0.15)[2]
        if prev is not None:
            assert _hue_gap(prev, cur) <= 0.11, h
        prev = cur


def test_chroma_follows_the_contrast_axis():
    quiet = character.category_seed(0, _with(contrast=0.0), 40.0, 0.15)[1]
    loud = character.category_seed(0, _with(contrast=1.0), 40.0, 0.15)[1]
    assert loud > quiet


def test_the_categories_never_read_the_industry():
    import inspect
    src = inspect.getsource(character.category_seed)
    assert "industry" not in src and "keyword" not in src


def test_the_seed_is_a_real_color():
    for k in range(N):
        L, C, H = character.category_seed(k, AXES, 200.0, 0.1)
        assert oklch_to_hex(L, C, H).startswith("#")


def test_the_gate_checks_that_categories_stand_apart():
    from engine.foundations.color import CHECKS, _categories_distinct
    from engine.foundations.tokens import Token
    assert "categories-distinct" in {c.id for c in CHECKS}
    ts = generate_color(AXES, "#3366FF").tokens
    assert _categories_distinct(ts, "scheme:light,contrast:standard") == []
    one = ts.resolve("color.category.1.strong", "scheme:light,contrast:standard")
    ts._tokens["color.category.2.strong"] = Token("color.category.2.strong", "color", one,
                                                  layer="semantic")
    found = _categories_distinct(ts, "scheme:light,contrast:standard")
    assert found and "color.category.2.strong" in found[0] and "point" in found[0]
