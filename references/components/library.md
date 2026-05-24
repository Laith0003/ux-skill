# Component Pattern Library

A library-independent reference for the patterns that appear in every product UI. Each pattern is described as: when to use, the required states, the anti-patterns, and code-level guidance that holds whether you are using a component library, headless primitives, or vanilla HTML and CSS.

Read this when you are deciding which pattern fits a surface, or when you are implementing a pattern and want to make sure it covers all the states the design needs.

The required states list for any interactive element is:

1. **Default** (idle).
2. **Hover** (mouse over, or focus on touch).
3. **Active** (pressed, mid-interaction).
4. **Focus** (keyboard or programmatic).
5. **Disabled** (non-interactive).

Some patterns add: loading, error, success, and selected.

---

## Buttons

The action trigger. Every interactive surface uses buttons; getting them right is the foundation of every other pattern.

### Primary button

**When to use.** The single most important action in the current context. Submit a form. Confirm a decision. Move to the next step. One per context — if two actions feel equally primary, the design is wrong.

**Required states.**
- Default: high-contrast fill, brand or accent color background, clear label.
- Hover: slight darkening (5-10%), optional shadow lift, cursor pointer.
- Active: deeper darkening (15%), optional slight scale-down (0.97-0.98) or position shift.
- Focus: visible ring (2-3px) at offset (2-4px). Never rely on default browser ring; style explicitly.
- Disabled: 40-50% opacity, no hover effect, cursor not-allowed.
- Loading: spinner replaces or sits next to label; button is unclickable; do not collapse width.

**Anti-patterns.**
- Two primary buttons in the same view. Promote one to primary, demote others.
- Tiny primary buttons (under 32px tall). The primary should feel important; tiny defeats the purpose.
- All-uppercase labels by default. Use sentence case unless the brand specifically uses caps.
- Bouncing or pulsing primary buttons. Calm primaries feel professional; bouncy primaries feel pushy.

**Code-level guidance.**
- Use a semantic `<button>` element (or `<a>` if it navigates). Never use a `<div>` with an onClick.
- Set `type="button"` or `type="submit"` explicitly. The default `submit` inside a form causes accidental submissions.
- Min height 40px on desktop, 44px on touch (matches WCAG touch target floor).
- Transition: `transition: all 200ms ease;` on base, faster on active (150ms).

### Secondary button

**When to use.** Important but not the primary action. Cancel inside a confirm flow. Edit inside a view flow. Add another. Save draft.

**Required states.**
- Default: lower contrast than primary — outlined, ghosted, or muted fill.
- Hover: slight darkening or fill increase.
- Active: deeper change, never matching primary's visual weight.
- Focus: same ring discipline as primary.
- Disabled: same opacity treatment.
- Loading: same spinner behavior.

**Anti-patterns.**
- Secondary buttons that look identical to primary. The user cannot tell which is which.
- Five secondary buttons in a row. Too many secondaries means the design has not chosen.

**Code-level guidance.**
- Same min-height, same touch-target rules.
- The outline variant uses a 1-1.5px border. Avoid 1px on retina-only screens where you want extra weight; 1.5px reads better at most densities.

### Ghost button

**When to use.** Tertiary or dismissive actions. Cancel. Skip. Close. Actions that should be discoverable but not prominent.

**Required states.**
- Default: no background, no border, label only (often in a muted color).
- Hover: subtle background tint appears (5-10% of brand or neutral).
- Active: tint deepens.
- Focus: ring visible.
- Disabled: text opacity reduced.

**Anti-patterns.**
- Ghost buttons that disappear visually until hovered. The user does not know they exist.
- Ghost buttons for primary actions. The lack of weight signals "skip me."

**Code-level guidance.**
- Same dimensions as other buttons for layout consistency.
- The hover tint should be visible without being loud. 8% opacity of the brand color often works.

### Destructive button

**When to use.** Delete. Remove. Cancel-with-loss. Actions that have negative consequences and cannot be easily undone.

**Required states.**
- Default: red or danger fill, white text. Never use a tinted red — the saturation signals danger.
- Hover: slight darkening.
- Active: deeper darkening.
- Focus: ring visible, in the danger color (not the brand color).
- Disabled: same opacity treatment.
- Confirmation: when the action is destructive, prefer a confirmation modal over a single-click destructive button.

**Anti-patterns.**
- Destructive buttons positioned as the primary action when the user is not in a destructive context. "Delete account" should not be the bottom-right button of every settings screen.
- Destructive buttons with cute or jokey copy. ("Yeet it" instead of "Delete.") The destructive button needs to read as serious.

**Code-level guidance.**
- Position consistently: the destructive button is typically on the left of the modal footer (where users do not casually click), with the safe action (Cancel) on the right.
- When destruction is irreversible, require explicit confirmation — type the resource name, or check a box, before the button is enabled.

