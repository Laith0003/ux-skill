"""The intake step before any write into a system someone already has: every
source is re-read and must be the file that was imported, each is copied
into a backup byte for byte, every file the write replaces is backed up by
its content, and all of it goes through the same all-or-nothing writer,
which refuses a file that differs unless forced, and a client's file
unless the second flag is given as well."""
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from engine.existing import stamp_digest
from engine.io.dtcg_in import read_dtcg
from engine.io.intake import INTAKE_DIR, source_digest, write_with_intake
from engine.io.markdown_in import read_markdown
from engine.io.report import read_source

ROOT = Path(__file__).resolve().parents[2]
ENGINE_KEY = "io.github.laith0003.ux-skill"
CLIENT_TOKENS = {"color": {"$type": "color", "ink": {"$value": "#111111"},
                           "paper": {"$value": "#ffffff"}}}


def _source(tmp_path, text=":root { --ink: #111; }\n"):
    f = tmp_path / "theme.css"
    f.write_text(text, encoding="utf-8")
    return read_source(f, "css", "--from")[0]


def _snapshot(folder):
    return {p.relative_to(folder).as_posix(): p.read_bytes()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def _digest(data):
    return hashlib.sha256(data).hexdigest()[:12]


def _record(out, sid):
    return json.loads((out / f"{INTAKE_DIR}/intake/{sid}.json").read_text(encoding="utf-8"))


def test_a_first_write_records_the_source_and_backs_it_up(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source)
    sid = source.sha256[:12]
    assert outcome["status"] == "written"
    assert outcome["written"] == [f"{INTAKE_DIR}/backup/{sid}/source/theme.css",
                                  f"{INTAKE_DIR}/intake/{sid}.json", "theme.css"]
    assert outcome["backup"] == f"{INTAKE_DIR}/backup/{sid}"
    assert outcome["replaced"] == {}
    assert outcome["message"] == (
        f"Wrote theme.css to {out}; the source is backed up in "
        f"{out / INTAKE_DIR / 'backup' / sid}.")
    assert (out / f"{INTAKE_DIR}/backup/{sid}/source/theme.css").read_text() == \
        ":root { --ink: #111; }\n"
    assert _record(out, sid) == {
        "sources": [source.to_dict()],
        "backed_up": {str(tmp_path / "theme.css"): f"{INTAKE_DIR}/backup/{sid}/source/theme.css"},
        "writes": ["theme.css"], "replaced": {}}


def test_the_same_write_again_changes_nothing(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    write_with_intake(out, {"theme.css": "new\n"}, source)
    before = _snapshot(out)
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source)
    assert outcome["status"] == "unchanged" and _snapshot(out) == before
    assert outcome["message"] == f"{out} already holds these files; nothing changed."
    assert outcome["backup"] == f"{INTAKE_DIR}/backup/{source.sha256[:12]}"


def test_files_that_are_already_there_write_no_backup(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "theme.css").write_text("new\n", encoding="utf-8")
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source)
    assert outcome["status"] == "unchanged" and outcome["backup"] == ""
    assert sorted(p.name for p in out.iterdir()) == ["theme.css"]


def test_a_later_write_from_the_same_source_adds_to_its_record(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    write_with_intake(out, {"theme.css": "new\n"}, source)
    outcome = write_with_intake(out, {"theme-ext.css": "ext\n"}, source)
    sid = source.sha256[:12]
    assert outcome["status"] == "written"
    # New files first, then the record, which the earlier one is replaced by.
    assert outcome["written"] == ["theme-ext.css", f"{INTAKE_DIR}/intake/{sid}.json"]
    assert _record(out, sid)["writes"] == ["theme.css", "theme-ext.css"]


def test_a_file_that_differs_is_refused_without_force_and_nothing_is_written(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "theme.css").write_text("theirs\n", encoding="utf-8")
    before = _snapshot(out)
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source)
    assert outcome["status"] == "refused" and outcome["conflicts"] == ["theme.css"]
    assert outcome["message"] == (
        f"Nothing was written: {out / 'theme.css'} already exists with different content. Pass "
        "--force to replace it, or pass a different --out folder.")
    assert _snapshot(out) == before


def test_the_refusal_names_the_callers_own_labels(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "theme.css").write_text("theirs\n", encoding="utf-8")
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source,
                                force_label="force: true", out_label="out")
    assert outcome["message"].endswith(
        "Pass force: true to replace it, or pass a different out folder.")


