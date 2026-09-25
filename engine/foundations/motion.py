"""Motion foundation: durations, easing curves and travel distances, the
interaction roles that use them, a reduced-motion variant, and a sign that
mirrors horizontal travel under dir="rtl".

The motion axis sets pace, and character.overshoot (motion, held back by
formality) bends every curve continuously from plain to springy: a still,
formal brand moves briefly with plain curves, a kinetic, playful one takes
longer and overshoots. motion.expressive is the one role for decoration: a
reveal on scroll, a celebration. Under motion:reduced every role keeps its
meaning but loses travel, overshoot and length: distances drop to 0,
curves turn gentle, durations cap at REDUCED_MAX_MS and never grow (the
progress loop keeps its pace, it reports status), and the expressive role
is removed: 0ms and no travel. In every context a press confirms in place,
only the progress loop runs linear, and the loop lasts at least
LOOP_MIN_MS.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple

from engine.foundations import character
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
# The plain and the springy end of each curve (out, in, in-out, expressive);
# character.overshoot places every curve between them.
PLAIN = ([0.25, 0.1, 0.25, 1], [0.42, 0, 1, 1], [0.42, 0, 0.58, 1], [0.3, 0.7, 0.4, 1])
SPRINGY = ([0.34, 1.56, 0.64, 1], [0.36, 0, 0.66, -0.56], [0.68, -0.6, 0.32, 1.6],
           [0.3, 1.8, 0.5, 1])
# role -> (ms when the motion axis is 0, ms when it is 1, curve, distance step or None)
ROLES: Dict[str, Tuple[int, int, str, object]] = {
    "motion.press": (100, 100, "out", None),
    "motion.reveal": (150, 300, "out", 1),
    "motion.dismiss": (100, 200, "in", 1),
    "motion.swap": (150, 250, "in-out", None),
    "motion.expand": (200, 300, "in-out", None),
    "motion.page": (250, 500, "out", 2),
    "motion.progress": (1200, 800, "linear", None),
    # decoration: removed under reduced motion
    "motion.expressive": (300, 800, "expressive", 3),
}
EXPRESSIVE = "motion.expressive"


def curves(overshoot: float) -> List[List[float]]:
    """(out, in, in-out, expressive) at this overshoot, each control point
    interpolated between the plain and the springy curve."""
    return [[round(p + (s - p) * overshoot, 3) for p, s in zip(plain, springy)]
            for plain, springy in zip(PLAIN, SPRINGY)]


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
    o = character.overshoot(axes)
    out_curve, in_curve, in_out_curve, expressive = curves(o)
    for name, curve in (("linear", LINEAR), ("out", out_curve), ("in", in_curve),
                        ("in-out", in_out_curve), ("expressive", expressive), ("gentle", GENTLE)):
        ts.add(Token(f"motion.curve.{name}", "cubicBezier", list(curve)))
    unit = distance_unit(m)
    for step, mult in enumerate((0, 1, 2, 4)):
        ts.add(Token(f"motion.distance.{step}", "dimension", {"value": unit * mult, "unit": "px"}))
    ts.add(Token("motion.sign.forward", "number", 1))
    ts.add(Token("motion.sign.backward", "number", -1))

    for role, (_, _, curve, distance) in ROLES.items():
        ms = duration_ms(role, m)
        reduced_ms = ms if role == "motion.progress" else (
            0 if role == EXPRESSIVE else min(ms, REDUCED_MAX_MS))
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
    return Generated(tokens=ts, notes=[f"motion: overshoot {o:g} from motion {m:g} and formality "
                                       f"{axes.formality:g}, {unit}px travel step"])


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


def _standard(ts: TokenSet, mode: str) -> str:
    """The same context with motion set back to standard."""
    return join({**parse(mode, ts.axes), "motion": "standard"}, ts.axes)


def _seen_ltr(ts: TokenSet, mode: str, read: Callable[[str], Any]) -> bool:
    """True in a right-to-left context whose reading equals the same
    context read left to right: a failure there is already reported there,
    so it is not repeated. A reading that differs is a new finding."""
    pairs = parse(mode, ts.axes)
    ltr = ts.axes["direction"][0]
    if pairs.get("direction", ltr) == ltr:
        return False
    return read(join({**pairs, "direction": ltr}, ts.axes)) == read(mode)


def _reduced_where(ts: TokenSet, mode: str) -> Tuple[str, str]:
    """(how a message names a reduced context, the override key to fix):
    ("reduced motion", "motion:reduced") for plain reduced motion, the
    context key twice otherwise."""
    key = sparse(mode, ts.axes)
    return ("reduced motion", key) if key == "motion:reduced" else (key, key)


def _reduced_travel(ts: TokenSet, mode: str) -> List[str]:
    if "motion:reduced" not in mode:
        return []
    under, key = _reduced_where(ts, mode)
    out = []
    for path in _roles_with(ts, "distance"):
        v = ts.resolve(path, mode)
        if v["value"] != 0 and not _seen_ltr(ts, mode, lambda m: ts.resolve(path, m)):
            out.append(f"{path} travels {v['value']:g}{v['unit']} under {under}; point its "
                       f"{key} override at motion.distance.0")
    return out


# The roles whose reduced duration another check owns: the progress loop
# keeps its pace (progress-keeps-pace) and decoration is removed
# (expressive-removed).
OWN_REDUCED_DURATION = ("motion.progress.duration", f"{EXPRESSIVE}.duration")


def _reduced_length(ts: TokenSet, mode: str) -> List[str]:
    """A one-shot role past the cap under reduced motion. The cap it names is
    the lower of REDUCED_MAX_MS and the role's standard length in the same
    direction, so the one fix also keeps reduced motion from lengthening
    the move; reduced-not-longer does not repeat it."""
    if "motion:reduced" not in mode:
        return []
    under, key = _reduced_where(ts, mode)
    out = []
    for path in _roles_with(ts, "duration"):
        ms = _ms(ts, path, mode)
        if path in OWN_REDUCED_DURATION or ms <= REDUCED_MAX_MS \
                or _seen_ltr(ts, mode, lambda m: _ms(ts, path, m)):
            continue
        standard = _ms(ts, path, _standard(ts, mode))
        cap = (f"{standard:g}ms, its standard length," if standard < REDUCED_MAX_MS
               else f"{REDUCED_MAX_MS}ms")
        out.append(f"{path} lasts {ms:g}ms under {under}; cap it at {cap} with a {key} override")
    return out


def _overshoots(curve: List[float]) -> bool:
    return not (0 <= curve[1] <= 1 and 0 <= curve[3] <= 1)


def _reduced_curve(ts: TokenSet, mode: str) -> List[str]:
    if "motion:reduced" not in mode:
        return []
    under, key = _reduced_where(ts, mode)
    return [f"{path} overshoots under {under}; point its {key} override at motion.curve.gentle"
            for path in _roles_with(ts, "curve")
            if _overshoots(ts.resolve(path, mode))
            and not _seen_ltr(ts, mode, lambda m: ts.resolve(path, m))]


def _dismiss_faster(ts: TokenSet, mode: str) -> List[str]:
    """Leaving is shorter than arriving. Under reduced motion both cap at
    the same length, so a tie passes there, but a dismiss longer than the
    reveal still fails. A reading already reported in the left-to-right or
    the standard-motion context is not repeated."""
    a, b = "motion.dismiss.duration", "motion.reveal.duration"
    if not (_typed(ts, a) and _typed(ts, b)):
        return []

    def read(m: str) -> Tuple[float, float]:
        return _ms(ts, a, m), _ms(ts, b, m)

    da, db = read(mode)
    reduced = "motion:reduced" in mode
    if (da <= db if reduced else da < db) or _seen_ltr(ts, mode, read):
        return []
    if reduced and da > REDUCED_MAX_MS:
        return []  # reduced-length's finding; its cap lets the two tie
    if reduced and read(_standard(ts, mode)) == (da, db):
        return []
    key = sparse(mode, ts.axes)
    if reduced:
        return [f"{a} ({da:g}ms) is longer than {b} ({db:g}ms) under {key}; reduced motion may "
                "let the two tie but never lets leaving outlast arriving, so shorten "
                f"{a} under {key}"]
    if not key:
        return [f"{a} ({da:g}ms) is not shorter than {b} ({db:g}ms); leaving should never hold "
                "the next action longer than arriving, so shorten it"]
    return [f"{a} ({da:g}ms) is not shorter than {b} ({db:g}ms) under {key}; leaving should "
            f"never hold the next action longer than arriving, so shorten {a} under {key}"]


def _progress_linear(ts: TokenSet, mode: str) -> List[str]:
    """The loop runs linear in every direction. Under reduced motion it
    keeps its standard curve, which progress-keeps-pace checks against the
    same direction, so this check reports the standard contexts only."""
    p = "motion.progress.curve"
    if not _typed(ts, p) or "motion:reduced" in mode:
        return []
    curve = ts.resolve(p, mode)
    if curve == LINEAR or _seen_ltr(ts, mode, lambda m: ts.resolve(p, m)):
        return []
    where, what = _where(ts, mode)
    return [f"{p} is {curve}{where}; a continuous loop must keep an even pace, so point {what} "
            "at motion.curve.linear"]


def _progress_pace(ts: TokenSet, mode: str) -> List[str]:
    """Under reduced motion the progress loop keeps the duration and curve
    it has with standard motion in the same direction: it reports status,
    so slowing or easing it misleads. A curve that is already wrong with
    standard motion is progress-linear's finding, not repeated here."""
    if "motion:reduced" not in mode:
        return []
    std = _standard(ts, mode)
    under, key = _reduced_where(ts, mode)
    std_where = "in standard" if key == "motion:reduced" else f"under {sparse(std, ts.axes)}"
    out = []
    d = "motion.progress.duration"
    if _typed(ts, d):
        reduced, standard = _ms(ts, d, mode), _ms(ts, d, std)
        if reduced != standard and not _seen_ltr(
                ts, mode, lambda m: (_ms(ts, d, m), _ms(ts, d, _standard(ts, m)))):
            out.append(f"{d} lasts {reduced:g}ms under {under} but {standard:g}ms {std_where}; "
                       f"a status loop keeps its pace, so drop its {key} override")
    c = "motion.progress.curve"
    if _typed(ts, c):
        curve = ts.resolve(c, mode)
        if curve != LINEAR and curve != ts.resolve(c, std) and not _seen_ltr(
                ts, mode, lambda m: (ts.resolve(c, m), ts.resolve(c, _standard(ts, m)))):
            out.append(f"{c} is {curve} under {under}; a status loop keeps an even pace, so "
                       f"drop its {key} override and keep motion.curve.linear")
    return out


