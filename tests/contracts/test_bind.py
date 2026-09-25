"""Contracts against a built token set: roles exist, are semantic and have
the right type; a fill below our edge floor against its surface declares an
edge; every declared pairing is measured in every color context."""
import copy
import dataclasses

import pytest

from engine.contracts.bind import EDGE_FLOOR, binding_problems, pairings_of, validate_contracts
from engine.contracts.library import seed_contracts
from engine.contracts.schema import contract_problems
from engine.contracts.yamlite import loads
from engine.foundations import build_system
from engine.foundations.color_math import contrast
from engine.foundations.gate import Pairing
from engine.synthesizer.axes import AxisValues
from tests.contracts.test_schema import TOGGLE

TS = build_system(AxisValues(*[0.5] * 7), "#3366FF").tokens
EDGE = [{"part": "track", "property": "border-width", "role": "border.outline"},
        {"part": "track", "property": "border-color", "role": "color.line.input"}]


def contract(edit=None, with_edge=True):
    d = loads(TOGGLE)
    if with_edge:
        d["tokens"] += copy.deepcopy(EDGE)
    if edit:
        edit(d)
    c, problems = contract_problems(d, f"{d['name']}.yaml")
    assert problems == [], problems
    return c


def messages(c):
    return [(p.rule, p.message) for p in binding_problems(c, TS)]


def test_a_contract_with_an_edge_binds_cleanly():
    assert messages(contract()) == []


def test_a_fill_that_equals_its_surface_declares_an_edge():
    assert messages(contract(with_edge=False)) == [
        ("container-edge",
         "toggle: track.fill is color.surface.sunken, which measures 1.00:1 against "
         "color.surface.page in scheme:dark,contrast:high, below our container edge floor of "
         "1.2:1 (WCAG sets no minimum for a container's edge), so the track has no visible edge "
         "there; bind border-width to border.outline and a border-color on track for the same "
         "variant and state")]


def test_the_edge_floor_is_ours_and_measured():
    assert EDGE_FLOOR == 1.2


def _without_edges(c):
    return dataclasses.replace(c, tokens=tuple(b for b in c.tokens
                                               if not b.property.startswith("border-")))


def test_a_fill_near_but_not_equal_to_its_surface_declares_an_edge():
    # In high contrast the status soft fills sit a few hex steps off the
    # surfaces, never on them: an equality rule misses every one, the floor
    # catches each.
    banner = next(c for c in seed_contracts() if c.name == "status-banner")
    high = ("scheme:light,contrast:high", "scheme:dark,contrast:high")
    for status in ("info", "success", "warning", "danger"):
        fill = f"color.status.{status}.soft"
        near = [(s, m) for s in banner.surfaces for m in high
                if contrast(TS.resolve(fill, m), TS.resolve(s, m)) < EDGE_FLOOR]
        assert near and all(TS.resolve(fill, m) != TS.resolve(s, m) for s, m in near), status
    assert binding_problems(banner, TS) == []
    found = binding_problems(_without_edges(banner), TS)
    assert [p.rule for p in found] == ["container-edge"] * 4
    for p, status in zip(found, ("info", "success", "warning", "danger")):
        fill = f"color.status.{status}.soft"
        assert p.message.startswith(f"status-banner: container.fill (status={status}) is {fill}, "
                                    "which measures 1.")
        ratio = float(p.message.split("measures ")[1].split(":1")[0])
        assert 1.0 <= ratio < EDGE_FLOOR
        assert "below our container edge floor of 1.2:1 (WCAG sets no minimum" in p.message


def test_a_fill_that_clears_the_edge_floor_needs_no_edge():
    c = contract(lambda d: d["tokens"][0].update(role="color.action.primary"), with_edge=False)
    assert messages(c) == []


def test_an_edge_for_another_state_does_not_count():
    def edit(d):
        for b in d["tokens"]:
            if b["property"].startswith("border-"):
                b["state"] = "selected"
    assert [r for r, _ in messages(contract(edit))] == ["container-edge"]


