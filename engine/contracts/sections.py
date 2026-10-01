"""Section contracts rendered as skeleton HTML.

render_section turns one section contract and a variant choice into a
``<section>`` and the CSS its bindings ask for: every value is a var() of a
bound semantic role, read from the design system's tokens.css, and the
phone recomposition the contract lists runs below the tablet width in its
fixed order. The copy is the contract's own description and job, a
skeleton that shows what the section holds; photographs are required and
passed in, sourced by the system's photo direction.

A tier role (layout.landing-gap.desktop) binds the tier-less alias that
tokens.css switches per tier (--layout-landing-gap), so the section takes
the phone value on a phone.
"""
from __future__ import annotations

import html
import re
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

from engine.contracts.schema import Binding, Contract

TIERS = ("desktop", "laptop", "tablet", "phone")
# Below this width the phone recomposition runs; plans switch below the
# tablet width.
PHONE_PX = 640
TABLET_PX = 1024
HEROES = ("hero", "secondary-hero")
_TYPOGRAPHY = ("font-family", "font-size", "font-weight", "line-height", "letter-spacing")


def css_var(role: str) -> str:
    """The custom property a role is written as; a tier role names the
    alias tokens.css switches per tier."""
    parts = role.split(".")
    if parts[-1] in TIERS and parts[0] == "layout":
        parts = parts[:-1]
    return "--" + "-".join(parts)


def _declarations(prop: str, role: str) -> List[str]:
    v = f"var({css_var(role)})"
    if prop == "font":
        return [f"{p}: var({css_var(role)}-{p})" for p in _TYPOGRAPHY]
    return {
        "fill": [f"background-color: {v}"], "text": [f"color: {v}"], "icon": [f"color: {v}"],
        "border-color": [f"border-color: {v}"],
        "border-width": [f"border-width: {v}", "border-style: solid"],
        "radius": [f"border-radius: {v}"], "padding-inline": [f"padding-inline: {v}"],
        "padding-block": [f"padding-block: {v}"], "gap": [f"gap: {v}"],
        "stack-gap": [f"margin-block-end: {v}"], "min-size": [f"min-block-size: {v}",
                                                               f"min-inline-size: {v}"],
        "max-width": [f"max-inline-size: {v}"], "font-weight": [f"font-weight: {v}"],
        "shadow": [f"box-shadow: {v}"], "layer": [f"z-index: {v}"],
    }.get(prop, [])


def _applies(b: Binding, variant: Mapping[str, str]) -> bool:
    return b.state is None and all(variant.get(k) == v for k, v in b.when)


def _rules(c: Contract, variant: Mapping[str, str]) -> str:
    """One rule per part from the bindings that apply; a binding with more
    conditions wins over one with fewer."""
    chosen: Dict[Tuple[str, str], Binding] = {}
    for b in c.tokens:
        if not _applies(b, variant):
            continue
        key = (b.part, b.property)
        if key not in chosen or len(b.when) > len(chosen[key].when):
            chosen[key] = b
    by_part: Dict[str, List[str]] = {}
    for (part, prop), b in chosen.items():
        by_part.setdefault(part, []).extend(_declarations(prop, b.role))
    out = []
    for part, decls in by_part.items():
        sel = f".s-{c.name}" if part == "container" else f".s-{c.name} .{part}"
        inner = [d for d in decls if part == "container" and d.startswith("max-inline-size")]
        rest = [d for d in decls if d not in inner]
        if rest:
            out.append(f"{sel} {{ {'; '.join(rest)}; }}")
        if inner:  # the container's width is the content's, inside the full band
            out.append(f".s-{c.name} .inner {{ {'; '.join(inner)}; }}")
    return "\n".join(out)


def _title(name: str) -> str:
    return name.replace("-", " ").capitalize()


def _esc(t: str) -> str:
    return html.escape(t, quote=True)


def _items(kind: str, n: int, photos: Sequence[Tuple[str, str]]) -> str:
    words = ("Order ahead", "Pick up at the counter", "Eat in or take away", "Pay as you like",
             "Book a table", "Bring a group")
    lis = []
    for i in range(n):
        media = ""
        if photos and kind == "card":
            src, alt = photos[i % len(photos)]
            media = (f'<img class="media" src="{_esc(src)}" alt="{_esc(alt)}" width="640" '
                     'height="480" loading="lazy">')
        lis.append(f'<li class="item">{media}<h3 class="item-title">{_esc(words[i])}</h3>'
                   f'<p class="body">One line on what changes for the reader.</p></li>')
    tag = "ol" if kind == "steps" else "ul"
    return f'<{tag} class="items" role="list">{"".join(lis)}</{tag}>'


