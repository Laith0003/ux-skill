"""The brief's structured fields: what each changes in the tokens and the
report, and that plain text the engine cannot read is named with how to
pass it."""
import pytest

from engine.foundations import build_system
from engine.foundations.audience import Audience, AudienceError, effects, read_audience
from engine.foundations.emit import (
    NEUTRAL, InputError, brief_audience, choose_axes, make_system, resolve_arabic, unread_lines)
from engine.synthesizer.axes import AxisValues

MID = AxisValues(*[0.5] * 7)


def px(dim):
    return dim["value"] * (16 if dim["unit"] == "rem" else 1)


def test_the_defaults_change_nothing():
    a = read_audience(None)
    assert a == Audience() and effects(a) == []
    assert (a.body_px, a.target_px, a.ring_extra, a.refuse_compact) == (16, 44, 0, False)
    assert a.arabic is None


def test_older_readers_get_larger_text_and_targets_a_wider_ring_and_no_compact():
    a = read_audience({"age": "older-adults"})
    ts = build_system(MID, "#3366FF", audience=a).tokens
    assert px(ts.resolve("type.text.body")["fontSize"]) == 18
    assert ts.resolve("layout.target.min")["value"] == 48
    assert ts.resolve("layout.target.min", "density:compact")["value"] == 48
    assert ts.resolve("border.focus-ring.width")["value"] == 3
    assert ts.resolve("space.control.gap", "density:compact") == ts.resolve("space.control.gap")
    lines = [e.line() for e in effects(a)]
    assert lines == ["Body text is 18px, targets are at least 48px, the focus ring is 1px wider, "
                     "and compact density is not offered: the brief says the readers are older "
                     "adults, who need larger text, larger targets and a focus ring they can "
                     "find"]


def test_long_reading_opens_the_lines_and_narrows_the_measure():
    a = read_audience({"reading_context": "long-read"})
    ts = build_system(MID, "#3366FF", audience=a).tokens
    assert ts.resolve("type.text.body")["lineHeight"] == 1.65
    assert ts.resolve("layout.measure.text")["value"] == 34


def test_languages_decide_arabic_and_the_primary_script():
    arabic = read_audience({"languages": ["ar-JO", "ar-EG", "en"]})
    assert arabic.arabic is True and arabic.primary_script == "arabic"
    latin = read_audience({"languages": "en, fr"})
    assert latin.arabic is False and latin.primary_script == "latin"
    assert resolve_arabic(False, latin, "--latin-only") is False
    assert resolve_arabic(True, Audience(), "--latin-only") is False
    with pytest.raises(InputError) as exc:
        resolve_arabic(True, arabic, "--latin-only")
    assert str(exc.value) == (
        "--latin-only leaves Arabic out, but the brief's languages (ar-JO, ar-EG, en) include "
        "one written in Arabic script; drop --latin-only, or take the Arabic languages out of "
        "the brief")


def test_a_dark_first_brief_opens_dark_and_keeps_the_light_choice():
    a = read_audience({"default_scheme": "dark"})
    out = make_system("#3366FF", MID, "x", audience=a)
    css = out.files["tokens.css"]
    assert ':root:not([data-theme="light"]) {\n  color-scheme: dark;' in css
    assert "prefers-color-scheme" not in css
    assert "- tokens.css opens in dark mode and sets color-scheme; data-theme still switches " \
           "it: the brief sets dark as the default scheme" in out.report


@pytest.mark.parametrize("brief, message", [
    ({"age": "senior"}, "brief field age is 'senior'; use one of children, teens, adults, "
                        "all-ages, older-adults"),
    ({"default_scheme": "dim"}, "brief field default_scheme is 'dim'; use one of light, dark, "
                                "system"),
    ({"languages": [3]}, "brief field languages is [3]; give language tags, for example "
                         '"languages": ["ar-JO", "en"]'),
])
def test_a_field_the_engine_does_not_read_is_named_with_the_choices(brief, message):
    with pytest.raises(AudienceError) as exc:
        read_audience(brief)
    assert str(exc.value) == message
    with pytest.raises(InputError):
        brief_audience(brief)


def test_a_brief_of_fields_only_builds_the_neutral_axes():
    axes, source = choose_axes({"age": "older-adults", "languages": ["en"]}, None)
    assert axes == NEUTRAL
    assert source == "from the brief's fields (age, languages), which leave every axis at 0.5"


