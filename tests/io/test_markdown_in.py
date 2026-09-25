"""The markdown importer: a system that lives only in rule files. Token
tables (a name column and a value column, or two mode columns) and lists of
backticked names with values are read; prose, other tables and code blocks
are not tokens, and anything unreadable is reported with its file and line."""
import ast
from pathlib import Path

import pytest

from engine.foundations.errors import InputError
from engine.io.markdown_in import (
    NAME_HEADERS, PROSE_HEADERS, VALUE_HEADERS, import_markdown, read_markdown)
from engine.io.report import Source

COLOR = """# Color rules

Our brand leans warm. Never put text on the accent fill.

| Token | Light | Dark | Notes |
|---|---|---|---|
| `ink.900` | #17181c | #f4f4f2 | Body text |
| `paper` | #fbfaf7 | #121316 | Page |
| `accent` | `#c2410c` | | Links and focus |
| `text.body` | `{ink.900}` | | Alias |
| `veil` | rgba(0, 0, 0, 0.4) | rgba(0, 0, 0, 0.6) | Behind dialogs |
| Accent hover | darker accent | | prose, not a token |

| Do | Don't |
|---|---|
| Use `accent` for links | Use `accent` for body text |
"""

SPACE = """# Spacing

- `space.1`: 4px
- `space.2` = 8px
- `space.gutter`: {space.2}
- `space.huge`: 3em
- Keep gaps on the 4px grid.

```css
:root { --space-9: 36px; }
```

| Name | Value |
|---|---|
| `radius.card` | 12px |
| `space.1` | 6px |
"""

PAIRED = ("a table with Light and Dark columns; Light was read as the base and Dark as "
          "scheme:dark")


def _write(tmp_path):
    folder = tmp_path / "rules"
    folder.mkdir()
    (folder / "color.md").write_text(COLOR, encoding="utf-8")
    (folder / "space.md").write_text(SPACE, encoding="utf-8")
    return folder


def _import(text, name="rules.md"):
    return import_markdown([(name, text)], Source(name, "markdown", "0" * 64, len(text)))


def _rows(items):
    return [(i.where, i.name, i.message) for i in items]


def test_the_header_names_are_published():
    assert "token" in NAME_HEADERS and "value" in VALUE_HEADERS and "notes" in PROSE_HEADERS


def test_a_folder_of_rule_files_reads_tables_and_lists(tmp_path):
    imported = read_markdown(_write(tmp_path))
    ts = imported.tokens
    assert [t.path for t in ts.tokens()] == [
        "ink.900", "paper", "accent", "text.body", "veil", "space.1", "space.2", "space.gutter",
        "radius.card"]
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert (ts.get("ink.900").value, ts.get("ink.900").modes) == (
        "#17181C", {"scheme:dark": "#F4F4F2"})
    assert ts.get("ink.900").layer == "semantic"
    assert (ts.get("accent").value, ts.get("accent").modes, ts.get("accent").layer) == (
        "#C2410C", {}, "primitive")
    assert (ts.get("text.body").value, ts.get("text.body").layer) == ("{ink.900}", "semantic")
    assert ts.resolve("text.body", "scheme:dark") == "#F4F4F2"
    assert ts.get("veil").value == "#00000066"
    assert ts.get("space.gutter").value == "{space.2}"
    assert ts.get("space.1").value == {"value": 4, "unit": "px"}


def test_the_report_names_each_file_and_line(tmp_path):
    folder = _write(tmp_path)
    report = read_markdown(folder).report
    assert report.source.format == "markdown" and report.source.path == str(folder)
    assert report.entries == 12 and report.tokens == 9
    assert _rows(report.notes) == [
        ("color.md:5", "", PAIRED),
        ("space.md:9", "", "a css code block was not read; import the stylesheet itself with "
                           "--from and a .css file")]
    assert _rows(report.not_read) == [
        ("color.md:12", "Accent hover", "is not a token name; write the name in backticks, for "
                                        "example `color.accent`"),
        ("space.md:6", "space.huge", "3em is relative to the parent's font size, so it has no "
                                     "fixed value; write it in px or rem"),
        ("space.md:16", "space.1", "is set again with another value (6px); space.md:3 set it "
                                   "first to 4px, which was kept, so keep one")]


