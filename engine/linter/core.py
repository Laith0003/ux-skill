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
from typing import Any, Dict, Iterable, List, Optional, Tuple

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
    waived_lines: int = 0  # lines where a ux-lint-disable or ux-lint-off waiver applies

    def to_dict(self) -> Dict[str, Any]:
        return {
            "files_scanned": self.files_scanned,
            "rules_loaded": self.rules_loaded,
            "exit_code": self.exit_code,
            "score": self.score,
            "waived_lines": self.waived_lines,
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


# Waivers, written as comments in the file being linted:
#   ux-lint-disable [rule-a, rule-b]      this line only; no ids waives every rule
#   ux-lint-disable-next-line [rule-a]    the line below
#   ux-lint-off rule-a, rule-b            from this line ...
#   ux-lint-on                            ... to this line, for the named rules only
# A region must name at least one rule and must be closed. A region that breaks
# either rule waives nothing and is reported as a finding on its opening line.
_IDS = r"(?:[:\s]+([a-z0-9][\w-]*(?:\s*,\s*[a-z0-9][\w-]*)*))?"
_DISABLE = re.compile(r"ux-lint-disable(-next-line)?" + _IDS, re.IGNORECASE)
_REGION = re.compile(r"ux-lint-(off|on)\b" + _IDS, re.IGNORECASE)
_REGION_RULE = {"id": "lint-waiver-region", "name": "Broken ux-lint-off region",
                "severity": "high", "category": "Lint"}


def _ids(raw: Optional[str]) -> Optional[set]:
    return {x.strip().lower() for x in raw.split(",")} if raw else None


def _waivers(text: str) -> Tuple[Dict[int, Optional[set]], List[Tuple[int, str]]]:
    """Map line number to the rule ids waived there (``None`` means every rule),
    plus (line, message) for each broken region."""
    waived: Dict[int, Optional[set]] = {}
    broken: List[Tuple[int, str]] = []
    if "ux-lint-" not in text:
        return waived, broken

    def waive(line_no: int, ids: Optional[set]) -> None:
        if ids is None or waived.get(line_no, set()) is None:
            waived[line_no] = None
        else:
            waived.setdefault(line_no, set()).update(ids)  # type: ignore[union-attr]

    opened: Optional[Tuple[int, Optional[set]]] = None
    for line_no, line in enumerate(text.splitlines(), start=1):
        for m in _DISABLE.finditer(line):
            waive(line_no + 1 if m.group(1) else line_no, _ids(m.group(2)))
        for m in _REGION.finditer(line):
            if m.group(1).lower() == "off":
                if opened is not None:
                    broken.append((opened[0], f"ux-lint-off at line {opened[0]} is still open when "
                                   f"another starts at line {line_no}. Add <!-- ux-lint-on --> "
                                   f"before line {line_no}."))
                opened = (line_no, _ids(m.group(2)))
            elif opened is None:
                broken.append((line_no, f"ux-lint-on at line {line_no} closes no region. Remove it, "
                               "or add <!-- ux-lint-off rule-id --> above the quoted text."))
            else:
                first, ids = opened
                opened = None
                if not ids:
                    broken.append((first, f"ux-lint-off at line {first} names no rule. Name the rules "
                                   "it waives: <!-- ux-lint-off rule-a, rule-b -->."))
                    continue
                for n in range(first, line_no + 1):
                    waive(n, ids)
    if opened is not None:
        broken.append((opened[0], f"ux-lint-off at line {opened[0]} is never closed. Add "
                       "<!-- ux-lint-on --> after the last line it should cover."))
    return waived, broken


# Post-filters: checks a regex cannot make across a file. Each gets the whole
# text and the match start, and returns True when the match is not a finding.
_ATTR = r"(?<![\w-]){name}\s*=\s*[\"']([^\"']*)[\"']"


def _attr(tag: str, name: str) -> Optional[str]:
    m = re.search(_ATTR.format(name=name), tag, re.IGNORECASE)
    return m.group(1) if m else None


def _has_id(text: str, value: str) -> bool:
    return re.search(r"(?<![\w-])id\s*=\s*[\"']" + re.escape(value) + r"[\"']", text) is not None


def _input_has_name(text: str, pos: int) -> bool:
    """placeholder-as-label: the input has an accessible name other than its
    placeholder: aria-label with text, aria-labelledby naming ids that exist,
    a <label for> (or htmlFor) matching its id, or a wrapping <label>."""
    end = text.find(">", pos)
    tag = text[pos:end + 1 if end != -1 else len(text)]
    if (_attr(tag, "aria-label") or "").strip():
        return True
    refs = (_attr(tag, "aria-labelledby") or "").split()
    if refs and all(_has_id(text, r) for r in refs):
        return True
    own_id = _attr(tag, "id")
    if own_id and re.search(r"<label\b[^>]*(?<![\w-])(?:for|htmlFor)\s*=\s*[\"']"
                            + re.escape(own_id) + r"[\"']", text, re.IGNORECASE):
        return True
    before = text[:pos].lower()
    opened = before.rfind("<label")
    return opened != -1 and before.find("</label", opened) == -1


def _blur_has_fallback(text: str, pos: int) -> bool:
    """glass-without-fallback: a background or background-color property in the
    same CSS rule or style attribute, before or after the blur."""
    brace, attr = text.rfind("{", 0, pos), text.rfind('style="', 0, pos)
    if attr > brace and text.find('"', attr + 7, pos) == -1:
        start, end = attr, text.find('"', pos)
    else:
        start, end = brace, text.find("}", pos)
    block = text[max(start, 0):end if end != -1 else len(text)]
    return re.search(r"(?<![\w-])background(?:-color)?\s*:", block, re.IGNORECASE) is not None


_POST_FILTERS = {
    "placeholder-as-label": _input_has_name,
    "glass-without-fallback": _blur_has_fallback,
}


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
    waived_lines = 0

    targets = [Path(p) for p in (paths or [Path(".")])]
    for path in _walk_paths(targets):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        files_scanned += 1
        lines = text.splitlines()
        waived, broken = _waivers(text)
        waived_lines += len(waived)
        for line_no, message in broken:
            findings.append(Finding(
                rule_id=_REGION_RULE["id"], rule_name=_REGION_RULE["name"],
                severity=_REGION_RULE["severity"], category=_REGION_RULE["category"],
                file=str(path), line=line_no, column=1,
                excerpt=lines[line_no - 1][:200] if line_no <= len(lines) else "",
                fix=message,
            ))

        for rule in rules:
            if not _scope_matches(path, rule["scope"]):
                continue
            post = _POST_FILTERS.get(rule["id"])
            for match in rule["regex"].finditer(text):
                start = match.start()
                line_no = text.count("\n", 0, start) + 1
                w = waived.get(line_no, set())
                if w is None or (rule["id"] or "").lower() in w:
                    continue
                if post is not None and post(text, start):
                    continue
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
        waived_lines=waived_lines,
        exit_code=1 if fatal else 0,
        score=score,
    )
