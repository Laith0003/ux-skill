"""The guidance reader and the role catalog: fixed sections, one bullet
per role and per check, family patterns, and every gap against the build
named with the fix."""
import pytest

from engine.foundations import build_system
from engine.foundations.tokens import Token, TokenSet
from engine.rulepack.guidance import (
    SECTIONS, SHARED, GuidanceError, describe, guidance_problems, load_guidance, read_guidance,
    role_catalog)
from engine.synthesizer.axes import AxisValues


def _text(roles="- `radius.card`: a card.", checks="- `radius-nesting`: nesting.",
          drop=None):
    parts = ["# Radius", ""]
    for heading in SECTIONS:
        if heading == drop:
            continue
        body = {"Roles": roles, "Checks": checks}.get(heading, f"{heading} text.")
        parts += [f"## {heading}", "", body, ""]
    return "\n".join(parts)


def test_reads_sections_roles_and_checks():
    g = read_guidance(_text(), "radius.md")
    assert g.title == "Radius" and [h for h, _ in g.sections] == list(SECTIONS)
    assert g.roles == (("radius.card", "a card."),)
    assert g.checks == (("radius-nesting", "nesting."),)
    assert g.section("Principles") == "Principles text."


@pytest.mark.parametrize("text,message", [
    (_text(drop="Modes"), "radius.md has the sections"),
    (_text(roles="radius.card is a card"), "radius.md: the Roles section line 'radius.card is "
                                           "a card' is not \"- `name`: description\""),
    (_text(roles="- `radius.card`: a.\n- `radius.card`: b."),
     "radius.md: radius.card is described twice under Roles; keep one line"),
    (_text().replace("# Radius\n", ""), "radius.md has no '# ' title line"),
    (_text().replace("Principles text.", ""), "radius.md: the Principles section is empty"),
])
def test_refuses_a_malformed_file_with_the_fix(text, message):
    with pytest.raises(GuidanceError) as err:
        read_guidance(text, "radius.md")
    assert str(err.value).startswith(message)


def test_a_family_pattern_describes_every_member_and_an_exact_key_wins():
    g = read_guidance(_text(roles="- `color.status.<status>.text`: status words.\n"
                                  "- `color.status.info.text`: info words."), "color.md")
    assert describe("color.status.danger.text", g) == "status words."
    assert describe("color.status.info.text", g) == "info words."
    assert describe("color.status.danger.soft", g) is None


def _folder(tmp_path, radius_text):
    (tmp_path / "radius.md").write_text(radius_text, encoding="utf-8")
    for name, sections in SHARED.items():
        body = "\n".join(f"## {h}\n\n{h} text.\n" for h in sections)
        (tmp_path / f"{name}.md").write_text(f"# {name}\n\n{body}", encoding="utf-8")
    return tmp_path


def test_guidance_problems_names_every_gap_against_the_build(tmp_path):
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", foundations=("radius",)).tokens
    folder = _folder(tmp_path, _text(roles="- `radius.card`: a card.\n- `radius.gone`: stale.",
                                     checks="- `radius-nesting`: n.\n- `radius-extra`: x."))
    problems = guidance_problems(ts, folder)
    assert "radius.md: radius.joined has no description under Roles; add \"- `radius.joined`: " \
           "what it is for\"" in problems
    assert "radius.md: the Roles line for radius.gone matches no role in the build; remove it " \
           "or fix the path" in problems
    assert "radius.md: the check radius-pill has no line under Checks; add \"- `radius-pill`: " \
           "what it guards\"" in problems
    assert "radius.md: the Checks line for radius-extra names no check of radius; remove it or " \
           "fix the id" in problems


def test_the_catalog_joins_description_type_and_axes(tmp_path):
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", foundations=("radius",)).tokens
    roles = "\n".join(f"- `{t.path}`: the {t.path.split('.')[-1]} corner." for t in ts.tokens()
                      if t.layer == "semantic")
    catalog = role_catalog(ts, _folder(tmp_path, _text(roles=roles)))
    assert [e.path for e in catalog] == ["radius.joined", "radius.chip", "radius.control",
                                         "radius.card", "radius.dialog", "radius.pill"]
    card = catalog[3]
    assert (card.foundation, card.type, card.axes, card.description) == (
        "radius", "dimension", (), "the card corner.")


def test_a_missing_file_names_the_sections_to_write(tmp_path):
    with pytest.raises(GuidanceError, match="write guidance for motion with the sections Summary"):
        load_guidance("motion", tmp_path)
    ts = TokenSet()
    ts.add(Token("radius.1", "dimension", {"value": 4, "unit": "px"}))
    assert guidance_problems(ts, _folder(tmp_path, _text())) == []
