"""The foundations engine's internal schema.

A TokenSet holds primitives (literal values, no modes) and semantics
(aliases to primitives, optionally overridden per mode). Generators write
into a TokenSet; the validator, the WCAG gate and the exporters read it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


class AliasError(ValueError):
    """An alias points at a missing token or loops back on itself."""


def is_alias(value: str) -> bool:
    return isinstance(value, str) and value.startswith("{") and value.endswith("}")


def alias_target(value: str) -> str:
    return value[1:-1]


@dataclass
class Token:
    path: str
    type: str
    value: str
    modes: Dict[str, str] = field(default_factory=dict)
    layer: str = "primitive"
    description: str = ""


class TokenSet:
    def __init__(self, mode_names: Tuple[str, ...] = ("light", "dark")):
        if not mode_names:
            raise ValueError(
                "TokenSet needs at least one mode name; pass mode_names=(\"light\",) or more."
            )
        self.mode_names = mode_names
        self._tokens: Dict[str, Token] = {}

    def add(self, token: Token) -> None:
        if token.path in self._tokens:
            raise ValueError(f"{token.path} is already defined; token paths must be unique")
        self._tokens[token.path] = token

    def get(self, path: str) -> Token:
        return self._tokens[path]

    def has(self, path: str) -> bool:
        return path in self._tokens

    def tokens(self) -> List[Token]:
        return list(self._tokens.values())

    def raw(self, path: str, mode: str) -> str:
        if mode not in self.mode_names:
            raise ValueError(f"mode {mode!r} is not one of {list(self.mode_names)}")
        tok = self._tokens[path]
        return tok.modes.get(mode, tok.value)

    def resolve(self, path: str, mode: str) -> str:
        if path not in self._tokens:
            raise AliasError(f"{path} is not defined; add it before resolving")
        seen: List[str] = []
        current = path
        while True:
            if current in seen:
                chain = " -> ".join(seen + [current])
                raise AliasError(
                    f"{path} alias cycle: {chain}; "
                    "point one of these at a literal value or a primitive"
                )
            seen.append(current)
            if current not in self._tokens:
                holder = seen[-2] if len(seen) > 1 else path
                raise AliasError(
                    f"{holder} aliases {current}, which is not defined "
                    f"(resolving {path}). Define {current} or point {holder} "
                    "at an existing token."
                )
            value = self.raw(current, mode)
            if not is_alias(value):
                return value
            current = alias_target(value)
