"""The CSS importer: custom properties on the root, theme selector blocks
and preference media queries, read in their own names; everything else
reported. Our own tokens.css comes back byte for byte apart from the
viewport layer, which is derived from tokens it reads, and a foreign file
round trips through the same exporter with its own selectors."""
import json
from pathlib import Path

import pytest

from engine.foundations import export
from engine.foundations.build import build_system
from engine.foundations.emit import InputError
from engine.foundations.export import dump_dtcg, from_dtcg, to_css
from engine.io.css_in import import_css, parse_css, read_css, write_css
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
    # Each form the file uses is recorded: the dark class as written, and
    # reduced motion under its media query alone.
    assert imported.forms == {"scheme": (".dark", ""),
                              "motion": ("", "(prefers-reduced-motion: reduce)")}
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
    assert report.entries == 17 and report.tokens == 12
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("theme.css:14", "--focus-ring", "its fallback #36f was left out; the reference holds "
                                         "the value"),
        ("theme.css:22", ".dark", "is the dark scheme; 2 properties were paired by name with "
                                  "the root's and read as scheme:dark (--text-body, "
                                  "--surface-page)")]
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
                                       "property set on a component is not a system token; "
                                       "move it to :root if it is one")]


def test_a_foreign_file_round_trips_through_its_own_selectors():
    first = _import(FOREIGN)
    text = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert '\n\n.dark {\n  color-scheme: dark;\n  --text-body: var(--paper);\n' in text
    assert ":root.dark" not in text and "data-motion" not in text
    second = _import(text)
    assert second.forms == first.forms
    assert [(t.path, t.type, t.value, t.modes, t.layer) for t in second.tokens.tokens()] == [
        (t.path, t.type, t.value, t.modes, t.layer) for t in first.tokens.tokens()]
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == text


def test_a_property_set_only_under_a_mode_is_named():
    report = _import(':root { --a: 1px; }\n[data-theme="dark"] { --b: #000; }\n').report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--b", "is set only under scheme:dark; give it a value on :root too, so the base mode "
                "has one, or import it together with the file that sets its base value")]


def test_a_class_that_sets_new_properties_is_a_component_not_a_mode():
    report = _import(":root { --a: 1px; }\n.compact { --a: 2px; --b: #000; }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--a", "is set on .compact, not on the root or a theme selector; a property set on a "
                "component is not a system token; move it to :root if it is one"),
        ("--b", "is set on .compact, not on the root or a theme selector; a property set on a "
                "component is not a system token; move it to :root if it is one")]


def test_a_class_that_switches_root_properties_is_an_axis_of_its_own():
    imported = _import(":root { --a: 1px; }\n.compact { --a: 2px; }\n")
    assert dict(imported.tokens.axes) == {"class-compact": ("off", "on")}
    assert imported.forms == {"class-compact": (".compact", "")}
    assert imported.tokens.get("a").modes == {"class-compact:on": {"value": 2, "unit": "px"}}


