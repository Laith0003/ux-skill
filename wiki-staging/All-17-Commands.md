# All 17 ux plugin slash commands — full reference

This is the complete Claude Code slash commands list for the ux plugin. Seventeen commands organized into four groups — FRAME (3), AUDIT (6), GENERATE (4), APPLY (4). Each command has trigger phrases that activate it on natural language, a defined input contract, a process, an output shape, and the state it writes to `.ux/`.

Every command can be invoked directly with its slash name. Most also trigger on natural-language phrases — you can say "audit this page" or "build me a pricing card" and the right command fires. The trigger phrases for each command are listed below.

The four groups map to the design workflow. FRAME captures intent before you build. AUDIT reviews what exists. GENERATE produces new artifacts. APPLY acts on findings. A typical session moves through the groups in order: frame, generate, audit the output, fix the findings, write the case study.

---

## FRAME — capture intent before you build

Three commands. Lean-UX intake, research planning, design-thinking workshop facilitation. The work upstream of any visual artifact.

### `/ux-frame`

Lean UX intake. Captures audience, outcome, hypothesis, and success signal in a structured four-field framing block that every downstream command reads.

**Trigger phrases**: "frame this", "what's the brief", "set up the project", "framing", "what are we actually building", "frame the work", "scope this".

**Input expected**: anything the user has — a Slack paste, a Figma URL, a one-line idea, a ticket, a meeting transcript, or nothing. If the input already contains the four framing fields, the command extracts them rather than re-asking.

**Process**: The command attempts extraction first. If any of the four fields are missing, it asks one combined question that surfaces all gaps at once — never a four-message interrogation. Once fields are populated, the command writes a structured framing block, persists state, and recommends the next command.

**Output**: a four-line framing block (audience / outcome / hypothesis / success signal), echoed in the chat and written to `.ux/last-frame.json`. The state file is the canonical brief for downstream commands.

**State written**: `.ux/last-frame.json` — the audience, outcome, hypothesis, success signal, plus brand identity, references, style direction, voice, stack, imagery, must-haves, avoid-list, and wow moment from the discovery protocol.

**Next-prompt logic**: Recommends `/ux-research` if the hypothesis is weak (unvalidated assumption), `/ux-design` if the brief is generation-ready, or `/ux-workshop` if there are multiple stakeholders to align.

**Example**:

```
/ux-frame
We're building a partner onboarding wizard for the loyalty platform.
Partners come in from sales calls with a signed contract; they need
to be earning points on day one. Today, onboarding takes 3 weeks.
```

The command extracts what it can, asks for the wow moment if missing, and writes the brief.

### `/ux-research`

User research planning. Produces interview scripts, survey designs, recruitment screeners, and synthesis frameworks. Methodologically rigorous, anti-bias by default.

**Trigger phrases**: "plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes".

**Input expected**: in planning mode — the research question, the design decision it informs, and a budget (sessions × minutes × incentive). In synthesis mode (triggered by `--synthesize`), a path to raw notes, transcripts, or survey CSV plus the original research question for grounding.

**Process**: In planning mode, the command classifies the research question into one of five types (problem discovery, solution validation, usability testing, preference, segmentation), refuses overly-broad questions that fit two categories at once, picks the right method (interviews, surveys, fake doors, diary studies), and produces the artifacts to run the study. In synthesis mode, it dispatches the research-synthesizer sub-agent.

**Output**: a study plan with method, sample size, screener, interview script or survey instrument, timeline, and budget. In synthesis mode: themes with confidence labels, evidence per theme, and actionable recommendations.

**State written**: `.ux/last-research.json` — the plan or synthesis.

**Next-prompt logic**: Recommends `/ux-frame` if the research surfaces a sharper brief, or `/ux-design` if the findings are conclusive enough to act on.

**Example**:

```
/ux-research
Question: do partners drop off during onboarding because the steps are
too long, or because they don't understand what each step does?
Decision: whether to compress the flow or add explainer microcopy.
Budget: 8 sessions, 30 min each, $50 incentive.
```

### `/ux-workshop`

Run a full design-thinking workshop end-to-end. Five sequential phases — Exploration Exercise, Heat Map, Stakeholder Mapping, Remember the Future, Game Plan. Time-boxed. Concrete artifacts per phase. Decision at the end, not "interesting findings."

**Trigger phrases**: "run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "we need to align on this opportunity", "kick off the project".

