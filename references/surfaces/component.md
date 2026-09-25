# Component playbook

The surface playbook for component work. `/ux-design` loads this file, and no other surface playbook, in component mode (`--component`, or a brief that names one element or a small set of components). It holds the rules for building a component: its states, its layout variants, and the patterns where the component library needs more than the mobile contract.

The mobile contracts for card grids, forms, data tables, modals, sheets and drawers live in `references/foundations/component-behaviors.md`, which every build loads when it contains those components. Page chrome for marketing pages (nav bar, announcement bar, sticky-header budget), the hero, feature splits and the footer live in `references/surfaces/landing.md`. The full state and behavior catalogue for each component lives in `references/components/library.md` and `references/foundations/components.md`.

## When it applies

Load this playbook when the brief asks for a component rather than a page: a button, a card or card grid, a form, a data table, a modal, sheet or drawer, a navbar, a chart, or a small set of such components for a design system. A whole page is a landing page or a dashboard, not a component.

## Component build rules

- All four interaction states: default, hover, active, disabled. A button or input that looks identical when hovered, active or disabled is a failure.
- Loading, error and empty states wherever the component can reach them.
- Imagery is mandatory when the component is visual (avatars, product shots, illustrations): real and on-brand, client assets first, then curated Unsplash or Pexels photos chosen to match the brand and its temperature.
- Inter is allowed in component mode. Do not ban it.
- No 3-equal-cards layouts for grouped components.

---

## Form layouts

### Single-column form

**When to use.** Linear flows. Sign-up, sign-in, simple settings. The user works top-to-bottom.

**Required structure.**
- Fields stacked vertically, full-width or comfortably wide (max-width 480-640px).
- Labels above inputs.
- Helper text below inputs (when needed).
- Error text replaces the helper text, or sits under it.
- Submit button at the bottom, start-aligned (full-width on mobile).

**Anti-patterns.**
- Two-column forms when the form has only 4-6 fields. The columns add no value.
- Centered single-column forms with narrow widths that force every label to break into multiple lines.

### Two-column form

**When to use.** Dense settings panels. Forms with many related field pairs (first name + last name, city + zip).

**Required structure.**
- Two-column grid with appropriate gap.
- Related fields side by side; unrelated fields full-width.
- Collapses to single column on mobile.

**Anti-patterns.**
- Two-column for fields that are not related. The user's eye does not know where to go.
- Two-column that does not collapse on mobile.

---

## Sheet (bottom drawer on mobile)

**When to use.** Mobile-first overlay for actions or content. Action sheets, picker UIs, share menus.

**Required behaviors.**
- Slides up from the bottom edge.
- Backdrop scrim above the sheet.
- Drag-to-dismiss handle (a small horizontal bar at the top of the sheet).
- Tap outside to dismiss.
- Max-height typically 80-90% of viewport; user can drag taller or shorter within bounds.

**Anti-patterns.**
- Sheets used on desktop. Desktop wants modals or drawers, not bottom sheets.
- Sheets that cover the entire viewport without a way back. The user feels trapped.

**Code-level guidance.**
- Use a portal as with modals.
- Animation: 250-300ms slide-in, cubic-bezier easing (e.g., `cubic-bezier(0.32, 0.72, 0, 1)`).
- Drag handling: track touch events on the handle; below a threshold (e.g., 100px drag), snap back; above threshold, dismiss.
