"""The face catalog: open-license faces with measured metrics, chosen by
the axes, never by a keyword."""
import pytest

from engine.foundations import fonts
from engine.synthesizer.axes import AxisValues

MID = AxisValues(*[0.5] * 7)


def test_every_face_is_open_license_with_whole_metrics():
    assert fonts.LICENSE == "OFL-1.1"
    for f in fonts.FACES:
        m = f.metrics
        assert m.upm in (1000, 2000, 2048), f.family
        assert m.ascent > 0 and m.descent > 0 and m.x_height > 0 and m.cap_height > m.x_height
        assert m.latin_avg and m.latin_avg > 0, f.family
        assert f.weights[0] <= 400 <= f.weights[1], f.family
        if f.role == "arabic":
            assert m.arabic_avg and m.arabic_body, f.family
        else:
            assert all(0 <= p <= 1 for p in f.place), f.family


def test_every_latin_text_and_display_face_names_an_arabic_partner_in_the_catalog():
    for f in fonts.FACES:
        if f.role in ("text", "display"):
            assert fonts.BY_FAMILY[f.arabic].role == "arabic", f.family


def test_the_axes_choose_three_distinct_roles():
    c = fonts.choose(MID)
    assert (c.text.role, c.display.role, c.mono.role) == ("text", "display", "mono")
    assert c.display.family != c.text.family
    assert (c.text.family, c.display.family, c.mono.family) == (
        "Noto Sans", "Outfit", "IBM Plex Mono")


@pytest.mark.parametrize("axes, text, display", [
    (AxisValues(*[0.0] * 7), "Manrope", "Space Grotesk"),
    (AxisValues(*[1.0] * 7), "Source Sans 3", "Playfair Display"),
    (AxisValues(0.85, 0.5, 0.5, 0.5, 0.2, 0.6, 0.5), "Nunito Sans", "Bricolage Grotesque"),
    (AxisValues(0.35, 0.5, 0.6, 0.4, 0.95, 0.25, 0.4), "IBM Plex Sans", "Sora"),
])
def test_opposite_characters_get_different_faces(axes, text, display):
    c = fonts.choose(axes)
    assert (c.text.family, c.display.family) == (text, display)


def test_the_choice_moves_with_type_personality_alone():
    geometric = fonts.choose(AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0))
    humanist = fonts.choose(AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0))
    assert geometric.text.family != humanist.text.family
    assert geometric.display.family != humanist.display.family


@pytest.mark.parametrize("latin, arabic, want", [
    ("IBM Plex Sans", "IBM Plex Sans Arabic", 1.13),
    ("Source Sans 3", "Noto Naskh Arabic", 1.15),
    ("Manrope", "Readex Pro", 1.116),
    ("Nunito Sans", "Tajawal", 1.05),
])
def test_the_arabic_scale_comes_from_the_two_faces_metrics(latin, arabic, want):
    assert fonts.arabic_scale(fonts.BY_FAMILY[latin], fonts.BY_FAMILY[arabic]) == want


def test_fallback_overrides_match_the_measured_widths():
    got = fonts.fallback_overrides(fonts.BY_FAMILY["IBM Plex Sans"])
    assert got == {"size-adjust": "101.58%", "ascent-override": "100.90%",
                   "descent-override": "27.07%", "line-gap-override": "0.00%"}
    arabic = fonts.fallback_overrides(fonts.BY_FAMILY["Tajawal"])
    assert arabic["line-gap-override"] == "19.13%"


def test_the_cdn_family_names_a_range_or_the_weights_used():
    assert fonts.css2_family(fonts.BY_FAMILY["Manrope"], (400, 600)) == "Manrope:wght@200..800"
    assert fonts.css2_family(fonts.BY_FAMILY["IBM Plex Mono"], (500, 400, 400)) == \
        "IBM+Plex+Mono:wght@400;500"
