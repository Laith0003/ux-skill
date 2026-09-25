"""Rules the generator keeps by construction and an edited or imported set
can break: layout bounds and reflow, the full type ladder, spacing inside
its group, strict radius nesting, and a color set with no dark values."""
import pytest

from engine.foundations import color, layout, radius, space, typography
from engine.foundations.build import build_system
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)


def _failures(ts, checks, check_id):
    report = gate(ts, [], checks, raise_on_fail=False)
    return [f.message for f in report.failures if f.check == check_id]


def _built(*names, axes=NEUTRAL):
    return build_system(axes, "#3366FF", foundations=names).tokens


def _with(ts, *tokens):
    """A copy of `ts` where each given token replaces the one with its path
    (or is added)."""
    new = {t.path: t for t in tokens}
    out = TokenSet(ts.axes)
    for t in ts.tokens():
        out.add(new.pop(t.path, t))
    for t in new.values():
        out.add(t)
    return out


def _px(n):
    return {"value": n, "unit": "px"}


def _rem(n):
    return {"value": n, "unit": "rem"}


# Generated systems pass every new check, at the ends of each axis.

@pytest.mark.parametrize("value", [0.0, 0.5, 1.0])
def test_generated_systems_pass_the_new_checks(value):
    axes = AxisValues(*[value] * 7)
    ts = build_system(axes, "#3366FF").tokens
    new = {"layout-grid-order", "layout-gutter-floor", "reflow-phone-tier", "phone-columns",
           "text-measure-floor", "form-measure", "container-bounds", "type-tracking-order",
           "line-height-floor", "code-face", "space-within-group", "radius-nesting"}
    checks = [c for f in (layout, typography, space, radius) for c in f.CHECKS if c.id in new]
    assert {c.id for c in checks} == new
    report = gate(ts, [], checks, raise_on_fail=False)
    assert report.failures == [], [f.message for f in report.failures]


# Layout: tiers never shrink, compact keeps its floor, reflow at 320px,
# bounded measures and container.

def test_a_wider_tier_never_gets_a_smaller_gutter_or_margin():
    ts = _built("space", "layout")
    ts = _with(ts, Token("layout.gutter.desktop", "dimension", "{space.2}", layer="semantic"))
    assert _failures(ts, layout.CHECKS, "layout-grid-order") == [
        "layout.gutter.desktop (8px) is narrower than layout.gutter.laptop (24px); a wider "
        "viewport never gets a smaller gutter or inline margin, so point layout.gutter.desktop "
        "at a step of 24px or more",
        "layout.gutter.desktop (8px in density:compact) is narrower than layout.gutter.laptop "
        "(20px in density:compact); a wider viewport never gets a smaller gutter or inline "
        "margin, so point layout.gutter.desktop at a step of 20px or more"]


def test_gutters_and_margins_keep_the_8px_floor():
    ts = _built("space", "layout")
    ts = _with(ts, Token("layout.gutter.phone", "dimension", "{space.4}",
                         modes={"density:compact": "{space.1}"}, layer="semantic"))
    assert _failures(ts, layout.CHECKS, "layout-gutter-floor") == [
        "layout.gutter.phone (density:compact) is 4px; our floor for a gutter or inline margin "
        "is 8px in every density, so point it at space.2 (8px) or a larger step"]


def test_the_phone_tier_owns_the_320px_reflow_width():
    ts = _built("space", "layout")
    ts = _with(ts, Token("layout.viewport.300", "dimension", _px(300)),
               Token("layout.breakpoint.tablet", "dimension", "{layout.viewport.300}",
                     layer="semantic"))
    assert _failures(ts, layout.CHECKS, "reflow-phone-tier") == [
        "layout.breakpoint.tablet is 300px, so a 320px viewport gets the tablet grid; WCAG "
        "1.4.10 asks that content reflow at 320 CSS px, so start the tablet tier above 320px"]


def test_the_phone_grid_leaves_room_for_its_columns_at_320px():
    ts = _built("space", "layout")
    ts = _with(ts, Token("layout.margin-inline.phone", "dimension", "{space.24}",
                         layer="semantic"))
    assert _failures(ts, layout.CHECKS, "phone-columns") == [
        "at 320px the phone grid leaves 20px per column (two layout.margin-inline.phone of "
        "96px and 3 layout.gutter.phone of 16px beside 4 columns); our floor is 44px per "
        "column so a column can hold a comfortable target, so narrow the phone margins or "
        "gutters",
        "at 320px the phone grid leaves 23px per column (two layout.margin-inline.phone of "
        "96px and 3 layout.gutter.phone of 12px beside 4 columns in density:compact); our "
        "floor is 44px per column so a column can hold a comfortable target, so narrow the "
        "phone margins or gutters"]


