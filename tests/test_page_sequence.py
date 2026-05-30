"""Page-level section-sequence selector tests.

The build flow must produce RICH, COMPLETE pages: pick a whole-page skeleton by
goal, expand the FULL ordered sequence, and include the goal's conversion
mechanisms. These tests pin the lead-gen sequence (the dogfood ground truth) so a
later reorder or a dropped mechanism can't pass silently.
"""
from engine.page_sequence import select_sequence, score_sequence, load_sequences


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


def test_select_by_goal_returns_lead_gen():
    seq = select_sequence("lead-gen-service")
    assert seq is not None
    assert seq["id"] == "lead-gen-service"
    # First section is the Hero-with-form (the conversion path, never buried).
    assert seq["section_sequence"][0]["section"] == "Hero (with inline quote/contact form)"
    assert "form" in seq["section_sequence"][0]["section"].lower()


def test_select_by_brief_returns_lead_gen():
    """A free-text brief with no goal id still routes to lead-gen by keywords."""
    seq = select_sequence("commercial skip hire quote")
    assert seq is not None, "brief should match a sequence"
    assert seq["id"] == "lead-gen-service"


def test_lead_gen_full_ordered_sequence():
    seq = select_sequence("lead-gen-service")
    assert _sections(seq) == LEAD_GEN_ORDER, (
        "lead-gen section_sequence must match the canonical order exactly"
    )


def test_lead_gen_contains_conversion_mechanisms():
    seq = select_sequence("lead-gen-service")
    for mech in LEAD_GEN_MECHANISMS:
        assert mech in seq["conversion_mechanisms"], (
            "lead-gen must include conversion mechanism %r" % mech
        )


def test_brief_match_also_carries_full_sequence_and_mechanisms():
    """The brief path returns the same rich, complete sequence as the goal path."""
    seq = select_sequence("commercial skip hire quote near me, get a quote")
    assert seq["id"] == "lead-gen-service"
    assert _sections(seq) == LEAD_GEN_ORDER
    for mech in LEAD_GEN_MECHANISMS:
        assert mech in seq["conversion_mechanisms"]


def test_select_is_deterministic():
    a = select_sequence("commercial skip hire quote")
    b = select_sequence("commercial skip hire quote")
    assert a is not None and a["id"] == b["id"]


def test_keyword_list_query_supported():
    seq = select_sequence(["skip hire", "quote", "coverage area"])
    assert seq is not None and seq["id"] == "lead-gen-service"


def test_saas_brief_routes_to_saas():
    seq = select_sequence("a SaaS platform marketing site with a free trial")
    assert seq is not None and seq["id"] == "saas-marketing"


def test_no_signal_returns_none():
    """An empty or signal-free query yields no opinion rather than a wrong guess."""
    assert select_sequence("") is None
    assert select_sequence(None) is None
    assert select_sequence("zzzz qqqq xxxx") is None


def test_exact_goal_outscores_incidental_keyword_overlap():
    """Exact goal match must dominate so routing is stable."""
    entries = load_sequences()
    lead = next(e for e in entries if e["id"] == "lead-gen-service")
    tokens = {"lead-gen-service"}
    # goal token present -> strong base score
    assert score_sequence(lead, tokens, "lead-gen-service") >= 100
