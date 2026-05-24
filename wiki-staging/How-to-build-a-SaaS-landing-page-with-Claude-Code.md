# How to Build a SaaS Landing Page with Claude Code

Build a premium SaaS landing page in Claude Code that doesn't look generated. The discovery protocol asks 10 questions; the plugin produces production-ready code with anti-AI-slop discipline and full SEO surface.

## What this page covers

You will install the plugin, run the discovery protocol, generate a premium landing page, iterate on the output, and ship it with accessibility and SEO surfaces already in place. The whole loop runs in Claude Code without leaving the terminal.

## Why most AI-generated landings fail

Three patterns kill the credibility of AI-generated landing pages before a real user ever sees them.

### The three-equal-cards pattern

The features section converges to the same shape every time: three cards of identical width, identical height, identical structure — icon, title, paragraph. Always three. Never two. Never four. Once you see the pattern, every landing built this way looks like the same landing.

A real product has features of different importance. The hero feature deserves more space. The supporting features deserve less. A premium landing reflects that hierarchy.

### The Inter problem

Inter is a good font. Inter is also the default font. When 70 percent of generated landings use Inter as the only typeface, no landing using Inter is memorable. Memorability comes from typographic pairing — a display face that carries the headline, a body face that carries the paragraph, a monospace that carries numbers and code.

### The centered hero

The default AI hero is middle-aligned. Headline centered. Subheadline centered. Two CTAs side by side, centered. Image below, centered. Nothing breaks the vertical line down the middle of the page.

A premium hero uses the full width. It has tension. The product is on one side and the proposition is on the other. The eye moves diagonally, not vertically.

## The plugin's approach

The plugin replaces the default "generate and ship" loop with a four-stage discipline.

1. **Discovery** — 10 questions before any code is written. The questions force specificity about user, voice, brand, stack, and constraints.
2. **Anti-slop generation** — the design-system-architect sub-agent generates code that is checked against a slop catalogue at write time. Inter-only, gradient heroes, John Doe placeholders, and three-equal-card grids are blocked.
3. **SEO foundation baked in** — every page generated includes a Title under 60 characters, a meta description in the 150-160 character snippet range, Open Graph tags, Twitter cards, and JSON-LD structured data scoped to the page type.
4. **Iteration in place** — `/ux-polish` and `/ux-a11y` run on the same files, with `--fix` flags that apply changes directly.

## Step 1: install the plugin

Clone the plugin into your Claude Code plugins directory.

```bash
git clone https://github.com/Laith0003/ux-skill.git ~/.claude/plugins/ux-skill
```

Restart Claude Code in your project directory. Verify the commands are available:

```
/ux-design
/ux-system
/ux-polish
/ux-a11y
/ux-copy
```

Five primary commands. Twelve more for specific surfaces (dashboard, pricing table, navbar, footer, modal, form, etc.). All listed under `/help` once the plugin is loaded.

## Step 2: run /ux-design with your brief

The brief is one or two sentences. Specific is better than long.

```bash
/ux-design landing page for a B2B treasury management SaaS targeting CFOs at mid-market firms who run weekly close
```

The plugin does not immediately generate. It runs discovery.

## Step 3: answer the 10 discovery questions

Here is the full set, with example answers from a real treasury-management product.

### 1. Who is the user?

Not "users." A specific persona, with role, company size, and the moment they show up.

> Example: CFO or VP Finance at a mid-market firm (200-2000 employees), running treasury close every Friday afternoon. Probably has 4-6 bank accounts to reconcile, intercompany loans, FX exposure across 2-3 currencies. Currently doing this in Excel.

### 2. What is the one job they came here to do?

Pick the single highest-priority action. Not three. One.

> Example: Decide whether to book a 15-minute demo. The page exists to move them from skeptic to demo-booker.

### 3. What is the brand voice?

Provide three sample lines you would write in the brand voice for unrelated topics. The model uses these to anchor.

> Example:
> "Close your week before Friday at 5."
> "Reconciliation is not a science project."
> "We do not sell dashboards. We sell time."

### 4. What is the visual register?

Pick one. Editorial. Brutalist. Apple-clean. Industrial. Maximalist. Minimalist. Each has implications for type, color, density, and motion.

> Example: Apple-clean monochrome. High contrast. One saturated accent (deep teal). Generous white space. Sans-serif body, but with a serif display face for headlines.

