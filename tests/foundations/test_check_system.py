"""check_system: one gate for generated, edited and imported sets. It never
raises for what it finds: structural problems and gate results come back
together, checks run over the axes the set has, and strict mode fails a
pairing it could not check."""
import pytest

from engine.foundations import build as build_module
from engine.foundations.build import (
    FOUNDATIONS, SystemCheck, build_system, check_system, foundations_in)
from engine.foundations.gate import GateFailure
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)


def test_a_generated_set_passes_with_the_same_counts_as_the_build():
    built = build_system(NEUTRAL, "#3366FF")
    result = check_system(built.tokens)
    assert isinstance(result, SystemCheck)
    assert result.passed and result.problems == ()
    assert result.foundations == tuple(f.name for f in FOUNDATIONS)
    assert (result.report.checked, result.report.rules_checked) == (
        built.report.checked, built.report.rules_checked)


def test_the_build_gates_through_the_same_entry_point(monkeypatch):
    seen = []
    real = build_module.gate_foundations

    def spy(ts, chosen, strict=False):
        seen.append((tuple(f.name for f in chosen), strict))
        return real(ts, chosen, strict)

    monkeypatch.setattr(build_module, "gate_foundations", spy)
    build_system(NEUTRAL, "#3366FF", foundations=("color", "border"))
    assert seen == [(("color", "border"), False)]


def test_the_foundations_checked_are_the_roots_the_set_has():
    ts = build_system(NEUTRAL, "#3366FF", foundations=("space", "radius")).tokens
    assert foundations_in(ts) == ("space", "radius")
    assert check_system(ts).foundations == ("space", "radius")


def test_structural_problems_come_back_and_the_gate_still_runs():
    ts = build_system(NEUTRAL, "#3366FF", foundations=("space",)).tokens
    edited = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == "space.control.gap":
            t = Token(t.path, t.type, {"value": 4, "unit": "px"}, layer="semantic")
        edited.add(t)
    result = check_system(edited)
    assert [p.rule for p in result.problems] == ["semantic-literal"]
    assert not result.passed
    assert any(f.check == "control-gap" for f in result.report.failures)


def test_checks_run_over_the_axes_the_set_has():
    built = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    scheme_only = TokenSet({"scheme": ("light", "dark")})
    for t in built.tokens():
        modes = {k: v for k, v in t.modes.items() if "contrast" not in k}
        scheme_only.add(Token(t.path, t.type, t.value, modes=modes, layer=t.layer))
    result = check_system(scheme_only)
    assert result.passed, result.report.summary()
    assert {f.mode for f in result.report.failures} == set()
    # Every color pairing is measured once per scheme, never per contrast.
    assert result.report.checked == 2 * len(build_module.color.PAIRINGS)


def test_strict_mode_fails_a_pairing_it_could_not_check():
    built = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    partial = TokenSet(built.axes)
    for t in built.tokens():
        if t.path != "color.text.link":
            partial.add(t)
    loose = check_system(partial)
    assert loose.passed and loose.report.skipped > 0
    strict = check_system(partial, strict=True)
    assert not strict.passed
    skipped = [f for f in strict.report.failures if f.check == "skipped-pairing"]
    assert len(skipped) == loose.report.skipped
    assert skipped[0].message == (
        "color.text.link on color.surface.page was not checked because color.text.link is not "
        "defined; define it, or for an imported system map the role to one of its tokens")


# The character roles: brand and accent surfaces, media and art colors, code
# colors, the phone scale, icons, display styles, page regions and the
# field and table spacing. A system the engine did not generate may have
# none of them.
CHARACTER = (
    "color.surface.tint", "color.surface.band", "color.surface.stripe", "color.surface.header",
    "color.surface.brand", "color.surface.code", "color.text.on-brand", "color.text.on-media",
    "color.text.accent", "color.text.support", "color.line.accent", "color.line.danger",
    "color.action.primary-edge", "color.decorative.", "color.illustration.", "color.syntax.",
    "color.logo", "color.media.", "imagery.", "type.phone.", "type.icon.", "type.run.",
    "type.text.section-title", "type.text.figure", "type.text.label", "type.text.ui-large",
    "radius.box", "radius.area", "radius.media", "layout.region-gap.", "layout.hero.",
    "layout.header.", "layout.footer.", "layout.target.large", "space.field.", "space.table.",
    "space.control.padding-inline-large", "space.control.padding-block-large",
    "elevation.inset", "motion.expressive.")


