# GitHub — DESIGN.md

## Overview
GitHub is the developer-platform brand that owns the social experience of writing software. Light mode is a near-white canvas with deep navy ink; dark mode is the dominant in-product surface (`#0d1117`) the engineers actually live in. The signature is the Octocat universe — a hand-illustrated cat-octopus cast joining seven-shade green contribution heatmaps, GitHub Sans (Mona Sans) display, and a typographic discipline borrowed from technical manuals, not SaaS marketing.

## Color
- **Primary:** `#2da44e` — GitHub green (CTAs + 'Merge' + 'Open Pull Request' buttons)
- **Canvas:** `#ffffff` — Pure white (marketing)
- **Canvas dark:** `#0d1117` — Near-black product chrome (the engineers' default)
- **Ink:** `#1f2328` — Deep navy-ink for type
- **Accent (link):** `#0969da` — GitHub blue (inline hyperlinks)
- **Contribution heatmap (7 shades):** `#ebedf0` → `#9be9a8` → `#40c463` → `#30a14e` → `#216e39`
- **Body:** `#3a4451`
- **Muted:** `#656d76`
- **Hairlines:** `#d0d7de`
- **Syntax highlight (light):** orange keywords `#cf222e`, blue idents `#0550ae`, green strings `#0a3622`

## Typography
- **Display:** Mona Sans (variable), weight 800–950, tight tracking, 48–80px hero
- **Sub-display:** Mona Sans, weight 700, 24–32px section heads
- **Body:** Mona Sans, weight 400, 16px running text, 1.5 line-height
- **Caption:** weight 500, 12–13px metadata
- **Mono:** Mona Sans Mono, 14px for code excerpts and CLI commands

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px. Marketing pages alternate light canvas with dark code-block bands. Product chrome is dense (12–16px row heights, 8px gutters).

## Motion signature
Octocat hover wiggles 4 degrees over 600ms cubic-bezier — the only chromatic motion the brand permits. Contribution-graph cell pops use a 120ms ease-out scale-in. Code-block reveal on scroll uses a slow 800ms opacity fade, no translate.

## Components observed
- `octocat-hero-illustration` — hand-drawn cat-octopus mascot
- `contribution-graph-grid` — 7-shade green heatmap year-grid
- `code-block-with-line-numbers` — dark code well with syntax highlight + line numbers
- `pull-request-card` — PR header with reviewer avatars + status
- `repo-stats-row` — star/fork/watch count row in mono
- `issue-thread-card` — threaded issue comment card
- `button-primary-green` — green-fill CTA, 6px radius
- `button-secondary-outline` — ink-outline secondary
- `footer-dark-multi-column` — dark-mode footer with 5 link columns

## Trademark signals
- Octocat cast — Mona, Mojo, Hubot — hand-drawn anthropomorphic cat-octopus mascots, often animated, never flat sticker-style
- Seven-shade green contribution heatmap — the brand's most-cited UI element, used both as data viz and as decorative texture
- Mona Sans (custom variable typeface) at display tiers, weight 800–950, tight letter-spacing — never thin
- Dual canvas — light mode (`#ffffff`) for marketing, near-black (`#0d1117`) for product chrome — most landing pages reveal both within scroll distance
- Code-block screenshots with line numbers, syntax highlighting in the actual GitHub palette (orange keywords, blue idents, green strings), and an Octocat motif overlaid

## What they DON'T do
- No replacing the Octocat with a generic mascot or emoji cat — the octopus-cat hybrid is non-negotiable and must be illustrated
- No non-green contribution heatmap palette — the seven-shade green is the recognized data-viz signature
- No thin Mona Sans display weights — locked at 800+
- No marketing pages without a dark code-block screenshot — they read as non-GitHub
- No shadows on code blocks — depth comes from the dark fill against light canvas
- No emoji-as-decoration in product chrome (in-PR reactions are an exception, not a brand-marketing affordance)

## Exemplar pages
- https://github.com/
- https://github.com/features
- https://github.com/copilot
- https://github.com/about
- https://github.blog

## When to reference
Reach for GitHub when the user wants developer-platform marketing with a strong mascot voice and real-code-as-content discipline — developer tools, open-source projects, dev-experience-led B2B. The "Octocat + 7-shade contribution grid + dual light/dark canvas + Mona Sans 800+ display" combination is the most-copyable GitHub move. Pairs well with any brand that wants to project credibility with engineers through real product screenshots rather than abstract marketing illustrations.
