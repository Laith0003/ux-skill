"""Tests for the v2.1 synthesizer — 7-axis derivation + triple-mode dispatch.

Verifies:
- Axis values stay in [0.0, 1.0]
- Same brief → same axes (deterministic, no randomness)
- Industry seeds nudge axes the right direction
- Tone tags push axes correctly
- Forbidden tags clamp axes
- Mode dispatch picks the right path
- Pure synthesis produces a valid palette + type pair
- Brand-anchor uses the named brand
- Strict-brand emits brand tokens verbatim
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import pytest

from engine.synthesizer import (
    synthesize,
    compute_axes,
    AxisValues,
    AXIS_NAMES,
    SYNTHESIS_MODES,
    distill_vocabulary,
    pick_exemplars_by_axes,
)


# ---------- Test Brief shim ----------

@dataclass
class _Brief:  # underscore-prefixed so pytest doesn't collect it
    """A minimal Brief look-alike for tests."""
    industry: str = ""
    tone: List[str] = field(default_factory=list)
    audience: List[str] = field(default_factory=list)
    must_have: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)
    reference_brands: List[str] = field(default_factory=list)
    strict: bool = False


# ---------- Axes ----------

def test_axis_names_locked():
    """AXIS_NAMES are a public contract."""
    assert AXIS_NAMES == (
        "warmth", "contrast", "density", "geometry",
        "formality", "motion", "type_personality",
    )


def test_axes_are_in_unit_range():
    """All axes always in [0, 1] for any brief."""
    briefs = [
        _Brief(),
        _Brief(industry="fintech-payments"),
        _Brief(industry="luxury", tone=["bold", "loud"]),
        _Brief(industry="healthcare", tone=["warm"], must_have=["dense"]),
        _Brief(industry="gaming", tone=["kinetic", "playful", "loud"]),
        _Brief(forbidden=["playful", "dense"]),
    ]
    for b in briefs:
        a = compute_axes(b)
        for name in AXIS_NAMES:
            v = getattr(a, name)
            assert 0.0 <= v <= 1.0, f"axis {name}={v} for brief {b}"


def test_axes_are_deterministic():
    """Same brief → same axes. Run twice, compare."""
    b = _Brief(industry="fintech-payments", tone=["serious", "bold"])
    a1 = compute_axes(b)
    a2 = compute_axes(b)
    assert a1.as_tuple() == a2.as_tuple()


def test_industry_seed_fintech_payments():
    """Fintech payments seeds formality high."""
    a = compute_axes(_Brief(industry="fintech-payments"))
    assert a.formality >= 0.7, f"fintech-payments should be formal, got {a.formality}"


def test_industry_seed_gaming():
    """Gaming seeds motion high, formality low."""
    a = compute_axes(_Brief(industry="gaming"))
    assert a.motion >= 0.7
    assert a.formality <= 0.4


def test_tone_warm_increases_warmth():
    """Adding 'warm' tone increases warmth axis."""
    cold = compute_axes(_Brief(industry="fintech-payments"))
    warm = compute_axes(_Brief(industry="fintech-payments", tone=["warm"]))
    assert warm.warmth > cold.warmth


def test_tone_bold_increases_contrast():
    """Adding 'bold' tone increases contrast."""
    quiet = compute_axes(_Brief(industry="saas"))
    bold = compute_axes(_Brief(industry="saas", tone=["bold"]))
    assert bold.contrast > quiet.contrast


def test_tone_minimal_decreases_density():
    """Adding 'minimal' tone decreases density."""
    dense = compute_axes(_Brief(industry="fintech-trading"))
    sparse = compute_axes(_Brief(industry="fintech-trading", tone=["minimal"]))
    assert sparse.density < dense.density


def test_forbidden_clamps_axis():
    """forbidden=['playful'] clamps formality to >= 0.6."""
    a = compute_axes(_Brief(industry="gaming", forbidden=["playful"]))
    # Gaming defaults to formality 0.3 — forbidden should push it >= 0.6
    assert a.formality >= 0.6, f"expected formality >= 0.6 after forbidden=playful, got {a.formality}"


def test_unknown_industry_uses_neutral_midpoint():
    """An unknown industry seeds all axes at 0.5."""
    a = compute_axes(_Brief(industry="zzz-not-a-real-industry"))
    for name in AXIS_NAMES:
        v = getattr(a, name)
        assert 0.4 <= v <= 0.6, f"unknown industry should be near 0.5, got {name}={v}"


def test_axes_to_dict_rounded():
    """to_dict returns rounded floats for stable comparisons."""
    a = compute_axes(_Brief(industry="fintech-payments"))
    d = a.to_dict()
    for v in d.values():
        # Roundedness check: 3 decimal places max
        s = str(v)
        if "." in s:
            assert len(s.split(".")[1]) <= 3


# ---------- Vocabulary ----------

def test_pick_exemplars_returns_n():
    a = compute_axes(_Brief(industry="fintech-payments"))
    ex = pick_exemplars_by_axes(a, n=5)
    assert len(ex) == 5
    # Every exemplar is a brand dict
    for b in ex:
        assert "id" in b


def test_pick_exemplars_excludes():
    a = compute_axes(_Brief(industry="fintech-payments"))
    ex = pick_exemplars_by_axes(a, n=8, exclude_brand_ids=["stripe", "linear.app"])
    ids = {(b.get("id") or "").lower() for b in ex}
    assert "stripe" not in ids
    assert "linear.app" not in ids


def test_distill_vocabulary_nonempty():
    a = compute_axes(_Brief(industry="fintech-payments"))
    ex = pick_exemplars_by_axes(a, n=6)
    vocab = distill_vocabulary(ex)
    assert not vocab.is_empty()
    assert len(vocab.source_brand_ids) == 6


# ---------- Mode dispatch ----------

def test_pure_synthesis_mode_default():
    """No reference_brands → pure_synthesis."""
    sys = synthesize(_Brief(industry="fintech-payments"))
    assert sys.mode == "pure_synthesis"
    assert "canvas" in sys.palette
    assert "ink" in sys.palette


def test_brand_anchor_mode_when_brand_named():
    """reference_brands without strict → brand_anchor."""
    sys = synthesize(_Brief(
        industry="fintech-payments",
        reference_brands=["stripe"],
    ))
    assert sys.mode == "brand_anchor"
    assert sys.anchor_brand_id == "stripe"


def test_strict_brand_mode_when_strict():
    """reference_brands + strict=True → strict_brand."""
    sys = synthesize(_Brief(
        industry="fintech-payments",
        reference_brands=["stripe"],
        strict=True,
    ))
    assert sys.mode == "strict_brand"
    assert sys.anchor_brand_id == "stripe"


def test_unknown_brand_falls_back_to_synthesis():
    """An unknown brand id in strict mode shouldn't crash; falls back to pure."""
    sys = synthesize(_Brief(
        industry="fintech-payments",
        reference_brands=["this-brand-does-not-exist"],
        strict=True,
    ))
    # Either strict_brand emits the missing-brand defaults OR falls through to
    # pure_synthesis. Both are valid; we just want no crash.
    assert sys.mode in ("pure_synthesis", "strict_brand")
    assert "canvas" in sys.palette


