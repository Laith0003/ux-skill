"""CLI brand-wiring tests -- subprocess, mirroring how the slash commands invoke it.

Engine-level tests (test_brand_wiring) prove the logic; these guard the CLI PLUMBING
(option -> Brief.brand / brand_profile), the layer where a wiring bug hides (passing
the flag but forgetting to thread it into the engine call). Runs in a tmp cwd so the
evolve loop's .ux/ output never touches the repo.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("click")  # the brand subcommand only exists on the click path

ROOT = Path(__file__).resolve().parents[1]

_PROFILE = {
    "source": "x", "name": "Instant Skip Hire",
    "logo": {"url": "/l.avif", "alt": "Instant Skip Hire logo"},
    "primary": "#f0890f", "primary_family": "orange", "primary_source": "logo",
    "secondary": ["#1c3829"],
    "fonts": {"display": "", "body": "", "type_personality": "bold rounded",
              "display_source": "logo-style", "site_stack": "Roboto Flex"},
    "imagery": [], "voice": "", "notes": [],
}


def _run(args, cwd):
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    return subprocess.run(
        [sys.executable, "-m", "engine.cli.main", "--no-pretty", *args],
        cwd=str(cwd), env=env, capture_output=True, text=True)


def test_brand_cmd_writes_brand_md_and_json(tmp_path):
    sig = tmp_path / "signals.json"
    sig.write_text(json.dumps({
        "name": "Instant Skip Hire",
        "logo": {"src": "/l.avif", "alt": "Instant Skip Hire logo"},
        "logo_colors": [{"hex": "#f0890f"}, {"hex": "#1c3829"}],
        "brand_colors": [{"hex": "#1c3829"}],
        "logo_type_style": "bold rounded humanist sans",
        "fonts": {"h1": '"Roboto Flex", system-ui'},
    }), encoding="utf-8")
    r = _run(["brand", "--signals-file", str(sig), "--out", str(tmp_path)], tmp_path)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["primary"] == "#f0890f" and out["primary_source"] == "logo"
    md = (tmp_path / "brand.md").read_text(encoding="utf-8")
    assert "#f0890f" in md and "Instant Skip Hire" in md
    assert json.loads((tmp_path / "brand.json").read_text(encoding="utf-8"))["primary"] == "#f0890f"


def test_recommend_brand_file_anchors_palette(tmp_path):
    bj = tmp_path / "brand.json"
    bj.write_text(json.dumps(_PROFILE), encoding="utf-8")
    r = _run(["recommend", "--project-type", "landing", "--tone", "bold",
              "--brand-file", str(bj)], tmp_path)
    assert r.returncode == 0, r.stderr
    rec = json.loads(r.stdout)
    assert rec["palette"]["colors"]["primary"] == "#f0890f"
    assert rec["brand"]["name"] == "Instant Skip Hire"


def test_evolve_brand_file_fails_off_brand(tmp_path):
    bj = tmp_path / "brand.json"
    bj.write_text(json.dumps(_PROFILE), encoding="utf-8")
    off = tmp_path / "off.html"
    off.write_text('<!doctype html><html><body><main><h1 style="color:#cc785c">Skips</h1>'
                   '<p>house clay, no logo, no image</p></main></body></html>', encoding="utf-8")
    r = _run(["evolve", str(off), "--brand-file", str(bj), "--no-log"], tmp_path)
    assert r.returncode == 1   # brand hard floor -> gate_failed -> exit 1
