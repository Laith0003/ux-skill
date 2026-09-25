"""Every page on the site states the version in pyproject.toml.

`scripts/site_version.py` defines what counts as a current-version claim.
Posts under docs/blog/ are dated articles about a release, so their head
metadata may name the release they cover.
"""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("site_version", ROOT / "scripts" / "site_version.py")
sv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sv)

PAGES = sorted((ROOT / "docs").rglob("*.html"))


def test_version_is_read_from_pyproject():
    assert sv.version().count(".") == 2 and sv.line() == ".".join(sv.version().split(".")[:2])


def test_the_homepages_state_the_current_version():
    """The check itself must find the claims it guards."""
    home = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    labels = {label for label, _ in sv.claims(home)}
    assert {"hero pill", "version footer", "SoftwareApplication.softwareVersion",
            "TechArticle.about.softwareVersion", "hero numeral", "head title"} <= labels


def test_a_stale_version_is_caught():
    stale = ('<title>uxskill v3.1, Stop</title></head>'
             '<span class="pill"><span class="d"></span>v3.1.0&nbsp;·&nbsp;LIVE</span>')
    assert [v for _, v in sv.claims(stale) if not sv.agrees(v)] == ["3.1.0", "3.1"]


@pytest.mark.parametrize("page", PAGES, ids=lambda p: str(p.relative_to(ROOT / "docs")))
def test_page_states_only_the_pyproject_version(page):
    html = page.read_text(encoding="utf-8")
    release_post = "blog" in page.relative_to(ROOT / "docs").parts
    wrong = [f"{label}: {v}" for label, v in sv.claims(html, is_release_post=release_post)
             if not sv.agrees(v)]
    assert wrong == [], (f"{page.relative_to(ROOT)} states a version other than "
                         f"{sv.version()} (pyproject.toml): {wrong}")
