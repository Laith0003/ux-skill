"""python -m bench <command>: capture, run, report, diff, sample, ablate, check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional


def _capture(args: argparse.Namespace) -> int:
    from bench import capture, manifest

    data = manifest.load()
    failed = []
    for src in capture.load_sources():
        if args.only and src["id"] not in args.only:
            continue
        try:
            entry = capture.capture(src)
        except capture.CaptureError as exc:
            failed.append(str(exc))
            print(f"FAILED {src['id']}: {exc}", file=sys.stderr)
            continue
        manifest.upsert(data, entry)
        print(f"captured {entry['id']} {entry['sha256'][:12]}")
    manifest.save(data)
    return 1 if failed else 0


def _run(args: argparse.Namespace) -> int:
    from bench import core

    result = core.run(
        render=not args.static_only, only=args.only, seeded=args.seeded, twice=args.twice
    )
    out = Path(args.out) if args.out else core.default_out(args.seeded)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
    print(core.summary(result))
    print(f"wrote {out}")
    if args.update_expected and not args.seeded:
        n = core.write_expected(result)
        print(f"updated {n} golden files in bench/expected/")
    return 1 if result.get("nondeterministic") else 0


def _report(args: argparse.Namespace) -> int:
    from bench import report
    from bench import ablate

    rows = None if args.no_ablation else ablate.run()
    text = report.build(
        run_path=Path(args.run) if args.run else None,
        seeded_path=Path(args.seeded_run) if args.seeded_run else None,
        ablation=rows,
    )
    out = Path(args.out) if args.out else report.REPORT
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def _label(args: argparse.Namespace) -> int:
    from bench import core, label, manifest

    result = core.load_run(Path(args.run) if args.run else core.default_out())
    rows, open_ = label.label_all(result, manifest.load())
    n = label.write(rows)
    missing = sum(1 for r in rows if r["final"] is None)
    print(
        f"wrote {n} label rows to bench/labels/labels.jsonl; {missing} findings have no "
        f"criterion in labels/guide.json; {len(open_)} disagreements have no tiebreak"
    )
    if args.show_open:
        for o in open_[: args.show_open]:
            print(json.dumps(o, ensure_ascii=True))
    return 0


def _ablate(args: argparse.Namespace) -> int:
    from bench import ablate

    try:
        rows = ablate.run(args.pack)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(ablate.table(rows))
    return 0


def _seed(args: argparse.Namespace) -> int:
    from bench import seeded

    data = seeded.build()
    print(f"wrote {len(data['pages'])} seeded pages and bench/seeded/plants.json")
    return 0


def _check(args: argparse.Namespace) -> int:
    from bench import manifest

    probs = manifest.problems(manifest.load())
    for p in probs:
        print(p)
    return 1 if probs else 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m bench", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("capture", help="freeze the designer-built sources in sources.json")
    c.add_argument("--only", nargs="*", help="source ids to capture (default: all)")
    c.set_defaults(fn=_capture)

    r = sub.add_parser("run", help="lint every page (static, and render where Playwright works)")
    r.add_argument("--static-only", action="store_true", help="skip the render pass")
    r.add_argument("--only", nargs="*", help="page ids to run (default: all)")
    r.add_argument("--seeded", action="store_true", help="run the seeded-defect set instead")
    r.add_argument(
        "--twice",
        action="store_true",
        help="run every page twice and fail when the findings differ",
    )
    r.add_argument("--out", help="where to write the run (default: bench/out/run.json)")
    r.add_argument(
        "--update-expected",
        action="store_true",
        help="rewrite bench/expected/ from this run (the only way goldens change)",
    )
    r.set_defaults(fn=_run)

    p = sub.add_parser(
        "report", help="write bench/report.md from a run, the labels and the seeded run"
    )
    p.add_argument("--run", help="corpus run json (default: bench/out/run.json)")
    p.add_argument("--seeded-run", help="seeded run json (default: bench/out/seeded.json)")
    p.add_argument("--out", help="where to write the report (default: bench/report.md)")
    p.add_argument("--no-ablation", action="store_true", help="leave the ablation table out")
    p.set_defaults(fn=_report)

    lb = sub.add_parser("label", help="apply labels/guide.json and labels/tiebreak.json to a run")
    lb.add_argument("--run", help="corpus run json (default: bench/out/run.json)")
    lb.add_argument(
        "--show-open",
        type=int,
        default=0,
        help="print this many disagreements that have no tiebreak",
    )
    lb.set_defaults(fn=_label)

    ab = sub.add_parser("ablate", help="build the rule pack with a guidance pack switched off")
    ab.add_argument("--pack", help="one guidance pack (default: every pack)")
    ab.set_defaults(fn=_ablate)

    s = sub.add_parser("seed", help="write the seeded-defect pages from bench/seeded.py")
    s.set_defaults(fn=_seed)

    k = sub.add_parser("check", help="check the manifest for missing or malformed fields")
    k.set_defaults(fn=_check)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
