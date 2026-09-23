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


def test_raises_when_the_action_group_ramp_is_flat(monkeypatch):
    # R16 item 1 / R17 item (c): force the brand ramp flat (every stop the
    # same gray) so no amount of retuning can ever change any contrast
    # ratio computed from it, and action.primary-hover can never read as a
    # different color from action.primary either. generate_color must not
    # return a system with an invisible hover state or a silently-failing
    # pairing; it must raise, naming the action group and the mode.
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
    assert "action group" in message
    assert "(light)" in message or "(dark)" in message
    assert "color.action.primary" in message and "color.action.primary-hover" in message


def test_raises_with_best_ratios_when_the_action_group_is_unsatisfiable(monkeypatch):
    # R17 item (b): a ramp that varies (so it is not the flat/hover-collision
    # case above) but never leaves the near-white end can never clear
    # action.primary's or action.primary-hover's 3:1 against a light page,
    # no matter which of its 11 (distinct) steps the solver tries. The
    # raise must name the action group, the mode, and the best ratios it
    # actually reached, per the R17 ruling's wording.
    real_ramp = color_module.ramp
    brand = "#3366FF"
    steps = list(STEPS)
    narrow = RampResult(
        stops={s: oklch_to_hex(0.99 - i * 0.01, 0.0, 0.0) for i, s in enumerate(steps)},
        retuned=False, note="")

    def fake_ramp(seed_hex):
        if seed_hex.upper() == brand:
            return narrow
        return real_ramp(seed_hex)

    monkeypatch.setattr(color_module, "ramp", fake_ramp)

    with pytest.raises(ValueError) as excinfo:
        generate_color(AXES, brand)

    message = str(excinfo.value)
    assert "action group (light)" in message
    assert "color.action.primary" in message and "color.action.primary-hover" in message
    assert "color.text.on-action" in message
    # the four ratios the ruling asks for, each to two decimals
    assert len(re.findall(r"\d+\.\d\d:1", message)) == 4


# R17 minor: pinned to the exact field shapes each note format uses, not
# just "a colon followed by a digit somewhere" (":\d" would also match a
# mangled "was X:15" with the wrong number of decimals, or survive a
# mutant that drops "now X:1" entirely as long as some other colon-digit
# remained). A full path is pinned as "color.<segment> -> color.<segment>"
# so a mutant that shortens either side to a bare family or step number
# fails it too.
_PATH_MOVE_RE = re.compile(r"color\.\S+ -> color\.\S+")
_WAS_RATIO_RE = re.compile(r"was \d+\.\d\d:1")
_NOW_RATIO_RE = re.compile(r"now \d+\.\d\d:1")
_BARE_RATIO_RE = re.compile(r"\d+\.\d\d:1")


@pytest.mark.parametrize("seed", ["#FFD400", "#6B4423"])
def test_notes_are_complete(seed):
    # R16 item 2 / R17 minor: every note the retune loop (generate_color,
    # not ramp()) writes must be traceable back to a specific role, in a
    # specific mode, moving between two full primitive paths, for a ratio
    # that was measured and a ratio it achieved. Filtered to notes carrying
    # "(light)"/"(dark)": that marker is exactly what separates a
    # retune-loop note from _primitives' own "color.<family>: <seed> is too
    # light/dark..." ramp-anchor note (a different, mode-independent kind
    # of note, owned by ramp.py's Task 3 format, not this task's retune
    # bookkeeping).
    #
    # Two note shapes exist: phase 1's ordinary one-pairing move ("<role>
    # (<mode>): <old> -> <new>, ... was X:1, now Y:1, needs Z:1 (<criterion>)")
    # and the R17 action-group solver's single per-mode summary ("action
    # group (<mode>): <role> <old> -> <new>, <role> <old> -> <new>, <role>
    # <old> -> <new>, on-action/primary A:1, on-action/hover B:1,
    # primary/page C:1, hover/page D:1"), which reports four achieved
    # ratios instead of a single was/now pair.
    r = generate_color(AXES, seed)
    retune_notes = [n for n in r.notes if "(light)" in n or "(dark)" in n]
    assert retune_notes, f"{seed}: expected at least one retune-loop note"
    for note in retune_notes:
        assert "(light)" in note or "(dark)" in note, note
        assert _PATH_MOVE_RE.search(note), note
        if note.startswith("action group ("):
            assert note.count("color.") >= 6, note  # 3 roles x (old, new)
            assert len(_BARE_RATIO_RE.findall(note)) == 4, note
        else:
            assert _WAS_RATIO_RE.search(note), note
            assert _NOW_RATIO_RE.search(note), note


@pytest.mark.parametrize("seed", SEEDS)
def test_hover_differs_from_primary(seed):
    # R16 item 3 / R17: action.primary-hover must read as a different color
    # from action.primary in both modes, must itself clear 3:1 against the
    # page (R17 item a: PAIRINGS now has an entry for this, so the loop
    # below already covers it; asserted directly too so the guarantee is
    # named, not just implied by iterating PAIRINGS), and every pairing
    # must still pass after the action-group solver runs.
    ts = generate_color(AXES, seed).tokens
    for mode in ts.mode_names:
        primary = ts.resolve("color.action.primary", mode)
        hover = ts.resolve("color.action.primary-hover", mode)
        page = ts.resolve("color.surface.page", mode)
        assert primary != hover, f"{seed}: primary == hover ({mode}) = {primary}"
        assert contrast(hover, page) >= 3.0, \
            f"{seed}: hover on page ({mode}) = {contrast(hover, page):.2f}"
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
        primary = ts.resolve("color.action.primary", mode)
        hover = ts.resolve("color.action.primary-hover", mode)
        page = ts.resolve("color.surface.page", mode)
        assert primary != hover, f"{seed}: primary == hover ({mode})"
        # R17: hover must stay usable (>= 3:1 against the page) even when
        # phase 3's old nudge-only fix would have satisfied on-action while
        # letting the hover fill nearly disappear.
        assert contrast(hover, page) >= 3.0, \
            f"{seed}: hover on page ({mode}) = {contrast(hover, page):.2f}"
