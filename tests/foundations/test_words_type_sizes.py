"""Fix round BF7a: the words, the type and the sizes a landing page needs.

Words: common tone words move the axes by what they say, four industries
seed the axes (never a look), and a brief's character object passes what an
unread word means as axis nudges, applied after the words and stated in the
report. Type: product_type reaches the face choice through a book target
that is continuous in type personality and formality, so an app gets a sans
display face and a UI Arabic face and an editorial product may take a serif.
Sizes and surfaces: a landing display step above the hero, a figure that
holds a number band, a landing region gap, a tint that stands off the page,
a light band whose chroma follows contrast and a clean light code surface.
Briefs and brand colors here are neutral examples."""
import math

import pytest

from engine.foundations import build_system, character, fonts, to_css
from engine.foundations.audience import (
    BOOK_DEPTH, FIELDS, FIELDS_HELP, PRODUCT_TYPES, AudienceError, effects, read_audience)
from engine.foundations.color import CODE_EDGE, TINT_FLOOR
from engine.foundations.color_math import contrast, hex_to_oklch
from engine.foundations.emit import (
    InputError, _reading, brief_audience, brief_axes, make_system, nudge_lines, unread_lines)
from engine.foundations.typography import MIN_LEVEL_RATIO, PHONE_ROLES, phone_token
from engine.synthesizer.axes import (
    AXIS_NAMES, INDUSTRY_SEEDS, NUDGE_LIMIT, TONE_NUDGES, AxisValues, compute_axes)

LIGHT = "scheme:light,contrast:standard"
DARK = "scheme:dark,contrast:standard"
LTR = "contrast:standard,direction:ltr"
MID = AxisValues(*[0.5] * 7)


def axes(**kw):
    values = dict(zip(AXIS_NAMES, [0.5] * 7))
    values.update(kw)
    return AxisValues(**values)


def px(ts, role, mode=LTR):
    size = ts.resolve(role, mode)["fontSize"]
    return size["value"] * (16 if size["unit"] == "rem" else 1)


def dim(ts, path, mode=""):
    v = ts.resolve(path, mode)
    return v["value"] * (16 if v["unit"] == "rem" else 1)


# ---------------------------------------------------------------- 1. words

# Each word and the axis it must move, with the sign of the move.
WORD_MOVES = [
    ("fast", "motion", +1), ("quick", "motion", +1), ("clear", "density", -1),
    ("practical", "formality", +1), ("practical", "type_personality", -1),
    ("solid", "contrast", +1), ("solid", "geometry", -1), ("modern", "type_personality", -1),
    ("reliable", "formality", +1), ("reliable", "motion", -1), ("simple", "density", -1),
    ("clean", "density", -1), ("direct", "contrast", +1), ("secure", "formality", +1),
    ("secure", "warmth", -1), ("efficient", "density", +1), ("elegant", "type_personality", +1),
    ("premium", "density", -1), ("approachable", "warmth", +1), ("caring", "warmth", +1),
    ("gentle", "contrast", -1), ("lively", "motion", +1), ("vibrant", "contrast", +1),
    ("dynamic", "motion", +1), ("stable", "motion", -1), ("robust", "geometry", -1),
    ("crisp", "geometry", -1), ("smooth", "geometry", +1), ("functional", "density", +1),
    ("welcoming", "warmth", +1), ("trusted", "formality", +1), ("expert", "formality", +1),
    ("fresh", "motion", +1), ("innovative", "type_personality", -1),
    # words the engine already read, held to what they say
    ("bold", "contrast", +1), ("calm", "motion", -1), ("warm", "warmth", +1),
    ("sharp", "geometry", -1), ("soft", "geometry", +1),
]


@pytest.mark.parametrize("word, axis, sign", WORD_MOVES)
def test_a_tone_word_moves_the_axis_it_speaks_to(word, axis, sign):
    moved = getattr(compute_axes({"tone": [word]}), axis) - 0.5
    assert moved * sign > 0, (word, axis, moved)
    assert _reading("tone", word) == word


def test_every_word_weight_is_a_small_continuous_nudge_on_the_seven_axes():
    for word, nudge in TONE_NUDGES.items():
        assert set(nudge) <= set(AXIS_NAMES), word
        assert all(0 < abs(v) <= 0.35 for v in nudge.values()), word