def test_the_reading_measure_has_a_floor_and_the_form_measure_a_cap():
    ts = _built("space", "layout")
    ts = _with(ts, Token("layout.rem.20", "dimension", _rem(20)),
               Token("layout.rem.48", "dimension", _rem(48)),
               Token("layout.measure.text", "dimension", "{layout.rem.20}", layer="semantic"),
               Token("layout.measure.form", "dimension", "{layout.rem.48}", layer="semantic"))
    assert _failures(ts, layout.CHECKS, "text-measure-floor") == [
        "layout.measure.text is 20rem; below our floor of 30rem a reading column breaks lines "
        "every few words, so keep it at 30rem or more"]
    assert _failures(ts, layout.CHECKS, "form-measure") == [
        "layout.measure.form is 48rem; a form wider than the reading measure is read like a "
        "long line, so keep it at 40rem or less, our ceiling for a reading width"]


def test_the_container_is_at_least_the_reflow_width_and_the_measure():
    ts = _built("space", "layout")
    ts = _with(ts, Token("layout.width.300", "dimension", _px(300)),
               Token("layout.container.max", "dimension", "{layout.width.300}",
                     layer="semantic"))
    assert _failures(ts, layout.CHECKS, "container-bounds") == [
        "layout.container.max is 300px, narrower than the 320px reflow width; point it at a "
        "width of 320px or more",
        "layout.container.max is 300px, narrower than layout.measure.text (608px), so a "
        "reading column would not fit; point it at a width of 608px or more"]


# Type: every role has a floor, tracking and leading behave on every role,
# code is monospace.

def _type_field(ts, role, **fields):
    """`ts` with one text role's fields changed and its right-to-left
    override dropped, so both directions read the changed value."""
    t = ts.get(f"type.text.{role}")
    return _with(ts, Token(t.path, t.type, {**t.value, **fields}, modes={}, layer=t.layer))


def test_every_text_role_keeps_the_12px_floor():
    ts = _with(_built("type"), Token("type.size.latin.0", "dimension", _rem(0.625)))
    t = ts.get("type.text.code")
    ts = _with(ts, Token(t.path, t.type, {**t.value, "fontSize": "{type.size.latin.0}"},
                         layer=t.layer))
    assert _failures(ts, typography.CHECKS, "type-sizes") == [
        "type.text.code (direction:ltr) is 10px; it needs at least 12px to stay readable, so "
        "point its fontSize at a larger step",
        "type.text.code (direction:rtl) is 10px; it needs at least 12px to stay readable, so "
        "point its fontSize at a larger step"]


def test_a_smaller_role_never_tracks_tighter_than_a_larger_one():
    ts = _type_field(_built("type"), "heading-3", letterSpacing="{type.tracking.step-8}")
    assert _failures(ts, typography.CHECKS, "type-tracking-order")[0] == (
        "type.text.heading-3 (direction:ltr) tracks at -0.71px, tighter than type.text.heading-2 "
        "(-0.09px) above it; tracking loosens as size falls, so point type.text.heading-3 at a "
        "looser tracking")


def test_every_role_keeps_a_line_height_above_1():
    ts = _with(_built("type"), Token("type.leading.tight", "number", 0.9))
    ts = _type_field(ts, "hero", lineHeight="{type.leading.tight}")
    assert _failures(ts, typography.CHECKS, "line-height-floor") == [
        "type.text.hero (direction:ltr) has line height 0.9; at 1 or less its lines touch, so "
        "point it at a leading above 1",
        "type.text.hero (direction:rtl) has line height 0.9; at 1 or less its lines touch, so "
        "point it at a leading above 1"]


def test_code_keeps_the_reading_leading_and_labels_never_tighten():
    ts = _type_field(_built("type"), "code", lineHeight="{type.leading.latin.2}")
    ts = _type_field(ts, "ui", letterSpacing="{type.tracking.step-5}")
    leading = _failures(ts, typography.CHECKS, "reading-leading")
    tracking = _failures(ts, typography.CHECKS, "reading-tracking")
    assert leading[0] == (
        "type.text.code (direction:ltr) has line height 1.3; running text needs 1.5 or more "
        "(1.4.8), so point it at a taller leading")
    assert tracking[0] == (
        "type.text.ui (direction:ltr) tightens letters to -0.09px; running text keeps 0 or "
        "more, so point it at type.tracking.0")