def test_with_force_the_engines_file_is_backed_up_by_its_content(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    ours = stamp_digest("ours\n")
    (out / "theme.css").write_text(ours, encoding="utf-8")
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source, force=True)
    old = _digest(ours.encode("utf-8"))
    sid = source.sha256[:12]
    where = f"{INTAKE_DIR}/backup/{old}/replaced/theme.css"
    assert outcome["status"] == "written"
    assert outcome["replaced"] == {"theme.css": where}
    assert outcome["message"] == (
        f"Wrote theme.css to {out}; the source is backed up in "
        f"{out / INTAKE_DIR / 'backup' / sid} and each replaced file under "
        f"{out / INTAKE_DIR / 'backup'}.")
    assert (out / where).read_text() == ours
    assert _record(out, sid)["replaced"] == {"theme.css": where}
    assert (out / "theme.css").read_text() == "new\n"


def test_a_source_that_changed_after_it_was_read_stops_the_write(tmp_path):
    source = _source(tmp_path)
    (tmp_path / "theme.css").write_text(":root { --ink: #222; }\n", encoding="utf-8")
    out = tmp_path / "out"
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source)
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        f"{tmp_path / 'theme.css'} changed after it was read, so nothing was written; import it "
        "again and repeat the step")
    assert not out.exists()


def test_a_source_that_is_gone_stops_the_write(tmp_path):
    source = _source(tmp_path)
    (tmp_path / "theme.css").unlink()
    out = tmp_path / "out"
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source)
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        f"{tmp_path / 'theme.css'} cannot be read again (No such file or directory), so nothing "
        "was written; put it back or import the system again, and repeat the step")
    assert not out.exists()


def test_a_folder_of_rule_files_is_digested_and_backed_up_file_by_file(tmp_path):
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "a.md").write_text("- `a`: 1px\n", encoding="utf-8")
    (rules / "b.md").write_text("- `b`: 2px\n", encoding="utf-8")
    source = read_markdown(rules).report.source
    assert source_digest(source) == source.sha256
    out = tmp_path / "out"
    outcome = write_with_intake(out, {"tokens.json": "{}\n"}, source)
    sid = source.sha256[:12]
    assert outcome["status"] == "written"
    assert (out / f"{INTAKE_DIR}/backup/{sid}/source/a.md").read_text() == "- `a`: 1px\n"
    assert (out / f"{INTAKE_DIR}/backup/{sid}/source/b.md").read_text() == "- `b`: 2px\n"
    (rules / "c.md").write_text("- `c`: 3px\n", encoding="utf-8")
    assert write_with_intake(out, {"tokens.json": "{}\n"}, source)["message"] == (
        f"{rules} changed after it was read, so nothing was written; import it again and "
        "repeat the step")


def test_files_in_a_subfolder_are_written_and_backed_up_under_the_same_path(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    (out / "art").mkdir(parents=True)
    ours = stamp_digest("<svg/>\n")
    (out / "art" / "pattern.svg").write_text(ours, encoding="utf-8")
    outcome = write_with_intake(out, {"art/pattern.svg": "<svg></svg>\n",
                                      "art/shapes.svg": "<svg/>\n"}, source, force=True)
    old = _digest(ours.encode("utf-8"))
    assert outcome["status"] == "written"
    assert (out / f"{INTAKE_DIR}/backup/{old}/replaced/art/pattern.svg").read_text() == ours
    assert (out / "art" / "shapes.svg").read_text() == "<svg/>\n"


# Every file an import read is a source: the report's own and each file in
# also_read (a dark sibling), and later several sources passed at once.
def _pair(tmp_path):
    folder = tmp_path / "src"
    folder.mkdir()
    (folder / "tokens.json").write_text(json.dumps(CLIENT_TOKENS), encoding="utf-8")
    (folder / "dark").mkdir()
    (folder / "dark" / "tokens.json").write_text(json.dumps(
        {"color": {"$type": "color", "ink": {"$value": "#ffffff"}}}), encoding="utf-8")
    return folder, read_dtcg(folder / "tokens.json").report


def _several(sources):
    lines = "".join(f"{rel}\0{s.sha256}\n" for rel, s in sources)
    return hashlib.sha256(lines.encode("utf-8")).hexdigest()[:12]


def test_every_file_the_import_read_is_backed_up_and_recorded(tmp_path):
    folder, report = _pair(tmp_path)
    assert [s.path for s in report.also_read] == [str(folder / "dark" / "tokens.json")]
    out = tmp_path / "out"
    outcome = write_with_intake(out, {"tokens.ext.css": ":root {}\n"}, report)
    sid = _several([("tokens.json", report.source), ("dark/tokens.json", report.also_read[0])])
    backup = f"{INTAKE_DIR}/backup/{sid}"
    assert outcome["status"] == "written" and outcome["backup"] == backup
    assert (out / backup / "source" / "tokens.json").read_bytes() == \
        (folder / "tokens.json").read_bytes()
    assert (out / backup / "source" / "dark" / "tokens.json").read_bytes() == \
        (folder / "dark" / "tokens.json").read_bytes()
    record = _record(out, sid)
    assert record["sources"] == [report.source.to_dict(), report.also_read[0].to_dict()]
    assert record["backed_up"] == {
        str(folder / "tokens.json"): f"{backup}/source/tokens.json",
        str(folder / "dark" / "tokens.json"): f"{backup}/source/dark/tokens.json"}


def test_a_change_to_any_file_the_import_read_stops_the_write(tmp_path):
    folder, report = _pair(tmp_path)
    (folder / "dark" / "tokens.json").write_text("{}", encoding="utf-8")
    out = tmp_path / "out"
    outcome = write_with_intake(out, {"tokens.ext.css": ":root {}\n"}, report)
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        f"{folder / 'dark' / 'tokens.json'} changed after it was read, so nothing was written; "
        "import it again and repeat the step")
    assert not out.exists()


