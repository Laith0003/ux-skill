"""Component contracts: what each component is made of, which semantic
roles it binds, the states and variants it supports, the copy rules per
state, its accessibility minimums and where it came from.

Contracts are YAML files read by yamlite, a strict standard-library reader
for the subset they use. schema checks a contract on its own.
"""
from engine.contracts.schema import (
    CATEGORIES, PROMOTION, PROPERTY_TYPES, RTL_BEHAVIORS, STATES, STATUSES, A11y, Binding,
    Contract, ContractError, ContractProblem, ContrastRule, Part, Provenance, Variant,
    contract_problems, load_contract, promotion_problems, read_contract)
from engine.contracts.yamlite import YamlError, loads

__all__ = [
    "A11y", "Binding", "CATEGORIES", "Contract", "ContractError", "ContractProblem",
    "ContrastRule", "PROMOTION", "PROPERTY_TYPES", "Part", "Provenance", "RTL_BEHAVIORS",
    "STATES", "STATUSES", "Variant", "YamlError", "contract_problems", "load_contract", "loads",
    "promotion_problems", "read_contract",
]
