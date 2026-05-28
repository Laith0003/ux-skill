---
description: Workflow conductor. Reads the latest reports from .ux/ and names the highest-leverage next command. Triggers on "what should I do next", "what's the next move", "decide for me", "/ux-next". Use when asking "what should I do next", the user wants the conductor to pick the next command, post-audit / post-fix decision-making, navigating between commands. Skip when no prior reports exist in .ux/, the user has a specific next command in mind.
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

## Error Handling

| Error condition | Recovery |
|---|---|
| No prior reports in `.ux/` | Output the empty-state response and suggest `/ux-frame` or `/ux-design` as entry points |
| All reports older than 30 days | Warn that state is stale; recommend `/ux-frame` to re-baseline |
| Conflicting signals (polish says ship, a11y says no-go) | Surface the conflict explicitly; recommend resolving a11y first — accessibility is a blocker |
| `.ux/last-*.json` files are malformed or unreadable | Skip the unreadable file, surface the parse error in evidence, continue with the rest |
| User asks for a specific report and it doesn't exist | List the reports that do exist and let the user pick |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

## Next prompt

This command's next prompt is itself. After any state-changing action, `/ux-next` is the way back to the conductor.

---

## v2 Python integration

`/ux-next` reads the chain of state files in `.ux/` and suggests the next deterministic step based on what's been done.

### Read state to suggest the next move

```bash
python3 -c "
import json, os
def has(p): return os.path.exists(p)
state = {
    'discovery':       has('.ux/last-discovery.json'),
    'recommendation':  has('.ux/last-recommendation.json'),
    'generated':       has('.ux/generated/manifest.json'),
    'lint_report':     has('/tmp/ux-lint-report.json'),
}
print('STATE:', state)
suggestion = None
if not state['discovery']:
    suggestion = '/ux-frame  -- start by framing the problem (10-field intake)'
elif not state['recommendation']:
    suggestion = '/ux-recommend  -- get the merged design system'
elif not state['generated']:
    suggestion = '/ux-design [brief]  -- generate frontend code using the recommendation'
elif not state['lint_report']:
    suggestion = '/ux-lint .  -- run the anti-slop linter on the generated code'
else:
    suggestion = '/ux-fix .  -- apply linter findings if any, or /ux-polish for taste-level upgrades'
print()
print('NEXT:', suggestion)
"
```

### Suggest commands when state is partial or missing

The suggestion logic above maps state -> next command deterministically. The LLM can layer judgment on top (e.g., 'you also might want /ux-case-study to write this up') but the base suggestion comes from Python.

### Fallback

If state files are missing entirely, the answer is always `/ux-frame` first.