def test_several_sources_are_taken_as_a_list(tmp_path):
    a = tmp_path / "tokens" / "tokens.json"
    a.parent.mkdir()
    a.write_text(json.dumps(CLIENT_TOKENS), encoding="utf-8")
    b = tmp_path / "app" / "globals.css"
    b.parent.mkdir()
    b.write_text(".dark { --ink: #fff; }\n", encoding="utf-8")
    sa = read_source(a, "dtcg", "--from")[0]
    sb = read_source(b, "css", "--from")[0]
    out = tmp_path / "out"
    outcome = write_with_intake(out, {"x.css": "x\n"}, [sa, sb, sa])
    sid = _several([("tokens/tokens.json", sa), ("app/globals.css", sb)])
    assert outcome["status"] == "written"
    assert sorted(p.relative_to(out / INTAKE_DIR / "backup" / sid).as_posix()
                  for p in (out / INTAKE_DIR / "backup" / sid).rglob("*") if p.is_file()) == [
        "source/app/globals.css", "source/tokens/tokens.json"]


def test_no_source_is_named(tmp_path):
    outcome = write_with_intake(tmp_path / "out", {"x.css": "x\n"}, [])
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        "sources is empty, so nothing was written; pass the import's report or every Source "
        "the files were built from")


def test_a_name_inside_the_intake_folder_is_refused(tmp_path):
    source = _source(tmp_path)
    outcome = write_with_intake(tmp_path / "out", {f"{INTAKE_DIR}/x.json": "{}\n"}, source)
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        f"files names {INTAKE_DIR}/x.json, inside {INTAKE_DIR}/, which holds the intake "
        f"backups, so nothing was written; write that file under another name")
    assert not (tmp_path / "out").exists()


# Backups keep bytes: a source in UTF-16 and a replaced file that is not
# UTF-8 both come back exactly.
def test_a_utf16_source_is_backed_up_byte_for_byte(tmp_path):
    f = tmp_path / "theme.css"
    data = ":root { --ink: #111; }\n".encode("utf-16")
    f.write_bytes(data)
    source = read_source(f, "css", "--from")[0]
    out = tmp_path / "out"
    assert write_with_intake(out, {"theme.css": "new\n"}, source)["status"] == "written"
    assert (out / f"{INTAKE_DIR}/backup/{_digest(data)}/source/theme.css").read_bytes() == data


