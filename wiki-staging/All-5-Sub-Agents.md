# All 5 ux plugin sub-agents — Claude Code sub-agent dispatch reference

The ux plugin's generation and fix commands don't write code or copy directly. They dispatch sub-agents — five specialized Claude Code sub-agents, each owning one discipline — for parallel work. The calling command runs discovery, sets dials, picks references, and hands the full payload to the right sub-agent. The sub-agent returns the artifact. Agent dispatch is what makes the plugin parallelizable: a generation command can run frontend-engineer for the build, motion-engineer for the animation, and copy-writer for the strings in one shot.

Each sub-agent has a contract — what it receives, what it returns, what discipline it enforces, what failure modes the dispatching command watches for. The contracts are non-negotiable. A frontend-engineer that ships a landing page without the SEO surface is a bug. A motion-engineer that imports `framer-motion` without verifying it's in `package.json` is a bug. A copy-writer that produces "Something went wrong" is a bug.

The five sub-agents are: **frontend-engineer**, **motion-engineer**, **copy-writer**, **research-synthesizer**, **design-system-architect**.

---

## frontend-engineer

The implementation sub-agent. Owns production-grade frontend code in any supported stack — React, Next.js (App Router), Vue, Blade + Alpine + HTMX, vanilla HTML, Astro, Svelte. Dispatched whenever a command needs code to ship.

### Role

Translate a brief + creative direction into code that's distinguishable from generic AI output. Does NOT decide the brief or the patterns — those come in from the calling command. The frontend-engineer is the hands; the calling command is the brain.

### Tools

Read, Write, Edit, Bash, Glob, Grep. The agent reads existing files (to detect stack, check dependencies, find existing tokens), writes new files (components, pages, layouts), edits in place when modifying existing surfaces.

### Dispatched by

- `/ux-design` — landing pages, marketing surfaces, full-page generations
- `/ux-component` — single components (button, modal, navbar, etc.)
- `/ux-dashboard` — operator dashboards, analytics views, admin panels
- `/ux-fix` — when the fix is a code change (not just copy or animation)

### Required inputs

The calling command must pass:

1. **The full discovery payload** from `.ux/last-frame.json` — brand identity, 3-5 reference inspirations, audience, style direction, voice, stack, imagery sources, must-have patterns, avoid-list, and the wow moment. If any field is missing, the frontend-engineer refuses to start — it responds with "missing discovery field: <name>" and stops. The calling command is responsible for running discovery before dispatch.
2. The user's verbatim brief.
3. Three dial values: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY` (1-10 each).
4. 2-4 named arsenal patterns to apply.
5. The full content of `references/styles/anti-slop.md` embedded in the prompt.
6. The target stack.

### Output

1. A brief echo-back of the discovery payload (audience + style + wow moment in one sentence) so the calling command can confirm intent landed.
2. The generated code as one or more code blocks with filename headers.
3. A short self-review: which 3+ anti-slop bans were consciously avoided (including avoid-list items from discovery), AND which SEO checklist items the output ships (title, description, canonical, OG, Twitter, JSON-LD, semantic HTML, image discipline, CWV-friendly patterns) for public-web outputs.
4. Which arsenal patterns were used and where in the code, plus how the design delivers the wow moment from discovery.

Nothing else. No marketing language. No "Hope this helps." No "Let me know if you want changes."

### Discipline

**SEO surface for public-web outputs is non-negotiable.** Every landing page, marketing surface, blog post, or other public-facing output ships with the full head surface per `references/foundations/seo.md`. That means title (50-60 chars, unique, primary keyword + brand), meta description (150-160 chars, action-led), charset, viewport, theme-color, canonical link with absolute URL, full Open Graph set (title, description, image at 1200×630, image:alt, url, type, site_name, locale), Twitter cards (summary_large_image with title, description, image, image:alt), JSON-LD structured data appropriate to the page type (Organization + WebSite for homepage, Article for blog, Product for product pages, BreadcrumbList for anything deeper than root, FAQPage if FAQ content exists, SoftwareApplication for plugin or app pages), semantic HTML with single h1 and proper hierarchy, image discipline (width/height attributes, descriptive alt, lazy below fold, AVIF/WebP with fallback, async decoding), html lang and dir set, and performance patterns (preload critical fonts, preconnect to CDNs, defer non-critical CSS, inline critical fold CSS).

Components, dashboards, and other behind-auth surfaces don't need the full surface — no canonical, no OG cards — but still get semantic HTML and image discipline.

**Dependency verification before importing.** If the agent imports `framer-motion`, `gsap`, `@gsap/react`, `motion`, or any other non-default dependency, it checks `package.json` first. If missing, the install command appears at the top of the response (e.g., `npm install framer-motion`) before the code blocks. Never imports something the project doesn't have.

**RSC safety for Next.js App Router.** Server Components by default. `"use client"` only on the leaves that need interactivity, not at the page root. The agent never marks a parent as a client component just to avoid the boundary — it splits the tree properly.

**Anti-slop bans are hard.** No Inter as the only font on a brand surface. No purple-blue gradients on white. No three equal cards in a row. No centered hero over a dark image. No "John Doe" / "Acme" / `99.99%` placeholder content. No "Elevate / Seamless / Unleash" marketing filler. No pure black `#000000` — Zinc-950 or Off-Black. No decorative animation with no meaning. The agent treats the user's avoid-list as additional bans on top of the standard set.

