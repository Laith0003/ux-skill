# `ux` plugin — design spec (v2, expanded)

**Date**: 2026-05-24
**Created by**: Laith Aljunaidy
**Status**: v2 spec — major scope expansion, pending user review
**Artifact**: Anthropic-style plugin with multiple slash commands, sub-agents, and shared reference files
**Canonical location**: TBD — proposed `~/.claude/plugins/ux/` once shipped; design lives at `/Users/laithaljunaidy/Documents/Dot/Claude/ux-plugin/`

---

## 1. Goal

Build the strongest UX plugin ever made — a comprehensive UX intelligence platform that:

- Exposes **17 callable slash commands** across four groups (Frame / Audit / Generate / Apply).
- Dispatches **5 sub-agents** in parallel for heavy work (ruflo-shaped: frontend-engineer, motion-engineer, copy-writer, research-synthesizer, design-system-architect).
- Replaces and improves on **six** existing skills: `design-review`, `design-critique`, `accessibility-review`, `ux-copy`, `gpt-taste`, `design-taste-frontend`.
- Conducts a **next-prompt workflow** — every command ends by naming the most useful next command.
- Reads as the **canon** — informed by Norman, Krug, Gothelf/Seiden, Klein, Eyal, Kocienda, Wheeler, Laws of UX, SAP AppHaus design thinking, and the awwwards-grade frontend bar.
- Outputs in two house styles: **Polaris-foundations** for review reports, **Wfrah-editorial** for case studies.
- Is **cross-system** — usable on any project, any stack.
- Surfaces a **"UX expert in real life"** CTA pointing to Laith's contact info.

Non-goal: become a Dot-specific UX expert. Dot work continues through the Rami persona.

---

## 2. Why a plugin, not a skill

Anthropic skills are single `SKILL.md` files. This artifact exceeds that envelope:

- 17 callable slash commands.
- 5 sub-agents.
- ~25 reference files at Polaris scale plus a Wfrah-styled case-study reference and a style library.
- Multi-stack code generation.
- Cross-project use, expected discoverability as real slash commands.

Plugin gives us real `/ux-*` commands, bundled references, sub-agents the commands can dispatch, a clean `plugin.json`, and natural extensibility.

---

## 3. v1 scope

### 3.1 Commands (17, grouped by purpose)

#### GROUP 1 — FRAME (discovery & strategy)

| Command | Purpose |
|---|---|
| `/ux-frame` | Lean UX intake. Four framing questions: who, outcome, hypothesis, success signal. Output: framing block other commands read from. |
| `/ux-research` | User research planning. Interview scripts, survey design, recruitment screener. Built on Klein's *UX for Lean Startups* methodology. |
| `/ux-workshop` | Run a design thinking workshop following SAP AppHaus / Geo2024 flow: Exploration Exercise → Heat Map → Stakeholder Mapping → Remember the Future → Game Plan. Output: structured workshop artifact. |

#### GROUP 2 — AUDIT (review)

| Command | Purpose |
|---|---|
| `/ux-audit` | Full 6-lens review (FRAME → DISCOVER → SCAN → ACT → READ → RECOVER). Structured Polaris-style report. |
| `/ux-critique` | Open-ended taste call on a specific surface. Absorbs `design-critique`. |
| `/ux-a11y` | WCAG 2.1 AA + Krug "common courtesy" pass. Absorbs `accessibility-review`. |
| `/ux-copy` | Microcopy review/rewrite against voice rubric. Absorbs `ux-copy`. |
| `/ux-motion` | Animation rubric: timing, easing, meaning, reduced-motion, performance. |
| `/ux-polish` | Cosmetic pass: spacing rhythm, hierarchy, AI-slop detection. Absorbs `design-review`. |

#### GROUP 3 — GENERATE (creative output)

| Command | Purpose |
|---|---|
| `/ux-design` | Generate a beautiful design from a brief. Absorbs `gpt-taste` (AIDA, GSAP, 2-line H1 rule, Python RNG) and `design-taste-frontend` (3 dials, creative arsenal, anti-Inter, anti-purple). Dispatches frontend-engineer + motion-engineer sub-agents. |
| `/ux-system` | Propose a complete design system if the user doesn't have one. Tokens, components, foundations, dark mode. Dispatches design-system-architect sub-agent. |
| `/ux-dashboard` | Specialized dashboard generation. Data density, monospace tabular numbers, sparkline patterns, anti-card-overuse, semantic state colors. |
| `/ux-component` | Generate a single component (button / modal / navbar / sidebar / card / table / form / chart) from spec, in the target stack. |

