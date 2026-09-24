"""Layout: breakpoints, columns, gutters and margins on the spacing scale,
container and reading widths, and the target-size floor."""
import re

import pytest

from engine.foundations import build_system, layout, space, to_css
from engine.foundations.build import GateFailure
from engine.foundations.foundation import role_types_check
from engine.foundations.gate import gate
from engine.foundations.layout import CHECKS, FOUNDATION, TIERS, container_px, generate_layout
from engine.foundations.space import generate_space
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(density=0.5, **kw):
    values = dict(warmth=0.5, contrast=0.5, density=density, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


def layout_with_space(density=0.5):
    ts = TokenSet()
    for t in generate_space(axes(density)).tokens.tokens() + generate_layout(axes(density)).tokens.tokens():
        ts.add(t)
    return ts


def px(ts, path, mode=""):
    v = ts.resolve(path, mode)
    return v["value"] * (16 if v["unit"] == "rem" else 1)


def test_breakpoints_and_columns():
    ts = layout_with_space()
    assert [px(ts, f"layout.breakpoint.{t}") for t in TIERS[1:]] == [640, 1024, 1280]
    assert [ts.resolve(f"layout.columns.{t}") for t in TIERS] == [4, 8, 12, 12]


def test_gutters_and_margins_ride_the_spacing_scale():
    ts = layout_with_space(0.5)
    assert ts.get("layout.gutter.laptop").value == "{space.6}"
    got = {t: (px(ts, f"layout.gutter.{t}", "density:comfortable"),
               px(ts, f"layout.gutter.{t}", "density:compact")) for t in TIERS}
    assert got == {"phone": (16, 12), "tablet": (20, 16), "laptop": (24, 20), "desktop": (32, 24)}
    margins = {t: px(ts, f"layout.margin-inline.{t}") for t in TIERS}
    assert margins == {"phone": 20, "tablet": 32, "laptop": 40, "desktop": 48}


def test_container_widens_with_density_and_reading_width_does_not():
    assert [container_px(d) for d in (0.0, 0.5, 1.0)] == [1120, 1280, 1440]
    for d in (0.0, 1.0):
        ts = layout_with_space(d)
        assert px(ts, "layout.measure.text") == 38 * 16
        assert ts.resolve("layout.measure.form") == {"value": 32, "unit": "rem"}


@pytest.mark.parametrize("density", [i / 10 for i in range(11)])
def test_every_density_is_valid_and_passes(density):
    ts = layout_with_space(density)
    assert validate(ts) == [] and gate(ts, [], (role_types_check([FOUNDATION]),) + CHECKS).passed
    for tier in TIERS:
        assert px(ts, f"layout.gutter.{tier}", "density:compact") >= 8
    assert px(ts, "layout.target.min", "density:comfortable") == 44
    assert px(ts, "layout.target.min", "density:compact") == 32


def test_checks_name_the_token_and_the_fix():
    ts = TokenSet()
    for n, v in (("a", 1024), ("b", 640), ("t", 20), ("m", 48)):
        ts.add(Token(f"layout.x.{n}", "dimension", {"value": v, "unit": "rem" if n == "m" else "px"}))
    ts.add(Token("layout.c.12", "number", 12))
    ts.add(Token("layout.c.8", "number", 8))
    ts.add(Token("layout.breakpoint.tablet", "dimension", "{layout.x.a}", layer="semantic"))
    ts.add(Token("layout.breakpoint.laptop", "dimension", "{layout.x.b}", layer="semantic"))
    ts.add(Token("layout.columns.phone", "number", "{layout.c.12}", layer="semantic"))
    ts.add(Token("layout.columns.tablet", "number", "{layout.c.8}", layer="semantic"))
    ts.add(Token("layout.target.min", "dimension", "{layout.x.t}", layer="semantic"))
    ts.add(Token("layout.measure.text", "dimension", "{layout.x.m}", layer="semantic"))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    comfortable, compact = "density:comfortable", "density:compact"
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("layout-breakpoints", "system", comfortable,
         "layout.breakpoint.laptop (640px) does not start above layout.breakpoint.tablet "
         "(1024px); keep breakpoints strictly increasing"),
        ("layout-columns", "system", comfortable,
         "layout.columns.tablet (8) has fewer columns than layout.columns.phone (12); a wider "
         "viewport never loses columns"),
        ("target-size-minimum", "2.5.8", comfortable,
         "layout.target.min (density:comfortable) is 20px; WCAG 2.5.8 asks for 24px targets "
         "here, so give it a value of 24px or more"),
        ("target-size-minimum", "2.5.8", compact,
         "layout.target.min (density:compact) is 20px; WCAG 2.5.8 asks for 24px targets here, "
         "so give it a value of 24px or more"),
        ("target-size-comfortable", "2.5.5", comfortable,
         "layout.target.min (density:comfortable) is 20px; WCAG 2.5.5 asks for 44px targets "
         "here, so give it a value of 44px or more"),
        ("text-measure", "1.4.8", comfortable,
         "layout.measure.text is 48rem; lines past about 80 characters tire readers (1.4.8), so "
         "keep it at 40rem or less")]


