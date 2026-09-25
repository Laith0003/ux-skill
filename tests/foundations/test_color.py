import itertools
import re

import pytest

import engine.foundations.color as color_module
from engine.foundations.build import build_color
from engine.foundations.color import COLOR_CONTEXTS, PAIRINGS, SEMANTIC, generate_color
from engine.foundations.color_math import contrast, oklch_to_hex
from engine.foundations.gate import GateFailure, required
from engine.foundations.ramp import STEPS, RampResult
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5,
                  formality=0.5, motion=0.5, type_personality=0.5)
SEEDS = ["#6B4423", "#3366FF", "#E61428", "#FFD400", "#1F9D55", "#7C3AED"]


@pytest.mark.parametrize("seed", SEEDS)
def test_every_pairing_passes_in_every_mode(seed):
    ts = generate_color(AXES, seed).tokens
    for p in PAIRINGS:
        for mode in COLOR_CONTEXTS:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= required(p, mode)[0], f"{p.fg} on {p.bg} ({mode}) = {ratio:.2f}"


# R16 item 5: a fast, broad sweep independent of the six brief seeds. Every
# 30 degrees of hue, three lightnesses, two chromas, plus three flat grays.
_SWEEP_HUES = range(0, 360, 30)
_SWEEP_LS = (0.35, 0.55, 0.75)
_SWEEP_CS = (0.05, 0.15)
_SWEEP_SEEDS = [oklch_to_hex(L, C, float(H))
                for H, L, C in itertools.product(_SWEEP_HUES, _SWEEP_LS, _SWEEP_CS)]
_SWEEP_SEEDS += ["#202020", "#808080", "#E0E0E0"]


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
    assert ts.raw("color.action.primary", "light") == "{color.brand.exact}"


@pytest.mark.parametrize("seed", SEEDS + ["#E85D04", "#0F766E", "#6D28D9", "#2563EB"])
def test_the_exact_brand_is_the_light_fill_whenever_either_text_color_reads(seed):
    ts = generate_color(AXES, seed).tokens
    exact = seed.upper()
    light = "scheme:light,contrast:standard"
    readable = max(contrast(exact, "#FFFFFF"), contrast(exact, "#000000")) >= 4.5
    assert (ts.resolve("color.action.primary", light) == exact) == readable
    assert ts.resolve("color.brand.exact") == exact


def test_an_orange_brand_keeps_its_color_with_black_text_in_light():
    ts = generate_color(AXES, "#E85D04").tokens
    light = "scheme:light,contrast:standard"
    assert ts.resolve("color.action.primary", light) == "#E85D04"
    assert ts.resolve("color.text.on-action", light) == "#000000"
    # black text keeps reading, so hover and pressed step away from it
    assert ts.raw("color.action.primary-hover", light) == "{color.brand.400}"
    assert ts.raw("color.action.primary-pressed", light) == "{color.brand.300}"


@pytest.mark.parametrize("seed", SEEDS + _SWEEP_SEEDS)
def test_dark_and_high_contrast_never_put_black_text_on_a_mid_tone_fill(seed):
    from engine.foundations.color_math import hex_to_oklch
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS[1:]:
        fill = ts.resolve("color.action.primary", mode)
        if ts.resolve("color.text.on-action", mode) == "#000000":
            assert hex_to_oklch(fill)[0] >= color_module.MUDDY_L, f"{seed} ({mode}) {fill}"


@pytest.mark.parametrize("seed", SEEDS)
def test_the_primary_edge_clears_the_page_and_equals_the_fill_when_the_fill_does(seed):
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        fill, edge = (ts.resolve(r, mode) for r in ("color.action.primary",
                                                     "color.action.primary-edge"))
        page = ts.resolve("color.surface.page", mode)
        need = 4.5 if "contrast:high" in mode else 3.0
        assert contrast(edge, page) >= need, f"{seed} ({mode})"
        if contrast(fill, page) >= need:
            assert edge == fill, f"{seed} ({mode})"


def test_light_brand_gets_retuned_with_notes():
    r = generate_color(AXES, "#FFD400")
    assert r.notes, "a yellow brand cannot carry white text at 4.5:1 without a retune"


def test_deterministic():
    a = [(t.path, t.value, t.modes) for t in generate_color(AXES, "#E61428").tokens.tokens()]
    b = [(t.path, t.value, t.modes) for t in generate_color(AXES, "#E61428").tokens.tokens()]
    assert a == b


def _brand_ramp(monkeypatch, brand, stops):
    real_ramp = color_module.ramp

    def fake_ramp(seed_hex):
        if seed_hex.upper() == brand:
            return RampResult(stops=stops, retuned=False, note="")
        return real_ramp(seed_hex)

    monkeypatch.setattr(color_module, "ramp", fake_ramp)


def test_flat_action_ramp_is_noted_and_the_gate_blocks_it(monkeypatch):
    # The generator never raises for an unsolvable fill group: it keeps
    # the defaults, notes why, and the build's gate blocks the result with
    # the states-distinct check naming the fix. The fill keeps the exact
    # brand color, so the two flat states collide with each other.
    brand = "#3366FF"
    _brand_ramp(monkeypatch, brand, {s: "#808080" for s in STEPS})
    result = generate_color(AXES, brand)
    assert any(n.startswith("color.action.primary group (scheme:light,contrast:standard): every "
                            "step of the brand ramp resolves to the same color")
               for n in result.notes)
    with pytest.raises(GateFailure) as exc:
        build_color(AXES, brand)
    failures = [f for f in exc.value.report.failures if f.check == "states-distinct"]
    assert failures and \
        "color.action.primary-pressed equals color.action.primary-hover" in failures[0].message
    assert "point color.action.primary-pressed at a neighboring step" in failures[0].message