def test_the_digest_covers_every_file_in_name_order(tmp_path):
    folder = _write(tmp_path)
    first = read_markdown(folder).report.source
    assert first.size == len(COLOR.encode()) + len(SPACE.encode())
    (folder / "space.md").write_text(SPACE + "\n", encoding="utf-8")
    assert read_markdown(folder).report.source.sha256 != first.sha256


def test_a_single_file_reads_too(tmp_path):
    f = tmp_path / "color.md"
    f.write_text(COLOR, encoding="utf-8")
    imported = read_markdown(f)
    assert [t.path for t in imported.tokens.tokens()] == [
        "ink.900", "paper", "accent", "text.body", "veil"]


def test_an_alias_to_a_name_no_file_defines_is_named():
    report = _import("- `a`: {b.c}\n").report
    assert [(i.name, i.message) for i in report.not_read] == [
        ("a", "references b.c, which no file defines; define it or write the value")]


def test_an_alias_to_a_value_that_was_not_read_says_which():
    report = _import("- `a`: 3em\n- `b`: {a}\n- `c`: var(--b)\n").report
    assert _rows(report.not_read) == [
        ("rules.md:1", "a", "3em is relative to the parent's font size, so it has no fixed "
                            "value; write it in px or rem"),
        ("rules.md:2", "b", "references a, which was not read; fix a and import again"),
        ("rules.md:3", "c", "references b, which was not read; fix b and import again")]


def test_a_loop_of_references_is_named():
    report = _import("- `a`: {b}\n- `b`: {a}\n").report
    assert report.tokens == 0
    assert [i.message for i in report.not_read] == [
        "references only itself through a loop of references; give one of them a value"] * 2


def test_a_folder_with_no_markdown_is_named(tmp_path):
    with pytest.raises(InputError) as exc:
        read_markdown(tmp_path)
    assert str(exc.value) == (f"--from {tmp_path} holds no .md file; pass a markdown rule file or "
                              "the folder that holds them")


def test_a_file_that_is_not_utf8_is_named(tmp_path):
    f = tmp_path / "rules.md"
    f.write_bytes(b"- `a`: #fff \xff\n")
    with pytest.raises(InputError) as exc:
        read_markdown(f, "--rules")
    assert str(exc.value) == (f"--rules {f} is not UTF-8 text; save it as UTF-8 and pass it "
                              "again")


def test_a_missing_file_is_named(tmp_path):
    f = tmp_path / "gone.md"
    with pytest.raises(InputError, match=r"^--from .*gone\.md cannot be read \(.*\); pass a "):
        read_markdown(f)


def test_an_out_of_gamut_oklch_is_mapped_and_reported():
    imported = _import("| Token | Value |\n|---|---|\n| `vivid` | oklch(0.7 0.35 145) |\n")
    assert imported.tokens.get("vivid").type == "color"
    [m] = imported.report.mapped
    assert (m.where, m.name, m.original) == ("rules.md:3", "vivid", "oklch(0.7 0.35 145)")
    assert m.hex == imported.tokens.get("vivid").value and m.distance > 0


def test_a_dark_first_table_still_reads_light_as_the_base():
    text = "| Role | Dark mode | Light mode |\n|---|---|---|\n| `bg` | #000000 | #ffffff |\n"
    ts = _import(text).tokens
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert (ts.get("bg").value, ts.get("bg").modes) == ("#FFFFFF", {"scheme:dark": "#000000"})


def test_a_value_column_and_a_dark_column_read_as_base_and_dark():
    text = "| Name | Value | Dark |\n|---|---|---|\n| `bg` | #ffffff | #000000 |\n"
    ts = _import(text).tokens
    assert (ts.get("bg").value, ts.get("bg").modes) == ("#FFFFFF", {"scheme:dark": "#000000"})


