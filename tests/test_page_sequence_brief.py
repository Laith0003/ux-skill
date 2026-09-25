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


# Briefs filled the way /ux-system fills them: industry from its list (or one of
# its other names), product_type from the one vocabulary the engine and the
# picker share (app, software, marketing-site, editorial, commerce, marketplace,
# local-service) or one of its aliases.
@pytest.mark.parametrize("brief", [
    # A pharmacy ordering app that sells from warehouses to pharmacies.
    {"primary_goal": "Pharmacies open an account and order from warehouses", "project_type": "landing",
     "audience": "pharmacy owners and drug warehouses", "industry": "pharmacy", "product_type": "marketplace",
     "description": "a B2B marketplace for pharmacy supply"},
    # Building materials: the industry by its other name, the product a marketplace.
    {"answers": {"primary_goal": "Book a demo", "audience": "contractors",
                 "industry": "building-materials", "product_type": "marketplace",
                 "description": "contractors order cement and steel online"}},
    {"industry": "ecommerce", "product_type": "marketplace",
     "description": "contractors order cement and steel online"},
    {"industry": "ecommerce", "product_type": "b2b-marketplace"},
    {"industry": "construction", "product_type": "commerce", "primary_goal": "order cement and steel"},
    {"industry": "b2b-marketplace", "product_type": "marketing-site", "audience": "clinics"},
    {"industry": "wholesale", "audience": "retailers"},
])
def test_b2b_marketplace_briefs_get_the_marketplace_sequence(brief):
    seq = select_for_brief(brief)
    assert seq is not None and seq["id"] == "b2b-marketplace", (seq["id"], seq["why"])


def test_product_type_outranks_industry():
    """commerce narrows to the shop and the marketplace; the industry then picks within."""
    seq = select_for_brief({"industry": "construction", "product_type": "commerce"})
    assert seq["id"] == "b2b-marketplace"
    assert seq["why"].index("product_type") < seq["why"].index("industry")
    assert select_for_brief({"industry": "ecommerce", "product_type": "editorial"})["id"] == "content-publication"
    assert select_for_brief({"industry": "saas", "product_type": "commerce"})["id"] == "ecommerce-product"
    assert select_for_brief({"industry": "saas", "product_type": "local-service"})["id"] == "lead-gen-service"


@pytest.mark.parametrize("written,value,expect", [
    ("b2b-marketplace", "marketplace", "b2b-marketplace"), ("saas", "software", "saas-marketing"),
    ("web-app", "software", "saas-marketing"), ("mobile-app", "app", "app-mobile-landing"),
    ("shop", "commerce", "ecommerce-product"), ("store", "commerce", "ecommerce-product"),
    ("service", "local-service", "lead-gen-service"),
])
def test_a_product_type_alias_is_mapped_and_reported(written, value, expect):
    seq = select_for_brief({"product_type": written})
    assert seq["id"] == expect
    assert f"product_type {value} (from {written})" in seq["why"]


@pytest.mark.parametrize("brief,expect", [
    ({"industry": "building-materials", "product_type": "b2b-marketplace", "tone": ["solid", "practical"],
      "proof": [], "contact": ["form", "whatsapp"], "stage": "live",
      "primary_goal": "contractors order cement and steel online"}, "b2b-marketplace"),
    ({"industry": "security", "product_type": "saas", "proof": ["certifications"],
      "primary_goal": "Book a demo"}, "trust-led"),
    ({"industry": "healthcare", "product_type": "service", "contact": ["phone"]}, "lead-gen-service"),
    ({"industry": "editorial-media", "product_type": "Web app"}, "saas-marketing"),
])
def test_system_build_and_the_picker_read_the_same_brief(tmp_path, brief, expect):
    """One brief file feeds both: the build accepts it, the picker accepts it,
    and both read product_type as the same value."""
    click = pytest.importorskip("click")  # noqa: F841
    from click.testing import CliRunner
    from engine.cli.main import cli
    path = tmp_path / "system-brief.json"
    path.write_text(json.dumps(brief), encoding="utf-8")
    result = CliRunner().invoke(cli, ["--no-pretty", "system", "build", "--brand", "#3366FF",
                                      "--brief", str(path), "--out", str(tmp_path / "ds")])
    assert result.exit_code == 0, result.output
    built = json.loads(result.stdout)["audience"]["product_type"]
    seq = select_for_brief(json.loads(path.read_text(encoding="utf-8")))
    assert seq["id"] == expect, seq["why"]
    assert f"product_type {built}" in seq["why"]


def test_a_product_type_the_build_refuses_the_picker_refuses_too(tmp_path):
    from click.testing import CliRunner
    from engine.cli.main import cli
    path = tmp_path / "system-brief.json"
    path.write_text(json.dumps({"product_type": "brochure"}), encoding="utf-8")
    result = CliRunner().invoke(cli, ["--no-pretty", "system", "build", "--brand", "#3366FF",
                                      "--brief", str(path), "--out", str(tmp_path / "ds")])
    assert result.exit_code != 0
    with pytest.raises(ValueError):
        select_for_brief({"product_type": "brochure"})


def test_the_picker_shares_the_engines_product_type_vocabulary():
    from engine.foundations import audience
    from engine.page_sequence.core import product_type_vocabulary
    values, aliases = product_type_vocabulary()
    assert tuple(values) == tuple(audience.PRODUCT_TYPES)
    assert set(values) == {"app", "software", "marketing-site", "editorial", "commerce", "marketplace",
                           "local-service"}
    assert aliases == dict(audience.PRODUCT_ALIASES)


def test_the_industry_value_is_not_counted_again_as_a_phrase():
    seq = select_for_brief({"industry": "ecommerce"})
    assert "phrases" not in seq["why"]


