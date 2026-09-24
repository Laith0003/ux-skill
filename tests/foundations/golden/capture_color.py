"""Writes the color golden: for three seeds, every color token's resolved
value in all four contexts (light and dark, standard and high contrast),
its DTCG $value, the CSS lines of the :root and dark blocks, and every
high-contrast CSS rule (attribute and media, alone and with dark). First
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


def _high_rules(css):
    """Every rule that applies high contrast, keyed by its media query and
    selector ("@media Q | selector", or the selector alone), with its lines."""
    rules, media, head, lines = {}, "", None, []
    for raw in css.splitlines():
        line = raw.strip()
        if line.startswith("@media "):
            media = line[len("@media "):-1].strip()
        elif line.endswith("{"):
            head, lines = line[:-1].strip(), []
        elif line == "}":
            if head is not None:
                key = f"@media {media} | {head}" if media else head
                if "contrast" in key:
                    rules[key] = lines
                head = None
            else:
                media = ""
        elif line and head is not None:
            lines.append(line)
    return rules


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
        "css_high": {key: sorted(lines) for key, lines in _high_rules(css).items()},
    }


if __name__ == "__main__":
    for seed in SEEDS:
        out = HERE / f"color-{seed[1:].lower()}.json"
        out.write_text(json.dumps(capture(seed), indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote", out.name)
