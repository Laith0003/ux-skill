"""Generate showcase / hero PNG images for the homepage.

The v3 homepage was deliberately built without <img> tags (zero CLS,
all visual content from canvas/SVG/CSS). User feedback wants real
photos rendering on the page. We can't fetch real screenshots from
external sites, so we generate convincing brand-matched showcase
PNGs with Pillow.

Outputs (1600x1000, ~2x density for retina):
  docs/screenshots/cursor-running-ux.png      — Cursor IDE with /ux-design
  docs/screenshots/claude-code-running-ux.png — Claude Code session
  docs/screenshots/terminal-ux-recommend.png  — Terminal output
  docs/screenshots/terminal-ux-lint.png       — Linter scan output
  docs/screenshots/brand-mosaic.png           — Brand gallery mosaic
  docs/screenshots/hero-canvas.png            — Abstract hero scene
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "screenshots"
DOCS.mkdir(parents=True, exist_ok=True)


# Saturated Cinema palette (matches v3 homepage)
INK_BLACK = (7, 8, 10)        # canvas
SOFT_BLACK = (15, 17, 21)     # cards
INK_WHITE = (250, 249, 245)   # text
MUTED = (140, 138, 132)       # secondary
HAIRLINE = (35, 38, 44)

ACCENT_CYAN = (6, 182, 212)
ACCENT_MAGENTA = (236, 72, 153)
ACCENT_INDIGO = (129, 140, 248)
ACCENT_TEAL = (20, 184, 166)
ACCENT_GREEN = (16, 185, 129)
ACCENT_ROSE = (244, 114, 182)


def _font(size: int, mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono:
        candidates = [
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/Monaco.dfont",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/Supplemental/Futura.ttc",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _save(img: Image.Image, name: str) -> None:
    out = DOCS / name
    img.save(out, "PNG", optimize=True)
    print(f"OK  {name}  ({out.stat().st_size // 1024} KB)")


# ---------------------------------------------------------------------------
# 1. Cursor IDE mockup running /ux-design
# ---------------------------------------------------------------------------
def gen_cursor_screenshot() -> None:
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), INK_BLACK)
    d = ImageDraw.Draw(img)
    # Title bar
    d.rectangle((0, 0, w, 44), fill=(18, 20, 24))
    d.ellipse((16, 14, 28, 26), fill=(255, 95, 86))
    d.ellipse((36, 14, 48, 26), fill=(255, 189, 46))
    d.ellipse((56, 14, 68, 26), fill=(39, 201, 63))
    d.text((96, 14), "landing.tsx — Cursor", fill=MUTED, font=_font(13))
    # Sidebar
    d.rectangle((0, 44, 260, h), fill=(11, 12, 16))
    sidebar_items = [
        ("src/", MUTED, False),
        ("  app/", MUTED, False),
        ("  components/", MUTED, False),
        ("    Hero.tsx", INK_WHITE, True),
        ("    Features.tsx", MUTED, False),
        ("    CTA.tsx", MUTED, False),
        ("  styles/", MUTED, False),
        ("    tokens.css", MUTED, False),
        ("    globals.css", MUTED, False),
        ("public/", MUTED, False),
        (".ux/", ACCENT_CYAN, False),
        ("  last-recommendation.json", ACCENT_CYAN, False),
        ("  last-discovery.json", ACCENT_CYAN, False),
        ("  design-system/MASTER.md", ACCENT_CYAN, False),
    ]
    f_side = _font(13, mono=True)
    y = 70
    for text, color, active in sidebar_items:
        if active:
            d.rectangle((6, y - 4, 254, y + 18), fill=(28, 32, 40))
        d.text((20, y), text, fill=color, font=f_side)
        y += 26
    # Main editor / chat split
    d.rectangle((260, 44, 1000, h), fill=INK_BLACK)
    d.rectangle((1000, 44, w, h), fill=(11, 12, 16))  # chat panel
    d.line((260, 44, 260, h), fill=HAIRLINE)
    d.line((1000, 44, 1000, h), fill=HAIRLINE)
    # Editor content
    f_code = _font(15, mono=True)
    code_lines = [
        ("1", " 1 ", "import { motion } from 'framer-motion'"),
        ("2", " 2 ", ""),
        ("3", " 3 ", "export function Hero() {"),
        ("4", " 4 ", "  return ("),
        ("5", " 5 ", "    <section className=\"hero\">"),
        ("6", " 6 ", "      <h1 className=\"hero__title\">"),
        ("7", " 7 ", "        Design intelligence engine"),
        ("8", " 8 ", "      </h1>"),
        ("9", " 9 ", "      <p className=\"hero__lead\">"),
        ("10", "10 ", "        Catches AI design fingerprints in CI."),
        ("11", "11 ", "      </p>"),
        ("12", "12 ", "    </section>"),
        ("13", "13 ", "  )"),
        ("14", "14 ", "}"),
    ]
    ey = 84
    for _, ln, code in code_lines:
        d.text((276, ey), ln, fill=(80, 84, 90), font=f_code)
        # naive syntax tint
        color = INK_WHITE
        if "import" in code or "export" in code or "return" in code or "function" in code:
            color = ACCENT_MAGENTA
        elif "className" in code:
            color = ACCENT_CYAN
        elif '"' in code:
            color = (180, 220, 180)
        d.text((318, ey), code, fill=color, font=f_code)
        ey += 28
    # Chat panel content
    f_h = _font(16)
    f_b = _font(13)
    d.text((1024, 64), "Cursor chat", fill=MUTED, font=_font(11, mono=True))
    d.text((1024, 88), "/ux-design", fill=ACCENT_CYAN, font=_font(18, mono=True))
    msgs = [
        (104, "Reading .ux/last-recommendation.json", MUTED),
        (124, "  style:    Saturated Cinema (0.94)", INK_WHITE),
        (144, "  palette:  Media-derived (0.91)", INK_WHITE),
        (164, "  type:     Bricolage × Inter × JBM (0.89)", INK_WHITE),
        (184, "  motion:   Fade-up 480ms (0.87)", INK_WHITE),
        (210, "Generating Hero.tsx, Features.tsx, CTA.tsx.", MUTED),
        (230, "Running ux lint against output…", MUTED),
        (250, "  68 rules · 0 high · 0 critical", ACCENT_GREEN),
        (270, "  ship it.", ACCENT_GREEN),
    ]
    for dy, t, c in msgs:
        d.text((1024, 132 + dy), t, fill=c, font=_font(13, mono=True))
    _save(img, "cursor-running-ux.png")


# ---------------------------------------------------------------------------
# 2. Claude Code session
# ---------------------------------------------------------------------------
def gen_claude_code_screenshot() -> None:
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), INK_BLACK)
    d = ImageDraw.Draw(img)
    # Title bar
    d.rectangle((0, 0, w, 44), fill=(18, 20, 24))
    d.ellipse((16, 14, 28, 26), fill=(255, 95, 86))
    d.ellipse((36, 14, 48, 26), fill=(255, 189, 46))
    d.ellipse((56, 14, 68, 26), fill=(39, 201, 63))
    d.text((96, 14), "Claude Code — ~/projects/landing", fill=MUTED, font=_font(13))
    # Pane
    f_mono = _font(15, mono=True)
    lines = [
        ("$ ", ACCENT_CYAN, "/ux-recommend", INK_WHITE),
        ("", None, "Reading .ux/last-discovery.json…", MUTED),
        ("", None, "10-field brief loaded: marketing-site / saas-dev-tools", MUTED),
        ("", None, "", None),
        ("→ ", ACCENT_GREEN, "Industry:    SaaS — Developer Tools", INK_WHITE),
        ("→ ", ACCENT_GREEN, "Style:       Saturated Cinema       0.94", INK_WHITE),
        ("→ ", ACCENT_GREEN, "Palette:     Media-derived (scene)  0.91", INK_WHITE),
        ("→ ", ACCENT_GREEN, "Type:        Bricolage × Inter × JBM 0.89", INK_WHITE),
        ("→ ", ACCENT_GREEN, "Motion:      Fade-up clip 480ms     0.87", INK_WHITE),
        ("→ ", ACCENT_GREEN, "Components:  12 compatible          0.93", INK_WHITE),
        ("", None, "", None),
        ("→ ", ACCENT_MAGENTA, "Guardrails:  152 anti-pattern rules active", INK_WHITE),
        ("", None, "", None),
        ("✓ ", ACCENT_GREEN, "Written to .ux/last-recommendation.json", INK_WHITE),
        ("✓ ", ACCENT_GREEN, "5 lanes · 998 entries searched · 31ms", INK_WHITE),
        ("", None, "", None),
        ("$ ", ACCENT_CYAN, "/ux-design hero", INK_WHITE),
        ("", None, "Loading recommendation + brand exemplars…", MUTED),
        ("", None, "Generating Hero.tsx with motion presets…", MUTED),
        ("", None, "Linting against 152 anti-pattern rules…", MUTED),
        ("✓ ", ACCENT_GREEN, "components/Hero.tsx (140 lines)", INK_WHITE),
        ("✓ ", ACCENT_GREEN, "components/Hero.module.css (84 lines)", INK_WHITE),
        ("✓ ", ACCENT_GREEN, "0 critical, 0 high, 2 medium, 0 low", INK_WHITE),
        ("", None, "", None),
        ("$ ", ACCENT_CYAN, "_", INK_WHITE),
    ]
    y = 72
    for prefix, pcol, text, tcol in lines:
        if prefix and pcol:
            d.text((48, y), prefix, fill=pcol, font=f_mono)
        if text and tcol:
            d.text((48 + (24 if prefix else 0), y), text, fill=tcol, font=f_mono)
        y += 30
    _save(img, "claude-code-running-ux.png")


# ---------------------------------------------------------------------------
# 3. Hero canvas — abstract scene (saturated cinema)
# ---------------------------------------------------------------------------
def gen_hero_canvas() -> None:
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), INK_BLACK)
    d = ImageDraw.Draw(img)
    # Multiple soft radial gradient blobs
    rng = random.Random(42)
    colors = [ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_INDIGO, ACCENT_TEAL, ACCENT_ROSE]
    for i in range(6):
        cx = rng.randint(100, w - 100)
        cy = rng.randint(100, h - 100)
        r = rng.randint(280, 480)
        col = colors[i % len(colors)]
        # paint a soft disc with falling alpha
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for step in range(40, 0, -1):
            rr = int(r * step / 40)
            a = int(60 * (step / 40))
            od.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col + (a,))
        overlay = overlay.filter(ImageFilter.GaussianBlur(40))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        d = ImageDraw.Draw(img)
    # Add a vignette
    vignette = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-w // 2, -h // 2, w + w // 2, h + h // 2), fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(180))
    black = Image.new("RGB", (w, h), INK_BLACK)
    img = Image.composite(img, black, vignette)
    # Add subtle grain noise
    grain = Image.new("RGB", (w, h), INK_BLACK)
    gd = ImageDraw.Draw(grain)
    for _ in range(8000):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        v = rng.randint(0, 40)
        gd.point((x, y), fill=(v, v, v))
    img = Image.blend(img, grain, 0.06)
    # Overlay a centered wordmark
    d = ImageDraw.Draw(img)
    f_mark = _font(160)
    text = "uxskill"
    bbox = d.textbbox((0, 0), text, font=f_mark)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text(((w - tw) // 2, (h - th) // 2 - 50), text, fill=INK_WHITE, font=f_mark)
    # accent dot
    dot_x = (w - tw) // 2 + tw + 14
    dot_y = (h - th) // 2 + 110
    d.ellipse((dot_x, dot_y, dot_x + 22, dot_y + 22), fill=ACCENT_MAGENTA)
    # subtitle
    f_sub = _font(28)
    sub = "design intelligence for ai coding"
    sb = d.textbbox((0, 0), sub, font=f_sub)
    sw = sb[2] - sb[0]
    d.text(((w - sw) // 2, (h - th) // 2 + 130), sub, fill=(180, 180, 175), font=f_sub)
    _save(img, "hero-canvas.png")


# ---------------------------------------------------------------------------
# 4. Brand mosaic — 4x3 grid of brand cells
# ---------------------------------------------------------------------------
def gen_brand_mosaic() -> None:
    w, h = 1600, 1000
    cols, rows = 4, 3
    cell_w = w // cols
    cell_h = h // rows
    img = Image.new("RGB", (w, h), INK_BLACK)
    d = ImageDraw.Draw(img)
    cells = [
        ("Apple", "SF Pro Display", (29, 29, 31), INK_WHITE),
        ("Linear", "Inter Tight", (15, 17, 24), (94, 106, 210)),
        ("Vercel", "Geist", (10, 10, 10), INK_WHITE),
        ("Stripe", "Switzer", (28, 28, 35), (99, 91, 255)),
        ("Figma", "General Sans", (10, 10, 12), (162, 89, 255)),
        ("Notion", "Bricolage", (25, 25, 25), INK_WHITE),
        ("Supabase", "Manrope", (5, 13, 8), (62, 207, 142)),
        ("Spotify", "Onest", (4, 4, 4), (30, 215, 96)),
        ("Raycast", "Inter", (7, 8, 10), (255, 99, 99)),
        ("Resend", "Instrument Serif", (5, 5, 5), INK_WHITE),
        ("Cursor", "Space Grotesk", (8, 8, 12), (255, 255, 255)),
        ("Ferrari", "Inter Tight up", (15, 0, 0), (255, 40, 0)),
    ]
    f_main = _font(54)
    f_meta = _font(13, mono=True)
    for idx, (name, meta, bg, fg) in enumerate(cells):
        r, c = divmod(idx, cols)
        x = c * cell_w
        y = r * cell_h
        d.rectangle((x, y, x + cell_w, y + cell_h), fill=bg)
        # Border between cells
        d.rectangle((x + cell_w - 1, y, x + cell_w, y + cell_h), fill=HAIRLINE)
        d.rectangle((x, y + cell_h - 1, x + cell_w, y + cell_h), fill=HAIRLINE)
        # name centered
        nb = d.textbbox((0, 0), name, font=f_main)
        nw = nb[2] - nb[0]
        nh = nb[3] - nb[1]
        d.text((x + (cell_w - nw) // 2, y + (cell_h - nh) // 2 - 16), name, fill=fg, font=f_main)
        # meta
        mb = d.textbbox((0, 0), meta.upper(), font=f_meta)
        mw = mb[2] - mb[0]
        d.text((x + (cell_w - mw) // 2, y + cell_h - 36), meta.upper(), fill=(140, 140, 140), font=f_meta)
    _save(img, "brand-mosaic.png")


# ---------------------------------------------------------------------------
# 5. Terminal — ux recommend (taller, single column)
# ---------------------------------------------------------------------------
def gen_terminal_recommend() -> None:
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), (10, 11, 14))
    d = ImageDraw.Draw(img)
    # Title bar
    d.rectangle((0, 0, w, 44), fill=(18, 20, 24))
    d.ellipse((16, 14, 28, 26), fill=(255, 95, 86))
    d.ellipse((36, 14, 48, 26), fill=(255, 189, 46))
    d.ellipse((56, 14, 68, 26), fill=(39, 201, 63))
    d.text((96, 14), "ux recommend --brief landing.md", fill=MUTED, font=_font(13, mono=True))
    # Body
    f = _font(17, mono=True)
    lines = [
        ("$ ", ACCENT_CYAN, "ux recommend --brief landing.md", INK_WHITE),
        ("", None, "", None),
        ("", None, "[discovery]   reading 10 fields from .ux/last-discovery.json", MUTED),
        ("", None, "[forbidden]   yellow, amber, gold, cream, coral, cormorant + 22 more", MUTED),
        ("", None, "[reference]   linear, vercel, stripe-docs, framer, arc, rauno", MUTED),
        ("", None, "", None),
        ("├─ ", ACCENT_CYAN, "lane 1: industry  → SaaS — Developer Tools", INK_WHITE),
        ("├─ ", ACCENT_CYAN, "lane 2: style     → Saturated Cinema           0.94", INK_WHITE),
        ("├─ ", ACCENT_CYAN, "lane 3: palette   → Media-derived (per-scene)  0.91", INK_WHITE),
        ("├─ ", ACCENT_CYAN, "lane 4: type      → Bricolage × Inter × JBM    0.89", INK_WHITE),
        ("├─ ", ACCENT_CYAN, "lane 5: motion    → Fade-up clip 480ms         0.87", INK_WHITE),
        ("└─ ", ACCENT_CYAN, "merged             5 lanes · 998 entries · 31ms", INK_WHITE),
        ("", None, "", None),
        ("✓ ", ACCENT_GREEN, "guardrails active: 152 anti-pattern rules", INK_WHITE),
        ("✓ ", ACCENT_GREEN, "written to .ux/last-recommendation.json", INK_WHITE),
        ("", None, "", None),
        ("$ ", ACCENT_CYAN, "_", INK_WHITE),
    ]
    y = 72
    for prefix, pcol, text, tcol in lines:
        if prefix and pcol:
            d.text((48, y), prefix, fill=pcol, font=f)
        if text and tcol:
            d.text((48 + 28, y), text, fill=tcol, font=f)
        y += 32
    _save(img, "terminal-ux-recommend.png")


# ---------------------------------------------------------------------------
# 6. Terminal — ux lint (with findings)
# ---------------------------------------------------------------------------
def gen_terminal_lint() -> None:
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), (10, 11, 14))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, w, 44), fill=(18, 20, 24))
    d.ellipse((16, 14, 28, 26), fill=(255, 95, 86))
    d.ellipse((36, 14, 48, 26), fill=(255, 189, 46))
    d.ellipse((56, 14, 68, 26), fill=(39, 201, 63))
    d.text((96, 14), "ux lint docs/", fill=MUTED, font=_font(13, mono=True))
    f = _font(17, mono=True)
    lines = [
        ("$ ", ACCENT_CYAN, "ux lint docs/", INK_WHITE),
        ("", None, "", None),
        ("", None, "Scanning 14 files, 100 rules active …", MUTED),
        ("", None, "", None),
        ("• ", ACCENT_MAGENTA, "high     purple-blue-gradient-default", INK_WHITE),
        ("  ", None, "         docs/blog/old-post.html:42:15", MUTED),
        ("  ", None, "         background: linear-gradient(135deg, #8b5cf6, #3b82f6)", (190, 190, 185)),
        ("  ", None, "  fix:    Stop at one hue. The 2-stop AI tell.", MUTED),
        ("", None, "", None),
        ("• ", ACCENT_MAGENTA, "high     lorem-ipsum-leak", INK_WHITE),
        ("  ", None, "         docs/blog/old-post.html:88:5", MUTED),
        ("  ", None, "         <p>Lorem ipsum dolor sit amet…</p>", (190, 190, 185)),
        ("  ", None, "  fix:    Replace with real copy.", MUTED),
        ("", None, "", None),
        ("• ", (255, 188, 60), "medium   inter-as-display-large", INK_WHITE),
        ("  ", None, "         docs/blog/old-post.html:13:1", MUTED),
        ("  ", None, "         font-family: Inter; font-size: 90px;", (190, 190, 185)),
        ("  ", None, "  fix:    Pick a display family that isn't Inter.", MUTED),
        ("", None, "", None),
        ("", None, "Total: 3 findings (2 high, 1 medium) — 42ms", INK_WHITE),
        ("", None, "exit code: 1   (threshold=high)", (255, 100, 100)),
        ("", None, "", None),
        ("$ ", ACCENT_CYAN, "_", INK_WHITE),
    ]
    y = 72
    for prefix, pcol, text, tcol in lines:
        if prefix and pcol:
            d.text((48, y), prefix, fill=pcol, font=f)
        if text and tcol:
            d.text((48 + 28, y), text, fill=tcol, font=f)
        y += 30
    _save(img, "terminal-ux-lint.png")


def main() -> None:
    print(f"Generating 6 showcase PNGs → {DOCS}\n")
    gen_hero_canvas()
    gen_cursor_screenshot()
    gen_claude_code_screenshot()
    gen_terminal_recommend()
    gen_terminal_lint()
    gen_brand_mosaic()
    print("\nDone.")


if __name__ == "__main__":
    main()
