"""Typography: three faces chosen from the catalog, a rem scale, weight
and tracking along the scale, text roles as DTCG typography composites,
heavier text under high contrast, icons, and the Arabic variant under
dir="rtl"."""
import pytest

from engine.foundations import build_system, fonts, from_dtcg, to_css, to_dtcg
from engine.foundations.foundation import role_types_check
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.typography import (
    CHECKS,
    FOUNDATION,
    arabic_px,
    generate_type,
    latin_px,
    leading,
    ratio,
    weights,
)
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


def axes(**kw):
    values = dict(warmth=0.5, contrast=0.5, density=0.5, geometry=0.5, formality=0.5,
                  motion=0.5, type_personality=0.5)
    values.update(kw)
    return AxisValues(**values)


def px(dim):
    return dim["value"] * (16 if dim["unit"] == "rem" else 1)


@pytest.mark.parametrize("contrast, sizes, r", [
    (0.0, [12, 14, 16, 18, 20, 22, 24, 27, 30], 1.11),
    (0.5, [12, 14, 16, 20, 24, 29, 36, 44, 54], 1.225),
    (1.0, [12, 14, 16, 21, 29, 38, 52, 69, 93], 1.34),
])
def test_scale_ratio_follows_the_contrast_axis(contrast, sizes, r):
    assert latin_px(axes(contrast=contrast)) == sizes
    assert ratio(axes(contrast=contrast)) == r


def test_arabic_sizes_follow_the_faces_ratio_and_are_never_equal():
    choice = fonts.choose(axes())
    scale = fonts.arabic_scale(choice.text, choice.arabic)
    assert scale == 1.15
    latin = latin_px(axes())
    arabic = arabic_px(latin, scale)
    assert arabic == [14, 16, 18, 23, 28, 33, 41, 51, 62]
    assert all(a >= lat + 1 and a <= lat * 1.2 for a, lat in zip(arabic, latin))


def test_three_faces_with_metric_matched_fallbacks():
    ts = generate_type(axes()).tokens
    assert ts.resolve("type.face.display") == ["Outfit", "Outfit Fallback", "sans-serif"]
    assert ts.resolve("type.face.text") == ["Noto Sans", "Noto Sans Fallback", "system-ui",
                                            "sans-serif"]
    assert ts.resolve("type.face.mono") == ["IBM Plex Mono", "IBM Plex Mono Fallback",
                                            "ui-monospace", "monospace"]
    assert ts.resolve("type.face.arabic")[:3] == ["Noto Sans Arabic", "Noto Sans Arabic Fallback",
                                                  "Noto Sans"]
    assert ts.resolve("type.face.arabic-display")[0] == "Alexandria"


def test_display_styles_use_the_display_face_and_reading_styles_the_text_face():
    ts = generate_type(axes()).tokens
    for role in ("type.text.hero", "type.text.heading-1", "type.text.section-title",
                 "type.text.figure"):
        assert ts.get(role).value["fontFamily"] == "{type.face.display}", role
    for role in ("type.text.heading-2", "type.text.heading-3", "type.text.body",
                 "type.text.ui", "type.text.fine"):
        assert ts.get(role).value["fontFamily"] == "{type.face.text}", role
    assert ts.get("type.text.code").value["fontFamily"] == "{type.face.mono}"


def test_sizes_are_rem_and_roles_are_composites():
    ts = generate_type(axes()).tokens
    assert all(t.value["unit"] == "rem" for t in ts.tokens() if t.path.startswith("type.size."))
    body = ts.get("type.text.body")
    assert body.type == "typography" and body.value == {
        "fontFamily": "{type.face.text}", "fontSize": "{type.size.latin.3}",
        "fontWeight": "{type.weight.400}", "letterSpacing": "{type.tracking.0}",
        "lineHeight": "{type.leading.latin.3}"}


@pytest.mark.parametrize("contrast, formality, hero, heading", [
    (0.5, 0.5, 600, 600), (1.0, 0.0, 800, 700), (0.0, 1.0, 300, 500)])
