"""Claims the enhance report must not make about a real system: each test
is one claim an earlier report made on an invented system shaped like a
real one, and the report now says what is true instead."""
import json

import pytest

from engine.io.adapter import Mapping, propose
from engine.io.css_in import import_css
from engine.io.dtcg_in import import_dtcg
from engine.io.enhance import drift, enhance
from engine.io.report import Source
from engine.io.scan import scan
from engine.io.values_in import NotRead, read_value


def _css(text, name="tokens.css"):
    return import_css(text, Source(name, "css", "0" * 64, len(text)))


def _files(root, files):
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


# A flat system: literal values, a dark class that overrides some of them,
# and one layer that points at a token whose value switches by mode.
FLAT = """:root {
  --white: #ffffff;
  --surface: #ffffff;
  --card-bg: var(--surface);
  --text: #111111;
  --border: #dddddd;
}
.dark {
  --surface: #111111;
  --text: #eeeeee;
  --border: #333333;
}
"""


def test_a_dark_override_that_exists_on_purpose_is_never_called_drift():
    structure = enhance(_css(FLAT), propose(_css(FLAT).tokens)).structure
    assert not [p for p in structure if "remove the" in p or "override" in p]
    # The same with the dark values in a second DTCG file.
    light = {"border": {"subtle": {"$type": "color", "$value": "#d0d4da"}}}
    dark = {"border": {"subtle": {"$type": "color", "$value": "#2a2d33"}}}
    lt, dt = json.dumps(light), json.dumps(dark)
    imported = import_dtcg(lt, Source("tokens.json", "dtcg", "0" * 64, len(lt)),
                           (dt, Source("tokens.dark.json", "dtcg", "0" * 64, len(dt))))
    structure = enhance(imported, Mapping()).structure
    assert not [p for p in structure if "move mode values" in p or "remove the" in p]


def test_a_flat_or_theme_switching_layer_is_told_once_and_never_per_token():
    structure = enhance(_css(FLAT), propose(_css(FLAT).tokens)).structure
    assert not [p for p in structure if "alias a primitive instead" in p
                or "alias its primitive directly" in p]
    assert structure == [
        "The system is layered its own way: 4 tokens hold a value of their own, point at another "
        "token that is not a primitive, or are primitives that change by mode (such as surface, "
        "card-bg, text, border). The "
        "engine's own systems alias primitives, but a flat system, or a layer whose values "
        "switch by mode, works as it is, so nothing here needs to change"]


def test_a_tailwind_step_is_never_matched_to_a_token_of_the_same_name(tmp_path):
    root = _files(tmp_path, {"page.html": '<div class="md:flex px-6 py-4"></div>\n'})
    ts = _css(":root { --space-6: 32px; --space-4: 16px; }\n").tokens
    classes = scan([root], ts).unknown_classes
    # px-6 is 24px in Tailwind's scale, space-6 is 32px: not the same step.
    assert [(u[2], u.near) for u in classes] == [("px-6", ""), ("py-4", "space-4")]


def test_equal_values_are_offered_only_from_a_token_named_for_the_property(tmp_path):
    root = _files(tmp_path, {"app.css": ".a { padding: 12px; margin: 2px; gap: 0; }\n"
                                        ".b { padding: 16px; }\n"})
    ts = _css(":root { --hairline: 2px; --icon-sm: 12px; --none: 0px; --space-4: 16px; }\n"
              ).tokens
    d = drift(ts, scan([root], ts))
    assert [(r.value, r.tokens) for r in d.raw_with_token] == [("16px", ["space-4"])]


def test_a_rounded_class_is_never_sent_to_a_text_size(tmp_path):
    root = _files(tmp_path, {"page.html": '<div class="md:flex rounded-lg"></div>\n'})
    ts = _css(":root { --text-body-lg: 18px; --radius-card-lg: 12px; }\n").tokens
    classes = scan([root], ts).unknown_classes
    assert [(u[2], u.near) for u in classes] == [("rounded-lg", "radius-card-lg")]
    ts = _css(":root { --text-body-lg: 18px; }\n").tokens
    assert [(u[2], u.near) for u in scan([root], ts).unknown_classes] == [("rounded-lg", "")]


def test_transparent_is_never_offered_a_border_token_for_a_background(tmp_path):
    root = _files(tmp_path, {"app.css": ".ghost { background: transparent; }\n"
                                        ".field { border-color: transparent; }\n"})
    ts = _css(":root { --border-field: transparent; }\n").tokens
    d = drift(ts, scan([root], ts))
    assert [(r.value, r.tokens, [u.where() for u in r.uses]) for r in d.raw_with_token] == [
        ("#00000000", ["border-field"], ["app.css:2"])]


def test_a_white_text_on_a_photo_is_never_offered_an_on_brand_token(tmp_path):
    root = _files(tmp_path, {"app.css": ".hero-caption { color: #fff; }\n"})
    ts = _css(":root { --on-brand: #ffffff; --text-on-brand: #ffffff; --white: #ffffff; }\n"
              ).tokens
    d = drift(ts, scan([root], ts))
    assert [(r.value, r.tokens) for r in d.raw_with_token] == [("#FFFFFF", ["white"])]


def test_a_definition_line_is_never_a_use(tmp_path):
    system = (":root {\n  --blue-600: #2952cc;\n  --primary-hover: var(--blue-600);\n"
              "  --link-hover: var(--primary-hover);\n}\n")
    root = _files(tmp_path, {"tokens.css": system,
                             "app.css": ".a:hover { color: var(--link-hover); }\n"})
    ts = _css(system).tokens
    d = drift(ts, scan([root], ts))
    assert d.strays == [] and d.lies == []
    assert d.unused == []


