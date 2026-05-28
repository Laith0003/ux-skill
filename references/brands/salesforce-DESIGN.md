# Design System Inspired by Salesforce

## 1. Visual Theme & Atmosphere

Salesforce's marketing surface is the rare enterprise-CRM site that opens with a cartoon. The atmosphere is deliberately disarming — a B2B sales-cloud platform that puts illustrated characters (Astro, Codey, Cloudy, Einstein) on its hero rather than a screenshot of dashboards or a c-suite portrait. The character cast is one of the most-recognized brand assets in enterprise software, and it carries the warmth of the otherwise serious chrome.

Cloud Blue (#00a1e0) is the chromatic anchor — saturated, slightly cyan-shifted, used on primary CTAs and on the wordmark's cloud silhouette. Every product is a "cloud" (Sales Cloud, Service Cloud, Marketing Cloud, Commerce Cloud), and each cloud has its own gradient-accented illustration. The cloud taxonomy is part of the brand's information architecture; replacing it with a flat "products" naming convention breaks recognition.

Salesforce Sans — the proprietary humanist sans — runs everything. It is wider and friendlier than Inter or Helvetica, with rounded terminals and slightly open apertures. Combined with the pill-shaped CTA buttons (full-rounded radius), the system reads as approachable enterprise rather than corporate severe.

**Key Characteristics:**
- Cloud Blue (#00a1e0) as the primary chromatic CTA color
- Astro and the character cast as illustrated heroes — disarming, character-led brand
- Salesforce Sans — proprietary friendly humanist sans
- Pill-shaped (full radius) primary CTA buttons
- Cloud-named product taxonomy — every product is a "Cloud"
- Trailhead — the learning platform — has its own ranger-badge visual language
- Mega-menu navigation with cloud icons for each product

## 2. Color Palette & Roles

### Primary
- **Cloud Blue** (`#00a1e0`): The primary CTA fill, wordmark cloud color, hover-link
- **Deep Blue** (`#0070d2`): Hover state for the primary CTA
- **Navy** (`#16325c`): The brand's deep blue, used for primary headlines and dark surfaces

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f3f3f3`): Alternating section bands
- **Surface Card** (`#fafaf9`): Card backgrounds
- **Hairline** (`#dddbda`): 1px borders

### Neutrals & Text
- **Ink** (`#16325c`): The brand's deep navy — used for headlines
- **Body** (`#3e3e3c`): Default body text
- **Muted** (`#706e6b`): Captions, breadcrumbs
- **Link** (`#0070d2`): Inline body links

### Semantic
- **Success** (`#4bca81`): Confirmation banners, "completed" badges
- **Warning** (`#ffb75d`): Caution banners
- **Error** (`#c23934`): Validation errors
- **Info** (`#16325c`): Information banners (uses the brand navy)

### Cloud Gradient Tints
Each Salesforce "Cloud" has a paired gradient: Sales (blue-to-cyan), Service (red-to-orange), Marketing (purple-to-pink), Commerce (orange-to-yellow). These are decorative on cloud-illustration surfaces only — never as section backgrounds.

## 3. Typography Rules

### Font Family
- **Display + Body**: `Salesforce Sans, Helvetica Neue, Arial, sans-serif` — proprietary friendly humanist sans

### Hierarchy
- **Hero h1** — 48–64px Salesforce Sans weight 700, line-height 1.1
- **Section h2** — 36–42px weight 700
- **Card title** — 22–28px weight 600
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 600

### Principles
- Weight 700 for hero h1 — the brand commits to heavier display weights than peers
- Salesforce Sans's wider proportions are what make the brand read as friendly enterprise
- Body sits at 16–18px — slightly larger than Material defaults, giving a leisurely reading pace

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Hero sections use a 7-5 or 6-6 split with the character illustration on the right. Product card grids run 3-up at desktop. Section padding is 80–120px vertical.

## 5. Componentry Feel

- **Primary CTA (pill)** — Cloud Blue fill, white text, full-pill radius, 44px height, weight-600 label
- **Secondary CTA** — Transparent fill, 2px Cloud Blue border, blue text, pill radius
- **Cloud product card** — White surface, hairline border, 8px radius, internal padding 32px. Cloud icon at top (illustrated, gradient-accented), product name, description, CTA
- **Character hero illustration** — Astro, Codey, Cloudy, or Einstein in a hand-illustrated scene — often outdoor or playful contexts (mountain, campfire, beach)
- **Trailhead badge** — Hexagonal ranger-style badge for the learning platform — gradient fills, character icons
- **Mega-menu** — Multi-column dropdown with cloud icons on the left, product list, and a "Featured" panel on the right
- **Footer** — Soft surface, multi-column site-map, country/region switcher

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use friendly enterprise language ("Get started with Sales Cloud"). Lead with the customer's outcome ("Close more deals, faster"). Use sentence case for buttons. Quantify benefit ("150,000+ companies grow with Salesforce").

**Don't.** Don't drop the character voice. Don't write corporate-speak ("Leverage AI-driven insights to optimize your sales pipeline"). Don't use exclamation points except in onboarding moments.

## 7. Motion Vocabulary

Characters have idle animations on landing pages — Astro might blink, float gently, or wave. Hover lifts on cards use a soft 200ms ease-out with a slight scale (1.02). Mega-menu drops with a 250ms ease-out. The character animations are signature; reducing them to static illustration flattens the brand.

## 8. Anti-patterns to Avoid

- **Don't replace the character illustrations with stock 3D renders.** The cast is the brand voice
- **Don't pair the Cloud Blue with a second saturated accent.** The blue is the brand voltage
- **Don't square the pill CTAs.** Full-pill radius is the brand's CTA shape
- **Don't remove the cloud iconography from product naming.** Every product is a Cloud
- **Don't reduce Salesforce Sans to Inter.** The wider, friendlier proportions are part of the brand voice
- **Don't lighten the deep navy headline color.** The brand's #16325c is part of the "trust" signal
- **Don't use the gradient cloud tints as section backgrounds.** They are decorative on illustrations only
