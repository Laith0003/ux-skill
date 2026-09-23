"""The foundations engine's internal schema.

A TokenSet holds primitives (literal values, no modes) and semantics
(aliases to primitives, optionally overridden per mode). Generators write
into a TokenSet; the validator, the WCAG gate and the exporters read it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


class AliasError(ValueError):
    """An alias points at a missing token or loops back on itself.

    `cause` is "missing" or "cycle", so callers can branch on it without
    parsing the message.
    """

    def __init__(self, message: str, cause: str):
        super().__init__(message)
        self.cause = cause


def is_alias(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("{") and value.endswith("}")


def alias_target(value: str) -> str:
    return value[1:-1]


def css_property(path: str) -> str:
    """The CSS custom property a token path becomes. validate uses it to
    reject two paths that would share one property; to_css uses it to emit."""
    return "--" + path.replace(".", "-")


@dataclass
class Token:
    path: str
    type: str
    value: Any
    modes: Dict[str, Any] = field(default_factory=dict)
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

    def _lookup(self, path: str) -> Token:
        if path not in self._tokens:
            raise KeyError(f"{path} is not defined; add it or check the spelling")
        return self._tokens[path]

    def get(self, path: str) -> Token:
        return self._lookup(path)

    def has(self, path: str) -> bool:
        return path in self._tokens

    def tokens(self) -> List[Token]:
        return list(self._tokens.values())

    def raw(self, path: str, mode: str) -> Any:
        if mode not in self.mode_names:
            raise ValueError(
                f"mode {mode!r} is not one of {list(self.mode_names)}; "
                "use one of these or add it to mode_names")
        tok = self._lookup(path)
        return tok.modes.get(mode, tok.value)

    def resolve(self, path: str, mode: str) -> Any:
        """The literal a token has in one mode. Aliases are followed, and a
        composite value (a shadow, a typography style) comes back with its
        aliased fields resolved too."""
        return self._resolve(path, mode, ())

    def _resolve(self, path: str, mode: str, outer: Tuple[str, ...]) -> Any:
        if path not in self._tokens:
            raise AliasError(f"{path} is not defined; add it before resolving", "missing")
        seen: List[str] = []
        current = path
        while True:
            if current in seen or current in outer:
                chain = " -> ".join(list(outer) + seen + [current])
                raise AliasError(
                    f"{path} alias cycle: {chain}; "
                    "point one of these at a literal value or a primitive",
                    "cycle",
                )
            seen.append(current)
            if current not in self._tokens:
                holder = seen[-2] if len(seen) > 1 else path
                raise AliasError(
                    f"{holder} aliases {current}, which is not defined "
                    f"(resolving {path}). Define {current} or point {holder} "
                    "at an existing token.",
                    "missing",
                )
            value = self.raw(current, mode)
            if not is_alias(value):
                return self._deep(value, mode, outer + tuple(seen))
            current = alias_target(value)

    def _deep(self, value: Any, mode: str, outer: Tuple[str, ...]) -> Any:
        if isinstance(value, dict):
            return {k: self._deep(v, mode, outer) for k, v in value.items()}
        if isinstance(value, list):
            return [self._deep(v, mode, outer) for v in value]
        if is_alias(value):
            return self._resolve(alias_target(value), mode, outer)
        return value
