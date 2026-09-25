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
    g = read_guidance(_text(roles="- `color.status.<status>.text`: <status> words.\n"
                                  "- `color.status.info.text`: info words."), "color.md")
    assert describe("color.status.danger.text", g) == "danger words."
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
                                         "radius.card", "radius.dialog", "radius.pill",
                                         "radius.media"]
    card = catalog[3]
    assert (card.foundation, card.type, card.axes, card.description) == (
        "radius", "dimension", (), "the card corner.")


def test_a_missing_file_names_the_sections_to_write(tmp_path):
    with pytest.raises(GuidanceError, match="write guidance for motion with the sections Summary"):
        load_guidance("motion", tmp_path)
    ts = TokenSet()
    ts.add(Token("radius.1", "dimension", {"value": 4, "unit": "px"}))
    assert guidance_problems(ts, _folder(tmp_path, _text())) == []


def test_guidance_problems_lists_a_missing_or_broken_foundation_file(tmp_path):
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", foundations=("radius",)).tokens
    folder = _folder(tmp_path, _text())
    (folder / "radius.md").unlink()
    assert any(p.startswith(f"{folder / 'radius.md'} does not exist; write guidance for radius")
               for p in guidance_problems(ts, folder))
    (folder / "radius.md").write_text(_text(drop="Modes"), encoding="utf-8")
    assert any(p.startswith("radius.md has the sections") for p in guidance_problems(ts, folder))


def test_two_patterns_that_describe_one_role_are_named_as_an_overlap(tmp_path):
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", foundations=("radius",)).tokens
    roles = "\n".join(f"- `{t.path}`: x." for t in ts.tokens()
                      if t.layer == "semantic" and t.path != "radius.card")
    roles += "\n- `radius.<a>`: any.\n- `<b>.card`: card."
    problems = guidance_problems(ts, _folder(tmp_path, _text(roles=roles)))
    assert "radius.md: radius.card matches more than one Roles pattern (radius.<a>, <b>.card); " \
           "describe it on its own line or keep one pattern" in problems
    assert not any("radius.card has no description" in p for p in problems)



# A family line names each member, so no role reads its sibling's use.
def test_a_pattern_line_names_the_member_it_describes():
    g = read_guidance(_text(roles="- `motion.<role>.duration`: how long the <role> move "
                                  "lasts."), "motion.md")
    assert describe("motion.reveal.duration", g) == "how long the reveal move lasts."
    assert describe("motion.page.duration", g) == "how long the page move lasts."


def test_a_pattern_line_that_does_not_name_its_member_is_a_gap(tmp_path):
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", foundations=("radius",)).tokens
    roles = "\n".join(f"- `{t.path}`: x." for t in ts.tokens()
                      if t.layer == "semantic" and t.path != "radius.card")
    roles += "\n- `radius.<a>`: a corner."
    problems = guidance_problems(ts, _folder(tmp_path, _text(roles=roles)))
    assert "radius.md: the Roles line for radius.<a> does not write <a> in its description, so " \
           "every role it matches would read the same; write <a> where the role's name goes, " \
           "or describe each role on its own line" in problems


# Lines marked {arabic} are read only for a build whose type varies on
# direction, lines marked {latin} only for one whose type does not.
def test_marked_lines_follow_whether_the_build_has_right_to_left_type():
    text = _text().replace("Principles text.", "{arabic} Arabic line.\n{latin} Latin line.")
    assert read_guidance(text, "radius.md").section("Principles") == "Arabic line."
    assert read_guidance(text, "radius.md", arabic=False).section("Principles") == "Latin line."


def test_rtl_type_is_read_from_the_tokens():
    from engine.rulepack.guidance import rtl_type
    assert rtl_type(build_system(AxisValues(*[0.5] * 7), "#3366FF").tokens)
    assert not rtl_type(build_system(AxisValues(*[0.5] * 7), "#3366FF", arabic=False).tokens)
