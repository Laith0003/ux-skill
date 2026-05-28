#!/usr/bin/env python3
"""
v3.0.3 — unify nav + fonts across all standalone HTML pages.

The canonical source is docs/index.html. This script rewrites the
font-loading block, the .nav CSS block, the <header class="nav"> markup,
the <div class="nav__drawer"> markup, and the nav-related JS in every
other public page so the entire site shares one header.

Page-local accents, page-local CSS for non-nav surfaces, page-local
content (hero, cards, tables, blog list) are preserved verbatim.

Mirrors docs/<page>.html to landing/<page>.html after each rewrite.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LANDING = ROOT / "landing"

# ============================================================
# CANONICAL FRAGMENTS
# ============================================================

# Single Google Fonts URL used everywhere.
CANONICAL_FONTS = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <!-- Bricolage Grotesque (display), Inter (body Latin), JetBrains Mono (mono),
       Instrument Serif (italic accents), IBM Plex Sans Arabic (mandatory for ar locale —
       see tests/test_arabic_typography.py for the regression guard). -->
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap" rel="stylesheet">"""

# Canonical nav CSS block. Self-contained — defines its own fallback custom
# properties via @supports-style declarations so it does not depend on the
# host page already defining --t-fast, --t-mid, --ease-cinema, --r-pill,
# --r-md, --gutter, --max-w. The host page's --accent is preserved.
CANONICAL_NAV_CSS = """  <style id="unified-nav-css">
    /* ============================================================
       UNIFIED SITE NAV (v3.0.3)
       Canonical source: docs/index.html
       ============================================================ */
    :root {
      --nav-t-fast: 160ms;
      --nav-t-mid: 280ms;
      --nav-ease: cubic-bezier(0.22, 1, 0.36, 1);
      --nav-r-pill: 999px;
      --nav-r-md: 8px;
      --nav-gutter: clamp(20px, 4vw, 48px);
      --nav-max-w: 1180px;
      --nav-canvas: #07080a;
      --nav-ink: #f6f7f9;
      --nav-body: #c7ccd3;
      --nav-muted: #8a8f96;
      --nav-hairline: rgba(246, 247, 249, 0.07);
      --nav-hairline-2: rgba(246, 247, 249, 0.14);
      --nav-accent-fallback: #f59e0b;
      --nav-display: 'Bricolage Grotesque', 'Inter Tight', system-ui, sans-serif;
      --nav-mono: 'JetBrains Mono', ui-monospace, 'SFMono-Regular', monospace;
      --nav-body-face: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* All canonical nav rules are prefixed with #nav or #nav-drawer
       so they always win against page-local .nav / .wordmark / .nav__link
       rules left over in the page CSS (specificity (0,1,1,0) > (0,0,1,0)). */

    #nav.nav {
      position: fixed;
      top: 0; left: 0; right: 0;
      z-index: 80;
      padding: 14px 0;
      transition: backdrop-filter var(--nav-t-mid) var(--nav-ease),
                  background-color var(--nav-t-mid) var(--nav-ease),
                  border-color var(--nav-t-mid) var(--nav-ease);
      border-bottom: 1px solid transparent;
    }
    #nav.nav.is-scrolled {
      background: rgba(7, 8, 10, 0.72);
      backdrop-filter: saturate(140%) blur(18px);
      -webkit-backdrop-filter: saturate(140%) blur(18px);
      border-bottom-color: var(--hairline, var(--nav-hairline));
    }
    #nav .nav__inner {
      max-width: var(--max-w, var(--nav-max-w));
      margin: 0 auto;
      padding: 0 var(--gutter, var(--nav-gutter));
      display: flex; align-items: center; justify-content: space-between;
      gap: 18px;
    }
    #nav .wordmark {
      font-family: var(--display, var(--nav-display));
      font-variation-settings: 'wdth' 92, 'opsz' 96, 'wght' 620;
      font-size: 24px;
      letter-spacing: -0.025em;
      line-height: 1;
      color: var(--ink, var(--nav-ink));
      display: inline-flex;
      align-items: baseline;
      gap: 4px;
      text-decoration: none;
      text-transform: none;
    }
    #nav .wordmark:hover { text-decoration: none; }
    #nav .wordmark__dot {
      display: inline-block;
      width: 7px; height: 7px;
      border-radius: 2px;
      background: var(--accent, var(--nav-accent-fallback));
      transform: none;
      margin-left: 0;
    }
    #nav .nav__links {
      display: flex; gap: 22px;
      align-items: center;
    }
    #nav .nav__link {
      font-family: var(--mono, var(--nav-mono));
      font-size: 12px;
      font-weight: 500;
      color: var(--muted, var(--nav-muted));
      letter-spacing: 0.10em;
      text-transform: uppercase;
      text-decoration: none;
      transition: color var(--nav-t-fast) var(--nav-ease);
    }
    #nav .nav__link:hover,
    #nav .nav__link:focus-visible { color: var(--ink, var(--nav-ink)); text-decoration: none; }
    #nav .nav__link.is-current { color: var(--ink, var(--nav-ink)); }
    #nav .nav__cta,
    #nav .cta-pill {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 8px 14px;
      min-height: 0;
      background: transparent;
      border: 1px solid var(--hairline-2, var(--nav-hairline-2));
      border-radius: var(--r-pill, var(--nav-r-pill));
      font-family: var(--mono, var(--nav-mono));
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--ink, var(--nav-ink));
      text-decoration: none;
      transition: border-color var(--nav-t-fast) var(--nav-ease),
                  background-color var(--nav-t-fast) var(--nav-ease),
                  transform var(--nav-t-fast) var(--nav-ease);
    }
    #nav .nav__cta:hover,
    #nav .cta-pill:hover {
      border-color: var(--accent, var(--nav-accent-fallback));
      background: transparent;
      transform: none;
    }
    #nav .nav__menu-btn {
      display: none;
      width: 38px; height: 38px;
      align-items: center; justify-content: center;
      border: 1px solid var(--hairline, var(--nav-hairline));
      border-radius: var(--r-md, var(--nav-r-md));
      color: var(--ink, var(--nav-ink));
      background: transparent;
      cursor: pointer;
    }
    @media (max-width: 880px) {
      #nav .nav__links { display: none; }
      #nav .nav__cta, #nav .cta-pill { display: none; }
      #nav .nav__menu-btn { display: inline-flex; }
    }

    #nav-drawer.nav__drawer {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      inset: auto;
      z-index: 90;
      background: var(--canvas, var(--nav-canvas));
      padding: 22px var(--gutter, var(--nav-gutter)) 44px;
      display: flex; flex-direction: column; gap: 18px;
      opacity: 0;
      pointer-events: none;
      transform: translateY(-8px);
      transition: opacity var(--nav-t-mid) var(--nav-ease),
                  transform var(--nav-t-mid) var(--nav-ease);
      overflow-y: auto;
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
    }
    #nav-drawer.nav__drawer.is-open {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }
    #nav-drawer a {
      font-family: var(--display, var(--nav-display));
      font-variation-settings: 'wdth' 90, 'opsz' 80, 'wght' 540;
      font-size: 28px;
      letter-spacing: -0.015em;
      color: var(--ink, var(--nav-ink));
      text-decoration: none;
      padding: 6px 0;
      border-bottom: none;
      display: block;
    }
    #nav-drawer .nav__drawer-top {
      position: static;
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 4px;
    }
    #nav-drawer .nav__drawer-close {
      position: static;
      width: 38px; height: 38px;
      display: inline-flex; align-items: center; justify-content: center;
      border: 1px solid var(--hairline, var(--nav-hairline));
      border-radius: var(--r-md, var(--nav-r-md));
      color: var(--ink, var(--nav-ink));
      background: transparent;
      cursor: pointer;
    }
    #nav-drawer .nav__drawer-langs-details summary {
      list-style: none;
      cursor: pointer;
      padding: 12px 0;
      display: flex; align-items: center; justify-content: space-between;
      border-top: 1px solid var(--hairline, var(--nav-hairline));
      border-bottom: 1px solid var(--hairline, var(--nav-hairline));
      font-family: var(--mono, var(--nav-mono));
      font-size: 12px;
      letter-spacing: 0.10em;
      text-transform: uppercase;
      color: var(--muted, var(--nav-muted));
    }
    #nav-drawer .nav__drawer-langs-details summary::-webkit-details-marker { display: none; }
    #nav-drawer .nav__drawer-langs-summary-label { display: inline-flex; align-items: center; gap: 10px; }
    #nav-drawer .nav__drawer-langs-caret { transition: transform var(--nav-t-mid) var(--nav-ease); }
    #nav-drawer .nav__drawer-langs-details[open] .nav__drawer-langs-caret { transform: rotate(180deg); }
    #nav-drawer .nav__drawer-langs-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px 24px;
      padding: 16px 0;
    }
    #nav-drawer .nav__drawer-langs-grid a {
      font-family: var(--body-face, var(--nav-body-face));
      font-size: 14px;
      letter-spacing: 0;
      text-transform: none;
      color: var(--body, var(--nav-body));
      padding: 4px 0;
      border-bottom: none;
    }
    #nav-drawer .nav__drawer-langs-grid a:hover { color: var(--ink, var(--nav-ink)); }

    /* RTL — nav inner flips */
    html[dir="rtl"] #nav .nav__inner { direction: rtl; }

    /* Defensive — when the fixed .nav is present, give layouts that
       previously assumed an inline header (.wrap on blog/index,
       .top/.toolbar on the catalogue pages) enough headroom so
       content isn't hidden behind the nav. */
    .wrap > main:first-of-type { padding-top: clamp(56px, 8vw, 80px); }
    body > section.top:first-of-type,
    body > .top:first-of-type { padding-top: clamp(96px, 12vw, 128px); }
    body > section.toolbar { top: 64px; }
  </style>"""

