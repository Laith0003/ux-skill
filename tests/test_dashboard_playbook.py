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
    assert "Every key figure carries its context" in DOC


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


# ------------------------------------------------ review fixes

import re  # noqa: E402

_ROLE = re.compile(r"`((?:color|space|radius|elevation|type|layout|border|motion|imagery)\.[a-z0-9.\-N]+)`")


def test_every_role_the_playbook_names_exists_in_a_built_system():
    from engine.foundations import build_system
    from engine.synthesizer.axes import AxisValues
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF").tokens
    names = {m.replace(".N.", ".1.") for m in _ROLE.findall(DOC)}
    assert names, "the playbook names no role"
    paths = [t.path for t in ts.tokens()]
    missing = sorted(n for n in names
                     if not ts.has(n) and not any(p.startswith(n + ".") for p in paths))
    assert missing == [], missing


def test_numerals_are_never_mono_outside_a_cockpit():
    for line in DOC.splitlines():
        if re.search(r"mono(spaced)? numerals|font-mono` for all numbers", line):
            assert re.search(r"cockpit|codes|IDs", line, re.I), line


def test_every_accent_rule_lets_the_current_nav_item_carry_it():
    for line in DOC.splitlines():
        if re.search(r"accent", line, re.I) and re.search(r"CTA|primary action", line) \
                and re.search(r"\bonly\b", line):
            assert re.search(r"navigation|nav item", line, re.I), line


def test_bento_cards_keep_the_panel_anatomy_and_the_system_radius():
    bento = _section("### Bento 2.0 (premium dashboard)")
    assert "OUTSIDE and BELOW" not in bento and "rounded-[2.5rem]" not in bento
    assert "radius.card" in bento


def test_the_playbook_says_what_shows_before_the_clients_photos_arrive():
    daily = _section("### Pattern: Daily-app dashboard")
    assert "stand-in" in daily and "photo direction" in daily


def test_key_figures_carry_context_not_every_cell():
    assert "Every key figure carries its context" in DOC
