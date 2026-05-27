---
name: ux-discover
description: The mandatory 10-field intake before any generation. Asks project type, audience, primary goal, tone, must-haves, forbidden, reference brands, stack, region, and success metric. Saves answers to .ux/last-discovery.json so downstream commands chain.
allowed-tools: Bash, Read, Write
disable-model-invocation: false
---

# /ux-discover — the forcing function

**No generation without discovery.**

This is the discipline gate. The 10-field intake every project goes through before `/ux-design`, `/ux-component`, `/ux-recommend`, or any other generation command runs. The plugin asks; you answer; the engine has constraints to work with instead of guessing.

The 10 fields:

1. **Project type** — landing / marketing-site / dashboard / admin-panel / docs / mobile-app / email
2. **Audience** — who specifically. Concrete. "B2B finance ops in MENA", not "business users."
3. **Primary goal** — ONE job for this surface. Trial signup. Pricing comprehension. At-a-glance dashboard status.
4. **Tone** — 3-5 words. warm / editorial / precise / playful / clinical / confident / calm / bold / technical.
5. **Must-have** — hard constraints. dark-mode / RTL / AA accessibility / mobile-first / print-fidelity.
6. **Forbidden** — what NOT to do. "No purple-to-blue gradient. No three-card hero. No Inter as display."
7. **Reference brands** — 3-5 real brands whose design language fits. Pulled into the recommender as exemplars.
8. **Stack** — react / nextjs / vue / svelte / blade-alpine / astro / vanilla-html.
9. **Region / locale** — mena / us / eu / apac / global. Affects RTL, typography, color norms, copy style.
10. **Success metric** — how will you know it worked? Signup CR > 4%. TTI < 2s. Lighthouse > 95.

## When to use

- Starting a new project, surface, or marketing page from zero.
- Before any `/ux-design`, `/ux-component`, or `/ux-recommend`.
- When picking up a stalled project and you need to re-anchor on the brief.

## When to skip

- You're fixing a bug in existing code → use `/ux-fix`.
- You're auditing → use `/ux-audit` or `/ux-lint`.
- You already have a `.ux/last-discovery.json` for this project and the brief hasn't changed.

## How it runs

Inside Claude Code:

```bash
python3 -m engine.cli.main discover
```

The CLI walks the 10 questions interactively, then writes the answers to
`.ux/last-discovery.json`. Subsequent commands (`/ux-recommend`,
`/ux-design`, `/ux-component`) auto-load that file if present.

## Output

`.ux/last-discovery.json`:

```jsonc
{
  "answers": {
    "project_type": "landing",
    "audience": "B2C, mobile-first, MENA region",
    "primary_goal": "Trial signup",
    "tone": "warm, editorial, trustworthy",
    "must_have": "dark-mode, rtl-arabic, a11y-AA",
    "forbidden": "brutalism, purple-gradients, emoji-in-ui",
    "reference_brands": "Stripe, Linear, Mercury",
    "stack": "nextjs-15-app-router",
    "region": "mena",
    "success_metric": "Signup CR > 4%"
  },
  "complete": true,
  "missing": []
}
```

## Resume from a saved discovery

```bash
ux discover --load-state .ux/last-discovery.json   # answer the missing fields only
```

## Why this exists

Because the alternative — letting the LLM "infer reasonable defaults" — is exactly what produces AI slop. Default Inter font, default purple gradient, default three-card hero. The 10 questions remove the guesswork. The plugin can't improvise its way past a structured input.

## Chaining

After discovery completes, the natural next steps:

- `/ux-recommend` → uses your discovery to pick style + palette + type + motion + components.
- `/ux-design [extra brief]` → generates frontend code grounded in the recommendation.
- `/ux-component <name>` → generates one component aligned to the discovered constraints.
