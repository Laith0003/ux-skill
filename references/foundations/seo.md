# SEO foundation

> One-sentence promise: SEO is not bolted on. Every public-web output ships with the meta surface, structured data, semantic HTML, and performance contract that lets the page be found, understood, and ranked.

## Principles

1. **Discoverability over decoration** — A beautiful page nobody finds is a private art piece. Every public surface earns its discoverability through structured markup, sound semantics, and the performance budget. Visual polish never wins against a missing title tag or a slow LCP.

2. **Structured data is mandatory** — Every page ships JSON-LD describing what it is. `Organization` on every page. `WebSite` on the homepage. Per-page type schema (`Article`, `Product`, `WebPage`, `SoftwareApplication`) on every other page. Crawlers should never have to guess.

3. **The title is the headline of the search result** — Write `<title>` like a headline, not a folder label. It is the single most weighted line on the page. 50–60 characters, primary keyword first, brand last, unique per page. If the title is generic, the page is invisible.

4. **Performance IS SEO** — Core Web Vitals are ranking signals. A page that loads slowly, jumps under the user, or stalls under interaction is a page that ranks lower no matter how well-written. LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 are not stretch goals — they are minimum viable shipping numbers.

5. **Accessibility IS SEO** — Crawlers parse the same semantic tree screen readers parse. Pass the accessibility foundation and you pass 70% of on-page SEO automatically. Semantic HTML, descriptive alt text, sequential heading hierarchy, real `<button>` and `<a>` elements — these serve crawlers and assistive tech identically.

6. **Internationalization signals matter** — Pages that target multiple locales must declare them explicitly. `<html lang>` on every page. `hreflang` link tags for every alternate locale. URL-path locale segmentation (`/en/`, `/ar/`). Cookies and geo-IP redirects are invisible to crawlers and hostile to users sharing links.

7. **Social cards are not optional** — Every public URL gets a hand-tuned Open Graph image and meta set. A link pasted into a chat or a social post is the first preview of the brand most viewers will ever see. Auto-generated default cards are a tax on every share.

8. **The URL is part of the design** — URLs are read, copied, spoken aloud. Hyphens not underscores. Lowercase. Words that describe the page. 50–70 characters. The slug is design surface — it appears in the search result, in the address bar, in the share preview.

9. **Fresh content beats clever content** — Crawlers reward pages that update. Date-stamp articles. Mark modified time. Refresh evergreen pages quarterly. A 4-year-old page with no `dateModified` is treated as stale even if the copy is still accurate.

10. **Mobile is the default crawler** — The primary crawl is mobile. If the mobile rendering is missing markup, missing content, or noticeably slower, that is the version that gets indexed. Build mobile-first or accept lower rankings.

## The mandatory head surface

The exact `<head>` template every landing page MUST ship with. Below are the rules; the full reusable template appears in the "Output template" section.

**Document basics — required on every page:**

- `<meta charset="UTF-8">` — first child of `<head>`. Must appear within the first 1024 bytes.
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` — mandatory. Never `user-scalable=no`; pinch-zoom must remain available (overlap with accessibility).
- `<html lang="...">` — mandatory; matches the actual page locale (`en`, `ar`, `fr-CA`).
- `<html dir="rtl">` when the language reads right-to-left.

**Title and description — required on every page:**

- `<title>` — 50–60 characters. Primary keyword first, brand suffix last (`Page topic | Brand`). Unique per page across the entire site. No site-wide template that produces "Home — Brand" on 30 different routes.
- `<meta name="description" content="...">` — 150–160 characters. Action-led ("Learn how to…", "Compare…", "Get started with…"). Includes primary keyword naturally, never stuffed. Unique per page. The description is the SERP snippet; treat it as marketing copy with a budget.

**Canonical — required on every page:**

- `<link rel="canonical" href="https://domain.com/full-path">` — mandatory. Absolute URL, not relative. Self-referential on the primary version; points to the canonical when the page is a duplicate or filtered variant.
- The canonical URL must match the trailing-slash policy of the site. Mixing `/about` and `/about/` as canonicals is a duplicate-content signal.

**Robots — required on every page:**

- `<meta name="robots" content="index,follow">` on every public, indexable page.
- `<meta name="robots" content="noindex,nofollow">` on staging, preview, internal admin, and search-result pages.
- `<meta name="robots" content="noindex,follow">` on search-result pages where you still want link equity to flow but do not want the results themselves indexed.

**Color and theme — required on every page:**

- `<meta name="theme-color" content="#000000" media="(prefers-color-scheme: light)">`
- `<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">`
- `<meta name="color-scheme" content="light dark">` when the site supports both.

**Internationalization — required when supporting multiple locales:**

- `<link rel="alternate" hreflang="en" href="https://domain.com/en/path">`
- `<link rel="alternate" hreflang="ar" href="https://domain.com/ar/path">`
- `<link rel="alternate" hreflang="x-default" href="https://domain.com/en/path">` — the fallback for unmatched locales. Mandatory when any `hreflang` is set.

**Favicons — full set required:**

