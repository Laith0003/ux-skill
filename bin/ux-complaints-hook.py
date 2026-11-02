#!/usr/bin/env python3
"""Stop hook: hold the session while a complaint about the page is open.

When the project keeps complaints in .ux/complaints.json, the work is not
done until `uxskill complaints check --page <page>` has measured the page
as it is now and found every complaint fixed. This hook reads the last
check (.ux/complaints-last.json) and, when it is missing, ran on other
complaints, left a complaint open, or is older than the page or any page
source in the project, blocks the stop
once with the reason, so the session runs the check or fixes the page
before it calls the work done. It renders nothing; it walks the project's
page sources once, up to 20000 files.

It blocks once per stop: when Claude Code reports the session is already
continuing because of a stop hook, it lets the stop through, so a page that
cannot be fixed never traps the session. Every error is swallowed and the
exit code is always 0.

Turn it off
-----------
* ``UXSKILL_COMPLAINTS_GATE=0`` in the environment, or
* an empty file at ``.ux/complaints-gate.off`` in the project root.

Pure Python standard library: engine/__init__.py and the foundations
package are not run, so no third-party package has to be installed.
"""
from __future__ import annotations

import json
import os
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFF_VALUES = {"0", "off", "false", "no"}


def _gate():
    for name, folder in (("engine", ROOT / "engine"),
                         ("engine.foundations", ROOT / "engine" / "foundations")):
        if name not in sys.modules:
            pkg = types.ModuleType(name)
            pkg.__path__ = [str(folder)]  # type: ignore[attr-defined]
            sys.modules[name] = pkg
    from engine.complaints import gate
    return gate


def decide(event: dict, project_dir: Path) -> dict:
    """The hook's answer: {} to let the stop through, or a block with the
    reason."""
    if event.get("stop_hook_active"):
        return {}
    if os.environ.get("UXSKILL_COMPLAINTS_GATE", "").strip().lower() in OFF_VALUES:
        return {}
    if (project_dir / ".ux" / "complaints-gate.off").exists():
        return {}
    reason = _gate()(project_dir)
    if not reason:
        return {}
    return {"decision": "block",
            "reason": f"ux-skill: {reason}. A complaint closes only when the check measures "
                      "it fixed."}


def main() -> int:
    try:
        event = json.loads(sys.stdin.read() or "{}")
        project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")
        answer = decide(event if isinstance(event, dict) else {}, project)
        if answer:
            print(json.dumps(answer))
    except Exception:  # noqa: BLE001 - a hook never breaks the session
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
