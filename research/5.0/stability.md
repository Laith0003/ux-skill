# ux-skill 5.0: running for months with no maintainer

Audit date: 2026-11-02. Repo state: main at 11b6345f (4.0.0), feat/4.1-stageshow at 7785d962.
Scope: what breaks when nobody is watching, the guard for each break, the checks that
find drift on a schedule, and the versioning promises a "stable for months" 5.0 can keep.

## 0. What the audit found, in one screen

Facts that drive the ranking below. Each has evidence in section 6.

1. 4.0.0 is tagged on GitHub but is not on PyPI or npm. PyPI and npm both still serve 3.2.0.
   Publishing is manual "with his own tokens" (PLAN-4.0.md:179). npm granular write tokens now
   expire in at most 90 days (7 by default) and classic tokens are gone, so a token-based
   publish cannot run unattended for months. Nothing publishes from CI today.
2. The release workflow tags and publishes a GitHub release on any push to main that carries
   new notes. It does not wait for the test workflow, so a red main can be released.
3. CI never installs Playwright. tests/test_render.py does `pytest.importorskip("playwright")`,
   so every render test is skipped in CI. The render check is the part of the product most
   exposed to drift (browser, Playwright, Chrome auto-update) and it has no CI coverage.
4. The MCP transport is never started in a test. tests/test_mcp.py builds the server object
   only. The MCP protocol moved to 2026-07-28, which drops the `initialize` handshake; a
   "modern only" client cannot talk to the mcp 1.x SDK this server is built on.
5. Dependabot has already opened a PR that widens `mcp` to `<3`
   (origin/dependabot/pip/mcp-gte-1.10-and-lt-3). mcp 2.x removed the decorators the server
   uses (`@server.list_tools()`), so merging it would break `ux-mcp` at startup.
6. Python 3.10 reached end of life on 2026-10-01. The CI matrix still tests 3.10 and stops at
   3.13; 3.14 (2025-10-07) and 3.15 (2026-10-09) are untested. `ubuntu-latest` is moving to
   Ubuntu 26.04 between 2026-10-19 and 2026-11-19, and EOL interpreters are the first thing
   setup-python stops shipping on a new image.
7. setuptools prints: "`project.license` as a TOML table is deprecated ... By 2027-Feb-18, you
   need to update your project". `[build-system]` has no upper bound, so a setuptools release
   after that date can fail the sdist build for every user who builds from source. Confirmed
   by building the wheel with setuptools 84.2.1 in an isolated venv.
8. The default CLI output is not valid JSON when piped. `_emit` uses rich `Console().print`
   (engine/cli/main.py:61), which wraps long strings at the terminal width and puts raw
   newlines inside JSON strings. `uxskill lint tests/lint_corpus/dirty | python -m json.tool`
   fails with "Invalid control character". `--no-pretty` is valid. Any CI user piping to jq
   depends on rich's wrapping behaviour.
9. A lint score can change with no rule change: `render-failed` is a medium finding
   (engine/render/core.py:170) and counts toward the score, so a timeout, a missing font CDN
   behind a proxy or a Chrome update lowers a user's score. The render check also prefers the
   user's auto-updating Google Chrome (`channel="chrome"`) over Playwright's pinned Chromium,
   follows remote resources (`wait_until="load"`, `page.request.get` for photos), and records
   neither the browser nor its version in the report. The lint report carries no ruleset
   version or digest; `data/anti-patterns.json` `_meta.version` still says "2.0.0".
10. Two install hints name fixes that do not work: `pip install 'uxskill[image]'` (no such
    extra exists) and `pip install Pillow>=10.0` (unquoted, the shell redirects to a file
    named `=10.0`). Several others name the fix but not the field (section 4).
11. The plugin hook runs `python3` with no fallback. On Windows without Git Bash, Claude Code
    runs shell-form hooks in PowerShell, and `python3` is usually absent or a Store stub.
12. The plugin root is the whole repo: 66 MB tracked, 48 MB of it the docs site. Claude Code
    copies the plugin into `~/.claude/plugins/cache/<mkt>/<plugin>/<version>/` per version and
    keeps old versions 14 days. A top-level `bin/` also puts `state.sh`, `ux-lint.sh` and
    friends on Claude's Bash PATH, and claude.ai and Cowork refuse to install a plugin that
    has a top-level `bin/`.
13. Third-party marketplaces do not auto-update by default, so users stay on the plugin
    version they installed while `pip install -U` moves the CLI and MCP server. The hook lints
    with the plugin copy of `engine/`; the CLI lints with the pip copy. Two rule sets, two
    scores, no field that says which.

## 1. Prioritized changes for 5.0

P0 means: without it, something users rely on breaks inside the unattended window, or a
release cannot ship unattended. P1: likely break or silent wrong answer. P2: hardening.

### P0