def test_two_columns_named_for_another_axis_read_on_that_axis():
    text = "| Token | Comfortable | Compact |\n|---|---|---|\n| `gap` | 16px | 8px |\n"
    ts = _import(text).tokens
    assert dict(ts.axes) == {"density": ("comfortable", "compact")}
    assert ts.get("gap").modes == {"density:compact": {"value": 8, "unit": "px"}}


def test_two_columns_named_for_no_known_axis_make_their_own():
    text = "| Token | Brand | Partner |\n|---|---|---|\n| `accent` | #ff0000 | #0000ff |\n"
    imported = _import(text)
    assert dict(imported.tokens.axes) == {"brand-partner": ("brand", "partner")}
    assert imported.tokens.get("accent").modes == {"brand-partner:partner": "#0000FF"}


def test_a_value_the_mode_column_cannot_read_names_the_column():
    text = "| Token | Light | Dark |\n|---|---|---|\n| `bg` | #ffffff | calc(1px) |\n"
    report = _import(text).report
    assert _rows(report.not_read) == [
        ("rules.md:3", "bg", "in the Dark column, calc(1px) is computed by the browser; write "
                             "the value it computes to")]


def test_an_empty_base_cell_names_the_column():
    text = "| Token | Light | Dark |\n|---|---|---|\n| `bg` | | #000000 |\n"
    assert _rows(_import(text).report.not_read) == [
        ("rules.md:3", "bg", "has no value in the Light column; write one there")]


def test_a_row_short_of_cells_is_named():
    text = "| Token | Value |\n|---|---|\n| `bg` |\n"
    assert _rows(_import(text).report.not_read) == [
        ("rules.md:3", "bg", "has 1 cell where the header has 2; give the row one cell per "
                             "column")]


def test_tables_without_outer_pipes_are_read():
    text = "Token | Value\n--- | ---\n`corner.tight` | 4px\n"
    assert _import(text).tokens.get("corner.tight").value == {"value": 4, "unit": "px"}


def test_a_second_value_column_is_left_out_with_a_note():
    text = "| Token | Px | Rem |\n|---|---|---|\n| `space.4` | 16px | 1rem |\n"
    imported = _import(text)
    assert imported.tokens.get("space.4").value == {"value": 16, "unit": "px"}
    assert _rows(imported.report.notes) == [
        ("rules.md:1", "", "a table with the value columns Px and Rem; Px was read and Rem was "
                           "left out; keep one value column, or head the columns with mode names "
                           "such as Light and Dark if they differ by mode")]


def test_a_table_with_more_mode_columns_than_one_axis_is_noted():
    text = ("| Token | Light | Dark | Dim |\n|---|---|---|---|\n| `bg` | #fff | #000 | #111 |\n")
    imported = _import(text)
    assert imported.report.tokens == 0 and imported.report.entries == 0
    assert _rows(imported.report.notes) == [
        ("rules.md:1", "", "a table with the columns Light, Dark and Dim was not read; the "
                           "engine reads one value column, or two columns for a base and one "
                           "mode, so split it into tables of that shape")]


def test_mode_columns_that_cannot_name_an_axis_are_noted():
    text = "| Token | 100% | 200% |\n|---|---|---|\n| `z` | 1 | 2 |\n"
    assert _rows(_import(text).report.notes) == [
        ("rules.md:1", "", "a table with the columns 100% and 200% was not read, since a mode "
                           "is named with letters; head them with mode names such as Light and "
                           "Dark")]


def test_prose_tables_and_code_blocks_are_not_tokens():
    text = ("| Role | Description |\n|---|---|\n| `accent` | links |\n\n"
            "~~~\n- `x`: 4px\n~~~\n\n```json\n- `y`: 4px\n```\n"
            "- plain item: 4px\n- `z` is used for gaps\n")
    imported = _import(text)
    assert imported.report.entries == 0 and imported.report.notes == []
    assert imported.report.not_read == []


def test_a_name_set_twice_with_the_same_value_is_not_reported():
    report = _import("- `a`: 4px\n- `a`: `4px`\n").report
    assert report.tokens == 1 and report.entries == 2 and report.not_read == []