def test_a_reference_to_an_undefined_property_is_named():
    report = _import(":root { --a: var(--missing); }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--a", "references --missing, which this file does not define; define it or write the "
                "value, or import it together with the file that defines it")]


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
    ("html.dark {", "", {"scheme": ("html.dark", "")}, "light", 6, "html.dark"),
    ('[data-mode="dark"] {', "", {"scheme": ('[data-mode="dark"]', "")}, "light", 6,
     '[data-mode="dark"]'),
    ('[data-theme="dark"] {', "", {}, "light", 6, '[data-theme="dark"]'),
    ("[data-theme=dark] {", "", {}, "light", 6, "[data-theme=dark]"),
    ("[data-theme='dark'] {", "", {}, "light", 6, "[data-theme='dark']"),
    ("[data-mode=dark] {", "", {"scheme": ("[data-mode=dark]", "")}, "light", 6,
     "[data-mode=dark]"),
    ('[data-color-scheme="dark"] {', "", {"scheme": ('[data-color-scheme="dark"]', "")},
     "light", 6, '[data-color-scheme="dark"]'),
    ("@media screen and (prefers-color-scheme: dark) {\n  :root {", "}",
     {"scheme": ("", "(prefers-color-scheme: dark)")}, "system", 7,
     "@media screen and (prefers-color-scheme: dark) :root"),
    ("@media (prefers-color-scheme: dark) {\n  :root {", "}",
     {"scheme": ("", "(prefers-color-scheme: dark)")}, "system", 7,
     "@media (prefers-color-scheme: dark) :root"),
    ('@media (prefers-color-scheme:dark) {\n  :root {', "}",
     {"scheme": ("", "(prefers-color-scheme: dark)")}, "system", 7,
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
        (f"theme.css:{where}", label, "is the dark scheme; 2 properties were paired by name "
                                      "with the root's and read as scheme:dark (--ink, "
                                      "--paper)")]
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
    assert "\n\n.dark {\n  color-scheme: dark;\n  --ink: #EEEEEE;\n}" in out
    assert ("@media (prefers-color-scheme: dark) {\n  :root {\n    color-scheme: dark;\n"
            "    --ink: #EEEEEE;\n  }\n}") in out
    second = _import(out)
    assert (second.forms, second.scheme) == (first.forms, first.scheme)
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == out


def test_a_property_set_only_under_a_dark_class_is_named():
    report = _import(":root { --a: 1px; }\n.dark { --a: 2px; --b: #000; }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--b", "is set only under .dark; give it a value on :root too, so the base mode "
                "has one, or import it together with the file that sets its base value")]
    assert [(i.name, i.message) for i in report.notes] == [
        (".dark", "is the dark scheme; 1 property was paired by name with the root's and "
                  "read as scheme:dark (--a)")]


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
    assert (report.entries, report.tokens) == (45, 43)
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
                       "it or write the value, or import it together with the file that "
                       "defines it")
    assert report.not_read[-1].message == (
        "is set on .prose-card, not on the root or a theme selector; a property set on a "
        "component is not a system token; move it to :root if it is one")
    assert report.notes == []


def test_the_compiled_stylesheet_pairs_the_app_dark_theme_into_the_foundation():
    imported = read_css(FIXTURE / "compiled" / "app.css")
    ts, report = imported.tokens, imported.report
    assert (report.entries, report.tokens) == (59, 52)
    assert dict(ts.axes) == {"scheme": ("light", "dark"), "motion": ("standard", "reduced")}
    assert (imported.forms, imported.scheme) == (
        {"scheme": (".dark", ""), "motion": ("", "(prefers-reduced-motion: reduce)")}, "light")
    assert [t.path for t in ts.tokens() if "scheme:dark" in t.modes] == [
        "shadow-raised", "surface-page", "surface-raised", "text-primary", "text-muted",
        "border-subtle", "action-primary"]
    assert ts.get("surface-page").modes == {"scheme:dark": "{neutral-950}"}
    assert ts.get("text-muted").modes == {"scheme:dark": "#A7A49E"}
    assert ts.get("border-subtle").modes == {"scheme:dark": "#FFFFFF1F"}
    assert ts.get("default-font-family").value == "{font-sans}"
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("app.css:97", ".dark", "is the dark scheme; 7 properties were paired by name with "
                                "the root's and read as scheme:dark (--surface-page, "
                                "--surface-raised, --text-primary, --text-muted, "
                                "--border-subtle, --action-primary, --shadow-raised)")]
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
        "property set on a component is not a system token; move it to :root if it is one")
    assert report.not_read[3].message == (
        "spin 1s linear infinite is a transition or animation shorthand; write its duration "
        "and its curve as separate tokens")


def test_the_compiled_stylesheet_round_trips_through_its_own_dark_class():
    first = read_css(FIXTURE / "compiled" / "app.css")
    text = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert "\n\n.dark {\n  color-scheme: dark;\n" in text
    second = _import(text, "app.css")
    assert (second.forms, second.scheme) == (first.forms, first.scheme)
    assert [(t.path, t.type, t.value, t.modes, t.layer) for t in second.tokens.tokens()] == [
        (t.path, t.type, t.value, t.modes, t.layer) for t in first.tokens.tokens()]
    assert second.report.not_read == []
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == text


