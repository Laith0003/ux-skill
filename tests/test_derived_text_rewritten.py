"""Guidance derived from an MIT-licensed skill is in our own words.

NOTICE credits the source for the dial model and some pattern vocabulary.
The passages that came across word for word, and the phrases the study of
that skill listed as shared, are rewritten; these tests keep them out.
"""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = sorted(p for folder in ("commands", "agents", "references")
              for p in (ROOT / folder).rglob("*.md"))

SHARED = ("w-[calc(33%-1rem)]", "inset_0_1px_0_rgba(255,255,255,0.1)", "QUESTION 05",
          "stiffness: 100, damping: 20", "min-h-[100dvh]", "grid-flow-dense",
          "\"Jane Doe\" effect", "button-in-button", "design-taste-frontend",
          "perfect symmetry", "artsy chaos", "1 art gallery", "1 art-gallery",
          "deepest OLED black", "near-vantablack", "unbelievably soft", "glass plate catching light",
          "Vibe archetypes")


@pytest.mark.parametrize("phrase", SHARED)
def test_the_shared_phrase_is_gone(phrase):
    hits = [str(p.relative_to(ROOT)) for p in DOCS
            if phrase.lower() in p.read_text(encoding="utf-8").lower()]
    assert not hits, f"{phrase!r} still in {hits}"


def test_the_notice_stays():
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    assert "taste-skill" in notice and "MIT License" in notice


def test_the_dials_are_described_in_our_words():
    design = (ROOT / "commands" / "ux-design.md").read_text(encoding="utf-8")
    step = design[design.index("### 3. Set the dials"):design.index("### 4.")]
    for dial in ("DESIGN_VARIANCE", "MOTION_INTENSITY", "VISUAL_DENSITY"):
        assert dial in step
    assert "axes" in step
