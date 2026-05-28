"""Tests for the v2.1 typography computation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import pytest

from engine.typography import (
    compute_type_scale,
    TypeScale,
    modular_ratio_for,
    SIZE_NAMES,
    WEIGHT_NAMES,
)
from engine.synthesizer.axes import compute_axes


@dataclass
class _Brief:
    industry: str = ""
    tone: List[str] = field(default_factory=list)
    audience: List[str] = field(default_factory=list)
    must_have: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)


def test_size_names_locked():
    """Public contract."""
    assert SIZE_NAMES == (
        "caption", "body", "body-lg", "h4", "h3", "h2", "h1", "display", "hero",
    )


def test_weight_names_locked():
    assert WEIGHT_NAMES == (
        "weight_caption", "weight_body", "weight_h4", "weight_h3",
        "weight_h2", "weight_h1", "weight_display",
    )


def test_modular_ratio_high_contrast():
    """Loud briefs get a 1.333 ratio."""
    axes = compute_axes(_Brief(industry="gaming", tone=["bold", "loud"]))
    assert modular_ratio_for(axes) == 1.333


def test_modular_ratio_low_contrast():
    """Quiet briefs get a 1.200 ratio."""
    axes = compute_axes(_Brief(industry="healthcare", tone=["muted", "subtle", "quiet"]))
    assert modular_ratio_for(axes) == 1.200


def test_modular_ratio_balanced():
    """Mid-contrast → 1.250."""
    axes = compute_axes(_Brief(industry="saas"))
    assert modular_ratio_for(axes) == 1.250


def test_compute_type_scale_returns_all_sizes():
    """Every named size step is computed."""
    scale = compute_type_scale(compute_axes(_Brief(industry="fintech-payments")))
    for name in SIZE_NAMES:
        assert name in scale.sizes_px, f"missing size {name}"
        assert name in scale.sizes_rem, f"missing rem size {name}"


def test_sizes_are_strictly_increasing():
    """The size ladder must monotonically increase from caption to hero."""
    scale = compute_type_scale(compute_axes(_Brief(industry="saas")))
    last = -1
    for name in SIZE_NAMES:
        v = scale.sizes_px[name]
        assert v > last, f"sizes not increasing at {name}: {v} <= {last}"
        last = v


def test_base_px_default_16():
    scale = compute_type_scale(compute_axes(_Brief()))
    assert scale.base_px == 16
    assert scale.sizes_px["body"] == 16.0


def test_caption_smaller_than_body():
    """Caption is below the base."""
    scale = compute_type_scale(compute_axes(_Brief()))
    assert scale.sizes_px["caption"] < scale.sizes_px["body"]


def test_hero_largest():
    scale = compute_type_scale(compute_axes(_Brief()))
    assert scale.sizes_px["hero"] == max(scale.sizes_px.values())


def test_weights_in_valid_range():
    """Font weights are valid 100-900 in 100-step ladder."""
    scale = compute_type_scale(compute_axes(_Brief()))
    for w in scale.weights.values():
        assert 100 <= w <= 900
        assert w % 100 == 0


def test_body_weight_is_400():
    """Body is always 400 (regular)."""
    scale = compute_type_scale(compute_axes(_Brief()))
    assert scale.weights["weight_body"] == 400


def test_geometric_display_heavier_than_humanist():
    """Geometric type (low type_personality) gets heavier display weights."""
    # Force geometric via tone
    geom = compute_type_scale(compute_axes(
        _Brief(industry="developer-tools", tone=["geometric", "technical", "bold"])
    ))
    human = compute_type_scale(compute_axes(
        _Brief(industry="hospitality-travel", tone=["warm", "humanist", "soft"])
    ))
    assert geom.weights["weight_display"] >= human.weights["weight_display"]


def test_tracking_display_negative():
    """Display tracking should always be negative (tighter)."""
    scale = compute_type_scale(compute_axes(_Brief()))
    val = scale.tracking["display"]
    # negative em (or zero) — check it doesn't start with "+"
    assert not val.startswith("+0."), f"display tracking should be negative or zero, got {val}"


def test_tracking_caption_positive():
    """Caption tracking should be positive (wider)."""
    scale = compute_type_scale(compute_axes(_Brief()))
    val = scale.tracking["caption"]
    assert val.startswith("+") or val == "0", (
        f"caption tracking should be positive, got {val}"
    )


def test_line_height_body_open():
    """Body line-height in [1.4, 1.7] range."""
    scale = compute_type_scale(compute_axes(_Brief()))
    assert 1.4 <= scale.line_height["body"] <= 1.7


def test_line_height_hero_tight():
    """Hero line-height tight (1.0 - 1.1)."""
    scale = compute_type_scale(compute_axes(_Brief()))
    assert 1.0 <= scale.line_height["hero"] <= 1.15


def test_dense_briefs_get_tighter_body_line_height():
    """High density axis → tighter line-heights overall."""
    dense = compute_type_scale(compute_axes(_Brief(industry="fintech-trading")))
    airy = compute_type_scale(compute_axes(
        _Brief(industry="luxury", tone=["minimal", "spacious", "airy"])
    ))
    # Dense should be tighter or equal
    assert dense.line_height["body"] <= airy.line_height["body"]


def test_to_dict_serializable():
    scale = compute_type_scale(compute_axes(_Brief()))
    d = scale.to_dict()
    assert "sizes_px" in d
    assert "weights" in d
    assert "tracking" in d
    assert "line_height" in d
    assert d["ratio"] in (1.2, 1.25, 1.333)


def test_to_css_emits_custom_properties():
    """to_css produces a :root block with --ux-font-size-* etc."""
    scale = compute_type_scale(compute_axes(_Brief()))
    css = scale.to_css()
    assert css.startswith(":root {")
    assert "--ux-font-size-body" in css
    assert "--ux-font-weight-display" in css
    assert "--ux-tracking-display" in css
    assert "--ux-line-height-body" in css
    assert css.rstrip().endswith("}")
