"""ux_system_build: the 4.0 foundations engine over MCP. Same inputs as
`uxskill system build`. By default it returns the report and each file's
size, small enough for an agent to read; the file texts come back only
when asked, and with `out` it writes the files the way the CLI does."""
import json

import pytest

import engine.foundations.color as color_module
from engine.foundations.emit import NEUTRAL, NEUTRAL_SOURCE, make_system
from engine.mcp import TOOLS, handle_ux_system_build
from engine.mcp.server import UxSystemBuildInput
from engine.synthesizer.axes import compute_axes


def test_registered_with_its_input_model():
    handler, model, description = TOOLS["ux_system_build"]
    assert handler is handle_ux_system_build and model is UxSystemBuildInput
    assert "WCAG" in description and "out" in description and "include_files" in description
    schema = model.model_json_schema()
    assert set(schema["properties"]) == {"brand", "brief", "axes", "latin_only", "out",
                                         "include_files", "force"}


def test_returns_css_dtcg_and_report_without_writing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = handle_ux_system_build({"brand": "#3366FF", "include_files": True})
    assert result["passed"] is True and result["findings"] == []
    assert result["status"] == "built"
    expected = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert result["css"] == expected.files["tokens.css"]
    assert result["dtcg"] == expected.files["tokens.json"]
    assert result["report"] == expected.report
    assert result["gate"].startswith("WCAG gate passed: ")
    json.loads(result["dtcg"])
    json.dumps(result)
    assert list(tmp_path.iterdir()) == []


def test_brief_axes_and_latin_only():
    result = handle_ux_system_build({"brand": "3366ff", "brief": {"industry": "healthcare"},
                                     "latin_only": True})
    assert result["passed"] and result["brand"] == "#3366FF" and result["arabic"] is False
    assert result["axes"] == compute_axes({"industry": "healthcare"}).to_dict()
    assert result["axes_source"] == "from the brief (industry: healthcare)"
    assert "type-face-arabic" not in handle_ux_system_build(
        {"brand": "3366ff", "latin_only": True, "include_files": True})["css"]

    nested = handle_ux_system_build({"brand": "#3366FF",
                                     "brief": {"answers": {"industry": "healthcare"}}})
    assert nested["axes"] == result["axes"] and nested["passed"]

    result = handle_ux_system_build({"brand": "#3366FF",
                                     "axes": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]})
    assert result["passed"] and result["axes"]["type_personality"] == 0.7
    assert result["axes_source"] == "set by hand (axes)"


def test_gate_failure_returns_findings_and_no_system(monkeypatch):
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    result = handle_ux_system_build({"brand": "#FFD400", "include_files": True})
    assert result["passed"] is False and result["css"] == "" and result["dtcg"] == ""
    assert result["status"] == "failed" and result["files"] == []
    assert result["gate"].startswith("WCAG gate failed: ")
    assert result["findings"] and "Findings" in result["report"]
    assert all(set(f) == {"subject", "context", "message"} for f in result["findings"])


def test_a_failed_build_carries_the_report_with_what_to_change(monkeypatch):
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    result = handle_ux_system_build({"brand": "#FFD400"})
    report = result["report"]
    assert report.startswith("# Design system report\n\nNo design system was built for #FFD400")
    change = report.split("## What to change\n\n", 1)[1].split("\n\n")[0]
    assert "darker or more saturated brand color" in change and "brief" in change
    assert "fix each finding" not in report.lower()
    listed = report.split("## Findings\n\n", 1)[1].strip().splitlines()
    assert len(listed) == len(result["findings"])


