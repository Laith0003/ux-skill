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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

from engine.foundations.errors import InputError, _brief_text
from engine.foundations.tokens import TokenSet

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

    @classmethod
    def of(cls, source: Source, ts: TokenSet, entries: int) -> "ImportReport":
        """A report on `ts` as read from `source`, which held `entries`
        entries that could be tokens. Types are counted in sorted order."""
        counts: Dict[str, int] = {}
        for t in ts.tokens():
            counts[t.type] = counts.get(t.type, 0) + 1
        return cls(source, entries, len(ts.tokens()), dict(sorted(counts.items())),
                   {a: list(v) for a, v in ts.axes.items()})

    def to_dict(self) -> Dict[str, Any]:
        return {"source": self.source.to_dict(),
                "also_read": [a.to_dict() for a in self.also_read],
                "entries": self.entries, "tokens": self.tokens,
                "by_type": dict(self.by_type), "axes": {a: list(v) for a, v in self.axes.items()},
                "renamed": [i.to_dict() for i in self.renamed],
                "notes": [i.to_dict() for i in self.notes],
                "mapped": [i.to_dict() for i in self.mapped],
                "not_read": [i.to_dict() for i in self.not_read]}

    def markdown(self) -> str:
        s = self.source
        lines = ["# Import report", "",
                 f"Read {s.path} ({s.format}, {s.size} bytes, sha256 {s.sha256[:12]}): "
                 f"{self.entries} entries, {self.tokens} tokens.", "",
                 *[f"Also read {a.path} ({a.format}, {a.size} bytes, sha256 {a.sha256[:12]})."
                   for a in self.also_read], *([""] if self.also_read else []),
                 "## What was read", "", "| Type | Tokens |", "|---|---|"]
        lines += [f"| {t} | {n} |" for t, n in self.by_type.items()]
        if self.axes:
            modes = "; ".join(f"{a} ({v[0]} is the base, {v[1]})" for a, v in self.axes.items())
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
            lines += ["Nothing below was guessed; each entry says how to write it so it can be "
                      "read.", "", *(i.line() for i in self.not_read)]
        else:
            lines.append("Nothing was left unread.")
        return "\n".join(lines) + "\n"


@dataclass
class Imported:
    """An imported system: its tokens in the source's own names, the
    report, and for a CSS source how each mode axis was switched there
    (axis -> (selector for the non-base value, media query or "")) and
    which scheme it opens (system, light or dark), so the system can be
    written back the way it came."""
    tokens: TokenSet
    report: ImportReport
    forms: Mapping[str, Tuple[str, str]] = field(default_factory=dict)
    scheme: str = "system"
