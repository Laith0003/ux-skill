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

from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

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


# The first screen a hero fills, desktop and phone, and what sits under
# the two-line headline in the scrim's region: a lede, the action, the gaps
# between them and the hero's bottom padding, in px.
HERO_VIEWS = ((1440, 900), (390, 844))
TEXT_ALLOWANCE_PX = 250
# The scrim reaches at least this share of the hero from its bottom edge,
# and fades to clear over SCRIM_FADE of the height above that.
SCRIM_REACH_MIN, SCRIM_FADE = 0.4, 0.15


def text_region(display_px: float, leading: float, view_height: float) -> float:
    """The share of a hero's height, from its bottom edge, that a two-line
    headline at `display_px` and `leading` fills with what sits under it."""
    return (2 * display_px * leading + TEXT_ALLOWANCE_PX) / view_height


def scrim_reach(axes: AxisValues, body_px: int = 16) -> float:
    """How far up from the bottom edge a full-bleed hero's scrim holds its
    full strength, as a share of the hero's height: the region the
    headline sits in on the desktop and the phone view (the landing
    display at the tallest display leading, typography.DISPLAY_LEAD[0]),
    at least SCRIM_REACH_MIN, rounded up to hundredths."""
    import math
    from engine.foundations import typography
    px = typography.latin_px(axes, body_px)[typography.DISPLAY_STEP - 1]
    lh = typography.DISPLAY_LEAD[0]
    need = max(text_region(px, lh, HERO_VIEWS[0][1]),
               text_region(min(px, character.PHONE_DISPLAY_PX[1]), lh, HERO_VIEWS[1][1]))
    return min(1.0, max(SCRIM_REACH_MIN, math.ceil(need * 100) / 100))


# Photography. A page uses photographs; when the client gives none the
# skill sources them to this direction. Every quantity is continuous in the
# axes and the brand color; the words that describe it for a search are
# read from the quantities, never from an industry. Measured in CIELAB over
# a photo: L* (lightness), b* (temperature: warm above 0, cool below) and
# C* (chroma); contrast is the standard deviation of L*, the black point
# the L* of its darkest percent.
PHOTO_KINDS = ("people in context", "places", "the product or goods", "details and textures",
               "staged lifestyle")
# The spread every photo on a page keeps from the page's own mean (the
# grade lock), from a formal to a playful brand, and how far the page's
# mean may sit from the direction's target.
GRADE_SPREAD = {"lightness": (6.0, 10.0), "temperature": (3.0, 5.0), "chroma": (4.0, 8.0)}
GRADE_TOLERANCE = {"lightness": 12.0, "temperature": 6.0, "chroma": 8.0}
# What a photo shows, by the brief's product_type (the product the page
# sells), its audience's age and its primary action: structured fields,
# never a word of the brief.
SUBJECTS = {
    "app": "people using the product in their own setting, the screen implied or out of focus",
    "software": "people at work with the product, the screen implied or out of focus",
    "commerce": "the goods themselves in real light, then in use",
    "marketplace": "the people on both sides of an exchange",
    "local-service": "the place and the people who serve in it",
    "editorial": "the subjects of the stories, where they are",
    "marketing-site": "the team and its work, where it happens",
}
PEOPLE = {"children": "children with the adults around them", "teens": "teenagers",
          "adults": "adults", "all-ages": "people across ages", "older-adults": "people over 60"}
MOMENTS = {"sign-up": "someone starting out", "sign-in": "someone returning to their work",
           "buy": "the goods in hand", "quote": "the job in progress", "book": "the moment before "
           "the visit", "contact": "a conversation", "demo": "the product at work",
           "download": "the product in use on the go", "subscribe": "a regular ritual",
           "open-account": "a first step with money"}


@dataclass(frozen=True)
class PhotoDirection:
    """How the page's photographs look, and the grade every one of them
    shares. None of it applies when a client system forbids photography
    (`allowed` False)."""
    allowed: bool
    lightness: float
    temperature: float
    chroma: float
    contrast: float
    black_point: float
    grain: float
    energy: float
    spread: Mapping[str, float]
    subject: str
    framing: str
    kinds: Tuple[str, ...]
    words: Tuple[str, ...]

    def ranges(self) -> Dict[str, Tuple[float, float]]:
        """The page mean's acceptance range per measure: the target plus or
        minus GRADE_TOLERANCE."""
        target = {"lightness": self.lightness, "temperature": self.temperature,
                  "chroma": self.chroma}
        return {k: (round(target[k] - GRADE_TOLERANCE[k], 1),
                    round(target[k] + GRADE_TOLERANCE[k], 1)) for k in target}

    def query(self) -> str:
        """Words for a photo search: the subject, then the look."""
        return ", ".join((self.subject,) + self.words)


