"""Contract files on disk: a folder of *.yaml contracts, and the seed
contracts that ship with the engine (in seed/, all experimental)."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple, Union

from engine.contracts.schema import Contract, ContractError, ContractProblem, load_contract

SEED_DIR = Path(__file__).resolve().parent / "seed"


def load_folder(folder: Union[str, Path]) -> Tuple[Contract, ...]:
    """Every *.yaml contract in `folder`, sorted by file name. Raises
    ContractError listing every problem in every file, or naming the folder
    when it holds no contract."""
    root = Path(folder)
    files = sorted(root.glob("*.yaml"))
    if not files:
        raise ContractError([ContractProblem(root.name, "no-contracts",
                                             f"{root} holds no .yaml contract; pass the folder "
                                             "that holds the contract files")])
    contracts: List[Contract] = []
    problems: List[ContractProblem] = []
    for f in files:
        try:
            contracts.append(load_contract(f))
        except ContractError as exc:
            problems.extend(exc.problems)
    if problems:
        raise ContractError(problems)
    return tuple(contracts)


def seed_contracts() -> Tuple[Contract, ...]:
    """The seed contracts, sorted by name."""
    return load_folder(SEED_DIR)


def seed_sources() -> Dict[str, str]:
    """Each seed file's name and text, sorted by name, for copying as is."""
    return {f.name: f.read_text(encoding="utf-8") for f in sorted(SEED_DIR.glob("*.yaml"))}
