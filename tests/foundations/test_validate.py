import pytest

from engine.foundations.color import generate_color
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)


def rules(ts):
    return sorted(p.rule for p in validate(ts))


def test_generated_color_is_valid():
    assert validate(generate_color(AXES, "#3366FF").tokens) == []


def test_each_rule_fires():
    ts = TokenSet()
    ts.add(Token("color.x.500", "color", "#111111"))
    ts.add(Token("color.x.600", "color", "{color.x.500}"))
    ts.add(Token("color.x.700", "color", "#222222", modes={"dark": "#333333"}))
    ts.add(Token("color.text.a", "color", "#444444", layer="semantic"))
    ts.add(Token("color.text.b", "color", "{color.text.a}", layer="semantic"))
    ts.add(Token("color.text.c", "color", "{color.missing.1}", layer="semantic"))
    ts.add(Token("color.text.d", "color", "{color.x.500}", layer="semantic", modes={"sepia": "{color.x.500}"}))
    assert rules(ts) == ["alias-missing", "primitive-alias", "primitive-modes",
                         "semantic-literal", "semantic-to-semantic", "unknown-mode"]


def test_messages_name_token_and_fix():
    ts = TokenSet()
    ts.add(Token("color.text.a", "color", "#444444", layer="semantic"))
    msg = validate(ts)[0].message
    assert "color.text.a" in msg and "alias a primitive" in msg


def test_every_mode_checked_light_literal_does_not_hide_dark_alias_missing():
    ts = TokenSet()
    ts.add(Token("color.text.a", "color", "#444444",
                 modes={"dark": "{color.missing.1}"}, layer="semantic"))
    found = sorted(p.rule for p in validate(ts) if p.token == "color.text.a")
    assert found == ["alias-missing", "semantic-literal"]


def test_distinct_raw_value_reported_only_once_per_token():
    ts = TokenSet()
    ts.add(Token("color.text.a", "color", "#444444", layer="semantic"))
    problems = [p for p in validate(ts) if p.token == "color.text.a"]
    assert len(problems) == 1
    assert problems[0].rule == "semantic-literal"


def test_alias_cycle_reported_for_semantic_pointing_into_a_cycle():
    ts = TokenSet()
    ts.add(Token("color.p.a", "color", "{color.p.b}"))
    ts.add(Token("color.p.b", "color", "{color.p.a}"))
    ts.add(Token("color.text.z", "color", "{color.p.a}", layer="semantic"))
    found = [p for p in validate(ts) if p.token == "color.text.z"]
    assert "alias-cycle" in [p.rule for p in found]
    cycle_problem = next(p for p in found if p.rule == "alias-cycle")
    assert "color.p.a" in cycle_problem.message and "color.p.b" in cycle_problem.message


def test_missing_target_reached_through_a_primitive_is_alias_missing():
    # s.x -> p.a -> p.missing is a missing target, not a cycle.
    ts = TokenSet()
    ts.add(Token("color.p.a", "color", "{color.p.missing}"))
    ts.add(Token("color.text.z", "color", "{color.p.a}", layer="semantic"))
    found = [p.rule for p in validate(ts) if p.token == "color.text.z"]
    assert found == ["alias-missing"]


def test_unknown_layer_rejected():
    # A layer typo would read as semantic in validate and as "not
    # semantic" in to_css, so the dark override would silently vanish.
    ts = TokenSet()
    ts.add(Token("color.neutral.50", "color", "#FAFAFA"))
    ts.add(Token("color.surface.page", "color", "{color.neutral.50}", layer="Semantic"))
    found = [p for p in validate(ts) if p.token == "color.surface.page"]
    assert [p.rule for p in found] == ["unknown-layer"]
    assert "color.surface.page has layer 'Semantic'" in found[0].message
    assert "use 'primitive' or 'semantic'" in found[0].message


def test_layer_typo_through_dtcg_is_caught():
    from engine.foundations.export import from_dtcg, to_dtcg
    doc = to_dtcg(generate_color(AXES, "#3366FF").tokens)
    from engine.foundations.export import EXT
    doc["color"]["surface"]["page"]["$extensions"][EXT]["layer"] = "Semantic"
    assert "unknown-layer" in rules(from_dtcg(doc))


def test_unknown_type_rejected():
    # Token.type is checked against the known types.
    ts = TokenSet()
    ts.add(Token("color.x.500", "colour", "#111111"))
    found = validate(ts)
    assert [p.rule for p in found] == ["unknown-type"]
    assert "color.x.500 has type 'colour'" in found[0].message
    assert "use one of ['color', 'cubicBezier', 'dimension'" in found[0].message


BAD_COLOR_VALUES = [
    "#GGGGGG", "rgb(250,250,250)", "#12345", "3366FF", " #3366FF", "",
    "red; } body { display:none", {"colorSpace": "srgb", "components": [1, 1, 1]}, None,
]