def test_unsatisfiable_action_group_keeps_the_closest_and_the_gate_blocks_it(monkeypatch):
    # A near-white brand whose ramp never leaves the near-white end cannot
    # give the button an edge at 3:1 against a light page. The generator
    # keeps the closest candidate, its note carries the ratios reached, and
    # the gate names the failing pairing.
    brand = "#FAFAFA"
    _brand_ramp(monkeypatch, brand,
                {s: oklch_to_hex(0.99 - i * 0.01, 0.0, 0.0) for i, s in enumerate(STEPS)})
    notes = [n for n in generate_color(AXES, brand).notes
             if n.startswith("color.action.primary group (scheme:light,contrast:standard)")]
    assert len(notes) == 1 and "kept the closest" in notes[0]
    assert len(re.findall(r"\d+\.\d\d:1", notes[0])) == 3
    with pytest.raises(GateFailure) as exc:
        build_color(AXES, brand)
    assert any((f.fg, f.bg, f.mode) == ("color.action.primary-edge", "color.surface.page",
                                        "scheme:light,contrast:standard")
               for f in exc.value.report.findings)


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
    # "(scheme:light)"/"(scheme:dark)": that marker is exactly what separates a
    # retune-loop note from _primitives' own "color.<family>: <seed> is too
    # light/dark..." ramp-anchor note (a different, mode-independent kind
    # of note, owned by ramp.py's Task 3 format, not this task's retune
    # bookkeeping).
    #
    # Two note shapes exist: the ordinary one-pairing move ("<role>
    # (<mode>): <old> -> <new>, ... was X:1, now Y:1, <minimum and its
    # source>") and the fill-group solver's per-context summary ("<fill>
    # group (<mode>): <role> <old> -> <new>, ..., text/fill A:1, fill/page
    # B:1[, ring/surface C:1]"), which reports the ratios reached instead of
    # a single was/now pair.
    r = generate_color(AXES, seed)
    retune_notes = [n for n in r.notes if "(scheme:" in n]
    assert retune_notes, f"{seed}: expected at least one retune-loop note"
    for note in retune_notes:
        assert re.search(r"\(scheme:(light|dark),contrast:(standard|high)\)", note), note
        assert _PATH_MOVE_RE.search(note), note
        if re.match(r"color\.\S+ group \(", note):
            # a fill-group note lists only the roles that moved, then the
            # text/fill and fill/page ratios, and for the primary the ring's
            # lowest ratio against the surfaces it is checked on
            ratios = len(_BARE_RATIO_RE.findall(note))
            assert ratios == (3 if note.startswith("color.action.primary group") else 2), note
        else:
            assert _WAS_RATIO_RE.search(note), note
            assert _NOW_RATIO_RE.search(note), note


@pytest.mark.parametrize("seed", SEEDS)
def test_hover_differs_from_primary(seed):
    # action.primary-hover reads as a different color from action.primary in
    # every context, the primary edge clears the page (the fill and its
    # states need not), and every pairing still passes after the solver.
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        primary = ts.resolve("color.action.primary", mode)
        hover = ts.resolve("color.action.primary-hover", mode)
        edge = ts.resolve("color.action.primary-edge", mode)
        page = ts.resolve("color.surface.page", mode)
        assert primary != hover, f"{seed}: primary == hover ({mode}) = {primary}"
        assert contrast(edge, page) >= 3.0, \
            f"{seed}: edge on page ({mode}) = {contrast(edge, page):.2f}"
    for p in PAIRINGS:
        for mode in COLOR_CONTEXTS:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= required(p, mode)[0], f"{seed}: {p.fg} on {p.bg} ({mode}) = {ratio:.2f}"


@pytest.mark.parametrize("seed", _SWEEP_SEEDS)
def test_sweep_pairings_pass_and_hover_is_distinct(seed):
    ts = generate_color(AXES, seed).tokens
    for p in PAIRINGS:
        for mode in COLOR_CONTEXTS:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= required(p, mode)[0], f"{seed}: {p.fg} on {p.bg} ({mode}) = {ratio:.2f}"
    for mode in COLOR_CONTEXTS:
        primary = ts.resolve("color.action.primary", mode)
        hover = ts.resolve("color.action.primary-hover", mode)
        page = ts.resolve("color.surface.page", mode)
        assert primary != hover, f"{seed}: primary == hover ({mode})"
        edge = ts.resolve("color.action.primary-edge", mode)
        assert contrast(edge, page) >= 3.0, \
            f"{seed}: edge on page ({mode}) = {contrast(edge, page):.2f}"


def test_public_tables_are_immutable():
    # R27 M8: one caller's PAIRINGS.append or SEMANTIC[...] = ... used to
    # change the gate and the generator for the whole process.
    from types import MappingProxyType
    assert isinstance(PAIRINGS, tuple)
    assert isinstance(SEMANTIC, MappingProxyType)
    with pytest.raises(TypeError):
        SEMANTIC["color.text.extra"] = ("color.neutral.900", "color.neutral.50")


# The focus ring is picked with the primary fill group but never constrains
# the fill: the border foundation guarantees an offset, so page color sits
# between an element and its ring and the ring is measured against surfaces.

def test_new_pairings_are_declared():
    from engine.foundations.gate import Pairing
    for p in (Pairing("color.focus.ring", "color.surface.sunken", 3.0, "1.4.11"),
              Pairing("color.text.muted", "color.surface.sunken", 4.5, "1.4.3"),
              Pairing("color.text.link", "color.surface.sunken", 4.5, "1.4.3"),
              Pairing("color.status.danger.text", "color.surface.sunken", 4.5, "1.4.3")):
        assert p in PAIRINGS, p


def test_high_contrast_ring_never_weakens_and_is_checked(monkeypatch):
    ts = generate_color(AXES, "#3366FF").tokens
    for scheme in ("light", "dark"):
        std, high = f"scheme:{scheme},contrast:standard", f"scheme:{scheme},contrast:high"
        assert color_module._lowest(ts, "color.focus.ring", high)[0] >= \
            color_module._lowest(ts, "color.focus.ring", std)[0]
    assert color_module._ring_not_weaker(ts, "scheme:light,contrast:high") == []
    weak = generate_color(AXES, "#3366FF").tokens
    weak.get("color.focus.ring").modes["contrast:high"] = "{color.brand.600}"
    found = color_module._ring_not_weaker(weak, "scheme:light,contrast:high")
    assert found and "high contrast never weakens focus" in found[0]


