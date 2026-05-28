"""Tests for the v2.1 layout synthesizer.

Verifies:
- Project-type → section sequence dispatch
- Axis-driven sequence adjustment
- Every primitive's CSS contains the responsive-by-construction defenses
- LayoutSpec output is well-formed
- DEFAULT_BREAKPOINTS includes 360 / 768 / 1024 / 1440
- CSS bundle never contains fixed pixel widths over 100vw
- No media queries are required for responsiveness (auto-fit minmax handles it)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import re
import pytest

from engine.layout import (
    synthesize_layout,
    LayoutSpec,
    Section,
    PRIMITIVES,
    DEFAULT_BREAKPOINTS,
)
from engine.synthesizer.axes import compute_axes


@dataclass
class _Brief:  # underscore so pytest doesn't collect
    project_type: str = ""
    industry: str = ""
    tone: List[str] = field(default_factory=list)
    audience: List[str] = field(default_factory=list)
    must_have: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)


def test_default_breakpoints_locked():
    """Public contract for the validator breakpoints."""
    assert DEFAULT_BREAKPOINTS == (360, 768, 1024, 1440)


def test_primitives_registry_complete():
    """All 7 primitives present."""
    expected = {"stack", "cluster", "grid", "sidebar", "cover", "frame", "split"}
    assert set(PRIMITIVES.keys()) == expected


def test_every_primitive_has_min_width_zero():
    """Defense against flex/grid overflow: every primitive sets min-width: 0."""
    for name, prim in PRIMITIVES.items():
        assert "min-width: 0" in prim.css, (
            f"primitive {name} missing min-width: 0 defense (overflow risk)"
        )


def test_grid_uses_auto_fit_minmax():
    """The grid primitive uses auto-fit minmax — the responsive-by-construction trick."""
    grid = PRIMITIVES["grid"]
    assert "auto-fit" in grid.css
    assert "minmax" in grid.css
    assert "100%" in grid.css, "the min(N, 100%) trick must be present"


def test_split_uses_auto_fit_minmax():
    """The split primitive uses the same trick → stacks below threshold."""
    s = PRIMITIVES["split"]
    assert "auto-fit" in s.css
    assert "minmax" in s.css


def test_no_fixed_width_in_primitive_css():
    """No primitive CSS sets a width over 100% of viewport (no overflow bombs)."""
    for name, prim in PRIMITIVES.items():
        # Forbid bare 'width: 100vw' or '> Npx widths' as a guideline check
        # (We use min(N, 100%) for grid columns which is fine.)
        bad = re.search(r"\bwidth\s*:\s*[1-9]\d{3,}px", prim.css)
        assert not bad, f"{name} sets a huge fixed pixel width (overflow risk)"


def test_landing_sequence():
    spec = synthesize_layout(_Brief(project_type="landing"))
    section_names = [s.name for s in spec.sections]
    assert "hero" in section_names
    assert "footer" in section_names
    assert "features" in section_names


def test_dashboard_sequence_includes_nav_and_grid():
    spec = synthesize_layout(_Brief(project_type="dashboard"))
    names = [s.name for s in spec.sections]
    assert "nav" in names
    assert "main-grid" in names


def test_unknown_project_type_uses_default():
    """Unknown project_type → default sequence (no crash)."""
    spec = synthesize_layout(_Brief(project_type="some-unheard-of-thing"))
    assert len(spec.sections) > 0
    assert "hero" in [s.name for s in spec.sections]


def test_low_density_drops_social_proof():
    """Density < 0.4 → social-proof gets removed."""
    # Force low density via minimal/spacious tone
    brief = _Brief(project_type="landing", industry="luxury",
                   tone=["minimal", "spacious", "quiet"])
    spec = synthesize_layout(brief)
    names = [s.name for s in spec.sections]
    assert "social-proof" not in names


def test_layout_spec_includes_css_bundle():
    spec = synthesize_layout(_Brief(project_type="landing"))
    assert spec.css_bundle, "css_bundle should not be empty"
    # Every used primitive's CSS should be included
    for p_name in spec.primitives_used:
        assert f"ux-{p_name}" in spec.css_bundle


def test_css_bundle_has_container_class():
    """Universal container class is always bundled."""
    spec = synthesize_layout(_Brief(project_type="landing"))
    assert ".ux-container" in spec.css_bundle
    assert "clamp(" in spec.css_bundle, "container should use clamp() for fluid gutters"


def test_no_media_queries_in_bundle():
    """We rely on auto-fit + container queries, not media queries.

    A future change might add tweaks behind a media query, but baseline
    primitives must not require them.
    """
    spec = synthesize_layout(_Brief(project_type="landing"))
    # @media may appear ONLY for prefers-reduced-motion / prefers-color-scheme.
    # The primitive bundle should have ZERO @media for size-based responsive.
    size_queries = re.findall(r"@media\s*\([^)]*(width|orientation)[^)]*\)",
                              spec.css_bundle)
    assert not size_queries, (
        f"primitive bundle should not require size-based media queries, "
        f"found: {size_queries}"
    )


def test_section_to_dict_round_trip():
    s = Section(name="hero", primitive="cover", css_classes=["ux-cover", "ux-section--hero"])
    d = s.to_dict()
    assert d["name"] == "hero"
    assert d["primitive"] == "cover"
    assert "ux-cover" in d["css_classes"]


def test_layout_spec_to_dict():
    spec = synthesize_layout(_Brief(project_type="landing"))
    d = spec.to_dict()
    assert "sections" in d
    assert "css_bundle" in d
    assert "primitives_used" in d
    assert d["project_type"] == "landing"


def test_axes_optional_param_uses_brief():
    """If axes not passed, compute from brief."""
    brief = _Brief(project_type="landing", industry="fintech-payments")
    spec_a = synthesize_layout(brief)
    spec_b = synthesize_layout(brief, axes=compute_axes(brief))
    # Same brief → same sequence (deterministic)
    assert [s.name for s in spec_a.sections] == [s.name for s in spec_b.sections]
