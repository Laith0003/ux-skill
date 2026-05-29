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
    reapply = 'class="usknav"' in s
    if not reapply and '<header' not in s:
        return 'skip (no header)'
    loc = locale_of(path)
    labels = LABELS_BY_LOCALE.get(loc) if loc else None
    nav = CN.nav_html(labels)
    if reapply:
        # remove the existing canonical nav entirely (header + drawer + css + js)
        s = re.sub(r'<header class="usknav".*?</header>\s*', '', s, count=1, flags=re.S)
        s = _strip_balanced_div(s, '<div class="usknav__drawer"')
        s = re.sub(r'<style id="usknav-css">.*?</style>\s*', '', s, flags=re.S)
        s = re.sub(r'<script id="usknav-js">.*?</script>\s*', '', s, flags=re.S)
    else:
        # first time: remove the legacy header + its drawer + any standalone crumb nav
        s, n = re.subn(r'<header\b[^>]*>.*?</header>\s*', '', s, count=1, flags=re.S)
        if n != 1:
            return 'skip (header regex miss)'
        s = _strip_balanced_div(s, '<div class="nav__drawer"')
        s = re.sub(r'<nav class="crumbs"[^>]*>.*?</nav>\s*', '', s, flags=re.S)
    # inject the nav as a direct <body> child, AFTER a leading skip-link if present,
    # so it is always full-width (never trapped inside a .wrap container).
    m = re.search(r'<body[^>]*>\s*(?:<a\b[^>]*class="[^"]*skip-link[^"]*"[^>]*>.*?</a>\s*)?', s, re.S)
    if not m:
        return 'skip (no body)'
    s = s[:m.end()] + nav + '\n' + s[m.end():]
    # (re-)inject CSS + JS
    if 'id="usknav-css"' not in s:
        s = s.replace('</head>', f'<style id="usknav-css">{CN.NAV_CSS}</style>\n</head>', 1)
    if 'id="usknav-js"' not in s:
        s = s.replace('</body>', f'<script id="usknav-js">{CN.NAV_JS}</script>\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    return ('reapplied' if reapply else 'applied') + (f' [{loc}]' if loc else '')

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
