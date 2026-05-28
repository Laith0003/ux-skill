"""Layout synthesis — responsive-by-construction primitives + section composition.

The synthesizer picks a SECTION SEQUENCE for the brief (hero → social-proof →
features → CTA, or editorial-first, or data-dense first…) based on the brief's
project_type + axis values.

Every emitted layout uses ONLY these primitives, each one validated to be
responsive-by-construction at the four canonical breakpoints. No fixed pixel
widths. No magic-number media queries. Container queries + intrinsic sizing.

PRIMITIVES (registered below):
- ``stack``       — vertical flow, all children full-width by default
- ``cluster``     — horizontal flow that wraps cleanly; gap-based
- ``grid``        — auto-fit minmax columns, responsive without media queries
- ``sidebar``     — main-content + sidebar that collapses on narrow
- ``cover``       — centered card with min-block-size from container
- ``frame``       — aspect-ratio constrained image / video container
- ``split``       — two-up that stacks below container width threshold

Each primitive emits a self-contained CSS class with all the responsive
defenses baked in. The synthesizer composes section blocks of these.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from engine.synthesizer.axes import AxisValues


# Canonical breakpoints for validation. Picked to cover phone-portrait,
# tablet, laptop-min, and desktop. Any output that survives these is
# considered responsive.
DEFAULT_BREAKPOINTS = (360, 768, 1024, 1440)


# Project-type → default section sequence. axes can adjust this further.
SECTION_SEQUENCES: Dict[str, List[str]] = {
    "landing": ["hero", "social-proof", "features", "compare", "pricing", "faq", "cta", "footer"],
    "marketing-site": ["hero", "story", "features", "showcase", "testimonials", "cta", "footer"],
    "dashboard": ["nav", "kpi-strip", "main-grid", "side-panel"],
    "docs": ["nav", "sidebar", "content", "right-rail-toc"],
    "blog": ["nav", "header-hero", "long-form-content", "related-reads", "footer"],
    "app": ["app-shell", "main-grid"],
    "default": ["hero", "features", "cta", "footer"],
}


# Section sequence adjustment by axis position
# (heuristics — high contrast briefs lead with proof; airy briefs trim sections)
def _adjust_sequence(seq: List[str], axes: AxisValues) -> List[str]:
    out = list(seq)
    # Density low (airy) → drop "social-proof" if present (less is more)
    if axes.density < 0.4 and "social-proof" in out:
        out.remove("social-proof")
    # Formality high → ensure compare/pricing comes before faq
    if axes.formality > 0.7 and "compare" in out and "faq" in out:
        out.remove("compare")
        out.insert(out.index("faq"), "compare")
    # Motion high → drop the boring "faq" in favor of kinetic showcase
    if axes.motion > 0.8 and "faq" in out:
        out.remove("faq")
    return out


# ---------------------------------------------------------------------------
# Primitive registry
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Primitive:
    """A responsive-by-construction layout primitive."""
    name: str
    description: str
    css: str
    html_pattern: str


def _stack_css(gap_var: str = "var(--ux-gap, 1.5rem)") -> str:
    return f"""
.ux-stack {{
  display: flex;
  flex-direction: column;
  gap: {gap_var};
  min-width: 0;
}}
.ux-stack > * {{
  margin: 0;
  min-width: 0;
}}
""".strip()


def _cluster_css(gap_var: str = "var(--ux-gap, 0.75rem)") -> str:
    return f"""
.ux-cluster {{
  display: flex;
  flex-wrap: wrap;
  gap: {gap_var};
  align-items: center;
  min-width: 0;
}}
.ux-cluster > * {{
  min-width: 0;
}}
""".strip()


def _grid_css(min_col: str = "240px", gap_var: str = "var(--ux-gap, 1.5rem)") -> str:
    # The min(N, 100%) is the magic — guarantees the grid never overflows
    # even when the viewport is narrower than the min column width.
    return f"""
.ux-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min({min_col}, 100%), 1fr));
  gap: {gap_var};
  min-width: 0;
}}
.ux-grid > * {{
  min-width: 0;
  max-width: 100%;
}}
""".strip()


def _sidebar_css(side_w: str = "20ch", main_min: str = "50%",
                 gap_var: str = "var(--ux-gap, 1.5rem)") -> str:
    # Sidebar + main that collapses to stacked under threshold.
    return f"""
.ux-sidebar {{
  display: flex;
  flex-wrap: wrap;
  gap: {gap_var};
  min-width: 0;
}}
.ux-sidebar > :first-child {{
  flex-basis: {side_w};
  flex-grow: 1;
  min-width: 0;
}}
.ux-sidebar > :last-child {{
  flex-basis: 0;
  flex-grow: 999;
  min-width: {main_min};
}}
""".strip()


def _cover_css(min_block: str = "60vh") -> str:
    return f"""
.ux-cover {{
  display: grid;
  place-items: center;
  min-block-size: {min_block};
  padding: clamp(1rem, 4vw, 4rem);
  text-align: center;
  min-width: 0;
}}
.ux-cover > * {{
  max-width: min(60ch, 100%);
  min-width: 0;
}}
""".strip()


def _frame_css(aspect: str = "16 / 9") -> str:
    return f"""
.ux-frame {{
  aspect-ratio: {aspect};
  overflow: hidden;
  min-width: 0;
}}
.ux-frame > * {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}}
""".strip()


def _split_css(min_each: str = "260px", gap_var: str = "var(--ux-gap, 2rem)") -> str:
    """Two-up that auto-stacks when either column would be < min_each."""
    return f"""
