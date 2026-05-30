"""Deterministic page-level section-sequence selector.

Picks a whole-page template (from ``data/page-sequences.json``) by GOAL or by a
free-text brief. The chosen sequence is the page skeleton the build flow expands:
every ordered section gets rendered, ALL source content is mapped into it, and the
goal's conversion mechanisms are included. This is the page-level complement to
``data/landing-patterns.json`` (which is section-level).

Pure ``dict -> dict``. No LLM, no network, fully deterministic: the same query
always returns the same sequence, and ties are broken by manifest order.

Public surface
--------------
``select_sequence(goal_or_keywords) -> Optional[Dict]``  -- best-matching entry
``score_sequence(entry, tokens, raw) -> float``          -- the match score (exposed for tests)
``load_sequences() -> List[Dict]``                       -- raw manifest entries
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Union

from engine.data_loader import load


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def load_sequences() -> List[Dict[str, Any]]:
    """Return the page-sequence entries from the manifest (empty list if absent)."""
    payload = load("page-sequences")
    entries = payload.get("entries", [])
    return entries if isinstance(entries, list) else []


def _tokenize(text: str) -> List[str]:
    """Lowercase word/number tokens from arbitrary text."""
    return _TOKEN_RE.findall((text or "").lower())


def _normalize_query(goal_or_keywords: Union[str, List[str], None]):
    """Return ``(raw_lower, token_set)`` for a string or list-of-strings query."""
    if goal_or_keywords is None:
        return "", set()
    if isinstance(goal_or_keywords, (list, tuple)):
        raw = " ".join(str(x) for x in goal_or_keywords)
    else:
        raw = str(goal_or_keywords)
    raw_lower = raw.strip().lower()
    return raw_lower, set(_tokenize(raw_lower))


def score_sequence(entry: Dict[str, Any], query_tokens: set, raw_query: str) -> float:
    """Score one entry against a normalized query. Higher is a better match.

    Signal (additive, deterministic):
      * exact goal/id match            -> strong base (100)
      * goal string is a substring of  -> (50) e.g. brief mentions "lead-gen-service"
        the raw query, or vice versa
      * keyword phrase appears in raw   -> +6 per keyword phrase found as a substring
      * token overlap (query tokens vs  -> +2 per shared token (keywords + goal)
        the entry's keyword/goal tokens)
    """
    goal = str(entry.get("goal") or entry.get("id") or "").strip().lower()
    keywords = [str(k).strip().lower() for k in (entry.get("keywords") or [])]

    score = 0.0
    if goal and (goal == raw_query or goal in query_tokens):
        score += 100.0
    elif goal and raw_query and (goal in raw_query or raw_query in goal):
        score += 50.0

    # Phrase hits: a keyword that appears verbatim in the raw query.
    for kw in keywords:
        if kw and raw_query and kw in raw_query:
            score += 6.0

    # Token overlap against the entry's vocabulary (keyword + goal tokens).
    entry_tokens: set = set()
    for kw in keywords:
        entry_tokens.update(_tokenize(kw))
    entry_tokens.update(_tokenize(goal))
    score += 2.0 * len(query_tokens & entry_tokens)

    return score


def select_sequence(goal_or_keywords: Union[str, List[str], None]) -> Optional[Dict[str, Any]]:
    """Return the best-matching page sequence for a goal id or a free-text brief.

    Deterministic: entries are scored, the highest score wins, and ties are broken
    by manifest order (first defined wins). Returns ``None`` when there are no
    entries or nothing scores above zero (no signal -> no opinion).
    """
    entries = load_sequences()
    if not entries:
        return None

    raw_query, query_tokens = _normalize_query(goal_or_keywords)
    if not raw_query:
        return None

    best: Optional[Dict[str, Any]] = None
    best_score = 0.0
    # Iterate in manifest order so ties resolve to the earlier-defined entry.
    for entry in entries:
        s = score_sequence(entry, query_tokens, raw_query)
        if s > best_score:
            best_score = s
            best = entry

    return best if best_score > 0 else None
