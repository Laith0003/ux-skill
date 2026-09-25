"""The Figma importer: a variables export (the REST shape, with or without
its meta wrapper, which the plugin reader writes too) read in the file's own
names. Scopes decide a number's unit; a collection with two modes is one
axis, and modes named for a known axis (Light and Dark) read into it;
anything else is reported, never guessed. No network call."""
import ast
import copy
import json
from pathlib import Path

import pytest

from engine.foundations.errors import InputError
from engine.io.figma_in import REST_ENDPOINT, SIZE_SCOPES, import_figma, read_figma
from engine.io.report import Source


def _var(vid, name, collection, kind, values, scopes=("ALL_SCOPES",), description=""):
    return {"id": vid, "name": name, "variableCollectionId": collection, "resolvedType": kind,
            "valuesByMode": values, "scopes": list(scopes), "description": description,
            "hiddenFromPublishing": False, "remote": False}


def _alias(vid):
    return {"type": "VARIABLE_ALIAS", "id": vid}


def _collection(cid, name, modes, variable_ids, default=None):
    modes = [{"modeId": f"{cid}:{n}", "name": n} for n in modes]
    return {"id": cid, "name": name, "defaultModeId": default or modes[0]["modeId"],
            "modes": modes, "variableIds": list(variable_ids)}


EXPORT = {
    "status": 200, "error": False,
    "meta": {
        "variableCollections": {
            "c:color": {"id": "c:color", "name": "Color", "defaultModeId": "m:light",
                        "modes": [{"modeId": "m:light", "name": "Light"},
                                  {"modeId": "m:dark", "name": "Dark"}],
                        "variableIds": ["v:1", "v:2", "v:3", "v:4", "v:5"]},
            "c:size": {"id": "c:size", "name": "Size", "defaultModeId": "m:one",
                       "modes": [{"modeId": "m:one", "name": "Value"}],
                       "variableIds": ["v:6", "v:7", "v:8", "v:9", "v:10", "v:11"]},
            "c:type": {"id": "c:type", "name": "Type", "defaultModeId": "m:lg",
                       "modes": [{"modeId": "m:sm", "name": "SM"},
                                 {"modeId": "m:lg", "name": "LG"},
                                 {"modeId": "m:xl", "name": "XL"}],
                       "variableIds": ["v:12", "v:13"]},
        },
        "variables": {
            "v:1": _var("v:1", "ink/900", "c:color", "COLOR",
                        {"m:light": {"r": 0.09, "g": 0.1, "b": 0.12, "a": 1},
                         "m:dark": {"r": 0.09, "g": 0.1, "b": 0.12, "a": 1}}),
            "v:2": _var("v:2", "paper", "c:color", "COLOR",
                        {"m:light": {"r": 1, "g": 1, "b": 1, "a": 1},
                         "m:dark": {"r": 1, "g": 1, "b": 1, "a": 1}}),
            "v:3": _var("v:3", "text/Body Copy", "c:color", "COLOR",
                        {"m:light": _alias("v:1"), "m:dark": _alias("v:2")},
                        description="Running text."),
            "v:4": _var("v:4", "veil", "c:color", "COLOR",
                        {"m:light": {"r": 0, "g": 0, "b": 0, "a": 0.4},
                         "m:dark": {"r": 0, "g": 0, "b": 0, "a": 0.6}}),
            "v:5": _var("v:5", "brand/shared", "c:color", "COLOR",
                        {"m:light": _alias("v:remote"), "m:dark": _alias("v:remote")}),
            "v:6": _var("v:6", "space/4", "c:size", "FLOAT", {"m:one": 16},
                        ["GAP", "WIDTH_HEIGHT"]),
            "v:7": _var("v:7", "radius/card", "c:size", "FLOAT", {"m:one": 12},
                        ["CORNER_RADIUS"]),
            "v:8": _var("v:8", "weight/strong", "c:size", "FLOAT", {"m:one": 600},
                        ["FONT_WEIGHT"]),
            "v:9": _var("v:9", "z/dialog", "c:size", "FLOAT", {"m:one": 2100}),
            "v:10": _var("v:10", "flag/beta", "c:size", "BOOLEAN", {"m:one": True}),
            "v:11": _var("v:11", "font/body", "c:size", "STRING", {"m:one": "Body Sans"},
                         ["FONT_FAMILY"]),
            "v:12": _var("v:12", "size/body", "c:type", "FLOAT",
                         {"m:sm": 15, "m:lg": 16, "m:xl": 16}, ["FONT_SIZE"]),
            "v:13": _var("v:13", "label/copy", "c:type", "STRING",
                         {"m:sm": "Hi", "m:lg": "Hi", "m:xl": "Hi"}, ["TEXT_CONTENT"]),
        },
    },
}


