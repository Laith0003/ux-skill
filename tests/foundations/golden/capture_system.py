"""Writes the full-system golden: for three seeds and three axis mixes,
plus one Latin-only build, the CSS and the DTCG text build_system emits.
Run from the repo root when a change to the output is intended, then
review the diff:

    PYTHONPATH=. python tests/foundations/golden/capture_system.py
"""
from pathlib import Path

from engine.foundations import build_system, dump_dtcg, to_css
from engine.synthesizer.axes import AxisValues

HERE = Path(__file__).resolve().parent
# name: (seed, axes, arabic)
CASES = {
    "3366ff": ("#3366FF", AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), True),
    "ffd400": ("#FFD400", AxisValues(0.8, 0.9, 0.2, 0.9, 0.3, 0.9, 0.8), True),
    "6b4423": ("#6B4423", AxisValues(0.2, 0.1, 0.9, 0.1, 0.9, 0.1, 0.1), True),
    "3366ff-latin": ("#3366FF", AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), False),
}


def render(seed, axes, arabic=True):
    ts = build_system(axes, seed, arabic=arabic).tokens
    return to_css(ts), dump_dtcg(ts)


if __name__ == "__main__":
    for name, case in CASES.items():
        css, dtcg = render(*case)
        (HERE / f"system-{name}.css").write_text(css, encoding="utf-8")
        (HERE / f"system-{name}.json").write_text(dtcg, encoding="utf-8")
        print("wrote", f"system-{name}.css", f"system-{name}.json")
