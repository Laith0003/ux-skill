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
from engine.foundations.values import TYPES
from engine.io.report import Item, Source
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
                  "they are left out of what it writes")] + [
        ("heading", f"its field {field} ({value}) is a literal inside a semantic token; extract "
                    "it to a primitive token and alias it, as fontSize is")
        for field, value in (("fontFamily", "Serif Display, serif"), ("fontWeight", "700"),
                             ("letterSpacing", "0px"), ("lineHeight", "1.2"))]
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


# An oklch or oklab color object outside sRGB is mapped into sRGB by CSS
# Color 4 gamut mapping and reported, never refused, the same way the
# value reader maps oklch() text. Tailwind v4's blue-500 sits
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
    # The dark file read on its own: its name marks it dark, so nothing is paired.
    imported = read_dtcg(FIXTURE / "semantic.dark.tokens.json")
    ts, report = imported.tokens, imported.report
    assert report.tokens == 11 and report.not_read == [] and dict(ts.axes) == {}
    assert {t.layer for t in ts.tokens()} == {"semantic"}
    assert ts.get("accent.root").value == "{color.brand.300}"
    assert _lines(report.renamed)[0][0] == "accent.$root"
    assert ("bg.canvas", "references color.neutral.950, which this file does not hold; the "
            "reference is kept as written and resolves only where the file that defines it is "
            "read too") in _lines(report.notes)
    assert len(report.notes) == 11


def test_the_light_file_pairs_its_dark_sibling_by_token_path():
    imported = read_dtcg(FIXTURE / "semantic.light.tokens.json")
    ts, report = imported.tokens, imported.report
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert report.tokens == 11 and report.not_read == []
    accent = ts.get("accent.root")
    assert (accent.value, accent.modes) == ("{color.brand.500}",
                                            {"scheme:dark": "{color.brand.300}"})
    # The same reference in both schemes needs no dark value.
    assert ts.get("status.success").modes == {}
    assert [s.path for s in report.also_read] == [str(FIXTURE / "semantic.dark.tokens.json")]
    assert report.notes[0] == Item(
        "semantic.dark.tokens.json", "",
        "paired with semantic.light.tokens.json by token path into scheme:dark; 9 tokens take "
        "their dark value from here and 2 are the same in both schemes")
    assert dump_dtcg(import_dtcg(dump_dtcg(ts), _src("t.json")).tokens) == dump_dtcg(ts)


def test_a_file_with_every_layer_pairs_the_dark_mode_another_tool_keeps():
    imported = read_dtcg(FIXTURE / "themed.tokens.json")
    ts, report = imported.tokens, imported.report
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert ts.get("semantic.surface.page").modes == {"scheme:dark": "{primitive.color.ink}"}
    assert ts.get("semantic.surface.text").modes == {"scheme:dark": "{primitive.color.white}"}
    assert report.notes[0] == Item(
        "themed.tokens.json $extensions org.example.themes", "",
        "paired with themed.tokens.json by token path into scheme:dark; 2 tokens take their "
        "dark value from here and 0 are the same in both schemes")
    assert [t.path for t in ts.tokens() if t.layer == "semantic"] == [
        "semantic.surface.page", "semantic.surface.text", "semantic.surface.muted",
        "semantic.action.primary", "semantic.gap.inline", "semantic.gap.stack",
        "component.button.padding-x"]
    assert ts.get("semantic.surface.muted").value == "{primitive.color.stone}"
    assert ts.get("component.button.label").value["fontWeight"] == 600
    assert len(ts.get("component.button.shadow").value) == 2
    notes = _lines(report.notes)
    assert notes[1] == ("", "carries $extensions from org.example.themes, which the engine "
                            "does not read; they are left out of what it writes")
    assert report.notes[1].where == "themed.tokens.json (root)"
    assert "semantic.surface.page" not in [n for n, _ in notes]
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


def _src(name):
    return Source(name, "dtcg", "0" * 64, 1)


