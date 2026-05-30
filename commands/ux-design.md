---
description: Generate a beautiful, anti-AI-slop design or component from a brief. Dispatches the frontend-engineer sub-agent with creative direction drawn from anti-slop and arsenal references. Use when generating a new design or component from a brief, the user says "build me X" or "design a Y", after running discovery + intaking brand identity, producing premium frontend code with anti-AI-slop discipline. Skip when the user wants a review not a build (use ux-audit / ux-critique), the user wants only one component (use ux-component), backend or infrastructure work.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-design

You are running the `/ux-design` command from the `ux` plugin. The job is to generate a beautiful, high-end design or component from a brief — and explicitly NOT produce AI-slop output.

## When to use

Triggers: "design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "I need a hero section", "design a modal", any free-form request for a visual/UI deliverable.

## Process

### 1. Run the discovery protocol (MANDATORY)

**Never improvise.** Before doing anything else, read `references/process/discovery-protocol.md` and run its 10-field intake on the user. The output of every generation command is downstream of the inputs — improvisation is the single biggest source of mediocre, generic results.

The 10 required fields are:
1. **Brand identity** — pasted brand brief, design tokens, logo files, or "no brand"
2. **Reference inspirations** — 3–5 URLs/screenshots of designs the user LIKES (for aesthetic, not features)
3. **Product type & audience** — one sentence
4. **Style direction** — minimalist / industrial / high-end-visual / editorial / dev-tool-dark / playful / your-call
5. **Voice** — direct, warm, brief / technical / friendly / editorial / playful / from brand
6. **Stack** — React+Tailwind / Next.js / Vue / Blade+Alpine / vanilla / Astro / "what we have"
7. **Imagery sources** — real screenshots / brand photos / placeholders / described generations
8. **Must-have patterns** — terminal mock / bento / interactive demo / specific arsenal pattern / freely pick
9. **Avoid list** — user's personal taste hard-rules beyond standard anti-slop
10. **The wow moment** — the ONE thing this design must do that lifts it above generic

**Delivery rules**:
- Group into 2–3 messages of 3–4 questions each. NEVER all 10 at once.
- First message: brand + references + audience (highest-leverage).
- Second message: style + voice + stack.
- Third message: imagery + must-haves + avoid + wow.
- Wait for each batch's answer before sending the next.

