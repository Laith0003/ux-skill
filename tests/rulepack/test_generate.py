"""The rule pack: fixed files and headings per foundation, every role,
check and pairing from the build, links that resolve inside the pack, no
dashes, and the same bytes for the same system."""
import posixpath
import re
import shutil

import pytest

from engine.contracts.library import SEED_DIR
from engine.foundations import FOUNDATIONS, build_system
from engine.rulepack.generate import (
    ARCHITECTURE_HEADINGS, AUDIT_HEADINGS, COLOR_REFERENCE_HEADINGS, FILES, HANDOFF_HEADINGS,
    PACK, README_HEADINGS, REFERENCE_HEADINGS, RulePackError, build_rule_pack)
from engine.rulepack.guidance import GUIDANCE_DIR, role_catalog
from engine.rulepack.records import RECORDS_DIR
from engine.synthesizer.axes import AxisValues
from tests.foundations.test_no_licensed_text import PRIVATE, shingles

AXES = AxisValues(*[0.5] * 7)
TS = build_system(AXES, "#3366FF").tokens
PACK_FILES = build_rule_pack(TS)
NAMES = [f.name for f in FOUNDATIONS]


def _h2(text):
    return [line[3:] for line in text.split("\n") if line.startswith("## ")]


def test_the_pack_holds_a_router_four_files_per_foundation_and_the_sources():
    expected = [f"{PACK}/README.md"]
    expected += [f"{PACK}/{n}/{f}" for n in NAMES for f in FILES]
    expected += [f"{PACK}/content.md", f"{PACK}/direction.md"]
    expected += [f"{PACK}/contracts/{p.name}" for p in sorted(SEED_DIR.glob("*.yaml"))]
    expected += [f"{PACK}/decisions/{p.name}" for p in sorted(RECORDS_DIR.glob("*.md"))]
    assert list(PACK_FILES) == expected


def test_every_file_has_its_fixed_headings():
    assert _h2(PACK_FILES[f"{PACK}/README.md"]) == list(README_HEADINGS)
    for n in NAMES:
        assert _h2(PACK_FILES[f"{PACK}/{n}/architecture.md"]) == list(ARCHITECTURE_HEADINGS), n
        want = COLOR_REFERENCE_HEADINGS if n == "color" else REFERENCE_HEADINGS
        assert _h2(PACK_FILES[f"{PACK}/{n}/reference.md"]) == list(want), n
        assert _h2(PACK_FILES[f"{PACK}/{n}/audit.md"]) == list(AUDIT_HEADINGS), n
        assert _h2(PACK_FILES[f"{PACK}/{n}/handoff.md"]) == list(HANDOFF_HEADINGS), n


def test_every_role_check_and_pairing_of_the_build_is_in_the_pack():
    for entry in role_catalog(TS):
        for name in ("architecture.md", "reference.md", "handoff.md"):
            assert f"`{entry.path}`" in PACK_FILES[f"{PACK}/{entry.foundation}/{name}"], entry.path
    for f in FOUNDATIONS:
        audit = PACK_FILES[f"{PACK}/{f.name}/audit.md"]
        for c in f.checks:
            assert f"| `{c.id}` |" in audit, c.id
        for p in f.pairings:
            assert f"| `{p.fg}` | `{p.bg}` |" in PACK_FILES[f"{PACK}/color/reference.md"]


def test_values_come_from_the_build():
    reference = PACK_FILES[f"{PACK}/space/reference.md"]
    value = TS.resolve("space.control.gap")
    assert f"| `space.control.gap` | dimension | `{TS.raw('space.control.gap')[1:-1]}` | " \
           f"{value['value']}px |" in reference
    color = PACK_FILES[f"{PACK}/color/reference.md"]
    assert TS.resolve("color.action.primary", "scheme:dark,contrast:high") in color


def test_links_and_citations_resolve_inside_the_pack():
    for path, text in PACK_FILES.items():
        for link in re.findall(r"\]\(([^)#]+)\)", text):
            target = posixpath.normpath(posixpath.join(posixpath.dirname(path), link))
            assert target in PACK_FILES, (path, link)
        for cited in re.findall(r"(?<![./\w])decisions/([a-z0-9-]+)\.md", text):
            assert f"{PACK}/decisions/{cited}.md" in PACK_FILES, (path, cited)


