"""The Stageshow kit, carried in engine/kits/stageshow, and the write that
drops it into a project with the system's look beside it.

Stageshow (github.com/benjitaylor/skills, MIT) builds product illustrations
from a React kit: a stage, window and phone frames, a cursor and the motion
parts. The copy here is its kit/ folder at the commit UPSTREAM.md names,
less the brand registry and BrandMark (other companies' marks, under their
own terms), with its few non-ASCII glyphs written as escapes. The kit needs
react, react-dom and lucide-react in the project.

run_kit() writes every kit file into `out`, and with a system (`source`)
the look `system export --to stageshow` writes, as stageshow-look.css. The
write is all or nothing. A file in `out` that differs from the kit's is
never replaced unless forced, and a forced write copies each file it
replaces into a backup folder inside `out` first.
"""
from __future__ import annotations

import shutil
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

KIT = Path(__file__).resolve().parent.parent / "kits" / "stageshow"
LABELS: Mapping[str, str] = {"out": "--out", "force": "--force", "from": "--from",
                             "format": "--format", "figma_mode": "--figma-mode",
                             "to": "--to", "build": "uxskill system build"}


def kit_files() -> Dict[str, str]:
    """Every file of the kit, by its path inside the kit."""
    return {p.relative_to(KIT).as_posix(): p.read_text(encoding="utf-8")
            for p in sorted(KIT.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def _backup(out: Path, names) -> str:
    """Copy each named file in `out` into a fresh backup folder; its path
    relative to `out`."""
    folder = Path(".uxskill") / "backup" / f"kit-{time.strftime('%Y%m%d-%H%M%S')}"
    for name in names:
        target = out / folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out / name, target)
    return folder.as_posix()


def run_kit(out: Any, *, source: Any = None, fmt: str = "auto", force: bool = False,
            second_modes: Optional[Mapping[str, str]] = None,
            labels: Mapping[str, str] = LABELS) -> Dict[str, Any]:
    """Write the kit into out, with the system's look when `source` names one.
    Returns status (written, unchanged or refused), the files written, left
    unchanged and in conflict, and the backup folder of a forced write."""
    from engine.foundations.emit import check_out_dir, conflict_message, plan_writes, write_files
    folder = check_out_dir(out, labels["out"])
    files = kit_files()
    if source is not None:
        from engine.io.read import read_sources
        from engine.io.stageshow_out import FILE_NAME, to_stageshow
        imported = read_sources(source, fmt, labels["from"], second_modes,
                                labels["figma_mode"], labels["format"])
        files[FILE_NAME] = to_stageshow(imported.tokens, labels=labels)
    plan = plan_writes(folder, files)
    if plan.conflicts and not force:
        return {"status": "refused", "written": [], "unchanged": list(plan.unchanged),
                "conflicts": list(plan.conflicts),
                "message": conflict_message(folder, plan, labels["force"], labels["out"])}
    backup = _backup(folder, plan.conflicts) if plan.conflicts else None
    done = write_files(folder, files, force=force)
    written = list(done.write) + list(done.conflicts)
    result: Dict[str, Any] = {"status": "written" if written else "unchanged",
                              "written": written, "unchanged": list(done.unchanged),
                              "conflicts": []}
    if backup:
        result["backup"] = backup
        result["replaced"] = list(plan.conflicts)
    return result