### 5. What stack are you on?

Framework. CSS approach. Component library if any.

> Example: Next.js 14, Tailwind 4, no component library. Self-hosted fonts.

### 6. What are the must-haves vs nice-to-haves?

Must-haves are blockers. Nice-to-haves are flexible.

> Example:
> Must: hero with primary CTA, feature triplet, demo-booking widget, real customer logos.
> Nice: a comparison table against incumbent (Excel + bank portal), a security/compliance section, a pricing summary.

### 7. What is the constraint you cannot break?

The non-negotiable. Often accessibility, performance, brand, or a regulatory rule.

> Example: WCAG 2.1 AA minimum. Largest Contentful Paint under 2 seconds on a mid-range Android device. No external trackers other than Plausible.

### 8. What competitors do you respect, and why?

Two or three. The reasons matter more than the names.

> Example: Trovata for the editorial restraint of their pricing page. Modern Treasury for the clarity of their hero proposition. Ramp for the density of useful information without feeling crowded.

### 9. What anti-patterns do you want to avoid?

Things you have seen and hated.

> Example: Purple-to-pink gradients. Lottie animations on the hero. Generic "Trusted by" gray logo strip. Three equal feature cards. "Get Started" as the CTA verb.

### 10. What is the call to action and what happens when they click it?

The exit. What you actually want them to do.

> Example: CTA text "Book a 15-minute demo." Click opens a Cal.com inline scheduler with three available slots in the next 48 hours. Secondary CTA is "See it on your own data" — a self-serve sandbox.

## Step 4: review the output and iterate

After discovery, the plugin generates the full page. Output includes:

- A single Blade, Astro, JSX, or Vue file (matching your stack)
- Component breakdown for sections you can reuse
- A `tokens.css` or Tailwind config patch with the brand palette
- A `meta.json` block with Title, description, OG, Twitter card, JSON-LD
- A README block at the top explaining the design decisions

You read it. You iterate. Iteration prompts that work well:

```
/ux-design tighten the hero — drop the secondary CTA, make the proposition feel more urgent
```

```
/ux-design swap the third feature card for a comparison table against Excel
```

```
/ux-design the testimonials section is too long — keep one quote and the three logos
```

Each iteration runs against the existing file. The plugin does not regenerate from scratch unless you explicitly ask. State is preserved.

## Step 5: apply fixes with /ux-polish --fix and /ux-a11y --fix

Once the structure is right, run the polish pass.

```bash
/ux-polish ./resources/views/landing.blade.php --fix
```

The polish pass catches anything the generation missed — generic copy, default colors, three-equal-card patterns, placeholder text, emoji icons.

Then the accessibility pass.

```bash
/ux-a11y ./resources/views/landing.blade.php --fix
```

The a11y pass verifies contrast, focus indicators, keyboard navigation, semantic HTML, ARIA labels, alt text, motion preferences, dynamic type support, and form-error patterns. The `--fix` flag applies mechanical fixes (alt text on images, `aria-label` on icon buttons, `focus-visible` rings on interactive elements, `prefers-reduced-motion` guards on animations).

## Anatomy of a premium SaaS landing

The plugin generates sections in AIDA order — Attention, Interest, Desire, Action. The structure is consistent because the structure works.

### Section 1: Hero (Attention)

- Asymmetric. Headline on one side. Product visual or proof on the other.
- Headline is one specific outcome. Not "transform your business." A concrete sentence with a verb and an object and ideally a number.
- Subheadline is one sentence. Names the user and the situation.
- Primary CTA is verb plus outcome ("Book a 15-minute demo," not "Get Started").
- One secondary CTA, lower hierarchy.
- Above the fold on a 1440px desktop and a 390px iPhone. The fold is real on first impression.

### Section 2: Proof strip (Interest)

- Real customer logos in color, with permission. Or none.
- A single pull quote from a real customer with name, title, and company.
- If you have a metric ("47 hours saved per close, on average"), it goes here.

### Section 3: Feature anatomy (Interest)

- Asymmetric. One hero feature gets the largest card or section. Two or three supporting features get smaller treatments.
- Each feature pairs a specific outcome ("Close in 14 minutes") with a specific capability ("Variance summary across 6 banks").
- Visuals are real screenshots or accurate illustrations. Not stock product mockups.

