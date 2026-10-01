"""The command layer the CLI and the MCP tools share: detect a source's
format, read it (one file, several read as one system, or a project
folder), and run import, enhance, extend, export and the contract check.
Each returns a small result; files are written only with an out folder,
after the intake step, through the safe writer, and a system the engine
did not write is never rewritten."""
import json

import pytest

from engine.contracts.library import SEED_DIR
from engine.existing.record import RECORD, file_digest
from engine.foundations.build import build_system
from engine.foundations.emit import InputError
from engine.foundations.export import dump_dtcg, to_css
from engine.io.commands import (
    EXIT, parse_modes, run_contracts_check, run_enhance, run_export, run_extend, run_import)
from engine.io.intake import INTAKE_DIR
from engine.io.read import CHOICES, detect_format, read_sources, read_system
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)
THEME = """:root { --ink: #1b1d22; --paper: #fdfdfb; --text-body: var(--ink); }
.dark { --text-body: var(--paper); }
"""


def _files(tmp_path):
    ts = build_system(NEUTRAL, "#3366FF").tokens
    (tmp_path / "tokens.json").write_text(dump_dtcg(ts), encoding="utf-8")
    (tmp_path / "tokens.css").write_text(to_css(ts), encoding="utf-8")
    (tmp_path / "theme.css").write_text(THEME, encoding="utf-8")
    (tmp_path / "app.css").write_text("@import 'x';\n@theme { --color-ink: #111; }\n",
                                      encoding="utf-8")
    (tmp_path / "vars.json").write_text(json.dumps({"meta": {"variables": {},
                                                             "variableCollections": {}}}),
                                        encoding="utf-8")
    (tmp_path / "tw.json").write_text(json.dumps({"colors": {"ink": "#111"}}),
                                      encoding="utf-8")
    (tmp_path / "studio.json").write_text(json.dumps(
        {"global": {"ink": {"value": "#111111", "type": "color"}}}), encoding="utf-8")
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "a.md").write_text("- `a`: 4px\n", encoding="utf-8")
    return tmp_path


# A tokens file and the app's own stylesheet holding its dark values.
TOKENS = {"color": {
    "ink": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.1, 0.1, 0.12],
                                         "hex": "#1a1a1f"}},
    "paper": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [1, 1, 0.98],
                                           "hex": "#fffffa"}},
    "text": {"body": {"$type": "color", "$value": "{color.ink}"}},
    "surface": {"page": {"$type": "color", "$value": "{color.paper}"}}}}
GLOBALS = """.dark {
  --color-text-body: var(--color-paper);
  --color-surface-page: var(--color-ink);
}
:root { --app-gap: 12px; }
"""


def _pair(tmp_path):
    (tmp_path / "tokens.json").write_text(json.dumps(TOKENS, indent=2), encoding="utf-8")
    (tmp_path / "globals.css").write_text(GLOBALS, encoding="utf-8")
    return tmp_path / "tokens.json", tmp_path / "globals.css"


def test_the_format_is_told_from_the_file(tmp_path):
    f = _files(tmp_path)
    assert [detect_format(f / n) for n in ("tokens.json", "tokens.css", "app.css", "vars.json",
                                           "tw.json", "studio.json", "rules", "rules/a.md")] == [
        "dtcg", "css", "tailwind", "figma", "tailwind-json", "dtcg", "markdown", "markdown"]
    other = tmp_path / "x.txt"
    other.write_text("a", encoding="utf-8")
    with pytest.raises(InputError) as exc:
        detect_format(other, "--from")
    assert str(exc.value) == (f"--from {other} is not a format uxskill reads by its name; pass "
                              "--format dtcg, css, tailwind, tailwind-json, markdown or figma")
    assert read_system(f / "theme.css").report.source.format == "css"
    assert CHOICES == ("auto", "dtcg", "css", "tailwind", "tailwind-json", "markdown", "figma")


def test_a_figma_mode_is_only_for_a_figma_export(tmp_path):
    f = _files(tmp_path)
    with pytest.raises(InputError) as exc:
        read_system(f / "theme.css", second_modes={"Type": "SM"})
    assert str(exc.value) == ("--figma-mode is for a Figma variables export, and --from "
                              "theme.css is read as css; drop --figma-mode")
    with pytest.raises(InputError, match="--figma-mode Type needs the form collection=mode"):
        parse_modes(["Type"])
    with pytest.raises(InputError, match="--format is scss; pass auto, dtcg"):
        read_system(f / "theme.css", "scss")