def _words(d: Dict[str, float]) -> Tuple[str, ...]:
    """The look in words, each read from a quantity by fixed cuts."""
    t, L, sd, c, bp, g, e = (d["temperature"], d["lightness"], d["contrast"], d["chroma"],
                             d["black_point"], d["grain"], d["energy"])
    return (
        "warm, golden light" if t >= 6 else "cool, blue light" if t <= -2 else "neutral daylight",
        "bright, high-key exposure" if L >= 60 else "low-key, moody exposure" if L <= 46
        else "balanced exposure",
        "hard light and deep shadows" if sd >= 22 else "soft, even light" if sd <= 15
        else "natural contrast",
        "vivid color" if c >= 22 else "muted, desaturated color" if c <= 12 else "natural color",
        "lifted, matte blacks" if bp >= 10 else "rich blacks",
        "visible film grain" if g >= 0.35 else "fine grain" if g >= 0.15
        else "clean, grain-free finish",
        "dynamic, caught mid-motion" if e >= 0.66 else "still and composed" if e <= 0.33
        else "a candid, natural moment")


def photo_direction(axes: AxisValues, brand_hex: str, product_type: Optional[str] = None,
                    age: str = "adults", primary_action: Optional[str] = None,
                    bans: Sequence[str] = (), forbidden: bool = False) -> PhotoDirection:
    """The photographs a page uses, from the axes and the brand color (the
    grade) and from the brief's structured fields (the subject). A brand's
    ban on a kind of photo (a name in PHOTO_KINDS) narrows the kinds;
    photography goes only when a client system forbids it."""
    _, bc, bh = hex_to_oklch(brand_hex)
    weight = character.hue_weight(bc)
    lean = (0.5 - character.coolness(bh)) * weight
    energy = character.energy(axes)
    d = {
        "temperature": round(-6 + 16 * axes.warmth + 4 * lean, 1),
        "lightness": round(38 + 30 * character.clamp(0.45 * (1 - axes.contrast)
                                                     + 0.3 * (1 - axes.formality)
                                                     + 0.25 * axes.warmth), 1),
        "contrast": round(12 + 14 * axes.contrast, 1),
        "chroma": round(6 + 20 * energy * (1 - 0.4 * axes.formality) + 4 * weight, 1),
        "black_point": round(2 + 14 * (1 - axes.contrast) * (0.5 + 0.5 * axes.warmth), 1),
        "grain": round(character.clamp(0.6 * axes.type_personality * (1 - 0.5 * axes.geometry)),
                       2),
        "energy": round(0.5 * energy + 0.5 * axes.motion, 2),
    }
    spread = {k: round(lo + (hi - lo) * (1 - axes.formality), 1)
              for k, (lo, hi) in GRADE_SPREAD.items()}
    who = PEOPLE.get(age, "adults")
    subject = SUBJECTS.get(product_type or "", "real people and places the product serves")
    subject += f"; people are {who}"
    if primary_action in MOMENTS:
        subject += f"; the moment: {MOMENTS[primary_action]}"
    framing = ("tight crops close to the subject" if axes.density >= 0.6 else
               "wide frames with room to breathe" if axes.density <= 0.4 else
               "medium frames") + (", centred and symmetric" if axes.formality >= 0.6 else
                                   ", off-centre and candid" if axes.formality <= 0.4 else "")
    kinds = tuple(k for k in PHOTO_KINDS if k not in set(bans))
    return PhotoDirection(not forbidden, d["lightness"], d["temperature"], d["chroma"],
                          d["contrast"], d["black_point"], d["grain"], d["energy"],
                          MappingProxyType(spread), subject, framing, kinds, _words(d))


def grade_problems(photos: Sequence[Tuple[str, float, float, float]],
                   direction: PhotoDirection) -> List[str]:
    """The grade lock, for lint --render: each (name, mean L*, mean b*, mean
    C*) of a page's photos sits within the direction's spread of the page's
    own mean, and the page's mean within the direction's ranges. One
    message per photo or measure out of line, naming it and the fix."""
    if not photos:
        return []
    keys = ("lightness", "temperature", "chroma")
    mean = {k: sum(p[i + 1] for p in photos) / len(photos) for i, k in enumerate(keys)}
    out = []
    for k, (lo, hi) in direction.ranges().items():
        if not lo <= mean[k] <= hi:
            out.append(f"the page's photos average {k} {mean[k]:.1f}, outside the direction's "
                       f"{lo:g} to {hi:g}; regrade them or choose photos nearer {k} "
                       f"{(lo + hi) / 2:g}")
    for name, *values in photos:
        for k, v in zip(keys, values):
            if abs(v - mean[k]) > direction.spread[k] + 1e-9:
                out.append(f"{name} has {k} {v:.1f}, {abs(v - mean[k]):.1f} from the page's mean "
                           f"{mean[k]:.1f}; every photo stays within {direction.spread[k]:g}, so "
                           "regrade it to match or replace it")
    return out


