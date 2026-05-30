"""Brand extraction tests — normalize captured signals into a travelling profile."""
from engine.brand import build_profile, render_md, hue_family


# Real signals captured from instantskiphire.com (the dogfood ground truth):
# brand is dark forest green + Roboto Flex + their own logo — NOT clay/mono.
SKIPHIRE_SIGNALS = {
    "source": "https://instantskiphire.com/commercial-skip-hire/",
    "logo": {"src": "https://instantskiphire.com/wp-content/uploads/2026/05/Logo-transparent-.avif",
             "alt": "instant skip hire logo"},
    "brand_colors": [{"hex": "#1c3829", "score": 49}, {"hex": "#001a0b", "score": 3}],
    "fonts": {"h1": '"Roboto Flex", system-ui, sans-serif',
              "body": '"Roboto Flex", system-ui, sans-serif'},
}


def test_hue_family():
    assert hue_family("#1c3829") == "green"     # skip-hire brand
    assert hue_family("#cc785c") == "orange"    # the clay the engine wrongly defaulted to
    assert hue_family("#5e6ad2") in ("blue", "violet")  # the blurple
    assert hue_family("#ffffff") == "neutral"
    assert hue_family("#0a0b0d") == "neutral"


def test_build_profile_from_skiphire_signals():
    p = build_profile(SKIPHIRE_SIGNALS)
    assert p.name == "Instant Skip Hire"
    assert p.primary == "#1c3829"
    assert p.primary_family == "green"
    assert p.fonts["display"] == "Roboto Flex"
    assert p.fonts["body"] == "Roboto Flex"
    assert "Logo-transparent" in p.logo["url"]
    assert p.source.endswith("/commercial-skip-hire/")


def test_primary_skips_neutral_colors():
    """A neutral captured first must not become the brand primary; the real hue wins."""
    p = build_profile({"colors": ["#0a0b0d", "#ffffff", "#1c3829"]})
    assert p.primary == "#1c3829"
    assert p.primary_family == "green"


def test_render_md_carries_the_anchor():
    md = render_md(build_profile(SKIPHIRE_SIGNALS))
    assert "#1c3829" in md
    assert "Instant Skip Hire" in md
    assert "Roboto Flex" in md
    assert "MUST use this" in md and "house style fails" in md  # the travelling-anchor contract
