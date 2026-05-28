"""Add a 'Related reads' section to every blog post before its footer.

One-shot script: idempotent — if the marker is already present, skip the post.
"""
from pathlib import Path
import re


BLOG_DIR = Path(__file__).resolve().parent.parent / "docs" / "blog"

POSTS = {
    "vs-ui-ux-pro-max": "ui-ux-pro-max alternative",
    "anti-ai-slop-claude-skills": "Anti-AI-slop tools for Claude Code",
    "best-claude-code-design-skills-2026": "Best Claude Code design skills 2026",
    "cursor-design-plugin": "Cursor design plugin",
    "python-design-system-generator": "Python design system generator",
    "claude-code-marketplace-best-plugins": "Best Claude Code marketplace plugins",
    "ai-design-fingerprints-list": "35 AI design fingerprints",
    "figma-vs-ux-skill": "Figma vs ux-skill",
    "windsurf-design-rules": "Windsurf design rules",
    "monorepo-design-system-ai-coding": "Monorepo design system for AI coding",
    "regex-linter-for-ai-coding": "Regex linter for AI coding",
    "dark-editorial-cinema-design": "Dark editorial cinema design",
    "mcp-server-design-intelligence": "MCP server design intelligence",
    "motion-presets-framer-gsap-css": "Motion presets: Framer, GSAP, CSS",
    "dogfooding-design-engine": "Dogfooding ux-skill",
    "zed-design-plugin": "Zed design plugin",
    "github-copilot-design-rules": "GitHub Copilot design rules",
    "jetbrains-ai-design-system": "JetBrains AI design system",
    "ai-design-system-cli": "AI design system CLI",
    "claude-desktop-mcp-design": "Claude Desktop MCP design intelligence",
}

# Each post maps to 4 related posts.
RELATIONS = {
    "vs-ui-ux-pro-max": ["anti-ai-slop-claude-skills", "best-claude-code-design-skills-2026",
                         "claude-code-marketplace-best-plugins", "figma-vs-ux-skill"],
    "anti-ai-slop-claude-skills": ["vs-ui-ux-pro-max", "best-claude-code-design-skills-2026",
                                   "ai-design-fingerprints-list", "regex-linter-for-ai-coding"],
    "best-claude-code-design-skills-2026": ["vs-ui-ux-pro-max", "anti-ai-slop-claude-skills",
                                            "claude-code-marketplace-best-plugins", "figma-vs-ux-skill"],
    "cursor-design-plugin": ["windsurf-design-rules", "claude-code-marketplace-best-plugins",
                             "anti-ai-slop-claude-skills", "python-design-system-generator"],
    "python-design-system-generator": ["mcp-server-design-intelligence", "regex-linter-for-ai-coding",
                                       "monorepo-design-system-ai-coding", "dogfooding-design-engine"],
    "claude-code-marketplace-best-plugins": ["best-claude-code-design-skills-2026", "vs-ui-ux-pro-max",
                                             "anti-ai-slop-claude-skills", "cursor-design-plugin"],
    "ai-design-fingerprints-list": ["anti-ai-slop-claude-skills", "regex-linter-for-ai-coding",
                                    "dark-editorial-cinema-design", "dogfooding-design-engine"],
    "figma-vs-ux-skill": ["vs-ui-ux-pro-max", "best-claude-code-design-skills-2026",
                          "python-design-system-generator", "monorepo-design-system-ai-coding"],
    "windsurf-design-rules": ["cursor-design-plugin", "claude-code-marketplace-best-plugins",
                              "anti-ai-slop-claude-skills", "mcp-server-design-intelligence"],
    "monorepo-design-system-ai-coding": ["python-design-system-generator", "figma-vs-ux-skill",
                                         "dogfooding-design-engine", "regex-linter-for-ai-coding"],
    "regex-linter-for-ai-coding": ["ai-design-fingerprints-list", "anti-ai-slop-claude-skills",
                                   "python-design-system-generator", "dogfooding-design-engine"],
    "dark-editorial-cinema-design": ["ai-design-fingerprints-list", "dogfooding-design-engine",
                                     "motion-presets-framer-gsap-css", "python-design-system-generator"],
    "mcp-server-design-intelligence": ["python-design-system-generator", "windsurf-design-rules",
                                       "cursor-design-plugin", "dogfooding-design-engine"],
    "motion-presets-framer-gsap-css": ["dark-editorial-cinema-design", "dogfooding-design-engine",
                                       "ai-design-fingerprints-list", "anti-ai-slop-claude-skills"],
    "dogfooding-design-engine": ["dark-editorial-cinema-design", "ai-design-fingerprints-list",
                                 "regex-linter-for-ai-coding", "python-design-system-generator"],
    "zed-design-plugin": ["cursor-design-plugin", "windsurf-design-rules",
                          "github-copilot-design-rules", "jetbrains-ai-design-system"],
    "github-copilot-design-rules": ["cursor-design-plugin", "jetbrains-ai-design-system",
                                    "regex-linter-for-ai-coding", "ai-design-fingerprints-list"],
    "jetbrains-ai-design-system": ["cursor-design-plugin", "ai-design-system-cli",
                                   "monorepo-design-system-ai-coding", "python-design-system-generator"],
    "ai-design-system-cli": ["python-design-system-generator", "claude-desktop-mcp-design",
                             "regex-linter-for-ai-coding", "dogfooding-design-engine"],
    "claude-desktop-mcp-design": ["mcp-server-design-intelligence", "ai-design-system-cli",
                                  "cursor-design-plugin", "anti-ai-slop-claude-skills"],
}


