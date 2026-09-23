"""Validation for a TokenSet: structure, values per type and path hygiene.
Every problem names the token and the fix."""
from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Dict, List, Mapping

from engine.foundations.tokens import (
    AliasError, Token, TokenSet, alias_target, css_property, is_alias)

LAYERS = ("primitive", "semantic")

_HEX_COLOR = re.compile(r"#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})")
_SEGMENT = re.compile(r"[A-Za-z0-9_-]+")


@dataclass(frozen=True)
class ValueRule:
    """How one token type's literal values are checked: `check` says whether
    a value is acceptable, `expected` is the fix quoted when it is not."""
    check: Callable[[Any], bool]
    expected: str


def _is_hex_color(value: Any) -> bool:
    return isinstance(value, str) and _HEX_COLOR.fullmatch(value) is not None


# One entry per known token type. M2 adds dimension, duration, shadow and
# font types here; nothing else in validate changes.
VALUE_RULES: Mapping[str, ValueRule] = MappingProxyType({
    "color": ValueRule(_is_hex_color, "use #RRGGBB or #RGB, for example #3366FF"),
})


@dataclass(frozen=True)
class Problem:
    token: str
    rule: str
    message: str


def _check_values(t: Token) -> List[Problem]:
    rule = VALUE_RULES.get(t.type)
    if rule is None:
        return [Problem(t.path, "unknown-type",
            f"{t.path} has type {t.type!r}; use one of {sorted(VALUE_RULES)}")]
    out: List[Problem] = []
    checked: List[Any] = []  # a list, not a set: a bad value may be unhashable
    for where, raw in [("", t.value)] + [(f" ({m})", v) for m, v in t.modes.items()]:
        # An alias is not a literal; its target is checked as a token itself.
        if is_alias(raw) or raw in checked:
            continue
        checked.append(raw)
        if not rule.check(raw):
            out.append(Problem(t.path, "bad-value",
                f"{t.path}{where} is type {t.type} but holds {raw!r}; {rule.expected}"))
    return out


def _check_paths(ts: TokenSet) -> List[Problem]:
    """Path hygiene: segment charset (bad-name), a token that is also a
    group of another token (path-conflict, which DTCG cannot hold), and two
    paths that become one CSS property (css-collision)."""
    out: List[Problem] = []
    paths = [t.path for t in ts.tokens()]
    defined = set(paths)
    props: Dict[str, str] = {}
    for path in paths:
        segments = path.split(".")
        for seg in segments:
            if not _SEGMENT.fullmatch(seg):
                out.append(Problem(path, "bad-name",
                    f"{path} has segment {seg!r}; path segments may use only letters, "
                    "digits, '_' and '-', so rename it"))
        for i in range(1, len(segments)):
            prefix = ".".join(segments[:i])
            if prefix in defined:
                out.append(Problem(path, "path-conflict",
                    f"{prefix} is a token and also a group holding {path}; DTCG cannot "
                    "hold both, so rename one"))
        prop = css_property(path)
        if prop in props:
            out.append(Problem(path, "css-collision",
                f"{props[prop]} and {path} both become the CSS property {prop}; "
                "rename one so each token keeps its own property"))
        else:
            props[prop] = path
    return out


def validate(ts: TokenSet) -> List[Problem]:
    out: List[Problem] = []
    for t in ts.tokens():
        out.extend(_check_values(t))
        if t.layer not in LAYERS:
            out.append(Problem(t.path, "unknown-layer",
                f"{t.path} has layer {t.layer!r}; use 'primitive' or 'semantic'"))
            continue
        if t.layer == "primitive":
            if is_alias(t.value):
                out.append(Problem(t.path, "primitive-alias",
                    f"{t.path} is a primitive but aliases {t.value}; give it a literal value"))
            if t.modes:
                out.append(Problem(t.path, "primitive-modes",
                    f"{t.path} is a primitive with modes {sorted(t.modes)}; move mode values to a semantic role"))
            continue
        base = ts.mode_names[0]
        if base in t.modes:
            out.append(Problem(t.path, "base-mode-override",
                f"{t.path} overrides the base mode '{base}', whose value is the token's own "
                f"$value; move {t.modes[base]} into $value and remove the '{base}' override"))
        for mode in t.modes:
            if mode not in ts.mode_names:
                out.append(Problem(t.path, "unknown-mode",
                    f"{t.path} sets mode '{mode}', which is not one of {list(ts.mode_names)}; "
                    "remove it or add the mode to the TokenSet's mode_names"))
        seen_raws: List[Any] = []
        for mode in ts.mode_names:
            raw = ts.raw(t.path, mode)
            if raw in seen_raws:
                # Same raw value already checked under an earlier mode for
                # this token (for example, no per-mode override at all); do
                # not report the same problem twice for one token.
                continue
            seen_raws.append(raw)
            if not is_alias(raw):
                out.append(Problem(t.path, "semantic-literal",
                    f"{t.path} ({mode}) holds {raw}; alias a primitive instead"))
                continue
            target = alias_target(raw)
            if not ts.has(target):
                out.append(Problem(t.path, "alias-missing",
                    f"{t.path} ({mode}) aliases {target}, which is not defined; add it or point at an existing primitive"))
                continue
            if ts.get(target).layer == "semantic":
                out.append(Problem(t.path, "semantic-to-semantic",
                    f"{t.path} ({mode}) aliases the semantic {target}; alias its primitive directly"))
                continue
            try:
                ts.resolve(t.path, mode)
            except AliasError as exc:
                rule = "alias-cycle" if exc.cause == "cycle" else "alias-missing"
                out.append(Problem(t.path, rule, str(exc)))
                continue
    out.extend(_check_paths(ts))
    return out
