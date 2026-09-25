"""The decision records that ship with the engine: all valid, routed by
HISTORY.md, one per design choice a designer could question."""
import re
from pathlib import Path

from engine.rulepack.records import AREAS, RECORDS_DIR, check_folder, load_records

ROOT = Path(__file__).resolve().parents[2]

# The choices the foundations engine makes on purpose, each with its record.
EXPECTED = {
    "two-layers", "axes-on-the-root", "breakpoints-are-reference-values", "two-density-modes",
    "color-roles", "space-roles", "radius-roles", "border-roles", "elevation-roles",
    "motion-roles", "layout-scope", "type-roles",
    "high-contrast-non-text-floor", "aaa-criteria-that-block", "no-large-text-relaxation",
    "ring-offset", "fill-edge-page-only", "ring-on-tinted-fills", "disabled-contrast",
    "status-hues", "dark-elevation-cue", "whole-pixel-borders", "nested-radius",
    "list-gap-and-control-gap", "unsigned-distances", "strong-equals-heading-weight",
    "reading-line-height", "container-edge", "button-intents",
    "status-harmony", "neutral-tint", "recessed-sunken", "high-contrast-surfaces", "error-edge",
    "brand-fidelity", "primary-edge", "ring-never-weaker",
    "brand-roles", "brand-surfaces", "support-accent", "logo-and-decoration",
    "code-and-table-colors", "roundness", "high-contrast-borders", "surface-treatment",
    "type-three-faces", "face-choice", "type-along-the-scale", "arabic-proportional",
    "high-contrast-weights", "strong-weight", "font-loading", "page-regions",
    "field-and-table-spacing", "expressive-motion", "brief-fields", "default-scheme",
    "imagery-foundation", "generated-art", "page-composition", "distinctness",
    "readable-fields", "button-sizes", "card-and-banner-reading", "form-contracts",
    "display-and-navigation-contracts", "arabic-market-content", "scrim-worst-image",
    "controls-on-brand-surfaces", "warmth-through-grey", "grey-brands-steer-no-hue",
    "exact-fill-states", "ring-room", "brief-fields-checked", "font-files",
    "strong-under-high-contrast", "grey-brand-support-hue", "art-composition",
    "motion-check-owners", "space-relationship-roles", "page-regions-by-tier", "layout-aliases",
    "distinctness-at-a-glance", "grey-accent-clear-of-status", "form-contracts-per-control",
    "display-contracts-measured", "radius-roles-by-shape", "divider-edge",
    "tone-words-reach-shape", "sentence-names-the-shown-face", "type-steps-down-on-phones",
    "direction-on-any-subtree", "dark-recess-and-bands", "high-contrast-levels",
    "soft-fills-follow-character", "brand-fill-family", "media-veil", "dark-surfaces-rise",
    "type-levels-apart", "arabic-by-script", "brand-leads-the-role",
    "natural-text-on-the-brand", "neutrals-follow-the-brand", "support-clear-of-banned-pairs",
    "fills-on-every-placement", "distinctness-on-a-grey-reference",
    "eyebrow-is-text",
    "edge-weight-inside", "faq-and-footer-contracts", "existing-system-wins", "client-identity-wins",
    "brand-leads-by-reach", "natural-fill-for-white-text", "neutrals-lean-along-the-brand",
    "support-in-the-brand-family", "grey-support-is-neutral", "fills-on-every-control-surface",
    "links-on-status-soft-fills", "distinctness-on-saturated-brands",
    "wider-vocabulary", "character-nudges", "faces-by-product-type", "landing-display-step",
    "figure-holds-a-number-band", "landing-gap", "surfaces-stand-apart", "clean-code-surface",
    "checks-read-one-unit", "roles-on-their-scale", "spacing-on-the-4px-grid", "unresolved-pairing",
    "layout-bounds", "reflow-at-320", "spacing-within-group", "strict-radius-nesting",
    "the-full-type-ladder", "imported-sets-pass", "phone-order-in-both-scripts",
}
# Records a later record replaced; each names its replacement.
SUPERSEDED = {"status-hues": "status-harmony", "fill-edge-page-only": "primary-edge",
              "type-roles": "type-three-faces", "strong-equals-heading-weight": "strong-weight",
              "strong-weight": "strong-under-high-contrast",
              "layout-scope": "page-regions", "neutral-tint": "warmth-through-grey",
              "font-loading": "font-files", "generated-art": "art-composition",
              "expressive-motion": "motion-check-owners",
              "space-roles": "space-relationship-roles", "page-regions": "page-regions-by-tier",
              "breakpoints-are-reference-values": "layout-aliases",
              "distinctness": "distinctness-at-a-glance",
              "grey-brand-support-hue": "grey-accent-clear-of-status",
              "form-contracts": "form-contracts-per-control",
              "display-and-navigation-contracts": "display-contracts-measured",
              "radius-roles": "radius-roles-by-shape",
              "layout-aliases": "type-steps-down-on-phones",
              "axes-on-the-root": "direction-on-any-subtree",
              "recessed-sunken": "dark-recess-and-bands",
              "high-contrast-surfaces": "high-contrast-levels",
              "brand-fidelity": "brand-fill-family",
              "dark-elevation-cue": "dark-surfaces-rise",
              "brand-roles": "brand-leads-the-role",
              "brand-fill-family": "natural-text-on-the-brand",
              "warmth-through-grey": "neutrals-follow-the-brand",
              "support-accent": "support-clear-of-banned-pairs",
              "primary-edge": "fills-on-every-placement",
              "distinctness-at-a-glance": "distinctness-on-a-grey-reference",
              "brand-leads-the-role": "brand-leads-by-reach",
              "natural-text-on-the-brand": "natural-fill-for-white-text",
              "neutrals-follow-the-brand": "neutrals-lean-along-the-brand",
              "support-clear-of-banned-pairs": "support-in-the-brand-family",
              "grey-accent-clear-of-status": "grey-support-is-neutral",
              "fills-on-every-placement": "fills-on-every-control-surface",
              "distinctness-on-a-grey-reference": "distinctness-on-saturated-brands",
              "face-choice": "faces-by-product-type",
              "type-steps-down-on-phones": "landing-display-step",
              "brand-surfaces": "surfaces-stand-apart",
              "code-and-table-colors": "clean-code-surface",
              "nested-radius": "strict-radius-nesting"}


