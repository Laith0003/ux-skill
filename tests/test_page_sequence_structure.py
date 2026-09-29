"""The page sequence follows the brief's structure, not its industry.

Two landing builds inside existing products showed the picker offering a
founding team and an early-access form on a page about one feature of a
product with users, store badges and a download band to a web app that signs
in by phone, and a buyer's page to a marketplace whose audience is its
suppliers. These tests pin the fields that decide instead: page, platforms,
sign_in and primary_side. Every brief here is invented.
"""
from __future__ import annotations

import json

import pytest

from engine.page_sequence import load_sequences, select_for_brief, select_sequence

STRUCTURAL = ("feature-page", "web-app", "marketplace-supply")


def _names(seq):
    return [s["section"] for s in seq["section_sequence"]]


def _blob(seq):
    return (json.dumps(seq["section_sequence"]) + seq["cta_placement"] + seq["footer"]
            + json.dumps(seq["conversion_mechanisms"])).lower()


def _industries():
    from engine.synthesizer.axes import INDUSTRY_SEEDS
    return sorted(INDUSTRY_SEEDS)


# ------------------------------------------------------------- feature page


def test_a_feature_page_of_a_live_product_has_no_team_and_no_early_access():
    seq = select_for_brief({"page": "feature", "stage": "live", "product_type": "app",
                            "primary_goal": "customers use split bills inside the app"})
    assert seq["id"] == "feature-page"
    assert "page feature" in seq["why"]
    blob = _blob(seq)
    for banned in ("early access", "early-access form in hero", "waitlist", "who is building",
                   "founder", "launch status"):
        assert banned not in blob.replace("never an early-access form", ""), banned
    assert "Who is building it" not in _names(seq)


def test_a_feature_page_before_launch_is_still_the_pre_launch_pattern():
    seq = select_for_brief({"page": "feature", "stage": "pre-launch", "product_type": "app"})
    assert seq["id"] == "pre-launch"


def test_home_leaves_the_pick_to_the_other_fields():
    assert select_for_brief({"page": "home", "product_type": "editorial"})["id"] == "content-publication"


# ------------------------------------------------------------- web app, phone sign-in


def test_a_web_app_that_signs_in_by_phone_has_no_store_badges_or_download():
    seq = select_for_brief({"product_type": "app", "platforms": ["web"], "sign_in": ["phone"],
                            "stage": "live"})
    assert seq["id"] == "web-app"
    assert "platforms web" in seq["why"]
    blob = _blob(seq)
    for banned in ("store badge", "app store", "play store", "download band", "device mock"):
        assert banned not in blob.replace("no store badges", "").replace("no download", ""), banned
    hero = seq["section_sequence"][0]["purpose"].lower()
    assert "phone number field" in hero
    band = next(s for s in seq["section_sequence"] if s["section"].startswith("CTA band"))
    assert "phone" in band["purpose"].lower()
    assert "phone sign-in" in seq["cta_placement"].lower()


def test_without_phone_sign_in_the_web_app_keeps_its_own_action():
    seq = select_for_brief({"product_type": "app", "platforms": ["web"], "sign_in": ["email"]})
    assert seq["id"] == "web-app"
    assert "phone number field" not in _blob(seq)
    assert not any("with_phone_sign_in" in s for s in seq["section_sequence"])
    assert "cta_placement_with_phone_sign_in" not in seq


def test_an_app_with_a_store_app_keeps_the_store_sequence():
    seq = select_for_brief({"product_type": "app", "platforms": ["web", "ios", "android"]})
    assert seq["id"] == "app-mobile-landing"


def test_a_mobile_project_that_runs_only_on_the_web_gets_the_web_sequence():
    seq = select_for_brief({"project_type": "mobile-app", "platforms": ["web"]})
    assert seq["id"] == "web-app"


# ------------------------------------------------------------- two-sided marketplace


def test_a_supply_side_audience_gets_the_supply_path():
    seq = select_for_brief({"product_type": "marketplace", "primary_side": "supply",
                            "audience": "independent bakeries that sell through the platform"})
    assert seq["id"] == "marketplace-supply"
    assert "primary_side supply" in seq["why"]
    names = " ".join(_names(seq)).lower()
    for buyer_only in ("how ordering works", "categories", "buyer and supplier paths"):
        assert buyer_only not in names, buyer_only
    assert "join" in seq["section_sequence"][0]["section"].lower()
    assert "supplier application in hero" in seq["conversion_mechanisms"]
    assert "account request in hero" not in seq["conversion_mechanisms"]


