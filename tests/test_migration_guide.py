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


def test_enhance_is_described_as_the_report_it_is():
    """system enhance writes a report and changes nothing; adding what is
    missing is system extend's job. The guide and the 4.0.0 entry say so."""
    import re

    from click.testing import CliRunner

    from engine.cli.main import cli
    help_text = CliRunner().invoke(cli, ["system", "enhance", "--help"]).output
    assert "A report only; nothing is rewritten." in " ".join(help_text.split())
    changelog = (GUIDE.parents[1] / "CHANGELOG.md").read_text(encoding="utf-8")
    # The 4.0.0 notes sit under [Unreleased] until 4.0.0 ships.
    entry = changelog.split("## [Unreleased]", 1)[1].split("\n## [", 1)[0]
    for name, text in (("docs/migrating-to-4.md", GUIDE.read_text(encoding="utf-8")),
                       ("CHANGELOG.md 4.0.0", entry)):
        flat = " ".join(text.split())
        for sentence in re.split(r"(?<=[.;])\s", flat):
            if "enhance" in sentence and "extend" not in sentence.split("enhance", 1)[0]:
                clause = sentence.split("enhance", 1)[1].split("extend", 1)[0]
                assert "writes the roles" not in clause and "adds" not in clause, (name, sentence)
        assert re.search(r"enhance.{0,200}?report", flat), name
