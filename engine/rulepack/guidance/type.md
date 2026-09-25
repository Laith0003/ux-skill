# Type

## Summary

{arabic} Type sets the faces, sizes, weights, line heights and letter spacing of all text, as twelve text styles, one emphasis weight, two run faces and the icon sizes and stroke. Three faces do separate jobs: a display face for the largest statements, a text face for reading and controls, and a mono face for code (and labels in a technical system). The axes choose each face from a small catalog of open-license faces by where it sits on formality, warmth, roundness, type personality and contrast (decisions/face-choice.md); a playful tone word moves type personality toward humanist, so a playful brief gets a friendlier face (decisions/tone-words-reach-shape.md), and each has an Arabic face drawn to sit beside it. Sizes are in rem. Weight and letter spacing change along the scale (decisions/type-along-the-scale.md). Under high contrast text styles are one weight heavier. Under right to left every style but code switches to its Arabic face at a size larger by the ratio the two faces' metrics give (decisions/arabic-proportional.md), with no letter spacing. Type does not govern text color or contrast; color does.
{latin} Type sets the faces, sizes, weights, line heights and letter spacing of all text, as twelve text styles, one emphasis weight, one run face and the icon sizes and stroke. Three faces do separate jobs: a display face for the largest statements, a text face for reading and controls, and a mono face for code (and labels in a technical system). The axes choose each face from a small catalog of open-license faces by where it sits on formality, warmth, roundness, type personality and contrast (decisions/face-choice.md); a playful tone word moves type personality toward humanist, so a playful brief gets a friendlier face (decisions/tone-words-reach-shape.md). Sizes are in rem. Weight and letter spacing change along the scale (decisions/type-along-the-scale.md). Under high contrast text styles are one weight heavier. Type does not govern text color or contrast; color does.

## Principles

- **Role before size.** A style is chosen for what the text is (a page title, a label, a caption), never for how big it should look.
- **Hierarchy by size, character by weight.** Hero, headings and body fall in size, so size sets the rank. The display face's weight eases toward the heading weight as sizes fall, so a light, formal display or a heavy, playful one still meets the text face cleanly; inside a style, weight marks emphasis.
- **Reading comes first.** Body styles keep a line height of 1.5 or more and no negative letter spacing.
{arabic} - **Faces per job and script.** Display, text and mono each have their face, and each Latin face has an Arabic partner; a style never sets Arabic in a Latin face.
{latin} - **Faces per job.** Display, text and mono each have their face; a style never sets code in the text face.
- **One anchor per view.** The hero, when used, appears once; one heading level opens each section.
- **Sizes follow the reader.** Rem sizes grow with the reader's own default text size.
- **Styles are whole.** Size, line height, weight, letter spacing and face travel together in one composite.

## Roles

- `type.text.hero`: the single largest statement on a view, such as a landing page headline, in the display face; once per view.
- `type.text.heading-1`: the title of a page, in the display face.
- `type.text.section-title`: the title of a section of a long page, between the page title and heading-2, in the display face.
- `type.phone.hero`: the factor type.text.hero's size and letter spacing take on a phone, every width below layout.breakpoint.tablet; tokens.css applies it, so a page reads the style as usual.
- `type.phone.heading-1`: the factor type.text.heading-1 takes on a phone, a little gentler than the hero's.
- `type.phone.section-title`: the factor type.text.section-title takes on a phone, so it stays under heading-1 there.
- `type.text.figure`: a price, an amount or a key number shown large, in the display face; set it with tabular figures.
- `type.text.heading-2`: the title of a major block, or of a dialog, in the text face.
- `type.text.heading-3`: the title of a card, a panel or a group.
- `type.text.body`: paragraphs and any text people read in full.
- `type.text.body-small`: secondary paragraphs and dense reading, such as table cells.
- `type.text.ui`: labels on buttons, tabs and menus; short, one line. A field's label takes type.text.ui-large.
- `type.text.ui-large`: the label of a field and of a large button; body size at the ui weight, so a label is never smaller than the value it names.
- `type.text.label`: an eyebrow above a heading, a tag or a line of metadata, spaced open; set in the mono face in a technical system.
- `type.text.fine`: captions, timestamps and small print nobody must read to act.
- `type.text.code`: code, token names and values that need fixed-width characters.
- `type.strong`: the weight of emphasis inside any style; the heading weight, and under high contrast at least 200 above body text, since body text gets heavier there (decisions/strong-under-high-contrast.md).
{arabic} - `type.run.latin`: the face for a Latin run, such as a brand name or a code, inside a right-to-left paragraph.
{latin} - `type.run.latin`: the text face, for a run that must keep it inside a style set in another face.
{arabic} - `type.run.arabic`: the face for an Arabic run inside a left-to-right paragraph.
- `type.icon.size.inline`: an icon inside a line of body text; the body size.
- `type.icon.size.control`: an icon inside a button, a field or a menu item.
- `type.icon.size.feature`: a large icon that heads a feature or an empty state.
- `type.icon.stroke`: the stroke width of line icons drawn on a 24 unit grid, following the display weight.

