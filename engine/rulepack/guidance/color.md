# Color

## Summary

Color sets every surface, text, line, fill and ring in the product, in light and dark and at standard and high contrast. It is generated from one brand color: the brand anchors its ramp at step 500, a neutral ramp takes a trace of the brand hue, and four status ramps sit at fixed hues. The build measures text roles against every surface they can sit on, the input line, the selected line and the focus ring against the page, card, sunken and raised surfaces, and the text on each fill against that fill. Action fills and strong status fills are measured against the page only: on card, sunken and raised a filled control is found by its label and its focus ring, not its fill (decisions/fill-edge-page-only.md). Contracts add the pairings their components need. Color does not govern type size, spacing or shadow; those foundations own them.

## Principles

- **Hierarchy by contrast.** The strongest contrast goes to primary content and the one main action; supporting content steps down. When everything is loud, nothing leads.
- **One meaning per role.** A role means the same thing on every screen and in every component. A role is never borrowed for its value.
- **Separate families.** Brand color marks identity and the main action, neutral carries structure and reading, status colors report outcomes. A family never stands in for another.
- **Saturation is an accent.** Fully saturated color goes on controls, focus and status, not on large surfaces, where it tires the eye and drowns the accent.
- **Depth by lightness.** Surfaces get lighter as they rise. In dark each rising level, page, card and raised, is its own step, and the step, not the shadow, is the main depth cue (decisions/dark-elevation-cue.md). Sunken sits below the page except under dark high contrast, where both are black. In light the card and raised surfaces share white and the shadow tells them apart.
- **Never color alone.** Anything color says, an icon, a word, a shape or a heavier edge says too (WCAG 1.4.1).
- **Measured, not hoped.** Every pairing the build declares is measured in all four color contexts, and a system that fails one is not written. A pairing the build does not declare, such as a fill on a raised surface, is not measured until a contract declares it.

## Roles

- `color.surface.page`: the page itself, the lowest working surface everything else sits on.
- `color.surface.card`: a contained block on the page, such as a card, a panel or a field's fill.
- `color.surface.sunken`: a recessed area below the page, such as a well, a code block, a hovered row or a disabled field.
- `color.surface.raised`: a surface above the page that floats, such as a dialog, a menu or a lifted card.
- `color.surface.inverse`: a surface in the opposite scheme, such as a tooltip or a snackbar; only inverse text and the inverse ring go on it.
- `color.surface.selected`: the tint of a selected item and the hover and pressed fill of secondary and ghost buttons.
- `color.text.default`: body copy, headings, labels and values; the text people read first.
- `color.text.muted`: supporting copy such as helper text, metadata and placeholders; never for disabled text.
- `color.text.link`: links and the labels of secondary and ghost buttons, in the brand color.
- `color.text.inverse`: text on the inverse surface only.
- `color.text.disabled`: the label of an unavailable control, and its edge where it has one (a secondary button, a check box); never to make active text quieter.
- `color.text.on-action`: text and icons on the primary fill and its hover and pressed steps.
- `color.text.on-danger`: text and icons on the danger fill and its hover and pressed steps.
- `color.action.primary`: the fill of the one main action on a view.
- `color.action.primary-hover`: the primary fill under a pointer.
- `color.action.primary-pressed`: the primary fill while pressed.
- `color.action.danger`: the fill of an action that destroys data.
- `color.action.danger-hover`: the danger fill under a pointer.
- `color.action.danger-pressed`: the danger fill while pressed.
- `color.action.disabled`: the fill of an unavailable filled control; it stays visible on card and raised surfaces.
- `color.line.subtle`: a quiet separator between siblings, the edge of a card or dialog that only marks its shape, and the edge of a disabled field; decorative, so never the only edge of an enabled control.
- `color.line.input`: the edge of a field, a check box, a status banner, a row under hover or press, and any control that must be found by its edge.
- `color.line.selected`: the edge and check mark of a selected item, and the edge of a secondary button and of a ghost button under hover or press.
- `color.focus.ring`: the keyboard focus ring on every surface except inverse.
- `color.focus.ring-inverse`: the focus ring on the inverse surface.
- `color.scrim`: the translucent dimming behind a dialog; a layer, never a surface for content.
- `color.status.<status>.text`: status words in running text, such as an error message under a field or the label of a danger secondary or ghost button.
- `color.status.<status>.soft`: the quiet tinted fill of a status banner or badge, and the hover and pressed fill of a danger secondary or ghost button.
- `color.status.<status>.strong`: the solid status color for an icon, a badge, a field's error edge or a danger button's edge.
- `color.status.<status>.on-strong`: text and icons on the strong status fill.

## Choosing

| When you need | Use | Not |
|---|---|---|
| The page background | color.surface.page | card, which is for contained blocks |
| A contained block on the page | color.surface.card with an edge | raised, which floats |
| A floating layer | color.surface.raised with an elevation shadow | card |
| Text people read | color.text.default | a status or link color |
| Secondary information | color.text.muted | color.text.disabled |
| The one main action on a view | a primary button: color.action.primary with color.text.on-action | a second primary, or a status fill |
| Another action that must read as a control on its own | a secondary button: an edge in color.line.selected, the label in color.text.link | a ghost button in an open area |
| A light, repeated action where the layout already marks it as an action | a ghost button: the label in color.text.link, a fill and edge only on hover and press | a secondary button in every row |
| A destructive action | color.action.danger with color.text.on-danger | a warning color |
| A field's edge | color.line.input | color.line.subtle, which may not reach 3:1 |
| A separator inside a card | color.line.subtle | color.line.input |
| A selected item | color.surface.selected with color.line.selected and a heavier edge | the tint alone |
| An error, warning, success or note | the matching color.status roles with an icon and words | the brand color |

