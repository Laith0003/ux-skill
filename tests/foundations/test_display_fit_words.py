"""The landing display fits a headline word as the face really sets it.

The fixture holds the width in em of headline words in each Latin face,
measured from the face's own file in Chromium at weight 400
(scripts/measure_face_letters.py). The fit's estimate for a word, from the
letters the brief's headline gives, never comes in under the measured width.
"""
import json
from pathlib import Path

import pytest

from engine.foundations import fonts
from engine.foundations.emit import brief_words
from engine.foundations.typography import LETTER_WIDTHS, letter_count, word_em

FIXTURE = json.loads((Path(__file__).parent / "data" / "face_word_widths.json")
                     .read_text(encoding="utf-8"))
PROPORTIONAL = [f for f in fonts.FACES if f.family in FIXTURE and f.role != "mono"]


def test_the_fixture_covers_every_latin_face():
    assert {f.family for f in fonts.FACES if f.role != "arabic"} == set(FIXTURE)


def test_every_latin_face_has_its_letter_advance_measured_without_the_space():
    for face in fonts.FACES:
        if face.role != "arabic":
            assert face.metrics.latin_letters, face.family


@pytest.mark.parametrize("face", PROPORTIONAL, ids=lambda f: f.slug)
def test_the_fit_never_comes_in_under_a_measured_word(face):
    for word, measured in FIXTURE[face.family].items():
        letters = brief_words({"headline": word})["latin"]
        estimate = word_em(face, "latin", letters)
        assert estimate >= measured, (face.family, word, letters, estimate, measured)


def test_the_estimate_stays_close_to_the_measured_word():
    # Never under, and not so far over that the display shrinks for nothing.
    for face in PROPORTIONAL:
        for word, measured in FIXTURE[face.family].items():
            estimate = word_em(face, "latin", brief_words({"headline": word})["latin"])
            assert estimate <= measured * 1.25, (face.family, word, estimate, measured)


def test_wide_letters_count_for_more_than_narrow_ones():
    assert letter_count("Momentum") > len("Momentum")
    assert letter_count("Intelligence") < len("Intelligence")
    assert brief_words({"headline": "Momentum now"})["latin"] > brief_words(
        {"headline": "Illicit tilt"})["latin"]


def test_accented_letters_weigh_as_their_base_letter_and_others_as_one():
    assert letter_count("\u00c9t\u00e9") == letter_count("Ete")
    assert letter_count("\u00df") == 1.0
    assert set(LETTER_WIDTHS) == set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def test_arabic_words_still_count_their_letters():
    assert brief_words({"headline": "\u0645\u0631\u062d\u0628\u0627"}) == {"arabic": 5}


def test_a_word_too_long_for_the_fit_is_still_refused_by_its_letters():
    from engine.foundations.errors import InputError
    with pytest.raises(InputError, match="of 41 letters"):
        brief_words({"headline": "i" * 41})


def test_a_word_of_wide_letters_is_refused_by_its_width():
    from engine.foundations.errors import InputError
    with pytest.raises(InputError, match="of 30 letters, as wide as .* average letters"):
        brief_words({"headline": "W" * 30})


def test_a_latin_count_is_in_tenths_and_build_takes_it():
    from engine.foundations import build_system
    from engine.foundations.emit import NEUTRAL
    letters = brief_words({"headline": "Momentum"})["latin"]
    assert letters == round(letters, 1) and letters != int(letters)
    assert build_system(NEUTRAL, "#3366FF", words={"latin": letters}).report.passed
