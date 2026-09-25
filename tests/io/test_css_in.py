"""The CSS importer: custom properties on the root, theme selector blocks
and preference media queries, read in their own names; everything else
reported. Our own tokens.css comes back byte for byte apart from the
viewport layer, which is derived from tokens it reads, and a foreign file
round trips through the same exporter with its own selectors."""
from pathlib import Path

import pytest

from engine.foundations import export
from engine.foundations.build import build_system
from engine.foundations.emit import InputError
from engine.foundations.export import to_css
from engine.io.css_in import import_css, parse_css, read_css
from engine.io.report import Source
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)

FOREIGN = """/* An invented product theme. */
:root {
  --ink-900: #14161a;
  --ink-100: rgb(236 238 242);
  --paper: #fff;
  --accent-500: oklch(0.62 0.19 255);
  --space-2: 0.5rem;
  --radius-card: 12px;
  --font-body: "Body Sans", system-ui, sans-serif;
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
  --shadow-card: 0 1px 2px rgba(0, 0, 0, 0.12);
  --text-body: var(--ink-900);
  --surface-page: var(--paper);
  --focus-ring: var(--accent-500, #36f);
  --measure: 65ch;
  --gutter: calc(var(--space-2) * 2);
  --border-card: 1px solid var(--ink-100);
  --brand-name: Inter;
  color: var(--text-body);
}

.dark {
  --text-body: var(--paper);
  --surface-page: var(--ink-900);
}

@media (prefers-reduced-motion: reduce) {
  :root { --ease-out: linear; }
}

@media (min-width: 640px) {
  :root { --space-2: 0.75rem; }
}

.card {
  --card-gap: 8px;
}

[data-density="compact"] {
  --space-2: 0.25rem;
}
"""


def _import(text, name="theme.css"):
    return import_css(text, Source(name, "css", "0" * 64, len(text)))


@pytest.mark.parametrize("scheme", ["system", "light", "dark"])
def test_our_own_tokens_css_comes_back_byte_for_byte(scheme, monkeypatch):
    ts = build_system(NEUTRAL, "#3366FF").tokens
    text = to_css(ts, scheme=scheme)
    imported = _import(text, "tokens.css")
    # The viewport layer (the responsive aliases and the phone step down)
    # is derived from tokens the import reads; without it, the file comes
    # back byte for byte.
    monkeypatch.setattr(export, "phone_roles", lambda ts: [])
    monkeypatch.setattr(export, "responsive_css", lambda ts, extra=None: [])
    assert imported.scheme == scheme
    assert to_css(imported.tokens, scheme=imported.scheme) == to_css(ts, scheme=scheme)
    report = imported.report
    assert (report.renamed, report.not_read) == ([], [])
    assert [i.name for i in report.notes] == [
        "--type-text-display-font-size", "--type-text-display-letter-spacing",
        "--type-text-hero-font-size", "--type-text-hero-letter-spacing",
        "--type-text-heading-1-font-size", "--type-text-heading-1-letter-spacing",
        "--type-text-section-title-font-size", "--type-text-section-title-letter-spacing",
        "--type-text-figure-font-size", "--type-text-figure-letter-spacing",
        "--layout-columns", "--layout-gutter", "--layout-margin-inline", "--layout-region-gap",
        "--layout-landing-gap", "--layout-hero-padding-block", "--type-text-display-scale",
        "--type-text-hero-scale", "--type-text-heading-1-scale",
        "--type-text-section-title-scale", "--type-text-figure-scale"]
    # A scale that is not 1 from the first breakpoint up: the unscaled value.
    assert report.notes[0].message == (
        "is calc(var(--type-size-latin-10) * var(--type-text-display-scale)), and "
        "--type-text-display-scale scales it with the viewport (0.4875, then 0.7742 from "
        "640px, then 0.7742 from 1024px, then 0.971 from 1280px), so it was read as "
        "var(--type-size-latin-10), its unscaled value; the viewport is not a mode, so the "
        "scale is not a token")
    assert report.notes[3].message == (
        "is calc(var(--type-tracking-step-9) * var(--type-text-hero-scale)), and "
        "--type-text-hero-scale is 1 from 640px up, so it was read as "
        "var(--type-tracking-step-9), its value from 640px up; below 640px "
        "--type-text-hero-scale scales it")
    assert report.notes[11].message == (
        "switches with the viewport (var(--layout-gutter-phone), then var(--layout-gutter-tablet) "
        "from 640px, then var(--layout-gutter-laptop) from 1024px, then "
        "var(--layout-gutter-desktop) from 1280px); the viewport is not a mode, so it was not "
        "made a token, and each property it points at is read as its own token")
    assert list(imported.tokens.axes) == ["scheme", "contrast", "density", "direction", "motion"]
    assert imported.forms == {}
    assert report.mapped == []


