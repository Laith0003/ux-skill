"""Structural validation for a TokenSet. Every problem names the token and the fix."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from engine.foundations.tokens import AliasError, TokenSet, alias_target, is_alias


@dataclass(frozen=True)
class Problem:
    token: str
    rule: str
    message: str


def validate(ts: TokenSet) -> List[Problem]:
    out: List[Problem] = []
    for t in ts.tokens():
        if t.layer == "primitive":
            if is_alias(t.value):
                out.append(Problem(t.path, "primitive-alias",
                    f"{t.path} is a primitive but aliases {t.value}; give it a literal value"))
            if t.modes:
                out.append(Problem(t.path, "primitive-modes",
                    f"{t.path} is a primitive with modes {sorted(t.modes)}; move mode values to a semantic role"))
            continue
        for mode in t.modes:
            if mode not in ts.mode_names:
                out.append(Problem(t.path, "unknown-mode",
                    f"{t.path} sets mode '{mode}', which is not one of {list(ts.mode_names)}; "
                    "remove it or add the mode to the TokenSet's mode_names"))
        for mode in ts.mode_names:
            raw = ts.raw(t.path, mode)
            if not is_alias(raw):
                out.append(Problem(t.path, "semantic-literal",
                    f"{t.path} ({mode}) holds {raw}; alias a primitive instead"))
                break
            target = alias_target(raw)
            if not ts.has(target):
                out.append(Problem(t.path, "alias-missing",
                    f"{t.path} ({mode}) aliases {target}, which is not defined; add it or point at an existing primitive"))
                break
            if ts.get(target).layer == "semantic":
                out.append(Problem(t.path, "semantic-to-semantic",
                    f"{t.path} ({mode}) aliases the semantic {target}; alias its primitive directly"))
                break
            try:
                ts.resolve(t.path, mode)
            except AliasError as exc:
                out.append(Problem(t.path, "alias-cycle", str(exc)))
                break
    return out
