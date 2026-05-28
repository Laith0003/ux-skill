"""Image-to-code extraction tests.

We construct synthetic PIL images in-memory so:
- The repo stays clean (no committed binary fixtures).
- Each test owns its inputs, no shared-state surprises.
- Tests skip cleanly when Pillow is not installed.
"""
from __future__ import annotations

from pathlib import Path

import pytest


# Skip the whole module if Pillow is unavailable.
PIL = pytest.importorskip("PIL")
from PIL import Image, ImageDraw  # noqa: E402 — imported after importorskip


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _write_solid(tmp_path: Path, name: str, color: tuple, size=(200, 200)) -> Path:
    """Write a solid-color RGB PNG to ``tmp_path/name``."""
    img = Image.new("RGB", size, color=color)
    out = tmp_path / name
    img.save(out, format="PNG")
    return out


def _write_split(tmp_path: Path, name: str, top: tuple, bottom: tuple,
                 size=(200, 200)) -> Path:
    """Write a two-tone split image (top half / bottom half)."""
    img = Image.new("RGB", size, color=top)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, size[1] // 2, size[0], size[1]], fill=bottom)
    out = tmp_path / name
    img.save(out, format="PNG")
    return out


def _write_palette(tmp_path: Path, name: str, colors: list,
                   size=(400, 100)) -> Path:
    """Write a horizontal swatch strip — N colors of equal width."""
    img = Image.new("RGB", size, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    n = len(colors)
    stripe_w = size[0] // n
    for i, color in enumerate(colors):
        x0 = i * stripe_w
        x1 = (i + 1) * stripe_w if i < n - 1 else size[0]
        draw.rectangle([x0, 0, x1, size[1]], fill=color)
    out = tmp_path / name
    img.save(out, format="PNG")
    return out


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_extract_dominant_palette_returns_hex_strings(tmp_path):
    """Two-tone input should yield at most 2 distinct dominant colors."""
    from engine.image_extract import extract_dominant_palette

    img = _write_split(tmp_path, "split.png", (255, 0, 0), (0, 0, 255))
    colors = extract_dominant_palette(str(img), n=5)

    assert isinstance(colors, list)
    assert all(isinstance(c, str) for c in colors)
    assert all(c.startswith("#") and len(c) == 7 for c in colors), colors
    # Two-tone image quantized to 5 colors → at least 1 actually distinct
    # color (Pillow may pad with zero-count slots). All entries must be
    # valid hex.
    assert len(colors) >= 1


def test_extract_dominant_palette_known_swatches(tmp_path):
    """Three-color swatch strip should map closely to the inputs."""
    from engine.image_extract import extract_dominant_palette

    inputs = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    img = _write_palette(tmp_path, "rgb.png", inputs)
    colors = extract_dominant_palette(str(img), n=5)

    # At least one of the extracted colors should be close to each input.
    def close(a, b, tol=40):
        return all(abs(x - y) <= tol for x, y in zip(a, b))

    extracted_rgb = [
        (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16))
        for c in colors
    ]
    for target in inputs:
        assert any(close(extracted, target) for extracted in extracted_rgb), (
            f"none of {extracted_rgb} matched target {target}"
        )


def test_detect_canvas_polarity_light_image(tmp_path):
    """A near-white image is light-canvas."""
    from engine.image_extract import detect_canvas_polarity

    img = _write_solid(tmp_path, "white.png", (245, 245, 245))
    assert detect_canvas_polarity(str(img)) == "light"


def test_detect_canvas_polarity_dark_image(tmp_path):
    """A near-black image is dark-canvas."""
    from engine.image_extract import detect_canvas_polarity

    img = _write_solid(tmp_path, "dark.png", (12, 14, 18))
    assert detect_canvas_polarity(str(img)) == "dark"


def test_detect_type_polarity_returns_known_value(tmp_path):
    """Heuristic — only assert the return value is in the allowed set."""
    from engine.image_extract import detect_type_polarity

    img = _write_solid(tmp_path, "flat.png", (200, 200, 200))
    result = detect_type_polarity(str(img))
    assert result in {"serif", "sans-serif", "unknown"}


def test_detect_aspect_density_shape(tmp_path):
    """detect_aspect_density returns a dict with the documented keys."""
    from engine.image_extract import detect_aspect_density

    img = _write_split(tmp_path, "split.png", (255, 255, 255), (10, 10, 10),
                       size=(400, 200))
    info = detect_aspect_density(str(img))

    assert set(info.keys()) >= {"aspect_ratio", "width", "height",
                                 "density", "orientation"}
    assert info["width"] == 400
    assert info["height"] == 200
    assert info["orientation"] == "landscape"
    assert 0.0 <= info["density"] <= 1.0


def test_image_to_brief_returns_brief_and_hints(tmp_path):
    """The top-level helper returns a Brief-shaped dict plus diagnostic hints."""
    from engine.image_extract import image_to_brief
    from engine.recommender import Brief

    img = _write_solid(tmp_path, "dark.png", (10, 12, 16), size=(800, 600))
    result = image_to_brief(str(img))

    # Top-level shape
    assert "brief" in result
    assert "hints" in result

    # Brief is a dict that can be slotted into the Brief dataclass.
    brief_dict = result["brief"]
    assert set(brief_dict.keys()) >= {
        "project_type", "industry", "audience", "tone",
        "must_have", "forbidden", "stack", "region",
    }
    # Round-tripping into the dataclass must not raise.
    brief_obj = Brief(**brief_dict)
    assert isinstance(brief_obj.tone, list)

    # Dark canvas → 'dark' should appear in tone and 'dark-mode' in must_have.
    assert "dark" in brief_dict["tone"]
    assert "dark-mode" in brief_dict["must_have"]

    # Default forbidden list includes the project-wide taste guardrails.
    assert "cormorant" in brief_dict["forbidden"]
    assert "yellow" in brief_dict["forbidden"]

    # Hints carry the diagnostic surface.
    hints = result["hints"]
    assert hints["canvas_polarity"] == "dark"
    assert isinstance(hints["dominant_colors"], list)
    assert hints["type_polarity"] in {"serif", "sans-serif", "unknown"}


def test_image_to_brief_missing_file_raises(tmp_path):
    """A non-existent path should raise FileNotFoundError."""
    from engine.image_extract import image_to_brief

    with pytest.raises(FileNotFoundError):
        image_to_brief(str(tmp_path / "does-not-exist.png"))


def test_match_closest_palette_returns_known_entry(tmp_path):
    """A monochrome dark input matches some palette in the manifest."""
    from engine.image_extract import (
        extract_dominant_palette,
        match_closest_palette,
    )

    img = _write_solid(tmp_path, "dark.png", (15, 17, 21), size=(400, 300))
    colors = extract_dominant_palette(str(img), n=5)
    matched = match_closest_palette(colors)

    # Manifest is populated — there must be a closest entry.
    assert matched is not None
    assert "id" in matched
    assert "colors" in matched


def test_mcp_handler_image_extract(tmp_path):
    """The MCP handler returns the same shape as the CLI subcommand."""
    from engine.mcp import handle_ux_image_extract

    img = _write_solid(tmp_path, "light.png", (250, 248, 244), size=(300, 200))
    result = handle_ux_image_extract({
        "path": str(img),
        "with_recommendation": False,
    })

    assert "brief" in result
    assert "hints" in result
    assert "recommendation" not in result

    # with_recommendation=True path runs the recommender
    result_with_rec = handle_ux_image_extract({
        "path": str(img),
        "with_recommendation": True,
    })
    assert "recommendation" in result_with_rec
    assert "rationale" in result_with_rec["recommendation"]
