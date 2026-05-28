"""Image-to-code capability — pure-CV extraction of design hints from an image.

This module turns a design reference image (PNG/JPG/WebP) into a synthetic
``Brief`` the recommender can act on. It does NOT call a multimodal LLM —
every signal is computed deterministically from pixel data via Pillow.

Public surface
--------------
``extract_dominant_palette(path, n=5)`` -> list of ``#rrggbb`` hex strings
``detect_canvas_polarity(path)``        -> "light" | "dark"
``match_closest_palette(colors)``       -> palette entry dict (or None)
``match_closest_style(colors, polarity)``-> style entry dict (or None)
``detect_type_polarity(path)``          -> "serif" | "sans-serif" | "unknown"
``detect_aspect_density(path)``         -> dict with aspect_ratio + density
``image_to_brief(path)``                -> synthetic Brief-shaped dict
"""
from engine.image_extract.core import (
    detect_aspect_density,
    detect_canvas_polarity,
    detect_type_polarity,
    extract_dominant_palette,
    image_to_brief,
    match_closest_palette,
    match_closest_style,
)

__all__ = [
    "detect_aspect_density",
    "detect_canvas_polarity",
    "detect_type_polarity",
    "extract_dominant_palette",
    "image_to_brief",
    "match_closest_palette",
    "match_closest_style",
]
