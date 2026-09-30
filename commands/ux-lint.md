---
description: Deterministic regex-based linter for AI fingerprints. No LLM, no API, no network. CI-friendly — exits non-zero on Critical / High findings. Rules sourced from references/foundations/anti-patterns.md. Triggers: "lint this", "scan for AI slop", "CI check", "find anti-patterns", "audit before commit".
allowed-tools: Read, Bash, Glob, Grep
disable-model-invocation: false
---

# /ux-lint

You are running the `/ux-lint` command from the `ux` plugin. The job is to run a fast, deterministic scan for the AI fingerprints catalogued in `references/foundations/anti-patterns.md` and report the findings — without making a single LLM call inside the lint pass itself.

This command complements the LLM-driven commands. `/ux-polish` uses your judgment on taste calls. `/ux-audit` walks six lenses with reasoning. `/ux-lint` runs the cheap, mechanical pass first — flagging the patterns that no taste call should waive — so the slower commands can focus on the genuinely subjective issues.

## When to use

Triggers: "lint this", "scan for AI slop", "CI check", "find anti-patterns", "audit before commit", "is there any slop in here", "pre-commit check", "fingerprint scan", "fast review".

Reach for `/ux-lint` when:

- Wiring a pre-commit hook that should block known fingerprints before they reach a PR.
- Wiring a CI gate that fails the build on any Critical or High finding.
- Doing a fast first pass on a large codebase, before paying the cost of `/ux-audit`.
- Triaging a file you just generated and want a quick "anything obvious?" check.
- Running on every save inside a watch loop.

Do NOT reach for `/ux-lint` when:

- The brief explicitly asks for taste-level judgment ("does this hero feel premium?"). The linter does not have taste — it has regex.
- The work is non-visual (a backend service, a CLI tool with no surfaces). The rules target UI artefacts.
- You want a fix loop. `/ux-lint` reports; it does not edit. Chain into `/ux-polish --fix` for that.

## Input

`/ux-lint` accepts any of:

- **A file path** — `src/components/Hero.tsx`. Only that file is scanned.
- **A directory path** — `src/`. The directory is walked recursively, with the standard exclusions (`node_modules`, `.git`, `dist`, `build`, `.next`, `vendor`, `public/build`, `.ux`).
- **"this project" or no argument** — the project root (current working directory) is scanned.

When no argument is passed the linter walks the project root and applies each rule to every file whose extension matches the rule's declared extension list. There is no project configuration required; defaults work out of the box.

### Flags

| Flag | Effect |
|---|---|
| `--rules <file>` | Override the rules file (default: `references/foundations/anti-patterns.md` shipped with the plugin) |
| `--include <glob>` | Only scan files matching this glob (repeatable) |
| `--exclude <glob>` | Skip files matching this glob (repeatable) |
| `--severity <level>` | Only show findings at or above this severity. One of `critical`, `high`, `medium`, `cosmetic` |
| `--fail-on <level>` | Exit non-zero only if a finding at or above this severity is found. Default: `high` |
| `--disable <id[,id...]>` | Skip these rule IDs entirely (e.g., `--disable 18,19` to skip Title Case and ALL CAPS rules) |
| `--ci` | Machine-readable TSV output on stdout, summary on stderr. Designed for CI logs and pipelines |
| `--list-rules` | Print every rule with its severity and exit (no scan) |
| `--help` | Print usage and exit |

## Process

When the user invokes `/ux-lint`:

### 1. Resolve the rules file

Confirm `references/foundations/anti-patterns.md` exists relative to the plugin root. If a `--rules` override was passed, use that path instead. The rules file is the source of truth — every rule the linter checks lives there, and editing it is the only way to change the linter's behavior.

Parse the file. Each rule is a markdown block built from a fixed set of pieces:

```
#### N. Short title

**Why it's bad**: prose explaining the failure mode.

**How to detect**:

` ``regex
<one regex per fenced block — PCRE features allowed>
` ``

(Optional additional regex blocks for the same rule. Each becomes a separate
scan pass; matches across blocks are deduplicated by file:line.)

**Better alternative**: One-line description of the correct replacement.

**Severity**: Critical | High | Medium | Cosmetic
**Mode**: brand-only | product-only | both

**Example bad**: optional code snippet.
**Example good**: optional code snippet.
```