def test_weight_eases_from_the_display_weight_to_the_heading_weight(contrast, formality, hero,
                                                                     heading):
    a = axes(contrast=contrast, formality=formality)
    w = weights(a, fonts.choose(a), latin_px(a))
    assert (w["type.text.hero"], w["type.text.heading-3"]) == (hero, heading)
    order = [w[r] for r in ("type.text.hero", "type.text.heading-1", "type.text.section-title",
                            "type.text.heading-2", "type.text.heading-3")]
    assert order == sorted(order, reverse=hero > heading)


def test_tracking_tightens_toward_the_hero_and_labels_open_up():
    ts = generate_type(axes()).tokens
    track = [ts.resolve(r)["letterSpacing"]["value"] for r in (
        "type.text.hero", "type.text.heading-1", "type.text.section-title",
        "type.text.heading-2")]
    assert track == [-1.1, -0.71, -0.43, -0.09]
    assert ts.resolve("type.text.label")["letterSpacing"]["value"] > 0
    assert ts.resolve("type.text.body")["letterSpacing"]["value"] == 0


def test_high_contrast_makes_text_styles_heavier_but_not_display_styles():
    ts = generate_type(axes()).tokens
    high = "contrast:high"
    assert ts.resolve("type.text.body", high)["fontWeight"] == 500
    assert ts.resolve("type.text.ui", high)["fontWeight"] == 600
    assert ts.resolve("type.text.hero", high)["fontWeight"] == \
        ts.resolve("type.text.hero")["fontWeight"]
    assert ts.resolve("type.text.body", "contrast:high,direction:rtl")["fontWeight"] == 500


def test_rtl_switches_face_size_leading_and_drops_tracking():
    ts = generate_type(axes()).tokens
    ltr, rtl = ts.resolve("type.text.heading-1", "direction:ltr"), ts.resolve(
        "type.text.heading-1", "direction:rtl")
    assert rtl["fontFamily"][0] == "Alexandria"
    assert px(rtl["fontSize"]) == 51 and px(ltr["fontSize"]) == 44
    assert rtl["lineHeight"] == round(ltr["lineHeight"] + 0.2, 2)
    assert ltr["letterSpacing"]["value"] < 0 and rtl["letterSpacing"]["value"] == 0
    body = ts.resolve("type.text.body", "direction:rtl")
    assert body["fontFamily"][0] == "Noto Sans Arabic"
    code = ts.resolve("type.text.code", "direction:rtl")
    assert code["fontFamily"][0] == "IBM Plex Mono"
    # Arabic sizing is for Arabic glyphs: code keeps its Latin size and
    # leading under rtl; it changes only its weight under high contrast.
    assert code == ts.resolve("type.text.code", "direction:ltr")
    assert set(ts.get("type.text.code").modes) == {"contrast:high"}


def test_body_text_is_open_and_never_tight():
    assert leading(axes(density=0.0))[3] == 1.6 and leading(axes(density=1.0))[3] == 1.5
    ts = generate_type(axes()).tokens
    for mode in ("direction:ltr", "direction:rtl"):
        body = ts.resolve("type.text.body", mode)
        assert px(body["fontSize"]) >= 16 and body["lineHeight"] >= 1.5
        assert body["letterSpacing"]["value"] == 0


def test_icons_follow_body_text_and_the_display_weight():
    ts = generate_type(axes()).tokens
    assert [px(ts.resolve(f"type.icon.size.{n}")) for n in ("inline", "control", "feature")] == \
        [16, 20, 40]
    assert ts.resolve("type.icon.stroke") == 1.75
    heavy = generate_type(axes(contrast=1.0, formality=0.0)).tokens
    assert heavy.resolve("type.icon.stroke") > ts.resolve("type.icon.stroke")


def test_runs_name_the_face_of_the_other_script():
    ts = generate_type(axes()).tokens
    assert ts.get("type.run.latin").value == "{type.face.text}"
    assert ts.get("type.run.arabic").value == "{type.face.arabic}"
    assert not generate_type(axes(), arabic=False).tokens.has("type.run.arabic")


