---
name: ux-discover
description: Intake before any build. Runs the 10-field discovery, then the recommender. --frame writes the four-field framing block; --recommend runs the recommender alone.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
disable-model-invocation: false
---

# /ux-discover: the forcing function

**No generation without discovery.**

This is the discipline gate. The intake every project goes through before `/ux-design`, `/ux-system`, or any other generation command runs. The plugin asks; you answer; the engine has constraints to work with instead of guessing.

`/ux-discover` has three modes. It absorbs what used to be `/ux-frame` and `/ux-recommend`; those names still work as aliases until 4.1.

| Mode | Flag | What it does | Writes |
|---|---|---|---|
| discovery (default) | none | 10-field intake, then the recommender | `.ux/last-discovery.json`, `.ux/last-recommendation.json` |
| frame | `--frame` | Lean four-field framing block: audience, outcome, hypothesis, success signal | `.ux/last-frame.json` (and `.ux/last-discovery.json` when the 10 fields are also filled) |
| recommend | `--recommend` | The 5-parallel-search recommender only, from a saved brief or from one-shot flags | `.ux/last-recommendation.json` |

Pick the mode from the flag. With no flag, pick from the words: "frame this", "what's the brief", "scope this" mean frame mode; "recommend a system", "what should I use", "pick a palette" mean recommend mode; everything else is discovery.

## Flags

| Flag | Mode | Meaning |
|---|---|---|
| `--frame` | frame | Run the four-field framing block instead of the 10-field intake |
| `--recommend` | recommend | Run only the recommender |
| `--no-recommend` | discovery | Stop after the intake; do not run the recommender |
| `--load-state <file>` | discovery | Resume from a saved discovery JSON and ask only the missing fields |
| `--save <path>` | discovery | Where to write the answers (default `.ux/last-discovery.json`) |
| `--brief-file <file>` | recommend | Brief to recommend from (default `.ux/last-discovery.json`) |
| `--brand-file <file>` | discovery, recommend | Anchor palette and type to an extracted client brand (`.ux/brand.json`) |
| `--project-type`, `--industry`, `--tone`, `--must-have`, `--forbidden`, `--stack`, `--region` | recommend | One-shot brief fields when there is no saved brief. `--tone`, `--must-have` and `--forbidden` repeat |
| `--persist` | discovery, recommend | Write `.ux/design-system/MASTER.md` after the recommendation without asking first |

## When to use

- Starting a new project, surface, or marketing page from zero.
- Before any `/ux-design` or `/ux-system`.
- When picking up a stalled project and you need to re-anchor on the brief.
- Mid-stream, when a conversation has drifted and nobody can answer "who is this for and what changes when we ship?" (frame mode).
- Pivoting a tired-looking product to a deliberate aesthetic (recommend mode).

## When to skip

- You're fixing a bug in existing code: use `/ux-fix`.
- You're auditing: use `/ux-audit` or `/ux-lint`.
- You already have a `.ux/last-discovery.json` for this project and the brief hasn't changed. Run `--recommend` alone if you only need a fresh recommendation.
- Frame mode: skip when `.ux/last-frame.json` already frames the project, or the brief is a one-off component build with no framing implications.

---

## Discovery mode (default)

The 10 fields:

1. **Project type**: landing / marketing-site / dashboard / admin-panel / docs / mobile-app / email
2. **Audience**: who specifically. Concrete. "B2B finance ops in MENA", not "business users."
3. **Primary goal**: ONE job for this surface. Trial signup. Pricing comprehension. At-a-glance dashboard status.
4. **Tone**: 3-5 words. warm / editorial / precise / playful / clinical / confident / calm / bold / technical.
5. **Must-have**: hard constraints. dark-mode / RTL / AA accessibility / mobile-first / print-fidelity.
6. **Forbidden**: what NOT to do. "No purple-to-blue gradient. No three-card hero. No Inter as display."
7. **Reference brands**: 3-5 real brands whose design language fits. Pulled into the recommender as exemplars.
8. **Stack**: react / nextjs / vue / svelte / blade-alpine / astro / vanilla-html.
9. **Region / locale**: mena / us / eu / apac / global. Affects RTL, typography, color norms, copy style.
10. **Success metric**: how will you know it worked? Signup CR > 4%. TTI < 2s. Lighthouse > 95.

