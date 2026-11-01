"""type.capitals: how far a brand leans to a display in capitals, emitted
from character (continuous in energy and formality), and read by the
all-caps-large rule so a calm system reports display capitals and a loud
one allows them."""
import pytest

from engine.foundations import build_system, character, to_css
from engine.linter.core import lint_text
from engine.synthesizer.axes import AxisValues

CALM = AxisValues(0.4, 0.2, 0.4, 0.3, 0.8, 0.2, 0.6)
LOUD = AxisValues(0.7, 0.9, 0.5, 0.7, 0.1, 0.9, 0.5)


def _capitals(axes):
    ts = build_system(axes, "#3366FF", arabic=False).tokens
    return ts.resolve("type.capitals", "")


def test_the_signal_is_the_character_value():
    for axes in (CALM, LOUD):
        assert _capitals(axes) == character.capitals(axes)
    assert _capitals(CALM) < character.CAPITALS_FROM <= _capitals(LOUD)


def test_the_signal_is_continuous_in_energy_and_formality():
    lean = [character.capitals(AxisValues(0.5, c, 0.5, 0.5, 0.2, c, 0.5))
            for c in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)]
    assert lean == sorted(lean) and lean[0] < lean[-1]
    steps = [b - a for a, b in zip(lean, lean[1:])]
    assert max(steps) < 0.4
    formal = [character.capitals(AxisValues(0.5, 1.0, 0.5, 0.5, f, 1.0, 0.5))
              for f in (0.0, 0.25, 0.5, 0.75, 1.0)]
    assert formal == sorted(formal, reverse=True)


def test_the_css_carries_it():
    css = to_css(build_system(LOUD, "#3366FF", arabic=False).tokens)
    assert "--type-capitals:" in css


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Page</title><style>
:root {{ --type-size-latin-9: 3.75rem; --type-size-latin-10: 7.5rem; --type-tracking-caps: 1.8px;
  --type-text-display-caps-letter-spacing: var(--type-tracking-caps); --type-capitals: {lean}; }}
.poster {{ text-transform: uppercase; font-size: 120px; letter-spacing: 1.8px; }}
</style></head><body><h1 class="poster">Night market</h1></body></html>"""


@pytest.mark.parametrize("lean,fires", [(0.05, True), (0.49, True), (0.5, False), (0.9, False)])
def test_all_caps_large_reads_the_signal(lean, fires):
    hits = {f.rule_id for f in lint_text("page.html", PAGE.format(lean=lean))}
    assert ("all-caps-large" in hits) is fires
