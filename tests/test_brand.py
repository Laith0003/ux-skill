"""Brand extraction tests — color from the logo, type from the logo style."""
from engine.brand import (
    build_profile, render_md, parse_brand_md, hue_family, image_search_terms,
    score_brand_fidelity, score_imagery,
)


# Real signals captured from instantskiphire.com (the dogfood ground truth):
# the LOGO is amber #f0890f (dominant) + green; the CSS chrome is green #1c3829;
# the site font is the Roboto Flex default; the wordmark is a bold rounded sans.
SKIPHIRE_SIGNALS = {
    "source": "https://instantskiphire.com/commercial-skip-hire/",
    "logo": {"src": "https://instantskiphire.com/wp-content/uploads/2026/05/Logo-transparent-.avif",
             "alt": "instant skip hire logo"},
    "logo_colors": [{"hex": "#f0890f", "score": 75}, {"hex": "#1c3829", "score": 12}],
    "brand_colors": [{"hex": "#1c3829", "score": 49}],
    "logo_type_style": "bold rounded humanist sans, friendly and sturdy",
    "fonts": {"h1": '"Roboto Flex", system-ui, sans-serif',
              "body": '"Roboto Flex", system-ui, sans-serif'},
}


def test_hue_family():
    assert hue_family("#f0890f") == "orange"    # the logo / true brand color
    assert hue_family("#1c3829") == "green"     # CSS chrome (secondary)
    assert hue_family("#cc785c") == "orange"    # the clay the engine wrongly defaulted to
    assert hue_family("#ffffff") == "neutral"


def test_primary_comes_from_the_logo_not_css():
    p = build_profile(SKIPHIRE_SIGNALS)
    assert p.name == "Instant Skip Hire"
    assert p.primary == "#f0890f"          # amber from the logo, NOT green from CSS
    assert p.primary_family == "orange"
    assert p.primary_source == "logo"
    assert "#1c3829" in p.secondary        # green demoted to secondary
    assert "Logo-transparent" in p.logo["url"]


def test_default_font_is_rejected_and_deferred_to_logo_style():
    p = build_profile(SKIPHIRE_SIGNALS)
    assert p.fonts["display"] == ""                       # Roboto Flex rejected
    assert p.fonts["display_source"] == "logo-style"
    assert "rounded" in p.fonts["type_personality"]       # pick type matching the logo
    assert any("Rejected default" in n for n in p.notes)


def test_logo_color_wins_over_css():
    p = build_profile({"logo_colors": [{"hex": "#f0890f"}], "brand_colors": [{"hex": "#1c3829"}]})
    assert p.primary == "#f0890f" and p.primary_source == "logo"
    assert "#1c3829" in p.secondary


def test_distinctive_site_font_is_kept():
    p = build_profile({"fonts": {"h1": '"Spectral", serif'}})
    assert p.fonts["display"] == "Spectral"
    assert p.fonts["display_source"] == "site"


def test_falls_back_to_css_when_no_logo_colors():
    p = build_profile({"colors": ["#0a0b0d", "#ffffff", "#1c3829"]})
    assert p.primary == "#1c3829"          # skips neutrals, uses the real CSS hue
    assert p.primary_source == "css"


def test_render_md_carries_the_anchor():
    """render_md emits a VALID open-standard brand.md AND keeps our gate anchor.

    The format conforms to thebrandmd/brand.md (frontmatter + the three H2
    layers), while a single anchor line keeps both enforcement substrings so the
    file still reads as our brand-fidelity gate note (our moat)."""
    md = render_md(build_profile(SKIPHIRE_SIGNALS))
    # Our moat: the brand primary, the name, and BOTH gate substrings survive.
    assert "#f0890f" in md
    assert "Instant Skip Hire" in md
    assert "MUST use this" in md
    assert "brand-fidelity gate" in md
    # Standard shape: YAML frontmatter + the three ordered H2 layers + Colors H3.
    assert md.lstrip().startswith("---")
    assert "name: Instant Skip Hire" in md
    assert "## Strategy" in md
    assert "## Voice" in md
    assert "## Visual" in md
    assert "### Colors" in md


def test_render_md_is_a_valid_standard_brand_md():
    """(a) The rendered file conforms to the open standard's required structure."""
    md = render_md(build_profile(SKIPHIRE_SIGNALS))
    # Frontmatter keys the spec requires.
    assert "name:" in md and "tagline:" in md and "version:" in md and "language:" in md
    # The H2 layers appear in the spec's order: Strategy -> Voice -> Visual.
    assert md.index("## Strategy") < md.index("## Voice") < md.index("## Visual")
    # Colors carries the primary hex and a "colors to avoid" line.
    assert "#f0890f" in md
    assert "avoid" in md.lower()
    # The gate anchor warning is a single line carrying both enforcement phrases.
    anchor = [ln for ln in md.splitlines() if "MUST use this" in ln]
    assert len(anchor) == 1 and "brand-fidelity gate" in anchor[0]


