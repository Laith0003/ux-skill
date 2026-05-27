---
name: ux-recommend
description: The v2 flagship. Runs the 5-parallel-search Python engine across 11 data manifests (75+ styles, 170+ palettes, 65+ type pairs, 120+ components, 170+ industries, 110+ UX laws, 50+ motion presets, 30+ anti-patterns, 72 brand specs) and returns a complete recommended design system for your project — with always-on anti-slop guardrails.
allowed-tools: Bash, Read, Write
disable-model-invocation: false
---

# /ux-recommend — the flagship

**One command. Five parallel searches. One merged system out.**

Industry → Style → Palette → Type → Motion + Components + Brand Exemplars + Guardrails. The Python engine does the merging; you get a structured recommendation you can hand directly to `/ux-design` or `/ux-system`.

## When to use

- Starting a new project, surface, or marketing page from zero.
- Pivoting a tired-looking product to a deliberate aesthetic.
- Pre-flight before any `/ux-design` or `/ux-component` so the generation has explicit constraints, not implicit ones.

## When to skip

- You already ran `/ux-discover` and saved a brief — `/ux-recommend` is automatic in that flow.
- You're fixing one bug in existing code — use `/ux-fix` instead.
- You only need to lint, not recommend — use `/ux-lint`.

## How it works

1. The engine reads your brief (project type, industry, audience, tone, must-haves, forbidden, stack, region).
2. Lane 1 — `industries.json` lookup gives style/palette/type biases for your domain.
3. Lane 2 — `styles.json` filtered by industry + brief tags.
4. Lane 3 — `palettes.json` filtered by `style.compatible_palettes`.
5. Lane 4 — `type-pairs.json` filtered by `style.compatible_type_pairs`.
6. Lane 5 — `motion-presets.json` filtered by style hints.
7. Auxiliary lanes: components by style compatibility, brand exemplars by industry, anti-pattern guardrails (always on).
8. The engine returns one merged Recommendation with rationale lines.

## Usage

### One-shot (no discovery)

```bash
python3 -m engine.cli.main recommend \
  --project-type=landing \
  --industry=fintech-neobank \
  --tone=warm --tone=editorial \
  --must-have=dark-mode --must-have=a11y-AA \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

### From a saved discovery brief (the canonical flow)

```bash
python3 -m engine.cli.main discover           # 10 questions, mandatory
python3 -m engine.cli.main recommend --brief-file .ux/last-discovery.json
```

### Direct Python (in scripts or other commands)

```python
from engine.recommender import recommend, Brief

rec = recommend(Brief(
    project_type="dashboard",
    industry="saas-productivity",
    tone=["precise", "calm"],
    must_have=["dark-mode"],
    forbidden=["playful-gradient"],
    region="us"
))

print(rec.rationale)              # one-line rationale per lane
print(rec.style["id"])             # picked style
print(rec.palette["colors"])       # token map
print(len(rec.guardrails))         # 30+ anti-patterns always on
```

## Output shape

The recommendation is a JSON document with:

- `style` — one entry from `styles.json` (the picked design philosophy)
- `palette` — one entry from `palettes.json` (the picked color system)
- `type_pair` — one entry from `type-pairs.json` (display + body + mono)
- `motion` — top 5 motion presets compatible with the style
- `components` — top 12 components compatible with the style
- `brand_exemplars` — top 5 brands in the same industry to study
- `guardrails` — all 30+ anti-patterns (always-on)
- `rationale` — one line per lane explaining the pick

## Chaining

The recommendation lands at `.ux/last-recommendation.json` so it can chain into:

- `/ux-design [brief]` — generates frontend code using the recommended tokens
- `/ux-system` — generates a full design system from the recommendation
- `/ux-component <name>` — generates one component using the recommended style
- `/ux-lint` — verifies the generated code against the guardrails

## Error handling

- **No data manifests found** → engine returns an empty recommendation with a `rationale` of "data/*.json not yet generated; run `ux init` or reinstall the package."
- **Industry not found** → engine falls back to scoring all industries against the brief tags and picks the closest.
- **Style and palette incompatible** → engine picks the highest-scoring palette regardless; flags this in rationale.

## What this command is and isn't

- IS: A deterministic Python reasoning engine over structured data. Same input always returns the same output. No LLM in the recommender itself.
- IS NOT: A code generator. It tells you WHAT to use; `/ux-design` and friends are what USE it.
- IS NOT: A replacement for taste. The engine recommends; you decide. The brief's `forbidden` field is yours to wield.
