"""Tests for the v2.1 evolve loop."""
from __future__ import annotations

import pytest

from engine.evolve import (
    evolve,
    EvolveResult,
    EvolveRound,
    MAX_ROUNDS,
    PLATEAU_DELTA,
    TARGET_SCORE,
    QUALITY_GATE,
)
from engine.evolve.core import (
    polish_strip_inline_styles,
    polish_replace_generic_ctas,
    polish_swap_placeholder_urls,
    polish_normalize_spacing,
    polish_strip_lorem_ipsum,
)


def test_constants_locked():
    """Public contracts for the loop knobs."""
    assert MAX_ROUNDS == 5
    assert PLATEAU_DELTA == 5
    assert TARGET_SCORE == 90
    assert QUALITY_GATE == 65


# ---------- individual polish passes ----------

def test_strip_inline_styles_removes_color():
    html = '<div style="color:red">x</div>'
    new, changed = polish_strip_inline_styles(html)
    assert "color:red" not in new
    assert changed is True


def test_strip_inline_styles_keeps_other_styles():
    """Only color/font-weight/text-align should be stripped."""
    html = '<div style="background: blue">x</div>'
    new, _ = polish_strip_inline_styles(html)
    assert "background: blue" in new


def test_strip_inline_styles_idempotent():
    """Running twice should produce no further change."""
    html = '<div style="color:red">x</div>'
    once, _ = polish_strip_inline_styles(html)
    twice, changed = polish_strip_inline_styles(once)
    assert changed is False


def test_replace_generic_ctas():
    html = "<button>Click here</button><a>Read more</a>"
    new, changed = polish_replace_generic_ctas(html)
    assert "Click here" not in new
    assert "Read more" not in new
    assert changed is True


def test_swap_placeholder_urls():
    html = '<img src="https://via.placeholder.com/300x200">'
    new, changed = polish_swap_placeholder_urls(html)
    assert "via.placeholder.com" not in new
    assert "data:image/svg" in new
    assert changed is True


def test_normalize_spacing_snaps_close_values():
    """7px → 8px (close to scale step)."""
    css = ".a { padding: 7px; gap: 25px; }"
    new, changed = polish_normalize_spacing(css)
    assert "8px" in new
    assert "24px" in new
    assert changed is True


def test_normalize_spacing_doesnt_snap_far_values():
    """A value not close to any scale step should NOT snap (preserve intent)."""
    # 200px is closest to 128px but ratio is too large
    css = ".x { width: 200px; }"
    new, _ = polish_normalize_spacing(css)
    assert "200px" in new


def test_strip_lorem_ipsum():
    html = "<p>Lorem ipsum dolor sit amet, consectetur.</p>"
    new, changed = polish_strip_lorem_ipsum(html)
    assert "Lorem ipsum" not in new
    assert "editorial copy" in new
    assert changed is True


# ---------- full loop ----------

def test_evolve_clean_input_stops_quickly():
    """Clean input → target hit on round 1 (no polish needed)."""
    html = "<main><h1>Hello</h1><h2>Subhead</h2></main>"
    css = ".ux-stack { display: flex; flex-direction: column; gap: 16px; }"
    res = evolve(
        html=html, css=css,
        synth_system={"axes": {"warmth": 0.5}},
        brief_axes={"warmth": 0.5},
        linter_score=100,
    )
    # Strong input scores high → should hit TARGET or plateau quickly
    assert res.final_score >= QUALITY_GATE
    assert res.above_gate is True
    # Should stop in <= MAX_ROUNDS
    assert len(res.rounds) <= MAX_ROUNDS


def test_evolve_dirty_input_polishes_through_loop():
    """Dirty input should be improved by polish passes."""
    html = '<div><span>Click here</span><img src="https://via.placeholder.com/300"></div>'
    css = ".a { padding: 7px; gap: 13px; font-weight: bold; }"
    res = evolve(
        html=html, css=css,
        synth_system={"axes": {"warmth": 0.5}},
        brief_axes={"warmth": 0.5},
        linter_score=80,
    )
    # Polish should have done SOMETHING
    all_polishes = []
    for r in res.rounds:
        all_polishes.extend(r.polishes_applied)
    assert len(all_polishes) > 0
    # Final output shouldn't contain the polish targets
    assert "Click here" not in res.final_html
    assert "via.placeholder" not in res.final_html


def test_evolve_returns_evolveresult():
    res = evolve(
        html="<main><h1>x</h1></main>",
        css=".a { padding: 16px; }",
        synth_system={"axes": {"warmth": 0.5}},
        brief_axes={"warmth": 0.5},
        linter_score=100,
    )
    assert isinstance(res, EvolveResult)
    assert isinstance(res.rounds, list)
    assert res.stopped_reason in ("target_hit", "plateau", "max_rounds", "gate_failed")


def test_evolve_caps_at_max_rounds():
    """Loop never exceeds MAX_ROUNDS."""
    res = evolve(
        html="",  # empty → nothing to polish, plateau immediately
        css="",
        synth_system={"axes": {}},
        brief_axes={},
        linter_score=50,
    )
    assert len(res.rounds) <= MAX_ROUNDS


def test_evolve_force_flag_overrides_gate():
    """force=True keeps above_gate=False but doesn't change stop logic."""
    res = evolve(
        html="",
        css="",
        synth_system={"axes": {}},
        brief_axes={},
        linter_score=10,
        force=True,
    )
    # Below gate, forced should be True if quality fails
    assert res.forced is True


def test_evolve_to_dict_serializable():
    res = evolve(
        html="<main><h1>x</h1></main>",
        css=".a { padding: 16px; }",
        synth_system={"axes": {"warmth": 0.5}},
        brief_axes={"warmth": 0.5},
        linter_score=95,
    )
    d = res.to_dict()
    assert "initial_score" in d
    assert "final_score" in d
    assert "rounds" in d
    assert "stopped_reason" in d