def test_parse_brand_md_round_trips_render():
    """(b) parse_brand_md(render_md(build_profile(...))) recovers primary + name."""
    p = parse_brand_md(render_md(build_profile(SKIPHIRE_SIGNALS)))
    assert p.primary == "#f0890f"           # primary survives the round-trip
    assert p.name == "Instant Skip Hire"    # name survives via frontmatter
    assert "#1c3829" in p.secondary         # green stays secondary, not avoided
    assert p.primary_source == "brand-md"   # provenance marked on the input side


def test_parse_brand_md_minimal_handwritten():
    """(c) A hand-written minimal standard brand.md parses (case-insensitive hex)."""
    md = (
        "---\n"
        "name: Northwind\n"
        "tagline: Built to last\n"
        "version: 1\n"
        "language: en\n"
        "---\n\n"
        "# Northwind\n\n"
        "## Visual\n\n"
        "### Colors\n\n"
        "- Primary: #0F172A\n"
    )
    p = parse_brand_md(md)
    assert p.primary == "#0f172a"           # #0F172A normalized to lowercase
    assert p.name == "Northwind"
    assert p.tagline == "Built to last"
    assert p.primary_source == "brand-md"


def test_parse_brand_md_is_robust_to_empty():
    """parse_brand_md never throws on sparse / empty input."""
    assert parse_brand_md("").primary == ""
    assert parse_brand_md("just some text, no frontmatter, no sections").name == ""
    # Frontmatter only, no Visual layer: name parses, colors stay empty.
    p = parse_brand_md("---\nname: Bare\nversion: 1\n---\n# Bare\n")
    assert p.name == "Bare" and p.primary == "" and p.secondary == []


def test_colors_to_avoid_lists_house_colors_for_amber_brand():
    """(d) The amber brand's colors_to_avoid carries the engine house clay."""
    p = build_profile(SKIPHIRE_SIGNALS)
    assert "#cc785c" in p.colors_to_avoid   # clay (Claude house) -- never for this brand
    assert "#5e6ad2" in p.colors_to_avoid   # blurple (Linear house)
    assert p.primary not in p.colors_to_avoid


def test_colors_to_avoid_skips_house_color_equal_to_primary():
    """A brand whose primary IS a house color does not list its own primary to avoid."""
    p = build_profile({"logo_colors": [{"hex": "#cc785c"}]})
    assert p.primary == "#cc785c"
    assert "#cc785c" not in p.colors_to_avoid   # cannot avoid your own primary
    assert "#5e6ad2" in p.colors_to_avoid       # the other house color still listed


def test_render_and_build_are_deterministic_with_new_fields():
    """(e) build_profile + render_md stay byte-stable with the richer fields."""
    a = build_profile(SKIPHIRE_SIGNALS)
    b = build_profile(SKIPHIRE_SIGNALS)
    assert a.to_dict() == b.to_dict()
    assert render_md(a) == render_md(b)
    # And a full round-trip is stable too.
    assert parse_brand_md(render_md(a)).to_dict() == parse_brand_md(render_md(b)).to_dict()


def test_parse_brand_md_recovers_typography_and_tonal():
    """A standard brand.md with real fonts + a We Say/We Never Say table parses."""
    md = (
        "---\nname: Voicey\nversion: 1\nlanguage: en\n---\n\n"
        "# Voicey\n\n"
        "## Voice\n\n"
        "### Tonal Rules\n\n"
        "- Lead with the verb.\n\n"
        "| We Say | We Never Say |\n"
        "| --- | --- |\n"
        "| 50 points added. | Congratulations! |\n\n"
        "## Visual\n\n"
        "### Typography\n\n"
        "- **Display:** Cabinet Grotesk -- weight 700. Usage: headings.\n"
        "- **Body:** Public Sans -- weight regular. Usage: body.\n"
    )
    p = parse_brand_md(md)
    assert p.fonts.get("display") == "Cabinet Grotesk"
    assert p.fonts.get("body") == "Public Sans"
    assert p.tonal.get("rules") == ["Lead with the verb."]
    assert p.tonal.get("we_say") == ["50 points added."]
    assert p.tonal.get("we_never_say") == ["Congratulations!"]


def test_parse_brand_md_rejects_default_display_font():
    """A default font in the Display slot is rejected (rule 4), not preserved."""
    md = (
        "---\nname: Defaulty\nversion: 1\n---\n\n# Defaulty\n\n"
        "## Visual\n\n### Typography\n\n"
        "- **Display:** Inter -- weight 700.\n"
    )
    p = parse_brand_md(md)
    assert p.fonts.get("display", "") == ""   # Inter is a default; not kept


