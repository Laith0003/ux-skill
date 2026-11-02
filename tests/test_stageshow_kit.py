"""The Stageshow kit, carried in engine/kits/stageshow under its MIT licence,
and `uxskill kit stageshow`, which drops it into a project with the system's
look beside it.

The copy leaves out the brand registry and BrandMark (other companies'
marks under their own terms) and writes its few non-ASCII glyphs as
escapes; UPSTREAM.md records the commit and both changes. TypeScript is not
compiled here, so every relative import is checked to resolve instead."""
import re
from pathlib import Path

import pytest

from engine.foundations.build import build_system
from engine.foundations.errors import InputError
from engine.foundations.export import dump_dtcg
from engine.io.stageshow_kit import KIT, kit_files, run_kit
from engine.synthesizer.axes import AxisValues

ROOT = Path(__file__).resolve().parents[1]
NEUTRAL = AxisValues(*[0.5] * 7)
_IMPORT = re.compile(r"""(?:from\s+|import\s+)['"](\.{1,2}/[^'"]+)['"]""")
_CSS_IMPORT = re.compile(r"""@import\s+['"](\.{1,2}/[^'"]+)['"]""")


def _tokens(tmp_path):
    src = tmp_path / "tokens.json"
    src.write_text(dump_dtcg(build_system(NEUTRAL, "#3366FF").tokens), encoding="utf-8")
    return src


