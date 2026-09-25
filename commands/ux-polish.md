---
description: Polish a surface. Loops lint, fix, re-lint until the score reaches 90 or three rounds pass, then a taste pass on spacing, hierarchy, tokens and AI-slop tells. --fix applies the taste findings.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(mkdir:*), Bash(date:*), Bash(git status:*), Bash(uxskill:*), Bash(python3:*), Glob, Grep, Task, WebFetch
disable-model-invocation: false
---

# /ux-polish

**An existing design system is fixed input.** Before any engine pick, run `python3 -m engine.cli.main --no-pretty system detect --root .` (over MCP, `ux_system_detect`). When `found` is true, follow `commands/ux-design.md` step 1a: the project's tokens win, the engine's palette and type picks are suggestions for gaps only, and nothing edits, overwrites or re-derives the system's files.

You are running the `/ux-polish` command from the `ux` plugin. The job is a cosmetic pass: the surface mostly works but feels rough, generic, or unfinished. First the deterministic loop (lint, fix, re-lint) raises the score; then the taste pass tightens spacing, sharpens hierarchy, kills AI-slop tells, and aligns loose tokens.

`/ux-polish` absorbs what used to be `/ux-evolve`; that name still works as an alias until 4.1.

## Modes and flags

| Mode | Flag | What it does |
|---|---|---|
| loop + taste (default) | none | Step 0 loop on a local HTML file, then steps 1 to 6 on `<artifact>.evolved.html`. The original file is never touched |
| loop only | `--loop-only` | Step 0 alone, then the loop report. No taste pass. Replaces the original after the clean-tree check (the old `/ux-evolve`) |
| taste only | `--no-loop` | Steps 1 to 6 alone. Used automatically when the input is a URL, a screenshot, or a snippet, because the loop needs a file |
| fix | `--fix` | Replaces the original with the loop output after the clean-tree check, then applies the taste findings (step 7) |

| Flag | Meaning |
|---|---|
| `--rounds <n>` | Loop cap. Default 3. `--max-rounds <n>` means the same. The old `/ux-evolve` cap was 5; pass `--rounds 5` for it |
| `--css <path>` | CSS file that belongs to the HTML under polish |
| `--force` | Ship the loop output even when the final score is below the 65 quality gate |
| `--brand-file <path>` | Client brand (`.ux/brand.json`). Turns on the brand-fidelity hard floor in the loop and in the taste pass. Used automatically when `.ux/brand.json` exists |
| `--no-log` | Do not append the loop result to `.ux/decisions.jsonl` |

When the same flag appears twice, the last value wins.

## When to use

Triggers: "polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste", "the design feels cheap", "evolve this surface", "improve until score 90+", "auto-fix this file", "run the loop on", "make it ship-ready".

Use when the structure is right but the execution is loose. Not for fundamental problems (use `/ux-audit` or `/ux-design`). Not for copy issues (use `/ux-copy`). Not for motion (use `/ux-motion`). Not for accessibility (use `/ux-a11y`).

If a `/ux-critique` or `/ux-audit` has surfaced structural issues, run those first — polish on a broken structure is wasted work.

Skip the loop when the artifact is already at 90+ (run `uxskill lint <file> --score-only` to confirm) or when the user wants a single targeted fix (`/ux-fix`). With no artifact yet, generate one with `/ux-design` or `/ux-system` first.

## Input

One of: a URL, an absolute file path containing the code, a screenshot, or a code snippet. Code is preferred for token consistency checks; a URL or screenshot is preferred for visual rhythm. The loop in step 0 runs only on a local HTML file (plus optional CSS).

## Process

### 0. The loop: lint, fix, re-lint

**Offline, deterministic, no LLM calls inside the loop.** Skip this step with `--no-loop`, or when the input is not a local HTML file.

#### Resolve the target

Take it from `$ARGUMENTS`, or ask once: "Path to the artifact (HTML + optional CSS)?" If the user says "the last one", search in this order:
1. `.ux/last-design.html` + `.ux/last-design.css`
2. The most recent file under `out/` matching `*.html`
3. Fall back to asking explicitly.

#### Run it

```bash
uxskill evolve <html_path> [--css <css_path>] [--force] --max-rounds <rounds, default 3> [--brand-file .ux/brand.json] [--no-log]
```

Each round:

1. Run the linter to get the 0-100 quality score
2. Run the evaluator to score the 7 axes (hierarchy / coherence / spacing / readability / tone / uniqueness + linter)
3. Apply the 6 deterministic polish passes
4. Re-evaluate
5. Decide: `target_hit` (score reaches 90), `plateau` (delta < 5 between rounds), `max_rounds` (the `--rounds` cap, default 3), or continue

The 6 polish passes are all idempotent: running them twice produces no further change. Strip inline styles, replace generic CTAs, swap placeholder URLs for data URIs, normalize spacing to the 8pt-ish scale, strip Lorem ipsum, normalize `font-weight: bold` to `700`.

