---
description: Moved to /ux-design --extract-only --from-image. Alias kept until 4.1.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Bash(python3:*), Glob, Grep, Task
disable-model-invocation: true
---

# /ux-image-to-code (alias)

`/ux-image-to-code` moved to `/ux-design --extract-only --from-image` in 4.0: the image extraction. Drop `--extract-only` to go on and build from the image. This alias is removed in 4.1.

1. Tell the user in one line: "/ux-image-to-code is now /ux-design --extract-only --from-image. Running it."
2. Run `/ux-design --extract-only --from-image $ARGUMENTS`. Follow `commands/ux-design.md` in image mode, extraction only, with the same arguments, exactly as if the user had typed the new command. Flags may come before the path: `--from-image` takes the first argument that is not a flag as the image path, as the old command did.