# Nothing is dropped without a line: older token forms, bare values and
# properties DTCG does not define are each listed.
def test_a_style_dictionary_3_file_is_listed_not_dropped():
    doc = {"color": {"base": {"red": {"value": "#f00", "comment": "Brand red",
                                      "attributes": {"category": "color"}},
                              "blue": {"value": "{color.base.red.value}"}}}}
    report = _import(doc).report
    assert (report.entries, report.tokens) == (0, 0)
    assert _lines(report.not_read) == [
        ("color.base.red", "uses value, the form before DTCG 2025.10; write $value and $type"),
        ("color.base.blue", "uses value, the form before DTCG 2025.10; write $value and $type")]


def test_a_tokens_studio_legacy_file_is_listed_not_dropped():
    doc = {"global": {"colors": {"white": {"value": "#ffffff", "type": "color"}},
                      "type": {"body": {"value": {"fontFamily": "Inter"}, "type": "typography"}}},
           "$themes": [], "$metadata": {"tokenSetOrder": ["global"]}}
    report = _import(doc).report
    assert [i.name for i in report.not_read] == ["global.colors.white", "global.type.body"]
    assert _lines(report.notes) == [
        ("$themes", "names no themes called light and dark, so its sets were read as groups"),
        ("$metadata", "is not a DTCG property; it was left out")]


def test_bare_values_and_unknown_properties_are_named():
    doc = {"red": "#f00", "g": {"$type": "number", "$foo": 1, "a": {"$value": 1}}}
    report = _import(doc).report
    assert _lines(report.not_read) == [
        ("red", 'a bare value; write it as {"$value": ..., "$type": ...}')]
    assert _lines(report.notes) == [("g.$foo", "is not a DTCG property; it was left out")]


def test_circular_references_are_refused_naming_the_loop():
    doc = {"c": {"$type": "color", "a": {"$value": "{c.b}"}, "b": {"$value": "{c.a}"},
                 "self": {"$value": "{c.self}"}, "ok": {"$value": "#FFFFFF"},
                 "leans": {"$value": "{c.a}"}},
           "u": {"x": {"$value": "{u.y}"}, "y": {"$value": "{u.x}"}}}
    imported = _import(doc)
    assert [t.path for t in imported.tokens.tokens()] == ["c.ok"]
    assert _lines(imported.report.not_read) == [
        ("c.a", "references c.b, which leads back to it (c.a -> c.b -> c.a); point one of them "
                "at a value"),
        ("c.b", "references c.a, which leads back to it (c.b -> c.a -> c.b); point one of them "
                "at a value"),
        ("c.self", "references c.self, which leads back to it (c.self -> c.self); point one of "
                   "them at a value"),
        ("c.leans", "references c.a, which was not read; fix c.a and import again"),
        ("u.x", "has no $type, and its references lead back to it (u.x -> u.y -> u.x); point "
                "one of them at a value"),
        ("u.y", "has no $type, and its references lead back to it (u.y -> u.x -> u.y); point "
                "one of them at a value")]


def test_a_typography_field_that_references_its_own_token_is_refused():
    doc = {"t": {"$type": "typography", "$value": {
        "fontFamily": "Inter", "fontSize": "{t}", "fontWeight": 400,
        "letterSpacing": {"value": 0, "unit": "px"}, "lineHeight": 1.5}}}
    imported = _import(doc)
    assert imported.tokens.tokens() == [] and [i.name for i in imported.report.not_read] == ["t"]


