"""Gate check (f) run for real: the snippet in commands/ux-design.md, in
headless Chromium at 390 by 844 and 360 by 780.

Only what is pinned on the first screen at load counts as an overlay: a
sticky table header far down the page does not, a promo bar at the top does.
The snippet runs under UXSKILL_GATE_PYTHON when set (a Python with
Playwright), else under this one. Skipped when neither has Playwright and
Chromium.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

GATE_PYTHON = os.environ.get("UXSKILL_GATE_PYTHON") or sys.executable
_PROBE = ("from playwright.sync_api import sync_playwright\n"
          "with sync_playwright() as p: p.chromium.launch().close()")
if subprocess.run([GATE_PYTHON, "-c", _PROBE], capture_output=True, timeout=120,
                  check=False).returncode:
    pytest.skip("no Python with Playwright and Chromium; set UXSKILL_GATE_PYTHON to one",
                allow_module_level=True)

HEAD = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;font:16px/1.4 sans-serif}
header{position:sticky;top:0;background:#fff;height:56px;z-index:2}
.navrow{display:flex;justify-content:space-between;align-items:center;height:56px;padding:0 12px}
.hero{padding:24px 16px}.btn{display:inline-block;padding:12px 16px;background:#222;color:#fff}
.consent{position:fixed;bottom:0;left:0;right:0;height:88px;background:#eee}
.chat{position:fixed;bottom:12px;right:12px;width:56px;height:56px;background:#09f}
.promo{position:fixed;top:0;left:0;right:0;height:40px;background:#fc0;z-index:3}
.bar{position:fixed;bottom:0;left:0;right:0;height:64px;background:#333}
</style></head><body>
<header><div class="navrow"><span class="brand"><span class="wm"><b>Tash</b></span></span>
<a class="btn" href="#s"><span class="btn-label">Start</span></a></div></header>
<section class="hero"><h1>Settle every bill</h1><div style="height:%dpx"></div>
<a class="btn btn-primary" href="#s"><span class="btn-label">Start</span></a></section>
"""
TAIL = '<div style="height:2400px"></div></body></html>'
TABLE = ('<div style="height:1400px"></div><table><thead style="position:sticky;top:56px">'
         '<tr><th>Basic</th><th>Pro</th></tr></thead><tbody>'
         + "<tr><td>1</td><td>2</td></tr>" * 40 + "</tbody></table>")

PAGES = {
    "one-banner": (HEAD % 100 + '<div class="consent"></div>' + TAIL, 0),
    "banner-and-a-sticky-table-header-below": (
        HEAD % 100 + '<div class="consent"></div>' + TABLE + TAIL, 0),
    "promo-bar-and-bottom-bar": (
        HEAD % 100 + '<div class="promo"></div><div class="bar"></div>' + TAIL, 1),
    "banner-and-chat": (HEAD % 100 + '<div class="consent"></div><div class="chat"></div>' + TAIL, 1),
    "action-under-the-banner": (HEAD % 640 + '<div class="consent"></div>' + TAIL, 1),
    "action-covered": (HEAD % 100 + '<div style="position:fixed;top:230px;left:0;right:0;'
                       'height:120px;background:red"></div>' + TAIL, 1),
}


def _snippet() -> str:
    doc = (ROOT / "commands" / "ux-design.md").read_text(encoding="utf-8")
    m = re.search(r"```bash\npython3 - \"\$OUTPUT_HTML\" <<'PY'\n(.*?)\nPY\n```", doc, re.DOTALL)
    assert m, "the responsive gate snippet is missing from commands/ux-design.md"
    return m.group(1)


@pytest.fixture(scope="module")
def gate(tmp_path_factory):
    path = tmp_path_factory.mktemp("gate") / "gate.py"
    path.write_text(_snippet(), encoding="utf-8")
    return path


@pytest.mark.parametrize("name", sorted(PAGES))
def test_check_f_counts_only_what_is_on_the_first_screen(gate, tmp_path, name):
    html, expect = PAGES[name]
    page = tmp_path / f"{name}.html"
    page.write_text(html, encoding="utf-8")
    run = subprocess.run([GATE_PYTHON, str(gate), str(page)], capture_output=True,
                         text=True, timeout=120, check=False)
    assert run.returncode == expect, f"{name}: exit {run.returncode}\n{run.stdout}{run.stderr}"
    lost = "ask-lost=True" in run.stdout
    assert lost is bool(expect), run.stdout
