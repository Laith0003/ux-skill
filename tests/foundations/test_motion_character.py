"""Motion character from measured award pages: interaction moves last 300
to 500ms, formality slows them and energy speeds them, on long-tail curves
that still answer at once; entrances, a state role, a sliding indicator, a
press scale and inertial scroll, each held under reduced motion."""
import itertools

import pytest

from engine.foundations import build_system, character
from engine.foundations.gate import gate
from engine.foundations.motion import (
    CHECKS, DIRECT, DIRECT_T50, DIRECT_T90, ENTRANCE_T50, ENTRANCES, curves, generate_motion,
    settle_ms)
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

FORMAL_CALM = AxisValues(warmth=0.4, contrast=0.2, density=0.4, geometry=0.3, formality=0.8,
                         motion=0.2, type_personality=0.6)
LOUD_PLAYFUL = AxisValues(warmth=0.7, contrast=0.9, density=0.5, geometry=0.7, formality=0.1,
                          motion=0.9, type_personality=0.5)
MODES = ("direction:ltr", "direction:rtl")


def axes(**kw):
    values = dict(zip(("warmth", "contrast", "density", "geometry", "formality", "motion",
                       "type_personality"), [0.5] * 7))
    values.update(kw)
    return AxisValues(**values)


def ms(ts, role, mode=""):
    return ts.resolve(f"{role}.duration", mode)["value"]


def test_settle_time_reads_the_curve():
    assert settle_ms(620, [0.2, 1, 0.25, 1], 0.5) == pytest.approx(69, abs=2)
    assert settle_ms(400, [0, 0, 1, 1], 0.5) == pytest.approx(200, abs=1)
    times = [settle_ms(500, [0.2, 0.8, 0.2, 1], f / 10) for f in range(1, 10)]
    assert times == sorted(times)
    # an overshooting curve counts its first arrival
    assert settle_ms(500, [0.34, 1.56, 0.64, 1], 0.9) < settle_ms(500, [0.2, 0.8, 0.2, 1], 0.9)


def test_the_plain_out_curve_is_a_long_tail_that_is_mostly_done_early():
    plain = curves(0.0)[0]
    assert plain == [0.2, 0.8, 0.2, 1]
    assert settle_ms(1000, plain, 0.9) <= 450
    assert all(0 <= p <= 1 for p in plain)


def test_a_formal_calm_brief_moves_slower_than_a_loud_playful_one():
    calm = generate_motion(FORMAL_CALM).tokens
    loud = generate_motion(LOUD_PLAYFUL).tokens
    assert 350 <= ms(calm, "motion.swap") <= 500
    assert 200 <= ms(loud, "motion.swap") <= 320
    assert ms(loud, "motion.reveal") < ms(calm, "motion.reveal")
    assert loud.resolve("motion.swap.curve")[1] > 1  # it overshoots
    assert calm.resolve("motion.swap.curve")[1] < 1


@pytest.mark.parametrize("axis, sign", [("formality", 1), ("contrast", -1), ("motion", -1)])
def test_the_pace_follows_formality_and_energy(axis, sign):
    paces = [character.motion_pace(axes(**{axis: i / 10})) for i in range(11)]
    assert min(sign * (b - a) for a, b in zip(paces, paces[1:])) > 0


def test_every_move_answers_at_once_at_every_corner():
    for m, f, c in itertools.product((0.0, 1.0), repeat=3):
        ts = generate_motion(axes(motion=m, formality=f, contrast=c)).tokens
        for role in DIRECT:
            curve = ts.resolve(f"{role}.curve")
            assert settle_ms(ms(ts, role), curve, 0.5) <= DIRECT_T50 + 0.5, (m, f, c, role)
            assert settle_ms(ms(ts, role), curve, 0.9) <= DIRECT_T90 + 0.5, (m, f, c, role)
        for role in ENTRANCES:
            curve = ts.resolve(f"{role}.curve")
            assert settle_ms(ms(ts, role), curve, 0.5) <= ENTRANCE_T50 + 0.5, (m, f, c, role)
        assert [f for f in gate(ts, [], CHECKS, raise_on_fail=False).failures] == []


