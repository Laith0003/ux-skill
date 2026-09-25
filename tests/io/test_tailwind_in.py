"""The Tailwind importer: a v4 stylesheet's @theme block and its mode
blocks, or a v3 theme a person exported as resolved JSON. JavaScript is
never run: a config file is refused with the command that exports it."""
import json
from pathlib import Path

import pytest

from engine.foundations.emit import InputError
from engine.io.report import Source
from engine.io.tailwind_in import (
    EXPORT_COMMAND, import_tailwind_css, import_tailwind_json, read_tailwind)
from engine.io.values_in import CSS_KEYWORDS, NotRead, read_value

V4 = """@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));

@theme {
  --color-*: initial;
  --color-ink: #1b1d22;
  --color-paper: #fdfdfb;
  --color-surface: var(--color-paper);
  --color-on-surface: var(--color-ink);
  --spacing: 0.25rem;
  --radius-card: 0.75rem;
  --text-body: 1rem;
  --text-body--line-height: 1.5;
  --font-sans: "Body Sans", ui-sans-serif, sans-serif;
  --ease-snap: cubic-bezier(0.3, 0, 0, 1);
  --breakpoint-tablet: 40rem;
  --shadow-card: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.dark {
  --color-surface: var(--color-ink);
  --color-on-surface: var(--color-paper);
}
"""

V3 = {
    "colors": {"inherit": "inherit", "white": "#fff",
               "moss": {"100": "#e3efe4", "700": "#2f5d3a", "DEFAULT": "#3f7a4c"}},
    "spacing": {"px": "1px", "0.5": "0.125rem", "4": "1rem"},
    "fontSize": {"sm": ["0.875rem", {"lineHeight": "1.25rem"}], "base": ["1rem", "1.5rem"]},
    "fontFamily": {"sans": ["Body Sans", "ui-sans-serif", "sans-serif"]},
    "borderRadius": {"none": "0px", "lg": "0.5rem", "full": "9999px"},
    "screens": {"md": "768px"},
    "transitionDuration": {"150": "150ms"},
    "boxShadow": {"none": "none", "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)"},
    "width": {"1/2": "50%"},
}


def test_v4_reads_the_theme_block_and_the_dark_class():
    text = V4
    imported = import_tailwind_css(text, Source("app.css", "tailwind", "0" * 64, len(text)))
    ts = imported.tokens
    assert [t.path for t in ts.tokens()] == [
        "color-ink", "color-paper", "color-surface", "color-on-surface", "spacing",
        "radius-card", "text-body", "text-body--line-height", "font-sans", "ease-snap",
        "breakpoint-tablet", "shadow-card"]
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert imported.forms == {"scheme": (".dark", "")}
    assert imported.scheme == "light"
    assert ts.get("color-surface").modes == {"scheme:dark": "{color-ink}"}
    report = imported.report
    assert report.source.format == "tailwind"
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("app.css:5", "--color-*", "clears Tailwind's default values in the --color-* "
                                   "namespace; the system holds only what this file sets"),
        ("app.css:20", ".dark", "is the dark scheme; 2 properties were paired by name with "
                                "the root's and read as scheme:dark (--color-surface, "
                                "--color-on-surface)")]
    assert report.not_read == []


