"""Brand first: a supplied brand color is the identity. Three brands with
briefs like real client work (industry and tone words only) show that the
brand leads the role, the text on a saturated mid tone reads naturally, the
neutrals take the brand's temperature, the supporting accent never forms a
pairing anti-slop bans, and every control fill is measured on every surface
its contract places it on, the brand band included."""
import copy
import functools
import itertools
import math

import pytest

from engine.contracts import SEED_DIR, load_contract
from engine.contracts.bind import binding_problems
from engine.foundations import build_system, character
from engine.foundations import color as color_module
from engine.foundations.art import art_files
from engine.foundations.color import COLOR_CONTEXTS, IDENTITY_DISTANCE, brand_fidelity
from engine.foundations.color_math import contrast, hex_to_oklch, oklab_distance, oklch_to_hex
from engine.foundations.emit import brief_audience, choose_axes, make_system
from engine.foundations.modes import parse
from engine.foundations.tokens import TokenSet
from engine.synthesizer.axes import AxisValues

# Neutral brands: an electric blue, a saturated mid blue that white text
# reads on at a little under 4.5:1, and a light grey.
ELECTRIC, MID_BLUE, GREY = "#1510F0", "#2279EE", "#BBBBBB"
# Briefs like the real ones: a formal, technical finance brief; a formal
# commerce brief with a warm industry; a warm, friendly care brief.
BRIEFS = {
    ELECTRIC: {"industry": "fintech-banking", "tone": ["precise", "trustworthy", "technical"]},
    GREY: {"industry": "ecommerce", "tone": ["serious", "trustworthy", "precise", "geometric"],
           "languages": ["ar-SA", "en"], "primary_script": "arabic"},
    MID_BLUE: {"industry": "healthcare", "tone": ["trustworthy", "friendly"],
               "languages": ["ar-JO", "en"], "primary_script": "arabic"},
}
LIGHT = "scheme:light,contrast:standard"
HIGH = {m for m in COLOR_CONTEXTS if parse(m).get("contrast") == "high"}


@functools.lru_cache(maxsize=None)
def built(brand):
    brief = BRIEFS[brand]
    axes, _ = choose_axes(brief, None)
    return axes, build_system(axes, brand, audience=brief_audience(brief))


def _copy(tokens):
    """A token set of copied tokens, so a test can repoint roles without
    touching the cached build."""
    ts = TokenSet()
    for token in tokens.tokens():
        ts.add(copy.deepcopy(token))
    return ts


def role_of(result):
    note = next(n for n in result.notes if n.startswith("color: brand role "))
    return note.split()[3]


# ---------------------------------------------------------------- 1. the role

def test_a_saturated_mid_brand_fills_the_action_even_in_a_formal_brief():
    for brand in (ELECTRIC, MID_BLUE):
        axes, result = built(brand)
        assert role_of(result) == "fill", brand
        raw = result.tokens.raw("color.action.primary", LIGHT)
        assert raw.startswith("{color.brand."), (brand, raw)
    # the formal finance brief alone would have chosen an ink action
    axes, _ = built(ELECTRIC)
    assert character.brand_role(axes) != "fill"


def test_a_grey_brand_argues_for_an_ink_action_in_a_formal_brief():
    axes, result = built(GREY)
    assert role_of(result) in ("accent", "edge")
    assert result.tokens.raw("color.action.primary", LIGHT).startswith("{color.neutral.")


@pytest.mark.parametrize("brand", ["#E8F1FF", "#0B1020", "#8A8A8A", "#F4F4EE", "#1A1C22"])
def test_a_near_white_near_black_or_near_grey_brand_leaves_the_role_to_a_formal_brief(brand):
    L, C, _ = hex_to_oklch(brand)
    assert character.brand_fill_evidence(L, C) < 0.25
    formal = AxisValues(0.3, 0.35, 0.6, 0.12, 1.0, 0.35, 0.0)
    assert character.brand_role(formal, character.brand_fill_evidence(L, C)) != "fill"


# Saturated yellows, ambers, navies, teals and greens stand apart from the
# page and from ink, so the lightness never demotes them.
SATURATED = ["#FFD400", "#FACC15", "#F59E0B", "#003366", "#1E3A8A", "#4B2E83", "#0A2463",
             "#0D9488", "#0F766E", "#16A34A", "#00A651", "#658BA7"]


