import re

import pytest

from engine.foundations.color import PAIRINGS, generate_color
from engine.foundations.color_math import contrast
from engine.foundations.gate import GateFailure, Pairing, gate
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

AXES = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)


def failing_set():
    ts = TokenSet()
    ts.add(Token("color.gray.300", "color", "#BBBBBB"))
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    ts.add(Token("color.text.default", "color", "{color.gray.300}", layer="semantic"))
    ts.add(Token("color.surface.page", "color", "{color.base.white}", layer="semantic"))
    return ts


def test_generated_system_passes():
    report = gate(generate_color(AXES, "#E61428").tokens, PAIRINGS)
    assert report.passed and report.checked == len(PAIRINGS) * 4


def test_failing_pairing_blocks_emission():
    with pytest.raises(GateFailure) as exc:
        gate(failing_set(), [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")])
    f = exc.value.report.findings[0]
    assert f.criterion == "1.4.3" and f.ratio < 4.5 and f.mode == "scheme:light,contrast:standard"


def test_report_mode_and_skips():
    report = gate(failing_set(), PAIRINGS, raise_on_fail=False)
    assert not report.passed and report.skipped > 0


def test_near_miss_ratio_never_prints_as_passing():
    # #777867 on #FFFFFF has a true ratio of ~4.499841992908034:1, just
    # under the 4.5:1 minimum. round(ratio, 2) would print "4.50:1", which
    # reads as meeting the minimum even though it fails it. message() must
    # floor instead of round so a failing ratio can never print as passing.
    fg_hex, bg_hex = "#777867", "#FFFFFF"
    true_ratio = contrast(fg_hex, bg_hex)
    assert 4.49 <= true_ratio < 4.5

    ts = TokenSet()
    ts.add(Token("color.gray.custom", "color", fg_hex))
    ts.add(Token("color.base.white", "color", bg_hex))
    ts.add(Token("color.text.default", "color", "{color.gray.custom}", layer="semantic"))
    ts.add(Token("color.surface.page", "color", "{color.base.white}", layer="semantic"))

    report = gate(ts, [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")],
                  raise_on_fail=False)
    assert not report.passed

    finding = report.findings[0]
    assert finding.ratio < 4.5

    message = finding.message()
    assert "4.49:1" in message
    assert "4.50:1" not in message

    printed = float(message.split(" is ")[1].split(":1")[0])
    assert printed < 4.5


@pytest.mark.parametrize("minimum, criterion, want", [
    (3.0, "1.4.11", "WCAG 1.4.11 needs 3:1"),
    (4.5, "1.4.3", "WCAG 1.4.3 needs 4.5:1"),
    (7.0, "1.4.6", "WCAG 1.4.6 needs 7:1"),
    (4.5, "high-contrast floor over 1.4.11",
     "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3:1)"),
    (4.0, "1.4.11", "the declared floor is 4:1 (WCAG 1.4.11 asks 3:1)"),
    (3.0, "custom", "the declared floor for custom is 3:1"),
])
def test_minimums_print_without_a_trailing_zero(minimum, criterion, want):
    from engine.foundations.gate import GateFinding, cite
    assert cite(minimum, criterion) == want
    # A measured ratio keeps its floored two decimals beside the minimum.
    message = GateFinding("color.line.input", "color.surface.raised", "scheme:dark", 2.639,
                          minimum, criterion).message()
    assert " is 2.63:1; " in message and want in message and ".0:1" not in message


def test_unvalidated_bad_value_names_the_token():
    # R27 I2: the gate used to raise the bare color_math error with no token path.
    # M4a Task 2 I2: it reports the pairing as unresolved in each context and
    # goes on, so check_system never raises on a color it cannot read.
    ts = TokenSet()
    ts.add(Token("color.gray.300", "color", "#GGGGGG"))
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    ts.add(Token("color.text.default", "color", "{color.gray.300}", layer="semantic"))
    ts.add(Token("color.surface.page", "color", "{color.base.white}", layer="semantic"))
    report = gate(ts, [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")],
                  raise_on_fail=False)
    first = report.failures[0]
    assert {f.check for f in report.failures} == {"unresolved-pairing"}
    assert first.mode == "scheme:light,contrast:standard"
    assert re.search(r"color\.text\.default \(scheme:light,contrast:standard\) resolves to "
                     r"'#GGGGGG'.*run validate", first.message)


LINK_ON_PAGE = Pairing("color.text.link", "color.surface.page", 4.5, "1.4.3")
TEXT_ON_PAGE = Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")


def test_skipped_pairings_are_listed():
    # R27 M7: a skipped pairing used to be a bare count.
    report = gate(failing_set(), PAIRINGS, raise_on_fail=False)
    assert report.skipped == len(report.skipped_pairings) > 0
    assert LINK_ON_PAGE in report.skipped_pairings
    assert TEXT_ON_PAGE not in report.skipped_pairings


def test_summary_names_skipped_pairings():
    ts = TokenSet()
    report = gate(ts, [TEXT_ON_PAGE, LINK_ON_PAGE], raise_on_fail=False)
    assert report.passed and report.checked == 0
    summary = report.summary()
    assert "0 checks" in summary and "2 pairings skipped" in summary
    assert "color.text.default on color.surface.page" in summary
    assert "color.text.link on color.surface.page" in summary
    assert "define those tokens or leave those pairings out" in summary


def test_gate_failure_names_skipped_pairings():
    with pytest.raises(GateFailure) as exc:
        gate(failing_set(), [TEXT_ON_PAGE, LINK_ON_PAGE])
    text = str(exc.value)
    assert "color.text.default on color.surface.page (scheme:light,contrast:standard)" in text
    assert ("Skipped 1 pairing because a token is not defined: color.text.link on "
            "color.surface.page") in text


def test_no_skip_line_when_nothing_skipped():
    with pytest.raises(GateFailure) as exc:
        gate(failing_set(), [TEXT_ON_PAGE])
    assert "Skipped" not in str(exc.value)
    assert "Skipped" not in gate(generate_color(AXES, "#3366FF").tokens, PAIRINGS).summary()


def test_check_naming_an_unknown_axis_is_refused():
    # A misspelled axis would otherwise be dropped, and the check would run
    # once in the base context while looking like it covered every mode.
    from engine.foundations.gate import Check
    ts = TokenSet()
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    typo = Check("space.min", "custom", lambda ts, mode: [], axes=("densty",))
    with pytest.raises(ValueError) as exc:
        gate(ts, [], checks=[typo])
    msg = str(exc.value)
    assert "space.min" in msg and "densty" in msg and "density" in msg


def test_gate_enforces_the_raised_minimum_in_high_contrast():
    ts = TokenSet()
    ts.add(Token("color.gray.600", "color", "#6B6B6B"))   # 5.33:1 on white
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    ts.add(Token("color.text.default", "color", "{color.gray.600}", layer="semantic"))
    ts.add(Token("color.surface.page", "color", "{color.base.white}", layer="semantic"))
    report = gate(ts, [TEXT_ON_PAGE], raise_on_fail=False)
    assert report.checked == 4
    assert [(f.mode, f.minimum, f.criterion) for f in report.findings] == [
        ("scheme:light,contrast:high", 7.0, "1.4.6"), ("scheme:dark,contrast:high", 7.0, "1.4.6")]
    assert "WCAG 1.4.6 needs 7:1" in report.findings[0].message()


# A token set with its own axes: the gate reads them, never the built-in ones.

def test_gate_measures_a_set_with_a_custom_axis():
    ts = TokenSet({"scheme": ("light", "dark"), "brand": ("main", "alt")})
    ts.add(Token("ink.fg", "color", "#BBBBBB", modes={"brand:alt": "#222222"}))
    ts.add(Token("ink.bg", "color", "#FFFFFF"))
    report = gate(ts, [Pairing("ink.fg", "ink.bg", 4.5, "1.4.3")], raise_on_fail=False)
    assert report.checked == 4
    assert [f.mode for f in report.findings] == ["scheme:light,brand:main",
                                                "scheme:dark,brand:main"]


def test_gate_measures_a_set_whose_axis_has_its_own_values():
    ts = TokenSet({"scheme": ("light", "dim"), "contrast": ("standard", "high")})
    ts.add(Token("color.text.default", "color", "#6B6B6B"))
    ts.add(Token("color.surface.page", "color", "#FFFFFF"))
    report = gate(ts, [TEXT_ON_PAGE], raise_on_fail=False)
    assert report.checked == 4
    assert [(f.mode, f.minimum, f.criterion) for f in report.findings] == [
        ("scheme:light,contrast:high", 7.0, "1.4.6"), ("scheme:dim,contrast:high", 7.0, "1.4.6")]


def test_a_check_that_raises_is_recorded_and_the_gate_goes_on():
    from engine.foundations.gate import Check, CheckFailure, GateFailure

    def broken(ts, mode):
        return [ts.resolve("space.missing")["value"]]

    ts = TokenSet()
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    checks = [Check("broken", "custom", broken),
              Check("passes", "custom", lambda ts, mode: []),
              Check("fails", "custom", lambda ts, mode: ["space.x is 3px; use 4px"])]
    report = gate(ts, [], checks=checks, raise_on_fail=False)
    assert report.rules_checked == 3
    assert [(f.check, f.criterion, f.mode) for f in report.failures] == [
        ("broken", "custom", ""), ("fails", "custom", "")]
    assert report.failures[0].message.startswith("check broken could not read the token set (")
    assert report.failures[0].message.endswith(
        "); a token it reads has an unexpected shape; run validate and fix the named token")
    assert report.failures[1] == CheckFailure("fails", "custom", "", "space.x is 3px; use 4px")
    with pytest.raises(GateFailure):
        gate(ts, [], checks=checks)


def test_a_raising_check_names_the_exception():
    from engine.foundations.gate import Check

    def broken(ts, mode):
        raise KeyError("offsetY")

    ts = TokenSet()
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    report = gate(ts, [], checks=[Check("broken", "custom", broken)], raise_on_fail=False)
    assert [f.message for f in report.failures] == [
        "check broken could not read the token set (KeyError: 'offsetY'); a token it reads has "
        "an unexpected shape; run validate and fix the named token"]


def test_the_summary_names_which_part_of_the_gate_failed():
    from engine.foundations.gate import CheckFailure, GateFinding, GateReport
    rule = CheckFailure("role-types", "system", "", "x is a dimension; fix it")
    assert GateReport(checked=3, rules_checked=2).summary().startswith("WCAG gate passed: ")
    assert GateReport(checked=3, rules_checked=2, failures=[rule]).summary().startswith(
        "WCAG gate failed on the rule checks: 3 checks, 0 failing")
    finding = GateFinding("color.text.default", "color.surface.page", "", 3.0, 4.5, "1.4.3")
    report = GateReport(findings=[finding], checked=3, rules_checked=2)
    assert report.summary().splitlines()[0].startswith("WCAG gate failed on contrast: ")
    report.failures.append(rule)
    assert report.summary().splitlines()[0].startswith(
        "WCAG gate failed on contrast and the rule checks: ")
