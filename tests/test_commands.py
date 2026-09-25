"""4.0 merges 25 slash commands into 18. The seven old names stay one
release as aliases: each says where it moved and runs the new command with
the same arguments. These tests hold the count, the aliases and every
place that states the count to that shape."""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = ROOT / "commands"

CANONICAL = {
    "ux-a11y", "ux-audit", "ux-case-study", "ux-copy", "ux-critique",
    "ux-design", "ux-discover", "ux-expert", "ux-fix", "ux-init", "ux-lint",
    "ux-mcp", "ux-motion", "ux-next", "ux-polish", "ux-research",
    "ux-system", "ux-workshop",
}
ALIASES = {
    "ux-frame": "ux-discover",
    "ux-recommend": "ux-discover",
    "ux-stats": "ux-init",
    "ux-evolve": "ux-polish",
    "ux-component": "ux-design",
    "ux-dashboard": "ux-design",
    "ux-image-to-code": "ux-design",
}
MERGED = {"ux-discover", "ux-design", "ux-polish", "ux-init"}
_MOVED = re.compile(r"^Moved to /(ux-[a-z0-9-]+)((?: --[a-z-]+(?: \d+)?)*)\. ")


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path.name} has no frontmatter"
    out = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


def _all():
    return {p.stem: p for p in sorted(COMMANDS.glob("ux-*.md"))}


def _is_alias(path: Path) -> bool:
    return bool(_MOVED.match(_frontmatter(path).get("description", "")))


def test_exactly_18_commands_that_are_not_aliases():
    real = {name for name, p in _all().items() if not _is_alias(p)}
    assert len(real) == 18
    assert real == CANONICAL


def test_the_aliases_are_the_seven_merged_names():
    aliases = {name for name, p in _all().items() if _is_alias(p)}
    assert aliases == set(ALIASES)
    assert len(_all()) == 18 + 7


@pytest.mark.parametrize("alias", sorted(ALIASES))
def test_every_alias_points_to_an_existing_command(alias):
    desc = _frontmatter(COMMANDS / f"{alias}.md")["description"]
    target, _flags = _MOVED.match(desc).groups()
    assert target == ALIASES[alias]
    path = COMMANDS / f"{target}.md"
    assert path.exists(), target
    assert not _is_alias(path), f"{alias} points at another alias"


@pytest.mark.parametrize("alias", sorted(ALIASES))
def test_every_alias_runs_its_target_with_the_same_arguments(alias):
    path = COMMANDS / f"{alias}.md"
    desc = _frontmatter(path)["description"]
    target, flags = _MOVED.match(desc).groups()
    body = path.read_text(encoding="utf-8")
    assert f"`/{target}{flags} $ARGUMENTS`" in body
    assert f"`commands/{target}.md`" in body
    assert "removed in 4.1" in body


@pytest.mark.parametrize("alias", sorted(ALIASES))
def test_the_target_documents_every_flag_the_alias_passes(alias):
    desc = _frontmatter(COMMANDS / f"{alias}.md")["description"]
    target, flags = _MOVED.match(desc).groups()
    doc = (COMMANDS / f"{target}.md").read_text(encoding="utf-8")
    for flag in re.findall(r"--[a-z-]+", flags):
        assert f"`{flag}" in doc, (alias, flag)
    assert f"/{alias}" in doc, f"{target}.md does not say it absorbed /{alias}"


@pytest.mark.parametrize("alias", sorted(ALIASES))
def test_the_model_does_not_pick_an_alias_on_its_own(alias):
    assert _frontmatter(COMMANDS / f"{alias}.md")["disable-model-invocation"] == "true"


@pytest.mark.parametrize("name", sorted(MERGED | set(ALIASES)))
def test_touched_descriptions_are_short_and_plain(name):
    desc = _frontmatter(COMMANDS / f"{name}.md")["description"]
    assert len(desc) <= 220, name
    assert "—" not in desc and " -- " not in desc, name


