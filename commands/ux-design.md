---
description: Generate a beautiful, anti-AI-slop design or component from a brief. Dispatches the frontend-engineer sub-agent with creative direction drawn from anti-slop and arsenal references. Use when generating a new design or component from a brief, the user says "build me X" or "design a Y", after running discovery + intaking brand identity, producing premium frontend code with anti-AI-slop discipline. Skip when the user wants a review not a build (use ux-audit / ux-critique), the user wants only one component (use ux-component), backend or infrastructure work.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-design

You are running the `/ux-design` command from the `ux` plugin. The job is to generate a beautiful, high-end design or component from a brief — and explicitly NOT produce AI-slop output.

## When to use

Triggers: "design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "I need a hero section", "design a modal", any free-form request for a visual/UI deliverable.

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

### 2. Read the references

Before writing a single line of code, read both:
- `references/styles/anti-slop.md` — the ban list. Internalize every forbidden pattern.
- `references/styles/arsenal.md` — the high-end pattern library. Pick 2-4 patterns that fit the brief.

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

For any landing page or public-facing surface, read `references/foundations/seo.md` and require the frontend-engineer to ship the full SEO foundation (head surface, OG + Twitter, JSON-LD, semantic HTML, image discipline, CWV targets). Surface this requirement in your dispatch prompt. The output is incomplete without it. Use sensible placeholder values (`{TODO_FILL}` for canonical, og:image URL, etc.) when the brief doesn't supply them — let the user patch before deploy.

## Hard rules (non-negotiable)

- NEVER use purple/blue AI gradients. Single high-contrast accent, saturation < 80%.
- NEVER use generic names ("John Doe", "Acme", "Nexus") in placeholder content.
- NEVER use pure black (`#000`). Use Zinc-950, Charcoal, or Off-Black.
- NEVER use Unsplash URLs. Use `picsum.photos/seed/<descriptive-seed>/W/H` or real assets.
- NEVER ship a text-only wall — always include intentional imagery.
- NEVER use emoji as icons. Prioritize **Google Material Symbols** (load via Google Fonts: `Material+Symbols+Outlined` / `Rounded` / `Sharp`, styled with `font-variation-settings`). Phosphor / Radix / Lucide are acceptable secondary choices when an icon doesn't exist in Material Symbols.
- NEVER ship 3-equal-cards layouts. Use 2-col zig-zag, asymmetric, or horizontal scroll.
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
