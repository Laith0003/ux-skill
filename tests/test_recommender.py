"""Recommender smoke tests — Brief → Recommendation roundtrip."""
from engine.recommender import recommend, Brief, Recommendation


def test_empty_brief_returns_recommendation():
    """A blank brief should still return a Recommendation object (engine never
    raises; it returns the best it can with the data on hand)."""
    rec = recommend(Brief())
    assert isinstance(rec, Recommendation)
    assert isinstance(rec.rationale, list)


def test_brief_dict_serialisable():
    rec = recommend(Brief(
        project_type="landing",
        tone=["warm", "editorial"],
        forbidden=["brutalism"],
    ))
    payload = rec.to_dict()
    assert "rationale" in payload
    assert "guardrails" in payload
    # Guardrails always come back — anti-patterns are always-on
    # (may be empty list if anti-patterns.json not yet populated)
    assert isinstance(payload["guardrails"], list)
