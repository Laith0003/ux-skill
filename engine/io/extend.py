"""extend: add to an imported system without changing what it has.

Three kinds of addition:
- a foundation, generated from the axes (and the brand color, for color)
  in the engine's own role names; a foundation that aliases another's
  steps (layout aliases space) brings only the steps it points at, and a
  role the mapping already sends to one of the system's tokens is not
  added again: what points at it points at the system's token; a role
  the owner keeps out with a "not mapped" entry gets no token, nor does
  anything that points at it;
- a role, pointed at one of the system's own tokens (color.focus.ring at
  brand-700), which the mapping then records;
- a contract, bound through the mapping and copied into contracts/.

A token the system already has is never changed: an added token that the
system holds with another value blocks the extension, and so does one
named like an entry the import did not read, since the extension would
replace it. A stylesheet is compared by the custom properties each token
writes, so --space-4 is the same entry whether it came in as space-4 or
is added as space.4. Mode switches follow the mapping, so an added token
varies on the system's own dark switch when scheme is mapped to it; an
engine axis the mapping does not name is added as the engine writes it.

Where the result goes. A system the engine did not write is never
rewritten: the additions go in an extension file beside it, in its own
format and naming, stamped as the engine's (a stylesheet carries the
digest in its opening comment; the intake step records every file it
writes), and the report says how to load it:
- a stylesheet gets theme-ext.css, loaded after theme.css, with the
  additions on :root and each mode in the stylesheet's own selectors;
- a Tailwind 4 theme gets app-ext.css with an @theme block of its own
  (tailwind_out.tailwind_extension);
- a tokens file gets tokens-ext.json, whose tokens alias the source's;
- markdown rule files and a Tailwind 3 theme, which the engine does not
  write, get tokens-ext.json, each token holding its own value;
- a Figma export gets variables-ext.json and the script that applies it
  (figma_out.figma_extension).
An extension file already beside the source is read first: what it added
is kept, counted as part of the system, and the new additions follow it.
Where the source now sets a name the earlier extension sets too, with
another value, the extension would replace the owner's value, so that
blocks with the fix. A Figma extension is read as the file will be once
its script runs, so a mapping that names what it adds still holds before
the owner exports again; the variables of it the file does not have yet
are kept, first, and the ones the file has now are left as it has them.
A role the mapping sends to a name the system declares in a form the
import could not read (calc(), clamp()) blocks with that value and the
fix: write it in a form the import reads, or map the role elsewhere.
Only the engine's own system, known from the record of the files it wrote
(Imported.owned, never token names), is rewritten in place, and only when
the import read every entry of it; otherwise it is extended like any
other, and a Figma export never is: Figma holds its variables.
write_extended() writes either through the intake step, the files that
belong beside the source there and the rest into another folder when one
is named; both folders are checked before anything is written, and a
second write that fails puts the first back.

The result is checked through the same view and gate enhance uses; the
Check section says how many roles are mapped per foundation, or that
nothing was measured. The system as it was is checked in the same
contexts, under every axis the additions bring, so what it had before is
never taken for what they caused. What the extension adds that fails,
and every addition problem, blocks it, each with a fix the owner can
take (map the role to one of their tokens, or leave the foundation out);
findings that were there before are listed apart, and so are findings
on the system's own tokens in a mode only the additions bring, which it
was never measured in. A blocked result gives only its report.

A foundation is generated for the brief's audience as a system build is
(body size, targets, the ring, the measure, the scripts), and the report
says what each field changed and which words were not read. An extension
that adds faces writes fonts.css and fonts-self-host.css beside the
system, as a build does, so the faces load with their fallbacks. It
writes no art: the art files belong to a system the engine builds.
"""
from __future__ import annotations

import dataclasses
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple
from typing import Mapping as Mapping_

from engine.contracts.bind import validate_contracts
from engine.contracts.schema import ContractError, load_contract
from engine.existing import stamp_digest
from engine.foundations.audience import Audience, effects
from engine.foundations.build import FOUNDATIONS, SystemCheck, build_system
from engine.foundations.errors import InputError
from engine.foundations.export import dump_dtcg, from_dtcg, to_css
from engine.foundations.fonts import faces_in, fonts_css, self_host_css
from engine.foundations.gate import GateFailure
from engine.foundations.modes import AXES, ModeError, compress, contexts, join, parse, select
from engine.foundations.tokens import (
    AliasError, Token, TokenSet, alias_target, css_property, is_alias)
from engine.foundations.validate import validate
from engine.foundations.values import TYPOGRAPHY_FIELDS, css_entries
from engine.io.adapter import ROLE_TYPES, AxisMap, Mapping, RoleMap, dump_mapping, view
from engine.io.css_in import import_css
from engine.io.enhance import enhance
from engine.io.figma_out import (
    EXTENSION_HEAD, apply_script, extension_names, figma_extension, figma_files)
from engine.io.figma_in import import_figma
from engine.io.intake import INTAKE_DIR, write_with_intake
from engine.io.report import Imported, read_source
from engine.io.scan import canonical
from engine.io.tailwind_in import import_tailwind_css
from engine.io.tailwind_out import (
    extension_name, tailwind_extension, to_tailwind, unread_properties)
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)
_NAMES = [f.name for f in FOUNDATIONS]
# Formats written as a stylesheet, where a token is the properties it writes.
_STYLESHEETS = ("css", "tailwind")
# Formats the engine does not write; their extension is a tokens file.
_READ_ONLY = {"markdown": "markdown rule files", "tailwind-json": "a Tailwind 3 theme"}
_TOKENS_EXT = "tokens-ext.json"
_NOT_MAPPED = '{"token": null, "by": "owner"}'


@dataclass
class Extended:
    """What extend made: the merged system in the source's names, the
    mapping with the additions, the paths added, the check of the result,
    what blocks it (empty when nothing does), the findings that were there
    before, the decisions it took, the files to write, the brief's words
    it did not read, the files that belong beside the source (the system
    or its extension file, and the font files), how to load an extension
    file ("" when the system is rewritten in place), and the findings on
    the system's own tokens in a mode only the additions bring (contrast
    high, say), which it was never measured in before."""
    tokens: TokenSet
    mapping: Mapping
    added: List[str]
    check: SystemCheck
    problems: List[str]
    existing: List[str]
    decisions: List[str]
    files: Dict[str, str] = field(default_factory=dict)
    unread: List[str] = field(default_factory=list)
    beside: List[str] = field(default_factory=list)
    load: str = ""
    unmeasured: List[str] = field(default_factory=list)


@dataclass
class _Earlier:
    """An extension file already beside the source: its name, the tokens
    it adds in the source's names, the text written for them (a
    stylesheet's body, without its opening comment), the properties or
    paths it declares that could not be read back, for a Figma
    extension its payload and the export as it will be once the payload
    is applied, and each place where it now replaces a value the source
    sets, with the fix."""
    name: str
    tokens: TokenSet
    body: str = ""
    unread: Dict[str, str] = field(default_factory=dict)
    payload: Optional[Dict[str, Any]] = None
    # (property, "unread" or "value", what the import said of the source's)
    clashes: List[Tuple[str, str, str]] = field(default_factory=list)
    combined: Optional[Imported] = None


def _refs(value: Any) -> List[str]:
    if isinstance(value, dict):
        return [r for v in value.values() for r in _refs(v)]
    if isinstance(value, list):
        return [r for v in value for r in _refs(v)]
    return [alias_target(value)] if is_alias(value) else []


