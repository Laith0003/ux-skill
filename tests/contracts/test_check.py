"""Checking contracts people write: the same schema and binding checks the
seed contracts pass, against a system read in any format the engine
imports, through a mapping when the system has its own names. The messages
are the seeds' messages; a role the mapping keeps out of the check is
named as such, never as one the system lacks."""
import dataclasses
import json
import shutil

import pytest

from engine.contracts import ContractCheck, bind_contracts
from engine.contracts import check_contracts as exported
from engine.contracts.check import check_contracts
from engine.contracts.library import SEED_DIR
from engine.contracts.schema import ContractError, load_contract
from engine.foundations.build import build_system
from engine.foundations.errors import InputError
from engine.foundations.export import dump_dtcg, to_css
from engine.foundations.values import TYPOGRAPHY_FIELDS
from engine.io import read_css, read_dtcg
from engine.io.adapter import FieldMap, Mapping, RoleMap, dump_mapping, propose
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)
SEEDS = ["badge", "button", "card", "checkbox", "chip", "date", "dialog", "faq-accordion",
         "input-prefix", "link", "nav", "progress", "radio", "select", "selectable-row",
         "site-footer", "status-banner", "table", "text-field", "textarea"]


def _tokens(tmp_path, *names):
    f = tmp_path / "tokens.json"
    ts = build_system(NEUTRAL, "#3366FF", foundations=names or None).tokens
    f.write_text(dump_dtcg(ts), encoding="utf-8")
    return f


def _css(tmp_path):
    """An engine-built system written as a stylesheet: every role under a
    custom property name, read back through a mapping."""
    f = tmp_path / "theme.css"
    f.write_text(to_css(build_system(NEUTRAL, "#3366FF").tokens), encoding="utf-8")
    return f


def _card(tmp_path):
    folder = tmp_path / "contracts"
    folder.mkdir()
    shutil.copy(SEED_DIR / "card.yaml", folder / "card.yaml")
    return folder


def _proposed(path):
    return propose(read_css(path).tokens)


def test_both_names_are_exported_from_the_package():
    assert exported is check_contracts
    assert ContractCheck.__module__ == "engine.contracts.check"


def test_the_seed_contracts_check_clean_against_a_built_system(tmp_path):
    result = check_contracts(SEED_DIR, _tokens(tmp_path))
    assert [c.name for c in result.contracts] == SEEDS
    assert result.problems == [] and result.lines == [] and result.passed


def test_a_schema_error_reads_exactly_as_it_does_for_a_seed(tmp_path):
    folder = tmp_path / "contracts"
    folder.mkdir()
    text = (SEED_DIR / "card.yaml").read_text(encoding="utf-8").replace(
        "status: experimental", "status: final")
    (folder / "card.yaml").write_text(text, encoding="utf-8")
    with pytest.raises(ContractError) as exc:
        load_contract(folder / "card.yaml")
    expected = [p.message for p in exc.value.problems]
    result = check_contracts(folder, _tokens(tmp_path))
    assert [p.message for p in result.problems] == expected and not result.passed
    assert result.contracts == ()


def test_every_file_is_read_so_one_bad_file_does_not_hide_another(tmp_path):
    folder = tmp_path / "contracts"
    folder.mkdir()
    for name in ("card", "link"):
        text = (SEED_DIR / f"{name}.yaml").read_text(encoding="utf-8").replace(
            "status: experimental", "status: final")
        (folder / f"{name}.yaml").write_text(text, encoding="utf-8")
    result = check_contracts(folder, _tokens(tmp_path))
    assert [p.contract for p in result.problems] == ["card", "link"]


def test_each_line_names_the_contract_file(tmp_path):
    folder = tmp_path / "contracts"
    folder.mkdir()
    text = (SEED_DIR / "card.yaml").read_text(encoding="utf-8").replace(
        "status: experimental", "status: final")
    (folder / "card.yaml").write_text(text, encoding="utf-8")
    (folder / "broken.yaml").write_text("name: [\n", encoding="utf-8")
    result = check_contracts(folder, _tokens(tmp_path))
    assert result.lines[0].startswith(f"{folder / 'broken.yaml'} line 1: ")
    assert result.lines[1] == (f"{folder / 'card.yaml'}: status is 'final'; use experimental, "
                               "ready, deprecated (agents author at experimental)")


def test_a_role_the_system_lacks_is_named_by_the_binding_check(tmp_path):
    folder = _card(tmp_path)
    result = check_contracts(folder, _tokens(tmp_path, "color", "space", "radius", "border"))
    assert result.problems
    assert all(p.contract == "card" for p in result.problems)
    assert any("binds elevation.card, which the token set does not define" in p.message
               for p in result.problems)
    assert f"{folder / 'card.yaml'}: container.shadow (level=standard) binds elevation.card, " \
           "which the token set does not define" in "\n".join(result.lines)


