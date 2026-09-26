"""Import Figma variables from a JSON export, in the file's own names.

The shape is the one Figma's REST API returns for GET
/v1/files/<file key>/variables/local ({"meta": {"variables": ...,
"variableCollections": ...}}), with or without the meta wrapper; a reader
run inside Figma writes the same shape. The engine makes no network call
and holds no file key: a person or an agent with Figma access exports the
variables and passes the JSON.

A variable's name becomes its path, a slash reading as a dot; a segment
with characters a path cannot hold is renamed with '-' and reported. Types
come from Figma's own fields: a COLOR is a color, its alpha kept (a
channel outside 0 to 1 is mapped into sRGB by CSS Color 4 gamut mapping
and reported, never refused); a FLOAT is a px dimension when every scope
it has sizes something (gap, width and height, corner radius, stroke, font
size, line height, letter spacing, effects, paragraphs), a font weight
under the font weight scope alone, and otherwise a plain number, noted; a
STRING is a font family under the font family scope alone. Figma keeps
numbers as 32-bit floats (0.2 comes back as 0.20000000298023224), so a
number is read to four decimals. Booleans and other strings are not read.
An alias to a variable in this export is an alias; one to a variable that
was not read is not read. The export also holds the library variables the
file uses, marked remote: those belong to another file and are not read as
this file's tokens, and each library collection is noted. An alias to a
library variable reads the value the export holds for it (a resolvedValue
on the alias, or the library variable's value in its default mode), with a
note that it is a snapshot; with no value held, it is not read, with what
the owner can do in Figma.

Modes: a collection with one mode gives values with no axis. One with two
gives one axis. Mode names are placed by the importers' shared matcher:
Light and Dark, Default and Dark, or Dark mode read into the scheme axis,
the light or default one the base and the dark one scheme:dark, as the
other importers read a dark scheme; any other pair gives an axis named
after both modes (Main and Partner give main-partner), the default mode
the base. Each such collection is noted. A collection whose modes are
viewport tiers (Mobile, Tablet and Desktop, or SM to XL, or a collection
named Breakpoints) is never a mode axis: its default tier is read, and one
note names the other tiers' values, which the engine sets itself. A
collection with more modes gives its default mode; second_modes names the
other mode to read for it.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.color_math import gamut_map_oklch, rgb_to_hex, srgb_to_oklch
from engine.foundations.errors import InputError
from engine.foundations.modes import AXES
from engine.foundations.tokens import Token, TokenSet
from engine.io.graph import cycles
from engine.io.mode_words import axis_of, words
from engine.io.report import Imported, ImportReport, Item, Mapped, Source, read_source

# The FLOAT scopes that size something in px.
SIZE_SCOPES = ("CORNER_RADIUS", "WIDTH_HEIGHT", "GAP", "STROKE_FLOAT", "FONT_SIZE",
               "LINE_HEIGHT", "LETTER_SPACING", "EFFECT_FLOAT", "PARAGRAPH_SPACING",
               "PARAGRAPH_INDENT")
# Where a person exports a file's variables.
REST_ENDPOINT = "GET /v1/files/<file key>/variables/local"
# Words that name a viewport tier in a mode's name, and a collection's.
VIEWPORT_WORDS = frozenset((
    "mobile", "phone", "tablet", "laptop", "desktop", "wide", "widescreen", "ultrawide", "watch",
    "tv", "xxs", "xs", "sm", "md", "lg", "xl", "xxl", "2xl", "3xl"))
VIEWPORT_COLLECTIONS = frozenset(("viewport", "viewports", "breakpoint", "breakpoints", "device",
                                  "devices", "screen", "screens", "responsive"))
_BAD = re.compile(r"[^A-Za-z0-9_-]+")
_AXIS_WORD = re.compile(r"[a-z][a-z0-9-]*")
_DECIMALS = 4


class _Bad(ValueError):
    """A variable that is not read; the message says why and the fix."""


@dataclass(frozen=True)
class _Ref:
    """An alias to another variable, by its id, with the value the export
    resolved it to when it holds one (a library variable's snapshot)."""
    id: str
    resolved: Any = field(default=None, compare=False)


@dataclass
class _Plan:
    """How a collection is read: its name, its modes (id to name), the
    modes read with their contexts (the base first, as ""), the axis they
    make, and a note for the report."""
    name: str
    modes: Dict[str, str]
    read: List[Tuple[str, str]]
    axis: Optional[Tuple[str, Tuple[str, str]]] = None
    note: str = ""
    # A library collection another file owns (remote in the export).
    remote: bool = False
    # A collection of viewport tiers: its other tiers, read for the note only.
    tiers: List[str] = field(default_factory=list)


@dataclass
class _Entry:
    """A variable as read, before its aliases are checked."""
    where: str
    name: str
    path: str
    kind: str
    values: Dict[str, Any]
    description: str
    # Collection and name, as a message names it: "Base/color/bg".
    label: str = ""
    # Each context's mode, for a message: "the mode Dark of Color".
    at: Dict[str, str] = field(default_factory=dict)
    renamed: List[Item] = field(default_factory=list)
    notes: List[Item] = field(default_factory=list)
    mapped: List[Mapped] = field(default_factory=list)
    # A viewport collection's other tiers: tier name -> the raw value there,
    # where it differs from the default tier's.
    tiers: Dict[str, Any] = field(default_factory=dict)
    # The collection's id.
    collection: Any = None


def _and(items: Sequence[str]) -> str:
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _or(items: Sequence[str]) -> str:
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " or " + items[-1]


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _known_axis(first: str, second: str, collection: str = "") -> Optional[Tuple[str, bool]]:
    """(axis, whether `first` is its base) when the two mode names name the
    two values of a known axis (Light and Dark, Dark mode and Light mode),
    or None, by the importers' shared matcher: contrast and motion also
    need their own name in the collection's name or a mode's."""
    known = axis_of([first, second], [collection])
    return None if known is None else (known[0], known[1] == 0)


def _number(raw: Any) -> bool:
    return isinstance(raw, (int, float)) and not isinstance(raw, bool) and math.isfinite(raw)


def _decimals(raw: float) -> Any:
    value = round(float(raw), _DECIMALS)
    return int(value) if value.is_integer() else value


def _viewport(col: Dict[str, Any], names: Sequence[str]) -> bool:
    """True when a collection's modes are viewport tiers: every mode is
    named for one (Mobile, Tablet, SM, LG), or the collection is named for
    viewports (Breakpoints, Devices)."""
    if len(names) < 2:
        return False
    return bool(words(str(col.get("name", ""))) & VIEWPORT_COLLECTIONS) \
        or all(words(n) & VIEWPORT_WORDS for n in names)


def _modes_of(col: Dict[str, Any]) -> Tuple[Dict[str, str], Optional[str]]:
    modes = {str(m.get("modeId")): str(m.get("name", "")) for m in col.get("modes") or []
             if isinstance(m, dict)}
    default = col.get("defaultModeId")
    if default not in modes:
        default = next(iter(modes), None)
    return modes, default


def _plan(col: Dict[str, Any], want: Optional[str],
          axes: Dict[str, Tuple[str, str]]) -> _Plan:
    """How one collection is read, given the second mode second_modes names
    for it (or None) and the axes the collections before it made."""
    cname = str(col.get("name", ""))
    modes, default = _modes_of(col)
    if default is None:
        return _Plan(cname, modes, [])
    names = list(modes.values())
    others = [m for m in modes if m != default]
    base_only = _Plan(cname, modes, [(default, "")])
    if not others:
        return base_only
    if _viewport(col, names):
        # A viewport is never a mode axis: the default tier is the value,
        # and the other tiers are named in one note once they are read.
        return _Plan(cname, modes, [(default, "")], tiers=others)
    if len(modes) > 2 and want is None:
        # Suggest the mode that makes a known axis with the default, if one does.
        example = next((m for m in others if _known_axis(modes[default], modes[m], cname)),
                       others[0])
        rest = [modes[m] for m in others]
        base_only.note = (f"has the modes {_and(names)}; its default mode {modes[default]} was "
                          f"read, and {_and(rest)} were not, since a mode axis holds two "
                          "values; pass the second mode to read with second_modes, for "
                          f"example {json.dumps({cname: modes[example]})}")
        return base_only
    if len(modes) > 2:
        other = next((m for m in others if modes[m] == want), None)
        if other is None:
            folded = [m for m in others if modes[m].lower() == str(want).lower()]
            other = folded[0] if len(folded) == 1 else None
        if other is None:
            fix = _or([modes[m] for m in others])
            if want == modes[default]:
                raise InputError(f"second_modes names {want}, the default mode of {cname}, "
                                 f"which is read as the base already; pass {fix}")
            raise InputError(f"second_modes names the mode {want} of {cname}, which has the "
                             f"modes {_and(names)}; pass {fix}, a mode other than its default "
                             f"{modes[default]}")
    else:
        other = others[0]
    left = [modes[m] for m in others if m != other]
    unread = f"; {_and(left)} {'was' if len(left) == 1 else 'were'} not read" if left else ""
    known = _known_axis(modes[default], modes[other], cname)
    if known is not None:
        axis, default_is_base = known
        base, second = (default, other) if default_is_base else (other, default)
        value = AXES[axis][1]
        note = (f"has the modes {_and(names)}, read as the {axis} axis: {modes[base]} is the "
                f"base and {modes[second]} is {axis}:{value}{unread}")
        if not default_is_base:
            note += (f"; the default mode in Figma is {modes[default]}, and the engine's base "
                     f"is the {AXES[axis][0]} one")
        return _Plan(cname, modes, [(base, ""), (second, f"{axis}:{value}")],
                     (axis, (AXES[axis][0], value)), note)
    first, second = _slug(modes[default]), _slug(modes[other])
    axis = f"{first}-{second}"
    if not (_AXIS_WORD.fullmatch(first) and _AXIS_WORD.fullmatch(second)) or first == second:
        base_only.note = (f"has the modes {_and(names)}, which cannot name a mode axis; its "
                          f"default mode {modes[default]} was read and {modes[other]} was not; "
                          "rename the modes in Figma so each starts with a letter and the two "
                          "differ")
        return base_only
    if axes.get(axis, (first, second)) != (first, second):
        base_only.note = (f"has the modes {_and(names)}, which name the axis {axis} that "
                          f"another collection names with other modes; its default mode "
                          f"{modes[default]} was read and {modes[other]} was not; rename the "
                          "modes in one of the two collections in Figma")
        return base_only
    note = (f"has the modes {_and(names)}, read as the axis {axis}: {modes[default]}, its "
            f"default mode, is the base and {modes[other]} is {axis}:{second}{unread}")
    return _Plan(cname, modes, [(default, ""), (other, f"{axis}:{second}")],
                 (axis, (first, second)), note)


def _wants(second_modes: Any, collections: Dict[str, Any]) -> Dict[str, str]:
    """second_modes checked against the export: collection name to mode
    name, each naming a collection with more than two modes."""
    if not second_modes:
        return {}
    if not isinstance(second_modes, Mapping) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in second_modes.items()):
        raise InputError('second_modes maps a collection name to a mode name, for example '
                         '{"Type": "SM"}; pass it in that form')
    counts: Dict[str, int] = {}
    library = set()
    tiers: Dict[str, List[str]] = {}
    for col in collections.values():
        if isinstance(col, dict) and col.get("remote") is True:
            library.add(str(col.get("name", "")))
        elif isinstance(col, dict):
            names = list(_modes_of(col)[0].values())
            counts.setdefault(str(col.get("name", "")), len(names))
            if _viewport(col, names):
                tiers.setdefault(str(col.get("name", "")), names)
    large = [n for n, c in counts.items() if c > 2 and n not in tiers]
    for cname in second_modes:
        if cname in library and cname not in counts:
            raise InputError(f"second_modes names {cname}, a library collection from another "
                             "file, whose variables are not read as this file's tokens; leave "
                             f"{cname} out of second_modes")
        if cname in tiers:
            raise InputError(f"second_modes names {cname}, whose modes {_and(tiers[cname])} are "
                             "viewport tiers, not a mode axis; its default tier is read and the "
                             "engine sets per-tier values itself, so leave "
                             f"{cname} out of second_modes")
        if cname not in counts:
            fix = (f"pass a collection with more than two modes: {_or(large)}" if large else
                   "this export has no collection with more than two modes, so leave "
                   "second_modes out")
            raise InputError(f"second_modes names the collection {cname}, which this export "
                             f"does not hold; {fix}")
        if counts[cname] <= 2:
            n = counts[cname]
            raise InputError(f"second_modes names {cname}, which has {n} mode"
                             f"{'' if n == 1 else 's'}, so every mode it has is read already; "
                             f"leave {cname} out of second_modes")
    return dict(second_modes)


