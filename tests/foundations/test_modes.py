"""Named mode axes: keys, contexts, the most-specific-override rule, the
validate rules that guard them, CSS selectors and the DTCG round trip."""
import pytest

from engine.foundations.export import EXT, from_dtcg, to_css, to_dtcg
from engine.foundations.gate import Check, Pairing, gate
from engine.foundations.modes import (
    AXES, FOUNDATION_AXES, ModeError, compress, contexts, parse, select, sparse)
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate


def test_axes_are_the_required_five_with_base_first():
    assert dict(AXES) == {"scheme": ("light", "dark"), "contrast": ("standard", "high"),
                          "density": ("comfortable", "compact"), "direction": ("ltr", "rtl"),
                          "motion": ("standard", "reduced")}
    assert FOUNDATION_AXES["color"] == ("scheme", "contrast")
    assert FOUNDATION_AXES["space"] == FOUNDATION_AXES["layout"] == ("density",)
    assert FOUNDATION_AXES["type"] == ("direction",)


@pytest.mark.parametrize("key, pairs", [
    ("", {}), ("dark", {"scheme": "dark"}), ("rtl", {"direction": "rtl"}),
    ("contrast:high,scheme:dark", {"contrast": "high", "scheme": "dark"}),
    ("scheme:light", {"scheme": "light"}),
])
def test_parse(key, pairs):
    assert parse(key) == pairs


@pytest.mark.parametrize("key, message", [
    ("sepia", r"'sepia' is not a value of any axis; write it as axis:value"),
    ("standard", r"'standard' is a value of contrast and motion; write it as axis:value"),
    ("shade:dark", r"names axis 'shade'; use one of \['scheme'"),
    ("scheme:dim", r"sets scheme to 'dim'; use one of \['light', 'dark'\]"),
    ("dark,scheme:light", r"sets scheme twice; keep one value"),
])
def test_bad_keys_name_the_fix(key, message):
    with pytest.raises(ModeError, match=message):
        parse(key)


def test_contexts_are_explicit_base_first_first_axis_slowest():
    assert contexts(("contrast", "scheme")) == [
        "scheme:light,contrast:standard", "scheme:light,contrast:high",
        "scheme:dark,contrast:standard", "scheme:dark,contrast:high"]
    assert contexts(()) == [""]
    assert sparse("scheme:light,contrast:high") == "contrast:high"


def test_select_prefers_the_override_naming_most_axes():
    modes = {"scheme:dark": "D", "contrast:high": "H", "scheme:dark,contrast:high": "DH"}
    assert select("B", modes, "scheme:light,contrast:standard") == ("B", [])
    assert select("B", modes, "dark") == ("D", [])
    assert select("B", modes, "contrast:high") == ("H", [])
    assert select("B", modes, "scheme:dark,contrast:high") == ("DH", [])


def test_select_reports_a_tie_with_different_values():
    value, tied = select("B", {"scheme:dark": "D", "contrast:high": "H"}, "scheme:dark,contrast:high")
    assert tied == ["scheme:dark", "contrast:high"]
    assert select("B", {"scheme:dark": "X", "contrast:high": "X"}, "dark,contrast:high") == ("X", [])


@pytest.mark.parametrize("values, overrides", [
    (("a", "a", "a", "a"), {}),
    (("a", "a", "b", "b"), {"scheme:dark": "b"}),
    (("a", "b", "a", "b"), {"contrast:high": "b"}),
    (("a", "b", "c", "d"), {"contrast:high": "b", "scheme:dark": "c", "scheme:dark,contrast:high": "d"}),
    # dark and high each differ from base and would tie in dark+high
    (("a", "b", "c", "b"), {"contrast:high": "b", "scheme:dark": "c", "scheme:dark,contrast:high": "b"}),
    (("a", "a", "a", "d"), {"scheme:dark,contrast:high": "d"}),
])
def test_compress_reads_back_every_context_with_the_fewest_overrides(values, overrides):
    ctxs = contexts(("scheme", "contrast"))
    by_ctx = dict(zip(ctxs, values))
    base, modes = compress(by_ctx)
    assert base == "a" and modes == overrides
    for ctx in ctxs:
        assert select(base, modes, ctx) == (by_ctx[ctx], [])


def _color_set(**modes):
    ts = TokenSet()
    for path, hx in (("color.n.1", "#FFFFFF"), ("color.n.2", "#000000"), ("color.n.3", "#777777")):
        ts.add(Token(path, "color", hx))
    ts.add(Token("color.surface.page", "color", "{color.n.1}", modes=modes, layer="semantic"))
    return ts


def test_raw_names_the_token_and_fix_on_a_tie():
    ts = _color_set(**{"scheme:dark": "{color.n.2}", "contrast:high": "{color.n.3}"})
    with pytest.raises(ModeError, match=r"color\.surface\.page has overrides \['scheme:dark', "
                                        r"'contrast:high'\] that all apply .*add an override for "
                                        r"'scheme:dark,contrast:high'"):
        ts.raw("color.surface.page", "scheme:dark,contrast:high")


