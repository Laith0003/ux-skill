import itertools

import pytest

from engine.foundations import ramp as ramp_module
from engine.foundations.color_math import hex_to_oklch, oklch_to_hex
from engine.foundations.ramp import ANCHOR, STEPS, ramp


@pytest.mark.parametrize("seed", ["#6B4423", "#3366FF", "#E61428", "#1F9D55", "#7C3AED"])
def test_anchor_is_the_seed(seed):
    r = ramp(seed)
    assert list(r.stops) == list(STEPS)
    assert r.stops[ANCHOR] == seed.upper() and not r.retuned


@pytest.mark.parametrize("seed", ["#6B4423", "#3366FF", "#FFE066", "#0B1020"])
def test_lightness_strictly_decreases(seed):
    ls = [hex_to_oklch(h)[0] for h in ramp(seed).stops.values()]
    assert all(a > b for a, b in zip(ls, ls[1:]))


@pytest.mark.parametrize("seed", ["#FFE066", "#0B1020"])
def test_extreme_seed_is_retuned_with_a_note(seed):
    r = ramp(seed)
    assert r.retuned and seed.upper() in r.note and r.stops[ANCHOR] != seed.upper()


def test_deterministic():
    assert ramp("#3366FF").stops == ramp("#3366FF").stops


def test_malformed_hex_raises_value_error():
    with pytest.raises(ValueError):
        ramp("#12345")


# Fix round 1 (controller ruling R14)


def test_anchor_is_normalized_to_canonical_uppercase_hex():
    assert ramp("#36f").stops[ANCHOR] == "#3366FF"
    assert ramp("3366ff").stops[ANCHOR] == "#3366FF"
    assert ramp(" #3366FF").stops[ANCHOR] == "#3366FF"


def test_in_band_seed_ramp_is_unchanged_by_the_min_step_widening():
    # Captured from the pre-fix implementation before MIN_STEP was added, to
    # prove an in-band seed with room on both sides of the band still uses
    # the plain L_TOP / L_BOTTOM constants after the fix.
    r = ramp("#3366FF")
    assert r.stops == {
        50: "#F3F7FF",
        100: "#CCDCFF",
        200: "#A5C2FF",
        300: "#7FA6FF",
        400: "#5888FF",
        500: "#3366FF",
        600: "#234ED9",
        700: "#1336B4",
        800: "#071D90",
        900: "#03006D",
        950: "#01003B",
    }


def test_note_reports_chroma_reduced_when_the_delivered_500_loses_chroma():
    r = ramp("#FFFF00")
    assert r.retuned
    assert "chroma reduced to fit sRGB" in r.note
    assert "same hue and chroma" not in r.note


_SWEEP_HUES = range(0, 360, 15)
_SWEEP_LS = (0.10, 0.20, 0.30, 0.50, 0.80, 0.90, 0.97)
_SWEEP_CS = (0.02, 0.10, 0.20)


def test_min_step_sweep_keeps_intended_lightness_apart(monkeypatch):
    # The algorithm's own guarantee, at full precision, proved against the
    # real ramp() rather than a reimplementation of its formula: patch
    # ramp_module.oklch_to_hex with a wrapper that records the L each call
    # was asked to render and then delegates to the real function, so the
    # ramp is still built correctly. ramp() calls this once per non-anchor
    # step, in STEPS order with 500 skipped; a retuned seed also calls it
    # once more, before the loop, to build the anchor itself. Reassembling
    # the recorded Ls back into STEPS order and diffing adjacent pairs
    # tests exactly what ramp() computed, at full float precision, with no
    # hex quantization in the way. A failure here means the widening
    # formula itself is wrong, not that hex rounding ate the margin.
    real_oklch_to_hex = ramp_module.oklch_to_hex
    calls = []

    def recording_oklch_to_hex(L, C, H):
        calls.append(L)
        return real_oklch_to_hex(L, C, H)

    monkeypatch.setattr(ramp_module, "oklch_to_hex", recording_oklch_to_hex)

    failures = []
    for h, l, c in itertools.product(_SWEEP_HUES, _SWEEP_LS, _SWEEP_CS):
        seed = oklch_to_hex(l, c, h)
        calls.clear()
        r = ramp(seed)
        if r.retuned:
            # The anchor's own oklch_to_hex(L, C, H) call happens before
            # the loop, so it is recorded first; the other ten follow in
            # STEPS order with 500 skipped.
            assert len(calls) == 11, f"{seed}: expected 11 calls, got {len(calls)}"
            anchor_L, rest = calls[0], calls[1:]
        else:
            # In-band seeds never call oklch_to_hex for the anchor: its
            # stop is the seed's own hex, verbatim, so its L is read back
            # off that hex instead (an exact match for the "L" ramp()
            # computed internally, not an approximation: the seed hex was
            # never quantized a second time).
            assert len(calls) == 10, f"{seed}: expected 10 calls, got {len(calls)}"
            anchor_L, rest = hex_to_oklch(r.stops[ANCHOR])[0], calls
        ls = rest[:5] + [anchor_L] + rest[5:]
        assert len(ls) == len(STEPS)
        for i in range(len(ls) - 1):
            gap = ls[i] - ls[i + 1]
            if gap < ramp_module.MIN_STEP - 1e-9:
                failures.append((seed, h, l, c, STEPS[i], STEPS[i + 1], gap))
    assert not failures, f"{len(failures)} intended gaps under MIN_STEP: {failures[:10]}"


# Delivered-hex tolerance for 8-bit quantization noise. Measured directly:
# sweeping every hue (0-345 by 15), L in (0.10, 0.20, 0.30, 0.50, 0.80, 0.90,
# 0.97) and C in (0.02, 0.10, 0.20) and reading the actual OKLCH L back off
# each delivered hex stop, the worst observed gap was 0.031455 against an
# intended 0.035 (seed #183700, steps 800-900), a deviation of 0.003545. All
# 383 sub-0.034 gaps in that sweep sit only at the six boundary L values
# (0.10, 0.20, 0.30, 0.80, 0.90, 0.97), never at 0.50, which is exactly where
# the widening formula pins the nominal gap to precisely MIN_STEP (0.035)
# with no headroom to spare before 8-bit hex rounding. This bound (0.031, a
# hair under the measured worst case) exists only to catch a REGRESSION back
# toward the original 0.028 crush; it is not a substitute for the strict,
# zero-tolerance check above (which now calls the real ramp() through a
# recording patch on oklch_to_hex, not a reimplementation of its formula).
_DELIVERED_MIN_GAP = 0.031


def test_min_step_sweep_delivered_hex_stays_within_rounding_tolerance():
    gap_failures = []
    duplicate_failures = []
    for h, l, c in itertools.product(_SWEEP_HUES, _SWEEP_LS, _SWEEP_CS):
        seed = oklch_to_hex(l, c, h)
        r = ramp(seed)
        hexes = [r.stops[s] for s in STEPS]
        ls = [hex_to_oklch(hx)[0] for hx in hexes]
        for i in range(len(ls) - 1):
            gap = ls[i] - ls[i + 1]
            if gap < _DELIVERED_MIN_GAP:
                gap_failures.append((seed, h, l, c, STEPS[i], STEPS[i + 1], gap))
            if hexes[i] == hexes[i + 1]:
                duplicate_failures.append((seed, h, l, c, STEPS[i], STEPS[i + 1], hexes[i]))
    assert not gap_failures, f"{len(gap_failures)} gaps under {_DELIVERED_MIN_GAP}: {gap_failures[:10]}"
    assert not duplicate_failures, f"{len(duplicate_failures)} duplicate adjacent stops: {duplicate_failures[:10]}"
