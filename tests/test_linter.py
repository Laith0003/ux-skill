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


# ---------- v2.1: lint score ----------

def test_lint_score_clean_file_is_100(tmp_path: Path):
    """A clean file scores 100."""
    f = tmp_path / "clean.html"
    f.write_text("<main><h1>Hello world</h1></main>", encoding="utf-8")
    report = lint([str(tmp_path)])
    assert report.score == 100, f"clean file should score 100, got {report.score}"


def test_lint_score_drops_with_findings(tmp_path: Path):
    """A file with AI-slop fingerprints drops below 100."""
    f = tmp_path / "slop.html"
    f.write_text(
        '<div style="background:linear-gradient(135deg,#8b5cf6,#3b82f6)">'
        '<p>Lorem ipsum dolor sit amet.</p>'
        '<span>Sign in as John Doe</span>'
        '</div>',
        encoding="utf-8",
    )
    report = lint([str(tmp_path)])
    assert report.score < 100, f"slop file should drop below 100, got {report.score}"


def test_lint_score_in_report_dict(tmp_path: Path):
    """to_dict() exposes the score so the CLI + MCP can read it."""
    f = tmp_path / "clean.html"
    f.write_text("<main><h1>Hello</h1></main>", encoding="utf-8")
    payload = lint([str(tmp_path)]).to_dict()
    assert "score" in payload
    assert payload["score"] == 100


def test_lint_score_bounded_0_to_100(tmp_path: Path):
    """Even a catastrophically bad file scores >= 0."""
    f = tmp_path / "catastrophe.html"
    bad_body = "\n".join([
        "<div style='background:linear-gradient(135deg,#8b5cf6,#3b82f6)'>",
        "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>",
        "<span>John Doe · jane.doe@example.com</span>",
        "<button>Click here</button>",
        "<img src='https://via.placeholder.com/300' alt='image'>",
        "<p>Elevate your business with our next-generation AI-powered solution.</p>",
        "</div>",
    ])
    f.write_text(bad_body, encoding="utf-8")
    report = lint([str(tmp_path)])
    assert 0 <= report.score <= 100, f"score out of bounds: {report.score}"


def test_compute_score_pure_function():
    """compute_score is callable directly with synthetic findings."""
    from engine.linter import compute_score, Finding
    fakes = [
        Finding("r1", "n1", "high", "C", "f", 1, 1, "x", "fix"),
        Finding("r2", "n2", "medium", "C", "f", 1, 1, "x", "fix"),
    ]
    # 100 - (10 + 4) = 86
    assert compute_score(fakes, files_scanned=1) == 86
    # 100 - 14/2 = 93
    assert compute_score(fakes, files_scanned=2) == 93