- `<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">`
- `<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">`
- `<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">`
- `<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#000000">` — for monochrome pin icon.
- `<link rel="manifest" href="/site.webmanifest">` — for PWA installability.
- 512×512 maskable PNG referenced inside the manifest for installable contexts.

**Performance hints — required:**

- `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` for any font CDN.
- `<link rel="preload" href="/fonts/Sans-Regular.woff2" as="font" type="font/woff2" crossorigin>` for any blocking font.
- `<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">` for the LCP image.
- `<link rel="dns-prefetch" href="https://analytics.domain.com">` for any non-critical third party.

## Open Graph (mandatory)

The full OG meta set every public page must include. Open Graph carries the link preview wherever the URL is pasted — a missing OG image is a missed first impression.

**Required tags — every page:**

- `<meta property="og:title" content="...">` — same content as `<title>` or a tighter variant.
- `<meta property="og:description" content="...">` — same content as `<meta name="description">` or a tighter variant.
- `<meta property="og:image" content="https://domain.com/og/page.jpg">` — absolute URL, never relative.
- `<meta property="og:image:width" content="1200">` — mandatory for layout reservation in the preview.
- `<meta property="og:image:height" content="630">` — mandatory.
- `<meta property="og:image:alt" content="Descriptive alt for the OG image">` — mandatory; accessibility carries into share previews.
- `<meta property="og:url" content="https://domain.com/full-path">` — absolute canonical URL.
- `<meta property="og:type" content="website|article|product|profile|book|video.movie">` — pick the closest match.
- `<meta property="og:site_name" content="Brand name">` — consistent across every page.
- `<meta property="og:locale" content="en_US">` — full locale code with underscore separator.
- `<meta property="og:locale:alternate" content="ar_JO">` — repeatable; one per supported locale.

**Image specs:**

- 1200×630px exactly. Wider than 2:1 gets cropped in some preview surfaces; narrower than 2:1 gets letterboxed.
- ≤ 8MB file size; ≤ 1MB is preferred for the share-preview cold path.
- JPG for photographic content, PNG for solid-color or text-heavy designs.
- Brand mark visible in the safe zone — the inner 1080×500 region. Edges may crop on some surfaces.
- One OG image per page minimum. Per-route ideally. Auto-generated default cards across an entire site are a brand tax.
- Text on the OG image must remain legible at 600×315px preview size — minimum 36px font for any body copy, 60px for primary headline.

**When `og:type="article"` — add:**

- `<meta property="article:author" content="https://domain.com/team/jane-doe">` — author profile URL, not just a name.
- `<meta property="article:published_time" content="2026-05-24T09:00:00+00:00">` — ISO 8601 with timezone.
- `<meta property="article:modified_time" content="2026-05-24T14:00:00+00:00">` — ISO 8601 with timezone; updated on every meaningful edit.
- `<meta property="article:tag" content="loyalty">` — repeatable; one per topic tag.
- `<meta property="article:section" content="Engineering">` — single section name.

**When `og:type="product"` — add:**

- `<meta property="product:price:amount" content="99.00">`
- `<meta property="product:price:currency" content="USD">` — ISO 4217 currency code.
- `<meta property="product:availability" content="in stock">`

## Twitter / X cards (mandatory)

The X card protocol overlays Open Graph but uses its own namespace. Set both; do not assume one falls back to the other.

**Required tags — every page:**

- `<meta name="twitter:card" content="summary_large_image">` — for marketing surfaces, blog posts, product pages, and any surface with a hero image.
- `<meta name="twitter:card" content="summary">` — for narrow content such as utility pages, error pages, terms.
- `<meta name="twitter:title" content="...">` — up to 70 characters; usually the `<title>` value.
- `<meta name="twitter:description" content="...">` — up to 200 characters; usually the `<meta name="description">` value.
- `<meta name="twitter:image" content="https://domain.com/og/page.jpg">` — absolute URL; 1200×628 minimum (Twitter crops slightly differently than Open Graph).
- `<meta name="twitter:image:alt" content="...">` — mandatory; matches `og:image:alt`.
- `<meta name="twitter:site" content="@brandhandle">` — the brand handle if one exists.
- `<meta name="twitter:creator" content="@authorhandle">` — for articles, the author's handle.

## Structured data (JSON-LD)

Embed `<script type="application/ld+json">` blocks describing the page. JSON-LD is preferred over inline microdata or RDFa because it lives in `<head>` separate from layout and is easier to maintain.

Multiple JSON-LD blocks per page are allowed and encouraged — one per schema type.

### `Organization` — every page

