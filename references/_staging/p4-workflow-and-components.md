# Design Workflow + Components

The end-to-end working method for translating ideas, references, and existing UIs into shippable interfaces. Each section is a self-contained playbook. Read top to bottom for a new project; jump to a section when the situation calls for it.

---

## Visual translation (image → code)

The job is not to "be inspired by" a reference. The job is to translate it faithfully into working frontend, then resolve the gaps the reference leaves behind. Drift kills more redesigns than ambition.

### The mandatory order

For any visually important task, the order is:

1. Visual reference is produced or sourced first.
2. The reference is deeply analyzed as a specification.
3. Implementation begins only after analysis is complete.

If image generation is available and the request is visual ("a beautiful hero", "a premium landing", "a creative website"), generate the reference yourself before writing code. Do not start with freeform coding and try to discover the design in the IDE. The reference is the source of truth; the code is the translation layer.

Direct-code-first is acceptable only when the task is bug-fix, structural, or the user has already handed over a precise spec.

### What to extract, in order

Run analysis as a checklist, not a vibe-read. For each visible region of the reference, surface:

1. **Layout structure.** Grid columns, alignment logic, section ordering, asymmetry, overlap, container max-widths, edge bleed, gutter rhythm.
2. **Typography scale.** Display size, body size, label size, line count per block, line-height feel, tracking, serif vs sans, display vs body contrast, weight steps used, alignment behavior.
3. **Color palette.** Background, surface, primary text, secondary text, accent, border, shadow tint, image grade. Extract hex values where readable.
4. **Spacing rhythm.** Headline-to-subheadline gap, text-to-CTA gap, card-to-card gap, section top/bottom padding, side gutters, card padding, image-to-text distance, navbar internal spacing.
5. **Component inventory.** Buttons (primary/secondary, fill/outline, radius, padding, icon use), cards (border, fill, shadow, radius), badges, pills, dividers, inputs, navbar treatment, footer treatment.
6. **Image system.** Aspect ratios, framing, repeated proportions, crop logic, grade.
7. **Motion mood (implied).** Calm vs energetic, scrubbing vs popping, parallax-leaning vs static. Even if motion is not visible, the composition often implies it.

If any of the above is ambiguous, do not invent. Either regenerate the reference for that section as a fresh standalone image, or generate an extra detail/extraction image focused on that region. Cropping out a tiny zone of a larger composition destroys spacing, proportion, and type-scale accuracy. Generate fresh.

### Handling ambiguity (low-fi vs high-fi sources)

The fidelity of the reference governs how much you invent.

- **Photograph or polished mockup.** Treat as a hard spec. Match layout, type scale, color, spacing within the limits of the medium. Invent only what is genuinely missing (hover states, focus rings, empty states, error states).
- **High-fi screenshot.** Treat as truth. Pixel-match where reasonable; preserve the type ramp; preserve the palette; preserve the spacing language.
- **Sketch or wireframe.** The skeleton is binding; the surface is yours. Hold structure, hierarchy, content density. Choose typography, color, and motion to serve the implied product, not your default taste.
- **Mood image or photo reference.** Atmosphere is binding; structure is yours. Extract palette, texture, mood, and translate into UI-shaped components.
- **Mixed reference set.** Pick one image as the structural anchor and treat the rest as palette/atmosphere supporting evidence. Do not average across them. Averaging produces mush.

For missing states (loading, empty, error, hover, focus), invent only after preserving everything else. The new state must inherit the reference's component family, radius logic, spacing rhythm, and mood. Do not let a missing state become an excuse to introduce a foreign visual language.

### Stack recommendations per reference type

- **Marketing site / landing / hero-driven brand page.** Static framework or SSR with utility-first CSS for fast iteration. Plain HTML + Tailwind or vanilla CSS modules. Heavy components rarely needed; image quality and type discipline matter more than the framework.
- **Product UI / dashboard / data-dense app.** Component library with strong primitives (Button, Modal, Form, Table, Card, Navbar) plus accessibility-first foundations. HeroUI on Tailwind v4 is a strong default; alternatives include Radix-based stacks or Aria-foundation libraries. See the HeroUI section below.
- **Editorial / portfolio / creative agency.** Vanilla CSS modules or utility-first with custom typography pipeline. Motion library only when it earns its weight. Heavy component frameworks fight editorial layouts more than they help.
- **Internal tool / admin.** Component library, conventions over creativity, dense data primitives. Optimize for "boring and obvious."
- **PWA / Blade + Alpine + HTMX style.** Stay in that stack. Do not introduce React for a single feature. Build with the project's primitives.

### Common false reads

These patterns trick analysts into producing wrong implementations:

- **Reading the sky for the system.** A reference's atmosphere is real; its system is what you extract by counting things. Count columns. Count steps in the type scale. Count radius values. Atmosphere without count is vibes-only and produces drift.
- **Confusing decoration for structure.** A grain overlay or a noise texture is not the design system. Strip the surface treatment, see the bones, then add the texture back as a final layer.
- **Conflating display and body.** Display type is loud and lies about the scale. Find the body and the labels; that is where the system lives.
- **Hero clean-up bias.** When a hero looks crowded in the reference, the temptation is to "clean it up." Don't. The crowd is the design. Either reduce the words in the headline or regenerate the reference cleaner — do not silently drop elements during translation.
- **Centering everything because some things are centered.** Asymmetry in the reference is intentional. Preserve it.
- **Replacing distinctive components with generic equivalents.** A "card" in the reference might be a one-off layered frame, not a re-usable card primitive. Read the actual structure before reaching for `<Card>`.
- **Mistaking pseudo-system labels for real UI.** Decorative micro-text ("00 orchestration layer", "system marker 03") often appears in moodier references. It is rarely real UI and almost never adds value in the build. Reduce or remove.

### Pitfalls (translation-stage failures)

- Compressing too many sections into one unreadable analysis pass. If the reference is multi-section, treat each section as its own analysis unit, with its own optional detail pass.
- Skipping deep analysis and going straight to code because the reference "looks easy." Easy references are the ones that get translated into generic AI defaults.
- Inventing details before regenerating the reference. Generate one more clean image of the unclear region first.
- Substituting "good defaults" for the reference's specific choices. The defaults are exactly what the reference was built to escape.
- Letting the implementation drift section-by-section so that section 1 looks like the reference and section 6 looks like a different website.

### The translation discipline

When implementing from a reference, follow it. Preserve layout logic, spacing rhythm, section order, text-image balance, typography mood, component style. The goal is not "inspired by" — the goal is "visually faithful, translated into real frontend." Do not "improve" the reference by replacing it with a generic coded layout. Improve it by executing it well.

---

## Redesigning existing projects

A redesign is not a rewrite. The job is to upgrade what is there, keep the lights on, and ship in slices that the team can absorb. Scope discipline is the difference between a redesign that ships and a redesign that stalls.

### Scope without creep

Before opening any file, answer four questions:

1. **What surface is in scope?** Marketing site, signed-in app, both, or a single page? Name it. The redesign covers exactly that and nothing else.
2. **What is the metric of success?** "Looks better" is not a metric. Choose one or two observable outcomes: trial signups, time-to-task, accessibility audit pass rate, CSS bundle size, page weight, perceived performance on a real device.
3. **What is explicitly out of scope?** Information architecture, content strategy, naming, copy rewrites, framework migrations — name each one as out unless it is explicitly in.
4. **What is the ship pattern?** One big-bang launch, parallel pages with a toggle, dark-launch behind a flag, or rolling per-route. Pick before you start.

Anything that surfaces during the work and does not serve the named scope goes on a follow-up list. Do not "while I'm here" your way through someone else's adjacent feature.

### Audit the existing UI first

Before deciding what to change, decide what is load-bearing. Walk the codebase and produce four lists.

- **Works.** Components and patterns that are doing their job. Touch them only when they conflict with the new direction. Even then, prefer to bend the new direction to fit, not the other way around.
- **Load-bearing equity.** Visual elements that are recognizable, trademarked-in-spirit, or carry user trust. The logo, the primary brand color, a signature curve, the typeface family if it has equity, the welcome microcopy that everyone has memorized. These can evolve but not vanish.
- **Stale.** Components that were good when they shipped and are now dated. These are the redesign's real targets.
- **Deprecated.** Components nobody loves, nobody asked for, and that exist only because of historical accident. Mark for removal; do not redesign what should be deleted.

Run the audit checklist against the codebase:

- Browser-default fonts or Inter everywhere — replace with a font that has character (Geist, Outfit, Cabinet Grotesk, Satoshi, or a distinctive serif like Fraunces).
- Headlines lacking presence — increase display size, tighten letter-spacing, reduce line-height; headlines should feel intentional.
- Body text wider than 65 characters — clamp paragraph width.
- Only 400/700 in the font weight set — introduce 500 and 600 for subtle hierarchy.
- Numbers in proportional figures in a data UI — switch to tabular figures.
- Pure black backgrounds — replace with off-black, dark charcoal, or a tinted dark.
- Oversaturated accents — drop saturation below 80%; desaturate so they blend with neutrals.
- More than one accent — pick one. Remove the rest.
- Mixed warm and cool grays — pick one gray family, tint consistently.
- Purple/blue "AI gradient" fingerprint — replace with neutral bases and one considered accent.
- Generic black box-shadow — tint shadows to match the background hue.
- Flat sections with no depth — add subtle noise, ambient gradient, or a low-opacity background image.
- Everything centered and symmetrical — break symmetry with offset margins, mixed aspect ratios, left-aligned headers over centered content.
- Three equal feature columns — replace with a 2-column zig-zag, asymmetric grid, masonry, or horizontal scroll.
- `100vh` on full-screen sections — switch to `min-height: 100dvh` to fix the iOS Safari viewport jump.
- Cards locked to equal heights by flexbox — allow variable heights or use masonry when content varies.
- Uniform radius on everything — vary: tighter on inner elements, softer on containers.
- Missing hover, active, focus states — add them; transitions 200-300ms; visible focus rings are required, not optional.
- Generic loading spinners — replace with skeleton loaders that match the layout shape.
- No empty states or error states — design composed empty states; inline error messages with the field and the fix; never `window.alert()`.
- Dead anchor links (`#`) — link to real destinations or visually disable.
- "John Doe", "Acme Corp", round numbers (50%, $100.00) — use diverse realistic names, contextual brand names, organic numbers (47.2%, $99.00).
- AI copywriting clichés ("Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer") — write plain, specific language.
- Exclamation marks in success messages, "Oops!" errors — be confident, direct.
- Lorem Ipsum, identical avatars, identical blog dates — fill with real-shaped placeholder content.
- Title Case On Every Header — switch to sentence case.
- Div soup — semantic HTML (`<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`).
- Missing alt text, missing meta tags, arbitrary z-index 9999 — clean up.
- No skip-to-content link — add one.
- No 404 — design a helpful, branded page.

