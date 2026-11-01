"""Validation for a TokenSet: structure, values per type and path hygiene.
Every problem names the token and the fix.

Literal values are checked against values.TYPES (one entry per token
type). A semantic token holds an alias to a primitive of its own type, or,
for typography only, a composite whose every field aliases a primitive of
that field's type. Primitives hold literals only, composites included."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from engine.foundations.modes import (
    FOUNDATION_AXES, ModeError, contexts, join, parse, select, sparse)
from engine.foundations.tokens import AliasError, Token, TokenSet, alias_target, is_alias
from engine.foundations.values import TYPES, TYPOGRAPHY_FIELDS, css_names

LAYERS = ("primitive", "semantic")

_SEGMENT = re.compile(r"[A-Za-z0-9_-]+")

# Left and right swap under dir="rtl" and top and bottom depend on the
# writing mode, so directional tokens use the logical words (inline-start,
# inline-end, block-start, block-end). The ban covers every use of the four
# words; a path that means something else by one (a top bar, a z-order top)
# is renamed (app-bar, order.front) rather than allowed.
_PHYSICAL = {"left": "inline-start", "right": "inline-end", "top": "block-start",
             "bottom": "block-end"}
# Words inside a segment: split on '-', '_' and a lower-to-upper case change.
_WORD_BREAK = re.compile(r"[-_]|(?<=[a-z0-9])(?=[A-Z])")


@dataclass(frozen=True)
class Problem:
    token: str
    rule: str
    message: str


def _leaves(value: Any) -> List[Any]:
    if isinstance(value, dict):
        return [leaf for v in value.values() for leaf in _leaves(v)]
    if isinstance(value, list):
        return [leaf for v in value for leaf in _leaves(v)]
    return [value]


def _check_values(t: Token) -> List[Problem]:
    spec = TYPES.get(t.type)
    if spec is None:
        return [Problem(t.path, "unknown-type",
            f"{t.path} has type {t.type!r}; use one of {sorted(TYPES)}")]
    out: List[Problem] = []
    checked: List[Any] = []  # a list, not a set: a bad value may be unhashable
    for where, raw in [("", t.value)] + [(f" ({m})", v) for m, v in t.modes.items()]:
        # An alias is not a literal; its target is checked as a token itself.
        if is_alias(raw) or raw in checked:
            continue
        checked.append(raw)
        if not spec.check(raw):
            out.append(Problem(t.path, "bad-value",
                f"{t.path}{where} is type {t.type} but holds {raw!r}; {spec.expected}"))
    return out


def _check_paths(ts: TokenSet) -> List[Problem]:
    """Path hygiene: segment charset (bad-name), a physical side word in a
    segment (physical-direction), a token that is also a
    group of another token (path-conflict, which DTCG cannot hold), and two
    tokens that print the same CSS property (css-collision)."""
    out: List[Problem] = []
    paths = [t.path for t in ts.tokens()]
    defined = set(paths)
    props: Dict[str, str] = {}
    for t in ts.tokens():
        path = t.path
        segments = path.split(".")
        for seg in segments:
            if not _SEGMENT.fullmatch(seg):
                out.append(Problem(path, "bad-name",
                    f"{path} has segment {seg!r}; path segments may use only letters, "
                    "digits, '_' and '-', so rename it"))
            for word in (w.lower() for w in _WORD_BREAK.split(seg)):
                if word in _PHYSICAL:
                    out.append(Problem(path, "physical-direction",
                        f"{path} names the physical side '{word}'; left and right swap under "
                        f"dir=\"rtl\" and top and bottom depend on the writing mode, so token "
                        f"paths use logical names: use '{_PHYSICAL[word]}' instead"))
        for i in range(1, len(segments)):
            prefix = ".".join(segments[:i])
            if prefix in defined:
                out.append(Problem(path, "path-conflict",
                    f"{prefix} is a token and also a group holding {path}; DTCG cannot "
                    "hold both, so rename one"))
        for prop in css_names(path, t.type):
            if prop in props and props[prop] != path:
                out.append(Problem(path, "css-collision",
                    f"{props[prop]} and {path} both become the CSS property {prop}; "
                    "rename one so each token keeps its own property"))
                break
            props[prop] = path
    return out


def _check_alias(ts: TokenSet, t: Token, mode: str, raw: str, expected: str,
                 where: str = "") -> List[Problem]:
    """One alias held by semantic t (whole value, or one composite field
    when `where` names it): the target exists, is a primitive, and has the
    type the holder expects."""
    target = alias_target(raw)
    label = f"{t.path} ({mode or 'base'}){where}"
    if not ts.has(target):
        return [Problem(t.path, "alias-missing",
            f"{label} aliases {target}, which is not defined; add it or point at an existing primitive")]
    tt = ts.get(target)
    if tt.layer == "semantic":
        return [Problem(t.path, "semantic-to-semantic",
            f"{label} aliases the semantic {target}; alias its primitive directly")]
    if tt.type != expected:
        return [Problem(t.path, "alias-type",
            f"{label} aliases {target}, a {tt.type} token, but needs a {expected} token; "
            f"point it at a {expected} primitive")]
    return []


def _check_mode_keys(ts: TokenSet, t: Token, out: List[Problem]) -> Optional[List[str]]:
    """Check a semantic token's override keys; return the axes they use,
    or None when a key does not parse (the token's contexts are unknown)."""
    used: List[str] = []
    allowed = FOUNDATION_AXES.get(t.path.split(".", 1)[0])
    first_key: Dict[str, str] = {}
    for key in t.modes:
        try:
            pairs = parse(key, ts.axes)
        except ModeError as exc:
            out.append(Problem(t.path, "unknown-mode", f"{t.path}: {exc}"))
            return None
        context = join(pairs, ts.axes)
        if context in first_key:
            out.append(Problem(t.path, "duplicate-mode-key",
                f"{t.path} has override keys {first_key[context]!r} and {key!r}, which name the "
                f"same context {context!r}; keep one of them"))
        else:
            first_key[context] = key
        for axis, value in pairs.items():
            if value == ts.axes[axis][0]:
                out.append(Problem(t.path, "base-mode-override",
                    f"{t.path} override {key!r} sets {axis} to its base '{value}', whose value "
                    f"is the token's own $value; drop '{axis}:{value}' from the key, or move "
                    "that value into $value"))
            if allowed is not None and axis not in allowed:
                out.append(Problem(t.path, "axis-not-allowed",
                    f"{t.path} varies on {axis}, but {t.path.split('.', 1)[0]} tokens vary only "
                    f"on {list(allowed) or 'no axis'}; remove the {key!r} override"))
            if axis not in used:
                used.append(axis)
    return [a for a in ts.axes if a in used]


def validate(ts: TokenSet) -> List[Problem]:
    out: List[Problem] = []
    for t in ts.tokens():
        out.extend(_check_values(t))
        if t.layer not in LAYERS:
            out.append(Problem(t.path, "unknown-layer",
                f"{t.path} has layer {t.layer!r}; use 'primitive' or 'semantic'"))
            continue
        if t.layer == "primitive":
            if any(is_alias(leaf) for leaf in _leaves(t.value)):
                out.append(Problem(t.path, "primitive-alias",
                    f"{t.path} is a primitive but aliases {t.value}; give it a literal value"))
            if t.modes:
                out.append(Problem(t.path, "primitive-modes",
                    f"{t.path} is a primitive with modes {sorted(t.modes)}; move mode values to a semantic role"))
            continue
        token_axes = _check_mode_keys(ts, t, out)
        if token_axes is None:
            continue
        seen_raws: List[Any] = []
        for mode in contexts(token_axes, ts.axes):
            value, tied = select(t.value, t.modes, mode, ts.axes)
            # Keys naming one context that tie are duplicate-mode-key,
            # already reported; check the first key's value and skip the
            # resolve below, which would raise on the tie.
            duplicate_tie = len({join(parse(k, ts.axes), ts.axes) for k in tied}) == 1
            if tied and not duplicate_tie:
                out.append(Problem(t.path, "mode-ambiguous",
                    f"{t.path} has overrides {tied} that all apply in {mode} with different "
                    f"values; add an override for {sparse(mode, ts.axes)!r} or make them agree"))
                continue
            raw = value
            if raw in seen_raws:
                # Same raw value already checked in an earlier context for
                # this token; do not report the same problem twice.
                continue
            seen_raws.append(raw)
            if is_alias(raw):
                found = _check_alias(ts, t, mode, raw, t.type)
            elif t.type == "typography" and isinstance(raw, dict) and set(raw) == set(TYPOGRAPHY_FIELDS):
                found = []
                for key, (field_type, _) in TYPOGRAPHY_FIELDS.items():
                    if is_alias(raw[key]):
                        found += _check_alias(ts, t, mode, raw[key], field_type, f" field {key}")
                    else:
                        found.append(Problem(t.path, "semantic-literal",
                            f"{t.path} ({mode or 'base'}) field {key} holds {raw[key]!r}; alias a "
                            f"{field_type} primitive instead"))
            else:
                found = [Problem(t.path, "semantic-literal",
                    f"{t.path} ({mode or 'base'}) holds {raw!r}; alias a primitive instead")]
            if found:
                out.extend(found)
                continue
            if duplicate_tie:
                continue
            try:
                ts.resolve(t.path, mode)
            except AliasError as exc:
                rule = "alias-cycle" if exc.cause == "cycle" else "alias-missing"
                out.append(Problem(t.path, rule, str(exc)))
    out.extend(_check_paths(ts))
    return out