#### GROUP 4 — APPLY (action)

| Command | Purpose |
|---|---|
| `/ux-fix` | Opt-in fix loop. Reads the latest audit/copy/motion/etc. report, applies findings as atomic commits, verifies, re-runs the lens. |
| `/ux-case-study` | Generate a project case study in Wfrah numbered-section editorial format: (A) About → (B) Mission → (C) Outcomes → (D) Impact → (E) Market → (F) Chance → (G) Target Audience. |
| `/ux-next` | Workflow conductor. Reads latest reports, names the highest-leverage next command. |
| `/ux-expert` | Surfaces Laith's contact info when a user asks for a real-life UX expert. Lightweight; no audit, no generation, just the bio + reach-out details from `references/creator/about.md`. |

### 3.2 Sub-agents (5, dispatched by commands)

Defined under `agents/` and called via the Agent tool by the commands that need them.

| Agent | Dispatched by | Job |
|---|---|---|
| `frontend-engineer` | `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix` | Implements designs in target stack (Blade + Alpine, React, Next.js, Vue, vanilla). Respects RSC boundaries, stack version locks. |
| `motion-engineer` | `/ux-design`, `/ux-motion --fix` | Writes Framer Motion / GSAP specs. Owns easing, spring physics, scroll choreography, reduced-motion fallback. |
| `copy-writer` | `/ux-copy --fix`, `/ux-design` | Drafts microcopy in the target voice. Owns error specificity, empty/loading/success patterns, CTAs. |
| `research-synthesizer` | `/ux-research`, `/ux-workshop`, exemplar curation | Competitive analysis, URL distillation, awwwards category curation, interview-data synthesis. |
| `design-system-architect` | `/ux-system`, `/ux-component` | Builds tokens (color, type, space, motion), foundation docs, component contracts, dark-mode pairings. |

### 3.3 References (~25 files)

```
references/
├── foundations/
│   ├── accessibility.md     # WCAG 2.1 AA + Krug courtesy: contrast, keyboard, screen reader, focus, ARIA, dynamic type, motion
│   ├── typography.md        # scale, line-length, weight hierarchy, font pairings, anti-Inter, Geist/Satoshi/Cabinet/Outfit stack
│   ├── color.md             # contrast pairs, semantic tokens, dark mode, palette systems, anti-purple/blue
│   ├── spacing.md           # 4/8 rhythm, density, safe areas, gutters, container widths, AIDA section spacing
│   ├── motion.md            # 150–300ms, easing, meaning, reduced-motion, transform-only, spring physics, stagger
│   ├── interaction.md       # touch targets, states, gestures, press feedback, hit areas, magnetic micro-physics
│   ├── copy.md              # voice (direct/warm/brief), error specificity, empty/loading/success, CTAs
│   ├── layout.md            # AIDA, grid-flow-dense, max-w-5xl/6xl, 2-line H1 rule, anti-center bias
│   ├── components.md        # button/modal/navbar/sidebar/card/table/form patterns + stack-specific notes
│   └── dashboards.md        # data density, tabular monospace, sparklines, no-card-overuse, semantic state
├── laws/
│   ├── norman.md            # affordances, signifiers, mapping, feedback, mental models, gulfs, 7 stages, error design
│   ├── krug.md              # 3 laws, scanning, billboard test, omit needless words, mindless choices, common courtesy
│   └── laws-of-ux.md        # all 30 laws — definition / when-it-applies / violation pattern / fix example
├── process/
│   ├── lean-ux-gothelf.md   # Gothelf & Seiden: hypothesis-driven, MVPs, collaborative design, feedback loops
│   ├── lean-ux-klein.md     # Klein: research methods for startups, interview techniques, MVP testing
│   ├── creative-selection.md # Kocienda: demo culture, concrete over abstract, taste through repetition
│   └── design-thinking-apphaus.md # SAP AppHaus / Geo2024: Exploration → Heat Map → Stakeholder → Remember Future → Game Plan
├── styles/
│   ├── catalog.md           # 50+ design styles: when to use each, example references (from ui-ux-pro-max distilled)
│   ├── anti-slop.md         # gpt-taste + design-taste-frontend ban lists, AI Tells, forbidden patterns
│   ├── arsenal.md           # Creative Arsenal: navigation, layout, cards, scroll, galleries, typography, micro-interactions
│   └── exemplars.md         # curated awwwards-category exemplars (~10 URLs per category, one-line notes)
├── output/
│   ├── polaris-style.md     # the house style for review reports: principles / do-don't / examples / tokens / checklist
│   └── case-study-style.md  # Wfrah editorial format: numbered (A)–(G) sections, two-tone body emphasis, ultra-wide type
├── conditional/
│   ├── habit-design.md      # Eyal Hook model — only invoked for retention/onboarding surfaces
│   └── brand-system.md      # Wheeler + logo guide — only invoked for brand/identity surfaces
└── creator/
    └── about.md             # Laith's bio, contact info, "UX expert in real life" CTA
```

