"""target-too-small: a control under 24 by 24 CSS pixels whose 24px circle
meets another control, measured at every width (WCAG 2.5.8 and its spacing
exception). A link inside a sentence and an unstyled checkbox or radio are
the criterion's own exceptions; a small target with room around it passes."""
from pathlib import Path

import pytest

pytest.importorskip("playwright")

from engine.render import RenderUnavailable, render_check  # noqa: E402

RULE = "target-too-small"
ROOT = Path(__file__).resolve().parents[1]
PAGE = ('<!doctype html><html lang="en"><head><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><style>'
        '.i{display:inline-block;width:18px;height:18px;padding:0;border:0;background:#333}'
        '</style></head><body style="margin:24px"><h1>Settings</h1>{body}</body></html>')


def _hits(tmp_path: Path, name: str, body: str):
    f = tmp_path / name
    f.write_text(PAGE.replace("{body}", body), encoding="utf-8")
    try:
        report = render_check([str(f)])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    return [x for x in report.findings if x.rule_id == RULE]


def test_crowded_small_icons_are_found(tmp_path):
    body = ('<div><button class="i" aria-label="Bold"></button>'
            '<button class="i" aria-label="Italic"></button>'
            '<button class="i" aria-label="Underline"></button></div>')
    hits = _hits(tmp_path, "toolbar.html", body)
    assert len(hits) == 3
    assert "18x18px" in hits[0].excerpt and "24px" in hits[0].fix


def test_stacked_small_links_are_found(tmp_path):
    body = ('<nav><a href="/a" style="display:block;font-size:12px;line-height:14px">A</a>'
            '<a href="/b" style="display:block;font-size:12px;line-height:14px">B</a></nav>')
    assert _hits(tmp_path, "stacked.html", body)


@pytest.mark.parametrize("name,body", [
    ("spaced-icons.html",
     '<div><button class="i" aria-label="Bold"></button>'
     '<button class="i" aria-label="Italic" style="margin-left:12px"></button></div>'),
    ("big-enough.html",
     '<div><button style="width:24px;height:24px" aria-label="A"></button>'
     '<button style="width:24px;height:24px" aria-label="B"></button></div>'),
    ("link-in-sentence.html",
     '<p style="font-size:14px">Read the <a href="/t">terms</a> and the '
     '<a href="/p">privacy notice</a> before you sign up.</p>'),
    ("native-checkboxes.html",
     '<label><input type="checkbox"> Email</label><br><label><input type="checkbox"> SMS</label>'),
    ("hidden-and-disabled.html",
     '<div aria-hidden="true"><a href="/x" class="i"></a><a href="/y" class="i"></a></div>'
     '<button class="i" disabled></button><button class="i" disabled></button>'),
])
def test_targets_the_criterion_lets_through_pass(tmp_path, name, body):
    assert _hits(tmp_path, name, body) == []


def test_the_site_passes():
    pages = [str(ROOT / "docs" / n) for n in ("index.html", "commands.html", "faq.html")]
    try:
        report = render_check(pages)
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    assert [f.excerpt for f in report.findings if f.rule_id == RULE] == []
