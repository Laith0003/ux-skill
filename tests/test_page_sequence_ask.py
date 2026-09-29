"""What the page asks for sets how much it argues before it asks.

A light ask (an email, a phone number) can sit in the hero; a heavy one (card
details, a call, a purchase, a contract) needs its objections answered above
the first place it is repeated. How the visitor arrives changes what the page
explains: a visitor who searched the brand's name needs no case for the
category. The objections come from the customer's own words, typed, and each
one is placed in the section that answers it. Three brief fields carry this
(commitment, arrival, objections), checked like every other structured field;
no industry and no word of the prose decides any of it. Every brief here is
invented.
"""
from __future__ import annotations

import json

import pytest

from engine.page_sequence import load_sequences, select_for_brief
from engine.page_sequence.core import (
    ARRIVALS,
    COMMITMENTS,
    HEAVY_COMMITMENTS,
    JOBS,
    OBJECTION_TYPES,
    PAGES,
)


def _names(seq):
    return [s["section"] for s in seq["section_sequence"]]


def _jobs(seq):
    return [s["job"] for s in seq["section_sequence"]]


# ------------------------------------------------------------- every section has a job


def test_every_section_of_every_sequence_names_its_job():
    for entry in load_sequences():
        for s in entry["section_sequence"]:
            assert s.get("job") in JOBS, (entry["id"], s["section"], s.get("job"))


def test_the_hero_asks_the_footer_navigates_and_the_band_before_it_asks():
    for entry in load_sequences():
        jobs = [s["job"] for s in entry["section_sequence"]]
        assert jobs[0] == "ask", entry["id"]
        assert jobs[-1] == "navigation", entry["id"]
        assert jobs[-2] == "ask", entry["id"]


def test_the_result_carries_each_sections_job():
    seq = select_for_brief({"product_type": "software"})
    assert all(j in JOBS for j in _jobs(seq))


# ------------------------------------------------------------- the fields are checked


def test_the_field_values():
    assert set(HEAVY_COMMITMENTS) == {"card", "call", "purchase", "contract"}
    assert set(HEAVY_COMMITMENTS) < set(COMMITMENTS)
    assert set(COMMITMENTS) == {"email", "phone", "account", "trial", "card", "call",
                                "purchase", "contract"}
    assert set(ARRIVALS) == {"cold", "warm", "branded", "returning"}
    assert set(OBJECTION_TYPES) == {"function", "risk", "price", "payback", "timing", "approval"}


@pytest.mark.parametrize("field,value", [("commitment", "signature"), ("arrival", "paid"),
                                         ("commitment", ["card"]), ("arrival", 3)])
def test_a_value_outside_the_choices_is_refused_naming_the_field_and_the_fix(field, value):
    with pytest.raises(ValueError) as err:
        select_for_brief({"product_type": "software", field: value})
    msg = str(err.value)
    assert msg.startswith(field + ":"), msg
    choices = COMMITMENTS if field == "commitment" else ARRIVALS
    assert all(c in msg for c in choices), msg
    assert "leave it out" in msg


@pytest.mark.parametrize("objections,where,fix", [
    ("people ask about price", "objections:", "list"),
    (["too expensive"], "objections[0]:", "quote, type and source"),
    ([{"quote": "", "type": "price", "source": "review"}], "objections[0].quote:", "own words"),
    ([{"quote": "Will my accountant accept it?", "type": "politics", "source": "call"}],
     "objections[0].type:", "approval"),
    ([{"quote": "a", "type": "risk", "source": "call"},
      {"quote": "Is it safe?", "type": "risk"}], "objections[1].source:", "where the words"),
])
def test_a_malformed_objection_names_its_position_field_and_fix(objections, where, fix):
    with pytest.raises(ValueError) as err:
        select_for_brief({"product_type": "software", "objections": objections})
    msg = str(err.value)
    assert msg.startswith(where), msg
    assert fix in msg, msg


def test_leaving_the_fields_out_changes_nothing():
    plain = select_for_brief({"product_type": "software"})
    blank = select_for_brief({"product_type": "software", "commitment": "", "arrival": None,
                              "objections": None})
    assert plain == blank
    assert plain["objection_map"] == [] and plain["at_the_ask"] == []


def test_the_fields_arrive_through_a_discovery_file_too():
    seq = select_for_brief({"answers": {"product_type": "software", "commitment": "card"}})
    assert "commitment card" in seq["why"]


# ------------------------------------------------------------- a light ask


@pytest.mark.parametrize("commitment", ["email", "phone", "account", "trial"])
def test_a_light_ask_keeps_the_sequence_and_says_so(commitment):
    plain = select_for_brief({"product_type": "software"})
    seq = select_for_brief({"product_type": "software", "commitment": commitment})
    assert _names(seq) == _names(plain)
    assert f"commitment {commitment}: a light ask" in seq["why"]