def test_image_search_terms_are_on_brand_and_real():
    """P3: deterministic search-term suggestions for sourcing curated stock.

    Imagery is mandatory and REAL (rule 8): client assets first, then curated
    Unsplash/Pexels chosen to match the brand. This helper feeds that sourcing
    step -- it must be brand-led and anchor on real photography, never picsum."""
    p = build_profile(SKIPHIRE_SIGNALS)
    terms = image_search_terms(p)
    assert isinstance(terms, list) and terms
    joined = " ".join(terms).lower()
    # Brand hue (amber/orange) seeds a color word.
    assert "amber" in joined
    # Voice descriptors from the logo style carry through (friendly / sturdy).
    assert "friendly" in terms or "sturdy" in terms
    # Anchors on real photography, never a placeholder service.
    assert any("photography" in t for t in terms)
    assert "picsum" not in joined and "placeholder" not in joined


def test_image_search_terms_factor_in_temperature():
    """The 7-axis temperature shifts the mood words deterministically."""
    p = build_profile(SKIPHIRE_SIGNALS)
    warm = image_search_terms(p, temperature={"warmth": 0.9, "formality": 0.9})
    cool = image_search_terms(p, temperature={"warmth": 0.1, "formality": 0.1})
    assert "warm toned" in warm and "polished editorial" in warm
    assert "cool toned" in cool and "candid casual" in cool
    assert warm != cool


def test_image_search_terms_deterministic_and_dedup():
    p = build_profile(SKIPHIRE_SIGNALS)
    a = image_search_terms(p, temperature={"warmth": 0.8})
    b = image_search_terms(p, temperature={"warmth": 0.8})
    assert a == b                       # same input -> same output
    assert len(a) == len(set(a))        # no duplicates


def test_image_search_terms_handle_empty_profile():
    """No brand signal still yields a usable, non-generic real-imagery baseline."""
    p = build_profile({})
    terms = image_search_terms(p)
    assert terms
    assert any("photography" in t or "editorial" in t for t in terms)


def test_anchor_recommendation_overrides_palette_with_brand():
    """P2: a recommendation's palette is overridden by the extracted brand; the
    engine's blurple loses to the brand amber, neutrals stay, logo+type carry."""
    from engine.brand import build_profile, anchor_recommendation
    p = build_profile(SKIPHIRE_SIGNALS)
    rec = {"palette": {"id": "linear-graphite",
                       "colors": {"primary": "#5e6ad2", "accent": "#5e6ad2", "ink": "#0a0b0d"}},
           "style": {"id": "monochrome-precise"}}
    out = anchor_recommendation(rec, p)
    assert out["palette"]["colors"]["primary"] == "#f0890f"   # brand amber wins
    assert out["palette"]["colors"]["accent"] == "#f0890f"
    assert out["palette"]["colors"]["ink"] == "#0a0b0d"        # neutral role preserved
    assert out["palette"]["brand_anchored"] is True
    assert out["brand"]["logo"]["url"].endswith(".avif")
    assert out["type_directive"]["reject_defaults"] is True
    assert "rounded" in out["type_directive"]["match_logo_style"]


# --- P4: brand_fidelity scoring (scored + hard floor) ---

# A faithful build: brand amber #f0890f drives the palette/CTA, the wordmark is in
# the header, and the type matches the logo style (no Roboto Flex fallback).
_FAITHFUL_HTML = """<!doctype html><html lang="en"><head>
<title>Instant Skip Hire</title>
<style>
  :root { --primary: #f0890f; --ink: #14110d; }
  .cta { background: #F0890F; color: #fff; }
  h1, .display { font-family: "Cabinet Grotesk", system-ui, sans-serif; }
  body { font-family: "Public Sans", system-ui, sans-serif; }
</style></head><body>
<header><a class="logo" href="/">Instant Skip Hire</a></header>
<main>
  <section class="hero"><h1>Book a commercial skip today</h1>
  <button class="cta">Get a quote</button></section>
</main></body></html>"""

# A drifting build: clay #cc785c (Claude house color) as primary, NO logo/wordmark,
# and the rejected Roboto Flex default brought back as the display face.
_DRIFTED_HTML = """<!doctype html><html><head>
<style>
  :root { --primary: #cc785c; }
  .cta { background: #cc785c; }
  h1 { font-family: "Roboto Flex", system-ui, sans-serif; }
</style></head><body>
<main><section><h1>Skips</h1><button class="cta">Get started</button></section></main>
</body></html>"""