def _sub(value: Any, rename: Callable[[str], str]) -> Any:
    """`value` with each alias renamed."""
    if isinstance(value, dict):
        return {k: _sub(v, rename) for k, v in value.items()}
    if isinstance(value, list):
        return [_sub(v, rename) for v in value]
    return "{" + rename(alias_target(value)) + "}" if is_alias(value) else value


def _copy(t: Token, path: Optional[str] = None, rename: Optional[Callable[[str], str]] = None,
          **changes: Any) -> Token:
    """A copy of a token, under another path or with its aliases renamed."""
    value, modes = t.value, dict(t.modes)
    if rename is not None:
        value = _sub(value, rename)
        modes = {k: _sub(v, rename) for k, v in modes.items()}
    fields = dict(value=value, modes=modes, layer=t.layer, description=t.description,
                  extensions=dict(t.extensions))
    fields.update(changes)
    return Token(path or t.path, t.type, **fields)


def _generated(names: Sequence[str], axes: AxisValues, brand: str,
               arabic: bool, audience: Audience) -> TokenSet:
    """The named foundations and the ones they need, in build order, for
    the brief's audience."""
    wanted = set(names)
    for f in FOUNDATIONS:
        if f.name in names:
            wanted |= set(f.requires)
    order = tuple(n for n in _NAMES if n in wanted)
    return build_system(axes, brand, arabic=arabic, foundations=order,
                        audience=audience).tokens


def _theirs(axis: str, mapping: Mapping) -> Tuple[str, Optional[AxisMap]]:
    """The system's own axis an engine axis is written on, and its map
    (None when the mapping does not read the axis from one of the
    system's)."""
    m = mapping.axes.get(axis)
    if m is None or m.source is None:
        return axis, None
    return m.source, m


def _translate(t: Token, mapping: Mapping, axes: Dict[str, Tuple[str, str]]) -> Token:
    """The token with its modes on the system's own axes where the mapping
    names them: each value placed in the system's context that the
    mapping reads as the engine's, so a mapping whose base is the other
    way round still gives each context its value."""
    if not t.modes:
        return _copy(t)
    ours = [a for a in AXES if any(a in parse(k, AXES) for k in t.modes)]
    names = [_theirs(a, mapping)[0] for a in ours]
    values: Dict[str, Any] = {}
    for ctx in contexts(names, axes):
        pairs = parse(ctx, axes)
        mine: Dict[str, str] = {}
        for a, name in zip(ours, names):
            m = _theirs(a, mapping)[1]
            v = pairs[name]
            mine[a] = v if m is None else next(o for o, x in m.values.items() if x == v)
        values[ctx] = select(t.value, t.modes, join(mine, AXES), AXES)[0]
    base, modes = compress(values, axes)
    return _copy(t, value=base, modes=modes)


def _written(t: Token) -> Dict[str, Dict[str, str]]:
    """The custom properties a token writes, each with its text per mode
    ("" the base)."""
    out: Dict[str, Dict[str, str]] = {}
    for key, value in [("", t.value), *t.modes.items()]:
        for prop, text in css_entries(t.path, t.type, value):
            out.setdefault(prop, {})[key] = text
    return out


def _shown_css(t: Token) -> str:
    """A token's base value as a stylesheet writes it."""
    return "; ".join(text for _, text in css_entries(t.path, t.type, t.value))


def _shown(ts: TokenSet, t: Token) -> str:
    """A token's value as a person reads it, resolved where it can be."""
    if t.type in ("dimension", "duration", "number", "color"):
        try:
            return canonical(t.type, ts.resolve(t.path))
        except (AliasError, ModeError):
            pass
    return str(t.value)


def _folder(imported: Imported) -> Path:
    """The folder an extension file is written to: the source's own."""
    return Path(imported.report.source.path).expanduser().parent


def _ext_names(imported: Imported) -> List[str]:
    """The extension files beside a source, the one to load or run first."""
    source = imported.report.source
    path = Path(source.path)
    if source.format in _READ_ONLY:
        return [_TOKENS_EXT]
    if source.format == "figma":
        data, script = extension_names(path)
        return [data, script]
    return [extension_name(path)]


def _in_place(imported: Imported) -> bool:
    """Whether the system is the engine's own and can be written back
    whole: the import read every entry of it and it is one file. A Figma
    export is never rewritten: Figma holds the variables, so an addition
    is always a script to run there."""
    report = imported.report
    if not imported.owned or report.source.format in _READ_ONLY \
            or report.source.format == "figma":
        return False
    if report.not_read or report.also_read:
        return False
    return not (report.source.format in _STYLESHEETS and unread_properties(imported))


def _unread(imported: Imported) -> Dict[str, str]:
    """Every name the source declares that the import did not make a
    token, with what the report says of it: custom properties for a
    stylesheet, paths for any other format."""
    if imported.report.source.format in _STYLESHEETS:
        return unread_properties(imported)
    out: Dict[str, str] = {}
    for item in imported.report.not_read:
        name = item.name.replace("/", ".")
        if name and not imported.tokens.has(name):
            out.setdefault(name, item.message)
    return out


def _body(text: str) -> str:
    """A stylesheet extension without the opening comment the engine
    wrote, which carries its digest; a file whose opening comment is not
    the engine's is kept whole."""
    if text.startswith("/*\n"):
        end = text.find("\n */\n")
        if end != -1 and "Written by ux-skill beside" in text[:end]:
            return text[end + len("\n */\n"):]
    return text


def _earlier(imported: Imported, name: str) -> Optional[_Earlier]:
    """The extension file already beside the source, read back, or None.
    Raises InputError naming the file and the fix when it cannot be read."""
    source = imported.report.source
    fmt = source.format
    path = _folder(imported) / name
    if not path.is_file():
        return None
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        reason = getattr(exc, "strerror", None) or "it is not UTF-8 text"
        raise InputError(f"{path} cannot be read ({reason}), so what an earlier extension added "
                         "cannot be kept; make it readable, or move it away to start the "
                         "extension again") from None
    if fmt in _STYLESHEETS:
        _, own = read_source(source.path, fmt, "the source")
        reader = import_tailwind_css if fmt == "tailwind" else import_css
        both = reader(own + "\n" + text, source)
        tokens = TokenSet(both.tokens.axes)
        for t in both.tokens.tokens():
            if not imported.tokens.has(t.path):
                tokens.add(t)
        before = unread_properties(imported)
        unread = {p: m for p, m in unread_properties(both).items() if p not in before}
        return _Earlier(name, tokens, _body(text), unread,
                        clashes=_sheet_clashes(imported, both, text))
    if fmt == "figma":
        try:
            payload = json.loads(text)
        except ValueError:
            payload = None
        if not isinstance(payload, dict) or not isinstance(payload.get("collections"), list):
            raise InputError(f"{path} is not the payload an earlier extension wrote, so what it "
                             "added cannot be kept; move it away to start the extension again")
        # What the file will hold once the owner runs the earlier script:
        # its own variables, and each the payload adds that it lacks.
        _, own = read_source(source.path, fmt, "the source")
        both = import_figma(_applied(own, payload), source)
        tokens = TokenSet(both.tokens.axes)
        for t in both.tokens.tokens():
            if not imported.tokens.has(t.path):
                tokens.add(t)
        return _Earlier(name, tokens, payload=payload, combined=both)
    try:
        tokens = from_dtcg(json.loads(text))
    except (ValueError, TypeError, KeyError) as exc:
        raise InputError(f"{path} cannot be read as the tokens file an earlier extension wrote "
                         f"({exc}), so what it added cannot be kept; move it away to start the "
                         "extension again") from None
    return _Earlier(name, tokens)


