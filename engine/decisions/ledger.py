"""Decisions ledger — JSONL append-only with schema_v=1 locked.

Writes mirror to:
  - ``.ux/decisions.jsonl`` in the current project (gitignored by convention)
  - ``~/.uxskill/decisions.jsonl`` for cross-project learning (per-user)

Both writes are best-effort and silently no-op on permission errors so a
read-only filesystem never breaks a command.

**Privacy switches:**
  - ``UXSKILL_NO_LOG=1`` env var disables all writes
  - ``--no-log`` CLI flag (handled in cli.main, sets the env var)
  - ``Scope.PROJECT`` writes only to project, never user
  - ``Scope.USER`` writes only to user, never project
  - ``Scope.BOTH`` (default) writes to both

**Schema lock:**
Every line is a JSON object with these REQUIRED fields:
    _v             int        schema version, currently 1
    ts             float      UTC unix time
    command        str        one of: recommend, design, lint, evolve, system
    brief_id       str        sha1 of the brief or "ad-hoc"
    context_hash   str        sha1 of (industry, ui_type, tone, stack) tuple
    industry       str|null
    ui_type        str|null
    mode           str        synthesis | brand_anchor | strict_brand | n/a
    picked_brand   str|null   brand id if brand-anchor / strict
    picked_style   str|null
    picked_palette str|null
    axes           dict|null  {warmth, contrast, density, ...} if synth
    lint_score     int|null   0-100 if a lint score is available
    lint_high      int        count of high-severity findings
    lint_med       int        count of medium-severity findings
    lint_low       int        count of low-severity findings
    artifact_path  str|null   filesystem path to generated artifact
    user_accepted  bool|null  None until user signals via /ux-critique
    duration_ms    int|null   how long the command took

NEVER rename a column. NEVER reuse a column name with different semantics.
To add a column: append it with default null. Old readers ignore it.
"""
from __future__ import annotations

import enum
import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SCHEMA_VERSION = 1


class Scope(enum.Enum):
    """Which logs to write to / read from."""
    PROJECT = "project"
    USER = "user"
    BOTH = "both"


def _project_root() -> Path:
    """Walk up from cwd looking for a .ux dir; fall back to cwd."""
    cur = Path.cwd().resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".ux").is_dir():
            return parent
    return cur


PROJECT_PATH = _project_root() / ".ux" / "decisions.jsonl"
USER_PATH = Path.home() / ".uxskill" / "decisions.jsonl"


def _logging_enabled() -> bool:
    return os.environ.get("UXSKILL_NO_LOG", "").strip() not in ("1", "true", "yes")


def _ensure_parent(path: Path) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError):
        pass


def _safe_write(path: Path, line: str) -> bool:
    """Append one line, swallowing filesystem errors."""
    try:
        _ensure_parent(path)
        with path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        return True
    except (OSError, PermissionError):
        return False


@dataclass(frozen=True)
class DecisionSchema:
    """Reference for the locked schema. Tests assert against this."""
    required: tuple = (
        "_v", "ts", "command", "brief_id", "context_hash",
        "industry", "ui_type", "mode",
        "picked_brand", "picked_style", "picked_palette",
        "axes", "lint_score", "lint_high", "lint_med", "lint_low",
        "artifact_path", "user_accepted", "duration_ms",
    )
    version: int = SCHEMA_VERSION


def _normalize(decision: Dict[str, Any]) -> Dict[str, Any]:
    """Coerce a partial decision dict into the locked schema shape."""
    schema = DecisionSchema()
    out: Dict[str, Any] = {"_v": SCHEMA_VERSION}
    # Auto-fill defaults for any missing field.
    defaults: Dict[str, Any] = {
        "ts": time.time(),
        "command": "unknown",
        "brief_id": "ad-hoc",
        "context_hash": "",
        "industry": None,
        "ui_type": None,
        "mode": "n/a",
        "picked_brand": None,
        "picked_style": None,
        "picked_palette": None,
        "axes": None,
        "lint_score": None,
        "lint_high": 0,
        "lint_med": 0,
        "lint_low": 0,
        "artifact_path": None,
        "user_accepted": None,
        "duration_ms": None,
    }
    for k in schema.required:
        if k == "_v":
            continue
        out[k] = decision.get(k, defaults.get(k))
    return out


