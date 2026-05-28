"""Generate localized homepages from docs/index.html using scripts/i18n-strings.json.

For each language defined in i18n-strings.json:
  1. Copy docs/index.html as the base.
  2. Swap a curated set of strings (title, meta description, hero pills,
     CTA labels, section eyebrows). Code blocks, brand names, file paths,
     stat numbers, and the terminal animation text stay in English.
  3. Set <html lang="..."> and dir="rtl" for Arabic.
  4. Inject a <link rel="alternate" hreflang="..."> for every language.
  5. Add a language picker dropdown to the nav (top-right).
  6. Mark canonical to the lang-specific URL.
  7. Write to docs/<lang>/index.html and landing/<lang>/index.html.

Re-run the script whenever docs/index.html or i18n-strings.json changes.
"""
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "docs" / "index.html"
STRINGS = ROOT / "scripts" / "i18n-strings.json"
DOCS_OUT = ROOT / "docs"
LANDING_OUT = ROOT / "landing"


def load_strings():
    with STRINGS.open(encoding="utf-8") as f:
        return json.load(f)


def base_html() -> str:
    return BASE.read_text(encoding="utf-8")


def hreflang_block(langs: dict, current: str) -> str:
    """Render <link rel="alternate" hreflang="..."> for every language + x-default."""
    lines = []
    for code in langs:
        if code == "en":
            url = "https://uxskill.laithjunaidy.com/"
        else:
            url = f"https://uxskill.laithjunaidy.com/{code}/"
        lines.append(f'  <link rel="alternate" hreflang="{code}" href="{url}">')
    lines.append('  <link rel="alternate" hreflang="x-default" href="https://uxskill.laithjunaidy.com/">')
    return "\n".join(lines)


def lang_picker_html(langs: dict, current: str, picker_label: str) -> str:
    """Tiny dropdown rendered in the nav."""
    items = []
    for code, info in langs.items():
        label = info["name"]
        href = "/" if code == "en" else f"/{code}/"
        active = " is-current" if code == current else ""
        items.append(f'      <a href="{href}" lang="{info["html_lang"]}" class="lang-picker__item{active}">{label}</a>')
    items_html = "\n".join(items)
    return f"""
    <div class="lang-picker">
      <button class="lang-picker__btn" aria-haspopup="true" aria-expanded="false" type="button" id="lang-picker-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
        <span>{langs[current]["name"]}</span>
      </button>
      <div class="lang-picker__menu" role="menu" aria-label="{picker_label}">
{items_html}
      </div>
    </div>"""


PICKER_CSS = """
    /* Language picker — dropdown in the nav */
    .lang-picker { position: relative; }
    .lang-picker__btn {
      display: inline-flex; align-items: center; gap: 8px;
      background: transparent;
      border: 1px solid var(--hairline);
      border-radius: 999px;
      color: var(--ink);
      padding: 6px 12px 6px 10px;
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: 0.06em;
      cursor: pointer;
      transition: border-color var(--t-fast) var(--ease-cinema);
    }
    .lang-picker__btn:hover, .lang-picker__btn[aria-expanded="true"] {
      border-color: var(--hairline-2);
    }
    .lang-picker__menu {
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      min-width: 220px;
      max-height: 360px;
      overflow-y: auto;
      background: rgba(15, 17, 21, 0.96);
      backdrop-filter: blur(20px);
      border: 1px solid var(--hairline);
      border-radius: 12px;
      padding: 8px;
      display: none;
      z-index: 50;
      box-shadow: 0 24px 60px -24px rgba(0,0,0,0.6);
    }
    .lang-picker.is-open .lang-picker__menu { display: block; }
    .lang-picker__item {
      display: block;
      padding: 8px 12px;
      color: var(--body);
      text-decoration: none;
      font-family: var(--sans);
      font-size: 14px;
      border-radius: 6px;
      transition: background-color var(--t-fast) var(--ease-cinema), color var(--t-fast) var(--ease-cinema);
    }
    .lang-picker__item:hover { background: rgba(255,255,255,0.06); color: var(--ink); }
    .lang-picker__item.is-current { color: var(--ink); background: rgba(255,255,255,0.04); }
    @media (max-width: 900px) {
      .lang-picker__menu { right: -16px; }
    }"""