def test_a_mapping_lets_contracts_bind_a_system_in_its_own_names(tmp_path):
    folder = _card(tmp_path)
    tokens = tmp_path / "theirs.json"
    tokens.write_text(json.dumps({
        "paper": {"$type": "color", "$value": "#FFFFFF"},
        "card-bg": {"$type": "color", "$value": "{paper}"}}), encoding="utf-8")
    mapping = Mapping(roles={"color.surface.card": RoleMap("card-bg", "owner")})
    messages = [p.message for p in check_contracts(folder, tokens, mapping).problems]
    # The mapped role binds; the card's unmapped roles are named.
    assert not any("binds color.surface.card" in m for m in messages)
    assert any("binds radius.card, which the token set does not define" in m for m in messages)


def test_a_stylesheet_is_checked_through_its_mapping(tmp_path):
    css = _css(tmp_path)
    mapping = _proposed(css)
    result = check_contracts(SEED_DIR, css, mapping, fmt="css")
    assert result.problems == [] and result.passed
    # Read as it is, without the mapping, it has none of the roles.
    bare = check_contracts(_card(tmp_path), css, fmt="css")
    assert any("binds color.surface.card, which the token set does not define" in p.message
               for p in bare.problems)
    assert bare.notes == [
        "the system has none of the engine's roles under their own names and no mapping was "
        "given, so every role reads as missing; import it to write a mapping.json and check "
        "again with that mapping"]


def test_a_mapping_file_is_read_and_named_in_the_messages(tmp_path):
    css = _css(tmp_path)
    mapping = _proposed(css)
    roles = dict(mapping.roles)
    roles["color.surface.card"] = RoleMap(None, "owner")
    # A remembered prefix is part of the file; it changes nothing checked.
    roles["color.text.muted"] = dataclasses.replace(roles["color.text.muted"], prefix="color")
    path = tmp_path / "mapping.json"
    path.write_text(dump_mapping(Mapping(roles, dict(mapping.axes))), encoding="utf-8")
    result = check_contracts(_card(tmp_path), css, path, fmt="css")
    assert f"left out of the check in {path}" in result.problems[0].message


def test_a_role_the_owner_left_out_is_named_as_left_out(tmp_path):
    css = _css(tmp_path)
    mapping = _proposed(css)
    mapping.roles["color.surface.card"] = RoleMap(None, "owner")
    result = check_contracts(_card(tmp_path), css, mapping, fmt="css",
                             mapping_name="mapping.json")
    messages = [p.message for p in result.problems]
    assert messages == [
        "card: container.fill (level=standard) binds color.surface.card, which the owner left "
        "out of the check in mapping.json; map color.surface.card there to the token that "
        "plays it to check this binding, or bind a role the mapping maps",
        "card: contrast binds color.surface.card, which the owner left out of the check in "
        "mapping.json; map color.surface.card there to the token that plays it to check this "
        "binding, or bind a role the mapping maps"]
    assert {p.rule for p in result.problems} == {"left-out-role"}
    assert not any("does not define" in m for m in messages)


def test_a_role_deleted_from_the_mapping_is_named_as_left_out(tmp_path):
    tokens = _tokens(tmp_path)
    mapping = propose(read_dtcg(tokens).tokens)
    del mapping.roles["radius.card"]
    result = check_contracts(_card(tmp_path), tokens, mapping, mapping_name="mapping.json")
    assert [p.message for p in result.problems] == [
        "card: container.radius binds radius.card, which the system has under the role's own "
        "name but mapping.json leaves out, so it is not checked; map it there to check this "
        "binding, or bind a role the mapping maps"]


def test_a_type_role_mapped_field_by_field_binds(tmp_path):
    css = _css(tmp_path)
    mapping = _proposed(css)
    fields = {k: FieldMap(f"type-text-heading-3-{prop}") for k, (_, prop)
              in TYPOGRAPHY_FIELDS.items()}
    mapping.roles["type.text.heading-3"] = RoleMap.per_field(fields)
    assert check_contracts(_card(tmp_path), css, mapping, fmt="css").passed


