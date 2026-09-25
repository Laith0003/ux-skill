"""Anti-AI-slop linter: the Python port of ``bin/ux-lint.sh``.

Reads ``data/anti-patterns.json`` (the source of truth for rules) and walks the
target paths, applying each rule's regex with the rule's flags. Output is JSON
by default, with a human-readable table when ``--pretty`` is passed.

Each rule reads one or more channels of a file (markup, css, classes, text,
code, raw); see ``engine/linter/views.py``.

Public surface
--------------
``lint(paths, severity_threshold) -> LintReport``
``lint_text(name, text) -> List[Finding]`` lints one file's contents.
``LintReport`` is JSON-serialisable via ``to_dict()``.
"""
from __future__ import annotations

import re
from bisect import bisect_right
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

from engine.data_loader import load
from engine.linter.structure import POST_CHECKS, FileContext, in_spans, token_definitions
from engine.linter.views import CHANNELS, FileViews, is_mention


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


IGNORED_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    ".astro", "vendor", ".ux", ".venv", "venv", "__pycache__", "coverage",
}
_DISABLE = re.compile(
    r"ux-lint-disable(-next-line)?"
    r"(?:[:\s]+([a-z0-9][\w-]*(?:\s*,\s*[a-z0-9][\w-]*)*))?",
    re.IGNORECASE,
)
_RULE_CACHE: Dict[int, List[Dict[str, Any]]] = {}


def _flags(flag_str: str) -> int:
    flags = 0
    if "i" in flag_str:
        flags |= re.IGNORECASE
    if "m" in flag_str:
        flags |= re.MULTILINE
    if "s" in flag_str:
        flags |= re.DOTALL
    return flags


def _targets(det: Dict[str, Any]) -> tuple:
    target = det.get("target", "markup")
    targets = (target,) if isinstance(target, str) else tuple(target)
    return tuple(t for t in targets if t in CHANNELS) or ("markup",)


def _compile_pass(det: Dict[str, Any], flags: int) -> Dict[str, Any]:
    """One regex pass: a pattern, the channels it reads, and an optional
    ``unless`` pattern that waives the pass for the whole file."""
    targets = _targets(det)
    unless_target = det.get("unless_target", targets)
    return {
        "regex": re.compile(det["pattern"], flags),
        "targets": targets,
        "unless": re.compile(det["unless"], flags) if det.get("unless") else None,
        "unless_targets": (unless_target,) if isinstance(unless_target, str) else tuple(unless_target),
    }


def _compile_rules() -> List[Dict[str, Any]]:
    data = load("anti-patterns")
    cached = _RULE_CACHE.get(id(data))
    if cached is not None:
        return cached
    rules: List[Dict[str, Any]] = []
    for entry in data.get("entries", []):
        det = entry.get("detection", {})
        if det.get("type") != "regex":
            continue
        flags = _flags(det.get("flags", ""))
        try:
            passes = [_compile_pass(det, flags)]
            passes.extend(_compile_pass(extra, _flags(extra.get("flags", det.get("flags", ""))))
                          for extra in det.get("also", []))
        except (re.error, KeyError):
            continue
        rules.append({
            "id": entry.get("id"),
            "name": entry.get("name"),
            "severity": entry.get("severity", "medium"),
            "category": entry.get("category", "General"),
            "fix": entry.get("fix", ""),
            "scope": set(det.get("scope", [])),
            "regex": passes[0]["regex"],
            "passes": passes,
            "skip_inside": tuple(x.lower() for x in det.get("skip_inside", [])),
            "post": POST_CHECKS.get(det.get("post", "")),
            # A rule written for token definitions also reads them inside a
            # token layer; every other rule skips them there.
            "token_defs": bool(det.get("token_definitions")),
        })
    _RULE_CACHE.clear()
    _RULE_CACHE[id(data)] = rules
    return rules


def _walk_paths(paths: Iterable[Path]) -> Iterable[Path]:
    seen = set()
    for p in paths:
        if p.is_file():
            candidates: Iterable[Path] = [p]
        elif p.is_dir():
            candidates = (
                f for glob in DEFAULT_GLOBS for f in p.rglob(glob)
                if not IGNORED_DIRS.intersection(f.relative_to(p).parts[:-1])
            )
        else:
            continue
        for f in candidates:
            key = f.resolve()
            if key in seen:
                continue
            seen.add(key)
            yield f


