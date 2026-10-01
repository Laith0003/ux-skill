"""Each section contract rendered from its bindings at 1440 and 390: no
overflow, every target at least 24 by 24px (2.5.8), and one h2 (the two
heroes carry the page's one h1 instead)."""
import base64

import pytest

from engine.contracts.library import seed_sections
from engine.contracts.sections import HEROES, render_section
from engine.foundations import build_system, to_css
from engine.synthesizer.axes import AxisValues

SECTIONS = {c.name: c for c in seed_sections()}
WEBP_JS = """(rgb) => { const c = document.createElement('canvas'); c.width = 480;
  c.height = 320; const g = c.getContext('2d'); g.fillStyle = 'rgb(' + rgb.join(',') + ')';
  g.fillRect(0, 0, 480, 320); return c.toDataURL('image/webp').split(',')[1]; }"""
MEASURE = """() => {
  const vw = window.innerWidth, out = {wide: document.documentElement.scrollWidth - vw};
  out.small = [...document.querySelectorAll('a, button, summary, label, input')]
    .filter(e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
      return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 1
        && !e.closest('.sr-only') && (r.height < 24 || r.width < 24); })
    .map(e => e.tagName + ' ' + (e.textContent || '').trim().slice(0, 20));
  out.h1 = document.querySelectorAll('h1').length;
  out.h2 = document.querySelectorAll('h2').length;
  out.over = [...document.querySelectorAll('section *')].filter(e => {
    const r = e.getBoundingClientRect(); return r.width && r.right > vw + 1
      && !e.closest('.table'); }).map(e => e.tagName + '.' + e.className).slice(0, 4);
  return out; }"""


def test_a_component_contract_is_not_a_section():
    from engine.contracts.library import seed_contracts
    with pytest.raises(ValueError, match="section"):
        render_section(seed_contracts()[0])


def test_a_section_that_needs_a_photograph_refuses_none():
    with pytest.raises(ValueError, match="photos"):
        render_section(SECTIONS["hero"])


def test_every_value_is_a_role_var():
    markup, css = render_section(SECTIONS["feature-grid"], photos=[("a.webp", "A dish")])
    assert "#" not in css.replace("#plan", "") and "var(--type-text-section-title-font-size)" in css
    assert "var(--layout-landing-gap)" in css  # the tier alias tokens.css switches


@pytest.fixture(scope="module")
def browser_page():
    sync_api = pytest.importorskip("playwright.sync_api")
    try:
        pw = sync_api.sync_playwright().start()
        browser = pw.chromium.launch()
    except Exception as exc:  # no browser in this environment
        pytest.skip(str(exc).splitlines()[0])
    page = browser.new_page()
    photo = base64.b64decode(page.evaluate(WEBP_JS, [150, 120, 96]))
    yield page, photo
    browser.close()
    pw.stop()


@pytest.mark.parametrize("name", sorted(SECTIONS))
def test_each_section_renders_clean_at_1440_and_390(name, browser_page, tmp_path):
    page, photo = browser_page
    (tmp_path / "photo.webp").write_bytes(photo)
    css = to_css(build_system(AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), "#3366FF",
                              arabic=False).tokens)
    markup, section_css = render_section(SECTIONS[name], photos=[("photo.webp", "The dining room")])
    f = tmp_path / f"{name}.html"
    f.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
                 'content="width=device-width, initial-scale=1"><title>Section</title><style>'
                 f'{css}\nbody{{margin:0;font-family:var(--type-face-text)}}\n{section_css}'
                 f'</style></head><body><main>{markup}</main></body></html>', encoding="utf-8")
    for width in (1440, 390):
        page.set_viewport_size({"width": width, "height": 900})
        page.goto(f.as_uri())
        m = page.evaluate(MEASURE)
        assert m["wide"] <= 0 and not m["over"], (name, width, m)
        assert not m["small"], (name, width, m["small"])
        if name in HEROES:
            assert (m["h1"], m["h2"]) == (1, 0), (name, width, m)
        else:
            assert (m["h1"], m["h2"]) == (0, 1), (name, width, m)
