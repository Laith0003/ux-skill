"""Force every HTML file to the dark Saturated Cinema theme.

Earlier theme-migration agents reported success but several blog posts
+ docs pages still ship the OLD cream + coral + Cormorant CSS tokens
in their `<style>` blocks. This script does a deterministic find-replace
on the ACTUAL color values + font references — no agent guesswork.

Token map (old → new):
  Backgrounds + ink:
    #faf9f5  → #07080a   (canvas)
    #efe9de  → #0d0f12   (surface-1)
    #f3eee4  → #14181d   (surface-2)
    #f4f0e8  → #14181d   (surface-2)
    #ece6dc  → #1c2128   (surface-3)
    #181715  → #f6f7f9   (ink — INVERTED)
    #3d3d3a  → #c7ccd3   (body — INVERTED)
    #6c6a64  → #8a8f96   (muted — INVERTED)
  Accent (coral) → magenta scene-accent:
    #cc785c  → #ec4899
    #a9583e  → #be185d
    rgba(204,120,92,0.12)  → rgba(236,72,153,0.10)
    rgba(204,120,92,0.04)  → rgba(236,72,153,0.04)
    rgba(204,120,92,0.08)  → rgba(236,72,153,0.08)
    rgba(204,120,92,0.4)   → rgba(236,72,153,0.4)
  Hairlines (dark on light → light on dark):
    rgba(20,20,19,0.10)    → rgba(246,247,249,0.07)
    rgba(20,20,19,0.18)    → rgba(246,247,249,0.14)
    rgba(20, 20, 19, 0.10) → rgba(246, 247, 249, 0.07)
    rgba(20, 20, 19, 0.18) → rgba(246, 247, 249, 0.14)
    rgba(24,23,21,0.18)    → rgba(0,0,0,0.55)
    rgba(24,23,21,0.12)    → rgba(0,0,0,0.45)
  Win/weak/neutral ramp — invert for dark base:
    #ecf2ec → rgba(16, 185, 129, 0.14)
    #2f7d32 → #34d399
    #f5e6e3 → rgba(244, 114, 182, 0.14)
    #b3261e → #f472b6
    #f4f0e8 → rgba(246, 247, 249, 0.08)
  Fonts:
    'Cormorant Garamond', serif → 'Bricolage Grotesque', 'Inter Tight', system-ui, sans-serif
    family=Cormorant+Garamond:wght@500;600;700 → family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,300..800
  Meta:
    <meta name="theme-color" content="#faf9f5"> → "#07080a"
    <meta name="color-scheme" content="light">  → "dark"

Idempotent: re-running is safe. Pages already on dark are unchanged.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent


REPLACEMENTS = [
    # --- meta ---
    ('<meta name="theme-color" content="#faf9f5">', '<meta name="theme-color" content="#07080a">'),
    ('<meta name="color-scheme" content="light">', '<meta name="color-scheme" content="dark">'),

    # --- Color tokens (hex, both quoted and bare) ---
    ('#faf9f5', '#07080a'),
    ('#efe9de', '#0d0f12'),
    ('#f3eee4', '#14181d'),
    ('#f4f0e8', '#14181d'),
    ('#ece6dc', '#1c2128'),
    ('#c8e0c2', 'rgba(16, 185, 129, 0.20)'),
    ('#1f5713', '#6ee7b7'),
    ('#ddebd9', 'rgba(16, 185, 129, 0.14)'),
    ('#28681c', '#34d399'),
    ('#f4e5dc', 'rgba(244, 114, 182, 0.14)'),
    ('#a4502f', '#f472b6'),
    ('#ecf2ec', 'rgba(16, 185, 129, 0.14)'),
    ('#2f7d32', '#34d399'),
    ('#f5e6e3', 'rgba(244, 114, 182, 0.14)'),
    ('#b3261e', '#f472b6'),
    # ink + body (inverted polarity)
    ('#181715', '#f6f7f9'),
    ('#3d3d3a', '#c7ccd3'),
    ('#6c6a64', '#8a8f96'),
    # coral → magenta
    ('#cc785c', '#ec4899'),
    ('#a9583e', '#be185d'),

    # --- rgba color helpers ---
    ('rgba(204,120,92,0.04)', 'rgba(236, 72, 153, 0.04)'),
    ('rgba(204,120,92,0.08)', 'rgba(236, 72, 153, 0.08)'),
    ('rgba(204,120,92,0.12)', 'rgba(236, 72, 153, 0.10)'),
    ('rgba(204,120,92,0.4)',  'rgba(236, 72, 153, 0.4)'),
    ('rgba(204, 120, 92, 0.04)', 'rgba(236, 72, 153, 0.04)'),
    ('rgba(204, 120, 92, 0.08)', 'rgba(236, 72, 153, 0.08)'),
    ('rgba(204, 120, 92, 0.12)', 'rgba(236, 72, 153, 0.10)'),
    ('rgba(204, 120, 92, 0.4)',  'rgba(236, 72, 153, 0.4)'),

    # --- hairlines ---
    ('rgba(20,20,19,0.10)',   'rgba(246, 247, 249, 0.07)'),
    ('rgba(20,20,19,0.18)',   'rgba(246, 247, 249, 0.14)'),
    ('rgba(20, 20, 19, 0.10)', 'rgba(246, 247, 249, 0.07)'),
    ('rgba(20, 20, 19, 0.18)', 'rgba(246, 247, 249, 0.14)'),
    ('rgba(24,23,21,0.18)',   'rgba(0, 0, 0, 0.55)'),
    ('rgba(24,23,21,0.12)',   'rgba(0, 0, 0, 0.45)'),
    ('rgba(24, 23, 21, 0.18)', 'rgba(0, 0, 0, 0.55)'),
    ('rgba(24, 23, 21, 0.12)', 'rgba(0, 0, 0, 0.45)'),

    # --- Fonts ---
    ("'Cormorant Garamond', serif", "'Bricolage Grotesque', 'Inter Tight', system-ui, sans-serif"),
    ("'Cormorant Garamond', Georgia, serif", "'Bricolage Grotesque', 'Inter Tight', system-ui, sans-serif"),

    # --- Google Fonts URL — swap Cormorant family request to Bricolage Grotesque variable ---
    ("family=Cormorant+Garamond:wght@500;600;700",
     "family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,300..800"),
    ("family=Cormorant+Garamond:wght@500;600;700&",
     "family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,300..800&"),

    # --- Box-shadow softening for dark ---
    ('box-shadow: 0 16px 36px -20px rgba(24,23,21,0.18)',
     'box-shadow: 0 16px 36px -20px rgba(0, 0, 0, 0.55)'),
    ('box-shadow: 0 8px 28px -16px rgba(24,23,21,0.12)',
     'box-shadow: 0 8px 28px -16px rgba(0, 0, 0, 0.45)'),
    ('box-shadow: 0 12px 40px -22px rgba(24,23,21,0.18)',
     'box-shadow: 0 12px 40px -22px rgba(0, 0, 0, 0.55)'),
]


SENTINEL = "<!-- force-dark-theme: applied -->"


def patch(path: Path) -> tuple[bool, int]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    # Check if any old-token signature is present
    needs_patch = any(old in text for old, _ in REPLACEMENTS if old in text)
    if not needs_patch and SENTINEL in text:
        return False, 0

    swaps = 0
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
            swaps += 1

    # Mark patched
    if SENTINEL not in text and "</head>" in text and swaps > 0:
        text = text.replace("</head>", f"  {SENTINEL}\n</head>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True, swaps
    return False, 0


def main() -> None:
    targets = []
    for root_dir in (ROOT / "docs",):
        targets.extend(root_dir.rglob("*.html"))
    targets.sort()
    print(f"Scanning {len(targets)} HTML files\n")
    changed = 0
    for p in targets:
        ok, swaps = patch(p)
        if ok:
            rel = str(p.relative_to(ROOT))
            print(f"ok   {rel:<60}  ({swaps} swaps)")
            changed += 1
    print(f"\nDone. {changed}/{len(targets)} files force-darkened.")


if __name__ == "__main__":
    main()
