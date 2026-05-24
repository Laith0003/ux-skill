# Frontend stacks compared

The ux plugin produces code in 6 frontend stacks — React + Tailwind, Next.js (App Router), Vue, Blade + Alpine + HTMX, Astro, vanilla HTML. Each stack has its own discipline. Here's when to pick which.

This page is the decision reference. If you are starting a project and choosing a stack, this tells you what each is for. If you are already in a stack, this tells you what the stack is best at (so you can lean into it) and what it is worst at (so you can avoid it).

The plugin auto-detects your stack from `package.json` / `composer.json` and produces code that fits. But the decision of which stack to be in is yours — and it's the most consequential decision in the project after "what are we building."

---

## React + Tailwind + Framer Motion

The default modern stack. The thing engineers reach for first.

### When to pick

- **You need rich client interactivity** — drag, sortable lists, real-time editors, complex form state, multi-step wizards with branching.
- **Your team already knows React** — and the cost of context-switching outweighs other stack advantages.
- **You're building a SPA** — single-page application where the URL is mostly cosmetic and the app is the page.
- **You need a wide component ecosystem** — Radix, React Aria, shadcn/ui, the headless component layer.
- **You're shipping behind authentication** — SEO is not a primary concern, and you can afford the JavaScript bundle weight.

### Strengths

- **Mature ecosystem.** Almost any UI pattern has a battle-tested library.
- **Component composition.** The mental model of components rendering components is clean.
- **TypeScript integration.** React + TS is the strongest type story in frontend.
- **Tailwind discipline.** Tailwind + React gives you utility-class consistency without CSS sprawl.
- **Framer Motion.** When animation matters, Framer Motion is the best in class for declarative motion.
- **Hot reload + dev experience.** Vite + React HMR is fast and reliable.

### Weaknesses

- **Bundle size.** Every page ships JavaScript. Initial paint is slow on poor networks. LCP suffers.
- **SEO complexity.** Without SSR, search engines see empty divs. Need to add a SSR layer or accept SEO loss.
- **State management chaos.** React has no canonical state pattern — Context, Redux, Zustand, Jotai, Recoil, TanStack Query. Teams burn cycles choosing.
- **Re-render footguns.** Components re-render more than necessary by default. Optimization requires memo discipline.
- **Build complexity.** Webpack/Vite + Babel/SWC + TypeScript + Tailwind + PostCSS + ESLint — many moving parts.

### Stack details

```
React 18+ (concurrent rendering, transitions, Suspense)
Tailwind CSS 4 (atomic utilities)
Framer Motion 11+ (motion)
Vite (dev server, build)
TypeScript (types)
React Router or TanStack Router (routing)
TanStack Query (server state)
Zustand or Jotai (client state, minimal)
```

### What the plugin produces

For React, the plugin produces:

- Functional components with hooks.
- Tailwind classes for styling, with `clsx` or `cn` for conditional classes.
- Framer Motion for animations beyond simple CSS transitions.
- ARIA-correct markup with Radix primitives where useful.
- Typed props with TypeScript interfaces.

The plugin avoids:

- Class components.
- CSS-in-JS solutions (Tailwind covers it).
- Inline styles (uses Tailwind utilities).
- Default exports without named ones (uses both).

---

## Next.js App Router

React with a server. The stack to pick when you need both interactivity and SEO.

### When to pick

- **You need both interactive UI and SEO.** Marketing pages that need to rank + product pages that need to be interactive, in the same app.
- **You want React Server Components.** RSC reduces client bundle size by rendering server-only components on the server.
- **You need flexible rendering modes.** Some pages SSG (build-time), some SSR (request-time), some ISR (hybrid), some client-only.
- **You want server actions.** Form submissions and mutations without a separate API layer.
- **You're on Vercel.** The hosting story is integrated; less devops overhead.

### Strengths

- **Server-rendered React.** Pages have content on first paint; SEO works.
- **App Router is the future.** Server Components, streaming, parallel routes, intercepting routes. The model is more powerful than Pages Router.
- **Built-in image optimization.** `next/image` handles responsive images automatically.
- **Built-in font optimization.** `next/font` self-hosts fonts and prevents layout shift.
- **API routes / Server Actions.** Backend logic colocated with frontend.
- **Edge functions.** Logic at the CDN edge for low latency.

### Weaknesses

