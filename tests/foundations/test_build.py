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
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)


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
    # every foundation's checks, plus the one role-types check the build adds
    assert result.report.rules_checked == 1 + sum(len(contexts(c.axes))
                                                  for f in build_module.FOUNDATIONS
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


# The color foundation checks the focus ring against surfaces only; that
# holds because the border foundation guarantees a ring offset.

_RING_NOTE = ("color.focus.ring is checked against surfaces only and relies on "
              "border.focus-ring.offset of at least 1px, which the border foundation "
              "guarantees; build border too, or keep a gap between the element and its ring")


@pytest.mark.parametrize("foundations", [("color",), ("color", "space"), ("color", "radius")])
def test_color_without_border_names_the_ring_assumption(foundations):
    notes = build_system(AXES, "#3366FF", foundations=foundations).notes
    assert notes.count(_RING_NOTE) == 1 and notes[-1] == _RING_NOTE


def test_build_color_carries_the_ring_assumption():
    assert _RING_NOTE in build_color(AXES, "#3366FF").notes


@pytest.mark.parametrize("foundations", [None, ("color", "border"), ("border",), ("space",)])
def test_no_ring_note_when_border_is_built_or_color_is_not(foundations):
    assert _RING_NOTE not in build_system(AXES, "#3366FF", foundations=foundations).notes


@pytest.mark.parametrize("a", [AXES, AxisValues(0, 0, 0, 0, 0, 0, 0),
                               AxisValues(1, 1, 1, 1, 1, 1, 1)])
def test_every_foundation_declares_the_type_of_every_role_it_generates(a):
    result = build_system(a, "#3366FF")
    for f in build_module.FOUNDATIONS:
        assert f.role_types, f"{f.name} declares no role types"
        roles = {t.path: t.type for t in result.tokens.tokens()
                 if t.layer == "semantic" and t.path.split(".", 1)[0] == f.name}
        assert roles == {p: t for p, t in f.role_types.items() if p in roles}
        assert set(roles) <= set(f.role_types)


def _mistype(monkeypatch, module, generator, path, type_, alias):
    real = getattr(module, generator)

    def mistyped(*args):
        generated = real(*args)
        ts = TokenSet()
        for t in generated.tokens.tokens():
            ts.add(Token(path, type_, alias, layer="semantic") if t.path == path else t)
        generated.tokens = ts
        return generated

    monkeypatch.setattr(module, generator, mistyped)


@pytest.mark.parametrize("module, path, type_, alias, names, want, example", [
    ("color", "color.text.default", "dimension", "{space.4}", ("color", "space"), "color",
     "#3366FF"),
    ("color", "color.action.disabled", "dimension", "{space.4}", ("color", "space"), "color",
     "#3366FF"),
    ("space", "space.control.gap", "number", "{elevation.z.100}", ("space", "elevation"),
     "dimension", "{value: 8, unit: px}"),
    ("space", "space.text.gap", "color", "{color.base.white}", ("color", "space"), "dimension",
     "{value: 8, unit: px}"),
    ("radius", "radius.card", "number", "{elevation.z.100}", ("radius", "elevation"),
     "dimension", "{value: 8, unit: px}"),
    ("radius", "radius.joined", "strokeStyle", "{border.line.solid}", ("radius", "border"),
     "dimension", "{value: 8, unit: px}"),
    ("border", "border.focus-ring.width", "strokeStyle", "{border.line.solid}", ("border",),
     "dimension", "{value: 8, unit: px}"),
    ("border", "border.active", "number", "{elevation.z.100}", ("border", "elevation"),
     "dimension", "{value: 8, unit: px}"),
    ("border", "border.style.default", "dimension", "{border.width.1}", ("border",),
     "strokeStyle", "solid"),
    ("elevation", "elevation.card", "dimension", "{space.4}", ("space", "elevation"), "shadow",
     None),
    ("elevation", "elevation.order.sticky", "dimension", "{space.4}", ("space", "elevation"),
     "number", None),
])
def test_a_mistyped_role_in_any_foundation_is_named_once_not_a_crash(
        monkeypatch, module, path, type_, alias, names, want, example):
    mod = importlib.import_module(f"engine.foundations.{module}")
    _mistype(monkeypatch, mod, f"generate_{module}", path, type_, alias)
    with pytest.raises(GateFailure) as err:
        build_system(AXES, "#3366FF", foundations=names)
    report = err.value.report
    assert report.findings == []
    assert [(f.check, f.message) for f in report.failures] == [
        ("role-types", f"{path} is a {type_} but its role expects a {want}; point it at a "
         f"{want} token" + (f", for example {example}" if example else ""))]


def test_a_translucent_paired_role_is_a_gate_failure_not_a_value_error(monkeypatch):
    # A validated set whose paired surface aliases a translucent overlay
    # reaches callers as GateFailure, naming the token and the fix.
    _mistype(monkeypatch, color_module, "generate_color", "color.surface.card", "color",
             "{color.shade.10}")
    with pytest.raises(GateFailure) as err:
        build_color(AXES, "#3366FF")
    failures = err.value.report.failures
    assert failures and {f.check for f in failures} == {"opaque-pairing"}
    first = failures[0]
    assert (first.criterion, first.mode) == ("system", "scheme:light,contrast:standard")
    assert first.message == (
        "color.surface.card (scheme:light,contrast:standard) resolves to the translucent "
        "#0000001A, so color.text.default on color.surface.card cannot be measured; contrast "
        "needs opaque colors, so point color.surface.card at an opaque color, or composite it "
        "over the surface beneath it first and pair the result")
    assert first.message in str(err.value)


def test_a_hint_that_raises_is_recorded_and_the_build_still_fails_cleanly(monkeypatch):
    # Hints run under the same guard as checks: an exception becomes a
    # failure naming the hint, and every finding keeps its own fix.
    _no_solver(monkeypatch)

    def boom(ts, finding):
        raise KeyError("color.brand.500")

    patched = tuple(dataclasses.replace(f, hint=boom) if f.name == "color" else f
                    for f in build_module.FOUNDATIONS)
    monkeypatch.setattr(build_module, "FOUNDATIONS", patched)
    with pytest.raises(GateFailure) as err:
        build_color(AXES, "#FFD400")
    report = err.value.report
    assert report.findings and all(f.hint == "" for f in report.findings)
    hint_failures = [f for f in report.failures if f.check == "color-hint"]
    assert len(hint_failures) == len(report.findings)
    first, finding = hint_failures[0], report.findings[0]
    assert (first.criterion, first.mode) == ("system", finding.mode)
    assert first.message == (
        f"the color hint could not advise on {finding.fg} on {finding.bg} ({finding.mode}) "
        "(KeyError: 'color.brand.500'); that finding keeps its own fix, so move "
        f"{finding.fg} as it says")


def _uncovered(foundation):
    """(check id, axis) for every axis the foundation varies on that a
    check neither walks nor exempts with a stated reason."""
    from engine.foundations.modes import FOUNDATION_AXES
    out = []
    for c in foundation.checks:
        exempt = dict(c.exempt_axes)
        out += [(c.id, a) for a in FOUNDATION_AXES[foundation.name]
                if a not in c.axes and not exempt.get(a, "").strip()]
    return out


def test_every_check_walks_every_axis_its_foundation_varies_on():
    # A check that skips an axis its tokens vary on passes sets that break
    # the rule only in that axis's contexts (an rtl-only reduced travel).
    from engine.foundations.modes import FOUNDATION_AXES
    assert {f.name for f in build_module.FOUNDATIONS} == set(FOUNDATION_AXES)
    for f in build_module.FOUNDATIONS:
        assert _uncovered(f) == [], f.name
        for c in f.checks:
            exempt = dict(c.exempt_axes)
            assert len(exempt) == len(c.exempt_axes), c.id
            assert set(exempt) <= set(FOUNDATION_AXES[f.name]) - set(c.axes), c.id


def test_the_axes_meta_test_catches_a_check_that_skips_an_axis():
    from engine.foundations import motion
    narrow = Check("narrow", "system", lambda ts, mode: [], axes=("motion",))
    reasoned = Check("reasoned", "system", lambda ts, mode: [], axes=("motion",),
                     exempt_axes=(("direction", "reads no directional token"),))
    blank = Check("blank", "system", lambda ts, mode: [], axes=("motion",),
                  exempt_axes=(("direction", " "),))
    f = dataclasses.replace(motion.FOUNDATION, checks=(narrow, reasoned, blank))
    assert _uncovered(f) == [("narrow", "direction"), ("blank", "direction")]
