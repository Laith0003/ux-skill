"""Type character from measured award pages: the landing display follows
expressiveness and the width, its word fits the composition's column in
each script, display lines sit tight but never collide, the phone display
follows the desktop size, weights stay light, capitals track open, and a
two-voice headline is derived from the axes."""
import pytest

from engine.foundations import build_system, character, fonts, to_css
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.typography import (
    CHECKS,
    DISPLAY_LEAD,
    GRID_COLUMNS,
    HEADLINE_COLUMNS,
    MIN_DISPLAY_LEADING,
    ROLES,
    clearance,
    display_leading,
    generate_type,
)
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues

CALM = AxisValues(warmth=0.4, contrast=0.2, density=0.4, geometry=0.3, formality=0.8, motion=0.2,
                  type_personality=0.6)
LOUD = AxisValues(warmth=0.7, contrast=0.9, density=0.5, geometry=0.7, formality=0.1, motion=0.9,
                  type_personality=0.5)
MID = AxisValues(*[0.5] * 7)
LTR = "contrast:standard,direction:ltr"


def axes(**kw):
    values = dict(zip(("warmth", "contrast", "density", "geometry", "formality", "motion",
                       "type_personality"), [0.5] * 7))
    values.update(kw)
    return AxisValues(**values)


def px(dim):
    return dim["value"] * (16 if dim["unit"] == "rem" else 1)


def display_px(ts, mode=LTR):
    return px(ts.resolve("type.text.display", mode)["fontSize"])


# 1. The landing display follows expressiveness.

@pytest.mark.parametrize("axis, sign", [("contrast", 1), ("motion", 1), ("formality", -1)])
def test_the_landing_display_rises_steadily_with_energy_and_playfulness(axis, sign):
    sizes = [character.landing_display_px(axes(**{axis: i / 10})) for i in range(11)]
    steps = [sign * (b - a) for a, b in zip(sizes, sizes[1:])]
    assert min(steps) > 0, sizes


def test_the_landing_display_spans_the_measured_range_at_the_corners():
    corners = [AxisValues(*[float(b) for b in f"{i:07b}"]) for i in range(128)]
    sizes = [character.landing_display_px(a) for a in corners]
    assert min(sizes) == pytest.approx(60.0) and max(sizes) == pytest.approx(240.0)
    assert character.landing_display_px(MID) == pytest.approx(120.0)


def test_a_calm_brief_and_a_loud_brief_land_in_their_measured_bands():
    calm = build_system(CALM, "#3366FF").tokens
    loud = build_system(LOUD, "#3366FF").tokens
    assert 60 <= display_px(calm) <= 90
    assert 180 <= display_px(loud) <= 260


# 2. The fit reads the composition's column and the page's own word.

def test_the_headline_columns_come_from_the_composition():
    assert HEADLINE_COLUMNS["stacked"] == HEADLINE_COLUMNS["full-bleed-media"] == GRID_COLUMNS
    assert HEADLINE_COLUMNS["split"] < GRID_COLUMNS


def test_a_loud_brief_keeps_its_full_display_at_the_desktop_tier():
    ts = build_system(LOUD, "#3366FF").tokens
    assert ts.resolve("type.fit-columns") == 12
    assert ts.resolve("type.fit.display.desktop", LTR) == 1.0
    assert display_px(ts) >= 200


def test_a_wide_arabic_face_never_shrinks_the_latin_headline():
    ts = build_system(MID, "#3366FF").tokens
    latin = ts.resolve("type.fit.display.desktop", LTR)
    arabic = ts.resolve("type.fit.display.desktop", "contrast:standard,direction:rtl")
    assert latin == 1.0 and arabic < latin


def test_a_shorter_known_word_lets_the_phone_display_grow():
    default = build_system(LOUD, "#3366FF").tokens
    known = build_system(LOUD, "#3366FF", words={"latin": 7, "arabic": 5}).tokens
    assert known.resolve("type.fit-word.latin") == 7
    assert known.resolve("type.fluid.display.phone", LTR) > \
        default.resolve("type.fluid.display.phone", LTR)


@pytest.mark.parametrize("words", [{"latin": 0}, {"greek": 5}, {"latin": 4.5}, "seven"])
def test_a_bad_word_count_is_refused_naming_the_input(words):
    with pytest.raises((TypeError, ValueError), match="words"):
        build_system(MID, "#3366FF", words=words)


