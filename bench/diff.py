"""New and lost findings per rule between two engine versions on the corpus.

    python bench/diff.py                      # v4.0.0 against this checkout
    python bench/diff.py --base v4.0.0 --head HEAD --static-only

Each side runs ``python -m bench run`` with that version's engine. A tag or
commit is checked out into a temporary git worktree, which is removed after
the run. The bench code and the frozen pages always come from this checkout,
so only the engine differs. Findings are matched by key (page, pass, rule,
file, line, excerpt or element), which pages being frozen keeps stable.
This is the corpus diff of eval.md A7 (as Ruff, mypy_primer and Clippy
lintcheck do for their rules).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


class DiffError(RuntimeError):
    """A side could not be run; the message names the ref and the fix."""


def _git(*args: str) -> str:
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise DiffError(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout.strip()


# Run in a fresh, isolated interpreter (-I: no PYTHONPATH, no user site, no
# script directory on the path) from a neutral working directory, with the
# engine's root first on sys.path and this checkout's root second, so the old
# engine and this checkout's bench code are the ones imported. The child checks
# that engine came from where it should and fails loudly otherwise.
_BOOT = """
import sys
from pathlib import Path
engine_root, bench_root, argv = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path[:0] = [engine_root, bench_root]
import engine, bench
got = Path(engine.__file__).resolve().parent.parent
if got != Path(engine_root).resolve():
    sys.exit(f"engine imported from {got}, expected {engine_root}")
if Path(bench.__file__).resolve().parent.parent != Path(bench_root).resolve():
    sys.exit(f"bench imported from {bench.__file__}, expected {bench_root}")
from bench.__main__ import main
sys.exit(main(argv))
"""


def _run_bench(engine_root: Path, argv: Sequence[str]) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="ux-bench-cwd-") as cwd:
        return subprocess.run(
            [sys.executable, "-I", "-c", _BOOT, str(engine_root), str(ROOT), *argv],
            cwd=cwd, capture_output=True, text=True,
        )


def run_side(
    ref: Optional[str], out: Path, static_only: bool, only: Optional[Sequence[str]] = None
) -> Dict[str, Any]:
    """Run this checkout's bench code with the engine at ``ref`` (None: this checkout)."""
    argv = ["run", "--out", str(out)]
    if static_only:
        argv.append("--static-only")
    if only:
        argv += ["--only", *only]
    if ref is None:
        proc = _run_bench(ROOT, argv)
    else:
        _git("rev-parse", "--verify", f"{ref}^{{commit}}")
        with tempfile.TemporaryDirectory(prefix="ux-bench-") as tmp:
            wt = Path(tmp) / "engine"
            _git("worktree", "add", "--detach", str(wt), ref)
            try:
                proc = _run_bench(wt, argv)
            finally:
                _git("worktree", "remove", "--force", str(wt))
    if proc.returncode not in (0, 1) or not out.exists():
        raise DiffError(
            f"bench run with engine {ref or 'checkout'} failed "
            f"(exit {proc.returncode}): {proc.stderr.strip()[-600:]}; check that {ref or 'HEAD'} "
            "has an engine/ package and that Playwright is installed for the render pass"
        )
    return json.loads(out.read_text(encoding="utf-8"))


def _keys(result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {f["key"]: f for page in result["pages"].values() for f in page["findings"]}


def compare(base: Dict[str, Any], head: Dict[str, Any]) -> Dict[str, Any]:
    """Per rule: findings in head only (new) and in base only (lost)."""
    kb, kh = _keys(base), _keys(head)
    new = Counter(kh[k]["rule"] for k in kh.keys() - kb.keys())
    lost = Counter(kb[k]["rule"] for k in kb.keys() - kh.keys())
    kept = Counter(kh[k]["rule"] for k in kh.keys() & kb.keys())
    rules = sorted(set(new) | set(lost))
    return {
        "base": base["engine"],
        "head": head["engine"],
        "render": [base.get("render"), head.get("render")],
        "totals": {
            "base": len(kb),
            "head": len(kh),
            "new": sum(new.values()),
            "lost": sum(lost.values()),
        },
        "rules": [{"rule": r, "new": new[r], "lost": lost[r], "kept": kept[r]} for r in rules],
        "new_keys": sorted(kh.keys() - kb.keys()),
        "lost_keys": sorted(kb.keys() - kh.keys()),
    }


def markdown(d: Dict[str, Any], base_ref: str, head_ref: str) -> str:
    t = d["totals"]
    out = [
        f"Engine {base_ref} ({d['base'].get('git', '')}) against {head_ref} "
        f"({d['head'].get('git', '')}): {t['base']} findings before, {t['head']} after, "
        f"{t['new']} new, {t['lost']} lost.",
        "",
        "| Rule | New | Lost | Kept |",
        "|---|---|---|---|",
    ]
    for r in d["rules"]:
        out.append(f"| {r['rule']} | {r['new']} | {r['lost']} | {r['kept']} |")
    return "\n".join(out) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", default="v4.0.0", help="tag or commit for the old engine")
    ap.add_argument(
        "--head", default=None, help="tag or commit for the new engine (default: this checkout)"
    )
    ap.add_argument("--static-only", action="store_true", help="skip the render pass")
    ap.add_argument("--only", nargs="*", help="page ids to compare (default: all)")
    ap.add_argument(
        "--out", default=str(HERE / "out" / "diff.json"), help="where to write the diff json"
    )
    args = ap.parse_args(argv)
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        base = run_side(args.base, out.with_name("diff-base.json"), args.static_only, args.only)
        head = run_side(args.head, out.with_name("diff-head.json"), args.static_only, args.only)
    except DiffError as exc:
        print(f"diff failed: {exc}", file=sys.stderr)
        return 2
    d = compare(base, head)
    d["refs"] = {"base": args.base, "head": args.head or "checkout"}
    out.write_text(json.dumps(d, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
    print(markdown(d, args.base, args.head or "checkout"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
