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
    # the states-distinct check naming the fix.
    brand = "#3366FF"
    _brand_ramp(monkeypatch, brand, {s: "#808080" for s in STEPS})
    result = generate_color(AXES, brand)
    assert any(n.startswith("color.action.primary group (scheme:light,contrast:standard): every "
                            "step of the brand ramp resolves to the same color")
               for n in result.notes)
    with pytest.raises(GateFailure) as exc:
        build_color(AXES, brand)
    failures = [f for f in exc.value.report.failures if f.check == "states-distinct"]
    assert failures and "color.action.primary-hover equals color.action.primary" in failures[0].message
    assert "point color.action.primary-hover at a neighboring step" in failures[0].message


def test_unsatisfiable_action_group_keeps_the_closest_and_the_gate_blocks_it(monkeypatch):
    # A ramp that never leaves the near-white end cannot give the button
    # 3:1 against a light page. The generator keeps the closest candidate,
    # its note carries the ratios reached, and the gate names the failing
    # pairing.
    brand = "#3366FF"
    _brand_ramp(monkeypatch, brand,
                {s: oklch_to_hex(0.99 - i * 0.01, 0.0, 0.0) for i, s in enumerate(STEPS)})
    notes = [n for n in generate_color(AXES, brand).notes
             if n.startswith("color.action.primary group (scheme:light,contrast:standard)")]
    assert len(notes) == 1 and "kept the closest" in notes[0]
    assert len(re.findall(r"\d+\.\d\d:1", notes[0])) == 3
    with pytest.raises(GateFailure) as exc:
        build_color(AXES, brand)
    assert any((f.fg, f.bg, f.mode) == ("color.action.primary", "color.surface.page",
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
    # R16 item 3 / R17: action.primary-hover must read as a different color
    # from action.primary in both modes, must itself clear 3:1 against the
    # page (R17 item a: PAIRINGS now has an entry for this, so the loop
    # below already covers it; asserted directly too so the guarantee is
    # named, not just implied by iterating PAIRINGS), and every pairing
    # must still pass after the action-group solver runs.
    ts = generate_color(AXES, seed).tokens
    for mode in COLOR_CONTEXTS:
        primary = ts.resolve("color.action.primary", mode)
        hover = ts.resolve("color.action.primary-hover", mode)
        page = ts.resolve("color.surface.page", mode)
        assert primary != hover, f"{seed}: primary == hover ({mode}) = {primary}"
        assert contrast(hover, page) >= 3.0, \
            f"{seed}: hover on page ({mode}) = {contrast(hover, page):.2f}"
    for p in PAIRINGS:
        for mode in COLOR_CONTEXTS:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= required(p, mode)[0], f"{seed}: {p.fg} on {p.bg} ({mode}) = {ratio:.2f}"


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
        for mode in COLOR_CONTEXTS:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            assert ratio >= required(p, mode)[0], f"{seed}: {p.fg} on {p.bg} ({mode}) = {ratio:.2f}"
    for mode in COLOR_CONTEXTS:
        primary = ts.resolve("color.action.primary", mode)
        hover = ts.resolve("color.action.primary-hover", mode)
        page = ts.resolve("color.surface.page", mode)
        assert primary != hover, f"{seed}: primary == hover ({mode})"
        # R17: hover must stay usable (>= 3:1 against the page) even when
        # phase 3's old nudge-only fix would have satisfied on-action while
        # letting the hover fill nearly disappear.
        assert contrast(hover, page) >= 3.0, \
            f"{seed}: hover on page ({mode}) = {contrast(hover, page):.2f}"


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


def test_ring_is_not_paired_with_the_button_fill():
    fills = ("color.action.primary",) + color_module._FILL_STATES["color.action.primary"]
    assert not [p for p in PAIRINGS if p.fg == "color.focus.ring" and p.bg in fills]
    assert all(p.high is None for p in PAIRINGS)


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
        assert "WCAG 1.4.11 needs 3.0:1" in std
        assert "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3.0:1)" in high
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
    return tuple(ts.raw(r, _LIGHT)[1:-1] for r in _GROUP_OUT + ("color.focus.ring",))


def test_solver_order_fill_distance_before_state_direction(monkeypatch):
    # brand.500 (the default fill) carries white text and clears the page,
    # but 600 and 700 are near white, so hover and pressed cannot go the
    # conventional (darker) way. The fill stays and the states go lighter.
    # An order that put the state direction first would move the fill to
    # 800 to keep 900 and 950 as darker states.
    # The ring's default brand.700 is near white; the next brand step in
    # the conventional direction, 800, clears every surface. A neutral ring
    # (neutral.950) would come first if neutral outranked the brand ramp.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.43, 0.983, 0.983, 0.37, 0.31, 0.27])
    assert _group(generate_color(AXES, "#3366FF").tokens) == (
        "color.brand.500", "color.brand.400", "color.brand.300", "color.base.white",
        "color.brand.800")


def test_solver_order_conventional_direction_at_equal_distance(monkeypatch):
    # The default fill brand.500 is too light. One step either way clears
    # (600 darker, 400 lighter); the conventional darker step wins, and its
    # states continue darker. The ring's default brand.700 clears every
    # surface; it equals the hover, which is allowed.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.8, 0.43, 0.39, 0.34, 0.31, 0.27])
    assert _group(generate_color(AXES, "#3366FF").tokens) == (
        "color.brand.600", "color.brand.700", "color.brand.800", "color.base.white",
        "color.brand.700")


def test_ring_prefers_a_color_other_than_the_fill(monkeypatch):
    # brand.800 resolves to the same color as the fill (brand.500). The
    # ring skips it for the next brand step that clears every surface.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.43, 0.983, 0.983, 0.43, 0.31, 0.27])
    assert _group(generate_color(AXES, "#3366FF").tokens) == (
        "color.brand.500", "color.brand.400", "color.brand.300", "color.base.white",
        "color.brand.900")


def test_the_fill_never_moves_to_make_the_ring_differ(monkeypatch):
    # When the only ring on offer is the fill itself, the ring equals the
    # fill; the fill does not move to make room.
    _gray_ramp(monkeypatch, [0.983, 0.95, 0.85, 0.49, 0.465, 0.43, 0.983, 0.983, 0.37, 0.31, 0.27])
    monkeypatch.setattr(color_module, "_ring_candidates",
                        lambda mode, default_ring: ["color.brand.500"])
    assert _group(generate_color(AXES, "#3366FF").tokens) == (
        "color.brand.500", "color.brand.400", "color.brand.300", "color.base.white",
        "color.brand.500")


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


def test_ring_moves_are_noted():
    # A yellow brand's light fill moves to brand.700, the ring's default;
    # the ring steps on to brand.800 so it differs from the fill, and the
    # note says so with the ring's lowest ratio against the surfaces.
    notes = [n for n in generate_color(AXES, "#FFD400").notes
             if n.startswith("color.action.primary group (scheme:light,contrast:standard)")]
    assert len(notes) == 1
    assert "color.action.primary color.brand.500 -> color.brand.700" in notes[0]
    assert "color.focus.ring color.brand.700 -> color.brand.800" in notes[0]
    assert re.search(r"ring/surface \d+\.\d\d:1$", notes[0]), notes[0]


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
    _assert_cites_only_wcag(GateFinding(p.fg, p.bg, mode, 1.0, minimum, criterion).message())


def test_high_contrast_non_text_floor_is_named_as_ours():
    from engine.foundations.gate import GateFinding
    part = next(p for p in PAIRINGS if p.fg == "color.line.input")
    minimum, criterion = required(part, "scheme:light,contrast:high")
    message = GateFinding(part.fg, part.bg, "scheme:light,contrast:high", 4.09,
                          minimum, criterion).message()
    assert "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3.0:1)" in message
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
    assert any("WCAG 1.4.6 needs 7.0:1" in n for n in notes), seed
    assert any("our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3.0:1)" in n
               for n in notes), seed
    for note in notes:
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
