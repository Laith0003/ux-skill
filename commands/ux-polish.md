---
description: Cosmetic pass on a surface. Spacing rhythm, hierarchy, AI-slop detection, token consistency. Triggers on "polish", "tighten this up", "remove the AI-slop", or "make it premium". Use when polishing an existing surface, tightening spacing / hierarchy, removing AI-slop tells, the user says "make this premium" or "tighten this up". Skip when the surface is missing core functionality (fix that first), the surface needs a redesign not a polish (use ux-design), backend or infrastructure.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(mkdir:*), Bash(date:*), Glob, Grep, Task, WebFetch
disable-model-invocation: false
---

# /ux-polish

You are running the `/ux-polish` command from the `ux` plugin. The job is a cosmetic pass — the surface mostly works but feels rough, generic, or unfinished. Tighten spacing, sharpen hierarchy, kill AI-slop tells, and align loose tokens.

## When to use

Triggers: "polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste", "the design feels cheap".

Use when the structure is right but the execution is loose. Not for fundamental problems (use `/ux-audit` or `/ux-design`). Not for copy issues (use `/ux-copy`). Not for motion (use `/ux-motion`). Not for accessibility (use `/ux-a11y`).

If a `/ux-critique` or `/ux-audit` has surfaced structural issues, run those first — polish on a broken structure is wasted work.

## Input

One of: a URL, an absolute file path containing the code, a screenshot, or a code snippet. Code is preferred for token consistency checks; a URL or screenshot is preferred for visual rhythm.

## Process

### 1. Run the AI-slop tell list

Scan the surface for these specific tells. Each found tell is a Critical or High finding depending on visibility.

#### Typography slop
- **Inter where wrong**: Inter is fine for utilitarian dashboards but feels generic on landing pages, marketing, brand surfaces. Look for Inter being used as the only typeface — that is the tell.
- **Generic sans pairing**: Inter + a "modern serif" with no character (Playfair, Lora, default Google Fonts serif). Editorial surfaces need stronger pairings.
- **System UI without intent**: defaulting to `-apple-system, BlinkMacSystemFont` when the surface needs voice.
- **Centered everything**: every heading, every paragraph, every CTA centered. Even when there is no reason.

#### Color slop
- **Purple-blue gradients**: the AI default. `#6366f1 → #8b5cf6` or any variant. The single strongest tell.
- **Pure black**: `#000` or `bg-black`. Should be Zinc-950, Charcoal, Off-Black.
- **Saturated accent colors**: anything over 80% saturation reads as generic.
- **Multiple chromatic accents**: a brand uses one accent. Two is loud. Three is a tell.
- **Tailwind defaults uncustomized**: `bg-blue-500`, `text-gray-500` everywhere. Even the colors are confessing.

#### Layout slop
- **3-equal-card row**: three identical cards in a grid. Lazy. Replace with 2-col zig-zag, asymmetric, horizontal scroll, or bento.
- **Centered hero**: title centered, subhead centered, CTA centered. When `DESIGN_VARIANCE > 4` this is a fail.
- **Equal-spaced everything**: 24px between every section. Real surfaces have rhythm — sections of different weight breathe differently.
- **Full-width containers**: every section spans the viewport, edge-to-edge. Real layouts have intentional asymmetry — some sections inset, some bleed.
- **No imagery**: walls of text and CTAs, no photography, no illustration, no diagrams. Text-only is a slop tell.

#### Content slop
- **"Acme," "Nexus," "Lumen"**: AI-default brand placeholders. Replace with real names or evocative ones tied to the brief.
- **"John Doe," "Jane Smith"**: AI-default people placeholders. Use real names or names that fit the audience.
- **Stock filler copy**: "Welcome to our amazing platform that helps you achieve your goals." Lorem with thesaurus.
- **Filler words**: "leverage," "empower," "seamless," "robust," "unlock," "delight," "elevate." Voice slop.
- **Generic icons**: Heroicons or Lucide used without intent — every section has an icon, every icon is the same weight. Real surfaces use icons sparingly and deliberately.
- **Random/generic stock**: the first `images.unsplash.com/photo-...` hit pasted in without choosing it, or a random/unseeded placeholder service. Replace with client assets, or curated Unsplash/Pexels chosen to match the brand + 7-axis temperature and treated so it reads as deliberate. An abstract SVG is not a substitute for a real product/site image.

#### Interaction slop
- **Missing states**: only happy-path UI. No hover, no focus, no disabled, no loading, no empty, no error.
- **Default browser focus rings**: blue outline on Chrome's defaults. Real surfaces design focus.
- **Hover with no consequence**: `hover:opacity-90` and nothing else. Hover should signal affordance.

### 2. Check spacing rhythm

