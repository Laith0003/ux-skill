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
    assert '"kits/stageshow/**/*"' in text


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
