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
    ROLE_TYPES, AxisMap, Mapping, RoleMap, dump_mapping, load_mapping, merge, parse_mapping,
    propose, their_names, view)
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


def test_a_view_error_names_the_mapping_file_it_came_from():
    mapping = Mapping(roles={"color.text.default": RoleMap("text-main", "owner")}, axes={})
    with pytest.raises(InputError) as exc:
        view(_css(FOREIGN), mapping, "mapping.json")
    assert str(exc.value).startswith("mapping.json sends color.text.default to text-main, ")


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
    ({"version": 1, "roles": {"space.control.gpa": {"token": "x", "by": "owner"}}},
     "mapping.json maps space.control.gpa, which is not a role the engine checks; use one of "
     "its roles, such as the nearest, space.control.gap"),
    ({"version": 1, "roles": {"brand.ink": {"token": "x", "by": "owner"}}},
     "mapping.json maps brand.ink, which is not a role the engine checks; use one of its "
     "roles, for example color.text.default"),
    ({"version": 1, "roles": {"color.text.default": "x"}},
     "mapping.json role color.text.default is \"x\"; write {\"token\": \"<your token>\", \"by\": "
     "\"owner\"}, or {\"token\": null, \"by\": \"owner\"} to keep it out of the check"),
    ({"version": 1, "roles": {"color.text.default": {"token": "x", "by": "me"}}},
     "mapping.json role color.text.default is {\"token\": \"x\", \"by\": \"me\"}; write "
     "{\"token\": \"<your token>\", \"by\": \"owner\"}, or {\"token\": null, \"by\": \"owner\"} "
     "to keep it out of the check"),
    ({"version": 1, "roles": {"color.text.default": {"token": None, "by": "name"}}},
     "mapping.json role color.text.default is {\"token\": null, \"by\": \"name\"}; write "
     "{\"token\": \"<your token>\", \"by\": \"owner\"}, or {\"token\": null, \"by\": \"owner\"} "
     "to keep it out of the check"),
    ({"version": 1, "roles": {"color.text.default": {"by": "owner"}}},
     "mapping.json role color.text.default is {\"by\": \"owner\"}; write "
     "{\"token\": \"<your token>\", \"by\": \"owner\"}, or {\"token\": null, \"by\": \"owner\"} "
     "to keep it out of the check"),
    ({"version": 1, "roles": ["color.text.default"]},
     "mapping.json roles is [\"color.text.default\"]; write it as an object of role to "
     "{\"token\": \"<your token>\", \"by\": \"owner\"}, or {\"token\": null, \"by\": \"owner\"} "
     "to keep it out of the check"),
    ({"version": 1, "axes": {"theme": {"from": "x", "values": {}, "by": "owner"}}},
     "mapping.json maps the axis theme, which is not one of the engine's axes; use scheme, "
     "contrast, density, direction or motion"),
    ({"version": 1, "axes": {"scheme": "class-night"}},
     "mapping.json axis scheme is \"class-night\"; write {\"from\": \"<your mode axis>\", "
     "\"values\": {\"light\": \"...\", \"dark\": \"...\"}, \"by\": \"owner\"}, or "
     "{\"from\": null, \"by\": \"owner\"} to keep it out of the check"),
    ({"version": 1, "axes": {"scheme": {"from": None, "by": "name"}}},
     "mapping.json axis scheme is {\"from\": null, \"by\": \"name\"}; write {\"from\": "
     "\"<your mode axis>\", \"values\": {\"light\": \"...\", \"dark\": \"...\"}, \"by\": "
     "\"owner\"}, or {\"from\": null, \"by\": \"owner\"} to keep it out of the check"),
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


# The system itself is checked only when the mapping names every role and
# axis the set has, each as itself. Anything the owner took out of the
# mapping file is out of the check.

def _own(recolor=None):
    """A generated color set in our own names, with color.text.default
    optionally pointed at another step."""
    built = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    if recolor is None:
        return built
    ts = TokenSet(built.axes)
    for t in built.tokens():
        ts.add(Token(t.path, t.type, recolor, layer=t.layer)
               if t.path == "color.text.default" else t)
    return ts