def test_a_name_set_again_with_another_mode_value_is_reported():
    text = ("| Token | Light | Dark |\n|---|---|---|\n| `bg` | #fff | #000 |\n"
            "| `bg` | #fff | #111 |\n")
    assert _rows(_import(text).report.not_read) == [
        ("rules.md:4", "bg", "is set again with another Dark value (#111); rules.md:3 set it "
                             "first to #000, which was kept, so keep one")]


def test_a_slash_in_a_name_reads_as_a_dot_and_is_reported():
    imported = _import("- `color/accent`: #c2410c\n")
    assert imported.tokens.has("color.accent")
    assert _rows(imported.report.renamed) == [
        ("rules.md:1", "color/accent", "read as color.accent, since a slash in a name reads as "
                                       "a dot")]


def test_a_name_in_bold_is_read():
    text = "| Token | Value |\n|---|---|\n| **brand** | #3b82f6 |\n| __ink__ | #111 |\n"
    assert [t.path for t in _import(text).tokens.tokens()] == ["brand", "ink"]


def test_a_value_that_changes_type_between_modes_is_named():
    text = "| Token | Light | Dark |\n|---|---|---|\n| `bg` | #fff | 4px |\n"
    assert _rows(_import(text).report.not_read) == [
        ("rules.md:3", "bg", "holds a color in the Light column and a dimension in the Dark "
                             "column; give it one type")]


def test_the_reader_does_not_import_the_writer():
    import engine.io.markdown_in

    tree = ast.parse(Path(engine.io.markdown_in.__file__).read_text(encoding="utf-8"))
    names = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert "engine.foundations.emit" not in names


def test_the_package_exports_the_importer():
    import engine.io

    assert engine.io.read_markdown is read_markdown
    assert {"import_markdown", "read_markdown", "Mapped", "GamutMapped"} <= set(engine.io.__all__)


def test_a_row_with_an_empty_name_cell_names_the_column():
    text = "| Token | Value |\n|---|---|\n| | #ffffff |\n"
    assert _rows(_import(text).report.not_read) == [
        ("rules.md:3", "", "has no name; write the token's name in the Token column")]


def test_two_columns_naming_the_same_mode_are_noted():
    text = "| Token | Dark | Dark mode |\n|---|---|---|\n| `bg` | #000 | #111 |\n"
    assert _rows(_import(text).report.notes) == [
        ("rules.md:1", "", "a table with the columns Dark and Dark mode was not read, since both "
                           "name the mode dark; head them with two mode names such as Light and "
                           "Dark")]


def test_a_high_contrast_column_reads_on_the_contrast_axis():
    text = "| Token | Standard | High contrast |\n|---|---|---|\n| `ink` | #333 | #000 |\n"
    ts = _import(text).tokens
    assert dict(ts.axes) == {"contrast": ("standard", "high")}
    assert ts.get("ink").modes == {"contrast:high": "#000000"}


def test_a_var_reference_is_an_alias_and_its_fallback_is_noted():
    imported = _import("- `ink`: #111\n- `text`: var(--ink, #000)\n")
    assert imported.tokens.get("text").value == "{ink}"
    assert _rows(imported.report.notes) == [
        ("rules.md:2", "text", "its fallback #000 was left out; the reference holds the value")]


def test_a_reference_the_mode_column_cannot_read_names_the_column():
    text = "| Token | Light | Dark |\n|---|---|---|\n| `bg` | #fff | var(--a) var(--b) |\n"
    assert _rows(_import(text).report.not_read) == [
        ("rules.md:3", "bg", "in the Dark column, var(--a) var(--b) joins several values with "
                             "var(); split it into one token per value")]


def test_a_reference_to_a_name_of_two_types_is_not_read_either():
    text = ("| Token | Light | Dark |\n|---|---|---|\n| `bg` | #fff | 4px |\n"
            "| `surface` | {bg} | |\n")
    imported = _import(text)
    assert imported.report.tokens == 0
    assert [i.name for i in imported.report.not_read] == ["bg", "surface"]
    assert imported.report.not_read[1].message == (
        "references bg, which was not read; fix bg and import again")