### Icon-only button

**When to use.** When space is tight and the action is universally understood. Close (X), more options (kebab), back (arrow), search (magnifying glass).

**Required states.**
- Default: icon centered in a square or circular hit area.
- Hover: background tint or icon color change.
- Active: deeper tint.
- Focus: ring around the entire hit area.
- Disabled: icon opacity reduced.

**Anti-patterns.**
- Icon-only buttons for non-universal actions. If the icon needs a label to be understood, it is not icon-only — it is "icon plus invisible label," which means inaccessible.
- Icon hit areas smaller than 40x40px on desktop, 44x44px on touch. Tiny icons frustrate everyone.
- Multiple icon-only buttons in a row with no labels. Looks like chrome but functions as a guessing game.

**Code-level guidance.**
- Always provide an `aria-label` for screen readers.
- Hit area should be larger than the icon itself. A 16px icon needs a 40px button.
- Use `currentColor` for the icon's fill or stroke so it inherits from the button's text color.

---

## Inputs

The text-entry primitives. Every form is built from these.

### Text input

**When to use.** Single line of free-form text. Names, titles, search queries, short answers.

**Required states.**
- Default: bordered or underlined input with a visible label above.
- Hover: slight border darkening.
- Focus: stronger border color, optional focus ring around the input, never the browser's default outline alone.
- Filled: the user has typed something; label remains visible.
- Disabled: opacity reduced, background slightly different.
- Error: red border, error message below in red text. Helper text (if present) is replaced by or accompanied by the error.

**Anti-patterns.**
- Placeholder-as-label. The label disappears when the user types and reappears when empty; users forget what the field was for.
- No visible focus state. The user cannot tell where the keyboard is.
- Errors that show on every keystroke. Validate on blur or submit, not on input.
- "Form contains errors" with no per-field messages. Always tell the user which field and what to fix.

**Code-level guidance.**
- Use a `<label>` element associated with the input via `htmlFor` or wrapping. Never use placeholder as the only label.
- Helper text below the input. Error text below the helper (or replacing it). Both with appropriate `aria-describedby` linking.
- Input min-height 40px on desktop, 44px on touch.

### Textarea

**When to use.** Multi-line text. Descriptions, comments, longer messages.

**Required states.**
- Same as text input, plus resize behavior. Default resize is vertical-only; horizontal-resize breaks layout.
- Auto-grow optional but useful: the textarea expands as the user types, up to a max height.

**Anti-patterns.**
- Fixed-tiny textarea (2 rows) for content that obviously needs more space.
- Disabling resize entirely without auto-grow. Users feel cramped.

**Code-level guidance.**
- `resize: vertical;` by default.
- For auto-grow, observe the content height on input and adjust the textarea's height; cap at a max (300-500px).
- Min-height matches the natural multi-line use case (4-6 rows).

### Select (dropdown)

**When to use.** Single selection from a known, short list. Status, role, country.

**Required states.**
- Default: input-like surface with a chevron indicating dropdown.
- Hover: border darkening.
- Open: dropdown menu visible, current selection highlighted.
- Focus: ring visible; keyboard navigation works (arrow keys to navigate, Enter to select, Esc to close).
- Disabled: opacity, no chevron interaction.
- Error: same red border treatment as text input.

**Anti-patterns.**
- Select with hundreds of items. Use a combobox or autocomplete instead.
- Native `<select>` styled to look custom but with native dropdown chrome. Either go fully custom (with proper keyboard handling) or stay fully native.
- No selected state inside the open dropdown. The user cannot tell what is currently selected.

**Code-level guidance.**
- Native `<select>` is the most accessible default. Custom selects require careful keyboard and screen reader work.
- The dropdown's max-height should not exceed the viewport; on long lists, scroll the menu.

### Multiselect

**When to use.** Multiple selections from a list. Tags, categories, recipients.

**Required states.**
- Default: input area showing selected items as chips or pills, with the search-and-add affordance.
- Each selected chip has its own dismiss state.
- Hover, focus, disabled, error: as above.

**Anti-patterns.**
- Multiselect without a way to remove items. Users add but cannot subtract.
- Multiselect where the order matters but the UI does not support reordering. If order matters, support drag.

**Code-level guidance.**
- Selected items are clearly visually distinct from the search input.
- Pressing Backspace at an empty input position removes the last selected item (a common pattern that users learn quickly).

### Autocomplete (combobox)

**When to use.** Searchable list. Many possible values, user knows what they are looking for.

**Required states.**
- Default: text input with a dropdown that opens on focus or input.
- Filtered list updates as the user types.
- Hover and focus on items in the list.
- No results state when the search returns nothing.

**Anti-patterns.**
- Autocomplete that requires exact match. Allow fuzzy or partial matching.
- Autocomplete that shows the same long list every time and only filters on full word match.

