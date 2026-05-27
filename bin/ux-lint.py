#!/usr/bin/env python3
"""ux-lint.py — Python entry-point shim for the v2 linter.

Delegates to ``engine.linter`` which reads rules from
``data/anti-patterns.json``. This is the v2 default; v1's ``ux-lint.sh``
remains as a fallback for environments without Python or the engine.

Usage
-----
::

    bin/ux-lint.py [paths...]
    bin/ux-lint.py --threshold high src/
    bin/ux-lint.py --json src/ > findings.json

Exit code 0 if no findings at or above ``--threshold`` (default: ``high``).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure ``engine`` is importable when run from the repo
HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from engine.linter import lint  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ux-lint",
        description="Deterministic anti-AI-slop linter — reads rules from data/anti-patterns.json",
    )
    parser.add_argument(
        "paths", nargs="*", default=["."],
        help="Files or directories to scan (default: current directory).",
    )
    parser.add_argument(
        "--threshold", default="high",
        choices=["low", "medium", "high", "critical"],
        help="Lowest severity that causes non-zero exit (default: high).",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit raw JSON to stdout (CI-friendly).",
    )
    args = parser.parse_args(argv)

    report = lint(args.paths, severity_threshold=args.threshold)
    payload = report.to_dict()

    if args.json:
        json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        summary = payload["summary"]
        print(f"ux-lint v2 — scanned {payload['files_scanned']} files "
              f"against {payload['rules_loaded']} rules")
        print(f"  critical: {summary.get('critical', 0)}")
        print(f"  high:     {summary.get('high', 0)}")
        print(f"  medium:   {summary.get('medium', 0)}")
        print(f"  low:      {summary.get('low', 0)}")
        print(f"  total:    {summary.get('total', 0)}")
        if payload["findings"]:
            print()
            print("Findings:")
            for f in payload["findings"][:50]:
                print(f"  [{f['severity']}] {f['file']}:{f['line']}:{f['column']}")
                print(f"          {f['rule_name']} ({f['rule_id']})")
                print(f"          {f['excerpt'].strip()[:120]}")
                print(f"          fix: {f['fix']}")
                print()
            if len(payload["findings"]) > 50:
                print(f"  ...and {len(payload['findings']) - 50} more (use --json for full list)")

    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
