"""The recommender maps a brief's industry text to an industries.json entry
by whole words only.

A loose substring test used to send "a" to fintech-neobank, "art" to
smart-home, "hr" to healthcare-ehr and "dev-tools" to
healthcare-medical-devices. These tests pin what matches, what falls
through to the tag-score fallback, and that sensible words keep the entry
they matched before.

Every brief here carries one audience tag that only longtail-funeral-services
holds, so the tag-score fallback has a single, known answer: a result equal
to FALLBACK means the industry text matched nothing.
"""
import pytest

from engine.data_loader import load
from engine.recommender import Brief
from engine.recommender.core import _lane_industry

ENTRIES = load("industries")["entries"]
TAGS = ["obituary publishing"]
FALLBACK = "longtail-funeral-services"


def industry_of(text):
    return _lane_industry(Brief(industry=text, audience=TAGS)).get("id")


def test_the_fallback_probe_is_what_the_tag_score_picks():
    assert _lane_industry(Brief(audience=TAGS))["id"] == FALLBACK


# --- garbage and vague words fall through ---------------------------------

@pytest.mark.parametrize("word", [
    "a", "e", "it", "tech", "app", "car", "pay", "b2b", "platform", "zzz",
    "zzz-not-a-real-industry", "id-from-industries", "", "   ", "-",
])
def test_garbage_and_vague_words_fall_through_to_the_tag_score(word):
    assert industry_of(word) == FALLBACK


@pytest.mark.parametrize("phrase", [
    # Each word is real, but no single entry's id, name or category holds
    # them all, so the phrase names no entry.
    "healthcare saas", "editorial-media", "consumer-lifestyle", "ai-ml",
])
def test_a_phrase_no_entry_holds_whole_falls_through(phrase):
    assert industry_of(phrase) == FALLBACK


# --- whole words, never a word inside a word -------------------------------

@pytest.mark.parametrize("word,wrong,right", [
    ("art", "smart-home", "longtail-art-marketplace"),
    ("hr", "healthcare-ehr", "enterprise-hr-payroll"),
    ("ai", "fintech-fundraising", "saas-ai-coding"),
    ("dev-tools", "healthcare-medical-devices", "saas-dev-tools"),
    ("media", "fintech-news", "media-video-streaming"),
])
def test_a_word_inside_another_word_does_not_match(word, wrong, right):
    got = industry_of(word)
    assert got != wrong
    assert got == right


@pytest.mark.parametrize("text", [
    "SaaS Dev Tools", "saas_dev_tools", "SAAS-DEV-TOOLS", "  saas.dev/tools  ",
])
def test_words_split_on_any_non_alphanumeric_and_ignore_case(text):
    assert industry_of(text) == "saas-dev-tools"


# --- ids, names and categories match their own entry -----------------------

@pytest.mark.parametrize("entry_id", [e["id"] for e in ENTRIES])
def test_every_exact_id_matches_its_entry(entry_id):
    assert industry_of(entry_id) == entry_id


@pytest.mark.parametrize("entry_id", [e["id"] for e in ENTRIES])
def test_an_id_with_spaces_underscores_or_capitals_matches_its_entry(entry_id):
    assert industry_of(entry_id.replace("-", " ")) == entry_id
    assert industry_of(entry_id.replace("-", "_")) == entry_id
    assert industry_of(entry_id.upper()) == entry_id
    assert industry_of(entry_id.replace("-", " ").title()) == entry_id


@pytest.mark.parametrize("entry", ENTRIES, ids=[e["id"] for e in ENTRIES])
def test_every_name_matches_its_entry(entry):
    assert industry_of(entry["name"]) == entry["id"]
    assert industry_of(entry["name"].lower().replace(" ", "-")) == entry["id"]


# "SaaS" is also a word of an id, and ids are checked before categories, so
# it keeps the entry the word "saas" has always matched.
CATEGORY_EXCEPTIONS = {"SaaS": "saas-accounting"}


@pytest.mark.parametrize("category", sorted({e["category"] for e in ENTRIES}))
def test_a_category_matches_the_first_entry_in_it(category):
    first = next(e["id"] for e in ENTRIES if e["category"] == category)
    assert industry_of(category) == CATEGORY_EXCEPTIONS.get(category, first)


# --- sensible words keep the entry they matched before ---------------------

@pytest.mark.parametrize("word,entry_id", [
    ("saas", "saas-accounting"), ("fintech", "fintech-neobank"),
    ("healthcare", "healthcare-telehealth"), ("luxury", "ecommerce-luxury-fashion"),
    ("crypto", "fintech-crypto"), ("telehealth", "healthcare-telehealth"),
    ("analytics", "saas-analytics-bi"), ("productivity", "saas-productivity"),
    ("education", "education-k12-edtech"), ("automotive", "longtail-automotive-marketplace"),
    ("ecommerce", "ecommerce-luxury-fashion"), ("e-commerce", "ecommerce-luxury-fashion"),
    ("gaming", "media-gaming-platform"), ("travel", "consumer-travel-booking"),
    ("banking", "mena-islamic-banking"), ("payments", "fintech-payments-infra"),
    ("fashion", "ecommerce-luxury-fashion"), ("crm", "saas-crm"), ("mena", "mena-islamic-banking"),
    ("luxury-fashion", "ecommerce-luxury-fashion"), ("real estate", "consumer-real-estate-rental"),
    ("k-12", "education-k12-edtech"), ("b2b saas", "saas-accounting"),
    ("fintech app", "fintech-neobank"),
    # a synthesizer industry id no entry spells out, kept by an explicit alias
    ("fintech-banking", "fintech-neobank"), ("Fintech Banking", "fintech-neobank"),
])
def test_sensible_words_keep_their_entry(word, entry_id):
    assert industry_of(word) == entry_id


# --- phrases now land on the entry that holds every word -------------------

@pytest.mark.parametrize("phrase,entry_id", [
    ("fintech-payments", "fintech-payments-infra"),
    ("fintech-trading", "fintech-brokerage"),
    ("developer-tools", "saas-dev-tools"),
    ("hospitality-travel", "travel-hotel-booking"),
    ("Saas Dev Tools", "saas-dev-tools"),
])
def test_a_phrase_lands_on_the_entry_that_holds_every_word(phrase, entry_id):
    assert industry_of(phrase) == entry_id
