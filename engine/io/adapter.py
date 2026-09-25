"""Naming adapters: an imported system keeps its own names end to end.

A mapping says which of the system's tokens plays each of the engine's
roles and which of its modes is each of the engine's axes. It is a JSON
file the owner edits (dump_mapping, load_mapping); propose() writes a first
one from names alone, marking each entry "by": "name" so the owner can see
what to confirm (an entry the owner writes says "by": "owner"). The owner
keeps a role or an axis out of the check with a "not mapped" entry,
{"token": null, "by": "owner"} or {"from": null, "by": "owner"}; view()
leaves it out with a note, merge() never fills it again and propose()
never writes one. An axis deleted from the file instead, one the system
has and propose() would read, is left out too, with a note that names it
and the "not mapped" entry that keeps it out on purpose.

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

import difflib
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
_ROLE_FIX = ("{\"token\": \"<your token>\", \"by\": \"owner\"}, or {\"token\": null, \"by\": "
             "\"owner\"} to keep it out of the check")
_ROLE_OUT = "{\"token\": null, \"by\": \"owner\"}"
_AXIS_OUT = "{\"from\": null, \"by\": \"owner\"}"
# Words a theme selector or mode name uses for a non-base value of our axes.
_AXIS_WORDS: Dict[str, str] = {
    "dark": "scheme", "rtl": "direction", "compact": "density", "high": "contrast",
    "high-contrast": "contrast", "contrast-high": "contrast", "more": "contrast",
    "reduced": "motion", "reduce": "motion", "reduced-motion": "motion",
}
# The notes view() gives for an owner's "not mapped" entry, shared so a
# report that lists those entries itself can tell the notes apart.
ROLE_LEFT_OUT = "{role} is not checked: the owner left it out in {name}"
AXIS_LEFT_OUT = ("the axis {axis} is not checked: the owner left it out in {name}, so every role "
                 "is read at the system's base")
AXIS_DELETED = ("{name} leaves out the axis {axis}, which the imported system has as {source}, "
                "so it was not checked and every role is read at the system's base; map it to "
                "check it, or write " + _AXIS_OUT.replace("{", "{{").replace("}", "}}")
                + " for it to keep it out on purpose")
_BASE_WORDS = ("light", "ltr", "comfortable", "standard", "default", "base", "off",
               "no-preference")


@dataclass(frozen=True)
class RoleMap:
    """The token that plays a role, and who said so. A token of None is
    the owner's "not mapped": the role stays out of the check."""
    token: Optional[str]
    by: str = "owner"


@dataclass(frozen=True)
class AxisMap:
    """The mode axis of the system that is one of ours: its name there, and
    our value -> its value. A source of None (and no values) is the
    owner's "not mapped": the axis stays out of the check."""
    source: Optional[str]
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
    return Mapping(roles, _propose_axes(ts))


def _propose_axes(ts: TokenSet) -> Dict[str, AxisMap]:
    """The axes a first mapping reads, by the names of the set's own."""
    axes: Dict[str, AxisMap] = {}
    for name, (base, other) in ts.axes.items():
        ours = _our_axis(name, base, other)
        if ours is None or ours in axes:
            continue
        axes[ours] = AxisMap(name, {AXES[ours][0]: base, AXES[ours][1]: other}, "name")
    return axes


def _our_axis(name: str, base: str, other: str) -> Optional[str]:
    """The axis of ours a mode axis is: the one it is named for, whatever
    its values, or the one its values or class name say."""
    if name in AXES:
        return name
    if base not in _BASE_WORDS and not name.startswith(base + "-"):
        return None
    word = other
    if (base, other) == ("off", "on"):
        word = name.split("-", 1)[1] if "-" in name else name
    return _AXIS_WORDS.get(word)


def merge(proposed: Mapping, existing: Mapping,
          name: str = "mapping.json") -> Tuple[Mapping, List[str]]:
    """The mapping to write when a system is imported again, and notes on
    what was proposed for the first time. Every entry the owner wrote
    ("by": "owner"), a "not mapped" one included, stays as it is; the new
    proposal fills only the roles and axes the owner has not set. An entry
    the engine proposed before is replaced by the new proposal, or dropped
    when names no longer say it. A role or axis the file does not have at
    all is proposed and named in a note, so the owner can write "not
    mapped" for it. Roles and axes come in the engine's order."""
    roles = {r: m for r, m in existing.roles.items() if m.by == "owner"}
    for r, m in proposed.roles.items():
        roles.setdefault(r, m)
    axes = {a: m for a, m in existing.axes.items() if m.by == "owner"}
    for a, m in proposed.axes.items():
        axes.setdefault(a, m)
    merged = Mapping({r: roles[r] for r in ROLE_TYPES if r in roles},
                     {a: axes[a] for a in AXES if a in axes})
    new = [r for r in merged.roles if r not in existing.roles]
    notes: List[str] = []
    if len(new) == 1:
        notes.append(f"{name} did not map {new[0]}, so it was proposed as "
                     f"{merged.roles[new[0]].token} by name; to keep it out of the check, write "
                     f"{_ROLE_OUT} for it")
    elif new:
        notes.append(f"{name} did not map {_few(new)}, so they were proposed by name; to keep "
                     f"one out of the check, write {_ROLE_OUT} for it")
    notes += [f"{name} did not map the axis {a}, so it was proposed from {m.source} by name; "
              f"to keep it out of the check, write {_AXIS_OUT} for it"
              for a, m in merged.axes.items() if a not in existing.axes]
    return merged, notes