def test_ring_is_not_paired_with_the_button_fill():
    fills = ("color.action.primary",) + color_module._FILL_STATES["color.action.primary"]
    assert not [p for p in PAIRINGS if p.fg == "color.focus.ring" and p.bg in fills]
    assert all(p.high is None for p in PAIRINGS if p.criterion != "system")


def test_ring_keeps_every_surface_pairing_at_its_minimum():
    from engine.foundations.gate import GateFinding, Pairing
    surfaces = ("color.surface.page", "color.surface.card", "color.surface.sunken",
                "color.surface.raised")
    for bg in surfaces:
        p = Pairing("color.focus.ring", bg, 3.0, "1.4.11")
        assert p in PAIRINGS, p
        assert required(p, "scheme:dark,contrast:standard") == (3.0, "1.4.11")
        assert required(p, "scheme:dark,contrast:high") == (4.5, "high-contrast floor over 1.4.11")
        std = GateFinding(p.fg, bg, "scheme:light,contrast:standard", 2.5,
                          *required(p, "scheme:light,contrast:standard")).message()
        high = GateFinding(p.fg, bg, "scheme:light,contrast:high", 4.2,
                           *required(p, "scheme:light,contrast:high")).message()
        assert "WCAG 1.4.11 needs 3:1" in std
        assert "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3:1)" in high
    assert Pairing("color.focus.ring-inverse", "color.surface.inverse", 3.0, "1.4.11") in PAIRINGS


@pytest.mark.parametrize("seed", SEEDS + _SWEEP_SEEDS)
def test_ring_stands_out_from_every_surface(seed):
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        need = 4.5 if "contrast:high" in mode else 3.0
        ring = ts.resolve("color.focus.ring", mode)
        for bg in ("color.surface.page", "color.surface.card", "color.surface.sunken",
                   "color.surface.raised"):
            assert contrast(ring, ts.resolve(bg, mode)) >= need, f"{seed} {bg} ({mode})"
        inverse = contrast(ts.resolve("color.focus.ring-inverse", mode),
                           ts.resolve("color.surface.inverse", mode))
        assert inverse >= need, f"{seed} ring-inverse ({mode})"


_GROUP_OUT = ("color.action.primary", "color.action.primary-hover",
              "color.action.primary-pressed", "color.text.on-action")


@pytest.mark.parametrize("seed", SEEDS + ["#00F1B0", "#291F18", "#FFFFFF", "#000000"])
def test_the_ring_never_moves_the_fill(seed, monkeypatch):
    # Whatever the ring may be, the fill, its states and its text come out
    # the same: the ring is chosen after them and constrains none of them.
    normal = generate_color(AXES, seed).tokens
    monkeypatch.setattr(color_module, "_ring_candidates",
                        lambda mode, default_ring: ["color.base.white", "color.base.black"])
    other = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        for role in _GROUP_OUT:
            assert other.raw(role, mode) == normal.raw(role, mode), f"{seed} {role} ({mode})"


# Hand-built brand ramps, grays by OKLCH lightness, read in the light
# standard context: page and card near white, sunken a light gray.
_LIGHT = "scheme:light,contrast:standard"


def _gray_ramp(monkeypatch, lightnesses):
    _brand_ramp(monkeypatch, "#3366FF",
                {s: oklch_to_hex(l, 0.0, 0.0) for s, l in zip(STEPS, lightnesses)})


def _group(ts):
    return tuple(ts.raw(r, _LIGHT)[1:-1] for r in _GROUP_OUT + ("color.action.primary-edge",
                                                                 "color.focus.ring"))


def test_solver_order_fill_distance_before_state_direction(monkeypatch):
    # The exact brand carries white text, but 600 and 700 are near white,
    # so hover and pressed cannot go the conventional (darker) way. The fill
    # stays and the states go lighter. An order that put the state
    # direction first would move the fill to keep darker states. The ring
    # takes the first brand step that clears every surface and stands 3:1
    # off the fill and the tinted fills: brand.950.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.43, 0.983, 0.983, 0.37, 0.31, 0.27])
    assert _group(generate_color(AXES, "#3366FF").tokens) == (
        "color.brand.exact", "color.brand.400", "color.brand.300", "color.base.white",
        "color.brand.exact", "color.brand.950")


def test_solver_order_conventional_direction_at_equal_distance(monkeypatch):
    # The exact brand carries white text; its states step the conventional
    # (darker) way, and the ring takes brand.950, the first step that also
    # stands 3:1 off the fill and the tinted fills.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.8, 0.43, 0.39, 0.34, 0.31, 0.27])
    assert _group(generate_color(AXES, "#3366FF").tokens) == (
        "color.brand.exact", "color.brand.600", "color.brand.700", "color.base.white",
        "color.brand.exact", "color.brand.950")


def test_ring_prefers_a_color_other_than_the_fill(monkeypatch):
    # With only white and the fill itself on offer, the ring takes white,
    # which differs from the fill, over a ring equal to the fill.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.43, 0.983, 0.983, 0.43, 0.31, 0.27])
    monkeypatch.setattr(color_module, "_ring_candidates",
                        lambda mode, default_ring: ["color.brand.exact", "color.neutral.950"])
    assert _group(generate_color(AXES, "#3366FF").tokens)[-1] == "color.neutral.950"


def test_the_fill_never_moves_to_make_the_ring_differ(monkeypatch):
    # When the only ring on offer is the fill itself, the ring equals the
    # fill; the fill does not move to make room.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.43, 0.983, 0.983, 0.37, 0.31, 0.27])
    monkeypatch.setattr(color_module, "_ring_candidates",
                        lambda mode, default_ring: ["color.brand.exact"])
    assert _group(generate_color(AXES, "#3366FF").tokens) == (
        "color.brand.exact", "color.brand.400", "color.brand.300", "color.base.white",
        "color.brand.exact", "color.brand.exact")


