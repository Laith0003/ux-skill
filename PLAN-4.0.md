# ux-skill 4.0: what is done and what is left

This file is the handoff for finishing 4.0 on `feat/4.0-foundations`. It is self-contained: a session that has only this repository can work from it. Delete it in the release commit.

## Where 4.0 stands

4.0 replaces the 3.x synthesizer output with a foundations engine:

- **Eight foundations plus imagery**: color, type, spacing, layout, radius, border, elevation, motion. Each runs from primitives to semantic roles across five mode axes, emits DTCG, and is checked by a WCAG gate.
- **Contracts**: component contracts in `engine/contracts/seed/`, plus a rule pack with decision records routed by `HISTORY.md`.
- **Importers** (`engine/io/`): CSS, DTCG, Tailwind, Markdown rule files and Figma variables. They feed a naming adapter (`mapping.json`), `scan`, and `system enhance --from`.
- **Writes and exporters**:
  - Every write goes through an intake step that backs up the client's files byte for byte and never overwrites a file the client owns.
  - Exporters: CSS, DTCG, Tailwind 4 and Figma variables, with apply and read scripts.
  - `system extend` adds an extension file beside a foreign system and never rewrites it.
  - Contract checking and 25 MCP tools sit on one shared command layer.
- **Retuned character**: every look is a continuous function of the axes, brand and brief, never a lookup by industry or keyword. That covers:
  - the display size (60 to 240px at 1440) and the phone display;
  - section gaps, measure, motion pacing (`motion.settle_ms`), and the roles `motion.state`, `motion.press.scale`, `motion.indicator` and `motion.arrive`;
  - dark weight compensation, ink-alpha lines, the colour budget, bands by energy;
  - a photo direction with grade-lock ranges, the bottom-anchored hero and the two-voice headline.
- **Lint and docs follow the engine**:
  - Lint rules judge values against the page's own token set when a system is present, and time motion from the declared curve.
  - `lint --render` checks the colour budget, the photo grade lock, accent grounds and moving content.
  - The docs state the engine's ranges, and no industry picks a look.

Last full run: 9,956 tests passed. The generated goldens in `tests/foundations/golden` were unchanged.

## Ground rules (every task)

- **Writing.**
  - No emojis.
  - No em dashes or en dashes, and no `--` as punctuation. CLI flags and CSS custom properties are fine.
  - New files are ASCII.
- **Errors.** Every error and finding names the input (file, line, field, token, role or flag) and the fix. An importer never guesses: it reads a value, or lists the entry under "Not read" and says how to write it.
- **Smart, never static.** A look is a continuous function of the axes, brand and brief. Never a table by industry, keyword or kind of business.
- **Photographs are required.**
  - A page uses photographs. When the client gives none, the skill sources them by the engine's photo direction (temperature, light, saturation, grain, mood, framing).
  - A brand's ban on a kind of photo narrows which kinds qualify; it never removes photos. Only a client system that forbids photography outright removes them, and the report says so.
  - Product interface fragments are extra imagery, never a replacement for photos.
- **WCAG** is cited only for what each criterion says:
  - 1.4.3: text 4.5:1. 1.4.6: 7:1. 1.4.11: non-text 3:1. 1.4.8: line spacing and measure.
  - 1.4.10: reflow at 320px. 2.2.2: pause, stop, hide. 2.3.3: animation from interactions.
  - 2.4.7: focus visible. 2.5.5: 44px targets (AAA). 2.5.8: 24px targets.
  - Our own floors are worded as ours.
- **An existing system is fixed input.** We read its names, durations and curves and never replace them. A foreign system is extended beside its source, never rewritten.
- **Determinism.** The same inputs give byte-identical output: no timestamps, fixed ordering.
- **No runtime dependencies.** `engine/io/` is standard library only. Python floor 3.10.
- **Public repo hygiene.**
  - No client names, vendor names or licensed text.
  - No private plan names, and no task, ruling or review ids in code, tests, comments, docs or commit messages.
  - `tests/foundations/test_no_licensed_text.py` and `tests/test_derived_text_rewritten.py` must stay green. `NOTICE` stays.
