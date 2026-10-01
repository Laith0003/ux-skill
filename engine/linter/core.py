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

When the project holds a client's own design system (``ux system detect``
finds one), the files of that system are linted and reported apart, under
``system``: they are the client's fixed input, not generated output, so
they never lower the page's score or its exit code.
"""
from __future__ import annotations

import math
import re
from bisect import bisect_right
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from engine.data_loader import load
from engine.linter.structure import (
    POST_CHECKS, FileContext, in_spans, token_definitions, unused_utility)
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


# Past this many points the penalty decays instead of subtracting, so pages
# with many findings still differ: the score is 100 minus the penalty down
# to SCORE_KNEE, then SCORE_KNEE * exp(-(penalty - SCORE_KNEE) / SCORE_TAIL).
# Past the knee the excess shrinks by how much of the page repeats one
# rule: the n-th finding of a rule in a file counts 1/n of its weight in the
# repeated penalty, and the excess is scaled by that penalty over the full
# one, so a page of distinct problems scores as before.
SCORE_KNEE = 50
SCORE_TAIL = 100.0


def compute_score(findings: List["Finding"], files_scanned: int = 1) -> int:
    """Compute a 0-100 quality score from a list of findings.

    Each finding costs its severity weight (SEVERITY_WEIGHT). The penalty
    is normalized per file scanned, so a big repo is not auto-penalized vs
    a single file.

    Up to SCORE_KNEE the score is 100 minus the penalty: a clean file is
    100, five mediums 80, five highs 50, and the v2.1 gate trips at 65.
    Past the knee the score decays toward 0 and never reaches it, so a page
    with thirty problems still scores under one with twelve. There the
    excess over the knee shrinks by how much the page repeats one rule
    (149 placeholder links are one pattern, not 149 problems): the n-th
    finding of a rule in a file counts 1/n of its weight, heaviest first, and the
    excess is scaled by that repeated penalty over the full one. A page of
    distinct problems scores as before, and so does any page up to the
    knee.
    """
    if not findings:
        return 100
    weights = [SEVERITY_WEIGHT.get(f.severity, 4) for f in findings]
    total_penalty = sum(weights)
    per_file = total_penalty / max(files_scanned, 1)
    if per_file <= SCORE_KNEE:
        return max(0, min(100, int(round(100 - per_file))))
    seen: Dict[Tuple[str, str], int] = {}
    repeated = 0.0
    for f, w in sorted(zip(findings, weights), key=lambda fw: -fw[1]):
        key = (f.file, f.rule_id)  # repeats count within a file, never across files
        seen[key] = seen.get(key, 0) + 1
        repeated += w / seen[key]
    excess = (per_file - SCORE_KNEE) * repeated / total_penalty
    return max(1, int(round(SCORE_KNEE * math.exp(-excess / SCORE_TAIL))))


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


def _counts(findings: Iterable["Finding"]) -> Dict[str, int]:
    out: Dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    n = 0
    for f in findings:
        out[f.severity] = out.get(f.severity, 0) + 1
        n += 1
    out["total"] = n
    return out


@dataclass
class LintReport:
    findings: List[Finding] = field(default_factory=list)
    files_scanned: int = 0
    rules_loaded: int = 0
    exit_code: int = 0
    score: int = 100   # v2.1 — 0-100 quality score, severity-weighted
    # The client's own system files, linted apart: they never touch the
    # score or the exit code above.
    system_files: List[str] = field(default_factory=list)
    system_findings: List[Finding] = field(default_factory=list)
    waived_lines: int = 0  # lines where a ux-lint-disable or ux-lint-off waiver applies

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "files_scanned": self.files_scanned,
            "rules_loaded": self.rules_loaded,
            "exit_code": self.exit_code,
            "score": self.score,
            "waived_lines": self.waived_lines,
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.counts(),
        }
        if self.system_files:
            out["system"] = {
                "note": ("The client's own design system files, found by ux system detect. "
                         "They are its fixed input, not generated output, so their findings "
                         "are listed here and do not lower the page's score or exit code."),
                "files": list(self.system_files),
                "score": compute_score(self.system_findings, len(self.system_files)),
                "findings": [f.to_dict() for f in self.system_findings],
                "summary": _counts(self.system_findings),
            }
        return out

    def counts(self) -> Dict[str, int]:
        return _counts(self.findings)


IGNORED_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    ".astro", "vendor", ".ux", ".venv", "venv", "__pycache__", "coverage",
}
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
    waived, broken = _waivers(text)
    ctx = FileContext(path, text, views)
    ctx.pages = _page_contexts(pages)
    defs = token_definitions(ctx)
    findings: List[Finding] = [Finding(
        rule_id=_REGION_RULE["id"], rule_name=_REGION_RULE["name"],
        severity=_REGION_RULE["severity"], category=_REGION_RULE["category"],
        file=str(name), line=line_no, column=1,
        excerpt=lines[line_no - 1][:200] if line_no <= len(lines) else "",
        fix=message,
    ) for line_no, message in broken]
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
                if target == "css" and unused_utility(ctx, view, match.start()):
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


# Sources that make up a client's system. A build script or package.json only
# builds it; the files it reads are listed as sources of their own.
SYSTEM_KINDS = frozenset(("tokens-source", "tokens", "built-output", "css-foundation",
                          "master-md", "design-md"))
# An extension file sits beside a system and holds what the page added to it.
_EXTENSION_NAME = re.compile(r"(?:[-_.]ext|[-_.]extension|^extension)$", re.I)
# At-rules whose blocks hold no page rules: a face, a registered property.
_TOKEN_AT_RULES = ("@font-face", "@property")


def _tokens_only(path: Path, text: str) -> bool:
    """True when a stylesheet holds nothing but token blocks: every
    declaration sets a custom property (or color-scheme), outside @font-face
    and @property. One page rule makes it the page's own stylesheet."""
    from engine.linter.structure import css_blocks
    view = FileViews(path.name, text).get("css")
    for block in css_blocks(view.text if view is not None else text):
        if any(a.startswith(_TOKEN_AT_RULES) for a in block.atrules):
            continue
        for decl in block.body.split(";"):
            name = decl.split(":", 1)[0].strip().lower()
            if name and not name.startswith("--") and name != "color-scheme" \
                    and not name.startswith("@"):
                return False
    return True


