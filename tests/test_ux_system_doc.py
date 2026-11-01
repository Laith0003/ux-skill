"""The /ux-system command doc and the architect agent must match the CLI
they tell the model to run: every flag the create mode uses exists, the
MCP tool it names exists, every status the CLI prints is in its table with
its exit code, the font families it names are the ones the engine picks,
and the existing-system modes say what works now, with no version label. The README and CHANGELOG
4.0 sections tell a reader how to install the release, and no doc promises a
brief word the synthesizer does not read."""
import json
import re
from pathlib import Path

import pytest

pytest.importorskip("click")

from engine.cli.main import cli  # noqa: E402
from engine.discovery.core import FIELDS  # noqa: E402
from engine.foundations.emit import STATUS_EXIT, _reading  # noqa: E402
from engine.foundations.fonts import FACES  # noqa: E402
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


CREATE = _section(DOC, "## create mode")


def _step(heading: str) -> str:
    """One numbered step of the create mode, up to the next step."""
    start = CREATE.index(heading)
    end = CREATE.find("\n### ", start + len(heading))
    return CREATE[start:] if end == -1 else CREATE[start:end]


README_40 = README[README.index("### New in 4.0: foundations"):README.index("### New in v3.1")]
CHANGELOG_40 = CHANGELOG[CHANGELOG.index("## [4.0.0]"):CHANGELOG.index("## [3.2.0]")]
# The 4.0.0 entry alone, without the beta notes below it.
CHANGELOG_RELEASE = CHANGELOG_40[:CHANGELOG_40.index("## [4.0.0-beta.1]")]


def _build_flags():
    """The flags of `system build`, and of `system detect`, which step 3 runs first."""
    flags = {"--no-pretty", "--pretty"}
    for name in ("build", "detect"):
        command = cli.commands["system"].commands[name]
        flags |= {opt for p in command.params for opt in p.opts}
    return flags


def test_every_flag_the_create_mode_names_exists():
    # A CSS custom property read with var() is not a flag.
    used = set(re.findall(r"(?<![\w(-])(--[a-z][a-z-]*)", CREATE))
    assert used, "the create section names no flags"
    # --version belongs to uxskill itself, which the first step runs.
    assert "--version" in {opt for p in cli.params for opt in p.opts}
    used.discard("--version")
    # --upgrade belongs to pip, in the install line the first step gives.
    used.discard("--upgrade")
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
    for face in FACES:
        assert face.family in CREATE, face.family
    assert "nothing loads the faces" in CREATE and "link `fonts.css` before `tokens.css`" in CREATE
    assert "Google Fonts" in CREATE and "self-hosted" in CREATE
    assert "system faces" in CREATE


def test_the_existing_system_modes_point_at_their_sections():
    modes = _section(DOC, "## Modes")
    for mode, section in (("enhance --from", "enhance mode"), ("extend --from", "extend mode")):
        row = next(line for line in modes.splitlines() if mode in line)
        assert f'"{section}"' in row, row
        assert "4.1" not in row and "being added" not in row and "Coming in" not in row
    assert "4.1" not in modes and "does not read an existing one" not in DOC
    assert "3.x" in modes and "`/ux-system create`" in modes
    existing = _section(DOC, "## An existing system")
    for part in ("system detect", "read_any", "propose", "merge", "scan", "enhance", "extension file"):
        assert part in existing, part
    for fmt in ("`dtcg`", "`css`", "`tailwind`", "`tailwind-json`", "`markdown`", "`figma`"):
        assert fmt in existing, fmt
    assert "\u2014" not in existing and "\u2013" not in existing


ENHANCE = _section(DOC, "## enhance mode")
EXTEND = _section(DOC, "## extend mode")
IO_TOOLS = ("ux_system_import", "ux_system_enhance", "ux_system_extend", "ux_system_export",
            "ux_contracts_check")


def _io_flags():
    system = cli.commands["system"]
    names = ("import", "enhance", "extend", "export", "detect")
    flags = {opt for n in names for p in system.commands[n].params for opt in p.opts}
    check = cli.commands["contracts"].commands["check"]
    return flags | {opt for p in check.params for opt in p.opts} | {"--no-pretty", "--help"}


def test_every_flag_the_enhance_and_extend_modes_name_exists():
    used = set(re.findall(r"(?<![\w(-])(--[a-z][a-z-]*)", ENHANCE + EXTEND))
    assert {"--from", "--mapping", "--scan", "--out", "--add", "--add-role", "--to",
            "--brief", "--scheme", "--contract", "--force", "--format",
            "--figma-mode"} <= used
    assert used <= _io_flags(), sorted(used - _io_flags())


def test_the_commands_and_tools_they_name_are_the_real_ones():
    for command in ("uxskill --no-pretty system import --from",
                    "uxskill --no-pretty system enhance --from",
                    "uxskill --no-pretty system extend --from",
                    "uxskill --no-pretty system export --from",
                    "uxskill --no-pretty contracts check"):
        assert command in ENHANCE + EXTEND, command
    for tool in IO_TOOLS:
        assert f"`{tool}`" in ENHANCE + EXTEND and tool in TOOLS, tool


