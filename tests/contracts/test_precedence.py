"""Which binding applies when states and variants meet.

One rule for every contract: a disabled component takes no hover, pressed
or focus binding; selected and error still apply, and where disabled and
another state bind the same part and property, disabled wins. That rule is
applied first; then a binding for a state beats one without a state, and
one with more variant conditions beats one with fewer. The tests below run
every reachable combination of every seed contract's variants and states.
"""
import itertools
import re
from pathlib import Path

import pytest

from engine.contracts.library import SEED_DIR, load_folder
from engine.contracts.precedence import (
    DISABLED_RULE, DISABLED_SUPPRESSES, SPECIFICITY_RULE, TWO_STATE_OPENING, resolve)

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
    # button: 6 variant choices by 2**5 state sets; the row 2 by 2**5; the
    # text field 2 by 2**4.
    counts = {name: sum(1 for n, _, _ in CASES if n == name) for name in CONTRACTS}
    assert counts == {"button": 192, "card": 2, "dialog": 4, "selectable-row": 64,
                      "status-banner": 8, "text-field": 32}


@pytest.mark.parametrize("name,variant,states", CASES)
def test_the_resolved_binding_follows_the_rule(name, variant, states):
    contract = CONTRACTS[name]
    resolved = resolve(contract, variant, states)
    disabled = "disabled" in states
    live = {s for s in states if not (disabled and s in DISABLED_SUPPRESSES)}
    keys = []
    for b in contract.tokens:
        if (b.part, b.property) not in keys and _matches(b, variant, live):
            keys.append((b.part, b.property))
    assert list(resolved) == keys
    for key, winners in resolved.items():
        candidates = [b for b in contract.tokens
                      if (b.part, b.property) == key and _matches(b, variant, live)]
        assert winners and all(w in candidates for w in winners)
        # The disabled rule first: nothing from hover, pressed or focus.
        if disabled:
            assert not any(w.state in DISABLED_SUPPRESSES for w in winners), (key, winners)
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


def test_a_disabled_button_under_the_pointer_takes_no_hover_or_press():
    button = CONTRACTS["button"]
    for emphasis in ("primary", "secondary", "ghost"):
        for intent in ("neutral", "danger"):
            v = {"emphasis": emphasis, "intent": intent}
            for extra in (("hover",), ("pressed",), ("hover", "pressed"), ("focus",)):
                states = ("default", "disabled") + extra
                assert _role(button, v, states, "label", "text") == "color.text.disabled"
                assert _role(button, v, states, "container", "focus-ring") is None
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
            assert _role(row, v, states, "container", "focus-ring") is None
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
    assert _role(field, v, states, "input", "border-width") == "border.emphasis"
    assert _role(field, v, states, "input", "border-color") == "color.line.subtle"
    assert _role(field, v, states, "message", "text") == "color.status.danger.text"
    assert _role(field, v, states, "icon", "icon") == "color.status.danger.strong"
    assert _role(field, v, states, "input", "fill") == "color.surface.sunken"
    assert _role(field, v, states, "input", "focus-ring") is None


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