# Extensions that read like another scope: an .htm file is HTML, and a Svelte
# component is HTML markup with Vue-like blocks.
SCOPE_ALIASES = {"htm": ("html",), "svelte": ("html", "vue")}


def _scope_matches(path: Path, scope: set) -> bool:
    if not scope:
        return True
    suffix = path.suffix.lstrip(".").lower()
    if suffix in scope or any(alias in scope for alias in SCOPE_ALIASES.get(suffix, ())):
        return True
    # special-case combined suffixes (.blade.php)
    name = path.name.lower()
    if name.endswith(".blade.php") and "blade" in scope:
        return True
    return False


def _suppressions(text: str) -> Dict[int, Optional[set]]:
    """Map line number to the rule ids waived there (``None`` means all)."""
    out: Dict[int, Optional[set]] = {}
    if "ux-lint-disable" not in text:
        return out
    for line_no, line in enumerate(text.splitlines(), start=1):
        for m in _DISABLE.finditer(line):
            target = line_no + 1 if m.group(1) else line_no
            ids = {x.strip().lower() for x in m.group(2).split(",")} if m.group(2) else None
            if ids is None or out.get(target, set()) is None:
                out[target] = None
            else:
                out.setdefault(target, set()).update(ids)  # type: ignore[union-attr]
    return out


def _pass_targets(rule: Dict[str, Any]) -> Iterable[tuple]:
    for rpass in rule["passes"]:
        for target in rpass["targets"]:
            yield rpass, target


# Files that hold markup a separate stylesheet can style.
MARKUP_SUFFIXES = (".html", ".htm", ".php", ".vue", ".svelte", ".astro", ".jsx", ".tsx")
STYLE_SUFFIXES = (".css", ".scss")
_STYLE_REF = re.compile(
    r"""<link\b[^>]*?\bhref\s*=\s*["']([^"'?#]+)"""
    r"""|\bimport\s+(?:[\w{}\s,*]+\s+from\s+)?["']([^"'?#]+\.s?css)["']""",
    re.I,
)


ROOT_MARKERS = (".git", "package.json", "pyproject.toml", "composer.json")
# How far a stylesheet's pages are looked for above it, without a root marker.
MAX_LEVELS = 4


def _project_root(start: Path, stop: Optional[Path] = None) -> Optional[Path]:
    """The nearest folder at or above ``start`` holding a project marker, or
    ``stop`` when the walk reaches it first; None when neither is found."""
    stop = stop.resolve() if stop else None
    for folder in [start, *start.parents]:
        if stop is not None and folder == stop:
            return folder
        if any((folder / m).exists() for m in ROOT_MARKERS):
            return folder
    return None


def _links(page: Path, text: str, css: Path, root: Optional[Path] = None) -> bool:
    """True when ``page`` loads the stylesheet at ``css`` by a link or an import.
    A root-relative link resolves against the project root; with no root
    known, against the page's own folder and each one above it."""
    target = css.resolve()
    page = page.resolve()
    for m in _STYLE_REF.finditer(text):
        ref = (m.group(1) or m.group(2) or "").strip()
        if not ref or re.match(r"^(?:[a-z]+:)?//", ref, re.I) or ref.startswith(("data:", "{", "$")):
            continue
        if ref.startswith("/"):
            base = root or _project_root(page.parent)
            bases = [base] if base else [page.parent, *page.parent.parents]
            if any((b / ref.lstrip("/")).resolve() == target for b in bases):
                return True
        elif (page.parent / ref).resolve() == target:
            return True
    return False


def _folders_up(css: Path, root: Optional[Path]) -> List[Path]:
    """The stylesheet's folder and the ones above it, up to the project root,
    at most MAX_LEVELS above the stylesheet."""
    out: List[Path] = []
    for folder in [css.parent, *css.parent.parents][:MAX_LEVELS + 1]:
        out.append(folder)
        if root is not None and folder == root:
            break
    return out


