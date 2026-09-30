"""Tell a source's format from the file, and read it with its importer.

detect_format() tells the format from the name and, for .css and .json,
the content: a stylesheet with an @theme block is Tailwind 4, any other
stylesheet is CSS; JSON with a variableCollections key is a Figma
variables export, JSON with a $value anywhere, or Tokens Studio's
$themes, $metadata or value and type leaves, is DTCG, and any other JSON
is a Tailwind 3 theme. A folder is markdown rule files, unless system
detect finds a token file or a foundation stylesheet in it: then it is a
project, read as the set detect proposes.

read_sources() reads one source, or several read as one system: the first
is the system (a tokens file, a stylesheet, any format), and each after
it is a stylesheet that adds to it, such as the app's own globals holding
the dark values. The stylesheets are read together with the system, so a
dark value is paired by name with the system's token (--color-text-body
with color.text.body), a var() in one file resolves to a token of
another, and a property the stylesheets alone declare becomes a token of
its own. A base value set more than once is read as the browser reads
it: the system loads first and each stylesheet after it, in the order
given; the more specific selector wins (html:root and :root:root outrank
:root, which outranks html; a token file's value is read as :root), and
of two as specific the later one does. The winner's value is the token's,
with a note naming the winner and the loser by file and line; a loser is
listed under Not read with both places and the fix. Every file read is in
the report's also_read, so the intake step checks and backs up each one.
"""
from __future__ import annotations

import json
import re
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.errors import InputError
from engine.foundations.tokens import TokenSet, alias_target, css_property, is_alias
from engine.io.values_in import split_top
from engine.io.report import (FORMATS, Imported, ImportReport, Item, Mapped, Source,
                              ownership_line, read_source)

# What --format takes: auto tells the format from the file.
CHOICES: Tuple[str, ...] = ("auto",) + FORMATS
# The kinds system detect gives that a project folder is read from.
_TOKEN_KINDS = ("tokens-source", "tokens")
_SHEET_KIND = "css-foundation"


def _has_value(node: Any) -> bool:
    if isinstance(node, dict):
        return "$value" in node or any(_has_value(v) for v in node.values())
    return False


def _studio(node: Any) -> bool:
    """A Tokens Studio leaf: value and type, without the dollar signs."""
    if isinstance(node, dict):
        if "value" in node and "type" in node and not isinstance(node["value"], dict):
            return True
        return any(_studio(v) for v in node.values())
    return False


def _project(p: Path) -> List[Tuple[str, str]]:
    """What system detect finds in a folder: (kind, path) for each token
    file and foundation stylesheet, built output left out, and so is what
    ux-skill keeps or writes there itself: anything under its .uxskill
    folder (the backups of every source), and a stylesheet it wrote (an
    export or an extension, known by the files record or its stamp). A
    token file the engine wrote stays: it is the engine's own system."""
    from engine.existing import detect_existing_system
    from engine.existing.record import engine_wrote
    from engine.io.intake import INTAKE_DIR
    found = detect_existing_system(p)
    out = []
    for s in found.get("sources", []):
        kind, rel = s["kind"], s["path"]
        if kind not in (*_TOKEN_KINDS, _SHEET_KIND) or INTAKE_DIR in Path(rel).parts:
            continue
        f = p / rel
        if kind == _SHEET_KIND and engine_wrote(f.parent, f.name):
            continue
        out.append((kind, rel))
    return out


