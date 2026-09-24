"""Industry words in a brief map to an industry seed by whole words only.

A loose substring match used to send "a", "tech", "it" and "car" to
unrelated industries. These tests pin what matches, what does not, and that
every word that matched sensibly before still gets the same seed.
"""
import pytest

from engine.synthesizer.axes import AXIS_NAMES, INDUSTRY_SEEDS, _seed_from_industry

NEUTRAL = {name: 0.5 for name in AXIS_NAMES}


def industry_of(word):
    seed = _seed_from_industry(word)
    if seed == NEUTRAL:
        return None
    return next(k for k, v in INDUSTRY_SEEDS.items() if v == seed)


@pytest.mark.parametrize("word", ["a", "e", "tech", "it", "car", "pay", "lux", "art",
                                  "notsaasy", "fintechx", "zzz-not-a-real-industry"])
def test_words_that_are_not_an_industry_match_nothing(word):
    assert industry_of(word) is None


@pytest.mark.parametrize("industry", list(INDUSTRY_SEEDS))
def test_every_industry_id_matches_itself(industry):
    assert industry_of(industry) == industry


@pytest.mark.parametrize("word,industry", [
    # one part of an id, as a whole word
    ("fintech", "fintech-payments"), ("payments", "fintech-payments"),
    ("banking", "fintech-banking"), ("trading", "fintech-trading"),
    ("developer", "developer-tools"), ("tools", "developer-tools"),
    ("ai", "ai-ml"), ("ml", "ai-ml"), ("consumer", "consumer-lifestyle"),
    ("lifestyle", "consumer-lifestyle"), ("editorial", "editorial-media"),
    ("media", "editorial-media"), ("hospitality", "hospitality-travel"),
    ("travel", "hospitality-travel"),
    # an id written inside a longer description, as whole words
    ("b2b saas", "saas"), ("healthcare saas", "saas"), ("saas platform", "saas"),
    ("crypto exchange", "crypto"), ("saas-dev-tools", "saas"),
    ("saas-productivity", "saas"),
    # common short forms, by explicit alias
    ("health", "healthcare"), ("bank", "fintech-banking"), ("payment", "fintech-payments"),
    ("auto", "automotive"), ("edu", "education"),
])
def test_words_that_matched_sensibly_before_keep_their_seed(word, industry):
    assert industry_of(word) == industry


@pytest.mark.parametrize("phrase,industry", [
    ("developer tools", "developer-tools"), ("Fintech Payments", "fintech-payments"),
    ("hospitality_travel", "hospitality-travel"),
])
def test_an_id_written_with_spaces_or_capitals_matches(phrase, industry):
    assert industry_of(phrase) == industry


@pytest.mark.parametrize("phrase", ["fintech-neobank", "construction-pm", "fintech app", "b2b"])
def test_a_description_without_a_whole_industry_id_stays_neutral(phrase):
    # One recognized part inside a longer description is not enough: the
    # other words may say a different industry.
    assert industry_of(phrase) is None


def test_matching_is_case_and_whitespace_insensitive():
    assert industry_of("  HealthCare  ") == "healthcare"
    assert industry_of("") is None and industry_of(None) is None
