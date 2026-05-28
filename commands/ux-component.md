---
description: Generate a single component (button, modal, navbar, sidebar, card, table, form, chart) from a spec. Triggers on "build a [component]", "create a pricing card", "make a modal", "add a navbar". Use when generating a single component, the user says "create a [button/modal/navbar/card/table/form/chart]", embedded into an existing surface — NOT a full page. Skip when the user wants a full page or multi-section surface (use ux-design), backend or infrastructure work.
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

## Error Handling

| Error condition | Recovery |
|---|---|
| Stack unclear | Ask one combined question covering stack + voice + behavior; do not ask three separate questions |
| Component type ambiguous (user says "thing to filter stuff") | List the candidate component types (table with command input / sidebar with filter chips / autocomplete combobox) and ask which one |
| Sub-agent returns happy-path only, no states | Reject and redo — all four interaction states are non-negotiable |
| Sub-agent ships code in the wrong stack | Catch in review, redo |
| Spec says "component" but the brief implies a full page | Trim to the requested component, surface the extra work as a `/ux-design` follow-up |
| `.ux/last-frame.json` absent and voice not provided | Ask one-line: "What's the voice — minimal / brutalist / editorial / playful / dark? Or 'your call'?" |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

## Next prompt

After `/ux-component`:
- `/ux-component` — build the next one
- `/ux-polish` — cosmetic pass
- `/ux-a11y` — accessibility audit
- `/ux-design` — assemble into a fuller surface
- `/ux-next` — let the conductor pick

---

## v2 Python integration — required preamble

Before generating any output, the LLM running this command MUST shell to the v2 Python engine to ground the work in structured data. This is not optional — running without the preamble means generating from training-data defaults (the slop signal).

### Step 1 — Load the saved discovery brief

```bash
test -f .ux/last-discovery.json && cat .ux/last-discovery.json
```

If the file doesn't exist, run `/ux-discover` first. Do NOT proceed without a complete 10-field brief.

### Step 2 — Get the merged recommendation from the engine

```bash
python3 -m engine.cli.main --no-pretty recommend \
  --brief-file=.ux/last-discovery.json > .ux/last-recommendation.json 2>/dev/null \
  || echo "engine not installed — falling back to v1 prose-only mode"
```

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

### Step 3 — Use the recommendation as hard constraints

The engine's picks are not suggestions — they're constraints:
- The picked `style.tokens` are the design vocabulary you generate from
- The picked `palette.colors` are the only color tokens used
- The picked `type_pair` is the only typography (display + body + mono)
- The 35+ `guardrails` are checked-against during generation — do NOT emit code that matches any anti-pattern regex
- The 5 `brand_exemplars` are the visual reference for taste

### Step 4 — Generate output

Look up the requested component name in `.ux/last-recommendation.json`'s `components` list. If present, generate using its `anatomy`, `states`, `tokens_used`, and `motion` fields as the spec. If not present, search `data/components.json` directly via `cat data/components.json | jq '.entries[] | select(.name | test("<name>"; "i"))'`. Dispatch `frontend-engineer` to build it.

### Step 5 — Lint the output before reporting

```bash
python3 -m engine.cli.main --no-pretty lint <output-paths> --threshold high
```

Exit code non-zero means a high+ finding landed in your output. Fix before declaring done.

### Fallback

If `python3 -m engine.cli.main` is not on PATH (user hasn't installed v2 yet), fall back to v1 prose-only behavior using references/foundations/*.md as the source of taste. The output quality will be lower but the command still works.
