"""Linter smoke + rule-specific behavior tests."""
import re
from pathlib import Path

import pytest

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


# Issue #36: the token alternatives were case-insensitive, so ordinary JSX
# style objects (sx={{...}}, style={{...}}) tripped the rule.
@pytest.mark.parametrize("snippet,should_fire", [
    ("<Box sx={{ left: fillLeftPercent }} />", False),
    ("<Box sx={{ backfill: true }} />", False),
    ("<div style={{ marginTop: spacing_md }} />", False),
    ("<title>{{FILL_ME}}</title>", True),
    ("<meta content='{{TODO}}' />", True),
    ("<p>Lorem Ipsum dolor sit amet</p>", True),
])
def test_placeholder_token_shipped_case_sensitivity_issue_36(tmp_path, snippet, should_fire):
    f = tmp_path / "c.tsx"
    f.write_text(snippet, encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert ("placeholder-token-shipped" in ids) is should_fire


# Decorative accent ruler: a hairline used as ornament, fading out of
# transparent and/or capped with a small dot. An AI fingerprint.
@pytest.mark.parametrize("name,snippet,should_fire", [
    ("fading.html",
     '<div class="h-px w-24 bg-gradient-to-r from-transparent via-emerald-400 to-transparent"></div>',
     True),
    ("v4.tsx",
     '<div className="mt-6 h-[1px] w-32 bg-linear-to-r from-emerald-500 to-transparent" />',
     True),
    ("dot.html",
     '<div class="flex items-center"><span class="h-px w-16 bg-emerald-400"></span>'
     '<span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span></div>',
     True),
    ("dot-first.jsx",
     '<span className="size-2 rounded-full bg-lime-400" /><span className="h-px w-20 bg-lime-400" />',
     True),
    ("rule.css",
     ".accent-rule {\n  height: 1px;\n  width: 96px;\n"
     "  background: linear-gradient(90deg, transparent, #34d399);\n}",
     True),
    ("structural-hr.html", '<hr class="border-t border-neutral-200">', False),
    ("solid-divider.html", '<div class="h-px w-full bg-neutral-200"></div>', False),
    ("progress.css", ".bar { height: 4px; background: linear-gradient(90deg, #111, #333); }", False),
    ("status-dot.html",
     '<span class="h-2 w-2 rounded-full bg-green-500"></span><span>Online</span>', False),
    ("hero.html",
     '<section class="h-96 bg-gradient-to-r from-transparent to-slate-900"></section>', False),
    # Eyebrow dash: a short solid hairline set beside a label.
    ("eyebrow.css",
     ".eyebrow::before {\n  content: ''; display: inline-block;\n"
     "  width: 22px; height: 1px;\n  background: currentColor;\n}",
     True),
    ("eyebrow-span.html",
     '<p class="flex items-center gap-3"><span class="h-px w-6 bg-current"></span>Roadmap</p>',
     True),
    ("eyebrow-variant.tsx",
     '<p className="before:h-px before:w-8 before:bg-current">Roadmap</p>',
     True),
    ("tab-underline.css",
     ".tab[aria-selected=true]::after { content: ''; height: 2px; width: 100%; background: var(--accent); }",
     False),
    ("link-hover.css",
     "a::after { content: ''; height: 1px; width: 0; transition: width .2s; }",
     False),
    # An animated scan line is a loading-state indicator, not ornament.
    ("scan-loader.css",
     ".lane::before {\n  height: 2px;\n"
     "  background: linear-gradient(90deg, transparent, #38bdf8, transparent);\n"
     "  animation: scan 1400ms ease infinite;\n}",
     False),
])
def test_decorative_accent_ruler(tmp_path, name, snippet, should_fire):
    f = tmp_path / name
    f.write_text(snippet, encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert ("decorative-accent-ruler" in ids) is should_fire


def test_every_regex_rule_compiles():
    """The loader skips rules whose pattern fails to compile. A broken pattern
    must fail here instead of silently disabling the rule."""
    from engine.data_loader import load
    from engine.linter.views import CHANNELS
    for entry in load("anti-patterns")["entries"]:
        det = entry.get("detection", {})
        if det.get("type") == "regex":
            for part in [det] + det.get("also", []):
                re.compile(part["pattern"])
                if part.get("unless"):
                    re.compile(part["unless"])
                targets = part.get("target", "markup")
                for target in [targets] if isinstance(targets, str) else targets:
                    assert target in CHANNELS, f"{entry['id']}: unknown target channel {target!r}"


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


# --- JSX awareness: CSS rules read style objects and class strings, never
# --- prop names or plain text.

@pytest.mark.parametrize("name,snippet,rule_id,should_fire", [
    # style objects: camelCase keys, numbers become px
    ("a.tsx", '<div style={{ zIndex: 9999 }} />', "arbitrary-z-index-9999", True),
    ("a.tsx", '<h1 style={{ fontSize: 96 }}>Hi</h1>', "hero-text-arbitrary-90px", True),
    ("a.tsx", '<h1 style={{ lineHeight: 96 }}>Hi</h1>', "hero-text-arbitrary-90px", False),
    ("a.jsx", '<div style={{ width: "100vw" }} />', "full-viewport-width-overflow", True),
    ("a.tsx", '<Box sx={{ transition: "all 200ms", "&:hover": { zIndex: 99999 } }} />',
     "transition-property-all", True),
    ("a.tsx", '<Box sx={{ "&:hover": { zIndex: 99999 } }} />', "arbitrary-z-index-9999", True),
    ("a.tsx", '<div style={{ transition: `height ${ms}ms` }} />', "animating-layout-properties", True),
    ("a.vue", '<template><div :style="{ zIndex: 9999 }"></div></template>', "arbitrary-z-index-9999", True),
    # class strings: className, class expressions, template literals
    ("a.tsx", '<div className="transition-all" />', "transition-property-all", True),
    ("a.tsx", '<div className={cn("h-screen", open && "flex")} />', "h-screen-no-dvh-fallback", True),
    ("a.tsx", '<div className={`w-screen ${x}`} />', "full-viewport-width-overflow", True),
    ("a.tsx", 'export const panel = "fixed inset-0 z-[9999] bg-black/50";', "arbitrary-z-index-9999", True),
    # prop names are not CSS
    ("a.tsx", '<Modal zIndex={9999} />', "arbitrary-z-index-9999", False),
    ("a.tsx", '<Frame width="100vw" transition="all" />', "full-viewport-width-overflow", False),
    ("a.tsx", '<Frame width="100vw" transition="all" />', "transition-property-all", False),
    # plain text is not CSS
    ("a.tsx", "<p>Never write transition: all or z-index: 9999.</p>", "transition-property-all", False),
    ("a.tsx", "<p>Never write transition: all or z-index: 9999.</p>", "arbitrary-z-index-9999", False),
    ("a.html", "<p>The class transition-all animates layout.</p>", "transition-property-all", False),
    ("a.html", "<pre><code>.a { width: 100vw; }</code></pre>", "full-viewport-width-overflow", False),
    # custom-property-only style attributes pass runtime values to CSS
    ("a.tsx", '<div style={{ "--progress": `${pct}%` }} />', "inline-style-attribute", False),
    ("a.html", '<div style="--progress: 40%"></div>', "inline-style-attribute", False),
    ("a.html", '<div style="--progress: 40%; color: red"></div>', "inline-style-attribute", True),
])
def test_jsx_awareness(tmp_path, name, snippet, rule_id, should_fire):
    f = tmp_path / name
    f.write_text(snippet, encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert (rule_id in ids) is should_fire, ids


def test_jsx_finding_points_at_the_style_key(tmp_path):
    f = tmp_path / "a.tsx"
    f.write_text('export const A = () => (\n  <div\n    style={{\n      zIndex: 9999,\n    }}\n  />\n);\n',
                 encoding="utf-8")
    hits = [x for x in lint([str(f)]).to_dict()["findings"] if x["rule_id"] == "arbitrary-z-index-9999"]
    assert [h["line"] for h in hits] == [4]


# --- Comments, strings and data URIs are not code.

@pytest.mark.parametrize("name,snippet", [
    ("a.css", "/* .x { transition: all 1s; z-index: 9999; } */"),
    ("a.scss", "// .x { transition: all 1s; z-index: 9999; }\n.y { color: red; }"),
    ("a.tsx", "// transition: all; z-index: 9999\nexport const x = 1;"),
    ("a.tsx", "/* <div className=\"transition-all\"> */ export const x = 1;"),
    ("a.tsx", "export const A = () => <div>{/* transition-all z-[9999] */}</div>;"),
    ("a.html", "<!-- <div class=\"transition-all\" style=\"z-index: 9999\"></div> -->"),
    ("a.blade.php", "{{-- <div class=\"transition-all\" style=\"z-index: 9999\"></div> --}}"),
    ("a.css", ".a { background: url(\"data:image/svg+xml;utf8,<svg><style>*{transition:all 1s}</style></svg>\"); }"),
])
def test_comments_and_data_uris_are_not_linted(tmp_path, name, snippet):
    f = tmp_path / name
    f.write_text(snippet, encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "transition-property-all" not in ids and "arbitrary-z-index-9999" not in ids, ids


@pytest.mark.parametrize("name,snippet,should_fire", [
    ("a.tsx", 'export const EVENT = "cta-cutting-edge-click";', False),
    ("a.html", '<a href="/blog/why-we-dropped-cutting-edge">Why we changed our copy</a>', False),
    ("a.html", "<p>Drafts often say &ldquo;cutting-edge&rdquo;; we do not.</p>", False),
    ("a.tsx", 'const hero = { title: "Cutting-edge routing for carriers" };', True),
    ("a.html", "<p>Cutting-edge routing for carriers.</p>", True),
])
def test_copy_rules_read_visible_copy_only(tmp_path, name, snippet, should_fire):
    f = tmp_path / name
    f.write_text(snippet, encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert ("marketing-buzz-cutting-edge" in ids) is should_fire, ids


# --- Suppression comments.

@pytest.mark.parametrize("snippet,suppressed", [
    ('.a { z-index: 9999; } /* ux-lint-disable */', True),
    ('.a { z-index: 9999; } /* ux-lint-disable arbitrary-z-index-9999 */', True),
    ('.a { z-index: 9999; } /* ux-lint-disable transition-property-all */', False),
    ('/* ux-lint-disable-next-line arbitrary-z-index-9999 */\n.a { z-index: 9999; }', True),
    ('/* ux-lint-disable-next-line */\n\n.a { z-index: 9999; }', False),
])
def test_ux_lint_disable(tmp_path, snippet, suppressed):
    f = tmp_path / "a.css"
    f.write_text(snippet, encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert ("arbitrary-z-index-9999" not in ids) is suppressed


# --- Walking.

def test_blade_file_is_scanned_once(tmp_path):
    (tmp_path / "view.blade.php").write_text("<p>ok</p>", encoding="utf-8")
    assert lint([str(tmp_path)]).files_scanned == 1


def test_dependency_and_build_dirs_are_skipped(tmp_path):
    for d in ("node_modules/pkg", "dist", ".next/static", "vendor/lib"):
        (tmp_path / d).mkdir(parents=True)
        (tmp_path / d / "x.css").write_text(".a { z-index: 9999; }", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "x.css").write_text(".a { color: red; }", encoding="utf-8")
    report = lint([str(tmp_path)])
    assert report.files_scanned == 1
    assert report.findings == []


def test_an_explicit_file_inside_an_ignored_dir_is_still_linted(tmp_path):
    d = tmp_path / "dist"
    d.mkdir()
    f = d / "x.css"
    f.write_text(".a { z-index: 9999; }", encoding="utf-8")
    ids = [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]
    assert "arbitrary-z-index-9999" in ids
