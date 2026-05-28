"""Vocabulary distillation from brand specs + manifests.

A "vocabulary" is the pool of design primitives the synthesizer draws from
when composing a fresh design language. The catalogue isn't TEMPLATES; it's
TRAINING DATA — patterns the engine learns from. No single brand's tokens
are copied verbatim (unless the brief explicitly requests strict-brand mode).

How distillation works:

1. Pick N brand exemplars matching the brief's axes (e.g. axis warmth=0.7
   → pick 5 brands whose seed warmth is also high: Mailchimp, Aesop,
   Glossier, ...).
2. Extract primitives from each spec:
     - palette anchors (canvas, ink, accent hex codes)
     - type stacks (display family, body family)
     - signature motion (timing, curves)
     - radius patterns (sharp / soft)
     - density signals (spacing rhythms)
3. Group + weight by axis position.

The synthesizer's job (in core.py) is to MIX these primitives along the
brief's axes into a fresh token set — not pick one spec wholesale.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

from engine.data_loader import load_brands
from engine.synthesizer.axes import AxisValues, INDUSTRY_SEEDS, AXIS_NAMES


# Default brand-side axis seeds. Brands without an explicit axis annotation
# inherit their category's seed (same dict the brief uses).
# A brand's category in the spec maps to one of the industry seed keys
# (best-effort fuzzy match).
CATEGORY_TO_INDUSTRY_KEY: Dict[str, str] = {
    "Fintech / Crypto":              "fintech-payments",
    "Fintech / Payments":            "fintech-payments",
    "Fintech / Banking":             "fintech-banking",
    "Fintech":                       "fintech-payments",
    "Developer Tools":               "developer-tools",
    "AI / ML Platform":              "ai-ml",
    "AI / ML":                       "ai-ml",
    "Productivity / Collaboration":  "productivity",
    "SaaS / Developer Tools":        "developer-tools",
    "SaaS / Productivity":           "productivity",
    "SaaS / Project Management":     "productivity",
    "Consumer / Lifestyle / Retail": "consumer-lifestyle",
    "Consumer / Lifestyle":          "consumer-lifestyle",
    "Consumer / Media":              "editorial-media",
    "Editorial / Media":             "editorial-media",
    "Media / Editorial":             "editorial-media",
    "Automotive":                    "automotive",
    "Automotive / Performance":      "automotive",
    "Hospitality / Travel":          "hospitality-travel",
    "Healthcare / Wellness":         "healthcare",
    "E-commerce / Marketplace":      "ecommerce",
    "Gaming / Entertainment":        "gaming",
    "Design Tools":                  "saas",
}


@dataclass
class Vocabulary:
    """A pool of design primitives extracted from N brand exemplars."""
    exemplars: List[Dict[str, Any]] = field(default_factory=list)
    palettes: List[Dict[str, Any]] = field(default_factory=list)
    type_pairs: List[Dict[str, Any]] = field(default_factory=list)
    motion_signals: List[Dict[str, Any]] = field(default_factory=list)
    radius_signals: List[float] = field(default_factory=list)
    spacing_signals: List[float] = field(default_factory=list)
    source_brand_ids: List[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not self.exemplars

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_brand_ids": list(self.source_brand_ids),
            "exemplar_count": len(self.exemplars),
            "palette_anchors": len(self.palettes),
            "type_pair_anchors": len(self.type_pairs),
        }


def _brand_axes(brand: Dict[str, Any]) -> Dict[str, float]:
    """Look up a brand's category → industry seed axes."""
    cat = brand.get("category", "")
    key = CATEGORY_TO_INDUSTRY_KEY.get(cat)
    if not key:
        # Try direct fuzzy match
        for ck in INDUSTRY_SEEDS:
            if ck in cat.lower().replace(" ", "-"):
                key = ck
                break
    if not key:
        return {name: 0.5 for name in AXIS_NAMES}
    return dict(INDUSTRY_SEEDS[key])


