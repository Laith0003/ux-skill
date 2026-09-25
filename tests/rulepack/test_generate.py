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
    expected += [f"{PACK}/built-from.json"]
    assert list(PACK_FILES) == expected


def test_the_pack_records_the_digest_of_the_tokens_it_was_built_from():
    import hashlib
    import json
    from engine.foundations import dump_dtcg
    manifest = json.loads(PACK_FILES[f"{PACK}/built-from.json"])
    assert manifest == {"tokens.json": {
        "sha256": hashlib.sha256(dump_dtcg(TS).encode("utf-8")).hexdigest()}}
    assert "built-from.json" in PACK_FILES[f"{PACK}/README.md"]


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
    arabic_ok = (f"{PACK}/content.md", f"{PACK}/direction.md")
    for path, text in PACK_FILES.items():
        outside = [c for c in text if not c.isascii()
                   and not (path in arabic_ok and "\u0600" <= c <= "\u06ff")]
        assert outside == [], path
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
from engine.contracts.precedence import (  # noqa: E402
    DISABLED_RULE, SPECIFICITY_OPENING, SPECIFICITY_RULE, TWO_STATE_OPENING)
from engine.rulepack.generate import (  # noqa: E402
    contract_pairing_rows, overlaps, precedence_lines, state_pairs)

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
        f"| `{p.fg}` | `{p.bg}` | {p.minimum:g}:1 | {_high(p)} | "
        f"{'our floor' if p.criterion == 'system' else 'WCAG ' + p.criterion} |"
        for p in color.pairings]
    intro = next(line for line in reference.split("\n")
                 if line.startswith("Contracts add these pairings"))
    want = []
    by_name = {c.name: c for c in CONTRACTS}
    for name, p in contract_pairing_rows(CONTRACTS):
        source = "our floor" if p.criterion == f"the {name} contract" else f"WCAG {p.criterion}"
        uses = [b for b in by_name[name].tokens if b.role == p.fg]
        kind = [b for b in uses if (b.property == "text") != (p.criterion == "1.4.11")]
        used = []
        for b in (kind or uses):
            if f"{b.part} {b.property}" not in used:
                used.append(f"{b.part} {b.property}")
        want.append(f"| {name} | {', '.join(used)} | `{p.fg}` | `{p.bg}` | {p.minimum:g}:1 | "
                    f"{_high(p)} | {source} |")
    assert _rows(reference, intro) == want
    assert len(want) == len(set(want))
    # A floor of our own is never attributed to WCAG, and a pinned minimum
    # is marked as pinned.
    assert "| button | label text | `color.text.disabled` | `color.action.disabled` | 1.3:1 | " \
           "1.3:1 (pinned) | our floor |" in want
    # A non-text pairing names the part it is for, not the text that shares
    # its color.
    assert "| dialog | close icon | `color.text.muted` | `color.surface.raised` | 3:1 | " \
           "4.5:1 (our floor) | WCAG 1.4.11 |" in want


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
    row = "| card | title text, body text | `color.text.default` | " \
          "`color.surface.page` | 4.5:1 | 7:1 (WCAG 1.4.6, AAA) | WCAG 1.4.3 |"
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


def test_the_readme_states_the_one_resolution_order_word_for_word():
    readme = PACK_FILES[f"{PACK}/README.md"]
    section = readme.split("## Contracts\n", 1)[1].split("## Rules")[0]
    # Only contracts whose bindings can meet state the order; card, dialog
    # and status-banner have nothing to resolve.
    assert "every contract resolves" not in section
    assert "they resolve in this order; each contract whose bindings can meet that way says " \
           "so in usage.do:" in section
    assert f"1. {DISABLED_RULE}.\n" in section
    assert f"2. {SPECIFICITY_RULE}.\n" in section
    assert f"3. Where two other states still bind one part and property, the contract's line " \
           f"that starts \"{TWO_STATE_OPENING}\" says which wins." in section
    # The rule is the contracts' own: every contract with a disabled state
    # carries it word for word, and the pack copies the contracts as written.
    for c in CONTRACTS:
        if "disabled" in c.states:
            assert DISABLED_RULE in c.do
            assert f"- {DISABLED_RULE}\n" in PACK_FILES[f"{PACK}/contracts/{c.name}.yaml"]


