# Color

## Summary

Color sets every surface, text, line, fill and ring in the product, in light and dark and at standard and high contrast. It is generated from one brand color and the axes. The axes choose the brand's role: it fills the main action (fill), marks words and links while the main action is ink (accent), or draws edges, rules and underlines while actions and links are ink (edge) (decisions/brand-roles.md). The brand anchors its ramp at step 500, a supporting accent takes a second hue the axes place (decisions/support-accent.md), a neutral ramp takes the brand hue pulled warm or cool by the warmth axis (decisions/neutral-tint.md), and four status ramps lean toward the brand inside a fixed band of their own hues (decisions/status-harmony.md). The build measures text roles against every surface they can sit on, the input line, the selected line, the error edge and the focus ring against the page, card, sunken and raised surfaces, and the text on each fill against that fill. The primary button keeps the exact brand color as its fill whenever white or black text reads on it (decisions/brand-fidelity.md), and its edge carries its 3:1 against the page (decisions/primary-edge.md). That edge, the danger fill and the strong status fills are measured against the page only: on card, sunken and raised a filled control is found by its label, its edge and its focus ring. The focus ring is also measured against the primary fill, and under high contrast never measures less than the standard ring (decisions/ring-never-weaker.md). Contracts add the pairings their components need. Color does not govern type size, spacing or shadow; those foundations own them.

## Principles

- **Hierarchy by contrast.** The strongest contrast goes to primary content and the one main action; supporting content steps down. When everything is loud, nothing leads.
- **One meaning per role.** A role means the same thing on every screen and in every component. A role is never borrowed for its value.
- **Separate families.** Brand color marks identity, and by its role the main action, the words or the edges; neutral carries structure and reading; status colors report outcomes. A family never stands in for another.
- **Saturation is an accent.** Fully saturated color goes on controls, focus, status and at most one brand band per view. Elsewhere the brand reaches surfaces as a tint or a band, never behind running text at full strength (decisions/brand-surfaces.md).
- **Depth by lightness.** A surface that sits higher is never darker than the one below it. In dark the page, card and raised surfaces are each their own lighter step, and the step, not the shadow, is the main depth cue (decisions/dark-elevation-cue.md). Where two levels share a color, as card and raised do in light, the shadow or an edge tells them apart. Modes lists the order in each context as built.
- **Never color alone.** Anything color says, an icon, a word, a shape or a heavier edge says too (WCAG 1.4.1).
- **Measured, not hoped.** Every pairing the build declares is measured in all four color contexts, and a system that fails one is not written. A pairing the build does not declare, such as a fill on a raised surface, is not measured until a contract declares it.

## Roles

