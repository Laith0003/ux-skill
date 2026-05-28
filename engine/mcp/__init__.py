"""MCP (Model Context Protocol) server for ux-skill.

Exposes the recommender, linter, persistence, and the 11 data manifests as
MCP tools over stdio so ANY MCP-capable client (Claude Desktop, Cursor,
Windsurf, generic agents) can call into the ux-skill engine without
installing the full plugin.

The transport layer (``mcp.server.stdio``) is an optional dependency. The
pure handler functions in :mod:`engine.mcp.server` work whether or not the
``mcp`` package is installed — they are plain ``dict -> dict`` callables so
tests and other callers can exercise them directly.

v2.1 added 3 new tools for the intelligence loop: ``ux_synthesize``,
``ux_decisions_query``, ``ux_decisions_stats``. Total = 18 tools.

Public surface
--------------
``run_server()``  -- launch the stdio MCP server (requires ``pip install mcp``)
``TOOLS``         -- dict mapping tool name to (handler, input_model, description)
``handle_*``      -- the 18 pure handler functions
"""
from engine.mcp.server import (
    run_server,
    TOOLS,
    MCP_AVAILABLE,
    handle_ux_recommend,
    handle_ux_lint,
    handle_ux_styles,
    handle_ux_palettes,
    handle_ux_type_pairs,
    handle_ux_components,
    handle_ux_industries,
    handle_ux_motion_presets,
    handle_ux_anti_patterns,
    handle_ux_brands,
    handle_ux_landing_patterns,
    handle_ux_persist_save,
    handle_ux_persist_load,
    handle_ux_stats,
    handle_ux_image_extract,
    # v2.1 — intelligence loop
    handle_ux_synthesize,
    handle_ux_decisions_query,
    handle_ux_decisions_stats,
)

__all__ = [
    "run_server",
    "TOOLS",
    "MCP_AVAILABLE",
    "handle_ux_recommend",
    "handle_ux_lint",
    "handle_ux_styles",
    "handle_ux_palettes",
    "handle_ux_type_pairs",
    "handle_ux_components",
    "handle_ux_industries",
    "handle_ux_motion_presets",
    "handle_ux_anti_patterns",
    "handle_ux_brands",
    "handle_ux_landing_patterns",
    "handle_ux_persist_save",
    "handle_ux_persist_load",
    "handle_ux_stats",
    "handle_ux_image_extract",
    "handle_ux_synthesize",
    "handle_ux_decisions_query",
    "handle_ux_decisions_stats",
]