The parser walks the file with a small state machine:

- A `#### N. Title` header opens a rule and flushes the previous rule's accumulated patterns into the cache.
- A ` ```regex` block enters pattern-capture mode; the closing ` ``` ` adds the captured pattern to the current rule's pattern list.
- `**Severity**:`, `**Mode**:`, and `**Better alternative**:` lines populate the rule's metadata.
- Other fenced blocks (` ```html`, ` ```js`, ` ```css`) are ignored — only ` ```regex` is treated as a pattern.
- The end of the file flushes the final rule.

This format lets the rules file double as human-readable documentation while remaining mechanically parseable. The parser is dumb on purpose — exact line prefixes, exact fence labels.

The patterns themselves use PCRE syntax — non-capturing groups (`(?:...)`), lookaheads (`(?!...)`), word-boundaries (`\b`), and unicode escapes (`\u{HEX}`). The script prefers `perl -nE` for matching because BSD grep on macOS does not support PCRE. When perl is unavailable the script falls back to `grep -E` with a best-effort syntax shim that strips lookarounds and converts non-capturing groups to capturing groups — patterns that depend on those features will broaden rather than match strictly.

### 2. Walk the target files

Default targets: all files in the current working directory whose extensions appear in any rule's `Extensions` list. Standard exclusions: `node_modules`, `.git`, `dist`, `build`, `.next`, `vendor`, `public/build`, `.ux`. Add custom exclusions via `--exclude`; restrict the scan further via `--include`.

The walker uses `find` with prune-style exclusions for portability across BSD (macOS) and GNU (Linux) coreutils.

### 3. Run each rule against each file

For every file, for every rule whose `Extensions` list matches the file's extension, run `LC_ALL=C grep -nE -- "$pattern" "$file"`. The `LC_ALL=C` forces byte-mode matching so high-byte character classes behave predictably regardless of the user's locale.

A line containing `ux-lint-disable` is skipped: every rule, or only the rule ids listed after it (`ux-lint-disable fake-name-john-doe`). `ux-lint-disable-next-line` does the same for the line below. This allows surgical suppression where the pattern is a true positive against intent (e.g., a legal-entity name that genuinely is "Acme" because Acme is a real party in a contract).

For a block of quoted text, such as a rule catalog or a "before" code sample, open a region with `<!-- ux-lint-off rule-a, rule-b -->` and close it with `<!-- ux-lint-on -->`. Only the named rules are waived, on every line from the opening comment to the closing one. A region must name at least one rule and must be closed. A region that names no rule, is never closed, or opens inside another waives nothing and is reported as a high finding (`lint-waiver-region`) on its opening line, with the fix. The JSON report counts waived lines in `waived_lines`.

If a rule's regex is malformed, the linter logs a warning to stderr, skips that rule, and continues. One broken rule does not fail the entire scan.

### 4. Group findings by severity

Findings are sorted Critical → High → Medium → Cosmetic, then by file path, then by line number. Counts per severity are surfaced in the header.

### 5. Emit the report

Default output is human-readable to stdout. `--ci` switches to TSV on stdout with a summary on stderr — designed for parsing in CI workflows or piping into another tool.

### 6. Exit code

- `0` — no findings at or above the `--fail-on` threshold (default: `high`).
- `1` — one or more findings at or above the `--fail-on` threshold.
- `2` — the rules file was missing or unreadable.
- `3` — invalid CLI usage.

`--fail-on critical` is the loosest setting (only Critical findings fail the build); `--fail-on cosmetic` is the strictest (everything fails). The default (`high`) is the recommended CI gate — Critical and High findings fail the build, Medium and Cosmetic surface as advisory.

## Output template

The command prints the following structure. Counts and rule numbers come from the actual scan; the layout is fixed.

```
─── /ux-lint report ───
Scanned: <N> files
Found:   <N> violations
Critical: <count>  High: <count>  Medium: <count>  Cosmetic: <count>

[CRITICAL] Rule 11 — Three equal cards in a row
  src/components/Hero.tsx:42  `<div className="grid grid-cols-3 gap-6">`
  Better: 2-col zig-zag or asymmetric bento (7/5 or 5/7 split)

[HIGH] Rule 6 — Inter as brand display face
  src/styles/globals.css:14  `--font-display: "Inter", ...`
  Better: Geist, Cabinet Grotesk, Satoshi, or system serif

... (one block per finding)

─── verdict ───
3 critical · 7 high · 12 medium · 0 cosmetic → CI exit code: 1 (fail-on: high)
Recommended next: /ux-polish --fix (LLM-driven, addresses both lintable and aesthetic findings)
```

In `--ci` mode the output is tab-separated:

```
severity<TAB>rule_id<TAB>title<TAB>file<TAB>line<TAB>matched<TAB>better
```

One row per finding on stdout. Summary on stderr in the form:
`ux-lint scanned N files, found M (critical=A high=B medium=C cosmetic=D)`.

## Implementation notes

**v2.0 — Python-first.** The linter has two implementations:

1. **`bin/ux-lint.py`** (preferred in v2) — Python script that reads rules from the structured `data/anti-patterns.json` manifest. Faster, extensible, identical regex semantics.
2. **`bin/ux-lint.sh`** (v1 fallback) — Bash + perl-PCRE, reads from `references/foundations/anti-patterns.md`. Kept for environments without Python.

The slash command itself is shallow — it just invokes one of the scripts and surfaces the output. There is no LLM call inside `/ux-lint`. The intelligence lives in the rules file; the script applies it.

### Dispatch order

Try Python first:

```
python3 <plugin-root>/bin/ux-lint.py [user-supplied args]
```

If Python is unavailable OR the engine package isn't importable, fall back to:

```
bash <plugin-root>/bin/ux-lint.sh [user-supplied args]
```

### Flag mapping (Python ↔ Bash)

| User-facing flag | Python | Bash |
|---|---|---|
| `--severity high src/` | `--threshold high src/` | `--severity high src/` |
| `--fail-on high` | `--threshold high` (default) | `--fail-on high` |
| `--json` | `--json` | `--ci` |

Pass through whatever flags the user named in their invocation, mapping the names through the table above when invoking Python.

### Exit codes

- 0 — no findings at or above the threshold
- 1 — findings at or above threshold (CI gate failure)
- 2 — rules file missing (Bash only)
- 3 — invalid CLI usage (Bash only)

If the script exits with code 2 or 3, surface the error to the user and stop — do not retry.

Do not paraphrase the script's output. The output is the contract — the report is designed to be the deliverable.

### Hard rules

- **Deterministic.** Same inputs always yield the same output. No randomness, no model temperature, no time-of-day variation.
- **No LLM call inside the linter.** The whole point of `/ux-lint` is the fast, mechanical pass. Adding judgment turns it back into `/ux-polish`.
- **CI-friendly.** The `--ci` flag produces machine-readable output. The exit code reflects the `--fail-on` threshold. Both are required for CI integration.
- **Configurable.** Accepts `--include`, `--exclude`, `--severity`, `--fail-on`, `--disable`, and an environment variable `UX_LINT_RULES` for the rules file path. No project file is required to run.
- **Portable.** Pure bash plus `awk`, `find`, `grep`, `sort`. No `jq` requirement. Works on BSD (macOS) and GNU (Linux) coreutils.

### Failure modes

| Condition | Behavior |
|---|---|
| No matching files found | Exit 0, print "no files matched" |
| Rules file missing | Exit 2, print "rules file not found" |
| Rules file unreadable | Exit 2, print "rules file not readable" |
| Regex error in a single rule | Skip that rule, log warning to stderr, continue |
| No rules parsed from the file | Exit 2, print "no rules parsed" |
| Bad CLI flag or missing value | Exit 3, print usage hint |
| `ux-lint-disable [ids]` on a matched line | Skip the match (all rules, or the listed ids), do not record a finding |
| Line inside a closed `ux-lint-off ids` region | Skip matches for the listed ids only |
| `ux-lint-off` that names no rule, is never closed, or opens inside another | Waive nothing; record a high `lint-waiver-region` finding on its line |

### Working with the rules file

The rules file is human-editable markdown. To add a rule:

1. Pick the next available integer ID. Insert a new `#### N. Title` block at an appropriate section.
2. Write the prose `**Why it's bad**` explanation so future contributors understand the fingerprint, not just the regex.
3. Add one or more ` ```regex` fenced blocks containing PCRE patterns. Each block is treated as a separate detection pass on the same rule.
4. Test the regex against three positive and three negative examples. Tighten until positives match and negatives don't. PCRE features (lookaheads, non-capturing groups) are available — but a tighter regex is always preferable to a broad regex with lookarounds, since the fallback grep mode drops lookarounds.
5. Add the `**Severity**:`, `**Mode**:`, and `**Better alternative**:` lines. Reserve Critical for fingerprints any reviewer catches in seconds.
6. Optionally include `**Example bad**` and `**Example good**` fenced code blocks for documentation. The parser ignores everything that is not a ` ```regex` block, so non-regex fences do not interfere with detection.

To suppress a finding without editing the rules:

- **Per-line**: add a `ux-lint-disable` comment on the offending line. Name the rule to waive only that rule: `/* ux-lint-disable arbitrary-z-index-9999 */`. Several ids can be listed, separated by commas.
- **Next line**: in JSX, where a trailing comment is awkward, put `{/* ux-lint-disable-next-line inline-style-attribute */}` on the line above.
- **Per-block**: wrap quoted text in `<!-- ux-lint-off rule-a, rule-b -->` ... `<!-- ux-lint-on -->`. Name every rule it waives; the region covers nothing else. A region that names no rule, or is never closed, waives nothing and is reported as `lint-waiver-region`.
- **Per-file** (shell linter `bin/ux-lint.sh` only): pass `--exclude` with that file's glob. The Python `uxskill lint` has no such flag; lint the paths you want instead.
- **Project-wide** (shell linter `bin/ux-lint.sh` only): pass `--disable <id>` for that rule ID. The Python `uxskill lint` has no such flag; use `ux-lint-disable` comments.

To raise or lower the CI gate, pass `--fail-on critical` (looser) or `--fail-on medium` (stricter).

## How a rule reads a file

The Python linter does not run a rule over the raw file. Each rule names the channel it judges in `detection.target` in `data/anti-patterns.json`, and every match is mapped back to the line and column of the original file.

| Channel | What it contains |
|---|---|
| `markup` | Tags, attributes and text, with comments blanked and `<style>` and `<script>` bodies removed. JSX `className` reads as `class`. The default. |
| `css` | Every CSS region: stylesheets, `<style>` bodies, `style` attributes, JSX `style` and `sx` objects (camelCase keys become kebab-case, numbers become px), Vue `:style` objects, CSS-in-JS templates. |
| `classes` | Every class list: `class` and `className` values, strings inside `cn()` or template literals, Vue `:class`, `@apply`, class-like string constants. |
| `text` | Visible copy: text nodes outside `<code>` and `<pre>`, copy attributes (`alt`, `title`, `aria-label`, `placeholder`), sentence-like strings in scripts. A phrase wrapped in quotation marks is a mention, not a use, and does not fire. |
| `code` | The file with comments and data URI payloads blanked. |
| `raw` | The file as written. |

So a CSS rule fires on `style={{ zIndex: 9999 }}` and on `className="z-[9999]"`, but not on a `zIndex={9999}` prop, a comment, a `data:` URI, or a sentence that mentions `z-index: 9999`.

Other detection fields: `also` adds more passes with their own pattern and target, `unless` waives a pass for the whole file when its pattern matches, `skip_inside` ignores matches inside the named elements (a `.jpg` fallback inside `<picture>`), and `post` names a structural check in `engine/linter/structure.py` that decides each hit on its own:

| Rule | What the `post` check decides |
|---|---|
| `placeholder-as-label` | The input passes only with a real accessible name: a `<label for>` that matches its id, a wrapping `<label>`, a non-empty `aria-label`, or `aria-labelledby` that points to another element with text. An id alone names nothing. A component such as `<Input>` passes with a non-empty `label` prop. |
| `outline-none-no-focus-visible` | Per rule block. A removal passes when it is limited to `:not(:focus-visible)`, when a `:focus-visible` or `:focus` rule that covers the same element (a bare `:focus-visible` or `*` covers every element; `:is()` and `:where()` are read per argument) draws a visible outline, box-shadow or border and wins on specificity, or when a `:focus-within` or `:has(:focus-visible)` rule on an ancestor of that element draws one. A ring inside a media query the removal is not in, a weaker outline against `!important`, or a ring on another element does not count. For inline styles only the element's own `ring`, `shadow` or `border` classes count. |
| `hover-only-card-actions` | Passes when the hiding sits inside `@media (hover: hover)`, or a focus rule on the same card reveals the actions too. |
| `imagery-mandatory-missing` | A landing page needs a photograph: a raster `<img>`, a `<picture>`, a `<video>` or a raster background that is not the logo. An SVG illustration, icons or the logo alone fire; an `<iframe>`, an element with `role="img"` that is not an SVG, and an SVG `<image>` of a raster file pass, since their content cannot be read. A page passes with none only when a `brand.md` beside it or above it forbids photography. Pages that are not landing pages are skipped: an app root with no text or `role="application"`; a docs page or app shell with a sidebar or table of contents beside the content; a page where one article, form, table, code listing, list or grid holds most of the main text; a layout template whose main is a slot the pages fill (`@yield`, `<slot>`, `{children}`) with no `h1`. A hero (an `h1` followed by a call to action) always marks a landing page, and a form that wraps several sections is the page itself. |
| `css-import-render-blocking` | Allows `@import` of a local stylesheet that only defines tokens: custom properties under any selector or `@media`, plus `color-scheme` and `@property` descriptors, which is what the engine's `tokens.css` holds. The file's content decides when it can be read; its name (`tokens.css`, `variables.css`) decides only when it cannot. Every other import still fires. |
| `decorative-accent-ruler` | Reads every build of a line, dash or dot beside an eyebrow: a `::before` or `::after` that draws a box, a border or a dash; a short thin pseudo-element line on any selector that is not a control or an icon; a side border or background line on the label; an empty `span` or `i`, or an SVG line or dot, first, last or next to the label; a dash typed at either end of its text. An eyebrow is read by its class (`eyebrow`, `kicker`, `overline`, `pretitle`, `section-label`) or by `uppercase` with a `tracking-` utility on an element a heading follows, never a table cell, link, button, label or list item. `hr`, table rules, card edges, full-width underlines and dividers (a `calc()` width with a percentage, a `var()` width named for a container), divider elements, list markers, icons and masked icon spans stay clean. |
| `screen-reader-only-without-class` | Judges the first link to `#main` or `#content` when it comes before the element with that id, whatever language its text is in. A class containing `sr-only`, `visually-hidden` or `screen-reader`, or a class named `skip`, `skip-link` or `skip-to-...`, passes. |
| `inline-svg-no-aria` | An SVG inside an `aria-hidden="true"` ancestor is hidden already. |
| `chrome-y-multi-stop-gradient` | Passes a scrim: every color stop is one color (transparent counts as its fade) at different alphas, as over a photograph. Two or more colors, or a stop it cannot read such as `var()`, still fire. |
| `loader-spinner-border-default` | Passes a spinner on a button (a `button`, `.btn` or `.button` selector, or `role="button"`) when the project's own button contract (in its rule pack) lists a spinner part for its loading state. Every selector of the rule must be a button's, so a list that also styles a page loader keeps the finding, and a project with no contract of its own keeps it too. |
| `nav-equal-hamburger-desktop` | Finds the menu button in any language: a menu word in its name, class, id or icon (English, Arabic and the other shipped languages), the hamburger glyph, or `aria-expanded` with `aria-controls` naming the site navigation; a button with other visible words (a desktop dropdown) is not one. It passes when anything hides the button or an ancestor at 1280px: the `hidden` attribute, an inline style, a Tailwind (`lg:hidden`, `hidden lg:flex`), Bootstrap (`d-lg-none`, `navbar-expand-lg`), Bulma or Foundation class, or any CSS rule with its media query, in a `<style>` or a local stylesheet the page links or imports. |
| `phone-field-requires-country-code` | Reads the pattern of a `type="tel"` input as the browser does (entities and a string literal in JSX resolved) and fires when it accepts none of a set of common local numbers (a leading zero, spaces, brackets, no country code) and does accept an international one. No pattern, a computed pattern, an optional plus or a pattern that takes a local number passes; a pattern that does not compile is read by its first token. |
| `one-action-several-labels` | Groups the calls to action in a file (a `button`, `role="button"`, or a link with a `btn`, `button` or `cta` class) by what they do: the same `href`, a trailing slash aside, or the same form by a button's `form` attribute. Fires on each one whose visible words differ from the first. Plain text links, icon-only controls, words filled in at run time, and `#`, `tel:` and `mailto:` links are not compared. |
| `display-bold-700`, `letterspacing-tracking-tight-display`, `hero-text-arbitrary-90px` | Read the page's own system: the custom properties the file defines, the local stylesheets it links and, for a stylesheet, the pages that load it. A weight, size or tracking value the system has passes (tracking in `em` is compared in pixels at the rule's font size; the tracking rule needs both the tracking and the weight). With no system of that kind, the fixed thresholds hold. |
| `all-caps-large` | Passes a capitals display when the page's system has a capitals role (a custom property named with `caps`), the size is one of the system's two largest and the letter spacing is 0 or open. Body, subhead and tight-tracked capitals, and any page with no system, still fire. |
| `transition-duration-500ms-or-longer`, `animation-duration-too-long`, `timing-300ms-default` | Judge when the move answers, from its declared curve: a transition whose rule, or another rule for the same element, is a hover, focus, press or state is a response and reaches half its travel within 70ms and nine tenths within 220ms; any other transition and every animation is an entrance and reaches half within 140ms. A curve that is not declared, a `var()` the page does not define, `steps()` or `linear()` falls back to the nominal cap (500ms, 800ms, 300ms); an ease-in exit is held to the cap only. A duration the page's system defines passes with the system's curve or none. The transition rule reads durations of 400ms and up; the 300ms rule reads exactly 300ms, as a delay never. Tailwind `duration-*` classes read the curve from `ease-*` classes on the same element. |
| `three-equal-card-grid` | Fires only when every card holds just an icon, a title and a line or two of text: a card with its own image, video, figure or large SVG, or a list, table, form or quote, passes. A small SVG icon or an icon image under 100px is not media. |
| `grid-cols-3-1fr-default` | Finds the markup the rule styles, in the same file or a page that loads the stylesheet, and passes when each cell carries its own media or richer content. A stylesheet with no markup to read still fires. |
| `eyebrows-over-budget` | Counts the page's sections (every `<section>` not inside another) and its eyebrows (read as `decorative-accent-ruler` reads them). The allowance is the brand's share of the sections, rounded up: a sixth for a playful brand to a half for a formal one, the formality read back from the system's photo grade spread, a third when the page has no system. Eyebrows past the allowance fire; a page with fewer than three sections, a docs page or an app surface is not counted. |
| `layout-family-repeated` | Reads each section's tree of elements four levels deep: headings, media, links and paragraphs as kinds, a run of the same item as one, words ignored. The third section with the same tree and every one after it fire. A section of fewer than two levels is not compared. |
| `split-sections-in-a-row` | A split is a section that, past single wrappers, holds two parts: one with media and no heading, the other with a heading and no media. The third split in a row among sibling sections, and every one after it, fire. |
| `marquee-more-than-one` | Counts `<marquee>`, `data-marquee` and elements whose class names a marquee or ticker (a part such as `marquee__track` inside one is the same marquee). Every one after the first fires. |
| `text-ink-at-low-alpha` | Fires on a text `color` in a near-neutral ink (channels within 24 of each other) at an alpha under 0.7: `rgba()`, an eight- or four-digit hex, `color-mix()` with `transparent`, or a Tailwind ink with an opacity modifier (`text-black/50`, `text-gray-900/60`). It passes when the color over white (dark ink) or black (light ink) is a color the page's own tokens define. Background and border colors are not text. |
| `animating-layout-properties` | Passes a transition whose only layout property is `width` or `inline-size` on a moving indicator: a selector naming an indicator, underline, ink bar, highlight, thumb or selection, or an element with `position: absolute` or `fixed`. Any other size, position, margin or padding still fires. `grid-template-rows` on a disclosure is not read. |
| `infinite-animation-without-reduced-motion` | Passes an infinite animation that runs only inside `@media (prefers-reduced-motion: no-preference)`, one a reduced-motion query stops (`animation: none`, paused, one iteration or a near-zero duration on its selector, a selector it matches, or `*`), and a progress indicator (a selector naming a spinner, loader or progress). |