PAD = '<div style="padding: 16px">x</div>\n'
JSX = 'export default () => <div style={{ padding: "16px" }}>x</div>;\n'
FULL = 'export default () => <Html><Body style={{ padding: "16px" }}>x</Body></Html>;\n'
EXEMPT = {
    "resources/views/errors/500.blade.php": PAD,
    "public/404.html": PAD,
    "app/global-error.tsx": JSX,
    "emails/VerifyEmail.tsx": FULL,
    "mail/welcome.html": PAD,
    "src/notifications/reset.email.tsx": JSX,
}
MEASURED = {
    "app/error.tsx": JSX,
    "src/components/error/Banner.vue": "<template>" + PAD + "</template>\n",
    "src/pages/VerifyEmail.tsx": JSX,
    "emails/components/Footer.tsx": JSX,
    "src/error/Notice.html": PAD,
}


def test_error_pages_and_email_templates_are_known_by_what_the_file_is(tmp_path):
    root = _files(tmp_path, {**EXEMPT, **MEASURED})
    imported = _css(":root { --space-4: 16px; }\n")
    scanned = scan([root], imported.tokens)
    assert sorted(f for f, _ in scanned.standalone) == sorted(EXEMPT)
    result = enhance(imported, Mapping(), scanned)
    held = [u.file for r in result.drift.raw_with_token for u in r.uses]
    # App screens and components stay measured; the standalone files do not.
    assert sorted(held) == sorted(MEASURED)
    text = result.markdown()
    for name in EXEMPT:
        assert text.count(name) == 1, name
    assert ("- app/global-error.tsx is the framework's error route, which replaces the root "
            "layout and loads none of the app's stylesheets, so its raw values are not listed "
            "here.") in text
    assert ("- emails/VerifyEmail.tsx and mail/welcome.html are email templates in a mail "
            "folder, which an email client styles without the app's custom properties, so their "
            "raw values are not listed here.") in text


def test_no_dark_mode_says_which_source_was_read_and_where_dark_lives(tmp_path):
    imported = _css(":root { --bg: #ffffff; --fg: #111111; }\n")
    root = _files(tmp_path, {"theme-dark.css": ".dark {\n  --bg: #0d0d0d;\n  --fg: #f2f2f2;\n}\n"})
    confirm = enhance(imported, Mapping(), scan([root], imported.tokens)).confirm
    assert ("tokens.css, the source read, has no dark mode, but theme-dark.css sets dark values "
            "for 2 of its tokens (--bg at theme-dark.css:2 and --fg at theme-dark.css:3): the dark "
            "mode is in a second source. Read it with tokens.css as a second source (another "
            "--from on the command line, the next path in source in the MCP tool), then map the "
            "scheme axis in mapping.json to check dark.") in confirm
    confirm = enhance(imported, Mapping()).confirm
    assert ("tokens.css, the source read, has no dark mode in the mapping, so dark was not "
            "checked; if another file holds its dark values, read it with tokens.css as a "
            "second source (another --from on the command line, the next path in source in the "
            "MCP tool), and if the system has a dark mode, map it as the scheme axis in "
            "mapping.json.") in confirm


@pytest.mark.parametrize("text", ["none", "None"])
def test_none_is_an_explicit_value_not_a_keyword_from_elsewhere(text):
    with pytest.raises(NotRead) as exc:
        read_value(text)
    assert str(exc.value) == (
        f"{text} is an explicit value: it turns the property off (no shadow, no border, no "
        "curve), and no token type holds it; leave it out, or write it where it is used")


@pytest.mark.parametrize("token", ["action-fg-on-color", "button-text-on-color",
                                   "fg-on-color"])
def test_a_foreground_on_color_used_as_text_keeps_its_promise(tmp_path, token):
    root = _files(tmp_path, {"app.css": f".btn {{ color: var(--{token}); }}\n"})
    ts = _css(f":root {{ --{token}: #ffffff; }}\n").tokens
    d = drift(ts, scan([root], ts))
    assert d.lies == [] and d.strays == []


def test_names_a_density_or_theme_block_defines_are_not_missing(tmp_path):
    system = (":root { --gap: 8px; --bg: #ffffff; }\n"
              "[data-density=compact] { --cell: 2px; }\n"
              "[data-theme=dark] { --bg: #000000; --glow: #222222; }\n")
    imported = _css(system)
    root = _files(tmp_path, {"app.css": ".t { padding: var(--cell); color: var(--glow); "
                                        "margin: var(--nope); }\n"})
    result = enhance(imported, Mapping(), scan([root], imported.tokens))
    assert [m.value for m in result.drift.missing] == ["--nope"]
    text = result.markdown()
    assert "--cell, which the system does not have" not in text
    assert ("- --cell (app.css:1) is in tokens.css, so it is not missing, but it was not read "
            "as a token: at tokens.css:2 it is set only under density:compact; give it a value "
            "on :root too, so the base mode has one, or import it together with the file that "
            "sets its base value.") in text
    assert "--glow (app.css:1) is in tokens.css, so it is not missing" in text


def test_the_layering_note_agrees_with_one_token_and_names_primitives_with_modes():
    lone = _css(":root { --ink: #111111; --text: var(--ink); --text-2: var(--text); }\n")
    assert enhance(lone, Mapping()).structure == [
        "The system is layered its own way: 1 token holds a value of its own, points at another "
        "token that is not a primitive, or is a primitive that changes by mode (such as text-2). "
        "The engine's own systems alias primitives, but a flat system, or a layer whose values "
        "switch by mode, works as it is, so nothing here needs to change"]
