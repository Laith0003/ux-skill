"""R27 M11: output is byte-identical across processes, not only within one.

Each run builds three seeds in a fresh interpreter under a different
PYTHONHASHSEED, so any set or hash ordering that leaks into the CSS or the
DTCG text shows up as a diff.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

from engine.foundations import Token, TokenSet, build_color, dump_dtcg, to_css, to_dtcg
from engine.synthesizer.axes import AxisValues

REPO = Path(__file__).resolve().parents[2]
SEEDS = ("#3366FF", "#FFD400", "#6B4423")

_SCRIPT = """
import json, sys
from engine.foundations import build_color, dump_dtcg, to_css
from engine.synthesizer.axes import AxisValues
axes = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
out = {}
for seed in sys.argv[1:]:
    ts = build_color(axes, seed).tokens
    out[seed] = {"css": to_css(ts), "dtcg": dump_dtcg(ts)}
sys.stdout.write(json.dumps(out))
"""


def _run(hash_seed):
    env = dict(os.environ, PYTHONHASHSEED=str(hash_seed))
    env["PYTHONPATH"] = os.pathsep.join(p for p in (str(REPO), env.get("PYTHONPATH")) if p)
    proc = subprocess.run([sys.executable, "-c", _SCRIPT, *SEEDS], cwd=REPO, env=env,
                          capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def test_css_and_dtcg_are_byte_identical_across_hash_seeds():
    first, second = _run(1), _run(987)
    assert first == second
    axes = AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    for seed in SEEDS:
        ts = build_color(axes, seed).tokens
        assert first[seed] == {"css": to_css(ts), "dtcg": dump_dtcg(ts)}


def test_dump_dtcg_fixes_the_json_settings():
    ts = TokenSet()
    ts.add(Token("color.base.white", "color", "#FFFFFF", description="أبيض"))
    text = dump_dtcg(ts)
    assert text == json.dumps(to_dtcg(ts), indent=2, ensure_ascii=False) + "\n"
    assert text.endswith("}\n") and "أبيض" in text and "\\u" not in text
    assert text.startswith('{\n  "color": {\n    "base"')
