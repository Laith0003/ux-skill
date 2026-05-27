# Changelog

All notable changes to ux-skill are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this
project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased] — 2.0.0 Python pivot

### Architecture
- **Major:** Pivot from "markdown an LLM reads" to "queryable JSON + Python engine."
- New `engine/` Python package with `recommender`, `linter`, `discovery`,
  `generator`, `installer`, and `cli` modules.
- New `data/` directory holding 11 structured JSON manifests (replacing prose
  in `references/` for everything the engine queries).
- New `ux` / `uxskill` CLI: `ux init`, `ux install <ide>`, `ux recommend`,
  `ux lint`, `ux discover`, `ux generate`, `ux stats`.
- Cross-IDE distribution: `pip install uxskill` (Python) and `npx uxskill init`
  (Node wrapper that auto-bootstraps via pipx).
- 17 supported IDEs: Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI,
  Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby,
  Tabnine, CodeWhisperer, Roo Cline.

### Data targets (vs. UI UX Pro Max — for context, not citation)
- `styles.json`: 75+ entries (theirs: 67)
- `palettes.json`: 170+ entries (theirs: 161)
- `type-pairs.json`: 65+ entries (theirs: 57)
- `components.json`: 120+ entries (theirs: 0)
- `industries.json`: 170+ entries (theirs: 161)
- `chart-types.json`: 30+ entries (theirs: 25)
- `tech-stacks.json`: 20+ entries (theirs: 15)
- `ux-guidelines.json`: 110+ entries (theirs: 99)
- `motion-presets.json`: 50+ entries (theirs: 0) — moat
- `anti-patterns.json`: 30+ entries (theirs: 0) — moat
- `brands/*.json`: 72 entries (theirs: 0) — moat

### Engine flagship
- `engine.recommend(brief: Brief)` — 5-parallel-search reasoning engine.
  Industry → style → palette → type → motion → components, merged with
  always-on anti-pattern guardrails.

### Linter
- `bin/ux-lint.sh` (v1) is preserved as fallback.
- `engine.lint(paths)` is the Python port — same regex rules, sourced from
  `data/anti-patterns.json`, faster, extensible.

### Preserved from v1
- 18 markdown command files in `commands/` (Claude Code plugin spec).
- 5 sub-agent definitions in `agents/` (Claude Code plugin spec).
- 72 prose brand DESIGN.md files in `references/brands/` (source of truth;
  `data/brands/*.json` is the queryable projection).
- Demo HTML reference pages in `references/foundations/*.html`.

### Compatibility
- v1 install via `/plugin marketplace add Laith0003/ux-skill` and
  `/plugin install ux@ux-skill` continues to work for existing users.
- v2 adds the Python layer; commands fall back to the v1 prose-only behavior
  when the Python engine is not available.

---

## [1.5.3] — 2026-05-24

- Privacy policy added (`PRIVACY.md` + `docs/privacy.html`).
- Landing footer links to `/privacy.html`.
- Arabic Facebook social image added (`docs/launch/social/facebook-ar.png`).

## [1.5.2] — 2026-05-24

- Fix `plugin.json` schema — `repository` and `bugs` must be strings
  (Claude Code spec), not objects (npm style).

## [1.5.0] — 2026-05-23

- Landing v2 POP edition shipped.
- Anti-patterns reference set absorbed.
- Motion principles synthesized (37 from production design-engineering work).
- 72 brand DESIGN.md files absorbed.

## [1.0.0] — 2026-05-22

- Initial public release. 18 commands, 5 sub-agents, 30+ references,
  deterministic regex linter.
