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


def test_unvalidated_bad_value_names_the_token():
    # R27 I2: the gate used to raise the bare color_math error with no token path.
    ts = TokenSet()
    ts.add(Token("color.gray.300", "color", "#GGGGGG"))
    ts.add(Token("color.base.white", "color", "#FFFFFF"))
    ts.add(Token("color.text.default", "color", "{color.gray.300}", layer="semantic"))
    ts.add(Token("color.surface.page", "color", "{color.base.white}", layer="semantic"))
    with pytest.raises(ValueError, match=r"color\.text\.default \(scheme:light,contrast:standard\) resolves to '#GGGGGG'.*run validate"):
        gate(ts, [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")])


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
    assert "Skipped 1 pairing because a token is not defined: color.text.link on color.surface.page" in text


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
