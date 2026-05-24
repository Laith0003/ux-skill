# How to Design a Dashboard with Claude Code

Generate a premium dashboard in Claude Code using `/ux-dashboard`. The command applies dashboard-specific discipline — data density, tabular monospace numbers, sparkline patterns, anti-card-overuse, semantic state colors, and the 5 dashboard archetypes (intelligent list, command input, live status, wide data stream, contextual focus).

This page walks you through running the command, answering the discovery prompts, reviewing the output, and applying the discipline that separates a shipped operator tool from a generic admin template.

---

## Why most AI-generated dashboards look generic

Default model output for a dashboard request reliably produces the same six failures. Recognize them so you can reject them.

1. **Card overuse.** Every metric wrapped in its own card with a 16px-radius border, soft shadow, and 24px padding. A real dashboard uses cards for grouping, not for decoration. Most data lives on flat tables, inline rows, or in a single bento panel.

2. **The equal-3 KPI grid.** Three identical cards in a row, each with a label, a big number, and a small percentage delta. Every AI dashboard has this. Operators never read three KPIs equally — one is primary, one is secondary, one is contextual. The visual hierarchy should reflect that.

3. **Sans-serif numbers in tables.** Numerals in proportional sans-serif do not align vertically. Column scanning fails. Real dashboards use `font-variant-numeric: tabular-nums` or a true monospace numeral font.

4. **Decorative gradients in status colors.** Success is solid green, not a green-to-teal gradient. Warning is solid amber. Operator dashboards do not have time for ambiguity. A gradient on a state pill reads as marketing, not telemetry.

5. **No empty / loading / error states.** The dashboard renders only the happy path. The first real moment a user sees it — fresh account, no data — they see broken UI.

6. **Live indicators on everything.** Five blinking dots in one viewport. The eye loses the signal because every signal is treated as urgent. Real dashboards cap live indicators at 2 per viewport and reserve them for true real-time fields.

`/ux-dashboard` blocks every one of these defaults.

---

## What `/ux-dashboard` does differently

`/ux-dashboard` is a dashboard-specific command, not a general-purpose UI generator. It runs a discovery protocol that captures the operator role, the data shape, and the decision the dashboard supports before any code is written. Then it applies dashboard-specific discipline:

- Bento 2.0 layout for KPIs (asymmetric grid, one anchor metric)
- Tabular monospace numerals everywhere a number is rendered
- Anti-card-overuse rule (cards group, never decorate)
- Semantic state palette (success / warning / danger / info — solid only)
- Capped live indicators (max 2 per viewport)
- Inline sparklines (no external chart library required)
- Skeleton, empty, error, and zero-data states generated alongside the happy path
- Keyboard-first density (command-K, slash filters, arrow-row navigation)
- WCAG AA contrast on every metric pair (color-not-only)

It also enforces the five dashboard archetypes. You pick one in discovery, and the layout, density, and motion adapt to fit.

---

## The 5 dashboard archetypes

Every dashboard maps to one of five archetypes. Picking the wrong archetype is the most common reason a generated dashboard feels off.

### 1. Intelligent List

A long, scannable list of items the operator triages. Emails, support tickets, fraud alerts, deployment runs. The primary action is "pick the next thing to look at."

- High row density (40–48px per row)
- Sticky filters, sticky column headers
- Hover-revealed actions (no permanent action column)
- Keyboard navigation is first-class
- Selection state survives filter changes

### 2. Command Input

A single primary input drives the whole screen. The dashboard is essentially a results surface for one question. Search consoles, query builders, prompt sandboxes.

- Input is centered above the fold
- Results are the dominant surface
- History as a sidebar, not the main area
- Streaming results render top-down
- Empty state is the input itself (no preview cards needed)

### 3. Live Status

A small number of metrics that update in real time. Trading consoles, ops dashboards, on-call surfaces. The operator stares at this for hours; the question is "did anything just change?"

- Numbers are giant and tabular
- Deltas are color-coded but never gradient
- Live indicators capped at 2
- Sparklines inline beside numbers
- Sound or flash on threshold (optional, off by default)

### 4. Wide Data Stream

Tables with many columns and high row counts. Logs, transactions, events, audit trails. The operator wants to filter, search, and export.

