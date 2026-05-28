# Changelog

All notable changes to ux-skill are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this
project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.0.0-alpha.83] — 2026-05-28 (anti-patterns 100 → 120 + sitewide stat refresh)

- **Round 6 anti-patterns**: +20 new deterministic rules. Total **120**.
  Mostly A11y (12) + Visual (4) + Motion (2). Severity: 2 critical, 10 high, 6 medium, 2 low.
  Highlights: `aria-live-polite-on-error`, `link-without-href`, `video-without-captions`,
  `autoplay-without-muted`, `marquee-tag`, `blink-tag`, `tabindex-positive`,
  `onclick-on-non-button`, `role-button-on-anchor-without-href`, `meta-refresh-redirect`.
- 80 files touched in the sitewide stat sweep (100→120 across hero copy, JSON-LD meta,
  OG meta, blog body text, table cells, badges, MASTER.md). Tests stay 75/75 passing.

## [2.0.0-alpha.82] — 2026-05-28 (GitHub Action workflow + PR/issue templates)

- New: `docs/install/ux-lint-on-pr.yml.txt` — drop-in GitHub Actions workflow that
  runs `ux lint` on every PR, posts findings as a comment, fails the build on
  Critical/High. Couldn't push the .yml directly due to OAuth scope; saved as
  paste-able .txt for the Actions web UI path.
- New: `.github/PULL_REQUEST_TEMPLATE.md` + `.github/ISSUE_TEMPLATE/bug.md`.
- Repo description + 20 GitHub topics updated (anti-ai-slop, claude-code, cursor,
  windsurf, vibe-coding, ai-design, mcp, design-intelligence, etc).
- README.id (Indonesian) + README.pt-BR (Portuguese, Brazil) shipped.

## [2.0.0-alpha.79–81] — 2026-05-28 (multilingual blog round 1 + Italian README)

- 6 new SEO blog posts (3 English + 3 Asian/Pacific): `vibe-coding-design-system`,
  `ai-built-website-no-slop`, `anti-slop-cli-vibe-coders`, `ja/vibe-coding-design`,
  `zh-CN/vibe-coding-shipping-real-design`, `ko/ai-coding-design-rules`.
  All 0 critical / 0 high lint. Sitemap + blog index + add-related-reads.py updated.
- README.it (Italian) translation landed.
- zh-CN/vibe-coding post in Simplified Chinese (1100+ words, emerald scene-accent).

## [2.0.0-alpha.77–78] — 2026-05-28 (full theme audit + triple-rail brand carousel)

- **Theme audit**: scripts/force-dark-theme.py runs a deterministic find-replace on
  CSS token values (no agent guesswork) — converted 79 of 94 HTML files from
  cream+coral+Cormorant to dark Saturated Cinema in one pass.
- **Skip-link removed sitewide** (scripts/strip-skip-link.py, 64 files touched).
- **Terminal screenshots removed** from the homepage gallery section per user
  feedback ("So much terminal screenshots people care to see real things").
  Section 05·5 now ships 3 figures: Cursor + Claude Code + brand mosaic.
- **Triple-rail brand carousel**: replaced the single drag-rail with 3 horizontal
  rows scrolling in opposite directions (left/right/left at 80s/100s/120s speeds).
  All 110 brand cards distributed round-robin. Each row is drag-to-scrub on
  touch + mouse. Click any card → reskin the entire homepage in that brand's voice
  for 6 seconds via :root CSS variable swap. 14 brands have full BRAND_SPECIMENS
  data for rich reskin; the other 96 do a "lite" scene-accent swap. Zero
  innerHTML — every node built via createElement/textContent for XSS safety.

## [2.0.0-alpha.72–76] — 2026-05-28 (i18n + Asian languages + dark theme migration)

- **Mobile horizontal scroll killed** sitewide (scripts/inject-noscroll.py, 99 files).
- **17-language website** live at /zh-CN/, /zh-TW/, /ja/, /ko/, /hi/, /id/, /vi/,
  /th/, /ar/, /es/, /fr/, /de/, /pt-BR/, /ru/, /tr/, /it/. Each locale has a
  translated title + meta + nav pills + section eyebrows (NOTE: round-1 i18n was
  a half-job; comprehensive translation agent dispatched in alpha.78 to fix the
  English-leak bug across hero h1 + section titles + paragraph bodies).
