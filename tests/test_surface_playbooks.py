"""Guards for the surface playbooks in references/surfaces/.

Surface-specific rules live in exactly one playbook. These tests fail when:
1. a rule sentence appears both in a playbook and in a file it was moved out of,
   or in two playbooks at once;
2. a file path pointer in commands/, agents/ or references/ names a file that
   does not exist;
3. an old source file stops pointing at its playbook;
4. /ux-design stops choosing exactly one playbook.
"""
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SURFACES = REPO / "references" / "surfaces"

# Each playbook and the files its rules were moved out of.
SOURCES = {
    "landing.md": [
        "references/styles/anti-slop.md",
        "references/styles/arsenal.md",
        "references/process/discovery-protocol.md",
        "references/foundations/component-behaviors.md",
        "references/components/library.md",
    ],
    "dashboard.md": [
        "references/foundations/dashboards.md",
        "references/styles/arsenal.md",
        "references/styles/anti-slop.md",
    ],
    "component.md": [
        "references/foundations/component-behaviors.md",
        "references/components/library.md",
        "references/components/heroui.md",
    ],
}

# The two old files that are now pure pointers.
POINTER_FILES = {
    "references/foundations/dashboards.md": ["references/surfaces/dashboard.md"],
    "references/foundations/component-behaviors.md": [
        "references/surfaces/component.md",
        "references/surfaces/landing.md",
    ],
}

MIN_WORDS = 6
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_MARKUP = re.compile(r"[*`_>#]|\[ \]|\[x\]")
_LIST_MARK = re.compile(r"^\s*(?:[-+]|\d+\.)\s+")
_NON_WORD = re.compile(r"[^a-z0-9%$.+/ ]+")


def _normalize(fragment):
    text = _MARKUP.sub(" ", fragment.lower())
    text = _NON_WORD.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text


def rule_sentences(markdown):
    """Every sentence-sized rule in a markdown document, normalized.

    Table rows are split into cells, list markers and emphasis are dropped,
    and prose is split at sentence ends. Fragments under MIN_WORDS words are
    ignored so shared labels ("Cost: zero") do not count as duplicated rules.
    """
    out = set()
    in_code = False
    for raw in markdown.splitlines():
        if raw.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        line = _MARKUP.sub(" ", _LIST_MARK.sub("", raw))
        pieces = line.split("|") if line.strip().startswith("|") else [line]
        for piece in pieces:
            for sentence in _SENTENCE_END.split(piece):
                norm = _normalize(sentence)
                if len(norm.split()) >= MIN_WORDS:
                    out.add(norm)
    return out


def _read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def test_playbooks_exist():
    for name in SOURCES:
        assert (SURFACES / name).is_file(), f"missing playbook references/surfaces/{name}"


def test_detector_catches_a_duplicate():
    """Prove the control can fail: a shared rule sentence is reported."""
    a = "| Don't | Do |\n|---|---|\n| Customer logos in full color | Single mono treatment for every logo on the page |"
    b = "- **Logos.** Single mono treatment for every logo on the page. Keep them quiet."
    assert rule_sentences(a) & rule_sentences(b) == {"single mono treatment for every logo on the page"}
    assert not (rule_sentences("Short label.") & rule_sentences("Short label."))


@pytest.mark.parametrize("playbook", sorted(SOURCES))
def test_no_rule_sentence_in_playbook_and_old_source(playbook):
    moved = rule_sentences(_read(f"references/surfaces/{playbook}"))
    problems = []
    for source in SOURCES[playbook]:
        shared = moved & rule_sentences(_read(source))
        problems += [f"{source}: {s}" for s in sorted(shared)]
    assert not problems, (
        f"rule sentences in both references/surfaces/{playbook} and an old source "
        f"(keep each rule in one place):\n" + "\n".join(problems)
    )


def test_no_rule_sentence_in_two_playbooks():
    names = sorted(SOURCES)
    sets = {n: rule_sentences(_read(f"references/surfaces/{n}")) for n in names}
    problems = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            problems += [f"{a} + {b}: {s}" for s in sorted(sets[a] & sets[b])]
    assert not problems, "rule sentences duplicated across playbooks:\n" + "\n".join(problems)


def _pointer_targets(path):
    """Yield (line_no, pointer, resolved Path) for every file pointer in a markdown file."""
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "if present" in line:
            continue
        for match in re.finditer(r"`([^`]+\.md)`|(references/[\w./-]+\.md)", line):
            ref = (match.group(1) or match.group(2)).strip()
            if "<" in ref or "*" in ref or " " in ref:
                continue
            if ref.startswith("references/"):
                yield n, ref, REPO / ref
            elif ref.startswith("../"):
                yield n, ref, (path.parent / ref).resolve()


def _markdown_files():
    for top in ("commands", "agents", "references"):
        for p in sorted((REPO / top).rglob("*.md")):
            if "brands" in p.relative_to(REPO).parts:
                continue
            yield p


def test_every_pointer_resolves():
    broken = []
    for path in _markdown_files():
        for n, ref, target in _pointer_targets(path):
            if not target.exists():
                broken.append(f"{path.relative_to(REPO)}:{n} points at {ref}, which does not exist")
    assert not broken, "\n".join(broken)


@pytest.mark.parametrize("playbook", sorted(SOURCES))
def test_old_sources_point_at_their_playbook(playbook):
    target = f"references/surfaces/{playbook}"
    missing = [s for s in SOURCES[playbook] if s != "references/components/heroui.md" and target not in _read(s)]
    assert not missing, f"these files lost their pointer to {target}: {missing}"


@pytest.mark.parametrize("rel", sorted(POINTER_FILES))
def test_old_files_are_pointers(rel):
    text = _read(rel)
    for target in POINTER_FILES[rel]:
        assert target in text, f"{rel} must point at {target}"
    assert len(rule_sentences(text)) <= 3, f"{rel} must stay a pointer, not a second copy of the rules"


def test_ux_design_loads_exactly_one_playbook():
    text = _read("commands/ux-design.md")
    for name in SOURCES:
        assert f"references/surfaces/{name}" in text, f"/ux-design must offer references/surfaces/{name}"
    assert "pick exactly one" in text.lower()
    assert "Load only the playbook you picked" in text
    assert "component-behaviors.md" not in text, "/ux-design must not load the old component-behaviors file"
