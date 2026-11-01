---
description: Moved to /ux-init --stats. Alias kept until 4.1.
allowed-tools: Bash, Read, Write
disable-model-invocation: true
---

# /ux-stats (alias)

`/ux-stats` moved to `/ux-init --stats` in 4.0: the data inventory snapshot. This alias is removed in 4.1.

1. Tell the user in one line: "/ux-stats is now /ux-init --stats. Running it."
2. Run `/ux-init --stats $ARGUMENTS`. Follow `commands/ux-init.md` in stats mode, with the same arguments, exactly as if the user had typed the new command.