@pytest.mark.parametrize("modes, rule", [
    ({"sepia": "{color.n.2}"}, "unknown-mode"),
    ({"scheme:light": "{color.n.2}"}, "base-mode-override"),
    ({"density:compact": "{color.n.2}"}, "axis-not-allowed"),
    ({"scheme:dark": "{color.n.2}", "contrast:high": "{color.n.3}"}, "mode-ambiguous"),
])
def test_validate_guards_override_keys(modes, rule):
    found = [p for p in validate(_color_set(**modes)) if p.token == "color.surface.page"]
    assert [p.rule for p in found] == [rule]
    assert "color.surface.page" in found[0].message


def test_axis_not_allowed_names_the_foundation_axes():
    ts = TokenSet()
    ts.add(Token("space.4", "dimension", {"value": 16, "unit": "px"}))
    ts.add(Token("space.gap", "dimension", "{space.4}", modes={"scheme:dark": "{space.4}"},
                 layer="semantic"))
    msg = [p.message for p in validate(ts) if p.rule == "axis-not-allowed"][0]
    assert msg == ("space.gap varies on scheme, but space tokens vary only on ['density']; "
                   "remove the 'scheme:dark' override")


def test_gate_walks_every_context_of_the_pairing_foundation():
    ts = _color_set(**{"scheme:dark": "{color.n.2}"})
    ts.add(Token("color.text.default", "color", "{color.n.2}", modes={"scheme:dark": "{color.n.1}"},
                 layer="semantic"))
    report = gate(ts, [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")])
    assert report.checked == 4 and report.passed


def test_gate_runs_a_check_in_every_context_of_its_axes():
    seen = []
    gate(TokenSet(), [], [Check("c", "system", lambda ts, m: seen.append(m) or [],
                                axes=("density", "direction"))])
    assert seen == contexts(("density", "direction"))


def test_css_sets_each_axis_by_attribute_or_media_query():
    ts = _color_set(**{"scheme:dark": "{color.n.2}", "contrast:high": "{color.n.3}",
                       "scheme:dark,contrast:high": "{color.n.1}"})
    ts.add(Token("space.4", "dimension", {"value": 16, "unit": "px"}))
    ts.add(Token("space.2", "dimension", {"value": 8, "unit": "px"}))
    ts.add(Token("space.gap", "dimension", "{space.4}", modes={"density:compact": "{space.2}"},
                 layer="semantic"))
    css = to_css(ts)
    for block in (
        ':root[data-theme="dark"] {\n  --color-surface-page: var(--color-n-2);\n}',
        '@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {\n'
        '    --color-surface-page: var(--color-n-2);\n  }\n}',
        ':root[data-contrast="high"] {\n  --color-surface-page: var(--color-n-3);\n}',
        '@media (prefers-contrast: more) {\n  :root:not([data-contrast="standard"]) {',
        ':root[data-theme="dark"][data-contrast="high"] {\n  --color-surface-page: var(--color-n-1);\n}',
        '@media (prefers-contrast: more) {\n  :root[data-theme="dark"]:not([data-contrast="standard"]) {',
        '@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"])[data-contrast="high"] {',
        '@media (prefers-color-scheme: dark) and (prefers-contrast: more) {\n'
        '  :root:not([data-theme="light"]):not([data-contrast="standard"]) {',
        ':root[data-density="compact"] {\n  --space-gap: var(--space-2);\n}',
    ):
        assert block in css, block
    assert "prefers-density" not in css
    # single-axis rules come before combined ones
    assert css.index(':root[data-contrast="high"] {') < css.index(
        ':root[data-theme="dark"][data-contrast="high"] {')


def test_css_direction_uses_the_dir_attribute():
    ts = TokenSet()
    ts.add(Token("type.tracking.0", "dimension", {"value": 0, "unit": "px"}))
    ts.add(Token("type.tracking.1", "dimension", {"value": -0.5, "unit": "px"}))
    ts.add(Token("type.heading-tracking", "dimension", "{type.tracking.1}",
                 modes={"direction:rtl": "{type.tracking.0}"}, layer="semantic"))
    assert ':root[dir="rtl"] {\n  --type-heading-tracking: var(--type-tracking-0);\n}' in to_css(ts)


def test_dtcg_records_the_axes_and_round_trips_them():
    ts = _color_set(**{"scheme:dark": "{color.n.2}", "scheme:dark,contrast:high": "{color.n.3}"})
    doc = to_dtcg(ts)
    assert doc["$extensions"][EXT]["axes"]["density"] == ["comfortable", "compact"]
    assert doc["color"]["surface"]["page"]["$extensions"][EXT]["modes"] == {
        "scheme:dark": "{color.n.2}", "scheme:dark,contrast:high": "{color.n.3}"}
    back = from_dtcg(doc)
    assert dict(back.axes) == dict(AXES) and to_dtcg(back) == doc


def test_dtcg_with_its_own_axes_round_trips():
    ts = TokenSet({"scheme": ("light", "dark", "dim")})
    ts.add(Token("color.a", "color", "#FFFFFF"))
    ts.add(Token("color.b", "color", "#222222"))
    ts.add(Token("color.page", "color", "{color.a}", modes={"scheme:dim": "{color.b}"},
                 layer="semantic"))
    back = from_dtcg(to_dtcg(ts))
    assert back.axes["scheme"] == ("light", "dark", "dim")
    assert back.resolve("color.page", "scheme:dim") == "#222222"
