"""Tests for the v2.1 decisions ledger.

Verifies:
- Schema lock: every record contains the required columns
- Default values for missing fields
- Offline-only writes (no network ever touched)
- ``UXSKILL_NO_LOG`` env var disables logging
- ``record`` + ``read_all`` round-trips
- ``query`` filters correctly
- ``stats`` aggregates correctly
- Scope.PROJECT / Scope.USER / Scope.BOTH all honored
- Forward-compat: lines with future _v are skipped on read
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from engine.decisions import (
    DecisionSchema,
    SCHEMA_VERSION,
    Scope,
    record,
    read_all,
    query,
    stats,
)
from engine.decisions.ledger import (
    hash_brief,
    hash_context,
    _normalize,
)


# ---------- Fixtures ----------

@pytest.fixture
def tmp_log(tmp_path, monkeypatch):
    """Redirect PROJECT_PATH + USER_PATH to a tmp dir for isolation."""
    proj = tmp_path / "proj" / ".ux" / "decisions.jsonl"
    user = tmp_path / "user" / ".uxskill" / "decisions.jsonl"
    monkeypatch.setattr("engine.decisions.ledger.PROJECT_PATH", proj)
    monkeypatch.setattr("engine.decisions.ledger.USER_PATH", user)
    monkeypatch.delenv("UXSKILL_NO_LOG", raising=False)
    return proj, user


# ---------- Schema lock ----------

def test_schema_version_is_one():
    """The locked schema version is 1. Tests fail if anyone bumps without thought."""
    assert SCHEMA_VERSION == 1


def test_schema_required_columns():
    """Required columns are a public contract. Renaming = breaking change."""
    schema = DecisionSchema()
    required = set(schema.required)
    expected = {
        "_v", "ts", "command", "brief_id", "context_hash",
        "industry", "ui_type", "mode",
        "picked_brand", "picked_style", "picked_palette",
        "axes", "lint_score", "lint_high", "lint_med", "lint_low",
        "artifact_path", "user_accepted", "duration_ms",
    }
    assert required == expected, "Schema columns drifted — breaking change!"


def test_normalize_fills_defaults():
    """Missing fields get default values."""
    out = _normalize({"command": "recommend"})
    for col in DecisionSchema().required:
        assert col in out, f"missing {col}"
    assert out["_v"] == 1
    assert out["command"] == "recommend"
    assert out["brief_id"] == "ad-hoc"
    assert out["lint_high"] == 0
    assert out["user_accepted"] is None


# ---------- Hashing ----------

def test_hash_brief_stable():
    """Same brief → same hash."""
    a = hash_brief("build a fintech dashboard")
    b = hash_brief("build a fintech dashboard")
    assert a == b
    assert len(a) == 16


def test_hash_brief_different():
    """Different briefs → different hashes."""
    a = hash_brief("build a fintech dashboard")
    b = hash_brief("build a healthcare app")
    assert a != b


def test_hash_context_case_insensitive():
    """Context hashing is lowercase-stable."""
    a = hash_context("Fintech", "Dashboard", "Serious", "Next.js")
    b = hash_context("fintech", "dashboard", "serious", "next.js")
    assert a == b


# ---------- Write / read round-trip ----------

def test_record_writes_to_both_scopes(tmp_log):
    proj, user = tmp_log
    decision = {"command": "recommend", "industry": "fintech", "ui_type": "dashboard"}
    ok = record(decision, scope=Scope.BOTH)
    assert ok
    assert proj.exists()
    assert user.exists()
    # Each file should have exactly one line.
    assert proj.read_text(encoding="utf-8").strip().count("\n") == 0
    assert user.read_text(encoding="utf-8").strip().count("\n") == 0


def test_record_scope_project_only(tmp_log):
    proj, user = tmp_log
    record({"command": "lint"}, scope=Scope.PROJECT)
    assert proj.exists()
    assert not user.exists()


def test_record_scope_user_only(tmp_log):
    proj, user = tmp_log
    record({"command": "lint"}, scope=Scope.USER)
    assert not proj.exists()
    assert user.exists()


def test_no_log_env_var_disables(tmp_log, monkeypatch):
    proj, user = tmp_log
    monkeypatch.setenv("UXSKILL_NO_LOG", "1")
    ok = record({"command": "recommend"})
    assert ok is False
    assert not proj.exists()
    assert not user.exists()


def test_read_all_round_trip(tmp_log):
    record({"command": "recommend", "industry": "fintech"}, scope=Scope.PROJECT)
    record({"command": "design", "industry": "healthcare"}, scope=Scope.PROJECT)
    rows = read_all(scope=Scope.PROJECT)
    assert len(rows) == 2
    cmds = {r["command"] for r in rows}
    assert cmds == {"recommend", "design"}
    # Every row carries _v.
    for r in rows:
        assert r["_v"] == 1


def test_read_skips_future_schema(tmp_log):
    proj, _ = tmp_log
    proj.parent.mkdir(parents=True, exist_ok=True)
    # Hand-write one row at a future schema version.
    proj.write_text(
        json.dumps({"_v": 2, "command": "future"}) + "\n"
        + json.dumps({"_v": 1, "command": "now"}) + "\n",
        encoding="utf-8",
    )
    rows = read_all(scope=Scope.PROJECT)
    assert len(rows) == 1
    assert rows[0]["command"] == "now"


# ---------- Query ----------

def test_query_filters_by_industry(tmp_log):
    record({"command": "recommend", "industry": "fintech"}, scope=Scope.PROJECT)
    record({"command": "recommend", "industry": "healthcare"}, scope=Scope.PROJECT)
    record({"command": "recommend", "industry": "fintech"}, scope=Scope.PROJECT)
    rows = query(industry="fintech", scope=Scope.PROJECT)
    assert len(rows) == 2


def test_query_filters_by_command(tmp_log):
    record({"command": "recommend"}, scope=Scope.PROJECT)
    record({"command": "lint"}, scope=Scope.PROJECT)
    record({"command": "design"}, scope=Scope.PROJECT)
    rows = query(command="lint", scope=Scope.PROJECT)
    assert len(rows) == 1
    assert rows[0]["command"] == "lint"


def test_query_filters_by_min_score(tmp_log):
    record({"command": "lint", "lint_score": 90}, scope=Scope.PROJECT)
    record({"command": "lint", "lint_score": 40}, scope=Scope.PROJECT)
    record({"command": "lint", "lint_score": 65}, scope=Scope.PROJECT)
    rows = query(min_score=65, scope=Scope.PROJECT)
    assert len(rows) == 2
    assert all(r["lint_score"] >= 65 for r in rows)


def test_query_filters_accepted_only(tmp_log):
    record({"command": "design", "user_accepted": True}, scope=Scope.PROJECT)
    record({"command": "design", "user_accepted": False}, scope=Scope.PROJECT)
    record({"command": "design", "user_accepted": None}, scope=Scope.PROJECT)
    rows = query(accepted_only=True, scope=Scope.PROJECT)
    assert len(rows) == 1
    assert rows[0]["user_accepted"] is True


def test_query_limit(tmp_log):
    for _ in range(10):
        record({"command": "recommend"}, scope=Scope.PROJECT)
    rows = query(limit=3, scope=Scope.PROJECT)
    assert len(rows) == 3


# ---------- Stats ----------

def test_stats_aggregates_correctly(tmp_log):
    record({"command": "recommend", "industry": "fintech", "picked_brand": "stripe",
            "lint_score": 90}, scope=Scope.PROJECT)
    record({"command": "recommend", "industry": "fintech", "picked_brand": "stripe",
            "lint_score": 80, "user_accepted": True}, scope=Scope.PROJECT)
    record({"command": "design", "industry": "healthcare", "lint_score": 50},
           scope=Scope.PROJECT)
    s = stats(scope=Scope.PROJECT)
    assert s["total_decisions"] == 3
    assert s["by_command"]["recommend"] == 2
    assert s["by_command"]["design"] == 1
    assert s["by_industry"]["fintech"] == 2
    assert s["top_brands"]["stripe"] == 2
    assert s["accepted_count"] == 1
    assert s["acceptance_rate"] == 1 / 3
    # Median of [50, 80, 90] = 80
    assert s["lint_score_median"] == 80


def test_stats_empty(tmp_log):
    s = stats(scope=Scope.PROJECT)
    assert s["total_decisions"] == 0
    assert s["lint_score_median"] is None
    assert s["acceptance_rate"] is None