def test_the_discovery_word_confident_stays_unread():
    """The discovery hint list keeps one tone word the engine leaves to the
    report; the command doc names it."""
    assert _reading("tone", "confident") is None


def test_practical_words_never_pull_a_book_serif():
    """A plain construction brief read "practical" as "professional" and got
    a formal serif; its words now point at a sturdy, plain look."""
    a = compute_axes({"industry": "construction",
                      "tone": ["solid", "reliable", "practical", "modern"]})
    choice = fonts.choose(a)
    assert choice.display.generic == "sans-serif", choice.display.family
    assert a.type_personality < 0.4 and a.geometry < 0.4, a


INDUSTRY_WORDS = {
    "construction": "construction", "building materials": "construction",
    "b2b marketplace": "b2b-marketplace", "wholesale": "b2b-marketplace",
    "security": "security", "cybersecurity": "security",
    "pharmacy": "pharmacy", "medical supply": "pharmacy",
}


@pytest.mark.parametrize("word, seed", sorted(INDUSTRY_WORDS.items()))
def test_new_industries_seed_the_axes(word, seed):
    assert seed in INDUSTRY_SEEDS
    assert compute_axes({"industry": word}) == compute_axes({"industry": seed})
    assert _reading("industry", word) is not None
    assert compute_axes({"industry": word}) != MID


def test_an_industry_seed_is_seven_axis_values_and_every_seed_is_distinct():
    """An industry is an axis seed, never a look: it names no face, color
    or size, and no two industries share a seed."""
    values = [tuple(v[a] for a in AXIS_NAMES) for v in INDUSTRY_SEEDS.values()]
    assert len(set(values)) == len(values)
    for key, seed in INDUSTRY_SEEDS.items():
        assert set(seed) == set(AXIS_NAMES), key
        assert all(0.0 <= v <= 1.0 for v in seed.values()), key


def test_a_security_brief_leans_cool_formal_and_geometric():
    a = compute_axes({"industry": "security"})
    assert a.warmth < 0.4 and a.formality > 0.7 and a.type_personality < 0.4, a


def test_character_nudges_apply_after_the_words():
    words, _ = brief_axes({"industry": "saas", "tone": ["warm"]})
    nudged, source = brief_axes({"industry": "saas", "tone": ["warm"],
                                 "character": {"warmth": -0.2, "motion": 0.1}})
    assert math.isclose(nudged.warmth, words.warmth - 0.2)
    assert math.isclose(nudged.motion, words.motion + 0.1)
    assert nudged.contrast == words.contrast
    assert "character nudges: warmth -0.2, motion +0.1" in source


def test_character_nudges_stay_inside_the_axis_and_under_forbidden():
    a, _ = brief_axes({"tone": ["warm", "inviting"], "character": {"warmth": 0.3}})
    assert a.warmth == 1.0
    b, _ = brief_axes({"tone": ["bold"], "character": {"contrast": 0.3},
                       "forbidden": ["loud"]})
    assert b.contrast == 0.5


def test_a_brief_with_only_character_builds_from_neutral():
    a, source = brief_axes({"character": {"formality": 0.25}})
    assert a == axes(formality=0.75)
    assert "character nudges: formality +0.25" in source


@pytest.mark.parametrize("value, needle", [
    ({"warmth": 0.31}, "character.warmth is 0.31; set a nudge from -0.3 to 0.3"),
    ({"warmth": "more"}, "character.warmth is 'more'; set a nudge from -0.3 to 0.3"),
    ({"vibe": 0.1}, 'character names "vibe", which is not an axis; use warmth, contrast'),
    (["warmth"], 'character is [\'warmth\']; give an object of axis nudges, for example'),
])
def test_a_bad_character_names_the_field_and_the_fix(value, needle):
    with pytest.raises(InputError) as exc:
        brief_axes({"industry": "saas", "character": value})
    assert needle in str(exc.value), str(exc.value)
    assert NUDGE_LIMIT == 0.3


def test_the_report_states_each_nudge_and_its_effect():
    brief = {"industry": "saas", "tone": ["warm"], "character": {"warmth": -0.2}}
    lines = nudge_lines(brief)
    words, _ = brief_axes({"industry": "saas", "tone": ["warm"]})
    assert len(lines) == 1
    line = lines[0]
    assert line.startswith("warmth -0.2: from %g to %g" % (round(words.warmth, 3),
                                                         round(words.warmth - 0.2, 3))), line
    assert "color and imagery" in line, line
    a, source = brief_axes(brief)
    out = make_system("#2F6FDB", a, source, audience=brief_audience(brief),
                      unread=unread_lines(brief), nudges=lines)
    assert "## Character nudges" in out.report and line in out.report