def test_a_product_type_outside_the_engine_list_is_refused():
    with pytest.raises(ValueError) as err:
        select_for_brief({"product_type": "brochure"})
    msg = str(err.value)
    assert "product_type" in msg and "commerce" in msg


def test_a_consumer_marketplace_is_not_the_b2b_sequence():
    seq = select_for_brief({"description": "consumer marketplace for used cars", "industry": "automotive"})
    assert seq["id"] != "b2b-marketplace"
    seq = select_for_brief({"description": "pharmacy ordering app, stock comes from warehouses",
                            "industry": "healthcare"})
    assert seq["id"] != "b2b-marketplace"


def test_the_marketplace_keys_need_a_b2b_signal():
    entry = next(e for e in load_sequences() if e["id"] == "b2b-marketplace")
    assert "marketplace" not in entry["keywords"] and "warehouses" not in entry["keywords"]


def test_b2b_software_still_gets_saas():
    seq = select_for_brief({"primary_goal": "start a free trial", "industry": "saas",
                            "audience": "B2B finance teams", "description": "a reporting platform"})
    assert seq["id"] == "saas-marketing"


# ------------------------------------------------------------- always a sequence


def _engine_industries():
    from engine.synthesizer.axes import INDUSTRY_ALIASES, INDUSTRY_SEEDS
    return sorted(INDUSTRY_SEEDS), dict(INDUSTRY_ALIASES)


def test_every_manifest_field_value_is_one_the_engine_reads():
    from engine.foundations.audience import PRODUCT_TYPES
    seeds, _ = _engine_industries()
    for entry in load_sequences():
        assert set(entry["industries"]) <= set(seeds), (entry["id"], set(entry["industries"]) - set(seeds))
        assert set(entry["product_types"]) <= set(PRODUCT_TYPES), entry["id"]


@pytest.mark.parametrize("industry", _engine_industries()[0] + sorted(_engine_industries()[1]))
def test_every_ux_system_industry_picks_a_sequence_that_lists_it(industry):
    seeds, aliases = _engine_industries()
    seq = select_for_brief({"industry": industry})
    assert seq is not None
    assert aliases.get(industry, industry) in seq["industries"], (industry, seq["id"])


@pytest.mark.parametrize("brief,expect", [
    ({"industry": "fintech-banking", "primary_goal": "Book a demo with our security team",
      "proof": ["certifications"]}, "trust-led"),
    ({"industry": "security", "primary_goal": "book a security review"}, "trust-led"),
    ({"industry": "healthcare", "primary_goal": "Book an appointment"}, "lead-gen-service"),
    ({"industry": "hospitality-travel", "primary_goal": "book a room"}, "lead-gen-service"),
    ({"industry": "gaming"}, "app-mobile-landing"),
])
def test_common_briefs_reach_a_sensible_sequence(brief, expect):
    assert select_for_brief(brief)["id"] == expect


def test_the_trust_sequence_takes_certifications_as_proof():
    entry = next(e for e in load_sequences() if e["id"] == "trust-led")
    assert "certifications" in {s.get("proof") for s in entry["section_sequence"]}


@pytest.mark.parametrize("brief", [{}, {"audience": "people"}, {"primary_goal": "book"},
                                   {"tone": ["calm"]}])
def test_the_picker_always_returns_a_sequence(brief):
    seq = select_for_brief(brief)
    assert seq is not None and seq["id"] == "general-landing"
    assert seq["section_sequence"] and "general" in seq["why"]


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


def test_the_general_sequence_keeps_proof_optional_and_asks_nothing_invented():
    entry = next(e for e in load_sequences() if e["id"] == "general-landing")
    kinds = [s["proof"] for s in entry["section_sequence"] if s.get("proof")]
    assert kinds, "the general sequence has one proof section, dropped when the brief has none"
    seq = select_for_brief({"proof": []})
    assert not [s for s in seq["section_sequence"] if s.get("proof")]


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


def test_pre_launch_with_listed_proof_says_how_to_show_it():
    seq = select_for_brief({"stage": "pre-launch", "industry": "saas", "proof": ["stats"]})
    assert seq["id"] == "pre-launch"
    assert any("stage" in d["reason"] and "live" in d["reason"] for d in seq["dropped"])


def test_a_dropped_phone_leaves_no_phone_in_the_section_text():
    seq = select_for_brief({"primary_goal": "commercial skip hire quote", "contact": ["form", "email"]})
    blob = json.dumps(seq["section_sequence"]).lower() + seq["cta_placement"].lower() + seq["footer"].lower()
    assert "phone" not in blob
    kept = select_for_brief({"primary_goal": "commercial skip hire quote", "contact": ["phone"]})
    assert "phone" in json.dumps(kept["section_sequence"]).lower()


def test_the_b2b_faq_comes_before_the_closing_band():
    entry = next(e for e in load_sequences() if e["id"] == "b2b-marketplace")
    names = [s["section"] for s in entry["section_sequence"]]
    faq = next(i for i, n in enumerate(names) if n.startswith("FAQ"))
    band = next(i for i, n in enumerate(names) if n.startswith("CTA band"))
    assert faq < band


def test_the_pre_launch_pattern_never_asks_for_invented_proof():
    entry = next(e for e in load_sequences() if e["id"] == "pre-launch")
    blob = json.dumps(entry).lower()
    for banned in ("testimonial", "logo wall", "trusted by", "stats bar"):
        assert banned not in blob, banned


def test_a_bad_stage_is_refused():
    with pytest.raises(ValueError) as err:
        select_for_brief({"stage": "beta"})
    assert "stage" in str(err.value) and "pre-launch" in str(err.value)
