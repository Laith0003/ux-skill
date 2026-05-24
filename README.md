# ux — the design intelligence plugin for Claude Code

> 18 callable slash commands. 5 specialized sub-agents. 35+ reference files. 26,000+ lines of curated UX guidance plus a deterministic regex linter. Built to produce premium frontend work directly inside Claude Code — and to defeat the AI-aesthetic fingerprints that mark output as machine-generated.
>
> **v1.4 — 72-brand library absorbed.** Built-in design specs for Apple, Stripe, Linear, Notion, Claude, Figma, Spotify, Tesla, BMW, Ferrari, Coinbase, Airbnb, Shopify, Vercel, Supabase and 57 more. When a user says "build me a landing in Stripe's style" the plugin reads the full brand DESIGN.md and produces output that matches the brand's design language — not a generic default. See `references/brands/_index.md`.
>
> **v1.5 — Deterministic linter**. `/ux-lint` runs 30 regex-based anti-pattern checks against your codebase. No LLM, no API key, no network — runs in milliseconds. CI-friendly: exits non-zero on Critical / High findings. Wire it into pre-commit hooks or CI for a hard floor against AI fingerprints. See `references/foundations/anti-patterns.md`.
>
> **v1.2 — SEO foundation baked in.** Every public-web output now ships with the full head surface, Open Graph + Twitter cards, JSON-LD structured data per page type, semantic HTML, CWV-passing performance contract, robots + sitemap. SEO is not bolted on; it's a foundation like accessibility. See `references/foundations/seo.md`.
>
> **v1.1 — Discovery protocol enforced.** Every generation command runs a mandatory 10-field intake before producing anything: brand identity, references, audience, style, voice, stack, imagery, must-have patterns, avoid-list, and the wow moment. Improvisation is banned. The plugin asks before it builds.

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Brands](https://img.shields.io/badge/brands-72-cc785c.svg)](https://github.com/Laith0003/ux-skill/blob/main/references/brands/_index.md)
[![Linter](https://img.shields.io/badge/lint-deterministic_(no_LLM)-2563EB.svg)](https://github.com/Laith0003/ux-skill/blob/main/commands/ux-lint.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Commands](https://img.shields.io/badge/commands-18-blueviolet)](#the-17-commands)
[![Sub-Agents](https://img.shields.io/badge/sub--agents-5-green)](#the-5-sub-agents)
[![References](https://img.shields.io/badge/references-30%2B-orange)](#references)
[![Guidance](https://img.shields.io/badge/guidance-19%2C000%2B_lines-red)](#references)
[![Claude Code](https://img.shields.io/badge/claude--code-plugin-7C3AED)](https://docs.anthropic.com/en/docs/claude-code)
[![Stacks](https://img.shields.io/badge/stacks-React%20%7C%20Next%20%7C%20Vue%20%7C%20Blade%20%7C%20Vanilla-lightgrey)](#supported-stacks)

The `ux` plugin replaces six existing skills (`design-review`, `design-critique`, `accessibility-review`, `ux-copy`, `gpt-taste`, `design-taste-frontend`) and adds the parts they were missing: a complete generation workflow, real sub-agent dispatch, a Polaris-style foundations library, and a workflow conductor that names the most useful next prompt after every command.

---

## Why this exists

Default model output has measurable, predictable failure modes. Inter font on every brief. Purple-to-blue gradients on white. Three equal cards in a row. Centered hero over a dark image. "John Doe", "Acme", `99.99%`. Decorative animation with no meaning. Pure black `#000000`. Generic CTAs ("Click here"). Marketing filler verbs ("Elevate", "Seamless", "Unleash").

These aren't preferences. They're **fingerprints**. Every one of them is in `references/styles/anti-slop.md` with a specific "do instead" pair. Every command in this plugin reads that file before it produces output.

The bar is what the best premium SaaS sites actually do — studied directly, codified as native guidance.

---

## What's in v1.0

### The 17 commands

```
FRAME       /ux-frame       Lean-UX intake — audience, outcome, hypothesis, success signal
            /ux-research    User-research planning — interviews, surveys, screeners
            /ux-workshop    Design-thinking workshop — Exploration → Heat Map → Stakeholder
                            → Remember the Future → Game Plan

AUDIT       /ux-audit       Full 6-lens review (FRAME → DISCOVER → SCAN → ACT → READ → RECOVER)
            /ux-critique    Open-ended taste call — 3 wins + 3 misses + 1 strategic move
            /ux-a11y        WCAG 2.1 AA + Krug-courtesy accessibility audit
            /ux-copy        Microcopy review against the voice rubric
            /ux-motion      Animation timing, easing, meaning, reduced-motion, performance
            /ux-polish      Cosmetic pass — spacing rhythm, hierarchy, AI-slop detection

GENERATE    /ux-design      Generate a beautiful design from a brief (dispatches frontend-engineer)
            /ux-system      Propose a complete design system if the project doesn't have one
            /ux-dashboard   Specialized dashboard generation — bento, tabular monospace, sparklines
            /ux-component   Generate a single component in the target stack

APPLY       /ux-fix         Opt-in fix loop — applies findings from the latest report as commits
            /ux-case-study  Generate a Wfrah-style numbered editorial case study
            /ux-next        Workflow conductor — names the highest-leverage next command
            /ux-expert      Surface real-life UX consulting contact
```

Every review command takes `--fix` to chain into the fix loop directly.

### The 5 sub-agents

```
frontend-engineer        Implements designs in target stack (React, Next.js, Vue, Blade, vanilla)
motion-engineer          Owns easing, spring physics, scroll choreography, reduced-motion
copy-writer              Drafts microcopy in the project's voice
research-synthesizer     Digests interview data, analytics, competitive sites, A/B results
design-system-architect  Builds tokens, foundation docs, component contracts, dark-mode pairings
```

Commands dispatch sub-agents in parallel where work is independent.

### 30+ reference files

```
foundations/            10 Polaris-shaped foundation systems — 4,126 lines
  ├── accessibility.md     WCAG 2.1 AA, keyboard, screen reader, motion preferences
  ├── color.md             Contrast pairs, semantic tokens, dark-mode pairings, palettes
  ├── components.md        Canonical button / input / modal / card / table / navbar contracts
  ├── copy.md              Voice, error specificity, empty / loading / success patterns
  ├── dashboards.md        Data density, tabular monospace, the 5 dashboard archetypes
  ├── interaction.md       Touch targets, gestures, press feedback, magnetic micro-physics
  ├── layout.md            AIDA, grid-flow-dense, max-widths, 2-line H1 rule, asymmetric
  ├── motion.md            150-300ms, easing, meaning, reduced-motion, spring physics
  ├── spacing.md           4/8 rhythm, density modes, safe areas, gutters
  └── typography.md        Scale, line-length, weight hierarchy, font pairings

laws/                   Canonical UX principles — 2,546 lines
  ├── norman.md            Affordances, signifiers, mapping, feedback, gulfs, 7 stages
  ├── krug.md              3 laws of usability, billboard test, scan-not-read, courtesy
  └── laws-of-ux.md        30 cognitive laws (Fitts, Hick, Miller, Jakob, Tesler, Postel...)

process/                Methodologies — 1,873 lines
  ├── lean-ux-gothelf.md   Hypothesis-driven design, MVPs, design studio, feedback loops
  ├── lean-ux-klein.md     Startup research methods — interviews, surveys, MVP testing
  ├── creative-selection.md  Demo culture — iterate on a thing, not a plan
  ├── design-thinking-apphaus.md  5-phase workshop methodology
  ├── generation-modes.md  Direct / shotgun-variant / consultation — when to use each
  ├── visual-translation.md  Image → code methodology
  └── refactor-existing.md   How to redesign without breaking what works

styles/                 Style libraries + the discipline — 3,068 lines
  ├── anti-slop.md         The forbidden patterns — every AI fingerprint with do-instead
  ├── arsenal.md           60+ high-end patterns to reach for
  ├── library.md           Three style systems — industrial, minimalist, high-end visual
  └── exemplars.md         Distilled patterns from 21+ premium SaaS sites

components/             Component pattern library — 1,568 lines
  ├── heroui.md            HeroUI v3 component system reference
  └── library.md           General component pattern library (button, input, modal, etc.)

output/                 House styles for review reports + case studies
  ├── polaris-style.md     Audit / review report format (severity, evidence, fix)
  └── case-study-style.md  Wfrah-style numbered editorial format — pure monochrome

conditional/            v3 expansion stubs
  ├── habit-design.md      Hook model — only invoked for retention surfaces
  └── brand-system.md      Brand identity / logo system — only invoked for brand surfaces

creator/
  └── about.md             Creator credit + real-life UX consulting contact
```

---

## How it works

Every command follows a single contract:

1. **Read the brief** (or extract from `.ux/last-frame.json` written by `/ux-frame`)
2. **Pull the relevant references** (e.g., `/ux-audit` reads all 6 lens references; `/ux-design` reads anti-slop + arsenal)
3. **Dispatch the right sub-agent(s)** in parallel where work is independent
4. **Format output** in the appropriate house style (`polaris-style.md` for reports, `case-study-style.md` for case studies)
5. **Persist state** to `.ux/last-<command>.json` so downstream commands can chain
6. **End with a next-prompt block** — the workflow conductor names the best next move

The next-prompt block is the difference between a pile of commands and a coherent workflow. Every output ends with something like:

```
─── next ───
Recommended: /ux-motion --fix    (4 motion findings, highest cluster)
Other moves: /ux-copy            (3 copy issues)
             /ux-a11y --fix      (2 a11y issues)
             /ux-design          (start a fresh design from a brief)
             /ux-next            (let me decide)
```

---

## Install

### Recommended — via Claude Code plugin marketplace

Inside any Claude Code session:

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

That's it. All 17 `/ux-*` slash commands and 5 sub-agents are immediately available. Run `/help` to see them.

### Alternative — local clone for development

If you want to hack on the plugin or pin a specific commit:

```bash
git clone https://github.com/Laith0003/ux-skill.git
cd ux-skill
/plugin marketplace add "$(pwd)"
/plugin install ux@ux-skill
```

### Updating

When new versions ship:

```
/plugin marketplace update ux-skill
/plugin update ux
```

### Uninstalling

```
/plugin uninstall ux
/plugin marketplace remove ux-skill
```

---

## Usage

Natural-language prompts work as well as the slash commands. The plugin's commands are designed to read trigger words from the user's message.

### Audit an existing page

```
/ux-audit https://my-product.com/pricing
```

```
review the UX on this landing page
```

Both invoke the same 6-lens audit and end with the next-prompt block.

### Generate a new design

```
/ux-design "a SaaS landing page for a fintech for freelancers, dark mode, asymmetric hero"
```

```
build me a dashboard for live logistics tracking
```

Dispatches `frontend-engineer` (and `motion-engineer` if motion is part of the brief) with `anti-slop.md` and `arsenal.md` embedded in the prompt. Output: complete component or page in the requested stack, with no AI-slop fingerprints, plus a self-review noting which bans were avoided and which arsenal patterns were used.

### Propose a design system

```
/ux-system
```

For a project with no existing system. Dispatches `design-system-architect`. Output: token JSON + 5-10 foundation docs + 6-8 component contracts + dark-mode pairings + theme switcher pattern.

### Fix what the audit found

```
/ux-audit --fix
```

Audits, then enters the fix loop on its own findings. For each finding (severity-sorted): dispatches the right sub-agent, applies the fix, commits atomically, re-runs the lens to verify.

### Generate a case study

```
/ux-case-study
```

Produces a Wfrah-style numbered editorial document — pure monochrome, hairline section separators, ultra-wide editorial typography, two-tone body emphasis. Default sections (A)–(G): About, Mission, Outcomes, Impact, Market, Chance, Target Audience.

### Run a design-thinking workshop

```
/ux-workshop "expanding our product into a new market"
```

Walks through five phases: Exploration → Heat Map → Stakeholder → Remember the Future → Game Plan. Outputs one populated artifact per phase plus a one-page summary.

### Let the conductor decide

```
/ux-next
```

Reads every report in `.ux/` and picks the highest-leverage next command. Always present as an escape hatch at the bottom of every other command's output.

---

## Supported stacks

| Stack | Discipline applied |
|---|---|
| React + Tailwind + Framer Motion | RSC safety, isolated client-component motion, memoized perpetual loops |
| Next.js (App Router) + Tailwind + Framer Motion | RSC vs Client boundaries, `app/` layout discipline |
| Vue + Tailwind + GSAP | Composition API + GSAP isolation |
| Blade + Alpine.js 3 + HTMX + Tailwind 4 | Logical properties for RTL, HTMX boundary discipline |
| Astro + Tailwind | Island architecture + content collections |
| Vanilla HTML/CSS + minimal JS | Static prototypes, design exploration |

Stack auto-detection from `package.json` / `composer.json` when present.

---

## The 6 audit lenses

The default audit (`/ux-audit`) walks every surface through six lenses in order. Each lens is grounded in a specific reference:

| Lens | Question | Source |
|---|---|---|
| **FRAME** | Who is this for, what outcome, what hypothesis? | `process/lean-ux-gothelf.md` |
| **DISCOVER** | Can a first-timer figure out what to do? | `laws/norman.md` |
| **SCAN** | 5-second billboard test — what is this, what should I click? | `laws/krug.md` |
| **ACT** | Action-cycle integrity. Cognitive load (Fitts, Hick, Miller, Jakob). | `laws/laws-of-ux.md` + `norman.md` |
| **READ** | Voice, error specificity, empty / loading / success patterns. | `foundations/copy.md` |
| **RECOVER** | Errors caught with specific paths. WCAG 2.1 AA. Common courtesy. | `laws/norman.md` + `foundations/accessibility.md` |

`/ux-motion` adds a 7th lens (MOTION) when invoked directly. `/ux-polish` adds STYLE.

---

## What's banned

A short selection from `references/styles/anti-slop.md`:

- Inter as the default brand display font (Inter is fine when intentional; never default)
- Purple-to-blue AI gradient on white
- Pure `#000000` (use Zinc-950 / Charcoal / Off-Black)
- Three equal cards in a row ("feature row" cliché)
- Centered hero over dark image (default to asymmetric split)
- `h-screen` on mobile hero (use `min-h-[100dvh]`)
- Animating `width` / `height` / `top` / `left` (transform + opacity only)
- Filler verbs: Elevate, Seamless, Unleash, Next-Gen, Revolutionize
- Placeholder names: John Doe, Sarah Chan
- Fake brands: Acme, Nexus, SmartFlow, Stellar
- Round-number stats: 99.99%, 50%, $1,234
- Unsplash URLs (broken too often; use `picsum.photos/seed/<descriptive-seed>/W/H`)
- Custom mouse cursors (outdated, breaks a11y, kills performance)
- Scroll-progress paths drawn on the side of the page
- Emoji as icons (Google Material Symbols preferred)
- Lucide user-egg avatars (use seeded `picsum.photos` instead)

Every ban has a "do instead" pair. Run `/ux-polish` on any surface to detect them.

---

## What's reached for

A short selection from `references/styles/arsenal.md`:

- Asymmetric split hero (7/5 or 5/7, not centered)
- Editorial column rhythm (text-left / image-right, alternating)
- Bento grid with `grid-flow-dense`
- Floating glass pill nav with backdrop blur
- Button-in-button trailing icon bezel
- Magnetic micro-physics (`useMotionValue` not `useState`)
- Spotlight border cards via `mask-composite: exclude`
- Skeleton shimmer loading states (RTL-aware)
- Thesis-statement hero (massive headline, prose subhead, single CTA)
- The 5 dashboard archetypes (intelligent list, command input, live status, wide data stream, contextual focus)
- AIDA section flow for landings
- Two-tone editorial body emphasis (black + gray)

---

## Anti-fingerprints: the discipline

`/ux-design` and `/ux-component` produce code with a built-in self-review. Every output ends with:

```
──── self-review ────
Anti-slop bans I consciously avoided:
1. [ban] — [what I did instead]
2. ...

Arsenal patterns used:
- [pattern] — in [component/section], because [why]
```

This is the difference between "generate code" and "generate premium code." The discipline is in the prompt.

---

## The Polaris-style report format

Every audit / review output follows the same shape. Per finding:

```
[SEVERITY] [LENS] Principle violated
Evidence: <screenshot region | copy excerpt | snippet | flow step>
Fix: <specific actionable change>
```

- **Severity**: Critical / High / Medium / Cosmetic
- **Principle**: cited by name (e.g., "Hick's Law", "Krug: Omit Needless Words", "WCAG 1.4.3 contrast")
- **Fix**: specific — "Rename 'Submit' → 'Pay $24.99'" not "improve clarity"

Reports end with: severity counts, top-3 must-fix-now, ship-readiness verdict, and the next-prompt block.

---

## Architecture

```
ux-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/                17 slash commands
├── agents/                  5 sub-agents
├── references/
│   ├── foundations/         10 systems (typography, color, spacing, motion, layout,
│   │                        accessibility, interaction, copy, components, dashboards)
│   ├── laws/                3 canon files (norman, krug, laws-of-ux)
│   ├── process/             7 methodology files
│   ├── styles/              4 style files (anti-slop, arsenal, library, exemplars)
│   ├── components/          2 component-library files
│   ├── output/              2 house-style files (polaris-style, case-study-style)
│   ├── conditional/         2 v3 stubs (habit-design, brand-system)
│   └── creator/             about.md
├── bin/
│   └── state.sh             .ux/ state read/write helpers
├── docs/                    design spec
├── LICENSE                  MIT
├── CONTRIBUTING.md
└── README.md
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions that sharpen the discipline are welcome. Contributions that loosen it are not.

---

## Real-life UX consulting

Created by **Laith Aljunaidy**, solo founder of [Dot](https://thedotwallet.com) — a MENA-first loyalty platform. This plugin is his shipped playbook for premium product UI/UX.

For UX consulting, design reviews, or product positioning sessions:

- LinkedIn: [https://www.linkedin.com/in/laithaljunaidy/](https://www.linkedin.com/in/laithaljunaidy/)
- Phone: +962 79 786 8335

---

## License

MIT. See [LICENSE](LICENSE).

---

## Star history

If this plugin helps you ship work you're proud of, a star is the cheapest way to support it.