def test_v3_reads_the_resolved_theme_in_its_own_names():
    text = json.dumps(V3)
    imported = import_tailwind_json(text, Source("theme.json", "tailwind-json", "0" * 64,
                                                 len(text)))
    ts = imported.tokens
    assert [(t.path, t.type) for t in ts.tokens()] == [
        ("colors.white", "color"), ("colors.moss.100", "color"), ("colors.moss.700", "color"),
        ("colors.moss.DEFAULT", "color"), ("spacing.px", "dimension"),
        ("spacing.0_5", "dimension"), ("spacing.4", "dimension"), ("fontSize.sm", "dimension"),
        ("fontSize.base", "dimension"), ("fontFamily.sans", "fontFamily"),
        ("borderRadius.none", "dimension"), ("borderRadius.lg", "dimension"),
        ("borderRadius.full", "dimension"), ("screens.md", "dimension"),
        ("transitionDuration.150", "duration"), ("boxShadow.sm", "shadow")]
    assert all(t.layer == "primitive" for t in ts.tokens())
    report = imported.report
    assert report.entries == 19 and report.tokens == 16
    assert [(i.name, i.message) for i in report.renamed] == [
        ("spacing.0.5", "read as spacing.0_5, since a path segment holds only letters, digits, "
                        "'_' and '-'")]
    assert [(i.name, i.message) for i in report.notes] == [
        ("fontSize.sm", "its line height 1.25rem was left out; the engine keeps line heights "
                        "as their own tokens, so add one if you need it"),
        ("fontSize.base", "its line height 1.5rem was left out; the engine keeps line heights "
                          "as their own tokens, so add one if you need it")]
    assert [(i.name, i.message) for i in report.not_read] == [
        ("colors.inherit", "inherit is a CSS keyword that takes its value from elsewhere, so it "
                           "has no value of its own; leave it out, or write the value it "
                           "stands for as a token"),
        ("boxShadow.none", "none is a CSS keyword that takes its value from elsewhere, so it "
                           "has no value of its own; leave it out, or write the value it "
                           "stands for as a token"),
        ("width.1/2", "50% is relative to its container, so it has no fixed value; write it in "
                      "px or rem")]


def test_a_whole_config_with_an_unresolved_extend_is_refused():
    text = json.dumps({"theme": {"extend": {"colors": {"moss": "#3f7a4c"}}}})
    with pytest.raises(InputError) as exc:
        import_tailwind_json(text, Source("cfg.json", "tailwind-json", "0" * 64, len(text)))
    assert str(exc.value) == (
        "cfg.json holds theme.extend, which Tailwind has not merged yet; export the resolved "
        f"theme instead: {EXPORT_COMMAND}")


def test_a_whole_config_reads_its_theme():
    text = json.dumps({"content": [], "theme": {"colors": {"moss": "#3f7a4c"}}})
    imported = import_tailwind_json(text, Source("cfg.json", "tailwind-json", "0" * 64,
                                                 len(text)))
    assert [t.path for t in imported.tokens.tokens()] == ["colors.moss"]


@pytest.mark.parametrize("name", ["tailwind.config.js", "tailwind.config.ts",
                                  "tailwind.config.cjs", "tailwind.config.mjs"])
def test_javascript_is_never_run(tmp_path, name):
    f = tmp_path / name
    f.write_text("module.exports = {}", encoding="utf-8")
    with pytest.raises(InputError) as exc:
        read_tailwind(f)
    assert str(exc.value) == (
        f"--from {f} is a JavaScript config, and uxskill never runs JavaScript; export the "
        f"resolved theme as JSON and pass that file: {EXPORT_COMMAND}")


def test_read_tailwind_picks_the_reader_by_extension(tmp_path):
    css = tmp_path / "app.css"
    css.write_text("@theme { --color-ink: #111; }\n", encoding="utf-8")
    js = tmp_path / "theme.json"
    js.write_text(json.dumps({"colors": {"ink": "#111"}}), encoding="utf-8")
    assert read_tailwind(css).report.source.format == "tailwind"
    assert read_tailwind(js).report.source.format == "tailwind-json"
    other = tmp_path / "theme.yaml"
    other.write_text("a: 1\n", encoding="utf-8")
    with pytest.raises(InputError, match="theme.yaml is not a Tailwind stylesheet"):
        read_tailwind(other)


# The realistic fixtures: an invented Tailwind 4 app stylesheet, and an
# invented Tailwind 3 theme in the shape resolveConfig(config).theme exports.
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "tailwind"


def _css(text, path="app.css"):
    return import_tailwind_css(text, Source(path, "tailwind", "0" * 64, len(text)))


