#!/usr/bin/env python3
"""
Canonical site nav component for ux-skill docs — single source of truth.

One identical nav on every page: a sticky bar (brand + primary links + language
globe + Star CTA + always-visible menu button) that opens a drawer with EVERY
page, the languages, and the Star. Self-contained: namespaced `.usknav` classes,
hardcoded dark-cinema colors (identical regardless of each page's own tokens),
native <details> language menu, vanilla drawer JS with full focus management.

Reachability: the bar shows the 5 primary links for quick access; the menu
button (visible at every width) opens a drawer listing ALL 10 pages, so nothing
is unreachable. Below 820px the bar links/globe/star collapse into the drawer.

A11y: focus-visible rings on every control (>=3:1 amber), drawer focus trap +
return-focus + Escape, aria-hidden on decorative icons, aria-expanded on the
button, >=24px tap targets, prefers-reduced-motion honored.

Link set: no separate plain "GitHub" link — the Star pill is the GitHub link.
"""
from __future__ import annotations

# (href, autonym, lang, dir-rtl?)
LOCALES = [
    ("/", "English", "en", False), ("/zh-CN/", "简体中文", "zh-CN", False),
    ("/zh-TW/", "繁體中文", "zh-TW", False), ("/ja/", "日本語", "ja", False),
    ("/ko/", "한국어", "ko", False), ("/hi/", "हिन्दी", "hi", False),
    ("/id/", "Bahasa Indonesia", "id", False), ("/vi/", "Tiếng Việt", "vi", False),
    ("/th/", "ไทย", "th", False), ("/ar/", "العربية", "ar", True),
    ("/es/", "Español", "es", False), ("/fr/", "Français", "fr", False),
    ("/de/", "Deutsch", "de", False), ("/pt-BR/", "Português", "pt-BR", False),
    ("/ru/", "Русский", "ru", False), ("/tr/", "Türkçe", "tr", False),
    ("/it/", "Italiano", "it", False),
]

# Primary links shown in the desktop bar (quick access). Labels localize per page.
# All pages live directly in the desktop bar (no desktop hamburger). The drawer
# is mobile-only and mirrors the same set.
LINKS = [
    ("/brands.html", "Brands"),
    ("/anti-patterns.html", "Anti-patterns"),
    ("/commands.html", "Commands"),
    ("/blog/", "Blog"),
    ("/compare.html", "Compare"),
    ("/mcp.html", "MCP"),
    ("/showcase.html", "Showcase"),
    ("/faq.html", "FAQ"),
    ("/about.html", "About"),
    ("/roadmap.html", "Roadmap"),
]
DRAWER_LINKS = LINKS
REPO = "https://github.com/Laith0003/ux-skill"

