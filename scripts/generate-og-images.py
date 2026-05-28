"""Generate per-page OpenGraph images at 1200x630 from a page-title list.

Output: docs/og/<slug>.png. No external assets needed — typography is
rendered from system fonts via Pillow's font loader with sensible fallbacks.

Style decisions:
  - Pure black canvas, white wordmark + headline, neutral subtitle.
  - One accent dot (#e85d50 / warm signal red) in the wordmark.
  - Wordmark bottom-left ("ux•"), title centered, eyebrow centered above.
  - Large title up to 80px; auto-shrinks if it overruns two lines.

The image deliberately ships zero gradient / glass / emoji / brand-clone
clutter — it should read as a serious dev-tool, not as marketing.

Idempotent: re-running overwrites any existing PNGs.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "og"
OUT_DIR.mkdir(parents=True, exist_ok=True)
LANDING_OUT_DIR = ROOT / "landing" / "og"
LANDING_OUT_DIR.mkdir(parents=True, exist_ok=True)


# slug -> (eyebrow, title, optional subtitle)
PAGES = {
    "home":                       ("ux-skill", "Design intelligence engine\nfor AI coding tools", "998 entries · 85+ anti-pattern rules · 92 brand specs"),
    "compare":                    ("Compare", "Every Claude design skill,\nside by side", "ux-skill 46/50 · next best 30/50"),
    "about":                      ("About", "Why ux-skill exists", "From the prose-only v1 to the queryable Python engine"),
    "faq":                        ("FAQ", "25 questions,\nanswered straight", "Install, license, plugin landscape, MCP"),
    "roadmap":                    ("Roadmap", "What ships next", "v2.1 -> v2.5 -> v3.0 milestones"),
    "mcp":                        ("MCP server", "14 tools over stdio.\nAny MCP host.", "Claude Desktop · Cursor · Windsurf · generic agents"),
    "blog-index":                 ("Blog", "Long-form writing on\nAI coding's design problem", "Honest comparisons. Real numbers. No marketing verbs."),
    "vs-ui-ux-pro-max":           ("Comparison", "ui-ux-pro-max alternative —\nthe honest table", "998 entries vs ~600 · 85-rule linter vs none"),
    "anti-ai-slop-claude-skills": ("Ranking", "Anti-AI-slop tools for\nClaude Code in 2026", "taste-skill · hallmark · ux-skill v2"),
    "best-claude-code-design-skills-2026": ("Ranking", "Best Claude Code skills\nfor UX/UI design (2026)", "ui-ux-pro-max · open-design · taste-skill · huashu · ux-skill"),
    "cursor-design-plugin":       ("Integration", "Cursor design plugin", "Install ux-skill via npx · 85-rule linter"),
    "python-design-system-generator": ("Architecture", "Python design system\ngenerator — 5-parallel-search", "998 entries · 5 lanes · one recommendation · pip install"),
    "ai-design-fingerprints-list":("Catalog", "The 35 AI design\nfingerprints, listed", "Detection regex · why each is slop · the fix"),
    "claude-code-marketplace-best-plugins": ("Marketplace", "Best Claude Code\nmarketplace plugins (2026)", "All 8 popular UX skills · honest ranking"),
    "figma-vs-ux-skill":          ("Comparison", "Figma vs ux-skill", "Different jobs · honest table"),
    "windsurf-design-rules":      ("Integration", "Windsurf design rules", "Install ux-skill in Windsurf"),
    "monorepo-design-system-ai-coding": ("Architecture", "Monorepo design system\nfor AI coding", "One MASTER.md · all agents grounded"),
    "regex-linter-for-ai-coding": ("Tooling", "Regex linter for\nAI coding output", "85 rules · deterministic · no LLM"),
    "dark-editorial-cinema-design": ("Design", "Dark editorial cinema design", "Charcoal + variable opsz + scroll-pinned scenes"),
    "mcp-server-design-intelligence": ("MCP", "MCP server for\ndesign intelligence", "14 tools over stdio"),
    "motion-presets-framer-gsap-css": ("Motion", "Motion presets — Framer,\nGSAP, CSS", "57 presets · 8 categories · 3 engines"),
    "dogfooding-design-engine":   ("Story", "Dogfooding ux-skill —\nbugs we found by using it", "Two engine bugs filed against ourselves · both fixed"),
}


CANVAS = (12, 11, 9)        # near-black ink (#0c0b09)
INK = (250, 249, 245)       # canvas white (#faf9f5)
MUTED = (140, 138, 132)     # neutral gray
ACCENT = (232, 93, 80)      # signal red dot (#e85d50)


def _font(size: int) -> ImageFont.FreeTypeFont:
    """Load a serviceable display font. Falls back through common system locations."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Futura.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _mono_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.dfont",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _draw_wordmark(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    """ux<•> in a 28px serif-ish bold."""
    f = _font(34)
    d.text((x, y), "ux", fill=INK, font=f)
    # the dot — small circle to the right of the wordmark
    bbox = d.textbbox((x, y), "ux", font=f)
    cx = bbox[2] + 8
    cy = y + 14
    d.ellipse((cx, cy, cx + 9, cy + 9), fill=ACCENT)


def _draw_eyebrow(d: ImageDraw.ImageDraw, text: str, w: int, y: int) -> None:
    f = _mono_font(20)
    text = text.upper()
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    d.text(((w - tw) // 2, y), text, fill=MUTED, font=f)


def _draw_title(d: ImageDraw.ImageDraw, text: str, w: int, h: int) -> int:
    """Draw the headline centered, return its bottom y."""
    size = 84
    lines = text.split("\n")
    # auto-shrink if any line too wide
    while size > 44:
        f = _font(size)
        wide = max((d.textbbox((0, 0), line, font=f)[2] for line in lines), default=0)
        if wide < w - 160:
            break
        size -= 6
    f = _font(size)
    line_h = int(size * 1.12)
    total_h = line_h * len(lines)
    y = (h - total_h) // 2 - 20
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        d.text(((w - tw) // 2, y), line, fill=INK, font=f)
        y += line_h
    return y


def _draw_subtitle(d: ImageDraw.ImageDraw, text: str, w: int, y: int) -> None:
    f = _font(28)
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    d.text(((w - tw) // 2, y + 8), text, fill=MUTED, font=f)


def _draw_footer(d: ImageDraw.ImageDraw, w: int, h: int) -> None:
    f = _mono_font(18)
    text = "uxskill.laithjunaidy.com"
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    d.text(((w - tw) // 2, h - 64), text, fill=MUTED, font=f)


def generate_one(slug: str, eyebrow: str, title: str, subtitle: str) -> Path:
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), CANVAS)
    d = ImageDraw.Draw(img)
    # wordmark top-left
    _draw_wordmark(d, 60, 50)
    # eyebrow centered, just above the title
    _draw_eyebrow(d, eyebrow, w, 170)
    # title centered, big
    bottom = _draw_title(d, title, w, h)
    # subtitle below the title
    if subtitle:
        _draw_subtitle(d, subtitle, w, bottom)
    # footer url
    _draw_footer(d, w, h)
    # thin hairline divider at the very bottom
    d.rectangle((60, h - 30, w - 60, h - 29), fill=(40, 38, 34))
    # save to docs/og + landing/og
    out = OUT_DIR / f"{slug}.png"
    img.save(out, "PNG", optimize=True)
    img.save(LANDING_OUT_DIR / f"{slug}.png", "PNG", optimize=True)
    return out


def main() -> None:
    print(f"Generating {len(PAGES)} OG images at {OUT_DIR}\n")
    for slug, (eb, title, sub) in PAGES.items():
        p = generate_one(slug, eb, title, sub)
        print(f"OK  {p.name}  ({Path(p).stat().st_size // 1024} KB)")
    print(f"\nDone. {len(PAGES)} PNGs written to docs/og/ and landing/og/.")


if __name__ == "__main__":
    main()
