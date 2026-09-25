"""The built system in a real browser: a small page that uses only the
generated tokens, measured in headless Chromium.

Modes switch on the html element (data-theme, dir, data-density,
data-motion), so each assertion flips one attribute and reads computed
styles. In dark mode the input's border must stay visible on the raised
card (WCAG 1.4.11, 3:1), measured from the colors the browser computed.
The same page, in English and in Arabic, must pass the render
check (no off-center text, no sideways scroll). Skips cleanly when
Playwright or a browser is missing, like tests/test_render.py.
"""
from string import Template

import pytest

pytest.importorskip("playwright")

from engine.foundations import build_system  # noqa: E402
from engine.foundations.color_math import contrast, hex_to_rgb, rgb_to_hex  # noqa: E402
from engine.foundations.emit import NEUTRAL, NEUTRAL_SOURCE, make_system  # noqa: E402
from engine.render import RenderUnavailable, render_check  # noqa: E402

BRAND = "#3366FF"

# Every value on this page is a token; nothing is hard coded. $lang, $dir
# and the copy are filled per direction.
PAGE = Template("""<!doctype html>
<html lang="$lang"$dir>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<link rel="stylesheet" href="tokens.css">
<style>
  body {
    margin: 0;
    background: var(--color-surface-page);
    color: var(--color-text-default);
    font-family: var(--type-text-body-font-family);
    font-size: var(--type-text-body-font-size);
    font-weight: var(--type-text-body-font-weight);
    letter-spacing: var(--type-text-body-letter-spacing);
    line-height: var(--type-text-body-line-height);
  }
  main {
    max-width: var(--layout-measure-form);
    margin-inline: auto;
    padding-block: var(--space-card-padding);
    padding-inline: var(--layout-margin-inline-phone);
  }
  .card {
    display: flex;
    flex-direction: column;
    gap: var(--space-group-gap);
    padding: var(--space-card-padding);
    background: var(--color-surface-raised);
    border: var(--border-outline) var(--border-style-default) var(--color-line-subtle);
    border-radius: var(--radius-card);
    box-shadow: var(--elevation-popover);
    transition: opacity var(--motion-reveal-duration) var(--motion-reveal-curve);
  }
  h1 {
    margin: 0;
    font-family: var(--type-text-heading-2-font-family);
    font-size: var(--type-text-heading-2-font-size);
    font-weight: var(--type-text-heading-2-font-weight);
    letter-spacing: var(--type-text-heading-2-letter-spacing);
    line-height: var(--type-text-heading-2-line-height);
  }
  .display {
    margin: 0;
    font-family: var(--type-text-heading-1-font-family);
    font-size: var(--type-text-heading-1-font-size);
    font-weight: var(--type-text-heading-1-font-weight);
    letter-spacing: var(--type-text-heading-1-letter-spacing);
    line-height: var(--type-text-heading-1-line-height);
  }
  p { margin: 0; color: var(--color-text-muted); }
  .field { display: flex; flex-direction: column; gap: var(--space-text-gap); }
  label {
    font-family: var(--type-text-ui-font-family);
    font-size: var(--type-text-ui-font-size);
    font-weight: var(--type-text-ui-font-weight);
    line-height: var(--type-text-ui-line-height);
  }
  input, button { font: inherit; min-height: var(--layout-target-min); box-sizing: border-box; }
  input {
    min-width: 0;
    padding-block: var(--space-control-padding-block);
    padding-inline: var(--space-control-padding-inline);
    color: var(--color-text-default);
    background: var(--color-surface-raised);
    border: var(--border-outline) var(--border-style-default) var(--color-line-input);
    border-radius: var(--radius-control);
  }
  button {
    align-self: flex-start;
    padding-inline: var(--space-control-padding-inline);
    color: var(--color-text-on-action);
    background: var(--color-action-primary);
    border: 0;
    border-radius: var(--radius-control);
    transition: background-color var(--motion-press-duration) var(--motion-press-curve);
  }
  input:focus-visible, button:focus-visible {
    outline: var(--border-focus-ring-width) solid var(--color-focus-ring);
    outline-offset: var(--border-focus-ring-offset);
  }
</style>
</head>
<body>
<main>
  <section class="card">
    <p class="display">$display</p>
    <h1>$heading</h1>
    <p>$body</p>
    <div class="field">
      <label for="name">$label</label>
      <input id="name" type="text" autocomplete="off">
    </div>
    <button type="button">$action</button>
  </section>
</main>
</body>
</html>
""")

