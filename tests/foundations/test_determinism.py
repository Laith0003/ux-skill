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
    assert text.startswith('{\n  "$extensions": {')


_SYSTEM_SCRIPT = """
import json, sys
from tests.foundations.golden.capture_system import CASES, render
sys.stdout.write(json.dumps({name: render(*CASES[name]) for name in sorted(CASES)}))
"""


def _run_system(hash_seed):
    env = dict(os.environ, PYTHONHASHSEED=str(hash_seed))
    env["PYTHONPATH"] = os.pathsep.join(p for p in (str(REPO), env.get("PYTHONPATH")) if p)
    proc = subprocess.run([sys.executable, "-c", _SYSTEM_SCRIPT], cwd=REPO, env=env,
                          capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def test_build_system_is_byte_identical_across_hash_seeds_and_matches_the_golden():
    first, second = _run_system(1), _run_system(987)
    assert first == second
    golden = REPO / "tests" / "foundations" / "golden"
    assert sorted(first) == sorted(p.stem[len("system-"):] for p in golden.glob("system-*.css"))
    for name, (css, dtcg) in first.items():
        assert css == (golden / f"system-{name}.css").read_text(encoding="utf-8")
        assert dtcg == (golden / f"system-{name}.json").read_text(encoding="utf-8")


_TRIAL_SCRIPT = """
import json, sys
from pathlib import Path
from engine.foundations.emit import (
    brief_audience, choose_axes, make_system, resolve_arabic, unread_lines)
out = {}
for name, brand in (("clinic", "#0F766E"), ("devtool", "#6D28D9"), ("restaurant", "#E85D04"),
                    ("fintech-ar", "#2563EB")):
    brief = json.loads(Path("tests/foundations/briefs", name + ".json").read_text("utf-8"))
    axes, source = choose_axes(brief, None)
    audience = brief_audience(brief)
    system = make_system(brand, axes, source, arabic=resolve_arabic(False, audience),
                         rule_pack=True, audience=audience, unread=unread_lines(brief))
    out[name] = dict(system.files)
sys.stdout.write(json.dumps(out))
"""


def test_the_trial_briefs_give_byte_identical_files_across_hash_seeds():
    """Every file a build writes (tokens, fonts.css, the report, the art and
    the rule pack) for the four site trial briefs, in two processes."""
    runs = []
    for hash_seed in (3, 4242):
        env = dict(os.environ, PYTHONHASHSEED=str(hash_seed))
        env["PYTHONPATH"] = os.pathsep.join(p for p in (str(REPO), env.get("PYTHONPATH")) if p)
        proc = subprocess.run([sys.executable, "-c", _TRIAL_SCRIPT], cwd=REPO, env=env,
                              capture_output=True, text=True, check=True)
        runs.append(json.loads(proc.stdout))
    assert runs[0] == runs[1]
    assert all("art/shapes.svg" in files and "fonts.css" in files for files in runs[0].values())