- **RSC boundaries are tricky.** Knowing when a component must be a Client Component vs Server Component is non-obvious. Mistakes lead to mysterious errors.
- **Caching complexity.** Next.js caches aggressively; understanding when and why is a constant battle.
- **Vendor lock-in (soft).** App Router patterns are most ergonomic on Vercel. Other hosts work but with friction.
- **Migration cost from Pages Router.** Old codebases on Pages Router face a non-trivial migration.
- **Build times.** Large Next.js apps can take 5-10 minutes to build.

### RSC boundaries

The fundamental Next.js App Router decision: is this component a Server Component or a Client Component?

**Server Component (default):**
- Renders on the server.
- Can `await` data directly in the component body.
- Cannot use hooks, state, event handlers, or browser APIs.
- Sends no JavaScript to the client.

**Client Component (`'use client'` directive):**
- Renders on the server initially, then hydrates on the client.
- Can use all React features (state, effects, event handlers).
- Sends JavaScript to the client.
- Must avoid server-only APIs.

The heuristic: start as Server Component. Convert to Client Component only when you need state, effects, or browser APIs. Keep Client Components small and at the leaves.

### Rendering modes

- **SSG (Static Site Generation).** Page rendered at build time. Fast, cheap, cacheable. Use for content that rarely changes (marketing pages, blog posts).
- **SSR (Server-Side Rendering).** Page rendered at request time. Always fresh but slower. Use for user-specific pages (dashboards).
- **ISR (Incremental Static Regeneration).** Page rendered at build time but regenerated periodically or on-demand. Use for content that changes occasionally (product catalog).
- **Client-side rendering.** Page rendered in the browser. Use for highly interactive pages where SEO doesn't matter (after login).

The plugin defaults to SSG for landing pages, SSR for authenticated pages, and Client Components only where state is essential.

### Stack details

```
Next.js 15+ (App Router)
React 19+
Tailwind CSS 4
Framer Motion (optional)
TypeScript
Drizzle or Prisma (database)
Server Actions (mutations)
React Server Components (data)
```

---

## Vue + Tailwind + GSAP

The composition API stack. Quietly excellent.

### When to pick

- **Your team prefers Vue.** Vue's Composition API is arguably cleaner than React hooks.
- **You want SFCs (Single File Components).** Vue's `.vue` file with `<template>`, `<script setup>`, and `<style scoped>` is a clean co-location.
- **You need GSAP-quality animation.** GSAP is the strongest motion library, period. It's stack-agnostic but pairs well with Vue.
- **You want a more opinionated framework than React.** Vue has fewer choices to make; the canonical patterns are clearer.

### Strengths

- **Composition API is clean.** `<script setup>` reads like a function — no class noise, no boilerplate.
- **Reactivity is automatic.** `ref()` and `reactive()` track dependencies; updates "just work."
- **Scoped CSS by default.** `<style scoped>` removes the CSS sprawl problem.
- **Slot system.** Vue slots are more ergonomic than React render props.
- **Smaller bundle.** Vue 3 + Tailwind ships less JavaScript than React + Tailwind for equivalent features.
- **Templates feel like HTML.** New team members ramp faster.

### Weaknesses

- **Smaller ecosystem.** Many high-quality libraries are React-first; Vue gets ports.
- **TypeScript integration is good, not perfect.** `<script setup lang="ts">` works well, but some patterns (especially with slots) require manual type assertions.
- **Two-way binding tradeoffs.** `v-model` is convenient but can hide data flow.
- **Hiring market.** Smaller pool of Vue developers in most regions vs React.

### GSAP isolation

The pattern for GSAP in Vue: keep GSAP usage in `onMounted`/`onUnmounted` lifecycle hooks. Never set up GSAP at component creation. Always clean up animations on unmount.

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const target = ref(null)
let ctx

onMounted(() => {
  ctx = gsap.context(() => {
    gsap.from(target.value, {
      opacity: 0,
      y: 40,
      scrollTrigger: {
        trigger: target.value,
        start: 'top 80%',
      },
    })
  })
})

