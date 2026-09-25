"""make_system: build, gate and report. A failing system has no files, only
findings, so no caller can write one."""
import json

import pytest

import engine.foundations.color as color_module
from engine.foundations import ValidationError, build_system, dump_dtcg, to_css
from engine.foundations.emit import (
    FILES, NEUTRAL, NEUTRAL_SOURCE, SystemFinding, make_system,
)
from engine.foundations.validate import Problem
from engine.synthesizer.axes import AxisValues


def test_passing_build_returns_all_three_files():
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert out.passed and out.findings == ()
    assert tuple(out.files) == FILES
    built = build_system(NEUTRAL, "#3366FF")
    assert out.files["tokens.json"] == dump_dtcg(built.tokens)
    assert out.files["tokens.css"] == to_css(built.tokens)
    assert out.files["system-report.md"] == out.report
    json.loads(out.files["tokens.json"])


def test_report_says_what_was_built_from_what():
    axes = AxisValues(0.2, 0.4, 0.6, 0.8, 1.0, 0.0, 0.5)
    report = make_system("#3366FF", axes, "set by hand (--axes)").report
    assert report.startswith("# Design system report\n")
    assert "Brand color: #3366FF" in report
    assert "Axes: set by hand (--axes)." in report
    assert "| density | 0.6 | airy 0 to packed 1 |" in report
    assert "| motion | 0 | still 0 to lively 1 |" in report
    assert "WCAG gate passed: " in report
    assert "WCAG 1.4.3 (text 4.5:1)" in report and "1.4.11 (non-text 3:1)" in report
    assert "## Notes" in report and "- type: " in report
    assert 'data-theme="dark"' in report and 'dir="rtl"' in report
    assert "Latin and Arabic" in report


def test_latin_only_is_reported_and_emits_no_arabic():
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE, arabic=False)
    assert out.passed and "Latin only" in out.report
    assert "type-face-arabic" not in out.files["tokens.css"]


def test_same_inputs_give_the_same_bytes():
    a = make_system("#6B4423", NEUTRAL, NEUTRAL_SOURCE)
    b = make_system("#6B4423", NEUTRAL, NEUTRAL_SOURCE)
    assert a.files == b.files


def test_gate_failure_returns_findings_and_no_files(monkeypatch):
    # With the action solver off, white text stays on the exact yellow.
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    out = make_system("#FFD400", NEUTRAL, NEUTRAL_SOURCE)
    assert not out.passed and dict(out.files) == {}
    assert out.findings
    first = out.findings[0]
    assert first.subject == "color.text.on-action on color.action.primary"
    assert first.context == "scheme:light,contrast:standard"
    assert "WCAG 1.4.3 needs 4.5:1" in first.message
    assert "Move color.text.on-action" in first.message
    assert "WCAG gate failed: " in out.report
    assert "so nothing was written." in out.report
    assert ("- color.text.on-action on color.action.primary (light mode, standard contrast) "
            "is 1.43:1; WCAG 1.4.3 needs 4.5:1.\n") in out.report
    findings = out.report.split("## Findings\n", 1)[1]
    assert len(findings.strip().splitlines()) == len(out.findings)
    assert "scheme:" not in findings and "Move " not in findings


def test_validation_failure_returns_every_problem(monkeypatch):
    problems = [Problem("color.text.default", "semantic-literal",
                        "color.text.default holds a literal; point it at a primitive"),
                Problem("space.4", "bad-value", "space.4 is 'x'; use a dimension")]

    def broken(*args, **kwargs):
        raise ValidationError(problems)

    monkeypatch.setattr("engine.foundations.emit.build_system", broken)
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert not out.passed and dict(out.files) == {}
    assert [f.subject for f in out.findings] == ["color.text.default", "space.4"]
    assert "Validation failed: 2 problems in the token set" in out.report
    assert "- space.4 is 'x'; use a dimension" in out.report


def test_finding_line_adds_the_mode_only_when_missing():
    named = SystemFinding("a on b", "scheme:dark", "a on b (scheme:dark) is 2:1")
    bare = SystemFinding("reduced-travel", "motion:reduced", "motion.reveal.distance travels")
    anywhere = SystemFinding("color.x", "", "color.x is broken")
    assert named.line() == named.message
    assert bare.line() == "motion.reveal.distance travels (in motion:reduced)"
    assert anywhere.line() == "color.x is broken"