def test_bad_inputs_return_an_error_naming_the_input():
    cases = [
        ({}, "brand is missing"),
        ({"brand": "blue"}, "brand is 'blue', which is not a hex color"),
        ({"brand": "#3366FF", "axes": [0.5]}, "axes has 1 value; pass seven numbers"),
        ({"brand": "#3366FF", "brief": "saas"}, "brief is 'saas'; pass an object"),
        ({"brand": "#3366FF", "brief": {"stack": "react"}}, "brief has none of industry"),
        ({"brand": "#3366FF", "brief": {"industry": "saas"}, "axes": [0.5] * 7},
         "both brief and axes were given; pass one"),
        ({"brand": "#3366FF", "latin_only": "maybe"},
         "latin_only is 'maybe'; pass true to leave out the Arabic face and scale"),
        ({"brand": "#3366FF", "latin_only": 1}, "latin_only is 1; pass true"),
        ({"brand": "#3366FF", "include_files": "yes"},
         "include_files is 'yes'; pass true to return the tokens.css and tokens.json text"),
        ({"brand": "#3366FF", "force": "yes"},
         "force is 'yes'; pass true to replace files in out that differ"),
        ({"brand": "#3366FF", "out": 5}, "out is 5; pass the folder to write the system into"),
        ({"brand": "#3366FF", "out": ""}, "out is missing; pass the folder"),
    ]
    for args, needle in cases:
        result = handle_ux_system_build(args)
        assert result["passed"] is False and result["status"] == "invalid", args
        assert "css" not in result and "dtcg" not in result, args
        assert needle in result["error"], (args, result["error"])


def test_the_brand_error_over_mcp_says_nothing_about_a_shell():
    for brand in (None, "blue"):
        error = handle_ux_system_build({"brand": brand})["error"]
        assert "shell" not in error and "'#3366FF'" in error, error


# ------------------------------------------------ result size and out

MCP_OUTPUT_LIMIT = 25_000  # characters an agent can take in one tool result


def test_a_default_passing_result_is_small_enough_for_an_agent():
    brief = {"industry": "saas", "tone": ["warm", "precise"], "must_have": ["dark-mode"]}
    for args in ({"brand": "#3366FF"}, {"brand": "#3366FF", "brief": brief}):
        result = handle_ux_system_build(args)
        assert result["passed"] is True and result["status"] == "built"
        assert "css" not in result and "dtcg" not in result
        text = json.dumps(result)
        assert len(text) < MCP_OUTPUT_LIMIT, len(text)
        expected = make_system("#3366FF", *(
            (NEUTRAL, NEUTRAL_SOURCE) if "brief" not in args else
            (compute_axes(brief), result["axes_source"])))
        assert result["report"] == expected.report
        assert result["files"] == [
            {"name": name, "bytes": len(expected.files[name].encode("utf-8"))}
            for name in ("tokens.json", "tokens.css", "system-report.md")]


def test_include_files_returns_the_texts():
    result = handle_ux_system_build({"brand": "#3366FF", "include_files": True})
    sizes = {f["name"]: f["bytes"] for f in result["files"]}
    assert len(result["css"].encode("utf-8")) == sizes["tokens.css"]
    assert len(result["dtcg"].encode("utf-8")) == sizes["tokens.json"]


def _cli_build(out, *args):
    from click.testing import CliRunner

    from engine.cli.main import cli
    result = CliRunner().invoke(cli, ["--no-pretty", "system", "build", "--brand", "#3366FF",
                                      *args, "--out", str(out)])
    assert result.exit_code == 0, result.output
    return result


def test_out_writes_the_same_bytes_as_the_cli(tmp_path):
    brief = {"industry": "healthcare", "tone": ["calm"]}
    brief_file = tmp_path / "brief.json"
    brief_file.write_text(json.dumps(brief), encoding="utf-8")
    _cli_build(tmp_path / "cli", "--brief", str(brief_file))
    out = tmp_path / "mcp"
    result = handle_ux_system_build({"brand": "#3366FF", "brief": brief, "out": str(out)})
    assert result["status"] == "written" and result["passed"] is True
    assert result["written"] == ["tokens.json", "tokens.css", "system-report.md"]
    assert result["unchanged"] == [] and result["conflicts"] == []
    assert "css" not in result
    for name in result["written"]:
        assert (out / name).read_bytes() == (tmp_path / "cli" / name).read_bytes(), name

    again = handle_ux_system_build({"brand": "#3366FF", "brief": brief, "out": str(out)})
    assert again["status"] == "unchanged" and again["written"] == []
    assert again["unchanged"] == ["tokens.json", "tokens.css", "system-report.md"]


