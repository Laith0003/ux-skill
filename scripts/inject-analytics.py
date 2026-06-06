"""Inject the Google Analytics 4 gtag.js tag into every page's <head>.

Measurement ID G-Z371T0DBW5 — property "Organization" (256942753), web stream
"uxskill website" → https://uxskill.laithjunaidy.com. Enhanced Measurement is ON
at the GA side (page_view, scroll, outbound click, site search, file download,
form interaction, video), so the standard tag below is all the page needs.

Walks docs/ for *.html and inserts the tag immediately after the
opening <head> on every page that doesn't already carry the Measurement ID.
Idempotent — the ID guard means re-runs are safe, and locale homepages that the
i18n build regenerates from docs/index.html inherit it from the base.

Re-run after adding new HTML pages.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEASUREMENT_ID = "G-Z371T0DBW5"

TAG = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z371T0DBW5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-Z371T0DBW5');
</script>"""


def inject(html: str) -> str | None:
    if MEASUREMENT_ID in html:
        return None  # already tagged
    idx = html.find("<head>")
    if idx == -1:
        return None  # no head — skip (shouldn't happen for our pages)
    cut = idx + len("<head>")
    return html[:cut] + TAG + html[cut:]


def main() -> None:
    written = skipped = nohead = 0
    targets = []
    for base in ("docs",):
        d = ROOT / base
        if d.exists():
            targets.extend(sorted(d.rglob("*.html")))
    for path in targets:
        html = path.read_text(encoding="utf-8")
        out = inject(html)
        if out is None:
            if MEASUREMENT_ID in html:
                skipped += 1
            else:
                nohead += 1
            continue
        path.write_text(out, encoding="utf-8")
        written += 1
    print(f"  tagged:        {written}")
    print(f"  already had:   {skipped}")
    print(f"  no <head>:     {nohead}")
    print(f"  total scanned: {len(targets)}")


if __name__ == "__main__":
    main()
