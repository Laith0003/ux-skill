"""Color output matches the golden: resolved values in all four contexts
(light and dark, standard and high contrast), DTCG $values, the CSS lines
of the :root and dark blocks, and every high-contrast CSS rule (the
data-contrast attribute rules and the prefers-contrast media rules, alone
and combined with dark). Roles added later are ignored; every
role the golden holds must be unchanged. A task that changes color output
on purpose recaptures the golden and lists every changed role."""
import json
from pathlib import Path

import pytest

from engine.foundations import build_color, to_css, to_dtcg
from engine.synthesizer.axes import AxisValues

GOLDEN = Path(__file__).resolve().parent / "golden"
SEEDS = ("#3366FF", "#FFD400", "#6B4423")
CONTEXTS = {"light": "scheme:light,contrast:standard", "dark": "scheme:dark,contrast:standard",
            "light-high": "scheme:light,contrast:high", "dark-high": "scheme:dark,contrast:high"}


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


@pytest.mark.parametrize("seed", SEEDS)
def test_standard_and_high_contrast_output_matches_the_golden(seed):
    golden = json.loads((GOLDEN / f"color-{seed[1:].lower()}.json").read_text(encoding="utf-8"))
    ts = build_color(AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), seed).tokens
    for path, want in golden["resolved"].items():
        assert set(want) == set(CONTEXTS), path
        for name, ctx in CONTEXTS.items():
            assert ts.resolve(path, ctx) == want[name], f"{path} ({ctx})"
    doc = to_dtcg(ts)
    for path, want in golden["dtcg"].items():
        node = doc
        for part in path.split("."):
            node = node[part]
        assert node["$value"] == want, path
    css = to_css(ts)
    known = {line.split(":")[0] for line in golden["css_root"]}

    def ours(lines):
        return [line for line in lines if line.split(":")[0] in known]

    assert ours(_block(css, ":root {")) == golden["css_root"]
    assert sorted(ours(_block(css, ':root[data-theme="dark"] {'))) == golden["css_dark"]
    high = _high_rules(css)
    assert len(golden["css_high"]) == 6
    assert {key: sorted(ours(high[key])) for key in golden["css_high"]} == golden["css_high"]