def _import(doc, **kw):
    text = json.dumps(doc)
    return import_figma(text, Source("variables.json", "figma", "0" * 64, len(text)), **kw)


def _one(collection, variables):
    """An export of one collection and its variables."""
    return {"variableCollections": {collection["id"]: collection},
            "variables": {v["id"]: v for v in variables}}


def _rows(items):
    return [(i.name, i.message) for i in items]


def test_variables_keep_the_files_names_and_modes():
    imported = _import(EXPORT)
    ts = imported.tokens
    assert [(t.path, t.type) for t in ts.tokens()] == [
        ("ink.900", "color"), ("paper", "color"), ("text.Body-Copy", "color"),
        ("veil", "color"), ("space.4", "dimension"), ("radius.card", "dimension"),
        ("weight.strong", "fontWeight"), ("z.dialog", "number"), ("font.body", "fontFamily"),
        ("size.body", "dimension")]
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert (ts.get("ink.900").value, ts.get("ink.900").modes) == ("#171A1F", {})
    assert ts.get("ink.900").layer == "primitive"
    text = ts.get("text.Body-Copy")
    assert (text.value, text.modes, text.layer, text.description) == (
        "{ink.900}", {"scheme:dark": "{paper}"}, "semantic", "Running text.")
    assert (ts.get("veil").value, ts.get("veil").modes) == (
        "#00000066", {"scheme:dark": "#00000099"})
    assert ts.get("space.4").value == {"value": 16, "unit": "px"}
    assert ts.get("weight.strong").value == 600
    assert ts.get("z.dialog").value == 2100
    assert ts.get("size.body").value == {"value": 16, "unit": "px"}
    assert ts.get("font.body").value == ["Body Sans"]


def test_the_report_names_what_it_renamed_noted_and_did_not_read():
    report = _import(EXPORT).report
    assert report.source.format == "figma" and report.entries == 13 and report.tokens == 10
    assert [(i.where, i.name, i.message) for i in report.renamed] == [
        ("variables.json Color/text/Body Copy", "text/Body Copy",
         "read as text.Body-Copy; a slash reads as a dot, and a path segment holds only "
         "letters, digits, '_' and '-'")]
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("variables.json Color", "Color",
         "has the modes Light and Dark, read as the scheme axis: Light is the base and Dark "
         "is scheme:dark"),
        ("variables.json Size/z/dialog", "z/dialog",
         "has no scope that fixes its unit, so it was read as the plain number 2100; give it "
         "a scope in Figma (Gap, Corner radius, Font size and so on) to read it as a size"),
        ("variables.json Type", "Type",
         "has the modes SM, LG and XL; its default mode LG was read, and SM and XL were not, "
         "since a mode axis holds two values; pass the second mode to read with second_modes, "
         "for example {\"Type\": \"SM\"}")]
    assert _rows(report.not_read) == [
        ("brand/shared", "references v:remote in the mode Light of Color, a variable from "
                         "another file that this export does not hold; import that library's "
                         "export too, or detach the variable in Figma"),
        ("flag/beta", "a boolean, and the engine holds no boolean tokens; keep it in Figma, "
                      "where it switches components"),
        ("label/copy", "a text variable scoped to TEXT_CONTENT; the engine reads text only as "
                       "a font family, so if it names a font, give it only the Font family "
                       "scope in Figma")]
    assert "## Not read" in report.markdown() and "scheme (light is the base, dark)" \
        in report.markdown()


def test_a_second_mode_can_be_chosen_for_a_collection_with_more():
    ts = _import(EXPORT, second_modes={"Type": "SM"}).tokens
    assert dict(ts.axes) == {"scheme": ("light", "dark"), "lg-sm": ("lg", "sm")}
    assert ts.get("size.body").modes == {"lg-sm:sm": {"value": 15, "unit": "px"}}


