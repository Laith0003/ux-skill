"""/ux-design page mode has one path, the 4.0 one.

Three agents followed commands/ux-design.md literally on real landing pages and
the 3.x steps fought 4.0 each time: the recommend palette called "the only"
tokens, anti-slop bans hitting the client's own identity, a page-sequence picker
keyed on one verb, "render every section" against "invent nothing", a mandatory
subagent dispatch and three icon rules. These tests hold the rewrite.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "commands" / "ux-design.md"
AGENT = ROOT / "agents" / "frontend-engineer.md"
SLOP = ROOT / "references" / "styles" / "anti-slop.md"
RECORD = ROOT / "engine" / "rulepack" / "decisions" / "client-identity-wins.md"


def _doc() -> str:
    return DESIGN.read_text(encoding="utf-8")


def _section(text: str, heading: str, level: str = "### ") -> str:
    start = text.index(heading)
    nxt = text.find("\n" + level, start + len(heading))
    return text[start:nxt if nxt != -1 else len(text)]


# ---------------------------------------------------------------- tokens


def test_the_system_tokens_are_the_only_tokens():
    doc = _doc()
    assert "the only color tokens" not in doc
    assert "the only typography" not in doc
    step = _section(doc, "### Step 3")
    assert "only tokens" in step
    assert "system build" in step
    assert "suggestion" in step


def test_recommend_and_synthesize_are_suggestions_only_without_a_system():
    step = _section(_doc(), "### Step 2")
    assert "recommend" in step and "synthesize" in step
    assert "no design system" in step.lower() or "no system" in step.lower()
    assert "suggestion" in step


def test_page_mode_builds_a_system_when_none_exists():
    doc = _doc()
    sec = _section(doc, "### 1b.")
    assert "system build" in sec and "--rule-pack" in sec
    assert "ux design-md" not in sec, "design-md writes foreign fonts; the built system is the contract"


def test_no_step_is_labelled_v2():
    assert "v2 step" not in _doc()
    assert "## v2 Python integration" not in _doc()


# ---------------------------------------------------------------- identity


def test_the_hard_rules_yield_to_the_clients_identity():
    rules = _section(_doc(), "## Hard rules", "## ")
    assert "decisions/client-identity-wins.md" in rules
    assert not re.search(r"^- NEVER use purple/blue AI gradients\. Single high-contrast accent, saturation < 80%\.$",
                         rules, re.M)


def test_anti_slop_extends_the_existing_system_principle_to_identity():
    slop = SLOP.read_text(encoding="utf-8")
    head = slop[:slop.index("## Responsive")]
    assert "decisions/client-identity-wins.md" in head
    assert "decisions/existing-system-wins.md" in head
    principle = next(ln for ln in head.splitlines() if "client-identity-wins" in ln)
    for word in ("logo", "gradient", "saturat", "white", "no full system"):
        assert word in principle.lower(), word
    for row in ("| Pure white", "| Oversaturated accents", "| The \"AI\" purple-to-blue gradient",
                "| Full-bleed gradient hero"):
        line = next(ln for ln in slop.splitlines() if ln.startswith(row))
        assert "client-identity-wins" in line, row


def test_the_identity_record_is_active_and_routed():
    text = RECORD.read_text(encoding="utf-8")
    assert "status: active" in text
    assert "existing-system-wins" in text
    history = (RECORD.parent / "HISTORY.md").read_text(encoding="utf-8")
    assert "(client-identity-wins.md)" in history


# ---------------------------------------------------------------- sequence


def test_step_2_5_reads_the_4_0_brief():
    step = _section(_doc(), "### Step 2.5")
    assert "select_for_brief" in step
    assert "select_sequence(query)" not in step
    for field in ("product_type", "industry", "proof", "contact", "stage"):
        assert field in step, field
    assert "Render EVERY section" not in step
    assert "dropped" in step and "invent" in step


def test_the_agent_never_forces_invented_proof():
    agent = AGENT.read_text(encoding="utf-8")
    assert "**Render every section** in `section_sequence`" not in agent
    assert "dropped" in agent and "invent" in agent


# ---------------------------------------------------------------- dispatch


def test_the_subagent_dispatch_is_a_recommendation():
    doc = _doc()
    step = _section(doc, "### 4.")
    assert "optional" in step.lower() or "recommended" in step.lower()
    assert "Do not write the design yourself" not in doc
    assert "Call the Task tool with" not in doc


# ---------------------------------------------------------------- icons


def test_one_icon_rule():
    doc = _doc()
    agent = AGENT.read_text(encoding="utf-8")
    for text, name in ((doc, "ux-design.md"), (agent, "frontend-engineer.md")):
        assert "Material Symbols" not in text, name
        assert "Lucide-style" not in text, name
        assert "give every card/pill/stat" not in text.lower(), name
    assert len(re.findall(r"^- \*\*Icons\.\*\*", doc, re.M)) == 1
    rule = next(ln for ln in doc.splitlines() if ln.startswith("- **Icons.**"))
    for word in ("type.icon.stroke", "type.icon.size", "emoji", "distinct"):
        assert word in rule, word
    assert "commands/ux-design.md" in agent and "Icons" in agent
