import pytest

from engine.foundations.tokens import AliasError, Token, TokenSet, alias_target, is_alias


def make():
    ts = TokenSet()
    ts.add(Token("color.neutral.50", "color", "#FAFAFA"))
    ts.add(Token("color.neutral.950", "color", "#0A0A0A"))
    ts.add(Token("color.surface.page", "color", "{color.neutral.50}",
                 modes={"dark": "{color.neutral.950}"}, layer="semantic"))
    return ts


def test_alias_helpers():
    assert is_alias("{a.b}") and not is_alias("#fff")
    assert alias_target("{color.neutral.50}") == "color.neutral.50"


def test_resolve_per_mode():
    ts = make()
    assert ts.resolve("color.surface.page", "light") == "#FAFAFA"
    assert ts.resolve("color.surface.page", "dark") == "#0A0A0A"


def test_duplicate_path_rejected():
    ts = make()
    with pytest.raises(ValueError, match="color.neutral.50"):
        ts.add(Token("color.neutral.50", "color", "#000000"))


def test_missing_alias_names_both_tokens():
    ts = TokenSet()
    ts.add(Token("color.text.default", "color", "{color.nope.900}", layer="semantic"))
    with pytest.raises(AliasError, match=r"color\.text\.default.*color\.nope\.900"):
        ts.resolve("color.text.default", "light")


def test_cycle_detected():
    ts = TokenSet()
    ts.add(Token("a", "color", "{b}", layer="semantic"))
    ts.add(Token("b", "color", "{a}", layer="semantic"))
    with pytest.raises(AliasError, match="cycle"):
        ts.resolve("a", "light")


def test_insertion_order_is_stable():
    assert [t.path for t in make().tokens()] == [
        "color.neutral.50", "color.neutral.950", "color.surface.page"]