def test_the_changelog_marks_every_alias_for_removal_in_4_1():
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    start = text.index("## [Unreleased]")
    section = text[start:text.index("\n## [", start + 1)]
    assert "removed in 4.1" in section
    for alias in ALIASES:
        assert f"`/{alias}`" in section, alias


def _dashboard_section() -> str:
    doc = (COMMANDS / "ux-design.md").read_text(encoding="utf-8")
    start = doc.index("### Dashboard mode (`--dashboard`)")
    return doc[start:doc.index("\n### ", start + 1)]


def test_dashboard_mode_skips_the_page_sequence():
    assert "The page-sequence step (v2 step 2.5) does not apply" in _dashboard_section()


def test_the_modes_table_keeps_page_steps_out_of_component_and_dashboard():
    doc = (COMMANDS / "ux-design.md").read_text(encoding="utf-8")
    rows = {}
    for line in doc.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[1:] in (["yes", "no", "no"], ["yes", "yes", "yes"]):
            rows[cells[0]] = cells[1:]
    page_only = [k for k, v in rows.items() if v == ["yes", "no", "no"]]
    assert any("2.5" in k for k in page_only)
    assert any("hero" in k for k in page_only)
    assert any("SEO" in k for k in page_only)
    assert any("(b)" in k and "(d)" in k for k in page_only)
    shared = [k for k, v in rows.items() if v == ["yes", "yes", "yes"]]
    assert any("(a)" in k and "(e)" in k for k in shared)
    assert any("brand" in k for k in shared)


def test_default_polish_never_touches_the_original_file():
    doc = (COMMANDS / "ux-polish.md").read_text(encoding="utf-8")
    assert "The original file is never touched" in doc
    assert "**`--loop-only` or `--fix`:** first validate a clean working tree" in doc
    assert "On `gate_failed` without `--force`" in doc


def test_the_polish_loop_defaults_to_three_rounds_and_a_score_of_90():
    doc = (COMMANDS / "ux-polish.md").read_text(encoding="utf-8")
    assert "reaches 90 or three rounds pass" in _frontmatter(COMMANDS / "ux-polish.md")["description"]
    assert "--max-rounds <rounds, default 3>" in doc


# ------------------------------------------------------ places that count


def test_the_manifests_say_18_commands():
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    texts = [plugin["description"], market["description"], market["plugins"][0]["description"]]
    for text in texts:
        assert "18 slash commands" in text or "18 callable slash commands" in text
        assert "25 slash commands" not in text and "25 callable" not in text


def test_the_readme_says_18_commands():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## The 18 slash commands: detailed reference" in readme
    assert "25 slash commands" not in readme.replace("25 slash commands become 18", "")
    assert "### Aliases, removed in 4.1" in readme


def test_the_readme_reference_documents_exactly_the_18_commands():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    start = readme.index("## The 18 slash commands: detailed reference")
    section = readme[start:readme.index("### Aliases, removed in 4.1", start)]
    documented = re.findall(r"^#### `/(ux-[a-z0-9-]+)`", section, re.M)
    assert len(documented) == len(set(documented)), documented
    assert set(documented) == CANONICAL


def test_the_commands_page_lists_18_commands_and_the_aliases():
    page = (ROOT / "docs" / "commands.html").read_text(encoding="utf-8")
    cards = re.findall(r'<article class="cmd" id="(ux-[a-z0-9-]+)">', page)
    assert sorted(cards) == sorted(CANONICAL)
    assert "18 slash commands referenced" in page
    for alias, target in ALIASES.items():
        assert f'<code>/{alias}</code> runs <a href="#{target}">' in page
    item_list = next(json.loads(m) for m in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', page) if '"ItemList"' in m)
    assert item_list["numberOfItems"] == 18
    assert {i["name"][1:] for i in item_list["itemListElement"]} == CANONICAL
