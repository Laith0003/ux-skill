"""ux_system_build: the 4.0 foundations engine over MCP. Same inputs as
`uxskill system build`, returns text instead of writing files."""
import json

import engine.foundations.color as color_module
from engine.foundations.emit import NEUTRAL, NEUTRAL_SOURCE, make_system
from engine.mcp import TOOLS, handle_ux_system_build
from engine.mcp.server import UxSystemBuildInput
from engine.synthesizer.axes import compute_axes


def test_registered_with_its_input_model():
    handler, model, description = TOOLS["ux_system_build"]
    assert handler is handle_ux_system_build and model is UxSystemBuildInput
    assert "WCAG" in description and "Writes no files" in description
    schema = model.model_json_schema()
    assert set(schema["properties"]) == {"brand", "brief", "axes", "latin_only"}


def test_returns_css_dtcg_and_report_without_writing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = handle_ux_system_build({"brand": "#3366FF"})
    assert result["passed"] is True and result["findings"] == []
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
    assert "type-face-arabic" not in result["css"]

    nested = handle_ux_system_build({"brand": "#3366FF",
                                     "brief": {"answers": {"industry": "healthcare"}}})
    assert nested["axes"] == result["axes"] and nested["passed"]

    result = handle_ux_system_build({"brand": "#3366FF",
                                     "axes": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]})
    assert result["passed"] and result["axes"]["type_personality"] == 0.7
    assert result["axes_source"] == "set by hand (axes)"


def test_gate_failure_returns_findings_and_no_system(monkeypatch):
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    result = handle_ux_system_build({"brand": "#FFD400"})
    assert result["passed"] is False and result["css"] == "" and result["dtcg"] == ""
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
    ]
    for args, needle in cases:
        result = handle_ux_system_build(args)
        assert result["passed"] is False and result["css"] == "", args
        assert needle in result["error"], (args, result["error"])