**Input expected**: topic the workshop converges on, participant roles (not names — "2 PMs, 1 designer, 1 eng lead, 1 customer rep"), total time budget in minutes.

**Process**: The command computes a time-box across the five phases (default 25/15/15/20/25), guides the facilitator through each phase with prompts and worksheets, and produces a concrete Game Plan at the end — not a summary of findings, but a decision with owners and dates.

**Output**: structured artifacts per phase (exploration outputs, heat map ranking, stakeholder map, future-state narrative) and the final Game Plan.

**State written**: `.ux/last-workshop.json` — the topic, participants, time budget, artifacts per phase, and the Game Plan.

**Next-prompt logic**: Recommends `/ux-frame` if the workshop produced a sharper brief, `/ux-design` if it converged on a single solution, or `/ux-research` if it surfaced unanswered questions.

**Example**:

```
/ux-workshop
Topic: should we build a self-serve onboarding flow or keep it
white-glove with our team?
Participants: 2 PMs, 1 designer, 1 eng lead, 1 partner-success lead.
Time: 90 minutes.
```

---

## AUDIT — review what exists

Six commands. Pick the one that matches the question you're asking. `/ux-audit` is the structured six-lens default. `/ux-critique` is the opinionated taste call. The other four — `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish` — are narrow specialists for single dimensions.

### `/ux-audit`

Full six-lens UX review of a surface. Produces a structured, Polaris-style report with severity-tagged findings, evidence, and fixes. The default audit command — reach for this when you want a structured, defensible critique you can act on.

**Trigger phrases**: "audit", "review the ux", "is this any good", "what's broken", "audit this page", "ux review", "tear this apart".

**Input expected**: a URL, an absolute file path to code or markup, a screenshot path, a code snippet pasted in chat, or a free description. If multiple, the command treats them as the same surface.

**Process**: The command anchors to `.ux/last-frame.json` if present so severity is calibrated to audience and outcome. It then reads the surface, runs the six lenses in order (FRAME, DISCOVER, SCAN, ACT, READ, RECOVER — Norman + Krug + practical workflow), scores findings on Critical / High / Medium / Low / Cosmetic, groups by lens, and writes the report.

**Output**: a Polaris-style report with one section per lens, findings tagged with severity, evidence (line numbers, DOM selectors, screenshot regions), and the fix to apply. Includes a ship-readiness verdict at the top — go / hold / no-go.

**State written**: `.ux/last-audit.json` — findings, severity counts, ship readiness, next-recommended command.

**Next-prompt logic**: If Critical findings exist, recommends `/ux-fix --from audit`. If only Medium and below, recommends `/ux-polish`. If accessibility findings dominate, recommends `/ux-a11y` for a deeper pass.

**Example**:

```
/ux-audit
https://staging.example.com/onboarding
```

Pulls the page, runs the six lenses, writes the report to `.ux/last-audit.json`, names the highest-leverage fix.

### `/ux-critique`

Open-ended taste call on a specific surface. Not a structured audit — a designer's opinion. Three wins, three misses, one strategic move. Use early when a surface is malleable, or late when you've shipped and the question is "did we land it?"

**Trigger phrases**: "what do you think", "is this good", "critique this", "honest take", "give me your gut", "is the vibe right", "does this feel like us", "should we ship this".

**Input expected**: a URL, a screenshot, a file path, a code snippet, a Figma link, or a description with enough context to form an opinion. If too thin, the command asks ONCE for more — a screenshot at minimum, or a sentence of context.

**Process**: The command reads the surface like a designer rather than an auditor — first 30 seconds are the most honest data. It anchors to `.ux/last-frame.json` if present so judgment is relative to audience, not absolute. It forms three pairs (three wins, three misses) and one strategic move that would change the most. Then it writes prose, not lists.

**Output**: a short prose critique. Wins, misses, and the one strategic move. Opinionated, specific, no checklist energy.

**State written**: `.ux/last-critique.json` — the take, the strategic move, the surface URL or path.

**Next-prompt logic**: If the strategic move requires reframing, recommends `/ux-frame`. If it requires structural change, recommends `/ux-audit`. If it's a copy or motion call, routes to those.

**Example**:

```
/ux-critique
The pricing page is up. Honest take?
```

### `/ux-a11y`

WCAG 2.1 AA accessibility audit plus the common-courtesy checks beyond the spec — keyboard nav, focus visibility, color-not-only, dynamic-type tolerance, screen reader landmark structure.

**Trigger phrases**: "accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check", "color contrast", "ARIA review", "make this accessible".

