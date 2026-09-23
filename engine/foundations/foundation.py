"""What every foundation hands the build: a generator plus the checks the
gate runs on its tokens.

A generator is a pure function of the seven axes and the brand inputs. It
returns tokens and notes and never gates itself; build_system validates
and gates every foundation once, then asks each foundation's hint hook for
advice on the findings it owns.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple

from engine.foundations.gate import Check, GateFinding, Pairing
from engine.foundations.tokens import TokenSet
from engine.synthesizer.axes import AxisValues


@dataclass(frozen=True)
class BrandInputs:
    """Brand inputs a generator may read besides the axes."""
    brand_hex: str
    arabic: bool = True


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
