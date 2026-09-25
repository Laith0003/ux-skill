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


def test_industry_words_with_spaces_are_read():
    axes, source = choose_axes({"industry": "developer tools"}, None)
    assert source == "from the brief (industry: developer tools, read as developer-tools)"
