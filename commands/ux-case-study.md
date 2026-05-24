---
description: Generate a project case study in pure-monochrome editorial format. Triggers on "write a case study", "case study this project", "do the wrap-up doc". Use when writing a project case study, shipping a publishable Wfrah-editorial document, ending a project with a case-study artifact, producing the (A)–(G) section format in pure monochrome. Skip when the project lacks the data to populate (A)–(G) sections, the user wants a marketing landing not a case study (use ux-design).
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-case-study

You are running the `/ux-case-study` command from the `ux` plugin. The job is to produce a project case study as a finished, publishable artifact — pure monochrome editorial typography, hairline separators, numbered section codes, bilingual-safe layout. Not a marketing brochure. A document.

## When to use

Triggers: "write a case study", "case study this project", "do the wrap-up doc", "publish this work", "post-launch retrospective", "portfolio piece". Use after a project ships or after a discrete milestone is hit.

## Input

Required:
- **Project facts** — audience, problem, solution, outcomes, impact, market, target. Pull from `.ux/last-frame.json` and any other `.ux/last-*.json` that contain relevant signal. Ask the user for any facts not in state.
- **Output format**: HTML / Blade / Markdown. Default: HTML.
- **Output path**: default `case-studies/<slug>.<ext>` in the project root.

Ask once if missing: *"Format (HTML / Blade / Markdown) and output path? Or 'defaults' and I'll pick."*

## Process

### 1. Gather facts

Walk through state in priority order:
1. `.ux/last-frame.json` — audience, problem, brand voice
2. `.ux/last-workshop.json` — the Game Plan if a workshop fed this work
3. `.ux/last-research.json` — research findings and decisions
4. `.ux/last-design.json` / `.ux/last-component.json` / `.ux/last-dashboard.json` — what was built
5. `.ux/last-a11y.json` / `.ux/last-polish.json` — quality signals

For anything missing, ask the user in a single round of questions — never piecemeal.

### 2. Read the style reference

Read `references/output/case-study-style.md` before writing. Internalize: pure monochrome, numbered section codes A-G, editorial type, hairline separators, two-tone body emphasis, RTL-safe layout.

### 3. Build the seven sections

Use these exact section codes and headers:

- **(A) About** — what is this project, in two sentences. Plain, declarative.
- **(B) Mission** — the problem and the position. Why this project exists.
- **(C) Outcomes** — what shipped. Specific, dated, with concrete artifacts.
- **(D) Impact** — measured change. Numbers if you have them; qualitative observations if not. Never invent metrics.
- **(E) Market** — the context. Competitors, adjacent solutions, why the moment is right.
- **(F) Chance** — the opportunity that remains. What's next, what's not yet solved.
- **(G) Target Audience** — who this is for. Not demographics — behaviors, needs, contexts.

### 4. Write the document

Direct, declarative voice. Short paragraphs. No marketing inflation. No "delight," "best-in-class," "robust," "leverage," "synergy," "innovative." If a sentence can be deleted without losing meaning, delete it.

Layout:
- Numbered section code (eg. "A") as a small caps prefix to the section header
- Hairline `border-top` between sections — never cards, never shaded boxes
- Body text in a single column, max 65 characters per line
- Two-tone emphasis: primary body in near-black, secondary observations in mid-gray (~50% luminance)
- Pull-quotes in editorial display type, larger than body, no quote marks needed
- Numbers in `font-mono` with tabular figures

### 5. Apply format-specific output

**HTML** (default):
- Single self-contained file with inline `<style>`
- Class names: `.cs-section`, `.cs-code`, `.cs-header`, `.cs-body`, `.cs-aside`, `.cs-quote`, `.cs-rule`
- `dir="ltr"` default; document the RTL swap in a comment
- Web fonts via Google Fonts or system stack; no JavaScript

**Blade**:
- Use the project's existing layout if a Dot-style DS is detected — pull `tokens.css` + `components.css` references
- Wrap in `@extends('layouts.app')` if applicable
- Use real DS classes where they exist; create case-study-specific classes only when DS has no match