# Canonical nav markup. Uses /-relative links so it works at any path depth.
CANONICAL_NAV_HTML = """<header class="nav" id="nav">
  <div class="nav__inner">
    <a href="/" class="wordmark" aria-label="uxskill home">
      uxskill<span class="wordmark__dot" aria-hidden="true"></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
      <a class="nav__link" href="/brands.html">Brands</a>
      <a class="nav__link" href="/anti-patterns.html">Anti-patterns</a>
      <a class="nav__link" href="/commands.html">Commands</a>
      <a class="nav__link" href="https://github.com/Laith0003/ux-skill" rel="noopener">GitHub</a>
    </nav>
    <a href="https://github.com/Laith0003/ux-skill" class="nav__cta" rel="noopener">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
      <span>Star on GitHub</span>
    </a>
    <button type="button" class="nav__menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav-drawer" id="nav-menu-btn">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<div class="nav__drawer" id="nav-drawer" role="dialog" aria-modal="true" aria-label="Site menu" aria-hidden="true">
  <div class="nav__drawer-top">
    <span aria-hidden="true"></span>
    <button type="button" class="nav__drawer-close" aria-label="Close menu" id="nav-drawer-close">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
    </button>
  </div>

  <details class="nav__drawer-langs-details" id="nav-drawer-langs">
    <summary>
      <span class="nav__drawer-langs-summary-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
        <span>Language &middot; 17</span>
      </span>
      <svg class="nav__drawer-langs-caret" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
    </summary>
    <div class="nav__drawer-langs-grid">
      <a href="/"        lang="en"   >English</a>
      <a href="/zh-CN/"  lang="zh-CN">&#31616;&#20307;&#20013;&#25991;</a>
      <a href="/zh-TW/"  lang="zh-TW">&#32321;&#39636;&#20013;&#25991;</a>
      <a href="/ja/"     lang="ja"   >&#26085;&#26412;&#35486;</a>
      <a href="/ko/"     lang="ko"   >&#54620;&#44397;&#50612;</a>
      <a href="/hi/"     lang="hi"   >&#2361;&#2367;&#2344;&#2381;&#2342;&#2368;</a>
      <a href="/id/"     lang="id"   >Bahasa</a>
      <a href="/vi/"     lang="vi"   >Ti&#7871;ng Vi&#7879;t</a>
      <a href="/th/"     lang="th"   >&#3652;&#3607;&#3618;</a>
      <a href="/ar/"     lang="ar"   dir="rtl">&#1575;&#1604;&#1593;&#1585;&#1576;&#1610;&#1577;</a>
      <a href="/es/"     lang="es"   >Espa&ntilde;ol</a>
      <a href="/fr/"     lang="fr"   >Fran&ccedil;ais</a>
      <a href="/de/"     lang="de"   >Deutsch</a>
      <a href="/pt-BR/"  lang="pt-BR">Portugu&ecirc;s</a>
      <a href="/ru/"     lang="ru"   >&#1056;&#1091;&#1089;&#1089;&#1082;&#1080;&#1081;</a>
      <a href="/tr/"     lang="tr"   >T&uuml;rk&ccedil;e</a>
      <a href="/it/"     lang="it"   >Italiano</a>
    </div>
  </details>

  <a href="/brands.html">Brands</a>
  <a href="/anti-patterns.html">Anti-patterns</a>
  <a href="/commands.html">Commands</a>
  <a href="/mcp.html">MCP</a>
  <a href="/compare.html">Compare</a>
  <a href="/blog/">Blog</a>
  <a href="/faq.html">FAQ</a>
  <a href="/about.html">About</a>
  <a href="/roadmap.html">Roadmap</a>
  <a href="https://github.com/Laith0003/ux-skill" rel="noopener">GitHub</a>
</div>"""

