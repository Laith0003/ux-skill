"""Build docs/commands.html — a reference page for all 25 slash commands.

Pulls the frontmatter (`name`, `description`) and the first "When to use" / "When to skip"
sections out of each commands/*.md file and renders them into a single HTML page that:
  - matches the dark Saturated Cinema aesthetic of the v3 site (canvas #07080a,
    Bricolage Grotesque display, magenta scene accent #ec4899)
  - lints clean against ux lint (0 critical / 0 high)
  - emits proper JSON-LD ItemList + breadcrumb
  - includes anchor links per command for deep linking
"""
from pathlib import Path
import re
import html


ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = ROOT / "commands"
DOCS_OUT = ROOT / "docs" / "commands.html"


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
  <title>ux-skill commands — 25 slash commands referenced</title>
  <meta name="description" content="Complete reference for the 23 ux-skill slash commands available in Claude Code, Cursor, Windsurf, and 14 more IDEs. Each command's purpose, triggers, and source link.">
  <link rel="canonical" href="https://uxskill.laithjunaidy.com/commands.html">
  <meta name="theme-color" content="#07080a">
  <meta name="color-scheme" content="dark">
  <meta name="robots" content="index,follow">

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://uxskill.laithjunaidy.com/commands.html">
  <meta property="og:title" content="ux-skill commands — 25 slash commands referenced">
  <meta property="og:description" content="One reference page for every ux-skill command. /ux-recommend, /ux-lint, /ux-design, /ux-component, +19 more.">
  <meta property="og:image" content="https://uxskill.laithjunaidy.com/og/home.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://uxskill.laithjunaidy.com/og/home.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,300..800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">

  <style>
    /* =========================================================================
       UXSKILL DOCS v3 — Saturated Cinema (dark)
       Scene accent: magenta #ec4899
       ========================================================================= */
    :root {
      --canvas:        #07080a;
      --surface-1:     #0d0f12;
      --surface-2:     #14181d;
      --surface-3:     #1c2128;
      --ink:           #f6f7f9;
      --body:          #c7ccd3;
      --muted:         #8a8f96;
      --faint:         #5a5f66;
      --hairline:      rgba(246, 247, 249, 0.07);
      --hairline-2:    rgba(246, 247, 249, 0.14);

      --scene-glow:    #ec4899;
      --scene-accent:  #ec4899;
      --scene-soft:    rgba(236, 72, 153, 0.10);

      --display:   'Bricolage Grotesque', 'Inter Tight', system-ui, sans-serif;
      --body-face: 'Inter', system-ui, -apple-system, sans-serif;
      --mono:      'JetBrains Mono', ui-monospace, 'SFMono-Regular', monospace;
      --italic-face: 'Instrument Serif', Georgia, serif;

      --max-w:    1320px;
      --gutter:   clamp(20px, 5vw, 56px);

      --ease-cinema: cubic-bezier(0.16, 1, 0.3, 1);
      --t-fast:   160ms;
      --t-mid:    260ms;
      --t-slow:   520ms;
    }
    *, *::before, *::after { box-sizing: border-box; }
    html { background: var(--canvas); scroll-behavior: smooth; }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
    body {
      margin: 0;
      background: var(--canvas);
      color: var(--body);
      font-family: var(--body-face);
      font-size: 16px;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
    }
    a { color: var(--ink); text-decoration: underline; text-decoration-color: var(--hairline-2); text-underline-offset: 3px; transition: text-decoration-color var(--t-fast) var(--ease-cinema), color var(--t-fast) var(--ease-cinema); }
    a:hover, a:focus-visible { text-decoration-color: var(--scene-accent); }
    a:focus-visible { outline: 2px solid var(--scene-glow); outline-offset: 3px; border-radius: 2px; }
    button { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; }

    .skip-link {
      position: absolute; top: -40px; left: 8px;
      background: var(--surface-2); color: var(--ink);
      padding: 12px 18px; border-radius: 8px;
      font-family: var(--mono); font-size: 12px;
      border: 1px solid var(--hairline-2);
      z-index: 200;
    }
    .skip-link:focus { top: 8px; }

    /* ===== NAV ===== */
    .nav {
      position: fixed; top: 0; left: 0; right: 0;
      z-index: 80;
      padding: 14px 0;
      transition: backdrop-filter var(--t-mid) var(--ease-cinema),
                  background-color var(--t-mid) var(--ease-cinema),
                  border-color var(--t-mid) var(--ease-cinema);
      border-bottom: 1px solid transparent;
    }
    .nav.is-scrolled {
      background: rgba(7, 8, 10, 0.72);
      backdrop-filter: saturate(140%) blur(18px);
      -webkit-backdrop-filter: saturate(140%) blur(18px);
      border-bottom-color: var(--hairline);
    }
    .nav__inner {
      max-width: var(--max-w);
      margin: 0 auto;
      padding: 0 var(--gutter);
      display: flex; align-items: center; justify-content: space-between;
      gap: 18px;
    }
    .wordmark {
      font-family: var(--display);
      font-variation-settings: 'wdth' 92, 'opsz' 96, 'wght' 620;
      font-size: 22px;
      letter-spacing: -0.04em;
      line-height: 1;
      color: var(--ink);
      display: inline-flex;
      align-items: baseline;
      gap: 2px;
      text-decoration: none;
    }
    .wordmark:hover { text-decoration: none; }
    .wordmark__dot {
      display: inline-block;
      width: 6px; height: 6px;
      border-radius: 2px;
      background: linear-gradient(135deg, #06b6d4, #ec4899);
      margin-left: 4px;
      transform: translateY(-2px);
    }
    .nav__links { display: none; gap: 26px; align-items: center; }
    .nav__link {
      font-family: var(--mono);
      font-size: 12px;
      font-weight: 500;
      color: var(--muted);
      letter-spacing: 0.04em;
      text-transform: lowercase;
      text-decoration: none;
      transition: color var(--t-fast) var(--ease-cinema);
    }
    .nav__link:hover, .nav__link:focus-visible { color: var(--ink); text-decoration: none; }
    .nav__link.is-current { color: var(--ink); }
    .nav__link:focus-visible { outline: 2px solid var(--scene-glow); outline-offset: 6px; border-radius: 3px; }
    .cta-pill {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 9px 14px; min-height: 36px;
      border-radius: 10px;
      background: var(--ink); color: var(--canvas);
      font-family: var(--mono); font-size: 12px; font-weight: 500;
      text-decoration: none;
      transition: transform var(--t-mid) var(--ease-cinema),
                  background-color var(--t-fast) var(--ease-cinema);
    }
    .cta-pill:hover, .cta-pill:focus-visible { transform: translateY(-1px); background: #ffffff; text-decoration: none; }
    .cta-pill:active { transform: translateY(0); }
    .cta-pill:focus-visible { outline: 2px solid var(--scene-glow); outline-offset: 4px; }

    .nav__menu-btn {
      display: inline-flex; width: 40px; height: 40px;
      align-items: center; justify-content: center;
      border-radius: 8px;
      border: 1px solid var(--hairline-2);
      color: var(--ink);
    }
    .nav__menu-btn:focus-visible { outline: 2px solid var(--scene-glow); outline-offset: 3px; }
    .nav__drawer {
      position: fixed; inset: 0;
      z-index: 90;
      display: flex; flex-direction: column;
      padding: 80px var(--gutter) 40px;
      opacity: 0; pointer-events: none;
      transition: opacity var(--t-mid) var(--ease-cinema);
      background-color: rgba(7, 8, 10, 0.94);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
    }
    .nav__drawer.is-open { opacity: 1; pointer-events: auto; }
    .nav__drawer a {
      display: block;
      font-family: var(--display);
      font-variation-settings: 'wdth' 88, 'wght' 560;
      font-size: 32px;
      color: var(--ink);
      padding: 14px 0;
      border-bottom: 1px solid var(--hairline);
      letter-spacing: -0.02em;
      text-decoration: none;
    }
    .nav__drawer .nav__drawer-close {
      position: absolute; top: 18px; right: var(--gutter);
      width: 44px; height: 44px;
      border-radius: 8px;
      border: 1px solid var(--hairline-2);
      display: inline-flex; align-items: center; justify-content: center;
      background: transparent; color: var(--ink);
    }
    @media (min-width: 768px) {
      .nav__links { display: flex; }
      .nav__menu-btn { display: none; }
    }

    /* ===== PAGE ===== */
    .page {
      max-width: 1100px;
      margin: 0 auto;
      padding: clamp(120px, 16vw, 168px) var(--gutter) clamp(80px, 12vw, 140px);
    }

    .crumbs {
      display: flex; gap: 18px; flex-wrap: wrap;
      font-family: var(--mono);
      font-size: 11px; letter-spacing: 0.06em;
      text-transform: lowercase;
      color: var(--muted);
      margin-bottom: 40px;
    }
    .crumbs a { color: var(--muted); text-decoration: none; }
    .crumbs a:hover { color: var(--ink); }
    .crumbs a.is-current { color: var(--ink); }

    .eyebrow {
      font-family: var(--mono);
      font-size: 11.5px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--muted);
      display: inline-flex; align-items: center; gap: 10px;
      margin-bottom: 22px;
    }
    .eyebrow::before {
      content: ''; display: inline-block;
      width: 22px; height: 1px;
      background: currentColor;
    }

    h1, h2 {
      font-family: var(--display);
      font-weight: 600;
      font-variation-settings: 'wdth' 88, 'opsz' 96, 'wght' 580;
      margin: 0;
      line-height: 1.04;
      letter-spacing: -0.028em;
      color: var(--ink);
    }
    h1 {
      font-size: clamp(42px, 6.5vw, 68px);
      font-variation-settings: 'wdth' 84, 'opsz' 96, 'wght' 600;
      letter-spacing: -0.034em;
      margin-bottom: 22px;
      max-width: 920px;
    }
    h1 .accent {
      font-family: var(--italic-face);
      font-style: italic;
      font-weight: 400;
      color: var(--scene-accent);
      letter-spacing: -0.015em;
    }
    .lede {
      font-size: 19px;
      line-height: 1.55;
      color: var(--body);
      max-width: 820px;
      margin-bottom: 48px;
    }
    .lede strong { color: var(--ink); font-weight: 600; }
    .lede code {
      font-family: var(--mono);
      font-size: 13px;
      background: var(--surface-2);
      padding: 1px 6px;
      border-radius: 4px;
      color: var(--ink);
      border: 1px solid var(--hairline);
    }

    /* TOC */
    .toc {
      background: var(--surface-1);
      border: 1px solid var(--hairline);
      border-radius: 14px;
      padding: 22px 28px 18px;
      margin-bottom: 56px;
      max-width: 900px;
    }
    .toc-h {
      font-family: var(--mono);
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
      padding: 0;
      margin: 0;
    }
    .toc a {
      font-family: var(--mono);
      font-size: 13.5px;
      color: var(--ink);
      text-decoration: none;
      border-bottom: 1px solid transparent;
      padding-bottom: 1px;
      transition: border-color var(--t-fast) var(--ease-cinema), color var(--t-fast) var(--ease-cinema);
    }
    .toc a:hover { border-bottom-color: var(--scene-accent); color: var(--scene-accent); }

    /* Command card */
    .cmd {
      background: var(--surface-1);
      border: 1px solid var(--hairline);
      border-radius: 14px;
      padding: 26px 30px;
      margin-bottom: 18px;
      scroll-margin-top: 100px;
      transition: border-color var(--t-fast) var(--ease-cinema), background-color var(--t-fast) var(--ease-cinema);
    }
    .cmd:hover { border-color: var(--hairline-2); background: var(--surface-2); }
    .cmd-h {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 12px;
    }
    .cmd-name {
      font-family: var(--mono);
      font-size: 17px;
      color: var(--ink);
      font-weight: 600;
      background: var(--surface-2);
      padding: 5px 10px;
      border-radius: 6px;
      border: 1px solid var(--hairline);
    }
    .cmd-link {
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: 0.06em;
      color: var(--muted);
      text-decoration: none;
      border-bottom: 1px solid currentColor;
      transition: color var(--t-fast) var(--ease-cinema);
    }
    .cmd-link:hover { color: var(--scene-accent); }
    .cmd-desc {
      color: var(--ink);
      font-weight: 500;
      margin: 0 0 8px;
    }
    .cmd-intro {
      color: var(--body);
      font-size: 15.5px;
      line-height: 1.55;
      margin: 0;
    }

    @media (max-width: 640px) {
      .toc ul { grid-template-columns: 1fr 1fr; }
      .cmd-h { flex-direction: column; align-items: flex-start; gap: 8px; }
    }

    /* ===== FOOTER ===== */
    .footer {
      padding: 88px 0 56px;
      border-top: 1px solid var(--hairline);
      background: var(--surface-1);
    }
    .footer__inner {
      max-width: var(--max-w);
      margin: 0 auto;
      padding: 0 var(--gutter);
      display: grid;
      grid-template-columns: 1fr;
      gap: 44px;
    }
    .footer__col-h {
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 14px;
    }
    .footer__col ul { list-style: none; padding: 0; margin: 0; }
    .footer__col li { margin-bottom: 10px; padding: 0; }
    .footer__link {
      color: var(--body);
      font-size: 13.5px;
      text-decoration: none;
      transition: color var(--t-fast) var(--ease-cinema);
    }
    .footer__link:hover, .footer__link:focus-visible { color: var(--ink); text-decoration: none; }
    .footer__link:focus-visible { outline: 2px solid var(--scene-glow); outline-offset: 3px; border-radius: 2px; }
    .footer__tagline {
      margin-top: 12px;
      font-size: 13.5px;
      color: var(--body);
      max-width: 320px;
    }
    .footer__bottom {
      max-width: var(--max-w);
      margin: 64px auto 0;
      padding: 28px var(--gutter) 0;
      display: flex; flex-wrap: wrap;
      gap: 16px;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--hairline);
      font-family: var(--mono);
      font-size: 11.5px;
      color: var(--muted);
    }
    @media (min-width: 720px) {
      .footer__inner { grid-template-columns: 1.4fr 1fr 1fr 1fr 1fr; gap: 40px; }
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
      }
    }
  </style>
