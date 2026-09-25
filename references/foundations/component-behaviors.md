# Component contracts

The mobile contracts for components that appear on every surface: card grids, forms, data tables, and modals, sheets and drawers. A landing page with a quote form, a pricing page with a comparison table and a dashboard with a filter drawer all use them. `/ux-design` loads this file on every build that contains one of these components, whatever surface playbook it picked; the one-playbook rule applies to surface playbooks only.

Component build guidance (states, form layouts, the sheet) lives in `references/surfaces/component.md`. Marketing page chrome and sections (nav bar, announcement topbar, sticky-header budget, hero, feature split, footer) live in `references/surfaces/landing.md`.

## The contract: reflow by design, never break by accident

A layout fails on mobile one component at a time. Each component has a contract: a defined behavior as the viewport narrows.

**Reflow by design** means the narrow state is composed and intentional. A 2-column section splits to 1 column with the image on top. A table becomes a stack of labeled cards. It looks like someone chose it. Reflow that makes a block taller is not automatically good: a composed stack that bloats a sticky header is still a failure.

**Break by accident** means the narrow state looks broken. A label clips. A table sets the page width. A `{TODO_FILL}` token shows because nothing was filled. The browser improvised and it shows.

Same mechanism, opposite outcomes. Engineer the intended narrow state for every component so the browser never has to improvise. When in doubt: show fewer things, stack them cleanly, or move them behind a control. Never cram.

## Card grid (value cards, item cards, coverage tiles)

Reflow the column count with `auto-fit minmax`, ending at 1 column on phones (2 only for small tiles that stay legible). Each card fully contains its content. If cards carry imagery, it is a contained background or a top media block, not a tiny thumbnail crammed beside text. A flat card whose only content is one repeated icon is weak; prefer a backdrop image or a strong typographic element (see the imagery and repeated-icon rules in `references/styles/anti-slop.md`).

## Form

Single column, full-width fields, label above input, controls at least 44px tall, submit button full-width. Inline per-field errors named to the field. Never a multi-column form on a phone.

## Data table

A table never sets the page's width. It lives inside a scroll container or becomes cards. Below a breakpoint (typically 768px or 1024px), the table does one of:

- Wraps in an `overflow-x: auto` scroller that is contained, keeps a sticky first column, and shows an edge shadow that signals more content.
- Transforms each row into a stacked "label: value" card, the columns becoming labeled fields.
- Hides non-essential columns, never the most important one.

A table that overflows the page on mobile with no handling is a failure: users scroll a tiny window.

## Modal, sheet and drawer

Full-screen or bottom sheet, never a desktop-width dialog that overflows the viewport. Focus-trapped, closed by `Esc` and the backdrop, body scroll locked, with a clearly tappable close control.

## Absent values

Omit an absent value's element entirely. A component with no phone number drops the phone affordance; it never renders a placeholder token.