def test_ring_candidates_run_brand_then_neutral_then_black_and_white():
    light = color_module._ring_candidates(_LIGHT, "color.brand.700")
    assert light[:5] == ["color.brand.700", "color.brand.800", "color.brand.600",
                         "color.brand.900", "color.brand.500"]
    assert light[11:13] == ["color.neutral.950", "color.neutral.900"]
    assert light[-2:] == ["color.base.black", "color.base.white"]
    dark = color_module._ring_candidates("scheme:dark,contrast:standard", "color.brand.200")
    assert dark[:3] == ["color.brand.200", "color.brand.100", "color.brand.300"]
    assert dark[11:13] == ["color.neutral.50", "color.neutral.100"]
    assert dark[-2:] == ["color.base.white", "color.base.black"]
    assert len(light) == len(dark) == 2 * len(STEPS) + 2


def test_ring_prefers_a_brand_step():
    ts = generate_color(AXES, "#3366FF").tokens
    for mode in ("scheme:light,contrast:standard", "scheme:dark,contrast:standard"):
        assert ts.raw("color.focus.ring", mode).startswith("{color.brand."), mode


def test_ring_and_edge_moves_are_noted():
    # A yellow brand keeps its exact fill with black text; its edge moves to
    # brand.700 to clear the page, and the note says so with the edge and
    # ring ratios.
    notes = [n for n in generate_color(AXES, "#FFD400").notes
             if n.startswith("color.action.primary group (scheme:light,contrast:standard)")]
    assert len(notes) == 1
    assert ", color.action.primary color." not in notes[0] and ": color.action.primary color." \
        not in notes[0]
    assert "color.text.on-action color.base.white -> color.base.black" in notes[0]
    assert "color.action.primary-edge color.brand.exact -> color.brand.700" in notes[0]
    assert re.search(r"edge/page \d+\.\d\d:1, ring/surface \d+\.\d\d:1$", notes[0]), notes[0]


# High contrast: a variant per scheme with raised minimums.

def test_required_raises_minimums_only_in_high_contrast():
    from engine.foundations.gate import Pairing
    text = Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")
    part = Pairing("color.line.input", "color.surface.page", 3.0, "1.4.11")
    pinned = Pairing("color.x.fg", "color.x.bg", 3.0, "1.4.11", high=3.0)
    assert required(text, "scheme:dark,contrast:standard") == (4.5, "1.4.3")
    assert required(text, "scheme:dark,contrast:high") == (7.0, "1.4.6")
    assert required(part, "contrast:high") == (4.5, "high-contrast floor over 1.4.11")
    assert required(pinned, "contrast:high") == (3.0, "1.4.11")


@pytest.mark.parametrize("seed", SEEDS)
def test_high_contrast_starts_from_extreme_surfaces(seed):
    ts = generate_color(AXES, seed).tokens
    assert ts.resolve("color.surface.page", "scheme:light,contrast:high") == "#FFFFFF"
    assert ts.resolve("color.surface.page", "scheme:dark,contrast:high") == "#000000"
    for scheme in ("light", "dark"):
        high = contrast(ts.resolve("color.text.muted", f"scheme:{scheme},contrast:high"),
                        ts.resolve("color.surface.page", f"scheme:{scheme},contrast:high"))
        assert high >= 7.0


def test_high_contrast_variant_is_written_as_contrast_overrides():
    ts = generate_color(AXES, "#3366FF").tokens
    keys = {k for t in ts.tokens() for k in t.modes}
    assert {"scheme:dark", "contrast:high", "scheme:dark,contrast:high"} <= keys


# Messages cite only what WCAG says: 1.4.3 sets 4.5:1, 1.4.6 sets 7:1,
# 1.4.11 sets 3:1. The raised high-contrast non-text floor is ours, and
# 2.4.7 sets no ratio at all.
_WCAG_CLAIM_RE = re.compile(r"WCAG (\d+\.\d+\.\d+) (?:needs|asks) (\d+(?:\.\d+)?):1")
_WCAG_TRUE = {("1.4.3", 4.5), ("1.4.6", 7.0), ("1.4.11", 3.0)}


def _assert_cites_only_wcag(text):
    claims = _WCAG_CLAIM_RE.findall(text)
    assert claims, text
    for sc, ratio in claims:
        assert (sc, float(ratio)) in _WCAG_TRUE, text
    assert "2.4.7" not in text, text
    assert "(high contrast)" not in text, text


@pytest.mark.parametrize("mode", COLOR_CONTEXTS)
@pytest.mark.parametrize("p", PAIRINGS, ids=lambda p: f"{p.fg}-on-{p.bg}")
def test_every_failure_message_cites_only_what_wcag_says(p, mode):
    from engine.foundations.gate import GateFinding
    minimum, criterion = required(p, mode)
    message = GateFinding(p.fg, p.bg, mode, 1.0, minimum, criterion).message()
    if p.criterion == "system":
        # a floor of ours (logo, decoration): named as ours, no WCAG claim
        assert f"our floor is {minimum:g}:1" in message and "WCAG" not in message
    else:
        _assert_cites_only_wcag(message)


def test_high_contrast_non_text_floor_is_named_as_ours():
    from engine.foundations.gate import GateFinding
    part = next(p for p in PAIRINGS if p.fg == "color.line.input")
    minimum, criterion = required(part, "scheme:light,contrast:high")
    message = GateFinding(part.fg, part.bg, "scheme:light,contrast:high", 4.09,
                          minimum, criterion).message()
    assert "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3:1)" in message
    assert "WCAG 1.4.11 needs 4.5" not in message


@pytest.mark.parametrize("seed", ["#FFD400", "#00F1B0", "#291F18", "#1F9D55"])
def test_retune_notes_cite_only_what_wcag_says(seed, monkeypatch):
    # The high-contrast table starts far enough out that no seed needs a
    # retune there, so two starting points move inward to make the retune
    # write high-contrast notes for text (1.4.6) and for a non-text part.
    high = dict(color_module.HIGH_CONTRAST)
    high["color.text.muted"] = ("color.neutral.500", "color.neutral.500")
    high["color.line.input"] = ("color.neutral.300", "color.neutral.700")
    monkeypatch.setattr(color_module, "HIGH_CONTRAST", high)
    notes = [n for n in generate_color(AXES, seed).notes
             if "(scheme:" in n and not re.match(r"color\.\S+ group \(", n)]
    assert any("contrast:standard" in n for n in notes), seed
    assert any("WCAG 1.4.6 needs 7:1" in n for n in notes), seed
    assert any("our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3:1)" in n
               for n in notes), seed
    for note in notes:
        if "our floor is" in note and "WCAG" not in note:
            continue  # a floor of ours, named as ours
        _assert_cites_only_wcag(note)


