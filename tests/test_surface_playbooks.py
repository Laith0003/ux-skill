"""Guards for the surface playbooks in references/surfaces/.

Surface-specific rules live in exactly one playbook. These tests fail when:
1. a rule sentence appears, exactly or nearly, both in a playbook and in a file
   it was moved out of, in commands/ux-design.md, or in two playbooks at once;
2. a file path pointer in commands/, agents/ or references/ names a file that
   does not exist;
3. an old source file stops pointing at its playbook;
4. /ux-design stops choosing exactly one playbook.
"""
import difflib
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SURFACES = REPO / "references" / "surfaces"

# Each playbook and the files its rules were moved out of, or that sit next to
# it on the same subject and must not restate its rules.
SOURCES = {
    "landing.md": [
        "references/styles/anti-slop.md",
        "references/styles/arsenal.md",
        "references/styles/exemplars.md",
        "references/process/discovery-protocol.md",
        "references/foundations/component-behaviors.md",
        "references/foundations/layout.md",
        "references/components/library.md",
    ],
    "dashboard.md": [
        "references/foundations/dashboards.md",
        "references/foundations/components.md",
        "references/styles/arsenal.md",
        "references/styles/anti-slop.md",
    ],
    "component.md": [
        "references/foundations/component-behaviors.md",
        "references/components/library.md",
        "references/components/heroui.md",
    ],
}

# Neighbours on the same subject that need no pointer to the playbook.
NO_POINTER_REQUIRED = {
    "references/components/heroui.md",
    "references/foundations/components.md",
}

# Command files that load the playbooks and must not restate their rules.
COMMANDS = ["commands/ux-design.md"]

# The old file that is now a pure pointer.
POINTER_FILES = {
    "references/foundations/dashboards.md": ["references/surfaces/dashboard.md"],
}

# Bare file names that name files in the user's project, not in this repo.
PROJECT_FILES = {
    "brand.md", "DESIGN.md", "MASTER.md", "GEMINI.md", "AGENTS.md", "CLAUDE.md",
    "system-report.md", "project_dot_voice.md",
}
_PROJECT_FILE_PATTERN = re.compile(r"^\d\d-[\w-]+\.md$")

NEAR_RATIO = 0.9
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


def near_duplicates(left, right, ratio=NEAR_RATIO):
    """Pairs of sentences from two sets that match exactly or at `ratio` or higher."""
    found = sorted((a, a) for a in left & right)
    rest_right = sorted(right - left)
    for a in sorted(left - right):
        for b in rest_right:
            la, lb = len(a), len(b)
            if 2 * min(la, lb) / (la + lb) < ratio:
                continue
            m = difflib.SequenceMatcher(None, a, b, autojunk=False)
            if m.real_quick_ratio() >= ratio and m.quick_ratio() >= ratio and m.ratio() >= ratio:
                found.append((a, b))
    return found


def _report(pairs):
    return [a if a == b else f"{a}  ~  {b}" for a, b in pairs]


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


def test_detector_catches_a_near_duplicate():
    """Prove the near-duplicate control can fail, and that it leaves distinct rules alone."""
    a = rule_sentences("Arabic is a connected script; any tracking breaks the joins between letters.")
    b = rule_sentences("Arabic is a connected script, and any tracking breaks the joins between letters.")
    assert near_duplicates(a, b)
    c = rule_sentences("Tables collapse to stacked cards below the tablet breakpoint.")
    assert not near_duplicates(a, c)


@pytest.mark.parametrize("playbook", sorted(SOURCES))
def test_no_rule_sentence_in_playbook_and_old_source(playbook):
    moved = rule_sentences(_read(f"references/surfaces/{playbook}"))
    problems = []
    for source in SOURCES[playbook]:
        pairs = near_duplicates(moved, rule_sentences(_read(source)))
        problems += [f"{source}: {s}" for s in _report(pairs)]
    assert not problems, (
        f"rule sentences in both references/surfaces/{playbook} and an old source "
        f"(keep each rule in one place):\n" + "\n".join(problems)
    )


@pytest.mark.parametrize("command", COMMANDS)
@pytest.mark.parametrize("playbook", sorted(SOURCES))
def test_no_playbook_rule_restated_in_a_command(command, playbook):
    moved = rule_sentences(_read(f"references/surfaces/{playbook}"))
    pairs = near_duplicates(moved, rule_sentences(_read(command)))
    assert not pairs, (
        f"{command} restates rules from references/surfaces/{playbook}; point at the playbook instead:\n"
        + "\n".join(_report(pairs))
    )


def test_no_rule_sentence_in_two_playbooks():
    names = sorted(SOURCES)
    sets = {n: rule_sentences(_read(f"references/surfaces/{n}")) for n in names}
    problems = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            problems += [f"{a} + {b}: {s}" for s in _report(near_duplicates(sets[a], sets[b]))]
    assert not problems, "rule sentences duplicated across playbooks:\n" + "\n".join(problems)


def _by_name():
    index = {}
    for p in (REPO / "references").rglob("*.md"):
        index.setdefault(p.name, []).append(p)
    return index


