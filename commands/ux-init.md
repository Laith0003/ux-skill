---
name: ux-init
description: Bootstrap ux-skill v2 in the current project — detects your IDE, installs the right artifacts, validates that the Python engine works, and prints a stats snapshot of the 11 data manifests.
allowed-tools: Bash, Read, Write
disable-model-invocation: false
---

# /ux-init — bootstrap ux-skill v2

**One command. Three things.**

1. Detects which IDE you're using (`.claude/`, `.cursor/`, `.windsurf/`, etc.) and installs the right artifacts for it.
2. Verifies the Python engine is reachable.
3. Prints a stats snapshot showing what's in your data manifests.

## When to use

- First time installing ux-skill v2 in a new project.
- After cloning a project that uses ux-skill, to ensure your local install matches.
- After a `pip install --upgrade uxskill`, to wire new IDEs you've started using.

## When to skip

- The project already has `.ux/installed.json` (you're set up).
- You only want to install for a specific IDE → use `ux install <ide-name>` directly.

## How it runs

```bash
# Inside a Claude Code session, the command runs:
python3 -m engine.cli.main init
```

Behind the scenes:

1. `engine/installer/core.py:detect_ides()` walks the project root for signature files (`.claude/`, `.cursorrules`, `.windsurfrules`, etc.).
2. For each detected IDE, it writes the right artifact:
   - Claude Code → reuses existing `.claude-plugin/plugin.json`
   - Cursor → `.cursorrules`
   - Windsurf → `.windsurfrules`
   - GitHub Copilot → `.github/copilot-instructions.md`
   - Gemini CLI → `GEMINI.md`
   - Codex → `AGENTS.md`
   - And 11 more (see `engine/installer/core.py` for the full list)
3. Validates Python engine import works.
4. Runs `ux stats` to print the manifest counts.

## Output

```json
{
  "detected": ["claude-code", "cursor"],
  "installs": [
    {
      "target": "claude-code",
      "root": "/path/to/project",
      "files_written": [],
      "notes": ["Claude Code plugin already present"]
    },
    {
      "target": "cursor",
      "root": "/path/to/project",
      "files_written": [".cursorrules"]
    }
  ]
}
```

## Manual invocation

If you've installed via pip, you can run this directly outside Claude Code:

```bash
ux init                       # detect + install for all
ux init --dry-run             # show what would change without writing
ux install cursor             # install for one specific IDE
ux install --root=/path/to/project cursor
```

## Errors

- **No IDE detected** → falls back to `claude-code` install.
- **Python not found** → installer instructs the user to install via `pip install uxskill` or `pipx install uxskill`.
- **Permissions error** → check that the project root is writable.

## What `/ux-init` is and isn't

- IS: A one-shot bootstrap for the v2 engine. Idempotent.
- IS NOT: A package installer. The engine itself comes via `pip install uxskill` or the Claude Code plugin marketplace; `/ux-init` just wires it into the current project.