_DECLARED = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")


def _sheet_clashes(imported: Imported, both: Imported,
                   text: str) -> List[Tuple[str, str, str]]:
    """Each custom property an earlier stylesheet extension declares that
    the source now declares too with another value ("value"), or declares
    where the import did not read it ("unread", with what the import said):
    the extension loads after the source, so it would replace the owner's
    value."""
    own = {css_property(t.path): t for t in imported.tokens.tokens()}
    unread = unread_properties(imported)
    out: List[Tuple[str, str, str]] = []
    bare = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    for prop in dict.fromkeys(_DECLARED.findall(bare)):
        if prop in unread:
            out.append((prop, "unread", unread[prop]))
            continue
        mine = own.get(prop)
        if mine is None:
            continue
        seen = both.tokens.get(mine.path) if both.tokens.has(mine.path) else None
        if seen is None or (seen.type, seen.value, seen.modes) != (
                mine.type, mine.value, mine.modes):
            out.append((prop, "value", ""))
    return out


def _sent_to(mapping: Mapping, token: str) -> List[str]:
    """The roles the mapping sends to a token."""
    return [r for r, m in mapping.roles.items() if m.token == token]


def _unread_fix(key: str, where: str, roles: List[str], mapping_name: str) -> str:
    """The fix for a name the import could not read in `where`: write it in
    a form it reads, or, when the mapping sends roles to it, map them to
    another token."""
    fix = f"write {key} in {where} in a form the import reads"
    if roles:
        fix = (f"{mapping_name} sends {_and(roles)} to it, so {fix}, or map {_and(roles)} to "
               f"another of your tokens in {mapping_name}")
    return fix


def _applied(text: str, payload: Dict[str, Any]) -> str:
    """A Figma export as it will read once an extension's payload is
    applied to the file: each collection the payload names is the file's
    own by name, or a new one; each variable the file lacks is added with
    its values under the collection's mode ids and its aliases by id; a
    variable the file has keeps the file's values, as the apply script
    leaves it."""
    doc = json.loads(text)
    data = doc.get("meta", doc)
    collections = {cid: dict(c) for cid, c in data["variableCollections"].items()}
    variables = dict(data["variables"])
    by_name = {c.get("name"): cid for cid, c in collections.items()}
    ids = {f"{collections[v['variableCollectionId']].get('name')}:{v.get('name')}": vid
           for vid, v in variables.items() if v.get("variableCollectionId") in collections}
    n = 0
    for c in payload["collections"]:
        cid = by_name.get(c["name"])
        if cid is None:
            cid = f"VariableCollectionId:added:{len(collections) + 1}"
            modes = [{"modeId": f"{cid}:{i}", "name": m} for i, m in enumerate(c["modes"])]
            collections[cid] = {"id": cid, "name": c["name"], "modes": modes,
                                "defaultModeId": modes[0]["modeId"], "variableIds": [],
                                "hiddenFromPublishing": False, "remote": False}
            by_name[c["name"]] = cid
        collections[cid]["variableIds"] = list(collections[cid].get("variableIds", []))
        for v in c["variables"]:
            if f"{c['name']}:{v['name']}" not in ids:
                n += 1
                ids[f"{c['name']}:{v['name']}"] = f"VariableID:added:{n}"
    for c in payload["collections"]:
        cid = by_name[c["name"]]
        mode_id = {m["name"]: m["modeId"] for m in collections[cid]["modes"]}
        for v in c["variables"]:
            vid = ids[f"{c['name']}:{v['name']}"]
            if vid in variables:
                continue
            values: Dict[str, Any] = {}
            for mode, value in v["values"].items():
                if mode not in mode_id:
                    continue
                if isinstance(value, dict) and "alias" in value:
                    if value["alias"] not in ids:
                        continue
                    value = {"type": "VARIABLE_ALIAS", "id": ids[value["alias"]]}
                values[mode_id[mode]] = value
            variables[vid] = {"id": vid, "name": v["name"], "variableCollectionId": cid,
                              "resolvedType": v["type"], "valuesByMode": values,
                              "scopes": list(v.get("scopes", [])),
                              "description": v.get("description", ""),
                              "hiddenFromPublishing": v.get("hidden", False), "remote": False}
            collections[cid]["variableIds"].append(vid)
    body = {"variableCollections": collections, "variables": variables}
    whole = {**doc, "meta": {**doc["meta"], **body}} if "meta" in doc else {**doc, **body}
    return json.dumps(whole)


def _union(*axes: Any) -> Dict[str, Tuple[str, str]]:
    out: Dict[str, Tuple[str, str]] = {}
    for group in axes:
        for a, v in group.items():
            out.setdefault(a, tuple(v))
    return out


class _Held:
    """What the system holds, by the name a new token is compared on: a
    custom property for a stylesheet, a path otherwise; each with the
    token that holds it and the file it is in."""

    def __init__(self, sheet: bool) -> None:
        self.sheet = sheet
        self.by: Dict[str, Tuple[Token, str]] = {}

    def keys(self, t: Token) -> List[str]:
        return list(_written(t)) if self.sheet else [t.path]

    def add(self, t: Token, where: str) -> None:
        for k in self.keys(t):
            self.by.setdefault(k, (t, where))

    def same(self, t: Token) -> Optional[bool]:
        """True when the system holds `t` as it is, False when it holds a
        name of it with another value, None when it holds none of them."""
        held = [self.by[k] for k in self.keys(t) if k in self.by]
        if not held:
            return None
        if self.sheet:
            theirs: Dict[str, Dict[str, str]] = {}
            for old, _ in held:
                theirs.update(_written(old))
            mine = _written(t)
            return len(held) == len(mine) and all(theirs.get(p) == v for p, v in mine.items())
        old = held[0][0]
        return (old.type, old.value, old.modes) == (t.type, t.value, t.modes)