### How it runs

```bash
python3 -m engine.cli.main discover
```

The CLI walks the 10 questions interactively, then writes the answers to
`.ux/last-discovery.json` (or the `--save` path). Subsequent commands
(`/ux-design` in every mode, `/ux-system`) auto-load that file if present.

For non-interactive use, hand-edit `.ux/last-discovery.json`:

```bash
mkdir -p .ux
cat > .ux/last-discovery.json <<'JSON'
{
  "answers": {
    "project_type": "...",
    "audience": "...",
    "primary_goal": "...",
    "tone": "...",
    "must_have": "...",
    "forbidden": "...",
    "reference_brands": "...",
    "stack": "...",
    "region": "...",
    "success_metric": "..."
  }
}
JSON
```

### Output

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

### Resume from a saved discovery

```bash
ux discover --load-state .ux/last-discovery.json   # answer the missing fields only
```

### Then recommend

Unless `--no-recommend` was passed, finish discovery by running the recommender exactly as recommend mode does below, so `/ux-design` finds `.ux/last-recommendation.json` waiting.

### Why this exists

Because the alternative, letting the LLM "infer reasonable defaults", is exactly what produces AI slop. Default Inter font, default purple gradient, default three-card hero. The 10 questions remove the guesswork. The plugin can't improvise its way past a structured input.

---

## Frame mode (`--frame`)

The job is a tight, structured framing block that every downstream command can read. No design work happens here. No critique. Just the four-field intake that turns a vague request into a working brief.

Triggers: "frame this", "what's the brief", "set up the project", "framing", "what are we actually building", "frame the work", "scope this".

### Input

Anything the user has: a Slack paste, a Figma URL, a one-line idea, a ticket, a meeting transcript, or nothing. If the input already contains the four framing fields, extract them. Do not re-ask.

### 1. Extract or ask, never both

Read what the user provided. If you can confidently pull `audience`, `outcome`, `hypothesis`, and `success_signal` out of the input, skip ahead to step 3.

If any field is missing, ask ONCE with a single combined question that surfaces all gaps. Example:

> "Quick framing: who specifically is this for (not 'users'), what changes for them when we ship, what's your bet on why this will work, and how will we know it worked? One paragraph is fine."

Do not ask the four questions in four separate messages. That is the failure mode this mode exists to prevent.

### 2. Sharpen the answers

Apply these tests before accepting any field:

- **Audience**: must name a real person/role/segment. Reject "everyone," "users," "people," "customers" without further qualifier. Push back specifically: "Which customers? Returning ones? First-time? A specific tier?"
- **Outcome**: must describe a behavior or state change for the audience, not a feature. Reject "make it better," "improve UX," "modernize." Push back: "What does the audience do differently after we ship that they don't do today?"
- **Hypothesis**: must include a causal "because" or "if-then." Reject "we think it'll be good." Push back: "What's the bet? If we change X, then Y will happen because Z."
- **Success signal**: must name a measurable thing or an observable behavior. Reject "users will love it." Push back: "What metric, behavior, or signal would prove this worked? How would you know in two weeks?"

If the user resists sharpening twice, accept their best answer and flag the soft field in the output.

### 3. Write the framing block

Format the output exactly like this:

```
─── framing ───
Audience:         <specific role/segment with qualifiers>
Outcome:          <behavior change the audience makes>
Hypothesis:       <if-then with causal reasoning>
Success signal:   <measurable metric or observable behavior>

Soft fields:      <list any fields flagged as not-sharp-enough, or "none">
```