- `color.surface.page`: the page itself, the lowest working surface everything else sits on.
- `color.surface.card`: a contained block on the page, such as a card, a panel or a field's fill.
- `color.surface.sunken`: a recessed area a small step below the page, such as a well, a hovered row or a disabled field (decisions/recessed-sunken.md).
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
- `color.action.primary`: the fill of the one main action on a view; the exact brand color whenever white or black text reads on it.
- `color.action.primary-edge`: the edge of the primary button: the fill itself when the fill clears the page, else the nearest step of its ramp that does.
- `color.action.primary-hover`: the primary fill under a pointer.
- `color.action.primary-pressed`: the primary fill while pressed.
- `color.action.danger`: the fill of an action that destroys data.
- `color.action.danger-hover`: the danger fill under a pointer.
- `color.action.danger-pressed`: the danger fill while pressed.
- `color.action.disabled`: the fill of an unavailable filled control; it stays visible on card and raised surfaces.
- `color.line.subtle`: a quiet separator between siblings, darker in a flat system and lighter in a deep one (decisions/surface-treatment.md), the edge of a card or dialog that only marks its shape, and the edge of a disabled field; decorative, so never the only edge of an enabled control.
- `color.line.input`: the edge of a field, a check box, a status banner, a row under hover or press, and any control that must be found by its edge.
- `color.line.selected`: the edge and check mark of a selected item, and the edge of a secondary button and of a ghost button under hover or press.
- `color.line.danger`: the edge of a field in error; it carries no text, so it keeps its red under high contrast (decisions/error-edge.md).
- `color.focus.ring`: the keyboard focus ring on every surface except inverse.
- `color.focus.ring-inverse`: the focus ring on the inverse surface.
- `color.scrim`: the translucent dimming behind a dialog; a layer, never a surface for content.
- `color.text.accent`: words in the brand color that are not links, such as an eyebrow above a heading or a highlighted figure; never body copy.
- `color.line.accent`: a brand rule or underline: a link's underline when links are ink, a section rule, the edge of a featured card.
- `color.text.support`: words in the supporting accent's hue, such as a tag or a second highlight; never a link and never body copy.
- `color.surface.tint`: a quiet brand tint behind a group, such as a feature panel or a callout.
- `color.surface.band`: a band in the brand's hue that sets one section of a long page apart.
- `color.surface.brand`: the exact brand color as a band, such as a closing call to action; only color.text.on-brand goes on it.
- `color.text.on-brand`: text and icons on the brand band.
- `color.surface.stripe`: every other row of a table, one step off the card.
- `color.surface.code`: the background of a code block.
- `color.syntax.<name>`: <name> tokens in a code block, on color.surface.code only.
- `color.decorative.<name>`: a <name> shape or pattern with no meaning, such as a form in generated art; never text and never the only cue.
- `color.illustration.line`: lines in a drawing that carry meaning, such as a diagram's arrows or a chart's axis.
- `color.logo`: the logo and brand mark: the exact brand color wherever it clears our 3:1 floor against the page (decisions/logo-and-decoration.md).
- `color.status.danger.text`: danger words in running text, such as an error message under a field, and the label of a danger secondary or ghost button.
- `color.status.danger.soft`: the quiet danger tint of a danger status banner or badge, and the hover and pressed fill of a danger secondary or ghost button.
- `color.status.danger.strong`: the solid danger color for the icon of a danger status banner, a field's error icon, the edge of a danger secondary button and of a danger ghost button under hover or press, and a danger badge.
- `color.status.danger.on-strong`: text and icons on the strong danger fill.
- `color.status.warning.text`: warning words in running text, such as a note about a risk that can still be avoided.
- `color.status.warning.soft`: the quiet warning tint of a warning status banner or badge.
- `color.status.warning.strong`: the solid warning color for the icon of a warning status banner and a warning badge.
- `color.status.warning.on-strong`: text and icons on the strong warning fill.
- `color.status.success.text`: success words in running text, such as a line that confirms a completed outcome.
- `color.status.success.soft`: the quiet success tint of a success status banner or badge.
- `color.status.success.strong`: the solid success color for the icon of a success status banner and a success badge.
- `color.status.success.on-strong`: text and icons on the strong success fill.
- `color.status.info.text`: info words in running text, such as a neutral note of guidance.
- `color.status.info.soft`: the quiet info tint of an info status banner or badge.
- `color.status.info.strong`: the solid info color for the icon of an info status banner and an info badge.
- `color.status.info.on-strong`: text and icons on the strong info fill.

## Choosing

| When you need | Use | Not |
|---|---|---|
| The page background | color.surface.page | card, which is for contained blocks |
| A contained block on the page | color.surface.card with an edge | raised, which floats |
| A floating layer | color.surface.raised with an elevation shadow | card |
| Text people read | color.text.default | a status or link color |
| Secondary information | color.text.muted | color.text.disabled |
| The one main action on a view | a primary button: color.action.primary with color.text.on-action and an edge in color.action.primary-edge | a second primary, or a status fill |
| Another action that must read as a control on its own | a secondary button: an edge in color.line.selected, the label in color.text.link | a ghost button in an open area |
| A light, repeated action where the layout already marks it as an action | a ghost button: the label in color.text.link, a fill and edge only on hover and press | a secondary button in every row |
| A destructive action | color.action.danger with color.text.on-danger | a warning color |
| A field's edge | color.line.input | color.line.subtle, which may not reach 3:1 |
| A field in error | color.line.danger with an icon and a message | the strong danger fill, which goes dark in high contrast |
| A separator inside a card | color.line.subtle | color.line.input |
| A selected item | color.surface.selected with color.line.selected and a heavier edge | the tint alone |
| An error, warning, success or note | the matching color.status roles with an icon and words | the brand color |
| An eyebrow or a highlighted word | color.text.accent | color.text.link, which reads as clickable |
| A group set apart on the page | color.surface.tint | the brand band, which is for one section |
| One section of a long page set apart | color.surface.band | a status soft fill |
| A closing call to action in the brand color | color.surface.brand with color.text.on-brand | a primary button stretched wide |
| A table's alternate rows | color.surface.stripe | color.surface.sunken, which reads as recessed |
| A code block | color.surface.code with the color.syntax roles | text colors meant for surfaces |
| A shape in generated art | a color.decorative role | a status color |
| The logo | color.logo | color.action.primary, which moves for text contrast |

Choose a button's emphasis by how it must be found. A primary button is the one main action on a view; its edge is paired with the page only, so elsewhere its label, edge and ring identify it. A secondary button keeps its edge in every state: color.line.selected, paired at 3:1 with every surface the button contract lists, turning to color.text.disabled when disabled, so it reads as a control at rest and when unavailable. Use it for the second action of a pair, a standalone action beside content, and any action on a busy surface. A ghost button has no fill and no edge at rest or when disabled; they appear only on hover and press. At rest only its label, color.text.link at 4.5:1, marks it, and a disabled ghost shows only color.text.disabled, which has no contrast minimum. Use it for low-weight actions that repeat, or that sit where the layout already says they are actions, such as a toolbar, a table row or a card's actions; never as the only control in an open area, and never where a disabled action must still read as a control (decisions/button-intents.md).

