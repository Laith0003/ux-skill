---
description: Specialized dashboard generation. Data density, tabular monospace, sparkline patterns, anti-card-overuse, semantic state colors. Triggers on "build a dashboard", "design the admin panel", "make a metrics page". Use when designing or generating a dashboard / admin panel / analytics view, the user says "build a dashboard", specialized dashboard discipline — bento, tabular monospace, sparkline patterns. Skip when the user wants a marketing page with stats (use ux-design), the user wants only one widget (use ux-component), backend or infrastructure.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-dashboard

You are running the `/ux-dashboard` command from the `ux` plugin. The job is to produce a dashboard that respects data density and operator attention — not a marketing site with charts pasted on. Anti-card-overuse, monospace tabular numbers, semantic state colors, sparing motion.

## When to use

Triggers: "build a dashboard", "design the admin panel", "make a metrics page", "operator console", "analytics view", "KPI board", "monitoring screen". If the user wants a marketing landing page with stats, route to `/ux-design` instead.

## Process

### 0. Discovery protocol (MANDATORY)

Before anything else, read `references/process/discovery-protocol.md` and run its intake. For dashboards, highest-leverage fields: brand identity, references (admired dashboards), audience (operator / analyst / exec — different density needs), key metrics + data shape, style direction, voice for state messages, stack, must-have widgets (intelligent-list / command-input / live-status / wide-stream / contextual-focus), avoid-list, and the wow moment. Group into 2–3 messages. Push back on "anything's fine".

### 1. Capture the brief

Required:
- **Data shape**: what entities, what metrics, what relationships. Time-series? Categorical? Hierarchical?
- **Key metrics**: the 3-7 numbers that dominate the page
- **Audience**: operator (always-on, scan-and-act) / analyst (deep dive, filter and segment) / exec (status at a glance)
- **Stack**: React + Tailwind / Next.js / Vue / Blade + Alpine / etc.

If anything's missing, ask once: *"One line — data shape, key metrics, audience (operator/analyst/exec), stack?"*

### 2. Read the references

Read before dispatching:
- `references/styles/anti-slop.md` — the ban list
- `references/styles/arsenal.md` — pick dashboard-relevant patterns

Dashboard-relevant arsenal patterns (pick 3-5):
- **Bento grid** — asymmetric, intentional, never 3-equal-cards
- **Intelligent list** — auto-sorting, contextual ordering
- **Command input** — keyboard-driven filter/search
- **Live status with overshoot** — for real-time indicators, used sparingly
- **Wide data stream** — infinite carousel of metrics when there's more than fits
- **Contextual focus mode** — click a metric, get the deep-dive without page change
- **Hairline-separated metric blocks** — for tight KPI rows, no cards needed

### 3. Set the dials

- **DESIGN_VARIANCE**: 4 default — dashboards should be calmer than landings
- **MOTION_INTENSITY**: 3 default — restraint; data should feel still until it changes
- **VISUAL_DENSITY**: 8 default — dashboards are cockpits, not galleries

### 4. Dispatch sub-agents

Call `frontend-engineer` via Task. Pass:
- Brief verbatim
- Data shape + key metrics + audience
- Stack
- Dial values
- 3-5 arsenal patterns picked
- Full content of `references/styles/anti-slop.md`
- Explicit instruction: monospace tabular numbers, no purple gradients, max 2 live indicators per viewport, semantic state colors only

Dispatch `motion-engineer` in parallel for live indicators and state transitions. Dispatch `copy-writer` in parallel for empty states, error messages, and metric labels.

### 5. Format the output

```
─── dashboard brief ───
Data shape:  <summary>
Metrics:     <3-7 key metrics>
Audience:    <operator | analyst | exec>
Stack:       <stack>
Dials:       DESIGN_VARIANCE=<n>, MOTION_INTENSITY=<n>, VISUAL_DENSITY=<n>
Patterns:    <3-5 arsenal patterns>

─── generated ───
<code from sub-agent — verbatim>

─── layout logic ───
Grouping:    <how widgets are grouped — by border-t / divide-y / negative space>
KPI row:     <pattern used — hairline-separated / asymmetric bento / focus widget>
Live count:  <number of breathing/live indicators in initial viewport — must be ≤2>

─── self-review ───
Bans avoided:    <list>
Patterns used:   <list>
Accessibility:   <color-not-only confirmed for all chart series>

─── next ───
Recommended: /ux-component   (build a missing widget)
Other moves: /ux-polish      (cosmetic pass)
             /ux-a11y        (color-not-only audit for charts)
             /ux-motion      (verify live indicators don't fight attention)
             /ux-next        (let me decide)
```

### 6. Persist state

Write to `.ux/last-dashboard.json`:

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

## Hard rules

- Numbers use `font-mono` with tabular figures (`font-variant-numeric: tabular-nums`). Non-negotiable.
- NEVER 3-equal-cards for KPIs. Use asymmetric bento or hairline-separated metric blocks.
- Maximum 2 "breathing" / live-pulse indicators per viewport. More = noise.
- Default monochrome. Semantic state colors only (success / warning / danger / info). No purple gradients.
- No serif fonts on dashboards.
- Charts: every series has a non-color indicator (pattern, shape, label) — never color alone.
- Empty states, loading states, error states for every widget — non-negotiable.
- Animate `transform` and `opacity` only.
- Material Symbols default for icons.
- Group via negative space, hairlines (`border-t`), or `divide-y`. Don't card-wrap everything.
- No pure black (`#000`). Use Zinc-950, Charcoal, Off-Black.

## Failure modes

- **Card-overuse**: every widget wrapped in `rounded-lg shadow border`. Reject. Use hairlines and grouping.
- **3-equal-card KPI row**: classic AI dashboard pattern. Reject, replace with asymmetric bento.
- **Too many live indicators**: counts ≥3 in the initial viewport. Reject, reduce to ≤2.
- **Proportional digits in metrics**: numbers jitter on update. Reject, force `tabular-nums`.
- **Color-only chart series**: reject, add patterns/shapes/labels.
- **Marketing gradient on the analytics page**: reject, swap to neutral + semantic accent.
- **No empty/loading/error states**: reject and redo.

## Error Handling

| Error condition | Recovery |
|---|---|
| Data shape missing | Ask for entities + relationships + metrics in one combined question |
| Audience unclear (operator / analyst / exec) | Ask once; density and motion defaults depend on it |
| User answers "all of them" for audience | Push back — density and motion calls depend on a single primary audience; pick one |
| Key metrics list exceeds 7 numbers | Force a triage to the 3-7 that dominate; surface the rest as secondary |
| Sub-agent returns 3-equal-card KPI row | Reject and redo with hairline-separated or asymmetric bento |
| Sub-agent returns proportional digits in metrics | Reject; force `tabular-nums` |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

## Next prompt

After `/ux-dashboard`:
- `/ux-component` — build a missing widget
- `/ux-polish` — cosmetic pass on the dashboard
- `/ux-a11y` — color-not-only audit for charts, contrast for tabular data
- `/ux-motion` — verify live indicators don't fight attention
- `/ux-next` — let the conductor pick
