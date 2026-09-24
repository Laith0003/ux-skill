"""Layout: breakpoints, columns, gutters and margins on the spacing scale,
container and reading widths, and the target-size floor."""
import pytest

from engine.foundations import build_system, to_css
from engine.foundations.gate import gate
from engine.foundations.layout import CHECKS, TIERS, container_px, generate_layout
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
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed
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
    assert [f.message for f in report.failures] == [
        "layout.breakpoint.laptop (640px) does not start above layout.breakpoint.tablet "
        "(1024px); keep breakpoints strictly increasing",
        "layout.columns.tablet (8) has fewer columns than layout.columns.phone (12); a wider "
        "viewport never loses columns",
        "layout.target.min (density:comfortable) is 20px; WCAG 2.5.5 asks for 44px targets "
        "here, so point it at layout.width.44 or larger",
        "layout.target.min (density:compact) is 20px; WCAG 2.5.8 asks for 24px targets here, "
        "so point it at layout.width.24 or larger",
        "layout.measure.text is 48rem; lines past about 80 characters tire readers (1.4.8), so "
        "keep it at 40rem or less"]


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
