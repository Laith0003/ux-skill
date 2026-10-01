"""A page family: inner pages built in one run that share one frame.

``build_family`` turns the sequences ``select_for_brief`` picks for each
inner page into skeleton HTML. Every page opens on its secondary hero (the
page's one h1, one line, one action and a photograph), lays out the
sections between, and closes on the site's closing band and sitemap
footer. The header, the closing band and the footer are one instance each,
written once and placed byte for byte on every page, so the site reads as
one. Styles bind the design system's custom properties only.

Section bodies are the sequence's own purpose lines: a skeleton that shows
what each section must hold, ready for the client's copy. Photographs are
required: pass at least one, sourced by the system's photo direction. Only
a system that forbids photography builds without them, and the page says
so where the photograph would sit.
"""
from __future__ import annotations

import html
import re
from typing import Dict, List, Mapping, Optional, Sequence

from engine.page_sequence.core import INNER_PAGES, select_for_brief

TITLES: Mapping[str, str] = {"pricing": "Pricing", "about": "About", "contact": "Contact",
                             "customers": "Customers", "customer-story": "Customer story",
                             "legal": "Legal"}

_STYLE = """
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--color-surface-page);color:var(--color-text-default);
  font-family:var(--type-text-body-font-family);font-size:var(--type-text-body-font-size);
  line-height:var(--type-text-body-line-height,1.5)}
img{max-width:100%;height:auto;display:block}
a{color:var(--color-text-link)}
.frame{max-width:var(--layout-container-max);margin-inline:auto;
  padding-inline:var(--layout-margin-inline)}
.site-header .frame{display:flex;flex-wrap:wrap;align-items:center;gap:var(--layout-gutter);
  justify-content:space-between;padding-block:var(--space-4)}
.site-header{background:var(--color-surface-header);
  border-block-end:1px solid var(--color-hairline)}
.brand{font-family:var(--type-face-display);font-weight:600;text-decoration:none;
  color:var(--color-text-default)}
.site-nav ul{display:flex;flex-wrap:wrap;gap:var(--space-2) var(--space-6);margin:0;padding:0;
  list-style:none}
.site-nav a{display:inline-block;min-height:24px;padding-block:var(--space-1);
  color:var(--color-text-default);text-decoration:none}
.site-nav a[aria-current=page]{text-decoration:underline;text-underline-offset:0.3em}
.action{display:inline-flex;align-items:center;min-height:44px;
  padding:var(--space-3) var(--space-6);border-radius:var(--radius-control);
  background:var(--color-action-primary);
  color:var(--color-text-on-action);text-decoration:none;font-weight:600}
.hero .frame{display:grid;gap:var(--layout-gutter);align-items:end;
  padding-block:var(--layout-hero-padding-block,var(--space-16))}
.hero h1{margin:0;font-family:var(--type-text-heading-1-font-family);
  font-size:var(--type-text-heading-1-font-size);
  font-weight:var(--type-text-heading-1-font-weight);
  line-height:var(--type-text-heading-1-line-height);
  letter-spacing:var(--type-text-heading-1-letter-spacing);overflow-wrap:break-word}
.hero p{max-width:var(--layout-measure-landing);margin:var(--space-4) 0 var(--space-6)}
.hero figure{margin:0}
.hero img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--radius-card)}
.section{padding-block:calc(var(--layout-landing-gap) / 2)}
.section h2{margin:0 0 var(--space-4);font-family:var(--type-text-section-title-font-family);
  font-size:var(--type-text-section-title-font-size);
  font-weight:var(--type-text-section-title-font-weight);
  line-height:var(--type-text-section-title-line-height);overflow-wrap:break-word}
.section p{max-width:var(--layout-measure-text);margin:0}
.closing-band{background:var(--color-surface-band);padding-block:var(--layout-landing-gap)}
.closing-band h2{margin:0 0 var(--space-6);font-family:var(--type-text-section-title-font-family);
  font-size:var(--type-text-section-title-font-size);overflow-wrap:break-word}
.site-footer{padding-block:var(--space-12);border-block-start:1px solid var(--color-hairline)}
.site-footer ul{display:grid;grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));
  gap:var(--space-2) var(--layout-gutter);margin:0;padding:0;list-style:none}
.site-footer a{display:inline-block;min-height:24px;padding-block:var(--space-1)}
.draft{margin:0;padding:var(--space-6);border:1px dashed var(--color-hairline)}
@media (min-width: 1024px){.hero .frame{grid-template-columns:1fr 1fr}}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
"""


