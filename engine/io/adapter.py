"""Naming adapters: an imported system keeps its own names end to end.

A mapping says which of the system's tokens plays each of the engine's
roles and which of its modes is each of the engine's axes. It is a JSON
file the owner edits (dump_mapping, load_mapping); propose() writes a first
one from names alone, marking each entry "by": "name" so the owner can see
what to confirm (an entry the owner writes says "by": "owner").

propose() maps a role only when a token's name is the role's own path
written with other separators (color.text.default, color-text-default,
color/text/default), and a typography role to the five field properties
the engine's CSS writes for it. It maps an axis only when its name or its
values say which one it is (light and dark, ltr and rtl, a .compact
class). Nothing else is guessed: the rest waits for the owner.

view() builds the set the engine checks: each mapped role under its own
path, holding the value its token resolves to in each of the engine's
contexts, so check_system(..., structure=False) can measure it.
their_names() writes findings back with the system's names beside the
roles.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from engine.foundations.build import FOUNDATIONS
from engine.foundations.errors import InputError
from engine.foundations.modes import AXES, ModeError, compress, contexts, join, parse
from engine.foundations.tokens import AliasError, Token, TokenSet
from engine.foundations.values import TYPOGRAPHY_FIELDS

# Every role a check or pairing reads, with the type it needs.
ROLE_TYPES: Dict[str, str] = {path: kind for f in FOUNDATIONS
                              for path, kind in f.role_types.items()}
VERSION = 1
BY = ("name", "owner")
_KEYS = ("version", "axes", "roles")
_ROLE_FIX = "{\"token\": \"<your token>\", \"by\": \"owner\"}"
# Words a theme selector or mode name uses for a non-base value of our axes.
_AXIS_WORDS: Dict[str, str] = {
    "dark": "scheme", "rtl": "direction", "compact": "density", "high": "contrast",
    "high-contrast": "contrast", "contrast-high": "contrast", "more": "contrast",
    "reduced": "motion", "reduce": "motion", "reduced-motion": "motion",
}
_BASE_WORDS = ("light", "ltr", "comfortable", "standard", "default", "base", "off",
               "no-preference")


@dataclass(frozen=True)
class RoleMap:
    """The token that plays a role, and who said so."""
    token: str
    by: str = "owner"


@dataclass(frozen=True)
class AxisMap:
    """The mode axis of the system that is one of ours: its name there, and
    our value -> its value."""
    source: str
    values: Dict[str, str] = field(hash=False)
    by: str = "owner"


@dataclass
class Mapping:
    roles: Dict[str, RoleMap] = field(default_factory=dict)
    axes: Dict[str, AxisMap] = field(default_factory=dict)


def _norm(name: str) -> str:
    return ".".join(p for p in re.split(r"[.\-/_ ]+", name.lower()) if p)


def _field_names(prefix: str) -> Dict[str, str]:
    """The five properties the engine's CSS writes for a typography role."""
    return {key: f"{prefix}-{css}" for key, (_, css) in TYPOGRAPHY_FIELDS.items()}


def _has_fields(ts: TokenSet, prefix: str) -> bool:
    return all(ts.has(p) for p in _field_names(prefix).values())


def propose(ts: TokenSet) -> Mapping:
    """A first mapping from names alone (see the module docstring)."""
    by_norm: Dict[str, str] = {}
    for t in ts.tokens():
        by_norm.setdefault(_norm(t.path), t.path)
    roles: Dict[str, RoleMap] = {}
    for role, kind in ROLE_TYPES.items():
        match = by_norm.get(_norm(role))
        if match is not None:
            roles[role] = RoleMap(match, "name")
        elif kind == "typography":
            prefix = role.replace(".", "-")
            if _has_fields(ts, prefix):
                roles[role] = RoleMap(prefix, "name")
    axes: Dict[str, AxisMap] = {}
    for name, (base, other) in ts.axes.items():
        ours = _our_axis(name, base, other)
        if ours is None or ours in axes:
            continue
        axes[ours] = AxisMap(name, {AXES[ours][0]: base, AXES[ours][1]: other}, "name")
    return Mapping(roles, axes)