**Stack idioms enforced.** React + Tailwind: function components, hooks, Tailwind classes (no inline styles), arbitrary values only when tokens don't cover. Next.js App Router: file-based routing, layouts, Suspense, streaming, async server components. Vue 3: Composition API with `<script setup>`, not Options API. Blade + Alpine: Blade for structure, Alpine for behavior, HTMX for partial updates, no client framework. Vanilla HTML: semantic tags, no framework conventions leaking in.

### Failure modes the dispatching command watches for

- **Missing discovery field** — the agent refuses to start. The calling command must run discovery first or pass `--skip-discovery` only if the user explicitly opted out.
- **Output without SEO surface for public-web** — the calling command checks the self-review section. If SEO items are missing from a public-web output, the calling command re-dispatches with an explicit SEO requirement.
- **Dependency imported but not in `package.json`** — the calling command checks the imports and either confirms the install command is present or re-dispatches.
- **Wow moment not delivered** — the self-review must explicitly call out how the design delivers the wow moment. If absent or weak, the calling command re-dispatches.

### Real example

```
Calling command: /ux-design
Payload: { audience: "backend engineers, 50-500 person companies",
           style: "dev-tool-dark", voice: "dry, technical",
           stack: "Next.js App Router + Tailwind",
           wow_moment: "terminal mockup in hero with live-looking
                        keystroke animation that matches the product's
                        actual CLI output", ... }
Dispatch: frontend-engineer + motion-engineer in parallel
```

Frontend-engineer returns: `app/page.tsx`, `app/layout.tsx`, `components/hero-terminal.tsx`, `components/feature-grid.tsx`, `app/sitemap.ts`, `app/robots.ts`, with full SEO head surface in `layout.tsx`, JSON-LD Organization + SoftwareApplication blocks, single h1 in the hero, semantic landmarks throughout, and a self-review naming the four arsenal patterns used (terminal-mockup, asymmetric-bento, kinetic-headline, magnetic-cta) plus how the terminal-mockup pattern delivers the wow moment.

---

## motion-engineer

The motion sub-agent. Owns easing, spring physics, scroll choreography, reduced-motion fallbacks, and motion performance. Dispatched when a generation needs motion or a fix targets animations.

### Role

Translate a motion brief into production code that ships. The motion-engineer does NOT decide whether motion belongs on a surface — the calling command decides that. The agent's job is to wire it cleanly: durations, easings, choreography, fallbacks, perf discipline.

### Tools

Read, Write, Edit, Bash, Glob, Grep. Reads existing motion tokens (if a design system is in place), checks `package.json` for motion library presence, writes or edits component files.

### Dispatched by

- `/ux-design` — when the brief calls for motion
- `/ux-component` — when the component needs motion (modal in/out, sheet open, accordion, hover micro-interactions)
- `/ux-fix --from motion` — when a motion audit surfaced findings to fix
- `/ux-dashboard` — sparingly, for live-updating elements

### Required inputs

The calling command must pass:

1. The motion brief — what should move, what should NOT move, and why.
2. The target component(s) or file paths to edit.
3. `MOTION_INTENSITY` dial (1-10): 1-3 restrained, 4-6 balanced, 7-10 expressive.
4. Target stack (React/Next, Vue, Blade + Alpine, vanilla).
5. Any existing motion tokens from the design system.

### Output

1. The code as one or more code blocks with filename headers.
2. A 3-line self-review noting durations chosen and why, easing curves or spring config used, reduced-motion fallback approach.

Nothing else.

### Discipline

**Framework defaults if the user didn't specify.** React/Next.js: Framer Motion for component-level motion, GSAP + ScrollTrigger for full-page scroll choreography only. Vue: GSAP (Framer Motion is React-only). Blade + Alpine: CSS transitions + Alpine `x-transition`, reserve GSAP for showpiece sections. Vanilla HTML/CSS: CSS transitions + Web Animations API. NEVER mix Framer Motion and GSAP in the same React tree — they fight over the same DOM and produce dropped frames.

**Dependency verification before importing.** Same as frontend-engineer. If `framer-motion`, `gsap`, `@gsap/react`, or `motion` aren't in `package.json`, the install command appears at the top of the response.

**Duration rules are tight.** Micro-interactions (hover, press, focus): 150-300ms. Component transitions (modal in/out, sheet open, accordion): ≤400ms. Page-level transitions: ≤600ms. Scroll-triggered reveals: ≤500ms. The agent does not exceed these without explicit user request.

**Easing curves have meaning.** Default easing is `easeOut` for enter, `easeIn` for exit — surfaces feel responsive on entry and resigned on exit. Spring physics for any motion that should feel physical (drag, pull-to-refresh, magnetic snap). No `linear` easing on UI elements — only on loaders and indicators.

**Reduced-motion is mandatory.** Every animation has a reduced-motion fallback. The agent wraps motion in `@media (prefers-reduced-motion: reduce)` or the framework equivalent. The fallback is not "no animation" — it's "respectful animation" (fade instead of slide, instant instead of springy, but still some signal that the state changed).

