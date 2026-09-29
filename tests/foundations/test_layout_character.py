"""Layout character from measured award pages: the landing gap follows how
calm and formal the brand is, measures count characters, an expressive
landing page runs nearly edge to edge, and sections meet by a seam."""
import pytest

from engine.foundations import build_system, character, fonts, to_css
from engine.foundations.layout import FULL_CONTAINER, MIN_MEASURE_CH
from engine.synthesizer.axes import AxisValues

CALM = AxisValues(warmth=0.4, contrast=0.2, density=0.4, geometry=0.3, formality=0.8, motion=0.2,
                  type_personality=0.6)
LOUD = AxisValues(warmth=0.7, contrast=0.9, density=0.5, geometry=0.7, formality=0.1, motion=0.9,
                  type_personality=0.5)
MID = AxisValues(*[0.5] * 7)
CORNERS = [AxisValues(*[float(b) for b in f"{i:07b}"]) for i in range(128)]


def axes(**kw):
    values = dict(zip(("warmth", "contrast", "density", "geometry", "formality", "motion",
                       "type_personality"), [0.5] * 7))
    values.update(kw)
    return AxisValues(**values)


def px(ts, role, mode=""):
    v = ts.resolve(role, mode)
    return v["value"] * (16 if v["unit"] == "rem" else 1)


def chars(ts, role):
    face = fonts.BY_FAMILY[ts.resolve("type.face.text")[0]]
    return px(ts, role) / (face.metrics.latin_avg / face.metrics.upm * 16)


# 5. The landing gap.

@pytest.mark.parametrize("axis, sign", [("contrast", -1), ("motion", -1), ("formality", 1)])
def test_the_landing_gap_falls_with_energy_and_rises_with_formality(axis, sign):
    gaps = [character.landing_gap_px(axes(**{axis: i / 10})) for i in range(11)]
    assert min(sign * (b - a) for a, b in zip(gaps, gaps[1:])) > 0, gaps


def test_the_landing_gap_spans_64_to_240_and_a_phone_keeps_most_of_it():
    gaps = [character.landing_gap_px(a) for a in CORNERS]
    assert min(gaps) == pytest.approx(64.0) and max(gaps) == pytest.approx(240.0)
    shares = [character.phone_gap_share(a) for a in CORNERS]
    assert min(shares) == pytest.approx(0.6) and max(shares) == pytest.approx(0.9)


def test_a_calm_brief_spaces_its_sections_far_apart_on_a_phone_too():
    calm, loud = (build_system(a, "#3366FF").tokens for a in (CALM, LOUD))
    assert px(calm, "layout.landing-gap.desktop") >= 180
    assert px(calm, "layout.landing-gap.phone") >= 80
    assert px(loud, "layout.landing-gap.desktop") < px(calm, "layout.landing-gap.desktop")
    loudest = build_system(AxisValues(1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), "#3366FF").tokens
    for ts in (calm, loud, loudest):
        share = px(ts, "layout.landing-gap.phone") / px(ts, "layout.landing-gap.desktop")
        assert 0.6 <= share <= 0.9, share
        tiers = [px(ts, f"layout.landing-gap.{t}") for t in ("phone", "tablet", "laptop",
                                                              "desktop")]
        assert tiers == sorted(tiers)


# 8. Measures count characters.

def test_landing_copy_runs_42_to_56_characters_and_reading_60_to_70():
    for a in (CALM, MID, LOUD):
        ts = build_system(a, "#3366FF").tokens
        assert 40 <= chars(ts, "layout.measure.landing") <= 58
        assert 58 <= chars(ts, "layout.measure.text") <= 72
    assert [character.landing_measure_ch(a) for a in (LOUD, MID, CALM)] == sorted(
        character.landing_measure_ch(a) for a in (LOUD, MID, CALM))
    assert character.reading_measure_ch(axes(formality=0.0), long_read=True) == 60
    assert character.reading_measure_ch(axes(formality=1.0), long_read=True) == 66


def test_the_phone_gap_keeps_its_share_everywhere():
    import itertools
    steps = (0.0, 0.25, 0.5, 0.75, 1.0)
    for c, d, f, m in itertools.product(steps, repeat=4):
        ts = build_system(AxisValues(0.5, c, d, 0.5, f, m, 0.5), "#3366FF",
                          foundations=("space", "layout")).tokens
        share = px(ts, "layout.landing-gap.phone") / px(ts, "layout.landing-gap.desktop")
        assert 0.6 <= share <= 0.9, (c, d, f, m, share)


def test_every_corner_keeps_the_character_floor():
    for a in CORNERS[::9]:
        ts = build_system(a, "#3366FF").tokens
        for role in ("layout.measure.landing", "layout.measure.text"):
            assert chars(ts, role) >= MIN_MEASURE_CH - 1.5, (a, role)


# 11. The full-width frame.

def test_an_expressive_landing_page_runs_nearly_edge_to_edge():
    ts = build_system(LOUD, "#3366FF").tokens
    assert px(ts, "layout.landing.max-width") == FULL_CONTAINER
    margin = px(ts, "layout.landing.margin-inline.desktop")
    assert 24 <= margin <= 48 and 1440 - 2 * margin >= 1340
    assert px(ts, "layout.measure.text") < px(ts, "layout.landing.max-width")
    assert "--layout-landing-margin-inline: var(--layout-landing-margin-inline-desktop);" in \
        to_css(ts)


def test_a_calm_landing_page_keeps_the_container():
    ts = build_system(CALM, "#3366FF").tokens
    assert px(ts, "layout.landing.max-width") == px(ts, "layout.container.max")
    assert px(ts, "layout.landing.margin-inline.desktop") == px(ts, "layout.margin-inline.desktop")


def test_the_full_width_margin_tightens_with_energy():
    margins = [character.full_margin_px(axes(contrast=i / 10, motion=i / 10)) for i in range(11)]
    assert margins == sorted(margins, reverse=True) and margins[0] == 48 and margins[-1] == 24


# 15. How sections meet.

def test_a_flat_brand_meets_edge_to_edge_and_a_bold_one_cuts_hard():
    flat = axes(contrast=0.0, formality=1.0)
    assert character.seam_overlap_px(flat) == 0 and character.seam_fade_px(flat) == 0
    assert character.seam_fade_px(axes(contrast=1.0)) == 0
    deep = axes(contrast=0.6, formality=0.0)
    assert character.seam_overlap_px(deep) > 64 and character.seam_fade_px(deep) > 0


def test_the_seam_grows_with_depth():
    overlaps = [character.seam_overlap_px(axes(contrast=i / 10)) for i in range(11)]
    assert overlaps == sorted(overlaps) and overlaps[-1] - overlaps[0] >= 100


def test_only_a_formal_calm_brand_draws_a_hairline_where_sections_meet():
    formal_calm = build_system(axes(contrast=0.0, motion=0.0, formality=1.0), "#3366FF").tokens
    assert px(formal_calm, "layout.seam.line") >= 1
    assert px(build_system(CALM, "#3366FF").tokens, "layout.seam.line") >= 1
    for a in (MID, LOUD, axes(contrast=0.0, motion=0.0, formality=0.5)):
        assert px(build_system(a, "#3366FF").tokens, "layout.seam.line") == 0, a
    lines = [character.seam_line(axes(contrast=0.0, motion=0.0, formality=i / 10))
             for i in range(11)]
    assert lines == sorted(lines) and lines[5] == 0 and lines[-1] == 1
