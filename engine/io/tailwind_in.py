"""Import a Tailwind theme in its own names, without running JavaScript.

Tailwind 4 keeps its theme in CSS: the @theme block is read as the root,
through the CSS importer, and a `--color-*: initial` reset is noted, since
it only clears Tailwind's own defaults. The dark scheme is read where the
stylesheet keeps it: `.dark` or another selector that `@custom-variant dark`
names, `@variant dark` nested in a rule, or prefers-color-scheme, which is
where Tailwind's dark: variant switches when no custom variant is declared.

Tailwind 3 keeps its theme in a JavaScript config, which this engine never
runs: the person exports the resolved theme as JSON (EXPORT_COMMAND) and
the importer reads that. Each key path becomes a token path
(colors.moss.700); a key holding characters a path cannot (a dot, a
slash) is renamed with '_' and the report says so. A font size paired with
a line height keeps the size and notes the line height. Dark values are
not in a Tailwind 3 theme (they are dark: utilities in markup), so a config
that sets darkMode is noted, not read.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, List, Tuple

from engine.foundations.errors import InputError
from engine.foundations.tokens import Token, TokenSet
from engine.io.css_in import import_css
from engine.io.report import Imported, ImportReport, Item, Mapped, Source, read_source
from engine.io.values_in import GamutMapped, NotRead, read_value

# The command that exports a Tailwind 3 config's resolved theme as JSON.
EXPORT_COMMAND = ("node -e \"const r=require('tailwindcss/resolveConfig');"
                  "console.log(JSON.stringify(r(require('./tailwind.config.js')).theme))\" "
                  "> tailwind-theme.json")
_JS = (".js", ".cjs", ".mjs", ".ts", ".cts", ".mts")
_SEGMENT = re.compile(r"[^A-Za-z0-9_-]")
# Keys of a whole Tailwind 3 config that are not theme values.
_CONFIG_KEYS = ("content", "plugins", "presets", "darkMode", "prefix", "important",
                "corePlugins", "safelist", "blocklist", "separator", "future", "experimental")
# The fields a font size pairs with its size, and their names in the report.
_SIZE_FIELDS = (("lineHeight", "line height"), ("letterSpacing", "letter spacing"),
                ("fontWeight", "font weight"))


def import_tailwind_css(text: str, source: Source) -> Imported:
    """A Tailwind 4 stylesheet: the CSS importer reads @theme as the root."""
    return import_css(text, source)


def import_tailwind_json(text: str, source: Source) -> Imported:
    """A Tailwind 3 theme exported as resolved JSON (or a config object
    whose theme is resolved)."""
    name = Path(source.path).name
    try:
        doc = json.loads(text)
    except ValueError as exc:
        raise InputError(f"{source.path} is not valid JSON ({exc}); export the theme again with "
                         f"{EXPORT_COMMAND}") from None
    if not isinstance(doc, dict):
        raise InputError(f"{source.path} does not hold a JSON object; export the theme with "
                         f"{EXPORT_COMMAND}")
    theme = doc["theme"] if isinstance(doc.get("theme"), dict) else {
        k: v for k, v in doc.items() if k not in _CONFIG_KEYS}
    if "extend" in theme:
        raise InputError(f"{source.path} holds theme.extend, which Tailwind has not merged yet; "
                         f"export the resolved theme instead: {EXPORT_COMMAND}")
    ts = TokenSet({})
    entries = 0
    renamed: List[Item] = []
    notes: List[Item] = []
    not_read: List[Item] = []
    mapped: List[Mapped] = []
    if "darkMode" in doc:
        notes.append(Item(f"{name} darkMode", "darkMode", (
            f"is {json.dumps(doc['darkMode'])}; Tailwind 3 writes dark values as dark: "
            "utilities in markup, not in the theme, so this file holds no dark scheme; if a "
            "stylesheet sets the dark values as custom properties, import that too")))

    def walk(node: Any, keys: List[str]) -> None:
        nonlocal entries
        for key, value in node.items():
            src = keys + [str(key)]
            source_name = ".".join(src)
            where = f"{name} {source_name}"
            if src[0] == "keyframes" and len(src) == 2:
                entries += 1
                not_read.append(Item(where, source_name, "is an animation's keyframes, not a "
                                     "value; keep it in the stylesheet that animates with it"))
                continue
            if isinstance(value, dict):
                walk(value, src)
                continue
            entries += 1
            dst = [_SEGMENT.sub("_", k) for k in src]
            path = ".".join(dst)
            text_value, extra = _tailwind_value(src[0], value)
            try:
                if isinstance(text_value, list):
                    kind, literal = "fontFamily", text_value
                else:
                    gamut: List[GamutMapped] = []
                    kind, literal = read_value(text_value, gamut)
                    mapped.extend(Mapped.of(where, source_name, g) for g in gamut)
            except NotRead as exc:
                not_read.append(Item(where, source_name, str(exc)))
                continue
            if ts.has(path):
                not_read.append(Item(where, source_name, f"is read as {path}, which an earlier "
                                     "key already names; rename one of the two keys"))
                continue
            if dst != src:
                renamed.append(Item(where, source_name, f"read as {path}, since a path segment "
                                    "holds only letters, digits, '_' and '-'"))
            if extra:
                notes.append(Item(where, source_name, extra))
            ts.add(Token(path, kind, literal))

    walk(theme, [])
    report = ImportReport.of(source, ts, entries=entries)
    report.renamed, report.notes, report.not_read = renamed, notes, not_read
    report.mapped = mapped
    return Imported(ts, report)


def _tailwind_value(key: str, value: Any) -> Tuple[Any, str]:
    """(the value to read, a note or ""). Tailwind writes a font size with
    what it pairs as [size, {lineHeight, letterSpacing, fontWeight}] or
    [size, lineHeight], and a font family as a list of names, or as
    [names, {fontFeatureSettings}]; the note names what was left out. Any
    other list (a drop shadow's layers) is read as one comma list."""
    if not isinstance(value, list):
        return str(value), ""
    if key == "fontSize" and len(value) == 2 and isinstance(value[1], (dict, str)):
        pairs = value[1] if isinstance(value[1], dict) else {"lineHeight": value[1]}
        left = [f"{label} {pairs[field]}" for field, label in _SIZE_FIELDS if field in pairs]
        if not left:
            return str(value[0]), ""
        if len(left) == 1 and "lineHeight" in pairs:
            return str(value[0]), (f"its {left[0]} was left out; the engine keeps line heights "
                                   "as their own tokens, so add one if you need it")
        listed = ", ".join(left[:-1]) + f" and {left[-1]} were" if len(left) > 1 \
            else f"{left[0]} was"
        return str(value[0]), (f"its {listed} left out; the engine keeps these as their own "
                               "tokens, so add them if you need them")
    if key == "fontFamily":
        names, note = value, ""
        if len(value) == 2 and isinstance(value[0], list) and isinstance(value[1], dict):
            names = value[0]
            note = ", ".join(f"{k} {v}" for k, v in value[1].items())
            note = f"its {note} was left out; a font family token holds only the names"
        return [str(n).strip().strip("\"'") for n in names], note
    return ", ".join(str(v) for v in value), ""


def read_tailwind(path: Any, label: str = "--from") -> Imported:
    """Read a Tailwind 4 stylesheet (.css) or a Tailwind 3 theme exported as
    JSON (.json). A JavaScript config is refused: it would have to run."""
    p = Path(path).expanduser()
    suffix = p.suffix.lower()
    if suffix in _JS:
        raise InputError(f"{label} {p} is a JavaScript config, and uxskill never runs "
                         f"JavaScript; export the resolved theme as JSON and pass that file: "
                         f"{EXPORT_COMMAND}")
    if suffix == ".css":
        source, text = read_source(p, "tailwind", label)
        return import_tailwind_css(text, source)
    if suffix == ".json":
        source, text = read_source(p, "tailwind-json", label)
        return import_tailwind_json(text, source)
    raise InputError(f"{label} {p.name} is not a Tailwind stylesheet (.css) or a theme exported "
                     f"as JSON (.json); pass one of those, for example {EXPORT_COMMAND}")
