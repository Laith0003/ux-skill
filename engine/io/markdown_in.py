"""Import a system that lives only in markdown rule files.

Read as tokens:
- a table with a name column (headed Token, Name, Variable or Role) and a
  value column (Value, Hex, Color, Size, Px, Rem, Ms or Duration). A further
  column headed with the non-base value of a mode axis (Dark, High
  contrast, Compact, Reduced motion, Rtl) is that mode, one column per
  axis;
- a table with a name column and mode columns only: the base column (Light,
  Default, Standard, or the first) and one column per axis. Two columns
  that name no known axis make an axis named after both headers, the first
  the base (Brand and Partner give brand-partner). Each such table is
  noted;
- a column that names each token's alias (Alias, References, Maps to, or
  Token beside a name column) reads as the value where it holds a
  reference, {a.b} or a backticked name;
- a palette keyed by step (a Step column of 50, 100 ... 900 and a column per
  family, or the steps across the top): each cell is a primitive named
  family.step;
- a list item whose name is in backticks: "- `space.2`: 8px" or "= 8px".

A unit in a column header (Value (px), Size [rem]) or in the heading above
(## Spacing (px), ## Motion, in ms) is the unit of a bare number there. A
bare number for a size or a duration with no unit anywhere is not read.
Do and Avoid tables (Do and Don't, Use and Avoid, Good and Bad) are
guidance: they make no axis and join the file's rule note.

A name may be written plain, in bold or in backticks, with dots, dashes or
slashes (a slash reads as a dot, and the report lists it as renamed); a
value may be a literal, `{other.token}` or var(--other). Prose, tables
without a name column, list items without a backticked name and code
blocks are not tokens; a css code block is noted with the fix. A row
whose name is not a token name, a value with no single reading, a column
or a table left out and a reference to a name no file defines are listed
under "Not read" with their file and line. A name set twice keeps its
first value, and a second, different value is reported. An oklch() or
oklab() color outside sRGB is mapped into it and reported, never refused.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from engine.foundations.errors import InputError, _brief_text
from engine.foundations.modes import AXES
from engine.foundations.values import GENERIC_FAMILIES, STROKE_STYLES
from engine.foundations.tokens import Token, TokenSet
from engine.io.mode_words import axis_of, is_base, mode_of, words as name_words
from engine.io.report import Imported, ImportReport, Item, Mapped, Source
from engine.io.values_in import (COLOR_KEYWORDS, CSS_KEYWORDS, EASING_KEYWORDS, GamutMapped,
                                 NotRead, css_alias, read_value, split_top)

NAME_HEADERS = ("token", "name", "variable", "role", "token name", "css variable")
VALUE_HEADERS = ("value", "hex", "color", "size", "px", "rem", "ms", "duration")
PROSE_HEADERS = ("notes", "note", "description", "usage", "use", "purpose", "meaning",
                 "example", "when", "why", "do", "don't", "dont")
# A column that names each token's alias, read as its value where it holds
# a reference. Token is one too, beside another name column.
ALIAS_HEADERS = ("alias", "aliases", "reference", "references", "maps to", "points to",
                 "refers to")
# Do and Avoid tables: guidance, never a mode axis. A table is guidance
# when it has a header from each list and nothing but guidance and prose.
GUIDANCE_DO = ("do", "use", "good", "correct", "right", "yes", "always", "prefer")
GUIDANCE_AVOID = ("don't", "dont", "do not", "avoid", "bad", "incorrect", "wrong", "no",
                  "never", "instead", "don't use")
# The first column of a palette keyed by step.
STEP_HEADERS = ("step", "steps", "shade", "shades", "scale", "tone", "tones", "level", "")

_NAME = re.compile(r"(?:--)?[A-Za-z0-9_-]+(?:[./][A-Za-z0-9_-]+)*")
_LIST = re.compile(r"\s*(?:[-*+]|\d+[.)])\s+`([^`]+)`\s*[:=]\s*(.+?)\s*$")
_DELIMITER = re.compile(r"\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$")
_FENCE = re.compile(r"\s{0,3}(`{3,}|~{3,})\s*([^`\s]*)")
_BRACE = re.compile(r"\{\s*([^{}\s]+)\s*\}")
_AXIS_WORD = re.compile(r"[a-z][a-z0-9-]*")
# The name column, when a table has several name-like headers: the one
# that holds the token's own name wins over a role or a label.
_NAME_PREFERENCE = ("token", "token name", "variable", "css variable", "name", "role")
# Words a mode column's header may carry around the mode's name.
_MODE_WORDS = ("mode", "theme", "scheme", "value", "contrast", "density", "motion",
               "direction", "hex", "color", "default")
# Every value of an engine axis: a header holding exactly one of them
# names that mode, whatever else it says ("Light (default)", "Dark hex").
_MODE_VALUES = frozenset(v for values in AXES.values() for v in values)
# Lowercase words that are values, not prose.
_KEYWORDS = frozenset((*CSS_KEYWORDS, *COLOR_KEYWORDS, *EASING_KEYWORDS, *STROKE_STYLES,
                       *GENERIC_FAMILIES, "none"))
_PLAIN = re.compile(r"[a-z]+(?:'[a-z]+)?")
_SENTENCE_END = re.compile(r"[.!?](?:\s|$)")
_VALUEISH = re.compile(r"[0-9#({\"']")
_BULLET = re.compile(r"\s*(?:[-*+]|\d+[.)])\s")
# Lines that end a block, so a line four spaces in right after one opens
# an indented code block: an ATX heading, a setext underline and a
# thematic break.
_BLOCK_END = re.compile(r" {0,3}(?:#{1,6}(?:\s|$)|=+\s*$|-{2,}\s*$"
                        r"|(?:\*\s*){3,}$|(?:-\s*){3,}$|(?:_\s*){3,}$)")
_LOOP = "references only itself through a loop of references; give one of them a value"
# A unit at the end of a header, Value (px) or Size [rem], and in a heading.
_HEADER_UNIT = re.compile(r"\s*[(\[]\s*(px|rem|ms|s)\s*[)\]]\s*$", re.I)
_HEADING = re.compile(r" {0,3}#{1,6}\s+(.*?)\s*#*\s*$")
_HEADING_UNIT = re.compile(r"[(\[]\s*(px|rem|ms|s)\s*[)\]]|\bin (px|rem|ms)\b", re.I)
_BARE_NUMBER = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)")
_STEP = re.compile(r"\d+")
# Words in a name that say its number is a size or a duration, and words
# that say it is a plain number whatever else the name says.
_SIZE_WORDS = frozenset(("space", "spacing", "gap", "padding", "margin", "inset", "radius",
                         "radii", "rounded", "corner", "corners", "size", "sizes", "width",
                         "height", "gutter", "offset", "blur", "spread", "indent", "breakpoint"))
_TIME_WORDS = frozenset(("duration", "delay"))
_UNITLESS_WORDS = frozenset(("line", "leading", "weight", "opacity", "z", "index", "zindex",
                             "ratio", "scale", "factor", "alpha", "order", "count", "flex"))


def _and(words: Sequence[str]) -> str:
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + f" and {words[-1]}"


def _split(line: str) -> List[str]:
    """The cells of a table line, an escaped pipe kept as text."""
    text = line.strip()
    text = text.removeprefix("|")
    if text.endswith("|") and not text.endswith("\\|"):
        text = text[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", text)]


def _unquote(cell: str) -> str:
    cell = cell.strip()
    return cell[1:-1].strip() if len(cell) > 1 and cell[0] == cell[-1] == "`" else cell


def _header(cell: str) -> str:
    """A header as written, without emphasis or backticks."""
    return re.sub(r"\s+", " ", cell.replace("*", "").replace("`", "")).strip()


def _mode_word(header: str) -> str:
    """The mode a column header names ("Dark mode" is dark), or "" when it
    cannot name one."""
    hits = {w for w in re.findall(r"[a-z0-9]+", header.lower()) if w in _MODE_VALUES}
    if len(hits) == 1:
        return hits.pop()
    bare = re.sub(r"\([^)]*\)", " ", header.lower())
    words = [w for w in bare.split() if w not in _MODE_WORDS]
    slug = re.sub(r"[^a-z0-9]+", "-", " ".join(words)).strip("-")
    return slug if _AXIS_WORD.fullmatch(slug) else ""


def _prose_header(header: str) -> bool:
    """True for a column of prose: Notes, Usage, When to use and the like."""
    return header in PROSE_HEADERS or any(w in PROSE_HEADERS for w in header.split())


def _prose(text: str) -> bool:
    """True when a value is a rule written in words, not a value: it holds a
    backtick or ends a sentence, or one of its comma parts has two or more
    plain lowercase words that are not CSS keywords, or more than four
    words and no number. A font list (Inter, system-ui, sans-serif) is not
    prose: each part is a name of a few words."""
    if "`" in text or _SENTENCE_END.search(text):
        return True
    for part in split_top(text):
        if part[:1] in "\"'":
            continue
        words = part.split()
        plain = [w for w in words if _PLAIN.fullmatch(w) and w not in _KEYWORDS]
        if len(plain) >= 2 or (len(words) > 4 and not _VALUEISH.search(part)):
            return True
    return False


_FONT_PART = re.compile(r"-?[A-Za-z][A-Za-z0-9 _-]*")
_TYPE_CONTEXT = re.compile(r"font|family|typeface", re.I)


def _font_shaped(text: str) -> bool:
    """True for an unquoted or quoted comma list of names, the shape of a
    font stack (Inter, system-ui, sans-serif)."""
    parts = split_top(text)
    return len(parts) > 1 and all(
        p and (p[0] in "\"'" and p[-1:] == p[0] or _FONT_PART.fullmatch(p))
        and len(p.split()) <= 5 for p in parts)


def _font_evidence(text: str, context: str) -> bool:
    """True when a comma list of names is a font stack for certain: a part
    is quoted, it ends in a generic family, or its name or column header
    says font, family or typeface. A bare "type" is no evidence: type.sizes
    and a Type column of sizes are common."""
    parts = split_top(text)
    last = parts[-1].lower()
    return (any(p[0] in "\"'" for p in parts) or last in GENERIC_FAMILIES
            or last.startswith("ui-") or bool(_TYPE_CONTEXT.search(context)))


def _valueish(cell: str) -> bool:
    """True when a cell could hold a value: a digit, a hex, a function, a
    reference, a quote or a CSS keyword."""
    text = _unquote(cell)
    return bool(_VALUEISH.search(text)) or any(p.lower() in _KEYWORDS
                                                for p in split_top(text))


def _path(name: str) -> str:
    name = name.removeprefix("--")
    return name.replace("/", ".")


def _header_unit(header: str) -> Tuple[str, str]:
    """(the header without its unit, the unit) for a header that carries
    one (Value (px), Size [rem]) or is one (Px); the unit is "" otherwise."""
    m = _HEADER_UNIT.search(header)
    if m:
        return header[:m.start()].strip(), m.group(1).lower()
    return header, header.lower() if header.lower() in ("px", "rem", "ms") else ""


def _heading_unit(text: str) -> str:
    """The unit a heading names for the values below it, or ""."""
    m = _HEADING_UNIT.search(text)
    return (m.group(1) or m.group(2)).lower() if m else ""


def _needs_unit(path: str) -> str:
    """"size" or "duration" when a name says its number needs a unit, or
    "" when it may be a plain number."""
    found = name_words(path.replace(".", " "))
    if found & _UNITLESS_WORDS:
        return ""
    if found & _TIME_WORDS:
        return "duration"
    return "size" if found & _SIZE_WORDS else ""


def _refish(cell: str) -> bool:
    """True when a cell holds a reference: {a.b}, var(--a) or a backticked
    token name."""
    text = cell.strip()
    inner = _unquote(text)
    if _BRACE.fullmatch(inner) or css_alias(inner) is not None:
        return True
    return len(text) > 1 and text[0] == text[-1] == "`" and bool(_NAME.fullmatch(inner))


def _as_reference(cell: str) -> str:
    """A reference cell written as the value reader reads it: a backticked
    name becomes {name}."""
    inner = _unquote(cell)
    if _BRACE.fullmatch(inner) or css_alias(inner) is not None:
        return inner
    return "{" + inner + "}"


def _token_named(cell: str) -> bool:
    """True when a cell is written as a token's name: in backticks, or with
    a dot, a dash or a slash in it."""
    text = re.sub(r"^(\*{1,2}|_{1,2})(.+)\1$", r"\2", cell.strip())
    inner = _unquote(text)
    return bool(_NAME.fullmatch(inner)) and (text != inner or any(c in inner for c in ".-/"))


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", _unquote(text).lower()).strip("-")
    return slug if _AXIS_WORD.fullmatch(slug) else ""


@dataclass
class _Entry:
    """A name as read: where, as written, its value text per context and
    the column each context came from ("" for a list item)."""
    where: str
    written: str
    values: Dict[str, str]
    labels: Dict[str, str]
    decoded: Dict[str, Tuple[str, Any]] = field(default_factory=dict)
    notes: List[Item] = field(default_factory=list)
    mapped: List[Mapped] = field(default_factory=list)
    # context -> why its bare number was not read (it needs a unit)
    bare: Dict[str, str] = field(default_factory=dict)
    # the contexts read from an alias column
    aliased: Tuple[str, ...] = ()


@dataclass
class _Table:
    """How a table is read: its name column, its base column, its alias
    column, a column per mode axis (column, axis, values) and the unit each
    column's header names; or a palette, or guidance. `dropped` lists each
    column (or the whole table, when `whole`) left out, with the fix."""
    name: int = -1
    base: int = -1
    alias: int = -1
    modes: List[Tuple[int, str, Tuple[str, str]]] = field(default_factory=list)
    units: Dict[int, str] = field(default_factory=dict)
    dropped: List[Tuple[str, str]] = field(default_factory=list)
    whole: bool = False
    palette: str = ""
    guidance: str = ""


def _guidance(raw: List[str], low: List[str]) -> str:
    """The label of a Do and Avoid table ("Do and Avoid"), or "" when the
    table is not guidance."""
    body = [c for c, h in enumerate(low) if h not in NAME_HEADERS and h]
    kinds = GUIDANCE_DO + GUIDANCE_AVOID
    if any(low[c] in GUIDANCE_DO for c in body) and any(low[c] in GUIDANCE_AVOID for c in body) \
            and all(low[c] in kinds or _prose_header(low[c]) for c in body):
        return _and([raw[c] for c in body if low[c] in kinds])
    return ""


def _palette(raw: List[str], low: List[str], rows: List[List[str]]) -> Optional[_Table]:
    """A palette keyed by step: steps down the first column and a column
    per family ("down"), or steps across the top and a row per family
    ("across"). None when the table is not one."""
    if len(raw) < 2:
        return None
    if all(_STEP.fullmatch(h) for h in raw[1:]):
        if any(_valueish(r[c]) for r in rows for c in range(1, min(len(r), len(raw)))):
            return _Table(name=0, palette="across")
        return None
    if low[0] in NAME_HEADERS or low[0] in VALUE_HEADERS:
        return None
    steps = [_unquote(r[0]) for r in rows if r and r[0].strip()]
    if not steps or not all(_STEP.fullmatch(x) for x in steps):
        return None
    families = [c for c in range(1, len(raw)) if not _prose_header(low[c])]
    if any(low[c] in VALUE_HEADERS or is_base(raw[c]) or mode_of(raw[c]) for c in families):
        return None
    if low[0] not in STEP_HEADERS and not any(
            _valueish(r[c]) for r in rows for c in families if c < len(r) and r[c].strip()):
        return None
    return _Table(name=0, palette="down")


def _table(raw: List[str], rows: List[List[str]]) -> Optional[_Table]:
    """How a table with these headers and rows is read; None when it holds
    no tokens (no name column, or only prose beside it)."""
    split = [_header_unit(h) for h in raw]
    low = [b.lower() for b, _ in split]
    guidance = _guidance(raw, low)
    if guidance:
        return _Table(guidance=guidance)
    palette = _palette(raw, low, rows)
    if palette is not None:
        palette.units = {c: u for c, (_, u) in enumerate(split) if u}
        return palette
    name = next((low.index(h) for h in _NAME_PREFERENCE if h in low), None)
    if name is None:
        return None
    alias = next((c for c, h in enumerate(low) if c != name and h in ALIAS_HEADERS), -1)
    value = [c for c, h in enumerate(low) if c not in (name, alias) and h in VALUE_HEADERS]
    other = [c for c, h in enumerate(low)
             if c not in (name, alias) and h and h not in VALUE_HEADERS and h not in NAME_HEADERS
             and not _prose_header(h)]
    if alias < 0 and not value and not other and low[name] == "token":
        # A Token column of references beside a column of names: the names
        # are the tokens, and the Token column holds what each aliases.
        named = next((c for c, h in enumerate(low) if c != name and h in NAME_HEADERS), None)
        cells = [(r[named], r[name]) for r in rows if named is not None and len(r) > max(named,
                                                                                         name)]
        if named is not None and cells and all(_token_named(n) for n, _ in cells if n.strip()) \
                and any(_refish(t) for _, t in cells):
            name, alias = named, name
    table = _Table(name, alias=alias, units={c: u for c, (_, u) in enumerate(split) if u})

    def place(columns: List[int], base: str) -> None:
        held: Dict[str, str] = {}
        for c in columns:
            axis = mode_of(split[c][0], [raw[c]])
            if axis is None:
                table.dropped.append((raw[c], (
                    "names no mode, so its column was not read; head it with a mode name such "
                    "as Dark or High contrast, or put it in a table of its own with a base "
                    "column")))
            elif axis in held:
                table.dropped.append((raw[c], (
                    f"is a second column for the {axis} axis, which {held[axis]} holds, so it "
                    "was not read; keep one column per axis, or put it in a table of its own")))
            else:
                held[axis] = raw[c]
                table.modes.append((c, axis, AXES[axis][:2]))

    if value:
        table.base = value[0]
        for c in value[1:]:
            table.dropped.append((raw[c], (
                f"is a second value column beside {raw[value[0]]}, so it was not read; keep one "
                "value column, or head the columns with mode names such as Light and Dark if "
                "they differ by mode")))
        place(other, raw[value[0]])
        return table
    if not other:
        return table if alias >= 0 else None
    if len(other) == 1:
        table.base = other[0]
        return table
    if len(other) > 2:
        base = next((c for c in other if is_base(raw[c])), other[0])
        table.base = base
        place([c for c in other if c != base], raw[base])
        return table
    known = axis_of([raw[c] for c in other], [raw[c] for c in other])
    if known is not None and known[1] != -1:
        axis = known[0]
        table.base, mode = other if known[1] == 0 else other[::-1]
        table.modes.append((mode, axis, AXES[axis][:2]))
        return table
    found = [_mode_word(raw[c]) for c in other]
    columns = _and([raw[c] for c in other])
    if all(found) and found[0] == found[1]:
        table.whole = True
        table.dropped.append(("", (f"a table with the columns {columns} was not read, since "
                                   f"both name the mode {found[0]}; head them with two mode "
                                   "names such as Light and Dark")))
        return table
    if not all(found):
        table.whole = True
        table.dropped.append(("", (f"a table with the columns {columns} was not read, since a "
                                   "mode is named with letters; head them with mode names such "
                                   "as Light and Dark")))
        return table
    table.base, mode = other
    table.modes.append((mode, f"{found[0]}-{found[1]}", (found[0], found[1])))
    return table


def _decode(text: str, entry: _Entry) -> Tuple[str, Any]:
    """(type, literal) or ("alias", target path) for one value; a mapped
    color or a dropped var() fallback is kept on the entry for the report."""
    brace = _BRACE.fullmatch(text)
    if brace:
        return "alias", _path(brace.group(1))
    alias = css_alias(text)
    if alias is not None:
        if alias[1]:
            entry.notes.append(Item(entry.where, entry.written, (
                f"its fallback {alias[1]} was left out; the reference holds the value")))
        return "alias", _path(alias[0])
    gamut: List[GamutMapped] = []
    read = read_value(text, gamut)
    entry.mapped += [Mapped.of(entry.where, entry.written, g) for g in gamut]
    return read


def import_markdown(files: Sequence[Tuple[str, str]], source: Source) -> Imported:
    """The tokens a list of (file name, text) rule files hold, in order."""
    found: Dict[str, _Entry] = {}
    axes: Dict[str, Tuple[str, str]] = {}
    notes: List[Item] = []
    not_read: List[Item] = []
    entries = 0
    # file -> [(line, name)] of lines whose value is a rule, not a value
    rules: Dict[str, List[Tuple[int, str]]] = {}
    # file -> [(line, label)] of Do and Avoid tables
    guidance: Dict[str, List[Tuple[int, str]]] = {}
    # files where a rule has the shape of a font list, so the note says how
    # a font list reads
    font_rules: set = set()
    # (path, where, name, what the second says, where the first was, what it set)
    again: List[Tuple[str, str, str, str, str, str]] = []
    # The unit the heading above names for the bare numbers below it.
    section = {"unit": ""}

    def add(name: str, where: str, values: Dict[str, str], labels: Dict[str, str],
            units: Optional[Dict[str, str]] = None, aliased: Tuple[str, ...] = ()) -> None:
        nonlocal entries
        written = _unquote(re.sub(r"^(\*{1,2}|_{1,2})(.+)\1$", r"\2", name.strip()))
        if written and _NAME.fullmatch(written):
            # A comma list of names is a font only with evidence; without it,
            # and for any value written in words, the line is a rule.
            ruled = fonty = False
            for ctx, v in values.items():
                text = _unquote(v)
                shaped = _font_shaped(text)
                if shaped and _font_evidence(text, f"{written} {labels.get(ctx, '')}"):
                    continue
                if shaped or _prose(text):
                    ruled = True
                    bare = text.rstrip(".")
                    fonty = fonty or (_font_shaped(bare) and not _prose(bare))
            if ruled:
                file_name, _, line = where.rpartition(":")
                rules.setdefault(file_name, []).append((int(line), written))
                if fonty:
                    font_rules.add(file_name)
                return
        entries += 1
        if not written:
            not_read.append(Item(where, "", f"has no name; write the token's name in the "
                                 f"{labels.get('name', 'first')} column"))
            return
        if not _NAME.fullmatch(written):
            not_read.append(Item(where, written, "is not a token name; write the name in "
                                 "backticks, for example `color.accent`"))
            return
        values = {ctx: _unquote(v) for ctx, v in values.items() if _unquote(v)}
        path = _path(written)
        # A bare number takes the unit its column or its heading names; a
        # size or a duration with no unit anywhere is not read.
        bare: Dict[str, str] = {}
        for ctx, v in list(values.items()):
            if not _BARE_NUMBER.fullmatch(v):
                continue
            unit = (units or {}).get(ctx) or section["unit"]
            need = _needs_unit(path)
            if unit:
                values[ctx] = v + unit
            elif need and float(v) == 0:
                values[ctx] = v + ("ms" if need == "duration" else "px")
            elif need:
                example = v + ("ms" if need == "duration" else "px")
                column = labels.get(ctx, "")
                if column:
                    fix = (f"write the unit in the cell, such as {example}, or in the column "
                           f"header, such as {column} ({example.lstrip('0123456789.+-')})")
                else:
                    heading = "## Motion (ms)" if need == "duration" else "## Sizes (px)"
                    fix = (f"write the unit, such as {example}, or name it in the heading above, "
                           f"such as {heading}")
                bare[ctx] = f"{v} has no unit, and {path} is a {need}; {fix}"
        first = found.get(path)
        if first is not None:
            for ctx in dict.fromkeys(["", *first.values, *values]):
                was, now = first.values.get(ctx, ""), values.get(ctx, "")
                if was == now:
                    continue
                label = f" {labels.get(ctx) or first.labels.get(ctx)}" if ctx else ""
                said = f"another{label} value ({now})" if now else f"no{label} value"
                kept = f"to {was}" if was else f"with no{label} value"
                again.append((path, where, written, said, first.where, kept))
                return
            return
        if "" not in values:
            column = labels.get("")
            not_read.append(Item(where, written, f"has no value in the {column} column; write "
                                 "one there" if column else "has no value; write one or remove "
                                 "the entry"))
            return
        found[path] = _Entry(where, written, values, labels, bare=bare, aliased=aliased)

    def read_table(table: _Table, raw: List[str], rows: List[Tuple[int, List[str]]],
                   file_name: str, where: str) -> None:
        """Read the rows of one table, as `table` says."""
        nonlocal entries
        not_read.extend(Item(where, column, why) for column, why in table.dropped)
        if table.whole:
            entries += sum(1 for _, cells in rows if table.name < len(cells)
                           and cells[table.name].strip())
            return
        if table.palette == "down":
            families = [c for c in range(1, len(raw)) if not _prose_header(raw[c].lower())]
            for c in families:
                if not _slug(_header_unit(raw[c])[0]):
                    not_read.append(Item(where, raw[c], (
                        f"a palette column (column {c + 1}) has no family name, so it was not "
                        "read; head it with the family, such as Blue")))
            for r, cells in rows:
                step = _unquote(cells[0]) if cells else ""
                for c in families:
                    family = _slug(_header_unit(raw[c])[0])
                    if family and c < len(cells) and cells[c].strip():
                        add(f"{family}.{step}", f"{file_name}:{r}", {"": cells[c]},
                            {"": raw[c], "name": raw[0]}, {"": table.units.get(c, "")})
            return
        if table.palette == "across":
            for r, cells in rows:
                family = _slug(cells[0]) if cells else ""
                if not family:
                    entries += 1
                    not_read.append(Item(f"{file_name}:{r}", "", (
                        f"a palette row with no family name; write the family in the "
                        f"{raw[0] or 'first'} column, such as Blue")))
                    continue
                for c in range(1, min(len(raw), len(cells))):
                    if cells[c].strip():
                        add(f"{family}.{raw[c]}", f"{file_name}:{r}", {"": cells[c]},
                            {"": raw[c], "name": raw[0]})
            return
        contexts = [(c, f"{axis}:{values[1]}") for c, axis, values in table.modes]
        for _, axis, values in table.modes:
            axes.setdefault(axis, values)
        head = raw[table.base] if table.base >= 0 else raw[table.alias]
        if contexts:
            if len(contexts) == 1:
                read = f"{head} was read as the base and {raw[contexts[0][0]]} as {contexts[0][1]}"
            else:
                read = f"{head} was read as the base, " + _and(
                    [f"{raw[c]} as {ctx}" for c, ctx in contexts])
            notes.append(Item(where, "", (
                f"a table with {_and([head] + [raw[c] for c, _ in contexts])} columns; {read}")))
        columns = [table.name] + [c for c in (table.base, table.alias) if c >= 0] \
            + [c for c, _ in contexts]
        for r, cells in rows:
            at = f"{file_name}:{r}"
            if len(cells) <= max(columns):
                entries += 1
                name = _unquote(cells[table.name]) if table.name < len(cells) else ""
                count = f"{len(cells)} cell{'s' if len(cells) != 1 else ''}"
                not_read.append(Item(at, name, f"has {count} where the header has "
                                     f"{len(raw)}; give the row one cell per column"))
                continue
            base = cells[table.base] if table.base >= 0 else ""
            alias = cells[table.alias] if table.alias >= 0 else ""
            if alias.strip() and (_refish(alias) or not base.strip()):
                values = {"": _as_reference(alias) if _refish(alias) else alias}
                labels = {"": raw[table.alias], "name": raw[table.name]}
                units = {"": table.units.get(table.alias, "")}
                aliased: Tuple[str, ...] = ("",)
            else:
                values = {"": base}
                labels = {"": raw[table.base] if table.base >= 0 else raw[table.alias],
                          "name": raw[table.name]}
                units = {"": table.units.get(table.base, "")}
                aliased = ()
            for c, ctx in contexts:
                values[ctx], labels[ctx] = cells[c], raw[c]
                units[ctx] = table.units.get(c, "")
            add(cells[table.name], at, values, labels, units, aliased)

    for file_name, text in files:
        lines = text.splitlines()
        i, fence, in_list, in_code, closed = 0, "", False, False, -1
        section["unit"] = ""
        while i < len(lines):
            line = lines[i]
            where = f"{file_name}:{i + 1}"
            opened = _FENCE.match(line)
            if not fence and line.strip():
                # An indented code block: four spaces in, after a blank line,
                # a heading, a thematic break or a closing fence (each ends
                # its block there), outside a list.
                indent = len(line.expandtabs(4)) - len(line.expandtabs(4).lstrip())
                if indent >= 4 and not in_list and (in_code or i == 0
                                                    or not lines[i - 1].strip()
                                                    or _BLOCK_END.match(lines[i - 1])
                                                    or closed == i - 1):
                    in_code = True
                    i += 1
                    continue
                in_code = False
                if _BULLET.match(line):
                    in_list = True
                elif indent == 0:
                    in_list = False
            if fence:
                if opened and opened.group(1)[0] == fence[0] and len(opened.group(1)) >= \
                        len(fence) and not opened.group(2):
                    fence, closed = "", i
                i += 1
                continue
            if opened:
                fence = opened.group(1)
                if opened.group(2).lower() == "css":
                    notes.append(Item(where, "", "a css code block was not read; import the "
                                      "stylesheet itself with --from and a .css file"))
                i += 1
                continue
            heading = _HEADING.fullmatch(line)
            if heading:
                section["unit"] = _heading_unit(heading.group(1))
                i += 1
                continue
            listed = _LIST.match(line)
            if listed:
                add(listed.group(1), where, {"": listed.group(2)}, {"": ""})
                i += 1
                continue
            if "|" in line and i + 1 < len(lines) and _DELIMITER.fullmatch(lines[i + 1]) \
                    and len(_split(line)) == len(_split(lines[i + 1])):
                raw = [_header(c) for c in _split(line)]
                end = i + 2
                while end < len(lines) and "|" in lines[end] and lines[end].strip() \
                        and not _FENCE.match(lines[end]):
                    end += 1
                rows = [(r + 1, _split(lines[r])) for r in range(i + 2, end)]
                rows = [(r, cells) for r, cells in rows if any(cells)]
                table = _table(raw, [cells for _, cells in rows])
                if table is not None and table.guidance:
                    guidance.setdefault(file_name, []).append((i + 1, table.guidance))
                    table = None
                if table is not None and table.base >= 0 and not table.modes \
                        and table.alias < 0 and not table.palette and not table.whole \
                        and _header_unit(raw[table.base])[0].lower() not in VALUE_HEADERS \
                        and not _TYPE_CONTEXT.search(raw[table.base]) \
                        and not any(_valueish(c[table.base]) for _, c in rows
                                    if len(c) > table.base):
                    notes.append(Item(where, "", (
                        f"a table whose {raw[table.base]} column holds no values was not read as "
                        "tokens; head the value column Value, Hex or Size to read it")))
                    table = None
                if table is not None:
                    read_table(table, raw, rows, file_name, where)
                i, in_list = end, False
                continue
            i += 1

    for file_name in dict.fromkeys([*rules, *guidance]):
        found_rules = rules.get(file_name, [])
        tables = guidance.get(file_name, [])
        parts = []
        if found_rules:
            listed = ", ".join(f"`{name}` (line {line})" for line, name in found_rules)
            count = len(found_rules)
            head = (f"{count} lines hold rules, not values, and were kept as rules"
                    if count > 1 else "1 line holds a rule, not a value, and was kept as a rule")
            parts.append(
                f"{head}: {listed}; to make {'one' if count > 1 else 'it'} a token, write only "
                "its value after the colon or in the cell, and put the rule on its own line"
                + ("; a font list reads when its font names are quoted or it ends in a generic "
                   "family such as sans-serif" if file_name in font_rules else ""))
        if tables:
            one = len(tables) == 1
            parts.append(_and([f"the {label} table (line {line})" for line, label in tables])
                         + (" holds guidance, not values, and was kept as a rule" if one else
                            " hold guidance, not values, and were kept as rules"))
        first = min(line for line, _ in found_rules + tables)
        notes.append(Item(f"{file_name}:{first}", "", "; ".join(parts)))

    # Decode each value; a reference is kept as an alias to its target.
    defined = set(found)
    # path -> why its first value was not read
    failed: Dict[str, str] = {}
    for path in list(found):
        entry = found[path]
        try:
            for ctx, text in entry.values.items():
                try:
                    if ctx in entry.bare:
                        raise NotRead(entry.bare[ctx])
                    entry.decoded[ctx] = _decode(text, entry)
                except NotRead as exc:
                    column = entry.labels.get(ctx, "")
                    if ctx in entry.aliased and _NAME.fullmatch(text):
                        raise NotRead(f"in the {column} column, {text} is not written as a "
                                      f"reference; write it in braces, {{{text}}}, or in "
                                      "backticks") from None
                    raise NotRead(f"in the {column} column, {exc}" if ctx else str(exc)) \
                        from None
        except NotRead as exc:
            not_read.append(Item(entry.where, entry.written, str(exc)))
            failed[path] = str(exc)
            del found[path]

    def drop(path: str, why: str) -> None:
        entry = found.pop(path)
        not_read.append(Item(entry.where, entry.written, why))
        failed[path] = why

    def targets(path: str) -> List[str]:
        return [v for k, v in found[path].decoded.values() if k == "alias"]

    def kind_of(path: str, seen: Tuple[str, ...] = ()) -> str:
        """Literals decide a type; an alias takes its target's."""
        literal = next((k for k, _ in found[path].decoded.values() if k != "alias"), "")
        if literal or path in seen:
            return literal
        return next((got for v in targets(path) if v in found
                     for got in [kind_of(v, seen + (path,))] if got), "")

    def loops(path: str) -> bool:
        """True when a chain of references from `path` comes back to it."""
        stack, seen = list(targets(path)), set()
        while stack:
            node = stack.pop()
            if node == path:
                return True
            if node in found and node not in seen:
                seen.add(node)
                stack += targets(node)
        return False

    while True:
        # A reference to a name that was not read, or that no file defines.
        changed = True
        while changed:
            changed = False
            for path in list(found):
                gone = next((v for v in targets(path) if v not in found), None)
                if gone is not None:
                    drop(path, f"references {gone}, which was not read; fix {gone} and import "
                               "again" if gone in defined else
                         f"references {gone}, which no file defines; define it or write the "
                         "value")
                    changed = True
        typeless = [p for p in found if not kind_of(p) and loops(p)]
        for path in typeless:
            drop(path, _LOOP)
        # A name whose columns hold values of two types.
        mixed = {}
        for path, entry in found.items():
            kind = kind_of(path)
            literals = [(ctx, k) for ctx, (k, _) in entry.decoded.items() if k != "alias"]
            odd = next(((ctx, k) for ctx, k in literals if k != kind), None)
            if odd:
                first = next(ctx for ctx, k in literals if k == kind)
                mixed[path] = (f"holds a {kind} in the {entry.labels[first]} column and a "
                               f"{odd[1]} in the {entry.labels[odd[0]]} column; give it one type")
        for path, why in mixed.items():
            drop(path, why)
        if not typeless and not mixed:
            break

    # A name set again: the first value wins; when it was not read, neither is used.
    for path, where, written, said, first_where, kept in again:
        fate = (f"which was not read ({failed[path]}); the first value wins, so no value is "
                f"used for {written}; fix that line or remove it, and keep one" if path in failed
                else "which was kept, so keep one")
        not_read.append(Item(where, written, f"is set again with {said}; {first_where} set it "
                             f"first {kept}, {fate}"))

    ts = TokenSet(axes)
    kept_notes: List[Item] = list(notes)
    renamed: List[Item] = []
    mapped: List[Mapped] = []
    for path, entry in found.items():
        kind = kind_of(path)
        written = {ctx: ("{" + v + "}" if k == "alias" else v)
                   for ctx, (k, v) in entry.decoded.items()}
        modes = {ctx: v for ctx, v in written.items() if ctx}
        aliased = any(k == "alias" for k, _ in entry.decoded.values())
        ts.add(Token(path, kind, written[""], modes=modes,
                     layer="semantic" if aliased or modes else "primitive"))
        kept_notes += entry.notes
        if "/" in entry.written:
            renamed.append(Item(entry.where, entry.written, f"read as {path}, since a slash in a "
                                "name reads as a dot"))
        mapped += entry.mapped

    order = {f: n for n, (f, _) in enumerate(files)}

    def key(item: Any) -> Tuple[int, int]:
        file_name, _, line = item.where.rpartition(":")
        return order.get(file_name, 0), int(line)

    report = ImportReport.of(source, ts, entries=entries)
    report.notes = sorted(kept_notes, key=key)
    report.not_read = sorted(not_read, key=key)
    report.mapped = sorted(mapped, key=key)
    report.renamed = sorted(renamed, key=key)
    return Imported(ts, report)


def read_markdown(path: Any, label: str = "--from") -> Imported:
    """Read one rule file, or every .md file in a folder, sorted by name.
    The source digest covers every file read, in that order."""
    p = Path(path).expanduser()
    paths = sorted(f for f in p.glob("*.md") if f.is_file()) if p.is_dir() else [p]
    if not paths:
        raise InputError(f"{label} {p} holds no .md file; pass a markdown rule file or the "
                         "folder that holds them")
    digest = hashlib.sha256()
    files: List[Tuple[str, str]] = []
    size = 0
    for f in paths:
        try:
            data = f.read_bytes()
        except OSError as exc:
            raise InputError(f"{label} {f} cannot be read ({exc.strerror or exc}); pass a "
                             "markdown rule file or the folder that holds them") from None
        try:
            text = _brief_text(data)
        except UnicodeDecodeError:
            raise InputError(f"{label} {f} is not UTF-8 text; save it as UTF-8 and pass it "
                             "again") from None
        digest.update(f.name.encode("utf-8") + b"\0" + data)
        size += len(data)
        files.append((f.name, text))
    return import_markdown(files, Source(str(p), "markdown", digest.hexdigest(), size))
