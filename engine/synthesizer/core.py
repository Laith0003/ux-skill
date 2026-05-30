"""Synthesizer core — mode dispatch + token synthesis.

The flagship public function ``synthesize(brief)`` returns a SynthesizedSystem
with palette + type pair + spacing + radius + motion + axes.

**Mode dispatch:**

- ``brief.reference_brands`` empty                  → pure_synthesis
- ``brief.reference_brands`` set, strict=False      → brand_anchor (70/30)
- ``brief.reference_brands`` set, strict=True       → strict_brand

**Synthesis math (pure_synthesis):**

1. Compute axes from brief.
2. Pick 8 brand exemplars closest to axes in 7-D space.
3. Distill vocabulary (palettes, type stacks, radius signals).
4. Synthesize a fresh palette by axis-weighted color mixing.
5. Pick a type pair anchored on the closest exemplar; tweak weights by axes.
6. Compute spacing scale + radius + motion timing from axes.
7. Return SynthesizedSystem with all tokens + axes + provenance.

**Brand-anchor (70/30):**

- Pick the named brand spec as the 70% anchor.
- Pick 4 other axis-matching brands as the 30% adaptation pool.
- Same synthesis math, but the anchor's palette/type/radius dominate.

**Strict-brand:**

- Pull the named brand spec.
- Emit its palette + type + spacing + radius + motion verbatim.
- No synthesis. Fastest path.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional

from engine.data_loader import load_brands
from engine.synthesizer.axes import AxisValues, compute_axes, AXIS_NAMES
from engine.synthesizer.vocabulary import (
    Vocabulary,
    distill_vocabulary,
    pick_exemplars_by_axes,
)


SYNTHESIS_MODES = ("strict_brand", "brand_anchor", "pure_synthesis")


# ---------------------------------------------------------------------------
# Output dataclass
# ---------------------------------------------------------------------------

@dataclass
class SynthesizedSystem:
    """A complete design language for one brief — palette + type + spacing + motion."""
    mode: str = "pure_synthesis"
    axes: Dict[str, float] = field(default_factory=dict)
    palette: Dict[str, str] = field(default_factory=dict)
    type_pair: Dict[str, str] = field(default_factory=dict)
    spacing: Dict[str, Any] = field(default_factory=dict)
    radius: Dict[str, Any] = field(default_factory=dict)
    motion: Dict[str, Any] = field(default_factory=dict)
    rationale: List[str] = field(default_factory=list)
    source_brand_ids: List[str] = field(default_factory=list)
    anchor_brand_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Color math (HEX <-> RGB <-> mix)
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_str: str) -> Optional[tuple]:
    s = (hex_str or "").strip()
    if not s.startswith("#"):
        return None
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        return None
    try:
        return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def _rgb_to_hex(rgb: tuple) -> str:
    return "#" + "".join(f"{int(round(max(0, min(255, c)))):02x}" for c in rgb)


def _mix_colors(hex_list: List[str], weights: List[float]) -> Optional[str]:
    """Weighted-average of HEX colors. Returns None if no valid colors."""
    if not hex_list:
        return None
    if weights is None or len(weights) != len(hex_list):
        weights = [1.0] * len(hex_list)
    total_w = sum(weights) or 1.0
    r, g, b = 0.0, 0.0, 0.0
    valid = 0
    for hx, w in zip(hex_list, weights):
        rgb = _hex_to_rgb(hx)
        if rgb is None:
            continue
        r += rgb[0] * w
        g += rgb[1] * w
        b += rgb[2] * w
        valid += w
    if not valid:
        return None
    return _rgb_to_hex((r / total_w, g / total_w, b / total_w))


def _warmth_shift(rgb: tuple, warmth: float) -> tuple:
    """Push RGB warmer (more R+G) or cooler (more B) based on axis value.

    Warmth 0.0 = no shift. 0.5 = baseline. 1.0 = warm shift max.
    Distance from 0.5 determines intensity.
    """
    delta = (warmth - 0.5) * 2  # -1 .. +1
    shift = 18 * delta          # ±18 max units
    r, g, b = rgb
    return (r + shift, g + shift / 2, b - shift / 2)


# ---------------------------------------------------------------------------
# Synthesis primitives
# ---------------------------------------------------------------------------

def _synthesize_palette(vocab: Vocabulary, axes: AxisValues) -> Dict[str, str]:
    """Synthesize a fresh 6-color palette by axis-weighted mixing."""
    # Gather palette anchors from the vocabulary
    canvas_pool = [p.get("canvas") for p in vocab.palettes if p.get("canvas")]
    ink_pool = [p.get("ink") for p in vocab.palettes if p.get("ink")]
    primary_pool = [p.get("primary") or p.get("accent") for p in vocab.palettes if p.get("primary") or p.get("accent")]

    # Defaults if vocabulary thin
    if not canvas_pool:
        canvas_pool = ["#0a0a0a" if axes.contrast > 0.5 else "#f6f7f9"]
    if not ink_pool:
        ink_pool = ["#f6f7f9" if axes.contrast > 0.5 else "#0a0a0a"]
    if not primary_pool:
        primary_pool = ["#06b6d4"] if axes.warmth < 0.5 else ["#f97316"]

    # Pure mix
    canvas = _mix_colors(canvas_pool, None) or canvas_pool[0]
    ink = _mix_colors(ink_pool, None) or ink_pool[0]
    primary = _mix_colors(primary_pool, None) or primary_pool[0]

    # Warmth-shift
    canvas_rgb = _hex_to_rgb(canvas)
    ink_rgb = _hex_to_rgb(ink)
    primary_rgb = _hex_to_rgb(primary)
    if canvas_rgb:
        canvas = _rgb_to_hex(_warmth_shift(canvas_rgb, axes.warmth))
    if ink_rgb:
        ink = _rgb_to_hex(_warmth_shift(ink_rgb, axes.warmth))
    if primary_rgb:
        primary = _rgb_to_hex(_warmth_shift(primary_rgb, axes.warmth))

    # Derived: muted = blend of canvas + ink at 70/30
    muted = _mix_colors([canvas, ink], [0.7, 0.3]) or "#808080"
    # Body = blend of canvas + ink at 30/70
    body = _mix_colors([canvas, ink], [0.3, 0.7]) or "#404040"
    # Hairline = 80/20 toward canvas; slight tint
    hairline = _mix_colors([canvas, ink], [0.85, 0.15]) or "#cccccc"

    return {
        "canvas": canvas,
        "ink": ink,
        "body": body,
        "muted": muted,
        "primary": primary,
        "hairline": hairline,
    }


def _synthesize_spacing(axes: AxisValues) -> Dict[str, Any]:
    """Compute spacing scale from density + formality interaction.

    Uses the documented axis interaction matrix
    (engine.synthesizer.interactions.spacing_base_for) so dense + formal,
    airy + corporate, etc. all resolve predictably instead of letting
    whichever axis the primitive checks first win silently.
    """
    from engine.synthesizer.interactions import spacing_base_for
    base = spacing_base_for(axes)
    # Fibonacci-ish scale anchored on the resolved base
    if base <= 4:
        scale = [base, base * 2, base * 3, base * 5, base * 8, base * 13, base * 21]
    elif base >= 10:
        scale = [base, base * 2, base * 3, base * 4, base * 6, base * 9, base * 14]
    elif base >= 8:
        scale = [base, base * 2, base * 4, base * 6, base * 8, base * 12, base * 16]
    else:
        scale = [base, base * 2, base * 3, base * 4, base * 6, base * 9, base * 14]
    return {
        "base": base,
        "scale": scale,
        "density_signal": round(axes.density, 3),
        "formality_signal": round(axes.formality, 3),
    }


def _synthesize_radius(vocab: Vocabulary, axes: AxisValues) -> Dict[str, Any]:
    """Compute radius scale via geometry × formality interaction.

    Uses interactions.radius_base_px_for() so sharp+corporate explicitly
    resolves to nearly-no-radius, soft+playful explicitly resolves to
    generous radius, and blends only in the ambiguous middle.
    """
    from engine.synthesizer.interactions import radius_base_px_for
    voc_signals = vocab.radius_signals
    voc_mean = (sum(voc_signals) / len(voc_signals)) if voc_signals else 0.5
    base_px = radius_base_px_for(axes, vocab_mean=voc_mean)
    return {
        "base_px": base_px,
        "sm": max(1, int(base_px * 0.5)),
        "md": base_px,
        "lg": int(base_px * 1.5),
        "xl": int(base_px * 2.5),
        "pill": 999,
        "geometry_signal": round(axes.geometry, 3),
        "formality_signal": round(axes.formality, 3),
    }


def _synthesize_motion(axes: AxisValues) -> Dict[str, Any]:
    """Compute motion timing via motion × formality interaction.

    Uses interactions.motion_timing_for() so high motion + corporate
    formality is dampened (slower base, same curve) instead of letting
    motion axis win blindly.
    """
    from engine.synthesizer.interactions import motion_timing_for
    m = axes.motion
    timings = motion_timing_for(axes)

    # Curve picks: still axis-driven
    if m > 0.7:
        curve = "cubic-bezier(0.34, 1.56, 0.64, 1)"  # springy overshoot
        curve_name = "spring-soft"
    elif m > 0.4:
        curve = "cubic-bezier(0.22, 1, 0.36, 1)"     # ease-out-cinema
        curve_name = "ease-cinema"
    else:
        curve = "cubic-bezier(0.4, 0.0, 0.2, 1)"     # standard ease
        curve_name = "ease-standard"

    return {
        "base_ms": timings["base_ms"],
        "fast_ms": timings["fast_ms"],
        "slow_ms": timings["slow_ms"],
        "curve": curve,
        "curve_name": curve_name,
        "motion_signal": round(m, 3),
        "formality_signal": round(axes.formality, 3),
    }


def _synthesize_type_pair(vocab: Vocabulary, axes: AxisValues) -> Dict[str, str]:
    """Pick a type pair, biased by type_personality axis."""
    if not vocab.type_pairs:
        # Defaults grounded in axis values
        if axes.type_personality > 0.6:
            return {"display": "Bricolage Grotesque", "body": "Inter", "mono": "JetBrains Mono"}
        elif axes.type_personality < 0.4:
            return {"display": "Inter Tight", "body": "Inter", "mono": "JetBrains Mono"}
        return {"display": "Inter", "body": "Inter", "mono": "JetBrains Mono"}

    # Find the type pair whose source brand has type_personality nearest to axes.type_personality
    # (We don't have per-brand axis on vocab.type_pairs, so just pick the first non-empty.)
    pair = vocab.type_pairs[0]
    out = {}
    if pair.get("display"):
        out["display"] = pair["display"]
    if pair.get("body"):
        out["body"] = pair["body"]
    if pair.get("mono"):
        out["mono"] = pair["mono"]
    if not out:
        return {"display": "Inter", "body": "Inter", "mono": "JetBrains Mono"}
    return out


# ---------------------------------------------------------------------------
# Mode dispatch
# ---------------------------------------------------------------------------

def _find_brand(brand_id: str) -> Optional[Dict[str, Any]]:
    """Look up a brand spec by id."""
    target = (brand_id or "").lower()
    for b in load_brands():
        if (b.get("id") or "").lower() == target:
            return b
    return None


def _strict_brand_mode(brand_id: str, axes: AxisValues) -> SynthesizedSystem:
    """Emit a brand's spec verbatim, no synthesis."""
    brand = _find_brand(brand_id)
    if not brand:
        # Fall back to pure synthesis if the named brand isn't in the catalogue
        return _pure_synthesis_mode(axes)
    dl = brand.get("design_language") or {}
    palette = {
        "canvas":   dl.get("color_canvas") or "#0a0a0a",
        "ink":      dl.get("color_ink") or "#f6f7f9",
        "primary":  dl.get("color_primary") or "#06b6d4",
        "body":     dl.get("color_body") or "#c0c3c9",
        "muted":    dl.get("color_muted") or "#8a8f96",
        "hairline": "rgba(255,255,255,0.08)",
    }
    type_pair = {}
    for src, dst in (("font_display", "display"), ("font_body", "body"), ("font_mono", "mono"),
                     ("typography_display", "display"), ("typography_body", "body")):
        v = dl.get(src)
        if v:
            type_pair[dst] = v
    if not type_pair:
        type_pair = {"display": "Inter", "body": "Inter", "mono": "JetBrains Mono"}

    return SynthesizedSystem(
        mode="strict_brand",
        axes=axes.to_dict(),
        palette=palette,
        type_pair=type_pair,
        spacing=_synthesize_spacing(axes),
        radius=_synthesize_radius(Vocabulary(), axes),
        motion=_synthesize_motion(axes),
        rationale=[f"strict_brand mode: emitting {brand_id!r} tokens verbatim."],
        source_brand_ids=[brand.get("id") or brand_id],
        anchor_brand_id=brand.get("id") or brand_id,
    )


