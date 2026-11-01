"""What an importer hands back: the tokens, in the source's own names, and
a report of what it read.

The report records the source (path, format, sha256, size), how many
entries the source held and how many became tokens, the token types and
the modes, and four lists: entries renamed on the way in, entries read
with a note, colors mapped into sRGB (an out-of-gamut color is mapped by
CSS Color 4 gamut mapping, never refused), and entries not read. Every list
item names where the entry sits and says what happened or how to write it
so it can be read. Nothing is guessed: an entry with more than one reading
is not read.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from engine.existing.record import read_record
from engine.foundations.errors import InputError, _brief_text
from engine.foundations.tokens import ROOT_BASE, TokenSet

# Every format the importers read.
FORMATS: Tuple[str, ...] = ("dtcg", "css", "tailwind", "tailwind-json", "markdown", "figma")


@dataclass(frozen=True)
class Item:
    """One entry of a report list: where it sits in the source (file and
    line, or file and path), its name as the source writes it, and what
    happened or the fix."""
    where: str
    name: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {"where": self.where, "name": self.name, "message": self.message}

    def line(self) -> str:
        name = f" `{self.name}`" if self.name else ""
        return f"- {self.where}{name}: {self.message}"


@dataclass(frozen=True)
class Folded(Item):
    """Report lines of one kind folded into one: the line says how many and
    names a few; to_dict() keeps every one under items."""
    items: Tuple[Item, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = dict(super().to_dict())
        out["items"] = [i.to_dict() for i in self.items]
        return out


# A Not read list longer than this is folded (fold); a folded line names
# this many entries and counts the rest.
FOLD_OVER = 12
FEW = 3


def _namespace(name: str) -> str:
    """The first word of a name, as its namespace: color for --color-ink,
    color.text.body or colorInk is not split (one word)."""
    words = [w for w in re.split(r"[.\-/_\s]+", name.lstrip("-$")) if w]
    return words[0] if words else ""


def _few(names: List[str]) -> str:
    shown = names if len(names) <= FEW + 1 else names[:FEW] + [f"{len(names) - FEW} more"]
    return shown[0] if len(shown) == 1 else ", ".join(shown[:-1]) + " and " + shown[-1]


def fold(items: List[Item], over: int = FOLD_OVER) -> List[Item]:
    """A long list with the entries of one file, one namespace and one
    message folded into one line at the place of the first: how many, a
    few of their names, and the message they share. A list of `over`
    entries or fewer comes back as it is, and so does an entry alone of
    its kind. Each Folded keeps every entry it stands for."""
    if len(items) <= over:
        return list(items)

    def key(i: Item) -> Tuple[str, str, str]:
        return i.where.split(":")[0], _namespace(i.name), i.message

    groups: Dict[Tuple[str, str, str], List[Item]] = {}
    for i in items:
        groups.setdefault(key(i), []).append(i)
    out: List[Item] = []
    for i in items:
        group = groups[key(i)]
        if len(group) < 2 or isinstance(i, Folded):
            out.append(i)
            continue
        if group[0] is not i:
            continue
        ns = key(i)[1]
        under = f" under {ns}" if ns else ""
        out.append(Folded(i.where, "", (
            f"{len(group)} entries{under} ({_few([g.name for g in group])}); for each: "
            f"{i.message}"), tuple(group)))
    return out


@dataclass(frozen=True)
class Mapped:
    """A color outside sRGB that was read by CSS Color 4 gamut mapping:
    where it sits, its name, the value as written, the hex it was read as,
    and the OKLab distance between the two."""
    where: str
    name: str
    original: str
    hex: str
    distance: float

    @classmethod
    def of(cls, where: str, name: str, gamut: Any) -> "Mapped":
        """From the GamutMapped that values_in.read_value reported."""
        return cls(where, name, gamut.original, gamut.hex, gamut.distance)

    def to_dict(self) -> Dict[str, Any]:
        return {"where": self.where, "name": self.name, "original": self.original,
                "hex": self.hex, "distance": round(self.distance, 4)}

    def line(self) -> str:
        name = f" `{self.name}`" if self.name else ""
        return (f"- {self.where}{name}: {self.original} is outside sRGB; read as {self.hex}, "
                f"the same lightness and hue with less chroma (OKLab distance "
                f"{self.distance:.4f})")


@dataclass(frozen=True)
class Source:
    """The file an import read, identified by its digest, so a later write
    can tell whether the source changed underneath it."""
    path: str
    format: str
    sha256: str
    size: int

    def __post_init__(self) -> None:
        if self.format not in FORMATS:
            raise ValueError(f"format {self.format!r} is not one of {list(FORMATS)}; pass one "
                             "of those")

    def to_dict(self) -> Dict[str, Any]:
        return {"path": self.path, "format": self.format, "sha256": self.sha256,
                "size": self.size}


def read_source(path: Any, fmt: str, label: str) -> Tuple[Source, str]:
    """The source file's record and its text. UTF-8 (a leading byte order
    mark dropped) or UTF-16 with its mark. Raises InputError naming `label`
    and the fix."""
    p = Path(path).expanduser()
    if p.is_dir():
        raise InputError(f"{label} {p} is a folder; pass the file that holds the system, for "
                         "example tokens.json")
    try:
        data = p.read_bytes()
    except OSError as exc:
        raise InputError(f"{label} {p} cannot be read ({exc.strerror or exc}); pass the path of "
                         "the file that holds the system") from None
    try:
        text = _brief_text(data)
    except UnicodeDecodeError:
        raise InputError(f"{label} {p} is not UTF-8 text; save it as UTF-8 and pass it "
                         "again") from None
    return Source(str(p), fmt, hashlib.sha256(data).hexdigest(), len(data)), text


def recorded(source: Source) -> Optional[bool]:
    """What the record of the files the engine wrote, in the source's
    folder, says of the source: True when it lists the file at the digest
    it was read at, False when at another (the file changed since the
    engine wrote it), None when it does not list the file."""
    p = Path(source.path).expanduser()
    listed = read_record(p.parent).get(p.name)
    return None if listed is None else listed == source.sha256[:12]


@dataclass
class ImportReport:
    source: Source
    entries: int
    tokens: int
    by_type: Dict[str, int]
    axes: Dict[str, List[str]]
    renamed: List[Item] = field(default_factory=list)
    notes: List[Item] = field(default_factory=list)
    not_read: List[Item] = field(default_factory=list)
    mapped: List[Mapped] = field(default_factory=list)
    # Other files read with the source (a sibling dark file), each with its
    # digest, so a later write can tell whether any of them changed.
    also_read: List[Source] = field(default_factory=list)
    # Values read for a mode beside the base (a dark value), counted apart
    # from the entries, so an entry means a name in every format.
    mode_values: int = 0
    # What the owner must see first, such as a file that holds values and
    # gave no token; written right under the count.
    headline: List[str] = field(default_factory=list)
    # Who owns the source and which marker said so (ownership_line), when
    # a command read it; written under the first line.
    ownership: str = ""

    @classmethod
    def of(cls, source: Source, ts: TokenSet, entries: int,
           mode_values: Optional[int] = None) -> "ImportReport":
        """A report on `ts` as read from `source`, which held `entries`
        names that could be tokens. `mode_values` defaults to the mode
        values the tokens hold. Types are counted in sorted order."""
        counts: Dict[str, int] = {}
        for t in ts.tokens():
            counts[t.type] = counts.get(t.type, 0) + 1
        if mode_values is None:
            mode_values = sum(len(t.modes) for t in ts.tokens())
        return cls(source, entries, len(ts.tokens()), dict(sorted(counts.items())),
                   {a: list(v) for a, v in ts.axes.items()}, mode_values=mode_values)

    def to_dict(self) -> Dict[str, Any]:
        return {"source": self.source.to_dict(),
                "also_read": [a.to_dict() for a in self.also_read],
                "entries": self.entries, "tokens": self.tokens,
                "mode_values": self.mode_values,
                "by_type": dict(self.by_type), "axes": {a: list(v) for a, v in self.axes.items()},
                "renamed": [i.to_dict() for i in self.renamed],
                "notes": [i.to_dict() for i in self.notes],
                "mapped": [i.to_dict() for i in self.mapped],
                "not_read": [i.to_dict() for i in self.not_read],
                **({"headline": list(self.headline)} if self.headline else {}),
                **({"ownership": self.ownership} if self.ownership else {})}

    def markdown(self) -> str:
        s = self.source
        lines = ["# Import report", "",
                 f"Read {s.path} ({s.format}, {s.size} bytes, sha256 {s.sha256[:12]}): "
                 f"{self.entries} entries, {self.tokens} tokens.", "",
                 *([self.ownership, ""] if self.ownership else []),
                 *(line for h in self.headline for line in (h, "")),
                 f"{self.mode_values} mode value{'' if self.mode_values == 1 else 's'}.", "",
                 *[f"Also read {a.path} ({a.format}, {a.size} bytes, sha256 {a.sha256[:12]})."
                   for a in self.also_read], *([""] if self.also_read else []),
                 "## What was read", "", "| Type | Tokens |", "|---|---|"]
        lines += [f"| {t} | {n} |" for t, n in self.by_type.items()]
        if self.axes:
            modes = "; ".join(
                f"{a} ({v[0]} is the base, {v[1]})" if v[0] != ROOT_BASE else
                f"{a} (the values set with no mode are the base; "
                f"{'mode' if len(v) == 2 else 'modes'} {', '.join(v[1:])})"
                for a, v in self.axes.items())
            lines += ["", f"Modes: {modes}."]
        else:
            lines += ["", "Modes: none; every token has one value."]
        if self.renamed:
            lines += ["", "## Renamed on the way in", "", *(i.line() for i in self.renamed)]
        if self.notes:
            lines += ["", "## Read with a note", "", *(i.line() for i in self.notes)]
        if self.mapped:
            lines += ["", "## Mapped into sRGB", "",
                      "CSS Color 4 gamut mapping: each color below lies outside sRGB and was "
                      "read at its own lightness and hue with the chroma lowered until it fits.",
                      "", *(i.line() for i in self.mapped)]
        lines += ["", "## Not read", ""]
        if self.not_read:
            folded = fold(self.not_read)
            lines += ["Nothing below was guessed; each entry says how to write it so it can be "
                      "read."
                      + (" Entries of one file, namespace and message share one line; the JSON "
                         "result lists each." if len(folded) < len(self.not_read) else ""),
                      "", *(i.line() for i in folded)]
        else:
            lines.append("Nothing was left unread.")
        return "\n".join(lines) + "\n"


@dataclass
class Imported:
    """An imported system: its tokens in the source's own names, the
    report, and for a CSS source how each mode axis was switched there
    (axis -> (the selector for the non-base value as the file writes it,
    or "" when only the media query sets it; the media query, or "")),
    which scheme it opens (system, light or dark), the Tailwind namespace
    resets it writes (`--color-*: initial`) and its `@custom-variant dark`
    declaration as written, so the system can be written back in the forms
    it came in (css_in.write_css, tailwind_out.to_tailwind). `owned` is
    what the source's ownership record says, never its token names: True
    for a file the engine wrote and nobody changed since, which the record
    in its folder lists at the digest it was read at (recorded), or a
    stylesheet whose engine digest stamp still matches, or a tokens file
    the record does not list that carries the engine's extension key on
    its root (one written before the record existed). `figma`, for a Figma
    export, holds each collection the file owns with its modes in order,
    each as [mode name, the context it was read into, or None when it was
    not read] under "collections", each unread mode with the context its
    name gives (or None) under "unread", each token's [collection,
    variable name] under "variables" and its scopes under "scopes", and
    every variable name the export declares, read or not, with the
    collections it sits in, under "declared", and every collection name
    under "declared_collections", so an extension can be written in the
    file's own collections, names, modes and scopes without taking a name
    the file uses."""
    tokens: TokenSet
    report: ImportReport
    forms: Mapping[str, Tuple[str, str]] = field(default_factory=dict)
    scheme: str = "system"
    resets: Tuple[str, ...] = ()
    variant: str = ""
    owned: bool = False
    figma: Mapping[str, Any] = field(default_factory=dict)


def owned_by(imported: Imported) -> str:
    """Which marker made `imported` the engine's own: "record" (the record
    of the files the engine wrote lists it at the digest it was read at),
    "stamp" (a stylesheet carrying the engine's digest stamp that still
    matches), "extension key" (a tokens file the record does not list, with
    the engine's extension key on its root), or "" when it is not."""
    if not imported.owned:
        return ""
    source = imported.report.source
    listed = recorded(source)
    if listed is True:
        return "record"
    if source.format in ("css", "tailwind"):
        return "stamp"
    return "extension key" if source.format == "dtcg" and listed is None else "record"


def ownership_line(imported: Imported) -> str:
    """The sentence an import report gives on who owns the source and why."""
    report = imported.report
    name = Path(report.source.path).name
    also = [Path(a.path).name for a in report.also_read]
    marker = owned_by(imported)
    if marker == "record":
        return (f"{name} is ux-skill's own: the record of the files ux-skill wrote in its folder "
                "(.uxskill/files.json) lists it at the digest it was read at.")
    if marker == "stamp":
        return f"{name} is ux-skill's own: it carries ux-skill's digest stamp, which still matches."
    if marker == "extension key":
        return (f"{name} is read as ux-skill's own because its root carries ux-skill's extension "
                "key. Its folder has no record of the files ux-skill wrote, so a hand edit to it "
                "is not seen; build the system into that folder again to write the record, or "
                "remove the key if the file is yours.")
    files = name if not also else ", ".join([name, *also[:-1]]) + " and " + also[-1]
    them = "it" if not also else "them"
    return (f"{files} {'is' if not also else 'are'} not ux-skill's own (no record, digest stamp "
            f"or extension key says so), so ux-skill never rewrites {them}: what it adds goes "
            f"beside {them}, and an export goes into a folder of its own.")
