import dataclasses
import importlib
import inspect

import pytest

import engine.foundations.build as build_module
import engine.foundations.color as color_module
from engine.foundations import (
    BuildResult, Check, ColorResult, GateFailure, GateFinding, ValidationError, build_color,
    build_system, generate_color,
)
from engine.foundations.color import PAIRINGS
from engine.foundations.gate import GateReport, gate
from engine.foundations.modes import contexts
from engine.foundations.ramp import STEPS, RampResult
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
gate_module = importlib.import_module("engine.foundations.gate")


def test_build_returns_tokens_notes_and_the_gate_report():
    # R27 I3: the gate report used to be thrown away.
    result = build_color(AXES, "#FFD400")
    assert isinstance(result, BuildResult)
    assert isinstance(result.report, GateReport) and result.report.passed
    assert result.report.checked == len(PAIRINGS) * 4
    assert result.notes and isinstance(result.notes, tuple)
    assert result.tokens.get("color.brand.500").layer == "primitive"
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.notes = ()


def test_validation_problems_raise_validation_error_with_every_problem(monkeypatch):
    broken = TokenSet()
    broken.add(Token("color.x.500", "color", "#GGGGGG"))
    broken.add(Token("color.text.a", "color", "#444444", layer="semantic"))
    monkeypatch.setattr(color_module, "generate_color",
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
                 if (f.fg, f.bg, f.mode) == ("color.text.on-action", "color.action.primary", "scheme:light,contrast:standard")]
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
        build_color(AXES, "#3366FF")
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
                 "build_system", "generate_color", "run_gate", "run_validate", "Foundation",
                 "Generated", "Check", "CheckFailure"):
        assert name in f.__all__
    assert "gate" not in f.__all__ and "validate" not in f.__all__
    assert f.build_color is build_module.build_color
    assert f.run_gate is gate_module.gate
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


# M2 kickoff: one pipeline, generators never gate themselves.

def test_package_attributes_gate_and_validate_are_the_submodules():
    import engine.foundations as f
    import engine.foundations.gate as g
    import engine.foundations.validate as v
    assert inspect.ismodule(f.gate) and inspect.ismodule(f.validate)
    assert inspect.ismodule(g) and inspect.ismodule(v)
    assert f.run_validate is v.validate


def test_build_system_builds_every_registered_foundation():
    result = build_system(AXES, "#3366FF")
    names = {f.name for f in build_module.FOUNDATIONS}
    assert {t.path.split(".", 1)[0] for t in result.tokens.tokens()} == names
    assert result.report.passed
    assert result.report.checked == sum(len(f.pairings) for f in build_module.FOUNDATIONS) * 4
    assert result.report.rules_checked == sum(len(contexts(c.axes)) for f in build_module.FOUNDATIONS
                                              for c in f.checks)


def test_build_color_is_build_system_for_color_alone():
    a, b = build_color(AXES, "#E61428"), build_system(AXES, "#E61428", foundations=("color",))
    assert [(t.path, t.value, t.modes) for t in a.tokens.tokens()] == \
        [(t.path, t.value, t.modes) for t in b.tokens.tokens()]
    assert a.notes == b.notes


def test_unknown_foundation_name_is_rejected():
    with pytest.raises(ValueError, match=r"foundations names 'colour', which is not one of \['color'"):
        build_system(AXES, "#3366FF", foundations=("colour",))


def test_foundations_must_be_a_tuple_of_names():
    with pytest.raises(TypeError, match=r"foundations is the string 'color'; pass a tuple"):
        build_system(AXES, "#3366FF", foundations="color")


@pytest.mark.parametrize("value", [None, 1, "yes"])
def test_arabic_must_be_a_bool(value):
    with pytest.raises(TypeError, match=r"arabic is .*; pass True or False"):
        build_system(AXES, "#3366FF", arabic=value)


def test_generator_returns_instead_of_raising_when_the_gate_would_fail(monkeypatch):
    _no_solver(monkeypatch)
    result = generate_color(AXES, "#FFD400")
    assert isinstance(result, ColorResult) and result.tokens.has("color.action.primary")


def test_check_failures_block_and_carry_their_message():
    ts = TokenSet()
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    check = Check("demo", "system", lambda s, mode: [f"color.base.white fails in {mode}; fix it"],
                  axes=("scheme",))
    with pytest.raises(GateFailure) as exc:
        gate(ts, [], [check])
    report = exc.value.report
    assert [(f.check, f.mode) for f in report.failures] == [("demo", "scheme:light"),
                                                           ("demo", "scheme:dark")]
    assert "color.base.white fails in scheme:dark; fix it" in str(exc.value)
    assert report.rules_checked == 2 and not report.passed


def test_seed_hint_direction_follows_the_other_side(monkeypatch):
    # With the solver off, dark mode keeps white text on a light yellow
    # button. White is lighter than the button, so only a darker seed can
    # help; the M1 hint said "lighter" for every dark-mode finding.
    _no_solver(monkeypatch)
    with pytest.raises(GateFailure) as exc:
        build_color(AXES, "#FFD400")
    dark = [f for f in exc.value.report.findings
            if (f.fg, f.bg, f.mode) == ("color.text.on-action", "color.action.primary", "scheme:dark,contrast:standard")]
    assert dark, [f.message() for f in exc.value.report.findings]
    assert "choose a darker or more saturated seed" in dark[0].message()
