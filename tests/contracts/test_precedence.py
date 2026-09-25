"""Which binding applies when states and variants meet.

One rule for every contract: a disabled component takes no hover or
pressed binding; one that can take focus keeps its focus ring (WCAG 2.4.7
has no exemption for inactive controls); selected and error still apply,
and where disabled and another state bind the same part and property,
disabled wins. That rule is applied first; then a binding for a state beats
one without a state, and among those one with more variant conditions
beats one with fewer. The tests below run
every reachable combination of every seed contract's variants and states.
"""
import itertools
import re
from pathlib import Path

import pytest

from engine.contracts.library import SEED_DIR, load_folder
from engine.contracts.precedence import (
    DISABLED_RULE, DISABLED_SUPPRESSES, SPECIFICITY_RULE, TWO_STATE_OPENING, resolve)
from engine.contracts.schema import read_contract

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = {c.name: c for c in load_folder(SEED_DIR)}


def _combinations(contract):
    """Every variant choice with every set of states the contract lists,
    default always among them."""
    names = [v.name for v in contract.variants]
    others = [s for s in contract.states if s != "default"]
    for values in itertools.product(*(v.values for v in contract.variants)):
        variant = dict(zip(names, values))
        for n in range(len(others) + 1):
            for chosen in itertools.combinations(others, n):
                yield variant, ("default",) + chosen


def _matches(b, variant, states):
    return all(variant[k] == v for k, v in b.when) and (b.state is None or b.state in states)


CASES = [(name, variant, states) for name, c in CONTRACTS.items()
         for variant, states in _combinations(c)]


def test_every_reachable_combination_is_run():
    # button: 12 variant choices by 2**5 state sets; the row 2 by 2**5; the
    # text field 2 by 2**4.
    counts = {name: sum(1 for n, _, _ in CASES if n == name) for name in CONTRACTS}
    assert counts == {"badge": 6, "button": 768, "card": 2, "checkbox": 48, "chip": 32,
                      "date": 32, "dialog": 4, "faq-accordion": 4, "input-prefix": 32, "link": 8, "nav": 16,
                      "progress": 4, "radio": 32, "select": 128, "selectable-row": 64, "site-footer": 4,
                      "status-banner": 8, "table": 48, "text-field": 32, "textarea": 32}


@pytest.mark.parametrize("name,variant,states", CASES)
def test_the_resolved_binding_follows_the_rule(name, variant, states):
    contract = CONTRACTS[name]
    resolved = resolve(contract, variant, states)
    disabled = "disabled" in states
    live = {s for s in states if not (disabled and s in ("hover", "pressed"))}
    keys = []
    for b in contract.tokens:
        if (b.part, b.property) not in keys and _matches(b, variant, live):
            keys.append((b.part, b.property))
    assert list(resolved) == keys
    for key, winners in resolved.items():
        candidates = [b for b in contract.tokens
                      if (b.part, b.property) == key and _matches(b, variant, live)]
        assert winners and all(w in candidates for w in winners)
        # The disabled rule first: nothing from hover or pressed.
        if disabled:
            assert not any(w.state in ("hover", "pressed") for w in winners), (key, winners)
        # Where disabled binds the part and property, disabled wins.
        if any(b.state == "disabled" for b in candidates):
            assert all(w.state == "disabled" for w in winners), (key, winners)
        # Then a state over no state.
        elif any(b.state for b in candidates):
            assert all(w.state for w in winners), (key, winners)
        # Then more variant conditions over fewer.
        pool = [b for b in candidates if bool(b.state) == bool(winners[0].state)
                and (winners[0].state != "disabled" or b.state == "disabled")]
        assert all(len(w.when) == max(len(b.when) for b in pool) for w in winners)
        # Two states left standing are ones the contract ranks in its own line.
        if len({w.state for w in winners}) > 1:
            pair = {w.state for w in winners}
            assert "disabled" not in pair
            assert any(line.startswith(TWO_STATE_OPENING)
                       and all(re.search(rf"\b{s}\b", line) for s in pair)
                       for line in contract.do), (name, pair)
        else:
            assert len(winners) == 1, (key, winners)


