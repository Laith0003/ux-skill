"""An existing design system is fixed input: every command reads it first.

The fixture under tests/fixtures/client_system is a small invented client
system: a DTCG tokens.json, a token build script, CSS custom-property
foundation files, a hand-written MASTER.md, a built tokens.css and a logo
whose pixels (#3D8BF0) differ from the declared primary (#1C64D9).
"""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

import pytest

click = pytest.importorskip("click")
from click.testing import CliRunner  # noqa: E402

from engine.cli.main import cli  # noqa: E402
from engine.existing import detect_existing_system, is_ux_skill_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "client_system"
PRIMARY = "#1C64D9"
LOGO_PIXEL = "#3D8BF0"
TEXT = "#1E2329"


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


# ---------------------------------------------------------------- 14: detection


def test_detect_finds_every_kind_of_source(client: Path) -> None:
    found = detect_existing_system(client)
    assert found["found"] is True
    kinds = {s["kind"] for s in found["sources"]}
    assert {"tokens", "build-script", "css-foundation", "master-md", "system-folder"} <= kinds
    paths = {s["path"] for s in found["sources"]}
    assert "design-system/tokens/tokens.json" in paths
    assert "design-system/tokens/build.mjs" in paths
    assert "design-system/MASTER.md" in paths


def test_detect_reads_the_declared_values(client: Path) -> None:
    declared = detect_existing_system(client)["declared"]
    assert declared["primary"] == PRIMARY
    assert declared["primary_token"] == "brand.primary"
    assert declared["text"] == TEXT
    assert declared["text_token"] == "text.primary"
    assert declared["fonts"]["body"] == "Fixture Sans"
    assert declared["languages"][0] == "ar"
    assert declared["colors"]["brand-primary"] == PRIMARY
    assert "color-harbor-500" not in declared["colors"]  # ramp steps are not roles


def test_detect_reads_css_foundations_when_there_is_no_token_file(tmp_path: Path) -> None:
    css = tmp_path / "styles"
    css.mkdir()
    (css / "theme.css").write_text(
        ":root{--blue-500: rgb(28 100 217); --color-primary: var(--blue-500);"
        "--color-text: #1E2329; --space-1: 4px}", encoding="utf-8")
    found = detect_existing_system(tmp_path)
    assert found["found"] is True
    assert found["declared"]["primary"] == PRIMARY
    assert found["declared"]["primary_token"] == "--color-primary"
    assert found["declared"]["text"] == TEXT


def test_detect_finds_nothing_in_an_empty_project(tmp_path: Path) -> None:
    found = detect_existing_system(tmp_path)
    assert found["found"] is False and found["sources"] == []


def test_detect_does_not_count_files_ux_skill_wrote(tmp_path: Path) -> None:
    from engine.persist import save_master
    save_master(str(tmp_path), {}, {"project": "p"})
    assert is_ux_skill_file(tmp_path / ".ux" / "design-system" / "MASTER.md")
    assert detect_existing_system(tmp_path)["found"] is False


def test_detect_finds_nothing_in_this_repository() -> None:
    """Commands default to the working folder; the plugin repo itself must
    not read as a client system."""
    assert detect_existing_system(ROOT)["found"] is False


def test_system_detect_cli_prints_the_detection(client: Path) -> None:
    result = _run(["system", "detect", "--root", str(client)], cwd=client)
    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["found"] is True
    assert payload["declared"]["primary"] == PRIMARY


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    nxt = text.find("\n### ", start + len(heading))
    return text[start:nxt if nxt != -1 else len(text)]


def test_ux_design_page_mode_checks_for_an_existing_system_first() -> None:
    text = (ROOT / "commands" / "ux-design.md").read_text(encoding="utf-8")
    sec = _section(text, "### 1a. An existing design system is fixed input")
    for word in ("tokens.json", "build script", "custom-property", "MASTER.md", "DESIGN.md",
                 "design-system/", "packages/tokens", "system detect", "extension file"):
        assert word in sec, word
    assert "skip" in sec.lower()
    assert len(sec.split()) < 260, "keep the existing-system step short"


# ---------------------------------------------------------------- 16: recommend


def test_step_3_calls_the_picks_suggestions_when_a_system_exists() -> None:
    text = (ROOT / "commands" / "ux-design.md").read_text(encoding="utf-8")
    sec = _section(text, "### Step 3")
    assert "existing design system" in sec
    assert "suggestion" in sec
    assert not re.search(r"^- The picked `palette.colors` are the only color tokens used$",
                         sec, re.M)


def test_recommend_marks_its_picks_as_suggestions_under_an_existing_system(client: Path) -> None:
    result = _run(["recommend", "--industry", "saas", "--project-root", str(client)], cwd=client)
    assert result.exit_code == 0, result.output
    rec = json.loads(result.stdout)
    assert rec["existing_system"]["declared"]["primary"] == PRIMARY
    assert rec["palette"]["status"] == "suggestion"
    assert rec["type_pair"]["status"] == "suggestion"
    assert any("existing design system" in w for w in rec["warnings"])


