"""The release checks in scripts/release_checks.py, run as tests: 600 sampled
briefs build, every gallery and fixture system round-trips through DTCG,
CSS, Tailwind and Figma with no mismatch, a build's digest is the same under
several PYTHONHASHSEED values, and the wheel ships engine/io and
engine/foundations and nothing private."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("release_checks",
                                               ROOT / "scripts" / "release_checks.py")
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)

BRIEFS = rc.sample_briefs()
CHUNK = 50


def test_the_sample_is_600_briefs_from_a_fixed_seed():
    assert len(BRIEFS) == rc.SAMPLES == 600
    assert BRIEFS == rc.sample_briefs()
    assert len({b for b, _ in BRIEFS}) > 590


@pytest.mark.parametrize("start", range(0, rc.SAMPLES, CHUNK))
def test_every_sampled_brief_builds(start):
    assert rc.check_briefs(BRIEFS[start:start + CHUNK]) == []


@pytest.mark.parametrize("label,ts", rc.systems(), ids=lambda x: x if isinstance(x, str) else "")
def test_every_system_round_trips_through_every_format(label, ts):
    problems, counts = rc.round_trip(label, ts)
    assert problems == []
    assert all(n > 1000 for n in counts.values()), counts


def test_a_mismatch_is_named():
    from engine.foundations.tokens import Token
    label, ts = rc.systems()[0]
    from engine.foundations import build_system
    from engine.synthesizer.axes import AxisValues
    other = build_system(AxisValues(*[0.5] * 7), "#3366FF").tokens
    del other._tokens["space.4"]
    other.add(Token("space.4", "dimension", {"value": 99, "unit": "px"}))
    problems, _ = rc._compare("fixture", "dtcg", ts, other)
    hit = [p for p in problems if p.startswith("fixture dtcg: space.4 ")]
    assert hit and "wrote 16.0 and read back 99.0" in hit[0]


def test_the_build_digest_is_stable_across_hash_seeds():
    assert rc.check_digest() == []


def test_the_wheel_rules_name_what_is_missing_and_what_is_private():
    problems = rc.check_wheel_names(["engine/io/read.py", "PLAN-4.0.md", "engine/x.pyc"])
    assert any("engine/foundations/" in p for p in problems)
    assert any("PLAN-4.0.md" in p for p in problems) and any(".pyc" in p for p in problems)
    assert rc.check_wheel_names(["engine/io/read.py", "engine/foundations/build.py"]) == []


def test_the_built_wheel_ships_the_engine_and_nothing_private():
    try:
        problems = rc.check_wheel()
    except RuntimeError as exc:
        if "No module named" in str(exc) or "setuptools" in str(exc):
            pytest.skip(str(exc)[:200])
        raise
    assert problems == []
