"""Component contracts: what each component is made of, which semantic
roles it binds, the states and variants it supports, the copy rules per
state, its accessibility minimums and where it came from.

Contracts are YAML files read by yamlite, a strict standard-library reader
for the subset they use. schema checks a contract on its own; bind checks
it against a built token set.
"""
from engine.contracts.bind import EDGE_ROLES, binding_problems, pairings_of, validate_contracts
from engine.contracts.schema import (
    CATEGORIES, PROMOTION, PROPERTY_TYPES, RTL_BEHAVIORS, STATES, STATUSES, A11y, Binding,
    Contract, ContractError, ContractProblem, ContrastRule, Part, Provenance, Variant,
    contract_problems, load_contract, promotion_problems, read_contract)
from engine.contracts.yamlite import YamlError, loads

__all__ = [
    "A11y", "Binding", "CATEGORIES", "Contract", "ContractError", "ContractProblem",
    "ContrastRule", "EDGE_ROLES", "PROMOTION", "PROPERTY_TYPES", "Part", "Provenance",
    "RTL_BEHAVIORS", "STATES", "STATUSES", "Variant", "YamlError", "binding_problems",
    "contract_problems", "load_contract", "loads", "pairings_of", "promotion_problems",
    "read_contract", "validate_contracts",
]
