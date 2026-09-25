"""The page-sequence picker reads a 4.0 brief, not one word of it.

Three real landing builds showed the picker keying on the verb "book", returning
the SaaS plan for a B2B marketplace, and asking for stats, a named testimonial
and a phone number that the client did not have. These tests pin the fixes:
structured fields decide first, a single verb never picks a sequence, a B2B
marketplace has its own sequence, and a proof section the client cannot fill
is dropped with a stated reason instead of invented.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from engine.page_sequence import load_sequences, select_for_brief, select_sequence

ROOT = Path(__file__).resolve().parents[1]
# Verbs a call to action uses. Any page might say them, so none may key a sequence.
CTA_VERBS = {"book", "booking", "buy", "call", "contact", "download", "get", "hire", "install",
             "join", "learn", "order", "request", "shop", "sign", "start", "subscribe", "try"}
PROOF_KINDS = {"stats", "testimonials", "logos", "reviews", "case-studies", "certifications", "press"}


def _ids(seq):
    return [s["section"] for s in seq["section_sequence"]]


# ------------------------------------------------------------- single verbs


def test_no_sequence_is_keyed_on_a_single_verb():
    for entry in load_sequences():
        single = [k for k in entry["keywords"] if " " not in k.strip() and k.strip().lower() in CTA_VERBS]
        assert not single, f"{entry['id']} is keyed on the verb(s) {single}; use a phrase that names the business"


@pytest.mark.parametrize("query", ["book", "Book a demo", "buy now", "download", "call us today", "start"])
def test_a_verb_alone_picks_nothing(query):
    assert select_sequence(query) is None, f"{query!r} should not pick a sequence"


def test_a_keyword_matches_whole_words_only():
    """'book' inside 'facebook' or 'notebook', 'app' inside 'approach', match nothing."""
    assert select_sequence("our approach to notebooks, see us on facebook") is None


# ------------------------------------------------------------- B2B marketplace


def test_a_b2b_marketplace_sequence_exists():
    entry = next((e for e in load_sequences() if e["id"] == "b2b-marketplace"), None)
    assert entry is not None, "data/page-sequences.json needs a b2b-marketplace entry"
    names = " ".join(_ids(entry)).lower()
    for part in ("buyer", "supplier", "categor", "how ordering works", "delivery", "faq", "footer"):
        assert part in names, f"b2b-marketplace lacks a section for {part!r}"


@pytest.mark.parametrize("brief", [
    {"primary_goal": "Pharmacies open an account and order from warehouses", "project_type": "landing",
     "audience": "pharmacy owners and drug warehouses", "industry": "healthcare",
     "description": "a B2B marketplace for pharmacy supply"},
    {"answers": {"primary_goal": "Book a demo", "audience": "contractors buying in bulk",
                 "industry": "ecommerce", "description": "B2B building materials marketplace with suppliers"}},
    {"product_type": "marketplace", "audience": "clinics buying from distributors", "primary_goal": "trade accounts"},
])
def test_b2b_marketplace_briefs_get_the_marketplace_sequence(brief):
    seq = select_for_brief(brief)
    assert seq is not None and seq["id"] == "b2b-marketplace", seq and seq["id"]


def test_b2b_software_still_gets_saas():
    seq = select_for_brief({"primary_goal": "start a free trial", "industry": "saas",
                            "audience": "B2B finance teams", "description": "a reporting platform"})
    assert seq["id"] == "saas-marketing"


# ------------------------------------------------------------- structured fields


def test_an_explicit_sequence_id_wins():
    seq = select_for_brief({"page_sequence": "content-publication", "industry": "saas"})
    assert seq["id"] == "content-publication"
    assert "page_sequence" in seq["why"]


def test_an_unknown_sequence_id_is_refused_with_the_choices():
    with pytest.raises(ValueError) as err:
        select_for_brief({"page_sequence": "blog"})
    msg = str(err.value)
    assert "page_sequence" in msg and "content-publication" in msg


def test_the_industry_field_steers_the_pick():
    assert select_for_brief({"industry": "editorial-media"})["id"] == "content-publication"
    assert select_for_brief({"industry": "developer-tools"})["id"] == "saas-marketing"


def test_the_project_type_mobile_app_steers_the_pick():
    assert select_for_brief({"project_type": "mobile-app", "audience": "commuters"})["id"] == "app-mobile-landing"


def test_the_product_type_field_is_read_when_present():
    seq = select_for_brief({"product_type": "editorial", "audience": "readers"})
    assert seq["id"] == "content-publication"
    assert "product_type" in seq["why"]


def test_the_discovery_file_shape_is_read(tmp_path: Path):
    path = tmp_path / "last-discovery.json"
    path.write_text(json.dumps({"answers": {"project_type": "landing",
                                            "primary_goal": "commercial skip hire quote"}}), encoding="utf-8")
    seq = select_for_brief(json.loads(path.read_text(encoding="utf-8")))
    assert seq["id"] == "lead-gen-service"


def test_the_result_says_why():
    seq = select_for_brief({"industry": "saas", "primary_goal": "start a free trial"})
    assert seq["why"] and "industry" in seq["why"]


def test_an_empty_brief_picks_nothing():
    assert select_for_brief({}) is None


# ------------------------------------------------------------- proof


def test_every_proof_section_names_its_kind():
    for entry in load_sequences():
        for s in entry["section_sequence"]:
            if "proof" in s:
                assert s["proof"] in PROOF_KINDS, (entry["id"], s["section"], s["proof"])
        marked = [s["section"] for s in entry["section_sequence"] if "proof" in s]
        looks = [s["section"] for s in entry["section_sequence"]
                 if re.search(r"proof|stats|testimonial|review|logo|metrics|case quote", s["section"], re.I)]
        assert set(looks) <= set(marked), f"{entry['id']}: proof sections without a proof kind: {set(looks) - set(marked)}"


def test_a_brief_without_proof_drops_the_proof_sections_with_a_reason():
    seq = select_for_brief({"primary_goal": "commercial skip hire quote", "proof": []})
    names = _ids(seq)
    assert "Proof/stats bar" not in names
    assert "Social proof / pull-quote" not in names
    dropped = {d["section"]: d["reason"] for d in seq["dropped"] if "section" in d}
    assert "Proof/stats bar" in dropped and "Social proof / pull-quote" in dropped
    for reason in dropped.values():
        assert "proof" in reason and "invent" in reason
    assert "proof/stats bar" not in seq["conversion_mechanisms"]
    assert "named testimonial" not in seq["conversion_mechanisms"]


def test_proof_the_client_has_stays():
    seq = select_for_brief({"primary_goal": "commercial skip hire quote", "proof": ["stats"]})
    names = _ids(seq)
    assert "Proof/stats bar" in names
    assert "Social proof / pull-quote" not in names


def test_no_phone_drops_the_phone_affordance_with_a_reason():
    seq = select_for_brief({"primary_goal": "commercial skip hire quote", "contact": ["form", "email"]})
    assert "phone affordance" not in seq["conversion_mechanisms"]
    assert any(d.get("mechanism") == "phone affordance" and "phone" in d["reason"] for d in seq["dropped"])


def test_unknown_proof_keeps_the_sections_but_marks_them():
    seq = select_for_brief({"primary_goal": "commercial skip hire quote"})
    marked = [s for s in seq["section_sequence"] if s.get("proof")]
    assert marked and seq["proof_unknown"] is True


def test_a_bad_proof_kind_is_refused_naming_the_field_and_the_choices():
    with pytest.raises(ValueError) as err:
        select_for_brief({"primary_goal": "quote", "proof": ["awards"]})
    msg = str(err.value)
    assert "proof" in msg and "testimonials" in msg


# ------------------------------------------------------------- pre-launch


def test_a_pre_launch_brief_gets_the_honest_pattern():
    seq = select_for_brief({"stage": "pre-launch", "industry": "saas", "primary_goal": "waitlist signups"})
    assert seq["id"] == "pre-launch"
    assert not [s for s in seq["section_sequence"] if s.get("proof")], "pre-launch has no proof section"
    text = json.dumps(seq).lower()
    assert "waitlist" in text or "early access" in text
    assert seq["dropped"], "the pre-launch pick states what it left out and why"


def test_the_pre_launch_pattern_never_asks_for_invented_proof():
    entry = next(e for e in load_sequences() if e["id"] == "pre-launch")
    blob = json.dumps(entry).lower()
    for banned in ("testimonial", "logo wall", "trusted by", "stats bar"):
        assert banned not in blob, banned


def test_a_bad_stage_is_refused():
    with pytest.raises(ValueError) as err:
        select_for_brief({"stage": "beta"})
    assert "stage" in str(err.value) and "pre-launch" in str(err.value)
