"""Motion foundation: durations, easing curves and travel distances, the
interaction roles that use them, a reduced-motion variant, and a sign that
mirrors horizontal travel under dir="rtl".

The motion axis sets pace and character: a still brand moves briefly with
plain curves, a kinetic one takes longer and may overshoot. Under
motion:reduced every role keeps its meaning but loses travel, overshoot
and length: distances drop to 0, curves turn gentle, durations cap at
REDUCED_MAX_MS (the progress loop keeps its pace, it reports status).
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations.foundation import BrandInputs, Foundation, Generated
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

DURATIONS_MS = (0, 50, 100, 150, 200, 250, 300, 400, 500, 800, 1200)
REDUCED_MAX_MS = 100
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


# role suffix -> (token type, what to point it at)
ROLE_TYPES: Dict[str, Tuple[str, str]] = {
    "duration": ("duration", "a motion.duration step, a duration like {value: 200, unit: ms}"),
    "curve": ("cubicBezier", "a motion.curve step, a cubicBezier like [0.4, 0, 0.6, 1]"),
    "distance": ("dimension", "a motion.distance step, a dimension like {value: 8, unit: px}"),
}
SIGN = "motion.inline-sign"
SIGN_TYPE = ("number", "motion.sign.forward or motion.sign.backward, a number like 1 or -1")


def _expected(path: str) -> Tuple[str, str]:
    return SIGN_TYPE if path == SIGN else ROLE_TYPES[path.rsplit(".", 1)[1]]


def _typed(ts: TokenSet, path: str) -> bool:
    """The typed accessor every check reads through: a role is read only
    when it exists with the type its suffix expects. A role of another type
    is reported once, by motion-role-types, and skipped by the others."""
    return ts.has(path) and ts.get(path).type == _expected(path)[0]


def _roles_with(ts: TokenSet, suffix: str) -> List[str]:
    return [f"{r}.{suffix}" for r in ROLES if _typed(ts, f"{r}.{suffix}")]


def _role_types(ts: TokenSet, mode: str) -> List[str]:
    paths = [f"{r}.{s}" for r in ROLES for s in ROLE_TYPES] + [SIGN]
    out = []
    for path in paths:
        if ts.has(path) and not _typed(ts, path):
            _, fix = _expected(path)
            out.append(f"{path} is a {ts.get(path).type}; point it at {fix}")
    return out


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


# Only removing travel is WCAG's (2.3.3, motion from interaction can be
# turned off); the length cap and the gentle curve are this system's rules.
CHECKS: Tuple[Check, ...] = (
    Check("motion-role-types", "system", _role_types),
    Check("reduced-travel", "2.3.3", _reduced_travel, axes=("motion",)),
    Check("reduced-length", "system", _reduced_length, axes=("motion",)),
    Check("reduced-curve", "system", _reduced_curve, axes=("motion",)),
    Check("dismiss-faster", "system", _dismiss_faster),
    Check("progress-linear", "system", _progress_linear),
    Check("progress-keeps-pace", "system", _progress_pace, axes=("motion",)),
    Check("mirrored-motion", "system", _mirrored, axes=("direction",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_motion(axes)


FOUNDATION = Foundation(name="motion", generate=_generate, checks=CHECKS)
