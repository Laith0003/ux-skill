"""Composition character from measured award pages: display faces spread
across the axis space, section bands and the color budget follow energy,
decorative lines are ink at a low alpha, and a full-bleed hero anchors its
headline with a scrim over the region it fills."""
import collections
import itertools

import pytest

from engine.foundations import build_system, character, composition, fonts, imagery
from engine.foundations.gate import gate
from engine.foundations.color_math import hex_to_oklch
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

CALM = AxisValues(warmth=0.4, contrast=0.2, density=0.4, geometry=0.3, formality=0.8, motion=0.2,
                  type_personality=0.6)
LOUD = AxisValues(warmth=0.7, contrast=0.9, density=0.5, geometry=0.7, formality=0.1, motion=0.9,
                  type_personality=0.5)


def axes(**kw):
    values = dict(zip(("warmth", "contrast", "density", "geometry", "formality", "motion",
                       "type_personality"), [0.5] * 7))
    values.update(kw)
    return AxisValues(**values)


# 16. The ubiquity cost.

def test_no_display_face_takes_more_than_its_share_and_every_face_wins_somewhere():
    steps = fonts.UBIQUITY_SAMPLE
    wins = collections.Counter()
    for w, c, g, f, p in itertools.product(steps, repeat=5):
        wins[fonts.nearest("display", AxisValues(w, c, 0.5, g, f, 0.5, p)).family] += 1
    total = sum(wins.values())
    display = [f.family for f in fonts.FACES if f.role == "display"]
    assert set(wins) == set(display)
    assert max(wins.values()) / total <= fonts.UBIQUITY_CAP
    assert min(wins.values()) / total >= fonts.UBIQUITY_FLOOR


def test_ubiquity_is_a_property_of_display_faces_only():
    for face in fonts.FACES:
        assert face.ubiquity >= 0
        if face.role != "display":
            assert face.ubiquity == 0


# 6. Bands and the color budget.

def test_a_calm_page_changes_no_color_between_sections():
    for a in (CALM, axes(contrast=0.0, motion=0.0)):
        assert character.light_band_chroma(a) == 0 == character.dark_band_chroma(a)
        assert character.band_share(a) == 0
        ts = build_system(a, "#3366FF").tokens
        assert hex_to_oklch(ts.resolve("color.surface.band", "scheme:light,contrast:standard"))[
            1] < 0.005
        assert ts.resolve("color.budget.bands") == 0


def test_a_loud_page_carries_color_in_its_bands_and_budget():
    ts = build_system(LOUD, "#3366FF").tokens
    assert character.light_band_chroma(LOUD) >= 0.09
    assert 0.3 <= ts.resolve("color.budget.bands") <= 0.5
    assert 0.15 <= ts.resolve("color.budget.chromatic") <= 0.2
    assert hex_to_oklch(ts.resolve("color.surface.band", "scheme:light,contrast:standard"))[1] \
        > 0.02


@pytest.mark.parametrize("fn", [character.light_band_chroma, character.band_share,
                                character.chromatic_budget])
def test_bands_and_the_budget_rise_with_energy(fn):
    values = [fn(axes(contrast=i / 10, motion=i / 10)) for i in range(11)]
    assert values == sorted(values) and values[-1] > values[0]


def test_the_chromatic_budget_runs_from_2_to_20_percent():
    corners = [AxisValues(*[float(b) for b in f"{i:07b}"]) for i in range(128)]
    budgets = [character.chromatic_budget(a) for a in corners]
    assert min(budgets) == 0.02 and max(budgets) == 0.2


# Lines in ink.

def test_the_hairline_is_the_ink_at_an_alpha_the_contrast_axis_sets():
    alphas = [character.ink_alpha(axes(contrast=i / 10)) for i in range(11)]
    assert alphas == sorted(alphas) and alphas[0] == 0.05 and alphas[-1] == 0.12
    ts = build_system(axes(), "#3366FF").tokens
    for mode, text in (("scheme:light,contrast:standard", "color.text.default"),
                       ("scheme:dark,contrast:standard", "color.text.default")):
        line = ts.resolve("color.hairline", mode)
        assert line[:7] == ts.resolve(text, mode) and len(line) == 9
    high = int(ts.resolve("color.hairline", "scheme:light,contrast:high")[7:9], 16)
    assert high > int(ts.resolve("color.hairline", "scheme:light,contrast:standard")[7:9], 16)


def test_a_card_rings_itself_in_the_ink_and_controls_keep_an_opaque_edge():
    ts = build_system(axes(), "#3366FF").tokens
    ring = ts.resolve("elevation.card")[-1]
    assert (ring["spread"]["value"], ring["blur"]["value"]) == (1, 0)
    assert int(ring["color"][7:9], 16) == round(character.ink_alpha(axes()) * 255)
    assert ts.resolve("elevation.card", "scheme:dark")[-1]["color"].startswith("#FFFFFF")
    assert len(ts.resolve("color.line.input", "scheme:light,contrast:standard")) == 7


# 13. The bottom-anchored hero.

def test_a_full_bleed_hero_anchors_at_the_bottom_unless_the_brand_is_a_poster():
    assert composition.hero_anchor(CALM) == "bottom-start"
    assert composition.hero_anchor(axes()) == "bottom-start"
    assert composition.hero_anchor(LOUD) == "center"
    media = composition.choose(axes(warmth=1.0, formality=0.0, motion=1.0, contrast=0.4))
    assert media.name == "full-bleed-media"
    assert "anchored at the bottom start" in media.line() or "centred" in media.line()
    assert media.to_dict()["anchor"] in composition.ANCHORS


def test_the_scrim_covers_the_region_the_headline_fills():
    for a in (CALM, axes(), LOUD, AxisValues(*[1.0] * 7)):
        ts = build_system(a, "#3366FF").tokens
        reach = ts.resolve("imagery.scrim-reach")
        px = ts.resolve("type.text.display")["fontSize"]["value"] * 16
        lh = ts.resolve("type.text.display")["lineHeight"]
        assert reach >= imagery.text_region(px, lh, 900) - 0.005
        assert imagery.SCRIM_REACH_MIN <= reach <= 1


def test_a_scrim_that_stops_short_of_the_headline_is_named():
    ts = build_system(LOUD, "#3366FF").tokens
    short = TokenSet(ts.axes)
    for t in ts.tokens():
        short.add(Token(t.path, t.type, 0.3) if t.path == "imagery.share.reach" else t)
    msgs = [f.message for f in gate(short, [], imagery.CHECKS, raise_on_fail=False).failures
            if f.check == "scrim-covers-text"]
    assert msgs and msgs[0].startswith("imagery.scrim-reach is 0.3, but a two-line headline at ")
