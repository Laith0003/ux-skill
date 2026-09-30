"""Export a system as Figma variables, and write an extension beside a
Figma source.

to_figma() gives a payload: one collection per foundation (the first
segment of each token path), with a mode for every context its tokens vary
in, named by the engine's axis values (color: light standard, light high,
dark standard, dark high), and one variable per token named by its path
with slashes. Primitives are hidden from publishing and have no scopes, so
a designer picks a role, never a raw value; a role aliases its primitive
and carries the scopes that bind it (a surface fills frames and shapes,
text fills text, a line strokes, a space or a padding is a gap, a corner a
radius, an icon a width and height). A typography role becomes one
variable per field (type/text/body/font-size), each aliasing its
primitive.

Figma variables hold colors, numbers, strings and booleans. A size is
given in px (rem at 16px), a duration in ms, a font family by its first
name, and a number held from 0 to 100 (an opacity read from Figma) from 0
to 100 under the Opacity scope; a curve, a shadow and a stroke style are
listed under skipped, with where they stay. figma_files() adds the script
that applies the payload through Figma's plugin API and the script that
reads a file's variables back for import. The apply script matches
collections, modes and variables by name, so a second run updates in
place; it never deletes, and a variable that exists with another type is
left as it is and listed. The engine makes no network call. as_export()
gives a payload in the shape Figma's REST API returns, which is what the
read script produces.

write_figma() writes beside a Figma variables export through the intake
step. When the record of the files the engine wrote lists that export, the
system is the engine's, and the whole system is written to be applied in
place. Otherwise the file is someone else's and is never rewritten:
figma_extension() gives only the additions, each placed in the file's own
collection that shares the most of its path and holds its modes, named and
valued in the file's own names and modes, or in a new collection
(ADDITIONS) when none does, and scoped as the file scopes the variable of
the same type and layer that shares the most of its path there (by the
engine's rule when none does). A mode the import did not read takes the
system's value for the context its name gives (High contrast dark), and
a collection with a mode whose name gives none holds only additions with
one value in every mode; either is said in the notes and the load text.
A token the file holds with another value, and an addition named like
any variable the export declares, read or not, library ones too, is
refused, with the fix; the apply script in extend mode never changes a
variable the file has, it lists it.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from engine.existing import stamp_digest
from engine.foundations.errors import InputError
from engine.foundations.export import PERCENT
from engine.foundations.modes import contexts, parse
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.foundations.values import TYPOGRAPHY_FIELDS, dimension_px, duration_ms
from engine.io.figma_in import SIZE_SCOPES
from engine.io.intake import write_with_intake
from engine.io.report import Imported

_HERE = Path(__file__).resolve().parent / "figma"
APPLY_SCRIPT = (_HERE / "apply-variables.js").read_text(encoding="utf-8")
READ_SCRIPT = (_HERE / "read-variables.js").read_text(encoding="utf-8")
# The collection an extension adds for tokens no collection of the file fits.
ADDITIONS = "ux-skill additions"
_HEAD = "// Apply a ux-skill design system to this Figma file through Figma's plugin API.\n"
# The line that opens an extension's script; {name} is the export it extends.
EXTENSION_HEAD = ("// Add ux-skill's additions to the Figma file {name} was exported from, "
                  "through Figma's plugin API.\n")

_FIGMA_TYPES = {"color": "COLOR", "dimension": "FLOAT", "duration": "FLOAT", "number": "FLOAT",
                "fontWeight": "FLOAT", "fontFamily": "STRING"}
_SKIPPED = {
    "cubicBezier": "a curve; Figma variables hold colors, numbers, strings and booleans, so it "
                   "stays in tokens.json and prototype settings",
    "shadow": "a shadow; Figma keeps shadows in effect styles, which this export does not "
              "write, so it stays in tokens.json",
    "strokeStyle": "a stroke style; Figma sets dashes on the stroke, not in a variable, so it "
                   "stays in tokens.json",
}
# Figma binds a number variable to line height and to letter spacing as a
# px value: its variable scopes list LINE_HEIGHT and LETTER_SPACING as plain
# numbers with no unit field, its REST API returns those values as bare
# floats, and a percent line height cannot come from a variable. So letter
# spacing, which the engine holds in px, takes LETTER_SPACING, and a line
# height, a unitless ratio, takes no scope.
_NOTES = {
    "rem": "Sizes written in rem are given in px at 16px per rem, since Figma variables have no "
           "units.",
    "family": "A font family keeps its first name; the fallbacks stay in tokens.json.",
    "leading": "Line heights are unitless ratios, and Figma binds a number to line height in px, "
               "so their variables have no scope.",
    "duration": "Durations are given in ms and have no scope, since no Figma field binds a "
                "duration, so they read back as plain numbers.",
    "percent": "Opacities held from 0 to 100 are given from 0 to 100 with the Opacity scope, as "
               "Figma holds them.",
}
_FIELD_SCOPES = {"fontFamily": ["FONT_FAMILY"], "fontSize": ["FONT_SIZE"],
                 "fontWeight": ["FONT_WEIGHT"], "letterSpacing": ["LETTER_SPACING"],
                 "lineHeight": []}
# Layout roles that space things apart, which Figma binds as a gap or padding.
_LAYOUT_GAPS = ("gutter", "margin-inline", "region-gap", "landing-gap", "hero", "header",
                "footer")
_FILL = ["FRAME_FILL", "SHAPE_FILL"]

# A function from a token path (and a typography field's CSS name, or "")
# to the key the payload aliases it by, "collection:variable", or None when
# the payload does not hold it.
Ref = Callable[[str, str], Optional[str]]


def _percent(t: Token) -> bool:
    return t.type == "number" and t.extensions.get("unit") == PERCENT


def _scopes(t: Token) -> List[str]:
    """The Figma fields a token's variable binds to. A primitive binds to
    none (designers reach it through a role), except a number held from 0
    to 100, which is an opacity wherever it sits."""
    if _percent(t):
        return ["OPACITY"]
    if t.layer != "semantic":
        return []
    parts = t.path.split(".")
    root, second, last = parts[0], (parts[1:2] or [""])[0], parts[-1]
    if t.type == "color":
        if second in ("text", "syntax") or last in ("text", "on-strong", "on-scrim"):
            return ["TEXT_FILL"]
        if second in ("line", "focus") or last == "line" or last.endswith("-edge"):
            return ["STROKE_COLOR"]
        return list(_FILL)
    if t.type == "fontWeight":
        return ["FONT_WEIGHT"]
    if t.type == "fontFamily":
        return ["FONT_FAMILY"]
    if t.type != "dimension":
        return []
    if root == "space" or (root == "layout" and second in _LAYOUT_GAPS):
        return ["GAP"]
    if root == "layout" or (root == "type" and second == "icon"):
        return ["WIDTH_HEIGHT"]
    if root == "radius":
        return ["CORNER_RADIUS"]
    if root == "border":
        return ["STROKE_FLOAT"]
    if root == "motion":
        # A distance an element travels: no Figma field binds it.
        return []
    if root == "type" and second == "tracking":
        return ["LETTER_SPACING"]
    if root == "type" and (second == "size" or last == "font-size"):
        return ["FONT_SIZE"]
    # A text role's fields, as a Figma file holds them: one variable each.
    if root == "type" and last == "letter-spacing":
        return ["LETTER_SPACING"]
    return ["ALL_SCOPES"]


def _literal(kind: str, value: Any, notes: set) -> Any:
    """A literal as a Figma variable holds it."""
    if kind == "color":
        s = value[1:]
        rgb = [round(int(s[i:i + 2], 16) / 255, 6) for i in (0, 2, 4)]
        alpha = round(int(s[6:8], 16) / 255, 6) if len(s) == 8 else 1
        return {"r": rgb[0], "g": rgb[1], "b": rgb[2], "a": alpha}
    if kind == "dimension":
        if value["unit"] == "rem":
            notes.add("rem")
        px = round(dimension_px(value), 4)
        return int(px) if float(px).is_integer() else px
    if kind == "duration":
        notes.add("duration")
        ms = duration_ms(value)
        return int(ms) if float(ms).is_integer() else ms
    if kind == "fontFamily":
        names = value if isinstance(value, list) else [value]
        if len(names) > 1:
            notes.add("family")
        return names[0]
    return value


def _name(path: str) -> str:
    return path.replace(".", "/")


def _mode_name(ctx: str, ts: TokenSet) -> str:
    """A context as the engine names a mode: one axis value per axis, in the
    axes' order (dark high), or "default" for a collection with no axis."""
    pairs = parse(ctx, ts.axes)
    return " ".join(pairs[a] for a in ts.axes if a in pairs) or "default"