Required fields: `@type`, `name`, `url`, `logo`. Strongly recommended: `sameAs` (array of social profile URLs), `contactPoint`, `address`.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Brand name",
  "url": "https://domain.com",
  "logo": "https://domain.com/logo.png",
  "sameAs": [
    "https://x.com/brandhandle",
    "https://linkedin.com/company/brand",
    "https://github.com/brand"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer support",
    "availableLanguage": ["English", "Arabic"]
  }
}
```

Common errors: omitting `logo` URL (required for knowledge-panel eligibility); referencing a logo smaller than 112×112px; pointing `url` to a redirect rather than the canonical origin; `sameAs` URLs that 404.

Validation approach: every `Organization` block must parse as valid JSON, all URLs must resolve to 200 OK, `logo` must be ≥ 112×112px and on the canonical origin.

### `WebSite` — homepage only

Provides the site-wide search action and brand identity. Required: `@type`, `name`, `url`. Strongly recommended: `potentialAction` for the sitewide search.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Brand name",
  "url": "https://domain.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://domain.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

Common errors: placing `WebSite` schema on every page (it belongs on the homepage); omitting `query-input` from the search action; pointing the search URL to a route that does not actually exist.

### `WebPage` / `Article` / `Product` / `SoftwareApplication` — per-page type

Pick the most specific type that matches the page. A generic `WebPage` is the fallback; specific types unlock richer SERP features.

**`Article` — required fields:** `@type`, `headline` (≤ 110 chars), `image` (≥ 1200×675), `datePublished`, `dateModified`, `author` (Person or Organization), `publisher` (Organization with logo).

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article title that matches the page H1",
  "image": ["https://domain.com/article-hero.jpg"],
  "datePublished": "2026-05-24T09:00:00+00:00",
  "dateModified": "2026-05-24T14:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author name",
    "url": "https://domain.com/team/author-slug"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Brand name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://domain.com/logo.png"
    }
  }
}
```

Common errors: `headline` longer than 110 characters; `image` array missing or under-sized; `dateModified` omitted on edited articles; `author` set to a string instead of a `Person` object; `publisher.logo` smaller than 600×60px.

**`Product` — required fields:** `@type`, `name`, `image`, `description`, `sku` or `gtin`, `brand`, `offers`.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product name",
  "image": ["https://domain.com/product-1.jpg"],
  "description": "Description matching the page meta description.",
  "sku": "SKU-12345",
  "brand": {
    "@type": "Brand",
    "name": "Brand name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://domain.com/product/slug",
    "priceCurrency": "USD",
    "price": "99.00",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2026-12-31"
  }
}
```

Common errors: omitting `priceValidUntil` (warning, not error, but reduces eligibility); using a different price in JSON-LD than appears on the page; setting `availability` without an actual inventory check.

**`SoftwareApplication` — required fields:** `@type`, `name`, `operatingSystem`, `applicationCategory`, `offers` (or `Free` indicator).

### `BreadcrumbList` — every page beyond root

Required: `@type`, `itemListElement` array with `@type: "ListItem"` entries containing `position`, `name`, and `item` (URL).

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://domain.com" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://domain.com/blog" },
    { "@type": "ListItem", "position": 3, "name": "Article title" }
  ]
}
```

Common errors: omitting `position`; the final item including an `item` URL (the last crumb is the current page and is named only); URLs that mismatch the page hierarchy.

### `FAQPage` — when the page has a FAQ section

Required: array of `Question` items, each with a `Question.name` and a `Question.acceptedAnswer.Answer.text`.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How long does setup take?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Setup takes under five minutes when you already have a phone number to verify."
    }
  }]
}
```

Common errors: FAQ schema applied to pages that do not actually display the FAQ visibly (a markup violation); answers that are too long (cap at ~300 words); promotional copy in the answer field.

### `Person` — creator and author pages

Required: `@type`, `name`. Strongly recommended: `image`, `url`, `jobTitle`, `worksFor`, `sameAs`.

### `HowTo` — for step-by-step content

Required: `@type`, `name`, `step` array with `HowToStep` entries containing `name` and `text`. Strongly recommended: `image` per step, `tool`, `supply`, `totalTime` (ISO 8601 duration).

### `VideoObject` — for embedded videos

Required: `@type`, `name`, `description`, `thumbnailUrl`, `uploadDate`, `duration` (ISO 8601), `contentUrl` or `embedUrl`.

## Semantic HTML

Crawlers parse the DOM the same way assistive technologies do. Semantic HTML carries the meaning that classes and styles cannot.

- **Single `<h1>` per page** — the page's primary message. Two `<h1>` tags is a structural error.
- **Hierarchy: `<h1>` → `<h2>` → `<h3>`** — never skip levels. Going from `<h2>` directly to `<h4>` breaks the outline and signals a malformed document.
- **Landmarks** — `<header>`, `<nav>`, `<main>` (exactly one per page), `<aside>`, `<footer>`, `<section>` (always with an accessible name via `aria-labelledby` or `aria-label`), `<article>`.
- **Lists** — `<ul>` for unordered groups, `<ol>` for ordered. Never `<div>` styled to look like a list. Crawlers count list items as a signal of structured content.
- **Buttons vs links** — `<button>` triggers actions, `<a>` navigates to URLs. Never `<div onclick="...">`. A `<button>` that navigates and an `<a>` that mutates state are both wrong.
- **Forms** — `<label for="...">` for every input. `<fieldset>` + `<legend>` for grouped inputs (radio groups, checkbox groups). Placeholder is never a label.
- **Tables** — `<thead>`, `<tbody>`, `<th scope="col">` for column headers, `<th scope="row">` for row headers. `<caption>` for the table's purpose. Never use tables for layout.
- **Time** — `<time datetime="2026-05-24T09:00:00+00:00">May 24</time>`. The machine-readable `datetime` attribute uses ISO 8601 with timezone.
- **Addresses** — `<address>` for contact blocks (postal address, email, phone). Not for generic addressing within prose.
- **Images** — `<picture>` for art-direction (different crops at different breakpoints); `srcset` + `sizes` for resolution switching at the same crop.
- **`<meta name="generator">`** — omit unless the framework demands it. Generic generator tags add noise without value.

## Image discipline (SEO ∩ a11y)

Images are evaluated by crawlers for context, performance impact, and accessibility. Get all three right at once.

- **Alt text** — descriptive on every content image. `alt=""` (empty) ONLY on decorative images. Never `alt="image"` or `alt="photo"` — meaningless and counts as missing.
- **Lazy loading** — `loading="lazy"` for every image below the fold. Never `loading="lazy"` on the LCP image (it hurts LCP timing); use `fetchpriority="high"` instead.
- **Async decoding** — `decoding="async"` on every image to avoid blocking render.
- **Width and height** — `width` and `height` attributes mandatory on every `<img>`. They reserve layout space and prevent Cumulative Layout Shift. CSS overrides the rendered size; the attributes provide the aspect ratio.
- **Responsive images** — `<picture>` for art-direction (different crops at different breakpoints); `srcset` + `sizes` for resolution switching at the same crop.
- **Modern formats** — AVIF or WebP for primary, JPG fallback via `<picture>`. Format hierarchy: AVIF → WebP → JPG.
- **Filename SEO** — `red-pricing-card-hover.webp` not `IMG_4828.webp`. Hyphens, descriptive, lowercase. The filename is a ranking signal for image search.
- **Captions** — `<figcaption>` inside `<figure>` for any content image that benefits from a caption. The caption is parsed as related context.
- **LCP image preload** — `<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">` in `<head>` for the largest above-fold image.
- **Hero image with crop fallback** — `<picture>` with breakpoint sources keyed to the design system's breakpoints. Never let a desktop crop ship to mobile.