def test_without_arabic_there_is_no_rtl_variant():
    ts = generate_type(axes(), arabic=False).tokens
    assert not ts.has("type.face.arabic") and not ts.has("type.size.arabic.3")
    assert all("direction" not in k for t in ts.tokens() for k in t.modes)
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed


@pytest.mark.parametrize("contrast, density, personality, formality", [
    (c, d, p, f) for c in (0.0, 0.5, 1.0) for d in (0.0, 1.0) for p in (0.0, 0.5, 1.0)
    for f in (0.0, 1.0)])
def test_every_axis_mix_is_valid_and_passes(contrast, density, personality, formality):
    a = axes(contrast=contrast, density=density, type_personality=personality,
             formality=formality)
    ts = generate_type(a).tokens
    assert validate(ts) == []
    report = gate(ts, [], CHECKS)
    assert report.passed and report.rules_checked == 21


def _hand():
    ts = TokenSet()
    ts.add(Token("type.f.a", "fontFamily", ["A", "serif"]))
    ts.add(Token("type.face.arabic", "fontFamily", ["B", "serif"]))
    ts.add(Token("type.size.x", "dimension", {"value": 14, "unit": "px"}))
    ts.add(Token("type.s.b", "dimension", {"value": 1.25, "unit": "rem"}))
    ts.add(Token("type.w.a", "fontWeight", 400))
    ts.add(Token("type.t.a", "dimension", {"value": -0.5, "unit": "px"}))
    ts.add(Token("type.l.a", "number", 1.2))
    ts.add(Token("type.text.body", "typography", {
        "fontFamily": "{type.f.a}", "fontSize": "{type.size.x}", "fontWeight": "{type.w.a}",
        "letterSpacing": "{type.t.a}", "lineHeight": "{type.l.a}"},
        modes={"direction:rtl": {"fontFamily": "{type.face.arabic}", "fontSize": "{type.s.b}",
                                 "fontWeight": "{type.w.a}", "letterSpacing": "{type.t.a}",
                                 "lineHeight": "{type.l.a}"}}, layer="semantic"))
    return ts


def test_checks_name_the_token_and_the_fix():
    report = gate(_hand(), [], CHECKS, raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "type.text.body (direction:ltr) is 14px; it needs at least 16px to stay readable, so "
        "point its fontSize at a larger step",
        "type.text.body (direction:ltr) has line height 1.2; running text needs 1.5 or more "
        "(1.4.8), so point it at a taller leading",
        "type.text.body (direction:rtl) has line height 1.2; running text needs 1.5 or more "
        "(1.4.8), so point it at a taller leading",
        "type.text.body (direction:ltr) tightens letters to -0.5px; running text keeps 0 or "
        "more, so point it at type.tracking.0",
        "type.text.body (direction:rtl) tightens letters to -0.5px; running text keeps 0 or "
        "more, so point it at type.tracking.0",
        "type.text.body (direction:rtl) spaces letters by -0.5px; letter spacing breaks Arabic "
        "joins, so point it at type.tracking.0",
        "type.text.body (direction:rtl) is 20px against its Latin 14px; Arabic reads at least "
        "1px and at most a fifth larger than the Latin size at the same step, so point it at "
        "the Arabic size for that step",
        "type.text.body (direction:rtl) has line height 1.2, not taller than its Latin 1.2; "
        "Arabic needs room for its marks, so point it at the Arabic leading",
        "type.text.body (direction:ltr) is 14px through type.size.x; sizes in rem follow the "
        "reader's default text size, so point its fontSize at a size in rem or express "
        "type.size.x in rem"]
    assert [(f.check, f.criterion) for f in report.failures] == [
        ("type-sizes", "system"), ("reading-leading", "1.4.8"), ("reading-leading", "1.4.8"),
        ("reading-tracking", "system"), ("reading-tracking", "system"),
        ("arabic-text", "system"), ("arabic-text", "system"), ("arabic-text", "system"),
        ("rem-sizes", "system")]