# Nested rules are rules of their own: `&` and a descendant join the
# parent's selector, and a nested block never folds into its parent.
def test_a_rule_nested_in_the_root_is_a_component_and_the_root_keeps_its_properties():
    imported = _import(":root {\n  .card { color: red; --card-pad: 16px; }\n  --a: 1px;\n}\n")
    report = imported.report
    assert [t.path for t in imported.tokens.tokens()] == ["a"]
    assert report.entries == 2
    assert [(i.where, i.name, i.message) for i in report.not_read] == [
        ("theme.css:2", "--card-pad", "is set on :root .card, not on the root or a theme "
                                      "selector; a property set on a component is not a system "
                                      "token; move it to :root if it is one")]


def test_properties_after_a_nested_rule_are_read():
    imported = _import(":root { --a: 1px; .x { --b: 2px; } --c: 3px; }\n")
    assert [t.path for t in imported.tokens.tokens()] == ["a", "c"]
    assert [i.name for i in imported.report.not_read] == ["--b"]
    assert imported.report.entries == 3


def test_a_nested_dark_class_and_a_nested_dark_query_are_the_dark_scheme():
    imported = read_css(PROBES / "nested.css")
    ts, report = imported.tokens, imported.report
    assert [t.path for t in ts.tokens()] == ["ink", "gap"]
    assert ts.get("ink").modes == {"scheme:dark": "#EEEEEE"}
    assert (imported.forms, imported.scheme) == (
        {"scheme": (":root.dark", "(prefers-color-scheme: dark)")}, "system")
    assert report.entries == 3
    assert [(i.where, i.name) for i in report.not_read] == [("nested.css:5", "--card-pad")]
    assert [(i.where, i.name) for i in report.notes] == [
        ("nested.css:3", ":root.dark"),
        ("nested.css:4", "@media (prefers-color-scheme: dark) :root")]


def test_an_unclosed_nested_block_is_named_with_its_line():
    with pytest.raises(InputError) as exc:
        _import(":root {\n  --a: 1px;\n  .x {\n    --b: 2px;\n}\n")
    assert "block opened on line 1 that never closes" in str(exc.value)


# The exporter keeps a file's own selector for an axis wherever the axis
# sits in a combined key.
def test_a_custom_form_after_an_engine_axis_round_trips():
    first = _import(':root { --gap: 8px; }\n.x { --gap: 6px; }\n'
                    '[data-density="compact"].x { --gap: 2px; }\n')
    assert first.forms == {"class-x": (".x", "")}
    text = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert ':root[data-density="compact"].x {\n  --gap: 2px;\n}' in text
    second = _import(text)
    assert second.forms == first.forms
    assert second.tokens.get("gap").modes == first.tokens.get("gap").modes
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == text


# A selector list is the root when each member is the root or a theme
# selector at its base value.
def test_a_root_list_is_the_root_for_a_mode_class():
    imported = _import(":root, :host { --a: 1px; }\n.compact { --a: 2px; }\n")
    assert dict(imported.tokens.axes) == {"class-compact": ("off", "on")}
    assert imported.tokens.get("a").modes == {"class-compact:on": {"value": 2, "unit": "px"}}
    assert imported.report.not_read == []


def test_the_root_listed_with_its_light_attribute_is_the_base():
    imported = read_css(PROBES / "root-and-light-attribute.css")
    ts, report = imported.tokens, imported.report
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert (imported.forms, imported.scheme) == ({"scheme": ("[data-ui-theme=dark]", "")},
                                                 "light")
    assert [t.path for t in ts.tokens()] == [
        "ui-blue", "ui-white", "ui-gray-900", "ui-primary", "ui-body-color", "ui-body-bg",
        "ui-font-sans-serif", "ui-body-font-size", "ui-body-line-height", "ui-border-radius",
        "ui-box-shadow"]
    assert ts.get("ui-body-bg").modes == {"scheme:dark": "#212529"}
    assert [i.name for i in report.not_read] == [
        "--ui-primary-rgb", "--ui-gradient", "--ui-link-color-rgb"]
    assert [(i.name, i.message) for i in report.notes] == [
        ("[data-ui-theme=dark]", "is the dark scheme; 2 properties were paired by name with "
                                 "the root's and read as scheme:dark (--ui-body-color, "
                                 "--ui-body-bg)")]
    text = to_css(ts, scheme=imported.scheme, forms=imported.forms)
    assert "\n\n[data-ui-theme=dark] {\n  color-scheme: dark;\n" in text
    again = _import(text)
    assert (again.forms, again.scheme) == (imported.forms, imported.scheme)