**Skip conditions** (the only ones):
- User passes `--skip-discovery` flag.
- User's first message already covers ALL 10 fields. Verify it does; if anything's missing, ask only for the missing fields.
- User is iterating on a prior design (read `.ux/last-frame.json`; ask only what's changed).

**After collecting answers**: write `.ux/last-frame.json` with the full discovery payload. Echo a 2-sentence summary back to the user before generating — let them stop you if their intent didn't land.

NEVER proceed to step 2 without the wow moment field populated. If the user says "anything's fine", push back: "Give me one concrete moment, even tiny — something a visitor would remember."

### 2. Read the references

Before writing a single line of code, read both:
- `references/styles/anti-slop.md` — the ban list. Internalize every forbidden pattern.
- `references/styles/arsenal.md` — the high-end pattern library. Pick 2-4 patterns that fit the brief.

These are non-negotiable. The output's distinction from generic AI output IS the value of this command.

### 3. Set the dials

Pick values for three dials based on the brief (these are inherited from `design-taste-frontend`):

- **DESIGN_VARIANCE** (1 perfect symmetry → 10 artsy chaos) — default 7 for landing pages, 4 for dashboards, 5 for components
- **MOTION_INTENSITY** (1 static → 10 cinematic) — default 6 for landing pages, 3 for dashboards, 4 for components
- **VISUAL_DENSITY** (1 art gallery → 10 cockpit) — default 4 for landing pages, 8 for dashboards, 5 for components

Override with whatever the user explicitly asked for. Surface your dial values in the output so the user sees what you picked.

### 4. Dispatch the frontend-engineer sub-agent

Call the Task tool with `subagent_type: "frontend-engineer"`. Pass the agent:

- The brief (verbatim from the user)
- Your dial values
- The 2-4 arsenal patterns you picked
- **The page-level section sequence** selected for the brief's goal (see the v2 Python integration step below). Instruct the sub-agent to expand the ENTIRE ordered sequence, map all source content into it (every sector -> a pill, every size -> a card, every benefit -> a checklist item — do not trim), give every card/pill/stat a relevant inline SVG icon, and ship the goal's conversion mechanisms.
- The full content of `references/styles/anti-slop.md` (paste into the prompt — do not assume the sub-agent has read it)
- The target stack
- An instruction to return:
  1. The generated code
  2. A self-review noting which anti-slop bans they had to consciously avoid
  3. Which arsenal patterns they used

Do not write the design yourself. The sub-agent's job is implementation; your job is orchestration.

### 5. Format the output

Use this exact template:

```
─── design brief ───
Product:   <one-line summary>
Stack:     <stack>
Dials:     DESIGN_VARIANCE=<n>, MOTION_INTENSITY=<n>, VISUAL_DENSITY=<n>
Patterns:  <2-4 arsenal patterns chosen>

─── generated ───
<code blocks from the sub-agent — preserve verbatim>

─── self-review (sub-agent) ───
<sub-agent's notes on which anti-slop bans they avoided>
<which arsenal patterns they used and why>

─── next ───
Recommended: /ux-polish      (cosmetic pass on the generated design)
Other moves: /ux-motion      (verify the motion holds up)
             /ux-a11y        (WCAG check on the generated design)
             /ux-case-study  (publish this as a case study)
             /ux-next        (let me decide)
```

### 6. Persist state

Write to `.ux/last-design.json` in the project root:

```json
{
  "command": "ux-design",
  "timestamp": "<ISO8601>",
  "brief": "<verbatim brief>",
  "stack": "<stack>",
  "dials": { "variance": <n>, "motion": <n>, "density": <n> },
  "patterns": ["<arsenal pattern names>"],
  "output_file": "<path if saved to disk>"
}
```

This lets `/ux-next` and downstream commands pick up where you left off.

## SEO is mandatory for public-web outputs

For any landing page or public-facing surface, read `references/foundations/seo.md` and require the frontend-engineer to ship the full SEO foundation (head surface, OG + Twitter, JSON-LD, semantic HTML, image discipline, CWV targets). Surface this requirement in your dispatch prompt. The output is incomplete without it. Derive sensible real values from the brief + source when the brief doesn't supply them (canonical/og:url from the source URL, og:image from a real CDN image the page references). **Never let the frontend-engineer ship a literal `{TODO_FILL...}` token inside the rendered markup** — the linter flags it HIGH and it is a draft-state leak. Where a value is genuinely absent (no phone, no OG image), OMIT that element gracefully (drop the `<meta>` / the affordance); surface any "you should patch this" note to the user OUTSIDE the code, never as a placeholder in the HTML.

## Hard rules (non-negotiable)

- NEVER use purple/blue AI gradients. Single high-contrast accent, saturation < 80%.
- NEVER use generic names ("John Doe", "Acme", "Nexus") in placeholder content.
- NEVER use pure black (`#000`). Use Zinc-950, Charcoal, or Off-Black.
- Imagery is mandatory and REAL: client assets first, then curated Unsplash/Pexels chosen to match the brand + 7-axis temperature (`engine.brand.image_search_terms` suggests on-brand search terms). Pick the best per slot; treat them so they read as deliberate. An abstract SVG is NOT a substitute for a real product/site image. Ban only random/generic stock and auto-rotating placeholder services.
- NEVER ship a text-only wall — always include intentional, real imagery.
- NEVER use emoji as icons. Prioritize **Google Material Symbols** (load via Google Fonts: `Material+Symbols+Outlined` / `Rounded` / `Sharp`, styled with `font-variation-settings`). Phosphor / Radix / Lucide are acceptable secondary choices when an icon doesn't exist in Material Symbols.
- NEVER ship 3-equal-cards layouts. Use 2-col zig-zag, asymmetric, or horizontal scroll.
- NEVER ship horizontal scroll on mobile. Every layout works at 360–390px with `scrollWidth <= innerWidth`; every multi-column block collapses to one column at ≤640px. This is verified in Step 5, not assumed.
- NEVER ship a literal placeholder token (`{TODO_FILL...}`, `{{ var }}`, "lorem ipsum") in the rendered markup. Fill known values; OMIT genuinely-absent elements; never print the token.
- NEVER repeat one icon across differentiated items (every skip size with the same box icon). Distinct icon per item, or none + typographic differentiation.
- NEVER animate `width`/`height`/`top`/`left`. Use `transform` and `opacity` only.
- NEVER skip empty/loading/error states.
- NEVER use serif fonts on dashboards.
- NEVER produce centered hero sections when `DESIGN_VARIANCE > 4` — force asymmetry.
- NEVER use scroll progress paths / scroll-tied SVG line drawing on the side of the page.

If you find yourself reaching for any of these, stop. Re-read `anti-slop.md`. Pick the alternative.

## Failure modes to watch

- **Stack drift**: user said React, sub-agent returns Vue. Catch this in your review of the sub-agent's output, ask for a redo.
- **Slop creep**: sub-agent claims it avoided Inter but actually used it. Grep the output for `Inter` and `font-family: Inter`. Reject and redo if found.
- **Missing states**: sub-agent shows a happy-path component with no loading/error/empty. Reject and redo.
- **Bare-bones output**: sub-agent returns 30 lines for a "landing page" request. Push back — landing pages have multiple sections.

## Error Handling

| Error condition | Recovery |
|---|---|
| Discovery incomplete (any of the 10 fields missing) | Return to discovery — never proceed without all 10 fields populated |
| User refuses to name a wow moment | Push back: "Give me one concrete moment, even tiny — something a visitor would remember." Block generation until provided |
| Stack auto-detection fails or conflicts | Ask the user explicitly which stack to target |
| Sub-agent returns slop tells (Inter on a brand surface, purple gradient, "Acme") | Reject and redo with explicit anti-slop reminder |
| Sub-agent ships code in the wrong stack | Catch in review, redo |
| SEO foundation missing on a public-web output | Reject; the output is incomplete without head surface, OG/Twitter, JSON-LD, semantic HTML, image discipline, CWV targets |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

---

## v2 Python integration — required preamble

Before generating any output, the LLM running this command MUST shell to the v2 Python engine to ground the work in structured data. This is not optional — running without the preamble means generating from training-data defaults (the slop signal).

### Step 1 — Load the saved discovery brief

```bash
test -f .ux/last-discovery.json && cat .ux/last-discovery.json
```

If the file doesn't exist, run `/ux-discover` first. Do NOT proceed without a complete 10-field brief.

### Step 1.5 — Brand: ingest an existing brand.md FIRST, else extract

**Input-first.** Before anything else, check if the project already has a `brand.md` (repo root, or walk up the directory tree) — the common `brand.md` convention. If so, **consume it** instead of extracting; it is the authoritative anchor:

```bash
python3 -m engine.cli.main brand --from-brand-md ./brand.md --out .ux
```

This parses the standard brand.md into `.ux/brand.json` (travels through the engine) + a normalized `.ux/brand.md`. Use it as the HARD ANCHOR exactly as an extracted brand below. Only if there is NO existing brand.md do you extract from the URL/screenshot (the steps below).

If the brief names a reference site/URL or provides a screenshot, the output MUST look like THEM, not the house style. Extract the brand FIRST — canonical rules in `references/process/brand-extraction.md`. The engine is offline, so YOU capture the signals; the engine normalizes + enforces.

1. **Capture the signals.** Open the URL / read the screenshot and **sample the logo pixels** for the dominant non-neutral color (the brand primary comes from the LOGO, not the most-painted CSS), read the logo's letterform style, and collect 2–3 secondary colors, the fonts, any real imagery URLs, and the voice. Write `.ux/brand-signals.json`:
   `{"name":"…","logo":{"src":"…","alt":"…"},"logo_colors":[{"hex":"#…"}],"brand_colors":[{"hex":"#…"}],"logo_type_style":"…","fonts":{"h1":"…","body":"…"},"imagery":["…"],"voice":"…"}`
2. **Build the anchor:**
   ```bash
   python3 -m engine.cli.main brand --signals-file .ux/brand-signals.json --out .ux
   ```
   Writes `.ux/brand.json` (travels through the engine) and `.ux/brand.md` (the human-readable anchor).
3. **CONFIRM before locking (do not skip).** Show the user the extracted `brand.md` — primary color, type direction, logo — in one short message and get a yes. A wrong auto-read (clay instead of amber) poisons the entire build; the 5-second check is the guardrail. If they correct it, edit `.ux/brand-signals.json` and re-run step 2.

If there is NO reference brand, skip this step (pure synthesis from the brief).

### Step 2 — Get the merged recommendation from the engine

```bash
# If a brand was extracted (Step 1.5), pass it so the palette + type anchor to THEM.
BRAND=""; [ -f .ux/brand.json ] && BRAND="--brand-file=.ux/brand.json"
python3 -m engine.cli.main --no-pretty recommend \
  --brief-file=.ux/last-discovery.json $BRAND > .ux/last-recommendation.json 2>/dev/null \
  || echo "engine not installed — falling back to v1 prose-only mode"
```

When `--brand-file` is passed, the recommendation's `palette.colors.primary` is the brand color (from the logo), and it carries `brand` + `type_directive` blocks — the build uses THOSE, not the engine's default pick.

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

### Step 2.5 — Select the page-level section sequence (richness)

A recommendation gives you the *vocabulary* (style/palette/type). The page
*skeleton* — what sections appear and in what order — comes from the page-sequence
selector. Pick one by the brief's goal so the output is RICH and COMPLETE, not a
hero + three cards.

```bash
python3 -c "
import json
from engine.page_sequence import select_sequence
brief = json.load(open('.ux/last-discovery.json'))
goal = brief.get('goal') or brief.get('primary_goal') or brief.get('product_type') or ''
query = goal or (str(brief.get('product_type','')) + ' ' + str(brief.get('audience','')))
seq = select_sequence(query) or select_sequence(json.dumps(brief))
print(json.dumps(seq, indent=2) if seq else 'no sequence matched')
" 2>/dev/null
```

Then EXPAND the whole sequence in the build (this is non-negotiable for richness):

- Render EVERY section in `section_sequence`, in order — do not trim to the few you find easiest.
- Map ALL source content into it: every sector -> a Category pill, every size/package -> an Item card, every benefit -> a Value card or checklist item. Completeness over neatness — one source item, one element.
- Give EVERY card, pill, and stat a relevant inline SVG icon (Lucide-style, `currentColor`, 1.5–2px stroke). Never emoji, and never a numbered-placeholder generic glyph.
- Include the `conversion_mechanisms` the goal needs even if the source page lacked them. For `lead-gen-service` that means an inline hero form, a proof/stats bar, trust signals, and a visible phone affordance.

Pass the selected sequence to the frontend-engineer sub-agent as the page skeleton.

### Step 3 — Use the recommendation as hard constraints

The engine's picks are not suggestions — they're constraints:
- The picked `style.tokens` are the design vocabulary you generate from
- The picked `palette.colors` are the only color tokens used
- The picked `type_pair` is the only typography (display + body + mono)
- The 35+ `guardrails` are checked-against during generation — do NOT emit code that matches any anti-pattern regex
- The 5 `brand_exemplars` are the visual reference for taste

### Step 4 — Generate output

Dispatch the `frontend-engineer` sub-agent (Task tool) with the recommendation passed in as creative-direction context. Generate the page/component as requested by the brief, using ONLY the picked style + palette + type + motion presets + components.

**If a brand was extracted (Step 1.5):** paste the full `.ux/brand.md` into the sub-agent prompt and state that the brand is a HARD ANCHOR — use the client's logo, the brand primary color (the recommendation's palette is already anchored to it), and type matching the logo style; never fall back to the house style or a rejected default font. **Preserve the client's existing human copy verbatim** unless the brief explicitly asks for a rewrite.

