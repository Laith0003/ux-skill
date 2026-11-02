"""The stop hook: a session with an open complaint about the page is held
once, with the reason, before it calls the work done.

It reads the last check and renders nothing, runs on the standard library
alone, lets a second stop through so it never traps a session, and has two
off switches."""
import json
import subprocess
import sys
import time
from pathlib import Path

from engine.complaints import LAST_FILE, _digest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "bin" / "ux-complaints-hook.py"
COVER = {"id": "cookie-card", "said": "the cookie banner covers the page",
         "probe": {"kind": "rule-clear", "rule": "first-screen-covered"}}


def _run(project: Path, event=None, env=None, raw=None):
    # -S: no site-packages, so the hook proves it needs nothing installed.
    run = subprocess.run([sys.executable, "-S", str(HOOK)],
                         input=raw if raw is not None else json.dumps(event or {}),
                         capture_output=True, text=True, timeout=30,
                         env={"CLAUDE_PROJECT_DIR": str(project), **(env or {})})
    assert run.returncode == 0, run.stderr
    return json.loads(run.stdout) if run.stdout.strip() else {}


def _project(tmp_path: Path, last=None, page_text="<h1>x</h1>") -> Path:
    ux = tmp_path / ".ux"
    ux.mkdir()
    complaints = ux / "complaints.json"
    complaints.write_text(json.dumps({"complaints": [COVER]}), encoding="utf-8")
    page = tmp_path / "index.html"
    page.write_text(page_text, encoding="utf-8")
    if last is not None:
        record = {"page": "index.html", "page_path": str(page.resolve()),
                  "page_digest": _digest(page.read_bytes()),
                  "complaints_digest": _digest(complaints.read_bytes()),
                  "checked_at": time.time() + 1, **last}
        (ux / LAST_FILE).write_text(json.dumps(record), encoding="utf-8")
    return tmp_path


def test_a_project_without_complaints_stops_freely(tmp_path):
    assert _run(tmp_path) == {}


def test_complaints_never_checked_hold_the_stop(tmp_path):
    answer = _run(_project(tmp_path))
    assert answer["decision"] == "block"
    assert "never checked" in answer["reason"] and "uxskill complaints check" in answer["reason"]


def test_an_open_complaint_holds_the_stop_and_names_it(tmp_path):
    answer = _run(_project(tmp_path, last={"open": ["cookie-card"]}))
    assert answer["decision"] == "block" and "cookie-card" in answer["reason"]


def test_a_page_changed_after_a_passing_check_holds_the_stop(tmp_path):
    project = _project(tmp_path, last={"open": []})
    assert _run(project) == {}
    (project / "index.html").write_text("<h1>edited</h1>", encoding="utf-8")
    assert "changed since the last check" in _run(project)["reason"]


def test_a_second_stop_goes_through_so_the_session_is_never_trapped(tmp_path):
    assert _run(_project(tmp_path), {"stop_hook_active": True}) == {}


def test_both_off_switches(tmp_path):
    project = _project(tmp_path)
    assert _run(project, env={"UXSKILL_COMPLAINTS_GATE": "0"}) == {}
    (project / ".ux" / "complaints-gate.off").write_text("", encoding="utf-8")
    assert _run(project) == {}


def test_bad_input_never_breaks_the_session(tmp_path):
    assert _run(_project(tmp_path), raw="not json") == {}
    (tmp_path / ".ux" / "complaints.json").write_text("{", encoding="utf-8")
    assert "not readable JSON" in _run(tmp_path)["reason"]


def test_the_plugin_registers_it_on_stop():
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    commands = [h["command"] for entry in manifest["hooks"]["Stop"] for h in entry["hooks"]]
    assert any("bin/ux-complaints-hook.py" in c for c in commands)