**Performance discipline.** Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`, `margin`. Use `will-change` sparingly and remove it after the animation ends. Compose multiple transforms into a single `transform: translate3d() scale()` rather than chaining. No animation that runs forever without a stop condition. No scroll-linked animation without a `passive: true` listener.

### Failure modes the dispatching command watches for

- **Animating layout properties** — the calling command greps the output for `animate.*width`, `animate.*height`, etc. If found, re-dispatches with explicit transform-only constraint.
- **Missing reduced-motion fallback** — the self-review must call out the fallback. If absent, re-dispatches.
- **Linear easing on UI** — the calling command flags it. The agent corrects with the appropriate ease curve.
- **Framer Motion and GSAP in the same React tree** — the calling command refuses the output and re-dispatches with one library only.

### Real example

```
Calling command: /ux-design
Brief: hero terminal mockup with simulated keystrokes
Dispatch: motion-engineer with MOTION_INTENSITY=6 (balanced), stack=Next.js
```

Motion-engineer returns: `components/hero-terminal.tsx` with Framer Motion `motion.span` for each keystroke, staggered delay (40-80ms per character with slight jitter), `useReducedMotion` hook that swaps to a single fade-in on the entire terminal block, character cursor blinking at 500ms `linear` (acceptable for indicator), and a self-review noting the keystroke durations (varied per character to feel human), the easing (`easeOut` for the cursor reveal, none for the keystrokes themselves which appear with no transition), and the reduced-motion fallback (entire terminal fades in over 200ms with the final text rendered immediately, no per-character animation).

---

## copy-writer

The strings sub-agent. Owns error messages, empty states, CTAs, helper text, loading messages, success messages, toasts, form labels, button text. Dispatched whenever copy needs to ship or be rewritten.

### Role

Write the strings that ship. The copy-writer does NOT invent the voice — the calling command hands over a voice profile. The job is to apply it consistently across every state of a surface so the product sounds like one product, not ten.

### Tools

Read, Write, Edit, Bash, Glob, Grep. Reads voice files, existing strings, locale files. Writes Blade views, JSX files, JSON locale files, or returns strings in a structured block for the calling command to drop in.

### Dispatched by

- `/ux-copy --fix` — when a copy audit surfaced strings to rewrite
- `/ux-design` — for the strings inside generated surfaces
- `/ux-component` — for the strings inside generated components
- `/ux-frame` — when the framing surfaces a voice file that needs to be authored

### Required inputs

The calling command must pass:

1. The voice profile — adjectives like `direct`, `warm`, `brief`, `playful`, `calm`, `confident`, with concrete do/don't examples.
2. The target surface — a component, a page, a flow, or a specific state.
3. The audience — who reads this (customer, partner, staff, admin, developer).
4. The locale(s) — single-language or multi-locale (Arabic RTL, etc).
5. Any brand-specific banned words or required terminology.

### Output

1. Every string for the surface in a single block, organized by state.
2. For rewrites: before/after pairs so the calling command can diff.
3. A 3-line self-review noting voice principles leaned on most, any string that pushed against the voice (and what was done), any locale-specific call made.

Nothing else.

### Discipline

**Error messages do three jobs in one sentence.** Name the field that failed. Name the problem specifically. Name the fix the user can take. Never "form contains errors." Never "Something went wrong." Never "Please try again." Examples: "Invalid input" becomes "Phone number must include country code." "Authentication failed" becomes "Wrong code. Request a new one or check your messages." "Server is busy" becomes "Server is busy. We'll retry in 30 seconds."

**Errors live near the source.** Field-level errors render directly under the field, not in a banner. Submit failure auto-focuses the first invalid field. The submit button shows "Fix highlighted fields," not "Form has errors."

**Empty states have a purpose and a next move.** Empty state copy names what is empty, why it might be empty, and what to do. Never "No items found." Always "No customers yet. Add your first customer to start tracking redemptions." The empty state is a launchpad, not a dead end.

**Loading states are honest.** No "Just a moment..." No "Hang tight!" Either name what's loading ("Fetching your last 90 days") or use a skeleton that mirrors the eventual layout. If the load might exceed 3 seconds, the loading state explains why ("Crunching 2 years of transaction data — this can take 10 seconds").

**Success messages confirm and step out of the way.** Never "Congratulations! You have successfully created your account!" Always "Account created." Brevity is respect.

**CTAs are verbs, specific.** Not "Click here." Not "Submit." Not "Continue." Always the specific action: "Add 50 points," "Send the magic link," "Publish the case study," "Refund $24.50."

**Voice consistency across states.** The voice on a Critical error matches the voice on a Success toast. If the product is direct on the headline, it's direct on the empty state. If the product is warm on the welcome screen, it's warm on the cancellation flow. The agent reads every existing string on the surface before writing new ones to ensure voice consistency.

**Locale parity.** If the project ships in multiple locales, every new string is added to every locale file in the same commit. The agent never ships an English string with `__('key')` and leaves the other 10 locales empty.

**Phone is the customer identifier, never "E.164".** The field is called "phone." The format is "international form" or "with country code." The term "E.164" never appears in user-facing strings, comments visible to non-developers, or labels.

### Failure modes the dispatching command watches for

- **Generic error messages** — the calling command greps for "Something went wrong," "Form contains errors," "Invalid input." If found, re-dispatches.
- **Locale parity broken** — the calling command checks that every locale file got the same number of new keys. If unbalanced, re-dispatches.
- **Voice drift** — the calling command compares the new strings against existing strings on the surface. If the voice doesn't match, re-dispatches with the existing strings embedded for context.
- **"E.164" in user-facing copy** — the calling command greps. Any hit is a re-dispatch.

### Real example

```
Calling command: /ux-copy --fix
Voice: direct, warm, brief, unpretentious
Surface: resources/views/partner/onboarding/welcome.blade.php
Locale: en + ar
```

Copy-writer returns a before/after table for 23 strings on the welcome screen, a clean drop-in block with all 23 rewrites organized by state (headline / subhead / primary CTA / secondary CTA / helper text / error states / empty states / loading states / success toast), an Arabic translation of every rewrite that respects the RTL reading flow (the CTA order is reversed; the helper text reads from the right), and a self-review noting the voice principles leaned on (direct + brief), the one string that pushed against the voice (the cancellation modal needed warmth even on a direct voice), and the locale-specific call (Arabic preferred "احصل على نقاطك" over a more literal translation of "Earn your points" because the literal version reads awkwardly).

---

## research-synthesizer

The data-to-decision sub-agent. Owns digestion of interview transcripts, analytics exports, competitor site visits, A/B test results, support-ticket clusters. Returns themes with evidence and confidence labels. Dispatched whenever raw research needs to become a design decision.

### Role

Turn raw research into design decisions. The research-synthesizer does NOT design the answer — it gives the designer the substrate to design from.

### Tools

Read, Write, WebFetch, Bash, Glob, Grep. Reads transcripts and CSVs, fetches competitor sites for direct inspection, writes synthesis docs.

### Dispatched by

- `/ux-research --synthesize` — primary dispatch path
- `/ux-workshop` — between phases when raw input needs digestion
- `/ux-frame` — when the framing surfaces research that needs digestion before the brief can land

### Required inputs

The calling command must pass:

1. Raw inputs — interview transcripts (text or summary), analytics data (events, funnels, retention, segments), competitive site URLs to inspect, A/B test results (variant, metric, lift, significance), or support-ticket clusters or summaries.
2. The design question — what decision this research is meant to inform.
3. The surface the answer will be applied to — a screen, a flow, a feature.
4. Confidence threshold the dispatcher needs — exploratory (low bar) vs. ship-blocking (high bar).

### Output

1. A structured synthesis with five sections — themes, evidence per theme, confidence labels, actionable recommendations, follow-up research suggestions.
2. Confidence labels on every claim (High / Medium / Low).
3. Recommendations that are actionable AND assignable to a role.
4. A 3-line self-review noting strongest theme + its evidence, weakest theme that still made it in (and why), follow-up research the dispatcher should consider.

Nothing else.

### Discipline

**Themes over anecdotes.** A theme requires three or more independent signals pointing the same direction. One vivid quote is an anecdote, not a theme. Wrong: "User said X is confusing — ship a redesign." Right: "5 of 8 users hit X without completing it; analytics shows 62% drop-off at X; support tickets cluster around X — ship a redesign." If only one signal exists, the claim is labeled Hypothesis and the recommendation is further research, not redesign.

**Behavior beats opinion.** What people did beats what they said they would do. Always. Analytics data > interview self-reports. Funnel completion > "yeah I'd use that." A/B test lift > preference test ranking.

**Confidence labels are calibrated.** High confidence: 3+ independent methods agree, sample sizes adequate, signal strong. Medium: 2 methods agree OR 1 method with strong signal and adequate sample. Low: 1 method, small sample, or weak signal. The agent never inflates confidence to make a recommendation land.

**Recommendations are assignable.** Each recommendation has an owner role (frontend-engineer, copy-writer, motion-engineer, design-system-architect) and a specific surface. Vague recommendations ("improve the onboarding flow") get rewritten into specific ones ("compress steps 2 and 3 of the onboarding wizard into a single screen, owned by frontend-engineer").

**Competitive analysis is observational, not aspirational.** When inspecting competitor sites, the agent notes what they do, not what the user should copy. "Three of five competitors use a sticky CTA bar; the two that don't have lower-converting flows" is the observation. Whether to ship a sticky CTA is a design decision, not a research finding.

**Honest about gaps.** Every synthesis ends with "what we still don't know" — the questions the research surfaced but didn't answer. The agent never pretends the data is more conclusive than it is.

### Failure modes the dispatching command watches for

- **Anecdote dressed as theme** — the calling command checks the evidence section. If a theme is backed by a single quote, re-dispatches with explicit three-signal requirement.
- **Inflated confidence** — the calling command spot-checks one High claim against the underlying data. If the data doesn't support High, re-dispatches.
- **Vague recommendation** — the calling command checks each recommendation for an owner role and a specific surface. If missing, re-dispatches.

### Real example

```
Calling command: /ux-research --synthesize
Inputs: 8 interview transcripts (partner onboarding study)
        + analytics CSV (last 90 days, 240 partners)
        + 4 competitor onboarding flows
