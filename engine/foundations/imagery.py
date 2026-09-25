"""Imagery foundation: aspect ratios for media, a scrim that keeps text
over any image readable, a brand tint and a duotone pair for treating
photos in the brand's light.

Every value is a continuous function of the axes and the brand color,
never of an industry. The hero ratio widens as the system gets bolder,
airier and more playful; the card ratio squares up as geometry softens and
widens as formality rises. The scrim's alpha is the least that lets white
text reach 4.5:1 over a pure white image (7:1 under high contrast), so the
worst photo still reads; the scrim is measured over a white and a black
image, and the lower ratio counts, since white is the worst image for light
text and black the worst for dark text (text whose luminance falls between
the two composites meets a grey image that matches it). The duotone pair takes the brand hue: a deep
shadow and a highlight pulled warm or cool with the warmth axis; the tint
is the brand color at a strength that grows with warmth.

The corner of media is radius.media (the radius foundation).
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations import character
from engine.foundations.color_math import (
    contrast, hex_to_oklch, hex_to_rgb, luminance, oklch_to_hex, rgb_to_hex)
from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

HERO_RATIOS: Tuple[Tuple[int, int], ...] = ((4, 3), (3, 2), (16, 9), (2, 1), (21, 9))
CARD_RATIOS: Tuple[Tuple[int, int], ...] = ((1, 1), (4, 3), (3, 2), (16, 9))
PORTRAIT: Tuple[int, int] = (4, 5)
# The minimum the text on the scrim must reach over the worst image.
SCRIM_TEXT = {"standard": (4.5, "1.4.3"), "high": (7.0, "1.4.6")}
# The two extreme images: white is the worst under light text, black under
# dark text. Compositing is linear in each channel and luminance rises with
# every channel, so no photo's composite is lighter than white's or darker
# than black's.
IMAGES = (("white", "#FFFFFF"), ("black", "#000000"))
# Our floor between the duotone's shadow and highlight, so an image keeps
# its detail.
DUOTONE_FLOOR = 7.0
WHITE = "#FFFFFF"


def hero_ratio(axes: AxisValues) -> Tuple[int, int]:
    t = character.clamp(0.4 * axes.contrast + 0.4 * (1 - axes.density)
                        + 0.2 * (1 - axes.formality))
    return HERO_RATIOS[int(t * (len(HERO_RATIOS) - 1) + 0.5)]


def card_ratio(axes: AxisValues) -> Tuple[int, int]:
    t = character.clamp(0.6 * (1 - axes.geometry) + 0.4 * axes.formality)
    return CARD_RATIOS[int(t * (len(CARD_RATIOS) - 1) + 0.5)]


def _over(color: str, alpha: float, under: str) -> str:
    """`color` at `alpha` composited over the opaque `under`."""
    top, bottom = hex_to_rgb(color), hex_to_rgb(under)
    return rgb_to_hex(tuple(alpha * t + (1 - alpha) * b for t, b in zip(top, bottom)))


def _worst(text: str, color: str, alpha: float) -> Tuple[float, str]:
    """The lowest ratio of `text` on `color` at `alpha` over any image, and
    the image that gives it. Over a grey image the composite runs between
    the two extremes, so when the text's luminance lies between theirs some
    grey matches it and the ratio is 1:1."""
    over = [(contrast(text, _over(color, alpha, hx)), name, luminance(_over(color, alpha, hx)))
            for name, hx in IMAGES]
    lows = sorted(lum for _, _, lum in over)
    if lows[0] < luminance(text) < lows[1]:
        return 1.0, "grey"
    ratio, name, _ = min(over)
    return ratio, name


def scrim_alpha(base: str, need: float, text: str = WHITE) -> int:
    """The smallest alpha, in 1/255 steps, at which `text` reaches `need`
    over `base` laid on the worst image for it."""
    for a in range(256):
        if _worst(text, base, a / 255)[0] >= need:
            return a
    return 255


# Chroma of the scrim base, and of the duotone highlight at the brand's hue
# and at the warm or cool anchor, for a brand at full hue weight.
SCRIM_C = 0.03
HIGHLIGHT_C = (0.04, 0.07)


def scrim_base(brand_hex: str) -> str:
    """A near black in the brand's hue, so a scrim reads as part of the
    palette rather than as grey fog. Its chroma scales with the brand's
    (character.hue_weight), so a grey brand gets a grey scrim."""
    _, chroma, hue = hex_to_oklch(brand_hex)
    return oklch_to_hex(0.16, SCRIM_C * character.hue_weight(chroma), hue)


def duotone(axes: AxisValues, brand_hex: str) -> Tuple[str, str]:
    """(shadow, highlight): the brand hue deep, and a light that travels
    in a straight line in the OKLab a/b plane from the brand hue toward a
    warm or a cool hue with warmth, so it never passes through a third hue.
    Both take chroma from the brand in proportion, so a grey brand gets a
    grey pair at the middle warmth."""
    _, chroma, hue = hex_to_oklch(brand_hex)
    shadow = oklch_to_hex(0.24, min(0.12, chroma), hue)
    anchor = character.WARM_HUE if axes.warmth >= 0.5 else character.COOL_HUE
    light_hue, light_c = character.ab_mix(
        hue, HIGHLIGHT_C[0] * character.hue_weight(chroma), anchor, HIGHLIGHT_C[1],
        0.6 * character.warm_pull(axes))
    return shadow, oklch_to_hex(0.94, light_c, light_hue)


def tint_alpha(axes: AxisValues) -> int:
    """How strongly a brand wash tints a photo, 0 to 255: from 0.10 for a
    cool brand to 0.30 for a warm one."""
    return int((0.10 + 0.20 * axes.warmth) * 255 + 0.5)


def generate_imagery(axes: AxisValues, brand_hex: str) -> Generated:
    ts = TokenSet()
    ratios = sorted({hero_ratio(axes), card_ratio(axes), PORTRAIT},
                    key=lambda r: r[0] / r[1])
    for w, h in ratios:
        ts.add(Token(f"imagery.aspect.{w}-{h}", "number", round(w / h, 4)))
    base = scrim_base(brand_hex)
    alphas = {k: scrim_alpha(base, need) for k, (need, _) in SCRIM_TEXT.items()}
    for k, a in alphas.items():
        ts.add(Token(f"imagery.shade.{k}", "color", f"{base}{a:02X}"))
    ts.add(Token("imagery.white", "color", WHITE))
    shadow, highlight = duotone(axes, brand_hex)
    ts.add(Token("imagery.duo.shadow", "color", shadow))
    ts.add(Token("imagery.duo.highlight", "color", highlight))
    brand = rgb_to_hex(hex_to_rgb(brand_hex))
    ts.add(Token("imagery.wash", "color", f"{brand}{tint_alpha(axes):02X}"))

    for name, (w, h) in (("hero", hero_ratio(axes)), ("card", card_ratio(axes)),
                         ("portrait", PORTRAIT)):
        ts.add(Token(f"imagery.ratio.{name}", "number", "{imagery.aspect.%d-%d}" % (w, h),
                     layer="semantic"))
    ts.add(Token("imagery.scrim", "color", "{imagery.shade.standard}",
                 modes={"contrast:high": "{imagery.shade.high}"}, layer="semantic"))
    ts.add(Token("imagery.on-scrim", "color", "{imagery.white}", layer="semantic"))
    ts.add(Token("imagery.duotone.shadow", "color", "{imagery.duo.shadow}", layer="semantic"))
    ts.add(Token("imagery.duotone.highlight", "color", "{imagery.duo.highlight}",
                 layer="semantic"))
    ts.add(Token("imagery.tint", "color", "{imagery.wash}", layer="semantic"))
    hw, hh = hero_ratio(axes)
    cw, ch = card_ratio(axes)
    return Generated(tokens=ts, notes=[
        f"imagery: hero {hw}:{hh}, card {cw}:{ch}, scrim alpha {alphas['standard'] / 255:.2f} "
        f"({alphas['high'] / 255:.2f} under high contrast)"])


ROLE_TYPES: Dict[str, str] = {
    "imagery.ratio.hero": "number", "imagery.ratio.card": "number",
    "imagery.ratio.portrait": "number", "imagery.scrim": "color", "imagery.on-scrim": "color",
    "imagery.duotone.shadow": "color", "imagery.duotone.highlight": "color",
    "imagery.tint": "color",
}


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _split(hx: str) -> Tuple[str, float]:
    return hx[:7], (int(hx[7:9], 16) / 255 if len(hx) == 9 else 1.0)


def _scrim_text(ts: TokenSet, mode: str) -> List[str]:
    """The text on the scrim reaches the text minimum over the worst image
    for it in this context: a white image under light text, a black one
    under dark text. The lower of the two is measured."""
    if not (_typed(ts, "imagery.scrim") and _typed(ts, "imagery.on-scrim")):
        return []
    key = "high" if "contrast:high" in mode else "standard"
    need, criterion = SCRIM_TEXT[key]
    color, alpha = _split(str(ts.resolve("imagery.scrim", mode)))
    text = str(ts.resolve("imagery.on-scrim", mode))
    ratio, image = _worst(text, color, alpha)
    if ratio >= need:
        return []
    return [f"imagery.on-scrim on imagery.scrim over a {image} image ({mode}) is "
            f"{int(ratio * 100) / 100:.2f}:1; WCAG {criterion} needs {need:g}:1, so point "
            "imagery.scrim at a stronger shade"]


def _ratios(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for role in ("imagery.ratio.hero", "imagery.ratio.card", "imagery.ratio.portrait"):
        if _typed(ts, role):
            v = ts.resolve(role, mode)
            if not 0.2 <= v <= 5:
                out.append(f"{role} is {v:g}; an aspect ratio outside 1:5 to 5:1 crops any "
                           "photo to a strip, so point it at a ratio in that range")
    return out


def _duotone(ts: TokenSet, mode: str) -> List[str]:
    a, b = "imagery.duotone.shadow", "imagery.duotone.highlight"
    if not (_typed(ts, a) and _typed(ts, b)):
        return []
    ratio = contrast(str(ts.resolve(a, mode)), str(ts.resolve(b, mode)))
    if ratio >= DUOTONE_FLOOR:
        return []
    return [f"{a} and {b} are {int(ratio * 100) / 100:.2f}:1 apart; our floor is "
            f"{DUOTONE_FLOOR:g}:1 so a duotone photo keeps its detail, so move them apart"]


CHECKS: Tuple[Check, ...] = (
    Check("scrim-text", "1.4.3", _scrim_text, axes=("contrast",)),
    Check("media-ratios", "system", _ratios,
          exempt_axes=(("contrast", "ratios never carry modes"),)),
    Check("duotone-range", "system", _duotone,
          exempt_axes=(("contrast", "the duotone pair never carries modes"),)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_imagery(axes, inputs.brand_hex)


FOUNDATION = Foundation(name="imagery", generate=_generate, checks=CHECKS,
                        role_types=ROLE_TYPES)
