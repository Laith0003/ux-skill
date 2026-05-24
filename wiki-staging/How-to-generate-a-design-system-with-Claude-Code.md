# How to Generate a Design System with Claude Code

Generate a complete starter design system inside Claude Code — tokens, foundations, components, dark-mode pairings — from a brand brief or an existing site. The /ux-system command dispatches a design-system-architect sub-agent that builds the full token JSON, 5-10 foundation docs, and 6-8 component contracts.

## What this page covers

You will run the design-system generation command, answer the system-level discovery questions, produce a working starter system with tokens and foundations and components, and integrate the output into your stack. The output is real code you ship, not a Figma file.

## What a design system actually is

The phrase is overloaded. Strip it down to four layers and the work becomes tractable.

### Layer 1: Tokens

The atomic units. Color values, spacing values, type sizes, border radii, shadow definitions, animation durations. Tokens are not "blue." Tokens are `color.text.primary`, `color.surface.elevated`, `space.4`, `radius.md`.

Tokens come in two flavors:

- **Raw tokens** — the actual values. `--color-neutral-900: oklch(0.15 0.01 250)`.
- **Semantic tokens** — what the value means. `--color-text-primary: var(--color-neutral-900)`.

Components only ever reference semantic tokens. Raw tokens are private to the system.

### Layer 2: Foundations

The rules for using tokens. Type scale ratios. Color contrast minimums. Spacing rhythm (4-point or 8-point grid). Layout breakpoints. Motion principles. Accessibility floors. Foundations are docs — markdown files that say "buttons are always at least 44 pixels tall on mobile" and "body text is never under 16 pixels."

### Layer 3: Components

The reusable parts. Button. Card. Input. Modal. Each component has a contract — props, variants, states, accessibility behaviors, supported sizes. A component is defined by the contract, not by a specific framework implementation.

### Layer 4: Theming

Dark mode. Brand variants. Tenant theming. Density modes. Each is a token override layer that maps semantic tokens to different raw values without touching components.

A real design system has all four. A starter design system from the plugin includes all four on day one.

## When to use /ux-system

Two situations make the command worth running.

### Situation 1: no design system exists

The codebase has scattered Tailwind classes, hardcoded hex values, inconsistent spacing, and ad-hoc components. Adding a fifth feature surfaces the cost — visual drift, accessibility regressions, slow handoffs. Time to generate a system.

### Situation 2: an existing system is generic

The codebase has a "design system" that is really just the Tailwind defaults with a custom logo. Slate gray. Inter font. Sky blue accent. Looks like every Linear clone. Time to rebuild with brand-specific tokens and real foundations.

### When not to use it

- The project already has a mature, well-documented system. Do not regenerate. Use `/ux-polish` to fix inconsistencies inside the existing system.
- The project is one-off marketing site. Skip the system and use `/ux-design` directly. Systems pay off over multiple surfaces.

## Step 1: run /ux-system

The command takes an optional brief.

```bash
# Generate from a brand brief
/ux-system design system for a B2B treasury management SaaS — Apple-clean monochrome, one saturated accent, serif display face for headlines

# Generate from an existing site
/ux-system rebuild the system from https://your-current-site.com

# Generate from existing tokens
/ux-system extend the system in ./resources/css/tokens.css with dark mode and density variants
```

The design-system-architect sub-agent picks up the brief and runs discovery.

## Step 2: answer the system-level discovery questions

These differ from the page-level discovery in `/ux-design`. The system questions are about durability — choices you cannot change easily once components depend on them.

### 1. What is the brand's visual register?

Pick one. The choice anchors every downstream decision.

