"""The AI rule pack: decision records, per-foundation guidance, and the
generator that writes, per foundation, architecture rules, a reference of
the built tokens, an audit procedure and a handoff contract.

records reads and checks the decision records in decisions/.
"""
from engine.rulepack.records import (
    AREAS, CORRECTION_WORDS, HEADINGS, RECORDS_DIR, Record, RecordError, RecordProblem,
    check_folder, history_problems, load_records, read_record, record_sources)

__all__ = [
    "AREAS", "CORRECTION_WORDS", "HEADINGS", "RECORDS_DIR", "Record", "RecordError",
    "RecordProblem", "check_folder", "history_problems", "load_records", "read_record",
    "record_sources",
]
