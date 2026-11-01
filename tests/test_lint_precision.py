"""Precision on pages as AI builders ship them: a compiled stylesheet holds
the utilities and library rules of every route, most of which match nothing
on the page; a toast library hides its toasts with attribute selectors; a
dashboard's header has a title and a button; a long headline can run past
its column. Each case reports what the page does, not what its bundle
carries."""
from engine.linter.core import compute_score, lint_text, Finding


def _ids(name: str, text: str):
    return [f.rule_id for f in lint_text(name, text)]


PAGE = """<!doctype html><html lang="en"><head><style>
{css}
</style></head><body>{body}</body></html>"""


# ------------------------------------------------ unused utility rules

UTILITIES = r"""
.h-screen { height: 100vh; }
.transition-\[width\] { transition-property: width; transition-duration: .2s; }
.md\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.text-white\/50 { color: rgba(255, 255, 255, .5); }
"""


def test_a_utility_no_element_uses_is_not_reported():
    body = "<main><h1>Orders</h1><p>Today</p></main>"
    ids = _ids("page.html", PAGE.format(css=UTILITIES, body=body))
    for rule in ("h-screen-no-dvh-fallback", "animating-layout-properties", "text-ink-at-low-alpha"):
        assert rule not in ids, rule


def test_a_utility_an_element_uses_is_still_reported():
    body = '<main class="h-screen"><h1>Orders</h1><p class="text-white/50">Today</p></main>'
    ids = _ids("page.html", PAGE.format(css=UTILITIES, body=body))
    assert "h-screen-no-dvh-fallback" in ids
    assert "text-ink-at-low-alpha" in ids


def test_an_escaped_class_matches_its_element():
    body = '<main><div class="md:grid-cols-3"><p>a</p><p>b</p><p>c</p></div></main>'
    css = r".md\:grid-cols-3 { transition-property: width; transition-duration: .2s; }"
    ids = _ids("page.html", PAGE.format(css=css, body=body))
    assert "animating-layout-properties" in ids


def test_a_class_a_script_adds_counts_as_used():
    body = ('<main><h1>Orders</h1><button type="button" id="t">Open</button></main>'
            "<script>document.body.classList.add('h-screen')</script>")
    ids = _ids("page.html", PAGE.format(css=UTILITIES, body=body))
    assert "h-screen-no-dvh-fallback" in ids


def test_a_stylesheet_without_markup_is_read_as_before():
    ids = _ids("app.css", UTILITIES)
    assert "h-screen-no-dvh-fallback" in ids


# ------------------------------------------------ attribute selectors

TOASTS = """
:where([data-toast][data-visible="false"]) { opacity: 0; pointer-events: none; }
:where([data-toast][data-expanded="false"]) > * { opacity: 0; }
"""


def test_toast_rules_for_toasts_the_page_does_not_have_are_quiet():
    body = '<main><h1>Orders</h1><a href="/new">New order</a></main>'
    assert "focusable-at-opacity-zero" not in _ids("page.html", PAGE.format(css=TOASTS, body=body))


def test_toast_rules_for_a_toast_holding_a_link_still_report():
    body = ('<main><h1>Orders</h1></main>'
            '<ol><li data-toast data-visible="false"><a href="/undo">Undo</a></li></ol>')
    assert "focusable-at-opacity-zero" in _ids("page.html", PAGE.format(css=TOASTS, body=body))


def test_a_selector_matching_nothing_on_a_page_with_markup_does_not_guess():
    css = ".drawer-panel { opacity: 0; }"
    body = '<main><h1>Orders</h1><a href="/new">New order</a></main>'
    assert "focusable-at-opacity-zero" not in _ids("page.html", PAGE.format(css=css, body=body))


# ------------------------------------------------ app shell

SHELL = """<!doctype html><html lang="en"><body>
<aside><a href="#d">Dashboard</a><a href="#o">Orders</a><a href="#p">Products</a></aside>
<main><h1>Today at the counter</h1><a class="btn" href="#new">Start a new bill</a>
<section><h2>Sales</h2><p>Revenue today and this week.</p></section></main>
</body></html>"""


def test_a_dashboard_header_with_an_action_is_not_a_landing_page():
    assert "imagery-mandatory-missing" not in _ids("app.html", SHELL)


