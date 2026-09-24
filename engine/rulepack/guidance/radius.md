# Radius

## Summary

Radius sets the corners of every shape. The geometry axis sets a base corner, from sharp to soft, and the scale is fixed multiples of it. Six roles say what a shape is: a joined seam, a chip, a control, a card, a dialog, a pill. Radius does not govern the color or width of a focus ring; color and border do.

## Principles

- **Corners signal structure.** A corner says whether a shape is a control, a container or a floating layer, not how big it is or how it should feel on one screen.
- **Nested corners stay concentric.** An element inset in a container by padding takes the container's radius minus the padding.
- **One rule per silhouette.** Every exposed corner of one shape follows the same role; only shared seams are square.
- **Same shape in every state.** A control keeps its radius in default, hover, pressed, focus and disabled.
- **Few families per view.** A screen uses as few radius roles as its structure needs.
- **Softness is a brand setting.** A softer or sharper look moves the whole scale through the geometry axis, not one role at a time.

## Roles

- `radius.joined`: square corners where two shapes share an edge, such as a segmented control or a button group; always 0.
- `radius.chip`: small tags, badges and chips; a pill in soft brands.
- `radius.control`: buttons, fields, toggles and selectable rows; a pill in very soft brands.
- `radius.card`: cards, panels, banners and other containers on the page.
- `radius.dialog`: dialogs, menus, popovers and other floating layers; never less rounded than a card.
- `radius.pill`: fully rounded shapes, such as a pill button or an avatar frame; the final shape follows the element's proportions.

## Choosing

| Shape | Role |
|---|---|
| A button, a field, a toggle, a row a person can choose | radius.control |
| A small tag, badge or chip | radius.chip |
| A card, a panel, a banner | radius.card |
| A dialog, a menu, a popover | radius.dialog |
| A fully round shape | radius.pill |
| The shared edge of joined shapes | radius.joined on the shared corners, the shape's role on the outer ones |

Joined shapes follow three patterns. A group of parts that reads as one shape keeps the role on its outer corners and squares the corners where parts meet. A region attached to another keeps the outline of the main shape and squares the shared edge. Stacked layers round only the corners that stay visible.

Nested shapes step down. A container inside a container without padding between them takes the next smaller role. An element inset by padding takes the outer radius minus the padding, and never the outer radius itself (decisions/nested-radius.md).

## Modes

Radius varies on no axis: corners are the same in every scheme, contrast, density, direction and motion setting. The geometry axis of the brief sets them once, at build time.

## Changing the system

1. Read before writing: note the pixel value of every role before changing one.
2. To make every corner softer or sharper, build again with another geometry axis value; the scale moves as one.
3. To change one shape, point its role at another step, keeping radius.dialog at least radius.card.
4. Keep the joined and nested rules when a parent's radius changes: its inset children and joined parts change with it.
5. Never write a pixel value into a component; if no role fits, propose one and name the shape it is for.
6. Make one change at a time and check the components that use the role.

## Audit scope

Audits the radius roles and the rules between them: the order of the scale, square joins, pill shapes, and a dialog never less rounded than a card. Radius values alone cannot fail a WCAG criterion; the risks are structural, such as a focus ring whose corners do not follow the element or nested corners that bulge. It does not audit focus ring color or width.

## Checks

- `radius-nesting`: radius.card is not rounder than radius.dialog.
- `radius-joined`: radius.joined is 0.
- `radius-pill`: radius.pill is at least 999px, so it is larger than any control's height.
- `radius-scale-order`: the scale steps strictly increase.

## Beyond the gate

- An inset child with the same radius as its parent is a finding; the expected inner radius is the parent's minus the padding.
- A container inside a container at the same role reads flat; the inner one takes the next smaller role.
- A control that changes radius between states is a finding that names the state.
- A focus ring drawn outside a rounded element follows its corner; with outline it does so on its own, with a box shadow it needs the element's radius plus the offset.
- Rounded corners on a shared seam are a finding that names the seam.
- A surface role on a control, or a control role on a floating layer, reads as the wrong kind of shape.

## Handoff notes

- Each role is a custom property; components use the role, never a scale step.
- Compute an inset child's radius in CSS and keep it at 0 or more: max(0px, calc(var(--radius-card) - var(--space-card-padding))).
- Square a shared seam with the logical corner properties, such as border-start-end-radius, so it holds under dir="rtl".
- The radius does not change between states; set it on the base selector only.

## Common mistakes

- Giving an inset child its parent's radius: its corners bulge past the parent's curve.
- Rounding a shared seam: the group reads as separate pieces with gaps.
- Using a card radius on a button: a control should look like a control.
- Using a control radius on a dialog: a floating layer should look detached.
- Using the pill role on a rectangle meant to be slightly rounded: it becomes a capsule.
