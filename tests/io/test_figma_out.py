"""The Figma exporter: one variable collection per foundation with its
modes, primitives hidden and unscoped, semantics aliasing them, typography
roles as one variable per field, applied by name so a second run updates in
place. The engine writes a payload and a script for Figma's plugin API; it
makes no network call. What Figma variables cannot hold is listed. Beside a
Figma source the engine did not write, only an extension is written: the
additions, in the source's own collections, modes and names."""
import copy
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from engine.foundations.build import build_system
from engine.foundations.errors import InputError
from engine.foundations.modes import contexts
from engine.foundations.tokens import Token, TokenSet
from engine.io.figma_in import import_figma, read_figma
from engine.io.figma_out import (
    ADDITIONS, APPLY_SCRIPT, READ_SCRIPT, as_export, figma_extension, figma_files, to_figma,
    write_figma)
from engine.io.report import Source
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)
NODE = shutil.which("node")


def _system():
    return build_system(NEUTRAL, "#3366FF").tokens


def _payload():
    return to_figma(_system())


def _copy(ts):
    """A token set with its own copy of every token."""
    out = TokenSet(dict(ts.axes))
    for t in ts.tokens():
        out.add(Token(t.path, t.type, copy.deepcopy(t.value), modes=copy.deepcopy(t.modes),
                      layer=t.layer, description=t.description,
                      extensions=copy.deepcopy(t.extensions)))
    return out


def _collection(payload, name):
    return next(c for c in payload["collections"] if c["name"] == name)


def _variable(collection, name):
    return next(v for v in collection["variables"] if v["name"] == name)


def _source(text, name="variables.json"):
    return Source(name, "figma", "0" * 64, len(text))


def test_one_collection_per_foundation_with_its_modes():
    payload = _payload()
    assert payload["version"] == 1
    assert payload["mode"] == "system"
    assert [(c["name"], c["modes"]) for c in payload["collections"]] == [
        ("color", ["light standard", "light high", "dark standard", "dark high"]),
        ("space", ["comfortable", "compact"]), ("radius", ["default"]),
        ("border", ["standard", "high"]), ("elevation", ["default"]),
        ("motion", ["ltr standard", "ltr reduced", "rtl standard", "rtl reduced"]),
        ("layout", ["comfortable", "compact"]),
        ("type", ["light standard ltr", "light standard rtl", "light high ltr", "light high rtl",
                  "dark standard ltr", "dark standard rtl", "dark high ltr", "dark high rtl"]),
        ("imagery", ["standard", "high"])]


def test_primitives_are_hidden_and_unscoped_and_roles_alias_them():
    color = _collection(_payload(), "color")
    brand = _variable(color, "color/brand/500")
    assert (brand["type"], brand["hidden"], brand["scopes"]) == ("COLOR", True, [])
    assert brand["values"]["light standard"] == {"r": 0.2, "g": 0.4, "b": 1.0, "a": 1}
    page = _variable(color, "color/surface/page")
    assert (page["hidden"], page["scopes"]) == (False, ["FRAME_FILL", "SHAPE_FILL"])
    assert page["values"]["light standard"] == {"alias": "color:color/neutral/50"}
    assert _variable(color, "color/text/default")["scopes"] == ["TEXT_FILL"]
    assert _variable(color, "color/syntax/keyword")["scopes"] == ["TEXT_FILL"]
    assert _variable(color, "color/status/danger/on-strong")["scopes"] == ["TEXT_FILL"]
    assert _variable(color, "color/focus/ring")["scopes"] == ["STROKE_COLOR"]
    assert _variable(color, "color/line/input")["scopes"] == ["STROKE_COLOR"]
    assert _variable(color, "color/illustration/line")["scopes"] == ["STROKE_COLOR"]


def test_sizes_are_pixels_with_the_scope_that_binds_them():
    payload = _payload()
    gap = _variable(_collection(payload, "space"), "space/control/gap")
    assert (gap["type"], gap["scopes"]) == ("FLOAT", ["GAP"])
    assert gap["values"] == {"comfortable": {"alias": "space:space/3"},
                             "compact": {"alias": "space:space/2"}}
    assert _variable(_collection(payload, "space"), "space/3")["values"] == {
        "comfortable": 12, "compact": 12}
    card = _variable(_collection(payload, "radius"), "radius/card")
    assert card["scopes"] == ["CORNER_RADIUS"]
    layout = _collection(payload, "layout")
    assert _variable(layout, "layout/gutter/phone")["values"]["comfortable"] == {
        "alias": "space:space/4"}
    for name in ("layout/region-gap/phone", "layout/hero/padding-block/phone",
                 "layout/header/padding-block", "layout/footer/padding-block",
                 "layout/landing-gap/phone"):
        assert _variable(layout, name)["scopes"] == ["GAP"], name
    assert _variable(layout, "layout/container/max")["scopes"] == ["WIDTH_HEIGHT"]
    size = _variable(_collection(payload, "type"), "type/size/latin/3")
    assert size["values"] == {f"{s} {c} {d}": 16 for s in ("light", "dark")
                              for c in ("standard", "high") for d in ("ltr", "rtl")}
    icon = _variable(_collection(payload, "type"), "type/icon/size/control")
    assert icon["scopes"] == ["WIDTH_HEIGHT"]
    # A rem size is given in px.
    assert _variable(_collection(payload, "type"), "type/icon/control")["values"][
        "light standard ltr"] == 20
    assert _variable(_collection(payload, "border"), "border/outline")["scopes"] == [
        "STROKE_FLOAT"]
    imagery = _collection(payload, "imagery")
    assert _variable(imagery, "imagery/on-scrim")["scopes"] == ["TEXT_FILL"]
    assert _variable(imagery, "imagery/scrim")["scopes"] == ["FRAME_FILL", "SHAPE_FILL"]
    assert _variable(imagery, "imagery/shade/standard")["values"]["standard"] == {
        "r": 0.027451, "g": 0.05098, "b": 0.101961, "a": 0.564706}