- All gaps should be multiples of 4 (or 8). Stray 5px, 13px, 22px gaps are findings.
- Vertical rhythm should match the type scale — line height should resolve to the baseline grid.
- White space should be intentional, not residual — large gaps should be larger, small gaps tighter. If every gap is 24px, there is no rhythm.
- Density should vary by section — hero loose, dense info-grid tight. Uniform density is a tell.

### 3. Check hierarchy

- Three weight levels at most per surface (display, body, secondary). More than three reads as visual noise.
- The eye should know where to land. If you blur your vision, the primary CTA / primary headline / primary visual should still hold.
- Hierarchy should compound — size + weight + color + position together. Relying on size alone is weak.
- Each section should have a single hero — one element that owns the section. Two competing heroes is a finding.

### 4. Check token consistency

If working from code:

- Spot color values that bypass tokens (`#1a1a1a` instead of `var(--color-fg-primary)`).
- Spot spacing values that bypass tokens (`margin: 13px` instead of `var(--space-3)`).
- Spot type sizes that bypass the scale (`font-size: 17px` when the scale has 16/18/20).
- Spot duplicate definitions (same color defined twice under different names).

### 5. Score and format the output

Each finding gets a severity:

- **Critical** — visible at a glance and embarrassing (purple gradient, "Acme," 3 equal cards).
- **High** — noticeable on inspection (Inter on a brand surface, missing states, weak hierarchy).
- **Medium** — visible to a discerning reviewer (loose spacing rhythm, token drift).
- **Cosmetic** — polish-on-polish (5px off the grid in one place).

Format:

```
─── polish pass ───
Surface:        <URL / path / description>
Tells found:    <total count>
Severity:       Critical <n> | High <n> | Medium <n> | Cosmetic <n>

─── AI-slop tells ───
[<severity>] <tell>
  Evidence:  <where it shows up — line number, selector, or screenshot region>
  Fix:       <specific replacement>

─── spacing rhythm ───
[<severity>] <issue>
  Evidence:  <>
  Fix:       <>

─── hierarchy ───
[<severity>] <issue>
  Evidence:  <>
  Fix:       <>

─── tokens ───
[<severity>] <issue>
  Evidence:  <>
  Fix:       <>

─── prioritized fix list ───
1. <Critical fix 1 — short>
2. <Critical fix 2>
3. <High fix 1>
...
```

### 6. Persist state

Write `.ux/last-polish.json`:

```json
{
  "command": "ux-polish",
  "timestamp": "<ISO8601>",
  "surface": "<URL / path / description>",
  "findings": [
    {
      "category": "slop | spacing | hierarchy | tokens",
      "severity": "Critical | High | Medium | Cosmetic",
      "title": "<short>",
      "evidence": "<line / selector / region>",
      "fix": "<specific replacement>",
      "auto_fixable": true | false
    }
  ],
  "severity_counts": { "critical": <n>, "high": <n>, "medium": <n>, "cosmetic": <n> },
  "prioritized_fix_list": ["<fix 1>", "<fix 2>", "..."]
}
```

The `auto_fixable` flag marks findings safe for `/ux-polish --fix` to apply without confirmation (token swaps, color literal replacements, simple class swaps). Findings requiring judgment (replacing 3-card row with zig-zag layout) are NOT auto-fixable.

### 7. Optional fix flag

If the user passed `--fix`:

1. Validate clean working tree.
2. Apply auto-fixable findings directly via Edit. Commit atomically.
3. For non-auto-fixable findings, dispatch the `frontend-engineer` sub-agent via the Task tool with the full polish report and the prioritized fix list.
4. After fixes, re-run the polish pass on the new state and report deltas.

If the surface is too far gone for polish (Critical count > 5 or "purple gradient as hero" found), do NOT enter fix mode — recommend `/ux-design` instead.

## Output

The polish report and (if `--fix`) the fix-loop results.

## State persisted

- `.ux/last-polish.json` — keys: `command`, `timestamp`, `surface`, `findings` (array of `{category, severity, title, evidence, fix, auto_fixable}`), `severity_counts`, `prioritized_fix_list`.

## Next prompt

```
─── next ───
Recommended: /ux-polish --fix    (apply the fixes)
Other moves: /ux-design          (surface too far gone for polish — needs redesign)
             /ux-audit            (broader structural review)
             /ux-motion           (motion-specific polish)
             /ux-next             (let me decide)
```

If Critical count > 5 OR a purple-blue gradient is found as the primary visual, change Recommended to `/ux-design` — polish cannot save a surface that is fundamentally slop.

## Hard rules