onUnmounted(() => {
  ctx?.revert()
})
</script>
```

`gsap.context()` is the cleanup mechanism. Revert on unmount.

### Stack details

```
Vue 3.4+
Vite
Tailwind CSS 4
GSAP 3+ with ScrollTrigger
TypeScript (optional but recommended)
Vue Router 4
Pinia (state)
```

---

## Blade + Alpine.js + HTMX + Tailwind

The Laravel server-side stack. Underrated for what it does.

### When to pick

- **You're already in Laravel.** Adding a frontend framework on top of Laravel multiplies complexity for little gain.
- **You need server-rendered HTML with light interactivity.** Forms, modals, tabs, real-time updates — without writing JavaScript-heavy components.
- **SEO is critical.** Server-rendered HTML by default, no hydration concerns.
- **You're shipping multi-language with RTL.** Blade + Laravel's localization handles this cleanly.
- **You want type safety from the database to the view.** Laravel's Eloquent + Blade is one cohesive type story.

### Strengths

- **Server-rendered by default.** First paint is fast. SEO works. No hydration mismatch.
- **HTMX for partial updates.** Want to swap a div on a button click without writing a SPA? `hx-get="/partials/foo" hx-target="#bar"` and done.
- **Alpine.js for client interactivity.** Want a dropdown that opens and closes? `x-data="{ open: false }" x-show="open"` and done.
- **Blade components are clean.** `<x-card>...</x-card>` with slots and props feels like JSX but renders server-side.
- **No build chain (mostly).** Tailwind needs a build, but you don't need webpack/Vite for app logic.
- **RTL-friendly.** Laravel's localization is mature; Blade with logical CSS properties handles RTL well.
- **Forms are easy.** `@csrf`, `@method`, validation, error display — all baked in.

### Weaknesses

- **No client-side routing.** Every navigation is a full request (HTMX mitigates this).
- **No SPA-style state across pages.** Each page is its own request.
- **Alpine.js for complex state is awkward.** Beyond simple `x-data`, you'll wish you had React/Vue.
- **Smaller community vs React/Next.** Fewer pre-built components.
- **HTMX is not React.** Real-time editors, complex forms, drag-and-drop — these need real JavaScript.

### When to use which

- **Blade for everything that's HTML structure.** Pages, layouts, components.
- **Alpine for local state.** Dropdowns, tabs, modals, simple form interactions.
- **HTMX for server interactions.** Submit a form and replace a div with the response. Refresh a list every 30 seconds.
- **Tailwind for all styling.** Same as other stacks.
- **Vanilla JS for things Alpine/HTMX can't do.** Charts, maps, complex visualizations.

### The Dot example

The Dot platform (thedotwallet.com) runs on this stack. The reasoning:

- Customer flows are mostly forms and confirmations — HTMX + Blade is the right tool.
- Partner dashboards are mostly data views — Alpine for local state, HTMX for refresh.
- Multi-language (English + Arabic + 9 others) — Laravel's localization is the cleanest path.
- Server-rendered means the wallet page works on flaky 3G connections common in MENA.

### Stack details

```
Laravel 11+
Blade templates
Alpine.js 3+ (client interactivity)
HTMX (server interactions)
Tailwind CSS 4 (utility classes)
Vite (Tailwind build only)
```

### What the plugin produces

For Blade + Alpine + HTMX, the plugin produces:

- `<x-component>` Blade components with named slots and typed `@props`.
- `x-data`, `x-show`, `x-on:click` Alpine directives.
- `hx-get`, `hx-post`, `hx-target`, `hx-swap` HTMX attributes.
- Tailwind classes with `me-*`/`ms-*`/`pe-*`/`ps-*` logical utilities for RTL safety.
- `@csrf` and `@method` for forms.
- `@error('field')` for validation display.

The plugin avoids:

- Inline `<script>` blocks (uses Alpine).
- jQuery (Alpine and HTMX are the modern equivalents).
- Frontend frameworks (Vue, React) on top of Blade — Laravel already serves HTML.

---

## Astro + Tailwind

The content stack. Islands of interactivity.

### When to pick

- **You're building a content-heavy site.** Marketing site, documentation, blog, portfolio.
- **You need zero JavaScript by default.** Astro ships HTML; JavaScript only loads where you opt in.
- **You want to mix frameworks.** Astro can host React components, Vue components, Svelte components, and vanilla HTML on the same page.
- **You want the fastest possible LCP.** Astro pages are static HTML; LCP is near-instant.
- **You're publishing markdown content.** Astro's content collections handle markdown + frontmatter cleanly.

### Strengths

- **Zero JavaScript by default.** Pages ship as static HTML. Hydration only happens for explicitly-marked islands.
- **Island architecture.** Sprinkle React/Vue/Svelte components only where you need interactivity.
- **Markdown-first.** Built for content sites. MDX support, frontmatter, type-safe content collections.
- **Fast builds.** Vite-based, hot reload is snappy.
- **Excellent image optimization.** Astro's Image component handles responsive, WebP/AVIF, lazy loading.
- **MDX integration.** Markdown with embedded components.

### Weaknesses

- **Not for apps.** Astro is for content sites with light interactivity. Don't build a SaaS dashboard on it.
- **No client routing.** Every navigation is a full request (View Transitions API mitigates this somewhat).
- **Less ecosystem.** Smaller than Next.js or React.
- **Server endpoints are less mature.** Astro can do API routes but Next.js does it better.

### Island architecture

The Astro mental model:

```astro
---
import StaticHeader from '../components/StaticHeader.astro';
import InteractiveSearch from '../components/InteractiveSearch.jsx';
---

