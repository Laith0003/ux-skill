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
    photo_exclusions,
    photography_forbidden,
    photography_rule,
    render_md,
    score_imagery,
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


@pytest.mark.parametrize("body", [
    # A wordmark in a link to a language home, or to the site's own root.
    '<header><a href="/en/"><svg viewBox="0 0 240 64"><path d="M0 0z"/></svg></a></header>',
    ('<header><a href="https://northfield.example/"><svg viewBox="0 0 240 64"><path d="M0 0z"/>'
     '</svg></a></header>'),
    # A wordmark in the navbar's brand wrapper.
    '<nav><span class="navbar-brand"><svg viewBox="0 0 240 64"><path d="M0 0z"/></svg></span></nav>',
    # An image whose label is the brand's name.
    '<header><img src="img/nf.png" width="240" height="64" alt="Northfield"></header>',
])
def test_a_wordmark_in_any_usual_place_is_not_imagery(body):
    res = score_imagery(_page(body), logo_url=LOGO, brand_name="Northfield")
    assert res["ok"] is False and res["kind"] == "logo-only", res


@pytest.mark.parametrize("body", [
    # A short path in the page body is any page, not a language home.
    '<main><a href="/go"><img src="/hero.jpg" width="800" height="500" alt="The market at dawn"></a></main>',
    # A section named brand holds the brand's story, not its logo.
    ('<section class="brand"><img src="/team.jpg" width="800" height="500" alt="The team"></section>'),
])
def test_only_the_logos_own_shape_is_taken_as_the_logo(body):
    assert score_imagery(_page(body), logo_url=LOGO)["kind"] == "image"


def test_a_bare_brand_class_in_the_header_is_the_logo():
    body = '<header><span class="brand"><svg viewBox="0 0 240 64"><path d="M0 0z"/></svg></span></header>'
    assert score_imagery(_page(body), logo_url=LOGO)["kind"] == "logo-only"


def test_a_photo_that_mentions_a_logo_in_its_alt_is_still_a_photo():
    body = ('<main><img src="img/storefront.jpg" width="800" height="500" '
            'alt="Our new logo above the storefront at dusk"></main>')
    assert score_imagery(_page(body), logo_url=LOGO)["kind"] == "image"


@pytest.mark.parametrize("body", [
    '<main><svg viewBox="0 0 24 24" width="24" height="24"><path d="M0 0z"/></svg></main>',
    f'<header><img src="{LOGO}" alt="Northfield"></header>',
    '<main><svg viewBox="0 0 640 400"><path d="M0 0z"/></svg></main>',
    '<main><img src="img/diagram.svg" width="640" height="400" alt="How orders flow"></main>',
    '<main><h1>Northfield</h1></main>',
])
def test_every_failing_page_is_told_to_add_photographs(body):
    res = score_imagery(_page(body), logo_url=LOGO)
    assert res["ok"] is False, res
    assert "Add photographs" in res["detail"] and "stock included" in res["detail"]
    assert "no picture" not in res["detail"] and "product screens" not in res["detail"]


def test_an_illustration_alone_is_not_a_photograph():
    for body in ('<main><svg viewBox="0 0 640 400"><path d="M0 0z"/></svg></main>',
                 '<main><img src="art/hero.svg" width="800" height="500" alt="A drawing"></main>'):
        assert score_imagery(_page(body))["kind"] == "illustration-only", body


@pytest.mark.parametrize("body", [
    (f'<header><img src="{LOGO}" alt="Northfield"></header>'
     '<main><img src="img/orders-screen.png" width="800" height="500" alt="The orders screen"></main>'),
    ('<header><a href="/" class="brand">Northfield</a></header>'
     '<main><a href="/"><img src="img/team-at-work.jpg" alt="The team at work"></a></main>'),
    '<main><video src="media/kitchen.mp4" muted></video></main>',
    '<main><div style="background:url(img/market.webp)"></div></main>',
])
def test_the_brands_own_photographs_beside_the_logo_count(body):
    assert score_imagery(_page(body), logo_url=LOGO)["ok"] is True


def test_a_brand_that_forbids_photography_passes_without_one_and_is_reported():
    body = '<main><svg viewBox="0 0 640 400"><path d="M0 0z"/></svg></main>'
    res = score_imagery(_page(body), photography_forbidden=True)
    assert res["ok"] is True and res["kind"] == "no-photography"
    assert "forbid photography" in res["detail"]


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


# ------------------------------------------------------------- photo rules


@pytest.mark.parametrize("entry", [
    "No stock photos or generic smiling people", "stock and generic imagery",
    "Stock imagery; generic illustrations", "posed lifestyle shots", "Never allow stock photos",
    "stock photos are not allowed", "stock photography is not permitted", "no stock",
    "avoid stock", "Don't use stock, even if it looks fine", "stock is never fine",
    "random/generic stock", "airbrushed people",
])
def test_a_ban_excludes_a_kind_of_photo_and_never_removes_photography(entry):
    p = build_profile({"photography": {"avoid": [entry]}})
    assert photo_exclusions(p) == [entry]
    assert photography_forbidden(p) is False
    assert image_search_terms(p), "photographs are still sourced, from the kinds that qualify"


@pytest.mark.parametrize("entry,excluded", [
    ("generic stock; curated stock allowed", ["generic stock"]),
    ("curated stock is fine when nothing real exists", []),
    ("watermarks", ["watermarks"]),
])
def test_an_unnegated_allowance_is_not_an_exclusion(entry, excluded):
    assert photo_exclusions(build_profile({"photography": {"avoid": [entry]}})) == excluded