@pytest.mark.parametrize("brand", SATURATED)
def test_a_saturated_yellow_amber_navy_teal_or_green_fills_its_action(brand):
    L, C, _ = hex_to_oklch(brand)
    evidence = character.brand_fill_evidence(L, C)
    assert evidence >= 0.3, evidence
    if C >= 0.1:
        assert evidence >= 0.8, evidence
        formal = AxisValues(0.3, 0.35, 0.6, 0.12, 1.0, 0.35, 0.0)
        assert character.brand_role(formal, evidence) == "fill"
    assert character.brand_role(AxisValues(*[0.5] * 7), evidence) == "fill"


def test_the_brand_evidence_is_continuous_in_lightness_and_chroma():
    for chroma in (0.0, 0.05, 0.1, 0.2):
        values = [character.brand_fill_evidence(i / 100, chroma) for i in range(101)]
        assert all(abs(b - a) <= 0.15 for a, b in zip(values, values[1:]))
    # pure white and pure black carry no fill, whatever the chroma
    assert character.brand_fill_evidence(1.0, 0.0) == character.brand_fill_evidence(0.0, 0.0) \
        == 0.0
    lights = [character.brand_fill_evidence(0.55, c / 100) for c in range(31)]
    assert all(abs(b - a) <= 0.12 for a, b in zip(lights, lights[1:]))
    assert lights[0] == 0.0 and lights[-1] == 1.0


def test_full_brand_evidence_wins_the_fill_whatever_the_axes():
    for corner in range(128):
        axes = AxisValues(*[(corner >> i) & 1 for i in range(7)])
        assert character.brand_role(axes, 1.0) == "fill", axes
    # with no brand the axes alone still decide, fill on a tie
    assert character.brand_role(AxisValues(*[0.5] * 7)) == "fill"


def test_the_report_says_the_brand_led_the_role():
    _, result = built(ELECTRIC)
    note = next(n for n in result.notes if n.startswith("color: brand role "))
    assert "brand 1.00" in note


def test_the_report_states_the_brand_s_case_and_the_natural_move_in_sentences():
    brief = BRIEFS[MID_BLUE]
    axes, source = choose_axes(brief, None)
    report = make_system(MID_BLUE, axes, source, audience=brief_audience(brief)).report
    assert ("Brand role fill: the brand fills the main action. The brand color's own case for "
            "a fill scored 1.00, where a saturated mid tone scores 1") in report
    assert ("In light mode, color.action.primary is color.brand.fill with white text rather "
            "than color.brand.exact with black text: black text there weighs ") in report
    assert "- color: in " not in report


# ------------------------------------------------------ 2. natural on-colors

def test_a_saturated_mid_tone_takes_white_on_a_step_just_darker_not_black_on_the_hex():
    _, result = built(MID_BLUE)
    ts = result.tokens
    fill, on = ts.resolve("color.action.primary", LIGHT), ts.resolve("color.text.on-action", LIGHT)
    assert on == "#FFFFFF"
    assert fill != MID_BLUE
    assert hex_to_oklch(fill)[0] < hex_to_oklch(MID_BLUE)[0]
    # the least darkening at the brand's own hue and chroma, not a ramp step
    assert ts.raw("color.action.primary", LIGHT) == "{color.brand.fill}"
    assert oklab_distance(fill, MID_BLUE) <= 0.03
    assert 4.5 <= contrast(on, fill) < 4.7
    line = brand_fidelity(ts)[0]
    assert "black text would measure" in line and "reads less naturally" in line, line
    # the brand band follows the same rule
    assert ts.resolve("color.text.on-brand", LIGHT) == "#FFFFFF"


def test_a_bright_brand_keeps_black_text_on_the_exact_color():
    for mode in (LIGHT, "scheme:dark,contrast:standard"):
        ts = build_system(AxisValues(*[0.5] * 7), "#F97316").tokens
        assert ts.resolve("color.action.primary", mode) == "#F97316", mode
        assert ts.resolve("color.text.on-action", mode) == "#000000", mode