# A rule written like a token is a rule: it is listed once per file, never
# read as a value, and a real font list still reads as a font.
RULES = """| Token | Value |
|---|---|
| `color.text` | #1b1d22 |

- `accent`: use for links and focus, never for body text
- `radius.card`: 12px, use for cards only
- `color.text`: always meets 4.5:1 on `color.bg`
- `font.body`: Inter, system-ui, sans-serif
- `font.mono`: "Mono Face", ui-monospace, monospace
- `font.head`: Display Serif, Georgia, serif
"""


def test_a_value_written_as_prose_is_kept_as_a_rule():
    imported = _import(RULES)
    ts = imported.tokens
    assert [t.path for t in ts.tokens()] == ["color.text", "font.body", "font.mono", "font.head"]
    assert imported.report.entries == 4 and imported.report.not_read == []
    assert _rows(imported.report.notes) == [
        ("rules.md:5", "", "3 lines hold rules, not values, and were kept as rules: `accent` "
                           "(line 5), `radius.card` (line 6), `color.text` (line 7); to make "
                           "one a token, write only its value after the colon or in the cell, "
                           "and put the rule on its own line")]


def test_a_font_list_is_still_a_font():
    ts = _import(RULES).tokens
    assert (ts.get("font.body").type, ts.get("font.body").value) == (
        "fontFamily", ["Inter", "system-ui", "sans-serif"])
    assert ts.get("font.mono").value == ["Mono Face", "ui-monospace", "monospace"]
    assert ts.get("font.head").value == ["Display Serif", "Georgia", "serif"]


def test_one_rule_in_a_file_is_named_in_the_singular():
    report = _import("- `accent`: for links\n").report
    assert _rows(report.notes) == [
        ("rules.md:1", "", "1 line holds a rule, not a value, and was kept as a rule: `accent` "
                           "(line 1); to make it a token, write only its value after the colon "
                           "or in the cell, and put the rule on its own line")]


def test_rules_are_grouped_per_file(tmp_path):
    folder = tmp_path / "rules"
    folder.mkdir()
    (folder / "a.md").write_text("- `x`: for links\n", encoding="utf-8")
    (folder / "b.md").write_text("- `y`: 4px\n- `z`: never on dark fills\n", encoding="utf-8")
    notes = read_markdown(folder).report.notes
    assert [(i.where, i.message.split(":")[0]) for i in notes] == [
        ("a.md:1", "1 line holds a rule, not a value, and was kept as a rule"),
        ("b.md:2", "1 line holds a rule, not a value, and was kept as a rule")]


@pytest.mark.parametrize("light, dark", [
    ("Light (default)", "Dark"), ("Light hex", "Dark hex"), ("Light", "Dark mode"),
    ("Light value", "Dark value")])
def test_a_header_holding_a_mode_word_reads_as_that_mode(light, dark):
    text = f"| Token | {light} | {dark} | Notes |\n|---|---|---|---|\n| `bg` | #fff | #000 | x |\n"
    ts = _import(text).tokens
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert ts.get("bg").modes == {"scheme:dark": "#000000"}


def test_the_token_column_wins_over_a_role_column():
    text = "| Role | Token | Value |\n|---|---|---|\n| Body text | `color.text` | #111 |\n"
    imported = _import(text)
    assert [t.path for t in imported.tokens.tokens()] == ["color.text"]
    assert imported.report.not_read == [] and imported.report.notes == []


def test_a_usage_map_is_noted_once_not_per_row():
    text = ("| Component | Token |\n|---|---|\n| Primary button | `color.accent` |\n"
            "| Card | `radius.card` |\n")
    imported = _import(text)
    assert imported.report.entries == 0 and imported.report.not_read == []
    assert _rows(imported.report.notes) == [
        ("rules.md:1", "", "a table whose Component column holds no values was not read as "
                           "tokens; head the value column Value, Hex or Size to read it")]


