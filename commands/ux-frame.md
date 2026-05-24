---
description: Lean UX intake. Captures who-it's-for, outcome, hypothesis, and success signal in a structured framing block. Triggers on "frame this", "what's the brief", "set up the project", or "framing".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(mkdir:*), Bash(date:*), Glob, Grep
disable-model-invocation: false
---

# /ux-frame

You are running the `/ux-frame` command from the `ux` plugin. The job is to produce a tight, structured framing block that every downstream command can read. No design work happens here. No critique. Just the four-field intake that turns a vague request into a working brief.

## When to use

Triggers: "frame this", "what's the brief", "set up the project", "framing", "what are we actually building", "frame the work", "scope this".

Use at the start of any project, sprint, or one-off engagement. Also use mid-stream if a conversation has drifted and nobody can answer "who is this for and what changes when we ship?"

## Input

Anything the user has: a Slack paste, a Figma URL, a one-line idea, a ticket, a meeting transcript, or nothing. If the input already contains the four framing fields, extract them — do not re-ask.

## Process

### 1. Extract or ask — never both

Read what the user provided. If you can confidently pull `audience`, `outcome`, `hypothesis`, and `success_signal` out of the input, skip ahead to step 3.

If any field is missing, ask ONCE with a single combined question that surfaces all gaps. Example:

> "Quick framing — who specifically is this for (not 'users'), what changes for them when we ship, what's your bet on why this will work, and how will we know it worked? One paragraph is fine."

Do not ask the four questions in four separate messages. That is the failure mode this command exists to prevent.

### 2. Sharpen the answers

Apply these tests before accepting any field:

- **Audience** — must name a real person/role/segment. Reject "everyone," "users," "people," "customers" without further qualifier. Push back specifically: "Which customers? Returning ones? First-time? A specific tier?"
- **Outcome** — must describe a behavior or state change for the audience, not a feature. Reject "make it better," "improve UX," "modernize." Push back: "What does the audience do differently after we ship that they don't do today?"
- **Hypothesis** — must include a causal "because" or "if-then." Reject "we think it'll be good." Push back: "What's the bet? If we change X, then Y will happen because Z."
- **Success signal** — must name a measurable thing or an observable behavior. Reject "users will love it." Push back: "What metric, behavior, or signal would prove this worked? How would you know in two weeks?"

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

Every downstream command reads this file to anchor its work.

## Output

The framing block from step 3, followed by the next-prompt section below. Nothing else. No commentary, no congratulations, no "here is your framing." Just the block and the next move.

## State persisted

- `.ux/last-frame.json` — keys: `command`, `timestamp`, `audience`, `outcome`, `hypothesis`, `success_signal`, `soft_fields`.

## Next prompt

After writing the block, surface the next move based on what the framing reveals:

- If the surface already exists and the user wants a review → `/ux-audit`
- If the surface needs to be built fresh → `/ux-design`
- If the audience is shaky and needs more grounding → `/ux-research`
- If the user is unsure → `/ux-next` (let the conductor pick)

Print the next-prompt block like this:

```
─── next ───
Recommended: <primary next command based on framing>
Other moves: <2-3 alternatives>
             /ux-next   (let me decide)
```

## Hard rules

- Never accept "everyone," "users," or "people" as audience without a qualifying segment. Push back specifically.
- Never accept "make it better," "improve UX," or "modernize" as outcome. Force a behavior-change statement.
- Never ask the four questions as four messages. One combined ask, or none if you can extract from input.
- Never write design or critique in this command. Framing only.
- Never skip writing `.ux/last-frame.json` — downstream commands depend on it.
- Never add emojis, decorative dividers beyond the `───` rule, or filler sentences.

## Failure modes

- **Question avalanche**: asking four separate questions instead of one combined ask. The user disengages.
- **Soft acceptance**: accepting "users" as audience because the user pushed back. Flag it as a soft field instead — be transparent that the framing is weaker than it should be.
- **Scope creep**: starting to design or critique mid-frame. Stop. Frame only. Hand off to `/ux-design` or `/ux-audit`.
- **State skip**: forgetting to write `.ux/last-frame.json`. Every downstream command silently degrades when this file is missing.
- **Over-formatting**: padding the output with prose. The framing block is four lines. Resist the urge to explain it.
