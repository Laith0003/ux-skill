---
description: Generate a single component (button, modal, navbar, sidebar, card, table, form, chart) from a spec. Triggers on "build a [component]", "create a pricing card", "make a modal", "add a navbar".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-component

You are running the `/ux-component` command from the `ux` plugin. The job is to produce a single, production-grade component that avoids generic AI aesthetics. One component, fully realized — all four interaction states, accessible, on-brand.

## When to use

Triggers: "build a button", "create a pricing card", "make a modal", "add a navbar", "design a sidebar", "I need a data table", "build a form", "make a chart component", or any single-element request.

If the user is asking for a full page or multi-section surface, hand off to `/ux-design` instead.

## Process

### 0. Discovery protocol (MANDATORY)

Before anything else, read `references/process/discovery-protocol.md` and run its intake on the user. For components, focus on: brand identity, 2–3 references for the component type, audience, style direction, voice, stack, imagery (if applicable), must-have-patterns, avoid-list, and the wow moment for THIS component specifically. Group into one or two messages. Skip only on `--skip-discovery` or if the spec already covers every field. Without the wow moment, push back.

### 1. Capture the spec

Required:
- **Component type**: button / modal / navbar / sidebar / card / table / form / chart / other
- **Stack**: React + Tailwind / Vue / Svelte / Blade + Alpine / vanilla HTML / etc.
- **Brand voice**: pull from `.ux/last-frame.json` if it exists, otherwise ask one-line: *"What's the voice — minimal / brutalist / editorial / playful / dark? Or 'your call'?"*

Optional but useful: specific behavior (auto-sort, multi-step, infinite scroll, drag-reorder), data shape, density target.

Do not ask three questions. One question that surfaces everything missing.

### 2. Read the references

Read both before writing:
- `references/styles/anti-slop.md` — the ban list
- `references/styles/arsenal.md` — the high-end pattern library

Pick 1-2 arsenal patterns that fit. For a button: live status with overshoot, optimistic update. For a modal: contextual focus mode. For a navbar: command input, intelligent list. For a card: hairline-separated metric blocks. For a table: intelligent list, monospace tabular. For a form: inline validation with field-level @error, multi-step wizard. For a chart: monochrome + semantic state colors only.

### 3. Set the dials

- **DESIGN_VARIANCE**: 5 default for components (4 for system components, 6 for marketing components)
- **MOTION_INTENSITY**: 4 default (3 for utility components, 5 for marketing components)
- **VISUAL_DENSITY**: 5 default (7 for tables/charts, 4 for buttons/modals)

### 4. Dispatch sub-agents

Call `frontend-engineer` via Task. Pass:
- The spec verbatim
- Dial values
- 1-2 arsenal patterns picked
- Full content of `references/styles/anti-slop.md`
- Target stack
- Instruction to return: code + self-review on bans avoided + patterns used

Dispatch `motion-engineer` in parallel if the spec involves motion (loading states, optimistic UI, micro-interactions, transitions). Dispatch `copy-writer` in parallel if the component has non-trivial copy (form labels, empty states, error messages, CTAs).

### 5. Format the output

```
─── component spec ───
Type:       <component type>
Stack:      <stack>
Voice:      <brand voice>
Dials:      DESIGN_VARIANCE=<n>, MOTION_INTENSITY=<n>, VISUAL_DENSITY=<n>
Patterns:   <1-2 arsenal patterns>

─── generated ───
<code from sub-agent — verbatim>

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
Recommended: /ux-component   (build the next one)
Other moves: /ux-polish      (cosmetic pass)
             /ux-a11y        (WCAG check)
             /ux-design      (assemble into a fuller surface)
             /ux-next        (let me decide)
```

### 6. Persist state

Write to `.ux/last-component.json`:

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

## Hard rules

- All four interaction states (default / hover / active / disabled) — non-negotiable.
- Loading + error + empty states wherever the component can hit them.
- Mandatory imagery if visual (avatars, product shots, illustrations) — use `picsum.photos/seed/<descriptive-seed>/W/H`.
- Google Material Symbols as icon default. Phosphor / Lucide / Radix acceptable secondary.
- Inter is allowed. Do not ban it.
- No scroll progress paths or scroll-tied SVG line drawing.
- No purple/blue AI gradients. Single high-contrast accent, saturation < 80%.
- No pure black (`#000`). Use Zinc-950, Charcoal, Off-Black.
- No emojis as icons.
- No 3-equal-cards layouts for grouped components.
- Animate `transform` and `opacity` only.
- Buttons/inputs that look identical when hovered, active, or disabled = failure.

## Failure modes

- **Stack drift**: sub-agent returns React when user said Vue. Catch in review, redo.
- **Missing states**: sub-agent shows the default state only. Reject and redo.
- **Slop creep**: sub-agent says "I avoided X" but the code uses X. Grep the output. Reject and redo.
- **Over-scope**: sub-agent returns a full landing page when asked for a single button. Trim to the requested component, surface the extra work as a `/ux-design` follow-up.
- **No motion when motion was specified**: re-dispatch with explicit motion brief.

## Next prompt

After `/ux-component`:
- `/ux-component` — build the next one
- `/ux-polish` — cosmetic pass
- `/ux-a11y` — accessibility audit
- `/ux-design` — assemble into a fuller surface
- `/ux-next` — let the conductor pick
