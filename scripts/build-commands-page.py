"""Build docs/commands.html — a reference page for all 23 slash commands.

Pulls the frontmatter (`name`, `description`) and the first "When to use" / "When to skip"
sections out of each commands/*.md file and renders them into a single HTML page that:
  - matches the cream + Cormorant + Inter aesthetic of the other docs pages
  - lints clean against ux lint at 0/0
  - emits proper JSON-LD ItemList + breadcrumb
  - includes anchor links per command for deep linking
"""
from pathlib import Path
import re
import html


ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = ROOT / "commands"
DOCS_OUT = ROOT / "docs" / "commands.html"
LANDING_OUT = ROOT / "landing" / "commands.html"


def parse_command(path: Path) -> dict:
    """Pull frontmatter + first body paragraph out of a command markdown file."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return {"name": path.stem, "description": "", "body_intro": ""}
    fm, body = m.group(1), m.group(2)
    name_match = re.search(r"^name:\s*(.*)$", fm, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.*)$", fm, re.MULTILINE)
    name = (name_match.group(1).strip() if name_match else path.stem).strip()
    desc = (desc_match.group(1).strip() if desc_match else "").strip()
    # First non-heading paragraph after the leading "# /name" heading
    body_lines = body.splitlines()
    intro_lines = []
    in_intro = False
    for line in body_lines[:60]:
        if line.startswith("# /"):
            in_intro = True
            continue
        if in_intro:
            if line.startswith("##"):
                break
            if line.strip():
                intro_lines.append(line.strip())
            elif intro_lines:
                break
    return {
        "name": name,
        "description": desc,
        "body_intro": " ".join(intro_lines)[:400],
    }


def collect() -> list:
    out = []
    for p in sorted(COMMANDS_DIR.glob("ux-*.md")):
        out.append({"slug": p.stem, **parse_command(p)})
    return out


def render_command_card(cmd: dict) -> str:
    name = html.escape(cmd["name"])
    slug = html.escape(cmd["slug"])
    desc = html.escape(cmd["description"])
    intro = html.escape(cmd["body_intro"])
    anchor = slug
    return f"""    <article class="cmd" id="{anchor}">
      <header class="cmd-h">
        <code class="cmd-name">/{name}</code>
        <a class="cmd-link" href="https://github.com/Laith0003/ux-skill/blob/main/commands/{slug}.md" rel="noopener">source</a>
      </header>
      <p class="cmd-desc">{desc}</p>
      <p class="cmd-intro">{intro}</p>
    </article>