# ---------------------------------------------------------------- file


def dump_mapping(mapping: Mapping) -> str:
    doc = {"version": VERSION,
           "axes": {a: ({"from": m.source, "values": dict(m.values), "by": m.by}
                        if m.source is not None else {"from": None, "by": m.by})
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
                      ("axes", "axis to {\"from\": ..., \"values\": ..., \"by\": \"owner\"}, "
                               f"or {_AXIS_OUT} to keep it out of the check")):
        if not isinstance(doc.get(key) or {}, dict):
            raise InputError(f"{name} {key} is {json.dumps(doc[key])}; write it as an object of "
                             f"{what}")
    roles: Dict[str, RoleMap] = {}
    for role, entry in (doc.get("roles") or {}).items():
        if role not in ROLE_TYPES:
            near = difflib.get_close_matches(role, list(ROLE_TYPES), n=1)
            example = (f"such as the nearest, {near[0]}" if near
                       else "for example color.text.default")
            raise InputError(f"{name} maps {role}, which is not a role the engine checks; use "
                             f"one of its roles, {example}")
        by = entry.get("by", "owner") if isinstance(entry, dict) else None
        token = entry.get("token", "") if isinstance(entry, dict) else ""
        if not (by in BY and (isinstance(token, str) and token
                              or token is None and by == "owner")):
            raise InputError(f"{name} role {role} is {json.dumps(entry)}; write {_ROLE_FIX}")
        roles[role] = RoleMap(entry["token"], entry.get("by", "owner"))
    axes: Dict[str, AxisMap] = {}
    for axis, entry in (doc.get("axes") or {}).items():
        if axis not in AXES:
            raise InputError(f"{name} maps the axis {axis}, which is not one of the engine's "
                             "axes; use scheme, contrast, density, direction or motion")
        values = entry.get("values") if isinstance(entry, dict) else None
        if isinstance(entry, dict) and "from" in entry and entry["from"] is None \
                and entry.get("by", "owner") == "owner" and not values:
            axes[axis] = AxisMap(None, {}, "owner")
            continue
        if not (isinstance(entry, dict) and isinstance(entry.get("from"), str)
                and isinstance(values, dict) and set(values) == set(AXES[axis])
                and all(isinstance(v, str) for v in values.values())
                and entry.get("by", "owner") in BY):
            raise InputError(f"{name} axis {axis} is {json.dumps(entry)}; write {{\"from\": "
                             f"\"<your mode axis>\", \"values\": {{\"{AXES[axis][0]}\": \"...\", "
                             f"\"{AXES[axis][1]}\": \"...\"}}, \"by\": \"owner\"}}, or {_AXIS_OUT} "
                             "to keep it out of the check")
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


def _check(ts: TokenSet, mapping: Mapping, name: str) -> None:
    for role, m in mapping.roles.items():
        if m.token is not None and not ts.has(m.token) and not (ROLE_TYPES[role] == "typography"
                                        and _has_fields(ts, m.token)):
            raise InputError(f"{name} sends {role} to {m.token}, which the imported system "
                             "does not have; point it at one of its tokens, or remove the line")
    used: Dict[str, str] = {}
    for axis, m in mapping.axes.items():
        if m.source is None:
            continue
        if m.source not in ts.axes:
            have = ", ".join(ts.axes) or "none"
            raise InputError(f"{name} reads {axis} from the mode axis {m.source}, which the "
                             f"imported system does not have (it has {have}); fix the from "
                             "value, or remove the axis")
        if m.source in used:
            raise InputError(f"{name} reads {used[m.source]} and {axis} both from "
                             f"{m.source}; read each of the engine's axes from a mode axis of "
                             "its own, or remove one")
        used[m.source] = axis
        theirs = ts.axes[m.source]
        for ours, value in m.values.items():
            if value not in theirs:
                raise InputError(f"{name} reads {axis} {ours} from {m.source} {value}, but "
                                 f"{m.source} has the values {theirs[0]} and {theirs[1]}; use "
                                 "those")
        if len(set(m.values.values())) < len(m.values):
            base, other = AXES[axis]
            raise InputError(f"{name} reads {axis} {base} and {other} both from "
                             f"{m.source} {m.values[base]}; read each from its own value")


def _own_roles(ts: TokenSet) -> List[str]:
    """The roles the set has under the role's own path."""
    return [r for r in ROLE_TYPES if ts.has(r)]


def _identity(ts: TokenSet, mapping: Mapping) -> bool:
    """Whether the mapping names every role and axis the set has, each as
    itself, and nothing else."""
    return set(mapping.roles) == set(_own_roles(ts)) \
        and all(r == m.token for r, m in mapping.roles.items()) \
        and set(mapping.axes) == set(ts.axes) \
        and all(a == m.source and m.values == {v: v for v in AXES[a]}
                for a, m in mapping.axes.items())


def _and(names: List[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def _few(names: List[str]) -> str:
    """The names, or the first three and how many more."""
    return _and(names if len(names) <= 4 else names[:3] + [f"{len(names) - 3} more"])


def _left_out(ts: TokenSet, mapping: Mapping, name: str) -> List[str]:
    """A note on the roles the set has under their own paths that the
    mapping leaves out: the owner took them out, so they are not checked."""
    gone = [r for r in _own_roles(ts) if r not in mapping.roles]
    if not gone:
        return []
    if len(gone) == 1:
        return [f"{name} leaves out {gone[0]}, which the imported system has under the role's "
                "own name, so it was not checked; map it to check it"]
    return [f"{name} leaves out {_few(gone)}, which the imported system has under each role's "
            "own name, so they were not checked; map each one to check it"]


def _axes_left_out(ts: TokenSet, mapping: Mapping, name: str) -> List[str]:
    """A note on each axis the set has, and a first mapping would read, that
    the mapping leaves out without a "not mapped" entry: it was deleted from
    the file, so it is not checked."""
    used = {m.source for m in mapping.axes.values() if m.source is not None}
    return [AXIS_DELETED.format(axis=axis, source=m.source, name=name)
            for axis, m in _propose_axes(ts).items()
            if axis not in mapping.axes and m.source not in used]


def _resolve(ts: TokenSet, role: str, token: str, context: str) -> Any:
    if ROLE_TYPES[role] == "typography" and not ts.has(token):
        return {key: ts.resolve(path, context) for key, path in _field_names(token).items()}
    return ts.resolve(token, context)


def view(ts: TokenSet, mapping: Mapping,
         name: str = "the mapping") -> Tuple[TokenSet, List[str]]:
    """The set the engine checks, in its own roles and axes, and notes on
    what it read differently or left out. Only the mapped roles and axes
    are in it: a role or axis the owner took out of the mapping is not
    checked, and an axis left out is held at the system's base. A mapping
    that names every role and axis the set has, each as itself, with
    nothing read differently, gives the system itself. A "not mapped"
    entry keeps its role or axis out with a note. Raises InputError for a
    token or axis value the system lacks; `name` is the mapping file its
    messages name."""
    _check(ts, mapping, name)
    axes = {a: AXES[a] for a in AXES if a in mapping.axes and mapping.axes[a].source is not None}
    out = TokenSet(axes)
    notes: List[str] = [AXIS_LEFT_OUT.format(axis=a, name=name)
                        for a, m in mapping.axes.items() if m.source is None]
    notes += _axes_left_out(ts, mapping, name)
    notes += _left_out(ts, mapping, name)
    for role, m in mapping.roles.items():
        if m.token is None:
            notes.append(ROLE_LEFT_OUT.format(role=role, name=name))
            continue
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
    if not notes and _identity(ts, mapping):
        return ts, []
    return out, notes


_CONTEXT = re.compile(r"\(([a-z]+:[a-z]+(?:,[a-z]+:[a-z]+)*)\)")


def their_names(text: str, mapping: Mapping) -> str:
    """`text` with each mapped role followed by the system's own name, and
    each context of mapped axes followed by the system's own modes when
    they differ. A role is matched whole: a longer path that starts with it
    is left, and a period that ends a sentence after it is not part of
    it."""
    roles = sorted((r for r, m in mapping.roles.items() if m.token is not None),
                   key=len, reverse=True)
    if roles:
        pattern = re.compile(r"(?<![\w.-])(" + "|".join(re.escape(r) for r in roles)
                             + r")(?![\w-]|\.[\w-])")
        text = pattern.sub(lambda m: f"{m.group(1)} (your {mapping.roles[m.group(1)].token})",
                           text)
    return _CONTEXT.sub(lambda m: _their_context(m.group(0), m.group(1), mapping), text)


def _their_context(whole: str, key: str, mapping: Mapping) -> str:
    pairs = [p.split(":") for p in key.split(",")]
    if not all(a in mapping.axes and mapping.axes[a].source is not None and v in AXES[a]
               for a, v in pairs):
        return whole
    theirs = ",".join(f"{mapping.axes[a].source}:{mapping.axes[a].values[v]}" for a, v in pairs)
    return whole if theirs == key else f"({key}; your {theirs})"
