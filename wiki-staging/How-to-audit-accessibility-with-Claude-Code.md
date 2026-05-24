# How to Audit Accessibility with Claude Code

Run a WCAG 2.1 AA accessibility audit on any web surface using the /ux-a11y command in Claude Code. The command checks contrast, keyboard navigation, focus indicators, semantic HTML, screen reader compatibility, motion preferences, dynamic type, and form-error patterns.

## What this page covers

You will run an accessibility audit, read the structured report, apply mechanical fixes in place, and understand which findings need human judgment versus which can be automated. The audit covers WCAG 2.1 AA as the floor and surfaces opportunities for AAA where they matter.

## What WCAG 2.1 AA requires

Plain-language version of the criteria the plugin enforces.

### Perceivable

- **Text alternatives.** Every non-text element (image, icon, chart, video thumbnail) has a text alternative. Decorative images get `alt=""`. Functional images get descriptive alt text. Icon buttons get `aria-label`.
- **Time-based media.** Videos have captions. Audio has transcripts.
- **Adaptable content.** Information and structure preserved when CSS is disabled. Headings in hierarchical order. Lists marked as lists.
- **Distinguishable.** Color is not the only way to convey information. Text contrast is at least 4.5:1. Large text contrast is at least 3:1. Interactive elements contrast at least 3:1 against adjacent colors.

### Operable

- **Keyboard accessible.** Every interactive element is reachable and operable with a keyboard. No keyboard traps (places the user can tab into but not out of).
- **Enough time.** Time-limited interactions can be extended or disabled. Auto-updating content can be paused.
- **No seizures.** Nothing flashes more than three times per second.
- **Navigable.** Skip links bypass repeated content. Page titles describe purpose. Focus order matches reading order. Link purpose is clear from context.
- **Input modalities.** Touch targets are at least 44 by 44 pixels on mobile. Pointer gestures have a single-pointer alternative.

### Understandable

- **Readable.** Language of the page is declared (`lang="en"`). Unusual words and abbreviations are explained on first use.
- **Predictable.** Components behave consistently across the site. Navigation appears in the same place. Focusing an element does not trigger a context change.
- **Input assistance.** Form errors identify the field and describe the problem. Labels and instructions are provided. Error prevention for legal or financial transactions.

### Robust

- **Compatible.** Markup is valid. ARIA roles are used correctly. Status messages are announced to assistive technology.

## What /ux-a11y checks

The plugin's audit covers the WCAG 2.1 AA criteria plus a layer of pragmatic checks that real users hit but the spec underspecifies.

### Automated checks

- **Color contrast.** Every text/background pair tested. Every interactive element against adjacent colors. Both light and dark mode if present.
- **Focus indicators.** Every interactive element has a visible focus state. Focus ring is at least 2 pixels and at least 3:1 contrast against the background.
- **Touch target size.** Buttons, links, form controls — minimum 44 by 44 pixels on viewports under 768px wide.
- **Semantic HTML.** Headings in hierarchy (no skipping h2 to h4). Lists marked as `<ul>` or `<ol>`. Landmarks used (`<nav>`, `<main>`, `<aside>`).
- **Alt text presence.** Every `<img>` has `alt`. Every icon button has `aria-label`. Decorative images use `alt=""` or `role="presentation"`.
- **Form labels.** Every `<input>`, `<select>`, `<textarea>` has an associated `<label>` or `aria-label`.
- **Form errors.** Errors identify the field by name. Errors describe what to do, not just what is wrong.
- **Language declaration.** `<html lang="...">` is present and correct.
- **Page title.** Every page has a unique `<title>` describing its purpose.
- **Skip link.** A "Skip to main content" link is present and reachable as the first focusable element.

### Behavioral checks

- **Keyboard navigation.** The plugin simulates tab order and reports any element reachable by mouse but not by keyboard.
- **Screen reader announcement.** The plugin reads the DOM in screen-reader order and reports whether headings, links, and form controls have meaningful text.
- **Motion preferences.** Every animation is wrapped in `@media (prefers-reduced-motion: reduce)` or equivalent.
- **Dynamic type.** Text scales correctly when the user increases browser zoom to 200 percent. No content cut off, no horizontal scroll triggered.
- **High contrast mode.** UI is readable in Windows High Contrast Mode and macOS Increase Contrast.

### Pragmatic checks the spec underspecifies

- **Focus visible vs focus.** The plugin enforces `:focus-visible` for keyboard-only focus rings, not `:focus` (which fires on mouse click).
- **Disabled controls have explanation.** A disabled button without a tooltip or description fails. The user must know why it is disabled.
- **Loading states have copy.** A spinner alone does not announce loading status. A loading state needs an `aria-live` region with text.
- **Empty states have action.** An empty state with no next step traps users.

