"""The npm wrapper runs the Python engine of its own version.

npm ships only bin/, so the wrapper finds or installs the Python package.
Without a pin, pip skips pre-releases and an npm beta would quietly run the
last stable release. These tests pin the version mapping and the pin itself.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "bin" / "uxskill.mjs"

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


def _node(expr):
    code = f"import {{ pythonSpec }} from {json.dumps(WRAPPER.as_uri())}; console.log({expr});"
    out = subprocess.run(["node", "--input-type=module", "-e", code],
                         capture_output=True, text=True, check=True, cwd=ROOT)
    return out.stdout.strip()


@pytest.mark.parametrize("npm,python", [
    ("4.0.0", "4.0.0"), ("4.0.0-beta.1", "4.0.0b1"), ("4.1.0-alpha.2", "4.1.0a2"),
    ("4.0.0-rc.3", "4.0.0rc3"), ("3.2.1", "3.2.1"),
])
def test_npm_versions_map_to_python_versions(npm, python):
    assert _node(f"pythonSpec({json.dumps(npm)})") == python


def test_the_wrapper_pins_its_own_package_version():
    pkg = json.loads((ROOT / "package.json").read_text())["version"]
    assert _node("pythonSpec()") == _node(f"pythonSpec({json.dumps(pkg)})")
    text = WRAPPER.read_text()
    assert '"--spec", `uxskill==${' in text and '`uxskill==${' in text


def test_importing_the_wrapper_does_not_run_it():
    # The test imports pythonSpec; the command itself must only run as a script.
    assert _node("'imported'") == "imported"


def test_the_wrapper_runs_through_a_symlink(tmp_path):
    # npm installs the command as a symlink in node_modules/.bin, so the
    # script-or-import check must compare real paths.
    link = tmp_path / "uxskill"
    link.symlink_to(WRAPPER)
    out = subprocess.run(["node", str(link), "--version"], capture_output=True, text=True,
                         cwd=tmp_path, timeout=60)
    assert "version" in (out.stdout + out.stderr).lower()
