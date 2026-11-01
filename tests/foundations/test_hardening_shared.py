"""Check hardening shared by every foundation, for token sets the engine did
not generate (an edited tokens.json, an import): values compare in one unit,
scale steps are read in the order of their numbers, roles stay on their own
foundation's scale, a pairing that cannot resolve is a finding, and a set
without one of our axes can still be checked."""
from engine.foundations import border, elevation, layout, motion, radius, space
from engine.foundations.build import build_system
from engine.foundations.gate import Pairing, gate
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.values import REM_PX, dimension_px, duration_ms
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)


def _failures(ts, checks, check_id):
    report = gate(ts, [], checks, raise_on_fail=False)
    return [f.message for f in report.failures if f.check == check_id]


def _built(*names):
    return build_system(NEUTRAL, "#3366FF", foundations=names).tokens


def _replace(ts, path, **changes):
    """A copy of `ts` with one token's fields changed."""
    out = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == path:
            t = Token(t.path, changes.get("type", t.type), changes.get("value", t.value),
                      modes=changes.get("modes", t.modes), layer=changes.get("layer", t.layer))
        out.add(t)
    return out


# One unit: rem reads as 16px, s as 1000ms, wherever a check compares.

def test_the_unit_helpers_convert_rem_and_seconds():
    assert REM_PX == 16
    assert dimension_px({"value": 1.5, "unit": "rem"}) == 24
    assert dimension_px({"value": 12, "unit": "px"}) == 12
    assert duration_ms({"value": 0.2, "unit": "s"}) == 200
    assert duration_ms({"value": 150, "unit": "ms"}) == 150


def test_border_compares_rem_widths_in_pixels():
    ts = _replace(_built("border"), "border.width.2", value={"value": 0.0625, "unit": "rem"})
    # border.emphasis points at border.width.2, now 1px: as heavy as the outline.
    assert _failures(ts, border.CHECKS, "border-weight-order") == [
        "border.emphasis (1px) is not heavier than border.outline (1px), so an emphasized edge "
        "differs from a resting edge by color alone; point border.emphasis at a wider step "
        "than border.outline"]
    assert _failures(ts, border.CHECKS, "border-whole-pixels") == []


def test_border_whole_pixels_reads_rem_in_pixels():
    ts = _replace(_built("border"), "border.width.3", value={"value": 0.1, "unit": "rem"})
    assert _failures(ts, border.CHECKS, "border-whole-pixels") == [
        "border.width.3 is 1.6px; a sub-pixel stroke vanishes on 1x screens, so use a whole "
        "number of pixels"]


def test_radius_compares_rem_corners_in_pixels():
    ts = _replace(_built("radius"), "radius.4", value={"value": 0.25, "unit": "rem"})
    # radius.dialog points at radius.4, now 4px, under the card's radius.3.
    found = _failures(ts, radius.CHECKS, "radius-nesting")
    assert found and found[0].startswith("radius.card (11px) is rounder than radius.dialog (4px)")


def test_elevation_compares_rem_offsets_in_pixels():
    ts = _built("elevation")
    card = ts.get("elevation.shadow.light.1").value
    lifted = [dict(layer) for layer in ts.get("elevation.shadow.light.2").value]
    # 0.1rem is 1.6px and 0.4rem 6.4px, above the card's 1px and 3px, so the
    # order holds in pixels; a unit-blind reading (0.1 < 1) would call it lower.
    lifted[0]["offsetY"] = {"value": 0.1, "unit": "rem"}
    lifted[0]["blur"] = {"value": 0.4, "unit": "rem"}
    ts = _replace(ts, "elevation.shadow.light.2", value=lifted)
    assert card[0]["offsetY"] == {"value": 1, "unit": "px"}
    assert _failures(ts, elevation.CHECKS, "elevation-order") == []


def test_space_and_layout_share_the_rem_reading():
    ts = _replace(_built("space"), "space.3", value={"value": 0.75, "unit": "rem"})
    assert _failures(ts, space.CHECKS, "space-scale-order") == []


