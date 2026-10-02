"""Every locale README says what the English README says.

The English README is held to the engine here too (the version, the MCP
tools, the data counts), and each of the 16 translations is held to the
English one: the same sections in the same order, the same code blocks and
inline code, the same figures section by section, the same links, the
current version and install commands, and none of the figures an earlier
release stated. The rule catalogue that scripts/readme_rules.py writes lives
in README.md only; each translation links to it and states its coverage.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pytest

from engine import __version__
from engine.data_loader import stats
from engine.mcp import TOOLS


def _badge(version: str) -> str:
    """The version as the README badge writes it: semver (4.0.0b2 is
    4.0.0-beta.2), with each hyphen doubled, since shields.io reads a single
    hyphen as a separator."""
    m = re.fullmatch(r"(\d+\.\d+\.\d+)(?:(a|b|rc)(\d+))?", version)
    base, tag, n = m.groups()
    name = {"a": "alpha", "b": "beta", "rc": "rc"}.get(tag)
    return (f"{base}-{name}.{n}" if tag else base).replace("-", "--")

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("ar", "de", "es", "fr", "hi", "id", "it", "ja", "ko", "pt-BR", "ru",
           "th", "tr", "vi", "zh", "zh-TW")
START, END = "<!-- rules:start -->", "<!-- rules:end -->"
RULES = json.loads((ROOT / "data" / "anti-patterns.json").read_text(encoding="utf-8"))["entries"]
TOOL_NAMES = [t["name"] if isinstance(t, dict) else str(t) for t in TOOLS]
COUNTS = stats()
ENTRIES = sum(COUNTS.values())
_MOVED = re.compile(r"^Moved to /(ux-[a-z0-9-]+)")

# Sections that describe what an earlier release shipped, with its figures.
HISTORY = ("### New in v3.1: brand-true, responsive, alive", "### What's new in v3")
CATALOGUE = "### Rules by category"
FENCE = re.compile(r"^[ ]*```.*?^[ ]*```", re.MULTILINE | re.DOTALL)


def _read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def _without_catalogue(text):
    if START not in text:
        return text
    return text[:text.index(START)] + text[text.index(END) + len(END):]


ENGLISH = _read("README.md")
EN = _without_catalogue(ENGLISH)


def _commands():
    real, aliases = set(), set()
    for path in sorted((ROOT / "commands").glob("ux-*.md")):
        head = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL).group(1)
        desc = next((line.partition(":")[2].strip() for line in head.splitlines()
                     if line.startswith("description:")), "")
        (aliases if _MOVED.match(desc) else real).add(path.stem)
    return real, aliases


CANONICAL, ALIASES = _commands()


def _sections(text):
    """(heading line, body) pairs; the text before the first heading is '_pre'."""
    out, head, body, fence = [], "_pre", [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and re.match(r"#{1,6} ", line):
            out.append((head, "\n".join(body)))
            head, body = line, []
        else:
            body.append(line)
    out.append((head, "\n".join(body)))
    return out


def _headings(text):
    return [h for h, _ in _sections(text) if h != "_pre"]


def slug(heading):
    """The anchor GitHub gives a heading."""
    text = re.sub(r"^#+\s*", "", heading).strip().lower()
    kept = []
    for ch in text:
        if ch in "-_":
            kept.append(ch)
        elif ch == " ":
            kept.append("-")
        elif unicodedata.category(ch)[0] in "PS" or unicodedata.category(ch) in ("Cc", "Cf"):
            continue
        else:
            kept.append(ch)
    return "".join(kept)


def _prose(text):
    """Text outside code blocks, with link targets dropped."""
    return re.sub(r"\]\([^)]*\)", "]", FENCE.sub("", text))


def _numbers(text):
    """Every figure of two or more digits that stands on its own (not the 11
    in a11y), thousands separators removed."""
    flat = re.sub(r"(?<=[0-9])[ .,\u00a0\u202f](?=[0-9]{3}(?![0-9]))", "", _prose(text))
    found = re.findall(r"(?<![A-Za-z0-9.])[0-9]+(?:[.:][0-9]+)*", flat)
    return Counter(n for n in found if sum(c.isdigit() for c in n) >= 2)


def _spans(text):
    return Counter(re.findall(r"`([^`\n]+)`", _prose(text)))


def _links(text):
    targets = set(re.findall(r"\]\(([^)\s]+)\)", text))
    return {t for t in targets
            if not t.startswith("#") and not re.match(r"README(\.[\w-]+)?\.md", t)}


def _locale(loc):
    return _read(f"README.{loc}.md")


def _paired(loc):
    """English and locale sections side by side, without the '_pre' block."""
    en = [s for s in _sections(EN) if s[0] != "_pre"]
    lo = [s for s in _sections(_locale(loc)) if s[0] != "_pre"]
    assert len(en) == len(lo), f"README.{loc}.md has {len(lo)} headings; English has {len(en)}"
    return list(zip(en, lo))


def _section(loc, english_heading):
    for (eh, _), (lh, lb) in _paired(loc):
        if eh == english_heading:
            return lh + "\n" + lb
    raise AssertionError(english_heading)


def _current(loc):
    """The locale text without the sections on earlier releases."""
    return "\n".join(lh + "\n" + lb for (eh, _), (lh, lb) in _paired(loc) if eh not in HISTORY)


# The English README against the engine.

def test_english_verify_block_is_what_ux_stats_prints():
    section = dict(_sections(EN))["### Verify install"]
    block = FENCE.search(section).group(0)
    printed = "\n".join(line[2:] for line in block.split("\n") if line.startswith("# "))
    assert json.loads(printed) == {"version": __version__, "counts": COUNTS}
    assert f"{ENTRIES:,} entries" in section


def test_english_names_every_mcp_tool_and_the_count():
    section = dict(_sections(EN))["## MCP server: the asymmetric move"]
    assert f"{len(TOOLS)} tools: " in section
    assert set(re.findall(r"`(ux_[a-z_]+)`", section)) == set(TOOL_NAMES)
    assert f"{len(TOOLS)} MCP tools" in EN
    assert not re.search(r"\b(Eighteen|Fourteen)\b", EN)


def test_english_states_the_current_version_and_counts():
    assert f"badge/version-{_badge(__version__)}-" in EN
    assert f"**v{__version__}**" in EN
    assert "-stable" not in EN
    assert f"{len(CANONICAL)} slash commands" in EN
    assert f"| Slash commands | **{len(CANONICAL)}** |" in EN
    assert f"| Anti-pattern rules | **{len(RULES)}** |" in EN


def test_the_catalogue_lives_in_the_english_readme_only():
    assert START in ENGLISH and END in ENGLISH
    assert slug(CATALOGUE) == "rules-by-category"


# Each locale against the English README.

@pytest.mark.parametrize("loc", LOCALES)
def test_the_language_switcher_links_every_readme(loc):
    first = _locale(loc).split("\n", 1)[0]
    others = {"README.md"} | {f"README.{x}.md" for x in LOCALES if x != loc}
    assert set(re.findall(r"\]\((README[^)]*\.md)\)", first)) == others
    assert f"README.{loc}.md" not in first


@pytest.mark.parametrize("loc", LOCALES)
def test_same_sections_in_the_same_order(loc):
    en, lo = _headings(EN), _headings(_locale(loc))
    assert [h.split(" ")[0] for h in lo] == [h.split(" ")[0] for h in en]
    for e, l in zip(en, lo):
        assert re.findall(r"`[^`]+`", l) == re.findall(r"`[^`]+`", e), (e, l)


@pytest.mark.parametrize("loc", LOCALES)
def test_every_internal_link_lands_on_a_heading(loc):
    text = _locale(loc)
    anchors = {slug(h) for h in _headings(text)}
    broken = sorted(set(re.findall(r"\]\(#([^)\s]+)\)", text)) - anchors)
    assert not broken, f"README.{loc}.md links to {broken}"


@pytest.mark.parametrize("loc", LOCALES)
def test_same_code_blocks_as_english(loc):
    assert FENCE.findall(_locale(loc)) == FENCE.findall(EN)


@pytest.mark.parametrize("loc", LOCALES)
def test_same_links_as_english(loc):
    extra = {"README.md#rules-by-category"}
    assert _links(_locale(loc)) - extra == _links(EN)


@pytest.mark.parametrize("loc", LOCALES)
def test_same_figures_and_inline_code_section_by_section(loc):
    drift = []
    for (eh, eb), (lh, lb) in _paired(loc):
        if eh == CATALOGUE:
            continue
        en, lo = eh + "\n" + eb, lh + "\n" + lb
        for count in (_numbers, _spans):
            extra, missing = count(lo) - count(en), count(en) - count(lo)
            if extra or missing:
                drift.append(f"{eh}: extra {dict(extra)}, missing {dict(missing)}")
    assert not drift, f"README.{loc}.md differs from English in:\n" + "\n".join(drift)


@pytest.mark.parametrize("loc", LOCALES)
def test_states_version_4_and_the_engine_figures(loc):
    text = _locale(loc)
    assert f"badge/version-{_badge(__version__)}-" in text
    assert f"**v{__version__}**" in text
    assert f"badge/anti--patterns-{len(RULES)}-" in text
    head = _paired(loc)[0][1]
    figures = _numbers(head[0] + "\n" + head[1])
    for n in (len(RULES), len(TOOLS), len(CANONICAL), COUNTS["brands"], COUNTS["components"]):
        assert figures[str(n)], (loc, n)
    assert _numbers(_section(loc, "### Verify install"))[str(ENTRIES)]
    mcp = _section(loc, "## MCP server: the asymmetric move")
    assert set(re.findall(r"`(ux_[a-z_]+)`", mcp)) == set(TOOL_NAMES)
    assert _numbers(mcp)[str(len(TOOLS))]


@pytest.mark.parametrize("loc", LOCALES)
def test_states_the_install_commands(loc):
    text = _locale(loc)
    for command in ("pip install --upgrade uxskill", "pip install --upgrade 'uxskill[mcp]'",
                    "pip install uxskill", "npx uxskill@latest"):
        assert command in text, (loc, command)


@pytest.mark.parametrize("loc", LOCALES)
def test_documents_the_18_commands_and_the_aliases(loc):
    pairs = _paired(loc)
    heads = [eh for (eh, _), _ in pairs]
    first = heads.index(f"## The {len(CANONICAL)} slash commands: detailed reference")
    last = heads.index("### Aliases, removed in 4.1")
    documented = [m for (_, _), (lh, _) in pairs[first:last]
                  for m in re.findall(r"^#### `/(ux-[a-z0-9-]+)`", lh)]
    assert sorted(documented) == sorted(CANONICAL)
    table = pairs[last][1][1]
    assert set(re.findall(r"^\| `/(ux-[a-z0-9-]+)` \|", table, re.MULTILINE)) == ALIASES


@pytest.mark.parametrize("loc", LOCALES)
def test_links_to_the_rule_catalogue_and_states_its_coverage(loc):
    import importlib.util
    spec = importlib.util.spec_from_file_location("readme_rules",
                                                  ROOT / "scripts" / "readme_rules.py")
    readme_rules = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(readme_rules)
    text = _locale(loc)
    assert START not in text and END not in text
    section = _section(loc, CATALOGUE)
    assert "(README.md#rules-by-category)" in section
    assert readme_rules.coverage(RULES) in section
    assert _numbers(section)[str(len(RULES))]


@pytest.mark.parametrize("loc", LOCALES)
def test_no_figure_from_an_earlier_release(loc):
    text = _locale(loc)
    current = _current(loc)
    assert "-stable" not in text
    assert not re.search(r"badge/version-3", text)
    assert not re.search(r"badge/anti--patterns-(145|152)-", text)
    assert not re.search(r"(?<![0-9.])(145|152)(?![0-9])", _prose(current)), loc
    assert re.findall(r"badge/tests-(\d+)_passing", text) == \
        re.findall(r"badge/tests-(\d+)_passing", EN)


def test_the_badge_writes_a_prerelease_as_shields_reads_it():
    assert _badge("4.0.0") == "4.0.0"
    assert _badge("4.0.0b2") == "4.0.0--beta.2"
    assert _badge("4.1.0rc1") == "4.1.0--rc.1"
