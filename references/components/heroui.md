# HeroUI v3 Component System

HeroUI v3 is a React component library built on Tailwind CSS v4 and React Aria Components. It provides accessible primitives that work out of the box, with theming and customization wired through CSS variables. Use it when you need a tested, accessible component layer under a custom visual system.

This document covers what the system provides, how to install and configure it, how to theme it, how to customize it so it does not look like its defaults, and the per-component patterns and gotchas that come up in real builds.

---

## What the system provides

The library exposes accessible React primitives for the common product UI surfaces. The primitives handle behavior — focus management, keyboard navigation, screen reader announcements, ARIA roles, state management — so the build can focus on visual customization and composition.

Surface coverage at a glance:

- **Layout primitives.** Card, Navbar, Modal, Drawer, Tabs.
- **Form primitives.** Button, TextField, NumberField, Checkbox, Radio, Select, Switch, DatePicker, FileTrigger, Combobox, Form wrapper.
- **Display primitives.** Avatar, Badge, Chip, Divider, Skeleton, Progress, Spinner.
- **Overlay primitives.** Tooltip, Popover, Toast, Notification, Dialog.
- **Data primitives.** Table, Listbox, Menu.

Each primitive is built on React Aria, so the accessibility behaviors are not bolted on after — they are foundational.

---

## Critical: v3 is not v2

The provider, styling, and component API all changed between v2 and v3. Do not apply v2 patterns.

- **Provider.** v2 required a `<HeroUIProvider>` at the root. v3 needs no provider.
- **Animations.** v2 used `framer-motion`. v3 ships CSS-based animations. No extra dependency.
- **Component API.** v2 used flat props (`<Card title="x" />`). v3 uses compound components (`<Card><Card.Header><Card.Title>x</Card.Title></Card.Header></Card>`).
- **Styling.** v2 used Tailwind v3 plus `@heroui/theme`. v3 requires Tailwind v4 plus `@heroui/styles`.
- **Packages.** v2 pulled `@heroui/system` and `@heroui/theme`. v3 pulls `@heroui/react` and `@heroui/styles`.

If your context includes a `HeroUIProvider` or a `framer-motion` import for the library, you are on v2. Migrate or use a different stack. Tailwind v3 will not work with v3 — v4 is mandatory.

---

## Installation

Install the runtime and the styles together:

```bash
npm install @heroui/styles @heroui/react tailwind-variants
```

For an App Router Next.js setup, add Tailwind v4 and the PostCSS plugin:

```bash
npm install @heroui/styles @heroui/react tailwind-variants tailwindcss @tailwindcss/postcss postcss
```

Wire the global stylesheet (`app/globals.css`):

```css
@import "tailwindcss";
@import "@heroui/styles";
```

Import order matters. Tailwind first, library styles after. Reverse it and the cascade breaks.

Import the stylesheet in the root layout:

```tsx
import "./globals.css";

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
```

No provider required. PostCSS config:

```js
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

For a Vite or other React setup, the import order is the same and the PostCSS plugin is the same — adapt to the framework's stylesheet entry point.

---

## Theming with oklch variables

The library uses CSS variables in the `oklch` color space. The naming convention is:

- A variable without a suffix is the background or fill color: `--accent`, `--background`, `--surface`.
- A variable with `-foreground` is the matching text color: `--accent-foreground`, `--background-foreground`.

Default tokens look like:

```css
:root {
  --accent: oklch(0.6204 0.195 253.83);
  --accent-foreground: var(--snow);
  --background: oklch(0.9702 0 0);
  --foreground: var(--eclipse);
}
```

Theme switching is class-based:

```html
<html class="dark" data-theme="dark"></html>
```

To customize, override the variables in your global stylesheet *after* the library styles import. Do not edit the library's stylesheet directly; you will lose your changes on upgrade.

### Dark and light pairings

The library ships paired light and dark tokens. The pairing is:

- `--background` (light) is paired with the dark mode equivalent on `.dark`.
- The `-foreground` variants flip accordingly to maintain contrast.

To override, define both modes:

```css
:root {
  --accent: oklch(0.62 0.18 254);
  --background: oklch(0.99 0 0);
}