def test_a_set_without_the_character_roles_passes_and_strict_names_each_gap():
    built = build_system(NEUTRAL, "#3366FF").tokens
    plain = TokenSet(built.axes)
    for t in built.tokens():
        if not (t.layer == "semantic" and t.path.startswith(CHARACTER)):
            plain.add(t)
    loose = check_system(plain)
    assert loose.passed, loose.report.summary()
    strict = check_system(plain, strict=True)
    failed = {f.check for f in strict.report.failures}
    assert failed == {"skipped-pairing"}
    assert len(strict.report.failures) == loose.report.skipped


def test_a_set_with_no_foundation_the_engine_knows_checks_nothing():
    ts = TokenSet({})
    ts.add(Token("brand.ink", "color", "#111111"))
    result = check_system(ts)
    assert result.foundations == () and result.passed
    assert result.report.checked == 0 and result.report.rules_checked == 0


def test_unknown_foundation_names_are_refused():
    with pytest.raises(ValueError, match="foundations names 'colour'"):
        check_system(TokenSet(), foundations=("colour",))


def test_the_build_still_raises_on_a_failing_gate_with_hints(monkeypatch):
    # With the fill solver off, white text sits on a yellow button.
    monkeypatch.setattr(build_module.color, "_solve_group", lambda *args, **kwargs: None)
    with pytest.raises(GateFailure) as exc:
        build_system(NEUTRAL, "#FFD400", foundations=("color",))
    assert any("choose a darker or more saturated seed" in f.message()
               for f in exc.value.report.findings)