@pytest.mark.parametrize("hue", [30.0, 60.0, 150.0, 200.0, 258.0])
def test_the_natural_fill_moves_continuously_with_the_brand_lightness(hue):
    """Sweep a brand's lightness through the point where white text stops
    reading on it. Wherever the fill takes white it sits nearer the brand
    than black text would cost on the brand, never at a ramp step further
    out; and the fill only jumps where the text turns from white to black,
    by about what black costs there, never by a ramp step."""
    prev = None
    for i in range(41):
        brand = oklch_to_hex(0.50 + i * 0.005, 0.13, hue)
        ts = build_system(AxisValues(*[0.5] * 7), brand, foundations=("color",)).tokens
        black = color_module.natural_cost(brand, "color.base.black", LIGHT)
        for mode in (LIGHT, "scheme:dark,contrast:standard"):
            fill = ts.resolve("color.action.primary", mode)
            if ts.resolve("color.text.on-action", mode) == "#FFFFFF" and fill != brand:
                assert ts.raw("color.action.primary", mode) == "{color.brand.fill}", (brand, mode)
                cost = color_module.natural_cost(brand, "color.base.black", mode)
                assert oklab_distance(fill, brand) <= cost + 1e-6, (brand, mode, fill)
        fill, on = ts.resolve("color.action.primary", LIGHT), \
            ts.resolve("color.text.on-action", LIGHT)
        if prev is not None:
            p_brand, p_fill, p_on, p_black = prev
            step = oklab_distance(p_brand, brand)
            # the same text: the fill follows the brand; a switch: at most
            # what black cost on the last brand, plus the step
            most = step + 0.01 if on == p_on else p_black + step + 1e-6
            assert oklab_distance(p_fill, fill) <= most, (brand, p_fill, fill)
        prev = (brand, fill, on, black)


@pytest.mark.parametrize("brand", ["#16A34A", "#00A651", "#00A19A", "#E4572E", MID_BLUE, "#F97316"])
def test_light_and_dark_weigh_black_text_by_one_cost_stricter_on_a_dark_page(brand):
    """One continuous cost decides both schemes; on a dark page it runs
    higher, so wherever light takes white text dark does too."""
    ts = build_system(AxisValues(*[0.5] * 7), brand).tokens
    light = ts.resolve("color.text.on-action", LIGHT)
    dark = ts.resolve("color.text.on-action", "scheme:dark,contrast:standard")
    assert light != "#FFFFFF" or dark == "#FFFFFF", (brand, light, dark)
    L, C, _ = hex_to_oklch(brand)
    assert character.black_text_cost(L, C, dark=True) >= character.black_text_cost(L, C)


def test_the_dark_fill_moves_continuously_with_the_brand_lightness():
    """The natural move for white text is continuous on a dark page too; a
    fill that keeps black text may take a lighter brand step, as before."""
    prev = None
    dark = "scheme:dark,contrast:standard"
    for i in range(61):
        brand = oklch_to_hex(0.55 + i * 0.005, 0.13, 150.0)
        ts = build_system(AxisValues(*[0.5] * 7), brand, foundations=("color",)).tokens
        fill, on = ts.resolve("color.action.primary", dark), ts.resolve("color.text.on-action", dark)
        cost = color_module.natural_cost(brand, "color.base.black", dark)
        if prev is not None:
            p_brand, p_fill, p_on, p_cost = prev
            step = oklab_distance(p_brand, brand)
            if on == p_on == "#FFFFFF":
                assert oklab_distance(p_fill, fill) <= step + 0.01, (brand, p_fill, fill)
            elif on != p_on:
                assert oklab_distance(p_fill, fill) <= max(p_cost, cost) + step + 1e-6, \
                    (brand, p_fill, fill)
        prev = (brand, fill, on, cost)


def test_the_cost_of_black_text_is_continuous_and_never_above_the_identity_distance():
    for chroma in (0.0, 0.08, 0.2):
        costs = [character.black_text_cost(i / 100, chroma) for i in range(101)]
        assert all(0.0 <= c <= IDENTITY_DISTANCE + 1e-12 for c in costs)
        assert all(abs(b - a) <= 0.012 for a, b in zip(costs, costs[1:]))
    assert character.black_text_cost(0.9, 0.2) == 0.0
    assert character.black_text_cost(0.55, 0.0) == 0.0


