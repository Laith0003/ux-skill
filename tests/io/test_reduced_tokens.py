"""Reduced motion written as separate tokens: a system with no motion mode
that declares a reduced value beside a token (duration-slow and
duration-slow-reduced, or motion.reduced.*) has reduced motion. The adapter
reads each pair as the base token's reduced-motion value, and the enhance
report says reduced motion is present instead of asking for a mode. A
global prefers-reduced-motion block in the code counts as present too."""
import json

from engine.foundations.build import check_system
from engine.io.adapter import AxisMap, Mapping, RoleMap, reduced_pairs, view
from engine.io.css_in import import_css
from engine.io.dtcg_in import import_dtcg
from engine.io.enhance import enhance
from engine.io.report import Source
from engine.io.scan import scan

# An invented system: each duration has a reduced twin beside it.
PAIRS = """:root {
  --duration-slow: 300ms;
  --duration-slow-reduced: 80ms;
  --duration-fast: 150ms;
  --duration-fast-reduced: 400ms;
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
}
"""


def _imported(text=PAIRS):
    return import_css(text, Source("motion.css", "css", "0" * 64, len(text)))


def test_a_reduced_twin_is_found_by_its_name_in_any_position():
    assert reduced_pairs(_imported().tokens) == {"duration-slow": "duration-slow-reduced",
                                                 "duration-fast": "duration-fast-reduced"}
    doc = {"motion": {"pace": {"calm": {"$type": "duration",
                                        "$value": {"value": 300, "unit": "ms"}}},
                      "reduced": {"pace": {"calm": {"$type": "duration",
                                                    "$value": {"value": 0, "unit": "ms"}}}}}}
    text = json.dumps(doc)
    ts = import_dtcg(text, Source("tokens.json", "dtcg", "0" * 64, len(text))).tokens
    assert reduced_pairs(ts) == {"motion.pace.calm": "motion.reduced.pace.calm"}
    # A reduced token with no twin, or a twin of another type, pairs with
    # nothing.
    lone = _imported(":root { --gap: 8px; --gap-reduced: 100ms; --blur-reduced: 2px; }\n")
    assert reduced_pairs(lone.tokens) == {}


def test_the_view_reads_each_twin_as_the_reduced_motion_value():
    mapping = Mapping(roles={"motion.reveal.duration": RoleMap("duration-slow", "owner"),
                             "motion.reveal.curve": RoleMap("ease-out", "owner")})
    checked, notes = view(_imported().tokens, mapping, "mapping.json")
    assert dict(checked.axes) == {"motion": ("standard", "reduced")}
    reveal = checked.get("motion.reveal.duration")
    assert (reveal.value, reveal.modes) == ({"value": 300, "unit": "ms"},
                                            {"motion:reduced": {"value": 80, "unit": "ms"}})
    assert checked.get("motion.reveal.curve").modes == {}
    assert notes == [
        "motion:reduced is read from the separate tokens the system declares for it: "
        "duration-slow-reduced for duration-slow; map the motion axis in mapping.json to read "
        "it from a mode instead"]
    assert check_system(checked, structure=False).passed


def test_the_gate_measures_a_reduced_twin_that_breaks_the_cap():
    mapping = Mapping(roles={"motion.press.duration": RoleMap("duration-fast", "owner")})
    result = enhance(_imported(), mapping)
    assert [f for f in result.findings if "under reduced motion" in f] == [
        "motion.press.duration (your duration-fast) lasts 400ms under reduced motion; cap it at "
        "100ms in your duration-fast-reduced (in motion:reduced)"]


def test_a_mapped_motion_axis_or_the_owners_null_wins_over_the_twins():
    ts = _imported(PAIRS + '[data-motion="reduced"] { --duration-slow: 0ms; }\n').tokens
    mapping = Mapping(roles={"motion.reveal.duration": RoleMap("duration-slow", "owner")},
                      axes={"motion": AxisMap("motion", {"standard": "standard",
                                                         "reduced": "reduced"}, "owner")})
    checked, notes = view(ts, mapping)
    assert checked.get("motion.reveal.duration").modes == {
        "motion:reduced": {"value": 0, "unit": "ms"}}
    assert notes == []
    out = Mapping(roles={"motion.reveal.duration": RoleMap("duration-slow", "owner")},
                  axes={"motion": AxisMap(None, {}, "owner")})
    checked, _ = view(_imported().tokens, out)
    assert dict(checked.axes) == {}


def test_enhance_reports_reduced_motion_present_through_the_twins():
    mapping = Mapping(roles={"motion.reveal.duration": RoleMap("duration-slow", "owner")})
    confirm = enhance(_imported(), mapping).confirm
    assert not [c for c in confirm if "no reduced-motion mode" in c]
    assert ("The system has reduced motion as separate tokens (duration-slow-reduced for "
            "duration-slow), read as the reduced-motion values of their base tokens, so the "
            "motion checks ran under reduced motion; confirm each pair.") in confirm
    # Twins no mapped role reads are still reduced motion the system has.
    confirm = enhance(_imported(), Mapping()).confirm
    assert ("The system has reduced motion as separate tokens (duration-slow-reduced for "
            "duration-slow and duration-fast-reduced for duration-fast), but no mapped role "
            "reads them; map the motion roles to their base tokens in mapping.json to check "
            "them under reduced motion.") in confirm


def test_a_global_reduced_motion_block_in_the_code_counts_as_present(tmp_path):
    (tmp_path / "base.css").write_text(
        ".card { transition: opacity 200ms; }\n"
        "@media (prefers-reduced-motion: reduce) {\n"
        "  *, ::before, ::after { animation-duration: 0.01ms !important; }\n"
        "}\n", encoding="utf-8")
    text = ":root { --ink: #111111; }\n"
    imported = _imported(text)
    scanned = scan([tmp_path], imported.tokens)
    assert scanned.reduced_motion == [("base.css", 3, "*, ::before, ::after")]
    confirm = enhance(imported, Mapping(), scanned).confirm
    assert not [c for c in confirm if "no reduced-motion mode" in c]
    assert ("The code turns motion down for everything in a prefers-reduced-motion block at "
            "base.css:3, so reduced motion is present, though not as a mode of the system: the "
            "motion checks under reduced motion ran on no token. To check them, give motion.css "
            "a reduced-motion mode or reduced tokens, and map them in mapping.json.") in confirm


def test_twins_are_motion_values_only():
    ts = _imported(":root { --opacity-overlay: 0.6; --opacity-overlay-reduced: 1; "
                   "--shadow-lift: 4px; --shadow-lift-reduced: 0px; "
                   "--distance-reveal: 16px; --distance-reveal-reduced: 0px; }\n").tokens
    assert reduced_pairs(ts) == {"distance-reveal": "distance-reveal-reduced"}


def test_a_boolean_reduced_motion_query_counts_as_present(tmp_path):
    (tmp_path / "base.css").write_text(
        "@media (prefers-reduced-motion) {\n  * { transition: none; }\n}\n"
        "@media (prefers-reduced-motion: no-preference) {\n  .a { transition: all 1s; }\n}\n",
        encoding="utf-8")
    scanned = scan([tmp_path], _imported(":root { --ink: #111111; }\n").tokens)
    assert scanned.reduced_motion == [("base.css", 2, "*")]