def extend(imported: Imported, mapping: Mapping, *, foundations: Sequence[str] = (),
           roles: Optional[Dict[str, str]] = None, contracts: Sequence[Any] = (),
           axes: AxisValues = NEUTRAL, axes_source: str = "every axis at 0.5",
           brand: str = "#3366FF", arabic: bool = True,
           audience: Optional[Audience] = None, unread: Sequence[str] = (),
           mapping_name: str = "mapping.json") -> Extended:
    """Extend an imported system (see the module docstring). `audience`
    holds the brief's structured fields and `unread` the brief's words the
    engine did not read (emit.brief_audience and emit.unread_lines);
    `mapping_name` is the mapping file the messages name. Raises
    InputError for an addition that cannot be made as asked."""
    roles = dict(roles or {})
    audience = audience or Audience()
    source = imported.report.source
    name = Path(source.path).name
    sheet = source.format in _STYLESHEETS
    for f in foundations:
        if f not in _NAMES:
            raise InputError(f"--add names {f}, which is not a foundation; use "
                             f"{', '.join(_NAMES[:-1])} or {_NAMES[-1]}")

    in_place = _in_place(imported)
    ext_names = [] if in_place else _ext_names(imported)
    earlier = None if in_place else _earlier(imported, ext_names[0])
    earlier_ts = earlier.tokens if earlier is not None else TokenSet({})
    base = TokenSet(_union(imported.tokens.axes, earlier_ts.axes))
    problems: List[str] = []
    for t in imported.tokens.tokens():
        base.add(t)
    for t in earlier_ts.tokens():
        if not base.has(t.path):
            base.add(t)
            continue
        old = base.get(t.path)
        if (old.type, old.value, old.modes) != (t.type, t.value, t.modes):
            problems.append(f"{t.path} is in {name} and in {earlier.name}, written by an "
                            f"earlier extension, with other values, so {earlier.name} "
                            f"replaces the value {name} sets; remove {t.path} from "
                            f"{earlier.name}, or from {name}")
    if earlier is not None:
        for prop, kind, why in earlier.clashes:
            if kind == "value":
                problems.append(f"{prop} is in {name} and in {earlier.name}, written by an "
                                f"earlier extension, with other values, so {earlier.name} "
                                f"replaces the value {name} sets; remove {prop} from "
                                f"{earlier.name}, or from {name}")
                continue
            roles_to = _sent_to(mapping, prop[2:])
            fix = (_unread_fix(prop, name, roles_to, mapping_name) if roles_to
                   else f"remove {prop} from {earlier.name}, or from {name}")
            problems.append(f"{prop} is declared in {name} as a value the import could not "
                            f"read ({why}), and in {earlier.name}, written by an earlier "
                            f"extension, which loads after {name} and replaces it; {fix}")
    _check_roles(roles, mapping, base, mapping_name)

    held = _Held(sheet)
    for t in imported.tokens.tokens():
        held.add(t, name)
    for t in earlier_ts.tokens():
        held.add(t, earlier.name)
    declared = {k: (name, m) for k, m in _unread(imported).items()}
    if earlier is not None:
        declared.update({k: (earlier.name, m) for k, m in earlier.unread.items()})

    # Roles the mapping sends to the system's own tokens: the foundation's
    # tokens for them are not added, and what points at them points there.
    played: Dict[str, str] = {}

    def named(path: str) -> str:
        """The name a token takes in the system: the system's token for a
        role it already plays, its own path, or in a stylesheet the name
        its property reads back as (space.control.gap comes back from
        theme-ext.css as space-control-gap), or the system's token that
        already writes that property."""
        if path in played:
            return played[path]
        if not sheet or base.has(path):
            return path
        key = css_property(path)
        return held.by[key][0].path if key in held.by else key[2:]

    def placed(where: str) -> str:
        return where if where == name else f"{where}, written by an earlier extension,"

    decisions: List[str] = []
    new_axes: Dict[str, Tuple[str, str]] = dict(base.axes)
    candidates: List[Tuple[Token, str]] = []   # (token in the engine's paths, where from)
    axis_trouble: List[str] = []
    generated = TokenSet()
    if foundations:
        try:
            generated = _generated(foundations, axes, brand, arabic, audience)
        except GateFailure as exc:
            problems += [line for line in str(exc).splitlines() if line]
        decisions.append(f"{', '.join(foundations)} was generated from {axes_source}"
                         + (f" and the brand color {brand}" if "color" in foundations else "")
                         + ("" if arabic else ", Latin only") + ".")
        decisions += [f"{e.line()}." for e in effects(audience, axes)]
        if "imagery" in foundations:
            decisions.append("No art was written: the art files (art/pattern.svg, "
                             "art/shapes.svg and art/gradient.svg) come with a system the "
                             "engine builds, so build one with uxskill system build to get "
                             "them.")
        wanted = [t for t in generated.tokens() if t.path.split(".", 1)[0] in foundations]
        played.update({t.path: str(mapping.roles[t.path].token) for t in wanted
                       if t.path in mapping.roles and mapping.roles[t.path].token is not None
                       and mapping.roles[t.path].token not in (t.path,
                                                               css_property(t.path)[2:])})
        if played:
            one = len(played) == 1
            decisions.append(f"{_and(list(played))} {'is' if one else 'are'} mapped in "
                             f"{mapping_name} to your {_and(list(played.values()))}, so the "
                             f"foundation did not add its own token{'' if one else 's'} for "
                             f"{'it' if one else 'them'}; its tokens that point at "
                             f"{'that role' if one else 'those roles'} point at yours.")
            wanted = [t for t in wanted if t.path not in played]
        kept = [t.path for t in wanted if t.path in mapping.roles
                and mapping.roles[t.path].token is None]
        if kept:
            # The owner's "not mapped" entry keeps the role out: no token is
            # added for it, nor for anything the foundation points at it.
            gone = set(kept)
            grew = True
            while grew:
                more = {t.path for t in wanted if t.path not in gone
                        and any(r in gone for v in [t.value, *t.modes.values()]
                                for r in _refs(v))}
                grew = bool(more)
                gone |= more
            after_them = [t.path for t in wanted if t.path in gone and t.path not in kept]
            one = len(kept) == 1
            line = (f"{_and(kept)} {'is' if one else 'are'} kept out in {mapping_name} with "
                    f"{_NOT_MAPPED}, so the foundation added no token for "
                    f"{'it' if one else 'them'}")
            if after_them:
                line += (f"; {_and([named(p) for p in after_them])} "
                         f"{'points' if len(after_them) == 1 else 'point'} at "
                         f"{'it' if one else 'them'} and "
                         f"{'was' if len(after_them) == 1 else 'were'} left out too")
            decisions.append(line + ".")
            wanted = [t for t in wanted if t.path not in gone]
        mine = {t.path for t in wanted}
        by_path = {t.path: t for t in generated.tokens()}
        todo = [r for t in wanted for v in [t.value, *t.modes.values()] for r in _refs(v)]
        pulled: List[str] = []
        while todo:
            ref = todo.pop(0)
            if ref in pulled or ref in mine or ref in played or ref not in by_path:
                continue
            pulled.append(ref)
            todo += [r for v in [by_path[ref].value, *by_path[ref].modes.values()]
                     for r in _refs(v)]
        for f in FOUNDATIONS:
            if f.name in foundations:
                for need in f.requires:
                    steps = [p for p in pulled if p.startswith(need + ".")]
                    if steps:
                        decisions.append(f"{f.name} aliases steps of the {need} scale, so the "
                                         f"steps it points at were added too: "
                                         f"{', '.join(named(p) for p in steps)}.")
        candidates = [(t, t.path.split(".", 1)[0]) for t in wanted] + \
            [(by_path[p], "step") for p in by_path if p in pulled]
        axis_trouble = _axis_problems([t for t, _ in candidates], mapping, new_axes,
                                      mapping_name)
        problems += axis_trouble
    new_axes = {**dict(base.axes),
                **{a: AXES[a] for a in AXES if a in new_axes and a not in base.axes}}

    adding: List[Tuple[Token, str]] = []
    blocked: set = set()   # engine paths of additions that clash
    if not axis_trouble:
        for t, origin in candidates:
            root = t.path.split(".", 1)[0]
            # A step another foundation points at is left out with that one.
            by = root if origin != "step" else _and(
                [f.name for f in FOUNDATIONS if f.name in foundations and root in f.requires]
                or [root])
            what = (f"the {root} foundation" if origin != "step"
                    else f"the {root} step {by} points at")
            probe = _translate(t, mapping, new_axes)
            probe = _copy(probe, path=named(t.path), rename=named)
            hit = [k for k in held.keys(probe) if k in declared]
            if hit:
                where, why = declared[hit[0]]
                problems.append(f"{hit[0]} is declared in {where}, where the import did not "
                                f"read it ({why}); the extension file loads after {name} and "
                                f"would replace its value, so write {hit[0]} in {where} in a "
                                f"form the import reads, or leave {by} out")
                blocked.add(t.path)
                continue
            same = held.same(probe)
            if same is None:
                adding.append((t, origin))
            elif not same:
                blocked.add(t.path)
                key = next(k for k in held.keys(probe) if k in held.by)
                old, where = held.by[key]
                shown = ([_shown_css(old), _shown_css(probe)] if sheet
                         else [_shown(base, old), _shown(generated, t)])
                fix = f"rename {key} in {name}" if where == name else f"edit {where} itself,"
                problems.append(f"{key} is already in {placed(where)} with another value "
                                f"({shown[0]}, {what} would write {shown[1]}); extend never "
                                f"changes a token the system has, so {fix} or leave {by} "
                                "out")
    for role, target in roles.items():
        token = Token(role, ROLE_TYPES[role], "{" + target + "}", layer="semantic")
        probe = _copy(token, path=named(role))
        hit = [k for k in held.keys(probe) if k in declared]
        same = held.same(probe)
        if hit:
            where, why = declared[hit[0]]
            problems.append(f"{hit[0]} is declared in {where}, where the import did not read it "
                            f"({why}); the extension file loads after {name} and would replace "
                            f"its value, so write {hit[0]} in {where} in a form the import "
                            f"reads, then map {role} to it in {mapping_name}")
        elif same is None:
            adding.append((token, "role"))
        elif not same:
            key = next(k for k in held.keys(probe) if k in held.by)
            old, where = held.by[key]
            shown = _shown_css(old) if sheet else _shown(base, old)
            if where == name:
                problems.append(f"{key} is already in {name} as {shown}; extend never changes "
                                f"a token the system has, so map {role} to {old.path} in "
                                f"{mapping_name}")
            else:
                back = (f", or point {role} at {alias_target(old.value)}"
                        if is_alias(old.value) else "")
                problems.append(f"{key} is already in {placed(where)} as {shown}; extend never "
                                f"changes a token the system has, so edit {where} itself{back}")

    # The new tokens in the engine's paths (what the files are written
    # from) and in the system's names (what it is checked and mapped in).
    ours = {t.path for t, _ in adding}
    engine_added = [_copy(_translate(t, mapping, new_axes),
                          rename=lambda p: p if p in ours else named(p)) for t, _ in adding]
    engine_set = TokenSet(new_axes)
    merged = TokenSet(new_axes)
    for t in base.tokens():
        engine_set.add(t)
        merged.add(t)
    added: List[str] = []
    origins: Dict[str, str] = {}
    for t, (_, origin) in zip(engine_added, adding):
        engine_set.add(t)
        path = named(t.path)
        merged.add(_copy(t, path=path, rename=named))
        added.append(path)
        origins[path] = origin

    new_mapping = Mapping(dict(mapping.roles), dict(mapping.axes))
    for t, origin in adding:
        if t.path in ROLE_TYPES and t.path not in new_mapping.roles:
            new_mapping.roles[t.path] = RoleMap(named(t.path),
                                                "owner" if origin == "role" else "name")
    for role in roles:
        if role not in new_mapping.roles:
            # The system already holds the role's token as it would be added.
            new_mapping.roles[role] = RoleMap(named(role), "owner")
    for axis in new_axes:
        if axis not in base.axes and axis not in new_mapping.axes:
            new_mapping.axes[axis] = AxisMap(axis, {v: v for v in AXES[axis]}, "name")

    # A role the mapping sends to a name the system declares in a form the
    # import could not read cannot be checked: the line says so and names
    # the fix, and the check leaves the role out.
    unreadable: Dict[str, str] = {}
    for role, m in mapping.roles.items():
        if m.token is None or base.has(m.token) or (
                ROLE_TYPES[role] == "typography"
                and all(base.has(f"{m.token}-{css}") for _, css in TYPOGRAPHY_FIELDS.values())):
            continue
        key = css_property(m.token) if sheet else m.token
        if key in declared:
            unreadable[role] = key
    covered = {prop for prop, kind, _ in (earlier.clashes if earlier else []) if kind == "unread"}
    for key in dict.fromkeys(unreadable.values()):
        if key in covered:
            continue
        where, why = declared[key]
        problems.append(f"{key} is declared in {where} as a value the import could not read "
                        f"({why}); "
                        + _unread_fix(key, where, [r for r, k in unreadable.items() if k == key],
                                      mapping_name))
    checking = Mapping({r: m for r, m in mapping.roles.items() if r not in unreadable},
                       dict(mapping.axes))
    checking_new = Mapping({r: m for r, m in new_mapping.roles.items() if r not in unreadable},
                           dict(new_mapping.axes))
    clashes = len(problems)
    # The system as it was, checked in the same contexts as the result:
    # under every axis the additions bring, so a finding it had before
    # reads the same in both and is never taken for one the additions
    # caused.
    brought = [a for a in new_axes if a not in base.axes]
    wide = TokenSet(new_axes)
    for t in base.tokens():
        wide.add(t)
    before = enhance(dataclasses.replace(imported, tokens=wide),
                     Mapping(dict(checking.roles), {**checking.axes,
                                                     **{a: new_mapping.axes[a] for a in brought
                                                        if a in new_mapping.axes}}),
                     mapping_name=mapping_name)
    after = enhance(dataclasses.replace(imported, tokens=merged), checking_new,
                    mapping_name=mapping_name)
    roles_added = {t.path: "role" if origin == "role" else t.path.split(".", 1)[0]
                   for t, origin in adding if t.path in ROLE_TYPES}
    caused = [_owner_fix(m, roles_added, mapping_name)
              for m in after.findings if m not in before.findings]
    problems += caused
    had = [m for m in after.findings if m in before.findings]
    existing = [m for m in had if not _in_new_mode(m, brought)]
    unmeasured = [m for m in had if _in_new_mode(m, brought)]
    problems += [p.message for p in validate(engine_set) if p.token in ours
                 and not any(r in blocked for v in [engine_set.get(p.token).value,
                                                    *engine_set.get(p.token).modes.values()]
                             for r in _refs(v))]

    contract_files: Dict[str, str] = {}
    if contracts:
        checked, _ = view(merged, checking_new, mapping_name)
        loaded = []
        for c in contracts:
            path = Path(c)
            try:
                loaded.append(load_contract(path))
            except ContractError as exc:
                problems += [p.message for p in exc.problems]
                continue
            contract_files[f"contracts/{path.name}"] = path.read_text(encoding="utf-8")
        problems += [p.message for p in validate_contracts(loaded, checked)]

    by_name = [t.path for t, origin in adding
               if t.path in ROLE_TYPES and new_mapping.roles[t.path].by == "name"
               and t.path not in mapping.roles]
    if by_name:
        decisions.append(f"{len(by_name)} role{_s(len(by_name))} the extension added "
                         f"{'is' if len(by_name) == 1 else 'are'} mapped in {mapping_name} to "
                         f"the token{_s(len(by_name))} it added under the role's own name, "
                         'marked "by": "name"; confirm or repoint each there.')
    fonts = _font_files(generated, list(ours))
    if fonts:
        decisions.append("The added faces load through fonts.css and fonts-self-host.css, "
                         "written beside the system; fonts.css says how to link them.")
    if not in_place and imported.owned:
        decisions.append(f"{name} is the engine's own, but the import did not read all of it, "
                         f"so it is not rewritten; the additions are in {ext_names[0]}.")
    result = Extended(merged, new_mapping, added, after.check, problems, existing, decisions,
                      unread=list(unread), unmeasured=unmeasured)
    system: Dict[str, str] = {}
    if not problems:
        try:
            system, result.load = _system_files(imported, engine_set, engine_added, earlier,
                                                ext_names, in_place, decisions)
        except (InputError, ValueError) as exc:
            problems.append(str(exc))
    report = _report(imported, result, list(foundations), roles, list(contract_files),
                     origins, after, earlier, in_place, ext_names, mapping_name, clashes,
                     brought, len(caused))
    if problems:
        result.files = {"extend-report.md": report}
        result.load = ""
        return result
    result.beside = [*system, *fonts]
    result.files = {**system, **fonts, "mapping.json": dump_mapping(new_mapping),
                    "extend-report.md": report, **contract_files}
    return result