@pytest.mark.parametrize("role,rule,message", [
    ("color.surface.floating", "unknown-role",
     "toggle: track.fill binds color.surface.floating, which the token set does not define; "
     "bind an existing semantic role, or add the role to the system first"),
    ("color.brand.500", "primitive-role",
     "toggle: track.fill binds color.brand.500, a primitive; components bind semantic roles "
     "only, so bind the role that aliases it"),
    ("space.card.padding", "role-type",
     "toggle: track.fill binds space.card.padding, a dimension, but it needs a color; bind a "
     "color role"),
])
def test_every_bound_role_exists_is_semantic_and_has_its_type(role, rule, message):
    c = contract(lambda d: d["tokens"][0].update(role=role))
    assert (rule, message) in messages(c)


def test_a_declared_pairing_is_measured_in_every_color_context():
    def edit(d):
        d["tokens"].append({"part": "label", "property": "text", "role": "color.text.disabled",
                            "state": "disabled"})
        d["contrast"].append({"fg": "color.text.disabled", "bg": "color.surface.page",
                              "minimum": 3, "criterion": "1.4.11"})
    found = messages(contract(edit))
    assert [m.split(" (")[1].split(")")[0] for _, m in found] == [
        "scheme:light,contrast:high", "scheme:dark,contrast:standard",
        "scheme:dark,contrast:high"]
    assert found[1] == (
        "contrast", "toggle: color.text.disabled on color.surface.page (scheme:dark,"
        "contrast:standard) is 2.88:1; WCAG 1.4.11 needs 3:1. Bind a role with more contrast "
        "against color.surface.page, or build the system again with a different brand color")
    assert "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3:1)" in found[0][1]


def test_high_pins_the_high_contrast_minimum_and_system_floors_say_whose_they_are():
    def edit(d):
        d["tokens"].append({"part": "label", "property": "text", "role": "color.text.disabled",
                            "state": "disabled"})
        d["contrast"].append({"fg": "color.text.disabled", "bg": "color.surface.page",
                              "minimum": 3, "criterion": "1.4.11", "high": 3})
        d["contrast"].append({"fg": "color.text.disabled", "bg": "color.surface.card",
                              "minimum": 5, "criterion": "system", "high": 5})
    found = [m for _, m in messages(contract(edit))]
    assert [m for m in found if "surface.page" in m] == [
        "toggle: color.text.disabled on color.surface.page (scheme:dark,contrast:standard) is "
        "2.88:1; WCAG 1.4.11 needs 3:1. Bind a role with more contrast against "
        "color.surface.page, or build the system again with a different brand color"]
    card = [m for m in found if "surface.card" in m]
    assert len(card) == 4 and all("the declared floor for the toggle contract is 5:1" in m
                                  for m in card)


def test_pairings_expand_the_surfaces_shorthand():
    c = contract()
    assert pairings_of([c])[:2] == [
        ("toggle", Pairing("color.action.primary", "color.surface.page", 3.0, "1.4.11")),
        ("toggle", Pairing("color.action.primary", "color.surface.card", 3.0, "1.4.11"))]


def test_validate_contracts_checks_names_and_replacements():
    a = contract()
    b = contract(lambda d: d.update(status="deprecated", replacement="switch"))
    assert [p.message for p in validate_contracts([a, b])] == [
        "toggle: two contracts are named toggle; rename one",
        "toggle: replacement is switch, which is not in this set of contracts; name a contract "
        "that exists"]
    switch = contract(lambda d: d.update(name="switch", status="deprecated",
                                         replacement="toggle"))
    old = contract(lambda d: d.update(status="deprecated", replacement="switch"))
    assert [p.message for p in validate_contracts([old, switch])] == [
        "toggle: replacement switch is deprecated too; name a contract people can move to",
        "switch: replacement toggle is deprecated too; name a contract people can move to"]


def test_validate_contracts_binds_each_contract_when_given_tokens():
    assert validate_contracts([contract()], TS) == []
    assert [p.rule for p in validate_contracts([contract(with_edge=False)], TS)] == [
        "container-edge"]
