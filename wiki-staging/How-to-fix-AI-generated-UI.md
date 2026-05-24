# How to Fix AI-Generated UI

AI-generated UIs share predictable fingerprints — Inter font, purple gradients, three equal cards, John Doe placeholders. Here's how to detect and fix them using a Claude Code plugin.

## What this page covers

You will learn how to identify the visual signatures of AI-generated interfaces, audit any existing surface for them, fix the findings in place, and prevent the pattern from showing up again in new work.

## The problem: AI slop has a fingerprint

When a large language model generates frontend code without specific instructions, it converges. The same fonts. The same gradients. The same hero composition. The same fake testimonial names. Once you can see the pattern, you cannot unsee it — and neither can your users, your investors, or your customers.

The plugin's job is to make you stop shipping that.

## The 10 most common AI fingerprints

### 1. Inter as the only font

The default. Sans-serif. Neutral. Used everywhere from Vercel marketing to startup landing pages. When every interface uses Inter, no interface feels designed.

**Detection signal:** `font-family: Inter` with no display face, no serif, no monospace counterweight.

**Fix:** Pair a display face (DM Serif Display, Fraunces, Editorial New) with a body face (Geist, Manrope, Söhne). Use a monospace (JetBrains Mono, Berkeley Mono) for code and numeric tables. Three faces, with clear roles.

### 2. Purple-to-pink gradient hero

The Stripe-derivative gradient. Indigo at top-left, pink-orange at bottom-right, 135-degree angle. Recognizable from a thumbnail. Used in roughly 40 percent of AI-generated landing pages.

**Detection signal:** `linear-gradient(135deg, #6366f1, #ec4899)` or anything in that color family.

**Fix:** If you need a gradient, build it from your own brand palette using OKLCH for perceptual uniformity. Use it once per page, not as wallpaper. Prefer a single accent color over a gradient on most surfaces.

### 3. Three equal cards in a row

The "Features" section pattern. Three cards. Same width. Same height. Same icon-title-paragraph structure. Always three. Never two. Never four.

**Detection signal:** `grid-template-columns: repeat(3, 1fr)` containing identical card components.

**Fix:** Asymmetric layouts. Two columns where one is wider. A hero card plus three supporting cards. A masonry grid. A horizontal scroller. Anything but the perfect three-by-one rectangle.

### 4. John Doe and jane@example.com placeholders

The fake person. Always John Doe or Jane Smith. Always with a generic title like "Product Manager." Always a stock-looking avatar. Always praising the product in vague terms.

**Detection signal:** Any string matching `John Doe`, `Jane Smith`, `jane@example.com`, `user@example.com`, `Lorem ipsum`, or placeholder testimonial text.

**Fix:** Either use real customers with permission or do not include testimonials at all. A landing page with no testimonials beats a landing page with fake testimonials. Empty is honest. Fake is desperate.

### 5. Centered hero with everything stacked

The middle-aligned wall. Headline centered. Subheadline centered. Two CTAs centered side-by-side. Image centered below. Nothing breaks the vertical line down the middle of the page.

**Detection signal:** A hero where every direct child has `text-align: center` and `margin: 0 auto`.

**Fix:** Asymmetric heroes. Headline on the left, product on the right. Headline at top with a horizontal product strip below. Editorial layouts where the eye moves diagonally, not vertically.

### 6. Generic SaaS gray-blue palette

Slate-700 text, slate-100 backgrounds, sky-500 accent, white cards with `shadow-lg`. The Tailwind defaults applied without taste. Looks like a Linear clone. Looks like every other Linear clone.

**Detection signal:** Color values matching Tailwind's default palette with no custom tokens defined.

**Fix:** Define brand-specific tokens. Pick a palette that says something about your product. Warm tones for hospitality. High-contrast monochrome for finance. Vibrant single-accent for creative tools. The point is intent.

### 7. Emojis as feature icons

Pizza emoji for restaurants. Rocket emoji for "fast." Sparkle emoji for "AI." Lightning bolt for "instant." The emoji-as-icon shortcut is the visual equivalent of using a stock photo.

**Detection signal:** Any emoji character (U+1F300 to U+1FAFF range) used inside a button, heading, card title, or feature description.

**Fix:** Inline SVG icons. Lucide. Phosphor. Feather. 1.5 to 2 pixel stroke. `currentColor` for theming. Consistent visual weight across the set.

### 8. "Trusted by" logos as a single gray strip

A horizontal row of company logos, all desaturated to gray, all sized identically, all evenly spaced. The compliance-grade "social proof" pattern.

