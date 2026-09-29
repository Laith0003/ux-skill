"""Page-level section sequences: pick a whole-page skeleton from a 4.0 brief.

``select_for_brief`` reads the brief's structured fields only, never its
industry or its prose, and drops a proof section the client cannot fill with
a stated reason instead of inventing proof.

Public surface:
    select_for_brief(brief) -> dict
    select_sequence(sequence_id) -> Optional[dict]
    load_sequences() -> list
"""
from engine.page_sequence.core import load_sequences, select_for_brief, select_sequence

__all__ = ["load_sequences", "select_for_brief", "select_sequence"]