def _our_axis(name: str, base: str, other: str) -> Optional[str]:
    if name in AXES and (base, other) == AXES[name]:
        return name
    if base not in _BASE_WORDS and not name.startswith(base + "-"):
        return None
    word = other
    if (base, other) == ("off", "on"):
        word = name.split("-", 1)[1] if "-" in name else name
    return _AXIS_WORDS.get(word)


# ---------------------------------------------------------------- file


def dump_mapping(mapping: Mapping) -> str:
    doc = {"version": VERSION,
           "axes": {a: {"from": m.source, "values": dict(m.values), "by": m.by}
                    for a, m in mapping.axes.items()},
           "roles": {r: {"token": m.token, "by": m.by} for r, m in mapping.roles.items()}}
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def parse_mapping(text: str, name: str) -> Mapping:
    """The mapping a file holds. Raises InputError naming the key and the
    fix."""
    try:
        doc = json.loads(text)
    except ValueError as exc:
        raise InputError(f"{name} is not valid JSON ({exc}); fix it, or remove it and import "
                         "again to get a new proposal") from None
    if not isinstance(doc, dict):
        raise InputError(f"{name} is not a JSON object; write {{\"version\": 1, \"axes\": {{}}, "
                         "\"roles\": {}}")
    extra = [k for k in doc if k not in _KEYS]
    if extra:
        raise InputError(f"{name} has the key {extra[0]}, which a mapping does not use; keep "
                         "only version, axes and roles")
    if "version" not in doc:
        raise InputError(f"{name} has no version; write \"version\": {VERSION}")
    if doc["version"] != VERSION:
        raise InputError(f"{name} has version {json.dumps(doc['version'])}; this engine reads "
                         f"version {VERSION}, so write \"version\": {VERSION}")
    for key, what in (("roles", f"role to {_ROLE_FIX}"),
                      ("axes", "axis to {\"from\": ..., \"values\": ..., \"by\": \"owner\"}")):
        if not isinstance(doc.get(key) or {}, dict):
            raise InputError(f"{name} {key} is {json.dumps(doc[key])}; write it as an object of "
                             f"{what}")
    roles: Dict[str, RoleMap] = {}
    for role, entry in (doc.get("roles") or {}).items():
        if role not in ROLE_TYPES:
            raise InputError(f"{name} maps {role}, which is not a role the engine checks; use "
                             "one of its roles, for example color.text.default")
        if not (isinstance(entry, dict) and isinstance(entry.get("token"), str)
                and entry["token"] and entry.get("by", "owner") in BY):
            raise InputError(f"{name} role {role} is {json.dumps(entry)}; write {_ROLE_FIX}")
        roles[role] = RoleMap(entry["token"], entry.get("by", "owner"))
    axes: Dict[str, AxisMap] = {}
    for axis, entry in (doc.get("axes") or {}).items():
        if axis not in AXES:
            raise InputError(f"{name} maps the axis {axis}, which is not one of the engine's "
                             "axes; use scheme, contrast, density, direction or motion")
        values = entry.get("values") if isinstance(entry, dict) else None
        if not (isinstance(entry, dict) and isinstance(entry.get("from"), str)
                and isinstance(values, dict) and set(values) == set(AXES[axis])
                and all(isinstance(v, str) for v in values.values())
                and entry.get("by", "owner") in BY):
            raise InputError(f"{name} axis {axis} is {json.dumps(entry)}; write {{\"from\": "
                             f"\"<your mode axis>\", \"values\": {{\"{AXES[axis][0]}\": \"...\", "
                             f"\"{AXES[axis][1]}\": \"...\"}}, \"by\": \"owner\"}}")
        axes[axis] = AxisMap(entry["from"], {v: values[v] for v in AXES[axis]},
                             entry.get("by", "owner"))
    return Mapping(roles, axes)


def load_mapping(path: Any, label: str = "--mapping") -> Mapping:
    p = Path(path).expanduser()
    try:
        text = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        reason = getattr(exc, "strerror", None) or "not UTF-8 text"
        raise InputError(f"{label} {p} cannot be read ({reason}); pass the mapping.json the "
                         "import wrote") from None
    return parse_mapping(text, str(p))


# ---------------------------------------------------------------- view