CANONICAL_NAV_JS = """  <script id="unified-nav-js">
  (function () {
    var nav = document.getElementById('nav');
    function onScroll() {
      var y = window.scrollY;
      if (!nav) return;
      if (y > 24) nav.classList.add('is-scrolled');
      else nav.classList.remove('is-scrolled');
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    var drawer = document.getElementById('nav-drawer');
    var menuBtn = document.getElementById('nav-menu-btn');
    var closeBtn = document.getElementById('nav-drawer-close');
    function openDrawer() {
      if (!drawer || !menuBtn) return;
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      menuBtn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }
    function closeDrawer() {
      if (!drawer || !menuBtn) return;
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      menuBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
    if (menuBtn) menuBtn.addEventListener('click', openDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    if (drawer) drawer.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeDrawer); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) closeDrawer();
    });
  })();
  </script>"""

# ============================================================
# REWRITE FUNCTIONS
# ============================================================

def replace_font_block(html: str) -> str:
    """Replace the head font preconnect+link block with the canonical fonts.

    Strategy: find the first <link rel="preconnect" href="https://fonts.googleapis.com">
    line and the next stylesheet <link> that references fonts.googleapis.com,
    replace the whole span. If no such block exists (brands.html, anti-patterns.html),
    insert before </head>.
    """
    # Pattern matches the preconnect pair + the stylesheet link.
    pattern = re.compile(
        r"[ \t]*<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">[ \t]*\n"
        r"[ \t]*<link rel=\"preconnect\" href=\"https://fonts\.gstatic\.com\" crossorigin>[ \t]*\n"
        r"(?:[ \t]*<!--[^\n]*-->[ \t]*\n)?"
        r"[ \t]*<link href=\"https://fonts\.googleapis\.com/css2\?[^\"]+\" rel=\"stylesheet\">[ \t]*",
        re.MULTILINE,
    )
    if pattern.search(html):
        return pattern.sub(CANONICAL_FONTS.rstrip(), html, count=1)
    # No fonts loaded — inject before </head>.
    return html.replace("</head>", CANONICAL_FONTS + "\n</head>", 1)


