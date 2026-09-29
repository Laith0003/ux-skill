"""A typography role mapped field by field: a system that keeps its type
as one token per field, in its own naming (text-size-lg, text-leading-lg,
font-weight-strong), maps each field of a role to its own token."""
import json

import pytest

from engine.foundations.build import check_system
from engine.foundations.errors import InputError
from engine.io.adapter import (
    FieldMap, Mapping, RoleMap, dump_mapping, merge, parse_mapping, propose, their_names, view)
from engine.io.css_in import import_css
from engine.io.report import Source

# An invented system that writes its type one field per token.
SPLIT = """:root {
  --font-family-sans: "Inter", sans-serif;
  --text-size-lg: 1.125rem;
  --text-size-sm: 14px;
  --text-leading-lg: 1.5;
  --text-leading-tight: 1.1;
  --font-weight-strong: 600;
  --text-tracking-lg: 0px;
  --ink: #1b1d22;
}
"""
FIELDS = {"fontFamily": FieldMap("font-family-sans", "owner"),
          "fontSize": FieldMap("text-size-lg", "owner"),
          "fontWeight": FieldMap("font-weight-strong", "owner"),
          "lineHeight": FieldMap("text-leading-lg", "owner"),
          "letterSpacing": FieldMap("text-tracking-lg", "owner")}


def _ts(text=SPLIT):
    return import_css(text, Source("type.css", "css", "0" * 64, len(text))).tokens


def _doc(fields):
    return json.dumps({"version": 1, "axes": {},
                       "roles": {"type.text.body": {"fields": fields}}})


def test_a_typography_role_maps_field_by_field_and_round_trips():
    doc = _doc({"fontFamily": {"token": "font-family-sans", "by": "owner"},
                "fontSize": {"token": "text-size-lg", "by": "owner"},
                "fontWeight": {"token": "font-weight-strong", "by": "owner"},
                "lineHeight": {"token": "text-leading-lg", "by": "name"},
                "letterSpacing": {"token": "text-tracking-lg", "by": "owner"}})
    mapping = parse_mapping(doc, "mapping.json")
    role = mapping.roles["type.text.body"]
    assert role.fields["fontSize"] == FieldMap("text-size-lg", "owner")
    assert role.fields["lineHeight"] == FieldMap("text-leading-lg", "name")
    # Any field the owner wrote makes the role the owner's.
    assert role.by == "owner"
    assert json.loads(dump_mapping(mapping)) == json.loads(doc)
    assert parse_mapping(dump_mapping(mapping), "mapping.json") == mapping


def test_the_view_resolves_each_field_from_its_own_token():
    mapping = Mapping(roles={"type.text.body": RoleMap.per_field(FIELDS)})
    checked, notes = view(_ts(), mapping)
    body = checked.get("type.text.body")
    assert (body.type, body.value) == ("typography", {
        "fontFamily": ["Inter", "sans-serif"], "fontSize": {"value": 1.125, "unit": "rem"},
        "fontWeight": 600, "lineHeight": 1.5, "letterSpacing": {"value": 0, "unit": "px"}})
    assert notes == []
    assert check_system(checked, structure=False).passed


def test_a_field_left_out_is_noted_and_never_guessed():
    fields = {k: v for k, v in FIELDS.items() if k != "lineHeight"}
    mapping = Mapping(roles={"type.text.body": RoleMap.per_field(fields)})
    checked, notes = view(_ts(), mapping, "mapping.json")
    # text-leading-lg is right there, but nothing maps it: the role is not
    # checked on a line height the engine picked.
    assert not checked.has("type.text.body")
    assert notes == [
        "type.text.body maps fontFamily, fontSize, fontWeight and letterSpacing field by field in "
        "mapping.json but not lineHeight, so it was not checked; add \"lineHeight\": {\"token\": "
        "\"<your token>\", \"by\": \"owner\"} to its fields"]


def test_a_field_of_the_wrong_type_is_noted_and_left_out():
    fields = dict(FIELDS, lineHeight=FieldMap("text-size-sm", "owner"))
    checked, notes = view(_ts(), Mapping(roles={"type.text.body": RoleMap.per_field(fields)}),
                          "mapping.json")
    assert not checked.has("type.text.body")
    assert notes == [
        "type.text.body field lineHeight reads text-size-sm, a dimension, but the field needs a "
        "number; point it at one of your number tokens in mapping.json"]


def test_a_field_token_the_system_lacks_is_named_with_the_fix():
    fields = dict(FIELDS, fontSize=FieldMap("text-size-xl", "owner"))
    with pytest.raises(InputError) as exc:
        view(_ts(), Mapping(roles={"type.text.body": RoleMap.per_field(fields)}), "mapping.json")
    assert str(exc.value) == (
        "mapping.json sends type.text.body field fontSize to text-size-xl, which the imported "
        "system does not have; point it at one of its tokens, or remove the field")


