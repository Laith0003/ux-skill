# Layout

## Summary

Layout sets the page grid and the page regions: three breakpoints that start four tiers (phone, tablet, laptop, desktop), columns, gutters, inline margins, the gap between regions and the hero's block padding per tier, the header and footer padding, the widest container, two reading measures and the minimum target size. Gutters, margins and region spacing alias the spacing scale, so layout and spacing move together. Panes and how they collapse are page patterns built on these tokens, not tokens of their own (decisions/page-regions-by-tier.md).

## Principles

- **Structure first.** Define the regions and the grid before placing anything in them.
- **Priority by space.** The primary task gets the most room and the most stable place; secondary areas give way first.
- **Flow.** Regions are arranged in the order the task is done, following the reading direction.
- **Readable width.** Running text stays within a comfortable measure however wide the screen is.
- **Scannable.** Repeated structure and shared alignment let people find things quickly.
- **Stable under change.** Layout holds when content, width or density change, through defined rules instead of fixes per screen.
- **One set of lines.** Content aligns to the grid's columns and margins; unrelated alignments on one screen look accidental.
- **Deliberate limits.** Containers and reading areas have maximum widths; full width is a choice for data, not the default.
- **Rules, not redesigns.** Each tier changes the grid in a defined way; screens do not invent their own breakpoints.
- **Same page, same rules.** Screens of the same kind share the same grid, margins and patterns.

## Roles

- `layout.breakpoint.<tier>`: the viewport width at which the <tier> tier starts; a reference value for media queries.
- `layout.columns.<tier>`: the number of grid columns in the <tier> tier.
- `layout.gutter.<tier>`: the gap between grid columns in the <tier> tier.
- `layout.margin-inline.<tier>`: the space between the viewport edge and the grid in the <tier> tier.
- `layout.region-gap.<tier>`: the gap between major regions of a product page or an app view, such as a header, the content and the footer, in the <tier> tier.
- `layout.landing-gap.<tier>`: the gap between the sections of a landing page, in the <tier> tier: 128 to 192px at desktop by density, never below the region gap at its tier (decisions/landing-gap.md).
- `layout.hero.padding-block.<tier>`: the space above and below the content of a hero in the <tier> tier.
- `layout.header.padding-block`: the space above and below the content of the page header.
- `layout.footer.padding-block`: the space above and below the content of the page footer.
- `layout.container.max`: the widest the page content grows.
- `layout.measure.text`: the widest a block of running text grows, about 80 characters.
- `layout.measure.form`: the widest a form or a dialog grows.
- `layout.target.large`: the height of a large control, such as the call to action of a hero; 12px above the minimum target.
- `layout.target.min`: the smallest size of anything a person taps or clicks, including icon-only controls such as a dialog's close and a banner's dismiss.

## Choosing

Content widths come in five kinds:

| Kind | Width | For |
|---|---|---|
| Full | every column inside the margins | dense data, wide canvases, dashboards |
| Contained | up to layout.container.max | most pages |
| Reading | up to layout.measure.text | articles, documentation, long text |
| Form | up to layout.measure.form | forms, settings, dialogs |
| Mixed | each region its own kind | pages with reading and tool areas side by side |

The grid names a few areas. The safe area sits inside the inline margins, and every piece of content that must be seen sits in it. A full-bleed area runs past the margins to the viewport edge, for media and backgrounds only. Column lines are the shared edges content aligns to. The grid is fluid: columns widen with the viewport between breakpoints, and the container stops that growth at layout.container.max.

Contained is where every page starts. Full width is picked on purpose, for data, and a data view never takes the reading width. On phones everything is one column inside the margins and secondary areas move below the main content or into an overlay. Pane patterns (navigation, side panels, split views) take their widths from columns and measures, and collapse in a fixed order: secondary tools, then supporting panels, then side regions, then navigation. The main content never collapses.

A block spans a whole number of columns and starts and ends on column lines.

## Modes

Layout varies on density: gutters, margins, the region gap, the landing gap and the hero, header and footer padding take one step less in compact, never below 8px, and the minimum target is 44px in comfortable and 32px in compact. Breakpoints, columns, the container and the measures are the same in every mode. Layout varies on the viewport through the aliases: tokens.css switches each tiered role at the literal breakpoints, since a media query cannot read a custom property, and a density override reaches the alias. The same blocks set the phone factor of the landing display, hero, heading-1, section-title and figure, so they step down below the tablet breakpoint, and each tier's fit factor from the tablet up, so a headline word fits the tier's column (decisions/landing-display-step.md).