def test_typography_roles_become_one_variable_per_field():
    t = _collection(_payload(), "type")
    names = [v["name"] for v in t["variables"] if v["name"].startswith("type/text/body/")]
    assert names == ["type/text/body/font-family", "type/text/body/font-size",
                     "type/text/body/font-weight", "type/text/body/letter-spacing",
                     "type/text/body/line-height"]
    size = _variable(t, "type/text/body/font-size")
    latin, arabic = {"alias": "type:type/size/latin/3"}, {"alias": "type:type/size/arabic/3"}
    assert (size["scopes"], size["values"]) == (
        ["FONT_SIZE"], {f"{s} {c} {d}": latin if d == "ltr" else arabic
                        for s in ("light", "dark") for c in ("standard", "high")
                        for d in ("ltr", "rtl")})
    assert _variable(t, "type/text/body/line-height")["scopes"] == []
    assert _variable(t, "type/text/body/letter-spacing")["scopes"] == ["LETTER_SPACING"]
    assert _variable(t, "type/text/body/font-family")["scopes"] == ["FONT_FAMILY"]
    weight = _variable(t, "type/text/body/font-weight")
    assert weight["scopes"] == ["FONT_WEIGHT"]
    assert weight["values"]["light high ltr"] == {"alias": "type:type/weight/500"}
    # dark mode sets a variable face lighter at standard contrast
    assert weight["values"]["dark standard ltr"] == {"alias": "type:type/weight/360"}
    assert weight["values"]["dark high ltr"] == {"alias": "type:type/weight/500"}
    face = _variable(t, "type/face/text")
    assert (face["type"], face["values"]["light standard ltr"]) == ("STRING", "Noto Sans")
    assert (face["hidden"], face["scopes"]) == (True, [])


def test_what_figma_variables_cannot_hold_is_listed():
    payload = _payload()
    skipped = {s["token"]: s["why"] for s in payload["skipped"]}
    assert skipped["motion.reveal.curve"] == (
        "a curve; Figma variables hold colors, numbers, strings and booleans, so it stays in "
        "tokens.json and prototype settings")
    assert skipped["elevation.card"].startswith("a shadow; Figma keeps shadows in effect styles")
    assert skipped["border.style.default"].startswith("a stroke style")
    assert payload["notes"] == [
        "Sizes written in rem are given in px at 16px per rem, since Figma variables have no "
        "units.",
        "A font family keeps its first name; the fallbacks stay in tokens.json.",
        "Line heights are unitless ratios, and Figma binds a number to line height in px, so "
        "their variables have no scope.",
        "Durations are given in ms and have no scope, since no Figma field binds a duration, "
        "so they read back as plain numbers.",
        "22 sizes have no size scope, since no Figma field binds them or no role points at "
        "them, so they read back as plain numbers."]


def test_an_opacity_held_from_0_to_100_keeps_its_unit_and_the_opacity_scope():
    ts = _copy(_system())
    ts.add(Token("imagery.fade", "number", 40, layer="primitive",
                 extensions={"unit": "percent"}))
    payload = to_figma(ts)
    fade = _variable(_collection(payload, "imagery"), "imagery/fade")
    assert (fade["type"], fade["scopes"], fade["values"]["standard"]) == (
        "FLOAT", ["OPACITY"], 40)
    assert payload["notes"][-2] == ("Opacities held from 0 to 100 are given from 0 to 100 "
                                    "with the Opacity scope, as Figma holds them.")


def test_the_payload_is_deterministic():
    assert json.dumps(_payload()) == json.dumps(_payload())
    assert figma_files(_system()) == figma_files(_system())


def test_the_files_are_the_payload_and_the_script_with_it_inlined():
    files = figma_files(_system())
    assert list(files) == ["figma-variables.json", "figma-variables.js",
                           "figma-read-variables.js"]
    payload = json.loads(files["figma-variables.json"])
    script = files["figma-variables.js"]
    assert script.startswith("// Apply a ux-skill design system to this Figma file")
    assert "const PAYLOAD = " + json.dumps(payload, separators=(",", ":")) + ";" in script
    assert script.endswith(APPLY_SCRIPT)
    assert files["figma-read-variables.js"] == READ_SCRIPT
    for text in files.values():
        assert text.isascii()


