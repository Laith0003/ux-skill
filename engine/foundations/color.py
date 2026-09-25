"""Color foundation: primitives from OKLCH ramps, semantic roles per
context, the WCAG pairings every system must meet, and a deterministic
retune.

Contexts are scheme x contrast (light, dark; standard, high). Each role
starts where SEMANTIC (standard) or HIGH_CONTRAST puts it for the scheme.
Fill groups (a solid fill, its hover and pressed steps, the text on it)
are solved jointly by _solve_group; the primary group also picks the
focus ring, after its fill, so the ring can prefer a color other than the
fill without ever moving it. Every other role moves one ramp step at a
time away from its background until its pairings hold. Surfaces never
move.

generate_color never gates itself: it returns tokens and notes, and
build_system validates and gates them with PAIRINGS and CHECKS, then asks
seed_hint for advice on the failing pairings the brand seed controls."""
from __future__ import annotations

import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Tuple

from engine.foundations import character
from engine.foundations.color_math import (
    contrast, hex_to_oklch, hex_to_rgb, luminance, oklab_distance, oklch_to_hex, rgb_to_hex)
from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check, GateFinding, Pairing, cite, required
from engine.foundations.modes import compress, contexts, parse
from engine.foundations.ramp import ANCHOR, STEPS, ramp
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.synthesizer.axes import AxisValues

# Every context color tokens are generated for, base first.
COLOR_CONTEXTS = tuple(contexts(("scheme", "contrast")))

# Each status family's own hue; character.status_seed harmonizes it to the
# brand and the warmth axis, never more than character.STATUS_BAND away.
STATUS_HUES = dict(character.STATUS_HUES)
# Translucent overlays: black ("shade") and white ("tint") at these percents.
OVERLAY_STEPS = (10, 20, 40, 60, 80)

_SEMANTIC: Dict[str, Tuple[str, str]] = {
    "color.surface.page": ("color.neutral.50", "color.neutral.950"),
    "color.surface.card": ("color.base.white", "color.neutral.900"),
    # A recess sits half a step below the page, so it reads as a well and
    # not as a disabled slab (light) or a hole (dark).
    "color.surface.sunken": ("color.neutral.recess-light", "color.neutral.recess-dark"),
    "color.surface.raised": ("color.base.white", "color.neutral.800"),
    "color.surface.inverse": ("color.neutral.900", "color.neutral.100"),
    "color.surface.selected": ("color.brand.100", "color.brand.900"),
    "color.text.default": ("color.neutral.900", "color.neutral.50"),
    "color.text.muted": ("color.neutral.600", "color.neutral.400"),
    "color.text.inverse": ("color.neutral.50", "color.neutral.900"),
    "color.text.link": ("color.brand.600", "color.brand.300"),
    "color.text.disabled": ("color.neutral.400", "color.neutral.600"),
    "color.text.on-action": ("color.base.white", "color.base.white"),
    "color.text.on-danger": ("color.base.white", "color.base.white"),
    # The exact brand color is every context's first candidate; the solver
    # moves off it only when neither white nor black text reads on it.
    "color.action.primary": ("color.brand.exact", "color.brand.exact"),
    "color.action.primary-hover": ("color.brand.600", "color.brand.300"),
    "color.action.primary-pressed": ("color.brand.700", "color.brand.200"),
    # The primary button's edge: the fill itself when the fill clears the
    # page, else the nearest step of its ramp that does.
    "color.action.primary-edge": ("color.brand.exact", "color.brand.exact"),
    "color.action.danger": ("color.danger.600", "color.danger.400"),
    "color.action.danger-hover": ("color.danger.700", "color.danger.300"),
    "color.action.danger-pressed": ("color.danger.800", "color.danger.200"),
    # One step off the surfaces a button sits on (card and raised are
    # white in light, neutral.900 and neutral.800 in dark).
    "color.action.disabled": ("color.neutral.200", "color.neutral.700"),
    # A separator sits on card and raised too, so it starts one step off
    # both (neutral.900 and neutral.800 in dark).
    "color.line.subtle": ("color.neutral.200", "color.neutral.700"),
    # A field border sits on every surface a control does. In dark, raised
    # is neutral.800, where neutral.500 falls under 3:1 for every seed, so
    # dark starts one step lighter.
    "color.line.input": ("color.neutral.500", "color.neutral.400"),
    "color.line.selected": ("color.brand.600", "color.brand.300"),
    # The error edge of a field: the danger hue at a non-text minimum, with
    # no text on it, so high contrast never pushes it toward black.
    "color.line.danger": ("color.danger.600", "color.danger.400"),
    "color.focus.ring": ("color.brand.700", "color.brand.200"),
    "color.focus.ring-inverse": ("color.brand.300", "color.brand.700"),
    "color.scrim": ("color.shade.40", "color.shade.60"),
    # Brand roles by character: an accent for words, an edge for rules and
    # underlines, a supporting accent from a second hue.
    "color.text.accent": ("color.brand.700", "color.brand.300"),
    "color.line.accent": ("color.brand.600", "color.brand.300"),
    "color.text.support": ("color.support.700", "color.support.300"),
    # Brand-tinted surfaces: a quiet tint, a section band, and the exact
    # brand as a band with its own text.
    "color.surface.tint": ("color.brand.50", "color.brand.950"),
    "color.surface.band": ("color.brand.100", "color.brand.900"),
    "color.surface.brand": ("color.brand.exact", "color.brand.exact"),
    "color.text.on-brand": ("color.base.white", "color.base.white"),
    # Table stripes and the code surface with its syntax colors.
    "color.surface.stripe": ("color.neutral.50", "color.neutral.950"),
    "color.surface.code": ("color.neutral.100", "color.neutral.recess-dark"),
    "color.syntax.plain": ("color.neutral.900", "color.neutral.50"),
    "color.syntax.keyword": ("color.brand.700", "color.brand.300"),
    "color.syntax.string": ("color.success.700", "color.success.300"),
    "color.syntax.number": ("color.warning.700", "color.warning.300"),
    "color.syntax.function": ("color.info.700", "color.info.300"),
    "color.syntax.comment": ("color.neutral.600", "color.neutral.400"),
    # Decoration and illustration: shapes with no meaning, and lines that
    # carry meaning in a drawing.
    "color.decorative.brand": ("color.brand.300", "color.brand.600"),
    "color.decorative.support": ("color.support.300", "color.support.600"),
    "color.decorative.neutral": ("color.neutral.300", "color.neutral.600"),
    "color.illustration.line": ("color.brand.600", "color.brand.400"),
    # The logo keeps the exact brand color wherever it clears our floor.
    "color.logo": ("color.brand.exact", "color.brand.exact"),
}
for _s in STATUS_HUES:
    _SEMANTIC[f"color.status.{_s}.text"] = (f"color.{_s}.700", f"color.{_s}.300")
    _SEMANTIC[f"color.status.{_s}.soft"] = (f"color.{_s}.100", f"color.{_s}.900")
    _SEMANTIC[f"color.status.{_s}.strong"] = (f"color.{_s}.600", f"color.{_s}.400")
    _SEMANTIC[f"color.status.{_s}.on-strong"] = ("color.base.white", "color.base.black")


