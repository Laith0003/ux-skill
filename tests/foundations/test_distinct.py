"""Distinctness: systems built from opposite characters, and the four site
trial briefs, are measurably different."""
import itertools
import json
from pathlib import Path

import pytest

from engine.foundations import build_system
from engine.foundations.distinct import NAMED, SPAN, character_of, distance
from engine.foundations.emit import brief_audience, choose_axes, resolve_arabic
from engine.synthesizer.axes import AXIS_NAMES, AxisValues

BRIEFS = Path(__file__).resolve().parent / "briefs"
# The four site trials and their brand colors.
TRIALS = {"clinic": "#0F766E", "devtool": "#6D28D9", "restaurant": "#E85D04",
          "fintech-ar": "#2563EB"}
# Our floors: opposite corners of the axes differ in at least this share of
# what a person sees, the site trials in at least this share, and moving
# any one axis end to end changes at least this share.
CORNER_FLOOR, TRIAL_FLOOR, AXIS_FLOOR = 0.35, 0.15, 0.05


def _built(name, brand):
    brief = json.loads((BRIEFS / f"{name}.json").read_text(encoding="utf-8"))
    axes, _ = choose_axes(brief, None)
    audience = brief_audience(brief)
    return character_of(build_system(axes, brand, arabic=resolve_arabic(False, audience),
                                     audience=audience).tokens)


def test_identical_systems_are_zero_apart_and_features_are_complete():
    a = character_of(build_system(AxisValues(*[0.5] * 7), "#3366FF").tokens)
    assert distance(a, a) == 0.0
    assert set(a) == set(SPAN) | set(NAMED)


def test_opposite_corners_of_the_axes_are_far_apart():
    found = []
    for bits in itertools.product((0.0, 1.0), repeat=6):
        low = AxisValues(0.0, *bits)
        high = AxisValues(1.0, *[1.0 - b for b in bits])
        d = distance(character_of(build_system(low, "#3366FF").tokens),
                     character_of(build_system(high, "#3366FF").tokens))
        found.append(d)
    assert min(found) >= CORNER_FLOOR, min(found)


@pytest.mark.parametrize("axis", AXIS_NAMES)
def test_every_axis_alone_moves_the_system(axis):
    def build(v):
        values = dict(zip(AXIS_NAMES, [0.5] * 7), **{axis: v})
        return character_of(build_system(AxisValues(**values), "#3366FF").tokens)
    assert distance(build(0.0), build(1.0)) >= AXIS_FLOOR


@pytest.mark.parametrize("brand_of", ["own", "same"])
def test_the_four_site_trials_build_pairwise_distinct_systems(brand_of):
    chars = {name: _built(name, brand if brand_of == "own" else "#3366FF")
             for name, brand in TRIALS.items()}
    for x, y in itertools.combinations(chars, 2):
        assert distance(chars[x], chars[y]) >= TRIAL_FLOOR, (x, y)
    faces = {chars[n]["face.display"] for n in chars}
    assert len(faces) == 4
