"""Ablation hook: run the engine with one guidance pack switched off.

PLAN-5.0 Phase 1 asks for the engine with and without each guidance pack on
the fixed briefs, so the report shows which guidance changes the output and
which only adds weight. The output has two halves:

1. What the engine writes for an agent to read (the rule pack built with
   ``ux system build --rule-pack``). This half is deterministic and runs
   here: each pack in engine/rulepack/guidance/ is switched off by keeping
   its Roles and Checks lines (the build needs them) and replacing every
   prose section with one line, then the rule pack is built again and
   compared with the full build, file by file.
2. What an agent builds after reading it (pages generated from the ten
   briefs with and without the pack). That half needs an AI coding tool
   run per brief and per pack, and is a stub: ``generation_plan`` lists the
   runs, and nothing here calls a model.

Run ``python -m bench ablate --pack motion`` for one pack, or without
``--pack`` for all of them.
"""

from __future__ import annotations

import difflib
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

OFF_LINE = "Switched off for an ablation run."
KEEP = ("Roles", "Checks")
BRAND = "#1A4D2E"


def switch_off(text: str) -> str:
    """The guidance text with every section but Roles and Checks reduced to
    one line, headings kept so the reader still accepts the file."""
    out: List[str] = []
    keep = True
    for line in text.splitlines():
        m = re.match(r"^(?:\{(?:arabic|latin)\} )?## (.+?)\s*$", line)
        if m:
            heading = m.group(1)
            keep = heading in KEEP
            out.append(line)
            if not keep:
                out.append("")
                out.append(OFF_LINE)
                out.append("")
            continue
        if keep or line.startswith("# "):
            out.append(line)
    return "\n".join(out) + "\n"


def packs() -> List[str]:
    from engine.rulepack.guidance import GUIDANCE_DIR

    return sorted(p.stem for p in GUIDANCE_DIR.glob("*.md"))


def _tokens(arabic: bool) -> Any:
    from engine.foundations.build import build_system
    from engine.foundations.emit import choose_axes

    axes, _ = choose_axes(None, None)
    return build_system(axes, BRAND, arabic=arabic).tokens


def run(pack: Optional[str] = None, arabic: bool = True) -> List[Dict[str, Any]]:
    """For each pack (or the one named), the rule pack files that change when
    it is switched off, and the lines that leave the pack."""
    from engine.rulepack.generate import RulePackError, build_rule_pack
    from engine.rulepack.guidance import GUIDANCE_DIR

    names = packs()
    if pack is not None and pack not in names:
        raise ValueError(f"--pack {pack!r} is not a guidance pack; use one of {', '.join(names)}")
    ts = _tokens(arabic)
    full = build_rule_pack(ts)
    rows = []
    for name in [pack] if pack else names:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "guidance"
            shutil.copytree(GUIDANCE_DIR, folder)
            src = folder / f"{name}.md"
            src.write_text(switch_off(src.read_text(encoding="utf-8")), encoding="utf-8")
            try:
                ablated = build_rule_pack(ts, guidance_dir=folder)
                error = ""
            except RulePackError as exc:
                ablated, error = {}, "; ".join(exc.problems)[:300]
        changed, removed = [], 0
        for path in sorted(set(full) | set(ablated)):
            a, b = full.get(path, ""), ablated.get(path, "")
            if a != b:
                changed.append(path)
                removed += sum(
                    1 for d in difflib.ndiff(a.splitlines(), b.splitlines()) if d.startswith("- ")
                )
        rows.append(
            {
                "pack": name,
                "files_changed": changed,
                "lines_removed": removed,
                "pack_lines": sum(len(v.splitlines()) for v in full.values()),
                "build_error": error,
            }
        )
    return rows


def generation_plan(briefs: Sequence[str], pack_names: Sequence[str]) -> List[Dict[str, str]]:
    """The generation runs the second half needs: every brief with all
    guidance, and every brief with each pack switched off. Not executed."""
    plan = [{"brief": b, "condition": "all guidance"} for b in briefs]
    plan += [{"brief": b, "condition": f"without {p}"} for b in briefs for p in pack_names]
    return plan


def table(rows: List[Dict[str, Any]]) -> str:
    out = [
        "| Pack switched off | Rule pack files changed | Lines removed | Build |",
        "|---|---|---|---|",
    ]
    for r in rows:
        build = "fails: " + r["build_error"] if r["build_error"] else "passes"
        out.append(f"| {r['pack']} | {len(r['files_changed'])} | {r['lines_removed']} | {build} |")
    return "\n".join(out)