def remove_existing_nav_css(html: str) -> str:
    """Remove the page-local .nav / .wordmark / .nav__drawer / .cta-pill /
    .nav__menu-btn / .menu-btn / .drawer / .lang-picker rules from the page CSS.

    We don't try to surgically extract individual rules — too brittle. Instead,
    if a previous run injected <style id="unified-nav-css">, we delete it so
    the script is idempotent.
    """
    html = re.sub(
        r"  <style id=\"unified-nav-css\">.*?</style>\n?",
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"  <script id=\"unified-nav-js\">.*?</script>\n?",
        "",
        html,
        flags=re.DOTALL,
    )
    return html


def replace_header_block(html: str) -> str:
    """Replace the <header class="nav"...> ... </header> + following
    <div class="nav__drawer">...</div> markup with the canonical version.

    Also handles the blog/index.html variant which uses <header class="top">.
    """
    # Variant 1: <header class="nav" ...> ... </header>  + drawer
    # Match a header tag (with optional id), capture through </header>,
    # then optionally the immediately-following nav__drawer div.
    header_pattern = re.compile(
        r"<header class=\"nav\"[^>]*>.*?</header>"
        r"(?:\s*<div class=\"nav__drawer\"[^>]*>.*?</div>)?",
        re.DOTALL,
    )
    if header_pattern.search(html):
        return header_pattern.sub(CANONICAL_NAV_HTML, html, count=1)

    # Variant 2: brands.html / anti-patterns.html style — simple header.nav block
    # (already covered by Variant 1 since they also use <header class="nav">).

    # Variant 3: blog/index.html — <header class="top"> ... </header> + .drawer div
    top_pattern = re.compile(
        r"<header class=\"top\">.*?</header>"
        r"(?:\s*<div class=\"drawer\"[^>]*>.*?</div>)?",
        re.DOTALL,
    )
    if top_pattern.search(html):
        return top_pattern.sub(CANONICAL_NAV_HTML, html, count=1)

    return html


