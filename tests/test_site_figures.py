"""The public site states the engine's own figures and holds together.

- Every count the site states about ux-skill (MCP tools, lint rules, brand
  specs, catalogue entries) is read from the engine: `engine.mcp.TOOLS` and
  `engine.data_loader.stats()`, the numbers `uxskill stats` prints.
  Dated blog posts describe the release they were written for, so they keep
  their figures; every other page, the blog indexes included, is current.
- Every og:image and twitter:image resolves to a file in docs/.
- No section eyebrow draws a dot or bullet before its label.
- The retired preview pages are gone and nothing links to them.
"""
import json
import re
from pathlib import Path

import pytest

from engine.data_loader import stats
from engine.mcp import TOOLS

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://uxskill.laithjunaidy.com/"
PAGES = sorted(DOCS.rglob("*.html"))

COUNTS = stats()
FIGURES = {
    "tools": len(TOOLS),
    "rules": COUNTS["anti-patterns"],
    "brands": COUNTS["brands"],
    "entries": sum(COUNTS.values()),
}


def _rel(page):
    return str(page.relative_to(DOCS))


def _dated_post(page, html):
    """A blog post with a datePublished: an article about its own release."""
    return "blog" in page.relative_to(DOCS).parts and '"datePublished"' in html.replace(" ", "")


CURRENT = [p for p in PAGES if not _dated_post(p, p.read_text(encoding="utf-8"))]

# Claims about ux-skill, as the site words them in English. The number is
# group "n"; commas are thousands separators.
CLAIMS = [
    ("tools", r"\b(?P<n>\d+) MCP tools\b"),
    ("tools", r"\b(?P<n>\d+) (?:MCP |typed )?tools (?:over stdio|any (?:agent|MCP)|registered)"),
    ("tools", r"\bexposes (?P<n>\d+) (?:MCP )?(?:\(Model Context Protocol\) )?tools"),
    ("tools", r"ux-skill's (?P<n>\d+) tools"),
    ("tools", r"MCP server &middot; (?P<n>\d+) tools"),
    ("rules", r"\b(?P<n>\d+) (?:anti-pattern |lint |linter |regex |deterministic )+rules\b"),
    ("rules", r"\b(?P<n>\d+)-rule (?:linter|lint)"),
    ("rules", r"\bLint (?P<n>\d+) anti-patterns\b"),
    ("rules", r"Anti-patterns &middot; (?P<n>\d+)<"),
    ("rules", r"\b(?P<n>\d+) anti-patterns</text>"),
    ("rules", r">anti-patterns</text><text [^>]*>(?P<n>\d+)<"),
    ("brands", r"\b(?P<n>\d+) (?:real )?brand (?:specs|DESIGN)"),
    ("brands", r"Brand specs &middot; (?P<n>\d+)<"),
    ("entries", r"\b(?P<n>\d,\d{3})(?:-entry| (?:structured |cross-referenced )?entries)"),
    ("entries", r"<b>(?P<n>\d,\d{3})</b>"),
]

# Sentences that state a past figure on purpose: (page, text, why).
HISTORY = [
    ("roadmap.html", "v2.0 ships with 35 rules", "the roadmap's record of v2.0"),
    ("roadmap.html", "+17 anti-pattern rules", "the roadmap's record of v2.1"),
    ("anti-patterns.html", "See all 145 rules", "an example quoted inside a rule's fix"),
    ("anti-patterns.html", "first regex linter with 145 rules", "an example quoted inside a rule"),
]

# The headline numbers a stat block may show: the engine's figures, the nine
# foundations and the 17 supported AI coding tools.
STAT_VALUES = {str(v) for v in FIGURES.values()} | {f"{FIGURES['entries']:,}", "9", "17"}


def test_figures_are_the_engines():
    assert FIGURES["tools"] == len(TOOLS) and FIGURES["rules"] == COUNTS["anti-patterns"]
    assert FIGURES["entries"] == sum(COUNTS.values()) > FIGURES["rules"]


def test_a_stale_claim_is_caught():
    html = "<p>exposes 18 MCP tools and 152 anti-pattern rules over 1,243 structured entries</p>"
    found = {(k, m.group("n")) for k, rx in CLAIMS for m in re.finditer(rx, html)}
    assert {("tools", "18"), ("rules", "152"), ("entries", "1,243")} <= found


