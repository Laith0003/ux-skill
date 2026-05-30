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


# --- Linter precision (dogfood fix): two rules flagged correct, conformant code.
# --- Both-direction tests: correct code must NOT flag; real violations MUST flag.

def test_skip_link_with_class_not_flagged(tmp_path):
    f = tmp_path / "ok.html"
    f.write_text(
        '<a class="skip-link" href="#main">Skip to content</a>\n'
        '<a href="#main" class="skip-link">Skip to content</a>',
        encoding="utf-8")
    findings = lint([str(f)]).to_dict()["findings"]
    assert not [x for x in findings if x["rule_id"] == "screen-reader-only-without-class"]


def test_skip_link_without_class_still_flagged(tmp_path):
    f = tmp_path / "bad.html"
    f.write_text('<a href="#main">Skip to content</a>', encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "screen-reader-only-without-class" in ids


def test_glass_blur_with_fallback_not_flagged(tmp_path):
    f = tmp_path / "ok.css"
    f.write_text('.h { backdrop-filter: blur(10px); background: rgba(255,255,255,0.82); }',
                 encoding="utf-8")
    findings = lint([str(f)]).to_dict()["findings"]
    assert not [x for x in findings if x["rule_id"] == "blur-bg-only-decoration"]


def test_blur_without_fallback_still_flagged(tmp_path):
    f = tmp_path / "bad.css"
    f.write_text('.x { backdrop-filter: blur(10px); }', encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "blur-bg-only-decoration" in ids


# --- P4: picsum rule narrowed to random/unseeded only (both-direction) ---

def test_random_picsum_still_flagged(tmp_path):
    """A random/unseeded picsum URL is the tell — must fire."""
    f = tmp_path / "rnd.html"
    f.write_text(
        '<body><section><img src="https://picsum.photos/200/300" alt="x">'
        '</section></body>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "picsum-photos-seed" in ids


def test_seeded_picsum_not_flagged(tmp_path):
    """A SEEDED picsum URL is stable and on the curated path — must NOT fire."""
    f = tmp_path / "seeded.html"
    f.write_text(
        '<body><section><img src="https://picsum.photos/seed/cafe-counter/1600/900"'
        ' alt="cafe"></section></body>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "picsum-photos-seed" not in ids


# --- P4: imagery-mandatory (no imagery on a full page) (both-direction) ---

def test_text_wall_page_flags_imagery_mandatory(tmp_path):
    """A full page (<body>) with zero imagery is a text-wall — must fire HIGH."""
    f = tmp_path / "wall.html"
    f.write_text(
        '<!doctype html><html><body><main><section><h1>Skips</h1>'
        '<div class="card">A</div><div class="card">B</div>'
        '</section></main></body></html>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "imagery-mandatory-missing" in ids


def test_page_with_img_not_flagged_imagery_mandatory(tmp_path):
    """A page that ships a real <img> must NOT fire the imagery rule."""
    f = tmp_path / "withimg.html"
    f.write_text(
        '<!doctype html><html><body><main><section><h1>Skips</h1>'
        '<img src="/hero.avif" alt="a commercial skip" width="800" height="600">'
        '</section></main></body></html>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "imagery-mandatory-missing" not in ids


def test_page_with_inline_svg_not_flagged_imagery_mandatory(tmp_path):
    """A SUBSTANTIAL inline SVG illustration (large viewBox) counts as imagery."""
    f = tmp_path / "withsvg.html"
    f.write_text(
        '<!doctype html><html><body><main><section><h1>Skips</h1>'
        '<svg viewBox="0 0 480 320"><path d="M3 7h18v10H3z"/></svg>'
        '</section></main></body></html>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "imagery-mandatory-missing" not in ids


def test_icon_only_page_flags_imagery_mandatory(tmp_path):
    """Icons are NOT imagery: a full page whose only SVGs are icon-sized
    (viewBox 0 0 24 24 / width 24) is still a text-wall -- the sharpened rule fires."""
    f = tmp_path / "icons.html"
    f.write_text(
        '<!doctype html><html><body><main><section><h1>Skips</h1>'
        '<div class="card"><svg viewBox="0 0 24 24" width="24" height="24">'
        '<path d="M3 7h18v10H3z"/></svg>Fast pickup</div>'
        '</section></main></body></html>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "imagery-mandatory-missing" in ids


def test_component_fragment_not_flagged_imagery_mandatory(tmp_path):
    """A component fragment (no <body>) is exempt — not every partial needs art."""
    f = tmp_path / "card.html"
    f.write_text(
        '<section class="pricing"><h2>Pro</h2><p>Real copy here.</p></section>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "imagery-mandatory-missing" not in ids


# --- Responsive gate (dogfood P6): placeholder-token-shipped (both-direction) ---

def test_placeholder_token_shipped_flags_todo_fill(tmp_path):
    """A literal {TODO_FILL...} left in shipped markup is a draft-state leak — must fire HIGH."""
    f = tmp_path / "leak.html"
    f.write_text(
        '<header><a class="nav-phone" href="tel:{TODO_FILL}">'
        '<span>{TODO_FILL: phone}</span></a></header>',
        encoding="utf-8")
    findings = lint([str(f)]).to_dict()["findings"]
    hit = [x for x in findings if x["rule_id"] == "placeholder-token-shipped"]
    assert hit, "literal {TODO_FILL} placeholder did not fire"
    assert hit[0]["severity"] == "high"


def test_placeholder_token_shipped_ignores_real_template_binding(tmp_path):
    """A legitimate Vue/Blade {{ binding }} is NOT a placeholder — must NOT fire."""
    f = tmp_path / "ok.vue"
    f.write_text(
        '<template><span>{{ user.name }}</span>'
        '<p>{{ price | currency }}</p><div>{{ item.title }}</div></template>',
        encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "placeholder-token-shipped" not in ids


# --- Responsive gate (dogfood P6): full-viewport-width-overflow (both-direction) ---

def test_full_viewport_width_flags_100vw(tmp_path):
    """width: 100vw overflows by the scrollbar width -> horizontal scroll. Must fire."""
    f = tmp_path / "overflow.css"
    f.write_text(".hero { width: 100vw; }\n.bar { min-width: 100vw; }", encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "full-viewport-width-overflow" in ids


def test_full_viewport_width_ignores_max_width_100vw(tmp_path):
    """max-width: 100vw is a legitimate ceiling, not an overflow source — must NOT fire."""
    f = tmp_path / "ok.css"
    f.write_text(".hero { max-width: 100vw; }\n.bar { width: 100%; }", encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "full-viewport-width-overflow" not in ids
