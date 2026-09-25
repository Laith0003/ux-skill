---
description: Build a page, a component (--component), a dashboard (--dashboard), or a design from a reference image (--from-image) from a brief, with anti-AI-slop discipline. The brief picks the mode when no flag is given.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Bash(python3:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-design

You are running the `/ux-design` command from the `ux` plugin. The job is to generate a beautiful, high-end design or component from a brief — and explicitly NOT produce AI-slop output.

## When to use

Triggers: "design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "I need a hero section", "design a modal", "build a button", "design the admin panel", "build it like this screenshot", any free-form request for a visual/UI deliverable.

## Modes

`/ux-design` builds four kinds of output. It absorbs what used to be `/ux-component`, `/ux-dashboard` and `/ux-image-to-code`; those names still work as aliases until 4.1.

| Mode | Flag | Picked from the brief when | State file |
|---|---|---|---|
| page (default) | none | A page, a landing, a multi-section surface, a marketing page with stats | `.ux/last-design.json` |
| component | `--component [name]` | The brief names ONE element: button, modal, navbar, sidebar, card, table, form, chart. Not a full page | `.ux/last-component.json` |
| dashboard | `--dashboard` | Dashboard, admin panel, metrics page, operator console, analytics view, KPI board, monitoring screen | `.ux/last-dashboard.json` |
| image | `--from-image <path>` | The brief attaches a design image (PNG, JPG, WebP) or names one | `.ux/last-image-extract.json`, then the state file of the build mode |

A flag always wins over the words. Image mode stacks with the others: `--from-image ref.png --dashboard` reads the image, then builds a dashboard. Say which mode you picked in the first line of the output so the user can stop you.

Every mode runs the same Process below (discovery, references, dials, dispatch, output, state) and the same v2 steps (brief, brand, recommendation, sequence, generation, lint and responsive and brand gates). The mode sections list only what changes.

| Flag | Meaning |
|---|---|
| `--component [name]` | Component mode |
| `--dashboard` | Dashboard mode |
| `--from-image <path>` | Image mode: read the image first |
| `--extract-only` | Image mode: stop after the extraction and print its JSON. No build |
| `--no-recommendation` | Image mode: hints only, no recommender run. Implies `--extract-only` |
| `--save <path>` | Image mode: where to write the extraction (default `.ux/last-image-extract.json`; empty string skips the write) |
| `--skip-discovery` | Skip the discovery intake (see step 1) |

### Component mode (`--component`)

The job is a single, production-grade component that avoids generic AI aesthetics. One component, fully realized: all four interaction states, accessible, on-brand. If the brief asks for a full page or multi-section surface, switch to page mode.

Triggers: "build a button", "create a pricing card", "make a modal", "add a navbar", "design a sidebar", "I need a data table", "build a form", "make a chart component", or any single-element request.

**Discovery (step 1).** Focus on: brand identity, 2-3 references for the component type, audience, style direction, voice, stack, imagery (if applicable), must-have patterns, avoid list, and the wow moment for THIS component specifically. Group into one or two messages. Skip only on `--skip-discovery` or if the spec already covers every field. Without the wow moment, push back.

**Capture the spec.** Required:
- **Component type**: button / modal / navbar / sidebar / card / table / form / chart / other
- **Stack**: React + Tailwind / Vue / Svelte / Blade + Alpine / vanilla HTML / etc.
- **Brand voice**: pull from `.ux/last-frame.json` if it exists, otherwise ask one line: *"What's the voice: minimal / brutalist / editorial / playful / dark? Or 'your call'?"*

Optional but useful: specific behavior (auto-sort, multi-step, infinite scroll, drag-reorder), data shape, density target. Do not ask three questions. One question that surfaces everything missing.

**Arsenal picks (step 2).** Pick 1-2 patterns that fit. For a button: live status with overshoot, optimistic update. For a modal: contextual focus mode. For a navbar: command input, intelligent list. For a card: hairline-separated metric blocks. For a table: intelligent list, monospace tabular. For a form: inline validation with field-level @error, multi-step wizard. For a chart: monochrome + semantic state colors only.

**Dials (step 3).** DESIGN_VARIANCE 5 (4 for system components, 6 for marketing components). MOTION_INTENSITY 4 (3 for utility components, 5 for marketing components). VISUAL_DENSITY 5 (7 for tables/charts, 4 for buttons/modals).

**Dispatch (step 4).** `frontend-engineer` gets the spec verbatim, the dials, the 1-2 patterns, the full `references/styles/anti-slop.md`, the target stack, and an instruction to return code + self-review on bans avoided + patterns used. Dispatch `motion-engineer` in parallel if the spec involves motion (loading states, optimistic UI, micro-interactions, transitions). Dispatch `copy-writer` in parallel if the component has non-trivial copy (form labels, empty states, error messages, CTAs).

**Generation (v2 step 4).** Look up the requested component name in `.ux/last-recommendation.json`'s `components` list. If present, generate using its `anatomy`, `states`, `tokens_used`, and `motion` fields as the spec. If not present, search `data/components.json` directly via `cat data/components.json | jq '.entries[] | select(.name | test("<name>"; "i"))'`. The page-sequence step (v2 step 2.5) does not apply. The brand anchor applies as in page mode: the component must use the brand primary color, the logo where one belongs, and logo-style type, and ship real imagery when it carries visuals, or it fails the brand-fidelity floor. A house-style component for a client brand is wrong no matter how clean.

**Output (step 5).**

```
─── component spec ───
Type:       <component type>
Stack:      <stack>
Voice:      <brand voice>
Dials:      DESIGN_VARIANCE=<n>, MOTION_INTENSITY=<n>, VISUAL_DENSITY=<n>
Patterns:   <1-2 arsenal patterns>

─── generated ───
<code from sub-agent, verbatim>

─── interaction states ───
Default:    <description>
Hover:      <description>
Active:     <description>
Disabled:   <description>
Loading:    <description>  (if applicable)
Error:      <description>  (if applicable)
Empty:      <description>  (if applicable)

─── self-review ───
Bans avoided:    <list>
Patterns used:   <list>

─── next ───
Recommended: /ux-design --component   (build the next one)
Other moves: /ux-polish      (cosmetic pass)
             /ux-a11y        (WCAG check)
             /ux-design      (assemble into a fuller surface)
             /ux-next        (let me decide)
```

**State (step 6).** Write `.ux/last-component.json`:

```json
{
  "command": "ux-component",
  "timestamp": "<ISO8601>",
  "type": "<component type>",
  "stack": "<stack>",
  "voice": "<voice>",
  "dials": { "variance": <n>, "motion": <n>, "density": <n> },
  "patterns": ["<arsenal patterns>"],
  "output_file": "<path if saved>"
}
```

The `command` value stays `ux-component` so `/ux-next` keeps reading it.

**Component hard rules** (in addition to the shared hard rules):
- All four interaction states (default / hover / active / disabled). Non-negotiable. Buttons/inputs that look identical when hovered, active, or disabled = failure.
- Loading + error + empty states wherever the component can hit them.
- Mandatory imagery if visual (avatars, product shots, illustrations): real and on-brand, client assets first, then curated Unsplash/Pexels chosen to match the brand + temperature.
- Inter is allowed. Do not ban it.
- No 3-equal-cards layouts for grouped components.

**Component failure modes and errors:**

| Failure or error | Recovery |
|---|---|
| Stack unclear | Ask one combined question covering stack + voice + behavior |
| Component type ambiguous ("thing to filter stuff") | List the candidate types (table with command input / sidebar with filter chips / autocomplete combobox) and ask which one |
| Sub-agent returns the default state only | Reject and redo; all four interaction states are non-negotiable |
| Sub-agent returns the wrong stack | Catch in review, redo |
| Sub-agent says "I avoided X" but the code uses X | Grep the output. Reject and redo |
| Over-scope: a full page for a single button, or a spec that implies a full page | Trim to the requested component; offer page mode as the follow-up |
| No motion when motion was specified | Re-dispatch with an explicit motion brief |
| `.ux/last-frame.json` absent and voice not provided | Ask the one-line voice question above |

### Dashboard mode (`--dashboard`)

The job is a dashboard that respects data density and operator attention, not a marketing site with charts pasted on. Anti-card-overuse, monospace tabular numbers, semantic state colors, sparing motion. A marketing landing page with stats stays in page mode.

Triggers: "build a dashboard", "design the admin panel", "make a metrics page", "operator console", "analytics view", "KPI board", "monitoring screen".

**Discovery (step 1).** Highest-leverage fields: brand identity, references (admired dashboards), audience (operator / analyst / exec: different density needs), key metrics + data shape, style direction, voice for state messages, stack, must-have widgets (intelligent-list / command-input / live-status / wide-stream / contextual-focus), avoid list, and the wow moment. Group into 2-3 messages. Push back on "anything's fine".

**Capture the brief.** Required:
- **Data shape**: what entities, what metrics, what relationships. Time-series? Categorical? Hierarchical?
- **Key metrics**: the 3-7 numbers that dominate the page
- **Audience**: operator (always-on, scan-and-act) / analyst (deep dive, filter and segment) / exec (status at a glance)
- **Stack**: React + Tailwind / Next.js / Vue / Blade + Alpine / etc.

If anything's missing, ask once: *"One line: data shape, key metrics, audience (operator/analyst/exec), stack?"*

**Arsenal picks (step 2).** Pick 3-5 dashboard patterns:
- **Bento grid**: asymmetric, intentional, never 3-equal-cards
- **Intelligent list**: auto-sorting, contextual ordering
- **Command input**: keyboard-driven filter/search
- **Live status with overshoot**: for real-time indicators, used sparingly
- **Wide data stream**: infinite carousel of metrics when there's more than fits
- **Contextual focus mode**: click a metric, get the deep-dive without page change
- **Hairline-separated metric blocks**: for tight KPI rows, no cards needed

**Dials (step 3).** DESIGN_VARIANCE 4 (dashboards are calmer than landings). MOTION_INTENSITY 3 (data should feel still until it changes). VISUAL_DENSITY 8 (dashboards are cockpits, not galleries).

**Dispatch (step 4).** `frontend-engineer` gets the brief verbatim, data shape + key metrics + audience, stack, dials, the 3-5 patterns, the full `references/styles/anti-slop.md`, and an explicit instruction: monospace tabular numbers, no purple gradients, max 2 live indicators per viewport, semantic state colors only. Dispatch `motion-engineer` in parallel for live indicators and state transitions. Dispatch `copy-writer` in parallel for empty states, error messages, and metric labels.

**Generation (v2 step 4).** Filter `components` from the recommendation for dashboard patterns (`category: Data Display`, `Charts & Viz`). Build a dashboard grid using the picked palette in dark mode (force `mode=dark` if not already set in the recommendation). Give `frontend-engineer` the `chart-types.json` picks scoped to the data the user described. With a client brand, dark mode still holds, but the brand primary (not the house pick) is the accent on every state color, the logo sits in the chrome, and type matches the logo style; the dashboard must clear the brand-fidelity floor.

**Output (step 5).**

```
─── dashboard brief ───
Data shape:  <summary>
Metrics:     <3-7 key metrics>
Audience:    <operator | analyst | exec>
Stack:       <stack>
Dials:       DESIGN_VARIANCE=<n>, MOTION_INTENSITY=<n>, VISUAL_DENSITY=<n>
Patterns:    <3-5 arsenal patterns>

─── generated ───
<code from sub-agent, verbatim>

─── layout logic ───
Grouping:    <how widgets are grouped: border-t / divide-y / negative space>
KPI row:     <pattern used: hairline-separated / asymmetric bento / focus widget>
Live count:  <number of breathing/live indicators in initial viewport, must be ≤2>

─── self-review ───
Bans avoided:    <list>
Patterns used:   <list>
Accessibility:   <color-not-only confirmed for all chart series>

─── next ───
Recommended: /ux-design --component   (build a missing widget)
Other moves: /ux-polish      (cosmetic pass)
             /ux-a11y        (color-not-only audit for charts, contrast for tabular data)
             /ux-motion      (verify live indicators don't fight attention)
             /ux-next        (let me decide)
```

**State (step 6).** Write `.ux/last-dashboard.json`:

```json
{
  "command": "ux-dashboard",
  "timestamp": "<ISO8601>",
  "data_shape": "<summary>",
  "metrics": ["<key metrics>"],
  "audience": "<operator|analyst|exec>",
  "stack": "<stack>",
  "dials": { "variance": <n>, "motion": <n>, "density": <n> },
  "patterns": ["<arsenal patterns>"],
  "live_indicator_count": <n>,
  "output_file": "<path if saved>"
}
```

**Dashboard hard rules** (in addition to the shared hard rules):
- Numbers use `font-mono` with tabular figures (`font-variant-numeric: tabular-nums`). Non-negotiable.
- NEVER 3-equal-cards for KPIs. Use asymmetric bento or hairline-separated metric blocks.
- Maximum 2 "breathing" / live-pulse indicators per viewport. More = noise.
- Default monochrome. Semantic state colors only (success / warning / danger / info).
- Charts: every series has a non-color indicator (pattern, shape, label). Never color alone.
- Empty, loading and error states for every widget.
- Group via negative space, hairlines (`border-t`), or `divide-y`. Don't card-wrap everything.

**Dashboard failure modes and errors:**

| Failure or error | Recovery |
|---|---|
| Card overuse: every widget in `rounded-lg shadow border` | Reject. Use hairlines and grouping |
| 3-equal-card KPI row | Reject, replace with asymmetric bento or hairline-separated blocks |
| 3 or more live indicators in the initial viewport | Reject, reduce to 2 or fewer |
| Proportional digits in metrics (numbers jitter on update) | Reject, force `tabular-nums` |
| Color-only chart series | Reject, add patterns/shapes/labels |
| Marketing gradient on the analytics page | Reject, swap to neutral + semantic accent |
| No empty/loading/error states | Reject and redo |
| Data shape missing | Ask for entities + relationships + metrics in one combined question |
| Audience unclear, or "all of them" | Ask once; density and motion defaults depend on a single primary audience, so push back until one is picked |
| More than 7 key metrics | Force a triage to the 3-7 that dominate; surface the rest as secondary |

### Image mode (`--from-image <path>`)

**Pure CV. No multimodal LLM.** Hand the engine a screenshot or a design reference; it returns a Brief, a closest-match palette, a closest-match style, and a full Recommendation. No vision model is called. Every signal is computed deterministically from pixels via Pillow.

Use it when you have a reference design (a competitor screenshot, a gallery shot, a Figma export) and want the build to go in that direction, when you want the recommendation anchored on a real image instead of a typed brief, or when you want to check the engine's read on a design before generating code. Skip it when the reference is text (a written brief, a PRD: use `/ux-discover`), or when you want pixel-perfect cloning: this is a HINT generator, not a copy-paste tool.

**1. Extract.**

```bash
python3 -m engine.cli.main image-extract path/to/reference.png [--no-recommendation] [--save .ux/last-image-extract.json]
```

What happens, step by step:

1. **Decode + downsample**: Pillow opens the image and resizes the long edge to 512px to keep quantization fast.
2. **Quantize to 5 colors**: `Image.quantize(colors=5, method=MAXCOVERAGE)` finds the dominant tones (a deterministic palette reduction, equivalent in shape to a small k-means but without sklearn).
3. **Canvas polarity**: average luminance under the sRGB curve. Above 0.5 is light; below is dark.
4. **Type polarity**: ratio of `EDGE_ENHANCE_MORE` variance to `EMBOSS` variance. High ratio leans serif, low leans sans, between is `unknown`.
5. **Aspect + density**: `FIND_EDGES` followed by binarization gives a coarse "edge fraction." Lots of edges means a dense layout (dashboard, dense editorial); few edges means an airy hero.
6. **Match against manifests**: for each palette in `data/palettes.json`, sum the nearest-neighbour distances between the extracted 5 colors and the palette's canvas/surface/ink/primary anchors. Lowest sum wins.
7. **Style fit**: bias styles whose id/category contains "dark"/"cinema"/"luxe" for dark canvas, "swiss"/"editorial"/"minimal" for light canvas. Boost styles that appear in the matched palette's `compatible_styles`.
8. **Synthetic Brief, then recommend**: pack the hints into a `Brief` and run the recommender to produce a complete system.

The result is JSON with `image`, `brief`, `hints` (`dominant_colors`, `canvas_polarity`, `type_polarity`, `aspect`, `matched_palette_id`, `matched_palette_name`, `matched_style_id`, `matched_style_name`), `recommendation`, and `saved_to`. The same pipeline is the MCP tool `ux_image_extract` (`{"path": "/abs/path/to/reference.png", "with_recommendation": true}`), and in Python:

```python
from engine.image_extract import image_to_brief
from engine.recommender import Brief, recommend

result = image_to_brief("reference.png")
rec = recommend(Brief(**result["brief"]))
```

**2. Report the read.** Tell the user in one short block what the engine sees: canvas polarity, type polarity, dominant colors, matched palette and matched style. With `--extract-only` or `--no-recommendation`, print the JSON and stop.

**3. Build.** Otherwise continue into the build mode (page by default, or `--component` / `--dashboard`). Use the extraction's `recommendation` in place of the v2 step 2 `recommend` call, and its `brief` to fill discovery fields the user has not answered. For more control, edit the saved file and rerun the recommender on it: `python3 -m engine.cli.main recommend --brief-file .ux/last-image-extract.json`.

**Brand anchor.** The uploaded image IS the brand source. When the build should match the source's identity rather than the house style, extract the brand from it first (v2 step 1.5: capture the logo color/type from the image into `.ux/brand-signals.json`, then `uxskill brand --signals-file .ux/brand-signals.json --out .ux`) so the build inherits the source's primary color, logo, and logo-style type. The CV `hints` are color and polarity only; the travelling brand carries the logo and type intent the recommender enforces.

**Default forbidden list.** The synthetic brief auto-populates `forbidden` with the project-wide taste guardrails: `yellow`, `amber`, `gold`, `cream`, `coral`, `cormorant`. The extraction is for COLOR and POLARITY hints; the forbidden vocabulary is a separate policy decision the engine respects regardless of what the image suggests. To override it, edit `.ux/last-image-extract.json`, remove items from `brief.forbidden`, and rerun the recommender on that file.

**Limitations (say these when they matter):**
- **Type polarity is a guess.** It samples edge-filter variance ratios; that correlates with serif vs sans-serif but is not OCR.
- **The matched palette is the closest in our manifest, not the closest globally.** If the reference uses colors no palette covers, the match picks the least-bad neighbour.
- **No layout reconstruction.** The engine reads color, light and edge density. It does NOT read grid structure, component boundaries, or copy. Layout comes from the brief and the page sequence, not the image.
- **No multimodal LLM is consulted.** That is the point: it stays cheap, deterministic, and offline.

## Process

### 1. Run the discovery protocol (MANDATORY)

**Never improvise.** Before doing anything else, read `references/process/discovery-protocol.md` and run its 10-field intake on the user. The output of every generation command is downstream of the inputs — improvisation is the single biggest source of mediocre, generic results.

The 10 required fields are:
1. **Brand identity** — pasted brand brief, design tokens, logo files, or "no brand"
2. **Reference inspirations** — 3–5 URLs/screenshots of designs the user LIKES (for aesthetic, not features)
3. **Product type & audience** — one sentence
4. **Style direction** — minimalist / industrial / high-end-visual / editorial / dev-tool-dark / playful / your-call
5. **Voice** — direct, warm, brief / technical / friendly / editorial / playful / from brand
6. **Stack** — React+Tailwind / Next.js / Vue / Blade+Alpine / vanilla / Astro / "what we have"
7. **Imagery sources** — real screenshots / brand photos / placeholders / described generations
8. **Must-have patterns** — terminal mock / bento / interactive demo / specific arsenal pattern / freely pick
9. **Avoid list** — user's personal taste hard-rules beyond standard anti-slop
10. **The wow moment** — the ONE thing this design must do that lifts it above generic

**Delivery rules**:
- Group into 2–3 messages of 3–4 questions each. NEVER all 10 at once.
- First message: brand + references + audience (highest-leverage).
- Second message: style + voice + stack.
- Third message: imagery + must-haves + avoid + wow.
- Wait for each batch's answer before sending the next.

**Skip conditions** (the only ones):
- User passes `--skip-discovery` flag.
- User's first message already covers ALL 10 fields. Verify it does; if anything's missing, ask only for the missing fields.
- User is iterating on a prior design (read `.ux/last-frame.json`; ask only what's changed).

**After collecting answers**: write `.ux/last-frame.json` with the full discovery payload. Echo a 2-sentence summary back to the user before generating — let them stop you if their intent didn't land.

NEVER proceed to step 2 without the wow moment field populated. If the user says "anything's fine", push back: "Give me one concrete moment, even tiny — something a visitor would remember."

### 1b. DESIGN.md is the visual contract

If a `DESIGN.md` exists in the project root, read it FIRST and treat it as the source of truth for the visual system (colors, typography, spacing, rounded, components). Match it exactly. If none exists, after discovery emit one for this project with `ux design-md` (the Google Stitch / awesome-design-md standard) and treat it as the contract the generated UI must satisfy.

### 2. Read the references

Before writing a single line of code, read:
- `references/styles/anti-slop.md` — the ban list. Internalize every forbidden pattern.
- `references/styles/arsenal.md` — the high-end pattern library. Pick 2-4 patterns that fit the brief.
- `references/foundations/wow.md` — derive the **WOW LAYER**: 2-3 coordinated signature moments (one hero moment + a motion signature + an optional section moment) from the brand temperature + industry + goal. The page must do something a visitor remembers, not just be clean — derived + varied to THIS brand, never a stamped recipe.
- `references/foundations/responsive.md` + `references/foundations/component-behaviors.md` — mobile-first mechanics + per-component responsive contracts. The build is verified at 360px (no horizontal scroll, no wrapping nav/wordmark/label, sticky chrome <= ~96px).

These are non-negotiable. The output's distinction from generic AI output IS the value of this command.

### 3. Set the dials

Pick values for three dials based on the brief (these are inherited from `design-taste-frontend`):

- **DESIGN_VARIANCE** (1 perfect symmetry → 10 artsy chaos) — default 7 for landing pages, 4 for dashboards, 5 for components
- **MOTION_INTENSITY** (1 static → 10 cinematic) — default 6 for landing pages, 3 for dashboards, 4 for components
- **VISUAL_DENSITY** (1 art gallery → 10 cockpit) — default 4 for landing pages, 8 for dashboards, 5 for components

Override with whatever the user explicitly asked for. Surface your dial values in the output so the user sees what you picked.

### 4. Dispatch the frontend-engineer sub-agent

Call the Task tool with `subagent_type: "frontend-engineer"`. Pass the agent:

- The brief (verbatim from the user)
- Your dial values
- The 2-4 arsenal patterns you picked
- **The page-level section sequence** selected for the brief's goal (see the v2 Python integration step below). Instruct the sub-agent to expand the ENTIRE ordered sequence, map all source content into it (every sector -> a pill, every size -> a card, every benefit -> a checklist item — do not trim), give every card/pill/stat a relevant inline SVG icon, and ship the goal's conversion mechanisms.
- The full content of `references/styles/anti-slop.md` (paste into the prompt — do not assume the sub-agent has read it)
- The target stack
- An instruction to return:
  1. The generated code
  2. A self-review noting which anti-slop bans they had to consciously avoid
  3. Which arsenal patterns they used

Do not write the design yourself. The sub-agent's job is implementation; your job is orchestration.

### 5. Format the output

Use this exact template:

```
─── design brief ───
Product:   <one-line summary>
Stack:     <stack>
Dials:     DESIGN_VARIANCE=<n>, MOTION_INTENSITY=<n>, VISUAL_DENSITY=<n>
Patterns:  <2-4 arsenal patterns chosen>

─── generated ───
<code blocks from the sub-agent — preserve verbatim>

─── self-review (sub-agent) ───
<sub-agent's notes on which anti-slop bans they avoided>
<which arsenal patterns they used and why>

─── next ───
Recommended: /ux-polish      (cosmetic pass on the generated design)
Other moves: /ux-motion      (verify the motion holds up)
             /ux-a11y        (WCAG check on the generated design)
             /ux-case-study  (publish this as a case study)
             /ux-next        (let me decide)
```

### 6. Persist state

Write to `.ux/last-design.json` in the project root:

```json
{
  "command": "ux-design",
  "timestamp": "<ISO8601>",
  "brief": "<verbatim brief>",
  "stack": "<stack>",
  "dials": { "variance": <n>, "motion": <n>, "density": <n> },
  "patterns": ["<arsenal pattern names>"],
  "output_file": "<path if saved to disk>"
}
```

This lets `/ux-next` and downstream commands pick up where you left off.

## SEO is mandatory for public-web outputs

For any landing page or public-facing surface, read `references/foundations/seo.md` and require the frontend-engineer to ship the full SEO foundation (head surface, OG + Twitter, JSON-LD, semantic HTML, image discipline, CWV targets). Surface this requirement in your dispatch prompt. The output is incomplete without it. Derive sensible real values from the brief + source when the brief doesn't supply them (canonical/og:url from the source URL, og:image from a real CDN image the page references). **Never let the frontend-engineer ship a literal `{TODO_FILL...}` token inside the rendered markup** — the linter flags it HIGH and it is a draft-state leak. Where a value is genuinely absent (no phone, no OG image), OMIT that element gracefully (drop the `<meta>` / the affordance); surface any "you should patch this" note to the user OUTSIDE the code, never as a placeholder in the HTML.

## Hard rules (non-negotiable)

- NEVER use purple/blue AI gradients. Single high-contrast accent, saturation < 80%.
- NEVER use generic names ("John Doe", "Acme", "Nexus") in placeholder content.
- NEVER use pure black (`#000`). Use Zinc-950, Charcoal, or Off-Black.
- Imagery is mandatory and REAL: client assets first, then curated Unsplash/Pexels chosen to match the brand + 7-axis temperature (`engine.brand.image_search_terms` suggests on-brand search terms). Pick the best per slot; treat them so they read as deliberate. An abstract SVG is NOT a substitute for a real product/site image. Ban only random/generic stock and auto-rotating placeholder services.
- NEVER ship a text-only wall — always include intentional, real imagery.
- NEVER use emoji as icons. Prioritize **Google Material Symbols** (load via Google Fonts: `Material+Symbols+Outlined` / `Rounded` / `Sharp`, styled with `font-variation-settings`). Phosphor / Radix / Lucide are acceptable secondary choices when an icon doesn't exist in Material Symbols.
- NEVER ship 3-equal-cards layouts. Use 2-col zig-zag, asymmetric, or horizontal scroll.
- NEVER ship horizontal scroll on mobile. Every layout works at 360–390px with `scrollWidth <= innerWidth`; every multi-column block collapses to one column at ≤640px. This is verified in Step 5, not assumed.
- NEVER ship a literal placeholder token (`{TODO_FILL...}`, `{{ var }}`, "lorem ipsum") in the rendered markup. Fill known values; OMIT genuinely-absent elements; never print the token.
- NEVER repeat one icon across differentiated items (every skip size with the same box icon). Distinct icon per item, or none + typographic differentiation.
- NEVER animate `width`/`height`/`top`/`left`. Use `transform` and `opacity` only.
- NEVER skip empty/loading/error states.
- NEVER use serif fonts on dashboards.
- NEVER produce centered hero sections when `DESIGN_VARIANCE > 4` — force asymmetry.
- NEVER use scroll progress paths / scroll-tied SVG line drawing on the side of the page.

If you find yourself reaching for any of these, stop. Re-read `anti-slop.md`. Pick the alternative.

## Failure modes to watch

- **Stack drift**: user said React, sub-agent returns Vue. Catch this in your review of the sub-agent's output, ask for a redo.
- **Slop creep**: sub-agent claims it avoided Inter but actually used it. Grep the output for `Inter` and `font-family: Inter`. Reject and redo if found.
- **Missing states**: sub-agent shows a happy-path component with no loading/error/empty. Reject and redo.
- **Bare-bones output**: sub-agent returns 30 lines for a "landing page" request. Push back — landing pages have multiple sections.

## Error Handling

| Error condition | Recovery |
|---|---|
| Discovery incomplete (any of the 10 fields missing) | Return to discovery — never proceed without all 10 fields populated |
| User refuses to name a wow moment | Push back: "Give me one concrete moment, even tiny — something a visitor would remember." Block generation until provided |
| Stack auto-detection fails or conflicts | Ask the user explicitly which stack to target |
| Sub-agent returns slop tells (Inter on a brand surface, purple gradient, "Acme") | Reject and redo with explicit anti-slop reminder |
| Sub-agent ships code in the wrong stack | Catch in review, redo |
| SEO foundation missing on a public-web output | Reject; the output is incomplete without head surface, OG/Twitter, JSON-LD, semantic HTML, image discipline, CWV targets |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

---

## v2 Python integration — required preamble

Before generating any output, the LLM running this command MUST shell to the v2 Python engine to ground the work in structured data. This is not optional — running without the preamble means generating from training-data defaults (the slop signal).

### Step 1 — Load the saved discovery brief

```bash
test -f .ux/last-discovery.json && cat .ux/last-discovery.json
```

If the file doesn't exist, run `/ux-discover` first. Do NOT proceed without a complete 10-field brief.

### Step 1.5 — Brand: ingest an existing brand.md FIRST, else extract

**Input-first.** Before anything else, check if the project already has a `brand.md` (repo root, or walk up the directory tree) — the common `brand.md` convention. If so, **consume it** instead of extracting; it is the authoritative anchor:

```bash
python3 -m engine.cli.main brand --from-brand-md ./brand.md --out .ux
```

This parses the standard brand.md into `.ux/brand.json` (travels through the engine) + a normalized `.ux/brand.md`. Use it as the HARD ANCHOR exactly as an extracted brand below. Only if there is NO existing brand.md do you extract from the URL/screenshot (the steps below).

If the brief names a reference site/URL or provides a screenshot, the output MUST look like THEM, not the house style. Extract the brand FIRST — canonical rules in `references/process/brand-extraction.md`. The engine is offline, so YOU capture the signals; the engine normalizes + enforces.

1. **Capture the signals.** Open the URL / read the screenshot and **sample the logo pixels** for the dominant non-neutral color (the brand primary comes from the LOGO, not the most-painted CSS), read the logo's letterform style, and collect 2–3 secondary colors, the fonts, any real imagery URLs, and the voice. Write `.ux/brand-signals.json`:
   `{"name":"…","logo":{"src":"…","alt":"…"},"logo_colors":[{"hex":"#…"}],"brand_colors":[{"hex":"#…"}],"logo_type_style":"…","fonts":{"h1":"…","body":"…"},"imagery":["…"],"voice":"…"}`
2. **Build the anchor:**
   ```bash
   python3 -m engine.cli.main brand --signals-file .ux/brand-signals.json --out .ux
   ```
   Writes `.ux/brand.json` (travels through the engine) and `.ux/brand.md` (the human-readable anchor).
3. **CONFIRM before locking (do not skip).** Show the user the extracted `brand.md` — primary color, type direction, logo — in one short message and get a yes. A wrong auto-read (clay instead of amber) poisons the entire build; the 5-second check is the guardrail. If they correct it, edit `.ux/brand-signals.json` and re-run step 2.

If there is NO reference brand, skip this step (pure synthesis from the brief).

### Step 2 — Get the merged recommendation from the engine

```bash
# If a brand was extracted (Step 1.5), pass it so the palette + type anchor to THEM.
BRAND=""; [ -f .ux/brand.json ] && BRAND="--brand-file=.ux/brand.json"
python3 -m engine.cli.main --no-pretty recommend \
  --brief-file=.ux/last-discovery.json $BRAND > .ux/last-recommendation.json 2>/dev/null \
  || echo "engine not installed — falling back to v1 prose-only mode"
```

When `--brand-file` is passed, the recommendation's `palette.colors.primary` is the brand color (from the logo), and it carries `brand` + `type_directive` blocks — the build uses THOSE, not the engine's default pick.

Inspect the recommendation:
```bash
cat .ux/last-recommendation.json | python3 -c "
import json, sys
r = json.load(sys.stdin)
print('STYLE:    ', (r.get('style') or {}).get('name'))
print('PALETTE:  ', (r.get('palette') or {}).get('name'))
print('TYPE:     ', (r.get('type_pair') or {}).get('name'))
print('MOTION:   ', [m['id'] for m in r.get('motion', [])[:5]])
print('COMPS:    ', [c['id'] for c in r.get('components', [])[:6]])
print('BRANDS:   ', [b['id'] for b in r.get('brand_exemplars', [])[:5]])
print('GUARDRAILS:', len(r.get('guardrails', [])), 'anti-pattern rules active')
"
```

### Step 2.5 — Select the page-level section sequence (richness)

A recommendation gives you the *vocabulary* (style/palette/type). The page
*skeleton* — what sections appear and in what order — comes from the page-sequence
selector. Pick one by the brief's goal so the output is RICH and COMPLETE, not a
hero + three cards.

```bash
python3 -c "
import json
from engine.page_sequence import select_sequence
brief = json.load(open('.ux/last-discovery.json'))
goal = brief.get('goal') or brief.get('primary_goal') or brief.get('product_type') or ''
query = goal or (str(brief.get('product_type','')) + ' ' + str(brief.get('audience','')))
seq = select_sequence(query) or select_sequence(json.dumps(brief))
print(json.dumps(seq, indent=2) if seq else 'no sequence matched')
" 2>/dev/null
```

Then EXPAND the whole sequence in the build (this is non-negotiable for richness):

- Render EVERY section in `section_sequence`, in order — do not trim to the few you find easiest.
- Map ALL source content into it: every sector -> a Category pill, every size/package -> an Item card, every benefit -> a Value card or checklist item. Completeness over neatness — one source item, one element.
- Give EVERY card, pill, and stat a relevant inline SVG icon (Lucide-style, `currentColor`, 1.5–2px stroke). Never emoji, and never a numbered-placeholder generic glyph.
- Include the `conversion_mechanisms` the goal needs even if the source page lacked them. For `lead-gen-service` that means an inline hero form, a proof/stats bar, trust signals, and a visible phone affordance.

Pass the selected sequence to the frontend-engineer sub-agent as the page skeleton.

### Step 3 — Use the recommendation as hard constraints

The engine's picks are not suggestions — they're constraints:
- The picked `style.tokens` are the design vocabulary you generate from
- The picked `palette.colors` are the only color tokens used
- The picked `type_pair` is the only typography (display + body + mono)
- The 35+ `guardrails` are checked-against during generation — do NOT emit code that matches any anti-pattern regex
- The 5 `brand_exemplars` are the visual reference for taste

### Step 4 — Generate output

Dispatch the `frontend-engineer` sub-agent (Task tool) with the recommendation passed in as creative-direction context. Generate the page/component as requested by the brief, using ONLY the picked style + palette + type + motion presets + components.

**If a brand was extracted (Step 1.5):** paste the full `.ux/brand.md` into the sub-agent prompt and state that the brand is a HARD ANCHOR — use the client's logo, the brand primary color (the recommendation's palette is already anchored to it), and type matching the logo style; never fall back to the house style or a rejected default font. **Preserve the client's existing human copy verbatim** unless the brief explicitly asks for a rewrite.

### Step 5 — Lint + brand-fidelity gate before reporting

```bash
python3 -m engine.cli.main --no-pretty lint <output-paths> --threshold high
```

Exit code non-zero means a high+ finding landed in your output. Fix before declaring done.

**Responsive gate — HARD, as hard as the brand gate. This is WRAP-AWARE and HEIGHT-AWARE, not scroll-only.** Run at **390px AND 360px** in a headless DOM and assert ALL of (a)–(e):

> **Run the packaged verifier first** — it is the real gate, not a guess:
> ```bash
> node scripts/verify-responsive.mjs <output.html> 360,390 <out-dir>
> ```
> Real headless Chrome at a TRUE device viewport (self-calibrated so a lying viewport is caught), it measures **(a) horizontal overflow** and **(e) sticky-chrome height** reliably and **writes a screenshot per width so you can SEE the page.** Honesty contract: exit `0` = verified clean · `1` = FAIL (it names the cause — usually a fixed min-width wider than the device, or a tall pinned bar) · `2` = DEGRADED/UNVERIFIED (no Chrome, or the viewport was not honored) — **you have NOT verified; eyeball on a real device and never claim passed.** It does NOT catch **(b)/(c)/(d)** nav wrap/collision or the *feel* — open the screenshots it writes and check those by eye. A green from a DEGRADED run is not a green. See `references/foundations/responsive.md`.

- **(a) No horizontal scroll** — `document.documentElement.scrollWidth <= window.innerWidth`. The page never scrolls sideways on a phone.
- **(b) The header/nav stayed one row** — the sticky header/primary nav bar stays a single row. `scrollWidth` alone MISSES this: a nav that wrapped to two rows still reports `scrollWidth == innerWidth`, so it sails through a scroll-only gate. Detect the wrap directly: the bar's `offsetHeight` exceeds ~1.6x its single-row content height, OR its flex children span more than one distinct row (compare child vertical centers, not raw `offsetTop`, since `align-items:center` shifts each child). The **utility/announcement topbar is NOT a strict one-row bar** — but its intended mobile state is now ONE compact centered line (middot-separated claims), or fewer claims, and it is **non-sticky** (see component-behaviors.md). Check it for "not ragged AND not tall": its `|` dividers are hidden on mobile, it does not wrap mid-phrase with dangling dividers, and it does not balloon into a tall stacked block. (A topbar collapsed to one line passes the strict one-row check too; the stacked-lines escape hatch is reserved for 1–2 short items and must never make the header tall — its height is policed by (e).)
- **(c) No short inline label wrapped** — for the brand wordmark and every button/CTA label, assert it is on ONE line: `el.scrollHeight <= 1.4 * lineHeight`. (Measure the label element itself, not its button wrapper — a chip/icon inside the button inflates the button's `scrollHeight` and gives a false positive. Wrap a bare label text node in its own `<span>` so it is measurable. Resolve `line-height:normal` to `fontSize * 1.2`.)
- **(d) Header-bar children do not collide/overlap** — `nowrap` (the fix for (c)) does not always cause horizontal scroll; inside a flex bar it can instead make the wordmark **overlap the CTA** while `scrollWidth == innerWidth` AND each label still measures one line — so (a), (b), and (c) ALL pass on a visibly-broken bar (observed). Catch it directly: no two of the header bar's one-row children's rects may intersect, i.e. each child's `right` must stay within the next child's `left` (and within the bar's content box). When the wordmark cannot fit beside the logo + CTA without colliding, the fix is to shrink it or **collapse to the logomark** (hide the words) — never overlap, never two lines.
- **(e) The sticky/fixed top chrome is not too tall** — sum the `offsetHeight` of every **top-anchored** `position:sticky` / `position:fixed` element, **de-duped for nesting** (drop any element contained by another in the set; count the OUTERMOST only, so a sticky child inside a sticky parent is not double-counted). "Top-anchored" means it pins at the top: computed `position` is sticky/fixed AND computed `top` ≈ 0. **Do NOT also require resting `getBoundingClientRect().top` ≈ 0** — when a non-sticky utility bar sits ABOVE a `sticky; top:0` header, that header's rest `rect.top` equals the bar's height (e.g. ~26px), so a rest-rect check would wrongly EXCLUDE the very header this gate exists to measure. A bottom-fixed bar (`bottom:0`, so `top:auto`) yields `NaN` for `top` and is excluded; a `top:80px` side rail is excluded by `|top| > 1`. **FAIL if the sum exceeds ~96px (hard ceiling) OR > ~20% of `window.innerHeight`.** This is the bug observed on a real phone: a tall sticky header (~168px — a utility bar stacked to four centered lines, pinned together with the nav) crushes the viewport and reads as broken. The page TARGET is ≤72px (one nav row); the 96px is the absolute gate ceiling. An over-tall sticky header is a failure — report it and fix it (drop decorative bars out of the sticky container so only the nav stays pinned, trim padding) before declaring done. Note: a sticky element is bounded by its containing block, so the correct fix is to keep the sticky wrapper around the nav ALONE — a utility bar left inside the sticky `<header>` both inflates this number AND lets the nav unstick once the header box scrolls past.

**Point the three selectors at the page under test — they are named-per-page, NOT auto-detected.** The snippet has three constants at the top — `NAV_ROW`, `WORDMARK`, `LABELS` — defaulted to this page's (skiphire) real values as a worked example. Set them to the page you are checking: the *innermost* nav row (NOT the whole `<header>` — the utility/announcement topbar is a separate bar, so policing the whole header false-flags it as "wrapped"), the brand wordmark element, and the *isolated* label spans (a label that has been wrapped in its own `<span>` away from any icon/chip). The sticky-height check (e) needs NO selector — it auto-discovers every top-anchored sticky/fixed element. Do NOT replace these with generic `header [class*=nav]` / "first link in header" structural guesses — that was tried and it mis-resolves the whole header instead of the nav row and the topbar mailto link instead of the wordmark, producing a false-positive storm. The operator running this gate just built the page and can read its markup; aiming three selectors is the contract. **Non-resolution is LOUD, not silent:** if any target resolves nothing, the snippet prints a `WARNING` and the gate is DEGRADED to horizontal-scroll-only — which is exactly the blind spot this gate exists to close, so treat a degraded run as unverified until the selectors are fixed. Any button without an isolated label span is reported "unmeasured" (never false-flagged by measuring button+chip) — wrap its label in a span or eyeball it.

**A wrapping nav, a wordmark that splits mid-name or overlaps the CTA, a button/CTA label on two lines, OR an over-tall sticky header (sticky/fixed top chrome > ~96px) is a CRITICAL fail — always report it and fix it before declaring done.** This is the user's standing instruction: a nav/label that wraps on mobile, or a tall sticky header that crushes the viewport, must ALWAYS be reported and fixed. Horizontal scroll is also CRITICAL. None of these is a nice-to-have.

Use whatever headless browser is on hand. Playwright is the cleanest:

```bash
python3 - "$OUTPUT_HTML" <<'PY'
import sys, pathlib
from playwright.sync_api import sync_playwright   # pip install playwright && playwright install chromium
url = pathlib.Path(sys.argv[1]).resolve().as_uri()
fail = False
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (390, 360):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2)
        pg.goto(url); pg.wait_for_timeout(400)
        m = pg.evaluate("""() => {
          // ===== SET THESE THREE TO THE PAGE UNDER TEST (do NOT auto-detect — see note) =====
          // Values below are this page's (skiphire) real selectors, as a worked example.
          const NAV_ROW = '.navrow';                         // the innermost nav row (NOT the whole header — the topbar may intentionally stack)
          const WORDMARK = '.brand .wm b';                   // the brand wordmark text element
          const LABELS = '.btn .btn-label';                  // ISOLATED label spans only (a label wrapped away from its icon/chip)
          // ================================================================================
          const lh = el => { const c = getComputedStyle(el); let l = parseFloat(c.lineHeight);
            return isFinite(l) ? l : parseFloat(c.fontSize) * 1.2; };
          const vis = el => el && el.offsetParent !== null && el.getBoundingClientRect().width > 0;
          const navBar = document.querySelector(NAV_ROW);
          // (a) horizontal scroll + the offending nodes
          const overflow = [...document.querySelectorAll('*')]
            .filter(e => e.getBoundingClientRect().right > window.innerWidth + 1)
            .slice(0, 8).map(e => e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).trim().split(/\\s+/)[0] : ''));
          // (b) the nav row is ONE row: height-ratio is robust; row-count via child CENTERS
          const barWrapped = bar => { if (!bar) return null;
            const kids = [...bar.children].filter(vis);
            const single = kids.length ? Math.max(...kids.map(c => c.offsetHeight)) : bar.offsetHeight;
            const rows = new Set(kids.map(c => { const r = c.getBoundingClientRect(); return Math.round(r.top + r.height / 2); })).size;
            return { h: bar.offsetHeight, single, ratio: +(bar.offsetHeight / single).toFixed(2),
                     wrapped: bar.offsetHeight > 1.6 * single || rows > 1 }; };
          // (c) short labels on ONE line — wordmark + each ISOLATED label span. Never measure a
          //     button that contains an icon/chip (its scrollHeight is box height, a false wrap):
          //     such a label is reported "unmeasured — wrap it in a span or eyeball it".
          const labelWrapped = el => { if (!el) return null;
            return { sh: el.scrollHeight, lh: +lh(el).toFixed(1),
                     ratio: +(el.scrollHeight / lh(el)).toFixed(2), wrapped: el.scrollHeight > 1.4 * lh(el) }; };
          const wmEl = document.querySelector(WORDMARK);
          const labelEls = [...document.querySelectorAll(LABELS)].filter(vis);
          const labels = [{ sel: 'wordmark', r: labelWrapped(wmEl) },
                          ...labelEls.map((el, i) => ({ sel: 'label[' + i + ']:' + (el.textContent || '').trim().slice(0, 16), r: labelWrapped(el) }))]
                         .filter(x => x.r);
          // (d) NAV-ROW children must not overlap — nowrap can make the wordmark overlap the CTA
          //     while (a)/(b)/(c) all pass. Scoped to NAV_ROW so the intentionally-stacked topbar
          //     is not flagged. This is the only check that catches the overlap class of bug.
          let collide = null;
          if (navBar) { const kids = [...navBar.querySelectorAll('*')].filter(vis)
              .filter(k => (k.textContent || '').trim() || k.querySelector('img,svg'));
            const boxes = kids.map(k => k.getBoundingClientRect());
            for (let i = 0; i < boxes.length && !collide; i++)
              for (let j = i + 1; j < boxes.length; j++) {
                const a = boxes[i], b = boxes[j];
                if (kids[i].contains(kids[j]) || kids[j].contains(kids[i])) continue;  // skip ancestor/descendant
                const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
                const oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
                if (ox > 2 && oy > 2) { collide = 'nav children overlap'; break; }
              } }
          // (e) sticky-header height budget — sum offsetHeight of every TOP-ANCHORED
          //     sticky/fixed element, de-duped for nesting (outermost only). Auto-discovered,
          //     no selector. A tall sticky header (utility bar stacked + pinned with the nav)
          //     crushes the viewport — the exact on-phone bug this catches.
          const sticky = [...document.querySelectorAll('*')].filter(el => {
            const c = getComputedStyle(el);
            if (c.position !== 'sticky' && c.position !== 'fixed') return false;
            if (!vis(el)) return false;
            // Top-anchored = pins at the top: computed `top` ~ 0. Do NOT also require
            // rect.top ~ 0 at rest — a `sticky; top:0` header sitting below a scroll-away
            // utility bar has rest rect.top ~ (bar height), and that check would wrongly
            // EXCLUDE the very header this gate exists to measure. A bottom-fixed bar
            // (top:auto) yields NaN here and is excluded; a `top:80px` rail is excluded.
            const top = parseFloat(c.top);
            return isFinite(top) && Math.abs(top) <= 1;
          });
          const outermost = sticky.filter(el => !sticky.some(o => o !== el && o.contains(el)));
          const stickyEls = outermost.map(el => ({
            tag: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).trim().split(/\\s+/)[0] : ''),
            h: el.offsetHeight }));
          const stickyTotal = stickyEls.reduce((s, e) => s + e.h, 0);
          return { iw: window.innerWidth, ih: window.innerHeight, sw: document.documentElement.scrollWidth, overflow,
                   navFound: !!navBar, nav: barWrapped(navBar), wmFound: !!wmEl, labelCount: labelEls.length,
                   labels, collide, stickyEls, stickyTotal };
        }""")
        hscroll = m["sw"] > m["iw"]
        navwrap = m["nav"] and m["nav"]["wrapped"]
        labelwrap = [x["sel"] for x in m["labels"] if x["r"]["wrapped"]]
        collide = bool(m["collide"])
        # (e) sticky-header height: hard ceiling 96px OR > 20% of innerHeight
        sticky_total = m["stickyTotal"]
        sticky_tall = sticky_total > 96 or sticky_total > 0.20 * m["ih"]
        degraded = (not m["navFound"]) or (not m["wmFound"]) or (m["labelCount"] == 0)
        print(f"[{w}px] iw={m['iw']} sw={m['sw']} h-scroll={hscroll} navFound={m['navFound']} nav={m['nav']}")
        print(f"        wmFound={m['wmFound']} labelSpans={m['labelCount']} labelWraps={labelwrap or 'none'} collide={m['collide'] or 'none'}")
        print(f"        sticky-chrome={sticky_total}px (ceiling 96, target <=72) too-tall={sticky_tall} parts={m['stickyEls']}")
        if m["overflow"]: print(f"        overflowing: {m['overflow']}")
        if degraded:
            print("        WARNING: a target (NAV_ROW / WORDMARK / LABELS) resolved nothing — point it at THIS page's elements. "
                  "The gate is DEGRADED (h-scroll-only for a/b/c/d; the sticky-height check (e) still runs) until it does; "
                  "any button without an isolated label span is unmeasured — eyeball it.")
        if hscroll or navwrap or labelwrap or collide or sticky_tall: fail = True
    b.close()
sys.exit(1 if fail else 0)
PY
```

If Playwright is not installed, read the SAME signals through any headless-DOM tool you have — a headless-Chrome eval, or an **MCP browser-preview that supports a viewport resize + a JS eval** (the cleanest fallback: resize to 360/390, then eval the measurement function above). Always read `window.innerWidth` first and confirm it is ~390/360 before trusting any number. **Headless screenshots are unreliable in this toolchain, but a DOM eval of `scrollWidth` / bar heights / label `scrollHeight` / summed sticky `offsetHeight` is reliable.** The honest backstop for the composed-vs-hollow judgment (and for anything the eval cannot prove) is to DEPLOY the iteration and eyeball it on a real phone — an un-eyeballed mobile layout is unverified. On a (b)/(c) failure the bar height and the per-label ratios name exactly what wrapped; on an (a) failure the `overflow` list names the offending nodes (almost always a fixed multi-column grid or a `100vw` element); on an (e) failure the `parts` list names which sticky element(s) sum over the ceiling (almost always a utility/announcement bar pinned together with the nav — move it OUT of the sticky container). For (e), also confirm the nav actually STAYS pinned after the topbar is unstuck: `scrollTo(0,600)` then assert the nav's `getBoundingClientRect().top` ≈ 0 (stuck) while the former topbar's `bottom < 0` (scrolled away) — a height-at-rest measurement alone does not prove the nav still sticks.

**If a brand was extracted, also run the brand-fidelity HARD FLOOR** — an off-brand page fails no matter how good it looks (it must use the brand primary, carry the logo, and ship real imagery):

```bash
python3 -c "
import json, sys
from engine.evaluator import evaluate
from engine.brand.extract import BrandProfile
b = json.load(open('.ux/brand.json'))
prof = BrandProfile(**{k: v for k, v in b.items() if k in BrandProfile.__dataclass_fields__})
ev = evaluate(html=open('<output.html>').read(), brand_profile=prof)
print('brand_fidelity', ev.brand_fidelity, '| imagery', ev.imagery, '| passed', ev.brand_passed)
[print(' -', n) for n in ev.notes if 'BRAND FLOOR' in n]
sys.exit(0 if ev.brand_passed else 1)
"
```

Exit `1` = the output dropped the brand primary/logo or shipped no real imagery. Fix it (use the brand color, carry the logo, add real images) and re-run. **Do not declare done while the brand gate fails.**

### Fallback

If `python3 -m engine.cli.main` is not on PATH (user hasn't installed v2 yet), fall back to v1 prose-only behavior using references/foundations/*.md as the source of taste. The output quality will be lower but the command still works.
