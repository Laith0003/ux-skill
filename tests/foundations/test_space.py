"""Spacing: a 4px-unit scale, roles placed by the density axis, a compact
mode, logical names, and the checks the gate runs on them."""
import pytest

from engine.foundations import build_system, to_css
from engine.foundations.gate import gate
from engine.foundations.space import (
    BASE_UNIT, CHECKS, ROLES, UNITS, compact_units, comfortable_units, generate_space)
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(density=0.5, **kw):
    values = dict(warmth=0.5, contrast=0.5, density=density, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


def px(ts, path, mode=""):
    return ts.resolve(path, mode)["value"]


def test_primitives_are_multiples_of_the_base_unit():
    ts = generate_space(axes()).tokens
    prims = [(t.path, t.value) for t in ts.tokens() if t.layer == "primitive"]
    assert BASE_UNIT == 4
    assert prims == [(f"space.{n}", {"value": 4 * n, "unit": "px"}) for n in UNITS]


def test_mid_density_values():
    ts = generate_space(axes(0.5)).tokens
    want = {"space.control.gap": (12, 8), "space.control.padding-inline": (16, 12),
            "space.control.padding-block": (12, 8), "space.field.label-gap": (8, 4),
            "space.field.message-gap": (8, 4), "space.table.cell-padding-inline": (16, 12),
            "space.table.cell-padding-block": (12, 8), "space.text.gap": (12, 8),
            "space.list.gap": (12, 8), "space.group.gap": (24, 20),
            "space.card.padding": (24, 20), "space.region.gap": (96, 80)}
    got = {r: (px(ts, r, "density:comfortable"), px(ts, r, "density:compact")) for r in ROLES}
    assert got == want


def test_the_density_axis_moves_roles_toward_dense():
    airy, dense = generate_space(axes(0.0)).tokens, generate_space(axes(1.0)).tokens
    for role in ROLES:
        assert px(airy, role) >= px(dense, role), role
    assert px(airy, "space.region.gap") == 128 and px(dense, "space.region.gap") == 64


@pytest.mark.parametrize("density", [i / 20 for i in range(21)])
def test_every_density_passes_the_checks(density):
    ts = generate_space(axes(density)).tokens
    assert validate(ts) == []
    report = gate(ts, [], CHECKS)
    assert report.passed, report.summary()
    for role in ROLES:
        assert compact_units(role, density) <= comfortable_units(role, density)
        assert compact_units(role, density) >= ROLES[role][2]


def test_only_density_moves_spacing():
    base = [(t.path, t.value, t.modes) for t in generate_space(axes()).tokens.tokens()]
    other = axes(warmth=0.0, contrast=1.0, geometry=0.0, formality=1.0, motion=0.0,
                 type_personality=1.0)
    assert [(t.path, t.value, t.modes) for t in generate_space(other).tokens.tokens()] == base


def _hand(gap_px=8, text=12, group=24, region=96, compact_card=24):
    ts = TokenSet()
    for n, v in (("a", gap_px), ("b", text), ("c", group), ("d", region), ("e", compact_card),
                 ("f", 20)):
        ts.add(Token(f"space.{n}", "dimension", {"value": v, "unit": "px"}))
    ts.add(Token("space.control.gap", "dimension", "{space.a}", layer="semantic"))
    ts.add(Token("space.text.gap", "dimension", "{space.b}", layer="semantic"))
    ts.add(Token("space.group.gap", "dimension", "{space.c}", layer="semantic"))
    ts.add(Token("space.region.gap", "dimension", "{space.d}", layer="semantic"))
    ts.add(Token("space.card.padding", "dimension", "{space.f}",
                 modes={"density:compact": "{space.e}"}, layer="semantic"))
    return ts


def test_checks_name_the_token_and_the_fix():
    report = gate(_hand(gap_px=4, text=30, compact_card=24), [], CHECKS, raise_on_fail=False)
    messages = {}
    for f in report.failures:
        messages.setdefault(f.check, f.message)  # first context: comfortable
    assert messages["control-gap"] == (
        "space.control.gap (density:comfortable) is 4px; our floor between adjacent controls "
        "is 8px, so point it at space.2 or larger. WCAG 2.5.8 sets a minimum target of 24 by "
        "24 CSS px, not a gap; this floor keeps smaller controls apart.")
    assert messages["space-hierarchy"].startswith("space.text.gap (density:comfortable) is not "
                                                  "smaller than space.group.gap")
    assert messages["compact-not-larger"].startswith("space.card.padding is larger in compact")
    assert "space.b is not larger than space.a" not in " ".join(messages.values())
    assert [f.message for f in report.failures if f.check == "space-scale-order"] == [
        "space.c is not larger than space.b; keep the scale strictly increasing",
        "space.e is not larger than space.d; keep the scale strictly increasing",
        "space.f is not larger than space.e; keep the scale strictly increasing"]


def test_directional_roles_use_logical_names_and_physical_names_are_rejected():
    ts = generate_space(axes()).tokens
    assert ts.has("space.control.padding-inline") and ts.has("space.control.padding-block")
    ts.add(Token("space.card.padding-left", "dimension", "{space.4}", layer="semantic"))
    found = [p for p in validate(ts) if p.rule == "physical-direction"]
    assert [p.message for p in found] == [
        "space.card.padding-left names the physical side 'left'; left and right swap under "
        "dir=\"rtl\" and top and bottom depend on the writing mode, so token paths use logical "
        "names: use 'inline-start' instead"]


def test_the_control_gap_floor_is_ours_not_a_wcag_gap():
    report = gate(_hand(gap_px=4), [], CHECKS, raise_on_fail=False)
    found = [f for f in report.failures if f.check == "control-gap"]
    assert found and {f.criterion for f in found} == {"system"}
    for f in found:
        assert "our floor between adjacent controls is 8px" in f.message
        assert "not a gap" in f.message
        for claim in ("2.5.8 needs", "2.5.8 requires", "2.5.8 sets a gap", "need at least"):
            assert claim not in f.message


def test_physical_direction_message_says_what_each_side_depends_on():
    ts = generate_space(axes()).tokens
    ts.add(Token("space.card.margin-bottom", "dimension", "{space.4}", layer="semantic"))
    found = [p.message for p in validate(ts) if p.rule == "physical-direction"]
    assert found == [
        "space.card.margin-bottom names the physical side 'bottom'; left and right swap under "
        "dir=\"rtl\" and top and bottom depend on the writing mode, so token paths use logical "
        "names: use 'block-end' instead"]
    assert "flips under" not in found[0]


@pytest.mark.parametrize("name,side", [
    ("paddingLeft", "left"), ("padding_left", "left"), ("padding-left", "left"),
    ("PaddingLeft", "left"), ("backToTop", "top"), ("TOP_BAR", "top")])
def test_physical_words_are_found_in_every_word_form(name, side):
    ts = generate_space(axes()).tokens
    ts.add(Token(f"space.card.{name}", "dimension", "{space.4}", layer="semantic"))
    found = [p.message for p in validate(ts) if p.rule == "physical-direction"]
    assert len(found) == 1 and f"names the physical side '{side}'" in found[0]


@pytest.mark.parametrize("name", ["leftover", "topology", "copyright", "stop", "topbar"])
def test_words_that_only_contain_a_side_pass(name):
    ts = generate_space(axes()).tokens
    ts.add(Token(f"space.card.{name}", "dimension", "{space.4}", layer="semantic"))
    assert [p for p in validate(ts) if p.rule == "physical-direction"] == []


def test_build_system_carries_spacing_and_its_density_css():
    result = build_system(axes(), "#3366FF")
    assert result.tokens.has("space.control.gap")
    css = to_css(result.tokens)
    assert ':root[data-density="compact"] {' in css
    assert "  --space-control-gap: var(--space-2);" in css.split(':root[data-density="compact"] {')[1]
    assert "prefers-density" not in css