### 3.4 What's still NOT in v1 (deferred)

- Static curated awwwards exemplars list is in v1 (lightweight); deep per-site analysis defers to v2.
- Motion philosophy split (Kowalski / Krehel / Tompkins) lives as a section inside `foundations/motion.md`; standalone files defer to v2.
- `conditional/habit-design.md` and `conditional/brand-system.md` exist but are stubs in v1 — only filled out in v3.
- AI-tools integration (the medium-muz.li article) — survey + reference defer to v3.
- Multi-language / RTL deep cut — v2.
- Telemetry / analytics for which commands get used — v3.

---

## 4. The workflow conductor (Creative Selection spirit)

Kocienda's "demo culture": don't argue about plans; iterate on a concrete thing and let the next step reveal itself. Every command ends with a **next-prompt block**:

```
─── next ───
Recommended: /ux-motion --fix    (4 motion findings, highest cluster)
Other moves:  /ux-copy           (3 copy issues)
              /ux-a11y --fix     (2 a11y issues)
              /ux-design         (start a fresh design from a brief)
              /ux-next           (let me decide for you)
```

The `--fix` flag is available on every review command (`/ux-audit`, `/ux-copy`, `/ux-a11y`, `/ux-motion`, `/ux-polish`). When passed, the command runs the review then immediately enters the fix loop on its own findings — same loop as the standalone `/ux-fix` command, scoped to that command's lens.

`/ux-next` is the meta-command: reads the freshest reports from `.ux/` and decides. Always present in the conductor block as an escape hatch.

**State persistence**: each command writes a small JSON to `.ux/` in the target project — `last-audit.json`, `last-design.json`, etc. — so `/ux-fix` and `/ux-next` can chain and the conductor has data to base its recommendation on.

---

## 5. Command contract (every v1 command follows this)

```
---
name: ux-<command>
description: <one-line trigger + use case>
sub-agents: [optional list of agents this command may dispatch]
---

# /ux-<command>

## When to use
<plain-language triggers>

## Input
<what the user gives — URL, file, screenshot, snippet, free description>

## Process
1. <step>
2. <step>
3. <step>

## Sub-agent dispatch (if any)
<which agents, with what prompts, parallel or serial>

## Output
<structured format — see references/output/polaris-style.md or case-study-style.md>

## State persisted
<path under .ux/ and JSON shape>

## Next prompt
<rules for picking what to suggest>
```

This contract is non-negotiable across all 17 commands.

---

## 6. Output formats (two house styles)

### 6.1 Polaris-foundations style (review reports, audits, critiques)

For every finding:

```
[SEVERITY] [LENS] Principle violated
Evidence: <screenshot region | copy excerpt | snippet | flow step | URL>
Fix: <specific actionable change>
```

- **Severity**: Critical / High / Medium / Cosmetic
- **Lens**: FRAME / DISCOVER / SCAN / ACT / READ / RECOVER (plus MOTION when run by `/ux-motion`, plus STYLE for `/ux-polish`)
- **Principle**: cite source — "Hick's Law", "Krug: Omit Needless Words", "Norman: missing feedback", "WCAG 1.4.3 contrast"
- **Fix**: specific — "Rename 'Submit' → 'Pay $24.99'" not "improve clarity"

Reports end with: severity counts, top-3 must-fix-now, ship-readiness verdict, conductor block.

