"""The shipped guidance describes every semantic role and every check the
build has, in full and Latin-only builds, and ships with the package."""
import re
from pathlib import Path

import pytest

from engine.foundations import FOUNDATIONS, build_system
from engine.rulepack.guidance import (
    GUIDANCE_DIR, SHARED, guidance_problems, load_guidance, role_catalog)
from engine.synthesizer.axes import AxisValues

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("arabic", [True, False])
@pytest.mark.parametrize("axes", [AxisValues(*[0.5] * 7), AxisValues(*[0.0] * 7),
                                  AxisValues(*[1.0] * 7)])
def test_every_role_and_check_is_described(arabic, axes):
    ts = build_system(axes, "#3366FF", arabic=arabic).tokens
    assert guidance_problems(ts) == []
    catalog = role_catalog(ts)
    assert all(e.description for e in catalog)
    assert {e.foundation for e in catalog} == {f.name for f in FOUNDATIONS}


def test_every_foundation_and_shared_topic_has_a_file():
    for f in FOUNDATIONS:
        assert load_guidance(f.name).title
    for name in SHARED:
        assert load_guidance(name).title


def test_guidance_cites_only_records_that_exist():
    records = {p.stem for p in (GUIDANCE_DIR.parent / "decisions").glob("*.md")}
    for path in GUIDANCE_DIR.glob("*.md"):
        for cited in re.findall(r"decisions/([a-z0-9-]+)\.md", path.read_text(encoding="utf-8")):
            assert cited in records, (path.name, cited)


def test_guidance_ships_with_the_package():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"engine.rulepack" = ["decisions/*.md", "guidance/*.md"]' in pyproject


def _section(name, heading):
    return load_guidance(name).section(heading)


def test_color_states_which_pairings_the_fills_have():
    """Action and strong status fills are paired with the page only; the
    guidance says so and cites the record, and claims no wider coverage."""
    text = (GUIDANCE_DIR / "color.md").read_text(encoding="utf-8")
    for record in ("primary-edge", "brand-fidelity", "ring-never-weaker",
                   "ring-on-tinted-fills"):
        assert f"decisions/{record}.md" in text, record
    assert "page only" in _section("color", "Summary")
    assert "every background it can sit on" not in text
    assert "Every pairing a role can meet" not in text


def test_border_names_every_edge_color_the_contracts_bind():
    from engine.contracts.library import SEED_DIR, load_folder
    text = (GUIDANCE_DIR / "border.md").read_text(encoding="utf-8")
    roles = {b.role for c in load_folder(SEED_DIR) for b in c.tokens
             if b.property == "border-color"}
    assert roles and [r for r in sorted(roles) if r not in text] == []


def test_our_floors_are_worded_as_ours():
    """A sentence that states one of our own floors says it is ours."""
    for path in sorted(GUIDANCE_DIR.glob("*.md")):
        for sentence in re.split(r"(?<=[.;])\s+|\n", path.read_text(encoding="utf-8")):
            if re.search(r"334ms|1\.2:1|1\.3:1", sentence):
                assert re.search(r"\bours?\b", sentence), (path.name, sentence)


def test_color_says_when_each_button_emphasis_is_right():
    from engine.contracts.library import SEED_DIR, load_folder
    button = next(c for c in load_folder(SEED_DIR) if c.name == "button")
    emphases = next(v.values for v in button.variants if v.name == "emphasis")
    choosing = _section("color", "Choosing")
    for emphasis in emphases:
        assert f"{emphasis.capitalize()} button" in choosing or f"{emphasis} button" in choosing, \
            emphasis


# Arabic words (currency abbreviations, month names) may appear in the
# content and direction guidance; every other character outside ASCII is
# refused everywhere.
ARABIC_ALLOWED = ("content.md", "direction.md")


def _outside(text, arabic):
    return [c for c in text if not c.isascii() and not (arabic and "\u0600" <= c <= "\u06ff")]


def test_guidance_is_ascii_without_dashes():
    for path in sorted(GUIDANCE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        assert _outside(text, path.name in ARABIC_ALLOWED) == [], path.name
        assert not re.search(r"\s--\s|\w--\s|\s--$", text, re.M), path.name


# Changing the system says what this version supports: change an input,
# build again and read the report. Repointing, exempting or adding a role
# comes with the 4.1 importers and the extend mode, and nothing tells a
# reader to edit engine code or a generated value.
INPUTS = {"border": "contrast axis", "color": "brand color",
          "elevation": "contrast and formality axes", "layout": "density axis",
          "motion": "motion axis", "radius": "geometry and formality axes",
          "space": "density axis", "type": "every axis but motion"}
REPOINT = re.compile(r"\bpoint (the|its|one|it|a) |COVERAGE_EXEMPT|coverage table|generator "
                     r"change|overrides|\badd (it|a|an) [a-z ]*role\b|engine/", re.I)


@pytest.mark.parametrize("arabic", [True, False])
@pytest.mark.parametrize("name", sorted(INPUTS))
def test_changing_the_system_says_what_this_version_supports(name, arabic):
    text = load_guidance(name, arabic=arabic).section("Changing the system")
    assert "uxskill system build" in text, name
    assert "system report it writes beside tokens.json" in text, name
    assert "4.1 importers and the extend mode" in text, name
    assert INPUTS[name] in text, name
    assert not REPOINT.search(text), (name, REPOINT.search(text).group(0))
    assert len(text) < 1400, (name, len(text))


def test_layout_names_what_the_density_axis_moves_and_what_is_fixed():
    text = load_guidance("layout").section("Changing the system")
    assert "it sets the gutters, the margins and layout.container.max (1120, 1280 or 1440px)" \
        in text
    assert "the measures and the targets (44px comfortable, 32px compact) are fixed" in text
    lo, hi = (build_system(AxisValues(*([d] * 7)), "#3366FF").tokens for d in (0.0, 1.0))
    for role in ("layout.target.min", "layout.measure.text", "layout.breakpoint.tablet",
                 "layout.columns.phone"):
        for mode in ("", "density:compact"):
            assert lo.resolve(role, mode) == hi.resolve(role, mode), (role, mode)
    assert lo.resolve("layout.container.max") != hi.resolve("layout.container.max")
