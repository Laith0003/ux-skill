#!/usr/bin/env python3
"""
Canonical site nav component for ux-skill docs — single source of truth.

One identical nav on every page: a sticky bar (brand + links + language globe +
Star CTA) that collapses to a hamburger + drawer on mobile. Self-contained:
namespaced `.usknav` classes, hardcoded dark-cinema colors (so it renders the
same regardless of each page's own CSS tokens), native <details> language menu
(no fragile JS), tiny vanilla drawer toggle.

Link set: Brands · Anti-patterns · Commands · Blog · Compare  (+ Star on GitHub).
No separate plain "GitHub" link — the Star pill is the GitHub link and the ask.

Used by the preview builder (__main__) and by the rollout apply-script.
"""
from __future__ import annotations

# (href, autonym, lang, dir-rtl?)
LOCALES = [
    ("/", "English", "en", False),
    ("/zh-CN/", "简体中文", "zh-CN", False),
    ("/zh-TW/", "繁體中文", "zh-TW", False),
    ("/ja/", "日本語", "ja", False),
    ("/ko/", "한국어", "ko", False),
    ("/hi/", "हिन्दी", "hi", False),
    ("/id/", "Bahasa Indonesia", "id", False),
    ("/vi/", "Tiếng Việt", "vi", False),
    ("/th/", "ไทย", "th", False),
    ("/ar/", "العربية", "ar", True),
    ("/es/", "Español", "es", False),
    ("/fr/", "Français", "fr", False),
    ("/de/", "Deutsch", "de", False),
    ("/pt-BR/", "Português", "pt-BR", False),
    ("/ru/", "Русский", "ru", False),
    ("/tr/", "Türkçe", "tr", False),
    ("/it/", "Italiano", "it", False),
]

# Primary links: (href, English label). Labels get localized per page via i18n.
LINKS = [
    ("/brands.html", "Brands"),
    ("/anti-patterns.html", "Anti-patterns"),
    ("/commands.html", "Commands"),
    ("/blog/", "Blog"),
    ("/compare.html", "Compare"),
]
REPO = "https://github.com/Laith0003/ux-skill"

NAV_CSS = """
  .usknav{position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:18px;
    padding:0 clamp(16px,4vw,48px);block-size:56px;background:rgba(7,8,10,0.86);
    backdrop-filter:saturate(150%) blur(14px);-webkit-backdrop-filter:saturate(150%) blur(14px);
    border-block-end:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif}
  .usknav__brand{font-family:'Bricolage Grotesque','Inter',sans-serif;font-weight:700;font-size:17px;
    color:#f6f7f9;text-decoration:none;letter-spacing:-0.01em;margin-inline-end:auto}
  .usknav__links{display:flex;align-items:center;gap:clamp(12px,2vw,26px)}
  .usknav__link{font-family:ui-monospace,'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:0.08em;
    text-transform:uppercase;color:#8a8f96;text-decoration:none;white-space:nowrap;transition:color 140ms ease}
  .usknav__link:hover,.usknav__link[aria-current="page"]{color:#f6f7f9}
  .usknav__langs{position:relative}
  .usknav__langs>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:5px;
    color:#8a8f96;padding:6px;transition:color 140ms ease}
  .usknav__langs>summary::-webkit-details-marker{display:none}
  .usknav__langs>summary:hover{color:#f6f7f9}
  .usknav__langs-menu{position:absolute;top:calc(100% + 8px);inset-inline-end:0;min-inline-size:184px;
    max-block-size:60vh;overflow-y:auto;background:#0e1014;border:1px solid rgba(255,255,255,0.1);
    border-radius:10px;padding:6px;display:grid;gap:1px;box-shadow:0 20px 40px -20px rgba(0,0,0,0.6);z-index:130}
  .usknav__langs-menu a{font-family:'Inter',sans-serif;font-size:12.5px;color:#c0c3c9;text-decoration:none;
    padding:7px 10px;border-radius:6px}
  .usknav__langs-menu a:hover{background:rgba(255,255,255,0.06);color:#f6f7f9}
  .usknav__star{display:inline-flex;align-items:center;gap:6px;white-space:nowrap;
    font-family:ui-monospace,'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;
    color:#f59e0b;text-decoration:none;border:1px solid #f59e0b;border-radius:999px;padding:5px 12px;transition:background-color 140ms ease}
  .usknav__star:hover{background:rgba(245,158,11,0.12)}
  .usknav__burger{display:none;background:none;border:0;cursor:pointer;padding:6px;color:#f6f7f9}
  .usknav__burger svg{display:block}
  .usknav__drawer{position:fixed;inset:0;z-index:120;background:#050608;display:flex;flex-direction:column;
    padding:20px clamp(16px,5vw,40px) 40px;transform:translateX(100%);
    transition:transform 240ms cubic-bezier(0.16,1,0.3,1);overflow-y:auto;visibility:hidden}
  .usknav__drawer.is-open{transform:translateX(0);visibility:visible}
  .usknav__drawer-top{display:flex;justify-content:space-between;align-items:center;block-size:56px;
    border-block-end:1px solid rgba(255,255,255,0.1);margin-block-end:20px}
  .usknav__drawer-close{background:none;border:0;cursor:pointer;color:#f6f7f9;padding:6px}
  .usknav__drawer-links{display:flex;flex-direction:column}
  .usknav__drawer-links a{font-family:'Bricolage Grotesque','Inter',sans-serif;font-size:clamp(26px,7vw,38px);
    color:#f6f7f9;text-decoration:none;padding:9px 0;border-block-end:1px solid rgba(255,255,255,0.06)}
  .usknav__drawer-links a:hover{color:#f59e0b}
  .usknav__drawer-star{margin-block-start:22px;align-self:flex-start}
  .usknav__drawer-langlabel{font-family:ui-monospace,'JetBrains Mono',monospace;font-size:11px;
    letter-spacing:0.1em;text-transform:uppercase;color:#8a8f96;margin:26px 0 10px}
  .usknav__drawer-langs{display:flex;flex-wrap:wrap;gap:8px 18px}
  .usknav__drawer-langs a{font-family:'Inter',sans-serif;font-size:13px;color:#8a8f96;text-decoration:none}
  .usknav__drawer-langs a:hover{color:#f6f7f9}
  @media (max-width:820px){.usknav__links,.usknav__langs,.usknav__star{display:none}.usknav__burger{display:inline-flex}}
  @media (prefers-reduced-motion:reduce){.usknav__drawer{transition:none}}
""".strip("\n")

