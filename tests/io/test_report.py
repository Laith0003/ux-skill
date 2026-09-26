"""The import report: the source it read (with its digest), what became
tokens, the modes, and every entry that was renamed, read with a note or
not read, each with where it sits and the fix."""
import hashlib
import json

import pytest

from engine.foundations.emit import InputError
from engine.foundations.tokens import Token, TokenSet
from engine.io import read_any
from engine.io.report import (FORMATS, Imported, ImportReport, Item, Mapped, Source,
                              read_source)


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
    assert list(d) == ["source", "also_read", "entries", "tokens", "mode_values", "by_type", "axes",
                       "renamed", "notes", "mapped", "not_read"]
    assert d["also_read"] == []
    assert d["mapped"] == []


def test_the_report_reads_as_markdown_in_a_fixed_order():
    _, report = _report()
    assert report.markdown() == (
        "# Import report\n\n"
        "Read design/tokens.css (css, 120 bytes, sha256 abababababab): 6 entries, 4 tokens.\n\n"
        "1 mode value.\n\n"
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
    assert "## Mapped into sRGB" not in text


def test_imported_carries_the_tokens_the_report_and_the_css_forms():
    ts, report = _report()
    imported = Imported(ts, report)
    assert imported.tokens is ts and imported.report is report and imported.forms == {}


def test_a_color_mapped_into_srgb_is_listed_with_both_values_and_the_distance():
    from engine.io.values_in import read_value

    _, report = _report()
    found = []
    text = "oklch(62.3% 0.214 259.815)"
    _, hx = read_value(text, found)
    report.mapped.append(Mapped.of("tokens.css:6", "--blue-500", found[0]))
    item = report.mapped[0]
    assert (item.original, item.hex) == (text, hx) and item.distance == found[0].distance
    assert report.to_dict()["mapped"] == [{
        "where": "tokens.css:6", "name": "--blue-500", "original": text, "hex": hx,
        "distance": round(found[0].distance, 4)}]
    line = (f"- tokens.css:6 `--blue-500`: {text} is outside sRGB; read as {hx}, the same "
            f"lightness and hue with less chroma (OKLab distance {found[0].distance:.4f})")
    text_md = report.markdown()
    assert ("## Mapped into sRGB\n\nCSS Color 4 gamut mapping: each color below lies "
            "outside sRGB and was read at its own lightness and hue with the chroma "
            "lowered until it fits.\n\n" + line + "\n\n## Not read") in text_md
    assert text_md.index("## Read with a note") < text_md.index("## Mapped into sRGB")


_FIGMA = {"meta": {
    "variableCollections": {"c:1": {"id": "c:1", "name": "Color", "defaultModeId": "m:1",
                                    "modes": [{"modeId": "m:1", "name": "Value"}],
                                    "variableIds": ["v:1"]}},
    "variables": {"v:1": {"id": "v:1", "name": "ink", "variableCollectionId": "c:1",
                          "resolvedType": "COLOR", "scopes": ["ALL_SCOPES"],
                          "valuesByMode": {"m:1": {"r": 0, "g": 0, "b": 0, "a": 1}},
                          "description": "", "hiddenFromPublishing": False,
                          "remote": False}}}}
_FILES = {
    "dtcg": ("tokens.json", json.dumps({"ink": {"$type": "color", "$value": "#111111"}})),
    "css": ("tokens.css", ":root { --ink: #111111; }\n"),
    "tailwind": ("app.css", "@theme { --color-ink: #111111; }\n"),
    "tailwind-json": ("theme.json", json.dumps({"colors": {"ink": "#111111"}})),
    "markdown": ("tokens.md", "| Token | Value |\n|---|---|\n| ink | #111111 |\n"),
    "figma": ("figma.json", json.dumps(_FIGMA)),
}


@pytest.mark.parametrize("fmt", FORMATS)
def test_read_any_reads_each_format_with_its_own_reader(tmp_path, fmt):
    name, text = _FILES[fmt]
    (tmp_path / name).write_text(text, encoding="utf-8")
    imported = read_any(tmp_path / name, fmt)
    assert imported.report.source.format == fmt
    assert imported.report.tokens == 1


def test_read_any_names_the_format_and_the_fix(tmp_path):
    (tmp_path / "tokens.css").write_text(":root { --ink: #111; }\n", encoding="utf-8")
    with pytest.raises(InputError) as exc:
        read_any(tmp_path / "tokens.css", "scss", label="--from")
    assert str(exc.value) == ("--from format 'scss' is not one of dtcg, css, tailwind, "
                              "tailwind-json, markdown and figma; pass one of those")
    with pytest.raises(InputError) as exc:
        read_any(tmp_path / "tokens.css", "tailwind-json")
    assert "is not a .json file, which tailwind-json reads" in str(exc.value)


def _var(i, name, kind, light, dark, scopes=("ALL_SCOPES",)):
    return {"id": f"v:{i}", "name": name, "variableCollectionId": "c:1", "resolvedType": kind,
            "valuesByMode": {"m:l": light, "m:d": dark}, "scopes": list(scopes),
            "description": "", "hiddenFromPublishing": False, "remote": False}


_RGB = {"ink": ({"r": 0, "g": 0, "b": 0, "a": 1}, {"r": 1, "g": 1, "b": 1, "a": 1})}
_SMALL = {
    "css": (":root {\n  --ink: #000000;\n  --paper: #FFFFFF;\n  --gap: 8px;\n}\n"
            ".dark {\n  --ink: #FFFFFF;\n  --paper: #000000;\n}\n"),
    "tailwind": ("@theme {\n  --ink: #000000;\n  --paper: #FFFFFF;\n  --gap: 8px;\n}\n"
                 ".dark {\n  --ink: #FFFFFF;\n  --paper: #000000;\n}\n"),
    "dtcg": json.dumps({
        "ink": {"$type": "color", "$value": "#000000",
                "$extensions": {"modes": {"dark": "#FFFFFF"}}},
        "paper": {"$type": "color", "$value": "#FFFFFF",
                  "$extensions": {"modes": {"dark": "#000000"}}},
        "gap": {"$type": "dimension", "$value": {"value": 8, "unit": "px"}}}),
    "markdown": ("| Token | Value | Dark |\n|---|---|---|\n| ink | #000000 | #FFFFFF |\n"
                 "| paper | #FFFFFF | #000000 |\n| gap | 8px | |\n"),
    "figma": json.dumps({"meta": {
        "variableCollections": {"c:1": {
            "id": "c:1", "name": "Theme", "defaultModeId": "m:l",
            "modes": [{"modeId": "m:l", "name": "Light"}, {"modeId": "m:d", "name": "Dark"}],
            "variableIds": ["v:1", "v:2", "v:3"]}},
        "variables": {"v:1": _var(1, "ink", "COLOR", *_RGB["ink"]),
                      "v:2": _var(2, "paper", "COLOR", *reversed(_RGB["ink"])),
                      "v:3": _var(3, "gap", "FLOAT", 8, 8, ("GAP",))}}}),
}


@pytest.mark.parametrize("fmt", list(_SMALL))
def test_one_small_system_counts_the_same_entries_and_mode_values_in_every_format(fmt):
    from engine.io import (import_css, import_dtcg, import_figma, import_markdown,
                           import_tailwind_css)
    read = {"css": import_css, "tailwind": import_tailwind_css, "dtcg": import_dtcg,
            "figma": import_figma,
            "markdown": lambda text, source: import_markdown([("tokens.md", text)], source)}
    report = read[fmt](_SMALL[fmt], Source("tokens", fmt, "0" * 64, 1)).report
    assert (report.entries, report.tokens, report.mode_values) == (3, 3, 2)
    assert report.to_dict()["mode_values"] == 2
    assert "3 entries, 3 tokens.\n\n2 mode values.\n" in report.markdown()