def _grouped(table: Dict[str, Tuple[str, str]]) -> Dict[str, Tuple[str, str]]:
    """The table in the order a DTCG document nests it: each group's
    members together, groups in the order they first appear. A role added
    at the end of its table still sits beside its siblings, so tokens.json
    reads back in the order it was written."""
    tree: Dict[str, object] = {}
    for path in table:
        node = tree
        for part in path.split("."):
            node = node.setdefault(part, {})  # type: ignore[assignment]
    out: List[str] = []

    def walk(node: Dict[str, object], prefix: str) -> None:
        for key, child in node.items():
            path = f"{prefix}.{key}" if prefix else key
            if path in table:
                out.append(path)
            walk(child, path)  # type: ignore[arg-type]

    walk(tree, "")
    return {path: table[path] for path in out}


# Read-only view: role -> (light primitive, dark primitive).
SEMANTIC: Mapping[str, Tuple[str, str]] = MappingProxyType(_grouped(_SEMANTIC))

# Starting points in contrast:high contexts, per scheme: extreme surfaces,
# text a step or two further out. The retune and the group solver then
# move roles until the raised minimums hold. Roles not listed start where
# the standard table puts them.
_HIGH: Dict[str, Tuple[str, str]] = {
    "color.surface.page": ("color.base.white", "color.base.black"),
    "color.surface.card": ("color.base.white", "color.neutral.900"),
    "color.surface.sunken": ("color.neutral.recess-light", "color.base.black"),
    "color.surface.raised": ("color.base.white", "color.neutral.800"),
    "color.surface.inverse": ("color.base.black", "color.base.white"),
    "color.surface.selected": ("color.brand.50", "color.brand.950"),
    "color.text.default": ("color.neutral.950", "color.base.white"),
    "color.text.muted": ("color.neutral.800", "color.neutral.200"),
    "color.text.inverse": ("color.base.white", "color.base.black"),
    "color.text.link": ("color.brand.800", "color.brand.200"),
    "color.action.primary": ("color.brand.exact", "color.brand.exact"),
    "color.action.primary-hover": ("color.brand.900", "color.brand.100"),
    "color.action.primary-pressed": ("color.brand.950", "color.brand.50"),
    "color.action.primary-edge": ("color.brand.exact", "color.brand.exact"),
    "color.action.danger": ("color.danger.800", "color.danger.200"),
    "color.action.danger-hover": ("color.danger.900", "color.danger.100"),
    "color.action.danger-pressed": ("color.danger.950", "color.danger.50"),
    "color.line.subtle": ("color.neutral.400", "color.neutral.600"),
    "color.line.input": ("color.neutral.700", "color.neutral.300"),
    "color.line.selected": ("color.brand.800", "color.brand.200"),
    "color.line.danger": ("color.danger.700", "color.danger.300"),
    # One step further out than the standard ring, so high contrast starts
    # no weaker than standard.
    "color.focus.ring": ("color.brand.800", "color.brand.100"),
    "color.focus.ring-inverse": ("color.brand.200", "color.brand.800"),
    "color.scrim": ("color.shade.60", "color.shade.80"),
    "color.text.accent": ("color.brand.800", "color.brand.200"),
    "color.line.accent": ("color.brand.800", "color.brand.200"),
    "color.text.support": ("color.support.800", "color.support.200"),
    "color.surface.stripe": ("color.neutral.100", "color.neutral.800"),
    "color.surface.code": ("color.neutral.100", "color.base.black"),
    "color.syntax.plain": ("color.neutral.950", "color.base.white"),
    "color.syntax.keyword": ("color.brand.800", "color.brand.200"),
    "color.syntax.string": ("color.success.800", "color.success.200"),
    "color.syntax.number": ("color.warning.800", "color.warning.200"),
    "color.syntax.function": ("color.info.800", "color.info.200"),
    "color.syntax.comment": ("color.neutral.700", "color.neutral.300"),
    "color.illustration.line": ("color.brand.800", "color.brand.200"),
}
for _s in STATUS_HUES:
    _HIGH[f"color.status.{_s}.text"] = (f"color.{_s}.800", f"color.{_s}.200")
    _HIGH[f"color.status.{_s}.soft"] = (f"color.{_s}.50", f"color.{_s}.950")
    _HIGH[f"color.status.{_s}.strong"] = (f"color.{_s}.800", f"color.{_s}.200")
HIGH_CONTRAST: Mapping[str, Tuple[str, str]] = MappingProxyType(_HIGH)

# The brand's role (character.brand_role): with "fill" the brand fills the
# main action; with "accent" or "edge" the main action is ink, a neutral
# at the far end of the ramp, and the brand marks words (accent) or edges,
# underlines and rules (edge; links are ink with a brand underline). These
# replace the standard and high contrast starting points of the roles
# they name.
INK: Mapping[str, Tuple[str, str]] = MappingProxyType({
    "color.action.primary": ("color.neutral.900", "color.neutral.100"),
    "color.action.primary-hover": ("color.neutral.800", "color.neutral.200"),
    "color.action.primary-pressed": ("color.neutral.700", "color.neutral.300"),
    "color.action.primary-edge": ("color.neutral.900", "color.neutral.100"),
})
INK_HIGH: Mapping[str, Tuple[str, str]] = MappingProxyType({
    "color.action.primary": ("color.neutral.950", "color.neutral.50"),
    "color.action.primary-hover": ("color.neutral.900", "color.neutral.100"),
    "color.action.primary-pressed": ("color.neutral.800", "color.neutral.200"),
    "color.action.primary-edge": ("color.neutral.950", "color.neutral.50"),
})
EDGE_LINK: Mapping[str, Tuple[str, str]] = MappingProxyType({
    "color.text.link": ("color.neutral.800", "color.neutral.200")})
EDGE_LINK_HIGH: Mapping[str, Tuple[str, str]] = MappingProxyType({
    "color.text.link": ("color.neutral.950", "color.base.white")})
BRAND_ROLES: Tuple[str, ...] = ("fill", "accent", "edge")

# Coverage by construction. Every role read as text pairs with every surface
# text can sit on, at the text minimum (WCAG 1.4.3 4.5:1; 1.4.6 7:1 in high
# contrast). Every line or ring that identifies a control or its state pairs
# with every surface a control sits on, at the non-text minimum (WCAG 1.4.11
# 3:1; our 4.5:1 floor in high contrast). A role or surface added to a table
# gets every pairing it needs; build_pairings writes them.
TEXT_ROLES: Tuple[str, ...] = ("color.text.default", "color.text.muted", "color.text.link") \
    + tuple(f"color.status.{s}.text" for s in STATUS_HUES) \
    + ("color.text.accent", "color.text.support")
TEXT_SURFACES: Tuple[str, ...] = ("color.surface.page", "color.surface.card",
                                  "color.surface.sunken", "color.surface.raised",
                                  "color.surface.selected", "color.surface.tint",
                                  "color.surface.band", "color.surface.stripe")
LINE_ROLES: Tuple[str, ...] = ("color.line.input", "color.line.selected", "color.line.danger",
                                "color.line.accent", "color.focus.ring")
# Syntax colors sit on the code surface only; plain is the text between them.
SYNTAX_ROLES: Tuple[str, ...] = ("color.syntax.plain", "color.syntax.keyword",
                                 "color.syntax.string", "color.syntax.number",
                                 "color.syntax.function", "color.syntax.comment")