def _kind(v: Dict[str, Any]) -> Tuple[Optional[str], str]:
    """(token type, a note holding {value}) for a variable, or (None, why
    it is not read and the fix)."""
    resolved = v.get("resolvedType")
    scopes = [str(s) for s in v.get("scopes") or []]
    if resolved == "COLOR":
        return "color", ""
    if resolved == "FLOAT":
        if scopes == ["FONT_WEIGHT"]:
            return "fontWeight", ""
        if scopes and all(s in SIZE_SCOPES for s in scopes):
            return "dimension", ""
        if scopes == ["OPACITY"]:
            return "number", ("is scoped to OPACITY, which Figma writes from 0 to 100, so it was "
                              "read as {value}; divide it by 100 where a value from 0 to 1 is "
                              "wanted")
        if not scopes or "ALL_SCOPES" in scopes:
            return "number", ("has no scope that fixes its unit, so it was read as {value}; "
                              "give it a scope in Figma (Gap, Corner radius, Font size and so "
                              "on) to read it as a size")
        return "number", (f"has the scopes {_and(scopes)}, which do not share one unit, so it "
                          "was read as {value}; keep only size scopes in Figma to read it as a "
                          "size")
    if resolved == "STRING":
        if scopes == ["FONT_FAMILY"]:
            return "fontFamily", ""
        return None, (f"a text variable scoped to {_and(scopes) if scopes else 'nothing'}; the "
                      "engine reads text only as a font family, so if it names a font, give it "
                      "only the Font family scope in Figma")
    if resolved == "BOOLEAN":
        return None, ("a boolean, and the engine holds no boolean tokens; keep it in Figma, "
                      "where it switches components")
    return None, (f"has the type {json.dumps(resolved)}, which Figma variables do not have; "
                  "export the variables again")


