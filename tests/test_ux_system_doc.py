"""The /ux-system command doc and the architect agent must match the CLI
they tell the model to run: every flag the create mode uses exists, the
MCP tool it names exists, every status the CLI prints is in its table with
its exit code, the font families it names are the ones the engine picks,
and the 4.1 modes are marked as not yet here. The README and CHANGELOG
beta sections tell a reader how to install the beta, and no doc promises a
brief word the synthesizer does not read."""
import re
from pathlib import Path

import pytest

pytest.importorskip("click")

from engine import __version__  # noqa: E402
from engine.cli.main import cli  # noqa: E402
from engine.discovery.core import FIELDS  # noqa: E402
from engine.foundations.emit import STATUS_EXIT, _reading  # noqa: E402
from engine.foundations.typography import CODE_FACE, PAIRINGS  # noqa: E402
from engine.mcp import TOOLS  # noqa: E402
from engine.mcp.server import UxSystemBuildInput  # noqa: E402
from engine.synthesizer.axes import INDUSTRY_SEEDS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOC = (ROOT / "commands" / "ux-system.md").read_text(encoding="utf-8")
AGENT = (ROOT / "agents" / "design-system-architect.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
CHANGELOG = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end == -1 else text[start:end]


CREATE = _section(DOC, "## create mode (4.0 beta)")


def _step(heading: str) -> str:
    """One numbered step of the create mode, up to the next step."""
    start = CREATE.index(heading)
    end = CREATE.find("\n### ", start + len(heading))
    return CREATE[start:] if end == -1 else CREATE[start:end]


README_BETA = README[README.index("### New in 4.0 beta"):README.index("### New in v3.1")]
CHANGELOG_BETA = CHANGELOG[CHANGELOG.index("## [4.0.0-beta.1]"):CHANGELOG.index("## [3.2.0]")]


def _build_flags():
    build = cli.commands["system"].commands["build"]
    return {opt for p in build.params for opt in p.opts} | {"--no-pretty", "--pretty"}


def test_every_flag_the_create_mode_names_exists():
    used = set(re.findall(r"(?<![\w-])(--[a-z][a-z-]*)", CREATE))
    assert used, "the create section names no flags"
    # --version belongs to uxskill itself, which the first step runs.
    assert "--version" in {opt for p in cli.params for opt in p.opts}
    used.discard("--version")
    assert used <= _build_flags(), sorted(used - _build_flags())


def test_the_documented_command_is_the_real_one():
    assert "uxskill --no-pretty system build --brand '#3366FF'" in CREATE
    assert "python3 -m engine.cli.main" in CREATE


def test_the_mcp_tool_it_names_exists():
    assert "ux_system_build" in CREATE and "ux_system_build" in TOOLS
    fields = set(UxSystemBuildInput.model_json_schema()["properties"])
    for field in ("brand", "brief", "axes", "latin_only", "out", "include_files", "force"):
        assert field in fields and f"`{field}`" in CREATE, field


def test_agents_with_a_shell_use_the_cli_and_agents_without_one_pass_out():
    run = _step("### 4. Run the engine")
    assert "With a shell, use the command above" in run
    assert "Without a shell" in run and "`out`" in run
    for status in ("`built`", "`invalid`"):
        assert status in run, status
    assert "save them with Write" not in CREATE
    assert "do not copy" in run


def test_every_status_the_cli_prints_is_in_the_table_with_its_exit_code():
    rows = re.findall(r"^\| `([a-z]+)` \| (\d) \|", CREATE, re.M)
    assert dict(rows) == {status: str(code) for status, code in STATUS_EXIT.items()}
    assert len(rows) == len(STATUS_EXIT)


def test_a_failed_build_points_at_the_inputs_not_at_tokens():
    assert "a darker or more saturated brand color" in CREATE
    assert "different axes or brief" in CREATE
    lowered = CREATE.lower()
    assert "brand seed" not in lowered
    assert not re.search(r"\bmove\b[^.]*\bto a step\b", lowered)


def test_it_says_nothing_loads_the_fonts_and_names_every_family():
    for latin, arabic in PAIRINGS.values():
        assert latin in CREATE and arabic in CREATE, (latin, arabic)
    assert CODE_FACE[0] in CREATE
    assert "nothing loads them" in CREATE
    assert "Google Fonts" in CREATE and "self-hosted" in CREATE
    assert "system faces" in CREATE


def test_modes_table_marks_enhance_and_extend_for_4_1():
    modes = _section(DOC, "## Modes")
    for mode in ("enhance --from", "extend --from"):
        row = next(line for line in modes.splitlines() if mode in line)
        assert "Coming in 4.1" in row
    assert "3.x" in modes and "`/ux-system create`" in modes


def test_new_prose_has_no_em_dashes_or_double_hyphen_punctuation():
    for text in (CREATE, _section(DOC, "## Modes"),
                 _section(AGENT, "## When the 4.0 engine already built the tokens")):
        assert "—" not in text and "–" not in text
        assert not re.search(r"\s--\s", text)


def test_architect_builds_on_engine_tokens_instead_of_redefining_them():
    section = _section(AGENT, "## When the 4.0 engine already built the tokens")
    assert "uxskill system build" in section
    assert "Do not write a second token file" in section


# ------------------------------------------------ installing the beta

PINNED = f"uxskill=={__version__}"


def test_create_checks_the_version_before_it_builds():
    first = _step("### 1. ")
    assert first.startswith("### 1. Check the engine version")
    assert "uxskill --version" in first and "python3 -m engine.cli.main --version" in first
    assert CREATE.index("uxskill --version") < CREATE.index("system build --brand")
    assert f"pip install {PINNED}" in first and f"pipx install --force {PINNED}" in first
    assert "stop" in first and "do not change" in first


def test_exit_2_names_the_old_uxskill_case():
    line = next(line for line in CREATE.splitlines() if line.startswith("Exit code 2"))
    assert "No such command 'system'" in line and "step 1" in line


BETA_TEXT = {"README": README_BETA, "CHANGELOG": CHANGELOG_BETA, "create": CREATE}


@pytest.mark.parametrize("name", ["README", "CHANGELOG"])
def test_the_beta_sections_say_how_to_install_the_beta(name):
    text = BETA_TEXT[name]
    for line in ("pip install --upgrade --pre uxskill", f"pip install {PINNED}",
                 "pip install --upgrade --pre 'uxskill[mcp]'",
                 "pipx install --pip-args=--pre uxskill", "npx uxskill@beta"):
        assert line in text, (name, line)
    assert text.index("pip install --upgrade --pre uxskill") < text.index("system build"), name


# ------------------------------------------------ what the brief moves


def test_create_asks_for_an_industry_from_the_synthesizer_list():
    gather = _step("### 2. Gather the inputs")
    line = next(line for line in gather.splitlines() if line.strip().startswith("Industries:"))
    assert re.findall(r"`([a-z-]+)`", line) == sorted(INDUSTRY_SEEDS)
    assert "skip" in gather and ".ux/system-brief.json" in gather


def _ignored_discovery_words():
    words = []
    for field in FIELDS:
        if field["id"] in ("tone", "must_have"):
            words += [w.strip() for w in field["hint"].split("|")
                      if _reading(field["id"], w.strip()) is None]
    return words


def test_the_doc_names_every_discovery_word_the_engine_ignores():
    ignored = _ignored_discovery_words()
    assert "confident" in ignored and "dark-mode" in ignored
    gather = _step("### 2. Gather the inputs")
    para = next(p for p in gather.split("\n\n") if "move nothing" in p)
    assert sorted(re.findall(r"`([^`]+)`", para.split("move nothing", 1)[1].split(";")[0])) \
        == sorted(ignored)
    assert "`project_type`" in para


@pytest.mark.parametrize("name", ["README", "CHANGELOG", "create"])
def test_the_look_follows_industry_and_tone_only_when_the_brief_names_them(name):
    text = BETA_TEXT[name]
    assert "when the brief names them" in text, name
    assert "look follows your industry and tone." not in text, name


def test_no_beta_doc_says_the_mcp_tool_writes_nothing():
    assert "writes no files" not in CHANGELOG_BETA.lower()
    assert "returns the same files as text and writes nothing" not in README_BETA


def test_the_test_count_sits_in_the_beta_section_and_matches_the_badge():
    badge = re.search(r"badge/tests-(\d+)_passing", README).group(1)
    assert f"Tests **{badge} passing**" in README_BETA
    v31 = README[README.index("### New in v3.1"):README.index("### What's new in v3")]
    assert "Tests **" not in v31
