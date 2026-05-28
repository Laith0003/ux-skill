"""Tests for the v2.1 evaluation engine."""
from __future__ import annotations

import pytest

from engine.evaluator import (
    evaluate,
    Evaluation,
    THRESHOLD,
    AXES,
    score_hierarchy,
    score_layout_coherence,
    score_spacing,
    score_readability,
    score_tone_match,
    score_uniqueness,
)


def test_threshold_locked_at_65():
    """Quality gate threshold is a public contract."""
    assert THRESHOLD == 65


def test_axes_locked():
    """The 7 axes are a public contract."""
    assert AXES == (
        "linter_score", "hierarchy_clarity", "layout_coherence",
        "spacing_consistency", "usability_readability",
        "tone_match", "uniqueness",
    )


# ---------- hierarchy ----------

def test_hierarchy_perfect():
    """Single H1 + H2 + H3 → high score."""
    html = "<h1>Title</h1><h2>Section</h2><h3>Sub</h3>"
    assert score_hierarchy(html) >= 90


def test_hierarchy_missing_h1():
    """No H1 = -25."""
    html = "<h2>Section</h2><h3>Sub</h3>"
    assert score_hierarchy(html) < 80


def test_hierarchy_multiple_h1_penalty():
    """Two H1s penalized."""
    html = "<h1>One</h1><h1>Two</h1><h2>OK</h2>"
    assert score_hierarchy(html) < 95


def test_hierarchy_skip_h1_to_h3_penalty():
    """H1 → H3 without H2 penalized."""
    perfect = score_hierarchy("<h1>A</h1><h2>B</h2><h3>C</h3>")
    skipped = score_hierarchy("<h1>A</h1><h3>C</h3>")
    assert skipped < perfect


# ---------- layout coherence ----------

def test_layout_coherence_clean():
    """Clean CSS scores high."""
    css = ".ux-stack { display: flex; flex-direction: column; gap: 1rem; }"
    assert score_layout_coherence("<div class='ux-stack'>x</div>", css) >= 90


def test_layout_coherence_big_widths_penalty():
    """Huge fixed-px widths get docked."""
    css = ".x { width: 1600px; } .y { width: 1800px; }"
    assert score_layout_coherence("<div>x</div>", css) < 90


def test_layout_coherence_inline_style_spam_penalty():
    """Excessive inline styles get docked."""
    html = "".join(f'<div style="color:red">{i}</div>' for i in range(30))
    # 30 inline styles → 20 over the threshold → -20 → score should be < 90
    assert score_layout_coherence(html, "") < 90


# ---------- spacing ----------

def test_spacing_on_scale():
    """All px values on the 8pt scale → high score."""
    css = ".a { padding: 16px; margin: 24px; gap: 8px; }"
    assert score_spacing(css) >= 90


def test_spacing_off_scale():
    """Random magic numbers → lower score."""
    css = ".a { padding: 13px; margin: 27px; gap: 7px; }"
    assert score_spacing(css) <= 70


# ---------- readability ----------

def test_readability_tiny_font_penalty():
    """font-size: 10px should drop the score."""
    css = "body { font-size: 10px; }"
    assert score_readability(css) < 95


def test_readability_thin_body_weight_penalty():
    """font-weight 100 on body should drop the score."""
    css = "body { font-weight: 100; font-size: 16px; }"
    assert score_readability(css) < 95


# ---------- tone match ----------

def test_tone_match_identical_axes():
    """Synth axes identical to brief axes → 100."""
    a = {"warmth": 0.5, "contrast": 0.5}
    assert score_tone_match(a, a) == 100


def test_tone_match_distant_axes():
    """Synth far from brief → lower score."""
    s = {"warmth": 0.0, "contrast": 0.0}
    b = {"warmth": 1.0, "contrast": 1.0}
    assert score_tone_match(s, b) < 50


# ---------- uniqueness ----------

def test_uniqueness_no_prior_history():
    """No prior decisions → default 80 (novel by absence)."""
    assert score_uniqueness({"warmth": 0.5}, prior_decisions=None) == 80


def test_uniqueness_near_duplicate_penalty():
    """Near-duplicate of prior → low uniqueness."""
    prior = [{"axes": {"warmth": 0.5, "contrast": 0.5}}]
    s = {"warmth": 0.5, "contrast": 0.5}
    score = score_uniqueness(s, prior_decisions=prior)
    assert score <= 50


def test_uniqueness_far_from_prior():
    """Very different from prior → high uniqueness."""
    prior = [{"axes": {"warmth": 0.0, "contrast": 0.0}}]
    s = {"warmth": 1.0, "contrast": 1.0}
    score = score_uniqueness(s, prior_decisions=prior)
    assert score >= 80


# ---------- composite evaluate ----------

def test_evaluate_returns_all_axes():
    """evaluate() populates every axis."""
    ev = evaluate(
        html="<main><h1>Hello</h1></main>",
        css=".ux-stack { display: flex; flex-direction: column; gap: 1rem; }",
        synth_system={"axes": {"warmth": 0.5}, "palette": {"canvas": "#000"}},
        brief_axes={"warmth": 0.5},
        linter_score=95,
    )
    for axis in AXES:
        assert hasattr(ev, axis), f"missing axis {axis}"


def test_evaluate_composite_is_mean():
    """Composite is the mean of the 7 axes."""
    ev = evaluate(
        html="<h1>x</h1><h2>y</h2>",
        css=".a { padding: 16px; }",
        synth_system={"axes": {"warmth": 0.5}},
        brief_axes={"warmth": 0.5},
        linter_score=100,
    )
    # Should be > 50 for clean inputs
    assert ev.composite >= 60


def test_evaluate_above_threshold_flag():
    """above_threshold True iff composite >= 65."""
    ev = evaluate(
        html="<main><h1>OK</h1></main>",
        css=".a { padding: 16px; }",
        synth_system={"axes": {"warmth": 0.5}},
        brief_axes={"warmth": 0.5},
        linter_score=100,
    )
    assert ev.above_threshold == (ev.composite >= THRESHOLD)


def test_evaluate_notes_populated_on_failures():
    """Failure modes generate diagnostic notes."""
    ev = evaluate(
        html="",  # no headings → hierarchy will be low
        css="body { font-size: 9px; font-weight: 100; }",  # readability fails
        synth_system={"axes": {"warmth": 0.0}},
        brief_axes={"warmth": 1.0},  # tone mismatch
        linter_score=30,  # linter low
    )
    assert len(ev.notes) > 0
