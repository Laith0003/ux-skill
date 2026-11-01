"""The product illustration guide: the rules for a picture of the product's
interface on a page, distilled from Stageshow and credited in NOTICE.

It loads beside a surface playbook, never as one; it keeps the photo rule;
it names the export that dresses a Stageshow illustration in the system;
and the dashboard playbook carries its flat failure as a principle."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = "references/styles/product-illustration.md"


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_the_guide_credits_its_source_and_notice_carries_the_licence():
    assert "Stageshow" in _read(GUIDE) and "NOTICE" in _read(GUIDE)
    notice = _read("NOTICE")
    assert "github.com/benjitaylor/skills" in notice
    assert "Copyright (c) 2026 Benji Taylor" in notice and notice.count("MIT License") >= 2


def test_the_landing_playbook_and_ux_design_point_at_the_guide():
    assert GUIDE in _read("references/surfaces/landing.md")
    assert GUIDE in _read("commands/ux-design.md")


def test_the_guide_is_not_a_surface_playbook():
    assert not (ROOT / "references" / "surfaces" / "product-illustration.md").exists()
    assert "not a surface playbook" in _read(GUIDE)


def test_photographs_stay_beside_an_illustration():
    text = _read(GUIDE)
    assert "**Photographs stay.**" in text
    assert "never stands in for the photographs" in text


def test_the_export_it_names_exists():
    from engine.io.commands import TARGETS
    text = _read(GUIDE)
    assert "--to stageshow" in text and "stageshow" in TARGETS
    assert 'className="ux-look"' in text


# Stageshow's own phrasings: the guide restates its rules, never its words.
STAGESHOW_PHRASES = (
    "the more detail, the more it looks generated", "the eye has nowhere to land",
    "between a richer story and a calmer frame", "the page is the ground",
    "a light pass does not prove", "most of the quality is decided",
    "a gray window with a cursor", "no dead corners")


def test_the_guidance_is_in_our_own_words():
    docs = [p for folder in ("commands", "agents", "references")
            for p in (ROOT / folder).rglob("*.md")]
    for phrase in STAGESHOW_PHRASES:
        hits = [str(p.relative_to(ROOT)) for p in docs
                if phrase in p.read_text(encoding="utf-8").lower()]
        assert not hits, f"{phrase!r} is Stageshow's wording, in {hits}; say it in our own words"


def test_the_dashboard_playbook_lets_one_thing_lead():
    text = _read("references/surfaces/dashboard.md")
    assert "**One thing leads.**" in text
    assert "without a starting point" in text