- Never auto-fix a layout change (3-card row → zig-zag) without confirmation. Layout decisions need a human signoff.
- Never approve a surface with a purple-blue gradient as the primary visual. That is the strongest AI-slop tell.
- Never approve a centered hero when `DESIGN_VARIANCE > 4`. Force asymmetry.
- Never replace one Inter with another generic sans. If Inter is wrong, the answer is a typeface with character, not "Inter but different."
- Never accept random/generic stock or a random/unseeded placeholder service (the linter flags these). Curated Unsplash/Pexels chosen to match the brand + temperature is acceptable; the first unchosen hit, or a rotating placeholder, is the tell. An abstract SVG is not a substitute for a real product/site image.
- Never approve a surface with no interaction states. Hover, focus, disabled, loading, empty, error — at minimum.
- If `.ux/brand.json` exists, also judge BRAND FIDELITY: run `evaluate(html, brand_profile=...)` (or read it from a prior `uxskill evolve --brand-file` run) for `brand_fidelity` + `imagery` + `brand_passed`. Treat off-brand drift — wrong or absent brand primary, missing logo, house-style colors (clay `#cc785c` / blurple `#5e6ad2`), or a text-wall with no real imagery — as a **Critical** slop tell: a surface that ignores the client's brand fails no matter how polished. See `references/process/brand-extraction.md`.

## Failure modes

- **Polish on broken structure**: spending an hour tightening spacing when the surface needs a redesign. Run `/ux-critique` first if you are unsure.
- **Tell-list creep**: marking every Tailwind utility as slop. Tailwind itself is not the tell — uncustomized Tailwind defaults are.
- **Token zealotry**: flagging every hex literal even when the project does not have a token system. Match the project's existing pattern.
- **Hidden bias against Inter**: Inter is fine on dashboards and utilitarian surfaces. The tell is "Inter on every kind of surface because it is the AI default," not "Inter ever."
- **Auto-fix overreach**: applying a layout change without the user agreeing it is the right move. Auto-fix is for the unambiguous swaps; layout decisions go through the sub-agent with the user in the loop.

## Error Handling

| Error condition | Recovery |
|---|---|
| Code style unclear (formatter, class convention, file structure) | Ask for stack and formatting preferences before applying any auto-fix |
| Project has no design token system | Propose ones from references/foundations/color.md + typography.md as a starter; do not invent literals beyond what the file currently uses |
| Surface is too far gone for polish (Critical > 5 or purple-blue gradient as hero) | Refuse `--fix`; recommend `/ux-design` instead |
| Auto-fixable flag conflicts with project convention | Show the diff before applying; require user confirmation |
| Screenshot-only mode for token consistency check | Limit findings to visible rhythm/hierarchy/slop; mark token check as `not_verifiable` |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

---

## v2 Python integration — required preamble

Before producing any judgment, the LLM running this command MUST shell to the v2 Python engine to ground its work in deterministic rules. The mechanical pass runs first; the taste pass runs second.

### Step 1 — Run the deterministic linter

```bash
python3 -m engine.cli.main --no-pretty lint <user-supplied-path> --threshold high > /tmp/ux-lint-report.json 2>/dev/null \
  || bash bin/ux-lint.sh <user-supplied-path>
```

The Python linter reads rules from `data/anti-patterns.json` (35 regex rules across 8 categories). It returns structured JSON with findings keyed by file:line:column.

### Step 2 — Inspect findings

```bash
cat /tmp/ux-lint-report.json | python3 -c "
import json, sys
r = json.load(sys.stdin)
s = r['summary']
print(f\"scanned: {r['files_scanned']} files, {r['rules_loaded']} rules\")
print(f\"  critical: {s.get('critical', 0)}\")
print(f\"  high:     {s.get('high', 0)}\")
print(f\"  medium:   {s.get('medium', 0)}\")
print(f\"  low:      {s.get('low', 0)}\")
print(f\"  total:    {s.get('total', 0)}\")
for f in r['findings'][:20]:
    print(f\"  [{f['severity']}] {f['file']}:{f['line']} {f['rule_name']} ({f['rule_id']})\")
"
```

### Step 3 — Command-specific Python action

Run the linter first to get the mechanical floor. Then read `data/styles.json` and `data/motion-presets.json` to know what taste-level polish is available beyond what regex catches:

```bash
python3 -c "
import json
styles = json.load(open('data/styles.json'))['entries']
motion = json.load(open('data/motion-presets.json'))['entries']
print(f'Styles available: {len(styles)}')
print(f'Motion presets:   {len(motion)}')
print('Top 3 entry motions (use these for first-impression polish):')
for m in motion[:3]:
    if m.get('category') == 'Entry':
        print(f\"  - {m['id']}: {m.get('name')}\")
"
```

Polish = applying named motion presets and named style tokens. NOT freelancing.

### Step 4 — Hand back to the LLM

Take the structured findings from Step 1 and any data the engine returned in Step 3, and use those AS YOUR INPUT to the LLM-side reasoning. Do NOT re-derive what the linter already proved — the regex pass is the truth on those rules. Your job is the taste-level judgment the linter cannot make.

### Fallback

If `python3 -m engine.cli.main` is not on PATH, fall back to `bash bin/ux-lint.sh` for the linter pass and v1 prose-only behavior for everything else.