def test_a_stylesheet_read_with_a_tokens_file_adds_its_dark_values(tmp_path):
    tokens, sheet = _pair(tmp_path)
    imported = read_sources([tokens, sheet])
    body = imported.tokens.get("color.text.body")
    # The var() in the stylesheet resolves to the tokens file's own token.
    assert body.value == "{color.ink}" and body.modes == {"scheme:dark": "{color.paper}"}
    assert imported.tokens.get("color.surface.page").modes == {"scheme:dark": "{color.ink}"}
    assert imported.tokens.get("app-gap").value == {"value": 12, "unit": "px"}
    assert dict(imported.tokens.axes) == {"scheme": ("light", "dark")}
    assert [a.path for a in imported.report.also_read] == [str(sheet)]
    assert imported.owned is False
    assert imported.report.notes[-1].message == (
        "read together with tokens.json: 2 mode values added to its tokens, paired by name, "
        "and 1 token of its own")


def test_a_later_stylesheet_wins_a_base_value_as_the_browser_does(tmp_path):
    tokens, sheet = _pair(tmp_path)
    sheet.write_text(":root { --color-ink: #000000; }\n", encoding="utf-8")
    imported = read_sources([tokens, sheet])
    assert imported.tokens.get("color.ink").value == "#000000"
    assert not imported.report.not_read
    [note] = [i for i in imported.report.notes if i.where == "globals.css:1"]
    assert note.name == "--color-ink"
    assert note.message == (
        "sets the base value #000000 on :root, which wins over #1A1A1F at tokens.json:3 "
        "(:root) as the browser decides: it loads after tokens.json with a selector as "
        "specific; #000000 is read. Keep one value: remove the other at tokens.json:3 (:root), "
        "or this one if #1A1A1F is the value you mean")
    assert all("uxskill-read-together" not in i.where + i.message
               for i in imported.report.notes)


def test_a_less_specific_stylesheet_loses_and_names_both_places(tmp_path):
    tokens, sheet = _pair(tmp_path)
    sheet.write_text("html {\n  --color-ink: #000000;\n}\n" + GLOBALS, encoding="utf-8")
    imported = read_sources([tokens, sheet])
    assert imported.tokens.get("color.ink").value == "#1A1A1F"
    # Every dark value still pairs, including those pointing at color.ink.
    assert imported.tokens.get("color.surface.page").modes == {"scheme:dark": "{color.ink}"}
    assert imported.tokens.get("color.text.body").modes == {"scheme:dark": "{color.paper}"}
    [kept] = imported.report.not_read
    assert (kept.where, kept.name) == ("globals.css:2", "--color-ink")
    assert kept.message == (
        "sets the base value #000000 on html, which loses to #1A1A1F at tokens.json:3 (:root) "
        "as the browser decides: that is more specific, so #1A1A1F is kept and globals.css's "
        "other values still pair with it. Remove it from globals.css, or change it at "
        "tokens.json:3 (:root) if #000000 is the value you mean")


def test_a_doubled_root_in_the_globals_wins_and_keeps_the_dark_values(tmp_path):
    tokens, sheet = _pair(tmp_path)
    sheet.write_text(GLOBALS + "html:root {\n  --color-ink: #000000;\n}\n"
                     ':root:root[data-theme="dark"] {\n  --color-paper: #101010;\n}\n',
                     encoding="utf-8")
    imported = read_sources([tokens, sheet])
    assert imported.tokens.get("color.ink").value == "#000000"
    assert imported.tokens.get("color.paper").modes == {"scheme:dark": "#101010"}
    assert imported.tokens.get("color.surface.page").modes == {"scheme:dark": "{color.ink}"}
    [note] = [i for i in imported.report.notes if i.name == "--color-ink"]
    assert "html:root is more specific than :root" in note.message
    assert note.where == "globals.css:7"


def test_of_two_stylesheets_the_later_wins_and_the_first_is_named(tmp_path):
    tokens, sheet = _pair(tmp_path)
    sheet.write_text(":root { --app-edge: #DDDDDD; }\n", encoding="utf-8")
    second = tmp_path / "site.css"
    second.write_text(":root {\n  --app-edge: #CCCCCC;\n}\n", encoding="utf-8")
    imported = read_sources([tokens, sheet, second])
    assert imported.tokens.get("app-edge").value == "#CCCCCC"
    assert not imported.report.not_read
    [note] = [i for i in imported.report.notes if i.name == "--app-edge"]
    assert note.where == "site.css:2"
    assert "wins over #DDDDDD at globals.css:1 (:root)" in note.message


