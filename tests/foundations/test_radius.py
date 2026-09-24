"""Radius: a corner scale from the geometry axis, roles on it, pill shapes
for soft brands, and the nesting rule."""
import pytest

from engine.foundations import build_system, to_css
from engine.foundations.gate import gate
from engine.foundations.radius import CHECKS, PILL_PX, base_corner, generate_radius, roles, scale
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(geometry=0.5, **kw):
    values = dict(warmth=0.5, contrast=0.5, density=0.5, geometry=geometry, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


@pytest.mark.parametrize("geometry, base, steps", [
    (0.0, 2, [0, 1, 2, 3, 4, 6, 8]),
    (0.5, 8, [0, 4, 8, 12, 16, 24, 32]),
    (1.0, 12, [0, 6, 12, 18, 24, 36, 48]),
])
def test_scale_follows_the_geometry_axis(geometry, base, steps):
    assert base_corner(geometry) == base and scale(geometry) == steps


def test_primitives_and_roles():
    ts = generate_radius(axes(0.5)).tokens
    assert [t.path for t in ts.tokens() if t.layer == "primitive"] == [
        f"radius.{n}" for n in range(7)] + ["radius.round"]
    assert ts.get("radius.round").value == {"value": PILL_PX, "unit": "px"}
    got = {r: ts.resolve(r)["value"] for r in roles(0.5)}
    assert got == {"radius.joined": 0, "radius.chip": 4, "radius.control": 8, "radius.card": 12,
                   "radius.dialog": 16, "radius.pill": PILL_PX}


def test_soft_brands_move_chips_then_controls_to_pills():
    assert roles(0.59)["radius.chip"] == "radius.1"
    assert roles(0.6)["radius.chip"] == "radius.round"
    assert roles(0.84)["radius.control"] == "radius.2"
    assert roles(0.85)["radius.control"] == "radius.round"
    notes = generate_radius(axes(0.9)).notes
    assert notes == ["radius.chip: pill shape, geometry 0.9 is soft",
                     "radius.control: pill shape, geometry 0.9 is soft"]


@pytest.mark.parametrize("geometry", [i / 20 for i in range(21)])
def test_every_geometry_is_valid_and_passes(geometry):
    ts = generate_radius(axes(geometry)).tokens
    assert validate(ts) == []
    assert gate(ts, [], CHECKS).passed


def test_only_geometry_moves_radius():
    base = [(t.path, t.value) for t in generate_radius(axes()).tokens.tokens()]
    other = axes(warmth=0.0, contrast=1.0, density=0.0, formality=1.0, motion=1.0,
                 type_personality=0.0)
    assert [(t.path, t.value) for t in generate_radius(other).tokens.tokens()] == base


def test_checks_name_the_token_and_the_fix():
    ts = TokenSet()
    for n, v in (("a", 4), ("b", 2), ("c", 20), ("d", 12)):
        ts.add(Token(f"radius.{n}", "dimension", {"value": v, "unit": "px"}))
    ts.add(Token("radius.1", "dimension", {"value": 8, "unit": "px"}))
    ts.add(Token("radius.2", "dimension", {"value": 6, "unit": "px"}))
    ts.add(Token("radius.joined", "dimension", "{radius.a}", layer="semantic"))
    ts.add(Token("radius.card", "dimension", "{radius.c}", layer="semantic"))
    ts.add(Token("radius.dialog", "dimension", "{radius.d}", layer="semantic"))
    ts.add(Token("radius.pill", "dimension", "{radius.c}", layer="semantic"))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "radius.card (20px) is rounder than radius.dialog (12px); a container is never rounder "
        "than the one it sits in, so point radius.dialog at a larger step",
        "radius.joined is 4px; shared edges must be square, so point it at radius.0",
        "radius.pill is 20px; a pill needs a radius larger than any control's height, so point "
        "it at radius.round",
        "radius.2 is not larger than radius.1; keep the radius scale strictly increasing"]


def test_radius_has_no_modes_and_prints_plain_css():
    result = build_system(axes(), "#3366FF")
    assert all(not t.modes for t in result.tokens.tokens() if t.path.startswith("radius."))
    css = to_css(result.tokens)
    assert "  --radius-control: var(--radius-2);" in css and "  --radius-2: 8px;" in css