**Code-level guidance.**
- Debounce search input (150-300ms) for server-backed queries to avoid hammering the API.
- Highlight the matching substring in the result list to confirm the match logic.

### Date picker

**When to use.** Date entry. Reservations, deadlines, birthdays.

**Required states.**
- Default: input with a calendar icon trigger.
- Open: calendar visible, current selection highlighted, today indicated.
- Hover on dates.
- Focus on the calendar grid: keyboard navigation works (arrow keys, Page Up/Down for months).
- Disabled dates (e.g., past dates for a future reservation): visually disabled, not clickable.
- Error: same red border treatment.

**Anti-patterns.**
- Date pickers without keyboard navigation. Inaccessible.
- Date pickers that force calendar use when the user could just type. Allow direct text input alongside the calendar.
- Date pickers that do not respect locale (DD/MM vs MM/DD).

**Code-level guidance.**
- Support both calendar selection and direct text input.
- Validate the input format and provide a clear error if it does not match.
- Disabled dates have appropriate `aria-disabled` and are skipped in keyboard navigation.

### Time picker

**When to use.** Time entry. Appointments, scheduling.

**Required states.**
- Same as date picker, with a different interface (hour/minute selectors or a clock face).

**Anti-patterns.**
- 24-hour-only pickers in locales that use 12-hour, or vice versa, without configuration.
- Time pickers without typing — forcing wheel scrolling for what could be three keypresses.

**Code-level guidance.**
- Allow direct text input (`14:30` or `2:30 PM`).
- Respect locale for default format.

### Color picker

**When to use.** Color selection. Theme customization, design tool surfaces.

**Required states.**
- Default: a swatch showing the current color with a click affordance.
- Open: picker UI visible (HSV/HSL/RGB sliders, hex input, eyedropper if supported).
- Hover and focus on color swatches inside the picker.

**Anti-patterns.**
- Color pickers without hex input. Designers and developers want to paste a hex value.
- Color pickers that close on every interaction. The user needs to drag and click multiple times.

**Code-level guidance.**
- Support hex input with paste; validate and normalize.
- Show the resulting color in a preview swatch that updates live as the user adjusts.

### File upload

**When to use.** File attachment. Document uploads, profile photos, asset libraries.

**Required states.**
- Default: a button to trigger native file picker, or a drop zone (or both).
- Hover on the drop zone: visual indication that drop is supported.
- Dragging over the drop zone: stronger visual indication.
- Uploading: progress indicator per file.
- Uploaded: thumbnail or filename with dismiss option.
- Error: file rejected (wrong type, too large) with a clear message.

**Anti-patterns.**
- Generic "Choose file" with no indication of what is acceptable. Show file type and size limits.
- File uploads that fail silently if the file is too large.
- Drop zones that do not clearly indicate "drop here." Users do not know to drop.

**Code-level guidance.**
- Use a `<input type="file">` for the picker trigger; the drop zone wires to the same input via JavaScript.
- Validate file type, size, and count before upload; show errors inline.
- For multi-file uploads, show each file's progress separately.

---

## Modals, Sheets, and Drawers

The overlay patterns. Each blocks or interrupts the user differently; choosing the right one is the design call.

### Modal (centered dialog)

**When to use.** A focused interaction that must complete before the user continues. Confirmation, critical decisions, complex forms that need full attention.

**Required behaviors.**
- Backdrop scrim: semi-transparent dark overlay (40-60% black) behind the modal.
- Focus trap: keyboard focus stays inside the modal until dismissed.
- Escape route: Esc key dismisses (non-destructive modals); explicit close button always present; backdrop click dismisses (non-destructive only).
- Scroll lock: the page behind does not scroll while the modal is open.
- Animation: 200-300ms fade-in for the scrim, scale-up for the modal (from 0.95 to 1).

**Anti-patterns.**
- Modals stacked more than two deep. The UX falls apart.
- Modals for non-blocking content. If the user could keep working, it should be a drawer or popover.
- Modals with no close button (relying on Esc only). Touch users cannot press Esc.
- Modals that dismiss on backdrop click during a destructive action. The user might lose work.

**Code-level guidance.**
- Render via a portal at the body root to avoid z-index battles.
- Apply `aria-modal="true"` and `role="dialog"`; the modal's title and description are linked via `aria-labelledby` and `aria-describedby`.
- Set `inert` on the rest of the page while the modal is open (or trap focus via JavaScript).

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

### Drawer (side-anchored panel)

**When to use.** Secondary content or chrome that lives alongside the main view. Filters, settings, navigation on mobile, detail panels.

**Required behaviors.**
- Anchored to one side (left, right, top, bottom). Pick based on the chrome's relationship to the main content.
- Slides in from the anchored side.
- Optional backdrop scrim (use scrim for blocking drawers; omit for non-blocking).
- Dismiss with backdrop click, Esc, or explicit close button.
- Width 320-480px typically; wider for content-heavy drawers, narrower for nav.