def test_a_right_to_left_subtree_and_a_dark_default_read_as_our_axes():
    text = (':root {\n  --ink: #111111;\n  --gap: 8px;\n}\n\n'
            ':root:not([data-theme="light"]) {\n  color-scheme: dark;\n  --ink: #EEEEEE;\n}\n\n'
            ':root [lang|="ar"] {\n  --gap: 12px;\n}\n')
    imported = _import(text)
    assert imported.scheme == "dark"
    assert dict(imported.tokens.axes) == {"scheme": ("light", "dark"),
                                          "direction": ("ltr", "rtl")}
    assert imported.tokens.get("ink").modes == {"scheme:dark": "#EEEEEE"}
    assert imported.tokens.get("gap").modes == {"direction:rtl": {"value": 12, "unit": "px"}}
    assert imported.report.not_read == []


def test_a_foreign_file_keeps_its_names_and_reads_its_modes():
    imported = _import(FOREIGN)
    ts = imported.tokens
    assert [t.path for t in ts.tokens()] == [
        "ink-900", "ink-100", "paper", "accent-500", "space-2", "radius-card", "font-body",
        "ease-out", "shadow-card", "text-body", "surface-page", "focus-ring"]
    assert dict(ts.axes) == {"scheme": ("light", "dark"), "motion": ("standard", "reduced"),
                             "density": ("comfortable", "compact")}
    assert imported.forms == {"scheme": (".dark", "")}
    assert imported.scheme == "light"
    assert ts.get("ink-100").value == "#ECEEF2"
    assert ts.get("paper").value == "#FFFFFF"
    assert ts.get("accent-500").value == "#1D84F5"
    assert ts.get("space-2").value == {"value": 0.5, "unit": "rem"}
    assert ts.get("space-2").modes == {"density:compact": {"value": 0.25, "unit": "rem"}}
    assert ts.get("space-2").layer == "semantic"
    assert (ts.get("text-body").value, ts.get("text-body").modes) == (
        "{ink-900}", {"scheme:dark": "{paper}"})
    assert ts.get("ease-out").modes == {"motion:reduced": [0, 0, 1, 1]}
    assert ts.get("font-body").value == ["Body Sans", "system-ui", "sans-serif"]
    assert ts.get("focus-ring").value == "{accent-500}"
    assert [t.path for t in ts.tokens() if t.layer == "semantic"] == [
        "space-2", "ease-out", "text-body", "surface-page", "focus-ring"]


def test_the_report_names_every_entry_it_did_not_read():
    report = _import(FOREIGN).report
    assert report.entries == 22 and report.tokens == 12
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("theme.css:14", "--focus-ring", "its fallback #36f was left out; the reference holds "
                                         "the value"),
        ("theme.css:22", ".dark", "is the dark scheme; 2 properties were paired by name with "
                                  "the root's and read as scheme:dark")]
    assert [(i.where, i.name, i.message) for i in report.not_read] == [
        ("theme.css:15", "--measure", "65ch is relative to the font, so it has no fixed value; "
                                      "write it in px or rem"),
        ("theme.css:16", "--gutter", "calc(var(--space-2) * 2) is computed by the browser; write "
                                     "the value it computes to"),
        ("theme.css:17", "--border-card", "1px solid var(--ink-100) joins several values with "
                                          "var(); split it into one token per value"),
        ("theme.css:18", "--brand-name", "Inter is a single word that could be a color name, a "
                                         "font name or a keyword; write a color as hex, and "
                                         "quote a font name"),
        ("theme.css:32", "--space-2", "is set under @media (min-width: 640px), which is not a "
                                      "mode the engine reads; it reads prefers-color-scheme, "
                                      "prefers-contrast and prefers-reduced-motion, so keep "
                                      "viewport values in the layout breakpoints"),
        ("theme.css:36", "--card-gap", "is set on .card, not on the root or a theme selector; a "
                                       "property set on a component is not a system token")]


def test_a_foreign_file_round_trips_through_its_own_selectors():
    first = _import(FOREIGN)
    text = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert ':root.dark {\n  color-scheme: dark;\n  --text-body: var(--paper);\n' in text
    second = _import(text)
    assert second.forms == first.forms
    assert [(t.path, t.type, t.value, t.modes, t.layer) for t in second.tokens.tokens()] == [
        (t.path, t.type, t.value, t.modes, t.layer) for t in first.tokens.tokens()]
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == text