`.htm` files read as HTML, and `.svelte` files match every rule scoped to HTML or Vue.

### The render check

`uxskill lint --render` loads each HTML file in headless Chromium at 390, 430, 768 and 1280px and adds what only the rendered page shows. Two rules measure layout at every width; the rest measure once, at 1280px, or on pages that are not frozen:

| Rule | What it measures |
|---|---|
| `centered-text-off-center` | Centered text in a box that sits against one edge of its container. |
| `horizontal-overflow` | The page scrolls sideways; names up to three elements that reach past the viewport. |
| `color-over-budget` | Only on a page that carries `--color-budget-chromatic`. The share of text characters in a chromatic color (OKLCH chroma 0.08 and up), and the share of the interface area (the page less images, video, canvas, SVG and background pictures) filled in one, painted on a 16px grid in document order. Text over `color.budget.chromatic`, or fill over it plus `color.budget.bands`, fires, with two points of slack. Colors of custom properties named for a status are left out. |
| `photo-grade-off` | Only on a page that carries the `--imagery-photo-*` tokens. Every raster image and background at least 120px on each side that is not a logo is measured for its mean L*, b* and C*; each must sit within the grade lock's spread of the page's mean, and the page's mean within the direction's ranges (`imagery.grade_problems`). |
| `accent-text-low-contrast` | Text in a color (OKLCH chroma 0.04 and up) against the ground under it, the backgrounds composited on white: under 4.5:1 fires, once per color and ground. Text over a picture, a gradient or an overlay beside media is left to the scrim check. |
| `infinite-animation-under-reduced-motion` | With reduced motion set, any animation that runs forever and is not a progress indicator. |
| `moving-content-without-pause` | With no motion preference, any animation that runs on its own for more than five seconds beside other content, when the page has no control that pauses it: a button or toggle named pause, stop or play, or one whose `aria-controls` names the moving region. |

