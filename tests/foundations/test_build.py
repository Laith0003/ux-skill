import dataclasses
import importlib
import inspect

import pytest

import engine.foundations.build as build_module
import engine.foundations.color as color_module
from engine.foundations import (
    BuildResult, ColorResult, GateFailure, GateFinding, ValidationError, build_color,
    generate_color,
)
from engine.foundations.color import PAIRINGS
from engine.foundations.gate import GateReport, gate
from engine.foundations.ramp import STEPS, RampResult
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
# The package re-exports the gate() function under the submodule's name, so
# "import engine.foundations.gate as m" would bind the function, not the module.
gate_module = importlib.import_module("engine.foundations.gate")


def test_build_returns_tokens_notes_and_the_gate_report():
    # R27 I3: the gate report used to be thrown away.
    result = build_color(AXES, "#FFD400")
    assert isinstance(result, BuildResult)
    assert isinstance(result.report, GateReport) and result.report.passed
    assert result.report.checked == len(PAIRINGS) * 2
    assert result.notes and isinstance(result.notes, tuple)
    assert result.tokens.get("color.brand.500").layer == "primitive"
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.notes = ()


def test_validation_problems_raise_validation_error_with_every_problem(monkeypatch):
    broken = TokenSet()
    broken.add(Token("color.x.500", "color", "#GGGGGG"))
    broken.add(Token("color.text.a", "color", "#444444", layer="semantic"))
    monkeypatch.setattr(build_module, "generate_color",
                        lambda axes, brand_hex: ColorResult(tokens=broken, notes=[]))
    with pytest.raises(ValidationError) as exc:
        build_color(AXES, "#3366FF")
    problems = exc.value.problems
    assert sorted(p.rule for p in problems) == ["bad-value", "semantic-literal"]
    for p in problems:
        assert p.message in str(exc.value)
    assert isinstance(exc.value, ValueError)


def _no_solver(monkeypatch):
    monkeypatch.setattr(color_module, "_solve_action_group", lambda *args, **kwargs: None)


def test_generator_recheck_raises_gate_failure_with_the_seed_hint(monkeypatch):
    # R27 I3: the generator's own re-check goes through gate(), so a
    # failing generated system reaches callers as GateFailure, never a
    # plain ValueError. A yellow seed with the action solver switched off
    # leaves white text on a yellow button.
    _no_solver(monkeypatch)
    with pytest.raises(GateFailure) as exc:
        build_color(AXES, "#FFD400")
    findings = exc.value.report.findings
    on_action = [f for f in findings
                 if (f.fg, f.bg, f.mode) == ("color.text.on-action", "color.action.primary", "light")]
    assert on_action, [f.message() for f in findings]
    assert "choose a darker or more saturated seed" in on_action[0].message()
    assert on_action[0].message() in str(exc.value)


def test_seed_hint_only_for_pairings_the_seed_controls(monkeypatch):
    # A flat neutral ramp fails text on page; the brand seed does not
    # control that pairing, so its message must not tell the user to change it.
    _no_solver(monkeypatch)
    real_ramp = color_module.ramp
    neutral_seed = "#808081"
    monkeypatch.setattr(color_module, "_neutral_seed", lambda brand_hex, axes: neutral_seed)
    monkeypatch.setattr(color_module, "ramp", lambda seed: RampResult(
        stops={s: "#808080" for s in STEPS}, retuned=False, note="")
        if seed == neutral_seed else real_ramp(seed))
    with pytest.raises(GateFailure) as exc:
        generate_color(AXES, "#3366FF")
    text = [f for f in exc.value.report.findings
            if (f.fg, f.bg) == ("color.text.default", "color.surface.page")]
    assert text and all("seed" not in f.message() for f in text)


def test_gate_takes_pairings_explicitly_and_never_imports_color():
    assert inspect.signature(gate).parameters["pairings"].default is inspect.Parameter.empty
    source = inspect.getsource(gate_module)
    assert "foundations.color import" not in source
    assert not hasattr(gate_module, "PAIRINGS")


def test_pairing_lives_in_gate_and_color_reuses_it():
    assert color_module.Pairing is gate_module.Pairing
    assert all(isinstance(p, gate_module.Pairing) for p in PAIRINGS)


def test_public_api():
    import engine.foundations as f
    for name in ("BuildResult", "ValidationError", "GateFinding", "ColorResult", "build_color",
                 "generate_color"):
        assert name in f.__all__
    assert f.build_color is build_module.build_color
    assert f.GateFinding is GateFinding
    assert "build_color" in (generate_color.__doc__ or "")
    import engine.foundations.export as export_module
    assert not hasattr(export_module, "build_color")


# R27 M9: build_color checks its inputs before generating, naming the input and the fix.

@pytest.mark.parametrize("brand_hex", [None, 0x3366FF, b"#3366FF"])
def test_brand_hex_must_be_a_string(brand_hex):
    with pytest.raises(TypeError, match=r"brand_hex is .*; pass the brand color as a hex string, "
                                        r"for example '#3366FF'"):
        build_color(AXES, brand_hex)


@pytest.mark.parametrize("brand_hex", ["blue", "#GGGGGG", "#12345", ""])
def test_brand_hex_must_be_a_hex_color(brand_hex):
    with pytest.raises(ValueError, match=r"brand_hex is .*, which is not a hex color; "
                                         r"use #RRGGBB or #RGB"):
        build_color(AXES, brand_hex)


@pytest.mark.parametrize("brand_hex", ["ff00ff", "#abc", " #3366ff "])
def test_brand_hex_forms_the_generator_accepts_still_build(brand_hex):
    assert build_color(AXES, brand_hex).report.passed


_AXIS_NAMES = [f.name for f in dataclasses.fields(AxisValues)]


def _axes_with(name, value):
    values = dict.fromkeys(_AXIS_NAMES, 0.5)
    values[name] = value
    return AxisValues(**values)


@pytest.mark.parametrize("name", _AXIS_NAMES)
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -0.1, 1.5])
def test_axis_out_of_range_names_the_axis(name, value):
    with pytest.raises(ValueError, match=rf"axes\.{name} is .*; set it to a number from 0 to 1"):
        build_color(_axes_with(name, value), "#3366FF")


@pytest.mark.parametrize("value", [None, "0.5", True])
def test_axis_must_be_a_number(value):
    with pytest.raises(TypeError, match=r"axes\.warmth is .*; set it to a number from 0 to 1"):
        build_color(_axes_with("warmth", value), "#3366FF")


@pytest.mark.parametrize("value", [0, 1, 0.0, 1.0])
def test_axis_bounds_are_inclusive(value):
    assert build_color(_axes_with("warmth", value), "#3366FF").report.passed


def test_axes_must_be_axis_values():
    with pytest.raises(TypeError, match=r"axes is dict; pass an AxisValues"):
        build_color({"warmth": 0.5}, "#3366FF")
