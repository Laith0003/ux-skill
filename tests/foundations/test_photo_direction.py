"""Photography: a page uses photographs to a direction the axes and the
brand set, every photo on a page shares one grade, the words for a search
come from the quantities, and a brand's bans narrow the kinds while only a
client system that forbids photography removes it."""
import pytest

from engine.foundations import build_system
from engine.foundations.emit import NEUTRAL, NEUTRAL_SOURCE, make_system
from engine.foundations.imagery import (
    PHOTO_KINDS, grade_problems, photo_direction, photo_lines)
from engine.synthesizer.axes import AxisValues


def axes(**kw):
    values = dict(zip(("warmth", "contrast", "density", "geometry", "formality", "motion",
                       "type_personality"), [0.5] * 7))
    values.update(kw)
    return AxisValues(**values)


def sweep(axis, attr, brand="#808080"):
    return [getattr(photo_direction(axes(**{axis: i / 10}), brand), attr) for i in range(11)]


@pytest.mark.parametrize("axis, attr, sign, least", [
    ("warmth", "temperature", 1, 12), ("contrast", "lightness", -1, 10),
    ("contrast", "contrast", 1, 12), ("motion", "chroma", 1, 5),
    ("contrast", "chroma", 1, 8), ("type_personality", "grain", 1, 0.3),
    ("motion", "energy", 1, 0.5), ("formality", "chroma", -1, 2)])
def test_each_quantity_moves_one_way_with_its_axis(axis, attr, sign, least):
    values = [sign * v for v in sweep(axis, attr)]
    assert values == sorted(values) and values[-1] - values[0] >= least, values


def test_formality_tightens_the_grade_lock():
    loose = photo_direction(axes(formality=0.0), "#808080").spread
    tight = photo_direction(axes(formality=1.0), "#808080").spread
    assert all(tight[k] < loose[k] for k in loose)


def test_a_warm_brand_leans_the_light_warm_and_a_grey_one_does_not():
    warm = photo_direction(axes(), "#E85D04").temperature
    cool = photo_direction(axes(), "#2563EB").temperature
    grey = photo_direction(axes(), "#808080").temperature
    assert warm > grey > cool


def test_the_look_comes_from_the_quantities_and_the_subject_from_the_fields():
    a = photo_direction(axes(), "#3366FF", product_type="software")
    b = photo_direction(axes(), "#3366FF", product_type="local-service")
    assert a.words == b.words and a.subject != b.subject
    older = photo_direction(axes(), "#3366FF", age="older-adults", primary_action="book")
    assert "people over 60" in older.subject and "the moment before the visit" in older.subject
    calm = photo_direction(axes(contrast=0.0, motion=0.0, formality=0.8), "#808080")
    loud = photo_direction(axes(contrast=1.0, motion=1.0, formality=0.0), "#808080")
    assert "soft, even light" in calm.words and "still and composed" in calm.words
    assert "vivid color" in loud.words and "dynamic, caught mid-motion" in loud.words


def test_a_ban_narrows_the_kinds_and_only_a_forbidding_system_removes_photos():
    banned = photo_direction(axes(), "#3366FF", bans=("staged lifestyle",))
    assert banned.allowed and "staged lifestyle" not in banned.kinds
    assert set(banned.kinds) == set(PHOTO_KINDS) - {"staged lifestyle"}
    forbidden = photo_direction(axes(), "#3366FF", forbidden=True)
    assert not forbidden.allowed
    assert photo_lines(forbidden) == [
        "The client's system forbids photography, so the pages carry none; imagery comes from "
        "generated art and the product itself."]


def test_the_grade_lock_passes_one_shoot_and_names_a_photo_from_another():
    d = photo_direction(axes(), "#808080")
    shoot = [(f"photo-{i}.jpg", d.lightness + i, d.temperature - i / 2, d.chroma + i / 2)
             for i in range(-2, 3)]
    assert grade_problems(shoot, d) == []
    mixed = shoot + [("stock-warm.jpg", d.lightness + 20, d.temperature + 14, d.chroma + 18)]
    msgs = grade_problems(mixed, d)
    assert any(m.startswith("stock-warm.jpg has temperature") for m in msgs)
    assert all("regrade" in m or "replace" in m for m in msgs)
    dark = [(n, L - 30, b, c) for n, L, b, c in shoot]
    assert grade_problems(dark, d)[0].startswith("the page's photos average lightness")


def test_the_direction_is_in_the_tokens_and_the_report():
    ts = build_system(axes(), "#3366FF").tokens
    d = photo_direction(axes(), "#3366FF")
    assert ts.resolve("imagery.photo.lightness") == d.lightness
    assert ts.resolve("imagery.photo.spread-temperature") == d.spread["temperature"]
    report = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE).report
    section = report.split("## Photography\n\n", 1)[1].split("\n## ", 1)[0]
    assert "- Grade lock: every photo within" in section and "- Search words: " in section
    none = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE, no_photography=True).report
    assert "forbids photography" in none
