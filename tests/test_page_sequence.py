"""Page-level section-sequence selector tests.

The build flow must produce RICH, COMPLETE pages: pick a whole-page skeleton from
the brief's structured fields, expand the FULL ordered sequence, and include
the conversion mechanisms. These tests pin the lead-gen sequence (the dogfood ground truth) so a
later reorder or a dropped mechanism can't pass silently.
"""
from engine.page_sequence import load_sequences, select_for_brief, select_sequence

# The lead-gen sequence MUST be exactly this order (canonical rule 9 / spec).
LEAD_GEN_ORDER = [
    "Hero (with inline quote/contact form)",
    "Proof/stats bar",
    "Value cards",
    "Category pills",
    "Item cards",
    "Split feature rows",
    "Coverage",
    "Social proof / pull-quote",
    "CTA band",
    "Rich footer",
]
LEAD_GEN_MECHANISMS = [
    "inline hero form",
    "proof/stats bar",
    "trust signals",
    "phone affordance",
]


def _sections(entry):
    return [s["section"] for s in entry["section_sequence"]]


def test_manifest_loads_with_entries():
    entries = load_sequences()
    assert entries, "page-sequences.json should load at least one entry"
    assert any(e["id"] == "lead-gen-service" for e in entries)


def test_select_by_id_returns_the_entry():
    seq = select_sequence("lead-gen-service")
    assert seq is not None and seq["id"] == "lead-gen-service"
    assert seq["section_sequence"][0]["section"] == "Hero (with inline quote/contact form)"
    assert select_sequence("Lead-gen-service")["id"] == "lead-gen-service"


def test_free_text_never_picks_a_sequence():
    for text in ("commercial skip hire quote", "a SaaS platform marketing site with a free trial",
                 ["skip hire", "quote", "coverage area"], "", None, "zzzz qqqq"):
        assert select_sequence(text) is None, text


def test_a_local_service_brief_gets_the_full_lead_gen_sequence():
    seq = select_for_brief({"product_type": "local-service"})
    assert seq["id"] == "lead-gen-service"
    assert _sections(seq) == LEAD_GEN_ORDER
    for mech in LEAD_GEN_MECHANISMS:
        assert mech in seq["conversion_mechanisms"], mech


def test_the_pick_is_deterministic():
    brief = {"product_type": "local-service", "primary_action": "quote"}
    assert select_for_brief(brief) == select_for_brief(brief)
