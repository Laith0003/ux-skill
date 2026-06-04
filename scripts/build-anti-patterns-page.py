"""Generate docs/anti-patterns.html: a browseable, searchable reference
page for every rule in data/anti-patterns.json.

High-value because:
- Single page lists every fingerprint of AI-generated design slop.
- Each rule has its own anchor → linkable from blog posts & wiki.
- Massive long-tail SEO surface (each rule's name is a search term).
- The linter README at /docs/blog/anti-ai-slop-claude-skills.html can
  link to specific rules.

Re-run after data/anti-patterns.json changes.
"""
from pathlib import Path
import json
import html
import re


def sanitize_dashes(s):
    """Strip em/en dashes from rendered rule text (no-AI-tell house rule).
    em-dash -> colon; en-dash (numeric range) -> hyphen."""
    s = re.sub(r'\s*—\s*', ': ', s)
    s = re.sub(r'\s*–\s*', '-', s)
    return s


ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "anti-patterns.json"
OUT = ROOT / "docs" / "anti-patterns.html"
LANDING_OUT = ROOT / "landing" / "anti-patterns.html"


SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SEVERITY_BADGE = {
    "high":   ("ff5d5d", "FFFFFF", "HIGH"),
    "medium": ("e8a63c", "07080a", "MED"),
    "low":    ("8be9b1", "07080a", "LOW"),
}


def load_rules():
    with SRC.open(encoding="utf-8") as f:
        raw = json.load(f)
    # Real schema is {"_meta": {...}, "entries": [...]}; legacy may be a flat
    # list or {"rules": [...]}.
    if isinstance(raw, dict):
        rules = raw.get("entries") or raw.get("rules") or []
        version = (raw.get("_meta") or {}).get("version") or raw.get("version")
        return rules, version
    if isinstance(raw, list):
        return raw, None
    return [], None


def slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_-]+", "-", s).strip("-").lower()
    return s


def render_rule_card(rule):
    rid = html.escape(str(rule.get("id", "")))
    name = html.escape(str(rule.get("name", rid)))
    category = html.escape(str(rule.get("category", "")))
    severity = (rule.get("severity") or "medium").lower()
    sev_color, sev_ink, sev_label = SEVERITY_BADGE.get(severity, SEVERITY_BADGE["medium"])
    # Real schema uses "detection.regex" + "why" + "fix"; legacy uses
    # "description", "why_bad", "example_bad", "example_good".
    detection = rule.get("detection") or {}
    desc = sanitize_dashes(html.escape(str(rule.get("description") or rule.get("detection_summary") or "")))
    why = sanitize_dashes(html.escape(str(rule.get("why_bad") or rule.get("why", ""))))
    fix = sanitize_dashes(html.escape(str(rule.get("fix", ""))))
    bad = (
        rule.get("example_bad")
        or (detection.get("example_bad") if isinstance(detection, dict) else "")
        or ""
    )
    good = (
        rule.get("example_good")
        or (detection.get("example_good") if isinstance(detection, dict) else "")
        or ""
    )
    # Try to surface the regex itself as a "detection" peek.
    regex_peek = ""
    if isinstance(detection, dict):
        rx = detection.get("regex") or detection.get("pattern")
        if rx:
            regex_peek = f'<pre class="ap-pre ap-pre--rx"><code>{html.escape(str(rx))[:240]}</code></pre>'
    applies = (
        rule.get("applies_to")
        or (detection.get("applies_to") if isinstance(detection, dict) else [])
        or []
    )
    applies_pills = "".join(
        f'<span class="ap-pill">{html.escape(str(a))}</span>' for a in applies
    )
    bad_block = f'<pre class="ap-pre ap-pre--bad"><code>{html.escape(bad)}</code></pre>' if bad else ""
    good_block = f'<pre class="ap-pre ap-pre--good"><code>{html.escape(good)}</code></pre>' if good else ""
    why_block = f'<div class="ap-why"><span class="ap-sub">Why bad</span><p>{why}</p></div>' if why else ""
    fix_block = f'<div class="ap-fix"><span class="ap-sub">Fix</span><p>{fix}</p></div>' if fix else ""
    return f'''
    <article class="ap-card" id="{rid}">
      <header class="ap-head">
        <span class="ap-id">#{rid}</span>
        <span class="ap-sev" style="background:#{sev_color};color:#{sev_ink}">{sev_label}</span>
        <span class="ap-cat">{category}</span>
        <h3 class="ap-name">{name}</h3>
        <div class="ap-applies">{applies_pills}</div>
      </header>
      <p class="ap-desc">{desc}</p>
      {why_block}
      {fix_block}
      {regex_peek}
      <div class="ap-examples">
        {bad_block}
        {good_block}
      </div>
      <a href="#{rid}" class="ap-anchor" aria-label="Link to rule #{rid}">link</a>
    </article>
    '''