The audit is the redesign's prioritization tool. Fix in this order: font swap, color cleanup, interaction states, layout and spacing, component replacements, missing states, typography scale polish.

### Preserving brand equity while modernizing

Brand equity lives in two places: marks (logo, brand color, type personality) and rituals (the way the product greets a user, the way it confirms a save, the way it apologizes). The modernization changes the surface around those marks and rituals; it does not delete them.

Concrete moves:

- Keep the logo. Replace its container, not its form.
- Keep the brand color. Reduce saturation, tighten its usage rules, give it more breathing room.
- Keep the type family if it carries equity. Refresh the scale, weights, and tracking — do not replace the family unless it is genuinely a problem (e.g., licensing, accessibility, or it never had equity to begin with).
- Keep the voice. Modernize tone where the current voice is shouty, exclamation-heavy, or condescending — but the personality stays.
- Keep the moments. A signature animation on save, a particular empty-state illustration style, a specific welcome flow — modernize the execution, preserve the moment.

If you cannot decide whether something is equity or just legacy, ask: would a returning user notice if it disappeared? If yes, it is equity. If no, it is legacy.

### Migration strategy

Pick one of these per surface; do not mix without intent.

1. **Big-bang.** Cut over the entire surface in one release. Reserved for small surfaces, internal tools, or when the existing UI is so broken that gradual is worse. Requires a tight blast radius and a rollback path.
2. **Parallel pages.** Ship the redesigned page at a sibling URL (`/v2/...`, `/new/...`) and link both. Let users opt in. Useful for marketing surfaces. Decommission the old page once metrics confirm the new one wins.
3. **Feature-flagged rollout.** Same templates, same routes, gated by a flag. Start at 1% to dogfood, 10% for early signal, 50% for confidence, 100% to commit. The flag is removable once the rollout settles.
4. **Dark launch.** Ship the new design rendered but not visible (e.g., behind a query param the team uses). Validate in production with real data before exposing to users. Useful when the redesign touches load-bearing flows.
5. **Per-route rolling.** Migrate one route at a time. The site looks inconsistent during the rollout; budget for visible "in transition" weeks. Works best when routes are independent (marketing pages, settings pages, standalone tools).

Whichever you pick, keep the old code in the tree until the new is proven. Cleanup happens after the redesign lands, not during.

### When to refactor vs rewrite vs replace

- **Refactor.** The existing code is roughly sound; the visual treatment is the problem. Keep the structure, swap tokens, restyle components, add missing states. This is the default and the right move for 80% of redesigns.
- **Rewrite.** The existing code is fighting the new design (wrong primitives, wrong stack, wrong layering). Rewrite the component or the page in place; keep the route and the URL stable.
- **Replace.** The existing surface is so far from the new direction that rewriting it costs more than rebuilding. Reserved for legacy surfaces with low usage or surfaces that the redesign explicitly retires.

If you cannot tell which mode applies, refactor first. The cost of refactor-then-rewrite is low; the cost of rewrite-when-refactor-would-have-worked is high.

### Rules of conduct during a redesign

- Work with the existing tech stack. Do not migrate frameworks under cover of a redesign.
- Check the project's dependency file before importing anything new.
- Do not break existing functionality. Test after every visible change.
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites.
- If a behavior changes, document the behavioral change separately from the visual one. Reviewers should be able to see "we restyled the button" and "we changed when the button is enabled" independently.

---

## Design taste development

Taste is not a vibe. It is the accumulated muscle for noticing what is wrong before the user does, and the discipline to remove it. The principles below describe how high-taste output is produced and how to develop the eye that produces it.

### The three principles

1. **Constraint.** A design system is a set of agreed limits. Limits make decisions cheap and consistency automatic. The taste move is not "more options" but "fewer, sharper choices."
2. **Restraint.** When in doubt, do less. Remove the badge. Drop the third accent color. Cut the headline by half. Restraint creates the breathing room that lets the remaining decisions matter.
3. **Intentionality.** Every element exists for a reason that you can name in one sentence. If you cannot, it is decoration; remove it.

These three are mutually reinforcing. Constraint enables restraint. Restraint forces intentionality. Intentionality validates the constraints.

### Common taste failures (and what they look like)