def test_recommend_without_a_system_is_unchanged(tmp_path: Path) -> None:
    result = _run(["recommend", "--industry", "saas", "--project-root", str(tmp_path)],
                  cwd=tmp_path)
    rec = json.loads(result.stdout)
    assert rec.get("existing_system") is None
    assert "status" not in (rec["palette"] or {})


# ---------------------------------------------------------------- 17: design-md


def test_design_md_accepts_extra_keys_and_forbidden_as_a_string(tmp_path: Path) -> None:
    brief = tmp_path / "brief.json"
    brief.write_text(json.dumps({
        "industry": "saas", "tone": "calm, precise", "forbidden": "brutalism, purple-gradients",
        "goal": "demo requests", "wow_moment": "a live quote", "reference_brands": ["x"],
    }), encoding="utf-8")
    result = _run(["design-md", "--brief-file", str(brief), "--out", str(tmp_path / "DESIGN.md")],
                  cwd=tmp_path)
    assert result.exit_code == 0, result.output
    assert (tmp_path / "DESIGN.md").is_file()


def test_design_md_names_the_field_and_the_fix_on_a_bad_brief(tmp_path: Path) -> None:
    brief = tmp_path / "brief.json"
    brief.write_text(json.dumps({"forbidden": 5}), encoding="utf-8")
    result = CliRunner().invoke(cli, ["--no-pretty", "design-md", "--brief-file", str(brief),
                                      "--out", str(tmp_path / "DESIGN.md"),
                                      "--project-root", str(tmp_path)])
    assert result.exit_code == 2
    assert "forbidden" in result.output and "list" in result.output
    assert not (tmp_path / "DESIGN.md").exists()


def test_design_md_refuses_to_contradict_an_existing_system(client: Path) -> None:
    result = _run(["design-md", "--out", str(client / "DESIGN.md")], cwd=client)
    assert result.exit_code == 1
    assert "--from-system" in result.output
    assert "design-system/tokens/tokens.json" in result.output
    assert not (client / "DESIGN.md").exists()


def test_design_md_from_system_writes_the_systems_values(client: Path) -> None:
    result = _run(["design-md", "--from-system", "--out", str(client / "DESIGN.md")], cwd=client)
    assert result.exit_code == 0, result.output
    md = (client / "DESIGN.md").read_text(encoding="utf-8")
    assert PRIMARY in md and TEXT in md and "Fixture Sans" in md
    assert "brand-primary" in md
    for house in ("#cc785c", "#5e6ad2", "Georgia"):
        assert house not in md


def test_design_md_never_overwrites_a_hand_written_design_md(client: Path) -> None:
    target = client / "DESIGN.md"
    target.write_text("# Our design\n\nHand-written.\n", encoding="utf-8")
    result = _run(["design-md", "--from-system", "--out", str(target)], cwd=client)
    assert result.exit_code == 1
    assert "did not write" in result.output
    assert target.read_text(encoding="utf-8") == "# Our design\n\nHand-written.\n"


# ---------------------------------------------------------------- 18: persist


def _hand_written_master(root: Path) -> Path:
    target = root / ".ux" / "design-system" / "MASTER.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIXTURE / "design-system" / "MASTER.md", target)
    return target


def test_persist_save_never_overwrites_a_hand_written_master(tmp_path: Path) -> None:
    from engine.persist import save_master
    target = _hand_written_master(tmp_path)
    before = target.read_text(encoding="utf-8")
    written = Path(save_master(str(tmp_path), {"palette": {"id": "x"}}, {"project": "p"}))
    assert target.read_text(encoding="utf-8") == before
    assert written != target and written.parent == target.parent
    assert is_ux_skill_file(written)


def test_persist_save_overwrites_its_own_file(tmp_path: Path) -> None:
    from engine.persist import save_master
    first = save_master(str(tmp_path), {"palette": {"id": "a"}}, {"project": "p"})
    second = save_master(str(tmp_path), {"palette": {"id": "b"}}, {"project": "p"})
    assert first == second
    assert "b" in Path(second).read_text(encoding="utf-8")


def test_persist_save_still_owns_a_master_from_before_the_marker(tmp_path: Path) -> None:
    from engine.persist import save_master
    target = tmp_path / ".ux" / "design-system" / "MASTER.md"
    target.parent.mkdir(parents=True)
    target.write_text("---\nproject: p\nlast_updated: \"2026-01-01T00:00:00Z\"\n"
                      "ux_skill_version: 2.0.0\n---\n\n# Design system \u2014 MASTER\n\nold\n",
                      encoding="utf-8")
    assert save_master(str(tmp_path), {}, {"project": "p"}) == str(target.resolve())


def test_persist_save_cli_says_it_wrote_beside(tmp_path: Path) -> None:
    _hand_written_master(tmp_path)
    rec = tmp_path / "rec.json"
    rec.write_text("{}", encoding="utf-8")
    result = _run(["persist", "save", "--project-root", str(tmp_path),
                   "--from-recommendation", str(rec), "--from-brief", str(tmp_path / "none.json")],
                  cwd=tmp_path)
    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["wrote_beside"] is True
    assert "MASTER.md" in payload["note"] and "did not write" in payload["note"]


