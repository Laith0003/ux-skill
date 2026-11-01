"""The page flow inside an existing system reads the brand before it picks.

Two builds inside real design systems kept the tokens but never learned how
the brand makes pages: the page style, the content register and the dials
were found by hand, the playbook spoke only the engine's role names, the wow
guidance mapped industries to effects, and the ban list recommended em
dashes. These tests hold the docs to the flow.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = (ROOT / "commands" / "ux-design.md").read_text(encoding="utf-8")
LANDING = (ROOT / "references" / "surfaces" / "landing.md").read_text(encoding="utf-8")
WOW = (ROOT / "references" / "foundations" / "wow.md").read_text(encoding="utf-8")
SLOP = (ROOT / "references" / "styles" / "anti-slop.md").read_text(encoding="utf-8")
DISCOVERY = (ROOT / "references" / "process" / "discovery-protocol.md").read_text(encoding="utf-8")


def _section(text: str, heading: str, level: str = "### ") -> str:
    start = text.index(heading)
    nxt = text.find("\n" + level, start + len(heading))
    return text[start:nxt if nxt != -1 else len(text)]


def _no_dashes(text: str, name: str) -> None:
    assert "\u2014" not in text and "\u2013" not in text, name
    assert not re.search(r"\w -- \w", text), name


def test_the_page_style_step_comes_right_after_the_existing_system_step():
    assert DESIGN.index("### 1a. An existing design system") < DESIGN.index("### 1a.1.") \
        < DESIGN.index("### 1b.")
    step = _section(DESIGN, "### 1a.1.")
    for fact in ("`scheme`", "`rhythm`", "`panels`", "`headlines`", "`density`", "`imagery`",
                 "`color_use`"):
        assert fact in step, fact
    assert "dark default counts" in step and "above the token scale" in step
    assert "templates" in step and "screenshots" in step
    assert "defaults" in step and "only where the brand has no page" in step
    _no_dashes(step, "step 1a.1")


def test_the_register_is_found_and_followed():
    step = _section(DESIGN, "### 1a.1.")
    for part in ("voice sheet", "facts file", "banned words", "dialect", "currency"):
        assert part in step, part
    assert "every public string follows it" in step and "`register`" in step


def test_the_dials_come_from_the_brand_with_an_existing_system():
    step = _section(DESIGN, "### 1a.1.")
    assert "quiet brand gets quiet dials" in step
    dials = _section(DESIGN, "### 3. Set the dials")
    assert "step 1a.1" in dials and "came from" in dials
    order = _section(DESIGN, "### Page mode, in order")
    assert order.index("system detect") < order.index("Page style") < order.index("Suggestions")


def test_discovery_takes_what_the_brand_already_answers():
    process = _section(DESIGN, "### 1. Run the discovery protocol")
    assert "brand book" in process and "`sources`" in process
    assert "Block generation until provided" not in DESIGN
    skip = DISCOVERY[DISCOVERY.index("## When to skip discovery"):DISCOVERY.index("## The 10 required fields")]
    assert "brand book" in skip and "`sources`" in skip and "wow moment" in skip


def test_the_brand_step_reads_language_and_the_brand_book():
    step = _section(DESIGN, "### Step 1.5")
    assert '"language"' in step and '"strategy"' in step and '"photography"' in step
    assert "templates and pages" in step and "never assumes" in step
    assert "never made of voice words" in step


def test_the_playbook_speaks_the_systems_own_names():
    sec = _section(LANDING, "## Inside an existing design system", "## ")
    assert "vocabulary" in sec and "never names to write" in sec
    assert "var(--space-section)" in sec and "engine.io.propose" in sec
    assert "Photographs are required" in sec and "photo_exclusions" in sec and "logo" in sec
    assert "product-screen section" not in sec and "no picture" not in sec
    _no_dashes(sec, "landing existing-system section")


def test_no_guidance_maps_an_industry_to_an_effect():
    from engine.synthesizer.axes import INDUSTRY_ALIASES, INDUSTRY_SEEDS
    low = WOW.lower()
    for word in sorted(set(INDUSTRY_SEEDS) | set(INDUSTRY_ALIASES)) + ["fintech", "dev tool",
                                                                       "skip-hire", "law-firm"]:
        assert word.replace("-", " ") not in low.replace("-", " "), word
    pairings = LANDING[LANDING.index("### Pattern pairings"):LANDING.index("## Compositions")]
    for word in ("Fintech", "SaaS landing", "Developer-tooling", "AI product landing"):
        assert word not in pairings, word


def test_no_em_dash_is_recommended_and_two_bans_are_scoped_to_generated_systems():
    assert "em dashes (\u2014) where appropriate" not in SLOP
    row = next(ln for ln in SLOP.splitlines() if ln.startswith("| Straight quotes"))
    assert "No em dashes" in row
    head = SLOP[:SLOP.index("## Responsive")]
    ten, eleven = head.index("\n10. "), head.index("\n11. ")
    assert ten < eleven
    principle = head[eleven:head.index("\n", eleven + 1)]
    assert "generated systems only" in principle and "system font stack" in principle \
        and "pure white" in principle
    for row_start in ("| Pure white", "| Arial, Roboto"):
        line = next(ln for ln in SLOP.splitlines() if ln.startswith(row_start))
        assert "generated system" in line, row_start


def test_the_build_gets_the_page_style_and_the_register():
    step = _section(DESIGN, "### 4. Build the page")
    assert ".ux/page-style.json" in step and "register" in step
    assert "which register file the copy followed" in step
    facts = _section(DESIGN, "### 1a.1.")
    assert "left out, never guessed" in facts


def test_no_reference_recommends_a_long_dash():
    pattern = re.compile(r"(?:em|en)[ -]dash(?:es)? \(|curly quotes and em dashes|"
                         r"em dashes \([^)]*\) where", re.IGNORECASE)
    for path in sorted((ROOT / "references").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        assert not pattern.search(text), path.relative_to(ROOT)


def test_no_use_when_line_names_an_industry():
    arsenal = (ROOT / "references" / "styles" / "arsenal.md").read_text(encoding="utf-8")
    words = re.compile(r"\b(?:fintech|saas|dev-tool|developer tools|infrastructure products|"
                       r"hospitality|clinics|agencies)\b", re.IGNORECASE)
    for text, name in ((arsenal, "arsenal.md"), (LANDING, "landing.md")):
        for line in text.splitlines():
            if line.startswith(("**Use when**", "**Pick it when.**", "**Terminal mockup.**")):
                assert not words.search(line), (name, line)
