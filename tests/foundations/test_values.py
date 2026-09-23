"""The value model: one checker, one DTCG 2025.10 codec and one CSS
printer per token type, composites included."""
import json

import pytest

from engine.foundations.export import from_dtcg, to_css, to_dtcg
from engine.foundations.gate import Pairing, gate
from engine.foundations.tokens import AliasError, Token, TokenSet
from engine.foundations.validate import validate
from engine.foundations.values import TYPES, css_entries, decode, encode

GOOD = {
    "color": ["#3366FF", "#abc", "#00000026"],
    "dimension": [{"value": 16, "unit": "px"}, {"value": 0.5, "unit": "rem"},
                  {"value": -1.5, "unit": "px"}],
    "duration": [{"value": 200, "unit": "ms"}, {"value": 0.3, "unit": "s"}],
    "cubicBezier": [[0.2, 0, 0, 1], [0, 0, 1, 1], [0.3, -0.5, 0.7, 1.5]],
    "fontFamily": ["Source Sans 3", ["IBM Plex Sans Arabic", "sans-serif"]],
    "fontWeight": [400, 650, 1000],
    "number": [1.5, 0, -1, 12],
    "strokeStyle": ["solid", "dashed"],
    "shadow": [[{"color": "#0000001A", "offsetX": {"value": 0, "unit": "px"},
                 "offsetY": {"value": 2, "unit": "px"}, "blur": {"value": 6, "unit": "px"},
                 "spread": {"value": -1, "unit": "px"}}],
               [{"color": "{color.base.black}", "offsetX": {"value": 0, "unit": "px"},
                 "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 2, "unit": "px"},
                 "spread": {"value": 0, "unit": "px"}, "inset": True}]],
    "typography": [{"fontFamily": "{type.face.latin}", "fontSize": {"value": 1, "unit": "rem"},
                    "fontWeight": 400, "letterSpacing": {"value": 0, "unit": "px"},
                    "lineHeight": 1.5}],
}
BAD = {
    "color": ["#GGGGGG", "#12345", "rgba(0,0,0,.1)", {"colorSpace": "srgb", "components": [1, 1, 1]}],
    "dimension": ["16px", {"value": 16}, {"value": 16, "unit": "em"}, {"value": True, "unit": "px"},
                  {"value": float("nan"), "unit": "px"}, {"value": 1, "unit": "px", "x": 1}],
    "duration": ["200ms", {"value": 200, "unit": "px"}],
    "cubicBezier": [[0.2, 0, 0], [1.2, 0, 0, 1], [0, 0, -0.1, 1], "ease"],
    "fontFamily": [[], "", ["Inter; } body {"], 12],
    "fontWeight": [0, 1001, "bold", True],
    "number": ["1.5", True, float("inf")],
    "strokeStyle": ["wavy", {"dashArray": [], "lineCap": "round"}],
    "shadow": [[], [{"color": "#000000"}], "0 1px 2px black",
               [{"color": "#000000", "offsetX": "0px", "offsetY": {"value": 1, "unit": "px"},
                 "blur": {"value": 2, "unit": "px"}, "spread": {"value": 0, "unit": "px"}}]],
    "typography": [{"fontFamily": "Serif"}, "16px/1.5 serif"],
}


@pytest.mark.parametrize("type_, value", [(t, v) for t, vs in GOOD.items() for v in vs])
def test_good_literals_pass(type_, value):
    assert TYPES[type_].check(value)


@pytest.mark.parametrize("type_, value", [(t, v) for t, vs in BAD.items() for v in vs])
def test_bad_literals_fail_with_a_named_fix(type_, value):
    assert not TYPES[type_].check(value)
    ts = TokenSet()
    ts.add(Token("x.y", type_, value))
    found = [p for p in validate(ts) if p.rule == "bad-value"]
    assert len(found) == 1
    assert f"x.y is type {type_} but holds {value!r}; {TYPES[type_].expected}" == found[0].message


def test_every_type_has_good_and_bad_cases():
    assert set(GOOD) == set(TYPES) and set(BAD) == set(TYPES)


def test_color_encodes_to_a_2025_10_color_object():
    assert encode("color", "#3366FF") == {"colorSpace": "srgb", "components": [0.2, 0.4, 1.0],
                                          "hex": "#3366FF"}
    assert encode("color", "#abc")["hex"] == "#AABBCC"
    translucent = encode("color", "#00000026")
    assert translucent["alpha"] == round(0x26 / 255, 6) and translucent["hex"] == "#000000"