def test_the_display_fits_its_word_at_every_tier_edge_in_both_scripts():
    """The display-fits check measures the fluid size at each tier's
    narrowest and widest widths; a fluid size too large is named."""
    ts = build_system(LOUD, "#3366FF").tokens
    assert [f for f in gate(ts, [], CHECKS, raise_on_fail=False).failures
            if f.check == "display-fits"] == []
    broken = TokenSet(ts.axes)
    for t in ts.tokens():
        broken.add(Token(t.path, t.type, 30.0) if t.path == "type.vw.phone" else t)
    msgs = [f.message for f in gate(broken, [], CHECKS, raise_on_fail=False).failures
            if f.check == "display-fits"]
    assert msgs and msgs[0].startswith("type.text.display at 320px wide (phone) sets a 13 letter "
                                       "latin word")
    assert "type.fluid.display.phone" in msgs[0]


def test_tokens_css_sets_the_display_fluid_between_the_hero_and_its_factor():
    css = to_css(build_system(MID, "#3366FF").tokens)
    assert ("  --type-text-display-font-size: clamp(calc(var(--type-text-hero-font-size) + 1px), "
            "calc(var(--type-text-display-fluid) * 1vw), calc(var(--type-size-latin-10) * "
            "var(--type-text-display-scale)));") in css
    assert "    --type-text-display-fluid: var(--type-fluid-display-desktop);" in css


def test_the_fluid_display_reaches_its_size_at_the_reference_width():
    for a in (CALM, MID, LOUD):
        ts = build_system(a, "#3366FF").tokens
        at_1440 = min(ts.resolve("type.fluid.display.desktop", LTR) * 14.4,
                      display_px(ts) * ts.resolve("type.fit.display.desktop", LTR))
        assert at_1440 == pytest.approx(display_px(ts), abs=1.5)


# 3. Display leading: tight at large sizes, never colliding.

def test_display_leading_falls_with_size_and_contrast_to_the_measured_band():
    for c in (0.0, 0.5, 1.0):
        lh = [display_leading(axes(contrast=c), p) for p in (40, 60, 90, 120, 160, 240)]
        assert lh == sorted(lh, reverse=True) and lh[0] == DISPLAY_LEAD[0]
    assert display_leading(axes(contrast=0.0), 200) == 1.0
    assert display_leading(axes(contrast=1.0), 200) == 0.92
    large = [display_leading(axes(contrast=i / 10), 200) for i in range(11)]
    assert large == sorted(large, reverse=True)


def test_no_display_face_sets_its_lines_closer_than_its_ink():
    for face in fonts.FACES:
        if face.role != "display":
            continue
        assert face.ink is not None
        assert display_leading(axes(contrast=1.0), 240, face) >= clearance(face)
        assert clearance(face) >= (face.ink[0] + face.ink[1]) / 1000


def test_reading_styles_keep_1_5_and_arabic_display_sits_0_15_above_latin():
    for a in (CALM, MID, LOUD):
        ts = generate_type(a).tokens
        for role in ("type.text.body", "type.text.body-small", "type.text.fine"):
            assert ts.resolve(role, "direction:ltr")["lineHeight"] >= 1.5
        for role, spec in ROLES.items():
            if spec[1] == "display":
                ltr = ts.resolve(role, "direction:ltr")["lineHeight"]
                rtl = ts.resolve(role, "direction:rtl")["lineHeight"]
                assert rtl >= ltr + 0.15 - 1e-9 and ltr >= MIN_DISPLAY_LEADING


def test_a_display_leading_under_the_face_clearance_is_named_with_the_fix():
    ts = generate_type(axes(type_personality=1.0, formality=0.3, warmth=0.9)).tokens
    face = ts.resolve("type.face.display")[0]
    need = clearance(fonts.BY_FAMILY[face])
    assert need > 0.92
    tight = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == "type.leading.latin.step-10":
            t = Token(t.path, t.type, 0.9)
        tight.add(t)
    msgs = [f.message for f in gate(tight, [], CHECKS, raise_on_fail=False).failures
            if f.check == "display-clearance"]
    assert msgs[0] == (f"type.text.display (direction:ltr) has line height 0.9, under the {need:g} "
                       f"{face} needs for a descender to clear the ascender of the next line, so "
                       f"point it at a leading of {need:g} or more")


# 4. The phone display follows the desktop size.