def _title(section: str) -> str:
    """A section's heading: its name without the note in parentheses."""
    return re.sub(r"\s*\([^)]*\)", "", section).strip()


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _header(brand: str, pages: Sequence[str], action: str) -> str:
    links = "".join(f'<li><a href="{p}.html">{_esc(TITLES[p])}</a></li>' for p in pages)
    return ('<header class="site-header" data-family="header"><div class="frame">'
            f'<a class="brand" href="index.html">{_esc(brand)}</a>'
            f'<nav class="site-nav" aria-label="Site"><ul>{links}</ul></nav>'
            f'<a class="action" href="#start">{_esc(action)}</a></div></header>')


def _closing_band(line: str, action: str) -> str:
    return ('<section class="closing-band" data-family="closing-band" aria-labelledby="closing">'
            f'<div class="frame"><h2 id="closing">{_esc(line)}</h2>'
            f'<a class="action" href="#start">{_esc(action)}</a></div></section>')


def _footer(brand: str, pages: Sequence[str]) -> str:
    links = "".join(f'<li><a href="{p}.html">{_esc(TITLES[p])}</a></li>' for p in pages)
    return ('<footer class="site-footer" data-family="footer"><div class="frame">'
            f'<nav aria-label="Sitemap"><ul><li><a href="index.html">{_esc(brand)}</a></li>'
            f'{links}</ul></nav></div></footer>')


def _hero(page: str, purpose: str, action: str, photo: Optional[str], alt: str) -> str:
    figure = (f'<figure><img src="{_esc(photo)}" alt="{_esc(alt)}" width="1200" height="900">'
              '</figure>' if photo else
              '<p class="draft">No photograph: the client\'s system forbids photography.</p>')
    return ('<section class="hero" aria-labelledby="page-title"><div class="frame"><div>'
            f'<h1 id="page-title">{_esc(TITLES[page])}</h1><p>{_esc(purpose)}</p>'
            f'<a class="action" id="start" href="#start">{_esc(action)}</a></div>'
            f'{figure}</div></section>')


def build_family(pages: Sequence[str], css: str, *, brand: str, action: str,
                 photos: Sequence[str] = (), photo_alts: Sequence[str] = (),
                 photography_forbidden: bool = False, closing_line: str = "",
                 brief: Optional[Mapping[str, object]] = None) -> Dict[str, str]:
    """HTML for each inner page in ``pages``, keyed by page, sharing one
    header, one closing band and one footer instance. ``css`` is the design
    system's custom properties (to_css). ``photos`` are the photographs the
    heroes take in turn, with ``photo_alts`` describing each. The header
    marks the page it sits on with aria-current; nothing else differs."""
    if not pages:
        raise ValueError("pages: name at least one inner page, from "
                         + ", ".join(sorted(INNER_PAGES)))
    unknown = [p for p in pages if p not in INNER_PAGES]
    if unknown:
        raise ValueError(f"pages: {', '.join(unknown)} is not an inner page; use one of "
                         + ", ".join(sorted(INNER_PAGES)))
    if len(set(pages)) != len(pages):
        raise ValueError("pages: each page is built once in a family; remove the repeat")
    if not photos and not photography_forbidden:
        raise ValueError("photos: a page family needs at least one photograph; pass photos "
                         "sourced by the system's photo direction (only a system that forbids "
                         "photography sets photography_forbidden)")
    if photos and len(photo_alts) != len(photos):
        raise ValueError("photo_alts: give one description per photograph in photos")
    if not brand.strip() or not action.strip():
        raise ValueError("brand and action: name the site and its primary action, in the "
                         "words the home page uses")
    seqs = {p: select_for_brief({**(brief or {}), "page": p})["section_sequence"] for p in pages}
    header = _header(brand, pages, action)
    closing = _closing_band(closing_line or action, action)
    footer = _footer(brand, pages)
    out: Dict[str, str] = {}
    for i, page in enumerate(pages):
        secs = seqs[page]
        middle = [s for s in secs[1:] if not s["section"].startswith(("Closing band",
                                                                       "Rich footer"))]
        photo = photos[i % len(photos)] if photos else None
        alt = photo_alts[i % len(photo_alts)] if photos else ""
        here = header.replace(f'<a href="{page}.html">',
                              f'<a href="{page}.html" aria-current="page">')
        body: List[str] = [here, "<main>", _hero(page, secs[0]["purpose"], action, photo, alt)]
        for n, s in enumerate(middle, 1):
            body.append(f'<section class="section" aria-labelledby="s{n}"><div class="frame">'
                        f'<h2 id="s{n}">{_esc(_title(s["section"]))}</h2>'
                        f'<p>{_esc(s["purpose"])}</p></div></section>')
        body += [closing, "</main>", footer]
        out[page] = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                     '<meta name="viewport" content="width=device-width, initial-scale=1">'
                     f'<title>{_esc(TITLES[page])} | {_esc(brand)}</title>'
                     f'<style>{css}{_STYLE}</style></head><body>{"".join(body)}</body></html>')
    return out