# Steps are read in the order of their numbers, not the order a file lists them.

def _reordered(ts, prefix):
    """The same set with the numbered steps under `prefix` listed backwards."""
    steps = [t for t in ts.tokens() if t.path.startswith(prefix)
             and t.path[len(prefix):].isdigit()]
    rest = [t for t in ts.tokens() if t not in steps]
    out = TokenSet(ts.axes)
    for t in list(reversed(steps)) + rest:
        out.add(t)
    return out


def test_a_space_scale_listed_out_of_order_still_passes():
    ts = _reordered(_built("space"), "space.")
    assert _failures(ts, space.CHECKS, "space-scale-order") == []


def test_a_radius_scale_listed_out_of_order_still_passes():
    ts = _reordered(_built("radius"), "radius.")
    assert _failures(ts, radius.CHECKS, "radius-scale-order") == []


def test_a_step_that_breaks_the_order_is_named_by_number():
    ts = _replace(_built("space"), "space.5", value={"value": 12, "unit": "px"})
    assert _failures(ts, space.CHECKS, "space-scale-order") == [
        "space.5 is not larger than space.4; keep the scale strictly increasing"]


# Roles stay on their own foundation's scale.

def test_a_space_role_on_another_foundations_step_is_named():
    ts = _built("space", "radius")
    ts = _replace(ts, "space.card.padding", value="{radius.4}")
    assert _failures(ts, space.CHECKS, "space-on-scale") == [
        "space.card.padding (density:comfortable) points at radius.4, which is not a step of "
        "the spacing scale; spacing values come from space.<n>, so point it at a space step"]


def test_space_steps_sit_on_the_4px_grid():
    ts = _replace(_built("space"), "space.5", value={"value": 22, "unit": "px"})
    assert _failures(ts, space.CHECKS, "space-grid") == [
        "space.5 is 22px, which is not a multiple of 4px; every spacing step sits on the 4px "
        "grid, so round it to 20px or 24px"]


def test_layout_spacing_roles_stay_on_the_spacing_scale():
    ts = _built("space", "layout")
    ts = _replace(ts, "layout.gutter.laptop", value="{layout.width.44}")
    ts = _replace(ts, "layout.region-gap.phone", value="{layout.width.44}")
    ts = _replace(ts, "layout.landing-gap.desktop", value="{layout.width.44}")
    ts = _replace(ts, "layout.footer.padding-block", value="{layout.width.44}")
    assert _failures(ts, layout.CHECKS, "layout-on-space") == [
        f"{role} (density:comfortable) points at layout.width.44, which is not a step of the "
        "spacing scale; layout spacing comes from space.<n>, so point it at a space step"
        for role in ("layout.gutter.laptop", "layout.region-gap.phone",
                     "layout.landing-gap.desktop", "layout.footer.padding-block")]


def test_a_radius_role_on_another_foundations_step_is_named():
    ts = _built("space", "radius")
    ts = _replace(ts, "radius.card", value="{space.3}")
    assert _failures(ts, radius.CHECKS, "radius-on-scale") == [
        "radius.card points at space.3, which is not a step of the radius scale; corners come "
        "from radius.<n> or radius.round, so point it at one of those"]


def test_a_role_aliasing_a_role_of_its_own_foundation_is_judged_at_the_step_it_reaches():
    # An imported set often chains roles: radius.dialog -> radius.card ->
    # radius.<n> is on the scale, and is not reported.
    ts = _replace(_built("radius"), "radius.dialog", value="{radius.card}")
    assert _failures(ts, radius.CHECKS, "radius-on-scale") == []
    ts = _replace(_built("space"), "space.control.gap", value="{space.list.gap}")
    assert _failures(ts, space.CHECKS, "space-on-scale") == []
    # A chain that ends off the scale names the step it reaches.
    ts = _replace(_built("space", "radius"), "radius.card", value="{space.3}")
    ts = _replace(ts, "radius.dialog", value="{radius.card}")
    assert _failures(ts, radius.CHECKS, "radius-on-scale") == [
        f"{role} points at space.3, which is not a step of the radius scale; corners come "
        "from radius.<n> or radius.round, so point it at one of those"
        for role in ("radius.card", "radius.dialog")]


