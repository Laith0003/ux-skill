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
    text = "Token | Value\n--- | ---\n`radius.sm` | 4px\n"
    assert _import(text).tokens.get("radius.sm").value == {"value": 4, "unit": "px"}


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
