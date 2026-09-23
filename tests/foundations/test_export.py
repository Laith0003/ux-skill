import json

from engine.foundations import build_color, from_dtcg, to_css, to_dtcg
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)


def test_dtcg_roundtrip_is_lossless():
    ts, _ = build_color(AXES, "#3366FF")
    doc = to_dtcg(ts)
    assert to_dtcg(from_dtcg(doc)) == doc


def test_dtcg_shape():
    doc = to_dtcg(build_color(AXES, "#3366FF")[0])
    leaf = doc["color"]["text"]["default"]
    assert leaf["$type"] == "color" and leaf["$value"].startswith("{color.neutral.")
    assert leaf["$extensions"]["ux.layer"] == "semantic"
    assert doc["color"]["brand"]["500"]["$value"] == "#3366FF"


def test_css_semantics_are_vars_and_dark_overrides_only_semantics():
    css = to_css(build_color(AXES, "#3366FF")[0])
    assert "--color-brand-500: #3366FF;" in css
    assert "--color-text-default: var(--color-neutral-900);" in css
    dark = css.split('[data-theme="dark"]')[1].split("}")[0]
    assert "--color-surface-page: var(--color-neutral-950);" in dark
    # the dark block only re-points semantics; it never redefines a primitive
    assert "--color-brand-500:" not in dark and "--color-neutral-950:" not in dark
    assert "@media (prefers-color-scheme: dark)" in css


def test_byte_identical_output():
    a = json.dumps(to_dtcg(build_color(AXES, "#E61428")[0]), sort_keys=False)
    b = json.dumps(to_dtcg(build_color(AXES, "#E61428")[0]), sort_keys=False)
    assert a == b and to_css(build_color(AXES, "#E61428")[0]) == to_css(build_color(AXES, "#E61428")[0])
