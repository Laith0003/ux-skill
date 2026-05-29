#!/usr/bin/env python3
"""
Apply the canonical nav (scripts/canonical_nav.py) to a set of HTML pages.

For each page: strip the existing <header>...</header> (any of the nav / nav__row
/ top-crumbs variants) and an immediately-following rich-nav drawer div if present,
then inject the canonical nav HTML in its place, the canonical CSS as a dedicated
<style id="usknav-css"> before </head>, and the canonical JS as <script id="usknav-js">
before </body>. Idempotent (skips pages already carrying .usknav).

Usage: apply_canonical_nav.py <glob-or-path> [<glob-or-path> ...]
Locale label localization is applied automatically for /<loc>/ and /blog/<loc>/ pages
when a translation map is available (see LABELS_BY_LOCALE; falls back to English).
"""
from __future__ import annotations
import re, sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canonical_nav as CN

# Per-locale label map (English label -> localized), loaded from the site's own
# i18n-strings.json so we reuse existing translations (no invention). Labels with
# no translation (MCP, Showcase) stay English.
def _load_labels():
    import json
    try:
        d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'i18n-strings.json'), encoding='utf-8'))
    except Exception:
        return {}
    labels = {l for _, l in CN.LINKS}
    by = {}
    for v in d.get('strings', {}).values():
        if isinstance(v, dict) and v.get('en') in labels:
            en = v['en']
            for loc, val in v.items():
                if loc != 'en' and isinstance(val, str) and val:
                    by.setdefault(loc, {})[en] = val
    return by

LABELS_BY_LOCALE = _load_labels()

def _strip_balanced_div(s, open_substr):
    """Remove the <div ...> ... </div> that begins at open_substr, matching nesting."""
    i = s.find(open_substr)
    if i < 0:
        return s
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return s[:i] + s[i + m.end():]
        else:
            depth += 1
    return s  # unbalanced; leave as-is

def locale_of(path):
    m = re.match(r'docs/(?:blog/)?([a-z]{2}(?:-[A-Z]{2})?)/', path)
    loc = m.group(1) if m else None
    return loc if loc in {l[2] for l in CN.LOCALES} and loc != 'en' else None

def transform(path):
    s = open(path, encoding='utf-8').read()
    if 'class="usknav"' in s:
        return 'skip (already applied)'
    if '<header' not in s:
        return 'skip (no header)'
    loc = locale_of(path)
    labels = LABELS_BY_LOCALE.get(loc) if loc else None
    nav = CN.nav_html(labels)
    # 1) replace the first <header>...</header> with a marker
    s2, n = re.subn(r'<header\b[^>]*>.*?</header>', '\x00NAV\x00', s, count=1, flags=re.S)
    if n != 1:
        return 'skip (header regex miss)'
    # 2) remove a rich-nav drawer div that followed the header (balanced match)
    s2 = _strip_balanced_div(s2, '<div class="nav__drawer"')
    # 2b) remove any standalone breadcrumb nav some rich pages carry in the body
    s2 = re.sub(r'<nav class="crumbs"[^>]*>.*?</nav>\s*', '', s2, flags=re.S)
    # 3) drop in canonical nav
    s2 = s2.replace('\x00NAV\x00', nav, 1)
    # 4) inject CSS + JS once
    s2 = s2.replace('</head>', f'<style id="usknav-css">{CN.NAV_CSS}</style>\n</head>', 1)
    s2 = s2.replace('</body>', f'<script id="usknav-js">{CN.NAV_JS}</script>\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s2)
    return f'applied{" ["+loc+"]" if loc else ""}'

def main(argv):
    files = []
    for a in argv:
        files.extend(sorted(glob.glob(a, recursive=True)))
    done = {}
    for f in files:
        r = transform(f)
        done.setdefault(r.split(' ')[0], []).append(f)
    for k, v in sorted(done.items()):
        print(f"{k}: {len(v)}")
    return done

if __name__ == "__main__":
    main(sys.argv[1:])
