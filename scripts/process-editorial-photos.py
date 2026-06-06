"""Optimize the 10 picsum.photos editorial JPEGs into smaller, web-ready files.

Steps per photo:
  - Resize to max 1600px wide
  - Apply a slight dark gradient overlay (so they match the Saturated Cinema theme)
  - Save at JPEG quality 78 (~80-120 KB target)
  - Generate a tiny 24px-wide blur placeholder (for LQIP / blur-up loading)

Outputs:
  docs/editorial/editorial-<n>.jpg          full (~100 KB each)
  docs/editorial/editorial-<n>-tiny.jpg     LQIP (~1 KB each)

All source images are from https://picsum.photos — CC0 licensed.
Attribution: Lorem Picsum (https://picsum.photos), photos by Unsplash contributors.
"""
from pathlib import Path
from PIL import Image, ImageFilter
import io


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "editorial"


def darken_gradient(img: Image.Image) -> Image.Image:
    """Top-to-bottom subtle dark overlay so text reads on the photo."""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        # 12% darkening at top → 38% darkening at bottom
        alpha = int(30 + (y / h) * 70)
        for x_band in range(0, w, 80):
            pass  # we'll just draw the line
        overlay.paste((0, 0, 0, alpha), (0, y, w, y + 1))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def process_one(src: Path) -> None:
    img = Image.open(src).convert("RGB")
    # Resize to max 1600 wide
    if img.width > 1600:
        new_h = int(1600 * img.height / img.width)
        img = img.resize((1600, new_h), Image.LANCZOS)
    # Apply subtle dark gradient (top→bottom)
    img = darken_gradient(img)
    # Save optimized
    out = DOCS / src.name
    img.save(out, "JPEG", quality=78, optimize=True, progressive=True)
    # Tiny LQIP — 24 wide, blurred
    tiny = img.copy()
    tiny.thumbnail((24, 24 * img.height // img.width), Image.LANCZOS)
    tiny = tiny.filter(ImageFilter.GaussianBlur(1.5))
    tiny_name = src.stem + "-tiny.jpg"
    tiny_out = DOCS / tiny_name
    tiny.save(tiny_out, "JPEG", quality=60, optimize=True)
    kb_main = out.stat().st_size // 1024
    kb_tiny = tiny_out.stat().st_size // 1024
    print(f"  ok  {src.name:24s}  {kb_main:>4} KB  + lqip {kb_tiny} KB")


def main() -> None:
    photos = sorted(DOCS.glob("editorial-*.jpg"))
    # Skip already-processed tinies
    photos = [p for p in photos if "-tiny" not in p.name]
    print(f"Processing {len(photos)} editorial photos\n")
    for p in photos:
        process_one(p)
    print(f"\nDone.")


if __name__ == "__main__":
    main()