__JSONLD__
</head>
<body>

<a href="#main" class="skip-link">Skip to content</a>

<header class="nav" id="nav">
  <div class="nav__inner">
    <a href="/" class="wordmark" aria-label="uxskill home">
      uxskill<span class="wordmark__dot" aria-hidden="true"></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
      <a class="nav__link" href="/compare.html">compare</a>
      <a class="nav__link" href="/about.html">about</a>
      <a class="nav__link" href="/roadmap.html">roadmap</a>
      <a class="nav__link" href="/faq.html">faq</a>
      <a class="nav__link" href="/mcp.html">mcp</a>
      <a class="nav__link is-current" href="/commands.html">commands</a>
      <a class="nav__link" href="/blog/">blog</a>
    </nav>
    <a href="https://github.com/Laith0003/ux-skill" class="cta-pill" rel="noopener">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
      <span>GitHub</span>
    </a>
    <button type="button" class="nav__menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav-drawer" id="nav-menu-btn">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<div class="nav__drawer" id="nav-drawer" role="dialog" aria-modal="true" aria-label="Site menu" aria-hidden="true">
  <button type="button" class="nav__drawer-close" aria-label="Close menu" id="nav-drawer-close">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
  </button>
  <a href="/compare.html">Compare</a>
  <a href="/about.html">About</a>
  <a href="/roadmap.html">Roadmap</a>
  <a href="/faq.html">FAQ</a>
  <a href="/mcp.html">MCP</a>
  <a href="/commands.html">Commands</a>
  <a href="/blog/">Blog</a>
  <a href="/privacy.html">Privacy</a>
  <a href="https://github.com/Laith0003/ux-skill" rel="noopener">GitHub</a>
