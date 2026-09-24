"""Elevation: two-layer shadows per level and scheme, stronger in dark,
and a strict stacking order."""
import pytest

from engine.foundations import build_system, from_dtcg, to_css, to_dtcg
from engine.foundations.elevation import (
    CHECKS, ORDER, ROLES, generate_elevation, key_alpha, shadow)
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(contrast=0.5, **kw):
    values = dict(warmth=0.5, contrast=contrast, density=0.5, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


def test_a_level_is_a_two_layer_shadow():
    assert shadow(0.5, 2, "light") == [
        {"color": "#0000001D", "offsetX": {"value": 0, "unit": "px"},
         "offsetY": {"value": 2, "unit": "px"}, "blur": {"value": 6, "unit": "px"},
         "spread": {"value": -1, "unit": "px"}},
        {"color": "#0000000E", "offsetX": {"value": 0, "unit": "px"},
         "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 2, "unit": "px"},
         "spread": {"value": 0, "unit": "px"}}]


def test_contrast_axis_sets_strength_and_dark_is_stronger():
    assert [key_alpha(0.0, lvl, "light") for lvl in (1, 2, 3, 4)] == [0.06, 0.075, 0.09, 0.12]
    assert [key_alpha(1.0, lvl, "light") for lvl in (1, 2, 3, 4)] == [0.12, 0.15, 0.18, 0.24]
    assert [key_alpha(1.0, lvl, "dark") for lvl in (1, 2, 3, 4)] == [0.3, 0.375, 0.45, 0.6]


def test_roles_switch_shadows_with_the_scheme():
    ts = generate_elevation(axes()).tokens
    for level, role in enumerate(ROLES, 1):
        tok = ts.get(role)
        assert tok.value == "{elevation.shadow.light.%d}" % level
        assert tok.modes == {"scheme:dark": "{elevation.shadow.dark.%d}" % level}
    assert {r: ts.resolve(r) for r in ORDER} == ORDER


@pytest.mark.parametrize("contrast", [0.0, 0.5, 1.0])
def test_generated_elevation_is_valid_passes_and_round_trips(contrast):
    ts = generate_elevation(axes(contrast)).tokens
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed
    doc = to_dtcg(ts)
    assert doc["elevation"]["shadow"]["light"]["1"]["$value"][0]["color"]["colorSpace"] == "srgb"
    assert to_dtcg(from_dtcg(doc)) == doc


def test_checks_name_the_token_and_the_fix():
    ts = TokenSet()
    ts.add(Token("elevation.s.big", "shadow", shadow(0.5, 4, "light")))
    ts.add(Token("elevation.s.small", "shadow", shadow(0.5, 1, "dark")))
    ts.add(Token("elevation.s.weak", "shadow", shadow(0.0, 1, "light")))
    ts.add(Token("elevation.card", "shadow", "{elevation.s.big}", layer="semantic"))
    ts.add(Token("elevation.lifted", "shadow", "{elevation.s.small}",
                 modes={"scheme:dark": "{elevation.s.weak}"}, layer="semantic"))
    ts.add(Token("elevation.z.a", "number", 5))
    ts.add(Token("elevation.z.b", "number", 1))
    ts.add(Token("elevation.order.base", "number", "{elevation.z.a}", layer="semantic"))
    ts.add(Token("elevation.order.sticky", "number", "{elevation.z.b}", layer="semantic"))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "elevation.lifted (scheme:light) does not rise above elevation.card; a higher level "
        "needs a larger offset and blur and at least the same strength, so point it at a "
        "higher shadow step",
        "elevation.lifted (scheme:dark) does not rise above elevation.card; a higher level "
        "needs a larger offset and blur and at least the same strength, so point it at a "
        "higher shadow step",
        "elevation.card is no stronger in dark than in light; dark surfaces need a stronger "
        "shadow than light to read, so point its scheme:dark override at a stronger shadow",
        "elevation.lifted is no stronger in dark than in light; dark surfaces need a stronger "
        "shadow than light to read, so point its scheme:dark override at a stronger shadow",
        "elevation.order.sticky (1) does not stack above elevation.order.base (5); keep the "
        "order base, sticky, dropdown, overlay, dialog, toast"]


def test_only_contrast_moves_elevation():
    base = [(t.path, t.value) for t in generate_elevation(axes()).tokens.tokens()]
    other = axes(warmth=0.0, density=1.0, geometry=0.0, formality=1.0, motion=0.0,
                 type_personality=1.0)
    assert [(t.path, t.value) for t in generate_elevation(other).tokens.tokens()] == base


