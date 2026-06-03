"""Guard against English copy leaking into localized homepages.

The i18n build is a verbatim string-swap: a key only translates if its `en`
source matches the markup byte-for-byte. When the homepage markup changes
(hero h1 restructured, a CTA renamed) but the matching key isn't updated, the
English silently survives on all 16 locale pages. This has regressed more than
once (the hero h1 second clause "design that doesn't look generated." and the
"See it work" CTA both leaked).

These tests assert specific high-visibility UI strings are NOT present in
localized pages. They are intentionally targeted (not a broad English scan) so
they don't false-positive on legitimately-English content: brand names
(Stripe, Ferrari), the canonical 7-axis identifiers (warmth, contrast, ...),
mode identifiers (strict_brand), code, or the slop-example terms named inside
translated prose (John Doe, Lorem ipsum).

If one fails: a homepage string changed without its scripts/i18n-strings.json
key being updated. Fix the key (or the build's hero-h1 / CTA handling), then
re-run scripts/build-i18n-homepages.py.
"""
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent

# All 16 localized homepages are checked — the v3.1 build is uniform, but a
# wide net catches a single locale that silently fell back to English.
LOCALES = ["ar", "de", "es", "fr", "hi", "id", "it", "ja", "ko", "pt-BR",
           "ru", "th", "tr", "vi", "zh-CN", "zh-TW"]

# Distinctive v3.1 homepage BODY copy that must be translated on every locale
# (verbatim English here = an untranslated section = a leak). Nav/CTA terms a
# translator may legitimately keep in English (e.g. "Star on GitHub", "Showcase")
# are deliberately NOT listed — these strings are prose with no reason to stay English.
MUST_NOT_LEAK = [
    "Your AI ships",                      # enemy section h2
    "What if the model had a",            # the turn
    "Runs where you already build",       # runs section kicker
    "Why this is the floor",              # moat eyebrow
    "The corpus is vocabulary",           # proof kicker
    "Same brief, same system",            # moat card 1 body
    "as words, not stamps",               # proof h3
    "One sequence, not scattered cards",  # how-it-works eyebrow
    "Ask any model to",                   # enemy sub
]


@pytest.mark.parametrize("locale", LOCALES)
def test_homepage_has_no_english_ui_leaks(locale):
    page = ROOT / "docs" / locale / "index.html"
    assert page.exists(), f"localized homepage missing: {page}"
    html = page.read_text(encoding="utf-8")
    leaked = [s for s in MUST_NOT_LEAK if s in html]
    assert not leaked, (
        f"English UI copy leaked into docs/{locale}/index.html: {leaked}. "
        "A homepage string changed without updating its i18n key. Fix the key "
        "in scripts/i18n-strings.json (or the build's hero-h1 / CTA handling) "
        "and re-run scripts/build-i18n-homepages.py."
    )


def test_english_homepage_keeps_its_copy():
    """Sanity: the English source page must keep real homepage copy. The v3.1
    redesign replaced the old hero CTA ("See it work"), so assert two stable
    current strings: the tagline and the centroid concept."""
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Stop your AI code looking generated" in html
    assert "the centroid" in html
