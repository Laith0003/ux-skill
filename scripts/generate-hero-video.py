"""Generate a 6-second cinematic hero video loop for the homepage.

Pipeline:
  1. Pillow generates 180 PNG frames (6 seconds @ 30fps) at 1920x1080.
  2. ffmpeg encodes them to MP4 (H.264, AAC silent) and WebM (VP9, no audio).
  3. Saves to docs/media/hero-loop.mp4 + docs/media/hero-loop.webm.

The video shows abstract saturated-cinema blobs morphing while the
uxskill wordmark fades in centered. Auto-loops, plays muted, designed
for `<video autoplay muted loop playsinline>` in the hero.

Each frame: layered radial gradient discs (cyan / magenta / indigo /
teal) drifting + breathing. Subtle particle drift. Film grain noise.
A vignette that pulls focus to center. Wordmark crossfades after 1.5s.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent.parent
FRAMES_DIR = ROOT / ".build" / "hero-frames"
OUT_DIR = ROOT / "docs" / "media"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080
FPS = 30
DURATION = 6.0       # seconds
TOTAL_FRAMES = int(FPS * DURATION)

# Saturated Cinema palette
INK_BLACK = (7, 8, 10)
INK_WHITE = (250, 249, 245)
ACCENT_CYAN = (6, 182, 212)
ACCENT_MAGENTA = (236, 72, 153)
ACCENT_INDIGO = (129, 140, 248)
ACCENT_TEAL = (20, 184, 166)
ACCENT_ROSE = (244, 114, 182)


def _font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Supplemental/Futura.ttc",
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


def render_frame(frame_idx: int) -> Image.Image:
    """Render a single 1920x1080 frame."""
    t = frame_idx / TOTAL_FRAMES  # 0.0 → 1.0
    img = Image.new("RGBA", (W, H), INK_BLACK + (255,))

    # ----- Layered radial blobs (4 of them, slow orbit) -----
    blobs = [
        # (center_base, color, radius_base, orbit_phase)
        ((W * 0.30, H * 0.40), ACCENT_CYAN,     520, 0.0),
        ((W * 0.72, H * 0.55), ACCENT_MAGENTA,  600, 0.25),
        ((W * 0.45, H * 0.78), ACCENT_INDIGO,   480, 0.55),
        ((W * 0.65, H * 0.30), ACCENT_TEAL,     420, 0.80),
    ]
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for (cx, cy), color, base_r, phase in blobs:
        # orbit drift — small ellipse around base center
        ang = 2 * math.pi * (t + phase)
        ox = math.cos(ang) * 80
        oy = math.sin(ang) * 50
        cx2 = cx + ox
        cy2 = cy + oy
        # breathing radius
        r = base_r + math.sin(2 * math.pi * (t + phase) * 2) * 60
        # soft falloff via stacked discs
        for step in range(38, 0, -1):
            rr = int(r * step / 38)
            a = int(70 * (step / 38))
            od.ellipse((cx2 - rr, cy2 - rr, cx2 + rr, cy2 + rr), fill=color + (a,))
    overlay = overlay.filter(ImageFilter.GaussianBlur(36))
    img = Image.alpha_composite(img, overlay)

    # ----- Particle drift -----
    rng = random.Random(frame_idx + 99)
    particles = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(particles)
    for _ in range(80):
        px = rng.randint(0, W - 1)
        py = rng.randint(0, H - 1)
        s = rng.choice([1, 2, 2, 3])
        a = rng.randint(80, 180)
        pd.ellipse((px, py, px + s, py + s), fill=(255, 255, 255, a))
    img = Image.alpha_composite(img, particles)

    # ----- Vignette -----
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-W // 2, -H // 2, W + W // 2, H + H // 2), fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(220))
    black_img = Image.new("RGBA", (W, H), (8, 9, 12, 255))
    img = Image.composite(img.convert("RGBA"), black_img, vignette)

    # ----- Wordmark — fades in between frames 30-90, hangs 90-150, fades out 150-180 -----
    if frame_idx > 30:
        d = ImageDraw.Draw(img)
        if frame_idx < 90:
            alpha = (frame_idx - 30) / 60
        elif frame_idx < 150:
            alpha = 1.0
        else:
            alpha = max(0.0, 1.0 - (frame_idx - 150) / 30)
        if alpha > 0.02:
            # Wordmark layer with alpha
            mark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            md = ImageDraw.Draw(mark)
            f_mark = _font(220)
            text = "uxskill"
            bb = md.textbbox((0, 0), text, font=f_mark)
            tw = bb[2] - bb[0]
            th = bb[3] - bb[1]
            tx = (W - tw) // 2
            ty = (H - th) // 2 - 60
            md.text((tx, ty), text, fill=(250, 249, 245, int(255 * alpha)), font=f_mark)
            # accent dot
            dot_x = tx + tw + 26
            dot_y = ty + 160
            md.ellipse((dot_x, dot_y, dot_x + 30, dot_y + 30), fill=ACCENT_MAGENTA + (int(255 * alpha),))
            # subtitle
            f_sub = _font(36)
            sub = "design intelligence for ai coding"
            sb = md.textbbox((0, 0), sub, font=f_sub)
            sw = sb[2] - sb[0]
            md.text(((W - sw) // 2, ty + th + 70), sub, fill=(190, 190, 185, int(220 * alpha)), font=f_sub)
            img = Image.alpha_composite(img, mark)

    # ----- Subtle grain noise -----
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    for _ in range(2000):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        v = rng.randint(0, 60)
        gd.point((x, y), fill=(v, v, v, 50))
    img = Image.alpha_composite(img, grain)

    return img.convert("RGB")


def render_all_frames() -> None:
    print(f"Rendering {TOTAL_FRAMES} frames at {W}x{H} @ {FPS}fps")
    for i in range(TOTAL_FRAMES):
        f = render_frame(i)
        f.save(FRAMES_DIR / f"frame_{i:04d}.png", "PNG", optimize=False)
        if i % 30 == 0:
            print(f"  frame {i:>4}/{TOTAL_FRAMES}")
    print("frames rendered.")


def encode_mp4() -> None:
    out = OUT_DIR / "hero-loop.mp4"
    print(f"Encoding MP4 → {out}")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "slower",
        "-crf", "22",
        "-movflags", "+faststart",
        "-an",
        str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    sz = out.stat().st_size // 1024
    print(f"  mp4 ok ({sz} KB)")


def encode_webm() -> None:
    out = OUT_DIR / "hero-loop.webm"
    print(f"Encoding WebM → {out}")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuv420p",
        "-b:v", "0",
        "-crf", "32",
        "-row-mt", "1",
        "-an",
        str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    sz = out.stat().st_size // 1024
    print(f"  webm ok ({sz} KB)")


def make_poster() -> None:
    """Save a single representative frame as a poster image."""
    poster_frame = TOTAL_FRAMES // 2
    img = render_frame(poster_frame)
    img.save(OUT_DIR / "hero-loop.jpg", "JPEG", quality=82, optimize=True)
    print(f"  poster ok ({(OUT_DIR / 'hero-loop.jpg').stat().st_size // 1024} KB)")


def main() -> None:
    render_all_frames()
    encode_mp4()
    encode_webm()
    make_poster()
    # Clean up frame stash
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    print("\nDone.")


if __name__ == "__main__":
    main()
