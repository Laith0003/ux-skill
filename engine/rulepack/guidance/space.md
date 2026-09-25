# Space

## Summary

Space sets the distances inside and between things: the padding of a control, the gap between controls, the rhythm of text, the gaps between rows, groups and page regions. Every value sits on a 4px scale. Roles are named by the relationship they separate, and the density axis moves them all together. Space does not govern color, type size or the focus ring.

## Principles

- **Relationship first.** Pick a role by what the space separates, never by the size you want; the value follows from the role.
- **Padding is not a gap.** The space inside a container and the space between siblings are different roles, even when their values match, and are never swapped.
- **Nearer means related.** Things that belong together sit closer than things that do not: text gaps are smaller than group gaps, which are smaller than region gaps.
- **Rhythm through repetition.** Repeated items keep one gap, so a list or a grid reads as one structure.
- **Density is deliberate.** Compact is a mode chosen for dense work, not a way to fit more on a crowded screen.
- **Clearance for fingers.** Adjacent controls never sit closer than 8px, in any density.
- **Logical sides.** Inline and block, never left and right, so the same values hold in both directions.

## Roles

- `space.control.gap`: between adjacent controls in a row, such as chips, toggles or a pair of buttons, and between an icon and its label inside a control; never below 8px.
- `space.control.padding-inline`: inside a control, between its edge and its content along the line.
- `space.control.padding-block`: inside a control, between its edge and its content across the line.
- `space.text.gap`: between blocks of text in one flow, such as a heading and its paragraph, or two paragraphs.
- `space.list.gap`: between stacked rows of a list, a table or a menu.
- `space.group.gap`: between groups of related content inside one region, such as sections of a form.
- `space.card.padding`: inside a container such as a card, a panel, a banner or a dialog.
- `space.region.gap`: between major regions of a page; it equals layout.region-gap.desktop at every density. A page that spaces its regions by viewport reads var(--layout-region-gap), which follows the tier.
- `space.control.padding-inline-large`: inside a large control, such as the call to action of a hero, along the line.
- `space.control.padding-block-large`: inside a large control, across the line.
- `space.field.label-gap`: between a field's label and the field.
- `space.field.message-gap`: between a field and its helper text or error message.
- `space.table.cell-padding-inline`: inside a table cell, along the line.
- `space.table.cell-padding-block`: inside a table cell, across the line.

## Choosing

| Situation | Role |
|---|---|
| Buttons, chips or icons side by side | space.control.gap |
| Inside a button or a field | space.control.padding-inline and space.control.padding-block |
| A label above its field | space.field.label-gap |
| A field above its helper text or error message | space.field.message-gap |
| A heading above its text | space.text.gap |
| Inside a table cell | space.table.cell-padding-inline and space.table.cell-padding-block |
| Rows of a list or a table | space.list.gap |
| Sections of a form, groups of settings | space.group.gap |
| Inside a card, panel, banner or dialog | space.card.padding |
| Between the hero and the content, the content and the footer | var(--layout-region-gap), which follows the viewport's tier |
| Page margins and grid gutters | layout.margin-inline and layout.gutter for the tier |

When two neighbors could take either of two roles, take the one for the larger relationship: a heading that opens a group uses the group gap above it and the text gap below it.

Stacked fields in a form sit space.group.gap apart: a label, its field and its helper text form one group, and the group gap separates one field's group from the next.

## Modes

Space varies on density (comfortable, compact). Comfortable is the base; the brief's density axis places it between airy and dense. Compact takes every role one step lower on the scale, never below the role's floor and never larger than comfortable (decisions/two-density-modes.md). The whole page switches with data-density on the html element; density is not scoped to one section (decisions/direction-on-any-subtree.md).

## Changing the system

1. Space moves with the density axis: every role grows larger or smaller together, while the scale stays fixed. Change the axis in --axes or the brief and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json.
2. The build keeps the control gap at 8px or more, the order text gap, group gap, region gap in every density, and compact never larger than comfortable; a failed check names the role and the density.
3. Never edit a generated value in tokens.json or tokens.css: the build has not checked it, and the next build replaces it.
4. Repointing one role, exempting a role from a check or adding a role comes with the 4.1 importers and the extend mode. Until then, record the need for the system owner.

## Audit scope

Audits the spacing roles in both densities: the order of the hierarchy, the scale, compact values against comfortable ones, and the clearance between adjacent controls. It does not audit color, type, the focus ring or where a component places its parts; those have their own audits.

WCAG sets target sizes, not gaps: 2.5.8 asks for targets of 24 by 24 CSS px, or spacing that keeps a 24px circle around each smaller target clear of others. Our 8px control gap is a floor of our own on top of that. The text, group, region and card roles do not sit between targets, so no WCAG rule applies to their values.

## Checks

- `control-gap`: space.control.gap is at least 8px in every density.
- `space-scale-order`: the scale steps strictly increase.
- `space-hierarchy`: text gap, group gap and region gap strictly increase in every density.
- `compact-not-larger`: no role is larger in compact than in comfortable.

## Beyond the gate

- Small targets placed side by side use space.control.gap, never space.list.gap or a text gap.
- A list of rows shorter than 24px needs space between them to meet WCAG 2.5.8; rows at the target size need none (decisions/list-gap-and-control-gap.md).
- Padding and gap are not swapped: a card whose content touches its edge while the card has a large gap uses the wrong role.
- A value typed as a number instead of a role is a finding that names the role it should be.
- When only one density ships, audit that density and say so in the report.

## Handoff notes

- Each role is a custom property; values switch with data-density on the html element, so components never read the compact value directly.
- Use logical properties: padding-inline, padding-block, margin-block, gap. Never padding-left or margin-right, which break under dir="rtl".
- Use gap on flex and grid containers for sibling spacing, and padding for the inside of a container; do not fake a gap with margins on children.
- The icon-to-label space inside a control is space.control.gap.

## Common mistakes

- Using a vertical text gap between items in a row, or the reverse: density moves each relationship separately, so the layout drifts.
- Using the list gap for unrelated blocks: it forces equal spacing on content that is not a repeated set.
- Using card padding between siblings: padding belongs inside the boundary.
- Using the region gap inside a component: page rhythm built from component spacing breaks when either changes.
- Squeezing controls below 8px in compact: the floor holds in every density.
