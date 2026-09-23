import itertools
import re

import pytest

import engine.foundations.color as color_module
from engine.foundations.color import PAIRINGS, SEMANTIC, generate_color
from engine.foundations.color_math import contrast, oklch_to_hex
from engine.foundations.ramp import STEPS, RampResult
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5,
                  formality=0.5, motion=0.5, type_personality=0.5)
SEEDS = ["#6B4423", "#3366FF", "#E61428", "#FFD400", "#1F9D55", "#7C3AED"]


@pytest.mark.parametrize("seed", SEEDS)
def test_every_pairing_passes_in_every_mode(seed):
    ts = generate_color(AXES, seed).tokens
    for p in PAIRINGS:
        for mode in ts.mode_names:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= p.minimum, f"{p.fg} on {p.bg} ({mode}) = {ratio:.2f}"


def test_every_role_exists_and_aliases_a_primitive():
    ts = generate_color(AXES, "#3366FF").tokens
    for role in SEMANTIC:
        tok = ts.get(role)
        assert tok.layer == "semantic" and tok.value.startswith("{color.")
        assert ts.get(tok.value[1:-1]).layer == "primitive"


def test_primitives_never_carry_modes():
    ts = generate_color(AXES, "#3366FF").tokens
    assert all(not t.modes for t in ts.tokens() if t.layer == "primitive")


def test_brand_seed_is_action_primary_when_it_passes():
    ts = generate_color(AXES, "#1D4ED8").tokens
    assert ts.resolve("color.action.primary", "light") == "#1D4ED8"


def test_light_brand_gets_retuned_with_notes():
    r = generate_color(AXES, "#FFD400")
    assert r.notes, "a yellow brand cannot carry white text at 4.5:1 without a retune"


def test_deterministic():
    a = [(t.path, t.value, t.modes) for t in generate_color(AXES, "#E61428").tokens.tokens()]
    b = [(t.path, t.value, t.modes) for t in generate_color(AXES, "#E61428").tokens.tokens()]
    assert a == b


def test_raises_when_a_pairing_cannot_be_satisfied(monkeypatch):
    # R16 item 1: force the brand ramp flat (every stop the same gray) so no
    # amount of retuning can ever change any contrast ratio computed from it.
    # The retune loop's own guards ("if not nxt: break", "if not moved:
    # break") are built for exactly this: a move that legitimately does
    # nothing. generate_color must not return a system that silently fails
    # one of its own pairings; it must raise, naming the pairing.
    real_ramp = color_module.ramp
    brand = "#3366FF"
    flat = RampResult(stops={s: "#808080" for s in STEPS}, retuned=False, note="")

    def fake_ramp(seed_hex):
        if seed_hex.upper() == brand:
            return flat
        return real_ramp(seed_hex)

    monkeypatch.setattr(color_module, "ramp", fake_ramp)

    with pytest.raises(ValueError) as excinfo:
        generate_color(AXES, brand)

    message = str(excinfo.value)
    assert "on" in message and ":1" in message
    assert any(p.fg in message and p.bg in message for p in PAIRINGS), (
        "the error must name the failing pairing's foreground and background")


_NOTE_RATIO_RE = re.compile(r":\d")


@pytest.mark.parametrize("seed", ["#FFD400", "#6B4423"])
def test_notes_are_complete(seed):
    # R16 item 2: every note the retune loop (generate_color, not ramp())
    # writes must be traceable back to a specific role, in a specific mode,
    # moving between two full primitive paths, for a ratio that was
    # measured. Filtered to notes carrying "(light)"/"(dark)": that marker
    # is exactly what separates a retune-loop note from _primitives' own
    # "color.<family>: <seed> is too light/dark..." ramp-anchor note (a
    # different, mode-independent kind of note, owned by ramp.py's Task 3
    # format, not this task's retune bookkeeping).
    r = generate_color(AXES, seed)
    retune_notes = [n for n in r.notes if "(light)" in n or "(dark)" in n]
    assert retune_notes, f"{seed}: expected at least one retune-loop note"
    for note in retune_notes:
        assert "(light)" in note or "(dark)" in note, note
        assert "->" in note, note
        assert note.count("color.") >= 2, note
        assert ":1" in note and _NOTE_RATIO_RE.search(note), note


@pytest.mark.parametrize("seed", SEEDS)
def test_hover_differs_from_primary(seed):
    # R16 item 3: action.primary-hover must read as a different color from
    # action.primary in both modes, and every pairing must still pass after
    # the distinctness fix-up runs.
    ts = generate_color(AXES, seed).tokens
    for mode in ts.mode_names:
        primary = ts.resolve("color.action.primary", mode)
        hover = ts.resolve("color.action.primary-hover", mode)
        assert primary != hover, f"{seed}: primary == hover ({mode}) = {primary}"
    for p in PAIRINGS:
        for mode in ts.mode_names:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= p.minimum, f"{seed}: {p.fg} on {p.bg} ({mode}) = {ratio:.2f}"


# R16 item 5: a fast, broad sweep independent of the six brief seeds. Every
# 30 degrees of hue, three lightnesses, two chromas, plus three flat grays.
_SWEEP_HUES = range(0, 360, 30)
_SWEEP_LS = (0.35, 0.55, 0.75)
_SWEEP_CS = (0.05, 0.15)
_SWEEP_SEEDS = [oklch_to_hex(L, C, float(H))
                for H, L, C in itertools.product(_SWEEP_HUES, _SWEEP_LS, _SWEEP_CS)]
_SWEEP_SEEDS += ["#202020", "#808080", "#E0E0E0"]


@pytest.mark.parametrize("seed", _SWEEP_SEEDS)
def test_sweep_pairings_pass_and_hover_is_distinct(seed):
    ts = generate_color(AXES, seed).tokens
    for p in PAIRINGS:
        for mode in ts.mode_names:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= p.minimum, f"{seed}: {p.fg} on {p.bg} ({mode}) = {ratio:.2f}"
    for mode in ts.mode_names:
        assert ts.resolve("color.action.primary", mode) != ts.resolve("color.action.primary-hover", mode), \
            f"{seed}: primary == hover ({mode})"