def test_out_refuses_a_differing_file_without_force(tmp_path):
    handle_ux_system_build({"brand": "#3366FF", "out": str(tmp_path)})
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = handle_ux_system_build({"brand": "#AA3300", "out": str(tmp_path)})
    assert result["status"] == "refused" and result["passed"] is True
    assert result["written"] == [] and set(result["conflicts"]) == set(before)
    assert "Pass force: true to replace them, or pass a different out folder." in result["message"]
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before

    forced = handle_ux_system_build({"brand": "#AA3300", "out": str(tmp_path), "force": True})
    assert forced["status"] == "written" and forced["conflicts"] == []
    assert (tmp_path / "tokens.css").read_bytes() != before["tokens.css"]


def test_out_with_a_failing_gate_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    result = handle_ux_system_build({"brand": "#FFD400", "out": str(tmp_path / "ds")})
    assert result["status"] == "failed" and result["written"] == []
    assert result["message"].startswith("Nothing was written: the WCAG gate found")
    assert not (tmp_path / "ds").exists()


def test_out_that_cannot_be_written_is_an_error_status(tmp_path):
    (tmp_path / "ds").mkdir()
    (tmp_path / "ds" / "tokens.css").mkdir()
    result = handle_ux_system_build({"brand": "#3366FF", "out": str(tmp_path / "ds")})
    assert result["status"] == "error" and result["written"] == []
    assert "is a folder, so tokens.css cannot be written there" in result["message"]
    assert sorted(p.name for p in (tmp_path / "ds").iterdir()) == ["tokens.css"]


def test_out_reports_what_the_cli_reports(tmp_path):
    """The same run on both surfaces gives the same status and lists; only
    the words that name an input differ (a field over MCP, a flag in a
    shell)."""
    from click.testing import CliRunner

    from engine.cli.main import cli
    keys = ("status", "passed", "written", "unchanged", "conflicts")
    for brand in ("#3366FF", "#3366FF", "#AA3300"):
        run = CliRunner().invoke(cli, ["--no-pretty", "system", "build", "--brand", brand,
                                       "--out", str(tmp_path / "cli")])
        cli_payload = json.loads(run.stdout)
        mcp = handle_ux_system_build({"brand": brand, "out": str(tmp_path / "mcp")})
        assert {k: mcp[k] for k in keys} == {k: cli_payload[k] for k in keys}, brand
        assert mcp["message"].replace("force: true", "--force").replace(
            "different out", "different --out").replace(str(tmp_path / "mcp"), "X") == \
            cli_payload["message"].replace(str(tmp_path / "cli"), "X")


def _call_through_the_server(arguments, raw=False):
    """Call ux_system_build the way an MCP client does: through the
    server's tools/call handler, which checks the arguments against the
    tool's input schema before our handler sees them."""
    import asyncio

    from engine.mcp import MCP_AVAILABLE
    if not MCP_AVAILABLE:
        pytest.skip("mcp is not installed")
    from mcp import types

    from engine.mcp.server import _build_server
    server = _build_server()
    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(name="ux_system_build", arguments=arguments))
    result = asyncio.run(server.request_handlers[types.CallToolRequest](request)).root
    assert result.isError is False, result.content[0].text
    return result.content[0].text if raw else json.loads(result.content[0].text)


def test_a_junk_latin_only_reads_like_every_other_bad_input_through_the_server():
    result = _call_through_the_server({"brand": "#3366FF", "latin_only": "maybe"})
    assert result["passed"] is False and result["status"] == "invalid" and "css" not in result
    assert result["error"] == ("latin_only is 'maybe'; pass true to leave out the Arabic face "
                               "and scale, or false (the default) to keep them")


def test_latin_only_true_and_false_work_through_the_server():
    latin = _call_through_the_server({"brand": "#3366FF", "latin_only": True})
    assert latin["passed"] is True and latin["arabic"] is False
    both = _call_through_the_server({"brand": "#3366FF", "latin_only": False})
    assert both["passed"] is True and both["arabic"] is True
    assert _call_through_the_server({"brand": "#3366FF"})["arabic"] is True


def test_the_default_result_an_agent_receives_is_under_the_output_limit():
    text = _call_through_the_server({"brand": "#3366FF", "brief": {"industry": "saas"}}, raw=True)
    assert len(text) < MCP_OUTPUT_LIMIT, len(text)
    assert json.loads(text)["status"] == "built"
