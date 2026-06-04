"""Generate docs/brands.html: browseable, searchable catalogue of every
brand spec in data/brands/_index.json.

High-value because:
- One page lists every brand the recommender knows about.
- Each brand has its own anchor → blog posts can deep-link.
- Massive long-tail SEO (each brand name is a search term).
- Lets visitors verify the catalogue is real before they install.

Re-run after data/brands/_index.json changes.
"""
from pathlib import Path
import json
import html
import re


def sanitize_dashes(s):
    """Strip em/en dashes from rendered prose (no-AI-tell house rule).
    em-dash -> comma; en-dash (numeric range) -> hyphen. Applied to brand
    spec text so a rebuild never reintroduces dashes into docs/brands.html."""
    s = re.sub(r'\s*—\s*', ', ', s)
    s = re.sub(r'\s*–\s*', '-', s)
    return s


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "brands" / "_index.json"
BRANDS_DIR = ROOT / "data" / "brands"
OUT = ROOT / "docs" / "brands.html"
LANDING_OUT = ROOT / "landing" / "brands.html"


def load_index():
    with INDEX.open(encoding="utf-8") as f:
        raw = json.load(f)
    brands = raw.get("brands") if isinstance(raw, dict) else raw
    version = (raw.get("_meta") or {}).get("version") if isinstance(raw, dict) else None
    return brands or [], version


