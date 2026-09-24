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
        "progress-keeps-pace": "system", "mirrored-motion": "system",
        "press-in-place": "system", "linear-progress-only": "system",
        "reduced-not-longer": "system", "progress-floor": "system"}
    ts = _roles_set(motion__reveal__distance=("dimension", "{motion.x.a}", {}))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.message) for f in report.failures] == [
        ("reduced-travel", "2.3.3", "motion.reveal.distance travels 0.5rem under reduced motion; "
         "point its motion:reduced override at motion.distance.0")]


def _press_set(**roles):
    ts = _roles_set(**roles)
    ts.add(Token("motion.x.four", "dimension", {"value": 4, "unit": "px"}))
    return ts


def test_a_press_never_travels_in_any_context():
    # A base travel is this check's finding in every context; under reduced
    # motion the reduced-travel check already names it, so it is not repeated.
    ts = _press_set(motion__press__distance=("dimension", "{motion.x.four}", {}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("reduced-travel", "2.3.3", "motion:reduced",
         "motion.press.distance travels 4px under reduced motion; point its motion:reduced "
         "override at motion.distance.0"),
        ("press-in-place", "system", "direction:ltr,motion:standard",
         "motion.press.distance travels 4px; a press confirms in place, so point it at "
         "motion.distance.0")]

    # Travel only under rtl, and a press travel token outside the roles.
    ts = _press_set(motion__press__distance=("dimension", "{motion.x.zero}",
                                             {"direction:rtl": "{motion.x.four}"}),
                    motion__press__travel=("dimension", "{motion.x.a}", {}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures
            if f.check == "press-in-place"] == [
        ("press-in-place", "direction:ltr,motion:standard",
         "motion.press.travel travels 0.5rem; a press confirms in place, so point it at "
         "motion.distance.0"),
        ("press-in-place", "direction:rtl,motion:standard",
         "motion.press.distance travels 4px under direction:rtl; a press confirms in place, so "
         "point its direction:rtl override at motion.distance.0")]


def test_linear_belongs_to_the_progress_loop_alone():
    ts = _roles_set(motion__progress__curve=("cubicBezier", "{motion.c.linear}", {}),
                    motion__reveal__curve=("cubicBezier", "{motion.c.linear}",
                                           {"motion:reduced": "{motion.c.gentle}"}),
                    motion__swap__curve=("cubicBezier", "{motion.c.gentle}",
                                         {"motion:reduced": "{motion.c.even}"}))
    ts.add(Token("motion.c.even", "cubicBezier", [0.3, 0.3, 0.7, 0.7]))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("linear-progress-only", "system", "direction:ltr,motion:standard",
         "motion.reveal.curve is linear; only motion.progress.curve loops, and a one-shot move "
         "at an even pace reads mechanical, so point it at an eased curve such as "
         "motion.curve.out"),
        ("linear-progress-only", "system", "direction:ltr,motion:reduced",
         "motion.swap.curve is linear under motion:reduced; only motion.progress.curve loops, "
         "and a one-shot move at an even pace reads mechanical, so point its motion:reduced "
         "override at motion.curve.gentle")]


def test_reduced_motion_never_lengthens_a_role():
    ts = _roles_set(motion__press__duration=("duration", "{motion.d.fast}",
                                             {"motion:reduced": "{motion.d.slow}"}),
                    motion__progress__duration=("duration", "{motion.d.slow}", {}))
    ts.add(Token("motion.d.tiny", "duration", {"value": 50, "unit": "ms"}))
    ts.add(Token("motion.swap.duration", "duration", "{motion.d.tiny}",
                 modes={"motion:reduced": "{motion.d.fast}"}, layer="semantic"))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures
            if f.check == "reduced-not-longer"] == [
        ("reduced-not-longer", "system", "direction:ltr,motion:reduced",
         "motion.press.duration lasts 1200ms under reduced motion but 100ms in standard; "
         "reduced motion never lengthens a move, so point its motion:reduced override at "
         "motion.d.fast or a shorter step"),
        ("reduced-not-longer", "system", "direction:ltr,motion:reduced",
         "motion.swap.duration lasts 100ms under reduced motion but 50ms in standard; reduced "
         "motion never lengthens a move, so point its motion:reduced override at motion.d.tiny "
         "or a shorter step")]