def test_places_in_messages_name_the_real_file_and_line(tmp_path):
    tokens, sheet = _pair(tmp_path)
    sheet.write_text(".dark {\n  --color-ink: #000;\n}\n.dark {\n  --color-ink: #111;\n}\n",
                     encoding="utf-8")
    imported = read_sources([tokens, sheet])
    text = " ".join(i.where + " " + i.message for i in imported.report.not_read)
    assert "line 2 of globals.css" in text and "line 5 of globals.css" in text
    assert "uxskill-read-together" not in text


def test_a_second_source_must_be_a_stylesheet_given_once(tmp_path):
    tokens, sheet = _pair(tmp_path)
    with pytest.raises(InputError) as exc:
        read_sources([sheet, tokens])
    assert str(exc.value) == ("--from tokens.json is read as dtcg; a second --from adds a "
                              "stylesheet's values (its dark scheme, say) to the first, so pass "
                              "the system first and each stylesheet after it")
    with pytest.raises(InputError, match="is given twice; pass each file once"):
        read_sources([tokens, tokens])


def test_a_project_folder_is_read_as_the_set_system_detect_finds(tmp_path):
    tokens, sheet = _pair(tmp_path)
    assert detect_format(tmp_path) == "project"
    imported = read_sources(tmp_path)
    assert imported.report.source.path == str(tokens)
    assert [a.path for a in imported.report.also_read] == [str(sheet)]
    assert imported.tokens.get("color.text.body").modes == {"scheme:dark": "{color.paper}"}


def test_a_project_folder_leaves_out_what_ux_skill_keeps_or_wrote_there(tmp_path):
    sheet = tmp_path / "theme.css"
    sheet.write_text(THEME, encoding="utf-8")
    assert run_extend(sheet, add=["radius"], out=tmp_path)["status"] == "written"
    run_export(sheet, to="css", out=tmp_path / "exp")
    # The owner changes the source; the backup under .uxskill and the
    # extension ux-skill wrote are not read as the system.
    sheet.write_text(THEME.replace("#1b1d22", "#202020"), encoding="utf-8")
    imported = read_sources(tmp_path)
    assert imported.report.source.path == str(sheet) and imported.report.also_read == []
    assert imported.report.not_read == []
    assert imported.tokens.get("ink").value == "#202020"


def test_every_source_is_checked_and_backed_up_before_a_write(tmp_path):
    tokens, sheet = _pair(tmp_path)
    out = tmp_path / "out"
    done = run_import([tokens, sheet], out=out)
    assert done["status"] == "written"
    backups = sorted(p.name for p in (out / INTAKE_DIR / "backup").rglob("*") if p.is_file())
    assert backups == ["globals.css", "tokens.json"]


def test_a_changed_second_source_stops_the_write(tmp_path):
    from engine.io.intake import write_with_intake
    tokens, sheet = _pair(tmp_path)
    imported = read_sources([tokens, sheet])
    sheet.write_text(GLOBALS + ":root { --app-more: 4px; }\n", encoding="utf-8")
    outcome = write_with_intake(tmp_path / "out", {"a.md": "x\n"}, imported.report)
    assert outcome["status"] == "error"
    assert outcome["message"] == (f"{sheet} changed after it was read, so nothing was written; "
                                  "import it again and repeat the step")


def test_import_reports_and_proposes_a_mapping_and_writes_only_with_out(tmp_path):
    f = _files(tmp_path)
    result = run_import(f / "tokens.json")
    assert result["status"] == "read" and result["format"] == "dtcg"
    assert result["not_read"] == [] and result["mapping"]["roles"] > 100
    assert result["report"].startswith("# Import report")
    assert result["owned_by"] == "extension key"
    out = tmp_path / "out"
    written = run_import(f / "theme.css", out=out)
    assert written["status"] == "written" and written["mapping_kept"] is False
    assert (out / "import-report.md").is_file() and (out / "mapping.json").is_file()
    assert (out / INTAKE_DIR / "backup").is_dir()


def test_an_owners_mapping_is_kept_and_merged_in_memory(tmp_path):
    f = _files(tmp_path)
    out = tmp_path / "out"
    run_import(f / "theme.css", out=out)
    owner = '{"version": 1, "roles": {}, "axes": {}}\n'
    (out / "mapping.json").write_text(owner, encoding="utf-8")
    again = run_import(f / "theme.css", out=out)
    assert again["status"] in ("written", "unchanged") and again["mapping_kept"] is True
    assert (out / "mapping.json").read_text() == owner
    assert again["mapping_notes"] and "was kept as it is" in again["message"]
    # Forced, it is still the owner's file, so it stays.
    forced = run_import(f / "theme.css", out=out, force=True)
    assert forced["mapping_kept"] is True and (out / "mapping.json").read_text() == owner