def _one_role(path, type_, alias, modes=None):
    """A few primitives plus one semantic role: the smallest validate-clean set."""
    ts = TokenSet()
    for n, v, unit in (("a", 640, "px"), ("b", 1024, "px"), ("t", 32, "px"), ("m", 38, "rem"),
                       ("w", 60, "rem")):
        ts.add(Token(f"layout.x.{n}", "dimension", {"value": v, "unit": unit}))
    ts.add(Token("layout.c.8", "number", 8))
    ts.add(Token(path, type_, alias, modes=modes or {}, layer="semantic"))
    return ts


def test_a_comfortable_only_target_miss_cites_2_5_5():
    ts = _one_role("layout.target.min", "dimension", "{layout.x.t}")
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode) for f in report.failures] == [
        ("target-size-comfortable", "2.5.5", "density:comfortable")]


def test_compact_overrides_are_checked():
    ts = _one_role("layout.measure.text", "dimension", "{layout.x.m}",
                   {"density:compact": "{layout.x.w}"})
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("text-measure", "1.4.8", "density:compact",
         "layout.measure.text is 60rem in density:compact; lines past about 80 characters tire "
         "readers (1.4.8), so keep it at 40rem or less")]

    ts = _one_role("layout.breakpoint.laptop", "dimension", "{layout.x.b}",
                   {"density:compact": "{layout.x.a}"})
    ts.add(Token("layout.breakpoint.tablet", "dimension", "{layout.x.a}", layer="semantic"))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures] == [
        ("layout-breakpoints", "density:compact",
         "layout.breakpoint.laptop (640px in density:compact) does not start above "
         "layout.breakpoint.tablet (640px in density:compact); keep breakpoints strictly "
         "increasing")]


@pytest.mark.parametrize("path, type_, alias, actual, want, example", [
    ("layout.breakpoint.tablet", "number", "{layout.c.8}", "number", "dimension",
     "{value: 8, unit: px}"),
    ("layout.columns.tablet", "dimension", "{layout.x.a}", "dimension", "number", None),
    ("layout.target.min", "number", "{layout.c.8}", "number", "dimension",
     "{value: 8, unit: px}"),
    ("layout.measure.text", "number", "{layout.c.8}", "number", "dimension",
     "{value: 8, unit: px}"),
])
def test_a_role_of_the_wrong_type_is_named_once_not_a_crash(path, type_, alias, actual, want,
                                                            example):
    ts = _one_role(path, type_, alias)
    assert validate(ts) == []
    report = gate(ts, [], (role_types_check([FOUNDATION]),) + CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.message) for f in report.failures] == [
        ("role-types", "system",
         f"{path} is a {actual} but its role expects a {want}; point it at a {want} token"
         + (f", for example {example}" if example else ""))]


