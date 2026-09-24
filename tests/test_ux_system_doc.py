"""The /ux-system command doc and the architect agent must match the CLI
they tell the model to run: every flag the create mode uses exists, the
MCP tool it names exists, every status the CLI prints is in its table with
its exit code, the font families it names are the ones the engine picks,
and the 4.1 modes are marked as not yet here."""
import re
from pathlib import Path

import pytest

pytest.importorskip("click")

from engine.cli.main import cli  # noqa: E402
from engine.foundations.emit import STATUS_EXIT  # noqa: E402
from engine.foundations.typography import CODE_FACE, PAIRINGS  # noqa: E402
from engine.mcp import TOOLS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOC = (ROOT / "commands" / "ux-system.md").read_text(encoding="utf-8")
AGENT = (ROOT / "agents" / "design-system-architect.md").read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end == -1 else text[start:end]


CREATE = _section(DOC, "## create mode (4.0 beta)")


def _build_flags():
    build = cli.commands["system"].commands["build"]
    return {opt for p in build.params for opt in p.opts} | {"--no-pretty", "--pretty"}


def test_every_flag_the_create_mode_names_exists():
    used = set(re.findall(r"(?<![\w-])(--[a-z][a-z-]*)", CREATE))
    assert used, "the create section names no flags"
    assert used <= _build_flags(), sorted(used - _build_flags())


def test_the_documented_command_is_the_real_one():
    assert "uxskill --no-pretty system build --brand '#3366FF'" in CREATE
    assert "python3 -m engine.cli.main" in CREATE


def test_the_mcp_tool_it_names_exists():
    assert "ux_system_build" in CREATE and "ux_system_build" in TOOLS
    for field in ("brand", "brief", "axes", "latin_only"):
        assert f"`{field}`" in CREATE


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