- Tabular numerals are non-negotiable
- Horizontal scroll allowed, but pin first 2 columns
- Filter chips above the table, sortable on every column
- Row hover reveals expand action
- Export is a primary affordance, not buried in a menu

### 5. Contextual Focus

A single record with rich context. Customer detail, order detail, incident detail. The operator is deep inside one thing.

- Hero summary at top (the answer to "what is this?")
- Tabs or accordion for sub-sections
- Activity timeline as a first-class panel
- Related-records sidebar
- Primary actions float top-right, secondary actions inline per section

---

## Step 1: Run `/ux-dashboard`

In Claude Code, type:

```
/ux-dashboard
```

The command does not start generating immediately. It enters discovery first.

If you want to skip discovery and run with defaults (not recommended for production work), pass `--quick`:

```
/ux-dashboard --quick
```

For an existing screen you want audited and upgraded rather than rebuilt:

```
/ux-dashboard --audit ./resources/views/dashboard.blade.php
```

The audit mode reports anti-pattern violations against the dashboard discipline checklist and outputs a patched version.

---

## Step 2: Answer dashboard-specific discovery

Discovery is not generic. It asks dashboard questions.

**Q1. Who is the operator?**
- Operator (handles incidents, triages queues, takes action)
- Analyst (explores data, finds patterns, exports)
- Executive (scans summary, makes go/no-go decisions)

The answer changes density. Operator gets dense rows and keyboard nav; analyst gets filters and exports; executive gets a single hero metric and trend.

**Q2. What is the data shape?**
- List of items (use Intelligent List archetype)
- Single search → many results (Command Input)
- Few metrics, frequently updating (Live Status)
- Many rows × many columns (Wide Data Stream)
- One record, deep context (Contextual Focus)

**Q3. What is the primary metric?**
Pick ONE metric that anchors the whole dashboard. If you cannot pick one, the dashboard is unfocused; redesign before coding.

**Q4. What are the 2–4 secondary metrics?**
These get smaller treatment in the bento. Anything beyond 4 is noise on first paint.

**Q5. What is the operator's primary action?**
"Resolve a ticket." "Approve a payout." "Promote a build." "Cancel a job." This action becomes the primary CTA — visible, keyboard-bound, never buried.

**Q6. What is the live data, if any?**
Be honest. If nothing is truly live (sub-15-second updates), say so. Then the dashboard does not get any live indicators. Polling every 60 seconds is not "live."

**Q7. What is the empty state?**
Brand new account. No data. What does the operator see? If you cannot answer this, the empty state will not get designed and will ship broken.

**Q8. What is the failure state?**
API down. Query timeout. Partial results. What does the dashboard show? This is where most dashboards fail in production.

**Q9. Is there an export?**
CSV? PDF? Print-friendly? If yes, it gets a primary affordance.

**Q10. Localization and direction?**
LTR only or RTL too? Number formats? Currency? Date format? If RTL, the bento layout and sparklines mirror correctly.

---

## Step 3: Review the output

The command outputs a single file by default. For a Laravel + Blade stack, it produces a Blade component. For a React or Vue stack, it produces an equivalent component file. Output includes:

- The full markup with the bento grid
- The state palette as inline CSS variables
- Tabular numeral utility classes
- Skeleton state
- Empty state
- Error state
- Sparkline SVG inline (no external dependency)
- Keyboard handlers for navigation
- ARIA live regions for the capped live indicators

Review with this checklist before accepting:

- [ ] Primary metric is visually 2–3x larger than secondary metrics
- [ ] Every number uses tabular-nums
- [ ] No more than 2 live indicators in any viewport
- [ ] Skeleton state covers every dynamic region
- [ ] Empty state has a clear call-to-action, not just an illustration
- [ ] Error state names the failure and the next action
- [ ] No card has decorative shadow + decorative gradient + decorative border at the same time
- [ ] Every state color works at WCAG AA on the surface it sits on
- [ ] RTL works (test by setting `dir="rtl"` on the root)
- [ ] Charts have a text summary for screen readers

If any item fails, run `/ux-polish` on the output to flag it.

---

## Dashboard discipline (what you should never break)

These rules are absolute. The command enforces them; you should too when editing afterward.

### No card overuse

A card has a purpose: it groups related fields and creates a focusable region. It is not a decoration. Rules:

