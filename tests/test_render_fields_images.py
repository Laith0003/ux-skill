"""input-text-zooms, image-broken and image-distorted: a text field under
16px at phone widths (iOS Safari zooms the page into it), an image that
failed to load, and a photograph stretched out of its own proportions."""
from pathlib import Path

import pytest

pytest.importorskip("playwright")

from engine.render import RenderUnavailable, render_check  # noqa: E402

PNG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAUCAIAAABwJOjsAAAAJElEQVR4nGPomLlqQBDDqMWjFo9aPGrxqMWjFo9aPGrxyLEYANY4mqxAgh+RAAAAAElFTkSuQmCC"  # 40 by 20 pixels
PAGE = ('<!doctype html><html lang="en"><head><meta name="viewport" '
        'content="width=device-width,initial-scale=1"></head><body style="margin:24px">'
        '<h1>Book a table</h1>{body}</body></html>')


def _hits(tmp_path: Path, name: str, body: str, rule: str):
    f = tmp_path / name
    f.write_text(PAGE.replace("{body}", body), encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x for x in report.findings if x.rule_id == rule]


def test_a_small_field_on_a_phone_is_found(tmp_path):
    hits = _hits(tmp_path, "small.html",
                 '<label>Email <input name="email" style="font-size:14px"></label>',
                 "input-text-zooms")
    assert hits and "14px (390px viewport)" in hits[0].excerpt and "[email]" in hits[0].excerpt


def test_a_sixteen_pixel_field_and_a_checkbox_pass(tmp_path):
    body = ('<input name="email" style="font-size:16px">'
            '<input type="checkbox" style="font-size:10px">')
    assert _hits(tmp_path, "ok.html", body, "input-text-zooms") == []


def test_a_missing_image_is_found(tmp_path):
    hits = _hits(tmp_path, "broken.html",
                 '<img src="photos/missing.jpg" alt="Dining room" width="200" height="120">',
                 "image-broken")
    assert hits and "missing.jpg did not load" in hits[0].excerpt


def test_a_root_relative_image_on_a_page_from_disk_is_not_judged(tmp_path):
    body = '<img src="/media/room.jpg" alt="Dining room" width="200" height="120">'
    assert _hits(tmp_path, "rootrel.html", body, "image-broken") == []


def test_a_stretched_photo_is_found(tmp_path):
    hits = _hits(tmp_path, "stretched.html",
                 f'<img src="{PNG}" alt="Terrace" style="width:200px;height:200px">',
                 "image-distorted")
    assert hits and "40x20 pixels drawn at 200x200" in hits[0].excerpt


@pytest.mark.parametrize("name,style", [
    ("cover.html", "width:200px;height:200px;object-fit:cover"),
    ("one-side.html", "width:200px"),
])
def test_a_photo_kept_in_shape_passes(tmp_path, name, style):
    body = f'<img src="{PNG}" alt="Terrace" style="{style}">'
    assert _hits(tmp_path, name, body, "image-distorted") == []
