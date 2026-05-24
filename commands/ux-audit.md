---
description: Full 6-lens UX review of a surface. Outputs a structured Polaris-style report with findings, severity, evidence, and fixes. Triggers on "audit", "review the ux", "is this any good", or "what's broken".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Bash(curl:*), Bash(date:*), Glob, Grep, Task, WebFetch
disable-model-invocation: false
---

# /ux-audit

You are running the `/ux-audit` command from the `ux` plugin. The job is a structured, opinionated review of a surface against six lenses, producing findings the user can act on.

## When to use

Triggers: "audit", "review the ux", "is this any good", "what's broken", "audit this page", "ux review", "tear this apart".

Use when the surface already exists (live URL, mockup, code, screenshot) and the user wants a structured, defensible critique with severity-tagged findings. Not for taste calls — that is `/ux-critique`. Not for a single dimension — use `/ux-copy`, `/ux-a11y`, `/ux-motion`, or `/ux-polish` for narrow scopes.

## Input

One of: a URL, an absolute file path to code or a markup file, a screenshot path, a code snippet pasted in chat, or a free description. If multiple, treat them as the same surface.

If `.ux/last-frame.json` exists, read it first — audience and outcome anchor every finding's severity.

## Process

### 1. Anchor to the framing

Read `.ux/last-frame.json` if present. If absent and the surface clearly needs framing context, suggest running `/ux-frame` first — but proceed if the user insists.

### 2. Read the surface

- URL → fetch the page (WebFetch or the browser MCP if available).
- File path → read the file.
- Screenshot → look at the image.
- Code snippet → use as-is.
- Description → ask one clarifying question if too vague to inspect, then proceed.

### 3. Run the six lenses in order

For each lens, identify findings, cite which principle each finding violates, write evidence (what you saw) and a fix (what to do).

#### Lens 1 — FRAME

Reference: `references/process/lean-ux-gothelf.md` and `references/process/lean-ux-klein.md`.

Check: does the surface match the audience and outcome from the framing? Is the hypothesis observable in the surface? Is the success signal supported by what the user can do here?

If the framing is missing, this lens checks: does the surface have a clear "who is this for and what changes for them?" signal — or is it generic?

#### Lens 2 — DISCOVER

Reference: `references/laws/norman.md`.

Check: signifiers (does the user see what they can do?), discoverability (are key actions findable in under three seconds?), mental models (does it match what the audience expects from this category of product?), gulf of execution (can the user form an intention here?).

#### Lens 3 — SCAN

Reference: `references/laws/krug.md`.

Check: information hierarchy (does the eye know where to land?), self-evidence (can the user grok the page without reading?), noise reduction (what can be cut?), the squint test (does the layout survive blurred vision?).

#### Lens 4 — ACT

Reference: `references/laws/laws-of-ux.md` and `references/laws/norman.md`.

Check: Fitts's law (are tap targets sized and placed for the gesture?), Hick's law (too many choices at decision points?), feedback (does every action have a visible response within 100ms?), affordances (do controls look like the kind of control they are?).

#### Lens 5 — READ

Reference: `references/foundations/copy.md`.

Check: are CTAs verb + outcome? Are errors specific with the fix included? Are empty states helpful, not decorative? Is the voice consistent? Is the copy doing work or filling space?

#### Lens 6 — RECOVER

Reference: `references/laws/norman.md` and `references/foundations/accessibility.md`.

Check: error prevention (can the user undo or be warned before mistakes?), error recovery (when something goes wrong, can the user fix it without leaving?), accessibility floor (contrast, focus, keyboard, screen reader basics — full audit lives in `/ux-a11y`).

### 4. Score and group findings

For each finding, assign severity:

- **Critical** — blocks the success signal. Audience cannot complete the outcome.
- **High** — degrades the success signal significantly. Outcome possible but friction is severe.
- **Medium** — friction the audience will tolerate but should not have to.
- **Cosmetic** — polish issue. Audience may not notice, but a discerning reviewer would.

Group findings by lens. Within each lens, sort Critical → Cosmetic.

### 5. Format the output

Use the Polaris-style report template per `references/output/polaris-style.md`. Skeleton:

```
─── audit ───
Surface:          <URL / path / brief description>
Framing anchor:   <audience + outcome, or "no framing on file">
Severity counts:  Critical <n> | High <n> | Medium <n> | Cosmetic <n>

─── findings ───

FRAME
  [<severity>] <finding title>
    Principle: <which principle>
    Evidence:  <what you saw>
    Fix:       <what to do>

DISCOVER
  ...

SCAN
  ...

ACT
  ...

READ
  ...

RECOVER
  ...

─── strategic moves ───
1. <highest-impact move based on finding cluster>
2. <second move>
3. <third move>
```

Keep each finding to three lines. No prose paragraphs in the findings section.

### 6. Persist state

Write `.ux/last-audit.json`:

```json
{
  "command": "ux-audit",
  "timestamp": "<ISO8601>",
  "surface": "<URL / path / description>",
  "findings": [
    {
      "lens": "FRAME | DISCOVER | SCAN | ACT | READ | RECOVER",
      "severity": "Critical | High | Medium | Cosmetic",
      "title": "<short>",
      "principle": "<which principle>",
      "evidence": "<what you saw>",
      "fix": "<what to do>"
    }
  ],
  "severity_counts": { "critical": <n>, "high": <n>, "medium": <n>, "cosmetic": <n> },
  "dominant_lens": "<lens with highest-severity cluster>",
  "strategic_moves": ["<m1>", "<m2>", "<m3>"]
}
```

### 7. Optional fix loop

If the user passed `--fix`, after writing the report enter the fix loop:

1. Validate clean working tree.
2. For each finding sorted Critical → Cosmetic (skip Cosmetic unless `--include-cosmetic`):
   - If it is a code/layout finding → dispatch `frontend-engineer` sub-agent via Task tool.
   - If it is a copy finding → dispatch `copy-writer` sub-agent.
   - If it is a motion finding → dispatch `motion-engineer` sub-agent.
   - Where findings are independent, dispatch the agents in parallel in a single message.
3. Each agent commits atomically with a message linking the finding title.
4. After fixes, re-run the audit and report deltas.

If no `--fix`, end with the next-prompt block.

## Output

The audit report from step 5, followed by either fix-loop results (if `--fix`) or the next-prompt block.

## State persisted

- `.ux/last-audit.json` — keys: `command`, `timestamp`, `surface`, `findings` (array of `{lens, severity, title, principle, evidence, fix}`), `severity_counts`, `dominant_lens`, `strategic_moves`.

## Next prompt

Based on `dominant_lens` (the lens with the highest-severity cluster), recommend the narrower follow-up:

- FRAME → `/ux-frame` (the brief is the problem)
- DISCOVER → `/ux-audit --fix` (structural fixes)
- SCAN → `/ux-polish` (hierarchy and rhythm)
- ACT → `/ux-audit --fix` (interaction-level fixes)
- READ → `/ux-copy --fix` (copy pass)
- RECOVER → `/ux-a11y` (accessibility deep-dive)

Print:

```
─── next ───
Recommended: <command keyed off dominant lens>
Other moves: /ux-audit --fix    (apply all findings)
             /ux-critique        (taste call instead of structured)
             /ux-next            (let me decide)
```

## Hard rules

- Never produce a finding without a citation to the relevant reference principle.
- Never write a finding longer than three lines (Principle, Evidence, Fix). Push detail into the fix loop or a follow-up command.
- Never skip a lens because the surface "doesn't need it." Run all six — "no findings" is itself a finding.
- Never use vague severity ("kinda bad"). Critical / High / Medium / Cosmetic only.
- Never start a fix loop without a clean working tree confirmation.
- Never dispatch the wrong agent — code findings to `frontend-engineer`, copy to `copy-writer`, motion to `motion-engineer`.

## Failure modes

- **Tour-guide audits**: describing what the surface does instead of what is wrong. Every finding must name a problem and a fix.
- **Severity inflation**: marking everything Critical. If severity counts are skewed, force triage — only outcome-blockers are Critical.
- **Lens skip**: running 4 lenses because the others "seem fine." Run all 6.
- **Fix without verify**: applying fixes in `--fix` mode but not re-running the audit. The user needs to see the delta.
- **Parallel-dispatch confusion**: dispatching dependent agents in parallel. If two findings touch the same file, queue them sequential.
