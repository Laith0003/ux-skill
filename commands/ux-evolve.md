---
description: Moved to /ux-polish --loop-only --rounds 5. Alias kept until 4.1.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(mkdir:*), Bash(date:*), Bash(git status:*), Bash(uxskill:*), Bash(python3:*), Glob, Grep, Task, WebFetch
disable-model-invocation: true
---

# /ux-evolve (alias)

`/ux-evolve` moved to `/ux-polish --loop-only --rounds 5` in 4.0: the lint, fix, re-lint loop. `--max-rounds` is read as `--rounds`. As before, the loop replaces the original file when it clears the gate, now after a clean-tree check. This alias is removed in 4.1.

1. Tell the user in one line: "/ux-evolve is now /ux-polish --loop-only --rounds 5. Running it."
2. Run `/ux-polish --loop-only --rounds 5 $ARGUMENTS`. Follow `commands/ux-polish.md` in loop-only mode with the old five-round cap, with the same arguments, exactly as if the user had typed the new command.