- **Over-decoration.** Pills inside cards inside section wrappers inside gradient borders. Every layer is fighting for attention. Strip back to one framing move; reduce the rest to typography and spacing.
- **Inconsistency.** Two card styles that disagree on radius. Three button heights. Two slightly different blues. Pick the canonical version and propagate.
- **Scale mismatch.** A massive hero headline next to tiny meek body copy with no mid-step between them. Or buttons too small for their labels, icons too large for their containers. Audit the type ramp and component sizes against a 4px or 8px grid.
- **Hierarchy drift.** The page used to read top-to-bottom; new additions have broken the reading order. Re-rank everything by importance and adjust size, weight, and position to match.
- **Density mismatch.** A dashboard page that is airy in section 1 and crammed in section 2. Sections should breathe together; if one feels crowded relative to its neighbors, it is not designed yet.
- **Color noise.** Three accent colors, all near-equal in weight. Pick one accent; demote the others to neutral or remove them.
- **Default-icon syndrome.** Every icon from Lucide or Feather, every concept rendered with the most obvious metaphor (rocket for launch, shield for security). Swap for Phosphor or Heroicons; replace clichés (bolt for fast, fingerprint for security, spark for AI, vault for storage).
- **Centered everything.** When alignment is centered by default, the page reads as a stack of unrelated elements. Use left-alignment with intent; reserve centering for genuinely standalone moments.
- **Container prison.** Every section is a rounded box inside a rounded box inside a section wrapper. Boxes should exist only when elevation or grouping communicates hierarchy. Otherwise, alignment and spacing carry the structure.
- **Generic accent gradient.** Default purple-blue, default top-left-to-bottom-right. Replace with a single considered color, or break the gradient with noise, mesh, or radial.
- **Type chaos.** Five fonts on one page, three weights of the same font in arbitrary roles. Reduce to one or two families with a clear role per weight.

### Developing taste (the operating system)

- **See more, save less.** Look at thousands of interfaces. Save dozens. Keep the saves curated; a bloated swipe file is a swipe file you never reread.
- **Name what you see.** When something feels good, do not stop at "nice." Name the moves: "the type scale has four steps and uses weight more than size for hierarchy," "the accent appears only on CTAs and links, never on chrome," "the cards have no border, only background tint." Naming converts admiration into vocabulary.
- **Audit your own work mercilessly.** Print a screenshot, walk away, come back. The taste failures are obvious to a fresh eye. They are also obvious to the user.
- **Build the same thing in three styles.** A pricing page that is brutalist-minimal, editorial-magazine, and luxury-refined. The exercise teaches you which moves belong to which style and which are universal.
- **Read criticism, not just praise.** Studios that publish post-mortems and design critiques will teach you more than feeds full of dribbles.

### Validating taste decisions across a team

Taste decisions break down on teams when they become opinion contests. The fix is to make them concrete and falsifiable.

- **Show, don't tell.** Render the choice in three variations side by side. The right answer is usually visible. If it is not, the differences are too small to matter; pick one and move on.
- **Use a memorable-thing forcing question.** Before a decision, agree on the one thing the product should be memorable for. Every taste call gets graded against that one thing. Things that serve it stay; things that do not, go.
- **Decide once.** Once a decision is made, write it into the design system. Re-litigating wastes the team's time. New evidence (user research, accessibility findings, performance data) reopens the decision; new opinions do not.
- **Default to the more restrained option.** When two choices are roughly tied and the team is split, pick the quieter one. Restraint compounds; loudness does not.
- **Identify the taste-owner.** One person has final say on visual decisions for a given surface. The team brings recommendations, the owner decides, the team commits. Design by committee produces averages.

### The role of demo-driven iteration

Talk is cheap. Show the thing.

- **First demo is rough on purpose.** The first version exists to surface what is wrong, not to be right. The team's job at first-demo is to find friction, not to validate.
- **Tighten in three rounds, not thirty.** Most surfaces converge after three rounds of demo-feedback-rebuild. If the surface is not converging, the brief is wrong, not the work.
- **Demo the worst version too.** Showing the ugliest variant alongside the polished one makes the team understand why the polished one is polished. It also gives the team license to reject the obviously-bad without thinking it is a viable path.
- **Demos beat documents.** A demo of the design system applied to a real screen beats a swatch page of hex codes. The demo proves coherence; the swatches prove only that you can pick colors.

The taste move is to demo earlier and oftener than feels comfortable, then to delete the variants that lost.

---

## HeroUI v3 component system (Tailwind v4 + React Aria foundation)

HeroUI v3 is a React component library built on Tailwind CSS v4 and React Aria Components. It provides accessible primitives that work out of the box, with theming and customization wired through CSS variables. Use it when you need a tested, accessible component layer under a custom visual system.

### Critical: v3 is not v2

The provider, styling, and component API all changed between v2 and v3. Do not apply v2 patterns.

