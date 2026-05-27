# v2 Data Schemas

Every entry in every manifest follows a strict schema so the Python engine can
query, cross-reference, and merge across them. All IDs are kebab-case strings,
globally unique within their file, and referenced across files via the `id`.

The engine's flagship `recommender.py` runs five parallel searches across these
manifests and merges the top results into a single recommended design system.

---

## `styles.json` — 75+ entries

UI/design styles (Bento, Brutalism, Editorial Warm, Glass, Neo-Brutalism, etc.)

```jsonc
{
  "id": "neo-brutalism",
  "name": "Neo-Brutalism",
  "category": "Bold Statement",                 // 12 categories total
  "philosophy": "Raw, intentionally crude, high-contrast geometry. Rejects polish in favor of presence.",
  "when_to_use": ["edgy brands", "developer tools", "creative agencies"],
  "when_to_skip": ["finance", "healthcare", "enterprise SaaS"],
  "tokens": {
    "borders": "thick (3-6px), pure black",
    "shadows": "harsh, offset, never blurred",
    "type": "wild contrast, mono+display mix",
    "color": "high saturation, primary triad",
    "radius": "0 or 8px max",
    "motion": "abrupt, no easing curves"
  },
  "exemplars": ["gumroad.com", "fey.com"],     // real-world examples
  "compatible_palettes": ["high-sat-red-yellow-black", "raw-paper-ink"],
  "compatible_type_pairs": ["jetbrains-mono-display-mono", "space-grotesk-jetbrains"],
  "compatible_industries": ["dev-tools", "creative-agency", "indie-saas"],
  "ai_slop_risk": "low",                       // low | medium | high
  "notes": "Don't add gradients. Don't soften edges. The whole point is the edge."
}
```

## `palettes.json` — 170+ entries

```jsonc
{
  "id": "claude-warm-editorial",
  "name": "Claude Warm Editorial",
  "mode": "light",                              // light | dark | auto
  "tone": ["warm", "editorial", "magazine"],
  "colors": {
    "canvas": "#faf9f5",
    "surface": "#efe9de",
    "ink": "#181715",
    "body": "#3d3d3a",
    "muted": "#6c6a64",
    "primary": "#cc785c",
    "primary_active": "#a9583e",
    "hairline": "rgba(20,20,19,0.08)",
    "success": "#2f7d32",
    "warning": "#c2710a",
    "danger": "#b3261e"
  },
  "contrast": {
    "ink_on_canvas": 19.2,                      // AA threshold: 4.5
    "body_on_canvas": 11.8,
    "primary_on_canvas": 3.8,
    "primary_on_dark": 5.4
  },
  "compatible_styles": ["editorial-warm", "magazine-modern"],
  "exemplars": ["claude.com", "stripe.com (warm-mode)"]
}
```

## `type-pairs.json` — 65+ entries

```jsonc
{
  "id": "cormorant-inter",
  "name": "Cormorant × Inter × JetBrains Mono",
  "display": {
    "family": "Cormorant Garamond",
    "weights": [500, 600, 700],
    "source": "Google Fonts",
    "license": "OFL",
    "url": "https://fonts.google.com/specimen/Cormorant+Garamond"
  },
  "body": {
    "family": "Inter",
    "weights": [400, 500, 600, 700],
    "source": "Google Fonts",
    "license": "OFL"
  },
  "mono": {
    "family": "JetBrains Mono",
    "weights": [400, 500],
    "source": "Google Fonts",
    "license": "OFL"
  },
  "character": ["editorial", "warm", "literary", "trustworthy"],
  "compatible_styles": ["editorial-warm", "magazine-modern"],
  "ai_slop_risk": "low",
  "notes": "Inter as body is fine; only flagged when used as DISPLAY (the slop signal)."
}
```

## `components.json` — 120+ entries

