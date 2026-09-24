# Type

## Summary

Type sets the faces, sizes, weights, line heights and letter spacing of all text, as nine text styles plus one emphasis weight. The type personality axis picks a pairing of a Latin face and an Arabic face drawn to sit beside it; code uses a monospace face. Sizes are in rem. Under right to left every style but code switches to the Arabic face at its own size and leading, with no letter spacing. Type does not govern text color or contrast; color does.

## Principles

- **Role before size.** A style is chosen for what the text is (a page title, a label, a caption), never for how big it should look.
- **Hierarchy by size.** Hero, headings and body fall in size. Every heading shares one heavier weight, so size, not weight, sets the rank between them; inside a style, weight marks emphasis.
- **Reading comes first.** Body styles keep a line height of 1.5 or more and no negative letter spacing.
- **Faces per script.** Latin, Arabic and code each have their face; a style never sets Arabic in a Latin face.
- **One anchor per view.** The hero, when used, appears once; one heading level opens each section.
- **Sizes follow the reader.** Rem sizes grow with the reader's own default text size.
- **Styles are whole.** Size, line height, weight, letter spacing and face travel together in one composite.

## Roles

- `type.text.hero`: the single largest statement on a view, such as a landing page headline; once per view.
- `type.text.heading-1`: the title of a page.
- `type.text.heading-2`: the title of a major section, or of a dialog.
- `type.text.heading-3`: the title of a card, a panel or a group.
- `type.text.body`: paragraphs and any text people read in full.
- `type.text.body-small`: secondary paragraphs and dense reading, such as banner bodies and table cells.
- `type.text.ui`: labels on buttons, fields, tabs and menus; short, one line.
- `type.text.fine`: captions, helper text, a field's error message, timestamps and metadata.
- `type.text.code`: code, token names and values that need fixed-width characters.
- `type.strong`: the weight of emphasis inside any style; the same as the heading weight.

## Choosing

| Text | Style |
|---|---|
| The one main statement of a landing page | type.text.hero |
| A page title | type.text.heading-1 |
| A section title, a dialog title | type.text.heading-2 |
| A card or panel title | type.text.heading-3 |
| A paragraph | type.text.body |
| A dense paragraph, a banner body | type.text.body-small |
| A button, a field label, a tab | type.text.ui |
| Helper text, a timestamp, a caption | type.text.fine |
| Code or an identifier | type.text.code |

Styles that work together: a heading above body text; a heading-3 with fine metadata below it; a ui label with fine helper text; code with a fine caption. A heading never sits inside a card at the page title level, body text never labels a button, and fine print never carries text people must read in full.

## Modes

Type varies on direction. Under dir="rtl" every style but code uses the Arabic face, at a size 1 to 2px larger than the Latin size at the same step, with taller line heights and letter spacing at 0, since spacing breaks the joins between Arabic letters. Code keeps its face, size and leading in both directions, with no letter spacing. A Latin-only build has no Arabic face and no right-to-left type, and arabic-text has nothing to check there. Type does not change by breakpoint or with the density mode; sizes are rem (decisions/breakpoints-are-reference-values.md). The brief's density axis sets the reading line heights and the ui size once, at build time.

## Changing the system

1. Read before writing: note each style's five fields in both directions.
2. To change the faces, build again with another type personality value, or add a face and point the styles at it; always keep an Arabic face beside a Latin one.
3. To change the scale, build again with another contrast axis value; the ratio and the heading weight follow.
4. To change one style, point one field at another primitive, keeping body at 16px or more, fine at 12px or more, and reading line heights at 1.5 or more.
5. Keep the order hero, heading-1, heading-2, heading-3, body falling in size in both directions.
6. Never merge two styles because their values match today; each has its own job.
7. Never write a text style outside the tokens; a new need is a new style with its five fields.

## Audit scope

Audits the text styles in both directions: minimum sizes, line height and letter spacing for reading, the Arabic rules, rem units and the size order. Every text style is held to the same contrast minimum by color, whatever its size (decisions/no-large-text-relaxation.md), so no large-text classification is needed. Whether headings and labels describe their content (WCAG 2.4.6) is a content check (content.md). It does not audit text color.

## Checks

- `type-sizes`: body is at least 16px and fine print at least 12px, in both directions.
- `reading-leading`: body, body-small and fine have a line height of 1.5 or more (WCAG 1.4.8, AAA).
- `reading-tracking`: reading styles never tighten letter spacing.
- `arabic-text`: under right to left every style but code uses the Arabic face at its size and taller leading, and no style spaces letters.
- `rem-sizes`: every style's size is in rem, in both directions.
- `type-hierarchy`: hero, headings and body fall in size, in both directions.

## Beyond the gate

- The hero appears at most once per view, and one heading level opens each section.
- Text set at 200 percent zoom still fits its container without cutting words (WCAG 1.4.4).
- Line length for running text stays within layout.measure.text.
- Arabic text inside a Latin page, or the reverse, uses the other script's style fields for that run.
- A page that ships Arabic loads the Arabic face; a missing face falls back to a system font and breaks the sizes.
- Headings and labels say what follows them; a vague heading is a content finding.

## Handoff notes

- Each style is five custom properties: font-family, font-size, font-weight, line-height and letter-spacing, named after the style, such as --type-text-body-font-size.
- Apply a style as a whole, all five properties together; never size text with a raw value.
- The faces are named, not loaded: the page loads the Latin face, the Arabic face and the code face it uses.
- Direction switches with dir on the html element; a right-to-left run inside a left-to-right page sets its five properties from the style's Arabic values by hand (decisions/axes-on-the-root.md).
- Emphasis inside text uses font-weight from type.strong.

## Common mistakes

- Using the hero or heading-1 more than once on a view: the anchor disappears.
- Using body for button labels: controls need the compact ui style.
- Using a heading level inside a card that belongs to the page: the hierarchy inverts.
- Using fine print for text people must read: it is too small to sustain.
- Tightening letter spacing on Arabic text: the letters disconnect.