def test_a_property_set_only_under_a_mode_is_named():
    report = _import(':root { --a: 1px; }\n[data-theme="dark"] { --b: #000; }\n').report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--b", "is set only under scheme:dark; give it a value on :root too, so the base mode "
                "has one")]


def test_a_class_that_sets_new_properties_is_a_component_not_a_mode():
    report = _import(":root { --a: 1px; }\n.compact { --a: 2px; --b: #000; }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--a", "is set on .compact, not on the root or a theme selector; a property set on a "
                "component is not a system token"),
        ("--b", "is set on .compact, not on the root or a theme selector; a property set on a "
                "component is not a system token")]


def test_a_class_that_switches_root_properties_is_an_axis_of_its_own():
    imported = _import(":root { --a: 1px; }\n.compact { --a: 2px; }\n")
    assert dict(imported.tokens.axes) == {"class-compact": ("off", "on")}
    assert imported.forms == {"class-compact": (".compact", "")}
    assert imported.tokens.get("a").modes == {"class-compact:on": {"value": 2, "unit": "px"}}


def test_a_reference_to_an_undefined_property_is_named():
    report = _import(":root { --a: var(--missing); }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--a", "references --missing, which this file does not define; define it or write the "
                "value")]


def test_a_selector_list_that_mixes_modes_is_named():
    report = _import(":root { --a: 1px; }\n:root, .dark { --a: 2px; }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--a", "is set under :root, .dark, which names more than one mode; split it into one "
                "rule per mode")]


def test_parse_css_gives_rules_with_their_lines_and_media():
    rules = parse_css("/* a */\n:root {\n  --a: 1px;\n}\n@media (x) {\n  .b { --c: 2; }\n}\n")
    assert [(r.selector, r.media, [(d.name, d.value, d.line) for d in r.declarations])
            for r in rules] == [(":root", (), [("--a", "1px", 3)]),
                                (".b", ("(x)",), [("--c", "2", 6)])]


def test_read_css_reads_the_file(tmp_path):
    f = tmp_path / "theme.css"
    f.write_text(":root { --a: 4px; }\n", encoding="utf-8")
    imported = read_css(f)
    assert imported.report.source.format == "css"
    assert [t.path for t in imported.tokens.tokens()] == ["a"]


def test_unbalanced_braces_are_named_with_the_line():
    with pytest.raises(InputError) as exc:
        _import(":root {\n  --a: 1px;\n")
    assert str(exc.value) == ("theme.css has a block opened on line 1 that never closes; add the "
                              "missing } and import it again")


# A dark scheme is read wherever stylesheets keep it, and each form this
# engine does not write is reported with its pairing.
@pytest.mark.parametrize("opens, form, forms, scheme, where, label", [
    (".dark {", "", {"scheme": (".dark", "")}, "light", 6, ".dark"),
    ("html.dark {", "", {"scheme": (".dark", "")}, "light", 6, "html.dark"),
    ('[data-mode="dark"] {', "", {"scheme": ('[data-mode="dark"]', "")}, "light", 6,
     '[data-mode="dark"]'),
    ('[data-theme="dark"] {', "", {}, "light", 6, '[data-theme="dark"]'),
    ("@media (prefers-color-scheme: dark) {\n  :root {", "}", {}, "system", 7,
     "@media (prefers-color-scheme: dark) :root"),
    ('@media (prefers-color-scheme:dark) {\n  :root {', "}", {}, "system", 7,
     "@media (prefers-color-scheme:dark) :root"),
])
def test_every_dark_form_pairs_into_scheme_dark(opens, form, forms, scheme, where, label):
    text = (":root {\n  --ink: #111111;\n  --paper: #FFFFFF;\n  --gap: 8px;\n}\n"
            f"{opens}\n  --ink: #EEEEEE;\n  --paper: #000000;\n}}\n{form}\n")
    imported = _import(text)
    assert imported.tokens.get("ink").modes == {"scheme:dark": "#EEEEEE"}
    assert imported.tokens.get("paper").modes == {"scheme:dark": "#000000"}
    assert imported.tokens.get("gap").modes == {}
    assert (imported.forms, imported.scheme) == (forms, scheme)
    assert [(i.where, i.name, i.message) for i in imported.report.notes] == [
        (f"theme.css:{where}", label, "is the dark scheme; 2 properties were paired by name with "
                               "the root's and read as scheme:dark")]
    assert imported.report.not_read == []


def test_the_dark_selectors_this_engine_writes_are_not_reported():
    text = (':root {\n  --ink: #111111;\n}\n:root[data-theme="dark"] {\n  --ink: #EEEEEE;\n}\n'
            '@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {\n'
            '    --ink: #EEEEEE;\n  }\n}\n')
    imported = _import(text)
    assert imported.tokens.get("ink").modes == {"scheme:dark": "#EEEEEE"}
    assert (imported.forms, imported.scheme) == ({}, "system")
    assert imported.report.notes == []


