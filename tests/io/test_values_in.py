"""Reading a value written as text (CSS, a Tailwind theme, a markdown table)
into a token type and our internal literal. Anything it cannot read for
certain comes back as a reason, never a guess."""
import pytest

from engine.io.values_in import NotRead, css_alias, read_value, split_top


@pytest.mark.parametrize("text,want", [
    ("#36f", ("color", "#3366FF")),
    ("#3366ff", ("color", "#3366FF")),
    ("#3366FFCC", ("color", "#3366FFCC")),
    ("#3366FFFF", ("color", "#3366FF")),
    ("#36fc", ("color", "#3366FFCC")),
    ("rgb(51, 102, 255)", ("color", "#3366FF")),
    ("rgb(51 102 255 / 50%)", ("color", "#3366FF80")),
    ("rgba(0,0,0,0.1)", ("color", "#0000001A")),
    ("rgb(20% 40% 100%)", ("color", "#3366FF")),
    ("hsl(225 100% 60%)", ("color", "#3366FF")),
    ("hsla(0, 0%, 100%, 1)", ("color", "#FFFFFF")),
    ("oklch(100% 0 0)", ("color", "#FFFFFF")),
    ("oklch(0 0 0 / 0.5)", ("color", "#00000080")),
    ("white", ("color", "#FFFFFF")),
    ("BLACK", ("color", "#000000")),
    ("transparent", ("color", "#00000000")),
])
def test_colors(text, want):
    assert read_value(text) == want


@pytest.mark.parametrize("text,want", [
    ("16px", ("dimension", {"value": 16, "unit": "px"})),
    ("1.5rem", ("dimension", {"value": 1.5, "unit": "rem"})),
    ("-0.25px", ("dimension", {"value": -0.25, "unit": "px"})),
    (".5rem", ("dimension", {"value": 0.5, "unit": "rem"})),
    ("200ms", ("duration", {"value": 200, "unit": "ms"})),
    ("0.2s", ("duration", {"value": 0.2, "unit": "s"})),
    ("1.5", ("number", 1.5)),
    ("0", ("number", 0)),
    ("600", ("number", 600)),
    ("cubic-bezier(0.2, 0, 0, 1)", ("cubicBezier", [0.2, 0, 0, 1])),
    ("ease-out", ("cubicBezier", [0, 0, 0.58, 1])),
    ("linear", ("cubicBezier", [0, 0, 1, 1])),
    ('"Source Sans 3", system-ui, sans-serif', ("fontFamily", ["Source Sans 3", "system-ui",
                                                               "sans-serif"])),
    ("'Readex Pro'", ("fontFamily", ["Readex Pro"])),
    ("ui-monospace, monospace", ("fontFamily", ["ui-monospace", "monospace"])),
    ("monospace", ("fontFamily", ["monospace"])),
    ("dashed", ("strokeStyle", "dashed")),
])
def test_dimensions_durations_numbers_curves_faces_and_strokes(text, want):
    assert read_value(text) == want


def test_shadows_read_every_layer_in_order():
    kind, value = read_value("0 1px 3px 0 rgba(0,0,0,0.1), inset 0 0 0 1px #FFFFFF")
    assert kind == "shadow"
    assert value == [
        {"color": "#0000001A", "offsetX": {"value": 0, "unit": "px"},
         "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 3, "unit": "px"},
         "spread": {"value": 0, "unit": "px"}},
        {"color": "#FFFFFF", "offsetX": {"value": 0, "unit": "px"},
         "offsetY": {"value": 0, "unit": "px"}, "blur": {"value": 0, "unit": "px"},
         "spread": {"value": 1, "unit": "px"}, "inset": True}]


def test_a_shadow_with_two_lengths_gets_no_blur_or_spread():
    assert read_value("#000 0 2px")[1] == [
        {"color": "#000000", "offsetX": {"value": 0, "unit": "px"},
         "offsetY": {"value": 2, "unit": "px"}, "blur": {"value": 0, "unit": "px"},
         "spread": {"value": 0, "unit": "px"}}]