- Do not wrap a single number in a card
- Do not put a card inside a card
- The bento panel itself is one card; the metrics inside it are not individually carded
- Hairline borders (1px) beat shadow + radius for grouping
- If a "card" has no border, no background, and no shadow, it is not a card — delete the wrapper

### Monospace numbers

Every numeral in the dashboard uses tabular-nums. This is non-negotiable for scannable tables and aligned KPIs.

```css
.dash-num {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
```

For true monospace (logs, IDs, tokens), use a monospace stack:

```css
.dash-mono {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}
```

Use proportional font for labels and prose. Use tabular nums for any number in a column. Use monospace for fixed-width tokens (IDs, hashes, dates that scan as columns).

### Breathing live indicators (max 2 per viewport)

A live indicator is a small dot or pill that animates to signal real-time data. It is a finite resource.

- Cap: 2 visible at once
- Animation: a slow pulse (1.5–2s ease-in-out, opacity 0.4 → 1)
- Color: semantic only (success green for "healthy live", danger red for "live alert")
- Never decorative: if the data is not actually updating in real time, no indicator

If your design wants more than two, prioritize. Demote the rest to static color pills.

```html
<span class="live-indicator" aria-label="Live">
  <span class="live-dot"></span>
  <span class="live-label">Live</span>
</span>
```

```css
.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}
@media (prefers-reduced-motion: reduce) {
  .live-dot { animation: none; }
}
```

### Semantic state colors

The palette is small and solid. No gradients on state.

- Success: solid green (use a single ramp anchor, e.g. `oklch(0.62 0.15 145)`)
- Warning: solid amber
- Danger: solid red
- Info: solid blue
- Neutral: grayscale ramp

State colors carry meaning. Brand color carries identity. Decoration uses neither — it uses neutrals.

### Density tiers

Pick one density per dashboard.

- Comfortable: 56–64px row height, 24px section padding (executive, low-frequency use)
- Standard: 44–48px row height, 16px section padding (analyst, mixed use)
- Compact: 32–40px row height, 12px section padding (operator, hours-per-day use)

Do not mix tiers in the same screen.

---

## Bento 2.0 layout for KPI sections

The bento is the dashboard equivalent of a hero. It anchors the screen with one primary metric and supports it with 2–4 secondary metrics in an asymmetric grid.

The geometry is intentionally asymmetric:

```
+-----------------------------+----------+
|                             |          |
|   PRIMARY METRIC            | SECONDARY|
|   (large, anchor, sparkline)|   1      |
|                             |          |
+-------------+---------------+----------+
| SECONDARY 2 | SECONDARY 3   | SECONDARY|
|             |               |    4     |
+-------------+---------------+----------+
```

Rules:

- The primary metric occupies a 2x2 area minimum
- Secondary metrics live in the remaining 1x1 cells
- The grid has no internal gutters wider than 1px (hairline separator) or 8px (gap)
- No external border around the whole bento — the bento IS the card
- Each cell has its own state color border (left edge, 2px) when surfacing a status
- Sparklines live INSIDE the metric cell, not below it

Avoid the equal-3 grid. Three identical KPI cards in a row is the single most recognizable AI-slop dashboard pattern.

Sample Tailwind grid for a 4-column bento:

```html
<section class="grid grid-cols-4 grid-rows-2 gap-px bg-border rounded-xl overflow-hidden">
  <div class="col-span-2 row-span-2 bg-surface p-6">
    <!-- primary metric -->
  </div>
  <div class="bg-surface p-4"><!-- secondary 1 --></div>
  <div class="bg-surface p-4"><!-- secondary 2 --></div>
  <div class="bg-surface p-4"><!-- secondary 3 --></div>
  <div class="bg-surface p-4"><!-- secondary 4 --></div>
</section>
```

The `gap-px` on a `bg-border` parent creates the hairline grid lines without separate border rules per cell. Each cell uses `bg-surface` to fill, leaving the 1px parent color as the separator.

---

## Chart accessibility (color-not-only)

A chart that uses color alone fails for colorblind users and screen reader users. The dashboard discipline requires three redundancies:

### 1. Direct labels, not legends

A legend forces the user to look at a swatch, match the color, find the line. A direct label on the line itself removes that step.

```svg
<g>
  <path d="M0,40 L20,30 L40,20 L60,15" stroke="var(--success)" fill="none" />
  <text x="62" y="15" font-size="12" fill="var(--success)">Revenue</text>
</g>
```