def test_a_landing_page_still_needs_a_photograph():
    page = """<!doctype html><html lang="en"><body>
<header><nav><a href="#a">About</a></nav></header>
<main><h1>Run your clinic's bookings</h1><a class="btn" href="#start">Start free</a>
<section><h2>Why</h2><p>Patients book themselves.</p></section></main></body></html>"""
    assert "imagery-mandatory-missing" in _ids("landing.html", page)


# ------------------------------------------------ the score

def _f(rule: str, severity: str) -> Finding:
    return Finding(rule_id=rule, rule_name=rule, severity=severity, category="Layout",
                   file="a.html", line=1, column=1, excerpt="", fix="")


def test_small_scores_keep_their_values():
    assert compute_score([_f(f"r{i}", "medium") for i in range(5)]) == 80
    assert compute_score([_f(f"r{i}", "high") for i in range(5)]) == 50


def test_heavy_pages_still_differ():
    worse = compute_score([_f(f"r{i}", "high") for i in range(30)])
    bad = compute_score([_f(f"r{i}", "high") for i in range(12)])
    assert 0 < worse < bad < 50


# ------------------------------------------------ text past its box (render)

def _render_ids(tmp_path, html):
    import pytest
    pytest.importorskip("playwright")
    from engine.render import RenderUnavailable, render_check
    f = tmp_path / "page.html"
    f.write_text(html, encoding="utf-8")
    try:
        return [x.rule_id for x in render_check([str(f)]).findings]
    except RenderUnavailable as exc:
        pytest.skip(str(exc))


COLUMNS = ('<!doctype html><html lang="en"><body style="margin:0"><main style="display:grid;'
           'grid-template-columns:300px 300px;gap:24px">'
           '<h1 style="font-size:88px;margin:0{extra}">Perimeterization</h1><p>Beside it.</p>'
           '</main></body></html>')


def test_a_headline_wider_than_its_column_is_reported(tmp_path):
    assert "text-overflows-its-box" in _render_ids(tmp_path, COLUMNS.format(extra=""))


def test_a_headline_that_breaks_its_words_is_clean(tmp_path):
    ids = _render_ids(tmp_path, COLUMNS.format(extra=";overflow-wrap:anywhere"))
    assert "text-overflows-its-box" not in ids


def test_text_inside_a_scroller_is_its_own_concern(tmp_path):
    html = ('<!doctype html><html lang="en"><body style="margin:0"><main>'
            '<div style="overflow-x:auto;width:300px"><p style="white-space:nowrap">'
            'A long line that scrolls inside its own container and nowhere else.</p></div>'
            '</main></body></html>')
    assert "text-overflows-its-box" not in _render_ids(tmp_path, html)


# ------------------------------------------------ review regressions

def test_a_hex_escaped_utility_matches_its_element():
    css = r".\32xl\:h-screen { height: 100vh; }"
    body = '<main class="2xl:h-screen"><h1>Orders</h1></main>'
    assert "h-screen-no-dvh-fallback" in _ids("page.html", PAGE.format(css=css, body=body))


def test_a_landing_page_with_a_drawer_still_needs_a_photograph():
    page = """<!doctype html><html lang="en"><body>
<aside class="drawer" hidden><a href="#a">About</a><a href="#p">Pricing</a><a href="#c">Contact</a></aside>
<main><h1>Run your clinic's bookings</h1><a class="btn" href="#start">Start free</a>
<section><h2>Why</h2><p>Patients book themselves.</p></section></main></body></html>"""
    assert "imagery-mandatory-missing" in _ids("landing.html", page)


def test_a_sibling_combinator_selector_still_reports():
    css = "input:not(:checked) ~ nav a { opacity: 0; }"
    body = '<input type="checkbox" aria-label="Menu"><nav><a href="/a">A</a></nav>'
    assert "focusable-at-opacity-zero" in _ids("page.html", PAGE.format(css=css, body=body))


def test_a_state_attribute_a_script_sets_still_reports():
    css = '[data-state="closed"] a { opacity: 0; }'
    body = ('<div id="m"><a href="/a">A</a></div>'
            "<script>document.getElementById('m').dataset.state = 'closed'</script>")
    assert "focusable-at-opacity-zero" in _ids("page.html", PAGE.format(css=css, body=body))


