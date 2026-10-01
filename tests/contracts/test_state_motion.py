"""State changes answer on the system's motion roles: every part that
changes under hover, selected or pressed binds a transition (motion.state),
pressable components scale on motion.press.scale, menus leave on
motion.dismiss, and one indicator moves on motion.indicator."""
import pytest

from engine.contracts import validate_contracts
from engine.contracts.library import seed_contracts
from engine.contracts.schema import ContractError, read_contract
from engine.foundations import build_system
from engine.synthesizer.axes import AxisValues

from tests.contracts.test_schema import TOGGLE

MOVING = ("hover", "selected", "pressed")
SEEDS = {c.name: c for c in seed_contracts()}
TS = build_system(AxisValues(*[0.5] * 7), "#3366FF", arabic=False).tokens


def _bound(c, part, prop, role, state=None, when=None):
    return any(b.part == part and b.property == prop and b.role == role
               and (state is None or b.state == state)
               and (when is None or set(when.items()) <= set(b.when)) for b in c.tokens)


def test_a_state_with_no_transition_is_refused_naming_part_state_and_fix():
    text = TOGGLE.replace("""  - {part: track, property: transition-duration, role: motion.state.duration}
  - {part: track, property: transition-curve, role: motion.state.curve}
""", "")
    with pytest.raises(ContractError) as exc:
        read_contract(text, "toggle.yaml")
    msg = str(exc.value)
    assert "track" in msg and "selected" in msg and "motion.state.duration" in msg
    assert "transition" in msg


def test_a_transition_on_the_part_satisfies_the_check():
    assert read_contract(TOGGLE, "toggle.yaml").name == "toggle"


@pytest.mark.parametrize("name", sorted(SEEDS))
def test_every_part_that_changes_under_a_moving_state_binds_motion_state(name):
    c = SEEDS[name]
    for b in c.tokens:
        if b.state in MOVING and not b.property.startswith(("transition-", "enter-", "exit-")) \
                and b.property not in ("press-scale",):
            assert _bound(c, b.part, "transition-duration", "motion.state.duration") \
                or (b.state == "pressed"
                    and _bound(c, b.part, "transition-duration", "motion.press.duration")), \
                (name, b.label())


@pytest.mark.parametrize("name,when", [("button", None), ("chip", None),
                                       ("selectable-row", None),
                                       ("card", {"interaction": "interactive"})])
def test_pressable_components_scale_on_motion_press(name, when):
    c = SEEDS[name]
    assert "pressed" in c.states
    assert _bound(c, "container", "press-scale", "motion.press.scale", "pressed", when)


def test_the_press_scale_is_one_under_reduced_motion_and_within_range_otherwise():
    for axes in (AxisValues(*[0.5] * 7), AxisValues(0.5, 1, 0.5, 0.5, 0, 1, 0.5)):
        ts = build_system(axes, "#3366FF", arabic=False).tokens
        assert 0.95 <= ts.resolve("motion.press.scale", "motion:standard") <= 1
        assert ts.resolve("motion.press.scale", "motion:reduced") == 1


def test_a_press_scale_outside_the_range_is_named():
    from engine.foundations.tokens import Token
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", arabic=False).tokens
    ts.add(Token("motion.scale-900", "number", 0.9))
    del ts._tokens["motion.press.scale"]  # the test replaces the role in place
    ts.add(Token("motion.press.scale", "number", "{motion.scale-900}", layer="semantic"))
    problems = validate_contracts([SEEDS["button"]], ts)
    assert any("motion.press.scale" in p.message and "0.95" in p.message for p in problems)


@pytest.mark.parametrize("name,part,when", [("select", "menu", None),
                                            ("nav", "menu", {"layout": "collapsed"})])
def test_menus_leave_on_motion_dismiss(name, part, when):
    c = SEEDS[name]
    for prop, role in (("exit-duration", "motion.dismiss.duration"),
                       ("exit-curve", "motion.dismiss.curve"),
                       ("exit-distance", "motion.dismiss.distance")):
        assert _bound(c, part, prop, role, when=when), (name, prop)


INDICATED = ("nav", "tabs", "segmented-control", "menu")


@pytest.mark.parametrize("name", INDICATED)
def test_one_indicator_moves_on_motion_indicator(name):
    c = SEEDS[name]
    assert "indicator" in {p.name for p in c.parts}
    assert _bound(c, "indicator", "transition-duration", "motion.indicator.duration")
    assert _bound(c, "indicator", "transition-curve", "motion.indicator.curve")
    assert _bound(c, "indicator", "enter-duration", "motion.indicator.duration")
    text = " ".join(c.do).lower()
    assert "fades in" in text and "slides" in text and "reduced motion" in text
    cue = c.a11y.cue.lower()
    assert ("aria-current" in cue or "aria-selected" in cue) and "never color alone" in cue


def test_the_indicator_snaps_under_reduced_motion():
    assert TS.resolve("motion.indicator.duration", "motion:reduced") == {"value": 0, "unit": "ms"}


def test_disabled_menu_rows_stay_visible_with_a_reason():
    c = SEEDS["menu"]
    assert "disabled" in c.states
    text = " ".join(c.do).lower()
    assert "aria-disabled" in text and "reason" in text and "visible" in text


def test_a_visited_mark_is_a_glyph():
    text = " ".join(SEEDS["link"].do).lower()
    assert "visited" in text and "glyph" in text


@pytest.mark.parametrize("name", ["select", "table", "menu"])
def test_async_lists_announce_loading_politely_and_failure_as_an_alert(name):
    text = " ".join(SEEDS[name].do).lower()
    assert 'aria-live="polite"' in text and 'role="alert"' in text


def test_the_new_seeds_bind_to_a_built_system():
    assert validate_contracts([SEEDS[n] for n in INDICATED], TS) == []
