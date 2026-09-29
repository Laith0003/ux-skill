"""The floors measured award pages often break still hold at the loudest
corner after the character retune: 16px body, 4.5:1 for small text, a
reduced-motion path, 24px targets (44px at comfortable density), and a
display that never pushes a phone sideways."""
from engine.foundations import build_system
from engine.foundations.motion import REDUCED_MAX_MS, ROLES
from engine.synthesizer.axes import AxisValues

LOUDEST = AxisValues(warmth=1.0, contrast=1.0, density=1.0, geometry=1.0, formality=0.0,
                     motion=1.0, type_personality=1.0)
BRANDS = ("#3366FF", "#FFD400", "#E85D04", "#111111")


def px(v):
    return v["value"] * (16 if v["unit"] == "rem" else 1)


def test_the_loudest_brief_passes_the_gate_with_body_at_16px_and_text_at_4_5():
    for brand in BRANDS:
        for arabic in (True, False):
            built = build_system(LOUDEST, brand, arabic=arabic)
            assert built.report.passed
            ts = built.tokens
            assert px(ts.resolve("type.text.body")["fontSize"]) >= 16
            assert all(f.ratio >= 4.5 for f in built.report.findings
                       if f.fg.startswith("color.text"))


def test_the_loudest_brief_keeps_a_reduced_motion_path():
    ts = build_system(LOUDEST, "#3366FF").tokens
    for role in ROLES:
        reduced = ts.resolve(f"{role}.duration", "motion:reduced")["value"]
        if role != "motion.progress":
            assert reduced <= REDUCED_MAX_MS
        if ts.has(f"{role}.distance"):
            assert ts.resolve(f"{role}.distance", "motion:reduced")["value"] == 0
    assert ts.resolve("motion.scroll", "motion:reduced") == 0
    assert ts.resolve("motion.press.scale", "motion:reduced") == 1


def test_the_loudest_brief_keeps_its_targets():
    ts = build_system(LOUDEST, "#3366FF").tokens
    assert px(ts.resolve("layout.target.min")) >= 44
    assert px(ts.resolve("layout.target.min", "density:compact")) >= 24


def test_the_loudest_display_fits_a_320px_phone():
    ts = build_system(LOUDEST, "#3366FF").tokens
    from engine.foundations import fonts
    from engine.foundations.typography import word_em
    face = fonts.BY_FAMILY[ts.resolve("type.face.display")[0]]
    letters = ts.resolve("type.fit-word.latin")
    size = ts.resolve("type.fluid.display.phone", "contrast:standard,direction:ltr") * 3.2
    margin = px(ts.resolve("layout.margin-inline.phone"))
    assert word_em(face, "latin", letters) * size <= 320 - 2 * margin + 0.5