def test_to_dict_is_json_ready():
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    data = out.to_dict()
    assert data["passed"] is True and data["brand"] == "#3366FF"
    assert data["gate"] == out.gate and out.gate.startswith("WCAG gate passed: ")
    assert data["axes"]["warmth"] == 0.5 and data["axes_source"] == NEUTRAL_SOURCE
    assert data["findings"] == [] and data["arabic"] is True
    json.dumps(data)


@pytest.mark.parametrize("brand", ["#3366FF", "#6B4423", "#FFD400"])
def test_golden_brands_pass(brand):
    assert make_system(brand, NEUTRAL, NEUTRAL_SOURCE).passed


# The report reads for a founder who never learned design-system words and
# for a design-system designer.
from engine.foundations.emit import render_report  # noqa: E402

SENTENCE = ("A complete design system for #3366FF: color, spacing, radius, borders, elevation, "
            "motion, layout and type, in light and dark, standard and high contrast, comfortable "
            "and compact spacing, left to right and right to left, and full and reduced motion. "
            "Every color pairing passed the WCAG contrast gate, so the files below are ready "
            "to use.")


def test_report_opens_with_one_plain_sentence():
    report = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE).report
    assert report.split("\n")[2] == SENTENCE


def test_every_axis_has_a_human_name_and_a_scale():
    report = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE).report
    assert "Each runs from 0 to 1" in report
    for row in ("| warmth | 0.5 | cool 0 to warm 1 |", "| contrast | 0.5 | muted 0 to bold 1 |",
                "| geometry | 0.5 | sharp 0 to rounded 1 |",
                "| formality | 0.5 | playful 0 to formal 1 |",
                "| type personality | 0.5 | geometric 0 to humanist 1 |"):
        assert row in report
    assert "type_personality" not in report


def test_modes_are_named_in_words():
    report = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE).report
    assert "dark mode, standard contrast" in report
    # The one machine key left is the legend that maps words to tokens.json.
    assert report.count("scheme:") == 1
    assert "tokens.json keys the same modes, so dark mode, high contrast is " \
           "scheme:dark,contrast:high there" in report
    assert 'data-theme="dark" for dark mode' in report


def test_notes_start_by_saying_what_they_are():
    report = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE).report
    notes = report.split("## Notes\n\n", 1)[1]
    assert notes.startswith("These are adjustments the engine made on its own, so nothing "
                            "needs doing: first the colors it moved off their default step so "
                            "every pairing meets its contrast minimum, and why")
    assert "### Colors moved to meet contrast" in notes and "### Other choices" in notes


NOTES = (
    "color.brand: #FFD400 is too light to anchor a ramp at 500; 500 retuned to #E0BA00, same "
    "hue, chroma reduced to fit sRGB.",
    "color.text.muted (scheme:dark,contrast:standard): color.neutral.400 -> color.neutral.300, "
    "color.text.muted on color.surface.raised was 3.76:1, now 5.21:1, WCAG 1.4.3 needs 4.5:1",
    "color.action.primary group (scheme:light,contrast:standard): color.action.primary "
    "color.brand.500 -> color.brand.700, color.text.on-action color.base.white -> "
    "color.base.black, text/fill 4.97:1, fill/page 4.63:1, ring/surface 6.21:1",
    "color.action.danger group (scheme:dark,contrast:high): no combination within the ramps "
    "clears every requirement; kept the closest, text/fill 3.10:1, fill/page 3.00:1",
    "motion: calm curves, 4px travel step",
)


