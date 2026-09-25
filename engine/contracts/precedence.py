"""Which binding applies when a component's states and variants meet.

Every contract resolves its bindings in one order. First the disabled
rule: a disabled component takes no hover, pressed or focus binding;
selected and error still apply, and where disabled and another state bind
the same part and property, disabled wins. Then the specificity rule: a
binding for a state beats one without a state, and one with more variant
conditions beats one with fewer. Two other states still left on one part
and property are ranked by the contract's own line that starts
TWO_STATE_OPENING.

A contract with a disabled state says the first rule word for word in
usage.do (DISABLED_RULE), and one whose bindings can meet by conditions
says the second (SPECIFICITY_RULE), so an agent reading one contract has
the whole rule.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Tuple

from engine.contracts.schema import Binding, Contract

# The states a disabled component takes no binding for.
DISABLED_SUPPRESSES: Tuple[str, ...] = ("hover", "pressed", "focus")
DISABLED_RULE = ("Apply the disabled rule before the others; a disabled component takes no "
                 "hover, pressed or focus binding, selected and error still apply, and where "
                 "disabled and another state bind the same part and property, disabled wins")
SPECIFICITY_RULE = ("Apply the binding for a state over the one without a state, and the one "
                    "with more variant conditions over the one with fewer")
SPECIFICITY_OPENING = "Apply the binding for a state"
TWO_STATE_OPENING = "When two states apply at once"


def live_states(states: Iterable[str]) -> Tuple[str, ...]:
    """The states whose bindings can apply, after the disabled rule."""
    states = tuple(states)
    if "disabled" not in states:
        return states
    return tuple(s for s in states if s not in DISABLED_SUPPRESSES)


def can_meet(a: str, b: str) -> bool:
    """Whether two states can apply at once under the disabled rule."""
    return not ({a, b} & {"disabled"} and {a, b} & set(DISABLED_SUPPRESSES))


def resolve(contract: Contract, variant: Mapping[str, str],
            states: Iterable[str]) -> Dict[Tuple[str, str], Tuple[Binding, ...]]:
    """For each part and property some binding sets, the bindings that win
    for this variant choice (a variant left out takes its default) and
    these states. One binding wins unless two other states are left, which
    the contract's own two-state line ranks."""
    chosen = {v.name: variant.get(v.name, v.default) for v in contract.variants}
    live = set(live_states(states))
    groups: Dict[Tuple[str, str], List[Binding]] = {}
    for b in contract.tokens:
        if all(chosen.get(k) == v for k, v in b.when) and (b.state is None or b.state in live):
            groups.setdefault((b.part, b.property), []).append(b)
    out: Dict[Tuple[str, str], Tuple[Binding, ...]] = {}
    for key, group in groups.items():
        disabled = [b for b in group if b.state == "disabled"]
        stated = [b for b in group if b.state]
        pool = disabled or stated or group
        most = max(len(b.when) for b in pool)
        out[key] = tuple(b for b in pool if len(b.when) == most)
    return out
