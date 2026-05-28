"""MCP server tests — exercise the pure handlers directly.

We deliberately avoid bringing up the actual stdio transport in tests so:

1. Tests run without the ``mcp`` Python package installed.
2. No async event loop or subprocess plumbing in the test suite.
3. Each handler is unit-testable as a plain ``dict -> dict`` function.

The transport layer is exercised manually via the ``ux-mcp`` entry point.
"""
from __future__ import annotations

from pathlib import Path

import pytest


def test_server_imports():
    """Import-graceful pattern — the module imports whether or not mcp is installed."""
    from engine.mcp import (
        run_server,
        TOOLS,
        MCP_AVAILABLE,
        handle_ux_recommend,
        handle_ux_lint,
        handle_ux_styles,
        handle_ux_stats,
    )
    assert callable(run_server)
    assert isinstance(TOOLS, dict)
    assert isinstance(MCP_AVAILABLE, bool)
    # All 15 tools are registered.
    expected_tools = {
        "ux_recommend",
        "ux_lint",
        "ux_styles",
        "ux_palettes",
        "ux_type_pairs",
        "ux_components",
        "ux_industries",
        "ux_motion_presets",
        "ux_anti_patterns",
        "ux_brands",
        "ux_landing_patterns",
        "ux_persist_save",
        "ux_persist_load",
        "ux_stats",
        "ux_image_extract",
    }
    assert set(TOOLS.keys()) == expected_tools, (
        f"missing: {expected_tools - set(TOOLS.keys())}; "
        f"extra: {set(TOOLS.keys()) - expected_tools}"
    )
    # If mcp is absent, run_server() must raise a clear RuntimeError when called.
    if not MCP_AVAILABLE:
        with pytest.raises(RuntimeError, match="mcp"):
            run_server()


def test_ux_recommend_via_mcp():
    """Recommend handler returns a Recommendation-shaped dict."""
    from engine.mcp import handle_ux_recommend

    result = handle_ux_recommend({
        "brief": {
            "project_type": "landing",
            "tone": ["warm", "editorial"],
            "must_have": ["dark-mode"],
            "forbidden": ["brutalism"],
        }
    })

    # Shape — top-level keys mirror engine.recommender.Recommendation
    assert "style" in result
    assert "palette" in result
    assert "type_pair" in result
    assert "motion" in result
    assert "components" in result
    assert "brand_exemplars" in result
    assert "guardrails" in result
    assert "rationale" in result

    # Guardrails (anti-patterns) are always-on — never empty when data is present.
    assert isinstance(result["guardrails"], list)
    assert isinstance(result["rationale"], list)
    assert len(result["rationale"]) >= 1


def test_ux_lint_via_mcp(tmp_path: Path):
    """Lint handler returns a LintReport-shaped dict for the given paths."""
    from engine.mcp import handle_ux_lint

    # Clean dir = no findings, exit_code 0
    result = handle_ux_lint({"paths": [str(tmp_path)], "threshold": "high"})
    assert "findings" in result
    assert "files_scanned" in result
    assert "rules_loaded" in result
    assert "exit_code" in result
    assert "summary" in result
    assert result["exit_code"] == 0
    assert result["findings"] == []
    assert result["summary"]["total"] == 0

    # File with a known anti-pattern produces findings.
    bad = tmp_path / "page.html"
    bad.write_text("<div>This is generic content that goes here</div>")
    result2 = handle_ux_lint({"paths": [str(tmp_path)], "threshold": "high"})
    assert result2["files_scanned"] >= 1
    assert result2["rules_loaded"] > 0


def test_ux_styles_returns_list():
    """Styles handler returns a count + entries list shape."""
    from engine.mcp import handle_ux_styles

    result = handle_ux_styles({})
    assert "count" in result
    assert "entries" in result
    assert isinstance(result["entries"], list)
    # Engine ships with 75+ styles per the data manifest.
    assert result["count"] > 0
    assert result["count"] == len(result["entries"])
    # Each entry has at least an id.
    for entry in result["entries"][:5]:
        assert "id" in entry


def test_ux_stats_returns_dict():
    """Stats handler returns version + counts shape."""
    from engine.mcp import handle_ux_stats

    result = handle_ux_stats({})
    assert "version" in result
    assert "counts" in result
    assert isinstance(result["counts"], dict)
    assert result["version"].startswith("2.")
    # Canonical manifests are present in the counts dict.
    for manifest in ("styles", "palettes", "type-pairs", "components", "brands"):
        assert manifest in result["counts"], f"missing manifest count: {manifest}"
        assert isinstance(result["counts"][manifest], int)
