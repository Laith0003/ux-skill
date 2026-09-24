"""Named mode axes.

A system varies along independent axes. Each axis has two values and the
first is its base. A context names one value per axis, written as a key:
"scheme:dark,contrast:high". Axes a key leaves out sit at their base, so
"" is the all-base context, and a bare value that belongs to exactly one
axis ("dark", "rtl") is shorthand for that pair.

A token stores its base value in `value` and one override per non-base
combination it needs in `modes`, keyed sparse (base values left out):
{"scheme:dark": ..., "contrast:high": ..., "scheme:dark,contrast:high": ...}.
In a context the override whose pairs all hold and that names the most
axes wins; two different values tied for most axes is a mode-ambiguous
problem, never a silent pick.
"""
from __future__ import annotations

import itertools
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Sequence, Tuple

AXES: Mapping[str, Tuple[str, ...]] = MappingProxyType({
    "scheme": ("light", "dark"),
    "contrast": ("standard", "high"),
    "density": ("comfortable", "compact"),
    "direction": ("ltr", "rtl"),
    "motion": ("standard", "reduced"),
})

# The axes a foundation's tokens may vary on, keyed by the first path
# segment. A root not listed here (an imported set) may use any axis.
FOUNDATION_AXES: Mapping[str, Tuple[str, ...]] = MappingProxyType({
    "color": ("scheme", "contrast"),
    "elevation": ("scheme",),
    "space": ("density",),
    "layout": ("density",),
    "type": ("direction",),
    "motion": ("motion", "direction"),
    "radius": (),
    "border": (),
})

# How each axis reaches CSS: the root attribute that sets it, and the media
# feature that sets its non-base value when the attribute is absent.
CSS_AXES: Mapping[str, Tuple[str, str]] = MappingProxyType({
    "scheme": ("data-theme", "(prefers-color-scheme: dark)"),
    "contrast": ("data-contrast", "(prefers-contrast: more)"),
    "density": ("data-density", ""),
    "direction": ("dir", ""),
    "motion": ("data-motion", "(prefers-reduced-motion: reduce)"),
})


class ModeError(ValueError):
    """A context or override key that does not parse against the axes."""


def parse(key: str, axes: Mapping[str, Tuple[str, ...]] = AXES) -> Dict[str, str]:
    """A key as {axis: value}, base values kept if written. Raises ModeError
    naming the bad part and the fix."""
    if not isinstance(key, str):
        raise ModeError(f"mode key {key!r} is not a string; write it like 'scheme:dark'")
    out: Dict[str, str] = {}
    for part in (p.strip() for p in key.split(",")) if key.strip() else []:
        if ":" in part:
            axis, _, value = part.partition(":")
        else:
            owners = [a for a, values in axes.items() if part in values]
            if len(owners) != 1:
                what = ("not a value of any axis" if not owners
                        else "a value of " + " and ".join(owners))
                raise ModeError(f"mode key {key!r}: {part!r} is {what}; write it as "
                                f"axis:value, one of {describe(axes)}")
            axis, value = owners[0], part
        if axis not in axes:
            raise ModeError(f"mode key {key!r} names axis {axis!r}; use one of {list(axes)}")
        if value not in axes[axis]:
            raise ModeError(f"mode key {key!r} sets {axis} to {value!r}; use one of "
                            f"{list(axes[axis])}")
        if axis in out and out[axis] != value:
            raise ModeError(f"mode key {key!r} sets {axis} twice; keep one value")
        out[axis] = value
    return out


def join(pairs: Mapping[str, str], axes: Mapping[str, Tuple[str, ...]] = AXES) -> str:
    """Canonical key: pairs in axis order."""
    return ",".join(f"{a}:{pairs[a]}" for a in axes if a in pairs)


def sparse(key: str, axes: Mapping[str, Tuple[str, ...]] = AXES) -> str:
    """The same context with base values left out: the form overrides use."""
    return join({a: v for a, v in parse(key, axes).items() if v != axes[a][0]}, axes)


def contexts(names: Sequence[str], axes: Mapping[str, Tuple[str, ...]] = AXES) -> List[str]:
    """Every explicit context over the named axes, base first, the first
    axis varying slowest: contexts(("scheme", "contrast")) gives
    scheme:light,contrast:standard, scheme:light,contrast:high,
    scheme:dark,contrast:standard, scheme:dark,contrast:high."""
    ordered = [a for a in axes if a in names]
    return [join(dict(zip(ordered, combo)), axes)
            for combo in itertools.product(*(axes[a] for a in ordered))]


def select(value: Any, modes: Mapping[str, Any], context: str,
           axes: Mapping[str, Tuple[str, ...]] = AXES) -> Tuple[Any, List[str]]:
    """The value a token has in `context`: its base `value`, or the override
    whose pairs all hold in the context and that names the most axes.
    Returns (value, tied) where tied lists the keys of overrides that tie
    for most axes with different values; callers treat a tie as an error."""
    active = {a: v for a, v in parse(context, axes).items() if v != axes[a][0]}
    best, best_n, tied = value, 0, []
    for key, override in modes.items():
        pairs = parse(key, axes)
        if any(active.get(a) != v for a, v in pairs.items()):
            continue
        if len(pairs) > best_n:
            best, best_n, tied = override, len(pairs), [key]
        elif len(pairs) == best_n and override != best:
            tied.append(key)
    return best, (tied if len(tied) > 1 else [])


def compress(values: Mapping[str, Any],
             axes: Mapping[str, Tuple[str, ...]] = AXES) -> Tuple[Any, Dict[str, Any]]:
    """Turn one value per explicit context into a base value plus the
    fewest sparse overrides that select() reads back exactly. `values` must
    hold every context over some set of axes (as contexts() lists them)."""
    ordered = sorted(values, key=lambda k: sum(
        1 for a, v in parse(k, axes).items() if v != axes[a][0]))
    base_key = ordered[0]
    base = values[base_key]
    modes: Dict[str, Any] = {}
    for key in ordered[1:]:
        inherited, tied = select(base, modes, key, axes)
        if tied or inherited != values[key]:
            modes[sparse(key, axes)] = values[key]
    return base, modes


def describe(axes: Mapping[str, Tuple[str, ...]] = AXES) -> str:
    return "; ".join(f"{a}: {', '.join(v)}" for a, v in axes.items())
