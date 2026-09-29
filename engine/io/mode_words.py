"""Mode names to the engine's axes, one rule for every importer.

A mode name names an axis value only as a whole word: Dark, Dark mode,
darkMode and dark-hex name dark; Darkness, Highlight and Lightness name
nothing. Contrast and motion share the word standard, and high or reduced
alone is as often a density or a size, so those two axes are read only
where their own name is written too: in a mode's name (High contrast,
Reduced motion) or in the context around it (a Contrast collection, a
column header).

A base word (default, base, value, standard) names no axis alone, but
opposite a non-base value it is that axis's base: Default and Dark are the
scheme axis, Default the light one. The words the CSS media queries use,
reduce and more, read as reduced and high.

The engine's own mode names, as its Figma export writes them, are read
apart (engine_axes): each name is one lowercase axis value per word, the
same axis at each position, every combination present and the default
the base of each (light standard, light high, dark standard, dark high).
Those name their axes exactly, so they need no axis word, with one guard:
a collection whose only axis is contrast or motion (standard and high)
reads on it only when its own name or the context names the axis or a
foundation that varies on it (border, imagery), since standard and high
alone are as often a density.
"""
from __future__ import annotations

import re
from typing import Iterable, List, Optional, Sequence, Set, Tuple

from engine.foundations.modes import AXES, FOUNDATION_AXES

# Axes whose value words are read only beside the axis's own name.
NEEDS_AXIS_WORD = ("contrast", "motion")
# Words that name the base of whichever axis the other name places.
BASE_WORDS = frozenset(("default", "base", "value", "standard"))
# Words other tools write for an axis value, and the value they mean.
_SYNONYMS = {"reduce": "reduced", "more": "high"}
_BASES = frozenset(values[0] for values in AXES.values())
_OTHERS = frozenset(values[1] for values in AXES.values())
_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def words(text: str) -> Set[str]:
    """The whole words of a name, lowercase, split at camelCase and at
    anything that is not a letter or a digit."""
    return set(re.findall(r"[a-z0-9]+", _CAMEL.sub(" ", text).lower()))


def _values(text: str) -> Set[str]:
    """The words of a name with the synonyms read as the values they mean."""
    found = words(text)
    return found | {_SYNONYMS[w] for w in found if w in _SYNONYMS}


def axis_of(names: Sequence[str], context: Iterable[str] = ()) -> Optional[Tuple[str, int]]:
    """(axis, index of the base name) when `names` name an axis: two names
    that are its two values (Light and Dark), a base word opposite its
    non-base value (Default and Dark), each name holding one value and not
    the other, or one name that is its non-base value (Dark mode), for
    which the index is -1. None when they name no axis. Contrast and
    motion need their name in a mode name or in `context`."""
    sets = [_values(n) for n in names]
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

        def based(s: Set[str]) -> bool:
            return other not in s and (base in s or bool(s & BASE_WORDS))

        def other_of(s: Set[str]) -> bool:
            return other in s and base not in s
        if based(a) and other_of(b):
            return axis, 0
        if other_of(a) and based(b):
            return axis, 1
    return None


def mode_of(name: str, context: Iterable[str] = ()) -> Optional[str]:
    """The axis whose non-base value `name` names on its own (Dark is
    scheme, High contrast is contrast), or None."""
    hit = axis_of([name], context)
    return hit[0] if hit is not None and hit[1] == -1 else None


def axes_named(name: str, context: Iterable[str] = ()) -> Tuple[str, ...]:
    """Every axis whose non-base value `name` names on its own, in the
    engine's axis order: High contrast dark names scheme and contrast. A
    mode that names two is a combined mode, which no one axis holds."""
    found = _values(name)
    around = set(found)
    for text in context:
        around |= words(text)
    return tuple(axis for axis, (base, other) in AXES.items()
                 if (axis not in NEEDS_AXIS_WORD or axis in around)
                 and other in found and base not in found)


def is_base(name: str) -> bool:
    """True when `name` is a base: an axis's base value (Light, LTR) or a
    base word (Default, Value), and no non-base value beside it."""
    found = _values(name)
    return not found & _OTHERS and bool(found & (_BASES | BASE_WORDS))


def engine_axes(names: Sequence[str], default: str,
                context: Iterable[str] = ()) -> Optional[List[str]]:
    """The axis each word position names when `names` are the engine's own
    mode names with `default` the base of every axis (see the module
    docstring), else None."""
    split = [n.split(" ") for n in names]
    width = len(default.split(" "))
    if len(names) < 2 or default not in names or any(len(w) != width for w in split) \
            or len(names) != 2 ** width or len({tuple(w) for w in split}) != len(names):
        return None
    axes: List[str] = []
    for i in range(width):
        seen = {w[i] for w in split}
        axis = next((a for a, values in AXES.items() if set(values) == seen), None)
        if axis is None or axis in axes or default.split(" ")[i] != AXES[axis][0]:
            return None
        axes.append(axis)
    if all(a in NEEDS_AXIS_WORD for a in axes):
        around: Set[str] = set()
        for text in context:
            around |= words(text)
        varies = {a for root in around for a in FOUNDATION_AXES.get(root, ())}
        if not all(a in around or a in varies for a in axes):
            return None
    return axes