@pytest.mark.parametrize("page", CURRENT, ids=_rel)
def test_page_states_the_engines_figures(page):
    html = page.read_text(encoding="utf-8")
    for rel, text, _why in HISTORY:
        if rel == _rel(page):
            html = html.replace(text, "")
    wrong = []
    for kind, rx in CLAIMS:
        for m in re.finditer(rx, html):
            if int(m.group("n").replace(",", "")) != FIGURES[kind]:
                wrong.append(f"{kind} {m.group('n')} in ...{m.group(0)[-60:]}")
    for n in re.findall(r'<div class="n">([\d,]+)</div>', html):
        if n not in STAT_VALUES:
            wrong.append(f"stat block {n}")
    assert wrong == [], (
        f"docs/{_rel(page)} states a figure the engine does not give: {wrong}. The engine has "
        f"{FIGURES['tools']} MCP tools (engine.mcp.TOOLS), {FIGURES['rules']} lint rules, "
        f"{FIGURES['brands']} brand specs and {FIGURES['entries']:,} entries "
        "(python -m engine.cli.main stats); fix the page, or its generator, to say these.")


@pytest.mark.parametrize("page", PAGES, ids=_rel)
def test_every_share_image_exists(page):
    head = page.read_text(encoding="utf-8").split("</head>", 1)[0]
    bad = []
    for key, url in re.findall(
            r'<meta (?:property|name)="(og:image|twitter:image)" content="([^"]*)"', head):
        path = url.split("?", 1)[0]
        if not path.startswith(SITE):
            bad.append(f"{key} {url} is not on {SITE}")
        elif not (DOCS / path[len(SITE):]).is_file():
            bad.append(f"{key} {url} has no file at docs/{path[len(SITE):]}")
    assert bad == [], (f"docs/{_rel(page)}: {bad}. Point the tag at an image under docs/ "
                       "(the 4.0 card is docs/og-image.png) or render the missing file.")


# A status badge (badge-success, badge-warning, ...) in a generated system's
# preview is a component specimen whose dot shows the state, not an eyebrow.
_EYEBROW = r'class="(?![^"]*\bbadge-)[^"]*\b(?:eyebrow|k|kicker|badge)\b[^"]*"'


def test_an_eyebrow_dot_is_caught_and_a_status_dot_is_not():
    dotted = r'>\s*<span class="(?:dot|d)\b'
    assert re.search(_EYEBROW + dotted, '<span class="eyebrow"><span class="dot"></span>Install</span>')
    assert re.search(_EYEBROW + dotted, '<p class="badge"><span class="dot"></span> 9</p>')
    assert not re.search(_EYEBROW + dotted, '<span class="badge badge-success"><span class="dot"></span>Live</span>')


@pytest.mark.parametrize("page", PAGES, ids=_rel)
def test_no_eyebrow_draws_a_dot(page):
    html = page.read_text(encoding="utf-8")
    bad = re.findall(_EYEBROW + r'>\s*<span class="(?:dot|d)\b[^"]*"', html)
    bad += re.findall(r'\.(?:eyebrow|k|kicker|badge)\s+\.(?:dot|d)\s*\{', html)
    bad += [m for m in re.findall(r'\.[\w-]*(?:eyebrow|kicker)[\w-]*::?before\s*\{[^}]*\}', html)
            if "content" in m]
    assert bad == [], (f"docs/{_rel(page)} draws a dot before an eyebrow label: {bad}. Remove the "
                       "dot span from the label and its CSS rule; the label stands on its own.")


ORPHANS = ("home-v31-preview.html", "home-v31-scene.html", "index-classic.html")


def test_retired_pages_are_gone_and_unlinked():
    assert not [o for o in ORPHANS if (DOCS / o).exists()]
    linked = [f"{_rel(p)} -> {o}" for p in PAGES for o in ORPHANS
              if o in p.read_text(encoding="utf-8")]
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    linked += [f"sitemap.xml -> {o}" for o in ORPHANS if o in sitemap]
    assert linked == [], f"links to retired pages remain: {linked}; remove each link"


def test_homepage_presents_4_0():
    html = (DOCS / "index.html").read_text(encoding="utf-8")
    for text in ("pip install --upgrade uxskill", "pip install --upgrade 'uxskill[mcp]'",
                 "npx uxskill@latest", "migrating-to-4.md", "nine foundations"):
        assert text in html, f"docs/index.html does not say {text!r}; add it to the 4.0 section"
    hero = html.split('id="hero"', 1)[1].split("</section>", 1)[0]
    assert "brand color" in hero and "WCAG" in hero, (
        "the hero must say what 4.0 does: one brand color and a brief in, a WCAG-gated "
        "design system out")
    assert re.search(r'<img [^>]*src="/media/photos/[^"]+\.(?:jpg|webp)"', html), (
        "docs/index.html shows no photograph; use one from docs/media/photos/")