- **Provider.** v2 required `<HeroUIProvider>`. v3 needs no provider.
- **Animations.** v2 used `framer-motion`. v3 ships CSS-based animations; no extra dependency.
- **Component API.** v2 used flat props (`<Card title="x" />`). v3 uses compound components (`<Card><Card.Header><Card.Title>x</Card.Title></Card.Header></Card>`).
- **Styling.** v2 used Tailwind v3 plus `@heroui/theme`. v3 requires Tailwind v4 plus `@heroui/styles`.
- **Packages.** v2 pulled `@heroui/system` and `@heroui/theme`. v3 pulls `@heroui/react` and `@heroui/styles`.

If your context includes a `HeroUIProvider` or a `framer-motion` import, you are on v2. Migrate or use a different stack. Tailwind v3 will not work with v3 — v4 is mandatory.

### Installation

Install the runtime and the styles together:

```bash
npm i @heroui/styles @heroui/react tailwind-variants
```

For a Next.js App Router setup, add Tailwind v4 and the PostCSS plugin:

```bash
npm i @heroui/styles @heroui/react tailwind-variants tailwindcss @tailwindcss/postcss postcss
```

Then wire the global stylesheet (`app/globals.css`):

```css
@import "tailwindcss";
@import "@heroui/styles";
```

Import order matters: Tailwind first, HeroUI styles after. Reverse it and the cascade breaks.

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

### Component primitives (typical surface)

The library exposes the common product primitives. Compose them with the compound pattern.

- **Button.** Variants: primary, secondary, tertiary, danger, ghost, outline. Sizes and shapes are theme-driven. Use `onPress` instead of `onClick` for proper accessibility handling.
- **Card.** Compound parts include `Card.Header`, `Card.Title`, `Card.Description`, `Card.Content`, `Card.Footer`. Cards exist when elevation communicates hierarchy — otherwise prefer typography and spacing.
- **Modal / Dialog.** Modal shell with header, body, footer slots. Built on React Aria's focus management; keyboard and screen-reader support is built in.
- **Form primitives.** TextField, NumberField, Checkbox, Radio, Select, Switch, DatePicker, FileTrigger. Labels are explicit components; helper text and error messages compose alongside.
- **Table.** Compound with `Table.Header`, `Table.Body`, `Table.Row`, `Table.Cell`. Sortable headers, selectable rows, multi-select supported via Aria.
- **Navbar.** Compound nav with brand slot, items, end slot, and a mobile menu. Mobile collapse is built in.
- **Tabs.** Tab list, panels, keyboard navigation.
- **Tooltip / Popover.** Positioning via Aria; focus trap on popover when interactive.
- **Toast / Notification.** Triggered via a hook; queue and dismissal are built in.
- **Avatar, Badge, Chip, Divider, Skeleton, Progress, Spinner.** Visual primitives for typical product surfaces.
- **Listbox, Menu, Combobox.** Selection patterns built on Aria with keyboard support.

Always fetch the component's documentation before implementing — the anatomy, prop tables, and examples are the contract. Compound subcomponents (`Card.Header`, `Table.Row`) are not optional flair; flattening them to props will not work.

### Theming with oklch variables

HeroUI v3 uses CSS variables in the `oklch` color space. The naming convention is:

- A variable without a suffix is the background/fill color: `--accent`, `--background`, `--surface`.
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

To customize, override the variables in your global stylesheet after the HeroUI styles import. Do not edit HeroUI's stylesheet directly; you will lose your changes on upgrade.

### Customization (do not ship the default look)

The default HeroUI palette and shapes are deliberately neutral. Shipping them unmodified produces a generic look. To make a product feel like itself, change the following before launch:

1. **Accent color.** Override `--accent` with a hue that fits the brand. Keep saturation below 80%; `oklch` lets you tune lightness and chroma independently.
2. **Radii.** The default radius scale is generic. Decide whether the product is sharp (radius 4-6), soft (8-12), or pillowed (16-24); pick a scale and apply it consistently.
3. **Shadows.** Default shadows are neutral. Tint them to the background hue. A faintly blue background wants a faintly blue shadow, not pure black at low opacity.
4. **Typography.** The library does not impose a typeface; you must. Wire `@font-face` for a real type family. Avoid Inter and Roboto unless the product specifically needs them.
5. **Spacing scale.** Tailwind's defaults are sensible but not signature. Set a base unit (4px or 8px) and confirm the scale matches the design system's density.
6. **Surface colors.** Off-white instead of pure white, off-black instead of pure black. Pure values feel sterile; tinted neutrals feel designed.

If you ship a HeroUI app with default tokens, the user will recognize it as a HeroUI app. That is the convergence trap. Customize before launch.

### Component-specific gotchas and patterns