Status colors report outcomes only: danger for failure and destruction, warning for risk that can still be avoided, success for a completed outcome, info for neutral guidance. They never color layout, and a status text role never carries body copy.

An icon takes the role its contract binds; with none, it takes the role of the text beside it.

## Modes

Color varies on scheme (light, dark) and contrast (standard, high). Every semantic role has a value in all four contexts; primitives never change. Dark is not an inversion: each role is chosen for dark and measured there. Under high contrast, text pairings rise to 7:1 and non-text pairings to our 4.5:1 floor, unless a pairing pins its own high-contrast minimum, as the ring on tinted fills (decisions/ring-on-tinted-fills.md) and the disabled label (decisions/disabled-contrast.md) do (decisions/high-contrast-non-text-floor.md). Under high contrast the surfaces move toward the ends of the ramp while each level stays apart: in light the page, card and raised surfaces are white and the sunken surface keeps its recess step, and in dark the page and the sunken surface are black, the card neutral.900 and the raised surface neutral.800 (decisions/high-contrast-surfaces.md). A container whose fill then measures below our 1.2:1 floor against the surface under it draws an edge (decisions/container-edge.md).

## Changing the system

1. Color moves with the brand color and the axes: warmth sets the neutral tint and leans the status hues, and contrast sets how saturated the status colors are. Change them and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json; the ramps, roles and pairings are regenerated and measured in all four contexts.
2. Change one input at a time: a failed gate names the pairing and the context, and a change is not done until it passes in dark and high contrast as well as light.
3. Never edit a generated value in tokens.json or tokens.css: the build has not checked it, and the next build replaces it.
4. Repointing one role, exempting a role from a check or adding a role comes with the 4.1 importers and the extend mode. Until then, record the need for the system owner.

## Audit scope

Audits the color roles and their pairings in all four contexts: contrast, distinctness, polarity, and whether color is ever the only signal. It does not audit type size, spacing, shadow or which component uses which role beyond the contracts; those have their own audits.

Some roles carry no contrast minimum. Disabled text and fills are checked for distinctness instead, since WCAG exempts inactive controls; the button contract still holds its disabled label to our 1.3:1 floor on the disabled fill (decisions/disabled-contrast.md). The subtle separator is decorative and is checked for distinctness from the surfaces it divides. The scrim is translucent and never enters a pairing; content sits on the raised surface above it. A hover or pressed fill is measured with the text on it, never as an overlay. The primary edge, the danger fill with its hover and pressed steps, and the strong status fills are measured against the page only; on card, sunken and raised a filled control is identified by its label, its edge and its focus ring, so an audit checks those there (decisions/primary-edge.md).

## Checks

- `ring-not-weaker`: under high contrast the focus ring measures at least what the standard ring measures against each surface.
- `ring-on-fill`: a ring under 3:1 against the primary fill keeps at least 2px of page color between them, our rule.
- `error-edge-hue`: under high contrast the error edge stays within one ramp step of its standard step, so it stays red; an edge that is a literal color or a step of another ramp is a finding too.
- `states-distinct`: each fill's hover and pressed steps differ from the fill and from each other.
- `disabled-distinct`: disabled text differs from default and muted text, and the disabled fill differs from the primary fill.
- `disabled-visible`: the disabled fill differs from the card and raised surfaces, so a disabled button never vanishes.
- `line-subtle-visible`: the subtle separator differs from the card and raised surfaces it divides.
- `scheme-polarity`: in light the page is lighter than the text, in dark it is darker.

## Beyond the gate

- Color is never the only signal: an error has an icon and words, a selected item has a heavier edge or a check, a link inside text is underlined or otherwise marked (WCAG 1.4.1).
- The edge of an enabled field or control uses color.line.input, not color.line.subtle; the subtle line does not promise 3:1.
- A component placed on a surface its contract does not list is measured on that surface before it ships.
- A filled control whose label is not visible, such as an icon-only button, on a card, sunken or raised surface pairs its fill with that surface in its own contract (decisions/primary-edge.md).
- A brand color near a status hue is not used where it could read as that status (decisions/status-harmony.md).
- Text over an image or a gradient is measured against the worst area it covers.
- A pass on the numbers is not a pass when the use breaks the rule: disabled text used for secondary copy fails even though no ratio applies.

## Handoff notes

- Every role is a custom property in tokens.css, grouped surfaces, text, action, line, focus and status; components use those and never a ramp step such as the brand 500.
- Dark and high contrast are the same property names with other values: set data-theme and data-contrast on the html element, or leave them off to follow the operating system. tokens.css sets color-scheme with each scheme, so native controls such as date pickers and selects follow it; a brief that opens dark makes dark the default and data-theme="light" still switches it (decisions/default-scheme.md).
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
