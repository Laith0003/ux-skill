"""Check contracts against a built token set.

Every role a contract names exists, is semantic and has the type its use
needs. A container whose fill measures below EDGE_FLOOR against a surface
it sits on, in any color context, declares an edge (border-width at
border.outline or heavier, and a border color) for that fill. The floor is
ours: WCAG sets no minimum for the edge of a container. Every contrast pairing the contract
declares is measured in every scheme and contrast context through the
same gate the build uses. validate_contracts adds the checks across a set
of contracts: unique names, and a deprecated contract's replacement exists
and is not deprecated itself.
"""
from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple

from engine.contracts.schema import CRITERIA, PROPERTY_TYPES, Binding, Contract, ContractProblem
from engine.foundations.color_math import contrast
from engine.foundations.gate import OPAQUE_PAIRING, Pairing, cite, gate
from engine.foundations.modes import contexts
from engine.foundations.tokens import AliasError, TokenSet, opaque_hex

# Border-width roles heavy enough to draw a container's edge.
EDGE_ROLES: Tuple[str, ...] = ("border.outline", "border.emphasis", "border.active")
# Our floor for telling a container's fill from the surface under it. A fill
# that measures below it against a surface, in any color context, draws an
# edge there. WCAG sets no minimum for a container's edge, so this is ours.
EDGE_FLOOR = 1.2


def _problem(contract: Contract, rule: str, message: str) -> ContractProblem:
    return ContractProblem(contract.name, rule, f"{contract.name}: {message}")


def _role_problem(contract: Contract, ts: TokenSet, role: str, want: str,
                  where: str) -> Optional[ContractProblem]:
    if not ts.has(role):
        return _problem(contract, "unknown-role",
                        f"{where} binds {role}, which the token set does not define; bind an "
                        "existing semantic role, or add the role to the system first")
    token = ts.get(role)
    if token.layer != "semantic":
        return _problem(contract, "primitive-role",
                        f"{where} binds {role}, a primitive; components bind semantic roles "
                        "only, so bind the role that aliases it")
    if token.type != want:
        return _problem(contract, "role-type",
                        f"{where} binds {role}, a {token.type}, but it needs a {want}; bind a "
                        f"{want} role")
    return None


def _color_contexts(ts: TokenSet) -> List[str]:
    return contexts([a for a in ("scheme", "contrast") if a in ts.axes], ts.axes)


def _covers(edge: Binding, fill: Binding) -> bool:
    """True when `edge` applies wherever `fill` does."""
    return edge.part == fill.part and set(edge.when) <= set(fill.when) \
        and (edge.state is None or edge.state == fill.state)


def _opaque(ts: TokenSet, role: str, mode: str) -> Optional[str]:
    """The role's color in `mode` as #RRGGBB, or None when it is translucent
    or not a hex color (the gate reports those for pairings)."""
    value = opaque_hex(ts.resolve(role, mode))
    if isinstance(value, str) and len(value) == 7 and value.startswith("#"):
        return value
    return None


def _edge_problems(contract: Contract, ts: TokenSet) -> List[ContractProblem]:
    out: List[ContractProblem] = []
    for fill in (b for b in contract.tokens if b.property == "fill"):
        if not (ts.has(fill.role) and ts.get(fill.role).type == "color"):
            continue
        width = any(_covers(e, fill) and e.property == "border-width" and e.role in EDGE_ROLES
                    for e in contract.tokens)
        color = any(_covers(e, fill) and e.property == "border-color" for e in contract.tokens)
        if width and color:
            continue
        worst: Optional[Tuple[float, str, str]] = None
        for surface in contract.surfaces:
            if not (ts.has(surface) and ts.get(surface).type == "color"):
                continue
            for mode in _color_contexts(ts):
                a, b = _opaque(ts, fill.role, mode), _opaque(ts, surface, mode)
                if a is None or b is None:
                    continue
                ratio = contrast(a, b)
                if ratio < EDGE_FLOOR and (worst is None or ratio < worst[0]):
                    worst = (ratio, surface, mode)
        if worst is not None:
            ratio, surface, mode = worst
            out.append(_problem(
                contract, "container-edge",
                f"{fill.label()} is {fill.role}, which measures {int(ratio * 100) / 100:.2f}:1 "
                f"against {surface} in {mode}, below our container edge floor of "
                f"{EDGE_FLOOR:g}:1 (WCAG sets no minimum for a container's edge), so the "
                f"{fill.part} has no visible edge there; bind border-width to border.outline "
                f"and a border-color on {fill.part} for the same variant and state"))
    return out