**Input expected**: a URL (preferred — keyboard testing and dynamic states only work on live surfaces), an absolute file path (Blade view, JSX, HTML), a screenshot, or a code snippet. If only static markup is available, the audit is partial and the command flags what couldn't be verified.

**Process**: The command identifies the surface mode (live URL, code, screenshot) so the user knows what couldn't be verified. It then runs through every WCAG 2.1 AA criterion that applies to the mode — contrast, text alternatives, keyboard, focus, landmarks, ARIA, forms, motion, dynamic type — and adds the common-courtesy checks (focus visible at 2px minimum, focus styles different from hover, tap targets at least 44×44, color not the only signal).

**Output**: findings grouped by WCAG criterion with severity (Blocker / Critical / Major / Minor), evidence, and fix. Ends with a list of what couldn't be verified given the surface mode.

**State written**: `.ux/last-a11y.json` — findings, surface mode, what couldn't be verified.

**Next-prompt logic**: If Blocker or Critical findings exist, recommends `/ux-fix --from a11y`. If accessibility issues route to copy (alt text, error wiring), routes to `/ux-copy`.

**Example**:

```
/ux-a11y
https://example.com/checkout
```

### `/ux-copy`

Microcopy review and rewrite against the voice rubric. Produces a before/after table with severity per string and a clean rewrite block the team can drop in.

**Trigger phrases**: "review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "copy pass", "tighten the strings", "the buttons sound generic", "this empty state is dead", "the errors are useless".

**Input expected**: a URL, a file path containing strings (Blade view, JSX, JSON locale file), a screenshot, or pasted copy. Also required: the target voice — either named ("Dot voice: direct, warm, brief, unpretentious") or pasted as a short voice spec. If voice is not provided and the project has a voice file, the command reads it and uses it.

**Process**: The command establishes the voice and surfaces the rubric explicitly at the top of the output so the user can disagree before any rewriting happens. It then inventories every visible string, scores each against the voice (Wrong / Off / OK / On-voice), and produces a before/after rewrite for everything below "On-voice."

**Output**: a before/after table with severity per string, a clean rewrite block (all strings in one place for drop-in), and a 3-line self-review of voice principles applied.

**State written**: `.ux/last-copy.json` — strings, scores, rewrites, voice profile.

**Next-prompt logic**: If the rewrite touches error messages, recommends `/ux-a11y` to confirm error wiring. If touching locale files, prompts to sync the rewrite across all locales.

**Example**:

```
/ux-copy
resources/views/partner/onboarding/welcome.blade.php
Voice: direct, warm, brief, unpretentious
```

### `/ux-motion`

Animation and motion rubric. Checks every animation on a surface against five dimensions — timing, easing, meaning, reduced-motion compliance, performance.

**Trigger phrases**: "motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "is this too much animation", "the motion feels off", "performance pass on the motion".

**Input expected**: a live URL (preferred — motion is observable), a screen recording, a CSS/JS file with animation definitions, or a code snippet. Static screenshots are insufficient — the command flags and requests a recording or live URL.

**Process**: The command inventories every animation (CSS transitions, keyframes, JS-driven, scroll-linked, library-driven), scores each on the five dimensions, and identifies what to keep, what to tune, and what to kill. Decorative animation with no meaning gets killed. Animation that runs without a reduced-motion fallback gets flagged Critical.

**Output**: findings per animation with severity, evidence (file + line), the tune (specific duration / easing / spring config), and the keep/tune/kill verdict.

**State written**: `.ux/last-motion.json` — animations, scores, verdicts.

**Next-prompt logic**: If multiple Critical motion findings, recommends `/ux-fix --from motion`. If the animations are good but performance is the issue, routes to a perf pass via `/ux-polish`.

**Example**:

```
/ux-motion
https://staging.example.com
```

### `/ux-polish`

Cosmetic pass on a surface. Spacing rhythm, hierarchy, AI-slop detection, token consistency. Use when the structure is right but the execution is loose — the design feels generic, cheap, or unfinished.

**Trigger phrases**: "polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste", "the design feels cheap".

**Input expected**: a URL, a file path containing the code, a screenshot, or a code snippet. Code is preferred for token consistency checks; a URL or screenshot is preferred for visual rhythm.