def test_an_unknown_second_mode_is_named():
    with pytest.raises(InputError) as exc:
        _import(EXPORT, second_modes={"Type": "Tablet"})
    assert str(exc.value) == ("second_modes names the mode Tablet of Type, which has the modes "
                              "SM, LG and XL; pass SM or XL, a mode other than its default LG")


def test_second_modes_naming_the_default_or_a_small_collection_is_named():
    with pytest.raises(InputError) as exc:
        _import(EXPORT, second_modes={"Type": "LG"})
    assert str(exc.value) == ("second_modes names LG, the default mode of Type, which is read "
                              "as the base already; pass SM or XL")
    with pytest.raises(InputError) as exc:
        _import(EXPORT, second_modes={"Color": "Dark"})
    assert str(exc.value) == ("second_modes names Color, which has 2 modes, so every mode it "
                              "has is read already; leave Color out of second_modes")
    with pytest.raises(InputError) as exc:
        _import(EXPORT, second_modes={"Sizes": "SM"})
    assert str(exc.value) == ("second_modes names the collection Sizes, which this export does "
                              "not hold; pass a collection with more than two modes: Type")


def test_the_bare_shape_without_meta_reads_the_same():
    bare = dict(EXPORT["meta"])
    assert [t.path for t in _import(bare).tokens.tokens()] == [
        t.path for t in _import(EXPORT).tokens.tokens()]


def test_a_file_that_is_not_a_variables_export_is_named(tmp_path):
    f = tmp_path / "file.json"
    f.write_text(json.dumps({"document": {}}), encoding="utf-8")
    with pytest.raises(InputError) as exc:
        read_figma(f)
    assert str(exc.value) == (
        f"--from {f} is not a Figma variables export: it has no variables and "
        "variableCollections; export them with the Figma REST endpoint "
        "GET /v1/files/<file key>/variables/local")
    assert REST_ENDPOINT == "GET /v1/files/<file key>/variables/local"


def test_invalid_json_and_an_error_response_are_named(tmp_path):
    f = tmp_path / "variables.json"
    f.write_text("{", encoding="utf-8")
    with pytest.raises(InputError) as exc:
        read_figma(f, "--figma")
    assert str(exc.value).startswith(f"--figma {f} is not valid JSON (")
    assert str(exc.value).endswith(f"); export the variables again with {REST_ENDPOINT}")
    f.write_text(json.dumps({"status": 403, "error": True, "message": "Invalid token"}),
                 encoding="utf-8")
    with pytest.raises(InputError) as exc:
        read_figma(f)
    assert str(exc.value) == (
        f"--from {f} is an error Figma sent back (403: Invalid token), not a variables export; "
        f"export again with a token that can read the file, from {REST_ENDPOINT}")


def test_a_dark_default_still_reads_light_as_the_base():
    col = _collection("c:1", "Theme", ["Dark mode", "Light mode"], ["v:1"])
    doc = _one(col, [_var("v:1", "surface", "c:1", "COLOR",
                          {"c:1:Dark mode": {"r": 0, "g": 0, "b": 0, "a": 1},
                           "c:1:Light mode": {"r": 1, "g": 1, "b": 1, "a": 1}})])
    imported = _import(doc)
    assert dict(imported.tokens.axes) == {"scheme": ("light", "dark")}
    surface = imported.tokens.get("surface")
    assert (surface.value, surface.modes) == ("#FFFFFF", {"scheme:dark": "#000000"})
    assert _rows(imported.report.notes) == [
        ("Theme", "has the modes Dark mode and Light mode, read as the scheme axis: Light mode "
                  "is the base and Dark mode is scheme:dark; the default mode in Figma is "
                  "Dark mode, and the engine's base is the light one")]


def test_other_two_mode_collections_are_one_axis_in_the_files_names():
    col = _collection("c:1", "Brand", ["Main", "Partner"], ["v:1"])
    doc = _one(col, [_var("v:1", "accent", "c:1", "COLOR",
                          {"c:1:Main": {"r": 1, "g": 0, "b": 0, "a": 1},
                           "c:1:Partner": {"r": 0, "g": 0, "b": 1, "a": 1}})])
    imported = _import(doc)
    assert dict(imported.tokens.axes) == {"main-partner": ("main", "partner")}
    assert imported.tokens.get("accent").modes == {"main-partner:partner": "#0000FF"}
    assert _rows(imported.report.notes) == [
        ("Brand", "has the modes Main and Partner, read as the axis main-partner: Main, its "
                  "default mode, is the base and Partner is main-partner:partner")]