def _brand_anchor_mode(brand_ids: List[str], axes: AxisValues) -> SynthesizedSystem:
    """70% anchor brand + 30% axis-adapted pool."""
    anchor_specs = [s for s in (_find_brand(bid) for bid in brand_ids) if s]
    if not anchor_specs:
        return _pure_synthesis_mode(axes)
    # Build a weighted vocabulary: anchor + 4 axis-matching others
    other_exemplars = pick_exemplars_by_axes(
        axes, n=4, exclude_brand_ids=[s["id"] for s in anchor_specs]
    )
    # Anchor first → its palette comes first → gets more weight in mixing
    pool = anchor_specs + anchor_specs + other_exemplars   # double-count anchor
    vocab = distill_vocabulary(pool)
    sys = _synthesize_from_vocab(vocab, axes, mode="brand_anchor",
                                  anchor_brand_id=anchor_specs[0].get("id"))
    sys.rationale = [
        f"brand_anchor mode: {anchor_specs[0].get('name')} at 70% + "
        f"{len(other_exemplars)} axis-adapted exemplars at 30%."
    ]
    return sys


def _pure_synthesis_mode(axes: AxisValues) -> SynthesizedSystem:
    """No brand named — infinity-space synthesis from 8 axis-matching exemplars."""
    exemplars = pick_exemplars_by_axes(axes, n=8)
    vocab = distill_vocabulary(exemplars)
    sys = _synthesize_from_vocab(vocab, axes, mode="pure_synthesis")
    sys.rationale = [
        f"pure_synthesis mode: 8 axis-matching exemplars distilled into a fresh design language. "
        f"No single brand copied."
    ]
    return sys


