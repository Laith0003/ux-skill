"""Typography: face pairings, a rem scale, text roles as DTCG typography
composites, and the Arabic variant under dir="rtl"."""
import pytest

from engine.foundations import build_system, from_dtcg, to_css, to_dtcg
from engine.foundations.foundation import role_types_check
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.typography import (
    CHECKS,
    FOUNDATION,
    PAIRINGS,
    arabic_px,
    band,
    generate_type,
    latin_px,
    leading,
    ratio,
    tracking,
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


@pytest.mark.parametrize("contrast, sizes", [
    (0.0, [12, 14, 16, 18, 20, 23, 26, 29, 32]),
    (0.5, [12, 14, 16, 20, 24, 29, 36, 44, 54]),
    (1.0, [12, 14, 16, 21, 28, 37, 49, 65, 87]),
])
def test_scale_ratio_follows_the_contrast_axis(contrast, sizes):
    assert latin_px(contrast) == sizes
    assert ratio(contrast) == round(1.125 + 0.2 * contrast, 4)


def test_arabic_sizes_are_one_to_two_px_larger():
    for contrast in (0.0, 0.5, 1.0):
        latin = latin_px(contrast)
        assert all(1 <= a - l <= 2 for a, l in zip(arabic_px(latin), latin))
    assert arabic_px([12, 16, 23, 24, 54]) == [14, 18, 25, 25, 55]


def test_face_pairing_follows_type_personality():
    assert [band(t) for t in (0.0, 0.33, 0.34, 0.65, 0.66, 1.0)] == [
        "geometric", "geometric", "neutral", "neutral", "humanist", "humanist"]
    ts = generate_type(axes(type_personality=1.0)).tokens
    latin, arabic = PAIRINGS["humanist"]
    assert ts.resolve("type.face.latin") == [latin, "system-ui", "sans-serif"]
    assert ts.resolve("type.face.arabic")[:2] == [arabic, latin]


def test_sizes_are_rem_and_roles_are_composites():
    ts = generate_type(axes()).tokens
    assert all(t.value["unit"] == "rem" for t in ts.tokens() if t.path.startswith("type.size."))
    body = ts.get("type.text.body")
    assert body.type == "typography" and body.value == {
        "fontFamily": "{type.face.latin}", "fontSize": "{type.size.latin.3}",
        "fontWeight": "{type.weight.400}", "letterSpacing": "{type.tracking.0}",
        "lineHeight": "{type.leading.latin.3}"}


def test_rtl_switches_face_size_leading_and_drops_tracking():
    ts = generate_type(axes()).tokens
    ltr, rtl = ts.resolve("type.text.heading-1", "direction:ltr"), ts.resolve(
        "type.text.heading-1", "direction:rtl")
    assert rtl["fontFamily"][0] == "IBM Plex Sans Arabic"
    assert px(rtl["fontSize"]) - px(ltr["fontSize"]) == 1
    assert rtl["lineHeight"] == round(ltr["lineHeight"] + 0.2, 2)
    assert ltr["letterSpacing"]["value"] < 0 and rtl["letterSpacing"]["value"] == 0
    code = ts.resolve("type.text.code", "direction:rtl")
    assert code["fontFamily"][0] == "IBM Plex Mono"
    # Arabic sizing is for Arabic glyphs: code keeps its Latin size and
    # leading, so it needs no rtl override at all.
    assert code == ts.resolve("type.text.code", "direction:ltr")
    assert ts.get("type.text.code").modes == {}


def test_body_text_is_open_and_never_tight():
    assert leading(0.0)[3] == 1.6 and leading(1.0)[3] == 1.5
    assert tracking(1.0) == {0: 0.0, 1: -0.25, 2: -0.5, 3: -1.0}
    ts = generate_type(axes()).tokens
    for mode in ("direction:ltr", "direction:rtl"):
        body = ts.resolve("type.text.body", mode)
        assert px(body["fontSize"]) >= 16 and body["lineHeight"] >= 1.5
        assert body["letterSpacing"]["value"] == 0


def test_without_arabic_there_is_no_rtl_variant():
    ts = generate_type(axes(), arabic=False).tokens
    assert not ts.has("type.face.arabic") and not ts.has("type.size.arabic.3")
    assert all(not t.modes for t in ts.tokens())
    assert validate(ts) == [] and gate(ts, [], CHECKS).passed


@pytest.mark.parametrize("contrast, density, personality", [
    (c, d, p) for c in (0.0, 0.5, 1.0) for d in (0.0, 1.0) for p in (0.0, 0.5, 1.0)])
def test_every_axis_mix_is_valid_and_passes(contrast, density, personality):
    a = axes(contrast=contrast, density=density, type_personality=personality)
    ts = generate_type(a).tokens
    assert validate(ts) == []
    report = gate(ts, [], CHECKS)
    assert report.passed and report.rules_checked == 12


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
        "type.text.body (direction:rtl) is +6px against its Latin size; Arabic reads at 1 to 2px "
        "larger at the same step, so point it at the Arabic size for that step",
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


def test_only_its_axes_move_typography():
    base = [(t.path, t.value, t.modes) for t in generate_type(axes()).tokens.tokens()]
    other = axes(warmth=0.0, geometry=1.0, formality=0.0, motion=1.0)
    assert [(t.path, t.value, t.modes) for t in generate_type(other).tokens.tokens()] == base


def test_dtcg_round_trip_and_rtl_css():
    ts = generate_type(axes()).tokens
    doc = to_dtcg(ts)
    assert doc["type"]["text"]["body"]["$value"]["fontSize"] == "{type.size.latin.3}"
    assert to_dtcg(from_dtcg(doc)) == doc
    css = to_css(build_system(axes(), "#3366FF").tokens)
    assert '  --type-face-latin: "IBM Plex Sans", system-ui, sans-serif;' in css
    rtl = css.split(':root[dir="rtl"] {')[1].split("}")[0]
    assert "  --type-text-body-font-family: var(--type-face-arabic);" in rtl
    assert "  --type-text-body-letter-spacing: var(--type-tracking-0);" in rtl
    assert "  --type-text-body-font-size: var(--type-size-arabic-3);" in rtl


def test_only_the_leading_rule_cites_wcag():
    ids = {c.id: c.criterion for c in CHECKS}
    assert ids == {"type-sizes": "system", "reading-leading": "1.4.8",
                   "reading-tracking": "system", "arabic-text": "system",
                   "rem-sizes": "system", "type-hierarchy": "system"}


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
        "type.text.heading-1 (direction:rtl) is set in IBM Plex Sans, not type.face.arabic; "
        "Arabic text needs its own face, so point its direction:rtl fontFamily at "
        "type.face.arabic",
        "type.text.heading-1 (direction:rtl) spaces letters by -0.375px; letter spacing breaks "
        "Arabic joins, so point it at type.tracking.0",
        "type.text.heading-1 (direction:rtl) is +0px against its Latin size; Arabic reads at 1 "
        "to 2px larger at the same step, so point it at the Arabic size for that step",
        "type.text.heading-1 (direction:rtl) has line height 1.1, not taller than its Latin "
        "1.1; Arabic needs room for its marks, so point it at the Arabic leading"]


def test_a_role_pointing_back_at_the_latin_face_fails():
    rtl = dict(generate_type(axes()).tokens.get("type.text.body").modes["direction:rtl"],
               fontFamily="{type.face.latin}")
    ts = _generated_with("type.text.body", rtl)
    assert validate(ts) == []
    assert _arabic_failures(ts) == [
        "type.text.body (direction:rtl) is set in IBM Plex Sans, not type.face.arabic; "
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
    tight = dict(code, letterSpacing="{type.tracking.1}")
    ts = _generated_with("type.text.code", tight)
    assert validate(ts) == []
    assert _arabic_failures(ts) == [
        "type.text.code (direction:rtl) spaces letters by -0.188px; letter spacing breaks "
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