def test_an_unread_tone_word_says_how_to_pass_it_as_a_nudge():
    lines = unread_lines({"industry": "saas", "tone": ["luxurious"]})
    assert any('tone "luxurious" moves no axis' in u and '"character"' in u for u in lines), lines


def test_project_type_points_at_product_type():
    lines = unread_lines({"industry": "saas", "project_type": "landing page"})
    line = next(u for u in lines if u.startswith("project_type"))
    assert "product_type" in line and "app" in line, line


def test_the_cli_and_mcp_descriptions_name_product_type_and_character():
    for name in ("product_type", "character", *PRODUCT_TYPES, "-0.3 to 0.3"):
        assert name in FIELDS_HELP, name


# ---------------------------------------------------------------- 2. type

CARE = {"industry": "healthcare", "tone": ["trustworthy", "friendly"],
        "languages": ["ar", "en"], "primary_script": "arabic"}


def faces_of(brief):
    a, _ = brief_axes(brief)
    ts = build_system(a, "#2F6FDB", audience=brief_audience(brief)).tokens
    return {r: fonts.BY_FAMILY[ts.resolve(f"type.face.{r}")[0]]
            for r in ("display", "text", "arabic", "arabic-display")}


def test_a_care_app_gets_a_sans_display_face_and_a_ui_arabic_face():
    f = faces_of({**CARE, "product_type": "app"})
    assert f["display"].generic == "sans-serif", f["display"].family
    assert f["arabic"].generic == "sans-serif", f["arabic"].family
    assert f["arabic-display"].generic == "sans-serif", f["arabic-display"].family


def test_the_same_brief_as_an_editorial_product_may_take_a_serif():
    f = faces_of({**CARE, "product_type": "editorial"})
    assert f["display"].generic == "serif", f["display"].family


def test_without_product_type_the_faces_stay_where_the_axes_put_them():
    a, _ = brief_axes(CARE)
    assert faces_of(CARE)["display"] == fonts.choose(a).display


def test_the_book_target_is_continuous_in_type_personality_and_formality():
    for depth in (0.25, 0.5, 1.0):
        for axis in ("type_personality", "formality"):
            values = [fonts.book_target(axes(**{axis: t / 10}), depth) for t in range(11)]
            assert values == sorted(values) and values[-1] > values[0], (depth, axis)
            assert all(abs(b - a) <= 0.06 for a, b in zip(values, values[1:]))
    assert fonts.book_target(axes(type_personality=1.0, formality=1.0), 0.0) == 0.0
    assert BOOK_DEPTH["app"] == 0.0 and BOOK_DEPTH["editorial"] == 1.0
    assert sorted(BOOK_DEPTH) == sorted(PRODUCT_TYPES)


@pytest.mark.parametrize("given, want", [("app", "app"), ("Marketing site", "marketing-site"),
                                         ("marketing-site", "marketing-site")])
def test_product_type_reads_its_values(given, want):
    assert read_audience({"product_type": given}).product_type == want
    assert "product_type" in FIELDS


def test_a_bad_product_type_names_the_field_and_the_choices():
    with pytest.raises(AudienceError) as exc:
        read_audience({"product_type": "website"})
    assert str(exc.value) == ("brief field product_type is 'website'; use one of app, "
                              "software, marketing-site, editorial, commerce")


def test_product_type_has_a_line_in_who_it_is_for():
    a, _ = brief_axes({**CARE, "product_type": "app"})
    lines = [e.line() for e in effects(read_audience({**CARE, "product_type": "app"}), a)]
    line = next(x for x in lines if "product" in x)
    assert "sans" in line and "app" in line, line


# ---------------------------------------------------------------- 3. sizes

def test_the_landing_display_step_reads_as_a_hero():
    for c in (0.0, 0.35, 0.5, 1.0):
        for f in (0.0, 0.5, 1.0):
            ts = build_system(axes(contrast=c, formality=f), "#2F6FDB").tokens
            display, hero = px(ts, "type.text.display"), px(ts, "type.text.hero")
            assert display >= 56 and display / hero >= MIN_LEVEL_RATIO, (c, f, display, hero)