**Anti-patterns.**
- Drawers that take more than 50% of the viewport. At that point, use a modal or a full page.
- Drawers without backdrop scrim that nevertheless block the underlying content. Either block or do not — be honest.

**Code-level guidance.**
- Same portal pattern.
- Animation: 250-300ms slide-in with the same cubic-bezier easing.
- Focus management: when blocking, trap focus; when non-blocking, do not trap.

### Dismiss patterns

A consistent dismiss vocabulary across modals, sheets, and drawers:

- **Escape (Esc key).** Always available for non-destructive overlays. Never for destructive ones (user might press by accident).
- **Backdrop click.** Available for non-destructive overlays. Disabled for forms with unsaved changes (prompt for confirmation).
- **Explicit close button (X).** Always present. Even when Esc and backdrop click are available — touch users cannot press Esc, and backdrop click is not always obvious.
- **Drag-to-dismiss.** Mobile sheets and drawers. The drag handle (visible bar) is the affordance.

### Focus trap

The focus must stay inside the overlay while it is open:

- Tab from the last focusable element cycles back to the first.
- Shift+Tab from the first focusable element cycles to the last.
- When the overlay closes, focus returns to the element that opened it.

This is non-negotiable for accessibility. Implementations exist in every modern framework.

---

## Cards

The surface container. Often overused; the right card pattern is the one that earns its frame.

### When to use cards

- The content groups exist independently and need visual separation beyond spacing.
- The elevation (shadow or border) communicates that the content is interactive (clickable card linking to detail).
- The grouped content is heterogeneous (image + text + actions) and would look chaotic without a frame.

### When to ban cards in favor of hairlines

- The content is in a list and the items are homogeneous (same shape, same data type). Hairlines (1px dividers) carry the structure with less visual noise.
- The content needs to feel continuous. Cards interrupt; hairlines connect.
- The design is editorial or content-heavy. Cards box content; editorial wants flow.

### When to ban cards in favor of plain typography

- The content groups are obvious from typography and spacing alone.
- The page is dense and cards add visual debt without communicating new structure.

### Elevation rules

- **No elevation (flat).** Static content cards. Background tint replaces shadow.
- **Light elevation (subtle shadow).** Interactive cards that link or expand. Shadow signals "this thing does something."
- **Heavy elevation (strong shadow).** Modal-like cards that hover above the page. Rare; usually a modal is the right pattern.

### Required states for interactive cards

- Default: card surface with the chosen elevation.
- Hover: slight elevation increase (lift), subtle scale (1.01-1.02) optional.
- Active: scale-down slightly (0.99), shadow decrease.
- Focus: focus ring around the entire card.
- Loading: skeleton inside the card preserves the shape.

### Anti-patterns

- Cards inside cards inside section wrappers. Strip back to one framing move.
- Cards locked to equal heights by flexbox when content varies wildly. Allow variable heights.
- Cards with no internal structure (no padding, no clear header). The frame is empty ceremony.
- Cards as the universal wrapper for everything on the page. Most content does not need a card.

### Code-level guidance

- Card padding: 16-24px internal padding typically. Tighter on dense data; generous on marketing.
- Card radius: matches the rest of the system. Often 8-16px.
- Card border: 1px hairline for flat cards; 0 for elevated cards (the shadow carries the edge).

---

## Navigation

How users move through the product. The right pattern depends on hierarchy depth, surface count, and the platform.

### Top navigation (horizontal nav bar)

**When to use.** Marketing sites. Product UIs with shallow hierarchy. Surfaces where the brand should be prominent.

**Required states.**
- Default: brand on the left (typically), nav items in the center or left, user actions on the right.
- Active state: clearly indicates which page the user is on (underline, fill, color change).
- Hover on items: subtle color or underline change.
- Focus: ring visible.
- Mobile: collapses to a hamburger menu that opens a drawer or full-screen overlay.

**Anti-patterns.**
- Stuffing every link into the top nav. Prioritize 3-7 items.
- Active state that is barely visible. Users need to know where they are.
- No mobile pattern — letting the desktop nav crash into the mobile viewport.

**Code-level guidance.**
- Use `<nav>` semantic element with appropriate `aria-label`.
- Active state via `aria-current="page"`.
- Mobile breakpoint typically 768-1024px; below, switch to the collapsed pattern.

### Bottom navigation (mobile tab bar)

**When to use.** Mobile apps and PWAs. Surfaces where the user needs persistent access to 3-5 top-level destinations.

**Required states.**
- Default: 3-5 tabs at the bottom of the viewport, each with an icon and label.
- Active state: clear visual distinction (color, fill, indicator).
- Hover not applicable (touch).
- Tap feedback: brief visual response on tap.

