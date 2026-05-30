"""Brand extraction — capture and carry a source site's identity.

Public surface:
    build_profile(signals) -> BrandProfile
    render_md(profile) -> str
    hue_family(hex) -> str
    image_search_terms(profile, temperature=None) -> list[str]
    score_brand_fidelity(html_text, profile) -> dict
    score_imagery(html_text) -> dict
"""
from engine.brand.extract import (
    BrandProfile, build_profile, render_md, hue_family, anchor_recommendation,
    image_search_terms,
)
from engine.brand.fidelity import score_brand_fidelity, score_imagery

__all__ = [
    "BrandProfile", "build_profile", "render_md", "hue_family",
    "anchor_recommendation", "image_search_terms", "score_brand_fidelity",
    "score_imagery",
]