def test_focus_ring_pairings_cite_non_text_contrast():
    rings = [p for p in PAIRINGS if p.fg in ("color.focus.ring", "color.focus.ring-inverse")]
    assert {p.fg for p in rings} == {"color.focus.ring", "color.focus.ring-inverse"}
    assert all(p.criterion == "1.4.11" for p in rings)


# Color completion: states, disabled, selected, destructive, strong status
# fills, overlays, the inverse focus ring and the raised surface.

NEW_ROLES = (
    "color.surface.raised", "color.surface.selected", "color.text.disabled",
    "color.text.on-danger", "color.action.primary-pressed", "color.action.danger",
    "color.action.danger-hover", "color.action.danger-pressed", "color.action.disabled",
    "color.line.selected", "color.focus.ring-inverse", "color.scrim",
) + tuple(f"color.status.{s}.{r}" for s in ("danger", "warning", "success", "info")
          for r in ("strong", "on-strong"))


def test_new_roles_exist_as_semantics():
    ts = generate_color(AXES, "#3366FF").tokens
    for role in NEW_ROLES:
        assert role in SEMANTIC and ts.get(role).layer == "semantic", role


def test_overlays_are_a_translucent_primitive_family():
    ts = generate_color(AXES, "#3366FF").tokens
    assert ts.get("color.shade.40").value == "#00000066"
    assert ts.get("color.tint.10").value == "#FFFFFF1A"
    assert [t.path for t in ts.tokens() if t.path.startswith("color.shade.")] == [
        f"color.shade.{p}" for p in (10, 20, 40, 60, 80)]
    assert ts.resolve("color.scrim", "scheme:light,contrast:standard") == "#00000066"
    assert ts.resolve("color.scrim", "scheme:dark,contrast:high") == "#000000CC"


@pytest.mark.parametrize("seed", SEEDS)
def test_fill_states_differ_and_carry_their_text(seed):
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        for fill, on in (("color.action.primary", "color.text.on-action"),
                         ("color.action.danger", "color.text.on-danger")):
            chain = [ts.resolve(r, mode) for r in (fill, f"{fill}-hover", f"{fill}-pressed")]
            assert len(set(chain)) == 3, f"{seed} {fill} ({mode})"
            text = ts.resolve(on, mode)
            assert text in ("#FFFFFF", "#000000")
            need = 7.0 if "contrast:high" in mode else 4.5
            assert all(contrast(text, c) >= need for c in chain), f"{seed} {fill} ({mode})"


def test_destructive_fill_comes_from_the_danger_ramp():
    ts = generate_color(AXES, "#3366FF").tokens
    for mode in COLOR_CONTEXTS:
        assert ts.raw("color.action.danger", mode).startswith("{color.danger."), mode


@pytest.mark.parametrize("seed", SEEDS)
def test_strong_status_fills_carry_black_or_white_text(seed):
    ts = generate_color(AXES, seed).tokens
    for s in ("danger", "warning", "success", "info"):
        for mode in COLOR_CONTEXTS:
            text = ts.resolve(f"color.status.{s}.on-strong", mode)
            fill = ts.resolve(f"color.status.{s}.strong", mode)
            assert text in ("#FFFFFF", "#000000")
            assert contrast(text, fill) >= (7.0 if "contrast:high" in mode else 4.5)


def test_disabled_and_state_checks_fire_on_collisions():
    from engine.foundations.color import CHECKS
    from engine.foundations.tokens import Token, TokenSet
    ts = TokenSet()
    ts.add(Token("color.n.1", "color", "#777777"))
    for role in ("color.action.primary", "color.action.primary-hover",
                 "color.action.primary-pressed", "color.text.default", "color.text.muted",
                 "color.text.disabled", "color.action.disabled"):
        ts.add(Token(role, "color", "{color.n.1}", layer="semantic"))
    by_id = {c.id: c for c in CHECKS}
    ctx = "scheme:dark,contrast:standard"
    states = by_id["states-distinct"].run(ts, ctx)
    assert states == [
        f"color.action.primary-hover equals color.action.primary ({ctx}) at #777777; point "
        "color.action.primary-hover at a neighboring step so each state reads as a different color",
        f"color.action.primary-pressed equals color.action.primary ({ctx}) at #777777; point "
        "color.action.primary-pressed at a neighboring step so each state reads as a different color"]
    disabled = by_id["disabled-distinct"].run(ts, ctx)
    assert len(disabled) == 3 and disabled[0].startswith("color.text.disabled equals color.text.default")


def test_disabled_fill_must_differ_from_card_and_raised():
    from engine.foundations.color import CHECKS
    from engine.foundations.tokens import Token, TokenSet
    def tokens(card):
        ts = TokenSet()
        ts.add(Token("color.n.800", "color", "#333333"))
        ts.add(Token("color.n.900", "color", "#222222"))
        ts.add(Token("color.action.disabled", "color", "{color.n.800}", layer="semantic"))
        ts.add(Token("color.surface.card", "color", "{" + card + "}", layer="semantic"))
        ts.add(Token("color.surface.raised", "color", "{color.n.800}", layer="semantic"))
        return ts

    ts = tokens("color.n.900")
    check = {c.id: c for c in CHECKS}["disabled-visible"]
    assert (check.criterion, check.axes) == ("system", ("scheme", "contrast"))
    ctx = "scheme:dark,contrast:standard"
    assert check.run(ts, ctx) == [
        f"color.action.disabled equals color.surface.raised ({ctx}) at #333333, so a disabled "
        "button vanishes on that surface. WCAG exempts inactive controls from contrast "
        "minimums, so this is a distinctness rule, not a ratio: point color.action.disabled at a "
        "step that differs from color.surface.card and color.surface.raised"]
    both = check.run(tokens("color.n.800"), ctx)
    assert [m.split(" (")[0] for m in both] == [
        "color.action.disabled equals color.surface.card",
        "color.action.disabled equals color.surface.raised"]