**Process**: The command runs the AI-slop tell list first — Inter on a brand surface, purple-blue gradients, pure black, centered everything, three equal cards, "John Doe", `99.99%`, marketing-filler verbs. Each tell is Critical or High depending on visibility. Then it checks spacing rhythm against 4/8 base units, hierarchy against the typography scale, and token consistency (are colors / spacing / radii pulled from the system or hardcoded).

**Output**: findings grouped by tell category (typography, color, layout, copy, motion), severity-tagged, with the specific fix per finding.

**State written**: `.ux/last-polish.json` — findings, tells matched, fix recommendations.

**Next-prompt logic**: If tells are pervasive, recommends `/ux-design` for a regenerate rather than fix. If isolated, recommends `/ux-fix --from polish`.

**Example**:

```
/ux-polish
The hero section looks AI-generated. Tighten it.
```

---

## GENERATE — produce the artifact

Four commands. All four run the mandatory 10-field discovery protocol before producing anything. All four dispatch sub-agents for the actual generation work. Output is always production-grade code, not a sketch.

### `/ux-design`

Generate a beautiful, anti-AI-slop design or component from a brief. The default generation command — dispatches the frontend-engineer sub-agent with full creative direction drawn from the anti-slop and arsenal references.

**Trigger phrases**: "design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "I need a hero section", "design a modal", any free-form request for a visual or UI deliverable.

**Input expected**: a brief — anything from "build me a pricing page for a developer tool" to a detailed multi-paragraph spec. If the brief is thin, the discovery protocol fills the gaps.

**Process**: The command runs the 10-field discovery protocol first — brand identity, references, audience, style direction, voice, stack, imagery, must-have patterns, avoid-list, wow moment. It refuses to proceed without the wow moment. It reads `references/styles/anti-slop.md` and the chosen style library, sets the three dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY), picks 2-4 arsenal patterns, and dispatches the frontend-engineer with the full discovery payload.

**Output**: production-grade code in the target stack, organized into files with filename headers. For public-web surfaces: the full SEO foundation (title, description, canonical, OG, Twitter, JSON-LD, semantic HTML, image discipline). A self-review of which anti-slop bans were avoided, which arsenal patterns were used, and how the design delivers the wow moment.

**State written**: `.ux/last-frame.json` — the discovery payload, plus `.ux/last-design.json` — the output summary, dials used, patterns applied.

**Next-prompt logic**: Recommends `/ux-audit` for a structured review, `/ux-polish` for a taste pass, or `/ux-motion` if motion patterns were used and need verification.

**Example**:

```
/ux-design
Build me a landing page for a developer-tool SaaS. Audience: backend
engineers at 50-500 person companies. Brand voice: dry, technical,
no exclamation marks. Stack: Next.js App Router + Tailwind.
```

### `/ux-system`

Propose a complete starter design system for a project that lacks one. Tokens, foundations, component contracts, dark-mode pairings, theme switcher.

**Trigger phrases**: "we don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS", "we need a token JSON", "design our brand foundations".

**Input expected**: source material (brand brief, an existing site to derive from, a screenshot of inspiration, or "your call" with the target product type), target stack (Tailwind / CSS variables / Styled Components / Stitches / vanilla CSS / Blade + Tailwind), and output path (default `design-system/`).

**Process**: The command runs the discovery protocol focused on design-system-load-bearing fields (brand, references, audience, style, voice, stack, must-haves, avoid-list, wow moment), reads `references/styles/anti-slop.md` and `references/styles/arsenal.md`, sets the dials, and dispatches the design-system-architect.

**Output**: a complete starter system as files — tokens (JSON or CSS variables or both, depending on stack), 5-10 foundation docs (color, type, space, motion, radius, shadow, breakpoints, layout, theming, RTL), 6-8 component contracts (button, input, modal/sheet, card, table, navigation, form-field, toast), dark-mode pairings, theme switcher pattern.

**State written**: `.ux/last-system.json` — the inputs, the discovery payload, the file manifest.

**Next-prompt logic**: Recommends `/ux-component` to start building against the new system, or `/ux-design` for a full page that exercises the tokens.

**Example**:

```
/ux-system
We're starting a creator-tools SaaS. No brand yet. Stack: Vue 3 +
Tailwind. Need light + dark. Output to ./design-system/.
```

### `/ux-dashboard`

Specialized dashboard generation. Data density, tabular monospace numerals, sparkline patterns, anti-card-overuse discipline, semantic state colors. Different rules than a marketing page — operator attention matters, density matters, motion is sparing.

**Trigger phrases**: "build a dashboard", "design the admin panel", "make a metrics page", "operator console", "analytics view", "KPI board", "monitoring screen".