@pytest.mark.parametrize("text,reason", [
    ("1.5em", "1.5em is relative to the parent's font size, so it has no fixed value; write it "
              "in px or rem"),
    ("50%", "50% is relative to its container, so it has no fixed value; write it in px or rem"),
    ("100vw", "100vw is relative to the viewport, so it has no fixed value; write it in px or "
              "rem"),
    ("calc(1rem + 2px)", "calc(1rem + 2px) is computed by the browser; write the value it "
                         "computes to"),
    ("color-mix(in srgb, red 50%, blue)", "color-mix(in srgb, red 50%, blue) is computed by the "
                                          "browser; write the value it computes to"),
    ("rebeccapurple", "rebeccapurple is a single word that could be a color name, a font name "
                      "or a keyword; write a color as hex, and quote a font name"),
    ("Inter", "Inter is a single word that could be a color name, a font name or a keyword; "
              "write a color as hex, and quote a font name"),
    ("lab(50% 20 30)", "lab(50% 20 30) is in a color space this reader does not convert; write "
                       "it as hex or oklch()"),
    ("#12345", "#12345 is not a hex color; use #RGB, #RGBA, #RRGGBB or #RRGGBBAA"),
    ("rgb(1, 2)", "rgb(1, 2) needs three channels; write it as rgb(r g b) or rgb(r g b / a)"),
    ("cubic-bezier(2, 0, 0, 1)", "cubic-bezier(2, 0, 0, 1) has an x outside 0 to 1; x1 and x2 "
                                 "must sit from 0 to 1"),
    ("", "the value is empty; write a value or remove the entry"),
])
def test_what_it_cannot_read_comes_back_as_a_reason(text, reason):
    with pytest.raises(NotRead) as exc:
        read_value(text)
    assert str(exc.value) == reason


def test_references_to_other_custom_properties():
    assert css_alias("var(--brand-500)") == ("brand-500", "")
    assert css_alias("var( --space-4 , 16px )") == ("space-4", "16px")
    assert css_alias("16px") is None
    with pytest.raises(NotRead, match="var\\(--a\\) var\\(--b\\) joins several values"):
        css_alias("var(--a) var(--b)")


def test_top_level_split_keeps_commas_inside_parentheses():
    assert split_top("rgb(0, 0, 0) 1px, 2px 3px") == ["rgb(0, 0, 0) 1px", "2px 3px"]
    assert split_top('"A, B", serif') == ['"A, B"', "serif"]


def test_unitless_hsl_saturation_and_lightness_are_percentages():
    # CSS Color 4: hsl(225 100 60) is hsl(225 100% 60%), never a clamped guess.
    assert read_value("hsl(225 100 60)") == ("color", "#3366FF")


def test_a_fallback_may_itself_hold_a_nested_reference():
    assert css_alias("var(--a, var(--b, rgb(0 0 0)))") == ("a", "var(--b, rgb(0 0 0))")


def test_system_detect_reads_colors_and_references_through_this_reader():
    """`system detect` and the importers read one color the same way:
    detect reads through read_value, maps out-of-gamut oklch the same way,
    and keeps its lenient reading only for what the importer refuses."""
    import random

    from engine.existing import normalize_hex, resolve_css_var

    rnd = random.Random(4)
    for _ in range(3000):
        r, g, b = (rnd.randint(0, 255) for _ in range(3))
        h, s, lt = rnd.uniform(0, 360), rnd.uniform(0, 100), rnd.uniform(0, 100)
        L, C, H = rnd.uniform(0, 1), rnd.uniform(0, 0.12), rnd.uniform(0, 360)
        for text in (f"rgb({r}, {g}, {b})", f"hsl({h:.2f} {s:.2f}% {lt:.2f}%)",
                     f"hsl({h:.2f} {s:.2f} {lt:.2f})", f"oklch({L:.4f} {C:.4f} {H:.2f})"):
            try:
                want = read_value(text)[1][:7]
            except NotRead:
                continue
            assert normalize_hex(text) == want, text
    assert normalize_hex("#36fc") == "#3366FF" and normalize_hex("white") == ""
    for text in TAILWIND_V4:
        assert normalize_hex(text) == read_value(text)[1]
    # The DTCG object form maps through the same function.
    assert normalize_hex({"colorSpace": "oklch", "components": [0.623, 0.214, 259.815]}) \
        == read_value("oklch(0.623 0.214 259.815)")[1]
    props = {"--a": "var(--b, var(--c, #111111))", "--x": "var(--y) var(--z)"}
    assert resolve_css_var("var(--a)", props) == "#111111"
    assert resolve_css_var("var(--x)", props) == "var(--y) var(--z)"


# Tailwind v4's blue-500, green-500 and red-600: written in oklch, outside
# sRGB. The hex each maps to is the widely used hex for these steps.
TAILWIND_V4 = {
    "oklch(62.3% 0.214 259.815)": "#2B7FFF",
    "oklch(72.3% 0.219 149.579)": "#00C950",
    "oklch(57.7% 0.245 27.325)": "#E7000B",
}
# Tailwind v4's red-500 sits inside sRGB: read as it is, with no report line.
TAILWIND_V4_RED_500 = "oklch(63.7% 0.237 25.331)"


