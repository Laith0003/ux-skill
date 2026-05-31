# Contributing to ux

Thanks for your interest. This plugin is opinionated by design — its value comes from a tight, disciplined point of view about what good UX looks like and how to produce it from a Claude Code session. Contributions are welcome when they sharpen the discipline. Contributions that loosen it are not.

## What we accept

- **New anti-pattern rules** for `data/anti-patterns.json` when they identify a real generative-model fingerprint with a tight regex, a clear severity, a why, and a fix. Add a positive test fixture too.
- **New brand DESIGN.md specs** in `references/brands/<id>-DESIGN.md` plus the JSON projection at `data/brands/<id>.json`. Pull tokens from publicly verifiable sources; never invent specs.
- **New entries** in any data manifest — styles, palettes, type-pairs, components, motion-presets, landing-patterns, industries, chart-types, tech-stacks, ux-guidelines. Read 3 existing entries first, match the schema.
- **README translations** into a new language. Existing: en, ar, es, zh, fr, de. Add yours, then update the 6-language picker at the top of every other README.
- **Fixes** to typos, broken examples, link rot, or factual errors in the canonical references.
- **Regression tests.** Especially against bugs you found in the recommender, linter, persist, or MCP server.
- **New commands** ONLY when they fill a clear, demonstrable gap in the 23 we ship. Most of what people want is already there under a different name.

## What we don't accept

- "Personal-preference" rewrites of the references. The discipline is the point.
- New style libraries beyond the three in `references/styles/library.md`. Three is enough; more dilutes.
- Decoration. Emoji in code, gratuitous formatting, badge collections, etc.
- Renames of the slash commands. They're stable.

## How to contribute

1. Open an issue first. Describe the gap you want to fix and the smallest possible change that fixes it.
2. Wait for a "go" before opening a PR — half the work is deciding what NOT to ship.
3. Match the existing voice: direct, prescriptive, second-person, no marketing language, no source attribution to other plugins or sites.
4. Run through `references/styles/anti-slop.md` before submitting — your contribution must pass its own discipline.
5. No source attribution: never cite a brand, site, plugin, or skill by name. The plugin's knowledge reads as its own.

## Voice rules for any markdown you write

- Direct, second-person. "Use X." "Never Y." Not "It is recommended that one consider..."
- No emojis.
- No filler verbs (Elevate, Seamless, Unleash, Next-Gen, Revolutionize, Empower).
- No source citations to external plugins/sites.
- Code samples should be concrete and runnable, not pseudo-code.
- Pre-flight: read the file aloud. If it sounds like marketing or a corporate decking, rewrite it.

## Development

The plugin is a Python engine (`engine/`), 12 queryable JSON manifests (`data/`), 25 slash command markdown files (`commands/`), 5 sub-agent definitions (`agents/`), 92 brand DESIGN.md specs (`references/brands/`), an MCP server (`engine/mcp/`), and the static docs site (`docs/` + `landing/`).

Local dev:

```bash
git clone https://github.com/Laith0003/ux-skill.git
cd ux-skill

# Python ≥3.9 baseline; ≥3.10 unlocks the MCP transport.
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run the test suite (currently 75 tests).
pytest

# Run the project's own linter against any path.
python3 -m engine.cli.main lint <path>

# Run the recommender against a brief.
python3 -m engine.cli.main recommend --brief-file <brief.json>

# Regenerate site artifacts if you touched data manifests.
python3 scripts/generate-og-images.py
python3 scripts/build-commands-page.py

# Symlink for Claude Code plugin development:
ln -s "$(pwd)" ~/.claude/plugins/ux
```

CI runs the pytest suite across Python 3.9 / 3.10 / 3.11 / 3.12 / 3.13 (matrix in `.github/workflows/test.yml`). Your PR must pass CI. The advisor reviewer will run your changes through `python3 -m engine.cli.main lint` — PRs must lint clean against ux-skill itself. We dogfood our own product.

## Releases

Patch and minor bumps for incremental improvements. Major bumps only for breaking changes to the slash-command surface.

## Code of conduct

Be sharp, be direct, be useful. Don't be a jerk.

## Contact

For UX consulting, design reviews, or product positioning sessions outside of plugin contributions:

- LinkedIn: https://www.linkedin.com/in/laithaljunaidy/
- Phone: +962 79 786 8335
