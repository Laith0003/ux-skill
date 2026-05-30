"""Page-level section sequences — pick a whole-page skeleton by goal.

The build flow selects a sequence by goal/keywords, then expands the full
ordered section list and maps all source content into it (every sector -> a
pill, every size -> a card, every benefit -> a checklist item) with a relevant
inline SVG icon per item and the goal's conversion mechanisms.

Public surface:
    select_sequence(goal_or_keywords) -> Optional[dict]
    score_sequence(entry, query_tokens, raw_query) -> float
    load_sequences() -> list
"""
from engine.page_sequence.core import (
    select_sequence, score_sequence, load_sequences,
)

__all__ = ["select_sequence", "score_sequence", "load_sequences"]