## URL discipline

URLs are read by humans, copied into emails, dictated over phones, and parsed by crawlers. Treat them as design surface.

- **Lowercase only** — `/about-us`, never `/About-Us` or `/aboutUs`. Mixed-case URLs cause duplicate-content issues when servers treat them as different paths.
- **Hyphens, not underscores** — word separators are hyphens. Underscores are concatenation; hyphens are tokenization.
- **Trailing-slash policy** — pick one (`/about` or `/about/`) and enforce it site-wide. Mixed policy creates duplicate content. Enforce via 301 redirect from the non-canonical form.
- **Length** — 50–70 characters total, including the domain. URLs longer than 75 characters truncate in search results and look untrustworthy.
- **Primary keyword in the slug** — the slug reflects the page's primary topic in 2–5 words.
- **No URL params for content** — `/blog/post-title` not `/blog?id=42`. Query params are for filters and tracking, never for content routing.
- **Redirect old URLs** — 301 (permanent) when the URL changes. Never delete a working URL without a redirect. Never break a working URL.
- **Redirect chain limit** — at most one hop. `/old` → `/new` is fine. `/old` → `/intermediate` → `/new` loses link equity at each hop.
- **No file extensions** — `/about` not `/about.html`. Extensions tie URLs to implementation; routes outlast file formats.
- **No session IDs in URLs** — never `?sid=abc123` in canonical URLs. Use cookies for session state.

## Performance (Core Web Vitals are ranking signals)

The three vital metrics are not aspirational. They are minimum viable. A page that misses any one of them ships with a known ranking penalty.

**LCP — Largest Contentful Paint — target ≤ 2.5s**

The time until the largest above-fold element renders. Usually the hero image, occasionally a heading.

- Preload the LCP image in `<head>` with `<link rel="preload" as="image" fetchpriority="high">`.
- Serve modern formats (AVIF or WebP) with size hints (`width`, `height`) so layout reserves space immediately.
- Avoid lazy-loading the LCP image. Lazy-load is for below-fold content only.
- Preconnect to the font CDN if web fonts block the headline render.
- Inline critical CSS for the above-fold paint; defer the rest.

**INP — Interaction to Next Paint — target ≤ 200ms**

The time from a user input (tap, click, key) until the next frame paints with the response visible. INP replaces FID as the interactivity metric.

- Avoid long tasks on the main thread. Break work into chunks; use `requestIdleCallback` for non-urgent work.
- Defer non-critical third-party scripts. Analytics, chat widgets, A/B testing — load these after the first user interaction.
- Use `passive: true` on scroll and touch event listeners.
- Memoize expensive recomputations; do not run `JSON.parse` on a 2MB payload during a click handler.

**CLS — Cumulative Layout Shift — target ≤ 0.1**

The sum of unexpected layout shifts across the page's lifetime. Shifts caused by user-initiated interactions do not count; shifts caused by late-arriving content do.

- Declare `width` and `height` on every image and embed.
- Reserve space for ads and dynamic content via `min-height` on the container.
- Avoid inserting content above existing content. New banners, cookie consent — render below, or push down on first paint, not on second.
- Use `font-display: optional` or `font-display: swap` with a metric-matched fallback to prevent FOIT/FOUT shifts.
- Never animate `top`, `left`, `width`, `height` — animate `transform` and `opacity` only (overlap with motion foundation).

