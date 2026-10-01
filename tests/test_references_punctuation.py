"""The prose in references/ carries no em dashes, en dashes or "--" as punctuation.

Sentences use a period, comma, colon or parentheses instead, and a numeric
range reads "4 to 8px". Code is left alone: fenced blocks, inline code spans
and HTML comments are skipped, and so are CLI flags (--foo), CSS custom
properties (--color-x), table separator rows and horizontal rules.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"
DOCS = sorted(REF.rglob("*.md"))

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
SEPARATOR = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$")
# Two hyphens that are not part of a longer run, not an HTML comment
# marker, and not the start of a flag or a custom property name.
DOUBLE = re.compile(r"(?<![-!])--(?![-\w>])")
DASHES = {"\u2014": "em dash", "\u2013": "en dash"}


def _strip_inline_code(line: str) -> str:
    """The line with every inline code span blanked out."""
    out, i = [], 0
    while i < len(line):
        if line[i] != "`":
            out.append(line[i])
            i += 1
            continue
        run = len(line[i:]) - len(line[i:].lstrip("`"))
        close = re.compile(r"(?<!`)" + "`" * run + r"(?!`)").search(line, i + run)
        if close is None:
            out.append(line[i:i + run])
            i += run
            continue
        out.append(" ")
        i = close.end()
    return "".join(out)


def prose_lines(text: str):
    """Yield (line number, prose) for every line outside code."""
    fence = None
    in_comment = False
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                if not line.strip().strip(fence[0]):
                    fence = None
            continue
        if match:
            fence = match.group(1)
            continue
        prose = []
        rest = line
        while rest:
            if in_comment:
                end = rest.find("-->")
                if end == -1:
                    rest = ""
                    break
                rest = rest[end + 3:]
                in_comment = False
            else:
                start = rest.find("<!--")
                if start == -1:
                    prose.append(rest)
                    break
                prose.append(rest[:start])
                rest = rest[start + 4:]
                in_comment = True
        yield number, _strip_inline_code(" ".join(prose))


def findings(path: Path, root: Path = ROOT) -> list[str]:
    found = []
    rel = path.relative_to(root)
    for number, line in prose_lines(path.read_text(encoding="utf-8")):
        for char, name in DASHES.items():
            if char in line:
                found.append(f"{rel}:{number}: {name} in prose; use a period, comma, colon "
                             f"or parentheses, or 'to' for a range")
        if not SEPARATOR.match(line) and DOUBLE.search(line):
            found.append(f"{rel}:{number}: '--' used as punctuation; use a period, comma, "
                         f"colon or parentheses")
    return found


def test_references_exist():
    assert len(DOCS) > 100


@pytest.mark.parametrize("path", DOCS, ids=lambda p: str(p.relative_to(REF)))
def test_no_dash_punctuation_in_prose(path):
    found = findings(path)
    assert not found, "\n".join(found[:20]) + (f"\n... {len(found) - 20} more"
                                               if len(found) > 20 else "")


def test_the_check_skips_code_and_catches_prose(tmp_path):
    sample = tmp_path / "references" / "sample.md"
    sample.parent.mkdir()
    sample.write_text(
        "---\n"
        "name: sample\n"
        "---\n"
        "Run `ux lint --render` or pass --strict; the role sets --color-ink.\n"
        "The block--modifier class and `a \u2014 b` stay.\n"
        "<!-- a marker -- with dashes \u2014 inside -->\n"
        "| a | b |\n"
        "|---|:--:|\n"
        "```css\n"
        ":root { --x: 1; } /* 4\u20138px \u2014 note -- here */\n"
        "```\n"
        "\n"
        "---\n"
        "Plain prose, then a pause \u2014 bad.\n"
        "A range 4\u20138px is bad.\n"
        "A pause -- bad.\n",
        encoding="utf-8")
    found = findings(sample, tmp_path)
    assert [f.split(":")[1] for f in found] == ["14", "15", "16"]


def _backfill():
    path = ROOT / "scripts" / "backfill-brand-designs.py"
    spec = importlib.util.spec_from_file_location("backfill_brand_designs", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BRANDS = sorted(p for p in (ROOT / "data" / "brands").glob("*.json") if p.stem != "_index")


@pytest.mark.parametrize("path", BRANDS, ids=lambda p: p.stem)
def test_every_rendered_brand_reference_has_no_dash_punctuation(path):
    body = _backfill().render(path.stem, json.loads(path.read_text(encoding="utf-8")))
    for char, name in DASHES.items():
        assert char not in body, f"{path.stem}: rendered reference holds an {name}"
    assert " -- " not in body, f"{path.stem}: rendered reference holds ' -- '"


def test_a_dash_entity_becomes_a_comma_with_one_space():
    unescape = _backfill().html_unescape_lite
    assert unescape("calm &mdash; never loud") == "calm, never loud"
    assert unescape("calm&mdash;never loud") == "calm, never loud"