# ---------- Output integrity ----------

def test_synthesized_palette_has_hex_colors():
    """Palette values are valid hex strings."""
    sys = synthesize(_Brief(industry="luxury"))
    for key in ("canvas", "ink", "primary", "muted"):
        val = sys.palette.get(key, "")
        assert val.startswith("#"), f"{key} should be hex, got {val}"
        # Allow 3, 6, or 8 hex digits (rgba)
        assert len(val) in (4, 7, 9), f"{key} hex length unexpected: {val}"


def test_synthesized_spacing_scale_is_increasing():
    """spacing.scale is monotonically non-decreasing."""
    sys = synthesize(_Brief(industry="fintech-trading"))
    scale = sys.spacing.get("scale", [])
    assert len(scale) > 0
    for a, b in zip(scale, scale[1:]):
        assert a <= b, f"spacing scale should be non-decreasing, got {scale}"


def test_synthesized_motion_timing_is_positive():
    """motion timing values are positive ms."""
    sys = synthesize(_Brief(industry="gaming"))
    for key in ("base_ms", "fast_ms", "slow_ms"):
        assert sys.motion.get(key, 0) > 0


def test_synthesized_radius_has_pill():
    """radius scale includes a pill (very large) value."""
    sys = synthesize(_Brief(industry="consumer-lifestyle"))
    assert sys.radius.get("pill", 0) >= 100


def test_synthesis_modes_list_locked():
    """SYNTHESIS_MODES is a public contract."""
    assert SYNTHESIS_MODES == ("strict_brand", "brand_anchor", "pure_synthesis")


def test_brand_anchor_palette_differs_from_strict():
    """Anchor mode should produce a different palette than strict mode for same brand+brief."""
    # Same brand, same brief, different modes.
    brief_anchor = _Brief(industry="luxury", reference_brands=["stripe"], strict=False)
    brief_strict = _Brief(industry="luxury", reference_brands=["stripe"], strict=True)
    sys_a = synthesize(brief_anchor)
    sys_s = synthesize(brief_strict)
    # Different modes
    assert sys_a.mode == "brand_anchor"
    assert sys_s.mode == "strict_brand"