def _literal(kind: str, raw: Any, at: str) -> Tuple[Any, Optional[Tuple[str, str, float]]]:
    """(the engine literal, and for a color outside sRGB (the channels as
    written, the hex, the distance)) for one mode's value. Raises _Bad."""
    if kind == "color":
        channels = [raw.get(k) for k in "rgb"] if isinstance(raw, dict) else []
        if len(channels) != 3 or not all(_number(c) for c in channels):
            raise _Bad(f"holds {json.dumps(raw)} in {at}, not a color; Figma writes a color as "
                       "r, g, b and a from 0 to 1, so export the variables again")
        alpha = raw.get("a", 1)
        if not _number(alpha):
            raise _Bad(f"holds {json.dumps(raw)} in {at}, not a color; Figma writes a color as "
                       "r, g, b and a from 0 to 1, so export the variables again")
        if not 0 <= alpha <= 1:
            raise _Bad(f"has the alpha {alpha} in {at}; Figma writes alpha from 0 to 1, so set "
                       "it again in Figma")
        suffix = "" if alpha >= 1 else f"{round(alpha * 255):02X}"
        if all(0 <= c <= 1 for c in channels):
            return rgb_to_hex(tuple(c * 255 for c in channels)) + suffix, None
        hx, distance, was_mapped = gamut_map_oklch(*srgb_to_oklch(*channels))
        written = json.dumps(dict(zip("rgb", channels)))
        return hx + suffix, ((written, hx + suffix, distance) if was_mapped else None)
    if kind == "fontFamily":
        if not (isinstance(raw, str) and raw.strip()):
            raise _Bad(f"holds {json.dumps(raw)} in {at}, not a font name; export the variables "
                       "again")
        return [raw.strip()], None
    if not _number(raw):
        raise _Bad(f"holds {json.dumps(raw)} in {at}, not a number; export the variables again")
    value = _decimals(raw)
    return ({"value": value, "unit": "px"} if kind == "dimension" else value), None