- **Apple-clean** — high contrast, generous white space, one saturated accent, sans-serif body, sometimes serif display
- **Editorial** — typographic hierarchy is the primary structure, large type sizes, narrow content widths, serifs allowed
- **Industrial** — dense, monospace-heavy, structural lines visible, almost no decoration
- **Brutalist** — raw, asymmetric, intentionally rough, single-color palette
- **Maximalist** — dense color, decorative borders, layered patterns, deliberate visual complexity
- **Minimalist** — almost no color, no shadows, no decoration, pure structure
- **Warm/hospitality** — cream backgrounds, warm neutrals, gentle curves, serif display, generous rounding
- **Tech/saturated** — dark default, neon accents, monospace numerics, sharp corners

### 2. What is the color story?

A real palette has three layers.

- **Neutrals** — the workhorse. Background, surface, border, text. Five to nine steps from lightest to darkest.
- **Accent** — the brand. Used sparingly. One saturated color, with five or six steps for hover, active, focus, disabled.
- **Semantic** — success, warning, danger, info. Four colors, each with three or four steps.

For Apple-clean monochrome, neutrals do almost all the work. Accent appears on CTAs and selected states only.

### 3. What is the type story?

Three faces, with clear roles.

- **Display** — used for hero headlines and section titles. Often serif (Fraunces, DM Serif Display, Editorial New, IBM Plex Serif) or a high-personality sans (Söhne, Calibre, GT America).
- **Body** — used for paragraphs, labels, UI text. Sans-serif. Variable weight. Self-hosted (Inter, Geist, Manrope, Söhne).
- **Mono** — used for code, numeric tables, technical data. JetBrains Mono, Berkeley Mono, Geist Mono.

The display face is the one that makes the system feel branded. Choose with intent.

### 4. What is the spacing rhythm?

Pick a base unit. Every spacing value is a multiple.

- **4-point grid** — finer control, used in dense UIs. Base spacing values: 4, 8, 12, 16, 20, 24, 32, 48, 64, 96.
- **8-point grid** — looser rhythm, used in marketing surfaces and content-heavy interfaces. Values: 8, 16, 24, 32, 48, 64, 96, 128.

Pick one. Use it everywhere. The exception is type-related spacing, which uses ems relative to the type size.

### 5. What is the type scale ratio?

Type sizes follow a ratio. Pick one.

- **1.125 (Major Second)** — tight, dense UI
- **1.2 (Minor Third)** — balanced, common default
- **1.25 (Major Third)** — generous, editorial
- **1.333 (Perfect Fourth)** — large jumps, hero-heavy
- **1.5 (Perfect Fifth)** — dramatic, used in editorial or maximalist registers

Anchored to a base size (usually 16px), the ratio generates the full scale. A 1.25 ratio from 16px gives you 12, 14, 16, 20, 25, 31, 39, 49, 61, 76, 95.

### 6. What is the radius vocabulary?

Border radii are a brand signal.

- **Sharp** — 0 radius, industrial register
- **Tight** — 2-4px, technical or dense UI
- **Standard** — 6-8px, default for most SaaS
- **Generous** — 12-16px, warm or hospitality
- **Pill** — fully rounded buttons and badges, modern SaaS default

Most systems pick one base radius (8px) and one for pills. Some add a small (4px) for input fields and a large (16px) for cards.

### 7. What is the elevation model?

Two approaches.

- **Shadow-based** — `shadow-sm`, `shadow-md`, `shadow-lg` define elevation. Standard SaaS pattern.
- **Border-based** — no shadows at all, elevation expressed with a 1px border and background contrast. Increasingly common in editorial and brutalist registers.

Pick one. Mixing both reads as inconsistent.

### 8. What are the motion principles?

Three decisions.

- **Duration tokens** — short (150ms), medium (300ms), long (500ms). Most interactions use short.
- **Easing tokens** — standard ease, ease-out (for entering elements), ease-in (for exiting elements), spring (for playful interactions).
- **Reduced motion** — every animation must respect `prefers-reduced-motion: reduce`. The system defines the fallback (usually instant transition with no movement).

### 9. What accessibility floor?

WCAG 2.1 AA is the baseline. Some systems push further.

