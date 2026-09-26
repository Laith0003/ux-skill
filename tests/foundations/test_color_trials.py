"""Color findings from trial site specimens: dark bands and the
dark sunken surface, table headers, status soft fills that follow the
character, the brand fill under high contrast, and a veil for generated art
with a role for a control on it."""
import json
from pathlib import Path

import pytest

from engine.contracts.library import seed_contracts
from engine.foundations import build_system, character
from engine.foundations.color import COLOR_CONTEXTS, IDENTITY_DISTANCE, RING_ON_FILL, CHECKS
from engine.foundations.color_math import contrast, hex_to_oklch, hex_to_rgb, oklab_distance
from engine.foundations.emit import brief_audience, choose_axes
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

from tests.foundations.trials import MID, TRIALS

BRIEFS = Path(__file__).resolve().parent / "briefs"
DARK, DARK_HIGH = "scheme:dark,contrast:standard", "scheme:dark,contrast:high"
LIGHT, LIGHT_HIGH = "scheme:light,contrast:standard", "scheme:light,contrast:high"
BRANDS = ("#2563EB", "#6D28D9", "#E85D04", "#0F766E", "#3366FF", "#FFD400", "#6B4423",
          "#E61428", "#1F9D55", "#808080")


def load_seed(name):
    return next(c for c in seed_contracts() if c.name == name)


def _trial(name):
    brief = json.loads((BRIEFS / f"{name}.json").read_text(encoding="utf-8"))
    axes, _ = choose_axes(brief, None)
    return build_system(axes, TRIALS[name], audience=brief_audience(brief)).tokens, axes


def _L(hx):
    return hex_to_oklch(hx[:7])[0]


def _C(hx):
    return hex_to_oklch(hx[:7])[1]


def axes(**kw):
    return AxisValues(**dict(MID, **kw))


# Item 3: dark bands, the dark sunken surface and table headers.

@pytest.mark.parametrize("brand", BRANDS)
@pytest.mark.parametrize("contrast_axis", [0.0, 0.4, 1.0])
def test_a_dark_band_keeps_its_chroma_under_the_characters_cap(brand, contrast_axis):
    a = axes(contrast=contrast_axis)
    ts = build_system(a, brand).tokens
    cap = character.dark_band_chroma(a)
    for mode in (DARK, DARK_HIGH):
        assert _C(ts.resolve("color.surface.band", mode)) <= cap + 0.004, (brand, mode)


def test_the_trial_dark_bands_are_quiet():
    for name in TRIALS:
        ts, a = _trial(name)
        assert _C(ts.resolve("color.surface.band", DARK)) <= 0.07, name


@pytest.mark.parametrize("brand", BRANDS)
@pytest.mark.parametrize("mode", [DARK, DARK_HIGH])
def test_the_dark_sunken_surface_sits_between_the_page_and_the_card(brand, mode):
    ts = build_system(axes(), brand).tokens
    page, sunken, card = (_L(ts.resolve(f"color.surface.{s}", mode))
                          for s in ("page", "sunken", "card"))
    assert page < sunken < card, (brand, mode, page, sunken, card)


@pytest.mark.parametrize("brand", BRANDS)
def test_a_table_header_is_a_band_off_the_card_and_never_below_the_page(brand):
    ts = build_system(axes(), brand).tokens
    for mode in COLOR_CONTEXTS:
        header = ts.resolve("color.surface.header", mode)
        assert header != ts.resolve("color.surface.card", mode) or "light" in mode, mode
        assert _L(header) >= _L(ts.resolve("color.surface.page", mode)) - 1e-9 \
            or "light" in mode, mode
    assert ts.resolve("color.surface.header", LIGHT) == ts.resolve("color.surface.stripe", LIGHT)
    assert ts.resolve("color.surface.header", DARK) == ts.resolve("color.surface.raised", DARK)


def test_the_table_contract_binds_its_header_to_the_header_surface():
    table = load_seed("table")
    fills = {(b.part, b.role) for b in table.tokens if b.property == "fill" and not b.state}
    assert ("header", "color.surface.header") in fills
    assert all(r != "color.surface.sunken" for p, r in fills if p == "header")


# Item 5: status soft fills take their chroma from the character.

def _soft_chroma(ts, mode=LIGHT):
    return sum(_C(ts.resolve(f"color.status.{s}.soft", mode))
               for s in character.STATUS_HUES) / len(character.STATUS_HUES)


