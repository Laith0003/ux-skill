"""The MCP tools for a system a project already has: ux_system_import,
ux_system_enhance, ux_system_extend, ux_system_export and
ux_contracts_check. Plain dict handlers over engine.io.commands, which the
CLI shares: small results (counts, statuses, problems, the report text),
file texts only on request, absolute paths only, and a bad input as status
invalid naming the field by its MCP name and the fix."""
import re
from pathlib import Path

from engine.contracts.library import SEED_DIR
from engine.foundations.build import build_system
from engine.foundations.export import dump_dtcg
from engine.io.commands import EXIT
from engine.mcp import TOOLS
from engine.mcp.server import (
    UxSystemExtendInput, UxSystemImportInput, handle_ux_contracts_check,
    handle_ux_system_enhance, handle_ux_system_export, handle_ux_system_extend,
    handle_ux_system_import)
from engine.synthesizer.axes import AxisValues

THEME = ":root { --ink: #1b1d22; --paper: #fdfdfb; --text-body: var(--ink); }\n"
DARK = ("@media (prefers-color-scheme: dark) { :root { --ink: #f2f2ee; --paper: #15171b; } }\n")
NAMES = ("ux_system_import", "ux_system_enhance", "ux_system_extend", "ux_system_export",
         "ux_contracts_check")


def _theme(tmp_path: Path) -> str:
    f = tmp_path / "theme.css"
    f.write_text(THEME, encoding="utf-8")
    return str(f)


def _tokens(tmp_path: Path) -> str:
    f = tmp_path / "tokens.json"
    f.write_text(dump_dtcg(build_system(AxisValues(*[0.5] * 7), "#3366FF").tokens),
                 encoding="utf-8")
    return str(f)


def test_the_tools_are_registered_with_short_plain_descriptions():
    for name in NAMES:
        handler, model, description = TOOLS[name]
        assert callable(handler) and model.model_json_schema()["properties"]
        assert len(description) < 600, name
        assert "4.1" not in description and "\u2014" not in description, name
        assert not re.search(r"\s--\s", description), name


def test_the_format_field_lists_every_format_the_readers_take():
    from engine.io import CHOICES
    text = UxSystemImportInput.model_json_schema()["properties"]["format"]["description"]
    assert all(fmt in text for fmt in CHOICES), text
    assert "tailwind-json" in text and "auto" in text


def test_import_returns_counts_and_the_report_not_every_entry(tmp_path):
    result = handle_ux_system_import({"source": _theme(tmp_path)})
    assert result["status"] == "read" and result["tokens"] == 3
    assert result["not_read"] == 0 and isinstance(result["not_read"], int)
    assert "not_read_count" not in result and result["report"]
    assert "texts" not in result


def test_import_with_out_writes_the_report_and_mapping(tmp_path):
    out = tmp_path / "intake"
    result = handle_ux_system_import({"source": _theme(tmp_path), "out": str(out)})
    assert result["status"] == "written"
    assert (out / "import-report.md").is_file() and (out / "mapping.json").is_file()
    assert Path(result["source"]["path"]).is_absolute()


def test_import_reads_several_sources_as_one_system(tmp_path):
    dark = tmp_path / "dark.css"
    dark.write_text(DARK, encoding="utf-8")
    result = handle_ux_system_import({"source": [_theme(tmp_path), str(dark)]})
    assert result["status"] == "read" and len(result["also_read"]) == 1
    assert result["mode_values"] > 0


def test_enhance_scans_and_writes_only_with_out(tmp_path):
    code = tmp_path / "code"
    code.mkdir()
    (code / "a.css").write_text(".x { color: var(--text-body); }\n", encoding="utf-8")
    result = handle_ux_system_enhance({"source": _theme(tmp_path), "scan": [str(code)]})
    assert result["status"] == "reported" and result["summary"]["unused"] == 1
    assert not (tmp_path / "enhance-report.md").exists()
    out = tmp_path / "out"
    written = handle_ux_system_enhance({"source": _theme(tmp_path), "out": str(out)})
    assert written["status"] == "written" and (out / "enhance-report.md").is_file()


