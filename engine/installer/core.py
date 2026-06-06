"""Multi-IDE installer.

Detects the current IDE / AI coding environment and writes the right artifacts
so the user can invoke ux-skill from inside that environment. Falls back to a
generic install if no IDE is detected.

Supported targets (17):

* claude-code          -- writes/symlinks the plugin folder
* cursor               -- writes ``.cursorrules`` + helper config
* windsurf             -- writes ``.windsurfrules``
* copilot              -- writes ``.github/copilot-instructions.md``
* gemini-cli           -- writes ``GEMINI.md``
* codex                -- writes ``AGENTS.md``
* kiro                 -- writes ``.kiro/instructions.md``
* cline                -- writes ``.cline/instructions.md``
* continue             -- writes ``.continue/config.json``
* aider                -- writes ``.aider.conf.yml``
* zed                  -- writes ``.zed/ai-instructions.md``
* jetbrains-ai         -- writes ``.jetbrains-ai/instructions.md``
* pieces               -- writes ``.pieces/instructions.md``
* tabby                -- writes ``.tabby/instructions.md``
* tabnine              -- writes ``.tabnine/instructions.md``
* codewhisperer        -- writes ``.aws-codewhisperer/instructions.md``
* roo-cline            -- writes ``.roo/instructions.md``

Public surface
--------------
``detect_ides(root) -> list[str]``
``install(target, root, dry_run) -> InstallReport``
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


SUPPORTED = [
    "claude-code", "cursor", "windsurf", "copilot", "gemini-cli", "codex",
    "kiro", "cline", "continue", "aider", "zed", "jetbrains-ai", "pieces",
    "tabby", "tabnine", "codewhisperer", "roo-cline",
]


DETECT_SIGNATURES: Dict[str, List[str]] = {
    "claude-code":   [".claude", "CLAUDE.md"],
    "cursor":        [".cursor", ".cursorrules"],
    "windsurf":      [".windsurf", ".windsurfrules"],
    "copilot":       [".github/copilot-instructions.md", ".vscode"],
    "gemini-cli":    ["GEMINI.md"],
    "codex":         ["AGENTS.md"],
    "kiro":          [".kiro"],
    "cline":         [".cline"],
    "continue":      [".continue"],
    "aider":         [".aider.conf.yml", ".aiderignore"],
    "zed":           [".zed"],
    "jetbrains-ai":  [".jetbrains-ai", ".idea"],
    "pieces":        [".pieces"],
    "tabby":         [".tabby"],
    "tabnine":       [".tabnine"],
    "codewhisperer": [".aws-codewhisperer"],
    "roo-cline":     [".roo"],
}


PROMPT_HEADER = (
    "# ux-skill v2 — design intelligence for AI coding\n\n"
    "Before generating ANY frontend code in this project, do the following:\n\n"
    "1. Run the 10-field discovery (`ux discover`) and wait for all answers.\n"
    "2. If the user gives a URL to their OWN site/brand, capture the real brand from the\n"
    "   RENDERED page (computed-style colors, the actual logo + pixel-sample, loaded fonts),\n"
    "   run `ux brand --signals-file <f>`, then pass `--brand-file` and `--brand-url` to\n"
    "   recommend. A raw fetch of a JS-rendered site is an empty shell; the engine never fetches.\n"
    "3. Run `ux recommend` to get the recommended style / palette / type / motion / components.\n"
    "   If `warnings` flags a brand URL given but not captured, stop and capture first.\n"
    "4. Generate code using ONLY the recommended tokens. Treat the anti-pattern\n"
    "   rules in `data/anti-patterns.json` as hard constraints.\n"
    "5. Run `ux lint` after generation. Fix all `high`+ findings before declaring done.\n\n"
    "See https://uxskill.laithjunaidy.com for full docs.\n"
)


@dataclass
class InstallReport:
    target: str
    root: str
    files_written: List[str] = field(default_factory=list)
    files_skipped: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    dry_run: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def detect_ides(root: Path) -> List[str]:
    """Return the list of IDEs whose signature files exist under ``root``."""
    detected: List[str] = []
    for ide, signatures in DETECT_SIGNATURES.items():
        if any((root / sig).exists() for sig in signatures):
            detected.append(ide)
    return detected


# ---------------------------------------------------------------------------
# Per-IDE writers
# ---------------------------------------------------------------------------

def _write(root: Path, rel: str, content: str, dry_run: bool, report: InstallReport) -> None:
    path = root / rel
    if dry_run:
        report.files_skipped.append(f"{rel} (dry-run)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    report.files_written.append(rel)


def _install_claude_code(root: Path, dry_run: bool, report: InstallReport) -> None:
    """Claude Code uses the existing plugin folder structure — no extra writes
    if we're inside our own repo."""
    plugin_manifest = root / ".claude-plugin" / "plugin.json"
    if plugin_manifest.exists():
        report.notes.append("Claude Code plugin already present (.claude-plugin/plugin.json)")
        return
    _write(root, ".claude-plugin/plugin.json", json.dumps({
        "name": "ux", "version": "2.0.0",
        "description": "ux-skill — design intelligence engine"
    }, indent=2), dry_run, report)


