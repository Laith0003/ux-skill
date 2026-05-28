"""Decisions ledger — append-only JSONL learning substrate for ux-skill v2.1.

Every command call (recommend, design, lint, evolve, system) writes one line
to ``.ux/decisions.jsonl``. The recommender re-reads this file to re-rank
candidates based on what worked before in similar contexts.

**Offline. Deterministic. No LLM. No telemetry. No network.**

Schema is locked at ``_v: 1``. Column names are a public contract — never
rename, only add (with default value = null for compat readers).

Public surface
--------------
``record(decision: dict) -> None``       — append one decision
``read_all(scope=BOTH) -> list[dict]``   — read everything
``query(bucket=..., limit=...) -> list`` — filtered read
``stats() -> dict``                      — aggregate counters
``SCHEMA_VERSION``                       — current schema int
"""
from engine.decisions.ledger import (
    record,
    read_all,
    query,
    stats,
    SCHEMA_VERSION,
    PROJECT_PATH,
    USER_PATH,
    Scope,
    DecisionSchema,
)

__all__ = [
    "record",
    "read_all",
    "query",
    "stats",
    "SCHEMA_VERSION",
    "PROJECT_PATH",
    "USER_PATH",
    "Scope",
    "DecisionSchema",
]