### 2. Pattern + color, not color alone

For bar charts, areas, or filled regions where multiple series stack, add a pattern (stripe, dot, cross-hatch) so the series is distinguishable in grayscale.

```svg
<defs>
  <pattern id="diag" patternUnits="userSpaceOnUse" width="6" height="6">
    <path d="M0,6 L6,0" stroke="currentColor" stroke-width="1" />
  </pattern>
</defs>
<rect fill="url(#diag)" />
```

### 3. Screen-reader summary

Every chart is preceded by a brief text summary that names the highest, lowest, and most recent value. Wrap the chart in a `figure` with a `figcaption`, and provide a longer description in a hidden region for screen readers.

```html
<figure role="figure" aria-labelledby="rev-cap" aria-describedby="rev-desc">
  <figcaption id="rev-cap">Revenue, last 30 days</figcaption>
  <svg aria-hidden="true"><!-- chart --></svg>
  <p id="rev-desc" class="sr-only">
    Revenue trended up from 12.4K on day 1 to 18.9K on day 30,
    with a peak of 21.2K on day 24 and a low of 11.0K on day 4.
  </p>
</figure>
```

### Keyboard-navigable data

For exploratory charts, expose the data points as a hidden but focusable list. Arrow-key navigation moves a marker on the chart and reads the value.

---

## Real example

You run `/ux-dashboard` for a payments-ops dashboard.

**Discovery answers:**
- Operator: ops engineer on-call
- Data shape: Live Status archetype
- Primary metric: settlement-success-rate (live)
- Secondary metrics: pending volume, failed-in-last-hour, average-latency
- Primary action: "Investigate failure" (opens drill-down)
- Live data: yes, settlement-success-rate updates every 5 seconds
- Empty state: pre-launch tenant, no traffic
- Failure state: webhook backlog > 60s
- Export: yes, CSV of last 24h failures
- Localization: LTR primary, RTL ready

**Output structure:**

```
ops/
  dashboard.blade.php          (Blade component, full surface)
  partials/
    bento-primary.blade.php    (settlement rate + sparkline)
    bento-secondary.blade.php  (3 secondary metrics)
    failure-table.blade.php    (wide data stream below bento)
    empty-state.blade.php
    error-state.blade.php
    skeleton.blade.php
  ops.css                      (state palette, density tier)
```

**The primary cell shows:**

- "98.4%" in 64px tabular numerals
- A 60-day sparkline below the number, in the same cell
- A pulsing live dot, top-right of the cell
- Label "Settlement success rate" in 13px proportional
- A delta pill "+0.2% vs. yesterday" in success-green, solid

**The failure table below:**

- 40px rows, compact density
- Filter chips above (`status: failed`, `last 1h`, `merchant: all`)
- Pinned first column: timestamp (monospace, tabular)
- Last column: action ("Investigate" link, keyboard-bound to Enter on row focus)
- Empty state: "No failures in this window. Last failure 4h ago."
- Error state: "Failure feed unreachable. Retrying in 5s. [Retry now]"

**What got blocked from the default output:**

- A bar chart of "total transactions per day" (operators do not care about volume, they care about failure rate — the discovery answer killed it)
- Three equal KPI cards above the bento (replaced with the asymmetric bento)
- A purple-to-blue gradient on the primary number (replaced with solid neutral text and a state-colored delta pill)
- Five live indicators (one on the primary, one in the table header for the live feed — capped at 2)

The output ships looking like a tool that an on-call engineer would build for themselves.

---

## Next steps

- Run [`/ux-motion`](How-to-add-motion-that-doesnt-break-Core-Web-Vitals) to add restrained motion to the live indicators and the bento entry animation
- Run [`/ux-polish`](How-to-detect-AI-slop-in-your-design) to catch any anti-patterns that slipped through
- Read [How to make AI output look human-grade](How-to-make-AI-output-look-human-grade) for the full pipeline
- For a case study writeup of the dashboard, see [How to ship a case study from product data](How-to-ship-a-case-study-from-product-data)

---

**Plugin repo:** https://github.com/Laith0003/ux-skill
**Author:** Laith Aljunaidy — https://www.linkedin.com/in/laith-aljunaidy/
**License:** MIT
