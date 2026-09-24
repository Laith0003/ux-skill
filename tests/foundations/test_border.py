"""Border: whole-pixel widths, stroke styles, roles, and the focus ring's
width and offset."""
import pytest

from engine.foundations import build_system, to_css
from engine.foundations.border import CHECKS, generate_border, roles
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(contrast=0.5, **kw):
    values = dict(warmth=0.5, contrast=contrast, density=0.5, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


def test_primitives():
    ts = generate_border(axes()).tokens
    assert [(t.path, t.type, t.value) for t in ts.tokens() if t.layer == "primitive"] == [
        (f"border.width.{n}", "dimension", {"value": n, "unit": "px"}) for n in (0, 1, 2, 3, 4)
    ] + [(f"border.line.{s}", "strokeStyle", s) for s in ("solid", "dashed", "dotted")]


def test_roles_resolve():
    ts = generate_border(axes()).tokens
    widths = {r: ts.resolve(r)["value"] for r in roles(axes()) if not r.startswith("border.style.")}
    assert widths == {"border.separator": 1, "border.outline": 1, "border.emphasis": 2,
                      "border.active": 2, "border.focus-ring.width": 2,
                      "border.focus-ring.offset": 2}
    assert ts.resolve("border.style.default") == "solid"
    assert ts.resolve("border.style.placeholder") == "dashed"
    assert ts.get("border.style.default").type == "strokeStyle"


def test_dramatic_brands_get_a_bolder_ring():
    assert roles(axes(0.65))["border.focus-ring.width"] == "border.width.2"
    assert roles(axes(0.66))["border.focus-ring.width"] == "border.width.3"
    assert generate_border(axes(0.9)).notes == [
        "border.focus-ring.width: 3px, contrast axis 0.9 is dramatic"]


@pytest.mark.parametrize("contrast", [0.0, 0.5, 0.66, 1.0])
def test_generated_borders_are_valid_and_pass(contrast):
    ts = generate_border(axes(contrast)).tokens
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed


def _hand(ring=1, offset=0, active=0, separator=2, outline=1, emphasis=1, extra=None):
    ts = TokenSet()
    for name, v in (("r", ring), ("o", offset), ("a", active), ("s", separator),
                    ("l", outline), ("e", emphasis)):
        ts.add(Token(f"border.x.{name}", "dimension", {"value": v, "unit": "px"}))
    for role, name in (("border.focus-ring.width", "r"), ("border.focus-ring.offset", "o"),
                       ("border.active", "a"), ("border.separator", "s"),
                       ("border.outline", "l"), ("border.emphasis", "e")):
        ts.add(Token(role, "dimension", "{border.x.%s}" % name, layer="semantic"))
    if extra is not None:
        ts.add(Token("border.width.half", "dimension", {"value": extra, "unit": "px"}))
    return ts


ACTIVE_NOT_WIDER = (
    "border.active ({a}px) is not wider than border.outline ({o}px), so a selected edge differs "
    "from a resting edge by color alone; WCAG 1.4.1 asks that color not be the only visual means "
    "of conveying information, so point border.active at a wider step than border.outline")
EMPHASIS_NOT_HEAVIER = (
    "border.emphasis ({e}px) is not heavier than border.outline ({o}px), so an emphasized edge "
    "differs from a resting edge by color alone; point border.emphasis at a wider step than "
    "border.outline")
SEPARATOR_HEAVIER = (
    "border.separator ({s}px) is heavier than border.outline ({o}px); a separator may match a "
    "resting edge but never outweigh it, so point border.separator at the step border.outline "
    "uses or a lighter one")


def test_checks_name_the_token_and_the_fix():
    report = gate(_hand(extra=0.5), [], CHECKS, raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "border.focus-ring.width is 1px; a focus ring needs at least 2px to be seen, so point it "
        "at border.width.2 or wider",
        "border.focus-ring.width is not wider than border.outline; a ring must stand out from "
        "resting borders, so point it at a wider step",
        "border.focus-ring.offset is 0px; leave at least 1px of page color between the element "
        "and its ring, so point it at border.width.1 or wider",
        ACTIVE_NOT_WIDER.format(a=0, o=1),
        SEPARATOR_HEAVIER.format(s=2, o=1),
        EMPHASIS_NOT_HEAVIER.format(e=1, o=1),
        "border.width.half is 0.5px; a sub-pixel stroke vanishes on 1x screens, so use a whole "
        "number of pixels"]


def _check(check_id):
    return [c for c in CHECKS if c.id == check_id][0]


@pytest.mark.parametrize("active, outline, fails", [
    (0, 1, True), (1, 1, True), (1, 2, True), (2, 1, False), (3, 2, False)])
def test_active_must_be_wider_than_outline(active, outline, fails):
    # A selected edge as thin as a resting edge differs by color alone.
    check = _check("active-border")
    assert check.criterion == "1.4.1"
    msgs = check.run(_hand(active=active, outline=outline, separator=1, emphasis=4), "")
    assert msgs == ([ACTIVE_NOT_WIDER.format(a=active, o=outline)] if fails else [])


def test_active_at_zero_fails_without_an_outline():
    ts = TokenSet()
    ts.add(Token("border.width.0", "dimension", {"value": 0, "unit": "px"}))
    ts.add(Token("border.active", "dimension", "{border.width.0}", layer="semantic"))
    assert _check("active-border").run(ts, "") == [
        "border.active is 0px; a selected state must show more than a color change, so point it "
        "at border.width.1 or wider"]


@pytest.mark.parametrize("separator, outline, emphasis, want", [
    (1, 1, 2, []),
    (0, 1, 2, []),
    (1, 1, 1, [EMPHASIS_NOT_HEAVIER.format(e=1, o=1)]),
    (1, 2, 1, [EMPHASIS_NOT_HEAVIER.format(e=1, o=2)]),
    (2, 1, 2, [SEPARATOR_HEAVIER.format(s=2, o=1)]),
    (3, 2, 2, [SEPARATOR_HEAVIER.format(s=3, o=2), EMPHASIS_NOT_HEAVIER.format(e=2, o=2)]),
])
def test_emphasis_is_heavier_and_separator_never_outweighs_outline(separator, outline, emphasis,
                                                                   want):
    check = _check("border-weight-order")
    assert check.criterion == "system"
    assert check.run(_hand(separator=separator, outline=outline, emphasis=emphasis), "") == want


def test_without_an_outline_emphasis_is_heavier_than_the_separator():
    ts = TokenSet()
    for px in (1, 2):
        ts.add(Token(f"border.width.{px}", "dimension", {"value": px, "unit": "px"}))
    ts.add(Token("border.separator", "dimension", "{border.width.2}", layer="semantic"))
    ts.add(Token("border.emphasis", "dimension", "{border.width.2}", layer="semantic"))
    assert _check("border-weight-order").run(ts, "") == [
        "border.emphasis (2px) is not heavier than border.separator (2px); point border.emphasis "
        "at a wider step than border.separator"]


def test_only_contrast_moves_borders():
    base = [(t.path, t.value) for t in generate_border(axes()).tokens.tokens()]
    other = axes(warmth=0.0, density=1.0, geometry=0.0, formality=1.0, motion=0.0,
                 type_personality=1.0)
    assert [(t.path, t.value) for t in generate_border(other).tokens.tokens()] == base


def test_build_system_prints_border_widths_and_styles():
    css = to_css(build_system(axes(), "#3366FF").tokens)
    assert "  --border-focus-ring-width: var(--border-width-2);" in css
    assert "  --border-line-dashed: dashed;" in css
    assert "  --border-style-placeholder: var(--border-line-dashed);" in css


def _ring_set(offset=None):
    ts = TokenSet()
    ts.add(Token("border.width.1", "dimension", {"value": 1, "unit": "px"}))
    ts.add(Token("border.width.2", "dimension", {"value": 2, "unit": "px"}))
    ts.add(Token("border.focus-ring.width", "dimension", "{border.width.2}", layer="semantic"))
    if offset is not None:
        ts.add(Token("border.width.half", "dimension", {"value": offset, "unit": "px"}))
        ts.add(Token("border.focus-ring.offset", "dimension", "{border.width.half}",
                     layer="semantic"))
    return ts


def test_ring_without_an_offset_is_refused():
    # Without an offset the ring sits on the element's own edge, which is
    # the case the offset rule exists to block.
    ring = [c for c in CHECKS if c.id == "focus-ring"][0]
    msgs = ring.run(_ring_set(), "")
    assert len(msgs) == 1
    assert "border.focus-ring.offset" in msgs[0] and "border.width.1" in msgs[0]


def test_offset_message_states_the_real_value():
    ring = [c for c in CHECKS if c.id == "focus-ring"][0]
    msgs = ring.run(_ring_set(offset=0.5), "")
    assert len(msgs) == 1 and "0.5px" in msgs[0]