def test_modes_that_cannot_name_an_axis_read_the_default_only():
    col = _collection("c:1", "Density", ["1x", "2x"], ["v:1"])
    doc = _one(col, [_var("v:1", "gap", "c:1", "FLOAT", {"c:1:1x": 8, "c:1:2x": 16}, ["GAP"])])
    imported = _import(doc)
    assert dict(imported.tokens.axes) == {}
    assert imported.tokens.get("gap").value == {"value": 8, "unit": "px"}
    assert _rows(imported.report.notes) == [
        ("Density", "has the modes 1x and 2x, which cannot name a mode axis; its default mode "
                    "1x was read and 2x was not; rename the modes in Figma so each starts with "
                    "a letter and the two differ")]


def test_a_color_keeps_its_alpha_and_one_outside_srgb_is_mapped():
    col = _collection("c:1", "Color", ["Value"], ["v:1", "v:2"])
    doc = _one(col, [
        _var("v:1", "scrim", "c:1", "COLOR", {"c:1:Value": {"r": 0, "g": 0, "b": 0, "a": 0.5}}),
        _var("v:2", "vivid", "c:1", "COLOR",
             {"c:1:Value": {"r": 1.2, "g": 0.1, "b": -0.05, "a": 1}})])
    imported = _import(doc)
    assert imported.tokens.get("scrim").value == "#00000080"
    vivid = imported.tokens.get("vivid").value
    assert vivid.startswith("#") and len(vivid) == 7
    [mapped] = imported.report.mapped
    assert (mapped.where, mapped.name, mapped.original, mapped.hex) == (
        "variables.json Color/vivid", "vivid", '{"r": 1.2, "g": 0.1, "b": -0.05}', vivid)
    assert mapped.distance > 0
    assert imported.report.not_read == []


def test_values_it_cannot_read_are_named_with_the_mode_and_the_fix():
    col = _collection("c:1", "Color", ["Light", "Dark"], ["v:1", "v:2", "v:3", "v:4"])
    doc = _one(col, [
        _var("v:1", "bg", "c:1", "COLOR", {"c:1:Light": {"r": 1, "g": 1, "b": 1, "a": 1}}),
        _var("v:2", "fg", "c:1", "COLOR",
             {"c:1:Light": "#000000", "c:1:Dark": {"r": 0, "g": 0, "b": 0, "a": 1}}),
        _var("v:3", "line", "c:1", "COLOR",
             {"c:1:Light": {"r": 0, "g": 0, "b": 0, "a": 1.5},
              "c:1:Dark": {"r": 0, "g": 0, "b": 0, "a": 1}}),
        _var("v:4", "gap", "c:1", "FLOAT", {"c:1:Light": "8px", "c:1:Dark": 8}, ["GAP"])])
    assert _rows(_import(doc).report.not_read) == [
        ("bg", "has no value for the mode Dark of Color; set one in Figma and export again"),
        ("fg", "holds \"#000000\" in the mode Light of Color, not a color; Figma writes a "
               "color as r, g, b and a from 0 to 1, so export the variables again"),
        ("line", "has the alpha 1.5 in the mode Light of Color; Figma writes alpha from 0 to "
                 "1, so set it again in Figma"),
        ("gap", "holds \"8px\" in the mode Light of Color, not a number; export the variables "
                "again")]


def test_figmas_float_noise_is_read_to_four_decimals():
    col = _collection("c:1", "Type", ["Value"], ["v:1", "v:2"])
    doc = _one(col, [
        _var("v:1", "tracking/tight", "c:1", "FLOAT", {"c:1:Value": -0.20000000298023224},
             ["LETTER_SPACING"]),
        _var("v:2", "opacity/muted", "c:1", "FLOAT", {"c:1:Value": 40.0}, ["OPACITY"])])
    imported = _import(doc)
    assert imported.tokens.get("tracking.tight").value == {"value": -0.2, "unit": "px"}
    assert imported.tokens.get("opacity.muted").value == 40
    assert _rows(imported.report.notes) == [
        ("opacity/muted", "is scoped to OPACITY, which Figma writes from 0 to 100, so it was "
                          "read as the plain number 40; divide it by 100 where a value from 0 "
                          "to 1 is wanted")]