def test_unread_text_is_named_with_how_to_pass_it_never_waved_through():
    brief = {"industry": "restaurant", "tone": ["warm", "reassuring"],
             "audience": "patients booking appointments, many over 60"}
    lines = unread_lines(brief)
    assert lines[0].startswith('industry "restaurant" is not one the engine knows. Pass the '
                               "nearest of ai-ml, automotive")
    assert lines[1].startswith('tone "reassuring" moves no axis. tone accepts: ')
    # a comma string is split into words, as the synthesizer reads it
    assert lines[2].startswith('audience "patients booking appointments" is plain text, which '
                               "the engine does not parse. Say who the readers are with the "
                               'brief\'s fields: age ("children"')
    assert lines[3].startswith('audience "many over 60" is plain text')
    report = make_system("#3366FF", MID, "x", unread=lines).report
    section = report.split("## What the engine did not read\n\n", 1)[1].split("\n## ", 1)[0]
    assert section.startswith("The engine reads a fixed vocabulary and the brief's structured "
                              "fields. These words changed nothing")
    assert "nothing needs doing" not in report


def test_the_unread_audience_line_names_only_the_fields_the_brief_lacks():
    brief = {"industry": "healthcare", "audience": "many over 60", "age": "older-adults",
             "languages": ["ar"]}
    assert unread_lines(brief) == [
        'audience "many over 60" is plain text, which the engine does not parse. Say who the '
        "readers are with the brief's fields: "
        'default_scheme ("light", "dark" or "system"); '
        'reading_context ("glance", "task", "long-read" or "on-the-go").']
    brief.update(default_scheme="dark", reading_context="task")
    assert unread_lines(brief) == [
        'audience "many over 60" is plain text, which the engine does not parse. The brief\'s '
        "fields age, languages, default_scheme and reading_context already say who the readers "
        "are."]


def test_industry_words_with_spaces_are_read():
    axes, source = choose_axes({"industry": "developer tools"}, None)
    assert source == "from the brief (industry: developer tools, read as developer-tools)"


@pytest.mark.parametrize("age", ["children", "teens", "adults", "all-ages", "older-adults"])
@pytest.mark.parametrize("contrast", [0.0, 0.66, 1.0])
def test_every_age_builds_at_every_contrast_and_the_high_ring_stays_one_wider(age, contrast):
    a = read_audience({"age": age})
    axes = AxisValues(0.5, contrast, 0.5, 0.5, 0.5, 0.5, 0.5)
    out = make_system("#3366FF", axes, "x", audience=a)
    assert out.passed, [f.message for f in out.findings]
    ts = build_system(axes, "#3366FF", audience=a).tokens
    std = ts.resolve("border.focus-ring.width")["value"]
    high = ts.resolve("border.focus-ring.width", "contrast:high")["value"]
    assert high == std + 1
    base = build_system(axes, "#3366FF").tokens.resolve("border.focus-ring.width")["value"]
    assert std >= base


def test_the_age_line_states_the_ring_the_build_made_at_a_dramatic_contrast():
    a = read_audience({"age": "older-adults"})
    axes = AxisValues(0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5)
    lines = [e.line() for e in effects(a, axes)]
    assert lines[0].startswith("Body text is 18px, targets are at least 48px, the focus ring "
                               "stays 3px, already the widest standard ring for this contrast "
                               "(4px under high contrast), and compact density is not offered")
    mid = [e.line() for e in effects(a, MID)]
    assert "the focus ring is 1px wider" in mid[0]


def test_glance_reading_states_the_composition_score_it_moved():
    a = read_audience({"reading_context": "glance"})
    dense = AxisValues(0.5, 0.7, 0.8, 0.5, 0.5, 0.5, 0.2)
    lines = [e.line() for e in effects(a, dense)]
    assert lines == ["Bento, the composition people scan, scores 0.20 higher, and the page starts "
                     "from it: the brief says people glance at it"]
    calm = AxisValues(0.5, 0.2, 0.1, 0.5, 0.9, 0.5, 0.9)
    lines = [e.line() for e in effects(a, calm)]
    assert lines == ["Bento, the composition people scan, scores 0.20 higher, and the page still "
                     "starts from editorial-column: the brief says people glance at it"]