- **Sitemap +16 locale URLs** for hreflang SEO.
- **Compare/About/FAQ/Roadmap/MCP/Privacy/Commands** migrated to dark Saturated Cinema.
- **All 20 blog posts** migrated to dark Saturated Cinema by 2 parallel agents.
- **README in 6 languages confirmed consistent on 100/110** (en, ar, es, zh, fr, de).
- **ux-god regression cleaned** out of README.ar.md (17 instances) and README.zh.md.

## [2.0.0-alpha.66–71] — 2026-05-28 (photos, logos, brands 110, hero video then removed)

- **Photos shipped**: 6 generated showcase PNGs (Pillow-rendered) in
  docs/screenshots/ — hero canvas, terminal-ux-recommend, terminal-ux-lint,
  Cursor IDE mockup, Claude Code session, brand mosaic.
- **SVG brand logos**: 25 simpleicons.org CC0 logos in docs/logos/. Brand gallery
  now renders real marks for 23 of 25 brands; styled wordmark fallback for clay/cursor.
- **131 brand specs** confirmed (anthropic, openai, perplexity, modal, railway,
  fly-io, retool, fivetran, dbt, snowflake, apple-music, instagram, tiktok,
  economist, wsj, dezeen, n26, robinhood — 18 added in round 5).
- **Hero video built then removed** at user request — autoplay didn't fire on
  iOS, browser showed play icon, the baked-in text overlapped the hero copy.
  Restored canvas-only flow field.
- **Scroll-pinned cinema** via `animation-timeline: view()` on screenshot gallery.
- **Editorial parallax section** added — 4 CC0 photos from picsum.photos with
  full-bleed parallax backgrounds + display-face quotes.

## [2.0.0-alpha.63] — 2026-05-28 (stats refresh — 100 rules / 92 brands)

- Round 5 anti-patterns landed at 100. Every reference to 120 anti-pattern rules / 85-rule linter / 85 deterministic rules across the site swept to 100 (42 files touched: 21 docs + 21 landing, plus README.md and command markdown).

## [2.0.0-alpha.62] — 2026-05-28 (anti-patterns 85 → 100)

- **+15 new deterministic regex rules** across A11y (6), Typography (2), Layout (2), Quality (2), Performance (2), Motion (1). Highlights: `overflow-hidden-on-html` (high), `lang-attribute-missing` (high), `cursor-not-allowed-no-visual` (high), `pointer-events-none-on-link` (high), `font-weight-numeric-100-or-900-on-body` (high), `event-listener-no-passive-on-scroll`, `image-format-jpg-no-webp-avif`, `transition-duration-500ms-or-longer`.
- The agent dropped 9 candidates: 6 duplicates of existing rules (viewport-no-zoom, img-no-dimensions, arbitrary-z-index-9999, h-screen-no-dvh-fallback, console-log-leak, target-blank-no-noopener) and 3 that required surrounding-context regex can't see.
- Total: **4 critical / 33 high / 42 medium / 21 low.** Demo file findings: 115 → 144.

## [2.0.0-alpha.61] — 2026-05-28 (CI green on Python 3.9)

- **Bug:** `python-tests (3.9)` matrix entry red on every push. Install step failed with `ERROR: Could not find a version that satisfies the requirement mcp>=1.0`.
- **Root cause:** `mcp>=1.0` listed unconditionally in `[project.optional-dependencies]` for both `mcp` and `dev` extras. The `mcp` package on PyPI requires Python ≥3.10, so pip on 3.9 couldn't resolve it.
- **Fix:** added a PEP 508 env marker — `mcp>=1.0; python_version >= '3.10'`. Engine MCP module already uses graceful try/except with `MCP_AVAILABLE` flag; test_mcp.py passes without the package on 3.9. Verified locally on Python 3.9.6 and via CI on the next push.

## [2.0.0-alpha.60] — 2026-05-28 (launch pack)

- New artifact: `docs/launch-pack.md` — ready-to-post copy for HN Show HN, Product Hunt, Reddit (r/ClaudeAI, r/cursor, r/programming), X/Twitter, LinkedIn, Discord. Per-platform tone-tuning, post-launch monitoring checklist, "what NOT to post" list.

