"""focus-obscured: a control that takes focus entirely hidden under fixed or
sticky author content, a cookie bar or a tall header (WCAG 2.4.11). A bar
the page leaves room for with scroll padding, and a control inside the bar
itself, pass."""
from pathlib import Path

import pytest

pytest.importorskip("playwright")

from engine.render import RenderUnavailable, render_check  # noqa: E402

RULE = "focus-obscured"
LINKS = "".join(f'<p style="margin:0;height:60px"><a href="#a{i}">Item {i}</a></p>' for i in range(40))
BAR = ('<div style="position:fixed;left:0;right:0;bottom:0;height:200px;background:#fff;'
       'border-top:1px solid #ccc">We use cookies. <button>OK</button></div>')


def _hits(tmp_path: Path, name: str, html: str):
    f = tmp_path / name
    f.write_text(html, encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x for x in report.findings if x.rule_id == RULE]


def _page(style: str, body: str) -> str:
    return ('<!doctype html><html lang="en"><head><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><style>{style}</style></head>'
            f'<body style="margin:0"><main><h1>Orders</h1>{body}</main></body></html>')


def test_links_tabbed_under_a_bottom_bar_are_found(tmp_path):
    hits = _hits(tmp_path, "bar.html", _page("", LINKS + BAR))
    assert hits and "entirely hidden under div" in hits[0].excerpt


def test_scroll_padding_leaves_room_and_passes(tmp_path):
    assert _hits(tmp_path, "padded.html", _page("html{scroll-padding-bottom:220px}", LINKS + BAR)) == []


def test_a_control_inside_the_bar_passes(tmp_path):
    assert _hits(tmp_path, "only-bar.html", _page("", "<p>Short page.</p>" + BAR)) == []