def _synthesize_from_vocab(vocab: Vocabulary, axes: AxisValues, mode: str,
                            anchor_brand_id: Optional[str] = None) -> SynthesizedSystem:
    """Shared synthesis path used by anchor + pure modes."""
    return SynthesizedSystem(
        mode=mode,
        axes=axes.to_dict(),
        palette=_synthesize_palette(vocab, axes),
        type_pair=_synthesize_type_pair(vocab, axes),
        spacing=_synthesize_spacing(axes),
        radius=_synthesize_radius(vocab, axes),
        motion=_synthesize_motion(axes),
        source_brand_ids=list(vocab.source_brand_ids),
        anchor_brand_id=anchor_brand_id,
    )


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------

def _stamp_client_brand(system: SynthesizedSystem, brand: Any) -> SynthesizedSystem:
    """Override the synthesized palette primary/accent + display type with an
    EXTRACTED client BrandProfile (rule 2). Distinct from the reference_brands
    exemplar modes (which pull known specs like Stripe); this stamps the actual
    client's amber/logo/font over whatever was synthesized. Neutrals, spacing and
    motion are left untouched. Deterministic.
    """
    from engine.brand.extract import BrandProfile
    prof = brand if isinstance(brand, BrandProfile) else None
    if prof is None and isinstance(brand, dict):
        try:
            prof = BrandProfile(**{k: v for k, v in brand.items()
                                   if k in BrandProfile.__dataclass_fields__})
        except TypeError:
            prof = None
    if prof is None or not (prof.primary or prof.name):
        return system
    pal = dict(system.palette or {})
    if prof.primary:
        pal["primary"] = prof.primary
        pal["accent"] = prof.primary
    if prof.secondary:
        pal["secondary"] = prof.secondary[0]
    system.palette = pal
    tp = dict(system.type_pair or {})
    if prof.fonts.get("display"):
        tp["display"] = prof.fonts["display"]
    elif prof.logo_style:
        tp["display_directive"] = ("match the logo style: %s (reject default fonts)"
                                    % prof.logo_style)
    system.type_pair = tp
    system.rationale = list(system.rationale or []) + [
        "Client-brand anchor: palette primary %s + type from the logo, overriding "
        "the synthesized pick." % (prof.primary or "n/a")]
    return system


def synthesize(brief: Any) -> SynthesizedSystem:
    """Synthesize a fresh design language from a Brief.

    Mode is dispatched based on what's in the brief:
      - reference_brands set + strict=True → strict_brand
      - reference_brands set                → brand_anchor
      - neither                             → pure_synthesis

    Same brief input → same SynthesizedSystem output (deterministic).
    """
    def g(field_name: str, default=None):
        if hasattr(brief, field_name):
            return getattr(brief, field_name)
        if isinstance(brief, dict):
            return brief.get(field_name, default)
        return default

    reference_brands = list(g("reference_brands", []) or [])
    strict = bool(g("strict", False) or g("strict_brand", False))

    axes = compute_axes(brief)

    if reference_brands and strict:
        system = _strict_brand_mode(reference_brands[0], axes)
    elif reference_brands:
        system = _brand_anchor_mode(reference_brands, axes)
    else:
        system = _pure_synthesis_mode(axes)

    # Extracted-client-brand anchor: a final, deterministic stamp on top of the
    # mode output (composes with, does not replace, the exemplar modes above).
    brand = g("brand", None)
    if brand:
        system = _stamp_client_brand(system, brand)
    return system