def load_spec(bid):
    """Try to load the full spec for a brand id; return {} on miss."""
    p = BRANDS_DIR / f"{bid}.json"
    if p.exists():
        try:
            with p.open(encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def render_swatches(dl):
    """Render a few color swatches from design_language dict."""
    colors = []
    if isinstance(dl, dict):
        for key in ("color_canvas", "color_ink", "color_primary", "color_accent",
                    "color_muted", "color_secondary"):
            v = dl.get(key)
            if v and isinstance(v, str):
                colors.append((key.replace("color_", ""), v))
    if not colors:
        return ""
    spans = "".join(
        f'<span class="br-sw" style="background:{html.escape(c)};" title="{html.escape(name)}: {html.escape(c)}"></span>'
        for name, c in colors[:6]
    )
    return f'<div class="br-swatches" aria-hidden="true">{spans}</div>'


def render_card(brand_idx, spec):
    bid = html.escape(str(brand_idx.get("id", "")))
    name = html.escape(str(brand_idx.get("name", bid)))
    category = html.escape(str(brand_idx.get("category", "")))
    philosophy = ""
    if spec:
        p = spec.get("philosophy") or spec.get("essence")
        if p:
            philosophy = sanitize_dashes(html.escape(str(p)))
    swatches = render_swatches(spec.get("design_language", {})) if spec else ""
    # Only emit the DESIGN.md link if the file actually exists on disk.
    # 72 of 160 brands historically had no DESIGN.md and the link 404'd.
    md_path = ROOT / "references" / "brands" / f"{bid}-DESIGN.md"
    if md_path.exists():
        md_link = f"<a href=\"https://github.com/Laith0003/ux-skill/blob/main/references/brands/{bid}-DESIGN.md\" rel=\"noopener\" class=\"br-md\">DESIGN.md</a>"
    else:
        md_link = ""
    json_link = f"<a href=\"https://github.com/Laith0003/ux-skill/blob/main/data/brands/{bid}.json\" rel=\"noopener\" class=\"br-json\">spec.json</a>"
    return f'''
    <article class="br-card" id="{bid}" data-cat="{category}">
      <header class="br-head">
        <span class="br-id">#{bid}</span>
        <span class="br-cat">{category}</span>
        <h3 class="br-name">{name}</h3>
      </header>
      {swatches}
      <p class="br-phil">{philosophy or '<em class="br-phil-empty">DESIGN.md only, no structured spec yet.</em>'}</p>
      <div class="br-links">
        {json_link}
        {md_link}
        <a href="#{bid}" class="br-anchor">link</a>
      </div>
    </article>
    '''


def build_html(brands, version):
    # Group/category counts.
    categories = sorted({b.get("category") or "Uncategorized" for b in brands})
    cat_counts = {}
    for b in brands:
        c = b.get("category") or "Uncategorized"
        cat_counts[c] = cat_counts.get(c, 0) + 1
    cat_chips = "".join(
        f'<button type="button" class="br-chip" data-cat="{html.escape(c)}">{html.escape(c)} <small>({cat_counts[c]})</small></button>'
        for c in categories
    )
    # Load specs + render cards (sorted by name).
    rendered = []
    for b in sorted(brands, key=lambda x: (x.get("name") or "").lower()):
        spec = load_spec(b.get("id", ""))
        rendered.append(render_card(b, spec))
    cards = "\n".join(rendered)
    total = len(brands)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{total} brand DESIGN specs · the ux-skill catalogue</title>
<meta name="description" content="The complete catalogue of {total} brand specs in ux-skill. Each one is a queryable JSON + a prose DESIGN.md: palette, typography, philosophy, components, anti-patterns to avoid. Apple, Stripe, Linear, Vercel, Ferrari, Anthropic, and {total - 6} more.">
<link rel="canonical" href="https://uxskill.laithjunaidy.com/brands.html">
<meta property="og:title" content="{total} brand DESIGN specs · ux-skill catalogue">
<meta property="og:description" content="Apple, Stripe, Linear, Vercel, Ferrari, Anthropic, plus {total - 6} more. Each brand is a structured spec.json + prose DESIGN.md.">
<meta property="og:url" content="https://uxskill.laithjunaidy.com/brands.html">
<meta property="og:image" content="https://uxskill.laithjunaidy.com/og/home.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{total} brand specs · ux-skill catalogue">
<meta name="twitter:description" content="The complete catalogue. Searchable + filterable + linkable.">
<meta name="twitter:image" content="https://uxskill.laithjunaidy.com/og/home.png">

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"{total} brand DESIGN specs","url":"https://uxskill.laithjunaidy.com/brands.html","description":"Browseable index of every brand spec known to ux-skill.","isPartOf":{{"@type":"WebSite","name":"ux-skill","url":"https://uxskill.laithjunaidy.com/"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://uxskill.laithjunaidy.com/"}},{{"@type":"ListItem","position":2,"name":"Brand specs","item":"https://uxskill.laithjunaidy.com/brands.html"}}]}}
</script>

<style>
  :root {{
    --canvas: #07080a;
    --surface-1: #0e1014;
    --ink: #f6f7f9;
    --body: #c0c3c9;
    --muted: #8a8f96;
    --hairline: rgba(255,255,255,0.08);
    --hairline-2: rgba(255,255,255,0.16);
    --accent: #cc785c;
    --display: 'Bricolage Grotesque', system-ui, sans-serif;
    --sans: 'Inter', system-ui, sans-serif;
    --mono: 'JetBrains Mono', ui-monospace, monospace;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: var(--canvas); color: var(--ink); font-family: var(--sans); line-height: 1.55; overflow-x: clip; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  h1, h2, h3 {{ font-family: var(--display); letter-spacing: -0.02em; }}
  .container {{ max-width: 1180px; margin: 0 auto; padding: 0 clamp(20px, 4vw, 48px); }}

  .nav {{ padding: 22px 0; border-bottom: 1px solid var(--hairline); }}
  .nav__row {{ display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }}
  .nav__brand {{ font-family: var(--display); font-size: 18px; font-weight: 700; letter-spacing: -0.02em; color: var(--ink); }}
  .nav__link {{ font-family: var(--mono); font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }}
  .nav__link:hover {{ color: var(--ink); }}

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
  .br-search {{ flex: 1; min-width: 260px; padding: 10px 14px; background: var(--surface-1); border: 1px solid var(--hairline); border-radius: 8px; color: var(--ink); font-family: var(--sans); font-size: 14px; }}
  .br-search:focus {{ outline: none; border-color: var(--accent); }}
  .br-chip {{ background: var(--surface-1); border: 1px solid var(--hairline); color: var(--body); padding: 6px 12px; border-radius: 999px; font-family: var(--mono); font-size: 10.5px; letter-spacing: 0.08em; text-transform: uppercase; cursor: pointer; }}
  .br-chip small {{ color: var(--muted); font-weight: 400; }}
  .br-chip.is-active {{ background: var(--accent); color: var(--canvas); border-color: var(--accent); }}
  .br-chip.is-active small {{ color: var(--canvas); }}
  .br-chip:hover {{ border-color: var(--hairline-2); }}

  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; padding: 36px 0 80px; }}
  .br-card {{ position: relative; background: var(--surface-1); border: 1px solid var(--hairline); border-radius: 14px; padding: 22px; min-height: 240px; display: flex; flex-direction: column; }}
  .br-card:hover {{ border-color: var(--hairline-2); }}
  .br-head {{ display: grid; grid-template-columns: auto auto; gap: 4px 12px; align-items: center; margin-bottom: 14px; }}
  .br-id {{ font-family: var(--mono); font-size: 10.5px; color: var(--muted); letter-spacing: 0.04em; }}
  .br-cat {{ font-family: var(--mono); font-size: 9.5px; color: var(--muted); letter-spacing: 0.10em; text-transform: uppercase; text-align: right; }}
  .br-name {{ grid-column: 1 / -1; font-size: 22px; font-weight: 600; color: var(--ink); line-height: 1.15; margin-top: 2px; }}
  .br-swatches {{ display: flex; gap: 4px; margin-bottom: 14px; height: 8px; border-radius: 4px; overflow: hidden; }}
  .br-sw {{ flex: 1; min-width: 0; border: 1px solid rgba(255,255,255,0.05); border-radius: 2px; }}
  .br-phil {{ color: var(--body); font-size: 13.5px; line-height: 1.55; flex: 1; margin-bottom: 14px; }}
  .br-phil-empty {{ color: var(--muted); font-style: italic; font-size: 12.5px; }}
  .br-links {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .br-md, .br-json {{ font-family: var(--mono); font-size: 10.5px; padding: 4px 10px; border: 1px solid var(--hairline); border-radius: 6px; color: var(--body); letter-spacing: 0.04em; }}
  .br-md:hover, .br-json:hover {{ color: var(--ink); border-color: var(--hairline-2); text-decoration: none; }}
  .br-anchor {{ font-family: var(--mono); font-size: 10.5px; padding: 4px 10px; color: var(--muted); margin-left: auto; opacity: 0.6; }}
  .br-anchor:hover {{ opacity: 1; color: var(--ink); text-decoration: none; }}
  .br-card.is-hidden {{ display: none; }}

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
    <a class="nav__link" href="/anti-patterns.html">Anti-patterns</a>
    <a class="nav__link" href="/mcp.html">MCP</a>
    <a class="nav__link" href="/compare.html">Compare</a>
    <a class="nav__link" href="/blog/">Blog</a>
    <a class="nav__link" href="https://github.com/Laith0003/ux-skill" rel="noopener">GitHub</a>
  </div>
</header>

<section class="top">
  <div class="container">
    <p class="top__eyebrow">Brand catalogue · v{html.escape(str(version)) if version else ""}</p>
    <h1 class="top__title">{total} brand <em>DESIGN.md</em> specs.</h1>
    <p class="top__lead">
      The recommender doesn't guess. Each brand is a queryable <code>spec.json</code> and a prose <code>DESIGN.md</code>: palette, typography, philosophy, components observed, voice do's-don'ts, anti-patterns to avoid. The AI session pulls the whole spec, not a slogan. Apple, Stripe, Linear, Vercel, Ferrari, Anthropic, and {total - 6} more.
    </p>
    <div class="top__stats">
      <span class="top__stat"><b>{total}</b> brand specs</span>
      <span class="top__stat"><b>{len(categories)}</b> categories</span>
      <span class="top__stat">MIT · no telemetry</span>
    </div>
  </div>
</section>

<section class="toolbar">
  <div class="container toolbar__row">
    <input type="search" class="br-search" id="br-search" placeholder="Search by brand name, category, or philosophy..." aria-label="Search brands">
    <button type="button" class="br-chip is-active" data-cat="*">All <small>({total})</small></button>
    {cat_chips}
  </div>
</section>

<section>
  <div class="container">
    <div class="grid" id="br-grid">
      {cards}
    </div>
  </div>
</section>

<footer>
  <div class="container">
    ux-skill &middot; {total} brand DESIGN.md specs &middot; MIT &middot; no telemetry &middot; <a href="/">home</a> &middot; <a href="https://github.com/Laith0003/ux-skill" rel="noopener">github</a>
  </div>
</footer>

<script>
(function() {{
  const search = document.getElementById('br-search');
  const grid = document.getElementById('br-grid');
  const chips = document.querySelectorAll('.br-chip');
  const cards = Array.from(grid.querySelectorAll('.br-card'));
  let activeCat = '*';
  function refilter() {{
    const q = (search.value || '').toLowerCase().trim();
    cards.forEach(function(c) {{
      const text = c.textContent.toLowerCase();
      const cat = c.dataset.cat || '';
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
    brands, version = load_index()
    out_html = build_html(brands, version)
    OUT.write_text(out_html, encoding="utf-8")
    LANDING_OUT.write_text(out_html, encoding="utf-8")
    print(f"ok  {len(brands)} brands  →  docs/brands.html + landing/brands.html")


if __name__ == "__main__":
    main()
