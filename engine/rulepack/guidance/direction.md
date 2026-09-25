# Direction

## Summary

{arabic} Right to left is a standing mode, not a translation pass. Every token that depends on direction is named with logical sides, every contract says how each part behaves under right to left, and the Arabic type rules hold in every style. This file collects the rules for building and checking a right-to-left interface.
{latin} Right to left is a standing mode, not a translation pass. Every token that depends on direction is named with logical sides, and every contract says how each part behaves under right to left. This file collects the rules for building and checking a right-to-left interface.

## Direction is a mode

- Direction is one of the mode axes: dir="rtl" on the html element switches every direction-dependent token at once (decisions/axes-on-the-root.md).
- Tokens never name physical sides: inline-start and inline-end, block-start and block-end, never left, right, top or bottom.
- Every contract part declares its right-to-left behavior: logical (placed with logical properties, so it moves to the other side), mirror (it moves to the other side like a logical part, and its glyph also flips), or fixed (never flips).
- Name frames and screens with their direction so both are reviewed.

## Mirroring

- A part's rtlBehavior governs where it sits; the glyph rules below govern how it is drawn. A logical part moves to the other side without flipping its drawing; a mirror part moves to the other side and also flips its drawing, as the row's chevron sits at the end and points there in both directions. A back arrow points to the start edge, which is on the right under right to left.
- Flip a drawing with transform: scaleX(-1) under [dir="rtl"], or ship a mirrored icon; never flip the container, which would reverse its text.
- The first item of a navigation and the home link sit at the start edge.
- Progress fills from the start edge to the end edge.
- A search icon sits at the start of its field, a clear button at the end.
- A leading icon sits at the start of its label in both directions.
- Icons that point along the line (back and forward arrows, chevrons, send) flip. Icons that point up or down (download, upload, sort), clocks, media controls and icons that do not point (a check, a star, a search glass) keep their drawing.
- Horizontal motion mirrors through motion.inline-sign; vertical motion does not (decisions/unsigned-distances.md).
- Layout that auto layout tools do not mirror on their own, such as a reordered row, is reversed by hand and checked.

{arabic} ## Arabic type

- Every text style but code switches to the Arabic face under right to left.
- The Arabic size at a step is larger than the Latin size by a ratio the two faces' metrics give (1.05 to 1.15, at least 1px), so the two scripts read at one size from body text to the hero; its line height is taller.
{arabic} - A Latin run inside Arabic text, such as a brand name, takes type.run.latin; an Arabic run inside Latin text takes type.run.arabic.
- Letter spacing is 0 for Arabic; spacing breaks the joins between letters.
- Arabic text is never set in italic or with a faux bold.
- Load the Arabic face the tokens name; without it the browser falls back and the sizes do not fit.

## Length and layout

{arabic} - Design fields and buttons at the Arabic length: Arabic copy runs 10 to 25 percent longer than the English draft.
{latin} - Design fields and buttons at the length of the longest language the product ships, not the first draft.
{arabic} - Alignment follows the content's direction, not the frame's: a Latin email address in an Arabic form aligns left inside a right-aligned label.
{latin} - Alignment follows the content's direction, not the frame's: a left-to-right run inside a right-to-left form aligns left inside a right-aligned label.
- Truncation keeps the start of the text in its own direction.
- Tables keep their first column at the start edge.

## Numbers and fixed runs

- Phone numbers, codes, card numbers, email addresses and Latin identifiers are fixed: they run left to right inside right-to-left text and never mirror.
- A fixed run never breaks across lines: wrap it in an element with dir="ltr" and white-space: nowrap, so a phone number never splits and its plus sign stays in front.
{arabic} - An amount with its currency is one fixed run too: 50 د.أ keeps the amount and the abbreviation on one line (content.md).
- Use Western digits and put the currency after the amount with a space (content.md).
- Mixed runs are wrapped so their direction is explicit and punctuation lands where the reader expects it.

## Audit checks

- Every direction-dependent token uses logical names; a physical side in a path is a finding.
- Every contract part has an rtlBehavior, and each rendered part behaves that way.
- Every pointing icon mirrors and every non-pointing icon does not.
- Every fixed run stays left to right and on one line.
{arabic} - Every style under right to left uses the Arabic face, size and leading, with no letter spacing.
{arabic} - Review each screen at the Arabic length in both directions.
{latin} - Review each screen in both directions at the length of the longest language it ships.