def _axis_distance(a: AxisValues, b: Dict[str, float]) -> float:
    """Euclidean distance in 7-D axis space between brief axes and brand axes."""
    diffs = [(getattr(a, name) - b.get(name, 0.5)) ** 2 for name in AXIS_NAMES]
    return sum(diffs) ** 0.5


def pick_exemplars_by_axes(axes: AxisValues, n: int = 8,
                           exclude_brand_ids: Optional[Iterable[str]] = None,
                           ) -> List[Dict[str, Any]]:
    """Return the N brand specs whose category-seed axes are closest to the brief.

    Sort by 7-D euclidean distance. Excludes any brand id passed in
    ``exclude_brand_ids``.

    **Fully deterministic.** Ties are broken by brand id (alphabetical) so
    two brands with identical category-seed axes always resolve in the
    same order across machines, filesystems, and Python versions.
    """
    all_brands = load_brands()
    excluded = {str(b).lower() for b in (exclude_brand_ids or [])}
    scored: List[Tuple[float, str, Dict[str, Any]]] = []
    for b in all_brands:
        bid = (b.get("id") or "").lower()
        if bid in excluded:
            continue
        b_axes = _brand_axes(b)
        dist = _axis_distance(axes, b_axes)
        # Primary: distance. Secondary: brand id (alphabetical, deterministic).
        scored.append((dist, bid, b))
    scored.sort(key=lambda t: (t[0], t[1]))
    return [b for _, _, b in scored[:n]]


def _extract_palette(brand: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pull palette anchors from a brand spec."""
    dl = brand.get("design_language") or {}
    if not isinstance(dl, dict):
        return None
    palette = {}
    for key in ("color_canvas", "color_ink", "color_primary", "color_accent",
                "color_muted", "color_secondary", "color_body"):
        v = dl.get(key)
        if v and isinstance(v, str):
            palette[key.replace("color_", "")] = v
    return palette if palette else None


def _extract_type_pair(brand: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pull type stack from a brand spec."""
    dl = brand.get("design_language") or {}
    if not isinstance(dl, dict):
        return None
    out = {}
    for key in ("typography_display", "typography_body", "typography_mono",
                "font_display", "font_body", "font_mono", "display_font", "body_font"):
        v = dl.get(key)
        if v and isinstance(v, str):
            short_key = key.replace("typography_", "").replace("font_", "").replace("_font", "")
            out[short_key] = v
    return out if out else None


def _extract_radius(brand: Dict[str, Any]) -> Optional[float]:
    """Pull radius (corner roundness) signal from a brand spec.

    Returns a normalized 0.0–1.0 value (0 = sharp, 1 = very rounded).
    """
    dl = brand.get("design_language") or {}
    if not isinstance(dl, dict):
        return None
    r = dl.get("radius")
    if not r:
        return None
    if isinstance(r, (int, float)):
        # Treat 0-32px as the range
        return max(0.0, min(1.0, float(r) / 32.0))
    if isinstance(r, str):
        s = r.strip().lower()
        # Try to extract pixel value
        import re
        m = re.match(r"(\d+(?:\.\d+)?)", s)
        if m:
            return max(0.0, min(1.0, float(m.group(1)) / 32.0))
        # Named radii
        named = {"sharp": 0.0, "minimal": 0.1, "subtle": 0.2, "medium": 0.4,
                 "soft": 0.6, "rounded": 0.75, "pill": 0.95, "full": 1.0}
        for k, v in named.items():
            if k in s:
                return v
    return None


def distill_vocabulary(brands: Iterable[Dict[str, Any]]) -> Vocabulary:
    """Build a vocabulary from N brand specs."""
    vocab = Vocabulary()
    for b in brands:
        bid = b.get("id") or "unknown"
        vocab.exemplars.append(b)
        vocab.source_brand_ids.append(bid)
        pal = _extract_palette(b)
        if pal:
            vocab.palettes.append({"source": bid, **pal})
        tp = _extract_type_pair(b)
        if tp:
            vocab.type_pairs.append({"source": bid, **tp})
        rad = _extract_radius(b)
        if rad is not None:
            vocab.radius_signals.append(rad)
    return vocab
