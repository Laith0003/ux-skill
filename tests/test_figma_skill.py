"""ux-skill packaged as a skill for Figma's agent, in the agentskills
discovery format Figma serves its own skills in: an index of skill-md
entries, each a SKILL.md with name and description front matter."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "figma-skill"


def _front(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "SKILL.md opens with front matter"
    out = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip().strip('"')
    return out


def test_the_index_lists_each_skill_by_name_and_relative_url():
    index = json.loads((PACK / "index.json").read_text(encoding="utf-8"))
    assert index["$schema"].startswith("https://schemas.agentskills.io/discovery/")
    for skill in index["skills"]:
        assert skill["type"] == "skill-md"
        path = PACK / skill["url"]
        assert path.is_file() and path.parent.name == skill["name"]
        front = _front(path.read_text(encoding="utf-8"))
        assert front["name"] == skill["name"] and front["description"] == skill["description"]
        assert front["disable-model-invocation"] == "false"


def test_the_skill_names_commands_and_files_the_engine_has():
    text = (PACK / "ux-skill-foundations" / "SKILL.md").read_text(encoding="utf-8")
    from engine.io.figma_out import figma_files  # noqa: F401
    for name in ("figma-variables.json", "figma-variables.js", "figma-read-variables.js"):
        assert name in text
    cli = (ROOT / "engine" / "cli" / "main.py").read_text(encoding="utf-8")
    for command in ("import", "extend", "export", "build"):
        assert f'command("{command}")' in cli or f"command('{command}')" in cli, command
    assert "figma-use" in text and "photograph" in text


def test_every_relative_link_resolves_and_the_text_is_plain():
    for f in PACK.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)#:]+)\)", text):
            assert (f.parent / link).is_file(), (f, link)
        assert not re.search("[–—]", text) and " -- " not in text, f


def test_every_command_the_skill_names_parses_with_its_arguments():
    """Each `uxskill ...` command in the skill carries the arguments and
    options the CLI requires, so the agent never stops at a usage error. A
    placeholder such as <file> stands for a path, so only a missing or
    unknown argument fails here, not a path that does not exist."""
    import shlex

    import click

    from engine.cli.main import cli
    text = "\n".join(f.read_text(encoding="utf-8") for f in sorted(PACK.rglob("*.md")))
    commands = re.findall(r"`uxskill ([^`]+)`", text)
    assert len(commands) >= 5
    for line in commands:
        args = [a.replace("<", "").replace(">", "") for a in shlex.split(line)]
        group = cli
        while isinstance(group, click.Group):
            name, args = args[0], args[1:]
            group = group.get_command(click.Context(cli), name)
            assert group is not None, (line, name)
        try:
            group.make_context(group.name, list(args))
        except click.BadParameter as exc:
            assert "does not exist" in str(exc), (line, exc)
        except click.UsageError as exc:
            raise AssertionError(f"{line}: {exc}")