def test_the_report_says_which_marker_decided_ownership(tmp_path):
    f = _files(tmp_path)
    assert "extension key" in run_import(f / "tokens.json")["report"]
    built = tmp_path / "built"
    built.mkdir()
    ts = build_system(NEUTRAL, "#3366FF").tokens
    text = dump_dtcg(ts)
    (built / "tokens.json").write_text(text, encoding="utf-8")
    (built / ".uxskill").mkdir()
    (built / RECORD).write_text(json.dumps({"files": {"tokens.json": file_digest(text)}}),
                                encoding="utf-8")
    recorded = run_import(built / "tokens.json")
    assert recorded["owned_by"] == "record"
    assert recorded["ownership"].startswith("tokens.json is ux-skill's own: the record")
    from engine.existing import stamp_digest
    (built / "own.css").write_text(stamp_digest(to_css(ts), css=True), encoding="utf-8")
    assert run_import(built / "own.css")["owned_by"] == "stamp"
    theirs = run_import(f / "theme.css")
    assert theirs["owned_by"] == ""
    assert theirs["ownership"].startswith("theme.css is not ux-skill's own")


def test_a_long_not_read_list_is_folded_by_namespace(tmp_path):
    sheet = tmp_path / "long.css"
    sheet.write_text(":root { --ok: 4px; }\n" + "".join(
        f".dark {{ --shade-{i}: #000; }}\n" for i in range(15)), encoding="utf-8")
    result = run_import(sheet)
    assert len(result["not_read"]) == 1 and result["not_read"][0]["count"] == 15
    assert result["not_read_count"] == 15
    assert "15 entries under shade (--shade-0, --shade-1, --shade-2 and 12 more)" \
        in result["report"]


def test_enhance_reports_without_writing_and_scans_what_it_is_given(tmp_path):
    f = _files(tmp_path)
    code = tmp_path / "code"
    code.mkdir()
    (code / "a.css").write_text(".x { color: var(--text-body); padding: 13px; }\n",
                                encoding="utf-8")
    (code / "a.html").write_text('<div class="p-13 text-body"></div>\n', encoding="utf-8")
    result = run_enhance(f / "theme.css", scan=[code])
    assert result["status"] == "reported"
    summary = result["summary"]
    assert summary["unused"] == 0 and summary["raw_values"] == 1
    assert set(summary) >= {"gate_measured", "gate_passed", "mapped", "of", "unknown_classes"}
    assert "## What the code uses" in result["report"]
    assert not (tmp_path / "enhance-report.md").exists()


OWNER = {"version": 1, "axes": {}, "roles": {
    "color.text.default": {"token": "ink", "by": "owner"},
    "color.surface.page": {"token": "paper", "by": "owner"}}}


def test_enhance_merges_an_owners_mapping(tmp_path):
    f = _files(tmp_path)
    mapping = tmp_path / "given.json"
    mapping.write_text(json.dumps(OWNER), encoding="utf-8")
    result = run_enhance(f / "theme.css", mapping=mapping, out=tmp_path / "enh")
    assert result["summary"]["mapped"] == 2 and result["mapping_file"] == str(mapping)
    # The owner's token is the one read, not the proposal's text-body.
    doc = json.loads((tmp_path / "enh" / "enhance.json").read_text())
    assert doc["mapping"]["roles"]["color.text.default"] == "ink"
    assert "color.text.default (your ink)" in result["report"]


def test_the_mapping_in_out_is_read_when_none_is_given(tmp_path):
    f = _files(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "mapping.json").write_text(json.dumps(OWNER), encoding="utf-8")
    proposed = run_enhance(f / "theme.css")
    used = run_enhance(f / "theme.css", out=out)
    assert proposed["summary"]["mapped"] == 1 and proposed["mapping_file"] == ""
    assert used["summary"]["mapped"] == 2 and used["mapping_file"] == str(out / "mapping.json")
    assert used["mapping_notes"][0].startswith(f"Read through {out / 'mapping.json'}")
    extended = run_extend(f / "theme.css", add=["radius"], out=out)
    assert extended["mapping_file"] == str(out / "mapping.json")
    # Beside the source, for the contract check, which has no out folder.
    (f / "mapping.json").write_text(json.dumps(OWNER), encoding="utf-8")
    checked = run_contracts_check(SEED_DIR, f / "theme.css")
    assert checked["mapping_file"] == str(f / "mapping.json")