def photo_lines(direction: Optional[PhotoDirection]) -> List[str]:
    """The report's lines on photography."""
    if direction is None:
        return []
    if not direction.allowed:
        return ["The client's system forbids photography, so the pages carry none; imagery "
                "comes from generated art and the product itself."]
    r = direction.ranges()
    return [
        f"Subject: {direction.subject}. Framing: {direction.framing}.",
        f"Kinds: {', '.join(direction.kinds)}.",
        f"Look: {'; '.join(direction.words)}.",
        f"Grade: mean lightness {direction.lightness:g} (L*), temperature "
        f"{direction.temperature:+g} (b*), chroma {direction.chroma:g} (C*), contrast "
        f"{direction.contrast:g} (the spread of L*), black point {direction.black_point:g}, "
        f"grain {direction.grain:g}, energy {direction.energy:g}.",
        f"Grade lock: every photo within {direction.spread['lightness']:g} of the page's mean "
        f"lightness, {direction.spread['temperature']:g} of its temperature and "
        f"{direction.spread['chroma']:g} of its chroma; the page's mean within lightness "
        f"{r['lightness'][0]:g} to {r['lightness'][1]:g}, temperature {r['temperature'][0]:g} "
        f"to {r['temperature'][1]:g} and chroma {r['chroma'][0]:g} to {r['chroma'][1]:g}.",
        f"Search words: {direction.query()}.",
    ]


def generate_imagery(axes: AxisValues, brand_hex: str, body_px: int = 16) -> Generated:
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
    photo = photo_direction(axes, brand_hex)
    grades = (("lightness", photo.lightness), ("temperature", photo.temperature),
              ("chroma", photo.chroma), ("contrast", photo.contrast),
              ("black-point", photo.black_point), ("grain", photo.grain),
              ("energy", photo.energy),
              *((f"spread-{k}", v) for k, v in photo.spread.items()))
    for name, v in grades:
        ts.add(Token(f"imagery.grade.{name}", "number", v))
    for name, _ in grades:
        ts.add(Token(f"imagery.photo.{name}", "number", "{imagery.grade.%s}" % name,
                     layer="semantic"))
    shares = (("reach", scrim_reach(axes, body_px)), ("fade", SCRIM_FADE))
    for name, v in shares:
        ts.add(Token(f"imagery.share.{name}", "number", v))
    for name, _ in shares:
        ts.add(Token(f"imagery.scrim-{name}", "number", "{imagery.share.%s}" % name,
                     layer="semantic"))
    hw, hh = hero_ratio(axes)
    cw, ch = card_ratio(axes)
    return Generated(tokens=ts, notes=[
        f"imagery: hero {hw}:{hh}, card {cw}:{ch}, scrim alpha {alphas['standard'] / 255:.2f} "
        f"({alphas['high'] / 255:.2f} under high contrast)"])


PHOTO_ROLES = ("lightness", "temperature", "chroma", "contrast", "black-point", "grain",
               "energy", "spread-lightness", "spread-temperature", "spread-chroma")
ROLE_TYPES: Dict[str, str] = {
    **{f"imagery.photo.{name}": "number" for name in PHOTO_ROLES},
    "imagery.scrim-reach": "number", "imagery.scrim-fade": "number",
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


def _scrim_covers(ts: TokenSet, mode: str) -> List[str]:
    """A full-bleed hero's scrim holds its full strength over the region a
    two-line landing headline and what sits under it fill, on the desktop
    and the phone view."""
    from engine.foundations.values import dimension_px
    if not (_typed(ts, "imagery.scrim-reach") and ts.has("type.text.display")
            and ts.get("type.text.display").type == "typography"):
        return []
    reach = float(ts.resolve("imagery.scrim-reach"))
    display = ts.resolve("type.text.display")
    px, lh = dimension_px(display["fontSize"]), float(display["lineHeight"])
    phone = float(ts.resolve("type.phone.display")) if ts.has("type.phone.display") else 1.0
    out = []
    for (w, h), size in zip(HERO_VIEWS, (px, px * phone)):
        need = text_region(size, lh, h)
        if need > reach + 0.005:
            out.append(f"imagery.scrim-reach is {reach:g}, but a two-line headline at "
                       f"{size:.0f}px with what sits under it fills {need:.2f} of a {w} by {h} "
                       "hero from its bottom edge; point imagery.scrim-reach at a share of "
                       f"{need:.2f} or more")
    return out


CHECKS: Tuple[Check, ...] = (
    Check("scrim-text", "1.4.3", _scrim_text, axes=("contrast",)),
    Check("media-ratios", "system", _ratios,
          exempt_axes=(("contrast", "ratios never carry modes"),)),
    Check("duotone-range", "system", _duotone,
          exempt_axes=(("contrast", "the duotone pair never carries modes"),)),
    Check("scrim-covers-text", "system", _scrim_covers,
          exempt_axes=(("contrast", "the scrim's reach never carries modes"),)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_imagery(axes, inputs.brand_hex, inputs.audience.body_px)


FOUNDATION = Foundation(name="imagery", generate=_generate, checks=CHECKS,
                        role_types=ROLE_TYPES)
