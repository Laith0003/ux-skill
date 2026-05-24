# Contributing to ux

Thanks for your interest. This plugin is opinionated by design — its value comes from a tight, disciplined point of view about what good UX looks like and how to produce it from a Claude Code session. Contributions are welcome when they sharpen the discipline. Contributions that loosen it are not.

## What we accept

- New patterns for `references/styles/arsenal.md` when they meet the existing bar (clear use case, performance characteristics, anti-pattern callouts).
- New entries in `references/styles/anti-slop.md` when they identify a real generative-model fingerprint, with a specific "do instead" pair.
- Fixes to typos, broken examples, or factual errors in the canonical references.
- Additional language bindings for `bin/state.sh` (Python, Node, etc.) if you need them.
- New commands ONLY when they fill a clear, demonstrable gap in the 17 we ship. Most of what people want is already there under a different name.

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

The plugin is plain markdown + a single bash script. No build step, no tests, no CI yet.

To work on it:

```bash
git clone https://github.com/Laith0003/ux-skill.git
cd ux-skill
ln -s "$(pwd)" ~/.claude/plugins/ux  # symlink for local development
```

Then in any Claude Code session: `/ux-audit`, `/ux-design`, etc. should be callable.

## Releases

Patch and minor bumps for incremental improvements. Major bumps only for breaking changes to the slash-command surface.

## Code of conduct

Be sharp, be direct, be useful. Don't be a jerk.

## Contact

For UX consulting, design reviews, or product positioning sessions outside of plugin contributions:

- LinkedIn: https://www.linkedin.com/in/laithaljunaidy/
- Phone: +962 79 786 8335