def test_mixed_scopes_read_a_plain_number_with_a_note():
    col = _collection("c:1", "Size", ["Value"], ["v:1"])
    doc = _one(col, [_var("v:1", "odd", "c:1", "FLOAT", {"c:1:Value": 4}, ["GAP", "OPACITY"])])
    imported = _import(doc)
    assert imported.tokens.get("odd").type == "number"
    assert _rows(imported.report.notes) == [
        ("odd", "has the scopes GAP and OPACITY, which do not share one unit, so it was read "
                "as the plain number 4; keep only size scopes in Figma to read it as a size")]


def test_references_to_what_was_not_read_and_loops_are_named():
    col = _collection("c:1", "Color", ["Value"], ["v:1", "v:2", "v:3", "v:4", "v:5"])
    doc = _one(col, [
        _var("v:1", "flag", "c:1", "BOOLEAN", {"c:1:Value": False}),
        _var("v:2", "uses-flag", "c:1", "COLOR", {"c:1:Value": _alias("v:1")}),
        _var("v:3", "a", "c:1", "COLOR", {"c:1:Value": _alias("v:4")}),
        _var("v:4", "b", "c:1", "COLOR", {"c:1:Value": _alias("v:3")}),
        _var("v:5", "on-a", "c:1", "COLOR", {"c:1:Value": _alias("v:3")})])
    imported = _import(doc)
    assert imported.tokens.tokens() == []
    assert _rows(imported.report.not_read) == [
        ("flag", "a boolean, and the engine holds no boolean tokens; keep it in Figma, where it "
                 "switches components"),
        ("uses-flag", "references flag in the mode Value of Color, which was not read; fix flag "
                      "and import again"),
        ("a", "references b in the mode Value of Color, which leads back to it (a -> b -> a); "
              "point one of them at a value in Figma"),
        ("b", "references a in the mode Value of Color, which leads back to it (b -> a -> b); "
              "point one of them at a value in Figma"),
        ("on-a", "references a in the mode Value of Color, which was not read; fix a and "
                 "import again")]


def test_two_variables_on_one_path_keep_the_first():
    one = _collection("c:1", "Base", ["Value"], ["v:1"])
    two = _collection("c:2", "Brand", ["Value"], ["v:2"])
    doc = {"variableCollections": {"c:1": one, "c:2": two},
           "variables": {"v:1": _var("v:1", "color/bg", "c:1", "COLOR",
                                     {"c:1:Value": {"r": 1, "g": 1, "b": 1, "a": 1}}),
                         "v:2": _var("v:2", "color/bg", "c:2", "COLOR",
                                     {"c:2:Value": {"r": 0, "g": 0, "b": 0, "a": 1}})}}
    imported = _import(doc)
    assert imported.tokens.get("color.bg").value == "#FFFFFF"
    assert [(i.where, i.name, i.message) for i in imported.report.not_read] == [
        ("variables.json Brand/color/bg", "color/bg",
         "is read as color.bg, the path of Base/color/bg read earlier; rename one of the two in "
         "Figma")]


def test_a_deleted_variable_is_not_read():
    col = _collection("c:1", "Color", ["Value"], ["v:1"])
    gone = _var("v:1", "old", "c:1", "COLOR", {"c:1:Value": {"r": 1, "g": 1, "b": 1, "a": 1}})
    gone["deletedButReferenced"] = True
    assert _rows(_import(_one(col, [gone])).report.not_read) == [
        ("old", "was deleted in Figma and is kept only because something still references it; "
                "restore it, or point those references at another variable")]


def test_the_import_is_deterministic_and_does_not_change_its_input():
    doc = copy.deepcopy(EXPORT)
    first = _import(doc)
    assert doc == EXPORT
    second = _import(EXPORT)
    assert first.report.to_dict() == second.report.to_dict()
    assert [(t.path, t.value, t.modes) for t in first.tokens.tokens()] == [
        (t.path, t.value, t.modes) for t in second.tokens.tokens()]
    assert "FONT_SIZE" in SIZE_SCOPES and "OPACITY" not in SIZE_SCOPES