def _document(text: str, source: Source) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """(variables, variableCollections) of an export. Raises InputError."""
    try:
        doc = json.loads(text)
    except ValueError as exc:
        raise InputError(f"{source.path} is not valid JSON ({exc}); export the variables again "
                         f"with {REST_ENDPOINT}") from None
    if isinstance(doc, dict) and doc.get("error") is True and "meta" not in doc \
            and "variables" not in doc:
        raise InputError(f"{source.path} is an error Figma sent back ({doc.get('status')}: "
                         f"{doc.get('message')}), not a variables export; export again with a "
                         f"token that can read the file, from {REST_ENDPOINT}")
    data = doc.get("meta", doc) if isinstance(doc, dict) else None
    if not (isinstance(data, dict) and isinstance(data.get("variables"), dict)
            and isinstance(data.get("variableCollections"), dict)):
        raise InputError(f"{source.path} is not a Figma variables export: it has no variables "
                         f"and variableCollections; export them with the Figma REST endpoint "
                         f"{REST_ENDPOINT}")
    return data["variables"], data["variableCollections"]


def import_figma(text: str, source: Source,
                 second_modes: Optional[Mapping[str, str]] = None) -> Imported:
    """The variables a Figma export holds, as tokens in the file's names,
    and the report. `second_modes` maps a collection with more than two
    modes to the mode read beside its default."""
    name = Path(source.path).name
    variables, collections = _document(text, source)
    wants = _wants(second_modes, collections)

    axes: Dict[str, Tuple[str, str]] = {}
    plans: Dict[str, _Plan] = {}
    for cid, col in collections.items():
        if not isinstance(col, dict):
            continue
        if col.get("remote") is True:
            # A library collection another file owns: no axis, no mode note.
            plans[cid] = _Plan(str(col.get("name", "")), _modes_of(col)[0], [], remote=True)
            continue
        plan = _plan(col, wants.get(str(col.get("name", ""))), axes)
        if plan.axis is not None:
            axes.setdefault(*plan.axis)
        plans[cid] = plan

    order = list(dict.fromkeys(
        [v for col in collections.values() if isinstance(col, dict)
         for v in col.get("variableIds") or [] if v in variables] + list(variables)))
    position = {vid: n for n, vid in enumerate(order)}
    # (position, 0 for a collection's note and 1 for a variable's, item)
    col_notes: List[Tuple[int, int, Item]] = []
    noted: set = set()
    not_read: List[Tuple[int, Item]] = []
    entries: Dict[str, _Entry] = {}
    # Library variables the export holds: id -> (name, library collection).
    library: Dict[str, Tuple[str, str]] = {}
    # A viewport collection's first variable, where its note sits.
    first: Dict[Any, int] = {}
    used: Dict[Any, int] = {}
    library_note: Dict[Any, int] = {}

    for vid in order:
        v = variables[vid]
        if not isinstance(v, dict):
            not_read.append((position[vid], Item(name, vid, "is not a variable "
                                                 "object; export the variables again")))
            continue
        vname = str(v.get("name") or vid)
        cid = v.get("variableCollectionId")
        plan = plans.get(cid)
        cname = plan.name if plan is not None else str(cid)
        if v.get("remote") is True or (plan is not None and plan.remote):
            if plan is None:
                # Its collection is not in the export: named by its own name.
                library[vid] = (vname, "")
                col_notes.append((position[vid], 0, Item(name, vname,
                                                         _UNKNOWN_LIBRARY)))
                continue
            library[vid] = (vname, cname)
            if ("library", cid) not in noted:
                noted.add(("library", cid))
                library_note[cid] = len(col_notes)
                col_notes.append((position[vid], 0, Item(name, cname, "")))
            used[cid] = used.get(cid, 0) + 1
            continue
        where = f"{name} {cname}"
        if plan is not None and plan.note and cid not in noted:
            noted.add(cid)
            col_notes.append((position[vid], 0, Item(name, cname, plan.note)))
        first.setdefault(cid, position[vid])
        try:
            entries[vid] = _read(v, vname, where, plan, cid)
        except _Bad as exc:
            not_read.append((position[vid], Item(where, vname, str(exc))))
    for cid, plan in plans.items():
        if plan.tiers:
            found = [e for e in entries.values() if e.collection == cid]
            col_notes.append((first.get(cid, len(order)), 0,
                              Item(name, plan.name, _tier_note(plan, found, variables))))
        if plan.note and cid not in noted:
            col_notes.append((len(order), 0, Item(name, plan.name, plan.note)))
    # A library collection's note, with the count of its variables here,
    # counted by collection id: two libraries may share a name.
    for cid, at in library_note.items():
        p, k, i = col_notes[at]
        col_notes[at] = (p, k, Item(i.where, i.name, _library_note(used[cid])))

    snapshots = _snapshots(library, variables, collections)
    while True:
        _check_aliases(entries, variables, library, snapshots, position, not_read)
        if not _drop_repeated_paths(entries, position, not_read):
            break

    ts = TokenSet(axes)
    notes = list(col_notes)
    renamed: List[Tuple[int, Item]] = []
    mapped: List[Tuple[int, Mapped]] = []
    for vid, e in entries.items():
        written = {ctx: ("{" + entries[r.id].path + "}" if isinstance(r, _Ref) else r)
                   for ctx, r in e.values.items()}
        base = written.pop("")
        modes = {ctx: val for ctx, val in written.items() if val != base}
        aliased = any(isinstance(r, _Ref) for r in e.values.values())
        ts.add(Token(e.path, e.kind, base, modes=modes,
                     layer="semantic" if aliased or modes else "primitive",
                     description=e.description))
        notes += [(position[vid], 1, i) for i in e.notes + _type_notes(e, entries)]
        renamed += [(position[vid], i) for i in e.renamed]
        mapped += [(position[vid], m) for m in e.mapped]
    report = ImportReport.of(source, ts, entries=len(variables) - len(library))
    report.notes = [i for _, _, i in sorted(notes, key=lambda n: n[:2])]
    report.renamed = [i for _, i in renamed]
    report.mapped = [m for _, m in mapped]
    report.not_read = [i for _, i in sorted(not_read, key=lambda n: n[0])]
    return Imported(ts, report)


