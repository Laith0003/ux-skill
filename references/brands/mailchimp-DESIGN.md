# Design System Inspired by Mailchimp

## 1. Visual Theme & Atmosphere

Mailchimp's web presence is the marketing-platform-with-personality chrome — Cavendish Yellow (#ffe01b) as the brand voltage, the chimp mascot Freddie as the brand character, hand-illustrated quirky heroes, and a typography stack that pairs Cooper Light serif display with a clean Helvetica Neue body. The atmosphere is warm, weird, and deliberately small-business-friendly. Where peer marketing platforms (HubSpot, Salesforce Marketing Cloud, Klaviyo) lean into enterprise polish, Mailchimp leans into idiosyncratic charm — the brand has long bet on personality as moat.

The hand-illustrated heroes are the brand's most-distinctive visual asset. Mailchimp's illustration style is rough, quirky, and deliberately not-polished: a person riding a strange creature, a hand reaching into a pot of something inexplicable, a chimp throwing a ball. The illustrations don't always literally illustrate the marketing message; they create a tonal atmosphere of "this is a brand that's having fun." Replacing this style with generic 3D renders or smooth corporate illustration flattens the brand entirely.

Freddie the chimp is the mascot. He appears in special-occasion contexts (the home page hero, error pages, holiday banners) and has accumulated a brand personality over the years — Freddie waves, winks, gestures. The mascot's quirky weirdness is what makes the brand feel like a person rather than a SaaS company.

**Key Characteristics:**
- Cavendish Yellow (#ffe01b) — brand voltage on chrome and certain hero panels
- Freddie the chimp — illustrated brand mascot
- Hand-illustrated quirky heroes — rough, personality-rich, deliberately not-polished
- Cooper Light serif display + Helvetica Neue body — distinctive type pairing
- Rectilinear cards (0–8px radius) — Mailchimp commits to flat edges
- Small-business friendly tone — warm, weird, never enterprise-corporate

## 2. Color Palette & Roles

### Primary
- **Cavendish Yellow** (`#ffe01b`): The brand voltage — used on hero banners, on the chrome wordmark, and as a generous background tone on certain pages. CTAs may also use yellow with dark text
- **Pure Black** (`#241c15`): The ink color — a near-black with a slight warm undertone
- **Pure White** (`#ffffff`): The canvas

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Yellow Tone** (`#ffe01b`): Yellow surface accent on featured sections
- **Surface Soft** (`#f4f0e8`): Warm-tinted alternate
- **Hairline** (`#dfdcd1`): 1px borders

### Neutrals & Text
- **Ink** (`#241c15`): Primary text
- **Body** (`#3a342a`): Default body text
- **Muted** (`#5e5a4f`): Captions
- **Muted Soft** (`#857f73`): Fine-print

### Illustration Accent Tints
- Hand-illustrated heroes use a muted earthy palette — terracotta, sage, ochre, mustard
- Freddie's color is a specific Mailchimp-tan brown

### Semantic
- **Success** (`#1ec27e`): Green
- **Warning** (`#e8a93a`): Amber (matches the illustration ochre)
- **Error** (`#c83d3d`): Red

## 3. Typography Rules

### Font Family
- **Display**: `Cooper Light, "Cooper Std Light", Georgia, serif` — distinctive rounded serif, the brand's most-recognized type choice
- **Body**: `Helvetica Neue, Arial, sans-serif` — clean neutral sans

### Hierarchy
- **Hero h1** — 56–80px Cooper Light weight 300, line-height 1.05
- **Section h2** — 36–48px Cooper Light weight 300
- **Card title** — 20–24px Helvetica Neue weight 600
- **Body** — 16–18px Helvetica Neue weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px Helvetica Neue weight 700, often uppercase

### Principles
- Cooper Light at weight 300 (Light) for display — the rounded-serif character is the brand's signature
- Sans body in Helvetica Neue at weight 400 — neutral counterbalance to the quirky serif
- The serif/sans split signals "personality + craft"
- Tracking neutral (0)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 80–120px vertical. Feature card grids run 3-up at desktop. Hero sections often use a 6-6 split with the illustration on the right or above the headline.

## 5. Componentry Feel

- **Freddie mascot illustration** — Quirky illustrated chimp character that appears in special contexts
- **Primary CTA (yellow rect)** — Cavendish Yellow fill, dark text, 4–8px radius, 44px height, weight-700 uppercase label
- **Secondary CTA** — Transparent fill, 2px black border, dark text
- **Hand-drawn hero** — Full-bleed or large card with a quirky hand-illustrated scene
- **Cooper Light display headline** — Large serif headline at 56–80px Cooper Light weight 300
- **Feature card (rectilinear)** — White surface, 1px hairline border, 4–8px radius, internal padding 24px

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use warm-weird small-business-friendly language ("Send better email", "Make your marketing more you"). Reference small-business contexts (coffee shops, online boutiques, side hustles). Use sentence case for chrome. Lean into idiosyncratic charm.

**Don't.** Don't write enterprise-corporate copy. Don't sanitize the quirky illustration personality. Don't drop Freddie from the brand presence.

## 7. Motion Vocabulary

Hand-illustrated quirky motion — Freddie the chimp blinks and gestures on idle. Hand-drawn illustrations have subtle wiggle animations on hero pages. Hover lift on cards is restrained (1.01 scale + 200ms). The motion budget is quirky-warm, never corporate-smooth.

## 8. Anti-patterns to Avoid

- **Don't replace the hand-illustrated quirk with generic 3D renders.** The illustration personality is brand
- **Don't sanitize Freddie the chimp.** The mascot's quirky weirdness is brand
- **Don't drop the Cooper Light serif display.** It is the signature pairing
- **Don't tint Cavendish Yellow.** The specific saturated #ffe01b is brand
- **Don't use Cooper Light at weight 400 or above.** Weight 300 (Light) is the brand standard
- **Don't pair the chrome with a saturated tech-blue accent.** The yellow + earthy-illustration palette is brand
- **Don't write enterprise-formal microcopy.** Mailchimp is deliberately warm-weird