def test_the_demand_side_keeps_the_buyers_path():
    seq = select_for_brief({"product_type": "marketplace", "primary_side": "demand"})
    assert seq["id"] == "b2b-marketplace"
    assert "primary_side demand" in seq["why"]


def test_a_side_on_a_product_with_one_side_is_refused_with_the_fix():
    with pytest.raises(ValueError) as err:
        select_for_brief({"product_type": "editorial", "primary_side": "supply"})
    msg = str(err.value)
    assert "primary_side" in msg and "product_type" in msg and "marketplace" in msg


# ------------------------------------------------------------- products that must fit by fields


@pytest.mark.parametrize("brief,expect", [
    # A points card people check and spend in the browser, signed in by phone.
    ({"product_type": "app", "platforms": ["web"], "sign_in": ["phone"], "stage": "live",
      "industry": "consumer-lifestyle", "proof": []}, "web-app"),
    # A stored-value wallet with store apps.
    ({"product_type": "app", "platforms": ["ios", "android"], "industry": "fintech-payments"},
     "app-mobile-landing"),
    # The same wallet, used on the web only.
    ({"product_type": "app", "platforms": ["web"], "industry": "fintech-payments"}, "web-app"),
    # A retailer that sells online.
    ({"product_type": "shop", "industry": "consumer-lifestyle"}, "ecommerce-product"),
    # A loyalty network the shops join: the page speaks to the shops.
    ({"product_type": "marketplace", "primary_side": "supply", "industry": "consumer-lifestyle"},
     "marketplace-supply"),
    # The redeem feature of a loyalty app that has members.
    ({"page": "feature", "stage": "live", "product_type": "app", "platforms": ["web"],
      "sign_in": ["phone"]}, "feature-page"),
])
def test_loyalty_retail_and_wallet_products_fit_through_their_fields(brief, expect):
    assert select_for_brief(brief)["id"] == expect


@pytest.mark.parametrize("industry", _industries())
def test_the_same_structure_gives_the_same_sequence_in_every_industry(industry):
    web = select_for_brief({"product_type": "app", "platforms": ["web"], "industry": industry})
    store = select_for_brief({"product_type": "app", "platforms": ["ios"], "industry": industry})
    feature = select_for_brief({"page": "feature", "industry": industry})
    supply = select_for_brief({"product_type": "marketplace", "primary_side": "supply",
                               "industry": industry})
    assert (web["id"], store["id"], feature["id"], supply["id"]) == (
        "web-app", "app-mobile-landing", "feature-page", "marketplace-supply"), industry


def test_a_consumer_app_is_not_sent_to_a_demo_request_page_by_its_industry():
    """A demo request is how a business buys software, not how an app's users start."""
    seq = select_for_brief({"product_type": "app", "industry": "fintech-banking"})
    assert seq["id"] != "trust-led"
    assert "demo" not in seq["section_sequence"][0]["section"].lower()


# ------------------------------------------------------------- structural entries


def test_structural_sequences_are_reached_only_by_their_field():
    entries = {e["id"]: e for e in load_sequences()}
    for sid in STRUCTURAL:
        entry = entries[sid]
        assert entry.get("picked_by"), sid
        assert not entry["keywords"] and not entry["industries"] and not entry["product_types"], sid
    for text in ("feature page for our web app", "a marketplace supply side page", "web app"):
        seq = select_sequence(text)
        assert seq is None or seq["id"] not in STRUCTURAL, (text, seq and seq["id"])
    for brief in ({"description": "a web app feature page"}, {"primary_goal": "supply side sign up"}):
        assert select_for_brief(brief)["id"] not in STRUCTURAL, brief


def test_picked_by_is_not_in_the_result():
    assert "picked_by" not in select_for_brief({"page": "feature"})


def test_no_structural_sequence_invents_proof():
    for sid in STRUCTURAL:
        seq = select_for_brief({"page_sequence": sid, "proof": []})
        assert not [s for s in seq["section_sequence"] if s.get("proof")], sid
        assert seq["dropped"], sid


@pytest.mark.parametrize("field,value,word", [
    ("page", "landing", "feature"),
    ("platforms", ["mobile"], "android"),
    ("sign_in", ["otp"], "phone"),
    ("primary_side", "sellers", "supply"),
])
def test_a_value_outside_a_field_is_refused_naming_the_field_and_the_choices(field, value, word):
    brief = {field: value}
    if field == "primary_side":
        brief["product_type"] = "marketplace"
    with pytest.raises(ValueError) as err:
        select_for_brief(brief)
    msg = str(err.value)
    assert msg.startswith(field) and word in msg
