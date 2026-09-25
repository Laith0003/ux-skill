"""Import a system that lives only in markdown rule files.

Read as tokens:
- a table with a name column (headed Token, Name, Variable or Role) and a
  value column (Value, Hex, Color, Size, Px, Rem or Ms). A second value
  column is left out with a note. A further column headed with the non-base
  value of a mode axis (Dark, Compact, High, Reduced, Rtl) is that mode;
- a table with a name column and two other columns that are not prose
  (Notes, Description, Usage and the like are prose): the two columns are
  two modes of one axis. Light and Dark read into the scheme axis with
  Light as the base, whichever comes first, and so do the other named axes
  (Comfortable and Compact are density); any other pair makes an axis
  named after both headers, the first the base (Brand and Partner give
  brand-partner). Each such table is noted;
- a list item whose name is in backticks: "- `space.2`: 8px" or "= 8px".

A name may be written plain, in bold or in backticks, with dots, dashes or
slashes (a slash reads as a dot, and the report lists it as renamed); a
value may be a literal, `{other.token}` or var(--other). Prose, tables
without a name column, list items without a backticked name and code
blocks are not tokens; a css code block is noted with the fix. A row
whose name is not a token name, a value with no single reading and a
reference to a name no file defines are listed under "Not read" with
their file and line. A name set twice keeps its first
value, and a second, different value is reported. An oklch() or oklab()
color outside sRGB is mapped into it and reported, never refused.
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
from engine.io.mode_words import axis_of
from engine.io.report import Imported, ImportReport, Item, Mapped, Source
from engine.io.values_in import (COLOR_KEYWORDS, CSS_KEYWORDS, EASING_KEYWORDS, GamutMapped,
                                 NotRead, css_alias, read_value, split_top)

NAME_HEADERS = ("token", "name", "variable", "role", "token name", "css variable")
VALUE_HEADERS = ("value", "hex", "color", "size", "px", "rem", "ms")
PROSE_HEADERS = ("notes", "note", "description", "usage", "use", "purpose", "meaning",
                 "example", "when", "why", "do", "don't", "dont")

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
_LOOP = "references only itself through a loop of references; give one of them a value"


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


def _known_axis(words: Sequence[str], headers: Sequence[str]) -> Optional[Tuple[str, int]]:
    """(axis, index of its base) when the mode words name an engine axis
    (both values, or the non-base one alone, index -1), by the importers'
    shared matcher; the headers as written may hold the axis's own name,
    which contrast and motion need. None otherwise."""
    return axis_of(list(words), headers) if all(words) else None


def _path(name: str) -> str:
    name = name.removeprefix("--")
    return name.replace("/", ".")


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


@dataclass
class _Table:
    """How a table is read: its name column, its base column and, for a
    mode, its column, axis and values; or a note when it is not read."""
    name: int
    base: int = -1
    mode: int = -1
    axis: str = ""
    values: Tuple[str, str] = ("", "")
    notes: List[str] = field(default_factory=list)


def _table(raw: List[str]) -> Optional[_Table]:
    """How a table with these headers is read; None when it holds no
    tokens (no name column, or only prose beside it)."""
    headers = [h.lower() for h in raw]
    name = next((headers.index(h) for h in _NAME_PREFERENCE if h in headers), None)
    if name is None:
        return None
    value = [c for c, h in enumerate(headers) if c != name and h in VALUE_HEADERS]
    other = [c for c, h in enumerate(headers)
             if c != name and h and h not in VALUE_HEADERS and h not in NAME_HEADERS
             and not _prose_header(h)]
    table = _Table(name)
    if value:
        table.base = value[0]
        if len(value) > 1:
            left = [raw[c] for c in value[1:]]
            table.notes.append(
                f"a table with the value columns {_and([raw[c] for c in value])}; "
                f"{raw[value[0]]} was read and {_and(left)} {'were' if len(left) > 1 else 'was'} "
                "left out; keep one value column, or head the columns with mode names such as "
                "Light and Dark if they differ by mode")
        modes = [(c, hit[0]) for c in other
                 for hit in [_known_axis([_mode_word(raw[c])], [raw[c]])]
                 if hit is not None and hit[1] == -1]
        if len(modes) == 1:
            table.mode, table.axis = modes[0]
            table.values = AXES[table.axis][:2]
        left = [raw[c] for c in other if c != table.mode]
        if left:
            table.notes.append(
                f"a table with the columns {_and(raw)}: {_and(left)} "
                f"{'name' if len(left) > 1 else 'names'} no mode and "
                f"{'were' if len(left) > 1 else 'was'} left out; head a column with a mode name "
                "such as Dark to read it as that mode, or put it in its own table")
        return table
    if len(other) == 1:
        table.base = other[0]
        return table
    if not other:
        return None
    if len(other) > 2:
        table.notes.append(f"a table with the columns {_and([raw[c] for c in other])} was not "
                           "read; the engine reads one value column, or two columns for a base "
                           "and one mode, so split it into tables of that shape")
        return table
    words = [_mode_word(raw[c]) for c in other]
    if all(words) and words[0] == words[1]:
        table.notes.append(f"a table with the columns {_and([raw[c] for c in other])} was not "
                           f"read, since both name the mode {words[0]}; head them with two mode "
                           "names such as Light and Dark")
        return table
    if not all(words):
        table.notes.append(f"a table with the columns {_and([raw[c] for c in other])} was not "
                           "read, since a mode is named with letters; head them with mode names "
                           "such as Light and Dark")
        return table
    known = _known_axis(words, [raw[c] for c in other])
    if known is not None and known[1] != -1:
        axis = known[0]
        table.base, table.mode = other if known[1] == 0 else other[::-1]
        table.axis, table.values = axis, AXES[axis][:2]
    else:
        table.base, table.mode = other
        table.axis, table.values = f"{words[0]}-{words[1]}", (words[0], words[1])
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
    # files where a rule has the shape of a font list, so the note says how
    # a font list reads
    font_rules: set = set()
    # (path, where, name, what the second says, where the first was, what it set)
    again: List[Tuple[str, str, str, str, str, str]] = []

    def add(name: str, where: str, values: Dict[str, str], labels: Dict[str, str]) -> None:
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
        found[path] = _Entry(where, written, values, labels)

    for file_name, text in files:
        lines = text.splitlines()
        i, fence, in_list, in_code = 0, "", False, False
        while i < len(lines):
            line = lines[i]
            where = f"{file_name}:{i + 1}"
            opened = _FENCE.match(line)
            if not fence and line.strip():
                # An indented code block: four spaces in, after a blank line,
                # outside a list.
                indent = len(line.expandtabs(4)) - len(line.expandtabs(4).lstrip())
                if indent >= 4 and not in_list and (in_code or i == 0
                                                    or not lines[i - 1].strip()):
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
                    fence = ""
                i += 1
                continue
            if opened:
                fence = opened.group(1)
                if opened.group(2).lower() == "css":
                    notes.append(Item(where, "", "a css code block was not read; import the "
                                      "stylesheet itself with --from and a .css file"))
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
                table = _table(raw)
                if table is not None:
                    notes += [Item(where, "", n) for n in table.notes]
                if table is not None and table.base >= 0 and not table.axis \
                        and raw[table.base].lower() not in VALUE_HEADERS \
                        and not _TYPE_CONTEXT.search(raw[table.base]) \
                        and not any(_valueish(c[table.base]) for c in
                                    (_split(x) for x in lines[i + 2:end]) if len(c) > table.base):
                    notes.append(Item(where, "", (
                        f"a table whose {raw[table.base]} column holds no values was not read as "
                        "tokens; head the value column Value, Hex or Size to read it")))
                    table = None
                if table is not None and table.base >= 0:
                    ctx = f"{table.axis}:{table.values[1]}" if table.axis else ""
                    if ctx:
                        axes.setdefault(table.axis, table.values)
                        notes.append(Item(where, "", (
                            f"a table with {raw[table.base]} and {raw[table.mode]} columns; "
                            f"{raw[table.base]} was read as the base and {raw[table.mode]} as "
                            f"{ctx}")))
                    columns = [table.name, table.base] + ([table.mode] if ctx else [])
                    for r in range(i + 2, end):
                        cells = _split(lines[r])
                        if not any(cells):
                            continue
                        at = f"{file_name}:{r + 1}"
                        if len(cells) <= max(columns):
                            entries += 1
                            name = _unquote(cells[table.name]) if table.name < len(cells) else ""
                            count = f"{len(cells)} cell{'s' if len(cells) != 1 else ''}"
                            not_read.append(Item(at, name, f"has {count} where the header has "
                                                 f"{len(raw)}; give the row one cell per column"))
                            continue
                        values = {"": cells[table.base]}
                        labels = {"": raw[table.base], "name": raw[table.name]}
                        if ctx:
                            values[ctx], labels[ctx] = cells[table.mode], raw[table.mode]
                        add(cells[table.name], at, values, labels)
                i, in_list = end, False
                continue
            i += 1

    for file_name, found_rules in rules.items():
        listed = ", ".join(f"`{name}` (line {line})" for line, name in found_rules)
        count = len(found_rules)
        head = (f"{count} lines hold rules, not values, and were kept as rules"
                if count > 1 else "1 line holds a rule, not a value, and was kept as a rule")
        notes.append(Item(f"{file_name}:{found_rules[0][0]}", "", (
            f"{head}: {listed}; to make {'one' if count > 1 else 'it'} a token, write only its "
            "value after the colon or in the cell, and put the rule on its own line"
            + ("; a font list reads when its font names are quoted or it ends in a generic "
               "family such as sans-serif" if file_name in font_rules else ""))))

    # Decode each value; a reference is kept as an alias to its target.
    defined = set(found)
    # path -> why its first value was not read
    failed: Dict[str, str] = {}
    for path in list(found):
        entry = found[path]
        try:
            for ctx, text in entry.values.items():
                try:
                    entry.decoded[ctx] = _decode(text, entry)
                except NotRead as exc:
                    column = entry.labels.get(ctx, "")
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