**Detection signal:** A logo row with `filter: grayscale(1)` or `opacity: 0.5` applied uniformly.

**Fix:** If you have real logos with real permission, show them in color. If you do not have permission, do not include them. The gray strip with logos you have not licensed is both a design crime and a legal one.

### 9. Lorem ipsum or "engaging description" placeholder copy

Latin filler text. Or worse: copy that says "Engaging description of your product goes here" left in place. Or even worse: copy that reads like an AI tried to sound human and produced phrases like "Unleash the power of seamless integration."

**Detection signal:** Any of the strings `Lorem ipsum`, `dolor sit amet`, `description goes here`, or filler verbs like `Unleash`, `Elevate`, `Empower`, `Seamlessly`.

**Fix:** Write real copy. Specific verbs. Specific outcomes. Specific objects. "Add a customer to a transaction" beats "Seamlessly integrate customer data with your transaction workflows."

### 10. Symmetric perfect rectangles everywhere

Every section is a rectangle. Every card is a rectangle. Every container is a rectangle. Padding is consistent. Border-radius is consistent. Nothing overlaps. Nothing breaks the grid.

**Detection signal:** Page-level layout with no overlapping elements, no negative space asymmetry, no elements that bleed past their container.

**Fix:** Break the grid intentionally. An image that bleeds past the card edge. A heading that overlaps two columns. A negative-space block that creates visual rhythm. A section divider that is not a horizontal line.

## Run the audit: detect AI slop in an existing surface

Once the plugin is installed, point it at any URL or local file.

```bash
# Audit a deployed page
/ux-polish https://your-site.com/landing

# Audit a local file
/ux-polish ./resources/views/landing.blade.php

# Audit an entire directory
/ux-polish ./src/components/marketing/
```

The audit returns a structured report with:

- **Severity-ranked findings** — critical (blocks ship), major (must fix), minor (taste call)
- **Specific line numbers and selectors** — not "the hero feels generic," but "line 47 uses Inter without a display pair"
- **Concrete fix recommendations** — what to change, to what value, why

A real audit output looks like this:

```
UX Polish Audit — landing.blade.php
====================================

CRITICAL (2 findings)
  L47  Inter is the only font face declared. No display face for headings.
       Recommendation: Add a display pair (DM Serif Display or Fraunces).
       
  L82  Three-equal-card layout in features section.
       Selector: .features > .grid (grid-template-columns: repeat(3, 1fr))
       Recommendation: Break the symmetry. Try a 2+1 or asymmetric grid.

MAJOR (4 findings)
  L23  Hero CTA uses placeholder text "Get Started" with no verb-outcome pair.
       Recommendation: "Start a free trial" or "See it in 60 seconds."
       
  L156 Testimonial uses placeholder name "John Doe."
       Recommendation: Real customer with permission, or remove the section.
       
  L201 Purple-to-pink gradient on the CTA section (#6366f1 to #ec4899).
       Recommendation: Use your brand accent token, not the default gradient.
       
  L289 Emoji used as icon in feature card (rocket, sparkle, lightning).
       Recommendation: Inline SVG from Lucide or Phosphor.

MINOR (3 findings)
  L67  Centered hero composition. Every child aligned to vertical centerline.
       Recommendation: Consider an asymmetric layout for visual interest.
       
  L134 "Trusted by" logos with grayscale filter applied uniformly.
       Recommendation: If licensed, show in color. If not, remove.
       
  L312 Copy uses filler verbs ("seamlessly," "unleash," "elevate").
       Recommendation: Specific verbs tied to specific outcomes.
```

## Fix the findings

Run the same command with `--fix` to apply recommendations in place.

```bash
/ux-polish ./resources/views/landing.blade.php --fix
```

The plugin will:

1. Show you each finding and the proposed fix
2. Ask for confirmation on taste-call decisions (color choices, font pairings)
3. Apply mechanical fixes automatically (placeholder text, emoji replacement, grid breaks)
4. Generate a diff summary at the end

For tighter control, fix one category at a time:

```bash
/ux-polish ./landing.blade.php --fix --only=fonts
/ux-polish ./landing.blade.php --fix --only=colors
/ux-polish ./landing.blade.php --fix --only=copy
/ux-polish ./landing.blade.php --fix --only=layout
```

## Prevent it next time

The audit-and-fix loop catches problems after they exist. The better move is to not generate slop in the first place.

For new builds, use the design command. It runs a discovery protocol before any code is written.

```bash
/ux-design landing page for a B2B finance SaaS targeting CFOs at mid-market firms
```