**Concrete tactics across all three:**

- Preload critical fonts with `<link rel="preload" as="font" type="font/woff2" crossorigin>`.
- Preconnect to font CDN with `<link rel="preconnect" href="..." crossorigin>`.
- Defer non-critical CSS with `<link rel="preload" as="style" onload="this.rel='stylesheet'">`.
- Inline critical above-fold CSS in `<head>` (≤ 14KB).
- Lazy-load below-fold images and iframes with `loading="lazy"`.
- Avoid synchronous third-party scripts above the fold. Defer or async every external script.
- Use HTTP/2 or HTTP/3 multiplexing — minimize critical-path round trips.
- Set explicit `Cache-Control` headers on every static asset.

## Internationalization (when supporting > 1 locale)

When the site ships in more than one language, every locale signal must be explicit. Crawlers do not infer language from content.

- **`<html lang="...">` mandatory** — matches the actual page locale. Use BCP 47 codes (`en`, `ar`, `fr-CA`, `es-MX`).
- **`<link rel="alternate" hreflang="...">`** — one per locale, on every localized page. Each page must declare every alternate, including itself.
- **`<link rel="alternate" hreflang="x-default">`** — the fallback for unmatched locales. Mandatory when any `hreflang` is set. Usually points to the primary English version.
- **Locale in URL path** — `/en/`, `/ar/`, `/fr-ca/`. Never cookie-based or geo-IP-based locale routing — crawlers and link shares cannot follow these.
- **RTL pages set `dir="rtl"`** on `<html>`, never on `<body>` or a wrapping `<div>`. RTL must be a document-level signal.
- **Locale-aware formatting** — dates, numbers, currency render per locale (`٢٠٢٦` vs `2026`, `1,234.56` vs `1.234,56`, `$99.00` vs `99,00 €`). Hardcoded en-US formatting on a localized page is a UX defect that crawlers also notice.
- **Translated `<title>`, `<meta description>`, `og:*`, alt text** — every public-facing string ships translated. English meta on an Arabic page is a duplicate-content signal and a UX failure.
- **Translated structured data** — `name`, `description`, `headline` values inside JSON-LD render in the locale of the page.

## Robots and sitemaps

The crawler's entry points. Both must exist and both must be honest.

**`/robots.txt`** at the root, allowing the marketing surface and disallowing internal routes.

```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /staging/
Disallow: /api/
Disallow: /search
Disallow: /preview/

Sitemap: https://domain.com/sitemap.xml
```

- Always reference the sitemap from `robots.txt` so first-time crawlers find it.
- Disallow search-result pages (typically `/search` or `?q=`) to avoid indexing thin, low-value variations.
- Disallow auth-gated routes and admin interfaces.
- Never `Disallow: /` on production by accident — the most common catastrophic deploy mistake.

**`/sitemap.xml`** at the root, auto-generated, updated on every deploy.

- ≤ 50,000 URLs per file. Beyond that, split into a sitemap index that references multiple sitemaps.
- Each URL includes `<loc>` (absolute URL), `<lastmod>` (ISO 8601 date), `<changefreq>` (hint, not a guarantee), `<priority>` (0.0–1.0 relative).
- Include only canonical URLs. Never include 301-redirect sources or `noindex` pages.
- Sitemaps for images, videos, and news content live in separate files.

**Staging and preview environments:**

- `<meta name="robots" content="noindex,nofollow">` on every page.
- `X-Robots-Tag: noindex, nofollow` HTTP header as a belt-and-suspenders backup (the meta tag relies on JavaScript execution in some cases; the header is unconditional).
- Basic-auth or IP-allowlist gating prevents crawlers from ever reaching the page.
- Never reuse the production canonical on staging — `<link rel="canonical">` on staging points to the staging URL.

## Anti-patterns (SEO slop — do not ship)