### Section 4: Workflow or demo (Desire)

- Show the actual product flow. Three to five steps. Each step is a screenshot or a short loop.
- The workflow section is the most-clicked, most-scrolled section on a B2B landing. It is where decisions are made.

### Section 5: Objection handling (Desire)

- Security and compliance section if relevant (SOC 2, GDPR, ISO 27001).
- Integrations section if relevant.
- Comparison against incumbent (Excel, the legacy tool) if relevant.

### Section 6: Pricing summary or CTA (Action)

- Either a pricing summary (three tiers, with the middle tier featured) or a single CTA section.
- If pricing is here, the recommended tier has stronger visual weight. Not the same width as the others.
- If a CTA section, it restates the hero CTA with a slightly different framing — "Still skeptical? Try it on your own data."

### Section 7: Footer (Action)

- Lightweight footer. Links to docs, pricing, security, status, careers.
- No newsletter signup unless you have a real newsletter to send.
- Social links only to active accounts. A dead Twitter link kills credibility.

## Stack recommendations

The plugin works with any stack. Some pair better with the discovery protocol's output style.

### For new projects

- **Astro** with Tailwind 4. Best raw HTML output, smallest payload, easiest SEO.
- **Next.js 14** with Tailwind 4 and server components. Best if you need authentication or dynamic data on the landing.
- **Remix** with Tailwind 4. Best if you are already on Remix elsewhere.

### For existing projects

- **Laravel + Blade + Alpine.js + Tailwind**. The plugin generates Blade components that drop into `resources/views/`.
- **Rails + ViewComponent + Tailwind**. Same pattern, different syntax.
- **Django + Tailwind**. Same pattern, different syntax.

### Avoid

- Stacks that pull in 200+ KB of JavaScript for a landing page. The landing should be HTML-first, CSS-second, JS-only-where-needed.
- Component libraries with heavy opinions (Material UI, Ant Design). They fight the discovery protocol's brand-specific output.

## SEO checklist

Every page generated includes the following. You verify them, then ship.

### Title tag

- Under 60 characters
- Includes the primary keyword
- Includes the brand name at the end
- Reads like a real sentence, not a keyword stuffing

Example: `Close your weekly treasury report in 14 minutes — Trovata`

### Meta description

- 150 to 160 characters
- Action-led, not feature-led
- Includes one target keyword naturally
- Reads as a Google snippet would read

Example: `Reconciliation across 6 bank accounts, FX positions, and intercompany loans — done before your 9 AM standup. Book a 15-minute demo to see it on your data.`

### Open Graph tags

- `og:title` matches Title
- `og:description` matches meta description
- `og:image` is a 1200x630 image specifically designed for share previews, not just the hero screenshot scaled down
- `og:type` is "website"
- `og:url` is the canonical URL

### Twitter card

- `twitter:card` is "summary_large_image"
- `twitter:title`, `twitter:description`, `twitter:image` match OG
- `twitter:site` is your handle, if you have an active one

### JSON-LD structured data

- `@type` is "SoftwareApplication" or "Product" for a SaaS landing
- Includes `name`, `applicationCategory`, `operatingSystem`, `offers` with price
- Real ratings only — never fake `aggregateRating`. Google penalizes fake structured data.

### Canonical URL

- Self-canonical for the landing page
- HTTPS only, no trailing slash inconsistency

### Performance signals

- Inline critical CSS for the hero
- Lazy-load images below the fold
- Preconnect to font origin
- Self-host fonts where possible

The plugin generates all of this. You verify it. You ship it.

## Real example walkthrough

Same brief as Step 2: B2B treasury management SaaS targeting CFOs at mid-market firms.

After discovery and `/ux-polish --fix` and `/ux-a11y --fix`, the output is a Next.js page with:

### File structure

```
app/
  page.tsx              # the landing page itself
  layout.tsx            # root layout with fonts, metadata
  components/
    landing/
      Hero.tsx
      ProofStrip.tsx
      FeatureGrid.tsx
      WorkflowSection.tsx
      ObjectionSection.tsx
      PricingSummary.tsx
      Footer.tsx
  tokens/
    colors.css
    typography.css
    spacing.css
public/
  fonts/
    Fraunces-Variable.woff2
    Inter-Variable.woff2
    JetBrainsMono-Variable.woff2
  og-image.png         # 1200x630, designed for share previews
```