def _resolve(path, ref, index):
    """Resolve one pointer. Returns a Path, or None when the pointer names a user project file."""
    if ref.startswith("references/"):
        return REPO / ref
    if ref.startswith("../") or ref.startswith("./"):
        return (path.parent / ref).resolve()
    if "/" in ref:
        # `surfaces/x.md`, `foundations/x.md` and similar name a file under
        # references/; `commands/x.md` and similar name one at the repo root.
        # A first folder that exists in neither place (`.ux/`, `rule-pack/`)
        # is a path in the user's project.
        first = ref.split("/", 1)[0]
        bases = [b for b in (REPO / "references", REPO) if not first.startswith(".") and (b / first).is_dir()]
        if not bases:
            return None
        for base in bases:
            if (base / ref).exists():
                return base / ref
        return bases[0] / ref
    local = path.parent / ref
    if local.exists():
        return local
    if ref in PROJECT_FILES or _PROJECT_FILE_PATTERN.match(ref):
        return None
    matches = index.get(ref, [])
    return matches[0] if len(matches) == 1 else local


def _pointer_targets(path, index):
    """Yield (line_no, pointer, resolved Path) for every file pointer in a markdown file.

    A pointer is a `code` or **bold** file name, or a bare references/ path. A bare
    name resolves next to the file first, then to the one file of that name under
    references/.
    """
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "if present" in line:
            continue
        for match in re.finditer(r"`([^`]+\.md)`|\*\*([\w./-]+\.md)\*\*|(references/[\w./-]+\.md)", line):
            ref = (match.group(1) or match.group(2) or match.group(3)).strip()
            if "<" in ref or "*" in ref or " " in ref:
                continue
            target = _resolve(path, ref, index)
            if target is not None:
                yield n, ref, target


def _markdown_files():
    for top in ("commands", "agents", "references"):
        for p in sorted((REPO / top).rglob("*.md")):
            if "brands" in p.relative_to(REPO).parts:
                continue
            yield p


def test_pointer_check_catches_a_bad_bare_name(tmp_path):
    """Prove the pointer control can fail on the bare forms the See-also lists use."""
    folder = tmp_path / "references" / "styles"
    folder.mkdir(parents=True)
    doc = folder / "doc.md"
    doc.write_text("See `anti-slopp.md` and **nowhere.md**.\n", encoding="utf-8")
    targets = [(ref, t.exists()) for _, ref, t in _pointer_targets(doc, _by_name())]
    assert ("anti-slopp.md", False) in targets
    assert ("nowhere.md", False) in targets


def test_pointer_check_catches_a_bad_folder_path(tmp_path):
    """Prove the pointer control fails on `surfaces/nope.md` and passes the real folder forms."""
    doc = tmp_path / "doc.md"
    doc.write_text(
        "See `surfaces/nope.md`, `surfaces/landing.md`, `foundations/layout.md` and `commands/ux-design.md`.\n",
        encoding="utf-8",
    )
    targets = dict((ref, t.exists()) for _, ref, t in _pointer_targets(doc, _by_name()))
    assert targets == {
        "surfaces/nope.md": False,
        "surfaces/landing.md": True,
        "foundations/layout.md": True,
        "commands/ux-design.md": True,
    }


def test_every_pointer_resolves():
    index = _by_name()
    broken = []
    for path in _markdown_files():
        for n, ref, target in _pointer_targets(path, index):
            if not target.exists():
                broken.append(f"{path.relative_to(REPO)}:{n} points at {ref}, which does not exist")
    assert not broken, "\n".join(broken)


@pytest.mark.parametrize("playbook", sorted(SOURCES))
def test_old_sources_point_at_their_playbook(playbook):
    target = f"references/surfaces/{playbook}"
    missing = [s for s in SOURCES[playbook] if s not in NO_POINTER_REQUIRED and target not in _read(s)]
    assert not missing, f"these files lost their pointer to {target}: {missing}"


@pytest.mark.parametrize("rel", sorted(POINTER_FILES))
def test_old_files_are_pointers(rel):
    text = _read(rel)
    for target in POINTER_FILES[rel]:
        assert target in text, f"{rel} must point at {target}"
    assert len(rule_sentences(text)) <= 3, f"{rel} must stay a pointer, not a second copy of the rules"


def test_component_contracts_stay_outside_the_playbooks():
    """The one-playbook rule covers surface playbooks only; the component contracts load on any build."""
    text = _read("references/foundations/component-behaviors.md")
    for heading in ("## Card grid", "## Form", "## Data table", "## Modal, sheet and drawer"):
        assert heading in text, f"component-behaviors.md lost its {heading!r} contract"
    for target in ("references/surfaces/component.md", "references/surfaces/landing.md"):
        assert target in text, f"component-behaviors.md must point at {target}"


def test_ux_design_loads_exactly_one_playbook():
    text = _read("commands/ux-design.md")
    for name in SOURCES:
        assert f"references/surfaces/{name}" in text, f"/ux-design must offer references/surfaces/{name}"
    assert "pick exactly one" in text.lower()
    assert "Load only the playbook you picked" in text
    assert "applies to surface playbooks only" in text
    assert "references/foundations/component-behaviors.md" in text, "/ux-design must still load the component contracts"


def test_every_mode_records_its_surface():
    text = _read("commands/ux-design.md")
    for value in ('"surface": "component"', '"surface": "dashboard"', '"surface": "<landing|none>"'):
        assert value in text, f"/ux-design state files must record {value}"