def test_a_slow_symmetric_swap_is_named_with_its_half_time():
    ts = generate_motion(axes()).tokens
    slow = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == "motion.swap.curve":
            t = Token(t.path, t.type, "{motion.curve.in-out}", modes=t.modes, layer="semantic")
        slow.add(t)
    msgs = [f.message for f in gate(slow, [], CHECKS, raise_on_fail=False).failures
            if f.check == "response-head"]
    assert len(msgs) == 1 and msgs[0].startswith("motion.swap reaches 50% of its travel at 175ms")
    assert "motion.curve.out" in msgs[0]


def test_the_entrance_role_runs_350_to_800ms_and_fades_briefly_under_reduced_motion():
    for m in (0.0, 0.5, 1.0):
        ts = generate_motion(axes(motion=m)).tokens
        assert 350 <= ms(ts, "motion.arrive") <= 800
        assert ms(ts, "motion.arrive", "motion:reduced") <= 100
        assert ts.resolve("motion.arrive.distance", "motion:reduced")["value"] == 0
    arrivals = [ms(generate_motion(axes(motion=i / 10)).tokens, "motion.arrive")
                for i in range(11)]
    assert arrivals == sorted(arrivals) and arrivals[-1] - arrivals[0] >= 200


def test_the_state_role_runs_about_150_to_240ms_and_stays_short_under_reduced_motion():
    still = generate_motion(axes(motion=0.0, formality=1.0)).tokens
    kinetic = generate_motion(axes(motion=1.0, formality=0.0)).tokens
    assert ms(still, "motion.state") == 150 and 200 <= ms(kinetic, "motion.state") <= 250
    for ts in (still, kinetic):
        assert ms(ts, "motion.state", "motion:reduced") <= 100
        assert ts.resolve("motion.state.curve") == ts.resolve("motion.curve.out")


def test_the_indicator_slides_by_the_motion_axis_snaps_under_reduced_motion_and_mirrors():
    for m in (0.0, 1.0):
        ts = generate_motion(axes(motion=m)).tokens
        assert 200 <= ms(ts, "motion.indicator") <= 300
        assert ms(ts, "motion.indicator", "motion:reduced") == 0
        assert ts.resolve("motion.inline-sign", "direction:rtl") == -1


def test_a_press_scales_by_the_motion_axis_and_never_under_reduced_motion():
    still = generate_motion(axes(motion=0.0, formality=1.0)).tokens
    kinetic = generate_motion(axes(motion=1.0, formality=0.0)).tokens
    assert still.resolve("motion.press.scale") == pytest.approx(0.985)
    assert kinetic.resolve("motion.press.scale") == pytest.approx(0.96)
    for ts in (still, kinetic):
        assert ts.resolve("motion.press.scale", "motion:reduced") == 1


def test_a_press_scale_out_of_range_or_under_reduced_motion_is_named():
    ts = generate_motion(axes(motion=1.0)).tokens
    for value, want in ((0.9, "a press scales to between 0.95 and 1"),
                        (0.97, "under reduced motion a press does not change size")):
        broken = TokenSet(ts.axes)
        for t in ts.tokens():
            if t.path == "motion.press.scale":
                t = Token(t.path, t.type, "{motion.scale.x}", layer="semantic")
            broken.add(t)
        broken.add(Token("motion.scale.x", "number", value))
        msgs = [f.message for f in gate(broken, [], CHECKS, raise_on_fail=False).failures
                if f.check == "press-in-place"]
        assert msgs and want in msgs[0], msgs


def test_inertial_scroll_starts_above_a_motion_threshold_and_never_runs_reduced():
    assert character.scroll_strength(axes(motion=0.6)) == 0
    assert character.scroll_strength(axes(motion=1.0)) > 0.5
    loud = build_system(LOUD_PLAYFUL, "#3366FF").tokens
    assert loud.resolve("motion.scroll") > 0 and loud.resolve("motion.scroll",
                                                              "motion:reduced") == 0
    assert build_system(FORMAL_CALM, "#3366FF").tokens.resolve("motion.scroll") == 0


def test_a_scroll_that_glides_under_reduced_motion_is_named():
    ts = generate_motion(axes(motion=1.0)).tokens
    broken = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == "motion.scroll":
            t = Token(t.path, t.type, t.value, layer="semantic")
        broken.add(t)
    report = gate(broken, [], CHECKS, raise_on_fail=False)
    msgs = [(f.check, f.criterion) for f in report.failures]
    assert ("reduced-scroll", "2.3.3") in msgs