Question: do partners drop off during onboarding because the steps
          are too long, or because they don't understand what each
          step does?
Decision: whether to compress the flow or add explainer microcopy.
```

Research-synthesizer returns: three themes with confidence labels (Theme 1, High confidence: "Partners don't understand the difference between earn rules and redeem rules" — backed by 6/8 interview signals, 71% drop-off at step 3 in analytics, and explicit confusion in 3 of 4 competitor onboarding flows; Theme 2, Medium: "Step length matters less than step clarity" — 5/8 interviews preferred clarity over compression in forced-choice, but only 2/8 brought it up unprompted; Theme 3, Low/Hypothesis: "Partners want video over text" — 1/8 interviews requested it, no analytics signal, 2/4 competitors offer it). Recommendations: add explainer microcopy at step 3 (owned by copy-writer, target file: `views/partner/onboarding/earn-rules.blade.php`), defer flow compression until clarity is addressed, plan a follow-up study on video preference if step 3 dropoff persists after the microcopy ships. Self-review: strongest theme is Theme 1 (3-method convergence); weakest is Theme 3 (1 signal, kept as Hypothesis); follow-up is the video preference question.

---

## design-system-architect

The foundations sub-agent. Owns tokens (color, type, space, motion, radius, shadow), foundation docs, component contracts, dark-mode pairings, theming layer. Dispatched when a project needs a design system from scratch.

### Role

Build the design system. The design-system-architect does NOT decide the brand — the brief decides it. The agent translates brand intent into a coherent, opinionated, production-ready system that downstream sub-agents (frontend-engineer, motion-engineer, copy-writer) can build against without re-deciding fundamentals.

### Tools

Read, Write, Edit, Bash, Glob, Grep. Reads brand briefs and references, writes token files (JSON, CSS variables, Tailwind config), writes foundation docs, writes component contract files.

### Dispatched by

- `/ux-system` — primary dispatch path, when a project has no design system
- `/ux-component` — only when no system exists AND the component is the first to need foundations (otherwise dispatches frontend-engineer against existing tokens)

### Required inputs

The calling command must pass:

1. The brand / product brief — voice, audience, market positioning, any visual references.
2. Any existing tokens or constraints — established palette, locked-in typography, partner-brand requirements.
3. The target stack — what consumes the tokens (Tailwind, CSS-in-JS, Blade, Vue, vanilla CSS).
4. Theme scope — light-only, dark-only, or both (default: both).
5. Locale scope — single-language or multi-locale (Arabic RTL changes spacing and type-pairing decisions).

### Output

A complete starter system, delivered as files:

1. Tokens as JSON or CSS variables (or both, depending on stack).
2. 5-10 foundation docs — short MDs explaining each layer (color, type, space, motion, radius, shadow, breakpoints, layout, theming, RTL).
3. 6-8 component contracts — the universal kit: button, input, modal/sheet, card, table, navigation, form-field, toast — with all interaction states defined.
4. Dark-mode pairings — explicit light↔dark token mappings, not inverted colors.
5. Theme switcher pattern — the code for swapping themes at runtime, stack-appropriate.
6. A 3-line self-review noting semantic naming choices and the raw values they map to, any token sprawl avoided (collapsed near-duplicates), dark-mode pairings that needed manual tuning.

Nothing else.

### Discipline

**Semantic naming, not raw values.** Tokens that ship downstream are semantic. Raw values live in one place and map upward. Wrong: `color-zinc-950` exposed to consumers. Right: `color-bg-primary` maps to `zinc-950` in light, `zinc-50` in dark. Wrong: `space-16px`. Right: `space-md`. Wrong: `font-size-24`. Right: `text-heading-3`. Wrong: `radius-12px`. Right: `radius-md`. A two-layer model — raw scale at the bottom, semantic names at the top.

**Dark mode is paired, not inverted.** Inverting a palette produces a dark mode that feels wrong because not every color pair inverts cleanly. The agent maps each light-mode semantic token to a hand-tuned dark-mode counterpart. A surface that's `zinc-50` in light might pair to `zinc-900` in dark, but the accent that's `blue-600` in light pairs to `blue-400` in dark, not `blue-50`. Every pairing is explicit; nothing is computed.

**Anti-token-sprawl.** If two tokens differ by less than 5% in value, they're collapsed into one. The agent does not ship `space-md-1` and `space-md-2`. The agent does not ship `color-text-primary` and `color-text-default` — those are the same thing.

**Contrast pairs are WCAG-compliant.** Every text-on-background pair in the token system meets 4.5:1 (AA for normal text) or 3:1 (AA for large text and UI components). The agent runs the contrast math during token design and surfaces any pair that fails — and either adjusts the value or marks the pair as "use only for decorative" with a note.

**RTL changes more than direction.** In RTL locales, the agent flips spacing patterns (a card that has `padding-inline-start: 24px` and `padding-inline-end: 16px` in LTR keeps the same logical inline values but reads visually mirrored). Type pairings also shift — some Western fonts don't have Arabic glyphs and the system pairs them with an Arabic-only fallback (e.g., `IBM Plex Sans Arabic` for body, `Tajawal` for display).

**Component contracts cover four states.** Every component contract defines rest, hover, focus, and active/pressed (or selected, depending on the component). Disabled is a fifth state, separate from the four interactive ones. Loading is a sixth, for any component that can fetch.

**Stack-appropriate output.** Tailwind: tokens land in `tailwind.config.js`. CSS variables: tokens land in `:root` and `[data-theme="dark"]`. Styled Components / Stitches: tokens land in the theme object. Blade + Tailwind: same as Tailwind plus a Blade-specific theme switcher pattern.

### Failure modes the dispatching command watches for

- **Tokens exposed as raw values** — the calling command checks the foundation docs. If `color-zinc-950` appears in any component contract instead of a semantic name, re-dispatches.
- **Dark mode is computed, not paired** — the calling command checks the dark-mode pairings doc. If pairings are missing or labeled as "inverted from light," re-dispatches.
- **Failing contrast pairs** — the calling command spot-checks one critical pair. If it fails, re-dispatches with the WCAG requirement explicit.
- **No RTL handling on multi-locale** — if the locale scope includes Arabic and the foundation docs don't mention RTL, re-dispatches.

### Real example

```
Calling command: /ux-system
Brief: creator-tools SaaS, no existing brand, audience: independent
       designers and small studios, market: global with strong Arabic
       presence