def test_a_page_mounted_by_an_external_script_keeps_its_utilities():
    body = '<div id="root"></div><script type="module" src="/assets/index.js"></script>'
    assert "h-screen-no-dvh-fallback" in _ids("index.html", PAGE.format(css=UTILITIES, body=body))


def test_component_files_with_runtime_classes_keep_their_utilities():
    sfc = ('<template><div :class="`alert-${kind}`">Saved</div></template>\n'
           "<style>.alert-muted { color: rgba(255, 255, 255, .4); }</style>")
    assert "text-ink-at-low-alpha" in _ids("Alert.vue", sfc)


def test_repeats_of_one_rule_cost_what_they_cost_before_up_to_the_knee():
    assert compute_score([_f("r", "high")] * 4) == 60
    assert compute_score([_f("r", "high")] * 50) < 50


def test_past_the_knee_a_repeated_rule_weighs_less_than_as_many_rules():
    # 149 placeholder links are one pattern; 149 different rules are not.
    one_rule = compute_score([_f("r", "high")] * 149)
    many = compute_score([_f(f"r{i}", "high") for i in range(149)])
    assert many == 1 and one_rule > many


def test_a_page_of_distinct_rules_scores_as_before():
    from engine.linter.core import SCORE_KNEE, SCORE_TAIL
    import math
    for n in (6, 12, 30):
        findings = [_f(f"r{i}", "high") for i in range(n)]
        flat = 10 * n
        want = round(100 - flat) if flat <= SCORE_KNEE else max(
            1, round(SCORE_KNEE * math.exp(-(flat - SCORE_KNEE) / SCORE_TAIL)))
        assert compute_score(findings) == want


def test_another_repeat_never_raises_the_score():
    findings, last = [], 100
    for i in range(300):
        findings.append(_f(f"r{i % 7}", "high" if i % 3 else "medium"))
        score = compute_score(findings)
        assert score <= last, (i, score, last)
        last = score


def test_an_is_with_a_combinator_inside_keeps_its_meaning():
    css = ".item:is(.closed *) { opacity: 0; }"
    body = '<div class="closed"><a class="item" href="/x">X</a></div>'
    assert "focusable-at-opacity-zero" in _ids("page.html", PAGE.format(css=css, body=body))


def test_a_stylesheet_with_linked_pages_still_guesses():
    from engine.linter.core import lint_text as lt
    css = ".drawer a { opacity: 0; }"
    page = '<!doctype html><html lang="en"><body><main><h1>Home</h1></main></body></html>'
    ids = [f.rule_id for f in lt("site.css", css, pages=[("index.html", page)])]
    assert "focusable-at-opacity-zero" in ids


def test_a_hidden_dropdown_is_not_text_past_its_box(tmp_path):
    html = ('<!doctype html><html lang="en"><body style="margin:0"><nav style="display:flex">'
            '<ul style="display:flex;list-style:none;margin:0;padding:0">'
            '<li style="position:relative;width:90px">Products<ul style="position:absolute;'
            'width:260px;visibility:hidden;margin:0"><li>Every product we sell</li></ul></li>'
            '</ul></nav><main><p>Body</p></main></body></html>')
    assert "text-overflows-its-box" not in _render_ids(tmp_path, html)


def test_an_inline_block_label_that_spills_is_reported(tmp_path):
    html = ('<!doctype html><html lang="en"><body style="margin:0"><main><label style="'
            'display:inline-block;width:80px;white-space:nowrap">A label much wider than eighty '
            'pixels</label><p>Next</p></main></body></html>')
    assert "text-overflows-its-box" in _render_ids(tmp_path, html)


def test_the_same_page_in_many_files_scores_as_one_page():
    def page(name):
        return [Finding(rule_id=f"r{i}", rule_name="r", severity="high", category="Layout",
                        file=name, line=1, column=1, excerpt="", fix="") for i in range(6)]
    one = compute_score(page("a.html"))
    many = [f for n in range(20) for f in page(f"p{n}.html")]
    assert compute_score(many, files_scanned=20) == one
