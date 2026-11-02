# ux-skill 4.0.0: Foundations

One brand color and a brief in, a WCAG-checked design system out.

ux-skill 4.0 builds a design system from one brand color and a brief, reads the system a team already has, checks every color pairing for contrast in light, dark and high contrast, and writes only what passes. Coming from 3.x? Start with [docs/migrating-to-4.md](https://github.com/Laith0003/ux-skill/blob/main/docs/migrating-to-4.md).

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

## Upgrade

- pip: `pip install --upgrade uxskill` (Python 3.10 or newer). For the MCP server: `pip install --upgrade 'uxskill[mcp]'`.
- pipx over an installed 3.x: `pipx upgrade uxskill`.
- npm: `npx uxskill@latest`.
- To stay on 3.x on purpose: `pip install 'uxskill<4'`. On Python 3.9, pip keeps installing 3.2.x, which still works.

## Migrating from 3.x

- The 3.x `tokens.css` from `ux generate` and the system pack's `DESIGN.md` and `tokens.css` are replaced by `tokens.css`, `tokens.json` (DTCG), `fonts.css`, `fonts-self-host.css`, `art/` and `system-report.md`.
- Path 1, build a new system and move the page onto its roles. Every 3.x custom property has a 4.0 role: `--color-canvas` is `--color-surface-page`, `--color-primary` is `--color-action-primary`, `--space-md` is `--space-4`, `--motion-base` is `--motion-state-duration`. The full table is in the guide.
- Path 2, keep the 3.x system. `uxskill system import --from DESIGN.md` reads it as it is, `system enhance` reports what it lacks and how to add it, and `system extend` adds the missing foundations, roles or contracts in an extension file beside it. Nothing is rewritten.

## Added

- **Nine foundations**: color, type, space, layout, radius, border, elevation, motion and imagery, each from primitives to semantic roles, emitted as DTCG and CSS.
- **Five mode axes** in every role: light and dark, standard and high contrast, comfortable and compact spacing, left to right and right to left, full and reduced motion. One attribute on `<html>` switches each.
- **The WCAG gate.** Every text, control and focus pairing is measured in light and dark, at standard and high contrast: text at 4.5:1 and non-text parts at 3:1 at standard contrast (WCAG 1.4.3 and 1.4.11), text at 7:1 in high contrast (WCAG 1.4.6), plus a 4.5:1 high-contrast floor for most non-text parts that is ux-skill's own, since WCAG sets no enhanced non-text level. A system that fails is not written.
- **Arabic and right to left built in**: an Arabic face with its own type scale under `dir="rtl"`, logical spacing and mirrored motion. `--latin-only` leaves it out.
- **Looks are continuous.** Seven axes, the brand and the brief set every look; no industry or keyword picks one.
- **Importers** for DTCG, CSS, Tailwind 4 and a resolved Tailwind 3 config, Markdown rule files and Figma variables, with a naming adapter, `--scan`, `system enhance --from` and `system extend`. An importer never guesses: it reads a value or lists the entry under Not read with how to write it.
- **Exporters** to CSS, DTCG, Tailwind 4 and Figma variables, with the scripts that apply and read them in a Figma file. Every write goes through an intake step that backs up the client's files byte for byte.
- **23 component contracts and 14 section contracts.** State changes transition on `motion.state`, pressable controls scale on `motion.press.scale` (1 under reduced motion), and nav, tabs, segmented controls and menus move one indicator on `motion.indicator`. A section names its job, the components its slots take, its variants, the proof it needs and its phone recomposition.
- **171 lint rules** that read the page's own system: motion timed from its curve, display line height held to the engine's floor, the system's lean to capitals, and how components show their states.
- **`lint --render`** measures the color budget, the photo grade lock, accent text on every ground, loops under reduced motion and pause controls, and drives the page with its motion running: focus rings that do not show or are clipped, hover and press that answer late, focus lost after Escape, and a press that still moves under reduced motion.
- **Inner pages** (pricing, about, contact, customers, customer story, legal) with their own sequences, built in one run as one page family.
- **Six category colors** for nominal data, `color.category.1` to `color.category.6`, each with a soft fill, a strong tone, text and text on the strong tone, in light, dark and high contrast. A shadcn theme's `chart-1` to `chart-5` map to them on import.
- **25 MCP tools** on one shared command layer.
- **`figma-skill/`**: ux-skill as a skill for Figma's agent.
- **Release checks** (`scripts/release_checks.py`): 600 sampled briefs build, every gallery and fixture system round-trips through every format with no mismatch, the build digest is stable across hash seeds, and the wheel ships nothing private.

## Changed

- **25 slash commands become 18.** Each merged command keeps every step and flag of the ones it absorbed: `/ux-discover` takes `--frame` and `--recommend`; `/ux-design` takes `--component`, `--dashboard` and `--from-image`; `/ux-polish` loops lint, fix and re-lint until the score reaches 90 or three rounds pass (`--loop-only`, `--no-loop`); `/ux-init` takes `--stats`.
- **Surface playbooks.** Landing, dashboard and component rules live in `references/surfaces/`, one playbook each, and `/ux-design` loads exactly one, picked by its mode.
- **Every page carries photographs**, sourced (stock included) when the client has none. The brand gate fails a page whose only images are illustrations, icons or the logo, unless the brand forbids photography outright.
- **The photo direction** asks for the client's own photos first, describes each missing shot by what it shows, and names the stock cliches to avoid.
- **The dashboard playbook** teaches the product dashboard people check many times a day: every figure carries its comparison, date or count, and states take the category colors, never color alone.
- **Lint reads what a page uses.** A rule on a utility class no element carries is not reported. Over a hundred pages from AI builders this removed a quarter of the findings, none on an element the page has.
- **The quality score** tells heavy pages apart: past 50 points of penalty it decays toward 0 instead of stopping there. Scores of 50 and up are unchanged.
- **Python 3.10 or newer.** Python 3.9 is past end of life.

## Fixed

- The landing display fits the headline word the face really sets: each Latin face carries its letter advance without the space, so a short headline no longer runs sideways at tablet width.
- Lint reads dashboards as admin templates build them. Over fourteen public admin dashboards this removed 166 findings, none of them a real problem.
- The quality score counts a repeated rule lightly past 50 points of penalty, so a page with 149 links to "#" reads as one pattern, not 149 problems.

## Deprecated

These seven commands are now aliases that say where they moved and run the new command with the same arguments. They are removed in 4.1.

| Old | New |
|---|---|
| `/ux-frame` | `/ux-discover --frame` |
| `/ux-recommend` | `/ux-discover --recommend` (the `ux_recommend` MCP tool is unchanged) |
| `/ux-stats` | `/ux-init --stats` |
| `/ux-evolve` | `/ux-polish --loop-only` (the alias passes `--rounds 5`) |
| `/ux-component` | `/ux-design --component` |
| `/ux-dashboard` | `/ux-design --dashboard` |
| `/ux-image-to-code` | `/ux-design --from-image` (the alias passes `--extract-only`) |

Offline. Deterministic. No LLM called by the engine. No telemetry. MIT.

Full notes: [CHANGELOG.md](https://github.com/Laith0003/ux-skill/blob/main/CHANGELOG.md) and the launch post at [uxskill.laithjunaidy.com/blog/ux-skill-4-foundations.html](https://uxskill.laithjunaidy.com/blog/ux-skill-4-foundations.html).