<StaticHeader />
<InteractiveSearch client:visible />
<article>
  <h1>This is just HTML.</h1>
  <p>No JavaScript on the page until you scroll to the search.</p>
</article>
```

The `client:visible` directive hydrates the search component only when it scrolls into view. The article is pure HTML.

Directives:

- `client:load` — hydrate immediately on page load.
- `client:idle` — hydrate when the browser is idle.
- `client:visible` — hydrate when the component scrolls into view.
- `client:media={query}` — hydrate when a media query matches.
- `client:only={framework}` — render only on the client (no SSR).

### Stack details

```
Astro 4+
Tailwind CSS 4
Optional: React/Vue/Svelte components for islands
TypeScript
Markdown/MDX content collections
```

---

## Vanilla HTML + CSS + minimal JS

The simplest stack. Always available.

### When to pick

- **You're prototyping.** A single-page exploration of a design idea.
- **You're building a portfolio piece.** Stand-alone HTML files that can be hosted anywhere.
- **You're designing in code.** The design itself is the artifact; the stack is incidental.
- **You're writing a tutorial.** Readers should be able to copy the file and open it in a browser.
- **You're shipping something tiny.** One-page sites where any framework overhead is silly.

### Strengths

- **Zero build chain.** Save the file, refresh the browser.
- **Maximum compatibility.** Works in every browser, including offline.
- **Easy to host.** Any static host, S3, GitHub Pages, even an email attachment.
- **Easy to read.** A single HTML file with embedded CSS and JS is the most readable thing in frontend.
- **Performance ceiling.** No framework overhead means LCP is bound only by your asset sizes.

### Weaknesses

- **Doesn't scale.** Beyond a single page, you'll want includes, components, partials. Hand-rolling these in vanilla gets ugly fast.
- **Limited interactivity.** Complex state, real-time updates, multi-step flows — these need a framework.
- **No type safety.** TypeScript can help but the integration is manual.
- **No component reuse across files.** Or rather, the reuse mechanism is "copy-paste."

### What "minimal JS" means

The plugin's vanilla HTML output uses JavaScript only for:

- Smooth scroll behavior (already CSS-able but JS gives more control).
- Intersection observers for scroll-triggered animations.
- Form validation enhancements (HTML5 validation does most of it).
- Theme toggle (light/dark mode).

Never:

- Routing (single page only).
- State management (use the URL or localStorage if needed).
- Templating (use HTML as written).

### Stack details

```
HTML5
CSS (Tailwind via CDN or hand-rolled)
JavaScript (vanilla, often inline)
No build chain
No bundler
No package manager (necessarily)
```

### What the plugin produces

For vanilla HTML, the plugin produces:

- A single `.html` file with `<style>` block.
- Tailwind via Play CDN (or hand-rolled CSS if Tailwind is too heavy).
- Inline `<script>` blocks for any required JavaScript.
- Self-contained, no external dependencies (except CDN scripts).

---

## Decision tree: what stack for what brief

Use this decision tree. Answer top to bottom:

```
Is the project content-heavy (marketing, blog, docs, portfolio)?
├─ Yes → Astro (or vanilla HTML if it's truly tiny).
└─ No → Continue.

Are you already in Laravel?
├─ Yes → Blade + Alpine + HTMX.
└─ No → Continue.

Do you need SEO AND rich interactivity?
├─ Yes → Next.js (App Router).
└─ No → Continue.

Do you need rich client interactivity (drag, real-time, complex forms)?
├─ Yes → React + Tailwind (or Vue + Tailwind if team prefers Vue).
└─ No → Continue.

Is it a single-page prototype or design exploration?
├─ Yes → Vanilla HTML.
└─ No → Reconsider — most cases fit above.
```

### Brief-to-stack examples

- **Loyalty platform with partner dashboards (server-rendered, multi-language, RTL)** → Blade + Alpine + HTMX.
- **Marketing site with one interactive demo widget** → Astro with one React island.
- **Documentation site for a developer tool** → Astro.
- **E-commerce storefront with cart and checkout** → Next.js.
- **Internal admin dashboard for a SaaS company** → React + Tailwind (SPA, no SEO concerns).
- **Single-page portfolio with one animated hero** → Vanilla HTML or Astro.
- **Designer's case study microsite** → Astro (or vanilla HTML for one-pagers).
- **Real-time chat application** → React + Tailwind (or Next.js if SEO + chat).
- **CMS-driven content site with editor previews** → Next.js with the CMS's preview mode.
- **Blog with very high traffic and low budget** → Astro (cheapest to host, fastest to serve).

---

## Performance comparison (LCP, INP, CLS)

Approximate metrics for equivalent work. Lower is better for LCP and CLS; higher is worse for INP.

| Stack | LCP (typical) | INP (typical) | CLS (typical) | JS shipped (KB, gzipped) |
|---|---|---|---|---|
| Vanilla HTML | 0.4-0.8s | <50ms | <0.05 | 0-20 |
| Astro (no islands) | 0.5-1.0s | <50ms | <0.05 | 0-30 |
| Astro (with islands) | 0.5-1.2s | 50-100ms | <0.05 | 30-80 |
| Blade + Alpine + HTMX | 0.6-1.2s | 50-150ms | 0.05-0.1 | 20-50 |
| Next.js App Router (SSG) | 0.8-1.5s | 100-200ms | 0.05-0.1 | 100-200 |
| Vue + Vite (SPA) | 1.2-2.5s | 100-200ms | 0.1-0.2 | 80-150 |
| React + Vite (SPA) | 1.5-3.0s | 150-300ms | 0.1-0.2 | 120-250 |

These are rough ranges. Specific implementations can do better or worse.

The trend:

- **Server-rendered HTML wins LCP.** Vanilla HTML, Astro, Blade.
- **Less JS wins INP.** Vanilla, Astro, HTMX.
- **CLS is mostly about layout discipline.** Any stack can have great or terrible CLS depending on how images and fonts are handled.

### Why this matters

Core Web Vitals affect SEO directly. Google ranks faster pages higher. For content sites, this is the entire game.

For apps behind authentication, the difference is less critical — users are already committed. But INP still affects perceived responsiveness.

---

## Developer experience comparison

What it feels like to work in each stack day-to-day.

### Hot reload speed (typical, on a 50-component app)

| Stack | Hot reload speed |
|---|---|
| Vanilla HTML | Instant (refresh manually or with `live-server`) |
| Astro | Fast (~100ms) |
| Blade + Vite (Tailwind only) | Fast (~150ms) |
| Vue + Vite | Fast (~150ms) |
| React + Vite | Fast (~200ms) |
| Next.js App Router | Medium (~500ms-1s for RSC changes) |

### Type safety

- **Vanilla HTML**: none (unless you add JSDoc).
- **Astro**: TypeScript built-in. Type-safe content collections.
- **Blade**: PHP types in props (Laravel 10+), some Blade type integration via tools like Larastan.
- **Vue + TS**: good but not as smooth as React + TS.
- **React + TS**: excellent. The TypeScript story is mature.
- **Next.js + TS**: excellent. Same as React.

### Debugging

- **Server-rendered (Blade, Astro static, Next.js SSG)**: View source shows actual HTML. Easy.
- **Client-rendered (React SPA, Vue SPA)**: View source shows empty div. React DevTools / Vue DevTools are essential.
- **Hybrid (Next.js, Astro islands)**: Some pages easy, some hard. Need to know which is which.

### Build times (cold, on a medium-sized project)

| Stack | Build time |
|---|---|
| Vanilla HTML | N/A (no build) |
| Astro | 5-20s |
| Blade (Tailwind only) | 5-15s |
| Vue + Vite | 10-30s |
| React + Vite | 10-30s |
| Next.js App Router | 30s-5min |

Long Next.js build times are a real cost in CI/CD pipelines.

---

## Stack auto-detection

The plugin detects your stack from project files:

| Detector | Resulting stack |
|---|---|
| `package.json` has `next` dependency | Next.js App Router |
| `package.json` has `react` but not `next` | React + Tailwind |
| `package.json` has `vue` | Vue + Tailwind |
| `package.json` has `astro` | Astro |
| `composer.json` has `laravel/framework` | Blade + Alpine + HTMX |
| No package manager files | Vanilla HTML |

When multiple detectors match (e.g., React inside an Astro project), the plugin asks which to use.

You can override via the `/ux-stack` command:

```
/ux-stack vue
```

This locks the stack for the session.

---

## Mixing stacks

Sometimes the right answer is mixing stacks.

### Astro + React islands

Astro is built for this. Static pages plus React islands for interactivity. Use when:

- Most of the site is content.
- A few interactive widgets need framework support.
- LCP matters more than uniform stack.

### Next.js + Server Components + Client Components

The Next.js App Router model. Use Server Components for static structure, Client Components for interactive leaves. This is "one stack" but uses two rendering modes.

### Laravel + Inertia.js

Inertia bridges Laravel to React/Vue without an API layer. Use when:

- You want a SPA-like experience with Laravel routing.
- You don't want to write a REST/GraphQL API.
- You're willing to take on more JS than HTMX would give.

Inertia is a legitimate stack but adds a layer of complexity. The plugin can produce code for it, but defaults to Blade + Alpine + HTMX for Laravel.

### Static + dynamic micro-frontends

Marketing site on Astro (static, SEO). App on Next.js or a separate domain (interactive, behind auth). The user crosses between them via links.

This is common for SaaS products: `www.example.com` is Astro, `app.example.com` is Next.js or a React SPA.

---

## Stack migration paths

Sometimes the right move is changing stacks. Common paths:

### Vanilla HTML → Astro

Easy. Astro is essentially "vanilla HTML with components." Wrap your existing HTML in `.astro` files, extract repeated chunks into components, add a layout file.

### React SPA → Next.js

Medium difficulty. Route by route, move from React Router to Next.js routing. Decide which pages are Server Components vs Client Components.

### Next.js Pages Router → App Router

Non-trivial. The data fetching model is different (`getServerSideProps` becomes `await fetch()` in a Server Component). Route by route, not all at once.

### Vue → React (or vice versa)

Major. Don't unless team or hiring constraints demand it. The cost is months, not weeks.

### Server-rendered (Blade, Astro, Next.js SSR) → Client SPA

Almost always a step backward. Server-rendering wins on most metrics. Don't migrate this direction unless you have a specific reason.

### Client SPA → Server-rendered

Often the right move when SEO becomes important or when bundle size hurts performance. Hard but valuable.

---

## Anti-patterns in stack choice

### "React for everything"

Default-React thinking treats the entire frontend as a React problem. A marketing site doesn't need React. A documentation site doesn't need React. A single-page portfolio doesn't need React. Use the stack that fits the brief.

### "Microservice-style frontend"

Each page is its own micro-frontend in its own stack. Sounds modern; in practice it's a maintenance nightmare. Pick one stack for the bulk of work; mix only where it earns its weight.

### "Old stack therefore bad"

Blade + Alpine + HTMX is not "old" — it's a different solution. PHP/Laravel is shipping more sites in 2026 than ever. Don't dismiss a stack because the tooling is mature.

### "New stack therefore good"

Every year there's a "new stack." Most don't survive. Pick stacks with ecosystem depth, not novelty.

### Choosing a stack before defining the brief

Stack choice is downstream of "what are we building." A team that chooses React first and then builds whatever React makes easy is shipping the framework's defaults, not the user's needs.

---

## When the plugin's stack choice is wrong

The plugin defaults to whatever it detects. Override when:

- The detected stack is the team's old stack but a new project should be different.
- The project is in a transition between stacks.
- The plugin chose React but the project's needs (SEO, performance) would be better served by Next.js or Astro.

Override via:

```
/ux-stack [next|react|vue|blade|astro|html]
```

The override is per-session. To make it permanent, document it in the project's CLAUDE.md or equivalent.

---

## Related pages

- [The 6 Audit Lenses](The-6-Audit-Lenses) — auditing code in any of these stacks.
- [Polaris-style audit reports](Polaris-style-audit-reports) — for documenting findings.
- [Wfrah-style case study format](Wfrah-style-case-study-format) — for writing up stack decisions in a case study.
- [Real-life UX consulting](Real-life-UX-consulting) — when the stack decision needs a human review.

---

## Footer

Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
Author: Laith Aljunaidy — [LinkedIn](https://www.linkedin.com/in/laithaljunaidy/) — +962 79 786 8335
