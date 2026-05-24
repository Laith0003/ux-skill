# `ux` plugin — design spec

**Date**: 2026-05-24
**Status**: Spec approved by user, pending review before plan handoff
**Owner**: Laith (product) + main Claude Code session (CTO)
**Artifact**: Anthropic-style plugin with multiple slash commands and shared reference files
**Canonical location**: TBD — proposed `~/.claude/plugins/ux/` once shipped; design lives here at `/Users/laithaljunaidy/Documents/Dot/Claude/ux-plugin/`

---

## 1. Goal

Build one comprehensive UX intelligence layer that:

- Replaces and improves on four existing skills: `design-review`, `design-critique`, `accessibility-review`, `ux-copy`.
- Exposes **multiple callable slash commands** for the specific UX tasks people actually do (audit, motion check, copy review, a11y pass, polish, etc.).
- Conducts a **next-prompt workflow** — every command ends by naming the most useful next command for the user's situation.
- Reads as the **canon** — informed by Norman (Design of Everyday Things), Krug (Don't Make Me Think), Lean UX (Gothelf/Seiden), Laws of UX (lawsofux.com), and Kocienda's Creative Selection philosophy.
- Is **cross-system** — usable on any project, not Dot-specific.
- Outputs in a **Polaris foundations** house style: principles → do/don't → examples → tokens → checklist.

Non-goal: be a Dot-specific UX expert. The Dot work continues to flow through the Rami persona; this plugin is the cross-project canon.

---

## 2. Why a plugin, not a skill

Anthropic skills are single `SKILL.md` files loaded on a trigger. What we're building exceeds that envelope:

- Multiple callable commands (8 in v1, more later).
- Shared reference files (~14 in v1) at Polaris-scale.
- Cross-system use, expected discoverability via real slash command names.

The plugin shape gives us: real slash commands (`/ux-audit`), bundled references in `references/`, a clean `plugin.json` manifest, and natural extensibility.

---

## 3. v1 scope

### Commands (8)

| Command | Trigger | What it does |
|---|---|---|
| `/ux-frame` | "frame this product / surface" | Lean UX intake. Asks the four framing questions (who, outcome, hypothesis, success signal). Outputs a framing block other commands read from. |
| `/ux-audit` | "audit ux", "ux review" | Full 6-lens review (FRAME → DISCOVER → SCAN → ACT → READ → RECOVER). Produces a structured report with severity, evidence, and fix-per-finding. Default = report only. |
| `/ux-copy` | "review copy", "fix microcopy" | Microcopy review against the voice rubric: error specificity, empty states, CTAs, loading, success. Produces before/after table. |
| `/ux-a11y` | "accessibility audit", "WCAG check" | WCAG 2.1 AA pass plus Krug's "common courtesy" pass: contrast, keyboard, screen reader, focus, motion preference, ARIA, dynamic type. |
| `/ux-motion` | "motion review", "check animations" | Animation rubric: duration (150–300ms), easing, meaning, reduced-motion compliance, performance (transform/opacity only), state transitions. |
| `/ux-polish` | "polish", "tighten this up" | Cosmetic pass: spacing rhythm, hierarchy, AI-slop detection (Inter everywhere, purple-on-white gradients, generic cards), token consistency. |
| `/ux-fix` | "fix findings", "apply fixes" | Opt-in fix loop. Reads last audit's findings, edits source, commits atomically per fix, verifies, re-runs the relevant lens at end. |
| `/ux-next` | "what should I do next?" | Workflow conductor. Reads the latest audit/copy/motion/etc. results and names the highest-value next command. |

### References (14 files, Polaris foundations IA)

```
references/
├── foundations/
│   ├── accessibility.md     # WCAG 2.1 AA + Krug courtesy: contrast, keyboard, screen reader, focus, motion, ARIA, dynamic type
│   ├── typography.md        # scale, line-length, weight hierarchy, font pairings, anti-AI-slop font choices
│   ├── color.md             # contrast pairs, semantic tokens, dark mode, palette systems
│   ├── spacing.md           # 4/8 rhythm, density, safe areas, gutters, container widths
│   ├── motion.md            # 150–300ms, easing (ease-out enter / ease-in exit), meaningful motion, reduced-motion, transform-only
│   ├── interaction.md       # touch targets (44pt), states, gestures, press feedback, hit areas
│   └── copy.md              # voice (direct/warm/brief), error specificity, empty/loading/success patterns, CTA microcopy
├── laws/
│   ├── norman.md            # affordances, signifiers, mapping, feedback, mental models, gulfs, 7 stages of action, error design
│   ├── krug.md              # 3 laws, scanning, billboard test, omit needless words, mindless choices, common courtesy
│   └── laws-of-ux.md        # all 30 laws — definition / when-it-applies / violation pattern / fix example
├── process/
│   ├── lean-ux.md           # hypothesis-driven framing, MVPs, feedback loops, the 4 framing questions
│   └── creative-selection.md # Kocienda: demo culture, concrete over abstract, iterate on a thing, taste through repetition
└── output/
    └── polaris-style.md     # the house style: section structure, do/don't tables, example blocks, severity, evidence format
```

### What's NOT in v1 (deferred)

- `/ux-critique` (open-ended taste call) — v2
- `/ux-brand` and `references/conditional/brand-system.md` (brand identity, logo) — v3
- `references/conditional/habit-design.md` (Eyal Hook model for retention surfaces) — v3
- `references/exemplars.md` (curated awwwards-category exemplars, 10 per category) — v2
- Motion philosophy split (Kowalski / Krehel / Tompkins) — v2 (lives inside `foundations/motion.md` as a "perspective" sub-section)
- AI-tools-integration reference — v3
- Dot-specific overlays — never; that's Rami's domain

---

## 4. The workflow conductor (Creative Selection spirit)

Kocienda's "demo culture" principle: don't argue about plans; iterate on a concrete thing and let the next step reveal itself. Every command ends with a **next-prompt block**:

```
─── next ───
Recommended: /ux-motion --fix    (4 motion findings, highest cluster)
Other moves:  /ux-copy           (3 copy issues)
              /ux-a11y --fix     (2 a11y issues)
              /ux-next           (let me decide for you)
```

The `--fix` flag is available on every review command (`/ux-audit`, `/ux-copy`, `/ux-a11y`, `/ux-motion`, `/ux-polish`). When passed, the command runs the review then immediately enters the fix loop on its own findings — same loop as the standalone `/ux-fix` command, scoped to that command's lens.

`/ux-next` is the meta-command: reads the freshest report in `.ux/last-report.json` (or wherever we persist state) and decides.

State persistence (lightweight): each command writes a small JSON to `.ux/` in the target project — `last-audit.json`, `last-copy.json`, etc. — so `/ux-fix` and `/ux-next` can chain.

---

## 5. Command contract (every v1 command follows this)

```
---
name: ux-<command>
description: <one-line trigger + use case>
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

## Output
<structured format — see references/output/polaris-style.md>

## State persisted
<path under .ux/ and JSON shape>

## Next prompt
<rules for picking what to suggest>
```

This contract is non-negotiable. Every command keeps the same shape so a user can pick up any of them without re-learning.

---

## 6. Output format (every finding)

```
[SEVERITY] [LENS] Principle violated
Evidence: <screenshot region | copy excerpt | snippet | flow step | URL>
Fix: <specific actionable change>
```

- **Severity**: Critical / High / Medium / Cosmetic
- **Lens**: FRAME / DISCOVER / SCAN / ACT / READ / RECOVER (plus MOTION when run by `/ux-motion`)
- **Principle**: cite source — "Hick's Law", "Krug: Omit Needless Words", "Norman: missing feedback", "WCAG 1.4.3 contrast"
- **Fix**: specific — "Rename 'Submit' → 'Pay $24.99'" not "improve clarity"

Reports end with: severity counts, top-3 must-fix-now, ship-readiness verdict, and the next-prompt block.

---

## 7. Opt-in fix loop (`/ux-fix`)

- **Default mode**: report-only. `/ux-audit`, `/ux-copy`, `/ux-a11y`, `/ux-motion`, `/ux-polish` produce reports.
- **`/ux-fix`** is the explicit fix command. Reads the latest report, applies each finding's `Fix:` to source code, commits atomically per finding, verifies (re-runs the relevant lens at the end).
- **Guardrails**: requires clean working tree (commit/stash prompt). Never auto-fixes copy without showing the proposed diff. Skips Cosmetic severity unless `--include-cosmetic` is passed.
- **`--fix` flag on any review command**: `/ux-audit --fix`, `/ux-copy --fix`, `/ux-a11y --fix`, `/ux-motion --fix`, `/ux-polish --fix` all run the review then enter the fix loop on the resulting findings. Same loop, scoped to the command's lens.

---

## 8. The 6 lenses (used inside `/ux-audit`)

Run in order. Each lens sources from canon:

1. **FRAME** (Lean UX) — Who is this for? What outcome? What hypothesis is the design testing? *Source: `references/process/lean-ux.md`*
2. **DISCOVER** (Norman) — Can a first-timer figure out what to do? Map gulfs of execution & evaluation. Affordances + signifiers + feedback present? *Source: `references/laws/norman.md`*
3. **SCAN** (Krug) — 5-second billboard test: what is this, what should I click first, can I scan-not-read? *Source: `references/laws/krug.md`*
4. **ACT** (Laws of UX + Norman action cycle) — Action loop integrity. Cognitive-load: Fitts, Hick, Miller, Jakob, Tesler, Postel. *Sources: `references/laws/laws-of-ux.md`, `references/laws/norman.md`*
5. **READ** (microcopy) — Voice, error specificity, empty states, CTAs, loading, success. *Source: `references/foundations/copy.md`*
6. **RECOVER** (Norman error design + a11y) — Errors caught with a specific path. WCAG 2.1 AA. Krug's "common courtesy". *Sources: `references/laws/norman.md`, `references/foundations/accessibility.md`*

`/ux-motion` adds a 7th lens (MOTION) when invoked directly; it isn't in the default audit pass to keep audits fast.

---

## 9. Polaris-style foundations house style

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
- [ ] ...

## Sources
<canon citations: Norman p.X, Krug ch.Y, Laws of UX, WCAG ref, etc.>
```

This is what "Polaris-style" means in practice: structured, citable, scannable, evidence-backed.

---

## 10. Absorbed-skills map (proves nothing is lost)

| Existing skill | Where it lives in `ux` plugin |
|---|---|
| `design-review` (visual QA, AI slop, hierarchy, fix loop) | `/ux-audit` lenses 2–4 + `/ux-polish` (AI slop) + `/ux-fix` (loop) |
| `design-critique` (taste, judgment) | Folded into `/ux-audit` voice + `/ux-polish` |
| `accessibility-review` (WCAG 2.1 AA) | `/ux-a11y` + `references/foundations/accessibility.md` |
| `ux-copy` (microcopy) | `/ux-copy` + `references/foundations/copy.md` |

v2's `/ux-critique` will pull `design-critique` into a standalone open-ended-taste command.

---

## 11. Canon mapping (where each book/source goes)

| Source | Location |
|---|---|
| Norman, *Design of Everyday Things* | `references/laws/norman.md`; primary source for DISCOVER + RECOVER lenses |
| Krug, *Don't Make Me Think* | `references/laws/krug.md`; primary source for SCAN lens + courtesy in `/ux-a11y` |
| lawsofux.com (30 laws) | `references/laws/laws-of-ux.md`; primary source for ACT lens |
| Gothelf/Seiden, *Lean UX* | `references/process/lean-ux.md`; basis for `/ux-frame` + FRAME lens |
| Kocienda, *Creative Selection* | `references/process/creative-selection.md`; spiritual basis for the workflow conductor |
| Eyal, *Hooked* | DEFERRED to v3 as `references/conditional/habit-design.md` |
| Wheeler, *Designing Brand Identity* + great-logos guide | DEFERRED to v3 as `references/conditional/brand-system.md` |
| Good to Great / Zero to One / Profit First | OUT OF SCOPE — strategy/business, not UX |

---

## 12. Open questions / decisions deferred to plan phase

1. **Canonical install location**: `~/.claude/plugins/ux/` vs a separate git repo we publish. Plan phase decides based on whether Laith wants to share this with the broader Claude Code community.
2. **State persistence path**: `.ux/` in the target project, or `~/.gstack/projects/<slug>/ux/`? Plan phase picks based on cross-project portability needs.
3. **Severity → "must-fix-now" cutoff**: Critical + High by default? Add a config flag for stricter teams?
4. **Awwwards exemplars** (v2): static curated list vs dynamic fetch?
5. **Motion philosophy split** (v2): single foundation doc with a "perspectives" section, or separate files per philosophy?

---

## 13. Suggested implementation order (for the plan phase)

1. Plugin scaffolding (`plugin.json`, directory layout, README).
2. The output style (`references/output/polaris-style.md`) — write this FIRST since every command depends on it.
3. `references/foundations/*` (7 files) — written by parallel research sub-agents, each grounded in one canon source.
4. `references/laws/*` (3 files) — same approach.
5. `references/process/*` (2 files).
6. Commands in dependency order: `/ux-frame` → `/ux-audit` (uses frame) → `/ux-copy`, `/ux-a11y`, `/ux-motion`, `/ux-polish` (parallel) → `/ux-fix` → `/ux-next`.
7. State persistence layer (`.ux/last-*.json`).
8. End-to-end test on three real surfaces from different stacks (e.g., a reward-loyalty Blade view, a generic React landing page, a Shopify product page).
9. README + install instructions.

---

## 14. Success criteria

- All 8 v1 commands callable as real slash commands.
- A user can run `/ux-audit` on a fresh page and get a Polaris-styled, evidence-cited report ending with a next-prompt block.
- `/ux-next` correctly identifies the highest-leverage next move from any combination of prior reports.
- `/ux-fix` applies findings as atomic commits with passing re-verification.
- Output beats `design-review` + `design-critique` + `accessibility-review` + `ux-copy` combined on: structure, citation quality, next-step clarity, and absence of AI-slop language.
- Plugin loads cleanly in Claude Code and surfaces commands in `/help`.