PICKER_JS = """
  /* =========================================================================
     LANG PICKER — open/close menu, close on outside click or Esc
     ========================================================================= */
  (function setupLangPicker() {
    const picker = document.querySelector('.lang-picker');
    const btn = document.getElementById('lang-picker-btn');
    if (!picker || !btn) return;
    const open = () => { picker.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); };
    const close = () => { picker.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); };
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      picker.classList.contains('is-open') ? close() : open();
    });
    document.addEventListener('click', (e) => {
      if (!picker.contains(e.target)) close();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
    });
  })();"""


# Where to inject things in the base template.
HEAD_INSERTION_MARKER = '  <link rel="canonical"'
NAV_INSERTION_MARKER = '<header class="nav" id="nav">'
NAV_BTN_MARKER = '<button type="button" class="nav__menu-btn"'  # we'll insert the picker BEFORE the hamburger button (markup carries type="button")


def build_lang(data: dict, lang: str) -> str:
    html = base_html()
    langs = data["languages"]
    strings = data["strings"]
    info = langs[lang]

    # 1. Set <html lang> and dir
    if info["dir"] == "rtl":
        html = re.sub(r'<html lang="[^"]*">', f'<html lang="{info["html_lang"]}" dir="rtl">', html, count=1)
    else:
        html = re.sub(r'<html lang="[^"]*">', f'<html lang="{info["html_lang"]}">', html, count=1)

    # 2. Inject hreflang block right before canonical
    hreflang = hreflang_block(langs, lang)
    if "hreflang=" not in html:
        html = html.replace(HEAD_INSERTION_MARKER, hreflang + "\n" + HEAD_INSERTION_MARKER, 1)

    # 3. Update canonical URL
    canonical = "https://uxskill.laithjunaidy.com/" if lang == "en" else f"https://uxskill.laithjunaidy.com/{lang}/"
    html = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{canonical}">',
        html, count=1
    )

    # 4. Swap strings — title, description, hero pills, eyebrows, CTAs
    def tr(key: str, fallback_en_default: str) -> str:
        bag = strings.get(key, {})
        return bag.get(lang, bag.get("en", fallback_en_default))

    # <title>
    if "page_title" in strings:
        html = re.sub(r'<title>[^<]+</title>', f'<title>{tr("page_title", "")}</title>', html, count=1)

    # <meta name="description">
    if "meta_description" in strings:
        desc = tr("meta_description", "")
        html = re.sub(r'<meta name="description" content="[^"]*">',
                      f'<meta name="description" content="{desc}">', html, count=1)
        # og:description
        html = re.sub(r'<meta property="og:description" content="[^"]*">',
                      f'<meta property="og:description" content="{desc}">', html, count=1)
        html = re.sub(r'<meta name="twitter:description" content="[^"]*">',
                      f'<meta name="twitter:description" content="{desc}">', html, count=1)

    # Hero pills
    if "hero_pill_1" in strings:
        html = html.replace('v3.0.0 — THE BRAIN', tr("hero_pill_1", "v3.0.0 — THE BRAIN"), 1)
    if "hero_pill_2" in strings:
        html = html.replace('MIT, no telemetry', tr("hero_pill_2", "MIT, no telemetry"), 1)

    # GENERIC_SWAP_SENTINEL — sweep EVERY string key whose english source
    # appears in the template. Order matters; do the longest matches first so
    # short keys don't partially match inside a longer key's output.
    keys_by_length = sorted(strings.keys(), key=lambda k: -len(strings[k].get("en") or ""))
    for key in keys_by_length:
        bag = strings.get(key, {})
        en = bag.get("en")
        target = bag.get(lang, en)
        if not en or not target or en == target:
            continue
        if en in html:
            # Swap ALL occurrences so the same English phrase that appears in
            # twitter:title, og:title, hero h1, and footer tagline all become
            # translated. Without this, only the first occurrence swapped.
            html = html.replace(en, target)

    # Hero h1 — the English markup splits the sentence across <br> + an accent
    # span, so the per-key generic swap can't translate the second clause (the
    # hero_h1_line3 key's en never matches the split markup, leaving "design
    # that doesn't look generated." in English on every locale). Rebuild the
    # whole h1 inner per locale from the three line keys. English keeps its
    # hand-tuned 3-line markup untouched.
    if lang != "en":
        l1 = tr("hero_h1_line1", "The brain")
        l2 = tr("hero_h1_line2", "that ships")
        l3 = tr("hero_h1_line3", "design that&nbsp;doesn&rsquo;t look generated.")
        new_h1 = (
            '<h1 class="hero__h1" id="hero-h1">\n'
            f'          {l1} {l2}<br>\n'
            f'          <span class="accent-italic">{l3}</span>\n'
            '        </h1>'
        )
        html = re.sub(
            r'<h1 class="hero__h1" id="hero-h1">.*?</h1>',
            lambda _m: new_h1, html, count=1, flags=re.DOTALL,
        )

    # Section eyebrows
    for key, original in [
        ("section_02_eyebrow", "02 — Brand specs · 160 catalogue · growing"),
        ("section_03_eyebrow", "03 — The reasoning engine"),
        ("section_04_eyebrow", "04 — The anti-slop linter"),
    ]:
        if key in strings:
            html = html.replace(original, tr(key, original), 1)

    # CTAs (hero)
    if "cta_install" in strings:
        html = html.replace('            pip install uxskill\n          </a>',
                            f'            {tr("cta_install", "pip install uxskill")}\n          </a>', 1)
    # Hero secondary CTA — "See it work" replaced the old "Read the source"
    # (cta_source) but no key tracked it, so it stayed English on every locale.
    if "cta_see_it_work" in strings:
        html = html.replace('            See it work\n          </a>',
                            f'            {tr("cta_see_it_work", "See it work")}\n          </a>', 1)

    # 5. Inject lang-picker CSS + nav element + picker JS
    picker_label = tr("lang_picker_label", "Language")
    picker_html = lang_picker_html(langs, lang, picker_label)

    # CSS: add before the closing </style> in the LAST big style block (the page styles).
    # The hero canvas style block is around the top; the nav styles end mid-file.
    # Simpler: just append a new <style> right before </head>.
    if "lang-picker__btn {" not in html:
        html = html.replace('</head>', f'<style>{PICKER_CSS}</style>\n</head>', 1)

    # Picker in the nav — insert before the hamburger button.
    # docs/index.html doubles as BOTH the source template and the en output, and
    # base_html() re-reads it each iteration — so the en pass (first in the dict)
    # bakes its own picker into the base, and every later locale would inherit
    # en's picker via a naive "if not present" guard. Strip any existing picker
    # first, then inject the locale-correct one. Idempotent across run count and
    # language order.
    html = re.sub(
        r'\s*<div class="lang-picker">.*?(?=' + re.escape(NAV_BTN_MARKER) + ')',
        '', html, count=1, flags=re.DOTALL)
    html = html.replace(NAV_BTN_MARKER, picker_html + "\n    " + NAV_BTN_MARKER, 1)

    # Picker JS — append before the closing </script> of the homepage's main script.
    # Find the last </script> and inject right before.
    if "setupLangPicker" not in html:
        last_script_close = html.rfind('</script>')
        if last_script_close != -1:
            html = html[:last_script_close] + PICKER_JS + "\n" + html[last_script_close:]

    return html


def write_lang(html: str, lang: str) -> None:
    if lang == "en":
        # English IS the root index.html — we keep the root file as-is and just
        # rewrite it with hreflang + lang picker added.
        out_docs = DOCS_OUT / "index.html"
        out_landing = LANDING_OUT / "index.html"
    else:
        sub_docs = DOCS_OUT / lang
        sub_landing = LANDING_OUT / lang
        sub_docs.mkdir(parents=True, exist_ok=True)
        sub_landing.mkdir(parents=True, exist_ok=True)
        out_docs = sub_docs / "index.html"
        out_landing = sub_landing / "index.html"
    out_docs.write_text(html, encoding="utf-8")
    out_landing.write_text(html, encoding="utf-8")


def main() -> None:
    data = load_strings()
    langs = data["languages"]
    print(f"Building i18n homepages for {len(langs)} languages\n")
    for lang in langs:
        html = build_lang(data, lang)
        write_lang(html, lang)
        size_kb = len(html) // 1024
        print(f"  ok  {lang:6}  →  /{lang if lang != 'en' else ''}/  ({size_kb} KB)")
    print(f"\nDone. {len(langs)} locales written under docs/ + landing/.")


if __name__ == "__main__":
    main()