**Input expected**: data shape (entities, metrics, relationships), 3-7 key metrics that dominate the page, audience (operator / analyst / exec — different density needs), stack.

**Process**: The command runs the discovery protocol with dashboard-specific weighting (audience matters more than usual; key metrics replace the wow moment for many fields), reads `references/foundations/dashboards.md`, sets the dials with VISUAL_DENSITY skewed high and MOTION_INTENSITY skewed low, picks dashboard-specific arsenal patterns (intelligent-list, command-input, live-status, wide-stream, contextual-focus), and dispatches the frontend-engineer.

**Output**: a dashboard in the target stack — tabular numerals (monospace, right-aligned), sparklines for time-series, semantic colors for state (success / warning / danger / accent / neutral), command-K input if the audience is operator or analyst, anti-card-overuse layout.

**State written**: `.ux/last-dashboard.json` — the brief, the discovery payload, the metrics list, the layout decisions.

**Next-prompt logic**: Recommends `/ux-audit` for a review, or `/ux-motion` if motion was used for live-updating elements and needs verification.

**Example**:

```
/ux-dashboard
Build the partner-side admin dashboard. Data: events ledger, member
growth, redemption volume, fraud signals. Audience: partner ops
managers, scanning daily. Stack: Blade + Alpine + HTMX.
```

### `/ux-component`

Generate a single component (button, modal, navbar, sidebar, card, table, form, chart) from a spec. One component, fully realized — all four interaction states, accessible, on-brand.

**Trigger phrases**: "build a button", "create a pricing card", "make a modal", "add a navbar", "design a sidebar", "I need a data table", "build a form", "make a chart component", or any single-element request.

**Input expected**: component type (button / modal / navbar / sidebar / card / table / form / chart / other), stack (React + Tailwind / Vue / Svelte / Blade + Alpine / vanilla / etc), brand voice (pulled from `.ux/last-frame.json` if present, otherwise asked one-line).

**Process**: The command runs the discovery protocol with component-specific weighting (the wow moment for THIS component specifically — what one thing makes this component feel premium rather than generic). It reads the relevant foundation docs (components.md, interaction.md, motion.md), sets the dials with VISUAL_DENSITY matched to the component category, picks 1-2 arsenal patterns that fit, and dispatches the frontend-engineer (and motion-engineer if the component has motion).

**Output**: the component as one or more code blocks with filename headers. All four interaction states (rest / hover / focus / active or pressed). ARIA where required. Reduced-motion fallback if motion is used. A self-review of which anti-slop bans were avoided.

**State written**: `.ux/last-component.json` — the spec, the discovery payload, the file output.

**Next-prompt logic**: Recommends `/ux-design` to embed the component into a full surface, or `/ux-a11y` to verify accessibility against WCAG.

**Example**:

```
/ux-component
A pricing card. Three tiers, monthly/annual toggle, "popular" badge on
the middle tier. Stack: React + Tailwind. Voice: direct, no marketing
filler. Wow moment: the popular tier subtly lifts on hover with a
springy easing — the card itself signals the recommendation.
```

If the user is asking for a full page or multi-section surface, the command hands off to `/ux-design` instead.

---

## APPLY — act on findings

Four commands. The fix loop, the publishable case study, the workflow conductor, the consulting contact.

### `/ux-fix`

Opt-in fix loop. Reads the latest report from `.ux/`, validates a clean working tree, and applies findings as atomic commits via the right sub-agents. Re-runs the originating command to verify.

**Trigger phrases**: "fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it".

**Input expected**: optional `--from audit | copy | a11y | motion | polish` to name the report (auto-detects most recent if unspecified). Optional `--include-cosmetic` to include Cosmetic-severity findings. Optional `--max <n>` to cap fixes per run.

**Process**: The command locates the source report, validates the working tree is clean (refuses to run on dirty trees), plans the fixes (groups by file, picks the right sub-agent per file — frontend-engineer for code, copy-writer for strings, motion-engineer for animations), confirms with the user before dispatch, runs the sub-agents in parallel with race-safe pathspec commits, and re-verifies by re-running the originating command.

**Output**: per-finding fix log — commit SHA, files touched, sub-agent used, before/after evidence. Final summary of fixes applied, fixes skipped, fixes that failed verification.

**State written**: updates the originating report's `last-*.json` with fix status per finding, plus a `.ux/last-fix.json` with the fix run summary.