</div>

<main id="main">
  <div class="page">
    <nav class="crumbs" aria-label="Breadcrumbs">
      <a href="/">home</a>
      <a href="/compare.html">compare</a>
      <a href="/blog/">blog</a>
      <a href="/mcp.html">mcp</a>
      <a href="/faq.html">faq</a>
      <a href="/commands.html" class="is-current">commands</a>
    </nav>

    <span class="eyebrow">Reference &middot; 25 commands</span>
    <h1>Every slash command, <span class="accent">documented</span>.</h1>
    <p class="lede">
      ux-skill ships 25 slash commands across discovery, recommendation, generation,
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
  </div>
</main>

<footer class="footer" role="contentinfo">
  <div class="footer__inner">
    <div class="footer__col">
      <a href="/" class="wordmark" aria-label="uxskill home">uxskill<span class="wordmark__dot" aria-hidden="true"></span></a>
      <p class="footer__tagline">Design intelligence for AI coding. Built so every model session ships work that does not look generated.</p>
    </div>
    <div class="footer__col">
      <p class="footer__col-h">Plugin</p>
      <ul>
        <li><a class="footer__link" href="/about.html">About</a></li>
        <li><a class="footer__link" href="/compare.html">Compare</a></li>
        <li><a class="footer__link" href="/roadmap.html">Roadmap</a></li>
        <li><a class="footer__link" href="/faq.html">FAQ</a></li>
        <li><a class="footer__link" href="/mcp.html">MCP</a></li>
        <li><a class="footer__link" href="/privacy.html">Privacy</a></li>
      </ul>
    </div>
    <div class="footer__col">
      <p class="footer__col-h">Reading</p>
      <ul>
        <li><a class="footer__link" href="/blog/">Blog index</a></li>
        <li><a class="footer__link" href="/blog/dark-editorial-cinema-design.html">Dark editorial cinema</a></li>
        <li><a class="footer__link" href="/blog/best-claude-code-design-skills-2026.html">Best Claude Code design skills</a></li>
        <li><a class="footer__link" href="/blog/anti-ai-slop-claude-skills.html">Anti AI-slop skills</a></li>
      </ul>
    </div>
    <div class="footer__col">
      <p class="footer__col-h">Reference</p>
      <ul>
        <li><a class="footer__link" href="/commands.html">Commands</a></li>
        <li><a class="footer__link" href="/blog/ai-design-fingerprints-list.html">AI design fingerprints</a></li>
        <li><a class="footer__link" href="/blog/regex-linter-for-ai-coding.html">Regex linter for AI coding</a></li>
      </ul>
    </div>
    <div class="footer__col">
      <p class="footer__col-h">Get it</p>
      <ul>
        <li><a class="footer__link" href="https://github.com/Laith0003/ux-skill" rel="noopener">GitHub</a></li>
        <li><a class="footer__link" href="https://pypi.org/project/uxskill/" rel="noopener">PyPI</a></li>
        <li><a class="footer__link" href="https://www.npmjs.com/package/uxskill" rel="noopener">npm</a></li>
      </ul>
    </div>
  </div>
  <div class="footer__bottom">
    <span>MIT licensed &middot; No telemetry &middot; No account</span>
    <span>&copy; 2026 Laith Aljunaidy</span>
  </div>
</footer>

<script>
(function () {
  'use strict';
  var nav = document.getElementById('nav');
  function onScroll() {
    if (window.scrollY > 24) nav.classList.add('is-scrolled');
    else nav.classList.remove('is-scrolled');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var menuBtn = document.getElementById('nav-menu-btn');
  var drawer = document.getElementById('nav-drawer');
  var drawerClose = document.getElementById('nav-drawer-close');
  function openDrawer() {
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    menuBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
  function closeDrawer() {
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    menuBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
  if (menuBtn) menuBtn.addEventListener('click', openDrawer);
  if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer.classList.contains('is-open')) closeDrawer();
  });
  Array.prototype.forEach.call(drawer.querySelectorAll('a'), function (a) {
    a.addEventListener('click', closeDrawer);
  });
})();
</script>

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
    print(f"Wrote {DOCS_OUT}  ({len(out) // 1024} KB)")


if __name__ == "__main__":
    main()
