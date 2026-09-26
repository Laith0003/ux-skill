"""Edges of the existing-system rule: where the token source lives, weak
signals, modern color syntax, ownership that survives hand edits, and every
command that could override a client's system."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

pytest.importorskip("click")
from click.testing import CliRunner  # noqa: E402

from engine.cli.main import cli  # noqa: E402
from engine.existing import detect_existing_system, is_ux_skill_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "client_system"
PRIMARY = "#1C64D9"


@pytest.fixture
def client(tmp_path: Path) -> Path:
    dest = tmp_path / "client"
    shutil.copytree(FIXTURE, dest)
    return dest


def _run(args, cwd: Path):
    old = os.getcwd()
    os.chdir(cwd)
    try:
        return CliRunner().invoke(cli, ["--no-pretty"] + list(args), catch_exceptions=False)
    finally:
        os.chdir(old)


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _dtcg(primary) -> str:
    return json.dumps({"brand": {"$type": "color", "primary": {"$value": primary}}})


# ---------------------------------------------------------------- source over build output


def test_the_file_a_build_script_reads_is_the_source(tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/build.mjs",
           'const SOURCE = resolve(here, "../../src/brand/tokens.json");\n')
    _write(tmp_path, "src/brand/tokens.json", _dtcg(PRIMARY))
    _write(tmp_path, "packages/tokens/build/tokens.resolved.json", _dtcg("#FFFFFF"))
    found = detect_existing_system(tmp_path)
    kinds = {s["path"]: s["kind"] for s in found["sources"]}
    assert kinds["src/brand/tokens.json"] == "tokens-source"
    assert kinds["packages/tokens/build/tokens.resolved.json"] == "built-output"
    assert found["sources"][0]["kind"] == "tokens-source"
    assert found["declared"]["primary"] == PRIMARY


def test_a_generated_header_marks_built_output(tmp_path: Path) -> None:
    _write(tmp_path, "tokens/tokens.css",
           "/* Generated from tokens.json. Do not edit. */\n"
           ":root{--brand-primary:#1C64D9;--text-default:#1E2329;--space-1:4px}")
    found = detect_existing_system(tmp_path)
    assert {"kind": "built-output", "path": "tokens/tokens.css"} in found["sources"]
    assert found["found"] is True


# ---------------------------------------------------------------- weak signals, modern color


@pytest.mark.parametrize("files", [
    {"packages/stylelint-config/index.js": "module.exports = {}"},
    {"css/build.js": "console.log(1)"},
    {"package.json": json.dumps({"scripts": {"refresh-token": "node auth.js"}})},
    {"tokens/api.json": json.dumps({"stripe": {"value": "sk_test_x", "type": "secret"}})},
], ids=["stylelint-folder", "css-build-js", "refresh-token-script", "api-secrets-json"])
def test_weak_signals_are_hints_not_a_system(tmp_path: Path, files: dict) -> None:
    for rel, text in files.items():
        _write(tmp_path, rel, text)
    found = detect_existing_system(tmp_path)
    assert found["found"] is False
    assert found["declared"] == {}


def test_a_folder_alone_is_reported_as_a_hint(tmp_path: Path) -> None:
    _write(tmp_path, "design-system/README.txt", "notes")
    found = detect_existing_system(tmp_path)
    assert found["found"] is False
    assert {"kind": "system-folder", "path": "design-system"} in found["hints"]


@pytest.mark.parametrize("value", [
    "oklch(53.15% 0.1928 260.18)",
    "hsl(217 77% 48%)",
    "hsl(217, 77%, 48%)",
    "color(srgb 0.1098 0.3922 0.851)",
    {"colorSpace": "oklch", "components": [0.5315, 0.1928, 260.18]},
    {"colorSpace": "hsl", "components": [217, 77, 48]},
], ids=["oklch", "hsl-space", "hsl-comma", "color-srgb", "dtcg-oklch", "dtcg-hsl"])
def test_modern_color_syntax_declares_a_primary(tmp_path: Path, value) -> None:
    _write(tmp_path, "tokens.json", _dtcg(value))
    primary = detect_existing_system(tmp_path)["declared"]["primary"]
    r, g, b = (int(primary[i:i + 2], 16) for i in (1, 3, 5))
    assert abs(r - 0x1C) <= 3 and abs(g - 0x64) <= 3 and abs(b - 0xD9) <= 3, primary


def test_an_unreadable_primary_is_reported_raw(tmp_path: Path) -> None:
    _write(tmp_path, "tokens.json", json.dumps({"brand": {
        "$type": "color", "primary": {"$value": "color-mix(in srgb, #1C64D9 80%, white)"},
        "canvas": {"$value": "#FFFFFF"}}}))
    declared = detect_existing_system(tmp_path)["declared"]
    assert "primary" not in declared
    assert declared["primary_raw"] == "color-mix(in srgb, #1C64D9 80%, white)"
    assert "primary_note" in declared


# ---------------------------------------------------------------- ownership


def test_a_hand_edited_persist_file_is_not_overwritten(tmp_path: Path) -> None:
    from engine.persist import save_master_result
    first = save_master_result(str(tmp_path), {"palette": {"id": "a"}}, {"project": "p"})
    path = Path(first["path"])
    edited = path.read_text(encoding="utf-8") + "\nOur own note.\n"
    path.write_text(edited, encoding="utf-8")
    second = save_master_result(str(tmp_path), {"palette": {"id": "b"}}, {"project": "p"})
    assert path.read_text(encoding="utf-8") == edited
    assert second["wrote_beside"] is True and second["path"] != str(path)


@pytest.mark.parametrize("text", [
    "---\nproject: p\n---\n\n# Design system \u2014 MASTER\n\nOur notes.\n",
    "---\nproject: p\nlast_updated: \"2026-01-01T00:00:00Z\"\nux_skill_version: 2.0.0\n---\n\n"
    "# Design system \u2014 MASTER\n\nold engine file\n",
    "---\nproject: p\ngenerated_by: ux-skill-inspired handwork\n---\n\n# Ours\n",
], ids=["legacy-heading-hand-file", "legacy-engine-file", "look-alike-owner"])
def test_files_without_a_valid_digest_are_written_beside(tmp_path: Path, text: str) -> None:
    from engine.persist import save_master_result
    target = _write(tmp_path, ".ux/design-system/MASTER.md", text)
    result = save_master_result(str(tmp_path), {}, {"project": "p"})
    assert target.read_text(encoding="utf-8") == text
    assert result["wrote_beside"] is True


def test_design_md_keeps_a_hand_edit(tmp_path: Path) -> None:
    out = tmp_path / "DESIGN.md"
    assert _run(["design-md", "--out", str(out)], cwd=tmp_path).exit_code == 0
    edited = out.read_text(encoding="utf-8").replace("canvas:", "canvas-edited:", 1) + "\n"
    out.write_text(edited, encoding="utf-8")
    result = _run(["design-md", "--out", str(out)], cwd=tmp_path)
    assert result.exit_code == 0, result.output
    assert out.read_text(encoding="utf-8") == edited
    assert (tmp_path / "DESIGN.ux-skill.md").is_file()
    assert "did not write" in result.output


def test_design_md_reruns_on_its_own_non_default_path(client: Path) -> None:
    out = client / "DESIGN.ux-skill.md"
    for _ in range(2):
        result = _run(["design-md", "--from-system", "--out", str(out)], cwd=client)
        assert result.exit_code == 0, result.output
    assert is_ux_skill_file(out)


# ---------------------------------------------------------------- every command reads it


def test_mcp_recommend_reads_the_project(client: Path) -> None:
    from engine.mcp import TOOLS
    handler = TOOLS["ux_recommend"][0]
    rec = handler({"brief": {"industry": "saas"}, "project_root": str(client)})
    assert rec["palette"]["status"] == "suggestion"
    assert rec["existing_system"]["declared"]["primary"] == PRIMARY


def test_mcp_has_a_detect_tool(client: Path) -> None:
    from engine.mcp import TOOLS
    handler = TOOLS["ux_system_detect"][0]
    assert handler({"root": str(client)})["declared"]["primary"] == PRIMARY


def test_system_build_never_replaces_a_client_system_even_with_force(client: Path) -> None:
    target = client / "design-system" / "tokens"
    _write(target, "tokens.css", ":root{--brand-primary:#1C64D9;--a:1px;--b:2px}")
    before = (target / "tokens.json").read_text(encoding="utf-8")
    result = _run(["system", "build", "--brand", "#3366FF", "--out", str(target), "--force"],
                  cwd=client)
    assert result.exit_code != 0
    assert (target / "tokens.json").read_text(encoding="utf-8") == before
    assert "--replace-client-files" in result.output


def test_mcp_system_build_never_replaces_a_client_system(client: Path) -> None:
    from engine.mcp import TOOLS
    target = client / "design-system" / "tokens"
    before = (target / "tokens.json").read_text(encoding="utf-8")
    result = TOOLS["ux_system_build"][0]({"brand": "#3366FF", "out": str(target),
                                           "force": True})
    assert result["status"] == "refused" and "tokens.json" in result["conflicts"]
    assert (target / "tokens.json").read_text(encoding="utf-8") == before


def test_system_build_may_rebuild_its_own_folder(tmp_path: Path) -> None:
    out = tmp_path / "sys"
    assert _run(["system", "build", "--brand", "#3366FF", "--out", str(out)],
                cwd=tmp_path).exit_code == 0
    result = _run(["system", "build", "--brand", "#FF6633", "--out", str(out), "--force"],
                  cwd=tmp_path)
    assert result.exit_code == 0, result.output


def test_generate_marks_its_picks_as_suggestions(client: Path) -> None:
    result = _run(["generate", "--out-dir", str(client / ".ux" / "gen")], cwd=client)
    assert result.exit_code == 0, result.output
    bundle = json.loads(result.stdout)
    assert bundle["summary"]["status"] == "suggestion"
    assert "design-system/tokens/tokens.json" in bundle["summary"]["existing_system"]


@pytest.mark.parametrize("doc", [
    "commands/ux-design.md", "commands/ux-discover.md", "commands/ux-fix.md",
    "commands/ux-polish.md", "commands/ux-system.md", "agents/frontend-engineer.md",
    "agents/design-system-architect.md",
])
def test_generating_commands_run_detect_first(doc: str) -> None:
    """ux-component, ux-dashboard and ux-recommend are aliases of ux-design and
    ux-discover, so the real commands carry the step."""
    text = (ROOT / doc).read_text(encoding="utf-8")
    assert "system detect" in text, doc


def test_ux_system_never_offers_to_replace_a_client_system() -> None:
    text = (ROOT / "commands" / "ux-system.md").read_text(encoding="utf-8")
    assert "extend or replace" not in text


# ---------------------------------------------------------------- L1 to L5


def test_persist_load_falls_back_to_the_clients_master(client: Path) -> None:
    from engine.persist import load_master
    loaded = load_master(str(client))
    assert loaded is not None and loaded["owner"] == "hand-written"
    assert loaded["path"].endswith("design-system/MASTER.md")


def test_save_page_says_it_wrote_beside_and_list_skips_the_copy(tmp_path: Path) -> None:
    from engine.persist import list_pages, save_page_result
    hand = _write(tmp_path, ".ux/design-system/pages/home.md", "# Our home page notes\n")
    result = save_page_result(str(tmp_path), "home", {}, {})
    assert result["wrote_beside"] is True and "did not write" in result["note"]
    assert hand.read_text(encoding="utf-8") == "# Our home page notes\n"
    assert list_pages(str(tmp_path)) == ["home"]


def test_a_bad_list_item_is_named() -> None:
    from engine.recommender import BriefError, brief_from_dict
    with pytest.raises(BriefError) as err:
        brief_from_dict({"forbidden": ["a", 1]})
    assert "forbidden item 2 is a number (1)" in str(err.value)
    with pytest.raises(BriefError) as err:
        brief_from_dict({"industry": {"x": 1}})
    assert "industry is an object" in str(err.value)
    with pytest.raises(BriefError) as err:
        brief_from_dict("saas")
    assert "is a string" in str(err.value)


def test_detect_on_a_missing_root_exits_2(tmp_path: Path) -> None:
    result = _run(["system", "detect", "--root", str(tmp_path / "nope")], cwd=tmp_path)
    assert result.exit_code == 2
    assert "does not exist" in result.output and "--root" in result.output


def test_brand_capture_docs_name_the_declared_exception() -> None:
    for rel in ("commands/ux-design.md", "references/process/brand-extraction.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "unless `ux system detect` declares a primary" in text, rel


def test_synthesize_reads_the_existing_system(client: Path) -> None:
    result = _run(["synthesize", "--industry", "saas", "--project-root", str(client)], cwd=client)
    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["existing_system"]["declared"]["primary"] == PRIMARY
    assert payload["status"] == "suggestion"


def test_mcp_synthesize_reads_the_existing_system(client: Path) -> None:
    from engine.mcp import TOOLS
    out = TOOLS["ux_synthesize"][0]({"industry": "saas", "project_root": str(client)})
    assert out["existing_system"]["declared"]["primary"] == PRIMARY
    assert out["status"] == "suggestion"


def test_mcp_image_extract_reads_the_existing_system(client: Path) -> None:
    pytest.importorskip("PIL")
    from PIL import Image
    from engine.mcp import TOOLS
    img = client / "shot.png"
    Image.new("RGB", (64, 64), (28, 100, 217)).save(img)
    out = TOOLS["ux_image_extract"][0]({"path": str(img), "project_root": str(client)})
    assert out["recommendation"]["palette"]["status"] == "suggestion"


def test_detect_reads_hues_and_hsl_through_the_value_reader():
    """detect keeps a lenient reading for what the importer refuses, but a
    hue and an hsl color are converted by the value reader's own helpers,
    so the two read one color one way."""
    from engine.existing import detect
    from engine.io.values_in import hsl_to_rgb, hue_degrees, read_value

    # The lenient paths still read, in the reader's units.
    assert detect.normalize_hex("hsl(0.5turn, 100%, 50%, 1, 2)") == "#00FFFF"
    assert detect.normalize_hex("oklch(60% 0.1 3.14rad, 1)") == "#239382"
    for unit, angle in (("deg", "225deg"), ("turn", "0.625turn"), ("rad", "3.92699rad"),
                        ("grad", "250grad")):
        assert round(detect._hue(angle)) == round(hue_degrees(angle)) == 225, unit
    # The DTCG hsl object is converted by the reader's own hsl conversion.
    for h, s, lt in ((225, 100, 60), (225, 50, 40), (10, 80, 30), (300, 20, 90)):
        want = "#%02X%02X%02X" % tuple(int(round(c)) for c in hsl_to_rgb(h, s / 100, lt / 100))
        assert detect.normalize_hex({"colorSpace": "hsl", "components": [h, s, lt]}) == want
    assert detect.normalize_hex({"colorSpace": "hsl", "components": [225, 100, 60]}) \
        == read_value("hsl(225 100% 60%)")[1]
