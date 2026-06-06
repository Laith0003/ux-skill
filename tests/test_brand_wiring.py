"""Brand wiring tests -- the extracted brand travels into the LIVE engine paths.

Covers the P2/P4/P7 wiring: recommend + synthesize honor an extracted brand, and
evaluate + evolve enforce it as a HARD FLOOR (off-brand drift fails regardless of
the design score). The no-brand path stays byte-identical to before (the existing
evaluator/recommender/synthesizer suites assert that -- they pass no brand).
"""
from engine.brand import build_profile
from engine.evaluator import evaluate
from engine.evolve.core import evolve
from engine.recommender.core import Brief, recommend
from engine.synthesizer.core import synthesize


def _profile():
    return build_profile({
        "logo_colors": [{"hex": "#f0890f"}],
        "logo": {"alt": "Instant Skip Hire logo"},
        "name": "Instant Skip Hire",
        "fonts": {"h1": '"Roboto Flex", system-ui'},
    })


_ON_BRAND = ('<!doctype html><html><body><header><a class="logo">Instant Skip Hire</a>'
             '</header><main style="background:#f0890f"><h1>Book a skip</h1>'
             '<img src="/yard.avif" alt="a commercial skip" width="800" height="600">'
             '</main></body></html>')
_OFF_BRAND = ('<!doctype html><html><body><main><h1 style="color:#cc785c">Skips</h1>'
              '<p>text only, house clay, no logo, no image</p></main></body></html>')


# --- evaluate(): brand fidelity reported + HARD FLOOR ---

def test_evaluate_on_brand_passes_floor():
    ev = evaluate(html=_ON_BRAND, brand_profile=_profile())
    assert ev.brand_fidelity >= 90
    assert ev.imagery == 100
    assert ev.brand_passed is True


def test_evaluate_off_brand_trips_hard_floor():
    """Clay + no logo + no imagery -> brand_passed False, above_threshold False."""
    ev = evaluate(html=_OFF_BRAND, brand_profile=_profile())
    assert ev.brand_passed is False
    assert ev.above_threshold is False          # floor overrides any composite
    assert ev.brand_fidelity < 50
    assert ev.imagery == 0
    assert any("BRAND FLOOR" in n for n in ev.notes)


def test_evaluate_accepts_profile_as_dict():
    """A brand profile passed as its to_dict() form behaves like the object."""
    p = _profile()
    a = evaluate(html=_OFF_BRAND, brand_profile=p)
    b = evaluate(html=_OFF_BRAND, brand_profile=p.to_dict())
    assert a.brand_passed is False and b.brand_passed is False


def test_evaluate_no_brand_is_unchanged_path():
    """No brand profile -> brand fields default, floor inert (back-compat)."""
    ev = evaluate(html=_OFF_BRAND)
    assert ev.brand_passed is True
    assert ev.brand_fidelity == 100 and ev.imagery == 100


# --- evolve(): floor honored at the accept gate ---

def test_evolve_off_brand_never_above_gate():
    res = evolve(_OFF_BRAND, "", brand_profile=_profile())
    assert res.above_gate is False
    assert res.stopped_reason == "gate_failed"


# --- recommend(): brand anchor overrides the palette pick ---

def test_recommend_brand_anchor_overrides_palette():
    rec = recommend(Brief(project_type="landing", tone=["bold"], brand=_profile().to_dict()))
    assert (rec.palette or {}).get("colors", {}).get("primary") == "#f0890f"
    assert (rec.brand or {}).get("name") == "Instant Skip Hire"
    assert (rec.type_directive or {}).get("reject_defaults") is True


def test_recommend_brand_url_without_capture_warns():
    """A site/brand URL supplied but no brand captured -> LOUD warning, never a
    silent brand:None (the dogfood failure mode rebuilt as an enforced guard)."""
    rec = recommend(Brief(project_type="landing", tone=["bold"],
                          brand_url="https://example.com"))
    assert rec.brand is None
    assert any("no brand was captured" in w.lower() for w in rec.warnings)
    assert any(w.startswith("WARNING:") for w in rec.rationale)


def test_recommend_brand_url_with_capture_no_warning():
    """URL supplied AND brand captured -> anchored, no capture warning."""
    rec = recommend(Brief(project_type="landing", tone=["bold"],
                          brand_url="https://example.com", brand=_profile().to_dict()))
    assert (rec.brand or {}).get("name") == "Instant Skip Hire"
    assert not any("no brand was captured" in w.lower() for w in rec.warnings)


def test_recommend_no_brand_url_no_capture_warning():
    """No URL -> no capture warning, warnings stays empty (back-compat)."""
    rec = recommend(Brief(project_type="landing", tone=["bold"]))
    assert rec.brand is None
    assert rec.warnings == []


def test_recommend_no_brand_leaves_fields_none():
    rec = recommend(Brief(project_type="landing", tone=["bold"]))
    assert rec.brand is None and rec.type_directive is None


# --- synthesize(): brand stamp overrides the synthesized palette ---

def test_synthesize_stamps_client_brand():
    sy = synthesize(Brief(project_type="landing", tone=["bold"], brand=_profile().to_dict()))
    assert sy.palette.get("primary") == "#f0890f"
    assert sy.palette.get("accent") == "#f0890f"


def test_brand_wired_paths_are_deterministic():
    p = _profile()
    b = Brief(project_type="landing", tone=["bold"], brand=p.to_dict())
    assert recommend(b).to_dict() == recommend(b).to_dict()
    assert synthesize(b).to_dict() == synthesize(b).to_dict()
    assert (evaluate(html=_ON_BRAND, brand_profile=p).to_dict()
            == evaluate(html=_ON_BRAND, brand_profile=p).to_dict())