def test_every_axis_but_motion_moves_typography():
    def dump(a):
        return [(t.path, t.value, t.modes) for t in generate_type(a).tokens.tokens()]
    base = dump(axes())
    assert dump(axes(motion=1.0)) == base
    for name in ("warmth", "contrast", "density", "geometry", "formality", "type_personality"):
        assert dump(axes(**{name: 0.0})) != base or dump(axes(**{name: 1.0})) != base, name


def test_dtcg_round_trip_and_rtl_css():
    ts = generate_type(axes()).tokens
    doc = to_dtcg(ts)
    assert doc["type"]["text"]["body"]["$value"]["fontSize"] == "{type.size.latin.3}"
    assert to_dtcg(from_dtcg(doc)) == doc
    css = to_css(build_system(axes(), "#3366FF").tokens)
    assert '  --type-face-text: "Noto Sans", "Noto Sans Fallback", system-ui, sans-serif;' in css
    rtl = css.split(':root[dir="rtl"] {')[1].split("}")[0]
    assert "  --type-text-body-font-family: var(--type-face-arabic);" in rtl
    assert "  --type-text-body-letter-spacing: var(--type-tracking-0);" in rtl
    assert "  --type-text-body-font-size: var(--type-size-arabic-3);" in rtl


def test_only_the_leading_rule_cites_wcag():
    ids = {c.id: c.criterion for c in CHECKS}
    assert ids == {"type-sizes": "system", "reading-leading": "1.4.8",
                   "reading-tracking": "system", "arabic-text": "system",
                   "rem-sizes": "system", "type-hierarchy": "system",
                   "high-contrast-weights": "system", "icon-sizes": "system",
                   "strong-weight": "system"}


def test_a_role_of_the_wrong_type_is_named_once_not_a_crash():
    ts = _hand()
    ts.add(Token("type.text.fine", "dimension", "{type.s.b}", layer="semantic"))
    ts.add(Token("type.text.hero", "number", "{type.l.a}", layer="semantic"))
    assert validate(ts) == []
    report = gate(ts, [], (role_types_check([FOUNDATION]),) + CHECKS, raise_on_fail=False)
    mistyped = [f.message for f in report.failures if f.check == "role-types"]
    assert mistyped == [
        "type.text.hero is a number but its role expects a typography; point it at a "
        "typography token",
        "type.text.fine is a dimension but its role expects a typography; point it at a "
        "typography token"]
    assert not any("could not read" in f.message for f in report.failures)
    assert not any("type.text.hero" in f.message or "type.text.fine" in f.message
                   for f in report.failures if f.check != "role-types")


def _generated_with(role, rtl=None):
    """The default generated set with one role's direction:rtl override
    replaced (rtl=None drops it)."""
    src = generate_type(axes()).tokens
    ts = TokenSet()
    for t in src.tokens():
        if t.path == role:
            t = Token(role, "typography", t.value,
                      modes={"direction:rtl": rtl} if rtl else {}, layer="semantic")
        ts.add(t)
    return ts


def _arabic_failures(ts):
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    others = [f.message for f in report.failures if f.check != "arabic-text"]
    assert others == []
    return [f.message for f in report.failures if f.check == "arabic-text"]


def test_a_role_without_an_rtl_override_fails_every_arabic_rule():
    ts = _generated_with("type.text.heading-1")
    assert validate(ts) == []
    assert _arabic_failures(ts) == [
        "type.text.heading-1 (direction:rtl) is set in Outfit, not type.face.arabic-display; "
        "Arabic text needs its own face, so point its direction:rtl fontFamily at "
        "type.face.arabic-display",
        "type.text.heading-1 (direction:rtl) spaces letters by -0.71px; letter spacing breaks "
        "Arabic joins, so point it at type.tracking.0",
        "type.text.heading-1 (direction:rtl) is 44px against its Latin 44px; Arabic reads at "
        "least 1px and at most a fifth larger than the Latin size at the same step, so point "
        "it at the Arabic size for that step",
        "type.text.heading-1 (direction:rtl) has line height 1.1, not taller than its Latin "
        "1.1; Arabic needs room for its marks, so point it at the Arabic leading"]


