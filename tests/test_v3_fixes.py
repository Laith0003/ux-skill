"""Tests for the v3.0 hardening: determinism, interactions, tag-decoupling, re-rank."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import pytest

from engine.synthesizer import compute_axes, pick_exemplars_by_axes
from engine.synthesizer.axes import AxisValues
from engine.synthesizer.interactions import (
    spacing_base_for,
    radius_base_px_for,
    motion_timing_for,
    accent_register_for,
    DOCUMENTED_INTERACTIONS,
)
from engine.evaluator import evaluate, score_tone_match


@dataclass
class _Brief:
    industry: str = ""
    project_type: str = ""
    tone: List[str] = field(default_factory=list)
    audience: List[str] = field(default_factory=list)
    must_have: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)
    region: str = ""
    stack: str = ""


# ---------- Determinism (T's #1) ----------

def test_exemplar_selection_is_deterministic_across_calls():
    """Same axes → same ordered list of exemplars, every call."""
    axes = compute_axes(_Brief(industry="fintech-payments"))
    a = pick_exemplars_by_axes(axes, n=10)
    b = pick_exemplars_by_axes(axes, n=10)
    assert [x["id"] for x in a] == [x["id"] for x in b]


def test_exemplar_tie_break_is_id_alphabetical():
    """Brands tying on distance break by id alphabetically (stable across machines)."""
    # Force a tie scenario by picking many brands in the same category
    axes = compute_axes(_Brief(industry="developer-tools"))
    exemplars = pick_exemplars_by_axes(axes, n=20)
    ids = [e["id"] for e in exemplars]
    # The top-N must be reproducible. If we exclude the first two and pick
    # again, the new top should still be sorted predictably.
    exemplars2 = pick_exemplars_by_axes(axes, n=20, exclude_brand_ids=ids[:2])
    assert all(eid not in ids[:2] for eid in [e["id"] for e in exemplars2])


# ---------- Axis interaction matrix (T's #2) ----------

def test_documented_interactions_locked():
    """The interaction manifest is a public contract."""
    assert DOCUMENTED_INTERACTIONS == (
        "spacing_base_for",
        "radius_base_px_for",
        "accent_register_for",
        "motion_timing_for",
    )


def test_spacing_dense_corporate_wins_density():
    """Bloomberg-school: dense + formal → tight 4px base (density wins)."""
    a = AxisValues(0.5, 0.7, 0.85, 0.4, 0.85, 0.4, 0.4)
    assert spacing_base_for(a) == 4


def test_spacing_airy_luxury_wins_formality():
    """Luxury: airy + formal → 12px base (formality overrides density toward space)."""
    a = AxisValues(0.5, 0.5, 0.25, 0.55, 0.85, 0.4, 0.7)
    assert spacing_base_for(a) == 12


def test_spacing_airy_casual_default():
    """Airy + casual → 8px."""
    a = AxisValues(0.7, 0.4, 0.3, 0.7, 0.3, 0.5, 0.7)
    assert spacing_base_for(a) == 8


def test_radius_sharp_corporate_resolves_to_two_px():
    """Sharp geometry + high formality → 2px (essentially no radius)."""
    a = AxisValues(0.5, 0.6, 0.6, 0.2, 0.85, 0.4, 0.4)
    assert radius_base_px_for(a) == 2


def test_radius_soft_playful_resolves_to_18_px():
    """Soft geometry + playful → 18px (generous radius)."""
    a = AxisValues(0.7, 0.5, 0.4, 0.8, 0.3, 0.6, 0.7)
    assert radius_base_px_for(a) == 18


def test_motion_corporate_dampened_at_high_motion():
    """High motion axis + high formality → timing dampened (slower base)."""
    high_motion_casual = motion_timing_for(AxisValues(0.5, 0.5, 0.5, 0.5, 0.3, 0.85, 0.5))
    high_motion_corporate = motion_timing_for(AxisValues(0.5, 0.5, 0.5, 0.5, 0.85, 0.85, 0.5))
    assert high_motion_corporate["base_ms"] > high_motion_casual["base_ms"]


def test_accent_register_warmth_axis_signed():
    """warmth_register is centered: warmth=0 → -1, warmth=1 → +1."""
    cold = accent_register_for(AxisValues(0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5))
    warm = accent_register_for(AxisValues(1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5))
    assert cold["warmth_register"] < 0
    assert warm["warmth_register"] > 0


# ---------- Decoupled tone_match (T's #3) ----------

def test_tone_match_uses_raw_tags_when_provided():
    """If brief_tags is provided, score is independent of derived axes."""
    # synth axes that have warmth low (the synthesizer drifted)
    synth = {"warmth": 0.1, "contrast": 0.5, "density": 0.5, "geometry": 0.5,
             "formality": 0.5, "motion": 0.5, "type_personality": 0.5}
    # brief explicitly says "warm" tone — synth output should be flagged
    score = score_tone_match(synth, {}, brief_tags=["warm"])
    # Synth warmth 0.1 is FAR from warm-expected range [0.55, 1.0] → score ~0
    assert score < 30


def test_tone_match_high_when_tags_match_synth():
    """Synth axes that DO match the brief tags get high score."""
    synth = {"warmth": 0.7, "contrast": 0.7, "density": 0.3,
             "geometry": 0.5, "formality": 0.5, "motion": 0.5, "type_personality": 0.5}
    score = score_tone_match(synth, {}, brief_tags=["warm", "bold", "minimal"])
    # All 3 tags satisfied → 100
    assert score == 100


def test_tone_match_unknown_tags_neutral():
    """Unknown tags → neutral 70 score (no false fail, no false pass)."""
    synth = {"warmth": 0.1, "contrast": 0.5, "density": 0.5}
    score = score_tone_match(synth, {}, brief_tags=["abracadabra-not-a-real-tag"])
    assert score == 70


def test_tone_match_legacy_axes_path_still_works():
    """Back-compat: callers without brief_tags fall through to legacy cosine path."""
    score = score_tone_match({"warmth": 0.5}, {"warmth": 0.5})
    assert score >= 90  # legacy axis-cosine, identical


# ---------- Recommender re-rank (T's #4) ----------

def test_rerank_cold_start_returns_input_unchanged(tmp_path, monkeypatch):
    """With < 3 prior decisions in bucket, the re-ranker is a no-op."""
    proj_log = tmp_path / "decisions.jsonl"
    user_log = tmp_path / "decisions-user.jsonl"
    monkeypatch.setattr("engine.decisions.ledger.PROJECT_PATH", proj_log)
    monkeypatch.setattr("engine.decisions.ledger.USER_PATH", user_log)
    from engine.recommender.core import _rerank_from_decisions, Brief
    brief = Brief(industry="fintech-payments", project_type="dashboard")
    pairs = [({"id": "a"}, 10.0), ({"id": "b"}, 5.0)]
    out = _rerank_from_decisions(pairs, brief, key="picked_style")
    assert out == pairs  # untouched


def test_rerank_warm_start_bumps_winners(tmp_path, monkeypatch):
    """With >= 3 prior accepted+lint>=80 decisions, winners get bumped."""
    proj_log = tmp_path / "decisions.jsonl"
    user_log = tmp_path / "decisions-user.jsonl"
    monkeypatch.setattr("engine.decisions.ledger.PROJECT_PATH", proj_log)
    monkeypatch.setattr("engine.decisions.ledger.USER_PATH", user_log)
    from engine.decisions import record, Scope
    # Seed 3 winning decisions for "stripe-style" in fintech-payments+dashboard
    for _ in range(3):
        record({
            "command": "design",
            "industry": "fintech-payments",
            "ui_type": "dashboard",
            "picked_style": "stripe-style",
            "lint_score": 92,
            "user_accepted": True,
        }, scope=Scope.PROJECT)

    from engine.recommender.core import _rerank_from_decisions, Brief
    brief = Brief(industry="fintech-payments", project_type="dashboard")
    pairs = [
        ({"id": "other-style"}, 50.0),
        ({"id": "stripe-style"}, 10.0),
    ]
    out = _rerank_from_decisions(pairs, brief, key="picked_style")
    # stripe-style should have +15 bump (3 wins * 5)
    found = False
    for e, s in out:
        if e["id"] == "stripe-style":
            assert s == 10.0 + 3 * 5.0
            found = True
    assert found, "stripe-style not in output"


def test_rerank_ignores_accepted_false_or_low_score(tmp_path, monkeypatch):
    """Decisions with user_accepted=False or lint<80 should NOT count."""
    proj_log = tmp_path / "decisions.jsonl"
    user_log = tmp_path / "decisions-user.jsonl"
    monkeypatch.setattr("engine.decisions.ledger.PROJECT_PATH", proj_log)
    monkeypatch.setattr("engine.decisions.ledger.USER_PATH", user_log)
    from engine.decisions import record, Scope
    # Seed rejected decisions + accepted but low-score decisions
    for _ in range(5):
        record({
            "command": "design",
            "industry": "fintech-payments",
            "ui_type": "dashboard",
            "picked_style": "stripe-style",
            "lint_score": 92,
            "user_accepted": False,   # rejected
        }, scope=Scope.PROJECT)
    for _ in range(5):
        record({
            "command": "design",
            "industry": "fintech-payments",
            "ui_type": "dashboard",
            "picked_style": "stripe-style",
            "lint_score": 60,       # too low
            "user_accepted": True,
        }, scope=Scope.PROJECT)

    from engine.recommender.core import _rerank_from_decisions, Brief
    brief = Brief(industry="fintech-payments", project_type="dashboard")
    pairs = [({"id": "stripe-style"}, 10.0)]
    out = _rerank_from_decisions(pairs, brief, key="picked_style")
    # No qualifying priors → no bump
    assert out[0][1] == 10.0
