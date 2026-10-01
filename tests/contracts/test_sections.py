"""Section contracts: a section's job, its slots (which take component
contracts or media), variants named by what differs, a proof requirement
that drops the section with its reason, and a phone recomposition in a
fixed order. Every seed validates and binds to a built system."""
import pytest

from engine.contracts import validate_contracts
from engine.contracts.library import seed_contracts, seed_sections
from engine.contracts.schema import PHONE_ORDER, ContractError, read_contract
from engine.foundations import build_system
from engine.page_sequence.core import PROOF_KINDS
from engine.synthesizer.axes import AxisValues

NAMES = ("bento", "comparison", "cta-band", "faq", "feature-grid", "footer", "hero",
         "how-it-works", "integrations", "logo-row", "named-quote", "pricing",
         "secondary-hero", "stats-band")
SECTIONS = {c.name: c for c in seed_sections()}
COMPONENTS = {c.name for c in seed_contracts()}

BASE = """\
name: proof-row
status: experimental
category: section
description: A row of proof under the hero.
job: Prove that real customers use the product, with their names.
parts:
  - {name: container, rtlBehavior: logical}
  - {name: heading, rtlBehavior: logical}
  - {name: item, rtlBehavior: logical}
slots:
  - {name: item, takes: [card], required: true}
  - {name: media, takes: [photograph], required: true}
variants:
  - {name: density, values: [standard, compact], default: standard}
states: [default]
tokens:
  - {part: container, property: fill, role: color.surface.page}
  - {part: heading, property: font, role: type.text.section-title}
  - {part: heading, property: text, role: color.text.default}
  - {part: item, property: gap, role: space.group.gap}
contrast:
  - {fg: color.text.default, bg: color.surface.page, minimum: 4.5, criterion: "1.4.3"}
surfaces: [color.surface.page]
proof: {kinds: [testimonials], drop: "with no named customer quote the row is empty, so it drops"}
phone: [drop-decorative-layers, fold-side-columns, pair-small-items]
a11y: {target: none, label: localized, cue: none}
copy:
  default:
    - Name the customer and their role
usage:
  do: [Show real customers only]
  dont: [Do not invent a quote]
provenance:
  figma: {node: null, variantCount: null, lastVerified: null}
  drift: []
"""


def test_a_section_reads():
    c = read_contract(BASE, "proof-row.yaml")
    assert c.section.job.startswith("Prove")
    assert [s.name for s in c.section.slots] == ["item", "media"]
    assert c.section.proof_kinds == ("testimonials",) and "drops" in c.section.drop
    assert c.section.phone == ("drop-decorative-layers", "fold-side-columns", "pair-small-items")


@pytest.mark.parametrize("edit,field", [
    (lambda t: t.replace("job: Prove that real customers use the product, with their names.\n", ""),
     "job"),
    (lambda t: t.replace("takes: [card]", "takes: [carousel]"), "slots[0].takes"),
    (lambda t: t.replace("{name: density, values: [standard, compact]",
                         "{name: color, values: [standard, compact]"), "variants"),
    (lambda t: t.replace("kinds: [testimonials]", "kinds: [rumours]"), "proof.kinds"),
    (lambda t: t.replace("[drop-decorative-layers, fold-side-columns, pair-small-items]",
                         "[pair-small-items, fold-side-columns]"), "phone"),
    (lambda t: t.replace("takes: [photograph]", "takes: [interface-fragment]"), "slots"),
])
def test_each_section_field_is_checked_naming_the_field_and_the_fix(edit, field):
    with pytest.raises(ContractError) as exc:
        read_contract(edit(BASE), "proof-row.yaml")
    msg = str(exc.value)
    assert field in msg and ";" in msg


def test_a_component_may_not_carry_section_fields():
    text = (BASE.replace("category: section", "category: container")
            .replace("job: Prove that real customers use the product, with their names.\n",
                     ""))
    with pytest.raises(ContractError, match="slots"):
        read_contract(text, "proof-row.yaml")


def test_the_seed_sections_are_the_set():
    assert tuple(sorted(SECTIONS)) == NAMES
    assert all(c.category == "section" and c.status == "experimental" for c in SECTIONS.values())


@pytest.mark.parametrize("name", NAMES)
def test_each_seed_section_holds_what_a_section_must(name):
    c = SECTIONS[name]
    s = c.section
    assert s.job.endswith(".") and s.job.count(". ") == 0, "one sentence"
    assert {v.name for v in c.variants} <= {"media", "alignment", "density"}
    for slot in s.slots:
        for t in slot.takes:
            assert t in COMPONENTS or t in ("photograph", "interface-fragment", "text"), t
    assert set(s.proof_kinds) <= set(PROOF_KINDS)
    assert list(s.phone) == [p for p in PHONE_ORDER if p in s.phone]
    takes = {t for slot in s.slots for t in slot.takes}
    assert "interface-fragment" not in takes or "photograph" in takes


def test_faq_and_footer_wrap_their_components():
    assert any("faq-accordion" in s.takes for s in SECTIONS["faq"].section.slots)
    assert any("site-footer" in s.takes for s in SECTIONS["footer"].section.slots)


def test_pricing_turns_three_plans_into_a_switcher_on_a_phone():
    assert "plan-switcher" in SECTIONS["pricing"].section.phone
    assert "recommended" in " ".join(SECTIONS["pricing"].do).lower()


@pytest.mark.parametrize("brand", ["#3366FF", "#6B4423", "#FFD400"])
@pytest.mark.parametrize("arabic", [True, False])
def test_every_section_binds_to_a_built_system(brand, arabic):
    ts = build_system(AxisValues(0.3, 0.7, 0.4, 0.6, 0.5, 0.5, 0.5), brand, arabic=arabic).tokens
    assert validate_contracts(list(SECTIONS.values()), ts) == []


def test_the_schema_reads_the_page_sequences_proof_kinds():
    from engine.contracts.schema import PROOF_KINDS as SCHEMA_KINDS
    assert SCHEMA_KINDS == PROOF_KINDS


def test_the_landing_compositions_point_at_section_contracts():
    import re
    from pathlib import Path
    text = (Path(__file__).resolve().parents[2] / "references" / "surfaces" /
            "landing.md").read_text(encoding="utf-8")
    sec = text[text.index("## Compositions"):text.index("\n## ", text.index("## Compositions") + 1)]
    named = set(re.findall(r"`([a-z-]+)`", sec)) & set(SECTIONS)
    assert {"hero", "cta-band", "bento", "named-quote", "stats-band"} <= named
    assert not re.search(r"\b\d+ (?:and \d+ )?of the 12 columns\b", sec)
