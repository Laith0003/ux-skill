"""Foundations engine (ux-skill 4.0): schema-first design-system compiler."""
from engine.foundations.color import PAIRINGS, SEMANTIC, Pairing, generate_color
from engine.foundations.export import build_color, from_dtcg, to_css, to_dtcg
from engine.foundations.gate import GateFailure, GateReport, gate
from engine.foundations.tokens import AliasError, Token, TokenSet, alias_target, is_alias
from engine.foundations.validate import Problem, validate

__all__ = [
    "AliasError", "GateFailure", "GateReport", "PAIRINGS", "Pairing", "Problem", "SEMANTIC",
    "Token", "TokenSet", "alias_target", "build_color", "from_dtcg", "gate", "generate_color",
    "is_alias", "to_css", "to_dtcg", "validate",
]