def test_extend_writes_an_extension_beside_a_foreign_source(tmp_path):
    source = _theme(tmp_path)
    out = tmp_path / "out"
    result = handle_ux_system_extend({"source": source, "add": ["radius"], "out": str(out)})
    assert result["status"] == "written", result.get("message")
    assert (tmp_path / "theme-ext.css").is_file() and (out / "extend-report.md").is_file()
    assert Path(source).read_text(encoding="utf-8") == THEME
    assert (out / ".uxskill" / "files.json").is_file()


def test_extend_names_the_brief_fields_and_reads_them(tmp_path):
    from engine.foundations.audience import FIELDS
    text = UxSystemExtendInput.model_json_schema()["properties"]["brief"]["description"]
    assert all(name in text for name in FIELDS)
    assert "imagery" in UxSystemExtendInput.model_json_schema()["properties"]["add"][
        "description"]
    result = handle_ux_system_extend({"source": _theme(tmp_path), "add": ["type"],
                                      "brief": {"primary_script": "arabic"},
                                      "latin_only": True, "out": str(tmp_path / "out")})
    assert result["status"] == "invalid"
    assert result["error"] == ("latin_only leaves Arabic out, but the brief's primary_script "
                               "is arabic; drop latin_only, or set primary_script to latin")


def test_extend_needs_out(tmp_path):
    result = handle_ux_system_extend({"source": _theme(tmp_path), "add": ["radius"]})
    assert result["status"] == "invalid" and result["error"].startswith("out is missing")


def test_export_returns_texts_only_on_request(tmp_path):
    tokens = _tokens(tmp_path)
    small = handle_ux_system_export({"source": tokens, "to": "tailwind"})
    assert small["status"] == "built" and "texts" not in small
    assert small["files"][0]["name"] == "tailwind-theme.css" and small["files"][0]["bytes"] > 0
    full = handle_ux_system_export({"source": tokens, "to": "tailwind", "include_files": True})
    assert "@theme" in full["texts"]["tailwind-theme.css"]
    dark = handle_ux_system_export({"source": tokens, "to": "css", "scheme": "dark",
                                    "include_files": True})
    assert ':root:not([data-theme="light"]) {' in dark["texts"]["tokens.css"]
    bad = handle_ux_system_export({"source": tokens, "to": "css", "scheme": "dim"})
    assert bad == {"status": "invalid", "error": "scheme is dim; pass light, dark or system"}


def test_export_with_out_writes_and_never_touches_the_source(tmp_path):
    tokens = _tokens(tmp_path)
    before = Path(tokens).read_bytes()
    out = tmp_path / "export"
    result = handle_ux_system_export({"source": tokens, "to": "figma", "out": str(out)})
    assert result["status"] == "written"
    assert Path(tokens).read_bytes() == before and any(out.iterdir())


def test_the_contract_check(tmp_path):
    result = handle_ux_contracts_check({"folder": str(SEED_DIR), "tokens": _tokens(tmp_path)})
    assert result["status"] == "passed"
    assert len(result["contracts"]) == len(list(SEED_DIR.glob("*.yaml")))


def test_every_status_the_tools_return_is_one_the_cli_knows(tmp_path):
    theme, tokens, out = _theme(tmp_path), _tokens(tmp_path), str(tmp_path / "o")
    runs = [
        handle_ux_system_import({"source": theme}),
        handle_ux_system_import({}),
        handle_ux_system_enhance({"source": theme}),
        handle_ux_system_enhance({"source": theme, "sourse": 1}),
        handle_ux_system_extend({"source": theme, "add": ["motion"], "out": out}),
        handle_ux_system_extend({"source": theme, "add": ["motion"], "out": out}),
        handle_ux_system_extend({"source": theme, "add": ["nothing"], "out": out}),
        handle_ux_system_export({"source": tokens, "to": "css"}),
        handle_ux_system_export({"source": tokens, "to": "css", "out": str(tmp_path / "e")}),
        handle_ux_system_export({"source": tokens}),
    ]
    # "invalid" is the tools' bad-input status, which the command line
    # reports as a usage error before any command runs; it always names
    # the input in "error".
    statuses = {r["status"] for r in runs}
    assert statuses - {"invalid"} <= set(EXIT), statuses - set(EXIT)
    assert {"invalid", "written", "unchanged", "read"} <= statuses, statuses
    assert all(r["error"] for r in runs if r["status"] == "invalid")