def test_a_replaced_file_that_is_not_utf8_is_backed_up_byte_for_byte(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    old = b"/* caf\xe9 */\n"
    (out / "theme.css").write_bytes(old)
    outcome = write_with_intake(out, {"theme.css": "new\n"}, source, force=True,
                                replace_client=True)
    assert outcome["status"] == "written"
    assert (out / f"{INTAKE_DIR}/backup/{_digest(old)}/replaced/theme.css").read_bytes() == old


# --force replaces only a file that carries the engine's digest and still
# matches it. Any other file, in any folder, needs the second flag as well.
def _refusal(out, name, force="--force", replace="--replace-client-files", out_label="--out"):
    return (f"Nothing was written: {out / name} was not written by ux-skill, or changed since, "
            f"and {force} replaces only files ux-skill wrote. Pass {replace} as well as {force} "
            f"to replace it after a backup, or pass a different {out_label} folder.")


def test_force_alone_never_replaces_a_clients_file(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "tokens.json").write_text(json.dumps(CLIENT_TOKENS), encoding="utf-8")
    before = _snapshot(out)
    outcome = write_with_intake(out, {"tokens.json": "{}\n"}, source, force=True)
    assert outcome["status"] == "refused" and outcome["conflicts"] == ["tokens.json"]
    assert outcome["message"] == _refusal(out, "tokens.json")
    assert _snapshot(out) == before


def test_force_alone_never_replaces_a_hand_written_file_in_a_plain_folder(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "README.md").write_text("# mine\n", encoding="utf-8")
    before = _snapshot(out)
    outcome = write_with_intake(out, {"README.md": "# new\n"}, source, force=True)
    assert outcome["status"] == "refused" and outcome["conflicts"] == ["README.md"]
    assert outcome["message"] == _refusal(out, "README.md")
    assert _snapshot(out) == before


def test_force_alone_never_replaces_a_hand_written_rule_file_beside_the_source(tmp_path):
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "a.md").write_text("- `a`: 1px\n", encoding="utf-8")
    (rules / "ext.md").write_text("- `b`: 2px\n", encoding="utf-8")
    source = read_markdown(rules).report.source
    before = _snapshot(rules)
    outcome = write_with_intake(rules, {"ext.md": "- `c`: 3px\n"}, source, force=True)
    assert outcome["status"] == "refused" and outcome["conflicts"] == ["ext.md"]
    assert outcome["message"] == _refusal(rules, "ext.md")
    assert _snapshot(rules) == before


def test_a_file_with_the_engines_key_but_no_stamp_needs_the_second_flag(tmp_path):
    """Only the digest stamp marks a file as the engine's; a key inside the
    file does not."""
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    ours = json.dumps({"$extensions": {ENGINE_KEY: {"axes": {}}}, **CLIENT_TOKENS})
    (out / "tokens.json").write_text(ours, encoding="utf-8")
    outcome = write_with_intake(out, {"tokens.json": "{}\n"}, source, force=True)
    assert outcome["status"] == "refused" and outcome["conflicts"] == ["tokens.json"]


def test_the_second_flag_replaces_a_clients_file_after_a_backup(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    theirs = json.dumps(CLIENT_TOKENS).encode("utf-8")
    (out / "tokens.json").write_bytes(theirs)
    outcome = write_with_intake(out, {"tokens.json": "{}\n"}, source, force=True,
                                replace_client=True, replace_label="replace_client_files: true")
    assert outcome["status"] == "written"
    assert (out / f"{INTAKE_DIR}/backup/{_digest(theirs)}/replaced/tokens.json").read_bytes() \
        == theirs
    assert (out / "tokens.json").read_text() == "{}\n"


def test_the_refusal_names_the_callers_labels(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "tokens.json").write_text(json.dumps(CLIENT_TOKENS), encoding="utf-8")
    outcome = write_with_intake(out, {"tokens.json": "{}\n"}, source, force=True,
                                force_label="force: true", out_label="out",
                                replace_label="replace_client_files: true")
    assert outcome["message"] == _refusal(out, "tokens.json", "force: true",
                                          "replace_client_files: true", "out")


def test_a_file_the_engine_wrote_is_replaced_with_force_until_a_person_edits_it(tmp_path):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "tokens.json").write_text(json.dumps(CLIENT_TOKENS), encoding="utf-8")
    (out / "notes.md").write_text(stamp_digest("# notes\n"), encoding="utf-8")
    outcome = write_with_intake(out, {"notes.md": "# new\n"}, source, force=True)
    assert outcome["status"] == "written" and list(outcome["replaced"]) == ["notes.md"]
    (out / "notes.md").write_text(stamp_digest("# notes\n") + "edited\n", encoding="utf-8")
    outcome = write_with_intake(out, {"notes.md": "# newer\n"}, source, force=True)
    assert outcome["status"] == "refused" and outcome["conflicts"] == ["notes.md"]