When the project holds a client's own design system, the files that make it up are linted and listed apart under `system` in the JSON, with their own score. They are the client's fixed input, so their findings never lower the page's score or trip the exit code. A file counts only when all of these hold: `ux system detect` reports it as a token source, a token file, built output, a foundation stylesheet or a hand-written `MASTER.md` or `DESIGN.md`, or it sits in a system folder detect reports; the engine did not write it (no digest stamp, not listed in a `.uxskill/files.json` record); it is not an extension file (a name ending in `-ext` or `-extension`); and, for a stylesheet, it holds only token blocks. A page's own globals with a theme block and page rules, the extension file beside a system, and anything the engine wrote are always scored with the page. So is a client's foundation stylesheet that holds one base rule (a `body` or `html` rule) beside its tokens: its findings count toward the page, and moving that rule into a stylesheet of its own keeps the token file apart.

A stylesheet made mostly of custom-property definitions (at least three, and at least nine in ten of its declarations) is a token layer: the engine's `tokens.css`, or a client's own token files. Its definitions are judged only by rules marked `token_definitions` (a default shadcn palette, a zero-offset glow, a default font); a duration or an easing defined as a token is the design system's choice, not a finding. Its other lines, and a page's own stylesheet, keep every rule. Content decides, never the file name.

Two fixture sets keep the rules honest. `tests/lint_corpus/clean/` holds real-world UI files with no anti-patterns, and the test suite requires zero findings at medium or above on it. `tests/lint_corpus/dirty/` holds one file per rule, named after the rule id, and every rule must fire on its own file. A new rule needs both.