# Refusals name the input and a fix that works.
def test_a_light_scheme_query_says_where_light_values_belong():
    report = _import(":root { --ink: #111111; }\n"
                     "@media (prefers-color-scheme: light) { :root { --ink: #000000; } }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--ink", "is set under @media (prefers-color-scheme: light); light is the base "
                  "scheme, so its values belong on :root")]


def test_a_third_value_of_an_imported_axis_names_the_cause():
    report = _import(':root { --a: 1px; }\n[data-brand="alt"] { --a: 2px; }\n'
                     '[data-brand="other"] { --a: 3px; }\n').report
    assert [(i.where, i.name, i.message) for i in report.not_read] == [
        ("theme.css:3", "--a", 'is set under [data-brand="other"], but [data-brand] already '
                               "switches to alt; an imported axis has one value besides its "
                               "base, so give other an attribute of its own")]


@pytest.mark.parametrize("selector", [
    ":root:not(.light)", ":where(.dark)", ":host(.dark)", ".dark, .dark *", "body.dark"])
def test_a_scheme_selector_in_a_form_not_read_is_named(selector):
    text = (":root { --ink: #111111; }\n"
            f"@media (prefers-color-scheme: dark) {{ {selector} {{ --ink: #EEEEEE; }} }}\n"
            if selector == ":root:not(.light)" else
            f":root {{ --ink: #111111; }}\n{selector} {{ --ink: #EEEEEE; }}\n")
    report = _import(text).report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--ink", f"is set on {selector}, a scheme selector in a form this importer does not "
                  'read; write the dark values under .dark, [data-theme="dark"] or @media '
                  "(prefers-color-scheme: dark) on :root")]


def test_a_value_marked_important_is_named():
    report = _import(":root { --a: 4px !important; }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--a", "is marked !important; drop !important, since a token holds only the value")]


def test_a_shadow_in_em_names_the_unit():
    report = _import(":root { --s: 0 0.1em 0.2em #000; }\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--s", "0.1em is relative to the parent's font size, so it has no fixed value; write "
                "it in px or rem")]


def test_equal_dark_values_in_two_forms_are_not_a_clash():
    imported = _import(":root { --a: #000000; }\n.dark { --a: #fff; }\n"
                       "@media (prefers-color-scheme: dark) { :root { --a: #FFFFFF; } }\n")
    assert imported.report.not_read == []
    assert imported.tokens.get("a").modes == {"scheme:dark": "#FFFFFF"}
    assert [(i.where, i.name, i.message) for i in imported.report.notes
            if i.name == "--a"] == [
        ("theme.css:3", "--a", "is #fff on line 2 and #FFFFFF on line 3, both in scheme:dark: "
                               "two spellings of one value, read as one")]


def test_a_second_dark_form_says_how_it_is_written_back():
    imported = _import(":root { --ink: #111111; }\n.dark { --ink: #EEEEEE; }\n"
                       '[data-mode="dark"] { --ink: #EEEEEE; }\n')
    assert imported.forms == {"scheme": (".dark", "")}
    assert [(i.name, i.message) for i in imported.report.notes] == [
        (".dark", "is the dark scheme; 1 property was paired by name with the root's and read "
                  "as scheme:dark (--ink)"),
        ('[data-mode="dark"]', "is the dark scheme; 1 property was paired by name with the "
                               "root's and read as scheme:dark (--ink); it is written back as "
                               ".dark")]