- **Keyword stuffing** — repeating the primary keyword 15 times in body copy. Crawlers detect lexical density and penalize.
- **Duplicate titles and descriptions** — the same `<title>` on 30 different pages. Every page gets a unique title and description.
- **Empty alt text on content images** — `alt=""` is for decorative images only. Content images with empty alt are crawler-invisible and screen-reader-invisible.
- **Single-page apps with no SSR/SSG** — client-rendered routes that ship an empty `<div id="root">` to crawlers index as blank. Pre-render every public route.
- **Decorative gradient text inside `<h1>`** — visually striking, semantically lost when the gradient drops out in screen readers or in dark-mode preview cards. Use real characters.
- **Lazy-loading above-the-fold imagery** — `loading="lazy"` on the LCP image delays the metric and reduces ranking.
- **Synchronous third-party tags blocking LCP** — analytics, chat, A/B testing scripts loaded synchronously above the fold. Defer everything non-critical.
- **"Click here" link text** — the link text is a ranking signal. Use descriptive text: "Read the pricing details" not "Click here."
- **Hidden text** — color-matching-background text, `display: none` SEO copy, off-screen text-indent hacks. Crawlers detect and penalize.
- **Broken redirect chains** — more than one hop loses link equity. Audit and flatten chains to a single 301.
- **Mixed-case URLs** — `/About` and `/about` treated as different pages is a duplicate-content split.
- **Multiple H1s per page** — exactly one H1 per page. The H1 is the page's primary message.
- **Skipping heading levels** — `<h2>` → `<h4>` breaks the outline. Use CSS to style sizes, not the wrong tag.
- **Generic OG images per-site** — one OG image used across an entire site is a missed first impression. Per-page minimum; per-route ideal.
- **Sitemap missing from robots.txt** — first-time crawlers may never find it. Always reference.
- **Missing canonical on any indexable page** — every public page declares its canonical, even if self-referential.
- **`noindex` on a page in the sitemap** — contradictory signals confuse crawlers. Pages in the sitemap are indexable; pages that are not, do not appear in the sitemap.
- **Auto-translated content marked as original** — machine translation without human review marked as the original language version is a quality penalty. Mark translated pages with `hreflang` and improve the translation.
- **Infinite scroll without paginated URLs** — content loaded via scroll alone is invisible to crawlers. Provide paginated routes (`/blog/page/2`) or sitemap entries for every item.
- **`window.location` redirects in JavaScript** — crawlers may not execute. Use HTTP 301/302 redirects.
- **Doorway pages** — multiple pages targeting near-identical queries that funnel to the same destination. Consolidate into a single canonical page.

## Per-page-type checklists

Each public page type has a defined SEO surface. Use the matching checklist on every output.

### Marketing landing page

- Full head surface (charset, viewport, title, description, canonical, robots, theme-color, color-scheme, favicons, preload hints).
- Open Graph large image card; per-page `og:image` at 1200×630.
- `Organization` JSON-LD; `WebPage` JSON-LD with the page's primary purpose.
- All CWV thresholds met — LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.
- Single H1 matching the page's primary headline.
- Persuasive `meta description` action-led ("Get started…", "See how…", "Compare…").
- Trust signals (testimonials, logos, ratings) marked up with `Review` or `AggregateRating` when authentic.

### Blog post / article

- `Article` JSON-LD with `headline`, `image` (≥ 1200×675), `datePublished`, `dateModified`, `author` (Person), `publisher` (Organization with logo).
- `BreadcrumbList` JSON-LD (Home → Blog → Article).
- Related-content section linking to 3–5 adjacent posts (internal linking signal).
- Reading-time estimate visible on the page and in meta.
- `<time datetime="...">` on the publication and modified timestamps.
- Author byline links to a `Person`-schema author profile.
- Hero image with `<picture>` for art-direction across breakpoints.
- Table of contents for posts over 1500 words, with anchor IDs on every heading.

### Product page

- `Product` JSON-LD with `name`, `image`, `description`, `sku` or `gtin`, `brand`, `offers` (price, currency, availability, priceValidUntil).
- `AggregateRating` schema only if real reviews exist (never fabricate ratings).
- Multiple OG images (gallery views) cycled by Open Graph crawler.
- `FAQPage` JSON-LD for the product-specific FAQ section.
- Comparison table accessibility — `<th scope>` on every header, `<caption>` for table purpose.
- Stock availability synced between page state and structured data.

### Documentation page

- `TechArticle` or `HowTo` JSON-LD describing the procedure.
- `BreadcrumbList` JSON-LD following the docs hierarchy.
- Deep-link anchor IDs on every heading (`<h2 id="installation">`, `<h3 id="installation-prerequisites">`).
- "Edit this page" link to the source repository.
- Code blocks with explicit language hints for syntax highlighting (which also helps semantic parsing).
- Previous/Next navigation links to adjacent docs pages (internal linking).
- Search bar with `SearchAction` schema on the docs root.

### Pricing page

- `Organization` JSON-LD; `Offer` schema for each tier.
- `FAQPage` JSON-LD for pricing-specific questions.
- Comparison-table accessibility — `<th scope="col">` for tier headers, `<th scope="row">` for feature names.
- Currency switcher with explicit locale URL or `<select>` (never silent geo-IP switching).
- Annotated savings ("Save 20%") backed by visible math, not just claimed.

### Contact page