@pytest.mark.parametrize("text", sorted(TAILWIND_V4))
def test_out_of_gamut_oklch_is_mapped_into_srgb_never_refused(text):
    """An out-of-gamut color is mapped by CSS Color 4 gamut mapping, never
    refused: lower the chroma, keep lightness and hue, until the color sits
    inside sRGB within a just visible step."""
    from engine.foundations.color_math import hex_to_oklch

    mapped = []
    kind, hx = read_value(text, mapped)
    assert (kind, hx) == ("color", TAILWIND_V4[text])
    assert [(m.original, m.hex) for m in mapped] == [(text, hx)]
    assert 0 < mapped[0].distance < 0.1
    L, C, H = hex_to_oklch(hx)
    body = text[6:-1].split()
    assert abs(L - float(body[0][:-1]) / 100) < 0.01
    assert abs((H - float(body[2]) + 180) % 360 - 180) < 3
    assert C < float(body[1])


def test_the_mapping_is_deterministic():
    runs = [[read_value(t) for t in sorted(TAILWIND_V4)] for _ in range(3)]
    assert runs[0] == runs[1] == runs[2]


def test_an_in_gamut_color_is_unchanged_and_not_reported():
    from engine.foundations.color_math import oklch_to_hex

    mapped = []
    for L, C, H in ((0.5, 0.1, 250), (0.9, 0.02, 90), (0.2, 0.05, 20)):
        assert read_value(f"oklch({L} {C} {H})", mapped) == ("color", oklch_to_hex(L, C, H))
    assert read_value("#3366FF", mapped) == ("color", "#3366FF")
    assert read_value(TAILWIND_V4_RED_500, mapped) == ("color", "#FB2C36")
    assert mapped == []


def test_oklab_reads_and_maps_the_same_way():
    import math

    a, b = 0.214 * math.cos(math.radians(259.815)), 0.214 * math.sin(math.radians(259.815))
    mapped = []
    assert read_value(f"oklab(0.623 {a:.6f} {b:.6f})", mapped) \
        == read_value("oklch(62.3% 0.214 259.815)")
    assert len(mapped) == 1
    assert read_value("oklab(1 0 0)") == ("color", "#FFFFFF")
    assert read_value("oklab(0 0 0 / 50%)") == ("color", "#00000080")


def test_a_mapped_color_inside_a_shadow_is_reported_too():
    mapped = []
    read_value("0 1px 2px oklch(62.3% 0.214 259.815)", mapped)
    assert [m.original for m in mapped] == ["oklch(62.3% 0.214 259.815)"]


@pytest.mark.parametrize("hue", ["180", "180deg", "0.5turn", "3.141592653589793rad",
                                 "200grad"])
def test_hue_units(hue):
    assert read_value(f"oklch(0.7 0.1 {hue})") == read_value("oklch(0.7 0.1 180)")
    assert read_value(f"hsl({hue} 100% 50%)") == ("color", "#00FFFF")


def test_any_other_hue_unit_is_refused_by_name():
    with pytest.raises(NotRead) as exc:
        read_value("oklch(0.7 0.1 30foo)")
    assert str(exc.value) == ("oklch(0.7 0.1 30foo) writes its hue in foo, which this reader "
                              "does not read; write the hue in deg, turn, rad or grad")


# Tailwind v4 compiles --tw-ring-shadow to this: several values, one of them
# a reference with an empty fallback.
TAILWIND_RING_SHADOW = ("var(--tw-ring-inset,) 0 0 0 calc(3px + var(--tw-ring-offset-width)) "
                        "var(--tw-ring-color, currentcolor)")


@pytest.mark.parametrize("text", ["var(--a, 1px) var(--b)", "var(--a) 1px",
                                  TAILWIND_RING_SHADOW])
def test_a_reference_followed_by_more_is_not_one_reference(text):
    with pytest.raises(NotRead, match="joins several values with var"):
        css_alias(text)


def test_detect_returns_a_value_of_several_references_as_written():
    from engine.existing import resolve_css_var

    props = {"--a": "#111111", "--sh": "var(--a, 0 1px) var(--b)",
             "--ring": TAILWIND_RING_SHADOW}
    assert resolve_css_var("var(--sh)", props) == "var(--a, 0 1px) var(--b)"
    assert resolve_css_var("var(--ring)", props) == TAILWIND_RING_SHADOW


def test_an_empty_fallback_and_a_fallback_with_parens_still_read():
    assert css_alias("var(--tw-ring-inset,)") == ("tw-ring-inset", "")
    assert css_alias("var(--c, rgb(0 0 0 / 50%))") == ("c", "rgb(0 0 0 / 50%)")
    assert css_alias('var(--f, "a)b")') == ("f", '"a)b"')