def render_block(slug: str) -> str:
    rels = RELATIONS[slug]
    items = "\n".join(
        f'        <li><a href="/blog/{r}.html">{POSTS[r]}</a></li>'
        for r in rels
    )
    return f"""
  <aside class="related-reads" aria-label="Related reads">
    <div class="related-reads-inner">
      <h2 class="related-reads-h">Related reads</h2>
      <ul>
{items}
      </ul>
    </div>
  </aside>
  <style>
    .related-reads {{
      max-width: 880px; margin: 80px auto 0 auto; padding: 32px 24px 8px;
      border-top: 1px solid rgba(20,20,19,0.10);
    }}
    .related-reads-h {{
      font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase;
      color: #6c6a64; margin-bottom: 16px; font-family: 'JetBrains Mono', ui-monospace, monospace;
    }}
    .related-reads ul {{
      list-style: none; padding: 0; margin: 0;
      display: grid; grid-template-columns: 1fr 1fr; gap: 12px 32px;
    }}
    .related-reads li {{ font-size: 15px; line-height: 1.5; }}
    .related-reads a {{
      color: inherit; text-decoration: none;
      border-bottom: 1px solid rgba(20,20,19,0.18);
      padding-bottom: 2px; transition: border-color .15s ease;
    }}
    .related-reads a:hover {{ border-color: currentColor; }}
    @media (max-width: 640px) {{
      .related-reads ul {{ grid-template-columns: 1fr; }}
    }}
    @media (prefers-color-scheme: dark) {{
      .related-reads {{ border-top-color: rgba(255,255,255,0.12); }}
      .related-reads a {{ border-bottom-color: rgba(255,255,255,0.20); }}
    }}
  </style>
"""


MARKER = "<aside class=\"related-reads\""


def inject(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    slug = path.stem
    if slug not in RELATIONS:
        return False, "no relations defined"
    if MARKER in text:
        return False, "already has related-reads"
    block = render_block(slug)
    # Insert immediately BEFORE <footer> (close out main content first).
    m = re.search(r"(\n\s*<footer\b)", text)
    if not m:
        return False, "no <footer> tag found"
    new_text = text[: m.start()] + block + text[m.start():]
    path.write_text(new_text, encoding="utf-8")
    return True, "injected"


def main() -> None:
    for slug in RELATIONS:
        p = BLOG_DIR / f"{slug}.html"
        if not p.exists():
            print(f"SKIP missing {slug}")
            continue
        ok, msg = inject(p)
        print(("OK   " if ok else "skip "), slug, "—", msg)


if __name__ == "__main__":
    main()
