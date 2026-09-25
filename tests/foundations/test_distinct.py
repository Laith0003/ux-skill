"""Distinctness: systems built from opposite characters, and the four site
trial briefs, look measurably different at a glance; what shows only in
use is measured apart; and every scale is the engine's real range."""
import functools
import itertools
import json
import math
from pathlib import Path

import pytest

from engine.foundations import build_system
from engine.foundations.audience import AGES, Audience
from engine.foundations.distinct import (
    BEHAVIOR, NAMED, REFERENCE_BRAND, SPAN, WEIGHTS, apart, behavior, character_of, distance)
from engine.foundations.emit import brief_audience, choose_axes, resolve_arabic
from engine.synthesizer.axes import AXIS_NAMES, AxisValues

from tests.foundations.trials import MID, TRIALS

BRIEFS = Path(__file__).resolve().parent / "briefs"
# Our floors, on the glance distance. Opposite corners of the axes differ
# in at least CORNER_FLOOR of what a person sees; the site trials in at
# least TRIAL_FLOOR, pairwise; moving any one axis but motion end to end
# changes at least AXIS_FLOOR. The motion axis shows only in use, so it is
# held to BEHAVIOR_FLOOR on the behavior score instead.
CORNER_FLOOR, TRIAL_FLOOR, AXIS_FLOOR, BEHAVIOR_FLOOR = 0.55, 0.15, 0.10, 0.30


def _built(name, brand):
    brief = json.loads((BRIEFS / f"{name}.json").read_text(encoding="utf-8"))
    axes, _ = choose_axes(brief, None)
    audience = brief_audience(brief)
    return character_of(build_system(axes, brand, arabic=resolve_arabic(False, audience),
                                     audience=audience).tokens)


@functools.lru_cache(maxsize=None)
def _corners():
    return {bits: character_of(build_system(AxisValues(*bits), REFERENCE_BRAND).tokens)
            for bits in itertools.product((0.0, 1.0), repeat=7)}


def _along(axis, v):
    return character_of(build_system(AxisValues(**dict(MID, **{axis: v})),
                                     REFERENCE_BRAND).tokens)


def test_identical_systems_are_zero_apart_and_features_are_complete():
    a = character_of(build_system(AxisValues(**MID), REFERENCE_BRAND).tokens)
    assert distance(a, a) == 0.0 and behavior(a, a) == 0.0
    assert set(a) == set(WEIGHTS) | set(BEHAVIOR)
    assert not set(WEIGHTS) & set(BEHAVIOR)
    assert set(SPAN) == set(a) - set(NAMED)


def test_what_shows_only_in_use_never_counts_at_a_glance():
    """Two systems that differ only in motion, the mono face and the ring
    width look the same on a first look: glance distance 0."""
    a = character_of(build_system(AxisValues(**MID), REFERENCE_BRAND).tokens)
    b = dict(a, **{"reveal.ms": a["reveal.ms"] + 150, "overshoot": a["overshoot"] + 0.8,
                   "ring.px": a["ring.px"] + 1, "face.mono": a["face.mono"] + " Other"})
    assert distance(a, b) == 0.0
    assert behavior(a, b) == 1.0


def test_every_span_is_the_widest_the_engine_goes():
    """SPAN is measured, not guessed: over the 128 corners of the axes each
    numeric feature spans at least 95 percent of its SPAN and never more.
    The body size moves with the audience's age, not the axes."""
    corners = list(_corners().values())
    for key, span in SPAN.items():
        if key == "body.px":
            continue
        widest = max((math.dist(a[key], b[key]) if isinstance(a[key], tuple)
                      else abs(a[key] - b[key])) for a, b in itertools.combinations(corners, 2))
        assert widest <= span <= widest / 0.95, (key, widest, span)
    sizes = [Audience(age=age).body_px for age in AGES]
    assert SPAN["body.px"] == max(sizes) - min(sizes)
    assert {c["body.px"] for c in corners} == {16}


def test_the_neutrals_and_status_colors_are_seen_at_their_real_range():
    """Warmth end to end moves the neutral tint across its whole range and
    the status hues across most of theirs, and the neutral tint weighs as
    much as the main button."""
    cool, warm = _along("warmth", 0.0), _along("warmth", 1.0)
    assert apart("neutral", cool["neutral"], warm["neutral"]) >= 0.9
    assert apart("status.hue", cool["status.hue"], warm["status.hue"]) >= 0.5
    low, high = _along("contrast", 0.0), _along("contrast", 1.0)
    assert apart("status.chroma", low["status.chroma"], high["status.chroma"]) >= 0.9
    assert WEIGHTS["neutral"] == WEIGHTS["button"] == max(WEIGHTS.values())


def test_opposite_corners_of_the_axes_are_far_apart():
    corners = _corners()
    found = [distance(corners[(0.0, *bits)], corners[(1.0, *[1.0 - b for b in bits])])
             for bits in itertools.product((0.0, 1.0), repeat=6)]
    assert min(found) >= CORNER_FLOOR, min(found)


@pytest.mark.parametrize("axis", [a for a in AXIS_NAMES if a != "motion"])
def test_every_axis_but_motion_moves_what_a_person_sees(axis):
    assert distance(_along(axis, 0.0), _along(axis, 1.0)) >= AXIS_FLOOR


def test_the_motion_axis_moves_what_shows_in_use():
    assert behavior(_along("motion", 0.0), _along("motion", 1.0)) >= BEHAVIOR_FLOOR


@pytest.mark.parametrize("brand_of", ["own", "same"])
def test_the_four_site_trials_build_pairwise_distinct_systems(brand_of):
    chars = {name: _built(name, brand if brand_of == "own" else REFERENCE_BRAND)
             for name, brand in TRIALS.items()}
    for x, y in itertools.combinations(chars, 2):
        assert distance(chars[x], chars[y]) >= TRIAL_FLOOR, (x, y)
    faces = {chars[n]["face.display"] for n in chars}
    assert len(faces) == 4
