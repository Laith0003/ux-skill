"""The guidance says what the engine builds.

The engine derives the headline size, the display weight and leading, the
section rhythm, the bands, the frame, motion and the photo direction from
the brand and the axes. These tests hold the reference docs to it: no fixed
ceiling on the headline, no eyebrow as a section separator, centring is not
the calm option, capitals and display faces are open to a loud brand,
photographs are required and sourced by the photo direction, no invented
number, no industry lookups, and the interaction guidance names the roles.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def _read(rel: str) -> str:
    return (REF / rel).read_text(encoding="utf-8")


SLOP = "styles/anti-slop.md"
TYPE = "foundations/typography.md"
LANDING = "surfaces/landing.md"


@pytest.mark.parametrize("rel,phrase", [
    (SLOP, "text-4xl md:text-6xl"),
    (SLOP, "whispers"),
    (SLOP, "pick a 4-step subset"),
    (SLOP, "Use eyebrow tags and whitespace rhythm to separate sections"),
    (SLOP, "Eyebrow tags replace decorative section dividers"),
    (SLOP, "Center alignment when DESIGN_VARIANCE > 4"),
    (SLOP, "Cap at 1200-1400px"),
    (SLOP, "ALL CAPS headlines at >14px"),
    (SLOP, "Decorative or handwritten display faces on premium surfaces"),
    (SLOP, "Cap micro at 300ms"),
    (TYPE, "clamp(3rem, 5vw, 5.5rem)"),
    (TYPE, "Sectioning a long page"),
    (TYPE, "ALL CAPS is reserved for eyebrows"),
    (TYPE, "Display: 600 to 800"),
    (LANDING, "It suits"),
    (LANDING, "an eyebrow above each stat"),
    (LANDING, "DESIGN_VARIANCE is 4 or below"),
    ("foundations/layout.md", "Cap layouts at 1400px"),
    ("foundations/layout.md", "Center-everything fallback at VARIANCE > 4"),
    ("foundations/motion.md", "Never exceed 500ms for UI feedback"),
    ("foundations/color.md", "Palette systems by industry"),
    ("foundations/color.md", "Reserve a true-dark band for one moment per page"),
    ("styles/exemplars.md", "No stock photo."),
])
def test_the_old_ceiling_is_gone(rel, phrase):
    assert phrase not in _read(rel), f"{rel} still says {phrase!r}"


@pytest.mark.parametrize("rel,phrase", [
    (SLOP, "6 to 10 sizes"),
    (SLOP, "character.landing_display_px"),
    (SLOP, "never separates sections"),
    (SLOP, "color.budget.bands"),
    (TYPE, "60 to 240px"),
    (TYPE, "400 to 650"),
    (TYPE, "text-wrap: balance"),
    (LANDING, "bottom start"),
    (LANDING, "in the header"),
    (LANDING, "a labeled draft placeholder"),
    ("foundations/layout.md", "layout.landing.full"),
    ("foundations/motion.md", "motion.settle_ms"),
    ("foundations/motion.md", "grid-template-rows"),
    ("styles/arsenal.md", "motion.scroll"),
])
def test_the_continuous_range_is_stated(rel, phrase):
    assert phrase in _read(rel), f"{rel} does not say {phrase!r}"


def test_photographs_are_required_and_sourced_by_the_photo_direction():
    lines = {
        SLOP: next(ln for ln in _read(SLOP).splitlines() if ln.startswith("| No imagery anywhere")),
        "styles/arsenal.md": next(ln for ln in _read("styles/arsenal.md").splitlines()
                                  if ln.startswith("**Source**: photographs are required")),
        "process/discovery-protocol.md": next(
            ln for ln in _read("process/discovery-protocol.md").splitlines()
            if ln.startswith('**Ask**: "Imagery')),
    }
    for rel, line in lines.items():
        assert "photo direction" in line, rel
        assert "narrow" in line, rel


def test_no_figure_is_invented():
    slop = _read(SLOP)
    assert "labeled draft placeholder" in slop
    import json
    rules = json.loads((ROOT / "data" / "anti-patterns.json").read_text(encoding="utf-8"))["entries"]
    fix = next(e["fix"] for e in rules if e["id"] == "round-number-stats")
    assert "placeholder" in fix and "never invent" in fix.lower()


INDUSTRY = re.compile(
    r"\b(?:fintech|saas|dev(?:eloper)?[ -]tools?|healthcare|health|medical|legal|luxury|e-?commerce"
    r"|retail|banking|insurance|crypto|web3|real estate|hospitality|food|beverage|restaurants?"
    r"|travel|education|kids|gaming|fashion|beauty|wellness|lifestyle|consumer|b2b|enterprise"
    r"|government|civic|agenc(?:y|ies)|startups?|ai products?|ai tooling|creative[ -]tools?"
    r"|finance|security|marketplace|public services|local businesses|consultanc(?:y|ies)"
    r"|events|research)\b", re.I)
DOCS = ("foundations/color.md", TYPE, "foundations/spacing.md", "surfaces/dashboard.md", LANDING,
        "foundations/layout.md", "foundations/motion.md", "styles/arsenal.md")


@pytest.mark.parametrize("rel", DOCS)
def test_no_use_when_line_is_keyed_to_an_industry(rel):
    for line in _read(rel).splitlines():
        if line.startswith(("**Use when**", "**The engine picks it**")) or "It suits" in line:
            assert not INDUSTRY.search(line), (rel, line)


def test_type_pairings_describe_the_pair_not_a_business():
    text = _read(TYPE)
    section = text[text.index("### Font pairings"):]
    section = section[:section.index("\n## ")] if "\n## " in section else section
    for line in section.splitlines():
        if line.startswith("- "):
            assert not INDUSTRY.search(line), line


def test_hover_and_press_come_from_the_roles():
    for path in sorted(REF.rglob("*.md")):
        assert "by aesthetic" not in path.read_text(encoding="utf-8"), path.relative_to(ROOT)
    interaction = _read("foundations/interaction.md")
    for role in ("motion.state", "motion.press.scale"):
        assert role in interaction, role


def test_loading_keeps_the_verb():
    interaction = _read("foundations/interaction.md")
    assert not re.search(r'"(?:Submitting|Saving|Loading|Sending)\.\.\."', interaction)
    assert "keeps its label" in interaction
