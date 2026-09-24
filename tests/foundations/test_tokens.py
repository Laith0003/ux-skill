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


def test_self_alias_is_a_cycle():
    ts = TokenSet()
    ts.add(Token("a", "color", "{a}", layer="semantic"))
    with pytest.raises(AliasError, match="cycle"):
        ts.resolve("a", "light")


def test_missing_target_names_the_holder_and_the_root():
    ts = TokenSet()
    ts.add(Token("a", "color", "{b}", layer="semantic"))
    ts.add(Token("b", "color", "{missing}", layer="semantic"))
    with pytest.raises(AliasError, match=r"b aliases missing.*resolving a"):
        ts.resolve("a", "light")


def test_multi_hop_dark_fallthrough():
    ts = TokenSet()
    ts.add(Token("color.neutral.900", "color", "#111111"))
    ts.add(Token("color.text.default", "color", "{color.neutral.900}", layer="semantic"))
    ts.add(Token("color.text.emphasis", "color", "#000000",
                 modes={"dark": "{color.text.default}"}, layer="semantic"))
    assert ts.resolve("color.text.emphasis", "dark") == "#111111"


def test_undefined_root_path_raises():
    ts = TokenSet()
    with pytest.raises(AliasError, match="nope is not defined"):
        ts.resolve("nope", "light")


def test_unknown_mode_raises_on_resolve():
    ts = make()
    with pytest.raises(ValueError, match=r"dakr.*light.*dark"):
        ts.resolve("color.surface.page", "dakr")


def test_unknown_mode_raises_on_raw():
    ts = make()
    with pytest.raises(ValueError, match=r"dakr.*light.*dark"):
        ts.raw("color.surface.page", "dakr")


@pytest.mark.parametrize("axes", [{"Scheme": ("light", "dark")},
                                  {"scheme": ("light", "light")}, {"scheme": ("light", "dark mode")}])
def test_unusable_axes_are_rejected(axes):
    with pytest.raises(ValueError, match=r"is not usable; name axes and values with lowercase"):
        TokenSet(axes)


@pytest.mark.parametrize("values", [("light",), ("light", "dark", "dim"), ()])
def test_an_axis_needs_exactly_two_values(values):
    with pytest.raises(ValueError, match=r"axis 'scheme' has values .*; a mode axis has exactly "
                                         r"two values, the base first"):
        TokenSet({"scheme": values})


def test_get_unknown_path_names_the_fix():
    # R27 M1: a bare KeyError('color.nope') names no fix.
    with pytest.raises(KeyError, match=r"color\.nope is not defined; add it or check the spelling"):
        make().get("color.nope")


def test_raw_unknown_path_names_the_fix():
    with pytest.raises(KeyError, match=r"color\.nope is not defined; add it or check the spelling"):
        make().raw("color.nope", "light")


def test_unknown_mode_message_names_the_fix():
    # R27 M2: the message listed the allowed modes but never said what to do.
    with pytest.raises(ValueError, match=r"write it as axis:value, one of scheme: light, dark"):
        make().raw("color.surface.page", "dakr")


def test_alias_error_carries_its_cause():
    # R27 M3: callers branch on .cause, never on the message text.
    cyc = TokenSet()
    cyc.add(Token("a", "color", "{b}", layer="semantic"))
    cyc.add(Token("b", "color", "{a}", layer="semantic"))
    with pytest.raises(AliasError) as exc:
        cyc.resolve("a", "light")
    assert exc.value.cause == "cycle"

    missing = TokenSet()
    missing.add(Token("a", "color", "{b}", layer="semantic"))
    with pytest.raises(AliasError) as exc:
        missing.resolve("a", "light")
    assert exc.value.cause == "missing"

    with pytest.raises(AliasError) as exc:
        TokenSet().resolve("nope", "light")
    assert exc.value.cause == "missing"