def test_a_role_pointing_back_at_the_latin_face_fails():
    rtl = dict(generate_type(axes()).tokens.get("type.text.body").modes["direction:rtl"],
               fontFamily="{type.face.text}")
    ts = _generated_with("type.text.body", rtl)
    assert validate(ts) == []
    assert _arabic_failures(ts) == [
        "type.text.body (direction:rtl) is set in Noto Sans, not type.face.arabic; "
        "Arabic text needs its own face, so point its direction:rtl fontFamily at "
        "type.face.arabic"]


def test_the_code_role_keeps_its_face_without_an_override():
    ts = _generated_with("type.text.code")
    assert validate(ts) == [] and _arabic_failures(ts) == []


def test_code_is_exempt_from_the_arabic_face_size_and_leading_rules():
    code = generate_type(axes()).tokens.get("type.text.code").value
    # Arabic size and leading under rtl: allowed, not required.
    arabic_metrics = dict(code, fontSize="{type.size.arabic.2}",
                          lineHeight="{type.leading.arabic.3}")
    ts = _generated_with("type.text.code", arabic_metrics)
    assert validate(ts) == [] and _arabic_failures(ts) == []
    # Letter spacing still breaks Arabic joins in comments and strings.
    tight = dict(code, letterSpacing="{type.tracking.step-9}")
    ts = _generated_with("type.text.code", tight)
    assert validate(ts) == []
    assert _arabic_failures(ts) == [
        "type.text.code (direction:rtl) spaces letters by -1.1px; letter spacing breaks "
        "Arabic joins, so point it at type.tracking.0"]


def test_a_latin_only_build_passes_the_arabic_rules():
    ts = generate_type(axes(), arabic=False).tokens
    assert _arabic_failures(ts) == []
    result = build_system(axes(), "#3366FF", arabic=False)
    assert result.report.passed and not result.tokens.has("type.face.arabic")


def test_a_px_size_reached_outside_the_size_tree_fails_in_both_directions():
    src = generate_type(axes()).tokens
    ts = TokenSet()
    ts.add(Token("type.px16", "dimension", {"value": 16, "unit": "px"}))
    for t in src.tokens():
        if t.path == "type.text.body":
            rtl = dict(t.modes["direction:rtl"], fontSize="{type.px16}")
            t = Token(t.path, t.type, dict(t.value, fontSize="{type.px16}"),
                      modes={"direction:rtl": rtl}, layer="semantic")
        ts.add(t)
    assert validate(ts) == []
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [(f.check, f.message) for f in report.failures if f.check == "rem-sizes"] == [
        ("rem-sizes", "type.text.body (direction:ltr) is 16px through type.px16; sizes in rem "
         "follow the reader's default text size, so point its fontSize at a size in rem or "
         "express type.px16 in rem"),
        ("rem-sizes", "type.text.body (direction:rtl) is 16px through type.px16; sizes in rem "
         "follow the reader's default text size, so point its fontSize at a size in rem or "
         "express type.px16 in rem")]


def test_an_unused_px_size_step_is_named_once():
    ts = generate_type(axes()).tokens
    ts.add(Token("type.size.extra", "dimension", {"value": 15, "unit": "px"}))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "type.size.extra is in px; sizes in rem follow the reader's default text size, so "
        "express it in rem"]


def test_a_mono_label_switches_to_the_arabic_face_under_rtl():
    technical = axes(warmth=0.0, type_personality=0.0)
    ts = generate_type(technical).tokens
    assert ts.get("type.text.label").value["fontFamily"] == "{type.face.mono}"
    rtl = ts.resolve("type.text.label", "direction:rtl")
    assert rtl["fontFamily"] == ts.resolve("type.face.arabic")
    assert rtl["letterSpacing"]["value"] == 0