def test_the_natural_check_skips_a_set_the_engine_did_not_build():
    _, result = built(MID_BLUE)
    ts = TokenSet()
    for token in result.tokens.tokens():
        if not token.path.startswith("color.brand.fill"):
            ts.add(copy.deepcopy(token))
    ts.get("color.action.primary").value = "{color.brand.exact}"
    ts.get("color.action.primary").modes.clear()
    ts.get("color.text.on-action").value = "{color.base.black}"
    ts.get("color.text.on-action").modes.clear()
    check = {c.id: c for c in color_module.CHECKS}["on-color-natural"]
    assert check.run(ts, LIGHT) == []


def test_the_gate_catches_black_text_on_a_mid_tone_where_a_near_step_reads_white():
    _, result = built(MID_BLUE)
    ts = _copy(result.tokens)
    ts.get("color.action.primary").value = "{color.brand.exact}"
    ts.get("color.action.primary").modes.clear()
    ts.get("color.text.on-action").value = "{color.base.black}"
    ts.get("color.text.on-action").modes.clear()
    check = {c.id: c for c in color_module.CHECKS}["on-color-natural"]
    found = check.run(ts, LIGHT)
    assert found and "color.text.on-action" in found[0] and "color.brand." in found[0]


# ------------------------------------------------------ 3. neutral temperature

def _neutral(ts):
    _, chroma, hue = hex_to_oklch(ts.resolve("color.neutral.500"))
    return chroma, hue


def test_a_grey_brand_with_a_warm_industry_keeps_near_true_neutrals():
    axes, result = built(GREY)
    assert axes.warmth > 0.5
    chroma, _ = _neutral(result.tokens)
    assert chroma <= 0.006


def test_a_blue_brand_with_a_warm_tone_keeps_neutral_or_cool_neutrals():
    axes, result = built(MID_BLUE)
    assert axes.warmth >= 0.8
    chroma, hue = _neutral(result.tokens)
    assert chroma <= 0.006 or 180 <= hue <= 300, (chroma, hue)


@pytest.mark.parametrize("brand", ["#C2410C", "#FF6A00", "#E85D04"])
def test_a_warm_brand_with_a_cool_brief_keeps_warm_or_grey_neutrals_never_rose(brand):
    """The lean runs along the brand's own hue, toward grey, and never turns
    the neutrals through red or magenta."""
    _, bc, bh = hex_to_oklch(brand)
    for warmth in (0.0, 0.2):
        hue, chroma = character.neutral_tint(AxisValues(warmth, *[0.5] * 6), bh, bc)
        assert chroma <= 0.002 or abs(character.hue_delta(bh, hue)) <= 5.0, (brand, hue, chroma)


def test_warmth_still_leans_the_neutrals_of_a_grey_brand():
    cool = character.neutral_tint(AxisValues(0.0, *[0.5] * 6), 0.0, 0.0)
    warm = character.neutral_tint(AxisValues(1.0, *[0.5] * 6), 0.0, 0.0)
    assert 0.006 <= cool[1] <= character.LEAN_C and 0.006 <= warm[1] <= character.LEAN_C
    assert abs(character.hue_delta(cool[0], character.COOL_HUE)) < 1
    assert abs(character.hue_delta(warm[0], character.WARM_HUE)) < 1


# ------------------------------------------------------ 5. the support accent

BLUE, PURPLE, PINK = (215.0, 285.0), (285.0, 330.0), (330.0, 380.0)


def _in(hue, arc):
    lo, hi = arc
    return lo <= hue < hi or lo <= hue + 360.0 < hi


def _banned(brand_hue, brand_chroma, support_hue, support_chroma):
    """A pairing anti-slop bans: a blue brand with a pink or purple support,
    a purple brand with a blue one, or any cool brand with a pink one. The
    engine's own rule (character.banned_pair) must agree with these arcs."""
    if brand_chroma < 0.06 or support_chroma < character.HUE_CHROMA:
        return False
    cool = character.coolness(brand_hue) >= 0.75
    ours = (_in(brand_hue, BLUE) and (_in(support_hue, PURPLE) or _in(support_hue, PINK))) \
        or (_in(brand_hue, PURPLE) and _in(support_hue, BLUE)) \
        or (cool and _in(support_hue, PINK))
    assert ours == character.banned_pair(brand_hue, support_hue), (brand_hue, support_hue)
    return ours