## Choosing

| Text | Style |
|---|---|
| The one main statement of a landing page | type.text.hero |
| A page title | type.text.heading-1 |
| The title of a section of a long page | type.text.section-title |
| A price or a key amount shown large | type.text.figure |
| A block title, a dialog title | type.text.heading-2 |
| A card or panel title | type.text.heading-3 |
| A paragraph, a banner body | type.text.body |
| A field's helper text or error message | type.text.body-small |
| A dense paragraph, a table cell | type.text.body-small |
| A button, a tab, a menu item | type.text.ui |
| A field's label, a large call to action | type.text.ui-large |
| An eyebrow, a tag, metadata | type.text.label |
| A timestamp, a caption | type.text.fine |
| Code or an identifier | type.text.code |

Styles that work together: a label above a section title or a hero; a heading above body text; a hero with body text or a ui action directly below it; a heading-3 with fine metadata below it, or with ui actions beside it kept at the ui weight; a ui-large label with body-small helper text; code with a fine caption. A heading never sits inside a card at the page title level, body text never labels a button, and fine print never carries text people must read to act, such as a field's error or helper text.

## Modes

{arabic} Type varies on direction and contrast. Under dir="rtl" every style but code uses its Arabic face, the display styles the Arabic display face, at a size larger than the Latin size at the same step by the ratio the two faces' metrics give (at least 1px, at most a fifth), with taller line heights and letter spacing at 0, since spacing breaks the joins between Arabic letters. Code keeps its face, size and leading in both directions, with no letter spacing under right to left; a label set in the mono face switches to the Arabic face like any other text. Under high contrast every style in the text or mono face is one weight heavier, within what the face ships (decisions/high-contrast-weights.md). Under right to left every weight, type.strong's too, is one the Arabic face ships, so a static face never gets a weight it lacks (decisions/font-files.md). The hero, heading-1 and section-title step down on a phone: below layout.breakpoint.tablet tokens.css multiplies their size and letter spacing by their type.phone factor, from a phone scale with a gentler ratio, and they keep falling in size above heading-2 (decisions/type-steps-down-on-phones.md). No other style changes by breakpoint, and none with the density mode; sizes are rem. The brief's density axis sets the reading line heights and the ui size once, at build time.
{latin} Type varies on contrast: under high contrast every style in the text or mono face is one weight heavier, within what the face ships (decisions/high-contrast-weights.md). The hero, heading-1 and section-title step down on a phone: below layout.breakpoint.tablet tokens.css multiplies their size and letter spacing by their type.phone factor, from a phone scale with a gentler ratio, and they keep falling in size above heading-2 (decisions/type-steps-down-on-phones.md). No other style changes by breakpoint, and none with the density mode; sizes are rem. The brief's density axis sets the reading line heights and the ui size once, at build time.

## Changing the system

{arabic} 1. Type moves with every axis but motion: the type personality, formality, warmth, geometry and contrast axes choose the faces, the contrast and formality axes set the display weight and letter spacing, the contrast axis the scale ratio, and the density axis the reading line heights, the ui size and a tighter ratio. Without --latin-only the build keeps an Arabic face beside each Latin one. Change them in --axes or the brief and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json.
{latin} 1. Type moves with every axis but motion: the type personality, formality, warmth, geometry and contrast axes choose the faces, the contrast and formality axes set the display weight and letter spacing, the contrast axis the scale ratio, and the density axis the reading line heights, the ui size and a tighter ratio. Change them in --axes or the brief and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json.
2. The build keeps body at 16px or more, fine at 12px or more, reading line heights at 1.5 or more, the order hero, heading-1, section-title, heading-2, heading-3, body falling in size, no style lighter under high contrast and the icon sizes rising; a failed check names the style and the mode.
3. Never edit a generated value in tokens.json or tokens.css: the build has not checked it, and the next build replaces it.
4. Repointing one role, exempting a role from a check or adding a role comes with the 4.1 importers and the extend mode. Until then, record the need for the system owner.

## Audit scope