## Lint on every write

The plugin registers a `PostToolUse` hook (`bin/ux-lint-hook.py`, declared in `.claude-plugin/plugin.json`). After every `Write`, `Edit` or `MultiEdit` on a UI file (`.html`, `.htm`, `.css`, `.scss`, `.jsx`, `.tsx`, `.vue`, `.svelte`, `.astro`, `.blade.php`), it lints that one file and hands findings at medium severity and above back to the session, each with its `file:line:column`, rule id and fix.

- It never blocks the write. The tool has already run, the hook always exits 0, and any error inside it is swallowed.
- It is pure Python standard library. No Node, no binaries, no installed packages.
- It finishes in well under 500 ms on a 2,000-line file (`tests/test_lint_hook.py` checks this).
- After an `Edit` or `MultiEdit` it lists only findings on the lines the edit wrote, and counts the older ones, so the same finding is not repeated on every edit. A `Write` lists them all.
- A file over 1 MB is skipped, with a one-line note on stderr that names the file. Lint it by hand with `uxskill lint <file>`.
- If the linter cannot load (for example under a Python older than 3.10), it prints one line to stderr saying so instead of going quiet.

To turn it off, use either of these:

1. Set `UXSKILL_LINT_ON_WRITE=0` in the environment. For one project, add it to `.claude/settings.json`:

   ```json
   { "env": { "UXSKILL_LINT_ON_WRITE": "0" } }
   ```