DECORATIVE_ROLES: Tuple[str, ...] = ("color.decorative.brand", "color.decorative.support",
                                     "color.decorative.neutral")
# Our floor for a decorative shape against the page and card: visible, but
# no contrast minimum applies to decoration.
DECORATIVE_FLOOR = 1.5
# Our floor for the logo against the page; WCAG exempts logotypes.
LOGO_FLOOR = 3.0
# Controls sit on the brand-tinted surfaces too: a ghost button in a striped
# table row, a field in a tinted panel, a link in a band. The brand band is
# not here: a control on it takes color.text.on-brand for its ring and
# edges, held to the text minimum against the band.
LINE_SURFACES: Tuple[str, ...] = ("color.surface.page", "color.surface.card",
                                  "color.surface.sunken", "color.surface.raised",
                                  "color.surface.tint", "color.surface.band",
                                  "color.surface.stripe")
# Roles in the four families the tables cover (text, surface, line,
# focus) that sit in no table, each with the reason it needs no row there.
# A role added to one of those families must join a table or this map, or
# uncovered_roles names it: a role in neither would get no pairing at all.
COVERAGE_EXEMPT: Mapping[str, str] = MappingProxyType({
    "color.text.inverse": "sits only on color.surface.inverse and is paired there",
    "color.text.disabled": "inactive text, which WCAG exempts from contrast minimums; "
                           "disabled-distinct keeps it apart from enabled text",
    "color.text.on-action": "sits only on the primary fill and its states and is paired there",
    "color.text.on-danger": "sits only on the danger fill and its states and is paired there",
    "color.surface.inverse": "a background whose text and ring are paired against it",
    "color.line.subtle": "a decorative separator with no contrast minimum; "
                         "line-subtle-visible keeps it apart from the surfaces it divides",
    "color.focus.ring-inverse": "the ring for color.surface.inverse and is paired there",
    "color.surface.brand": "a band whose only text is color.text.on-brand, paired there",
    "color.text.on-brand": "sits only on color.surface.brand and is paired there",
    "color.surface.code": "a background whose syntax colors are paired against it",
})
COVERAGE_FAMILIES: Tuple[str, ...] = ("color.text.", "color.surface.", "color.line.",
                                      "color.focus.")


def uncovered_roles(roles: Iterable[str]) -> List[str]:
    """Every role in a covered family that no coverage table names and
    COVERAGE_EXEMPT does not excuse, in the order given."""
    tables = set(TEXT_ROLES + TEXT_SURFACES + LINE_ROLES + LINE_SURFACES)
    return [r for r in roles if r.startswith(COVERAGE_FAMILIES)
            and r not in tables and r not in COVERAGE_EXEMPT]

_FILL_STATES = {
    "color.action.primary": ("color.action.primary-hover", "color.action.primary-pressed"),
    "color.action.danger": ("color.action.danger-hover", "color.action.danger-pressed"),
}


def _extra_text_bgs(role: str) -> Tuple[str, ...]:
    """Fills a text role also sits on, beyond the surfaces: body and muted
    copy on every status soft fill (alert and banner copy), status text on
    its own soft fill."""
    if role in ("color.text.default", "color.text.muted"):
        return tuple(f"color.status.{s}.soft" for s in STATUS_HUES)
    if role.startswith("color.status.") and role.endswith(".text"):
        return (role[:-len("text")] + "soft",)
    return ()


def build_pairings(text_roles: Tuple[str, ...] = TEXT_ROLES,
                   text_surfaces: Tuple[str, ...] = TEXT_SURFACES,
                   line_roles: Tuple[str, ...] = LINE_ROLES,
                   line_surfaces: Tuple[str, ...] = LINE_SURFACES) -> Tuple[Pairing, ...]:
    """Every color pairing: the two coverage tables crossed, plus the
    pairings that belong to one fill or one surface."""
    return tuple(
        [Pairing(role, bg, 4.5, "1.4.3")
         for role in text_roles for bg in text_surfaces + _extra_text_bgs(role)]
        + [Pairing("color.text.inverse", "color.surface.inverse", 4.5, "1.4.3")]
        + [Pairing(on, state, 4.5, "1.4.3")
           for fill, on in (("color.action.primary", "color.text.on-action"),
                            ("color.action.danger", "color.text.on-danger"))
           for state in (fill,) + _FILL_STATES[fill]]
        + [Pairing(f"color.status.{s}.on-strong", f"color.status.{s}.strong", 4.5, "1.4.3")
           for s in STATUS_HUES]
        # A focus indicator is a non-text part: 1.4.11 sets its 3:1 against
        # the colors next to it (2.4.7 asks only that focus be visible). The
        # border foundation guarantees border.focus-ring.offset of at least
        # 1px, so the colors next to the ring are the surfaces, never the
        # fill it surrounds; the ring is not paired with the button fill.
        + [Pairing(role, bg, 3.0, "1.4.11") for role in line_roles for bg in line_surfaces]
        # The primary fill keeps the brand color; its edge carries the 3:1
        # against the page. The danger fill carries it itself.
        + [Pairing("color.action.primary-edge", "color.surface.page", 3.0, "1.4.11")]
        + [Pairing(state, "color.surface.page", 3.0, "1.4.11")
           for state in ("color.action.danger",) + _FILL_STATES["color.action.danger"]]
        + [Pairing(f"color.status.{s}.strong", "color.surface.page", 3.0, "1.4.11")
           for s in STATUS_HUES]
        # One ring cannot also stand out from the inverse surface, so that
        # surface gets its own.
        + [Pairing("color.focus.ring-inverse", "color.surface.inverse", 3.0, "1.4.11")]
        + [Pairing("color.text.on-brand", "color.surface.brand", 4.5, "1.4.3")]
        + [Pairing(role, "color.surface.code", 4.5, "1.4.3") for role in SYNTAX_ROLES]
        + [Pairing("color.illustration.line", bg, 3.0, "1.4.11")
           for bg in ("color.surface.page", "color.surface.card", "color.surface.raised")]
        + [Pairing(role, bg, DECORATIVE_FLOOR, "system", high=DECORATIVE_FLOOR)
           for role in DECORATIVE_ROLES for bg in ("color.surface.page", "color.surface.card")]
        + [Pairing("color.logo", "color.surface.page", LOGO_FLOOR, "system", high=LOGO_FLOOR)]
    )


PAIRINGS: Tuple[Pairing, ...] = build_pairings()


def _paired_with(fg: str) -> Tuple[str, ...]:
    """Every background PAIRINGS pairs `fg` with, in declaration order."""
    return tuple(p.bg for p in PAIRINGS if p.fg == fg)


@dataclass(frozen=True)
class _Group:
    """Roles solved together: a fill, its interaction states, the text on
    it, and optionally the focus ring, picked after the fill so it can
    prefer a color other than the fill."""
    fill: str
    on: str
    states: Tuple[str, ...] = ()
    ring: str = ""
    # Whether the fill (or its edge) must clear the page: a control must, a
    # band of brand color behind a section need not.
    page: bool = True
    # The role that carries the fill's contrast against the page, drawn as
    # an edge around it; "" when the fill and its states carry it.
    edge: str = ""
    # Whether the group keeps the exact brand color when a text color reads
    # on it (brand fidelity).
    brand: bool = False


