"""Check contracts people write, the way the seed contracts are checked.

check_contracts() reads every *.yaml contract in a folder with the schema
checks the seeds pass (governance thresholds included), then binds them to
a system read in any format the engine imports (engine.io.read_any): every
role exists, is semantic and has the type its property needs, a container
that blends into its surface declares an edge, a control's fill clears the
surfaces it is placed on, and every declared pairing is measured in every
mode. The messages are the seeds' messages.

A system in its own names is checked through its mapping
(engine.io.adapter): a contract names the engine's roles, the mapping says
which of the system's tokens plays each, and each finding carries the
system's own name beside the role. A contract binds roles only; the system
is read as it is and never changed. A role the mapping keeps out of the
check (the owner's "not mapped" entry, a role deleted from the file, a
typography role with a field left out) is named as such, with the entry to
write, never as a role the system lacks.

bind_contracts() is the binding step on its own, for contracts already
read, so every command that binds contracts to a system gives the same
messages. Each problem keeps the seeds' wording in `problems`; `lines`
gives the same problems with the contract file named in place of the
contract.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from engine.contracts.bind import validate_contracts
from engine.contracts.library import load_folder
from engine.contracts.schema import Contract, ContractError, ContractProblem, load_contract
from engine.foundations.tokens import TokenSet

# How messages name a mapping passed as one already read.
MAPPING_NAME = "mapping.json"
NO_MAPPING = ("the system has none of the engine's roles under their own names and no mapping "
              "was given, so every role reads as missing; import it to write a mapping.json and "
              "check again with that mapping")
NOT_BOUND = ("the contracts were not bound to the system, since a contract could not be read; "
             "fix those first and check again")
_OR_BIND = "or bind a role the mapping maps"
_LEFT_OUT = ("left-out-role", "unchecked-role")


@dataclass
class ContractCheck:
    """The contracts read, every problem in the seeds' words, the same
    problems with the contract file named (`lines`), and notes on what the
    mapping left out of the check."""
    contracts: Tuple[Contract, ...] = ()
    problems: List[ContractProblem] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.problems


def _roles(contracts: Sequence[Contract]) -> Set[str]:
    """Every role the contracts name."""
    out: Set[str] = set()
    for c in contracts:
        out |= {b.role for b in c.tokens} | set(c.surfaces)
        out |= {r.fg for r in c.contrast} | {r.bg for r in c.contrast if r.bg != "surfaces"}
        if c.a11y.target != "none":
            out.add(c.a11y.target)
    return out


def _absent(ts: TokenSet, checked: TokenSet, mapping: Any, notes: Sequence[str], name: str,
            roles: Set[str]) -> Dict[str, Tuple[str, str]]:
    """Each role the contracts bind that the mapping keeps out of the
    checked set, with the rule and the reason its message gives."""
    from engine.io.adapter import ROLE_TYPES
    out: Dict[str, Tuple[str, str]] = {}
    for role in sorted(roles):
        if checked.has(role):
            continue
        m = mapping.roles.get(role)
        if m is not None and m.token is None:
            out[role] = ("left-out-role",
                         f"which the owner left out of the check in {name}; map {role} there to "
                         f"the token that plays it to check this binding, {_OR_BIND}")
        elif m is not None:
            note = next((n for n in notes if n.startswith(f"{role} ")), None)
            if note is not None:
                out[role] = ("unchecked-role",
                             f"which {name} maps but the check leaves out ({note}); fix that "
                             f"entry in {name} to check this binding, {_OR_BIND}")
        elif ts.has(role) and role in ROLE_TYPES:
            out[role] = ("left-out-role",
                         f"which the system has under the role's own name but {name} leaves "
                         f"out, so it is not checked; map it there to check this binding, "
                         f"{_OR_BIND}")
        elif ts.has(role):
            out[role] = ("unknown-role",
                         "which is a token of the system but not one of the engine's roles, so "
                         f"{name} cannot send it and the check does not read it; bind the "
                         "engine role it plays")
    return out


def bind_contracts(contracts: Sequence[Contract], tokens: TokenSet, mapping: Optional[Any] = None,
                   mapping_name: str = MAPPING_NAME) -> Tuple[List[ContractProblem], List[str]]:
    """Every problem binding `contracts` to the system `tokens`, read
    through `mapping` (an engine.io.adapter.Mapping) when one is given, and
    the notes on what the mapping left out. Raises InputError (from
    engine.io.adapter.view) for a mapping that names a token or mode the
    system lacks; `mapping_name` is the file its messages name."""
    if mapping is None:
        from engine.io.adapter import ROLE_TYPES
        notes = [] if any(tokens.has(r) for r in ROLE_TYPES) else [NO_MAPPING]
        return validate_contracts(contracts, tokens), notes
    from engine.io.adapter import their_names, view
    checked, notes = view(tokens, mapping, mapping_name)
    absent = _absent(tokens, checked, mapping, notes, mapping_name, _roles(contracts))
    # A role left out has no name of the system's to give.
    problems = [p if p.rule in _LEFT_OUT
                else dataclasses.replace(p, message=their_names(p.message, mapping))
                for p in validate_contracts(contracts, checked, absent)]
    return problems, notes


def _read(folder: Any) -> Tuple[Tuple[Contract, ...], List[ContractProblem], List[Optional[Path]],
                               Dict[str, Path]]:
    """The contracts in `folder` read one file at a time, as load_folder
    reads them, with the file each problem came from and each contract's
    file."""
    root = Path(folder)
    files = sorted(root.glob("*.yaml"))
    if not files:
        try:
            load_folder(root)
        except ContractError as exc:
            return (), list(exc.problems), [None] * len(exc.problems), {}
    contracts: List[Contract] = []
    problems: List[ContractProblem] = []
    where: List[Optional[Path]] = []
    named: Dict[str, Path] = {}
    for f in files:
        path = root / f.name
        try:
            c = load_contract(path)
        except ContractError as exc:
            problems += exc.problems
            where += [path] * len(exc.problems)
            continue
        contracts.append(c)
        named.setdefault(c.name, path)
    return tuple(contracts), problems, where, named


def _line(problem: ContractProblem, path: Optional[Path]) -> str:
    """The problem with its contract file named in place of the contract."""
    message = problem.message
    if path is None:
        return message
    head = f"{problem.contract}: "
    if message.startswith(head):
        return f"{path}: {message[len(head):]}"
    if message.startswith(path.name):
        return f"{path}{message[len(path.name):]}"
    return message


def check_contracts(folder: Any, source: Any, mapping: Optional[Any] = None, *,
                    fmt: str = "dtcg", label: str = "--from", mapping_name: Optional[str] = None,
                    **options: Any) -> ContractCheck:
    """Read the contracts in `folder` and bind them to the system in
    `source`: a file read with engine.io.read_any in the format `fmt` (one
    of engine.io.FORMATS; `options` go to its reader and `label` is the
    flag its errors name), or a system already read (an Imported or a
    TokenSet). `mapping` is an engine.io.adapter.Mapping or the path of a
    mapping.json; `mapping_name` is how messages name it (the path as
    given, or mapping.json). A contract that cannot be read stops the
    binding, with a note. Raises InputError for a source or mapping that
    cannot be read, naming the flag and the fix."""
    contracts, problems, where, named = _read(folder)
    if problems:
        notes = [NOT_BOUND] if contracts else []
        return ContractCheck((), problems, [_line(p, w) for p, w in zip(problems, where)],
                             notes)
    from engine.io import read_any
    from engine.io.adapter import Mapping, load_mapping
    from engine.io.report import Imported
    if isinstance(source, TokenSet):
        ts = source
    elif isinstance(source, Imported):
        ts = source.tokens
    else:
        ts = read_any(source, fmt, label, **options).tokens
    if mapping is not None and not isinstance(mapping, Mapping):
        mapping_name = mapping_name or str(mapping)
        mapping = load_mapping(mapping)
    found, notes = bind_contracts(contracts, ts, mapping, mapping_name or MAPPING_NAME)
    return ContractCheck(contracts, found, [_line(p, named.get(p.contract)) for p in found],
                         notes)
