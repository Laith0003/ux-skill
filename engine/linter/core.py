"""Anti-AI-slop linter — Python port of ``bin/ux-lint.sh``.

Reads ``data/anti-patterns.json`` (the source of truth for rules) and walks the
target paths, applying each rule's regex with the rule's flags. Output is JSON
by default, with a human-readable table when ``--pretty`` is passed.

Public surface
--------------
``lint(paths, severity_threshold) -> LintReport``
``LintReport`` is JSON-serialisable via ``to_dict()``.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from engine.data_loader import load


SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
# Severity weights for the 0-100 quality score (higher penalty = bigger drop).
# Tuned so a clean file scores 100, a file with a few mediums scores ~80,
# a file with multiple highs scores < 50 (triggers the v2.1 quality gate).
SEVERITY_WEIGHT = {"low": 1, "medium": 4, "high": 10, "critical": 20}
DEFAULT_GLOBS = (
    "*.html", "*.htm", "*.css", "*.scss",
    "*.jsx", "*.tsx", "*.js", "*.ts",
    "*.vue", "*.svelte", "*.astro",
    "*.blade.php", "*.php",
)


def compute_score(findings: List["Finding"], files_scanned: int = 1) -> int:
    """Compute a 0-100 quality score from a list of findings.

    Formula: start at 100, subtract severity-weighted penalties, normalized
    per file scanned so a big repo isn't auto-penalized vs a single file.

        score = max(0, 100 - sum(SEVERITY_WEIGHT[f.severity]) / max(files, 1))

    A clean file = 100. A file with 5 mediums = 80. A file with 5 highs = 50.
    Compounding violations drop the score quickly; the v2.1 gate trips at 65.
    """
    if not findings:
        return 100
    total_penalty = 0
    for f in findings:
        total_penalty += SEVERITY_WEIGHT.get(f.severity, 4)
    per_file = total_penalty / max(files_scanned, 1)
    return max(0, min(100, int(round(100 - per_file))))


@dataclass
class Finding:
    rule_id: str
    rule_name: str
    severity: str
    category: str
    file: str
    line: int
    column: int
    excerpt: str
    fix: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LintReport:
    findings: List[Finding] = field(default_factory=list)
    files_scanned: int = 0
    rules_loaded: int = 0
    exit_code: int = 0
    score: int = 100   # v2.1 — 0-100 quality score, severity-weighted

    def to_dict(self) -> Dict[str, Any]:
        return {
            "files_scanned": self.files_scanned,
            "rules_loaded": self.rules_loaded,
            "exit_code": self.exit_code,
            "score": self.score,
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.counts(),
        }

    def counts(self) -> Dict[str, int]:
        out: Dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for f in self.findings:
            out[f.severity] = out.get(f.severity, 0) + 1
        out["total"] = len(self.findings)
        return out


def _compile_rules() -> List[Dict[str, Any]]:
    data = load("anti-patterns")
    rules: List[Dict[str, Any]] = []
    for entry in data.get("entries", []):
        det = entry.get("detection", {})
        if det.get("type") != "regex":
            continue
        flags = 0
        flag_str = det.get("flags", "")
        if "i" in flag_str:
            flags |= re.IGNORECASE
        if "m" in flag_str:
            flags |= re.MULTILINE
        if "s" in flag_str:
            flags |= re.DOTALL
        try:
            compiled = re.compile(det["pattern"], flags)
        except re.error:
            continue
        rules.append({
            "id": entry.get("id"),
            "name": entry.get("name"),
            "severity": entry.get("severity", "medium"),
            "category": entry.get("category", "General"),
            "fix": entry.get("fix", ""),
            "scope": set(det.get("scope", [])),
            "regex": compiled,
        })
    return rules


def _walk_paths(paths: Iterable[Path]) -> Iterable[Path]:
    for p in paths:
        if p.is_file():
            yield p
        elif p.is_dir():
            for glob in DEFAULT_GLOBS:
                yield from p.rglob(glob)


def _scope_matches(path: Path, scope: set) -> bool:
    if not scope:
        return True
    suffix = path.suffix.lstrip(".").lower()
    if suffix in scope:
        return True
    # special-case combined suffixes (.blade.php)
    name = path.name.lower()
    if name.endswith(".blade.php") and "blade" in scope:
        return True
    return False


def lint(
    paths: Iterable[str] | Iterable[Path],
    severity_threshold: str = "high",
) -> LintReport:
    """Lint the given paths against ``data/anti-patterns.json``.

    ``severity_threshold`` sets the lowest severity that counts toward the
    non-zero exit code (CI gate). Findings below this severity are still
    reported, just not fatal.
    """
    rules = _compile_rules()
    threshold = SEVERITY_RANK.get(severity_threshold, 2)
    findings: List[Finding] = []
    files_scanned = 0

    targets = [Path(p) for p in (paths or [Path(".")])]
    for path in _walk_paths(targets):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        files_scanned += 1
        lines = text.splitlines()

        for rule in rules:
            if not _scope_matches(path, rule["scope"]):
                continue
            for match in rule["regex"].finditer(text):
                start = match.start()
                line_no = text.count("\n", 0, start) + 1
                col_no = start - (text.rfind("\n", 0, start) + 1) + 1
                excerpt = lines[line_no - 1] if 0 < line_no <= len(lines) else match.group(0)
                findings.append(Finding(
                    rule_id=rule["id"] or "unknown",
                    rule_name=rule["name"] or "Unknown rule",
                    severity=rule["severity"],
                    category=rule["category"],
                    file=str(path),
                    line=line_no,
                    column=col_no,
                    excerpt=excerpt[:200],
                    fix=rule["fix"],
                ))

    fatal = any(SEVERITY_RANK.get(f.severity, 0) >= threshold for f in findings)
    score = compute_score(findings, files_scanned)
    return LintReport(
        findings=findings,
        files_scanned=files_scanned,
        rules_loaded=len(rules),
        exit_code=1 if fatal else 0,
        score=score,
    )