def test_the_precedence_lines_are_the_contracts_own_and_every_overlap_has_them():
    readme = PACK_FILES[f"{PACK}/README.md"]
    listed = readme.split("with each contract's own line:")[1].split("## Rules")[0]
    met = [c for c in CONTRACTS if state_pairs(c)]
    assert [c.name for c in met] == ["button", "checkbox", "chip", "date", "input-prefix",
                                     "radio", "select", "selectable-row", "table", "text-field",
                                     "textarea"]
    for c in CONTRACTS:
        lines = precedence_lines(c)
        assert all(line in c.do for line in lines)
        if overlaps(c)[0]:
            assert SPECIFICITY_RULE in lines, c.name
        own = [line for line in lines if line.startswith(TWO_STATE_OPENING)]
        for a, b in state_pairs(c):
            if "disabled" not in (a, b):
                assert any(a in line and b in line for line in own), (c.name, a, b)
        pairs = "; ".join(f"{a} and {b}" for a, b in state_pairs(c))
        if not pairs:
            assert f"- {c.name}" not in listed
            continue
        head = f"- {c.name} (states that meet: {pairs})" + (":" if own else ".")
        assert "\n".join([head] + [f"  - {line}" for line in own]) in listed
    assert "- text-field (states that meet: disabled and error):\n  - When two states apply at " \
           "once, error wins over hover\n" in listed


def test_the_states_that_meet_come_from_the_bindings(tmp_path):
    by_name = {c.name: c for c in CONTRACTS}
    # A disabled button takes no hover or pressed binding, so those states
    # never meet disabled; hover and press still meet.
    assert state_pairs(by_name["button"]) == [("hover", "pressed")]
    assert state_pairs(by_name["text-field"]) == [("disabled", "error")]
    # Two states that bind the same role never meet: the row's hover and
    # pressed both take color.surface.sunken.
    assert state_pairs(by_name["selectable-row"]) == [
        ("hover", "selected"), ("pressed", "selected"), ("selected", "disabled")]
    contracts = tmp_path / "contracts"
    shutil.copytree(SEED_DIR, contracts)
    field = contracts / "text-field.yaml"
    text = field.read_text(encoding="utf-8")
    assert "property: border-color, role: color.line.danger, state: error}" in text
    field.write_text(text.replace("role: color.line.subtle, state: disabled}",
                                  "role: color.line.danger, state: disabled}"),
                     encoding="utf-8")
    changed = {c.name: c for c in load_folder(contracts)}["text-field"]
    assert state_pairs(changed) == []


def test_a_contract_with_overlapping_bindings_and_no_precedence_stops_the_pack(tmp_path):
    contracts = tmp_path / "contracts"
    shutil.copytree(SEED_DIR, contracts)
    button = contracts / "button.yaml"
    text = button.read_text(encoding="utf-8")
    kept = [line for line in text.split("\n") if line.strip()[2:] not in (
        DISABLED_RULE, SPECIFICITY_RULE, "When two states apply at once, pressed wins over hover")]
    assert len(kept) == len(text.split("\n")) - 3
    button.write_text("\n".join(kept), encoding="utf-8")
    with pytest.raises(RulePackError) as err:
        build_rule_pack(TS, contracts_dir=contracts)
    assert err.value.problems == (
        "button: it has a disabled state, and usage.do does not state the disabled rule; add "
        f"this line word for word: \"{DISABLED_RULE}\"",
        "button: two of its bindings for one part and property can apply at once, and usage.do "
        f"does not say which wins; add a line that starts \"{SPECIFICITY_OPENING}\"",
        "button: its hover and pressed bindings can set one part and property at once, and no "
        f"usage.do line that starts \"{TWO_STATE_OPENING}\" names both; add one that says "
        "which wins")


def test_a_two_state_line_must_name_both_states(tmp_path):
    contracts = tmp_path / "contracts"
    shutil.copytree(SEED_DIR, contracts)
    row = contracts / "selectable-row.yaml"
    text = row.read_text(encoding="utf-8")
    old = "When two states apply at once, selected wins over hover and pressed"
    assert old in text
    row.write_text(text.replace(old, "When two states apply at once, selected wins over hover"),
                   encoding="utf-8")
    with pytest.raises(RulePackError) as err:
        build_rule_pack(TS, contracts_dir=contracts)
    assert err.value.problems == (
        "selectable-row: its pressed and selected bindings can set one part and property at "
        f"once, and no usage.do line that starts \"{TWO_STATE_OPENING}\" names both; add one "
        "that says which wins",)


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
        assert "hand edit" not in audit
        assert "A value that passes but sits within 10 percent of its minimum is a minor " \
               "finding: record it, never block on it." in audit
        assert "A missing contract is a serious finding" in audit


