"""Inject per-page og:image and twitter:image into every docs/*.html page.

Idempotent: pages that already declare an og:image are skipped.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent

# Map docs path -> og image slug (under docs/og/).
PAGE_TO_SLUG = {
    "docs/index.html":           "home",
    "docs/compare.html":         "compare",
    "docs/about.html":           "about",
    "docs/faq.html":             "faq",
    "docs/roadmap.html":         "roadmap",
    "docs/mcp.html":             "mcp",
    "docs/blog/index.html":      "blog-index",
    "docs/blog/vs-ui-ux-pro-max.html":                 "vs-ui-ux-pro-max",
    "docs/blog/anti-ai-slop-claude-skills.html":       "anti-ai-slop-claude-skills",
    "docs/blog/best-claude-code-design-skills-2026.html": "best-claude-code-design-skills-2026",
    "docs/blog/cursor-design-plugin.html":             "cursor-design-plugin",
    "docs/blog/python-design-system-generator.html":   "python-design-system-generator",
    "docs/blog/ai-design-fingerprints-list.html":      "ai-design-fingerprints-list",
    "docs/blog/claude-code-marketplace-best-plugins.html": "claude-code-marketplace-best-plugins",
    "docs/blog/figma-vs-ux-skill.html":                "figma-vs-ux-skill",
    "docs/blog/windsurf-design-rules.html":            "windsurf-design-rules",
    "docs/blog/monorepo-design-system-ai-coding.html": "monorepo-design-system-ai-coding",
    "docs/blog/regex-linter-for-ai-coding.html":       "regex-linter-for-ai-coding",
    "docs/blog/dark-editorial-cinema-design.html":     "dark-editorial-cinema-design",
    "docs/blog/mcp-server-design-intelligence.html":   "mcp-server-design-intelligence",
    "docs/blog/motion-presets-framer-gsap-css.html":   "motion-presets-framer-gsap-css",
    "docs/blog/dogfooding-design-engine.html":         "dogfooding-design-engine",
}


def render_block(slug: str) -> str:
    url = f"https://uxskill.laithjunaidy.com/og/{slug}.png"
    return (
        f'  <meta property="og:image" content="{url}">\n'
        f'  <meta property="og:image:width" content="1200">\n'
        f'  <meta property="og:image:height" content="630">\n'
        f'  <meta property="og:image:alt" content="ux-skill — {slug}">\n'
        f'  <meta name="twitter:image" content="{url}">\n'
    )


def inject(path: Path, slug: str) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    if 'property="og:image"' in text:
        return False, "already has og:image"
    # Find the og:title line and inject the image block right after the og:description (or og:title) line.
    m = re.search(r'(<meta property="og:description"[^>]*>\n)', text)
    if m:
        new = text[: m.end()] + render_block(slug) + text[m.end():]
    else:
        # Fallback: inject after og:title
        m2 = re.search(r'(<meta property="og:title"[^>]*>\n)', text)
        if not m2:
            return False, "no og:title found"
        new = text[: m2.end()] + render_block(slug) + text[m2.end():]
    path.write_text(new, encoding="utf-8")
    return True, "injected"


def main() -> None:
    docs_count = 0
    land_count = 0
    for rel, slug in PAGE_TO_SLUG.items():
        p_docs = ROOT / rel
        p_landing = ROOT / rel.replace("docs/", "landing/", 1)
        if p_docs.exists():
            ok, msg = inject(p_docs, slug)
            print(("OK   " if ok else "skip "), rel, "—", msg)
            if ok:
                docs_count += 1
        if p_landing.exists():
            ok, msg = inject(p_landing, slug)
            print(("OK   " if ok else "skip "), rel.replace("docs/", "landing/", 1), "—", msg)
            if ok:
                land_count += 1
    print(f"\nDone: {docs_count} docs/ pages updated, {land_count} landing/ pages updated.")


if __name__ == "__main__":
    main()