def test_findings_name_each_fields_token():
    mapping = Mapping(roles={"type.text.body": RoleMap.per_field(FIELDS)})
    assert their_names("type.text.body is too small.", mapping) == (
        "type.text.body (your fontFamily font-family-sans, fontSize text-size-lg, fontWeight "
        "font-weight-strong, letterSpacing text-tracking-lg and lineHeight text-leading-lg) is "
        "too small.")


def test_merge_keeps_the_owners_field_entries():
    fields = {"fontSize": FieldMap("text-size-lg", "owner"),
              "lineHeight": FieldMap("text-leading-tight", "name")}
    existing = Mapping(roles={"type.text.body": RoleMap.per_field(fields)})
    merged, notes = merge(propose(_ts()), existing)
    # The owner's field stays; a field the engine wrote and names no longer
    # say is dropped.
    assert merged.roles["type.text.body"].fields == {"fontSize": FieldMap("text-size-lg",
                                                                           "owner")}
    assert notes == []


@pytest.mark.parametrize("fields, message", [
    ({"size": {"token": "text-size-lg"}},
     "mapping.json role type.text.body maps the field size, which a typography role does not "
     "have; use fontFamily, fontSize, fontWeight, letterSpacing or lineHeight"),
    ({"fontSize": {"token": ""}},
     "mapping.json role type.text.body field fontSize is {\"token\": \"\"}; write {\"token\": "
     "\"<your token>\", \"by\": \"owner\"}"),
    ({"fontSize": "text-size-lg"},
     "mapping.json role type.text.body field fontSize is \"text-size-lg\"; write {\"token\": "
     "\"<your token>\", \"by\": \"owner\"}"),
    ({}, "mapping.json role type.text.body has no field in fields; map at least one field, for "
         "example \"fontSize\": {\"token\": \"<your token>\", \"by\": \"owner\"}"),
])
def test_a_bad_field_entry_names_the_field_and_the_fix(fields, message):
    with pytest.raises(InputError) as exc:
        parse_mapping(_doc(fields), "mapping.json")
    assert str(exc.value) == message


def test_fields_belong_to_typography_roles_only():
    doc = json.dumps({"version": 1, "roles": {"color.text.default": {
        "fields": {"fontSize": {"token": "text-size-lg"}}}}})
    with pytest.raises(InputError) as exc:
        parse_mapping(doc, "mapping.json")
    assert str(exc.value) == (
        "mapping.json role color.text.default maps fields, but only a typography role takes "
        "them; write {\"token\": \"<your token>\", \"by\": \"owner\"} for a color role")
    doc = json.dumps({"version": 1, "roles": {"type.text.body": {
        "token": "text-size-lg", "fields": {"fontSize": {"token": "text-size-lg"}}}}})
    with pytest.raises(InputError) as exc:
        parse_mapping(doc, "mapping.json")
    assert str(exc.value) == (
        "mapping.json role type.text.body has both token and fields; keep token for one "
        "composite token, or fields for one token per field")


def test_the_enhance_report_names_each_field_and_notes_a_field_left_out():
    from engine.io.enhance import enhance
    text = SPLIT
    imported = import_css(text, Source("type.css", "css", "0" * 64, len(text)))
    fields = {k: v for k, v in FIELDS.items() if k != "letterSpacing"}
    mapping = Mapping(roles={"type.text.body": RoleMap.per_field(FIELDS),
                             "type.text.label": RoleMap.per_field(fields)})
    result = enhance(imported, mapping)
    assert result.to_dict()["mapping"]["roles"]["type.text.body"] == {
        "fontFamily": "font-family-sans", "fontSize": "text-size-lg",
        "fontWeight": "font-weight-strong", "letterSpacing": "text-tracking-lg",
        "lineHeight": "text-leading-lg"}
    assert ("type.text.label maps fontFamily, fontSize, fontWeight and lineHeight field by field "
            "in mapping.json but not letterSpacing, so it was not checked; add \"letterSpacing\": "
            "{\"token\": \"<your token>\", \"by\": \"owner\"} to its fields") in result.decisions
    assert result.measured and result.check.report.passed


def test_a_field_the_owner_left_out_is_said_so():
    fields = dict(FIELDS, letterSpacing=FieldMap(None, "owner"))
    checked, notes = view(_ts(), Mapping(roles={"type.text.body": RoleMap.per_field(fields)}),
                          "mapping.json")
    assert not checked.has("type.text.body")
    assert notes == [
        "type.text.body is not checked: the owner left out its field letterSpacing in "
        "mapping.json, and the engine never picks a field for it"]


def test_a_role_entry_may_carry_a_note_of_the_owners():
    doc = json.dumps({"version": 1, "roles": {"color.text.default": {
        "token": "ink", "by": "owner", "note": "checked by hand"}}})
    assert parse_mapping(doc, "mapping.json").roles["color.text.default"] == RoleMap("ink")