## Step 1: run /ux-a11y with a URL or file

The command works against deployed URLs, local files, or directories.

```bash
# Audit a live URL
/ux-a11y https://your-site.com/dashboard

# Audit a local file
/ux-a11y ./resources/views/dashboard.blade.php

# Audit a directory
/ux-a11y ./src/components/

# Audit with a specific WCAG level
/ux-a11y ./dashboard.blade.php --level=AA   # default
/ux-a11y ./dashboard.blade.php --level=AAA  # stricter

# Audit a specific category only
/ux-a11y ./dashboard.blade.php --only=contrast
/ux-a11y ./dashboard.blade.php --only=keyboard
/ux-a11y ./dashboard.blade.php --only=forms
/ux-a11y ./dashboard.blade.php --only=semantic
```

The audit runs in the background. Output streams to the terminal. For URLs, the plugin renders the page in a headless browser to catch dynamic content. For files, it parses the markup and runs static checks plus visual rendering.

## Step 2: read the structured report

The output is severity-ranked. Critical findings block ship. Major findings need fixing before launch. Minor findings are taste-level.

```
UX Accessibility Audit — dashboard.blade.php
=============================================

CRITICAL (3 findings) — Blocks WCAG 2.1 AA
  L47  Text contrast 3.8:1 fails AA minimum 4.5:1.
       Selector: .stat-card__label (color: #888 on background: #fff)
       Recommendation: Darken to #595959 for 4.6:1 ratio.

  L82  Icon button has no accessible name.
       Selector: button.icon-menu (contains <svg> only, no aria-label)
       Recommendation: Add aria-label="Open menu" or visible text.

  L156 Form input has no associated label.
       Selector: input[name="search"] (no <label>, no aria-label)
       Recommendation: Add <label for="search">Search transactions</label>
       or aria-label="Search transactions" on the input.

MAJOR (5 findings) — Should fix before launch
  L23  Heading hierarchy skip — h2 followed directly by h4.
       Selector: section.hero (h2 -> div -> h4)
       Recommendation: Use h3 instead of h4, or restructure content.

  L67  Touch target below 44x44px on mobile viewport.
       Selector: a.footer-link (current size: 36x20px)
       Recommendation: Increase padding to reach 44x44 minimum.

  L134 Focus indicator missing on custom dropdown.
       Selector: .custom-select__trigger
       Recommendation: Add focus-visible ring (2px solid, 3:1 contrast).

  L201 Animation does not respect prefers-reduced-motion.
       Selector: .hero-illustration (transform animation, 2s duration)
       Recommendation: Wrap in @media (prefers-reduced-motion: no-preference)
       or set transition to none in reduced motion.

  L289 Form error does not identify the field.
       Current: "Please fix the errors below."
       Recommendation: "Email is missing the @ symbol. Add it to continue."

MINOR (4 findings) — Taste-level improvements
  L67  Skip-to-main-content link missing.
       Recommendation: Add <a href="#main">Skip to main content</a> as
       the first focusable element.

  L134 Page title is generic ("Dashboard").
       Recommendation: "Treasury Dashboard — Trovata" for specificity
       and screen-reader context.

  L201 Decorative image has alt text describing the image.
       Selector: img.background-pattern (alt="abstract pattern")
       Recommendation: Set alt="" since the image is decorative.

  L312 Color is the only signal for status in pill component.
       Selector: .status-pill (green/red, no icon or text)
       Recommendation: Add an icon (check/x) or text label.

SUMMARY
  WCAG 2.1 AA: 8 violations (3 critical, 5 major)
  Pragmatic:   4 improvements
  Score: 72/100 — needs work before launch
```

The score is informational. Critical findings must reach zero. Major findings must reach zero for production launch. Minor findings can ship with a backlog.

## Step 3: fix the findings with /ux-a11y --fix

The same command with `--fix` applies mechanical fixes in place.

```bash
/ux-a11y ./resources/views/dashboard.blade.php --fix
```

The plugin will:

1. Show each finding and the proposed fix
2. Ask for confirmation on judgment-level decisions (color value choices, copy choices)
3. Apply mechanical fixes automatically:
   - `aria-label` on icon buttons
   - `alt=""` on decorative images
   - `alt="descriptive text"` on functional images (asks for the text)
   - `focus-visible:ring-2` on interactive elements missing focus indicators
   - `<label>` associations on unlabeled form inputs
   - Skip-to-main-content link insertion
   - `lang` attribute on the html element
   - `prefers-reduced-motion` guards on animations
