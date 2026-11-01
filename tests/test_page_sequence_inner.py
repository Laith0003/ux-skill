"""Inner pages of a site, picked by the page field, and one page family.

A pricing, about, contact, customers, customer story or legal page opens on
a secondary hero that orients inside the site (the page's own name, one
line, one action) and shares the site's header, closing band and footer
with every page built in the same run.
"""
from __future__ import annotations

import json

import pytest

from engine.page_sequence import load_sequences, select_for_brief
from engine.page_sequence.core import PAGES

INNER = {"pricing": "pricing-page", "about": "about-page", "contact": "contact-page",
         "customers": "customers-page", "customer-story": "customer-story",
         "legal": "legal-page"}


@pytest.mark.parametrize("page,sid", sorted(INNER.items()))
def test_the_page_field_picks_the_inner_sequence_and_says_why(page, sid):
    assert page in PAGES
    seq = select_for_brief({"product_type": "software", "page": page})
    assert seq["id"] == sid
    assert f"page {page}" in seq["why"]
    hero = seq["section_sequence"][0]
    assert hero["section"].startswith("Secondary hero") and hero["job"] == "ask"
    assert "one action" in hero["purpose"]


@pytest.mark.parametrize("sid", sorted(INNER.values()))
def test_an_inner_page_shares_the_sites_header_band_and_footer(sid):
    entry = next(e for e in load_sequences() if e["id"] == sid)
    notes = entry["notes"].lower()
    assert "one page family" in notes and "header" in notes and "footer" in notes
    assert entry["section_sequence"][-2]["job"] == "ask"
    assert entry["section_sequence"][-1]["job"] == "navigation"


def test_an_inner_page_before_launch_stays_an_inner_page():
    seq = select_for_brief({"page": "legal", "stage": "pre-launch"})
    assert seq["id"] == "legal-page"


def test_the_pricing_page_recomposes_a_comparison_on_a_phone():
    seq = select_for_brief({"page": "pricing"})
    text = json.dumps(seq).lower()
    assert "plan switcher" in text and "recommended plan" in text


def test_customer_proof_is_dropped_when_the_client_has_none():
    seq = select_for_brief({"page": "customers", "proof": []})
    assert not [s for s in seq["section_sequence"] if s.get("proof")]
    assert seq["dropped"]


@pytest.mark.parametrize("page", ["customers", "customer-story"])
def test_a_pre_launch_inner_page_drops_its_proof_with_the_pre_launch_reason(page):
    seq = select_for_brief({"page": page, "stage": "pre-launch"})
    assert seq["id"] == INNER[page]
    assert not [s for s in seq["section_sequence"] if s.get("proof")]
    assert seq["dropped"] and all("not launched" in d["reason"] for d in seq["dropped"])
    assert "stage pre-launch" in seq["why"]


def test_where_to_find_us_needs_an_address():
    seq = select_for_brief({"page": "contact", "contact": ["email"]})
    names = [s["section"] for s in seq["section_sequence"]]
    assert "Where to find us" not in names
    reason = next(d["reason"] for d in seq["dropped"] if d.get("section") == "Where to find us")
    assert "address" in reason and "contact" in reason


def test_where_to_find_us_stays_with_an_address_or_an_unknown_contact_list():
    for brief in ({"page": "contact", "contact": ["address", "email"]}, {"page": "contact"}):
        names = [s["section"] for s in select_for_brief(brief)["section_sequence"]]
        assert "Where to find us" in names


def test_a_section_contact_need_names_a_contact_kind():
    from engine.page_sequence.core import CONTACT_KINDS
    for entry in load_sequences():
        for s in entry["section_sequence"]:
            if "contact" in s:
                assert s["contact"] in CONTACT_KINDS, (entry["id"], s["section"])
