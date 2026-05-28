"""Smoke tests — confirm the engine imports and the public surface is callable."""
from engine import __version__
from engine.data_loader import MANIFESTS, stats
from engine.discovery import FIELDS, DiscoveryState, is_complete, next_question, record


def test_version_string():
    assert __version__.startswith("2."), f"unexpected version: {__version__}"


def test_manifest_list_canonical():
    expected = {
        "styles", "palettes", "type-pairs", "components", "industries",
        "chart-types", "tech-stacks", "ux-guidelines", "motion-presets",
        "anti-patterns", "landing-patterns",
    }
    assert set(MANIFESTS) == expected


def test_stats_returns_dict():
    counts = stats()
    assert isinstance(counts, dict)
    assert "styles" in counts
    assert "brands" in counts


def test_discovery_has_ten_fields():
    assert len(FIELDS) == 10
    state = DiscoveryState()
    assert not is_complete(state)
    q = next_question(state)
    assert q is not None
    assert q["id"] == "project_type"


def test_discovery_completes_in_ten():
    state = DiscoveryState()
    for f in FIELDS:
        record(state, f["id"], "test")
    assert is_complete(state)
