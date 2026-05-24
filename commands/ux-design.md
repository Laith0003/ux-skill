---
description: Generate a beautiful, anti-AI-slop design or component from a brief. Dispatches the frontend-engineer sub-agent with creative direction drawn from anti-slop and arsenal references.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-design

You are running the `/ux-design` command from the `ux` plugin. The job is to generate a beautiful, high-end design or component from a brief — and explicitly NOT produce AI-slop output.

## When to use

Triggers: "design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "I need a hero section", "design a modal", any free-form request for a visual/UI deliverable.

## Process

### 1. Capture the brief

If the user provided a brief in the same turn, use it. If not, ask ONCE for:
- **Product type**: landing page / dashboard / component / e-commerce / portfolio / SaaS app / mobile / brand site
- **Style direction**: minimal / brutalist / glassmorphism / editorial / playful / dark mode / etc. (or "you choose")
- **Stack**: React + Tailwind / Next.js / Vue / Blade + Alpine / vanilla HTML / Astro / whatever they have

Don't ask 4 questions in a row. One short question that surfaces all three, e.g.: *"One line: what's the product, what's the vibe, and what stack? Or say 'your call' and I'll pick."*

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

## Hard rules (non-negotiable)

- NEVER use Inter font. Use Geist, Outfit, Cabinet Grotesk, or Satoshi.
- NEVER use purple/blue AI gradients. Single high-contrast accent, saturation < 80%.
- NEVER use generic names ("John Doe", "Acme", "Nexus") in placeholder content.
- NEVER use pure black (`#000`). Use Zinc-950, Charcoal, or Off-Black.
- NEVER use Unsplash URLs. Use `picsum.photos/seed/<random>/W/H` or SVG.
- NEVER ship 3-equal-cards layouts. Use 2-col zig-zag, asymmetric, or horizontal scroll.
- NEVER animate `width`/`height`/`top`/`left`. Use `transform` and `opacity` only.
- NEVER skip empty/loading/error states.
- NEVER use serif fonts on dashboards.
- NEVER produce centered hero sections when `DESIGN_VARIANCE > 4` — force asymmetry.

If you find yourself reaching for any of these, stop. Re-read `anti-slop.md`. Pick the alternative.

## Failure modes to watch

- **Stack drift**: user said React, sub-agent returns Vue. Catch this in your review of the sub-agent's output, ask for a redo.
- **Slop creep**: sub-agent claims it avoided Inter but actually used it. Grep the output for `Inter` and `font-family: Inter`. Reject and redo if found.
- **Missing states**: sub-agent shows a happy-path component with no loading/error/empty. Reject and redo.
- **Bare-bones output**: sub-agent returns 30 lines for a "landing page" request. Push back — landing pages have multiple sections.