@pytest.mark.parametrize("seed", SEEDS + _SWEEP_SEEDS)
def test_generated_disabled_fill_differs_from_card_and_raised(seed):
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        disabled = ts.resolve("color.action.disabled", mode)
        for bg in ("color.surface.card", "color.surface.raised"):
            assert disabled != ts.resolve(bg, mode), f"{seed} {bg} ({mode})"


def test_scheme_polarity_catches_a_dark_scheme_with_a_light_palette():
    from engine.foundations.color import CHECKS
    from engine.foundations.tokens import Token, TokenSet
    ts = TokenSet()
    ts.add(Token("color.n.50", "color", "#FAFAFA"))
    ts.add(Token("color.n.900", "color", "#111111"))
    ts.add(Token("color.surface.page", "color", "{color.n.50}", layer="semantic"))
    ts.add(Token("color.text.default", "color", "{color.n.900}", layer="semantic"))
    polarity = {c.id: c for c in CHECKS}["scheme-polarity"]
    assert polarity.run(ts, "scheme:light,contrast:standard") == []
    assert polarity.run(ts, "scheme:dark,contrast:standard") == [
        "color.surface.page is not darker than color.text.default (scheme:dark,contrast:standard); "
        "a dark scheme needs a darker page, so point color.surface.page and color.text.default at "
        "the other ends of the neutral ramp"]


# Selection and separators: the selected edge stands out from every
# surface the ring does, and a separator never equals the surface it
# divides.

_SURFACES = ("color.surface.page", "color.surface.card", "color.surface.sunken",
             "color.surface.raised")


def test_line_selected_pairs_with_every_surface_the_ring_does():
    from engine.foundations.gate import GateFinding, Pairing
    ring_bgs = {p.bg for p in PAIRINGS if p.fg == "color.focus.ring"}
    selected = {p.bg: p for p in PAIRINGS if p.fg == "color.line.selected"}
    assert set(selected) == ring_bgs == set(_SURFACES)
    for bg, p in selected.items():
        assert p == Pairing("color.line.selected", bg, 3.0, "1.4.11")
        assert required(p, "scheme:dark,contrast:standard") == (3.0, "1.4.11")
        assert required(p, "scheme:dark,contrast:high") == (4.5, "high-contrast floor over 1.4.11")
        std = GateFinding(p.fg, bg, "scheme:light,contrast:standard", 2.5,
                          *required(p, "scheme:light,contrast:standard")).message()
        high = GateFinding(p.fg, bg, "scheme:light,contrast:high", 4.2,
                           *required(p, "scheme:light,contrast:high")).message()
        assert "WCAG 1.4.11 needs 3:1" in std
        assert "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3:1)" in high


@pytest.mark.parametrize("seed", SEEDS + _SWEEP_SEEDS)
def test_line_selected_stands_out_from_every_surface(seed):
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        need = 4.5 if "contrast:high" in mode else 3.0
        line = ts.resolve("color.line.selected", mode)
        for bg in _SURFACES:
            assert contrast(line, ts.resolve(bg, mode)) >= need, f"{seed} {bg} ({mode})"


def test_line_selected_retunes_against_sunken(monkeypatch):
    # A brand.600 that clears the page and card at 3:1 but not the sunken
    # surface: the retune moves line.selected on, as it moves other lines,
    # and notes the sunken pairing it fixed.
    from engine.foundations.color_math import hex_to_oklch
    ts = generate_color(AXES, "#3366FF").tokens
    ctx = "scheme:light,contrast:standard"
    page, card, sunken = (ts.resolve(r, ctx) for r in _SURFACES[:3])
    grays = [oklch_to_hex(l / 1000, 0.0, 0.0) for l in range(1000, 0, -1)]
    edge = next(g for g in grays if min(contrast(g, page), contrast(g, card)) >= 3.0)
    assert contrast(edge, sunken) < 3.0
    stops = {s: oklch_to_hex(0.98 - 0.09 * i, 0.0, 0.0) for i, s in enumerate(STEPS)}
    stops[600] = edge
    _brand_ramp(monkeypatch, "#3366FF", stops)
    result = generate_color(AXES, "#3366FF")
    line = result.tokens.resolve("color.line.selected", ctx)
    assert line != edge and hex_to_oklch(line)[0] < hex_to_oklch(edge)[0]
    for bg in (page, card, sunken):
        assert contrast(line, bg) >= 3.0
    assert any(n.startswith(f"color.line.selected ({ctx}): color.brand.600 -> ")
               and "color.line.selected on color.surface.sunken" in n
               and "WCAG 1.4.11 needs 3:1" in n for n in result.notes)


def _subtle_set(subtle, card, raised):
    from engine.foundations.tokens import Token, TokenSet
    ts = TokenSet()
    for step, hx in (("700", "#444444"), ("800", "#333333"), ("900", "#222222")):
        ts.add(Token(f"color.n.{step}", "color", hx))
    for role, step in (("color.line.subtle", subtle), ("color.surface.card", card),
                       ("color.surface.raised", raised)):
        ts.add(Token(role, "color", "{color.n.%s}" % step, layer="semantic"))
    return ts


def test_line_subtle_must_differ_from_card_and_raised():
    from engine.foundations.color import CHECKS
    check = {c.id: c for c in CHECKS}["line-subtle-visible"]
    assert (check.criterion, check.axes) == ("system", ("scheme", "contrast"))
    ctx = "scheme:dark,contrast:standard"
    assert check.run(_subtle_set("700", "900", "800"), ctx) == []
    assert check.run(_subtle_set("800", "900", "800"), ctx) == [
        f"color.line.subtle equals color.surface.raised ({ctx}) at #333333, so a separator "
        "vanishes on that surface. A decorative line needs no contrast ratio, but it must differ "
        "from the surface it divides: point color.line.subtle at a step that differs from "
        "color.surface.card and color.surface.raised"]
    both = check.run(_subtle_set("800", "800", "800"), ctx)
    assert [m.split(" (")[0] for m in both] == [
        "color.line.subtle equals color.surface.card",
        "color.line.subtle equals color.surface.raised"]