def detect_format(path: Any, label: str = "--from", format_label: str = "--format") -> str:
    """dtcg, css, tailwind, tailwind-json, markdown, figma or project, from
    the file's name and, for .css and .json, its content (see the module
    docstring). Raises InputError naming `label` and the fix for a file
    whose format its name does not say."""
    p = Path(path).expanduser()
    suffix = p.suffix.lower()
    if p.is_dir():
        return "project" if _project(p) else "markdown"
    if suffix == ".md":
        return "markdown"
    if suffix in (".js", ".cjs", ".mjs", ".ts", ".cts", ".mts"):
        return "tailwind"
    try:
        text = p.read_text(encoding="utf-8-sig") if suffix in (".css", ".json") else ""
    except (OSError, UnicodeDecodeError):
        text = ""
    if suffix == ".css":
        return "tailwind" if re.search(r"@theme\b", text) else "css"
    if suffix == ".json":
        try:
            doc = json.loads(text)
        except ValueError:
            return "dtcg"
        data = doc.get("meta", doc) if isinstance(doc, dict) else None
        if isinstance(data, dict) and "variableCollections" in data:
            return "figma"
        if isinstance(doc, dict) and ("$themes" in doc or "$metadata" in doc):
            return "dtcg"
        return "dtcg" if _has_value(doc) or _studio(doc) else "tailwind-json"
    names = ", ".join(CHOICES[1:-1]) + " or " + CHOICES[-1]
    raise InputError(f"{label} {p} is not a format uxskill reads by its name; pass "
                     f"{format_label} {names}")


def read_system(path: Any, fmt: str = "auto", label: str = "--from",
                second_modes: Optional[Mapping[str, str]] = None,
                modes_label: str = "--figma-mode",
                format_label: str = "--format") -> Imported:
    """Read one system with the importer for its format (engine.io.read_any).
    `second_modes` (collection -> mode) is for a Figma export only. A
    project folder is read as the set system detect proposes. Messages name
    the inputs by the caller's labels."""
    if fmt not in CHOICES:
        names = ", ".join(CHOICES[:-1]) + " or " + CHOICES[-1]
        raise InputError(f"{format_label} is {fmt}; pass {names}")
    found = detect_format(path, label, format_label) if fmt == "auto" else fmt
    _check_format(Path(path).expanduser(), fmt, format_label)
    if found == "project":
        root = Path(path).expanduser()
        imported = read_sources(_proposed(root, label), "auto", label, second_modes,
                                modes_label, format_label)
        return _root_direction(imported, root)
    if second_modes and found != "figma":
        raise InputError(f"{modes_label} is for a Figma variables export, and {label} "
                         f"{Path(path).name} is read as {found}; drop {modes_label}")
    from engine.io import read_any
    options = {"second_modes": dict(second_modes)} if second_modes else {}
    imported = read_any(path, found, label, **options)
    imported.report.ownership = ownership_line(imported)
    return imported


def _root_direction(imported: Imported, root: Path) -> Imported:
    """A project whose pages read right to left (<html dir="rtl">) holds
    its rtl values on the root: a direction axis read with the root as its
    base and ltr as its mode is rtl-based, said so in a note. The base is
    what the root holds, never a guess from the selectors."""
    from engine.existing import detect_existing_system
    from engine.foundations.tokens import ROOT_BASE
    axis = imported.tokens.axes.get("direction")
    if not axis or axis[0] != ROOT_BASE or "rtl" in axis:
        return imported
    if detect_existing_system(root).get("declared", {}).get("direction") != "rtl":
        return imported
    ts = TokenSet({**imported.tokens.axes, "direction": ("rtl", *axis[1:])})
    for t in imported.tokens.tokens():
        ts.add(t)
    imported.tokens = ts
    imported.report.axes = {a: tuple(v) for a, v in ts.axes.items()}
    imported.report.notes.append(Item(root.name, "direction", (
        "the pages set dir=\"rtl\" on <html>, so the root holds the rtl values: rtl is the "
        "direction axis's base and ltr its mode")))
    return imported


def _check_format(p: Path, fmt: str, flag: str = "--format") -> None:
    """A --format that cannot read the file, by its name: JSON formats on a
    stylesheet and stylesheet formats on JSON. Raises InputError naming the
    flag and the fix."""
    suffix = p.suffix.lower()
    if fmt in ("dtcg", "figma", "tailwind-json") and suffix == ".css":
        raise InputError(f"{flag} {fmt} reads JSON and {p.name} is a stylesheet; pass "
                         f"{flag} css or tailwind, or leave {flag} out")
    if fmt in ("css", "tailwind") and suffix == ".json":
        raise InputError(f"{flag} {fmt} reads a stylesheet and {p.name} is JSON; pass "
                         f"{flag} dtcg, figma or tailwind-json, or leave {flag} out")


