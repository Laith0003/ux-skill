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
# in the repo gets brought into line. Source of truth: `python -m engine.cli.main stats`
# (the summed manifest counts == TOTAL_ENTRIES). Counts only -- NEVER version: the
# version label is correct inside CHANGELOG + historical launch posts, so it is handled
# surgically elsewhere, never blanket-swept.
TOTAL_ENTRIES = "1,243"
BRAND_SPECS = "160"
ANTI_PATTERN_RULES = "152"
COMPONENTS = "148"
PALETTES = "176"
STYLES = "84"
TYPE_PAIRS = "70"
INDUSTRIES = "184"
MOTION_PRESETS = "57"
UX_LAWS = "112"
CHART_TYPES = "35"
TECH_STACKS = "25"
COMMANDS = "25"
MANIFESTS = "12"


# (pattern, replacement). Order matters -- do longest/most-specific first.
# Patterns are regex; replacements are plain. Counts only (no version).
# IMPORTANT: this file excludes ITSELF from the sweep (see SKIP_NAMES) -- otherwise the
# stale literals in the patterns below get rewritten in place and the tool eats itself.
REWRITES = [
    # --- Entry total: language-independent comma-number (guard against longer numbers
    #     like 11,182 or 1,1820 so we never corrupt an unrelated figure). Both stale
    #     variants (1,182 and the partially-updated 1,238) -> canonical.
    (r"(?<!\d)1,182(?!\d)", TOTAL_ENTRIES),
    (r"(?<!\d)1,238(?!\d)", TOTAL_ENTRIES),
    # --- Anti-pattern rule count (English phrasing + shields badge; longest first).
    (r"145\+ anti-pattern", f"{ANTI_PATTERN_RULES} anti-pattern"),
    (r"145 anti-pattern", f"{ANTI_PATTERN_RULES} anti-pattern"),
    (r"\b145 anti\b", f"{ANTI_PATTERN_RULES} anti"),
    (r"120 anti-pattern", f"{ANTI_PATTERN_RULES} anti-pattern"),
    # NOTE: "100 anti-pattern" is deliberately NOT rewritten -- it survives only inside a
    # quoted v2 release note ("1,182 ... 100 anti-pattern regex rules ..."), and that file
    # is skipped below so the quotation stays faithful.
    (r"anti-patterns-145", f"anti-patterns-{ANTI_PATTERN_RULES}"),
    (r"anti-patterns-120", f"anti-patterns-{ANTI_PATTERN_RULES}"),
    # --- Slash-command count.
    (r"22 slash commands", f"{COMMANDS} slash commands"),
    (r"23 slash commands", f"{COMMANDS} slash commands"),
    (r"\b22 commands\b", f"{COMMANDS} commands"),
    (r"\b23 commands\b", f"{COMMANDS} commands"),
    (r"commands-22\b", f"commands-{COMMANDS}"),
    (r"commands-23\b", f"commands-{COMMANDS}"),
    # --- Manifest count.
    (r"11 queryable JSON manifests", f"{MANIFESTS} queryable JSON manifests"),
    (r"11 JSON manifests", f"{MANIFESTS} JSON manifests"),
    (r"11 manifests", f"{MANIFESTS} manifests"),
    (r"manifests-11\b", f"manifests-{MANIFESTS}"),
    # --- Brand-spec count (131 stragglers; most surfaces already say 160).
    (r"131 brand specs?", f"{BRAND_SPECS} brand specs"),
    (r"brand_specs-131", f"brand_specs-{BRAND_SPECS}"),
    (r"\b131 specimens", f"{BRAND_SPECS} specimens"),
    (r"\b131 catalogue", f"{BRAND_SPECS} catalogue"),
    (r"\b131 design languages", f"{BRAND_SPECS} design languages"),
    (r"\b131 brand DESIGN", f"{BRAND_SPECS} brand DESIGN"),
    # --- Components (already current; kept so future data drift is caught).
    (r"\b148 components\b", f"{COMPONENTS} components"),
    (r"components-148\b", f"components-{COMPONENTS}"),
    (r"\b148 component entries", f"{COMPONENTS} component entries"),
]


# Files to skip outright (build artefacts, lockfiles, and the changelog -- whose
# per-release counts are an immutable historical record, not a current-state stat).
SKIP_NAMES = {"package-lock.json", "uv.lock", ".DS_Store", "CHANGELOG.md",
              # Quotes the v2 release notes verbatim ("1,182 ... 100 anti-pattern ...");
              # sweeping its numbers would falsify the quotation.
              "anti-ai-slop-claude-skills.html",
              # Self-exclude: this script's REWRITES contain the stale literals as regex;
              # scanning itself would rewrite the patterns in place and break the tool.
              "sweep-stats.py"}
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
