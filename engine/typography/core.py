"""Typography computation core.

Derives a fresh type scale (sizes, weights, tracking, line-heights) from
the 7-axis values. No fixed table picked from a manifest — every brief
gets a unique computed ladder.

Math:
- Modular scale: size[n] = base * (ratio ** (n - body_idx))
- Body = 16px base (standard).
- 9 named steps: caption, body, body-lg, h4, h3, h2, h1, display, hero
- Ratio derives from axes.contrast:
    - contrast >= 0.7  → 1.333 (perfect fourth, loud)
    - contrast >= 0.4  → 1.250 (major third, balanced)
    - contrast <  0.4  → 1.200 (minor third, quiet)
- Weights derive from axes.type_personality + axes.contrast.
- Tracking shrinks on display sizes (negative), widens on caption (positive).
- Line-heights tighten on large sizes (1.04→1.10), open on body (1.50→1.65).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Tuple

from engine.synthesizer.axes import AxisValues


SIZE_NAMES: Tuple[str, ...] = (
    "caption",   # -2
    "body",      # 0 (base, 16px)
    "body-lg",   # +1
    "h4",        # +2
    "h3",        # +3
    "h2",        # +4
    "h1",        # +5
    "display",   # +6
    "hero",      # +7
)

# Step offsets relative to body (=0).
_STEP_OFFSETS: Dict[str, int] = {
    "caption": -2,
    "body": 0,
    "body-lg": 1,
    "h4": 2,
    "h3": 3,
    "h2": 4,
    "h1": 5,
    "display": 6,
    "hero": 7,
}

WEIGHT_NAMES: Tuple[str, ...] = (
    "weight_caption",
    "weight_body",
    "weight_h4",
    "weight_h3",
    "weight_h2",
    "weight_h1",
    "weight_display",
)


@dataclass
class TypeScale:
    """A complete type system computed per brief."""
    ratio: float = 1.25
    base_px: int = 16
    sizes_px: Dict[str, float] = field(default_factory=dict)
    sizes_rem: Dict[str, float] = field(default_factory=dict)
    weights: Dict[str, int] = field(default_factory=dict)
    tracking: Dict[str, str] = field(default_factory=dict)   # letter-spacing
    line_height: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_css(self) -> str:
        """Emit a CSS custom-properties block for the scale."""
        lines: List[str] = [":root {"]
        for name, px in self.sizes_px.items():
            lines.append(f"  --ux-font-size-{name}: {px:.1f}px;")
        for name, w in self.weights.items():
            short = name.replace("weight_", "")
            lines.append(f"  --ux-font-weight-{short}: {w};")
        for name, tr in self.tracking.items():
            lines.append(f"  --ux-tracking-{name}: {tr};")
        for name, lh in self.line_height.items():
            lines.append(f"  --ux-line-height-{name}: {lh:.2f};")
        lines.append("}")
        return "\n".join(lines)


def modular_ratio_for(axes: AxisValues) -> float:
    """Pick the modular scale ratio based on contrast axis.

    Contrast >= 0.7  → 1.333 (perfect fourth, loud, dramatic)
    Contrast >= 0.4  → 1.250 (major third, balanced)
    Contrast <  0.4  → 1.200 (minor third, quiet)
    """
    if axes.contrast >= 0.7:
        return 1.333
    if axes.contrast >= 0.4:
        return 1.250
    return 1.200


def _compute_sizes_px(base_px: int, ratio: float) -> Dict[str, float]:
    """Return px size per named step."""
    out: Dict[str, float] = {}
    for name, offset in _STEP_OFFSETS.items():
        # Negative offsets shrink, positive grow.
        out[name] = round(base_px * (ratio ** offset), 1)
    return out


def _compute_weights(axes: AxisValues) -> Dict[str, int]:
    """Heavier display when contrast high or type geometric (low type_personality).

    Body always 400. Caption usually 500 for legibility at small size.
    """
    geometric = axes.type_personality < 0.5
    loud = axes.contrast > 0.65

    # Base curve
    display_w = 700
    h1_w = 600
    h2_w = 600
    h3_w = 600
    h4_w = 500
    body_w = 400
    caption_w = 500

    if geometric:
        # Geometric grotesque looks crisp with heavier display weights
        display_w = 800 if loud else 700
        h1_w = 700
        h2_w = 600
    else:
        # Humanist looks better with mid weights even when loud
        display_w = 600 if not loud else 700
        h1_w = 500
        h2_w = 500

    return {
        "weight_caption": caption_w,
        "weight_body": body_w,
        "weight_h4": h4_w,
        "weight_h3": h3_w,
        "weight_h2": h2_w,
        "weight_h1": h1_w,
        "weight_display": display_w,
    }


def _compute_tracking(axes: AxisValues) -> Dict[str, str]:
    """Letter-spacing per size.

    Display tighter (negative em), caption wider (positive em).
    Formality high → slightly more conservative tracking everywhere.
    """
    formal = axes.formality
    # Tighter display when formal+confident, more open when playful
    tracking_display = -0.025 if formal > 0.6 else -0.015
    tracking_h1 = -0.02 if formal > 0.6 else -0.012
    tracking_h2 = -0.015
    tracking_body = 0.0
    tracking_caption = 0.06 if formal > 0.6 else 0.04

    def fmt(em: float) -> str:
        # Format as em with leading sign
        return f"{em:+.3f}em".replace("+0.000em", "0").replace("-0.000em", "0")

    return {
        "display": fmt(tracking_display),
        "h1": fmt(tracking_h1),
        "h2": fmt(tracking_h2),
        "h3": fmt(-0.01),
        "h4": fmt(-0.005),
        "body-lg": fmt(0.0),
        "body": fmt(tracking_body),
        "caption": fmt(tracking_caption),
    }


def _compute_line_heights(axes: AxisValues) -> Dict[str, float]:
    """Tighter line-height on large sizes, more open on body.

    Density high → tighter line-heights overall (more on a screen).
    Density low → looser line-heights (airier).
    """
    dense = axes.density > 0.6
    open_body = 1.55 if not dense else 1.50
    return {
        "hero": 1.02,
        "display": 1.05,
        "h1": 1.08,
        "h2": 1.12,
        "h3": 1.20,
        "h4": 1.30,
        "body-lg": 1.50,
        "body": open_body,
        "caption": 1.45,
    }


def compute_type_scale(axes: AxisValues, base_px: int = 16) -> TypeScale:
    """Build a complete type system from axis values.

    Deterministic: same axes → same scale.
    """
    ratio = modular_ratio_for(axes)
    sizes_px = _compute_sizes_px(base_px, ratio)
    sizes_rem = {k: round(v / base_px, 3) for k, v in sizes_px.items()}
    weights = _compute_weights(axes)
    tracking = _compute_tracking(axes)
    lh = _compute_line_heights(axes)
    return TypeScale(
        ratio=ratio,
        base_px=base_px,
        sizes_px=sizes_px,
        sizes_rem=sizes_rem,
        weights=weights,
        tracking=tracking,
        line_height=lh,
    )