### Step 5 — Lint + brand-fidelity gate before reporting

```bash
python3 -m engine.cli.main --no-pretty lint <output-paths> --threshold high
```

Exit code non-zero means a high+ finding landed in your output. Fix before declaring done.

**Responsive gate — HARD, as hard as the brand gate.** Render the output at 390px in a headless DOM and assert there is NO horizontal scroll (`document.documentElement.scrollWidth <= window.innerWidth`) AND that the hero / any 2-col sections have stacked to a single column. Horizontal scroll on mobile is a CRITICAL fail and the single most common shipped defect — **do not declare done while it exists.** Run it at 390px AND 360px.

Use whatever headless browser is on hand. Playwright is the cleanest:

```bash
python3 - "$OUTPUT_HTML" <<'PY'
import sys, pathlib
from playwright.sync_api import sync_playwright   # pip install playwright && playwright install chromium
url = pathlib.Path(sys.argv[1]).resolve().as_uri()
fail = False
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (390, 360):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2)
        pg.goto(url); pg.wait_for_timeout(400)
        m = pg.evaluate("""() => {
          const overflow = [...document.querySelectorAll('*')]
            .filter(e => e.getBoundingClientRect().right > window.innerWidth + 1)
            .slice(0, 8).map(e => e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).trim().split(/\\s+/)[0] : ''));
          const hero = document.querySelector('.hero .grid, [class*="hero"] [class*="grid"], main section:first-of-type .grid');
          const cols = hero ? getComputedStyle(hero).gridTemplateColumns.split(' ').length : null;
          return { iw: window.innerWidth, sw: document.documentElement.scrollWidth, overflow, heroCols: cols };
        }""")
        hscroll = m["sw"] > m["iw"]
        stacked = (m["heroCols"] is None) or (m["heroCols"] == 1)
        print(f"[{w}px] innerWidth={m['iw']} scrollWidth={m['sw']} h-scroll={hscroll} heroCols={m['heroCols']} stacked={stacked}")
        if m["overflow"]: print(f"        overflowing: {m['overflow']}")
        if hscroll or not stacked: fail = True
    b.close()
sys.exit(1 if fail else 0)
PY
```

