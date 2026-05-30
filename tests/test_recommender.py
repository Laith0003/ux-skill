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


def test_forbidden_typography_family_actually_excluded():
    """v2.2 regression — task #57.

    With ``cormorant`` in brief.forbidden, the type-pair lane MUST NOT return
    a pair whose display.family is Cormorant Garamond, even when that pair is
    listed in style.compatible_type_pairs.
    """
    rec = recommend(Brief(
        project_type="marketing-site",
        industry="saas-dev-tools",
        tone=["cinematic", "saturated"],
        forbidden=["cormorant", "cormorant-garamond"],
    ))
    tp = rec.type_pair or {}
    display_family = (tp.get("display") or {}).get("family") or ""
    assert "cormorant" not in display_family.lower(), (
        f"forbidden 'cormorant' leaked into type_pair.display.family: {display_family!r}"
    )


def test_forbidden_palette_actually_excluded():
    """v2.2 regression — task #57.

    A palette whose id or name contains a forbidden token MUST be skipped,
    even if it appears in style.compatible_palettes.
    """
    rec = recommend(Brief(
        project_type="marketing-site",
        industry="saas-dev-tools",
        tone=["dark"],
        forbidden=["graphite"],
    ))
    p = rec.palette or {}
    assert "graphite" not in (p.get("id") or "").lower()
    assert "graphite" not in (p.get("name") or "").lower()


def test_industry_fuzzy_match_does_not_return_unrelated():
    """v2.1 regression — task #53.

    A plausible-but-not-exact industry id should fuzzy-match within the
    same category, not bounce to score-all and return ``fintech-neobank``.
    """
    rec = recommend(Brief(
        industry="saas-dev-tools",
        tone=["precise"],
    ))
    # rationale[0] is "Industry: <name>" — make sure it's not the score-all fallback
    industry_line = rec.rationale[0] if rec.rationale else ""
    assert "fintech" not in industry_line.lower(), (
        f"Unknown-industry fallback returned an unrelated industry: {industry_line!r}"
    )


# --- Anti-slop palette guardrail (dogfood fix: forbidden=purple must work, and
# --- the engine must not DEFAULT to AI blurple). Both-direction tests.

def test_palette_slop_band_detection():
    from engine.recommender.core import _primary_in_slop_band
    assert _primary_in_slop_band({"colors": {"primary": "#5e6ad2"}}) is True   # blurple
    assert _primary_in_slop_band({"colors": {"primary": "#cc785c"}}) is False  # clay
    assert _primary_in_slop_band({"colors": {"primary": "#0a0b0d"}}) is False  # near-black


def test_palette_color_penalty_default_deprioritizes_blurple():
    from engine.recommender.core import _palette_color_penalty
    assert _palette_color_penalty({"colors": {"primary": "#5e6ad2"}}, Brief()) == -8.0


def test_palette_color_penalty_forbidden_purple_excludes_blurple():
    from engine.recommender.core import _palette_color_penalty
    p = _palette_color_penalty(
        {"colors": {"primary": "#5e6ad2"}},
        Brief(forbidden=["purple", "purple-gradients"]),
    )
    assert p == -100.0


def test_palette_color_penalty_leaves_non_slop_alone():
    from engine.recommender.core import _palette_color_penalty
    assert _palette_color_penalty(
        {"colors": {"primary": "#cc785c"}}, Brief(forbidden=["purple"])
    ) == 0.0


def test_recommend_forbidding_purple_avoids_blurple_primary():
    from engine.recommender.core import _primary_in_slop_band
    rec = recommend(Brief(industry="construction-pm",
                          forbidden=["purple", "purple-gradients", "inter"]))
    assert rec.palette is not None
    assert not _primary_in_slop_band(rec.palette), \
        "recommender returned a blue-violet primary despite forbidden=purple"