def test_line_subtle_check_blocks_the_build(monkeypatch):
    # Put dark line.subtle back on raised's step: the gate refuses the build
    # and names the check.
    semantic = dict(color_module.SEMANTIC)
    semantic["color.line.subtle"] = ("color.neutral.200", "color.neutral.800")
    monkeypatch.setattr(color_module, "SEMANTIC", semantic)
    with pytest.raises(GateFailure) as exc:
        build_color(AXES, "#3366FF")
    failures = [f for f in exc.value.report.failures if f.check == "line-subtle-visible"]
    assert [f.mode for f in failures] == ["scheme:dark,contrast:standard"]
    assert failures[0].message.startswith("color.line.subtle equals color.surface.raised")


@pytest.mark.parametrize("seed", SEEDS + _SWEEP_SEEDS)
def test_generated_line_subtle_differs_from_card_and_raised(seed):
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        subtle = ts.resolve("color.line.subtle", mode)
        for bg in ("color.surface.card", "color.surface.raised"):
            assert subtle != ts.resolve(bg, mode), f"{seed} {bg} ({mode})"


# Pairing coverage by construction: every text role pairs with every surface
# text can sit on, and every line and ring role with every surface a control
# sits on, generated from two tables so a new surface or role cannot be missed.

_TEXT_ROLES = ("color.text.default", "color.text.muted", "color.text.link",
               "color.status.danger.text", "color.status.warning.text",
               "color.status.success.text", "color.status.info.text",
               "color.text.accent", "color.text.support")
_TEXT_SURFACES = _SURFACES + ("color.surface.selected", "color.surface.tint",
                              "color.surface.band", "color.surface.stripe")
_LINE_ROLES = ("color.line.input", "color.line.selected", "color.line.danger",
               "color.line.accent", "color.focus.ring")


def test_the_coverage_tables_name_every_text_and_line_role():
    assert color_module.TEXT_ROLES == _TEXT_ROLES
    assert color_module.TEXT_SURFACES == _TEXT_SURFACES
    assert color_module.LINE_ROLES == _LINE_ROLES
    assert color_module.LINE_SURFACES == _SURFACES


def test_every_text_and_line_role_pairs_with_every_surface_in_its_table():
    from engine.foundations.gate import Pairing
    for role in _TEXT_ROLES:
        for bg in _TEXT_SURFACES:
            assert Pairing(role, bg, 4.5, "1.4.3") in PAIRINGS, (role, bg)
    for role in _LINE_ROLES:
        for bg in _SURFACES:
            assert Pairing(role, bg, 3.0, "1.4.11") in PAIRINGS, (role, bg)
    assert len(set(PAIRINGS)) == len(PAIRINGS)


def test_every_other_pairing_is_kept():
    from engine.foundations.gate import Pairing
    softs = [f"color.status.{s}.soft" for s in color_module.STATUS_HUES]
    kept = ([Pairing(r, soft, 4.5, "1.4.3") for r in ("color.text.default", "color.text.muted")
             for soft in softs]
            + [Pairing(f"color.status.{s}.text", f"color.status.{s}.soft", 4.5, "1.4.3")
               for s in color_module.STATUS_HUES]
            + [Pairing("color.text.inverse", "color.surface.inverse", 4.5, "1.4.3")]
            + [Pairing(on, state, 4.5, "1.4.3")
               for fill, on in (("color.action.primary", "color.text.on-action"),
                                ("color.action.danger", "color.text.on-danger"))
               for state in (fill, fill + "-hover", fill + "-pressed")]
            + [Pairing(f"color.status.{s}.on-strong", f"color.status.{s}.strong", 4.5, "1.4.3")
               for s in color_module.STATUS_HUES]
            + [Pairing("color.action.primary-edge", "color.surface.page", 3.0, "1.4.11")]
            + [Pairing(state, "color.surface.page", 3.0, "1.4.11")
               for state in ("color.action.danger", "color.action.danger-hover",
                             "color.action.danger-pressed")]
            + [Pairing(f"color.status.{s}.strong", "color.surface.page", 3.0, "1.4.11")
               for s in color_module.STATUS_HUES]
            + [Pairing("color.focus.ring-inverse", "color.surface.inverse", 3.0, "1.4.11")]
            + [Pairing("color.text.on-brand", "color.surface.brand", 4.5, "1.4.3")]
            + [Pairing(r, "color.surface.code", 4.5, "1.4.3") for r in color_module.SYNTAX_ROLES]
            + [Pairing("color.illustration.line", bg, 3.0, "1.4.11")
               for bg in ("color.surface.page", "color.surface.card", "color.surface.raised")]
            + [Pairing(r, bg, 1.5, "system", high=1.5) for r in color_module.DECORATIVE_ROLES
               for bg in ("color.surface.page", "color.surface.card")]
            + [Pairing("color.logo", "color.surface.page", 3.0, "system", high=3.0)])
    for p in kept:
        assert p in PAIRINGS, p
    covered = len(_TEXT_ROLES) * len(_TEXT_SURFACES) + len(_LINE_ROLES) * len(_SURFACES)
    assert len(PAIRINGS) == covered + len(kept)


