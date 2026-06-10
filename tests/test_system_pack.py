"""Tests for the system-pack folder emitter (engine.generator.system_pack).

Locks the contract: a synthesized system emits a full folder (DESIGN.md +
metadata.json + css/tokens.css + preview.html), the derived semantic palette is
accessible (text trio >= 4.5:1, signals readable, on-primary readable), and the
metadata is valid JSON with the full token set.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List

import pytest

from engine.synthesizer import synthesize
from engine.generator.system_pack import pack_system, derive_palette


@dataclass
class _Brief:
    industry: str = ""
    tone: List[str] = field(default_factory=list)
    audience: List[str] = field(default_factory=list)
    must_have: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)
    reference_brands: List[str] = field(default_factory=list)
    strict: bool = False


def _lum(hex_str: str) -> float:
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def test_pack_writes_all_four_files(tmp_path):
    s = synthesize(_Brief(industry="saas", tone=["clean"]))
    r = pack_system(s, "Testsys", "a test system", "concept prose", str(tmp_path))
    root = tmp_path / "testsys"
    assert (root / "DESIGN.md").exists()
    assert (root / "metadata.json").exists()
    assert (root / "css" / "tokens.css").exists()
    assert (root / "preview.html").exists()
    assert r["slug"] == "testsys"
    assert r["wcag_aa_text"] is True


def test_metadata_is_valid_json_with_full_palette(tmp_path):
    s = synthesize(_Brief(industry="luxury"))
    pack_system(s, "Lux", "d", "c", str(tmp_path))
    meta = json.loads((tmp_path / "lux" / "metadata.json").read_text(encoding="utf-8"))
    tokens = {c["token"] for c in meta["palette"]}
    for need in ("canvas", "surface", "ink", "body", "muted", "primary",
                 "on_primary", "success", "warning", "danger", "info"):
        assert need in tokens, f"metadata palette missing {need}"
    assert meta["accessibility"]["wcag_aa_text"] is True
    assert meta["theme"] in ("light", "dark")


def test_tokens_css_has_custom_properties_and_components(tmp_path):
    s = synthesize(_Brief(industry="developer-tools"))
    pack_system(s, "Dev", "d", "c", str(tmp_path))
    css = (tmp_path / "dev" / "css" / "tokens.css").read_text(encoding="utf-8")
    assert "--color-canvas:" in css and "--color-primary:" in css
    assert ".btn-primary" in css and ".card" in css


def test_preview_html_applies_tokens(tmp_path):
    s = synthesize(_Brief(industry="ecommerce", tone=["playful"]))
    pack_system(s, "Pop", "d", "c", str(tmp_path))
    html = (tmp_path / "pop" / "preview.html").read_text(encoding="utf-8")
    assert "var(--color-canvas)" in html and "<h1>" in html
    assert "ux-skill" in html


@pytest.mark.parametrize("brief", [
    _Brief(industry="fintech-payments", tone=["bold"]),
    _Brief(industry="healthcare", tone=["calm"]),
    _Brief(industry="gaming", tone=["loud"]),
    _Brief(industry="editorial-media", tone=["warm"]),
    _Brief(reference_brands=["stripe"]),
    _Brief(reference_brands=["spotify"]),
])
def test_derived_palette_is_accessible(brief):
    """Text trio AA on canvas, signals readable, text on the accent readable."""
    pal = derive_palette(synthesize(brief))
    cv = pal["canvas"]
    for k in ("ink", "body", "muted"):
        assert _contrast(pal[k], cv) >= 4.5, f"{k} {pal[k]} on {cv} = {_contrast(pal[k], cv):.2f}"
    for k in ("success", "warning", "danger", "info"):
        assert _contrast(pal[k], cv) >= 4.4, f"signal {k} {pal[k]} on {cv} = {_contrast(pal[k], cv):.2f}"
    assert _contrast(pal["on_primary"], pal["primary"]) >= 4.4, "text on primary unreadable"