# DTCG makes the components the color and the hex a fallback: they are
# checked, never clamped, and a fallback that disagrees is not guessed at.
@pytest.mark.parametrize("value, message", [
    ({"colorSpace": "srgb", "components": [255, 128, 0]},
     "its srgb components [255, 128, 0] look like 0 to 255; divide each by 255"),
    ({"colorSpace": "srgb", "components": [1.2, 0, 0]},
     "its srgb components [1.2, 0, 0] run outside 0 to 1; write each from 0 to 1"),
    ({"colorSpace": "srgb", "components": [1, 0, 0], "hex": "#00FF00"},
     "its components read as #FF0000 but its hex fallback is #00FF00; fix one"),
    ({"colorSpace": "srgb", "components": [1, 0, 0], "alpha": 2},
     "its alpha 2 is not a number from 0 to 1; write one"),
    ({"colorSpace": "srgb", "components": [1, 0]},
     "an srgb color without three numeric components; write them from 0 to 1"),
    ({"colorSpace": "hsl", "components": [120, 140, 50]},
     "its hsl saturation and lightness run from 0 to 100; write them in that range"),
])
def test_srgb_components_are_checked_not_clamped(value, message):
    report = _import({"c": {"$type": "color", "$value": value}}).report
    assert _lines(report.not_read) == [("c", message)]


def test_srgb_components_are_the_color_and_a_hex_one_step_off_is_the_same_color():
    ts = _import({"c": {"$type": "color",
                        "a": {"$value": {"colorSpace": "srgb", "components": [1, 0.5, 0]}},
                        "b": {"$value": {"colorSpace": "srgb", "components": [0.1, 0.1, 0.1],
                                         "hex": "#191919"}}}}).tokens
    assert ts.get("c.a").value == "#FF8000"
    assert ts.get("c.b").value == "#191919"


# Malformed shapes are named with the fix, never a crash.
def test_malformed_shapes_are_named_with_the_fix():
    doc = {"$extensions": [1],
           "a": {"$type": 5, "$value": 1},
           "g": {"$type": ["color"], "x": {"$value": "#fff"}},
           "o": {"$type": "number", "$value": 1,
                 "$extensions": {"io.github.laith0003.ux-skill": "primitive"}},
           "m": {"$type": "number", "$value": 1,
                 "$extensions": {"io.github.laith0003.ux-skill": {"modes": [1]}}},
           "r": {"$type": "number", "$root": {"$value": 1}, "root": {"$value": 2}},
           "a.b": {"$type": "number", "$value": 1}}
    imported = _import(doc)
    assert [t.path for t in imported.tokens.tokens()] == ["o", "r.root"]
    assert _lines(imported.report.not_read) == [
        ("a", "its $type 5 is not a string; write one of " + str(sorted(TYPES))),
        ("g", "its $type ['color'] is not a string; write one of " + str(sorted(TYPES))
              + "; the tokens below take no type from it"),
        ("g.x", "has no $type and its groups set none; add a $type"),
        ("m", 'its modes are not an object; write them as {"scheme:dark": <value>}'),
        ("r.root", "is read as r.root, which r.$root already names; rename one"),
        ("a.b", "a name cannot contain '.', '{' or '}'; rename it")]
    assert _lines(imported.report.notes) == [
        ("", "its $extensions is not an object; it was left out"),
        ("o", "its io.github.laith0003.ux-skill extension is not an object; it was left out")]


def test_ref_forms_the_importer_cannot_follow_are_named():
    doc = {"g": {"$type": "number", "a/b": {"$value": 1},
                 "c": {"$value": {"$ref": "#/g/a~1b"}},
                 "far": {"$value": {"$ref": "prims.json#/g/a"}},
                 "part": {"$value": {"$ref": "#/g/c/$value/0"}}}}
    imported = _import(doc)
    assert imported.tokens.get("g.c").value == "{g.a/b}"
    assert _lines(imported.report.not_read) == [
        ("g.far", "references another file (prims.json#/g/a); import both together or write "
                  "the value"),
        ("g.part", "references part of a value (#/g/c/$value/0); reference the whole token")]