### Hero output (pseudo-code preview)

```tsx
// app/components/landing/Hero.tsx
export function Hero() {
  return (
    <section className="grid grid-cols-12 gap-8 py-24">
      <div className="col-span-7">
        <h1 className="font-display text-6xl leading-[1.05] tracking-tight">
          Close your weekly treasury report
          <br />
          in 14 minutes, not 4 hours.
        </h1>
        <p className="mt-6 text-xl text-neutral-700 max-w-xl">
          Reconciliation across 6 bank accounts, FX positions, and
          intercompany loans — done before your 9 AM standup.
        </p>
        <div className="mt-10 flex items-center gap-4">
          <a
            href="/demo"
            className="rounded-full bg-teal-700 px-6 py-3 text-white font-medium"
          >
            Book a 15-minute demo
          </a>
          <a
            href="/sandbox"
            className="text-neutral-900 underline underline-offset-4"
          >
            See it on your own data
          </a>
        </div>
      </div>
      <div className="col-span-5">
        <ProductScreenshot
          src="/landing/variance-summary.png"
          alt="Treasury variance summary showing 6 bank accounts reconciled, FX positions, and one intercompany loan flag"
          width={720}
          height={540}
        />
      </div>
    </section>
  );
}
```

Note what is and is not present.

Present:
- Asymmetric grid (7 columns headline, 5 columns product)
- Display font on the headline, body font on the paragraph
- Specific CTA verb plus outcome ("Book a 15-minute demo")
- Real screenshot with descriptive alt text
- Token-based colors (`bg-teal-700`) not raw hex

Not present:
- No purple-pink gradient
- No "Get Started" CTA
- No Inter as only font
- No centered composition
- No emoji icons
- No placeholder copy

### Metadata output

```tsx
// app/layout.tsx
export const metadata = {
  title: "Close your weekly treasury report in 14 minutes — Trovata",
  description:
    "Reconciliation across 6 bank accounts, FX positions, and intercompany loans — done before your 9 AM standup. Book a 15-minute demo to see it on your data.",
  openGraph: {
    title: "Close your weekly treasury report in 14 minutes",
    description:
      "Reconciliation across 6 bank accounts, FX positions, and intercompany loans — done before your 9 AM standup.",
    url: "https://trovata.io",
    siteName: "Trovata",
    images: [{ url: "/og-image.png", width: 1200, height: 630 }],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Close your weekly treasury report in 14 minutes",
    description:
      "Reconciliation across 6 bank accounts, FX positions, and intercompany loans.",
    images: ["/og-image.png"],
  },
};
```

### JSON-LD

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Trovata Treasury",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "499",
    "priceCurrency": "USD"
  }
}
</script>
```

No fake `aggregateRating`. No invented review count. If the product has real reviews on G2 or Capterra, they get pulled in; if not, the field is absent.

## What to do next

The landing is shipped. The next layer is the rest of the surface area.

- The pricing page. Same discovery protocol, different structure. Run `/ux-design pricing page` with the brief.
- The dashboard. Internal product surface, not marketing. Run `/ux-design dashboard for the variance summary view`.
- The empty state, the error state, the success state. Run `/ux-design empty state for new users with no bank accounts connected yet`.

Every surface gets the same treatment. Every surface is specific. None of them look generated.

## Linked next steps

- If your fonts and colors are still defaults, generate a real design system first. See [How to generate a design system with Claude Code](How-to-generate-a-design-system-with-Claude-Code).
- If you are still seeing AI fingerprints after the polish pass, see [How to fix AI-generated UI](How-to-fix-AI-generated-UI).
- The copy on the landing is half the work. See [How to fix microcopy that sounds like AI](How-to-fix-microcopy-that-sounds-like-AI).
- Accessibility is the other half of the polish. See [How to audit accessibility with Claude Code](How-to-audit-accessibility-with-Claude-Code).

---

**See also**: [How to fix AI-generated UI](How-to-fix-AI-generated-UI) | [How to generate a design system with Claude Code](How-to-generate-a-design-system-with-Claude-Code) | [How to fix microcopy that sounds like AI](How-to-fix-microcopy-that-sounds-like-AI)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