.dark {
  --accent: oklch(0.68 0.15 254);
  --background: oklch(0.15 0.01 254);
}
```

### Custom palettes

Override the variable scale to introduce a brand palette:

```css
:root {
  --brand-50: oklch(0.97 0.02 254);
  --brand-100: oklch(0.93 0.04 254);
  --brand-300: oklch(0.81 0.10 254);
  --brand-500: oklch(0.62 0.18 254);
  --brand-700: oklch(0.45 0.16 254);
  --brand-900: oklch(0.25 0.10 254);

  --accent: var(--brand-500);
  --accent-foreground: oklch(0.99 0 0);
}
```

The `oklch` color space lets you tune lightness, chroma, and hue independently — useful for keeping a palette consistent across modes (same hue, different lightness for light/dark).

---

## Customization (do not ship the default look)

The default library palette and shapes are deliberately neutral. Shipping them unmodified produces a generic look — the user will recognize it as the library's defaults, and the product will not feel like itself.

Customize the following before launch:

### 1. Accent color

Override `--accent` with a hue that fits the brand. Keep saturation below 80%. `oklch` lets you tune lightness and chroma independently — use that to keep the accent vibrant without becoming garish.

If the brand has a primary color in a different color space (hex, RGB, HSL), convert to `oklch` for the variable. The conversion is lossy at extreme values but generally clean for mid-range brand colors.

### 2. Radii

The default radius scale is generic. Decide whether the product is sharp (radius 4-6px), soft (8-12px), or pillowed (16-24px). Pick a scale and apply it consistently. The radius scale is one of the strongest carriers of aesthetic — sharp radii read as serious or industrial; soft radii read as friendly; pillowed radii read as playful or contemporary.

### 3. Shadows

Default shadows are neutral. Tint them to the background hue. A faintly blue background wants a faintly blue shadow, not pure black at low opacity. The tinted shadow reads as designed; the neutral shadow reads as a placeholder.

```css
:root {
  --shadow-sm: 0 1px 2px oklch(0.2 0.05 254 / 0.06);
  --shadow-md: 0 4px 12px oklch(0.2 0.05 254 / 0.08);
  --shadow-lg: 0 12px 40px oklch(0.2 0.05 254 / 0.12);
}
```

### 4. Typography

The library does not impose a typeface. You must. Wire `@font-face` for a real type family. Avoid Inter and Roboto unless the product specifically needs them — they are the convergence trap.

Pair display and body if the brand benefits from the contrast. A grotesk display with a humanist sans body reads as designed; a single grotesk throughout reads as default.

### 5. Spacing scale

Tailwind's defaults are sensible but not signature. Set a base unit (4px or 8px) and confirm the scale matches the design system's density. Dashboards want tighter spacing; marketing surfaces want generous spacing.

### 6. Surface colors

Off-white instead of pure white. Off-black instead of pure black. Pure values feel sterile; tinted neutrals feel designed. The library's defaults are already off-white and off-black, but check the values — if they are too close to pure, the product reads as generic.

### The convergence trap

If you ship the library with default tokens, the user will recognize it. That recognition is fine for internal tools where speed matters more than identity. It is a problem for any product that needs its own face. Customize before launch.

---

## Component primitives reference

Each primitive is listed with its one-line purpose. For full anatomy and prop signatures, fetch the component's documentation directly — the documentation is the contract.

| Component | Purpose |
|---|---|
| **Button** | Action trigger with semantic variants (primary, secondary, tertiary, danger, ghost, outline). |
| **Card** | Surface container with compound parts (Header, Title, Description, Content, Footer). |
| **Modal / Dialog** | Focused interaction blocking the page; built on React Aria focus trap. |
| **Drawer** | Side-anchored panel for secondary content or chrome (filters, settings, navigation). |
| **TextField** | Single-line text input with label, helper text, and error message slots. |
| **NumberField** | Numeric input with format support and increment controls. |
| **Checkbox** | Binary state input; supports indeterminate state. |
| **Radio** | Group selection input. |
| **Select** | Single-selection dropdown with searchable variant. |
| **Switch** | Binary toggle with on/off states; for settings, not actions. |
| **DatePicker** | Calendar-based date input with keyboard navigation. |
| **FileTrigger** | File upload trigger; pairs with custom drop zones. |
| **Combobox** | Searchable selection with custom item rendering. |
| **Form** | Wrapper with built-in submit handling, validation orchestration, and accessibility. |
| **Table** | Data grid with sortable headers, selectable rows, and multi-select support. |
| **Navbar** | Top navigation with brand slot, items, end slot, and mobile menu. |
| **Tabs** | Tabbed panel switching with keyboard navigation. |
| **Tooltip** | Hover/focus-triggered label, positioned via Aria. |
| **Popover** | Click-triggered floating panel; focus trap when interactive. |
| **Toast / Notification** | Triggered via hook; queue and dismissal built in. |
| **Avatar** | User image with fallback initials. |
| **Badge** | Small status indicator overlaid on an element. |
| **Chip** | Inline tag with dismiss affordance. |
| **Divider** | Visual separator; horizontal or vertical. |
| **Skeleton** | Loading placeholder matching layout shape. |
| **Progress** | Linear or radial progress indicator. |
| **Spinner** | Indeterminate loading indicator. |
| **Listbox** | Single or multi-select list. |
| **Menu** | Context or action menu. |

Always fetch the component's documentation before implementing. The anatomy, prop tables, and examples are the contract. Compound subcomponents (`Card.Header`, `Table.Row`) are not optional flair; flattening them to props will not work.

---

## Per-component patterns

The component-level patterns and anti-patterns that come up in real builds.

### Button

**Patterns:**
- Use semantic variants: `primary`, `secondary`, `tertiary`, `danger`, `ghost`, `outline`. These adapt to themes and accessibility constraints.
- One primary action per context. If you find yourself wanting two primary buttons in the same view, the design is wrong — promote one to primary and demote the others.
- `tertiary` is for dismissive actions: Cancel, Skip, Dismiss. Not for "another nice button."
- Use `onPress`, not `onClick`. `onPress` is the Aria-friendly handler that works for mouse, touch, keyboard, and assistive tech.

**Anti-patterns:**
- Hardcoding background classes (`bg-blue-500`) on Buttons defeats the variant system.
- Using `primary` for chrome (a "Back" button at the top of a flow). Chrome is `ghost` or `outline`.
- Wrapping a Button in an anchor for navigation. Use the library's native navigation prop if supported, or render an `<a>` directly for true links.

### Card

**Patterns:**
- Compound: `<Card><Card.Header><Card.Title /><Card.Description /></Card.Header><Card.Content /><Card.Footer /></Card>`.
- Cards exist when elevation communicates hierarchy. If the card is just a wrapper around content that already groups, omit it — alignment and spacing carry the structure.
- Hover affordance on cards only when the card is interactive (links to detail page, opens modal). Static cards should not animate on hover.

**Anti-patterns:**
- Cards inside cards inside section wrappers. Strip back to one framing move.
- Equal-height cards locked by flexbox when content varies wildly. Allow variable heights; the visual rhythm is honest.
- Using cards as the universal layout primitive. Most pages do not need cards.

### Modal / Dialog

**Patterns:**
- One primary action in the footer. Cancel is `tertiary`; confirm is `primary` or `danger` depending on consequence.
- Title in the header, description below the title, content in the body.
- Dismiss with: backdrop click (when non-destructive), `Esc` key, explicit close button. All three together for non-destructive modals; only the explicit close for destructive modals.
- Trap focus inside the modal. The library handles this — do not override.

**Anti-patterns:**
- Stacking modals more than two deep. The UX falls apart; users lose track of which modal is which.
- Skipping the close button "because Esc works." Esc is keyboard-only; touch users need the button.
- Using a modal for non-blocking content. If the user can keep working while it is open, it should be a drawer, popover, or toast.

### Drawer

**Patterns:**
- Anchor side (left, right, top, bottom) based on chrome direction. Filters typically anchor right; navigation typically anchors left on mobile.
- Dismiss with backdrop click and Esc. The drawer is less blocking than a modal; users should be able to leave it easily.
- For complex content, a drawer beats a modal — the side-anchored layout preserves orientation.

**Anti-patterns:**
- Drawers that take more than 50% of the viewport width. At that point, the chrome behind is invisible and the drawer should have been a modal or a page.
- Animations slower than 250ms. The drawer should feel responsive; slow animations make the interaction feel laggy.

### TextField, NumberField, and form inputs

**Patterns:**
- Label above the input. Helper text optional, below the input. Error text below the helper text, in `danger` color.
- The label is an explicit component, not a placeholder. Placeholders disappear on focus and hurt accessibility.
- Use the library's `<Form>` wrapper for submit handling. It orchestrates validation and accessibility.
- For `NumberField`, the format prop handles locale-appropriate number rendering.

**Anti-patterns:**
- Floating labels. The library does not invent them; do not bolt them on. They hurt accessibility and add complexity for no real benefit.
- Placeholder-only labels (a placeholder that vanishes when the user types, with no persistent label). Bad for accessibility, bad for users who forgot what the field was for.
- Inline errors that appear on every keystroke. Validate on blur or submit, not on input.

### Select and Combobox

**Patterns:**
- Use `Select` when the list is short (under ~12 items) and the user knows the values.
- Use `Combobox` when the list is long or the user benefits from searching.
- For very long lists (hundreds of items), virtualize the rendering. The library may or may not virtualize by default — check the documentation.

**Anti-patterns:**
- Using `Select` for lists over ~20 items. The dropdown becomes unwieldy.
- Using `Combobox` when the user does not know what they are searching for. Combobox is for search-then-pick; if the user is browsing, use a different pattern.

### Table

**Patterns:**
- Compound: `<Table><Table.Header><Table.Column /></Table.Header><Table.Body><Table.Row><Table.Cell /></Table.Row></Table.Body></Table>`.
- Tabular figures in the body cells for numeric data. The library does not enforce this — set it in your typography layer.
- Sortable headers via the library's prop; multi-select via Aria's selection behavior.
- For dense data, use tight row padding (8-12px). For comfortable data, use generous row padding (16-20px).

**Anti-patterns:**
- Tables with horizontal scroll on desktop. Either reduce columns, prioritize columns, or design a per-column visibility toggle.
- Sortable indicators that are easy to miss. The sort icon should be visible at rest, not only on hover.
- Tables for non-tabular data. If the data is not rows-and-columns, use a different primitive.

### Navbar

**Patterns:**
- Compound: `<Navbar><Navbar.Brand /><Navbar.Items /><Navbar.End /></Navbar>`.
- Brand slot for logo, end slot for user actions or chrome, items for navigation links.
- Mobile collapse is built in. The library handles the hamburger toggle; supply the items.

**Anti-patterns:**
- Stuffing every link into the navbar. Prioritize. If a link is rarely used, move it to a footer or a settings menu.
- Hiding the active state. Users need to know where they are.
- Custom hamburger icons that do not animate to a close icon. The library's default is correct; override with intent.

### Tabs

**Patterns:**
- Tab list horizontal at the top, panels below.
- Visible active state with a tinted indicator or underline.
- Keyboard navigation: arrow keys to switch tabs, Tab to enter the panel.
- For mobile, consider whether tabs or a dropdown is the right pattern. Tabs work when there are 2-5; more than 5 needs a different approach.

**Anti-patterns:**
- Tabs that scroll horizontally with no overflow affordance. If the tabs do not fit, the design needs rework.
- Tabs that wrap to a second line. Two lines of tabs are confusing; redesign.

### Tooltip and Popover

**Patterns:**
- Tooltip for short, non-interactive hints. Position via Aria; the library handles flipping near viewport edges.
- Popover for interactive floating content. Focus trap on the popover when interactive.
- Tooltips should have a short delay before appearing (200-400ms) to avoid showing on accidental hovers.

**Anti-patterns:**
- Tooltips on touch devices. Touch has no hover; the tooltip cannot appear. Use a different pattern for touch.
- Tooltips with long content. If the tooltip needs to explain something complex, use a popover or expand the UI to make the explanation persistent.

### Toast / Notification

**Patterns:**
- Triggered via the library's hook. Queue is built in.
- Auto-dismiss after 4-6 seconds for success; do not auto-dismiss errors.
- Position: top-right or bottom-right typically. Pick one and be consistent.
- One toast at a time on mobile; stacked toasts on desktop.

**Anti-patterns:**
- Toasts for critical errors. A critical error needs a modal or inline error, not a 4-second toast that the user might miss.
- Stacking more than 3 toasts. Beyond 3, the queue is unreadable.
- Toasts for navigation feedback ("page loaded"). Pointless noise.

### Avatar, Badge, Chip, Divider

**Patterns:**
- Avatar with image; fallback to initials with consistent background color (computed from name hash).
- Badge for status indicators (online, away, count). Overlay positioning via the library.
- Chip for inline tags with dismiss. Use sparingly — too many chips on a page is noise.
- Divider for visual separation between unrelated groups. Within a related group, use spacing instead.

**Anti-patterns:**
- Avatars with no fallback. If the image fails to load, the user sees a broken image icon.
- Badges on everything. The badge loses meaning if every element has one.
- Chips as buttons. If clicking the chip does something other than dismiss, use a button.

### Skeleton, Progress, Spinner

**Patterns:**
- Skeleton matching the layout shape. A list skeleton has list-shaped rows; a card skeleton has card-shaped boxes.
- Progress for known-duration tasks (file upload, multi-step form). Linear for chrome, radial for inline.
- Spinner for indeterminate-duration tasks. Should appear only after a delay (200-400ms) to avoid flashing on fast loads.

**Anti-patterns:**
- Skeletons that do not match the eventual layout. The skeleton's job is to reduce perceived layout shift; mismatched skeletons make the shift worse.
- Spinners for known-duration tasks. If you know the duration, use a progress bar.
- Skeletons on every load. For sub-200ms loads, the skeleton flashes and annoys.

---

## When to use HeroUI vs alternatives

### Use HeroUI when:

- You are building a React product UI on Tailwind v4.
- You need accessibility for free (the React Aria foundation handles it).
- You want to focus on visual customization rather than primitive engineering.
- The product is a dashboard, settings panel, admin tool, or product surface where the value is in the workflow, not the chrome.

### Use Radix-based stacks (Radix UI primitives + tailwind-variants, or shadcn/ui) when:

- You want more granular control over the primitives' DOM structure.
- You are willing to assemble more yourself in exchange for finer control.
- The team prefers a "ship the visuals, get the behavior" model where the library gives you behavior and you supply every pixel.

### Use Aria primitives directly when:

- You need a single specialized component (e.g., a combobox with custom rendering) and do not want a full library footprint.
- The product has a strong existing visual system and you only need the behavior of one primitive.

### Use a fuller library (Material UI, Chakra UI) when:

- The project already uses one and the team is committed.
- The team is comfortable with the conventions of that library.
- The design language is compatible with the library's defaults.

### Skip a component library entirely when:

- The surface is editorial or marketing-heavy. Heavy component libraries fight editorial layouts more than they help.
- The team is small and the surface is simple. Vanilla CSS or utility-first without a component layer is often faster and cleaner.
- The project is on a non-React stack and switching is not worth the cost.

### Do not use HeroUI when:

- You cannot move to Tailwind v4. The library requires v4.
- The project is on a non-React stack (Vue, Svelte, Angular, server-rendered with no React layer).
- The team has settled on a different library and the switching cost is not justified by the value.

The library is a tool; the brief decides. Pick the library that matches the surface, not the surface that matches the library.

---

## Common gotchas

### Form input quirks

- The library's input components are controlled. Pass `value` and `onChange`/`onValueChange` consistently.
- Validation runs via the `<Form>` wrapper; standalone inputs handle their own validation.
- File inputs use `<FileTrigger>` — render a custom drop zone, wire `<FileTrigger>` to open the native picker. Do not invent your own file input.

### Drawer animation

- The drawer slides in from the anchor side. The animation duration is configurable; the default is reasonable for most cases.
- On mobile, drawers should cover most of the viewport and feel like a sheet. Adjust the width prop accordingly.
- Drawers do not always reset their scroll position on close. If the drawer's content scrolls, reset on close or the next open shows the scroll position from the previous open.

### Theme switcher

- The class toggle (`.dark`) is the recommended switch mechanism.
- For SSR, suppress hydration warnings on the `<html>` element (`suppressHydrationWarning`) because the class is determined client-side after hydration.
- Persist the theme preference (e.g., in localStorage) and apply it before first paint to avoid the flash of incorrect theme.

### Tailwind v4 syntax

- Tailwind v4 uses `@import "tailwindcss"` instead of the v3 directives (`@tailwind base; @tailwind components; @tailwind utilities`).
- Config is in CSS (`@theme` block) instead of `tailwind.config.js`. Migration guides exist for v3 → v4.
- Some plugin patterns from v3 do not work in v4. If a v3-era snippet does not work, check the v4 migration documentation.

### Compound subcomponents

- The compound pattern is what makes the library composable. Resist wrapping subcomponents into a single "smart" component with all the props.
- Importing a subcomponent directly (e.g., `import { CardHeader } from "@heroui/react"`) sometimes works but breaks the compound semantics. Use the compound form (`Card.Header`) to make the relationship explicit.

### Semantic variants

- Use `primary`, `secondary`, `tertiary`, `danger`, `ghost`, `outline`. These adapt to themes and accessibility constraints.
- Hardcoding colors (`bg-blue-500`) on variants defeats the system. The variant is supposed to absorb the theme; the hardcoded color does not.

### Modal stacking

- The library handles focus trap correctly. Do not stack modals more than two deep — the UX falls apart, and even with correct focus trap, users lose track of which modal is which.

### Toast queue

- Toasts triggered via the hook are queued by the library. Do not invent your own queue.
- Queue capacity is sensible by default; if you hit the cap, the problem is too many toasts, not too small a queue.

### Tooltip on touch

- Tooltips do not appear on touch (no hover). For touch-relevant hints, use a popover triggered by an info icon, or expand the UI to make the hint persistent.

### Server components

- Most primitives are client components (they manage state, handle events). Wrapping a server component in a primitive forces the wrapper to be a client component.
- For pure server-rendered pages, use the primitives' static markup equivalents where the library provides them, or use a lighter primitive.

---

## Anti-patterns

- **Shipping default tokens.** The defaults are the convergence trap. Customize colors, radii, shadows, typography, and spacing before launch.
- **`onClick` instead of `onPress`.** Skips the Aria-friendly handler that works across mouse, touch, keyboard, and assistive tech.
- **Flattening compound components.** Wrapping `Card.Header` and `Card.Title` into a single `<Card title="x" />` defeats the composability.
- **Hardcoded colors on variants.** `<Button className="bg-blue-500">` defeats the variant system.
- **Two primary buttons in one view.** One primary per context. The rest are secondary or below.
- **Modals stacked three deep.** The UX falls apart. Restructure the flow.
- **Tooltips with long content.** Use a popover instead.
- **Toasts for critical errors.** Auto-dismissing on a critical error is a bug.
- **Loading spinners on fast loads.** Delay the spinner 200-400ms; if the load completes before, no spinner at all.
- **Skeletons that do not match the eventual layout.** The skeleton's job is to reduce perceived shift; a mismatched skeleton makes the shift worse.

---

## The library's role

The library is the component layer. It is not the design system. The design system is yours — your tokens, your type stack, your spacing rhythm, your motion philosophy. The library implements the primitives that the design system styles.

The discipline:

1. **Install once, configure deliberately.** The import order, the token overrides, the typography wiring — set these up early and do not revisit unless something breaks.
2. **Customize before launch.** The defaults are neutral; the product is not.
3. **Use the compound API.** Do not flatten.
4. **Use semantic variants.** Do not hardcode colors.
5. **Use `onPress`, not `onClick`.** The Aria handler is the right handler.
6. **Fetch the documentation for each primitive before implementing.** The anatomy is the contract.
7. **Treat the library as a tool, not a style.** You supply the style.

Hold these and the library compounds. The primitives let you ship product UI quickly. The customization makes the product feel like itself. The discipline keeps the build maintainable as it grows.