def _pairings(contract: Contract) -> List[Pairing]:
    out: List[Pairing] = []
    for rule in contract.contrast:
        criterion = rule.criterion if rule.criterion in CRITERIA \
            else f"the {contract.name} contract"
        bgs = contract.surfaces if rule.bg == "surfaces" else (rule.bg,)
        out += [Pairing(rule.fg, bg, rule.minimum, criterion, rule.high) for bg in bgs]
    return out


def _contrast_problems(contract: Contract, ts: TokenSet) -> List[ContractProblem]:
    pairings = [p for p in _pairings(contract)
                if all(ts.has(r) and ts.get(r).type == "color" for r in (p.fg, p.bg))]
    report = gate(ts, pairings, raise_on_fail=False)
    out = []
    for f in report.findings:
        ratio = int(f.ratio * 100) / 100
        out.append(_problem(contract, "contrast",
                            f"{f.fg} on {f.bg} ({f.mode}) is {ratio:.2f}:1; "
                            f"{cite(f.minimum, f.criterion)}. Bind a role with more contrast "
                            f"against {f.bg}, or build the system again with a different brand "
                            "color"))
    out += [_problem(contract, "contrast", c.message) for c in report.failures
            if c.check == OPAQUE_PAIRING]
    return out


def binding_problems(contract: Contract, ts: TokenSet) -> List[ContractProblem]:
    """Every problem binding one contract to a built token set."""
    out: List[ContractProblem] = []
    for b in contract.tokens:
        p = _role_problem(contract, ts, b.role, PROPERTY_TYPES[b.property], b.label())
        if p:
            out.append(p)
    for s in contract.surfaces:
        p = _role_problem(contract, ts, s, "color", "surfaces")
        if p:
            out.append(p)
    for rule in contract.contrast:
        for role in (rule.fg,) + (() if rule.bg == "surfaces" else (rule.bg,)):
            p = _role_problem(contract, ts, role, "color", "contrast")
            if p and p.message not in {o.message for o in out}:
                out.append(p)
    if contract.a11y.target != "none":
        p = _role_problem(contract, ts, contract.a11y.target, "dimension", "a11y.target")
        if p and p.message not in {o.message for o in out}:
            out.append(p)
    if out:
        return out
    try:
        return _edge_problems(contract, ts) + _contrast_problems(contract, ts)
    except AliasError as exc:
        return [_problem(contract, "unresolved", f"a role it binds cannot be resolved ({exc}); "
                                                 "run validate on the token set and fix it")]


def validate_contracts(contracts: Sequence[Contract],
                       ts: Optional[TokenSet] = None) -> List[ContractProblem]:
    """Checks across a set of contracts, then each contract's bindings when
    a token set is given."""
    out: List[ContractProblem] = []
    by_name = {}
    for c in contracts:
        if c.name in by_name:
            out.append(_problem(c, "duplicate-contract",
                                f"two contracts are named {c.name}; rename one"))
        by_name.setdefault(c.name, c)
    for c in contracts:
        if c.status != "deprecated":
            continue
        target = by_name.get(c.replacement or "")
        if target is None:
            out.append(_problem(c, "replacement",
                                f"replacement is {c.replacement}, which is not in this set of "
                                "contracts; name a contract that exists"))
        elif target.status == "deprecated":
            out.append(_problem(c, "replacement",
                                f"replacement {target.name} is deprecated too; name a contract "
                                "people can move to"))
    if ts is not None:
        for c in contracts:
            out += binding_problems(c, ts)
    return out


def pairings_of(contracts: Iterable[Contract]) -> List[Tuple[str, Pairing]]:
    """(contract name, pairing) for every pairing the contracts declare,
    the surfaces shorthand expanded."""
    return [(c.name, p) for c in contracts for p in _pairings(c)]
