"""The PostToolUse hook that lints UI files on every write."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "bin" / "ux-lint-hook.py"
CORPUS = Path(__file__).resolve().parent / "lint_corpus"

# The hook must finish in 500 ms on a 2,000-line file. CI runners are slower
# and noisier than a laptop, so the test allows three times that.
BUDGET_SECONDS = 0.5
CI_MARGIN = 3.0


def run_hook(payload, env_extra=None, cwd=None):
    env = {k: v for k, v in os.environ.items() if k not in ("UXSKILL_LINT_ON_WRITE", "CLAUDE_PROJECT_DIR")}
    env.update(env_extra or {})
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        [sys.executable, str(HOOK)], input=raw, capture_output=True, text=True,
        env=env, cwd=cwd, timeout=60,
    )


def payload_for(path: Path, tool="Write", cwd: Path | None = None):
    return {
        "session_id": "test",
        "hook_event_name": "PostToolUse",
        "tool_name": tool,
        "tool_input": {"file_path": str(path)},
        "cwd": str(cwd or path.parent),
    }


def test_plugin_declares_the_hook():
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    entries = manifest["hooks"]["PostToolUse"]
    matchers = " ".join(e["matcher"] for e in entries)
    for tool in ("Write", "Edit", "MultiEdit"):
        assert tool in matchers
    commands = [h["command"] for e in entries for h in e["hooks"]]
    assert any("bin/ux-lint-hook.py" in c and "${CLAUDE_PLUGIN_ROOT}" in c for c in commands)
    assert HOOK.exists()


@pytest.mark.parametrize("tool", ["Write", "Edit", "MultiEdit"])
def test_hook_reports_findings_with_location_and_fix(tmp_path, tool):
    f = tmp_path / "Hero.tsx"
    f.write_text(
        'export const Hero = () => (\n'
        '  <section className="bg-gradient-to-r from-violet-500 to-blue-500">\n'
        '    <div style={{ zIndex: 9999 }}>Launch</div>\n'
        '  </section>\n'
        ');\n',
        encoding="utf-8",
    )
    result = run_hook(payload_for(f, tool))
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    context = out["hookSpecificOutput"]["additionalContext"]
    assert "Hero.tsx:2:" in context and "purple-to-blue-gradient" in context
    assert "Hero.tsx:3:" in context and "arbitrary-z-index-9999" in context
    assert context.count("Fix: ") >= 2


def test_hook_reports_medium_and_above_only(tmp_path):
    f = tmp_path / "a.css"
    # border-radius-2xl-default is low; transition-property-all is medium
    f.write_text(".a { border-radius: 24px; }\n.b { transition: all 150ms; }\n", encoding="utf-8")
    context = json.loads(run_hook(payload_for(f)).stdout)["hookSpecificOutput"]["additionalContext"]
    assert "transition-property-all" in context
    assert "border-radius-2xl-default" not in context


def test_hook_is_silent_on_clean_files():
    f = CORPUS / "clean" / "react" / "Hero.tsx"
    result = run_hook(payload_for(f))
    assert result.returncode == 0
    assert result.stdout.strip() == ""


@pytest.mark.parametrize("name", ["notes.md", "script.py", "data.json", "util.ts"])
def test_hook_ignores_non_ui_files(tmp_path, name):
    f = tmp_path / name
    f.write_text("transition: all; z-index: 9999; Lorem ipsum dolor", encoding="utf-8")
    result = run_hook(payload_for(f))
    assert result.returncode == 0 and result.stdout.strip() == ""


def test_hook_resolves_relative_paths_against_cwd(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.css").write_text(".a { z-index: 9999; }", encoding="utf-8")
    payload = {"tool_name": "Write", "tool_input": {"file_path": "src/a.css"}, "cwd": str(tmp_path)}
    context = json.loads(run_hook(payload).stdout)["hookSpecificOutput"]["additionalContext"]
    assert "src/a.css:1:" in context


def test_hook_can_be_disabled_by_env(tmp_path):
    f = tmp_path / "a.css"
    f.write_text(".a { z-index: 9999; }", encoding="utf-8")
    for value in ("0", "off", "false"):
        result = run_hook(payload_for(f), env_extra={"UXSKILL_LINT_ON_WRITE": value})
        assert result.returncode == 0 and result.stdout.strip() == ""


def test_hook_can_be_disabled_by_project_file(tmp_path):
    f = tmp_path / "a.css"
    f.write_text(".a { z-index: 9999; }", encoding="utf-8")
    (tmp_path / ".ux").mkdir()
    (tmp_path / ".ux" / "lint-on-write.off").write_text("", encoding="utf-8")
    result = run_hook(payload_for(f, cwd=tmp_path))
    assert result.returncode == 0 and result.stdout.strip() == ""


@pytest.mark.parametrize("payload", [
    "not json",
    "[]",
    json.dumps({"tool_name": "Write"}),
    json.dumps({"tool_name": "Write", "tool_input": {"file_path": "/no/such/file.tsx"}}),
])
def test_hook_never_fails(payload):
    result = run_hook(payload)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def _two_thousand_line_file(tmp_path: Path) -> Path:
    sources = sorted((CORPUS / "clean" / "react").glob("*.tsx")) + sorted((CORPUS / "dirty").glob("*.tsx"))
    chunk = "\n".join(p.read_text(encoding="utf-8") for p in sources)
    lines = []
    while len(lines) < 2000:
        lines.extend(chunk.splitlines())
    f = tmp_path / "Big.tsx"
    f.write_text("\n".join(lines[:2000]) + "\n", encoding="utf-8")
    return f


def test_hook_is_fast_on_a_2000_line_file(tmp_path):
    f = _two_thousand_line_file(tmp_path)
    assert len(f.read_text(encoding="utf-8").splitlines()) == 2000
    timings = []
    for _ in range(3):
        start = time.perf_counter()
        result = run_hook(payload_for(f))
        timings.append(time.perf_counter() - start)
        assert result.returncode == 0
    assert "ux-lint found" in result.stdout
    best = min(timings)
    assert best < BUDGET_SECONDS * CI_MARGIN, (
        f"hook took {best * 1000:.0f} ms on 2,000 lines; budget is {BUDGET_SECONDS * 1000:.0f} ms "
        f"(test allows x{CI_MARGIN} for CI)"
    )