def _slot_html(c: Contract, slot: str, takes: Sequence[str], variant: Mapping[str, str],
               photos: Sequence[Tuple[str, str]]) -> str:
    """The markup one slot holds, by what it takes."""
    first = photos[0] if photos else ("", "")
    if "button" in takes:
        return '<a class="action" href="#book">Book a table</a>'
    if "link" in takes:
        return '<a class="action" href="#book">See the menu</a>'
    if "faq-accordion" in takes:
        qs = ("Can I book for a group?", "Do you take cards?", "Is there a vegetarian menu?")
        return "".join(f'<details class="question"><summary>{_esc(q)}</summary>'
                       '<p class="body">Yes, and the answer says how.</p></details>' for q in qs)
    if "site-footer" in takes:
        cols = (("Visit", ("Menu", "Hours", "Find us")), ("Company", ("About", "Jobs", "Press")),
                ("Help", ("Contact", "Bookings", "Privacy")))
        return '<div class="columns">' + "".join(
            f'<nav aria-label="{t}"><h3 class="item-title">{t}</h3><ul role="list">'
            + "".join(f'<li><a class="link" href="#{w.lower()}">{w}</a></li>' for w in links)
            + "</ul></nav>" for t, links in cols) + "</div>"
    if "table" in takes:
        rows = (("Booking", "Online, any hour", "By phone"), ("Groups", "Up to 20", "Up to 8"))
        return ('<div class="table"><table><caption>How it compares</caption><thead><tr>'
                '<th scope="col">What</th><th scope="col">Us</th><th scope="col">Others</th>'
                '</tr></thead><tbody>' + "".join(
                    f'<tr><th scope="row">{a}</th><td>{b}</td><td>{d}</td></tr>'
                    for a, b, d in rows) + "</tbody></table></div>")
    if "segmented-control" in takes:
        return ""  # the plan switcher is drawn with the plans
    if "card" in takes:
        if slot == "plan":
            return _plans(c)
        return _items("card", 4 if c.name == "bento" else 3, photos)
    if slot == "stat":
        stats = (("1,200", "tables served each week, 2026"), ("4.8", "average rating, 2026"),
                 ("12", "years on the same street"))
        return '<dl class="stats">' + "".join(
            f'<div><dt class="label">{_esc(l)}</dt><dd class="stat">{_esc(n)}</dd></div>'
            for n, l in stats) + "</dl>"
    if slot == "quote":
        return ('<figure class="quote-figure"><blockquote class="quote">The booking took a '
                'minute and the table was ready when we walked in.</blockquote>'
                '<figcaption><span class="name">Rana Haddad</span> '
                '<span class="role">Office manager, Harbour Studio</span></figcaption></figure>')
    if slot == "item":
        return _items("steps", 3, photos)
    if slot == "logo":
        return '<ul class="logos" role="list">' + "".join(
            f'<li><img class="logo" src="{_esc(first[0])}" alt="Partner {i + 1}" width="120" '
            'height="40"></li>' for i in range(6)) + "</ul>"
    if "interface-fragment" in takes and "photograph" not in takes:
        if variant.get("media") not in ("photograph-and-fragment", "fragment"):
            return ""
        return (f'<img class="fragment" src="{_esc(first[0])}" alt="The booking screen" '
                'width="800" height="600">')
    if "photograph" in takes:
        if not first[0]:
            return ""
        return (f'<figure class="media-figure"><img class="media" src="{_esc(first[0])}" '
                f'alt="{_esc(first[1])}" width="1200" height="800"></figure>')
    return ""


def _plans(c: Contract) -> str:
    plans = (("Lunch", "12", "Two courses at midday"), ("Dinner", "24", "Three courses, our "
             "recommended plan"), ("Group", "40", "A set menu for eight or more"))
    radios = "".join(
        f'<input type="radio" name="plan-{c.name}" id="plan-{c.name}-{i}" class="switch"'
        f'{" checked" if i == 1 else ""}><label for="plan-{c.name}-{i}">{p}</label>'
        for i, (p, _, _) in enumerate(plans))
    cards = "".join(
        f'<li class="plan{" recommended" if i == 1 else ""}" data-plan="{i}">'
        f'<h3 class="item-title">{p}{" (recommended)" if i == 1 else ""}</h3>'
        f'<p class="price">{price}</p><p class="body">{_esc(d)}</p>'
        f'<a class="action" href="#plan-{i}">Choose {p}</a></li>'
        for i, (p, price, d) in enumerate(plans))
    return (f'<div class="switcher" role="radiogroup" aria-label="Plans">{radios}</div>'
            f'<ul class="plans" role="list">{cards}</ul>')