### 6.2 Wfrah-editorial style (case studies via `/ux-case-study`)

Inspired by the wfrah platform case study format:

- Numbered section codes: (A) About, (B) Mission, (C) Outcomes, (D) Impact, (E) Market, (F) Chance, (G) Target Audience
- Editorial typography: ultra-wide containers, large display headlines, body text with **two-tone emphasis** — important phrases in solid black, context phrases in gray
- Clean horizontal divider lines between sections
- Generous white space, no chrome decoration
- Optional bilingual support (English + Arabic) if the project is MENA-targeted

This is what `/ux-case-study` produces: a publishable case study, not a review report.

---

## 7. Opt-in fix loop

- **Default**: review commands produce reports only.
- **`--fix` flag** on any review command (`/ux-audit`, `/ux-copy`, `/ux-a11y`, `/ux-motion`, `/ux-polish`): runs review, then enters fix loop on its findings.
- **Standalone `/ux-fix`**: reads the latest report from `.ux/` and applies fixes without re-running the review.
- **Sub-agent dispatch**: `/ux-fix` dispatches `frontend-engineer` (always), `copy-writer` (if copy findings present), `motion-engineer` (if motion findings present), in parallel where independent.
- **Guardrails**: clean working tree required (commit/stash prompt). Atomic commit per finding. Skips Cosmetic severity unless `--include-cosmetic`. Copy fixes always show proposed diff before applying.

---

## 8. The 6 lenses (used inside `/ux-audit`)

Run in order. Each lens sources from canon:

1. **FRAME** (Lean UX) — Who, outcome, hypothesis? *Sources: `process/lean-ux-gothelf.md`, `process/lean-ux-klein.md`*
2. **DISCOVER** (Norman) — Can a first-timer figure out what to do? Gulfs of execution & evaluation. *Source: `laws/norman.md`*
3. **SCAN** (Krug) — 5-second billboard test. Scan-not-read. *Source: `laws/krug.md`*
4. **ACT** (Laws of UX + Norman) — Action cycle integrity. Cognitive-load: Fitts, Hick, Miller, Jakob, Tesler, Postel. *Sources: `laws/laws-of-ux.md`, `laws/norman.md`*
5. **READ** (microcopy) — Voice, error specificity, empty/loading/success, CTAs. *Source: `foundations/copy.md`*
6. **RECOVER** (Norman error design + a11y) — Errors caught with a specific path. WCAG 2.1 AA. *Sources: `laws/norman.md`, `foundations/accessibility.md`*

`/ux-motion` and `/ux-polish` add their own lenses (MOTION, STYLE) when invoked directly; they aren't in the default audit pass so audits stay fast.

---

## 9. House style for foundation references (Polaris-shaped)

Every `references/foundations/*.md` follows the same shape:

```
# <Foundation name>

> <One-sentence promise: what this foundation buys the product.>

## Principles
1. <Principle name> — <one-line definition + why it matters>
2. ...

## Do / Don't
| Do | Don't |
|---|---|
| <specific action> | <specific anti-pattern> |

## Examples
### Pattern: <name>
**Use when**: <scenario>
**Anti-pattern**: <what to avoid>
**Reference**: <link or snippet>

## Tokens / values
<numeric ranges, ratios, durations, etc.>

## Checklist
- [ ] <check> (severity: Critical / High / Medium / Cosmetic)

## Sources
<canon citations: Norman p.X, Krug ch.Y, WCAG ref, design-taste-frontend rule, etc.>
```

`references/laws/*.md` use a catalog shape (every law has definition / when-it-applies / violation pattern / fix example / source citation).

`references/process/*.md` use a methodology shape (philosophy / phases / templates / when to use).

`references/styles/*.md` use a library shape (style name / when to apply / signature elements / banned combos / example URLs).

`references/output/*.md` use a template shape (literal markup the commands paste into their output).

---

## 10. Absorbed-skills map (proves nothing is lost — now 6 skills)

