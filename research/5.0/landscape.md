# ux-skill 5.0: landscape and standards horizon

Internal research, compiled 2026-11-02. Not legal advice. Repo read: README.md, docs/compare.html, PLAN-4.0.md (PLAN-4.1.md does not exist in the repo), data/anti-patterns.json, engine/linter.

Verification legend, used on every fact below:

- [V] verified this session against a primary source (vendor repo or docs, standards body page, package registry, law firm alert quoting the regulation) or against machine data (web-features npm package, npm and PyPI registries, shields.io star counts).
- [S] secondary source only (news, vendor blog, search summary of a first-party page that was not opened).
- [U] could not verify, or sources conflict. Do not repeat without checking.
- [K] well-known background fact, not re-fetched this session.

---

## Part A. Recommendations for 5.0

### A1. Positioning

1. Stop competing on "taste". The generation and taste space is now owned by very large skills: Anthropic's own frontend-design skill (anthropics/skills, 187k stars), ui-ux-pro-max (144k), taste-skill (108k), open-design (105k), impeccable (100k), hallmark (46k) [V, shields.io 2026-11-02]. ux-skill has 90 stars [V]. A star race is lost.
2. Position 5.0 as the offline, deterministic quality gate and design-system compiler that any agent or skill can call, with compliance-grade evidence. The differentiators nobody else combines [V from READMEs]:
   - No network, no telemetry, no LLM. Impeccable fetches visual directions from its catalog on every new design and keeps telemetry that only stops the record, not the request; open-design sells credits; taste-skill takes 30 to 45 minutes and a few hundred thousand tokens per build.
   - A DTCG 2025.10 compiler with a WCAG gate that refuses to write a failing system.
   - Arabic and RTL as a first-class mode.
   - 171 rules versus impeccable's 62 deterministic rules.
   - Same input, same bytes: reproducible reports that can sit in an audit file.
3. Sell the gate to the demand that law is creating (A4): every finding mapped to a WCAG 2.2 success criterion and to an EN 301 549 V4.1.1 clause, and a dated report that says what was checked automatically and what still needs a person. Be honest that automated checks cover only part of WCAG.
4. Housekeeping before any 5.0 claim:
   - PyPI and npm both show uxskill 3.2.0 (PyPI release 2026-09-23) while README and the release commit say 4.0.0 [V]. Publish 4.x before docs say it shipped.
   - docs/compare.html is stale: it lists ui-ux-pro-max at 83,958 stars (now 144k), hallmark at 2,164 (now 46k), and omits impeccable, Anthropic's frontend-design, Vercel's web-design-guidelines and Google's DESIGN.md [V]. A stale comparison page undermines the "honest" framing.

### A2. Checks to add

Grouped by what drives the demand. Severity suggestions in brackets.

**Standards-driven (WCAG 2.2 delta, now in EN 301 549 V4.1.1)**

The engine references 1.4.3, 1.4.11, 1.4.6, 1.4.8, 2.3.3, 2.5.8, 1.4.10, 2.4.7, 1.4.1, 2.2.2 and 1.4.4, but none of the other WCAG 2.2 additions [V, grep of engine/]. Add to `lint --render`:

- 2.4.11 Focus Not Obscured (Minimum): tab through the page and fail when the focused element is fully covered by a sticky header, cookie banner, chat widget or fixed footer. This is a real Chromium check and a common failure of AI pages with sticky navs. [high]
- 2.5.8 Target Size: already referenced; measure rendered hit areas (24 by 24 CSS px or spacing exception) at phone width, not only declared sizes. [high]
- 1.4.12 Text Spacing: inject the WCAG text-spacing overrides (line height 1.5, paragraph 2x, letter 0.12em, word 0.16em) and fail on clipped or overlapping text. Fixed-height text blocks already exist as a static rule; this is the rendered proof. [medium]
- 1.4.10 Reflow at 320 CSS px and 1.4.4 resize to 200 percent: horizontal scroll and clipped content. [high]
- 3.3.8 Accessible Authentication: static check for `onpaste` prevention or `autocomplete="off"` on password and one-time-code fields. [high]
- 3.3.7 Redundant Entry and 1.3.5: missing `autocomplete` tokens on name, email, address and phone fields. [medium]
- 2.5.7 Dragging Movements: drag-only sliders, sortable lists or carousels without a single-pointer alternative (heuristic). [medium]
- 3.2.6 Consistent Help: across multi-page builds, help links or contact in a different relative order. [low]
- Keep full coverage of the six most common WebAIM failures, which are what complaints and demand letters cite: low contrast 83.9 percent of home pages, missing alt 53.1, missing form labels 51, empty links 46.3, empty buttons 30.6, missing lang 13.5 [V, WebAIM Million 2026]. Most already exist as rules; make sure each also runs on the rendered DOM, where framework output hides empty links and buttons.

**Platform-driven ("prefer the platform", gated by a Baseline policy)**

- Add a project setting `baseline: widely | newly | <year>` and only suggest a feature that meets it. Bundle the `web-features` dataset (npm, version 3.44.0 published 2026-10-22 [V]) so the check stays offline and deterministic; print the dataset version in every report. Neighbours already do this for compatibility (stylelint-plugin-use-baseline 1.4.8, eslint-plugin-baseline-js 0.7.7 [V npm]); ux-skill's angle is design quality, not compatibility.
- Suggestions, each with its Baseline status from Part B3:
  - Hand-rolled JS dropdowns, tooltips and menus positioned with scroll and resize listeners: use `popover` (Baseline newly 2025-01-27) plus anchor positioning (core properties interoperable since 2026-01-13, umbrella feature not yet Baseline; see B3), or a floating library as fallback.
  - `onclick` that only opens a dialog or popover: `commandfor` and `command` invoker buttons (Baseline newly 2025-12-12).
  - A div-based fake `<select>`: native `<select>` with `appearance: base-select` as progressive enhancement (Chrome 135, Safari 27, not Firefox; not Baseline).
  - Display headings with no `text-wrap: balance` (Baseline newly 2024-05-13), and prose with `text-wrap: pretty` as optional enhancement (not Baseline: Chrome and Safari only). [low, suggestion only]
  - Duplicated dark-mode token blocks: `color-scheme` plus `light-dark()` (Baseline newly 2024-05-13).
  - Component layouts switching on viewport media queries: container queries (Baseline widely 2025-08-14).
  - Hex or HSL ramps in a token file: OKLCH (Baseline widely 2025-11-09); `color-mix()` (widely 2025-11-09) and relative color syntax (newly 2024-09-16) for state colors.
  - JS autosizing textareas: `field-sizing: content` (Baseline newly 2026-06-16).
  - Accordions animated in JS: `<details>` with `::details-content` (newly 2025-09-16) and optional `interpolate-size: allow-keywords` (Chromium only).
  - Theme switch or route change cross-fades in JS: same-document View Transitions (newly 2025-10-14), always inside a reduced-motion guard.
  - Scroll-linked reveals done with scroll listeners or IntersectionObserver loops: `animation-timeline` as progressive enhancement only (not Baseline: no Firefox) and only with `prefers-reduced-motion` handling.