def test_the_pack_is_plain_ascii_with_no_dashes():
    for path, text in PACK_FILES.items():
        assert text.isascii(), path
        assert not re.search(r"\s--\s", text), path


def test_the_same_system_gives_the_same_pack():
    assert build_rule_pack(build_system(AXES, "#3366FF").tokens) == PACK_FILES


def test_a_latin_only_system_gets_a_pack_too():
    files = build_rule_pack(build_system(AXES, "#3366FF", arabic=False).tokens)
    assert list(files) == list(PACK_FILES)
    assert "type.face.arabic" not in files[f"{PACK}/type/reference.md"]


def test_a_gap_between_guidance_and_build_stops_the_pack(tmp_path):
    guidance = tmp_path / "guidance"
    shutil.copytree(GUIDANCE_DIR, guidance)
    text = (guidance / "radius.md").read_text(encoding="utf-8")
    (guidance / "radius.md").write_text(
        text.replace("- `radius.pill`: fully rounded shapes, such as a pill button or an avatar "
                     "frame; the final shape follows the element's proportions.\n", ""),
        encoding="utf-8")
    with pytest.raises(RulePackError) as err:
        build_rule_pack(TS, guidance_dir=guidance)
    assert err.value.problems == (
        "radius.md: radius.pill has no description under Roles; add \"- `radius.pill`: what it "
        "is for\"",)


def test_a_contract_that_does_not_bind_stops_the_pack(tmp_path):
    contracts = tmp_path / "contracts"
    shutil.copytree(SEED_DIR, contracts)
    text = (contracts / "card.yaml").read_text(encoding="utf-8")
    (contracts / "card.yaml").write_text(
        text.replace("  - {part: container, property: border-width, role: border.outline}\n",
                     ""), encoding="utf-8")
    with pytest.raises(RulePackError) as err:
        build_rule_pack(TS, contracts_dir=contracts)
    assert [p.split(" is ")[0] for p in err.value.problems] == [
        "card: container.fill (level=standard)", "card: container.fill (level=lifted)"]


@pytest.mark.skipif(not PRIVATE.exists(), reason="private source not on this machine")
def test_the_generated_pack_repeats_no_licensed_phrasing():
    licensed = set()
    for md in PRIVATE.glob("*/*.md"):
        licensed |= shingles(md.read_text(encoding="utf-8", errors="ignore"))
    hits = {path: sorted(shingles(text) & licensed)[:1] for path, text in PACK_FILES.items()}
    assert {p: h for p, h in hits.items() if h} == {}


# The pack states no fact of its own about contracts and pairings: every
# row and line below is computed here from the build and the contracts,
# and a change to a contract shows up in the pack.
from engine.contracts.library import load_folder  # noqa: E402
from engine.foundations.gate import HIGH_FLOOR, required  # noqa: E402
from engine.foundations.export import to_css  # noqa: E402
from engine.rulepack.generate import (  # noqa: E402
    PRECEDENCE_OPENINGS, contract_pairing_rows, overlaps, precedence_lines, state_pairs)

CONTRACTS = load_folder(SEED_DIR)


def _rows(text, heading_line):
    """The table rows under the line that introduces them."""
    lines = text.split("\n")
    at = lines.index(heading_line)
    start = next(i for i in range(at + 1, len(lines)) if lines[i].startswith("|")) + 2
    out = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        out.append(line)
    return out


def _high(p):
    high, criterion = required(p, "contrast:high", TS.axes)
    if p.high is not None:
        return f"{high:g}:1 (pinned)"
    if criterion.startswith(HIGH_FLOOR):
        return f"{high:g}:1 (our floor)"
    return f"{high:g}:1 (WCAG {criterion}{', AAA' if criterion == '1.4.6' else ''})"


