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

Lines containing the string `ux-lint-disable` are skipped — this allows surgical suppression on individual lines where the pattern is a true positive against intent (e.g., a legal-entity name that genuinely is "Acme" because Acme is a real party in a contract).

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
| `ux-lint-disable` on a matched line | Skip the match, do not record a finding |

### Working with the rules file

The rules file is human-editable markdown. To add a rule:

1. Pick the next available integer ID. Insert a new `#### N. Title` block at an appropriate section.
2. Write the prose `**Why it's bad**` explanation so future contributors understand the fingerprint, not just the regex.
3. Add one or more ` ```regex` fenced blocks containing PCRE patterns. Each block is treated as a separate detection pass on the same rule.
4. Test the regex against three positive and three negative examples. Tighten until positives match and negatives don't. PCRE features (lookaheads, non-capturing groups) are available — but a tighter regex is always preferable to a broad regex with lookarounds, since the fallback grep mode drops lookarounds.
5. Add the `**Severity**:`, `**Mode**:`, and `**Better alternative**:` lines. Reserve Critical for fingerprints any reviewer catches in seconds.
6. Optionally include `**Example bad**` and `**Example good**` fenced code blocks for documentation. The parser ignores everything that is not a ` ```regex` block, so non-regex fences do not interfere with detection.

To suppress a finding without editing the rules:

- **Per-line**: add a `ux-lint-disable` comment on the offending line. Use `ux-lint-disable rule-N` to document the specific rule being waived.
- **Per-file**: pass `--exclude` to the linter with that file's glob.
- **Project-wide**: pass `--disable <id>` for that rule ID.

To raise or lower the CI gate, pass `--fail-on critical` (looser) or `--fail-on medium` (stricter).

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
