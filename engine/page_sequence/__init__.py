"""Page-level section sequences: pick a whole-page skeleton from a 4.0 brief.

``select_for_brief`` reads the brief's structured fields first and its
phrases second, never a single call-to-action verb, and drops a proof section
the client cannot fill with a stated reason instead of inventing proof.

Public surface:
    select_for_brief(brief) -> Optional[dict]
    select_sequence(goal_or_keywords) -> Optional[dict]
    score_sequence(entry, query_tokens, raw_query) -> float
    load_sequences() -> list
"""
from engine.page_sequence.core import (
    select_for_brief, select_sequence, score_sequence, load_sequences,
)

__all__ = ["select_for_brief", "select_sequence", "score_sequence", "load_sequences"]
