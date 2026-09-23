"""Render check: layout rules measured on the rendered page, not the source.

Regex cannot see that a centered heading's box is pinned to one edge. These
tests load real HTML in a headless browser and assert on geometry, in both
LTR and RTL. Skips cleanly when Playwright or a browser is unavailable.
"""
from pathlib import Path

import pytest

pytest.importorskip("playwright")

from engine.render import render_check, RenderUnavailable  # noqa: E402


def _ids(tmp_path: Path, name: str, html: str):
    f = tmp_path / name
    f.write_text(html, encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x.rule_id for x in report.findings]


PAGE = '<!doctype html><html{attrs}><body style="margin:0"><main style="max-width:800px">{body}</main></body></html>'


@pytest.mark.parametrize("name,attrs,body,rule", [
    # The docs/*/index.html .turn-lead bug: centered text in a max-width box
    # with margin 0 sits against the start edge (left in LTR, right in RTL).
    ("off-ltr.html", "",
     '<h2 style="text-align:center;max-width:10ch;margin:0">What if the model had a brain</h2>',
     "centered-text-off-center"),
    ("off-rtl.html", ' lang="ar" dir="rtl"',
     '<h2 style="text-align:center;max-width:10ch;margin:0">ماذا لو كان النموذج يمتلك عقل مصمم</h2>',
     "centered-text-off-center"),
    # Inherited centering: the section centers, the narrow paragraph does not.
    ("inherited.html", "",
     '<section style="text-align:center"><p style="max-width:20ch">A narrow paragraph that '
     'inherits centered text but whose box hugs the start edge.</p></section>',
     "centered-text-off-center"),
    ("overflow.html", "",
     '<div style="width:2400px">A row that is wider than the viewport.</div>',
     "horizontal-overflow"),
])
def test_render_flags(tmp_path, name, attrs, body, rule):
    assert rule in _ids(tmp_path, name, PAGE.format(attrs=attrs, body=body))


@pytest.mark.parametrize("name,attrs,body", [
    ("auto-margin.html", "",
     '<h2 style="text-align:center;max-width:10ch;margin:0 auto">What if the model had a brain</h2>'),
    ("auto-margin-rtl.html", ' lang="ar" dir="rtl"',
     '<h2 style="text-align:center;max-width:10ch;margin-inline:auto">ماذا لو كان النموذج</h2>'),
    ("full-width.html", "",
     '<p style="text-align:center">Full-width centered text is centered.</p>'),
    # Columns in a flex row are placed by the row, not by auto margins.
    ("flex-row.html", "",
     '<div style="display:flex"><p style="text-align:center;width:200px">One</p>'
     '<p style="text-align:center;width:200px">Two</p></div>'),
    ("left-aligned.html", "",
     '<p style="max-width:20ch">Start-aligned text in a narrow box is fine.</p>'),
    ("clipped.html", "",
     '<div style="overflow:hidden"><div style="width:2400px">Clipped by its parent.</div></div>'),
])
def test_render_clean(tmp_path, name, attrs, body):
    ids = _ids(tmp_path, name, PAGE.format(attrs=attrs, body=body))
    assert "centered-text-off-center" not in ids
    assert "horizontal-overflow" not in ids


def test_render_catches_drift_that_only_exists_between_breakpoints(tmp_path):
    """The docs/index.html bug: at 390px the heading's max-width exceeds its
    container (looks centered), at 1280px the flex parent shrink-wraps it
    (looks centered). Only a mid-width viewport shows the drift."""
    long = "What if the model had a designer's brain built in, deciding every time? " * 2
    # The wrapper shrink-wraps its widest child: the 600px paragraph. The
    # heading's max-width grows with the viewport. At 390 the heading fills
    # the column; at 1280 (50vw = 640) it is the widest child; at 430 and 768
    # it is narrower than the paragraph and drifts to the start edge.
    html = ('<!doctype html><html><body style="margin:0">'
            '<div style="display:flex;justify-content:center">'
            '<div style="text-align:center">'
            f'<h2 style="max-width:max(400px, 50vw);margin:0">{long}</h2>'
            f'<p style="max-width:600px;margin:0 auto">{long}</p>'
            '</div></div></body></html>')
    assert "centered-text-off-center" in _ids(tmp_path, "band.html", html)


def test_overflow_names_the_element_whose_text_spills(tmp_path):
    """docs/commands.html: a 288px paragraph holds an unbreakable string that
    runs past the viewport. The box fits; its text does not. The finding must
    point at the paragraph, not at <body>."""
    f = tmp_path / "spill.html"
    f.write_text('<!doctype html><html><body style="margin:0"><main style="padding:0 16px">'
                 '<p class="cmd-desc">Run /ux_image_to_code_with_a_very_long_unbreakable_'
                 'command_name_that_never_wraps_anywhere</p></main></body></html>',
                 encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    hit = [x for x in report.findings if x.rule_id == "horizontal-overflow"]
    assert hit and hit[0].excerpt.startswith("p.cmd-desc")


def test_render_reports_line_and_direction(tmp_path):
    f = tmp_path / "line.html"
    f.write_text(PAGE.format(attrs=' dir="rtl"', body=(
        '\n\n<h2 class="turn-lead" style="text-align:center;max-width:10ch;margin:0">'
        'ماذا لو كان النموذج يمتلك عقل مصمم</h2>')), encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    hit = [x for x in report.findings if x.rule_id == "centered-text-off-center"]
    assert hit and hit[0].line == 3
    assert "rtl" in hit[0].excerpt and "px" in hit[0].excerpt
