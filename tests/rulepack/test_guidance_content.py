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
    for record in ("fill-edge-page-only", "ring-on-tinted-fills"):
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


def test_guidance_is_ascii_without_dashes():
    for path in sorted(GUIDANCE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        assert text.isascii(), path.name
        assert not re.search(r"\s--\s|\w--\s|\s--$", text, re.M), path.name