def test_a_step_number_is_ascii_digits_only():
    from engine.foundations.foundation import is_step, numbered_steps
    assert is_step("space.12", "space.") and not is_step("space.\u00b2", "space.")
    ts = _built("space")
    ts.add(Token("space.\u00b2", "dimension", {"value": 99, "unit": "px"}))
    assert "space.\u00b2" not in numbered_steps(ts, "space.", others=False)


def test_distinct_reads_px_through_the_shared_conversion(monkeypatch):
    from engine.foundations import distinct, values
    assert distinct._px({"value": 2, "unit": "rem"}) == dimension_px({"value": 2, "unit": "rem"})
    monkeypatch.setattr(values, "REM_PX", 10)
    assert distinct._px({"value": 2, "unit": "rem"}) == 20


def test_generated_sets_pass_the_scale_checks():
    ts = _built("space", "radius", "layout")
    for checks, check_id in ((space.CHECKS, "space-on-scale"), (space.CHECKS, "space-grid"),
                             (layout.CHECKS, "layout-on-space"),
                             (radius.CHECKS, "radius-on-scale")):
        assert _failures(ts, checks, check_id) == [], check_id


def test_a_role_holding_a_literal_is_not_a_scale_finding():
    # An imported role may hold its value directly; the scale checks judge
    # aliases only, and the value checks still measure it.
    ts = _replace(_built("space"), "space.card.padding",
                  value={"value": 24, "unit": "px"}, modes={})
    assert _failures(ts, space.CHECKS, "space-on-scale") == []


# A pairing whose token cannot be resolved is a finding; the gate goes on.

def test_an_unresolved_pairing_is_a_finding_and_the_gate_goes_on():
    ts = TokenSet()
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    ts.add(Token("color.base.ink", "color", "#111111"))
    ts.add(Token("color.text.default", "color", "{color.gray.900}", layer="semantic"))
    ts.add(Token("color.text.muted", "color", "{color.base.ink}", layer="semantic"))
    ts.add(Token("color.surface.page", "color", "{color.base.white}", layer="semantic"))
    report = gate(ts, [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3"),
                       Pairing("color.text.muted", "color.surface.page", 4.5, "1.4.3")],
                  raise_on_fail=False)
    assert not report.passed and report.findings == []
    assert [(f.check, f.mode) for f in report.failures] == [
        ("unresolved-pairing", "scheme:light,contrast:standard"),
        ("unresolved-pairing", "scheme:light,contrast:high"),
        ("unresolved-pairing", "scheme:dark,contrast:standard"),
        ("unresolved-pairing", "scheme:dark,contrast:high")]
    assert report.failures[0].message == (
        "color.text.default on color.surface.page (scheme:light,contrast:standard) cannot be "
        "measured: color.text.default aliases color.gray.900, which is not defined (resolving "
        "color.text.default). Define color.gray.900 or point color.text.default at an existing "
        "token.")
    assert report.checked == 8


# A set without one of our axes: the motion helpers read the axes it has.

def test_motion_checks_run_on_a_set_without_a_direction_axis():
    built = _built("motion")
    ts = TokenSet({"motion": ("standard", "reduced")})
    for t in built.tokens():
        if t.path == "motion.inline-sign":
            continue
        ts.add(Token(t.path, t.type, t.value, modes=t.modes, layer=t.layer))
    checks = [c for c in motion.CHECKS if c.id != "mirrored-motion"]
    narrowed = [type(c)(c.id, c.criterion, c.run, axes=("motion",)) for c in checks]
    report = gate(ts, [], narrowed, raise_on_fail=False)
    assert report.failures == [], [f.message for f in report.failures]