GROUPS: Tuple[_Group, ...] = (
    _Group("color.action.primary", "color.text.on-action",
           _FILL_STATES["color.action.primary"], "color.focus.ring",
           edge="color.action.primary-edge", brand=True),
    _Group("color.action.danger", "color.text.on-danger", _FILL_STATES["color.action.danger"]),
) + tuple(_Group(f"color.status.{s}.strong", f"color.status.{s}.on-strong") for s in STATUS_HUES) \
    + (_Group("color.surface.brand", "color.text.on-brand", page=False, brand=True),)
_GROUP_ROLES = frozenset(r for g in GROUPS for r in (g.fill, g.on, g.ring, g.edge) + g.states
                         if r)
EXACT = "color.brand.exact"
# In dark and high contrast, black text goes only on a fill at least this
# light (OKLCH): black on a mid tone reads muddy.
MUDDY_L = 0.72
# The ring prefers a color that also stands 3:1 off the primary fill.
RING_ON_FILL = 3.0
# The least OKLab distance a hover or pressed step keeps from its fill: a
# just visible step.
JUST_VISIBLE = 0.02
# A brand fill further than this from the brand color (OKLab distance)
# reads as another color; the report says so.
IDENTITY_DISTANCE = 0.12

# M1 name for the generator's result; every foundation now returns Generated.
ColorResult = Generated


def _scheme(mode: str) -> str:
    return parse(mode).get("scheme", "light")


def _default(role: str, mode: str, brand_role: str = "fill") -> str:
    """Where a role starts in one context, before any retune."""
    high = parse(mode).get("contrast") == "high"
    tables = []
    if brand_role != "fill":
        tables += [INK_HIGH, INK] if high else [INK]
    if brand_role == "edge":
        tables += [EDGE_LINK_HIGH, EDGE_LINK] if high else [EDGE_LINK]
    tables += [HIGH_CONTRAST, SEMANTIC] if high else [SEMANTIC]
    table = next(t for t in tables if role in t)
    return table[role][0 if _scheme(mode) == "light" else 1]


def _need(fg: str, bg: str, mode: str) -> float:
    """The minimum PAIRINGS asks of fg on bg in this context."""
    return next(required(p, mode)[0] for p in PAIRINGS if (p.fg, p.bg) == (fg, bg))


def _neutral_seed(brand_hex: str, axes: AxisValues) -> str:
    """The neutral ramp's seed: the brand hue at warmth 0.5 (weighted by
    the brand's chroma), moving to a warm or a cool hue, with more chroma,
    toward either end."""
    _, brand_chroma, brand_hue = hex_to_oklch(brand_hex)
    hue, chroma = character.neutral_tint(axes, brand_hue, brand_chroma)
    return oklch_to_hex(0.55, chroma, hue)


# How far a recess sits below the page, in OKLCH lightness.
RECESS_L = 0.035


def _shift(hx: str, delta: float) -> str:
    """The same hue and chroma at a lightness `delta` away."""
    L, C, H = hex_to_oklch(hx)
    return oklch_to_hex(L + delta, C, H)


def _primitives(axes: AxisValues, brand_hex: str, notes: List[str]) -> Dict[str, str]:
    prims = {"color.base.white": "#FFFFFF", "color.base.black": "#000000"}
    seeds = {"brand": brand_hex, "neutral": _neutral_seed(brand_hex, axes)}
    _, brand_chroma, brand_hue = hex_to_oklch(brand_hex)
    seeds["support"] = oklch_to_hex(0.6, min(0.16, max(0.06, 0.9 * brand_chroma)),
                                    character.support_hue(axes, brand_hue))
    seeds.update({s: oklch_to_hex(*character.status_seed(s, axes, brand_hue, brand_chroma))
                  for s in STATUS_HUES})
    for family, seed in seeds.items():
        r = ramp(seed)
        if r.retuned:
            notes.append(f"color.{family}: {r.note}")
        for step, hx in r.stops.items():
            prims[f"color.{family}.{step}"] = hx
        if family == "brand":
            # The brand color exactly as given, beside its ramp (a DTCG round
            # trip keeps the order).
            prims[EXACT] = rgb_to_hex(hex_to_rgb(brand_hex))
        if family == "neutral":
            # Kept beside the ramp, so a DTCG round trip keeps the order.
            prims["color.neutral.recess-light"] = _shift(r.stops[50], -RECESS_L)
            prims["color.neutral.recess-dark"] = _shift(r.stops[950], -RECESS_L)
    for family, rgb in (("shade", "#000000"), ("tint", "#FFFFFF")):
        for pct in OVERLAY_STEPS:
            prims[f"color.{family}.{pct}"] = rgb + f"{round(pct * 255 / 100):02X}"
    return prims


def _step_path(path: str, delta: int) -> str:
    family, step = path.rsplit(".", 1)
    if path == EXACT:
        step = str(ANCHOR)  # the exact brand steps as its ramp's anchor does
    if not step.isdigit():
        return ""
    i = STEPS.index(int(step)) + delta
    return f"{family}.{STEPS[i]}" if 0 <= i < len(STEPS) else ""


def _order_from(idx: int, conv: int) -> List[int]:
    """Ramp indices from idx outward: idx, then one step in the
    conventional direction, one step against it, two steps, and so on."""
    out = [idx]
    for d in range(1, len(STEPS)):
        for delta in (conv * d, -conv * d):
            if 0 <= idx + delta < len(STEPS) and idx + delta not in out:
                out.append(idx + delta)
    return out


def _ring_candidates(mode: str, default_ring: str) -> List[str]:
    """Where the focus ring may land, in preference order: brand steps
    nearest its default, then neutral steps from the extreme that contrasts
    with the surfaces, then black and white."""
    conv = +1 if _scheme(mode) == "light" else -1
    family, step = default_ring.rsplit(".", 1)
    brand = [f"{family}.{STEPS[i]}" for i in _order_from(STEPS.index(int(step)), conv)]
    light = _scheme(mode) == "light"
    neutral_steps = list(reversed(STEPS)) if light else list(STEPS)
    base = ["color.base.black", "color.base.white"]
    return brand + [f"color.neutral.{s}" for s in neutral_steps] + (
        base if light else list(reversed(base)))


def _side(fill_hex: str, family: str, d: int, prims: Dict[str, str]) -> List[str]:
    """The steps of a ramp on one side of a fill, darker than it for d = +1
    and lighter for d = -1, nearest in lightness first, keeping a step only
    when it sits at least JUST_VISIBLE from the step before it (the fill
    first) and further from the fill than that step does. Walking from the
    fill's own lightness, not from a step number, lets the exact brand step
    from wherever it sits in its ramp, and each state kept this way moves
    visibly further from the fill than the one before it."""
    fill_l = hex_to_oklch(fill_hex)[0]
    steps = []
    for i, step in enumerate(STEPS):
        path = f"{family}.{step}"
        step_l = hex_to_oklch(prims[path])[0]
        if (step_l < fill_l) if d > 0 else (step_l > fill_l):
            steps.append((round(abs(step_l - fill_l), 6), i if d > 0 else -i, path))
    out: List[str] = []
    prev, prev_d = fill_hex, 0.0
    for _, _, path in sorted(steps):
        dist = oklab_distance(prims[path], fill_hex)
        if dist > prev_d and oklab_distance(prims[path], prev) >= JUST_VISIBLE:
            out.append(path)
            prev, prev_d = prims[path], dist
    return out


