"""Imagery: ratios, a scrim measured over the worst image, and a duotone
and tint in the brand's light, all from the axes."""
import pytest

from engine.foundations import build_system
from engine.foundations.color_math import contrast
from engine.foundations.gate import gate
from engine.foundations.imagery import (
    CHECKS, _over, card_ratio, duotone, generate_imagery, hero_ratio, scrim_alpha, scrim_base,
    tint_alpha)
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(**kw):
    values = dict(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


@pytest.mark.parametrize("kw, hero, card", [
    ({}, (16, 9), (3, 2)),
    ({"contrast": 1.0, "density": 0.0, "formality": 0.0}, (21, 9), (4, 3)),
    ({"contrast": 0.0, "density": 1.0, "formality": 1.0}, (4, 3), (3, 2)),
    ({"geometry": 0.0, "formality": 1.0}, (16, 9), (16, 9)),
    ({"geometry": 1.0, "formality": 0.0}, (16, 9), (1, 1)),
])
def test_ratios_follow_the_axes(kw, hero, card):
    assert hero_ratio(axes(**kw)) == hero and card_ratio(axes(**kw)) == card


@pytest.mark.parametrize("brand", ["#3366FF", "#E85D04", "#FFD400", "#0F766E", "#000000"])
def test_white_text_on_the_scrim_reads_over_a_white_image(brand):
    ts = generate_imagery(axes(), brand).tokens
    for mode, need in (("", 4.5), ("contrast:high", 7.0)):
        scrim = ts.resolve("imagery.scrim", mode)
        composite = _over(scrim[:7], int(scrim[7:], 16) / 255, "#FFFFFF")
        assert contrast("#FFFFFF", composite) >= need, (brand, mode)
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed


def test_the_scrim_is_the_least_that_reaches_the_minimum():
    base = scrim_base("#3366FF")
    a = scrim_alpha(base, 4.5)
    assert contrast("#FFFFFF", _over(base, a / 255, "#FFFFFF")) >= 4.5
    assert contrast("#FFFFFF", _over(base, (a - 1) / 255, "#FFFFFF")) < 4.5


def test_warmth_warms_the_duotone_and_strengthens_the_tint():
    cool_shadow, cool_light = duotone(axes(warmth=0.0), "#3366FF")
    warm_shadow, warm_light = duotone(axes(warmth=1.0), "#3366FF")
    assert cool_shadow == warm_shadow and cool_light != warm_light
    assert tint_alpha(axes(warmth=1.0)) > tint_alpha(axes(warmth=0.0))
    assert contrast(warm_shadow, warm_light) >= 7.0


def test_a_scrim_too_weak_is_named_with_the_fix():
    ts = generate_imagery(axes(), "#3366FF").tokens
    ts.get("imagery.shade.standard").value = "#070D1A20"
    check = next(c for c in CHECKS if c.id == "scrim-text")
    found = check.run(ts, "")
    assert len(found) == 1 and found[0].startswith(
        "imagery.on-scrim on imagery.scrim over a white image () is ")
    assert found[0].endswith("WCAG 1.4.3 needs 4.5:1, so point imagery.scrim at a stronger shade")


def test_media_is_rounded_by_the_roundness():
    sharp = build_system(axes(geometry=0.0, formality=1.0), "#3366FF").tokens
    soft = build_system(axes(geometry=1.0, formality=0.0), "#3366FF").tokens
    assert sharp.resolve("radius.media")["value"] < soft.resolve("radius.media")["value"]


def test_the_scrim_is_measured_against_the_worst_image_for_its_text():
    """Dark text on a light scrim is weakest over a black image, not a white one."""
    ts = generate_imagery(axes(), "#3366FF").tokens
    ts.get("imagery.shade.standard").value = "#FFFFFF20"
    ts.get("imagery.white").value = "#000000"
    check = next(c for c in CHECKS if c.id == "scrim-text")
    found = check.run(ts, "")
    assert len(found) == 1 and found[0].startswith(
        "imagery.on-scrim on imagery.scrim over a black image () is 1.28:1")


def test_the_scrim_alpha_reaches_the_minimum_over_both_images():
    base = scrim_base("#3366FF")
    for need in (4.5, 7.0):
        a = scrim_alpha(base, need)
        for image in ("#FFFFFF", "#000000"):
            assert contrast("#FFFFFF", _over(base, a / 255, image)) >= need


def test_text_between_the_two_composites_meets_a_grey_image_at_one_to_one():
    ts = generate_imagery(axes(), "#3366FF").tokens
    ts.get("imagery.white").value = "#404040"
    check = next(c for c in CHECKS if c.id == "scrim-text")
    assert check.run(ts, "")[0].startswith(
        "imagery.on-scrim on imagery.scrim over a grey image () is 1.00:1")


def _grey(hx):
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return max(r, g, b) - min(r, g, b) <= 1


@pytest.mark.parametrize("brand", ["#000000", "#808080", "#FFFFFF"])
def test_a_grey_brand_gets_a_neutral_scrim_and_highlight(brand):
    """A grey brand has no hue (hex_to_oklch reads 0 degrees), so its scrim
    and, at the middle warmth, its duotone highlight stay grey."""
    assert _grey(scrim_base(brand))
    shadow, highlight = duotone(axes(), brand)
    assert _grey(shadow) and _grey(highlight)


def test_near_greys_get_the_same_scrim_and_highlight():
    """#7F8080 reads 197 degrees, #80807F 106 and #807F80 326, at a chroma
    of about 0.002: they must not turn cyan, olive or magenta."""
    from engine.foundations.color_math import oklab_distance
    for warmth in (0.0, 0.5, 1.0):
        looks = [(scrim_base(b),) + duotone(axes(warmth=warmth), b)
                 for b in ("#808080", "#7F8080", "#80807F", "#807F80")]
        for i in range(3):
            assert max(oklab_distance(looks[0][i], other[i]) for other in looks[1:]) <= 0.006


def test_the_scrim_and_highlight_keep_the_hue_of_a_colorful_brand():
    from engine.foundations.color_math import hex_to_oklch
    assert scrim_base("#3366FF") == "#070D1A"
    assert abs(hex_to_oklch(duotone(axes(), "#3366FF")[1])[2] - hex_to_oklch("#3366FF")[2]) < 3


@pytest.mark.parametrize("brand_hue", [30.0, 60.0, 144.0, 265.0])
def test_the_highlight_turns_warm_or_cool_without_crossing_a_third_hue(brand_hue):
    from engine.foundations import character
    from engine.foundations.color_math import hex_to_oklch, oklch_to_hex
    brand = oklch_to_hex(0.55, 0.12, brand_hue)
    for warmth, anchor in ((0.0, character.COOL_HUE), (1.0, character.WARM_HUE)):
        hue = hex_to_oklch(duotone(axes(warmth=warmth), brand)[1])[2]
        assert abs(character.hue_delta(anchor, hue)) <= 40.0, (brand, warmth, hue)