NAV_CSS = """
  .usknav{position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:18px;
    padding:0 clamp(16px,4vw,48px);block-size:56px;background:rgba(7,8,10,0.86);
    backdrop-filter:saturate(150%) blur(14px);-webkit-backdrop-filter:saturate(150%) blur(14px);
    border-block-end:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif}
  .usknav__brand{font-family:'Bricolage Grotesque','Inter',sans-serif;font-weight:700;font-size:17px;
    color:#f6f7f9;text-decoration:none;letter-spacing:-0.01em;margin-inline-end:auto;padding:6px 2px}
  .usknav__links{display:flex;align-items:center;gap:clamp(9px,1.1vw,17px)}
  .usknav__link{font-family:ui-monospace,'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:0.08em;
    text-transform:uppercase;color:#8a8f96;text-decoration:none;white-space:nowrap;
    padding-block:8px;transition:color 140ms ease}
  .usknav__link:hover,.usknav__link[aria-current="page"]{color:#f6f7f9}
  .usknav__langs{position:relative}
  .usknav__langs>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:5px;
    color:#8a8f96;padding:8px 6px;transition:color 140ms ease;min-block-size:24px}
  .usknav__langs>summary::-webkit-details-marker{display:none}
  .usknav__langs>summary:hover{color:#f6f7f9}
  .usknav__langs-menu{position:absolute;top:calc(100% + 8px);inset-inline-end:0;min-inline-size:184px;
    max-block-size:60vh;overflow-y:auto;background:#0e1014;border:1px solid rgba(255,255,255,0.1);
    border-radius:10px;padding:6px;display:grid;gap:1px;box-shadow:0 20px 40px -20px rgba(0,0,0,0.6);z-index:130}
  .usknav__langs-menu a{font-family:'Inter',sans-serif;font-size:12.5px;color:#c0c3c9;text-decoration:none;padding:7px 10px;border-radius:6px}
  .usknav__langs-menu a:hover{background:rgba(255,255,255,0.06);color:#f6f7f9}
  .usknav__star{display:inline-flex;align-items:center;gap:6px;white-space:nowrap;
    font-family:ui-monospace,'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;
    color:#f59e0b;text-decoration:none;border:1px solid #f59e0b;border-radius:999px;padding:7px 13px;transition:background-color 140ms ease}
  .usknav__star:hover{background:rgba(245,158,11,0.12)}
  .usknav__burger{display:none;align-items:center;background:none;border:0;cursor:pointer;padding:7px;color:#f6f7f9;min-block-size:24px;min-inline-size:24px}
  .usknav__burger svg{display:block}
  .usknav__drawer{position:fixed;inset:0;z-index:120;background:#050608;display:flex;flex-direction:column;
    padding:20px clamp(16px,5vw,40px) 40px;transform:translateX(100%);
    transition:transform 240ms cubic-bezier(0.16,1,0.3,1);overflow-y:auto;visibility:hidden}
  .usknav__drawer.is-open{transform:translateX(0);visibility:visible}
  .usknav__drawer-top{display:flex;justify-content:space-between;align-items:center;block-size:56px;
    border-block-end:1px solid rgba(255,255,255,0.1);margin-block-end:18px}
  .usknav__drawer-close{background:none;border:0;cursor:pointer;color:#f6f7f9;padding:7px;min-block-size:24px;min-inline-size:24px}
  .usknav__drawer-links{display:flex;flex-direction:column}
  .usknav__drawer-links a{font-family:'Bricolage Grotesque','Inter',sans-serif;font-size:clamp(22px,5.5vw,32px);
    color:#f6f7f9;text-decoration:none;padding:8px 0;border-block-end:1px solid rgba(255,255,255,0.06)}
  .usknav__drawer-links a:hover{color:#f59e0b}
  .usknav__drawer-star{margin-block-start:20px;align-self:flex-start}
  .usknav__drawer-langlabel{font-family:ui-monospace,'JetBrains Mono',monospace;font-size:11px;
    letter-spacing:0.1em;text-transform:uppercase;color:#8a8f96;margin:24px 0 10px}
  .usknav__drawer-langs{display:flex;flex-wrap:wrap;gap:10px 18px}
  .usknav__drawer-langs a{font-family:'Inter',sans-serif;font-size:13px;color:#8a8f96;text-decoration:none;padding:4px 0}
  .usknav__drawer-langs a:hover{color:#f6f7f9}
  /* Focus-visible: amber ring on every control (WCAG 2.4.7, >=3:1 on dark). */
  .usknav__brand:focus-visible,.usknav__link:focus-visible,.usknav__langs>summary:focus-visible,
  .usknav__star:focus-visible,.usknav__burger:focus-visible,.usknav__drawer-close:focus-visible,
  .usknav__langs-menu a:focus-visible,.usknav__drawer-links a:focus-visible,.usknav__drawer-langs a:focus-visible{
    outline:2px solid #f59e0b;outline-offset:3px;border-radius:4px}
  @media (max-width:820px){.usknav__links,.usknav__langs,.usknav__star{display:none}}
  @media (prefers-reduced-motion:reduce){.usknav__drawer{transition:none}}
""".strip("\n")

_GLOBE = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>'
          '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>')
_CARET = ('<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>')
_BURGER = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>')
_CLOSE = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>')

