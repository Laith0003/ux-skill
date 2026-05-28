# Design System Inspired by Amazon

## 1. Visual Theme & Atmosphere

Amazon's storefront is the textbook density-over-elegance e-commerce surface — the design system that does not aspire to design accolades but to conversion. Every pixel is engineered. Where peers stage products on white space and editorial photography, Amazon stages products on dense grids with prices, reviews, Prime badges, "deal of the day" callouts, and one or two yellow CTAs visible in the same viewport. The atmosphere is utilitarian to the point of austerity; chrome is gray-on-white-on-navy, accents are amber-yellow and orange, and the product imagery is small, low-prestige, and informationally complete.

The brand voltage is the yellow-orange Add-to-Cart / Buy-Now button — `#ffd814` (Add to Cart) and `#ffa41c` (Buy Now). These two specific hues are conversion-research-validated and have remained essentially unchanged for two decades. They are the brand's most-recognized chromatic asset, and replacing them with a "more modern" CTA color is widely understood as a conversion-rate regression.

Amazon Ember — the proprietary humanist sans — runs display through body at unusually small sizes (14px body, 18–24px headlines). The narrow proportions and tight x-height let the storefront cram more content per viewport than competitors using wider geometric sans. The Ember choice is part of why Amazon pages feel "dense" — the font itself is dense.

**Key Characteristics:**
- Amazon yellow (#ffd814) Add to Cart and orange (#ffa41c) Buy Now — the conversion voltage
- Amazon Ember system font — narrow humanist sans, runs display through body at small sizes
- Dense product grids — 6+ products visible above the fold
- Navy-blue header (#131921) — the persistent chrome holding search, account, cart
- Yellow-orange search bar accent — `#febd69` on the search submit button
- Star rating row — amber star icons + count in muted gray
- Prime badge — small blue cyan badge with "prime" wordmark in italic

## 2. Color Palette & Roles

### Brand Voltage
- **Add-to-Cart Yellow** (`#ffd814`): The primary purchase CTA fill. Saturated, slightly warm. Used only on Add-to-Cart and similar purchase actions
- **Buy-Now Orange** (`#ffa41c`): The "1-Click Buy" CTA — a more urgent, action-now color
- **Search Submit Yellow** (`#febd69`): The yellow square on the search bar's submit button
- **Hover Yellow** (`#f7ca00`): Slightly deeper yellow used on Add-to-Cart hover state

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Header Navy** (`#131921`): The top utility bar
- **Sub-Nav Blue** (`#232f3e`): The second-tier header strip
- **Light Surface** (`#f7f8f8`): Sectioned bands and footer
- **Hairline** (`#ddd`): 1px borders
- **Hairline Soft** (`#e7e7e7`): Subtle card divider

### Neutrals & Text
- **Ink** (`#0f1111`): Primary text — very dark, near-black
- **Body** (`#0f1111`): Same hex — Amazon doesn't separate ink and body
- **Muted** (`#565959`): Sub-headings, breadcrumbs, "X out of 5 stars" caption
- **Link Blue** (`#007185`): Text-link color — a dusty teal-cyan, not the saturated brand blue
- **Link Hover** (`#c45500`): Link hover shifts to a burnt orange — distinctive Amazon detail
- **Price Red** (`#b12704`): "Sale" or "deal" price color — a muted dark red

### Semantic
- **Prime Cyan** (`#00a8e1`): Prime badge and "prime delivery" indicators
- **Deal Red** (`#cc0c39`): Lightning deal countdown
- **Stock Green** (`#007600`): "In stock" indicator
- **Out-of-Stock Red** (`#b12704`): Same as Price Red

## 3. Typography Rules

### Font Family
- **Display + Body**: `Amazon Ember, Helvetica, Arial, sans-serif` — proprietary humanist sans with narrow proportions

### Hierarchy
- **Hero h1** — 28px Amazon Ember weight 400, line-height 1.2 — small by marketing-site standards
- **Section h2** — 21–24px weight 700
- **Product title** — 16–18px weight 400, two-line clamp
- **Price** — 21–28px weight 400 with the dollar sign superscripted
- **Star rating + count** — 14px weight 400, muted gray
- **Body** — 14px weight 400, line-height 1.5
- **Caption** — 12–13px weight 400, muted gray

### Principles
- Type stays small — Amazon refuses the 56–72px hero h1 of modern SaaS pages
- Weight 400 is the workhorse; weight 700 is reserved for prices and emphasized headlines
- Price typography uses a quirky baseline-shifted dollar sign: small `$` superscripted, large dollars, small superscripted cents. Distinctive Amazon detail
- Italic is used sparingly — the Prime wordmark is italic, "by [Author Name]" is italic

## 4. Layout & Spacing

The storefront uses a 12-column grid but rarely respects it strictly — modules sit edge-to-edge or with arbitrary padding. Section spacing is tight (24–40px between bands). Product card internal padding is 12–16px. The page is engineered for "above the fold" density — every viewport should show enough products to keep the user scanning.

## 5. Componentry Feel

- **Add-to-Cart button** — Yellow fill `#ffd814`, dark text, 3px radius, 32–40px height. The most-recognized CTA in e-commerce
- **Buy-Now button** — Orange fill `#ffa41c`, dark text, same dimensions. Sits directly below Add-to-Cart
- **Product card (dense)** — White surface, no border, product image at top (1:1 crop), title (2-line clamp), price, star rating, "FREE delivery" line, Add-to-Cart button. ~280px tall
- **Search bar** — Three-part: category dropdown (left), search input (center), yellow submit square (right). The yellow square is the signature
- **Star rating row** — Amber filled stars + muted gray "4.5 / 5" + link-blue review count. The whole row is clickable to scroll to reviews
- **Prime badge** — Cyan italic "prime" wordmark, often with a checkmark and "FREE delivery" line
- **Deal callout** — Red "Lightning Deal" banner above the product card, countdown timer below in muted gray
- **Navy header** — Site-wide top bar with logo (small), location pin, search bar (wide), account links, cart icon with count badge

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use direct purchase language ("Add to Cart", "Buy Now", "Subscribe & Save"). Quantify ("1,287 reviews", "FREE delivery Wednesday"). Lead with the price and the rating — the customer's primary decision inputs.

**Don't.** Don't write aspirational copy ("Discover the joy of…"). Don't use exclamation points in chrome. Don't replace "Add to Cart" with friendlier alternatives ("Add to bag", "Save for later" exists separately but is a different action).

## 7. Motion Vocabulary

Amazon's motion is minimal by design. The storefront is engineered for fast load and zero distraction. Hover triggers a slight color shift on buttons (50ms). Add-to-Cart click triggers a brief "Added to cart" confirmation in the upper right. Carousel hero on the homepage auto-cycles but most product pages have no motion. The brand explicitly avoids spring easing and decorative transitions.

## 8. Anti-patterns to Avoid

- **Don't replace the yellow Add-to-Cart with a brand-recolored CTA.** The specific #ffd814 yellow is conversion-validated
- **Don't sparsify the product grid.** Amazon's density is intentional, not a flaw to be "fixed"
- **Don't add motion or hover transforms to product cards.** The storefront optimizes for stillness
- **Don't replace Amazon Ember with Inter or a friendlier sans.** Ember's narrowness is part of the density
- **Don't raise the hero h1 to 56px+.** Amazon's small headlines are a deliberate density choice
- **Don't paint the chrome in saturated brand blue.** The brand uses the dusty link teal (#007185), not a saturated blue
- **Don't remove the price red.** The deal-price color (#b12704) is a brand convention; replacing with a "modern" pink or rose breaks recognition