def test_pairing_rows_are_the_build_and_the_contracts_and_nothing_else():
    reference = PACK_FILES[f"{PACK}/color/reference.md"]
    color = next(f for f in FOUNDATIONS if f.name == "color")
    assert _rows(reference, "## Pairings") == [
        f"| `{p.fg}` | `{p.bg}` | {p.minimum:g}:1 | {_high(p)} | WCAG {p.criterion} |"
        for p in color.pairings]
    intro = next(line for line in reference.split("\n")
                 if line.startswith("Contracts add these pairings"))
    want = []
    for name, p in contract_pairing_rows(CONTRACTS):
        source = "our floor" if p.criterion.startswith("the ") else f"WCAG {p.criterion}"
        want.append(f"| {name} | `{p.fg}` | `{p.bg}` | {p.minimum:g}:1 | {_high(p)} | {source} |")
    assert _rows(reference, intro) == want
    assert len(want) == len(set(want))
    # A floor of our own is never attributed to WCAG, and a pinned minimum
    # is marked as pinned.
    assert "| button | `color.text.disabled` | `color.action.disabled` | 1.3:1 | 1.3:1 (pinned) " \
           "| our floor |" in want


def test_a_new_contract_pairing_or_description_shows_up_in_the_pack(tmp_path):
    contracts = tmp_path / "contracts"
    shutil.copytree(SEED_DIR, contracts)
    card = contracts / "card.yaml"
    text = card.read_text(encoding="utf-8")
    text = text.replace(
        "contrast:\n",
        "contrast:\n  - {fg: color.text.default, bg: color.surface.page, minimum: 4.5, "
        "criterion: \"1.4.3\"}\n")
    text = text.replace("Groups related content into one bounded block",
                        "Holds related content in one bounded block")
    card.write_text(text, encoding="utf-8")
    files = build_rule_pack(TS, contracts_dir=contracts)
    row = "| card | `color.text.default` | `color.surface.page` | 4.5:1 | 7:1 (WCAG 1.4.6, AAA) | " \
          "WCAG 1.4.3 |"
    assert row in files[f"{PACK}/color/reference.md"]
    assert row not in PACK_FILES[f"{PACK}/color/reference.md"]
    assert "Holds related content in one bounded block" in files[f"{PACK}/README.md"]


def test_contract_lines_come_from_the_contracts():
    readme = PACK_FILES[f"{PACK}/README.md"]
    for c in CONTRACTS:
        assert f"- [{c.name}](contracts/{c.name}.yaml) ({c.status}): {c.description}" in readme
    for f in FOUNDATIONS:
        arch = PACK_FILES[f"{PACK}/{f.name}/architecture.md"]
        section = arch.split("## Contracts\n", 1)[1]
        bound = [(c, [r for r in c.roles() if r.startswith(f.name + ".")]) for c in CONTRACTS]
        want = [f"- [{c.name}](../contracts/{c.name}.yaml) ({c.status}): binds "
                + ", ".join(f"`{r}`" for r in roles) + "." for c, roles in bound if roles]
        assert [line for line in section.split("\n") if line.startswith("- ")] == \
            (want or ["- No contract binds these roles yet."]), f.name


def test_the_precedence_lines_are_the_contracts_own_and_every_overlap_has_them():
    readme = PACK_FILES[f"{PACK}/README.md"]
    ruled = [c for c in CONTRACTS if any(overlaps(c))]
    assert [c.name for c in ruled] == ["button", "selectable-row", "text-field"]
    for c in ruled:
        lines = precedence_lines(c)
        for need, opening in zip(overlaps(c), PRECEDENCE_OPENINGS):
            assert not need or any(line.startswith(opening) for line in lines), (c.name, opening)
        assert all(line in c.do for line in lines)
        pairs = "; ".join(f"{a} and {b}" for a, b in state_pairs(c))
        head = f"- {c.name} (states that meet: {pairs}):" if pairs else f"- {c.name}:"
        assert "\n".join([head] + [f"  - {line}" for line in lines]) in readme
    listed = readme.split("are listed with it.")[1].split("## Rules")[0]
    for c in CONTRACTS:
        if not any(overlaps(c)):
            assert f"- {c.name}" not in listed


