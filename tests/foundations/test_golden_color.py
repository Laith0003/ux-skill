"""The mode-axes migration keeps standard-contrast light and dark output
identical: resolved values, DTCG $values, and the CSS lines of the :root
and dark blocks match the golden captured before the change. Roles added
later are ignored; every role the golden holds must be unchanged."""
import json
from pathlib import Path

import pytest

from engine.foundations import build_color, to_css, to_dtcg
from engine.synthesizer.axes import AxisValues

GOLDEN = Path(__file__).resolve().parent / "golden"
SEEDS = ("#3366FF", "#FFD400", "#6B4423")
LIGHT, DARK = "scheme:light,contrast:standard", "scheme:dark,contrast:standard"


def _block(css, opener):
    body = css.split(opener, 1)[1].split("}", 1)[0]
    return [line.strip() for line in body.strip().splitlines()]


@pytest.mark.parametrize("seed", SEEDS)
def test_standard_contrast_output_matches_the_golden(seed):
    golden = json.loads((GOLDEN / f"color-{seed[1:].lower()}.json").read_text(encoding="utf-8"))
    ts = build_color(AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), seed).tokens
    for path, want in golden["resolved"].items():
        assert ts.resolve(path, LIGHT) == want["light"], path
        assert ts.resolve(path, DARK) == want["dark"], path
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
