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
    for entry in load("anti-patterns")["entries"]:
        det = entry.get("detection", {})
        if det.get("type") == "regex":
            re.compile(det["pattern"])


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


# --- Site lint false positives (docs/ dogfood). Each case is a minimal copy of the
# --- page markup that fired, plus the real violation the rule must still catch.

def _ids(tmp_path, name, body):
    f = tmp_path / name
    f.write_text(body, encoding="utf-8")
    return [x["rule_id"] for x in lint([str(f)]).to_dict()["findings"]]


def test_animating_layout_ignores_transition_none_before_later_css(tmp_path):
    """docs/*.html nav: `transition:none}` has no `;`, so the old pattern ran on
    into later markup until it met a word like `left`."""
    html = ('<style>@media (prefers-reduced-motion:reduce){.usknav__drawer{transition:none}}</style>\n'
            '<div class="x" style="margin-left:4px;">a</div>')
    assert "animating-layout-properties" not in _ids(tmp_path, "nav.html", html)


def test_animating_layout_ignores_svg_transition_delay(tmp_path):
    """docs/index.html hero wiring: a transition-delay on an SVG node."""
    html = ('<circle class="wnode" cx="200" cy="110" r="7" style="transition-delay:.55s"/>\n'
            '<rect width="10" height="10"/><p style="padding:0;">x</p>')
    assert "animating-layout-properties" not in _ids(tmp_path, "wire.html", html)


def test_animating_layout_still_flags_width_transition(tmp_path):
    assert "animating-layout-properties" in _ids(
        tmp_path, "bad.css", ".bar { transition: width .3s ease }")
    assert "animating-layout-properties" in _ids(
        tmp_path, "bad.html", '<div style="transition: height 1s">x</div>')


def test_inline_style_custom_properties_only_not_flagged(tmp_path):
    """docs/design-systems.html cards and index.html wiring pass data in as CSS vars."""
    html = ('<a class="ds-card" style="--c:#00040c;--i:#e5f1ff;--p:#db3291">x</a>\n'
            '<span class="sw" style="--sw:#bf3722"></span>')
    assert "inline-style-attribute" not in _ids(tmp_path, "vars.html", html)


def test_inline_style_ignores_svg_path_tag(tmp_path):
    """`<p` must not match `<path`."""
    html = '<svg><path class="wire" d="M40 110 H200" style="stroke-dasharray:160"/></svg>'
    assert "inline-style-attribute" not in _ids(tmp_path, "svg.html", html)


def test_inline_style_still_flags_real_declarations(tmp_path):
    assert "inline-style-attribute" in _ids(
        tmp_path, "bad.html", '<div style="margin-top:14px; opacity:0.6;">x</div>')
    assert "inline-style-attribute" in _ids(
        tmp_path, "mixed.html", '<span style="--sw:#fff;background:var(--sw)"></span>')


def test_imagery_counts_an_iframe_of_the_product(tmp_path):
    """docs/design-systems/<slug>/index.html: the main visual is a live iframe."""
    html = ('<!doctype html><html><body><main><h1>Iris</h1>'
            '<iframe src="/design-systems/iris/preview.html" title="Iris preview"></iframe>'
            '</main></body></html>')
    assert "imagery-mandatory-missing" not in _ids(tmp_path, "detail.html", html)


def test_multi_stop_gradient_ignores_commas_inside_rgba(tmp_path):
    """docs/blog/index.html: a two-stop gradient whose stops are rgba()."""
    css = ".post { background: linear-gradient(180deg, rgba(34,211,238,0.06), rgba(16, 185, 129, 0.02)); }"
    assert "chrome-y-multi-stop-gradient" not in _ids(tmp_path, "two.css", css)


def test_multi_stop_gradient_still_flags_four_stops(tmp_path):
    css = ".chrome { background: linear-gradient(180deg, #fff, #ccc 40%, #999 60%, #eee); }"
    assert "chrome-y-multi-stop-gradient" in _ids(tmp_path, "four.css", css)


def test_box_shadow_two_color_mix_layers_not_flagged(tmp_path):
    """docs/design-systems/*/css/tokens.css .card-elevated: two layers, the
    ambient plus contact pair the rule's own fix recommends."""
    css = (".card-elevated {\n  box-shadow:\n"
           "    0 1px 2px color-mix(in srgb, var(--color-ink) 6%, transparent),\n"
           "    0 18px 40px color-mix(in srgb, var(--color-ink) 8%, transparent);\n}")
    assert "box-shadow-multilayer-default" not in _ids(tmp_path, "tokens.css", css)