# ------------------------------------------------------------- a heavy ask


def _first(seq, jobs, start=1):
    return next(i for i, s in enumerate(seq["section_sequence"]) if i >= start
                and s["job"] in jobs)


@pytest.mark.parametrize("brief", [
    {"product_type": "software"}, {"product_type": "local-service"},
    {"product_type": "commerce"}, {"product_type": "marketplace", "primary_side": "supply"},
    {"product_type": "app", "platforms": ["web"]}, {"page": "feature"}, {},
    {"product_type": "editorial"}, {"page_sequence": "portfolio-agency"},
])
@pytest.mark.parametrize("commitment", ["card", "call", "purchase", "contract"])
def test_a_heavy_ask_is_repeated_only_after_an_objection_or_proof(brief, commitment):
    seq = select_for_brief({**brief, "commitment": commitment})
    first_answer = _first(seq, ("proof", "objection"))
    first_repeat = _first(seq, ("ask",))
    assert first_repeat > first_answer, (seq["id"], _names(seq))
    assert f"commitment {commitment}: a heavy ask" in seq["why"]


def test_a_heavy_ask_adds_a_mid_page_ask_right_after_the_argument():
    seq = select_for_brief({"product_type": "software", "commitment": "card"})
    names = _names(seq)
    at = names.index("Mid-page ask")
    assert seq["section_sequence"][at - 1]["section"] == "Logo / trust strip"
    assert seq["section_sequence"][at]["job"] == "ask"
    assert "Mid-page ask" in seq["why"] and "Logo / trust strip" in seq["why"]


def test_an_ask_placed_before_the_argument_moves_below_it():
    seq = select_for_brief({"product_type": "editorial", "commitment": "card"})
    names = _names(seq)
    signup = names.index("Newsletter signup")
    answer = _first(seq, ("proof", "objection"))
    assert signup == answer + 1, names
    assert "moved Newsletter signup below" in seq["why"]


def test_with_no_argument_left_a_heavy_ask_gets_an_objection_section_before_the_band():
    seq = select_for_brief({"product_type": "app", "platforms": ["ios"], "commitment": "purchase",
                            "proof": []})
    names = _names(seq)
    at = names.index("FAQ (objections)")
    assert seq["section_sequence"][at]["job"] == "objection"
    assert seq["section_sequence"][at + 1]["section"] == "CTA band (download)"
    assert "FAQ (objections)" in seq["why"]
    assert "Mid-page ask" not in names


def test_the_pick_does_not_change_with_the_commitment():
    for commitment in COMMITMENTS:
        assert select_for_brief({"product_type": "software", "commitment": commitment})["id"] \
            == "saas-marketing"


# ------------------------------------------------------------- arrival


def test_a_cold_arrival_with_a_heavy_ask_offers_a_lighter_step_as_a_link():
    seq = select_for_brief({"product_type": "software", "commitment": "call",
                            "arrival": "cold"})
    assert "arrival cold" in seq["why"]
    placement = seq["cta_placement"].lower()
    assert "text link" in placement and "never a second button" in placement
    assert "lighter step (text link)" in seq["conversion_mechanisms"]


@pytest.mark.parametrize("brief", [{"arrival": "cold", "commitment": "email"},
                                   {"arrival": "warm", "commitment": "card"},
                                   {"arrival": "cold"}])
def test_the_lighter_step_needs_both_a_cold_arrival_and_a_heavy_ask(brief):
    seq = select_for_brief({"product_type": "software", **brief})
    assert "lighter step (text link)" not in seq["conversion_mechanisms"]


def test_a_branded_arrival_drops_the_case_for_the_category():
    base = select_for_brief({"product_type": "software", "primary_action": "demo"})
    assert "The problem and the stakes" in _names(base)
    seq = select_for_brief({"product_type": "software", "primary_action": "demo",
                            "arrival": "branded"})
    assert "The problem and the stakes" not in _names(seq)
    reason = next(d["reason"] for d in seq["dropped"]
                  if d.get("section") == "The problem and the stakes")
    assert "arrival branded" in reason
    assert "arrival branded" in seq["why"]


def test_a_branded_arrival_on_a_page_with_no_category_case_changes_nothing():
    plain = select_for_brief({"product_type": "software"})
    seq = select_for_brief({"product_type": "software", "arrival": "branded"})
    assert _names(seq) == _names(plain) and seq["dropped"] == plain["dropped"]


