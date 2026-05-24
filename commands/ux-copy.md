---
description: Microcopy review and rewrite against the voice rubric. Produces a before/after table with severity per string and a clean rewrite block. Triggers on "review the copy", "fix the microcopy", "the error messages are bad", or "rewrite this". Use when reviewing or rewriting microcopy, fixing error messages that sound like AI, tightening empty/loading/success state copy, checking CTAs against the voice rubric, auditing forms for label / helper / error patterns. Skip when the surface has no user-facing strings, the copy is auto-generated from data with no editorial layer, backend or infrastructure.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(mkdir:*), Bash(date:*), Glob, Grep, Task, WebFetch
disable-model-invocation: false
---

# /ux-copy

You are running the `/ux-copy` command from the `ux` plugin. The job is to evaluate every visible string on a surface against the voice rubric and produce a before/after rewrite that the team can drop in.

## When to use

Triggers: "review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "copy pass", "tighten the strings", "the buttons sound generic", "this empty state is dead", "the errors are useless".

Use when the structure of the surface is roughly right but the words are weak. Not for layout problems (use `/ux-audit` or `/ux-polish`). Not for accessibility-driven copy (use `/ux-a11y`, which catches alt text and form-error wiring).

## Input

One of: a URL, an absolute file path containing the strings (Blade view, JSX, JSON locale file, etc.), a screenshot, or pasted copy. Also required: the **target voice** — either named (e.g., "Dot voice: direct, warm, brief, unpretentious") or pasted as a short voice spec. If voice is not provided and the project has a voice file (`project_dot_voice.md` or similar), read it and use it.

## Process

### 1. Establish the voice

Confirm or look up the target voice. Surface the rubric explicitly at the top of the output so the user can disagree before you spend time rewriting.

Standard voice rubric (default if no voice provided):

- **Direct** — say the thing, no preamble.
- **Warm** — assume good faith, not corporate.
- **Brief** — two sentences max, one if you can.
- **Specific** — name the thing, name the action.
- **Unpretentious** — no "leverage," "empower," "seamless," "robust."

Project-specific voice overrides the default — if Dot is the project, the rubric is whatever `project_dot_voice.md` says.

### 2. Extract every string

Pull every visible string from the surface:

- Headings, subheads, body copy
- Button labels, link text
- Form labels, placeholder text, helper text, validation messages
- Error states, empty states, loading states, success messages
- Tooltips, modal titles, modal body, modal CTAs
- Notification text, toast text
- Image alt text (also caught by `/ux-a11y` — flag here too)
- Locale file keys if a locale file is in scope

If a locale file (`lang/en.json`, `lang/ar.json`, etc.) is the source, list ALL locale keys in scope, not only the ones currently displayed.

### 3. Evaluate each string

For each string, score against the rubric and decide severity:

- **Critical** — breaks the user's task. Examples: error messages that do not name the field or the fix; CTAs that do not describe the action; empty states that say "nothing here" with no next move.
- **High** — confuses or slows the user. Examples: jargon, passive voice in errors, generic CTAs ("Submit," "OK," "Continue"), congratulatory exclamations ("Awesome! You did it!").
- **Medium** — works but undersells the surface. Examples: weak headlines, filler subheads, tooltips that restate the label.
- **Cosmetic** — voice drift. Examples: a stray "leverage," inconsistent capitalization in CTAs, missing serial comma where the voice uses them.

### 4. Write the before/after table

Format:

```
─── voice rubric ───
<bulleted list of the rubric being applied>

─── before/after ───

Location                   Severity   Before                                  After
─────────────────────────  ─────────  ──────────────────────────────────────  ──────────────────────────────────────
<page/file:line or label>  Critical   <verbatim current string>               <rewrite>
<page/file:line or label>  High       <verbatim>                              <rewrite>
...
```

Keep the table compact. If a rewrite needs context (alternates, voice notes), put it in a `Notes` column or a short follow-up block under the table.

### 5. Write the clean rewrite block

After the table, produce a clean block of all rewrites grouped by location, ready to paste into the codebase or the locale file. If the source was a locale JSON file, output the JSON patch directly:

```json
{
  "errors.phone.invalid": "Phone number isn't quite right. Try the international form with country code.",
  "states.empty.transactions": "No transactions yet. New activity will show up here within a minute."
}
```

