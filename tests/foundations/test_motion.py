"""Motion: pace and curves from the motion axis, a reduced-motion variant
that keeps meaning and drops travel, and a sign mirrored under rtl."""
import pytest

from engine.foundations import build_system, from_dtcg, to_css, to_dtcg
from engine.foundations.foundation import role_types_check
from engine.foundations.gate import gate
from engine.foundations.motion import (
    CHECKS, CURVES, FOUNDATION, GENTLE, LINEAR, ROLES, band, distance_unit, duration_ms, generate_motion)
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(motion=0.5, **kw):
    values = dict(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5, formality=0.5,
                  motion=motion, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


@pytest.mark.parametrize("motion, want", [
    (0.0, {"motion.press": 100, "motion.reveal": 150, "motion.dismiss": 100, "motion.swap": 150,
           "motion.expand": 200, "motion.page": 250, "motion.progress": 1200}),
    (0.5, {"motion.press": 100, "motion.reveal": 250, "motion.dismiss": 150, "motion.swap": 200,
           "motion.expand": 250, "motion.page": 400, "motion.progress": 1200}),
    (1.0, {"motion.press": 100, "motion.reveal": 300, "motion.dismiss": 200, "motion.swap": 250,
           "motion.expand": 300, "motion.page": 500, "motion.progress": 800}),
])
def test_durations_follow_the_motion_axis(motion, want):
    assert {r: duration_ms(r, motion) for r in ROLES} == want
    ts = generate_motion(axes(motion)).tokens
    assert {r: ts.resolve(f"{r}.duration")["value"] for r in ROLES} == want


def test_curves_and_travel_follow_the_motion_axis():
    assert [band(m) for m in (0.0, 0.33, 0.34, 0.65, 0.66, 1.0)] == [
        "calm", "calm", "balanced", "balanced", "lively", "lively"]
    assert [distance_unit(m) for m in (0.0, 0.5, 1.0)] == [4, 6, 8]
    ts = generate_motion(axes(1.0)).tokens
    assert ts.resolve("motion.reveal.curve") == CURVES["lively"][0]
    assert ts.resolve("motion.page.distance") == {"value": 16, "unit": "px"}


@pytest.mark.parametrize("motion", [i / 10 for i in range(11)])
def test_reduced_motion_keeps_meaning_and_drops_travel(motion):
    ts = generate_motion(axes(motion)).tokens
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed
    for role in ROLES:
        reduced = ts.resolve(f"{role}.duration", "motion:reduced")["value"]
        standard = ts.resolve(f"{role}.duration")["value"]
        if role == "motion.progress":
            assert reduced == standard
        else:
            assert 0 < reduced <= 100 and reduced <= standard
            assert ts.resolve(f"{role}.curve", "motion:reduced") == GENTLE
        if ts.has(f"{role}.distance"):
            assert ts.resolve(f"{role}.distance", "motion:reduced")["value"] == 0
    assert ts.resolve("motion.progress.curve", "motion:reduced") == LINEAR


def test_inline_sign_mirrors_under_rtl():
    ts = generate_motion(axes()).tokens
    assert ts.resolve("motion.inline-sign", "direction:ltr") == 1
    assert ts.resolve("motion.inline-sign", "direction:rtl") == -1


def test_checks_name_the_token_and_the_fix():
    ts = TokenSet()
    ts.add(Token("motion.d.a", "duration", {"value": 300, "unit": "ms"}))
    ts.add(Token("motion.d.b", "duration", {"value": 0.2, "unit": "s"}))
    ts.add(Token("motion.x.a", "dimension", {"value": 12, "unit": "px"}))
    ts.add(Token("motion.c.a", "cubicBezier", [0.34, 1.56, 0.64, 1]))
    ts.add(Token("motion.n.a", "number", 1))
    ts.add(Token("motion.reveal.duration", "duration", "{motion.d.b}", layer="semantic"))
    ts.add(Token("motion.dismiss.duration", "duration", "{motion.d.a}", layer="semantic"))
    ts.add(Token("motion.dismiss.distance", "dimension", "{motion.x.a}", layer="semantic"))
    ts.add(Token("motion.dismiss.curve", "cubicBezier", "{motion.c.a}", layer="semantic"))
    ts.add(Token("motion.progress.curve", "cubicBezier", "{motion.c.a}", layer="semantic"))
    ts.add(Token("motion.inline-sign", "number", "{motion.n.a}", layer="semantic"))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "motion.dismiss.distance travels 12px under reduced motion; point its motion:reduced "
        "override at motion.distance.0",
        "motion.reveal.duration lasts 200ms under reduced motion; cap it at 100ms with a "
        "motion:reduced override",
        "motion.dismiss.duration lasts 300ms under reduced motion; cap it at 100ms with a "
        "motion:reduced override",
        "motion.dismiss.curve overshoots under reduced motion; point its motion:reduced override "
        "at motion.curve.gentle",
        "motion.progress.curve overshoots under reduced motion; point its motion:reduced override "
        "at motion.curve.gentle",
        "motion.dismiss.duration (300ms) is not shorter than motion.reveal.duration (200ms); "
        "leaving should never hold the next action longer than arriving, so shorten it",
        "motion.progress.curve is [0.34, 1.56, 0.64, 1]; a continuous loop must keep an even "
        "pace, so point it at motion.curve.linear",
        "motion.inline-sign (direction:rtl) is 1; horizontal travel follows the reading "
        "direction, so it must be -1 here"]