def hash_context(industry: Optional[str], ui_type: Optional[str],
                 tone: Optional[str] = None, stack: Optional[str] = None) -> str:
    """Stable sha1 of the four context dimensions for bucket-matching."""
    raw = "|".join(str(x or "").lower() for x in (industry, ui_type, tone, stack))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def hash_brief(brief_text: str) -> str:
    """Stable sha1 of a brief string."""
    return hashlib.sha1((brief_text or "").encode("utf-8")).hexdigest()[:16]


def record(decision: Dict[str, Any], scope: Scope = Scope.BOTH) -> bool:
    """Append a decision to the ledger.

    Returns True if at least one write succeeded. False if logging is
    disabled or all writes failed.
    """
    if not _logging_enabled():
        return False
    normalized = _normalize(decision)
    line = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"))
    ok = False
    if scope in (Scope.PROJECT, Scope.BOTH):
        ok = _safe_write(PROJECT_PATH, line) or ok
    if scope in (Scope.USER, Scope.BOTH):
        ok = _safe_write(USER_PATH, line) or ok
    return ok


def _read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    # Schema-compat: only yield rows whose _v we support.
                    if obj.get("_v", 1) > SCHEMA_VERSION:
                        continue
                    yield obj
                except json.JSONDecodeError:
                    continue
    except (OSError, PermissionError):
        return


def read_all(scope: Scope = Scope.BOTH) -> List[Dict[str, Any]]:
    """Read every decision in the requested scope, project before user."""
    out: List[Dict[str, Any]] = []
    if scope in (Scope.PROJECT, Scope.BOTH):
        out.extend(_read_jsonl(PROJECT_PATH))
    if scope in (Scope.USER, Scope.BOTH):
        out.extend(_read_jsonl(USER_PATH))
    return out


def query(industry: Optional[str] = None, ui_type: Optional[str] = None,
          command: Optional[str] = None, min_score: Optional[int] = None,
          accepted_only: bool = False, limit: Optional[int] = None,
          scope: Scope = Scope.BOTH) -> List[Dict[str, Any]]:
    """Filter decisions by common dimensions."""
    rows = read_all(scope=scope)
    out: List[Dict[str, Any]] = []
    for row in rows:
        if industry and (row.get("industry") or "").lower() != industry.lower():
            continue
        if ui_type and (row.get("ui_type") or "").lower() != ui_type.lower():
            continue
        if command and row.get("command") != command:
            continue
        if min_score is not None and (row.get("lint_score") or 0) < min_score:
            continue
        if accepted_only and not row.get("user_accepted"):
            continue
        out.append(row)
        if limit and len(out) >= limit:
            break
    return out


def stats(scope: Scope = Scope.BOTH) -> Dict[str, Any]:
    """Aggregate counters for the public stats view."""
    rows = read_all(scope=scope)
    by_cmd: Dict[str, int] = {}
    by_industry: Dict[str, int] = {}
    by_ui_type: Dict[str, int] = {}
    by_mode: Dict[str, int] = {}
    by_brand: Dict[str, int] = {}
    scores: List[int] = []
    accepted = 0
    total = len(rows)
    for r in rows:
        cmd = r.get("command") or "unknown"
        by_cmd[cmd] = by_cmd.get(cmd, 0) + 1
        ind = r.get("industry")
        if ind:
            by_industry[ind] = by_industry.get(ind, 0) + 1
        ut = r.get("ui_type")
        if ut:
            by_ui_type[ut] = by_ui_type.get(ut, 0) + 1
        m = r.get("mode")
        if m:
            by_mode[m] = by_mode.get(m, 0) + 1
        b = r.get("picked_brand")
        if b:
            by_brand[b] = by_brand.get(b, 0) + 1
        s = r.get("lint_score")
        if isinstance(s, (int, float)):
            scores.append(int(s))
        if r.get("user_accepted"):
            accepted += 1
    return {
        "_v": SCHEMA_VERSION,
        "total_decisions": total,
        "by_command": by_cmd,
        "by_industry": by_industry,
        "by_ui_type": by_ui_type,
        "by_mode": by_mode,
        "top_brands": dict(sorted(by_brand.items(), key=lambda kv: -kv[1])[:20]),
        "lint_score_median": _median(scores),
        "lint_score_mean": (sum(scores) / len(scores)) if scores else None,
        "accepted_count": accepted,
        "acceptance_rate": (accepted / total) if total else None,
    }


def _median(xs: List[int]) -> Optional[float]:
    if not xs:
        return None
    s = sorted(xs)
    n = len(s)
    if n % 2 == 1:
        return float(s[n // 2])
    return (s[n // 2 - 1] + s[n // 2]) / 2