## Changing the system

1. Layout moves with the density axis: it sets the gutters, the margins and layout.container.max (1120, 1280 or 1440px). Breakpoints, the columns per tier (4, 8, 12 and 12), the measures and the targets (44px comfortable, 32px compact) are fixed in this version. Change the axis in --axes or the brief and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json.
2. The build keeps the breakpoints strictly increasing, no wider tier with fewer columns, layout.measure.text at 40rem or less and layout.target.min at 44px or more in comfortable; review the main screens of the product after a change.
3. Never edit a generated value in tokens.json or tokens.css: the build has not checked it, and the next build replaces it.
4. Repointing one role, exempting a role from a check or adding a role comes with the 4.1 importers and the extend mode. Until then, record the need for the system owner.

## Audit scope

Audits the grid tokens in both densities: breakpoint order, column order, the region gap, the landing gap and hero padding growing with the viewport, the landing gap at or above the region gap, target size and the reading measure. The WCAG risks are reflow at narrow widths (1.4.10: content works at 320 CSS px without scrolling in two directions), target size (2.5.8, 24 by 24 CSS px; 2.5.5, 44 by 44 CSS px, AAA) and line length (1.4.8, AAA, about 80 characters). It does not audit color, type size or the spacing inside a region.

## Checks

- `layout-breakpoints`: breakpoints strictly increase.
- `layout-columns`: a wider tier never has fewer columns.
- `target-size-minimum`: the minimum target is at least 24px in every density (WCAG 2.5.8).
- `target-size-comfortable`: the minimum target is at least 44px at comfortable density (WCAG 2.5.5, AAA, applied at comfortable density by our choice).
- `text-measure`: the reading measure is 40rem or less, our approximation of 80 characters (WCAG 1.4.8, AAA).
- `layout-regions`: the region gap, the landing gap and the hero padding never shrink as the viewport grows, and the landing gap never falls below the region gap at its tier.
- `layout-on-space`: gutters, inline margins, region and landing gaps and the hero, header and footer padding point at steps of the spacing scale, so layout and spacing move together.

## Beyond the gate

- At 320 CSS px wide, no content needs scrolling in two directions and nothing is cut off (WCAG 1.4.10); check the phone tier first.
- The main content keeps priority at every tier; a layout that narrows it to keep a side panel is a finding.
- Navigation stays reachable on phones, through an overlay, a rail or a visible control.
- Every supporting panel has a defined place on phones: below the content, in an overlay, or hidden behind a control.
- A layout that works only in one orientation is a finding.
- Browser zoom at 400% brings a 1280px window to 320 CSS px, so the reflow check applies to a desktop-only product too. A product that never runs on a phone may record that scope for the phone checks above, never for reflow, and says so in the report instead of skipping a check silently.

## Handoff notes

- Aliases: tokens.css gives each tiered role one property that takes the value of the viewport's tier: --layout-columns, --layout-gutter, --layout-margin-inline, --layout-region-gap, --layout-landing-gap and --layout-hero-padding-block (decisions/landing-display-step.md).
- Page grid: display grid with grid-template-columns: repeat(var(--layout-columns), 1fr), column-gap: var(--layout-gutter), padding-inline: var(--layout-margin-inline), and max-inline-size from layout.container.max with margin-inline: auto. The aliases switch at the breakpoints on their own; no media query is needed for them.
- Page regions: gap or margin-block var(--layout-region-gap) between the regions of a product page, var(--layout-landing-gap) between the sections of a landing page, padding-block var(--layout-hero-padding-block) in the hero.
- A media query of your own for anything else copies the breakpoint value: @media (min-width: 640px) when layout.breakpoint.tablet is 640px.
- Reading and form areas use max-inline-size from layout.measure.text and layout.measure.form.
- Every target uses min-block-size and min-inline-size from layout.target.min.
- Use logical properties throughout, so the grid mirrors under dir="rtl".

## Common mistakes

- Protecting a side panel's width while the main content narrows.
- Constraining a data table to the reading measure.
- Letting text run the full width of a large screen.
- Adding breakpoints per screen instead of using the tiers.
- Reading a breakpoint custom property inside a media query: it does not work; copy the value.
- Spacing page sections with one tier's token, such as --layout-region-gap-desktop, at every width: a phone gets a screen of empty space; use var(--layout-region-gap).
- Spacing a landing page's sections with a gap of your own, such as 160px: it ignores density and the tier; use var(--layout-landing-gap).