## [2.0.0-alpha.59] — 2026-05-28 (README stat refresh)

- README.md stats updated to current numbers (85 → 100 in next ship; 72 → 92 brand specs). Shield badge `anti--patterns-51` bumped to `anti--patterns-85` then to `100` in alpha.63.

## [2.0.0-alpha.58] — 2026-05-28 (German README)

- Translation agent shipped README.de.md (1214 lines, native German). All 6 README files (en, ar, es, zh, fr, de) share the same 6-language picker with the current language bolded.
- Round-4 blog posts stat-snapshot bug: agent used '68 anti-patterns' / '93 brand specs' / '959 entries' from when it started; swept to current numbers.

## [2.0.0-alpha.53–57] — 2026-05-28

- alpha.57: 6 new OG images (zed, github-copilot, jetbrains, ai-design-system-cli, claude-desktop-mcp, commands).
- alpha.56: round-4 SEO blogs complete (5/5 IDE-specific posts shipped).
- alpha.55: rebuild commands.html with refreshed descriptions.
- alpha.54: refresh commands/*.md stat references.
- alpha.53: French README shipped (en, ar, es, zh, fr — de pending).

## [2.0.0-alpha.52] — 2026-05-28 (register landing-patterns in MANIFESTS)

- Round-3 manifest landing-patterns was authored but never wired into `engine/data_loader.py:MANIFESTS` — `ux stats` and the MCP `ux_landing_patterns` tool couldn't see it. Added. test_manifest_list_canonical now expects 11 manifests.

## [2.0.0-alpha.51] — 2026-05-28 (commands page + landing-patterns 40 + round-4 blogs)

- New page: `docs/commands.html` — reference for all 23 slash commands, with ItemList + BreadcrumbList JSON-LD, quick TOC, and source links. Lints clean.
- landing-patterns 24 → 40 (16 new patterns + 2 new categories: Trust, Onboarding).
- 2 round-4 blog posts landed (github-copilot-design-rules, zed-design-plugin).

## [2.0.0-alpha.45] — 2026-05-28 (stats refresh — 85 / 92)

- Homepage copy + JSON-LD + meta synced to the live numbers: **120 anti-pattern rules** (was 68), **92 brand specs** (was 72). Brand-gallery section title now reads "92 design languages. Each in its own voice." Linter section title now reads "85 regex rules. Run before commit."
- 0 critical / 0 high / 32 medium / 3 low lint findings on the homepage — still passes the success gate.

## [2.0.0-alpha.44] — 2026-05-28 (homepage v3 + OG images + antipat 68→85)

- **Homepage v3 — Saturated Cinema.** Replaces the rejected v2 Dark Editorial Cinema. Canvas `#07080a`, Bricolage Grotesque variable display (NOT Inter, NOT Cormorant), Inter for body, JetBrains Mono for mono. **Zero yellow/amber/gold/mustard/ochre/cream/coral/Cormorant anywhere.** Each section ships its own `--scene-accent` (cyan / pink / indigo / teal) — color comes from media, never a single accent.
- **All 4 media types:** (a) animated terminal sessions in the hero + linter scenes, (b) brand wordmark gallery (18 brands cycling, each in its own typeface), (c) device mockups (Cursor / Claude Code / Windsurf), (d) abstract Canvas generative scene break.
- **Anti-patterns 68 → 85.** 17 new rules across A11y (3, including 1 critical `aria-hidden-on-interactive`), Visual (4), Layout (3), Motion (2), Typography (2), Content (2), Quality (1). +24% catch-rate delta on the demo files (115 → 143 findings).
- **OG images.** 22 per-page PNGs at 1200×630 generated by `scripts/generate-og-images.py`; wired into every docs/ + landing/ page via `og:image` + `twitter:image` meta (script: `scripts/wire-og-images.py`).
- a11y: 97 references to aria-/focus-visible/prefers-reduced-motion on the homepage. Skip-to-content link. Reduced-motion fallback renders the terminal session statically.

## [2.0.0-alpha.43] — 2026-05-28 (docs↔landing parity sync + brand index → 92)

- Brand expansion landed: `_index.json` reflects 92 brands (was 72). Schema 1.0, version 2.1.0. 20 new specs: aesop, allbirds, atlantic, bloomberg, brex, datadog, glossier, hims-hers, honeycomb, mercury, monzo, neon, nytimes, patagonia, pitchfork, plaid, ramp, render, sourcegraph, substack.
- Sync: 9 blog posts + compare + mcp had docs↔landing divergence (docs/ had JSON-LD, OG meta, related-reads that landing/ didn't). Synced docs→landing — now byte-identical across both trees.

## [2.0.0-alpha.42] — 2026-05-28 (internal linking sweep)

- 'Related reads' block injected before the footer of every blog post via `scripts/add-related-reads.py`. Each post links to 4 topic-adjacent posts. Idempotent re-run.
- Sitemap +5 new blog URLs. Brand specs hit 92 (bloomberg added).

## [2.0.0-alpha.41] — 2026-05-28 (brands 81→91 + 3 SEO blogs)

- +10 brand specs (atlantic, brex, mercury, monzo, nytimes, pitchfork, plaid, ramp, substack, aesop JSON). Brand count: 91/92.
- 3 new SEO posts: dogfooding-design-engine, mcp-server-design-intelligence, motion-presets-framer-gsap-css.
- Blog index rewritten — 13 posts total, categories tagged.

## [2.0.0-alpha.40] — 2026-05-28 (JSON-LD structured data)

- Adds schema.org JSON-LD to every docs page missing it: 5 blog posts → BlogPosting; docs/blog/index.html → Blog; docs/compare.html → SoftwareApplication + AggregateRating; docs/mcp.html → SoftwareApplication with full featureList. Unlocks Google rich-result eligibility.

## [2.0.0-alpha.39] — 2026-05-28 (recommender forbidden-bypass fix)

- Bug: in palette and type-pair lanes, sort key `(is_compatible, score)` let a forbidden-but-compatible entry rank above a clean-but-not-compatible one — `True > False` outranked the -100 penalty.
- Fix: drop entries with score < -50 BEFORE applying the compatibility-first sort. Same shape across `_lane_palette`, `_lane_type`, `_lane_motion`, `_lane_components` (now accepts a Brief).
- 3 regression tests added. Full suite: **68 passing** (was 65).

## [2.0.0-alpha.38] — 2026-05-28 (anti-patterns 51 → 68 + brands +9)

- 17 new anti-pattern rules across Content, Color, Visual, Layout, A11y, Motion, Performance. Severity split: 5 high, 9 medium, 3 low.
- 9 brand specs added (aesop, allbirds, datadog, glossier, hims-hers, honeycomb, neon, patagonia, render, sourcegraph).
- 2 new SEO posts: regex-linter-for-ai-coding, dark-editorial-cinema-design.

## [2.0.0-alpha.25] — 2026-05-28 (MCP server — the asymmetric move)

- **New module:** `engine/mcp/` — Model Context Protocol stdio server exposing the engine as 14 tools so any MCP-capable host (Claude Desktop, Cursor, Windsurf, generic agents) can call into the recommender, linter, persistence, and the 11 data manifests without installing the full plugin.
- **14 tools registered:** `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`.
- **New entry point:** `ux-mcp` (wired by `pyproject.toml` → `engine.mcp.server:run_server`).
- **Optional dependency:** `pip install 'uxskill[mcp]'` pulls in `mcp>=1.0`. Base install stays slim. Module imports cleanly without the transport library; `ux-mcp` fails fast with a clear install hint if it's missing.
- **Architecture:** transport split from handlers. Each tool is a pure `dict -> dict` Python function; the stdio wrapper is a thin async layer. Tests exercise handlers directly — no event loop, no subprocess plumbing.
- **Asymmetric position:** none of the top 8 Claude UX skills (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) ship an MCP server. They are locked inside Claude Code's plugin runtime. ux-skill is now reachable from any MCP host.
- New command file: `commands/ux-mcp.md`.
- New documentation page: `docs/mcp.html` (brand-matched to `compare.html`).
- New tests: `tests/test_mcp.py` (5 tests, all passing). Total suite: 65 passing.
- README hero TOC + new "MCP server" section between brand specs and the 17-IDE installer.

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
