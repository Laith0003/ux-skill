# Elevation

## Summary

Elevation sets how far things float: four shadow levels, each stronger in dark, and the stacking order of floating layers. The surface under a shadow is a color role and the dimming behind a dialog is color.scrim (decisions/elevation-roles.md). Elevation does not govern the contrast of surfaces; color does.

## Principles

- **Every surface has a place.** A surface sits at a defined level: the page, a sunken well, a card, a raised surface, a floating layer. It is never between levels.
- **The lowest level that works.** Use the least elevation that separates what needs separating; escalate only when a lower level fails.
- **Shadows say depth, not style.** A shadow means the surface floats above the one beneath; it is not decoration.
- **Contained or detached.** A card belongs to the page; a dialog or menu floats above it. The two use different levels and different surfaces.
- **Fix layout with layout.** Weak grouping is fixed with space and structure before any shadow is added.
- **Temporary lifts return.** A drag or a press may lift an element for its duration; it comes back to rest when the interaction ends.
- **A scrim travels with its dialog.** The dimming layer appears and leaves with the surface above it; one never shows without the other.

## Roles

- `elevation.card`: the resting shadow of a card or panel on the page.
- `elevation.lifted`: a card that stands above its siblings, or an element held during a drag.
- `elevation.popover`: menus, dropdowns, popovers and tooltips anchored to a control.
- `elevation.dialog`: dialogs and other layers that block the page.
- `elevation.order.base`: the stacking level of normal content.
- `elevation.order.sticky`: headers and toolbars that stick while content scrolls under them.
- `elevation.order.dropdown`: menus and popovers above sticky content.
- `elevation.order.overlay`: the scrim behind a dialog.
- `elevation.order.dialog`: the dialog above its scrim.
- `elevation.order.toast`: transient notices above everything, dialogs included.

## Choosing

| Need | Surface and elevation |
|---|---|
| The page itself | color.surface.page, no shadow |
| Quiet grouping inside the page | color.surface.sunken, no shadow |
| A standard contained block | color.surface.card with elevation.card |
| One block that must stand above its siblings | color.surface.raised with elevation.lifted |
| A menu or popover anchored to a control | color.surface.raised with elevation.popover at elevation.order.dropdown |
| A layer that stops the flow | color.scrim at elevation.order.overlay, then color.surface.raised with elevation.dialog at elevation.order.dialog |
| A short lift while dragging | elevation.lifted for the drag only |
| A layout that feels flat because groups are weak | space and structure, no elevation |

When several siblings all look important, lower one rather than raising all. Not every dialog blocks the page: a panel that leaves the page usable is a popover or a raised surface, not a dialog.

## Modes

Elevation varies on scheme (light, dark). Dark shadows are stronger than light ones so they still read, but in dark the main depth cue is lightness: surfaces lighten as they rise (decisions/dark-elevation-cue.md). The stacking order is the same in every mode.

## Changing the system

1. Read before writing: note each level's shadow in both schemes before changing one.
2. To make shadows stronger or softer, build again with another contrast axis value; every level moves together and stays ordered.
3. Keep every level above the one below it: a larger offset and blur and at least the same strength.
4. Keep dark shadows stronger than light ones, and every level visible in both schemes.
5. Keep the stacking order base, sticky, dropdown, overlay, dialog, toast.
6. To add a level, add a shadow role and an order role for it and place both in the sequence; never reuse a level for a different kind of layer.

## Audit scope

Audits the shadow levels and the stacking order: that each level rises above the one below, that dark is stronger than light, that every shadow is visible, and that the order holds. Shadows are not measured for contrast, so a shadow is never the only edge: a container whose fill measures below our 1.2:1 floor against its surface draws an edge, a contract rule (decisions/container-edge.md). It does not audit surface colors.

## Checks

- `elevation-order`: each shadow level has a larger offset and blur than the one below and at least its strength.
- `elevation-dark`: every level is stronger in dark than in light.
- `visible-shadow`: every level casts a visible shadow in both schemes.
- `stacking-order`: base, sticky, dropdown, overlay, dialog and toast stack in that order.

## Beyond the gate

- A surface whose only boundary is its shadow is a finding when its fill measures below our 1.2:1 floor against the surface under it: the shadow is not measured, so the surface needs an edge or a fill that clears the floor (decisions/container-edge.md).
- A scrim with a shadow is a finding: it reads as a content surface.
- A dialog without its scrim, or a scrim left behind after its dialog closes, is a finding.
- A lift that stays after a drag ends is a finding.
- A z-index without its shadow, or a shadow without its z-index, stacks correctly but reads at the wrong depth.

## Handoff notes

- Each shadow role is a box-shadow custom property with two layers; the stacking roles are unitless z-index numbers.
- Every floating surface sets two things from the same level: box-shadow from its shadow role and z-index from its order role. The surface fill comes from color.
- The scrim is a fixed element with color.scrim as its background at elevation.order.overlay and no shadow.
- Dark shadows switch with data-theme on the html element; components read one property.

## Common mistakes

- Using the dialog level for every modal: a panel that does not block the page is a popover or a raised surface.
- Putting a shadow on the scrim: it becomes a content surface instead of a dimming layer.
- Opening a dialog without its scrim: the page behind still competes for attention.
- Raising every sibling to show importance: nothing stands out.
- Leaving the scrim up after the dialog closes: the page stays dim and blocked.