def test_the_kit_carries_its_licence_and_where_it_came_from():
    licence = (KIT / "LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in licence and "Benji Taylor" in licence
    upstream = (KIT / "UPSTREAM.md").read_text(encoding="utf-8")
    assert re.search(r"\b[0-9a-f]{40}\b", upstream), "UPSTREAM.md names the commit copied"
    assert "github.com/benjitaylor/skills" in upstream


def test_no_other_companys_marks_come_with_it():
    assert not (KIT / "brands").exists()
    assert not list(KIT.rglob("BrandMark*"))
    for path in KIT.rglob("*"):
        if path.suffix in (".ts", ".tsx", ".css"):
            text = path.read_text(encoding="utf-8")
            assert "brands" not in _IMPORT.findall(text) and "BrandMark" not in text, path


def test_every_kit_file_is_ascii():
    for path in KIT.rglob("*"):
        if path.is_file():
            data = path.read_bytes()
            assert data.isascii(), f"{path.relative_to(ROOT)} holds a non-ASCII byte; write it as an escape"


def _resolves(base: Path, spec: str) -> bool:
    target = (base.parent / spec).resolve()
    candidates = [target, *(target.with_name(target.name + ext) for ext in (".ts", ".tsx", ".css")),
                  target / "index.ts", target / "index.tsx"]
    return any(c.is_file() for c in candidates)


def test_every_relative_import_in_the_kit_resolves():
    missing = []
    for path in KIT.rglob("*"):
        if path.suffix in (".ts", ".tsx"):
            specs = _IMPORT.findall(path.read_text(encoding="utf-8"))
        elif path.suffix == ".css":
            specs = _CSS_IMPORT.findall(path.read_text(encoding="utf-8"))
        else:
            continue
        missing += [f"{path.relative_to(KIT)} -> {s}" for s in specs if not _resolves(path, s)]
    assert not missing, f"imports that name no file in the kit: {missing}"


def test_the_kit_writes_into_a_project_with_the_look(tmp_path):
    out = tmp_path / "src" / "stageshow"
    result = run_kit(out, source=_tokens(tmp_path))
    assert result["status"] == "written"
    assert (out / "index.ts").is_file() and (out / "stageshow.css").is_file()
    assert (out / "LICENSE").is_file() and (out / "UPSTREAM.md").is_file()
    assert ".ux-look .ss-stage {" in (out / "stageshow-look.css").read_text(encoding="utf-8")
    assert set(result["written"]) == set(kit_files()) | {"stageshow-look.css"}


def test_without_a_system_it_writes_the_kit_alone(tmp_path):
    result = run_kit(tmp_path / "kit")
    assert result["status"] == "written" and "stageshow-look.css" not in result["written"]


def test_a_changed_file_is_never_replaced_without_force(tmp_path):
    out = tmp_path / "kit"
    run_kit(out)
    (out / "index.ts").write_text("// my own edit\n", encoding="utf-8")
    refused = run_kit(out)
    assert refused["status"] == "refused" and refused["conflicts"] == ["index.ts"]
    assert refused["message"].startswith("Nothing was written: ") and "--force" in refused["message"]
    assert str(out / "index.ts") in refused["message"]
    assert (out / "index.ts").read_text(encoding="utf-8") == "// my own edit\n"


def test_force_replaces_a_changed_file_after_backing_it_up(tmp_path):
    out = tmp_path / "kit"
    run_kit(out)
    (out / "index.ts").write_text("// my own edit\n", encoding="utf-8")
    result = run_kit(out, force=True)
    assert result["status"] == "written"
    backup = out / result["backup"] / "index.ts"
    assert backup.read_text(encoding="utf-8") == "// my own edit\n"
    assert (out / "index.ts").read_text(encoding="utf-8") == kit_files()["index.ts"]


def test_the_wheel_carries_the_kit():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"kits/stageshow/**/*.tsx"' in text and '"kits/stageshow/LICENSE"' in text


def test_the_command_is_on_the_cli(tmp_path):
    from click.testing import CliRunner

    from engine.cli.main import cli
    out = tmp_path / "kit"
    run = CliRunner().invoke(cli, ["--no-pretty", "kit", "stageshow", "--out", str(out),
                                   "--from", str(_tokens(tmp_path))])
    assert run.exit_code == 0, run.output
    assert (out / "stageshow-look.css").is_file()


def test_out_is_required_and_named_in_the_error():
    with pytest.raises(InputError) as err:
        run_kit(None)
    assert str(err.value).startswith("--out is missing")


def test_two_forced_writes_keep_both_backups(tmp_path):
    out = tmp_path / "kit"
    run_kit(out)
    (out / "index.ts").write_text("// first edit\n", encoding="utf-8")
    first = run_kit(out, force=True)
    (out / "index.ts").write_text("// second edit\n", encoding="utf-8")
    second = run_kit(out, force=True)
    assert first["backup"] != second["backup"]
    assert (out / first["backup"] / "index.ts").read_text(encoding="utf-8") == "// first edit\n"
    assert (out / second["backup"] / "index.ts").read_text(encoding="utf-8") == "// second edit\n"


def test_a_folder_that_cannot_hold_the_backup_is_an_input_error(tmp_path):
    out = tmp_path / "kit"
    run_kit(out)
    (out / "index.ts").write_text("// my edit\n", encoding="utf-8")
    (out / ".uxskill").write_text("a file where the backup folder goes\n", encoding="utf-8")
    with pytest.raises(InputError):
        run_kit(out, force=True)
    assert (out / "index.ts").read_text(encoding="utf-8") == "// my edit\n"


def test_a_format_without_a_system_is_refused(tmp_path):
    with pytest.raises(InputError) as err:
        run_kit(tmp_path / "kit", fmt="figma")
    assert str(err.value).startswith("--format reads the --from system")
    with pytest.raises(InputError) as err:
        run_kit(tmp_path / "kit", second_modes={"Colors": "Dark"})
    assert str(err.value).startswith("--figma-mode reads the --from system")


def test_only_the_kits_own_file_types_are_carried(tmp_path, monkeypatch):
    import engine.io.stageshow_kit as kit
    fake = tmp_path / "kit-src"
    (fake / "parts").mkdir(parents=True)
    (fake / "index.ts").write_text("export {}\n", encoding="utf-8")
    (fake / "parts" / "Row.css").write_text(".a{}\n", encoding="utf-8")
    (fake / ".DS_Store").write_bytes(b"\x00\x01\xff")
    (fake / "notes.swp").write_bytes(b"\xff\xfe")
    monkeypatch.setattr(kit, "KIT", fake)
    assert sorted(kit.kit_files()) == ["index.ts", "parts/Row.css"]
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "kits/stageshow/**/*\"" not in text


def test_the_look_lists_what_the_import_left_out(tmp_path):
    from engine.foundations.export import to_css
    src = tmp_path / "theme.css"
    src.write_text(to_css(build_system(NEUTRAL, "#3366FF").tokens)
                   + "\n.card { --card-glow: 0 0 4px red; }\n", encoding="utf-8")
    out = tmp_path / "kit"
    result = run_kit(out, source=src)
    assert result["not_read"] == 1
    assert "--card-glow" in (out / "stageshow-look.css").read_text(encoding="utf-8")


def test_a_system_without_the_roles_names_this_command():
    from engine.foundations.tokens import Token, TokenSet
    import engine.io.stageshow_kit as kit
    ts = TokenSet()
    ts.add(Token("brand.blue", "color", "#3366FF"))
    from engine.io.stageshow_out import to_stageshow
    with pytest.raises(InputError) as err:
        to_stageshow(ts, labels=kit.LABELS)
    assert str(err.value).startswith("kit stageshow reads")


def test_force_says_it_replaces_your_own_files_too():
    from click.testing import CliRunner

    from engine.cli.main import cli
    help_text = " ".join(CliRunner().invoke(cli, ["kit", "stageshow", "--help"]).output.split())
    assert "your own included" in help_text and ".uxskill/backup" in help_text


def test_files_an_older_kit_left_are_reported(tmp_path):
    out = tmp_path / "kit"
    run_kit(out)
    (out / "parts" / "Gone.tsx").write_text("export const Gone = 1\n", encoding="utf-8")
    result = run_kit(out)
    assert result["not_in_kit"] == ["parts/Gone.tsx"]
    assert "remove" in result["note"] and (out / "parts" / "Gone.tsx").exists()


def test_a_fresh_folder_reports_nothing_left_over(tmp_path):
    result = run_kit(tmp_path / "kit")
    assert "not_in_kit" not in result


def test_look_only_refreshes_the_look_and_keeps_your_kit_edits(tmp_path):
    out = tmp_path / "kit"
    run_kit(out, source=_tokens(tmp_path))
    (out / "index.ts").write_text("// my own edit\n", encoding="utf-8")
    old_look = (out / "stageshow-look.css").read_text(encoding="utf-8")
    other = tmp_path / "other.json"
    other.write_text(dump_dtcg(build_system(NEUTRAL, "#C0643A").tokens), encoding="utf-8")
    result = run_kit(out, source=other, look_only=True)
    assert result["status"] == "written" and result["written"] == ["stageshow-look.css"]
    assert (out / "stageshow-look.css").read_text(encoding="utf-8") != old_look
    assert (out / result["backup"] / "stageshow-look.css").read_text(encoding="utf-8") == old_look
    assert (out / "index.ts").read_text(encoding="utf-8") == "// my own edit\n"
    assert "not_in_kit" not in result


def test_look_only_needs_a_system(tmp_path):
    with pytest.raises(InputError) as err:
        run_kit(tmp_path / "kit", look_only=True)
    assert str(err.value).startswith("--look-only writes the look of the --from system")
