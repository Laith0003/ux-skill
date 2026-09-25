#!/usr/bin/env python3
"""PostToolUse hook: lint a UI file right after Write, Edit or MultiEdit.

Claude Code pipes the tool call as JSON on stdin. When the written file is a
UI file (HTML, CSS, JSX, TSX, Vue, Svelte, Astro, Blade), this script runs the
anti-pattern linter on it and hands findings at medium severity and above back
to the session as additional context.

After an Edit or MultiEdit it lists only the findings on the lines the edit
wrote, and counts the rest, so an old finding is not repeated on every edit.
A Write lists every finding in the file.

It never blocks the write: the tool has already run, every error is swallowed,
and the exit code is always 0. A file over 1 MB is skipped with a one-line
note on stderr, so a huge generated file never stalls the session.

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
MAX_BYTES = 1_000_000
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
    try:
        from engine.linter.core import lint_text
    except Exception as exc:  # noqa: BLE001 - reported, never raised
        version = ".".join(str(x) for x in sys.version_info[:3])
        sys.stderr.write(
            f"ux-lint hook is off: the linter could not load under Python {version} ({exc}). "
            f"Run the hook with Python 3.10 or newer, or run `uxskill lint <file>` by hand.\n"
        )
        return None
    return lint_text


def _pages(path: Path, project_dir: Path) -> list:
    """The pages that load a stylesheet, so a parent focus ring in a separate
    stylesheet is read against their markup. Empty for any other file."""
    if not path.name.lower().endswith((".css", ".scss")):
        return []
    try:
        from engine.linter.core import stylesheet_pages
        root = project_dir.resolve()
        inside = root == path.resolve() or root in path.resolve().parents
        return [(str(p), p.read_text(encoding="utf-8", errors="ignore"))
                for p in stylesheet_pages(path, root=root if inside else None)]
    except Exception:  # noqa: BLE001 - the pages only waive; the lint still runs
        return []


def _files(payload: dict) -> list:
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return []
    value = tool_input.get("file_path")
    return [value] if isinstance(value, str) and value else []


def _written_strings(payload: dict):
    """The new text an Edit or MultiEdit wrote, or None for a whole-file write."""
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict) or payload.get("tool_name") not in ("Edit", "MultiEdit"):
        return None
    edits = tool_input.get("edits")
    if isinstance(edits, list):
        pieces = [e.get("new_string") for e in edits if isinstance(e, dict)]
    else:
        pieces = [tool_input.get("new_string")]
    pieces = [p for p in pieces if isinstance(p, str) and p.strip()]
    return pieces or None


def _touched_lines(text: str, pieces: list) -> set:
    """Line numbers covered by every occurrence of the written strings."""
    lines = set()
    for piece in pieces:
        start = text.find(piece)
        while start != -1:
            first = text.count("\n", 0, start) + 1
            lines.update(range(first, first + piece.count("\n") + 1))
            start = text.find(piece, start + 1)
    return lines


def _display(path: Path, project_dir: Path) -> str:
    try:
        return str(path.resolve().relative_to(project_dir.resolve()))
    except ValueError:
        return str(path)


def build_report(paths: list, project_dir: Path, written=None) -> str:
    lint_text = None
    blocks = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = project_dir / path
        if not path.name.lower().endswith(UI_SUFFIXES):
            continue
        shown = _display(path, project_dir)
        try:
            size = path.stat().st_size
            if size > MAX_BYTES:
                sys.stderr.write(
                    f"ux-lint skipped {shown}: {size / 1_000_000:.1f} MB is over the hook's 1 MB limit. "
                    f"Lint it by hand with `uxskill lint {shown}`.\n"
                )
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if lint_text is None:
            lint_text = _load_linter()
            if lint_text is None:
                return ""
        findings = [
            f for f in lint_text(shown, text, pages=_pages(path, project_dir))
            if REPORT_RANKS.get(f.severity, 0) >= 1
        ]
        elsewhere = 0
        touched = _touched_lines(text, written) if written else set()
        if touched:
            kept = [f for f in findings if f.line in touched]
            elsewhere = len(findings) - len(kept)
            findings = kept
        if not findings:
            continue
        findings.sort(key=lambda f: (-REPORT_RANKS[f.severity], f.line, f.column))
        where = "on the edited lines of" if touched else "in"
        lines = [f"ux-lint found {len(findings)} issue(s) at medium severity or above {where} {shown}:"]
        for f in findings[:MAX_LISTED]:
            lines.append(
                f"- {shown}:{f.line}:{f.column} [{f.severity}] {f.rule_id}: {f.rule_name}. Fix: {f.fix}"
            )
        if len(findings) > MAX_LISTED:
            lines.append(f"- {len(findings) - MAX_LISTED} more; run `uxskill lint {shown}` for the full list.")
        if elsewhere:
            lines.append(
                f"- {elsewhere} older finding(s) elsewhere in the file are not repeated; "
                f"run `uxskill lint {shown}` to see them."
            )
        lines.append(
            "To waive one finding on purpose, add a comment containing "
            "`ux-lint-disable <rule-id>` on that line, or `ux-lint-disable-next-line <rule-id>` above it."
        )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
        if _disabled(project_dir):
            return 0
        report = build_report(_files(payload), project_dir, _written_strings(payload))
        if report:
            json.dump(
                {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": report}},
                sys.stdout,
            )
            sys.stdout.write("\n")
    except Exception:  # the hook must never get in the way of a write
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