@pytest.mark.parametrize("desktop, low, high", [(60, 44, 50), (120, 56, 66), (240, 80, 90)])
def test_the_phone_display_follows_the_desktop_size(desktop, low, high):
    assert low <= character.phone_display_for(desktop) <= high


def test_the_phone_display_never_falls_as_the_desktop_grows():
    sizes = [character.phone_display_for(d) for d in range(20, 300)]
    assert sizes == sorted(sizes) and min(sizes) == 20 and max(sizes) == 90


def test_three_briefs_get_a_phone_display_within_the_measured_band():
    for a in (CALM, MID, LOUD):
        ts = build_system(a, "#3366FF").tokens
        phone = display_px(ts) * ts.resolve("type.phone.display")
        assert 44 <= phone <= 90 and 0.4 <= phone / display_px(ts) <= 0.8


# 7. Weights stay light.

def test_display_weight_is_regular_to_medium_at_mid_axes_and_formal_is_lighter():
    assert 400 <= character.display_weight(MID) <= 500
    assert character.display_weight(axes(formality=1.0)) <= character.display_weight(MID)
    assert character.display_weight(axes(contrast=1.0, motion=1.0, formality=0.0)) >= 600
    corners = [AxisValues(*[float(b) for b in f"{i:07b}"]) for i in range(128)]
    assert {character.display_weight(a) for a in corners} == {400, 450, 500, 550, 600, 650}


# 10. Capitals track at 0 or open.

def test_capitals_track_at_zero_or_open_and_follow_the_display():
    for a in (CALM, MID, LOUD, AxisValues(*[1.0] * 7), AxisValues(*[0.0] * 7)):
        ts = build_system(a, "#3366FF").tokens
        caps = ts.resolve("type.text.display-caps", LTR)
        display = ts.resolve("type.text.display", LTR)
        assert caps["letterSpacing"]["value"] >= 0
        assert caps["fontSize"] == display["fontSize"] and caps["lineHeight"] == \
            display["lineHeight"]
        assert ts.resolve("type.phone.display-caps") == ts.resolve("type.phone.display")


def test_a_loud_informal_brief_leans_to_capitals_and_a_calm_one_does_not():
    assert character.capitals(LOUD) >= 0.5 > character.capitals(CALM)
    assert character.capitals(MID) == 0.0


# 14. A two-voice headline.

def test_the_emphasis_voice_is_lighter_in_the_same_face_and_keeps_the_size():
    for a in (CALM, MID, LOUD):
        ts = build_system(a, "#3366FF").tokens
        voice = ts.resolve("type.text.display-emphasis", LTR)
        display = ts.resolve("type.text.display", LTR)
        assert voice["fontFamily"] == display["fontFamily"]
        assert voice["fontSize"] == display["fontSize"]
        face = fonts.BY_FAMILY[display["fontFamily"][0]]
        assert voice["fontWeight"] < display["fontWeight"] or \
            voice["fontWeight"] == max(300, face.weights[0])
        assert voice["fontWeight"] >= 300
        assert 0 <= ts.resolve("type.emphasis.tone") <= 1


def test_the_emphasis_gap_and_tone_widen_with_type_personality_and_contrast():
    for axis in ("type_personality", "contrast"):
        tones = [character.emphasis_contrast(axes(**{axis: i / 10})) for i in range(11)]
        assert tones == sorted(tones) and tones[-1] - tones[0] >= 0.4


def test_italic_emphasis_only_in_a_face_that_ships_it_and_never_in_arabic():
    humanist = axes(type_personality=1.0, formality=0.3, warmth=0.9, contrast=0.8)
    ts = build_system(humanist, "#3366FF").tokens
    face = fonts.BY_FAMILY[ts.resolve("type.face.display")[0]]
    assert face.italic and ts.resolve("type.emphasis.italic", LTR) == 1
    assert ts.resolve("type.emphasis.italic", "contrast:standard,direction:rtl") == 0
    geometric = build_system(axes(type_personality=0.0), "#3366FF").tokens
    assert not fonts.BY_FAMILY[geometric.resolve("type.face.display")[0]].italic
    assert geometric.resolve("type.emphasis.italic", LTR) == 0