def _core_set() -> TokenSet:
    """A system written by hand, as an import would be: the core color,
    space, radius, layout and type roles on the scheme axis only, and none
    of the roles M3.5 and the fixes after it added (brand and band surfaces
    and buttons, the primary edge, the landing gap, the display step and its
    fit factors, the phone scale)."""
    ts = TokenSet({"scheme": ("light", "dark")})
    for path, hex_ in {
        "palette.white": "#FFFFFF", "palette.gray.50": "#F7F7F8", "palette.gray.400": "#9A9AA5",
        "palette.gray.500": "#6B6B76", "palette.gray.900": "#18181B",
        "palette.gray.950": "#0E0E10", "palette.blue.300": "#93B4FD",
        "palette.blue.400": "#6D96FA", "palette.blue.500": "#4C7BF4",
        "palette.blue.700": "#1D4ED8", "palette.blue.800": "#1E40AF",
        "palette.blue.900": "#1E3A8A",
    }.items():
        ts.add(Token(path, "color", hex_))
    for path, (light, dark) in {
        "color.surface.page": ("palette.white", "palette.gray.950"),
        "color.surface.card": ("palette.gray.50", "palette.gray.900"),
        "color.text.default": ("palette.gray.950", "palette.gray.50"),
        "color.text.muted": ("palette.gray.500", "palette.gray.400"),
        "color.text.link": ("palette.blue.700", "palette.blue.300"),
        "color.action.primary": ("palette.blue.700", "palette.blue.300"),
        "color.action.primary-hover": ("palette.blue.800", "palette.blue.400"),
        "color.action.primary-pressed": ("palette.blue.900", "palette.blue.500"),
        "color.text.on-action": ("palette.white", "palette.gray.950"),
        "color.line.input": ("palette.gray.500", "palette.gray.400"),
        "color.focus.ring": ("palette.blue.700", "palette.blue.300"),
    }.items():
        ts.add(Token(path, "color", "{%s}" % light, modes={"scheme:dark": "{%s}" % dark},
                     layer="semantic"))
    for n in (1, 2, 3, 4, 5, 6, 8, 10, 12):
        ts.add(Token(f"space.{n}", "dimension", {"value": 4 * n, "unit": "px"}))
    for n, px in enumerate((4, 8, 12), 1):
        ts.add(Token(f"radius.{n}", "dimension", {"value": px, "unit": "px"}))
    for path, value in {"layout.viewport.640": 640, "layout.viewport.1024": 1024,
                        "layout.viewport.1280": 1280, "layout.width.44": 44,
                        "layout.width.1200": 1200}.items():
        ts.add(Token(path, "dimension", {"value": value, "unit": "px"}))
    ts.add(Token("layout.rem.36", "dimension", {"value": 36, "unit": "rem"}))
    for n in (4, 8, 12):
        ts.add(Token(f"layout.column-count.{n}", "number", n))
    tiers = ("phone", "tablet", "laptop", "desktop")
    roles = {"space.control.gap": "space.2", "space.control.padding-inline": "space.4",
             "space.control.padding-block": "space.2", "space.card.padding": "space.6",
             "radius.control": "radius.2", "radius.card": "radius.3",
             "layout.breakpoint.tablet": "layout.viewport.640",
             "layout.breakpoint.laptop": "layout.viewport.1024",
             "layout.breakpoint.desktop": "layout.viewport.1280",
             "layout.container.max": "layout.width.1200",
             "layout.measure.text": "layout.rem.36", "layout.target.min": "layout.width.44"}
    roles.update({f"layout.gutter.{t}": f"space.{n}" for t, n in zip(tiers, (4, 5, 6, 8))})
    roles.update({f"layout.margin-inline.{t}": f"space.{n}"
                  for t, n in zip(tiers, (4, 6, 8, 8))})
    roles.update({f"layout.region-gap.{t}": f"space.{n}"
                  for t, n in zip(tiers, (8, 10, 12, 12))})
    for path, target in roles.items():
        ts.add(Token(path, "dimension", "{%s}" % target, layer="semantic"))
    for t, n in zip(tiers, (4, 8, 12, 12)):
        ts.add(Token(f"layout.columns.{t}", "number", "{layout.column-count.%d}" % n,
                     layer="semantic"))
    ts.add(Token("type.face.sans", "fontFamily", ["Inter", "system-ui", "sans-serif"]))
    ts.add(Token("type.tracking.0", "dimension", {"value": 0, "unit": "px"}))
    for w in (400, 600):
        ts.add(Token(f"type.weight.{w}", "fontWeight", w))
    for name, rem in (("body", 1), ("h3", 1.25), ("h2", 1.5), ("h1", 2)):
        ts.add(Token(f"type.size.{name}", "dimension", {"value": rem, "unit": "rem"}))
    for name, lh in (("tight", 1.2), ("body", 1.5)):
        ts.add(Token(f"type.leading.{name}", "number", lh))
    for role, size, weight, lh in (("type.text.body", "body", 400, "body"),
                                   ("type.text.heading-3", "h3", 600, "tight"),
                                   ("type.text.heading-2", "h2", 600, "tight"),
                                   ("type.text.heading-1", "h1", 600, "tight")):
        ts.add(Token(role, "typography", {
            "fontFamily": "{type.face.sans}", "fontSize": "{type.size.%s}" % size,
            "fontWeight": "{type.weight.%d}" % weight, "lineHeight": "{type.leading.%s}" % lh,
            "letterSpacing": "{type.tracking.0}"}, layer="semantic"))
    return ts


def test_a_hand_written_set_with_the_core_roles_only_passes_and_strict_fails_it():
    ts = _core_set()
    newer = ("color.action.on-brand", "color.text.on-brand-action", "color.surface.band",
             "color.action.primary-edge", "layout.landing-gap.", "type.text.display",
             "type.fit.", "type.phone.")
    assert not any(t.path.startswith(newer) for t in ts.tokens())
    loose = check_system(ts)
    assert loose.problems == ()
    assert loose.foundations == ("color", "space", "radius", "layout", "type")
    assert loose.passed, loose.report.summary()
    # Each color pairing the set has is measured once per scheme; the rest
    # are skipped and listed, the newer roles' pairings among them.
    present = [p for p in build_module.color.PAIRINGS if ts.has(p.fg) and ts.has(p.bg)]
    assert present and loose.report.checked == 2 * len(present)
    skipped = {(p.fg, p.bg) for p in loose.report.skipped_pairings}
    assert len(skipped) == loose.report.skipped == len(build_module.color.PAIRINGS) - len(present)
    for pair in (("color.text.on-brand-action", "color.action.on-brand"),
                 ("color.text.default", "color.surface.band"),
                 ("color.action.primary-edge", "color.surface.page")):
        assert pair in skipped
        assert "%s on %s" % pair in loose.report.skipped_message()
    strict = check_system(ts, strict=True)
    assert not strict.passed
    assert {f.check for f in strict.report.failures} == {build_module.SKIPPED_PAIRING}
    assert len(strict.report.failures) == loose.report.skipped


