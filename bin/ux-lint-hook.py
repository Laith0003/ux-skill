#!/usr/bin/env python3
"""PostToolUse hook: lint a UI file right after Write, Edit or MultiEdit.

Claude Code pipes the tool call as JSON on stdin. When the written file is a
UI file (HTML, CSS, JSX, TSX, Vue, Svelte, Astro, Blade), this script runs the
anti-pattern linter on it and hands findings at medium severity and above back
to the session as additional context.

It never blocks the write: the tool has already run, every error is swallowed,
and the exit code is always 0.

Turn it off
-----------
* ``UXSKILL_LINT_ON_WRITE=0`` in the environment (for example in the ``env``
  block of ``.claude/settings.json``), or
* an empty file at ``.ux/lint-on-write.off`` in the project root.

Pure Python standard library. The linter modules are loaded without running
``engine/__init__.py``, so no third-party package has to be installed.
"""
from __future__ import annotations

import json
import os
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UI_SUFFIXES = (
    ".html", ".htm", ".css", ".scss", ".jsx", ".tsx",
    ".vue", ".svelte", ".astro", ".blade.php",
)
REPORT_RANKS = {"medium": 1, "high": 2, "critical": 3}
OFF_VALUES = {"0", "off", "false", "no"}
MAX_BYTES = 2_000_000
MAX_LISTED = 20


def _disabled(project_dir: Path) -> bool:
    if os.environ.get("UXSKILL_LINT_ON_WRITE", "").strip().lower() in OFF_VALUES:
        return True
    return (project_dir / ".ux" / "lint-on-write.off").exists()


def _load_linter():
    """Import engine.linter.core without executing engine/__init__.py."""
    if "engine" not in sys.modules:
        pkg = types.ModuleType("engine")
        pkg.__path__ = [str(ROOT / "engine")]  # type: ignore[attr-defined]
        sys.modules["engine"] = pkg
    from engine.linter.core import lint_text

    return lint_text


def _files(payload: dict) -> list:
    tool_input = payload.get("tool_input") or {}
    paths = []
    for key in ("file_path",):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            paths.append(value)
    return paths


def _display(path: Path, project_dir: Path) -> str:
    try:
        return str(path.resolve().relative_to(project_dir.resolve()))
    except ValueError:
        return str(path)


def build_report(paths: list, project_dir: Path) -> str:
    lint_text = None
    blocks = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = project_dir / path
        if not path.name.lower().endswith(UI_SUFFIXES):
            continue
        try:
            if path.stat().st_size > MAX_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if lint_text is None:
            lint_text = _load_linter()
        shown = _display(path, project_dir)
        findings = [
            f for f in lint_text(shown, text)
            if REPORT_RANKS.get(f.severity, 0) >= 1
        ]
        if not findings:
            continue
        findings.sort(key=lambda f: (-REPORT_RANKS[f.severity], f.line, f.column))
        lines = [f"ux-lint found {len(findings)} issue(s) at medium severity or above in {shown}:"]
        for f in findings[:MAX_LISTED]:
            lines.append(
                f"- {shown}:{f.line}:{f.column} [{f.severity}] {f.rule_id}: {f.rule_name}. Fix: {f.fix}"
            )
        if len(findings) > MAX_LISTED:
            lines.append(f"- {len(findings) - MAX_LISTED} more; run `uxskill lint {shown}` for the full list.")
        lines.append(
            "To waive one finding on purpose, add a comment containing "
            "`ux-lint-disable <rule-id>` on that line, or `ux-lint-disable-next-line <rule-id>` above it."
        )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
    if _disabled(project_dir):
        return 0
    try:
        report = build_report(_files(payload), project_dir)
    except Exception:  # the hook must never get in the way of a write
        return 0
    if report:
        json.dump(
            {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": report}},
            sys.stdout,
        )
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