- **AA minimum** — 4.5:1 contrast for text, 3:1 for large text, 3:1 for interactive elements
- **AAA target** — 7:1 contrast for text, 4.5:1 for large text. Required for some industries (healthcare, government, finance).

The accessibility floor affects the color palette directly. If neutral-700 fails AA on white text, it cannot be `color.text.muted`.

### 10. What is the dark mode strategy?

Three approaches.

- **No dark mode** — single theme. Valid for marketing-only surfaces.
- **Token-overridden dark mode** — same semantic tokens, different raw values. Components do not know which theme is active.
- **Theme-aware components** — components inspect the current theme. More flexible, more complexity.

Most starter systems use token-overridden dark mode. Components reference `color.surface.primary` which resolves to white in light mode and a deep neutral in dark mode.

## Step 3: the design-system-architect produces the output

After discovery, the sub-agent generates a complete starter system. The output structure:

```
design-system/
  tokens/
    colors.css           # raw + semantic color tokens, light + dark
    typography.css       # font faces, sizes, weights, line heights
    spacing.css          # spacing scale
    radius.css           # border radius scale
    shadow.css           # elevation scale (or border alternative)
    motion.css           # durations, easings
  foundations/
    accessibility.md     # contrast floors, focus indicators, motion preferences
    color-usage.md       # when to use which semantic token
    typography-rules.md  # type scale, line height ratios, content widths
    spacing-rhythm.md    # how to read the spacing scale
    elevation.md         # when to use shadow vs border
    motion-principles.md # duration choices, easing choices, reduced-motion
    iconography.md       # icon set, stroke width, sizing
    voice.md             # tone, microcopy rules
  components/
    button.tsx           # primary, secondary, ghost, link variants
    input.tsx            # text, email, number, search variants
    textarea.tsx
    select.tsx
    checkbox.tsx
    radio.tsx
    switch.tsx
    card.tsx             # standard, elevated, bordered variants
    modal.tsx
    drawer.tsx
    toast.tsx
    badge.tsx
    avatar.tsx
    tabs.tsx
    table.tsx
    skeleton.tsx
  index.css              # imports all tokens
  README.md              # how to use the system
```

The exact component set depends on the discovery answers — if you said "dashboard-heavy," the system includes a `data-table.tsx` and `chart-container.tsx`. If you said "marketing-only," the system skips form components and adds `pricing-card.tsx` and `testimonial.tsx`.

### Example tokens output

For an Apple-clean monochrome system with a deep teal accent:

```css
/* design-system/tokens/colors.css */

:root {
  /* Raw neutrals — OKLCH for perceptual uniformity */
  --color-neutral-50:  oklch(0.99 0.002 250);
  --color-neutral-100: oklch(0.97 0.003 250);
  --color-neutral-200: oklch(0.93 0.004 250);
  --color-neutral-300: oklch(0.86 0.005 250);
  --color-neutral-400: oklch(0.68 0.006 250);
  --color-neutral-500: oklch(0.52 0.007 250);
  --color-neutral-600: oklch(0.40 0.008 250);
  --color-neutral-700: oklch(0.30 0.009 250);
  --color-neutral-800: oklch(0.20 0.010 250);
  --color-neutral-900: oklch(0.13 0.011 250);

  /* Raw accent — deep teal */
  --color-accent-100: oklch(0.95 0.04 200);
  --color-accent-300: oklch(0.78 0.08 200);
  --color-accent-500: oklch(0.55 0.12 200);
  --color-accent-700: oklch(0.40 0.10 200);
  --color-accent-900: oklch(0.25 0.08 200);

  /* Raw semantic — success, warning, danger */
  --color-success-500: oklch(0.55 0.14 145);
  --color-warning-500: oklch(0.75 0.14 80);
  --color-danger-500:  oklch(0.55 0.20 25);

  /* Semantic tokens — what components reference */
  --color-bg-primary:    var(--color-neutral-50);
  --color-bg-elevated:   #ffffff;
  --color-bg-muted:      var(--color-neutral-100);
  --color-text-primary:  var(--color-neutral-900);
  --color-text-muted:    var(--color-neutral-600);
  --color-text-on-accent: #ffffff;
  --color-border:        var(--color-neutral-200);
  --color-border-strong: var(--color-neutral-300);
  --color-accent:        var(--color-accent-700);
  --color-accent-hover:  var(--color-accent-900);
  --color-focus-ring:    var(--color-accent-500);
}

[data-theme="dark"] {
  --color-bg-primary:    var(--color-neutral-900);
  --color-bg-elevated:   var(--color-neutral-800);
  --color-bg-muted:      var(--color-neutral-800);
  --color-text-primary:  var(--color-neutral-50);
  --color-text-muted:    var(--color-neutral-400);
  --color-border:        var(--color-neutral-700);
  --color-border-strong: var(--color-neutral-600);
  --color-accent:        var(--color-accent-300);
  --color-accent-hover:  var(--color-accent-100);
}
```

