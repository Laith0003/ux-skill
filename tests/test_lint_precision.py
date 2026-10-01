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


def test_a_repeated_rule_counts_less_each_time():
    once = compute_score([_f("r", "high")])
    many = compute_score([_f("r", "high")] * 10)
    distinct = compute_score([_f(f"r{i}", "high") for i in range(10)])
    assert once > many > distinct


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