def test_the_states_that_meet_come_from_the_bindings(tmp_path):
    by_name = {c.name: c for c in CONTRACTS}
    assert state_pairs(by_name["button"]) == [
        ("hover", "pressed"), ("hover", "disabled"), ("pressed", "disabled")]
    assert state_pairs(by_name["text-field"]) == [("disabled", "error")]
    # Two states that bind the same role never meet: the row's hover and
    # pressed both take color.surface.sunken.
    assert ("hover", "pressed") not in state_pairs(by_name["selectable-row"])
    contracts = tmp_path / "contracts"
    shutil.copytree(SEED_DIR, contracts)
    field = contracts / "text-field.yaml"
    text = field.read_text(encoding="utf-8")
    assert "role: color.status.danger.strong, state: error}" in text
    field.write_text(text.replace("role: color.line.subtle, state: disabled}",
                                  "role: color.status.danger.strong, state: disabled}"),
                     encoding="utf-8")
    changed = {c.name: c for c in load_folder(contracts)}["text-field"]
    assert state_pairs(changed) == []


def test_a_contract_with_overlapping_bindings_and_no_precedence_stops_the_pack(tmp_path):
    contracts = tmp_path / "contracts"
    shutil.copytree(SEED_DIR, contracts)
    field = contracts / "text-field.yaml"
    text = field.read_text(encoding="utf-8")
    kept = [line for line in text.split("\n") if not line.strip().startswith(
        ("- Apply the binding for a state", "- When two states apply at once"))]
    field.write_text("\n".join(kept), encoding="utf-8")
    with pytest.raises(RulePackError) as err:
        build_rule_pack(TS, contracts_dir=contracts)
    assert err.value.problems == tuple(
        "text-field: two of its bindings for one part and property can apply at once, and "
        f"usage.do does not say which wins; add a line that starts \"{o}\""
        for o in PRECEDENCE_OPENINGS)


def test_the_mode_lines_are_the_selectors_tokens_css_writes():
    css = to_css(TS)
    handoff = PACK_FILES[f"{PACK}/color/handoff.md"]
    assert "- scheme (light, dark): data-theme=\"dark\" on the html element, or the media " \
           "query (prefers-color-scheme: dark) unless data-theme=\"light\" is set" in handoff
    assert ':root[data-theme="dark"]' in css
    assert "@media (prefers-color-scheme: dark)" in css
    assert ':root:not([data-theme="light"])' in css
    assert "- direction (ltr, rtl): dir=\"rtl\" on the html element" in \
        PACK_FILES[f"{PACK}/type/handoff.md"]
    assert ':root[dir="rtl"]' in css


def test_checks_citing_aaa_block_and_so_do_our_floors():
    layout = PACK_FILES[f"{PACK}/layout/audit.md"]
    assert "| `target-size-comfortable` | WCAG 2.5.5 (AAA) |" in layout
    assert "decisions/aaa-criteria-that-block.md" in layout
    assert "decisions/aaa-criteria-that-block.md" not in PACK_FILES[f"{PACK}/radius/audit.md"]
    for f in FOUNDATIONS:
        audit = PACK_FILES[f"{PACK}/{f.name}/audit.md"]
        assert "| blocking | fails WCAG at level A or AA; or fails a check the gate runs or a " \
               "contract pairing, AAA criteria and our floors included |" in audit
        assert "misses an AAA criterion the system does not apply |" in audit


def test_the_pack_is_the_same_under_every_hash_seed():
    import hashlib
    import os
    import subprocess
    import sys
    script = ("import hashlib\n"
              "from engine.foundations import build_system\n"
              "from engine.synthesizer.axes import AxisValues\n"
              "from engine.rulepack.generate import build_rule_pack\n"
              "files = build_rule_pack(build_system(AxisValues(*[0.5] * 7), '#3366FF').tokens)\n"
              "h = hashlib.sha256()\n"
              "for k, v in files.items():\n"
              "    h.update(k.encode() + b'\\0' + v.encode() + b'\\0')\n"
              "print(h.hexdigest())\n")
    here = hashlib.sha256()
    for k, v in PACK_FILES.items():
        here.update(k.encode() + b"\0" + v.encode() + b"\0")
    for seed in ("0", "1", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        out = subprocess.run([sys.executable, "-c", script], env=env, check=True,
                             capture_output=True, text=True).stdout.strip()
        assert out == here.hexdigest(), seed
