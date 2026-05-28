# Design System Inspired by Asana

## 1. Visual Theme & Atmosphere

Asana's web presence is project-management-as-flow chrome — a coral-orange primary (#fc636b) as the brand voltage, the three-dot brand mark referencing teams in coordination, illustration-driven heroes featuring teams in motion, and a soft-rounded card grammar that reads as approachable enterprise. The atmosphere is friendly productivity SaaS. The brand's tagline ("work without the chaos") shapes the entire chrome — every page sells the calm-after-the-storm of having work organized.

Where peer project-management tools (Jira, Monday, Trello) lean into different aesthetic positionings (Jira is enterprise-rectilinear, Monday is colorful-grid, Trello is kanban-classic), Asana leans into warm-illustration friendliness. The hero illustrations show people collaborating, task boards in action, gantt timelines syncing — the brand is selling the feeling of coordinated work, not the database underneath.

The Asana coral (#fc636b) is the chromatic voltage. It is a specific warm coral — neither true red nor salmon — and pairs with a near-black ink to create the brand's high-warmth contrast. The coral appears on CTAs, on the three-dot brand mark, and as accents inside illustrations.

**Key Characteristics:**
- Asana coral (#fc636b) — chromatic voltage on CTAs and wordmark
- Three-dot brand mark — circular triad referencing teams in coordination
- Soft rounded cards (8–16px radius) — approachable enterprise
- Friendly workflow-illustration heroes — teams collaborating
- Asana Sans typography across chrome
- Workflow-themed mockups (gantt, kanban, task cards) carry the visual atmosphere

## 2. Color Palette & Roles

### Primary
- **Asana Coral** (`#fc636b`): The brand voltage — CTAs, wordmark, accents
- **Coral Hover** (`#c54f56`): Press state
- **Coral Soft** (`#fde2e3`): Subtle background tint

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f9fafb`): Alternating section bands
- **Surface Card** (`#f5f5f7`): Card hover state
- **Hairline** (`#e8e8eb`): 1px borders

### Neutrals & Text
- **Ink** (`#0d1f2d`): Primary text
- **Body** (`#2c3a47`): Default body text
- **Muted** (`#6b6f76`): Captions
- **Muted Soft** (`#a4a8b0`): Fine-print

### Workflow Color Tags (task labels)
- **High Priority Red** (`#e83e3e`)
- **Medium Priority Orange** (`#f59e0b`)
- **Low Priority Yellow** (`#eab308`)
- **Mint** (`#22c55e`)
- **Sky** (`#3b82f6`)
- **Lavender** (`#a855f7`)

### Semantic
- **Success** (`#22c55e`): Green
- **Warning** (`#f59e0b`): Amber
- **Error** (`#e83e3e`): Red

## 3. Typography Rules

### Font Family
- **Display + Body**: `Asana Sans, Inter, system-ui, sans-serif` — proprietary humanist sans (open-source substitute: Inter)

### Hierarchy
- **Hero h1** — 48–64px Asana Sans weight 700, line-height 1.1
- **Section h2** — 32–40px weight 700
- **Card title** — 20–24px weight 600
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 600

### Principles
- Weight 700 for hero h1
- Body sits at 16–18px for friendly reading pace
- Tracking neutral (0)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 80–120px vertical. Feature card grids run 3-up at desktop.

## 5. Componentry Feel

- **Primary CTA (coral pill)** — Asana Coral fill, white text, full-pill radius, 44px height, weight-600 label
- **Secondary CTA** — Transparent fill, 2px Asana Coral border, coral text
- **Task card mockup** — Soft rounded card (12px) with task title, owner avatar, due date, priority chip — used in hero illustrations to demonstrate the product
- **Gantt timeline visualization** — Multi-row horizontal bars in workflow colors showing project timelines
- **Hero illustration team** — Illustrated people collaborating on a task board with the Asana task cards visible
- **Feature card (soft radius)** — White surface, 12–16px radius, hairline border, internal padding 24px

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use calm-productivity language ("Work without the chaos", "Bring your work together"). Reference team coordination contexts. Use sentence case for chrome.

**Don't.** Don't write urgency-driven copy ("Get more done faster!"). Don't sanitize the warm-illustration personality. Don't use exclamation points except in onboarding moments.

## 7. Motion Vocabulary

Gentle workflow-themed micro-animations — task cards have a subtle hover lift (1.01 scale + 200ms ease). The three-dot brand mark may pulse on landing. Carousel transitions use 300ms ease-in-out. The brand reads as friendly-productive.

## 8. Anti-patterns to Avoid

- **Don't replace Asana coral with a saturated red.** The specific warm coral is brand
- **Don't sharpen card radii below 8px.** Friendly SaaS softness
- **Don't strip the three-dot brand mark.** It is the brand identity anchor
- **Don't sanitize the workflow-illustration heroes to generic enterprise stock.** The hand-illustrated personality is brand
- **Don't pair the coral with a second saturated brand accent.** The coral is the voltage
- **Don't use weight 600 for hero h1.** Weight 700 is the brand standard
- **Don't add aggressive scroll-triggered motion.** Asana's brand voice is calm-productive
