import json

import pytest

from engine.foundations import build_color, from_dtcg, to_css, to_dtcg
from engine.foundations.export import EXT
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)


def test_dtcg_roundtrip_is_lossless():
    ts = build_color(AXES, "#3366FF").tokens
    doc = to_dtcg(ts)
    assert to_dtcg(from_dtcg(doc)) == doc


def test_dtcg_shape():
    doc = to_dtcg(build_color(AXES, "#3366FF").tokens)
    leaf = doc["color"]["text"]["default"]
    assert leaf["$type"] == "color" and leaf["$value"].startswith("{color.neutral.")
    assert leaf["$extensions"][EXT]["layer"] == "semantic"
    assert doc["color"]["brand"]["500"]["$value"] == {
        "colorSpace": "srgb", "components": [0.2, 0.4, 1.0], "hex": "#3366FF"}


def test_css_semantics_are_vars_and_dark_overrides_only_semantics():
    css = to_css(build_color(AXES, "#3366FF").tokens)
    assert "--color-brand-500: #3366FF;" in css
    assert "--color-text-default: var(--color-neutral-900);" in css
    dark = css.split('[data-theme="dark"]')[1].split("}")[0]
    assert "--color-surface-page: var(--color-neutral-950);" in dark
    # the dark block only re-points semantics; it never redefines a primitive
    assert "--color-brand-500:" not in dark and "--color-neutral-950:" not in dark
    assert "@media (prefers-color-scheme: dark)" in css


def test_byte_identical_output():
    a = json.dumps(to_dtcg(build_color(AXES, "#E61428").tokens), sort_keys=False)
    b = json.dumps(to_dtcg(build_color(AXES, "#E61428").tokens), sort_keys=False)
    assert a == b and to_css(build_color(AXES, "#E61428").tokens) == to_css(build_color(AXES, "#E61428").tokens)


def test_css_emits_mode_overrides_whatever_the_layer():
    # R27 I1: the gate reads modes regardless of layer, so the exporter must too.
    from engine.foundations.tokens import Token, TokenSet
    ts = TokenSet()
    ts.add(Token("color.a", "color", "#FFFFFF"))
    ts.add(Token("color.b", "color", "#000000"))
    ts.add(Token("color.role", "color", "{color.a}", layer="Semantic", modes={"dark": "{color.b}"}))
    dark = to_css(ts).split('[data-theme="dark"]')[1].split("}")[0]
    assert "--color-role: var(--color-b);" in dark


def test_from_dtcg_tolerates_null_extensions():
    # R27 M4: "$extensions": null used to raise AttributeError.
    doc = {"color": {"base": {
        "white": {"$type": "color", "$value": "#FFFFFF", "$extensions": None},
        "black": {"$type": "color", "$value": "#000000", "$extensions": {EXT: {"modes": None}}},
        "grey": {"$type": "color", "$value": "#777777", "$extensions": {EXT: None}},
    }}}
    ts = from_dtcg(doc)
    for path in ("color.base.white", "color.base.black", "color.base.grey"):
        t = ts.get(path)
        assert t.layer == "primitive" and t.modes == {}


def test_from_dtcg_inherits_group_type():
    # R27 M4: DTCG lets a group declare $type for every token below it; the
    # nearest declaration wins and a token's own $type wins over all.
    doc = {
        "$type": "color",
        "color": {
            "base": {"white": {"$value": "#FFFFFF"}},
            "odd": {"$type": "dimension",
                    "inner": {"gap": {"$value": "4px"}},
                    "own": {"$type": "color", "$value": "#000000"}},
        },
    }
    ts = from_dtcg(doc)
    assert ts.get("color.base.white").type == "color"
    assert ts.get("color.odd.inner.gap").type == "dimension"
    assert ts.get("color.odd.own").type == "color"


def _props(block):
    return [line.split(":")[0].strip() for line in block.strip().splitlines()]


def test_css_light_scope_restores_base_values():
    # R27 M6: a light subtree inside a dark page (or a light-scoped
    # component under OS dark) needs every re-pointed property set back.
    css = to_css(build_color(AXES, "#3366FF").tokens)
    light = css.split('[data-theme="light"] {')[1].split("}")[0]
    dark = css.split('[data-theme="dark"] {')[1].split("}")[0]
    assert "--color-surface-page: var(--color-neutral-50);" in light
    assert "--color-text-default: var(--color-neutral-900);" in light
    assert _props(light) == _props(dark) and _props(light)
    assert "--color-brand-500:" not in light


@pytest.mark.parametrize("order", [("radius", "radius.card"), ("radius.card", "radius")])
def test_to_dtcg_raises_on_a_path_conflict_instead_of_dropping(order):
    from engine.foundations.tokens import Token, TokenSet
    ts = TokenSet()
    for path in order:
        ts.add(Token(path, "color", "#111111"))
    with pytest.raises(ValueError, match=r"radius is a token and also a group holding radius\.card; "
                                         r"DTCG cannot hold both, so rename one"):
        to_dtcg(ts)


@pytest.mark.parametrize("ext", [
    {"ux.layer": "semantic", "ux.modes": {"dark": "{color.base.white}"}},
    {"ux.layer": "semantic"},
    {"ux.modes": {"dark": "{color.base.white}"}},
    {EXT: {"layer": "semantic"}, "ux.layer": "semantic"},
])
def test_from_dtcg_rejects_the_old_extension_keys_by_name(ext):
    doc = {"color": {
        "base": {"black": {"$type": "color", "$value": "#000000"},
                 "white": {"$type": "color", "$value": "#FFFFFF"}},
        "text": {"default": {"$type": "color", "$value": "{color.base.black}",
                             "$extensions": ext},
                 "muted": {"$type": "color", "$value": "{color.base.black}",
                           "$extensions": {"ux.layer": "semantic"}}},
    }}
    with pytest.raises(ValueError) as exc:
        from_dtcg(doc)
    msg = str(exc.value)
    assert msg.startswith("color.text.default ")
    assert "this file was written by an older build; re-export it with the current version" in msg