def test_notes_are_rewritten_in_plain_words():
    report = render_report("#FFD400", NEUTRAL, NEUTRAL_SOURCE, True, "WCAG gate passed: x.",
                           NOTES, ())
    moved = report.split("### Colors moved to meet contrast\n\n", 1)[1].split("\n\n")[0]
    assert moved.splitlines() == [
        "- In dark mode, standard contrast, color.text.muted moved from color.neutral.400 to "
        "color.neutral.300: on color.surface.raised it measured 3.76:1, now 5.21:1, and WCAG "
        "1.4.3 needs 4.5:1.",
        "- In light mode, standard contrast, for the color.action.primary button the engine "
        "changed color.action.primary from color.brand.500 to color.brand.700 and color.text.on-action "
        "from color.base.white to color.base.black. It now measures 4.97:1 for text on the "
        "fill, 4.63:1 for the fill on the page and 6.21:1 for the focus ring on the surface.",
        # A shape the report does not know keeps the engine's words, modes in words.
        "- color.action.danger group (dark mode, high contrast): no combination within the "
        "ramps clears every requirement; kept the closest, text/fill 3.10:1, fill/page 3.00:1",
    ]
    other = report.split("### Other choices\n\n", 1)[1].split("\n\n")[0]
    assert other.splitlines() == [
        "- The brand color #FFD400 is too light to sit at step 500, the middle of its color "
        "scale, so step 500 is #E0BA00 (same hue, chroma reduced to fit sRGB).",
        "- motion: calm curves, 4px travel step",
    ]


def test_a_gate_failure_says_what_to_change_in_the_inputs(monkeypatch):
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    out = make_system("#FFD400", NEUTRAL, NEUTRAL_SOURCE)
    lines = out.report.split("\n")
    assert lines[2] == (f"No design system was built for #FFD400: the WCAG gate found "
                        f"{len(out.findings)} problems with these inputs, so nothing was "
                        "written.")
    change = out.report.split("## What to change\n\n", 1)[1].split("\n\n")[0]
    assert "darker or more saturated brand color" in change
    assert "different axes, or a different brief" in change
    assert "seed" not in out.report.split("## Findings", 1)[1]


def test_a_validation_failure_says_it_is_not_the_inputs(monkeypatch):
    def broken(*args, **kwargs):
        raise ValidationError([Problem("space.4", "bad-value", "space.4 is 'x'; use a dimension")])
    monkeypatch.setattr("engine.foundations.emit.build_system", broken)
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert out.report.split("\n")[2] == (
        "No design system was built for #3366FF: the generated tokens broke 1 structural rule, "
        "so the WCAG gate did not run and nothing was written.")
    assert "report it" in out.report.split("## What to change\n\n", 1)[1]


def test_a_validation_error_without_problems_still_fails(monkeypatch):
    def broken(*args, **kwargs):
        raise ValidationError([])
    monkeypatch.setattr("engine.foundations.emit.build_system", broken)
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert not out.passed and dict(out.files) == {}