def test_the_v4_fixture_reads_the_theme_the_layers_and_both_dark_forms():
    imported = read_tailwind(FIXTURE / "v4" / "app.css")
    ts = imported.tokens
    assert [t.path for t in ts.tokens()] == [
        "color-white", "color-black", "color-moss-100", "color-moss-500", "color-moss-700",
        "color-ink-50", "color-ink-900", "font-sans", "font-mono", "text-xs", "text-base",
        "text-base--line-height", "spacing", "breakpoint-md", "radius-lg", "shadow-sm",
        "ease-out", "default-transition-duration", "color-surface", "color-on-surface",
        "color-accent", "surface", "on-surface", "accent"]
    # A value after a nested @keyframes block is still read.
    assert ts.get("default-transition-duration").value == {"value": 150, "unit": "ms"}
    assert (dict(ts.axes), imported.forms, imported.scheme) == (
        {"scheme": ("light", "dark")}, {"scheme": (".dark", "")}, "light")
    assert {p: (ts.get(p).value, ts.get(p).modes) for p in ("surface", "on-surface", "accent")} \
        == {"surface": ("{color-ink-50}", {"scheme:dark": "{color-ink-900}"}),
            "on-surface": ("{color-ink-900}", {"scheme:dark": "{color-ink-50}"}),
            "accent": ("{color-moss-700}", {"scheme:dark": "{color-moss-100}"})}
    report = imported.report
    assert (report.entries, report.tokens) == (32, 24)
    assert [(i.where, i.name) for i in report.notes] == [
        ("app.css:10", "--color-*"), ("app.css:11", "--font-*"), ("app.css:55", ".dark"),
        ("app.css:68", ":root @variant dark")]
    assert report.notes[3].message == ("is the dark scheme; 1 property was paired by name with "
                                       "the root's and read as scheme:dark (--accent)")
    assert [(m.where, m.name, m.hex) for m in report.mapped] == [
        ("app.css:15", "--color-moss-500", "#00A440")]
    assert [(i.where, i.name) for i in report.not_read] == [
        ("app.css:24", "--text-xs--line-height"), ("app.css:33", "--animate-wiggle"),
        ("app.css:76", "--card-pad")]


def test_the_v3_fixture_reads_what_has_a_value_and_names_the_rest():
    imported = read_tailwind(FIXTURE / "v3" / "tailwind-theme.json")
    ts = imported.tokens
    report = imported.report
    assert (report.entries, report.tokens) == (68, 49)
    assert report.by_type == {"color": 12, "cubicBezier": 2, "dimension": 18, "duration": 2,
                              "fontFamily": 2, "number": 9, "shadow": 4}
    assert ts.get("fontFamily.sans").value == [
        "Body Sans", "ui-sans-serif", "system-ui", "sans-serif", "Color Emoji"]
    assert ts.get("fontFamily.display").value == ["Display Serif", "serif"]
    assert ts.get("borderRadius.DEFAULT").value == {"value": 0.25, "unit": "rem"}
    assert ts.get("transitionTimingFunction.linear").value == [0, 0, 1, 1]
    assert len(ts.get("dropShadow.md").value) == 2
    assert [i.name for i in report.renamed] == ["spacing.0.5", "spacing.1.5"]
    assert [(i.name, i.message) for i in report.notes] == [
        ("fontFamily.display", 'its fontFeatureSettings "ss01" was left out; a font family '
                               "token holds only the names"),
        ("fontSize.xs", "its line height 1rem was left out; the engine keeps line heights as "
                        "their own tokens, so add one if you need it"),
        ("fontSize.base", "its line height 1.5rem was left out; the engine keeps line heights "
                          "as their own tokens, so add one if you need it"),
        ("fontSize.hero", "its line height 1.1, letter spacing -0.02em and font weight 700 were "
                          "left out; the engine keeps these as their own tokens, so add them if "
                          "you need them")]
    by_name = {i.name: i.message for i in report.not_read}
    assert list(by_name) == [
        "accentColor.auto", "animation.none", "animation.spin", "aspectRatio.auto",
        "aspectRatio.square", "aspectRatio.video", "boxShadow.none", "colors.inherit",
        "colors.current", "cursor.auto", "cursor.pointer", "keyframes.spin",
        "letterSpacing.tight", "letterSpacing.normal", "width.auto", "width.1/2", "width.full",
        "width.screen", "zIndex.auto"]
    assert by_name["aspectRatio.video"] == ("16 / 9 is a ratio, and the engine has no ratio "
                                            "token; keep it in the component that uses it")
    assert by_name["keyframes.spin"] == ("is an animation's keyframes, not a value; keep it in "
                                         "the stylesheet that animates with it")
    assert by_name["colors.current"] == ("currentColor has no fixed value; it takes the color "
                                         "of the element it sits on, so write the color as hex")


