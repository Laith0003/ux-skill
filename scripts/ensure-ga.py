#!/usr/bin/env python3
"""
Ensure every docs/*.html page carries the GA4 gtag.js snippet.

The site is static (GitHub Pages, no server-side includes), so the analytics
tag lives inline in each page's <head>. New pages routinely shipped without it,
silently undercounting GA (the homepage itself was missing it until 2026-06-30).
This script is the durable guard: it injects the canonical snippet right after
<head> on any page missing it. Idempotent (a page that already has the
measurement ID is left untouched).

Usage:
  ensure-ga.py [<glob-or-path> ...]      # inject into any page missing the tag
  ensure-ga.py --check [<glob-or-path>]  # report-only; exit 1 if any page lacks it

With no path args, defaults to docs/*.html (relative to repo root).
CI runs it with --check so a PR that adds an untagged page fails.
"""
from __future__ import annotations
import glob
import os
import sys

# Python puts scripts/ on sys.path when this file runs, so ga imports.
from ga import GA_ID, has_tag, inject


def repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_targets(args: list[str]) -> list[str]:
    if not args:
        args = [os.path.join(repo_root(), "docs", "*.html")]
    files: list[str] = []
    for pattern in args:
        matched = glob.glob(pattern)
        files.extend(matched if matched else [pattern])
    # de-dup, stable order
    seen, out = set(), []
    for f in sorted(files):
        if f not in seen and os.path.isfile(f):
            seen.add(f)
            out.append(f)
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    targets = resolve_targets([a for a in argv if not a.startswith("--")])
    if not targets:
        print("ensure-ga: no HTML files matched", file=sys.stderr)
        return 1

    missing, fixed = [], []
    for path in targets:
        with open(path, encoding="utf-8") as f:
            html = f.read()
        if has_tag(html):
            continue
        if check:
            missing.append(path)
            # GitHub Actions annotation
            print(f"::error file={path}::missing GA4 tag ({GA_ID})")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(inject(html, path))
            fixed.append(path)
            print(f"injected GA into {path}")

    if check:
        if missing:
            print(f"\n{len(missing)} page(s) missing the GA tag. "
                  f"Run: python scripts/ensure-ga.py", file=sys.stderr)
            return 1
        print(f"GA tag present on all {len(targets)} page(s).")
        return 0

    print(f"\nDone. {len(fixed)} page(s) fixed, "
          f"{len(targets) - len(fixed)} already tagged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
