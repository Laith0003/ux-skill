"""The naming adapter: an imported system keeps its names; a mapping file
the owner can edit says which of its tokens plays each of our roles and
which of its modes is each of our axes. The engine checks a view in our
names and reports findings in both."""
import json

import pytest

from engine.foundations.build import FOUNDATIONS, build_system, check_system
from engine.foundations.errors import InputError
from engine.foundations.export import to_css
from engine.foundations.tokens import Token, TokenSet
from engine.io.adapter import (
    ROLE_TYPES, AxisMap, Mapping, RoleMap, dump_mapping, load_mapping, parse_mapping, propose,
    their_names, view)
from engine.io.css_in import import_css
from engine.io.dtcg_in import import_dtcg
from engine.io.report import Source
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)
SCHEME = AxisMap("scheme", {"light": "light", "dark": "dark"}, "owner")


def _source(text, name, fmt):
    return Source(name, fmt, "0" * 64, len(text))


def _css(text, name="theme.css"):
    return import_css(text, _source(text, name, "css")).tokens


def _dtcg(light, dark):
    lt, dt = json.dumps(light), json.dumps(dark)
    return import_dtcg(lt, _source(lt, "tokens.json", "dtcg"),
                       (dt, _source(dt, "tokens.dark.json", "dtcg"))).tokens


# An invented system: a .dark class the importer reads as the dark scheme.
FOREIGN = """:root {
  --ink: #1b1d22;
  --paper: #fdfdfb;
  --text-body: var(--ink);
  --page: var(--paper);
  --weight-strong: 600;
}
.dark {
  --text-body: var(--paper);
  --page: var(--ink);
}
"""

# The same system with its dark values under a class the importer keeps as
# an axis of its own, class-night, since the name alone does not say scheme.
NIGHT = FOREIGN.replace(".dark", ".night")


def test_the_roles_are_every_role_a_check_reads():
    assert ROLE_TYPES["color.text.default"] == "color"
    assert ROLE_TYPES["space.control.gap"] == "dimension"
    assert ROLE_TYPES["type.strong"] == "fontWeight"
    assert ROLE_TYPES["color.surface.brand"] == "color"
    assert ROLE_TYPES["type.text.body"] == "typography"
    assert ROLE_TYPES == {path: kind for f in FOUNDATIONS for path, kind in f.role_types.items()}


def test_our_own_css_maps_every_role_by_name_and_every_axis_to_itself():
    ts = build_system(NEUTRAL, "#3366FF").tokens
    flat = _css(to_css(ts), "tokens.css")
    mapping = propose(flat)
    assert set(mapping.roles) == {r for r in ROLE_TYPES if ts.has(r)}
    assert mapping.roles["color.text.default"] == RoleMap("color-text-default", "name")
    assert mapping.roles["type.text.body"] == RoleMap("type-text-body", "name")
    assert mapping.axes["scheme"] == AxisMap("scheme", {"light": "light", "dark": "dark"},
                                             "name")
    checked, notes = view(flat, mapping)
    # CSS writes a weight as a bare number; the view reads it back as one.
    assert notes == ["type.strong reads type-strong, a number, as a fontWeight (600), since the "
                     "role needs one"]
    result = check_system(checked, structure=False)
    assert result.passed, result.report.summary()


def test_a_foreign_system_maps_what_its_names_say_and_leaves_the_rest_to_the_owner():
    mapping = propose(_css(FOREIGN))
    assert mapping.roles == {}
    assert mapping.axes == {"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"},
                                              "name")}
    # A class the importer keeps as its own axis maps when its name says which.
    compact = _css(":root { --gap: 8px; }\n.compact { --gap: 4px; }\n")
    assert propose(compact).axes == {
        "density": AxisMap("class-compact", {"comfortable": "off", "compact": "on"}, "name")}
    # One whose name says nothing waits for the owner.
    assert propose(_css(NIGHT)).axes == {}


def test_the_view_puts_their_values_under_our_roles_and_axes():
    ts = _css(FOREIGN)
    mapping = Mapping(roles={"color.text.default": RoleMap("text-body", "owner"),
                             "color.surface.page": RoleMap("page", "owner"),
                             "type.strong": RoleMap("weight-strong", "owner")},
                      axes={"scheme": SCHEME})
    checked, notes = view(ts, mapping)
    assert dict(checked.axes) == {"scheme": ("light", "dark")}
    text = checked.get("color.text.default")
    assert (text.type, text.value, text.modes, text.layer) == (
        "color", "#1B1D22", {"scheme:dark": "#FDFDFB"}, "semantic")
    strong = checked.get("type.strong")
    assert (strong.type, strong.value) == ("fontWeight", 600)
    assert notes == ["type.strong reads weight-strong, a number, as a fontWeight (600), since the "
                     "role needs one"]
    report = check_system(checked, structure=False).report
    assert [f.fg for f in report.findings] == []


