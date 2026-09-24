"""The shipped guidance describes every semantic role and every check the
build has, in full and Latin-only builds, and ships with the package."""
import re
from pathlib import Path

import pytest

from engine.foundations import FOUNDATIONS, build_system
from engine.rulepack.guidance import (
    GUIDANCE_DIR, SHARED, guidance_problems, load_guidance, role_catalog)
from engine.synthesizer.axes import AxisValues

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("arabic", [True, False])
@pytest.mark.parametrize("axes", [AxisValues(*[0.5] * 7), AxisValues(*[0.0] * 7),
                                  AxisValues(*[1.0] * 7)])
def test_every_role_and_check_is_described(arabic, axes):
    ts = build_system(axes, "#3366FF", arabic=arabic).tokens
    assert guidance_problems(ts) == []
    catalog = role_catalog(ts)
    assert all(e.description for e in catalog)
    assert {e.foundation for e in catalog} == {f.name for f in FOUNDATIONS}


def test_every_foundation_and_shared_topic_has_a_file():
    for f in FOUNDATIONS:
        assert load_guidance(f.name).title
    for name in SHARED:
        assert load_guidance(name).title


def test_guidance_cites_only_records_that_exist():
    records = {p.stem for p in (GUIDANCE_DIR.parent / "decisions").glob("*.md")}
    for path in GUIDANCE_DIR.glob("*.md"):
        for cited in re.findall(r"decisions/([a-z0-9-]+)\.md", path.read_text(encoding="utf-8")):
            assert cited in records, (path.name, cited)


def test_guidance_ships_with_the_package():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"engine.rulepack" = ["decisions/*.md", "guidance/*.md"]' in pyproject