def test_report_bytes_do_not_depend_on_the_hash_seed():
    import hashlib
    import os
    import subprocess
    import sys
    from pathlib import Path
    code = ("import hashlib, engine.foundations.emit as e;"
            "a, s = e.choose_axes({'industry': 'saas', 'tone': 'warm, calm, luxurious'}, None);"
            "o = e.make_system('#3366FF', a, s);"
            "print(hashlib.sha256(''.join(o.files.values()).encode()).hexdigest())")
    root = Path(__file__).resolve().parents[2]
    digests = set()
    for seed in ("0", "1", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        run = subprocess.run([sys.executable, "-c", code], cwd=root, env=env,
                             capture_output=True, text=True, check=True)
        digests.add(run.stdout.strip())
    assert len(digests) == 1


def test_word_tables_cover_every_engine_name():
    from engine.foundations import emit
    from engine.foundations.build import FOUNDATIONS
    from engine.foundations.modes import AXES
    from engine.synthesizer.axes import AXIS_NAMES
    assert set(emit._FOUNDATION_WORDS) == {f.name for f in FOUNDATIONS}
    assert list(emit._MODE_WORDS) == list(AXES)
    for axis, values in AXES.items():
        assert set(emit._MODE_WORDS[axis][1]) == set(values)
    assert list(emit._AXIS_WORDS) == list(AXIS_NAMES)


@pytest.mark.parametrize("brand,axes", [
    ("#3366FF", NEUTRAL), ("#FFD400", AxisValues(0, 1, 1, 1, 0, 1, 0)),
    ("#6B4423", AxisValues(1, 0, 0, 0, 1, 0, 1)),
    ("#F0F0F0", AxisValues(.9, .9, .1, .9, .2, .9, .9)),
    ("#0B0B0B", AxisValues(.3, .7, .5, .2, .8, .4, .3)),
])
def test_every_engine_note_reads_in_words(brand, axes):
    report = make_system(brand, axes, "x").report
    body = report.split("## Notes", 1)[1].split("## Files", 1)[0]
    body = body.split("\n\n", 2)[2]  # past the lead, which names one key on purpose
    assert "scheme:" not in body and "contrast:" not in body
    moved = body.split("### Other choices")[0]
    assert "->" not in moved and "text/fill" not in moved
    assert "anchor a ramp" not in body


# What a caller tells the user when nothing was built: the report's own
# guidance on what to change, and every finding, in words.
def test_failure_text_and_message_point_at_the_inputs(monkeypatch):
    from engine.foundations.emit import failure_message, failure_text
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    out = make_system("#FFD400", NEUTRAL, NEUTRAL_SOURCE)
    text = failure_text(out)
    opening = out.report.split("\n")[2]
    change = out.report.split("## What to change\n\n", 1)[1].split("\n\n")[0]
    listed = out.report.split("## Findings\n\n", 1)[1]
    assert text == f"{opening}\n\nWhat to change\n{change}\n\nFindings\n{listed}"
    message = failure_message(out)
    assert message.startswith("Nothing was written: the WCAG gate found ")
    assert "darker or more saturated" in message and "the axes or the brief" in message
    assert "fix each finding" not in (text + message).lower()


def test_failure_message_for_a_validation_failure_says_to_report_it(monkeypatch):
    from engine.foundations.emit import failure_message, failure_text

    def broken(*args, **kwargs):
        raise ValidationError([Problem("space.4", "bad-value", "space.4 is 'x'; use a dimension")])
    monkeypatch.setattr("engine.foundations.emit.build_system", broken)
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert "report it" in failure_message(out)
    assert "- space.4 is 'x'; use a dimension" in failure_text(out)


def test_failure_text_of_a_passing_system_is_empty():
    from engine.foundations.emit import failure_message, failure_text
    out = make_system("#3366FF", NEUTRAL, NEUTRAL_SOURCE)
    assert failure_text(out) == "" and failure_message(out) == ""


# The rule pack: off by default, written after the three files when asked,
# and a pack that does not fit the build writes nothing.
def test_the_rule_pack_is_off_by_default_and_follows_the_three_files():
    from engine.foundations.emit import FILES, RULE_PACK_DIR
    plain = make_system("#3366FF", NEUTRAL, "x")
    assert tuple(plain.files) == FILES and "rule-pack" not in plain.report
    packed = make_system("#3366FF", NEUTRAL, "x", rule_pack=True)
    names = list(packed.files)
    assert tuple(names[:3]) == FILES and names[3] == f"{RULE_PACK_DIR}/README.md"
    assert all(n.startswith(f"{RULE_PACK_DIR}/") for n in names[3:])
    assert {k: packed.files[k] for k in FILES[:2]} == {k: plain.files[k] for k in FILES[:2]}
    assert "- rule-pack/: the rules for AI agents and people" in packed.report
    assert packed.files["system-report.md"] == packed.report


def test_a_rule_pack_that_does_not_fit_writes_nothing(monkeypatch):
    import engine.rulepack.generate as generate
    from engine.foundations.emit import failure_message

    def broken(ts):
        raise generate.RulePackError(["card: container.fill needs an edge"])
    monkeypatch.setattr(generate, "build_rule_pack", broken)
    out = make_system("#3366FF", NEUTRAL, "x", rule_pack=True)
    assert out.passed is False and out.files == {}
    assert [(f.subject, f.message) for f in out.findings] == [
        ("rule-pack", "card: container.fill needs an edge")]
    assert "The rule pack could not be built: 1 problem" in out.gate
    assert "the tokens passed the WCAG gate, but the rule pack found 1 problem" in out.report
    assert "Build again without the rule pack" in out.report
    assert failure_message(out).startswith("Nothing was written: the tokens passed the WCAG "
                                           "gate, but the rule pack found 1 problem")


def test_the_report_states_the_brand_color_in_every_context():
    report = make_system("#E85D04", NEUTRAL, NEUTRAL_SOURCE).report
    section = report.split("## Brand color\n\n", 1)[1].split("\n## ", 1)[0]
    lines = [line for line in section.splitlines() if line.startswith("- ")]
    assert len(lines) == 5 and lines[4].startswith("- The logo (color.logo) is the brand color")
    assert lines[0].startswith("- Light mode: the button is the brand color #E85D04 exactly")
    assert report.index("## Brand color") < report.index("## Notes")