**Markdown**:
- Pure markdown, no HTML embedding
- Section codes as `## A — About` etc.
- Pull-quotes as blockquotes
- Numbers and metrics in inline backticks for monospace rendering

### 6. Format the meta-output

```
─── case study brief ───
Project:    <name>
Format:     <HTML | Blade | Markdown>
Output:     <path>
Sections:   A, B, C, D, E, F, G

─── facts assembled ───
Audience:   <one line>
Problem:    <one line>
Solution:   <one line>
Outcomes:   <one line>
Impact:     <one line — or "qualitative only">
Market:     <one line>
Chance:     <one line>
Target:     <one line>

─── document written ───
<path>

─── self-review ───
Voice:           direct / declarative — no marketing inflation
Color:           pure monochrome — no accents
Typography:      editorial — pull-quotes in display, body in serif/sans pairing
RTL-safe:        confirmed
Numbers:         tabular monospace

─── next ───
Recommended: /ux-expert      (share / promote — if the user wants to)
Other moves: /ux-next        (let me decide)
             done            (this is the wrap-up)
```

### 7. Persist state

Write to `.ux/last-case-study.json`:

```json
{
  "command": "ux-case-study",
  "timestamp": "<ISO8601>",
  "project": "<name>",
  "format": "<HTML|Blade|Markdown>",
  "output_path": "<path>",
  "sections": ["A", "B", "C", "D", "E", "F", "G"],
  "facts": {
    "audience": "",
    "problem": "",
    "solution": "",
    "outcomes": "",
    "impact": "",
    "market": "",
    "chance": "",
    "target": ""
  }
}
```

## Hard rules

- **PURE MONOCHROME**. No brand accent on the case study — this is the one place the rule is absolute. Even a brand mark renders monochrome in this format.
- Hairline separators between sections — never cards, never shaded boxes, never colored panels.
- Two-tone body emphasis only: near-black primary, mid-gray secondary.
- Numbers in `font-mono` with tabular figures.
- Bilingual-ready: RTL-safe layout, no directional assumptions in CSS (use `inline-start` / `inline-end`).
- No emojis.
- No marketing inflation language ("delight," "best-in-class," "robust," "synergy," "innovative," "cutting-edge," "leverage").
- No invented metrics. If a number isn't real, don't include it.
- Section codes A-G in order, exact letters.
- Max 65 characters per line in body text.
- Pull-quotes are editorial display type, no quote marks.

## Failure modes

- **Marketing voice creep**: "We delivered a robust, best-in-class solution." Reject and rewrite in declarative voice.
- **Invented metrics**: "Engagement up 47%" with no source. Reject — only real numbers, qualitative if none.
- **Color slip**: a colored CTA button or accent rule appears. Reject — pure monochrome is non-negotiable.
- **Cards reappear**: a section gets a shaded background box. Reject — hairlines only.
- **Section codes out of order or skipped**: reject — A through G, in sequence.
- **DS not respected (Blade format)**: case study written with generic Tailwind when project has a Dot-style DS. Reject — pull tokens + classes.

## Error Handling

| Error condition | Recovery |
|---|---|
| Section (A)–(G) data missing from `.ux/` state and the user can't supply it | Fill placeholders with `{TODO_FILL}` and warn the user that the document is a draft until those fields are populated |
| Impact metrics requested but none are real | Use qualitative observations only; never invent numbers |
| `.ux/last-frame.json` absent and project facts unclear | Ask the user in a single round for the missing fields; never piecemeal |
| Format ambiguous (HTML / Blade / Markdown) | Default to HTML; surface the choice in the meta-output for the user to override |
| Output path collides with existing file | Stop and ask the user; never silently overwrite |
| Blade format requested but no Dot-style DS detected | Fall back to project layout if applicable; otherwise use case-study-specific classes |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

## Next prompt

After `/ux-case-study`:
- `/ux-expert` — share / promote the work, surface contact info
- `/ux-next` — let the conductor pick
- Done — this is the wrap-up artifact