_CONTEXT = re.compile(r"\(([a-z]+:[a-z]+(?:,[a-z]+:[a-z]+)*)")
# The fixes a finding ends with for a system the owner holds: they name
# what to change in it, which for a token the extension adds is nothing
# the owner can edit.
_THEIR_FIXES = (" Change the value of one of them in your system", ", so ")


def _in_new_mode(finding: str, brought: Sequence[str]) -> bool:
    """Whether a finding holds in a mode of an axis the additions bring,
    at its other value (contrast:high), and so was never measured on the
    system before."""
    return any(axis in brought and value != AXES[axis][0]
               for key in _CONTEXT.findall(finding)
               for axis, value in (pair.split(":") for pair in key.split(",")))


def _owner_fix(finding: str, roles: Dict[str, str], mapping_name: str) -> str:
    """A finding on a role the extension adds, with a fix the owner can
    take: map the role to one of their tokens, which a foundation then
    uses instead of adding its own, or leave the foundation out; for a
    role added with --add-role, point it at another token. Any other
    finding is as it is."""
    hit = [(m.start(), r) for r in roles
           for m in [re.search(r"(?<![\w.-])" + re.escape(r) + r"(?![\w-]|\.[\w-])", finding)]
           if m]
    if not hit:
        return finding
    role = min(hit)[1]
    head = finding
    for cut in _THEIR_FIXES:
        at = head.find(cut)
        if at != -1:
            head = head[:at]
            break
    head = head.rstrip(" .;")
    origin = roles[role]
    if origin == "role":
        fix = f"Point --add-role {role} at another of your tokens, or leave it out"
    else:
        fix = (f"Map {role} in {mapping_name} to one of your tokens, which the {origin} "
               f"foundation then uses instead of adding its own, or leave {origin} out")
    return f"{head}. {fix}."