def _check(ts: TokenSet, mapping: Mapping) -> None:
    for role, m in mapping.roles.items():
        if not ts.has(m.token) and not (ROLE_TYPES[role] == "typography"
                                        and _has_fields(ts, m.token)):
            raise InputError(f"the mapping sends {role} to {m.token}, which the imported system "
                             "does not have; point it at one of its tokens, or remove the line")
    used: Dict[str, str] = {}
    for axis, m in mapping.axes.items():
        if m.source not in ts.axes:
            have = ", ".join(ts.axes) or "none"
            raise InputError(f"the mapping reads {axis} from the mode axis {m.source}, which the "
                             f"imported system does not have (it has {have}); fix the from "
                             "value, or remove the axis")
        if m.source in used:
            raise InputError(f"the mapping reads {used[m.source]} and {axis} both from "
                             f"{m.source}; read each of the engine's axes from a mode axis of "
                             "its own, or remove one")
        used[m.source] = axis
        theirs = ts.axes[m.source]
        for ours, value in m.values.items():
            if value not in theirs:
                raise InputError(f"the mapping reads {axis} {ours} from {m.source} {value}, but "
                                 f"{m.source} has the values {theirs[0]} and {theirs[1]}; use "
                                 "those")
        if len(set(m.values.values())) < len(m.values):
            base, other = AXES[axis]
            raise InputError(f"the mapping reads {axis} {base} and {other} both from "
                             f"{m.source} {m.values[base]}; read each from its own value")


def _identity(ts: TokenSet, mapping: Mapping) -> bool:
    return all(r == m.token for r, m in mapping.roles.items()) and all(
        a == m.source and m.values == {v: v for v in AXES[a]} for a, m in mapping.axes.items())


def _resolve(ts: TokenSet, role: str, token: str, context: str) -> Any:
    if ROLE_TYPES[role] == "typography" and not ts.has(token):
        return {key: ts.resolve(path, context) for key, path in _field_names(token).items()}
    return ts.resolve(token, context)


def view(ts: TokenSet, mapping: Mapping) -> Tuple[TokenSet, List[str]]:
    """The set the engine checks, in its own roles and axes, and notes on
    what it read differently or left out. A mapping that names every role
    and axis as the system already does gives the system itself. Raises
    InputError for a token or axis value the system lacks."""
    _check(ts, mapping)
    if _identity(ts, mapping) and set(ts.axes) <= set(AXES):
        return ts, []
    axes = {a: AXES[a] for a in AXES if a in mapping.axes}
    out = TokenSet(axes)
    notes: List[str] = []
    for role, m in mapping.roles.items():
        want = ROLE_TYPES[role]
        values: Dict[str, Any] = {}
        try:
            for ctx in contexts(list(axes), axes):
                theirs = {mapping.axes[a].source: mapping.axes[a].values[v]
                          for a, v in parse(ctx, axes).items()}
                their_ctx = join({a: v for a, v in theirs.items()
                                  if v != ts.axes[a][0]}, ts.axes)
                values[ctx] = _resolve(ts, role, m.token, their_ctx)
        except (AliasError, ModeError) as exc:
            notes.append(f"{role} reads {m.token}, which cannot be resolved ({exc}); it was left "
                         "out of the check")
            continue
        kind = want if want == "typography" and not ts.has(m.token) else ts.get(m.token).type
        if want == "fontWeight" and kind == "number" and all(
                isinstance(v, (int, float)) and not isinstance(v, bool) and 1 <= v <= 1000
                for v in values.values()):
            notes.append(f"{role} reads {m.token}, a number, as a fontWeight "
                         f"({values[next(iter(values))]:g}), since the role needs one")
            kind = "fontWeight"
        base, modes = compress(values, axes) if axes else (values[""], {})
        out.add(Token(role, kind, base, modes=modes, layer="semantic"))
    return out, notes


def their_names(text: str, mapping: Mapping) -> str:
    """`text` with each mapped role followed by the system's own name. A
    role is matched whole: a longer path that starts with it is left, and
    a period that ends a sentence after it is not part of it."""
    roles = sorted(mapping.roles, key=len, reverse=True)
    if not roles:
        return text
    pattern = re.compile(r"(?<![\w.-])(" + "|".join(re.escape(r) for r in roles)
                         + r")(?![\w-]|\.[\w-])")
    return pattern.sub(lambda m: f"{m.group(1)} (your {mapping.roles[m.group(1)].token})", text)