def test_the_reader_does_not_import_the_writer():
    import engine.io.figma_in

    tree = ast.parse(Path(engine.io.figma_in.__file__).read_text(encoding="utf-8"))
    names = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert "engine.foundations.emit" not in names


def test_the_package_exports_the_importer():
    import engine.io

    assert engine.io.read_figma is read_figma and engine.io.import_figma is import_figma
    assert {"import_figma", "read_figma", "import_markdown", "Mapped", "GamutMapped",
            "CSS_KEYWORDS"} <= set(engine.io.__all__)


# The REST export also holds the library variables the file uses, marked
# remote, with their collections. They belong to another file.
LIBRARY = {
    "variableCollections": {
        "c:lib": {"id": "c:lib", "name": "Shared Palette", "remote": True,
                  "defaultModeId": "m:a", "modes": [{"modeId": "m:a", "name": "Default"},
                                                    {"modeId": "m:b", "name": "Partner"}],
                  "variableIds": ["v:lib1"]},
        "c:own": _collection("c:own", "Color", ["Light", "Dark"], ["v:1", "v:2", "v:3"]),
    },
    "variables": {
        "v:lib1": dict(_var("v:lib1", "white", "c:lib", "COLOR",
                            {"m:a": {"r": 1, "g": 1, "b": 1, "a": 1},
                             "m:b": {"r": 1, "g": 1, "b": 1, "a": 1}}), remote=True),
        "v:1": _var("v:1", "surface/base", "c:own", "COLOR",
                    {"c:own:Light": _alias("v:lib1"),
                     "c:own:Dark": {"r": 0, "g": 0, "b": 0, "a": 1}}),
        "v:2": _var("v:2", "surface/raised", "c:own", "COLOR",
                    {"c:own:Light": _alias("v:gone"),
                     "c:own:Dark": {"r": 0, "g": 0, "b": 0, "a": 1}}),
        "v:3": _var("v:3", "ink", "c:own", "COLOR",
                    {"c:own:Light": {"r": 0, "g": 0, "b": 0, "a": 1},
                     "c:own:Dark": {"r": 1, "g": 1, "b": 1, "a": 1}}),
    },
}


def test_library_variables_in_the_export_are_not_read_as_the_files_own():
    imported = _import(LIBRARY)
    assert [t.path for t in imported.tokens.tokens()] == ["ink"]
    assert dict(imported.tokens.axes) == {"scheme": ("light", "dark")}
    report = imported.report
    assert report.entries == 3 and report.tokens == 1
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("variables.json Shared Palette", "Shared Palette",
         "is a library collection from another file (remote in the export); the 1 variable "
         "of it this file uses was not read as this file's tokens; import that library's own "
         "export to read them"),
        ("variables.json Color", "Color",
         "has the modes Light and Dark, read as the scheme axis: Light is the base and Dark "
         "is scheme:dark")]
    assert _rows(report.not_read) == [
        ("surface/base", "references white in the mode Light of Color, a variable of the "
                         "library collection Shared Palette in another file; import that "
                         "library's export too, or detach the variable in Figma"),
        ("surface/raised", "references v:gone in the mode Light of Color, a variable from "
                           "another file that this export does not hold; import that "
                           "library's export too, or detach the variable in Figma")]


def test_a_remote_variable_is_library_even_in_a_collection_not_marked_remote():
    doc = copy.deepcopy(LIBRARY)
    del doc["variableCollections"]["c:lib"]["remote"]
    imported = _import(doc)
    assert [t.path for t in imported.tokens.tokens()] == ["ink"]
    assert "main-partner" not in imported.tokens.axes
    assert _rows(imported.report.not_read)[0][1].startswith(
        "references white in the mode Light of Color, a variable of the library collection "
        "Shared Palette")


def test_second_modes_naming_a_library_collection_is_named():
    with pytest.raises(InputError) as exc:
        _import(LIBRARY, second_modes={"Shared Palette": "Partner"})
    assert str(exc.value) == ("second_modes names Shared Palette, a library collection from "
                              "another file, whose variables are not read as this file's "
                              "tokens; leave Shared Palette out of second_modes")