_UNKNOWN_COLLECTION = "an unknown library collection"
_UNKNOWN_LIBRARY = (f"is a variable of {_UNKNOWN_COLLECTION} (remote in the export, and its "
                    "collection is not in it); it was not read as this file's token; import "
                    "that library's own export to read it")


def _library_note(count: int) -> str:
    held = "1 variable of it" if count == 1 else f"{count} variables of it"
    return (f"is a library collection from another file (remote in the export); the "
            f"{held} this file uses {'was' if count == 1 else 'were'} not read as this file's "
            "tokens; import that library's own export to read them")


def _read(v: Dict[str, Any], vname: str, where: str, plan: Optional[_Plan],
          cid: Any) -> _Entry:
    """One variable read, its aliases and its path not yet checked. Raises
    _Bad."""
    if plan is None:
        raise _Bad(f"names the collection {cid}, which this export does not hold; export the "
                   "variables again")
    if v.get("deletedButReferenced"):
        raise _Bad("was deleted in Figma and is kept only because something still references "
                   "it; restore it, or point those references at another variable")
    kind, why = _kind(v)
    if kind is None:
        raise _Bad(why)
    if not plan.read:
        raise _Bad(f"sits in {plan.name}, which has no modes; export the variables again")
    path = ".".join(_BAD.sub("-", s).strip("-") or "_" for s in vname.split("/"))
    by_mode = v.get("valuesByMode") if isinstance(v.get("valuesByMode"), dict) else {}
    entry = _Entry(where, vname, path, kind, {}, str(v.get("description") or ""),
                   label=f"{plan.name}/{vname}", collection=cid)
    for mode_id, ctx in plan.read:
        at = f"the mode {plan.modes[mode_id]} of {plan.name}"
        entry.at[ctx] = at
        raw = by_mode.get(mode_id)
        if raw is None:
            raise _Bad(f"has no value for {at}; set one in Figma and export again")
        if isinstance(raw, dict) and raw.get("type") == "VARIABLE_ALIAS":
            entry.values[ctx] = _Ref(str(raw.get("id")), _resolved(v, mode_id, raw))
            continue
        value, outside = _literal(kind, raw, at)
        entry.values[ctx] = value
        if outside is not None:
            # With more than one mode read, the report says which one was mapped.
            spot = f"{where} in the mode {plan.modes[mode_id]}" if len(plan.read) > 1 else where
            entry.mapped.append(Mapped(spot, vname, *outside))
    base_raw = by_mode.get(plan.read[0][0])
    for mode_id in plan.tiers:
        raw = by_mode.get(mode_id)
        if raw is not None and raw != base_raw:
            entry.tiers[plan.modes[mode_id]] = raw
    if path != vname.replace("/", "."):
        entry.renamed.append(Item(where, vname, f"read as {path}; a slash reads as a dot, and a "
                                  "path segment holds only letters, digits, '_' and '-'"))
    if why:
        base = entry.values[""]
        shown = "a plain number" if isinstance(base, _Ref) else f"the plain number {base}"
        entry.notes.append(Item(where, vname, why.format(value=shown)))
    return entry