COPY = {
    "ltr": dict(lang="en", dir="", title="Workspace", display="Welcome",
                heading="Create your workspace",
                body="Every color, size and space on this card comes from the generated tokens.",
                label="Workspace name", action="Continue"),
    "rtl": dict(lang="ar", dir=' dir="rtl"', title="مساحة العمل", display="أهلا",
                heading="أنشئ مساحة العمل",
                body="كل لون وحجم ومسافة في هذه البطاقة مأخوذ من الرموز المولّدة.",
                label="اسم مساحة العمل", action="متابعة"),
}


def _rgb(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"rgb({r}, {g}, {b})"


def _hex(computed: str) -> str:
    """An opaque computed color, rgb(r, g, b), as #RRGGBB."""
    assert computed.startswith("rgb("), computed
    return rgb_to_hex(tuple(int(c) for c in computed[4:-1].split(",")))


def _px(value) -> str:
    return f"{value['value']:g}px"


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    folder = tmp_path_factory.mktemp("system-page")
    system = make_system(BRAND, NEUTRAL, NEUTRAL_SOURCE)
    assert system.passed, system.report
    (folder / "tokens.css").write_text(system.files["tokens.css"], encoding="utf-8")
    for direction, copy in COPY.items():
        (folder / f"{direction}.html").write_text(PAGE.substitute(copy), encoding="utf-8")
    return folder


@pytest.fixture(scope="module")
def tokens():
    return build_system(NEUTRAL, BRAND).tokens


@pytest.fixture
def page(site):
    """A fresh browser per test. Function scope on purpose: the sync API
    keeps an event loop running while it is open, and render_check starts
    its own, so no browser may stay open across the render check tests."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = None
        errors = []
        for kwargs in ({"channel": "chrome"}, {}):
            try:
                browser = pw.chromium.launch(**kwargs)
                break
            except Exception as exc:  # browser not installed on this channel
                errors.append(str(exc).splitlines()[0])
        if browser is None:
            pytest.skip("no browser for the render test: " + "; ".join(errors))
        context = browser.new_context(viewport={"width": 390, "height": 844},
                                      color_scheme="light", reduced_motion="no-preference")
        pg = context.new_page()
        pg.goto((site / "ltr.html").as_uri())
        yield pg
        browser.close()


def _set(page, **attrs):
    """Set (or, with None, remove) attributes on the html element."""
    page.evaluate("""(attrs) => {
        for (const [k, v] of Object.entries(attrs)) {
            if (v === null) document.documentElement.removeAttribute(k);
            else document.documentElement.setAttribute(k, v);
        }
    }""", attrs)


def _style(page, selector: str, prop: str) -> str:
    """A computed style at rest: running transitions are finished first,
    so a color reads its end value, not the first frame of its fade."""
    return page.evaluate("""([s, p]) => {
        document.getAnimations().forEach(a => a.finish());
        return getComputedStyle(document.querySelector(s)).getPropertyValue(p);
    }""", [selector, prop])


def test_light_and_dark_follow_data_theme(page, tokens):
    light = tokens.resolve("color.surface.page", "")
    dark = tokens.resolve("color.surface.page", "scheme:dark")
    assert light != dark
    assert _style(page, "body", "background-color") == _rgb(light)
    assert _style(page, "body", "color") == _rgb(tokens.resolve("color.text.default", ""))
    _set(page, **{"data-theme": "dark"})
    assert _style(page, "body", "background-color") == _rgb(dark)
    assert _style(page, "body", "color") == _rgb(
        tokens.resolve("color.text.default", "scheme:dark"))
    assert _style(page, "button", "background-color") == _rgb(
        tokens.resolve("color.action.primary", "scheme:dark"))


def test_dark_input_border_is_visible_on_the_raised_card(page, tokens):
    _set(page, **{"data-theme": "dark"})
    border = _hex(_style(page, "input", "border-top-color"))
    card = _hex(_style(page, ".card", "background-color"))
    assert border == tokens.resolve("color.line.input", "scheme:dark")
    assert card == tokens.resolve("color.surface.raised", "scheme:dark")
    assert _hex(_style(page, "input", "background-color")) == card
    ratio = contrast(border, card)
    assert ratio >= 3.0, f"input border {border} on raised card {card} is {ratio:.2f}:1"


def test_dir_rtl_switches_to_the_arabic_face_and_scale(page, tokens):
    latin_family = _style(page, "body", "font-family")
    latin_size = float(_style(page, "body", "font-size").removesuffix("px"))
    heading_tracking = _style(page, "h1", "letter-spacing")
    assert tokens.resolve("type.face.text", "")[0] in latin_family.split(",")[0]
    assert heading_tracking not in ("normal", "0px"), heading_tracking

    _set(page, dir="rtl")
    arabic_first = tokens.resolve("type.face.arabic", "")[0]
    assert arabic_first in _style(page, "body", "font-family").split(",")[0]
    assert arabic_first in _style(page, "h1", "font-family").split(",")[0]
    assert float(_style(page, "body", "font-size").removesuffix("px")) > latin_size
    assert _style(page, "body", "letter-spacing") in ("normal", "0px")
    assert _style(page, "h1", "letter-spacing") in ("normal", "0px")
    assert float(_style(page, "body", "line-height").removesuffix("px")) > 0


def test_dir_rtl_sets_a_display_style_in_the_arabic_display_face(page, tokens):
    latin_display = tokens.resolve("type.face.display", "")[0]
    assert latin_display in _style(page, ".display", "font-family").split(",")[0]
    assert _style(page, ".display", "letter-spacing") not in ("normal", "0px")
    _set(page, dir="rtl")
    arabic_display = tokens.resolve("type.face.arabic-display", "")[0]
    assert arabic_display != tokens.resolve("type.face.arabic", "")[0]
    assert arabic_display in _style(page, ".display", "font-family").split(",")[0]
    assert _style(page, ".display", "letter-spacing") in ("normal", "0px")
    size = tokens.resolve("type.text.heading-1", "direction:rtl")["fontSize"]
    # the page is 390px wide, a phone, where heading-1 takes its phone factor
    factor = tokens.resolve("type.phone.heading-1", "direction:rtl")
    got = float(_style(page, ".display", "font-size").removesuffix("px"))
    assert got == pytest.approx(size["value"] * 16 * factor, abs=0.01)


def test_compact_density_shrinks_the_gaps(page, tokens):
    comfortable = _style(page, ".card", "row-gap")
    assert comfortable == _px(tokens.resolve("space.group.gap", ""))
    _set(page, **{"data-density": "compact"})
    compact = _style(page, ".card", "row-gap")
    assert compact == _px(tokens.resolve("space.group.gap", "density:compact"))
    assert float(compact.removesuffix("px")) < float(comfortable.removesuffix("px"))


def test_reduced_motion_shortens_the_reveal_and_stops_travel(page, tokens):
    standard = _style(page, ".card", "transition-duration")
    _set(page, **{"data-motion": "reduced"})
    reduced = _style(page, ".card", "transition-duration")
    ms = tokens.resolve("motion.reveal.duration", "motion:reduced")["value"]
    assert reduced == f"{ms / 1000:g}s" and reduced != standard
    distance = page.evaluate(
        "getComputedStyle(document.documentElement).getPropertyValue('--motion-reveal-distance')")
    assert distance.strip() == "0px"


@pytest.mark.parametrize("direction", ["ltr", "rtl"])
def test_the_page_passes_the_render_check(site, direction):
    try:
        report = render_check([str(site / f"{direction}.html")])
    except RenderUnavailable as exc:
        pytest.skip(str(exc))
    assert report.findings == [], [f"{f.rule_id}: {f.excerpt}" for f in report.findings]


REGIONS = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Regions</title>
<link rel="stylesheet" href="tokens.css">
<style>
  body { margin: 0; }
  main { display: flex; flex-direction: column; row-gap: var(--layout-region-gap); }
  .hero { padding-block: var(--layout-hero-padding-block); }
  section { min-block-size: 10px; }
</style>
</head>
<body>
<main>
  <section class="hero">Hero</section>
  <section>Features</section>
</main>
</body>
</html>
"""


@pytest.mark.parametrize("width, tier", [(375, "phone"), (800, "tablet"), (1100, "laptop"),
                                         (1440, "desktop")])
def test_the_region_gap_follows_the_viewport_from_one_property(site, tokens, width, tier):
    (site / "regions.html").write_text(REGIONS, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = None
        for kwargs in ({"channel": "chrome"}, {}):
            try:
                browser = pw.chromium.launch(**kwargs)
                break
            except Exception:
                continue
        if browser is None:
            pytest.skip("no browser for the render test")
        pg = browser.new_page(viewport={"width": width, "height": 800})
        pg.goto((site / "regions.html").as_uri())
        for density in (None, "compact"):
            _set(pg, **{"data-density": density})
            mode = "density:compact" if density else ""
            gap = float(_style(pg, "main", "row-gap").removesuffix("px"))
            hero = float(_style(pg, ".hero", "padding-top").removesuffix("px"))
            assert gap == tokens.resolve(f"layout.region-gap.{tier}", mode)["value"]
            assert hero == tokens.resolve(f"layout.hero.padding-block.{tier}", mode)["value"]
            if width == 375:
                assert gap <= 40, f"a phone shows a {gap:g}px gap between regions"
        browser.close()


# M3.5c items 1 and 7: the hero steps down on phones from one property,
# and an Arabic block inside a left to right page gets the Arabic type.
TYPE_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Type</title>
<link rel="stylesheet" href="tokens.css">
<style>
  body { margin: 0; }
  .body { font-family: var(--type-text-body-font-family); font-size: var(--type-text-body-font-size);
          font-weight: var(--type-text-body-font-weight); }
  .hero, .h1, .st { margin: 0; }
  .hero { font-family: var(--type-text-hero-font-family); font-size: var(--type-text-hero-font-size);
          letter-spacing: var(--type-text-hero-letter-spacing); }
  .h1 { font-family: var(--type-text-heading-1-font-family);
        font-size: var(--type-text-heading-1-font-size); }
  .st { font-size: var(--type-text-section-title-font-size); }
  .h2 { font-size: var(--type-text-heading-2-font-size); }
</style>
</head>
<body>
<p class="hero">Ship it</p><p class="h1">Heading</p><p class="st">Section</p><p class="h2">Sub</p>
<p class="body" id="latin">Latin body</p>
<div dir="rtl" lang="ar"><p class="body" id="nested">نص عربي</p><p class="h1" id="nested-h1">عنوان</p></div>
<div lang="ar"><p class="body" id="lang-only">نص عربي</p></div>
</body>
</html>
"""


def _open(site, width):
    (site / "type.html").write_text(TYPE_PAGE, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = None
    for kwargs in ({"channel": "chrome"}, {}):
        try:
            browser = pw.chromium.launch(**kwargs)
            break
        except Exception:
            continue
    if browser is None:
        pw.stop()
        pytest.skip("no browser for the render test")
    pg = browser.new_page(viewport={"width": width, "height": 800})
    pg.goto((site / "type.html").as_uri())
    return pw, browser, pg


def _size(pg, selector):
    return float(_style(pg, selector, "font-size").removesuffix("px"))


def test_an_arabic_block_inside_a_latin_page_gets_the_arabic_type(site, tokens):
    pw, browser, pg = _open(site, 1024)
    try:
        arabic = tokens.resolve("type.face.arabic", "")[0]
        latin = tokens.resolve("type.face.text", "")[0]
        assert latin in _style(pg, "#latin", "font-family").split(",")[0]
        for sel in ("#nested", "#lang-only"):
            assert arabic in _style(pg, sel, "font-family").split(",")[0], sel
            want = tokens.resolve("type.text.body", "direction:rtl")["fontSize"]["value"] * 16
            assert _size(pg, sel) == pytest.approx(want), sel
        display = tokens.resolve("type.face.arabic-display", "")[0]
        assert display in _style(pg, "#nested-h1", "font-family").split(",")[0]
        _set(pg, **{"data-contrast": "high"})
        want = tokens.resolve("type.text.body", "contrast:high,direction:rtl")["fontWeight"]
        assert _style(pg, "#nested", "font-weight") == f"{want:g}"
    finally:
        browser.close()
        pw.stop()


@pytest.mark.parametrize("direction", ["ltr", "rtl"])
def test_the_hero_steps_down_on_a_phone_and_keeps_its_order(site, tokens, direction):
    mode = "direction:rtl" if direction == "rtl" else ""
    desktop = {r: tokens.resolve(f"type.text.{r}", mode)["fontSize"]["value"] * 16
               for r in ("hero", "heading-1", "section-title", "heading-2")}
    for width in (375, 1440):
        pw, browser, pg = _open(site, width)
        try:
            if direction == "rtl":
                _set(pg, dir="rtl")
            sizes = {r: _size(pg, "." + c) for r, c in
                     (("hero", "hero"), ("heading-1", "h1"), ("section-title", "st"),
                      ("heading-2", "h2"))}
        finally:
            browser.close()
            pw.stop()
        if width == 1440:
            assert sizes == pytest.approx(desktop)
        else:
            factor = tokens.resolve("type.phone.hero", "")
            assert sizes["hero"] == pytest.approx(desktop["hero"] * factor, abs=0.01)
            assert sizes["hero"] < desktop["hero"] and sizes["heading-1"] < desktop["heading-1"]
            assert sizes["hero"] > sizes["heading-1"] > sizes["section-title"] \
                > sizes["heading-2"], sizes