def test_persist_save_notes_an_existing_system(client: Path) -> None:
    from engine.persist import save_master
    path = save_master(str(client), {}, {"project": "p"})
    body = Path(path).read_text(encoding="utf-8")
    assert "## Existing design system" in body
    assert "design-system/tokens/tokens.json" in body


def test_persist_load_returns_structure(tmp_path: Path) -> None:
    from engine.persist import load_master
    _hand_written_master(tmp_path)
    loaded = load_master(str(tmp_path))
    assert loaded["owner"] == "hand-written"
    assert loaded["meta"]["maintainer"] == "client design team"
    sections = {s["title"]: s for s in loaded["sections"]}
    assert sections["Palette"]["fields"]["Primary"] == "#1C64D9 (brand.primary)"
    assert sections["Type"]["tables"][0][0] == {"Role": "Primary", "Token": "brand.primary"}
    assert "Labels are sentence case at zero tracking." in sections["Rules"]["items"]
    assert loaded["body"].startswith("# Fixture Client tokens and rules")


# ---------------------------------------------------------------- 19: brand extraction


def test_declared_primary_beats_logo_pixels_and_both_are_reported(client: Path) -> None:
    from engine.brand import build_profile
    signals = json.loads((client / "brand-signals.json").read_text(encoding="utf-8"))
    signals["declared"] = detect_existing_system(client)["declared"]
    p = build_profile(signals)
    assert p.primary == PRIMARY
    assert p.primary_source == "tokens"
    assert p.logo_primary == LOGO_PIXEL
    assert any(PRIMARY in n and LOGO_PIXEL in n for n in p.notes)
    assert p.text_color == TEXT
    assert TEXT not in p.secondary
    assert p.language == "ar"


def test_text_color_is_not_a_secondary_without_tokens() -> None:
    from engine.brand import build_profile
    p = build_profile({"logo_colors": [{"hex": "#1C64D9"}],
                       "brand_colors": [{"hex": "#D6263B"}, {"hex": "#1E2329"}]})
    assert p.secondary == ["#D6263B"]
    assert p.text_color == "#1E2329"


def test_language_comes_from_the_voice_when_no_file_says() -> None:
    from engine.brand import build_profile
    assert build_profile({"voice": "professional, Arabic-first"}).language == "ar"


def test_brand_cli_reads_the_project_files(client: Path) -> None:
    result = _run(["brand", "--signals-file", "brand-signals.json", "--out", ".ux"], cwd=client)
    assert result.exit_code == 0, result.output
    bj = json.loads((client / ".ux" / "brand.json").read_text(encoding="utf-8"))
    assert bj["primary"] == PRIMARY and bj["primary_source"] == "tokens"
    assert bj["logo_primary"] == LOGO_PIXEL
    assert bj["language"] == "ar"
    assert TEXT not in bj["secondary"]


# ---------------------------------------------------------------- 20: brand fidelity


def _profile():
    from engine.brand.extract import BrandProfile
    return BrandProfile(name="Fixture Client", primary=PRIMARY,
                        logo={"url": "img/logo.svg", "alt": "Fixture Client"})


def test_fidelity_reads_linked_stylesheets(client: Path) -> None:
    from engine.brand import score_brand_fidelity
    site = client / "site"
    html = (site / "index.html").read_text(encoding="utf-8")
    assert PRIMARY.lower() not in html.lower()
    res = score_brand_fidelity(html, _profile(), base_dir=site)
    assert res["passed"] is True and res["score"] == 100
    detail = next(f for f in res["findings"] if f["check"] == "primary_used")["detail"]
    assert "--brand-primary" in detail


def test_fidelity_resolves_custom_properties_in_other_color_forms() -> None:
    from engine.brand import score_brand_fidelity
    html = ("<html><head><style>:root{--blue: rgb(28, 100, 217); --cta: var(--blue)}"
            ".b{background: var(--cta)}</style></head><body><header>Fixture Client</header>"
            "</body></html>")
    res = score_brand_fidelity(html, _profile())
    assert res["passed"] is True


def test_evaluate_passes_the_page_folder_to_fidelity(client: Path) -> None:
    from engine.evaluator import evaluate
    site = client / "site"
    ev = evaluate(html=(site / "index.html").read_text(encoding="utf-8"),
                  brand_profile=_profile(), base_dir=str(site))
    assert ev.brand_fidelity == 100 and ev.brand_passed is True


# ---------------------------------------------------------------- 22: guidance


def test_anti_slop_says_the_clients_system_wins() -> None:
    text = (ROOT / "references" / "styles" / "anti-slop.md").read_text(encoding="utf-8")
    head = text[:text.index("## Responsive")]
    assert "existing design system" in head.lower()
    row = next(ln for ln in text.splitlines() if ln.startswith("| Eyebrows that aren't tracked"))
    assert "existing design system" in row


def test_eyebrow_guidance_defers_to_the_clients_system() -> None:
    for rel in ("engine/rulepack/guidance/type.md", "references/foundations/typography.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert re.search(r"existing (design )?system", text), rel
