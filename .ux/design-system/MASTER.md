---
project: ux-plugin
last_updated: "2026-05-28T10:59:09Z"
ux_skill_version: 2.0.0-alpha.1
---

# Design system — MASTER

## Brief

- **Project type:** marketing-site
- **Audience:** frontend engineers, design-engineers, AI coding tool users (Cursor, Claude Code, Windsurf)
- **Primary goal:** —
- **Tone:** editorial, cinematic, confident, precise, dark
- **Must have:** dark-mode, mobile-first-responsive, a11y-AA, no-cormorant-no-coral-no-cream, fraunces-variable-display, inter-tight-body, scroll-pinned-scenes, single-amber-accent
- **Forbidden:** claude, claude-warm-editorial, claude-com-clone, cream-canvas, cream, coral-primary, coral, cormorant-garamond, cormorant, three-equal-cards, inter-as-display, purple-to-blue-gradient, john-doe, lorem-ipsum, emoji-in-ui, marketing-verbs
- **Reference brands:** linear, vercel, stripe-docs, the-browser-company
- **Stack:** vanilla-html-css-js
- **Region:** global
- **Success metric:** 0 high-severity ux-lint findings on the generated HTML + reads as distinctly NOT Claude-derived to a critical viewer

## Recommendation

### Style: Swiss International

- **id:** swiss-international
- **philosophy:** Grid is law. Type does the heavy lifting. Decoration is failure.
- **category:** Minimalist / Swiss
- **when to use:** editorial publications, design portfolios, cultural institutions, premium consultancies
- **exemplars:** bureauborsche.com, kasper-florio.ch, experimentaljetset.nl
- **tokens:** borders, color, motion, radius, shadows, type

### Palette: Linear Graphite

- **id:** linear-graphite
- **tone:** minimal, technical, precise
- **body:** `#3f4147`
- **canvas:** `#ffffff`
- **danger:** `#c52f1a`
- **hairline:** `rgba(10,11,13,0.08)`
- **ink:** `#0a0b0d`
- **muted:** `#6f7178`
- **primary:** `#5e6ad2`
- **primary_active:** `#4651b8`
- **success:** `#1c8a4f`
- **surface:** `#f4f5f8`
- **warning:** `#b85900`
- **contrast:** body_on_canvas=9.4, ink_on_canvas=20.1, primary_on_canvas=4.6, primary_on_dark=4.8

### Type pair: Young Serif (400) x Inter (400, 500, 600) x JetBrains Mono (400, 500)

- **id:** young-serif-inter-jetbrains
- **display:** Young Serif (400)
- **body:** Inter (400, 500, 600)
- **mono:** JetBrains Mono (400, 500)
- **character:** chunky, confident, editorial-modern, distinctive

### Motion presets (5)

- Fade-Up 12px (cubic-bezier(0.16, 1, 0.3, 1), 360)
- Fade-In Pure (cubic-bezier(0.4, 0.0, 0.2, 1), 200)
- Fade-Up 24px Slow (cubic-bezier(0.16, 1, 0.3, 1), 560)
- Slide-Up From Clip (cubic-bezier(0.22, 1, 0.36, 1), 480)
- Scale-Pop 95 to 100 (cubic-bezier(0.16, 1, 0.3, 1), 220)

### Components (12)

- mobile-bottom-nav — Navigation
- tab-bar-underline — Navigation
- select-combobox — Forms
- date-picker-inline — Forms
- button-magnetic — Actions
- fab-mobile — Actions
- bento-card-tall — Card Patterns
- loading-page-shell — States
- heatmap-calendar — Charts
- notification-preferences-matrix — Settings
- stat-card-with-chart-bg — Data Display
- presence-indicator-typing — States

### Brand exemplars (5)

- airbnb — Consumer / Lifestyle / Retail
- airtable — Productivity / Collaboration
- apple — Consumer / Lifestyle / Retail
- bmw — Automotive
- bmw-m — Automotive

### Anti-pattern guardrails (51 active)

- **by severity:** critical=3, high=20, low=9, medium=19
- **by category:** A11y=12, Color=6, Content=8, Layout=6, Motion=4, Performance=1, Quality=6, Typography=6, Visual=2

## Rationale

- Industry: SaaS — Developer Tools
- Style: Swiss International
- Palette: Linear Graphite
- Type pair: Young Serif × Inter × JetBrains Mono
- Motion presets considered: 5
- Compatible components: 12
- Guardrails active: 51 anti-pattern rules

## Pages persisted

- (auto-populated as pages are added)