# Every name is a plain path below the out folder and outside .uxskill/.
@pytest.mark.parametrize("name, message", [
    ("../x.css", "files names ../x.css, which is outside {out}, so nothing was written; name it "
                 "by its path below that folder, for example x.css"),
    ("/abs/x.css", "files names /abs/x.css, an absolute path, so nothing was written; name it "
                   "by its path below {out}, for example x.css"),
    ("z/../.uxskill/intake/x.json", "files names z/../.uxskill/intake/x.json, inside .uxskill/, "
                                    "which holds the intake backups, so nothing was written; "
                                    "write that file under another name"),
    (".UXSKILL/x", "files names .UXSKILL/x, inside .uxskill/, which holds the intake backups, "
                   "so nothing was written; write that file under another name"),
    ("z/../x.css", "files names z/../x.css, which is not a plain path below {out}, so nothing "
                   "was written; write it as x.css"),
])
def test_a_name_that_is_not_a_plain_path_below_the_folder_is_refused(tmp_path, name, message):
    source = _source(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    outcome = write_with_intake(out, {name: "x\n", "ok.css": "ok\n"}, source, force=True,
                                replace_client=True)
    assert outcome["status"] == "error"
    assert outcome["message"] == message.format(out=out)
    assert list(out.iterdir()) == [] and sorted(p.name for p in tmp_path.iterdir()) == [
        "out", "theme.css"]


def test_a_link_inside_the_folder_that_points_outside_is_refused(tmp_path):
    source = _source(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    out = tmp_path / "out"
    out.mkdir()
    (out / "ext").symlink_to(outside, target_is_directory=True)
    outcome = write_with_intake(out, {"ext/x.css": "x\n"}, source, force=True,
                                replace_client=True)
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        f"{out / 'ext'} is a file or a link where a folder should be, so ext/x.css cannot be "
        "written; move it away or write the system into a different folder")
    assert list(outside.iterdir()) == []


# The record and the sources.
def test_the_same_step_into_two_folders_writes_the_same_bytes(tmp_path):
    folder, report = _pair(tmp_path)
    write_with_intake(tmp_path / "one", {"a.css": "a\n"}, report)
    write_with_intake(tmp_path / "two", {"a.css": "a\n"}, report)
    assert _snapshot(tmp_path / "one") == _snapshot(tmp_path / "two")


def test_sources_with_the_same_bytes_share_a_record_that_keeps_both(tmp_path):
    a = _source(tmp_path)
    (tmp_path / "copy").mkdir()
    (tmp_path / "copy" / "theme.css").write_bytes((tmp_path / "theme.css").read_bytes())
    b = read_source(tmp_path / "copy" / "theme.css", "css", "--from")[0]
    out = tmp_path / "out"
    write_with_intake(out, {"a.css": "a\n"}, a)
    write_with_intake(out, {"b.css": "b\n"}, b)
    record = _record(out, a.sha256[:12])
    assert record["sources"] == [a.to_dict(), b.to_dict()]
    assert list(record["backed_up"]) == [a.path, b.path]
    assert record["writes"] == ["a.css", "b.css"]


def test_sources_that_share_no_folder_each_keep_their_digest(tmp_path, monkeypatch):
    import engine.io.intake as intake

    def no_common(paths):
        raise ValueError("Paths don't have the same drive")

    folder, report = _pair(tmp_path)
    monkeypatch.setattr(intake.os.path, "commonpath", no_common)
    out = tmp_path / "out"
    assert write_with_intake(out, {"a.css": "a\n"}, report)["status"] == "written"
    record = json.loads(next((out / INTAKE_DIR / "intake").iterdir()).read_text())
    light = str(folder / "tokens.json")
    assert record["backed_up"][light].endswith(
        f"/source/{_digest(os.path.abspath(light).encode('utf-8'))}/tokens.json")


def test_a_path_is_not_a_source(tmp_path):
    source = _source(tmp_path)
    outcome = write_with_intake(tmp_path / "out", {"x.css": "x\n"}, source.path)
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        f"sources is {source.path!r}, not a Source; pass the import's report, its Source, or a "
        "list of them (read_source and every importer give one)")


def test_one_path_read_twice_is_checked_both_times(tmp_path):
    first = _source(tmp_path)
    second = _source(tmp_path, ":root { --ink: #222; }\n")
    # The later read matches the file; the earlier one is still checked.
    outcome = write_with_intake(tmp_path / "out", {"x.css": "x\n"}, [second, first])
    assert outcome["status"] == "error"
    assert outcome["message"].startswith(f"{tmp_path / 'theme.css'} changed after it was read")


# The package: reading a system never loads the writer, and every name the
# package had before is still exported beside the new ones.
def test_importing_the_package_does_not_load_the_writer():
    code = ("import sys, engine.io; "
            "print('engine.foundations.emit' in sys.modules)")
    done = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT), capture_output=True,
                          text=True, check=True)
    assert done.stdout.strip() == "False"
    import engine.io.intake as intake

    tree = ast.parse(Path(intake.__file__).read_text(encoding="utf-8"))
    top = [n.module for n in tree.body if isinstance(n, ast.ImportFrom)]
    assert "engine.foundations.emit" not in top


def test_the_package_keeps_its_names_and_adds_the_intake_step():
    import engine.io

    for name in ("INTAKE_DIR", "source_digest", "write_with_intake", "read_any", "merge",
                 "write_css", "Rule", "axis_of", "Source", "read_source"):
        assert name in engine.io.__all__ and hasattr(engine.io, name), name
