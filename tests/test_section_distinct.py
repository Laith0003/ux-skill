"""One section contract built under five corners of the axes stays above
the glance floor, read on what that section shows: a section built from
a contract still looks like its brand."""
import itertools

import pytest

from engine.contracts.library import seed_contracts, seed_sections
from engine.foundations import build_system
from engine.foundations.distinct import GLANCE_FLOOR, character_of, distance, features_shown
from engine.synthesizer.axes import AxisValues

CORNERS = (AxisValues(0, 0, 0, 0, 0, 0, 0), AxisValues(1, 1, 1, 1, 1, 1, 1),
           AxisValues(1, 0, 1, 0, 1, 0, 1), AxisValues(0, 1, 0, 1, 0, 1, 0),
           AxisValues(0.5, 1, 0, 0, 1, 1, 0.5))
SECTIONS = {c.name: c for c in seed_sections()}
COMPONENTS = {c.name: c for c in seed_contracts()}


def _shown(section):
    """The roles a section shows: its own bindings and those of the
    component contracts its slots take."""
    roles = {b.role for b in section.tokens}
    for slot in section.section.slots:
        for name in slot.takes:
            if name in COMPONENTS:
                roles |= {b.role for b in COMPONENTS[name].tokens if b.state is None}
    return roles
CHARACTERS = [character_of(build_system(a, "#808080").tokens) for a in CORNERS]


# The hero carries the brand's first look; a section of neutral text and
# space (pricing, a stats band, the closing band) reads closer across briefs.
@pytest.mark.parametrize("name", ["hero", "secondary-hero"])
def test_a_section_under_five_corners_stays_above_the_glance_floor(name):
    keys = features_shown(_shown(SECTIONS[name]))
    assert keys, name
    worst = min(distance(a, b, keys) for a, b in itertools.combinations(CHARACTERS, 2))
    assert worst >= GLANCE_FLOOR, (name, keys, worst)


def test_the_restricted_distance_names_an_empty_selection():
    with pytest.raises(ValueError, match="keys"):
        distance(CHARACTERS[0], CHARACTERS[1], ())