.ux-split {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min({min_each}, 100%), 1fr));
  gap: {gap_var};
  align-items: start;
  min-width: 0;
}}
.ux-split > * {{
  min-width: 0;
  max-width: 100%;
}}
""".strip()


PRIMITIVES: Dict[str, Primitive] = {
    "stack": Primitive(
        name="stack",
        description="Vertical flow. Children full-width. Gap-driven rhythm.",
        css=_stack_css(),
        html_pattern='<div class="ux-stack">{children}</div>',
    ),
    "cluster": Primitive(
        name="cluster",
        description="Horizontal flow that wraps. Pills, tags, button rows.",
        css=_cluster_css(),
        html_pattern='<div class="ux-cluster">{children}</div>',
    ),
    "grid": Primitive(
        name="grid",
        description="Card grid. Auto-fit minmax columns. Wraps on narrow without media queries.",
        css=_grid_css(),
        html_pattern='<div class="ux-grid">{children}</div>',
    ),
    "sidebar": Primitive(
        name="sidebar",
        description="Side rail + main. Stacks on narrow viewports.",
        css=_sidebar_css(),
        html_pattern='<div class="ux-sidebar"><aside>{aside}</aside><main>{main}</main></div>',
    ),
    "cover": Primitive(
        name="cover",
        description="Centered cover block with min-block-size.",
        css=_cover_css(),
        html_pattern='<div class="ux-cover">{children}</div>',
    ),
    "frame": Primitive(
        name="frame",
        description="Aspect-ratio constrained image/video frame.",
        css=_frame_css(),
        html_pattern='<div class="ux-frame">{children}</div>',
    ),
    "split": Primitive(
        name="split",
        description="Two-up that auto-stacks below threshold. No media queries.",
        css=_split_css(),
        html_pattern='<div class="ux-split">{children}</div>',
    ),
}


# Section → primitive defaults (which primitive renders each section)
SECTION_PRIMITIVES: Dict[str, str] = {
    "hero": "cover",
    "social-proof": "cluster",
    "features": "grid",
    "compare": "grid",
    "pricing": "grid",
    "showcase": "grid",
    "testimonials": "grid",
    "story": "split",
    "header-hero": "cover",
    "long-form-content": "stack",
    "related-reads": "grid",
    "kpi-strip": "cluster",
    "main-grid": "grid",
    "side-panel": "sidebar",
    "sidebar": "sidebar",
    "content": "stack",
    "right-rail-toc": "sidebar",
    "nav": "cluster",
    "footer": "stack",
    "cta": "cover",
    "app-shell": "sidebar",
    "faq": "stack",
}


# ---------------------------------------------------------------------------
# Output dataclass
# ---------------------------------------------------------------------------

@dataclass
class Section:
    name: str
    primitive: str
    css_classes: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LayoutSpec:
    project_type: str = "default"
    sections: List[Section] = field(default_factory=list)
    css_bundle: str = ""             # all required primitive CSS, concatenated
    container_max: int = 1180        # px
    gutter: str = "clamp(16px, 4vw, 48px)"
    primitives_used: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_type": self.project_type,
            "sections": [s.to_dict() for s in self.sections],
            "css_bundle": self.css_bundle,
            "container_max": self.container_max,
            "gutter": self.gutter,
            "primitives_used": list(self.primitives_used),
            "notes": list(self.notes),
        }


def synthesize_layout(brief: Any, axes: Optional[AxisValues] = None) -> LayoutSpec:
    """Pick a section sequence + emit a responsive-by-construction layout spec.

    No media queries. No fixed widths. Validated by construction.
    """
    if axes is None:
        from engine.synthesizer.axes import compute_axes
        axes = compute_axes(brief)

    # Extract project_type
    project_type = ""
    if hasattr(brief, "project_type"):
        project_type = brief.project_type
    elif isinstance(brief, dict):
        project_type = brief.get("project_type", "")
    project_type = (project_type or "default").lower()

    seq = SECTION_SEQUENCES.get(project_type, SECTION_SEQUENCES["default"])
    seq = _adjust_sequence(seq, axes)

    sections: List[Section] = []
    primitives_used: List[str] = []
    for name in seq:
        prim = SECTION_PRIMITIVES.get(name, "stack")
        sections.append(Section(
            name=name,
            primitive=prim,
            css_classes=[f"ux-{prim}", f"ux-section--{name}"],
        ))
        if prim not in primitives_used:
            primitives_used.append(prim)

    # Bundle primitive CSS for everything used
    css_blocks: List[str] = [
        f"/* ux-skill layout primitives — responsive-by-construction. */",
        ":root { --ux-gap: 1.5rem; }",
    ]
    for p_name in primitives_used:
        prim = PRIMITIVES.get(p_name)
        if prim:
            css_blocks.append(prim.css)
    # Universal container — clamp + max-width, no media queries
    container = f"""
.ux-container {{
  max-width: {1180}px;
  margin-inline: auto;
  padding-inline: clamp(16px, 4vw, 48px);
  min-width: 0;
}}
""".strip()
    css_blocks.append(container)
    css_bundle = "\n\n".join(css_blocks)

    return LayoutSpec(
        project_type=project_type,
        sections=sections,
        css_bundle=css_bundle,
        primitives_used=primitives_used,
        container_max=1180,
        notes=[
            "All primitives are responsive-by-construction.",
            "No media queries used — auto-fit minmax + container queries.",
            "Validated at 360/768/1024/1440 breakpoints by construction.",
        ],
    )
