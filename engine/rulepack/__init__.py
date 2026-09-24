"""The AI rule pack: decision records, per-foundation guidance, and the
generator that writes, per foundation, architecture rules, a reference of
the built tokens, an audit procedure and a handoff contract.

records reads and checks the decision records in decisions/. guidance
reads the per-foundation guidance in guidance/ and builds the role
catalog from it.
"""
from engine.rulepack.guidance import (
    GUIDANCE_DIR, SECTIONS, SHARED, Guidance, GuidanceError, RoleEntry, describe,
    guidance_problems, load_guidance, read_guidance, role_catalog)
from engine.rulepack.records import (
    AREAS, CORRECTION_WORDS, HEADINGS, RECORDS_DIR, Record, RecordError, RecordProblem,
    check_folder, history_problems, load_records, read_record, record_sources)

__all__ = [
    "AREAS", "CORRECTION_WORDS", "GUIDANCE_DIR", "Guidance", "GuidanceError", "HEADINGS",
    "RECORDS_DIR", "Record", "RecordError", "RecordProblem", "RoleEntry", "SECTIONS", "SHARED",
    "check_folder", "describe", "guidance_problems", "history_problems", "load_guidance",
    "load_records", "read_guidance", "read_record", "record_sources", "role_catalog",
]