def test_only_the_arrival_field_marks_a_section_as_a_case_for_the_category():
    marked = sorted((e["id"], s["section"]) for e in load_sequences()
                    for s in e["section_sequence"] if s.get("explains_category"))
    assert marked == [("pre-launch", "The problem"), ("trust-led", "The problem and the stakes")]


# ------------------------------------------------------------- objections


OBJ = [
    {"quote": "Does it work with the till we already have?", "type": "function",
     "source": "support ticket"},
    {"quote": "What if the numbers are wrong at month end?", "type": "risk",
     "source": "sales call"},
    {"quote": "Is it cheaper than what we pay now?", "type": "price", "source": "review"},
    {"quote": "I need something to show my manager", "type": "approval",
     "source": "lost deal"},
]


def test_each_objection_is_placed_in_the_section_that_answers_it():
    seq = select_for_brief({"product_type": "software", "primary_action": "demo",
                            "objections": OBJ})
    placed = {o["type"]: o["section"] for o in seq["objection_map"]}
    assert placed["function"] == "How it works"
    assert placed["risk"].startswith("FAQ")
    assert placed["price"].startswith("FAQ")
    assert placed["approval"].startswith("FAQ")
    kept = [(o["quote"], o["type"], o["source"]) for o in seq["objection_map"]]
    assert kept == [(o["quote"], o["type"], o["source"]) for o in OBJ]


def test_a_price_objection_goes_to_the_pricing_section_when_there_is_one():
    seq = select_for_brief({"product_type": "software", "objections": OBJ[2:3]})
    assert seq["objection_map"][0]["section"] == "Pricing teaser"


def test_objections_on_a_page_with_no_faq_get_one_before_the_closing_band():
    seq = select_for_brief({"product_type": "software", "objections": OBJ[1:2]})
    names = _names(seq)
    assert names[names.index("FAQ (objections)") + 1] == "CTA band"
    assert seq["objection_map"][0]["section"] == "FAQ (objections)"
    assert names.count("FAQ (objections)") == 1


def test_a_heavy_ask_and_objections_share_one_objection_section():
    seq = select_for_brief({"product_type": "app", "platforms": ["ios"], "commitment": "purchase",
                            "proof": [], "objections": OBJ[1:2]})
    assert _names(seq).count("FAQ (objections)") == 1


def test_objection_quotes_are_kept_exactly_as_given():
    odd = [{"quote": "  honestly?? is it SAFE  ", "type": "risk", "source": "comment"}]
    seq = select_for_brief({"product_type": "software", "objections": odd})
    assert seq["objection_map"][0]["quote"] == "  honestly?? is it SAFE  "


def test_every_faq_says_where_its_questions_come_from():
    for entry in load_sequences():
        for s in entry["section_sequence"]:
            if s["section"].startswith("FAQ"):
                assert "objections" in s["purpose"], (entry["id"], s["section"])
                assert "operational questions" in s["purpose"], (entry["id"], s["section"])


# ------------------------------------------------------------- at the ask


def test_the_answers_needed_at_the_ask_grow_with_the_commitment():
    light = select_for_brief({"product_type": "software", "commitment": "email"})["at_the_ask"]
    trial = select_for_brief({"product_type": "software", "commitment": "trial"})["at_the_ask"]
    heavy = select_for_brief({"product_type": "software", "commitment": "card"})["at_the_ask"]
    assert light and set(light) < set(trial) < set(heavy)
    joined = " ".join(heavy).lower()
    for need in ("who runs", "data", "goes wrong", "next"):
        assert need in joined, need


# ------------------------------------------------------------- campaign pages


def test_campaign_is_a_page_value():
    assert "campaign" in PAGES


def test_a_campaign_page_closes_its_exits():
    home = select_for_brief({"product_type": "software"})
    seq = select_for_brief({"product_type": "software", "page": "campaign"})
    assert seq["id"] == home["id"]
    assert "page campaign" in seq["why"]
    foot = seq["section_sequence"][-1]
    assert foot["job"] == "navigation" and foot["section"] == "Compact footer"
    assert "legal" in foot["purpose"].lower() and "contact" in foot["purpose"].lower()
    assert "sitemap" not in (foot["purpose"] + seq["footer"]).lower()
    placement = seq["cta_placement"].lower()
    assert "no nav links" in placement and "new tab" in placement


def test_a_home_page_keeps_its_sitemap_footer():
    seq = select_for_brief({"product_type": "software", "page": "home"})
    assert "sitemap" in seq["footer"].lower()


def test_a_campaign_footer_names_only_the_routes_the_client_has():
    seq = select_for_brief({"product_type": "local-service", "page": "campaign",
                            "contact": ["form"]})
    assert "phone" not in json.dumps(seq["section_sequence"][-1]).lower()