Keep each field to one tight sentence. Two if needed. Never more.

### 4. Persist state

Write to `.ux/last-frame.json` in the project root. Create the `.ux/` directory if it does not exist.

```json
{
  "command": "ux-frame",
  "timestamp": "<ISO8601>",
  "audience": "<verbatim from output>",
  "outcome": "<verbatim from output>",
  "hypothesis": "<verbatim from output>",
  "success_signal": "<verbatim from output>",
  "soft_fields": ["<list of any field names that were accepted soft>"]
}
```

The `command` value stays `ux-frame` so older readers of the file keep working. Every downstream command reads this file to anchor its work.

### 5. Chain into discovery and recommendation

The frame covers four of the ten discovery fields. When the user wants to build next, run the 10-field discovery (`python3 -m engine.cli.main discover --save=.ux/last-discovery.json`, filling audience and success metric from the frame), then the recommender:

```bash
python3 -m engine.cli.main --no-pretty recommend --brief-file=.ux/last-discovery.json > .ux/last-recommendation.json
```

The recommendation is what `/ux-design` and `/ux-system` read next.

### Output

The framing block from step 3, followed by the next-prompt block. Nothing else. No commentary, no congratulations, no "here is your framing." Just the block and the next move.

### Next prompt (frame mode)

Surface the next move based on what the framing reveals:

- If the surface already exists and the user wants a review: `/ux-audit`
- If the surface needs to be built fresh: `/ux-design`
- If the audience is shaky and needs more grounding: `/ux-research`
- If the user is unsure: `/ux-next` (let the conductor pick)

```
─── next ───
Recommended: <primary next command based on framing>
Other moves: <2-3 alternatives>
             /ux-next   (let me decide)
```

### Frame mode hard rules

- Never accept "everyone," "users," or "people" as audience without a qualifying segment. Push back specifically.
- Never accept "make it better," "improve UX," or "modernize" as outcome. Force a behavior-change statement.
- Never ask the four questions as four messages. One combined ask, or none if you can extract from input.
- Never write design or critique in this mode. Framing only.
- Never skip writing `.ux/last-frame.json`. Downstream commands depend on it.
- Never add emojis, decorative dividers beyond the `───` rule, or filler sentences.

### Frame mode failure modes

- **Question avalanche**: asking four separate questions instead of one combined ask. The user disengages.
- **Soft acceptance**: accepting "users" as audience because the user pushed back. Flag it as a soft field instead; be transparent that the framing is weaker than it should be.
- **Scope creep**: starting to design or critique mid-frame. Stop. Frame only. Hand off to `/ux-design` or `/ux-audit`.
- **State skip**: forgetting to write `.ux/last-frame.json`. Every downstream command silently degrades when this file is missing.
- **Over-formatting**: padding the output with prose. The framing block is four lines. Resist the urge to explain it.

---

## Recommend mode (`--recommend`)

**One call. Five parallel searches. One merged system out.**

Industry, then style, palette, type, motion, components, brand exemplars and guardrails. The Python engine does the merging; you get a structured recommendation you can hand directly to `/ux-design` or `/ux-system`. The MCP tool `ux_recommend` runs the same engine for MCP hosts.

### How it works

1. The engine reads your brief (project type, industry, audience, tone, must-haves, forbidden, stack, region).
2. Lane 1: `industries.json` lookup gives style/palette/type biases for your domain.
3. Lane 2: `styles.json` filtered by industry + brief tags.
4. Lane 3: `palettes.json` filtered by `style.compatible_palettes`.
5. Lane 4: `type-pairs.json` filtered by `style.compatible_type_pairs`.
6. Lane 5: `motion-presets.json` filtered by style hints.
7. Auxiliary lanes: components by style compatibility, brand exemplars by industry, anti-pattern guardrails (always on).
8. The engine returns one merged Recommendation with rationale lines.