{arabic} Audits the text styles in both directions and both contrast modes: minimum sizes, line height and letter spacing for reading, the Arabic rules, rem units, the size order, high contrast weights and the icon sizes. Every text style is held to the same contrast minimum by color, whatever its size (decisions/no-large-text-relaxation.md), so no large-text classification is needed. Whether headings and labels describe their content (WCAG 2.4.6) is a content check (content.md). It does not audit text color.
{latin} Audits the text styles in both contrast modes: minimum sizes, line height and letter spacing for reading, rem units, the size order, high contrast weights and the icon sizes. Every text style is held to the same contrast minimum by color, whatever its size (decisions/no-large-text-relaxation.md), so no large-text classification is needed. Whether headings and labels describe their content (WCAG 2.4.6) is a content check (content.md). It does not audit text color.

## Checks

{arabic} - `type-sizes`: body is at least 16px and fine print at least 12px, in both directions.
{latin} - `type-sizes`: body is at least 16px and fine print at least 12px.
- `reading-leading`: body, body-small and fine have a line height of 1.5 or more (WCAG 1.4.8, AAA).
- `reading-tracking`: reading styles never tighten letter spacing.
{arabic} - `arabic-text`: under right to left every style but code uses its Arabic face at a size at least 1px and at most a fifth above its Latin size, with taller leading, and no style spaces letters.
{latin} - `arabic-text`: this build has one script, so the check has nothing to hold.
{arabic} - `rem-sizes`: every style's size is in rem, in both directions.
{latin} - `rem-sizes`: every style's size is in rem.
{arabic} - `phone-hierarchy`: on a phone hero, heading-1 and section-title keep falling in size above heading-2, in both directions, and each factor sits above 0 and at most 1.
{latin} - `phone-hierarchy`: on a phone hero, heading-1 and section-title keep falling in size above heading-2, and each factor sits above 0 and at most 1.
{arabic} - `type-hierarchy`: hero, heading-1, section-title, heading-2, heading-3 and body fall in size, in both directions.
{latin} - `type-hierarchy`: hero, heading-1, section-title, heading-2, heading-3 and body fall in size.
- `high-contrast-weights`: under high contrast no style is lighter than at standard contrast.
- `strong-weight`: under high contrast type.strong is at least 200 above body text.
- `icon-sizes`: inline, control and feature icons rise in size, and the stroke stays between 1 and 3 units.

## Beyond the gate

- The hero appears at most once per view, and one heading level opens each section.
- Text set at 200 percent zoom still fits its container without cutting words (WCAG 1.4.4).
- Line length for running text stays within layout.measure.text.
{arabic} - An Arabic block inside a Latin page takes the Arabic styles from dir="rtl" and lang="ar" on its element; a Latin run inside Arabic text takes type.run.latin.
{arabic} - A page that ships Arabic loads the Arabic face; a missing face falls back to a system font and breaks the sizes.
- Headings and labels say what follows them; a vague heading is a content finding.

## Handoff notes

- Each style is five custom properties: font-family, font-size, font-weight, line-height and letter-spacing, named after the style, such as --type-text-body-font-size.
- Apply a style as a whole, all five properties together; never size text with a raw value.
- fonts.css, written beside tokens.css, holds a metric-matched fallback for each face, named "<face> Fallback", so text keeps its size and line breaks while the face loads; it does not load the faces. Load them with the Google Fonts link the system report gives, or with fonts-self-host.css and the files it names in a fonts/ folder, and link fonts.css with either one, before tokens.css. Edit neither file (decisions/font-files.md).
- Set type.text.figure with font-variant-numeric: tabular-nums, so amounts line up.
- Draw line icons with stroke-width from type.icon.stroke and size them with the type.icon.size roles.
{arabic} - Direction switches with dir on the html element, and an element inside the page with dir="rtl" or an Arabic lang takes every style's Arabic values on its own, faces, sizes and line heights included (decisions/direction-on-any-subtree.md).
- The hero, heading-1 and section-title step down on a phone on their own; read their properties as usual and never copy a breakpoint to resize them.
- Emphasis inside text uses font-weight from type.strong.

## Common mistakes

- Using the hero or heading-1 more than once on a view: the anchor disappears.
- Using body for button labels: controls need the compact ui style.
- Shrinking the hero with a media query of your own: tokens.css already steps it down on a phone, and a second rule breaks the order with heading-1.
- Using a heading level inside a card that belongs to the page: the hierarchy inverts.
- Using fine print for text people must read: it is too small to sustain.
{arabic} - Tightening letter spacing on Arabic text: the letters disconnect.
- Using fine print for a field's helper or error text: people must read it to act; use body-small.
- Setting body text in the display face: the display face is drawn for large sizes.
