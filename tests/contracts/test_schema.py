"""The contract schema: every field is checked on its own, every problem
names the contract, the field and the fix, and ready needs the objective
promotion thresholds."""
import copy

import pytest

from engine.contracts.schema import (
    PROMOTION, STATES, Binding, ContractError, contract_problems, load_contract,
    promotion_problems, read_contract)
from engine.contracts.yamlite import loads

TOGGLE = """\
name: toggle
status: experimental
category: action
description: Turns one setting on or off at once.
parts:
  - {name: track, rtlBehavior: logical}
  - {name: thumb, rtlBehavior: mirror}
  - {name: label, rtlBehavior: logical}
variants:
  - {name: tone, values: [neutral, danger], default: neutral}
states: [default, focus, selected, disabled]
tokens:
  - {part: track, property: fill, role: color.surface.sunken}
  - {part: track, property: fill, role: color.action.primary, state: selected}
  - {part: track, property: fill, role: color.action.danger, when: {tone: danger}, state: selected}
  - {part: track, property: min-size, role: layout.target.min}
  - {part: label, property: text, role: color.text.default}
  - {part: track, property: focus-ring, role: color.focus.ring, state: focus}
  - {part: track, property: focus-ring-width, role: border.focus-ring.width, state: focus}
  - {part: track, property: focus-ring-offset, role: border.focus-ring.offset, state: focus}
contrast:
  - {fg: color.action.primary, bg: surfaces, minimum: 3, criterion: "1.4.11"}
  - {fg: color.text.default, bg: color.surface.page, minimum: 4.5, criterion: "1.4.3"}
surfaces: [color.surface.page, color.surface.card]
a11y: {target: layout.target.min, label: localized, cue: the thumb moves to the other end}
copy:
  default:
    - Name the setting, not the action
usage:
  do: [Apply the change at once]
  dont: [Do not ask for a save after a toggle]
provenance:
  figma: {node: null, variantCount: null, lastVerified: null}
  drift: []
"""


def data():
    return loads(TOGGLE)


def problems(d, source="toggle.yaml"):
    return [(p.rule, p.message) for p in contract_problems(d, source)[1]]


def test_a_valid_contract_reads_whole():
    c = read_contract(TOGGLE, "toggle.yaml")
    assert (c.name, c.status, c.category, c.states) == (
        "toggle", "experimental", "action", ("default", "focus", "selected", "disabled"))
    assert [(p.name, p.rtl_behavior) for p in c.parts] == [
        ("track", "logical"), ("thumb", "mirror"), ("label", "logical")]
    assert c.variant_product() == 2
    assert c.tokens[2] == Binding("track", "fill", "color.action.danger", (("tone", "danger"),),
                                  "selected")
    assert c.tokens[2].label() == "track.fill (tone=danger, selected)"
    assert c.contrast[0].bg == "surfaces" and c.contrast[0].minimum == 3.0
    assert c.copy == (("default", ("Name the setting, not the action",)),)
    assert c.roles()[:2] == ("color.surface.sunken", "color.action.primary")
    assert c.interactive


def test_states_come_back_in_the_fixed_order():
    d = data()
    d["states"] = ["disabled", "selected", "focus", "default"]
    c, found = contract_problems(d, "toggle.yaml")
    assert found == [] and c.states == ("default", "focus", "selected", "disabled")
    assert c.states == tuple(s for s in STATES if s in c.states)