def test_build_system_checks_role_types(monkeypatch):
    real = layout.generate_layout

    def mistyped(axes):
        generated = real(axes)
        ts = TokenSet()
        for t in generated.tokens.tokens():
            if t.path == "layout.columns.tablet":
                t = Token(t.path, "dimension", "{layout.viewport.640}", layer="semantic")
            ts.add(t)
        generated.tokens = ts
        return generated

    monkeypatch.setattr(layout, "generate_layout", mistyped)
    with pytest.raises(GateFailure) as err:
        build_system(axes(), "#3366FF", foundations=("space", "layout"))
    assert [(f.check, f.message) for f in err.value.report.failures] == [
        ("role-types", "layout.columns.tablet is a dimension but its role expects a number; "
         "point it at a number token")]


def test_layout_steps_come_from_the_spacing_scale(monkeypatch):
    before = {t: px(layout_with_space(0.5), f"layout.gutter.{t}", "density:compact")
              for t in TIERS}
    monkeypatch.setattr(space, "compact_step", lambda comfortable, floor: comfortable)
    ts = layout_with_space(0.5)
    for role in space.ROLES:
        assert space.compact_units(role, 0.5) == space.comfortable_units(role, 0.5)
    after = {t: px(ts, f"layout.gutter.{t}", "density:compact") for t in TIERS}
    assert after == {t: px(ts, f"layout.gutter.{t}", "density:comfortable") for t in TIERS}
    assert all(after[t] > before[t] for t in TIERS)


def test_layout_needs_space_in_the_same_build():
    with pytest.raises(ValueError, match=r"foundations includes 'layout', which aliases 'space' "
                                         r"tokens; add 'space' to foundations"):
        build_system(axes(), "#3366FF", foundations=("layout",))
    assert build_system(axes(), "#3366FF", foundations=("space", "layout")).report.passed


def test_only_density_moves_layout():
    base = [(t.path, t.value, t.modes) for t in generate_layout(axes()).tokens.tokens()]
    other = axes(warmth=0.0, contrast=1.0, geometry=0.0, formality=1.0, motion=1.0,
                 type_personality=0.0)
    assert [(t.path, t.value, t.modes) for t in generate_layout(other).tokens.tokens()] == base


def test_css_uses_logical_margin_names_and_density_blocks():
    css = to_css(build_system(axes(), "#3366FF").tokens)
    assert "  --layout-margin-inline-phone: var(--space-5);" in css
    assert "  --layout-target-min: var(--layout-width-32);" in css.split(
        ':root[data-density="compact"] {')[1]


def test_the_target_fix_names_only_tokens_the_set_has():
    ts = TokenSet()
    for t in layout_with_space(0.5).tokens():
        if t.path == "layout.target.min":
            t = Token(t.path, "dimension", "{layout.width.20}", layer="semantic")
        ts.add(t)
    ts.add(Token("layout.width.20", "dimension", {"value": 20, "unit": "px"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    messages = [f.message for f in report.failures]
    assert messages == [
        "layout.target.min (density:comfortable) is 20px; WCAG 2.5.8 asks for 24px targets "
        "here, so point it at layout.width.32 (32px) or a larger step",
        "layout.target.min (density:compact) is 20px; WCAG 2.5.8 asks for 24px targets here, "
        "so point it at layout.width.32 (32px) or a larger step",
        "layout.target.min (density:comfortable) is 20px; WCAG 2.5.5 asks for 44px targets "
        "here, so point it at layout.width.44 (44px) or a larger step"]
    named = [n for m in messages for n in re.findall(r"\b(?:layout|space)\.[a-z0-9.-]*[a-z0-9]", m)]
    assert named and all(ts.has(n) for n in named)
    assert not ts.has("layout.width.24")


def test_without_widths_the_target_fix_falls_back_to_a_space_step():
    ts = TokenSet()
    for t in generate_space(axes(0.5)).tokens.tokens():
        ts.add(t)
    ts.add(Token("layout.x.t", "dimension", {"value": 40, "unit": "px"}))
    ts.add(Token("layout.target.min", "dimension", "{layout.x.t}", layer="semantic"))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "layout.target.min (density:comfortable) is 40px; WCAG 2.5.5 asks for 44px targets "
        "here, so point it at space.12 (48px) or a larger step"]
