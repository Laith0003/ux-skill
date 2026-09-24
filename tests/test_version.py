"""One version everywhere. Python packaging writes it the PEP 440 way
(4.0.0b1); npm and the Claude Code plugin write it the semver way
(4.0.0-beta.1). This test holds every copy to the same release."""
import json
import re
from pathlib import Path

from engine import __version__

ROOT = Path(__file__).resolve().parents[1]
_PEP440 = re.compile(r"(\d+\.\d+\.\d+)(?:(a|b|rc)(\d+))?")
_TAG = {"a": "alpha", "b": "beta", "rc": "rc"}


def semver(pep440: str) -> str:
    """4.0.0b1 -> 4.0.0-beta.1; 4.0.0 -> 4.0.0."""
    m = _PEP440.fullmatch(pep440)
    assert m, f"{pep440!r} is not a release or pre-release version"
    base, tag, n = m.groups()
    return f"{base}-{_TAG[tag]}.{n}" if tag else base


def test_semver_mapping():
    assert semver("4.0.0b1") == "4.0.0-beta.1"
    assert semver("4.1.0rc2") == "4.1.0-rc.2"
    assert semver("4.0.0") == "4.0.0"


def test_pyproject_matches_the_engine():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^version = "([^"]+)"$', text, re.M).group(1) == __version__


def test_package_json_and_plugin_json_match():
    for rel in ("package.json", ".claude-plugin/plugin.json"):
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        assert data["version"] == semver(__version__), rel


def test_readme_badge_and_changelog_match():
    # shields.io writes a literal hyphen in a badge as two hyphens.
    badge = semver(__version__).replace("-", "--")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"badge/version-{badge}-" in readme
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    first = re.search(r"^## \[([^\]]+)\]", changelog, re.M).group(1)
    assert first == semver(__version__)


def test_npm_publishes_a_pre_release_under_its_own_tag():
    # npx uxskill and npm i uxskill must stay on the last stable release;
    # the docs send beta users to npx uxskill@beta.
    data = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    tag = _PEP440.fullmatch(__version__).group(2)
    expected = _TAG[tag] if tag else None
    assert data.get("publishConfig", {}).get("tag") == expected