def test_a_handoff_starts_only_when_asked():
    for f in FOUNDATIONS:
        handoff = PACK_FILES[f"{PACK}/{f.name}/handoff.md"]
        assert "- Hand off only when someone asks for a handoff; a build or an audit does not " \
               "start one." in handoff


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
                             capture_output=True, text=True,
                             cwd=str(SEED_DIR.parents[2])).stdout.strip()
        assert out == here.hexdigest(), seed


# Fix round 1: role uses per role, surface order per context, direction
# from the tokens, the screen route.
from engine.foundations.color_math import luminance  # noqa: E402
from engine.rulepack.guidance import load_guidance  # noqa: E402

BRANDS = ("#3366FF", "#E7EEE7", "#FFD400")
LATIN = build_system(AXES, "#3366FF", arabic=False).tokens
LATIN_PACK = build_rule_pack(LATIN)
LEVELS = ("sunken", "page", "card", "raised")
COLOR_MODES = {"light, standard contrast": "scheme:light",
               "dark, standard contrast": "scheme:dark",
               "light, high contrast": "scheme:light,contrast:high",
               "dark, high contrast": "scheme:dark,contrast:high"}


def test_every_status_role_has_its_own_line_and_its_uses_are_its_own():
    exact = dict(load_guidance("color").roles)
    status = [e for e in role_catalog(TS) if e.path.startswith("color.status.")]
    assert len(status) == 16
    for e in status:
        assert exact.get(e.path) == e.description, e.path
        binders = {c.name for c in CONTRACTS if e.path in c.roles()}
        for word, contract in (("button", "button"), ("field", "text-field"),
                               ("banner", "status-banner")):
            if word in e.description:
                assert contract in binders, (e.path, word)
    for e in role_catalog(TS):
        for name in ("architecture.md", "reference.md", "handoff.md"):
            assert f"`{e.path}`" in PACK_FILES[f"{PACK}/{e.foundation}/{name}"]


def test_no_two_roles_read_the_same_use():
    by_text = {}
    for e in role_catalog(TS):
        by_text.setdefault(e.description, []).append(e.path)
    assert {d: p for d, p in by_text.items() if len(p) > 1} == {}


DARK_LEVELS = ("page", "sunken", "card", "raised")


def _surface_order(ts, mode):
    levels = DARK_LEVELS if "dark" in mode else LEVELS
    v = {s: ts.resolve(f"color.surface.{s}", mode).upper() for s in levels}
    text = levels[0]
    for a, b in zip(levels, levels[1:]):
        if v[a] == v[b]:
            sign = "="
        else:
            sign = "<" if luminance(v[a]) < luminance(v[b]) else ">"
        text += f" {sign} {b}"
    return text, v


@pytest.mark.parametrize("brand", BRANDS)
def test_every_surface_order_statement_holds_for_the_build(brand):
    ts = build_system(AXES, brand).tokens
    files = build_rule_pack(ts)
    arch = files[f"{PACK}/color/architecture.md"]
    values = {}
    for words, mode in COLOR_MODES.items():
        order, v = _surface_order(ts, mode)
        values[words] = v
        assert f"- {words}: {order}" in arch, (brand, words)
    # The sentences written by hand, each checked against the same values.
    light, dark = values["light, standard contrast"], values["dark, standard contrast"]
    lhc, dhc = values["light, high contrast"], values["dark, high contrast"]
    for words, v in values.items():
        levels = DARK_LEVELS if "dark" in words else LEVELS
        assert all(luminance(v[a]) <= luminance(v[b]) for a, b in zip(levels, levels[1:]))
    assert "A surface that sits higher is never darker than the one below it." in arch
    for v in (dark, dhc):
        assert luminance(v["page"]) < luminance(v["card"]) < luminance(v["raised"])
    assert light["card"] == light["raised"] and lhc["card"] == lhc["raised"]
    assert "Where two levels share a color, as card and raised do in light" in arch
    assert lhc["page"] == lhc["card"] == lhc["raised"] == "#FFFFFF" != lhc["sunken"]
    assert dhc["page"] == "#000000" != dhc["sunken"]
    for v in (dark, dhc):
        assert luminance(v["page"]) < luminance(v["sunken"]) < luminance(v["card"])
    assert "in light the page, card and raised surfaces are white and the sunken surface keeps " \
           "its recess step, and in dark the page is black, the sunken surface keeps its recess " \
           "between the page and the card" in arch
    record = files[f"{PACK}/decisions/dark-surfaces-rise.md"]
    assert "The sunken surface sits between the page and the card, at standard and high " \
           "contrast." in record
    edge = files[f"{PACK}/decisions/container-edge.md"]
    assert "in light high contrast the page, card, sunken and raised surfaces are all white" \
        in edge


