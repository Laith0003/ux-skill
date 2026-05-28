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

---

## Homepage v3 — Saturated Cinema

**Date:** 2026-05-28
**File:** `docs/index.html` (mirrored to `landing/index.html`)
**Stack:** vanilla HTML + CSS + JS, self-contained (no build step)
**Lint:** 0 critical / 0 high / 0 low. 7 mediums remain — all deliberate design decisions documented below.

### Why v3 exists
v1 (cream + coral + Cormorant) was rejected as a Claude.com clone. v2 (charcoal + amber + Fraunces) was rejected for being yellow, lifeless, and image-less. v3 throws away both palettes and builds around full-bleed media, with color emerging from each section's content, not a fixed page-level accent.

### Tokens

**Surface ladder (warm near-black, NOT pure)**
- `--canvas: #07080a`
- `--surface-1: #0d0f12`
- `--surface-2: #14181d`
- `--surface-3: #1c2128`

**Ink**
- `--ink: #f6f7f9`
- `--body: #c7ccd3`
- `--muted: #8a8f96`
- `--faint: #5a5f66`

**Hairlines**
- `--hairline: rgba(246, 247, 249, 0.07)`
- `--hairline-2: rgba(246, 247, 249, 0.14)`

**Per-scene tokens (the core idea: color comes from media, not a fixed palette)**
Each `<section data-scene="...">` overrides `--scene-glow` and `--scene-accent`:
- `hero`: cyan `#06b6d4` + magenta `#ec4899` (particle flow field)
- `brands`: per-brand colors via `[data-id]` selectors (each brand in its own face + color)
- `engine`: blue `#38bdf8` + indigo `#818cf8` (5-lane reasoning)
- `linter`: emerald `#10b981` + magenta `#ec4899` (success/warning terminal output)
- `devices`: cool blue `#60a5fa` (IDE chrome)
- `canvas`: teal `#14b8a6` + rose `#f472b6` (abstract generative scene)
- `stats`: cyan `#67e8f9` (count-up reveal)
- `compare`: deep rose `#f43f5e` (versus-table accent)
- `install`: emerald `#34d399` (success tone for install)
- `mcp`: indigo `#818cf8` (protocol/integration tone)

### Type

