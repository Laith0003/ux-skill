"""Brand extraction — capture and carry a source site's identity.

Public surface:
    build_profile(signals) -> BrandProfile
    render_md(profile) -> str
    hue_family(hex) -> str
"""
from engine.brand.extract import BrandProfile, build_profile, render_md, hue_family

__all__ = ["BrandProfile", "build_profile", "render_md", "hue_family"]
