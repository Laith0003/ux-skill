"""The CI-only scans in .github/workflows/test.yml, run with the suite so a
failure shows up before a pull request does.

Every page in docs/ carries the analytics tag, and the plugin source carries
no emoji: the same code point ranges and folders the workflow scans.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# U+2713 (check mark) and U+2318 (command key) are allowed, as in the workflow.
_EMOJI = re.compile("[\U0001F300-\U0001F9FF\u2600-\u2712\u2714-\u27BF]")
_SCANNED_DIRS = ["commands", "agents", "engine", "tests", "bin"]
_SCANNED_SUFFIXES = {".py", ".json", ".md", ".html", ".css", ".ts", ".js", ".tsx", ".jsx"}
_SCANNED_ROOT_FILES = ["README.md", "CHANGELOG.md", "PRIVACY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"]


def _scanned_files():
    for name in _SCANNED_DIRS:
        for path in sorted((ROOT / name).rglob("*")):
            if path.is_file() and path.suffix in _SCANNED_SUFFIXES:
                yield path
    for name in _SCANNED_ROOT_FILES:
        if (ROOT / name).is_file():
            yield ROOT / name


def test_every_docs_page_carries_the_analytics_tag():
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "ensure-ga.py"), "--check"],
                         capture_output=True, text=True, cwd=ROOT)
    assert out.returncode == 0, out.stdout + out.stderr


def test_the_plugin_source_carries_no_emoji():
    found = []
    for path in _scanned_files():
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if _EMOJI.search(line):
                found.append(f"{path.relative_to(ROOT)}:{n}")
    assert not found, ("emoji in the plugin source, which the CI emoji scan rejects: "
                       f"{found}; write the code point as an escape such as \\u2630 instead")
