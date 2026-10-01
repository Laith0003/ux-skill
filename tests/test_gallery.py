"""The gallery in data/gallery: one foundations system per brand spec in
data/brands, built by scripts/build_gallery.py. Every spec has an entry,
the committed entries are exactly what the script writes, every entry
passes the gate in every mode, the axes stay in range and move a little
when a fact moves a little, and nothing but the spec's design facts places
them."""
import copy
import importlib.util
import json
import re
from pathlib import Path

import pytest

from engine.foundations.emit import make_system
from engine.synthesizer.axes import AXIS_NAMES, AxisValues

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("build_gallery",
                                               ROOT / "scripts" / "build_gallery.py")
bg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bg)

SPECS = bg.load_specs()
ENTRIES = sorted((ROOT / "data" / "gallery").glob("*.json"))
IDS = [sid for sid, _ in SPECS]


def _invented(**design):
    """An invented spec: a made-up studio with the design facts given."""
    base = {"color_primary": "#2F6B4F", "color_canvas": "#FBFAF7", "color_ink": "#1B1C1A",
            "radius": [6, 10], "spacing": "4-based",
            "type": {"display": "Invented Grotesk", "body": "Invented Text"},
            "motion_signature": "A 240ms fade on hover."}
    base.update(design)
    return {"id": "invented-studio", "name": "Invented Studio", "design_language": base}


# ---------------------------------------------------------------- coverage


def test_there_are_160_specs():
    assert len(SPECS) == 160


def test_every_spec_has_an_entry_and_every_entry_a_spec():
    assert sorted(f.stem for f in ENTRIES) == sorted(IDS)


def test_the_committed_entries_are_what_the_script_writes():
    built = bg.build_all()
    on_disk = {f.name: f.read_bytes() for f in ENTRIES}
    assert sorted(built) == sorted(on_disk)
    drift = [name for name, text in built.items() if text.encode("ascii") != on_disk[name]]
    assert drift == [], f"rerun python scripts/build_gallery.py; these differ: {drift[:10]}"


def test_the_output_is_deterministic_ascii_with_sorted_keys_and_a_final_newline():
    sid, spec = SPECS[0]
    one, two = bg.dump(bg.entry(spec)), bg.dump(bg.entry(copy.deepcopy(spec)))
    assert one == two and one.endswith("}\n") and one.isascii()
    data = json.loads(one)
    assert list(data) == sorted(data)
    assert set(data) >= {"id", "name", "brand", "axes", "arabic", "axes_source", "digest"}


def test_the_check_mode_names_a_drifted_entry(tmp_path):
    sid, spec = SPECS[0]
    (tmp_path / f"{sid}.json").write_text("{}\n", encoding="ascii")
    problems = bg.check(tmp_path, {f"{sid}.json": bg.dump(bg.entry(spec))})
    assert len(problems) == 1 and f"{sid}.json" in problems[0]
    assert "build_gallery.py" in problems[0]


# ---------------------------------------------------------------- gate


@pytest.mark.parametrize("path", ENTRIES, ids=lambda p: p.stem)
def test_every_entry_passes_the_gate_in_every_mode(path):
    entry = json.loads(path.read_text(encoding="utf-8"))
    out = make_system(entry["brand"], AxisValues(**entry["axes"]), entry["axes_source"],
                      arabic=entry["arabic"])
    assert out.passed, [f.line() for f in out.findings]
    assert out.findings == ()


@pytest.mark.parametrize("path", ENTRIES, ids=lambda p: p.stem)
def test_every_entry_has_axes_in_range_and_a_plain_source(path):
    entry = json.loads(path.read_text(encoding="utf-8"))
    assert set(entry["axes"]) == set(AXIS_NAMES)
    assert all(0.0 <= v <= 1.0 for v in entry["axes"].values())
    assert re.fullmatch(r"#[0-9A-F]{6}", entry["brand"])
    source = entry["axes_source"]
    assert source.endswith(".") and source.count(". ") == 0


# ---------------------------------------------------------------- continuity


def _nudged(spec, step):
    """The spec with every numeric design fact moved a little: radii and
    the spacing base by a fraction of a pixel, each color by one step of
    one channel, stated durations by a few milliseconds."""
    out = copy.deepcopy(spec)
    dl = out["design_language"]
    if isinstance(dl.get("radius"), list):
        dl["radius"] = [r + step for r in dl["radius"]]
    if isinstance(dl.get("spacing"), str):
        dl["spacing"] = re.sub(r"\d+(?:\.\d+)?", lambda m: str(float(m.group()) + step / 4),
                               dl["spacing"], count=1)
    for key, value in list(dl.items()):
        if key.startswith("color_") and isinstance(value, str) and \
                re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            r = int(value[1:3], 16)
            dl[key] = "#%02x%s" % (r + 1 if r < 255 else r - 1, value[3:])
    if isinstance(dl.get("motion_signature"), str):
        dl["motion_signature"] = re.sub(
            r"(\d+)ms", lambda m: f"{int(m.group(1)) + 4}ms", dl["motion_signature"])
    return out