@pytest.mark.parametrize("edit,rule,message", [
    (lambda d: d.pop("usage"), "missing-key",
     "toggle: missing usage; every contract has name, status, category, description, parts, "
     "variants, states, tokens, contrast, surfaces, a11y, copy, usage, provenance"),
    (lambda d: d.update(colour="x"), "unknown-key", "toggle: 'colour' is not a contract field"),
    (lambda d: d.update(name="Toggle"), "bad-name",
     "Toggle: name is 'Toggle'; use a lowercase name with '-', such as text-field"),
    (lambda d: d.update(name="switch"), "bad-name",
     "switch: name is 'switch' but the file is toggle.yaml; name the file switch.yaml or change "
     "the name"),
    (lambda d: d.update(status="final"), "bad-status",
     "toggle: status is 'final'; use experimental, ready, deprecated (agents author at "
     "experimental)"),
    (lambda d: d.update(category="widget"), "bad-category", "toggle: category is 'widget'"),
    (lambda d: d.update(status="deprecated"), "replacement",
     "toggle: a deprecated contract names its replacement; set replacement to the contract to "
     "use instead of toggle"),
    (lambda d: d.update(replacement="switch"), "replacement",
     "toggle: replacement is set but status is experimental; only a deprecated contract names "
     "a replacement, so remove it"),
    (lambda d: d["parts"][1].update(rtlBehavior="flip"), "bad-rtl",
     "toggle: part thumb has rtlBehavior 'flip'; use logical (placed with logical properties), "
     "mirror (the glyph flips under rtl) or fixed (never flips, such as a phone number)"),
    (lambda d: d["variants"][0].update(values=["neutral"]), "bad-variants",
     "toggle: variant tone values are ['neutral']; list every value the component supports, at "
     "least two, each a distinct lowercase name"),
    (lambda d: d["variants"][0].update(default="loud"), "bad-variants",
     "toggle: variant tone default is 'loud'; pick one of ['neutral', 'danger']"),
    (lambda d: d.update(states=["default", "focus", "active"]), "bad-states",
     "toggle: states ['active'] are not in the fixed list"),
    (lambda d: d.update(states=["focus"]), "bad-states",
     "toggle: states has no default; every component has a default state, so add it"),
    (lambda d: d["tokens"][0].update(role="#FFFFFF"), "not-a-role",
     "toggle: tokens[0].role is '#FFFFFF'; bind a semantic role by its path, for example "
     "color.action.primary, never a hex or an alias"),
    (lambda d: d["tokens"][0].update(part="knob"), "bad-binding",
     "toggle: tokens[0].part is 'knob'; use one of the declared parts ['label', 'thumb', "
     "'track']"),
    (lambda d: d["tokens"][0].update(property="colour"), "bad-binding",
     "toggle: tokens[0].property is 'colour'"),
    (lambda d: d["tokens"][2].update(when={"tone": "loud"}), "bad-binding",
     "toggle: tokens[2].when sets tone to 'loud'; use one of ['neutral', 'danger']"),
    (lambda d: d["tokens"][1].update(state="pressed"), "bad-binding",
     "toggle: tokens[1].state is 'pressed'; use a declared state, one of ['default', 'focus', "
     "'selected', 'disabled']"),
    (lambda d: d["tokens"].append(dict(d["tokens"][0])), "duplicate-binding",
     "toggle: track.fill is bound twice; keep one binding for it"),
    (lambda d: d["contrast"][1].update(minimum=4), "bad-contrast",
     "toggle: contrast[1] cites WCAG 1.4.3 with 4:1, but 1.4.3 sets 4.5:1; use that ratio, or "
     "cite system for a floor of your own"),
    (lambda d: d["contrast"][1].update(criterion="2.4.7"), "bad-contrast",
     "toggle: contrast[1].criterion is '2.4.7'"),
    (lambda d: d["contrast"][1].update(criterion="system"), "bad-contrast",
     "toggle: contrast[1] sets a system floor with no high"),
    (lambda d: d["contrast"][1].update(fg="color.text.muted"), "unbound-pairing",
     "toggle: contrast[1].fg color.text.muted is not bound in tokens; pair only roles the "
     "component uses, or bind it"),
    (lambda d: d["contrast"][1].update(bg="color.surface.raised"), "unbound-pairing",
     "toggle: contrast[1].bg color.surface.raised is neither bound in tokens nor listed in "
     "surfaces"),
    (lambda d: d["a11y"].update(target="none"), "bad-a11y",
     "toggle: an action component is a target, so a11y.target names the role that sets its "
     "minimum size, such as layout.target.min"),
    (lambda d: d["tokens"].pop(3), "bad-a11y",
     "toggle: a11y.target is layout.target.min, but no part binds min-size to it; bind "
     "min-size on the part a person presses"),
    (lambda d: d["tokens"].pop(5), "bad-a11y",
     "toggle: an action component shows focus, but no binding sets focus-ring in the focus "
     "state; bind it"),
    (lambda d: d["a11y"].update(label="english"), "bad-a11y",
     "toggle: a11y.label is 'english'; write localized"),
    (lambda d: d["a11y"].update(cue="none"), "bad-a11y",
     "toggle: the component binds color.action.danger, which carry meaning by color; "
     "a11y.cue must name the second cue"),
    (lambda d: d["copy"].update(default=['"Wi-Fi"']), "copy-is-a-string",
     "toggle: copy.default holds the literal \"Wi-Fi\"; copy holds rules, not strings"),
    (lambda d: d["copy"].update(error=["Say what failed"]), "bad-copy",
     "toggle: copy names 'error', which is not a declared state"),
    (lambda d: d["usage"].update(dont=[]), "bad-list",
     "toggle: usage.dont is []; write a list of one or more rules"),
    (lambda d: d["provenance"]["figma"].update(lastVerified="25/09/2026"), "bad-provenance",
     "toggle: provenance.figma.lastVerified is '25/09/2026'; write the date it was last read "
     "as YYYY-MM-DD, or null"),
    (lambda d: d["provenance"]["figma"].update(variantCount=3), "variant-count",
     "toggle: provenance.figma.variantCount is 3 but the variant enums allow 2; a mismatch is "
     "drift, so record it in provenance.drift, never change the count to fit"),
])
def test_each_field_is_checked_with_the_fix(edit, rule, message):
    d = copy.deepcopy(data())
    edit(d)
    found = problems(d)
    assert any(r == rule and m.startswith(message) for r, m in found), found


