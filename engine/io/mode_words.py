"""Mode names to the engine's axes, one rule for every importer.

A mode name names an axis value only as a whole word: Dark, Dark mode,
darkMode and dark-hex name dark; Darkness, Highlight and Lightness name
nothing. Contrast and motion share the word standard, and high or reduced
alone is as often a density or a size, so those two axes are read only
where their own name is written too: in a mode's name (High contrast,
Reduced motion) or in the context around it (a Contrast collection, a
column header).
"""
from __future__ import annotations

import re
from typing import Iterable, Optional, Sequence, Set, Tuple

from engine.foundations.modes import AXES

# Axes whose value words are read only beside the axis's own name.
NEEDS_AXIS_WORD = ("contrast", "motion")
_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def words(text: str) -> Set[str]:
    """The whole words of a name, lowercase, split at camelCase and at
    anything that is not a letter or a digit."""
    return set(re.findall(r"[a-z0-9]+", _CAMEL.sub(" ", text).lower()))


def axis_of(names: Sequence[str], context: Iterable[str] = ()) -> Optional[Tuple[str, int]]:
    """(axis, index of the base name) when `names` name an axis: two names
    that are its two values (Light and Dark), each name holding one value
    and not the other, or one name that is its non-base value (Dark mode),
    for which the index is -1. None when they name no axis. Contrast and
    motion need their name in a mode name or in `context`."""
    sets = [words(n) for n in names]
    around: Set[str] = set().union(*sets) if sets else set()
    for text in context:
        around |= words(text)
    for axis, (base, other) in AXES.items():
        if axis in NEEDS_AXIS_WORD and axis not in around:
            continue
        if len(sets) == 1:
            if other in sets[0] and base not in sets[0]:
                return axis, -1
            continue
        if len(sets) != 2:
            continue
        a, b = sets
        if base in a and other not in a and other in b and base not in b:
            return axis, 0
        if other in a and base not in a and base in b and other not in b:
            return axis, 1
    return None