@pytest.mark.parametrize("sid,spec", SPECS, ids=IDS)
def test_a_small_change_in_a_fact_is_a_small_change_in_the_axes(sid, spec):
    before = bg.spec_axes(spec)[0].to_dict()
    after = bg.spec_axes(_nudged(spec, 0.25))[0].to_dict()
    moved = {a: round(abs(after[a] - before[a]), 4) for a in AXIS_NAMES}
    assert all(m <= 0.03 for m in moved.values()), moved


def test_each_axis_follows_its_own_fact():
    def axes(**design):
        return bg.spec_axes(_invented(**design))[0]
    assert axes(radius=[0]).geometry < axes(radius=[8]).geometry < axes(radius=[24]).geometry
    assert axes(spacing="8-based").density < axes(spacing="4-based").density \
        < axes(spacing="2-based").density
    assert axes(motion_signature="A 120ms fade.").motion \
        < axes(motion_signature="A 600ms glide.").motion \
        < axes(motion_signature="Cross-fades over 1.5s.").motion
    assert axes(color_primary="#1F5FD6").warmth < axes(color_primary="#D6641F").warmth
    assert axes(color_ink="#6E6E6E").contrast < axes(color_ink="#111111").contrast
    assert axes(color_primary="#555555").formality > axes(color_primary="#E0218A").formality


def test_a_fact_the_spec_does_not_state_sits_at_the_middle():
    spec = _invented()
    for key in ("radius", "spacing", "motion_signature"):
        del spec["design_language"][key]
    a, source = bg.spec_axes(spec)
    assert a.geometry == a.density == a.motion == 0.5
    assert "0.5" in source


def test_a_face_in_the_engine_catalog_brings_its_measured_place():
    from engine.foundations.fonts import FACES
    face = next(f for f in FACES if f.role == "display" and f.place[3] > 0.8)
    plain = bg.spec_axes(_invented())[0]
    known = bg.spec_axes(_invented(type={"display": face.family, "body": "Invented Text"}))[0]
    assert known.type_personality > plain.type_personality == 0.5


# ---------------------------------------------------------------- inputs


def test_nothing_but_the_design_facts_places_the_axes_or_the_brand():
    spec = _invented()
    other = copy.deepcopy(spec)
    other.update({"id": "another-invented-id", "name": "Another", "category": "Anything",
                  "industry": "anything", "philosophy": "Loud, playful and warm.",
                  "trademark_signals": ["round"], "ai_slop_avoided": ["sharp"]})
    (axes, source), (axes2, source2) = bg.spec_axes(spec), bg.spec_axes(other)
    assert axes == axes2 and source == source2.replace(other["id"], spec["id"])
    assert bg.brand_hex(spec) == bg.brand_hex(other)


def test_no_code_path_reads_a_category_industry_or_brand_name():
    text = (ROOT / "scripts" / "build_gallery.py").read_text(encoding="utf-8")
    assert not re.search(r"category|industry|keyword", text, re.I)
    names = {spec.get("name", "") for _, spec in SPECS} | set(IDS)
    named = [n for n in names if len(n) >= 4 and re.search(r"(?<![\w-])" + re.escape(n)
                                                           + r"(?![\w-])", text)]
    assert named == []


def test_the_primary_is_the_brand_when_it_can_carry_an_action():
    hex_, why = bg.brand_hex(_invented(color_primary="#2F6B4F", color_accent="#E0A100"))
    assert hex_ == "#2F6B4F" and "3:1" in why


def test_an_accent_carries_the_action_when_the_primary_cannot():
    spec = _invented(color_primary="#F2E96B", color_accent="#7A3BD1", color_canvas="#FFFFFF")
    hex_, why = bg.brand_hex(spec)
    assert hex_ == "#7A3BD1" and "accent" in why


def test_the_primary_stays_when_no_accent_does_better():
    spec = _invented(color_primary="#F2E96B", color_accent="#F6F1C0", color_canvas="#FFFFFF")
    assert bg.brand_hex(spec)[0] == "#F2E96B"


def test_an_alpha_ink_is_read_over_the_canvas():
    # Black at alpha 230 of 255 over white is #191919: the ink reads as that,
    # not as black.
    spec = _invented(color_ink="#000000e6", color_canvas="#FFFFFF")
    contrast = bg.spec_axes(spec)[0].contrast
    assert bg._color("#000000e6") == "#191919"
    assert contrast == bg.spec_axes(_invented(color_ink="#191919", color_canvas="#FFFFFF"))[0].contrast
    assert contrast != bg.spec_axes(_invented(color_ink="#000000", color_canvas="#FFFFFF"))[0].contrast


def test_a_spec_without_a_readable_primary_is_named_with_the_fix():
    spec = _invented(color_primary="blue")
    with pytest.raises(bg.GalleryError) as exc:
        bg.brand_hex(spec)
    message = str(exc.value)
    assert "invented-studio" in message and "color_primary" in message and "#RRGGBB" in message


def test_a_count_in_prose_is_not_read_as_a_duration():
    text = "911s carving through mountain passes, then a 0.3s ease and a 200ms fade"
    assert bg._durations({"motion_signature": text}) == [300.0, 200.0]
    assert bg._durations({"motion_signature": "a 12 seconds loop"}) == []