def _install_cursor(root: Path, dry_run: bool, report: InstallReport) -> None:
    _write(root, ".cursorrules", PROMPT_HEADER, dry_run, report)


def _install_windsurf(root: Path, dry_run: bool, report: InstallReport) -> None:
    _write(root, ".windsurfrules", PROMPT_HEADER, dry_run, report)


def _install_copilot(root: Path, dry_run: bool, report: InstallReport) -> None:
    _write(root, ".github/copilot-instructions.md", PROMPT_HEADER, dry_run, report)


def _install_markdown_root(root: Path, filename: str, dry_run: bool, report: InstallReport) -> None:
    _write(root, filename, PROMPT_HEADER, dry_run, report)


def _install_dotdir(root: Path, dirname: str, dry_run: bool, report: InstallReport) -> None:
    _write(root, f"{dirname}/instructions.md", PROMPT_HEADER, dry_run, report)


def _install_aider(root: Path, dry_run: bool, report: InstallReport) -> None:
    yml = (
        "# ux-skill v2 install\n"
        "model: sonnet\n"
        "read:\n"
        "  - data/anti-patterns.json\n"
        "  - data/styles.json\n"
        "  - data/palettes.json\n"
        "  - data/type-pairs.json\n"
    )
    _write(root, ".aider.conf.yml", yml, dry_run, report)
    _write(root, "AIDER.md", PROMPT_HEADER, dry_run, report)


def _install_continue(root: Path, dry_run: bool, report: InstallReport) -> None:
    cfg = {
        "name": "ux-skill",
        "version": "2.0.0",
        "systemMessage": PROMPT_HEADER,
    }
    _write(root, ".continue/config.json", json.dumps(cfg, indent=2), dry_run, report)


WRITERS = {
    "claude-code":   _install_claude_code,
    "cursor":        _install_cursor,
    "windsurf":      _install_windsurf,
    "copilot":       _install_copilot,
    "gemini-cli":    lambda r, d, rep: _install_markdown_root(r, "GEMINI.md", d, rep),
    "codex":         lambda r, d, rep: _install_markdown_root(r, "AGENTS.md", d, rep),
    "kiro":          lambda r, d, rep: _install_dotdir(r, ".kiro", d, rep),
    "cline":         lambda r, d, rep: _install_dotdir(r, ".cline", d, rep),
    "continue":      _install_continue,
    "aider":         _install_aider,
    "zed":           lambda r, d, rep: _install_dotdir(r, ".zed", d, rep),
    "jetbrains-ai":  lambda r, d, rep: _install_dotdir(r, ".jetbrains-ai", d, rep),
    "pieces":        lambda r, d, rep: _install_dotdir(r, ".pieces", d, rep),
    "tabby":         lambda r, d, rep: _install_dotdir(r, ".tabby", d, rep),
    "tabnine":       lambda r, d, rep: _install_dotdir(r, ".tabnine", d, rep),
    "codewhisperer": lambda r, d, rep: _install_dotdir(r, ".aws-codewhisperer", d, rep),
    "roo-cline":     lambda r, d, rep: _install_dotdir(r, ".roo", d, rep),
}


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def install(target: str, root: Optional[str] = None, dry_run: bool = False) -> InstallReport:
    if target not in WRITERS:
        raise ValueError(f"Unknown install target '{target}'. Supported: {', '.join(SUPPORTED)}")
    root_path = Path(root or ".").resolve()
    report = InstallReport(target=target, root=str(root_path), dry_run=dry_run)
    WRITERS[target](root_path, dry_run, report)
    return report
