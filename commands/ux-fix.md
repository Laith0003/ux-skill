---
description: Opt-in fix loop. Reads the latest report from .ux/, validates working tree, and applies findings as atomic commits via the right sub-agents. Triggers on "fix the findings", "apply the fixes", or "run the fix loop".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(mkdir:*), Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git stash:*), Bash(git log:*), Bash(date:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-fix

You are running the `/ux-fix` command from the `ux` plugin. The job is to take a report already produced by another `ux-*` command, apply its findings as atomic commits via the right sub-agents, and re-verify by re-running the originating command.

## When to use

Triggers: "fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it".

Use after running `/ux-audit`, `/ux-copy`, `/ux-a11y`, `/ux-motion`, or `/ux-polish` and reviewing the findings. The user has decided to act; this command is the act.

Do not use without an existing report. If `.ux/` has no `last-*.json` file, return an error and direct the user to run an audit command first.

## Input

Optional: which report to act on (`--from audit | copy | a11y | motion | polish`). If unspecified, auto-detect by reading every `.ux/last-*.json` file and picking the most recent timestamp.

Optional: `--include-cosmetic` to include Cosmetic-severity findings (default skips them).

Optional: `--max <n>` to cap the number of fixes per run (default: all eligible findings).

## Process

### 1. Locate the source report

If `--from` is set, read `.ux/last-<name>.json` directly.

If not, list every `.ux/last-*.json`, parse timestamps, pick the most recent. Surface to the user which report is being acted on:

```
Acting on .ux/last-<name>.json (timestamp: <ISO>)
<n> findings — <Critical>/<High>/<Medium>/<Cosmetic>
```

If the latest report is older than 24 hours, warn the user — the surface may have changed since the report was generated. Ask for confirmation to proceed, or recommend re-running the originating command first.

### 2. Validate clean working tree

Run `git status --short`. If the tree is dirty:

1. Show the user what is dirty.
2. Offer three options:
   - **Commit** — let the user commit the existing changes first before starting the fix loop.
   - **Stash** — `git stash push -m "ux-fix pre-loop stash"` and proceed; restore at the end.
   - **Abort** — exit without applying any fixes.
3. Wait for the user's choice. Do NOT proceed silently with a dirty tree.

If the project is not a git repo (the workspace root, for example), warn the user that atomic commits will not be possible and ask whether to proceed with edits only (no commits) or to abort. The Dot workspace root is NOT a git repo — fixes there must be made inside a subproject like `reward-loyalty/` or `dot-design-system/`.

### 3. Plan the fixes

From the report's findings, build a fix queue:

1. Filter out Cosmetic unless `--include-cosmetic` is set.
2. Sort: Critical → High → Medium → (Cosmetic if included).
3. Apply `--max <n>` cap if set.

For each finding, classify the sub-agent based on the report's `category` field:

- `code` (or unspecified for `/ux-audit` code findings) → `frontend-engineer`
- `copy` → `copy-writer`
- `motion` → `motion-engineer`

Group findings by whether they touch the same file or component. Independent findings can be dispatched in parallel; co-located findings must be queued sequential to avoid merge conflicts.

### 4. Confirm with the user before dispatch

Show the planned queue:

```
─── fix plan ───
Source:     .ux/last-<name>.json
Findings:   <n> in scope (after filtering Cosmetic / applying --max)
Skipped:    <n> Cosmetic / <n> over --max cap

Critical:
  1. <finding title>   →   <sub-agent>
  2. <finding title>   →   <sub-agent>

High:
  3. <finding title>   →   <sub-agent>
  ...

Parallel batches: <n>    Sequential steps: <n>
```

Wait for the user's confirmation before dispatching. For copy fixes specifically, show the before/after diff inline so the user can veto specific rewrites — copy is taste, never apply silently.

### 5. Dispatch the agents

For each batch:

- **Parallel batch** (independent findings) — call multiple Task tools in a SINGLE message, one per finding. Each agent gets:
  - The finding's full payload (`title`, `evidence`, `fix`, plus any category-specific fields).
  - The relevant reference files (e.g., copy fixes get the voice rubric; motion fixes get the timing/easing rules).
  - An explicit instruction to make ONLY the fix described, commit atomically with a message linking the finding, and return success/failure.
- **Sequential step** (co-located findings) — dispatch one at a time, waiting for each agent to finish before dispatching the next.

After every fix:

- Verify the commit landed (`git log -1 --oneline`).
- Capture the commit SHA and the finding title.
- If the agent reported failure (could not fix, fix did not apply cleanly), capture the reason.

### 6. Re-verify

After all fixes are applied, re-run the originating command (`/ux-audit`, `/ux-copy`, etc.) on the same surface. Compare:

- Which findings cleared.
- Which findings remain.
- Which findings are new (regressions introduced by the fix loop).

Format the re-verification delta:

```
─── re-verification ───
Originating:  /ux-<name>
Re-ran:       <ISO timestamp>

Cleared:      <n> findings
Remaining:    <n> findings  (list them)
New:          <n> findings  (regressions — flag urgently)

Net severity: Critical <was→now> | High <was→now> | Medium <was→now> | Cosmetic <was→now>
```

If new findings emerged (regressions), flag them prominently. If Critical findings remain, recommend re-running `/ux-fix` after addressing root cause.

### 7. Restore stashed work

If the user chose Stash in step 2, run `git stash pop` and verify the tree is back to the pre-loop state plus the fix commits.

### 8. Format the final output

```
─── fix log ───
Source report:   .ux/last-<name>.json
Started:         <ISO>
Finished:        <ISO>

Applied:         <n> fixes
Skipped:         <n> Cosmetic
Failed:          <n>  (list each with reason)

Commits:
  <SHA>  <finding title>
  <SHA>  <finding title>
  ...

─── re-verification ───
<from step 6>

─── next ───
<next-prompt block>
```

### 9. Persist state

Write `.ux/last-fix.json`:

```json
{
  "command": "ux-fix",
  "timestamp": "<ISO8601 of finish>",
  "source_report": ".ux/last-<name>.json",
  "started_at": "<ISO>",
  "finished_at": "<ISO>",
  "applied": [
    { "finding_title": "<>", "sub_agent": "frontend-engineer | copy-writer | motion-engineer", "commit_sha": "<>", "severity": "Critical | High | Medium | Cosmetic" }
  ],
  "skipped": [
    { "finding_title": "<>", "reason": "cosmetic | over_max | user_vetoed" }
  ],
  "failed": [
    { "finding_title": "<>", "reason": "<>" }
  ],
  "re_verification": {
    "originating_command": "/ux-<name>",
    "ran_at": "<ISO>",
    "cleared_count": <n>,
    "remaining_findings": [{ "title": "<>", "severity": "<>" }],
    "new_findings": [{ "title": "<>", "severity": "<>" }]
  }
}
```

## Output

The fix-plan confirmation, the running log of dispatched agents and commits, the re-verification delta, and the next-prompt block.

## State persisted

- `.ux/last-fix.json` — keys: `command`, `timestamp`, `source_report`, `started_at`, `finished_at`, `applied` (array of `{finding_title, sub_agent, commit_sha, severity}`), `skipped` (array of `{finding_title, reason}`), `failed` (array of `{finding_title, reason}`), `re_verification` (object).

## Next prompt

Routing based on re-verification:

- New findings (regressions) emerged → recommend `/ux-audit` (full re-audit to catch what the narrow check missed).
- Critical findings remain → recommend `/ux-fix --from <same>` again after addressing root cause.
- All findings cleared → recommend `/ux-next` or a complementary command (`/ux-a11y` after `/ux-audit`, etc.).
- Mostly cleared but Cosmetic skipped → recommend `/ux-fix --include-cosmetic`.

Print:

```
─── next ───
Recommended: <command based on the above>
Other moves: /ux-audit          (full re-verification)
             /ux-next           (let me decide)
```

## Hard rules

- Never start the fix loop with a dirty tree. Commit, stash, or abort — explicit user choice required.
- Never auto-apply copy fixes without showing the before/after diff to the user. Copy is taste; require explicit go.
- Never skip the re-verification step. The user needs to see whether the fixes worked AND whether they introduced regressions.
- Never dispatch the wrong sub-agent — frontend-engineer for code, copy-writer for copy, motion-engineer for motion. Each agent has constraints the others do not.
- Never dispatch parallel agents that touch the same file. Queue them sequential.
- Never proceed if the source report is older than 24 hours without explicit user confirmation. The surface may have changed.
- Never claim a fix succeeded without verifying the commit landed AND the finding cleared on re-verification.

## Failure modes

- **Dirty-tree disaster**: starting the loop with uncommitted work, then losing it to a sub-agent's branch switch. Always commit/stash/abort first.
- **Silent copy rewrites**: applying copy fixes without showing diffs. The user vetoes after the fact and has to revert.
- **No re-verification**: declaring "done" without re-running the source command. The user has no way to know whether the fix loop worked.
- **Regression blindness**: clearing 5 findings but introducing 3 new ones, then reporting success. Flag new findings urgently.
- **Wrong agent dispatch**: sending a copy finding to `frontend-engineer`. The agent does the wrong job.
- **Parallel-batch collision**: dispatching two fixes to the same file in parallel; second commit fails or stomps the first. Always check file overlap before parallelizing.
- **Stale-report acting**: applying yesterday's audit to today's surface. Always check the timestamp; warn if > 24h.
