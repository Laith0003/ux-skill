# Changelog

All notable changes to ux-skill are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this
project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.0.0-alpha.24] — 2026-05-28 (brand revert)

- Reverted the brand from "ux-god-skill" back to "ux-skill" (better SEO, more humble voice).
- Global rewrite across README.md, README.es.md, docs/compare.html, references/foundations/motion.md, references/foundations/color.md, references/laws/laws-of-ux.md, data/landing-patterns.json.
- Package names on PyPI/npm unchanged (`uxskill` — already published).
- GitHub repo unchanged (`Laith0003/ux-skill`).
- 60 tests still passing.

## [2.0.0-alpha.23] — 2026-05-28 (landing patterns + persist)

- New manifest: `data/landing-patterns.json` (24 entries across 7 categories — Hero, Features, Social Proof, Pricing, CTA, Footer, Navigation). 6 entries flagged `ai_slop_risk:high` as the "default AI" patterns.
- New module: `engine/persist/` — `save_master`, `save_page`, `load_master`, `list_pages` for writing `MASTER.md` + `pages/<name>.md` to user projects (Pro Max parity).
- CLI: `ux persist save / save-page / load / list` subcommands.
- Idempotency verified: same input produces same bytes.
- README.es.md landed (Spanish translation).

## [2.0.0-alpha.22] — 2026-05-28 (Awwwards + CLI flags)

- Star history badge + Discord badge in README hero.
- `--global` and `--offline` flags on `ux init` / `ux install` (Pro Max parity).
- Laws of UX source URLs — 30-row link index to lawsofux.com canonical cards.
- GSAP first-class — `--engine gsap` flag on `/ux-motion` + recommended-engines table.
- Color-discovery tools row in `references/foundations/color.md` (Huemint, Picular, Colourcode, Colir, Coolors, WebAIM, OKLCH, APCA).
- `physicallybased.info` cited as the honest PBR materials source.

## [2.0.0-alpha.21] — 2026-05-28 (massive README rewrite)

- README rewritten to 1181 lines (~72 KB) matching ui-ux-pro-max-skill's depth (~25 KB) and exceeding it.
- Every command documented with use / skip / example / output / chains-to.
- All 5 sub-agents, 11 manifests, 35 (now 52) anti-pattern rules, 72 brand specs itemized.
- 17-IDE installer table with detection signals.
- 8 concrete use cases with full code.

## [2.0.0-alpha.20] — 2026-05-28 (compare page scorecard)

- Compare page rewritten as a **master scorecard** — every plugin scored 1-5 on 10 dimensions, no empty cells. ux-skill scores 46/50; next-best (open-design) scores 30.
- Per-competitor head-to-head tables with REAL content in every cell (no "—" placeholders).
- Corrected: open-design DOES have per-brand DESIGN.md (as prose); the real differentiator is SHAPE (queryable JSON + regex linter), not presence.

## [2.0.0-alpha.16-19] — 2026-05-28 (blog + sitemap + facebook image)

- 5 SEO blog posts: vs-ui-ux-pro-max / anti-ai-slop-claude-skills / best-claude-code-design-skills-2026 / cursor-design-plugin / python-design-system-generator.
- Blog index page with brand-styled cards.
- `docs/sitemap.xml` + `docs/robots.txt`.
- Brand-matched Arabic Facebook image (1080x1080) at `docs/launch/social/facebook-ar.png`.

## [2.0.0-alpha.11-15] — 2026-05-28 (Phase 4 wiring)

- All 17 v1 commands wired to Python engine via Bash invocations.
- Generation commands call `recommender.recommend()` + `generator.generate()`.
- Quality commands shell to `engine.linter`.
- Workflow commands chain via `.ux/last-*.json` state files.
- LLM-judgment commands load structured data (UX laws, anti-patterns, brand specs) as grounding.

## [2.0.0-alpha.1-10] — 2026-05-27..28 (v2 foundation)

- Phase 1: 11 data manifests filled to 998 total entries (beating UI UX Pro Max's ~600).
- Phase 2: Python engine modules built (recommender, linter, discovery, generator, installer, cli).
- Phase 3: cross-IDE distribution shipped to PyPI (`pip install uxskill`) and npm (`npx uxskill@alpha`).
- 17-IDE installer (Claude Code, Cursor, Windsurf, Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer, Roo Cline).
- GitHub release v2.0.0-alpha.1 cut.

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