**Anti-patterns.**
- More than 5 bottom tabs. Beyond 5, the labels shrink and users cannot read them.
- Bottom nav on desktop. Desktop has space for a top or side nav.
- Bottom nav that disappears on scroll. The persistence is the point.

**Code-level guidance.**
- Min height 56-64px for the bar; each tab at least 64px wide.
- Safe area inset on iOS (`padding-bottom: env(safe-area-inset-bottom)`).
- Active state on tap, sustained while the destination is active.

### Side navigation (vertical sidebar)

**When to use.** Product UIs with deep hierarchy. Admin panels. Dashboards. Surfaces with 5+ top-level destinations and nested sections.

**Required states.**
- Default: vertical list of items, optionally grouped into sections.
- Active state: clear visual distinction on the active item.
- Expanded/collapsed state for grouped items.
- Collapsed sidebar (icons only) for users who want more space.
- Mobile: hidden by default, opens via a hamburger trigger.

**Anti-patterns.**
- Side nav with no visual hierarchy between top-level and nested items. Users get lost.
- Side nav that does not remember its collapsed state across sessions. Frustrating.
- Side nav that hides the active item when scrolled. The user needs the orientation.

**Code-level guidance.**
- Use `<nav>` with `<ul>` and `<li>` for semantic structure.
- Persist collapsed/expanded state in localStorage.
- Active state via `aria-current="page"`.

### Breadcrumb

**When to use.** Deep hierarchy where the user benefits from knowing where they are and being able to navigate up. Admin tools, file systems, e-commerce.

**Required states.**
- Default: chain of links separated by a visual delimiter (chevron, slash). The current page is at the end and is not a link.
- Hover on previous segments.
- Focus on links.
- Mobile: often collapsed (show first and last, hide middle behind a "...").

**Anti-patterns.**
- Breadcrumbs that show only the parent (e.g., "Back to Settings"). That is a back link, not a breadcrumb — say so.
- Breadcrumbs that wrap to two lines. Either prune the hierarchy or collapse middle segments.

**Code-level guidance.**
- Use `<nav>` with `aria-label="Breadcrumb"`.
- Use an ordered list (`<ol>`) for the chain.
- The current page is rendered as text, not a link, with `aria-current="page"`.

### Tabs

**When to use.** Switching between related views of the same content. Settings sections. Product detail tabs (description, reviews, specs).

**Required states.**
- Default: horizontal list of tab labels at the top of the panel area.
- Active state: clear distinction (underline, fill, or color).
- Hover on tabs.
- Focus on tabs: keyboard navigation works (arrow keys, Tab to enter panel).
- Disabled tabs: visually distinct, not clickable.

**Anti-patterns.**
- Tabs with more than 5-7 items. Beyond that, use a different pattern.
- Tabs that wrap to two lines. Redesign the IA.
- Tabs that scroll horizontally without overflow affordance.

**Code-level guidance.**
- Use `role="tablist"` on the container, `role="tab"` on each tab, and `role="tabpanel"` on each panel.
- Active tab has `aria-selected="true"`; others have `aria-selected="false"`.
- Keyboard: arrow keys move between tabs; Enter or Space activates; Tab leaves the tablist.

### Pagination

**When to use.** Long lists that cannot be loaded all at once. Search results, transaction histories, archives.

**Required states.**
- Default: previous/next buttons, current page number, optional jump-to-first/last.
- Disabled state on previous (when on first page) and next (when on last page).
- Hover on page numbers.
- Focus on buttons.

**Anti-patterns.**
- Pagination with no current-page indicator. The user does not know where they are.
- Pagination that requires loading the page before showing total count. Users do not know how long the list is.
- Infinite scroll without a way to go back to a specific point. Lost their position; cannot return.

**Code-level guidance.**
- Use `<nav>` with `aria-label="Pagination"`.
- Buttons that are disabled have `disabled` attribute and `aria-disabled="true"`.
- Current page indicated with `aria-current="page"`.

---

## Tables

The data grid pattern. Tables are inherently dense; the design choice is how dense.

### Sortable tables

**Required behaviors.**
- Clickable column headers that sort ascending, descending, or unsorted (cycle).
- Visual indicator on the active sort column (arrow up/down).
- Visual indicator on inactive sortable columns (smaller or muted arrow).
- Keyboard support: Enter on header to sort.

**Anti-patterns.**
- Sortable indicators that only appear on hover. Users do not know which columns are sortable.
- Sorting that does not preserve scroll position.

### Filterable tables

**Required behaviors.**
- Per-column filter UI (search input, dropdown, date range) above or below the column.
- Active filter indicator (highlighted column, filter chip above the table).
- Clear-all-filters affordance.

**Anti-patterns.**
- Filter inputs that are hidden by default behind a "Filters" button on dense tables — adds friction. Make common filters always visible.
- Filters that fire on every keystroke without debouncing. Server hammered.