def test_the_owner_names_which_of_their_axes_is_ours():
    ts = _css(NIGHT)
    mapping = Mapping(roles={"color.text.default": RoleMap("text-body", "owner"),
                             "color.surface.page": RoleMap("page", "owner")},
                      axes={"scheme": AxisMap("class-night", {"light": "off", "dark": "on"},
                                              "owner")})
    checked, notes = view(ts, mapping)
    assert notes == []
    assert dict(checked.axes) == {"scheme": ("light", "dark")}
    assert checked.get("color.surface.page").modes == {"scheme:dark": "#1B1D22"}
    assert check_system(checked, structure=False).passed


def test_an_imported_dtcg_set_with_a_dark_file_is_checked_in_our_roles():
    light = {"ink": {"$type": "color", "$value": "#1b1d22"},
             "paper": {"$type": "color", "$value": "#fdfdfb"},
             "text": {"body": {"$type": "color", "$value": "{ink}"}},
             "surface": {"page": {"$type": "color", "$value": "{paper}"}}}
    dark = {"text": {"body": {"$type": "color", "$value": "{paper}"}},
            "surface": {"page": {"$type": "color", "$value": "{ink}"}}}
    ts = _dtcg(light, dark)
    mapping = propose(ts)
    assert mapping.axes == {"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"},
                                              "name")}
    mapping.roles.update({"color.text.default": RoleMap("text.body"),
                          "color.surface.page": RoleMap("surface.page")})
    checked, notes = view(ts, mapping)
    assert notes == []
    assert [t.path for t in checked.tokens()] == ["color.text.default", "color.surface.page"]
    assert checked.get("color.text.default").modes == {"scheme:dark": "#FDFDFB"}
    assert check_system(checked, structure=False).passed
    # A dark text that sinks into its page is found, and named in their words.
    dark["text"]["body"]["$value"] = "{ink}"
    failing = check_system(view(_dtcg(light, dark), mapping)[0], structure=False)
    found = failing.report.findings
    assert [(f.fg, f.bg, f.mode) for f in found] == [
        ("color.text.default", "color.surface.page", "scheme:dark")]
    assert "color.text.default (your text.body) on color.surface.page (your surface.page)" in \
        their_names(found[0].message(), mapping)


def test_a_mapping_to_a_token_that_is_not_there_is_named():
    ts = _css(FOREIGN)
    mapping = Mapping(roles={"color.text.default": RoleMap("text-main", "owner")}, axes={})
    with pytest.raises(InputError) as exc:
        view(ts, mapping)
    assert str(exc.value) == (
        "the mapping sends color.text.default to text-main, which the imported system does not "
        "have; point it at one of its tokens, or remove the line")


def test_an_axis_mapping_with_the_wrong_values_is_named():
    ts = _css(NIGHT)
    mapping = Mapping(roles={}, axes={"scheme": AxisMap("class-night", {"light": "off",
                                                                        "dark": "yes"}, "owner")})
    with pytest.raises(InputError) as exc:
        view(ts, mapping)
    assert str(exc.value) == (
        "the mapping reads scheme dark from class-night yes, but class-night has the values off "
        "and on; use those")


def test_an_axis_mapping_from_a_mode_axis_the_system_lacks_is_named():
    ts = _css(FOREIGN)
    mapping = Mapping(roles={}, axes={"scheme": AxisMap("class-night", {"light": "off",
                                                                        "dark": "on"}, "owner")})
    with pytest.raises(InputError) as exc:
        view(ts, mapping)
    assert str(exc.value) == (
        "the mapping reads scheme from the mode axis class-night, which the imported system does "
        "not have (it has scheme); fix the from value, or remove the axis")


@pytest.mark.parametrize("axes,message", [
    ({"scheme": AxisMap("class-night", {"light": "off", "dark": "on"}),
      "contrast": AxisMap("class-night", {"standard": "off", "high": "on"})},
     "the mapping reads scheme and contrast both from class-night; read each of the engine's "
     "axes from a mode axis of its own, or remove one"),
    ({"scheme": AxisMap("class-night", {"light": "on", "dark": "on"})},
     "the mapping reads scheme light and dark both from class-night on; read each from its own "
     "value"),
])
def test_an_axis_mapping_that_folds_values_together_is_named(axes, message):
    with pytest.raises(InputError) as exc:
        view(_css(NIGHT), Mapping(roles={}, axes=axes))
    assert str(exc.value) == message


