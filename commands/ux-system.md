---
description: Propose a complete starter design system for a project that doesn't have one. Triggers on "we don't have a design system", "build us a system", "propose tokens", "what should our theme be".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-system

You are running the `/ux-system` command from the `ux` plugin. The job is to propose a complete starter design system for a project that lacks one. Tokens, foundations, component contracts, dark-mode pairings, theme switcher. Not a sketch — a usable starter.

## When to use

Triggers: "we don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS", "we need a token JSON", "design our brand foundations".

If the project already has a design system, do not run this. Recommend `/ux-component` against the existing system instead.

## Process

### 0. Discovery protocol (MANDATORY)

Before anything else, read `references/process/discovery-protocol.md` and run its intake. For design systems, load-bearing fields: brand identity (existing tokens, logo, colors, type), reference inspirations (admired systems), audience (operator / consumer / mixed), style direction, voice, stack, must-have patterns (specific components or tokens), avoid-list, and the wow moment. Group into 2 messages. Skip only on `--skip-discovery` or full-spec input. Without the wow moment, push back.

### 1. Capture inputs

Required:
- **Source material**: a brand brief, an existing site to derive from, a screenshot of inspiration, OR explicit "your call" with the target product type
- **Target stack**: Tailwind / CSS variables / Styled Components / Stitches / vanilla CSS / Blade + Tailwind / etc.
- **Output path**: default `design-system/` in the target project root; configurable

If anything's missing, ask once: *"Source material (brief / site / 'your call'), target stack, and output path? Or say 'defaults' and I'll pick."*

### 2. Read the references

Read before dispatching:
- `references/styles/anti-slop.md` — bans the architect must respect
- `references/styles/arsenal.md` — patterns the components should support
- `references/system/foundations.md` if present — house style for foundations
- Any existing `design-system/` files in the target — do not overwrite, propose alongside

### 3. Set the dials

System-level dials drive the architect:
- **DESIGN_VARIANCE**: 4 default for systems (systems should be calmer than landings)
- **MOTION_INTENSITY**: 3 default (components define motion; the system defines tokens for it)
- **VISUAL_DENSITY**: 5 default

### 4. Dispatch design-system-architect

Call `design-system-architect` via Task. Pass:
- Source material verbatim
- Target stack
- Output path
- Dial values
- Full content of `references/styles/anti-slop.md`
- Instruction to produce:
  1. **Token JSON** — colors (with semantic + brand layers), type scale, spacing scale, radius scale, shadow scale, motion duration + easing, breakpoints
  2. **5-10 foundation MDs** — color principles, type rules, spacing logic, motion principles, accessibility floor, dark mode strategy, voice tone, iconography (Material Symbols default), imagery rules, data viz palette
  3. **6-8 component contracts** — button, input, modal, card, table, navbar, badge, alert (at minimum). Each contract: anatomy, states, variants, accessibility notes, do/don't
  4. **Dark-mode pairings** — every light token has a dark counterpart, not just inverted
  5. **Theme switcher pattern** — CSS variable swap on `[data-theme]`, no JS for the toggle beyond setting the attribute

### 5. Format the output

```
─── system brief ───
Source:     <brand brief or derived-from source>
Stack:      <stack>
Output:     <path>
Dials:      DESIGN_VARIANCE=<n>, MOTION_INTENSITY=<n>, VISUAL_DENSITY=<n>

─── token highlights ───
Brand accent:    <hex + name>
Neutral scale:   <range>
Type scale:      <smallest>–<largest>, <n> steps
Spacing scale:   <unit>, <n> steps
Radius:          <values>
Motion:          <durations>, <easings>

─── files written ───
<tree of files with one-line purpose each>

─── self-review ───
Bans avoided:    <list>
Decisions made:  <2-3 key taste calls the architect made>

─── next ───
Recommended: /ux-component   (build components against the new system)
Other moves: /ux-design      (build a page against the system)
             /ux-a11y        (audit the token contrast)
             /ux-next        (let me decide)
```

### 6. Persist state

Write to `.ux/last-system.json`:

```json
{
  "command": "ux-system",
  "timestamp": "<ISO8601>",
  "source": "<source>",
  "stack": "<stack>",
  "output_path": "<path>",
  "dials": { "variance": <n>, "motion": <n>, "density": <n> },
  "tokens": {
    "brand_accent": "<hex>",
    "neutral_scale_steps": <n>,
    "type_scale_steps": <n>,
    "spacing_scale_unit": "<unit>"
  },
  "files_written": ["<paths>"]
}
```

## Hard rules

- No purple/blue AI gradient as the brand accent. Single high-contrast accent, saturation < 80%.
- No pure black (`#000`) anywhere in the neutral scale. Start at Zinc-950 or darker-but-not-black.
- Material Symbols is the default icon set; the system MUST specify font-variation-settings for it.
- Dark mode is mandatory. Every semantic token has a dark counterpart.
- Type scale uses a modular ratio, not arbitrary px jumps.
- Spacing scale is a single unit-based scale (4 or 8), not mixed.
- Color contrast at AA minimum on every text/background pairing in the docs.
- No 3-equal-cards example layouts in component contracts.
- Token JSON is the source of truth; CSS variables derive from it, not the other way around.

## Failure modes

- **Architect produces a single CSS file instead of a system**: reject. The output must be structured — tokens, foundations, contracts, separately.
- **Brand accent is purple/blue gradient**: reject, redo with a constrained palette.
- **Dark mode is just inverted light**: reject. Dark mode needs its own decisions (lower contrast, different elevation strategy).
- **No accessibility floor specified**: reject. Every system must state its AA/AAA target.
- **Output overwrites existing files**: stop and ask the user. Never silently overwrite.

## Next prompt

After `/ux-system`:
- `/ux-component` — build components against the new system
- `/ux-design` — build a page against the new system
- `/ux-a11y` — audit token contrast pairs
- `/ux-next` — let the conductor pick