def test_adding_a_surface_or_a_role_to_a_table_adds_its_pairings():
    from engine.foundations.gate import Pairing
    base = color_module.build_pairings()
    assert base == PAIRINGS
    more = color_module.build_pairings(
        text_roles=_TEXT_ROLES + ("color.text.extra",),
        text_surfaces=_TEXT_SURFACES + ("color.surface.extra",),
        line_roles=_LINE_ROLES + ("color.line.extra",),
        line_surfaces=_SURFACES + ("color.surface.extra",))
    added = set(more) - set(base)
    assert added == (
        {Pairing("color.text.extra", bg, 4.5, "1.4.3")
         for bg in _TEXT_SURFACES + ("color.surface.extra",)}
        | {Pairing(r, "color.surface.extra", 4.5, "1.4.3") for r in _TEXT_ROLES}
        | {Pairing("color.line.extra", bg, 3.0, "1.4.11")
           for bg in _SURFACES + ("color.surface.extra",)}
        | {Pairing(r, "color.surface.extra", 3.0, "1.4.11") for r in _LINE_ROLES})
    assert set(base) <= set(more)


def test_the_ring_solver_reads_the_ring_surfaces_from_the_pairings(monkeypatch):
    # The group solver picks the ring against the surfaces PAIRINGS names
    # for it, so a surface added to the line table reaches the solver too.
    assert color_module._paired_with("color.focus.ring") == _SURFACES
    extra = color_module.build_pairings(line_surfaces=_SURFACES + ("color.surface.selected",))
    monkeypatch.setattr(color_module, "PAIRINGS", extra)
    assert color_module._paired_with("color.focus.ring") == _SURFACES + ("color.surface.selected",)


@pytest.mark.parametrize("seed", SEEDS + _SWEEP_SEEDS)
def test_input_borders_and_muted_text_clear_every_surface(seed):
    # The two gaps the final review measured: an input border on the raised
    # surface in dark mode, and muted text on the selected surface.
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        high = "contrast:high" in mode
        line = ts.resolve("color.line.input", mode)
        for bg in _SURFACES:
            assert contrast(line, ts.resolve(bg, mode)) >= (4.5 if high else 3.0), (bg, mode)
        muted = ts.resolve("color.text.muted", mode)
        for bg in _TEXT_SURFACES:
            assert contrast(muted, ts.resolve(bg, mode)) >= (7.0 if high else 4.5), (bg, mode)


@pytest.mark.parametrize("seed", SEEDS + _SWEEP_SEEDS)
def test_dark_input_border_starts_where_it_clears_the_raised_surface(seed):
    # The default is the fix, not a retune on every build.
    assert SEMANTIC["color.line.input"][1] == "color.neutral.400"
    notes = generate_color(AXES, seed).notes
    assert not [n for n in notes if n.startswith("color.line.input (scheme:dark,contrast:standard)")]


# Coverage closure: a role added to SEMANTIC in the text, surface, line or
# focus family joins a coverage table or is exempt with a stated reason, so
# it can never ship with no pairing at all.

def test_every_text_surface_line_and_focus_role_is_in_a_table_or_exempt():
    assert color_module.uncovered_roles(SEMANTIC) == []
    tables = set(color_module.TEXT_ROLES + color_module.TEXT_SURFACES
                 + color_module.LINE_ROLES + color_module.LINE_SURFACES)
    exempt = color_module.COVERAGE_EXEMPT
    assert set(exempt) <= set(SEMANTIC)
    assert not set(exempt) & tables
    assert all(reason.strip() for reason in exempt.values())


def test_a_role_added_only_to_the_semantic_table_is_named():
    extra = list(SEMANTIC) + ["color.text.subtle", "color.surface.overlay", "color.scrim-2",
                              "color.action.secondary"]
    assert color_module.uncovered_roles(extra) == ["color.text.subtle", "color.surface.overlay"]


def test_brand_fidelity_states_every_context_and_names_an_identity_loss():
    ts = generate_color(AXES, "#E85D04").tokens
    lines = color_module.brand_fidelity(ts)
    assert [line.split(":")[0] for line in lines[:4]] == [
        "Light mode", "Dark mode", "Light mode, high contrast", "Dark mode, high contrast"]
    assert lines[4] == "The logo (color.logo) is the brand color #E85D04 exactly in every mode."
    assert lines[0].startswith("Light mode: the button is the brand color #E85D04 exactly, with "
                               "black text at 5.99:1 (white would be 3.50:1).")
    assert "black on a mid tone reads muddy in this mode" in lines[1]
    assert "reads as a different color from the brand (OKLab distance 0.14)" in lines[2]
    assert all("The focus ring measures " in line for line in lines[:4])
    assert "different color" not in lines[1]


@pytest.mark.parametrize("axes, role", [
    (AxisValues(0.85, 0.5, 0.5, 0.5, 0.2, 0.6, 0.5), "fill"),
    (AxisValues(0.7, 0.4, 0.5, 0.75, 0.7, 0.1, 0.7), "accent"),
    (AxisValues(0.3, 0.7, 0.6, 0.2, 0.65, 0.4, 0.0), "edge"),
])
def test_the_axes_choose_the_brand_role_and_every_role_passes(axes, role):
    from engine.foundations import character
    assert character.brand_role(axes) == role
    ts = build_color(axes, "#6D28D9").tokens
    light = "scheme:light,contrast:standard"
    primary = ts.raw("color.action.primary", light)
    link = ts.raw("color.text.link", light)
    assert primary.startswith("{color.brand.") == (role == "fill")
    assert link.startswith("{color.brand.") == (role != "edge")
    assert ts.raw("color.line.accent", light).startswith("{color.brand.")
    lines = color_module.brand_fidelity(ts)
    assert ("ink" in lines[0]) == (role != "fill")


def test_a_brief_can_name_the_brand_role():
    ts = generate_color(AXES, "#6D28D9", brand_role="edge").tokens
    assert ts.raw("color.action.primary", "scheme:light,contrast:standard") == \
        "{color.neutral.900}"
    assert "color: brand role edge (set by the brief)" in \
        generate_color(AXES, "#6D28D9", brand_role="edge").notes


def test_the_logo_keeps_the_exact_brand_where_it_clears_our_floor():
    ts = generate_color(AXES, "#6D28D9").tokens
    assert ts.resolve("color.logo", "scheme:light,contrast:standard") == "#6D28D9"
    for mode in COLOR_CONTEXTS:
        assert contrast(ts.resolve("color.logo", mode),
                        ts.resolve("color.surface.page", mode)) >= color_module.LOGO_FLOOR