def _resolved(v: Dict[str, Any], mode_id: str, raw: Dict[str, Any]) -> Any:
    """The value an export resolved an alias to, when it holds one: the
    alias's own resolvedValue, or the variable's resolvedValuesByMode."""
    if "resolvedValue" in raw:
        return raw["resolvedValue"]
    table = v.get("resolvedValuesByMode")
    got = table.get(mode_id) if isinstance(table, dict) else None
    if isinstance(got, dict) and "resolvedValue" in got:
        return got["resolvedValue"]
    if got is None or (isinstance(got, dict) and got.get("type") == "VARIABLE_ALIAS"):
        return None
    return got


def _snapshots(library: Dict[str, Tuple[str, str]], variables: Dict[str, Any],
               collections: Dict[str, Any]) -> Dict[str, Tuple[Any, str]]:
    """Each library variable whose value the export holds: id -> (the value
    in its collection's default mode, that mode's name when the collection
    has more than one). With its collection missing, a value is held only
    when every mode has the same one. An alias inside the library is not a
    value."""
    out: Dict[str, Tuple[Any, str]] = {}
    for vid in library:
        v = variables.get(vid)
        by_mode = v.get("valuesByMode") if isinstance(v, dict) else None
        if not isinstance(by_mode, dict) or not by_mode:
            continue
        col = collections.get(v.get("variableCollectionId"))
        if isinstance(col, dict):
            modes, default = _modes_of(col)
            raw, mode = by_mode.get(default), (modes.get(default, "") if len(modes) > 1 else "")
        else:
            values = list(by_mode.values())
            raw = values[0] if all(x == values[0] for x in values) else None
            mode = ""
        if raw is not None and not (isinstance(raw, dict) and raw.get("type") == "VARIABLE_ALIAS"):
            out[vid] = (raw, mode)
    return out


