# Border

## Summary

Border sets the width of every stroke: separators, the edges of containers and controls, emphasis, selection and the focus ring, plus the stroke styles. Widths are whole pixels. Border colors are color roles, and a border role carries a width only. An edge at rest or selected takes a color.line role (color.line.subtle, color.line.input, color.line.selected, and color.line.accent for a link's underline or a highlighted column); a primary button's edge takes color.action.primary-edge, and on the brand band its own fill, color.action.on-brand (decisions/fills-on-every-placement.md), a field in error color.line.danger and a danger button's edge color.status.danger.strong, unless the control is disabled; a disabled edge, in error or not, takes the role its contract names, color.text.disabled for the secondary button and the row's check box and color.line.subtle for the text field (decisions/disabled-contrast.md). Border does not govern the contrast of a stroke; color does.

## Principles

- **A job before a weight.** Every stroke does one job: separate, enclose, emphasize, show selection or show focus. Pick the role for the job, and the width follows.
- **Border, space or surface.** A border is one of three ways to separate things; use it only when space and a surface change are not enough.
- **Fewer lines, clearer structure.** Each extra line raises the visual noise and weakens the lines that matter.
- **Enclose or divide.** An outline says these things belong together; a separator says these siblings are apart. They are different roles even at the same width.
- **State needs more than color.** A selected or emphasized edge is heavier than a resting one.
- **Stable meaning.** A role keeps its job across components and screens, and is never borrowed for its width.
- **Density changes how many lines, not their width.** Dense data views lean on separators to guide the eye; spacious views lean on space.

## Roles

- `border.separator`: a line between siblings inside one parent, such as plain table rows, menu groups, or the divider between a field's prefix and its value; a striped row takes border.outline, since its fill can match the card and its edge is then a container edge (decisions/container-edge.md).
- `border.outline`: the resting edge of a container or a control, such as a card, a field or a secondary button.
- `border.emphasis`: an edge that must outrank the edges around it, such as a highlighted module, a field in error or the boundary of a check box.
- `border.active`: the edge of a selected or active item, such as a selected row or an active tab.
- `border.focus-ring.width`: the width of the keyboard focus ring; at least 2px and wider than an outline.
- `border.focus-ring.offset`: the gap of surface color between an element and its focus ring; at least 1px.
- `border.style.default`: the solid stroke for every border.
- `border.style.placeholder`: the dashed stroke of an empty drop zone or a slot waiting for content.

## Choosing

| Situation | Tool |
|---|---|
| Rows in a dense list or table need scan lines | border.separator with color.line.subtle; a striped row takes border.outline |
| A part inside a group meets the rest, such as a field's prefix or a table's sticky first column | a divider: divider-width at border.separator and divider-color, on the one side where it meets the rest |
| Blocks already read as separate through spacing | space, no border |
| A card, panel or field needs a visible edge | border.outline |
| Related controls should read as one set | border.outline around them, or space.group.gap if proximity is enough |
| Two sections touch and need a stronger boundary | a surface change plus space before a heavier line |
| Major page regions | a surface change and var(--layout-region-gap), the region gap for the viewport's tier |
| A selected item or row | border.active with color.line.selected |
| Keyboard focus | the focus ring (width and offset roles) with color.focus.ring |
| One boundary must outrank its neighbors | border.emphasis |

Emphasis and active widths are used sparingly: when they appear everywhere, the hierarchy flattens. Selection and focus are different states; one role never stands in for the other, and neither appears on something a person cannot interact with.

## Modes

Border varies on contrast. Under high contrast the outline, the emphasis edge, the active edge and the focus ring are each one pixel heavier; the separator and the ring's offset keep their width (decisions/high-contrast-borders.md). Widths are the same in every scheme, density, direction and motion setting. Density changes how many borders a view uses, not their width; in dense views separators replace some of the space.

## Changing the system

1. Border widths move with the contrast axis: at 0.66 or more the focus ring is one step wider. Older and mixed-age readers add a pixel to the ring, up to 3px at standard contrast (decisions/ring-room.md). The high contrast mode adds a pixel to the outline, emphasis, active edge and ring. Change the axis in --axes or the brief and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json.
2. The build keeps widths whole pixels, emphasis and active heavier than the outline, the separator no heavier than the outline, and the focus ring at least 2px with an offset of at least 1px (decisions/whole-pixel-borders.md, decisions/ring-offset.md); a failed check names the role.
3. Never edit a generated value in tokens.json or tokens.css: the build has not checked it, and the next build replaces it.
4. Repointing one role, exempting a role from a check or adding a role comes with the 4.1 importers and the extend mode. Until then, record the need for the system owner.

## Audit scope

Audits the width roles and the rules between them: whole pixels, the weight order, a selected edge heavier than a resting one, and a focus ring wide enough with an offset. It does not audit the color or contrast of strokes (color does) or component layout beyond the contracts.

## Checks

- `focus-ring`: the ring is at least 2px, wider than the outline, and has an offset of at least 1px.
- `active-border`: the selected edge is wider than the resting outline, so selection is not shown by color alone (WCAG 1.4.1).
- `border-weight-order`: emphasis is heavier than the outline, and the separator is no heavier than the outline.
- `border-whole-pixels`: every width is a whole number of pixels.
- `high-contrast-borders`: under high contrast no edge is thinner than at standard contrast, and the ring and the outline are heavier.

## Beyond the gate

- An enabled control whose only edge is color.line.subtle is a finding: its edge may not reach 3:1 (WCAG 1.4.11); use color.line.input.
- A selected state with a zero-width edge passes only when another non-color cue shows it, such as a check mark or a filled icon; record the cue.
- A selection or focus width on a static element is a finding: it signals a state that is not there.
- A screen whose borders outnumber its groups probably separates with lines what space already separates.
- A focus indicator drawn with border instead of outline shifts the layout; that is a finding for the component.

## Handoff notes

- Border roles hold widths only; write the stroke as three properties: border-width from the role, border-style from border.style.default, and border-color from the color role the contract binds for that variant and state: a color.line role, color.action.primary-edge for a primary button, color.action.on-brand for the primary button on the brand band, color.line.danger for a field in error, color.status.danger.strong for a danger button's edge, or, on a disabled control, the disabled edge color the contract names.
- Draw focus with outline, outline-width from border.focus-ring.width and outline-offset from border.focus-ring.offset, so it never moves the layout.
- Use logical sides for single edges: border-block-end for a row separator, border-inline-start for a leading indicator.
- The separator and the outline can share a value; keep both properties in the code so a later change to one does not move the other.

## Common mistakes

- Using the separator and the outline interchangeably because their widths match: a divider starts to read as a container edge.
- Putting selection or focus widths on passive elements: people read a state that does not exist.
- Adding borders where space or a surface already separates: the noise rises and real edges lose weight.
- Drawing focus with a border: the element jumps by the ring's width.
- A hairline border: it disappears on standard screens.
