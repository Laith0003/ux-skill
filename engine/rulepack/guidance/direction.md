# Direction

## Summary

Right to left is a standing mode, not a translation pass. Every token that depends on direction is named with logical sides, every contract says how each part behaves under right to left, and the Arabic type rules hold in every style. This file collects the rules for building and checking a right-to-left interface.

## Direction is a mode

- Direction is one of the mode axes: dir="rtl" on the html element switches every direction-dependent token at once (decisions/axes-on-the-root.md).
- Tokens never name physical sides: inline-start and inline-end, block-start and block-end, never left, right, top or bottom.
- Every contract part declares its right-to-left behavior: logical (placed with logical properties, so it moves to the other side), mirror (the glyph itself flips), or fixed (never flips).
- Name frames and screens with their direction so both are reviewed.

## Mirroring

- Mirror the glyph, never the container: a back arrow points to the start edge, which is on the right under right to left.
- The first item of a navigation and the home link sit at the start edge.
- Progress fills from the start edge to the end edge.
- A search icon sits at the start of its field, a clear button at the end.
- A leading icon sits at the start of its label in both directions.
- Icons that do not point (a check, a star, a search glass) never flip; icons that point (arrows, chevrons, send) do.
- Horizontal motion mirrors through motion.inline-sign; vertical motion does not (decisions/unsigned-distances.md).
- Layout that auto layout tools do not mirror on their own, such as a reordered row, is reversed by hand and checked.

## Arabic type

- Every text style but code switches to the Arabic face under right to left.
- The Arabic size at a step is 1 to 2px larger than the Latin size at the same step, and its line height is taller.
- Letter spacing is 0 for Arabic; spacing breaks the joins between letters.
- Arabic text is never set in italic or with a faux bold.
- Load the Arabic face the tokens name; without it the browser falls back and the sizes no longer fit.

## Length and layout

- Design fields and buttons at the Arabic length: Arabic copy runs 10 to 25 percent longer than the English draft.
- Alignment follows the content's direction, not the frame's: a Latin email address in an Arabic form aligns left inside a right-aligned label.
- Truncation keeps the start of the text in its own direction.
- Tables keep their first column at the start edge.

## Numbers and fixed runs

- Phone numbers, codes, card numbers, email addresses and Latin identifiers are fixed: they run left to right inside right-to-left text and never mirror.
- Use Western digits and put the currency after the amount with a space (content.md).
- Mixed runs are wrapped so their direction is explicit and punctuation lands where the reader expects it.

## Audit checks

- Every direction-dependent token uses logical names; a physical side in a path is a finding.
- Every contract part has an rtlBehavior, and each rendered part behaves that way.
- Every pointing icon mirrors and every non-pointing icon does not.
- Every fixed run stays left to right.
- Every style under right to left uses the Arabic face, size and leading, with no letter spacing.
- Review each screen at the Arabic length in both directions.