- Parser and contrast-engine updates so modern code is measured, not skipped (these are false-negative risks, the most serious kind for a gate):
  - Resolve `light-dark()` by evaluating both branches under each scheme.
  - Resolve relative color syntax, `color-mix()` and `contrast-color()` (Baseline newly 2026-04-10) before computing ratios.
  - Parse native CSS nesting (Baseline widely 2026-06-11), `@scope` (newly 2026-03-24), `@layer` and `@container` style queries (newly 2026-05-19) so selector-scoped rules see the right blocks.

**2026 AI tells (update the slop catalogue)**

The purple-gradient and Inter era is now the old tell; the current defaults are documented by the vendors themselves (B4). Add a "tells 2026" pack, keep existing ids stable:

- Cream page near #F4F1EA with a high-contrast serif display and a terracotta accent near #D97757 (Anthropic's frontend-design names this as cluster 1, and notes #D97757 is Anthropic's own accent) [V].
- Near-black page with a single acid-green or vermilion accent [V].
- Broadsheet kit: hairline rules, zero radius, dense columns used regardless of subject [V].
- SaaS card kit: one radius on every card, the same `rgba(0,0,0,.1)` shadow under each, gradient washes as decoration [V]. Partly covered by border-radius-2xl-default and three-equal-card-grid; extend to "one radius regardless of hierarchy".
- Template chrome [V, frontend-design; hallmark; impeccable]:
  - tracked ALL-CAPS eyebrow above every heading (eyebrows-over-budget exists; also flag tracked-capital labels in general),
  - meta strings joined with middle dots `A . B . C`,
  - labels built as `WORD`, spaced dash, fragment,
  - tinted near-black (#0B0B0B, #111) standing in for black,
  - monospace face for small data labels,
  - a right arrow appended to link and button text,
  - one accented word in a headline (italic, bold or colored),
  - numbered 01 / 02 / 03 markers on content that is not a sequence,
  - a rounded-square icon tile above every heading,
  - cards nested inside cards, gray text on colored backgrounds,
  - colored side-tab borders on every card, colored status dots on every element,
  - fade-and-slide-up on every section and hover transitions on every card.
- Page-level tells from hallmark [V]: email sign-up at the end of every page; a hero that misses its screen (headline or CTA below the first viewport at phone width); a page of empty frames; and "a form that says thanks without sending anything" (render check: submit handler that changes UI state but has no `action`, no fetch, no navigation).
- Copy tells: hedging ("may help you", "can potentially") and vague aspirational headlines ("Build the future of", "Your all-in-one platform", "Scale without limits") [S, 925studios]; UI text that states the obvious about its own element [V, HN thread, small sample].
- A sparkle icon with no AI disclosure (Red Hat's AI guidelines forbid sparkles without disclosure) [S]. Pairs with the AI Act pack below.

**EU AI Act Article 50 pack (opt-in, `eu-ai-transparency`)**

- Chat or assistant widgets (common component names, `role="log"` chat regions, assistant avatars) with no visible text saying the user is talking to an AI system (Art. 50(1)) [V obligation; heuristic detection].
- AI-generated imagery or text blocks marked as such in code (data attributes, alt text, CMS fields) but with no visible label, or with a label that is color-only or icon-only without a text alternative. The Code of Practice refers to "the publicly available EU icon or equivalent labels" [V]; ux-skill should check the label exists and is accessible, not design the icon.
- Keep it opt-in and frame findings as "disclosure missing", never as a legal verdict.

### A3. Rules to retire or update because the platform changed

| Rule id | Problem now | Change |
|---|---|---|
| h-screen-no-dvh-fallback | Its fix says to keep 100vh as "the legacy fallback for browsers that lack dvh". Viewport unit variants are Baseline widely available since 2025-06-05 [V]. | Rename to `full-height-uses-vh`. Flag bare `100vh` or `h-screen` on full-height sections; recommend `svh` for heroes (stable, no jump) and `dvh` only where resizing is wanted. Drop the fallback advice. |
| glass-without-fallback | Its "why" says backdrop-filter is unsupported on Firefox and older Safari. backdrop-filter is Baseline newly available since 2024-09-16 (Firefox 103, Safari 18) [V]. | Reframe as legibility: text on a blurred surface needs an opaque or high-alpha background so contrast holds over any content behind it. Mention `prefers-reduced-transparency` (Chrome 119 only, not Baseline [V]) as an optional enhancement. |
| image-format-jpg-no-webp-avif | Says picture with AVIF "has been universal since 2023". AVIF was Baseline newly 2024-01-25 and widely 2026-07-25 [V]. | Fix the date claim. Consider allowing a bare `<img>` that points at `.avif` or `.webp` directly, now that AVIF is widely available. |
| exit-cut-by-display-none | Correctly suggests `allow-discrete`. | Also accept `@starting-style` (Baseline newly 2024-08-06) and `transition-behavior: allow-discrete` (newly 2024-08-06) as passing patterns, including `overlay` for popover and dialog exits. |
| animating-layout-properties | Fix offers the grid-rows trick only. | Accept `interpolate-size: allow-keywords` or `calc-size()` (Chromium only) when paired with a non-animated fallback, and `::details-content` (Baseline newly 2025-09-16). |
| arbitrary-z-index-9999 | Fix offers only a z-scale token map. | Add: overlays belong in the top layer (`popover`, `<dialog>`), which removes the z-index race entirely. |
| tooltip-on-required-info | Fix says "aria-describedby popover". | Point to `popover="hint"` and `interestfor` only as future options (both non-Baseline: popover hint Chrome 151 and Firefox 153; interest invokers Chrome 142 only, no spec merge confirmed [V web-features; U spec]); the shippable fix stays visible text or a click or focus popover. |
| theme-switch-animates-everything | Fix suspends transitions with a class. | Add the View Transitions option (Baseline newly 2025-10-14) with a reduced-motion guard. |
| text-align-justify-web | Says CSS has "none of the hyphenation" a print justifier relies on. `hyphens` is Baseline widely since 2026-03-18 [V]. | Soften the why: justification still makes rivers at web measures; if a brand requires it, `hyphens: auto` with a correct `lang` is now dependable. |
| css-import-render-blocking | Fine, but `@import url(...) layer(...)` is how cascade layers are often wired. | Allow a layer import of a local token or reset file, like the tokens.css exception. |
| purple-to-blue-gradient, inter-as-display, default-font-only, gradient-mesh-purple-pink | Still valid, but no longer the main tell (B4). | Keep; lower to medium where they are high; move them into a "tells 2023 to 2025" group so the scoring does not reward a page for merely avoiding purple. |
| outline-none-no-focus-visible, inert, search | `:focus-visible` widely available since 2024-09-14, `inert` widely 2025-10-11 [V]. | No change in logic; drop any "polyfill" or fallback wording in fixes if present. |

### A4. Standards and law deadlines that create demand

| Date | Event | Status |
|---|---|---|
| 28 Jun 2025 | European Accessibility Act applies; enforcement is national and complaint-driven, with few fines so far | [K] date, [S] enforcement picture |
| 2 Aug 2026 | EU AI Act Article 50 transparency duties apply (not delayed by the Omnibus) | [V] |
| 2 Sep 2026 | EN 301 549 V4.1.1 published, adopts WCAG 2.2 Level AA | [V] |
| 10 Sep 2026 | WCAG 3.0 Working Draft: single conformance level plus reporting tiers; contrast measure still "to be determined" | [V] |
| about 30 Nov 2026 | EN 301 549 V4.1.1 expected in the Official Journal, which gives presumption of conformity under the EAA | [V] as Deque's expectation, not a fact yet |
| 2 Dec 2026 | Article 50(2) machine-readable marking deadline for generative systems already on the market before 2 Aug 2026 | [V] (one outlier source says Dec 2027 [U]) |
| 26 Apr 2027 | ADA Title II web rule: state and local governments of 50,000 or more (moved from 24 Apr 2026 by DOJ interim final rule, Apr 2026) | [V] dates, [U] litigation against the extension |
| 26 Apr 2028 | ADA Title II: entities under 50,000 and special districts | [V] |
| 2 Dec 2027 and 2 Aug 2028 | AI Act high-risk obligations (Annex III, Annex I) | [V], not relevant to ux-skill checks |
| 28 Jun 2030 | EAA transition ends for services using products already in use before June 2025 | [K] |

What this means for 5.0:

- Ship WCAG 2.2 delta checks (A2) before the EN 301 549 V4.1.1 citation lands. Vendors already tell buyers to target WCAG 2.2 AA now.
- ADA Title II stays on WCAG 2.1 AA [V]; a WCAG 2.2 gate covers it.
- Treat WCAG 3 as horizon, not target. Do not build a WCAG 3 score. Optionally tag findings with the draft's requirement tags (Physical harm, Risk, Barrier, Friction) as a severity vocabulary [V the tags exist in the Sep 2026 model; they may change].
- Keep the WCAG 2 contrast ratio as the only gate. APCA is not adopted, and the WCAG 3 draft says the contrast algorithm "is yet to be determined" [V]. APCA can stay as an informational second number.

### A5. Ten recommendations in priority order

1. Reposition as the offline, deterministic gate and compiler with compliance-grade evidence; stop competing on taste and stars (A1).
2. Add WCAG 2.2 delta checks to the rendered pass: 2.4.11 focus not obscured, rendered 2.5.8 target size, 1.4.12 text spacing, 1.4.10 reflow, 1.4.4 zoom, plus static 3.3.8 and 3.3.7 (A2).
3. Ship `uxskill audit --standard` with WCAG 2.2 AA, EN 301 549 V4.1.1 and ADA Title II (WCAG 2.1 AA) profiles: a dated, reproducible report with the ruleset and web-features versions and a manual-check list. Time it for the EN 301 549 citation (about 30 Nov 2026) and the ADA Title II 26 Apr 2027 date.
4. Refresh the slop catalogue to the 2026 defaults (cream, serif and terracotta; near-black and acid accent; broadsheet; SaaS card kit; template chrome; fake-submit forms). Demote the purple and Inter rules so avoiding purple no longer scores well on its own.
5. Make the contrast engine and CSS parser read modern CSS: `light-dark()`, relative color, `color-mix()`, `contrast-color()`, nesting, `@scope`, `@layer` and style queries. Without this the gate silently skips modern code.
6. Add a Baseline policy setting backed by the bundled web-features dataset, and a "prefer the platform" rule family (popover, invokers, anchor, base-select, container queries, OKLCH, field-sizing, details-content, view transitions), suggestion-level only.
7. Retire or rewrite the outdated rules in A3 (dvh fallback, glass fallback, AVIF date, exit and layout animation, z-index, justify).
8. Interop: ingest, lint-compatible emit and round-trip Google's DESIGN.md (alpha, Apache-2.0, 29k stars, has its own lint, diff and DTCG export), and emit the DTCG Resolver 2025.10 for modes. Make the 160 brand specs valid DESIGN.md so Stitch and every agent can use them.
9. Close the agent-loop gap: lint on every write through a hook (impeccable and hallmark already gate on every edit or build), SARIF and GitHub annotations, stable exit codes, and an MCP tool that returns a fix per finding. 4.2 planned this; it is table stakes now.
10. Add the opt-in EU AI Act Article 50 pack: AI chat widgets without disclosure, AI content labels that are missing or not accessible, sparkle icons without disclosure. Publish 4.x to PyPI and npm and refresh compare.html before announcing 5.0.

---

## Part B. Evidence

### B1. Competitors and neighbours (late 2026)

Star counts from shields.io on 2026-11-02 [V]. Package versions from the npm registry on 2026-11-02 [V].

#### B1.1 Design and taste skills for coding agents

**Anthropic frontend-design skill** (anthropics/skills, repo 187k stars) [V SKILL.md]
- What: prose guidance only, model-invoked. A design process (plan as 4 to 6 named hex colors, typefaces, layout, principles; review the plan against the brief; build; self-critique with screenshots). Lists the 2026 AI default clusters (B4) and copy rules (active voice, consistent action names, errors that do not apologize).
- Measures: nothing deterministically; no checker.
- Licence: "Complete terms in LICENSE.txt" [U type not checked]. Free, ships with Claude Code marketplace. Install counts of 1.1 million on directories [S].
- ux-skill ahead: deterministic checks, token compiler, WCAG gate, RTL. Behind: it is the default in the most-used agent and its calibration list is current; ux-skill's rules should encode that list.

**impeccable** (pbakaus/impeccable, 100k stars; npm `impeccable` 4.8.0, 2026-10-26, Apache-2.0) [V README, npm]
- What: one skill, 24 commands (bolder, quieter, distill, colorize, typeset, layout, animate, delight, overdrive, critique, audit, polish, harden, clarify, adapt, optimize, onboard, live, generate, shape, init, document, extract). Writes PRODUCT.md and DESIGN.md. Live mode hot-swaps variants in a running dev server. Started from Anthropic's frontend-design skill.
- Measures: 62 deterministic rules, no LLM; `detect` on source (pattern rules) and on a URL using the installed Chrome or Edge (contrast, tiny text, overflow); critique scores against usability heuristics; audit ranks P0 to P3. Design hook scans every UI file the agent edits. Chrome extension overlay. GitHub annotations, JSON, exit codes.
- Network: fetches visual directions from the impeccable.style catalog when a new design starts; turning telemetry off does not stop that request [V].
- Supports about 19 harnesses.
- ux-skill ahead: 171 rules, offline with no catalog fetch, DTCG compiler and WCAG gate, components and section contracts, Arabic and RTL, brand specs. Behind: distribution, hook on every edit, live variant iteration, Chrome extension, CI annotations, critique and P0 to P3 framing.

**taste-skill** (Leonxlnx/taste-skill, 108k stars; MIT) [V README]
- What: one skill, `design-taste-frontend`, built from a study of 247 curated sites; deals three of 20 researched directions; uses credited open-archive photographs; app-screen route since v2.1.
- Measures: checks the page in a real browser at three widths and "fails it on slop"; self-review of screenshots up to three rounds; v2.1 frame checks (clear title on first screen, equal margins, no lopsided sections, no random blank stretches).
- Cost: 30 to 45 minutes and a few hundred thousand tokens per build [V].
- ux-skill ahead: speed and cost (deterministic, seconds), reproducibility, token output. Behind: art direction depth, imagery sourcing, popularity.

**hallmark** (Nutlope/hallmark, 46k stars; MIT; made by Together AI) [V README]
- What: fifty themes as "materials", deals three, builds from the job of the page, custom mode.
- Measures: lints in a real browser with tiered gates: Floor (contrast, focus, reduced motion, invented facts, broken phone layout) never ships; Reflex gates (model defaults) can be overruled on the record; Finish checks never block. A fresh-context reviewer has the last word. Named tells: eyebrow above every heading, tracked-capital labels, one colored word in a headline, empty frames, hero that misses its screen, email sign-up at the end of every page, a form that thanks without sending.
- ux-skill ahead: rule count, standards mapping, compiler. Behind: the tiered-gate framing (Floor, Reflex, Finish) is a clearer story than a 0 to 100 score; consider adopting it.

**ui-ux-pro-max** (nextlevelbuilder, 144k stars; MIT; `uipro-cli` 2.2.3 on npm, 2026-01-29) [V]
- What: BM25 search over CSV manifests; README claims 192 industry reasoning rules and 119 UX guidelines; design-system generation via CLI; many harness targets.
- Measures: no standalone linter found in README [V absence in README only].
- ux-skill ahead: linter, rendered checks, compiler. Behind: reach.

**open-design** (nexu-io, 105k stars; Apache-2.0) [V README]
- What: a design agent workspace (templates, decks, video templates), paid "OpenDesign Go" credits ($8 first month promotion).
- Measures: "Artifact lint API plus 5-dimension self-critique pre-emit gate".
- ux-skill ahead: deterministic and offline. Different category (workspace).

**Vercel web-design-guidelines skill** (vercel-labs/agent-skills, 33k stars) [V README]
- What: reviews UI code against "100+ rules covering accessibility, performance, and UX" (aria labels, focus states, forms). Mechanism (LLM review against a guideline file vs deterministic) [U].
- ux-skill ahead if Vercel's is LLM-judged: determinism. Behind: brand and reach with Next.js users.

**Google DESIGN.md** (google-labs-code/design.md, 29k stars; Apache-2.0; npm `@google/design.md` 0.4.0, 2026-07-27; format version "alpha") [V README, npm]
- What: a format for describing a visual identity to coding agents: YAML tokens plus prose rationale. Used by Google Stitch.
- Measures: `lint` (spec validity, broken token references, WCAG contrast of component pairs), `diff` (token and prose regressions), `export` to Tailwind v3 JSON, Tailwind v4 `@theme`, and DTCG.
- Relevance: ux-skill names its 160 brand specs DESIGN.md. Making them valid under Google's format is cheap reach.

**google-labs-code/stitch-skills** (8.7k stars) [V stars]. Google Stitch itself: free in Google Labs with usage limits that sources disagree on; March 2026 design agent; DESIGN.md sync [S].

#### B1.2 AI site and app builders and their guardrails

| Product | Quality guardrails found | Pricing | Status |
|---|---|---|---|
| Vercel v0 | Design Mode (visual edit), Design Systems 2.0 import from GitHub and Figma; no accessibility or quality checks named on the pricing page | Free $0, Plus $30 per user per month, Business $100 per user per month, Enterprise custom | [V] pricing page; [S] Design Systems 2.0 date (Feb or Jun 2026, sources conflict) |
| Lovable | Basic security scan runs automatically on publish (RLS policy lint, schema review), deep scan on demand, admins can block publish on errors; no accessibility gate found | Free with daily credits; Pro, Business, Enterprise (figures not captured) | [S] security scan (first-party docs via search summary); [V] plan names |
| Bolt.new | Design-system imports (Material UI, Chakra, shadcn and others); no accessibility audit found | not checked | [S] |
| Replit Agent | Design Mode (Nov 2025), Figma import, self-testing agent; no accessibility audit found | not checked | [S] |
| Claude Design (Anthropic Labs) | Builds a design system from codebase and design files; export HTML, PDF, PPTX, Canva, Claude Code handoff; research preview since 17 Apr 2026 for Pro, Max, Team, Enterprise | included in plans | [S] news coverage; Anthropic announcement page exists but was not opened |
| Figma (see B1.4) | Agent, MCP write to canvas | seats | [V] |

Pattern: builders gate security, not design quality or accessibility. The AudioEye study (B4) tested Lovable among five tools and found task-blocking issues on 13 of 15 sites [S]. That is the gap a deterministic gate fills.

#### B1.3 Design lint and accessibility engines

| Tool | What it measures | Licence, version | Notes |
|---|---|---|---|
| axe-core | Rendered DOM rules mapped to WCAG A, AA and best practice; 4.11 added RGAA tags; 4.11.1 fixed a contrast-rule skip | MPL-2.0; 4.14.0 (2026-10-05); @axe-core/cli 4.14.0 | [V] npm; [S] 4.11 notes. The de facto engine; ux-skill should not reimplement generic a11y rules axe already has, and could optionally call axe in render mode and merge results |
| Lighthouse | Performance insights (old audits removed in 13), accessibility subset of axe, agentic-browsing category added in 2026 | Apache-2.0; 13.6.0 (2026-10-27) | [V] npm; [S] 13.2 notes |
| Chrome DevTools MCP | Lets agents drive Chrome: Lighthouse, traces, network, a11y tree | Apache-2.0; 1.12.0 (2026-10-22) | [V] npm. Agents can now render pages themselves; ux-skill's value is the deterministic judgement, not the browser |
| Playwright MCP | Browser automation for agents | Apache-2.0; 0.0.84 (2026-10-31) | [V] npm |
| IBM Equal Access accessibility-checker | Rendered checks | Apache-2.0; 4.0.34 (2026-09-08) | [V] npm |
| pa11y | Rendered checks (axe or HTML_CodeSniffer) | LGPL-3.0; 10.0.0 (2026-08-28) | [V] npm |
| Storybook addon-a11y | axe per component story | MIT; 10.6.5 (2026-10-27) | [V] npm |
| eslint-plugin-jsx-a11y | Static JSX a11y rules | MIT; 6.10.2, last release 2024-10-26 | [V] npm; stale, an opening for static JSX rules |
| @eslint/css, stylelint-plugin-use-baseline, eslint-plugin-baseline-js | Baseline compatibility lint for CSS and JS | Apache-2.0 / MIT; 2.0.1, 1.4.8, 0.7.7 | [V] npm; [K] @eslint/css ships a use-baseline rule |
| Project Wallace css-analyzer | CSS metrics: token usage, specificity, complexity | MIT; 9.9.5 (2026-10-27) | [V] npm |
| @lapidist/design-lint | Design token governance lint | MIT; 8.0.0 (2026-05-12) | [V] npm |

ux-skill ahead: it is the only one that judges design defaults (slop), binds checks to its own token system, and covers RTL typography. Behind: axe's rule maturity and ecosystem; no Baseline awareness; no SARIF.

#### B1.4 Figma's agent features

- Config 2026 (announced 24 Jun 2026) [V Figma forum post]: Figma agent in design files, open beta on all paid plans (generate and remix designs, automate tasks, give design feedback, attach skills and third-party tools); agent in FigJam and Slides coming soon; code layers coming soon (from a frame, the agent, or a cloned repo); generative plugins open beta; custom shaders exportable via MCP.
- Library guidelines for agents (open beta) and code sources (closed beta), paid plans; design-system management preview with automated checks for missing information [S].
- MCP server [V Figma FAQ]: remote server at mcp.figma.com; `use_figma` (write to canvas through the Plugin API, building from published components and variables) and `generate_figma_design` are remote only; write to canvas is beta and free now, "will eventually become a usage-based paid feature"; Full seat needed to write outside drafts. Read limits: View and Collab seats 20 calls per month; Full and Dev seats none on Starter, 200 per day on Professional and Organization, 600 per day on Enterprise.
- ux-skill position: it already exports Figma variables and reads Figma variable exports. Figma's own "design feedback" agent is LLM-based and paid; ux-skill can be the deterministic checker an agent runs on code that came out of Figma (Code Connect, `@figma/code-connect` 2.1.0 MIT [V npm]).

#### B1.5 Design-token tooling and DTCG

- DTCG Format Module 2025.10, first stable version, 28 Oct 2025; Resolver Module 2025.10 final report (themes and modes) [V w3.org community reports and DTCG blog]. There is no "1.0" label: versions are calendar-based. No newer version as of Nov 2026; the only 2026 group news is a chair change on 17 Jun 2026 [V]. ux-skill already emits 2025.10.
- Style Dictionary 5.7.1 (2026-10-24, Apache-2.0) [V npm]; 2025.10 support added piecemeal (color 5.3, dimension object 5.4 or 5.5) [S]; Resolver Module support missing as of the source date [S, may be outdated].
- Terrazzo CLI 2.10.0 (2026-10-21, MIT), DTCG-native [V npm].
- Tokens Studio: Starter EUR 0, Team EUR 39 per month (annual), Organization EUR 499 per month (annual), Enterprise custom [V pricing page]; DTCG 2025.10 support claimed by a Zeroheight guide [S].
- ux-skill ahead: WCAG-gated generation from one brand color, Arabic type, motion and component contracts in tokens. Behind: Resolver Module output; ecosystem transforms.

### B2. Standards and law

**WCAG 2.2**
- Errata page lists editorial fixes dated 27 Jun 2025 and 28 Oct 2025 (including rewording the 1.4.13 preamble) [S, search summary of the W3C errata page].
- AGWG calls for consensus on WCAG 2 editorial errata in Jul and Aug 2026, outcome not found [S].
- Discussion (Dec 2025) on whether normative fixes would be 2.2.1 or 2.3, not decided [S].
- 2.2 adds six A and AA criteria over 2.1 that matter for checks: 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8 [V Deque list].

**WCAG 3.0**
- Latest Working Draft dated 10 Sep 2026; earlier draft 3 Mar 2026 [V w3.org/TR/wcag-3.0, W3C news].
- September 2026 model: a single conformance level of "core requirements" that "builds on WCAG 2.2 Level A and AA"; supplemental requirements, assertions and recommended practices beyond it; tags (Physical harm, Risk, Barrier, Friction) that regulators can use to include or exclude requirements; multiple reporting tiers; an alternative "scoring" approach described in the Explainer, with W3C asking for feedback on both [V WAI WCAG 3 intro page updated 25 Sep 2026; W3C blog 25 Sep 2026].
- Bronze, Silver and Gold belong to earlier drafts and commentary [S]; claims of a 3.5 Bronze threshold are unverified [U].
- "WCAG 3 is not expected to be a completed W3C standard for a few more years" [V].

**APCA**
- Not adopted. The WCAG 3 draft says "The contrast algorithm used in WCAG 3 is yet to be determined" with placeholders in the text contrast requirements [V]. APCA was the Visual Contrast subgroup candidate; apca-w3 algorithm version 0.0.98G-4g [S].
- Related: CSS `contrast-color()` is Baseline newly available since 2026-04-10 [V web-features]; it picks black or white. Which contrast algorithm UAs use is not something I verified [U]; the linter should compute the ratio itself.

**EN 301 549**
- V4.1.1 published 2 Sep 2026 by ETSI, CEN and CENELEC; moves the web baseline to WCAG 2.2 A and AA; first version to map EAA requirements in annexes; reworked user preferences and real-time communication clauses [V Deque, Irish NDA].
- Expected OJEU citation around 30 Nov 2026; until cited, V3.2.1 (WCAG 2.1) remains the presumption-of-conformity baseline [V as Deque's expectation; S for the V3.2.1 point].

**European Accessibility Act**
- Applies from 28 Jun 2025; services may keep using products already in use until 28 Jun 2030; microenterprises providing services are exempt [K, EUR-Lex text could not be loaded this session].
- Enforcement: national market surveillance authorities, mostly complaint-driven, compliance notices before fines, few public fines in year one [S Taylor Wessing summary, vendor blogs]. First court ruling under a national transposition, Tribunal judiciaire de Lille, 5 May 2026 [U, single source].

**EU AI Act Article 50**
- Applies from 2 Aug 2026; Article 50 was not delayed by the AI Omnibus, Regulation (EU) 2026/1744, in force 27 Jul 2026 [V Goodwin alert].
- Who: providers of systems that interact directly with people must inform users they are dealing with AI unless obvious (50(1)); providers of generative systems must mark synthetic audio, image, video and text in a machine-readable, detectable way (50(2)); deployers of emotion recognition or biometric categorisation must inform people (50(3)); deployers must disclose deepfakes and AI-generated text published to inform the public on matters of public interest, unless it had human review and someone holds editorial responsibility (50(4)) [V Goodwin, Jones Day].
- Transition: generative systems already on the market before 2 Aug 2026 have until 2 Dec 2026 for marking [V Goodwin]. Al Jazeera reported a postponement to 2 Dec 2027 [U, outlier].
- Commission guidelines on Article 50 adopted 20 Jul 2026 [V Goodwin]. Final Code of Practice on marking and labelling published 10 Jun 2026: providers need "at least two layers of machine-readable marking where necessary" plus detection; deployers label with "the publicly available EU icon or equivalent labels"; Commission found it adequate on 8 Jul 2026 [V Jones Day for content; S for the 8 Jul opinion].
- Penalties: up to EUR 15 million or 3 percent of worldwide turnover [V].
- Relevance to ux-skill: the engine calls no model, so its own output is not the output of a generative AI system (an internal reading, needs counsel). The opportunity is checking that pages built with AI features show the disclosures (A2).

**ADA Title II (US)**
- DOJ interim final rule (Apr 2026) moved deadlines by one year: 26 Apr 2027 for entities serving 50,000 or more; 26 Apr 2028 for smaller entities and special districts; technical standard unchanged at WCAG 2.1 AA; comments were due 22 Jun 2026 [V Duane Morris]. Rule dated 20 Apr 2026 [S]. A court challenge to the extension was mentioned [U]. HHS Section 504 web rule deadline 11 May 2026 [S].

**Apple HIG and Material 3 Expressive (web relevance)**
- Apple Liquid Glass (WWDC 2025): reserve glass for the navigation layer above content; it adapts to Reduce Transparency (frostier), Increase Contrast (borders) and Reduce Motion; custom elements need their own fallbacks [S, developer summaries of WWDC25 sessions]. WWDC 2026 transparency slider and HIG changes [U, secondary blogs only]. Web takeaway: glass-like surfaces need a legibility check and a reduced-transparency path; `prefers-reduced-transparency` is Chrome-only on the web [V].
- Safari 27 (Sep 2026) ships customizable select and transform-aware anchor positioning [S WebKit WWDC26 post via search; V web-features shows Safari 27 support].
- Material Web Components are in maintenance mode pending new maintainers, no future work planned; no Material 3 Expressive web components found [S, npm page and GitHub discussion 5642 via search]. Web takeaway: M3 Expressive is an Android and Compose system; ux-skill's Material brand spec should not promise Expressive web components.

**DTCG** see B1.5: Format 2025.10 stable, Resolver 2025.10 stable, no later version [V].

### B3. Web platform features 2024 to 2026 and Baseline status

Source: `web-features` npm 3.44.0, published 2026-10-22 [V], read directly from data.json. "Newly" means available in all core browsers since the low date; "widely" means 30 months after.

| Feature | web-features id | Baseline | Date(s) | Support note | Lint implication |
|---|---|---|---|---|---|
| Anchor positioning | anchor-positioning | No (umbrella) | core keys low 2026-01-13 | Core properties (anchor-name, position-anchor, anchor(), position-try) are interoperable in Chrome 125, Firefox 147, Safari 26 since 2026-01-13; the umbrella feature is held back by `position-visibility: anchor-valid / anchor-visible` (Safari 27 only). web.dev called it Baseline in Jan 2026 [S] | Suggest for tooltips and menus with a fallback; do not flag JS positioning as an error |
| Popover | popover | Newly | 2025-01-27 | all | Suggest over JS show/hide for menus, toasts, tooltips |
| popover="hint" | popover-hint | No | | Chrome 151, Firefox 153 | Future only |
| Invoker commands (commandfor, command) | invoker-commands | Newly | 2025-12-12 | Safari 26.2 completed it | Suggest over onclick that only opens a dialog or popover |
| Interest invokers (interestfor) | interest-invokers | No | | Chrome 142 only; MDN says not in a spec [S] | Do not suggest yet |
| Customizable select (appearance: base-select) | customizable-select | No | | Chrome 135, Safari 27; Firefox behind a flag [S] | Suggest as progressive enhancement over div dropdowns |
| View transitions (same document) | view-transitions | Newly | 2025-10-14 | Firefox 144 completed it | Suggest for theme switch and state changes, with reduced-motion guard |
| Cross-document view transitions | cross-document-view-transitions | No | | Chrome 126, Safari 18.2 | Enhancement only |
| :active-view-transition | active-view-transition | Newly | 2026-01-13 | | |
| Scroll-driven animations | scroll-driven-animations | No | | Chrome 115, Safari 26; no Firefox | Enhancement only; require reduced-motion handling |
| Container size queries | container-queries | Widely | 2023-02-14 / 2025-08-14 | | Suggest over viewport queries inside components |
| Container style queries | container-style-queries | Newly | 2026-05-19 | Firefox 151 completed it | Parser must handle |
| Scroll-state queries | container-scroll-state-queries | No | | Chrome 133 | |
| @scope | scope | Newly | 2026-03-24 | Safari 26.4 completed it | Parser must handle |
| OKLCH and OKLab | oklab | Widely | 2023-05-09 / 2025-11-09 | | Recommend for token ramps |
| color-mix() | color-mix | Widely | 2023-05-09 / 2025-11-09 | | Contrast engine must resolve |
| Relative color syntax | relative-color | Newly | 2024-09-16 | | Contrast engine must resolve |
| light-dark() | light-dark | Newly | 2024-05-13 | | Contrast engine must evaluate both branches |
| light-dark() for images | light-dark-image | Newly | 2026-09-14 | | |
| contrast-color() | contrast-color | Newly | 2026-04-10 | | Compute the ratio, do not trust blindly |
| text-wrap: balance | text-wrap-balance | Newly | 2024-05-13 | | Suggest on display headings |
| text-wrap: pretty | text-wrap-pretty | No | | Chrome 117, Safari 26 | Optional suggestion on prose |
| interpolate-size and calc-size() | interpolate-size, calc-size | No | | Chrome 129 only | Accept as enhancement in animation rules |
| field-sizing | field-sizing | Newly | 2026-06-16 | Firefox 152 completed it | Suggest over JS autosize |
| @starting-style | starting-style | Newly | 2024-08-06 | | Accept as a passing exit and entry pattern |
| transition-behavior: allow-discrete | transition-behavior | Newly | 2024-08-06 | | Accept |
| ::details-content | details-content | Newly | 2025-09-16 | | Accept for accordion animation |
| details name (exclusive accordion) | details-name | Newly | 2024-09-03 | | Suggest over JS exclusive accordions |
| dialog closedby | dialog-closedby | No | | Chrome 134, Firefox 141 | |
| Viewport unit variants (svh, lvh, dvh) | viewport-unit-variants | Widely | 2022-12-05 / 2025-06-05 | | Drop "vh fallback" advice |
| backdrop-filter | backdrop-filter | Newly | 2024-09-16 | | Drop "unsupported" claim |
| prefers-reduced-transparency | prefers-reduced-transparency | No | | Chrome 119 only | Optional |
| CSS nesting | nesting | Widely | 2023-12-11 / 2026-06-11 | | Parser must handle |
| :has() | has | Widely | 2023-12-19 / 2026-06-19 | | Accept in rules (hover-only-card-actions already uses it) |
| Subgrid | subgrid | Widely | 2023-09-15 / 2026-03-15 | | Suggest for card alignment |
| AVIF | avif | Widely | 2024-01-25 / 2026-07-25 | | Fix rule wording |
| hyphens | hyphens | Widely | 2023-09-18 / 2026-03-18 | | Fix justify rule wording |
| inert | inert | Widely | 2023-04-11 / 2025-10-11 | | |
| :dir() | dir-pseudo | Widely | 2023-12-07 / 2026-06-07 | | Useful for RTL rules |
| sibling-count() | sibling-count | Newly | 2026-08-18 | | Staggered motion without JS |
| text-box (trim) | text-box | No | | Chrome 133, Safari 18.2 | Optional for display type |
| accent-color | accent-color | No | | missing Chrome Android in data | |

Interop 2026 focus areas (announced 12 Feb 2026) include anchor positioning, container style queries, dialogs and popovers, scroll-driven animations, view transitions, attr(), contrast-color(), custom highlights, scroll snap, shape() and zoom; accessibility testing is an investigation area [V web.dev]. Expect scroll-driven animations and cross-document view transitions to move toward Baseline during 2027; re-check before promoting them past "enhancement".

### B4. What users complain about in AI-generated UIs (2026)

**Measured harm (accessibility)**
- WebAIM Million 2026: 95.9 percent of home pages had detected WCAG 2 failures (94.8 in 2025); 56.1 errors per page (51 in 2025); WebAIM links the rise to "automated or AI-assisted coding practices" and says it reverses years of slow improvement [V].
- AudioEye study, 30 Sep 2026: five AI tools (OpenAI, Anthropic, Google, xAI, Lovable) asked for WCAG 2.2 AA sites; about 55 issues per page; 91 percent medium or high severity; 13 of 15 sites had at least one task-blocking issue; 81 percent of surveyed developers trust AI code on accessibility [S, vendor study via press; vendor sells remediation].
- CHI EA 2026 paper (Calo, Gurita, De Russis), "Measuring the Semantic Accessibility Gap in LLM-Generated Web UIs": semantic failures automated checkers miss [S, headline numbers not read].

**Sameness and visual tells (vendors now document them)**
- Anthropic frontend-design, current calibration list [V]: (1) warm cream near #F4F1EA with high-contrast serif display and terracotta near #D97757; (2) near-black with one acid-green or vermilion accent; (3) broadsheet layout with hairline rules, zero radius, dense columns; (4) SaaS card kit with one radius everywhere, `rgba(0,0,0,.1)` shadows and gradient washes; (5) template chrome: tracked ALL-CAPS eyebrow above every heading, middle-dot meta strings, `WORD`-dash-fragment labels, tinted near-black, monospace small labels, an arrow appended to links and buttons. Also: one accented word in a headline, all-caps labels, unnecessary labels above content, 01/02/03 markers on non-sequences, "big number with small label and gradient accent" heroes, fade-and-slide-up on each section, hover transitions on every card.
- impeccable README [V]: "Inter for everything. Purple-to-blue gradients. Cards nested in cards, gray text on colored backgrounds, a rounded-square icon tile above every heading"; and the newer "tasteful default: cream page, thin serif, italic accent, pill buttons".
- hallmark README [V]: eyebrow above every heading, tracked-capital labels, one colored word in a headline, a page of empty frames or only photographs, hero that misses its screen, email sign-up at the end of every page, a form that says thanks without sending anything.
- Hacker News "Ask HN: How can you tell a site/app is vibe coded?" (small thread) [V]: black background with green and orange gradients; Inter; zero-offset dark glows on text; 1px borders with 40px shadow blur; emoji in headers as iconography; very rounded corners; navy and techy palettes; em dashes in copy; UI text describing the obvious.
- 925studios guide (Mar 2026) [S]: Inter, purple-to-blue gradients, stock people at laptops or 3D blobs, plastic AI illustrations, oversized vague heroes, uniform 16px radius cards, identical padding and card heights, hedging and superlative copy, inert hover states, buttons that snap, the same fade-in on every element.
- Fountain Institute "7 tells" [S]: neon palettes of five or more colors, dark aurora gradients, emoji as icons, purple gradients, nested cards, multicolored side tabs on every card, colored status dots on every element.
- shadcn changelog (Dec 2025) acknowledged "all apps started looking the same" and added style presets [S].
- Commentators: asking the model to avoid the look moves it to the next most probable look [S]. Implication for ux-skill: rules must catch the second and third defaults, not just the first.

**AI disclosure in UI**
- Red Hat's AI guidelines: sparkle icons only for content actually AI-generated and never without a disclosure; AWS Cloudscape uses sparkles as AI badges [S].

**What this means for checks**
- The most-cited functional harms are contrast, missing labels and names, and broken phone layouts; the most-cited aesthetic harm is sameness across a small set of defaults that has shifted in 2026 away from purple and toward cream, serif and terracotta, near-black and acid, and template chrome. 5.0 should score both, and keep them separate (hallmark's Floor versus Reflex split is a good model).

---

## Sources

Repo and packages
- ux-skill README and compare page: /home/user/ux-skill/README.md, /home/user/ux-skill/docs/compare.html
- PyPI uxskill: https://pypi.org/pypi/uxskill/json
- npm registry entries: https://registry.npmjs.org/uxskill, https://registry.npmjs.org/impeccable, https://registry.npmjs.org/axe-core, https://registry.npmjs.org/lighthouse, https://registry.npmjs.org/chrome-devtools-mcp, https://registry.npmjs.org/style-dictionary, https://registry.npmjs.org/@terrazzo/cli, https://registry.npmjs.org/@google/design.md, https://registry.npmjs.org/stylelint-plugin-use-baseline, https://registry.npmjs.org/eslint-plugin-baseline-js, https://registry.npmjs.org/@eslint/css, https://registry.npmjs.org/eslint-plugin-jsx-a11y, https://registry.npmjs.org/accessibility-checker, https://registry.npmjs.org/pa11y, https://registry.npmjs.org/@storybook/addon-a11y, https://registry.npmjs.org/@projectwallace/css-analyzer, https://registry.npmjs.org/@lapidist/design-lint, https://registry.npmjs.org/@figma/code-connect, https://registry.npmjs.org/@playwright/mcp, https://registry.npmjs.org/uipro-cli
- web-features 3.44.0: https://registry.npmjs.org/web-features/-/web-features-3.44.0.tgz ; explorer: https://web-platform-dx.github.io/web-features-explorer/
- Star counts: https://img.shields.io/github/stars/{owner}/{repo}.json (queried 2026-11-02)

Competitors and neighbours
- Anthropic frontend-design: https://github.com/anthropics/skills/tree/main/skills/frontend-design
- impeccable: https://github.com/pbakaus/impeccable ; https://impeccable.style/docs/detector
- taste-skill: https://github.com/Leonxlnx/taste-skill
- hallmark: https://github.com/Nutlope/hallmark
- ui-ux-pro-max: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- open-design: https://github.com/nexu-io/open-design
- Vercel agent skills: https://github.com/vercel-labs/agent-skills
- Google DESIGN.md: https://github.com/google-labs-code/design.md
- Google Stitch pricing (secondary): https://www.banani.co/blog/google-stitch-pricing-and-credits
- v0 pricing: https://v0.app/pricing ; design systems: https://v0.app/docs/design-systems
- Lovable security: https://docs.lovable.dev/features/security ; https://lovable.dev/blog/how-lovable-protects-your-apps-automatically ; pricing: https://lovable.dev/pricing
- Bolt review (secondary): https://uxmagic.ai/blog/bolt-new-review-2026-ai-app-builder-limits
- Claude Design: https://www.anthropic.com/news/claude-design-anthropic-labs ; https://the-decoder.com/anthropics-claude-design-turns-chatbot-conversations-into-prototypes-slide-decks-and-marketing-assets/
- Figma Config 2026: https://forum.figma.com/product-updates-3/everything-announced-at-config-2026-55221
- Figma MCP FAQ: https://help.figma.com/hc/en-us/articles/39252411778583-Figma-MCP-server-FAQs ; guide: https://help.figma.com/hc/articles/32132100833559-Guide-to-the-Figma-MCP-server
- Figma library guidelines (secondary): https://www.techradar.com/pro/figma-is-making-its-ai-agents-smarter-and-more-connected-to-help-boost-your-designs
- axe-core 4.11 notes: https://docs.deque.com/axe-release-impact/4.11.0/en/release-notes ; https://rocketvalidator.com/blog/accessibility-checker-upgraded-to-axe-core-4.11.1
- Lighthouse 13: https://developer.chrome.com/blog/lighthouse-13-0
- DTCG: https://www.w3.org/community/design-tokens/ ; https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/ ; https://www.w3.org/community/reports/design-tokens/CG-FINAL-resolver-20251028/
- Style Dictionary and Resolver support (secondary): https://project.pages.drupalcode.org/design_system_api/prior-art/tokens/ ; Zeroheight: https://help.zeroheight.com/hc/en-us/articles/48049028236187
- Terrazzo: https://terrazzo.app/docs/guides/dtcg/
- Tokens Studio pricing: https://tokens.studio/pricing

Standards and law
- WCAG 3 draft: https://www.w3.org/TR/wcag-3.0/ ; March draft: https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/ ; intro: https://www.w3.org/WAI/WCAG3 ; blog: https://www.w3.org/blog/2026/crafting-wcag-3-for-more-accessible-user-experiences/ ; explainer: https://w3c.github.io/wcag3/explainer/
- WCAG 2.2 errata: https://www.w3.org/WAI/WCAG22/errata/ ; 2024 update: https://www.w3.org/WAI/news/2024-12-12/wcag2updates/ ; AGWG list: https://lists.w3.org/Archives/Public/w3c-wai-gl/2026JulSep/author.html ; WCAG2ICT minutes: https://www.w3.org/2025/12/04-wcag2ict-minutes.html
- APCA: https://github.com/Myndex/apca-w3
- EN 301 549 V4.1.1: https://www.deque.com/blog/en-301-549-v4-1-1-is-final-what-changed-what-it-means-and-what-you-should-do/ ; https://nda.ie/news/en301549-published ; https://www.dwt.com/insights/2026/09/european-accessibility-act-ict-standards-update
- EAA: https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en ; https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng ; enforcement (secondary): https://www.taylorwessing.com/en/insights-and-events/insights/2026/03/the-eaa-takes-shape ; https://www.levelaccess.com/blog/eaa-compliance-in-2026-how-enforcement-has-evolved-and-what-to-expect-next/ ; Lille ruling (unverified): https://www.pinmeto.com/news/eu-accessibility-act-enforcement-french-courts-2026/
- AI Act Article 50: https://www.goodwinlaw.com/en/insights/publications/2026/08/alerts-technology-dpc-eu-ai-act-transparency-obligations-now-in-force ; https://www.ropesgray.com/en/insights/viewpoints/2026/08/102nfqm/you-talkin-to-me-operationalising-the-eu-ai-acts-transparency-obligations ; https://www.bakerbotts.com/thought-leadership/publications/2026/september/eu-ai-act-article-50-transparency-obligations-go-live ; Code of Practice: https://www.jonesday.com/en/insights/2026/06/european-commission-publishes-final-code-of-practice-on-marking-and-labelling-aigenerated-content ; https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content ; outlier: https://www.aljazeera.com/economy/2026/8/6/what-came-into-force-with-the-eus-ai-act-this-week-and-what-didnt
- ADA Title II: https://www.duanemorris.com/alerts/doj_extends_ada_title_ii_digital_accessibility_deadlines_one_year_0426.html ; https://plantemoran.com/explore-our-thinking/insight/2026/04/doj-extends-ada-title-ii-web-accessibility-compliance-deadlines ; https://natlawreview.com/article/doj-extends-public-entities-compliance-deadline-ada-related-website-accessibility
- Apple Liquid Glass (secondary): https://developer.apple.com/forums/thread/791070 ; https://mobilesyrup.com/2025/06/10/how-apple-is-making-sure-liquid-glass-as-legible-as-possible/
- Safari 27 and WebKit WWDC26: https://webkit.org/blog/17967/news-from-wwdc26-webkit-in-saf ; https://developer.apple.com/documentation/safari-release-notes/safari-27-release-notes ; https://web.dev/blog/web-platform-09-2026
- Material Web maintenance mode: https://github.com/material-components/material-web/discussions/5642 ; https://npmjs.com/package/@material/web

Web platform
- Interop 2026: https://web.dev/blog/interop-2026 ; https://webkit.org/?p=17818
- New to the web platform, January 2026: https://web.dev/blog/web-platform-01-2026
- MDN anchor(): https://developer.mozilla.org/docs/Web/CSS/anchor ; interestForElement: https://developer.mozilla.org/docs/Web/API/HTMLButtonElement/interestForElement

User complaints
- WebAIM Million 2026: https://webaim.org/projects/million/
- AudioEye study (press): https://www.marketscreener.com/news/audioeye-study-finds-ai-coding-tools-do-not-write-accessible-code-ce785ad2d18bf520
- CHI EA 2026 paper: https://iris.polito.it/retrieve/handle/11583/3008330/983056
- Hacker News thread: https://news.ycombinator.com/item?id=49290499
- 925studios: https://www.925studios.co/blog/ai-slop-web-design-guide
- Fountain Institute: https://pages.thefountaininstitute.com/posts/7-tells-that-a-ui-is-ai-generated
- Vibe-coded sameness: https://codemyspec.com/blog/vibe-coded-websites-look-the-same ; https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website
- shadcn changelog: https://ui.shadcn.com/docs/changelog/2025-12-shadcn-create
- Red Hat AI iconography: https://ux.redhat.com/ai-guidelines/iconography/ ; Cloudscape: https://cloudscape.design/gen-ai/foundation/iconography/