### Paginated tables

**Required behaviors.**
- Pagination controls at the bottom of the table (sometimes top as well).
- Total count visible.
- Configurable page size.
- Persistent page in URL or state so refresh preserves position.

### Virtualized tables

**When to use.** Very long datasets (thousands of rows). Virtualization renders only the visible rows for performance.

**Required behaviors.**
- Smooth scrolling without visual artifacts.
- Sticky header that stays at the top.
- Sticky columns optional (left or right) for orientation.

**Anti-patterns.**
- Virtualization that breaks selection across pages (selecting a row, scrolling away, scrolling back — selection lost).
- Virtualization without a fallback for screen readers.

### Responsive collapse

**Required behaviors.**
- Below a breakpoint (typically 768px or 1024px), the table either:
  - Collapses to cards (each row becomes a card with the columns as labeled fields).
  - Allows horizontal scroll with sticky first column.
  - Hides non-essential columns.

**Anti-patterns.**
- Tables that overflow horizontally on mobile without any handling. Users have to scroll a tiny window.
- Hiding the most important column on collapse. Choose what to hide carefully.

### General table guidance

- Tabular figures (mono-spaced digits) for numeric columns. Reading numbers stacked together requires alignment.
- Right-align numbers; left-align text. Center for short codes (status, country).
- Row padding 8-12px for dense; 16-20px for comfortable.
- Hairlines between rows; heavier line under the header.
- Hover state on rows when rows are interactive (link to detail); no hover when static.

---

## Forms

How users provide structured input. The form pattern shapes the entire flow.

### Single-column form

**When to use.** Linear flows. Sign-up, sign-in, simple settings. The user works top-to-bottom.

**Required structure.**
- Fields stacked vertically, full-width or comfortably wide (max-width 480-640px).
- Labels above inputs.
- Helper text below inputs (when needed).
- Error text below the helper text or replacing it.
- Submit button at the bottom, left-aligned (or full-width on mobile).

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

### Multi-step wizard

**When to use.** Long forms where the user benefits from chunking. Onboarding, complex configuration, multi-page surveys.

**Required structure.**
- Progress indicator at the top showing steps and current position.
- Each step focuses on a coherent group of fields.
- Back and Next buttons (and Save/Submit on the last step).
- Form state preserved across steps (the user can go back and not lose data).

**Anti-patterns.**
- Wizards with too many steps (10+). Users abandon.
- Wizards without back navigation. Users get stuck and start over.
- Wizards that lose data on back navigation.
- Wizards that do not say how many steps total. Users do not know how committed they are.

### Inline edit

**When to use.** Settings or data where the user edits one field at a time without going to a separate page. Profile fields, list item editing.

**Required behaviors.**
- Click on the field surface to enter edit mode.
- Edit affordance visible (pencil icon, "Edit" label).
- Save and Cancel buttons inline.
- Escape cancels; Enter saves (for single-line fields).
- Visual feedback on save (saved state, brief checkmark).

**Anti-patterns.**
- Inline edit that is not discoverable. The user does not know clicking the field starts editing.
- Inline edit with no Cancel. The user cannot abort.
- Inline edit that saves on blur without confirmation. The user might leave focus accidentally and not realize they saved.

### Autosave

**When to use.** Long-form input (drafts, documents, notes) where the user expects work to persist automatically.

**Required behaviors.**
- Saves at sensible intervals (every few seconds or on blur).
- Visual indicator of save state ("Saved 2 seconds ago," "Saving...", "Failed to save - retry").
- Conflict handling: if the user makes changes while a save is in flight, the latest change wins.

**Anti-patterns.**
- Autosave with no indicator. The user does not trust that their work is saved.
- Autosave that fires too often, hammering the server.
- Autosave that loses data on conflict.

### Form validation

- Validate on blur for most fields (after the user moves on from the field).
- Validate on submit for the whole form.
- Inline error messages — per-field, specific, with the fix.
- Never just "Form contains errors." Always name the field and the action.
- Scroll the first error into view on submit if errors exist.

---

## Toast, Alert, Banner

The notification patterns. Each communicates at a different intensity and persistence.

### Toast

**When to use.** Transient confirmation. Success messages, brief notifications.

**Required behaviors.**
- Appears in a corner of the viewport (typically top-right or bottom-right).
- Auto-dismisses after 4-6 seconds.
- Dismissible by user (X button or swipe).
- Queue up to 3-4 toasts; beyond that, the queue is unreadable.

**Severity variants.**
- Success: green or brand color.
- Info: blue or neutral.
- Warning: yellow or amber.
- Error: red.

**Anti-patterns.**
- Toasts for critical errors. Auto-dismiss is a bug on a critical error.
- Stacking more than 3-4 toasts.
- Toasts with long content. The user cannot read 5 sentences in 4 seconds.
- Toasts as the primary feedback mechanism. They are confirmation, not announcement.

