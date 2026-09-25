"""Motion: pace and curves from the motion axis, a reduced-motion variant
that keeps meaning and drops travel, and a sign mirrored under rtl."""
import pytest

from engine.foundations import build_system, from_dtcg, to_css, to_dtcg
from engine.foundations.foundation import role_types_check
from engine.foundations.gate import gate
from engine.foundations.motion import (
    CHECKS, FOUNDATION, GENTLE, LINEAR, ROLES, curves, distance_unit, duration_ms,
    generate_motion)
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
           "motion.expand": 200, "motion.page": 250, "motion.progress": 1200,
           "motion.expressive": 300}),
    (0.5, {"motion.press": 100, "motion.reveal": 250, "motion.dismiss": 150, "motion.swap": 200,
           "motion.expand": 250, "motion.page": 400, "motion.progress": 1200,
           "motion.expressive": 500}),
    (1.0, {"motion.press": 100, "motion.reveal": 300, "motion.dismiss": 200, "motion.swap": 250,
           "motion.expand": 300, "motion.page": 500, "motion.progress": 800,
           "motion.expressive": 800}),
])
def test_durations_follow_the_motion_axis(motion, want):
    assert {r: duration_ms(r, motion) for r in ROLES} == want
    ts = generate_motion(axes(motion)).tokens
    assert {r: ts.resolve(f"{r}.duration")["value"] for r in ROLES} == want


def test_curves_bend_continuously_with_the_overshoot():
    assert curves(0.0)[0] == [0.25, 0.1, 0.25, 1]
    assert curves(1.0)[0] == [0.34, 1.56, 0.64, 1]
    assert curves(0.5)[0] == [0.295, 0.83, 0.445, 1]
    assert [distance_unit(m) for m in (0.0, 0.5, 1.0)] == [4, 6, 8]
    ts = generate_motion(axes(1.0)).tokens
    # motion 1 at formality 0.5 overshoots 0.7 of the way
    assert ts.resolve("motion.reveal.curve") == curves(0.7)[0]
    assert ts.resolve("motion.page.distance") == {"value": 16, "unit": "px"}
    formal = generate_motion(AxisValues(0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5)).tokens
    assert formal.resolve("motion.reveal.curve") == curves(0.4)[0]


def test_the_expressive_role_is_removed_under_reduced_motion():
    ts = generate_motion(axes(0.8)).tokens
    assert ts.resolve("motion.expressive.duration")["value"] > 400
    assert ts.resolve("motion.expressive.duration", "motion:reduced")["value"] == 0
    assert ts.resolve("motion.expressive.distance", "motion:reduced")["value"] == 0
    assert ts.resolve("motion.expressive.distance")["value"] == 4 * distance_unit(0.8)


@pytest.mark.parametrize("motion", [i / 10 for i in range(11)])
def test_reduced_motion_keeps_meaning_and_drops_travel(motion):
    ts = generate_motion(axes(motion)).tokens
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed
    for role in ROLES:
        reduced = ts.resolve(f"{role}.duration", "motion:reduced")["value"]
        standard = ts.resolve(f"{role}.duration")["value"]
        if role == "motion.progress":
            assert reduced == standard
        elif role == "motion.expressive":
            assert reduced == 0
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


def test_only_motion_and_formality_move_motion():
    base = [(t.path, t.value, t.modes) for t in generate_motion(axes()).tokens.tokens()]
    other = axes(warmth=0.0, contrast=1.0, density=1.0, geometry=0.0, type_personality=0.0)
    assert [(t.path, t.value, t.modes) for t in generate_motion(other).tokens.tokens()] == base
    formal = axes(formality=1.0)
    assert [(t.path, t.value, t.modes) for t in generate_motion(formal).tokens.tokens()] != base


