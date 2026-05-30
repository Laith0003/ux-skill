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

import colorsys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

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
    brand: Optional[Dict[str, Any]] = None  # extracted BrandProfile dict; anchors palette/type


@dataclass
class Recommendation:
    style: Optional[Dict[str, Any]] = None
    palette: Optional[Dict[str, Any]] = None
    type_pair: Optional[Dict[str, Any]] = None
    motion: List[Dict[str, Any]] = field(default_factory=list)
    components: List[Dict[str, Any]] = field(default_factory=list)
    brand_exemplars: List[Dict[str, Any]] = field(default_factory=list)
    guardrails: List[Dict[str, Any]] = field(default_factory=list)
    brand: Optional[Dict[str, Any]] = None           # set when brand-anchored (rule 2)
    type_directive: Optional[Dict[str, Any]] = None  # logo-style type directive
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


# ---------------------------------------------------------------------------
# Anti-slop palette guardrail (dogfood fix)
# ---------------------------------------------------------------------------
# AI design defaults to a blue-indigo-violet "blurple" primary (the #5e6ad2
# zone). We de-prioritize that band by default and hard-exclude it when the
# brief forbids purple/violet. The whole zone is treated as one region so the
# blue/violet boundary (#5e6ad2 reads as ~234deg "blue" by strict bins) cannot
# slip the filter when a user forbids "purple".
_SLOP_HUE_LO = 215.0
_SLOP_HUE_HI = 295.0
_SLOP_FORBID_WORDS = {
    "purple", "purples", "purple-gradient", "purple-gradients",
    "violet", "indigo", "blurple", "blue-gradient", "blue-gradients",
}


def _hex_to_hsv(hexstr):
    """Parse '#rrggbb' (or '#rgb') into (hue_degrees, saturation, value)."""
    if not isinstance(hexstr, str):
        return None
    s = hexstr.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        return None
    try:
        r = int(s[0:2], 16) / 255.0
        g = int(s[2:4], 16) / 255.0
        b = int(s[4:6], 16) / 255.0
    except ValueError:
        return None
    h, sat, val = colorsys.rgb_to_hsv(r, g, b)
    return (h * 360.0, sat, val)


def _primary_in_slop_band(entry: Dict[str, Any]) -> bool:
    """True if a palette's primary sits in the blue-violet AI-slop zone."""
    colors = entry.get("colors") or {}
    hsv = _hex_to_hsv(colors.get("primary"))
    if not hsv:
        return False
    hue, sat, val = hsv
    return _SLOP_HUE_LO <= hue <= _SLOP_HUE_HI and sat >= 0.30 and val >= 0.30


def _palette_color_penalty(entry: Dict[str, Any], brief: Brief) -> float:
    """Anti-slop-by-default guardrail for palette primaries.

    Returns -100 (hard exclude) when the brief forbids purple/violet and this
    palette's primary is in the slop band; -8 (mild, always-on) for any
    slop-band primary so the engine never *defaults* to AI blurple; 0 otherwise.
    A brief that genuinely wants blurple omits the forbid, and the mild penalty
    is easily out-scored by a strong tag or compatibility match.
    """
    if not _primary_in_slop_band(entry):
        return 0.0
    forbid = {str(f).lower().strip() for f in (brief.forbidden or [])}
    if forbid & _SLOP_FORBID_WORDS:
        return -100.0
    return -8.0


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

    # v3.0: pre-score then run through the decisions re-ranker, then sort
    scored = [(e, style_score(e)) for e in entries]
    valid = [(e, s) for (e, s) in scored if s > -50]
    valid = _rerank_from_decisions(valid, brief, key="picked_style")
    ranked = sorted(valid, key=lambda es: es[1], reverse=True)
    return ranked[0][0] if ranked else {}