**Code-level guidance.**
- Use `role="status"` for non-critical toasts (announced but not interrupting).
- Use `role="alert"` for critical ones (interrupting screen reader).
- Animation: slide-in from edge, fade-out.

### Alert (inline notification)

**When to use.** A message in the flow of the page. Form errors, status updates, contextual warnings.

**Required behaviors.**
- Lives in the page flow, not floating.
- Severity color indicates urgency.
- Dismissible (X button) when transient; persistent when load-bearing.

**Severity variants.**
- Same color set as toast.

**Anti-patterns.**
- Alerts that take up half the viewport for low-importance information.
- Alerts that cannot be dismissed when the user has acknowledged them.

**Code-level guidance.**
- `role="alert"` for critical; `role="status"` for non-critical.
- Icon at the start of the alert to reinforce severity.

### Banner (top-of-page or app-wide)

**When to use.** System-level messages. Service disruption, upcoming maintenance, terms updates.

**Required behaviors.**
- Spans the full width at the top of the page or app.
- Dismissible when informational; non-dismissible for critical announcements.
- Persists across page navigation when load-bearing.

**Anti-patterns.**
- Banners for marketing. Users learn to ignore them.
- Banners that cover important UI. Place above the chrome, not over it.
- Banners that cannot be dismissed when they are clearly informational.

**Code-level guidance.**
- `role="status"` or `role="alert"` per severity.
- Cookie or localStorage to remember dismissal across sessions.

### Accessibility

All three patterns need:
- Appropriate ARIA role (`status` or `alert`).
- High contrast between text and background.
- Touch-friendly dismiss button (44px minimum).
- Keyboard support for the dismiss button.

---

## Empty States

The pattern for "there is nothing here yet." Often skipped; getting it right turns a dead-end into a beginning.

### When to use

- The user has navigated to a list, table, or grid that has no items.
- A search or filter returns no results.
- A new section or feature has never been used.

### Required structure

- A visual element (illustration, icon, or just well-chosen typography).
- A clear, calm message explaining what is here and why it is empty.
- A clear action the user can take (primary button to create, secondary to learn, or a link to documentation).
- Optionally, a tip or hint about what success looks like in this section.

### Variants

- **Never used.** "You have no projects yet. Create one to get started."
- **Filter returned nothing.** "No results match these filters. Try adjusting them."
- **Cleared.** "Inbox zero. Nice."
- **Error empty.** "We couldn't load this. Retry."

### Anti-patterns

- Generic empty states copied across the product. Each empty state should feel like part of its section.
- Empty states with no action. The user lands on nothing with nothing to do.
- Empty states that are too cute or too jokey. The user wants direction, not entertainment.
- Empty states that look like errors when they are not.
- Lorem ipsum or placeholder names in the empty state copy.

### Code-level guidance

- Centered layout within the available space.
- Max-width 400-500px on the text and the action.
- Icon or illustration that matches the system's visual language.
- The primary action is a real button leading to a real next step.

---

## Loading States

The pattern for "we are getting your data." Every interface has loading states; designing them is the discipline that separates polished from generic.

### Skeleton

**When to use.** Loading data that has a known shape (list, table, card grid). The skeleton mimics the eventual layout.

**Required behaviors.**
- Gray or low-contrast blocks shaped like the eventual content.
- Optional shimmer animation (subtle, 1-2s loop).
- Renders in the same dimensions as the eventual content (no layout shift on load).

**Anti-patterns.**
- Skeletons that do not match the eventual layout. The whole point is to reduce shift; mismatched skeletons make the shift worse.
- Skeletons with overly aggressive shimmer that distracts more than it informs.
- Skeletons on sub-200ms loads. The flash is annoying.

**Code-level guidance.**
- Apply a delay (200-400ms) before showing the skeleton. If the load completes before, no skeleton.
- Use `aria-busy="true"` on the loading container.

### Shimmer

The animated highlight that sweeps across a skeleton. Subtle, slow, monochromatic. Avoid colored or fast shimmers — they distract.

### Progress (linear or radial)

**When to use.** Known-duration tasks. File uploads, multi-step operations, batch processing.

**Required behaviors.**
- Visual indicator that fills as the task progresses.
- Numeric percentage (optional) for transparency.
- Estimated time remaining (optional) for long tasks.

**Anti-patterns.**
- Progress bars that jump or go backwards. Users lose trust.
- Progress bars that hit 99% and sit for the rest of the time. Designers know — avoid this by using a non-linear approach (slower at the end is fine; backward is not).
- Progress for unknown-duration tasks. Use a spinner instead.

**Code-level guidance.**
- Use `<progress>` element when possible.
- Apply `aria-valuenow`, `aria-valuemin`, `aria-valuemax`.

### Spinner

