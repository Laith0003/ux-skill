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
    "ltr": dict(lang="en", dir="", title="Workspace", heading="Create your workspace",
                body="Every color, size and space on this card comes from the generated tokens.",
                label="Workspace name", action="Continue"),
    "rtl": dict(lang="ar", dir=' dir="rtl"', title="مساحة العمل", heading="أنشئ مساحة العمل",
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
