"""Every section of every page sequence names its section contract, or is
marked prose-only, and the contract agrees with the sequence on proof."""
import pytest

from engine.contracts.library import seed_sections
from engine.page_sequence import load_sequences, select_for_brief

SECTIONS = {c.name: c for c in seed_sections()}
ROWS = [(e["id"], s) for e in load_sequences() for s in e["section_sequence"]]


@pytest.mark.parametrize("sid,section", ROWS, ids=[f"{i}:{s['section'][:30]}" for i, s in ROWS])
def test_every_sequence_section_resolves(sid, section):
    has_contract = "contract" in section
    assert has_contract != bool(section.get("prose_only")), (
        f"{sid}: {section['section']} names a contract or is prose_only, exactly one")
    if has_contract:
        assert section["contract"] in SECTIONS, (sid, section["contract"])


@pytest.mark.parametrize("sid,section", [(i, s) for i, s in ROWS if s.get("proof")])
def test_a_proof_section_uses_a_contract_that_needs_that_proof(sid, section):
    if "contract" in section:
        assert section["proof"] in SECTIONS[section["contract"]].section.proof_kinds, (
            sid, section["section"], section["proof"])


def test_a_dropped_section_gives_its_contracts_reason():
    seq = select_for_brief({"product_type": "software", "proof": []})
    reasons = [d["reason"] for d in seq["dropped"] if "section" in d]
    assert reasons
    contracts = {s["section"]: s.get("contract") for e in load_sequences()
                 for s in e["section_sequence"]}
    for d in seq["dropped"]:
        name = contracts.get(d.get("section"))
        if name and SECTIONS[name].section.drop != "none":
            assert SECTIONS[name].section.drop in d["reason"]


def test_the_split_rows_stay_prose_only_with_their_rule():
    rows = [s for _, s in ROWS if s["section"].startswith("Split feature rows")]
    assert rows and all(s.get("prose_only") for s in rows)


@pytest.mark.parametrize("sid,section", [(i, s) for i, s in ROWS if s.get("contract")])
def test_a_section_whose_contract_needs_proof_names_its_proof(sid, section):
    if SECTIONS[section["contract"]].section.proof_kinds:
        assert section.get("proof"), (sid, section["section"])


def test_a_section_keeps_its_place_with_another_proof_its_contract_takes():
    seq = select_for_brief({"product_type": "software", "proof": ["reviews"]})
    quotes = [s for s in seq["section_sequence"] if s.get("contract") == "named-quote"]
    assert quotes and all(s["proof"] == "reviews" for s in quotes)
