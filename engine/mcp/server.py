"""MCP stdio server exposing the ux-skill engine.

Architecture
------------
The 14 tools are implemented as pure ``dict -> dict`` handler functions
that have NO dependency on the ``mcp`` package. The MCP transport
(``mcp.server.stdio``) is optional and only imported inside ``run_server()``.

This split keeps three things clean:

1. **Tests run without the mcp library installed.** They call the handlers
   directly and assert on the returned JSON-serialisable dicts.
2. **Import remains safe.** ``from engine.mcp import run_server`` works
   even when ``pip install mcp`` has not been done — the error only fires
   when you actually attempt to start the server.
3. **One source of truth for the tool catalogue.** ``TOOLS`` maps each
   tool name to its handler, Pydantic input model, and description. The
   ``run_server`` wrapper iterates this dict to register them all with
   the MCP framework.

Logging always goes to stderr because stdout is reserved for the MCP
JSON-RPC protocol stream when running under stdio transport.
"""
from __future__ import annotations

import json
import logging
import sys
from dataclasses import is_dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel, Field

from engine import __version__
from engine.data_loader import load, load_brands, stats
from engine.foundations.audience import FIELDS_HELP as BRIEF_FIELDS_HELP
from engine.linter import lint
from engine.persist import save_master, load_master
from engine.recommender import Brief, recommend


# ---------------------------------------------------------------------------
# Logging — stderr only (stdout is the MCP transport channel)
# ---------------------------------------------------------------------------