@pytest.mark.parametrize("hex_", ["#3366FF", "#00000026", "#FFFFFF00", "#0A0B0C", "#FEFDFC80"])
def test_color_round_trip_is_lossless(hex_):
    assert decode("color", encode("color", hex_)) == hex_


def test_decode_reads_components_when_hex_is_absent_and_accepts_old_hex_strings():
    assert decode("color", {"colorSpace": "srgb", "components": [0.2, 0.4, 1.0]}) == "#3366FF"
    assert decode("color", "#3366ff") == "#3366FF"


def test_decode_leaves_what_it_cannot_read_for_validate_to_name():
    oklch = {"colorSpace": "oklch", "components": [0.5, 0.1, 250]}
    assert decode("color", oklch) is oklch
    ts = TokenSet()
    ts.add(Token("color.x", "color", decode("color", oklch)))
    assert [p.rule for p in validate(ts)] == ["bad-value"]


def test_shadow_colors_are_encoded_layer_by_layer():
    layer = GOOD["shadow"][0][0]
    doc_value = encode("shadow", [layer])
    assert doc_value[0]["color"]["hex"] == "#000000" and doc_value[0]["color"]["alpha"] == round(0x1A / 255, 6)
    assert decode("shadow", doc_value) == [layer]
    assert encode("shadow", GOOD["shadow"][1]) == GOOD["shadow"][1]  # alias color unchanged


@pytest.mark.parametrize("type_, value, css", [
    ("dimension", {"value": 16, "unit": "px"}, "16px"),
    ("dimension", {"value": 1.125, "unit": "rem"}, "1.125rem"),
    ("dimension", {"value": -0.5, "unit": "px"}, "-0.5px"),
    ("duration", {"value": 200, "unit": "ms"}, "200ms"),
    ("cubicBezier", [0.2, 0, 0, 1], "cubic-bezier(0.2, 0, 0, 1)"),
    ("fontFamily", ["Source Sans 3", "system-ui", "sans-serif"], '"Source Sans 3", system-ui, sans-serif'),
    ("fontWeight", 600, "600"),
    ("number", 1.5, "1.5"),
    ("strokeStyle", "dashed", "dashed"),
    ("color", "#00000026", "#00000026"),
])
def test_css_prints_each_type(type_, value, css):
    assert css_entries("a.b", type_, value) == [("--a-b", css)]


def test_css_prints_a_shadow_with_aliases_and_inset():
    assert css_entries("e.s", "shadow", GOOD["shadow"][1]) == [
        ("--e-s", "inset 0px 1px 2px 0px var(--color-base-black)")]


def test_css_expands_typography_into_one_property_per_field():
    assert css_entries("type.text.body", "typography", GOOD["typography"][0]) == [
        ("--type-text-body-font-family", "var(--type-face-latin)"),
        ("--type-text-body-font-size", "1rem"),
        ("--type-text-body-font-weight", "400"),
        ("--type-text-body-letter-spacing", "0px"),
        ("--type-text-body-line-height", "1.5"),
    ]


def _typed_set():
    ts = TokenSet()
    ts.add(Token("type.face.latin", "fontFamily", ["Source Sans 3", "sans-serif"]))
    ts.add(Token("type.size.3", "dimension", {"value": 1, "unit": "rem"}))
    ts.add(Token("type.weight.400", "fontWeight", 400))
    ts.add(Token("type.tracking.0", "dimension", {"value": 0, "unit": "px"}))
    ts.add(Token("type.leading.3", "number", 1.5))
    ts.add(Token("type.text.body", "typography", {
        "fontFamily": "{type.face.latin}", "fontSize": "{type.size.3}",
        "fontWeight": "{type.weight.400}", "letterSpacing": "{type.tracking.0}",
        "lineHeight": "{type.leading.3}"}, layer="semantic"))
    ts.add(Token("color.base.black", "color", "#000000"))
    ts.add(Token("elevation.shadow.light.1", "shadow", GOOD["shadow"][0]))
    ts.add(Token("elevation.card", "shadow", "{elevation.shadow.light.1}", layer="semantic"))
    ts.add(Token("motion.curve.out", "cubicBezier", [0.2, 0, 0, 1]))
    ts.add(Token("motion.duration.2", "duration", {"value": 200, "unit": "ms"}))
    ts.add(Token("border.line.solid", "strokeStyle", "solid"))
    return ts


