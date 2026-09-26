"""The foundations engine's internal schema.

A TokenSet holds primitives (literal values, no modes) and semantics
(aliases to primitives, optionally overridden per mode). Generators write
into a TokenSet; the validator, the WCAG gate and the exporters read it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Tuple

from engine.foundations.modes import AXES, ModeError, join, parse, select

_AXIS_NAME = re.compile(r"[a-z][a-z0-9-]*")


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


def opaque_hex(value: Any) -> Any:
    """#RRGGBBFF is opaque: hold it as #RRGGBB, so an opaque color never
    reads as translucent. Anything else comes back unchanged."""
    if isinstance(value, str) and len(value) == 9 and value.startswith("#") \
            and value[7:].upper() == "FF":
        return value[:7]
    return value


def _opaque_layers(value: Any) -> Any:
    """A shadow value with each layer's opaque #RRGGBBFF color shortened."""
    if isinstance(value, dict) and "color" in value:
        return dict(value, color=opaque_hex(value["color"]))
    if isinstance(value, list):
        return [_opaque_layers(v) if isinstance(v, dict) else v for v in value]
    return value


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
    # What an importer keeps beside the value so a write-back gives the
    # file's own form back: "original" (context -> the value as written)
    # and "read_as" (context -> the value it was read as), for a color
    # mapped into sRGB. Empty for every token the engine builds.
    extensions: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        norm = {"color": opaque_hex, "shadow": _opaque_layers}.get(self.type)
        if norm is not None:
            self.value = norm(self.value)
            self.modes = {m: norm(v) for m, v in self.modes.items()}


class TokenSet:
    """Tokens in insertion order, plus the mode axes their overrides use
    (see modes.py). A context is a key such as "scheme:dark,contrast:high";
    "" is the all-base context."""

    def __init__(self, axes: Mapping[str, Tuple[str, ...]] = AXES):
        for name, values in axes.items():
            if len(values) != 2:
                raise ValueError(
                    f"axis {name!r} has values {list(values)}; a mode axis has exactly two "
                    "values, the base first; split a third value into its own axis")
            if not _AXIS_NAME.fullmatch(name) or len(set(values)) != len(values) \
                    or not all(isinstance(v, str) and _AXIS_NAME.fullmatch(v) for v in values):
                raise ValueError(
                    f"axis {name!r} with values {list(values)} is not usable; name axes and values "
                    "with lowercase letters, digits and '-', and give each axis two distinct "
                    "values, the base first")
        self.axes: Mapping[str, Tuple[str, ...]] = MappingProxyType(
            {name: tuple(values) for name, values in axes.items()})
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

    def raw(self, path: str, mode: str = "") -> Any:
        """The value a token holds in one context, before following aliases.
        Raises ModeError for a context that does not parse, or when two of
        the token's overrides tie in it with different values."""
        tok = self._lookup(path)
        value, tied = select(tok.value, tok.modes, mode, self.axes)
        if tied:
            raise ModeError(
                f"{path} has overrides {tied} that all apply in {mode!r} with different "
                f"values; add an override for {join(parse(mode, self.axes), self.axes)!r} "
                "or make them agree")
        return value

    def resolve(self, path: str, mode: str = "") -> Any:
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