def _proposed(root: Path, label: str) -> List[Path]:
    """The files of the system detect finds in a project folder: its first
    token file, then each foundation stylesheet; or the stylesheets alone.
    Raises InputError naming the folder and the fix when detect finds a
    second token file, which is not read with the first."""
    found = _project(root)
    tokens = [path for kind, path in found if kind in _TOKEN_KINDS]
    sheets = [path for kind, path in found if kind == _SHEET_KIND]
    if len(tokens) > 1:
        raise InputError(f"{label} {root} holds more than one token file ({', '.join(tokens)}); "
                         f"pass the one that holds the system as {label}, and each stylesheet "
                         f"that adds to it as another {label}")
    return [root / p for p in [*tokens, *sheets]]


def read_sources(paths: Any, fmt: str = "auto", label: str = "--from",
                 second_modes: Optional[Mapping[str, str]] = None,
                 modes_label: str = "--figma-mode",
                 format_label: str = "--format") -> Imported:
    """Read one source, or several as one system (see the module
    docstring). `paths` is a path or a list of them; `fmt` applies to the
    first. Raises InputError naming `label` (or `format_label`) and the fix."""
    if isinstance(paths, (str, Path)):
        paths = [paths]
    paths = [Path(p).expanduser() for p in paths]
    if not paths:
        raise InputError(f"{label} is missing; pass the file that holds the system, for "
                         "example tokens.json")
    seen = set()
    for p in paths:
        key = str(p.resolve())
        if key in seen:
            raise InputError(f"{label} {p} is given twice; pass each file once")
        seen.add(key)
    first = read_system(paths[0], fmt, label, second_modes, modes_label, format_label)
    if len(paths) == 1:
        return first
    sheets: List[Tuple[Source, str]] = []
    for p in paths[1:]:
        kind = detect_format(p, label, format_label)
        if kind not in ("css", "tailwind") or p.suffix.lower() != ".css":
            raise InputError(f"{label} {p.name} is read as {kind}; a second {label} adds a "
                             f"stylesheet's values (its dark scheme, say) to the first, so pass "
                             f"the system first and each stylesheet after it")
        sheets.append(read_source(p, kind, label))
    imported = combine(first, sheets, label)
    imported.report.ownership = ownership_line(imported)
    return imported


# ---------------------------------------------------------------- combine

_MARK = "uxskill-read-together.css"
_DECLARED = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")


def _rename(value: Any, names: Dict[str, str]) -> Any:
    """`value` with each alias to a stylesheet name that is the system's
    token pointed at that token's path."""
    if is_alias(value):
        target = alias_target(value)
        return "{" + names.get(target, target) + "}"
    if isinstance(value, dict):
        return {k: _rename(v, names) for k, v in value.items()}
    if isinstance(value, list):
        return [_rename(v, names) for v in value]
    return value


class _Places:
    """Where each line of the text read together came from: the system's
    own values (dropped: they are the system's report's to tell), or a
    stylesheet and its own line."""

    def __init__(self, first_lines: int, sheets: Sequence[Tuple[Source, str]],
                 system: str) -> None:
        self.system = system
        self.parts: List[Tuple[int, int, str]] = []
        at = first_lines + 1
        for source, text in sheets:
            n = text.count("\n") + 1
            self.parts.append((at, at + n, Path(source.path).name))
            at += n
        self.first_lines = first_lines

    def where(self, line: int) -> Optional[str]:
        for start, end, name in self.parts:
            if start <= line < end:
                return f"{name}:{line - start + 1}"
        return None

    def text(self, message: str) -> str:
        """A message with each place in the text read together named by its
        stylesheet and line, or as the system's."""
        def sub(m: "re.Match[str]") -> str:
            return self.where(int(m.group(1))) or self.system

        def line(m: "re.Match[str]") -> str:
            at = self.where(int(m.group(2)))
            if at is None:
                return f"in {self.system}" if m.group(1) else self.system
            file, n = at.rsplit(":", 1)
            return f"{m.group(1) or ''}line {n} of {file}"
        message = re.sub(re.escape(_MARK) + r":(\d+)", sub, message)
        message = re.sub(r"\b(on )?line (\d+)", line, message)
        return message.replace(_MARK, self.parts[0][2])

    def item(self, i: Any) -> Any:
        m = re.fullmatch(re.escape(_MARK) + r":(\d+)", i.where)
        if m is None:
            where = self.parts[0][2] if i.where == _MARK else i.where
        else:
            where = self.where(int(m.group(1)))
            if where is None:
                return None
        if isinstance(i, Mapped):
            return replace(i, where=where)
        return replace(i, where=where, message=self.text(i.message))