- **Use `onPress`, not `onClick`.** `onPress` is the Aria-friendly handler that works for mouse, touch, keyboard, and assistive tech. `onClick` will work but skips the abstractions that make the components accessible.
- **Compound, not flat.** Resist the temptation to wrap subcomponents into a single "smart" component with all the props. The compound pattern is what makes the library composable; collapsing it produces leaky abstractions that fight the framework.
- **Semantic variants, not raw colors.** Use `primary`, `secondary`, `tertiary`, `danger`, `ghost`, `outline`. These adapt to themes and accessibility constraints. Hardcoding `bg-blue-500` defeats the system.
- **One primary per context.** A page has one primary action. The rest are secondary, tertiary, or ghost. If you find yourself wanting two primary buttons in the same view, the design is wrong.
- **`tertiary` is for dismissive actions.** Cancel, skip, dismiss — not for "another nice button." Reserve it.
- **Tailwind v4 syntax differs from v3.** Some plugin patterns, the `@layer` ordering, and config-as-CSS instead of `tailwind.config.js` are v4 specifics. If a v3-era snippet pasted in does not work, that is why.
- **Forms.** Compose with `<Form>` for built-in submit handling, validation, and accessibility. Label above input, helper text optional, error text below. Do not invent floating labels.
- **Tables.** For dense data, use tabular figures in the body cells and tight row padding. The library does not enforce this — you set it in your typography layer.
- **Modal stacking.** The library handles focus trap correctly. Do not stack modals more than two deep; the UX falls apart.

### When to use HeroUI vs alternatives

- **Use HeroUI when** you are building a React product UI on Tailwind v4, you need accessibility for free, and you want to focus on visual customization rather than primitive engineering. It is a strong default for dashboards, settings panels, admin tools, and product surfaces.
- **Use Radix-based stacks (Radix + tailwind-variants, or shadcn/ui)** when you want more granular control over the primitives' DOM and you are willing to assemble more yourself. Radix gives you the behavior; you ship the visuals.
- **Use Aria primitives directly** when you need a single specialized component (e.g., a combobox) and do not want a full library footprint.
- **Use Material UI or Chakra** when the project already uses one of them, when the team is comfortable with the conventions, and the design language is compatible.
- **Skip a component library entirely** when the surface is editorial or marketing — heavy component libraries fight editorial layouts. Vanilla CSS or utility-first without a component layer is often faster and cleaner.
- **Do not use HeroUI** if you cannot move to Tailwind v4, if the project is on a non-React stack, or if the team has settled on a different library.

The library is a tool; the brief decides. Pick the library that matches the surface, not the surface that matches the library.

---

## Design consultation mode

A design consultation is a conversation that produces a decision, not a workshop that produces a deck. The consultant shows up with a point of view, listens for the constraints, proposes a coherent system, explains why it works, and adjusts based on the stakeholder's response. The output is a written direction the team can ship against.

### Posture

Consultant, not form-wizard. You do not present menus and wait for picks. You listen, think, propose a complete system, defend the moves, and absorb pushback. The stakeholder's job is to react; your job is to commit.

Opinionated, not dogmatic. Recommend with reasons. Defend with evidence. Update when the evidence changes.

### Discovery questions

Cover these in one well-structured opening conversation. Do not fragment into ten small questions when one structured question gathers the same data.

1. **What is the product?** What it does, who uses it, what space it occupies, what category it lives in.
2. **Who is it for?** The persona, the expertise level, the context of use (desktop, mobile, in a hurry, leisurely, professional, casual).
3. **What is the project type?** Web app, dashboard, marketing site, editorial site, internal tool, mobile app. The type governs many design defaults.
4. **What brand exists already?** Logo, palette, type, voice, prior touchpoints. Is there equity to preserve, or is this a clean slate?
5. **What are the constraints?** Stack, accessibility requirements, performance budgets, timeline, team capacity, regulatory limits.
6. **What does success look like?** Trial signups, time-to-task, comprehension, conversion, accessibility audit pass. Define the metric so the design serves it.
7. **The memorable thing.** What is the one thing a first-time user should remember after seeing this product? One sentence. Could be a feeling, a visual, a claim, or a posture. Every subsequent decision serves this.

For the rest of the conversation, the memorable thing is the tiebreaker.

### Surfacing assumptions early

Pre-fill what you can infer from the codebase, the brief, and any artifacts in hand. Then confirm: "From what I see, this is X for Y in Z space. Sound right?" Confirming an inference is fast; correcting one is faster than surfacing it in the build.

Look for hidden assumptions:

- Is the audience really who the brief says it is, or are there secondary audiences that will see this first?
- Is the constraint really binding, or is it a habit ("we always use Material UI" — but is that actually required)?
- Is the brand equity real, or is it inherited from a previous era and not actually loved?
- Is the success metric the right one, or is it a proxy for something the team has not named?

Name assumptions in the proposal. Stakeholders will either confirm or correct, and either outcome is useful.

### Proposing a coherent system

Propose everything at once. Do not feed decisions in one at a time. A system is coherent or it is not; coherence cannot be evaluated piece by piece.

A proposal covers:

- **Aesthetic direction.** One name (Brutally Minimal, Maximalist, Retro-Futuristic, Luxury-Refined, Playful, Editorial, Brutalist, Industrial, Organic). One sentence of rationale.
- **Decoration level.** Minimal, intentional, expressive. Rationale.
- **Layout approach.** Grid-disciplined, creative-editorial, or hybrid. Rationale.
- **Color approach.** Restrained (one accent + neutrals), balanced (primary + secondary), or expressive. Proposed palette with hex values.
- **Typography.** Display, body, and (if applicable) mono. Specific font names, not categories. Rationale per choice.
- **Spacing scale.** Base unit (4 or 8), density (compact, comfortable, spacious).
- **Motion approach.** Minimal-functional, intentional, or expressive. Rationale.