HIGH_CONTEXTS = ("contrast:high,direction:ltr", "contrast:high,direction:rtl")


@pytest.mark.parametrize("contrast", [0.0, 0.2, 0.5, 0.8, 1.0])
@pytest.mark.parametrize("personality, warmth, geometry", [
    (0.5, 0.5, 0.5), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (0.5, 0.9, 0.9), (0.9, 0.2, 0.3)])
@pytest.mark.parametrize("arabic", [True, False])
def test_strong_stays_200_above_body_under_high_contrast(contrast, personality, warmth,
                                                         geometry, arabic):
    ax = axes(contrast=contrast, type_personality=personality, warmth=warmth, geometry=geometry)
    ts = generate_type(ax, arabic=arabic).tokens
    for mode in HIGH_CONTEXTS if arabic else ("contrast:high",):
        strong = ts.resolve("type.strong", mode)
        body = ts.resolve("type.text.body", mode)["fontWeight"]
        assert strong - body >= 200, (mode, strong, body)
    assert ts.resolve("type.strong") == ts.resolve("type.text.heading-3")["fontWeight"]
    assert gate(ts, [], CHECKS, raise_on_fail=False).passed


def test_a_low_contrast_brand_keeps_its_emphasis_under_high_contrast():
    ts = generate_type(axes(contrast=0.1, formality=0.9)).tokens
    assert ts.resolve("type.strong") == 500
    assert ts.resolve("type.text.body", "contrast:high")["fontWeight"] == 500
    assert ts.resolve("type.strong", "contrast:high") == 700


def test_the_strong_check_names_the_context_and_the_fix():
    ts = TokenSet()
    for t in generate_type(axes()).tokens.tokens():
        ts.add(t if t.path != "type.strong" else
               Token("type.strong", "fontWeight", "{type.weight.600}", layer="semantic"))
    report = gate(ts, [], CHECKS, raise_on_fail=False)
    found = [f.message for f in report.failures if f.check == "strong-weight"]
    assert found and found[0].startswith(
        "type.strong (contrast:high,direction:ltr) is weight 600, only 100 above "
        "type.text.body at 500; bold words must stay at least 200 above body text under high "
        "contrast, so point its contrast:high value at type.weight.700 or heavier")


@pytest.mark.parametrize("brand_axes", [
    axes(warmth=0.8, contrast=0.9, density=0.2, geometry=0.9, formality=0.3, motion=0.9,
         type_personality=0.8),
    axes(warmth=0.8, formality=0.3, type_personality=0.55, contrast=0.9),
])
def test_every_weight_a_style_names_is_one_its_face_ships(brand_axes):
    ts = generate_type(brand_axes).tokens
    c = fonts.choose(brand_axes)
    ctxs = ("contrast:standard,direction:ltr", "contrast:high,direction:ltr",
            "contrast:standard,direction:rtl", "contrast:high,direction:rtl")
    for role in ("type.text.body", "type.text.ui", "type.text.label", "type.text.heading-2",
                 "type.text.hero"):
        for mode in ctxs:
            v = ts.resolve(role, mode)
            face = fonts.BY_FAMILY[v["fontFamily"][0]]
            assert _ships(face, v["fontWeight"]), (role, mode, face.family, v["fontWeight"])
    for mode in ctxs[2:]:
        assert _ships(c.arabic, ts.resolve("type.strong", mode)), mode


def _ships(face, weight):
    if face.stops:
        return weight in face.stops
    return face.weights[0] <= weight <= face.weights[1]


def test_the_static_arabic_case_is_exercised():
    c = fonts.choose(axes(warmth=0.8, formality=0.3, type_personality=0.55, contrast=0.9))
    assert c.arabic.family == "Tajawal"
    ts = generate_type(axes(warmth=0.8, formality=0.3, type_personality=0.55,
                            contrast=0.9)).tokens
    assert ts.resolve("type.text.ui", "contrast:high,direction:rtl")["fontWeight"] == 700
