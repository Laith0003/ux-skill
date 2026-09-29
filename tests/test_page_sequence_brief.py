"""The page-sequence picker reads a 4.0 brief, not one word of it.

Real landing builds showed the picker keying on the verb "book", on an industry
and on a phrase, returning the SaaS plan for a B2B marketplace, and asking for
stats, a named testimonial and a phone number the client did not have. These
tests pin the fixes: only structured fields pick a sequence, never an industry
or a word of the prose, and a proof section the client cannot fill is dropped
with a stated reason instead of invented.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from engine.page_sequence import load_sequences, select_for_brief

ROOT = Path(__file__).resolve().parents[1]
PROOF_KINDS = {"stats", "testimonials", "logos", "reviews", "case-studies", "certifications", "press"}


def _ids(seq):
    return [s["section"] for s in seq["section_sequence"]]


# ------------------------------------------------------------- no word picks


@pytest.mark.parametrize("brief", [
    {"primary_goal": "Book a demo"}, {"description": "commercial skip hire quote"},
    {"audience": "B2B finance teams", "description": "a stored value wallet for payments at shops"},
    {"primary_goal": "download the app"}, {"description": "wholesale pharmacy supply marketplace"},
])
def test_no_word_of_the_brief_picks_a_sequence(brief):
    seq = select_for_brief(brief)
    assert seq["id"] == "general-landing", (brief, seq["why"])
    assert "product_type" in seq["why"] and "primary_action" in seq["why"]


def test_no_entry_carries_a_keyword_or_industry_table():
    for entry in load_sequences():
        for key in ("keywords", "industries", "product_types", "project_types"):
            assert key not in entry, (entry["id"], key)
        assert entry.get("picked_by"), entry["id"]


def _engine_industries():
    from engine.synthesizer.axes import INDUSTRY_ALIASES, INDUSTRY_SEEDS
    return sorted(INDUSTRY_SEEDS) + sorted(INDUSTRY_ALIASES)


@pytest.mark.parametrize("industry", _engine_industries())
def test_industry_alone_never_picks_a_sequence(industry):
    seq = select_for_brief({"industry": industry})
    assert seq["id"] == "general-landing", (industry, seq["id"])
    assert "industry informs the copy" in seq["why"]
    base = select_for_brief({"product_type": "commerce"})["id"]
    assert select_for_brief({"product_type": "commerce", "industry": industry})["id"] == base


# ------------------------------------------------------------- product_type


@pytest.mark.parametrize("brief,expect", [
    ({"product_type": "marketplace"}, "b2b-marketplace"),
    ({"product_type": "b2b-marketplace"}, "b2b-marketplace"),
    ({"product_type": "commerce"}, "ecommerce-product"),
    ({"product_type": "shop"}, "ecommerce-product"),
    ({"product_type": "editorial"}, "content-publication"),
    ({"product_type": "local-service"}, "lead-gen-service"),
    ({"product_type": "service"}, "lead-gen-service"),
    ({"product_type": "software"}, "saas-marketing"),
    ({"product_type": "saas"}, "saas-marketing"),
    ({"product_type": "software", "primary_action": "demo"}, "trust-led"),
    ({"product_type": "app", "platforms": ["ios", "android"]}, "app-mobile-landing"),
    ({"project_type": "mobile-app"}, "app-mobile-landing"),
])
def test_product_type_and_its_refinements_pick(brief, expect):
    assert select_for_brief(brief)["id"] == expect, select_for_brief(brief)["why"]


@pytest.mark.parametrize("written,value", [
    ("b2b-marketplace", "marketplace"), ("saas", "software"), ("web-app", "software"),
    ("mobile-app", "app"), ("shop", "commerce"), ("store", "commerce"), ("service", "local-service"),
])
def test_a_product_type_alias_is_mapped_and_reported(written, value):
    seq = select_for_brief({"product_type": written, "platforms": ["web"]})
    assert f"product_type {value} (from {written})" in seq["why"]


def test_an_app_without_platforms_asks_for_them():
    seq = select_for_brief({"product_type": "app"})
    assert seq["id"] == "general-landing"
    assert "platforms" in seq["why"] and "store platform" in seq["why"]


def test_marketing_site_says_how_to_choose():
    seq = select_for_brief({"product_type": "marketing-site"})
    assert seq["id"] == "general-landing" and "page_sequence" in seq["why"]


@pytest.mark.parametrize("action,expect", [
    ("quote", "lead-gen-service"), ("book", "lead-gen-service"), ("contact", "lead-gen-service"),
    ("buy", "ecommerce-product"), ("subscribe", "content-publication"), ("demo", "trust-led"),
    ("open-account", "b2b-marketplace"), ("sign-up", "saas-marketing"),
])
def test_primary_action_alone_picks(action, expect):
    seq = select_for_brief({"primary_action": action})
    assert seq["id"] == expect and f"primary_action {action}" in seq["why"]


def test_a_bad_primary_action_is_refused_with_the_choices():
    with pytest.raises(ValueError) as err:
        select_for_brief({"primary_action": "learn more"})
    assert str(err.value).startswith("primary_action") and "quote" in str(err.value)


@pytest.mark.parametrize("brief,expect", [
    ({"industry": "building-materials", "product_type": "b2b-marketplace", "tone": ["solid", "practical"],
      "proof": [], "contact": ["form", "whatsapp"], "stage": "live"}, "b2b-marketplace"),
    ({"industry": "security", "product_type": "saas", "proof": ["certifications"],
      "primary_action": "demo"}, "trust-led"),
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
    with pytest.raises(ValueError) as err:
        select_for_brief({"product_type": "brochure"})
    assert "product_type" in str(err.value) and "commerce" in str(err.value)


def test_the_picker_shares_the_engines_product_type_vocabulary():
    from engine.foundations import audience
    from engine.page_sequence.core import product_type_vocabulary
    values, aliases = product_type_vocabulary()
    assert tuple(values) == tuple(audience.PRODUCT_TYPES)
    assert aliases == dict(audience.PRODUCT_ALIASES)


def test_a_b2b_marketplace_sequence_exists():
    entry = next(e for e in load_sequences() if e["id"] == "b2b-marketplace")
    names = " ".join(_ids(entry)).lower()
    for part in ("buyer", "supplier", "categor", "how ordering works", "delivery", "faq", "footer"):
        assert part in names, part


def test_the_trust_sequence_takes_certifications_as_proof():
    entry = next(e for e in load_sequences() if e["id"] == "trust-led")
    assert "certifications" in {s.get("proof") for s in entry["section_sequence"]}


@pytest.mark.parametrize("brief", [{}, {"audience": "people"}, {"primary_goal": "book"},
                                   {"tone": ["calm"]}])
def test_the_picker_always_returns_a_sequence(brief):
    seq = select_for_brief(brief)
    assert seq is not None and seq["id"] == "general-landing"
    assert seq["section_sequence"] and "general" in seq["why"]


def test_an_explicit_sequence_id_wins():
    seq = select_for_brief({"page_sequence": "content-publication", "product_type": "commerce"})
    assert seq["id"] == "content-publication"
    assert "page_sequence" in seq["why"]


def test_an_unknown_sequence_id_is_refused_with_the_choices():
    with pytest.raises(ValueError) as err:
        select_for_brief({"page_sequence": "blog"})
    msg = str(err.value)
    assert "page_sequence" in msg and "content-publication" in msg


def test_the_discovery_file_shape_is_read(tmp_path: Path):
    path = tmp_path / "last-discovery.json"
    path.write_text(json.dumps({"answers": {"project_type": "landing", "product_type": "local-service",
                                            "primary_goal": "commercial skip hire quote"}}),
                    encoding="utf-8")
    seq = select_for_brief(json.loads(path.read_text(encoding="utf-8")))
    assert seq["id"] == "lead-gen-service"


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
                 if re.search(r"proof|stats|testimonial|review|logo|metrics|case quote", s["section"], re.IGNORECASE)]
        assert set(looks) <= set(marked), f"{entry['id']}: proof sections without a proof kind: {set(looks) - set(marked)}"


def test_a_brief_without_proof_drops_the_proof_sections_with_a_reason():
    seq = select_for_brief({"product_type": "local-service", "proof": []})
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
    seq = select_for_brief({"product_type": "local-service", "proof": ["stats"]})
    names = _ids(seq)
    assert "Proof/stats bar" in names
    assert "Social proof / pull-quote" not in names


def test_no_phone_drops_the_phone_affordance_with_a_reason():
    seq = select_for_brief({"product_type": "local-service", "contact": ["form", "email"]})
    assert "phone affordance" not in seq["conversion_mechanisms"]
    assert any(d.get("mechanism") == "phone affordance" and "phone" in d["reason"] for d in seq["dropped"])


def test_unknown_proof_keeps_the_sections_but_marks_them():
    seq = select_for_brief({"product_type": "local-service"})
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
    seq = select_for_brief({"product_type": "local-service", "contact": ["form", "email"]})
    blob = json.dumps(seq["section_sequence"]).lower() + seq["cta_placement"].lower() + seq["footer"].lower()
    assert "phone" not in blob
    kept = select_for_brief({"product_type": "local-service", "contact": ["phone"]})
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