### From a saved discovery brief (the canonical flow)

```bash
python3 -m engine.cli.main --no-pretty recommend --brief-file=.ux/last-discovery.json > .ux/last-recommendation.json
```

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

### Anchored to an extracted client brand

```bash
python3 -m engine.cli.main recommend --brief-file .ux/last-discovery.json --brand-file .ux/brand.json
```

When `--brand-file` points at an extracted client brand (from `/ux-design` Step 1.5 or `references/process/brand-extraction.md`), the recommendation's `palette.colors.primary` becomes the brand color (sampled from the logo, not the most-painted CSS), and it carries `brand` + `type_directive` blocks so the build anchors palette + type to THEM, not the engine's default pick. Without it, the recommender chooses freely from the manifests.

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
print(len(rec.guardrails))         # anti-patterns, always on
```

### Output shape

The recommendation is a JSON document with:

- `style`: one entry from `styles.json` (the picked design philosophy)
- `palette`: one entry from `palettes.json` (the picked color system)
- `type_pair`: one entry from `type-pairs.json` (display + body + mono)
- `motion`: top 5 motion presets compatible with the style
- `components`: top 12 components compatible with the style
- `brand_exemplars`: top 5 brands in the same industry to study
- `guardrails`: every anti-pattern rule (always on)
- `rationale`: one line per lane explaining the pick

The recommendation lands at `.ux/last-recommendation.json` so it chains into `/ux-design` (every mode), `/ux-system`, and `/ux-lint` (which verifies generated code against the guardrails).

### Persisting to your project

After running, save the recommendation as a MASTER.md in your project (offer it every time; `--persist` saves without asking):

    python3 -m engine.cli.main persist save --project-root .

This creates `.ux/design-system/MASTER.md`: a human-readable Markdown capture of every decision. Re-runnable, version-controllable, shareable.

### What recommend mode is and isn't

- IS: A deterministic Python reasoning engine over structured data. Same input always returns the same output. No LLM in the recommender itself.
- IS NOT: A code generator. It tells you WHAT to use; `/ux-design` is what USES it.
- IS NOT: A replacement for taste. The engine recommends; you decide. The brief's `forbidden` field is yours to wield.

---

## Chaining

After discovery completes, the natural next steps:

- `/ux-design [extra brief]`: generates frontend code grounded in the recommendation.
- `/ux-design --component <name>`: generates one component aligned to the discovered constraints.
- `/ux-design --dashboard`: generates a dashboard from the same brief.
- `/ux-system`: generates a full design system from the recommendation.

## Error handling

| Error condition | Recovery |
|---|---|
| User provides empty or near-empty brief | Ask one combined question for the missing fields; never one question per message |
| User answers "everyone" or "users" as audience | Push back with a specific clarifier ("Which customers? Returning, first-time, a specific tier?") up to twice, then flag as a soft field |
| User answers with a vague outcome ("make it better", "improve UX", "modernize") | Push back: "What does the audience do differently after we ship that they don't do today?" |
| Hypothesis lacks causal reasoning | Push back: "What's the bet? If we change X, then Y will happen because Z." |
| Success signal is unmeasurable ("users will love it") | Push back: "What metric, behavior, or signal would prove this worked in two weeks?" |
| `.ux/` directory cannot be created (permissions) | Surface the path error to the user and ask for an alternative project root |
| No data manifests found (recommend) | The engine returns an empty recommendation whose `rationale` says the data files are missing; run `/ux-init` or reinstall the package |
| Industry not found (recommend) | The engine scores all industries against the brief tags and picks the closest |
| Style and palette incompatible (recommend) | The engine picks the highest-scoring palette regardless and flags this in `rationale` |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

## Fallback

If `python3 -m engine.cli.main` is not on PATH, prompt for the 10 fields (or the four framing fields) in the chat and save them as JSON manually. Recommend mode has no prose fallback: say the engine is missing and point to `/ux-init`.