2. Create an empty file at `.ux/lint-on-write.off` in the project root.

`"disableAllHooks": true` in settings also stops it, along with every other hook.

## Wiring into pre-commit hooks

For a Husky / lefthook / native-git pre-commit hook:

```
#!/usr/bin/env bash
# .git/hooks/pre-commit
bash <plugin-root>/bin/ux-lint.sh --fail-on high
```

The hook blocks the commit when any Critical or High violation appears. Set `--fail-on critical` to block only on the worst class.

## Wiring into CI

For GitHub Actions, GitLab CI, or any CI runner:

```
- name: ux-lint
  run: bash <plugin-root>/bin/ux-lint.sh --ci --fail-on high
```

The `--ci` flag emits a TSV on stdout that downstream steps can parse. The exit code is set by `--fail-on`.

For a soft-fail mode (advisory, never blocks):

```
- name: ux-lint (advisory)
  run: bash <plugin-root>/bin/ux-lint.sh --ci || true
```

The trailing `|| true` swallows the exit code while still emitting the findings to the build log.

## Next prompt

After `/ux-lint` reports findings, recommend the most useful next move:

- If Critical or High findings dominate: `/ux-polish --fix` — the polish command's fix loop handles the same patterns and applies edits.
- If the findings cluster around a specific lens (e.g., copy, motion): point to the matching command — `/ux-copy --fix`, `/ux-motion --fix`.
- If the findings are sparse and Cosmetic-only: ship it.

End every output with:

```
─── next ───
Recommended: /ux-polish --fix    (cosmetic + LLM-judged pass on the same findings)
Other moves: /ux-audit            (full 6-lens review for taste-level issues)
             /ux-fix              (apply findings as commits, severity-sorted)
             /ux-next             (let me decide)
```

The linter's job is to find what regex can find. The judgment-driven commands pick up where the linter stops.

## Cross-reference

- The rules live in `references/foundations/anti-patterns.md` — that's where edits land.
- The prose anti-pattern catalogue (with "do instead" pairs) lives in `references/styles/anti-slop.md` — that's where the rationale for each rule is documented.
- The polish command lives in `commands/ux-polish.md` — that's the LLM-driven counterpart.
- The audit command lives in `commands/ux-audit.md` — that's the full 6-lens reasoning pass.

The linter is the floor; the audit is the ceiling. Run the linter first, often. Run the audit when the linter is clean and the question is about taste.
