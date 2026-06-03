**English** · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — the design intelligence engine for Claude Code, Cursor, and every other AI coding tool

**A design-intelligence engine that makes AI-generated UI distinctive instead of generic.** Drop it into any of 17 AI coding tools and your output stops reading as AI-built. Free, MIT, offline, no LLM.

```bash
pip install uxskill
```

**[Star ux-skill on GitHub](https://github.com/Laith0003/ux-skill)** if this is useful — it is the single cheapest way to help the project. New here? Start with the [60-second tour](#quick-install) or see it live at [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

> **v3.1.0 — THE BRAIN, now brand-true + responsive.** The strongest UX plugin for AI coding. A Python reasoning core with a deterministic 7-axis synthesizer, 12 queryable JSON manifests (84 styles, 176 palettes, 70 type pairings, 148 components, 184 industries, 35 chart types, 57 motion presets, 112 UX laws, 152 anti-pattern rules, 25 tech stacks, 160 brand specs), 25 slash commands, 5 sub-agents, 18 MCP tools, and a deterministic anti-AI-slop linter. Cross-IDE: ships into Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer, and Roo Cline.

> **The brand name is `ux-skill`.** The PyPI / npm package name stays `uxskill`. The GitHub repo lives at [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Site:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Compare vs every Claude UX plugin:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.1.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#the-17-ide-installer)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-152-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-310_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### New in v3.1 — brand-true, responsive, alive

- **Brand fidelity is enforced, not hoped.** The primary color is read from the LOGO's pixels (not the most-painted CSS); default fonts are rejected for the logo's letterform style. The extracted brand travels `recommend` -> `synthesize`, and a **hard floor** in `evaluate` FAILS any output that drops the brand color/logo or ships no real imagery. Two-way interop with the open `brand.md` convention (render + ingest).
- **Mobile-first, gated.** New craft foundations (`responsive.md`, `component-behaviors.md`) plus a wrap-aware gate that fails on horizontal scroll, a wrapping nav/wordmark/button label, or an over-tall sticky header.
- **The wow layer.** The engine derives 2-3 coordinated signature moments per page — the "wow can only come from the user" doctrine is overturned.
- **Sharper linter** (152 rules): imagery-mandatory + icon-only detection, placeholder-token and `100vw` rules; seeded picsum kept, random stripped.

Tests **310 passing**. Offline. Deterministic. No LLM ever called. Full notes in [CHANGELOG.md](CHANGELOG.md).

### What's new in v3

- **Brand specs become training data, not templates.** The 160 brand specs are no longer a catalogue the recommender picks from — they're vocabulary the synthesizer distills from. Output is novel every call.
- **7-axis synthesizer** (warmth, contrast, density, geometry, formality, motion, type_personality). Briefs map deterministically to axis values; axis values compile to fresh palette + type + spacing + radius + motion tokens.
- **Three auto-dispatched modes** — `strict_brand` (100% of one brand), `brand_anchor` (70% one brand + 30% axis-adapted siblings), `pure_synthesis` (no brand named — distill from 8 axis-matching exemplars).
- **Decisions ledger drives the recommender.** `.ux/decisions.jsonl` re-ranks candidates by past wins in the same `(industry, ui_type)` bucket. Cold-start safe. Counts only `lint_score >= 80` + `user_accepted = true` decisions.
- **Axis interaction matrix** — explicit conflict resolution between competing axes (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). No more silent ad-hoc rules.
- **`/ux-evolve` auto-loop** — lint → polish → re-lint until score ≥ 90 or plateau or 5 rounds. Quality gate at 65.
- **3 new MCP tools** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Local stats dashboard** — `uxskill stats --html` writes `.ux/stats.html` showing what YOUR install has learned. No telemetry, no global aggregate.
- **223 tests pass.** Offline. Deterministic. No LLM ever called.

Full details in [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Star history

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## What is ux-skill

ux-skill is a **design intelligence engine** for AI coding tools. It runs as a Python package (`pip install uxskill`), as a Claude Code plugin, and as a 17-IDE multi-installer. The engine ingests a project brief (industry, audience, tone, must-haves, forbidden moves, stack, region) and returns a complete recommended design system: style, palette, type pair, motion presets, components, brand exemplars to study, and the anti-pattern guardrails that must hold. The recommendation is deterministic — same input always produces the same output.

The plugin sits between you and the AI coding tool. When you ask Claude Code, Cursor, or any other AI assistant to "build a fintech landing page," the assistant typically improvises — and the result reads as AI-generated within five seconds (purple-to-blue gradients, three equal cards, Inter at display size, "John Doe" in testimonials, 300ms default transitions, centered hero, bouncing arrow CTAs). ux-skill replaces improvisation with **structured constraints**: you run `/ux-discover` to capture the brief, `/ux-recommend` to pick the system, `/ux-design` to generate the code, and `/ux-lint` to verify it passes the 152 deterministic anti-AI-slop rules before commit.

This README is the canonical reference. Every command, every sub-agent, every data manifest, every install path, every brand spec, every anti-pattern category — it's all documented here. If you're shopping for a Claude Code design plugin or comparing AI design tools for Cursor, Windsurf, or Codex, read this top to bottom and the [compare.html](https://uxskill.laithjunaidy.com/compare.html) side by side.

---

## Table of contents

1. [The Brain — what v3.0 is](#the-brain--what-v30-is)
2. [Quick install](#quick-install)
3. [The numbers — live comparison vs the top 8 Claude UX skills](#the-numbers--live-comparison-vs-the-top-8-claude-ux-skills)
4. [Architecture — how the pieces fit](#architecture--how-the-pieces-fit)
5. [The 25 slash commands — detailed reference](#the-23-slash-commands--detailed-reference)
6. [The 5 sub-agents](#the-5-sub-agents)
7. [The 11 data manifests](#the-11-data-manifests)
8. [The 152 anti-AI-slop rules — the linter](#the-152-anti-ai-slop-rules--the-linter)
9. [The 160 brand DESIGN.md specs — by category](#the-160-brand-designmd-specs--by-category)
10. [MCP server — the asymmetric move](#mcp-server--the-asymmetric-move)
11. [The 17-IDE installer](#the-17-ide-installer)
12. [Use cases — concrete scenarios](#use-cases--concrete-scenarios)
13. [Compared to alternatives](#compared-to-alternatives)
14. [Roadmap](#roadmap)
15. [Contributing](#contributing)
16. [License, author, acknowledgments](#license-author-acknowledgments)

---

## The Brain — what v3.0 is

v3.0.0 is the biggest architectural shift in ux-skill's history. The recommender no longer picks templates from a catalogue — the engine **synthesizes** a fresh design language per brief. Same brief always yields the same output (fully deterministic), but every distinct brief gets its own novel system. Brand specs aren't templates anymore; they're training data the engine learns the vocabulary from. The system has eyes on its own history, closes the feedback loop locally, and never calls an LLM.

The compiler is a **deterministic 7-axis synthesizer** — warmth, contrast, density, geometry, formality, motion, type_personality. Every brief maps to axis values; axis values compile to fresh palette + type + spacing + radius + motion tokens. Modular type scales pick their ratio from contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Layout primitives are responsive by construction (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Broken layouts can't be emitted because they aren't representable.

There are three auto-dispatched modes: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% Stripe tokens, fastest path); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% axis-adapted from 4 sibling brands); and `pure_synthesis` (no brand named → infinity space, 8 axis-matching exemplars distilled into a novel design language). Conflicting axes are resolved by a documented **axis interaction matrix** — dense + corporate compiles to 4px (density wins, Bloomberg-school), airy + corporate to 12px (formality wins, luxury), soft + playful to 18px radius, sharp + corporate to 2px. No silent ad-hoc rules in the implementation.

The **decisions ledger** (`.ux/decisions.jsonl`, schema `_v: 1` locked) closes the feedback loop. The recommender now re-ranks candidates by past wins in the same `(industry, ui_type)` bucket. Cold-start safe — it skips below 3 priors. It only counts decisions with `lint_score >= 80` AND `user_accepted = true`. Plus `/ux-evolve` runs lint → polish → re-lint until score ≥ 90 or plateau or 5 rounds, with a 65-score quality gate below which output is refused unless `--force`. The result: every install gets smarter on its own corpus, every run is reproducible across machines, and the engine stays fully offline.

---

## Quick install

Three install paths. Pick the one that matches your environment.

### Path 1 — Claude Code marketplace (canonical)

If you live in Claude Code, install via the plugin marketplace:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

That wires all 25 slash commands and 5 sub-agents into your Claude Code session. After install, run `/ux-init` to set up the per-project `.ux/` state directory and verify the Python engine is reachable.

### Path 2 — pip (universal)

If you live outside Claude Code (Cursor, Windsurf, CLI, CI), install the Python package:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

The package exposes both `ux` and `uxskill` as CLI entry points — they're the same binary.

### Path 3 — npx (no Python required)

If you don't want to manage Python directly, the npx wrapper bootstraps everything via `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verify install

```bash
ux stats
# {
#   "version": "3.0.0-stable",
#   "counts": {
#     "styles": 84,
#     "palettes": 176,
#     "type-pairs": 70,
#     "components": 148,
#     "industries": 184,
#     "chart-types": 35,
#     "tech-stacks": 25,
#     "ux-guidelines": 112,
#     "motion-presets": 57,
#     "anti-patterns": 145,
#     "brands": 160
#   }
# }
```

If any count returns 0, the JSON file is missing — open an issue at [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## The numbers — live comparison vs the top 8 Claude UX skills

Star counts last verified via `gh api` on **2026-05-28**. ux-skill (Laith0003/ux-skill) is the newest entrant — we're tiny on awareness, deep on architecture. The comparison below is honest: where we lose, where we win.

| Plugin | Stars | Architecture | Slash commands | Linter (CI-safe) | Brand specs | Components | Motion presets | IDEs supported |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV, single skill | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 skills + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + research-backed taste | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | Single 62 KB SKILL.md + scripts | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | MCP-wired skill library | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | Single-aesthetic skill | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | Anti-slop design skill | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 components + audit | 1 | — | (MD3 only) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python engine + 12 manifests + 25 commands + 5 sub-agents + CI linter** | **22** | **152 regex rules** | **160** | **148** | **57** | **17** |

### Where we lose

- **Awareness.** They have hundreds of thousands of stars. We have 14. Star us — it's the cheapest way to help.
- **Brand recognition.** ui-ux-pro-max and open-design have a head start measured in months, not days.
- **Marketing polish.** They have screenshots, demo videos, and a discoverable landing page. We have a thorough README and a thin landing.

### Where we win

- **Component library:** 148 documented components with anatomy, states, tokens used, and motion specs. None of the other 8 ship a component manifest.
- **Motion presets:** 57 stack-ready entries (Framer Motion, GSAP, CSS) with reduced-motion fallbacks. None of the others ship a motion manifest.
- **Anti-pattern linter:** 152 deterministic regex rules, runs in CI, exits non-zero on Critical/High. None of the others ship a deterministic linter.
- **Brand specs:** 160 real DESIGN.md specs (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude, and 96 more). None of the others ship a brand library.
- **17 IDEs supported:** same engine, different glue per IDE.
- **25 slash commands:** discovery, generation, audit, lint, polish, fix loop, case-study, workshop, copy, motion, a11y, dashboard, conductor — fully integrated.

Full table-by-table side-by-side at [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Architecture — how the pieces fit

```
ux-skill (package name: uxskill)
│
├── data/                              The brain — queryable JSON manifests
│   ├── styles.json                    84 design styles + when/skip + tokens
│   ├── palettes.json                  176 palettes (light/dark, contrast verified)
│   ├── type-pairs.json                70 display × body × mono triplets
│   ├── components.json                148 components (anatomy, states, motion)
│   ├── industries.json                184 industry rules + audience signals
│   ├── chart-types.json               35 chart types (when/skip, encoding)
│   ├── tech-stacks.json               25 stacks (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 named UX laws (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 motion presets (entry, exit, hover...)
│   ├── anti-patterns.json             152 regex rules (CI-safe linter source)
│   └── brands/*.json                  160 brand DESIGN specs + _index.json
│
├── engine/                            Python — the reasoning
│   ├── synthesizer/                   v3 — 7-axis deterministic compiler
│   ├── decisions/                     v3 — .ux/decisions.jsonl ledger + recommender re-rank
│   ├── recommender/                   5-parallel-search merge engine (re-ranked by decisions)
│   ├── linter/                        Deterministic anti-slop scanner
│   ├── discovery/                     10-field forcing protocol
│   ├── generator/                     Token + manifest emitter
│   ├── installer/                     17-IDE multi-installer
│   └── cli/                           `ux` / `uxskill` entry point
│
├── commands/                          22 Claude Code slash commands (.md)
│   ├── ux-init.md                     bootstrap
│   ├── ux-stats.md                    inventory snapshot
│   ├── ux-discover.md                 10-field intake (gate)
│   ├── ux-recommend.md                FLAGSHIP — 5-parallel search
│   ├── ux-lint.md                     deterministic linter
│   ├── ux-design.md                   generate frontend code
│   ├── ux-component.md                generate one component
│   ├── ux-system.md                   generate full design system
│   ├── ux-dashboard.md                generate dashboard surface
│   ├── ux-motion.md                   motion treatment + audit
│   ├── ux-audit.md                    6-lens design audit
│   ├── ux-a11y.md                     WCAG 2.1 AA audit
│   ├── ux-critique.md                 taste critique (3 wins, 3 misses, 1 move)
│   ├── ux-copy.md                     microcopy review + rewrite
│   ├── ux-fix.md                      apply findings as atomic commits
│   ├── ux-polish.md                   cosmetic pass + AI-slop kill
│   ├── ux-frame.md                    4-field framing block
│   ├── ux-research.md                 research planning + synthesis
│   ├── ux-workshop.md                 5-phase design thinking workshop
│   ├── ux-case-study.md               publishable Wfrah-editorial case study
│   ├── ux-next.md                     workflow conductor (read-only)
│   └── ux-expert.md                   consulting hook
│
├── agents/                            5 sub-agents (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy in brand voice
│   ├── research-synthesizer.md        interviews + analytics + competitors
│   └── design-system-architect.md     tokens / components / foundations
│
├── references/                        Prose source for the data + demo pages
│   ├── foundations/                   anti-patterns.md, principles, taste
│   ├── laws/                          UX laws long-form
│   ├── process/                       discovery-protocol.md (load-bearing)
│   ├── styles/                        per-style prose (anti-slop.md, etc.)
│   ├── components/                    component long-form
│   ├── output/                        output rubrics
│   └── conditional/                   stack-specific guidance
│
├── bin/
│   ├── uxskill.mjs                    npx wrapper -> Python engine
│   ├── ux-lint.py                     v2 linter (preferred)
│   └── ux-lint.sh                     v1 fallback (bash + perl-PCRE)
│
└── .ux/                               (created per project)
    ├── last-discovery.json            brief snapshot
    ├── last-recommendation.json       picked system
    ├── last-frame.json                framing block
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### How the engine actually works

1. **Input.** You provide a brief — either interactively via `/ux-discover` (10 fields) or non-interactively via flags to `ux recommend`.
2. **5 parallel searches.** The engine runs five lookups concurrently across the manifests:
   - **Industry → recommended_styles** (industries.json)
   - **Style → palette + type + motion compatibility** (styles.json)
   - **Tone × must-have → palette filter** (palettes.json)
   - **Stack → component compatibility + motion presets** (tech-stacks.json, motion-presets.json)
   - **Forbidden + region → guardrails + brand exemplar shortlist** (anti-patterns.json, brands/)
3. **Merge.** A deterministic merger ranks candidates, resolves conflicts (e.g., must-have dark-mode forces palette mode), and emits a single recommended system.
4. **Output.** A JSON document with the picked style, palette, type pair, top 5 motion presets, top 12 components, top 5 brand exemplars, and all 152 anti-pattern guardrails active. Plus a rationale block explaining each pick.
5. **Generation.** Downstream commands (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) consume the recommendation to generate actual code via the sub-agents.
6. **Verification.** `/ux-lint` re-scans the generated code against the 152 regex rules. Exits non-zero on Critical/High in CI.

**v3 additions.** The recommender now re-ranks candidates from `engine/decisions/` using `.ux/decisions.jsonl` (only counts decisions with `lint_score >= 80` AND `user_accepted = true`; cold-start safe below 3 priors). The generator path can dispatch into `engine/synthesizer/` — a deterministic 7-axis compiler that produces fresh palette + type + spacing + radius + motion tokens per brief instead of picking templates from a catalogue. See [The Brain — what v3.0 is](#the-brain--what-v30-is) for details.

**Python thinks. HTML shows. Markdown chains.**

---

## The 25 slash commands — detailed reference

Every command is shipped as a `.md` file under `commands/` with `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process`, and `output state file`. The descriptions below are condensed; the full source is the canonical spec.

Commands are grouped into five buckets: **bootstrap & inventory**, **discovery & recommendation**, **generation**, **audit & verify**, **fix & polish**, and **conductor**.

### Bootstrap & inventory

#### `/ux-init` — bootstrap the project

- **What:** Detects which IDE you're using (`.claude/`, `.cursor/`, `.windsurf/`, etc.), installs the right artifact, verifies the Python engine is reachable, prints a stats snapshot.
- **When to use:** First time installing in a new project. After cloning a project that uses ux-skill. After `pip install --upgrade uxskill`.
- **When to skip:** You already ran it in this project and nothing changed.
- **Invocation:** `/ux-init` (no args) or `uxskill init` from the CLI.
- **Output:** Per-IDE artifact (see [The 17-IDE installer](#the-17-ide-installer)) + `.ux/` directory + stdout summary.
- **Chains to:** `/ux-discover` next.

#### `/ux-stats` — print the data inventory

- **What:** Prints version + entry counts for the 11 data manifests, so you can verify what's installed.
- **When to use:** After install. After upgrade. When `/ux-recommend` returns surprising picks and you suspect the manifests are incomplete.
- **When to skip:** Never — it's a 50ms read-only command.
- **Invocation:** `/ux-stats` or `uxskill stats`.
- **Output:** JSON to stdout (see [Verify install](#verify-install) above).
- **Chains to:** Diagnostic only; doesn't feed downstream.

### Discovery & recommendation

#### `/ux-discover` — the forcing function (10-field intake)

- **What:** The mandatory 10-field intake every project goes through before any generation command. Project type, audience, primary goal, tone, must-haves, forbidden, reference brands, stack, region, success metric. **No improvisation.** Banned phrases ("modern", "clean") force the user to be specific.
- **When to use:** Before any `/ux-design`, `/ux-component`, `/ux-system`, or `/ux-dashboard`. Whenever a previous brief has gone stale.
- **When to skip:** You're fixing a bug (`/ux-fix`). You're only running a linter pass (`/ux-lint`). The brief is unchanged from the last session.
- **Invocation:** `/ux-discover`. The plugin asks; you answer.
- **Output:** Writes `.ux/last-discovery.json` (the 10-field brief).
- **Chains to:** `/ux-recommend` → uses the discovery to pick style + palette + type + motion + components. `/ux-design [extra brief]` → generates frontend code grounded in the recommendation. `/ux-component <name>` → generates one component aligned to discovered constraints.

#### `/ux-recommend` — the flagship 5-parallel-search engine

- **What:** Runs the Python engine's 5-parallel-search across 12 manifests and returns one merged design system. Industry → Style → Palette → Type → Motion + Components + Brand Exemplars + Guardrails.
- **When to use:** Starting a new project from zero. Pivoting a tired-looking product. Pre-flight before any `/ux-design` or `/ux-component`.
- **When to skip:** You already ran `/ux-discover` and saved a brief — `/ux-recommend` is automatic in that flow. You're fixing one bug (use `/ux-fix`). You only need to lint (use `/ux-lint`).
- **Invocation (Claude Code):**
  ```
  /ux-recommend
  ```
  **Invocation (CLI):**
  ```bash
  ux recommend \
    --project-type=landing \
    --industry=fintech-neobank \
    --tone=warm --tone=editorial \
    --must-have=dark-mode --must-have=a11y-AA \
    --forbidden=brutalism --forbidden=purple-gradients \
    --stack=nextjs-15-app-router \
    --region=mena
  ```
- **Output:** Writes `.ux/last-recommendation.json` — picked style, picked palette, picked type pair, top 5 motion presets, top 12 components, top 5 brand exemplars, all 152 anti-pattern guardrails active, plus rationale.
- **Chains to:** `/ux-design [brief]` → frontend code using the recommended tokens. `/ux-system` → full design system from the recommendation. `/ux-component <name>` → one component using the recommended style. `/ux-lint` → verify the generated code.

### Generation

#### `/ux-design` — generate a beautiful, anti-slop surface from a brief

- **What:** Generates a complete, production-grade frontend artifact (landing, marketing site, app shell) from the discovery brief + recommendation. Dispatches `frontend-engineer` with creative direction from anti-slop and arsenal references.
- **When to use:** "Design a", "build me a", "generate a landing page", "create a dashboard", "make a component" — any free-form visual deliverable request.
- **When to skip:** You want a review, not a build (use `/ux-audit` or `/ux-critique`). You want one component only (use `/ux-component`). Backend or infrastructure work.
- **Invocation:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`.
- **Output:** Generated code (HTML / Blade / JSX / Vue / Astro), plus `.ux/last-design.json`.
- **Chains to:** `/ux-lint` → verify against guardrails. `/ux-polish` → cosmetic pass. `/ux-a11y` → accessibility audit. `/ux-copy` → microcopy review. `/ux-fix` → apply findings as atomic commits.

#### `/ux-component` — generate one component

- **What:** Produces a single, production-grade component (button, modal, navbar, sidebar, card, table, form, chart) from a spec. All four interaction states, accessible, on-brand. Looks up the component in `.ux/last-recommendation.json` first, falls back to direct manifest query.
- **When to use:** Any single-element request — "build a button", "create a pricing card", "make a modal", "add a navbar", "design a sidebar", "I need a data table", "build a form", "make a chart component".
- **When to skip:** Full page or multi-section surface (use `/ux-design`). Backend or infrastructure.
- **Invocation:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`.
- **Output:** Generated component code, plus `.ux/last-component.json`.
- **Chains to:** `/ux-lint` → verify. `/ux-polish` → tighten.

#### `/ux-system` — generate a complete starter design system

- **What:** Proposes a complete starter design system for a project that doesn't have one — tokens (color, type, space, motion, radius, shadow), foundation docs, component contracts, dark-mode pairings, theme switcher. Dispatches `design-system-architect`.
- **When to use:** "We don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS".
- **When to skip:** The project already has a design system — use `/ux-component` against the existing system instead. Backend or infrastructure.
- **Invocation:** `/ux-system` (runs discovery first if not already on file).
- **Output:** `tokens.json`, `foundations.md`, `components/*.md` contracts, optional Tailwind / vanilla / SCSS emit. Writes `.ux/last-system.json` for chain context.
- **Chains to:** `/ux-component` → build against the new system. `/ux-design` → generate a surface using the new tokens.

#### `/ux-dashboard` — specialized dashboard generation

- **What:** Dashboard with data density discipline — bento layout, tabular monospace numerals, sparkline patterns, anti-card-overuse, semantic state colors, sparing motion. Not a marketing site with charts pasted on.
- **When to use:** "Build a dashboard", "design the admin panel", "make a metrics page", "operator console", "analytics view", "KPI board", "monitoring screen".
- **When to skip:** Marketing landing page with stats (use `/ux-design`). One widget only (use `/ux-component`). Backend or infrastructure.
- **Invocation:** `/ux-dashboard`.
- **Output:** Generated dashboard code + `.ux/last-dashboard.json`.
- **Chains to:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — motion treatment

- **What:** Generates the motion layer of a surface — durations, easings, choreography, reduced-motion fallbacks, performance discipline. Also audits existing motion against the 5 dimensions (timing, easing, meaning, reduced-motion, performance).
- **When to use:** "Motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "performance pass on the motion".
- **When to skip:** Surface has no motion (use `/ux-audit` or `/ux-polish`). Backend or infrastructure.
- **Invocation:** `/ux-motion path/to/component.tsx` (audit mode) or `/ux-motion --generate hero-entry` (generation).
- **Output:** Updated code (in generation mode) or `.ux/last-motion.json` report (in audit mode).
- **Chains to:** `/ux-fix` → apply motion findings. `/ux-polish` → tighten.

### Audit & verify

#### `/ux-lint` — deterministic regex-based linter (no LLM, CI-safe)

- **What:** Runs 152 regex rules against your code. No LLM call. Exits non-zero on Critical / High in CI. Source: `data/anti-patterns.json`. Rules cover A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4).
- **When to use:** Pre-commit hook. CI gate. Fast first pass on a large codebase before paying the cost of `/ux-audit`. After `/ux-design` or `/ux-component` to verify generation.
- **When to skip:** You want a fix loop (the linter reports, it does not edit — chain into `/ux-polish --fix` or `/ux-fix`). You want taste judgment (use `/ux-critique`).
- **Invocation (slash):** `/ux-lint src/`.
- **Invocation (CLI):** `uxskill lint .` or `python3 bin/ux-lint.py .` or `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocation (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Findings to stdout (location, rule id, severity, evidence). Exit code 0 if clean, non-zero on Critical/High when `--fail-on high` is set.
- **Chains to:** `/ux-polish --fix` → LLM-driven counterpart on the same patterns. `/ux-fix` → apply findings as commits, severity-sorted. `/ux-audit` → full 6-lens reasoning pass. `/ux-next` → let the conductor decide.

#### `/ux-audit` — 6-lens design audit

- **What:** A structured, opinionated review against six lenses (clarity, hierarchy, accessibility, voice, motion, taste), producing severity-tagged findings. Polaris-style report. Reads `.ux/last-frame.json` first — audience and outcome anchor every finding's severity.
- **When to use:** Surface exists and you want a defensible critique. "Audit", "review the ux", "is this any good", "what's broken", "tear this apart".
- **When to skip:** Surface doesn't exist yet (use `/ux-design`). User wants one lens (use the targeted command: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). User wants taste opinion (use `/ux-critique`). Backend or infrastructure.
- **Invocation:** `/ux-audit https://example.com/pricing` or `/ux-audit src/components/Pricing.tsx`.
- **Output:** Writes `.ux/last-audit.json` — `findings` array of `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Chains to:** `/ux-fix` → apply findings. `/ux-polish` → cosmetic pass. `/ux-design` → if structural redesign needed.

#### `/ux-a11y` — WCAG 2.1 AA audit + common-courtesy checks

- **What:** A structured WCAG 2.1 AA audit, plus the common-courtesy checks that pass automated tools but still hurt real users (focus visibility, error specificity, motion preferences, keyboard traps, color reliance).
- **When to use:** Pre-ship accessibility gate. After a redesign. "Accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check".
- **When to skip:** Not user-facing. Backend or infrastructure. Work-in-progress sketches.
- **Invocation:** `/ux-a11y https://example.com` (live URL preferred — automated tools and keyboard testing only work live).
- **Output:** Writes `.ux/last-a11y.json` — `findings` array of `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, `beyond_wcag` array, `severity_counts`.
- **Chains to:** `/ux-fix` → apply findings as commits. `/ux-copy` → fix alt text and form-error wiring as part of a copy pass.

#### `/ux-critique` — taste call (3 wins, 3 misses, 1 strategic move)

- **What:** A designer's opinion — not a structured audit, not a severity score, just a tight, opinionated take that names what's working, what's not, and the one strategic move that would change the most.
- **When to use:** "What do you think", "is this good", "critique this", "honest take", "is the vibe right", "does this feel like us", "should we ship this".
- **When to skip:** User explicitly wants a structured audit (use `/ux-audit`). Backend or infrastructure.
- **Invocation:** `/ux-critique https://example.com`.
- **Output:** Writes `.ux/last-critique.json` — 3 wins, 3 misses, 1 strategic move, plus prose.
- **Chains to:** `/ux-design` if the take recommends redesign. `/ux-polish` if the take recommends tightening.

#### `/ux-copy` — microcopy review + rewrite

- **What:** Evaluates every visible string against the voice rubric and produces a before/after rewrite. Catches: "form contains errors" (generic), "John Doe" (placeholder), AI-cheerful celebratory copy, generic CTAs, dead empty states, useless errors.
- **When to use:** Structure is right but words are weak. "Review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "tighten the strings", "the buttons sound generic", "this empty state is dead".
- **When to skip:** Layout problems (use `/ux-audit` or `/ux-polish`). Accessibility-driven copy issues like alt text (use `/ux-a11y`). Backend or infrastructure.
- **Invocation:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Writes `.ux/last-copy.json` — `strings` array of `{location, severity, before, after, notes}`, plus rubric + locales needing translation.
- **Chains to:** `/ux-fix` → apply rewrites. `/ux-a11y` → re-check after copy fixes.

### Fix & polish

#### `/ux-fix` — apply findings as atomic commits

- **What:** Reads the latest report from `.ux/` (audit, copy, a11y, motion, or polish), validates the working tree, and applies findings as atomic commits via the right sub-agents. Re-verifies by re-running the originating command.
- **When to use:** After running an audit-class command and reviewing findings. "Fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it".
- **When to skip:** No prior report in `.ux/`. Working tree is dirty and the user hasn't agreed to stash/commit. Fixes need design judgment, not mechanical application (use `/ux-design` for a redesign).
- **Invocation:** `/ux-fix` (auto-detects which report to fix) or `/ux-fix --from=last-a11y.json`.
- **Output:** Atomic commits per finding. Re-runs the originating command and updates the `.ux/last-*.json` file. Prints a summary.
- **Chains to:** `/ux-next` → conductor picks the next move.

#### `/ux-polish` — cosmetic pass + AI-slop kill

- **What:** Spacing rhythm, hierarchy sharpening, AI-slop detection, token consistency. The LLM-driven counterpart to `/ux-lint` — uses your judgment on taste calls.
- **When to use:** Structure is right but execution is loose. "Polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste".
- **When to skip:** Surface is missing core functionality (fix that first). Needs a redesign, not a polish (use `/ux-design`). Copy issues (use `/ux-copy`). Motion issues (use `/ux-motion`). A11y issues (use `/ux-a11y`).
- **Invocation:** `/ux-polish src/components/Hero.tsx`.
- **Output:** Updated code + `.ux/last-polish.json` describing the changes.
- **Chains to:** `/ux-lint` → verify the polish held. `/ux-a11y` → re-check accessibility.

### Discovery & narrative

#### `/ux-frame` — 4-field framing block

- **What:** Captures who-it's-for, outcome, hypothesis, and success signal in a structured framing block. No design work happens — just the four-field intake that turns a vague request into a working brief. Lighter than `/ux-discover` (4 fields vs 10).
- **When to use:** Start of any project, sprint, or one-off engagement. Mid-stream when a conversation has drifted. "Frame this", "what's the brief", "set up the project", "framing".
- **When to skip:** Already framed (check `.ux/last-frame.json`). One-off component build with no framing implications. Backend or infrastructure.
- **Invocation:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`.
- **Output:** Writes `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Chains to:** `/ux-discover` → extend the frame to the 10-field brief. `/ux-design` → generate using the frame as anchor.

#### `/ux-research` — research planning + synthesis

- **What:** Planning mode: writes interview scripts, surveys, recruitment screeners. Synthesis mode (`--synthesize`): digests interviews, analytics, competitor sites, A/B results, support tickets into recommendations. Dispatches `research-synthesizer`.
- **When to use:** "Plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes".
- **When to skip:** Answer is already known with high confidence. Low-risk reversible decisions. Backend or infrastructure.
- **Invocation:** `/ux-research --plan "loyalty wallet adoption in MENA"` or `/ux-research --synthesize interviews/*.md`.
- **Output:** Writes `.ux/last-research.json` — research plan or synthesized themes + evidence + recommendations.
- **Chains to:** `/ux-frame` → integrate findings into a frame. `/ux-design` → generate from findings. `/ux-workshop` → run a workshop using the research as input.

#### `/ux-workshop` — 5-phase design thinking workshop

- **What:** Facilitates a discovery / design-thinking workshop end-to-end. Five sequential phases (exploration → heat map → stakeholder map → solution sketch → game plan). Time-boxed. Concrete artifacts per phase. Ends with a decision, not "interesting findings."
- **When to use:** Real question, real participants, real time budget. "Run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "kick off the project".
- **When to skip:** Brief is already clear and scoped. Solo brainstorm (use `/ux-design` or `/ux-frame`). Team is mid-execution, not in discovery.
- **Invocation:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Writes `.ux/last-workshop.json` — game plan + per-phase artifacts.
- **Chains to:** `/ux-design` → execute the game plan. `/ux-research` → fill gaps the workshop surfaced. `/ux-case-study` → publish the journey.

#### `/ux-case-study` — publishable case study (Wfrah-editorial format)

- **What:** Generates a project case study in pure-monochrome editorial format — Wfrah typography, hairline separators, numbered (A)–(G) section codes, bilingual-safe layout. A document, not a marketing brochure. Reads from `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **When to use:** Post-launch. After a discrete milestone. "Write a case study", "case study this project", "do the wrap-up doc", "publish this work", "portfolio piece".
- **When to skip:** Project lacks data to populate (A)–(G) sections. User wants a marketing landing, not a case study (use `/ux-design`).
- **Invocation:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Chains to:** Terminal command — usually the end of a project.

### Conductor

#### `/ux-next` — workflow conductor (read-only)

- **What:** Reads every `.ux/last-*.json` and names the highest-leverage next command. A conductor, not a builder. Read-only.
- **When to use:** Between commands. "What should I do next", "what's the next move", "decide for me", "where do we go from here".
- **When to skip:** No prior reports in `.ux/`. You have a specific next command in mind.
- **Invocation:** `/ux-next` (no args) or `/ux-next --focus=a11y`.
- **Output:** Stdout — recommended next command + rationale.
- **Chains to:** Whichever command it picks.

#### `/ux-expert` — consulting hook

- **What:** Surfaces the plugin creator's contact info when a user asks for a real-life UX expert. Brief, direct, no marketing.
- **When to use:** "Who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin".
- **When to skip:** User is asking about plugin features, not about consulting.
- **Invocation:** `/ux-expert`.
- **Output:** Brief contact card with LinkedIn / email / repo.

### Command chaining graph

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  4-field framing block
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10-field intake (FORCING GATE)
                  └────────────┬─────────┘
                               │ writes .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 parallel searches -> merged system
                  └────────────┬─────────┘
                               │ writes .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ writes .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ writes .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  apply findings as commits
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  publishable artifact
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor — read-only
                  │  /ux-expert          │  consulting hook
                  └──────────────────────┘
```

---

## The 5 sub-agents

Sub-agents are role-specific generators dispatched by commands. They never run independently — they're called by `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, etc. Each agent has a defined ownership boundary: they do NOT decide the brief; they execute against it.

### `frontend-engineer`

- **Owns:** Production-grade frontend code (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro) with anti-AI-slop discipline.
- **Dispatched by:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Inputs:** Brief + creative direction + tokens (from `.ux/last-recommendation.json`).
- **Outputs:** Working code that's distinguishable from generic AI output. No purple gradients, no centered hero, no three equal cards, no Inter at display size, no "John Doe", no emoji, no 300ms defaults.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Owns:** Motion in production frontend code — Framer Motion, GSAP, CSS animations. Durations, easings, choreography, reduced-motion fallbacks, performance discipline.
- **Dispatched by:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Inputs:** Motion brief + tokens + the 57 motion presets from `data/motion-presets.json`.
- **Outputs:** Motion that earns its place. Always wrapped in `prefers-reduced-motion` fallbacks. Always tested against Core Web Vitals.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Owns:** The strings that ship — error messages, empty states, CTAs, loading states, success messages, toasts, helper text, form labels, button text.
- **Dispatched by:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Inputs:** Voice profile (named or pasted) + the surface's strings.
- **Outputs:** Production microcopy applied consistently across every state of a surface so the product sounds like one product, not ten. Bans: "form contains errors", "John Doe", AI-cheerful celebratory copy, generic CTAs, dead empty states.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Owns:** Digesting research inputs (interviews, analytics, competitive sites, A/B results, support tickets) into actionable design recommendations.
- **Dispatched by:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Inputs:** Raw research — transcripts, exports, competitor URLs, support clusters.
- **Outputs:** Themes, evidence, recommendations. Never designs the answer — gives the designer the substrate to design from.
- **Tools:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Owns:** Complete design systems — tokens (color, type, space, motion, radius, shadow), foundation docs, component contracts, dark-mode pairings, theming layer.
- **Dispatched by:** `/ux-system`, `/ux-component` when no system exists.
- **Inputs:** Brand brief + `.ux/last-recommendation.json` (style + palette + type pair + motion presets).
- **Outputs:** A coherent, opinionated, production-ready system that downstream agents can build against without re-deciding fundamentals. Tokens JSON, foundations MD, component contracts, dark-mode mapping.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### Sub-agent dispatch protocol

When a command dispatches a sub-agent, it passes:

1. The brief / recommendation (loaded from `.ux/`).
2. The relevant manifest slice (e.g., `frontend-engineer` gets the picked style + palette + components; `motion-engineer` gets the picked motion presets).
3. The 152 anti-pattern guardrails (always active).
4. A success criterion (what the artifact must do).

Sub-agents return:

1. The artifact (code, doc, system).
2. A rationale block (why these picks).
3. A self-check against the guardrails (which rules they verified).

The calling command then runs `/ux-lint` automatically before declaring done.

---

## The 11 data manifests

The data layer is the brain. Every command reads from it; the engine merges across it; the linter scans against it. All files live under `data/` and wrap their entries in `{_meta, entries}` for schema versioning.

### `styles.json` — 84 design styles

| Field | Description |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, etc. |
| `sample entry` | `swiss-international` — "Grid is law. Type does the heavy lifting. Decoration is failure." |

Used by: `/ux-recommend`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 color palettes

| Field | Description |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, etc. |
| `sample entry` | `claude-warm-editorial` — light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Used by: `/ux-recommend`, `/ux-system`. Contrast verified at AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 type pairings

| Field | Description |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

All families have license + source URL. Used by `/ux-recommend`, `/ux-system`.

### `components.json` — 148 components

| Field | Description |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` — Mega Navigation, Product Grid — 6-part anatomy, 4 states |

This is our biggest moat. No other Claude UX plugin ships a structured component manifest.

### `industries.json` — 184 industry rules

| Field | Description |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, etc. |
| `sample entry` | `fintech-neobank` — high trust, regulatory disclosures, balance/transaction primary UI, mobile-first daily-use |

Used by `/ux-recommend` as the first parallel search axis.

### `chart-types.json` — 35 chart types

| Field | Description |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical` — Compare 4–15 discrete categories. Position along x-axis maps category; height maps value. |

Used by `/ux-dashboard`, `/ux-component` (chart instances).

### `tech-stacks.json` — 25 stacks

| Field | Description |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, compatible with Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Other stacks include Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 named UX laws

| Field | Description |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, etc. |
| `sample entry` | `hicks-law` — Decision time grows logarithmically with the number of choices presented |

Used by `/ux-audit` (6-lens scoring) and `/ux-critique` (taste anchor).

### `motion-presets.json` — 57 motion presets

| Field | Description |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (reduced-motion fallback), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Every preset has a reduced-motion variant. Stack-ready code for Framer Motion, GSAP, and pure CSS.

### `anti-patterns.json` — 152 regex rules

| Field | Description |
|---|---|
| `entries` | 145 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categories` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

The full rule list is in [The 152 anti-AI-slop rules](#the-152-anti-ai-slop-rules--the-linter).

### `brands/*.json` — 160 brand specs

| Field | Description |
|---|---|
| `entries` | 160 (plus `_index.json` listing all) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Full list in [The 160 brand DESIGN.md specs](#the-160-brand-designmd-specs--by-category).

---

## The 152 anti-AI-slop rules — the linter

ux-skill ships a deterministic regex-based linter. **No LLM.** **No API.** **No network.** Runs in CI in ~200ms on a typical Next.js app. Exits non-zero on Critical / High findings when `--fail-on high` is set.

The rules are sourced from `data/anti-patterns.json` (v2 preferred) with a `references/foundations/anti-patterns.md` fallback (v1 bash). Two binaries ship: `bin/ux-lint.py` (Python, fast, extensible) and `bin/ux-lint.sh` (Bash + perl-PCRE, for environments without Python).

### Rules by category

#### Typography (3 rules)

| Severity | Rule ID | Name |
|---|---|---|
| high | `inter-as-display` | Inter used as display font |
| medium | `hero-text-arbitrary-90px` | Arbitrary hero font size |
| low | `font-system-only` | System font stack with no chosen typeface |

#### Color (6 rules)

| Severity | Rule ID | Name |
|---|---|---|
| high | `purple-to-blue-gradient` | Default purple-to-blue AI gradient |
| high | `dark-text-on-dark-card` | Low-contrast text on card |
| medium | `gradient-text-rainbow` | Multi-stop gradient text |
| medium | `card-glow-purple-shadow` | Purple glow shadow on cards |
| medium | `gradient-mesh-purple-pink` | Purple-pink mesh gradient hero |
| low | `tailwind-color-named-vague` | Named Tailwind colors with no semantic token |

#### Layout (5 rules)

| Severity | Rule ID | Name |
|---|---|---|
| high | `three-equal-card-grid` | Three equal cards in a row |
| medium | `centered-everything-hero` | Centered hero composition |
| medium | `avatar-stack-overlapping` | Generic overlapping avatar stack |
| low | `pill-rounded-full-everywhere` | `rounded-full` applied to everything |
| low | `nav-equal-hamburger-desktop` | Hamburger menu on desktop |

#### Content (5 rules)

| Severity | Rule ID | Name |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum in shipping code |
| high | `emoji-in-ui` | Emoji used as UI element |
| high | `icon-emoji-stamp` | Emoji used as icon stamp |
| high | `testimonial-fake-five-stars` | Hardcoded five-star testimonial |
| medium | `fake-name-john-doe` | Generic placeholder names |

#### Motion (3 rules)

| Severity | Rule ID | Name |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Bouncing arrow on CTA |
| low | `timing-300ms-default` | Default 300ms transition timing |
| low | `cubic-bezier-material-only` | Material default easing everywhere |

#### A11y (6 rules)

| Severity | Rule ID | Name |
|---|---|---|
| high | `inline-svg-no-aria` | SVG without aria-label or aria-hidden |
| high | `img-no-alt` | Image missing alt attribute |
| high | `link-onclick-no-href` | Anchor with onClick but no href |
| medium | `button-no-type` | Button missing type attribute |
| medium | `heading-skip-h1-h3` | Skipped heading level |
| medium | `infinite-scroll-no-pagination` | Infinite scroll without keyboard fallback |

#### Quality (6 rules)

| Severity | Rule ID | Name |
|---|---|---|
| high | `console-log-leak` | `console.log` in component code |
| medium | `inline-style-attribute` | Inline style attribute |
| medium | `any-type-leak` | TypeScript `any` type |
| medium | `arbitrary-z-index-9999` | Lazy z-index value |
| low | `shadcn-default-everywhere` | Default shadcn token block unmodified |
| low | `todo-fixme-comment` | TODO or FIXME in shipping code |

#### Visual (1 rule)

| Severity | Rule ID | Name |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur with no glass surface |

### Linter usage

**One-off scan:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
bash bin/ux-lint.sh src/
```

**CI gate (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**Pre-commit hook:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**Output (sample):**

```
─── /ux-lint report ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  evidence: bg-gradient-to-br from-purple-500 to-blue-500
  fix: replace with the recommended palette's primary gradient or remove gradient

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  evidence: grid grid-cols-3 gap-6 (3 equal Card children)
  fix: feature one card; flank with two reduced-emphasis cards

3 files scanned · 2 high · 0 medium · 0 low · exit 1
Recommended next: /ux-polish --fix (LLM-driven, addresses both lintable and aesthetic findings)
```

---

## The 160 brand DESIGN.md specs — by category

Real brands. Real design languages. Real DESIGN.md specs — not generic palettes. Tell the plugin "build a landing in Stripe's style" and it reads the actual brand vocabulary: voice rubric, color tokens, motion conventions, signature moves, anti-moves.

Each brand ships as a structured JSON (`data/brands/<slug>.json`) plus a prose reference (`references/brands/<slug>.md`).

### Developer Tools (36)

ClickHouse, Composio, Cursor, Datadog, dbt Labs, Expo, Fivetran, Fly.io, Framer, HashiCorp, Honeycomb, IBM, Lovable, Mintlify, Modal, MongoDB, Neon, Ollama, OpenCode, PostHog, Railway, Raycast, Render, Replicate, Resend, Retool, Sanity, Sentry, Slack, Snowflake, Sourcegraph, Supabase, Superhuman, Vercel, Warp, Webflow

### Consumer / Lifestyle / Retail (19)

Aesop, Airbnb, Allbirds, Apple, Apple Music, Glossier, HP, Hims & Hers, Instagram, Meta, Nike, Patagonia, Pinterest, PlayStation, Shopify, Spotify, Starbucks, TikTok, Uber

### Fintech / Crypto (14)

Binance, Brex, Coinbase, Kraken, Mastercard, Mercury, Monzo, N26, Plaid, Ramp, Revolut, Robinhood, Stripe, Wise

### Editorial / Media (13)

Bloomberg, Clay, Dezeen, NVIDIA, Pitchfork, Substack, The Atlantic, The Economist, The New York Times, The Verge, The Wall Street Journal, Vodafone, Wired

### AI / ML Platform (12)

Anthropic, Claude, Cohere, ElevenLabs, MiniMax, Mistral AI, OpenAI, Perplexity, Runway, Together AI, VoltAgent, xAI

### Productivity / Collaboration (8)

Airtable, Cal.com, Figma, Intercom, Linear, Miro, Notion, Zapier

### Automotive (8)

BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, SpaceX, Tesla

### Why this matters

The other 8 popular Claude UX plugins generate "modern minimal" or "clean dashboard" — variants of the same default aesthetic. ux-skill lets you ask for **Linear's clarity**, **Stripe's seriousness**, **Apple's restraint**, **Tesla's monolith**, **Notion's friendliness**, **Cursor's gradient discipline**, **Raycast's hairline density**, **Claude's warm editorial** — and the engine pulls the right tokens, voice, motion conventions, and signature moves from the brand spec.

---

## MCP server — the asymmetric move

ux-skill ships a **Model Context Protocol server**. Run `ux-mcp` and the engine becomes a long-running stdio process that any MCP-capable host — Claude Desktop, Cursor, Windsurf, generic agents — can call into. Eighteen tools: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`. Same Python handlers the slash commands use; same data manifests; same deterministic recommender.

**Why this is the asymmetric move:** none of the top eight Claude UX skills (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) ship an MCP server. They are locked inside Claude Code's plugin runtime. ux-skill is reachable from any host that speaks MCP, including agents that have never heard of a Claude Code plugin.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Point your client at the `ux-mcp` binary. Full tool docs, JSON examples, and per-client config for Claude Desktop, Cursor, and Windsurf live at [docs/mcp.html](docs/mcp.html) and in `commands/ux-mcp.md`.

---

## The 17-IDE installer

`uxskill init` (or `/ux-init` inside Claude Code) auto-detects which IDE you're using and writes the right artifact. Same Python engine. Same recommendations. Different glue per IDE.

| IDE / Tool | Detection signal | Installed artifact |
|---|---|---|
| Claude Code | `.claude/` or `CLAUDE.md` | Plugin manifest at `.claude-plugin/plugin.json` + all 25 commands + all 5 sub-agents |
| Cursor | `.cursor/` or `.cursorrules` | `.cursorrules` prompt header pointing at the engine |
| Windsurf | `.windsurf/` or `.windsurfrules` | `.windsurfrules` with the same prompt header |
| GitHub Copilot | `.github/copilot-instructions.md` or `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json` patch |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` or `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

In every IDE, the same `uxskill recommend` / `uxskill lint` / `uxskill stats` CLI commands work from the terminal. The Python engine is the source of truth; the IDE artifacts are thin prompt-headers that route into it.

---

## Use cases — concrete scenarios

Eight real scenarios. Pick the one closest to your situation and adapt the invocation.

### 1. Building a fintech dashboard in Cursor

You're in Cursor working on a MENA neobank dashboard. You install the plugin and run discovery, recommendation, then dashboard generation.

```bash
pip install uxskill
uxskill init                                # detects Cursor, writes .cursorrules
uxskill discover                            # 10-field intake
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Then in Cursor, ask: *"Generate the dashboard surface using the recommendation in .ux/last-recommendation.json"*. Cursor reads the `.cursorrules` header, loads the recommendation, dispatches a dashboard generation with explicit constraints.

### 2. Generating a Stripe-style landing in Claude Code

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> Project type? landing
> Industry? fintech-payments
> Tone? serious, technical, confident
> Must have? dark-mode, AA, mobile-first
> Forbidden? purple-gradients, three-equal-cards
> Reference brands? stripe
> Stack? nextjs-15-app-router
> Region? global
> Success metric? signup conversion

/ux-recommend
> [returns picked style, palette, type pair, motion presets, components, brand exemplars]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer generates the page]

/ux-lint .
> [passes — Stripe brand spec was respected]
```

### 3. Auditing existing code for AI slop in CI

You shipped a Next.js app two weeks ago. You want a hard floor against AI fingerprints on every PR.

```yaml
# .github/workflows/ux-lint.yml
name: ux-lint
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install uxskill
      - run: uxskill lint . --ci --fail-on high
```

PRs that introduce purple-to-blue gradients, Inter at 96px, "John Doe" testimonials, or emoji-as-icons fail CI. No LLM cost. ~200ms.

### 4. Polishing an existing surface that "feels AI-generated"

You inherited a React app that looks like every other AI-generated SaaS site. You want to make it not look like that.

```
/ux-critique src/components/Hero.tsx
> [3 wins, 3 misses, 1 strategic move — the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Three commands, one polished surface, atomic commits per fix.

### 5. Designing a Linear-style command palette

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

The generated component uses Linear's actual color tokens, type stack, motion conventions, hairline densities — not "generic dark UI."

### 6. Running a 90-minute design thinking workshop with stakeholders

You have a room of 5 people for 90 minutes. You want them to leave with a game plan, not a vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

The plugin facilitates the five phases (exploration → heat map → stakeholder map → solution sketch → game plan) end-to-end, time-boxed, with concrete per-phase artifacts. The output is `.ux/last-workshop.json` — the game plan, not just "interesting findings."

### 7. Writing a publishable case study after launch

You shipped the loyalty wallet. You want a portfolio piece.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

The case study is a finished, publishable artifact — not a draft. Pure monochrome, editorial typography, ready to ship to your portfolio.

### 8. Running discovery in a non-AI context (just structured intake)

You're scoping a project. You don't need a recommendation yet — you need a structured brief.

```bash
uxskill discover
# 10-field intake, saves to .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

You can hand the JSON to your team, paste into a Notion doc, or feed it into a separate AI tool. ux-skill is also a structured intake tool in addition to being an engine.

### 9. MASTER.md persistence — your design decisions, in the repo

After `/ux-recommend`, persist the picked style + palette + type + motion + components + brand exemplars + guardrails as a human-readable Markdown file your team can review, diff, and version-control.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Writes `.ux/design-system/MASTER.md` (YAML frontmatter + body) and `.ux/design-system/pages/<name>.md` per generated surface via `persist save-page`. Idempotent — same input produces byte-identical output, so re-running on unchanged state is a no-op in git.

---

## Compared to alternatives

Short summary table. Full table-by-table comparison is at [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimension | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash commands | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Components | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Motion presets | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand specs | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Anti-pattern rules | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-safe deterministic linter | **yes** | no | no | no | no | no | no | no | no |
| IDEs supported | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery gate | **10 fields** | implicit | implicit | implicit | implicit | implicit | implicit | implicit | implicit |
| `.ux/` state chain | **yes** | no | no | no | no | no | no | no | no |
| Stars (2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### Honest assessment

- **ui-ux-pro-max** is bigger on awareness, ships 18 IDEs, has BM25-style search over its CSV. It doesn't ship a component manifest, motion manifest, brand library, or deterministic linter.
- **open-design** has 19 skills + preview but only Claude Code support and no anti-slop layer.
- **hallmark** is the closest in spirit (also anti-slop) but is a single skill — no engine, no manifests, no chained commands.
- **material-3-skill** is excellent if you specifically want Material Design 3. We don't compete on MD3.

For full detail per dimension, see [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

### v2.1 — Linter completeness (Q3 2026)

- **+17 deferred anti-pattern rules** to reach 52 total. Targets: dark-on-dark hover states, color-only state encoding, redundant z-index escalation, hardcoded breakpoints in JS, opacity instead of disabled state, etc.
- **`uxskill lint --fix` for safe rewrites** of mechanically-fixable findings (button-no-type, img-no-alt empty-string, console-log-leak removal).
- **VS Code extension** that surfaces lint findings inline (no need to run CI).

### v2.2 — Component manifest expansion (Q4 2026)

- **+50 components** to reach 198 total. Net-new: combobox with async filter, command-palette with recent-items heuristic, conditional-form-step, payment-element variants, RTL-aware date picker, MENA-specific phone input, calendar grid with hijri overlay.
- **Per-component code emit** in 6 stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, vanilla HTML/CSS).
- **Component playground** at uxskill.laithjunaidy.com/playground — try the recommendation engine + see live component preview.

### v3 — The marketplace + the lock-in (2027)

- **Brand spec marketplace** — publish and discover community brand specs. Pay-to-publish to fund moderation.
- **Custom anti-pattern rules** — projects can define their own regex rules in `data/anti-patterns.local.json` (already shipped in v2; v3 adds discovery + sharing).
- **`uxskill plan`** — full multi-page site planning from a brief, not just one surface.
- **Figma plugin parity** — same recommendation engine, surfaced in Figma.

---

## Contributing

Issues and PRs welcome. Three high-leverage areas:

### Add an anti-pattern rule

1. Edit `data/anti-patterns.json` — add an entry with `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Add a test in `tests/linter/` — one file that triggers the rule, one that doesn't.
3. Run `uxskill lint tests/linter/should-trigger/<rule>.tsx` — confirm it fires. Run on `tests/linter/should-not-trigger/<rule>.tsx` — confirm it doesn't.
4. Open a PR.

### Add a brand spec

1. Create `data/brands/<slug>.json` with `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Add the corresponding prose at `references/brands/<slug>.md`.
3. Register in `data/brands/_index.json`.
4. Open a PR. Spec must be backed by primary-source references (the brand's actual product, public design system, or DESIGN.md if they publish one).

### Add a motion preset

1. Edit `data/motion-presets.json` — add an entry with `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. The preset must have a reduced-motion variant. No exceptions.
3. Open a PR.

### Process

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full process.
- Read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- New rules and brand specs are reviewed for: primary-source grounding, no overfitting to a single project, no emoji in any of the data, RTL-safe behavior where applicable.

---

## License, author, acknowledgments

### License

MIT. Use it, fork it, build on it. If it saves you from shipping AI slop, star the repo — it's the cheapest way to support it.

### Author

**Laith Aljunaidy** — solo founder of [Dot](https://thedotwallet.com), a MENA-first loyalty platform. Building ux-skill so the AI-generated frontend doesn't all look the same.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Site: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Acknowledgments

- The team at Anthropic for Claude Code and the skill / plugin architecture that made this distributable.
- Nielsen Norman Group, Laws of UX (lawsofux.com), and the UX research community whose work informs `data/ux-guidelines.json`.
- Every brand listed in `data/brands/` — their public design systems are the source of truth for the brand specs.
- The original v1 contributors: a single-shot Claude skill that became the seed for the v2 Python engine.
- The 8 popular Claude UX plugins we compared against — they raised the bar; this is our answer.

---

**ux-skill** · **v3.0.0-stable** · Built so Claude Code, Cursor, Windsurf, and every other AI coding tool output frontend that doesn't read as AI-generated.

> Star the repo at [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Install via `pip install uxskill` or `npx uxskill init` · Browse the comparison at [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