The discovery protocol asks 10 questions before generating anything:

1. Who is the user? (specific persona, not "users")
2. What is the one job they came here to do?
3. What is the brand voice? (sample lines)
4. What is the visual register? (editorial, brutalist, Apple-clean, etc.)
5. What stack are you on? (framework, CSS approach)
6. What are the must-haves vs nice-to-haves?
7. What is the constraint you cannot break? (accessibility, performance, brand)
8. What competitors do you respect, and why?
9. What anti-patterns do you want to avoid?
10. What is the call to action and what happens when they click it?

Only after the answers are in does the plugin generate. The result is specific, not generic.

## Real example: before and after

### Before — generic AI output

A B2B SaaS landing page for a "treasury management platform." The output:

- Headline: "Unleash the power of seamless treasury management"
- Subheadline: "Empower your finance team with intelligent automation"
- Hero: centered. Inter font throughout. Purple-to-pink gradient background.
- Features: three equal cards with rocket emoji, lightning emoji, sparkle emoji
- Testimonials: John Doe, CFO at Example Corp; Jane Smith, VP Finance at Acme
- CTA: "Get Started" in a gradient button

Looks like every other AI-generated B2B landing. Nothing in it tells you what the product does, who it is for, or why it exists.

### After — `/ux-polish --fix` plus discovery

Same brief, run through the plugin with discovery answers (CFOs at mid-market firms, specifically those who run weekly treasury close):

- Headline: "Close your weekly treasury report in 14 minutes, not 4 hours."
- Subheadline: "Reconciliation across 6 bank accounts, FX positions, and intercompany loans — done before your 9 AM standup."
- Hero: asymmetric. Headline left, product screenshot right with one annotation arrow pointing to the variance summary.
- Font pair: Fraunces (display) + Inter (body) + JetBrains Mono (numeric tables).
- Features: a 2+1 grid. One large card showing the variance reconciliation flow. Two supporting cards for FX hedging and intercompany. Each card has a custom illustration of the actual workflow, not a stock icon.
- Social proof: three real customer logos with permission, in full color, plus one verbatim pull quote with name, title, and company.
- CTA: "Run the 14-minute close on your own data" — verb plus outcome, specific not generic.
- Color: high-contrast monochrome with a single saturated teal accent for active states. No gradient.

Same starting prompt. Different output. The difference is the discovery protocol and the anti-slop pass.

## Common AI fingerprints catalogue

For reference, the full list of patterns the plugin flags, with do/don't pairs.

| Anti-pattern | Don't | Do |
|---|---|---|
| Inter as only font | `font-family: Inter, sans-serif` everywhere | Display pair plus body pair plus mono |
| Purple-pink gradient | `linear-gradient(135deg, #6366f1, #ec4899)` | Brand-specific accent, used sparingly |
| Three equal cards | `grid-template-columns: repeat(3, 1fr)` | Asymmetric grids (2+1, masonry, scroller) |
| Centered hero stack | Everything `margin: 0 auto` | Left-aligned, asymmetric, editorial |
| John Doe placeholders | "John Doe, CEO at Example Corp" | Real customers or no testimonials |
| Lorem ipsum | "Lorem ipsum dolor sit amet" | Real copy or empty state with intent |
| Emoji as icons | Rocket, sparkle, lightning in feature cards | Inline SVG, 1.5-2px stroke, currentColor |
| Gray logo strip | "Trusted by" with desaturated logos | Real logos in color with permission |
| Filler verbs | "Unleash," "Elevate," "Empower," "Seamlessly" | Specific verbs with specific outcomes |
| Perfect rectangles | Every section a uniform card | Intentional grid breaks, bleeds, overlap |
| Default Tailwind palette | Slate-700, sky-500, white cards, shadow-lg | Custom tokens for your brand |
| Generic feature triplet | Speed, Security, Scale | Specific capabilities your users asked for |
| Stock product screenshots | Generic dashboard mock | Real screenshot or domain-accurate illustration |
| Loading spinners with no copy | A spinner alone in the middle of the page | "Closing the books for May..." with progress |
| Empty states with no action | "No data yet" with no next step | Sentence plus action ("No customers yet. Add one.") |

## Why AI converges on these patterns

A note on root cause. Understanding why AI produces these fingerprints helps you write better prompts and recognize failures faster.

### Training data bias

Language models are trained on the public internet. The public internet is full of generic SaaS landings, default Tailwind palettes, and Inter-everywhere. When asked to generate a SaaS landing, the model produces the statistical average of what it has seen. The average is what you are fighting.