4. Generate a diff summary at the end

For tighter control, fix one category at a time.

```bash
/ux-a11y ./dashboard.blade.php --fix --only=contrast
/ux-a11y ./dashboard.blade.php --fix --only=labels
/ux-a11y ./dashboard.blade.php --fix --only=focus
/ux-a11y ./dashboard.blade.php --fix --only=keyboard
/ux-a11y ./dashboard.blade.php --fix --only=motion
```

The `--fix` flag does not apply changes that require human judgment — color choices when the current value fails contrast (the plugin suggests but does not pick), copy choices for form errors (the plugin suggests but does not write), or restructuring decisions for heading hierarchy.

## The accessibility checklist

Reference checklist of every category the audit covers.

### Contrast and color

- All text meets 4.5:1 contrast against its background
- Large text (18pt+ or 14pt+ bold) meets 3:1
- Interactive elements meet 3:1 against adjacent colors
- UI components (borders of inputs, focus rings) meet 3:1
- Color is not the only signal for status, errors, or required fields
- Both light and dark modes pass independently

### Keyboard navigation

- Every interactive element reachable via Tab
- Tab order matches visual order
- No keyboard traps (Esc closes modals, drawer, dropdowns)
- Skip-to-main-content link is the first focusable element
- Custom interactive components (combobox, tabs, accordion) follow ARIA Authoring Practices
- Arrow keys work where users expect them (within menus, tabs, radio groups)

### Focus indicators

- Every interactive element has a visible focus state
- Focus ring is at least 2 pixels
- Focus ring contrasts at least 3:1 against the background
- `:focus-visible` used for keyboard-only focus, not `:focus` (which triggers on mouse click)
- Focus ring is not removed via `outline: none` without a replacement

### Semantic HTML

- One `<h1>` per page
- Headings in hierarchical order (no skipping levels)
- `<nav>`, `<main>`, `<aside>`, `<footer>` landmarks used
- Lists marked as `<ul>` or `<ol>`
- Buttons use `<button>`, not `<div onclick>`
- Links use `<a href>`, not `<button onclick="location.href=">`
- Tables use proper `<th>`, `<scope>`, and `<caption>` where applicable

### Labels and ARIA

- Every form input has an associated `<label>` or `aria-label`
- Icon buttons have `aria-label`
- Decorative images have `alt=""` or `role="presentation"`
- Functional images have descriptive `alt` text
- ARIA roles are used correctly (no `role="button"` on actual `<button>`)
- ARIA properties match the component pattern (e.g., `aria-expanded` on disclosure, `aria-selected` on tabs)
- `aria-live` regions used for status announcements

### Form errors and validation

- Errors identify the field by name
- Errors describe what to do, not just what is wrong
- Errors are programmatically associated with their field (`aria-describedby`)
- Errors are announced to screen readers via `aria-live="assertive"` or `role="alert"`
- Inline validation does not block submission until the user has interacted with the field

### Touch targets

- Minimum 44 by 44 pixels on viewports under 768px wide
- Adjacent touch targets have at least 8 pixels of space between them
- Tap-and-hold gestures have a single-tap alternative

### Motion and animation

- Every animation respects `prefers-reduced-motion: reduce`
- Reduced motion fallback is meaningful (instant transition, not just shorter)
- No autoplaying video or animation longer than 5 seconds without controls
- No flashing more than 3 times per second
- Parallax and scroll-triggered animations have a reduced-motion fallback

### Dynamic type and zoom

- Text scales correctly at 200 percent browser zoom
- No content cut off at 200 percent zoom
- No horizontal scroll triggered at 200 percent zoom on a 1280px viewport
- Layout reflows correctly at small viewports (320px minimum)

### Page structure