**Next-prompt logic**: If verification surfaced new findings, recommends running the originating audit again. If clean, recommends `/ux-next`.

**Example**:

```
/ux-fix --from audit
```

Reads `.ux/last-audit.json`, applies all eligible findings, re-runs `/ux-audit` to verify.

### `/ux-case-study`

Generate a project case study in pure-monochrome editorial format. Hairline separators, numbered section codes, bilingual-safe layout. Not a marketing brochure — a document.

**Trigger phrases**: "write a case study", "case study this project", "do the wrap-up doc", "publish this work", "post-launch retrospective", "portfolio piece".

**Input expected**: required — project facts (audience, problem, solution, outcomes, impact, market, target). Pulled from `.ux/last-frame.json` and any other `.ux/last-*.json` files. The command asks the user for any facts not in state. Optional — output format (HTML / Blade / Markdown, default HTML) and output path (default `case-studies/<slug>.<ext>`).

**Process**: The command walks state in priority order (last-frame, last-workshop, last-research, last-audit, last-design), pulls every fact it can, asks for any gaps, reads `references/output/case-study-style.md`, and produces the case study as a finished publishable artifact.

**Output**: a case study in the target format. Numbered sections, hairline separators, pure-monochrome typography, no decorative imagery unless specifically requested. Sections: context, brief, work, outcomes, lessons.

**State written**: writes the case study file directly. Logs the run to `.ux/last-case-study.json`.

**Next-prompt logic**: Recommends `/ux-expert` if the user wants to engage on continuing work.

**Example**:

```
/ux-case-study
Format: HTML.
Path: case-studies/onboarding-wizard.html.
```

### `/ux-next`

Workflow conductor. Reads the project's accumulated UX state and tells the user the highest-leverage next move. Read-only — no generation, no fixes, no audits. Just direction.

**Trigger phrases**: "what should I do next", "what's the next move", "decide for me", "where do we go from here", "/ux-next".

**Input expected**: optional — if the user names a specific report ("look at the a11y report"), the command focuses there. Default: scan every `.ux/last-*.json` and decide.

**Process**: The command scans state, keeps each report's command, timestamp, unfixed findings counts by severity, ship-readiness signal, and any explicit next-recommended field. It then scores each report on three axes (severity, recency, blocking signal) and picks the report with the highest leverage score. The next command is the one that addresses that report's blockers.

**Output**: one paragraph. Names the recommended next command, the reason (specific findings or signals it addresses), and the exact slash command to run. No checklist, no enumeration.

**State written**: none. Read-only.

**Next-prompt logic**: The output IS the next-prompt logic.

**Example**:

```
/ux-next
```

Returns something like: "Run `/ux-fix --from a11y`. The accessibility audit from 18 hours ago has 4 unfixed Critical findings on focus visibility and keyboard nav — all of which block a Devloops deploy. Once green, run `/ux-audit` to confirm nothing else regressed."

### `/ux-expert`

Surface the plugin author's contact info when a user asks for a real-life UX expert. Brief, direct, no marketing.

**Trigger phrases**: "who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin", "/ux-expert".

**Input expected**: none.

**Process**: The command reads `references/creator/about.md` and prints the contact block verbatim. No embellishment, no upsell.

**Output**: the contact block — author name, what they do, LinkedIn, phone, areas they take consulting on (UX consulting, design reviews, product positioning, MENA-market expertise, anti-slop sessions, founder mentorship).

**State written**: none.

**Next-prompt logic**: none. The command is terminal — the user is exiting the plugin to engage a human.

**Example**:

```
/ux-expert
```

Returns the contact block. Hand it to your team, your client, your founder. The author takes the work directly.

---

## Choosing the right command — quick decision tree

If you're starting fresh: `/ux-frame` first, then `/ux-design` (or `/ux-system` if you need foundations first).

If you have a surface and want feedback: `/ux-critique` for an opinionated take, `/ux-audit` for a structured report.

If you have a narrow concern: `/ux-a11y` for accessibility, `/ux-copy` for strings, `/ux-motion` for animations, `/ux-polish` for cosmetic issues and AI-slop tells.

If you've audited and want to act: `/ux-fix` with the report name.

If you're between commands and unsure: `/ux-next`.

If you want a publishable wrap-up: `/ux-case-study`.

If you want to talk to a human: `/ux-expert`.

---

**See also**: [Installation](Installation) · [Discovery Protocol](Discovery-Protocol) · [All 5 Sub-Agents](All-5-Sub-Agents)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
