"""The landing playbook lays out every composition the engine can choose.

The engine names one of five compositions for each system it builds (decisions/
page-composition.md). The playbook never named them, so an agent had a name and
no layout. Each composition now has its structure, when the engine picks it, the
hero, proof and call to action at 1440 and 375, the Arabic mirror and its
failure mode.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from engine.foundations.composition import DESCRIPTIONS

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "references" / "surfaces" / "landing.md"
PARTS = ("**Structure.**", "**The engine picks it**", "**At 1440.**", "**At 375.**", "**Arabic.**",
         "**It fails when.**")


def _text() -> str:
    return LANDING.read_text(encoding="utf-8")


def _compositions() -> str:
    text = _text()
    start = text.index("## Compositions")
    return text[start:text.index("\n## ", start + 1)]


def _one(name: str) -> str:
    sec = _compositions()
    start = sec.index(f"### {name}")
    nxt = sec.find("\n### ", start + 1)
    return sec[start:nxt if nxt != -1 else len(sec)]


def test_the_section_names_all_five():
    sec = _compositions()
    names = re.findall(r"^### ([a-z-]+)$", sec, re.M)
    assert len(names) == 5 and set(names) == set(DESCRIPTIONS), names


def test_the_section_says_where_the_name_comes_from():
    sec = _compositions()
    assert "system-report.md" in sec and "Page composition" in sec
    assert "decisions/page-composition.md" in sec


@pytest.mark.parametrize("name", sorted(DESCRIPTIONS))
def test_each_composition_has_every_part(name):
    sec = _one(name)
    for part in PARTS:
        assert part in sec, f"{name} lacks {part}"
    for word in ("hero", "proof", "call to action"):
        assert word in sec.lower(), f"{name} does not place the {word}"


@pytest.mark.parametrize("name", sorted(DESCRIPTIONS))
def test_each_composition_uses_token_roles_not_pixels(name):
    sec = _one(name)
    assert re.search(r"`(?:layout|type|imagery|color)\.[a-z.-]+", sec), f"{name} names no token role"
    assert not re.search(r"\b\d{2,3}px\b", sec), f"{name} hard-codes a pixel value; use the role"


def test_editorial_column_says_what_replaces_pull_quotes():
    sec = _one("editorial-column")
    assert "no pull quote" in sec.lower() or "has none" in sec.lower()
    assert "never an invented quote" in sec.lower()


def test_the_scores_named_match_the_engine():
    """The picks follow the terms in engine/foundations/composition.py."""
    expect = {
        "split": ("formality", "contrast", "cool"),
        "stacked": ("age", "airy", "muted contrast"),
        "bento": ("density", "contrast", "geometric", "glance"),
        "editorial-column": ("humanist", "formality", "long reading"),
        "full-bleed-media": ("warmth", "playful", "motion"),
    }
    for name, words in expect.items():
        line = next(ln for ln in _one(name).splitlines() if ln.startswith("**The engine picks it**"))
        for w in words:
            assert w in line.lower(), f"{name}: the pick line lacks {w!r}"


def _part(sec: str, label: str) -> str:
    line = next(ln for ln in sec.splitlines() if ln.startswith(label))
    return line.lower()


@pytest.mark.parametrize("name", sorted(DESCRIPTIONS))
@pytest.mark.parametrize("width", ["**At 1440.**", "**At 375.**"])
def test_each_width_places_the_hero_the_proof_and_the_call_to_action(name, width):
    part = _part(_one(name), width)
    for word in ("hero", "proof", "call to action"):
        assert word in part, f"{name} {width} does not place the {word}"


def test_the_shared_rules_name_the_landing_tokens():
    sec = _compositions()
    shared = sec[:sec.index("### ")]
    assert "`type.text.display`" in shared and "`layout.landing-gap.<tier>`" in shared
    assert "where it has one" not in shared
