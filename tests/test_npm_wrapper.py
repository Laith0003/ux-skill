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


# ------------------------------------------------ the pip last resort
#
# A temp PATH holds only shims: an old `uxskill` that reports 3.2.0, a fake
# `python3` that logs each call, and the real `which`. No pipx, so the
# wrapper reaches its last resort, pip install --user.

_OLD_UXSKILL = """#!/bin/sh
echo "uxskill $*" >> "$LOG"
echo "uxskill, version 3.2.0"
"""

_PYTHON3 = """#!/bin/sh
echo "python3 $*" >> "$LOG"
if [ "$1" = "-m" ] && [ "$2" = "pip" ]; then exit "${PIP_EXIT:-0}"; fi
if [ "$1" = "-m" ] && [ "$2" = "engine.cli.main" ]; then
  if [ "$3" = "--version" ]; then echo "python -m engine.cli.main, version $ENGINE_VERSION"; exit 0; fi
  echo "engine ran"; exit 0
fi
exit 3
"""


def _shim(folder, name, text):
    path = folder / name
    path.write_text(text)
    path.chmod(0o755)


def _run_packaged(tmp_path, *, python3=True, pip_exit=0, engine_version=None):
    """Run the wrapper as npm installs it (bin/ and package.json, no
    engine/ beside it) with PATH limited to the shims."""
    pkg = tmp_path / "pkg"
    (pkg / "bin").mkdir(parents=True)
    shutil.copy(WRAPPER, pkg / "bin" / "uxskill.mjs")
    shutil.copy(ROOT / "package.json", pkg / "package.json")
    shims = tmp_path / "shims"
    shims.mkdir()
    (shims / "which").symlink_to(shutil.which("which"))
    _shim(shims, "uxskill", _OLD_UXSKILL)
    if python3:
        _shim(shims, "python3", _PYTHON3)
    log = tmp_path / "calls.log"
    log.write_text("")
    version = _node("pythonSpec()")
    env = {"PATH": str(shims), "HOME": str(tmp_path), "LOG": str(log),
           "PIP_EXIT": str(pip_exit), "ENGINE_VERSION": engine_version or version}
    out = subprocess.run([shutil.which("node"), str(pkg / "bin" / "uxskill.mjs"), "system",
                          "build", "--brand", "3366FF", "--out", "ds"],
                         capture_output=True, text=True, cwd=tmp_path, env=env, timeout=60)
    return out, log.read_text().splitlines(), version


needs_which = pytest.mark.skipif(shutil.which("which") is None, reason="which is not installed")


@needs_which
def test_after_pip_installs_it_runs_the_module_not_an_older_uxskill_on_path(tmp_path):
    out, calls, version = _run_packaged(tmp_path)
    assert out.returncode == 0, out.stderr
    assert "engine ran" in out.stdout
    assert f"python3 -m pip install --user --quiet uxskill=={version}" in calls
    assert "python3 -m engine.cli.main system build --brand 3366FF --out ds" in calls
    assert [c for c in calls if c.startswith("uxskill")] == ["uxskill --version"], calls


@needs_which
def test_a_failed_pip_install_says_pip_failed_and_gives_the_pinned_line(tmp_path):
    out, calls, version = _run_packaged(tmp_path, pip_exit=1)
    assert out.returncode == 1
    assert f"pip could not install uxskill=={version}" in out.stderr
    assert f"pipx install uxskill=={version}" in out.stderr
    assert "Python runtime" not in out.stderr
    assert not any("engine.cli.main" in c or c.startswith("uxskill system") for c in calls)


@needs_which
def test_without_python3_it_says_there_is_no_python_runtime(tmp_path):
    out, calls, version = _run_packaged(tmp_path, python3=False)
    assert out.returncode == 1
    assert "no Python runtime" in out.stderr and f"uxskill=={version}" in out.stderr
    assert not any(c.startswith("uxskill system") for c in calls)


@needs_which
def test_it_never_runs_a_module_of_another_version(tmp_path):
    out, calls, version = _run_packaged(tmp_path, engine_version="3.2.0")
    assert out.returncode == 1
    assert "3.2.0" in out.stderr and f"uxskill=={version}" in out.stderr
    assert "engine ran" not in out.stdout
    assert not any(c.startswith(("uxskill system", "python3 -m engine.cli.main system"))
                   for c in calls)
