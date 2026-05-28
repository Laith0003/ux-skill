"""5-parallel-search reasoning engine — the flagship.

Given a brief (project type, audience, tone, must-haves), the recommender runs
five parallel searches across the v2 manifests and merges the top results into
a single recommended design system.

The five lanes:

1. Industry  -> ``industries.json`` lookup, gives style/palette/type biases.
2. Style     -> ``styles.json`` filtered by industry + brief tags.
3. Palette   -> ``palettes.json`` filtered by style.compatible_palettes.
4. Type      -> ``type-pairs.json`` filtered by style.compatible_type_pairs.
5. Motion    -> ``motion-presets.json`` filtered by style.tokens.motion hints.

Plus auxiliary lanes:
- Components -> ``components.json`` filtered by style compatibility.
- Brands     -> ``data/brands/*.json`` returned as exemplars.
- Anti-slop  -> ``anti-patterns.json`` returned as hard guardrails.

Public surface
--------------
``recommend(brief: Brief) -> Recommendation``
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from engine.data_loader import load, load_brands


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

@dataclass
class Brief:
    """User-supplied design brief.

    Either pass an ``industry`` id directly, or pass loose tags and let the
    engine infer the industry."""

    project_type: str = ""              # "landing" | "dashboard" | "marketing-site" | ...
    industry: str = ""                  # industries.json id, optional
    audience: List[str] = field(default_factory=list)
    tone: List[str] = field(default_factory=list)       # ["warm", "editorial", "precise"]
    must_have: List[str] = field(default_factory=list)  # ["dark-mode", "rtl", "a11y-AA"]
    forbidden: List[str] = field(default_factory=list)  # ["brutalism", "purple-gradients"]
    stack: str = ""                     # tech-stacks.json id
    region: str = ""                    # "mena" | "us" | "eu" | "apac"


@dataclass
class Recommendation:
    style: Optional[Dict[str, Any]] = None
    palette: Optional[Dict[str, Any]] = None
    type_pair: Optional[Dict[str, Any]] = None
    motion: List[Dict[str, Any]] = field(default_factory=list)
    components: List[Dict[str, Any]] = field(default_factory=list)
    brand_exemplars: List[Dict[str, Any]] = field(default_factory=list)
    guardrails: List[Dict[str, Any]] = field(default_factory=list)
    rationale: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Lane implementations
# ---------------------------------------------------------------------------

def _score(entry: Dict[str, Any], brief: Brief) -> float:
    """Rough fit score for an entry against a brief.

    Naive but explainable. Higher = better fit. The recommender prefers
    transparent scoring over learned weights.
    """
    score = 0.0
    tags = set(brief.tone) | set(brief.audience)

    for field_name in ("tone", "character", "characteristics", "tokens"):
        value = entry.get(field_name)
        if isinstance(value, list):
            score += sum(1.0 for t in value if t in tags)
        elif isinstance(value, dict):
            score += sum(1.0 for v in value.values() if isinstance(v, str) and v in tags)

    # Forbidden filter (v2.1 fix — task #52)
    # Apply -100 penalty if entry matches anything in brief.forbidden.
    # Check id, category, AND every typography family name nested in
    # display/body/mono blocks (type-pairs use this shape).
    entry_id = entry.get("id", "")
    entry_cat = entry.get("category", "")
    type_fams = []
    for block_key in ("display", "body", "mono"):
        block = entry.get(block_key)
        if isinstance(block, dict):
            fam = block.get("family")
            if fam:
                type_fams.append(fam.lower().replace(" ", "-"))
                type_fams.append(fam.lower())
    name_lower = (entry.get("name") or "").lower()

    for forbidden in brief.forbidden:
        fbd = forbidden.lower()
        if fbd == entry_id.lower() or fbd == entry_cat.lower():
            return -100.0
        if fbd in name_lower:
            return -100.0
        for fam in type_fams:
            if fbd in fam:
                return -100.0

    return score


def _lane_industry(brief: Brief) -> Dict[str, Any]:
    """Find the industry entry matching the brief.

    v2.1 fix (task #53) — falls back through three matching strategies
    instead of bouncing to score-all on unknown industry IDs:
      1. exact id match
      2. fuzzy match: brief.industry substring in entry.id / name / category
      3. tag-score (the original fallback)
    """
    data = load("industries")
    entries = data.get("entries", [])
    if not entries:
        return {}

    target = (brief.industry or "").strip().lower()

    # Strategy 1: exact id match
    if target:
        for e in entries:
            if (e.get("id") or "").lower() == target:
                return e

        # Strategy 2: fuzzy substring match on id / name / category
        for e in entries:
            haystack = " ".join([
                (e.get("id") or "").lower(),
                (e.get("name") or "").lower(),
                (e.get("category") or "").lower(),
            ])
            if target in haystack or any(
                tok in haystack for tok in target.replace("-", " ").split() if len(tok) > 2
            ):
                return e

    # Strategy 3: tag-score fallback (original behavior)
    ranked = sorted(entries, key=lambda e: _score(e, brief), reverse=True)
    return ranked[0] if ranked else {}


def _lane_style(brief: Brief, industry: Dict[str, Any]) -> Dict[str, Any]:
    data = load("styles")
    entries = data.get("entries", [])
    recommended = set(industry.get("recommended_styles", []))
    avoid = set(industry.get("avoid_styles", []) + brief.forbidden)

    def style_score(e: Dict[str, Any]) -> float:
        sid = e.get("id", "")
        if sid in avoid:
            return -100.0
        s = _score(e, brief)
        if sid in recommended:
            s += 10.0
        return s

    ranked = sorted(entries, key=style_score, reverse=True)
    return ranked[0] if ranked else {}


def _lane_palette(brief: Brief, style: Dict[str, Any]) -> Dict[str, Any]:
    data = load("palettes")
    entries = data.get("entries", [])
    compatible = set(style.get("compatible_palettes", []))
    ranked = sorted(
        entries,
        key=lambda e: (e.get("id") in compatible, _score(e, brief)),
        reverse=True,
    )
    return ranked[0] if ranked else {}


def _lane_type(brief: Brief, style: Dict[str, Any]) -> Dict[str, Any]:
    data = load("type-pairs")
    entries = data.get("entries", [])
    compatible = set(style.get("compatible_type_pairs", []))
    ranked = sorted(
        entries,
        key=lambda e: (e.get("id") in compatible, _score(e, brief)),
        reverse=True,
    )
    return ranked[0] if ranked else {}


def _lane_motion(brief: Brief, style: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = load("motion-presets")
    entries = data.get("entries", [])
    ranked = sorted(entries, key=lambda e: _score(e, brief), reverse=True)
    return ranked[:5]


def _lane_components(style: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = load("components")
    entries = data.get("entries", [])
    sid = style.get("id")
    return [c for c in entries if sid in c.get("compatible_styles", [])][:12]


def _lane_brands(style: Dict[str, Any], industry: Dict[str, Any]) -> List[Dict[str, Any]]:
    brands = load_brands()
    bias = set(industry.get("exemplars", []))
    ranked = sorted(brands, key=lambda b: (b.get("id") in bias, b.get("name", "")))
    return ranked[:5]


def _lane_guardrails() -> List[Dict[str, Any]]:
    """Always-on. The 30 anti-patterns are non-negotiable."""
    data = load("anti-patterns")
    return data.get("entries", [])


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def recommend(brief: Brief) -> Recommendation:
    """Run the 5-parallel-search engine and return a merged recommendation."""

    industry = _lane_industry(brief)

    with ThreadPoolExecutor(max_workers=5) as pool:
        style_future = pool.submit(_lane_style, brief, industry)
        guard_future = pool.submit(_lane_guardrails)
        style = style_future.result()
        palette_future = pool.submit(_lane_palette, brief, style)
        type_future = pool.submit(_lane_type, brief, style)
        motion_future = pool.submit(_lane_motion, brief, style)
        components_future = pool.submit(_lane_components, style)
        brand_future = pool.submit(_lane_brands, style, industry)

        palette = palette_future.result()
        type_pair = type_future.result()
        motion = motion_future.result()
        components = components_future.result()
        brands = brand_future.result()
        guardrails = guard_future.result()

    rationale: List[str] = []
    if industry:
        rationale.append(f"Industry: {industry.get('name', industry.get('id', '—'))}")
    if style:
        rationale.append(f"Style: {style.get('name', style.get('id', '—'))}")
    if palette:
        rationale.append(f"Palette: {palette.get('name', palette.get('id', '—'))}")
    if type_pair:
        rationale.append(f"Type pair: {type_pair.get('name', type_pair.get('id', '—'))}")
    if motion:
        rationale.append(f"Motion presets considered: {len(motion)}")
    if components:
        rationale.append(f"Compatible components: {len(components)}")
    rationale.append(f"Guardrails active: {len(guardrails)} anti-pattern rules")

    return Recommendation(
        style=style or None,
        palette=palette or None,
        type_pair=type_pair or None,
        motion=motion,
        components=components,
        brand_exemplars=brands,
        guardrails=guardrails,
        rationale=rationale,
    )