def test_box_shadow_three_layers_still_flagged(tmp_path):
    css = ".c { box-shadow: 0 1px 2px rgba(0,0,0,.1), 0 4px 8px rgba(0,0,0,.1), 0 16px 32px rgba(0,0,0,.1); }"
    assert "box-shadow-multilayer-default" in _ids(tmp_path, "three.css", css)


def test_fixed_height_ignores_letters_inside_other_words(tmp_path):
    """tokens.css: the `p` in `display` and the `div` in `.divider` are not selectors."""
    css = (".grid {\n  display: grid;\n}\n\n.divider {\n  height: 1px;\n"
           "  background: var(--color-border);\n}")
    assert "fixed-height-text-block" not in _ids(tmp_path, "tokens.css", css)


def test_fixed_height_still_flags_text_div(tmp_path):
    css = "div.note { height: 40px; color: #333; }"
    assert "fixed-height-text-block" in _ids(tmp_path, "bad.css", css)


def test_glass_with_background_before_blur_not_flagged(tmp_path):
    """docs/faq.html nav drawer: background-color is declared above the blur."""
    css = (".nav__drawer {\n  background-color: rgba(7, 8, 10, 0.94);\n"
           "  backdrop-filter: blur(18px);\n  -webkit-backdrop-filter: blur(18px);\n}")
    assert "glass-without-fallback" not in _ids(tmp_path, "drawer.css", css)


def test_glass_without_background_still_flagged(tmp_path):
    assert "glass-without-fallback" in _ids(
        tmp_path, "bad.css", ".x { backdrop-filter: blur(10px); }\n.y { background: red; }")
    assert "glass-without-fallback" in _ids(
        tmp_path, "bad.html", '<div style="backdrop-filter: blur(8px)">x</div>')


def test_placeholder_with_label_for_not_flagged(tmp_path):
    """preview.html specimen form: a visible <label for> plus a placeholder hint."""
    html = ('<label class="field-label" for="sh-email">Work email</label>\n'
            '<input class="input" id="sh-email" type="email" name="email" '
            'placeholder="you@studio.com" autocomplete="email">')
    assert "placeholder-as-label" not in _ids(tmp_path, "form.html", html)


def test_placeholder_as_only_label_still_flagged(tmp_path):
    assert "placeholder-as-label" in _ids(
        tmp_path, "bad.html", '<input type="email" placeholder="Email">')


def _hits(tmp_path, name, body, rule):
    f = tmp_path / name
    f.write_text(body, encoding="utf-8")
    report = lint([str(f)])
    return [x for x in report.to_dict()["findings"] if x["rule_id"] == rule], report


def test_region_waives_only_the_rules_it_names(tmp_path):
    """docs/anti-patterns.html quotes the rules it documents. A ux-lint-off
    region waives the named rules on its lines; other rules still fire there,
    and lines after ux-lint-on are linted as usual."""
    html = ('<!-- ux-lint-off lorem-ipsum-leak, placeholder-token-shipped -->\n'
            '<h3 class="ap-name">Lorem ipsum in shipping code</h3>\n'
            '<p>We saved John Doe 10 hours.</p>\n'
            '<!-- ux-lint-on -->\n'
            '<p>lorem ipsum dolor</p>\n')
    lorem, report = _hits(tmp_path, "catalog.html", html, "lorem-ipsum-leak")
    assert [x["line"] for x in lorem] == [5]
    names, _ = _hits(tmp_path, "catalog.html", html, "fake-name-john-doe")
    assert [x["line"] for x in names] == [3]
    assert report.waived_lines == 4
    assert report.to_dict()["waived_lines"] == 4


def test_unclosed_region_waives_nothing_and_is_a_finding(tmp_path):
    html = '<p>ok</p>\n<!-- ux-lint-off lorem-ipsum-leak -->\n<p>Lorem ipsum</p>\n'
    lorem, _ = _hits(tmp_path, "open.html", html, "lorem-ipsum-leak")
    assert [x["line"] for x in lorem] == [3]
    broken, report = _hits(tmp_path, "open.html", html, "lint-waiver-region")
    assert [x["line"] for x in broken] == [2]
    assert broken[0]["severity"] == "high"
    assert "line 2" in broken[0]["fix"] and "ux-lint-on" in broken[0]["fix"]
    assert report.exit_code == 1


def test_region_without_rule_ids_waives_nothing_and_is_a_finding(tmp_path):
    html = '<!-- ux-lint-off -->\n<p>Lorem ipsum</p>\n<!-- ux-lint-on -->\n'
    lorem, _ = _hits(tmp_path, "bare.html", html, "lorem-ipsum-leak")
    assert [x["line"] for x in lorem] == [2]
    broken, _ = _hits(tmp_path, "bare.html", html, "lint-waiver-region")
    assert [x["line"] for x in broken] == [1] and "names no rule" in broken[0]["fix"]


