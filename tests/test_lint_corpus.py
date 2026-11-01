"""Precision and recall of the anti-pattern linter, measured on fixtures.

``tests/lint_corpus/clean`` holds real-world style UI files with no real
anti-patterns, including the cases that used to trip rules: JSX style and sx
objects, custom properties, comments and strings that mention banned words,
minified CSS, data URIs, SVG, Arabic and RTL text, logical properties. Not one
finding at medium severity or above may fire on it.

``tests/lint_corpus/dirty`` holds one file per rule, named ``<rule-id>.<ext>``.
Every rule must fire on its own fixture, so a rule cannot be loosened into
silence without a test failing.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.linter import lint
from engine.linter.core import SEVERITY_RANK, lint_text

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(__file__).resolve().parent / "lint_corpus"
CLEAN = CORPUS / "clean"
DIRTY = CORPUS / "dirty"
RULES = json.loads((ROOT / "data" / "anti-patterns.json").read_text(encoding="utf-8"))["entries"]
RULE_IDS = [r["id"] for r in RULES]

# Rules added for AI-generated tells, each with a clean fixture that holds the
# near-miss the rule must not flag.
NEW_RULE_CLEAN = {
    "default-font-only": ["rules/default-font-only.css", "rules/default-font-only.tsx"],
    "navy-to-purple-gradient": ["rules/navy-to-purple-gradient.css"],
    "purple-to-blue-gradient": ["rules/purple-to-blue-gradient.html", "css/layout.css"],
    "glow-shadow-zero-offset": ["rules/glow-shadow-zero-offset.css", "css/tokens.css"],
    "hairline-border-heavy-shadow": ["rules/hairline-border-heavy-shadow.css", "rules/HairlineCard.tsx"],
    "emoji-in-ui": ["rules/emoji-as-icon.html"],
    "emoji-bullet-marker": ["rules/emoji-as-icon.html"],
    "lone-emoji-as-icon": ["rules/emoji-as-icon.html"],
}


def _dirty_fixture(rule_id: str) -> Path | None:
    matches = [p for p in DIRTY.iterdir() if p.name.split(".", 1)[0] == rule_id]
    return matches[0] if len(matches) == 1 else None


def _fired(path: Path) -> set:
    return {f.rule_id for f in lint_text(str(path), path.read_text(encoding="utf-8"))}


# ---------------------------------------------------------------------------
# Clean corpus
# ---------------------------------------------------------------------------

def test_clean_corpus_is_large_and_varied():
    files = [p for p in CLEAN.rglob("*") if p.is_file()]
    assert len(files) >= 40, f"clean corpus has {len(files)} files; it needs at least 40"
    names = [p.name for p in files]
    for suffix in (".tsx", ".jsx", ".vue", ".blade.php", ".astro", ".html", ".css", ".scss"):
        assert any(n.endswith(suffix) for n in names), f"clean corpus has no {suffix} file"


def test_clean_corpus_has_no_findings_at_medium_or_above():
    report = lint([str(CLEAN)], severity_threshold="medium")
    loud = [f for f in report.findings if SEVERITY_RANK[f.severity] >= SEVERITY_RANK["medium"]]
    detail = "\n".join(
        f"  {Path(f.file).relative_to(CLEAN)}:{f.line}:{f.column} [{f.severity}] {f.rule_id}: {f.excerpt.strip()[:80]}"
        for f in loud
    )
    assert not loud, f"{len(loud)} false positive(s) on the clean corpus:\n{detail}"
    assert report.exit_code == 0


def test_clean_corpus_scans_every_file_once():
    files = [p for p in CLEAN.rglob("*") if p.is_file()]
    assert lint([str(CLEAN)]).files_scanned == len(files)


# ---------------------------------------------------------------------------
# Dirty fixtures: one per rule
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rule_id", RULE_IDS)
def test_rule_fires_on_its_dirty_fixture(rule_id):
    fixture = _dirty_fixture(rule_id)
    assert fixture is not None, (
        f"rule {rule_id!r} has no fixture: add tests/lint_corpus/dirty/{rule_id}.<ext> "
        f"containing code the rule must flag"
    )
    fired = _fired(fixture)
    assert rule_id in fired, (
        f"{fixture.relative_to(CORPUS)}: rule {rule_id!r} did not fire (fired: {sorted(fired)}). "
        f"Fix the rule pattern or its target channel in data/anti-patterns.json"
    )


def test_no_orphan_dirty_fixtures():
    orphans = sorted(p.name for p in DIRTY.iterdir() if p.name.split(".", 1)[0] not in RULE_IDS)
    assert not orphans, f"tests/lint_corpus/dirty has fixtures for unknown rules: {orphans}. Rename or delete them"


# ---------------------------------------------------------------------------
# New rules for AI-generated tells
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rule_id,clean", [(r, c) for r, cs in NEW_RULE_CLEAN.items() for c in cs])
def test_new_rule_stays_quiet_on_its_clean_fixture(rule_id, clean):
    path = CLEAN / clean
    assert rule_id not in _fired(path), f"{rule_id} fired on the clean fixture {clean}"


def test_new_rules_are_medium():
    by_id = {r["id"]: r for r in RULES}
    for rule_id in ("default-font-only", "navy-to-purple-gradient", "glow-shadow-zero-offset",
                    "hairline-border-heavy-shadow"):
        assert by_id[rule_id]["severity"] == "medium", f"{rule_id}: severity must be medium"


@pytest.mark.parametrize("name,snippet,rule_id,should_fire", [
    ("a.css", ".x { font-family: 'Geist', sans-serif; }", "default-font-only", True),
    ("a.css", ":root { --font-sans: Inter, sans-serif; --font-mono: 'Geist Mono', monospace; }",
     "default-font-only", True),
    ("a.css", ".x { font-family: Inter; } @font-face { font-family: Brand; src: url(b.woff2); }",
     "default-font-only", False),
    ("layout.tsx", 'import { Geist, Geist_Mono } from "next/font/google";', "default-font-only", True),
    ("layout.tsx", 'import { Inter, Fraunces } from "next/font/google";\n'
     'const a = Inter({ subsets: ["latin"] });\nconst b = Fraunces({ subsets: ["latin"] });',
     "default-font-only", False),
    ("a.tsx", '<div className="bg-gradient-to-br from-slate-900 via-slate-900 to-purple-900" />',
     "navy-to-purple-gradient", True),
    ("a.tsx", '<div className="bg-slate-900"><span className="text-purple-400">x</span></div>',
     "navy-to-purple-gradient", False),
    ("a.css", ".h { background: linear-gradient(to right, #3b82f6, #8b5cf6); }", "purple-to-blue-gradient", True),
    ("a.html", '<div class="bg-linear-to-r from-indigo-500 to-sky-400"></div>', "purple-to-blue-gradient", True),
    ("a.css", ".g { filter: drop-shadow(0 0 24px #a855f7); }", "glow-shadow-zero-offset", True),
    ("a.html", '<div class="shadow-[0_0_40px_rgba(168,85,247,0.5)]"></div>', "glow-shadow-zero-offset", True),
    ("a.css", ".r { box-shadow: 0 0 0 4px rgb(0 0 0 / 0.2); }", "glow-shadow-zero-offset", False),
    ("a.css", ".r { box-shadow: inset 0 0 30px rgb(0 0 0 / 0.2); }", "glow-shadow-zero-offset", False),
    ("a.html", '<div class="rounded-xl border bg-white shadow-2xl"></div>', "hairline-border-heavy-shadow", True),
    ("a.html", '<div class="rounded-xl border-b bg-white shadow-2xl"></div>', "hairline-border-heavy-shadow", False),
    ("a.tsx", '<article style={{ border: "1px solid #eee", boxShadow: "0 24px 64px rgba(0,0,0,.2)" }} />',
     "hairline-border-heavy-shadow", True),
    ("a.html", "<h2>&#x1F680; Launch</h2>", "emoji-in-ui", True),
    ("a.tsx", '<button type="button">{"\\u{1F389}"} Celebrate</button>', "emoji-in-ui", True),
    ("a.html", '<button type="button" aria-label="Close">&times;</button>', "emoji-in-ui", False),
    ("a.css", 'li::before { content: "\\2714"; }', "emoji-bullet-marker", True),
    ("a.css", 'li::before { content: "\\2022"; }', "emoji-bullet-marker", False),
])
def test_new_rule_cases(tmp_path, name, snippet, rule_id, should_fire):
    path = tmp_path / name
    path.write_text(snippet, encoding="utf-8")
    assert (rule_id in _fired(path)) is should_fire
