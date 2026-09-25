"""7-axis derivation from a Brief.

Each axis is a continuous 0.0–1.0 value derived deterministically from the
brief's industry, tone, audience, must-haves, and forbidden-list. No
randomness, no LLM — same brief always yields the same axis values.

Axis semantics:

| Axis              | 0.0 end          | 1.0 end          |
|-------------------|------------------|------------------|
| warmth            | cold / clinical  | warm / inviting  |
| contrast          | flat / muted     | dramatic / loud  |
| density           | airy / sparse    | dense / packed   |
| geometry          | sharp / angular  | soft / rounded   |
| formality         | playful          | corporate        |
| motion            | still / minimal  | kinetic / active |
| type_personality  | geometric        | humanist         |

The mapping uses keyword dictionaries — each tag pushes axes one way or
the other. Industry defaults seed the values; brief tags adjust them.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional, Tuple


AXIS_NAMES = (
    "warmth",
    "contrast",
    "density",
    "geometry",
    "formality",
    "motion",
    "type_personality",
)


# Industry → axis seeds. Sensible neutral midpoint when the industry is
# unknown is 0.5 across the board.
INDUSTRY_SEEDS: Dict[str, Dict[str, float]] = {
    "fintech-payments":     {"warmth": 0.35, "contrast": 0.55, "density": 0.6, "geometry": 0.4, "formality": 0.75, "motion": 0.45, "type_personality": 0.4},
    "fintech-banking":      {"warmth": 0.3,  "contrast": 0.4,  "density": 0.6, "geometry": 0.4, "formality": 0.8,  "motion": 0.35, "type_personality": 0.35},
    "fintech-trading":      {"warmth": 0.2,  "contrast": 0.75, "density": 0.85, "geometry": 0.3, "formality": 0.8, "motion": 0.55, "type_personality": 0.3},
    "developer-tools":      {"warmth": 0.3,  "contrast": 0.7,  "density": 0.6, "geometry": 0.3, "formality": 0.55, "motion": 0.4,  "type_personality": 0.3},
    "ai-ml":                {"warmth": 0.35, "contrast": 0.65, "density": 0.55, "geometry": 0.35, "formality": 0.5, "motion": 0.55, "type_personality": 0.4},
    "saas":                 {"warmth": 0.4,  "contrast": 0.5,  "density": 0.55, "geometry": 0.45, "formality": 0.6, "motion": 0.4,  "type_personality": 0.5},
    "productivity":         {"warmth": 0.45, "contrast": 0.5,  "density": 0.55, "geometry": 0.55, "formality": 0.55, "motion": 0.4, "type_personality": 0.5},
    "ecommerce":            {"warmth": 0.65, "contrast": 0.6,  "density": 0.55, "geometry": 0.55, "formality": 0.45, "motion": 0.55, "type_personality": 0.65},
    "consumer-lifestyle":   {"warmth": 0.7,  "contrast": 0.5,  "density": 0.4,  "geometry": 0.7, "formality": 0.35, "motion": 0.6,  "type_personality": 0.7},
    "luxury":               {"warmth": 0.55, "contrast": 0.7,  "density": 0.3,  "geometry": 0.55, "formality": 0.75, "motion": 0.4,  "type_personality": 0.75},
    "editorial-media":      {"warmth": 0.6,  "contrast": 0.65, "density": 0.65, "geometry": 0.55, "formality": 0.65, "motion": 0.45, "type_personality": 0.8},
    "automotive":           {"warmth": 0.45, "contrast": 0.85, "density": 0.55, "geometry": 0.35, "formality": 0.7,  "motion": 0.75, "type_personality": 0.4},
    "healthcare":           {"warmth": 0.7,  "contrast": 0.4,  "density": 0.5,  "geometry": 0.75, "formality": 0.7,  "motion": 0.3,  "type_personality": 0.7},
    "hospitality-travel":   {"warmth": 0.75, "contrast": 0.5,  "density": 0.35, "geometry": 0.65, "formality": 0.5,  "motion": 0.5,  "type_personality": 0.75},
    "gaming":               {"warmth": 0.5,  "contrast": 0.85, "density": 0.7,  "geometry": 0.35, "formality": 0.3,  "motion": 0.85, "type_personality": 0.45},
    "crypto":               {"warmth": 0.25, "contrast": 0.85, "density": 0.7,  "geometry": 0.3,  "formality": 0.55, "motion": 0.7,  "type_personality": 0.3},
    "education":            {"warmth": 0.6,  "contrast": 0.5,  "density": 0.5,  "geometry": 0.6,  "formality": 0.5,  "motion": 0.45, "type_personality": 0.65},
    # Sturdy and square: plain type, firm contrast, little motion.
    "construction":         {"warmth": 0.45, "contrast": 0.6,  "density": 0.55, "geometry": 0.3,  "formality": 0.65, "motion": 0.35, "type_personality": 0.35},
    # A trade catalog: dense, practical, plain type.
    "b2b-marketplace":      {"warmth": 0.45, "contrast": 0.5,  "density": 0.65, "geometry": 0.45, "formality": 0.6,  "motion": 0.4,  "type_personality": 0.4},
    # Cool, formal and exact.
    "security":             {"warmth": 0.25, "contrast": 0.65, "density": 0.55, "geometry": 0.3,  "formality": 0.8,  "motion": 0.35, "type_personality": 0.25},
    # Clinical supply: calmer and denser than care, less warm.
    "pharmacy":             {"warmth": 0.5,  "contrast": 0.45, "density": 0.6,  "geometry": 0.55, "formality": 0.65, "motion": 0.35, "type_personality": 0.45},
}

# Other names for a seeded industry. Each points at a key of INDUSTRY_SEEDS,
# so the name reaches the same axis seed; it never names a look.
INDUSTRY_ALIASES: Dict[str, str] = {
    "building-materials": "construction",
    "wholesale": "b2b-marketplace",
    "cybersecurity": "security",
    "medical-supply": "pharmacy",
}


# Tone tag → axis nudges. Each entry pushes the named axis by ±delta.
# Applied additively after the industry seed.
TONE_NUDGES: Dict[str, Dict[str, float]] = {
    # warmth
    "warm":         {"warmth": +0.20},
    "inviting":     {"warmth": +0.15},
    "human":        {"warmth": +0.15, "type_personality": +0.15},
    "friendly":     {"warmth": +0.20, "formality": -0.15},
    "cool":         {"warmth": -0.15},
    "clinical":     {"warmth": -0.25, "formality": +0.20},
    "cold":         {"warmth": -0.20},

    # contrast / drama
    "bold":         {"contrast": +0.25, "motion": +0.10},
    "dramatic":     {"contrast": +0.30, "geometry": -0.10},
    "loud":         {"contrast": +0.30, "density": +0.10},
    "subtle":       {"contrast": -0.20},
    "muted":        {"contrast": -0.25, "warmth": -0.05},
    "quiet":        {"contrast": -0.25, "density": -0.15},

    # density
    "minimal":      {"density": -0.30, "contrast": -0.10},
    "spacious":     {"density": -0.25},
    "airy":         {"density": -0.25, "warmth": +0.05},
    "dense":        {"density": +0.30},
    "data-heavy":   {"density": +0.30, "formality": +0.10},
    "compact":      {"density": +0.20},

    # geometry
    "sharp":        {"geometry": -0.25, "type_personality": -0.15},
    "angular":      {"geometry": -0.20},
    "soft":         {"geometry": +0.25, "warmth": +0.10},
    "rounded":      {"geometry": +0.25, "warmth": +0.10},
    "organic":      {"geometry": +0.30, "type_personality": +0.15},

    # formality
    "serious":      {"formality": +0.20},
    "professional": {"formality": +0.20, "geometry": -0.05},
    "corporate":    {"formality": +0.25, "warmth": -0.10},
    "trustworthy":  {"formality": +0.20, "contrast": -0.05},
    "casual":       {"formality": -0.25, "warmth": +0.10},
    "playful":      {"formality": -0.30, "warmth": +0.15, "motion": +0.10},
    "irreverent":   {"formality": -0.25, "contrast": +0.10},

    # motion
    "kinetic":      {"motion": +0.25, "contrast": +0.10},
    "energetic":    {"motion": +0.25, "warmth": +0.10},
    "calm":         {"motion": -0.20},
    "still":        {"motion": -0.30},
    "static":       {"motion": -0.35},

    # type
    "editorial":    {"type_personality": +0.25, "density": +0.10},
    "geometric":    {"type_personality": -0.25},
    "humanist":     {"type_personality": +0.25, "warmth": +0.10},
    "technical":    {"type_personality": -0.20, "formality": +0.10},
    "precise":      {"type_personality": -0.15, "geometry": -0.10},

    # Common brief words, each weighted by what it says about the axes.
    "fast":         {"motion": +0.20, "density": +0.05},
    "quick":        {"motion": +0.15},
    "dynamic":      {"motion": +0.25, "contrast": +0.05},
    "lively":       {"motion": +0.20, "warmth": +0.10},
    "fresh":        {"motion": +0.10, "warmth": +0.05, "contrast": +0.05},
    "stable":       {"motion": -0.15, "formality": +0.10},
    "clear":        {"density": -0.15, "contrast": +0.10},
    "simple":       {"density": -0.20, "contrast": -0.05, "type_personality": -0.05},
    "clean":        {"density": -0.15, "contrast": -0.05},
    "efficient":    {"density": +0.15, "type_personality": -0.10},
    "functional":   {"density": +0.10, "formality": +0.05, "type_personality": -0.10},
    "premium":      {"density": -0.15, "contrast": +0.10, "formality": +0.15},
    "elegant":      {"type_personality": +0.20, "density": -0.15, "formality": +0.10},
    "practical":    {"formality": +0.05, "type_personality": -0.15, "density": +0.05,
                     "motion": -0.05},
    "solid":        {"contrast": +0.10, "geometry": -0.10, "formality": +0.05, "motion": -0.05},
    "robust":       {"contrast": +0.10, "geometry": -0.15},
    "crisp":        {"contrast": +0.10, "geometry": -0.15},
    "direct":       {"contrast": +0.10, "formality": +0.05, "motion": -0.05},
    "vibrant":      {"contrast": +0.20, "warmth": +0.10},
    "gentle":       {"contrast": -0.15, "geometry": +0.15, "motion": -0.10},
    "smooth":       {"geometry": +0.15, "motion": +0.05},
    "modern":       {"type_personality": -0.15, "warmth": -0.05, "density": -0.05},
    "innovative":   {"type_personality": -0.10, "motion": +0.10},
    "reliable":     {"formality": +0.10, "motion": -0.05},
    "trusted":      {"formality": +0.15, "contrast": -0.05},
    "secure":       {"formality": +0.20, "warmth": -0.10, "motion": -0.10},
    "expert":       {"formality": +0.15, "type_personality": -0.05},
    "approachable": {"warmth": +0.15, "formality": -0.10},
    "welcoming":    {"warmth": +0.20},
    "caring":       {"warmth": +0.20, "geometry": +0.10},
}

# The most a brief's character object moves one axis, either way. The host
# AI passes what a word the engine does not read means as these nudges.
NUDGE_LIMIT = 0.3


# A word's formality weight also reaches geometry and type personality,
# in proportion to it: a playful word (formality down) rounds the corners
# and humanizes the type, a formal word (formality up) sharpens the
# corners. Type personality moves on the playful side only, since formal
# type can be a serif or a grotesque. Continuous in the weight, so two
# words with close formality weights move the shape by close amounts.
GEOMETRY_PER_FORMALITY = -0.6
TYPE_PER_PLAYFULNESS = 0.5


def word_weights(nudge: Dict[str, float]) -> Dict[str, float]:
    """A tone word's axis weights with its formality weight carried to
    geometry and type personality (GEOMETRY_PER_FORMALITY,
    TYPE_PER_PLAYFULNESS)."""
    out = dict(nudge)
    formality = nudge.get("formality", 0.0)
    if formality:
        out["geometry"] = out.get("geometry", 0.0) + GEOMETRY_PER_FORMALITY * formality
        playful = max(0.0, -formality)
        if playful:
            out["type_personality"] = out.get("type_personality", 0.0) \
                + TYPE_PER_PLAYFULNESS * playful
    return out


# Forbidden tag → forced clamps. Used to clip axes hard.
FORBIDDEN_CLAMPS: Dict[str, Tuple[str, Tuple[float, float]]] = {
    "playful":       ("formality", (0.6, 1.0)),
    "loud":          ("contrast", (0.0, 0.5)),
    "dense":         ("density",  (0.0, 0.55)),
    "brutalism":     ("geometry", (0.3, 1.0)),
    "rounded":       ("geometry", (0.0, 0.55)),
    "soft":          ("geometry", (0.0, 0.55)),
    "warm-tones":    ("warmth",   (0.0, 0.45)),
    "cool-tones":    ("warmth",   (0.55, 1.0)),
}


@dataclass(frozen=True)
class AxisValues:
    """A 7-axis design position for one brief."""
    warmth: float
    contrast: float
    density: float
    geometry: float
    formality: float
    motion: float
    type_personality: float

    def to_dict(self) -> Dict[str, float]:
        return {k: round(v, 3) for k, v in asdict(self).items()}

    def as_tuple(self) -> Tuple[float, ...]:
        return (self.warmth, self.contrast, self.density, self.geometry,
                self.formality, self.motion, self.type_personality)


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def _normalize_tag(tag: str) -> str:
    return (tag or "").strip().lower()


def _seed_from_industry(industry: Optional[str]) -> Dict[str, float]:
    """Look up the industry seed, fuzzy on substring if exact id misses."""
    if not industry:
        return {name: 0.5 for name in AXIS_NAMES}
    key = "-".join(_normalize_tag(industry).split())
    if not key:
        return {name: 0.5 for name in AXIS_NAMES}
    if key in INDUSTRY_SEEDS:
        return dict(INDUSTRY_SEEDS[key])
    if key in INDUSTRY_ALIASES:
        return dict(INDUSTRY_SEEDS[INDUSTRY_ALIASES[key]])
    # fuzzy: substring match, on the seeds and then on their other names
    for k, v in INDUSTRY_SEEDS.items():
        if key in k or k in key:
            return dict(v)
    for k, seed in INDUSTRY_ALIASES.items():
        if key in k or k in key:
            return dict(INDUSTRY_SEEDS[seed])
    return {name: 0.5 for name in AXIS_NAMES}


def _apply_tone_nudges(axes: Dict[str, float], tags: Iterable[str]) -> Dict[str, float]:
    for raw in tags:
        tag = _normalize_tag(raw)
        if not tag:
            continue
        nudge = TONE_NUDGES.get(tag)
        if not nudge:
            # Try multi-word tags by hyphenating
            tag2 = tag.replace(" ", "-")
            nudge = TONE_NUDGES.get(tag2)
        if not nudge:
            continue
        for axis, delta in word_weights(nudge).items():
            axes[axis] = _clamp(axes[axis] + delta)
    return axes


def _apply_character(axes: Dict[str, float], nudges: Any) -> Dict[str, float]:
    """A brief's character object: each named axis moves by its nudge,
    held to NUDGE_LIMIT either way, after the words. The build's inputs
    check the object and name a bad entry; here an entry that is not a
    number is skipped."""
    if not isinstance(nudges, dict):
        return axes
    for axis in AXIS_NAMES:
        value = nudges.get(axis)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        axes[axis] = _clamp(axes[axis] + _clamp(float(value), -NUDGE_LIMIT, NUDGE_LIMIT))
    return axes


def _apply_forbidden_clamps(axes: Dict[str, float], forbidden: Iterable[str]) -> Dict[str, float]:
    for raw in forbidden:
        tag = _normalize_tag(raw)
        clamp_spec = FORBIDDEN_CLAMPS.get(tag)
        if not clamp_spec:
            continue
        axis_name, (lo, hi) = clamp_spec
        axes[axis_name] = _clamp(axes[axis_name], lo, hi)
    return axes


def compute_axes(brief: Any) -> AxisValues:
    """Derive the 7-axis position from a Brief.

    Accepts the v2 ``engine.recommender.Brief`` dataclass OR a plain dict
    with the same field names — so callers can use either.

    The math is deterministic: same brief → same axes. No randomness.
    """
    # Defensive accessor for both Brief dataclass and dict
    def g(field_name: str, default=None):
        if hasattr(brief, field_name):
            return getattr(brief, field_name)
        if isinstance(brief, dict):
            return brief.get(field_name, default)
        return default

    industry = g("industry", "") or g("industry_id", "")
    tone = list(g("tone", []) or [])
    audience = list(g("audience", []) or [])
    must_have = list(g("must_have", []) or [])
    forbidden = list(g("forbidden", []) or [])

    # 1. Seed from industry
    axes = _seed_from_industry(industry)

    # 2. Apply tone + audience tag nudges (audience tags can also be tonal)
    axes = _apply_tone_nudges(axes, list(tone) + list(audience))

    # 3. Must-have tags can nudge too — "data-heavy" must imply density up
    axes = _apply_tone_nudges(axes, must_have)

    # 4. The character object's nudges, after the words
    axes = _apply_character(axes, g("character", None))

    # 5. Forbidden tags clamp axes hard
    axes = _apply_forbidden_clamps(axes, forbidden)

    # 6. Build the frozen value object
    return AxisValues(
        warmth=axes["warmth"],
        contrast=axes["contrast"],
        density=axes["density"],
        geometry=axes["geometry"],
        formality=axes["formality"],
        motion=axes["motion"],
        type_personality=axes["type_personality"],
    )
