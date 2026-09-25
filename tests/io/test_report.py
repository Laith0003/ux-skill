"""The import report: the source it read (with its digest), what became
tokens, the modes, and every entry that was renamed, read with a note or
not read, each with where it sits and the fix."""
import hashlib

import pytest

from engine.foundations.emit import InputError
from engine.foundations.tokens import Token, TokenSet
from engine.io.report import FORMATS, Imported, ImportReport, Item, Source, read_source


def test_read_source_records_the_digest_and_decodes_the_text(tmp_path):
    f = tmp_path / "tokens.css"
    f.write_bytes(b"\xef\xbb\xbf:root { --a: 1px; }\n")
    source, text = read_source(f, "css", "--from")
    assert text == ":root { --a: 1px; }\n"
    assert source == Source(path=str(f), format="css",
                            sha256=hashlib.sha256(f.read_bytes()).hexdigest(), size=23)


def test_read_source_reads_utf16_from_windows_tools(tmp_path):
    f = tmp_path / "tokens.json"
    f.write_bytes("{}".encode("utf-16"))
    assert read_source(f, "dtcg", "--from")[1] == "{}"


@pytest.mark.parametrize("make,message", [
    (lambda p: None, "--from {p} cannot be read (No such file or directory); pass the path of "
                     "the file that holds the system"),
    (lambda p: p.mkdir(), "--from {p} is a folder; pass the file that holds the system, for "
                          "example tokens.json"),
    (lambda p: p.write_bytes(b"\x80\x81 not text"),
     "--from {p} is not UTF-8 text; save it as UTF-8 and pass it again"),
])
def test_read_source_names_the_input_and_the_fix(tmp_path, make, message):
    p = tmp_path / "system.css"
    make(p)
    with pytest.raises(InputError) as exc:
        read_source(p, "css", "--from")
    assert str(exc.value) == message.format(p=p)


def test_unknown_formats_are_refused():
    assert FORMATS == ("dtcg", "css", "tailwind", "tailwind-json", "markdown", "figma")
    with pytest.raises(ValueError, match="format 'scss' is not one of"):
        Source("x", "scss", "0" * 64, 0)


def _report():
    source = Source("design/tokens.css", "css", "ab" * 32, 120)
    ts = TokenSet({"scheme": ("light", "dark")})
    ts.add(Token("ink-900", "color", "#111111"))
    ts.add(Token("paper", "color", "#FFFFFF"))
    ts.add(Token("text-body", "color", "{ink-900}", modes={"scheme:dark": "{paper}"},
                 layer="semantic"))
    ts.add(Token("gap-2", "dimension", {"value": 8, "unit": "px"}))
    report = ImportReport.of(source, ts, entries=6)
    report.renamed.append(Item("tokens.css:3", "--Text Body", "read as text-body"))
    report.notes.append(Item("tokens.css:4", "--gap-2", "its fallback 4px was left out; the "
                                                         "reference holds the value"))
    report.not_read.append(Item("tokens.css:5", "--measure", "60ch is relative to the font, so "
                                                              "it has no fixed value; write it "
                                                              "in px or rem"))
    return ts, report


def test_the_report_counts_tokens_by_type_and_lists_the_modes():
    ts, report = _report()
    assert report.tokens == 4 and report.entries == 6
    assert report.by_type == {"color": 3, "dimension": 1}
    assert report.axes == {"scheme": ["light", "dark"]}
    d = report.to_dict()
    assert d["source"] == {"path": "design/tokens.css", "format": "css", "sha256": "ab" * 32,
                           "size": 120}
    assert d["not_read"] == [{"where": "tokens.css:5", "name": "--measure",
                              "message": report.not_read[0].message}]
    assert list(d) == ["source", "entries", "tokens", "by_type", "axes", "renamed", "notes",
                       "not_read"]


def test_the_report_reads_as_markdown_in_a_fixed_order():
    _, report = _report()
    assert report.markdown() == (
        "# Import report\n\n"
        "Read design/tokens.css (css, 120 bytes, sha256 abababababab): 6 entries, 4 tokens.\n\n"
        "## What was read\n\n"
        "| Type | Tokens |\n|---|---|\n| color | 3 |\n| dimension | 1 |\n\n"
        "Modes: scheme (light is the base, dark).\n\n"
        "## Renamed on the way in\n\n"
        "- tokens.css:3 `--Text Body`: read as text-body\n\n"
        "## Read with a note\n\n"
        "- tokens.css:4 `--gap-2`: its fallback 4px was left out; the reference holds the value\n\n"
        "## Not read\n\n"
        "Nothing below was guessed; each entry says how to write it so it can be read.\n\n"
        "- tokens.css:5 `--measure`: 60ch is relative to the font, so it has no fixed value; "
        "write it in px or rem\n")


def test_an_empty_section_says_so():
    ts = TokenSet({})
    ts.add(Token("a", "number", 1))
    report = ImportReport.of(Source("a.json", "dtcg", "cd" * 32, 9), ts, entries=1)
    text = report.markdown()
    assert "Modes: none; every token has one value.\n" in text
    assert "## Not read\n\nNothing was left unread.\n" in text
    assert "## Renamed on the way in" not in text and "## Read with a note" not in text


def test_imported_carries_the_tokens_the_report_and_the_css_forms():
    ts, report = _report()
    imported = Imported(ts, report)
    assert imported.tokens is ts and imported.report is report and imported.forms == {}
