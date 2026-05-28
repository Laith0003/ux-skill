# Design System Inspired by Twilio

## 1. Visual Theme & Atmosphere

Twilio's web presence is communication-API developer chrome — Twilio Red (#f22f46) as the chromatic anchor, white canvas with developer-documentation aesthetic, and code snippets as the dominant feature visualization. The atmosphere is API-first developer-friendly. Where peer SaaS marketing (Salesforce, HubSpot) leans into character illustrations and case-study photography, Twilio leans into code — every page shows the product as code-in-action, with curl/Node/Python/Go language tabs as the hero treatment.

The developer-first commitment is the brand's most-important positioning decision. Twilio's marketing site reads more like docs.twilio.com than salesforce.com — sidebar TOCs, version pickers, language switchers, and code blocks dominate the visual atmosphere. The brand's open-source Paste design system is visible in the product chrome and creeps into the marketing pages.

Twilio Red is the chromatic anchor. It is a specific saturated coral-red (#f22f46) — slightly warm, distinctive against typical CTA reds. The red appears on CTAs, on the wordmark, and as syntax-highlighting accent inside code blocks (Twilio API calls render the SDK class name in the brand red).

**Key Characteristics:**
- Twilio Red (#f22f46) — chromatic voltage on CTAs and wordmark
- White canvas with developer-documentation aesthetic
- Code-snippet-as-hero — language tabs for curl/Node/Python/Go/Java
- Inter typography for chrome, JetBrains Mono for code
- Twilio Paste design system patterns
- Feature card grids with API request/response mockups
- Developer-doc sidebar layout pattern across product family pages

## 2. Color Palette & Roles

### Primary
- **Twilio Red** (`#f22f46`): The brand voltage — CTAs, wordmark, code syntax accent
- **Red Hover** (`#c12338`): Press state

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f4f4f6`): Alternating section bands
- **Surface Card** (`#ebebef`): Card hover state
- **Code Block Dark** (`#0d122b`): Dark surface for code blocks
- **Hairline** (`#e1e3ea`): 1px borders

### Neutrals & Text
- **Ink** (`#0d122b`): Primary text — uses a deep dark blue
- **Body** (`#3a3f51`): Default body text
- **Muted** (`#606b85`): Captions
- **Muted Soft** (`#9da3b3`): Fine-print

### Code Syntax Colors
- **Keyword Red** (`#f22f46`): Class names, SDK keywords
- **String Green** (`#22c55e`): String literals
- **Number Amber** (`#f59e0b`): Numeric literals
- **Comment Gray** (`#9da3b3`): Comments

### Semantic
- **Success** (`#22c55e`): Green
- **Warning** (`#f59e0b`): Amber
- **Error** (`#f22f46`): Twilio Red doubles as error

## 3. Typography Rules

### Font Family
- **Display + Body**: `Inter, system-ui, sans-serif`
- **Mono**: `JetBrains Mono, Courier New, monospace`

### Hierarchy
- **Hero h1** — 48–64px Inter weight 700, line-height 1.1
- **Section h2** — 32–40px weight 700
- **Card title** — 20–24px weight 600
- **Body** — 16–18px weight 400, line-height 1.5
- **Code** — 13–14px JetBrains Mono weight 400, 1.6 line-height
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 600

### Principles
- Weight 700 for hero h1
- Mono for code snippets and API method references inline in body copy
- Tracking neutral (0)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 80–120px vertical. Feature card grids run 3-up at desktop. Product family pages use a 9-3 split with content on the left and sidebar TOC on the right.

## 5. Componentry Feel

- **Primary CTA (red rect)** — Twilio Red fill, white text, 4–8px radius, 44px height, weight-600 label
- **Secondary CTA** — Transparent fill, 2px Twilio Red border, red text
- **Code snippet (tabbed)** — Dark surface (`#0d122b`), language tabs at the top (curl, Node, Python, Go, Java), syntax-highlighted code in JetBrains Mono, copy button top-right
- **API request/response card** — Side-by-side request/response code snippets demonstrating an API call
- **Developer doc sidebar** — Hierarchical TOC with expand/collapse rows, current-page indicator (a 2px red bar on the left)
- **Feature card (soft radius)** — White surface, 8–12px radius, hairline border, internal padding 24px

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use developer-direct language ("Add SMS in 5 lines of code"). Reference programming languages and SDK methods. Quantify capability ("99.999% uptime"). Lead with the code.

**Don't.** Don't write marketing-aspirational copy. Don't use exclamation points in chrome. Don't sanitize the developer-doc aesthetic.

## 7. Motion Vocabulary

Functional developer-grade motion — code-snippet tabs have a 150ms underline slide. Hover lifts on cards are subtle (1.01 scale). API request/response chrome animates with a slight type-in effect on landing. The brand reads as devtools-functional.

## 8. Anti-patterns to Avoid

- **Don't replace the code-snippet hero with marketing illustration.** The brand is API-first
- **Don't tint Twilio Red to a softer coral.** The saturated red is brand
- **Don't sanitize the developer-documentation aesthetic.** Twilio reads as devtools-first
- **Don't sharpen card radii below 4px.** Modest softness is the brand's friendliness budget
- **Don't drop the language tabs on code snippets.** Multi-language is brand IA
- **Don't pair Twilio Red with a second saturated accent.** The red is the voltage
- **Don't use weight 600 for hero h1.** Weight 700 is the brand standard