def _role(contract, variant, states, part, prop):
    winners = resolve(contract, variant, states).get((part, prop), ())
    assert len(winners) <= 1
    return winners[0].role if winners else None


def test_the_rule_suppresses_hover_and_pressed_only():
    assert DISABLED_SUPPRESSES == ("hover", "pressed")


def test_a_disabled_button_under_the_pointer_takes_no_hover_or_press():
    button = CONTRACTS["button"]
    for emphasis in ("primary", "secondary", "ghost"):
        for intent in ("neutral", "danger"):
            v = {"emphasis": emphasis, "intent": intent}
            for extra in (("hover",), ("pressed",), ("hover", "pressed"), ("focus",)):
                states = ("default", "disabled") + extra
                assert _role(button, v, states, "label", "text") == "color.text.disabled"
                # A disabled button that can take focus keeps its ring.
                ring = "color.focus.ring" if "focus" in extra else None
                assert _role(button, v, states, "container", "focus-ring") == ring
                fill = _role(button, v, states, "container", "fill")
                assert fill == ("color.action.disabled" if emphasis == "primary" else None)
    ghost = {"emphasis": "ghost", "intent": "neutral"}
    hovered = ("default", "hover", "disabled")
    assert _role(button, ghost, hovered, "container", "border-width") is None
    assert _role(button, ghost, hovered, "container", "border-color") is None
    secondary = {"emphasis": "secondary", "intent": "neutral"}
    assert _role(button, secondary, hovered, "container", "border-color") == "color.text.disabled"
    assert _role(button, secondary, hovered, "container", "border-width") == "border.outline"
    # Enabled, the hover fill applies and press ranks over hover by the
    # contract's own line.
    primary = {"emphasis": "primary", "intent": "neutral"}
    assert _role(button, primary, ("default", "hover"), "container", "fill") == \
        "color.action.primary-hover"
    both = resolve(button, primary, ("default", "hover", "pressed"))[("container", "fill")]
    assert {b.state for b in both} == {"hover", "pressed"}


def test_a_disabled_selected_row_keeps_its_selection():
    row = CONTRACTS["selectable-row"]
    for selection in ("single", "multiple"):
        v = {"selection": selection}
        for extra in ((), ("hover",), ("pressed",), ("focus",)):
            states = ("default", "selected", "disabled") + extra
            assert _role(row, v, states, "leading", "icon") == "color.line.selected"
            assert _role(row, v, states, "container", "fill") == "color.surface.selected"
            assert _role(row, v, states, "container", "border-width") == "border.active"
            assert _role(row, v, states, "container", "border-color") == "color.line.selected"
            assert _role(row, v, states, "content", "text") == "color.text.disabled"
            ring = "color.focus.ring" if "focus" in extra else None
            assert _role(row, v, states, "container", "focus-ring") == ring
        hovered = ("default", "hover", "disabled")
        assert _role(row, v, hovered, "container", "fill") is None
        assert _role(row, v, hovered, "container", "border-width") is None
    multiple = {"selection": "multiple"}
    assert _role(row, multiple, ("default", "selected", "disabled"), "leading",
                 "border-color") == "color.text.disabled"


def test_a_disabled_field_in_error_keeps_the_error_where_disabled_binds_nothing():
    field = CONTRACTS["text-field"]
    v = {"lines": "single"}
    states = ("default", "hover", "focus", "disabled", "error")
    assert _role(field, v, states, "input", "border-width") == "border.outline"
    assert _role(field, v, states, "input", "edge-weight") == "border.emphasis"
    assert _role(field, v, states, "input", "border-color") == "color.line.subtle"
    assert _role(field, v, states, "message", "text") == "color.status.danger.text"
    assert _role(field, v, states, "icon", "icon") == "color.status.danger.strong"
    assert _role(field, v, states, "input", "fill") == "color.surface.sunken"
    assert _role(field, v, states, "input", "focus-ring") == "color.focus.ring"
    assert _role(field, v, states, "input", "focus-ring-width") == "border.focus-ring.width"