| Existing skill | Where it lives in `ux` plugin |
|---|---|
| `design-review` (visual QA, AI slop, hierarchy, fix loop) | `/ux-audit` lenses 2–4 + `/ux-polish` (AI slop) + `/ux-fix` (loop) |
| `design-critique` (taste, judgment) | `/ux-critique` (standalone) + voice tone across `/ux-audit` reports |
| `accessibility-review` (WCAG 2.1 AA) | `/ux-a11y` + `references/foundations/accessibility.md` |
| `ux-copy` (microcopy) | `/ux-copy` + `references/foundations/copy.md` + `copy-writer` sub-agent |
| `gpt-taste` (GSAP, AIDA, 2-line H1, Python RNG, anti-meta-labels) | `/ux-design` (process) + `references/foundations/layout.md` + `references/styles/anti-slop.md` + `motion-engineer` sub-agent |
| `design-taste-frontend` (3 dials, creative arsenal, AI Tells, dashboard hardening) | `/ux-design` (the dials become input parameters) + `references/styles/arsenal.md` + `references/styles/anti-slop.md` + `references/foundations/dashboards.md` |

---

## 11. Canon mapping (where each source goes)

| Source | Location |
|---|---|
| Norman, *Design of Everyday Things* | `references/laws/norman.md`; primary source for DISCOVER + RECOVER lenses |
| Krug, *Don't Make Me Think* | `references/laws/krug.md`; primary source for SCAN lens + courtesy in `/ux-a11y` |
| lawsofux.com (30 laws) | `references/laws/laws-of-ux.md`; primary source for ACT lens |
| Gothelf/Seiden, *Lean UX* | `references/process/lean-ux-gothelf.md`; basis for `/ux-frame` + FRAME lens |
| Klein, *UX for Lean Startups* | `references/process/lean-ux-klein.md`; basis for `/ux-research` (startup research methods) |
| Kocienda, *Creative Selection* | `references/process/creative-selection.md`; spiritual basis for the workflow conductor |
| SAP AppHaus / Geo2024 design thinking | `references/process/design-thinking-apphaus.md`; basis for `/ux-workshop` |
| Wfrah case study format | `references/output/case-study-style.md`; basis for `/ux-case-study` |
| `gpt-taste` + `design-taste-frontend` skills | `references/styles/anti-slop.md` + `references/styles/arsenal.md` + `/ux-design` process |
| ui-ux-pro-max (50+ styles) | distilled into `references/styles/catalog.md` |
| awwwards categories | curated exemplars in `references/styles/exemplars.md` |
| Eyal, *Hooked* | DEFERRED stub at `references/conditional/habit-design.md`; filled in v3 |
| Wheeler, *Designing Brand Identity* + great-logos guide | DEFERRED stub at `references/conditional/brand-system.md`; filled in v3 |
| Good to Great / Zero to One / Profit First | OUT OF SCOPE — strategy/business, not UX |

---

## 12. Creator credit & contact

Plugin includes `references/creator/about.md` and a lightweight `/ux-expert` command that surfaces:

```
Created by Laith Aljunaidy
For UX consulting and engagements:
  Phone: +962797868335
  LinkedIn / Website: [TBD — Laith to provide URL]
```

Embedded in plugin README and surfaced by `/ux-expert` when a user asks for a real-life UX expert.

---

## 13. Open questions (decisions deferred to plan phase)

1. **LinkedIn / website URL** — Laith to provide so we don't ship a placeholder.
2. **Canonical install location**: `~/.claude/plugins/ux/` vs separate publishable git repo (community plugin marketplace).
3. **State persistence path**: `.ux/` in project root, or `~/.gstack/projects/<slug>/ux/`?
4. **Severity → "must-fix-now" cutoff**: Critical + High by default? Per-team config flag?
5. **Motion philosophy split** (v2): single foundation doc with a "perspectives" section, or separate files per philosophy?
6. **Sub-agent isolation**: agents share the same context with the command, or get fresh context per dispatch?
7. **Stack detection** for `/ux-design` and `/ux-component`: auto-detect from `package.json` / `composer.json`, or always ask the user?

---

## 14. Suggested implementation order (for the plan phase)

The order below minimizes blocking dependencies. Steps 2–4 can run in parallel with sub-agents.