def test_the_mapping_file_round_trips_and_is_checked_on_load(tmp_path):
    mapping = Mapping(roles={"color.text.default": RoleMap("text-body", "name")},
                      axes={"scheme": AxisMap("class-night", {"light": "off", "dark": "on"},
                                              "name")})
    text = dump_mapping(mapping)
    assert json.loads(text) == {
        "version": 1,
        "axes": {"scheme": {"from": "class-night", "values": {"light": "off", "dark": "on"},
                            "by": "name"}},
        "roles": {"color.text.default": {"token": "text-body", "by": "name"}}}
    assert parse_mapping(text, "mapping.json") == mapping
    f = tmp_path / "mapping.json"
    f.write_text(text, encoding="utf-8")
    assert load_mapping(f) == mapping


def test_a_mapping_file_that_cannot_be_read_names_the_flag_and_the_fix(tmp_path):
    missing = tmp_path / "mapping.json"
    with pytest.raises(InputError) as exc:
        load_mapping(missing)
    assert str(exc.value) == (
        f"--mapping {missing} cannot be read (No such file or directory); pass the mapping.json "
        "the import wrote")


@pytest.mark.parametrize("doc,message", [
    ({"roles": {}}, "mapping.json has no version; write \"version\": 1"),
    ({"version": 1, "role": {}}, "mapping.json has the key role, which a mapping does not use; "
                                 "keep only version, axes and roles"),
    ({"version": 2}, "mapping.json has version 2; this engine reads version 1, so write "
                     "\"version\": 1"),
    ({"version": 1, "roles": {"color.text.main": {"token": "x", "by": "owner"}}},
     "mapping.json maps color.text.main, which is not a role the engine checks; use one of its "
     "roles, for example color.text.default"),
    ({"version": 1, "roles": {"color.text.default": "x"}},
     "mapping.json role color.text.default is \"x\"; write {\"token\": \"<your token>\", \"by\": "
     "\"owner\"}"),
    ({"version": 1, "roles": {"color.text.default": {"token": "x", "by": "me"}}},
     "mapping.json role color.text.default is {\"token\": \"x\", \"by\": \"me\"}; write "
     "{\"token\": \"<your token>\", \"by\": \"owner\"}"),
    ({"version": 1, "roles": ["color.text.default"]},
     "mapping.json roles is [\"color.text.default\"]; write it as an object of role to "
     "{\"token\": \"<your token>\", \"by\": \"owner\"}"),
    ({"version": 1, "axes": {"theme": {"from": "x", "values": {}, "by": "owner"}}},
     "mapping.json maps the axis theme, which is not one of the engine's axes; use scheme, "
     "contrast, density, direction or motion"),
    ({"version": 1, "axes": {"scheme": "class-night"}},
     "mapping.json axis scheme is \"class-night\"; write {\"from\": \"<your mode axis>\", "
     "\"values\": {\"light\": \"...\", \"dark\": \"...\"}, \"by\": \"owner\"}"),
    ([1], "mapping.json is not a JSON object; write {\"version\": 1, \"axes\": {}, "
          "\"roles\": {}}"),
])
def test_a_bad_mapping_file_names_the_key_and_the_fix(doc, message):
    with pytest.raises(InputError) as exc:
        parse_mapping(json.dumps(doc), "mapping.json")
    assert str(exc.value) == message


def test_a_mapping_file_that_is_not_json_names_the_fix():
    with pytest.raises(InputError) as exc:
        parse_mapping("{", "mapping.json")
    assert str(exc.value).startswith("mapping.json is not valid JSON (")
    assert str(exc.value).endswith("); fix it, or remove it and import again to get a new "
                                   "proposal")


def test_findings_name_their_token_beside_our_role():
    mapping = Mapping(roles={"color.text.default": RoleMap("text-body", "owner"),
                             "color.surface.page": RoleMap("page", "owner")}, axes={})
    assert their_names("color.text.default on color.surface.page (scheme:dark) is 2.1:1",
                       mapping) == ("color.text.default (your text-body) on color.surface.page "
                                    "(your page) (scheme:dark) is 2.1:1")
    # A role at the end of a sentence is renamed; a longer path that starts
    # with a mapped one is not.
    assert their_names("Move color.text.default against color.surface.page.", mapping) == (
        "Move color.text.default (your text-body) against color.surface.page (your page).")
    assert their_names("color.text.default-hover and color.surface.page.raised",
                       mapping) == "color.text.default-hover and color.surface.page.raised"
    assert their_names("anything", Mapping()) == "anything"


def test_a_role_that_resolves_nowhere_in_a_context_is_left_out_with_a_note():
    ts = TokenSet({})
    ts.add(Token("text-body", "color", "{ink}", layer="semantic"))
    mapping = Mapping(roles={"color.text.default": RoleMap("text-body", "owner")}, axes={})
    checked, notes = view(ts, mapping)
    assert not checked.has("color.text.default")
    assert notes == ["color.text.default reads text-body, which cannot be resolved (text-body "
                     "aliases ink, which is not defined (resolving text-body). Define ink or "
                     "point text-body at an existing token.); it was left out of the check"]