def _project(ts: TokenSet, keep, drop=()) -> TokenSet:
    """The set on the axes in `keep` only, as a system without our other
    modes would be, less the tokens whose path starts with `drop`."""
    out = TokenSet({a: v for a, v in ts.axes.items() if a in keep})
    for t in ts.tokens():
        if drop and t.path.startswith(tuple(drop)):
            continue
        modes = {k: v for k, v in t.modes.items()
                 if all(part.split(":", 1)[0] in keep for part in k.split(","))}
        out.add(Token(t.path, t.type, t.value, modes=modes, layer=t.layer))
    return out


@pytest.mark.parametrize("keep", [("scheme",), ("scheme", "direction"),
                                  ("scheme", "contrast"), ()])
def test_display_fits_reads_the_axes_the_set_has(keep):
    ts = _project(build_system(NEUTRAL, "#3366FF").tokens, keep)
    assert ts.has("type.text.display")
    result = check_system(ts)
    assert result.passed, result.report.summary()


def test_display_fits_skips_a_tier_without_its_margin():
    ts = _project(build_system(NEUTRAL, "#3366FF").tokens, tuple(build_module.TokenSet().axes),
                  drop=("layout.margin-inline.",))
    result = check_system(ts)
    assert result.passed, result.report.summary()


def test_a_color_it_cannot_read_comes_back_as_a_problem():
    ts = _core_set()
    ts.add(Token("palette.ink", "color", "rgb(0 0 0)"))
    edited = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == "color.text.default":
            t = Token(t.path, t.type, "{palette.ink}", modes={}, layer="semantic")
        edited.add(t)
    result = check_system(edited)
    assert [(p.token, p.rule) for p in result.problems] == [("palette.ink", "bad-value")]
    assert not result.passed
    # Without validate's findings the gate still does not raise: each
    # context of each pairing on the role is a failure naming the value.
    report = build_module.gate_foundations(edited, build_module.FOUNDATIONS[:1])
    unread = [f for f in report.failures if f.check == "unresolved-pairing"]
    assert unread and all("rgb(0 0 0)" in f.message for f in unread)


def test_bad_value_roles_are_left_to_validate():
    ts = _core_set()
    edited = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == "color.text.muted":
            t = Token(t.path, t.type, "{palette.ink}", layer="semantic")
        edited.add(t)
    edited.add(Token("palette.ink", "color", "oklch(0.2 0 0)"))
    problems = tuple(build_module.validate(edited))
    report = build_module.gate_foundations(edited, build_module.FOUNDATIONS[:1],
                                           problems=problems)
    assert report.failures == []
    assert not any("color.text.muted" in (p.fg, p.bg) for p in report.skipped_pairings)


def test_strict_names_both_sides_when_both_are_missing():
    ts = _core_set()
    strict = check_system(ts, strict=True)
    both = next(f for f in strict.report.failures
                if f.message.startswith("color.text.muted on color.surface.band "))
    assert "color.text.muted" not in both.message.split(" was not checked ")[1]
    missing = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path != "color.text.muted":
            missing.add(t)
    msg = next(f.message for f in check_system(missing, strict=True).report.failures
               if f.message.startswith("color.text.muted on color.surface.band "))
    assert "because color.text.muted and color.surface.band are not defined; define them" in msg


def test_a_string_for_foundations_is_refused():
    with pytest.raises(TypeError, match=r"pass a tuple of names, for example \('color',\)"):
        check_system(TokenSet(), foundations="color")