def test_an_italic_voice_loads_the_italic_file():
    from engine.foundations.fonts import cdn_url, self_host_css
    ts = build_system(axes(type_personality=1.0, formality=0.3, warmth=0.9, contrast=0.8),
                      "#3366FF").tokens
    family = ts.resolve("type.face.display")[0]
    assert f"family={family.replace(' ', '+')}:ital,wght@0," in cdn_url(ts)
    assert "-italic.woff2" in self_host_css(ts) and "font-style: italic;" in self_host_css(ts)
    plain = build_system(axes(type_personality=0.0), "#3366FF").tokens
    assert "ital," not in cdn_url(plain) and "italic" not in self_host_css(plain)


# Lines break well.

def test_headlines_balance_and_running_text_breaks_pretty():
    css = to_css(build_system(MID, "#3366FF").tokens)
    assert "  --type-text-display-text-wrap: balance;" in css
    assert "  --type-text-heading-2-text-wrap: balance;" in css
    assert "  --type-text-body-text-wrap: pretty;" in css
    assert css.count("-text-wrap:") == len([r for r in ROLES if r.endswith(
        ("display", "display-caps", "display-emphasis", "hero", "heading-1", "section-title",
         "figure", "heading-2", "heading-3", "body", "body-small", "fine"))])


def test_every_brief_still_validates_and_passes_the_type_gate():
    for a in (CALM, MID, LOUD, AxisValues(*[1.0] * 7), AxisValues(*[0.0] * 7)):
        ts = generate_type(a).tokens
        assert validate(ts) == [] and gate(ts, [], CHECKS).passed


# Dark mode sets a variable face lighter.

DARK, LIGHT = "scheme:dark,contrast:standard,direction:ltr", \
    "scheme:light,contrast:standard,direction:ltr"


def test_dark_body_text_in_a_variable_face_is_20_to_50_lighter():
    ts = build_system(MID, "#3366FF").tokens
    assert fonts.BY_FAMILY[ts.resolve("type.face.text")[0]].variable
    light = ts.resolve("type.text.body", LIGHT)["fontWeight"]
    dark = ts.resolve("type.text.body", DARK)["fontWeight"]
    assert 20 <= light - dark <= 50
    big = ts.resolve("type.text.display", LIGHT)["fontWeight"] - \
        ts.resolve("type.text.display", DARK)["fontWeight"]
    assert 0 < big <= 20


def test_a_static_face_keeps_its_weights_in_dark_mode():
    face = fonts.BY_FAMILY["IBM Plex Sans Arabic"]
    from engine.foundations.typography import dark_weight
    assert not face.variable and dark_weight(400, 16, face) == 400
    ts = build_system(CALM, "#3366FF").tokens
    rtl = ts.resolve("type.face.arabic")[0]
    if not fonts.BY_FAMILY[rtl].variable:
        for role in ("type.text.body", "type.text.heading-3"):
            assert ts.resolve(role, "scheme:dark,contrast:standard,direction:rtl")[
                "fontWeight"] == ts.resolve(role, "scheme:light,contrast:standard,"
                                                  "direction:rtl")["fontWeight"]


def test_high_contrast_wins_over_the_dark_adjustment():
    ts = build_system(MID, "#3366FF").tokens
    for role in ROLES:
        high_dark = ts.resolve(role, "scheme:dark,contrast:high,direction:ltr")["fontWeight"]
        assert high_dark >= ts.resolve(role, LIGHT)["fontWeight"]
        assert high_dark == ts.resolve(role, "scheme:light,contrast:high,direction:ltr")[
            "fontWeight"]


def test_a_dark_weight_heavier_than_light_is_named():
    ts = build_system(MID, "#3366FF").tokens
    heavy = TokenSet(ts.axes)
    for t in ts.tokens():
        if t.path == "type.text.body":
            modes = dict(t.modes, **{"scheme:dark": dict(t.value, fontWeight="{type.weight.700}")})
            t = Token(t.path, t.type, t.value, modes=modes, layer="semantic")
        heavy.add(t)
    msgs = [f.message for f in gate(heavy, [], CHECKS, raise_on_fail=False).failures
            if f.check == "dark-weights"]
    assert msgs and msgs[0].startswith("type.text.body (scheme:dark,direction:ltr) is weight "
                                       "700, heavier than its 400 in light mode")


def test_a_set_without_color_gets_no_dark_weights():
    ts = build_system(MID, "#3366FF", foundations=("space", "layout", "type")).tokens
    assert not any("scheme" in k for t in ts.tokens() for k in t.modes)
