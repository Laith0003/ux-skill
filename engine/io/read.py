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
its own. A value a stylesheet sets differently from the system is listed
under Not read, and the system's is kept. Every file read is in the
report's also_read, so the intake step checks and backs up each one.
"""
from __future__ import annotations

import json
import re
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.errors import InputError
from engine.foundations.tokens import TokenSet, alias_target, css_property, is_alias
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
    file and foundation stylesheet, built output left out."""
    from engine.existing import detect_existing_system
    found = detect_existing_system(p)
    return [(s["kind"], s["path"]) for s in found.get("sources", [])
            if s["kind"] in (*_TOKEN_KINDS, _SHEET_KIND)]


def detect_format(path: Any, label: str = "--from") -> str:
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
    raise InputError(f"{label} {p} is not a format uxskill reads by its name; pass --format "
                     f"{names}")


def read_system(path: Any, fmt: str = "auto", label: str = "--from",
                second_modes: Optional[Mapping[str, str]] = None,
                modes_label: str = "--figma-mode") -> Imported:
    """Read one system with the importer for its format (engine.io.read_any).
    `second_modes` (collection -> mode) is for a Figma export only. A
    project folder is read as the set system detect proposes."""
    if fmt not in CHOICES:
        names = ", ".join(CHOICES[:-1]) + " or " + CHOICES[-1]
        raise InputError(f"--format is {fmt}; pass {names}")
    found = detect_format(path, label) if fmt == "auto" else fmt
    if found == "project":
        return read_sources(_proposed(Path(path).expanduser(), label), "auto", label,
                            second_modes, modes_label)
    if second_modes and found != "figma":
        raise InputError(f"{modes_label} is for a Figma variables export, and {label} "
                         f"{Path(path).name} is read as {found}; drop {modes_label}")
    from engine.io import read_any
    options = {"second_modes": dict(second_modes)} if second_modes else {}
    imported = read_any(path, found, label, **options)
    imported.report.ownership = ownership_line(imported)
    return imported


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
                 modes_label: str = "--figma-mode") -> Imported:
    """Read one source, or several as one system (see the module
    docstring). `paths` is a path or a list of them; `fmt` applies to the
    first. Raises InputError naming `label` and the fix."""
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
    first = read_system(paths[0], fmt, label, second_modes, modes_label)
    if len(paths) == 1:
        return first
    sheets: List[Tuple[Source, str]] = []
    for p in paths[1:]:
        kind = detect_format(p, label)
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

    def __init__(self, first_lines: int, sheets: Sequence[Tuple[Source, str]]) -> None:
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
            return self.where(int(m.group(1))) or "the system"
        return re.sub(re.escape(_MARK) + r":(\d+)", sub, message).replace(
            _MARK, self.parts[0][2])

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
    text = base + "\n" + "\n".join(t for _, t in sheets)
    places = _Places(base.count("\n") + 1, sheets)
    together = import_css(text, Source(_MARK, "css", "0" * 64, len(text)))
    names = {css_property(t.path)[2:]: t.path for t in first.tokens.tokens()}
    declared = {m.group(1)[2:] for _, t in sheets for m in _DECLARED.finditer(t)}
    axes: Dict[str, Tuple[str, ...]] = {a: tuple(v) for a, v in first.tokens.axes.items()}
    for a, v in together.tokens.axes.items():
        axes.setdefault(a, tuple(v))
    ts = TokenSet(axes)
    added_modes = 0
    for t in first.tokens.tokens():
        theirs = together.tokens.get(css_property(t.path)[2:]) \
            if together.tokens.has(css_property(t.path)[2:]) else None
        modes = dict(t.modes)
        if theirs is not None:
            for ctx, v in theirs.modes.items():
                if ctx not in modes and _usable(ctx, first.tokens.axes, together.tokens.axes):
                    modes[ctx] = _rename(v, names)
                    added_modes += 1
        ts.add(replace(t, modes=modes, extensions=dict(t.extensions)))
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
    report.notes = list(old.notes)
    report.not_read = list(old.not_read)
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