def test_a_column_beside_the_value_that_names_no_mode_is_noted():
    text = "| Token | Value | Hover |\n|---|---|---|\n| `accent` | #c2410c | #9a3412 |\n"
    imported = _import(text)
    assert imported.tokens.get("accent").modes == {}
    assert _rows(imported.report.notes) == [
        ("rules.md:1", "", "a table with the columns Token, Value and Hover: Hover names no mode "
                           "and was left out; head a column with a mode name such as Dark to "
                           "read it as that mode, or put it in its own table")]


def test_a_name_set_again_after_an_unreadable_first_value_says_so():
    report = _import("- `a`: 3em\n- `a`: 4px\n").report
    assert _rows(report.not_read) == [
        ("rules.md:1", "a", "3em is relative to the parent's font size, so it has no fixed "
                            "value; write it in px or rem"),
        ("rules.md:2", "a", "is set again with another value (4px); rules.md:1 set it first to "
                            "3em, which was not read (3em is relative to the parent's font size, "
                            "so it has no fixed value; write it in px or rem); the first value "
                            "wins, so no value is used for a; fix that line or remove it, and "
                            "keep one")]


def test_an_indented_code_block_is_not_read():
    text = "Example:\n\n    | Token | Value |\n    |---|---|\n    | `a` | 4px |\n\n- `b`: 8px\n"
    imported = _import(text)
    assert [t.path for t in imported.tokens.tokens()] == ["b"]


def test_an_indented_list_item_inside_a_list_is_read():
    text = "- `a`: 4px\n\n    - `b`: 8px\n"
    assert [t.path for t in _import(text).tokens.tokens()] == ["a", "b"]


def test_a_table_inside_a_fence_is_not_read():
    text = "```\n| Token | Value |\n|---|---|\n| `a` | 4px |\n```\n"
    imported = _import(text)
    assert imported.report.entries == 0 and imported.report.notes == []


def test_a_folder_is_read_in_name_order(tmp_path):
    folder = tmp_path / "rules"
    folder.mkdir()
    (folder / "b.md").write_text("- `second`: 8px\n", encoding="utf-8")
    (folder / "a.md").write_text("- `first`: 4px\n", encoding="utf-8")
    assert [t.path for t in read_markdown(folder).tokens.tokens()] == ["first", "second"]


def test_a_name_set_again_after_a_first_value_dropped_for_a_reference_says_so():
    report = _import("- `a`: {missing}\n- `a`: 4px\n").report
    assert _rows(report.not_read) == [
        ("rules.md:1", "a", "references missing, which no file defines; define it or write the "
                            "value"),
        ("rules.md:2", "a", "is set again with another value (4px); rules.md:1 set it first to "
                            "{missing}, which was not read (references missing, which no file "
                            "defines; define it or write the value); the first value wins, so no "
                            "value is used for a; fix that line or remove it, and keep one")]
    assert report.tokens == 0


@pytest.mark.parametrize("value", ["Links, Buttons", "Gray, Slate", "Small, Medium, Large"])
def test_a_comma_list_of_names_without_font_evidence_is_a_rule(value):
    for text in (f"- `link`: {value}\n", f"| Token | Value |\n|---|---|\n| `link` | {value} |\n"):
        imported = _import(text)
        assert imported.report.tokens == 0 and imported.report.not_read == []
        [note] = imported.report.notes
        assert note.message.startswith("1 line holds a rule, not a value")
        assert note.message.endswith("; a font list reads when its font names are quoted or it "
                                     "ends in a generic family such as sans-serif")


@pytest.mark.parametrize("line", [
    "- `font.body`: Inter, Arial",
    "- `brand.family`: Inter, Arial",
    "- `body`: Inter, Arial, sans-serif",
    "- `body`: Inter, Arial, ui-sans-serif",
    "- `body`: Inter, Arial, emoji",
    "- `body`: \"Brand Sans\", Arial",
    "- `body`: helvetica neue, arial, sans-serif",
])
def test_a_comma_list_of_names_with_evidence_is_a_font(line):
    imported = _import(line + "\n")
    [token] = imported.tokens.tokens()
    assert token.type == "fontFamily" and imported.report.notes == []