@pytest.mark.parametrize("text,reason", [
    ("1e999px", "1e999 is not a finite number; write a plain number"),
    ("rgb(nan 0 0)", "rgb(nan 0 0) has a channel that is not a number; write it as hex"),
    ("rgb(0 0 0 / inf)", "rgb(0 0 0 / inf) has a channel that is not a number; write it as hex"),
    ("hsl(inf 50% 50%)", "hsl(inf 50% 50%) has a channel that is not a number; write it as hex"),
    ("oklch(from var(--brand) l c h / 50%)", "oklch(from var(--brand) l c h / 50%) is a "
     "relative color, computed by the browser; write the value it computes to"),
    ("oklch(0.5 0.1)", "oklch(0.5 0.1) needs three channels; write it as oklch(l c h) or "
                       "oklch(l c h / a)"),
    ("hsl(1, 2)", "hsl(1, 2) needs three channels; write it as hsl(h s l) or hsl(h s l / a)"),
    ("1px solid #000", "1px solid #000 is a border shorthand; write its width, style and "
                       "color as separate tokens"),
    ("400 16px/1.5 Inter", "400 16px/1.5 Inter is a font shorthand; write its family, size, "
                           "weight and line height as separate tokens"),
    ("currentColor", "currentColor has no fixed value; it takes the color of the element it "
                     "sits on, so write the color as hex"),
    ("hsl(225, 100, 60)", "hsl(225, 100, 60) writes saturation and lightness without %, which "
                          "the comma syntax does not allow; write hsl(225, 100%, 60%)"),
])
def test_odd_values_are_refused_with_the_right_reason(text, reason):
    with pytest.raises(NotRead) as exc:
        read_value(text)
    assert str(exc.value) == reason


def test_calc_around_a_reference_is_refused_as_computed():
    with pytest.raises(NotRead) as exc:
        css_alias("calc(var(--x) * 2)")
    assert str(exc.value) == ("calc(var(--x) * 2) is computed by the browser; write the value "
                              "it computes to")


def test_a_none_channel_reads_as_zero():
    assert read_value("oklch(none 0.1 180)") == read_value("oklch(0 0.1 180)")
    assert read_value("rgb(0 0 0 / none)") == ("color", "#00000000")
    assert read_value("hsl(none 100% 50%)") == ("color", "#FF0000")


def test_float_noise_at_the_gamut_edge_is_not_reported_as_mapped():
    mapped = []
    # #FF0000 written as oklch with the usual rounding sits a hair outside sRGB.
    assert read_value("oklch(62.8% 0.258 29.234)", mapped) == ("color", "#FF0000")
    assert mapped == []


@pytest.mark.parametrize("text", [
    "opacity 200ms ease, transform 300ms ease",
    "opacity 200ms",
    "color .2s linear, background-color 150ms",
    "fade 1s ease-out",
])
def test_a_transition_list_is_named_not_read_as_a_font_stack(text):
    with pytest.raises(NotRead) as exc:
        read_value(text)
    assert str(exc.value) == (f"{text} is a transition or animation shorthand; write its "
                              "duration and its curve as separate tokens")


@pytest.mark.parametrize("text,names", [
    ('"Inter", system-ui, sans-serif', ["Inter", "system-ui", "sans-serif"]),
    ("Body Sans, ui-sans-serif, sans-serif", ["Body Sans", "ui-sans-serif", "sans-serif"]),
    ('"Font 2s", serif', ["Font 2s", "serif"]),
])
def test_a_font_stack_still_reads_after_the_transition_check(text, names):
    assert read_value(text) == ("fontFamily", names)


@pytest.mark.parametrize("text", ["200ms, 300ms", "0.2s, 150MS, 1s"])
def test_a_bare_list_of_durations_is_named(text):
    with pytest.raises(NotRead) as exc:
        read_value(text)
    assert str(exc.value) == (f"{text} is a list of durations, one per transition or "
                              "animation; write each duration as its own token")


def test_an_unquoted_font_ending_in_a_duration_like_word_is_still_a_font():
    assert read_value("Font 2s, serif") == ("fontFamily", ["Font 2s", "serif"])


@pytest.mark.parametrize("text", ["opacity 200MS ease", "fade 1S ease-out"])
def test_the_duration_in_a_shorthand_is_matched_in_any_case(text):
    with pytest.raises(NotRead) as exc:
        read_value(text)
    assert "is a transition or animation shorthand" in str(exc.value)