def test_the_code_face_ends_in_a_monospace_family():
    ts = _with(_built("type"), Token("type.face.mono", "fontFamily", ["Mono Sans", "sans-serif"]))
    assert _failures(ts, typography.CHECKS, "code-face") == [
        "type.face.mono ends in sans-serif; code needs a fixed width, so end its list with "
        "ui-monospace or monospace"]


# Space: component roles stay inside their group.

def test_component_spacing_never_outgrows_the_group_gap():
    ts = _built("space")
    ts = _with(ts, Token("space.card.padding", "dimension", "{space.12}", layer="semantic"),
               Token("space.list.gap", "dimension", "{space.6}", layer="semantic"))
    assert _failures(ts, space.CHECKS, "space-within-group") == [
        "space.list.gap (density:comfortable, 24px) is not smaller than space.group.gap (24px); "
        "rows inside a group sit closer than groups do, so move space.list.gap down the scale",
        "space.card.padding (density:comfortable, 48px) is larger than space.group.gap (24px); "
        "spacing inside a component never outgrows the gap between groups, so move "
        "space.card.padding down the scale",
        "space.list.gap (density:compact, 24px) is not smaller than space.group.gap (20px); "
        "rows inside a group sit closer than groups do, so move space.list.gap down the scale",
        "space.card.padding (density:compact, 48px) is larger than space.group.gap (20px); "
        "spacing inside a component never outgrows the gap between groups, so move "
        "space.card.padding down the scale"]


def test_field_and_table_spacing_stay_inside_the_group():
    ts = _built("space")
    ts = _with(ts, Token("space.table.cell-padding-inline", "dimension", "{space.12}",
                         layer="semantic"),
               Token("space.field.label-gap", "dimension", "{space.10}", layer="semantic"))
    assert _failures(ts, space.CHECKS, "space-within-group") == [
        "space.field.label-gap (density:comfortable, 40px) is larger than space.group.gap "
        "(24px); spacing inside a component never outgrows the gap between groups, so move "
        "space.field.label-gap down the scale",
        "space.table.cell-padding-inline (density:comfortable, 48px) is larger than "
        "space.group.gap (24px); spacing inside a component never outgrows the gap between "
        "groups, so move space.table.cell-padding-inline down the scale",
        "space.field.label-gap (density:compact, 40px) is larger than space.group.gap (20px); "
        "spacing inside a component never outgrows the gap between groups, so move "
        "space.field.label-gap down the scale",
        "space.table.cell-padding-inline (density:compact, 48px) is larger than "
        "space.group.gap (20px); spacing inside a component never outgrows the gap between "
        "groups, so move space.table.cell-padding-inline down the scale"]


# Radius: every nested shape is strictly less round than its container.

def test_equal_card_and_dialog_corners_fail_unless_both_are_square():
    ts = _with(_built("radius"), Token("radius.dialog", "dimension", "{radius.3}",
                                       layer="semantic"))
    assert _failures(ts, radius.CHECKS, "radius-nesting") == [
        "radius.card (11px) is as round as radius.dialog (11px); a shape inside another is "
        "less round than its container, so point radius.dialog at a larger step"]
    square = _with(ts, Token("radius.card", "dimension", "{radius.0}", layer="semantic"),
                   Token("radius.dialog", "dimension", "{radius.0}", layer="semantic"),
                   Token("radius.control", "dimension", "{radius.0}", layer="semantic"),
                   Token("radius.chip", "dimension", "{radius.0}", layer="semantic"))
    assert _failures(square, radius.CHECKS, "radius-nesting") == []


def test_controls_and_chips_nest_inside_cards_pills_aside():
    ts = _with(_built("radius"), Token("radius.control", "dimension", "{radius.5}",
                                       layer="semantic"))
    assert _failures(ts, radius.CHECKS, "radius-nesting") == [
        "radius.control (21px) is rounder than radius.card (11px); a container is never rounder "
        "than the one it sits in, so point radius.card at a larger step"]
    pill = _with(ts, Token("radius.control", "dimension", "{radius.round}", layer="semantic"))
    assert _failures(pill, radius.CHECKS, "radius-nesting") == []


# Color: a set that never says what dark looks like fails in dark.

def test_a_color_set_with_no_dark_values_fails_the_polarity_check():
    ts = _built("color")
    light_only = TokenSet(ts.axes)
    for t in ts.tokens():
        light_only.add(Token(t.path, t.type, t.value, layer=t.layer))
    found = _failures(light_only, color.CHECKS, "scheme-polarity")
    assert found and found[0].startswith(
        "color.surface.page is not darker than color.text.default (scheme:dark,contrast:"
        "standard); a dark scheme needs a darker page")