def test_extend_writes_beside_a_foreign_source_and_blocks_with_a_report(tmp_path):
    f = _files(tmp_path)
    out = tmp_path / "out"
    result = run_extend(f / "theme.css", add=["space"], out=out)
    assert result["status"] == "written" and result["added"] > 0
    # The source is never rewritten; the additions sit beside it.
    assert (f / "theme.css").read_text() == THEME
    assert (f / "theme-ext.css").is_file()
    assert "Load theme-ext.css after theme.css" in result["load"]
    assert (out / "mapping.json").is_file() and (out / "extend-report.md").is_file()
    blocked = run_extend(f / "theme.css", out=tmp_path / "b",
                         add_role=["color.surface.page=ink"])
    assert blocked["status"] == "blocked" and blocked["problems"]
    assert sorted(p.name for p in (tmp_path / "b").iterdir()) == [
        ".uxskill", "extend-report.md"]
    with pytest.raises(InputError, match="--add-role ink needs the form role=token"):
        run_extend(f / "theme.css", add_role=["ink"], out=out)
    # With no mapping file, the fix says how to get one.
    with pytest.raises(InputError, match=r"edit mapping.json \(run system import with --out "
                                         r"to write one, and pass it as --mapping\)"):
        run_extend(f / "theme.css", add_role=["color.text.default=paper"], out=tmp_path / "m")


