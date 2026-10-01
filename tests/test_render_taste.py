"""Render checks that read the page's own system and its motion.

The color budget, the photo grade lock, accent text on every ground it
lands on, loops under reduced motion and a pause control for anything that
moves on its own. Each case renders a real page in a headless browser.
"""
import math
import struct
import zlib
from pathlib import Path

import pytest

pytest.importorskip("playwright")

from engine.render import RenderUnavailable, render_check  # noqa: E402

TASTE = {"color-over-budget", "photo-grade-off", "accent-text-low-contrast",
         "infinite-animation-under-reduced-motion", "moving-content-without-pause"}


def _render(tmp_path: Path, name: str, html: str, files=None):
    for fname, data in (files or {}).items():
        (tmp_path / fname).write_bytes(data)
    f = tmp_path / name
    f.write_text(html, encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x for x in report.findings if x.rule_id in TASTE]


def _png(rgb, size=160):
    """A solid color PNG, written with the standard library."""
    raw = b"".join(b"\x00" + bytes(rgb) * size for _ in range(size))

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def _lab(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    L, A, B = 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))
    return L, B, math.hypot(A, B)


PAGE = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Page</title>'
        '<style>{css}</style></head><body style="margin:0;background:#fff;color:#1a1a1a">'
        '<main style="padding:24px">{body}</main></body></html>')
BUDGET = ":root{--color-budget-chromatic:0.06;--color-budget-bands:0}"
PROSE = "".join(f"<p>Plain paragraph {i} about the evening service and the kitchen.</p>" for i in range(8))


def test_color_over_budget_fires_when_the_text_is_mostly_brand_color(tmp_path):
    body = "".join(f'<h2 style="color:#1d4ed8">Heading {i}</h2><p style="color:#1d4ed8">Blue copy '
                   f'{i} about the evening.</p>' for i in range(6))
    hits = _render(tmp_path, "loud.html", PAGE.format(css=BUDGET, body=body))
    assert [h.rule_id for h in hits] == ["color-over-budget"]
    assert "color.budget.chromatic" in hits[0].excerpt and "text" in hits[0].excerpt


def test_color_over_budget_fires_on_chromatic_fill(tmp_path):
    body = ('<section style="background:#1d4ed8;height:900px;color:#fff"><h2>Band</h2></section>'
            + PROSE)
    hits = _render(tmp_path, "band.html", PAGE.format(css=BUDGET, body=body))
    assert [h.rule_id for h in hits] == ["color-over-budget"]
    assert "fill" in hits[0].excerpt


def test_bands_raise_the_budget(tmp_path):
    css = ":root{--color-budget-chromatic:0.06;--color-budget-bands:0.5}"
    body = ('<section style="background:#1d4ed8;height:500px;color:#fff"><h2>Band</h2></section>'
            + PROSE + '<div style="height:600px"></div>')
    assert _render(tmp_path, "banded.html", PAGE.format(css=css, body=body)) == []


def test_calm_page_within_budget_passes(tmp_path):
    body = ('<h1>Supper after nine</h1>' + PROSE
            + '<a href="/book" style="display:inline-block;padding:12px 20px;background:#1d4ed8;'
              'color:#fff">Book a table</a>')
    assert _render(tmp_path, "calm.html", PAGE.format(css=BUDGET, body=body)) == []


def test_no_system_means_no_budget(tmp_path):
    body = "".join(f'<h2 style="color:#1d4ed8">Heading {i}</h2>' for i in range(6))
    assert _render(tmp_path, "nosystem.html", PAGE.format(css="", body=body)) == []


def _grade_css(photos):
    labs = [_lab(c) for c in photos]
    mean = [sum(x[i] for x in labs) / len(labs) for i in range(3)]
    return (":root{--imagery-photo-lightness:%.1f;--imagery-photo-temperature:%.1f;"
            "--imagery-photo-chroma:%.1f;--imagery-photo-spread-lightness:8;"
            "--imagery-photo-spread-temperature:4;--imagery-photo-spread-chroma:6}" % tuple(mean))


def test_photo_grade_lock_fires_on_a_photo_out_of_line(tmp_path):
    warm, cool = (222, 196, 160), (32, 48, 74)
    body = ('<img src="warm.png" alt="The bar at dusk" width="320" height="320">'
            '<img src="cool.png" alt="The street at night" width="320" height="320">')
    hits = _render(tmp_path, "grade.html", PAGE.format(css=_grade_css([warm, cool]), body=body),
                   {"warm.png": _png(warm), "cool.png": _png(cool)})
    assert hits and {h.rule_id for h in hits} == {"photo-grade-off"}
    assert any("warm.png" in h.excerpt or "cool.png" in h.excerpt for h in hits)


def test_photo_grade_lock_passes_one_grade(tmp_path):
    a, b = (200, 170, 140), (190, 165, 136)
    body = ('<img src="a.png" alt="Bread on the rack" width="320" height="320">'
            '<img src="b.png" alt="Coffee at the bar" width="320" height="320">')
    assert _render(tmp_path, "onegrade.html", PAGE.format(css=_grade_css([a, b]), body=body),
                   {"a.png": _png(a), "b.png": _png(b)}) == []