def test_a_mapping_that_names_every_role_and_axis_as_itself_checks_the_system_itself():
    ts = _own()
    checked, notes = view(ts, propose(ts))
    assert checked is ts and notes == []


def test_a_role_the_owner_took_out_of_the_mapping_is_not_checked():
    ts = _own("{color.neutral.100}")
    mapping = propose(ts)
    assert any(f.fg == "color.text.default"
               for f in check_system(view(ts, mapping)[0], structure=False).report.findings)
    del mapping.roles["color.text.default"]
    checked, notes = view(ts, mapping)
    assert checked is not ts and not checked.has("color.text.default")
    assert notes == ["the mapping leaves out color.text.default, which the imported system has "
                     "under the role's own name, so it was not checked; map it to check it"]
    report = check_system(checked, structure=False).report
    assert not [f for f in report.findings if "color.text.default" in (f.fg, f.bg)]
    assert not [f for f in report.failures if "color.text.default" in f.message]


def test_an_empty_mapping_checks_nothing():
    checked, notes = view(_css(FOREIGN), Mapping())
    assert (checked.tokens(), dict(checked.axes)) == ([], {})
    # Nothing is checked, and the axis the file lost is named.
    assert [n.split(",")[0] for n in notes] == [
        "the mapping leaves out the axis scheme"]
    checked, notes = view(_own(), Mapping())
    assert checked.tokens() == []
    assert [n.split(",")[0] for n in notes[:5]] == [
        f"the mapping leaves out the axis {a}" for a in
        ("scheme", "contrast", "density", "direction", "motion")]
    assert notes[5:] == [
        "the mapping leaves out color.surface.page, color.surface.card, color.surface.sunken and "
        "68 more, which the imported system has under each role's own name, so they were not "
        "checked; map each one to check it"]


def test_an_axis_the_owner_took_out_of_the_mapping_is_held_at_its_base():
    ts = _own()
    mapping = propose(ts)
    del mapping.axes["scheme"]
    checked, notes = view(ts, mapping)
    assert notes == [
        "the mapping leaves out the axis scheme, which the imported system has as scheme, so it "
        "was not checked and every role is read at the system's base; map it to check it, or "
        'write {"from": null, "by": "owner"} for it to keep it out on purpose'] \
        and "scheme" not in checked.axes
    text = checked.get("color.text.default")
    assert text.value == ts.resolve("color.text.default")
    assert all("scheme" not in key for key in text.modes)


def test_own_names_still_read_a_number_weight_and_leave_out_what_cannot_resolve():
    ts = TokenSet({})
    ts.add(Token("type.strong", "number", 600, layer="semantic"))
    ts.add(Token("color.text.default", "color", "{color.ink}", layer="semantic"))
    mapping = propose(ts)
    assert mapping.roles == {"type.strong": RoleMap("type.strong", "name"),
                             "color.text.default": RoleMap("color.text.default", "name")}
    checked, notes = view(ts, mapping)
    assert checked is not ts
    assert [(t.path, t.type, t.value) for t in checked.tokens()] == [
        ("type.strong", "fontWeight", 600)]
    assert notes == [
        "color.text.default reads color.text.default, which cannot be resolved "
        "(color.text.default aliases color.ink, which is not defined (resolving "
        "color.text.default). Define color.ink or point color.text.default at an existing "
        "token.); it was left out of the check",
        "type.strong reads type.strong, a number, as a fontWeight (600), since the role needs "
        "one"]


