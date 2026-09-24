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


def _roles_with(ts: TokenSet, suffix: str) -> List[str]:
    return [f"{r}.{suffix}" for r in ROLES if ts.has(f"{r}.{suffix}")]


def _reduced(ts: TokenSet, mode: str) -> List[str]:
    if "motion:reduced" not in mode:
        return []
    out = []
    for path in _roles_with(ts, "distance"):
        v = ts.resolve(path, mode)["value"]
        if v != 0:
            out.append(f"{path} travels {v:g}px under reduced motion; point its motion:reduced "
                       "override at motion.distance.0")
    for path in _roles_with(ts, "duration"):
        if path == "motion.progress.duration":
            continue
        v = ts.resolve(path, mode)
        ms = v["value"] * (1000 if v["unit"] == "s" else 1)
        if ms > REDUCED_MAX_MS:
            out.append(f"{path} lasts {ms:g}ms under reduced motion; cap it at "
                       f"{REDUCED_MAX_MS}ms with a motion:reduced override")
    for path in _roles_with(ts, "curve"):
        c = ts.resolve(path, mode)
        if not (0 <= c[1] <= 1 and 0 <= c[3] <= 1):
            out.append(f"{path} overshoots under reduced motion; point its motion:reduced "
                       "override at motion.curve.gentle")
    return out


def _ms(ts: TokenSet, path: str, mode: str = "") -> float:
    v = ts.resolve(path, mode)
    return v["value"] * (1000 if v["unit"] == "s" else 1)


def _dismiss_faster(ts: TokenSet, mode: str) -> List[str]:
    a, b = "motion.dismiss.duration", "motion.reveal.duration"
    if ts.has(a) and ts.has(b) and _ms(ts, a) >= _ms(ts, b):
        return [f"{a} ({_ms(ts, a):g}ms) is not shorter than {b} ({_ms(ts, b):g}ms); leaving "
                "should never hold the next action longer than arriving, so shorten it"]
    return []


def _progress_linear(ts: TokenSet, mode: str) -> List[str]:
    p = "motion.progress.curve"
    if ts.has(p) and ts.resolve(p) != LINEAR:
        return [f"{p} is {ts.resolve(p)}; a continuous loop must keep an even pace, so point "
                "it at motion.curve.linear"]
    return []


def _mirrored(ts: TokenSet, mode: str) -> List[str]:
    p = "motion.inline-sign"
    if not ts.has(p):
        return []
    want = -1 if "direction:rtl" in mode else 1
    got = ts.resolve(p, mode)
    if got == want:
        return []
    return [f"{p} ({mode}) is {got:g}; horizontal travel follows the reading direction, so it "
            f"must be {want} here"]


CHECKS: Tuple[Check, ...] = (
    Check("reduced-motion", "2.3.3", _reduced, axes=("motion",)),
    Check("dismiss-faster", "system", _dismiss_faster),
    Check("progress-linear", "system", _progress_linear),
    Check("mirrored-motion", "system", _mirrored, axes=("direction",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_motion(axes)


FOUNDATION = Foundation(name="motion", generate=_generate, checks=CHECKS)