def test_a_dark_class_and_the_media_query_write_back_in_both_forms():
    text = (":root {\n  --ink: #111111;\n}\n.dark {\n  --ink: #EEEEEE;\n}\n"
            "@media (prefers-color-scheme: dark) {\n  :root {\n    --ink: #EEEEEE;\n  }\n}\n")
    first = _import(text)
    assert first.forms == {"scheme": (".dark", "(prefers-color-scheme: dark)")}
    assert first.scheme == "system"
    out = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert ":root.dark {\n  color-scheme: dark;\n  --ink: #EEEEEE;\n}" in out
    assert ("@media (prefers-color-scheme: dark) {\n  :root {\n    color-scheme: dark;\n"
            "    --ink: #EEEEEE;\n  }\n}") in out
    second = _import(out)
    assert (second.forms, second.scheme) == (first.forms, first.scheme)
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == out


def test_a_property_set_only_under_a_dark_class_is_named():
    report = _import(":root { --a: 1px; }\n.dark { --a: 2px; --b: #000; }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--b", "is set only under .dark; give it a value on :root too, so the base mode "
                "has one")]
    assert [(i.name, i.message) for i in report.notes] == [
        (".dark", "is the dark scheme; 1 property was paired by name with the root's and "
                  "read as scheme:dark")]


def test_two_dark_values_for_one_property_are_named_not_chosen():
    text = (":root {\n  --a: #111111;\n  --b: #222222;\n}\n.dark { --a: #EEEEEE; --b: #DDDDDD; }\n"
            "@media (prefers-color-scheme: dark) { :root { --a: #FFFFFF; --b: #DDDDDD; } }\n")
    imported = _import(text)
    assert [(i.where, i.name, i.message) for i in imported.report.not_read] == [
        ("theme.css:6", "--a", "is #EEEEEE on line 5 and #FFFFFF on line 6, both in "
                               "scheme:dark; keep one, or make them agree")]
    assert [t.path for t in imported.tokens.tokens()] == ["b"]
    assert imported.tokens.get("b").modes == {"scheme:dark": "#DDDDDD"}


def test_a_color_outside_srgb_is_mapped_and_reported():
    text = (":root {\n  --vivid: oklch(0.7 0.35 150);\n  --gone: oklch(0.7 0.35 150);\n}\n"
            ".dark {\n  --vivid: oklch(0.8 0.3 150);\n  --gone: 65ch;\n}\n")
    report = _import(text).report
    assert [(m.where, m.name, m.original) for m in report.mapped] == [
        ("theme.css:2", "--vivid", "oklch(0.7 0.35 150)"),
        ("theme.css:6", "--vivid", "oklch(0.8 0.3 150)")]
    assert all(m.distance > 0 for m in report.mapped)
    # A property that is not read takes its mapped colors with it.
    assert [i.name for i in report.not_read] == ["--gone"]


def test_a_rule_with_no_custom_property_sets_no_mode():
    text = (":root { --a: 1px; }\n.px-4 { padding-inline: 1rem; }\n"
            "@media (prefers-color-scheme: dark) { body { color: #fff; } }\n"
            "@media (prefers-reduced-motion: reduce) { .card { --b: 0ms; } }\n")
    imported = _import(text)
    assert dict(imported.tokens.axes) == {}
    assert imported.scheme == "system"
    assert [i.name for i in imported.report.not_read] == ["--b"]


def test_a_value_under_another_at_rule_names_its_fix():
    report = _import("@supports (display: grid) {\n  :root { --a: 1px; }\n}\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--a", "is set under @supports (display: grid), which is not a mode the engine reads; "
                "it reads prefers-color-scheme, prefers-contrast and prefers-reduced-motion, "
                "so set it on the root or under one of those")]


# A neutral foundation shaped like a real one: primitives and a semantic
# layer in a tokens file, the dark theme only in the app's globals, and the
# compiled stylesheet a utility framework builds from the two.
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "css_foundation"
SEMANTIC = ["surface-page", "surface-raised", "text-primary", "text-muted", "border-subtle",
            "action-primary", "action-primary-hover", "focus-ring", "status-danger",
            "status-success", "radius-control", "gap-stack", "motion-hover"]