Then explain why the system is coherent: "These choices reinforce each other because the brutalist aesthetic wants the editorial layout, the editorial layout wants the serif/sans pairing, the pairing wants the restrained color, and restrained color wants intentional motion."

Then present the system as **safe choices + risks**. Safe choices keep the product literate in its category — the things users expect. Risks are the deliberate departures from convention, the moves where the product gets its own face. Always propose at least two risks, each with the rationale and the cost.

The stakeholder can accept, adjust, or ask for wilder risks. Do not present as "what do you want?" — present as "this is what I recommend. Push back where you disagree."

### Driving toward concrete decisions

Endless debate is the death of a consultation. Drive to decisions with these moves:

- **Make the choice visual.** When the stakeholder cannot pick between two fonts, render both in their actual product context. The right answer is usually obvious once both are on screen.
- **Tie every choice to the memorable thing.** "If we go with the playful palette, the memorable thing becomes 'fun.' If we go with the restrained palette, the memorable thing becomes 'serious software.' Which is correct for this product?"
- **Time-box drill-downs.** Pick a section to debate (typography, palette, aesthetic). Resolve it. Move on. Do not loop back unless new evidence emerges.
- **Default to the more restrained option.** When the stakeholder is genuinely torn, recommend the quieter choice. Restraint compounds.
- **Validate coherence after every override.** When the stakeholder swaps one section, check whether the rest still holds together. Flag mismatches gently: "Brutalist aesthetic with expressive motion is unusual. Want me to adjust motion to fit, or keep the contrast?"
- **Accept the final call.** If the stakeholder picks a direction you would not have, document it and commit. Do not litigate after the decision.

### Outputs

A consultation produces three artifacts:

1. **Decision log.** Date, decision, rationale. One row per major call (aesthetic, palette, typography, spacing, motion). The log explains why future contributors should not re-relitigate.
2. **Design direction document.** The full system, written down: aesthetic, palette with hex values, typography with font names and roles, spacing scale, layout approach, motion philosophy, explicit anti-patterns. This is the source of truth the team builds against.
3. **A preview or mockup.** A visual artifact showing the system applied to a real screen — at least the hero of the marketing site, or a representative page of the product. Without a preview, the document is theoretical.

The decision log lives at the top of the direction document. The mockup lives alongside, or is embedded as a screenshot. Together, they make the system reviewable, defensible, and reusable.

### Anti-patterns in consultation

- **Death by options.** Presenting every aesthetic, every palette, every font, every layout. The stakeholder cannot evaluate; the consultant has dodged the work of recommending.
- **No rationale.** "I recommend Geist" without "because the product wants a contemporary, neutral display face that does not call attention to itself." The rationale is the consultation.
- **Ignoring constraints.** Recommending a font stack the team cannot license, a stack the team cannot use, or an accessibility approach the team cannot ship.
- **Refusing to commit.** "I could go either way" is not a consultation. The consultant's job is to have the way.
- **Litigation after commit.** Once a decision is logged, the consultant defends it, not re-opens it. Reopening happens with new evidence, not with second thoughts.

---

## Design shotgun mode (multiple variants)

The shotgun is visual brainstorming: produce N genuinely-different variants, view them side by side, pick the winner. The mode is for when the team cannot describe the answer but will recognize it, or when the team is stuck in convergence and needs to see real divergence.

### When to use the shotgun (and when not to)

Use it when:

- The brief is fuzzy on visual direction. Words have stopped helping.
- The team is converging on a generic answer. Showing wilder variants resets the conversation.
- The stakeholder said "I don't like how this looks" but cannot say what would be better.
- You are early in a redesign and want to explore three directions before committing.
- The design system is in place but you need to see it applied across genuinely different aesthetic moves.

Skip it when:

- The brief already names the direction. Variants will be three flavors of the same thing; the exercise wastes time.
- The stakeholder is decisive and ready to commit. Show one strong proposal, defend it.
- You are late in implementation. Variants now mean rework; commit and ship.
- The decision is small (e.g., a single component, a single color). One option with rationale is faster.

### How many variants

- **Two** when the choice is binary (light vs dark, dense vs spacious, illustrated vs photographic). Two surfaces the trade-off cleanly.
- **Three** for general exploration. Three is enough to triangulate without diluting; the most common shotgun count.
- **Four or more** when the directions are truly divergent and the team needs to see the full space. Reserve for genuinely creative briefs where the answer might be in any of four corners.

More than six variants is rarely useful. The team cannot hold that many comparisons in mind; the second-tier variants get ignored.

### Variant axes (what to vary)

A shotgun without an axis is noise. Pick one or two axes per round and hold the rest constant.