**When to use.** Indeterminate-duration tasks. Initial loads, API calls, anything where the duration is unknown.

**Required behaviors.**
- Animated rotation, smooth.
- Sized appropriately for context (small in a button, larger as a full-page indicator).
- Centered in its container.

**Anti-patterns.**
- Spinners on every interaction, including instant ones. Delay 200-400ms before showing.
- Spinners that are huge for tiny interactions, or tiny for full-page loads.
- Spinners with custom animations that look broken (jerky, slow, fast-flashing).

**Code-level guidance.**
- CSS animation, not JavaScript animation.
- `role="status"` and `aria-label="Loading"` for screen readers.

### Optimistic UI

**When to use.** Actions where the success is highly likely and the latency would otherwise be visible. Liking, favoriting, marking as read.

**Required behaviors.**
- The UI updates immediately as if the action succeeded.
- The actual request goes to the server in the background.
- If the request fails, the UI rolls back and shows an error.

**Anti-patterns.**
- Optimistic UI on actions that fail often. The rollback is jarring.
- Optimistic UI on critical actions (payments, deletions). The user expects confirmation.
- Optimistic UI without rollback. The user thinks they succeeded but did not.

**Code-level guidance.**
- Local state update first, then API call.
- On error, revert state and show inline error.

---

## Error States

The pattern for "something went wrong." Errors are inevitable; design them so the user recovers.

### Inline errors

**When to use.** Form validation. Per-field issues. The error belongs next to the input that caused it.

**Required structure.**
- Red text below the field (or to the side, depending on the form pattern).
- Specific message: "Email must include an @ symbol" beats "Invalid input."
- The action to take: "Email must include an @ symbol — for example, name@example.com."
- The input itself gets a red border.

**Anti-patterns.**
- Vague messages ("Invalid input," "Form contains errors").
- Errors that disappear when the user starts typing again without actually fixing the issue.
- Errors that show on every keystroke (no debounce).
- Errors that block submission without indicating which field is wrong.

**Code-level guidance.**
- Link the error message to the input via `aria-describedby`.
- Set `aria-invalid="true"` on the input.
- Focus the first error on submit.

### Summary errors

**When to use.** When multiple errors exist or when the user needs an overview before fixing. Top-of-form summary listing every error.

**Required structure.**
- A heading ("Please fix these issues:").
- A list of specific errors, each linking to the offending field.
- Click on a list item scrolls to and focuses the field.

**Anti-patterns.**
- Summary errors that duplicate inline errors without adding value. If every error is also inline, the summary is noise.
- Summary errors without links to the fields. The user has to find each one manually.

### Recovery paths

Every error should suggest a recovery:

- "Try again" button when retrying makes sense.
- "Contact support" link when the error is unrecoverable.
- "Refresh" suggestion when the state might be stale.
- "Sign in again" when the session expired.

**Anti-patterns.**
- Errors with no recovery path. The user is stuck.
- Errors that say "An error occurred" with no detail or action.

### Code-level guidance

- Use `role="alert"` for critical errors that interrupt.
- Use `role="status"` for less urgent errors.
- Log the underlying error to the console or a monitoring service for debugging, but show a human message to the user.

---

## State summary reference

Quick reference for the states every pattern needs:

| Pattern | Required States |
|---|---|
| Button | default, hover, active, focus, disabled, loading |
| Input | default, hover, focus, filled, disabled, error |
| Card (interactive) | default, hover, active, focus, loading |
| Modal | open, closed, focused (focus trap active) |
| Tab | default, hover, active (current), focus, disabled |
| Toggle/Switch | off, on, focus, disabled |
| Table row (interactive) | default, hover, focus, selected |
| Toast | entering, visible, dismissing |
| Loading | initial, in-progress, complete |
| Error | inline, summary, with-recovery |

---

## Closing rules

Patterns are tools; the brief decides. The right pattern is the one that:

1. **Matches the task.** A confirmation needs a modal; a status update needs a toast; deep hierarchy needs side nav, not top nav.
2. **Covers all the states.** Every interactive element has 5 states. Missing one is a bug.
3. **Respects accessibility floors.** Keyboard navigation, focus management, ARIA where needed, color contrast, touch targets.
4. **Stays consistent across the product.** Two button styles in the same product is noise; one button style with variants is system.
5. **Defaults to the calmer option.** Loud patterns (heavy shadows, big radii, intense colors) lose their power when used everywhere. Restraint compounds.

The discipline:

1. **Pick the pattern that fits the task, not the task that fits the pattern.**
2. **Implement all required states. Always.**
3. **Use semantic HTML. Use proper ARIA. Test with keyboard.**
4. **One primary per context.**
5. **Be specific in errors. Name the field. Name the fix.**
6. **Restrain. When in doubt, do less.**

Hold these and the components compound. Each pattern teaches the next one. The system gets cleaner as it grows.
