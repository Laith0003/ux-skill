"""Inject a tiny universal stylesheet into every HTML file that bans
horizontal scroll on mobile (and everywhere).

Idempotent: pages already carrying the `<!-- noscroll-fix -->` sentinel
are skipped. Re-runs are safe.

Applies to:
  docs/**/*.html
  landing/**/*.html
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent

SENTINEL = "<!-- noscroll-fix -->"
INJECTION = f"""{SENTINEL}
  <style>
    /* Never allow horizontal scroll on mobile. The body sets overflow-x: clip
       and max-width: 100%; carousels that need their own horizontal scroll
       (e.g. .brand-rail) opt in by setting overflow-x: auto on themselves —
       overflow-x:clip on the parent does NOT prevent inner overflow scrolling. */
    html, body {{
      overflow-x: clip;
      max-width: 100%;
    }}
    /* Defensive — make sure no section, image, or table forces width >100%. */
    section, header, footer, main, article {{ max-width: 100vw; }}
    img, video, canvas, svg, iframe {{ max-width: 100%; height: auto; }}
    table {{ max-width: 100%; }}
  </style>"""


def inject(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if SENTINEL in text:
        return False, "already injected"
    if "</head>" not in text:
        return False, "no </head>"
    new = text.replace("</head>", f"  {INJECTION}\n</head>", 1)
    path.write_text(new, encoding="utf-8")
    return True, "injected"


def main() -> None:
    count_ok = 0
    count_skip = 0
    for root_dir in (ROOT / "docs", ROOT / "landing"):
        for p in root_dir.rglob("*.html"):
            ok, msg = inject(p)
            rel = p.relative_to(ROOT)
            if ok:
                print(f"ok   {rel}")
                count_ok += 1
            else:
                count_skip += 1
    print(f"\nDone. injected: {count_ok}, skipped: {count_skip}")


if __name__ == "__main__":
    main()
