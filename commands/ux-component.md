---
description: Moved to /ux-design --component. Alias kept until 4.1.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Bash(python3:*), Glob, Grep, Task
disable-model-invocation: true
---

# /ux-component (alias)

`/ux-component` moved to `/ux-design --component` in 4.0: one component. This alias is removed in 4.1.

1. Tell the user in one line: "/ux-component is now /ux-design --component. Running it."
2. Run `/ux-design --component $ARGUMENTS`. Follow `commands/ux-design.md` in component mode, with the same arguments, exactly as if the user had typed the new command.