def test_merge_keeps_what_the_owner_wrote_and_fills_only_the_rest():
    proposed = Mapping(
        roles={"color.text.default": RoleMap("text-default", "name"),
               "color.surface.page": RoleMap("surface-page", "name"),
               "space.control.gap": RoleMap("gap", "name")},
        axes={"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"}, "name"),
              "density": AxisMap("class-compact", {"comfortable": "off", "compact": "on"},
                                 "name")})
    existing = Mapping(
        roles={"color.text.default": RoleMap("text-body", "owner"),
               "color.surface.page": RoleMap("old-page", "name"),
               "color.line.danger": RoleMap("error-edge", "owner")},
        axes={"scheme": AxisMap("class-night", {"light": "off", "dark": "on"}, "owner")})
    merged, notes = merge(proposed, existing)
    assert notes == [
        "mapping.json did not map space.control.gap, so it was proposed as gap by name; to keep "
        "it out of the check, write {\"token\": null, \"by\": \"owner\"} for it",
        "mapping.json did not map the axis density, so it was proposed from class-compact by "
        "name; to keep it out of the check, write {\"from\": null, \"by\": \"owner\"} for it"]
    assert merged.roles == {"color.text.default": RoleMap("text-body", "owner"),
                            "color.surface.page": RoleMap("surface-page", "name"),
                            "color.line.danger": RoleMap("error-edge", "owner"),
                            "space.control.gap": RoleMap("gap", "name")}
    assert list(merged.roles) == [r for r in ROLE_TYPES if r in merged.roles]
    assert merged.axes == {"scheme": existing.axes["scheme"],
                           "density": proposed.axes["density"]}
    assert merge(proposed, Mapping())[0] == proposed
    assert merge(proposed, Mapping())[1][0] == (
        "mapping.json did not map color.surface.page, color.text.default and "
        "space.control.gap, so they were proposed by name; to keep one out of the check, write "
        "{\"token\": null, \"by\": \"owner\"} for it")
    assert merge(Mapping(), existing) == (Mapping(
        roles={r: m for r, m in existing.roles.items() if m.by == "owner"},
        axes=existing.axes), [])


def test_an_axis_named_as_one_of_ours_is_that_axis_whatever_its_values():
    ts = TokenSet({"density": ("default", "high")})
    ts.add(Token("gap", "dimension", {"value": 8, "unit": "px"},
                 modes={"density:high": {"value": 4, "unit": "px"}}, layer="semantic"))
    assert propose(ts).axes == {
        "density": AxisMap("density", {"comfortable": "default", "compact": "high"}, "name")}


def test_findings_name_their_mode_beside_ours():
    mapping = Mapping(roles={"color.text.default": RoleMap("text-body", "owner")},
                      axes={"scheme": AxisMap("class-night", {"light": "off", "dark": "on"}),
                            "contrast": AxisMap("contrast",
                                                {"standard": "standard", "high": "high"})})
    assert their_names("color.text.default (scheme:dark,contrast:high) is 2.1:1", mapping) == (
        "color.text.default (your text-body) (scheme:dark,contrast:high; your class-night:on,"
        "contrast:high) is 2.1:1")
    # A context every axis of which the system names as we do is left as it is.
    assert their_names("x (contrast:high) and y (scheme:light)", mapping) == (
        "x (contrast:high) and y (scheme:light; your class-night:off)")


# The owner keeps a role or an axis out of the check with an explicit
# "not mapped" entry, which a new import never fills again.

NOT_MAPPED_ROLE = RoleMap(None, "owner")
NOT_MAPPED_AXIS = AxisMap(None, {}, "owner")


def test_a_not_mapped_entry_reads_writes_and_is_never_proposed():
    doc = {"version": 1,
           "axes": {"scheme": {"from": None, "by": "owner"}},
           "roles": {"color.text.default": {"token": None, "by": "owner"},
                     "color.surface.page": {"token": None}}}
    mapping = parse_mapping(json.dumps(doc), "mapping.json")
    assert mapping == Mapping(roles={"color.text.default": NOT_MAPPED_ROLE,
                                     "color.surface.page": NOT_MAPPED_ROLE},
                              axes={"scheme": NOT_MAPPED_AXIS})
    assert json.loads(dump_mapping(mapping)) == {
        "version": 1, "axes": {"scheme": {"from": None, "by": "owner"}},
        "roles": {"color.text.default": {"token": None, "by": "owner"},
                  "color.surface.page": {"token": None, "by": "owner"}}}
    proposed = propose(_css(to_css(build_system(NEUTRAL, "#3366FF").tokens), "tokens.css"))
    assert all(m.token and m.by == "name" for m in proposed.roles.values())
    assert all(m.source and m.by == "name" for m in proposed.axes.values())


