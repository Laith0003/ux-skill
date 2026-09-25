---
name: ux-init
description: Set up ux-skill in this project and print the data inventory. --stats prints only the inventory snapshot.
allowed-tools: Bash, Read, Write
disable-model-invocation: false
---

# /ux-init: bootstrap ux-skill

**One command. Three things.**

1. Detects which IDE you're using (`.claude/`, `.cursor/`, `.windsurf/`, etc.) and installs the right artifacts for it.
2. Verifies the Python engine is reachable.
3. Prints a stats snapshot showing what's in your data manifests.

`/ux-init` absorbs what used to be `/ux-stats`; that name still works as an alias until 4.1.

| Mode | Flag | What it does |
|---|---|---|
| setup (default) | none | Detect IDEs, install, verify the engine, print the stats snapshot |
| stats | `--stats` | Print only the stats snapshot. Installs nothing |

## Flags

| Flag | Mode | Meaning |
|---|---|---|
| `--stats` | stats | Skip setup; print the inventory snapshot only |
| `--decisions` | stats, setup | Add the decisions ledger summary to the snapshot |
| `--html` | stats, setup | Also write `.ux/stats.html`, a local dashboard of the snapshot |
| `--dry-run` | setup | Show what would be written without writing |
| `--root <path>` | setup | Project root (default `.`) |
| `--global` | setup | Install at the user level (`~/.config/ux-skill`) instead of the project root |
| `--offline` | setup | Skip any network calls; use only local manifests |
| `<ide>` | setup | Install for one IDE only (`ux install <ide>`) |

## When to use

- First time installing ux-skill in a new project.
- After cloning a project that uses ux-skill, to ensure your local install matches.
- After a `pip install --upgrade uxskill`, to wire new IDEs you've started using.
- `--stats`: verify the install (data files present, counts reasonable), audit before a release (no manifest dropped entries), or sanity-check after an upgrade.

## When to skip

- The project already has `.ux/installed.json` (you're set up). Use `--stats` if you only want the counts.
- You only want to install for a specific IDE: use `ux install <ide-name>` directly.

## How it runs

```bash
# Inside a Claude Code session, setup runs:
python3 -m engine.cli.main init
```

Behind the scenes:

1. `engine/installer/core.py:detect_ides()` walks the project root for signature files (`.claude/`, `.cursorrules`, `.windsurfrules`, etc.).
2. For each detected IDE, it writes the right artifact:
   - Claude Code: reuses existing `.claude-plugin/plugin.json`
   - Cursor: `.cursorrules`
   - Windsurf: `.windsurfrules`
   - GitHub Copilot: `.github/copilot-instructions.md`
   - Gemini CLI: `GEMINI.md`
   - Codex: `AGENTS.md`
   - And 11 more (see `engine/installer/core.py` for the full list)
3. Validates Python engine import works.
4. Runs the stats snapshot below to print the manifest counts.

### Stats snapshot (`--stats`)

```bash
python3 -m engine.cli.main stats
```

This calls `engine.data_loader.stats()`, which loads each manifest, reads the
`_meta.entries` count and the actual entry list length, and returns the
version plus one count per manifest:

```json
{
  "version": "4.0.0b1",
  "counts": {
    "styles": 84,
    "palettes": 176,
    "type-pairs": 70,
    "components": 148,
    "industries": 184,
    "chart-types": 35,
    "tech-stacks": 25,
    "ux-guidelines": 112,
    "motion-presets": 57,
    "anti-patterns": 153,
    "landing-patterns": 40,
    "brands": 160
  }
}
```

The numbers above are an example; the command prints what is on disk.

## Output (setup)

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

If you've installed via pip, you can run these directly outside Claude Code:

```bash
ux init                       # detect + install for all
ux init --dry-run             # show what would change without writing
ux install cursor             # install for one specific IDE
ux install --root=/path/to/project cursor
ux stats                      # pretty (rich) output by default
ux --no-pretty stats          # raw JSON, pipe-friendly
ux stats | jq '.counts'       # extract just counts
ux stats --decisions          # add the decisions ledger summary
ux stats --html               # write .ux/stats.html, a local dashboard
```

## Errors

- **No IDE detected**: falls back to `claude-code` install.
- **Python not found**: the installer tells the user to install via `pip install uxskill` or `pipx install uxskill`.
- **Permissions error**: check that the project root is writable.
- **`{"missing": true}` in a count**: the JSON file isn't present yet. Run `pip install --upgrade uxskill` or check the install path.
- **Counts of 0**: the JSON file exists but is empty. Open an issue at https://github.com/Laith0003/ux-skill/issues.

## What `/ux-init` is and isn't

- IS: A one-shot bootstrap for the engine. Idempotent. `--stats` installs nothing.
- IS NOT: A package installer. The engine itself comes via `pip install uxskill` or the Claude Code plugin marketplace; `/ux-init` just wires it into the current project.
