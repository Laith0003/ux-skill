"""The landing display fits a headline word as the face really sets it.

The fixture holds each face's letter advances and the width in em of
headline words in every face, measured from the face's own file in Chromium
at a display size and the heaviest display weight
(scripts/measure_face_letters.py). The committed metrics and letter table
are recomputed from it, and the fit's estimate for a word, from the letters
the brief's headline gives, never comes in under the measured width: on the
words the slack was chosen on, on words it was not, set in capitals, and in
Arabic.
"""
import json
import math
from pathlib import Path

import pytest

from engine.foundations import build_system, character, fonts
from engine.foundations.emit import NEUTRAL, brief_words
from engine.foundations.errors import InputError
from engine.foundations.typography import (ARABIC_SLACK, FIT_LETTERS, FIT_WORD, LETTER_FREQ,
                                           LETTER_WIDTHS, WORD_SLACK, capitals_letters,
                                           letter_count, word_em)
from engine.synthesizer.axes import AxisValues

DATA = json.loads((Path(__file__).parent / "data" / "face_word_widths.json")
                  .read_text(encoding="ascii"))
FACES = DATA["faces"]
LOWER = "abcdefghijklmnopqrstuvwxyz"
PROPORTIONAL = [f for f in fonts.FACES if f.role in ("text", "display")]
LATIN = [f for f in fonts.FACES if f.role != "arabic"]
ARABIC = [f for f in fonts.FACES if f.role == "arabic"]


def _weighted(letters, upper=False):
    return sum(letters[c.upper() if upper else c] * f
               for c, f in zip(LOWER, LETTER_FREQ)) / sum(LETTER_FREQ)


def _up(x):
    return math.ceil(round(x * 100, 6)) / 100


def test_the_fixture_was_measured_at_a_display_size_and_the_heaviest_display_weight():
    heaviest = max(character.display_weight(AxisValues(*[v] * 7)) for v in (0.0, 0.5, 1.0))
    assert DATA["measure"]["weight"] >= heaviest
    assert DATA["measure"]["px"] <= character.PHONE_DISPLAY_PX[0] * 1.2
    assert set(FACES) == {f.family for f in fonts.FACES}


@pytest.mark.parametrize("face", LATIN, ids=lambda f: f.slug)
def test_each_latin_face_carries_the_advances_measured_in_the_fixture(face):
    letters = FACES[face.family]["letters"]
    assert face.metrics.latin_letters == round(_weighted(letters) * face.metrics.upm, 1)
    assert face.metrics.latin_capitals == round(_weighted(letters, True) * face.metrics.upm, 1)


def test_the_letter_table_is_the_fixture_shares():
    for c in LOWER + LOWER.upper():
        shares = [FACES[f.family]["letters"][c] / _weighted(FACES[f.family]["letters"])
                  for f in PROPORTIONAL]
        want = sum(shares) / len(shares) if c.islower() else max(shares)
        assert LETTER_WIDTHS[c] == _up(want), c


@pytest.mark.parametrize("face", PROPORTIONAL, ids=lambda f: f.slug)
@pytest.mark.parametrize("words", ["words", "held_out"])
def test_the_fit_never_comes_in_under_a_measured_word(face, words):
    for word, measured in FACES[face.family][words].items():
        estimate = word_em(face, "latin", brief_words({"headline": word})["latin"])
        assert estimate >= measured, (face.family, word, estimate, measured)


@pytest.mark.parametrize("face", PROPORTIONAL, ids=lambda f: f.slug)
def test_a_capitals_display_never_comes_in_under_the_word_in_capitals(face):
    for word, measured in FACES[face.family]["held_out"].items():
        if word.isupper():
            letters = capitals_letters(face, brief_words({"headline": word.capitalize()})["latin"],
                                       0.0)
            assert word_em(face, "latin", letters) >= measured, (face.family, word)


def test_capitals_tracking_widens_the_word():
    face = fonts.BY_FAMILY["Sora"]
    assert capitals_letters(face, 10, 0.02) > capitals_letters(face, 10, 0.0) > 10