Choose a button's emphasis by how it must be found. A primary button is the one main action on a view; its fill is paired with the page only, so elsewhere its label and ring identify it. A secondary button keeps its edge in every state: color.line.selected, paired at 3:1 with every surface the button contract lists, turning to color.text.disabled when disabled, so it reads as a control at rest and when unavailable. Use it for the second action of a pair, a standalone action beside content, and any action on a busy surface. A ghost button has no fill and no edge at rest or when disabled; they appear only on hover and press. At rest only its label, color.text.link at 4.5:1, marks it, and a disabled ghost shows only color.text.disabled, which has no contrast minimum. Use it for low-weight actions that repeat, or that sit where the layout already says they are actions, such as a toolbar, a table row or a card's actions; never as the only control in an open area, and never where a disabled action must still read as a control (decisions/button-intents.md).

Status colors report outcomes only: danger for failure and destruction, warning for risk that can still be avoided, success for a completed outcome, info for neutral guidance. They never color layout, and a status text role never carries body copy.

## Modes

Color varies on scheme (light, dark) and contrast (standard, high). Every semantic role has a value in all four contexts; primitives never change. Dark is not an inversion: each role is chosen for dark and measured there. Under high contrast, text pairings rise to 7:1 and non-text pairings to our 4.5:1 floor, unless a pairing pins its own high-contrast minimum, as the ring on tinted fills (decisions/ring-on-tinted-fills.md) and the disabled label (decisions/disabled-contrast.md) do (decisions/high-contrast-non-text-floor.md). The surfaces move to the ends of the ramp: in light the page, card, sunken and raised surfaces are all white. A container whose fill then measures below our 1.2:1 floor against the surface under it draws an edge (decisions/container-edge.md).

## Changing the system

1. Read before writing: trace the role to the primitive it points at in every context before changing anything.
2. To change the palette, change the brand color and build again; the ramps, roles and pairings are regenerated and measured. Never edit a generated hex in tokens.json or tokens.css.
3. To change one use, point the role at another step in the contexts that need it, then build and let the gate measure it in all four.
4. To add a role, add it to a coverage table, so it is paired with every surface that table lists, or to COVERAGE_EXEMPT with the reason it needs no pairing.
5. To drop a status family, first confirm no contract binds its roles; keep the ramp, since other roles may point at it.
6. Change one thing at a time and build after each change; a failed gate names the pairing and the context.
7. Dark and high contrast are never an afterthought: a change that passes in light is not done until the gate passes in all four contexts.

## Audit scope

Audits the color roles and their pairings in all four contexts: contrast, distinctness, polarity, and whether color is ever the only signal. It does not audit type size, spacing, shadow or which component uses which role beyond the contracts; those have their own audits.

Some roles carry no contrast minimum. Disabled text and fills are checked for distinctness instead, since WCAG exempts inactive controls; the button contract still holds its disabled label to our 1.3:1 floor on the disabled fill (decisions/disabled-contrast.md). The subtle separator is decorative and is checked for distinctness from the surfaces it divides. The scrim is translucent and never enters a pairing; content sits on the raised surface above it. A hover or pressed fill is measured with the text on it, never as an overlay. Action and strong status fills, with their hover and pressed steps, are measured against the page only; on card, sunken and raised a filled control is identified by its label and its focus ring, so an audit checks those there (decisions/fill-edge-page-only.md).

## Checks

- `states-distinct`: each fill's hover and pressed steps differ from the fill and from each other.
- `disabled-distinct`: disabled text differs from default and muted text, and the disabled fill differs from the primary fill.
- `disabled-visible`: the disabled fill differs from the card and raised surfaces, so a disabled button never vanishes.
- `line-subtle-visible`: the subtle separator differs from the card and raised surfaces it divides.
- `scheme-polarity`: in light the page is lighter than the text, in dark it is darker.

## Beyond the gate

- Color is never the only signal: an error has an icon and words, a selected item has a heavier edge or a check, a link inside text is underlined or otherwise marked (WCAG 1.4.1).
- The edge of an enabled field or control uses color.line.input, not color.line.subtle; the subtle line does not promise 3:1.
- A component placed on a surface its contract does not list is measured on that surface before it ships.
- A filled control whose label is not visible, such as an icon-only button, on a card, sunken or raised surface pairs its fill with that surface in its own contract (decisions/fill-edge-page-only.md).
- A brand color near a status hue is not used where it could read as that status (decisions/status-hues.md).
- Text over an image or a gradient is measured against the worst area it covers.
- A pass on the numbers is not a pass when the use breaks the rule: disabled text used for secondary copy fails even though no ratio applies.

## Handoff notes

- Every role is a custom property in tokens.css, grouped surfaces, text, action, line, focus and status; components use those and never a ramp step such as the brand 500.
- Dark and high contrast are the same property names with other values: set data-theme and data-contrast on the html element, or leave them off to follow the operating system.
- The scrim is an 8-digit hex (#RRGGBBAA): a translucent layer for overlays, never a surface for text.
- Hover and pressed are separate roles, not an opacity trick, because each is measured with the text on it.
- Draw focus with outline and outline-offset, using color.focus.ring and the border foundation's width and offset.

## Common mistakes

- Using color.text.default on the inverse surface or on an action or strong status fill: it fails there; use color.text.inverse or the fill's on role. On a soft status fill it is paired and fine.
- Placing text on the scrim: the scrim is a layer; put content on color.surface.raised above it.
- Using disabled text for secondary copy: people read it as unavailable; use color.text.muted.
- Using status colors for neutral structure: a red card edge reads as an error; use color.line roles.
- Changing the brand color without building again: the values in use were never measured against the new brand.
- Checking only light mode after a change: dark and high contrast fail on their own.