def test_omissions_are_noted():
    doc = {"$extensions": {"io.github.laith0003.ux-skill": {"axes": {"scheme": ["light",
                                                                                "dark"]}}},
           "old": {"$type": "number", "$deprecated": True, "a": {"$value": 1}},
           "d": {"$type": "number", "$value": 1, "$description": 5},
           "l": {"$type": "number", "$value": 1,
                 "$extensions": {"io.github.laith0003.ux-skill": {"layer": "banana"}}},
           "f": {"$type": "number", "$value": 1,
                 "$extensions": {"io.github.laith0003.ux-skill": {"modes": {"flavor:x": 2}}}},
           "s": {"$type": "dimension", "$value": {"value": "16", "unit": "px"}}}
    imported = _import(doc)
    assert _lines(imported.report.notes) == [
        ("old", "is marked deprecated; the engine has no deprecated tokens, so the tokens below "
                "were read as live ones"),
        ("d", "its $description is not text; it was left out"),
        ("l", "its layer 'banana' is not one of ['primitive', 'semantic']; it was read as "
              "primitive by its references"),
        ("s", "its value is text inside the object; read as 16px")]
    assert _lines(imported.report.not_read) == [
        ("f", "its mode flavor:x does not parse: mode key 'flavor:x' names axis 'flavor'; use "
              "one of ['scheme']")]
    assert imported.tokens.get("l").layer == "primitive"


def test_a_reference_to_a_group_or_to_another_type_is_not_read():
    doc = {"bg": {"$type": "color", "a": {"$value": "#ffffff"}},
           "x": {"$type": "color", "$value": "{bg}"},
           "s": {"$type": "dimension", "$value": {"value": 8, "unit": "px"}},
           "c": {"$type": "color", "$value": "{s}"}}
    assert _lines(_import(doc).report.not_read) == [
        ("x", "references bg, which names a group, not a token; reference one of its tokens"),
        ("c", "references s, a dimension, where a color belongs; point it at a color")]


def test_json_errors_name_comments_trailing_commas_and_duplicate_keys():
    with pytest.raises(InputError) as exc:
        import_dtcg('{\n  // a comment\n  "a": 1\n}', _src("/x/t.json"))
    assert str(exc.value).startswith("t.json is not valid JSON (")
    assert str(exc.value).endswith("JSON holds no comments or trailing commas; remove them and "
                                   "import it again")
    with pytest.raises(InputError) as exc:
        import_dtcg('{"a": 1,}', _src("t.json"))
    assert "JSON holds no comments or trailing commas" in str(exc.value)
    with pytest.raises(InputError) as exc:
        import_dtcg('{"a": {"$value": 1}, "a": {"$value": 2}}', _src("t.json"))
    assert str(exc.value) == ("t.json holds the key 'a' twice in one object; keep one and import "
                              "it again")


def test_errors_name_the_file_by_its_name():
    doc = {"$extensions": {"io.github.laith0003.ux-skill": {"axes": {"scheme": ["light"]}}}}
    text = json.dumps(doc)
    with pytest.raises(InputError, match=r"^t\.json names the mode axis scheme"):
        import_dtcg(text, _src("/some/folder/t.json"))


def test_long_broken_and_untyped_chains_import_in_linear_time():
    import time

    n = 5000
    broken = {"c": {"$type": "dimension",
                    **{f"t{i}": {"$value": f"{{c.t{i + 1}}}"} for i in range(n)},
                    f"t{n}": {"$value": {"value": 2, "unit": "em"}}}}
    untyped = {"p": {"$type": "number", "$value": 1},
               **{f"u{i}": {"$value": "{p}" if i == 0 else f"{{u{i - 1}}}"} for i in range(n)}}
    start = time.perf_counter()
    assert _import(broken).report.tokens == 0
    assert _import(untyped).report.tokens == n + 1
    assert time.perf_counter() - start < 3


def test_the_reader_does_not_import_the_writer():
    """The importers take their error class from a leaf module, so reading a
    system does not load emit and everything it builds with."""
    import ast

    import engine.io.dtcg_in
    import engine.io.report
    import engine.io.values_in
    from engine.foundations import emit, errors

    assert emit.InputError is errors.InputError and emit._brief_text is errors._brief_text
    for module in (engine.io.dtcg_in, engine.io.report, engine.io.values_in, errors):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        assert "engine.foundations.emit" not in names, module.__name__