def build_html(rules, version):
    rules_sorted = sorted(
        rules,
        key=lambda r: (
            SEVERITY_ORDER.get((r.get("severity") or "medium").lower(), 9),
            (r.get("category") or "").lower(),
            (r.get("id") or ""),
        ),
    )
    categories = sorted({(r.get("category") or "Uncategorized") for r in rules_sorted})
    cards = "\n".join(render_rule_card(r) for r in rules_sorted)
    cat_chips = "".join(
        f'<button type="button" class="ap-chip" data-cat="{html.escape(c)}">{html.escape(c)}</button>'
        for c in categories
    )
    total = len(rules_sorted)
    high = sum(1 for r in rules_sorted if (r.get("severity") or "").lower() == "high")
    med = sum(1 for r in rules_sorted if (r.get("severity") or "").lower() == "medium")
    low = sum(1 for r in rules_sorted if (r.get("severity") or "").lower() == "low")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{total} anti-pattern rules · the ux-skill linter catalogue</title>
<meta name="description" content="The complete catalogue of {total} AI design-slop fingerprints caught by the ux-skill linter. {high} high, {med} medium, {low} low severity. Each rule includes regex, why it's bad, and the fix.">
<link rel="canonical" href="https://uxskill.laithjunaidy.com/anti-patterns.html">
<link rel="alternate" hreflang="en" href="https://uxskill.laithjunaidy.com/anti-patterns.html">
<meta property="og:title" content="{total} anti-pattern rules · the ux-skill linter catalogue">
<meta property="og:description" content="Every fingerprint of AI-generated design slop, named and indexed. Browse {total} rules from the deterministic linter that runs in &lt;50ms.">
<meta property="og:url" content="https://uxskill.laithjunaidy.com/anti-patterns.html">
<meta property="og:image" content="https://uxskill.laithjunaidy.com/og/home.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{total} anti-pattern rules · the ux-skill linter">
<meta name="twitter:description" content="The complete linter catalogue. {high} high · {med} medium · {low} low severity.">
<meta name="twitter:image" content="https://uxskill.laithjunaidy.com/og/home.png">

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"{total} anti-pattern rules · ux-skill linter","url":"https://uxskill.laithjunaidy.com/anti-patterns.html","description":"Browseable index of every AI-design-slop fingerprint caught by the ux-skill deterministic linter.","isPartOf":{{"@type":"WebSite","name":"ux-skill","url":"https://uxskill.laithjunaidy.com/"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://uxskill.laithjunaidy.com/"}},{{"@type":"ListItem","position":2,"name":"Anti-pattern rules","item":"https://uxskill.laithjunaidy.com/anti-patterns.html"}}]}}
</script>

<style>
  :root {{
    --canvas: #07080a;
    --surface-1: #0e1014;
    --surface-2: #14171c;
    --ink: #f6f7f9;
    --body: #c0c3c9;
    --muted: #8a8f96;
    --hairline: rgba(255,255,255,0.08);
    --hairline-2: rgba(255,255,255,0.16);
    --accent: #cc785c;
    --display: 'Bricolage Grotesque', system-ui, sans-serif;
    --sans: 'Inter', system-ui, sans-serif;
    --mono: 'JetBrains Mono', ui-monospace, monospace;
    --t-fast: 0.18s;
    --ease: cubic-bezier(0.22, 1, 0.36, 1);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: var(--canvas); color: var(--ink); font-family: var(--sans); line-height: 1.55; overflow-x: clip; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  h1, h2, h3 {{ font-family: var(--display); letter-spacing: -0.02em; }}
  .container {{ max-width: 1180px; margin: 0 auto; padding: 0 clamp(20px, 4vw, 48px); }}
  .top {{ padding: 64px 0 32px; }}
  .top__eyebrow {{ font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.16em; color: var(--muted); text-transform: uppercase; margin-bottom: 14px; }}
  .top__title {{ font-size: clamp(36px, 6vw, 64px); line-height: 1.04; font-weight: 600; margin-bottom: 22px; }}
  .top__title em {{ font-style: italic; color: var(--accent); }}
  .top__lead {{ color: var(--body); font-size: 17px; max-width: 720px; line-height: 1.6; }}
  .top__stats {{ display: flex; gap: 18px; flex-wrap: wrap; margin-top: 28px; }}
  .top__stat {{ display: inline-flex; align-items: baseline; gap: 8px; padding: 8px 14px; border: 1px solid var(--hairline); border-radius: 999px; font-family: var(--mono); font-size: 12px; color: var(--body); }}
  .top__stat b {{ color: var(--ink); font-weight: 700; }}

  .toolbar {{ padding: 24px 0; border-top: 1px solid var(--hairline); border-bottom: 1px solid var(--hairline); position: sticky; top: 0; background: rgba(7,8,10,0.92); backdrop-filter: blur(8px); z-index: 10; }}
  .toolbar__row {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }}
  .ap-search {{ flex: 1; min-width: 260px; padding: 10px 14px; background: var(--surface-1); border: 1px solid var(--hairline); border-radius: 8px; color: var(--ink); font-family: var(--sans); font-size: 14px; }}
  .ap-search:focus {{ outline: none; border-color: var(--accent); }}
  .ap-chip {{ background: var(--surface-1); border: 1px solid var(--hairline); color: var(--body); padding: 6px 12px; border-radius: 999px; font-family: var(--mono); font-size: 10.5px; letter-spacing: 0.08em; text-transform: uppercase; cursor: pointer; }}
  .ap-chip.is-active {{ background: var(--accent); color: var(--canvas); border-color: var(--accent); }}
  .ap-chip:hover {{ border-color: var(--hairline-2); }}

  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 18px; padding: 36px 0 80px; }}
  .ap-card {{ position: relative; background: var(--surface-1); border: 1px solid var(--hairline); border-radius: 14px; padding: 24px; }}
  .ap-head {{ display: grid; grid-template-columns: auto auto auto; gap: 8px 12px; align-items: center; margin-bottom: 14px; }}
  .ap-id {{ font-family: var(--mono); font-size: 11px; color: var(--muted); letter-spacing: 0.04em; }}
  .ap-sev {{ font-family: var(--mono); font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; letter-spacing: 0.08em; }}
  .ap-cat {{ font-family: var(--mono); font-size: 10px; color: var(--muted); letter-spacing: 0.10em; text-transform: uppercase; }}
  .ap-name {{ grid-column: 1 / -1; font-size: 20px; font-weight: 600; color: var(--ink); line-height: 1.2; }}
  .ap-applies {{ grid-column: 1 / -1; display: flex; gap: 6px; flex-wrap: wrap; }}
  .ap-pill {{ font-family: var(--mono); font-size: 10px; color: var(--accent); padding: 2px 7px; border: 1px solid var(--hairline-2); border-radius: 4px; text-transform: uppercase; letter-spacing: 0.08em; }}
  .ap-desc {{ color: var(--body); font-size: 14.5px; margin-bottom: 14px; }}
  .ap-sub {{ display: inline-block; font-family: var(--mono); font-size: 9.5px; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 4px; }}
  .ap-why, .ap-fix {{ margin-bottom: 12px; }}
  .ap-why p {{ color: var(--body); font-size: 13.5px; }}
  .ap-fix p {{ color: var(--ink); font-size: 13.5px; }}
  .ap-examples {{ display: grid; gap: 8px; }}
  .ap-pre {{ background: var(--canvas); border: 1px solid var(--hairline); border-radius: 8px; padding: 10px 12px; font-family: var(--mono); font-size: 11.5px; line-height: 1.45; color: var(--body); overflow-x: auto; }}
  .ap-pre--bad {{ border-left: 2px solid #ff5d5d; }}
  .ap-pre--good {{ border-left: 2px solid #8be9b1; }}
  .ap-pre--rx {{ border-left: 2px solid var(--accent); color: var(--muted); font-size: 11px; margin-bottom: 8px; }}
  .ap-anchor {{ position: absolute; top: 18px; right: 18px; font-family: var(--mono); font-size: 10px; color: var(--muted); padding: 2px 6px; border: 1px solid var(--hairline); border-radius: 4px; opacity: 0; transition: opacity var(--t-fast) var(--ease); }}
  .ap-card:hover .ap-anchor, .ap-card:focus-within .ap-anchor {{ opacity: 1; }}
  .ap-card.is-hidden {{ display: none; }}

  .nav {{ padding: 22px 0; border-bottom: 1px solid var(--hairline); }}
  .nav__row {{ display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }}
  .nav__brand {{ font-family: var(--display); font-size: 18px; font-weight: 700; letter-spacing: -0.02em; color: var(--ink); }}
  .nav__link {{ font-family: var(--mono); font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }}
  .nav__link:hover {{ color: var(--ink); }}

  footer {{ padding: 40px 0 80px; border-top: 1px solid var(--hairline); color: var(--muted); font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.08em; text-align: center; }}

  @media (max-width: 640px) {{
    .grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<header class="nav">
  <div class="container nav__row">
    <a class="nav__brand" href="/">uxskill</a>
    <a class="nav__link" href="/">Home</a>
    <a class="nav__link" href="/commands.html">Commands</a>
    <a class="nav__link" href="/mcp.html">MCP</a>
    <a class="nav__link" href="/compare.html">Compare</a>
    <a class="nav__link" href="/blog/">Blog</a>
    <a class="nav__link" href="https://github.com/Laith0003/ux-skill" rel="noopener">GitHub</a>
  </div>
</header>

<section class="top">
  <div class="container">
    <p class="top__eyebrow">Linter catalogue · v{html.escape(str(version)) if version else ""}</p>
    <h1 class="top__title">{total} fingerprints of <em>AI design slop.</em></h1>
    <p class="top__lead">
      Every rule in <code>data/anti-patterns.json</code>, browseable. Run the linter (<code>uxskill lint</code>) and it scans your HTML/CSS/JS for these regex patterns in &lt;50&#x20;ms: no LLM, no API call, no telemetry. Each rule names the fingerprint, explains why it's slop, and tells the AI session what to ship instead.
    </p>
    <div class="top__stats">
      <span class="top__stat"><b>{total}</b> rules total</span>
      <span class="top__stat"><b>{high}</b> high severity</span>
      <span class="top__stat"><b>{med}</b> medium</span>
      <span class="top__stat"><b>{low}</b> low</span>
      <span class="top__stat"><b>{len(categories)}</b> categories</span>
    </div>
  </div>
</section>

<section class="toolbar">
  <div class="container toolbar__row">
    <input type="search" class="ap-search" id="ap-search" placeholder="Search rules by name, category, or fix..." aria-label="Search rules">
    <button type="button" class="ap-chip is-active" data-cat="*">All</button>
    {cat_chips}
  </div>
</section>

<section>
  <div class="container">
    <div class="grid" id="ap-grid">
      {cards}
    </div>
  </div>
</section>

<footer>
  <div class="container">
    ux-skill &middot; deterministic anti-AI-slop linter &middot; MIT &middot; no telemetry &middot; <a href="/">home</a> &middot; <a href="https://github.com/Laith0003/ux-skill" rel="noopener">github</a>
  </div>
</footer>

<script>
(function() {{
  const search = document.getElementById('ap-search');
  const grid = document.getElementById('ap-grid');
  const chips = document.querySelectorAll('.ap-chip');
  const cards = Array.from(grid.querySelectorAll('.ap-card'));
  let activeCat = '*';
  function refilter() {{
    const q = (search.value || '').toLowerCase().trim();
    cards.forEach(function(c) {{
      const text = c.textContent.toLowerCase();
      const cat = (c.querySelector('.ap-cat') || {{}}).textContent || '';
      const catOk = activeCat === '*' || cat === activeCat;
      const queryOk = !q || text.indexOf(q) !== -1;
      c.classList.toggle('is-hidden', !(catOk && queryOk));
    }});
  }}
  search.addEventListener('input', refilter);
  chips.forEach(function(chip) {{
    chip.addEventListener('click', function() {{
      chips.forEach(function(c) {{ c.classList.remove('is-active'); }});
      chip.classList.add('is-active');
      activeCat = chip.dataset.cat;
      refilter();
    }});
  }});
}})();
</script>

</body>
</html>
"""


def main():
    rules, version = load_rules()
    out_html = build_html(rules, version)
    OUT.write_text(out_html, encoding="utf-8")
    LANDING_OUT.write_text(out_html, encoding="utf-8")
    print(f"ok  {len(rules)} rules  →  docs/anti-patterns.html + landing/anti-patterns.html")


if __name__ == "__main__":
    main()
