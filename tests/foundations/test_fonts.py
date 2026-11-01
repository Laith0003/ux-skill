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


def test_a_static_face_records_the_weights_it_ships():
    for f in fonts.FACES:
        if f.variable:
            assert f.stops == (), f.family
        else:
            assert f.stops == tuple(sorted(set(f.stops))) and f.stops, f.family
            assert (f.stops[0], f.stops[-1]) == f.weights, f.family
    assert fonts.BY_FAMILY["Tajawal"].stops == (200, 300, 400, 500, 700, 800, 900)
    assert fonts.BY_FAMILY["Amiri"].stops == (400, 700)
    assert fonts.BY_FAMILY["IBM Plex Mono"].stops == (100, 200, 300, 400, 500, 600, 700)
    assert fonts.BY_FAMILY["IBM Plex Sans Arabic"].stops == (100, 200, 300, 400, 500, 600, 700)


@pytest.mark.parametrize("face", fonts.FACES, ids=lambda f: f.slug)
def test_every_weight_snaps_to_one_the_face_ships(face):
    for w in range(100, 1001, 50):
        got = face.clamp(w)
        if face.variable:
            assert face.weights[0] <= got <= face.weights[1]
        else:
            assert got in face.stops
            assert all(abs(s - w) >= abs(got - w) for s in face.stops)
        family = fonts.css2_family(face, (400, w))
        if not face.variable:
            asked = [int(x) for x in family.split("@", 1)[1].split(";")]
            assert set(asked) <= set(face.stops), family


def test_a_weight_between_two_shipped_weights_takes_the_heavier():
    assert fonts.BY_FAMILY["Tajawal"].clamp(600) == 700
    assert fonts.BY_FAMILY["Amiri"].clamp(500) == 400
    assert fonts.BY_FAMILY["Amiri"].clamp(600) == 700
    assert fonts.css2_family(fonts.BY_FAMILY["Tajawal"], (400, 600)) == "Tajawal:wght@400;700"


def test_local_names_are_per_weight_and_no_two_weights_share_one():
    assert fonts.local_names(fonts.BY_FAMILY["Tajawal"], 700) == ("Tajawal Bold", "Tajawal-Bold")
    assert fonts.local_names(fonts.BY_FAMILY["IBM Plex Mono"], 400) == (
        "IBM Plex Mono Regular", "IBMPlexMono-Regular")
    seen = {}
    for f in fonts.FACES:
        for w in f.stops:
            for name in fonts.local_names(f, w):
                assert name not in seen, (name, seen.get(name), (f.family, w))
                seen[name] = (f.family, w)
    assert fonts.local_names(fonts.BY_FAMILY["Outfit"], 700) == ()