def test_the_mcp_fields_they_name_are_the_tools_fields():
    from engine.mcp.server import (
        UxContractsCheckInput, UxSystemExportInput, UxSystemExtendInput)
    fields = {f for model in (UxSystemExtendInput, UxSystemExportInput, UxContractsCheckInput)
              for f in model.model_json_schema()["properties"]}
    named = set(re.findall(r"`([a-z_]+)`", _paragraph(ENHANCE + EXTEND, "Over MCP")))
    named -= set(IO_TOOLS) | {"invalid"}
    assert named and named <= fields, sorted(named - fields)


def _paragraph(text, start):
    return "\n".join(p for p in text.split("\n\n") if p.startswith(start))


def test_the_io_status_table_matches_the_exit_codes():
    from engine.io.commands import EXIT
    rows = re.findall(r"^\| `([a-z]+)` \| (\d) \|", ENHANCE, re.M)
    assert dict(rows) == {status: str(code) for status, code in EXIT.items()}
    assert "`invalid`" in ENHANCE and "Exit code 2" in ENHANCE


def test_extend_names_the_brief_fields_the_font_files_and_the_phone_styles():
    from engine.foundations.audience import FIELDS
    assert all(f"`{name}`" in EXTEND for name in FIELDS)
    assert "fonts.css" in EXTEND and "fonts-self-host.css" in EXTEND
    assert "`text-hero-phone`" in EXTEND and "imagery" in EXTEND


def test_the_modes_say_what_works_now():
    text = ENHANCE + EXTEND
    for part in ("Measure before defining", "never rewrites", "theme-ext.css", "tokens-ext.json",
                 "rewritten in place", ".uxskill/files.json", ".uxskill/backup/",
                 "Tailwind 4", "Figma", "high-contrast", "several files",
                 '{"token": null, "by": "owner"}', '"fields"', "prefix",
                 "Do not pass --force", "Decisions made without you"):
        assert part in text, part


EXT_SOURCES = {
    "css": ("theme.css", ":root { --ink: #1b1d22; --paper: #fdfdfb; }\n"),
    "tailwind": ("app.css", "@theme {\n  --color-ink: #1b1d22;\n  --color-paper: #fdfdfb;\n}\n"),
    "dtcg": ("brand.json", '{"ink": {"$type": "color", "$value": "#1b1d22"}, '
                           '"paper": {"$type": "color", "$value": "#fdfdfb"}}'),
    "tailwind-json": ("tailwind-theme.json", '{"colors": {"ink": "#1b1d22", "paper": "#fdfdfb"}}'),
    "markdown": ("DESIGN.md", "# Tokens\n\n| Token | Value |\n|---|---|\n| ink | #1b1d22 |\n"
                              "| paper | #fdfdfb |\n"),
    "figma": ("variables.json", json.dumps({"meta": {
        "variableCollections": {"c:1": {"id": "c:1", "name": "Color", "defaultModeId": "m:1",
                                        "modes": [{"modeId": "m:1", "name": "Light"}],
                                        "variableIds": ["v:1"]}},
        "variables": {"v:1": {"id": "v:1", "name": "ink", "variableCollectionId": "c:1",
                              "resolvedType": "COLOR",
                              "valuesByMode": {"m:1": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1}},
                              "scopes": ["ALL_SCOPES"], "description": "",
                              "hiddenFromPublishing": False, "remote": False}}}})),
}


def test_the_extension_file_the_doc_names_is_the_one_extend_writes(tmp_path):
    from engine.io import FORMATS
    from engine.io.commands import run_extend
    rows = dict(re.findall(r"^  \| `([a-z-]+)` \| (.+?) \|$", EXTEND, re.M))
    assert set(rows) == set(FORMATS) == set(EXT_SOURCES)
    for fmt, (name, text) in EXT_SOURCES.items():
        folder = tmp_path / fmt
        folder.mkdir()
        (folder / name).write_text(text, encoding="utf-8")
        result = run_extend(str(folder / name), out=str(folder / "out"), add=["radius"])
        assert result["status"] == "written" and result["format"] == fmt, (fmt, result)
        named = {n.replace("<name>", Path(name).stem)
                 for n in re.findall(r"`([^`]+-ext\.[a-z]+)`", rows[fmt])}
        beside = {p.name for p in folder.iterdir()} - {name, "out", ".uxskill"}
        assert named and beside == named, (fmt, beside, named)


def test_the_modes_carry_no_version_label_and_no_measured_example():
    text = ENHANCE + EXTEND
    assert "4.1" not in text and "(4." not in text
    assert "eleven ways" not in text and "11 ways" not in text
    assert not re.search(r"\bM4|\bR\d|ruling", text)


def test_ux_design_points_a_gap_at_extend():
    design = (ROOT / "commands" / "ux-design.md").read_text(encoding="utf-8")
    step = design[design.index("### 1a. An existing design system"):design.index("### 1a.1.")]
    assert "/ux-system extend --from" in step and "theme-ext.css" in step