```jsonc
{
  "id": "stat-card-magnetic",
  "name": "Magnetic Stat Card",
  "category": "Data Display",                   // 14 categories
  "purpose": "Show one metric with optional delta and sparkline. Magnetic hover for engagement.",
  "anatomy": ["label", "value", "delta-pill", "sparkline (optional)", "footer-note (optional)"],
  "states": ["default", "hover", "loading", "empty", "error"],
  "tokens_used": ["surface", "ink", "primary", "muted", "hairline"],
  "motion": ["magnetic-pointer-track (max 6px)", "delta-pill-fade-up"],
  "a11y": ["label is the visual h-tag mapped to actual h3", "delta has aria-label with direction"],
  "code_refs": {
    "react": "examples/react/StatCard.tsx",
    "vue": "examples/vue/StatCard.vue",
    "blade": "examples/blade/stat-card.blade.php"
  },
  "compatible_styles": ["editorial-warm", "bento-modern", "glass-luxe"]
}
```

## `industries.json` — 170+ entries

```jsonc
{
  "id": "fintech-neobank",
  "name": "Fintech — Neobank",
  "category": "Financial Services",
  "characteristics": ["high trust requirement", "regulatory disclosures", "balance/transaction primary UI"],
  "audience_signals": ["mobile-first", "literacy varies", "anxiety about money"],
  "recommended_styles": ["editorial-trust", "minimal-confident", "monochrome-precise"],
  "avoid_styles": ["brutalism", "neo-brutalism", "playful-gradient"],
  "recommended_palettes": ["monochrome-confident", "deep-navy-cream", "ink-paper-warm"],
  "recommended_type_pairs": ["inter-display-inter", "sohne-inter"],
  "tone_guidance": "Specific, calm, never celebratory of debt. Use exact amounts in lists; never abstract them.",
  "compliance_notes": ["KYC flows", "AML disclosures", "FDIC/SAMA badge per region"],
  "exemplars": ["mercury.com", "ramp.com", "wise.com"]
}
```

## `chart-types.json` — 30+ entries

```jsonc
{
  "id": "horizon-chart",
  "name": "Horizon Chart",
  "category": "Time Series",
  "when_to_use": ["dense time-series", "multiple series side-by-side", "anomaly detection"],
  "when_to_skip": ["sparse data", "non-technical audience"],
  "encoding": "Color band + density",
  "stacks": {
    "d3": "d3-horizon-chart",
    "recharts": "custom composition",
    "vega-lite": "supported via mark:rect"
  },
  "a11y": ["always pair with table view", "use ordinal palette, never rainbow"]
}
```

## `tech-stacks.json` — 20+ entries

```jsonc
{
  "id": "nextjs-15-app-router",
  "name": "Next.js 15 (App Router)",
  "category": "React Meta-Framework",
  "tier": "production",
  "languages": ["TypeScript", "JavaScript"],
  "ssr": true,
  "rsc": true,
  "compatible_styling": ["tailwind-4", "css-modules", "vanilla-extract"],
  "scaffold_command": "npx create-next-app@latest --typescript --tailwind --app",
  "ux_plugin_target": "/ux-design --stack nextjs",
  "notes": "Use RSC for static layout; islands for interactive."
}
```

## `ux-guidelines.json` — 110+ entries

```jsonc
{
  "id": "hicks-law",
  "name": "Hick's Law",
  "category": "Decision Cost",                  // 14 categories
  "source": "Hick (1952), Hyman (1953)",
  "principle": "Decision time grows logarithmically with choice count.",
  "application": [
    "Limit primary actions to one per surface.",
    "Chunk secondary options behind progressive disclosure.",
    "Default selections reduce perceived choice."
  ],
  "anti_patterns": ["20+ item nav", "10-option settings dropdown"],
  "compatible_components": ["primary-cta", "stepped-form", "progressive-disclosure"]
}
```

## `motion-presets.json` — 50+ entries (our moat)