def combine(first: Imported, sheets: Sequence[Tuple[Source, str]], label: str) -> Imported:
    """`first` with the stylesheets `sheets` ((source, text) each) read
    together with it (see the module docstring)."""
    from engine.foundations.export import to_css
    from engine.io.css_in import import_css
    try:
        base = to_css(first.tokens, scheme=first.scheme, forms=first.forms)
    except ValueError as exc:
        raise InputError(f"{label} {Path(first.report.source.path).name} cannot be read "
                         f"together with a stylesheet ({exc}); pass it on its own") from None
    names = {css_property(t.path)[2:]: t.path for t in first.tokens.tokens()}
    system = Path(first.report.source.path).name
    kept: List[Item] = []
    won_notes: List[Item] = []
    texts, won = _cascade(first, sheets, names, kept, won_notes)
    sheets = [(source, text) for (source, _), text in zip(sheets, texts)]
    text = base + "\n" + "\n".join(t for _, t in sheets)
    places = _Places(base.count("\n") + 1, sheets, system)
    together = import_css(text, Source(_MARK, "css", "0" * 64, len(text)))
    declared = {m.group(1)[2:] for _, t in sheets for m in _DECLARED.finditer(t)}
    axes: Dict[str, Tuple[str, ...]] = {a: tuple(v) for a, v in first.tokens.axes.items()}
    for a, v in together.tokens.axes.items():
        axes.setdefault(a, tuple(v))
    ts = TokenSet(axes)
    added_modes = 0
    for t in first.tokens.tokens():
        key = css_property(t.path)[2:]
        theirs = together.tokens.get(key) if together.tokens.has(key) else None
        modes = dict(t.modes)
        if theirs is not None:
            for ctx, v in theirs.modes.items():
                if ctx not in modes and _usable(ctx, first.tokens.axes, together.tokens.axes):
                    modes[ctx] = _rename(v, names)
                    added_modes += 1
        value = won[key] if key in won else t.value
        ts.add(replace(t, value=value, modes=modes, extensions=dict(t.extensions)))
    own = 0
    for t in together.tokens.tokens():
        if t.path in names or t.path not in declared or ts.has(t.path):
            continue
        ts.add(replace(t, value=_rename(t.value, names),
                       modes={k: _rename(v, names) for k, v in t.modes.items()}))
        own += 1
    old = first.report
    report = ImportReport.of(old.source, ts, old.entries + own)
    report.renamed = list(old.renamed)
    report.notes = list(old.notes) + won_notes
    report.not_read = list(old.not_read) + kept
    report.mapped = list(old.mapped)
    report.headline = list(old.headline)
    report.also_read = [*old.also_read, *(s for s, _ in sheets)]
    for target, items in ((report.renamed, together.report.renamed),
                          (report.notes, together.report.notes),
                          (report.not_read, together.report.not_read),
                          (report.mapped, together.report.mapped)):
        target += [x for x in (places.item(i) for i in items) if x is not None]
    names_read = ", ".join(Path(s.path).name for s, _ in sheets)
    report.notes.append(Item(names_read, "", (
        f"read together with {Path(old.source.path).name}: {added_modes} mode "
        f"value{'' if added_modes == 1 else 's'} added to its tokens, paired by name, and "
        f"{own} token{'' if own == 1 else 's'} of {'its' if len(sheets) == 1 else 'their'} "
        "own")))
    return Imported(ts, report, dict(first.forms) or dict(together.forms),
                    scheme=first.scheme if first.forms else together.scheme,
                    resets=first.resets or together.resets,
                    variant=first.variant or together.variant, owned=False,
                    figma=first.figma)


