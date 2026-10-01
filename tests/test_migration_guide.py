"""The migration guide names only 4.0 roles a built system has."""
import re
from pathlib import Path

from engine.foundations import build_system, to_css
from engine.synthesizer.axes import AxisValues

GUIDE = Path(__file__).resolve().parents[1] / "docs" / "migrating-to-4.md"


def test_every_4_0_role_in_the_table_is_built():
    text = GUIDE.read_text(encoding="utf-8")
    table = text[text.index("## 3.x names and their 4.0 roles"):text.index("## What changes")]
    css = to_css(build_system(AxisValues(*[0.5] * 7), "#3366FF").tokens)
    built = set(re.findall(r"(--[a-z0-9-]+):", css))
    for row in table.splitlines()[2:]:
        cells = row.split("|")
        if len(cells) < 4:
            continue
        for name in re.findall(r"`(--[a-z0-9-]+)`", cells[2] + cells[3]):
            if "*" not in name:
                assert name in built, name


def test_the_guide_is_plain_text():
    text = GUIDE.read_text(encoding="utf-8")
    assert not re.search("[–—]", text) and " -- " not in text