- **Style.** Brutalist vs editorial vs luxury vs playful. The aesthetic family changes; the layout, density, and motion may stay similar.
- **Layout.** Grid-disciplined vs editorial-asymmetric vs poster-stacked. Same palette and type, different composition.
- **Density.** Airy gallery vs balanced product vs cockpit-dense. Same components, different breathing room.
- **Motion intensity.** Static, intentional, or expressive. Same surface, different motion philosophy.
- **Color approach.** Restrained mono vs balanced bi-color vs expressive multi-accent.
- **Typography character.** Clean grotesk vs expressive display vs editorial serif-sans pairing.

The strongest shotguns vary one axis sharply (e.g., style) and let the consequences fall where they may. Trying to vary every axis at once produces incomparable variants.

### Generating variants

For each variant, decide its concept first, in writing, before producing anything visual. A concept is one sentence per variant: "A: brutalist editorial with a serif/grotesk pairing and a single ink-blue accent." "B: luxury-refined with a serif display, off-white surfaces, and warm-gray neutrals." "C: industrial-utilitarian with a monospace accent for data and a single muted teal."

Present the concepts as a lettered list before generating images. Confirm with the stakeholder that the directions are worth pursuing. If two concepts sound similar in words, they will look similar in pixels — rework one to diverge.

Anti-convergence directive: each variant must use a different font family, a different palette, and a different layout approach. The test: if someone could swap the headline text between two variants without noticing, they are too similar. Regenerate the weaker one with a deliberately different direction.

Variants should feel like they came from three different design teams, not from the same team at three different coffee levels.

### Comparing and choosing

Show the variants side by side. Not in a sequence, not on three tabs — side by side, in the same viewport, at comparable sizes. Decisions about visual direction are visual; they have to be made with eyes, not with memory.

For each variant, the stakeholder gives:

- **Rating.** One to five. Captures intuition.
- **Notes per variant.** What works, what does not, what they would steal.
- **Overall direction.** Which variant wins, or which combination of moves to pursue.

The winner is the one that wins. Do not negotiate.

If no variant wins outright, the diagnosis is usually that the axes were wrong or the concepts were not divergent enough. Run a second round with sharper axes; do not average across the first round.

### Avoiding "frankenstein synthesis"

The most tempting failure mode is to take "the typography from A, the color from B, the layout from C" and produce a synthesized fourth option. This is almost always bad.

Why it fails:

- The choices in each variant are coherent because they were made together. Taking the type from A removes it from the structure that made it work.
- The synthesis has no author. Every variant was a deliberate point of view; the synthesis is a committee.
- The synthesis loses the risk-taking that made any individual variant interesting. Averaging produces the bland median.

The right move when the stakeholder wants to combine elements:

- **Pick the strongest variant and iterate.** Take the variant that wins on the most important axis, then refine it with feedback from the others. "B wins on color; let's iterate B with the spacing rhythm from A."
- **Treat the others as critique, not parts.** What did A do well that B could absorb without breaking? Often the answer is "B was too restrained — borrow A's confidence with type scale." That is a refinement, not a frankenstein.
- **Run a second shotgun.** If the answer is genuinely "the right direction is none of these but somewhere in between," run another round with new concepts informed by the first.

The shotgun's value is in producing genuine alternatives. Synthesis destroys the alternatives. Iterate the winner instead.

### After the shotgun

Save the chosen direction as a reference for future sessions. Record what was approved, what was rejected, and why. The next shotgun for this product should bias toward the demonstrated taste and away from the rejected directions — without dogma. The taste record is evidence, not gospel; if the brief changes, the taste can change.

Move from the shotgun winner into the production pipeline: extract the design tokens (color, typography, spacing) from the chosen variant, add them to the design system document, and apply the system across the rest of the surface. The shotgun is the start of the work, not the end.

---

## Connecting the workflow

The six modes above are not separate skills; they are the moves of a single working method.

- **Translating an image** is the basic literacy: read what is there, extract the system, build it. Every other mode depends on this skill.
- **Redesigning an existing project** is translation applied to a moving target. The current UI is the reference for what to preserve; the new direction is the reference for what to change.
- **Developing taste** is the accumulating muscle that makes the other modes produce signal instead of noise. Without taste, translation is mechanical and redesigns are arbitrary.
- **HeroUI** is the component layer that lets you build product UI quickly without re-inventing primitives. It is a tool, not a style; you supply the style.
- **Consultation** is how decisions get made when the brief is ambiguous and the stakeholder is the source of truth.
- **The shotgun** is how decisions get made when words have stopped working and the stakeholder needs to see the alternatives.

The standing rules across all modes:

1. Reference first, code second. Whether the reference is an image, an audit, or a generated mockup, it precedes the build.
2. Coherence over individuality. Choices that reinforce each other beat choices that are individually optimal but mismatched.
3. Constraint, restraint, intentionality. When in doubt, do less.
4. Demo, do not describe. The visual artifact closes more decisions than the document.
5. Preserve equity, modernize the surface. Logos, brand colors, signature moments survive redesigns; the chrome around them does not.
6. Default to the more restrained option when the team is split.
7. Commit and ship. Litigation after commit is overhead; demo-driven iteration is progress.

Hold these and the work compounds. Each project teaches the system; the system makes the next project faster.