def inject_unified_css_and_js(html: str) -> str:
    """Inject the canonical nav CSS before </head> and JS before </body>."""
    if "<style id=\"unified-nav-css\">" not in html:
        html = html.replace("</head>", CANONICAL_NAV_CSS + "\n</head>", 1)
    if "<script id=\"unified-nav-js\">" not in html:
        html = html.replace("</body>", CANONICAL_NAV_JS + "\n</body>", 1)
    return html


def unify_page(path: Path) -> bool:
    """Apply all transforms to a single HTML file. Returns True if modified."""
    original = path.read_text(encoding="utf-8")
    out = original

    out = remove_existing_nav_css(out)
    out = replace_font_block(out)
    out = replace_header_block(out)
    out = inject_unified_css_and_js(out)

    if out != original:
        path.write_text(out, encoding="utf-8")
        return True
    return False


# ============================================================
# DRIVE
# ============================================================

PAGES = [
    "about.html",
    "compare.html",
    "faq.html",
    "mcp.html",
    "commands.html",
    "brands.html",
    "anti-patterns.html",
    "roadmap.html",
    "showcase.html",
    "privacy.html",
    "blog/index.html",
]

def main():
    touched = []
    for rel in PAGES:
        docs_path = DOCS / rel
        landing_path = LANDING / rel
        if docs_path.exists():
            if unify_page(docs_path):
                touched.append(str(docs_path.relative_to(ROOT)))
            # Mirror to landing/
            if landing_path.exists():
                # Reuse the just-rewritten docs version as the landing source
                # to guarantee parity.
                landing_path.write_text(
                    docs_path.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
                touched.append(str(landing_path.relative_to(ROOT)))
            else:
                # If the landing mirror is missing entirely, write it.
                landing_path.parent.mkdir(parents=True, exist_ok=True)
                landing_path.write_text(
                    docs_path.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
                touched.append(str(landing_path.relative_to(ROOT)) + " (new)")
        else:
            print(f"SKIP — missing: {docs_path}")

    print(f"\nTouched {len(touched)} files:")
    for t in touched:
        print(f"  - {t}")


if __name__ == "__main__":
    main()