def test_the_scripts_never_delete_and_never_rename_a_mode_they_did_not_make():
    assert ".remove(" not in APPLY_SCRIPT and "removeMode" not in APPLY_SCRIPT
    assert APPLY_SCRIPT.count("renameMode(") == 1
    for script in (APPLY_SCRIPT, READ_SCRIPT):
        assert "fetch(" not in script and "XMLHttpRequest" not in script


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_both_scripts_parse_as_javascript(tmp_path):
    files = figma_files(_system())
    for name in ("figma-variables.js", "figma-read-variables.js"):
        wrapped = tmp_path / name
        wrapped.write_text("(async () => {\n" + files[name] + "\n})();\n", encoding="utf-8")
        run = subprocess.run([NODE, "--check", str(wrapped)], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr


def _mode_contexts(modes, axes):
    """Each engine mode name as {axis: value}: the words at one position
    across the modes are the two values of one axis."""
    if modes == ["default"]:
        return {"default": {}}
    width = len(modes[0].split(" "))
    at = []
    for i in range(width):
        seen = {m.split(" ")[i] for m in modes}
        at.append(next(a for a, v in axes.items() if set(v) == seen))
    return {m: dict(zip(at, m.split(" "))) for m in modes}


def _compare(payload, back, axes):
    """Every exported variable, in every mode, reads back to the value the
    payload gives it there, aliases followed into the mode of the target's
    collection that agrees on the axes both have. Returns the count."""
    by_key = {f"{c['name']}:{v['name']}": (c, v) for c in payload["collections"]
              for v in c["variables"]}
    ctx_of = {c["name"]: _mode_contexts(c["modes"], axes) for c in payload["collections"]}

    def resolve(c, v, pairs):
        while True:
            mode = next(m for m, p in ctx_of[c["name"]].items()
                        if all(pairs.get(a, axes[a][0]) == val for a, val in p.items()))
            value = v["values"][mode]
            if not (isinstance(value, dict) and "alias" in value):
                return value
            c, v = by_key[value["alias"]]

    def figma_form(value):
        if isinstance(value, str) and value.startswith("#"):
            s = value[1:]
            rgb = [round(int(s[i:i + 2], 16) / 255, 6) for i in (0, 2, 4)]
            alpha = round(int(s[6:8], 16) / 255, 6) if len(s) == 8 else 1
            return {"r": rgb[0], "g": rgb[1], "b": rgb[2], "a": alpha}
        if isinstance(value, dict) and set(value) == {"value", "unit"}:
            return value["value"]
        if isinstance(value, list):
            return value[0]
        return value

    checked = 0
    for c in payload["collections"]:
        for v in c["variables"]:
            path = v["name"].replace("/", ".")
            for mode, pairs in ctx_of[c["name"]].items():
                ctx = ",".join(f"{a}:{val}" for a, val in pairs.items() if val != axes[a][0])
                got, want = figma_form(back.resolve(path, ctx)), resolve(c, v, pairs)
                if isinstance(want, float) or isinstance(got, float):
                    assert got == pytest.approx(want, abs=1e-4), (path, mode)
                else:
                    assert got == want, (path, mode)
                checked += 1
    return checked


def test_an_export_read_back_gives_the_same_names_and_values():
    ts = _system()
    payload = to_figma(ts)
    text = json.dumps(as_export(payload))
    imported = import_figma(text, _source(text))
    back = imported.tokens
    assert back.get("color.surface.page").value == "{color.neutral.50}"
    assert back.resolve("color.surface.page") == ts.resolve("color.surface.page")
    assert back.get("space.control.gap").value == "{space.3}"
    assert back.get("space.control.gap").modes == {"density:compact": "{space.2}"}
    assert back.resolve("space.4") == ts.resolve("space.4")
    exported = {v["name"].replace("/", ".") for c in payload["collections"]
                for v in c["variables"]}
    assert {t.path for t in back.tokens()} == exported
    assert imported.report.not_read == []
    # The mode names are the engine's own, so every mode comes back on its
    # own axes, and a combined mode that equals what its axes give is not
    # written twice.
    assert list(back.axes) == ["scheme", "contrast", "density", "direction", "motion"]
    assert back.get("type.text.body.font-size").modes == {"direction:rtl": "{type.size.arabic.3}"}
    assert back.get("type.face.text").type == "fontFamily"
    assert back.get("type.weight.500").type == "fontWeight"
    assert back.get("type.tracking.0").type == "dimension"
    for ctx in contexts(("scheme", "contrast"), ts.axes):
        assert back.resolve("color.surface.page", ctx) == ts.resolve("color.surface.page", ctx)
    for ctx in contexts(("direction", "contrast"), ts.axes):
        assert back.resolve("type.text.body.font-weight", ctx) == \
            ts.resolve("type.text.body", ctx)["fontWeight"]
    assert _compare(payload, back, ts.axes) > 1500
    # Every token keeps its type, except what the notes say reads back as a
    # plain number: durations, and sizes with no size scope.
    same = [t for t in back.tokens() if ts.has(t.path)]
    changed = {(ts.get(t.path).type, t.type) for t in same if ts.get(t.path).type != t.type}
    assert changed == {("duration", "number"), ("dimension", "number")}
    unscoped = sorted(t.path for t in same
                      if ts.get(t.path).type == "dimension" and t.type == "number")
    assert unscoped[:4] == ["border.width.0", "border.width.4", "layout.width.1120",
                            "layout.width.1440"]
    assert len(unscoped) == 22
    assert payload["notes"][-1] == (
        "22 sizes have no size scope, since no Figma field binds them or no role points at "
        "them, so they read back as plain numbers.")


def test_the_scripts_say_they_run_as_the_body_of_an_async_function():
    for script in (APPLY_SCRIPT, READ_SCRIPT):
        head = script.split("\nconst ")[0].replace("\n// ", " ")
        assert "as the body of an async function" in head


# ---------------------------------------------------------------- a source


def _var(vid, name, cid, kind, values, scopes, description=""):
    return {"id": vid, "name": name, "variableCollectionId": cid, "resolvedType": kind,
            "valuesByMode": values, "scopes": scopes, "description": description,
            "hiddenFromPublishing": False, "remote": False}


def _foreign():
    """An invented Figma file: a palette with one mode, a theme with Light
    and Dark, and a spacing collection."""
    alias = lambda vid: {"type": "VARIABLE_ALIAS", "id": vid}  # noqa: E731
    cols = {
        "c:1": {"id": "c:1", "name": "Palette", "defaultModeId": "1:0",
                "modes": [{"modeId": "1:0", "name": "Value"}], "variableIds": ["v:1", "v:2"]},
        "c:2": {"id": "c:2", "name": "Theme", "defaultModeId": "2:0",
                "modes": [{"modeId": "2:0", "name": "Light"}, {"modeId": "2:1", "name": "Dark"}],
                "variableIds": ["v:3", "v:4"]},
        "c:3": {"id": "c:3", "name": "Spacing", "defaultModeId": "3:0",
                "modes": [{"modeId": "3:0", "name": "Value"}], "variableIds": ["v:5"]},
    }
    variables = {
        "v:1": _var("v:1", "ink/900", "c:1", "COLOR", {"1:0": {"r": 0.1, "g": 0.1, "b": 0.1,
                                                               "a": 1}}, ["ALL_SCOPES"]),
        "v:2": _var("v:2", "paper/0", "c:1", "COLOR", {"1:0": {"r": 1, "g": 1, "b": 1, "a": 1}},
                    ["ALL_SCOPES"]),
        "v:3": _var("v:3", "bg/base", "c:2", "COLOR", {"2:0": alias("v:2"), "2:1": alias("v:1")},
                    ["FRAME_FILL"]),
        "v:4": _var("v:4", "fg/base", "c:2", "COLOR", {"2:0": alias("v:1"), "2:1": alias("v:2")},
                    ["TEXT_FILL"]),
        "v:5": _var("v:5", "gap/md", "c:3", "FLOAT", {"3:0": 12}, ["GAP"]),
    }
    return {"meta": {"variableCollections": cols, "variables": variables}}


def _write_source(tmp_path, doc=None):
    path = tmp_path / "variables.json"
    path.write_text(json.dumps(doc or _foreign(), indent=2) + "\n", encoding="utf-8")
    return path, read_figma(path)


def _extended(imported, *tokens):
    ts = _copy(imported.tokens)
    for t in tokens:
        ts.add(t)
    return ts


def test_an_import_records_the_files_collections_modes_and_names():
    text = json.dumps(_foreign())
    imported = import_figma(text, _source(text))
    assert imported.figma["collections"] == {
        "Palette": [["Value", ""]], "Theme": [["Light", ""], ["Dark", "scheme:dark"]],
        "Spacing": [["Value", ""]]}
    assert imported.figma["variables"]["bg.base"] == ["Theme", "bg/base"]
    assert imported.figma["scopes"]["bg.base"] == ["FRAME_FILL"]
    assert imported.owned is False


def test_an_extension_holds_only_the_additions_in_the_sources_collections(tmp_path):
    _, imported = _write_source(tmp_path)
    ts = _extended(imported,
                   Token("fg.muted", "color", "{ink.900}", modes={"scheme:dark": "{paper.0}"},
                         layer="semantic"),
                   Token("ink.500", "color", "#555555"),
                   Token("gap.lg", "dimension", {"value": 1.5, "unit": "rem"}))
    payload = figma_extension(imported, ts)
    assert payload["mode"] == "extend"
    assert [(c["name"], c["modes"], [v["name"] for v in c["variables"]])
            for c in payload["collections"]] == [
        ("Theme", ["Light", "Dark"], ["fg/muted"]), ("Palette", ["Value"], ["ink/500"]),
        ("Spacing", ["Value"], ["gap/lg"])]
    muted = _variable(_collection(payload, "Theme"), "fg/muted")
    assert muted["values"] == {"Light": {"alias": "Palette:ink/900"},
                               "Dark": {"alias": "Palette:paper/0"}}
    # Scoped as the file scopes fg/base, the variable of its type nearest it.
    assert muted["scopes"] == ["TEXT_FILL"]
    assert _variable(_collection(payload, "Palette"), "ink/500")["scopes"] == ["ALL_SCOPES"]
    assert _variable(_collection(payload, "Spacing"), "gap/lg")["scopes"] == ["GAP"]
    assert _variable(_collection(payload, "Spacing"), "gap/lg")["values"] == {"Value": 24}
    assert all(not c.get("new") for c in payload["collections"])


def test_an_addition_no_collection_can_hold_goes_in_a_new_one(tmp_path):
    _, imported = _write_source(tmp_path)
    ts = _extended(imported, Token("gap.dense", "dimension", {"value": 8, "unit": "px"},
                                   modes={"density:compact": {"value": 4, "unit": "px"}}))
    ts.axes = {**ts.axes, "density": ("comfortable", "compact")}
    payload = figma_extension(imported, ts)
    assert [(c["name"], c["modes"], c.get("new")) for c in payload["collections"]] == [
        (ADDITIONS, ["comfortable", "compact"], True)]


def test_an_extension_never_changes_what_the_source_holds(tmp_path):
    _, imported = _write_source(tmp_path)
    ts = _copy(imported.tokens)
    ts.get("gap.md").value = {"value": 14, "unit": "px"}
    with pytest.raises(InputError) as exc:
        figma_extension(imported, ts)
    assert str(exc.value) == (
        "gap/md is 12px in the collection Spacing of variables.json and 14px in the system to "
        "write; an extension only adds variables, so change gap/md in Figma itself, or add a "
        "token under a new name")


def test_writing_beside_a_foreign_source_writes_an_extension_through_intake(tmp_path):
    path, imported = _write_source(tmp_path)
    before = path.read_bytes()
    ts = _extended(imported, Token("ink.500", "color", "#555555"))
    done = write_figma(ts, imported)
    assert done["status"] == "written", done["message"]
    assert sorted(done["written"]) == [".uxskill/backup/" + imported.report.source.sha256[:12]
                                       + "/source/variables.json", ".uxskill/files.json",
                                       ".uxskill/intake/" + imported.report.source.sha256[:12]
                                       + ".json", "variables-ext.js", "variables-ext.json"]
    assert path.read_bytes() == before
    script = (tmp_path / "variables-ext.js").read_text(encoding="utf-8")
    assert script.startswith("/*\nux-skill-digest: ")
    assert done["file"] == str(tmp_path / "variables-ext.js")
    assert done["load"] == (
        f"Run {tmp_path / 'variables-ext.js'} in the Figma file {path.name} was exported from, "
        "through Figma's plugin API: it adds 1 variable and changes none that the file has.")
    assert done["load"] in done["message"]
    again = write_figma(ts, imported)
    assert again["status"] == "unchanged"


def test_nothing_to_add_writes_nothing(tmp_path):
    _, imported = _write_source(tmp_path)
    done = write_figma(_copy(imported.tokens), imported)
    assert done["status"] == "unchanged"
    assert done["written"] == [] and not (tmp_path / "variables-ext.js").exists()
    assert done["message"] == (f"{imported.report.source.path} already holds every token of "
                               "the system to write, so no extension was written.")


def test_an_edited_extension_needs_the_second_flag(tmp_path):
    _, imported = _write_source(tmp_path)
    write_figma(_extended(imported, Token("ink.500", "color", "#555555")), imported)
    ext = tmp_path / "variables-ext.js"
    ext.write_text(ext.read_text(encoding="utf-8") + "// mine\n", encoding="utf-8")
    ts = _extended(imported, Token("ink.600", "color", "#444444"))
    assert write_figma(ts, imported)["status"] == "refused"
    assert write_figma(ts, imported, force=True)["status"] == "refused"
    done = write_figma(ts, imported, force=True, replace_client=True)
    assert done["status"] == "written"


def test_a_source_the_record_lists_is_the_engines_and_gets_the_whole_system(tmp_path):
    path = tmp_path / "variables.json"
    text = json.dumps(as_export(_payload()), indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    from engine.existing.record import RECORD, record_text
    (tmp_path / ".uxskill").mkdir()
    (tmp_path / RECORD).write_text(record_text(tmp_path, {"variables.json": text}),
                                   encoding="utf-8")
    imported = read_figma(path)
    assert imported.owned is True
    done = write_figma(imported.tokens, imported)
    assert done["status"] == "written", done["message"]
    assert {"figma-variables.json", "figma-variables.js"} <= set(done["written"])
    assert done["load"].startswith(f"Run {tmp_path / 'figma-variables.js'} in the Figma file "
                                   "variables.json was exported from, through Figma's plugin "
                                   "API: it writes ")
    assert done["load"].endswith("updating the ones the file has in place by name, and deletes "
                                 "none.")
    payload = json.loads((tmp_path / "figma-variables.json").read_text(encoding="utf-8"))
    assert payload["mode"] == "system"
    # Once edited, the same file is no longer the engine's.
    path.write_text(text.replace('"color"', '"colour"', 1), encoding="utf-8")
    assert read_figma(path).owned is False


def test_only_a_figma_source_gets_figma_files(tmp_path):
    _, imported = _write_source(tmp_path)
    imported.report.source = Source(str(tmp_path / "tokens.json"), "dtcg", "0" * 64, 1)
    with pytest.raises(InputError) as exc:
        write_figma(imported.tokens, imported)
    assert str(exc.value).startswith(f"{tmp_path / 'tokens.json'} is a dtcg source, not a "
                                      "Figma variables export")


def _with(doc, cid, name, modes, variables):
    """`doc` with one more collection holding `variables`."""
    doc = copy.deepcopy(doc)
    doc["meta"]["variableCollections"][cid] = {
        "id": cid, "name": name, "defaultModeId": f"{cid}:0",
        "modes": [{"modeId": f"{cid}:{i}", "name": m} for i, m in enumerate(modes)],
        "variableIds": [v["id"] for v in variables]}
    doc["meta"]["variables"].update({v["id"]: v for v in variables})
    return doc


def test_an_addition_named_like_a_variable_the_import_did_not_read_is_refused(tmp_path):
    doc = copy.deepcopy(_foreign())
    # Palette ink/500 aliases a variable the export does not hold: not read.
    doc["meta"]["variables"]["v:6"] = _var("v:6", "ink/500", "c:1", "COLOR",
                                           {"1:0": {"type": "VARIABLE_ALIAS", "id": "v:gone"}},
                                           ["ALL_SCOPES"])
    doc["meta"]["variableCollections"]["c:1"]["variableIds"].append("v:6")
    _, imported = _write_source(tmp_path, doc)
    assert not imported.tokens.has("ink.500")
    assert imported.figma["declared"]["ink/500"] == ["Palette"]
    with pytest.raises(InputError) as exc:
        figma_extension(imported, _extended(imported, Token("ink.500", "color", "#555555")))
    assert str(exc.value) == (
        "ink/500 is already a variable of Palette in variables.json, which the import did not "
        "read as a token; an extension only adds variables and never changes one the file "
        "has, so give the token a name the file does not use")


def test_an_addition_named_like_a_library_variable_is_refused(tmp_path):
    doc = copy.deepcopy(_foreign())
    doc["meta"]["variableCollections"]["c:lib"] = {
        "id": "c:lib", "name": "Brand library", "defaultModeId": "l:0", "remote": True,
        "modes": [{"modeId": "l:0", "name": "Value"}], "variableIds": ["v:lib"]}
    lib = _var("v:lib", "gap/xl", "c:lib", "FLOAT", {"l:0": 32}, ["GAP"])
    lib["remote"] = True
    doc["meta"]["variables"]["v:lib"] = lib
    _, imported = _write_source(tmp_path, doc)
    with pytest.raises(InputError) as exc:
        figma_extension(imported, _extended(
            imported, Token("gap.xl", "dimension", {"value": 40, "unit": "px"})))
    assert str(exc.value).startswith("gap/xl is already a variable of Brand library in "
                                     "variables.json, which the import did not read as a token")
    # The new collection's name is kept clear of every collection the export names.
    assert imported.figma["declared_collections"] == ["Palette", "Theme", "Spacing",
                                                      "Brand library"]


def _four_mode_theme():
    """Theme with Light, Dark, High contrast and a combined High contrast
    dark, which the import does not read."""
    alias = {"type": "VARIABLE_ALIAS", "id": "v:1"}
    return _with(_foreign(), "c:4", "Look", ["Light", "Dark", "High contrast",
                                             "High contrast dark"],
                 [_var("v:9", "look/bg", "c:4", "COLOR",
                       {f"c:4:{i}": alias for i in range(4)}, ["FRAME_FILL"])])


def test_a_mode_the_import_did_not_read_takes_the_value_its_name_gives(tmp_path):
    _, imported = _write_source(tmp_path, _four_mode_theme())
    assert imported.figma["unread"] == {"Look": {"High contrast dark": "scheme:dark,contrast:high"}}
    ts = _extended(imported, Token("look.fg", "color", "#222222", modes={
        "scheme:dark": "#DDDDDD", "contrast:high": "#000000",
        "scheme:dark,contrast:high": "#FFFFFF"}))
    payload = figma_extension(imported, ts)
    fg = _variable(_collection(payload, "Look"), "look/fg")
    assert list(fg["values"]) == ["Light", "Dark", "High contrast", "High contrast dark"]
    assert fg["values"]["High contrast dark"] == {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1}
    assert fg["values"]["Dark"] == {"r": 0.866667, "g": 0.866667, "b": 0.866667, "a": 1}
    note = ("Look has the mode High contrast dark, which the import did not read; each "
            "addition there takes the system's value for scheme:dark,contrast:high, which the "
            "mode's name gives.")
    assert note in payload["notes"]
    done = write_figma(ts, imported)
    assert done["status"] == "written" and done["load"].endswith(note)


def test_a_mode_whose_name_gives_no_value_never_takes_the_default_silently(tmp_path):
    alias = {"type": "VARIABLE_ALIAS", "id": "v:1"}
    doc = _with(_foreign(), "c:4", "Look", ["Light", "Dark", "Dim"],
                [_var("v:9", "look/bg", "c:4", "COLOR", {f"c:4:{i}": alias for i in range(3)},
                      ["FRAME_FILL"])])
    _, imported = _write_source(tmp_path, doc)
    assert imported.figma["unread"] == {"Look": {"Dim": None}}
    # A token that varies by scheme cannot say what Dim holds: it goes to a
    # collection of its own, never into Look with its light value in Dim.
    varied = Token("look.fg", "color", "#222222", modes={"scheme:dark": "#DDDDDD"})
    payload = figma_extension(imported, _extended(imported, varied))
    assert [(c["name"], c["modes"]) for c in payload["collections"]] == [
        (ADDITIONS, ["light", "dark"])]
    # One value in every mode is the same in Dim, and says so.
    same = Token("look.edge", "color", "#333333")
    payload = figma_extension(imported, _extended(imported, same))
    edge = _variable(_collection(payload, "Look"), "look/edge")
    assert list(edge["values"]) == ["Light", "Dark", "Dim"]
    assert edge["values"]["Dim"] == edge["values"]["Light"]


def test_an_addition_takes_the_scopes_of_a_neighbour_on_its_own_layer(tmp_path):
    _, imported = _write_source(tmp_path)
    ts = _extended(imported, Token("fg.muted", "color", "{ink.900}", layer="semantic"),
                   Token("fg.raw", "color", "#123456"))
    payload = figma_extension(imported, ts)
    theme = _collection(payload, "Theme")
    assert _variable(theme, "fg/muted")["scopes"] == ["TEXT_FILL"]
    # No primitive sits in Theme, so the new primitive takes the engine's rule.
    assert _variable(theme, "fg/raw")["scopes"] == []


def test_a_foreign_collection_in_lowercase_axis_values_keeps_its_own_note():
    alias = {"type": "VARIABLE_ALIAS", "id": "v:1"}
    doc = _with(_foreign(), "c:4", "Look", ["light", "dark"],
                [_var("v:9", "look/bg", "c:4", "COLOR", {"c:4:0": alias, "c:4:1": alias},
                      ["FRAME_FILL"])])
    text = json.dumps(doc)
    notes = [i.message for i in import_figma(text, _source(text)).report.notes]
    assert "has the modes light and dark, read as the scheme axis: light is the base and dark " \
           "is scheme:dark" in notes
    assert not any("per word" in n for n in notes)


# ---------------------------------------------------- the scripts in a mock


_MOCK = r"""
function mock(meta) {
  const cols = []; const vars = {}; let n = 0;
  const log = {renamed: [], added: []};
  function makeVar(v) {
    const obj = {id: v.id, name: v.name, variableCollectionId: v.variableCollectionId,
      resolvedType: v.resolvedType, valuesByMode: Object.assign({}, v.valuesByMode),
      _scopes: v.scopes.slice(), description: v.description || "",
      get scopes() { return this._scopes; },
      set scopes(x) { if (x.includes("NOT_A_SCOPE")) throw new Error("invalid scope");
        this._scopes = x; },
      hiddenFromPublishing: !!v.hiddenFromPublishing, remote: false,
      setValueForMode(modeId, value) {
        const alias = value && typeof value === "object" && value.type === "VARIABLE_ALIAS";
        const ok = alias || (this.resolvedType === "FLOAT" && typeof value === "number")
          || (this.resolvedType === "STRING" && typeof value === "string")
          || (this.resolvedType === "COLOR" && typeof value === "object" && "r" in value);
        if (!ok) throw new Error("wrong value for " + this.name);
        this.valuesByMode[modeId] = value;
      }};
    vars[obj.id] = obj; return obj;
  }
  function makeCol(c) {
    const obj = {id: c.id, name: c.name, modes: c.modes.map((m) => Object.assign({}, m)),
      defaultModeId: c.defaultModeId, variableIds: c.variableIds.slice(), remote: false,
      hiddenFromPublishing: false,
      renameMode(id, name) { log.renamed.push(this.name + ":" + name);
        this.modes.find((m) => m.modeId === id).name = name; },
      addMode(name) { const id = this.id + ":m" + (++n); log.added.push(this.name + ":" + name);
        this.modes.push({modeId: id, name: name}); return id; }};
    cols.push(obj); return obj;
  }
  for (const c of Object.values(meta.variableCollections)) makeCol(c);
  for (const v of Object.values(meta.variables)) makeVar(v);
  return {log: log, figma: {variables: {
    getLocalVariableCollectionsAsync: async () => cols.slice(),
    getLocalVariablesAsync: async () => Object.values(vars),
    getVariableByIdAsync: async (id) => vars[id] || null,
    createVariableCollection(name) {
      return makeCol({id: "C" + (++n), name: name, modes: [{modeId: "M" + (++n), name: "Mode 1"}],
                      defaultModeId: "M" + n, variableIds: []}); },
    createVariable(name, col, type) {
      const v = makeVar({id: "V" + (++n), name: name, variableCollectionId: col.id,
                         resolvedType: type, valuesByMode: {}, scopes: ["ALL_SCOPES"]});
      col.variableIds.push(v.id); return v; },
    createVariableAlias(v) { return {type: "VARIABLE_ALIAS", id: v.id}; },
  }}};
}
"""


def _run(tmp_path, meta, *scripts):
    """Run each script in turn against one mock Figma file holding `meta`;
    the results in order, and the mock's log."""
    body = [_MOCK, f"const made = mock({json.dumps(meta)});", "const figma = made.figma;",
            "(async () => {", "const out = [];"]
    for script in scripts:
        body.append("out.push(await (async () => {\n" + script + "\n})());")
    body += ["console.log(JSON.stringify({out: out, log: made.log}));", "})();"]
    harness = tmp_path / "harness.js"
    harness.write_text("\n".join(body), encoding="utf-8")
    run = subprocess.run([NODE, str(harness)], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    return json.loads(run.stdout)


def test_an_export_read_back_and_exported_again_is_the_same_payload():
    # A text role's fields come back as one variable each; exporting them
    # again keeps the field scope each had, so nothing else changes.
    ts = _system()
    payload = to_figma(ts)
    back = import_figma(json.dumps(as_export(payload)), _source("x")).tokens
    again = to_figma(back)
    assert again["collections"] == payload["collections"]
    assert again["mode"] == payload["mode"]


_EMPTY = {"variableCollections": {}, "variables": {}}


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_apply_script_writes_the_system_and_a_second_run_updates_in_place(tmp_path):
    ts = _system()
    files = figma_files(ts)
    payload = json.loads(files["figma-variables.json"])
    count = sum(len(c["variables"]) for c in payload["collections"])
    got = _run(tmp_path, _EMPTY, files["figma-variables.js"], files["figma-variables.js"],
               files["figma-read-variables.js"])
    first, second, read = got["out"]
    assert (first["created"], first["updated"], first["conflicts"]) == (count, 0, [])
    assert first["aliased"] > 0
    assert (second["created"], second["updated"], second["conflicts"]) == (0, count, [])
    # Each new collection's first mode is renamed once; nothing else is.
    assert sorted(got["log"]["renamed"]) == sorted(
        f"{c['name']}:{c['modes'][0]}" for c in payload["collections"])
    back = import_figma(read, _source(read)).tokens
    assert {t.path for t in back.tokens()} == {v["name"].replace("/", ".")
                                               for c in payload["collections"]
                                               for v in c["variables"]}
    assert _compare(payload, back, ts.axes) > 1500


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_apply_script_lists_a_variable_of_another_type_and_keeps_it(tmp_path):
    files = figma_files(_system())
    meta = {"variableCollections": {"c": {
        "id": "c", "name": "color", "defaultModeId": "c:0", "variableIds": ["v"],
        "modes": [{"modeId": "c:0", "name": "light standard"}]}},
        "variables": {"v": _var("v", "color/neutral/50", "c", "FLOAT", {"c:0": 3}, ["GAP"])}}
    got = _run(tmp_path, meta, files["figma-variables.js"], files["figma-read-variables.js"])
    result, read = got["out"]
    assert "color/color/neutral/50 is a FLOAT in this file, not a COLOR; it was left as it " \
           "is, so rename one of the two" in result["conflicts"]
    # A variable aliasing the one left as it is is listed too, never pointed at it.
    assert ("color/color/surface/page aliases color/color/neutral/50 in the mode light "
            "standard, which was not written, so that mode keeps its value; fix "
            "color/color/neutral/50 and run this again") in result["conflicts"]
    doc = json.loads(read)["meta"]
    kept = doc["variables"]["v"]
    assert (kept["resolvedType"], kept["valuesByMode"]) == ("FLOAT", {"c:0": 3})
    # The existing mode keeps its name; the others are added.
    assert got["log"]["renamed"].count("color:light standard") == 0
    assert "color:dark high" in got["log"]["added"]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_an_extension_applied_adds_its_variables_and_changes_nothing_else(tmp_path):
    path, imported = _write_source(tmp_path)
    ts = _extended(imported,
                   Token("fg.muted", "color", "{ink.900}", modes={"scheme:dark": "{paper.0}"},
                         layer="semantic"),
                   Token("gap.lg", "dimension", {"value": 24, "unit": "px"}))
    assert write_figma(ts, imported)["status"] == "written"
    script = (tmp_path / "variables-ext.js").read_text(encoding="utf-8")
    meta = _foreign()["meta"]
    got = _run(tmp_path, meta, script, READ_SCRIPT)
    result, read = got["out"]
    assert (result["created"], result["updated"], result["conflicts"]) == (2, 0, [])
    assert got["log"] == {"renamed": [], "added": []}
    after = json.loads(read)["meta"]
    for vid, v in meta["variables"].items():
        assert after["variables"][vid]["valuesByMode"] == v["valuesByMode"]
        assert after["variables"][vid]["scopes"] == v["scopes"]
    back = import_figma(read, _source(read)).tokens
    assert back.get("fg.muted").value == "{ink.900}"
    assert back.get("fg.muted").modes == {"scheme:dark": "{paper.0}"}
    assert back.resolve("gap.lg") == {"value": 24, "unit": "px"}


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_an_extension_whose_collection_is_gone_lists_it_and_makes_nothing(tmp_path):
    _, imported = _write_source(tmp_path)
    write_figma(_extended(imported, Token("gap.lg", "dimension", {"value": 24, "unit": "px"})),
                imported)
    script = (tmp_path / "variables-ext.js").read_text(encoding="utf-8")
    meta = copy.deepcopy(_foreign()["meta"])
    del meta["variableCollections"]["c:3"]
    del meta["variables"]["v:5"]
    result = _run(tmp_path, meta, script)["out"][0]
    assert result["created"] == 0
    assert result["conflicts"] == [
        "Spacing is not a collection in this file, so its 1 variable was not written; export "
        "the variables of this file again and repeat the extension"]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_an_extension_never_updates_a_variable_the_file_has(tmp_path):
    _, imported = _write_source(tmp_path)
    write_figma(_extended(imported, Token("ink.500", "color", "#555555"),
                          Token("ink.600", "color", "#444444")), imported)
    script = (tmp_path / "variables-ext.js").read_text(encoding="utf-8")
    # Since the export was taken, someone added ink/500 in Figma.
    meta = _with(_foreign(), "c:x", "Other", ["Value"], [])["meta"]
    meta["variables"]["v:7"] = _var("v:7", "ink/500", "c:1", "COLOR",
                                    {"1:0": {"r": 0.5, "g": 0, "b": 0, "a": 1}}, ["TEXT_FILL"])
    meta["variableCollections"]["c:1"]["variableIds"].append("v:7")
    got = _run(tmp_path, meta, script, READ_SCRIPT)
    result, read = got["out"]
    assert (result["created"], result["updated"]) == (1, 0)
    assert result["conflicts"] == [
        "Palette/ink/500 is already in this file, and an extension only adds variables, so it "
        "was left as it is; give the token a name the file does not use and write the "
        "extension again"]
    kept = json.loads(read)["meta"]["variables"]["v:7"]
    assert kept["valuesByMode"] == {"1:0": {"r": 0.5, "g": 0, "b": 0, "a": 1}}
    assert kept["scopes"] == ["TEXT_FILL"]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_a_scope_figma_refuses_is_listed_and_the_run_goes_on(tmp_path):
    payload = {"version": 1, "mode": "system", "skipped": [], "notes": [], "collections": [
        {"name": "space", "modes": ["default"], "variables": [
            {"name": "space/odd", "type": "FLOAT", "scopes": ["NOT_A_SCOPE"], "hidden": False,
             "description": "", "values": {"default": 3}},
            {"name": "space/even", "type": "FLOAT", "scopes": ["GAP"], "hidden": False,
             "description": "", "values": {"default": 4}}]}]}
    script = "const PAYLOAD = " + json.dumps(payload) + ";\n" + APPLY_SCRIPT
    result = _run(tmp_path, _EMPTY, script)["out"][0]
    assert result["created"] == 2
    assert result["conflicts"] == [
        "space/space/odd could not take its settings (invalid scope); set its scopes in Figma"]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_a_collection_opening_with_another_mode_is_listed(tmp_path):
    files = figma_files(_system())
    meta = {"variableCollections": {"c": {
        "id": "c", "name": "radius", "defaultModeId": "c:0", "variableIds": [],
        "modes": [{"modeId": "c:0", "name": "Mode 1"}]}}, "variables": {}}
    result = _run(tmp_path, meta, files["figma-variables.js"])["out"][0]
    assert ("radius opens with the mode Mode 1, not default, and Figma reads a collection's "
            "first mode as its default; rename Mode 1 to default in Figma, or delete it once "
            "nothing uses it, and run this again") in result["conflicts"]


def test_the_package_ships_the_scripts():
    root = Path(__file__).resolve().parents[2]
    text = (root / "pyproject.toml").read_text(encoding="utf-8")
    assert '"engine.io" = ["figma/*.js"]' in text
    assert sorted(p.name for p in (root / "engine/io/figma").glob("*.js")) == [
        "apply-variables.js", "read-variables.js"]


def test_the_package_exports_the_exporter():
    from engine import io
    for name in ("to_figma", "figma_files", "figma_extension", "write_figma", "as_export",
                 "APPLY_SCRIPT", "READ_SCRIPT", "ADDITIONS"):
        assert name in io.__all__ and hasattr(io, name)
    for name in ("read_any", "write_tailwind", "REST_ENDPOINT", "SIZE_SCOPES"):
        assert name in io.__all__