def test_bad_inputs_are_invalid_and_name_the_field(tmp_path):
    relative = handle_ux_system_import({"source": "theme.css"})
    assert relative["status"] == "invalid"
    assert relative["error"] == (
        "source is 'theme.css', a relative path; the MCP server runs in its own folder, so "
        "pass an absolute path, for example /Users/you/project/theme.css")
    one_relative = handle_ux_system_import({"source": [_theme(tmp_path), "dark.css"]})
    assert one_relative["status"] == "invalid" and one_relative["error"].startswith(
        "source is 'dark.css', a relative path")
    missing = handle_ux_system_import({})
    assert missing["status"] == "invalid" and missing["error"].startswith("source is missing")
    no_to = handle_ux_system_export({"source": _tokens(tmp_path)})
    assert no_to["status"] == "invalid" and no_to["error"].startswith("to is missing")
    role = handle_ux_system_extend({"source": _theme(tmp_path), "add_role": ["ink"],
                                    "out": str(tmp_path / "o")})
    assert role["status"] == "invalid"
    assert role["error"].startswith("add_role ink needs the form role=token")
    scan = handle_ux_system_enhance({"source": _theme(tmp_path), "scan": ["src"]})
    assert scan["status"] == "invalid" and scan["error"].startswith("scan is 'src', a relative")
    force = handle_ux_system_import({"source": _theme(tmp_path), "force": "maybe"})
    assert force["status"] == "invalid" and "force" in force["error"]
    modes = handle_ux_system_import({"source": _theme(tmp_path), "figma_modes": "SM"})
    assert modes["status"] == "invalid" and modes["error"].startswith("figma_modes is 'SM'")


def test_a_bad_format_is_named_by_its_mcp_field(tmp_path):
    unknown = handle_ux_system_import({"source": _theme(tmp_path), "format": "yaml"})
    assert unknown["status"] == "invalid" and unknown["error"].startswith("format is yaml;")
    assert "tailwind-json" in unknown["error"]
    wrong = handle_ux_system_import({"source": _theme(tmp_path), "format": "dtcg"})
    assert wrong["status"] == "invalid"
    assert wrong["error"] == ("format dtcg reads JSON and theme.css is a stylesheet; pass "
                              "format css or tailwind, or leave format out")
    assert "--" not in unknown["error"] + wrong["error"]


def test_extend_names_add_and_add_role_by_their_fields(tmp_path):
    source, out = _theme(tmp_path), str(tmp_path / "out")
    cases = (({"add": ["shadow"]}, "add names shadow"),
             ({"add_role": ["color.nope=ink"]}, "add_role names color.nope"),
             ({"add_role": ["color.focus.ring=hb-nope"]},
              "add_role points color.focus.ring at hb-nope"))
    for extra, start in cases:
        result = handle_ux_system_extend({"source": source, "out": out, **extra})
        assert result["status"] == "invalid", result
        assert result["error"].startswith(start), result["error"]
        assert "--" not in result["error"], result["error"]


