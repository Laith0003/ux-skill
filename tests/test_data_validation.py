"""Validate every data manifest.

These tests are intentionally lenient on COUNTS (run before the data agents
finish), but strict on STRUCTURE — every present entry must conform.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from engine.data_loader import DATA_DIR, MANIFESTS, load, load_brands


KEBAB_CASE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@pytest.mark.parametrize("manifest", MANIFESTS)
def test_manifest_loads_and_has_meta(manifest):
    data = load(manifest)
    if data["_meta"].get("missing"):
        pytest.skip(f"{manifest}.json not yet generated")
    assert "entries" in data
    assert isinstance(data["entries"], list)


@pytest.mark.parametrize("manifest", MANIFESTS)
def test_entry_ids_unique_and_kebab(manifest):
    data = load(manifest)
    if data["_meta"].get("missing"):
        pytest.skip(f"{manifest}.json not yet generated")
    seen = set()
    for i, entry in enumerate(data["entries"]):
        eid = entry.get("id")
        assert eid, f"{manifest}[{i}] missing id"
        assert KEBAB_CASE.match(eid), f"{manifest}[{i}] id not kebab-case: {eid}"
        assert eid not in seen, f"{manifest} duplicate id: {eid}"
        seen.add(eid)


def test_brands_load():
    brands = load_brands()
    if not brands:
        pytest.skip("data/brands/ not yet populated")
    seen = set()
    for b in brands:
        bid = b.get("id")
        assert bid, f"brand missing id: {b}"
        assert bid not in seen, f"duplicate brand id: {bid}"
        seen.add(bid)


def test_phase_plan_exists():
    """The phase tracker doc must be present."""
    assert (DATA_DIR / "PHASE-PLAN.md").exists()


def test_schemas_exists():
    """The schema doc must be present."""
    assert (DATA_DIR / "SCHEMAS.md").exists()