def test_the_support_accent_never_forms_a_banned_pairing():
    for hue in range(0, 360, 3):
        for chroma in (0.06, 0.1, 0.16, 0.24):
            brand = oklch_to_hex(0.56, chroma, float(hue))
            _, bc, bh = hex_to_oklch(brand)
            for w in (0.0, 0.5, 1.0):
                for c in (0.0, 0.5, 1.0):
                    axes = AxisValues(w, c, 0.5, 0.5, 0.5, 0.5, 0.5)
                    _, sc, sh = character.support_seed(axes, bh, bc)
                    assert not _banned(bh, bc, sh, sc), (brand, w, c, round(sh), round(sc, 3))


def test_the_three_brands_get_an_analogous_or_quiet_support():
    for brand in (ELECTRIC, MID_BLUE, GREY):
        _, result = built(brand)
        _, bc, bh = hex_to_oklch(brand)
        _, sc, sh = hex_to_oklch(result.tokens.resolve("color.support.500"))
        assert not _banned(bh, bc, sh, sc), (brand, sh, sc)
        if bc >= 0.12:
            assert abs(character.hue_delta(bh, sh)) <= 45, (brand, sh, sc)


def test_an_achromatic_brand_s_support_is_a_neutral_step_and_a_near_grey_s_nearly_one():
    for warmth in (0.0, 0.5, 1.0):
        for contrast_ in (0.0, 1.0):
            axes = AxisValues(warmth, contrast_, *[0.5] * 5)
            assert character.support_seed(axes, 30.0, 0.0)[1] == 0.0
            assert character.support_seed(axes, 30.0, 0.01)[1] <= 0.02
    _, result = built(GREY)
    assert hex_to_oklch(result.tokens.resolve("color.support.500"))[1] <= 0.01
    chromas = [character.support_seed(AxisValues(*[0.5] * 7), 250.0, c / 1000)[1]
               for c in range(0, 81)]
    assert all(abs(b - a) <= 0.01 for a, b in zip(chromas, chromas[1:]))


@pytest.mark.parametrize("brand", [ELECTRIC, MID_BLUE, "#0D9488", "#7C3AED"])
def test_a_cool_brand_s_support_moves_with_the_axes_within_its_family(brand):
    """Brand fidelity fixes the button, so character shows in the support:
    warmth, formality and contrast move it, inside the brand's family and
    outside every banned pairing."""
    _, bc, bh = hex_to_oklch(brand)
    seen = set()
    for w, c, f in itertools.product((0.0, 0.25, 0.5, 0.75, 1.0), repeat=3):
        axes = AxisValues(w, c, 0.5, 0.5, f, 0.5, 0.5)
        _, sc, sh = character.support_seed(axes, bh, bc)
        assert not character.banned_pair(bh, sh) or sc < character.HUE_CHROMA, (brand, axes)
        seen.add((round(sh), round(sc, 3)))
    hues = sorted({h for h, _ in seen})
    assert len(seen) >= 8, seen
    assert max(abs(character.hue_delta(bh, h)) for h in hues) >= 15, hues


def test_the_support_seed_is_continuous_in_the_brand():
    axes = AxisValues(0.9, 0.35, 0.5, 0.7, 0.75, 0.3, 0.8)
    prev = None
    for step in range(0, 201):
        a = 0.2 * math.cos(math.radians(260)) * step / 200
        b = 0.2 * math.sin(math.radians(260)) * step / 200
        chroma, hue = math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360
        _, sc, sh = character.support_seed(axes, hue, chroma)
        point = (sc * math.cos(math.radians(sh)), sc * math.sin(math.radians(sh)))
        if prev is not None:
            assert math.dist(prev, point) <= 0.02, step
        prev = point


def test_the_gradient_draws_the_brand_ramp_and_neutrals_only():
    for brand in (ELECTRIC, MID_BLUE, GREY):
        axes, result = built(brand)
        svg = art_files(result.tokens, axes, brand)["art/gradient.svg"]
        assert "color-decorative-support" not in svg
        assert "color-surface-tint" in svg and "color-decorative-brand" in svg


# ------------------------------------------------ 9. fills on every placement

