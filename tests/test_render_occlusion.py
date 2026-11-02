"""First-screen occlusion: a fixed banner, popup or overlay that covers the
page at rest. The rebuild of a budget calculator kept its cookie banner
floating over the content, the one thing the brief asked to fix; this is
the check that would have caught it.

A docked bar (touching the top or bottom edge, thin, over nothing key),
a narrow widget, and a decorative overlay that paints nothing or takes no
pointer all pass."""
from pathlib import Path

import pytest

pytest.importorskip("playwright")

from engine.render import RenderUnavailable, render_check  # noqa: E402

RULE = "first-screen-covered"
PAGE = ('<!doctype html><html lang="en"><head><meta name="viewport" '
        'content="width=device-width,initial-scale=1"></head><body style="margin:0">'
        '<main><h1 style="margin:80px 24px 16px;font-size:40px">How much is left at the end of '
        'the month?</h1><form style="margin:0 24px"><label>Income <input name="income"></label>'
        '<button>Work it out</button></form>'
        '<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="" '
        'style="display:block;width:90%;height:420px;margin:24px">'
        '<p style="margin:24px">Everything you enter stays in your browser.</p>'
        '<p style="margin:24px;height:900px">More below.</p></main>{extra}</body></html>')


def _hits(tmp_path: Path, name: str, extra: str):
    f = tmp_path / name
    f.write_text(PAGE.format(extra=extra), encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x for x in report.findings if x.rule_id == RULE]


@pytest.mark.parametrize("name,extra", [
    # The budget calculator: a wide cookie card floating mid-screen over content.
    ("floating-cookie-card.html",
     '<div role="region" aria-label="Cookies" style="position:fixed;left:20%;right:20%;'
     'bottom:22%;padding:16px;background:#fff;border:1px solid #ccc">We use cookies. '
     '<button>Reject</button><button>Accept</button></div>'),
    # A consent wall over most of the first screen.
    ("consent-wall.html",
     '<div style="position:fixed;inset:10% 5%;background:#fff;padding:24px">'
     'We value your privacy. <button>Accept all</button></div>'),
    # A bar docked to the top, but over the form the visitor came for.
    ("bar-over-the-form.html",
     '<div style="position:fixed;top:0;left:0;right:0;height:230px;background:#222;color:#fff">'
     'Sign up for our newsletter</div>'),
])
def test_a_cover_over_the_first_screen_is_found(tmp_path, name, extra):
    hits = _hits(tmp_path, name, extra)
    assert hits, f"{name}: {RULE} not reported"
    assert "dock" in hits[0].fix.lower() and hits[0].excerpt


@pytest.mark.parametrize("name,extra", [
    # web.dev's advice: a thin bar docked to the bottom edge, over nothing key.
    ("docked-bottom-bar.html",
     '<div style="position:fixed;left:0;right:0;bottom:0;padding:12px 24px;background:#fff;'
     'border-top:1px solid #ccc">We use cookies. <button>Reject</button>'
     '<button>Accept</button></div>'),
    # A slim header pinned to the top.
    ("pinned-header.html",
     '<header style="position:fixed;top:0;left:0;right:0;height:56px;background:#fff">'
     'Brand</header>'),
    # A small chat bubble in the corner.
    ("chat-bubble.html",
     '<button style="position:fixed;right:16px;bottom:16px;width:56px;height:56px;'
     'border-radius:50%;background:#333;color:#fff">?</button>'),
    # A full-screen grain overlay that takes no pointer.
    ("grain-overlay.html",
     '<div aria-hidden="true" style="position:fixed;inset:0;pointer-events:none;'
     'background:rgba(0,0,0,.04)"></div>'),
    # A closed dialog.
    ("closed-dialog.html",
     '<div style="position:fixed;inset:10%;background:#fff;display:none">Cookies</div>'),
])
def test_a_bar_that_leaves_the_page_readable_passes(tmp_path, name, extra):
    assert _hits(tmp_path, name, extra) == []