def test_the_v4_default_palette_is_mapped_into_srgb_and_reported():
    # Tailwind 4's default blue-500, green-500 and red-600 lie outside sRGB.
    text = ("@theme {\n  --color-blue-500: oklch(62.3% 0.214 259.815);\n"
            "  --color-green-500: oklch(72.3% 0.219 149.579);\n"
            "  --color-red-600: oklch(57.7% 0.245 27.325);\n}\n")
    imported = _css(text)
    assert [(t.path, t.value) for t in imported.tokens.tokens()] == [
        ("color-blue-500", "#2B7FFF"), ("color-green-500", "#00C950"),
        ("color-red-600", "#E7000B")]
    assert [(m.where, m.name, m.original, m.hex) for m in imported.report.mapped] == [
        ("app.css:2", "--color-blue-500", "oklch(62.3% 0.214 259.815)", "#2B7FFF"),
        ("app.css:3", "--color-green-500", "oklch(72.3% 0.219 149.579)", "#00C950"),
        ("app.css:4", "--color-red-600", "oklch(57.7% 0.245 27.325)", "#E7000B")]
    assert all(0 < m.distance < 0.02 for m in imported.report.mapped)
    assert imported.report.not_read == []


@pytest.mark.parametrize("variant", [
    "@custom-variant dark (&:where([data-theme=night], [data-theme=night] *));",
    "@custom-variant dark (&:where([data-theme='night'], [data-theme='night'] *));",
    "@custom-variant dark {\n  &:where([data-theme=night], [data-theme=night] *) {\n"
    "    @slot;\n  }\n}",
])
def test_a_custom_dark_variant_names_the_dark_selector(variant):
    text = (f"{variant}\n:root {{ --surface: #fff; }}\n"
            "[data-theme=night] { --surface: #111; }\n")
    imported = _css(text)
    assert dict(imported.tokens.axes) == {"scheme": ("light", "dark")}
    # The selector is written back as the rule writes it.
    assert imported.forms == {"scheme": ("[data-theme=night]", "")}
    assert imported.tokens.get("surface").modes == {"scheme:dark": "#111111"}
    assert [i.name for i in imported.report.notes] == ["[data-theme=night]"]


def test_without_the_custom_variant_the_night_attribute_is_an_axis_of_its_own():
    imported = _css(':root { --surface: #fff; }\n[data-theme="night"] { --surface: #111; }\n')
    assert dict(imported.tokens.axes) == {"data-theme": ("base", "night")}


def test_a_nested_dark_variant_is_read_on_the_custom_selector():
    text = ("@custom-variant dark (&:is(.theme-night *));\n"
            "@layer theme {\n  :root {\n    --accent: #2f5d3a;\n    @variant dark {\n"
            "      --accent: #e3efe4;\n    }\n    --paper: #fff;\n  }\n}\n")
    imported = _css(text)
    ts = imported.tokens
    assert [t.path for t in ts.tokens()] == ["accent", "paper"]
    assert ts.get("accent").modes == {"scheme:dark": "#E3EFE4"}
    assert imported.forms == {"scheme": (".theme-night", "")}
    assert [(i.where, i.name) for i in imported.report.notes] == [
        ("app.css:5", ":root @variant dark")]


