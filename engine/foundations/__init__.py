"""Foundations engine (ux-skill 4.0): schema-first design-system compiler.

build_color is the entry point: generate, validate, gate, and return the
tokens with the gate report. generate_color is the low-level call that
build_color wraps; it skips the input checks, validate and the report.
"""
from engine.foundations.build import BuildResult, ValidationError, build_color
from engine.foundations.color import PAIRINGS, SEMANTIC, ColorResult, generate_color
from engine.foundations.export import dump_dtcg, from_dtcg, to_css, to_dtcg
from engine.foundations.gate import GateFailure, GateFinding, GateReport, Pairing, gate
from engine.foundations.tokens import AliasError, Token, TokenSet, alias_target, is_alias
from engine.foundations.validate import Problem, validate

__all__ = [
    "AliasError", "BuildResult", "ColorResult", "GateFailure", "GateFinding", "GateReport",
    "PAIRINGS", "Pairing", "Problem", "SEMANTIC", "Token", "TokenSet", "ValidationError",
    "alias_target", "build_color", "dump_dtcg", "from_dtcg", "gate", "generate_color", "is_alias",
    "to_css", "to_dtcg", "validate",
]
