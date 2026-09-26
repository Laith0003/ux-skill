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
    # The gate reads modes regardless of layer, so the exporter must too.
    from engine.foundations.tokens import Token, TokenSet
    ts = TokenSet()
    ts.add(Token("color.a", "color", "#FFFFFF"))
    ts.add(Token("color.b", "color", "#000000"))
    ts.add(Token("color.role", "color", "{color.a}", layer="Semantic", modes={"dark": "{color.b}"}))
    dark = to_css(ts).split('[data-theme="dark"]')[1].split("}")[0]
    assert "--color-role: var(--color-b);" in dark


def test_from_dtcg_tolerates_null_extensions():
    # "$extensions": null is read as no extensions, never an AttributeError.
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
    # DTCG lets a group declare $type for every token below it; the
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


def test_css_light_attribute_opts_out_of_the_dark_media_query():
    # data-theme="light" on the root keeps an OS-dark user on light values.
    css = to_css(build_color(AXES, "#3366FF").tokens)
    assert '@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {' in css


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


def test_css_carries_the_high_contrast_variant():
    css = to_css(build_color(AXES, "#3366FF").tokens)
    assert ':root[data-contrast="high"] {' in css
    assert '@media (prefers-contrast: more) {\n  :root:not([data-contrast="standard"]) {' in css
    assert ':root[data-theme="dark"][data-contrast="high"] {' in css


# A right to left or Arabic subtree gets the Arabic type
# anywhere on the page, not only on the root.
NESTED = ':is([dir="rtl"], [lang|="ar"])'


def _block(css, selector):
    head = selector + " {\n"
    assert head in css, selector
    return css.split(head, 1)[1].split("}", 1)[0]


def test_a_nested_rtl_or_arabic_subtree_gets_every_direction_override():
    from engine.foundations import build_system
    css = to_css(build_system(AXES, "#3366FF").tokens)
    root = _block(css, ':root[dir="rtl"]')
    nested = _block(css, f":root {NESTED}")
    assert nested == root
    assert "--type-text-body-font-family: var(--type-face-arabic);" in nested


def test_a_nested_subtree_keeps_the_axes_set_on_the_root():
    """dark high contrast on the root and an Arabic block inside: the
    combined override reaches the block with the root's other attributes."""
    from engine.foundations import build_system
    css = to_css(build_system(AXES, "#3366FF").tokens)
    combined = _block(css, ':root[data-contrast="high"][dir="rtl"]')
    assert _block(css, f':root[data-contrast="high"] {NESTED}') == combined
    media = css.split("@media (prefers-contrast: more) {\n  :root:not("
                      '[data-contrast="standard"]) ' + NESTED + " {\n", 1)
    assert len(media) == 2


def test_a_latin_only_set_gives_a_subtree_its_travel_sign_but_no_arabic_type():
    from engine.foundations import build_system
    css = to_css(build_system(AXES, "#3366FF", arabic=False).tokens)
    nested = _block(css, f":root {NESTED}")
    assert "--type-" not in nested and "--motion-" in nested
