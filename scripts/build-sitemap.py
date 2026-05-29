#!/usr/bin/env python3
"""
Generate docs/sitemap.xml by scanning docs/ for canonical HTML pages.

The sitemap was hand-maintained and drifted as pages were added: four nav-linked
product pages (anti-patterns, brands, mcp, showcase), two English posts, and the
newer translated posts were never added. This regenerates the whole file from the
filesystem so it can never silently drift again.

Excluded (non-canonical, must NOT be indexed):
  - index-classic.html : a duplicate of the homepage (same title); indexing it
    would compete with "/".
  - launch/**          : marketing collateral and OG-share pages (facebook-*.html),
    not organic landing pages.
  - any page carrying <meta name="robots" content="noindex">.

lastmod is the file's last git commit date (best-effort; falls back to today).
Output is sorted deterministically (priority desc, then URL) for clean diffs.
Run with /usr/bin/python3.
"""
from __future__ import annotations
import glob, os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
BASE = "https://uxskill.laithjunaidy.com/"
LOCALES = {"ar", "de", "es", "fr", "hi", "id", "it", "ja", "ko",
           "pt-BR", "ru", "th", "tr", "vi", "zh-CN", "zh-TW"}
TODAY = datetime.date.today().isoformat()


def excluded(rel):
    if rel == "index-classic.html":
        return True
    if rel.startswith("launch/"):
        return True
    return False


def url_for(rel):
    # docs-relative path -> absolute URL ("dir/index.html" -> "dir/")
    if rel == "index.html":
        return BASE
    if rel.endswith("/index.html"):
        return BASE + rel[: -len("index.html")]
    return BASE + rel


def rank(rel):
    """Return (priority, changefreq) for a docs-relative path."""
    parts = rel.split("/")
    top = parts[0]
    if rel == "index.html":
        return ("1.0", "weekly")
    if len(parts) == 1:  # top-level page
        if rel in ("compare.html", "anti-patterns.html", "brands.html",
                   "mcp.html", "showcase.html", "commands.html"):
            return ("0.9", "weekly")
        return ("0.6", "monthly")  # about, faq, roadmap, privacy
    if top == "blog":
        if rel == "blog/index.html":
            return ("0.8", "weekly")
        if len(parts) == 3 and parts[2] == "index.html":  # blog/<loc>/index.html
            return ("0.5", "weekly")
        if len(parts) == 3:  # blog/<loc>/<post>.html (translated)
            return ("0.5", "monthly")
        return ("0.7", "monthly")  # blog/<post>.html (English)
    if top in LOCALES and len(parts) == 2 and parts[1] == "index.html":
        return ("0.7", "monthly")  # locale homepage
    return ("0.5", "monthly")


def has_noindex(path):
    s = open(path, encoding="utf-8").read(8192)
    return bool(re.search(r'name="robots"[^>]*noindex', s, re.I))


def lastmod(path):
    try:
        out = subprocess.run(
            ["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", path],
            capture_output=True, text=True, timeout=10)
        d = out.stdout.strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
            return d
    except Exception:
        pass
    return TODAY


def main():
    entries = []
    skipped = []
    for path in glob.glob(os.path.join(DOCS, "**", "*.html"), recursive=True):
        rel = os.path.relpath(path, DOCS).replace(os.sep, "/")
        if excluded(rel):
            skipped.append(rel)
            continue
        if has_noindex(path):
            skipped.append(rel + " (noindex)")
            continue
        prio, freq = rank(rel)
        entries.append((url_for(rel), lastmod(path), freq, prio))
    # deterministic order: priority desc, then URL asc
    entries.sort(key=lambda e: (-float(e[3]), e[0]))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lm, freq, prio in entries:
        lines.append("  <url>")
        lines.append("    <loc>" + loc + "</loc>")
        lines.append("    <lastmod>" + lm + "</lastmod>")
        lines.append("    <changefreq>" + freq + "</changefreq>")
        lines.append("    <priority>" + prio + "</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"
    open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8").write(out)

    print("sitemap.xml: " + str(len(entries)) + " urls")
    print("excluded: " + str(len(skipped)))
    for s in sorted(skipped):
        print("  - " + s)


if __name__ == "__main__":
    main()