def _shown(value: Any) -> str:
    if isinstance(value, dict) and set(value) == {"value", "unit"}:
        return f"{value['value']:g}{value['unit']}" if isinstance(value["value"], (int, float)) \
            else f"{value['value']}{value['unit']}"
    return value if isinstance(value, str) else json.dumps(value, sort_keys=True)


def _decl_value(text: str, names: Dict[str, str]) -> Optional[Tuple[str, Any]]:
    """(kind, value) of a declaration as a token holds it, an alias to a
    system token by its path; None when it has no single reading."""
    from engine.io.values_in import NotRead, css_alias, read_value
    try:
        alias = css_alias(text)
        if alias is not None:
            return "alias", "{" + names.get(alias[0], alias[0]) + "}"
        return read_value(text)
    except NotRead:
        return None


def _system_place(first: Imported, key: str, path: str) -> Tuple[str, int, str,
                                                                   Tuple[int, int, int]]:
    """(file, line, selector, specificity) where the system sets a token's
    base value: the last base rule that declares it in the system's
    stylesheets, else its key in the token file, read as :root (the root
    a built token file's values load on)."""
    from engine.existing.survey import _key_line
    from engine.io.css_in import _base, is_root, parse_css, specificity
    files = [first.report.source.path, *(a.path for a in first.report.also_read)]
    for f in reversed(files):
        p = Path(f)
        if p.suffix.lower() not in (".css", ".scss", ".pcss"):
            continue
        try:
            rules = parse_css(p.read_text(encoding="utf-8-sig"), p.name)
        except (OSError, UnicodeDecodeError, ValueError, InputError):
            continue
        hit = None
        for rule in rules:
            if rule.media or not (rule.selector == "@theme" or _base(rule.selector)):
                continue
            for d in rule.declarations:
                if d.name == "--" + key:
                    hit = (p.name, d.line, rule.selector.strip(),
                           max(specificity(m) for m in split_top(rule.selector, ",")
                               if is_root(m) or m.strip() == "@theme"))
        if hit is not None:
            return hit
    p = Path(first.report.source.path)
    try:
        line = _key_line(p.read_text(encoding="utf-8-sig"), path)
    except (OSError, UnicodeDecodeError):
        line = 1
    return p.name, line, ":root", (0, 1, 0)