### Reward signal bias

Models are tuned with human preference data. Humans, when given two outputs, tend to pick the one that looks "safe" and "professional." Safe and professional often means generic. Over many rounds of preference tuning, the model gravitates further toward the safe option.

### Lack of taste anchor

When you ask "generate a landing page," you give the model no taste anchor. The model has no idea whether you want Apple-clean, brutalist, editorial, or maximalist. With no anchor, it defaults to the center of its distribution — generic SaaS.

The discovery protocol fixes the third problem. The anti-slop audit fixes the first two by checking the output against a catalogue of known-bad patterns and forcing corrections.

## Manual checks the plugin can't fully automate

Some AI fingerprints need a human eye. The audit flags them; the human decides.

### The hero illustration that screams Midjourney

AI-generated hero illustrations have their own fingerprints. Floating glass orbs. Geometric abstract shapes. Hyper-saturated gradients. People rendered with slightly-wrong hands or faces. Logos with letters that almost-but-not-quite match the brand name.

The plugin flags any hero image. The human checks whether it looks generated. If yes, replace with:

- A real product screenshot (best)
- A custom illustration commissioned from a real illustrator
- A clean photograph with attribution
- No image at all — sometimes the absence is the better choice

### The "as featured in" badge row that is not real

If your landing has badges saying "Featured in TechCrunch, Forbes, Wired" — verify each one is real. The model will invent these. Inventing press coverage is fraud, not bad design.

The plugin flags any badge row. The human verifies each citation has a real link to a real article published with permission to use the badge.

### The customer logos you do not have permission to use

A logo strip with company logos you do not have permission to display is both an AI-output tell and a legal problem. The model will happily generate logos for "Acme Corp," "Stripe," "Notion," and "Linear" because those are common in its training data. None of those companies gave you permission.

The plugin flags any logo strip. The human verifies permission for each one.

### The roadmap that promises features that do not exist

AI-generated roadmaps include capabilities the product has not built. "Coming Q3 — AI-powered insights." "Roadmap — automated reconciliation." Reads as ambitious; in reality, sets up disappointment.

The plugin flags any roadmap section. The human verifies every promised feature has a real plan to ship by the stated date.

## Stack-specific fixes

The fix recipes change slightly by framework. The principles do not.

### React / Next.js fixes

Common patterns the plugin rewrites:

```jsx
// Before: generic Tailwind defaults
<div className="bg-gradient-to-br from-indigo-500 to-pink-500 text-white">
  <h1 className="text-5xl font-bold text-center">Unleash the Power</h1>
</div>

// After: token-based, asymmetric
<div className="bg-(--color-bg-primary) text-(--color-text-primary)">
  <div className="grid grid-cols-12 gap-8 py-24">
    <h1 className="col-span-7 font-display text-6xl leading-tight">
      Close your weekly treasury report in 14 minutes.
    </h1>
    <ProductScreenshot className="col-span-5" />
  </div>
</div>
```

### Vue / Nuxt fixes

```vue
<!-- Before -->
<template>
  <div class="hero-centered">
    <h1>Empower Your Business</h1>
    <p>Seamlessly integrate with your existing tools.</p>
    <button>Get Started</button>
  </div>
</template>

<!-- After -->
<template>
  <section class="hero-asymmetric">
    <div class="hero-content">
      <h1>Close your weekly treasury report in 14 minutes.</h1>
      <p>Reconciliation across 6 bank accounts, FX positions, intercompany loans.</p>
      <button class="cta-primary">Book a 15-minute demo</button>
    </div>
    <ProductScreenshot class="hero-visual" />
  </section>
</template>
```

### Laravel / Blade fixes

```blade
{{-- Before --}}
<div class="text-center py-20 bg-gradient-to-r from-purple-600 to-pink-600">
  <h1 class="text-5xl text-white font-bold">{{ __('marketing.hero.title') }}</h1>
  <p class="text-white/80 mt-4">{{ __('marketing.hero.subtitle') }}</p>
  <a href="#" class="bg-white text-purple-600 px-8 py-4 rounded-full">Get Started</a>
</div>

{{-- After --}}
<section class="grid grid-cols-12 gap-8 py-24">
  <div class="col-span-7">
    <h1 class="font-display text-6xl leading-tight">
      {{ __('marketing.hero.title') }}
    </h1>
    <p class="mt-6 text-xl text-(--color-text-muted)">
      {{ __('marketing.hero.subtitle') }}
    </p>
    <a href="/demo" class="mt-10 inline-flex items-center bg-(--color-accent) text-(--color-text-on-accent) px-6 py-3 rounded-full">
      {{ __('marketing.hero.cta') }}
    </a>
  </div>
  <x-product.screenshot class="col-span-5" />
</section>
```