Stack: Vue 3 + Tailwind
Theme scope: light + dark
Locale scope: English + Arabic
```

Design-system-architect returns: `design-system/tokens/raw.json` (the bottom layer — color scales, type scale, space scale), `design-system/tokens/semantic.json` (the top layer — `color-bg-primary`, `text-heading-1`, `space-md`, etc.), `design-system/tailwind.config.js` (consumes the semantic layer), 8 foundation docs (`color.md`, `typography.md`, `spacing.md`, `motion.md`, `radius.md`, `shadow.md`, `layout.md`, `rtl.md`), 7 component contracts (`button.md`, `input.md`, `modal.md`, `card.md`, `table.md`, `nav.md`, `toast.md` — each with rest/hover/focus/active/disabled/loading), `design-system/dark-mode-pairings.md` (47 paired tokens), and `design-system/theme-switcher.vue` (the runtime swap pattern). Self-review: semantic naming chose 23 tokens at the semantic layer mapping to 81 raw values, collapsed three near-duplicates (`color-text-default` / `color-text-body` / `color-text-primary` all became `color-text-primary`), and the dark-mode accent needed manual tuning because `blue-600 → blue-400` produced insufficient contrast on dark surfaces — settled on `blue-450` with a manual hex value.

---

## How sub-agents work together

A generation command can dispatch multiple sub-agents in parallel. The most common pattern is `/ux-design` dispatching frontend-engineer + motion-engineer + copy-writer for a single landing page — frontend-engineer builds the layout, motion-engineer wires the hero animation, copy-writer writes the headline and body strings. The calling command merges the output into a coherent deliverable.

When sub-agents work on the same file, the calling command serializes them — frontend-engineer first (lays down the structure), then motion-engineer (adds motion to the structure), then copy-writer (fills in the strings). The calling command uses race-safe pathspec commits so concurrent edits to different files don't collide.

A sub-agent never dispatches another sub-agent. Only commands dispatch sub-agents. This keeps the dispatch graph flat and debuggable.

---

**See also**: [Installation](Installation) · [Discovery Protocol](Discovery-Protocol) · [All 17 Commands](All-17-Commands)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
