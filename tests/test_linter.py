"""Linter smoke + rule-specific behavior tests."""
from pathlib import Path

from engine.linter import lint


def test_lint_empty_path(tmp_path: Path):
    """No files → no findings, exit_code 0."""
    report = lint([str(tmp_path)])
    assert report.exit_code == 0
    assert report.findings == []


def test_lint_returns_report_shape(tmp_path: Path):
    report = lint([str(tmp_path)])
    payload = report.to_dict()
    assert "findings" in payload
    assert "files_scanned" in payload
    assert "rules_loaded" in payload
    assert "summary" in payload
    assert payload["summary"]["total"] == 0


def test_rules_loaded_is_85_or_more(tmp_path: Path):
    """The deterministic linter loads from data/anti-patterns.json.

    Regression for task #61: we shipped at 68 rules, then 85. This
    smoke check makes sure a future deletion of rules doesn't slip
    through CI."""
    (tmp_path / "blank.css").write_text("/* empty */", encoding="utf-8")
    report = lint([str(tmp_path)])
    assert report.rules_loaded >= 85, (
        f"Expected >= 85 rules loaded (we shipped at 85 in alpha.44); "
        f"got {report.rules_loaded}"
    )


def test_lint_catches_purple_blue_gradient(tmp_path: Path):
    """The signature AI-design fingerprint must fire."""
    css = tmp_path / "slop.css"
    css.write_text(
        ".hero { background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); }",
        encoding="utf-8",
    )
    report = lint([str(tmp_path)])
    fired_ids = {f.rule_id for f in report.findings}
    # at least one gradient-related rule should fire
    assert any("gradient" in fid or "purple" in fid for fid in fired_ids), (
        f"No gradient/purple rule fired on a textbook purple-to-blue gradient. "
        f"Rules that fired: {sorted(fired_ids)}"
    )


def test_lint_catches_lorem_ipsum(tmp_path: Path):
    """Placeholder copy fingerprint must fire."""
    html = tmp_path / "filler.html"
    html.write_text(
        "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>",
        encoding="utf-8",
    )
    report = lint([str(tmp_path)])
    fired_ids = {f.rule_id for f in report.findings}
    assert any("lorem" in fid or "placeholder" in fid for fid in fired_ids), (
        f"Lorem ipsum didn't fire any rule. Rules that fired: {sorted(fired_ids)}"
    )


def test_lint_catches_johndoe_placeholder(tmp_path: Path):
    """John Doe / Jane Doe fingerprint must fire (added in round 4)."""
    html = tmp_path / "names.html"
    html.write_text(
        '<div>Sign in as <span>John Doe</span></div>',
        encoding="utf-8",
    )
    report = lint([str(tmp_path)])
    fired_ids = {f.rule_id for f in report.findings}
    assert any("doe" in fid or "placeholder" in fid for fid in fired_ids), (
        f"John Doe didn't fire any rule. Rules that fired: {sorted(fired_ids)}"
    )


def test_lint_severity_threshold(tmp_path: Path):
    """A clean file should exit 0 at every threshold."""
    f = tmp_path / "clean.html"
    f.write_text("<main><h1>Hello</h1></main>", encoding="utf-8")
    for threshold in ("low", "medium", "high", "critical"):
        report = lint([str(tmp_path)], severity_threshold=threshold)
        # clean file means no findings AT OR ABOVE the threshold
        assert report.exit_code == 0, f"clean file failed at threshold {threshold!r}"