def test_the_contract_check_result_stays_small_on_a_foreign_system(tmp_path):
    import json
    result = handle_ux_contracts_check({"folder": str(SEED_DIR), "tokens": _theme(tmp_path)})
    assert result["status"] == "failed" and "lines" not in result
    assert result["problems_total"] > 100
    assert sum(result["by_rule"].values()) == result["problems_total"]
    assert sum(p["count"] for p in result["problems"]) + result["problems_omitted"] \
        == result["problems_total"]
    assert len(result["problems"]) <= 40
    assert len(json.dumps(result)) < 20000
    assert all("--" not in n for n in result["notes"])
    assert "ux_system_import" in " ".join(result["notes"])


def test_missing_folders_and_contracts_are_invalid(tmp_path):
    folder = handle_ux_contracts_check({"folder": str(tmp_path / "nope"),
                                        "tokens": _tokens(tmp_path)})
    assert folder["status"] == "invalid" and folder["error"].startswith("folder ")
    contract = handle_ux_system_extend({"source": _theme(tmp_path), "out": str(tmp_path / "o"),
                                        "contracts": [str(tmp_path / "chip.yaml")]})
    assert contract["status"] == "invalid" and contract["error"].startswith("contracts ")


def test_a_second_identical_extend_is_unchanged(tmp_path):
    args = {"source": _theme(tmp_path), "add": ["radius"], "out": str(tmp_path / "out")}
    assert handle_ux_system_extend(args)["status"] == "written"
    ext = (tmp_path / "theme-ext.css").read_text(encoding="utf-8")
    again = handle_ux_system_extend(args)
    assert again["status"] == "unchanged", again.get("message")
    assert (tmp_path / "theme-ext.css").read_text(encoding="utf-8") == ext
    assert not re.search(r"\{\s*\}", ext)


def test_a_single_markdown_file_can_be_written(tmp_path):
    md = tmp_path / "DESIGN.md"
    md.write_text("# Tokens\n\n| Token | Value |\n|---|---|\n| ink | #1b1d22 |\n"
                  "| paper | #fdfdfb |\n", encoding="utf-8")
    out = tmp_path / "intake"
    result = handle_ux_system_import({"source": str(md), "out": str(out)})
    assert result["status"] == "written", result.get("message")
    extended = handle_ux_system_extend({"source": str(md), "add": ["radius"],
                                        "out": str(out)})
    assert extended["status"] == "written", extended.get("message")
    assert (tmp_path / "tokens-ext.json").is_file()


def test_a_second_identical_extend_is_unchanged_on_the_command_line(tmp_path):
    import json
    from click.testing import CliRunner
    from engine.cli.main import cli
    args = ["--no-pretty", "system", "extend", "--from", _theme(tmp_path), "--add", "radius",
            "--out", str(tmp_path / "out")]
    first = CliRunner().invoke(cli, args)
    assert first.exit_code == 0 and json.loads(first.output)["status"] == "written"
    again = CliRunner().invoke(cli, args)
    assert again.exit_code == 0, again.output
    assert json.loads(again.output)["status"] == "unchanged"


def test_an_unknown_field_is_reported_never_ignored(tmp_path):
    # A misspelled scan would otherwise give a report that measured no code.
    result = handle_ux_system_enhance({"source": _theme(tmp_path), "scna": [str(tmp_path)]})
    assert result["status"] == "invalid"
    assert result["error"].startswith("scna is not a field of ux_system_enhance; did you mean "
                                      "scan? use source, format, out, force, figma_modes, "
                                      "mapping or scan, or leave it out")
    for handler, name in ((handle_ux_system_import, "ux_system_import"),
                          (handle_ux_system_export, "ux_system_export"),
                          (handle_ux_system_extend, "ux_system_extend"),
                          (handle_ux_contracts_check, "ux_contracts_check")):
        got = handler({"source": _theme(tmp_path), "bogus": 1, "to": "css"})
        assert got["status"] == "invalid" and f"is not a field of {name}" in got["error"]


def test_the_report_asks_for_code_in_words_both_callers_read(tmp_path):
    result = handle_ux_system_enhance({"source": _theme(tmp_path)})
    assert "(--scan on the command line, scan in the MCP tool)" in result["report"]