def test_a_curve_linear_only_under_rtl_fails():
    ts = _roles_set(motion__reveal__curve=("cubicBezier", "{motion.c.gentle}",
                                           {"direction:rtl": "{motion.c.linear}",
                                            "direction:rtl,motion:reduced": "{motion.c.gentle}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("linear-progress-only", "system", "direction:rtl,motion:standard",
         "motion.reveal.curve is linear under direction:rtl; only motion.progress.curve loops, "
         "and a one-shot move at an even pace reads mechanical, so point its direction:rtl "
         "override at an eased curve such as motion.curve.out")]


def test_a_duration_longer_only_under_rtl_reduced_motion_fails():
    ts = _roles_set(motion__press__duration=("duration", "{motion.d.fast}",
                                             {"direction:rtl,motion:reduced": "{motion.d.slow}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("reduced-not-longer", "system", "direction:rtl,motion:reduced",
         "motion.press.duration lasts 1200ms under direction:rtl,motion:reduced but 100ms under "
         "direction:rtl; reduced motion never lengthens a move, so point its "
         "direction:rtl,motion:reduced override at motion.d.fast or a shorter step")]


def test_reduced_is_compared_with_standard_in_the_same_direction():
    # The reduced value is the same in both directions and passes in ltr,
    # but rtl shortens standard, so rtl reduced motion lengthens the move.
    ts = _roles_set(motion__press__duration=("duration", "{motion.d.mid}",
                                             {"motion:reduced": "{motion.d.fast}",
                                              "direction:rtl": "{motion.d.tiny}",
                                              "direction:rtl,motion:reduced": "{motion.d.fast}"}))
    ts.add(Token("motion.d.mid", "duration", {"value": 200, "unit": "ms"}))
    ts.add(Token("motion.d.tiny", "duration", {"value": 50, "unit": "ms"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures] == [
        ("reduced-not-longer", "direction:rtl,motion:reduced",
         "motion.press.duration lasts 100ms under direction:rtl,motion:reduced but 50ms under "
         "direction:rtl; reduced motion never lengthens a move, so point its "
         "direction:rtl,motion:reduced override at motion.d.tiny or a shorter step")]


def test_the_progress_loop_is_never_faster_than_three_cycles_a_second():
    ts = _roles_set(motion__progress__duration=("duration", "{motion.d.fast}", {}))
    ts.add(Token("motion.d.400", "duration", {"value": 0.4, "unit": "s"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    want = ("motion.progress.duration lasts 100ms; our floor for a loop is 334ms, since a "
            "shorter cycle repeats more than three times a second and a loop that flashes that "
            "often falls under WCAG 2.3.1, so point it at motion.d.400 or a longer step")
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("progress-floor", "system", "direction:ltr,motion:standard", want)]
    assert "2.3.1 sets" not in want and "2.3.1 asks" not in want

    # Fast only under rtl: the fix names that override and the shortest
    # duration primitive at or above the floor.
    ts = _roles_set(motion__progress__duration=("duration", "{motion.d.slow}",
                                                {"direction:rtl": "{motion.d.fast}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures] == [
        ("progress-floor", "direction:rtl,motion:standard",
         "motion.progress.duration lasts 100ms under direction:rtl; our floor for a loop is "
         "334ms, since a shorter cycle repeats more than three times a second and a loop that "
         "flashes that often falls under WCAG 2.3.1, so point its direction:rtl override at "
         "motion.d.slow or a longer step")]


@pytest.mark.parametrize("motion", [i / 10 for i in range(11)])
def test_generated_motion_passes_the_new_rules(motion):
    ts = generate_motion(axes(motion)).tokens
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert report.passed, report.summary()
    assert {"press-in-place", "linear-progress-only", "reduced-not-longer",
            "progress-floor"} <= {c.id for c in CHECKS}
