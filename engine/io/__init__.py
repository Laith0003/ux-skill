"""Systems in and out: importers that read an existing design system in
its own names (DTCG JSON, CSS custom properties, a Tailwind theme, markdown
rule files, a Figma variables export), each with a report of what it read,
the value reader they share, the naming adapter that checks an imported
system in the engine's roles while it keeps its own names, the scanner
that measures what a codebase actually uses, and the enhance report that
sets the two side by side. read_any reads a file in any of FORMATS.
"""
from pathlib import Path
from typing import Any

from engine.foundations.errors import InputError
from engine.io.adapter import (
    ROLE_TYPES, AxisMap, Mapping, RoleMap, dump_mapping, load_mapping, merge, parse_mapping,
    propose, their_names, view)
from engine.io.css_in import Rule, import_css, parse_css, read_css, write_css
from engine.io.dtcg_in import import_dtcg, read_dtcg
from engine.io.enhance import Drift, Enhanced, Lie, RawWithToken, drift, enhance
from engine.io.figma_in import REST_ENDPOINT, SIZE_SCOPES, import_figma, read_figma
from engine.io.graph import cycles, loop
from engine.io.markdown_in import import_markdown, read_markdown
from engine.io.mode_words import axis_of
from engine.io.report import (FORMATS, Imported, ImportReport, Item, Mapped, Source,
                              read_source)
from engine.io.scan import SKIP_DIRS, NotMeasured, Scan, UnknownClass, Usage, scan
from engine.io.tailwind_in import (
    EXPORT_COMMAND, import_tailwind_css, import_tailwind_json, read_tailwind)
from engine.io.values_in import (CSS_KEYWORDS, GamutMapped, NotRead, css_alias, read_value,
                                 split_top)

__all__ = [
    "CSS_KEYWORDS", "EXPORT_COMMAND", "FORMATS", "REST_ENDPOINT", "ROLE_TYPES", "SIZE_SCOPES",
    "SKIP_DIRS", "AxisMap", "Drift", "Enhanced", "GamutMapped", "ImportReport", "Imported",
    "Item", "Lie", "Mapped", "Mapping", "NotMeasured", "NotRead", "RawWithToken", "RoleMap",
    "Rule", "Scan", "Source", "UnknownClass", "Usage", "axis_of", "css_alias",
    "cycles", "drift", "dump_mapping", "enhance",
    "import_css", "import_dtcg", "import_figma", "import_markdown", "import_tailwind_css",
    "import_tailwind_json", "load_mapping", "loop", "merge",
    "parse_css", "parse_mapping", "propose", "read_css", "read_dtcg", "read_figma",
    "read_any", "read_markdown", "read_source", "read_tailwind", "read_value", "scan",
    "split_top", "write_css",
    "their_names", "view",
]


def read_any(path: Any, fmt: str, label: str = "--from", **options: Any) -> Imported:
    """Read and import `path` with the reader for `fmt`, one of FORMATS.
    `options` go to that reader (pair for dtcg, second_modes for figma).
    Raises InputError naming `label` and the fix for a format that is not
    one of FORMATS, or a Tailwind file whose extension is not the one the
    format reads."""
    if fmt == "dtcg":
        return read_dtcg(path, label, **options)
    if fmt == "css":
        return read_css(path, label, **options)
    if fmt in ("tailwind", "tailwind-json"):
        want = ".css" if fmt == "tailwind" else ".json"
        p = Path(path).expanduser()
        if p.suffix.lower() in (".css", ".json") and p.suffix.lower() != want:
            raise InputError(f"{label} {p.name} is not a {want} file, which {fmt} reads; pass "
                             f"the format that matches it ("
                             f"{'tailwind-json' if fmt == 'tailwind' else 'tailwind'})")
        return read_tailwind(path, label, **options)
    if fmt == "markdown":
        return read_markdown(path, label, **options)
    if fmt == "figma":
        return read_figma(path, label, **options)
    names = ", ".join(FORMATS[:-1]) + " and " + FORMATS[-1]
    raise InputError(f"{label} format {fmt!r} is not one of {names}; pass one of those")