@pytest.mark.parametrize("entry,forbidden", [
    # Photographs excluded as a whole.
    ("no photography", True), ("No photos at all", True), ("never use photographs", True),
    ("no photography whatsoever", True), ("we never use photography", True),
    ("no photographs", True), ("photos are not allowed", True),
    ("illustration only, never photos", True), ("Illustrations only, no photographs", True),
    ("No real photos, illustration only", True), ("illustrations instead of photos", True),
    ("only illustrations", True), ("drawn illustrations only", True),
    # One kind only: it narrows.
    ("no stock", False), ("no staged people", False), ("no stock photography", False),
    ("no photos of people", False), ("no lifestyle photography", False),
    ("no photography except product shots", False), ("illustration only for icons", False),
    ("photography", False), ("No stock photos or generic smiling people", False),
])
def test_only_a_rule_against_photos_as_a_whole_forbids_them(entry, forbidden):
    p = build_profile({"photography": {"avoid": [entry]}})
    assert photography_forbidden(p) is forbidden, entry
    assert photography_rule(p) == (entry if forbidden else ""), entry
    assert bool(image_search_terms(p)) is (not forbidden), entry
    if forbidden:
        assert photo_exclusions(p) == []
    else:
        assert photo_exclusions(p) == [entry]


def _forbidding_profile(rule: str = "illustration only, never photos") -> BrandProfile:
    return BrandProfile(name="Northfield", primary="#0B6E4F", logo={"url": LOGO, "alt": "Northfield"},
                        photography={"avoid": [rule]})


_BODY = ('<header><img src="' + LOGO + '" alt="Northfield"></header>'
         '<main><h1>Northfield</h1><a style="background:#0B6E4F" href="#go">Go</a>{}</main>')


def test_the_gate_reports_the_rule_it_honors():
    from engine.evaluator import evaluate
    html = _page(_BODY.format('<svg viewBox="0 0 640 400"><path d="M0 0z"/></svg>'))
    ev = evaluate(html=html, brand_profile=_forbidding_profile())
    assert ev.brand_passed is True, ev.notes
    note = next(n for n in ev.notes if n.startswith("IMAGERY:"))
    assert '"illustration only, never photos"' in note and "no photograph" in note


def test_a_photograph_under_a_rule_against_photos_fails_naming_both():
    from engine.evaluator import evaluate
    html = _page(_BODY.format('<img src="img/market-stall.jpg" width="800" height="500" alt="A stall">'))
    ev = evaluate(html=html, brand_profile=_forbidding_profile())
    assert ev.brand_passed is False
    note = next(n for n in ev.notes if "imagery" in n)
    assert "img/market-stall.jpg" in note and '"illustration only, never photos"' in note
    res = score_imagery(html, logo_url=LOGO, photography_rule="no photography")
    assert res["kind"] == "photo-under-ban"


@pytest.mark.parametrize("img", ['<img alt="A stall">', '<img src="" alt="A stall">',
                                 '<img src="  " alt="A stall">'])
def test_an_img_with_no_source_is_not_a_photograph(img):
    assert score_imagery(_page("<main>" + img + "</main>"))["ok"] is False


def test_the_gate_says_any_raster_counts_until_the_grade_check():
    doc = " ".join(score_imagery.__doc__.split())
    assert "Any raster counts, screenshots and raster drawings included" in doc


def test_a_forbidden_flag_round_trips_through_brand_md():
    p = build_profile({"photography": {"forbidden": True}})
    assert photography_forbidden(p) is True
    assert photography_forbidden(parse_brand_md(render_md(p))) is True


def test_the_gate_honors_a_brand_that_forbids_photography_by_name():
    from engine.evaluator import evaluate
    profile = BrandProfile(name="Northfield", primary="#0B6E4F", logo={"url": LOGO, "alt": "Northfield"},
                           photography={"avoid": ["no photography"]})
    html = _page(f'<header><img src="{LOGO}" alt="Northfield"></header>'
                 '<main><h1>Northfield</h1><a style="background:#0B6E4F" href="#go">Go</a>'
                 '<svg viewBox="0 0 640 400"><path d="M0 0z"/></svg></main>')
    ev = evaluate(html=html, brand_profile=profile)
    assert ev.brand_passed is True, ev.notes


def test_the_engines_old_default_avoid_line_excludes_nothing():
    legacy = ("---\nname: Northfield\nversion: 1\nlanguage: en\n---\n\n# Northfield\n\n## Visual\n\n"
              "### Photography\n\n- **Avoid:** random/generic stock, AI-slop clutter\n")
    p = parse_brand_md(legacy)
    assert p.photography["avoid"] == ["random/generic stock", "AI-slop clutter"]
    assert photo_exclusions(p) == [] and photography_forbidden(p) is False
    more = build_profile({"photography": {"avoid": ["random/generic stock", "AI-slop clutter",
                                                    "posed lifestyle shots"]}})
    assert photo_exclusions(more) == ["posed lifestyle shots"]


def test_a_new_brand_md_default_line_excludes_nothing_about_stock():
    p = parse_brand_md(render_md(build_profile({"name": "Northfield"})))
    assert all("stock" not in e for e in photo_exclusions(p))
    assert image_search_terms(p)