# The real-world shapes a review probed, as neutral fixtures.
PROBES = Path(__file__).resolve().parents[1] / "fixtures" / "css_probes"


def test_hsl_channels_are_named_with_the_function_to_write():
    imported = read_css(PROBES / "hsl-channels-globals.css")
    report = imported.report
    assert [t.path for t in imported.tokens.tokens()] == ["radius"]
    assert [(i.where, i.name, i.message) for i in report.not_read][:2] == [
        ("hsl-channels-globals.css:5", "--background", "0 0% 100% is hsl channels without "
                                                       "hsl(); write hsl(0 0% 100%) or hex"),
        ("hsl-channels-globals.css:6", "--foreground", "222.2 84% 4.9% is hsl channels "
                                                       "without hsl(); write hsl(222.2 84% "
                                                       "4.9%) or hex")]
    assert [i.name for i in report.not_read] == [
        "--background", "--foreground", "--primary", "--primary-foreground", "--border"]


def test_the_oklch_form_pairs_its_dark_class_and_maps_the_vivid_color():
    imported = read_css(PROBES / "oklch-theme-inline.css")
    ts, report = imported.tokens, imported.report
    assert [t.path for t in ts.tokens()] == [
        "radius", "background", "foreground", "primary", "chart-1", "color-background",
        "color-primary"]
    assert [t.path for t in ts.tokens() if t.modes] == [
        "background", "foreground", "primary", "chart-1"]
    assert [(m.where, m.name) for m in report.mapped] == [
        ("oklch-theme-inline.css:8", "--chart-1")]
    assert [i.name for i in report.not_read] == ["--radius-sm"]
    assert [i.name for i in report.notes] == [".dark"]


def test_the_compiled_utility_theme_reads_its_theme_layer():
    imported = read_css(PROBES / "utility-compiled.css")
    ts, report = imported.tokens, imported.report
    assert len(ts.tokens()) == 12 and dict(ts.axes) == {}
    assert ts.get("default-font-family").value == "{font-sans}"
    assert [i.name for i in report.not_read] == ["--text-base--line-height"]
    assert [(m.where, m.name) for m in report.mapped] == [
        ("utility-compiled.css:6", "--color-sky-500")]
    assert report.entries == 13


def test_every_layer_is_read_through():
    imported = read_css(PROBES / "layers.css")
    ts, report = imported.tokens, imported.report
    assert [t.path for t in ts.tokens()] == ["ink", "gap", "gap-lg"]
    assert ts.get("ink").modes == {"scheme:dark": "#EEEEEE"}
    assert [i.name for i in report.not_read] == ["--btn-pad"]
    assert [i.name for i in report.notes] == ['[data-theme="dark"]']


def test_a_scoped_theme_with_no_root_is_named_with_its_fix():
    report = read_css(PROBES / "scoped-theme.css").report
    assert [(i.name, i.message) for i in report.not_read] == [
        (n, f"is set on {sel}, not on the root or a theme selector; a property set on a "
            "component is not a system token; move it to :root if it is one")
        for n, sel in [("--ink", ".theme-harbor"), ("--gap", ".theme-harbor"),
                       ("--ink", ".theme-harbor.dark")]]


# Every value that disagrees is reported; two spellings of one value never
# hide a third that differs.
def test_a_real_clash_after_two_spellings_of_one_value_is_reported():
    imported = _import(":root { --a: #000000; }\n.dark { --a: #fff; }\n"
                       "@media (prefers-color-scheme: dark) { :root { --a: #FFFFFF; } }\n"
                       '[data-mode="dark"] { --a: #123456; }\n')
    assert [(i.where, i.name, i.message) for i in imported.report.not_read] == [
        ("theme.css:4", "--a", "is #fff on line 2, #FFFFFF on line 3 and #123456 on line 4, "
                               "all in scheme:dark; keep one, or make them agree")]
    assert imported.tokens.tokens() == []
    assert [i.name for i in imported.report.notes] == []


