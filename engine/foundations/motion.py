"""Motion foundation: durations, easing curves and travel distances, the
interaction roles that use them, a reduced-motion variant, and a sign that
mirrors horizontal travel under dir="rtl".

The motion axis sets pace and character: a still brand moves briefly with
plain curves, a kinetic one takes longer and may overshoot. Under
motion:reduced every role keeps its meaning but loses travel, overshoot
and length: distances drop to 0, curves turn gentle, durations cap at
REDUCED_MAX_MS and never grow (the progress loop keeps its pace, it
reports status). In every context a press confirms in place, only the
progress loop runs linear, and the loop lasts at least LOOP_MIN_MS.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.modes import join, parse, sparse
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.synthesizer.axes import AxisValues

DURATIONS_MS = (0, 50, 100, 150, 200, 250, 300, 400, 500, 800, 1200)
REDUCED_MAX_MS = 100
# Our floor for one cycle of a loop: shorter repeats more than three times
# a second.
LOOP_MIN_MS = 334
LINEAR = [0, 0, 1, 1]
GENTLE = [0.4, 0, 0.6, 1]
# motion axis band -> curves (out, in, in-out)
CURVES = {
    "calm": ([0.25, 0.1, 0.25, 1], [0.42, 0, 1, 1], [0.42, 0, 0.58, 1]),
    "balanced": ([0.16, 1, 0.3, 1], [0.7, 0, 0.84, 0], [0.65, 0, 0.35, 1]),
    "lively": ([0.34, 1.56, 0.64, 1], [0.36, 0, 0.66, -0.56], [0.68, -0.6, 0.32, 1.6]),
}
# role -> (ms when the motion axis is 0, ms when it is 1, curve, distance step or None)
ROLES: Dict[str, Tuple[int, int, str, object]] = {
    "motion.press": (100, 100, "out", None),
    "motion.reveal": (150, 300, "out", 1),
    "motion.dismiss": (100, 200, "in", 1),
    "motion.swap": (150, 250, "in-out", None),
    "motion.expand": (200, 300, "in-out", None),
    "motion.page": (250, 500, "out", 2),
    "motion.progress": (1200, 800, "linear", None),
}


def band(motion: float) -> str:
    return "calm" if motion < 0.34 else ("lively" if motion >= 0.66 else "balanced")


def distance_unit(motion: float) -> int:
    """Travel step in px: 4 for a still brand, 8 for a kinetic one."""
    return 4 + int(4 * motion + 0.5)


def duration_ms(role: str, motion: float) -> int:
    still, kinetic = ROLES[role][0], ROLES[role][1]
    target = still + (kinetic - still) * motion
    return min(DURATIONS_MS, key=lambda d: (abs(d - target), -d))


def generate_motion(axes: AxisValues) -> Generated:
    m = axes.motion
    ts = TokenSet()
    for ms in DURATIONS_MS:
        ts.add(Token(f"motion.duration.{ms}", "duration", {"value": ms, "unit": "ms"}))
    out_curve, in_curve, in_out_curve = CURVES[band(m)]
    for name, curve in (("linear", LINEAR), ("out", out_curve), ("in", in_curve),
                        ("in-out", in_out_curve), ("gentle", GENTLE)):
        ts.add(Token(f"motion.curve.{name}", "cubicBezier", list(curve)))
    unit = distance_unit(m)
    for step, mult in enumerate((0, 1, 2, 4)):
        ts.add(Token(f"motion.distance.{step}", "dimension", {"value": unit * mult, "unit": "px"}))
    ts.add(Token("motion.sign.forward", "number", 1))
    ts.add(Token("motion.sign.backward", "number", -1))

    for role, (_, _, curve, distance) in ROLES.items():
        ms = duration_ms(role, m)
        reduced_ms = ms if role == "motion.progress" else min(ms, REDUCED_MAX_MS)
        ts.add(Token(f"{role}.duration", "duration", "{motion.duration.%d}" % ms,
                     modes={} if reduced_ms == ms else
                     {"motion:reduced": "{motion.duration.%d}" % reduced_ms},
                     layer="semantic"))
        reduced_curve = {} if curve == "linear" else {"motion:reduced": "{motion.curve.gentle}"}
        ts.add(Token(f"{role}.curve", "cubicBezier", "{motion.curve.%s}" % curve,
                     modes=reduced_curve, layer="semantic"))
        if distance is not None:
            ts.add(Token(f"{role}.distance", "dimension", "{motion.distance.%d}" % distance,
                         modes={"motion:reduced": "{motion.distance.0}"}, layer="semantic"))
    ts.add(Token("motion.inline-sign", "number", "{motion.sign.forward}",
                 modes={"direction:rtl": "{motion.sign.backward}"}, layer="semantic"))
    return Generated(tokens=ts, notes=[f"motion: {band(m)} curves, {unit}px travel step"])


# role suffix -> the token type its checks read
SUFFIX_TYPES: Dict[str, str] = {"duration": "duration", "curve": "cubicBezier",
                                "distance": "dimension"}
SIGN = "motion.inline-sign"
# Role path -> token type; the build's role-types check reports any other
# type once, and the checks below skip it.
ROLE_TYPES: Dict[str, str] = {
    **{f"{r}.{suffix}": t for r in ROLES for suffix, t in SUFFIX_TYPES.items()},
    SIGN: "number",
}


def _typed(ts: TokenSet, path: str) -> bool:
    """The typed accessor every check reads through: a role is read only
    when it exists with the type its role expects."""
    return typed(ts, path, ROLE_TYPES)


def _roles_with(ts: TokenSet, suffix: str) -> List[str]:
    return [f"{r}.{suffix}" for r in ROLES if _typed(ts, f"{r}.{suffix}")]


def _ms(ts: TokenSet, path: str, mode: str = "") -> float:
    v = ts.resolve(path, mode)
    return v["value"] * (1000 if v["unit"] == "s" else 1)


def _reduced_travel(ts: TokenSet, mode: str) -> List[str]:
    if "motion:reduced" not in mode:
        return []
    out = []
    for path in _roles_with(ts, "distance"):
        v = ts.resolve(path, mode)
        if v["value"] != 0:
            out.append(f"{path} travels {v['value']:g}{v['unit']} under reduced motion; point "
                       "its motion:reduced override at motion.distance.0")
    return out


def _reduced_length(ts: TokenSet, mode: str) -> List[str]:
    if "motion:reduced" not in mode:
        return []
    return [f"{path} lasts {_ms(ts, path, mode):g}ms under reduced motion; cap it at "
            f"{REDUCED_MAX_MS}ms with a motion:reduced override"
            for path in _roles_with(ts, "duration")
            if path != "motion.progress.duration" and _ms(ts, path, mode) > REDUCED_MAX_MS]


def _reduced_curve(ts: TokenSet, mode: str) -> List[str]:
    if "motion:reduced" not in mode:
        return []
    out = []
    for path in _roles_with(ts, "curve"):
        c = ts.resolve(path, mode)
        if not (0 <= c[1] <= 1 and 0 <= c[3] <= 1):
            out.append(f"{path} overshoots under reduced motion; point its motion:reduced "
                       "override at motion.curve.gentle")
    return out


def _dismiss_faster(ts: TokenSet, mode: str) -> List[str]:
    a, b = "motion.dismiss.duration", "motion.reveal.duration"
    if _typed(ts, a) and _typed(ts, b) and _ms(ts, a) >= _ms(ts, b):
        return [f"{a} ({_ms(ts, a):g}ms) is not shorter than {b} ({_ms(ts, b):g}ms); leaving "
                "should never hold the next action longer than arriving, so shorten it"]
    return []


def _progress_linear(ts: TokenSet, mode: str) -> List[str]:
    p = "motion.progress.curve"
    if _typed(ts, p):
        curve = ts.resolve(p)
        if curve != LINEAR:
            return [f"{p} is {curve}; a continuous loop must keep an even pace, so point it "
                    "at motion.curve.linear"]
    return []


def _progress_pace(ts: TokenSet, mode: str) -> List[str]:
    """Under reduced motion the progress loop keeps its standard duration
    and its linear curve: it reports status, so slowing or easing it
    misleads. A curve that is already wrong in standard is progress-linear's
    finding, not repeated here."""
    if "motion:reduced" not in mode:
        return []
    out = []
    d = "motion.progress.duration"
    if _typed(ts, d):
        reduced, standard = _ms(ts, d, mode), _ms(ts, d)
        if reduced != standard:
            out.append(f"{d} lasts {reduced:g}ms under reduced motion but {standard:g}ms in "
                       "standard; a status loop keeps its pace, so drop its motion:reduced "
                       "override")
    c = "motion.progress.curve"
    if _typed(ts, c):
        curve = ts.resolve(c, mode)
        if curve != LINEAR and curve != ts.resolve(c):
            out.append(f"{c} is {curve} under reduced motion; a status loop keeps an even "
                       "pace, so drop its motion:reduced override and keep motion.curve.linear")
    return out


def _mirrored(ts: TokenSet, mode: str) -> List[str]:
    p = SIGN
    if not _typed(ts, p):
        return []
    want = -1 if "direction:rtl" in mode else 1
    got = ts.resolve(p, mode)
    if got == want:
        return []
    return [f"{p} ({mode}) is {got:g}; horizontal travel follows the reading direction, so it "
            f"must be {want} here"]


def _new_here(ts: TokenSet, path: str, mode: str) -> bool:
    """False when `path` reads the same one step closer to the base context
    (one non-base axis set back to its base): a failure there is already
    reported there."""
    pairs = parse(mode, ts.axes)
    value = ts.resolve(path, mode)
    return all(ts.resolve(path, join({**pairs, axis: ts.axes[axis][0]}, ts.axes)) != value
               for axis, v in pairs.items() if v != ts.axes[axis][0])


def _where(ts: TokenSet, mode: str) -> Tuple[str, str]:
    """(" under <context>", "its <context> override") for a non-base
    context; ("", "it") for the base one."""
    key = sparse(mode, ts.axes)
    return (f" under {key}", f"its {key} override") if key else ("", "it")


def _press_in_place(ts: TokenSet, mode: str) -> List[str]:
    """A press confirms where the finger is: any press travel is 0 in every
    context. Under plain reduced motion, reduced-travel already names a
    travelling press role, so it is not repeated."""
    owned = set(_roles_with(ts, "distance")) if sparse(mode, ts.axes) == "motion:reduced" else set()
    out = []
    for t in ts.tokens():
        if not (t.path.startswith("motion.press.") and t.type == "dimension") or t.path in owned:
            continue
        v = ts.resolve(t.path, mode)
        if v["value"] != 0 and _new_here(ts, t.path, mode):
            where, what = _where(ts, mode)
            out.append(f"{t.path} travels {v['value']:g}{v['unit']}{where}; a press confirms in "
                       f"place, so point {what} at motion.distance.0")
    return out


def _is_linear(curve: List[float]) -> bool:
    """Both control points on the diagonal: an even pace from start to end."""
    return curve[0] == curve[1] and curve[2] == curve[3]


def _linear_progress_only(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for t in ts.tokens():
        if (t.layer != "semantic" or t.type != "cubicBezier" or not t.path.startswith("motion.")
                or t.path == "motion.progress.curve"):
            continue
        if _is_linear(ts.resolve(t.path, mode)) and _new_here(ts, t.path, mode):
            where, what = _where(ts, mode)
            eased = ("motion.curve.gentle" if "motion:reduced" in mode
                     else "an eased curve such as motion.curve.out")
            out.append(f"{t.path} is linear{where}; only motion.progress.curve loops, and a "
                       "one-shot move at an even pace reads mechanical, so point "
                       f"{what} at {eased}")
    return out


def _reduced_not_longer(ts: TokenSet, mode: str) -> List[str]:
    """Reduced motion never lengthens a role. The progress loop keeps its
    pace instead; progress-keeps-pace owns it."""
    if "motion:reduced" not in mode:
        return []
    out = []
    for path in _roles_with(ts, "duration"):
        reduced, standard = _ms(ts, path, mode), _ms(ts, path)
        if path == "motion.progress.duration" or reduced <= standard:
            continue
        raw = ts.raw(path)
        step = alias_target(raw) if is_alias(raw) else f"a duration of {standard:g}ms"
        out.append(f"{path} lasts {reduced:g}ms under reduced motion but {standard:g}ms in "
                   "standard; reduced motion never lengthens a move, so point its "
                   f"motion:reduced override at {step} or a shorter step")
    return out


def _progress_floor(ts: TokenSet, mode: str) -> List[str]:
    """The loop lasts at least LOOP_MIN_MS in every context. The floor is
    ours: WCAG 2.3.1 limits flashes, not durations, and a loop quicker than
    a third of a second is one that could flash more than three times a
    second. Under plain reduced motion a loop that differs from standard is
    progress-keeps-pace's finding, whose fix (drop the override) also
    clears this one."""
    p = "motion.progress.duration"
    if not _typed(ts, p) or not _new_here(ts, p, mode):
        return []
    ms = _ms(ts, p, mode)
    if ms >= LOOP_MIN_MS:
        return []
    if sparse(mode, ts.axes) == "motion:reduced" and ms != _ms(ts, p):
        return []
    longer = sorted((_ms(ts, t.path), t.path) for t in ts.tokens()
                    if t.layer == "primitive" and t.type == "duration"
                    and _ms(ts, t.path) >= LOOP_MIN_MS)
    step = longer[0][1] if longer else f"a duration of {LOOP_MIN_MS}ms"
    where, what = _where(ts, mode)
    return [f"{p} lasts {ms:g}ms{where}; our floor for a loop is {LOOP_MIN_MS}ms, since a "
            "shorter cycle repeats more than three times a second and a loop that flashes that "
            f"often falls under WCAG 2.3.1, so point {what} at {step} or a longer step"]


# Only removing travel is WCAG's (2.3.3, motion from interaction can be
# turned off); the length cap, the gentle curve, the still press, linear
# for the loop alone and the loop floor are this system's rules.
CHECKS: Tuple[Check, ...] = (
    Check("reduced-travel", "2.3.3", _reduced_travel, axes=("motion",)),
    Check("reduced-length", "system", _reduced_length, axes=("motion",)),
    Check("reduced-curve", "system", _reduced_curve, axes=("motion",)),
    Check("dismiss-faster", "system", _dismiss_faster),
    Check("progress-linear", "system", _progress_linear),
    Check("progress-keeps-pace", "system", _progress_pace, axes=("motion",)),
    Check("mirrored-motion", "system", _mirrored, axes=("direction",)),
    Check("press-in-place", "system", _press_in_place, axes=("motion", "direction")),
    Check("linear-progress-only", "system", _linear_progress_only, axes=("motion",)),
    Check("reduced-not-longer", "system", _reduced_not_longer, axes=("motion",)),
    Check("progress-floor", "system", _progress_floor, axes=("motion", "direction")),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_motion(axes)


FOUNDATION = Foundation(name="motion", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
