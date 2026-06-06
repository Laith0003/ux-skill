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
  7. Write to docs/<lang>/index.html.

Re-run the script whenever docs/index.html or i18n-strings.json changes.
"""
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "docs" / "index.html"
STRINGS = ROOT / "scripts" / "i18n-strings.json"
DOCS_OUT = ROOT / "docs"


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

    # 1b. Arabic needs a real Arabic webfont — the browser default Arabic face is
    #     unusable (v3.0 shipped without it and the user complained). Load IBM
    #     Plex Sans Arabic and apply it to body + headings under html[lang="ar"].
    if lang == "ar":
        html = html.replace("&display=swap",
            "&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap", 1)
        ar_css = (
            "<style>"
            "html[lang=\"ar\"] body{font-family:'IBM Plex Sans Arabic','Inter',system-ui,sans-serif}"
            "html[lang=\"ar\"] h1,html[lang=\"ar\"] h2,html[lang=\"ar\"] h3,"
            "html[lang=\"ar\"] .lead,html[lang=\"ar\"] .lede,html[lang=\"ar\"] .sub,"
            "html[lang=\"ar\"] .turn-lead,html[lang=\"ar\"] .turn-sub,"
            "html[lang=\"ar\"] .pbeat-title,html[lang=\"ar\"] .pbeat-sub,"
            "html[lang=\"ar\"] .k,html[lang=\"ar\"] .eyebrow,html[lang=\"ar\"] .bub,html[lang=\"ar\"] .pill"
            "{font-family:'IBM Plex Sans Arabic','Bricolage Grotesque',sans-serif}"
            "</style>")
        html = html.replace("</head>", ar_css + "\n</head>", 1)

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

    # 3b. og:url -> the locale URL; add og:locale (Facebook locale form)
    html = re.sub(r'<meta property="og:url" content="[^"]*">',
                  f'<meta property="og:url" content="{canonical}">', html, count=1)
    OG_LOCALE = {"en": "en_US", "de": "de_DE", "es": "es_ES", "fr": "fr_FR",
                 "it": "it_IT", "pt-BR": "pt_BR", "ru": "ru_RU", "tr": "tr_TR",
                 "zh-CN": "zh_CN", "zh-TW": "zh_TW", "ja": "ja_JP", "ko": "ko_KR",
                 "hi": "hi_IN", "id": "id_ID", "vi": "vi_VN", "th": "th_TH", "ar": "ar_AR"}
    ogl = OG_LOCALE.get(lang, "en_US")
    if 'property="og:locale"' not in html:
        html = re.sub(r'(<meta property="og:url" content="[^"]*">)',
                      rf'\1\n<meta property="og:locale" content="{ogl}">', html, count=1)

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

    # (v3.1: hero pills are handled by the generic full-phrase swap below.)

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

    # (v3.1: the hero h1, section eyebrows, and hero CTAs are all single-phrase
    #  markup now, so the generic full-phrase swap above handles them. The old
    #  hand-tuned 3-line h1 rebuild + hardcoded pill/eyebrow/CTA replacements
    #  were keyed to retired markup and have been removed.)

    # 5. (v3.1: the homepage ships its own .usknav__langs globe picker with
    #  absolute /<locale>/ hrefs that resolve correctly from every page, so no
    #  picker injection is needed. The old .lang-picker CSS/HTML/JS injection
    #  was keyed to retired markup and has been removed.)

    return html


def write_lang(html: str, lang: str) -> None:
    if lang == "en":
        # English IS the root index.html — we keep the root file as-is and just
        # rewrite it with hreflang + lang picker added.
        out_docs = DOCS_OUT / "index.html"
    else:
        sub_docs = DOCS_OUT / lang
        sub_docs.mkdir(parents=True, exist_ok=True)
        out_docs = sub_docs / "index.html"
    out_docs.write_text(html, encoding="utf-8")


def main() -> None:
    data = load_strings()
    langs = data["languages"]
    print(f"Building i18n homepages for {len(langs)} languages\n")
    for lang in langs:
        if lang == "en":
            continue  # the root docs/index.html IS the English source — never rewrite it
        html = build_lang(data, lang)
        write_lang(html, lang)
        size_kb = len(html) // 1024
        print(f"  ok  {lang:6}  →  /{lang}/  ({size_kb} KB)")
    print(f"\nDone. {len(langs)} locales written under docs/.")


if __name__ == "__main__":
    main()
