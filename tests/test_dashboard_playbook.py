"""The dashboard playbook teaches the product dashboard people check many
times a day, not only the cockpit: every figure carries its context, states
take the category colors, panels have one anatomy, icons are one set, and a
product's own photo is content. The cockpit rules stay, for dense briefs."""
from pathlib import Path

DOC = (Path(__file__).resolve().parents[1] / "references" / "surfaces" / "dashboard.md").read_text(
    encoding="utf-8")


def _section(heading: str) -> str:
    start = DOC.index(heading)
    nxt = DOC.find("\n### ", start + len(heading))
    return DOC[start:nxt if nxt != -1 else len(DOC)]


def test_the_daily_app_pattern_comes_first_and_covers_the_anatomy():
    daily = _section("### Pattern: Daily-app dashboard")
    assert DOC.index("### Pattern: Daily-app dashboard") < DOC.index("### Pattern: Cockpit density")
    for words in ("vs yesterday", "color.category.", "color.status.", "panel title",
                  "line icon set", "thumbnail", "color.surface.header", "empty, loading and error"):
        assert words in daily, words


def test_figures_carry_their_context():
    assert "Every figure carries its context" in DOC


def test_numerals_are_tabular_without_forcing_a_mono_face():
    checklist = DOC[DOC.index("## Checklist"):DOC.index("## Worked example")]
    assert "font-mono` + `tabular-nums`) on numeric columns" not in checklist
    assert "tabular" in checklist


def test_states_take_category_colors_and_outcomes_take_status():
    assert "color.category." in _section("### Status and category colors (dashboard data)")


def test_no_card_loops_forever():
    assert "loops infinitely" not in DOC


def test_equal_kpi_cards_are_judged_by_what_they_carry():
    banned = _section("### Banned dashboard patterns")
    assert "Three equal cards for a KPI row" not in banned
    assert "bare number" in banned


def test_a_products_own_photo_is_content():
    banned = _section("### Banned dashboard patterns")
    assert "Stock photography" in banned and "own photo" in banned
