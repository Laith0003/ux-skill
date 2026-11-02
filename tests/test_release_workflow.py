"""The release workflow: a version that lands on main with its notes in
docs/launch/release-<version>.md and no tag yet is tagged and published by
GitHub Actions, so a release never waits on a tag pushed by hand."""
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOW = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")


def test_it_runs_on_main_and_may_write_the_tag():
    assert re.search(r"push:\s*\n\s*branches: \[main\]", FLOW)
    assert "contents: write" in FLOW and "workflow_dispatch" in FLOW


def test_it_skips_a_tag_that_exists_and_a_version_without_notes():
    assert "ls-remote --exit-code --tags" in FLOW
    assert 'notes="docs/launch/release-${version}.md"' in FLOW
    assert "--notes-file" in FLOW and "--prerelease" in FLOW


def test_the_current_version_has_its_notes():
    version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    notes = ROOT / "docs" / "launch" / f"release-{version}.md"
    assert notes.is_file(), f"write the release notes for {version} at {notes.relative_to(ROOT)}"
    assert notes.read_text(encoding="utf-8").startswith(f"# ux-skill {version}")