def test_the_readme_says_the_existing_system_modes_work():
    assert "does not read an existing one yet" not in README
    assert f"{len(TOOLS)} MCP tools" in README
    assert "/ux-system enhance --from" in README and "/ux-system extend --from" in README


def test_the_readers_the_doc_names_are_the_engines():
    from engine import io
    existing = _section(DOC, "## An existing system")
    for name in ("read_any", "propose", "merge", "dump_mapping", "scan", "enhance"):
        assert f"engine.io.{name}(" in existing and hasattr(io, name), name
    for fmt in io.FORMATS:
        assert f"`{fmt}`" in existing, fmt


def test_new_prose_has_no_em_dashes_or_double_hyphen_punctuation():
    for text in (CREATE, _section(DOC, "## Modes"), ENHANCE, EXTEND,
                 _section(AGENT, "## When the 4.0 engine already built the tokens")):
        assert "—" not in text and "–" not in text
        assert not re.search(r"\s--\s", text)


def test_architect_builds_on_engine_tokens_instead_of_redefining_them():
    section = _section(AGENT, "## When the 4.0 engine already built the tokens")
    assert "uxskill system build" in section
    assert "Do not write a second token file" in section


def test_create_mode_offers_the_rule_pack_off_by_default():
    run = _step("### 4. Run the engine")
    assert "`--rule-pack`" in run and "off by default" in run
    assert "design-system/rule-pack/" in run
    assert "`rule-pack/README.md`" in _step("### 6. Tell the user what they got, in plain words")
    assert "`rule-pack/` folder" in _step("### 3. Look before writing")


def test_create_mode_says_a_pack_goes_stale_without_the_flag():
    look = _step("### 3. Look before writing")
    assert "`--rule-pack` again" in look and "stale" in look and "rule-pack/built-from.json" in look
    run = _step("### 4. Run the engine")
    assert "all checked against the tokens" not in run
    assert "which names the files to load for each task" in \
        _step("### 6. Tell the user what they got, in plain words")


def test_architect_authors_contracts_at_experimental_and_reads_decisions_first():
    from engine.contracts.schema import RTL_BEHAVIORS
    section = _section(AGENT, "## When the 4.0 engine already built the tokens")
    assert "`rule-pack/README.md`" in section
    assert "`status: experimental`" in section and "never set `ready`" in section
    assert all(b in section for b in RTL_BEHAVIORS)
    assert "`rule-pack/decisions/`" in section


# ------------------------------------------------ installing the release


def test_create_checks_the_version_before_it_builds():
    first = _step("### 1. ")
    assert first.startswith("### 1. Check the engine version")
    assert "uxskill --version" in first and "python3 -m engine.cli.main --version" in first
    assert CREATE.index("uxskill --version") < CREATE.index("system build --brand")
    assert "pip install --upgrade uxskill" in first and "pipx upgrade uxskill" in first
    assert "uxskill 4.0.0 or later" in first
    assert "pre-release" not in first and "--pre" not in first
    assert "stop" in first and "do not change" in first


def test_exit_2_names_the_old_uxskill_case():
    line = next(line for line in CREATE.splitlines() if line.startswith("Exit code 2"))
    assert "No such command 'system'" in line and "step 1" in line


TEXT_40 = {"README": README_40, "CHANGELOG": CHANGELOG_40, "create": CREATE}
RELEASE_TEXT = {"README": README_40, "CHANGELOG": CHANGELOG_RELEASE}


@pytest.mark.parametrize("name", ["README", "CHANGELOG"])
def test_the_release_sections_say_how_to_install_the_release(name):
    text = RELEASE_TEXT[name]
    for line in ("pip install --upgrade uxskill", "pip install --upgrade 'uxskill[mcp]'",
                 "npx uxskill@latest"):
        assert line in text, (name, line)
    assert text.index("pip install --upgrade uxskill") < text.index("system build"), name


@pytest.mark.parametrize("name", ["README", "CHANGELOG"])
def test_the_release_sections_send_no_one_to_a_pre_release(name):
    text = RELEASE_TEXT[name]
    for word in ("--pre", "@beta", "4.0.0b1", "pre-release"):
        assert word not in text, (name, word)


# ------------------------------------------------ what the brief moves


def test_create_asks_for_an_industry_from_the_synthesizer_list():
    gather = _step("### 2. Gather the inputs")
    line = next(line for line in gather.splitlines() if line.strip().startswith("Industries:"))
    assert re.findall(r"`([a-z0-9-]+)`", line) == sorted(INDUSTRY_SEEDS)
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
    text = TEXT_40[name]
    assert "when the brief names them" in text, name
    assert "look follows your industry and tone." not in text, name


def test_no_beta_doc_says_the_mcp_tool_writes_nothing():
    assert "writes no files" not in CHANGELOG_40.lower()
    assert "returns the same files as text and writes nothing" not in README_40


def test_the_test_count_sits_in_the_beta_section_and_matches_the_badge():
    badge = re.search(r"badge/tests-(\d+)_passing", README).group(1)
    assert f"Tests **{badge} passing**" in README_40
    v31 = README[README.index("### New in v3.1"):README.index("### What's new in v3")]
    assert "Tests **" not in v31