@pytest.mark.parametrize("value", BAD_COLOR_VALUES)
def test_bad_color_literal_rejected(value):
    # A color literal must be #RGB or #RRGGBB, so nothing
    # else (a malformed hex, a CSS function, a DTCG object, CSS injection)
    # reaches the gate or the CSS.
    ts = TokenSet()
    ts.add(Token("color.neutral.50", "color", value))
    found = validate(ts)
    assert [p.rule for p in found] == ["bad-value"]
    assert f"color.neutral.50 is type color but holds {value!r}" in found[0].message
    assert "use #RRGGBB or #RGB" in found[0].message


@pytest.mark.parametrize("value", ["#abc", "#ABC", "#aabbcc", "#AABBCC"])
def test_good_color_literals_pass(value):
    ts = TokenSet()
    ts.add(Token("color.neutral.50", "color", value))
    assert validate(ts) == []


def test_bad_value_in_a_mode_is_named_with_its_mode():
    ts = TokenSet()
    ts.add(Token("color.x.500", "color", "#111111"))
    ts.add(Token("color.text.a", "color", "{color.x.500}", layer="semantic",
                 modes={"dark": "#12"}))
    found = [p for p in validate(ts) if p.rule == "bad-value"]
    assert len(found) == 1 and "color.text.a (dark) is type color but holds '#12'" in found[0].message


def test_bad_value_through_dtcg_is_caught():
    from engine.foundations.export import from_dtcg, to_dtcg
    doc = to_dtcg(generate_color(AXES, "#3366FF").tokens)
    doc["color"]["neutral"]["50"]["$value"] = "#GGGGGG"
    found = [p for p in validate(from_dtcg(doc)) if p.rule == "bad-value"]
    assert [p.token for p in found] == ["color.neutral.50"]


def test_value_rules_are_table_driven():
    from engine.foundations.values import TYPES
    assert set(TYPES) == {"color", "cubicBezier", "dimension", "duration", "fontFamily",
                          "fontWeight", "number", "shadow", "strokeStyle", "typography"}
    assert TYPES["color"].check("#3366FF") and not TYPES["color"].check("#GGGGGG")


@pytest.mark.parametrize("path, segment", [
    ("color.Brand Blue.500", "Brand Blue"),
    ("color..500", ""),
    ("color.brand.", ""),
    ("color.brand;x.500", "brand;x"),
])
def test_bad_name_rejected(path, segment):
    # Path segments go into CSS property names unescaped.
    ts = TokenSet()
    ts.add(Token(path, "color", "#111111"))
    found = [p for p in validate(ts) if p.rule == "bad-name"]
    assert len(found) == 1
    assert f"{path} has segment {segment!r}" in found[0].message
    assert "letters, digits, '_' and '-'" in found[0].message


@pytest.mark.parametrize("order", [("radius", "radius.card"), ("radius.card", "radius")])
def test_path_conflict_rejected_in_either_order(order):
    # DTCG cannot hold a token and a group at the same path, so to_dtcg
    # would drop one of them silently.
    ts = TokenSet()
    for path in order:
        ts.add(Token(path, "color", "#111111"))
    found = [p for p in validate(ts) if p.rule == "path-conflict"]
    assert len(found) == 1 and found[0].token == "radius.card"
    assert "radius is a token and also a group holding radius.card" in found[0].message
    assert "rename one" in found[0].message


def test_deep_path_conflict_names_each_prefix():
    ts = TokenSet()
    for path in ("a", "a.b", "a.b.c"):
        ts.add(Token(path, "color", "#111111"))
    found = sorted(p.message.split(" is a token")[0] + ">" + p.token
                   for p in validate(ts) if p.rule == "path-conflict")
    assert found == ["a.b>a.b.c", "a>a.b", "a>a.b.c"]


def test_css_collision_rejected():
    # Two paths that map to one custom property; the last one would win.
    ts = TokenSet()
    ts.add(Token("color.text-default", "color", "#111111"))
    ts.add(Token("color.text.default", "color", "#222222"))
    found = [p for p in validate(ts) if p.rule == "css-collision"]
    assert len(found) == 1 and found[0].token == "color.text.default"
    assert ("color.text-default and color.text.default both become the CSS property "
            "--color-text-default") in found[0].message
    assert "rename one" in found[0].message


def test_base_mode_override_is_rejected():
    # The base mode's value is the token's own value; to_css writes it into
    # :root. A separate override for the base mode would let the gate check
    # one color while the CSS ships another.
    ts = TokenSet()
    ts.add(Token("color.neutral.50", "color", "#FAFAFA"))
    ts.add(Token("color.neutral.900", "color", "#111111"))
    ts.add(Token("color.surface.page", "color", "{color.neutral.900}", layer="semantic",
                 modes={"light": "{color.neutral.50}"}))
    problems = [p for p in validate(ts) if p.rule == "base-mode-override"]
    assert len(problems) == 1
    msg = problems[0].message
    assert "color.surface.page" in msg and "light" in msg and "$value" in msg
