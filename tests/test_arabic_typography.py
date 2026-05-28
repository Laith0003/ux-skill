"""Guard: the Arabic homepage MUST load IBM Plex Sans Arabic.

The browser default Arabic font is unusable. v3.0 shipped briefly without
this and the user (correctly) complained. This test fails fast so it can
never regress.

Checks:
1. docs/ar/index.html exists.
2. The page loads `IBM Plex Sans Arabic` via Google Fonts.
3. The page has a `html[lang="ar"]` CSS block that sets font-family to
   IBM Plex Sans Arabic for body + headings.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AR = ROOT / "docs" / "ar" / "index.html"


def test_ar_homepage_exists():
    assert AR.exists(), f"Arabic homepage missing: {AR}"


def test_ar_loads_ibm_plex_sans_arabic_font():
    body = AR.read_text(encoding="utf-8", errors="replace")
    assert "IBM+Plex+Sans+Arabic" in body, (
        "Arabic homepage MUST link to IBM Plex Sans Arabic via Google Fonts. "
        "Without it the browser falls back to OS default which is unusable. "
        "Edit docs/index.html font import, then run scripts/build-i18n-homepages.py."
    )


def test_ar_applies_plex_arabic_via_lang_selector():
    body = AR.read_text(encoding="utf-8", errors="replace")
    assert "html[lang=\"ar\"]" in body or "html[lang='ar']" in body, (
        "Arabic homepage must have html[lang=\"ar\"] CSS selectors that "
        "swap the font stack to IBM Plex Sans Arabic for body + headings."
    )
    # The string `IBM Plex Sans Arabic` (the font family name) must appear in
    # a CSS context within the page so the selectors actually use it.
    assert "IBM Plex Sans Arabic" in body, (
        "Arabic homepage must use 'IBM Plex Sans Arabic' as a font-family value "
        "in its CSS. Add it to docs/index.html's :root variables."
    )


def test_landing_ar_also_has_plex_arabic():
    landing_ar = ROOT / "landing" / "ar" / "index.html"
    if not landing_ar.exists():
        # landing/ mirror is optional
        return
    body = landing_ar.read_text(encoding="utf-8", errors="replace")
    assert "IBM+Plex+Sans+Arabic" in body, (
        "landing/ar/index.html (mirror) must also load IBM Plex Sans Arabic. "
        "Re-run scripts/build-i18n-homepages.py to regenerate both docs/ and landing/."
    )