def test_a_brand_that_sets_its_display_in_capitals_fits_the_word_in_capitals():
    loud = AxisValues(warmth=0.7, contrast=0.9, density=0.5, geometry=0.7, formality=0.1,
                      motion=0.9, type_personality=0.6)
    assert character.capitals(loud) >= character.CAPITALS_FROM
    assert character.capitals(NEUTRAL) < character.CAPITALS_FROM
    word = build_system(loud, "#3366FF", words={"latin": 9}).tokens.resolve("type.fit-word.latin")
    assert word > 9
    assert build_system(NEUTRAL, "#3366FF", words={"latin": 9}).tokens.resolve(
        "type.fit-word.latin") == 9


def test_the_capitals_measure_moves_with_the_lean_and_never_jumps():
    from engine.foundations.typography import CAPS_RAMP, caps_fit_letters
    face = fonts.BY_FAMILY["Sora"]
    seen = []
    for i in range(101):
        e = i / 100
        axes = AxisValues(warmth=0.5, contrast=e, density=0.5, geometry=0.5, formality=0.2,
                          motion=e, type_personality=0.5)
        seen.append((character.capitals(axes), caps_fit_letters(axes, face, 10)))
    for (_, a), (_, b) in zip(seen, seen[1:]):
        assert abs(b - a) <= 0.3
    assert all(n == 10 for lean, n in seen if lean <= character.CAPITALS_FROM - CAPS_RAMP)
    assert all(n == capitals_letters(face, 10, character.capitals_tracking(AxisValues(
        warmth=0.5, contrast=1, density=0.5, geometry=0.5, formality=0.2, motion=1,
        type_personality=0.5))) for lean, n in seen[-1:])


def test_the_estimate_stays_close_to_the_measured_word():
    # Never under, and not so far over that the display shrinks for nothing.
    for face in PROPORTIONAL:
        for word, measured in FACES[face.family]["words"].items():
            estimate = word_em(face, "latin", brief_words({"headline": word})["latin"])
            assert estimate <= measured * 1.25, (face.family, word, estimate, measured)


@pytest.mark.parametrize("face", ARABIC, ids=lambda f: f.slug)
def test_an_arabic_word_never_comes_in_over_its_estimate(face):
    for word, measured in FACES[face.family]["words"].items():
        letters = brief_words({"headline": word})["arabic"]
        assert word_em(face, "arabic", letters) >= measured, (face.family, len(word))


def test_the_default_word_takes_the_same_slack_as_a_brief_word():
    assert FIT_WORD["latin"] == math.ceil(round(FIT_LETTERS["latin"] * WORD_SLACK * 10, 6)) / 10
    assert FIT_WORD["arabic"] == math.ceil(round(FIT_LETTERS["arabic"] * ARABIC_SLACK * 10,
                                                 6)) / 10
    # A brief word of 13 average letters fits as the default does.
    assert brief_words({"headline": "Collaboration"})["latin"] <= FIT_WORD["latin"]


def test_wide_letters_count_for_more_than_narrow_ones():
    assert letter_count("Momentum") > len("Momentum")
    assert letter_count("Intelligence") < len("Intelligence")
    assert brief_words({"headline": "Momentum now"})["latin"] > brief_words(
        {"headline": "Illicit tilt"})["latin"]


def test_accented_letters_weigh_as_their_base_letter_and_others_as_one():
    assert letter_count("\u00c9t\u00e9") == letter_count("Ete")
    assert letter_count("\u00df") == 1.0
    assert set(LETTER_WIDTHS) == set(LOWER + LOWER.upper())


def test_an_arabic_word_counts_its_letters_with_the_slack():
    assert brief_words({"headline": "\u0645\u0631\u062d\u0628\u0627"}) == {
        "arabic": math.ceil(round(5 * ARABIC_SLACK * 10, 6)) / 10}


def test_a_word_too_long_for_the_fit_is_still_refused_by_its_letters():
    with pytest.raises(InputError, match="of 41 letters"):
        brief_words({"headline": "i" * 41})


def test_a_word_of_wide_letters_is_refused_by_its_width():
    with pytest.raises(InputError, match="of 30 letters, as wide as .* average letters"):
        brief_words({"headline": "W" * 30})


def test_a_count_is_in_tenths_and_build_takes_it():
    letters = brief_words({"headline": "Momentum"})["latin"]
    assert letters == round(letters, 1) and letters != int(letters)
    assert build_system(NEUTRAL, "#3366FF", words={"latin": letters}).report.passed