def test_every_shipped_record_is_valid_and_routed():
    records, problems = check_folder()
    assert problems == []
    assert {r.id for r in records} == EXPECTED
    assert {r.id: r.superseded_by for r in records if r.status == "superseded"} == SUPERSEDED


def test_every_foundation_has_a_record_for_its_roles():
    ids = {r.id for r in load_records()}
    for foundation in ("color", "space", "radius", "border", "elevation", "motion"):
        assert f"{foundation}-roles" in ids, foundation
    assert "type-three-faces" in ids
    assert "page-regions" in ids


def test_every_area_a_record_names_is_known_and_each_foundation_is_covered():
    areas = {a for r in load_records() for a in r.areas}
    assert areas <= set(AREAS)
    assert {"color", "space", "radius", "border", "elevation", "motion", "layout",
            "type"} <= areas


def test_records_cite_wcag_only_by_criteria_that_exist_here():
    cited = set()
    for r in load_records():
        cited |= set(re.findall(r"\b([1-4]\.\d\.\d{1,2})\b", r.text))
    assert cited <= {"1.4.1", "1.4.3", "1.4.6", "1.4.8", "1.4.10", "1.4.11", "2.3.3", "2.4.7",
                     "2.5.5", "2.5.8"}, cited


def test_decision_records_ship_with_the_package():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'"engine\.rulepack" = \["decisions/\*\.md"', pyproject)
    assert (RECORDS_DIR / "HISTORY.md").exists()