def _check_roles(roles: Dict[str, str], mapping: Mapping, base: TokenSet,
                 mapping_name: str) -> None:
    """Raise InputError naming the flag and the fix for a role that cannot
    be added as asked."""
    for role, target in roles.items():
        if role not in ROLE_TYPES:
            raise InputError(f"--add-role names {role}, which is not a role the engine checks; "
                             "use one of its roles, for example color.text.default")
        if role in mapping.roles:
            if mapping.roles[role].token is None:
                raise InputError(f"--add-role names {role}, which {mapping_name} keeps out of "
                                 f"the check with {_NOT_MAPPED}; remove that entry from "
                                 f"{mapping_name} to add it")
            raise InputError(f"--add-role names {role}, which the mapping already sends to "
                             f"{mapping.roles[role].token}; edit {mapping_name} to repoint it")
        if not base.has(target):
            raise InputError(f"--add-role points {role} at {target}, which the system does not "
                             "have; name one of its tokens")
        if base.get(target).type != ROLE_TYPES[role]:
            raise InputError(f"--add-role points {role} at {target}, a {base.get(target).type}, "
                             f"but the role needs a {ROLE_TYPES[role]}; name a "
                             f"{ROLE_TYPES[role]} token")


def _axis_problems(tokens: Sequence[Token], mapping: Mapping,
                   axes: Dict[str, Tuple[str, str]], mapping_name: str) -> List[str]:
    """Add to `axes` each engine axis the tokens vary on that the mapping
    does not read from one of the system's, and name each the system
    already has under that name with other values."""
    out: List[str] = []
    for t in tokens:
        for key in t.modes:
            for axis in parse(key, AXES):
                if _theirs(axis, mapping)[1] is not None:
                    continue
                if axis not in axes:
                    axes[axis] = AXES[axis]
                elif axes[axis] != AXES[axis]:
                    line = (f"the system has a mode axis named {axis} with the values "
                            f"{axes[axis][0]} and {axes[axis][1]}, but {t.path} varies on the "
                            f"engine's {axis}; map it in {mapping_name}")
                    if not any(o.startswith(f"the system has a mode axis named {axis} ")
                               for o in out):
                        out.append(line)
    return out


def _font_files(generated: TokenSet, added: Sequence[str]) -> Dict[str, str]:
    """fonts.css and fonts-self-host.css when the extension added a face
    the engine's catalog holds, else nothing."""
    if not any(path in added for path, _ in faces_in(generated)):
        return {}
    return {"fonts.css": fonts_css(generated), "fonts-self-host.css": self_host_css(generated)}


def _head(imported: Imported) -> List[str]:
    """The comment that opens an extension stylesheet, as the Tailwind
    extension writes it."""
    name = Path(imported.report.source.path).name
    return [f"Written by ux-skill beside {name}, which it never rewrites: each",
            "token below is an addition in the source's own names.", f"Load it after {name}."]


def _css_extension(imported: Imported, added: TokenSet) -> str:
    """The additions as a stylesheet in the source's own forms, opened by
    the comment the engine writes on an extension and stamped. The source
    sets color-scheme with each scheme; the extension adds tokens only."""
    text = to_css(added, scheme=imported.scheme, forms=imported.forms, header=_head(imported))
    lines = [line for line in text.split("\n") if not line.strip().startswith("color-scheme:")]
    return stamp_digest("\n".join(lines), css=True)


def _sheet(imported: Imported, added: TokenSet, earlier: Optional[_Earlier]) -> str:
    """A stylesheet extension: what an earlier one holds, as it is, then
    the new additions (a Tailwind theme's in an @theme block of their
    own), under one stamped opening comment."""
    if imported.report.source.format == "tailwind":
        text = tailwind_extension(imported, added)
    else:
        text = _css_extension(imported, added)
    if earlier is None or not earlier.body.strip():
        return text
    head = "/*\n" + "".join(f" * {line}\n" for line in _head(imported)) + " */\n"
    return stamp_digest(head + earlier.body.rstrip("\n") + "\n\n" + _body(text), css=True)


def _detached(ts: TokenSet, added: Sequence[Token]) -> List[Token]:
    """The additions with every alias into the source resolved, mode by
    mode, so a tokens file stands without the files it came from."""
    mine = {t.path for t in added}
    names = list(ts.axes)
    out: List[Token] = []
    for t in added:
        if all(r in mine for v in [t.value, *t.modes.values()] for r in _refs(v)):
            out.append(t)
            continue
        values = {ctx: ts.resolve(t.path, ctx) for ctx in contexts(names, ts.axes)}
        base, modes = compress(values, ts.axes) if names else (values[""], {})
        out.append(_copy(t, value=base, modes=modes))
    return out