def test_a_size_that_aliases_an_unscoped_number_names_the_fix():
    col = _collection("c:1", "Size", ["Value"], ["v:1", "v:2", "v:3"])
    doc = _one(col, [_var("v:1", "num/8", "c:1", "FLOAT", {"c:1:Value": 8}),
                     _var("v:2", "space/md", "c:1", "FLOAT", {"c:1:Value": _alias("v:1")},
                          ["GAP"]),
                     _var("v:3", "weight/body", "c:1", "FLOAT", {"c:1:Value": _alias("v:1")},
                          ["FONT_WEIGHT"])])
    notes = _rows(_import(doc).report.notes)
    assert notes[1:] == [
        ("space/md", "aliases num/8 in the mode Value of Size, which was read as a number, "
                     "where a dimension is wanted; give num/8 a size scope in Figma (Gap, "
                     "Corner radius, Font size and so on) and import again"),
        ("weight/body", "aliases num/8 in the mode Value of Size, which was read as a number, "
                        "where a fontWeight is wanted; give num/8 only the Font weight scope in "
                        "Figma and import again")]


def test_standard_and_high_are_contrast_only_where_contrast_is_named():
    def axes(collection, modes):
        col = _collection("c:1", collection, modes, ["v:1"])
        doc = _one(col, [_var("v:1", "gap", "c:1", "FLOAT",
                              {f"c:1:{m}": 8 for m in modes}, ["GAP"])])
        return dict(_import(doc).tokens.axes)
    assert axes("Density", ["Standard", "High"]) == {"standard-high": ("standard", "high")}
    assert axes("Contrast", ["Standard", "High"]) == {"contrast": ("standard", "high")}
    assert axes("Theme", ["Standard", "High contrast"]) == {"contrast": ("standard", "high")}


def test_light_and_dark_among_more_modes_read_the_scheme_when_chosen():
    col = _collection("c:1", "Theme", ["Light", "Dark", "Dim"], ["v:1"])
    doc = _one(col, [_var("v:1", "bg", "c:1", "COLOR", {
        "c:1:Light": {"r": 1, "g": 1, "b": 1, "a": 1},
        "c:1:Dark": {"r": 0, "g": 0, "b": 0, "a": 1},
        "c:1:Dim": {"r": 0.2, "g": 0.2, "b": 0.2, "a": 1}})])
    assert "for example {\"Theme\": \"Dark\"}" in _import(doc).report.notes[0].message
    imported = _import(doc, second_modes={"Theme": "Dark"})
    assert dict(imported.tokens.axes) == {"scheme": ("light", "dark")}
    assert imported.tokens.get("bg").modes == {"scheme:dark": "#000000"}
    assert _rows(imported.report.notes) == [
        ("Theme", "has the modes Light, Dark and Dim, read as the scheme axis: Light is the "
                  "base and Dark is scheme:dark; Dim was not read")]


def test_a_mapped_color_names_its_mode_and_keeps_its_alpha():
    col = _collection("c:1", "Color", ["Light", "Dark"], ["v:1"])
    doc = _one(col, [_var("v:1", "vivid", "c:1", "COLOR", {
        "c:1:Light": {"r": 0, "g": 0, "b": 0, "a": 1},
        "c:1:Dark": {"r": 1.2, "g": 0.1, "b": -0.05, "a": 0.5}})])
    imported = _import(doc)
    [mapped] = imported.report.mapped
    assert mapped.where == "variables.json Color/vivid in the mode Dark"
    assert mapped.hex.endswith("80") and len(mapped.hex) == 9
    assert imported.tokens.get("vivid").modes == {"scheme:dark": mapped.hex}


def test_a_path_is_free_again_when_its_first_holder_is_not_read():
    col = _collection("c:1", "Color", ["Value"], ["v:1", "v:2", "v:3"])
    doc = _one(col, [_var("v:1", "flag", "c:1", "BOOLEAN", {"c:1:Value": True}),
                     _var("v:2", "color/bg", "c:1", "COLOR", {"c:1:Value": _alias("v:1")}),
                     _var("v:3", "color/bg", "c:1", "COLOR",
                          {"c:1:Value": {"r": 1, "g": 1, "b": 1, "a": 1}})])
    imported = _import(doc)
    assert imported.tokens.get("color.bg").value == "#FFFFFF"
    assert [n for n, _ in _rows(imported.report.not_read)] == ["flag", "color/bg"]