- `Organization` JSON-LD with `contactPoint` (telephone, email, contactType, availableLanguage, areaServed).
- `address` schema with `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `addressCountry`.
- `<address>` HTML element wrapping the visible contact block.
- Hours of operation as `openingHoursSpecification` if applicable.
- Map embed with `LocalBusiness` schema when there is a physical location.

### Search results page

- `<meta name="robots" content="noindex,follow">` — do not index the results, but follow links to canonical content.
- `SearchAction` declared on the homepage's `WebSite` schema (not on the results page itself).
- Visible result count and pagination via `<nav aria-label="Search results pagination">`.
- "No results" state with helpful navigation to popular content.

### 404 page

- `<meta name="robots" content="noindex,nofollow">` on the 404 itself.
- HTTP status code 404 (not 200 with 404 content — that is a soft-404 and a known issue).
- Helpful navigation back to indexable content (search, popular pages, category links).
- `<title>404 — Page not found | Brand</title>` so the SERP-displayed title is clear when the 404 is somehow indexed by accident.

## Output template (every landing page MUST include this head)

A reusable block the frontend-engineer pastes into every landing-page output. Placeholders shown in `{BRACES}`.

```html
<!DOCTYPE html>
<html lang="{LANG_CODE}" dir="{LTR_OR_RTL}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{TITLE_50_60_CHARS} | {ORG_NAME}</title>
  <meta name="description" content="{DESCRIPTION_150_160_CHARS}">

  <link rel="canonical" href="{CANONICAL_URL}">

  <meta name="robots" content="index,follow">

  <meta name="theme-color" content="{LIGHT_THEME_COLOR}" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="{DARK_THEME_COLOR}" media="(prefers-color-scheme: dark)">
  <meta name="color-scheme" content="light dark">

  <link rel="alternate" hreflang="en" href="{EN_URL}">
  <link rel="alternate" hreflang="ar" href="{AR_URL}">
  <link rel="alternate" hreflang="x-default" href="{DEFAULT_URL}">

  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="mask-icon" href="/safari-pinned-tab.svg" color="{BRAND_BLACK}">
  <link rel="manifest" href="/site.webmanifest">

  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="/fonts/Sans-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{LCP_IMAGE_URL}" as="image" fetchpriority="high">

  <meta property="og:title" content="{OG_TITLE}">
  <meta property="og:description" content="{OG_DESCRIPTION}">
  <meta property="og:image" content="{OG_IMAGE_URL}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{OG_IMAGE_ALT}">
  <meta property="og:url" content="{CANONICAL_URL}">
  <meta property="og:type" content="{OG_TYPE}">
  <meta property="og:site_name" content="{ORG_NAME}">
  <meta property="og:locale" content="{OG_LOCALE_PRIMARY}">
  <meta property="og:locale:alternate" content="{OG_LOCALE_ALTERNATE}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{TWITTER_TITLE}">
  <meta name="twitter:description" content="{TWITTER_DESCRIPTION}">
  <meta name="twitter:image" content="{OG_IMAGE_URL}">
  <meta name="twitter:image:alt" content="{OG_IMAGE_ALT}">
  <meta name="twitter:site" content="{BRAND_HANDLE}">
  <meta name="twitter:creator" content="{AUTHOR_HANDLE}">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "{ORG_NAME}",
    "url": "{ORG_URL}",
    "logo": "{ORG_LOGO_URL}",
    "sameAs": [{ORG_SOCIAL_URLS}]
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "{PAGE_SCHEMA_TYPE}",
    "headline": "{PAGE_HEADLINE}",
    "url": "{CANONICAL_URL}",
    "datePublished": "{ISO_DATE_PUBLISHED}",
    "dateModified": "{ISO_DATE_MODIFIED}"
  }
  </script>

  <style>{INLINE_CRITICAL_CSS_ABOVE_FOLD}</style>
  <link rel="preload" as="style" href="/css/main.css" onload="this.rel='stylesheet'">
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>
  <header>
    <nav aria-label="Primary">
      <!-- navigation -->
    </nav>
  </header>
  <main id="main" tabindex="-1">
    <h1>{PAGE_H1}</h1>
    <!-- page content -->
  </main>
  <footer>
    <!-- footer -->
  </footer>