def _figma(imported: Imported, ts: TokenSet, earlier: Optional[_Earlier],
           names: List[str]) -> Tuple[Dict[str, str], int]:
    """A Figma extension's payload and script, with what an earlier one
    holds that the file does not have yet kept, and how many variables it
    adds. Raises InputError when a new variable has the name of one the
    earlier extension holds with other values."""
    # The file as it will be once the earlier script runs holds what that
    # script adds, so only the new additions go in this payload.
    held = earlier.combined if earlier is not None and earlier.combined is not None \
        else imported
    payload = figma_extension(held, ts)
    if earlier is not None and earlier.payload is not None:
        record = imported.figma or {}
        have = {(col, vname) for col, vname in record.get("variables", {}).values()}
        # What the earlier script adds comes first, collection by collection
        # and before the new variables, so each alias finds its target.
        specs = {c["name"]: c for c in payload["collections"]}
        order: List[str] = []
        for old in earlier.payload["collections"]:
            spec = specs.get(old["name"])
            if spec is None:
                spec = dict(old, variables=[])
                specs[old["name"]] = spec
            elif old.get("new"):
                spec["new"] = True
            order.append(old["name"])
            new = {v["name"]: v for v in spec["variables"]}
            kept: List[Dict[str, Any]] = []
            for v in old.get("variables", []):
                if (old["name"], v["name"]) in have:
                    continue
                if v["name"] in new:
                    if new[v["name"]] != v:
                        raise InputError(
                            f"{v['name']} is in {earlier.name}, written by an earlier "
                            "extension, with other values; extend never changes what an "
                            f"extension added, so run {names[1]} in Figma, export the file "
                            "again and extend that, or leave it out")
                    continue
                kept.append(v)
            spec["variables"] = kept + spec["variables"]
        order += [c["name"] for c in payload["collections"] if c["name"] not in order]
        payload["collections"] = [specs[n] for n in order if specs[n]["variables"]]
    count = sum(len(c["variables"]) for c in payload["collections"])
    source = Path(imported.report.source.path).name
    return ({names[0]: json.dumps(payload, indent=2) + "\n",
             names[1]: stamp_digest(apply_script(payload, EXTENSION_HEAD.format(name=source)),
                                    css=True)},
            count)


def _system_files(imported: Imported, ts: TokenSet, added: Sequence[Token],
                  earlier: Optional[_Earlier], names: List[str], in_place: bool,
                  decisions: List[str]) -> Tuple[Dict[str, str], str]:
    """The system file, or the extension files, and how to load an
    extension file. `ts` holds the system with the additions, the new
    tokens under the engine's paths; `added` are the new tokens."""
    source = imported.report.source
    fmt = source.format
    name = Path(source.path).name
    if in_place:
        if fmt == "dtcg":
            return {name: dump_dtcg(ts)}, ""
        if fmt == "css":
            return {name: stamp_digest(to_css(ts, scheme=imported.scheme, forms=imported.forms),
                                       css=True)}, ""
        if fmt == "tailwind":
            return {name: stamp_digest(to_tailwind(ts, imported.forms, imported.resets,
                                                   scheme=imported.scheme, roles=False,
                                                   variant=imported.variant), css=True)}, ""
        files = figma_files(ts)
        return {n: stamp_digest(t, css=True) if n.endswith(".js") else t
                for n, t in files.items()}, ""
    ext = names[0]
    held = len(earlier.tokens.tokens()) if earlier is not None else 0
    if fmt == "figma":
        files, count = _figma(imported, ts, earlier, names)
        return files, (f"Run {names[1]} in the Figma file {name} was exported from, through "
                       f"Figma's plugin API: it adds {count} variable{_s(count)} and changes "
                       "none that the file has.")
    if fmt in _STYLESHEETS:
        new = TokenSet(ts.axes)
        for t in added:
            new.add(t)
        count = held + len(added)
        how = (f'where {name} is imported, import {ext} on the line after it (@import '
               f'"./{ext}";)')
        return {ext: _sheet(imported, new, earlier)}, (
            f"Load {ext} after {name}: link it on the line after {name}, or {how}. It adds "
            f"{count} token{_s(count)} and changes nothing in {name}.")
    out = TokenSet(_union(earlier.tokens.axes if earlier else {}, ts.axes))
    for t in earlier.tokens.tokens() if earlier is not None else []:
        out.add(t)
    mine = list(added)
    if fmt in _READ_ONLY:
        mine = _detached(ts, mine)
        decisions.append(f"{ext} holds each addition's own value, since a tokens file cannot "
                         f"point into {_READ_ONLY[fmt]}; the engine does not write "
                         f"{_READ_ONLY[fmt]}, so {name} is left as it is.")
    for t in mine:
        out.add(t)
    count = len(out.tokens())
    if fmt in _READ_ONLY:
        return {ext: dump_dtcg(out)}, (
            f"Read {ext} with {name}: it is a tokens file with {count} token{_s(count)} the "
            f"system does not have, and changes nothing in {name}.")
    return {ext: dump_dtcg(out)}, (
        f"Read {ext} with {name}: list {ext} after {name} among the token files your tools "
        f"read, since its tokens point at {name}'s by name. It holds {count} "
        f"token{_s(count)} and changes nothing in {name}.")


def _s(n: int) -> str:
    return "" if n == 1 else "s"


def _report(imported: Imported, result: Extended, foundations: List[str],
            roles: Dict[str, str], contracts: List[str], origins: Dict[str, str],
            after: Any, earlier: Optional[_Earlier], in_place: bool, ext_names: List[str],
            mapping_name: str, clashes: int, brought: List[str], caused: int) -> str:
    source = imported.report.source
    name = Path(source.path).name
    also = [Path(a.path).name for a in imported.report.also_read]
    ext = ext_names[0] if ext_names else ""
    if result.problems:
        intro = (f"{name} ({source.format}) was not extended: nothing was written but this "
                 "report. Fix each line under What blocks it and run it again.")
    elif in_place:
        intro = (f"Extended {name} ({source.format}), the engine's own system, in place. "
                 "Every token it had is unchanged.")
    else:
        intro = (f"Extended {name} ({source.format}) without rewriting it: the additions are "
                 f"in {ext}, beside it.")
    lines = ["# Extend report", "", intro, "", "## What was added", ""]
    if result.problems:
        lines += ["Nothing, since the extension is blocked. It would add:", ""]
    for f in foundations:
        count = sum(1 for p in result.added if origins.get(p) == f)
        lines.append(f"- {f}: {count} token{_s(count)}.")
    steps = [p for p in result.added if origins.get(p) == "step"]
    if steps:
        lines.append(f"- Steps the new tokens point at: {', '.join(steps)}.")
    for role, target in roles.items():
        lines.append(f"- {role} points at {target}.")
    lines += [f"- {c}." for c in contracts]
    if not (result.added or contracts):
        lines.append("Nothing.")
    if result.load:
        lines += ["", result.load]
    lines += ["", "## What was kept", "",
              f"All {len(imported.tokens.tokens())} tokens {name} had are unchanged, in their "
              "order and with their names."]
    if not in_place:
        files = _and([name, *also])
        n = len(imported.report.not_read)
        kept = (f", so the {n} entr{'y' if n == 1 else 'ies'} the import did not read "
                f"stay{'s' if n == 1 else ''} in it as {'it is' if n == 1 else 'they are'}"
                if n else "")
        lines.append(f"{files} {'is' if not also else 'are'} not rewritten{kept}.")
    if earlier is not None:
        if earlier.payload is not None:
            count = sum(len(c.get("variables", [])) for c in earlier.payload["collections"])
            lines.append(f"{earlier.name}, written by an earlier extension, holds {count} "
                         f"variable{_s(count)}; each the file does not have yet is kept.")
        else:
            count = len(earlier.tokens.tokens())
            lines.append(f"{earlier.name}, written by an earlier extension, holds {count} "
                         f"token{_s(count)}; it is kept as it is, and the new additions follow "
                         "it.")
    lines += ["", "## Check", ""]
    if clashes:
        lines += ["What the lines under What blocks it name was left out of this check; it "
                  "covers the system with the rest.", ""]
    check = after.check_lines(source.path)
    if not after.measured:
        check[-1] = ("The gate was not measured: no role is mapped, so nothing was checked and "
                     f"nothing here passed; map roles to your tokens in {mapping_name} to check "
                     "them.")
    lines += check
    if after.measured and not after.check.report.passed and not caused \
            and (result.existing or result.unmeasured):
        lines += ["", "Every failing check counted above is one listed under Already in the "
                      "system; the additions cause none."]
    if result.problems:
        lines += ["", "## What blocks it", "",
                  "Nothing was written but this report; fix each line and run it again.", ""]
        lines += [f"- {p}" for p in result.problems]
    if result.existing or result.unmeasured:
        lines += ["", "## Already in the system", ""]
    if result.existing:
        lines += ["These were there before the extension; it did not cause them.", ""]
        lines += [f"- {m}" for m in result.existing]
    if result.unmeasured:
        seen = [a for a in brought if any(_in_new_mode(m, [a]) for m in result.unmeasured)]
        one = len(seen) == 1
        modes = _and([f"{a} {AXES[a][1]}" for a in seen])
        lines += ([""] if result.existing else []) + [
            f"Your system was never measured in {modes}, "
            f"{'a mode' if one else 'modes'} the additions bring. These findings are on your "
            f"own tokens in {'that mode' if one else 'those modes'}; the extension did not "
            "cause them, and they do not block it. Decide whether your system should hold "
            f"{'that mode' if one else 'them'}.", ""]
        lines += [f"- {m}" for m in result.unmeasured]
    lines += ["", "## Decisions made without you", ""]
    lines += [f"- {d}" for d in result.decisions] or ["None."]
    if result.unread:
        lines += ["", "## Not read from the brief", ""]
        lines += [f"- {u}" for u in result.unread]
    return "\n".join(lines) + "\n"