_GLOBE = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>'
          '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>')
_CARET = ('<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>')
_BURGER = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>')
_CLOSE = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>')

def _langlinks(cls=""):
    out = []
    for href, name, lang, rtl in LOCALES:
        d = ' dir="rtl"' if rtl else ''
        out.append(f'<a href="{href}" lang="{lang}"{d}>{name}</a>')
    return "\n      ".join(out)

def nav_html(labels=None):
    """labels: optional {english_label: localized} for the 5 primary links."""
    labels = labels or {}
    bar_links = "\n    ".join(
        f'<a class="usknav__link" href="{href}">{labels.get(lbl, lbl)}</a>' for href, lbl in LINKS)
    drawer_links = "\n      ".join(
        f'<a href="{href}">{labels.get(lbl, lbl)}</a>' for href, lbl in LINKS)
    return f'''<header class="usknav" aria-label="Site navigation">
  <a class="usknav__brand" href="/">uxskill</a>
  <nav class="usknav__links" aria-label="Primary">
    {bar_links}
  </nav>
  <details class="usknav__langs">
    <summary aria-label="Language">{_GLOBE}{_CARET}</summary>
    <div class="usknav__langs-menu">
      {_langlinks()}
    </div>
  </details>
  <a class="usknav__star" href="{REPO}" rel="noopener">Star on GitHub</a>
  <button class="usknav__burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="usknav-drawer">{_BURGER}</button>
</header>
<div class="usknav__drawer" id="usknav-drawer" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="usknav__drawer-top">
    <a class="usknav__brand" href="/">uxskill</a>
    <button class="usknav__drawer-close" type="button" aria-label="Close menu">{_CLOSE}</button>
  </div>
  <nav class="usknav__drawer-links" aria-label="Primary">
    {drawer_links}
  </nav>
  <a class="usknav__star usknav__drawer-star" href="{REPO}" rel="noopener">Star on GitHub</a>
  <div class="usknav__drawer-langlabel">Language</div>
  <div class="usknav__drawer-langs">
      {_langlinks()}
  </div>
</div>'''

NAV_JS = '''(function(){var d=document.getElementById('usknav-drawer');var o=document.querySelector('.usknav__burger');var c=d&&d.querySelector('.usknav__drawer-close');if(!d||!o)return;function s(v){d.classList.toggle('is-open',v);o.setAttribute('aria-expanded',v?'true':'false');document.body.style.overflow=v?'hidden':'';}o.addEventListener('click',function(){s(true);});if(c)c.addEventListener('click',function(){s(false);});d.addEventListener('click',function(e){if(e.target.tagName==='A')s(false);});document.addEventListener('keydown',function(e){if(e.key==='Escape')s(false);});})();'''

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
<div class="sample">Canonical nav preview. One link to GitHub (the Star pill). Globe = language menu (17 locales). Narrow the window to see the hamburger + drawer.</div>
<script>{NAV_JS}</script>
</body>
</html>'''

if __name__ == "__main__":
    open("docs/nav-preview.html", "w", encoding="utf-8").write(preview_page())
    print("wrote docs/nav-preview.html")
