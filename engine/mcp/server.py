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
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel, Field

from engine import __version__
from engine.data_loader import load, load_brands, stats
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
    path: str = Field(
        description="Absolute or relative path to a design image (PNG/JPG/WebP/etc.).",
    )
    with_recommendation: bool = Field(
        default=True,
        description="If true, run the recommender on the extracted brief and include the result.",
    )


# v2.1 — synthesis + decisions log MCP inputs

class UxSynthesizeInput(BaseModel):
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
    rec = recommend(Brief(**brief_kwargs))
    return rec.to_dict()


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
    path = save_master(payload.project_root, payload.recommendation, payload.brief)
    return {"path": path, "project_root": payload.project_root}


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
        rec = recommend(Brief(**brief_kwargs))
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
    return out.to_dict()


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
            "Install it with:  pip install 'uxskill[mcp]'   or   pip install 'mcp>=1.0'.\n"
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
            "Install it with:  pip install 'uxskill[mcp]'   or   pip install 'mcp>=1.0'."
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