def test_the_foundation_file_reads_its_primitives_and_semantic_layer():
    imported = read_css(FIXTURE / "tokens" / "foundation.css")
    ts, report = imported.tokens, imported.report
    assert (report.entries, report.tokens) == (47, 43)
    assert dict(ts.axes) == {"motion": ("standard", "reduced")}
    assert [t.path for t in ts.tokens() if t.layer == "semantic"] == [
        "ease-standard"] + SEMANTIC
    assert ts.get("motion-hover").modes == {"motion:reduced": {"value": 0, "unit": "ms"}}
    assert ts.get("overlay").value == "#11111099"
    assert ts.get("duration-base").value == {"value": 0.2, "unit": "s"}
    assert [(m.where, m.name, m.hex) for m in report.mapped] == [
        ("foundation.css:13", "--brand-300", "#8EC5FF"),
        ("foundation.css:14", "--brand-500", "#2B7FFF")]
    assert [(i.where, i.name) for i in report.not_read] == [
        ("foundation.css:35", "--tracking-tight"), ("foundation.css:40", "--content-max")]


def test_the_app_globals_alone_name_what_the_foundation_holds():
    imported = read_css(FIXTURE / "app" / "globals.css")
    report = imported.report
    assert [t.path for t in imported.tokens.tokens()] == ["header-height"]
    assert (imported.forms, imported.scheme) == ({"scheme": (".dark", "")}, "light")
    only_dark = [i.name for i in report.not_read if i.message.startswith("is set only under")]
    assert only_dark == ["--surface-page", "--surface-raised", "--text-primary", "--text-muted",
                         "--border-subtle", "--action-primary", "--shadow-raised"]
    assert report.not_read[0].message == (
        "references --surface-page, which was not read; fix --surface-page and import again")
    assert (report.not_read[5].name, report.not_read[5].message) == (
        "--radius-lg", "references --radius-control, which this file does not define; define "
                       "it or write the value")
    assert report.not_read[-1].message == (
        "is set on .prose-card, not on the root or a theme selector; a property set on a "
        "component is not a system token")
    assert report.notes == []


def test_the_compiled_stylesheet_pairs_the_app_dark_theme_into_the_foundation():
    imported = read_css(FIXTURE / "compiled" / "app.css")
    ts, report = imported.tokens, imported.report
    assert (report.entries, report.tokens) == (70, 52)
    assert dict(ts.axes) == {"scheme": ("light", "dark"), "motion": ("standard", "reduced")}
    assert (imported.forms, imported.scheme) == ({"scheme": (".dark", "")}, "light")
    assert [t.path for t in ts.tokens() if "scheme:dark" in t.modes] == [
        "shadow-raised", "surface-page", "surface-raised", "text-primary", "text-muted",
        "border-subtle", "action-primary"]
    assert ts.get("surface-page").modes == {"scheme:dark": "{neutral-950}"}
    assert ts.get("text-muted").modes == {"scheme:dark": "#A7A49E"}
    assert ts.get("border-subtle").modes == {"scheme:dark": "#FFFFFF1F"}
    assert ts.get("default-font-family").value == "{font-sans}"
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("app.css:97", ".dark", "is the dark scheme; 7 properties were paired by name with "
                                "the root's and read as scheme:dark")]
    assert [(m.where, m.name) for m in report.mapped] == [
        ("app.css:15", "--color-leaf-500"), ("app.css:40", "--brand-300"),
        ("app.css:41", "--brand-500")]
    assert [(i.where, i.name) for i in report.not_read] == [
        ("app.css:6", "--tw-shadow"), ("app.css:7", "--tw-ring-offset-width"),
        ("app.css:19", "--text-sm--line-height"), ("app.css:22", "--animate-spin"),
        ("app.css:62", "--tracking-tight"), ("app.css:67", "--content-max"),
        ("app.css:113", "--card-padding"), ("app.css:118", "--tw-shadow")]
    assert report.not_read[0].message == (
        "is set on *, :before, :after, ::backdrop, not on the root or a theme selector; a "
        "property set on a component is not a system token")
    assert report.not_read[3].message == (
        "spin 1s linear infinite is not a value this reader knows; write a hex color, a "
        "length in px or rem, a duration in ms or s, a number, a curve or a quoted font list")


def test_the_compiled_stylesheet_round_trips_through_its_own_dark_class():
    first = read_css(FIXTURE / "compiled" / "app.css")
    text = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert ":root.dark {\n  color-scheme: dark;\n" in text
    second = _import(text, "app.css")
    assert (second.forms, second.scheme) == (first.forms, first.scheme)
    assert [(t.path, t.type, t.value, t.modes, t.layer) for t in second.tokens.tokens()] == [
        (t.path, t.type, t.value, t.modes, t.layer) for t in first.tokens.tokens()]
    assert second.report.not_read == []
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == text