def _state_paths(fill_hex: str, family: str, conv: int, n: int,
                 prims: Dict[str, str]) -> List[Tuple[str, ...]]:
    """Ramp steps for n interaction states, in preference order: each state
    one visible step further from the fill in the conventional direction,
    then against it, then with a gap of two, so every state moves away from
    the fill and each further than the one before."""
    if n == 0:
        return [()]
    out: List[Tuple[str, ...]] = []
    for gap, d in ((1, conv), (1, -conv), (2, conv), (2, -conv)):
        side = _side(fill_hex, family, d, prims)
        if len(side) >= gap * n:
            out.append(tuple(side[gap * (k + 1) - 1] for k in range(n)))
    return out


def _choose_ring(rings: List[str], fit: Callable[[str], float], fill_hex: str,
                 prims: Dict[str, str], tints: Tuple[str, ...] = ()) -> str:
    """The ring for a fill already chosen: the first candidate that clears
    every surface and stands RING_ON_FILL off the fill and off each tinted
    fill the contracts pair it with (`tints`: the selected surface and the
    status soft fills), else the first that clears every surface and
    differs from the fill, else the first that clears every surface (it
    equals the fill, which the offset makes visible), else the closest.
    Only the ring moves here, never the fill."""
    clear = [r for r in rings if fit(r) >= 1.0]
    if clear:
        return next((r for r in clear
                     if all(contrast(prims[r], hx) >= RING_ON_FILL for hx in (fill_hex,) + tints)),
                    next((r for r in clear if prims[r] != fill_hex), clear[0]))
    return max(rings, key=fit)


def _fill_candidates(g: _Group, default: str, conv: int,
                     prims: Dict[str, str]) -> List[str]:
    """Fill paths in preference order. A brand group whose default is the
    exact brand color tries it first, then every brand step by OKLab
    distance from it, so a move keeps as much of the brand as the text
    allows. Any other group walks its ramp outward from the default, the
    conventional direction first."""
    family, step = default.rsplit(".", 1)
    if g.brand and default == EXACT:
        order = _order_from(STEPS.index(ANCHOR), conv)
        steps = sorted(range(len(STEPS)), key=lambda i: (
            round(oklab_distance(prims[f"{family}.{STEPS[i]}"], prims[EXACT]), 6),
            order.index(i)))
        return [EXACT] + [f"{family}.{STEPS[i]}" for i in steps]
    return [f"{family}.{STEPS[i]}" for i in _order_from(STEPS.index(int(step)), conv)]


def _muddy(fill_hex: str, on: str, mode: str) -> bool:
    """Black text on a mid tone, in a context where that reads muddy (dark
    or high contrast)."""
    strict = _scheme(mode) == "dark" or parse(mode).get("contrast") == "high"
    return strict and on == "color.base.black" and hex_to_oklch(fill_hex)[0] < MUDDY_L


def _choose_edge(fill_path: str, family: str, page_hex: str, need: float,
                 prims: Dict[str, str]) -> str:
    """The fill itself when it clears the page, else the step of its ramp
    nearest the fill that does, else the one that comes closest."""
    if contrast(prims[fill_path], page_hex) >= need:
        return fill_path
    steps = sorted((f"{family}.{s}" for s in STEPS),
                   key=lambda p: (round(oklab_distance(prims[p], prims[fill_path]), 6), p))
    return next((p for p in steps if contrast(prims[p], page_hex) >= need),
                max(steps, key=lambda p: contrast(prims[p], page_hex)))


def _solve_group(g: _Group, mode: str, prims: Dict[str, str],
                 pick: Dict[str, Dict[str, str]], notes: List[str],
                 ring_floor: float = 0.0) -> None:
    """Choose one fill group for one context.

    Search order (deterministic):
      1. the fill: for the brand group the exact brand color, then brand
         steps by OKLab distance from it; for any other group the ramp
         outward from its default, the conventional direction (darker in
         light, lighter in dark) first at equal distance;
      2. its states (hover, then pressed) one and two steps on from the
         fill's own lightness in the conventional direction, then against
         it, then with gaps of two, each at least JUST_VISIBLE from the
         fill (_state_paths), so the exact brand steps from where it sits
         in its ramp, not from step 500;
      3. the text on it as base.white, then base.black; in dark and high
         contrast the brand group first skips black text on a fill darker
         than MUDDY_L, and takes it only when nothing else clears;
      4. for a group with an edge, the edge: the fill when it clears the
         page, else the nearest step of its ramp that does;
      5. for the primary group, the ring, after the rest is fixed: brand
         steps nearest its default, then neutral steps, then black and
         white (_ring_candidates), preferring a ring that stands 3:1 off
         the fill, then one whose color differs from it. The fill never
         moves for the ring.
    The minimums are PAIRINGS' own in this context, so they rise under
    contrast:high:
      text on the fill and on every state   >= 4.5 (WCAG 1.4.3), 7.0 high (WCAG 1.4.6)
      the fill and every state on the page  >= 3.0 (WCAG 1.4.11), 4.5 high (our floor),
                                               or the edge on the page when the group has one
      every state's hex differs from the fill's and from each other's
      ring on every surface PAIRINGS names  >= 3.0 (WCAG 1.4.11), 4.5 high (our floor),
                                               and under high contrast its lowest ratio never
                                               below the standard ring's lowest (ring_floor)
    When nothing clears, the closest candidate is kept and noted; the gate
    then reports the failing pairings. The generator never raises here.
    """
    roles = (g.fill,) + g.states + (g.on,) + ((g.edge,) if g.edge else ()) \
        + ((g.ring,) if g.ring else ())
    defaults = {r: pick[mode][r] for r in roles}
    page_hex = prims[pick[mode]["color.surface.page"]]
    family = defaults[g.fill].rsplit(".", 1)[0]
    conv = +1 if _scheme(mode) == "light" else -1
    need_text = _need(g.on, g.fill, mode)
    need_fill = 0.0 if g.edge or not g.page else _need(g.fill, "color.surface.page", mode)
    rings = _ring_candidates(mode, defaults[g.ring]) if g.ring else []
    ring_bgs = [(prims[pick[mode][bg]], _need(g.ring, bg, mode))
                for bg in _paired_with(g.ring)] if g.ring else []

    tints = tuple(prims[pick[mode][r]] for r in ("color.surface.selected",)
                  + tuple(f"color.status.{s}.soft" for s in STATUS_HUES)) if g.ring else ()

    def ring_low(ring: str) -> float:
        return min(contrast(prims[ring], hx) for hx, _ in ring_bgs)

    def ring_fit(ring: str) -> float:
        fit = min(contrast(prims[ring], hx) / need for hx, need in ring_bgs)
        return min(fit, ring_low(ring) / ring_floor) if ring_floor else fit

    def finish(choice: Tuple[str, ...], hexes: List[str], on: str, solved: bool) -> None:
        summary = f"text/fill {contrast(prims[on], hexes[0]):.2f}:1"
        if g.edge:
            need_edge = _need(g.edge, "color.surface.page", mode)
            edge = _choose_edge(choice[0], family, page_hex, need_edge, prims)
            choice += (edge,)
            solved = solved and contrast(prims[edge], page_hex) >= need_edge
            summary += f", edge/page {contrast(prims[edge], page_hex):.2f}:1"
        else:
            summary += f", fill/page {contrast(hexes[0], page_hex):.2f}:1"
        if g.ring:
            ring = _choose_ring(rings, ring_fit, hexes[0], prims, tints)
            choice += (ring,)
            solved = solved and ring_fit(ring) >= 1.0
            summary += f", ring/surface {ring_low(ring):.2f}:1"
        _apply(g, mode, pick, defaults, roles, choice, summary, notes, solved=solved)

    best: Optional[Tuple[float, Tuple[str, ...], List[str], str]] = None
    candidates = _fill_candidates(g, defaults[g.fill], conv, prims)
    for allow_muddy in ((False, True) if g.brand else (True,)):
        for fill_path in candidates:
            for states in _state_paths(prims[fill_path], family, conv, len(g.states), prims):
                paths = [fill_path] + list(states)
                hexes = [prims[p] for p in paths]
                if len(set(hexes)) != len(hexes):
                    continue
                for on in ("color.base.white", "color.base.black"):
                    if not allow_muddy and _muddy(hexes[0], on, mode):
                        continue
                    score = min([contrast(prims[on], h) / need_text for h in hexes]
                                + [contrast(h, page_hex) / need_fill for h in hexes
                                   if need_fill])
                    choice = tuple(paths) + (on,)
                    if best is None or score > best[0]:
                        best = (score, choice, hexes, on)
                    if score >= 1.0:
                        finish(choice, hexes, on, solved=True)
                        return
    if best is None:
        notes.append(f"{g.fill} group ({mode}): every step of the {family.split('.')[-1]} ramp "
                     "resolves to the same color, so the states cannot differ from the fill; "
                     "kept the defaults")
        return
    finish(best[1], best[2], best[3], solved=False)


