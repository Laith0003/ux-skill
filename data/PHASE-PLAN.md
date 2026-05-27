# v2.0.0 — Python Pivot Phase Plan

Living tracker for the architecture pivot from "markdown an LLM reads" to
"queryable data + Python engine."

## Targets vs. UI UX Pro Max

| Manifest | UI UX Pro Max | v2 Target | Status |
|---|---|---|---|
| `data/styles.json` | 67 | **75+** | in-progress |
| `data/palettes.json` | 161 | **170+** | in-progress |
| `data/type-pairs.json` | 57 | **65+** | in-progress |
| `data/components.json` | none | **120+** | in-progress |
| `data/industries.json` | 161 | **170+** | in-progress |
| `data/chart-types.json` | 25 | **30+** | in-progress |
| `data/tech-stacks.json` | 15 | **20+** | in-progress |
| `data/ux-guidelines.json` | 99 | **110+** | in-progress |
| `data/motion-presets.json` | none | **50+** ← moat | in-progress |
| `data/anti-patterns.json` | none | **30+** ← moat | in-progress |
| `data/brands/*.json` | none | **72** ← moat | in-progress |

## Engine targets

| Module | Purpose | Status |
|---|---|---|
| `engine/cli/main.py` | `ux` entry point | in-progress |
| `engine/recommender/core.py` | 5-parallel-search engine | in-progress |
| `engine/linter/core.py` | Port from `bin/ux-lint.sh` to Python | in-progress |
| `engine/discovery/core.py` | 10-field protocol enforcer | in-progress |
| `engine/generator/core.py` | Code generation from recommendations | in-progress |
| `engine/installer/core.py` | Multi-IDE installer | in-progress |

## Distribution targets

- `pip install uxskill` — Python-native install
- `npx uxskill init` — Node wrapper for IDE users without Python
- Auto-detect + install for: Claude Code, Cursor, Windsurf, GitHub Copilot,
  Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces,
  Tabby, Tabnine, CodeWhisperer, Roo Cline. (17 IDEs)

## Existing v1 surface — preservation rules

- All 18 `commands/*.md` files keep their frontmatter (Claude Code spec requirement).
- The 5 `agents/*.md` definitions stay (Claude Code spec).
- The 72 `references/brands/*-DESIGN.md` files stay as the source-of-truth prose;
  `data/brands/*.json` is the structured projection.
- `references/foundations/*.html` demo pages stay (live demos can't be JSON).
- `bin/ux-lint.sh` stays as the fallback until Python linter ships and is tested.

## Release plan

- **v2.0.0-alpha.1** (this commit) — schemas + skeleton + first batch of data
- **v2.0.0-alpha.2** — all 11 manifests filled to target numbers
- **v2.0.0-beta.1** — Python engine works end-to-end (`ux recommend` returns a system)
- **v2.0.0-rc.1** — multi-IDE installer works for top 5 IDEs
- **v2.0.0** — all 17 IDEs supported, docs updated, landing v3
