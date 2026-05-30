# Responsive & mobile-first

The single most common shipped defect is a layout that looks right at 1440px and falls
apart at 360px. Mobile is not a smaller desktop -- it is the primary canvas. Design the
360px view first; desktop is the enhancement. A layout that has not been seen at 360px
is not finished.

## Principles

1. **Mobile-first.** Author the 360-390px layout first, then add complexity upward with
   `@media (min-width: ...)`. Never design wide and "make it responsive" after.
2. **Zero horizontal scroll, ever.** On a phone, the page never scrolls sideways. This is
   non-negotiable, not a nice-to-have. It is the first thing to verify and the most common
   thing to get wrong.
3. **Every element has a defined behavior at every width.** Nothing is left to the
   browser's default reflow. You decide what each block does as it narrows -- you do not
   discover it.
4. **Content reflows; it does not shrink.** Text wraps and stacks; columns become rows. Text
   never scales down to illegibility, and nothing is clipped or cut off to "make it fit."
5. **Touch targets >= 44x44px.** Fingers are not cursors. Links, buttons, and form controls
   need real hit area and spacing on mobile.
6. **Reflow by DESIGN, never break by ACCIDENT** (the distinction that matters most).
   Intentional reflow is good: a row of claims becoming centered stacked lines, a 2-column
   section becoming 1 column with the image on top. Accidental break is the failure: a brand
   wordmark splitting mid-name, nav items wrapping into ragged multiple rows, a label
   clipping, content overflowing its card. Same mechanism ("it wrapped") -- opposite
   outcomes. **The test:** does the narrow state look composed and intended, or does it look
   like it fell apart? Engineer the intended narrow state; never let the browser improvise it.

## The horizontal-scroll killers (memorize these -- they cause ~all of it)

| Cause | Fix |
|---|---|
| `width: 100vw` (includes the scrollbar's width -> overflows) | `width: 100%` |
| Fixed px widths wider than the viewport | `max-width: Npx; width: 100%` |
| Unconstrained media (`img`/`video`/`iframe`) | `max-width: 100%; height: auto; display: block` |
| Long unbroken strings (URLs, tokens, emails) | `overflow-wrap: anywhere` |
| `white-space: nowrap` on real prose | only for short labels/pills, never sentences |
| Flex/grid child that won't shrink | `min-width: 0` on the child (the #1 hidden cause inside flex) |
| Absolutely-positioned content escaping its box | contain it; `position: relative` parent + `overflow: clip` |
| Wide tables | wrap in `overflow-x: auto` container, or collapse to cards |
| Fixed column counts in a grid | `grid-template-columns: repeat(auto-fit, minmax(min(100%, Npx), 1fr))` |

## Breakpoints

- **Think in content, not devices.** Add a breakpoint where the layout *starts to strain*,
  not at "an iPhone is 390px." If a 3-card row gets cramped at 900px, break at 900px.
- Sane defaults when you have no better signal: `<=640` phone (1 column), `641-1024` tablet,
  `>=1024` desktop. These are starting points, not law.
- Mobile-first queries: the base styles ARE the mobile layout; `min-width` queries add columns
  and scale upward. Avoid `max-width` queries that try to undo desktop on mobile.

## Fluid type & space

- Use `clamp(min, preferred, max)` for display type so it scales across the range without a
  dozen breakpoints: `font-size: clamp(1.9rem, 6vw, 3.5rem)`. A 56px headline must clamp down
  to ~30-34px on a phone -- never ship desktop display sizes to 360px.
- Section padding should also breathe down: generous on desktop, tighter on mobile (clamp or
  a smaller mobile value), so a hero isn't 160px of dead space on a phone.

## Viewport units (the traps)

- `100vw` overflows by the scrollbar width on desktop -> use `100%` for widths.
- `100vh` is wrong on mobile (it ignores the browser chrome, causing jump/cutoff) -> use
  `100svh` or `100dvh` for full-height sections.

## Verify -- this is mandatory, not optional

1. Measure at **360 AND 390px**: `document.documentElement.scrollWidth <= window.innerWidth`.
   If it's greater, there is horizontal scroll -- find the offending node and fix it before
   anything else.
2. **scrollWidth alone misses WRAP.** A nav that wrapped to 3 rows still reports
   `scrollWidth == innerWidth`. Also check: do the children of a bar that should be one row
   share an `offsetTop` (if not, it wrapped)? Is the sticky header a sane height (<= ~96px)?
   Did any short label/wordmark split across lines?
3. Headless screenshots are unreliable in this toolchain. **Deploy the iteration and look on a
   real phone.** An un-eyeballed mobile layout is unverified -- treat "I think it's fine" as
   "it is broken until seen."

## Do / Don't

- **Do** build and test the 360px layout first; **don't** retrofit responsiveness onto a
  desktop comp.
- **Do** give every multi-column block an explicit single-column mobile state; **don't** rely
  on the default flex/grid wrap to "handle it."
- **Do** clamp display type and section padding; **don't** ship desktop sizes to phones.
- **Do** constrain every image with `max-width: 100%`; **don't** ever use `width: 100vw`.
- **Do** make the reflowed state look intentional; **don't** accept a layout that merely
  "doesn't crash" on mobile.

## Patterns

### Stacking hero
```css
.hero { display: grid; grid-template-columns: 1fr; gap: 2rem; }
@media (min-width: 900px) { .hero { grid-template-columns: 1.1fr 0.9fr; } }
.hero h1 { font-size: clamp(2rem, 6vw, 3.5rem); }
.hero img { max-width: 100%; height: auto; display: block; }
```

### Column-count-free card grid (never a fixed N that overflows)
```css
.cards { display: grid; gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); }
```
At 360px each card is full-width automatically; no media query needed, and it can never
force horizontal scroll.
