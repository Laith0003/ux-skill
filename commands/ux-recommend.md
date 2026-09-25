---
description: Moved to /ux-discover --recommend. Alias kept until 4.1.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
disable-model-invocation: true
---

# /ux-recommend (alias)

`/ux-recommend` moved to `/ux-discover --recommend` in 4.0: the recommender. The MCP tool `ux_recommend` is unchanged. This alias is removed in 4.1.

1. Tell the user in one line: "/ux-recommend is now /ux-discover --recommend. Running it."
2. Run `/ux-discover --recommend $ARGUMENTS`. Follow `commands/ux-discover.md` in recommend mode, with the same arguments, exactly as if the user had typed the new command.