def test_the_landing_display_rises_with_contrast_and_falls_with_formality():
    by_contrast = [character.landing_display_px(axes(contrast=t / 10)) for t in range(11)]
    by_formality = [character.landing_display_px(axes(formality=t / 10)) for t in range(11)]
    assert by_contrast == sorted(by_contrast) and by_contrast[-1] > by_contrast[0]
    assert by_formality == sorted(by_formality, reverse=True)
    assert by_formality[0] > by_formality[-1]


def test_the_landing_display_steps_down_on_a_phone_through_its_alias():
    ts = build_system(MID, "#2F6FDB").tokens
    assert PHONE_ROLES[0] == "type.text.display"
    factor = ts.resolve(phone_token("type.text.display"))
    hero_phone = px(ts, "type.text.hero") * ts.resolve(phone_token("type.text.hero"))
    assert 0 < factor < 1 and px(ts, "type.text.display") * factor > hero_phone
    css = to_css(ts)
    assert "--type-text-display-scale: var(--type-phone-display);" in css
    assert "--type-text-display-scale: 1;" in css


def test_the_figure_holds_a_number_band():
    """A proof number reads at the page title's size, so three or four of
    them across a band hold it."""
    for brief in (CARE, {"industry": "security"}, {"industry": "construction"}):
        a, _ = brief_axes(brief)
        ts = build_system(a, "#2F6FDB").tokens
        assert px(ts, "type.text.figure") == px(ts, "type.text.heading-1")
        assert px(ts, "type.text.figure") >= 36, (brief, px(ts, "type.text.figure"))


@pytest.mark.parametrize("density, want", [(0.0, 192), (0.5, 160), (1.0, 128)])
def test_the_landing_gap_matches_the_playbook_at_desktop(density, want):
    ts = build_system(axes(density=density), "#2F6FDB").tokens
    assert dim(ts, "layout.landing-gap.desktop") == want
    for tier in ("phone", "tablet", "laptop", "desktop"):
        assert dim(ts, f"layout.landing-gap.{tier}") >= dim(ts, f"layout.region-gap.{tier}")
    assert "--layout-landing-gap: var(--layout-landing-gap-desktop);" in to_css(ts)


BRANDS = ("#2F6FDB", "#1510F0", "#BBBBBB", "#E0A800", "#7A4B2A", "#0E8A5F")


@pytest.mark.parametrize("brand", BRANDS)
@pytest.mark.parametrize("mode", [LIGHT, DARK])
def test_the_tint_stands_off_the_page(brand, mode):
    for a in (MID, axes(contrast=0.1, warmth=0.9), axes(contrast=0.9, warmth=0.1)):
        ts = build_system(a, brand).tokens
        page, tint = ts.resolve("color.surface.page", mode), ts.resolve("color.surface.tint", mode)
        assert contrast(page, tint) >= TINT_FLOOR, (brand, mode, page, tint)


def test_the_light_tint_sits_between_the_page_and_the_band():
    ts = build_system(MID, "#2F6FDB").tokens
    L = {r: hex_to_oklch(ts.resolve(f"color.surface.{r}", LIGHT))[0]
         for r in ("page", "tint", "band")}
    assert L["page"] > L["tint"] > L["band"], L


def test_the_light_band_chroma_follows_contrast():
    chroma = []
    for c in (0.1, 0.35, 0.6, 0.9):
        ts = build_system(axes(contrast=c), "#1510F0").tokens
        band = hex_to_oklch(ts.resolve("color.surface.band", LIGHT))[1]
        assert band <= character.light_band_chroma(axes(contrast=c)) + 0.002, (c, band)
        chroma.append(band)
    assert chroma == sorted(chroma) and chroma[0] < 0.03 < chroma[-1], chroma


@pytest.mark.parametrize("brand", BRANDS)
def test_the_light_code_surface_is_clean(brand):
    ts = build_system(MID, brand).tokens
    code = ts.resolve("color.surface.code", LIGHT)
    card = ts.resolve("color.surface.card", LIGHT)
    L, C, _ = hex_to_oklch(code)
    assert L >= 0.93 and C <= 0.012, (brand, code)
    assert contrast(code, card) >= CODE_EDGE, (brand, code)


def test_the_code_edge_is_the_container_edge_floor():
    from engine.contracts import EDGE_FLOOR
    assert CODE_EDGE == EDGE_FLOOR