def _layout_css(c: Contract) -> str:
    """Grid and recomposition rules, with the phone steps the contract
    lists, in their fixed order."""
    s = f".s-{c.name}"
    out = [
        f"{s} {{ display: block; margin-inline: auto; box-sizing: border-box; }}",
        f"{s} .inner {{ display: grid; gap: var(--layout-gutter); max-inline-size: "
        "var(--layout-container-max); margin-inline: auto; }",
        f"{s} img {{ max-inline-size: 100%; block-size: auto; display: block; }}",
        f"{s} h1, {s} h2, {s} h3 {{ margin: 0; overflow-wrap: break-word; }}",
        f"{s} .items, {s} .logos, {s} .plans, {s} .stats {{ list-style: none; margin: 0; "
        "padding: 0; display: grid; gap: var(--space-group-gap); grid-template-columns: "
        "repeat(auto-fit, minmax(min(100%, 14rem), 1fr)); }",
        f"{s} .logos {{ grid-template-columns: repeat(auto-fit, minmax(min(100%, 7rem), 1fr)); }}",
        f"{s} .action {{ display: inline-flex; align-items: center; justify-content: center; "
        "min-block-size: var(--layout-target-large); padding-inline: "
        "var(--space-control-padding-inline-large); border-radius: var(--radius-control); "
        "background-color: var(--color-action-primary); color: var(--color-text-on-action); "
        "font-weight: 600; text-decoration: none; justify-self: start; }",
        f"{s} .item, {s} .plan {{ display: grid; gap: var(--space-text-gap); "
        "align-content: start; }",
        f"{s} .stats dd {{ margin: 0; }} {s} .stats > div {{ display: flex; "
        "flex-direction: column-reverse; gap: var(--space-text-gap); }",
        f"{s} .quote {{ margin: 0; }} {s} .quote-figure {{ margin: 0; display: grid; "
        "gap: var(--space-text-gap); align-content: center; }",
        f"{s} .media-figure {{ margin: 0; }}",
        f"{s} .text:has(> .sr-only:only-child) {{ display: contents; }}",
        f"{s} .link {{ display: inline-flex; align-items: center; min-block-size: 24px; }}",
        f"{s} summary {{ min-block-size: var(--layout-target-min); display: flex; "
        "align-items: center; cursor: pointer; }",
        f"{s} .switcher {{ display: none; }}",
        f"{s} .switch {{ position: absolute; inline-size: 1px; block-size: 1px; overflow: hidden; "
        "clip-path: inset(50%); }",
        f"{s} .switch:checked + label {{ font-weight: 600; text-decoration: underline; }}",
        f"{s} .switch:focus-visible + label {{ outline: var(--border-focus-ring-width) solid "
        "var(--color-focus-ring); outline-offset: var(--border-focus-ring-offset); }",
        f"{s} .switcher label {{ display: inline-flex; align-items: center; min-block-size: "
        "var(--layout-target-min); padding-inline: var(--space-control-padding-inline); }",
        f"{s} .table {{ overflow-x: auto; }} {s} table {{ border-collapse: separate; "
        "border-spacing: 0; inline-size: 100%; }",
        f"{s} .columns {{ display: grid; gap: var(--layout-gutter); grid-template-columns: "
        "repeat(auto-fit, minmax(min(100%, 10rem), 1fr)); }",
        f"{s} .columns ul {{ list-style: none; margin: 0; padding: 0; }}",
        f"{s} .sr-only {{ position: absolute; inline-size: 1px; block-size: 1px; overflow: "
        "hidden; clip-path: inset(50%); white-space: nowrap; }",
        f"@media (min-width: {TABLET_PX}px) {{ {s}[data-alignment=split] .inner, "
        f"{s}[data-alignment=start] .inner.has-media {{ grid-template-columns: 1fr 1fr; "
        "align-items: center; } }",
        f"{s} .sr-only {{ position: absolute; }}",
    ]
    if c.name == "hero":
        for align, place in (("bottom-start", "end start"), ("center", "center")):
            h = f"{s}[data-alignment={align}]"
            out += [
                f"{h} .inner {{ position: relative; min-block-size: 70vh; align-content: end; "
                f"place-items: {place}; }}",
                f"{h} .media-figure {{ position: absolute; inset: 0; margin: 0; }}",
                f"{h} .media-figure .media {{ inline-size: 100%; block-size: 100%; "
                "object-fit: cover; }",
                f"{h} .text {{ position: relative; z-index: 1; display: grid; gap: var(--space-text-gap); "
                "padding: var(--space-card-padding); background-color: var(--imagery-scrim); }",
            ]
        out.append(f"{s}[data-alignment=center] .text {{ text-align: center; "
                   "justify-items: center; }")
    steps = c.section.phone if c.section else ()
    phone: List[str] = []
    if "drop-decorative-layers" in steps:
        phone.append(f"{s} .decor {{ display: none; }}")
    if "fold-side-columns" in steps:
        phone.append(f"{s} .inner {{ grid-template-columns: 1fr; }}")
    if "pair-small-items" in steps:
        phone.append(f"{s} .items, {s} .logos, {s} .stats, {s} .columns {{ "
                     "grid-template-columns: 1fr 1fr; }")
    if "recrop-fragments" in steps:
        phone.append(f"{s} .fragment {{ aspect-ratio: 4 / 3; object-fit: cover; "
                     "object-position: top left; inline-size: 100%; }")
    out.append(f"@media (max-width: {PHONE_PX - 1}px) {{ {' '.join(phone)} }}" if phone else "")
    if "plan-switcher" in steps:
        out.append(f"@media (max-width: {TABLET_PX - 1}px) {{ {s} .switcher {{ display: flex; "
                   f"flex-wrap: wrap; gap: var(--space-control-gap); }} "
                   f"{s} .plans {{ grid-template-columns: 1fr; }} {s} .plan {{ display: none; }} }}")
        for i in range(3):
            out.append(f"@media (max-width: {TABLET_PX - 1}px) {{ {s} .switcher:has(#plan-"
                       f"{c.name}-{i}:checked) + .plans .plan[data-plan=\"{i}\"] {{ "
                       "display: block; } }")
    return "\n".join(x for x in out if x)


