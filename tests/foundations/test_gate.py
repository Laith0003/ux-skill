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
    assert report.passed and report.checked == len(PAIRINGS) * 2


def test_failing_pairing_blocks_emission():
    with pytest.raises(GateFailure) as exc:
        gate(failing_set(), [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")])
    f = exc.value.report.findings[0]
    assert f.criterion == "1.4.3" and f.ratio < 4.5 and f.mode == "light"


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
    with pytest.raises(ValueError, match=r"color\.text\.default \(light\) resolves to '#GGGGGG'.*run validate"):
        gate(ts, [Pairing("color.text.default", "color.surface.page", 4.5, "1.4.3")])
