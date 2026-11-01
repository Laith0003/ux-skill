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
    assert "**Photographs stay.**" in text and "references/surfaces/landing.md" in text


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


def _shipped_text():
    """Every doc the project ships: the command, agent, reference and Figma
    guides, the site and the root documents."""
    for folder in ("commands", "agents", "references", "figma-skill", "docs"):
        for p in (ROOT / folder).rglob("*"):
            if p.suffix in (".md", ".html"):
                yield p
    yield from ROOT.glob("*.md")


def test_the_guidance_is_in_our_own_words():
    docs = list(_shipped_text())
    for phrase in STAGESHOW_PHRASES:
        hits = [str(p.relative_to(ROOT)) for p in docs
                if phrase in p.read_text(encoding="utf-8").lower()]
        assert not hits, f"{phrase!r} is Stageshow's wording, in {hits}; say it in our own words"


def test_the_dashboard_playbook_lets_one_thing_lead():
    text = _read("references/surfaces/dashboard.md")
    lead = text[text.index("**One thing leads.**"):]
    lead = lead[:lead.index("\n")]
    assert "without a starting point" in lead
    # Principle 6 keeps the accent for the action, focus and current item,
    # and every grid has a first panel, so neither can be what makes one lead.
    assert "accent" not in lead and "reading order" not in lead


def test_a_moving_illustration_can_be_paused():
    text = _read(GUIDE)
    assert "pause control" in text and "references/foundations/motion.md" in text
    assert "(2.2.2)" in text


def test_the_phone_design_is_checked_at_the_narrowest_gate():
    text = _read(GUIDE)
    assert "360" in text and "390" in text


def test_a_hidden_illustration_holds_nothing_focusable():
    text = _read(GUIDE)
    assert 'aria-hidden="true"' in text and "nothing focusable" in text and "inert" in text


def test_the_close_up_is_the_one_enlarged_layout():
    text = _read(GUIDE)
    row = next(line for line in text.splitlines() if line.startswith("| Close-up"))
    assert "before the enlargement" in row
    assert "the close-up excepted" in text


def test_the_framing_rule_fits_every_layout_in_the_table():
    text = _read(GUIDE)
    rule = next(line for line in text.splitlines() if "two thirds of the stage" in line)
    assert "at least one edge" in rule and "satellite focus" in rule.lower()


def test_the_guide_stays_out_of_a_dashboard_build():
    text = _read(GUIDE)
    assert "as imagery" in text.split("## Where it sits")[0]
    assert "dashboard mode" in text


def test_the_large_product_mock_follows_the_guide():
    mock = _read("references/surfaces/landing.md")
    mock = mock[mock.index("**Large product mock.**"):]
    mock = mock[:mock.index("\n")]
    assert "extreme detail" not in mock and "floats above the page" not in mock
