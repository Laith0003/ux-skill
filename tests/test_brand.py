"""Brand extraction tests — color from the logo, type from the logo style."""
from engine.brand import build_profile, render_md, hue_family


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
    md = render_md(build_profile(SKIPHIRE_SIGNALS))
    assert "#f0890f" in md
    assert "Instant Skip Hire" in md
    assert "MUST use this brand" in md
    assert "fails the brand-fidelity gate" in md
