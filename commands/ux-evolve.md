---
description: Auto-iterate the lint→polish→re-lint loop on a generated artifact until score crosses 90 or plateaus. Triggers on "polish this", "evolve this surface", "improve until score 90+", "auto-fix", "run the loop". Use when the user has a freshly generated surface that needs automatic refinement to ship-ready quality. Skip when the artifact is already at 90+ score (just `/ux-lint --score-only` to confirm) or when the user wants a single targeted fix (`/ux-fix` instead).
allowed-tools: Read, Write, Edit, Bash(uxskill:*), Bash(python3:*), Bash(ls:*), Bash(cat:*)
disable-model-invocation: false
---

# /ux-evolve

You are running the `/ux-evolve` command. Your job is to auto-iterate the polish loop on a target artifact until the evaluation score crosses 90, plateaus, or hits the 5-round safety cap. **Offline, deterministic, no LLM calls inside the loop.**

## When to use

Triggers: "polish this", "evolve this surface", "improve until score 90+", "auto-fix this file", "run the loop on …", "make it ship-ready", "ten/ten this".

Skip when:
- The artifact is already at 90+ (run `uxskill lint <file> --score-only` first to confirm).
- The user wants a single targeted fix (`/ux-fix` instead).
- There's no artifact yet (use `/ux-design` or `/ux-system` first to generate one).

## Behaviour

The loop is a single Python call. Each round:

1. Run the linter to get the 0-100 quality score
2. Run the evaluator to score the 7 axes (hierarchy / coherence / spacing / readability / tone / uniqueness + linter)
3. Apply the 6 deterministic polish passes
4. Re-evaluate
5. Decide: target_hit (>=90), plateau (delta < 5), max_rounds (5), or continue

The 6 polish passes are all idempotent — running them twice produces no further change. Strip inline styles, replace generic CTAs, swap placeholder URLs for data URIs, normalize spacing to the 8pt-ish scale, strip Lorem ipsum, normalize `font-weight: bold` → `700`.

## Quality gate

If the final score is < 65, the loop refuses to commit by default and returns `stopped_reason: "gate_failed"`. The user can override with `--force` to ship anyway. The recommended next move on a gate failure is to regenerate the artifact via `/ux-design` with different axis hints (e.g., add `forbidden: [low-contrast]` if the linter is flagging contrast issues).

## Process

### 1. Resolve target

Ask once (or take from `$ARGUMENTS`): "Path to the artifact (HTML + optional CSS)?"

Default search order if user says "the last one":
1. `.ux/last-design.html` + `.ux/last-design.css`
2. The most recent file under `out/` matching `*.html`
3. Fall back to asking explicitly.

### 2. Run the loop

```bash
uxskill evolve <html_path> [--css <css_path>] [--force] [--max-rounds 5] [--brand-file .ux/brand.json]
```

This writes:
- `<artifact>.evolved.html` and `<artifact>.evolved.css` (the refined output)
- `.ux/last-evolve.json` (the full EvolveResult with rounds + scores)
- One line to `.ux/decisions.jsonl` (the learning signal)

**If the surface is a brand redesign, pass `--brand-file .ux/brand.json`.** The brand-fidelity HARD FLOOR then applies at every exit: an off-brand page (dropped the brand primary/logo, or shipped no real imagery) reports `above_gate=false` + `stopped_reason=gate_failed` no matter how high the composite score, and `uxskill evolve` exits `1`. Polishing cannot fix brand drift — fix the source (use the brand color, carry the logo, add real imagery) and regenerate.

### 3. Report

Print:
- Initial score → final score (e.g., `72 → 91`)
- Number of rounds (e.g., `3 rounds`)
- Stop reason (`target_hit` / `plateau` / `max_rounds` / `gate_failed`)
- The polish passes applied per round (e.g., `round 1: strip_inline_styles, replace_generic_ctas; round 2: normalize_spacing`)
- Where the evolved output landed
- If gate_failed and not forced: suggest the regenerate axis hints

Below 65 + not forced: do NOT replace the original file. Above 65 OR forced: replace the original `<file>.html` with the evolved version (the user can `git diff` to inspect).

## Output contract

The command must end with:
```
EVOLVE COMPLETE: <initial> → <final> ({stop_reason}, {n} rounds)
artifact:      <path>
evaluation:    .ux/last-evolve.json
ledger entry:  .ux/decisions.jsonl (+1)
```

## What the loop CANNOT fix

Things outside its remit (user should rerun /ux-design or /ux-system):
- Wrong information architecture (sections in wrong order)
- Missing content (no real copy, no real imagery)
- Stack mismatch (user wants Next.js, you generated Blade)
- Brand axis target wildly off (tone_match < 30 → axes are wrong, not polish)

Flag these in the report instead of pushing them through more polish rounds.

## Anti-slop discipline

The polish passes already encode anti-slop discipline. Do NOT add LLM-driven cosmetic passes on top — the loop is meant to be fast and predictable. If the user needs LLM-driven polish, that's `/ux-polish`, a separate command.

## State

Writes to:
- `.ux/last-evolve.json` (full EvolveResult)
- `.ux/decisions.jsonl` (one append, schema `_v: 1`)

Reads from:
- The target artifact paths
- `data/anti-patterns.json` (for lint scoring)
- `data/brands/_index.json` and `data/brands/*.json` (for uniqueness comparison)
