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
    "high-contrast-weights", "strong-weight",
}
# Records a later record replaced; each names its replacement.
SUPERSEDED = {"status-hues": "status-harmony", "fill-edge-page-only": "primary-edge",
              "type-roles": "type-three-faces", "strong-equals-heading-weight": "strong-weight"}


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
    assert "layout-scope" in ids


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
