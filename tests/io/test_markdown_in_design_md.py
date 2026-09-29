"""The markdown importer on a DESIGN.md shaped like a real one: prose,
headed sections, tables of role, value and usage, values in sentences,
code blocks and a frontmatter of token groups. Nothing that holds a value
is dropped silently. Every document here is invented."""
from engine.io.markdown_in import import_markdown
from engine.io.report import Source

PROSE = """# Lantern design language

Lantern is calm and quiet. The action color is `#0F766E`, used on buttons
and links; everything else is ink on paper.

## Color

| Swatch | Hex | Usage |
|---|---|---|
| Action | `#0F766E` | Buttons, links, focus |
| Ink | `#14161A` | Body text |
| Scrim | rgba(20, 22, 26, 0.5) | Behind dialogs |
| Paper | `#FFFFFF` | The page |
| Line | `#D0D5DD` | Dividers |

## Shape

- Cards: 12px
- **Fields**: `8px`

## Motion

Most transitions take `160ms`; page changes take 0.3s.

```scss
$shadow-card: 0 1px 2px rgba(0, 0, 0, 0.08);
```

Issue #123 tracks the icon set.
"""


def _import(text, name="DESIGN.md"):
    return import_markdown([(name, text)], Source(name, "markdown", "0" * 64, len(text)))


def _rows(items):
    return [(i.where, i.name, i.message) for i in items]


def test_every_place_that_holds_a_value_is_listed_with_its_fix():
    report = _import(PROSE).report
    assert report.tokens == 0
    assert _rows(report.not_read) == [
        ("DESIGN.md:3", "", "holds #0F766E in running text, which is not read as a token; write "
                            "it as a list item such as - `color.<name>`: #0F766E, or as a row of "
                            "a table with Token and Value columns"),
        ("DESIGN.md:8", "", "a table with the columns Swatch, Hex and Usage holds #0F766E, "
                            "#14161A, rgba(20, 22, 26, 0.5) and #FFFFFF and more, but no column "
                            "names the tokens, so it was not read; head the column that names "
                            "each one Token, Name or Role, and the column of values Value"),
        ("DESIGN.md:18", "Cards", "holds 12px under a name not in backticks, so it was not read; "
                                  "write it as - `shape.cards`: 12px"),
        ("DESIGN.md:19", "Fields", "holds 8px under a name not in backticks, so it was not read; "
                                   "write it as - `shape.fields`: 8px"),
        ("DESIGN.md:23", "", "holds 160ms and 0.3s in running text, which is not read as a "
                             "token; write it as a list item such as - `motion.<name>`: 160ms, "
                             "or as a row of a table with Token and Value columns"),
        ("DESIGN.md:25", "", "a scss code block holds 1px, 2px and rgba(0, 0, 0, 0.08), which "
                             "are not read as tokens; write them as custom properties on :root "
                             "in a .css file and import it with --from, or list them in a table "
                             "with Token and Value columns")]


def test_the_not_read_list_names_each_place():
    report = _import(PROSE).report
    assert [i.where for i in report.not_read] == [
        "DESIGN.md:3", "DESIGN.md:8", "DESIGN.md:18", "DESIGN.md:19", "DESIGN.md:23",
        "DESIGN.md:25"]


def test_an_issue_number_is_not_a_color():
    assert not any("#123" in i.message for i in _import(PROSE).report.not_read)


def test_a_file_with_values_and_no_token_says_so_at_the_top():
    report = _import(PROSE).report
    assert report.headline == [
        "No token was read from DESIGN.md, though it holds values; every line that holds one is "
        "listed below, under Not read or as a rule, with how to write it so it can be read."]
    text = report.markdown()
    assert text.index("No token was read from DESIGN.md") < text.index("## What was read")
    assert report.to_dict()["headline"] == report.headline


def test_a_file_that_gives_tokens_has_no_headline():
    report = _import("| Token | Value |\n|---|---|\n| `ink` | #14161A |\n").report
    assert report.headline == [] and "headline" not in report.to_dict()


def test_a_file_of_prose_alone_has_no_headline():
    report = _import("# About\n\nLantern is calm and quiet.\n").report
    assert report.headline == [] and report.not_read == []


FRONT = """---
version: alpha
name: lantern
description: "Calm and quiet, #0F766E on paper"
colors:
  primary: "#0F766E"
  ink: "#14161A"
typography:
  body:
    fontFamily: Inter Text
    fontSize: 16px
rounded:
  md: 8px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    rounded: 8px
---

# Lantern

The system in prose.
"""


def test_a_frontmatter_of_token_groups_is_read():
    imported = _import(FRONT)
    ts = imported.tokens
    assert [t.path for t in ts.tokens()] == [
        "colors.primary", "colors.ink", "typography.body.fontFamily",
        "typography.body.fontSize", "rounded.md"]
    assert ts.get("colors.primary").value == "#0F766E"
    assert ts.get("typography.body.fontFamily").value == ["Inter Text"]
    assert ts.get("rounded.md").value == {"value": 8, "unit": "px"}
    assert _rows(imported.report.not_read) == [(
        "DESIGN.md:16", "components",
        "holds component properties, which are not system tokens, so the group was not read; "
        "keep them in each component's contract, and move a value the system shares into "
        "colors, rounded or spacing")]
    assert imported.report.headline == []
