"""The Stageshow kit, carried in engine/kits/stageshow, and the write that
drops it into a project with the system's look beside it.

Stageshow (github.com/benjitaylor/skills, MIT) builds product illustrations
from a React kit: a stage, window and phone frames, a cursor and the motion
parts. The copy here is its kit/ folder at the commit UPSTREAM.md names,
less the brand registry and BrandMark (other companies' marks, under their
own terms), with its few non-ASCII glyphs written as escapes. The kit needs
react, react-dom and lucide-react in the project.

run_kit() writes every kit file into `out`, and with a system (`source`)
the look `system export --to stageshow` writes, as stageshow-look.css,
with the same note of what its import left out. It plans once and writes
once, all or nothing. A file in `out` that differs from the kit's is never
replaced unless forced; a forced write puts a copy of each file it
replaces into .uxskill/backup/<digest>/ in the same batch, the folder named
after what it holds so a later backup never lands on an earlier one, and a
file that changes between the plan and the write stops the whole write.
Files an older kit left in `out` that this one no longer ships are listed,
never removed. With look_only, only the look is written, replacing the
one there after the same backup, so a system that changed reaches the
illustrations without touching kit files the project has edited.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

KIT = Path(__file__).resolve().parent.parent / "kits" / "stageshow"
# The kit's own file types: anything else in the folder (an editor's swap
# file, a .DS_Store) is never carried into a project.
SUFFIXES = (".ts", ".tsx", ".css", ".md")
NAMES = ("LICENSE",)
LOOK_FILE = "stageshow-look.css"
LABELS: Mapping[str, str] = {"out": "--out", "force": "--force", "from": "--from",
                             "format": "--format", "figma_mode": "--figma-mode",
                             "to": "kit", "build": "uxskill system build",
                             "look_only": "--look-only"}


def kit_files() -> Dict[str, str]:
    """Every file of the kit, by its path inside the kit."""
    return {p.relative_to(KIT).as_posix(): p.read_text(encoding="utf-8")
            for p in sorted(KIT.rglob("*"))
            if p.is_file() and (p.suffix in SUFFIXES or p.name in NAMES)}


def _backups(folder: Path, names) -> Tuple[str, Dict[str, bytes]]:
    """A backup folder named after the digest of the named files, and each
    file's current bytes placed under it."""
    from engine.foundations.errors import InputError
    held: Dict[str, bytes] = {}
    for name in names:
        try:
            held[name] = (folder / name).read_bytes()
        except OSError as exc:
            raise InputError(f"{folder / name} cannot be read to back it up "
                             f"({exc.strerror or exc}), so nothing was written; make it "
                             "readable or move it out of the folder") from None
    digest = hashlib.sha256(b"".join(n.encode() + b"\0" + held[n] for n in sorted(held)))
    base = f".uxskill/backup/kit-{digest.hexdigest()[:12]}"
    return base, {f"{base}/{name}": data for name, data in held.items()}


def _left_over(folder: Path, files: Mapping[str, Any]) -> List[str]:
    """Kit-type files in a folder an earlier kit was written into (it holds
    UPSTREAM.md) that this kit does not ship."""
    if not (folder / "UPSTREAM.md").is_file():
        return []
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*")
                  if p.is_file() and p.suffix in SUFFIXES and ".uxskill" not in p.parts
                  and p.relative_to(folder).as_posix() not in files)


def run_kit(out: Any, *, source: Any = None, fmt: str = "auto", force: bool = False,
            look_only: bool = False, second_modes: Optional[Mapping[str, str]] = None,
            labels: Mapping[str, str] = LABELS) -> Dict[str, Any]:
    """Write the kit into out, with the system's look when `source` names one.
    Returns status (written, unchanged or refused), the files written, left
    unchanged and in conflict, the backup folder of a forced write, and the
    files an older kit left that this one does not ship."""
    from engine.foundations.emit import check_out_dir, conflict_message, plan_writes, write_files
    from engine.foundations.errors import InputError
    if look_only and source is None:
        raise InputError(f"{labels['look_only']} writes the look of the {labels['from']} system, "
                         f"and no {labels['from']} was given; pass {labels['from']} "
                         "design-system/tokens.json with it")
    if source is None:
        for given, label in ((fmt != "auto", "format"), (bool(second_modes), "figma_mode")):
            if given:
                raise InputError(f"{labels[label]} reads the {labels['from']} system, and no "
                                 f"{labels['from']} was given; pass {labels['from']} with it, "
                                 "or leave it out to write the kit alone")
    folder = check_out_dir(out, labels["out"])
    files: Dict[str, Any] = {} if look_only else dict(kit_files())
    result: Dict[str, Any] = {}
    if source is not None:
        from engine.io.commands import _header
        from engine.io.read import read_sources
        from engine.io.stageshow_out import to_stageshow
        imported = read_sources(source, fmt, labels["from"], second_modes,
                                labels["figma_mode"], labels["format"])
        files[LOOK_FILE] = to_stageshow(imported.tokens, labels=labels, header=_header(imported))
        result["not_read"] = len(imported.report.not_read)
    left = [] if look_only else _left_over(folder, files)
    plan = plan_writes(folder, files)
    if plan.conflicts and not (force or look_only):
        return {"status": "refused", "written": [], "unchanged": list(plan.unchanged),
                "conflicts": list(plan.conflicts),
                "message": conflict_message(folder, plan, labels["force"], labels["out"]),
                **result}
    base, backups = _backups(folder, plan.conflicts) if plan.conflicts else ("", {})
    done = write_files(folder, {**files, **backups}, force=True, replace=plan.conflicts)
    if done.conflicts:
        return {"status": "refused", "written": [], "unchanged": [],
                "conflicts": list(done.conflicts),
                "message": (f"{', '.join(str(folder / n) for n in done.conflicts)} changed while "
                            "the kit was being written, so nothing was written; run the "
                            "command again"), **result}
    written = [n for n in done.write if n not in backups]
    result.update({"status": "written" if written else "unchanged", "written": written,
                   "unchanged": list(done.unchanged), "conflicts": []})
    if backups:
        result["backup"] = base
        result["replaced"] = list(plan.conflicts)
    if left:
        result["not_in_kit"] = left
        result["note"] = ("these files are in the kit folder but not in this kit, so an older "
                          "kit may have written them; remove each one that nothing imports")
    return result