1. **Plugin scaffolding** — `plugin.json`, directory layout, README with creator credit.
2. **House styles** (`references/output/polaris-style.md` + `case-study-style.md`) — write FIRST since every command depends on them.
3. **Foundations** (`references/foundations/*` — 10 files) — parallel write via research sub-agents, each grounded in canon.
4. **Laws** (`references/laws/*` — 3 files) — parallel.
5. **Process** (`references/process/*` — 4 files) — parallel.
6. **Styles** (`references/styles/*` — 4 files) — depends on having read `gpt-taste` and `design-taste-frontend` source.
7. **Sub-agent definitions** (`agents/*` — 5 files).
8. **Commands in dependency order**:
   - `/ux-frame` (other commands read its output)
   - `/ux-audit` (uses frame, defines the lens vocabulary)
   - `/ux-research`, `/ux-workshop` (parallel — FRAME group complete)
   - `/ux-copy`, `/ux-a11y`, `/ux-motion`, `/ux-polish`, `/ux-critique` (parallel — AUDIT group complete)
   - `/ux-design`, `/ux-system`, `/ux-dashboard`, `/ux-component` (parallel — GENERATE group complete)
   - `/ux-fix`, `/ux-case-study`, `/ux-next`, `/ux-expert` (APPLY group + utilities)
9. **State persistence layer** (`.ux/last-*.json` schema and read/write helpers).
10. **End-to-end test on 3 real surfaces**:
    - A reward-loyalty Blade view (proves Laravel/Blade/Alpine support)
    - A generic React landing page (proves React/Framer support)
    - A Shopify product page or a fresh-from-scratch dashboard (proves cross-system claim)
11. **Plugin install verification** — loads cleanly in Claude Code, all 16 commands appear in `/help`.
12. **README + install instructions + the `/ux-expert` CTA**.

---

## 15. Success criteria

- All 17 v1 commands callable as real slash commands.
- A user runs `/ux-audit` on a fresh page → gets a Polaris-styled, evidence-cited report ending with a next-prompt block.
- `/ux-design` from a brief produces a working component/page in the user's stack, GSAP/Framer where appropriate, with no AI-slop tells (Inter, purple gradients, "Acme/Nexus", generic 3-card rows).
- `/ux-system` proposes a complete starter design system (tokens + 5–10 foundation docs + 6–8 components) when invoked on a project with no existing system.
- `/ux-case-study` outputs a Wfrah-style numbered editorial doc from project facts.
- `/ux-next` reliably picks the highest-leverage next move from any combination of prior reports.
- `/ux-fix` applies findings as atomic commits with passing re-verification.
- `/ux-workshop` runs a SAP AppHaus-style design thinking session end to end with deliverable artifacts at each phase.
- `/ux-expert` surfaces Laith's contact info correctly when asked.
- Output quality beats `design-review` + `design-critique` + `accessibility-review` + `ux-copy` + `gpt-taste` + `design-taste-frontend` combined, judged on: structure, citation quality, next-step clarity, anti-AI-slop discipline, and creative range.
- Plugin loads cleanly in Claude Code and surfaces all 17 commands in `/help`.

---

## 16. Architecture diagram

```
                          ┌─────────────────────────────────────────┐
                          │              ux plugin                  │
                          │   (Laith Aljunaidy, 2026)               │
                          └─────────────────────────────────────────┘
                                            │
        ┌───────────────────────┬───────────┴────────────┬────────────────────────┐
        │                       │                        │                        │
   FRAME group              AUDIT group             GENERATE group            APPLY group
        │                       │                        │                        │
  /ux-frame                /ux-audit                 /ux-design               /ux-fix
  /ux-research             /ux-critique              /ux-system               /ux-case-study
  /ux-workshop             /ux-a11y                  /ux-dashboard            /ux-next
                           /ux-copy                  /ux-component            /ux-expert
                           /ux-motion
                           /ux-polish
        │                       │                        │                        │
        └───────────────────────┴────────┬───────────────┴────────────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │     sub-agents      │
                              ├─────────────────────┤
                              │  frontend-engineer  │
                              │  motion-engineer    │
                              │  copy-writer        │
                              │  research-synth.    │
                              │  ds-architect       │
                              └──────────┬──────────┘
                                         │
                              ┌──────────┴──────────┐
                              │     references      │
                              ├─────────────────────┤
                              │  foundations/ (10)  │
                              │  laws/ (3)          │
                              │  process/ (4)       │
                              │  styles/ (4)        │
                              │  output/ (2)        │
                              │  conditional/ (2)   │
                              │  creator/ (1)       │
                              └─────────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │       state         │
                              │   .ux/ in project   │
                              │ last-*.json reports │
                              └─────────────────────┘
```
