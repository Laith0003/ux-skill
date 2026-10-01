# Moving from 3.x to 4.0

4.0 builds a design system from a brand color and a brief, checks every pairing for contrast in light, dark and high contrast, and writes it only when it passes. The 3.x outputs (the `tokens.css` that `ux generate` wrote, and the `DESIGN.md` and `tokens.css` of a system pack from `ux system-pack`) are replaced by one set of files: `tokens.css`, `tokens.json` (DTCG), `fonts.css`, `art/` and `system-report.md`.

Nothing is rewritten for you. Pick one of the two paths below.

## Path 1: build a new system and move the page onto its roles

1. Build: `uxskill system build --brand '<your primary hex>' --brief .ux/system-brief.json --out design-system`. Read `design-system/system-report.md`.
2. Link `design-system/fonts.css` and then `design-system/tokens.css` where the 3.x `tokens.css` was linked.
3. Replace each 3.x custom property with its 4.0 role, using the table below. A role carries every mode, so a page that switched its own dark colors can drop that code: set `data-theme="dark"` on the html element, or let the operating system decide.
4. Run `uxskill lint <your pages> --render` and fix what it reports.

## Path 2: keep your 3.x system and extend it

A system pack's `DESIGN.md` and `tokens.css` are read as they are: `uxskill system import --from DESIGN.md` (or `--from tokens.css`) reports what it read and lists every entry it did not read with how to write it. `uxskill system enhance --from DESIGN.md --out design-system` measures your system against the 4.0 checks and writes a report of what it lacks and how to add it; it changes nothing. `uxskill system extend --from tokens.css --add motion` adds what is missing (a foundation, roles or contracts) in an extension file next to the source, never over a token you have.

## 3.x names and their 4.0 roles

| 3.x custom property | 4.0 role | Note |
|---|---|---|
| `--color-canvas` | `--color-surface-page` | |
| `--color-surface` | `--color-surface-card` | |
| `--color-elevated` | `--color-surface-raised` | |
| `--color-border` | `--color-line-subtle` | a decorative line; a control's edge is `--color-line-input` (3:1) |
| `--color-ink` | `--color-text-default` | |
| `--color-body` | `--color-text-default` | |
| `--color-muted` | `--color-text-muted` | |
| `--color-primary` | `--color-action-primary` | the fill of the main action; a link is `--color-text-link` |
| `--color-primary-active` | `--color-action-primary-pressed` | hover is `--color-action-primary-hover` |
| `--color-on-primary` | `--color-text-on-action` | |
| `--color-success`, `--color-warning`, `--color-danger`, `--color-info` | `--color-status-success-strong`, `--color-status-warning-strong`, `--color-status-danger-strong`, `--color-status-info-strong` | text in that status is `--color-status-*-text`, a soft fill `--color-status-*-soft` |
| `--font-display` | `--type-face-display` | a text style is a role: `--type-text-display-font-size` and its fields |
| `--font-body` | `--type-face-text` | |
| `--font-mono` | `--type-face-mono` | |
| `--space-xxs`, `--space-xs`, `--space-sm`, `--space-md` | `--space-1`, `--space-2`, `--space-3`, `--space-4` | 4, 8, 12 and 16px; prefer a role such as `--space-control-gap` |
| `--space-lg`, `--space-xl`, `--space-xxl`, `--space-xxxl` | `--space-6`, `--space-8`, `--space-12`, `--space-16` | 24, 32, 48 and 64px; sections are `--layout-landing-gap` apart |
| `--radius-sm` | `--radius-control` | |
| `--radius-md` | `--radius-card` | |
| `--radius-lg` | `--radius-dialog` | |
| `--radius-pill` | `--radius-pill` | |
| `--motion-base` | `--motion-state-duration` | a hover or state change; a press is `--motion-press-duration` |
| `--motion-ease` | `--motion-state-curve` | |

The 3.x system pack's `DESIGN.md` front matter maps the same way: `colors.primary` is `color.action.primary`, `colors.canvas` is `color.surface.page`, `rounded.md` is `radius.card`, and a component block (`button-primary`) becomes the button contract in `engine/contracts/seed/button.yaml`, which binds each part to a role for every variant and state.

## What changes in behaviour

- Contrast is measured on the built tokens and the build refuses a system that fails; the 3.x pack's claim of AA by construction is replaced by the gate's report.
- Looks follow the brand and the brief's axes as continuous values. No industry picks a palette or a face.
- Every page carries photographs sourced by the system's photo direction; a brand's ban on a kind of photo narrows the choice, and only a system that forbids photography removes them.
- Python 3.10 or newer. `pip install 'uxskill<4'` keeps 3.2.x.
