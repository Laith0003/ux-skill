#!/usr/bin/env python3
"""
Build per-locale blog index pages at docs/blog/<locale>/index.html.

Why: the blog has translated POSTS under /blog/<locale>/ but never had a locale
index, so /blog/ar/ etc. looked empty and the locale homepages' Blog link sent
readers to the English blog. This generates a real index per locale that lists
that locale's posts and links back to the full English blog.

Approach (per the review): clone docs/blog/index.html (reuse its head/style/nav/
footer + .post-list/.post card CSS), swap in localized chrome (only the reliable
"Blog" word + the language autonym; the rest is an English-blog link, so we do
NOT hand-translate sentences into 12 languages), and emit a reciprocal +
self-referential hreflang cluster across the index pages (NOT per-post — post
slugs differ from English and need an explicit map, done separately).

Idempotent: re-run any time the locale post set changes. Run with /usr/bin/python3.
"""
from __future__ import annotations
import re, glob, os, html as _html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "docs", "blog")
BASE_URL = "https://uxskill.laithjunaidy.com"

# locale -> (autonym, localized "Blog" word, rtl?)
LOCALES = {
    "ar":    ("العربية",   "المدوّنة", True),
    "de":    ("Deutsch",    "Blog",     False),
    "es":    ("Español",    "Blog",     False),
    "fr":    ("Français",   "Blog",     False),
    "hi":    ("हिन्दी",      "ब्लॉग",     False),
    "it":    ("Italiano",   "Blog",     False),
    "ja":    ("日本語",      "ブログ",    False),
    "ko":    ("한국어",      "블로그",    False),
    "pt-BR": ("Português",  "Blog",     False),
    "vi":    ("Tiếng Việt", "Blog",     False),
    "zh-CN": ("简体中文",    "博客",      False),
    "zh-TW": ("繁體中文",    "部落格",    False),
}

def clean_title(t: str) -> str:
    t = t.strip()
    # strip a trailing site suffix " — ux-skill" / " · ux-skill" / " - ux-skill"
    t = re.sub(r'\s*[—\-·|]\s*ux-skill\s*$', '', t, flags=re.I)
    return t.strip()

def locale_posts(loc: str):
    out = []
    for f in sorted(glob.glob(os.path.join(BLOG, loc, "*.html"))):
        if os.path.basename(f) == "index.html":
            continue
        h = open(f, encoding="utf-8").read()
        m = re.search(r'<title>(.*?)</title>', h, re.S)
        title = clean_title(m.group(1)) if m else os.path.basename(f)
        out.append((os.path.basename(f), title))
    return out

def hreflang_block(indent="") -> str:
    lines = [f'<link rel="alternate" hreflang="en" href="{BASE_URL}/blog/">']
    for loc in LOCALES:
        lines.append(f'<link rel="alternate" hreflang="{loc}" href="{BASE_URL}/blog/{loc}/">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/blog/">')
    return "\n".join(indent + l for l in lines) + "\n"

def build_one(base: str, loc: str) -> str:
    autonym, blogw, rtl = LOCALES[loc]
    h = base

    # 1) <html lang/dir>
    assert '<html lang="en">' in h, "no <html lang=en> anchor"
    dirattr = ' dir="rtl"' if rtl else ''
    h = h.replace('<html lang="en">', f'<html lang="{loc}"{dirattr}>', 1)

    # 2) <title>
    title = f"{blogw} · {autonym} · ux-skill"
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', h, count=1, flags=re.S)

    # 3) meta description
    desc = f"{blogw} ({autonym}) · ux-skill. Posts available in {autonym}, with the full archive in English."
    h = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + desc + m.group(2), h, count=1)

    # 4) canonical + og:url -> /blog/<loc>/
    h = h.replace(f'href="{BASE_URL}/blog/"', f'href="{BASE_URL}/blog/{loc}/"')
    h = h.replace(f'content="{BASE_URL}/blog/"', f'content="{BASE_URL}/blog/{loc}/"')

    # 5) intro: eyebrow + h1 + lede
    h = re.sub(r'<span class="eyebrow">.*?</span>',
               f'<span class="eyebrow">{blogw} &middot; {autonym}</span>', h, count=1, flags=re.S)
    h = re.sub(r'<h1>.*?</h1>', f'<h1>{blogw}</h1>', h, count=1, flags=re.S)
    h = re.sub(r'<p class="lede">.*?</p>',
               '<p class="lede"><a href="/blog/">Read the full blog in English &rarr;</a></p>',
               h, count=1, flags=re.S)

    # 6) post-list -> locale cards
    cards = []
    for fname, title in locale_posts(loc):
        cards.append(
            f'      <li class="post"><a href="/blog/{loc}/{fname}">\n'
            f'        <div class="post-meta"><span class="tag">{blogw}</span> &middot; {autonym}</div>\n'
            f'        <h2>{title}</h2>\n'
            f'      </a></li>'
        )
    new_list = '<ul class="post-list">\n' + "\n\n".join(cards) + '\n    </ul>'
    h = re.sub(r'<ul class="post-list">.*?</ul>', lambda m: new_list, h, count=1, flags=re.S)

    # 7) hreflang cluster before </head> (idempotent; base may already carry it)
    if 'hreflang="x-default"' not in h:
        h = h.replace('</head>', hreflang_block() + '</head>', 1)
    return h

def main():
    base = open(os.path.join(BLOG, "index.html"), encoding="utf-8").read()
    # add the same reciprocal hreflang cluster to the English blog index (once)
    if 'hreflang="x-default"' not in base:
        base_en = base.replace('</head>', hreflang_block() + '</head>', 1)
        open(os.path.join(BLOG, "index.html"), "w", encoding="utf-8").write(base_en)
        print("added hreflang cluster to EN blog/index.html")
        base = base_en

    for loc in LOCALES:
        out = build_one(base, loc)
        d = os.path.join(BLOG, loc)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
        n = len(locale_posts(loc))
        print(f"  wrote /blog/{loc}/index.html  ({n} posts)")

if __name__ == "__main__":
    main()