def _vary_line(text):
    return next(line for line in text.split("\n") if line.startswith("Roles vary on"))


@pytest.mark.parametrize("ts,files", [(TS, PACK_FILES), (LATIN, LATIN_PACK)])
def test_the_axes_a_foundation_names_are_the_axes_its_roles_use(ts, files):
    for f in FOUNDATIONS:
        entries = [e for e in role_catalog(ts) if e.foundation == f.name]
        used = [a for a in ts.axes
                if any(a in k for e in entries for k in ts.get(e.path).modes)]
        line = _vary_line(files[f"{PACK}/{f.name}/architecture.md"])
        assert line == ("Roles vary on " + ", ".join(used) + "." if used
                        else "Roles vary on no mode axis."), f.name
        handoff = files[f"{PACK}/{f.name}/handoff.md"]
        listed = [a for a in ts.axes if f"\n- {a} (" in handoff]
        assert listed == used, f.name


def test_a_latin_only_pack_says_nothing_about_arabic_or_right_to_left_type():
    for path, text in LATIN_PACK.items():
        if path.startswith((f"{PACK}/decisions/", f"{PACK}/contracts/")):
            continue
        assert "arabic" not in text.lower() or "`arabic-text`" in text, path
        assert "Arabic" not in text.replace("`arabic-text`", ""), path
    for name in FILES:
        text = LATIN_PACK[f"{PACK}/type/{name}"]
        for words in ("right to left", "right-to-left", "rtl", "both directions"):
            assert words not in text, (name, words)
    assert _vary_line(LATIN_PACK[f"{PACK}/type/architecture.md"]) == "Roles vary on contrast."
    assert "## Arabic type" not in LATIN_PACK[f"{PACK}/direction.md"]
    assert "## Arabic type" in PACK_FILES[f"{PACK}/direction.md"]
    assert "- direction (ltr, rtl): dir=\"rtl\" on the html element" in \
        LATIN_PACK[f"{PACK}/motion/handoff.md"]
    assert "- direction (ltr, rtl)" not in LATIN_PACK[f"{PACK}/type/handoff.md"]
    assert "- direction (ltr, rtl)" in PACK_FILES[f"{PACK}/type/handoff.md"]


def test_the_screen_route_loads_the_direction_and_content_rules():
    for files in (PACK_FILES, LATIN_PACK):
        row = next(line for line in files[f"{PACK}/README.md"].split("\n")
                   if line.startswith("| Build or change a screen |"))
        for name in ("contracts/", "<foundation>/architecture.md", "direction.md", "content.md",
                     "<foundation>/handoff.md"):
            assert name in row, name



def test_plain_path_citations_are_relative_to_the_pack():
    """Paths in the text (not markdown link targets) resolve from rule-pack/,
    as README says."""
    for path, text in PACK_FILES.items():
        if path.startswith(f"{PACK}/decisions/") or path.endswith((".yaml", ".json")):
            continue
        plain = re.sub(r"\]\([^)]*\)", "]", text)
        for cited in re.findall(r"(?<![\w./<>-])((?:[a-z0-9-]+/)*[a-z0-9-]+\.md)\b", plain):
            assert f"{PACK}/{cited}" in PACK_FILES, (path, cited)
        for cited in re.findall(r"(?<![\w./-])(contracts|decisions)/(?![\w])", plain):
            assert any(k.startswith(f"{PACK}/{cited}/") for k in PACK_FILES), (path, cited)
        assert "../" not in plain, path


def test_the_reference_says_which_mode_the_alias_column_shows():
    reference = PACK_FILES[f"{PACK}/color/reference.md"]
    assert "| Role | Type | Points at (base) |" in reference
    typ = PACK_FILES[f"{PACK}/type/reference.md"]
    body = TS.resolve("type.text.body")["fontFamily"]
    stack = body if isinstance(body, str) else ", ".join(body)
    assert stack.count(",") >= 1 and stack.split(",")[1].strip().strip('"') in typ


def test_the_readme_names_the_whole_rebuild_for_a_stale_pack():
    readme = PACK_FILES[f"{PACK}/README.md"]
    assert "the pack describes other tokens: build again into this folder with --rule-pack " \
           "--force." in readme
