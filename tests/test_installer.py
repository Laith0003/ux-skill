"""Installer smoke tests — dry-run install for every supported IDE."""
from pathlib import Path

import pytest

from engine.installer import install, detect_ides, SUPPORTED


@pytest.mark.parametrize("target", SUPPORTED)
def test_dry_run_install(target, tmp_path: Path):
    """Every supported target installs (dry-run) without raising."""
    report = install(target, root=str(tmp_path), dry_run=True)
    assert report.target == target
    assert report.dry_run is True


def test_detect_ides_empty(tmp_path: Path):
    """A blank dir detects no IDEs."""
    assert detect_ides(tmp_path) == []


def test_detect_claude_code(tmp_path: Path):
    (tmp_path / ".claude").mkdir()
    detected = detect_ides(tmp_path)
    assert "claude-code" in detected


def test_detect_cursor(tmp_path: Path):
    (tmp_path / ".cursorrules").write_text("test")
    assert "cursor" in detect_ides(tmp_path)


def test_unknown_target_raises(tmp_path: Path):
    with pytest.raises(ValueError):
        install("not-a-real-ide", root=str(tmp_path), dry_run=True)
