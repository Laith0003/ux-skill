# Design System Inspired by LinkedIn

## 1. Visual Theme & Atmosphere

LinkedIn's web interface is the professional network's chrome — the "newspaper of work" rendered as a card-based feed on a tinted off-white canvas. The atmosphere is white-collar formal, deliberate, and unflashy. Where consumer social networks (Instagram, TikTok, X) lean into media-rich edge-to-edge content and motion, LinkedIn leans into rectangular cards on a tinted canvas, with serif-adjacent humanist sans typography and a single chromatic anchor — LinkedIn Blue (#0a66c2). The design choices communicate "this is your workplace identity, treat accordingly."

The off-white canvas (#f3f2ef) is one of LinkedIn's most-distinctive choices. Most social platforms use pure white or near-black for their backgrounds; LinkedIn uses a warm tinted gray that gives the feed cards a sense of lifting off the page. The tint is barely perceptible but does real work: cards in white visibly "float" against it, and the eye is led to scan card-by-card rather than swimming in undifferentiated white space.

LinkedIn Blue (#0a66c2) is the chromatic CTA color, used on Connect/Follow buttons, on links, and on the wordmark. It is a specific corporate-leaning blue — slightly darker and less saturated than consumer blues (Facebook's #1877f2 or Twitter's #1da1f2). The corporate restraint is the signal.

**Key Characteristics:**
- LinkedIn Blue (#0a66c2) — primary CTA, link color, wordmark
- Off-white canvas (#f3f2ef) — the tinted-gray background that makes cards lift
- Pill-shaped (full-radius) Connect / Follow buttons — the signature CTA shape
- Card-based feed grammar — every post, job, announcement in a rounded white card
- Reaction picker — 6 colored emoji-style reactions (Like, Celebrate, Support, Love, Insightful, Funny)
- Profile header with banner photo + circular profile photo overlapping at the bottom-left
- Left-rail profile summary card on feed pages — sticky as you scroll

## 2. Color Palette & Roles

### Primary
- **LinkedIn Blue** (`#0a66c2`): Primary CTA, link color, wordmark
- **Deep Blue** (`#004182`): Press / hover state for the primary
- **Light Blue** (`#70b5f9`): Inverted CTA on dark surfaces (used in InMail, premium chrome)

### Surface & Background
- **Canvas** (`#f3f2ef`): The tinted off-white background that distinguishes the feed
- **Card Surface** (`#ffffff`): Card backgrounds — pure white against the tinted canvas
- **Card Hover** (`#f4f2ee`): Slightly darker tint on card hover
- **Hairline** (`#d9d9d6`): 1px card borders and dividers

### Neutrals & Text
- **Ink** (`rgba(0, 0, 0, 0.9)`): Primary text — `#000000` at 90% alpha
- **Body** (`rgba(0, 0, 0, 0.9)`): Same
- **Muted** (`rgba(0, 0, 0, 0.6)`): Captions, metadata
- **Muted Soft** (`rgba(0, 0, 0, 0.4)`): Disabled states
- **On Primary** (`#ffffff`): Text on LinkedIn Blue CTAs

### Reaction Colors
- **Like Blue** (`#378fe9`): The default reaction
- **Celebrate Yellow** (`#dca40d`): Celebration reaction
- **Support Purple** (`#915dd9`): Support reaction (added 2020)
- **Love Red** (`#df5a45`): Heart reaction
- **Insightful Amber** (`#e6a23a`): Lightbulb reaction
- **Funny Teal** (`#41b85b`): Smiley reaction

### Semantic
- **Success** (`#057642`): Green confirmation
- **Warning** (`#915907`): Amber caution
- **Error** (`#cc1016`): Red error

## 3. Typography Rules

### Font Family
- **Display**: `LinkedIn Brand Sans` (proprietary) or `Source Sans Pro` as substitute
- **Body**: `Source Sans Pro, system-ui, sans-serif` — wide humanist sans
- **Mono**: `Source Code Pro` — for code snippets in technical posts

### Hierarchy
- **Hero h1 (marketing pages)** — 48–64px LinkedIn Brand Sans weight 700, line-height 1.1
- **Profile header name** — 24px weight 600
- **Post body** — 14–16px Source Sans Pro weight 400, line-height 1.5
- **Card title** — 18–20px weight 600
- **Caption / metadata** — 12–14px weight 400, muted color
- **Button label** — 14–16px weight 600

### Principles
- Weight 600 is the workhorse for headlines and labels
- Body sits at 14–16px — slightly larger than X/Twitter, tighter than long-form publications
- Tracking neutral (0) across the system
- Italic appears in inline emphasis only; the brand avoids italic body copy

## 4. Layout & Spacing

The feed uses a 3-column layout at desktop: left rail (profile summary card + community/group cards), center column (the feed itself), right rail (news / trending / ads). The center column is ~540px wide; rails are ~280px each.

Card padding is 16–24px internal. Card-to-card vertical gap is 8–12px. Section spacing on marketing pages runs 80–120px between bands.

## 5. Componentry Feel

- **Primary CTA (Connect, Follow, Apply)** — LinkedIn Blue fill, white text, full-pill radius, 32px height. The signature CTA shape
- **Secondary CTA (Message, More)** — Transparent fill, 2px LinkedIn Blue border, blue text, full-pill radius
- **Feed post card** — White surface, 8px radius, 1px hairline border, 16px padding. Author row (avatar 48px + name + caption) at top, body content, reaction count row, action row (Like, Comment, Share, Send)
- **Profile header card** — Banner image (top), circular profile photo (overlapping at bottom-left), name + headline + metadata below
- **Reaction picker** — Floating row of 6 colored reaction icons that appears on long-press of the Like button
- **Job card** — Company logo + role title + company name + location + posted-date — clickable to detail
- **Left-rail profile summary** — Sticky card on feed pages with profile photo, name, "Who's viewed your profile" count, "Impressions of your post" count
- **Footer** — Multi-column site-map at the bottom of marketing pages; on the feed, no footer (infinite scroll)

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use professional-but-warm language ("Connect with [Name]", "Save job for later"). Treat the user as a working adult. Quantify ("3 mutual connections"). Lead with the action ("Apply now").

**Don't.** Don't use playful microcopy that breaks the workplace tone. Don't use exclamation points in chrome. Don't anthropomorphize the algorithm ("we picked this for you"). Don't translate "Connect" to other social-platform verbs.

## 7. Motion Vocabulary

Motion is functional and minimal. Hover triggers 150ms color shift on links and CTAs. Reaction picker animates in with a soft 200ms ease-out + slight scale. Reactions on press scale up briefly (1.1) and back. The feed lazy-loads content with no explicit loading spinner — new cards appear as you reach the end. No spring overshoots elsewhere.

## 8. Anti-patterns to Avoid

- **Don't replace the off-white canvas with pure white.** The tint is what makes cards lift
- **Don't square the pill CTAs.** Full-radius is the brand's CTA shape
- **Don't replace LinkedIn Blue with a brighter consumer blue.** The specific corporate-leaning blue is part of the recognition
- **Don't animate the feed cards on scroll.** The brand reads as serious workplace, not TikTok
- **Don't increase card radii above 8–12px.** The slight rounding is the brand's softness budget
- **Don't drop the reaction picker colors.** The 6-color palette is brand-specific
- **Don't use friendly mascots or playful illustrations.** LinkedIn's brand voice is white-collar formal