def test_extend_keeps_an_owners_mapping_in_out_instead_of_refusing(tmp_path):
    f = _files(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    owner = '{"version": 1, "roles": {}, "axes": {}}\n'
    (out / "mapping.json").write_text(owner, encoding="utf-8")
    result = run_extend(f / "theme.css", add=["radius"], out=out)
    assert result["status"] == "written" and result["mapping_kept"] is True
    assert (out / "mapping.json").read_text() == owner
    assert (out / "extend-report.md").is_file()


def test_a_second_extend_into_another_out_folder_adds_to_the_first(tmp_path):
    from pathlib import Path
    f = _files(tmp_path)
    first = run_extend(f / "theme.css", add=["space"], out=tmp_path / "one")
    assert first["status"] == "written"
    ext = (f / "theme-ext.css").read_text()
    second = run_extend(f / "theme.css", add=["radius"], out=tmp_path / "two")
    assert second["status"] == "written", second["message"]
    after = (f / "theme-ext.css").read_text()
    # What the first extension added is kept, and the new additions follow.
    assert "--space-" in after and "--radius-" in after
    assert (f / "theme.css").read_text() == THEME
    # The earlier extension is backed up before it is written again.
    backup = Path(second["replaced"][str(f / "theme-ext.css")])
    assert backup.read_text() == ext
    # Each folder keeps its own intake record of what was written there.
    for out in (tmp_path / "one", tmp_path / "two"):
        [record] = (out / INTAKE_DIR / "intake").glob("*.json")
        assert json.loads(record.read_text())["writes"] == ["mapping.json", "extend-report.md"]
    [beside] = (f / INTAKE_DIR / "intake").glob("*.json")
    assert json.loads(beside.read_text())["writes"] == ["theme-ext.css"]
    assert second["where"]["out"]["folder"] == str(tmp_path / "two")
    # An extension the owner edited is theirs: it is not written over.
    (f / "theme-ext.css").write_text(after + "/* mine */\n", encoding="utf-8")
    third = run_extend(f / "theme.css", add=["border"], out=tmp_path / "three")
    assert third["status"] == "refused"
    assert "theme-ext.css" in third["message"] and "--force" in third["message"]


def test_a_file_in_the_way_beside_the_source_is_named_with_the_right_fix(tmp_path):
    f = _files(tmp_path)
    (f / "theme-ext.css").write_text("/* mine */\n", encoding="utf-8")
    result = run_extend(f / "theme.css", add=["radius"], out=tmp_path / "out")
    assert result["status"] == "refused"
    assert "sits beside theme.css, where the extension has to load from, so --out does not " \
           "move it" in result["message"]
    assert "pass a different --out folder" not in result["message"]


def test_the_engines_own_system_is_rewritten_with_force_and_its_outputs_follow(tmp_path):
    from engine.existing.record import record_text
    ds = tmp_path / "ds"
    ds.mkdir()
    ts = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    files = {"tokens.json": dump_dtcg(ts), "tokens.css": to_css(ts)}
    for name, text in files.items():
        (ds / name).write_text(text, encoding="utf-8")
    (ds / ".uxskill").mkdir()
    (ds / RECORD).write_text(record_text(ds, files), encoding="utf-8")
    refused = run_extend(ds / "tokens.json", add=["radius"], out=ds)
    assert refused["status"] == "refused"
    assert "tokens.json is the system ux-skill wrote" in refused["message"]
    assert "pass --force to rewrite" in refused["message"]
    assert "rename" not in refused["message"] and "sits beside" not in refused["message"]
    done = run_extend(ds / "tokens.json", add=["radius"], out=ds, force=True)
    assert done["status"] == "written"
    doc = json.loads((ds / "tokens.json").read_text())
    css = (ds / "tokens.css").read_text()
    # tokens.css is built again from the extended tokens.json.
    assert css == to_css(read_system(ds / "tokens.json").tokens)
    assert "radius" in doc


def _own_system_with_report(ds, art_axes=NEUTRAL):
    """The engine's own system, built with color only, beside the report
    and art a build writes: the report says it was built from #3366FF at
    every axis 0.5, and the art was drawn at `art_axes`."""
    from engine.existing.record import record_text
    from engine.foundations.art import art_files
    from engine.foundations.emit import make_system
    ds.mkdir()
    ts = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    built = make_system("#3366FF", NEUTRAL, "every axis at 0.5", arabic=False)
    files = {"tokens.json": dump_dtcg(ts), "tokens.css": to_css(ts),
             "system-report.md": built.files["system-report.md"],
             **art_files(ts, art_axes, "#3366FF")}
    for name, text in files.items():
        (ds / name).parent.mkdir(parents=True, exist_ok=True)
        (ds / name).write_text(text, encoding="utf-8")
    (ds / ".uxskill").mkdir()
    (ds / RECORD).write_text(record_text(ds, files), encoding="utf-8")
    return built.files["system-report.md"]


def test_an_in_place_extend_rebuilds_the_report_and_the_art(tmp_path):
    from engine.existing.record import engine_wrote
    from engine.foundations.art import FILES, art_files
    ds = tmp_path / "ds"
    # Art drawn at other axes than the report records: the rebuild follows
    # the report, the record of what the system was built from.
    old = _own_system_with_report(ds, art_axes=AxisValues(*[0.9] * 7))
    done = run_extend(ds / "tokens.json", add=["radius"], out=ds, force=True)
    assert done["status"] == "written", done["message"]
    ts = read_system(ds / "tokens.json").tokens
    assert ts.has("radius.card")
    for name, text in art_files(ts, NEUTRAL, "#3366FF").items():
        assert (ds / name).read_text() == text
    assert set(FILES) <= set(done["written"])
    report = (ds / "system-report.md").read_text()
    # What it was built from stays; what extend added is said, with where
    # to read why.
    built_from = report.split("## Built from")[1].split("## WCAG gate")[0]
    assert built_from == old.split("## Built from")[1].split("## WCAG gate")[0]
    # The opening says what the system holds now and that it was extended.
    opening = report.split("\n\n")[1]
    assert opening.startswith("A design system for #3366FF, built by ux-skill and extended in "
                              "place since: color and radius,")
    assert "complete" not in opening
    assert "## Extended in place" in report
    added = report.split("## Extended in place")[1].split("## Files")[0]
    assert f"- Added {done['added']} tokens: radius." in added
    assert "radius.chip" in added and "extend-report.md" in added
    assert report.endswith(old[old.index("## Files"):])
    # Each rebuilt file is the engine's, so a later force can replace it.
    assert all(engine_wrote(ds, n) for n in ("system-report.md", *FILES))
    assert "system-report.md" in done["message"] or "system-report.md" in done["written"]


def test_the_rebuilt_report_says_the_brand_color_from_the_tokens(tmp_path):
    from engine.existing.record import record_text
    from engine.foundations.emit import _FIDELITY_LEAD
    ds = tmp_path / "ds"
    old = _own_system_with_report(ds)
    # A report written before the system had its brand color section.
    start = old.index("## Brand color")
    cut = old[:start] + old[old.index("## Notes"):]
    (ds / "system-report.md").write_text(cut, encoding="utf-8")
    (ds / RECORD).write_text(record_text(ds, {"system-report.md": cut}), encoding="utf-8")
    done = run_extend(ds / "tokens.json", add=["radius"], out=ds, force=True)
    assert done["status"] == "written", done["message"]
    report = (ds / "system-report.md").read_text()
    section = report.split("## Brand color")[1].split("## Notes")[0]
    assert _FIDELITY_LEAD in section and "- Light mode: the button is" in section
    assert report.index("## Brand color") < report.index("## Notes")


def test_added_imagery_says_no_art_was_written_unless_art_is_drawn(tmp_path):
    from engine.foundations.art import FILES
    ds = tmp_path / "ds"
    _own_system_with_report(ds)
    for name in FILES:   # a build whose art the owner removed
        (ds / name).unlink()
    done = run_extend(ds / "tokens.json", add=["imagery"], out=ds, force=True)
    assert done["status"] == "written", done["message"]
    assert "No art was written" in done["report"]
    assert not any((ds / n).exists() for n in FILES)
    # With the art beside it, the art is drawn again and the line is not said.
    drawn = tmp_path / "drawn"
    _own_system_with_report(drawn)
    done = run_extend(drawn / "tokens.json", add=["imagery"], out=drawn, force=True)
    assert done["status"] == "written", done["message"]
    assert "No art was written" not in done["report"]


def test_an_engine_stylesheet_extended_in_place_says_no_art_was_written(tmp_path):
    from engine.existing import stamp_digest
    ds = tmp_path / "ds"
    _own_system_with_report(ds)
    ts = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    (ds / "theme.css").write_text(stamp_digest(to_css(ts), css=True), encoding="utf-8")
    done = run_extend(ds / "theme.css", add=["imagery"], out=ds, force=True)
    assert done["status"] == "written", done["message"]
    assert "No art was written" in done["report"]


def test_a_report_the_owner_edited_is_left_with_the_art(tmp_path):
    from engine.foundations.art import FILES
    ds = tmp_path / "ds"
    _own_system_with_report(ds, art_axes=AxisValues(*[0.9] * 7))
    edited = (ds / "system-report.md").read_text() + "\nOur notes.\n"
    (ds / "system-report.md").write_text(edited, encoding="utf-8")
    art = {n: (ds / n).read_text() for n in FILES}
    done = run_extend(ds / "tokens.json", add=["radius"], out=ds, force=True)
    assert done["status"] == "written", done["message"]
    assert (ds / "system-report.md").read_text() == edited
    assert {n: (ds / n).read_text() for n in FILES} == art
    assert "system-report.md" in done["report"] and "uxskill system build" in done["report"]


def test_a_foreign_radius_token_does_not_block_added_radius(tmp_path):
    sheet = tmp_path / "theme.css"
    sheet.write_text(":root { --ink: #1b1d22; --paper: #fdfdfb; --radius: 8px; }\n",
                     encoding="utf-8")
    result = run_extend(sheet, add=["radius"], out=tmp_path / "out")
    assert result["status"] == "written", result["problems"][:2]


def test_a_format_that_cannot_read_the_file_names_the_flag(tmp_path):
    f = _files(tmp_path)
    with pytest.raises(InputError) as exc:
        run_import(f / "theme.css", fmt="dtcg")
    assert str(exc.value) == ("--format dtcg reads JSON and theme.css is a stylesheet; pass "
                              "--format css or tailwind, or leave --format out")


def test_extend_reads_the_briefs_fields_as_a_build_does(tmp_path):
    f = _files(tmp_path)
    brief = {"tone": ["calm"], "age": "older-adults", "region": "Levant",
             "headline": "Care that comes to you"}
    result = run_extend(f / "theme.css", add=["type"], brief=brief, out=tmp_path / "out")
    assert result["status"] == "written"
    assert result["unread"] == [
        'region "Levant" is not read by the system build. Say what it means for the system '
        'with languages (tags such as ["ar-JO", "en"]) and primary_script ("latin" or '
        '"arabic").']
    assert (f / "fonts.css").is_file()
    assert "Body text is 18px" in result["report"]
    # The headline's longest word, five letters, sizes the added display.
    assert "--type-fit-word-latin: 5;" in (f / "theme-ext.css").read_text()
    with pytest.raises(InputError) as exc:
        run_extend(f / "theme.css", add=["type"], brief={"primary_script": "arabic"},
                   latin_only=True, out=tmp_path / "x")
    assert str(exc.value) == ("--latin-only leaves Arabic out, but the brief's primary_script "
                              "is arabic; drop --latin-only, or set primary_script to latin")
    with pytest.raises(InputError, match="--brief field headline is 5; give the page's"):
        run_extend(f / "theme.css", add=["type"], brief={"tone": ["calm"], "headline": 5},
                   out=tmp_path / "y")


def test_export_gives_sizes_without_out_and_writes_with_it(tmp_path):
    f = _files(tmp_path)
    result = run_export(f / "tokens.json", to="tailwind")
    assert result["status"] == "built" and [x["name"] for x in result["files"]] == [
        "tailwind-theme.css"]
    assert "texts" not in result
    assert run_export(f / "tokens.json", to="css", include_files=True)["texts"]["tokens.css"] \
        == (f / "tokens.css").read_text()
    out = tmp_path / "out"
    figma = run_export(f / "tokens.json", to="figma", out=out)
    assert figma["status"] == "written"
    assert (out / "figma-variables.js").is_file()
    with pytest.raises(InputError, match="--to is scss; pass css, tailwind, figma or dtcg"):
        run_export(f / "tokens.json", to="scss")


def test_the_export_of_a_foreign_system_carries_what_was_not_read(tmp_path):
    sheet = tmp_path / "theme.css"
    sheet.write_text(THEME + ".dark { --only-dark: #000; }\n", encoding="utf-8")
    css = run_export(sheet, to="css", include_files=True)["texts"]["tokens.css"]
    assert css.startswith("/*\n * Written by ux-skill from theme.css, which it did not write")
    assert "theme.css:3 --only-dark: is set only under .dark" in css
    tw = run_export(sheet, to="tailwind", include_files=True)["texts"]["tailwind-theme.css"]
    assert tw.startswith("/*\n * Written by ux-skill from theme.css") and "--only-dark" in tw
    dtcg = run_export(sheet, to="dtcg")
    assert dtcg["not_read"] == 1 and "run system import on it" in dtcg["note"]


def test_export_opens_in_the_scheme_asked_and_a_stylesheet_keeps_its_own(tmp_path):
    f = _files(tmp_path)
    ts = build_system(NEUTRAL, "#3366FF").tokens
    dark = run_export(f / "tokens.json", to="css", scheme="dark", include_files=True)
    assert dark["texts"]["tokens.css"] == to_css(ts, scheme="dark")
    (f / "dark.css").write_text(to_css(ts, scheme="dark"), encoding="utf-8")
    kept = run_export(f / "dark.css", to="tailwind", include_files=True)
    assert '\n:root:not([data-theme="light"]) {\n' in kept["texts"]["tailwind-theme.css"]
    with pytest.raises(InputError, match="--scheme is dim; pass light, dark or system"):
        run_export(f / "tokens.json", to="css", scheme="dim")


def test_the_contract_check_passes_the_seeds_on_any_format(tmp_path):
    f = _files(tmp_path)
    result = run_contracts_check(SEED_DIR, f / "tokens.json")
    assert result["status"] == "passed" and len(result["contracts"]) == 23
    assert result["problems"] == []
    # A stylesheet is read through a mapping proposed from its names.
    css = run_contracts_check(SEED_DIR, f / "tokens.css")
    assert css["status"] == "passed" and "proposed from names" in css["notes"][0]


def test_every_status_has_an_exit_code():
    assert EXIT == {"read": 0, "reported": 0, "built": 0, "passed": 0, "written": 0,
                    "unchanged": 0, "blocked": 1, "failed": 1, "refused": 1, "error": 1}


def test_every_place_holding_the_losing_value_is_named(tmp_path):
    # A token file, a stylesheet that mirrors it, and an html:root override
    # in a third file: the browser overrides the mirror, so both are named.
    tokens, sheet = _pair(tmp_path)
    sheet.write_text(":root {\n  --color-ink: #1a1a1f;\n}\n", encoding="utf-8")
    site = tmp_path / "site.css"
    site.write_text("html:root {\n  --color-ink: #000000;\n}\n", encoding="utf-8")
    imported = read_sources([tokens, sheet, site])
    assert imported.tokens.get("color.ink").value == "#000000"
    [note] = [i for i in imported.report.notes if i.name == "--color-ink"]
    assert note.where == "site.css:2"
    assert ("wins over #1A1A1F at globals.css:2 (:root) and tokens.json:3 (:root) as the "
            "browser decides: html:root is more specific than :root") in note.message
    assert "remove the other at globals.css:2 (:root) and tokens.json:3 (:root)" in note.message
    assert not imported.report.not_read
