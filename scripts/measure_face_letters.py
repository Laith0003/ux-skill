"""Measure each face's letters and a set of headline words, the space left out.

Metrics.latin_avg weighs the space in with English letter frequencies, as a
line of running text does, and that is what a measure needs. A headline
word has no space, so the display fit reads letter advances instead. This
script loads every face in engine.foundations.fonts.FACES from Google Fonts,
sets each letter and each headline word in a headless browser at MEASURE_PX
(a display size, so a face with an optical size axis draws its display
cut) and at MEASURE_WEIGHT, the heaviest weight a display takes
(character.display_weight), within the face's range, and writes
tests/foundations/data/face_word_widths.json:

- per Latin face, the advance of a to z and A to Z and the width of every
  word in WORDS and HELD_OUT, in em;
- per Arabic face, the isolated advance of the 28 letters (a record only:
  joined letters take other forms) and the width of every word in
  ARABIC_WORDS, in em.

From that file tests/foundations/test_display_fit_words.py recomputes
Metrics.latin_letters and latin_capitals and typography.LETTER_WIDTHS, and
checks the fit against every word. WORD_SLACK is chosen on WORDS and
ARABIC_SLACK on ARABIC_WORDS; HELD_OUT checks the Latin fit on words the
slack was not chosen on, capitals included. The script prints the values to
paste. Run it when a face is added:

    python scripts/measure_face_letters.py

It needs network access and Playwright with Chromium; the engine never
runs it.
"""
from __future__ import annotations

import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.foundations import fonts  # noqa: E402
from engine.foundations.typography import LETTER_FREQ  # noqa: E402

MEASURE_PX = 40
MEASURE_WEIGHT = 650
LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = LOWER.upper()
# The 28 letters of the Arabic alphabet.
ARABIC = "".join(chr(c) for c in (
    0x0627, 0x0628, 0x062A, 0x062B, 0x062C, 0x062D, 0x062E, 0x062F, 0x0630, 0x0631,
    0x0632, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 0x0638, 0x0639, 0x063A, 0x0641,
    0x0642, 0x0643, 0x0644, 0x0645, 0x0646, 0x0647, 0x0648, 0x064A))
# Headline words of 6 to 13 letters, capitalized as a headline sets them,
# wide letters included.
WORDS = ("Houseplants", "Delivered", "Perimeter", "Anomaly", "Intelligence", "Revenue",
         "Bookings", "Customers", "Minimum", "Wellness", "Collaboration", "International",
         "Neighbourhood", "Membership", "Warehouse", "Momentum")
# Words the slack is not chosen on: wide letters, capitals and short words.
HELD_OUT = ("Workflow", "Mammoth", "Swimwear", "Homework", "Maximum", "Wholesome",
            "Showroom", "Somewhere", "Memorable", "Welcome", "MOMENTUM", "WAREHOUSE",
            "NEIGHBOURHOOD", "Wow", "Mum", "Overwhelm")
# Arabic headline words of 4 to 11 letters (delivery, community, investment,
# hospital, garden, technology, sales, customers, safety, plants, the
# neighbourhood, international, experiences, subscriptions).
ARABIC_WORDS = (
    "\u0627\u0644\u062a\u0648\u0635\u064a\u0644",
    "\u0627\u0644\u0645\u062c\u062a\u0645\u0639",
    "\u0627\u0644\u0627\u0633\u062a\u062b\u0645\u0627\u0631",
    "\u0645\u0633\u062a\u0634\u0641\u0649",
    "\u0627\u0644\u062d\u062f\u064a\u0642\u0629",
    "\u0627\u0644\u062a\u0643\u0646\u0648\u0644\u0648\u062c\u064a\u0627",
    "\u0627\u0644\u0645\u0628\u064a\u0639\u0627\u062a",
    "\u0627\u0644\u0639\u0645\u0644\u0627\u0621",
    "\u0627\u0644\u0623\u0645\u0627\u0646",
    "\u0627\u0644\u0646\u0628\u0627\u062a\u0627\u062a",
    "\u0627\u0644\u062d\u064a",
    "\u0627\u0644\u062f\u0648\u0644\u064a\u0629",
    "\u062a\u062c\u0627\u0631\u0628",
    "\u0627\u0634\u062a\u0631\u0627\u0643\u0627\u062a")
FIXTURE = ROOT / "tests" / "foundations" / "data" / "face_word_widths.json"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36")


def weighted(letters) -> float:
    """A face's lowercase advance weighted by English letter frequency, in em."""
    return sum(letters[c] * f for c, f in zip(LOWER, LETTER_FREQ)) / sum(LETTER_FREQ)


def capitals(letters) -> float:
    """A face's capital advance, A to Z weighted as a to z are, in em."""
    return sum(letters[c.upper()] * f for c, f in zip(LOWER, LETTER_FREQ)) / sum(LETTER_FREQ)