def _apply(g: _Group, mode: str, pick: Dict[str, Dict[str, str]], defaults: Dict[str, str],
           roles: Tuple[str, ...], choice: Tuple[str, ...], summary: str, notes: List[str],
           solved: bool) -> None:
    for role, path in zip(roles, choice):
        pick[mode][role] = path
    moves = ", ".join(f"{role} {defaults[role]} -> {path}"
                      for role, path in zip(roles, choice) if defaults[role] != path)
    if not solved:
        notes.append(f"{g.fill} group ({mode}): no combination within the ramps clears every "
                     f"requirement; kept the closest{': ' + moves if moves else ''}, {summary}")
    elif moves:
        notes.append(f"{g.fill} group ({mode}): {moves}, {summary}")


def seed_hint(ts: TokenSet, finding: GateFinding) -> str:
    """Advice for a failing pairing the brand seed controls: one side
    aliases a brand step in that context. The direction comes from the
    other side: when it is lighter than the brand color, a darker seed
    gains contrast, otherwise a lighter one does. Pairings the seed does
    not control get no advice ("") and keep the gate's own fix."""
    for side, other in ((finding.fg, finding.bg), (finding.bg, finding.fg)):
        raw = ts.raw(side, finding.mode)
        if is_alias(raw) and alias_target(raw).startswith("color.brand."):
            brand_lum = luminance(ts.resolve(side, finding.mode))
            other_lum = luminance(ts.resolve(other, finding.mode))
            direction = "a darker" if other_lum > brand_lum else "a lighter"
            return ("The brand seed cannot reach it within its ramp; "
                    f"choose {direction} or more saturated seed.")
    return ""