def test_a_calm_brief_gets_a_quiet_info_fill():
    clinic, _ = _trial("clinic")
    restaurant, _ = _trial("restaurant")
    assert _C(clinic.resolve("color.status.info.soft", LIGHT)) <= 0.03
    assert _soft_chroma(clinic) < _soft_chroma(restaurant)
    assert _soft_chroma(clinic, DARK) < _soft_chroma(restaurant, DARK)


@pytest.mark.parametrize("axis", ["contrast", "motion"])
def test_the_soft_fill_chroma_rises_continuously_with_energy(axis):
    prev = None
    for i in range(11):
        c = _soft_chroma(build_system(axes(**{axis: i / 10}), "#3366FF").tokens)
        if prev is not None:
            assert c >= prev - 1e-4 and c - prev < 0.01, (axis, i)
        prev = c


def test_status_text_still_reads_on_every_quieter_soft_fill():
    for name in TRIALS:
        ts, _ = _trial(name)
        for s in character.STATUS_HUES:
            for mode in COLOR_CONTEXTS:
                need = 7.0 if "high" in mode else 4.5
                assert contrast(ts.resolve(f"color.status.{s}.text", mode),
                                ts.resolve(f"color.status.{s}.soft", mode)) >= need


# Item 6: high contrast keeps the brand's family, and the ring its own rule.

def test_light_high_contrast_keeps_a_bright_brand_in_its_family():
    ts, _ = _trial("restaurant")
    fill = ts.resolve("color.action.primary", LIGHT_HIGH)
    assert oklab_distance(fill, TRIALS["restaurant"]) <= IDENTITY_DISTANCE, fill
    assert contrast(ts.resolve("color.text.on-action", LIGHT_HIGH), fill) >= 7.0


def test_dark_high_contrast_picks_a_fill_the_ring_can_stand_off():
    ts, _ = _trial("restaurant")
    fill = ts.resolve("color.action.primary", DARK_HIGH)
    ring = ts.resolve("color.focus.ring", DARK_HIGH)
    assert contrast(ring, fill) >= RING_ON_FILL, (fill, ring)
    assert contrast(ts.resolve("color.text.on-action", DARK_HIGH), fill) >= 7.0
    assert abs(character.hue_delta(hex_to_oklch(fill)[2],
                                   hex_to_oklch(TRIALS["restaurant"])[2])) < 3


# Item 2: a veil for generated art, and a role for a control on media.

def _over(color, alpha, under):
    top, bottom = hex_to_rgb(color), hex_to_rgb(under)
    return "#" + "".join(f"{round(alpha * t + (1 - alpha) * b):02X}" for t, b in zip(top, bottom))


def _art(ts, mode):
    return [ts.resolve(r, mode) for r in ("color.decorative.brand", "color.decorative.support",
                                          "color.decorative.neutral", "color.surface.page")]


@pytest.mark.parametrize("brand", BRANDS)
def test_text_on_the_veil_reads_over_every_art_color(brand):
    ts = build_system(axes(), brand).tokens
    for mode in COLOR_CONTEXTS:
        veil = ts.resolve("color.media.veil", mode)
        base, alpha = veil[:7], int(veil[7:9], 16) / 255
        text = ts.resolve("color.text.on-media", mode)
        need = 7.0 if "high" in mode else 4.5
        for art in _art(ts, mode):
            assert contrast(text, _over(base, alpha, art)) >= need, (brand, mode, art)


def test_the_veil_is_the_page_color_and_light_art_needs_little_of_it():
    ts, _ = _trial("restaurant")
    veil = ts.resolve("color.media.veil", LIGHT)
    assert veil[:7] == ts.resolve("color.surface.page", LIGHT)
    assert int(veil[7:9], 16) < int(ts.resolve("imagery.scrim")[7:9], 16) / 2
    assert _L(veil) > 0.9


def test_a_control_on_media_has_a_role_and_the_button_contract_names_it():
    ts, _ = _trial("restaurant")
    assert ts.has("color.text.on-media")
    usage = " ".join(load_seed("button").do)
    assert "color.text.on-media" in usage and "imagery.on-scrim" in usage


def test_the_veil_check_names_the_role_and_the_fix():
    built = build_system(axes(), "#3366FF").tokens
    ts = TokenSet()
    for t in built.tokens():
        if t.path == "color.text.on-media":
            t = Token(t.path, "color", "{color.base.white}", layer="semantic")
        ts.add(t)
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    msgs = [f.message for f in report.failures if f.check == "media-veil"]
    assert msgs and "color.text.on-media" in msgs[0] and "color.media.veil" in msgs[0]
