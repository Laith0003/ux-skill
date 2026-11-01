"""The analytics tag every docs page carries.

The site is static, so the GA4 snippet sits inline in each page's head.
scripts/ensure-ga.py adds it to pages that lack it and checks them in CI; the
site generators call tagged() before they write, so a rebuild keeps it.
"""
from __future__ import annotations

import re

GA_ID = "G-Z371T0DBW5"

SNIPPET = (
    "<!-- Google tag (gtag.js) -->\n"
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  gtag('js', new Date());\n"
    f"  gtag('config', '{GA_ID}');\n"
    "</script>\n"
)

HEAD_RE = re.compile(r"<head\b[^>]*>", re.IGNORECASE)


def has_tag(html: str) -> bool:
    return GA_ID in html


def inject(html: str, path: str) -> str:
    m = HEAD_RE.search(html)
    if not m:
        raise ValueError(f"{path}: no <head> tag found, cannot inject GA")
    i = m.end()
    return html[:i] + "\n" + SNIPPET + html[i:]


def tagged(html: str, path: str) -> str:
    """The page with the tag: unchanged when it already carries it."""
    return html if has_tag(html) else inject(html, path)