If multi-locale (Dot ships in 11 locales), flag any keys added/changed and list the locales that need a parallel rewrite. Do NOT machine-translate — flag and hand off to a translator (Hala for Dot).

### 6. Persist state

Write `.ux/last-copy.json`:

```json
{
  "command": "ux-copy",
  "timestamp": "<ISO8601>",
  "surface": "<URL / path / description>",
  "voice_rubric": ["<rule 1>", "<rule 2>", "..."],
  "strings": [
    {
      "location": "<page/file:line or label>",
      "severity": "Critical | High | Medium | Cosmetic",
      "before": "<verbatim>",
      "after": "<rewrite>",
      "notes": "<optional>"
    }
  ],
  "severity_counts": { "critical": <n>, "high": <n>, "medium": <n>, "cosmetic": <n> },
  "locales_needing_translation": ["<locale codes>"]
}
```

### 7. Optional fix flag

If the user passed `--fix`, after writing the report:

1. Validate clean working tree.
2. Show the user the diff (before/after side by side) and ask for explicit confirmation — copy fixes are taste-sensitive and silent application is the wrong default.
3. On confirmation, dispatch the `copy-writer` sub-agent via the Task tool to apply the changes. Pass the agent the full table and the voice rubric.
4. Commit atomically with a message naming the location and the severity tier addressed.
5. If multi-locale, only apply the English (or source-locale) change automatically and create a translation task for the rest.

## Output

The voice rubric, the before/after table, the clean rewrite block, and (if `--fix`) the diff-confirm-apply flow.

## State persisted

- `.ux/last-copy.json` — keys: `command`, `timestamp`, `surface`, `voice_rubric` (array), `strings` (array of `{location, severity, before, after, notes}`), `severity_counts`, `locales_needing_translation`.

## Next prompt

```
─── next ───
Recommended: /ux-copy --fix     (apply the rewrites)
Other moves: /ux-a11y           (check form-error wiring and alt text)
             /ux-audit          (broader structural review)
             /ux-next           (let me decide)
```

If all severities are Cosmetic only, recommend `/ux-polish` instead of `--fix` — the copy is fine, the surface needs a different kind of attention.

## Hard rules

- Never auto-apply copy fixes without a diff-confirm step. Copy is taste; silent rewrites burn trust.
- Never machine-translate. Flag locales that need translation; hand off to a human or named translator (Hala for Dot).
- Never use "leverage," "empower," "seamless," "robust," "delight," "elevate," or "unlock" in rewrites unless the voice explicitly allows them.
- Never write a rewrite that is longer than the original unless the original was unsafe or unclear. Brevity is the default.
- Never produce a rewrite that exclaims congratulations ("Awesome!", "You did it!", "Yay!"). Calm even when celebrating.
- Never rewrite legal, accessibility-required, or branded copy without flagging it. Some strings are constraints, not opportunities.

## Failure modes

- **Voice drift mid-table**: starting in the target voice and slipping into generic SaaS-speak by row 10. Re-read the rubric before each batch.
- **Length creep**: rewrites that are "better" but longer. If the rewrite is longer, justify it in the Notes column or shorten it.
- **Missing the error pattern**: leaving error messages with no fix included. Every error rewrite must name the field AND tell the user what to do.
- **Locale orphans**: rewriting English and never flagging the other 10 locales for Dot. Always surface the translation task.
- **CTAs that hide**: rewriting a CTA to "Continue" or "OK." A CTA is verb + outcome ("Save payment method," "Send reset code"). Generic CTAs are a fix regression.

## Error Handling

| Error condition | Recovery |
|---|---|
| Voice profile missing | Reuse `.ux/last-frame.json` if present; otherwise apply the default voice rubric and surface it at the top of output for the user to disagree |
| Source strings ambiguous (which file / which key / which surface) | Echo back what you extracted before rewriting; ask one clarifier if still unclear |
| Multi-locale project — non-source-locale strings encountered | Flag for translation; never machine-translate; hand off to the named translator (Hala for Dot) |
| `--fix` requested without a diff-confirm step | Refuse; copy fixes always require explicit user go on the before/after |
| Legal, accessibility-required, or branded copy detected in the rewrite scope | Flag it as a constraint, do not silently rewrite |
| Locale file path malformed or unreadable | Surface the parse error, ask for the canonical path |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.