### Example component output

A button using semantic tokens:

```tsx
// design-system/components/button.tsx
import { ButtonHTMLAttributes, forwardRef } from "react";
import { cva, type VariantProps } from "class-variance-authority";

const button = cva(
  // Base styles using semantic tokens only
  "inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-focus-ring)] focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
  {
    variants: {
      variant: {
        primary: "bg-[var(--color-accent)] text-[var(--color-text-on-accent)] hover:bg-[var(--color-accent-hover)]",
        secondary: "bg-[var(--color-bg-elevated)] text-[var(--color-text-primary)] border border-[var(--color-border-strong)] hover:bg-[var(--color-bg-muted)]",
        ghost: "text-[var(--color-text-primary)] hover:bg-[var(--color-bg-muted)]",
      },
      size: {
        sm: "h-9 px-3 text-sm rounded-md",
        md: "h-11 px-4 text-base rounded-lg",
        lg: "h-12 px-6 text-lg rounded-lg",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof button> {}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant, size, className, ...props }, ref) => (
    <button
      ref={ref}
      className={button({ variant, size, className })}
      {...props}
    />
  )
);

Button.displayName = "Button";
```

Notice what is and is not present.

Present:
- Only semantic tokens (`--color-accent`, `--color-text-primary`). Never raw values inside the component.
- Focus indicator (`focus-visible:ring-2`) with offset, using the focus-ring token.
- Disabled state styling.
- Three variants, three sizes — common minimum.

Not present:
- No hardcoded colors.
- No inline styles.
- No magic numbers for padding or height.

## Step 4: integrate into your stack

The output is portable. The integration depends on what you ship.

### Tailwind 4 integration

Tailwind 4 reads CSS variables natively. Drop the tokens into your CSS entry and reference them as Tailwind classes.

```css
/* app/globals.css */
@import "tailwindcss";
@import "../design-system/tokens/colors.css";
@import "../design-system/tokens/typography.css";
@import "../design-system/tokens/spacing.css";

/* Tailwind 4 picks up CSS variables automatically */
```

Use them as utility classes: `bg-(--color-accent)`, `text-(--color-text-primary)`.

### Tailwind 3 integration

Tailwind 3 needs the tokens declared in `tailwind.config.js`. The plugin generates the config patch.

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        accent: "var(--color-accent)",
        "accent-hover": "var(--color-accent-hover)",
        "bg-primary": "var(--color-bg-primary)",
        "bg-elevated": "var(--color-bg-elevated)",
        "text-primary": "var(--color-text-primary)",
        "text-muted": "var(--color-text-muted)",
        border: "var(--color-border)",
      },
    },
  },
};
```

Use them: `bg-accent`, `text-text-muted`, `border-border`.

### CSS variables only (no Tailwind)

If you are on plain CSS or Sass, the tokens drop in directly. Reference them in your stylesheets.

```css
.button {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
}