def _show(value: Any) -> str:
    """A literal as a person reads it: #FFFFFF, 16px, 600, Inter."""
    if isinstance(value, dict) and set(value) == {"value", "unit"}:
        return f"{value['value']}{value['unit']}"
    if isinstance(value, list):
        return ", ".join(str(x) for x in value)
    return str(value)


_FEW = 3


def _tier_note(plan: _Plan, found: List[_Entry], variables: Dict[str, Any]) -> str:
    """The one note on a viewport collection: its tiers, the default one
    read, and each other tier's values where they differ."""
    names = list(plan.modes.values())
    default = plan.modes[plan.read[0][0]]
    rest = [plan.modes[m] for m in plan.tiers]
    note = (f"has the modes {_and(names)}, which are viewport tiers, not a mode axis: its "
            f"default tier {default} was read as each variable's value, and "
            f"{_and(rest)} {'was' if len(rest) == 1 else 'were'} not read")

    def shown(e: _Entry, raw: Any) -> str:
        if isinstance(raw, dict) and raw.get("type") == "VARIABLE_ALIAS":
            target = variables.get(str(raw.get("id")))
            return str(target.get("name")) if isinstance(target, dict) else str(raw.get("id"))
        try:
            return _show(_literal(e.kind, raw, "")[0])
        except _Bad:
            return json.dumps(raw)

    differ = [e for e in found if e.tiers]
    if differ:
        parts = [f"{e.name} is " + _and([f"{shown(e, raw)} at {tier}"
                                         for tier, raw in e.tiers.items()])
                 for e in differ[:_FEW]]
        more = len(differ) - _FEW
        tail = f", and {more} more variable{'s' if more > 1 else ''} differ" if more > 0 else ""
        note += f" ({'; '.join(parts)}{tail})"
    else:
        note += " (they hold the same values)"
    return note + "; the engine sets per-tier values itself, so there is nothing to pass for them"