def test_stray_region_close_is_a_finding(tmp_path):
    broken, _ = _hits(tmp_path, "stray.html", "<p>ok</p>\n<!-- ux-lint-on -->\n", "lint-waiver-region")
    assert [x["line"] for x in broken] == [2]


def test_disable_comment_waives_its_own_line_only(tmp_path):
    """commands/ux-lint.md: `ux-lint-disable` on a line skips that line."""
    html = ('<p>Acme Inc, Lorem ipsum <!-- ux-lint-disable --></p>\n'
            '<p>Lorem ipsum</p>\n'
            '<p>Lorem ipsum <!-- ux-lint-disable fake-name-john-doe --></p>\n'
            '<!-- ux-lint-disable-next-line lorem-ipsum-leak -->\n'
            '<p>Lorem ipsum</p>\n')
    lorem, _ = _hits(tmp_path, "line.html", html, "lorem-ipsum-leak")
    assert [x["line"] for x in lorem] == [2, 3]


def test_passive_listener_explicit_false_not_flagged(tmp_path):
    """docs/index.html pins a scene and blocks scroll on purpose: an explicit
    `{passive:false}` is the opt-out the rule's own fix allows."""
    js = ("function lockScroll(){document.addEventListener('wheel',noScroll,{passive:false});"
          "document.addEventListener('touchmove',noScroll,{passive:false});}")
    assert "event-listener-no-passive-on-scroll" not in _ids(tmp_path, "pin.js", js)


def test_passive_listener_missing_option_still_flagged(tmp_path):
    js = "window.addEventListener('scroll', onScroll);"
    assert "event-listener-no-passive-on-scroll" in _ids(tmp_path, "bad.js", js)


# --- placeholder-as-label: pass only with a real accessible name ---

@pytest.mark.parametrize("name,body", [
    ("id-no-label.html", '<input id="email" type="email" placeholder="Email">'),
    ("search.tsx", '<input id="search" placeholder="Search" />'),
    ("label-elsewhere.html", '<label for="other">Name</label><input id="email" placeholder="Email">'),
    ("data-id.html", '<input data-id="x" placeholder="Search">'),
    ("testid.html", '<input data-testid="q" placeholder="Search">'),
    ("labelledby-missing.html", '<input aria-labelledby="nope" placeholder="Search">'),
    ("empty-aria-label.html", '<input aria-label="" placeholder="Search">'),
    ("closed-label.html", '<label>Name</label><input placeholder="Search">'),
])
def test_placeholder_without_accessible_name_fires(tmp_path, name, body):
    assert "placeholder-as-label" in _ids(tmp_path, name, body)


@pytest.mark.parametrize("name,body", [
    ("label-for.html", '<label for="email">Email</label>\n<input id="email" placeholder="you@x.com">'),
    ("label-after.html", '<input id="q" placeholder="Search"><label for="q">Search</label>'),
    ("html-for.tsx", '<label htmlFor="q">Search</label><input id="q" placeholder="Search" />'),
    ("wrapping.html", '<label>Email <input type="email" placeholder="you@x.com"></label>'),
    ("aria-label.html", '<input aria-label="Search" placeholder="Search">'),
    ("labelledby.html", '<span id="lbl">Search</span><input aria-labelledby="lbl" placeholder="Search">'),
])
def test_placeholder_with_accessible_name_passes(tmp_path, name, body):
    assert "placeholder-as-label" not in _ids(tmp_path, name, body)


def test_box_shadow_tailwind_composite_not_flagged(tmp_path):
    css = (".ring { box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), "
           "var(--tw-shadow, 0 0 #0000); }")
    assert "box-shadow-multilayer-default" not in _ids(tmp_path, "tw.css", css)


def test_box_shadow_three_hex_layers_flagged(tmp_path):
    css = ".c { box-shadow: 0 1px 2px #0001, 0 4px 8px #0001, 0 16px 32px #0001; }"
    assert "box-shadow-multilayer-default" in _ids(tmp_path, "hex.css", css)


def test_glass_word_background_in_transition_is_not_a_fallback(tmp_path):
    css = ".x { transition: background .2s; backdrop-filter: blur(8px); }"
    assert "glass-without-fallback" in _ids(tmp_path, "t.css", css)


def test_glass_finding_points_at_the_blur_line(tmp_path):
    css = ".x {\n  color: red;\n  backdrop-filter: blur(8px);\n}\n"
    hits, _ = _hits(tmp_path, "l.css", css, "glass-without-fallback")
    assert [x["line"] for x in hits] == [3]