```jsonc
{
  "id": "fade-up-12px",
  "name": "Fade-Up 12px",
  "category": "Entry",                          // 8 motion categories
  "tokens": {
    "duration_ms": 360,
    "easing": "cubic-bezier(0.16, 1, 0.3, 1)", // out-expo
    "transform_from": "translateY(12px)",
    "transform_to": "translateY(0)",
    "opacity_from": 0,
    "opacity_to": 1
  },
  "stacks": {
    "framer_motion": "{ initial: { y: 12, opacity: 0 }, animate: { y: 0, opacity: 1 }, transition: { duration: 0.36, ease: [0.16, 1, 0.3, 1] } }",
    "gsap": "gsap.from(el, { y: 12, opacity: 0, duration: 0.36, ease: 'expo.out' })",
    "css": "@keyframes fade-up { from { transform: translateY(12px); opacity: 0; } }"
  },
  "reduced_motion": "instant — fade only, no transform",
  "performance": "transform + opacity only — GPU composited"
}
```

## `anti-patterns.json` — 30+ entries (our moat — ported from `ux-lint.sh`)

```jsonc
{
  "id": "inter-as-display",
  "name": "Inter used as display font",
  "severity": "high",                           // critical | high | medium | low
  "category": "Typography",
  "detection": {
    "type": "regex",
    "pattern": "font-family:\\s*['\"]?Inter['\"]?[^;]+\\s+(font-size:\\s*([4-9]\\d|\\d{3,})px|text-(5xl|6xl|7xl|8xl|9xl))",
    "flags": "im",
    "scope": ["css", "tsx", "jsx", "vue", "html"]
  },
  "why": "Inter is a body font tuned for screen legibility at small sizes. As display, it reads as generic AI output.",
  "fix": "Pair Inter (body) with a real display: Cormorant Garamond, Fraunces, Domine, Space Grotesk display, Druk."
}
```

## `brands/*.json` — 72 entries (our moat — converted from existing DESIGN.md)

```jsonc
{
  "id": "stripe",
  "name": "Stripe",
  "category": "Fintech Infrastructure",
  "year_observed": 2026,
  "philosophy": "Geometric precision + warm gradients. Documentation as marketing.",
  "design_language": {
    "type": { "display": "Sohne", "body": "Sohne", "mono": "Sohne Mono" },
    "color_primary": "#635bff",
    "color_canvas": "#ffffff",
    "color_ink": "#0a2540",
    "color_accent_gradient": "linear-gradient(135deg, #635bff 0%, #00d4ff 100%)",
    "radius": [4, 8, 12, 24],
    "spacing": "8-based",
    "motion_signature": "soft-spring, max 200ms"
  },
  "trademark_signals": [
    "subtle wireframe annotations",
    "side-by-side code/output",
    "horizontal hairline dividers"
  ],
  "components_observed": ["pricing-table-horizontal", "product-nav-mega", "blog-quote-warm"],
  "exemplar_pages": ["stripe.com/payments", "stripe.com/billing"],
  "ai_slop_avoided": ["no purple-to-blue chrome-y gradients", "no inter as display"]
}
```

---

## Cross-reference rules (enforced by the recommender)

1. `styles.json` entries reference `palettes.json` and `type-pairs.json` IDs in `compatible_palettes` / `compatible_type_pairs`.
2. `industries.json` entries reference `styles.json` and `palettes.json` IDs.
3. `components.json` entries reference `styles.json` IDs in `compatible_styles`.
4. `brands/*.json` entries are queryable as exemplars by all other manifests.
5. Every ID is unique within its file. The engine validates this on load.
6. Missing cross-references warn (not fail) — the engine surfaces gaps as TODOs.

---

## Versioning

Each manifest has a top-level `_meta` block:

```jsonc
{
  "_meta": {
    "version": "2.0.0",
    "entries": 75,
    "last_updated": "2026-05-27",
    "source": "ux-skill v2 — Python pivot",
    "schema_version": "1.0"
  },
  "entries": [ /* ... */ ]
}
```