# A dark scheme is read wherever systems keep it: a sibling file named for
# dark, another tool's mode in $extensions, or a Tokens Studio theme. Each
# pairing is reported, and so is every token found in only one scheme.
def _write(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


LIGHT = {"color": {"$type": "color", "bg": {"$value": "#ffffff"}, "fg": {"$value": "#111111"},
                   "brand": {"$value": "#3366ff"}},
         "space": {"$type": "dimension", "2": {"$value": {"value": 8, "unit": "px"}}}}
DARK = {"color": {"$type": "color", "bg": {"$value": "#111111"}, "fg": {"$value": "#ffffff"},
                  "brand": {"$value": "#3366ff"}, "glow": {"$value": "#00ffff"}},
        "space": {"2": {"$type": "color", "$value": "#000000"}}}


@pytest.mark.parametrize("dark_name", ["tokens.dark.json", "dark/tokens.json"])
def test_a_sibling_dark_file_is_paired_by_token_path(tmp_path, dark_name):
    src = _write(tmp_path / "tokens.json", LIGHT)
    _write(tmp_path / dark_name, DARK)
    imported = read_dtcg(src)
    ts, report = imported.tokens, imported.report
    label = Path(dark_name).name
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert ts.get("color.bg").modes == {"scheme:dark": "#111111"}
    assert ts.get("color.fg").modes == {"scheme:dark": "#FFFFFF"}
    assert ts.get("color.brand").modes == {} and ts.get("space.2").modes == {}
    assert [s.path for s in report.also_read] == [str(tmp_path / dark_name)]
    assert report.notes[0] == Item(label, "", "paired with tokens.json by token path into "
                                              "scheme:dark; 2 tokens take their dark value "
                                              "from here and 1 is the same in both schemes")
    assert Item("tokens.json space.2", "space.2",
                f"has no dark value in {label}; it keeps this value in both schemes") \
        not in report.notes
    assert _lines(report.not_read) == [
        ("color.glow", f"is only in {label}, with no light value in tokens.json, so it was not "
                       "read; add it to tokens.json"),
        ("space.2", f"is a color in {label} but a dimension in tokens.json; give both one "
                    "type")]
    assert report.not_read[0].where == f"{label} color.glow"


def test_a_token_missing_from_the_dark_file_is_named(tmp_path):
    src = _write(tmp_path / "tokens.json", LIGHT)
    _write(tmp_path / "tokens.dark.json", {"color": {"$type": "color",
                                                     "bg": {"$value": "#111111"}}})
    report = read_dtcg(src).report
    assert ("color.fg", "has no dark value in tokens.dark.json; it keeps this value in both "
                        "schemes") in _lines(report.notes)


def test_the_dark_file_read_on_its_own_and_our_own_file_are_not_paired(tmp_path):
    _write(tmp_path / "tokens.json", LIGHT)
    dark = _write(tmp_path / "tokens.dark.json", DARK)
    assert dict(read_dtcg(dark).tokens.axes) == {}
    ours = tmp_path / "ours" / "tokens.json"
    ours.parent.mkdir()
    ours.write_text(dump_dtcg(build_system(NEUTRAL, "#3366FF").tokens), encoding="utf-8")
    _write(tmp_path / "ours" / "tokens.dark.json", DARK)
    imported = read_dtcg(ours)
    assert imported.report.also_read == [] and imported.report.not_read == []
    assert imported.report.notes == [Item(
        "tokens.dark.json", "", "is named as the dark half of tokens.json, which carries its "
                                "own modes, so it was not read")]


def test_a_dark_mode_in_another_tools_extensions_is_paired():
    doc = {"c": {"$type": "color",
                 "a": {"$value": "#ffffff", "$extensions": {"com.example.figma": {
                     "modes": {"Light": "#ffffff", "Dark": "#000000"}}}},
                 "b": {"$value": "#ffffff", "$extensions": {"com.example.figma": {
                     "modes": {"Compact": "#ffffff", "Comfortable": "#eeeeee"}}}},
                 "c": {"$value": "#ffffff", "$extensions": {"org.example.themes": {
                     "dark": {"colorSpace": "oklch", "components": [0.623, 0.214, 259.815]},
                     "id": "123"}}}}}
    imported = _import(doc)
    ts, report = imported.tokens, imported.report
    assert ts.get("c.a").modes == {"scheme:dark": "#000000"}
    assert ts.get("c.b").modes == {}
    assert ts.get("c.c").modes == {"scheme:dark": "#2B7FFF"}
    assert [(n, m) for n, m in _lines(report.notes) if "hex string" not in m] == [
        ("", "paired with system.tokens.json by token path into scheme:dark; 1 token takes "
             "its dark value from here and 0 are the same in both schemes"),
        ("", "paired with system.tokens.json by token path into scheme:dark; 1 token takes "
             "its dark value from here and 0 are the same in both schemes"),
        ("c.b", "carries the modes Compact, Comfortable under com.example.figma, which are not "
                "light and dark, so the engine left them out"),
        ("c.c", "carries $extensions from org.example.themes, which the engine does not read; "
                "they are left out of what it writes")]
    assert [n.where for n in report.notes[:2]] == [
        "system.tokens.json $extensions com.example.figma",
        "system.tokens.json $extensions org.example.themes"]
    assert [(m.where, m.name) for m in report.mapped] == [
        ("system.tokens.json c.c (scheme:dark)", "c.c")]


STUDIO = {
    "global": {"colors": {"white": {"$type": "color", "$value": "#ffffff"},
                          "ink": {"$type": "color", "$value": "#111111"}},
               "space": {"sm": {"$type": "spacing", "$value": "8"}}},
    "light": {"bg": {"$type": "color", "$value": "{colors.white}"},
              "fg": {"$type": "color", "$value": "{colors.ink}"}},
    "dark": {"bg": {"$type": "color", "$value": "{colors.ink}"},
             "fg": {"$type": "color", "$value": "{colors.white}"}},
    "brand-b": {"bg": {"$type": "color", "$value": "#ff0000"}},
    "$themes": [
        {"id": "1", "name": "Light", "selectedTokenSets": {"global": "source",
                                                          "light": "enabled",
                                                          "brand-b": "disabled"}},
        {"id": "2", "name": "Dark", "selectedTokenSets": {"global": "source",
                                                         "dark": "enabled"}}],
    "$metadata": {"tokenSetOrder": ["global", "light", "dark", "brand-b"]},
}


def test_a_tokens_studio_file_pairs_its_light_and_dark_themes():
    imported = _import(STUDIO, "studio.json")
    ts, report = imported.tokens, imported.report
    assert [t.path for t in ts.tokens()] == ["colors.white", "colors.ink", "bg", "fg"]
    assert dict(ts.axes) == {"scheme": ("light", "dark")}
    assert (ts.get("bg").value, ts.get("bg").modes) == ("{colors.white}",
                                                        {"scheme:dark": "{colors.ink}"})
    assert ts.resolve("bg", "scheme:dark") == "#111111"
    assert report.notes[0] == Item("studio.json $themes", "",
                                   "paired with the theme Light by token path into "
                                   "scheme:dark; 2 tokens take their dark value from here and "
                                   "2 are the same in both schemes")
    assert ("brand-b", "is a set in neither the light nor the dark theme; it was left out") \
        in _lines(report.notes)
    assert not any("does not hold" in n for _, n in _lines(report.notes))
    assert [i.name for i in report.not_read] == ["global.space.sm"]
    assert report.not_read[0].where == "studio.json global.space.sm"


def test_a_bare_dark_json_pairs_with_a_light_named_file(tmp_path):
    for light in ("light.json", "theme.light.json"):
        folder = tmp_path / light.split(".")[0]
        src = _write(folder / light, LIGHT)
        _write(folder / "dark.json", DARK)
        imported = read_dtcg(src)
        assert imported.tokens.get("color.bg").modes == {"scheme:dark": "#111111"}
        assert [s.path for s in imported.report.also_read] == [str(folder / "dark.json")]


def test_a_bare_dark_json_beside_a_file_not_named_light_is_a_candidate(tmp_path):
    src = _write(tmp_path / "tokens.json", LIGHT)
    _write(tmp_path / "dark.json", DARK)
    imported = read_dtcg(src)
    assert dict(imported.tokens.axes) == {} and imported.report.also_read == []
    assert imported.report.notes[0] == Item(
        "dark.json", "", "sits beside tokens.json and may hold its dark scheme, but was not "
                         "paired, since neither file is named for light; rename tokens.json to "
                         "light.json, or dark.json to tokens.dark.json, and import again to "
                         "read it as scheme:dark")


def test_a_bare_dark_json_beside_a_light_json_is_that_files_not_anothers(tmp_path):
    src = _write(tmp_path / "tokens.json", LIGHT)
    _write(tmp_path / "light.json", LIGHT)
    _write(tmp_path / "dark.json", DARK)
    imported = read_dtcg(src)
    assert imported.report.also_read == []
    assert imported.report.notes[0] == Item(
        "dark.json", "", "sits beside light.json, so it is read as the dark half of light.json, "
                         "not of tokens.json; import light.json to read the two schemes "
                         "together")


def test_a_literal_inside_a_partly_aliased_composite_is_named():
    doc = {"font": {"$type": "fontFamily", "body": {"$value": ["Inter", "sans-serif"]}},
           "shade": {"$type": "color", "soft": {"$value": "#00000033"}},
           "type": {"$type": "typography", "body": {"$value": {
               "fontFamily": "{font.body}", "fontSize": {"value": 16, "unit": "px"},
               "fontWeight": 400, "lineHeight": 1.5,
               "letterSpacing": {"value": 0, "unit": "px"}}}},
           "lift": {"$type": "shadow", "card": {"$value": {
               "color": "{shade.soft}", "offsetX": {"value": 0, "unit": "px"},
               "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 2, "unit": "px"},
               "spread": {"value": 0, "unit": "px"}}}}}
    imported = _import(doc)
    assert imported.tokens.get("type.body").layer == "semantic"
    notes = [(i.name, i.message) for i in imported.report.notes
             if "a literal inside a semantic token" in i.message]
    assert notes[0] == (
        "type.body", "its field fontSize (16px) is a literal inside a semantic token; extract "
                     "it to a primitive token and alias it, as fontFamily is")
    assert [n for n, _ in notes] == ["type.body"] * 4 + ["lift.card"] * 4
    assert "its field blur (2px) is" in notes[6][1]


def test_a_composite_with_every_field_aliased_or_none_has_no_literal_note():
    doc = {"font": {"$type": "fontFamily", "body": {"$value": ["Inter", "sans-serif"]}},
           "type": {"$type": "typography", "body": {"$value": {
               "fontFamily": ["Inter"], "fontSize": {"value": 16, "unit": "px"},
               "fontWeight": 400, "lineHeight": 1.5,
               "letterSpacing": {"value": 0, "unit": "px"}}}}}
    imported = _import(doc)
    assert imported.tokens.get("type.body").layer == "primitive"
    assert not [i for i in imported.report.notes if "literal inside" in i.message]


def test_a_bare_dark_json_in_a_light_folder_pairs(tmp_path):
    src = _write(tmp_path / "light" / "tokens.json", LIGHT)
    _write(tmp_path / "light" / "dark.json", DARK)
    imported = read_dtcg(src)
    assert imported.tokens.get("color.bg").modes == {"scheme:dark": "#111111"}
    assert not any("named for light" in i.message for i in imported.report.notes)