def test_the_button_on_the_brand_band_clears_the_band_in_every_context():
    for brand in (ELECTRIC, MID_BLUE, GREY):
        _, result = built(brand)
        ts = result.tokens
        for mode in COLOR_CONTEXTS:
            band = ts.resolve("color.surface.brand", mode)
            need_fill = 4.5 if mode in HIGH else 3.0
            need_text = 7.0 if mode in HIGH else 4.5
            label = ts.resolve("color.text.on-brand-action", mode)
            # the rest fill is also the button's edge in every state
            assert contrast(ts.resolve("color.action.on-brand", mode), band) >= need_fill, \
                (brand, mode)
            for fill in ("color.action.on-brand", "color.action.on-brand-hover",
                         "color.action.on-brand-pressed"):
                assert contrast(label, ts.resolve(fill, mode)) >= need_text, (brand, fill, mode)


def test_the_primary_edge_and_the_danger_fill_clear_every_surface_the_button_sits_on():
    for brand in (ELECTRIC, MID_BLUE, GREY, "#2D0679", "#658BA7"):
        ts = built(brand)[1].tokens if brand in BRIEFS else \
            build_system(AxisValues(*[0.5] * 7), brand).tokens
        for mode in COLOR_CONTEXTS:
            need = 4.5 if mode in HIGH else 3.0
            for surface in ("color.surface.page", "color.surface.card", "color.surface.raised",
                            "color.surface.sunken", "color.surface.tint", "color.surface.band",
                            "color.surface.stripe", "color.surface.header"):
                bg = ts.resolve(surface, mode)
                for role in ("color.action.primary-edge", "color.action.danger",
                             "color.action.danger-hover", "color.action.danger-pressed"):
                    assert contrast(ts.resolve(role, mode), bg) >= need, (brand, role, surface,
                                                                         mode)


def test_the_contract_check_measures_a_fill_on_the_brand_band():
    """The default primary button placed on the brand band of a grey brand
    in dark measured about 1.3:1 and nothing caught it. The contract check
    now measures every fill on every surface its contract places it on,
    the band included, and the button binds the band's own fill there."""
    _, result = built(GREY)
    ts = _copy(result.tokens)
    button = load_contract(SEED_DIR / "button.yaml")
    assert binding_problems(button, ts) == []
    dark = "scheme:dark,contrast:standard"
    ink = ts.resolve("color.action.primary", dark)
    assert contrast(ink, ts.resolve("color.surface.brand", dark)) < 3.0
    # repoint the band's fill at the ink action: the check names it
    ts.get("color.action.on-brand").modes.clear()
    ts.get("color.action.on-brand").value = ts.raw("color.action.primary", dark)
    ts.get("color.action.on-brand").modes["scheme:dark"] = ts.raw("color.action.primary", dark)
    found = [p for p in binding_problems(button, ts) if p.rule == "fill-placement"]
    assert found and "color.surface.brand" in found[0].message


def test_the_steel_blue_edge_clears_the_section_band_under_its_own_axes():
    ts = build_system(AxisValues(0, 0, 0.5, 0.5, 0, 0.5, 0.5), "#658BA7").tokens
    for mode in COLOR_CONTEXTS:
        need = 4.5 if mode in HIGH else 3.0
        assert contrast(ts.resolve("color.action.primary-edge", mode),
                        ts.resolve("color.surface.band", mode)) >= need, mode


def test_on_the_brand_band_only_bound_combinations_exist_and_each_is_measured():
    button = load_contract(SEED_DIR / "button.yaml")
    combos = button.combinations()
    on_band = [c for c in combos if c["surface"] == "brand"]
    assert on_band and all(c["intent"] == "neutral" for c in on_band)
    assert {c["emphasis"] for c in on_band} == {"primary", "secondary", "ghost"}
    assert button.variant_product() == len(combos)
    for brand in (ELECTRIC, MID_BLUE, GREY):
        assert binding_problems(button, built(brand)[1].tokens) == [], brand


@pytest.mark.parametrize("brand", ["#F59E0B", "#CDAC00", "#E79E4A", "#F3973D"])
def test_link_text_reads_on_every_status_soft_fill_for_a_warm_brand(brand):
    ts = build_system(AxisValues(*[0.5] * 7), brand).tokens
    for mode in COLOR_CONTEXTS:
        need = 7.0 if mode in HIGH else 4.5
        for status in character.STATUS_HUES:
            assert contrast(ts.resolve("color.text.link", mode),
                            ts.resolve(f"color.status.{status}.soft", mode)) >= need, \
                (brand, status, mode)
