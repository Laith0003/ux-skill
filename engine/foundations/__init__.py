"""Foundations engine (ux-skill 4.0): schema-first design-system compiler.

build_system is the entry point: generate every foundation, validate,
gate, and return the tokens with the gate report. build_color is its
color-only shortcut. generate_color is the low-level generator both wrap.

The gate and validate functions are exported as run_gate and run_validate
so the package attributes gate and validate stay the submodules.
"""
from engine.foundations.build import (
    FOUNDATIONS, BuildResult, ValidationError, build_color, build_system)
from engine.foundations.color import PAIRINGS, SEMANTIC, ColorResult, generate_color
from engine.foundations.export import dump_dtcg, from_dtcg, to_css, to_dtcg
from engine.foundations.foundation import BrandInputs, Foundation, Generated
from engine.foundations.gate import (
    Check, CheckFailure, GateFailure, GateFinding, GateReport, Pairing)
from engine.foundations.gate import gate as run_gate
from engine.foundations.tokens import AliasError, Token, TokenSet, alias_target, is_alias
from engine.foundations.validate import Problem
from engine.foundations.validate import validate as run_validate

__all__ = [
    "AliasError", "BrandInputs", "BuildResult", "Check", "CheckFailure", "ColorResult",
    "FOUNDATIONS", "Foundation", "GateFailure", "GateFinding", "GateReport", "Generated",
    "PAIRINGS", "Pairing", "Problem", "SEMANTIC", "Token", "TokenSet", "ValidationError",
    "alias_target", "build_color", "build_system", "dump_dtcg", "from_dtcg", "generate_color",
    "is_alias", "run_gate", "run_validate", "to_css", "to_dtcg",
]