def test_a_real_clash_in_another_mode_is_reported_beside_a_spelling_pair():
    imported = _import(":root { --a: #000000; }\n.dark { --a: #fff; }\n"
                       "@media (prefers-color-scheme: dark) { :root { --a: #FFFFFF; } }\n"
                       '[data-contrast="high"] { --a: #111111; }\n'
                       "@media (prefers-contrast: more) { :root { --a: #222222; } }\n")
    assert [(i.where, i.name, i.message) for i in imported.report.not_read] == [
        ("theme.css:5", "--a", "is #111111 on line 4 and #222222 on line 5, both in "
                               "contrast:high; keep one, or make them agree")]
    assert imported.tokens.tokens() == []


@pytest.mark.parametrize("value", ["200ms 100ms ease-out", "150ms cubic-bezier(0.2, 0, 0, 1)"])
def test_a_transition_shorthand_is_named_as_one(value):
    report = _import(f":root {{ --t: {value}; }}\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("--t", f"{value} is a transition or animation shorthand; write its duration and its "
                "curve as separate tokens")]


def test_an_attribute_that_does_not_name_the_page_theme_is_not_the_scheme():
    imported = _import(":root { --side: #FFFFFF; }\n[data-sidebar=dark] { --side: #000000; }\n")
    assert dict(imported.tokens.axes) == {}
    assert imported.tokens.get("side").modes == {}
    assert [(i.name, i.message) for i in imported.report.not_read] == [
        ("--side", "is set on [data-sidebar=dark], which sets dark on data-sidebar, a name that "
                   "does not say it themes the page; write it on :root or html to make it the "
                   "page scheme, or keep it in the component it themes")]


@pytest.mark.parametrize("selector", [":root[data-sidebar=dark]", "html[data-sidebar=dark]",
                                      "[data-color-mode=dark]", "[data-app-theme=dark]"])
def test_an_attribute_on_the_root_or_naming_the_theme_is_the_scheme(selector):
    imported = _import(f":root {{ --ink: #FFFFFF; }}\n{selector} {{ --ink: #000000; }}\n")
    assert imported.tokens.get("ink").modes == {"scheme:dark": "#000000"}
    assert imported.report.not_read == []


def test_a_screen_query_is_read_as_the_base():
    imported = _import("@media screen {\n  :root { --b: 2px; }\n}\n")
    assert imported.tokens.get("b").value == {"value": 2, "unit": "px"}
    assert imported.report.not_read == []


@pytest.mark.parametrize("attr", ["data-code-theme", "data-model", "data-remode"])
def test_an_attribute_that_holds_a_theme_word_inside_another_name_is_not_the_scheme(attr):
    imported = _import(f":root {{ --ink: #FFFFFF; }}\n[{attr}=dark] {{ --ink: #000000; }}\n")
    assert imported.tokens.get("ink").modes == {}
    assert [i.message for i in imported.report.not_read] == [
        f"is set on [{attr}=dark], which sets dark on {attr}, a name that does not say it "
        "themes the page; write it on :root or html to make it the page scheme, or keep it in "
        "the component it themes"]


@pytest.mark.parametrize("attr", ["data-theme", "data-mode", "data-color-scheme", "data-scheme"])
def test_an_attribute_named_for_the_page_theme_is_the_scheme(attr):
    imported = _import(f":root {{ --ink: #FFFFFF; }}\n[{attr}=dark] {{ --ink: #000000; }}\n")
    assert imported.tokens.get("ink").modes == {"scheme:dark": "#000000"}


def test_a_spelling_note_does_not_hide_the_scaled_note_on_the_same_property():
    text = (":root { --s-phone: 0.5; --s-wide: 0.8; --s: var(--s-phone); --size-a: 20px; "
            "--size-b: 24px; --t: calc(var(--size-a) * var(--s)); }\n"
            "@media (min-width: 640px) { :root { --s: var(--s-wide); } }\n"
            ".dark { --t: var(--size-b); }\n"
            "@media (prefers-color-scheme: dark) { :root { --t: var(--size-b, 1px); } }\n")
    notes = [i.message for i in _import(text).report.notes if i.name == "--t"]
    assert any("two spellings of one value" in n for n in notes)
    assert any(n.startswith("is calc(var(--size-a) * var(--s)), and --s scales it") for n in notes)


