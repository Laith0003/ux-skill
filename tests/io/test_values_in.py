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
    ("", "the value is empty"),
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
    """BF6's `system detect` and the importers read one color the same way:
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
# sRGB. The hex each maps to is the sRGB fallback Tailwind itself publishes.
TAILWIND_V4 = {
    "oklch(62.3% 0.214 259.815)": "#2B7FFF",
    "oklch(72.3% 0.219 149.579)": "#00C950",
    "oklch(57.7% 0.245 27.325)": "#E7000B",
}
# Tailwind v4's red-500 sits inside sRGB: read as it is, with no report line.
TAILWIND_V4_RED_500 = "oklch(63.7% 0.237 25.331)"


@pytest.mark.parametrize("text", sorted(TAILWIND_V4))
def test_out_of_gamut_oklch_is_mapped_into_srgb_never_refused(text):
    """M4-R5: CSS Color 4 gamut mapping. Lower the chroma, keep lightness
    and hue, until the color sits inside sRGB within a just visible step."""
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