# Every semantic role is a color. The build's role-types check reports any
# other type once, and the checks below skip it.
ROLE_TYPES: Mapping[str, str] = MappingProxyType({role: "color" for role in SEMANTIC})


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _states_distinct(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for fill, states in _FILL_STATES.items():
        chain = (fill,) + states
        if not all(_typed(ts, r) for r in chain):
            continue
        hexes = [ts.resolve(r, mode) for r in chain]
        for i, role in enumerate(chain[1:], 1):
            if hexes[i] in hexes[:i]:
                other = chain[hexes.index(hexes[i])]
                out.append(f"{role} equals {other} ({mode}) at {hexes[i]}; point {role} at a "
                           "neighboring step so each state reads as a different color")
    return out


def _disabled_visible(ts: TokenSet, mode: str) -> List[str]:
    """A disabled button must not vanish into the surface it sits on.
    Inactive controls are exempt from the WCAG contrast minimums, so this
    asks only that the colors differ."""
    disabled = "color.action.disabled"
    if not _typed(ts, disabled):
        return []
    hx = ts.resolve(disabled, mode)
    return [f"{disabled} equals {bg} ({mode}) at {hx}, so a disabled button vanishes on that "
            "surface. WCAG exempts inactive controls from contrast minimums, so this is a "
            f"distinctness rule, not a ratio: point {disabled} at a step that differs from "
            "color.surface.card and color.surface.raised"
            for bg in ("color.surface.card", "color.surface.raised")
            if _typed(ts, bg) and ts.resolve(bg, mode) == hx]


def _line_subtle_visible(ts: TokenSet, mode: str) -> List[str]:
    """A separator must not vanish into the surface it divides. It is
    decorative, so no contrast ratio applies; this asks only that the
    colors differ."""
    subtle = "color.line.subtle"
    if not _typed(ts, subtle):
        return []
    hx = ts.resolve(subtle, mode)
    return [f"{subtle} equals {bg} ({mode}) at {hx}, so a separator vanishes on that surface. "
            "A decorative line needs no contrast ratio, but it must differ from the surface it "
            f"divides: point {subtle} at a step that differs from color.surface.card and "
            "color.surface.raised"
            for bg in ("color.surface.card", "color.surface.raised")
            if _typed(ts, bg) and ts.resolve(bg, mode) == hx]


def _disabled_distinct(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for disabled, enabled in (("color.text.disabled", ("color.text.default", "color.text.muted")),
                              ("color.action.disabled", ("color.action.primary",))):
        if not _typed(ts, disabled):
            continue
        hx = ts.resolve(disabled, mode)
        for role in enabled:
            if _typed(ts, role) and ts.resolve(role, mode) == hx:
                out.append(f"{disabled} equals {role} ({mode}) at {hx}; point {disabled} at a "
                           "step that reads as inactive next to it")
    return out


def _scheme_polarity(ts: TokenSet, mode: str) -> List[str]:
    """A light scheme has a page lighter than its text, a dark scheme the
    reverse; a set that says dark but ships a light palette is caught here."""
    page, text = "color.surface.page", "color.text.default"
    if not (_typed(ts, page) and _typed(ts, text)):
        return []
    light = _scheme(mode) == "light"
    if (luminance(ts.resolve(page, mode)) > luminance(ts.resolve(text, mode))) == light:
        return []
    want = "lighter" if light else "darker"
    return [f"{page} is not {want} than {text} ({mode}); a {_scheme(mode)} scheme needs a "
            f"{want} page, so point {page} and {text} at the other ends of the neutral ramp"]


def _step_of(ts: TokenSet, role: str, mode: str) -> Optional[Tuple[str, int]]:
    """(family, ramp index) a role aliases in one context, or None."""
    raw = ts.raw(role, mode)
    if not is_alias(raw):
        return None
    family, _, step = alias_target(raw).rpartition(".")
    return (family, STEPS.index(int(step))) if step.isdigit() and int(step) in STEPS else None


def _error_edge_hue(ts: TokenSet, mode: str) -> List[str]:
    """Under high contrast the error edge sits at most one ramp step past
    its standard step, so it stays red instead of going near black (light)
    or near white (dark). It fails closed: a high contrast edge that is a
    literal or a step of another ramp is a finding too."""
    role, family = "color.line.danger", "color.danger"
    if parse(mode).get("contrast") != "high" or not _typed(ts, role):
        return []
    std = mode.replace("contrast:high", "contrast:standard")
    high, base = _step_of(ts, role, mode), _step_of(ts, role, std)
    if high is None or high[0] != family:
        where = (f" of its standard step {base[0]}.{STEPS[base[1]]}"
                 if base is not None and base[0] == family else "")
        return [f"{role} ({mode}) is {ts.raw(role, mode)}, not a step of the danger ramp, so "
                f"the error edge can lose its red; point it at a {family} step within one step"
                f"{where}"]
    if base is None or base[0] != family or abs(high[1] - base[1]) <= 1:
        return []
    return [f"{role} ({mode}) sits {abs(high[1] - base[1])} ramp steps from its standard step "
            f"{base[0]}.{STEPS[base[1]]}, so the error edge loses its red; keep it within one "
            "step and let the field's icon and message carry the rest"]


def _lowest(ts: TokenSet, ring: str, mode: str) -> Tuple[float, str]:
    """The ring's lowest ratio against the surfaces it is paired with, and
    that surface."""
    return min((contrast(ts.resolve(ring, mode), ts.resolve(bg, mode)), bg)
               for bg in _opaque_surfaces(ts, ring, mode))


def _opaque_surfaces(ts: TokenSet, ring: str, mode: str) -> List[str]:
    """The surfaces the ring is paired with that resolve to an opaque color
    here; a translucent one is the opaque-pairing check's finding."""
    return [bg for bg in _paired_with(ring)
            if _typed(ts, bg) and len(str(ts.resolve(bg, mode))) == 7]


def _ring_not_weaker(ts: TokenSet, mode: str) -> List[str]:
    """Under high contrast the ring's lowest ratio against its surfaces is
    at least the standard ring's lowest in the same scheme."""
    ring = "color.focus.ring"
    std = mode.replace("contrast:high", "contrast:standard")
    if parse(mode).get("contrast") != "high" or not _typed(ts, ring) \
            or not (_opaque_surfaces(ts, ring, mode) and _opaque_surfaces(ts, ring, std)):
        return []
    (high, bg), (base, base_bg) = _lowest(ts, ring, mode), _lowest(ts, ring, std)
    if high + 1e-9 >= base:
        return []
    return [f"{ring} ({mode}) measures {math.floor(high * 100) / 100:.2f}:1 on {bg}, weaker than "
            f"the standard ring's lowest, {math.floor(base * 100) / 100:.2f}:1 on {base_bg}; "
            "high contrast never weakens focus, so point the high contrast ring at a step with "
            "at least that contrast against every surface"]


def _ring_on_fill(ts: TokenSet, mode: str) -> List[str]:
    """Where the ring stands under RING_ON_FILL against the primary fill,
    a gap of page color of at least 2px keeps it visible: our rule."""
    ring, fill, offset = "color.focus.ring", "color.action.primary", "border.focus-ring.offset"
    if not (_typed(ts, ring) and _typed(ts, fill)) or not ts.has(offset):
        return []
    ratio = contrast(ts.resolve(ring, mode), ts.resolve(fill, mode))
    gap = ts.resolve(offset)
    px = gap["value"] * (16 if gap["unit"] == "rem" else 1) if isinstance(gap, dict) else 0
    if ratio >= RING_ON_FILL or px >= 2:
        return []
    return [f"{ring} stands {math.floor(ratio * 100) / 100:.2f}:1 off {fill} ({mode}) and "
            f"{offset} is {px:g}px; our rule keeps a ring under {RING_ON_FILL:g}:1 against the "
            f"fill at least 2px away from it, so point {offset} at border.width.2 or wider"]


CHECKS: Tuple[Check, ...] = (
    Check("ring-not-weaker", "system", _ring_not_weaker, axes=("scheme", "contrast")),
    Check("ring-on-fill", "system", _ring_on_fill, axes=("scheme", "contrast")),
    Check("error-edge-hue", "system", _error_edge_hue, axes=("scheme", "contrast")),
    Check("states-distinct", "system", _states_distinct, axes=("scheme", "contrast")),
    Check("disabled-distinct", "system", _disabled_distinct, axes=("scheme", "contrast")),
    Check("disabled-visible", "system", _disabled_visible, axes=("scheme", "contrast")),
    Check("line-subtle-visible", "system", _line_subtle_visible, axes=("scheme", "contrast")),
    Check("scheme-polarity", "system", _scheme_polarity, axes=("scheme", "contrast")),
)


def _subtle_steps(depth: float) -> Tuple[str, str]:
    """color.line.subtle for light and dark at standard contrast: neutral
    300, 200 or 100 in light as the surface treatment goes from flat to
    deep; in dark 600 when flat and 700 otherwise, since 800 is the raised
    surface."""
    k = min(2, int(depth * 3))
    return f"color.neutral.{(300, 200, 100)[k]}", f"color.neutral.{(600, 700, 700)[k]}"


def _ring_low(ring_hex: str, mode: str, prims: Dict[str, str],
              pick: Dict[str, Dict[str, str]]) -> float:
    """The ring's lowest ratio against the surfaces PAIRINGS pairs it with."""
    return min(contrast(ring_hex, prims[pick[mode][bg]]) for bg in _paired_with("color.focus.ring"))


def _ring_floor(mode: str, prims: Dict[str, str], pick: Dict[str, Dict[str, str]]) -> float:
    """Under high contrast, the standard ring's lowest ratio against its
    surfaces in the same scheme; 0 in a standard context."""
    if parse(mode).get("contrast") != "high":
        return 0.0
    std = mode.replace("contrast:high", "contrast:standard")
    return _ring_low(prims[pick[std]["color.focus.ring"]], std, prims, pick)


def generate_color(axes: AxisValues, brand_hex: str, brand_role: Optional[str] = None) -> Generated:
    """Low-level call: build_system (and build_color, its color-only
    shortcut) wraps it with input checks, validate and the gate, so prefer
    those unless you need the raw generator.

    Returns the color TokenSet and the retune notes. It never raises for a
    failing pairing: when the ramp cannot reach a minimum it keeps the
    closest step, notes it, and leaves the failure to the gate. The brand's
    role is `brand_role` when given (a brief can name it), else the one the
    axes score highest (character.brand_role).
    """
    notes: List[str] = []
    prims = _primitives(axes, brand_hex.upper(), notes)
    role = brand_role or character.brand_role(axes)
    scores = character.brand_role_scores(axes)
    notes.append(f"color: brand role {role} (" + ("set by the brief" if brand_role else ", ".join(
        f"{k} {scores[k]:.2f}" for k in BRAND_ROLES)) + ")")
    pick = {mode: {r: _default(r, mode, role) for r in SEMANTIC} for mode in COLOR_CONTEXTS}
    # Surface treatment: a flat system draws its separators and card edges
    # a step darker (a hairline carries the shape), a deep one a step
    # lighter (the shadow carries it).
    subtle = _subtle_steps(character.depth(axes))
    for mode in COLOR_CONTEXTS:
        if parse(mode).get("contrast") != "high":
            pick[mode]["color.line.subtle"] = subtle[0 if _scheme(mode) == "light" else 1]

    def value(mode: str, role: str) -> str:
        return prims[pick[mode][role]]

    generic_pairings = [p for p in PAIRINGS if p.fg not in _GROUP_ROLES]
    for mode in COLOR_CONTEXTS:
        for _pass in range(len(generic_pairings) * len(STEPS) + 1):
            changed = False
            for p in generic_pairings:
                for _ in range(len(STEPS)):
                    ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    minimum, criterion = required(p, mode)
                    if ratio >= minimum:
                        break
                    old = pick[mode][p.fg]
                    bg_light = hex_to_oklch(value(mode, p.bg))[0] > 0.5
                    nxt = _step_path(old, +1 if bg_light else -1)
                    if not nxt:
                        break
                    pick[mode][p.fg] = nxt
                    new_ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    notes.append(f"{p.fg} ({mode}): {old} -> {nxt}, "
                                 f"{p.fg} on {p.bg} was {ratio:.2f}:1, now {new_ratio:.2f}:1, "
                                 f"{cite(minimum, criterion)}")
                    changed = True
            if not changed:
                break
        # No generic pairing reads a group role as its background, so each
        # group is solved once, after the loop settles. Under high contrast
        # the ring's lowest ratio against the surfaces never falls below the
        # standard ring's lowest in the same scheme.
        floor = _ring_floor(mode, prims, pick)
        for g in GROUPS:
            _solve_group(g, mode, prims, pick, notes, ring_floor=floor if g.ring else 0.0)

    ts = TokenSet()
    for path, hx in prims.items():
        ts.add(Token(path, "color", hx))
    for role in SEMANTIC:
        base, modes = compress({mode: "{" + pick[mode][role] + "}" for mode in COLOR_CONTEXTS})
        ts.add(Token(role, "color", base, modes=modes, layer="semantic"))
    return Generated(tokens=ts, notes=notes)


_CONTEXT_WORDS = (("scheme:light,contrast:standard", "Light mode"),
                  ("scheme:dark,contrast:standard", "Dark mode"),
                  ("scheme:light,contrast:high", "Light mode, high contrast"),
                  ("scheme:dark,contrast:high", "Dark mode, high contrast"))


def _ratio(v: float) -> str:
    return f"{math.floor(v * 100) / 100:.2f}:1"


def brand_fidelity(ts: TokenSet) -> List[str]:
    """One plain line per color context on the primary fill: whether it is
    the exact brand color, the text on it, where it moved and how far, its
    edge, and the focus ring against it. Read from the tokens, so it states
    what was built. Empty for a set without the primary group."""
    roles = ("color.action.primary", "color.text.on-action", "color.action.primary-edge",
             "color.focus.ring", EXACT)
    if not all(ts.has(p) for p in roles):
        return []
    exact = ts.resolve(EXACT)
    out = _role_lines(ts)
    if out:
        return out + _logo_lines(ts, exact)
    for mode, words in _CONTEXT_WORDS:
        fill, on, edge, ring = (ts.resolve(p, mode) for p in roles[:4])
        text = "black" if on == "#000000" else ("white" if on == "#FFFFFF" else on)
        other = "#FFFFFF" if on == "#000000" else "#000000"
        other_word = "white" if on == "#000000" else "black"
        raw = ts.raw("color.action.primary", mode)
        where = alias_target(raw) if is_alias(raw) else fill
        if where == EXACT or fill == exact:
            line = (f"{words}: the button is the brand color {exact} exactly, with {text} text "
                    f"at {_ratio(contrast(on, fill))} ({other_word} would be "
                    f"{_ratio(contrast(other, fill))}).")
        else:
            distance = oklab_distance(fill, exact)
            need = required(next(p for p in PAIRINGS if (p.fg, p.bg) == (
                "color.text.on-action", "color.action.primary")), mode)[0]
            white, black = contrast("#FFFFFF", exact), contrast("#000000", exact)
            if black >= need and _muddy(exact, "color.base.black", mode):
                why = (f"black text would measure {_ratio(black)} on the brand color, but black "
                       "on a mid tone reads muddy in this mode, and white measures "
                       f"{_ratio(white)}")
            else:
                why = (f"on the brand color white text measures {_ratio(white)} and black "
                       f"{_ratio(black)}, under the {need:g}:1 this mode needs")
            line = (f"{words}: the button is {fill} ({where}), with {text} text at "
                    f"{_ratio(contrast(on, fill))}; {why}.")
            if distance > IDENTITY_DISTANCE:
                line += (f" This fill reads as a different color from the brand (OKLab distance "
                         f"{distance:.2f}), so the button does not carry the brand here; the "
                         "logo (color.logo) and the accents still do.")
        if edge != fill:
            line += f" Its edge is {edge}, so the button still stands out from the page."
        line += f" The focus ring measures {_ratio(contrast(ring, fill))} against the fill."
        out.append(line)
    return out + _logo_lines(ts, exact)


def _role_lines(ts: TokenSet) -> List[str]:
    """For an ink action, the sentence that says where the brand goes
    instead; empty when the brand fills the action."""
    raw = ts.raw("color.action.primary", COLOR_CONTEXTS[0])
    if not (is_alias(raw) and alias_target(raw).startswith("color.neutral.")):
        return []
    link = ts.raw("color.text.link", COLOR_CONTEXTS[0]) if ts.has("color.text.link") else ""
    if is_alias(link) and alias_target(link).startswith("color.neutral."):
        return ["The main action and the links are ink, a neutral from the end of the ramp; the "
                "brand draws edges, rules and link underlines (color.line.accent), the selected "
                "state and the focus ring."]
    return ["The main action is ink, a neutral from the end of the ramp; the brand colors the "
            "links, accents (color.text.accent), the selected state and the focus ring."]


def _logo_lines(ts: TokenSet, exact: str) -> List[str]:
    """Where the logo keeps the exact brand color, and where it moves."""
    if not ts.has("color.logo"):
        return []
    moved = [(words, ts.resolve("color.logo", mode), alias_target(ts.raw("color.logo", mode)))
             for mode, words in _CONTEXT_WORDS if ts.resolve("color.logo", mode) != exact]
    if not moved:
        return [f"The logo (color.logo) is the brand color {exact} exactly in every mode."]
    return [f"The logo (color.logo) is the brand color {exact} except in "
            + "; ".join(f"{words.lower()}, where it is {hx} ({path})" for words, hx, path in moved)
            + ", the nearest step that clears our 3:1 floor against the page."]


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    if inputs.brand_role is None:
        return generate_color(axes, inputs.brand_hex)
    return generate_color(axes, inputs.brand_hex, inputs.brand_role)


FOUNDATION = Foundation(name="color", generate=_generate, pairings=PAIRINGS,
                        checks=CHECKS, hint=seed_hint, role_types=ROLE_TYPES)