def test_a_nested_dark_variant_follows_the_system_without_a_custom_variant():
    text = ":root {\n  --accent: #2f5d3a;\n  @variant dark {\n    --accent: #e3efe4;\n  }\n}\n"
    imported = _css(text)
    assert imported.scheme == "system"
    assert imported.tokens.get("accent").modes == {"scheme:dark": "#E3EFE4"}
    assert [(i.where, i.name) for i in imported.report.notes] == [
        ("app.css:3", ":root @variant dark")]


def test_a_custom_variant_with_no_dark_values_is_noted():
    text = "@custom-variant dark (&:where(.dark, .dark *));\n@theme { --color-ink: #111; }\n"
    report = _css(text).report
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("app.css:1", "@custom-variant dark",
         "puts Tailwind's dark: variant on .dark, and this file sets no custom property there, "
         "so it holds no dark scheme; dark: utilities in markup are not theme values. Set the "
         "dark values under .dark to read them")]


def test_a_config_with_dark_mode_says_where_its_dark_values_are():
    text = json.dumps({"darkMode": "class", "content": ["./src/**/*.html"],
                       "theme": {"colors": {"ink": "#111"}}})
    imported = import_tailwind_json(text, Source("cfg.json", "tailwind-json", "0" * 64,
                                                 len(text)))
    assert [t.path for t in imported.tokens.tokens()] == ["colors.ink"]
    assert [(i.name, i.message) for i in imported.report.notes] == [
        ("darkMode", 'is "class"; Tailwind 3 writes dark values as dark: utilities in markup, '
                     "not in the theme, so this file holds no dark scheme; if a stylesheet "
                     "sets the dark values as custom properties, import that too")]


def test_a_config_without_a_theme_reads_no_config_keys():
    text = json.dumps({"content": ["./a.html"], "plugins": [], "colors": {"ink": "#111"}})
    imported = import_tailwind_json(text, Source("cfg.json", "tailwind-json", "0" * 64,
                                                 len(text)))
    assert [t.path for t in imported.tokens.tokens()] == ["colors.ink"]


def test_two_keys_that_rename_to_one_path_are_not_both_read():
    text = json.dumps({"spacing": {"0_5": "2px", "0.5": "0.125rem"}})
    report = import_tailwind_json(text, Source("t.json", "tailwind-json", "0" * 64,
                                               len(text))).report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("spacing.0.5", "is read as spacing.0_5, which an earlier key already names; rename "
                        "one of the two keys")]


def test_a_json_theme_maps_an_oklch_color_and_reports_it():
    text = json.dumps({"colors": {"blue": {"500": "oklch(62.3% 0.214 259.815)"}}})
    imported = import_tailwind_json(text, Source("t.json", "tailwind-json", "0" * 64,
                                                 len(text)))
    assert imported.tokens.get("colors.blue.500").value == "#2B7FFF"
    assert [(m.where, m.name) for m in imported.report.mapped] == [
        ("t.json colors.blue.500", "colors.blue.500")]


@pytest.mark.parametrize("word", ["inherit", "initial", "unset", "revert", "revert-layer",
                                  "auto", "none", "Inherit"])
def test_css_keywords_have_no_value_of_their_own(word):
    with pytest.raises(NotRead) as exc:
        read_value(word)
    assert str(exc.value) == (f"{word} is a CSS keyword that takes its value from elsewhere, "
                              "so it has no value of its own; leave it out, or write the value "
                              "it stands for as a token")
    assert word.lower() in CSS_KEYWORDS


