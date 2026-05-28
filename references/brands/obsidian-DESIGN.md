# Obsidian — DESIGN.md

## Overview
Obsidian is the personal-knowledge-management tool that worships the knowledge graph. Canvas is a deep slate-purple-black (`#202020`) in dark mode (the default), or a parchment-cream (`#f6f3ee`) in light. The signature visual element is the force-directed graph of nodes — purple glowing dots connected by faint white edges — that appears as both the product's centerpiece and the marketing hero. Type is a precise grotesk (Inter / Söhne) with markdown-derived hierarchy: H1 / H2 / H3 styled to mirror raw markdown rendering. The brand reads as 'private, infinite, sovereign' — the antithesis of cloud-collab.

## Color
- **Primary:** `#a882ff` — Obsidian purple (CTAs + knowledge-graph node glow)
- **Canvas:** `#202020` — Slate-purple-black (dark mode, the default)
- **Canvas light:** `#f6f3ee` — Parchment-cream (light mode)
- **Ink (dark):** `#dcddde`
- **Ink (light):** `#1a1a1a`
- **Accent:** `#7f6df2` — Secondary purple for emphasis and active states
- **Body (dark):** `#bcbcc1`
- **Muted:** `#888892`
- **Hairlines:** `rgba(255,255,255,0.08)` on dark; `rgba(26,26,26,0.10)` on light
- **Syntax (markdown):** purple H1, blue links, green strings, orange code

## Typography
- **Display:** Inter / Söhne, weight 700, 36–56px hero (modest, markdown-rendered scale)
- **Sub-display:** weight 600, 22–28px section heads
- **Body:** Inter, weight 400, 16px, 1.6 line-height
- **Caption:** weight 500, 13–14px metadata
- **Mono:** JetBrains Mono, 14px for code excerpts and inline markdown

## Spacing & rhythm
8-base (8/16/24/32/48/64/96). Section padding 64–96px. Marketing pages use markdown-style rendering — H1 + H2 + body paragraphs in a 720px column with the knowledge-graph hero filling the upper viewport.

## Motion signature
Knowledge-graph nodes drift in slow physics simulation — gentle force-directed jiggle, ~0.2 Hz. Edges glow faintly purple on hover. New-node animation pulses out from center over 600ms. Markdown preview updates use a 120ms cross-fade. The product chrome is otherwise still — sovereignty is calmness.

## Components observed
- `knowledge-graph-hero` — force-directed node-graph with purple glow
- `plugin-grid-card` — community plugin tile grid (1500+ plugins)
- `markdown-preview-pane` — split markdown source + rendered preview
- `feature-screenshot-block` — real product screenshot embedded in essay
- `theme-gallery-card` — community theme thumbnail
- `pricing-tier-comparison-table` — Free / Catalyst / Sync table
- `button-primary-purple` — purple-fill CTA
- `footer-minimal-dark` — dark footer with vault metaphor

## Trademark signals
- Force-directed knowledge graph — purple glowing nodes connected by faint white edges on slate-purple-black — marketing hero + product centerpiece + decorative motif
- Dark slate-purple canvas (`#202020`) as default — Obsidian is dark-mode-first; light mode is the second-class citizen
- Markdown-rendered hierarchy on the marketing page itself — H1s with the same styling as in-product H1, code-blocks in identical syntax-highlight palette
- Plugin-grid ecosystem showcase — 1500+ community plugins displayed as a dense card grid reinforces the 'infinitely extensible' message
- Long-form feature explanations with screenshot-as-illustration — actual product screenshots embedded in editorial-length paragraphs

## What they DON'T do
- No pure-black canvas — slight purple-tint slate (`#202020`) is the differentiator from generic dark-mode SaaS
- No flat-illustration knowledge graph — must look like the real product output, physics-simulated and glowing
- No saturated accent colors — single purple voltage; teal/orange/red break sovereignty-and-focus voice
- No cloud-sync as primary value prop — 'your notes, on your machine, forever' is the lead; Obsidian Sync is a paid add-on
- No stock illustrations — every visual is a product screenshot, a knowledge-graph render, or a plugin tile
- No emoji, no friendly mascot, no SaaS-marketing hero gradient

## Exemplar pages
- https://obsidian.md/
- https://obsidian.md/about
- https://obsidian.md/plugins
- https://help.obsidian.md/

## When to reference
Reach for Obsidian when the user wants dark-mode-first PKM/local-first software with strong sovereignty messaging — note-taking tools, research apps, indie developer-power-user products. The "slate-purple canvas + force-directed knowledge graph + markdown-rendered marketing prose + dense plugin grid" combination is the most-copyable Obsidian move. Pairs well with brands that want to position local-first ownership against cloud-default competitors.