def test_build_system_prints_shadows_and_their_dark_switch():
    css = to_css(build_system(axes(), "#3366FF").tokens)
    assert "  --elevation-shadow-light-1: 0px 1px 3px 0px #00000017, 0px 0px 1px 0px #0000000B;" in css
    dark = css.split(':root[data-theme="dark"] {')[1].split("}")[0]
    assert "  --elevation-dialog: var(--elevation-shadow-dark-4);" in dark


def _layer(y, blur, color):
    px = lambda v: {"value": v, "unit": "px"}
    return {"color": color, "offsetX": px(0), "offsetY": px(y), "blur": px(blur), "spread": px(0)}


def test_single_layer_shadows_are_measured_not_crashed_on():
    # DTCG allows a shadow to be one layer object instead of a list.
    ts = TokenSet()
    ts.add(Token("elevation.shadow.one", "shadow", _layer(4, 8, "#00000033")))
    ts.add(Token("elevation.shadow.two", "shadow", [_layer(2, 4, "#00000033")]))
    ts.add(Token("elevation.card", "shadow", "{elevation.shadow.one}", layer="semantic"))
    ts.add(Token("elevation.lifted", "shadow", "{elevation.shadow.two}", layer="semantic"))
    order = [c for c in CHECKS if c.id == "elevation-order"][0]
    msgs = order.run(ts, "")
    assert len(msgs) == 1 and "elevation.lifted" in msgs[0]
    report = gate(ts, [], checks=CHECKS, raise_on_fail=False)
    assert not report.passed


def _roles(**modes):
    """Two shadow steps and order tokens; card and lifted point at them."""
    ts = TokenSet()
    ts.add(Token("elevation.s.one", "shadow", [_layer(1, 3, "#00000026"), _layer(0, 1, "#00000013")]))
    ts.add(Token("elevation.s.one-dark", "shadow", [_layer(1, 3, "#00000060")]))
    ts.add(Token("elevation.s.two", "shadow", [_layer(2, 6, "#00000030")]))
    ts.add(Token("elevation.s.two-dark", "shadow", [_layer(2, 6, "#00000070")]))
    ts.add(Token("elevation.s.clear", "shadow", [_layer(4, 8, "#00000000"), _layer(1, 2, "#00000000")]))
    ts.add(Token("elevation.card", "shadow", "{elevation.s.one}",
                 modes=modes.get("card", {"scheme:dark": "{elevation.s.one-dark}"}),
                 layer="semantic"))
    ts.add(Token("elevation.lifted", "shadow", "{elevation.s.two}",
                 modes=modes.get("lifted", {"scheme:dark": "{elevation.s.two-dark}"}),
                 layer="semantic"))
    ts.add(Token("elevation.z.0", "number", 0))
    ts.add(Token("elevation.z.100", "number", 100))
    ts.add(Token("elevation.order.base", "number", "{elevation.z.0}", layer="semantic"))
    ts.add(Token("elevation.order.sticky", "number", "{elevation.z.100}",
                 modes=modes.get("sticky", {}), layer="semantic"))
    return ts


def test_well_formed_roles_pass():
    ts = _roles()
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed


def test_dark_equal_to_light_fails():
    ts = _roles(card={})
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.message) for f in report.failures] == [
        ("elevation-dark", "elevation.card is no stronger in dark than in light; dark surfaces "
         "need a stronger shadow than light to read, so point its scheme:dark override at a "
         "stronger shadow")]


def test_a_shadow_with_no_visible_layer_fails():
    ts = _roles(lifted={"scheme:dark": "{elevation.s.clear}"})
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    visible = [(f.criterion, f.mode, f.message) for f in report.failures
               if f.check == "visible-shadow"]
    assert visible == [
        ("system", "scheme:dark", "elevation.lifted (scheme:dark) casts no visible shadow; every "
         "layer is fully transparent, so point it at a shadow step with a layer above alpha 0")]


def test_a_dark_override_that_flips_the_stack_fails():
    ts = _roles(sticky={"scheme:dark": "{elevation.z.0}"})
    assert validate(ts) == []
    stacking = [c for c in CHECKS if c.id == "stacking-order"][0]
    assert stacking.axes == ("scheme",)
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures] == [
        ("stacking-order", "scheme:dark", "elevation.order.sticky (0) does not stack above "
         "elevation.order.base (0) under scheme:dark; keep the order base, sticky, dropdown, "
         "overlay, dialog, toast")]


@pytest.mark.parametrize("contrast", [i / 10 for i in range(11)])
def test_generated_dark_shadows_are_strictly_stronger(contrast):
    ts = generate_elevation(axes(contrast)).tokens
    assert gate(ts, [], CHECKS).passed