def _lane_palette(brief: Brief, style: Dict[str, Any]) -> Dict[str, Any]:
    data = load("palettes")
    entries = data.get("entries", [])
    compatible = set(style.get("compatible_palettes", []))
    scored = [(e, _score(e, brief) + _palette_color_penalty(e, brief)) for e in entries]
    valid = [(e, s) for (e, s) in scored if s > -50]
    # v3.0: bump entries that won in prior similar decisions
    valid = _rerank_from_decisions(valid, brief, key="picked_palette")
    ranked = sorted(
        valid,
        key=lambda es: (es[0].get("id") in compatible, es[1]),
        reverse=True,
    )
    return ranked[0][0] if ranked else {}


def _lane_type(brief: Brief, style: Dict[str, Any]) -> Dict[str, Any]:
    data = load("type-pairs")
    entries = data.get("entries", [])
    compatible = set(style.get("compatible_type_pairs", []))
    scored = [(e, _score(e, brief)) for e in entries]
    valid = [(e, s) for (e, s) in scored if s > -50]
    # v3.0: bump entries that won in prior similar decisions
    valid = _rerank_from_decisions(valid, brief, key="picked_type_pair")
    ranked = sorted(
        valid,
        key=lambda es: (es[0].get("id") in compatible, es[1]),
        reverse=True,
    )
    return ranked[0][0] if ranked else {}


