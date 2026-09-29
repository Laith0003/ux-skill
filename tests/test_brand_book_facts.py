"""The brand step reads the brand's own material and assumes nothing.

Two builds inside existing systems showed the brand gate passing "imagery" on
a logo alone, the language written as "en" beside a right-to-left product, a
photography mood made of voice words, and a brand book's positioning left
unread. These tests pin the fixes with an invented brand, Northfield.
"""
from __future__ import annotations

import pytest

from engine.brand import (
    build_profile,
    image_search_terms,
    parse_brand_md,
    render_md,
    score_imagery,
    stock_allowed,
)
from engine.brand.extract import BrandProfile

LOGO = "img/northfield-mark.svg"


def _page(body: str) -> str:
    return "<!doctype html><html><head><title>Northfield</title></head><body>" + body + "</body></html>"


# ------------------------------------------------------------- imagery is not the logo


@pytest.mark.parametrize("body", [
    # The logo file, sized like a picture.
    f'<header><img src="{LOGO}" width="240" height="64" alt="Northfield"></header><main><h1>Hi</h1></main>',
    # An element marked as the logo.
    '<header><img class="site-logo" src="img/mark.png" width="240" height="64" alt=""></header>',
    # An inline SVG wordmark inside the home link, large enough to pass as art.
    '<header><a href="/"><svg viewBox="0 0 240 64"><path d="M0 0h240v64H0z"/></svg></a></header>',
    # An inline SVG whose own title says it is the logo.
    '<main><svg viewBox="0 0 300 120"><title>Northfield logo</title><path d="M0 0z"/></svg></main>',
    # A row of customer logos is identity too.
    ('<section class="client-logos"><img src="img/a.png" width="160" height="60" alt="A">'
     '<img src="img/b.png" width="160" height="60" alt="B"></section>'),
    # A logo painted as a background image.
    '<div style="background:url(img/northfield-logo.png) no-repeat"></div>',
])
def test_a_page_whose_only_picture_is_a_logo_has_no_imagery(body):
    res = score_imagery(_page(body), logo_url=LOGO)
    assert res["ok"] is False, res
    assert res["kind"] in ("logo-only", "none"), res


def test_the_logo_only_detail_names_the_fix():
    res = score_imagery(_page(f'<header><img src="{LOGO}" alt="Northfield"></header>'), logo_url=LOGO)
    assert res["kind"] == "logo-only"
    assert "logo" in res["detail"] and "product screens" in res["detail"]


@pytest.mark.parametrize("body", [
    (f'<header><img src="{LOGO}" alt="Northfield"></header>'
     '<main><img src="img/orders-screen.png" width="800" height="500" alt="The orders screen"></main>'),
    ('<header><a href="/"><svg viewBox="0 0 240 64"><path d="M0 0z"/></svg></a></header>'
     '<main><svg viewBox="0 0 640 400"><path d="M0 0z"/></svg></main>'),
    ('<header><a href="/" class="brand">Northfield</a></header>'
     '<main><a href="/"><img src="img/team-at-work.jpg" alt="The team at work"></a></main>'),
])
def test_the_brands_own_pictures_beside_the_logo_count(body):
    assert score_imagery(_page(body), logo_url=LOGO)["ok"] is True


def test_the_gate_fails_a_logo_only_page():
    from engine.evaluator import evaluate
    profile = BrandProfile(name="Northfield", primary="#0B6E4F", logo={"url": LOGO, "alt": "Northfield"})
    html = _page(f'<header><img src="{LOGO}" alt="Northfield"></header>'
                 '<main><h1>Northfield</h1><a style="background:#0B6E4F" href="#go">Go</a></main>')
    ev = evaluate(html=html, brand_profile=profile)
    assert ev.brand_passed is False
    assert any("imagery" in n and "logo" in n for n in ev.notes)


# ------------------------------------------------------------- language


def test_the_language_is_never_assumed():
    p = build_profile({"name": "Northfield"})
    assert p.language == ""
    note = next(n for n in p.notes if n.startswith("Language"))
    assert "templates" in note and "html lang" in note and "language" in note
    md = render_md(p)
    assert "language: und" in md
    assert parse_brand_md(md).language == ""


def test_a_stated_language_is_kept():
    assert build_profile({"language": "ar"}).language == "ar"
    assert build_profile({"declared": {"languages": ["ar", "en"]}}).language == "ar"


# ------------------------------------------------------------- photography and strategy


def test_a_photography_mood_is_never_made_of_voice_words():
    p = build_profile({"voice": "warm, plain, witty", "logo_type_style": "rounded friendly sans"})
    assert p.photography["mood"] == []
    assert "Mood:** (not extracted" in render_md(p)


def test_the_brand_books_photography_words_are_kept():
    p = build_profile({"photography": {"mood": ["daylight", "unposed"], "avoid": ["stock photography"]}})
    assert p.photography["mood"] == ["daylight", "unposed"]
    assert parse_brand_md(render_md(p)).photography["mood"] == ["daylight", "unposed"]


def test_strategy_is_read_from_the_brand_book_and_round_trips():
    signals = {"name": "Northfield", "strategy": {
        "positioning": "The ordering app independent grocers run their week on.",
        "personality": ["calm", "exact", "neighbourly"],
        "guardrails": "No discounts shouted in red; no stock photos of smiling shoppers."}}
    p = build_profile(signals)
    assert p.strategy["positioning"].startswith("The ordering app")
    assert p.strategy["personality"] == "calm; exact; neighbourly"
    assert "promise" not in p.strategy
    md = render_md(p)
    positioning = md[md.index("### Positioning"):md.index("### Personality")]
    assert "independent grocers" in positioning
    assert "(not extracted" in md[md.index("### Promise"):md.index("### Guardrails")]
    assert parse_brand_md(md).strategy == p.strategy


def test_nothing_in_the_strategy_is_guessed_from_the_voice():
    p = build_profile({"voice": "positioned as the calm choice, personality: bold"})
    assert p.strategy == {}


# ------------------------------------------------------------- stock


def test_a_brand_that_bans_stock_gets_no_stock_search_terms():
    p = build_profile({"photography": {"avoid": ["stock photography", "lifestyle scenes"]}})
    assert stock_allowed(p) is False
    assert image_search_terms(p) == []


def test_the_default_avoid_line_still_allows_curated_stock():
    p = parse_brand_md(render_md(build_profile({"name": "Northfield"})))
    assert stock_allowed(p) is True
    assert image_search_terms(p)
