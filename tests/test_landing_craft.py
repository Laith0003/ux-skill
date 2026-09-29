"""Landing-page craft rules the build reads from the references.

These hold the rules for what a page asks and how it earns the ask: the
fields that shape it, what sits at the form, where the FAQ's questions come
from, and when a page closes its exits. The engine half is pinned in
tests/test_page_sequence_ask.py; these pin the words the builder reads.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _section(text: str, heading: str, level: str = "### ") -> str:
    start = text.index(heading)
    nxt = text.find("\n" + level, start + len(heading))
    return text[start:nxt if nxt != -1 else len(text)]


LANDING = "references/surfaces/landing.md"
DESIGN = "commands/ux-design.md"


# ---------------------------------------------------------------- the ask


def test_step_2_5_documents_the_three_ask_fields_and_campaign():
    step = _section(_read(DESIGN), "### Step 2.5")
    for field in ("commitment", "arrival", "objections", "at_the_ask", "objection_map"):
        assert f"`{field}`" in step, field
    for value in ("`card`", "`call`", "`purchase`", "`contract`", "`branded`", "`cold`",
                  "`approval`", "`campaign`"):
        assert value in step, value
    assert "never a second button" in step
    rows = [ln for ln in step.splitlines()
            if ln.startswith(("| `commitment`", "| `arrival`", "| `objections`"))]
    assert len(rows) == 3


def test_page_mode_writes_the_new_fields_into_the_brief():
    step = _section(_read(DESIGN), "### Page mode, in order")
    for field in ("`commitment`", "`arrival`", "`objections`"):
        assert field in step, field


def test_the_self_review_names_each_sections_job_and_the_faq_source():
    template = _section(_read(DESIGN), "### 5. Format the output")
    assert "naming its job" in template
    assert "where the FAQ's questions came from" in template


def test_the_error_table_names_the_new_fields():
    row = next(ln for ln in _read(DESIGN).splitlines()
               if ln.startswith("| `select_for_brief` raises"))
    for field in ("`commitment`", "`arrival`", "`objections`"):
        assert field in row, field


def test_the_landing_playbook_states_the_ask_rule():
    flow = _section(_read(LANDING), "### The ask sets how much the page argues")
    assert "light ask" in flow and "heavy ask" in flow
    assert "text link" in flow
    assert "is cut" in flow


def test_the_answers_sit_at_the_ask_and_are_never_invented():
    ask = _section(_read(LANDING), "### At the ask")
    for need in ("who runs this", "data", "goes wrong", "money back", "`at_the_ask`"):
        assert need in ask, need
    assert "never invented" in ask


def test_faq_questions_come_from_the_customer():
    cta = _section(_read(LANDING), "## CTA", "## ")
    assert "FAQ questions come from the customer" in cta
    assert "operational questions" in cta
    assert "Proof sits beside the objection it answers" in _read(LANDING)


def test_the_form_contract_has_a_success_state():
    form = _section(_read("references/foundations/component-behaviors.md"), "## Form", "## ")
    assert "**Success state.**" in form
    for need in ("what happens next", "channel", "phone-first", "within what time"):
        assert need in form, need
    assert "success-state contract" in _read(LANDING)


def test_discovery_asks_for_objections_without_blocking():
    text = _read("references/process/discovery-protocol.md")
    part = _section(text, "### 3a. What stops people saying yes (optional)")
    assert "never block" in part and "`objections`" in part
    assert "never write objections for them" in part


# ---------------------------------------------------------------- campaign pages


def test_a_campaign_page_closes_its_exits_in_the_playbook():
    text = _read(LANDING)
    nav = _section(text, "### Nav bar")
    assert "**Campaign page.**" in nav and "no nav links" in nav
    footer = _section(text, "## Footer", "## ")
    assert "campaign page keeps a reduced footer" in footer
    assert "new tab" in footer
