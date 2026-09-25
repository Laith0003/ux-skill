"""The DTCG importer: our own files come back exactly; a foreign file is
read in its own names, with group $type inheritance, aliases, $root,
translucent colors and older value forms handled or reported, and other
tools' $extensions left out and said so."""
import json
from pathlib import Path

import pytest

from engine.foundations.build import build_system
from engine.foundations.emit import InputError
from engine.foundations.export import dump_dtcg
from engine.io.dtcg_in import import_dtcg, read_dtcg
from engine.io.report import Source
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)

FOREIGN = {
    "$schema": "https://www.designtokens.org/schemas/2025.10/format.json",
    "palette": {
        "$type": "color",
        "ink": {"900": {"$value": {"colorSpace": "srgb", "components": [0.07, 0.08, 0.1],
                                   "hex": "#121419"}}},
        "paper": {"$value": "#fafaf7", "$description": "The page."},
        "sky": {"$value": {"colorSpace": "hsl", "components": [225, 100, 60]}},
        "leaf": {"$value": {"colorSpace": "display-p3", "components": [0.2, 0.6, 0.3],
                            "hex": "#2E9950"}},
        "night": {"$value": {"colorSpace": "lab", "components": [20, 0, 0]}},
        "veil": {"$value": {"colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.4}},
        "accent": {"$root": {"$value": {"colorSpace": "srgb", "components": [0.8, 0.2, 0.1]}},
                   "soft": {"$value": {"colorSpace": "srgb", "components": [1, 0.9, 0.88]}}},
    },
    "text": {
        "$type": "color",
        "body": {"$value": "{palette.ink.900}"},
        "accent": {"$value": "{palette.accent.$root}"},
    },
    "size": {
        "$type": "dimension",
        "2": {"$value": {"value": 8, "unit": "px"}},
        "4": {"$value": "16px"},
        "wide": {"$value": {"value": 2, "unit": "em"}},
    },
    "gap": {"$value": "{size.2}"},
    "weight": {"strong": {"$type": "fontWeight", "$value": "semi-bold"}},
    "motion": {"quick": {"$type": "duration", "$value": {"value": 120, "unit": "ms"}},
               "calm": {"$type": "cubicBezier", "$value": [0.2, 0, 0, 1],
                        "$deprecated": "use motion.quick"}},
    "edge": {"$type": "border", "$value": {"color": "{palette.ink.900}", "width": "1px",
                                           "style": "solid"}},
    "count": {"$value": 3},
    "layer": {"$type": "number", "$value": 2,
              "$extensions": {"com.example.tool": {"hidden": True}}},
    "heading": {"$type": "typography", "$value": {
        "fontFamily": ["Serif Display", "serif"], "fontSize": "{size.4}", "fontWeight": 700,
        "letterSpacing": {"value": 0, "unit": "px"}, "lineHeight": 1.2}},
}


def _import(doc, name="system.tokens.json"):
    text = json.dumps(doc, indent=2)
    return import_dtcg(text, Source(name, "dtcg", "0" * 64, len(text)))


def test_our_own_file_comes_back_exactly():
    ts = build_system(NEUTRAL, "#3366FF").tokens
    text = dump_dtcg(ts)
    imported = import_dtcg(text, Source("tokens.json", "dtcg", "0" * 64, len(text)))
    assert dump_dtcg(imported.tokens) == text
    report = imported.report
    assert (report.renamed, report.notes, report.not_read) == ([], [], [])
    assert report.entries == report.tokens == len(ts.tokens())
    assert report.axes == {a: list(v) for a, v in ts.axes.items()}


def test_a_foreign_file_keeps_its_own_names_and_infers_layers():
    ts = _import(FOREIGN).tokens
    paths = [t.path for t in ts.tokens()]
    assert paths == ["palette.ink.900", "palette.paper", "palette.sky", "palette.leaf",
                     "palette.veil", "palette.accent.root", "palette.accent.soft", "text.body",
                     "text.accent", "size.2", "size.4", "gap", "weight.strong", "motion.quick",
                     "motion.calm", "layer", "heading"]
    assert dict(ts.axes) == {}
    assert ts.get("palette.ink.900").value == "#121419"
    assert ts.get("palette.paper").value == "#FAFAF7"
    assert ts.get("palette.paper").description == "The page."
    assert ts.get("palette.sky").value == "#3366FF"
    assert ts.get("palette.leaf").value == "#2E9950"
    assert ts.get("palette.veil").value == "#00000066"
    assert ts.get("text.accent").value == "{palette.accent.root}"
    assert ts.get("size.4").value == {"value": 16, "unit": "px"}
    assert (ts.get("gap").type, ts.get("gap").value) == ("dimension", "{size.2}")
    assert ts.get("weight.strong").value == 600
    assert ts.get("heading").layer == "semantic"
    assert [t.path for t in ts.tokens() if t.layer == "semantic"] == [
        "text.body", "text.accent", "gap", "heading"]


def test_the_report_lists_renames_notes_and_what_was_not_read():
    report = _import(FOREIGN).report
    assert report.entries == 21 and report.tokens == 17
    assert [(i.where, i.name, i.message) for i in report.renamed] == [
        ("system.tokens.json palette.accent.$root", "palette.accent.$root",
         "read as palette.accent.root, since a token path segment cannot start with $; "
         "references to it now read palette.accent.root")]
    assert [(i.name, i.message) for i in report.notes] == [
        ("palette.paper", "a hex string, the form before DTCG 2025.10; read as #FAFAF7"),
        ("palette.sky", "an hsl color, converted to sRGB #3366FF"),
        ("palette.leaf", "a display-p3 color, read from its hex fallback #2E9950; the engine "
                         "measures sRGB only"),
        ("size.4", "a string, the form before DTCG 2025.10; read as 16px"),
        ("gap", "has no $type, so it takes the type of size.2, which it references"),
        ("weight.strong", "the weight name semi-bold, read as 600"),
        ("motion.calm", "is marked deprecated (use motion.quick); the engine has no deprecated "
                        "tokens, so it was read as a live one"),
        ("layer", "carries $extensions from com.example.tool, which the engine does not read; "
                  "they are left out of what it writes")]
    assert [(i.name, i.message) for i in report.not_read] == [
        ("palette.night", "a lab color with no hex fallback; the engine measures sRGB only, so "
                          "write it as srgb or add a hex fallback"),
        ("size.wide", "2em is relative to the parent's font size, so it has no fixed value; "
                      "write it in px or rem"),
        ("edge", "a border token; the engine holds no border composites, so write its width, "
                 "style and color as three tokens"),
        ("count", "has no $type and its groups set none; add a $type")]


def test_an_alias_to_a_token_that_was_not_read_is_reported_not_kept():
    doc = {"size": {"$type": "dimension", "wide": {"$value": {"value": 2, "unit": "em"}},
                    "gutter": {"$value": "{size.wide}"}}}
    imported = _import(doc)
    assert [t.path for t in imported.tokens.tokens()] == []
    assert [(i.name, i.message) for i in imported.report.not_read] == [
        ("size.wide", "2em is relative to the parent's font size, so it has no fixed value; "
                      "write it in px or rem"),
        ("size.gutter", "references size.wide, which was not read; fix size.wide and import "
                        "again")]


def test_json_errors_name_the_line():
    with pytest.raises(InputError) as exc:
        import_dtcg('{\n  "a": {\n', Source("t.json", "dtcg", "0" * 64, 9))
    assert str(exc.value).startswith("t.json is not valid JSON (")
    assert str(exc.value).endswith("line 3 column 1 (char 11)); fix the file and import it again")
    with pytest.raises(InputError, match=r"t.json holds a JSON list, not an object"):
        import_dtcg("[]", Source("t.json", "dtcg", "0" * 64, 2))


def test_a_file_from_an_older_build_is_refused_with_the_fix():
    doc = {"a": {"$type": "number", "$value": 1, "$extensions": {"ux.layer": "primitive"}}}
    with pytest.raises(InputError) as exc:
        _import(doc, "old.json")
    assert str(exc.value) == ("old.json a carries the extension keys ['ux.layer']; this file was "
                              "written by an older build; build it again with the current "
                              "version and import that")


def test_a_malformed_axes_block_is_named():
    doc = {"$extensions": {"io.github.laith0003.ux-skill": {"axes": {"scheme": ["light"]}}}}
    with pytest.raises(InputError) as exc:
        _import(doc, "t.json")
    assert str(exc.value) == (
        "t.json names the mode axis scheme with ['light']; a mode axis has exactly two values, "
        "the base first, for example \"scheme\": [\"light\", \"dark\"]")


def test_read_dtcg_reads_the_file(tmp_path):
    f = tmp_path / "tokens.json"
    f.write_text(json.dumps({"a": {"$type": "number", "$value": 1}}), encoding="utf-8")
    imported = read_dtcg(f)
    assert imported.report.source.format == "dtcg"
    assert imported.report.source.path == str(f)
    assert [t.path for t in imported.tokens.tokens()] == ["a"]


# Ruling M4-R5: an oklch or oklab color object outside sRGB is mapped into
# sRGB by CSS Color 4 gamut mapping and reported, never refused, the same
# way the value reader maps oklch() text. Tailwind v4's blue-500 sits
# outside sRGB; its red-500 sits inside.
def test_oklch_and_oklab_objects_are_converted_and_out_of_gamut_ones_mapped():
    import math

    from engine.io.values_in import read_value

    a, b = 0.214 * math.cos(math.radians(259.815)), 0.214 * math.sin(math.radians(259.815))
    doc = {"c": {"$type": "color",
                 "red": {"$value": {"colorSpace": "oklch", "components": [0.637, 0.237, 25.331]}},
                 "blue": {"$value": {"colorSpace": "oklch", "components": [0.623, 0.214, 259.815],
                                     "hex": "#2B7FFF"}},
                 "lab": {"$value": {"colorSpace": "oklab", "components": [0.623, a, b],
                                    "alpha": 0.5}},
                 "grey": {"$value": {"colorSpace": "oklch", "components": [0.5, 0, "none"]}}}}
    imported = _import(doc)
    ts, report = imported.tokens, imported.report
    blue = read_value("oklch(62.3% 0.214 259.815)")[1]
    assert ts.get("c.red").value == "#FB2C36"
    assert ts.get("c.blue").value == blue == "#2B7FFF"
    assert ts.get("c.lab").value == blue + "80"
    assert ts.get("c.grey").value == read_value("oklch(0.5 0 0)")[1]
    assert report.not_read == []
    assert [(i.name, i.message) for i in report.notes] == [
        ("c.red", "an oklch color, converted to sRGB #FB2C36"),
        ("c.grey", f"an oklch color, converted to sRGB {ts.get('c.grey').value}")]
    assert [(m.where, m.name, m.original, m.hex) for m in report.mapped] == [
        ("system.tokens.json c.blue", "c.blue", "oklch(0.623 0.214 259.815)", blue),
        ("system.tokens.json c.lab", "c.lab",
         f"oklab(0.623 {a:g} {b:g} / 0.5)", blue + "80")]
    assert all(0 < m.distance < 0.1 for m in report.mapped)
    assert "## Mapped into sRGB" in report.markdown()


def test_a_mapped_color_in_a_mode_is_reported_with_its_mode():
    doc = {"$extensions": {"io.github.laith0003.ux-skill": {"axes": {"scheme": ["light", "dark"]}}},
           "c": {"$type": "color", "$value": "#FFFFFF", "$extensions": {
               "io.github.laith0003.ux-skill": {"modes": {"scheme:dark": {
                   "colorSpace": "oklch", "components": [0.623, 0.214, 259.815]}}}}}}
    report = _import(doc).report
    assert [(m.where, m.name) for m in report.mapped] == [
        ("system.tokens.json c (scheme:dark)", "c")]


def test_a_css_color_string_is_read_with_a_note_and_mapped_when_outside_srgb():
    doc = {"c": {"$type": "color", "a": {"$value": "rgb(255 0 0)"},
                 "b": {"$value": "oklch(62.3% 0.214 259.815)"}}}
    imported = _import(doc)
    assert [(i.name, i.message) for i in imported.report.notes] == [
        ("c.a", "a CSS color string, the form before DTCG 2025.10; read as #FF0000"),
        ("c.b", "a CSS color string, the form before DTCG 2025.10; read as #2B7FFF")]
    assert [m.name for m in imported.report.mapped] == ["c.b"]


def test_a_token_dropped_for_a_broken_reference_takes_its_mapped_line_with_it():
    doc = {"size": {"$type": "dimension", "wide": {"$value": {"value": 2, "unit": "em"}}},
           "c": {"$type": "shadow", "$value": {
               "color": {"colorSpace": "oklch", "components": [0.623, 0.214, 259.815]},
               "offsetX": "{size.wide}", "offsetY": {"value": 1, "unit": "px"},
               "blur": {"value": 2, "unit": "px"}, "spread": {"value": 0, "unit": "px"}}}}
    report = _import(doc).report
    assert [i.name for i in report.not_read] == ["size.wide", "c"]
    assert report.mapped == []


# A realistic foreign system, split the way teams split one: primitives,
# semantic roles per theme in their own files, one file with every layer
# and its dark mode kept in another tool's $extensions, and the build
# script's flattened output. The fixture names no product.
FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "dtcg_multilayer"


def _lines(items):
    return [(i.name, i.message) for i in items]


def test_a_primitives_file_reads_its_ramps_and_maps_the_vivid_steps():
    imported = read_dtcg(FIXTURE / "primitives.tokens.json")
    ts, report = imported.tokens, imported.report
    assert (report.entries, report.tokens) == (40, 39)
    assert {t.layer for t in ts.tokens()} == {"primitive"}
    assert ts.get("color.brand.500").value == "#2B7FFF"
    assert ts.get("color.overlay").value == "#0C0A0999"
    assert ts.get("font.weight.bold").value == 700
    assert [m.name for m in report.mapped] == ["color.brand.300", "color.brand.500",
                                               "color.danger.700"]
    assert _lines(report.not_read) == [
        ("font.tracking.tight", "-0.02em is relative to the parent's font size, so it has no "
                                "fixed value; write it in px or rem")]
    assert dump_dtcg(ts)


def test_a_semantic_file_alone_keeps_its_references_and_says_they_do_not_resolve_here():
    for theme in ("light", "dark"):
        imported = read_dtcg(FIXTURE / f"semantic.{theme}.tokens.json")
        ts, report = imported.tokens, imported.report
        assert report.tokens == 11 and report.not_read == []
        assert {t.layer for t in ts.tokens()} == {"semantic"}
        assert ts.get("accent.root").value.startswith("{color.brand.")
        assert _lines(report.renamed)[0][0] == "accent.$root"
        assert ("bg.canvas", "references " + ts.get("bg.canvas").value[1:-1] + ", which this "
                "file does not hold; the reference is kept as written and resolves only where "
                "the file that defines it is read too") in _lines(report.notes)
        assert len(report.notes) == 11


def test_a_file_with_every_layer_reports_the_modes_it_cannot_read():
    imported = read_dtcg(FIXTURE / "themed.tokens.json")
    ts, report = imported.tokens, imported.report
    assert dict(ts.axes) == {}
    assert [t.path for t in ts.tokens() if t.layer == "semantic"] == [
        "semantic.surface.page", "semantic.surface.text", "semantic.surface.muted",
        "semantic.action.primary", "semantic.gap.inline", "semantic.gap.stack",
        "component.button.padding-x"]
    assert ts.get("semantic.surface.muted").value == "{primitive.color.stone}"
    assert ts.get("component.button.label").value["fontWeight"] == 600
    assert len(ts.get("component.button.shadow").value) == 2
    notes = _lines(report.notes)
    assert notes[0] == ("", "carries $extensions from org.example.themes, which the engine "
                            "does not read; they are left out of what it writes")
    assert report.notes[0].where == "themed.tokens.json (root)"
    assert ("semantic.surface.page", "carries $extensions from org.example.themes, which the "
            "engine does not read; they are left out of what it writes") in notes
    assert [i.name for i in report.not_read] == ["component.button.outline",
                                                 "component.button.press"]
    assert [m.name for m in report.mapped] == ["primitive.color.blue"]


def test_a_build_script_output_reads_its_string_forms_with_notes():
    imported = read_dtcg(FIXTURE / "generated" / "tokens.json")
    ts, report = imported.tokens, imported.report
    assert ts.get("font.family.sans").value == ["Inter", "system-ui", "sans-serif"]
    assert ts.get("font.weight.bold").value == 700
    assert ts.get("easing.standard").value == [0.2, 0, 0, 1]
    assert ts.get("body").value == {
        "fontFamily": ["Inter", "system-ui", "sans-serif"], "fontSize": {"value": 16, "unit": "px"},
        "fontWeight": 400, "letterSpacing": {"value": 0, "unit": "px"}, "lineHeight": 1.5}
    assert ts.get("color.brand.500").value == ts.get("color.brand.500-rgb").value == "#2B7FFF"
    notes = _lines(report.notes)
    assert ("font.family.sans", 'a string, the form before DTCG 2025.10; read as '
            '["Inter", "system-ui", "sans-serif"]') in notes
    assert ("font.weight.bold", "a string, the form before DTCG 2025.10; read as 700") in notes
    assert ("easing.standard", "a string, the form before DTCG 2025.10; read as "
            "[0.2, 0, 0, 1]") in notes
    assert report.notes[0].where == "tokens.json (root)"
    assert [m.name for m in report.mapped] == ["color.brand.500"]
    assert _lines(report.not_read) == [
        ("space.gutter", "clamp(1rem, 4vw, 2rem) is computed by the browser; write the value it "
                         "computes to"),
        ("radius.pill", "50% is relative to its container, so it has no fixed value; write it in "
                        "px or rem")]
    assert dump_dtcg(ts)


def test_an_untyped_reference_to_a_token_the_file_does_not_hold_names_it():
    report = _import({"gap": {"$value": "{space.2}"}}).report
    assert _lines(report.not_read) == [
        ("gap", "has no $type, and space.2, which it references, is not in this file; add a "
                "$type")]
