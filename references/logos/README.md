# Real brand logos — use these, never fabricate

A set of real, single-path brand/tool SVGs (CC0, from simple-icons). When a
generated design references a **known brand, IDE, or integration**, use the
actual mark from this folder. **Never** draw, abstract, approximate, or emoji a
brand logo — a fabricated mark is an instant slop tell and a credibility leak.

## Available (33)

**AI coding tools / IDEs:** claude, cursor, windsurf, copilot, gemini, zed,
jetbrains, cline, github, warp, raycast

**Companies / products (design exemplars + integrations):** anthropic, apple,
bmw, discord, ferrari, figma, framer, instagram, linear, nike, notion, npm,
pinterest, posthog, pypi, python, resend, spotify, stripe, supabase, tiktok,
vercel

## How to use

- Inline the SVG and set `fill="currentColor"` (or a single brand/ink color) so
  it adapts to light/dark surfaces. The marks are monochrome single-path.
- Render at a uniform optical size in a logo wall; one mono treatment for all
  (see `../styles/anti-slop.md` logo-wall rules).

## Adding a logo

If a brand isn't here, fetch the real SVG before hand-drawing one:

```bash
curl -s "https://cdn.simpleicons.org/<slug>" -o references/logos/<name>.svg
```

Common slugs: `googlegemini`, `zedindustries`, `githubcopilot`, `intellijidea`.
If simple-icons doesn't have it (newer/niche tools), pull the official SVG from
the brand's own press/brand kit. Only as a last resort, set the brand name as
clean wordmark text — never an invented glyph.
