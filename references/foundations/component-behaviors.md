# Component responsive behaviors

A layout fails on mobile one component at a time. Each component has a **contract**: a
defined behavior as the viewport narrows. The rule across all of them is the same --
*reflow by design, never break by accident*.

## The distinction (read this first)

**Reflow by design** = the narrow state is composed and intentional. A row of rating +
claims collapses to one compact centered line (stars + claims separated by middots), or
shows fewer claims. A 2-column section splits to 1 column with the image on top. It looks
like someone *chose* it. (Reflow that makes the block TALLER is not automatically good --
stacking a claims row into four centered lines is "composed" but it bloats a sticky header;
see the topbar contract and the sticky-header budget below.)

**Break by accident** = the narrow state looks broken. A brand wordmark splits mid-name
("Instant / Skip / Hire" stacked because the box got too narrow). Nav links wrap to a
second ragged row. A button label clips. A `{TODO_FILL}` token shows because nothing was
filled. The browser improvised and it shows.

Same mechanism -- text "wrapped." Opposite outcomes. Your job is to **engineer the intended
narrow state for every component** so the browser never has to improvise. When in doubt:
show fewer things, stack them cleanly, or move them behind a control -- never cram.

---

## Nav bar (primary navigation)

**Desktop:** logo left, links center/right, primary CTA right.
**Mobile contract:** the bar stays **one row**. Only the logo and the single primary CTA
persist; all nav links collapse behind a menu button (hamburger -> drawer). The bar's height
stays sane (<= ~64-72px).

- The brand wordmark must **never split mid-name**. Give it `white-space: nowrap`; if the
  full wordmark won't fit beside the menu + CTA, drop to the logomark alone (keep the icon,
  hide the words) rather than letting "Instant Skip Hire" break to three lines.
- Utility actions (phone, search, account) become **icon-only** below the breakpoint --
  a labeled icon button (`aria-label`), not a text+icon pair that overflows. A phone shows
  the handset glyph, not the number.
- The drawer is a real overlay: focus-trapped, `Esc` and backdrop close it, body scroll
  locked, links are >=44px tall.

**Accidental breaks to kill:** links wrapping to a second row; the wordmark stacking
mid-name; a phone number + label + CTA crammed so the bar becomes 2-3 rows tall; a
`{TODO_FILL: phone}` rendered literally.

**Sticky-header budget (mobile).** Total sticky/fixed top chrome should be ~one row:
target `<= 64-72px`, hard ceiling `~96px`. Only the primary nav + its single CTA persist on
scroll. A decorative/utility bar (ratings, announcement) is NOT sticky -- it sits at the top
and scrolls away (see the topbar contract). A tall sticky header crushes the viewport and is a
failure, not a style choice -- if the summed height of everything that stays pinned exceeds the
ceiling, cut what sticks (drop bars out of the sticky container, shrink padding) until only the
nav row remains. Keep the sticky element wrapping the nav ALONE: a sticky element is bounded by
its containing block, so a utility bar left inside the sticky `<header>` both inflates the
budget AND lets the nav unstick once that box scrolls past.

## Utility / announcement topbar (ratings, trust claims)

**Desktop:** claims inline, divider-separated ("***** Rated Excellent | Same Day | UK Wide").
**Mobile contract -- stay COMPACT.** This bar is secondary chrome; on a phone it must stay
roughly **one line tall**, in priority order:
1. **One condensed centered line** -- the stars then the claims in small text separated by
   middots ("***** Rated Excellent | Same Day Delivery | UK Wide Coverage"), `|` dividers
   swapped for middots, smaller font. This is the default.
2. **Show fewer** -- if one line is still cramped at 360px, keep the stars + the single
   strongest claim and drop the rest on mobile (bring them back at a wider breakpoint).
3. **Horizontal scroller** -- claims in a single `overflow-x: auto` row.

Stacking claims to their own lines is acceptable **only for 1-2 short items**, and **NEVER**
when it makes the header tall -- four centered lines of stars + claims is the exact failure
this contract exists to prevent (it produces a ~150px+ block). Prefer one compact line or
fewer claims over stacking.

**This bar is NOT sticky.** It sits at the very top and **scrolls away** -- only the primary
nav stays pinned (see the Nav sticky-header budget). Leaving it inside a sticky `<header>` both
blows the sticky-header budget and breaks the nav's stickiness (a sticky element is bounded by
its containing block).

**Accidental break to kill:** claims wrapping mid-phrase into 2.5 ragged lines with dangling
"|" dividers; or claims stacked into a tall multi-line block that bloats the header. If three
claims won't fit cleanly on one compact line, drop the weaker ones on mobile -- you never let
them wrap raggedly and you never let the bar grow tall.

## Hero

**Mobile contract:** stack to one column -- copy + CTA first, media below; **or** the media
as a full-bleed background with a legibility scrim (dark overlay) so the headline and accent
stay readable. The headline clamps down (no 56px on a 360px screen). A hero form goes
full-width below the copy.
**Accidental break to kill:** a fixed 2-column hero where the text and form sit side by side
and overflow the viewport.

## Card grid (value cards, item cards, coverage tiles)

**Mobile contract:** reflow column count with `auto-fit minmax`, ending at 1 column on phones
(2 only for small tiles that stay legible). Each card fully contains its content. If cards
carry imagery, it's a **contained background or a top media block** -- not a tiny thumbnail
crammed beside text. A flat card whose only content is one repeated icon is weak; prefer a
backdrop image or a strong typographic element (see hierarchy-and-differentiation).

## Feature split (alternating image + text rows)

**Mobile contract:** stack -- the image goes **full-width above** the text (use `order`), not
a squeezed half-width thumbnail. Rows alternate sides on desktop; on mobile they all stack
the same way (image on top reads best).

## Form

**Mobile contract:** single column, full-width fields, label above input, controls >=44px
tall, submit button full-width. Inline per-field errors named to the field. Never a
multi-column form on a phone.

## Data table

**Mobile contract:** either wrap in an `overflow-x: auto` scroller (contained, with an edge
shadow that signals more) **or** transform each row into a stacked "label: value" card. A
table never sets the page's width -- it lives inside a scroll container or becomes cards.

## Modal / drawer

**Mobile contract:** full-screen or bottom-sheet -- never a desktop-width dialog that
overflows the viewport. Focus-trapped, `Esc`/backdrop closes, body scroll locked, a clearly
tappable close.

## Footer

**Mobile contract:** link columns stack to a single column (or collapse into accordion
sections). Legible spacing, not a cramped 4-column grid squeezed into 360px.

## Do / Don't

- **Do** keep the nav one row on mobile and move links to a drawer; **don't** let nav links
  or the wordmark wrap.
- **Do** turn utility actions into labeled icon-only buttons on mobile; **don't** keep
  text+icon pairs that overflow the bar.
- **Do** stack 2-column sections with the image on top; **don't** ship a side-by-side that
  overflows.
- **Do** collapse a claims bar to ONE compact line (middot-separated) or show fewer, and keep
  it non-sticky; **don't** stack it into a tall multi-line block, and **don't** let claims wrap
  raggedly mid-phrase.
- **Do** keep mobile sticky chrome to ~one row (`<= 72px`, ceiling `~96px`) -- only the nav +
  CTA persist; **don't** pin a tall header or leave decorative bars in the sticky container.
- **Do** omit an absent value's element entirely; **don't** render a placeholder token.