def _mirrored(ts: TokenSet, mode: str) -> List[str]:
    """The sign follows the reading direction whatever the motion setting.
    Under reduced motion a value it already has with standard motion is
    reported there, not repeated."""
    p = SIGN
    if not _typed(ts, p):
        return []
    want = -1 if "direction:rtl" in mode else 1
    got = ts.resolve(p, mode)
    if got == want or ("motion:reduced" in mode and ts.resolve(p, _standard(ts, mode)) == got):
        return []
    label = sparse(mode, ts.axes) or "direction:ltr"
    return [f"{p} ({label}) is {got:g}; horizontal travel follows the reading direction, so it "
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
    context. Under reduced motion, reduced-travel already names a
    travelling press role, so it is not repeated."""
    owned = set(_roles_with(ts, "distance")) if "motion:reduced" in mode else set()
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
    """Reduced motion never lengthens a role: each reduced duration is
    compared with the standard one in the same direction. A pair already
    seen in the left-to-right context is not repeated. The progress loop
    keeps its pace instead (progress-keeps-pace), the expressive role is
    removed (expressive-removed), and a duration past the cap is
    reduced-length's finding, whose fix clears this one."""
    if "motion:reduced" not in mode:
        return []
    std = _standard(ts, mode)
    base_dir = {**parse(mode, ts.axes), "direction": ts.axes["direction"][0]}
    ltr, ltr_std = join(base_dir, ts.axes), _standard(ts, join(base_dir, ts.axes))
    where = sparse(mode, ts.axes)
    std_where = sparse(std, ts.axes)
    out = []
    for path in _roles_with(ts, "duration"):
        reduced, standard = _ms(ts, path, mode), _ms(ts, path, std)
        if path in OWN_REDUCED_DURATION or reduced <= standard or reduced > REDUCED_MAX_MS:
            continue
        if ltr != mode and (_ms(ts, path, ltr), _ms(ts, path, ltr_std)) == (reduced, standard):
            continue
        raw = ts.raw(path, std)
        step = alias_target(raw) if is_alias(raw) else f"a duration of {standard:g}ms"
        if where == "motion:reduced":
            out.append(f"{path} lasts {reduced:g}ms under reduced motion but {standard:g}ms in "
                       "standard; reduced motion never lengthens a move, so point its "
                       f"motion:reduced override at {step} or a shorter step")
        else:
            out.append(f"{path} lasts {reduced:g}ms under {where} but {standard:g}ms under "
                       f"{std_where}; reduced motion never lengthens a move, so point its "
                       f"{where} override at {step} or a shorter step")
    return out


def _progress_floor(ts: TokenSet, mode: str) -> List[str]:
    """The loop lasts at least LOOP_MIN_MS in every context. The floor is
    ours: WCAG 2.3.1 limits flashes, not durations, and a loop quicker than
    a third of a second is one that could flash more than three times a
    second. Under reduced motion a loop that differs from standard motion
    in the same direction is progress-keeps-pace's finding, whose fix (drop
    the override) also clears this one."""
    p = "motion.progress.duration"
    if not _typed(ts, p) or not _new_here(ts, p, mode):
        return []
    ms = _ms(ts, p, mode)
    if ms >= LOOP_MIN_MS:
        return []
    if "motion:reduced" in mode and ms != _ms(ts, p, _standard(ts, mode)):
        return []
    longer = sorted((_ms(ts, t.path), t.path) for t in ts.tokens()
                    if t.layer == "primitive" and t.type == "duration"
                    and _ms(ts, t.path) >= LOOP_MIN_MS)
    step = longer[0][1] if longer else f"a duration of {LOOP_MIN_MS}ms"
    where, what = _where(ts, mode)
    return [f"{p} lasts {ms:g}ms{where}; our floor for a loop is {LOOP_MIN_MS}ms, since a "
            "shorter cycle repeats more than three times a second and a loop that flashes that "
            f"often falls under WCAG 2.3.1, so point {what} at {step} or a longer step"]


def _expressive_removed(ts: TokenSet, mode: str) -> List[str]:
    """Under reduced motion the expressive role does not run: it lasts 0ms.
    This is our rule, not WCAG's. Its travel is reduced-travel's finding
    (WCAG 2.3.3), not repeated here."""
    if "motion:reduced" not in mode:
        return []
    d = f"{EXPRESSIVE}.duration"
    if not _typed(ts, d) or _ms(ts, d, mode) == 0 or _seen_ltr(ts, mode, lambda m: _ms(ts, d, m)):
        return []
    under, key = _reduced_where(ts, mode)
    return [f"{d} lasts {_ms(ts, d, mode):g}ms under {under}; decoration is removed under "
            f"reduced motion, our rule, so point its {key} override at motion.duration.0"]


# Only removing travel is WCAG's (2.3.3, motion from interaction can be
# turned off); the length cap, the gentle curve, the still press, linear
# for the loop alone, the loop floor and removing decoration are this
# system's rules. Each property has one owner check, so a broken role gives
# one finding with one fix. Motion
# tokens vary on motion and direction, so every check reads both, and a
# right-to-left finding that repeats the left-to-right one is not repeated.
_BOTH = ("motion", "direction")
CHECKS: Tuple[Check, ...] = (
    Check("reduced-travel", "2.3.3", _reduced_travel, axes=_BOTH),
    Check("reduced-length", "system", _reduced_length, axes=_BOTH),
    Check("reduced-curve", "system", _reduced_curve, axes=_BOTH),
    Check("dismiss-faster", "system", _dismiss_faster, axes=_BOTH),
    Check("progress-linear", "system", _progress_linear, axes=_BOTH),
    Check("progress-keeps-pace", "system", _progress_pace, axes=_BOTH),
    Check("mirrored-motion", "system", _mirrored, axes=_BOTH),
    Check("press-in-place", "system", _press_in_place, axes=_BOTH),
    Check("linear-progress-only", "system", _linear_progress_only, axes=_BOTH),
    Check("reduced-not-longer", "system", _reduced_not_longer, axes=_BOTH),
    Check("progress-floor", "system", _progress_floor, axes=_BOTH),
    Check("expressive-removed", "system", _expressive_removed, axes=_BOTH),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_motion(axes)


FOUNDATION = Foundation(name="motion", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
