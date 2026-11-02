"""Cases a review of the 4.1 checks found, each a page or a line that once
gave the wrong answer: text over a positioned photo, a dark canvas, text in
a scroll container or past the scroll, a visually hidden skip link, a
padded thumbnail, apostrophes and inch marks read as quotation marks,
neutral declines read as shaming, and an empty SVG title."""
from pathlib import Path

import pytest

from engine.linter.core import lint_text

GIF = "data:image/gif;base64,R0lGODlhAQABAAAAACw="


def _lint(text, rule, ext="html"):
    return [f for f in lint_text(f"x.{ext}", text) if f.rule_id == rule]


@pytest.mark.parametrize("text", [
    "<a>No thanks, I don’t like saving money</a>",
    "<a>No thanks, I don&rsquo;t like saving money</a>",
    "<a>No thanks, I don&#39;t like saving money</a>",
    "<a>I’ll pay full price</a>",
])
def test_shaming_with_any_apostrophe_is_found(text):
    assert _lint(text, "confirmshaming")


@pytest.mark.parametrize("text", [
    "<a>No thanks, I don't need an account</a>",
    "<a>No thanks, I am not interested</a>",
    "<a>No thanks, I prefer to check out as a guest</a>",
])
def test_a_plain_decline_is_not_shaming(text):
    assert not _lint(text, "confirmshaming")


@pytest.mark.parametrize("text", [
    "<p>Don&#39;t wait, only 3 left at this price. We&#39;re restocking.</p>",
    "<p>Our 12&quot; pan, only 3 left, and the 16&quot; pan</p>",
])
def test_apostrophes_and_inch_marks_do_not_hide_a_use(text):
    assert _lint(text, "fake-urgency")


def test_a_quoted_example_inside_prose_is_still_a_mention():
    text = "<p>The overlay, &#x27;5 people are looking at this property&#x27;, is the tell.</p>"
    assert not _lint(text, "fake-urgency")


def test_an_empty_svg_title_is_not_a_page_title():
    assert not _lint('<svg><title></title><path d="M0 0"/></svg>', "title-is-a-framework-default")


pytest.importorskip("playwright")

from engine.render import RenderUnavailable, render_check  # noqa: E402

HEAD = ('<!doctype html><html lang="en"><head><meta name="viewport" '
        'content="width=device-width,initial-scale=1">{meta}<style>{css}</style></head>'
        '<body style="margin:0">{body}</body></html>')


def _render(tmp_path: Path, name: str, body: str, rule: str, css: str = "", meta: str = ""):
    f = tmp_path / name
    f.write_text(HEAD.replace("{meta}", meta).replace("{css}", css).replace("{body}", body),
                 encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x for x in report.findings if x.rule_id == rule]


def test_white_text_over_a_positioned_photo_is_left_to_the_scrim_check(tmp_path):
    body = (f'<section style="position:relative;height:500px"><img src="{GIF}" alt="" '
            'style="position:absolute;inset:0;width:100%;height:100%">'
            '<div style="position:relative;color:#fff;padding:40px"><h1>Field notes</h1>'
            '<p>Stories from the coast.</p></div></section>')
    assert _render(tmp_path, "hero.html", body, "text-low-contrast") == []


def test_default_text_on_a_dark_canvas_passes(tmp_path):
    body = "<main><h1>Night mode</h1><p>Plain text on the browser's own dark canvas.</p></main>"
    assert _render(tmp_path, "dark.html", body, "text-low-contrast",
                   meta='<meta name="color-scheme" content="dark">') == []


def test_text_in_a_scroll_container_is_read(tmp_path):
    css = "html,body{height:100%;overflow:hidden}main{height:100%;overflow:auto}"
    body = '<main><h1>Inbox</h1><div style="height:2400px"></div><p style="color:#bbb">Archived.</p></main>'
    assert _render(tmp_path, "shell.html", body, "text-low-contrast", css=css)


def test_a_failing_block_before_a_long_tail_is_reported(tmp_path):
    body = '<main><p style="color:#bbb">Fine print.</p><div style="height:3000px"></div></main>'
    assert _render(tmp_path, "tail.html", body, "text-low-contrast")


def test_a_visually_hidden_skip_link_is_not_a_target(tmp_path):
    css = (".sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;"
           "clip:rect(0,0,0,0);white-space:nowrap;border:0}")
    body = ('<a class="sr-only" href="#main">Skip to content</a><header>'
            '<a href="/" style="display:block;padding:16px 24px">Home</a></header><main id="main"><h1>Hi</h1></main>')
    assert _render(tmp_path, "skip.html", body, "target-too-small", css=css) == []


def test_a_padded_thumbnail_is_measured_by_its_image(tmp_path):
    import base64
    import struct
    import zlib

    def png(w, h):
        raw = b"".join(b"\x00" + b"\x88\x99\xaa" * w for _ in range(h))
        def chunk(t, d):
            return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    src = "data:image/png;base64," + base64.b64encode(png(100, 40)).decode()
    body = (f'<main><h1>Logo</h1><img src="{src}" alt="Logo" '
            'style="width:100px;height:40px;padding:6px;border:1px solid #ccc;box-sizing:content-box"></main>')
    assert _render(tmp_path, "thumb.html", body, "image-distorted") == []