</body>
</html>
```

## Tokens / numeric guardrails

- Title length: 50–60 characters
- Description length: 150–160 characters
- URL slug length: 50–70 characters (total URL ≤ 75 chars including domain)
- OG image dimensions: 1200×630 pixels, ≤ 8MB (≤ 1MB preferred)
- OG image safe zone: inner 1080×500 region
- OG image text minimum: 36px body / 60px headline (legibility at 600×315 preview)
- Twitter image minimum: 1200×628 pixels
- Article headline maximum: 110 characters
- LCP target: ≤ 2.5 seconds
- INP target: ≤ 200 milliseconds
- CLS target: ≤ 0.1
- Critical inline CSS budget: ≤ 14KB
- Single H1 per page
- Sitemap maximum URLs per file: ≤ 50,000
- Alt text length: 80–125 characters typical
- Alt text empty (`alt=""`): decorative images only — never content
- Logo minimum for Organization schema: ≥ 112×112 pixels
- Publisher logo minimum (Article schema): ≥ 600×60 pixels
- Article image minimum: ≥ 1200×675 pixels
- Redirect chain: at most 1 hop
- Heading hierarchy: never skip levels
- Font display: `swap` or `optional` with metric-matched fallback
- HTTP status for 404: must be 404 (not 200 with 404 content)
- Trailing slash policy: committed and enforced site-wide

## Checklist (severity-tagged)

- [ ] Single H1 present on the page (Critical)
- [ ] `<title>` set, 50–60 chars, unique per page (Critical)
- [ ] `<meta name="description">` set, 150–160 chars, unique per page (Critical)
- [ ] `<link rel="canonical">` set to absolute URL (Critical)
- [ ] `<meta charset="UTF-8">` as the first child of `<head>` (Critical)
- [ ] `<meta name="viewport">` set with `width=device-width, initial-scale=1.0` (Critical)
- [ ] `<html lang>` set to the actual page locale (Critical)
- [ ] `<html dir>` set when content is RTL (High)
- [ ] `<meta name="robots">` set to `index,follow` on production (Critical)
- [ ] `<meta name="robots" content="noindex,nofollow">` set on staging and preview environments (Critical)
- [ ] Open Graph full set present (`og:title` / `og:description` / `og:image` / `og:image:width` / `og:image:height` / `og:image:alt` / `og:url` / `og:type` / `og:site_name` / `og:locale`) (High)
- [ ] OG image generated at 1200×630 with text legible at preview size (High)
- [ ] Twitter card meta set (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt`) (High)
- [ ] JSON-LD `Organization` block present (Critical)
- [ ] JSON-LD `BreadcrumbList` present on every page beyond root (High)
- [ ] JSON-LD per-page-type schema present (`Article`, `Product`, `WebPage`, etc.) (Critical)
- [ ] All images have `width` and `height` attributes (Critical for CLS)
- [ ] All content images have descriptive alt text (Critical)
- [ ] All decorative images have `alt=""` (High)
- [ ] All below-fold images have `loading="lazy"` (High)
- [ ] LCP image preloaded with `fetchpriority="high"`, not lazy-loaded (Critical)
- [ ] All images have `decoding="async"` (Medium)
- [ ] Modern image formats served (AVIF/WebP) with JPG fallback via `<picture>` (High)
- [ ] Semantic HTML — `<main>`, `<header>`, `<nav>`, `<footer>` present and unique where appropriate (Critical)
- [ ] Heading hierarchy sequential — no skipped levels (Critical)
- [ ] `<button>` for actions, `<a>` for navigation; never `<div onclick>` (Critical)
- [ ] `robots.txt` present at root and references the sitemap (High)
- [ ] `sitemap.xml` present, current, ≤ 50,000 URLs per file (High)
- [ ] LCP ≤ 2.5s on mobile (Critical)
- [ ] INP ≤ 200ms (Critical)
- [ ] CLS ≤ 0.1 (Critical)
- [ ] No keyword stuffing in body copy (Critical)
- [ ] No "Click here" link text (Medium)
- [ ] No hidden text for keywords (color matching background, off-screen indents) (Critical)
- [ ] `theme-color` meta present for light and dark schemes (Medium)
- [ ] Favicons full set (16, 32, 180 apple-touch, mask-icon, manifest, 512 maskable) (Medium)
- [ ] `hreflang` set on every localized page including `x-default` (High when multi-locale)
- [ ] Translated `<title>`, `<meta description>`, `og:*`, alt text on localized pages (High when multi-locale)
- [ ] Trailing-slash policy committed and enforced site-wide (Medium)
- [ ] No redirect chains longer than 1 hop (Medium)
- [ ] URLs lowercase, hyphenated, ≤ 70 chars in slug (Medium)
- [ ] No URL params for content routing (Medium)
- [ ] `dateModified` updated on every meaningful article edit (Medium)
- [ ] Author byline links to `Person`-schema profile on article pages (Medium)
- [ ] Internal links to related content present on every article and product page (Medium)
- [ ] No synchronous third-party scripts above the fold (High)
- [ ] Critical CSS inlined above the fold (≤ 14KB) (High)
- [ ] Non-critical CSS deferred via preload pattern (Medium)
- [ ] Font preloaded for the primary face (Medium)
- [ ] Preconnect to font CDN declared (Medium)
- [ ] 404 page returns HTTP 404 status (not 200 with 404 content) (High)
- [ ] No `noindex` on any page that appears in the sitemap (High)
- [ ] SPA routes pre-rendered or server-rendered for crawler access (Critical)
- [ ] OG image unique per page (or at minimum per route) (Medium)
- [ ] JSON-LD validates as well-formed JSON and references resolvable URLs (Critical)
- [ ] No `Disallow: /` in production `robots.txt` (Critical)
- [ ] Staging environments gated by basic-auth or IP allowlist in addition to `noindex` (High)

## Related

- See **foundations/accessibility.md** for the overlap with SEO (semantic HTML, alt text, heading hierarchy, focus, descriptive link text — passing the accessibility foundation gets you most of the way through SEO basics).
- See **foundations/motion.md** for the `prefers-reduced-motion` and CWV intersection — motion that animates layout properties wrecks CLS; motion that runs heavy work on the main thread wrecks INP.
- See **foundations/layout.md** for image-dimension declaration to prevent CLS, and for landmark structure (`<main>`, `<header>`, `<nav>`, `<footer>`) that crawlers depend on.
- See **foundations/typography.md** for font-loading strategy (`font-display: swap` with metric-matched fallback) that prevents layout shift on font swap.
- See **foundations/copy.md** for action-led `<title>` and `<meta description>` writing patterns, and for link-text discipline ("Read the pricing details" not "Click here").
- See **foundations/color.md** for `theme-color` token choices in light and dark schemes.
- See **foundations/components.md** for the form and card markup contracts that affect crawler comprehension of product, FAQ, and pricing surfaces.