@pytest.mark.parametrize("langs, message", [
    (["Arabic", "English"], 'brief field languages holds "Arabic", a language name; give its '
                            'tag "ar", for example "languages": ["ar", "en"]'),
    (["english"], 'brief field languages holds "english", a language name; give its tag "en", '
                  'for example "languages": ["en"]'),
    (["klingon"], 'brief field languages holds "klingon", which is not a language tag; give a '
                  'tag of two or three letters and optional subtags, for example "languages": '
                  '["ar-JO", "en"]'),
    (["ar_JO"], 'brief field languages holds "ar_JO", which is not a language tag; give a tag of '
                'two or three letters and optional subtags, for example "languages": '
                '["ar-JO", "en"]'),
])
def test_languages_need_a_tag_and_a_language_name_points_to_its_tag(langs, message):
    with pytest.raises(AudienceError) as exc:
        read_audience({"languages": langs})
    assert str(exc.value) == message
    assert read_audience({"languages": ["ar-JO", "zh-Hant-TW", "en"]}).arabic is True


def test_an_arabic_primary_script_names_arabic():
    a = read_audience({"primary_script": "arabic"})
    assert a.arabic is True
    with pytest.raises(InputError) as exc:
        resolve_arabic(True, a, "--latin-only")
    assert "primary_script is arabic" in str(exc.value)
    assert read_audience({"primary_script": "latin"}).arabic is None
    rtl = [e.line() for e in effects(a) if 'dir="rtl"' in e.line()]
    assert rtl and resolve_arabic(False, a) is True


def test_every_unread_field_gets_a_line():
    brief = {"industry": "fintech", "region": "Jordan", "project_type": "landing",
             "reference_brands": ["a", "b"], "success_metric": "", "stack": "astro"}
    lines = unread_lines(brief)
    assert lines == [
        'project_type "landing" is not read by the system build. Say what the product is with '
        'product_type ("app", "software", "marketing-site", "editorial", "commerce", '
        '"marketplace" or "local-service", the product the page sells).',
        'reference_brands "a, b" is not read by the system build, so it changed nothing here.',
        'region "Jordan" is not read by the system build. Say what it means for the system with '
        'languages (tags such as ["ar-JO", "en"]) and primary_script ("latin" or "arabic").',
        'stack "astro" is not read by the system build, so it changed nothing here.',
    ]


@pytest.mark.parametrize("tag", ["arz", "apc", "ajp", "ary", "aeb", "acm", "arz-EG", "ar-arz",
                                 "pa-Arab", "ur-Aran", "ms-Arab-MY", "prs", "pbt"])
def test_arabic_varieties_and_an_arabic_script_subtag_ship_arabic(tag):
    """A member of the Arabic, Persian or Pashto macrolanguage, or any tag
    whose script subtag is Arab (or Aran), is written in Arabic script."""
    a = read_audience({"languages": [tag, "en"]})
    assert a.arabic is True and a.primary_script == "arabic"
    assert resolve_arabic(False, a) is True
    lines = [e.line() for e in effects(a)]
    assert f"Arabic faces, sizes and right to left styles are built: the brief names {tag}, en" \
        in lines
    with pytest.raises(InputError) as exc:
        resolve_arabic(True, a, "--latin-only")
    assert f"brief's languages ({tag}, en) include one written in Arabic script" in str(exc.value)


@pytest.mark.parametrize("tag", ["arz", "apc", "pa-Arab", "ur-Aran", "fa"])
def test_a_tag_the_arabic_selector_misses_is_told_to_carry_dir_rtl(tag):
    lines = [e.line() for e in effects(read_audience({"languages": ["en", tag]}))]
    assert (f'Mark text in {tag} with dir="rtl": tokens.css switches to the Arabic styles on '
            f'dir="rtl" or on a lang of ar and its subtags, and "{tag}" is neither') in lines


def test_a_tag_the_arabic_selector_matches_needs_no_extra_line():
    for tag in ("ar", "ar-EG", "ar-arz", "AR-jo"):
        lines = [e.line() for e in effects(read_audience({"languages": [tag]}))]
        assert not any(line.startswith("Mark text in") for line in lines), tag
    lines = [e.line() for e in effects(read_audience({"languages": ["ar"]}))]
    assert lines == ["Arabic faces, sizes and right to left styles are built: the brief names ar",
                     'Set dir="rtl" and the lang attribute on the html element: the primary '
                     "script is Arabic, so pages open right to left"]


@pytest.mark.parametrize("tag", ["en", "ar-Latn", "sd-Deva", "tr", "hi", "mt"])
def test_a_tag_in_another_script_stays_latin(tag):
    a = read_audience({"languages": [tag]})
    assert a.arabic is False and a.primary_script == "latin"
    assert resolve_arabic(False, a) is False


def test_an_arabic_variety_builds_the_arabic_faces():
    a = read_audience({"languages": ["arz"]})
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", arabic=resolve_arabic(False, a),
                      audience=a).tokens
    assert ts.has("type.face.arabic") and ts.has("type.size.arabic.3")
