# Design System Inspired by Hugging Face

## 1. Visual Theme & Atmosphere

Hugging Face's web presence is the open-source AI community's home — the hugging face emoji as the brand mark, a clean white canvas, model card listings as the dominant content unit, and a developer-documentation aesthetic. The atmosphere is open-community AI. Where commercial AI peers (OpenAI, Anthropic, Cohere) lean into branded marketing surfaces, Hugging Face leans into the model hub itself — the home page is a search bar followed by a listing of trending models, datasets, and spaces. The site reads as "GitHub for ML" rather than enterprise SaaS.

The hugging face emoji is the brand mark — the yellow open-armed hugging-face glyph (or its inline-rendered equivalent) used as the wordmark prefix and as a decorative anchor. The emoji-as-logo choice is deliberate: the brand is community-first, welcoming, and playfully un-corporate. Replacing the mark with a stylized abstract icon would flatten the brand voice.

The yellow voltage (#ff9d00) appears scarcely on individual elements but generously on the brand presence — a yellow pill CTA, the wordmark accent, the "like" heart on model cards. The chrome is otherwise nearly monochrome — clean white canvas, near-black ink, gray hairlines.

**Key Characteristics:**
- Hugging face emoji as brand mark — welcoming, community-first
- Hugging Face yellow (#ff9d00) — scarce CTA voltage
- White canvas with developer-documentation aesthetic
- Model card listings — author + model name + downloads + likes + task tags
- Code snippets with copy-button, tabbed by framework (PyTorch, TensorFlow, JAX)
- Sign in with GitHub as primary auth — open-source signal
- Source Sans 3 typography across chrome — open-source font

## 2. Color Palette & Roles

### Primary
- **HF Yellow** (`#ff9d00`): The brand voltage — CTAs, wordmark accent, like-button fill
- **Yellow Hover** (`#cc7d00`): Press state
- **Pure White** (`#ffffff`): The canvas

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#fafafa`): Alternating section bands
- **Surface Card** (`#f7f7f7`): Hover state on cards
- **Hairline** (`#e5e7eb`): 1px borders

### Neutrals & Text
- **Ink** (`#0f0f0f`): Primary text
- **Body** (`#374151`): Default body text
- **Muted** (`#6b7280`): Captions, metadata
- **Muted Soft** (`#9ca3af`): Fine-print

### Task Tag Colors (model task chips)
- **NLP Blue** (`#3b82f6`): Natural language processing
- **CV Purple** (`#8b5cf6`): Computer vision
- **Audio Green** (`#10b981`): Audio processing
- **Multimodal Pink** (`#ec4899`): Multimodal models

### Semantic
- **Success** (`#10b981`): Green
- **Warning** (`#f59e0b`): Amber
- **Error** (`#ef4444`): Red

## 3. Typography Rules

### Font Family
- **Display + Body**: `Source Sans 3, system-ui, sans-serif` — open-source humanist sans
- **Mono**: `IBM Plex Mono, Courier New, monospace` — for code blocks

### Hierarchy
- **Hero h1** — 36–48px Source Sans 3 weight 700, line-height 1.1
- **Model name (in card)** — 16–18px weight 600
- **Body** — 14–16px weight 400, line-height 1.5
- **Code** — 13–14px IBM Plex Mono weight 400, 1.6 line-height
- **Caption / metadata** — 13px weight 400, muted gray
- **Button label** — 14px weight 600

### Principles
- Weight 700 for hero h1; weight 600 for model names and labels
- Mono for code snippets, downloads counters, model IDs
- Tracking neutral (0) across the system

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 48–80px vertical — tighter than marketing-site convention because the site is content-dense. Model card listings run 1-up (full-width rows) at desktop on the model hub.

## 5. Componentry Feel

- **Model card listing** — Row with model author + model name + task tag chips + downloads count + likes count. Clickable to detail. Hover lifts background to `#f7f7f7`
- **Primary CTA (yellow pill)** — HF Yellow fill, dark text, full-pill radius, 40px height, weight-600 label
- **Secondary CTA** — Transparent fill, 1px gray border, ink text
- **Code snippet (tabbed)** — Code block with framework tabs at the top (PyTorch, TensorFlow, JAX), code in IBM Plex Mono, copy button in the top-right
- **Model likes / downloads stats** — Inline pill with heart icon + count, download icon + count
- **Task filter chips** — Pill-shaped task category filters (NLP, CV, Audio, Multimodal) with colored backgrounds

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use open-community developer language ("Share your model", "Try it in your browser"). Reference the GitHub-like community contract. Use technical precision in model card descriptions.

**Don't.** Don't write enterprise sales-speak. Don't sanitize the playful emoji brand mark. Don't translate "model card" to "AI product" — the community vocabulary is specific.

## 7. Motion Vocabulary

Functional minimal motion — 150ms hover on links and buttons, slight card lift on hover (1.01 scale). Model card "like" button has a satisfying scale-tick on click. The brand reads as developer-platform functional, never marketing-flashy.

## 8. Anti-patterns to Avoid

- **Don't replace the hugging face emoji with a stylized abstract mark.** It is the brand voice
- **Don't sanitize the community chrome.** "Sign in with GitHub" as primary auth is intentional
- **Don't tint the yellow voltage.** The specific #ff9d00 is brand
- **Don't strip the developer-doc aesthetic.** Hugging Face reads as docs-first
- **Don't sparsify the model card listings to "curated 6".** The brand is a long-tail community hub
- **Don't replace Source Sans 3 with Inter.** The open-source font choice is part of the brand's open-source positioning
- **Don't add scroll-triggered marketing reveals.** The chrome is utilitarian