def _check_aliases(entries: Dict[str, _Entry], variables: Dict[str, Any],
                   library: Dict[str, Tuple[str, str]],
                   snapshots: Dict[str, Tuple[Any, str]], position: Dict[str, int],
                   not_read: List[Tuple[int, Item]]) -> None:
    """Drop every entry whose alias points outside what was read (another
    file's variable, or one not read), or runs in a loop, until what is
    left holds together. An alias to a library variable whose value the
    export holds reads that value, with a note that it is a snapshot. Each
    message names the mode and the fix."""
    def drop(vid: str, why: str) -> None:
        e = entries.pop(vid)
        not_read.append((position[vid], Item(e.where, e.name, why)))

    def label(vid: str) -> str:
        v = variables.get(vid)
        return str(v.get("name") or vid) if isinstance(v, dict) else vid

    contexts = sorted({c for e in entries.values() for c in e.values})
    while True:
        changed = False
        for vid, e in list(entries.items()):
            gone = next(((ctx, r.id) for ctx, r in e.values.items()
                         if isinstance(r, _Ref) and r.id not in entries), None)
            if gone is None:
                continue
            ctx, target = gone
            at = e.at.get(ctx, "")
            ref = e.values[ctx]
            if target in variables and target not in library:
                drop(vid, f"references {label(target)} in {at}, which was not read; fix "
                          f"{label(target)} and import again")
                changed = True
                continue
            # A variable of another file: read its value when the export
            # holds one, as a snapshot; otherwise say what the owner can do.
            if target in library:
                tname, cname = library[target]
                which = f"the library collection {cname}" if cname else _UNKNOWN_COLLECTION
                origin = f"a variable of {which} in another file"
            else:
                tname, origin = target, "a variable from another file"
            snap = (ref.resolved, "") if isinstance(ref, _Ref) and ref.resolved is not None \
                else snapshots.get(target)
            if snap is None and target in library:
                drop(vid, f"references {tname} in {at}, {origin}, and the export holds no "
                          "value for it; detach the variable in Figma to keep its value here, "
                          "publish the library so the export carries its values, or export "
                          "the library and import it on its own")
            elif snap is None:
                drop(vid, f"references {target} in {at}, a variable from another file that "
                          "this export does not hold; detach the variable in Figma to keep its "
                          "value here, or export that library and import it on its own")
            else:
                try:
                    value, outside = _literal(e.kind, snap[0], at)
                except _Bad as exc:
                    drop(vid, f"references {tname} in {at}, {origin}, whose value in the export "
                              f"cannot be read: it {exc}")
                else:
                    e.values[ctx] = value
                    if outside is not None:
                        e.mapped.append(Mapped(e.where, e.name, *outside))
                    mode = f" in its mode {snap[1]}" if snap[1] else ""
                    e.notes.append(Item(e.where, e.name, (
                        f"aliases {tname} in {at}, {origin}; the export holds its value{mode}, "
                        f"so it was read as {_show(value)}, a snapshot that does not follow "
                        "later changes to the library; to keep the link, export the library "
                        "and import it on its own")))
            changed = True
        if changed:
            continue
        looped: Dict[str, Tuple[List[str], str]] = {}
        for ctx in contexts:
            def succ(vid: str, ctx: str = ctx) -> List[str]:
                values = entries[vid].values
                r = values.get(ctx, values[""])
                return [r.id] if isinstance(r, _Ref) and r.id in entries else []
            for vid, loop in cycles(list(entries), succ).items():
                looped.setdefault(vid, (loop, ctx))
        if not looped:
            return
        for vid, (loop, ctx) in looped.items():
            names = [label(x) for x in loop]
            at = entries[vid].at.get(ctx, entries[vid].at[""])
            drop(vid, f"references {names[1]} in {at}, which leads back to it "
                      f"({' -> '.join(names)}); point one of them at a value in Figma")


def _drop_repeated_paths(entries: Dict[str, _Entry], position: Dict[str, int],
                         not_read: List[Tuple[int, Item]]) -> bool:
    """Drop every entry on a path an earlier entry holds; True when one was
    dropped, so the aliases to it are checked again."""
    seen: Dict[str, _Entry] = {}
    dropped = False
    for vid in sorted(entries, key=position.__getitem__):
        e = entries[vid]
        first = seen.setdefault(e.path, e)
        if first is not e:
            not_read.append((position[vid], Item(e.where, e.name, (
                f"is read as {e.path}, the path of {first.label} read earlier; rename one of the "
                "two in Figma"))))
            del entries[vid]
            dropped = True
    return dropped


def _type_notes(e: _Entry, entries: Dict[str, _Entry]) -> List[Item]:
    """A note for each alias whose target was read as another type, with
    the fix in Figma: a size that aliases a number with no size scope is
    the usual case."""
    out: List[Item] = []
    # target id -> the modes that alias it
    ats: Dict[str, List[str]] = {}
    for ctx, r in e.values.items():
        if isinstance(r, _Ref) and entries[r.id].kind != e.kind:
            ats.setdefault(r.id, []).append(e.at.get(ctx, ""))
    for tid, where in ats.items():
        target = entries[tid]
        at = _and(where)
        if target.kind == "number" and e.kind == "dimension":
            fix = (f"give {target.name} a size scope in Figma (Gap, Corner radius, Font size and "
                   "so on) and import again")
        elif target.kind == "number" and e.kind == "fontWeight":
            fix = f"give {target.name} only the Font weight scope in Figma and import again"
        else:
            fix = f"give {target.name} the same scopes as {e.name} in Figma and import again"
        message = (f"aliases {target.name} in {at}, which was read as a {target.kind}, where a "
                   f"{e.kind} is wanted; {fix}")
        out.append(Item(e.where, e.name, message))
    return out


def read_figma(path: Any, label: str = "--from",
               second_modes: Optional[Mapping[str, str]] = None) -> Imported:
    """Read and import a Figma variables export. Errors name `label`."""
    source, text = read_source(path, "figma", label)
    try:
        return import_figma(text, source, second_modes)
    except InputError as exc:
        message = str(exc)
        if message.startswith(source.path):
            message = f"{label} {message}"
        raise InputError(message) from None