If Playwright is not installed, the same three signals (`window.innerWidth`, `document.documentElement.scrollWidth`, and the hero container's computed `grid-template-columns` track count) can be read through any headless-DOM tool you have — a headless-Chrome eval, or an MCP browser-preview that supports a viewport resize + a JS eval. Always read `window.innerWidth` first and confirm it is ~390/360 before trusting the scroll number; on failure, the `overflow` list above names the offending nodes so you can fix the specific block (almost always a fixed multi-column grid or a `100vw` element).

**If a brand was extracted, also run the brand-fidelity HARD FLOOR** — an off-brand page fails no matter how good it looks (it must use the brand primary, carry the logo, and ship real imagery):

```bash
python3 -c "
import json, sys
from engine.evaluator import evaluate
from engine.brand.extract import BrandProfile
b = json.load(open('.ux/brand.json'))
prof = BrandProfile(**{k: v for k, v in b.items() if k in BrandProfile.__dataclass_fields__})
ev = evaluate(html=open('<output.html>').read(), brand_profile=prof)
print('brand_fidelity', ev.brand_fidelity, '| imagery', ev.imagery, '| passed', ev.brand_passed)
[print(' -', n) for n in ev.notes if 'BRAND FLOOR' in n]
sys.exit(0 if ev.brand_passed else 1)
"
```

Exit `1` = the output dropped the brand primary/logo or shipped no real imagery. Fix it (use the brand color, carry the logo, add real images) and re-run. **Do not declare done while the brand gate fails.**

### Fallback

If `python3 -m engine.cli.main` is not on PATH (user hasn't installed v2 yet), fall back to v1 prose-only behavior using references/foundations/*.md as the source of taste. The output quality will be lower but the command still works.
