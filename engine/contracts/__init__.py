"""Component contracts: what each component is made of, which semantic
roles it binds, the states and variants it supports, the copy rules per
state, its accessibility minimums and where it came from.

Contracts are YAML files read by yamlite, a strict standard-library reader
for the subset they use.
"""
from engine.contracts.yamlite import YamlError, loads

__all__ = ["YamlError", "loads"]