This writes:
- `<artifact>.evolved.html` and `<artifact>.evolved.css` (the refined output)
- `.ux/last-evolve.json` (the full EvolveResult with rounds + scores)
- One line to `.ux/decisions.jsonl` (the learning signal; schema `_v: 1`), unless `--no-log`

It reads the target artifact paths, `data/anti-patterns.json` (for lint scoring), and `data/brands/_index.json` plus `data/brands/*.json` (for uniqueness comparison).

**If the surface is a brand redesign, pass `--brand-file .ux/brand.json`.** The brand-fidelity HARD FLOOR then applies at every exit: an off-brand page (dropped the brand primary/logo, or shipped no real imagery) reports `above_gate=false` + `stopped_reason=gate_failed` no matter how high the composite score, and `uxskill evolve` exits `1`. Polishing cannot fix brand drift: fix the source (use the brand color, carry the logo, add real imagery) and regenerate.

#### Quality gate

If the final score is < 65, the loop refuses to commit by default and returns `stopped_reason: "gate_failed"`. The user can override with `--force` to ship anyway.

Who may touch the original file:

- **Default (no `--loop-only`, no `--fix`):** never. The loop output stays at `<artifact>.evolved.html` (and `.evolved.css`) and the original is left as it was, whatever the score. The taste pass reads `<artifact>.evolved.html` when the loop cleared the gate or `--force` was passed.
- **`--loop-only` or `--fix`:** first validate a clean working tree (the same check as step 7: `git status --porcelain <file>` must print nothing for the original and its CSS). If the file has uncommitted changes, stop, say so, and leave the evolved file next to it. Then, above 65 OR forced: replace the original `<file>.html` (and its CSS) with the evolved version; the user can diff it in version control. Below 65 and not forced: do NOT replace the original.

On `gate_failed` without `--force`, the evolved file is still written but never promoted. The taste pass then reads the original `<file>.html`, not the evolved one, because the loop output did not clear the gate; say so in the report. The recommended next move on a gate failure is to regenerate the artifact via `/ux-design` with different axis hints (for example, add `forbidden: [low-contrast]` if the linter is flagging contrast issues).

#### Loop report

Print:
- Initial score to final score (for example `72 → 91`)
- Number of rounds (for example `3 rounds`)
- Stop reason (`target_hit` / `plateau` / `max_rounds` / `gate_failed`)
- The polish passes applied per round (for example `round 1: strip_inline_styles, replace_generic_ctas; round 2: normalize_spacing`)
- Where the evolved output landed, and whether the original was replaced (only under `--loop-only` or `--fix`)
- If gate_failed and not forced: the regenerate axis hints

End the loop report with:
```
EVOLVE COMPLETE: <initial> → <final> ({stop_reason}, {n} rounds)
artifact:      <path>
evaluation:    .ux/last-evolve.json
ledger entry:  .ux/decisions.jsonl (+1)
```

With `--loop-only`, stop here.

#### What the loop cannot fix

Things outside its remit (rerun `/ux-design` or `/ux-system`):
- Wrong information architecture (sections in wrong order)
- Missing content (no real copy, no real imagery)
- Stack mismatch (user wants Next.js, you generated Blade)
- Brand axis target wildly off (tone_match < 30 means the axes are wrong, not the polish)

Flag these in the report instead of pushing them through more rounds. Do not add LLM-driven cosmetic passes inside the loop; it is meant to be fast and predictable. The taste pass below is where judgment happens. It reads `<artifact>.evolved.html`, or, after the original was replaced, the original path; on `gate_failed` without `--force` it reads the original file.

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
- **Centered hero**: title centered, subhead centered, CTA centered. When `DESIGN_VARIANCE > 4` this is a fail, unless the page uses the Thesis statement or Cinematic brand archetype by deliberate choice (the centered-hero rule in `references/surfaces/landing.md`).
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

1. Validate clean working tree. With the loop run, this is the check step 0 already did before replacing the original.
2. Apply auto-fixable findings directly via Edit. Commit atomically.
3. For non-auto-fixable findings, dispatch the `frontend-engineer` sub-agent via the Task tool with the full polish report and the prioritized fix list.
4. After fixes, re-run the polish pass on the new state and report deltas.

If the surface is too far gone for polish (Critical count > 5 or "purple gradient as hero" found), do NOT enter fix mode — recommend `/ux-design` instead.

## Output

The loop report (step 0, when it ran), the polish report, and (if `--fix`) the fix-loop results.

## State persisted

- `.ux/last-evolve.json`: the full loop result, when step 0 ran.
- `.ux/decisions.jsonl`: one appended line per loop run, unless `--no-log`.
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
- Never approve a centered hero when `DESIGN_VARIANCE > 4`, unless the page uses the Thesis statement or Cinematic brand archetype by deliberate choice (`references/surfaces/landing.md`). Otherwise force asymmetry.
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