def _axes_of(t: Token, ts: TokenSet) -> List[str]:
    """The axes a token's overrides name, in the set's order."""
    named = {a for key in t.modes for a in parse(key, ts.axes)}
    return [a for a in ts.axes if a in named]


def _variables(t: Token, ts: TokenSet, modes: List[Tuple[str, str]], ref: Ref,
               notes: set, scopes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """A token's variables: one, or one per field for a typography style.
    `modes` pairs each mode name with the context its value comes from;
    `scopes`, when given, replace the engine's for a token that is not a
    typography style."""
    def value_of(raw: Any, kind: str, ctx: str) -> Any:
        if is_alias(raw):
            target = alias_target(raw)
            key = ref(target, "")
            if key is not None:
                return {"alias": key}
            return _literal(kind, ts.resolve(target, ctx), notes)
        return _literal(kind, raw, notes)

    if t.type == "typography":
        out = []
        for field, (kind, css) in TYPOGRAPHY_FIELDS.items():
            if field == "lineHeight":
                notes.add("leading")
            values = {}
            for mode, ctx in modes:
                raw = ts.raw(t.path, ctx)
                if is_alias(raw):
                    # A whole style aliasing another: each field aliases its field.
                    key = ref(alias_target(raw), css)
                    values[mode] = {"alias": key} if key else _literal(
                        kind, ts.resolve(t.path, ctx)[field], notes)
                else:
                    values[mode] = value_of(raw[field], kind, ctx)
            out.append({"name": f"{_name(t.path)}/{css}", "type": _FIGMA_TYPES[kind],
                        "scopes": list(_FIELD_SCOPES[field]) if t.layer == "semantic" else [],
                        "hidden": t.layer != "semantic", "description": t.description,
                        "values": values})
        return out
    if t.type == "number" and t.path.startswith("type.leading."):
        notes.add("leading")
    if _percent(t):
        notes.add("percent")
    values = {mode: value_of(ts.raw(t.path, ctx), t.type, ctx) for mode, ctx in modes}
    return [{"name": _name(t.path), "type": _FIGMA_TYPES[t.type],
             "scopes": list(scopes) if scopes is not None else _scopes(t),
             "hidden": t.layer != "semantic", "description": t.description, "values": values}]


def _skip(t: Token) -> Optional[Dict[str, str]]:
    """The skipped entry for a token Figma variables cannot hold, or None."""
    if t.type == "typography" or t.type in _FIGMA_TYPES:
        return None
    return {"token": t.path, "why": _SKIPPED.get(
        t.type, f"a {t.type}; Figma variables cannot hold it, so it stays in tokens.json")}


def _payload(mode: str, collections: List[Dict[str, Any]], skipped: List[Dict[str, str]],
             notes: set, more: Optional[List[str]] = None) -> Dict[str, Any]:
    return {"version": 1, "mode": mode, "collections": collections, "skipped": skipped,
            "notes": [text for key, text in _NOTES.items() if key in notes] + list(more or [])}


def to_figma(ts: TokenSet) -> Dict[str, Any]:
    """The payload the apply script writes into a Figma file: the whole
    system, one collection per foundation (see the module docstring)."""
    roots: Dict[str, List[Token]] = {}
    skipped: List[Dict[str, str]] = []
    for t in ts.tokens():
        entry = _skip(t)
        if entry is not None:
            skipped.append(entry)
        else:
            roots.setdefault(t.path.split(".", 1)[0], []).append(t)
    types = {t.path: t.type for ts_tokens in roots.values() for t in ts_tokens}

    def ref(target: str, field: str) -> Optional[str]:
        if target not in types or (types[target] == "typography") != bool(field):
            return None
        name = _name(target) + (f"/{field}" if field else "")
        return f"{target.split('.', 1)[0]}:{name}"

    notes: set = set()
    collections = []
    for root, tokens in roots.items():
        used = {a for t in tokens for a in _axes_of(t, ts)}
        ctxs = contexts([a for a in ts.axes if a in used], ts.axes)
        modes = [(_mode_name(c, ts), c) for c in ctxs]
        variables = [v for t in tokens for v in _variables(t, ts, modes, ref, notes)]
        collections.append({"name": root, "modes": [m for m, _ in modes],
                            "variables": variables})
    unsized = _unsized(collections, {_name(t.path) for ts_tokens in roots.values()
                                     for t in ts_tokens if t.type == "dimension"})
    more = [f"{unsized} size{'s have' if unsized != 1 else ' has'} no size scope, since no "
            "Figma field binds them or no role points at them, so they read back as plain "
            "numbers."] if unsized else []
    return _payload("system", collections, skipped, notes, more)


def _unsized(collections: List[Dict[str, Any]], sizes: set) -> int:
    """How many of the variables named in `sizes` a Figma import reads back
    as plain numbers: a size is read as one when all its scopes size
    something, or when it has no scope and only such sizes point at it."""
    kinds: Dict[str, str] = {}
    users: Dict[str, List[str]] = {}
    for c in collections:
        for v in c["variables"]:
            key = f"{c['name']}:{v['name']}"
            if v["type"] != "FLOAT":
                kinds[key] = v["type"]
            elif v["scopes"] and all(x in SIZE_SCOPES for x in v["scopes"]):
                kinds[key] = "size"
            else:
                kinds[key] = "" if not v["scopes"] else "number"
            for value in v["values"].values():
                if isinstance(value, dict) and "alias" in value:
                    users.setdefault(value["alias"], []).append(key)
    changed = True
    while changed:
        changed = False
        for key, kind in kinds.items():
            found = {kinds[u] for u in users.get(key, [])}
            if kind == "" and found == {"size"}:
                kinds[key] = "size"
                changed = True
    return sum(1 for c in collections for v in c["variables"]
               if v["name"] in sizes and kinds[f"{c['name']}:{v['name']}"] != "size")


def apply_script(payload: Dict[str, Any], head: str) -> str:
    """The apply script with `head` on top and `payload` inlined."""
    inline = "const PAYLOAD = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    return head + inline + APPLY_SCRIPT


def figma_files(ts: TokenSet) -> Dict[str, str]:
    """figma-variables.json (the payload), figma-variables.js (the apply
    script with the payload inlined) and figma-read-variables.js."""
    payload = to_figma(ts)
    return {"figma-variables.json": json.dumps(payload, indent=2) + "\n",
            "figma-variables.js": apply_script(payload, _HEAD),
            "figma-read-variables.js": READ_SCRIPT}


def as_export(payload: Dict[str, Any]) -> Dict[str, Any]:
    """A whole payload as Figma's REST API would return it once applied:
    ids in order, the first mode the default, aliases by id. Raises
    ValueError naming the variable when an alias points outside the
    payload (an extension's aliases point into the file it extends)."""
    collections: Dict[str, Any] = {}
    variables: Dict[str, Any] = {}
    ids: Dict[str, str] = {}
    n = 0
    for c in payload["collections"]:
        for v in c["variables"]:
            n += 1
            ids[f"{c['name']}:{v['name']}"] = f"VariableID:{n}"
    for ci, c in enumerate(payload["collections"], 1):
        cid = f"VariableCollectionId:{ci}"
        mode_ids = {m: f"{ci}:{mi}" for mi, m in enumerate(c["modes"])}
        collections[cid] = {"id": cid, "name": c["name"], "defaultModeId": mode_ids[c["modes"][0]],
                            "modes": [{"modeId": mode_ids[m], "name": m} for m in c["modes"]],
                            "variableIds": [ids[f"{c['name']}:{v['name']}"]
                                            for v in c["variables"]],
                            "hiddenFromPublishing": False, "remote": False}
        for v in c["variables"]:
            vid = ids[f"{c['name']}:{v['name']}"]
            values: Dict[str, Any] = {}
            for mode, value in v["values"].items():
                if isinstance(value, dict) and "alias" in value:
                    if value["alias"] not in ids:
                        raise ValueError(f"{c['name']}/{v['name']} aliases {value['alias']}, "
                                         "which the payload does not hold; pass a whole "
                                         "system's payload (to_figma)")
                    values[mode_ids[mode]] = {"type": "VARIABLE_ALIAS", "id": ids[value["alias"]]}
                else:
                    values[mode_ids[mode]] = value
            variables[vid] = {"id": vid, "name": v["name"], "variableCollectionId": cid,
                              "resolvedType": v["type"], "valuesByMode": values,
                              "scopes": list(v["scopes"]), "description": v["description"],
                              "hiddenFromPublishing": v["hidden"], "remote": False}
    return {"meta": {"variableCollections": collections, "variables": variables}}


def _show(t: Token) -> str:
    """A token's value as a person reads it, with each mode: 12px,
    #FFFFFF (scheme:dark: #000000)."""
    def text(value: Any) -> str:
        if isinstance(value, dict) and set(value) == {"value", "unit"}:
            return f"{value['value']}{value['unit']}"
        if isinstance(value, list):
            return ", ".join(str(x) for x in value)
        return json.dumps(value) if isinstance(value, dict) else str(value)
    modes = ", ".join(f"{k}: {text(v)}" for k, v in t.modes.items())
    return f"{text(t.value)} ({modes})" if modes else text(t.value)


def _prefix(a: str, b: str) -> int:
    """How many leading path segments two paths share."""
    n = 0
    for x, y in zip(a.split("."), b.split(".")):
        if x != y:
            break
        n += 1
    return n


def figma_extension(imported: Imported, ts: TokenSet) -> Dict[str, Any]:
    """The payload of what `ts` adds to the Figma file `imported` was read
    from, in the file's own collections, modes and names (see the module
    docstring); its collections are empty when there is nothing to add.
    Raises InputError naming the variable, both values and the fix when
    `ts` changes a token the file holds."""
    record = imported.figma or {}
    source = Path(imported.report.source.path).name
    if not record.get("collections"):
        raise InputError(f"{imported.report.source.path} was not read as a Figma variables "
                         "export, so its collections are not known; import the Figma export "
                         "and pass what the import gives")
    held = imported.tokens
    own: Dict[str, List[str]] = record["variables"]
    scoped: Dict[str, List[str]] = record.get("scopes", {})
    declared: Dict[str, List[str]] = record.get("declared", {})
    unread: Dict[str, Dict[str, Optional[str]]] = record.get("unread", {})

    def projected(ctx: Optional[str]) -> Optional[str]:
        # A context an unread mode's name gives, on the axes the system has.
        if ctx is None:
            return None
        return ",".join(p for p in ctx.split(",") if p.split(":")[0] in ts.axes)

    # Each collection's modes with the context its value comes from: the
    # one it was read in, or the one its name gives; None when neither.
    cols: Dict[str, List[Tuple[str, Optional[str]]]] = {
        name: [(mode, ctx if ctx is not None else projected(unread.get(name, {}).get(mode)))
               for mode, ctx in modes]
        for name, modes in record["collections"].items()}
    covers = {name: {a for _, ctx in modes if ctx for a in parse(ctx, ts.axes)}
              for name, modes in cols.items()}
    # A collection with a mode nothing gives a value for holds only tokens
    # with one value in every mode.
    blind = {name for name, modes in cols.items() if any(ctx is None for _, ctx in modes)}
    members: Dict[str, List[str]] = {}
    for path, (col, _) in own.items():
        members.setdefault(col, []).append(path)

    added: List[Token] = []
    skipped: List[Dict[str, str]] = []
    for t in ts.tokens():
        if held.has(t.path):
            old = held.get(t.path)
            if (old.type, old.value, old.modes) != (t.type, t.value, t.modes):
                col, vname = own.get(t.path, ["", _name(t.path)])
                where = f"the collection {col} of {source}" if col else source
                raise InputError(f"{vname} is {_show(old)} in {where} and {_show(t)} in the "
                                 "system to write; an extension only adds variables, so change "
                                 f"{vname} in Figma itself, or add a token under a new name")
            continue
        entry = _skip(t)
        if entry is not None:
            skipped.append(entry)
            continue
        names = [f"{_name(t.path)}/{css}" for _, css in TYPOGRAPHY_FIELDS.values()] \
            if t.type == "typography" else [_name(t.path)]
        taken = next((n for n in names if n in declared), None)
        if taken is not None:
            raise InputError(f"{taken} is already a variable of {_and(declared[taken])} in "
                             f"{source}, which the import did not read as a token; an "
                             "extension only adds variables and never changes one the file "
                             "has, so give the token a name the file does not use")
        added.append(t)

    new_name = ADDITIONS
    n = 1
    while new_name in cols or new_name in record.get("declared_collections", []):
        n += 1
        new_name = f"{ADDITIONS} {n}"
    placed: Dict[str, str] = {}
    for t in added:
        needs = set(_axes_of(t, ts))
        best, score = new_name, 0
        for name in cols:
            if needs <= covers[name] and not (needs and name in blind):
                got = max((_prefix(t.path, p) for p in members.get(name, [])), default=0)
                if got > score:
                    best, score = name, got
        placed[t.path] = best
    types = {t.path: t.type for t in added}

    def ref(target: str, field: str) -> Optional[str]:
        if target in types:
            if (types[target] == "typography") != bool(field):
                return None
            return f"{placed[target]}:{_name(target)}" + (f"/{field}" if field else "")
        if target in own and not field:
            col, vname = own[target]
            return f"{col}:{vname}"
        return None

    new_axes = [a for a in ts.axes if any(a in _axes_of(t, ts) for t in added
                                          if placed[t.path] == new_name)]
    new_modes = [(_mode_name(c, ts), c) for c in contexts(new_axes, ts.axes)]
    notes: set = set()
    more: List[str] = []
    order: Dict[str, Dict[str, Any]] = {}
    for t in added:
        name = placed[t.path]
        if name == new_name:
            modes = new_modes
        else:
            modes = [(m, ctx or "") for m, ctx in cols[name]]
            if name not in order:
                more += _unread_notes(name, unread.get(name, {}), cols[name])
        spec = order.setdefault(name, {"name": name, "modes": [m for m, _ in modes],
                                       "variables": []})
        if name == new_name:
            spec["new"] = True
        # The file's own scopes for its kind: those of the variable of the
        # same type that shares the most of this path in the collection.
        like = [(_prefix(t.path, p), -i, p) for i, p in enumerate(members.get(name, []))
                if held.get(p).type == t.type and held.get(p).layer == t.layer
                and p in scoped]
        scopes = scoped[max(like)[2]] if like and max(like)[0] > 0 else None
        spec["variables"] += _variables(t, ts, modes, ref, notes, scopes)
    return _payload("extend", list(order.values()), skipped, notes, more)


def _unread_notes(name: str, unread: Dict[str, Optional[str]],
                  modes: List[Tuple[str, Optional[str]]]) -> List[str]:
    """What an extension writes in each mode of a collection that the
    import did not read."""
    out = []
    for mode, ctx in modes:
        if mode not in unread:
            continue
        if ctx:
            out.append(f"{name} has the mode {mode}, which the import did not read; each "
                       f"addition there takes the system's value for {ctx}, which the mode's "
                       "name gives.")
        else:
            out.append(f"{name} has the mode {mode}, which the import did not read and whose "
                       "name gives no mode of the system; only additions with one value in "
                       f"every mode go in {name}, and {mode} takes that value.")
    return out


def _and(items: List[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def extension_names(source: Path) -> Tuple[str, str]:
    """The payload and the script written beside a source: variables.json
    gives variables-ext.json and variables-ext.js."""
    return f"{source.stem}-ext.json", f"{source.stem}-ext.js"


def write_figma(ts: TokenSet, imported: Imported, *, force: bool = False,
                replace_client: bool = False, force_label: str = "--force",
                replace_label: str = "--replace-client-files",
                out_label: str = "--out") -> Dict[str, Any]:
    """Write `ts`, a system in the names of the Figma export `imported` was
    read from, beside that export through the intake step (see the module
    docstring): the whole system when the engine wrote the export, else an
    extension. Returns write_with_intake's outcome with `file` (the script
    to run) and `load` (how to run it). Raises InputError when `imported`
    is not a Figma export, or when `ts` changes a token a foreign file
    holds."""
    source = imported.report.source
    path = Path(source.path).expanduser()
    if source.format != "figma":
        raise InputError(f"{source.path} is a {source.format} source, not a Figma variables "
                         "export, so no Figma files are written beside it; pass the Figma "
                         "variables export the system was read from, or export the system to a "
                         "new folder")
    said: List[str] = []
    if imported.owned:
        files = figma_files(ts)
        script = "figma-variables.js"
        files = {name: stamp_digest(text, css=True) if name.endswith(".js") else text
                 for name, text in files.items()}
        count = sum(len(c["variables"]) for c in to_figma(ts)["collections"])
        does = (f"it writes {count} variable{'' if count == 1 else 's'}, updating the ones the "
                "file has in place by name, and deletes none")
    else:
        payload = figma_extension(imported, ts)
        count = sum(len(c["variables"]) for c in payload["collections"])
        if not count:
            return {"status": "unchanged", "written": [], "unchanged": [], "conflicts": [],
                    "message": f"{source.path} already holds every token of the system to "
                               "write, so no extension was written.",
                    "backup": "", "replaced": {}, "file": "", "load": ""}
        data, script = extension_names(path)
        files = {data: json.dumps(payload, indent=2) + "\n",
                 script: stamp_digest(
                     apply_script(payload, EXTENSION_HEAD.format(name=path.name)), css=True)}
        does = (f"it adds {count} variable{'' if count == 1 else 's'} and changes none that the "
                "file has")
        # What it writes in a mode the import did not read is said here too.
        said = [n for n in payload["notes"] if "which the import did not read" in n]
    load = (f"Run {path.parent / script} in the Figma file {path.name} was exported from, "
            f"through Figma's plugin API: {does}.")
    if said:
        load += " " + " ".join(said)
    outcome = write_with_intake(path.parent, files, imported.report, force=force,
                                replace_client=replace_client, force_label=force_label,
                                replace_label=replace_label, out_label=out_label)
    outcome["file"] = str(path.parent / script)
    outcome["load"] = load
    if outcome["status"] in ("written", "unchanged"):
        outcome["message"] += " " + load
    return outcome


__all__ = ["ADDITIONS", "APPLY_SCRIPT", "EXTENSION_HEAD", "READ_SCRIPT", "Ref", "apply_script",
           "as_export", "extension_names", "figma_extension", "figma_files", "to_figma",
           "write_figma"]
