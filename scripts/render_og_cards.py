"""Render the share cards: docs/og-image.png and the current pages' cards.

    python scripts/render_og_cards.py              # every card below
    python scripts/render_og_cards.py og-image mcp # only these

scripts/og-card.html is the source. Before rendering, its figures (the
release numeral, catalogue entries, lint rules, MCP tools, brand specs) are
refreshed in place from the engine: engine.data_loader.stats(),
engine.mcp.TOOLS and scripts/site_version.py. docs/og-image.png is the
homepage card at exactly 1200x630. The page cards reuse the same look with
their own eyebrow, title and line, at 2400x1260 like the rest of docs/og/.

Cards for dated blog posts stay with scripts/render-og-pages.mjs: they
describe the release they were written for.

The card links its web fonts from a font CDN. Those requests are fetched by
Python and handed to the page, so the render trusts the same certificate
store as the rest of the toolchain.
"""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine.data_loader import stats  # noqa: E402
from engine.mcp import TOOLS  # noqa: E402
from site_version import line, version  # noqa: E402

CARD = ROOT / "scripts" / "og-card.html"
DOCS = ROOT / "docs"


def figures() -> dict:
    counts = stats()
    return {
        "entries": f"{sum(counts.values()):,}",
        "rules": str(counts["anti-patterns"]),
        "tools": str(len(TOOLS)),
        "brands": str(counts["brands"]),
    }


def refresh_card() -> str:
    """Write the engine's figures into og-card.html and return the page."""
    html = CARD.read_text(encoding="utf-8")
    for key, value in figures().items():
        html = re.sub(rf'(<b data-fig="{key}">)[^<]*(</b>)', rf"\g<1>{value}\g<2>", html)
    major, minor = line().split(".")
    html = re.sub(r'(<div class="three" data-fig="line">).*?(</div>)',
                  rf"\g<1>{major}<em>.</em>{minor}\g<2>", html)
    CARD.write_text(html, encoding="utf-8")
    return html


# slug -> (eyebrow, title, line); the title may hold <br> and <i>
PAGES = {
    "home": ("The design brain for AI coding", "One brand color in.<br><i>A design system out.</i>",
             "Nine foundations, checked against WCAG before a file is written."),
    "about": ("About", "Why ux-skill exists", "From a prose-only v1 to a design system engine"),
    "blog-index": ("Blog", "Long-form writing on<br>AI coding's design problem",
                   "Honest comparisons. Real numbers. No marketing verbs."),
    "compare": ("Compare", "Every Claude design<br>skill, side by side", "ux-skill 46/50 &middot; next best 30/50"),
    "faq": ("FAQ", "25 questions,<br>answered straight", "Install, license, plugin landscape, MCP"),
    "mcp": ("MCP server", "{tools} tools over stdio.<br>Any MCP host.",
            "Claude Desktop &middot; Cursor &middot; Windsurf &middot; any MCP agent"),
    "roadmap": ("Roadmap", "What ships next", "v{version} shipped &middot; Foundations"),
}


def page_card(base: str, eyebrow: str, title: str, sub: str) -> str:
    fill = {**figures(), "version": version()}
    title, sub = title.format(**fill), sub.format(**fill)
    html = re.sub(r'<div class="eyebrow">.*?</div>', f'<div class="eyebrow">{eyebrow}</div>', base, flags=re.S)
    html = re.sub(r"<h1>.*?</h1>", f'<h1 dir="auto">{title}</h1>', html, flags=re.S)
    html = re.sub(r'<p class="sub">.*?</p>', f'<p class="sub" dir="auto">{sub}</p>', html, flags=re.S)
    return html.replace("</style>", "  h1{font-size:58px}\n  .sub{font-size:21px;margin-top:22px}\n"
                                    "  .three{font-size:480px}\n</style>", 1)


def _fetch(route):
    req = urllib.request.Request(route.request.url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"})
    with urllib.request.urlopen(req, timeout=30) as res:
        route.fulfill(status=res.status, body=res.read(),
                      headers={"content-type": res.headers.get("content-type", "application/octet-stream"),
                               "access-control-allow-origin": "*"})


def render(jobs) -> None:
    """jobs: (html, out_path, device_scale_factor)."""
    from playwright.sync_api import sync_playwright
    tmp = ROOT / ".og-render.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for html, out, scale in jobs:
                page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=scale)
                page.route(re.compile(r"^https?://"), _fetch)
                tmp.write_text(html, encoding="utf-8")
                page.goto(tmp.as_uri())
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(600)
                page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
                page.close()
                print("wrote", out.relative_to(ROOT))
        finally:
            browser.close()
            tmp.unlink(missing_ok=True)


def main(only) -> None:
    base = refresh_card()
    jobs = []
    if not only or "og-image" in only:
        jobs.append((base, DOCS / "og-image.png", 1))
    for slug, (eyebrow, title, sub) in PAGES.items():
        if not only or slug in only:
            jobs.append((page_card(base, eyebrow, title, sub), DOCS / "og" / f"{slug}.png", 2))
    render(jobs)


if __name__ == "__main__":
    main(sys.argv[1:])