def test_accent_text_is_measured_on_every_ground(tmp_path):
    body = ('<p><a href="/a" style="color:#2563eb">On white</a></p>'
            '<div style="background:#cbd5e1;padding:16px"><a href="/b" style="color:#2563eb">'
            'On a grey card</a></div>')
    hits = _render(tmp_path, "accent.html", PAGE.format(css="", body=body))
    assert [h.rule_id for h in hits] == ["accent-text-low-contrast"]
    assert "#cbd5e1" in hits[0].excerpt and "4.5:1" in hits[0].excerpt


def test_loop_without_reduced_motion_stop_fires(tmp_path):
    css = ("@keyframes glow{to{opacity:.4}} .glow{width:80px;height:80px;background:#ddd;"
           "animation:glow 2s ease-in-out infinite}")
    hits = _render(tmp_path, "loop.html", PAGE.format(css=css, body='<div class="glow"></div>' + PROSE))
    ids = [h.rule_id for h in hits]
    assert "infinite-animation-under-reduced-motion" in ids


def test_guarded_loop_with_pause_passes(tmp_path):
    css = ("@keyframes slide{to{transform:translateX(-50%)}} "
           "@media (prefers-reduced-motion:no-preference){.track{animation:slide 20s linear infinite}} "
           ".paused .track{animation-play-state:paused}")
    body = ('<div id="m" class="marquee"><div class="track">Open late every night</div></div>'
            '<button type="button" aria-controls="m" aria-pressed="false">Pause</button>' + PROSE)
    assert _render(tmp_path, "guarded.html", PAGE.format(css=css, body=body)) == []


def test_moving_content_without_pause_fires(tmp_path):
    css = ("@keyframes slide{to{transform:translateX(-50%)}} "
           "@media (prefers-reduced-motion:no-preference){.track{animation:slide 20s linear infinite}}")
    body = '<div class="marquee"><div class="track">Open late every night</div></div>' + PROSE
    hits = _render(tmp_path, "nopause.html", PAGE.format(css=css, body=body))
    assert [h.rule_id for h in hits] == ["moving-content-without-pause"]


def test_spinner_is_progress_not_decoration(tmp_path):
    css = ("@keyframes spin{to{transform:rotate(1turn)}} .spinner{width:24px;height:24px;"
           "border:2px solid #999;animation:spin 1s linear infinite}")
    body = '<div role="progressbar" aria-label="Loading" class="spinner"></div>' + PROSE
    assert _render(tmp_path, "spin.html", PAGE.format(css=css, body=body)) == []


def test_large_accent_text_is_held_to_the_system_floor_not_cited_as_1_4_3(tmp_path):
    body = '<h1 style="color:#3d8bfd;font-size:48px">Supper after nine</h1>' + PROSE
    hits = _render(tmp_path, "large.html", PAGE.format(css="", body=body))
    assert [h.rule_id for h in hits] == ["accent-text-low-contrast"]
    assert "system's own floor" in hits[0].excerpt and "3:1 of large text" in hits[0].excerpt


def test_small_accent_text_under_4_5_cites_1_4_3(tmp_path):
    body = '<p><a href="/a" style="color:#3d8bfd;font-size:16px">Book a table</a></p>' + PROSE
    hits = _render(tmp_path, "small.html", PAGE.format(css="", body=body))
    assert [h.rule_id for h in hits] == ["accent-text-low-contrast"]
    assert "under 4.5:1 (1.4.3)" in hits[0].excerpt


MARQUEE = ("@keyframes slide{to{transform:translateX(-50%)}} "
           "@media (prefers-reduced-motion:no-preference){.track{animation:slide 20s linear infinite}}")


@pytest.mark.parametrize("button", ['<button type="button">Display options</button>',
                                    '<button type="button">Play video</button>'])
def test_an_unrelated_button_is_no_pause_control(tmp_path, button):
    body = ('<section><div class="marquee"><div class="track">Open late every night</div></div>'
            '</section>' + button + PROSE)
    hits = _render(tmp_path, "unrelated.html", PAGE.format(css=MARQUEE, body=body))
    assert [h.rule_id for h in hits] == ["moving-content-without-pause"]


def test_a_pause_button_beside_the_motion_counts(tmp_path):
    body = ('<section><div class="marquee"><div class="track">Open late every night</div></div>'
            '<button type="button">Pause</button></section>' + PROSE)
    assert _render(tmp_path, "beside.html", PAGE.format(css=MARQUEE, body=body)) == []


def test_a_failed_photo_check_keeps_the_layout_result(tmp_path):
    css = (_grade_css([(200, 170, 140)])
           + '.wide{width:2000px;height:300px;background-image:url("http://[bad")}')
    f = tmp_path / "broken.html"
    f.write_text(PAGE.format(css=css, body='<div class="wide"></div>' + PROSE), encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    ids = {x.rule_id for x in report.findings}
    assert "render-failed" not in ids
    assert ids & {"horizontal-overflow", "overflow-x"} or any("overflow" in i for i in ids), ids


def test_category_colors_carry_meaning_and_sit_outside_the_budget(tmp_path):
    css = BUDGET + ":root{--color-category-1-text:#1d4ed8;--color-category-2-text:#9d174d}"
    body = "".join(f'<p><span style="color:var(--color-category-{1 + i % 2}-text)">Shipped order '
                   f'{i} and its line items, one per row of the table</span></p>' for i in range(10))
    assert _render(tmp_path, "pills.html", PAGE.format(css=css, body=body)) == []
