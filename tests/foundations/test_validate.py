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
