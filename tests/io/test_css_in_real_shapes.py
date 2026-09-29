"""The CSS importer on stylesheets shaped like real ones: font lists with
platform keywords or a leading var(), a root selector list with theme
aliases, and a density axis whose named values both differ from the root.
Every stylesheet here is invented."""
from engine.io.css_in import import_css, write_css
from engine.io.report import Source


def _import(text, name="theme.css"):
    return import_css(text, Source(name, "css", "0" * 64, len(text)))


def _rows(items):
    return [(i.where, i.name, i.message) for i in items]


def test_a_font_list_with_platform_keywords_is_a_font_list():
    imported = _import(':root {\n  --font-ui: "Inter Text", -apple-system, BlinkMacSystemFont, '
                       '"Segoe UI", system-ui, ui-sans-serif, sans-serif;\n}\n')
    assert imported.report.not_read == []
    token = imported.tokens.get("font-ui")
    assert (token.type, token.value) == ("fontFamily", [
        "Inter Text", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "system-ui",
        "ui-sans-serif", "sans-serif"])
    assert ('--font-ui: "Inter Text", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, '
            'ui-sans-serif, sans-serif;') in write_css(imported)


def test_a_font_list_opening_with_var_reads_its_named_families():
    imported = _import(':root {\n  --font-a: "Grid Sans", sans-serif;\n'
                       '  --font-display: var(--font-a), "Rubik", sans-serif;\n}\n')
    assert imported.report.not_read == []
    assert imported.tokens.get("font-display").value == ["Rubik", "sans-serif"]
    assert _rows(imported.report.notes) == [
        ("theme.css:3", "--font-display", 'opens with var(--font-a), whose face this file sets '
                                          'elsewhere, so it was read as the named families '
                                          'after it ("Rubik", sans-serif); write that face into '
                                          "the list by name if it should lead")]


def test_a_root_list_with_theme_aliases_is_the_base():
    imported = _import(':root, .theme-harbor, [data-theme=light] {\n  --ink: #14161A;\n'
                       '  --paper: #FFFFFF;\n}\n[data-theme=dark] {\n  --ink: #F4F4F2;\n'
                       '  --paper: #121316;\n}\n')
    report = imported.report
    assert report.not_read == []
    ink = imported.tokens.get("ink")
    assert (ink.value, ink.modes) == ("#14161A", {"scheme:dark": "#F4F4F2"})
    assert _rows(report.notes)[0] == (
        "theme.css:1", ":root, .theme-harbor, [data-theme=light]",
        "names the root with .theme-harbor, so .theme-harbor holds the root's values; read as "
        "the base, and written back on :root")


DENSITY = """:root {
  --space-2: 8px;
  --space-4: 16px;
  --row: 44px;
}
[data-density="comfortable"] {
  --space-2: 10px;
  --space-4: 20px;
  --row: 52px;
}
[data-density="compact"] {
  --space-2: 6px;
  --space-4: 12px;
  --row: 36px;
}
"""


def test_the_base_is_what_the_root_holds_and_one_attribute_is_one_axis():
    imported = _import(DENSITY)
    report = imported.report
    assert report.not_read == []
    assert dict(imported.tokens.axes) == {"density": ("base", "comfortable", "compact")}
    row = imported.tokens.get("row")
    assert row.value == {"value": 44, "unit": "px"}
    assert row.modes == {"density:comfortable": {"value": 52, "unit": "px"},
                         "density:compact": {"value": 36, "unit": "px"}}
    assert _rows(report.notes) == [(
        "theme.css:6", '[data-density="comfortable"]',
        "sets values that differ from :root; the base is what :root holds, so [data-density] "
        "was read as one axis, density, with :root as its base and comfortable and compact as "
        "its modes")]


def test_the_report_never_names_a_density_value_as_the_base():
    text = _import(DENSITY).report.markdown()
    assert "Modes: density (what :root holds is the base; modes comfortable, compact)." in text
    assert "comfortable is the base" not in text


def test_the_density_modes_are_written_back_under_their_own_selectors():
    text = write_css(_import(DENSITY))
    assert ':root[data-density="comfortable"] {\n  --space-2: 10px;' in text
    assert ':root[data-density="compact"] {\n  --space-2: 6px;' in text
    again = _import(text)
    assert again.report.not_read == []
    assert dict(again.tokens.axes) == {"density": ("base", "comfortable", "compact")}
    assert again.tokens.get("row").modes == _import(DENSITY).tokens.get("row").modes


def test_the_density_axis_survives_a_dtcg_round_trip():
    from engine.foundations.export import from_dtcg, to_dtcg
    ts = _import(DENSITY).tokens
    back = from_dtcg(to_dtcg(ts))
    assert dict(back.axes) == dict(ts.axes)
    assert back.resolve("row", "density:compact") == {"value": 36, "unit": "px"}


def test_a_var_the_file_does_not_define_is_named_so():
    imported = _import(':root {\n  --font-display: var(--font-missing), "Rubik", sans-serif;\n}\n')
    [note] = imported.report.notes
    assert note.message.startswith("opens with var(--font-missing), which this file does not "
                                   "define, so it was read as the named families after it")


def test_a_base_value_rule_that_repeats_the_root_stays_the_base():
    imported = _import(':root { --row: 44px; }\n[data-density="comfortable"] { --row: 44px; }\n'
                       '[data-density="compact"] { --row: 36px; }\n')
    assert imported.report.not_read == []
    assert dict(imported.tokens.axes) == {"density": ("comfortable", "compact")}
