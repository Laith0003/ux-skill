"""Milestone 2 gate: build_system builds all eight foundations into one
set that validates, passes the gate in every context, round-trips through
DTCG and matches the full golden output byte for byte."""
import json
from pathlib import Path

import pytest

from engine.foundations import (
    FOUNDATIONS, build_system, dump_dtcg, from_dtcg, run_validate, to_css, to_dtcg)
from engine.foundations.modes import FOUNDATION_AXES, parse
from engine.synthesizer.axes import AxisValues
from tests.foundations.golden.capture_system import CASES, render

GOLDEN = Path(__file__).resolve().parent / "golden"
MID = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
EIGHT = ("color", "space", "radius", "border", "elevation", "motion", "layout", "type",
         "imagery")


def _rule_body(css, selector):
    """The declarations of the first rule whose selector line is exactly
    selector, or None when the CSS has no such rule."""
    lines = css.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == selector + " {":
            body = []
            for inner in lines[i + 1:]:
                if inner.strip() == "}":
                    return body
                body.append(inner.strip())
    return None


def test_all_eight_foundations_build_in_order():
    assert tuple(f.name for f in FOUNDATIONS) == EIGHT
    result = build_system(MID, "#3366FF")
    roots = []
    for t in result.tokens.tokens():
        root = t.path.split(".", 1)[0]
        if root not in roots:
            roots.append(root)
    assert tuple(roots) == EIGHT
    report = result.report
    assert report.passed and report.findings == [] and report.failures == []
    assert report.skipped_pairings == [] and report.checked > 0 and report.rules_checked > 0


@pytest.mark.parametrize("name", sorted(CASES))
def test_every_golden_case_passes_the_gate_with_nothing_skipped(name):
    seed, axes, arabic = CASES[name]
    report = build_system(axes, seed, arabic=arabic).report
    assert report.passed, report.summary()
    assert report.skipped_pairings == [], report.skipped_message()


def test_every_token_varies_only_on_its_foundation_axes():
    ts = build_system(MID, "#3366FF").tokens
    for t in ts.tokens():
        allowed = FOUNDATION_AXES[t.path.split(".", 1)[0]]
        for key in t.modes:
            assert set(parse(key)) <= set(allowed), (t.path, key)


def test_every_axis_reaches_the_css():
    css = to_css(build_system(MID, "#3366FF").tokens)
    for selector in ('[data-theme="dark"]', '[data-contrast="high"]', '[data-density="compact"]',
                     '[dir="rtl"]', '[data-motion="reduced"]', "(prefers-color-scheme: dark)",
                     "(prefers-contrast: more)", "(prefers-reduced-motion: reduce)"):
        assert selector in css, selector


def test_the_whole_system_round_trips_through_dtcg():
    ts = build_system(MID, "#E61428").tokens
    doc = json.loads(dump_dtcg(ts))
    back = from_dtcg(doc)
    assert run_validate(back) == []
    assert to_dtcg(back) == doc and to_css(back) == to_css(ts)


def test_arabic_off_builds_a_latin_only_system():
    ts = build_system(MID, "#3366FF", arabic=False).tokens
    assert not ts.has("type.face.arabic")
    assert not any(t.path.startswith(("type.size.arabic.", "type.leading.arabic."))
                   for t in ts.tokens())
    assert not any("direction:rtl" in k for t in ts.tokens() if t.path.startswith("type.")
                   for k in t.modes)


@pytest.mark.parametrize("name", sorted(CASES))
def test_full_output_matches_the_golden(name):
    css, dtcg = render(*CASES[name])
    assert css == (GOLDEN / f"system-{name}.css").read_text(encoding="utf-8")
    assert dtcg == (GOLDEN / f"system-{name}.json").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", sorted(CASES))
def test_every_golden_css_carries_the_high_contrast_and_reduced_motion_blocks(name):
    css = (GOLDEN / f"system-{name}.css").read_text(encoding="utf-8")
    for selector in (':root[data-contrast="high"]',
                     ':root:not([data-contrast="standard"])',
                     ':root[data-motion="reduced"]',
                     ':root:not([data-motion="standard"])'):
        body = _rule_body(css, selector)
        assert body, f"{name}: no declarations under {selector}"
    assert "@media (prefers-contrast: more) {" in css
    assert "@media (prefers-reduced-motion: reduce) {" in css


def test_latin_golden_has_no_arabic_type():
    seed, axes, arabic = CASES["3366ff-latin"]
    assert arabic is False
    css = (GOLDEN / "system-3366ff-latin.css").read_text(encoding="utf-8")
    dtcg = (GOLDEN / "system-3366ff-latin.json").read_text(encoding="utf-8")
    assert "arabic" not in css.lower() and "arabic" not in dtcg.lower()
    rtl = _rule_body(css, ':root[dir="rtl"]') or []
    assert not [line for line in rtl if line.startswith("--type-")], rtl
    arabic_rtl = _rule_body((GOLDEN / "system-3366ff.css").read_text(encoding="utf-8"),
                            ':root[dir="rtl"]')
    assert any(line.startswith("--type-") for line in arabic_rtl)