1. **`.github/workflows/release.yml` (rewrite) and new `.github/workflows/publish.yml` logic: publish from CI by trusted publishing, after tests pass.**
   Change: trigger on `workflow_run` of `test` (conclusion success) on main, or fold the
   tests into the release workflow as a `needs:` job. Steps: read version; skip if tag exists
   or notes missing (keep today's rule); build sdist and wheel once (`python -m build`); run
   `scripts/release_checks.py wheel digest`; check pyproject, package.json and plugin.json
   versions agree (tests/test_version.py already asserts it; run it here too); create the
   GitHub release as a draft; attest the dists (`actions/attest-build-provenance`); upload
   to PyPI with `pypa/gh-action-pypi-publish` in a `pypi` environment with job-level
   `id-token: write` and no token; poll the PyPI JSON API until the version resolves;
   `npm publish` with trusted publishing (Node 24, npm >= 11.5.1, `id-token: write`), which
   adds npm provenance automatically for a public repo; attach the SBOM and dists to the
   draft; publish the release last.
   Why: today publishing needs the maintainer's local tokens, 4.0.0 never reached PyPI or
   npm, and the npm wrapper pins `uxskill==<its own version>` on PyPI, so an npm release that
   lands before its PyPI twin fails for every `npx` user. PyPI first, then npm, closes that.
   Tokens that expire in 90 days cannot carry an unattended release; OIDC has nothing to
   expire. Gating on tests stops a red main from being tagged.

2. **`.github/dependabot.yml`: stop Dependabot from widening across known-breaking majors, and add cooldown and groups.**
   Change: under the pip entry add `ignore: [{dependency-name: "mcp", update-types: ["version-update:semver-major"]}, {dependency-name: "playwright", update-types: ["version-update:semver-major"]}]`;
   `cooldown: {default-days: 7, semver-major-days: 30}`; `groups` for minor and patch so one
   PR carries them; for github-actions, group everything and keep SHA pins (Dependabot
   updates the SHA and the version comment). Close the open `mcp <3` PR.
   Why: the open Dependabot PR would break the MCP server. With nobody reviewing, a
   Dependabot PR that passes a test suite that never starts the transport would look green.
   Cooldown keeps a compromised or yanked release from landing in its first week.

3. **`.github/workflows/test.yml`: install Playwright and a browser in one leg, start the MCP server over stdio in another, and test the Python versions that will exist during 5.0.**
   Change: matrix `python-version: ["3.11", "3.12", "3.13", "3.14", "3.15"]` on
   `runs-on: ubuntu-24.04` (pinned, not `ubuntu-latest`). Add a `render` job:
   `pip install -e ".[dev,render]" -c constraints/tested.txt`,
   `python -m playwright install --with-deps --only-shell chromium`, then run the render tests
   with `UXSKILL_RENDER_BROWSER=bundled` (see P1 item 8) and fail if any render test skipped
   (`pytest -rs` plus a check, or `--strict-markers` with a `render` marker that must run).
   Add an `mcp-stdio` test (new `tests/test_mcp_stdio.py`) that spawns `ux-mcp` with
   `mcp.client.stdio`, runs `initialize`, `tools/list`, and calls `ux_stats`, asserting 25
   tools and a version string. Add one `windows-latest` job running the hook test and the npm
   wrapper test. Drop the `|| true` on `engine stats`.
   Why: the render check and the MCP transport are the two surfaces that break when a
   dependency moves, and neither runs in CI today. Pinning the runner image stops the
   ubuntu-latest flip (Oct 19 to Nov 19, 2026) from changing CI under a release.

4. **`pyproject.toml`: build metadata that will still build in 2027, and a Python floor that will still be supported.**
   Change: `license = "MIT"` (SPDX string) and `license-files = ["LICENSE", "NOTICE"]`; drop
   the `License ::` classifier; `requires = ["setuptools>=77,<90", "wheel"]` (floor is the
   PEP 639 release, cap is "next majors we have not tested"; the canary moves it);
   `requires-python = ">=3.11"`; classifiers 3.11 to 3.15; drop the `tomli` dependency
   (tomllib is stdlib from 3.11); `Development Status :: 5 - Production/Stable`; render extra
   `playwright>=1.63,<2`; add the missing `image = ["Pillow>=10"]` extra the error message
   already promises.
   Why: setuptools says the table form stops being supported after 2027-02-18, inside the
   months 5.0 must run. 3.10 is EOL since 2026-10-01; pydantic, mcp and playwright will drop
   it during the window, after which 3.10 users would resolve to old, untested dependency
   sets. 5.0 is the one release where raising the floor is allowed. Python 3.10 users keep
   getting 4.x from pip automatically because 4.x declares `>=3.10`.

5. **`engine/render/core.py`: make the render check deterministic and keep environment failures out of the score.**
   Change: (a) block network by default: `await page.route("**/*", ...)` that continues
   `file:` and `data:` and aborts the rest, with `--render-network allow` to opt in; (b)
   pick the browser explicitly: default `bundled` (Playwright's Chromium, whose revision is
   fixed by the Playwright version), `chrome` only on request or as a fallback when bundled is
   missing, and say which in the report; (c) set `page.set_default_timeout` and
   `set_default_navigation_timeout` from one constant; (d) report `render-failed` as an
   unmeasured page in a new `unmeasured` list, not as a finding, so `compute_score` never sees
   it; (e) add `"render": {"browser": "chromium", "version": browser.version, "playwright":
   <version>, "network": "blocked"}` to the report.
   Why: today a proxy that stalls fonts.googleapis.com, a CDN photo, or a Chrome update can
   move a score with no change to the page or the rules. A score that moves on its own is the
   first thing an unattended user files as a bug.

6. **`engine/linter/core.py` and `data/anti-patterns.json`: version the rules and the score formula, and put both in every report.**
   Change: `_meta.version` follows the engine release, add `_meta.ruleset` (for example
   `"5.0"`) and compute a digest of the rule entries at load. `LintReport.to_dict()` gains
   `"ruleset": {"version": "5.0", "digest": "sha256:...", "score_formula": 2}`. Same block in
   the MCP `ux_lint` result and the hook text ("ux-lint 5.0.3, ruleset 5.0"). Add
   `uxskill lint --ruleset 5.0` to score with the frozen rule set of an earlier minor (keep
   the last two minors' rule lists in the package), and `--compare-ruleset` to print the
   delta.
   Why: rule changes are the main way a user's score changes between releases. Without a
   version in the report nobody can tell a regression in their page from a regression in the
   rules, and the plugin hook and the pip CLI can disagree silently (finding 13).

7. **`engine/cli/main.py` `_emit`: never print wrapped JSON.**
   Change: use rich only when `sys.stdout.isatty()`; otherwise `json.dumps(..., indent=2,
   ensure_ascii=False)`. When rich is used, `Console(soft_wrap=True)`. Reconfigure stdout to
   UTF-8 at startup (`sys.stdout.reconfigure(encoding="utf-8", errors="replace")`) so Windows
   on 3.11 to 3.14 matches 3.15, where UTF-8 mode becomes the default (PEP 686). Add a test
   that pipes `uxskill lint` on the dirty corpus through `json.loads`.
   Why: confirmed today that piped default output is invalid JSON. The JSON shape is a
   public interface; it must not depend on a rich release or a terminal width.

### P1

8. **`engine/mcp/server.py`: feature-detect the SDK, name the version and the fix, and plan the 2.x port.**
   Change: in `run_server`, include `_MCP_IMPORT_ERROR` in the message (it is in
   `_build_server` but `run_server` checks first and drops it); check
   `hasattr(Server, "list_tools") and hasattr(Server, "call_tool")` and, if not, raise
   "mcp <installed version> is installed; ux-skill 5.0 needs mcp>=1.28.1,<2. Fix: pip install
   'mcp>=1.28.1,<2' in the environment that runs ux-mcp (<sys.executable>)". Wrap the console
   entry in a `main()` that prints the message to stderr and exits 2 instead of a traceback.
   Log the negotiated protocol version at startup. Track the 2.x port (on_* constructor
   handlers, explicit result types, `MCPError`) as 5.x work; when it lands, widen to
   `mcp>=2.x,<3` in a minor and keep a 1.x code path behind feature detection for one minor.
   Why: mcp 1.x is maintained for critical and security fixes only, with no end date; the
   protocol's current revision (2026-07-28) is per-request versioned with no handshake, and a
   modern-only client "Fails" against a legacy server per the spec's compatibility matrix.
   The canary (section 3) watches for the day Claude Code or Cursor stops speaking legacy.

9. **`.claude-plugin/plugin.json` hooks and a new `hooks/run.sh` launcher: find a Python, check its version, say what to set.**
   Change: replace `python3 "${CLAUDE_PLUGIN_ROOT}/bin/ux-lint-hook.py"` with
   `"command": "sh", "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/run.sh", "lint"]` (exec form, no
   quoting issues) where `run.sh` tries `$UXSKILL_PYTHON`, `python3`, `python`, `py -3`, and
   uses the first that reports >= 3.11. If none: write one line to stderr, "ux-skill hook is
   off: no Python 3.11+ found (tried UXSKILL_PYTHON, python3, python, py -3). Set
   UXSKILL_PYTHON to a Python 3.11+ path in the env block of .claude/settings.json", and exit
   0. Same for the 4.1 Stop hook. Drop `MultiEdit` from the matcher (no longer a Claude Code
   tool; harmless today, noise in validation). When `tool_input` has no `file_path`, append
   the payload's key names once per day to `${CLAUDE_PLUGIN_DATA}/hook-shape.log` so a renamed
   field is visible instead of silent.
   Why: Windows hosts without Git Bash run shell-form hooks in PowerShell; macOS Command Line
   Tools ship a 3.9 `python3`; a renamed Edit field would turn the hook into a silent no-op.

10. **`bin/uxskill.mjs`: find the right Python, say why pip failed, and work offline when it can.**
    Change: probe `python3`, `python`, `py -3` (Windows) and accept the first whose
    `sys.version_info >= (3, 11)`; when only an older one exists, say "python3 is 3.9.6;
    ux-skill 5.0 needs 3.11+". In step 2, when an installed `uxskill` has a different version,
    say so ("uxskill 5.0.1 is installed; this npm package is 5.0.3; run pipx upgrade uxskill")
    before falling through to pipx. When pip fails, recognise "externally-managed-environment"
    (PEP 668) and "No matching distribution" in its stderr and print the matching fix
    (pipx, or Python version, or PIP_INDEX_URL / HTTPS_PROXY for a proxy). Raise
    `engines.node` to `>=22` (18 ended 2025-04-30, 20 ended 2026-04-30).
    Why: `pip install --user` is refused on PEP 668 interpreters (Debian, Ubuntu, Homebrew),
    Windows rarely has `python3`, and today every one of these ends in "pip's own message is
    above".

11. **`engine/render/core.py` `_launch` and `_run`: install hints that work in the environment that runs the check.**
    Change: hint with `sys.executable`: "run `<sys.executable> -m playwright install
    chromium`" (a pipx install has its own interpreter; `python -m` on PATH is the wrong one);
    for pipx installs (`"pipx" in sys.prefix`) hint `pipx inject uxskill playwright`; when the
    launch error mentions missing host dependencies, add `playwright install-deps chromium`;
    when a download fails, name `HTTPS_PROXY`, `NODE_EXTRA_CA_CERTS` and
    `PLAYWRIGHT_DOWNLOAD_HOST`; when the bundled revision directory is missing but another
    revision exists, say "Playwright <v> needs Chromium revision <r>; you have <r2>; rerun
    install".
    Why: these are the top render-check support questions behind a proxy, in pipx and after a
    Playwright upgrade.

12. **`engine/image_extract/core.py:44`: fix the hint.**
    Change: `pip install 'Pillow>=10'` (quoted) or `pip install 'uxskill[image]'` once the
    extra exists (P0 item 4).
    Why: both commands in today's message fail.

13. **New `.github/workflows/canary.yml` (section 3): weekly run against latest dependencies and a fixed corpus, opening one issue on drift.**
    Why: the core of "no maintainer attention": drift is found by a schedule, not by users.

14. **New `constraints/tested.txt` (pip-compile output) used by every CI leg, updated by Dependabot.**
    Change: CI installs with `-c constraints/tested.txt`; one extra leg installs with
    `uv pip install --resolution lowest-direct` to prove the floors in pyproject are true.
    Why: today CI resolves whatever is newest on each run, so a red build can come from a
    dependency release on a day nobody changed anything, and the floors (`playwright>=1.40`)
    are never tested.

15. **All workflows: pin actions by full commit SHA with a version comment; least-privilege `permissions:` per job; `persist-credentials: false` on checkout where the job does not push.**
    Why: tags like `@v7` are mutable; SHA pins plus Dependabot keep them current and
    immutable. Add `zizmor` (zizmorcore/zizmor-action) to lint workflows for template
    injection and over-broad permissions.

### P2

16. **Plugin layout: move the plugin to a subdirectory (`plugin/`) or use a `git-subdir` marketplace source, and move hook scripts from `bin/` to `hooks/`.**
    Why: 66 MB copied per version (48 MB of docs), generic scripts on Claude's Bash PATH, and
    claude.ai and Cowork refuse plugins with a top-level `bin/`. The npm wrapper can move to
    `npm/uxskill.mjs` with `bin` in package.json pointing there.

17. **Rename the import package `engine` to `uxskill` and move `data/` inside it (5.0 only).**
    Change: `uxskill/` package, `uxskill/data/` read with `importlib.resources`; keep an
    `engine` shim package that re-exports and warns for the 5.x line, removed in 6.0.
    Why: the wheel installs top-level `engine/` and `data/` into site-packages, generic names
    another distribution can collide with (the npm wrapper already strips the cwd from
    sys.path for this reason). Only a major release can do it. If this is too big for 5.0,
    at least move `data/` into the package.

18. **`.claude-plugin/plugin.json` and `marketplace.json`: run `claude plugin validate --strict .` in the canary; update the stale descriptions (v3.0, 18 MCP tools; the code has 25).**
    Why: the validator is the authoritative manifest check and reports unknown or moved
    fields as warnings before Claude Code stops loading them.

19. **Repository settings (no file): enable immutable releases, branch protection on main requiring `test`, private vulnerability reporting, and the OpenSSF Scorecard action.**
    Why: immutable releases protect tags and assets after publish; the release workflow must
    then create a draft, attach assets, publish (P0 item 1 already does).

20. **`CONTRIBUTING.md`: replace "Major bumps only for breaking changes to the slash-command surface" with the stability policy in section 5, and fix stale counts (75 tests, 92 brand specs, 6 READMEs).**

21. **`engine/installer/core.py`: stop writing a stub `.claude-plugin/plugin.json` with version "2.0.0" into user projects; read IDE config formats from one table with a "last verified" date the canary checks (Continue and Aider formats have moved since these writers were written; verify before relying on them).**

## 2. Dependency risk table

| Dependency | Current pin or state | How it breaks unattended | Guard to add |
|:-|:-|:-|:-|
| Python runtime | `requires-python >=3.10`; CI 3.10 to 3.13; local 3.11 | 3.10 EOL 2026-10-01; deps drop it and 3.10 resolves to stale sets; 3.14 and 3.15 untested; setup-python may not ship 3.10 on ubuntu 26.04; 3.15 turns UTF-8 mode on (PEP 686) | `>=3.11`; CI 3.11 to 3.15; canary adds the next pre-release (3.16 alpha) as allowed-failure; engine/__init__ checks `sys.version_info` and raises "ux-skill 5.0 needs Python 3.11+, this is X.Y (sys.executable); install with pipx or a newer Python" |
| setuptools (build) | `>=82.0.1`, no cap; latest 84.2.1 | license table and classifier deprecated, unsupported after 2027-02-18; sdist builds fail | SPDX `license`, `license-files`, cap `<90`; canary builds with newest setuptools and reports deprecation warnings as failures (`-W error::DeprecationWarning` on the build or grep the log) |
| click, rich, pydantic | floors 8.4.2, 15.0.0, 2.13.4; no caps | rich output change already makes piped JSON invalid; pydantic 3 would change `model_json_schema` and validation | caps at next major (`click<9`, `rich<16`, `pydantic<3`); JSON output never via rich when not a TTY; tests compare MCP tool schemas with a committed snapshot |
| Playwright (Python) | extra `>=1.40`; local 1.63.0; latest 1.64.1 | each Playwright version needs its own browser revision; floor 1.40 never tested; API changes on a major | `>=1.63,<2`; canary on latest; feature-detect anything newer than the floor; error names the revision mismatch and the install command with `sys.executable` |
| Chromium / Chrome | prefers installed Google Chrome (`channel="chrome"`, auto-updates; here Chrome for Testing 153), else bundled headless shell | geometry and color results move with Chrome releases; enterprise policy can block launch; missing Linux libs | default to bundled Chromium; record browser and version in the report; `--render-browser chrome` opt-in; canary diffs corpus findings against a committed baseline; `install-deps` hint |
| Network during render | `wait_until="load"`; photos fetched via `page.request.get` | proxy stalls, offline runs, CDN changes alter findings and score | block non-file requests by default; `render-failed` out of the score; timeouts explicit |
| mcp Python SDK | `mcp>=1.28.1,<2` (extra and dev); local 1.30.0; latest 2.3.0 | 2.x removed decorators; 1.x gets only critical and security fixes; Dependabot already proposes `<3` | Dependabot ignore major; feature-detect decorators with a named error; stdio e2e test; 2.x port planned for 5.x |
| MCP protocol | server speaks legacy (handshake) revisions via SDK 1.x | current revision 2026-07-28 drops `initialize`; modern-only clients fail against legacy servers | canary probe: send `server/discover` and `initialize` to `ux-mcp`, record which era answers; track client support; dual-era via SDK 2.x |
| Claude Code plugin format | plugin.json inline `hooks`; marketplace `source: "./"`; version pinned in manifest | unknown top-level fields are stripped with a warning; strict objects reject unknown keys; `MultiEdit` no longer a tool; third-party marketplaces do not auto-update | `claude plugin validate --strict` in canary; keep manifest minimal; launcher logs unexpected payload shapes; release notes tell users to `claude plugin update ux@ux-skill` |
| Claude Code hooks | shell-form `python3 ...`, timeout 10s; 4.1 Stop hook uses `stop_hook_active` | PowerShell on Windows without Git Bash; Python missing or old; field rename turns the hook into a no-op or (Stop) a repeated block | exec-form launcher with Python discovery and version check; Stop hook also rate-limits by its own marker file (block at most once per page hash per 10 minutes) so it cannot loop even if the field changes |
| npm wrapper runtime | `engines.node >=18`; no deps | Node 18 and 20 are EOL; `python3` absent on Windows; `pip --user` refused by PEP 668; `pipx run` needs network | `engines.node >=22`; Python discovery; parse pip errors; offline message naming PIP_INDEX_URL and HTTPS_PROXY; test on Node 22 and 24 and Windows |
| npm registry auth | manual, maintainer token | granular write tokens expire in 90 days max (7 default); classic tokens revoked | trusted publishing (OIDC) from release workflow; provenance automatic |
| PyPI auth | manual, maintainer token; no provenance on 2.0.0a1 or 3.2.0 | token loss or 2FA prompts block an unattended release | trusted publishing; PEP 740 attestations via pypa/gh-action-pypi-publish |
| actions/checkout, setup-python | `@v7` tags (latest v7.0.1, v7.1.0) | mutable tags; Node 20 runtime removed from runners 2026-09-23, so any action still on Node 20 fails | SHA pins plus Dependabot grouped updates; zizmor |
| github/codeql-action | `@v4` (latest v4.39.1) | v3 deprecated Dec 2026 (already on v4, fine); new queries can fail the scan | SHA pin; weekly run already scheduled; keep `security-extended` |
| Runner image | `ubuntu-latest` | flips to 26.04 between 2026-10-19 and 2026-11-19; tools and EOL Pythons removed | `ubuntu-24.04` for required jobs; canary on `ubuntu-latest` to see the next image early |
| Fonts and data at runtime | none fetched by the engine; generated CSS links Google Fonts CDN for users' pages; data shipped in the wheel | only the render check touches the network (see above) | keep it so: a test that monkeypatches `socket.socket` to raise and runs build, lint, MCP handlers |
| IDE config writers | `engine/installer/core.py` writes Continue `config.json`, Aider yml, etc. | target tools change file formats | one table with "last verified" dates; canary flags entries older than 180 days |

## 3. Scheduled self-checks

### 3.1 `.github/workflows/canary.yml` (weekly, plus manual)

Schedule: `cron: "41 4 * * 3"` (off the hour, mid week). Jobs:

1. **latest-deps**, matrix python 3.11 and 3.15, `runs-on: ubuntu-latest` on purpose:
   `pip install -U --upgrade-strategy eager -e ".[dev,render,mcp]"` with no constraints file,
   `python -m playwright install --with-deps chromium`, full `pytest`, then
   `python scripts/release_checks.py`.
2. **corpus-baseline**: runs `uxskill --no-pretty lint` and `uxskill --no-pretty lint
   --render` over a fixed corpus (`tests/lint_corpus/*`, plus 10 to 20 frozen pages in a new
   `tests/canary/pages/` taken from docs/ and examples/, network blocked) and compares rule
   ids, counts and scores with `tests/canary/baseline.json`. Static lint must match exactly;
   render findings must match exactly with `bundled` browser. A diff is drift, reported with
   the browser version, Playwright version and ruleset digest.
3. **mcp-protocol**: spawns `ux-mcp` and (a) runs a legacy `initialize`, `tools/list`,
   `tools/call ux_stats`; (b) sends a modern `server/discover`; records which era answered.
   Fails when (a) fails. Writes (b) to the job summary so the move to dual-era is planned, not
   discovered.
4. **next-majors** (allowed to fail, reported only): installs `mcp` latest ignoring the cap,
   `pydantic` pre-releases, newest setuptools with deprecation warnings as errors, Python
   next alpha via `allow-prereleases: true`.
5. **plugin**: `npm i -g @anthropic-ai/claude-code` then `claude plugin validate --strict .`;
   runs both hook scripts with recorded payloads (Write, Edit, Stop) from
   `tests/fixtures/hooks/`.
6. **wrapper**: on `windows-latest` and `macos-latest`, Node 22 and 24: `node bin/uxskill.mjs
   --version` in a clean runner; `npx uxskill@latest --version` against the registry.
7. **registry-drift**: compares pyproject version with PyPI JSON `info.version` and npm
   `dist-tags.latest`; fails if a tagged release is missing from either registry for more
   than 24 hours.

On failure, one step at the end (permissions `issues: write` for that job only):

```yaml
- if: failure()
  env: { GH_TOKEN: "${{ github.token }}" }
  run: |
    title="canary: drift on $(date -u +%Y-%m-%d)"
    existing=$(gh issue list --label canary --state open --json number -q '.[0].number')
    body="Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
    if [ -n "$existing" ]; then gh issue comment "$existing" --body "$body";
    else gh issue create --label canary --title "$title" --body "$body"; fi
```

and a success step that closes an open `canary` issue with a comment. One issue, updated,
never a pile.

### 3.2 Dependabot (replace `.github/dependabot.yml`)

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule: { interval: "weekly" }
    cooldown: { default-days: 7, semver-major-days: 30 }
    ignore:
      - dependency-name: "mcp"
        update-types: ["version-update:semver-major"]
      - dependency-name: "playwright"
        update-types: ["version-update:semver-major"]
    groups:
      minor-and-patch: { update-types: ["minor", "patch"] }
    labels: ["dependencies"]
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule: { interval: "weekly" }
    cooldown: { default-days: 7 }
    groups:
      actions: { patterns: ["*"] }
    labels: ["dependencies", "github-actions"]
  - package-ecosystem: "npm"
    directory: "/"
    schedule: { interval: "monthly" }
    labels: ["dependencies"]
```

Dependabot PRs then target `constraints/tested.txt` (tested pins) and the action SHAs.
pyproject floors move by hand, and only when the lowest-direct leg says they must. Optional:
allow auto-merge for grouped patch updates when `test` and the render leg pass; never for
majors. Renovate is an alternative with the same rules (`minimumReleaseAge`,
`packageRules` with `matchUpdateTypes: ["major"]`, `enabled: false` for mcp); Dependabot is
already wired, so stay with it.

### 3.3 Release workflow hardening

- Trigger after `test` succeeds (workflow_run, branch main, conclusion success), plus manual
  dispatch with the version as input for a re-run.
- `concurrency: release` (kept), `permissions: {}` at top, per-job grants: build
  (`contents: read`), attest (`id-token: write`, `attestations: write`), pypi
  (`id-token: write`, environment `pypi`), npm (`id-token: write`, environment `npm`),
  release (`contents: write`).
- Build once, upload the dists as an artifact, every later job downloads that artifact: the
  bytes attested are the bytes published.
- Idempotent: skip PyPI upload if the version exists (`skip-existing: true`), skip npm if
  `npm view uxskill@<v>` resolves, so a re-run after a partial failure finishes the job.
- Prerelease rule kept: hyphenated version is a GitHub prerelease and an npm `next` tag; PyPI
  gets the PEP 440 form (the wrapper's `pythonSpec` already maps it).
- Post-publish smoke: in a fresh runner, `pipx run --spec uxskill==<v> uxskill --version` and
  `npx uxskill@<v> --version` must print `<v>`.

### 3.4 Supply chain

- Trusted publishing on PyPI and npm (no long-lived tokens anywhere).
- Attestations: PyPI PEP 740 via the publish action; npm provenance automatic with trusted
  publishing for a public repo; `actions/attest-build-provenance` on the dists for GitHub.
- SBOM: CycloneDX or SPDX from `anchore/sbom-action` over the built wheel, attached to the
  release.
- Immutable releases on the repo; release created as draft, assets attached, then published.
- Actions pinned by SHA; zizmor in CI; OpenSSF Scorecard weekly.
- `SECURITY.md` names private vulnerability reporting and the supported versions table from
  section 5.

## 4. Failure modes users hit unattended, and the messages they see

"Names field and fix" means the message says which input, file, version or variable is wrong
and gives a command that works in the user's environment.

| Path | Where | Message today | Names field and fix? | Change |
|:-|:-|:-|:-|:-|
| Missing browser binary | engine/render/core.py `_launch` | "No browser for the render check. Install Google Chrome, or run `python -m playwright install chromium`. (...)" | Fix yes, but `python` may be the wrong interpreter (pipx, venv); no revision named | Use `sys.executable`; name the needed revision; `install-deps` hint on missing libs |
| Playwright not installed | core.py `_run` | "The render check needs Playwright: pip install 'uxskill[render]'" | Fix only for pip in the same env | Add pipx form (`pipx inject uxskill playwright`); print `sys.executable` |
| Page timeout or page error | core.py `_measure` | `render-failed`: first 160 chars of the exception, "Run it again" | No field (which resource), and it lowers the score | Name the URL that stalled (track pending requests); move out of score |
| Render via CLI | engine/cli/main.py lint `--render` | "Render check skipped: <exc>", exit 2 | Inherits the above | Fine once the above is fixed |
| MCP SDK missing | engine/mcp/server.py `run_server` | RuntimeError with install hint, raised as a traceback from the console script; original import error dropped | Fix yes, cause no; misleading when mcp is present but broken | Include import error and installed version; exit 2 with one line |
| MCP SDK 2.x installed | `_build_server` | `AttributeError: 'Server' object has no attribute 'list_tools'` | No | Feature-detect and name the pin |
| MCP relative path | server.py `_source` | "... is a relative path; the MCP server runs in its own ..." | Yes (good model for the rest) | Keep |
| Pillow missing | engine/image_extract/core.py:44 | "pip install Pillow>=10.0 or pip install 'uxskill[image]'" | Fix is wrong twice (no `image` extra; unquoted `>=`) | Quote; add the extra |
| No click | engine/cli/main.py:79 | "Install `click` for the full CLI: pip install click rich" | Fix yes, field no (which interpreter) | Add `sys.executable -m pip install` |
| No python3 (npm) | bin/uxskill.mjs:111 | "no Python runtime found (python3 is not on PATH). Install Python 3.10+ ..." | Field yes; wrong on Windows where `python` or `py` exists | Probe `python` and `py -3`; update to 3.11+ |
| Old python3 (npm) | bin/uxskill.mjs step 4 | pip: "No matching distribution found for uxskill==X", then "pip could not install ... pip's own message is above" | No: never says the Python version is the cause | Check version first and say "python3 is 3.9; needs 3.11+" |
| PEP 668 interpreter | bin/uxskill.mjs step 4 | pip "externally-managed-environment", then the generic message | Partly (suggests pipx) | Detect and say it in one line |
| Offline or proxy (npm) | bin/uxskill.mjs step 3 | whatever `pipx run` prints; wrapper exits with its code | No | When pipx fails, print "pipx could not fetch uxskill==X from PyPI; set HTTPS_PROXY or PIP_INDEX_URL, or install once with `pipx install uxskill==X`" |
| Installed uxskill, other version (npm) | bin/uxskill.mjs step 2 | silent fall-through to pipx (network) | No | Say which versions differ and the upgrade command |
| Hook: no or old Python | plugin.json hook | Claude Code non-blocking hook error from the shell ("python3: command not found" or Store stub) | No | Launcher with discovery and the UXSKILL_PYTHON message |
| Hook: linter fails to import | bin/ux-lint-hook.py `_load_linter` | "ux-lint hook is off: the linter could not load under Python X ... Run the hook with Python 3.10 or newer" | Yes, but the user cannot choose the hook's Python today | Point at UXSKILL_PYTHON once the launcher exists |
| Hook: file over 1 MB | ux-lint-hook.py | "ux-lint skipped <file>: N MB is over the hook's 1 MB limit. Lint it by hand with `uxskill lint <file>`" | Yes | Keep |
| Plugin cache after update | Claude Code | hooks keep the old path until `/reload-plugins`; old dir removed after 14 days | n/a (Claude Code handles) | Release notes: "run /reload-plugins"; hook prints its own version so skew is visible |
| Windows encoding | CLI `_emit` with `ensure_ascii=False` | UnicodeEncodeError on cp1252 when output is redirected (Arabic, Thai text) on 3.11 to 3.14 | No | Reconfigure stdout to UTF-8 |
| Piped JSON | CLI `_emit` | invalid JSON (wrapped strings) | No | TTY detection |
| Old Python, pip direct | PyPI | pip silently installs the newest release allowing that Python (3.9 gets 3.2.0 today) | No | Accept (it is pip's design), but say in README and in 4.x final notes; the engine's version check covers source runs |

## 5. Versioning policy for a stable 5.0

### 5.1 What semver covers in 5.x

The public surface, each item listed in a new `docs/stability.md`:

1. CLI: command names, flags, exit codes (0, 1 findings at or above threshold, 2 could not
   run), and the JSON output schema (keys may be added, never removed or retyped).
2. MCP: tool names, input schemas (fields may be added as optional), result keys.
3. Generated output names: CSS custom property names and DTCG token paths of the roles
   (`--color-action-primary` etc.). A rename is breaking for every user page.
4. Lint: rule ids, severities and the score formula version (see 5.3).
5. Plugin: slash command names, hook opt-out variables (`UXSKILL_LINT_ON_WRITE`,
   `UXSKILL_COMPLAINTS_GATE`, `.ux/*.off` files), the `.ux/` file formats it reads.
6. Python API: only names exported from `uxskill.api` (new, small). Everything else under
   the package is internal and may change in a minor.
7. Data manifests: `schema_version` in `_meta`; entries may be added in a minor.

Minor: additions, new rules in preview, new optional fields. Patch: fixes that do not change
a score on the canary corpus except where the fix is the point (named in the changelog).

### 5.2 Deprecation windows

- A deprecated CLI flag, MCP tool, slash command alias or output field keeps working for at
  least two minors and at least six months, whichever is longer, and is removed only in a
  major.
- It warns on stderr (CLI), in a `deprecations` list in JSON and MCP results, and in the
  hook text: "flag X is deprecated since 5.2 and goes in 6.0; use Y".
- The CHANGELOG gets a "Deprecated" section per release (Keep a Changelog already has it).
- The 3.x aliases kept "until 4.1" (marketplace.json) are removed in 5.0, not later.

### 5.3 Rules and scores that do not move silently

- Each minor has a frozen ruleset (`5.0`, `5.1`, ...). The report says which one scored it and
  its digest.
- A new rule ships as `preview`: reported, counted zero in the score, for one minor. It
  becomes scoring in the next minor, listed under "Score changes" in the changelog with the
  canary corpus delta.
- A rule fix that lowers false positives can land in a patch; one that adds findings waits for
  a minor.
- `uxskill lint --ruleset 5.0` scores with an earlier minor's rules (keep the last two). CI
  users pin it in `.ux/config.toml` (`ruleset = "5.1"`) and move on purpose.
- `score_formula` is an integer in the report; changing `compute_score` bumps it and is a
  major change unless gated behind `--score-formula`.
- Environment failures (render could not run, page timed out) never change a score; they are
  listed as unmeasured.
- Data manifests carry `_meta.version` equal to the release that last changed them, and the
  loader refuses an unknown `schema_version` with "data/<file>.json has schema_version X; this
  engine reads Y; reinstall uxskill".

### 5.4 LTS option

Recommended for a single maintainer: no separate LTS branch at 5.0. Declare 5.x the
long-lived line: no 6.0 before a stated date (for example 2027-11), monthly patch window
filled only by Dependabot groups and canary fixes. If 6.0 ships, cut `release/5.x` at that
point and keep it for six months with compatibility and security fixes only, backported by
label (`backport-5.x`) with a backport action, released by the same workflow (it reads the
version from the branch). Publish a support table in SECURITY.md:

| Line | Status | Fixes until |
|:-|:-|:-|
| 5.x | current | until 6.0 plus 6 months |
| 4.x | security only | 2027-05-01 (last line that runs on Python 3.10) |
| 3.x and older | unsupported | now |

## 6. Evidence

### 6.1 Repo evidence

- No publish to PyPI or npm in any workflow: `.github/workflows/release.yml` only runs
  `gh release create`. PLAN-4.0.md:177-179: "the PyPI and npm publish, with his own tokens".
  PLAN-4.1.md (on research/hendurhance-kb and origin/feat/4.1-stageshow) "Waiting on the
  owner: ... Publish 4.0.0 to PyPI and npm."
- Registries today: `https://pypi.org/pypi/uxskill/json` gives info.version 3.2.0, releases
  2.0.0a1 and 3.2.0, both `requires_python >=3.9`, no provenance on either file (PyPI simple
  JSON API). `https://registry.npmjs.org/uxskill` gives dist-tags latest 3.2.0, alpha
  2.0.0-alpha.1. Git tag v4.0.0 exists.
- Release does not wait for tests: release.yml triggers on `push: branches: [main]`
  independently of test.yml.
- Render tests skipped in CI: tests/test_render.py:11 `pytest.importorskip("playwright")`;
  test.yml installs `.[dev]`, which has no playwright.
- MCP transport untested: tests/test_mcp.py:3-6 "We deliberately avoid bringing up the actual
  stdio transport in tests"; test at line 159 builds `_build_server()` only.
- MCP message drops the cause: engine/mcp/server.py:1183-1187 (`run_server`) vs 1137-1142
  (`_build_server` includes `_MCP_IMPORT_ERROR`). Decorators used: server.py:1146, 1159.
- Dependabot widening PR: `git show origin/dependabot/pip/mcp-gte-1.10-and-lt-3`
  "update mcp requirement from <2,>=1.10 to >=1.10,<3" (2026-09-26).
- render-failed in score: engine/render/core.py:170-171 severity "medium"; cli/main.py:350-354
  extends findings and recomputes score.
- Browser choice: core.py:185-194 tries `{"channel": "chrome"}` first. Local run used
  "Google Chrome for Testing 153.0.8010.12". Network: core.py:226
  `wait_until="load"`; taste.py:299 `page.request.get(url)`.
- No ruleset version in report: engine/linter/core.py:134-143 `to_dict` keys.
  `data/anti-patterns.json` `_meta`: version "2.0.0", entries 171, schema_version "1.0".
- Invalid piped JSON: engine/cli/main.py:56-65 and :89 (`--pretty` default True). Reproduced:
  `python -m engine.cli.main lint tests/lint_corpus/dirty | python -c "import json,sys;
  json.load(sys.stdin)"` gives "Invalid control character at: line 17 column 81"; with
  `--no-pretty` it parses.
- setuptools deprecation: building the 4.0.0 tree with setuptools 84.2.1 printed
  "`project.license` as a TOML table is deprecated ... By 2027-Feb-18, you need to update your
  project" and "License classifiers are deprecated". pyproject.toml:2 `setuptools>=82.0.1`,
  :11 `license = { text = "MIT" }`.
- Wheel layout: the built wheel holds top-level `data/...json` next to `engine/`
  (package-data `"engine" = ["../data/**/*.json"]`, pyproject.toml).
- Wrong hint: engine/image_extract/core.py:44-47; pyproject has no `image` extra.
- Hook command: .claude-plugin/plugin.json:71 `python3 "${CLAUDE_PLUGIN_ROOT}/bin/ux-lint-hook.py"`;
  4.1 adds a Stop hook `bin/ux-complaints-hook.py` relying on `stop_hook_active`.
- npm wrapper: bin/uxskill.mjs:111 checks only `python3`; :119 `pip install --user`;
  package.json:15 `"engines": {"node": ">=18"}`.
- Plugin size: `git ls-files | xargs du -cb` gives 65,839,948 bytes; docs/ 48,392,412.
- Installer stale stub: engine/installer/core.py:138 writes plugin.json with version "2.0.0".
- Local tool versions: playwright 1.63.0, mcp 1.30.0, pydantic 2.14.2, click 8.5.0, rich
  15.0.0, setuptools 79.0.1 in .venv (Python 3.11.18).
- Latest upstream (PyPI JSON, 2026-11-02): playwright 1.64.1, mcp 2.3.0, setuptools 84.2.1,
  pydantic 2.14.2, click 8.5.0, rich 15.0.0. pydantic-core 2.50.2 and greenlet 3.5.6 ship
  cp315 wheels. Action tags (git ls-remote): actions/checkout v7.0.1, actions/setup-python
  v7.1.0, actions/setup-node v7.1.0, github/codeql-action v4.39.1,
  pypa/gh-action-pypi-publish v1.14.3, actions/attest-build-provenance v4.2.2,
  anchore/sbom-action v0.24.3, zizmorcore/zizmor-action v0.8.0, ossf/scorecard-action v2.5.0.

### 6.2 External sources

- Python versions and EOL dates (3.10 EOL 2026-10-01; 3.14 2025-10-07; 3.15 2026-10-09):
  https://devguide.python.org/versions/
- PEP 686, UTF-8 mode default from Python 3.15: https://peps.python.org/pep-0686/
- PEP 668, externally managed environments, applies to `pip install --user`:
  https://peps.python.org/pep-0668/
- setuptools license metadata guidance (link printed by the deprecation warning):
  https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license
- Node.js release schedule (18 ended 2025-04-30, 20 ended 2026-04-30, 22 until 2027-04-30,
  24 until 2028-04-30): https://raw.githubusercontent.com/nodejs/Release/main/schedule.json
  and https://github.com/nodejs/Release
- Playwright browsers, headless shell vs new headless, channels, proxy and download host
  variables, garbage collection: https://playwright.dev/python/docs/browsers
- MCP Python SDK v1 to v2 migration (decorators replaced by `on_*` handlers; v1.x keeps
  critical and security fixes; keep `<2` until migrated):
  https://py.sdk.modelcontextprotocol.io/migration/ and
  https://github.com/modelcontextprotocol/python-sdk
- MCP versioning, current revision 2026-07-28, per-request version, `server/discover`:
  https://modelcontextprotocol.io/specification/versioning
- MCP legacy vs modern compatibility matrix (modern client vs legacy server fails):
  https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning.md
- Claude Code plugin manifest reference (unknown fields stripped, `claude plugin validate
  --strict`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, exec form, top-level `bin/` on
  PATH and refused by claude.ai and Cowork): https://code.claude.com/docs/en/plugins-reference
- Claude Code plugin loading (cache path, version pinning, 14-day cleanup, auto-update off for
  third-party marketplaces, hooks keep old path until `/reload-plugins`):
  https://code.claude.com/docs/en/plugins/loading
- Claude Code hooks (exec vs shell form, PowerShell when Git Bash is missing, PostToolUse
  `additionalContext`, non-blocking errors, matchable tools without MultiEdit):
  https://code.claude.com/docs/en/hooks
- Node 20 removal from Actions runners (default Node 24 from 2026-06-16, removal 2026-09-23):
  https://github.blog/changelog/2026-09-23-deprecation-of-node-20-on-github-actions-runners/
  and https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
- ubuntu-latest moving to Ubuntu 26.04, rollout 2026-10-19 to 2026-11-19:
  https://github.blog/changelog/2026-09-17-ubuntu-26-generally-available-and-latest-migration
  and https://github.com/actions/runner-images/issues/14226
- CodeQL Action v3 deprecation (Dec 2026), v4 on Node 24:
  https://github.blog/changelog/2025-10-28-upcoming-deprecation-of-codeql-action-v3/
- npm token changes (granular tokens max 90 days, write tokens default 7 days, classic tokens
  revoked): https://github.blog/changelog/2025-09-29-strengthening-npm-security-important-changes-to-authentication-and-token-management/
  and https://github.blog/changelog/2025-10-10-strengthening-npm-security-important-changes-to-authentication-and-token-management
- npm trusted publishing requirements (npm CLI 11.5.1+, Node 22.14.0+, `id-token: write`,
  provenance automatic for public repo and package, GitHub-hosted runners only, workflow
  filename must match): https://docs.npmjs.com/trusted-publishers
- PyPI trusted publishing and the recommended workflow (environment `pypi`, job-level
  `id-token: write`, `pypa/gh-action-pypi-publish@release/v1`):
  https://docs.pypi.org/trusted-publishers/ and
  https://docs.pypi.org/trusted-publishers/using-a-publisher/
- Dependabot options (cooldown, groups, ignore with update-types):
  https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference
- Immutable releases GA (tags and assets protected, release attestations):
  https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
- zizmor (GitHub Actions static analysis): https://github.com/zizmorcore/zizmor
- OpenSSF Scorecard action: https://github.com/ossf/scorecard-action

### 6.3 Not verified, flagged for follow-up

- Exact behaviour of setup-python for 3.10 on the ubuntu-26.04 image (risk stated, not
  observed).
- Whether Continue and Aider still read the files `engine/installer/core.py` writes.
- The Stop input section of the hooks reference was not in the fetched excerpt;
  `stop_hook_active` appears in the SubagentStop example on the same page.