def test_only_motion_moves_motion():
    base = [(t.path, t.value, t.modes) for t in generate_motion(axes()).tokens.tokens()]
    other = axes(warmth=0.0, contrast=1.0, density=1.0, geometry=0.0, formality=1.0,
                 type_personality=0.0)
    assert [(t.path, t.value, t.modes) for t in generate_motion(other).tokens.tokens()] == base


def test_dtcg_round_trip_and_css_for_reduced_motion_and_rtl():
    ts = generate_motion(axes()).tokens
    doc = to_dtcg(ts)
    assert doc["motion"]["duration"]["150"]["$value"] == {"value": 150, "unit": "ms"}
    assert doc["motion"]["curve"]["linear"]["$value"] == [0, 0, 1, 1]
    assert to_dtcg(from_dtcg(doc)) == doc
    css = to_css(build_system(axes(), "#3366FF").tokens)
    assert "  --motion-curve-in-out: cubic-bezier(0.65, 0, 0.35, 1);" in css
    assert '@media (prefers-reduced-motion: reduce) {\n  :root:not([data-motion="standard"]) {' in css
    assert ':root[data-motion="reduced"] {' in css
    assert ':root[dir="rtl"] {\n  --motion-inline-sign: var(--motion-sign-backward);' in css


def _roles_set(**roles):
    """Motion primitives plus the given semantic roles: path -> (type, alias, modes)."""
    ts = TokenSet()
    ts.add(Token("motion.d.fast", "duration", {"value": 100, "unit": "ms"}))
    ts.add(Token("motion.d.slow", "duration", {"value": 1200, "unit": "ms"}))
    ts.add(Token("motion.c.linear", "cubicBezier", [0, 0, 1, 1]))
    ts.add(Token("motion.c.gentle", "cubicBezier", [0.4, 0, 0.6, 1]))
    ts.add(Token("motion.x.a", "dimension", {"value": 0.5, "unit": "rem"}))
    ts.add(Token("motion.x.zero", "dimension", {"value": 0, "unit": "rem"}))
    ts.add(Token("motion.n.a", "number", 150))
    ts.add(Token("motion.s.a", "strokeStyle", "solid"))
    for path, (type_, alias, modes) in roles.items():
        ts.add(Token(path.replace("__", ".").replace("_", "-"), type_, alias, modes=modes,
                     layer="semantic"))
    return ts


def test_a_role_of_the_wrong_type_is_a_finding_not_a_crash():
    ts = _roles_set(motion__press__duration=("number", "{motion.n.a}", {}),
                    motion__reveal__curve=("dimension", "{motion.x.a}", {}),
                    motion__inline_sign=("strokeStyle", "{motion.s.a}", {}))
    assert validate(ts) == []
    report = gate(ts, [], (role_types_check([FOUNDATION]),) + CHECKS, raise_on_fail=False)
    assert [(f.check, f.message) for f in report.failures] == [
        ("role-types", "motion.press.duration is a number but its role expects a duration; "
         "point it at a duration token, for example {value: 200, unit: ms}"),
        ("role-types", "motion.reveal.curve is a dimension but its role expects a cubicBezier; "
         "point it at a cubicBezier token, for example [0.4, 0, 0.6, 1]"),
        ("role-types", "motion.inline-sign is a strokeStyle but its role expects a number; "
         "point it at a number token")]


@pytest.mark.parametrize("roles, want", [
    ({"motion__progress__duration": ("duration", "{motion.d.slow}",
                                     {"motion:reduced": "{motion.d.fast}"})},
     "motion.progress.duration lasts 100ms under reduced motion but 1200ms in standard; a "
     "status loop keeps its pace, so drop its motion:reduced override"),
    ({"motion__progress__curve": ("cubicBezier", "{motion.c.linear}",
                                  {"motion:reduced": "{motion.c.gentle}"})},
     "motion.progress.curve is [0.4, 0, 0.6, 1] under reduced motion; a status loop keeps an "
     "even pace, so drop its motion:reduced override and keep motion.curve.linear"),
])
def test_reduced_progress_keeps_its_pace(roles, want):
    ts = _roles_set(**roles)
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("progress-keeps-pace", "system", "motion:reduced", want)]


def test_only_travel_removal_cites_wcag_and_distances_keep_their_unit():
    assert {c.id: c.criterion for c in CHECKS} == {
        "reduced-travel": "2.3.3", "reduced-length": "system",
        "reduced-curve": "system", "dismiss-faster": "system", "progress-linear": "system",
        "progress-keeps-pace": "system", "mirrored-motion": "system"}
    ts = _roles_set(motion__reveal__distance=("dimension", "{motion.x.a}", {}))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.message) for f in report.failures] == [
        ("reduced-travel", "2.3.3", "motion.reveal.distance travels 0.5rem under reduced motion; "
         "point its motion:reduced override at motion.distance.0")]