def test_a_nested_dark_class_joins_the_root_selector():
    imported = _css(":root {\n  --a: #fff;\n  &.dark {\n    --a: #000;\n  }\n  --b: 2px;\n}\n")
    assert [t.path for t in imported.tokens.tokens()] == ["a", "b"]
    assert imported.tokens.get("a").modes == {"scheme:dark": "#000000"}
    assert imported.forms == {"scheme": (".dark", "")}


@pytest.mark.parametrize("variant", [
    "@custom-variant dark (&:where(:not(.light), :not(.light) *));",
    "@custom-variant dark (&:not([data-theme=light] *));",
])
def test_a_dark_variant_that_names_only_what_dark_is_not_is_not_guessed(variant):
    text = (f"{variant}\n:root {{\n  --bg: #111;\n  @variant dark {{\n    --bg: #000;\n  }}\n}}\n"
            ".card {\n  --pad: 4px;\n  @variant dark {\n    --pad: 8px;\n  }\n}\n")
    imported = _css(text)
    ts = imported.tokens
    # The root value is kept; the dark value is named, never read as the base.
    assert [(t.path, t.value, t.modes) for t in ts.tokens()] == [("bg", "#111111", {})]
    assert dict(ts.axes) == {}
    report = imported.report
    written = variant[len("@custom-variant dark ("):-len(");")]
    assert [(i.where, i.name, i.message) for i in report.notes] == [
        ("app.css:1", "@custom-variant dark",
         f"is declared as {written}, which names no dark selector, only what dark is not, so "
         "no value is read as the dark scheme through it; name one, such as "
         "&:where(.dark, .dark *), and set the dark values under that selector")]
    assert [(i.where, i.name, i.message) for i in report.not_read] == [
        ("app.css:5", "--bg",
         f"is set under :root @variant dark, and @custom-variant dark ({written}) names no dark "
         "selector, only what dark is not; name one in it, such as &:where(.dark, .dark *) or "
         "&:where([data-theme=dark], [data-theme=dark] *), and set the dark values under that "
         "selector"),
        ("app.css:9", "--pad", "is set on .card, not on the root or a theme selector; a "
                               "property set on a component is not a system token; move it to "
                               ":root if it is one"),
        ("app.css:11", "--pad", "is set on .card @variant dark, not on the root or a theme "
                                "selector; a property set on a component is not a system token; "
                                "move it to :root if it is one")]


def test_a_component_under_the_dark_variant_is_named_as_the_file_writes_it():
    text = ("@custom-variant dark (&:where([data-appearance=night], [data-appearance=night] *));\n"
            ".card {\n  --pad: 4px;\n  @variant dark {\n    --pad: 8px;\n  }\n}\n")
    report = _css(text).report
    assert [i.message.split(",")[0] for i in report.not_read] == [
        "is set on .card", "is set on .card @variant dark"]


def test_json_literals_and_a_theme_that_is_not_an_object_are_named():
    text = json.dumps({"colors": {"ink": None, "paper": True, "": {"x": "#111"}},
                       "zIndex": {"10": 10}})
    imported = import_tailwind_json(text, Source("t.json", "tailwind-json", "0" * 64,
                                                 len(text)))
    assert [(t.path, t.value) for t in imported.tokens.tokens()] == [
        ("colors._.x", "#111111"), ("zIndex.10", 10)]
    report = imported.report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("colors.ink", "is null, a JSON literal, not a theme value; write the value as a "
                       "string, or remove the key"),
        ("colors.paper", "is true, a JSON literal, not a theme value; write the value as a "
                         "string, or remove the key")]
    assert [(i.name, i.message) for i in report.renamed] == [
        ("colors..x", "read as colors._.x, since a path segment cannot be empty")]
    bad = json.dumps({"content": [], "theme": None})
    with pytest.raises(InputError) as exc:
        import_tailwind_json(bad, Source("cfg.json", "tailwind-json", "0" * 64, len(bad)))
    assert str(exc.value) == ("cfg.json holds theme as null, not an object; export the "
                              f"resolved theme instead: {EXPORT_COMMAND}")
