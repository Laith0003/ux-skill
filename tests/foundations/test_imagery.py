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
