"""The page composition: scored from the axes and the brief's fields, with
its reason in the report, and different for the four trial briefs."""
import json
from pathlib import Path

import pytest

from engine.foundations.audience import Audience
from engine.foundations.composition import DESCRIPTIONS, SCORES, choose
from engine.foundations.emit import brief_audience, choose_axes, make_system
from engine.synthesizer.axes import AxisValues

from tests.foundations.trials import TRIALS

BRIEFS = Path(__file__).resolve().parent / "briefs"


def _trial(name):
    brief = json.loads((BRIEFS / f"{name}.json").read_text(encoding="utf-8"))
    axes, _ = choose_axes(brief, None)
    return axes, brief_audience(brief)


def test_every_composition_is_named_and_scored():
    assert set(SCORES) == set(DESCRIPTIONS) == {"split", "stacked", "bento", "editorial-column",
                                                "full-bleed-media"}


@pytest.mark.parametrize("name, want", [("clinic", "stacked"), ("devtool", "bento"),
                                        ("fintech-ar", "split"),
                                        ("restaurant", "full-bleed-media")])
def test_the_four_trial_briefs_choose_different_compositions(name, want):
    assert choose(*_trial(name)).name == want


def test_the_brief_fields_move_the_choice():
    mid = AxisValues(*[0.5] * 7)
    assert choose(mid, Audience(age="older-adults")).name == "stacked"
    assert choose(mid, Audience(reading_context="long-read")).name == "editorial-column"
    assert choose(mid, Audience(reading_context="glance")).name == "bento"


def test_the_report_and_the_result_say_which_and_why():
    axes, audience = _trial("restaurant")
    out = make_system("#E85D04", axes, "x", audience=audience)
    section = out.report.split("## Page composition\n\n", 1)[1].split("\n## ", 1)[0]
    assert "- full-bleed-media: edge-to-edge images or generated art" in section
    assert "ahead of stacked at 0.50, mostly for warmth and playfulness." in section
    assert out.to_dict()["composition"]["name"] == "full-bleed-media"


def test_the_report_opens_with_one_character_sentence_per_system():
    sentences = {}
    for name, brand in TRIALS.items():
        axes, audience = _trial(name)
        report = make_system(brand, axes, "x", audience=audience).report
        sentences[name] = report.split("\n")[4]
    assert sentences["restaurant"] == (
        "Character: warm, rounded, playful and humanist. In this system the brand fills the "
        "main action, Baloo 2 sets the display type, and a landing page starts from the "
        "full-bleed-media composition.")
    assert all(s.startswith("Character: ") for s in sentences.values())
    assert len(set(sentences.values())) == 4


# M3.5c item 8: an Arabic-first page renders its display type in the Arabic
# display face, so the character sentence names that face first.
def test_an_arabic_first_sentence_names_the_arabic_display_face():
    from engine.foundations import build_system
    axes, audience = _trial("fintech-ar")
    ts = build_system(axes, TRIALS["fintech-ar"], arabic=True, audience=audience).tokens
    arabic, latin = ts.resolve("type.face.arabic-display")[0], ts.resolve("type.face.display")[0]
    report = make_system(TRIALS["fintech-ar"], axes, "x", audience=audience).report
    sentence = next(line for line in report.splitlines() if line.startswith("Character:"))
    assert f"{arabic} sets the Arabic display type and {latin} the Latin" in sentence, sentence
    assert sentence.index(arabic) < sentence.index(latin)


def test_a_latin_first_sentence_names_the_latin_display_face_only():
    axes, audience = _trial("clinic")
    report = make_system(TRIALS["clinic"], axes, "x", audience=audience).report
    sentence = next(line for line in report.splitlines() if line.startswith("Character:"))
    assert "Arabic display" not in sentence and "sets the display type" in sentence