def _lane_motion(brief: Brief, style: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = load("motion-presets")
    entries = data.get("entries", [])
    scored = [(e, _score(e, brief)) for e in entries]
    valid_pairs = [(e, s) for (e, s) in scored if s > -50]
    # v3.0: bump entries that won in prior similar decisions
    valid_pairs = _rerank_from_decisions(valid_pairs, brief, key="picked_motion")
    ranked = sorted(valid_pairs, key=lambda es: es[1], reverse=True)
    return [e for e, _ in ranked[:5]]


def _lane_components(style: Dict[str, Any], brief: Brief = None) -> List[Dict[str, Any]]:
    data = load("components")
    entries = data.get("entries", [])
    sid = style.get("id")
    compat = [c for c in entries if sid in c.get("compatible_styles", [])]
    # v2.2 fix (task #57): when called with a brief, drop forbidden components.
    if brief is not None:
        compat = [c for c in compat if _score(c, brief) > -50]
    return compat[:12]


def _lane_brands(style: Dict[str, Any], industry: Dict[str, Any],
                 brief: Optional[Brief] = None) -> List[Dict[str, Any]]:
    brands = load_brands()
    bias = set(industry.get("exemplars", []))
    ranked = sorted(brands, key=lambda b: (not (b.get("id") in bias), b.get("name", "")))
    # v3.0: re-rank by past wins in this bucket
    if brief is not None:
        ranked = _rerank_brands_from_decisions(ranked, brief)
    return ranked[:5]


def _lane_guardrails() -> List[Dict[str, Any]]:
    """Always-on. The 30 anti-patterns are non-negotiable."""
    data = load("anti-patterns")
    return data.get("entries", [])


# ---------------------------------------------------------------------------
# v3.0 — decisions-driven re-rank (the actual learning loop)
# ---------------------------------------------------------------------------

# Cold-start threshold. Below this many matching prior decisions, fall back
# to the manifest-only ranking. Prevents learning-from-N=1.
_REROUTE_MIN_PRIORS = 3

# Bump per matching prior decision (lint_score >= 80 AND user_accepted=true).
_REROUTE_BUMP = 5.0


def _rerank_from_decisions(
    entries_with_scores: List[Tuple[Dict[str, Any], float]],
    brief: Brief,
    key: str,
) -> List[Tuple[Dict[str, Any], float]]:
    """Bump entries whose id appears in the local decisions ledger with
    ``lint_score >= 80`` AND ``user_accepted=true`` for the same
    ``(industry, ui_type)`` bucket.

    **This is the actual closing of the intelligence loop.** Before this
    call, decisions were logged but never consumed; the recommender behaved
    like v2.0. After this call, ux-skill genuinely learns from its own
    history without ever calling an LLM.

    Cold-start safe: below 3 matching priors, returns the input untouched.

    Args:
        entries_with_scores: list of (entry, score) tuples
        brief:              the active Brief
        key:                which decision field to match (e.g. "picked_style",
                            "picked_palette", "picked_brand")

    Returns:
        A new list of (entry, possibly_bumped_score) tuples.
    """
    try:
        from engine.decisions import query
    except Exception:
        return entries_with_scores

    try:
        hits = query(
            industry=getattr(brief, "industry", None) or None,
            ui_type=getattr(brief, "project_type", None) or None,
            min_score=80,
            accepted_only=True,
        )
    except Exception:
        return entries_with_scores

    if len(hits) < _REROUTE_MIN_PRIORS:
        return entries_with_scores  # cold start

    # Count how often each id won in this bucket
    win_counts: Dict[str, int] = {}
    for h in hits:
        v = h.get(key)
        if v:
            win_counts[str(v).lower()] = win_counts.get(str(v).lower(), 0) + 1

    if not win_counts:
        return entries_with_scores

    # Apply bumps
    out: List[Tuple[Dict[str, Any], float]] = []
    for e, s in entries_with_scores:
        eid = str(e.get("id", "")).lower()
        bumped = s + win_counts.get(eid, 0) * _REROUTE_BUMP
        out.append((e, bumped))
    return out


def _rerank_brands_from_decisions(
    brands: List[Dict[str, Any]],
    brief: Brief,
) -> List[Dict[str, Any]]:
    """Same idea, applied to the brand exemplar list."""
    try:
        from engine.decisions import query
    except Exception:
        return brands
    try:
        hits = query(
            industry=getattr(brief, "industry", None) or None,
            ui_type=getattr(brief, "project_type", None) or None,
            min_score=80,
            accepted_only=True,
        )
    except Exception:
        return brands
    if len(hits) < _REROUTE_MIN_PRIORS:
        return brands
    win_counts: Dict[str, int] = {}
    for h in hits:
        v = h.get("picked_brand")
        if v:
            win_counts[str(v).lower()] = win_counts.get(str(v).lower(), 0) + 1
    if not win_counts:
        return brands
    # Stable sort: prior winners first (by win count, then by original order)
    return sorted(
        brands,
        key=lambda b: -win_counts.get(str(b.get("id", "")).lower(), 0),
    )


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
        components_future = pool.submit(_lane_components, style, brief)
        brand_future = pool.submit(_lane_brands, style, industry, brief)

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

    rec = Recommendation(
        style=style or None,
        palette=palette or None,
        type_pair=type_pair or None,
        motion=motion,
        components=components,
        brand_exemplars=brands,
        guardrails=guardrails,
        rationale=rationale,
    )

    # Brand anchor (rule 2): if the brief carries an EXTRACTED brand profile, the
    # client's logo + primary color OVERRIDE the engine's palette/type pick, so
    # generation uses THEIR brand instead of the house style. Deterministic; only
    # active when brief.brand is set (no brand -> byte-identical to before).
    if getattr(brief, "brand", None):
        from engine.brand import anchor_recommendation
        from engine.brand.extract import BrandProfile
        raw = brief.brand
        prof = raw if isinstance(raw, BrandProfile) else BrandProfile(
            **{k: v for k, v in raw.items() if k in BrandProfile.__dataclass_fields__})
        if prof.primary or prof.name or prof.logo:
            anchored = anchor_recommendation(rec.to_dict(), prof)
            rec.palette = anchored.get("palette")
            rec.brand = anchored.get("brand")
            rec.type_directive = anchored.get("type_directive")
            rec.rationale.append(
                "Brand-anchored to %s — palette primary %s from the logo (not the "
                "engine pick); type matches the logo style."
                % (prof.name or "the source brand", prof.primary or "n/a"))
    return rec
