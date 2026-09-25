# Decision history

A router, not a story. Each line opens one record; the record says what was decided and why. Read it before changing what it decides.

## Token structure

- [Tokens have two layers, primitives and semantic roles](two-layers.md)
- [Mode axes switch on the root element only](axes-on-the-root.md)
- [Breakpoints are reference values, and type does not change by breakpoint](breakpoints-are-reference-values.md)
- [Density has two modes, comfortable and compact](two-density-modes.md)
- [The build writes fonts.css with local faces first and matched fallbacks](font-loading.md)
- [fonts.css holds the matched fallbacks, fonts-self-host.css the faces, and every weight is one a face ships](font-files.md)
- [Who the product is for arrives as structured fields, and every effect is reported](brief-fields.md)
- [Languages are tags, an Arabic primary script ships Arabic, and every field gets a line](brief-fields-checked.md)
- [A brief can open the page dark, and color-scheme follows every scheme](default-scheme.md)
- [Opposite characters build measurably different systems](distinctness.md)

## Roles per foundation

- [Color keeps one role per job, and interaction states belong to their fill](color-roles.md)
- [Spacing roles name a relationship, and there are eight of them](space-roles.md)
- [Six radius roles follow structure, and geometry sets the scale](radius-roles.md)
- [Border roles are widths for four jobs plus the focus ring](border-roles.md)
- [Elevation is four shadows and a stacking order; surfaces are color](elevation-roles.md)
- [Motion has seven interaction roles and reduced motion is a mode](motion-roles.md)
- [Layout tokens cover the page grid; regions and panes belong to page patterns](layout-scope.md)
- [Layout tokens cover the page grid and its regions; panes belong to page patterns](page-regions.md)
- [Nine text styles as composites, faces chosen per script](type-roles.md)
- [Twelve text styles in three faces, display, text and mono](type-three-faces.md)
- [The axes choose whether the brand fills the action, marks words or draws edges](brand-roles.md)
- [The brand reaches surfaces as a tint, a band or one brand band](brand-surfaces.md)
- [Controls keep their edges and focus ring on the tint, the band, the stripe and the brand band](controls-on-brand-surfaces.md)
- [A supporting accent takes a second hue placed by the axes](support-accent.md)
- [Code blocks and tables have their own surfaces](code-and-table-colors.md)
- [The axes choose each face from a catalog by distance, never by keyword](face-choice.md)
- [Arabic is set larger by a ratio the two faces' metrics give](arabic-proportional.md)
- [Fields and tables have their own inner spacing](field-and-table-spacing.md)
- [Imagery is a foundation of ratios, a measured scrim, a duotone and a tint](imagery-foundation.md)
- [The scrim is measured over the worst image for its text](scrim-worst-image.md)
- [Every build draws decorative brand art from the axes](generated-art.md)

## Contrast and the gate

- [High contrast raises non-text parts to our own 4.5:1 floor](high-contrast-non-text-floor.md)
- [The gate blocks on the AAA criteria it applies](aaa-criteria-that-block.md)
- [Every text style is held to the body text minimum](no-large-text-relaxation.md)
- [The focus ring clears the surfaces, and an offset keeps it off the fill](ring-offset.md)
- [A filled control's fill clears 3:1 against the page only](fill-edge-page-only.md)
- [The primary button's edge carries its contrast against the page](primary-edge.md)
- [A focus ring on a tinted fill keeps 3:1 in high contrast](ring-on-tinted-fills.md)
- [Disabled colors stay distinct and visible, not readable at 4.5:1](disabled-contrast.md)
- [Status colors keep their own hues, whatever the brand hue](status-hues.md)
- [Status colors lean toward the brand and the warmth axis, inside a fixed band](status-harmony.md)
- [Warmth sets the hue and chroma of the neutrals](neutral-tint.md)
- [Warmth moves the neutrals and the duotone light through grey, never around the wheel](warmth-through-grey.md)
- [A brand's hue counts in proportion to its chroma, so a grey brand steers no hue](grey-brands-steer-no-hue.md)
- [A sunken surface sits a small step below the page](recessed-sunken.md)
- [High contrast keeps every surface level apart](high-contrast-surfaces.md)
- [In dark mode, surfaces lighten as they rise](dark-elevation-cue.md)
- [The primary fill keeps the exact brand color whenever text reads on it](brand-fidelity.md)
- [Hover and pressed step away from the fill from where the fill sits in its ramp](exact-fill-states.md)
- [The focus ring never weakens under high contrast, and is measured against the fill](ring-never-weaker.md)
- [The standard focus ring stops one step below the widest, so high contrast can widen it](ring-room.md)
- [The logo keeps the brand color, and decoration has a visibility floor of ours](logo-and-decoration.md)
- [High contrast sets text one weight heavier](high-contrast-weights.md)

## Shape, space and motion

- [Border widths are whole pixels](whole-pixel-borders.md)
- [A dialog is never less rounded than a card, and inner corners follow the padding](nested-radius.md)
- [Stacked rows use the list gap, controls in a row use the control gap](list-gap-and-control-gap.md)
- [Travel distances are unsigned, and one sign follows the reading direction](unsigned-distances.md)
- [Emphasis inside text uses the heading weight](strong-equals-heading-weight.md)
- [Emphasis inside text uses the text face's heading weight](strong-weight.md)
- [Emphasis uses the heading weight, and stays 200 above body text under high contrast](strong-under-high-contrast.md)
- [Reading styles have a line height of 1.5 or more by default](reading-line-height.md)
- [Geometry and formality set one roundness, and every corner follows it](roundness.md)
- [High contrast makes edges and the focus ring heavier](high-contrast-borders.md)
- [The surface treatment runs from flat hairlines to deep shadows](surface-treatment.md)
- [Weight and letter spacing change along the type scale](type-along-the-scale.md)
- [Curves bend continuously, and decoration has one role that reduced motion removes](expressive-motion.md)

## Components

- [A container whose fill measures below 1.2:1 against its surface draws an edge](container-edge.md)
- [Buttons have two intents, neutral and danger](button-intents.md)
- [A field's error edge has its own role and keeps its red](error-edge.md)
- [A landing page starts from one of five compositions, scored from the axes](page-composition.md)
- [A field's helper and error text are readable, and its label is never smaller than its value](readable-fields.md)
- [Buttons come in two sizes, and a view is one screen](button-sizes.md)
- [Card bodies and banner text read at full strength](card-and-banner-reading.md)
- [Every form control has a contract, and they share the field rules](form-contracts.md)
- [Chips, badges, links, navigation, progress and tables have contracts](display-and-navigation-contracts.md)
- [Arabic copy follows the market for currency, months and fixed runs](arabic-market-content.md)