def test_a_loading_state_needs_copy_rules():
    d = data()
    d["states"] = ["default", "focus", "disabled", "loading"]
    assert ("bad-copy", "toggle: the loading state changes what the component says, so copy "
                        "needs rules for loading") in problems(d)


def test_a_non_interactive_contract_may_have_no_target_and_no_focus():
    d = data()
    d["category"] = "container"
    d["states"] = ["default"]
    d["tokens"] = [t for t in d["tokens"] if "state" not in t and "focus" not in t["property"]]
    d["a11y"] = {"target": "none", "label": "localized", "cue": "none"}
    d["contrast"] = [d["contrast"][1]]
    assert problems(d) == []


def test_ready_needs_every_promotion_threshold():
    d = data()
    d["status"] = "ready"
    found = problems(d)
    assert [r for r, _ in found] == ["promotion"] * 3
    assert len(PROMOTION) == 4
    d["provenance"] = {"figma": {"node": "12:345", "variantCount": 2,
                                 "lastVerified": "2026-09-25"}, "drift": []}
    assert problems(d) == []
    d["provenance"]["drift"] = ["the design file has a third tone"]
    assert [m for r, m in problems(d)] == [
        "toggle: provenance.drift lists 1 difference; ready needs none, so resolve each in the "
        "design file or the contract"]


def test_promotion_problems_can_be_asked_of_an_experimental_contract():
    c = read_contract(TOGGLE, "toggle.yaml")
    assert [p.rule for p in promotion_problems(c)] == ["promotion"] * 3


def test_read_contract_raises_with_every_problem_and_yaml_errors_by_line():
    with pytest.raises(ContractError) as err:
        read_contract(TOGGLE.replace("status: experimental", "status: final")
                      .replace("category: action", "category: widget"), "toggle.yaml")
    assert [p.rule for p in err.value.problems] == ["bad-status", "bad-category"]
    with pytest.raises(ContractError) as err:
        read_contract("name: toggle\n\tstatus: x", "toggle.yaml")
    assert str(err.value) == "toggle.yaml line 2: a tab indents this line; indent with spaces"


def test_load_contract_names_an_unreadable_file(tmp_path):
    bad = tmp_path / "toggle.yaml"
    bad.write_bytes(b"\xff\xfe")
    with pytest.raises(ContractError, match="toggle.yaml cannot be read"):
        load_contract(bad)
    good = tmp_path / "ok" / "toggle.yaml"
    good.parent.mkdir()
    good.write_text(TOGGLE, encoding="utf-8")
    assert load_contract(good).name == "toggle"