def letter_widths(fixture) -> dict:
    """Each letter's share of its face's weighted lowercase advance over the
    proportional Latin faces, rounded up to a hundredth: the average share
    for a lowercase letter and the widest for a capital, since capitals
    differ far more between faces."""
    faces = [f for f in fonts.FACES if f.role in ("text", "display")]
    out = {}
    for c in LOWER + UPPER:
        shares = [fixture["faces"][f.family]["letters"][c]
                  / weighted(fixture["faces"][f.family]["letters"]) for f in faces]
        share = sum(shares) / len(shares) if c in LOWER else max(shares)
        out[c] = math.ceil(round(share * 100, 6)) / 100
    return out


def _font_file(face: fonts.Face, out: pathlib.Path) -> pathlib.Path:
    lo, hi = face.weights
    axis = f":wght@{lo}..{hi}" if face.variable else f":wght@{face.clamp(MEASURE_WEIGHT)}"
    css = subprocess.run(["curl", "-sL", "-m", "20", "-A", UA,
                          "https://fonts.googleapis.com/css2?family="
                          + face.family.replace(" ", "+") + axis],
                         capture_output=True, text=True, check=True).stdout
    subset = "arabic" if face.role == "arabic" else "latin"
    url = re.search(r"/\* " + subset + r" \*/\s*@font-face\s*{[^}]*?url\((https://[^)]+\.woff2)\)",
                    css)
    if not url:
        raise SystemExit(f"{face.family}: no {subset} file in the Google Fonts CSS; check the "
                         "family name in fonts.FACES")
    path = out / (re.sub(r"\W+", "-", face.family.lower()) + ".woff2")
    subprocess.run(["curl", "-sL", "-m", "20", "-o", str(path), url.group(1)], check=True)
    return path


def _spans(i: int, face: fonts.Face, texts) -> str:
    style = (f"font-family:F{i};font-size:{MEASURE_PX}px;"
             f"font-weight:{face.clamp(MEASURE_WEIGHT)};white-space:pre;"
             "font-optical-sizing:auto")
    return "".join(f'<span class="f{i}" style="{style}">{t}</span>' for t in texts)


def main() -> None:
    from playwright.sync_api import sync_playwright
    faces = list(fonts.FACES)
    texts = {f.family: (list(ARABIC) + list(ARABIC_WORDS) if f.role == "arabic"
                        else list(LOWER + UPPER) + list(WORDS) + list(HELD_OUT))
             for f in faces}
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp)
        rules, rows = [], []
        for i, face in enumerate(faces):
            path = _font_file(face, out)
            rules.append(f'@font-face{{font-family:"F{i}";src:url("{path.as_uri()}");'
                         'font-weight:100 1000}')
            rows.append(_spans(i, face, texts[face.family]))
        page = out / "letters.html"
        page.write_text(f"<!doctype html><meta charset=utf-8><style>{''.join(rules)}</style>"
                        + "".join(f"<div>{r}</div>" for r in rows), encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            tab = browser.new_page()
            tab.goto(page.as_uri())
            tab.evaluate("document.fonts.ready.then(() => true)")
            loaded = tab.evaluate("() => [...document.fonts].map(f => [f.family, f.status])")
            missing = [name for name, status in loaded if status != "loaded"]
            if missing or len(loaded) != len(faces):
                raise SystemExit(f"{len(missing)} faces did not load ({', '.join(missing)}), so "
                                 "they would measure the fallback; check the network and run "
                                 "again")
            widths = tab.evaluate("""() => { const o = {};
              for (const s of document.querySelectorAll('span'))
                (o[s.className] = o[s.className] || []).push(s.getBoundingClientRect().width);
              return o; }""")
            browser.close()
    fixture = {"measure": {"px": MEASURE_PX, "weight": MEASURE_WEIGHT}, "faces": {}}
    for i, face in enumerate(faces):
        named = dict(zip(texts[face.family],
                         (round(w / MEASURE_PX, 4) for w in widths[f"f{i}"])))
        if face.role == "arabic":
            entry = {"letters": {c: named[c] for c in ARABIC},
                     "words": {w: named[w] for w in ARABIC_WORDS}}
        else:
            entry = {"letters": {c: named[c] for c in LOWER + UPPER},
                     "words": {w: named[w] for w in WORDS},
                     "held_out": {w: named[w] for w in HELD_OUT}}
        fixture["faces"][face.family] = entry
    for face in faces:
        letters = fixture["faces"][face.family]["letters"]
        if face.role == "arabic":
            # Joined Arabic letters take other forms than isolated ones, so
            # the fit sets an Arabic word at arabic_avg with ARABIC_SLACK,
            # checked against the measured words; the isolated advances are
            # recorded as evidence only.
            continue
        print(f"{face.family}: latin_letters {weighted(letters) * face.metrics.upm:.1f}, "
              f"latin_capitals {capitals(letters) * face.metrics.upm:.1f}")
    print("LETTER_WIDTHS", letter_widths(fixture))
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(fixture, indent=1, sort_keys=True, ensure_ascii=True) + "\n",
                       encoding="ascii")
    print(f"wrote {FIXTURE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