.button:hover {
  background: var(--color-accent-hover);
}
```

### Style Dictionary export

For multi-platform consumption (web + iOS + Android), the plugin can export tokens as a Style Dictionary source.

```bash
/ux-system export --format=style-dictionary
```

Produces `tokens.json` that Style Dictionary transforms into platform-specific outputs (CSS, Swift, Kotlin, JSON, Figma Tokens).

## Token discipline rules

The system survives only if these rules hold.

### Rule 1: components reference semantic tokens, never raw values

Wrong:
```css
.button { background: #0d9488; }
.button { background: oklch(0.55 0.12 200); }
.button { background: var(--color-accent-500); }  /* raw token */
```

Right:
```css
.button { background: var(--color-accent); }  /* semantic token */
```

### Rule 2: maximum one accent color

The system has one brand accent. Buttons use it. Active states use it. Focus rings use it. Anything else competing with the accent dilutes it.

If a second color is needed (e.g., for a chart legend), it comes from the semantic palette (`--color-success`, `--color-warning`), never from a second brand color.

### Rule 3: type scale follows a single ratio

Pick a ratio (1.25 for most). All type sizes derive from it. Adding a one-off "20px because 18 felt too small" breaks the scale.

If a real edge case needs an off-scale size, document it explicitly in `foundations/typography-rules.md`.

### Rule 4: spacing follows a single base

Pick 4-point or 8-point. Stay on it. Padding values of 13px, 17px, 22px are signals the system is being violated.

### Rule 5: dark mode is an override layer, not a parallel system

Components do not check `theme === "dark"`. They reference semantic tokens that resolve differently in dark mode. The component code is identical.

### Rule 6: accessibility minimums are non-negotiable

A semantic token that fails WCAG AA contrast cannot ship. The system enforces this at token-definition time, not at component time.

### Rule 7: every component has every state

A button without a hover, focus, active, disabled, and loading state is half-built. Same for every interactive component. The system defines all states upfront.

## Dark mode pairings

Each semantic token has a light value and a dark value. Get the pairing wrong and dark mode looks like inverted-light, not dark.

### Background pairing

Light mode `--color-bg-primary` is near-white (oklch 0.99). Dark mode `--color-bg-primary` is near-black but never pure black (oklch 0.13). Pure black creates harsh contrast with text and gives users eye strain in dark mode.

### Surface elevation

Light mode elevation is achieved with shadows or subtle background lift. Dark mode elevation is achieved by making elevated surfaces *lighter*, not darker. A modal in dark mode sits at oklch 0.20 while the page background is oklch 0.13. Same direction as light mode — elevated is brighter.

### Text contrast

Light mode text is dark on light. Dark mode text is light on dark, but never pure white. Pure white on dark backgrounds creates a "bloom" effect that strains eyes. Use oklch 0.95 instead.

### Accent in dark mode

Brand accents often need brightening in dark mode. A deep teal at oklch 0.40 reads correctly on light backgrounds but disappears on dark. The dark mode override shifts it to oklch 0.65 or higher.

### Borders in dark mode

Borders that worked in light mode (subtle neutral-200) often disappear in dark mode. Dark mode borders need to be lifted from the background — usually 10-15 lightness points up from the surface they sit on.

The plugin handles these pairings automatically. You verify visually.

## Updating the system over time

The first generation is the starter system. Real systems grow.

### Adding a component

```bash
/ux-system add component=combobox
```

The sub-agent generates the new component following the existing system's discipline — same token usage, same accessibility patterns, same state coverage.

### Adding a theme variant

```bash
/ux-system add theme=high-contrast
```

Produces a third theme alongside light and dark. Same semantic tokens, different raw values mapped to extreme contrast (text at oklch 0.05 on backgrounds at oklch 0.99).

### Adding a density mode

```bash
/ux-system add density=compact
```

Adds a `[data-density="compact"]` override that reduces spacing scale by 25 percent and component heights by 4-8 pixels.

### Refactoring an existing component

```bash
/ux-system refactor component=button
```

Re-runs the component through the system's rules. Catches drift — hardcoded values, missing states, accessibility gaps.

## Real example: a system generated from one brief

The brief: "Design system for a B2B treasury management SaaS — Apple-clean monochrome, deep teal accent, serif display face for headlines, 8-point spacing grid, dark mode required."

After running `/ux-system`, the output is the full starter system. The full file tree is in Step 3. Key decisions the sub-agent made automatically based on the brief:

- **Display face**: Fraunces variable. Serif. Tightened tracking on large sizes. Loosened tracking on small sizes.
- **Body face**: Inter variable. Self-hosted. Weight range 400-700.
- **Mono face**: JetBrains Mono variable. Used in numeric tables and code blocks.
- **Type scale ratio**: 1.25. Generates a 12-size scale from 12px to 96px.
- **Spacing**: 8-point grid. Eight named values from `space-1` (4px, exception for tight UI) through `space-32` (128px).
- **Radius**: 8px base, 4px on input fields, 16px on cards, 9999px on pills.
- **Elevation**: shadow-based. Three levels — `shadow-sm`, `shadow-md`, `shadow-lg`. Subtle on light mode, near-invisible in dark mode (replaced with a 1px border).
- **Motion**: 150ms standard, 300ms for modals and drawers, all wrapped in `prefers-reduced-motion` guards.
- **Accent**: deep teal at oklch(0.40 0.10 200) in light, brightened to oklch(0.65 0.12 200) in dark.
- **Accessibility**: AA minimum. All text/background pairings tested. Focus indicators on every interactive element. Skip-to-content link in the layout component.

Components generated:

- Button (primary, secondary, ghost, link)
- Input (text, email, number, search)
- Textarea, Select, Checkbox, Radio, Switch
- Card (standard, elevated, bordered)
- Modal, Drawer, Toast
- Badge, Avatar, Tabs, Table
- Skeleton, EmptyState, ErrorState
- DataTable (specific to dashboards)
- ChartContainer (specific to dashboards)

Foundations generated:

- `accessibility.md` — WCAG 2.1 AA floor, focus indicator rules, motion preferences, keyboard navigation contract
- `color-usage.md` — semantic token reference, when to use which token
- `typography-rules.md` — type scale, line height ratios, content width recommendations
- `spacing-rhythm.md` — 8-point grid, named values, when to use each
- `elevation.md` — shadow vs border decision rules
- `motion-principles.md` — duration choices, easing choices, reduced-motion fallback
- `iconography.md` — Lucide icons, 1.75px stroke, sizing scale
- `voice.md` — tone, microcopy rules pulled from the brief

The system ships as a real package. Components are importable. Tokens are referenced via CSS variables. Dark mode works on day one. Accessibility floors are documented and enforced.

The team uses the system for the next year. New surfaces inherit the discipline. AI slop does not come back in because the tokens prevent it.

## Linked next steps

- The system gives you the foundation. The landing page comes next. See [How to build a SaaS landing page with Claude Code](How-to-build-a-SaaS-landing-page-with-Claude-Code).
- If your existing surfaces still look like AI output, run the polish pass. See [How to fix AI-generated UI](How-to-fix-AI-generated-UI).
- Foundations include accessibility. Verify the system meets WCAG. See [How to audit accessibility with Claude Code](How-to-audit-accessibility-with-Claude-Code).
- The voice foundation needs reinforcement at the microcopy layer. See [How to fix microcopy that sounds like AI](How-to-fix-microcopy-that-sounds-like-AI).

---

**See also**: [How to build a SaaS landing page with Claude Code](How-to-build-a-SaaS-landing-page-with-Claude-Code) | [How to fix AI-generated UI](How-to-fix-AI-generated-UI) | [How to audit accessibility with Claude Code](How-to-audit-accessibility-with-Claude-Code)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
