# Design System Inspired by 1Password

## 1. Visual Theme & Atmosphere

1Password's web presence is security-trust-as-friendly chrome — a deep navy (#0a2540) as the primary anchor, a soft sky blue (#5b8def) as the brand accent, and illustration-driven heroes featuring people in everyday secure contexts. The atmosphere is friendly enterprise security. Where security peers (Bitwarden, LastPass, NordVPN) often lean into alarm-bell imagery (locks, padlocks, warning shields, red CTAs), 1Password leans into the calm-confidence of "this just works." The illustrations show families sharing passwords, developers managing API keys, parents helping their kids set up accounts — security depicted as everyday, not as cybersecurity-thriller.

The deep navy (#0a2540) is the brand's trust anchor. It is a specific saturated dark blue — neither pure black nor a saturated bright blue — and it grounds the brand on every page. The sky blue (#5b8def) is the bright accent — softer than peer-tech blues, slightly periwinkle, used on CTAs and key UI moments to bring lift without alarming the user.

The vault icon — the blue safe-door visual metaphor — is the brand's product anchor. Every product mockup shows the 1Password vault interface, with categorized items (Logins, Secure Notes, Credit Cards, Identities) in a left-sidebar layout. The vault is the product; the chrome shows it as the everyday tool it is.

**Key Characteristics:**
- 1Password Navy (#0a2540) — deep blue trust anchor
- 1Password Sky (#5b8def) — bright accent on CTAs
- Vault icon — the blue safe-door visual metaphor
- Friendly illustration heroes — everyday secure-living contexts
- Soft rounded cards (8–16px radius)
- Inter typography across chrome
- Never alarm-bell imagery — calm-confidence over scare-tactics

## 2. Color Palette & Roles

### Primary
- **1Password Navy** (`#0a2540`): The trust anchor — used on dark sections and as ink
- **1Password Sky** (`#5b8def`): The bright accent on CTAs
- **Sky Hover** (`#3d6dd6`): Press state

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f7f9fc`): Slightly cool alternating sections
- **Surface Card** (`#f0f3f8`): Card hover state
- **Hairline** (`#e0e5ec`): 1px borders

### Neutrals & Text
- **Ink** (`#0a2540`): Primary text — uses the brand navy
- **Body** (`#2c3a4d`): Default body text
- **Muted** (`#6b7280`): Captions
- **Muted Soft** (`#9da3ad`): Fine-print

### Semantic
- **Success** (`#22c55e`): Green
- **Warning** (`#f59e0b`): Amber
- **Error** (`#ef4444`): Red — used sparingly, never as alarm imagery

## 3. Typography Rules

### Font Family
- **Display + Body**: `Inter, system-ui, sans-serif` — modern humanist sans

### Hierarchy
- **Hero h1** — 48–64px Inter weight 700, line-height 1.1
- **Section h2** — 32–40px weight 700
- **Card title** — 20–24px weight 600
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 600

### Principles
- Weight 700 for hero h1
- Body sits at 16–18px for friendly reading
- Tracking slightly negative at display sizes (-0.5px)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 80–120px vertical. Feature card grids run 3-up at desktop.

## 5. Componentry Feel

- **Primary CTA (sky pill)** — 1Password Sky fill, white text, full-pill radius, 44px height, weight-600 label
- **Vault icon illustration** — Blue safe-door metaphor used throughout the brand presence
- **Feature card (soft radius)** — White surface, 12–16px radius, hairline border, internal padding 24px. Icon, headline, description, optional CTA
- **Hero illustration family** — Illustrated family/team sharing passwords or setting up accounts
- **Security callout band** — Section showing security feature highlights (Watchtower, security audits, zero-knowledge architecture)

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use calm-confidence security language ("Your passwords, organized"). Reference everyday contexts (family, work, travel). Avoid scare-tactic security language.

**Don't.** Don't use alarm-bell copy ("Your passwords are at risk!"). Don't sanitize the friendly-illustration personality. Don't write enterprise-security speak in consumer contexts.

## 7. Motion Vocabulary

Gentle micro-interactions — vault icons may have a subtle "unlock" animation on hover, the lock icon clicks closed/open with a 150ms spring. Hero illustrations have idle gestures (a hand reaching for a phone, a family member smiling). The brand reads as calm-friendly.

## 8. Anti-patterns to Avoid

- **Don't lean into alarm-bell security imagery.** Locks, warnings, red shields read off-brand
- **Don't replace 1Password Navy with a brighter saturated tech-blue.** The deep navy is the trust anchor
- **Don't sharpen card radii below 8px.** Approachable security
- **Don't sanitize the illustration heroes to generic enterprise stock.** The hand-illustrated personality is brand
- **Don't use weight 800 for hero h1.** Weight 700 is the brand standard
- **Don't pair Sky Blue with a saturated red CTA.** The blue is the brand voltage
- **Don't anthropomorphize the vault as a "watchdog" or "guardian".** The brand is friendly-everyday, not security-thriller