def test_a_type_column_header_is_font_evidence():
    text = "| Name | Typeface |\n|---|---|\n| `body` | Inter, Arial |\n"
    assert _import(text).tokens.get("body").value == ["Inter", "Arial"]


def test_a_font_column_of_unquoted_stacks_reads():
    text = ("| Token | Font |\n|---|---|\n| `body` | Inter, system-ui, sans-serif |\n"
            "| `mono` | Mono Face, Courier |\n")
    imported = _import(text)
    assert imported.tokens.get("body").value == ["Inter", "system-ui", "sans-serif"]
    assert imported.tokens.get("mono").value == ["Mono Face", "Courier"]
    assert imported.report.notes == []


def test_a_prose_rule_does_not_get_the_font_hint():
    [note] = _import("- `accent`: use for links, never for text\n").report.notes
    assert "font list" not in note.message


def test_a_bare_type_in_a_name_is_not_font_evidence():
    imported = _import("- `type.sizes`: Small, Large\n")
    assert imported.report.tokens == 0
    [note] = imported.report.notes
    assert note.message.startswith("1 line holds a rule, not a value")


def test_a_type_column_of_size_names_is_not_read_as_fonts():
    imported = _import("| Token | Type |\n|---|---|\n| `size` | Small, Large |\n")
    assert imported.report.tokens == 0
    assert [i.message for i in imported.report.notes] == [
        "a table whose Type column holds no values was not read as tokens; head the value "
        "column Value, Hex or Size to read it"]


@pytest.mark.parametrize("text", [
    "- `type.family.body`: Inter, Arial\n",
    "- `fontFamily`: Inter, Arial\n",
    "| Token | Font family |\n|---|---|\n| `body` | Inter, Arial |\n",
])
def test_font_family_or_typeface_in_the_context_is_evidence(text):
    [token] = _import(text).tokens.tokens()
    assert (token.type, token.value) == ("fontFamily", ["Inter", "Arial"])


@pytest.mark.parametrize("head, axes", [
    ("| Token | Standard | High |", {"standard-high": ("standard", "high")}),
    ("| Token | Standard | Reduced |", {"standard-reduced": ("standard", "reduced")}),
    ("| Token | Standard | High contrast |", {"contrast": ("standard", "high")}),
    ("| Token | Standard motion | Reduced motion |", {"motion": ("standard", "reduced")}),
])
def test_standard_high_and_reduced_name_an_axis_only_beside_its_name(head, axes):
    text = f"{head}\n|---|---|---|\n| `gap` | 8px | 4px |\n"
    assert dict(_import(text).tokens.axes) == axes


def test_a_lone_high_or_reduced_column_needs_the_axis_name():
    text = "| Token | Value | High |\n|---|---|---|\n| `gap` | 8px | 4px |\n"
    imported = _import(text)
    assert dict(imported.tokens.axes) == {}
    assert "High names no mode" in imported.report.notes[0].message
    text = "| Token | Value | Reduced motion |\n|---|---|---|\n| `t` | 200ms | 0ms |\n"
    assert dict(_import(text).tokens.axes) == {"motion": ("standard", "reduced")}


def test_an_indented_line_right_after_a_heading_is_code_as_in_commonmark():
    text = "# Tokens\n    - `a`: 4px\n\n- `b`: 8px\n"
    assert [t.path for t in _import(text).tokens.tokens()] == ["b"]
    # A paragraph line is not a heading: an indented line after it continues it.
    text = "Spacing\n    - `a`: 4px\n"
    assert [t.path for t in _import(text).tokens.tokens()] == ["a"]


@pytest.mark.parametrize("before", ["Tokens\n======\n", "Tokens\n------\n", "```\nx\n```\n",
                                    "***\n"])
def test_an_indented_line_after_a_setext_heading_a_fence_or_a_break_is_code(before):
    text = f"{before}    - `a`: 4px\n\n- `b`: 8px\n"
    assert [t.path for t in _import(text).tokens.tokens()] == ["b"]