def stylesheet_pages(css: Path, candidates: Iterable[Path] = (), root: Optional[Path] = None,
                     read: Optional[Callable[[Path], Optional[str]]] = None) -> List[Path]:
    """The pages that load the stylesheet ``css``: from ``candidates`` (the
    files being linted) and the markup files in its folder and each folder
    above it, up to the project root (``root``, else the nearest folder with
    a .git, package.json, pyproject.toml or composer.json). ``read`` returns
    a page's text, so a lint run reads each page once."""
    css = Path(css).resolve()
    proj = Path(root).resolve() if root else _project_root(css.parent)
    pool: Dict[Path, Path] = {}
    for folder in _folders_up(css, proj):
        if folder.is_dir():
            for f in sorted(folder.iterdir()):
                if f.is_file() and f.name.lower().endswith(MARKUP_SUFFIXES):
                    pool.setdefault(f.resolve(), f)
    for f in candidates:
        f = Path(f)
        if f.name.lower().endswith(MARKUP_SUFFIXES) and f.is_file():
            pool.setdefault(f.resolve(), f)
    out: List[Path] = []
    for key in sorted(pool):
        if read is not None:
            text = read(pool[key])
        else:
            try:
                text = pool[key].read_text(encoding="utf-8", errors="ignore")
            except OSError:
                text = None
        if text is not None and _links(pool[key], text, css, proj):
            out.append(pool[key])
    return out


def _page_contexts(pages: Optional[Iterable[tuple]]) -> List[FileContext]:
    out: List[FileContext] = []
    for pname, ptext in pages or ():
        ppath = Path(pname)
        out.append(FileContext(ppath, ptext, FileViews(ppath.name, ptext)))
    return out


def lint_text(name: str, text: str, rules: Optional[List[Dict[str, Any]]] = None,
              pages: Optional[Iterable[tuple]] = None) -> List[Finding]:
    """Lint one file's contents. ``name`` supplies the extension and the
    path reported in each finding. ``pages`` are ``(name, text)`` pairs of
    the pages that load this stylesheet, read by rules that need its markup."""
    rules = _compile_rules() if rules is None else rules
    path = Path(name)
    views = FileViews(path.name, text)
    line_starts = [0] + [m.end() for m in re.finditer("\n", text)]
    lines = text.splitlines()
    waived = _suppressions(text)
    ctx = FileContext(path, text, views)
    ctx.pages = _page_contexts(pages)
    defs = token_definitions(ctx)
    findings: List[Finding] = []
    for rule in rules:
        if not _scope_matches(path, rule["scope"]):
            continue
        seen_lines = set()
        for rpass, target in _pass_targets(rule):
            if rpass["unless"] is not None and any(
                (uv := views.get(ut)) is not None and rpass["unless"].search(uv.text)
                for ut in rpass["unless_targets"]
            ):
                continue
            view = views.get(target)
            if view is None or not view.text:
                continue
            for match in rpass["regex"].finditer(view.text):
                if target == "text" and is_mention(view.text, match.start(), match.end()):
                    continue
                start = view.orig(match.start())
                if defs is not None and not rule["token_defs"] and in_spans(defs, start):
                    continue
                if rule["skip_inside"] and ctx.inside(start, rule["skip_inside"]):
                    continue
                line_no = bisect_right(line_starts, start)
                if line_no in seen_lines:
                    continue
                w = waived.get(line_no, set())
                if w is None or (rule["id"] or "").lower() in w:
                    continue
                if rule["post"] is not None and not rule["post"](ctx, view, match, start):
                    continue
                seen_lines.add(line_no)
                col_no = start - line_starts[line_no - 1] + 1
                excerpt = lines[line_no - 1] if 0 < line_no <= len(lines) else match.group(0)
                findings.append(Finding(
                    rule_id=rule["id"] or "unknown",
                    rule_name=rule["name"] or "Unknown rule",
                    severity=rule["severity"],
                    category=rule["category"],
                    file=str(name),
                    line=line_no,
                    column=col_no,
                    excerpt=excerpt[:200],
                    fix=rule["fix"],
                ))
    return findings


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
    files = list(_walk_paths(targets))
    texts: Dict[Path, str] = {}

    def read(p: Path) -> Optional[str]:
        key = p.resolve()
        if key not in texts:
            try:
                texts[key] = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                return None
        return texts[key]

    for path in files:
        text = read(path)
        if text is None:
            continue
        files_scanned += 1
        pages = None
        if path.name.lower().endswith(STYLE_SUFFIXES):
            pages = [(str(p), t) for p in stylesheet_pages(path, files, read=read) if (t := read(p)) is not None]
        findings.extend(lint_text(str(path), text, rules, pages=pages))

    fatal = any(SEVERITY_RANK.get(f.severity, 0) >= threshold for f in findings)
    score = compute_score(findings, files_scanned)
    return LintReport(
        findings=findings,
        files_scanned=files_scanned,
        rules_loaded=len(rules),
        exit_code=1 if fatal else 0,
        score=score,
    )
