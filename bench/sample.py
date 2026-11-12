"""Draw 50 labelled findings for a person to confirm.

    python bench/sample.py               # 50 findings, seed 5
    python bench/sample.py --n 50 --seed 5

The draw is stratified so every rule with a labelled finding appears before
any rule appears twice (rules taken in order of how often they fire), then
filled at random. It writes labels/sample-50.md, a table to read beside the
pages, and labels/sample-50.jsonl with an empty ``human`` field per row. The
person fills ``human`` with TP, FP or cantTell; until then every label in
the bench stays model-made. Same labels and seed give the same sample.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from bench import BENCH, OUT  # noqa: E402
from bench import core, label  # noqa: E402
from bench import manifest as mf  # noqa: E402


def draw(labels: Dict[str, Dict[str, Any]], n: int = 50, seed: int = 5) -> List[Dict[str, Any]]:
    rows = sorted((r for r in labels.values() if r.get("final")), key=lambda r: r["key"])
    if not rows:
        raise ValueError("no labelled findings; run python -m bench label first")
    rng = random.Random(seed)
    by_rule: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_rule[r["rule"]].append(r)
    freq = Counter(r["rule"] for r in rows)
    picked: List[Dict[str, Any]] = []
    for rule, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0])):
        if len(picked) >= n:
            break
        picked.append(rng.choice(by_rule[rule]))
    rest = [r for r in rows if r not in picked]
    rng.shuffle(rest)
    picked += rest[: max(0, n - len(picked))]
    return picked


def write(sample: List[Dict[str, Any]], result: Optional[Dict[str, Any]], n: int) -> Path:
    findings = {f["key"]: f for f in core.all_findings(result)} if result else {}
    entries = {p["id"]: p for p in mf.load()["pages"]}
    md = BENCH / "labels" / f"sample-{n}.md"
    jl = BENCH / "labels" / f"sample-{n}.jsonl"
    lines = [
        f"# Label check: {len(sample)} findings",
        "",
        "Every label below is model-made. Open the page, find the line, and write TP, FP "
        "or cantTell in the human field of the matching row in "
        f"sample-{n}.jsonl.",
        "",
        "| # | Rule | Page | File:line | Excerpt | Model label | Model reason |",
        "|---|---|---|---|---|---|---|",
    ]
    with jl.open("w", encoding="utf-8") as fh:
        for i, r in enumerate(sample, 1):
            f = findings.get(r["key"], {})
            exc = " ".join((f.get("excerpt", "") or "").replace("|", "/").split())[:120]
            exc = exc.encode("ascii", "backslashreplace").decode("ascii")  # ASCII file
            where = ""
            if f.get("file") and r["page"] in entries:
                # page_dir is bench/pages/<id> or bench/private/<id>; files are
                # relative to its parent, the page store.
                store = mf.page_dir(entries[r["page"]]).parent
                rel = (store / f["file"]).relative_to(BENCH.parent).as_posix()
                where = f"{rel}:{f.get('line', '')}"
            why = (r.get("why") or "").replace("|", "/")
            lines.append(
                f"| {i} | {r['rule']} | {r['page']} | {where} | `{exc}` | {r['final']} | {why} |"
            )
            fh.write(
                json.dumps(
                    {"n": i, "key": r["key"], "rule": r["rule"], "model": r["final"], "human": ""},
                    ensure_ascii=True,
                )
                + "\n"
            )
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n", type=int, default=50, help="findings to draw")
    ap.add_argument("--seed", type=int, default=5, help="random seed")
    ap.add_argument("--run", default=str(OUT / "run.json"), help="corpus run json")
    args = ap.parse_args(argv)
    labels = label.load()
    run = Path(args.run)
    result = core.load_run(run) if run.exists() else None
    try:
        sample = draw(labels, args.n, args.seed)
    except ValueError as exc:
        print(f"sample failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {write(sample, result, args.n)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