def test_dtcg_round_trip_and_css_for_reduced_motion_and_rtl():
    ts = generate_motion(axes()).tokens
    doc = to_dtcg(ts)
    assert doc["motion"]["duration"]["150"]["$value"] == {"value": 150, "unit": "ms"}
    assert doc["motion"]["curve"]["linear"]["$value"] == [0, 0, 1, 1]
    assert to_dtcg(from_dtcg(doc)) == doc
    css = to_css(build_system(axes(), "#3366FF").tokens)
    assert "  --motion-curve-in-out: cubic-bezier(0.511, -0.21, 0.489, 1.21);" in css
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
        ("progress-keeps-pace", "system", "direction:ltr,motion:reduced", want)]


def test_only_travel_removal_cites_wcag_and_distances_keep_their_unit():
    assert {c.id: c.criterion for c in CHECKS} == {
        "reduced-travel": "2.3.3", "reduced-length": "system", "expressive-removed": "system",
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
        ("reduced-travel", "2.3.3", "direction:ltr,motion:reduced",
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
    # The press is past the cap too, so reduced-length owns it alone.
    assert [(f.check, f.message) for f in report.failures
            if f.message.startswith("motion.press.duration")] == [
        ("reduced-length", "motion.press.duration lasts 1200ms under reduced motion; cap it at "
         "100ms with a motion:reduced override")]
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures
            if f.check == "reduced-not-longer"] == [
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
        ("reduced-length", "system", "direction:rtl,motion:reduced",
         "motion.press.duration lasts 1200ms under direction:rtl,motion:reduced; cap it at 100ms "
         "with a direction:rtl,motion:reduced override")]


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


# Motion varies on motion and direction, so every check reads both: a rule
# broken only under direction:rtl fails there, named with that context.

def test_an_rtl_only_reduced_distance_fails():
    ts = _roles_set(motion__reveal__distance=("dimension", "{motion.x.a}",
                                              {"motion:reduced": "{motion.x.zero}",
                                               "direction:rtl,motion:reduced": "{motion.x.a}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("reduced-travel", "2.3.3", "direction:rtl,motion:reduced",
         "motion.reveal.distance travels 0.5rem under direction:rtl,motion:reduced; point its "
         "direction:rtl,motion:reduced override at motion.distance.0")]


def test_an_rtl_only_overshoot_under_reduced_motion_fails():
    ts = _roles_set(motion__reveal__curve=("cubicBezier", "{motion.c.gentle}",
                                           {"direction:rtl,motion:reduced": "{motion.c.over}"}))
    ts.add(Token("motion.c.over", "cubicBezier", [0.34, 1.56, 0.64, 1]))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("reduced-curve", "system", "direction:rtl,motion:reduced",
         "motion.reveal.curve overshoots under direction:rtl,motion:reduced; point its "
         "direction:rtl,motion:reduced override at motion.curve.gentle")]


def test_an_rtl_only_loop_pace_change_fails():
    ts = _roles_set(motion__progress__duration=("duration", "{motion.d.slow}",
                                                {"direction:rtl,motion:reduced": "{motion.d.400}"}))
    ts.add(Token("motion.d.400", "duration", {"value": 400, "unit": "ms"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("progress-keeps-pace", "system", "direction:rtl,motion:reduced",
         "motion.progress.duration lasts 400ms under direction:rtl,motion:reduced but 1200ms "
         "under direction:rtl; a status loop keeps its pace, so drop its "
         "direction:rtl,motion:reduced override")]


def test_an_rtl_only_eased_loop_fails():
    ts = _roles_set(motion__progress__curve=("cubicBezier", "{motion.c.linear}",
                                             {"direction:rtl": "{motion.c.gentle}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("progress-linear", "system", "direction:rtl,motion:standard",
         "motion.progress.curve is [0.4, 0, 0.6, 1] under direction:rtl; a continuous loop "
         "must keep an even pace, so point its direction:rtl override at motion.curve.linear")]


def test_an_rtl_only_reduced_loop_ease_fails_once():
    # Eased only under rtl reduced motion: the loop changes pace there, which
    # is progress-keeps-pace's finding; progress-linear does not repeat it.
    ts = _roles_set(motion__progress__curve=("cubicBezier", "{motion.c.linear}",
                                             {"direction:rtl,motion:reduced": "{motion.c.gentle}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures] == [
        ("progress-keeps-pace", "direction:rtl,motion:reduced",
         "motion.progress.curve is [0.4, 0, 0.6, 1] under direction:rtl,motion:reduced; a "
         "status loop keeps an even pace, so drop its direction:rtl,motion:reduced override and "
         "keep motion.curve.linear")]


def test_an_rtl_only_reduced_length_fails():
    ts = _roles_set(motion__reveal__duration=("duration", "{motion.d.fast}",
                                              {"direction:rtl": "{motion.d.slow}",
                                               "direction:rtl,motion:reduced": "{motion.d.slow}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures
            if f.check == "reduced-length"] == [
        ("reduced-length", "direction:rtl,motion:reduced",
         "motion.reveal.duration lasts 1200ms under direction:rtl,motion:reduced; cap it at "
         "100ms with a direction:rtl,motion:reduced override")]


def test_dismiss_is_faster_in_both_directions():
    ts = _roles_set(motion__reveal__duration=("duration", "{motion.d.slow}", {}),
                    motion__dismiss__duration=("duration", "{motion.d.fast}",
                                               {"direction:rtl": "{motion.d.slow}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures
            if f.check == "dismiss-faster"] == [
        ("dismiss-faster", "direction:rtl,motion:standard",
         "motion.dismiss.duration (1200ms) is not shorter than motion.reveal.duration (1200ms) "
         "under direction:rtl; leaving should never hold the next action longer than arriving, "
         "so shorten motion.dismiss.duration under direction:rtl")]
    dismiss = {c.id: c for c in CHECKS}["dismiss-faster"]
    assert dismiss.axes == ("motion", "direction") and dismiss.exempt_axes == ()


def test_reduced_motion_lets_dismiss_and_reveal_tie():
    ts = _roles_set(motion__reveal__duration=("duration", "{motion.d.slow}",
                                              {"motion:reduced": "{motion.d.fast}"}),
                    motion__dismiss__duration=("duration", "{motion.d.fast}", {}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [f for f in report.failures if f.check == "dismiss-faster"] == []


def test_reduced_motion_never_lets_dismiss_outlast_reveal():
    ts = _roles_set(motion__reveal__duration=("duration", "{motion.d.slow}",
                                              {"motion:reduced": "{motion.d.tiny}"}),
                    motion__dismiss__duration=("duration", "{motion.d.fast}", {}))
    ts.add(Token("motion.d.tiny", "duration", {"value": 50, "unit": "ms"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures
            if f.check == "dismiss-faster"] == [
        ("dismiss-faster", "direction:ltr,motion:reduced",
         "motion.dismiss.duration (100ms) is longer than motion.reveal.duration (50ms) under "
         "motion:reduced; reduced motion may let the two tie but never lets leaving outlast "
         "arriving, so shorten motion.dismiss.duration under motion:reduced")]


def test_a_dismiss_past_the_cap_is_the_length_check_alone():
    # Capping the dismiss at its standard 100ms also lets it tie the reveal.
    ts = _roles_set(motion__reveal__duration=("duration", "{motion.d.slow}",
                                              {"motion:reduced": "{motion.d.fast}"}),
                    motion__dismiss__duration=("duration", "{motion.d.fast}",
                                               {"motion:reduced": "{motion.d.slow}"}))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.message) for f in report.failures
            if f.message.startswith("motion.dismiss.duration")] == [
        ("reduced-length", "motion.dismiss.duration lasts 1200ms under reduced motion; cap it at "
         "100ms with a motion:reduced override")]


def test_a_standard_motion_finding_is_not_repeated_under_reduced_motion():
    ts = _roles_set(motion__reveal__duration=("duration", "{motion.d.fast}", {}),
                    motion__dismiss__duration=("duration", "{motion.d.slow}", {}))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [f.mode for f in report.failures if f.check == "dismiss-faster"] == [
        "direction:ltr,motion:standard"]


def test_the_inline_sign_mirrors_under_reduced_motion_too():
    ts = _roles_set(motion__inline_sign=("number", "{motion.n.fwd}",
                                         {"direction:rtl": "{motion.n.back}",
                                          "direction:rtl,motion:reduced": "{motion.n.fwd}"}))
    ts.add(Token("motion.n.fwd", "number", 1))
    ts.add(Token("motion.n.back", "number", -1))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode, f.message) for f in report.failures] == [
        ("mirrored-motion", "direction:rtl,motion:reduced",
         "motion.inline-sign (direction:rtl,motion:reduced) is 1; horizontal travel follows the "
         "reading direction, so it must be -1 here")]


def test_an_rtl_reduced_finding_is_named_once():
    # A press that travels only under rtl reduced motion is reduced-travel's
    # finding; press-in-place does not repeat it.
    ts = _press_set(motion__press__distance=("dimension", "{motion.x.zero}",
                                             {"direction:rtl,motion:reduced": "{motion.x.four}"}))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode) for f in report.failures] == [
        ("reduced-travel", "direction:rtl,motion:reduced")]
    # A loop that speeds up only under rtl reduced motion is
    # progress-keeps-pace's finding; dropping the override also clears the
    # loop floor, so progress-floor does not repeat it.
    fast = {"direction:rtl,motion:reduced": "{motion.d.fast}"}
    ts = _roles_set(motion__progress__duration=("duration", "{motion.d.slow}", fast))
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.mode) for f in report.failures] == [
        ("progress-keeps-pace", "direction:rtl,motion:reduced")]


def _broken(role_path, modes):
    """Generated motion with one role's overrides replaced."""
    ts = generate_motion(axes(0.8)).tokens
    ts.get(role_path).modes = modes
    return ts


def _findings_for(ts, path):
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    return [(f.check, f.mode, f.message) for f in report.failures if f.message.startswith(path)]


def test_a_broken_expressive_role_gives_one_finding_per_property():
    ts = _broken("motion.expressive.duration", {})
    ts.get("motion.expressive.distance").modes = {}
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.criterion, f.mode, f.message) for f in report.failures] == [
        ("reduced-travel", "2.3.3", "direction:ltr,motion:reduced",
         "motion.expressive.distance travels 28px under reduced motion; point its "
         "motion:reduced override at motion.distance.0"),
        ("expressive-removed", "system", "direction:ltr,motion:reduced",
         "motion.expressive.duration lasts 800ms under reduced motion; decoration is removed "
         "under reduced motion, our rule, so point its motion:reduced override at "
         "motion.duration.0")]


def test_a_short_expressive_role_under_reduced_motion_still_fails_as_our_rule():
    ts = _broken("motion.expressive.duration", {"motion:reduced": "{motion.duration.50}"})
    assert _findings_for(ts, "motion.expressive") == [
        ("expressive-removed", "direction:ltr,motion:reduced",
         "motion.expressive.duration lasts 50ms under reduced motion; decoration is removed "
         "under reduced motion, our rule, so point its motion:reduced override at "
         "motion.duration.0")]


@pytest.mark.parametrize("role", [r for r in ROLES if r != "motion.progress"])
def test_every_broken_reduced_duration_has_one_owner(role):
    # Longer than standard and past the cap: one finding whose fix clears both.
    ts = _broken(f"{role}.duration", {"motion:reduced": "{motion.duration.1200}"})
    found = _findings_for(ts, f"{role}.duration")
    assert len(found) == 1, found
    # Longer than standard but under the cap: one finding too.
    ts = generate_motion(axes(0.0)).tokens
    std = ts.resolve(f"{role}.duration")["value"]
    if std < 100:
        ts.get(f"{role}.duration").modes = {"motion:reduced": "{motion.duration.100}"}
        assert len(_findings_for(ts, f"{role}.duration")) == 1


def test_the_length_cap_names_a_step_that_also_keeps_reduced_no_longer():
    ts = _roles_set(motion__swap__duration=("duration", "{motion.d.tiny}",
                                            {"motion:reduced": "{motion.d.slow}"}))
    ts.add(Token("motion.d.tiny", "duration", {"value": 50, "unit": "ms"}))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.message) for f in report.failures] == [
        ("reduced-length", "motion.swap.duration lasts 1200ms under reduced motion; cap it at "
         "50ms, its standard length, with a motion:reduced override")]