def test_a_type_role_with_a_field_left_out_is_named_with_why(tmp_path):
    css = _css(tmp_path)
    mapping = _proposed(css)
    fields = {k: FieldMap(f"type-text-heading-3-{prop}") for k, (_, prop)
              in TYPOGRAPHY_FIELDS.items()}
    fields["lineHeight"] = FieldMap(None)
    mapping.roles["type.text.heading-3"] = RoleMap.per_field(fields)
    result = check_contracts(_card(tmp_path), css, mapping, fmt="css",
                             mapping_name="mapping.json")
    assert [(p.rule, p.message) for p in result.problems] == [(
        "unchecked-role",
        "card: title.font binds type.text.heading-3, which mapping.json maps but the check "
        "leaves out (type.text.heading-3 is not checked: the owner left out its field "
        "lineHeight in mapping.json, and the engine never picks a field for it); fix that "
        "entry in mapping.json to check this binding, or bind a role the mapping maps")]


def test_findings_carry_the_systems_own_names(tmp_path):
    css = _css(tmp_path)
    mapping = _proposed(css)
    # Muted text played by the card's own fill cannot be read on the card.
    mapping.roles["color.text.muted"] = RoleMap("color-surface-card", "owner")
    problems = check_contracts(_card(tmp_path), css, mapping, fmt="css").problems
    assert problems and {p.rule for p in problems} == {"contrast"}
    assert all(p.message.startswith("card: color.text.muted (your color-surface-card) on ")
               for p in problems)


def _card_again(tmp_path):
    folder = tmp_path / "again"
    folder.mkdir()
    shutil.copy(SEED_DIR / "card.yaml", folder / "card.yaml")
    return folder


def test_a_mapping_that_names_a_token_the_system_lacks_is_refused(tmp_path):
    css = _css(tmp_path)
    mapping = Mapping(roles={"color.surface.card": RoleMap("surface-card", "owner")})
    with pytest.raises(InputError, match="mapping.json sends color.surface.card to "
                                         "surface-card, which the imported system does not "
                                         "have"):
        check_contracts(_card(tmp_path), css, mapping, fmt="css", mapping_name="mapping.json")


def test_a_format_it_does_not_read_is_refused_with_the_label(tmp_path):
    with pytest.raises(InputError, match="--from format 'scss' is not one of"):
        check_contracts(_card(tmp_path), _css(tmp_path), fmt="scss")


def test_an_empty_folder_is_named(tmp_path):
    result = check_contracts(tmp_path, _tokens(tmp_path))
    assert [p.message for p in result.problems] == [
        f"{tmp_path} holds no .yaml contract; pass the folder that holds the contract files"]
    assert result.lines == [p.message for p in result.problems]


def test_contracts_already_read_bind_through_the_same_helper(tmp_path):
    css = _css(tmp_path)
    imported = read_css(css)
    mapping = propose(imported.tokens)
    mapping.roles["color.surface.card"] = RoleMap(None, "owner")
    contract = load_contract(SEED_DIR / "card.yaml")
    problems, notes = bind_contracts([contract], imported.tokens, mapping, "mapping.json")
    assert [p.rule for p in problems] == ["left-out-role", "left-out-role"]
    assert "color.surface.card is not checked: the owner left it out in mapping.json" in notes
    # An imported system is read as it is: nothing it holds changes.
    assert check_contracts(_card_again(tmp_path), imported, mapping).problems == problems


def test_the_check_is_deterministic(tmp_path):
    css = _css(tmp_path)
    mapping = _proposed(css)
    mapping.roles["color.text.muted"] = RoleMap("color-surface-card", "owner")
    folder = _card(tmp_path)
    first = check_contracts(folder, css, mapping, fmt="css")
    second = check_contracts(folder, css, mapping, fmt="css")
    assert first.lines == second.lines and first.notes == second.notes


def test_a_token_that_is_no_role_is_named_through_a_mapping(tmp_path):
    tokens = _tokens(tmp_path)
    folder = tmp_path / "contracts"
    folder.mkdir()
    text = (SEED_DIR / "card.yaml").read_text(encoding="utf-8").replace(
        "role: color.line.subtle", "role: color.brand.500")
    (folder / "card.yaml").write_text(text, encoding="utf-8")
    # Read as it is, the seed check names the primitive.
    assert [p.rule for p in check_contracts(folder, tokens).problems] == ["primitive-role"]
    mapping = propose(read_dtcg(tokens).tokens)
    # A mapping that names every role as itself checks the system itself.
    assert [p.rule for p in check_contracts(folder, tokens, mapping).problems] == [
        "primitive-role"]
    # Any other mapping checks the roles it maps, and a primitive is none.
    mapping.roles["color.surface.card"] = RoleMap("color.surface.raised", "owner")
    result = check_contracts(folder, tokens, mapping, mapping_name="mapping.json")
    assert [p.message for p in result.problems] == [
        "card: container.border-color binds color.brand.500, which is a token of the system but "
        "not one of the engine's roles, so mapping.json cannot send it and the check does not "
        "read it; bind the engine role it plays"]
