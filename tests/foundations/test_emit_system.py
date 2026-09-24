"""make_system: build, gate and report. A failing system has no files, only
findings, so no caller can write one."""
import json

import pytest

import engine.foundations.color as color_module
from engine.foundations import ValidationError, build_system, dump_dtcg, to_css
from engine.foundations.emit import (
    FILES, NEUTRAL, NEUTRAL_SOURCE, SystemFinding, make_system,
)
from engine.foundations.validate import Problem
from engine.synthesizer.axes import AxisValues


def test_passing_build_returns_all_three_files():
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert out.passed and out.findings == ()
    assert tuple(out.files) == FILES
    built = build_system(NEUTRAL, "#3366FF")
    assert out.files["tokens.json"] == dump_dtcg(built.tokens)
    assert out.files["tokens.css"] == to_css(built.tokens)
    assert out.files["system-report.md"] == out.report
    json.loads(out.files["tokens.json"])


def test_report_says_what_was_built_from_what():
    axes = AxisValues(0.2, 0.4, 0.6, 0.8, 1.0, 0.0, 0.5)
    report = make_system("#3366FF", axes, "set by hand (--axes)").report
    assert report.startswith("# Design system report\n")
    assert "Brand color: #3366FF" in report
    assert "Axes: set by hand (--axes)." in report
    assert "| density | 0.6 |" in report and "| motion | 0 |" in report
    assert "WCAG gate passed: " in report
    assert "WCAG 1.4.3 (text 4.5:1)" in report and "1.4.11 (non-text 3:1)" in report
    assert "## Notes" in report and "- type: " in report
    assert 'data-theme="dark"' in report and 'dir="rtl"' in report
    assert "Latin and Arabic" in report


def test_latin_only_is_reported_and_emits_no_arabic():
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE, arabic=False)
    assert out.passed and "Latin only" in out.report
    assert "type-face-arabic" not in out.files["tokens.css"]


def test_same_inputs_give_the_same_bytes():
    a = make_system("#6B4423", NEUTRAL, NEUTRAL_SOURCE)
    b = make_system("#6B4423", NEUTRAL, NEUTRAL_SOURCE)
    assert a.files == b.files


def test_gate_failure_returns_findings_and_no_files(monkeypatch):
    # With the action solver off, white text stays on a yellow button.
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    out = make_system("#FFD400", NEUTRAL, NEUTRAL_SOURCE)
    assert not out.passed and dict(out.files) == {}
    assert out.findings
    first = out.findings[0]
    assert first.subject == "color.text.on-action on color.action.primary"
    assert first.context == "scheme:light,contrast:standard"
    assert "WCAG 1.4.3 needs 4.5:1" in first.message
    assert "Move color.text.on-action" in first.message
    assert "WCAG gate failed: " in out.report
    assert "Nothing was written." in out.report
    for f in out.findings:
        assert f"- {f.line()}" in out.report


def test_validation_failure_returns_every_problem(monkeypatch):
    problems = [Problem("color.text.default", "semantic-literal",
                        "color.text.default holds a literal; point it at a primitive"),
                Problem("space.4", "bad-value", "space.4 is 'x'; use a dimension")]

    def broken(*args, **kwargs):
        raise ValidationError(problems)

    monkeypatch.setattr("engine.foundations.emit.build_system", broken)
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert not out.passed and dict(out.files) == {}
    assert [f.subject for f in out.findings] == ["color.text.default", "space.4"]
    assert "Validation failed: 2 problems in the token set" in out.report
    assert "- space.4 is 'x'; use a dimension" in out.report


def test_finding_line_adds_the_mode_only_when_missing():
    named = SystemFinding("a on b", "scheme:dark", "a on b (scheme:dark) is 2:1")
    bare = SystemFinding("reduced-travel", "motion:reduced", "motion.reveal.distance travels")
    anywhere = SystemFinding("color.x", "", "color.x is broken")
    assert named.line() == named.message
    assert bare.line() == "motion.reveal.distance travels (in motion:reduced)"
    assert anywhere.line() == "color.x is broken"


def test_to_dict_is_json_ready():
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    data = out.to_dict()
    assert data["passed"] is True and data["brand"] == "#3366FF"
    assert data["gate"] == out.gate and out.gate.startswith("WCAG gate passed: ")
    assert data["axes"]["warmth"] == 0.5 and data["axes_source"] == NEUTRAL_SOURCE
    assert data["findings"] == [] and data["arabic"] is True
    json.dumps(data)


@pytest.mark.parametrize("brand", ["#3366FF", "#6B4423", "#FFD400"])
def test_golden_brands_pass(brand):
    assert make_system(brand, NEUTRAL, NEUTRAL_SOURCE).passed
