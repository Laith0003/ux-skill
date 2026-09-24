"""Writes the color golden: for three seeds, every color token's resolved
value in all four contexts (light and dark, standard and high contrast),
its DTCG $value, and the CSS lines of the :root and dark blocks. First
captured before the mode-axes migration to prove it changed nothing;
recaptured only when a task changes color output on purpose, and the diff
is reviewed. From the repo root:

    PYTHONPATH=. python tests/foundations/golden/capture_color.py
"""
import json
from pathlib import Path

from engine.foundations import build_color, to_css, to_dtcg
from engine.synthesizer.axes import AxisValues

SEEDS = ("#3366FF", "#FFD400", "#6B4423")
CONTEXTS = {"light": "scheme:light,contrast:standard", "dark": "scheme:dark,contrast:standard",
            "light-high": "scheme:light,contrast:high", "dark-high": "scheme:dark,contrast:high"}
HERE = Path(__file__).resolve().parent


def _block(css, opener):
    body = css.split(opener, 1)[1].split("}", 1)[0]
    return [line.strip() for line in body.strip().splitlines()]


def capture(seed):
    ts = build_color(AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), seed).tokens
    doc = to_dtcg(ts)

    def dtcg_value(path):
        node = doc
        for part in path.split("."):
            node = node[part]
        return node["$value"]

    css = to_css(ts)
    return {
        "resolved": {t.path: {name: ts.resolve(t.path, ctx) for name, ctx in CONTEXTS.items()}
                     for t in ts.tokens()},
        "dtcg": {t.path: dtcg_value(t.path) for t in ts.tokens()},
        "css_root": _block(css, ":root {"),
        "css_dark": sorted(_block(css, '[data-theme="dark"] {')),
    }


if __name__ == "__main__":
    for seed in SEEDS:
        out = HERE / f"color-{seed[1:].lower()}.json"
        out.write_text(json.dumps(capture(seed), indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote", out.name)