def _and(names: List[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def write_extended(result: Extended, imported: Imported, *, out: Any = None,
                   force: bool = False, replace_client: bool = False,
                   force_label: str = "--force", replace_label: str = "--replace-client-files",
                   out_label: str = "--out") -> Dict[str, Any]:
    """Write what extend made through the intake step: the system or its
    extension file, and the font files, beside the source (the only place
    an extension file loads from); the mapping, the report and the
    contracts into `out`, or beside the source when `out` is None. A
    blocked result writes only its report. Two folders are written both or
    neither: each is checked before anything is written, and if the second
    write fails the first is put back as it was. Returns write_with_intake's
    outcome, with `load` added (and appended to the message after a
    write). When two folders are written, `beside` and `out` hold each
    folder's outcome and the lists name each file under its folder."""
    here = _folder(imported)
    labels = dict(force=force, replace_client=replace_client, force_label=force_label,
                  replace_label=replace_label, out_label=out_label)
    target = here if out is None else Path(out).expanduser()
    if result.problems:
        return {**write_with_intake(target, {"extend-report.md": result.files["extend-report.md"]},
                                    imported.report, **labels), "load": ""}
    if out is None or target.resolve() == here.resolve():
        return _loaded(_fonts_note(write_with_intake(here, result.files, imported.report,
                                                     **labels), result, labels), result)
    near = {n: result.files[n] for n in result.beside}
    rest = {n: t for n, t in result.files.items() if n not in result.beside}
    stopped = []
    for folder, files in ((here, near), (target, rest)):
        planned = write_with_intake(folder, files, imported.report, plan_only=True, **labels)
        if planned["status"] not in ("planned", "unchanged"):
            stopped.append((folder, _fonts_note(planned, result, labels)))
    if len(stopped) == 1:
        return {**stopped[0][1], "load": result.load}
    if stopped:
        # Every refusal at once, so one fix round covers both folders.
        return {"status": "error" if any(o["status"] == "error" for _, o in stopped)
                else "refused",
                "written": [], "unchanged": [],
                "conflicts": [str(f / n) for f, o in stopped for n in o["conflicts"]],
                "message": " ".join(_stop(o["message"]) for _, o in stopped),
                "backup": "", "replaced": {}, "load": result.load}
    saved = _snapshot(here, near)
    first = write_with_intake(here, near, imported.report, **labels)
    if first["status"] not in ("written", "unchanged"):
        return {**first, "load": result.load}
    second = write_with_intake(target, rest, imported.report, **labels)
    if second["status"] not in ("written", "unchanged"):
        _put_back(here, first["written"], saved)
        return {**second, "load": result.load,
                "message": _stop(second["message"]) + f" What was written in {here} was put "
                                                       "back as it was, so nothing changed."}
    status = "written" if "written" in (first["status"], second["status"]) else "unchanged"
    words = [o["message"] for o in (first, second) if o["status"] == "written"]
    outcome = {"status": status,
               "written": [str(here / n) for n in first["written"]]
               + [str(target / n) for n in second["written"]],
               "unchanged": [str(here / n) for n in first["unchanged"]]
               + [str(target / n) for n in second["unchanged"]],
               "conflicts": [],
               "message": " ".join(words) or second["message"],
               "backup": second["backup"],
               "replaced": {**{str(here / n): str(here / b)
                               for n, b in first["replaced"].items()},
                            **{str(target / n): str(target / b)
                               for n, b in second["replaced"].items()}},
               "beside": first, "out": second}
    return _loaded(outcome, result)


def _stop(message: str) -> str:
    """A message ending with a full stop, so another can follow it."""
    message = message.rstrip()
    return message if message.endswith((".", "!", "?")) else message + "."


def _loaded(outcome: Dict[str, Any], result: Extended) -> Dict[str, Any]:
    """The outcome with how to load the extension, said after a write."""
    outcome["load"] = result.load
    if result.load and outcome["status"] in ("written", "unchanged"):
        outcome["message"] += " " + result.load
    return outcome


_FONTS = ("fonts.css", "fonts-self-host.css")


def _fonts_note(outcome: Dict[str, Any], result: Extended,
                labels: Dict[str, Any]) -> Dict[str, Any]:
    """A refusal over a font file the extension writes, with why it is
    written and what to do."""
    hit = [c for c in outcome.get("conflicts", []) if Path(c).name in _FONTS]
    if outcome["status"] == "refused" and hit and any(n in result.files for n in _FONTS):
        one = len(hit) == 1
        outcome["message"] += (
            f" {_and([Path(h).name for h in hit])} {'is one of' if one else 'are'} the font "
            "files the added faces load through, written beside the system as a build writes "
            f"them; move your own file{'' if one else 's'} of that name, or pass "
            f"{labels['replace_label']} as well as {labels['force_label']} to replace "
            f"{'it' if one else 'them'} after a backup.")
    return outcome


def _snapshot(folder: Path, files: Mapping_[str, str]) -> Dict[str, bytes]:
    """The bytes of every file a write into `folder` may replace: the files
    it writes that exist, and the records under the intake folder."""
    saved: Dict[str, bytes] = {}
    names = [*files, *(str(p.relative_to(folder)) for p in sorted(
        (folder / INTAKE_DIR).rglob("*.json")) if p.is_file())] \
        if (folder / INTAKE_DIR).is_dir() else list(files)
    for name in names:
        p = folder / name
        if p.is_file():
            saved[name] = p.read_bytes()
    return saved


def _put_back(folder: Path, written: Sequence[str], saved: Dict[str, bytes]) -> None:
    """Undo a write: each file it wrote gets its old bytes back, or is
    removed when it was new, and folders it made that are now empty go."""
    for name in written:
        p = folder / name
        if name in saved:
            p.write_bytes(saved[name])
            continue
        p.unlink(missing_ok=True)
        parent = p.parent
        while parent != folder and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent
