"""text-low-contrast: any text under what WCAG 1.4.3 asks on the ground the
visitor sees (4.5:1, or 3:1 at 24px or 18.66px bold), read with the page
scrolled so each block is in view. Accent text keeps its own rule and the
system's 4.5:1 floor. Text 1.4.3 exempts (an inactive control, text hidden
from assistive technology) passes, and a ground a script swaps in on
scroll is the one measured."""
from pathlib import Path

import pytest

pytest.importorskip("playwright")

from engine.render import RenderUnavailable, render_check  # noqa: E402

RULE = "text-low-contrast"
PAGE = ('<!doctype html><html lang="en"><head><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><style>{css}</style></head>'
        '<body style="margin:0;background:#fff;color:#111"><main style="padding:24px">'
        '<h1>Plans</h1>{body}</main></body></html>')


def _hits(tmp_path: Path, name: str, body: str, css: str = ""):
    f = tmp_path / name
    f.write_text(PAGE.replace("{css}", css).replace("{body}", body), encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x for x in report.findings if x.rule_id == RULE]


def test_light_grey_body_text_is_found(tmp_path):
    hits = _hits(tmp_path, "grey.html", '<p style="color:#999">Billed yearly.</p>')
    assert hits and "#999999 on #ffffff" in hits[0].excerpt and "4.5:1 (1.4.3)" in hits[0].excerpt


def test_large_text_needs_three_to_one(tmp_path):
    assert _hits(tmp_path, "large-ok.html",
                 '<p style="color:#949494;font-size:24px">Save 20%</p>') == []
    assert _hits(tmp_path, "large-low.html",
                 '<p style="color:#b0b0b0;font-size:24px">Save 20%</p>')


def test_text_far_down_the_page_is_read(tmp_path):
    body = '<div style="height:3000px"></div><p style="color:#aaa">Terms apply.</p>'
    css = "html{scroll-behavior:smooth}"
    assert _hits(tmp_path, "far.html", body, css)


@pytest.mark.parametrize("name,body", [
    ("dark-enough.html", '<p style="color:#595959">Billed yearly.</p>'),
    ("disabled.html", '<button disabled style="color:#aaa">Upgrade</button>'),
    ("decorative.html", '<span aria-hidden="true" style="color:#eee;font-size:120px">01</span>'),
])
def test_text_the_criterion_lets_through_passes(tmp_path, name, body):
    assert _hits(tmp_path, name, body) == []


def test_the_ground_a_script_swaps_in_on_scroll_is_measured(tmp_path):
    # The section is transparent; a script paints the body dark once the
    # section is in view, as scroll-led pages do. Light text there passes.
    body = ('<div style="height:1600px"></div><section id="dark" style="padding:40px">'
            '<p style="color:#e8e8e8">Built for night shifts.</p></section>'
            '<div style="height:1600px"></div><script>'
            'new IntersectionObserver(es => es.forEach(e => {document.body.style.background ='
            ' e.isIntersecting ? "#0b0b0b" : "#fff";})).observe(document.getElementById("dark"));'
            '</script>')
    assert _hits(tmp_path, "swap.html", body) == []