"""


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ux-skill commands — 23 slash commands referenced</title>
  <meta name="description" content="Complete reference for the 23 ux-skill slash commands available in Claude Code, Cursor, Windsurf, and 14 more IDEs. Each command's purpose, triggers, and source link.">
  <link rel="canonical" href="https://uxskill.laithjunaidy.com/commands.html">
  <meta name="theme-color" content="#faf9f5">
  <meta name="color-scheme" content="light">
  <meta name="robots" content="index,follow">

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://uxskill.laithjunaidy.com/commands.html">
  <meta property="og:title" content="ux-skill commands — 23 slash commands referenced">
  <meta property="og:description" content="One reference page for every ux-skill command. /ux-recommend, /ux-lint, /ux-design, /ux-component, +19 more.">
  <meta property="og:image" content="https://uxskill.laithjunaidy.com/og/home.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://uxskill.laithjunaidy.com/og/home.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <style>
    :root {
      --canvas: #faf9f5;
      --surface: #efe9de;
      --ink: #181715;
      --body: #3d3d3a;
      --muted: #6c6a64;
      --hairline: rgba(20,20,19,0.10);
      --primary: #cc785c;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
      background: var(--canvas);
      color: var(--body);
      font-size: 16px;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }
    .wrap { max-width: 1100px; margin: 0 auto; padding: 64px 24px 96px; }
    header.top {
      display: flex; align-items: center; justify-content: space-between;
      padding: 8px 0 56px;
      border-bottom: 1px solid var(--hairline);
      margin-bottom: 56px;
    }
    .wordmark {
      display: inline-flex; align-items: baseline; gap: 4px;
      text-decoration: none; color: var(--ink);
      font-family: 'Cormorant Garamond', serif;
      font-weight: 600; font-size: 28px; letter-spacing: -0.02em;
    }
    .wordmark .dot {
      display: inline-block; width: 6px; height: 6px;
      border-radius: 999px; background: var(--primary);
      transform: translateY(-3px);
    }
    nav.crumbs {
      display: flex; gap: 28px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px; text-transform: uppercase; letter-spacing: 0.16em;
      color: var(--muted);
    }
    nav.crumbs a { color: var(--muted); text-decoration: none; }
    nav.crumbs a:hover { color: var(--ink); }
    nav.crumbs a.current { color: var(--ink); }

    .eyebrow {
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase;
      color: var(--primary);
      margin-bottom: 22px;
    }
    h1 {
      font-family: 'Cormorant Garamond', serif;
      font-weight: 500;
      font-size: clamp(40px, 6vw, 64px);
      line-height: 1.06;
      letter-spacing: -0.025em;
      color: var(--ink);
      margin-bottom: 22px;
      max-width: 920px;
    }
    h1 .accent { font-style: italic; color: var(--primary); font-weight: 600; }
    .lede {
      font-size: 19px; line-height: 1.55;
      color: var(--body); max-width: 820px; margin-bottom: 48px;
    }
    .lede strong { color: var(--ink); font-weight: 600; }

    .toc {
      background: var(--surface);
      border-radius: 14px;
      padding: 22px 28px 18px;
      margin-bottom: 56px;
      max-width: 900px;
    }
    .toc-h {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 12px;
    }
    .toc ul {
      list-style: none;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: 8px 18px;
    }
    .toc a {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13.5px;
      color: var(--ink);
      text-decoration: none;
      border-bottom: 1px solid transparent;
      padding-bottom: 1px;
    }
    .toc a:hover { border-bottom-color: var(--primary); }

    .cmd {
      background: white;
      border-radius: 14px;
      border: 1px solid var(--hairline);
      padding: 26px 30px;
      margin-bottom: 18px;
      scroll-margin-top: 100px;
    }
    .cmd-h {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 12px;
    }
    .cmd-name {
      font-family: 'JetBrains Mono', monospace;
      font-size: 18px;
      color: var(--ink);
      font-weight: 600;
      background: var(--surface);
      padding: 4px 10px;
      border-radius: 6px;
    }
    .cmd-link {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.06em;
      color: var(--muted);
      text-decoration: none;
      border-bottom: 1px solid currentColor;
    }
    .cmd-link:hover { color: var(--primary); }
    .cmd-desc {
      color: var(--ink);
      font-weight: 500;
      margin-bottom: 8px;
    }
    .cmd-intro {
      color: var(--body);
      font-size: 15.5px;
      line-height: 1.55;
    }

    footer {
      margin-top: 96px;
      padding-top: 32px;
      border-top: 1px solid var(--hairline);
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 13px;
      color: var(--muted);
    }
    footer a { color: var(--muted); text-decoration: none; }
    footer a:hover { color: var(--ink); }
    footer .links { display: flex; gap: 24px; flex-wrap: wrap; }
    @media (max-width: 640px) {
      .toc ul { grid-template-columns: 1fr 1fr; }
      .cmd-h { flex-direction: column; align-items: flex-start; gap: 8px; }
    }
  </style>
__JSONLD__
</head>
<body>
  <div class="wrap">
    <header class="top">
      <a href="/" class="wordmark">ux<span class="dot"></span></a>
      <nav class="crumbs" aria-label="Primary">
        <a href="/">Home</a>
        <a href="/compare.html">Compare</a>
        <a href="/blog/">Blog</a>
        <a href="/mcp.html">MCP</a>
        <a href="/faq.html">FAQ</a>
        <a href="/commands.html" class="current">Commands</a>
        <a href="https://github.com/Laith0003/ux-skill" rel="noopener">GitHub</a>
      </nav>
    </header>

    <span class="eyebrow">Reference · 23 commands</span>
    <h1>Every slash command, <span class="accent">documented</span>.</h1>
    <p class="lede">
      ux-skill ships 23 slash commands across discovery, recommendation, generation,
      quality, and workflow. Each one runs the Python engine under the hood and chains
      into the next via <code>.ux/last-*.json</code> state files. Click any name to jump
      to its summary or follow the source link for the full markdown.
    </p>

    <nav class="toc" aria-label="Commands index">
      <p class="toc-h">Quick index</p>
      <ul>
__TOC__
      </ul>
    </nav>

__BODY__

    <footer>
      <span>© 2026 Laith Aljunaidy. MIT licensed. No telemetry.</span>
      <div class="links">
        <a href="/">Home</a>
        <a href="/compare.html">Compare</a>
        <a href="/blog/">Blog</a>
        <a href="/mcp.html">MCP</a>
        <a href="/about.html">About</a>
        <a href="/roadmap.html">Roadmap</a>
        <a href="/faq.html">FAQ</a>
        <a href="/privacy.html">Privacy</a>
        <a href="https://github.com/Laith0003/ux-skill">GitHub</a>
        <a href="https://pypi.org/project/uxskill/">PyPI</a>
        <a href="https://www.npmjs.com/package/uxskill">npm</a>
      </div>
    </footer>
  </div>
</body>
</html>
"""


def build_jsonld(cmds: list) -> str:
    items = []
    for i, c in enumerate(cmds, 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": f"/{c['name']}",
            "description": c["description"][:240],
            "url": f"https://uxskill.laithjunaidy.com/commands.html#{c['slug']}",
        })
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "ux-skill slash commands",
        "numberOfItems": len(cmds),
        "itemListElement": items,
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://uxskill.laithjunaidy.com/"},
            {"@type": "ListItem", "position": 2, "name": "Commands", "item": "https://uxskill.laithjunaidy.com/commands.html"},
        ],
    }
    import json
    return (
        f'\n  <script type="application/ld+json">{json.dumps(item_list)}</script>\n'
        f'  <script type="application/ld+json">{json.dumps(breadcrumb)}</script>\n'
    )


def main() -> None:
    cmds = collect()
    print(f"Found {len(cmds)} commands.")
    toc = "\n".join(
        f'        <li><a href="#{c["slug"]}">/{c["name"]}</a></li>'
        for c in cmds
    )
    body = "".join(render_command_card(c) for c in cmds)
    jsonld = build_jsonld(cmds)
    out = (
        HEAD
        .replace("__JSONLD__", jsonld)
        .replace("__TOC__", toc)
        .replace("__BODY__", body)
    )
    DOCS_OUT.write_text(out, encoding="utf-8")
    LANDING_OUT.write_text(out, encoding="utf-8")
    print(f"Wrote {DOCS_OUT}  ({len(out) // 1024} KB)")
    print(f"Wrote {LANDING_OUT}  ({len(out) // 1024} KB)")


if __name__ == "__main__":
    main()