def _langlinks():
    out = []
    for href, name, lang, rtl in LOCALES:
        d = ' dir="rtl"' if rtl else ''
        out.append(f'<a href="{href}" lang="{lang}"{d}>{name}</a>')
    return "\n      ".join(out)

def nav_html(labels=None):
    """labels: optional {english_label: localized} for link text (locale pages)."""
    labels = labels or {}
    bar = "\n    ".join(f'<a class="usknav__link" href="{h}">{labels.get(l, l)}</a>' for h, l in LINKS)
    draw = "\n      ".join(f'<a href="{h}">{labels.get(l, l)}</a>' for h, l in DRAWER_LINKS)
    return f'''<header class="usknav" aria-label="Site navigation">
  <a class="usknav__brand" href="/">uxskill</a>
  <nav class="usknav__links" aria-label="Primary">
    {bar}
  </nav>
  <details class="usknav__langs">
    <summary aria-label="Choose language">{_GLOBE}{_CARET}</summary>
    <div class="usknav__langs-menu">
      {_langlinks()}
    </div>
  </details>
  <a class="usknav__star" href="{REPO}" rel="noopener">Star on GitHub</a>
  <button class="usknav__burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="usknav-drawer">{_BURGER}</button>
</header>
<div class="usknav__drawer" id="usknav-drawer" role="dialog" aria-modal="true" aria-label="Site menu">
  <div class="usknav__drawer-top">
    <a class="usknav__brand" href="/">uxskill</a>
    <button class="usknav__drawer-close" type="button" aria-label="Close menu">{_CLOSE}</button>
  </div>
  <nav class="usknav__drawer-links" aria-label="All pages">
    {draw}
  </nav>
  <a class="usknav__star usknav__drawer-star" href="{REPO}" rel="noopener">Star on GitHub</a>
  <div class="usknav__drawer-langlabel">Language</div>
  <div class="usknav__drawer-langs">
      {_langlinks()}
  </div>
</div>'''

# Drawer focus management: move focus in on open, trap Tab, Escape + return focus
# to the trigger on close; close the language menu on Escape / outside click.
NAV_JS = '''(function(){var d=document.getElementById('usknav-drawer');var b=document.querySelector('.usknav__burger');if(!d||!b)return;var c=d.querySelector('.usknav__drawer-close');function F(){return d.querySelectorAll('a[href],button:not([disabled])');}function set(v){d.classList.toggle('is-open',v);b.setAttribute('aria-expanded',v?'true':'false');document.body.style.overflow=v?'hidden':'';if(v){var f=c||F()[0];if(f)f.focus();}else{b.focus();}}b.addEventListener('click',function(){set(true);});if(c)c.addEventListener('click',function(){set(false);});d.addEventListener('click',function(e){if(e.target.tagName==='A')set(false);});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.classList.contains('is-open'))set(false);if(e.key==='Tab'&&d.classList.contains('is-open')){var f=F();if(!f.length)return;var a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus();}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus();}}});var L=document.querySelector('.usknav__langs');if(L){document.addEventListener('click',function(e){if(L.open&&!L.contains(e.target))L.open=false;});L.addEventListener('keydown',function(e){if(e.key==='Escape')L.open=false;});}})();'''

def preview_page():
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nav preview — uxskill</title>
<style>
  body{{margin:0;background:#07080a;min-height:220vh;font-family:'Inter',system-ui,sans-serif}}
  .sample{{padding:120px 24px;color:#8a8f96;max-width:720px;margin:0 auto;line-height:1.6}}
{NAV_CSS}
</style>
</head>
<body>
{nav_html()}
<div class="sample">Canonical nav. All 10 pages sit in the bar on desktop (no hamburger). Tab to see focus rings. Globe = language menu (17 locales). Narrow the window below ~1100px to collapse the links into a hamburger + drawer.</div>
<script>{NAV_JS}</script>
</body>
</html>'''

if __name__ == "__main__":
    open("docs/nav-preview.html", "w", encoding="utf-8").write(preview_page())
    print("wrote docs/nav-preview.html")