logger = logging.getLogger("engine.mcp")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter(
        "%(asctime)s ux-mcp %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(_handler)
logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Optional transport — graceful import
# ---------------------------------------------------------------------------

try:  # pragma: no cover - depends on env
    # The canonical low-level public path per the official Anthropic SDK docs:
    # https://github.com/modelcontextprotocol/python-sdk
    from mcp.server.lowlevel import Server, NotificationOptions  # type: ignore
    from mcp.server.stdio import stdio_server  # type: ignore
    from mcp.server.models import InitializationOptions  # type: ignore
    import mcp.types as mcp_types  # type: ignore

    MCP_AVAILABLE = True
except Exception as _import_error:  # pragma: no cover - depends on env
    Server = None  # type: ignore
    NotificationOptions = None  # type: ignore
    stdio_server = None  # type: ignore
    InitializationOptions = None  # type: ignore
    mcp_types = None  # type: ignore
    MCP_AVAILABLE = False
    _MCP_IMPORT_ERROR: Optional[BaseException] = _import_error
else:  # pragma: no cover - depends on env
    _MCP_IMPORT_ERROR = None


# ---------------------------------------------------------------------------
# Pydantic input schemas
# ---------------------------------------------------------------------------


class BriefModel(BaseModel):
    """Mirror of :class:`engine.recommender.Brief` for MCP input validation."""

    project_type: str = ""
    industry: str = ""
    audience: List[str] = Field(default_factory=list)
    tone: List[str] = Field(default_factory=list)
    must_have: List[str] = Field(default_factory=list)
    forbidden: List[str] = Field(default_factory=list)
    stack: str = ""
    region: str = ""


class UxRecommendInput(BaseModel):
    brief: BriefModel = Field(
        default_factory=BriefModel,
        description="Project brief — industry, audience, tone, must-haves, forbidden moves.",
    )
    project_root: Optional[str] = Field(
        default=None,
        description="The project folder. When it holds an existing design system, its tokens "
                    "win: palette and type_pair come back as suggestions, with an "
                    "existing_system block.",
    )


class UxSystemDetectInput(BaseModel):
    root: str = Field(default=".", description="The project folder to look in.")


class UxLintInput(BaseModel):
    paths: List[str] = Field(
        default_factory=lambda: ["."],
        description="Files or directories to scan. Defaults to the current directory.",
    )
    threshold: str = Field(
        default="high",
        description="Lowest severity that gates exit code: low | medium | high | critical.",
    )


class UxStylesInput(BaseModel):
    pass


class UxPalettesInput(BaseModel):
    mode: Optional[str] = Field(
        default=None,
        description="Filter by palette mode (e.g. 'light', 'dark'). Omit for all entries.",
    )


class UxTypePairsInput(BaseModel):
    pass


class UxComponentsInput(BaseModel):
    category: Optional[str] = Field(
        default=None,
        description="Filter by component category (e.g. 'navigation', 'forms'). Omit for all.",
    )


class UxIndustriesInput(BaseModel):
    category: Optional[str] = Field(
        default=None,
        description="Filter by industry category (e.g. 'fintech', 'b2b-saas'). Omit for all.",
    )


class UxMotionPresetsInput(BaseModel):
    category: Optional[str] = Field(
        default=None,
        description="Filter by motion preset category. Omit for all entries.",
    )


class UxAntiPatternsInput(BaseModel):
    severity: Optional[str] = Field(
        default=None,
        description="Filter by severity: low | medium | high | critical. Omit for all.",
    )


class UxBrandsInput(BaseModel):
    category: Optional[str] = Field(
        default=None,
        description="Filter by brand category (e.g. 'fintech', 'consumer'). Omit for all.",
    )


class UxLandingPatternsInput(BaseModel):
    category: Optional[str] = Field(
        default=None,
        description="Filter by landing pattern category. Omit for all entries.",
    )


class UxPersistSaveInput(BaseModel):
    project_root: str = Field(
        description="Absolute path to the project root where .ux/design-system/ should be written.",
    )
    recommendation: Dict[str, Any] = Field(
        description="The recommendation dict (typically from ux_recommend).",
    )
    brief: Dict[str, Any] = Field(
        default_factory=dict,
        description="The brief dict — included in the persisted MASTER.md.",
    )


class UxPersistLoadInput(BaseModel):
    project_root: str = Field(
        description="Absolute path to the project root holding .ux/design-system/MASTER.md.",
    )


class UxStatsInput(BaseModel):
    pass


class UxImageExtractInput(BaseModel):
    project_root: Optional[str] = Field(
        default=None,
        description="The project folder. When it holds an existing design system, the "
                    "recommendation's palette and type pair are suggestions its tokens override.")
    path: str = Field(
        description="Absolute or relative path to a design image (PNG/JPG/WebP/etc.).",
    )
    with_recommendation: bool = Field(
        default=True,
        description="If true, run the recommender on the extracted brief and include the result.",
    )


# v2.1 — synthesis + decisions log MCP inputs

class UxSynthesizeInput(BaseModel):
    project_root: Optional[str] = Field(
        default=None,
        description="The project folder. When it holds an existing design system, the "
                    "synthesis comes back as a suggestion its tokens override.")
    industry: str = Field(default="", description="Industry id, e.g. fintech-payments.")
    tone: List[str] = Field(default_factory=list, description="Tone tags.")
    audience: List[str] = Field(default_factory=list, description="Audience tags.")
    must_have: List[str] = Field(default_factory=list, description="Must-have tags.")
    forbidden: List[str] = Field(default_factory=list, description="Forbidden tags.")
    reference_brands: List[str] = Field(
        default_factory=list,
        description="Reference brand ids. Empty = pure synthesis. Set = brand_anchor mode.",
    )
    strict: bool = Field(
        default=False,
        description="With reference_brands: emit brand tokens verbatim (no synthesis).",
    )


class UxDecisionsQueryInput(BaseModel):
    industry: Optional[str] = Field(default=None, description="Filter by industry.")
    ui_type: Optional[str] = Field(default=None, description="Filter by ui_type.")
    command: Optional[str] = Field(default=None,
        description="Filter by command (recommend, design, lint, evolve, synthesize).")
    min_score: Optional[int] = Field(default=None, description="Min lint_score filter.")
    accepted_only: bool = Field(default=False, description="user_accepted=true only.")
    limit: Optional[int] = Field(default=50, description="Max rows.")


class UxDecisionsStatsInput(BaseModel):
    pass


# 4.0 beta: the foundations engine

class UxSystemBuildInput(BaseModel):
    brand: Any = Field(
        default=None,
        description="Brand color as hex, for example '#3366FF'. Required.")
    brief: Any = Field(
        default=None,
        description="Optional brief object (industry, tone, audience, must_have, forbidden, "
                    "character); the synthesizer places the axes from it. Do not combine with "
                    "axes. "
                    + BRIEF_FIELDS_HELP)
    axes: Any = Field(
        default=None,
        description="Optional list of seven numbers from 0 to 1: warmth, contrast, density, "
                    "geometry, formality, motion, type_personality. Do not combine with brief.")
    latin_only: Any = Field(
        default=False,
        description="Optional true or false (default false). True leaves out the Arabic face "
                    "and scale.")
    out: Any = Field(
        default=None,
        description="Optional folder path, best absolute. When given, the tool writes "
                    "tokens.json, tokens.css, fonts.css, fonts-self-host.css, system-report.md "
                    "and art/ there, as `uxskill system build --out` does: identical files "
                    "are left alone, and if any file differs nothing is written unless force "
                    "is true.")
    include_files: Any = Field(
        default=False,
        description="Optional true or false (default false). True adds the tokens.css text "
                    "(css) and the tokens.json text (dtcg) to the result. They are large "
                    "(tokens.json is over 100 KB), so prefer out.")
    force: Any = Field(
        default=False,
        description="Optional true or false (default false). With out, true replaces files "
                    "that differ.")


# A system a project already has (engine.io.commands, shared with the CLI)

_PATH = "the absolute path of"


class UxSystemImportInput(BaseModel):
    source: Any = Field(default=None, description=f"Required. {_PATH} the system: tokens.json, a "
                        "stylesheet, a Tailwind theme, a markdown file or folder, a Figma "
                        "variables export, or a project folder. A list reads several files as "
                        "one system: the system first, then each stylesheet that adds to it "
                        "(its dark values, say).")
    format: Any = Field(default="auto", description="Optional: auto (default, told from the "
                        "file), dtcg, css, tailwind, tailwind-json, markdown or figma.")
    out: Any = Field(default=None, description=f"Optional. {_PATH} a folder to write into, after "
                     "every source is checked and backed up under .uxskill/ there.")
    force: Any = Field(default=False, description="Optional true or false: with out, replace "
                       "files ux-skill wrote that differ (each is backed up first).")
    figma_modes: Any = Field(default=None, description="Optional object: for a Figma collection "
                             "with more than two modes, the second mode to read, for example "
                             "{\"Type\": \"SM\"}.")


class UxSystemEnhanceInput(UxSystemImportInput):
    mapping: Any = Field(default=None, description=f"Optional. {_PATH} mapping.json; without it "
                         "the mapping.json in out (or beside the source) is read, merged with a "
                         "mapping proposed from names.")
    scan: Any = Field(default=None, description="Optional list of absolute paths of product "
                      "code folders or files to measure.")


class UxSystemExtendInput(UxSystemEnhanceInput):
    add: Any = Field(default=None, description="Optional list of foundations to add: color, "
                     "type, space, radius, border, elevation, motion, layout, imagery.")
    add_role: Any = Field(default=None, description="Optional list of role=token pairs that "
                          "point the engine's roles at the system's own tokens, for example "
                          "color.focus.ring=brand-700.")
    add_modes: Any = Field(default=None, description="Optional list of mode axes the system "
                           "does not have to add with the foundations: contrast, motion or "
                           "density. Without it none is added.")
    contracts: Any = Field(default=None, description="Optional list of absolute paths of "
                           "contract .yaml files to check and add.")
    brand: Any = Field(default=None, description="Optional brand color as hex for added color; "
                       "without it the system's own primary fill is used.")
    axes: Any = Field(default=None, description="Optional seven numbers from 0 to 1 that shape "
                      "an added foundation. Do not combine with brief.")
    brief: Any = Field(default=None, description="Optional brief object (industry, tone, "
                       "audience, must_have, forbidden, headline) that places the axes for an "
                       "added foundation. Do not combine with axes. " + BRIEF_FIELDS_HELP)
    latin_only: Any = Field(default=False, description="Optional true or false: add type "
                            "without the Arabic face.")


class UxSystemExportInput(UxSystemImportInput):
    to: Any = Field(default=None, description="Required: css (tokens.css), tailwind (a "
                    "Tailwind 4 theme), figma (Figma variables and the script that applies "
                    "them) or dtcg (tokens.json).")
    scheme: Any = Field(default=None, description="Optional: system, light or dark, the scheme "
                        "the css or tailwind file opens in. A stylesheet keeps its own; "
                        "tokens.json holds none, so it opens in system when left out.")
    include_files: Any = Field(default=False, description="Optional true or false: return the "
                               "file texts too. Prefer out.")


class UxContractsCheckInput(BaseModel):
    folder: Any = Field(default=None, description=f"Required. {_PATH} a folder of contract "
                        ".yaml files.")
    tokens: Any = Field(default=None, description=f"Required. {_PATH} the system, in any format "
                        "the import reads.")
    format: Any = Field(default="auto", description="Optional: auto (default), dtcg, css, "
                        "tailwind, tailwind-json, markdown or figma.")
    mapping: Any = Field(default=None, description=f"Optional. {_PATH} mapping.json; without it "
                         "the one beside the system is read when there is one.")


# How the command layer names each input in a message: the MCP fields.
_MCP_LABELS = {"from": "source", "format": "format", "out": "out", "force": "force: true",
               "replace_client": "the command line's --replace-client-files",
               "mapping": "mapping", "add": "add", "add_role": "add_role", "to": "to",
               "brand": "brand", "axes": "axes", "brief": "brief", "tokens": "tokens",
               "latin_only": "latin_only", "scheme": "scheme", "figma_mode": "figma_modes",
               "import": "ux_system_import", "add_mode": "add_modes"}
# The most folded problem lines a contract check returns over MCP.
_PROBLEM_CAP = 40


def _abs_path(value: Any, label: str, example: str, required: bool = False,
              kind: str = "") -> Optional[str]:
    """An absolute path as text, or None when optional and left out; with
    `kind` ("folder" or "file") it must exist as one. Raises InputError
    naming `label` and the fix."""
    from engine.foundations.emit import InputError
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            raise InputError(f"{label} is missing; pass {_PATH} it, for example "
                             f"/Users/you/project/{example}")
        return None
    if not isinstance(value, str):
        raise InputError(f"{label} is {value!r}; pass {_PATH} it as text, for example "
                         f"/Users/you/project/{example}")
    p = Path(value).expanduser()
    if not p.is_absolute():
        raise InputError(f"{label} is {value!r}, a relative path; the MCP server runs in its own "
                         f"folder, so pass an absolute path, for example "
                         f"/Users/you/project/{example}")
    if kind and not (p.is_dir() if kind == "folder" else p.is_file()):
        raise InputError(f"{label} {p} is not a {kind} that exists; pass {_PATH} an existing "
                         f"{kind}")
    return str(p)


def _paths(value: Any, label: str, example: str, kind: str = "") -> List[str]:
    from engine.foundations.emit import InputError
    items = [] if value is None else ([value] if isinstance(value, str) else value)
    if not isinstance(items, list):
        raise InputError(f"{label} is {value!r}; pass a list of absolute paths, for example "
                         f"[\"/Users/you/project/{example}\"]")
    return [str(_abs_path(v, label, example, required=True, kind=kind)) for v in items]


def _words(value: Any, label: str) -> List[str]:
    from engine.foundations.emit import InputError
    items = [] if value is None else ([value] if isinstance(value, str) else value)
    if not (isinstance(items, list) and all(isinstance(v, str) for v in items)):
        raise InputError(f"{label} is {value!r}; pass a list of words")
    return items


def _source(value: Any, example: str, label: str = "source") -> Any:
    """One absolute path, or a list of them (several files read as one system)."""
    if isinstance(value, list) and value:
        return _paths(value, label, example)
    return _abs_path(value, label, example, required=True)


def _io_call(fn: Callable[[], Dict[str, Any]], args: Optional[Dict[str, Any]] = None,
             model: Any = None, tool: str = "") -> Dict[str, Any]:
    from engine.foundations.emit import InputError
    try:
        if model is not None:
            _known_fields(args, model, tool)
        return fn()
    except InputError as exc:
        return {"status": "invalid", "error": str(exc)}


def _known_fields(args: Optional[Dict[str, Any]], model: Any, tool: str) -> None:
    """A field the tool does not have is reported, never ignored: a
    misspelled scan would otherwise give a report with no code measured.
    Raises InputError naming the field, the nearest field the tool has and
    every field it takes."""
    import difflib
    from engine.foundations.emit import InputError
    fields = list(model.model_fields)
    unknown = [k for k in (args or {}) if k not in fields]
    if not unknown:
        return
    near = difflib.get_close_matches(unknown[0], fields, n=1)
    hint = f"did you mean {near[0]}? " if near else ""
    others = f" ({', '.join(unknown[1:])} too)" if len(unknown) > 1 else ""
    raise InputError(f"{unknown[0]}{others} is not a field of {tool}; {hint}use "
                     f"{', '.join(fields[:-1])} or {fields[-1]}, or leave it out")


def _format(value: Any) -> str:
    from engine.foundations.emit import InputError
    if value is None:
        return "auto"
    if not isinstance(value, str):
        raise InputError(f"format is {value!r}; pass auto, dtcg, css, tailwind, tailwind-json, "
                         "markdown or figma")
    return value


def _folded(result: Dict[str, Any]) -> Dict[str, Any]:
    """A contract check small enough for one tool result: counts, problems
    by rule, and the problems folded by what they say once the contract and
    part are set aside, each with how many and which contracts, at most
    _PROBLEM_CAP of them. `lines` repeats `problems` and is dropped."""
    import re
    problems = result.pop("problems")
    result.pop("lines", None)
    groups: Dict[Tuple[str, str], Dict[str, Any]] = {}
    by_rule: Dict[str, int] = {}
    for p in problems:
        said = re.sub(r"^[\w.-]+: [\w.-]+(?: \([^)]*\))? ", "", p["message"])
        entry = groups.setdefault((p["rule"], said), {"rule": p["rule"], "message": said,
                                                      "count": 0, "contracts": []})
        entry["count"] += 1
        if p["contract"] not in entry["contracts"]:
            entry["contracts"].append(p["contract"])
        by_rule[p["rule"]] = by_rule.get(p["rule"], 0) + 1
    folded = sorted(groups.values(), key=lambda g: -g["count"])
    result.update({"problems_total": len(problems), "by_rule": by_rule,
                   "problems": folded[:_PROBLEM_CAP],
                   "problems_omitted": sum(g["count"] for g in folded[_PROBLEM_CAP:])})
    if result["problems_omitted"]:
        result["notes"].append(f"{result['problems_omitted']} more problems are not shown; "
                               "uxskill contracts check prints every one.")
    return result


def _common(payload: Any) -> Dict[str, Any]:
    """format, out, force and figma_modes, checked, as the command layer takes them."""
    from engine.foundations.emit import InputError, parse_switch
    modes = payload.figma_modes
    if modes is not None and not (isinstance(modes, dict) and all(
            isinstance(k, str) and isinstance(v, str) for k, v in modes.items())):
        raise InputError(f"figma_modes is {modes!r}; pass an object such as "
                         "{\"Type\": \"SM\"}, collection to mode, or leave it out")
    return {"fmt": _format(payload.format), "out": _abs_path(payload.out, "out", "design-system"),
            "force": parse_switch(payload.force, "force", "replace files in out that differ",
                                  "write nothing when a file differs"),
            "second_modes": modes, "labels": _MCP_LABELS}


def handle_ux_system_import(args: Dict[str, Any]) -> Dict[str, Any]:
    """Read an existing system in its own names and report what was read.
    The result holds counts, the proposed mapping's counts and the import
    report; `not_read` is a count, the report lists each entry."""
    from engine.io.commands import run_import
    payload = UxSystemImportInput.model_validate(args or {})

    def run() -> Dict[str, Any]:
        result = run_import(_source(payload.source, "theme.css"), **_common(payload))
        result["not_read"] = result.pop("not_read_count")
        return result
    return _io_call(run, args, UxSystemImportInput, "ux_system_import")


def handle_ux_system_enhance(args: Dict[str, Any]) -> Dict[str, Any]:
    """Measure an existing system and the code that uses it: a report,
    written as enhance-report.md only with out."""
    from engine.io.commands import run_enhance
    payload = UxSystemEnhanceInput.model_validate(args or {})

    def run() -> Dict[str, Any]:
        source = _source(payload.source, "theme.css")
        return run_enhance(source, mapping=_abs_path(payload.mapping, "mapping", "mapping.json"),
                           scan=_paths(payload.scan, "scan", "src"), **_common(payload))
    return _io_call(run, args, UxSystemEnhanceInput, "ux_system_enhance")


def handle_ux_system_extend(args: Dict[str, Any]) -> Dict[str, Any]:
    """Add to an existing system without changing a token it has: an
    extension file beside a system ux-skill did not write, or its own
    system rewritten in place after a backup."""
    from engine.foundations.emit import InputError, parse_latin_only
    from engine.io.commands import run_extend
    payload = UxSystemExtendInput.model_validate(args or {})

    def run() -> Dict[str, Any]:
        source = _source(payload.source, "theme.css")
        common = _common(payload)
        if common["out"] is None:
            raise InputError(f"out is missing; pass {_PATH} the folder for mapping.json and "
                             "extend-report.md, for example /Users/you/project/design-system")
        if payload.brief is not None and not isinstance(payload.brief, dict):
            raise InputError(f"brief is {payload.brief!r}; pass an object such as "
                             '{"industry": "saas"}, or leave it out')
        return run_extend(
            source, mapping=_abs_path(payload.mapping, "mapping", "mapping.json"),
            add=_words(payload.add, "add"), add_role=_words(payload.add_role, "add_role"),
            add_mode=_words(payload.add_modes, "add_modes"),
            contracts=_paths(payload.contracts, "contracts", "chip.yaml", "file"),
            brand=payload.brand, axes=payload.axes, brief=payload.brief,
            latin_only=parse_latin_only(payload.latin_only, "latin_only"), **common)
    return _io_call(run, args, UxSystemExtendInput, "ux_system_extend")


def handle_ux_system_export(args: Dict[str, Any]) -> Dict[str, Any]:
    """A system in another format, written only into out; the file texts
    come back only with include_files."""
    from engine.foundations.emit import InputError, parse_switch
    from engine.io.commands import run_export
    payload = UxSystemExportInput.model_validate(args or {})

    def run() -> Dict[str, Any]:
        source = _source(payload.source, "tokens.json")
        if payload.to is None:
            raise InputError("to is missing; pass css, tailwind, figma or dtcg")
        include = parse_switch(payload.include_files, "include_files", "return the file texts",
                               "return only their sizes")
        return run_export(source, to=payload.to, include_files=include, scheme=payload.scheme,
                          **_common(payload))
    return _io_call(run, args, UxSystemExportInput, "ux_system_export")


def handle_ux_contracts_check(args: Dict[str, Any]) -> Dict[str, Any]:
    """Check a folder of component contracts against a system: counts, and
    the problems folded and capped (_folded)."""
    from engine.io.commands import run_contracts_check
    payload = UxContractsCheckInput.model_validate(args or {})

    def run() -> Dict[str, Any]:
        return _folded(run_contracts_check(
            _abs_path(payload.folder, "folder", "contracts", required=True, kind="folder"),
            _source(payload.tokens, "tokens.json", "tokens"), fmt=_format(payload.format),
            mapping=_abs_path(payload.mapping, "mapping", "mapping.json"), labels=_MCP_LABELS))
    return _io_call(run, args, UxContractsCheckInput, "ux_contracts_check")


# ---------------------------------------------------------------------------
# Filter helpers
# ---------------------------------------------------------------------------


def _filter_entries(entries: List[Dict[str, Any]], **filters: Optional[str]) -> List[Dict[str, Any]]:
    """Filter a list of entries by exact match on each non-None filter key.

    Each filter key is matched against ``entry.get(key)``. Filters whose
    value is None are skipped so callers can pass them through unconditionally.
    """
    out = entries
    for key, value in filters.items():
        if value is None:
            continue
        out = [e for e in out if e.get(key) == value]
    return out


# ---------------------------------------------------------------------------
# Pure handlers — dict in, dict out. No mcp dependency.
# ---------------------------------------------------------------------------


def handle_ux_recommend(args: Dict[str, Any]) -> Dict[str, Any]:
    """Run the 5-parallel-search recommender and return a serialisable dict."""
    payload = UxRecommendInput.model_validate(args or {})
    brief_kwargs = payload.brief.model_dump()
    brief = Brief(**brief_kwargs)
    if payload.project_root:
        from engine.existing import detect_existing_system
        found = detect_existing_system(payload.project_root)
        brief.existing_system = found if found.get("found") else None
    rec = recommend(brief)
    return rec.to_dict()


from engine.existing import mark_suggestions  # noqa: E402


def _found(project_root: Optional[str]) -> Optional[Dict[str, Any]]:
    """The existing design system under ``project_root``, or None."""
    if not project_root:
        return None
    from engine.existing import detect_existing_system
    found = detect_existing_system(project_root)
    return found if found.get("found") else None


def handle_ux_system_detect(args: Dict[str, Any]) -> Dict[str, Any]:
    """Find an existing design system under ``root`` and what it declares."""
    payload = UxSystemDetectInput.model_validate(args or {})
    from engine.existing import detect_existing_system
    if not Path(payload.root).expanduser().is_dir():
        return {"found": False, "error": f"root {payload.root} does not exist or is not a "
                                         "folder; pass the project folder"}
    return detect_existing_system(payload.root)


def handle_ux_lint(args: Dict[str, Any]) -> Dict[str, Any]:
    """Run the regex linter over the given paths and return the findings."""
    payload = UxLintInput.model_validate(args or {})
    report = lint(payload.paths, severity_threshold=payload.threshold)
    return report.to_dict()


def handle_ux_styles(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return all entries from ``data/styles.json``."""
    UxStylesInput.model_validate(args or {})
    data = load("styles")
    return {"count": len(data.get("entries", [])), "entries": data.get("entries", [])}


def handle_ux_palettes(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``data/palettes.json`` entries, optionally filtered by ``mode``."""
    payload = UxPalettesInput.model_validate(args or {})
    data = load("palettes")
    entries = _filter_entries(data.get("entries", []), mode=payload.mode)
    return {"count": len(entries), "filter": {"mode": payload.mode}, "entries": entries}


def handle_ux_type_pairs(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return all entries from ``data/type-pairs.json``."""
    UxTypePairsInput.model_validate(args or {})
    data = load("type-pairs")
    return {"count": len(data.get("entries", [])), "entries": data.get("entries", [])}


def handle_ux_components(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``data/components.json`` entries, optionally filtered by category."""
    payload = UxComponentsInput.model_validate(args or {})
    data = load("components")
    entries = _filter_entries(data.get("entries", []), category=payload.category)
    return {"count": len(entries), "filter": {"category": payload.category}, "entries": entries}


def handle_ux_industries(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``data/industries.json`` entries, optionally filtered by category."""
    payload = UxIndustriesInput.model_validate(args or {})
    data = load("industries")
    entries = _filter_entries(data.get("entries", []), category=payload.category)
    return {"count": len(entries), "filter": {"category": payload.category}, "entries": entries}


def handle_ux_motion_presets(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``data/motion-presets.json`` entries, optionally filtered by category."""
    payload = UxMotionPresetsInput.model_validate(args or {})
    data = load("motion-presets")
    entries = _filter_entries(data.get("entries", []), category=payload.category)
    return {"count": len(entries), "filter": {"category": payload.category}, "entries": entries}


def handle_ux_anti_patterns(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``data/anti-patterns.json`` entries, optionally filtered by severity."""
    payload = UxAntiPatternsInput.model_validate(args or {})
    data = load("anti-patterns")
    entries = _filter_entries(data.get("entries", []), severity=payload.severity)
    return {"count": len(entries), "filter": {"severity": payload.severity}, "entries": entries}


def handle_ux_brands(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return brand specs from ``data/brands/*.json``, optionally filtered by category."""
    payload = UxBrandsInput.model_validate(args or {})
    brands = load_brands()
    if payload.category is not None:
        brands = [b for b in brands if b.get("category") == payload.category]
    return {"count": len(brands), "filter": {"category": payload.category}, "entries": brands}


def handle_ux_landing_patterns(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``data/landing-patterns.json`` entries, optionally filtered by category."""
    payload = UxLandingPatternsInput.model_validate(args or {})
    data = load("landing-patterns")
    entries = _filter_entries(data.get("entries", []), category=payload.category)
    return {"count": len(entries), "filter": {"category": payload.category}, "entries": entries}


def handle_ux_persist_save(args: Dict[str, Any]) -> Dict[str, Any]:
    """Persist a recommendation as ``.ux/design-system/MASTER.md`` and return its path."""
    payload = UxPersistSaveInput.model_validate(args or {})
    from engine.persist import save_master_result
    result = save_master_result(payload.project_root, payload.recommendation, payload.brief)
    return {**result, "project_root": payload.project_root}


def handle_ux_persist_load(args: Dict[str, Any]) -> Dict[str, Any]:
    """Load ``.ux/design-system/MASTER.md`` back into a structured dict (or None)."""
    payload = UxPersistLoadInput.model_validate(args or {})
    result = load_master(payload.project_root)
    if result is None:
        return {"found": False, "project_root": payload.project_root}
    return {"found": True, "project_root": payload.project_root, "master": result}


def handle_ux_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    """Return version + per-manifest entry counts."""
    UxStatsInput.model_validate(args or {})
    return {"version": __version__, "counts": stats()}


def handle_ux_image_extract(args: Dict[str, Any]) -> Dict[str, Any]:
    """Extract a synthetic Brief from a design image and (optionally) recommend.

    Pure-CV pipeline via Pillow — no multimodal LLM calls. Returns the brief,
    the raw extraction hints (dominant colors, canvas polarity, type polarity,
    matched palette + style), and (if requested) the merged recommendation.
    """
    payload = UxImageExtractInput.model_validate(args or {})
    try:
        from engine.image_extract import image_to_brief
    except ImportError as exc:  # pragma: no cover - environment specific
        return {"error": "Pillow not installed", "hint": str(exc)}

    try:
        result = image_to_brief(payload.path)
    except RuntimeError as exc:
        return {"error": str(exc)}
    except FileNotFoundError as exc:
        return {"error": str(exc)}

    response: Dict[str, Any] = {
        "image": payload.path,
        "brief": result["brief"],
        "hints": result["hints"],
    }
    if payload.with_recommendation:
        brief_kwargs = {
            k: v for k, v in result["brief"].items()
            if k in {"project_type", "industry", "audience", "tone",
                     "must_have", "forbidden", "stack", "region"}
        }
        image_brief = Brief(**brief_kwargs)
        image_brief.existing_system = _found(payload.project_root)
        rec = recommend(image_brief)
        response["recommendation"] = rec.to_dict()
    return response


# v2.1 — synthesis + decisions log handlers

def handle_ux_synthesize(args: Dict[str, Any]) -> Dict[str, Any]:
    """Synthesize a fresh design language from a brief (v2.1).

    Modes: pure_synthesis (no brand) / brand_anchor (with brand) / strict_brand.
    All offline, deterministic, no LLM.
    """
    payload = UxSynthesizeInput.model_validate(args or {})
    from engine import synthesize as _synth
    b = Brief(
        industry=payload.industry,
        tone=list(payload.tone),
        audience=list(payload.audience),
        must_have=list(payload.must_have),
        forbidden=list(payload.forbidden),
    )
    # Attach v2.1 fields via duck-typed setattr
    object.__setattr__(b, "reference_brands", list(payload.reference_brands))
    object.__setattr__(b, "strict", payload.strict)
    out = _synth(b)
    # Log decision
    try:
        from engine.decisions import record as _rec
        _rec({
            "command": "synthesize",
            "industry": payload.industry or None,
            "mode": out.mode,
            "picked_brand": out.anchor_brand_id,
            "axes": out.axes,
        })
    except Exception:
        pass
    return mark_suggestions(out.to_dict(), _found(payload.project_root))


def handle_ux_decisions_query(args: Dict[str, Any]) -> Dict[str, Any]:
    """Filter the decisions ledger by industry / ui_type / command / score."""
    payload = UxDecisionsQueryInput.model_validate(args or {})
    from engine.decisions import query
    rows = query(
        industry=payload.industry,
        ui_type=payload.ui_type,
        command=payload.command,
        min_score=payload.min_score,
        accepted_only=payload.accepted_only,
        limit=payload.limit,
    )
    return {"count": len(rows), "rows": rows}


def handle_ux_decisions_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate stats over the decisions ledger (top brands, lint score median…)."""
    UxDecisionsStatsInput.model_validate(args or {})
    from engine.decisions import stats as _ds
    return _ds()


def handle_ux_system_build(args: Dict[str, Any]) -> Dict[str, Any]:
    """Build a WCAG-gated design system with the 4.0 foundations engine.

    The result is small by default: status, passed, gate, findings, the
    report text and each file's name and size in bytes. The file texts
    (css, dtcg) come back only with include_files, since tokens.json alone
    is too large for one agent tool result. With out, the files are
    written through the same safe writer and statuses as `uxskill system
    build`; without it nothing is written and status is "built" or
    "failed". A bad input returns status "invalid", passed=false and an
    error naming the input and the fix.
    """
    from engine.foundations.emit import (
        InputError, brief_audience, brief_words, check_out_dir, choose_axes, make_system,
        note_rule_pack, nudge_lines, parse_brand, parse_latin_only, parse_switch, resolve_arabic,
        unread_lines, write_outcome)
    payload = UxSystemBuildInput.model_validate(args or {})
    try:
        brand = parse_brand(payload.brand, "brand")
        if payload.brief is not None and not isinstance(payload.brief, dict):
            raise InputError(f"brief is {payload.brief!r}; pass an object such as "
                             '{"industry": "saas", "tone": ["warm"]}, or leave it out')
        axes, source = choose_axes(payload.brief, payload.axes)
        latin_only = parse_latin_only(payload.latin_only, "latin_only")
        audience = brief_audience(payload.brief, "brief")
        words = brief_words(payload.brief, "brief")
        arabic = resolve_arabic(latin_only, audience, "latin_only")
        include_files = parse_switch(payload.include_files, "include_files",
                                     "return the tokens.css and tokens.json text",
                                     "return only their sizes")
        force = parse_switch(payload.force, "force", "replace files in out that differ",
                             "write nothing when a file differs")
        out_arg = payload.out
        if isinstance(out_arg, str) and out_arg.strip():
            if not Path(out_arg).expanduser().is_absolute():
                raise InputError(
                    f"out is {out_arg!r}, a relative path; the MCP server runs in its own "
                    "folder, so pass an absolute path, for example /Users/you/project/tokens")
            out_arg = str(Path(out_arg).expanduser())
        out = None if out_arg is None else check_out_dir(out_arg, "out")
    except InputError as exc:
        return {"status": "invalid", "passed": False, "error": str(exc), "findings": [],
                "report": "", "files": []}
    system = make_system(brand, axes, source, arabic=arabic, audience=audience,
                         unread=unread_lines(payload.brief, "brief"),
                         nudges=nudge_lines(payload.brief, "brief"), words=words)
    if out is not None:
        system = note_rule_pack(system, out, force=force)
    result: Dict[str, Any] = {
        "status": "built" if system.passed else "failed", **system.to_dict(),
        "report": system.report,
        "files": [{"name": name, "bytes": len(text.encode("utf-8"))}
                  for name, text in system.files.items()]}
    if include_files:
        result.update(css=system.files.get("tokens.css", ""),
                      dtcg=system.files.get("tokens.json", ""))
    if out is not None:
        result["out"] = str(out)
        from engine.existing import client_files_in
        theirs = client_files_in(out, system.files) if force else []
        if theirs:
            # An existing design system is fixed input: force never replaces it here.
            result.update({
                "status": "refused", "written": [], "unchanged": [], "conflicts": theirs,
                "stale_rule_pack": None,
                "message": (f"Nothing was written: {out} holds a design system ux-skill did not "
                            f"build, and {', '.join(theirs)} would be replaced. An existing "
                            "design system is fixed input; pass a new out folder. Only the "
                            "command line's --replace-client-files replaces it."),
            })
        else:
            result.update(write_outcome(system, out, force=force, force_label="force: true",
                                        out_label="out"))
            from engine.existing.record import RECORD, record_unchanged
            if result["status"] == "unchanged" and record_unchanged(out, system.files):
                result["message"] += (f" Recorded the files in {out / RECORD}, so force: true "
                                      "can tell them from files you edit.")
    return result


# ---------------------------------------------------------------------------
# Tool catalogue — single source of truth
# ---------------------------------------------------------------------------

# (handler, input_model, description)
ToolEntry = Tuple[Callable[[Dict[str, Any]], Dict[str, Any]], Type[BaseModel], str]

TOOLS: Dict[str, ToolEntry] = {
    "ux_recommend": (
        handle_ux_recommend,
        UxRecommendInput,
        "Run the 5-parallel-search recommender over a brief and return the "
        "merged design system (style, palette, type pair, motion, components, "
        "brand exemplars, anti-pattern guardrails, rationale).",
    ),
    "ux_system_detect": (
        handle_ux_system_detect,
        UxSystemDetectInput,
        "Find an existing design system in a project (a DTCG or tokens.json file, a token "
        "build script, CSS custom-property foundations, a hand-written MASTER.md or DESIGN.md) "
        "and return its files and what it declares: primary, text color, fonts, named colors "
        "and page languages. An existing system is fixed input: read it before any other "
        "tool, and never override or overwrite it.",
    ),
    "ux_lint": (
        handle_ux_lint,
        UxLintInput,
        "Run the anti-AI-slop regex linter over the given paths. Returns "
        "structured findings with rule id, severity, file, line, excerpt, fix.",
    ),
    "ux_styles": (
        handle_ux_styles,
        UxStylesInput,
        "Return all entries from data/styles.json (84+ design philosophies).",
    ),
    "ux_palettes": (
        handle_ux_palettes,
        UxPalettesInput,
        "Return entries from data/palettes.json. Optional mode filter "
        "('light' | 'dark').",
    ),
    "ux_type_pairs": (
        handle_ux_type_pairs,
        UxTypePairsInput,
        "Return all entries from data/type-pairs.json (display + body + mono "
        "type pairings).",
    ),
    "ux_components": (
        handle_ux_components,
        UxComponentsInput,
        "Return entries from data/components.json. Optional category filter.",
    ),
    "ux_industries": (
        handle_ux_industries,
        UxIndustriesInput,
        "Return entries from data/industries.json with style/palette/type "
        "biases for each domain. Optional category filter.",
    ),
    "ux_motion_presets": (
        handle_ux_motion_presets,
        UxMotionPresetsInput,
        "Return entries from data/motion-presets.json (easing, duration, "
        "stagger tokens). Optional category filter.",
    ),
    "ux_anti_patterns": (
        handle_ux_anti_patterns,
        UxAntiPatternsInput,
        "Return entries from data/anti-patterns.json (the regex rules that "
        "drive the linter). Optional severity filter.",
    ),
    "ux_brands": (
        handle_ux_brands,
        UxBrandsInput,
        "Return brand specs from data/brands/*.json (Apple, Stripe, Linear, "
        "Tesla, Notion, etc.). Optional category filter.",
    ),
    "ux_landing_patterns": (
        handle_ux_landing_patterns,
        UxLandingPatternsInput,
        "Return entries from data/landing-patterns.json (proven landing-page "
        "section patterns). Optional category filter.",
    ),
    "ux_persist_save": (
        handle_ux_persist_save,
        UxPersistSaveInput,
        "Persist a recommendation as .ux/design-system/MASTER.md in the "
        "given project root. Idempotent — same input produces byte-identical bytes.",
    ),
    "ux_persist_load": (
        handle_ux_persist_load,
        UxPersistLoadInput,
        "Load .ux/design-system/MASTER.md back into a structured dict, or "
        "report not-found.",
    ),
    "ux_stats": (
        handle_ux_stats,
        UxStatsInput,
        "Return the engine version and per-manifest entry counts. Useful as "
        "a health check.",
    ),
    "ux_image_extract": (
        handle_ux_image_extract,
        UxImageExtractInput,
        "Read a design image (PNG/JPG/WebP) and return a synthetic Brief plus "
        "diagnostic hints (dominant colors, canvas polarity, matched palette + "
        "style). Pure CV — no multimodal LLM calls. Set with_recommendation=true "
        "(default) to also run the recommender on the extracted brief.",
    ),
    "ux_synthesize": (
        handle_ux_synthesize,
        UxSynthesizeInput,
        "v2.1 — synthesize a fresh design language from a brief. Returns "
        "axes + palette + type pair + spacing + radius + motion. Mode "
        "auto-dispatched: pure_synthesis (no brand) / brand_anchor (with "
        "reference_brands) / strict_brand (reference_brands + strict=true). "
        "100% offline. Deterministic. No LLM.",
    ),
    "ux_decisions_query": (
        handle_ux_decisions_query,
        UxDecisionsQueryInput,
        "v2.1 — filter the local decisions ledger (.ux/decisions.jsonl + "
        "~/.uxskill/decisions.jsonl) by industry / ui_type / command / "
        "min_score / accepted_only. The recommender re-ranks based on this "
        "data once >= 3 prior decisions exist in the brief's bucket.",
    ),
    "ux_decisions_stats": (
        handle_ux_decisions_stats,
        UxDecisionsStatsInput,
        "v2.1 — aggregate stats over the local decisions ledger. Returns "
        "total decisions, by_command, by_industry, by_ui_type, by_mode, "
        "top_brands, lint_score_median, acceptance_rate. No telemetry — "
        "this is your install's local view of what it has learned.",
    ),
    "ux_system_build": (
        handle_ux_system_build,
        UxSystemBuildInput,
        "4.0 beta: build a WCAG-gated design system from a brand color, with the brief or "
        "seven axes optional. Nine foundations (color, type, space, layout, radius, border, "
        "elevation, motion, imagery) with light, dark, high contrast, density, right-to-left "
        "Arabic and reduced motion modes. Returns status, passed, the gate line, findings, a "
        "plain report and each file's size. Pass out (a folder) to write tokens.json, "
        "tokens.css, fonts.css, fonts-self-host.css, system-report.md and art/ there, refused "
        "when a file differs unless force is true; pass include_files true to get the css and "
        "dtcg text back instead. Without out it writes nothing. " + BRIEF_FIELDS_HELP,
    ),
    "ux_system_import": (
        handle_ux_system_import,
        UxSystemImportInput,
        "Read a design system a project already has (DTCG tokens.json, CSS custom properties, "
        "a Tailwind theme, markdown rule files, a Figma variables export, or several files as "
        "one) in its own names. Returns the counts, how many entries were not read, a proposed "
        "mapping to the engine's roles and the import report. Pass out (an absolute folder) to "
        "write import-report.md and mapping.json there.",
    ),
    "ux_system_enhance": (
        handle_ux_system_enhance,
        UxSystemEnhanceInput,
        "Measure a system a project already has and, with scan, the code that uses it: unused "
        "tokens, raw values a token holds, values written several ways, names every use "
        "contradicts, and the WCAG gate read through the mapping. A report only; no token or "
        "code is rewritten. Pass out to write enhance-report.md.",
    ),
    "ux_system_extend": (
        handle_ux_system_extend,
        UxSystemExtendInput,
        "Add foundations, roles or contracts to a system a project already has without "
        "changing a token it has. A system ux-skill did not write gets an extension file beside "
        "it; its own is rewritten in place after a backup. The report goes into out. A result "
        "that does not pass writes only its report and returns status blocked.",
    ),
    "ux_system_export": (
        handle_ux_system_export,
        UxSystemExportInput,
        "Write a system as tokens.css, a Tailwind 4 theme, Figma variables with the script "
        "that applies them, or tokens.json, into out only, never over the source. Without out "
        "it returns each file's size; include_files returns the texts.",
    ),
    "ux_contracts_check": (
        handle_ux_contracts_check,
        UxContractsCheckInput,
        "Check a folder of component contracts against a system: the schema, every role they "
        "bind and every pairing they declare, measured in every mode, read through the "
        "mapping.",
    ),
}


# ---------------------------------------------------------------------------
# Transport — only used when run_server() is actually invoked
# ---------------------------------------------------------------------------


def _ensure_serialisable(value: Any) -> Any:
    """Best-effort JSON-safe conversion for tool results."""
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, BaseModel):
        return value.model_dump()
    return value


def _build_server() -> Any:  # pragma: no cover - requires mcp lib
    """Construct an ``mcp.server.Server`` with every tool in :data:`TOOLS` registered."""
    if not MCP_AVAILABLE:
        raise RuntimeError(
            "The 'mcp' Python package is required to run the ux-skill MCP server. "
            "Install it with:  pip install 'uxskill[mcp]'   or   pip install 'mcp>=1.28.1,<2'.\n"
            f"Original import error: {_MCP_IMPORT_ERROR!r}"
        )

    server = Server("ux-skill")

    @server.list_tools()
    async def _list_tools():  # type: ignore[misc]
        tools = []
        for name, (_handler, model, description) in TOOLS.items():
            tools.append(
                mcp_types.Tool(
                    name=name,
                    description=description,
                    inputSchema=model.model_json_schema(),
                )
            )
        return tools

    @server.call_tool()
    async def _call_tool(name: str, arguments: Dict[str, Any]):  # type: ignore[misc]
        if name not in TOOLS:
            raise ValueError(f"Unknown tool: {name}")
        handler, _model, _description = TOOLS[name]
        logger.info("call_tool name=%s", name)
        try:
            result = handler(arguments or {})
        except Exception as exc:
            logger.exception("call_tool failed name=%s", name)
            err_payload = {"error": str(exc), "type": type(exc).__name__}
            return [mcp_types.TextContent(type="text", text=json.dumps(err_payload))]
        result = _ensure_serialisable(result)
        return [mcp_types.TextContent(type="text", text=json.dumps(result, default=str))]

    return server


def run_server() -> None:
    """Launch the stdio MCP server. Blocks until the client disconnects.

    Raises ``RuntimeError`` with a clear install hint if the ``mcp`` package
    is not available — keeps the import side of this module safe everywhere.
    """
    if not MCP_AVAILABLE:
        raise RuntimeError(
            "The 'mcp' Python package is required to run the ux-skill MCP server. "
            "Install it with:  pip install 'uxskill[mcp]'   or   pip install 'mcp>=1.28.1,<2'."
        )

    import asyncio

    async def _main() -> None:  # pragma: no cover - requires mcp lib
        server = _build_server()
        logger.info("ux-skill MCP server starting on stdio. version=%s tools=%d",
                    __version__, len(TOOLS))
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="ux-skill",
                    server_version=__version__,
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_main())


if __name__ == "__main__":  # pragma: no cover - manual entry point
    run_server()