The Blade version also enforces locale keys — the headline and subtitle live in `lang/{locale}/marketing.php`, not hardcoded.

### Astro fixes

Astro's static-first output makes anti-slop patterns easier to enforce — no runtime override of token values, no client-side framework injecting defaults.

```astro
---
import ProductScreenshot from "../components/ProductScreenshot.astro";
---

<section class="hero">
  <div class="hero-content">
    <h1>Close your weekly treasury report in 14 minutes.</h1>
    <p>Reconciliation across 6 bank accounts, FX positions, intercompany loans.</p>
    <a href="/demo" class="cta-primary">Book a 15-minute demo</a>
  </div>
  <ProductScreenshot />
</section>

<style>
  .hero {
    display: grid;
    grid-template-columns: 7fr 5fr;
    gap: 2rem;
    padding: 6rem 0;
  }
  .hero h1 {
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 5vw, 4rem);
    line-height: 1.05;
  }
</style>
```

## Edge cases the audit handles

### Multi-page audits

For a project with 20+ pages, the plugin can run a project-wide audit.

```bash
/ux-polish ./src/pages/ --recursive
```

The report consolidates findings across pages and surfaces patterns. If three pages all use the same purple-pink gradient, the recommendation is "fix this once at the token level, not three times at the component level."

### Generated documentation sites

Documentation sites (Docusaurus, MkDocs, Mintlify defaults) often have their own AI-slop fingerprints — generic feature grids, identical card layouts on every concept page, placeholder examples. The audit handles them.

```bash
/ux-polish ./docs/ --recursive --doc-mode
```

The doc-mode flag relaxes the "asymmetric grids" rule (documentation often benefits from grid consistency) but tightens the "specific examples" rule (a doc with `foo = "bar"` examples is doc slop).

### Component libraries

When auditing a component library (your own design system, or one you maintain for clients), the plugin checks token discipline, prop API consistency, and the do/don't pairs published in the docs.

```bash
/ux-polish ./packages/ui/src/ --component-library
```

The output flags components that hardcode colors instead of referencing tokens, components missing variants, and components without TypeScript types where the rest of the library has them.

## Beyond the audit: prevent recurrence

Once a project is on the plugin, the same checks run in three other places:

- `/ux-system` — when generating a design system, the tokens are bounded so AI-slop colors and fonts cannot come back in
- `/ux-design` — when generating new components, the discovery protocol forces specificity upfront
- `/ux-copy` — when reviewing microcopy, the filler-verb ban list and marketing-cliché ban list catch generic phrasing

You stop fighting AI slop one component at a time. You build a workflow where it does not appear.

## The shipping discipline

A practical rule of thumb for production work.

### Rule 1: never ship a page without running the audit

Make `/ux-polish` part of the pre-merge check. If a PR adds or modifies a marketing surface, the audit runs in CI and posts findings as PR comments. Critical findings block merge.

### Rule 2: store the audit report alongside the surface

Keep the audit output in `./surface-name.audit.md` next to the file. When the next person edits it, they have the audit history.

### Rule 3: run the audit on staging before production

Staging URLs sometimes use placeholder content that gets replaced on production. Run the audit against staging to catch issues before they reach customers.

### Rule 4: track audit scores over time

The audit produces a numeric score. Track it across the project — when it drops, investigate the cause. Sudden drops usually mean someone shipped without running the audit, or a generation step regressed.

## Linked next steps

- Building a new landing page from scratch? See [How to build a SaaS landing page with Claude Code](How-to-build-a-SaaS-landing-page-with-Claude-Code).
- Need to rebuild your design tokens before fixing slop? See [How to generate a design system with Claude Code](How-to-generate-a-design-system-with-Claude-Code).
- AI copy fingerprints are a separate problem class. See [How to fix microcopy that sounds like AI](How-to-fix-microcopy-that-sounds-like-AI).
- Accessibility is the other half of the polish pass. See [How to audit accessibility with Claude Code](How-to-audit-accessibility-with-Claude-Code).

---

**See also**: [How to build a SaaS landing page with Claude Code](How-to-build-a-SaaS-landing-page-with-Claude-Code) | [How to fix microcopy that sounds like AI](How-to-fix-microcopy-that-sounds-like-AI) | [How to audit accessibility with Claude Code](How-to-audit-accessibility-with-Claude-Code)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