- `<html lang="...">` is present and correct
- Page has a unique `<title>` describing its purpose
- Skip-to-main-content link is present
- Page does not refresh or redirect without user action
- Focus moves to relevant content after page transitions (e.g., to the new page's `<h1>`)

### Screen reader compatibility

- Headings announce in correct order
- Form labels are announced when the input receives focus
- Status messages (success, error, loading) are announced via `aria-live`
- Modals trap focus inside while open, return focus to the trigger on close
- Decorative content is hidden from screen readers (`aria-hidden="true"`)

## Common a11y bugs and how the plugin catches them

The patterns the audit catches most often in real codebases.

### Bug 1: icon-only buttons with no accessible name

```html
<!-- Wrong -->
<button class="icon-menu"><svg>...</svg></button>

<!-- Right -->
<button class="icon-menu" aria-label="Open menu"><svg aria-hidden="true">...</svg></button>
```

The screen reader reads the second version as "Open menu, button." The first version reads as just "button" with no context.

### Bug 2: form inputs with placeholder-as-label

```html
<!-- Wrong -->
<input type="text" placeholder="Email address" />

<!-- Right -->
<label for="email">Email address</label>
<input type="email" id="email" />
```

Placeholders disappear when the user starts typing. They are not labels. The wrong version fails screen reader users and users who clear the field by accident.

### Bug 3: `outline: none` without a replacement

```css
/* Wrong */
button:focus { outline: none; }

/* Right */
button:focus { outline: none; }
button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
```

Removing the default outline without providing a custom focus indicator strands keyboard users — they cannot see where the focus is.

### Bug 4: color-only status signals

```html
<!-- Wrong -->
<span class="pill" style="background: red;">Failed</span>
<span class="pill" style="background: green;">Passed</span>

<!-- Right -->
<span class="pill pill--danger">
  <svg aria-hidden="true">...</svg> Failed
</span>
<span class="pill pill--success">
  <svg aria-hidden="true">...</svg> Passed
</span>
```

The right version uses both a color and an icon. Color-blind users see the icon. Sighted users see both.

### Bug 5: divs pretending to be buttons

```html
<!-- Wrong -->
<div class="button" onclick="submit()">Submit</div>

<!-- Right -->
<button type="button" onclick="submit()">Submit</button>
```

The right version is keyboard-accessible, announced as a button by screen readers, and supports Space and Enter activation. The wrong version requires explicit ARIA roles and tabindex management to be accessible, and even then is fragile.

### Bug 6: heading hierarchy skipping levels

```html
<!-- Wrong -->
<h1>Treasury Dashboard</h1>
<section>
  <h4>Recent transactions</h4>
</section>

<!-- Right -->
<h1>Treasury Dashboard</h1>
<section>
  <h2>Recent transactions</h2>
</section>
```

Screen reader users navigate by heading level. Skipping levels disorients them. Heading levels reflect document structure, not styling.

### Bug 7: keyboard traps in custom dropdowns

```js
// Wrong — focus stays inside the dropdown forever
document.addEventListener("keydown", (e) => {
  if (e.key === "Tab" && dropdown.contains(e.target)) {
    e.preventDefault();
    // keeps focus in dropdown
  }
});

// Right — Escape closes the dropdown and returns focus to the trigger
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && isOpen) {
    close();
    triggerButton.focus();
  }
});
```

The right version follows the ARIA Authoring Practices pattern for menus.

### Bug 8: animations that respect no preferences

```css
/* Wrong */
.hero-image {
  animation: float 4s infinite ease-in-out;
}

/* Right */
@media (prefers-reduced-motion: no-preference) {
  .hero-image {
    animation: float 4s infinite ease-in-out;
  }
}
```

The right version respects the user's system preference. Users who set "Reduce motion" in their OS or browser see the static image. Users who did not see the animation.

### Bug 9: form errors that do not identify the field

```html
<!-- Wrong -->
<div class="error">Form contains errors. Please correct and resubmit.</div>

<!-- Right -->
<div role="alert">
  Email is missing the @ symbol. Add it to continue.
</div>
```

The right version tells the user exactly what is wrong and how to fix it. The wrong version is functionally hostile — the user has to find the error themselves, with no announcement to screen readers.

### Bug 10: dynamic content with no announcement

```js
// Wrong — change happens silently
function addItem(item) {
  list.appendChild(item);
}

// Right — change is announced
function addItem(item) {
  list.appendChild(item);
  statusRegion.textContent = `${item.name} added to cart.`;
}
```

With `<div role="status" id="statusRegion" aria-live="polite">` in the markup, the right version announces additions to screen reader users without interrupting them.

## Performance and accessibility intersection

Two performance concerns are also accessibility concerns. The plugin checks both.

### Reduced motion

Users who enable reduced motion include people with vestibular disorders, ADHD, and anyone using an underpowered device that drops frames on heavy animation. Respecting `prefers-reduced-motion: reduce` is not optional — it is both an accessibility requirement and a performance benefit on weak hardware.

The fallback is rarely "no animation at all." It is usually "instant state change, no movement." A modal still appears; it just appears without sliding in.

```css
.modal {
  transform: translateY(0);
  transition: transform 300ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .modal {
    transition: none;
  }
}
```

### Dynamic type

Users with low vision often increase browser zoom to 200 or 400 percent. A site that breaks at 200 percent zoom fails these users.

The audit checks zoom behavior. The fix is usually one of:

- Use relative units (rem, em, percentage) instead of fixed pixels
- Use container queries instead of viewport queries
- Allow long content to wrap rather than truncate

```css
/* Wrong — breaks at 200% zoom */
.card { width: 320px; padding: 16px; }

/* Right — scales with zoom */
.card { width: 20rem; padding: 1rem; }
```

## Real example

A B2B treasury dashboard, audited before launch.

### Before audit

The dashboard has:
- A custom dropdown for account selection
- A data table with sortable columns
- Form inputs for filter dates
- Status pills (red/green/yellow) for each transaction
- A modal for transaction details
- Animations on the variance summary cards

Visual review says it looks good. Lighthouse score is 92/100 for accessibility.

### Audit findings

```
UX Accessibility Audit — TreasuryDashboard.tsx
===============================================

CRITICAL (4)
  Dropdown trigger has no aria-expanded or aria-haspopup.
  Sortable column headers have no aria-sort.
  Status pills use color only — no icon or text indicator.
  Modal does not trap focus while open.

MAJOR (6)
  Date input has placeholder-as-label.
  Table cells lack scope attributes.
  Variance card animation does not respect reduced-motion.
  Close button on modal has no aria-label.
  Form errors say "Invalid input" without naming field.
  Page title is "Dashboard" with no context.

MINOR (3)
  Skip-to-main-content link missing.
  Decorative pattern image has alt="background pattern".
  Loading spinner has no aria-live announcement.
```

Lighthouse missed most of these. Automated tools catch contrast and missing alt — they miss interactive behavior, dynamic announcements, and custom component patterns.

### Fixes applied

After `/ux-a11y --fix`:

```
APPLIED (mechanical)
  + aria-label="Close modal" on close buttons
  + aria-hidden="true" on decorative SVGs and pattern
  + alt="" on decorative pattern image
  + Skip-to-main-content link added to layout
  + lang="en" on root html element
  + Page title updated to "Treasury Dashboard — Trovata"
  + Date input wrapped in <label>
  + Table cells given scope="col" / scope="row"
  + prefers-reduced-motion guard on variance animation
  + aria-live="polite" region added for loading state
  + role="alert" on form error containers

PENDING (judgment-level)
  - Status pill icons: needs design decision on which icons to use
  - Form error copy: needs per-error rewrite (field name + fix instruction)
  - Custom dropdown: needs full ARIA Authoring Practices implementation
  - Modal focus trap: needs implementation review (suggested utility)
```

### Result after fixes

```
WCAG 2.1 AA: 0 violations
Pragmatic: 0 improvements pending
Score: 98/100
```

The dashboard ships. Screen reader users can navigate. Keyboard users can complete every task. Reduced-motion users see no jarring animation. Color-blind users see status via icon, not just color. Users at 200 percent zoom can still read every cell of the data table.

Two percentage points remain because the design uses one slightly off-brand color combination in a low-priority surface. Acceptable for launch, on the backlog for the next iteration.

## When the audit cannot help

The plugin catches WCAG 2.1 AA violations. It does not catch every accessibility problem.

Things the plugin cannot detect:

- **Whether the copy makes sense.** A perfectly-labeled form with confusing instructions is still inaccessible to users with cognitive disabilities. Run `/ux-copy` for that.
- **Whether the workflow itself is accessible.** A six-step form that times out after 90 seconds may pass WCAG but fail real users with motor impairments who cannot complete it in time. Watch real users.
- **Whether assistive technology actually works.** The plugin tests markup. It cannot test what NVDA, JAWS, or VoiceOver actually say. Test with real screen readers on real flows.
- **Whether the experience is dignified.** WCAG is the floor. A site that meets WCAG but treats disabled users as an afterthought ("Click here for accessibility mode") fails on dignity. That requires human judgment.

The audit is the floor. Real accessibility work continues past it.

## Linked next steps

- The polish pass catches design issues that intersect with accessibility. See [How to fix AI-generated UI](How-to-fix-AI-generated-UI).
- The copy on the page is part of the accessibility surface. See [How to fix microcopy that sounds like AI](How-to-fix-microcopy-that-sounds-like-AI).
- New surfaces should be designed accessible from the start. See [How to build a SaaS landing page with Claude Code](How-to-build-a-SaaS-landing-page-with-Claude-Code).
- A real design system bakes accessibility into the foundations. See [How to generate a design system with Claude Code](How-to-generate-a-design-system-with-Claude-Code).

---

**See also**: [How to fix AI-generated UI](How-to-fix-AI-generated-UI) | [How to fix microcopy that sounds like AI](How-to-fix-microcopy-that-sounds-like-AI) | [How to generate a design system with Claude Code](How-to-generate-a-design-system-with-Claude-Code)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
