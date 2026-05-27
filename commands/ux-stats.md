---
name: ux-stats
description: Print a snapshot of what's in the ux-skill data manifests — counts per file, version info, total entries. Useful for verifying your install and seeing how much the engine has to work with.
allowed-tools: Bash
disable-model-invocation: false
---

# /ux-stats — show the data inventory

**One command. One snapshot.**

Prints the version, then the count of entries in each of the 11 data manifests:

```json
{
  "version": "2.0.0-alpha.1",
  "counts": {
    "styles": 84,
    "palettes": 176,
    "type-pairs": 70,
    "components": 148,
    "industries": 170,
    "chart-types": 35,
    "tech-stacks": 25,
    "ux-guidelines": 112,
    "motion-presets": 57,
    "anti-patterns": 35,
    "brands": 72
  }
}
```

## When to use

- Verify the install — confirm the data files are present and reasonable counts.
- Audit before a release — check no manifest has dropped entries.
- Quick sanity check after upgrading via `pip install --upgrade uxskill`.

## How it runs

```bash
python3 -m engine.cli.main stats
```

Behind the scenes this calls `engine.data_loader.stats()` which loads each
manifest, reads the `_meta.entries` count and the actual entry list length,
and returns the dictionary above.

## Manual invocation

```bash
ux stats                      # pretty (rich) output by default
ux --no-pretty stats          # raw JSON, pipe-friendly
ux stats | jq '.counts'       # extract just counts
```

## Errors

- **`{"missing": true}`** in a count → the JSON file isn't present yet. Run `pip install --upgrade uxskill` or check the install path.
- **Counts of 0** → the JSON file exists but is empty. Open an issue at https://github.com/Laith0003/ux-skill/issues.