def _cascade(first: Imported, sheets: Sequence[Tuple[Source, str]], names: Dict[str, str],
             kept: List[Item], notes: List[Item]) -> Tuple[List[str], Dict[str, Any]]:
    """The base values the system and the stylesheets set more than once,
    decided as the browser decides them (see the module docstring): each
    stylesheet's text with every declaration that lost, and every one that
    beat the system's value, blanked out (lines and places stay), and the
    value that won over the system's for each token. A loser is listed in
    `kept` as not read, a winner over another value in `notes`, each naming
    every place that holds the other value, stylesheets first."""
    from engine.io.css_in import _base, is_root, parse_css, specificity
    lines = [text.split("\n") for _, text in sheets]
    # key -> the value that stands: its reading, specificity, text, and
    # every place that holds it, [(file, line, selector, the sheet's
    # (index, line, property) or None for the system)].
    current: Dict[str, Dict[str, Any]] = {}
    won: Dict[str, Any] = {}

    def blank(i: int, line: int, prop: str) -> None:
        row = lines[i][line - 1]
        m = re.search(re.escape(prop) + r"\s*:[^;}]*;?", row)
        if m is not None:
            lines[i][line - 1] = row[:m.start()] + " " * (m.end() - m.start()) + row[m.end():]

    def at(places: List[Tuple[str, int, str, Any]]) -> str:
        """Every place, stylesheets first, as file:line (selector)."""
        ordered = [p for p in places if p[3] is not None] + [p for p in places if p[3] is None]
        shown = [f"{f}:{n} ({sel})" for f, n, sel, _ in ordered]
        return shown[0] if len(shown) == 1 else ", ".join(shown[:-1]) + " and " + shown[-1]

    for i, (source, text) in enumerate(sheets):
        sheet = Path(source.path).name
        for rule in parse_css(text, source.path):
            if rule.media or not (rule.selector == "@theme" or _base(rule.selector)):
                continue
            members = [m for m in split_top(rule.selector, ",") if is_root(m)
                       or m.strip() == "@theme"] or split_top(rule.selector, ",")
            spec = max(specificity(m) for m in members)
            selector = rule.selector.strip()
            for d in rule.declarations:
                key = d.name[2:]
                read = _decl_value(d.value, names)
                if read is None:
                    continue
                if key not in current and key in names:
                    ours = first.tokens.get(names[key])
                    file, line, sel, sys_spec = _system_place(first, key, names[key])
                    current[key] = {"read": (ours.type, ours.value), "spec": sys_spec,
                                    "text": _shown(ours.value),
                                    "places": [(file, line, sel, None)]}
                place = (sheet, d.line, selector, (i, d.line, d.name))
                prev = current.get(key)
                if prev is None:
                    current[key] = {"read": read, "spec": spec, "text": d.value.strip(),
                                    "places": [place]}
                    continue
                if _same(read, prev["read"]):
                    # Another place holding the value that stands.
                    prev["places"].append(place)
                    prev["spec"] = max(prev["spec"], spec)
                    continue
                losers = at(prev["places"])
                if spec >= prev["spec"]:
                    top = max(prev["places"], key=lambda p: p[2] != ":root")[2]
                    why = (f"{selector} is more specific than {top}" if spec > prev["spec"]
                           else f"it loads after "
                           f"{' and '.join(dict.fromkeys(p[0] for p in prev['places']))} "
                           "with a selector as specific")
                    notes.append(Item(f"{sheet}:{d.line}", d.name, (
                        f"sets the base value {d.value.strip()} on {selector}, which wins over "
                        f"{prev['text']} at {losers} as the browser decides: {why}; "
                        f"{d.value.strip()} is read. Keep one value: remove the other at "
                        f"{losers}, or this one if {prev['text']} is the value you mean")))
                    for p in prev["places"]:
                        if p[3] is not None:
                            blank(*p[3])
                    if key in names:
                        blank(i, d.line, d.name)
                        won[key] = read[1]
                    current[key] = {"read": read, "spec": spec, "text": d.value.strip(),
                                    "places": [place]}
                else:
                    blank(i, d.line, d.name)
                    kept.append(Item(f"{sheet}:{d.line}", d.name, (
                        f"sets the base value {d.value.strip()} on {selector}, which loses to "
                        f"{prev['text']} at {losers} as the browser decides: that is more "
                        f"specific, so {prev['text']} is kept and {sheet}'s other values still "
                        f"pair with it. Remove it from {sheet}, or change it at {losers} if "
                        f"{d.value.strip()} is the value you mean")))
    return ["\n".join(rows) for rows in lines], won


def _same(a: Tuple[str, Any], b: Tuple[str, Any]) -> bool:
    """Whether two readings are one value: equal, or two spellings of one
    color."""
    if a[1] == b[1]:
        return True
    return isinstance(a[1], str) and isinstance(b[1], str) and a[1].upper() == b[1].upper()


def _usable(ctx: str, first: Mapping[str, Sequence[str]],
            together: Mapping[str, Sequence[str]]) -> bool:
    """Whether a context read together can be kept: each of its axes is the
    system's with the value, or one only the stylesheets bring."""
    for pair in ctx.split(","):
        axis, _, value = pair.partition(":")
        values = first.get(axis, together.get(axis, ()))
        if value not in values:
            return False
    return True
