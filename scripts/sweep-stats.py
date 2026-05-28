"""Sweep stat references across the repo to keep them in sync.

Single source of truth: the constants below. Re-run after data changes.

Usage:
  python3 scripts/sweep-stats.py        # dry-run
  python3 scripts/sweep-stats.py --write
"""
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent

# CURRENT canonical counts. Update these once and re-run; everywhere else
# in the repo gets brought into line.
TOTAL_ENTRIES = "1,182"
BRAND_SPECS = "131"
ANTI_PATTERN_RULES = "120"
COMPONENTS = "148"
PALETTES = "176"
STYLES = "84"
TYPE_PAIRS = "70"
INDUSTRIES = "184"
MOTION_PRESETS = "57"
UX_LAWS = "112"
CHART_TYPES = "35"
TECH_STACKS = "25"


# (pattern, replacement, description). Order matters — do longest first.
REWRITES = [
    # Brand count
    (r"131 brand specs?", f"{BRAND_SPECS} brand specs"),
    (r"brand_specs-131", f"brand_specs-{BRAND_SPECS}"),
    (r"131 specimens", f"{BRAND_SPECS} specimens"),
    (r"131 catalogue", f"{BRAND_SPECS} catalogue"),
    (r"131 design languages", f"{BRAND_SPECS} design languages"),
    (r"131 brand DESIGN", f"{BRAND_SPECS} brand DESIGN"),
    # Entry total
    (r"1,182 structured entries", f"{TOTAL_ENTRIES} structured entries"),
    (r"1,182 entries", f"{TOTAL_ENTRIES} entries"),
    (r"1,182 entries", f"{TOTAL_ENTRIES} entries"),
    (r"1,182 structured", f"{TOTAL_ENTRIES} structured"),
    # Anti-pattern total
    (r"120 anti-pattern rules", f"{ANTI_PATTERN_RULES} anti-pattern rules"),
    (r"anti-patterns-120", f"anti-patterns-{ANTI_PATTERN_RULES}"),
    (r"120 anti-pattern rules", f"{ANTI_PATTERN_RULES} anti-pattern rules"),
    (r"anti-patterns-120", f"anti-patterns-{ANTI_PATTERN_RULES}"),
    (r"120 anti-pattern rules", f"{ANTI_PATTERN_RULES} anti-pattern rules"),
    (r"anti-patterns-120", f"anti-patterns-{ANTI_PATTERN_RULES}"),
    # Components
    (r"148 components\b", f"{COMPONENTS} components"),
    (r"components-148", f"components-{COMPONENTS}"),
    (r"148 component entries", f"{COMPONENTS} component entries"),
]


# Files to skip outright (build artefacts, lockfiles, etc.).
SKIP_NAMES = {"package-lock.json", "uv.lock", ".DS_Store"}
SKIP_DIRS = {".git", "node_modules", "_staging", ".pytest_cache", "__pycache__", "dist", "build", "site-packages"}


# Extensions to scan.
TEXT_EXTS = {".md", ".html", ".css", ".js", ".json", ".py", ".txt", ".yml", ".yaml", ".toml"}


def iter_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p.name in SKIP_NAMES:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXTS:
            continue
        yield p


def main():
    write = "--write" in sys.argv
    touched = 0
    changes = 0
    for path in iter_files():
        try:
            txt = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        original = txt
        for pat, rep in REWRITES:
            txt = re.sub(pat, rep, txt)
        if txt != original:
            rel = path.relative_to(ROOT)
            n = sum(1 for _ in re.finditer("|".join(re.escape(p[0]) for p in REWRITES), original))
            changes += n
            touched += 1
            print(f"  {'WRITE' if write else 'dry  '}  {rel}")
            if write:
                path.write_text(txt, encoding="utf-8")
    mode = "wrote" if write else "would touch"
    print(f"\n{mode} {touched} files  ({changes} matches)")


if __name__ == "__main__":
    main()