- **Goldens stay byte-identical** unless a task says otherwise. The check `git diff --stat <base> HEAD -- tests/foundations/golden` prints nothing.
- **TDD.**
  - Write the failing test first and run it.
  - Every lint change gets clean, dirty and probe-corpus cases, a decision record in `engine/rulepack` and a line in `HISTORY.md`.
  - Fixtures are invented systems.
- **Commits.**
  - Stage exact files, never `git add -A`.
  - Message bodies say what changed in plain words.
  - Trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev,render,mcp]'
python -m playwright install chromium
pytest -q
```

The render tests need Chromium. The gate render test runs only when `UXSKILL_GATE_PYTHON` points at a Python that has Playwright.

## Work left, in order

Work on a branch from `feat/4.0-foundations`. Open a PR per task into `feat/4.0-foundations`, and never into `main`. Run one review per task, and fix every finding with a test.

### 1. Close the lint gaps the last pass left

- **Display line-height floor.**
  - Add a rule that flags a display line height under the engine's floor. The floor falls from 1.12 to 0.92 as size and contrast rise, and Arabic display stays at least 0.15 above Latin.
  - When the page has a system, the rule flags only values outside its token set.
- **All-caps on a calm brand.** Capitals at display size pass today even on a calm system.
  - Emit a `type.capitals` signal (or an equivalent token) from character, continuous in energy and formality.
  - Have `all-caps-large` read it, so calm systems flag display capitals and loud ones allow them.
- **Page-family render test.** Build three inner pages (for example pricing, about and contact) in one run. Assert at 1440 and 390:
  - one header, one closing band and one footer instance;
  - no overflow;
  - one h1 per page.

### 2. The component layer

- **State bindings.**
  - Every contract with a hover, selected or pressed state binds transition duration and curve to `motion.state`.
  - `button`, `chip`, `selectable-row` and an interactive `card` variant bind `motion.press.scale` under pressed. The scale is exactly 1 under reduced motion; the contract accepts 0.95 to 1.
  - `select` and `nav` gain exit bindings on `motion.dismiss`.
  - A schema check in `engine/contracts/schema.py` fails a contract that declares a state and binds no transition. The error names the part, the state and the fix.
- **Shared indicator.** Nav, tabs, segmented controls and menu rows bind one indicator to `motion.indicator`. It fades in the first time, slides after that and snaps under reduced motion. Selection is still carried by `aria-current` or `aria-selected` plus a non-colour cue.
- **Hover-reveal lint.** `hover-only-reveal` (`engine/linter/structure.py`) passes only when the revealed control also:
  - shows on focus inside its container;
  - stays while a menu it owns is open (`aria-expanded="true"`);
  - is visible under `(hover: none)`.
- **Exit hygiene lint.** Flag a focusable element left at `opacity: 0` without a `visibility`, `inert` or `hidden` companion. Popovers keep their exit animation until it ends. The theme toggle suspends transitions for one frame.
- **States that name themselves.**
  - An action inside a repeated item carries the item in its accessible name. Three identical `aria-label="Save"` buttons produce a finding.
  - Disabled menu rows stay visible with a reason and `aria-disabled`.
  - A visited mark uses a glyph, not colour alone.
  - Async lists put loading in a polite live region and failure in an alert region.
- **Render interaction probe.** Add a second pass in `lint --render` that does not freeze motion, at 1280 and 390:
  - Tab through the first 30 focusables and assert a visible ring that no ancestor clips.
  - Hover and press each button, chip and card, sampling `transform`, `background-color` and `opacity` to compute the time to half travel.
  - Open each `aria-haspopup` control, press Escape, and assert focus returns to the trigger.
  - Repeat under reduced motion and assert identity press transforms and no infinite animation except progress.
  - Fixtures in `tests/test_lint_probes.py`: a clipped chip ring, `outline: none` with no replacement (2.4.7), focus dropped on `body` after Escape, `transition: all .5s ease-in-out` on hover, and an infinite shimmer under reduced motion.

### 3. The section layer

- **Section contracts.** Add a `section` category in `engine/contracts/schema.py`, with slots that take component contracts, and seeds in `engine/contracts/seed/sections/`. The set: hero, secondary hero, logo row, feature grid, bento, how it works, integrations, stats band, named quote, comparison, pricing, FAQ (wrap `faq-accordion`), CTA band and footer (wrap `site-footer`).
- **What each section holds:**
  - its job, one sentence saying what it must prove;
  - its parts;
  - variants named by what differs: media kind, alignment, density;
  - token-role bindings only, never values;
  - a proof requirement, so that with no real proof the section drops with its reason;
  - a phone recomposition rule, applied in order: drop decorative layers, fold side columns into the text stack, pair small items two to a row, turn three or more plans into a plan switcher with the recommended plan preselected, and recrop interface fragments instead of shrinking them.
- **Page sequences.** Every section in `data/page-sequences.json` gains a `contract` field, or is marked prose-only. The compositions in `references/surfaces/landing.md` point at the contracts instead of restating widths.
- **Tests:**
  - every seed validates;
  - every sequence section resolves;
  - a render test per contract at 1440 and 390 (no overflow, targets at least 24px, one h2);
  - a distinctness test: one contract built under five axis corners stays above the glance-distance floor in `engine/foundations/distinct.py`.

### 4. Importer gaps

- Figma: values in modes beyond the default are kept only as a note. Read them into the mode axes.
- Figma: reduced-motion twins never pair. Handle plain-number durations and extra path words.
- A line height written in px is refused. Read it against the style's px size.
- Markdown: a Definition and Avoid column pair is read as a mode axis. It is not one.
- Markdown: alias columns are dropped. Read them as aliases, and the error for a bad mode name names the fix.
- Bare numbers on size-like roles (container, radius, elevation) are read unitless with no note. Read them as px and add a note.

### 5. Leftovers from the write and export work

- An in-place `system extend` of our own system does not rebuild `art/` or `system-report.md`. Rebuild both.
- A second `system extend` into a different out folder is refused. Allow it, with the intake record kept per folder.
- The block-scalar reader (`engine/contracts/yamlite.py`): a whitespace-only line longer than the indentation in a `|` block loses its spaces. Match standard YAML.
- A project read as rtl through its pages carries two notes that disagree. Keep one. Also apply the pages rule to `--from` files with `--scan`.
- `detect`: say which value `primary` reports when the token file and the rendered page disagree.
- Keep one list of Tailwind 4 namespaces, shared by `tailwind_config` and `tailwind_out`. text-shadow is emitted; durations are reported as outside Tailwind's namespaces.
- Map `type.size-*` names to type roles.
- Tailwind's default spacing scale values (`px-6`, `inset-0`) are not missing tokens when a preset extends, rather than replaces, the spacing scale.

### 6. Punctuation pass on references/

The `references/` prose still carries em dashes on about 9,000 lines and `--` as punctuation on a few dozen. Replace each one with judgment (a period, comma, colon or parentheses, whichever reads right), and never touch code, flags or CSS custom properties. Then add a test that keeps the dashes out.

### 7. Release

- **Site.** Redesign the site for 4.0:
  - keep the cyan glow and remove the dot eyebrows;
  - correct the counts (`docs/mcp.html` and `docs/index.html` say 18 MCP tools; there are 25);
  - add the OG card;
  - delete the orphan pages `docs/home-v31-preview.html`, `docs/home-v31-scene.html` and `docs/index-classic.html`.
- **Gallery.** Rebuild the 160 brand systems in the foundations format. Every one passes the gate in every mode.
- **Docs.**
  - Update the README in all 17 locales.
  - Add a CHANGELOG entry with a migration guide from the 3.x token format and the system-pack DESIGN.md.
  - Package ux-skill as a skill for Figma's agent after checking its current skill format.
- **Dependencies.** Merge the minor Dependabot PRs once CI is green. Test the major bumps on this branch and merge only what passes.
- **Release checks**, written as committed scripts or tests:
  - 600 sampled briefs build with 0 failures;
  - every gallery and fixture system round-trips through DTCG, CSS, Tailwind and Figma with 0 mismatches;
  - the build digest is stable across `PYTHONHASHSEED` values;
  - the wheel contains `engine/io` and `engine/foundations` and nothing private.
- **Version.** Bump to 4.0.0 in `pyproject.toml`, `package.json` and `.claude-plugin/plugin.json`.
- **Maintainer steps.** These stay with the maintainer:
  - the private coverage check;
  - the merge to `main`;
  - the PyPI and npm publish, with his own tokens.