def test_typed_set_is_valid_and_round_trips_through_dtcg():
    ts = _typed_set()
    assert validate(ts) == []
    doc = to_dtcg(ts)
    assert to_dtcg(from_dtcg(json.loads(json.dumps(doc)))) == doc
    back = from_dtcg(doc)
    assert [(t.path, t.type, t.value, t.layer) for t in back.tokens()] == \
        [(t.path, t.type, t.value, t.layer) for t in ts.tokens()]


def test_resolve_follows_aliases_inside_a_composite():
    assert _typed_set().resolve("type.text.body", "light") == {
        "fontFamily": ["Source Sans 3", "sans-serif"], "fontSize": {"value": 1, "unit": "rem"},
        "fontWeight": 400, "letterSpacing": {"value": 0, "unit": "px"}, "lineHeight": 1.5}


def test_a_composite_that_reaches_itself_is_a_cycle():
    ts = TokenSet()
    ts.add(Token("type.text.a", "typography", {
        "fontFamily": "{type.text.a}", "fontSize": "{type.text.a}", "fontWeight": 400,
        "letterSpacing": {"value": 0, "unit": "px"}, "lineHeight": 1.5}, layer="semantic"))
    with pytest.raises(AliasError) as exc:
        ts.resolve("type.text.a", "light")
    assert exc.value.cause == "cycle"


def test_alias_to_a_token_of_another_type_is_rejected():
    ts = _typed_set()
    ts.add(Token("type.text.bad", "typography", {
        "fontFamily": "{type.face.latin}", "fontSize": "{type.leading.3}",
        "fontWeight": "{type.weight.400}", "letterSpacing": "{type.tracking.0}",
        "lineHeight": "{type.leading.3}"}, layer="semantic"))
    ts.add(Token("color.text.odd", "color", "{type.size.3}", layer="semantic"))
    found = {(p.token, p.rule): p.message for p in validate(ts)}
    assert found[("type.text.bad", "alias-type")] == (
        "type.text.bad (light) field fontSize aliases type.leading.3, a number token, but needs "
        "a dimension token; point it at a dimension primitive")
    assert ("color.text.odd", "alias-type") in found


def test_semantic_typography_field_must_alias():
    ts = _typed_set()
    ts.add(Token("type.text.loose", "typography", dict(GOOD["typography"][0]), layer="semantic"))
    msgs = [p.message for p in validate(ts) if p.token == "type.text.loose"]
    assert "type.text.loose (light) field fontSize holds {'value': 1, 'unit': 'rem'}; alias a " \
           "dimension primitive instead" in msgs


def test_a_primitive_composite_may_not_alias():
    ts = TokenSet()
    ts.add(Token("color.base.black", "color", "#000000"))
    ts.add(Token("elevation.shadow.light.9", "shadow", GOOD["shadow"][1]))
    assert [p.rule for p in validate(ts)] == ["primitive-alias"]


def test_expanded_typography_names_count_for_css_collisions():
    ts = _typed_set()
    ts.add(Token("type.text.body-font-size", "dimension", {"value": 1, "unit": "rem"}))
    found = [p for p in validate(ts) if p.rule == "css-collision"]
    assert found and "--type-text-body-font-size" in found[0].message


def test_css_for_a_typed_set_prints_every_type():
    css = to_css(_typed_set())
    for line in ("--type-face-latin: \"Source Sans 3\", sans-serif;",
                 "--type-text-body-font-size: var(--type-size-3);",
                 "--elevation-card: var(--elevation-shadow-light-1);",
                 "--elevation-shadow-light-1: 0px 2px 6px -1px #0000001A;",
                 "--motion-curve-out: cubic-bezier(0.2, 0, 0, 1);",
                 "--motion-duration-2: 200ms;",
                 "--border-line-solid: solid;"):
        assert line in css, line


def test_gate_refuses_a_translucent_color_by_name():
    ts = TokenSet()
    ts.add(Token("color.scrim.40", "color", "#00000066"))
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    with pytest.raises(ValueError, match=r"color\.scrim\.40 \(light\) resolves to the translucent "
                                         r"#00000066; contrast needs opaque colors"):
        gate(ts, [Pairing("color.scrim.40", "color.base.white", 3.0, "1.4.11")])
