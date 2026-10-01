"""Measure each face's average letter advance, the space left out.

Metrics.latin_avg weighs the space in with English letter frequencies, as a
line of running text does, and that is what a measure needs. A headline
word has no spaces, so fitting one with latin_avg sets it too large. This
script loads each Latin face in engine.foundations.fonts.FACES from Google
Fonts at weight 400, measures a to z in a headless browser, and prints each
face's frequency-weighted letter advance in font units, for
Metrics.latin_letters. With --words it also writes the width in em of each
word in WORDS per face to tests/foundations/data/face_word_widths.json, the
fixture the fit is checked against. Run it when a face is added:

    python scripts/measure_face_letters.py --words

It needs network access and Playwright with Chromium; the engine never
runs it.
"""
from __future__ import annotations

import math
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.foundations import fonts  # noqa: E402

# English letter frequencies in percent, a to z.
FREQ = (8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772,
        4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978,
        2.360, 0.150, 1.974, 0.074)
# Headline words of 6 to 13 letters, capitalized as a headline sets them,
# wide letters included.
WORDS = ("Houseplants", "Delivered", "Perimeter", "Anomaly", "Intelligence", "Revenue",
         "Bookings", "Customers", "Minimum", "Wellness", "Collaboration", "International",
         "Neighbourhood", "Membership", "Warehouse", "Momentum")
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
FIXTURE = ROOT / "tests" / "foundations" / "data" / "face_word_widths.json"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"


def _font_file(face: fonts.Face, out: pathlib.Path) -> pathlib.Path:
    lo, hi = face.weights
    axis = f":wght@{lo}..{hi}" if face.variable else ":wght@400"
    css = subprocess.run(["curl", "-sL", "-m", "20", "-A", UA,
                          "https://fonts.googleapis.com/css2?family="
                          + face.family.replace(" ", "+") + axis],
                         capture_output=True, text=True, check=True).stdout
    url = re.search(r"/\* latin \*/\s*@font-face\s*{[^}]*?url\((https://[^)]+\.woff2)\)", css)
    if not url:
        raise SystemExit(f"{face.family}: no Latin file in the Google Fonts CSS; check the family name")
    path = out / (re.sub(r"\W+", "-", face.family.lower()) + ".woff2")
    subprocess.run(["curl", "-sL", "-m", "20", "-o", str(path), url.group(1)], check=True)
    return path


def main() -> None:
    from playwright.sync_api import sync_playwright
    latin = [f for f in fonts.FACES if f.role != "arabic"]
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp)
        rules, rows = [], []
        for i, face in enumerate(latin):
            path = _font_file(face, out)
            rules.append(f'@font-face{{font-family:"F{i}";src:url("{path.as_uri()}");'
                         'font-weight:100 900}')
            rows.append("".join(f'<span class="f{i}" style="font-family:F{i};font-size:1000px;'
                                f'font-weight:400;white-space:pre">{c}</span>'
                                for c in LETTERS)
                        + "".join(f'<span class="w{i}" style="font-family:F{i};font-size:1000px;'
                                  f'font-weight:400;white-space:pre">{w}</span>' for w in WORDS))
        page = out / "letters.html"
        page.write_text(f"<!doctype html><style>{''.join(rules)}</style>"
                        + "".join(f"<div>{r}</div>" for r in rows), encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            tab = browser.new_page()
            tab.goto(page.as_uri())
            tab.wait_for_timeout(1500)
            widths = tab.evaluate("""() => { const o = {};
              for (const s of document.querySelectorAll('span'))
                (o[s.className] = o[s.className] || []).push(s.getBoundingClientRect().width);
              return o; }""")
            browser.close()
    fixture = {}
    share = {c: 0.0 for c in LETTERS}
    for i, face in enumerate(latin):
        w = widths[f"f{i}"]
        em = sum(x * f for x, f in zip(w, FREQ)) / sum(FREQ) / 1000
        print(f"{face.family}: {em * face.metrics.upm:.1f}")
        fixture[face.family] = {word: round(x / 1000, 4) for word, x in zip(WORDS, widths[f"w{i}"])}
        if face.role != "mono":
            for c, x in zip(LETTERS, w):
                share[c] = max(share[c], x / 1000 / em)
    # Each letter's widest share of its face's letter advance over the
    # proportional faces, rounded up: typography.LETTER_WIDTHS.
    print({c: math.ceil(v * 100) / 100 for c, v in share.items()})
    if "--words" in sys.argv:
        import json
        FIXTURE.parent.mkdir(parents=True, exist_ok=True)
        FIXTURE.write_text(json.dumps(fixture, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {FIXTURE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
