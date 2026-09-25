# Component playbook

The surface playbook for component work. `/ux-design` loads this file, and only this file, when the brief is a single component or a small set of components; `/ux-component` reads it as its surface reference. It holds the responsive contracts for components that appear on any surface, and the layout patterns where those contracts overlap the component library.

Page chrome for marketing pages (nav bar, announcement bar, sticky-header budget), the hero, feature splits and the footer live in `references/surfaces/landing.md`. The full state and behavior catalogue for each component lives in `references/components/library.md` and `references/foundations/components.md`.

## When it applies

Load this playbook when the brief asks for a component rather than a page: a card or card grid, a form, a data table, a modal, sheet or drawer, or a set of such components for a design system. A whole page is a landing page or a dashboard, not a component.

## The contract: reflow by design, never break by accident

A layout fails on mobile one component at a time. Each component has a contract: a defined behavior as the viewport narrows.

**Reflow by design** means the narrow state is composed and intentional. A 2-column section splits to 1 column with the image on top. A table becomes a stack of labeled cards. It looks like someone chose it. Reflow that makes a block taller is not automatically good: a composed stack that bloats a sticky header is still a failure.

**Break by accident** means the narrow state looks broken. A label clips. A table sets the page width. A `{TODO_FILL}` token shows because nothing was filled. The browser improvised and it shows.

Same mechanism, opposite outcomes. Engineer the intended narrow state for every component so the browser never has to improvise. When in doubt: show fewer things, stack them cleanly, or move them behind a control. Never cram.

---

## Card grid (value cards, item cards, coverage tiles)

**Mobile contract.** Reflow the column count with `auto-fit minmax`, ending at 1 column on phones (2 only for small tiles that stay legible). Each card fully contains its content. If cards carry imagery, it is a contained background or a top media block, not a tiny thumbnail crammed beside text. A flat card whose only content is one repeated icon is weak; prefer a backdrop image or a strong typographic element (see the imagery and repeated-icon rules in `references/styles/anti-slop.md`).

---

## Form

**Mobile contract.** Single column, full-width fields, label above input, controls at least 44px tall, submit button full-width. Inline per-field errors named to the field. Never a multi-column form on a phone.

### Single-column form

**When to use.** Linear flows. Sign-up, sign-in, simple settings. The user works top-to-bottom.

**Required structure.**
- Fields stacked vertically, full-width or comfortably wide (max-width 480-640px).
- Labels above inputs.
- Helper text below inputs (when needed).
- Error text below the helper text or replacing it.
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

## Data table

**Mobile contract.** A table never sets the page's width. It lives inside a scroll container or becomes cards. Below a breakpoint (typically 768px or 1024px), the table does one of:

- Wraps in an `overflow-x: auto` scroller that is contained, keeps a sticky first column, and shows an edge shadow that signals more content.
- Transforms each row into a stacked "label: value" card, the columns becoming labeled fields.
- Hides non-essential columns.

**Anti-patterns.**
- Tables that overflow horizontally on mobile without any handling. Users have to scroll a tiny window.
- Hiding the most important column on collapse. Choose what to hide carefully.

---

## Modal, sheet and drawer

**Mobile contract.** Full-screen or bottom sheet, never a desktop-width dialog that overflows the viewport. Focus-trapped, closed by `Esc` and the backdrop, body scroll locked, with a clearly tappable close control.

### Sheet (bottom drawer on mobile)

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

---

## Absent values

Omit an absent value's element entirely. A component with no phone number drops the phone affordance; it never renders a placeholder token.