def test_every_contract_with_a_disabled_state_states_the_rule_word_for_word():
    for c in CONTRACTS.values():
        if "disabled" in c.states:
            assert DISABLED_RULE in c.do, c.name
            assert c.do.index(DISABLED_RULE) < c.do.index(SPECIFICITY_RULE), c.name
        else:
            assert DISABLED_RULE not in c.do, c.name


def test_the_architect_doc_states_the_rule_word_for_word():
    doc = (ROOT / "agents" / "design-system-architect.md").read_text(encoding="utf-8")
    assert DISABLED_RULE in doc
    assert SPECIFICITY_RULE in doc


# A synthetic contract in which each half of the specificity rule decides:
# the variant-condition count between two bindings of one state, the state
# over a stateless binding that has more conditions, and an omitted variant
# taking its default.
CHIP = """\
name: chip
status: experimental
category: action
description: Marks one filter as on or off.
parts:
  - {name: container, rtlBehavior: logical}
variants:
  - {name: tone, values: [neutral, danger], default: neutral}
  - {name: size, values: [small, large], default: small}
states: [default, hover, focus]
tokens:
  - {part: container, property: fill, role: color.surface.card, when: {tone: danger, size: large}}
  - {part: container, property: fill, role: color.surface.sunken, state: hover}
  - {part: container, property: fill, role: color.surface.selected, when: {tone: danger}, state: hover}
  - {part: container, property: fill, role: color.status.danger.soft, when: {tone: danger, size: large}, state: hover}
  - {part: container, property: min-size, role: layout.target.min}
  - {part: container, property: border-width, role: border.outline, when: {size: small}}
  - {part: container, property: focus-ring, role: color.focus.ring, state: focus}
  - {part: container, property: focus-ring-width, role: border.focus-ring.width, state: focus}
  - {part: container, property: focus-ring-offset, role: border.focus-ring.offset, state: focus}
contrast: []
surfaces: [color.surface.page]
a11y: {target: layout.target.min, label: localized, cue: the label names the filter}
copy:
  default:
    - Name the filter in one or two words
usage:
  do: [Apply the binding for a state over the one without a state]
  dont: [Do not use a chip as a button]
provenance:
  figma: {node: null, variantCount: null, lastVerified: null}
  drift: []
"""


def test_more_variant_conditions_beat_fewer_within_one_state():
    chip = read_contract(CHIP, "chip.yaml")
    hover = ("default", "hover")
    fill = lambda v, s: _role(chip, v, s, "container", "fill")  # noqa: E731
    # Three hover bindings match a large danger chip: none, one and two
    # conditions. Two conditions win.
    assert fill({"tone": "danger", "size": "large"}, hover) == "color.status.danger.soft"
    # A small danger chip matches the ones with none and one: one wins.
    assert fill({"tone": "danger", "size": "small"}, hover) == "color.surface.selected"
    assert fill({"tone": "neutral", "size": "large"}, hover) == "color.surface.sunken"
    # The state step comes first: at rest the stateless two-condition fill
    # applies, and on hover even the no-condition hover fill beats it.
    assert fill({"tone": "danger", "size": "large"}, ("default",)) == "color.surface.card"
    assert resolve(chip, {"tone": "danger", "size": "large"}, hover)[
        ("container", "fill")][0].state == "hover"
    # An omitted variant takes its default: size small.
    assert fill({"tone": "danger"}, hover) == "color.surface.selected"
    assert fill({"tone": "danger"}, ("default",)) is None
    assert _role(chip, {"tone": "danger"}, ("default",), "container", "border-width") == \
        "border.outline"
    assert _role(chip, {"tone": "danger", "size": "large"}, ("default",), "container",
                 "border-width") is None


def test_the_architect_doc_says_when_the_specificity_line_is_required():
    # The generator asks for it when two bindings of one part and property,
    # naming different roles, can both apply and differ in whether they
    # have a state or in their variant conditions.
    doc = (ROOT / "agents" / "design-system-architect.md").read_text(encoding="utf-8")
    assert ("A contract in which two bindings of one part and property name different roles "
            "and can both apply, one with a state and one without or the two with different "
            f"variant conditions, carries \"{SPECIFICITY_RULE}\"") in doc
    assert "meet by variant conditions" not in doc
