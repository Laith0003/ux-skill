---
description: Propose a complete starter design system for a project that doesn't have one. Triggers on "we don't have a design system", "build us a system", "propose tokens", "what should our theme be". Use when proposing a starter design system, generating tokens / foundations / components from a brand brief, the project has no existing design system, extracting a system from an existing site. Skip when the project already has a complete design system (use ux-component to build against it), backend or infrastructure.
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

## Error Handling

| Error condition | Recovery |
|---|---|
| Existing partial system detected | Ask whether to extend or replace; never silently overwrite |
| Brand brief missing | Reuse brand library from `references/brands/` if a brand was named; otherwise ask the user to paste a brief or pick "your call" |
| Source material is a screenshot only | Extract tokens visually with stated uncertainty; flag derived tokens for user confirmation |
| Target stack unclear | Ask for the stack before dispatching the architect — token output format is stack-dependent |
| Output path collides with existing files | Stop and ask the user; never silently overwrite |
| Architect returns a single CSS file instead of a structured system | Reject and redo with the structured-output instruction restated |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

## Next prompt

After `/ux-system`:
- `/ux-component` — build components against the new system
- `/ux-design` — build a page against the new system
- `/ux-a11y` — audit token contrast pairs
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

Use the picked style and palette as the system foundation. Generate tokens.css via `python3 -m engine.cli.main generate --brief-file=.ux/last-discovery.json --out-dir=./generated-system` which produces tokens.css + manifest.json. Then dispatch `design-system-architect` to expand into component contracts + foundation docs that consume those tokens.

### Step 5 — Lint the output before reporting

```bash
python3 -m engine.cli.main --no-pretty lint <output-paths> --threshold high
```

Exit code non-zero means a high+ finding landed in your output. Fix before declaring done.

### Fallback

If `python3 -m engine.cli.main` is not on PATH (user hasn't installed v2 yet), fall back to v1 prose-only behavior using references/foundations/*.md as the source of taste. The output quality will be lower but the command still works.
