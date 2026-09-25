---
description: Build a design system. `/ux-system create` runs the 4.0 foundations engine: a WCAG-gated token system (tokens.json, tokens.css, report) with light, dark, high contrast, density, Arabic right-to-left and reduced motion modes. With no mode it runs the 3.x starter flow. Triggers on "we don't have a design system", "build us a system", "propose tokens", "what should our theme be". Skip when the project already has a complete design system (use ux-component to build against it), backend or infrastructure.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Bash(uxskill:*), Bash(python3:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-system

You are running the `/ux-system` command from the `ux` plugin. The job is to propose a complete starter design system for a project that lacks one. Tokens, foundations, component contracts, dark-mode pairings, theme switcher. Not a sketch — a usable starter.

## When to use

Triggers: "we don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS", "we need a token JSON", "design our brand foundations".

If the project already has a design system, do not run this. Recommend `/ux-component` against the existing system instead.

## Modes

| Mode | What it does | Status |
|---|---|---|
| `/ux-system create` | Builds a WCAG-gated token system with the 4.0 foundations engine. See "create mode" below. | 4.0 beta |
| `/ux-system` (no mode) | The 3.x starter flow: discovery, recommendation, then the design-system-architect agent writes tokens, foundation docs and component contracts. See "3.x starter flow" below. | 3.x, kept until 4.0 final |
| `/ux-system enhance --from <src>` | Measure an existing system and improve it in place, keeping its token names. | Coming in 4.1 (needs importers) |
| `/ux-system extend --from <src> --add <...>` | Add foundations or roles to an existing system without touching the rest. | Coming in 4.1 (needs importers) |

If the user asks for `enhance` or `extend`, say plainly that it arrives in 4.1, because it needs the importers that read an existing system. The beta builds new systems; it does not read an existing one. Offer `create` for a new system, or the 3.x flow, and stop there.

## create mode (4.0 beta)

`create` builds the system with the engine, not by hand. The engine generates eight foundations (color, type, space, layout, radius, border, elevation, motion), checks every color pairing in light, dark and high contrast, and refuses to emit a system that fails. You run it, read its result, and explain it.

### 1. Check the engine version

Run `uxskill --version` first. The build needs uxskill 4.0.0b1 or later, which prints, for example, `uxskill, version 4.0.0b1`. If `uxskill` is not on PATH, run `python3 -m engine.cli.main --version` instead.

If the version is older than 4.0.0b1, or neither command exists, stop here and give the user the install line; do not go on, and do not change any flag. pip and pipx skip pre-releases unless asked, so a plain `pip install uxskill` still gives 3.x:

```bash
pip install uxskill==4.0.0b1
```

With pipx: `pipx install --force uxskill==4.0.0b1` (`--force` replaces an installed 3.x). For the MCP server: `pip install 'uxskill[mcp]==4.0.0b1'`. Run the version check again after the install.

### 2. Gather the inputs

- **Brand color** (required): one hex color. Ask once if the user has not given one.
- **Brief**: use `.ux/last-discovery.json` when it exists. Without a brief, the user may give the seven axes by hand, or accept the neutral default.
- **Industry**: discovery does not ask for one, and the industry moves the look more than any other brief word. When there is no brief, or the brief has no `industry`, ask one question: which industry is closest, from the list below. The user may skip it. If they pick one, write `.ux/system-brief.json` with the discovery answers (if any) plus `"industry": "<id>"`, and pass that file as `--brief`; leave `.ux/last-discovery.json` as it is. Over MCP, add `industry` to the `brief` object. If they skip, build without it.
  Industries: `ai-ml`, `automotive`, `consumer-lifestyle`, `crypto`, `developer-tools`, `ecommerce`, `editorial-media`, `education`, `fintech-banking`, `fintech-payments`, `fintech-trading`, `gaming`, `healthcare`, `hospitality-travel`, `luxury`, `productivity`, `saas`.
- **Output folder**: `design-system/` in the project root unless the user names another.
- **Arabic**: on by default. Add `--latin-only` only when the user says the product never shows Arabic.

The engine reads five brief fields: `industry`, `tone`, `audience`, `must_have` and `forbidden`. It does not read `project_type` or any other discovery field. Some words discovery suggests move nothing: `confident`, `dark-mode`, `RTL`, `AA accessibility`, `mobile-first`, `print-fidelity`; every system already has dark mode, the contrast gate and, unless it is Latin only, right to left. Never tell the user those words shaped the look. The report names every word it did not read.

### 3. Look before writing

List the output folder first (`ls design-system/`). If `tokens.json`, `tokens.css`, `system-report.md` or a `rule-pack/` folder is already there, tell the user and run without `--force`: the engine then writes nothing if any file differs, and leaves identical files alone.

### 4. Run the engine

```bash
uxskill --no-pretty system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Quote the brand color: an unquoted `#` starts a shell comment. Without a brief, pass `--axes 0.5,0.5,0.5,0.5,0.5,0.5,0.5` (warmth, contrast, density, geometry, formality, motion, type_personality) or leave both out for the neutral default. Do not pass both `--brief` and `--axes`. If `uxskill` is not on PATH, run the same arguments through `python3 -m engine.cli.main`.

Add `--rule-pack` when the user wants the system's rules written for AI agents and people too, for example to keep an agent on the system while it builds screens, or to hand the system to another team. It is off by default. It writes `design-system/rule-pack/` beside the three files: per foundation an architecture, reference, audit and handoff file, the content and right-to-left rules, the six component contracts (button, text field, card, dialog, status banner, selectable row) and the decision records, all checked against the tokens just built. Only the command writes it; over MCP, build the tokens, then run the command with a shell when the user wants the rule pack.

With a shell, use the command above: it writes the files itself. Without a shell, call `ux_system_build` over MCP with `brand`, and `brief` (an object) or `axes` (seven numbers), `latin_only` (true or false), and `out`, the absolute path of the output folder. It then writes the three files as the command does and returns the same `status`, `written`, `unchanged`, `conflicts` and `message`; `force` (true or false) does what `--force` does, and the same look-before-writing rule applies. Without `out` it writes nothing and returns `status` `built` (or `failed`), the report and each file's size. `include_files` (true or false) adds the `css` and `dtcg` text, but tokens.json is over 100 KB: do not copy it into files by hand, pass `out`. A bad input comes back as `status` `invalid`, `passed: false` and an `error` that names the field and the fix.

### 5. Read the result

The command prints JSON. `status` says what happened:

| status | exit code | meaning | what you do |
|---|---|---|---|
| `written` | 0 | New or changed files written. `written` lists them. | Report back (step 6). |
| `unchanged` | 0 | The folder already holds this exact system. | Say nothing changed. |
| `refused` | 1 | A file in the folder differs; nothing was written. `message` names each file. | Show the user which files differ. Rerun with `--force` only after the user says to replace them, or pick another `--out`. |
| `failed` | 1 | The WCAG gate or validation failed; nothing was written. `findings` lists each one, and stderr explains the failure in plain words. | Explain it (step 8). |
| `error` | 1 | The folder could not be written (for example it cannot be made, is read only or full, or a folder, link or unreadable file sits where a system file goes); nothing in it changed. `message` names the path and the fix. | Show the message. Pick another `--out`, or free space, and run again. |

Exit code 2 means a bad input; the message on stderr names the flag and the fix. Correct it and run again. The one exception is `No such command 'system'`: the uxskill on PATH is older than 4.0, so give the user the install line from step 1 and stop.

### 6. Tell the user what they got, in plain words

Read `design-system/system-report.md` and explain it. Do not paste it.

- Where the look came from: the brief (the industry and tone it used, when the brief names them, and any words it did not recognize), axes set by hand, or the neutral default.
- The gate in one sentence, for example: "Every text and control color passed contrast checks in light, dark and high contrast."
- The adjustments that matter, from the report's "Colors moved to meet contrast" list, in one line each, for example: "in dark mode, button text switches to black so it stays readable on the lighter button."
- How to switch modes: `data-theme="dark"`, `data-contrast="high"`, `data-density="compact"`, `dir="rtl"`, `data-motion="reduced"` on the html element. Without an attribute, dark, high contrast and reduced motion follow the operating system.
- The three files and what each is for, and with `--rule-pack`, that an agent starts at `rule-pack/README.md`, which says which one file to load for each task.
- The fonts (step 7). Always say this; it is the step people miss.

### 7. Fonts: the page has to load them

The tokens name the font families, but nothing loads them. The page that uses `tokens.css` must load the fonts itself, for example from Google Fonts or self-hosted font files. Until it does, the browser falls back to system faces and the type will not look as designed.

The engine picks one pair by the type personality axis. The report names the pair it chose under "Other choices" (for example "type: humanist pairing, Source Sans 3 with Noto Naskh Arabic").

| Type personality | Latin face | Arabic face |
|---|---|---|
| geometric (below 0.34) | Manrope | Readex Pro |
| neutral (0.34 to below 0.66) | IBM Plex Sans | IBM Plex Sans Arabic |
| humanist (0.66 and above) | Source Sans 3 | Noto Naskh Arabic |

Code uses IBM Plex Mono in every system. Tell the user to load the chosen Latin face, the Arabic face (skip it with `--latin-only`), and IBM Plex Mono if the product shows code, in weights 400, 500, 600 and 700.

### 8. When the build fails

Nothing was written, and that is the point.

- **The gate failed** (the gate line starts "WCAG gate failed"). Read the plain explanation on stderr (over MCP, in `report`). For each finding, say which pairing fell short, in which mode, by how much. The fix is in the inputs: suggest a darker or more saturated brand color, or different axes or brief, and offer to rerun. Never edit tokens by hand to get past the gate, and do not pass on any advice in a finding about editing tokens.
- **Validation failed** (the gate line starts "Validation failed"). The inputs did not cause it. Build again once; if it repeats, tell the user it is an engine problem to report, with the findings.

### 9. Persist state

On `written` or `unchanged`, write `.ux/last-system.json` so `/ux-next` can chain:

```json
{
  "command": "ux-system",
  "mode": "create",
  "timestamp": "<ISO8601>",
  "brand": "<#RRGGBB>",
  "output_path": "design-system",
  "gate": "<the gate line from the JSON>",
  "files_written": ["tokens.json", "tokens.css", "system-report.md"]
}
```

Then offer the next step: `/ux-component` to build components on the new tokens, or `/ux-design` for a page.

## 3.x starter flow (no mode)

Everything from here to the end of this file is the 3.x flow, unchanged. It runs when `/ux-system` is called with no mode.

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