def test_a_not_mapped_role_or_axis_is_out_of_the_view_with_a_note():
    ts = _css(FOREIGN)
    mapping = Mapping(roles={"color.text.default": NOT_MAPPED_ROLE,
                             "color.surface.page": RoleMap("page", "owner")},
                      axes={"scheme": NOT_MAPPED_AXIS})
    checked, notes = view(ts, mapping, "mapping.json")
    assert [t.path for t in checked.tokens()] == ["color.surface.page"]
    assert dict(checked.axes) == {}
    assert checked.get("color.surface.page").value == "#FDFDFB"
    assert notes == [
        "the axis scheme is not checked: the owner left it out in mapping.json, so every role "
        "is read at the system's base",
        "color.text.default is not checked: the owner left it out in mapping.json"]
    assert their_names("color.text.default (scheme:dark)", mapping) == (
        "color.text.default (scheme:dark)")
    # Under our own names too, a not mapped role is out and the set is not
    # checked as a whole.
    own = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    mapping = propose(own)
    mapping.roles["color.text.default"] = NOT_MAPPED_ROLE
    checked, notes = view(own, mapping)
    assert checked is not own and not checked.has("color.text.default")
    assert notes == ["color.text.default is not checked: the owner left it out in the mapping"]


def test_a_reimport_keeps_what_the_owner_left_out_and_proposes_what_is_missing(tmp_path):
    ts = _css(to_css(build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens),
              "tokens.css")
    first = propose(ts)
    f = tmp_path / "mapping.json"
    f.write_text(dump_mapping(first), encoding="utf-8")
    # The owner keeps one role and the contrast axis out, and deletes the
    # line for another role.
    doc = json.loads(f.read_text(encoding="utf-8"))
    doc["roles"]["color.text.default"] = {"token": None, "by": "owner"}
    doc["axes"]["contrast"] = {"from": None, "by": "owner"}
    del doc["roles"]["color.surface.page"]
    f.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    # A new import proposes again and merges with the owner's file.
    merged, notes = merge(propose(ts), load_mapping(f), f.name)
    assert merged.roles["color.text.default"] == NOT_MAPPED_ROLE
    assert merged.axes["contrast"] == NOT_MAPPED_AXIS
    assert merged.roles["color.surface.page"] == RoleMap("color-surface-page", "name")
    assert notes == [
        "mapping.json did not map color.surface.page, so it was proposed as color-surface-page "
        "by name; to keep it out of the check, write {\"token\": null, \"by\": \"owner\"} for it"]
    f.write_text(dump_mapping(merged), encoding="utf-8")
    again = load_mapping(f)
    assert again == merged and merge(propose(ts), again, f.name) == (merged, [])
    checked, notes = view(ts, again, f.name)
    assert not checked.has("color.text.default") and checked.has("color.surface.page")
    assert "contrast" not in checked.axes and "scheme" in checked.axes
    assert notes == [
        "the axis contrast is not checked: the owner left it out in mapping.json, so every role "
        "is read at the system's base",
        "color.text.default is not checked: the owner left it out in mapping.json"]


def test_an_axis_deleted_from_a_foreign_mapping_is_named_and_a_null_is_not():
    ts = _css(FOREIGN)
    mapping = propose(ts)
    source = mapping.axes["scheme"].source
    del mapping.axes["scheme"]
    _, notes = view(ts, mapping, "mapping.json")
    assert [n for n in notes if "the axis scheme" in n] == [
        f"mapping.json leaves out the axis scheme, which the imported system has as {source}, "
        "so it was not checked and every role is read at the system's base; map it to check "
        'it, or write {"from": null, "by": "owner"} for it to keep it out on purpose']
    mapping.axes["scheme"] = AxisMap(None, {}, "owner")
    _, notes = view(ts, mapping, "mapping.json")
    assert [n for n in notes if "leaves out the axis" in n] == []


def test_merge_and_the_loop_finder_are_exported():
    import engine.io
    from engine.io.graph import cycles, loop
    assert engine.io.merge is merge and engine.io.cycles is cycles and engine.io.loop is loop
    assert {"merge", "cycles", "loop"} <= set(engine.io.__all__)