def render_section(c: Contract, variant: Optional[Mapping[str, str]] = None,
                   photos: Sequence[Tuple[str, str]] = ()) -> Tuple[str, str]:
    """(markup, css) for one section contract. ``variant`` names a value per
    variant (a left-out variant takes its default); ``photos`` are (src,
    alt) pairs the media slots take in turn."""
    if c.section is None:
        raise ValueError(f"{c.name}: render_section takes a section contract, category "
                         f"section; {c.name} is {c.category}")
    chosen = {v.name: (variant or {}).get(v.name, v.default) for v in c.variants}
    bad = [k for k in (variant or {}) if k not in chosen]
    if bad:
        raise ValueError(f"{c.name}: variant {bad} is not a variant of this section; use "
                         f"{sorted(chosen) or 'none'}")
    needs = any("photograph" in s.takes and s.required for s in c.section.slots)
    if needs and not photos:
        raise ValueError(f"photos: {c.name} needs a photograph; pass (src, alt) pairs sourced "
                         "by the system's photo direction")
    level = "h1" if c.name in HEROES else "h2"
    quiet = c.name in ("footer", "named-quote")  # the quote or the links speak for the band
    heading_cls = "heading sr-only" if quiet else "heading"
    head = (f'<{level} class="{heading_cls}" id="h-{c.name}">{_esc(_title(c.name))}</{level}>')
    body = f'<p class="body">{_esc(c.section.job)}</p>' if not quiet else ""
    names = {s.name for s in c.section.slots}
    cards = any("card" in s.takes for s in c.section.slots)

    def held(slot) -> bool:
        """A slot another one already draws: a card grid carries each item's
        photograph, and each plan carries its own action."""
        if cards and slot.name == "media" and "card" not in slot.takes:
            return True
        if not slot.required and "photograph" in slot.takes:
            return True  # an optional photograph is the page's choice, not the skeleton's
        return "plan" in names and slot.name == "action"
    slots = ["" if held(s) else _slot_html(c, s.name, s.takes, chosen, photos)
             for s in c.section.slots]
    text_side = head + body + "".join(x for s, x in zip(c.section.slots, slots)
                                      if s.name in ("action",))
    rest = "".join(x for s, x in zip(c.section.slots, slots) if s.name not in ("action",))
    media = bool(re.search(r'class="media-figure"', rest))
    attrs = " ".join(f'data-{k}="{_esc(v)}"' for k, v in chosen.items())
    markup = (f'<section class="s-{c.name}" {attrs} aria-labelledby="h-{c.name}">'
              f'<div class="inner{" has-media" if media else ""}"><div class="text">'
              f'{text_side}</div>{rest}</div></section>')
    return markup, _rules(c, chosen) + "\n" + _layout_css(c)