def test_brand_fidelity_passes_for_on_brand_page():
    """Amber #f0890f used + logo referenced -> passes, high score."""
    p = build_profile(SKIPHIRE_SIGNALS)
    r = score_brand_fidelity(_FAITHFUL_HTML, p)
    assert r["passed"] is True
    assert r["score"] >= 90
    by = {f["check"]: f for f in r["findings"]}
    assert by["primary_used"]["ok"] is True
    assert by["logo_present"]["ok"] is True
    assert by["no_house_drift"]["ok"] is True


def test_brand_fidelity_fails_hard_floor_on_house_color_no_logo():
    """Clay #cc785c as primary with no logo -> hard floor: passed=False."""
    p = build_profile(SKIPHIRE_SIGNALS)
    r = score_brand_fidelity(_DRIFTED_HTML, p)
    assert r["passed"] is False                       # hard floor, regardless of score
    by = {f["check"]: f for f in r["findings"]}
    assert by["primary_used"]["ok"] is False          # brand amber missing
    assert by["logo_present"]["ok"] is False          # no wordmark
    assert by["no_house_drift"]["ok"] is False        # clay leaked in
    assert by["type_matches"]["ok"] is False          # Roboto Flex came back


def test_brand_fidelity_hard_floor_logo_present_but_primary_missing():
    """Even with the logo, dropping the brand primary trips the hard floor."""
    p = build_profile(SKIPHIRE_SIGNALS)
    html = ('<body><header><a class="logo">Instant Skip Hire</a></header>'
            '<main><section><h1 style="color:#222">Skips</h1>'
            '<img src="/x.avif" alt="a skip" width="8" height="6"></section></main></body>')
    r = score_brand_fidelity(html, p)
    assert r["passed"] is False
    by = {f["check"]: f for f in r["findings"]}
    assert by["logo_present"]["ok"] is True
    assert by["primary_used"]["ok"] is False


def test_brand_fidelity_case_insensitive_primary():
    """The brand hex matches regardless of case (#f0890f vs #F0890F)."""
    p = build_profile(SKIPHIRE_SIGNALS)
    html = ('<body><header><a class="logo">Instant Skip Hire</a></header>'
            '<main><section style="background:#F0890F"><h1>Skips</h1></section></main></body>')
    r = score_brand_fidelity(html, p)
    by = {f["check"]: f for f in r["findings"]}
    assert by["primary_used"]["ok"] is True
    assert r["passed"] is True


def test_brand_fidelity_is_deterministic():
    p = build_profile(SKIPHIRE_SIGNALS)
    a = score_brand_fidelity(_FAITHFUL_HTML, p)
    b = score_brand_fidelity(_FAITHFUL_HTML, p)
    assert a == b


# --- imagery presence (richness -- a SIBLING to brand fidelity, not in its score) ---

def test_imagery_real_image_passes():
    html = ('<!doctype html><html><body><main>'
            '<img src="/hero.avif" alt="a commercial skip" width="800" height="600">'
            '</main></body></html>')
    r = score_imagery(html)
    assert r["ok"] is True and r["kind"] == "image"


def test_imagery_substantial_svg_passes():
    """A real inline SVG illustration (large viewBox) counts as imagery."""
    html = ('<!doctype html><html><body><main>'
            '<svg viewBox="0 0 480 320"><path d="M0 0h480v320H0z"/></svg>'
            '</main></body></html>')
    r = score_imagery(html)
    assert r["ok"] is True and r["kind"] == "illustration-svg"


def test_imagery_icon_only_page_fails():
    """Icons are NOT imagery: a wall of cards with only 24px SVGs is a text-wall."""
    html = ('<!doctype html><html><body><main><h1>Skips</h1>'
            '<div class="card"><svg viewBox="0 0 24 24" width="24" height="24">'
            '<path d="M3 7h18"/></svg>Fast</div></main></body></html>')
    r = score_imagery(html)
    assert r["ok"] is False and r["kind"] == "icons-only"


def test_imagery_background_photo_passes():
    html = ('<!doctype html><html><body>'
            '<section style="background:url(/yard.jpg) center"><h1>Skips</h1></section>'
            '</body></html>')
    r = score_imagery(html)
    assert r["ok"] is True and r["kind"] == "bg-photo"


def test_imagery_text_wall_fails():
    html = ('<!doctype html><html><body><main><h1>Skips</h1>'
            '<div class="card">A</div><div class="card">B</div></main></body></html>')
    r = score_imagery(html)
    assert r["ok"] is False and r["kind"] == "none"


def test_imagery_fragment_is_exempt():
    """Component fragments (no <body>) are not penalized -- not every partial needs art."""
    r = score_imagery('<section class="pricing"><h2>Pro</h2><p>Real copy.</p></section>')
    assert r["ok"] is True and r["kind"] == "fragment"


def test_imagery_is_deterministic():
    html = ('<!doctype html><html><body>'
            '<img src="/x.png" alt="x" width="400" height="300"></body></html>')
    assert score_imagery(html) == score_imagery(html)
