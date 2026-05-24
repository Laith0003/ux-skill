---
description: Workflow conductor. Reads the latest reports from .ux/ and names the highest-leverage next command. Triggers on "what should I do next", "what's the next move", "decide for me", "/ux-next".
allowed-tools: Read, Bash(ls:*), Bash(cat:*), Bash(find:*), Glob, Grep
disable-model-invocation: false
---

# /ux-next

You are running the `/ux-next` command from the `ux` plugin. The job is to read the project's accumulated UX state and tell the user the highest-leverage next move. You are a conductor, not a builder. Read-only.

## When to use

Triggers: "what should I do next", "what's the next move", "decide for me", "where do we go from here", "/ux-next", or any moment the user is between commands and asks for direction.

## Input

Optional — if the user names a specific report ("look at the a11y report"), focus there. Default: scan every `.ux/last-*.json` and decide.

## Process

### 1. Scan state

List `.ux/last-*.json` in the project root. If the directory does not exist, output the empty-state response (see Failure modes) and stop.

For each report, read it. Keep in memory:
- The command that produced it
- Timestamp
- Counts of unfixed Critical / High / Medium / Low findings
- Any explicit `ship_readiness` or `go_no_go` signal
- Any explicit `next_recommended` field

### 2. Score leverage

Score each report on three axes:

- **Severity** — sum of `(Critical * 4) + (High * 2) + (Medium * 1)` for unfixed findings
- **Recency** — newer reports score higher; reports older than 14 days are halved
- **Blocking signal** — if any report says "ship-readiness: no-go" or "blockers present," it gets +10

Pick the report with the highest leverage score. The next command is the one that directly addresses that report's blockers.

### 3. Map report to next command

| Source report | Highest-leverage next command |
|---|---|
| `last-a11y.json` with Critical findings | `/ux-a11y --fix` |
| `last-polish.json` with open items | `/ux-polish --apply` |
| `last-motion.json` flagging jank | `/ux-motion --fix` |
| `last-design.json` with no follow-up | `/ux-polish` then `/ux-a11y` |
| `last-research.json` with results pending | `/ux-research --synthesize` |
| `last-workshop.json` with a Game Plan | `/ux-design` (first MVP) or `/ux-frame` |
| `last-component.json` standalone | `/ux-component` (next one) or `/ux-design` (assemble) |
| `last-dashboard.json` with Critical | `/ux-polish` or `/ux-a11y` |
| `last-system.json` newly built | `/ux-component` (build against it) |
| `last-case-study.json` complete | `/ux-expert` (share) or done |
| Nothing actionable, all green | `/ux-next done` (call it shipped) |

### 4. Present the choice

Use this exact template:

```
─── ux state ───
Reports found:  <N>
Latest:         <command>  <timestamp>
Highest leverage: <report name>  (score: <n>)

─── evidence ───
<3-5 bullet lines citing specific findings/signals from the report that drove the recommendation>

─── recommendation ───
Next:       <command>
Why:        <one sentence — what this resolves>

─── alternatives ───
Option B:   <command>  — <one-line rationale>
Option C:   <command>  — <one-line rationale>
Escape:     nothing — call it done.  <one-line rationale if applicable>

─── decide ───
Pick one. I'll run it.
```

### 5. State

This command is read-only. Do not write to `.ux/`. The user re-runs `/ux-next` after any state change to get a fresh recommendation.

## Hard rules

- Read-only. Never modify `.ux/` files.
- Cite evidence. Every recommendation names the specific report and the specific finding driving it.
- Always offer an escape hatch. "Call it done" is a valid recommendation when reports are clean.
- Maximum three alternatives. Decision paralysis is failure.
- No emojis.

## Failure modes

- **Empty `.ux/` directory**: output `No prior UX state. Start with /ux-frame (lock the brief) or /ux-design (jump in).` Stop.
- **All reports older than 30 days**: warn the user that state is stale; recommend `/ux-frame` to re-baseline.
- **Conflicting signals across reports** (e.g. polish says ship-ready, a11y says no-go): surface the conflict explicitly. Recommend resolving a11y first — accessibility is a blocker.
- **Stale state vs. current code**: this command cannot detect drift between `.ux/` reports and the actual codebase. If the user has made changes since the last report, recommend re-running the relevant audit before acting.

## Next prompt

This command's next prompt is itself. After any state-changing action, `/ux-next` is the way back to the conductor.
