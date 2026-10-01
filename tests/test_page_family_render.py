"""Three inner pages built in one run are one page family: at 1440 and 390
each page has one header, one closing band and one footer, the same
instance on every page, one h1, and nothing wider than the viewport."""
import re
import struct
import zlib

import pytest

from engine.foundations import build_system, to_css
from engine.page_sequence.family import build_family
from engine.synthesizer.axes import AxisValues

PAGES = ("pricing", "about", "contact")


def _png(rgb, size=160):
    raw = b"".join(b"\x00" + bytes(rgb) * size for _ in range(size))

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))
    head = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head)
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


@pytest.fixture(scope="module")
def family(tmp_path_factory):
    out = tmp_path_factory.mktemp("family")
    css = to_css(build_system(AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), "#3366FF",
                              arabic=False).tokens)
    photos = ["kitchen.png", "street.png"]
    for name, rgb in zip(photos, ((176, 150, 120), (160, 140, 118))):
        (out / name).write_bytes(_png(rgb))
    pages = build_family(PAGES, css, brand="Night Market", action="Book a table", photos=photos,
                         photo_alts=["The kitchen at the start of service",
                                     "The street outside at dusk"])
    for page, text in pages.items():
        (out / f"{page}.html").write_text(text, encoding="utf-8")
    return out, pages


def _shared(text, tag, cls):
    m = re.search(rf'<{tag} class="{cls}"[^>]*>.*?</{tag}>', text, re.S)
    return re.sub(r' aria-current="page"', "", m.group(0))


def test_the_frame_is_one_instance_across_the_family(family):
    _, pages = family
    for tag, cls in (("header", "site-header"), ("section", "closing-band"),
                     ("footer", "site-footer")):
        assert len({_shared(t, tag, cls) for t in pages.values()}) == 1, cls


def test_the_header_marks_the_page_it_sits_on(family):
    _, pages = family
    for page, text in pages.items():
        assert f'<a href="{page}.html" aria-current="page">' in text
        assert text.count('aria-current="page"') == 1


def test_a_family_without_photographs_is_refused():
    with pytest.raises(ValueError, match="photos"):
        build_family(PAGES, "", brand="Night Market", action="Book a table")


def test_an_unknown_page_is_named():
    with pytest.raises(ValueError, match="pages: home is not an inner page"):
        build_family(("home",), "", brand="B", action="A", photos=["a.png"], photo_alts=["a"])


MEASURE = """() => ({
  headers: document.querySelectorAll('[data-family=header]').length,
  bands: document.querySelectorAll('[data-family=closing-band]').length,
  footers: document.querySelectorAll('[data-family=footer]').length,
  h1: document.querySelectorAll('h1').length,
  photos: [...document.querySelectorAll('main img')].filter(i => i.naturalWidth > 0).length,
  wide: document.documentElement.scrollWidth - window.innerWidth,
  over: [...document.querySelectorAll('body *')].filter(e => {
    const r = e.getBoundingClientRect(); return r.width && r.right > window.innerWidth + 1;
  }).map(e => e.tagName + '.' + e.className).slice(0, 5),
})"""


@pytest.mark.parametrize("width", [1440, 390])
def test_each_page_renders_one_frame_one_h1_and_no_overflow(family, width):
    sync_api = pytest.importorskip("playwright.sync_api")
    out, _ = family
    try:
        with sync_api.sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": 900})
            for name in PAGES:
                page.goto((out / f"{name}.html").as_uri(), wait_until="load")
                m = page.evaluate(MEASURE)
                assert (m["headers"], m["bands"], m["footers"]) == (1, 1, 1), (name, m)
                assert m["h1"] == 1, (name, m)
                assert m["photos"] >= 1, (name, m)
                assert m["wide"] <= 0 and not m["over"], (name, width, m)
            browser.close()
    except sync_api.Error as exc:
        if "Executable doesn't exist" in str(exc):
            pytest.skip(str(exc).splitlines()[0])
        raise
