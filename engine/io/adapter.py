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

A typography role maps to one composite token, or field by field:
{"fields": {"fontSize": {"token": "text-size-lg", "by": "owner"}, ...}},
for a system that keeps each field of its type in a token of its own
(fontFamily, fontSize, fontWeight, lineHeight, letterSpacing). view()
reads each field from its own token; a role with a field left out is not
checked, with a note that names the field, since the engine never picks
one for it.

A system with no motion mode may keep its reduced motion in separate
tokens, a twin beside each token whose name adds a reduced word
(duration-slow and duration-slow-reduced, or motion.reduced.*). When the
mapping reads no motion axis, view() reads each twin as its token's
reduced-motion value, with a note naming the pairs.

propose() maps a role when a token's name is the role's own path
written with other separators (color.text.default, color-text-default,
color/text/default), a typography role to the five field properties the
engine's CSS writes for it, and a color role when a token's name is one
the common naming vocabularies give it (VOCABULARIES: background and
foreground, on- pairs, brand names, bg, fg and border families, text
names, or the role's path without color), each entry saying which
vocabulary matched. Names only: a name maps only a token of the role's
type, and a name that means different things in different systems
(accent, secondary) is not in the table. It maps an axis only when its name or its
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
from engine.foundations.modes import FOUNDATION_AXES
from engine.foundations.tokens import (
    ROOT_BASE, AliasError, Token, TokenSet, alias_target, is_alias)
from engine.foundations.values import TYPOGRAPHY_FIELDS
from engine.io.mode_words import axis_of, mode_of

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
# The notes view() gives for an owner's "not mapped" entry, shared so a
# report that lists those entries itself can tell the notes apart.
ROLE_LEFT_OUT = "{role} is not checked: the owner left it out in {name}"
AXIS_LEFT_OUT = ("the axis {axis} is not checked: the owner left it out in {name}, so every role "
                 "is read at the system's base")
AXIS_DELETED = ("{name} leaves out the axis {axis}, which the imported system has as {source}, "
                "so it was not checked and every role is read at the system's base; map it to "
                "check it, or write " + _AXIS_OUT.replace("{", "{{").replace("}", "}}")
                + " for it to keep it out on purpose")


@dataclass(frozen=True)
class FieldMap:
    """The token one field of a typography role reads, and who said so. A
    token of None is the owner's "not mapped" for that field."""
    token: Optional[str]
    by: str = "owner"


@dataclass(frozen=True)
class RoleMap:
    """The token that plays a role, and who said so. A token of None is
    the owner's "not mapped": the role stays out of the check. A
    typography role may map field by field instead (fields, made with
    per_field): its token is then the fields and their tokens written out,
    for the messages that name it."""
    token: Optional[str]
    by: str = "owner"
    fields: Optional[Dict[str, FieldMap]] = field(default=None, hash=False)
    # The naming vocabulary a proposal by name matched (see VOCABULARIES);
    # "" for a token named as the role itself, or an entry the owner wrote.
    vocabulary: str = ""

    @classmethod
    def per_field(cls, fields: Dict[str, FieldMap]) -> "RoleMap":
        """A typography role mapped one field at a time, in the engine's
        field order; the role is the owner's when any field is."""
        ordered = {k: fields[k] for k in TYPOGRAPHY_FIELDS if k in fields}
        by = "owner" if any(f.by == "owner" for f in ordered.values()) else "name"
        return cls(_field_label(ordered), by, ordered)


def _field_label(fields: Dict[str, FieldMap]) -> str:
    """The mapped fields and their tokens, as a message names them."""
    return _and([f"{k} {f.token}" for k, f in fields.items() if f.token is not None] or ["none"])


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


# Common naming vocabularies: names a system writes for a role, in hyphens,
# matched with any separators, after a leading color or colors segment
# and before a trailing default one (color-background, colors.primary.
# DEFAULT). A table of names, never a look. Earlier vocabularies win a
# role; a name maps only a token of the role's type.
VOCABULARIES: Tuple[Tuple[str, str, Tuple[Tuple[str, str], ...]], ...] = (
    ("plain names", "background, foreground, primary, border, input, ring and the -foreground "
     "pairs", (
        ("background", "color.surface.page"), ("foreground", "color.text.default"),
        ("card", "color.surface.card"), ("surface", "color.surface.card"),
        ("popover", "color.surface.raised"), ("muted", "color.surface.sunken"),
        ("muted-foreground", "color.text.muted"),
        ("primary", "color.action.primary"), ("primary-foreground", "color.text.on-action"),
        ("destructive", "color.action.danger"),
        ("destructive-foreground", "color.text.on-danger"), ("border", "color.line.subtle"),
        ("input", "color.line.input"), ("ring", "color.focus.ring"),
        ("focus", "color.focus.ring"), ("link", "color.text.link"))),
    ("text names", "text-primary, text-secondary, text-link", (
        ("text", "color.text.default"), ("text-primary", "color.text.default"),
        ("text-base", "color.text.default"), ("text-body", "color.text.default"),
        ("text-secondary", "color.text.muted"), ("text-subtle", "color.text.muted"),
        ("text-tertiary", "color.text.muted"), ("text-on-inverse", "color.text.inverse"),
        ("text-brand", "color.text.accent"), ("text-on-primary", "color.text.on-action"),
        ("text-on-brand", "color.text.on-action"), ("text-on-accent", "color.text.on-action"),
        ("text-danger", "color.status.danger.text"), ("text-error", "color.status.danger.text"),
        ("text-warning", "color.status.warning.text"),
        ("text-success", "color.status.success.text"), ("text-info", "color.status.info.text"))),
    ("bg, fg and border families", "bg-default, fg-muted, border-default", (
        ("bg", "color.surface.page"), ("bg-default", "color.surface.page"),
        ("bg-canvas", "color.surface.page"),
        ("bg-page", "color.surface.page"), ("bg-base", "color.surface.page"),
        ("bg-surface", "color.surface.card"), ("bg-card", "color.surface.card"),
        ("bg-panel", "color.surface.card"), ("bg-subtle", "color.surface.sunken"),
        ("bg-muted", "color.surface.sunken"), ("bg-inset", "color.surface.sunken"),
        ("bg-sunken", "color.surface.sunken"), ("bg-raised", "color.surface.raised"),
        ("bg-overlay", "color.surface.raised"), ("bg-elevated", "color.surface.raised"),
        ("bg-inverse", "color.surface.inverse"), ("bg-emphasis", "color.surface.inverse"),
        ("bg-selected", "color.surface.selected"), ("bg-brand", "color.surface.brand"),
        ("fg", "color.text.default"), ("fg-default", "color.text.default"),
        ("fg-base", "color.text.default"),
        ("fg-muted", "color.text.muted"), ("fg-subtle", "color.text.muted"),
        ("fg-secondary", "color.text.muted"), ("fg-inverse", "color.text.inverse"),
        ("fg-on-emphasis", "color.text.inverse"), ("fg-on-inverse", "color.text.inverse"),
        ("fg-disabled", "color.text.disabled"), ("fg-link", "color.text.link"),
        ("fg-accent", "color.text.accent"), ("fg-on-brand", "color.text.on-action"),
        ("fg-on-primary", "color.text.on-action"), ("fg-on-accent", "color.text.on-action"),
        ("fg-danger", "color.status.danger.text"), ("fg-error", "color.status.danger.text"),
        ("border-default", "color.line.subtle"), ("border-base", "color.line.subtle"),
        ("border-subtle", "color.line.subtle"),
        ("border-muted", "color.line.subtle"), ("border-input", "color.line.input"),
        ("border-field", "color.line.input"), ("border-control", "color.line.input"),
        ("border-focus", "color.focus.ring"), ("border-focused", "color.focus.ring"),
        ("border-danger", "color.line.danger"), ("border-error", "color.line.danger"),
        ("border-selected", "color.line.selected"), ("border-active", "color.line.selected"),
        ("border-accent", "color.line.accent"), ("border-brand", "color.line.accent"))),
    ("on- pairs", "on-surface, on-primary, on-error", (
        ("on-background", "color.text.default"), ("on-surface", "color.text.default"),
        ("on-surface-variant", "color.text.muted"), ("surface-variant", "color.surface.sunken"),
        ("inverse-surface", "color.surface.inverse"),
        ("inverse-on-surface", "color.text.inverse"), ("on-primary", "color.text.on-action"),
        ("error", "color.action.danger"), ("danger", "color.action.danger"),
        ("on-error", "color.text.on-danger"), ("on-danger", "color.text.on-danger"),
        ("outline", "color.line.input"), ("outline-variant", "color.line.subtle"))),
    ("brand names", "brand, brand-hover, on-brand", (
        ("brand", "color.action.primary"), ("brand-primary", "color.action.primary"),
        ("brand-base", "color.action.primary"), ("brand-hover", "color.action.primary-hover"),
        ("brand-pressed", "color.action.primary-pressed"),
        ("brand-active", "color.action.primary-pressed"), ("on-brand", "color.text.on-action"),
        ("brand-foreground", "color.text.on-action"), ("brand-fg", "color.text.on-action"),
        ("brand-contrast", "color.text.on-action"))),
)
# The vocabulary a token named as a color role without its color segment
# (text-default, surface-raised, focus-ring) matches.
ROLE_NAMES = ("role names", "a color role's own path without color, such as text-default")
VOCABULARY_EXAMPLES: Dict[str, str] = {ROLE_NAMES[0]: ROLE_NAMES[1],
                                       **{v: ex for v, ex, _ in VOCABULARIES}}


def _keys(path: str) -> Tuple[str, Optional[str]]:
    """The names a token answers to in the vocabularies: its own, without a
    leading color or colors segment, and that without a trailing default
    one (None when it has none), which a name matches only after every
    whole name has."""
    parts = _norm(path).split(".")
    if len(parts) > 1 and parts[0] in ("color", "colors"):
        parts = parts[1:]
    short = ".".join(parts[:-1]) if len(parts) > 1 and parts[-1] == "default" else None
    return ".".join(parts), short


def propose(ts: TokenSet) -> Mapping:
    """A first mapping from names alone (see the module docstring)."""
    by_norm: Dict[str, str] = {}
    by_key: Dict[str, str] = {}
    by_short: Dict[str, str] = {}
    for t in ts.tokens():
        by_norm.setdefault(_norm(t.path), t.path)
        whole, short = _keys(t.path)
        by_key.setdefault(whole, t.path)
        if short is not None:
            by_short.setdefault(short, t.path)
    roles: Dict[str, RoleMap] = {}
    for role, kind in ROLE_TYPES.items():
        match = by_norm.get(_norm(role))
        if match is not None:
            roles[role] = RoleMap(match, "name")
        elif kind == "typography":
            prefix = role.replace(".", "-")
            if _has_fields(ts, prefix):
                roles[role] = RoleMap(prefix, "name")
    taken = {m.token for m in roles.values()}
    tables = [(ROLE_NAMES[0], tuple((r[len("color."):], r) for r in ROLE_TYPES
                                    if r.startswith("color.")))]
    tables += [(name, entries) for name, _, entries in VOCABULARIES]
    for index, (vocabulary, entries) in ((i, t) for i in (by_key, by_short) for t in tables):
        for name, role in entries:
            token = index.get(_norm(name))
            if role in roles or token is None or token in taken \
                    or ts.get(token).type != ROLE_TYPES[role]:
                continue
            roles[role] = RoleMap(token, "name", vocabulary=vocabulary)
            taken.add(token)
    return Mapping({r: roles[r] for r in ROLE_TYPES if r in roles}, _propose_axes(ts))


def _propose_axes(ts: TokenSet) -> Dict[str, AxisMap]:
    """The axes a first mapping reads, by the names of the set's own."""
    axes: Dict[str, AxisMap] = {}
    for name, values in ts.axes.items():
        if _root_based(name, values):  # only the owner can say which value is which
            continue
        base, other = values
        ours = _our_axis(name, base, other)
        if ours is None or ours in axes:
            continue
        axes[ours] = AxisMap(name, {AXES[ours][0]: base, AXES[ours][1]: other}, "name")
    return axes


def _root_based(name: str, values: Tuple[str, ...]) -> bool:
    """True for an axis whose base is what :root holds and whose modes
    include a value the engine keeps as a base (density: base, comfortable):
    a first mapping by name would put the file's own mode on the engine's
    other value, so only the owner maps it. A root plus one mode that is
    one of the engine's other values (data-size: base, compact) maps by
    name as before."""
    return values[0] == ROOT_BASE and (
        len(values) > 2 or name in AXES or values[1] in {v[0] for v in AXES.values()})


def _our_axis(name: str, base: str, other: str) -> Optional[str]:
    """The axis of ours a mode axis is: the one it is named for, whatever
    its values, or the one its values say by the importers' shared matcher
    (its name is the context contrast and motion need). A class that is on
    or off (class-compact) is the axis its name says."""
    if name in AXES:
        return name
    if (base, other) == ("off", "on"):
        return mode_of(name)
    hit = axis_of([base, other], [name])
    return hit[0] if hit is not None and hit[1] == 0 else None


def merge(proposed: Mapping, existing: Mapping,
          name: str = "mapping.json") -> Tuple[Mapping, List[str]]:
    """The mapping to write when a system is imported again, and notes on
    what was proposed for the first time. Every entry the owner wrote
    ("by": "owner"), a "not mapped" one included, stays as it is; the new
    proposal fills only the roles and axes the owner has not set. An entry
    the engine proposed before is replaced by the new proposal, or dropped
    when names no longer say it. A role or axis the file does not have at
    all is proposed and named in a note, so the owner can write "not
    mapped" for it. A role mapped field by field keeps the fields the owner
    wrote; a field the engine proposed before is dropped unless the new
    proposal maps it field by field too. Roles and axes come in the
    engine's order."""
    roles = {r: _owners(m, proposed.roles.get(r)) for r, m in existing.roles.items()
             if m.by == "owner"}
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


def _owners(m: RoleMap, proposed: Optional[RoleMap]) -> RoleMap:
    """An owner's role entry as a merge keeps it: whole, or for one mapped
    field by field, the owner's fields and the new proposal's for the
    rest."""
    if m.fields is None:
        return m
    fields = {k: f for k, f in m.fields.items() if f.by == "owner"}
    for k, f in ((proposed.fields or {}) if proposed is not None else {}).items():
        fields.setdefault(k, f)
    return RoleMap.per_field(fields)


# ---------------------------------------------------------------- file


def dump_mapping(mapping: Mapping) -> str:
    doc = {"version": VERSION,
           "axes": {a: ({"from": m.source, "values": dict(m.values), "by": m.by}
                        if m.source is not None else {"from": None, "by": m.by})
                    for a, m in mapping.axes.items()},
           "roles": {r: _dump_role(m) for r, m in mapping.roles.items()}}
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def _dump_role(m: RoleMap) -> Dict[str, Any]:
    if m.fields is None:
        return ({"token": m.token, "by": m.by, "vocabulary": m.vocabulary} if m.vocabulary
                else {"token": m.token, "by": m.by})
    return {"fields": {k: {"token": f.token, "by": f.by} for k, f in m.fields.items()}}


_FIELD_FIX = "{\"token\": \"<your token>\", \"by\": \"owner\"}"


def _parse_fields(role: str, entry: Dict[str, Any], name: str) -> RoleMap:
    """A typography role mapped field by field (see RoleMap)."""
    if ROLE_TYPES[role] != "typography":
        raise InputError(f"{name} role {role} maps fields, but only a typography role takes "
                         f"them; write {_FIELD_FIX} for a {ROLE_TYPES[role]} role")
    if "token" in entry:
        raise InputError(f"{name} role {role} has both token and fields; keep token for one "
                         "composite token, or fields for one token per field")
    extra = [k for k in entry if k != "fields"]
    if extra:
        raise InputError(f"{name} role {role} has the key {extra[0]}, which a role mapped "
                         "field by field does not use; keep only fields")
    raw = entry["fields"]
    if not isinstance(raw, dict):
        raise InputError(f"{name} role {role} fields is {json.dumps(raw)}; write it as an "
                         f"object of field to {_FIELD_FIX}")
    fields: Dict[str, FieldMap] = {}
    for key, value in raw.items():
        if key not in TYPOGRAPHY_FIELDS:
            raise InputError(f"{name} role {role} maps the field {key}, which a typography "
                             f"role does not have; use {_or(list(TYPOGRAPHY_FIELDS))}")
        by = value.get("by", "owner") if isinstance(value, dict) else None
        token = value.get("token", "") if isinstance(value, dict) else ""
        if not (by in BY and (isinstance(token, str) and token
                              or token is None and by == "owner")):
            raise InputError(f"{name} role {role} field {key} is {json.dumps(value)}; write "
                             f"{_FIELD_FIX}")
        fields[key] = FieldMap(token, by)
    if not any(f.token is not None for f in fields.values()):
        raise InputError(f"{name} role {role} has no field in fields; map at least one field, "
                         f"for example \"fontSize\": {_FIELD_FIX}")
    return RoleMap.per_field(fields)


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
        if isinstance(entry, dict) and "fields" in entry:
            roles[role] = _parse_fields(role, entry, name)
            continue
        by = entry.get("by", "owner") if isinstance(entry, dict) else None
        token = entry.get("token", "") if isinstance(entry, dict) else ""
        if not (by in BY and (isinstance(token, str) and token
                              or token is None and by == "owner")):
            raise InputError(f"{name} role {role} is {json.dumps(entry)}; write {_ROLE_FIX}")
        vocabulary = entry.get("vocabulary", "")
        if not isinstance(vocabulary, str):
            raise InputError(f"{name} role {role} has vocabulary {json.dumps(vocabulary)}; "
                             "remove it, or write the name of the vocabulary as text")
        extra = [k for k in entry if k not in ("token", "by", "vocabulary")]
        if extra:
            raise InputError(f"{name} role {role} has the key {extra[0]}, which a role entry "
                             "does not use; keep only token, by and vocabulary")
        roles[role] = RoleMap(entry["token"], entry.get("by", "owner"), vocabulary=vocabulary)
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
        for key, f in (m.fields or {}).items():
            if f.token is not None and not ts.has(f.token):
                raise InputError(f"{name} sends {role} field {key} to {f.token}, which the "
                                 "imported system does not have; point it at one of its "
                                 "tokens, or remove the field")
        if m.fields is not None:
            continue
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
                                 f"{m.source} has the values {_and(list(theirs))}; use "
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


def _or(names: List[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} or {names[-1]}"


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


def deleted_axes(ts: TokenSet, mapping: Mapping) -> Dict[str, str]:
    """Each axis the set has, and a first mapping would read, that the
    mapping leaves out without a "not mapped" entry (it was deleted from
    the file), with the set's own axis it would read."""
    used = {m.source for m in mapping.axes.values() if m.source is not None}
    return {axis: m.source for axis, m in _propose_axes(ts).items()
            if axis not in mapping.axes and m.source not in used}


def _axes_left_out(ts: TokenSet, mapping: Mapping, name: str) -> List[str]:
    """A note on each axis deleted from the mapping, and on each axis whose
    base is the root that the mapping does not read: it is not checked."""
    notes = [AXIS_DELETED.format(axis=axis, source=source, name=name)
             for axis, source in deleted_axes(ts, mapping).items()]
    used = {m.source for m in mapping.axes.values()}
    return notes + [_root_axis_note(axis, values, name) for axis, values in ts.axes.items()
                    if _root_based(axis, values) and axis not in used]


def _root_axis_note(axis: str, values: Tuple[str, ...], name: str) -> str:
    """Why an axis whose base is the root is not mapped, and the entry that
    maps it by hand."""
    ours = axis if axis in AXES else (mode_of(axis) or "<the engine's axis>")
    pair = AXES.get(ours, ("<its base>", "<its other value>"))
    choice = "<one of " + _and(list(values)) + ">"
    entry = (f'"{ours}": {{"from": "{axis}", "values": {{"{pair[0]}": "{choice}", '
             f'"{pair[1]}": "{choice}"}}, "by": "owner"}}')
    return (f"the axis {axis} of the imported system ({_and(list(values))}) has what :root "
            f"holds as its base, not a named value, so it was not mapped and is not checked; "
            f"to check it, write in {name} {entry}")


# The word a token's name carries when it holds another token's value under
# reduced motion (duration-slow-reduced, motion.reduced.duration.slow).
REDUCED_WORDS = ("reduced", "reduce")
REDUCED_NOTE = ("motion:reduced is read from the separate tokens the system declares for it: "
                "{pairs}; map the motion axis in {name} to read it from a mode instead")


def _name_words(path: str) -> Tuple[str, ...]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", path)
    return tuple(w.lower() for w in re.split(r"[.\-/_ ]+", spaced) if w)


def reduced_pairs(ts: TokenSet) -> Dict[str, str]:
    """Each token that has a separate reduced-motion twin, and the twin: a
    token of the same type whose name is the token's own with a reduced
    word added anywhere (duration-slow-reduced, reduced-duration-slow,
    motion.reduced.duration.slow, or reduced-motion before the rest).
    Names only, in the set's order."""
    by_words: Dict[Tuple[str, ...], str] = {}
    for t in ts.tokens():
        by_words.setdefault(_name_words(t.path), t.path)
    out: Dict[str, str] = {}
    for t in ts.tokens():
        words = _name_words(t.path)
        for i, word in enumerate(words):
            if word not in REDUCED_WORDS:
                continue
            for drop in (1, 2):
                if drop == 2 and words[i + 1:i + 2] != ("motion",):
                    continue
                base = by_words.get(words[:i] + words[i + drop:])
                if base is not None and base != t.path and base not in out \
                        and ts.get(base).type == t.type:
                    out[base] = t.path
                    break
            else:
                continue
            break
    return out


def reduced_twins(ts: TokenSet, mapping: Mapping) -> Dict[str, Tuple[str, str]]:
    """The mapped motion roles view() reads under reduced motion from a
    separate twin token, each with (the token it reads, the twin): only
    when the mapping reads no motion axis and the owner did not leave it
    out, and the system has no mode a first mapping would read as one. A
    role whose token aliases a token with a twin reads that twin."""
    if "motion" in mapping.axes or "motion" in _propose_axes(ts):
        return {}
    pairs = reduced_pairs(ts)
    out: Dict[str, Tuple[str, str]] = {}
    for role, m in mapping.roles.items():
        if m.token is None or m.fields is not None or not ts.has(m.token) \
                or "motion" not in FOUNDATION_AXES.get(role.split(".", 1)[0], ()):
            continue
        path, seen = m.token, set()
        while path not in pairs and path not in seen and ts.has(path) \
                and is_alias(ts.get(path).value):
            seen.add(path)
            path = alias_target(ts.get(path).value)
        if path in pairs:
            out[role] = (path, pairs[path])
    return out


def _resolve(ts: TokenSet, role: str, token: str, context: str,
             fields: Optional[Dict[str, FieldMap]] = None) -> Any:
    if fields is not None:
        return {key: ts.resolve(f.token, context) for key, f in fields.items()}
    if ROLE_TYPES[role] == "typography" and not ts.has(token):
        return {key: ts.resolve(path, context) for key, path in _field_names(token).items()}
    return ts.resolve(token, context)


def _fields_unfit(ts: TokenSet, role: str, fields: Dict[str, FieldMap],
                  name: str) -> str:
    """Why a role mapped field by field cannot be checked ("" when it can):
    a field left out, which is never guessed, or a field token of another
    type."""
    missing = [k for k in TYPOGRAPHY_FIELDS if fields.get(k) is None or fields[k].token is None]
    if missing:
        mapped = [k for k in TYPOGRAPHY_FIELDS if k not in missing]
        return (f"{role} maps {_and(mapped)} field by field in {name} but not {_and(missing)}, "
                "so it was not checked; add " + _and([f'"{k}": {_FIELD_FIX}' for k in missing])
                + " to its fields")
    for key, f in fields.items():
        want = TYPOGRAPHY_FIELDS[key][0]
        kind = ts.get(f.token).type
        weight = want == "fontWeight" and kind == "number"
        if kind != want and not weight:
            return (f"{role} field {key} reads {f.token}, a {kind}, but the field needs a {want}; "
                    f"point it at one of your {want} tokens in {name}")
    return ""


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
    twins = reduced_twins(ts, mapping)
    axes = {a: AXES[a] for a in AXES if a in mapping.axes and mapping.axes[a].source is not None
            or a == "motion" and twins}
    out = TokenSet(axes)
    notes: List[str] = [AXIS_LEFT_OUT.format(axis=a, name=name)
                        for a, m in mapping.axes.items() if m.source is None]
    notes += _axes_left_out(ts, mapping, name)
    notes += _left_out(ts, mapping, name)
    if twins:
        pairs = {base: twin for base, twin in twins.values()}
        notes.append(REDUCED_NOTE.format(
            pairs=_and([f"{twin} for {base}" for base, twin in pairs.items()]), name=name))
    for role, m in mapping.roles.items():
        if m.token is None:
            notes.append(ROLE_LEFT_OUT.format(role=role, name=name))
            continue
        want = ROLE_TYPES[role]
        if m.fields is not None:
            why = _fields_unfit(ts, role, m.fields, name)
            if why:
                notes.append(why)
                continue
        values: Dict[str, Any] = {}
        try:
            for ctx in contexts(list(axes), axes):
                ours = parse(ctx, axes)
                theirs = {mapping.axes[a].source: mapping.axes[a].values[v]
                          for a, v in ours.items() if a in mapping.axes}
                their_ctx = join({a: v for a, v in theirs.items()
                                  if v != ts.axes[a][0]}, ts.axes)
                token = (twins[role][1] if role in twins and ours.get("motion") == "reduced"
                         else m.token)
                values[ctx] = _resolve(ts, role, token, their_ctx, m.fields)
        except (AliasError, ModeError) as exc:
            notes.append(f"{role} reads {m.token}, which cannot be resolved ({exc}); it was left "
                         "out of the check")
            continue
        kind = (want if want == "typography" and (m.fields is not None or not ts.has(m.token))
                else ts.get(m.token).type)
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
        text = pattern.sub(lambda m: _yours(m.group(1), mapping.roles[m.group(1)].token), text)
    return _CONTEXT.sub(lambda m: _their_context(m.group(0), m.group(1), mapping), text)


def _yours(role: str, token: Optional[str]) -> str:
    """The role, and the system's name beside it unless the name is the
    role's own written with other separators."""
    return role if token is None or _norm(token) == _norm(role) else f"{role} (your {token})"


def _their_context(whole: str, key: str, mapping: Mapping) -> str:
    pairs = [p.split(":") for p in key.split(",")]
    if not all(a in mapping.axes and mapping.axes[a].source is not None and v in AXES[a]
               for a, v in pairs):
        return whole
    theirs = ",".join(f"{mapping.axes[a].source}:{mapping.axes[a].values[v]}" for a, v in pairs)
    return whole if theirs == key else f"({key}; your {theirs})"