# The write-back gives each form the file used back as it was written.
@pytest.mark.parametrize("query, attribute", [
    ("(prefers-color-scheme: dark)", "data-theme"),
    ("(prefers-contrast: more)", "data-contrast"),
    ("(prefers-reduced-motion: reduce)", "data-motion"),
])
def test_an_axis_kept_only_in_its_media_query_is_written_back_there_alone(query, attribute):
    text = (":root {\n  --ink: #111111;\n  --ease: cubic-bezier(0.2, 0, 0, 1);\n}\n"
            f"@media {query} {{\n  :root {{\n"
            + ("    --ease: linear;\n" if "motion" in query else "    --ink: #EEEEEE;\n")
            + "  }\n}\n")
    first = _import(text)
    axis = next(iter(first.forms))
    assert first.forms == {axis: ("", query)}
    out = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert attribute not in out and ":not(" not in out
    assert f"@media {query} {{\n  :root {{\n" in out
    second = _import(out)
    assert (second.forms, second.scheme) == (first.forms, first.scheme)
    assert to_css(second.tokens, scheme=second.scheme, forms=second.forms) == out


@pytest.mark.parametrize("selector", [".dark", ":root.dark", "html.dark"])
def test_a_dark_class_is_written_back_on_the_root_it_was_written_on(selector):
    first = _import(f":root {{\n  --ink: #111111;\n}}\n{selector} {{\n  --ink: #EEEEEE;\n}}\n")
    assert first.forms == {"scheme": (selector, "")}
    out = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    assert f"\n\n{selector} {{\n  color-scheme: dark;\n  --ink: #EEEEEE;\n}}" in out
    assert out.count(".dark") == 1


GAMUT = (":root {\n  --brand: oklch(0.7 0.3 150);\n  --ink: #111111;\n  --gap: 1.5em;\n}\n"
         ".dark {\n  --brand: oklch(0.8 0.35 150);\n}\n")


def test_a_color_mapped_into_srgb_keeps_its_own_spelling_in_the_token():
    imported = _import(GAMUT)
    brand = imported.tokens.get("brand")
    assert brand.value == imported.report.mapped[0].hex
    assert brand.extensions == {
        "original": {"": "oklch(0.7 0.3 150)", "scheme:dark": "oklch(0.8 0.35 150)"},
        "read_as": {"": brand.value, "scheme:dark": brand.modes["scheme:dark"]}}
    assert imported.tokens.get("ink").extensions == {}
    # DTCG carries the spelling in the token's extensions, both ways.
    doc = json.loads(dump_dtcg(imported.tokens))
    ext = doc["brand"]["$extensions"]["io.github.laith0003.ux-skill"]
    assert ext["original"] == brand.extensions["original"]
    assert from_dtcg(doc).get("brand").extensions == brand.extensions


def test_the_write_back_gives_the_spelling_back_and_lists_what_was_not_read():
    imported = _import(GAMUT)
    out = write_css(imported)
    head = out.split("*/", 1)[0]
    assert head.startswith("/*\n * Written back from theme.css.\n")
    assert (" * 1 entry was not read on the way in and is not below; each with how to write "
            "it so it can be read:\n *   theme.css:4 --gap: 1.5em is relative to the parent's "
            "font size, so it has no fixed value; write it in px or rem\n") in head
    assert " *   theme.css:2 --brand: oklch(0.7 0.3 150), read as #" in head
    body = out.split("*/\n", 1)[1]
    assert "  --brand: oklch(0.7 0.3 150);\n" in body
    assert "\n\n.dark {\n  color-scheme: dark;\n  --brand: oklch(0.8 0.35 150);\n}" in body
    again = _import(out)
    assert [(t.path, t.value, t.modes, t.extensions) for t in again.tokens.tokens()] == [
        (t.path, t.value, t.modes, t.extensions) for t in imported.tokens.tokens()]
    assert (again.forms, again.scheme) == (imported.forms, imported.scheme)