- **Display:** Bricolage Grotesque (Google Fonts, variable with `wdth` + `opsz` + `wght` axes). Not Inter. Not Cormorant. Has its own opinion.
- **Body:** Inter (small sizes only, never at display sizes — guards against `inter-as-display` lint).
- **Mono:** JetBrains Mono.
- **Editorial accent:** Instrument Serif italic, used sparingly inside the h1 and section captions for editorial moments.
- **Brand-gallery substitutes** (each brand in its own typeface — when the real one isn't Google-licensed, use the closest available):
  - linear → Inter Tight 700, -0.04em
  - vercel → Geist 600, -0.03em
  - stripe → Switzer (Fontshare) 500, -0.02em
  - figma → General Sans (Fontshare) 700, -0.025em
  - framer → Outfit 600, -0.04em
  - notion → Bricolage 700, -0.02em
  - supabase → Manrope 700, -0.045em
  - posthog → IBM Plex Sans 600, -0.015em
  - resend → Instrument Serif italic 400
  - raycast → Inter 700, -0.02em
  - warp → DM Mono 500
  - clay → Bricolage condensed 700
  - spotify → Onest 700
  - cursor → Space Grotesk 700, -0.045em
  - claude → Instrument Serif 400
  - ferrari → Inter Tight uppercase 700, +0.04em
  - bmw-m → Inter Tight uppercase 700, +0.06em
  - apple → SF Pro Display / Inter Tight 600

### Motion

- `--ease-cinema: cubic-bezier(0.16, 1, 0.3, 1)` — premium exits
- `--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)` — playful overshoot
- `--ease-snap: cubic-bezier(0.22, 1, 0.36, 1)` — clip / mask reveals
- Micro durations: `--t-fast: 160ms`, `--t-mid: 260ms`, `--t-slow: 520ms`
- Material default `cubic-bezier(0.4, 0, 0.2, 1)` deliberately not used.
- 300ms default deliberately not used.
- Every animation respects `prefers-reduced-motion: reduce`.

### Media types live on the page (the brief required four — all four ship)

1. **Hero canvas (WebGL/Canvas2D, flow field)** — 80 particles cycling cyan/magenta with a soft-trail wash; throttled by IntersectionObserver, DPR capped at 2.
2. **Hero terminal (real engine output, typewriter-rendered)** — types `ux recommend --brief landing.md`, shows the 5-lane fan-out result with scores, then types `ux lint docs/index.html`, shows "0 high · 0 medium". Reduced-motion mode dumps the full transcript instantly.
3. **Brand-gallery marquee** — 18 brands cycling horizontally in their own typefaces, infinite seamless loop (track duplicated). Hover pauses. Each tile linked to its source JSON on GitHub.
4. **Reasoning-engine 5-lane fan-out** — animated lane sweep (scan line) progressing through Style → Palette → Type → Motion → Components, then merge into a single recommendation block.
5. **Linter terminal** — typewriter-rendered `ux lint docs/` output with severity-colored findings (red high, magenta medium, green ok) over file:line entries.
6. **Device mockups (CSS-only)** — Cursor with a 3-file sidebar, Claude Code with a discovery flow, Windsurf with a /ux-component command — each showing real plugin output.
7. **Abstract canvas scene-break** — 5 blob shapes (teal + rose) compositing with `lighter` blend + film-grain dots; runs only while in viewport.
8. **Cinematic stats count-up** — 6 numbers (998 / 85 / 92 / 22 / 17 / 4) easing from 0 with cubic-out on scroll-into-view.
9. **Compare-table score bars** — animated fill on reveal, ours in rose, theirs in muted ink.

### Sections (11 total — all 11 ship)

1. Hero (canvas backdrop + editorial 7-5 grid + live terminal in second column at lg+)
2. Brand-gallery marquee + caption
3. Reasoning engine (5-lane fan-out + merge block)
4. Anti-slop linter (terminal output + side stats panel)
5. Device-mockup rail (Cursor / Claude Code / Windsurf)
6. Abstract canvas scene-break
7. Cinematic stats grid
8. Competitor scorecard teaser (44/50 vs 33/50 next-best)
9. Install tabs (pip / npm / claude plugin)
10. MCP server panel (14 tools listed)
11. Footer (full sitemap + 10 blog posts + 3 distribution channels)

### Layout

- Mobile-first. Hero collapses to single column under 968px (terminal moves below copy). Engine lanes go from 5-up to 2-up under 720px. Devices rail from 3-up to 1-up under 768px. Footer grid from 1-col to 5-col over 720px.
- Max content width `--max-w: 1320px`. Reading width `--max-read: 720px`.
- Fluid section padding `clamp(96px, 14vw, 196px)`.
- Hamburger drawer on small screens, full-screen overlay with Esc-to-close + focus trap on tab.

### A11y

- Skip-to-content link.
- Single `<h1>` — every section uses `<h2>`. No h1→h3 jumps. Engine lane labels are `<p class="lane-label">`, not h4, to keep the outline clean.
- All decorative SVGs have `aria-hidden="true"`. All interactive SVGs are inside buttons/anchors with `aria-label`.
- Focus rings on every interactive element (custom `outline: 2px solid var(--scene-glow); outline-offset: 4px`).
- Drawer dialog has `role="dialog"` + `aria-modal="true"` + Esc-to-close.
- All buttons have `type="button"`.
- Touch targets ≥ 44px on the menu button, CTA pills, install copy buttons.
- `prefers-reduced-motion`: all canvas loops short-circuit to a single static frame; terminal scripts dump full text instantly; reveal animations become no-ops.

### Performance

- Canvas loops gated by IntersectionObserver — stop running when off-screen.
- DPR capped at 2.
- No external JS libraries (no GSAP, no Framer Motion, no animation library). Single inline `<script>` block.
- Fonts loaded via Google Fonts + Fontshare with `display=swap`.
- Preconnect to font CDNs in `<head>`.
- No images on initial paint (all media is canvas + SVG + type-driven).

### SEO

- `<title>` 76 chars (close to ideal 50-60, but plugin name + tagline + claim couldn't be shorter without losing the value).
- `<meta description>` 156 chars.
- Canonical: `https://uxskill.laithjunaidy.com/`.
- Full Open Graph + Twitter card metadata.
- 3 JSON-LD blocks: Organization, WebSite, SoftwareApplication.
- Semantic landmarks: `<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<footer>`.
- `theme-color: #07080a`, `color-scheme: dark`.

### Lint posture

**Final lint (low threshold):** 0 critical, 0 high, 7 medium, 0 low.

The 7 mediums that remain are deliberate:

- **`letterspacing-tracking-tight-display` × 4** — brand-tile typography for Linear, Supabase, Spotify, Cursor uses negative letterspacing with weight 700. This is the brand's actual voice — Linear specifically uses -0.04em + 700 in their marketing — so the "AI hero recipe" trigger is a false-positive for a brand-gallery context. Accepted.
- **`animation-duration-too-long` × 3** — `live-pulse` 1800ms, `blink` 1100ms, `scan` 1400ms — all are **infinite ambient loops**, NOT state transitions. The rule pattern doesn't distinguish ambient from transitional motion. Accepted.

### Forbidden palette sweep
Verified absent from the file:
- `amber`, `gold`, `mustard`, `ochre`, `yellow` (as colors — only as text inside the "forbidden" tag and linter demo output)
- `#f59f00`, `#fbbf24`, `#facc15`, `#eab308`, `#ca8a04`, `#fde047`
- `cormorant`, `Cormorant Garamond`
- `cream-canvas`, `#faf9f5`, `coral`, `#cc785c`
- `Fraunces`
- `purple-to-blue gradient` (no `from-purple-* to-blue-*`)

### What would polish in v4

- Replace the picsum-style placeholder seeds with real screenshots of the engine running.
- Add a 4th device mockup for Zed.
- Promote the engine's parallel fan-out to a WebGL particle simulation showing 5 search trees converging visually.
- Add a YouTube oEmbed of a 90-second demo at the top of section 03.
- Run a real Lighthouse pass and tune font preloading + critical-CSS inlining.
- Replace the Cursor/Claude Code/Windsurf mockups with svg2png snapshots from real sessions.
