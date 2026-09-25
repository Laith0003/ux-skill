"""What every foundation hands the build: a generator plus the checks the
gate runs on its tokens.

A generator is a pure function of the seven axes and the brand inputs. It
returns tokens and notes and never gates itself; build_system validates
and gates every foundation once, then asks each foundation's hint hook for
advice on the findings it owns.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.gate import Check, GateFinding, Pairing
from engine.foundations.tokens import TokenSet
from engine.synthesizer.axes import AxisValues


@dataclass(frozen=True)
class BrandInputs:
    """Brand inputs a generator may read besides the axes."""
    brand_hex: str
    arabic: bool = True
    # "fill", "accent" or "edge" when the brief names the brand's role;
    # None lets the axes choose (character.brand_role).
    brand_role: Optional[str] = None


@dataclass
class Generated:
    """A generator's output: its tokens and the notes on every retune."""
    tokens: TokenSet
    notes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Foundation:
    """One foundation as the build sees it. `name` is also the first path
    segment of every token it generates; the hint hook sees only findings
    whose foreground token starts with that segment."""
    name: str
    generate: Callable[[AxisValues, BrandInputs], Generated]
    pairings: Tuple[Pairing, ...] = ()
    checks: Tuple[Check, ...] = ()
    hint: Optional[Callable[[TokenSet, GateFinding], str]] = None
    # Foundations whose primitives this one aliases (layout aliases space).
    requires: Tuple[str, ...] = ()
    # Role path -> the token type its checks read. A role of another type
    # passes validate; the build's role-types check reports it once and
    # this foundation's checks and pairings skip it.
    role_types: Mapping[str, str] = field(default_factory=dict, hash=False)


# An example value per type, for the role-types fix. Types left out (number,
# shadow) need none: a number is plain, a shadow too long to quote.
TYPE_EXAMPLES = {
    "color": "#3366FF",
    "strokeStyle": "solid",
    "dimension": "{value: 8, unit: px}",
    "duration": "{value: 200, unit: ms}",
    "cubicBezier": "[0.4, 0, 0.6, 1]",
}


def mistyped(ts: TokenSet, foundations: Sequence[Foundation]) -> List[str]:
    """Every declared role present with a type other than its role expects:
    the roles the role-types check reports and every other rule skips."""
    return [path for f in foundations for path, want in f.role_types.items()
            if ts.has(path) and ts.get(path).type != want]


def typed(ts: TokenSet, path: str, role_types: Mapping[str, str]) -> bool:
    """True when `path` exists with the type its role expects; the typed
    accessor foundation checks read through, so a mistyped role is skipped."""
    return ts.has(path) and ts.get(path).type == role_types[path]


def role_types_check(foundations: Sequence[Foundation]) -> Check:
    """One check over every role the given foundations declare: each role
    whose token has another type is reported once, naming the token, its
    type, the expected type and the fix."""
    expected = {path: want for f in foundations for path, want in f.role_types.items()}

    def run(ts: TokenSet, mode: str) -> List[str]:
        out = []
        for path, want in expected.items():
            if ts.has(path) and ts.get(path).type != want:
                example = TYPE_EXAMPLES.get(want)
                out.append(f"{path} is a {ts.get(path).type} but its role expects a {want}; "
                           f"point it at a {want} token"
                           + (f", for example {example}" if example else ""))
        return out

    return Check("role-types", "system", run)