def _engine_listed(f: Path, root: Path) -> bool:
    """True when an engine record (.uxskill/files.json) in the file's folder
    or any folder above it, up to the project root, lists the file."""
    from engine.existing.record import read_record
    for folder in [f.parent, *f.parent.parents]:
        try:
            rel = f.relative_to(folder).as_posix()
        except ValueError:
            break
        if rel in read_record(folder):
            return True
        if folder == root:
            break
    return False


def system_files(files: Iterable[Path], targets: Iterable[Path] = ()) -> set:
    """The resolved paths among ``files`` that belong to a client's own
    design system, which lint reports apart. A file belongs only when all of
    these hold:

    - ``ux system detect`` reports it for the file's project (the nearest
      folder with a project marker, else the linted folder that holds it,
      else its own folder) as a token source, a token file, built output, a
      foundation stylesheet or a hand-written MASTER.md or DESIGN.md, or it
      sits inside a system folder detect reports;
    - the engine did not write it: no digest stamp, and no engine record
      (``.uxskill/files.json``) lists it;
    - it is not an extension file (a name ending in ``-ext`` or
      ``-extension``), which holds what a page added;
    - a stylesheet holds only token blocks: one page rule beside its theme
      block makes it the page's own stylesheet, and it is scored.
    """
    from engine.existing import detect_existing_system, is_ux_skill_file

    folders = [Path(t).resolve() for t in targets if Path(t).is_dir()]
    found: Dict[Path, List[tuple]] = {}
    out = set()
    for f in files:
        f = Path(f).resolve()
        root = (_project_root(f.parent)
                or next((d for d in folders if d in f.parents), None) or f.parent)
        if root not in found:
            result = detect_existing_system(root)
            found[root] = ([((root / s["path"]).resolve(), s["kind"] == "system-folder")
                            for s in result.get("sources", [])
                            if s["kind"] in SYSTEM_KINDS or s["kind"] == "system-folder"]
                           if result.get("found") else [])
        if not any(f == src or (folder and src in f.parents) for src, folder in found[root]):
            continue
        stem = f.name.rsplit(".", 1)[0]
        if _EXTENSION_NAME.search(stem) or is_ux_skill_file(f) or _engine_listed(f, root):
            continue
        if f.name.lower().endswith(STYLE_SUFFIXES):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if not _tokens_only(f, text):
                continue
        out.add(f)
    return out


def lint(
    paths: Iterable[str] | Iterable[Path],
    severity_threshold: str = "high",
) -> LintReport:
    """Lint the given paths against ``data/anti-patterns.json``.

    ``severity_threshold`` sets the lowest severity that counts toward the
    non-zero exit code (CI gate). Findings below this severity are still
    reported, just not fatal. Files of the client's own design system
    (``system_files``) are linted and reported apart: their findings never
    count toward the score or the exit code.
    """
    rules = _compile_rules()
    threshold = SEVERITY_RANK.get(severity_threshold, 2)
    findings: List[Finding] = []
    files_scanned = 0
    waived_lines = 0

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

    theirs = system_files(files, targets)
    own_system: List[str] = []
    system_findings: List[Finding] = []
    for path in files:
        text = read(path)
        if text is None:
            continue
        pages = None
        if path.name.lower().endswith(STYLE_SUFFIXES):
            pages = [(str(p), t) for p in stylesheet_pages(path, files, read=read) if (t := read(p)) is not None]
        found = lint_text(str(path), text, rules, pages=pages)
        if path.resolve() in theirs:
            own_system.append(str(path))
            system_findings.extend(found)
            continue
        files_scanned += 1
        waived_lines += len(_waivers(text)[0])
        findings.extend(found)

    fatal = any(SEVERITY_RANK.get(f.severity, 0) >= threshold for f in findings)
    score = compute_score(findings, files_scanned)
    return LintReport(
        findings=findings,
        files_scanned=files_scanned,
        rules_loaded=len(rules),
        waived_lines=waived_lines,
        exit_code=1 if fatal else 0,
        score=score,
        system_files=own_system,
        system_findings=system_findings,
    )
