"""A small catalog of open-license faces with measured metrics, and the
choice of a display, a text and a mono face from the axes.

Every face is on Google Fonts under the SIL Open Font License 1.1. Each
entry carries the metrics the page needs for a metric-matched fallback
(units per em, ascent, descent, line gap, x-height, cap height, and the
average advance of Latin letters weighted by English letter frequency and,
for Arabic faces, of the Arabic letters), the weights it ships, the Arabic
face drawn to sit beside it, and where it sits on the axes (formality,
warmth, roundness, type personality, contrast). Metrics were measured from
the published font files with fontTools.

choose(axes) picks, for each role, the face nearest the axes by weighted
distance, ties broken by name: never an industry or keyword table. The
display face is never the text face.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Mapping, Optional, Tuple

from engine.foundations import character
from engine.synthesizer.axes import AxisValues

LICENSE = "OFL-1.1"
CDN = "https://fonts.googleapis.com/css2"


@dataclass(frozen=True)
class Metrics:
    """Measured in font units. latin_avg and arabic_avg are average
    advances (Latin weighted by English letter frequency, space included;
    Arabic over the 28 letters and space); arabic_body is the median top
    of the Arabic letters that have no ascender."""
    upm: int
    ascent: int
    descent: int
    line_gap: int
    x_height: int
    cap_height: int
    latin_avg: Optional[float]
    arabic_avg: Optional[float]
    arabic_body: Optional[float]


@dataclass(frozen=True)
class Face:
    family: str
    role: str                       # "text", "display", "mono" or "arabic"
    generic: str                    # the CSS generic family it falls back to
    weights: Tuple[int, int]        # lightest and heaviest weight shipped
    variable: bool                  # one file holds every weight
    metrics: Metrics
    # formality, warmth, roundness, type personality, contrast, 0 to 1
    place: Tuple[float, float, float, float, float] = (0.5, 0.5, 0.5, 0.5, 0.5)
    arabic: str = ""                # the Arabic face drawn to sit beside it

    @property
    def slug(self) -> str:
        return self.family.lower().replace(" ", "-")

    def clamp(self, weight: int) -> int:
        return max(self.weights[0], min(self.weights[1], weight))


def _m(*v: Optional[float]) -> Metrics:
    return Metrics(*v)  # type: ignore[arg-type]


FACES: Tuple[Face, ...] = (
    # text faces
    Face("IBM Plex Sans", "text", "sans-serif", (100, 700), True,
         _m(1000, 1025, 275, 0, 516, 698, 454.1, None, None),
         (0.8, 0.35, 0.3, 0.45, 0.45), "IBM Plex Sans Arabic"),
    Face("Source Sans 3", "text", "sans-serif", (200, 900), True,
         _m(1000, 1024, 400, 0, 478, 660, 403.4, None, None),
         (0.6, 0.6, 0.45, 0.8, 0.4), "Noto Naskh Arabic"),
    Face("Manrope", "text", "sans-serif", (200, 800), True,
         _m(2000, 2132, 600, 0, 1080, 1440, 899.3, None, None),
         (0.5, 0.4, 0.6, 0.1, 0.5), "Readex Pro"),
    Face("Nunito Sans", "text", "sans-serif", (200, 1000), True,
         _m(1000, 1011, 353, 0, 484, 705, 439.4, None, None),
         (0.3, 0.8, 0.85, 0.55, 0.4), "Tajawal"),
    Face("Noto Sans", "text", "sans-serif", (100, 900), True,
         _m(1000, 1069, 293, 0, 536, 714, 479.0, None, None),
         (0.55, 0.5, 0.45, 0.5, 0.45), "Noto Sans Arabic"),
    # display faces
    Face("Fraunces", "display", "serif", (100, 900), True,
         _m(2000, 1956, 510, 0, 964, 1400, 1042.1, None, None),
         (0.35, 0.9, 0.75, 0.9, 0.7), "El Messiri"),
    Face("Playfair Display", "display", "serif", (400, 900), True,
         _m(1000, 1082, 251, 0, 514, 708, 456.4, None, None),
         (0.9, 0.55, 0.35, 0.85, 0.85), "Amiri"),
    Face("Space Grotesk", "display", "sans-serif", (300, 700), True,
         _m(1000, 984, 292, 0, 486, 700, 497.7, None, None),
         (0.55, 0.2, 0.3, 0.05, 0.65), "Readex Pro"),
    Face("Bricolage Grotesque", "display", "sans-serif", (200, 800), True,
         _m(1000, 930, 270, 0, 528, 660, 453.6, None, None),
         (0.15, 0.7, 0.55, 0.5, 0.85), "Baloo Bhaijaan 2"),
    Face("Sora", "display", "sans-serif", (100, 800), True,
         _m(1000, 970, 290, 0, 534, 730, 512.1, None, None),
         (0.65, 0.35, 0.55, 0.15, 0.5), "Alexandria"),
    Face("Outfit", "display", "sans-serif", (100, 900), True,
         _m(1000, 1000, 260, 0, 460, 676, 444.0, None, None),
         (0.4, 0.6, 0.8, 0.3, 0.45), "Alexandria"),
    Face("Newsreader", "display", "serif", (200, 800), True,
         _m(2000, 1470, 530, 0, 852, 1340, 816.1, None, None),
         (0.8, 0.6, 0.4, 1.0, 0.5), "Noto Naskh Arabic"),
    Face("Baloo 2", "display", "sans-serif", (400, 800), True,
         _m(1000, 1078, 524, 0, 460, 602, 435.4, None, None),
         (0.05, 0.95, 1.0, 0.6, 0.6), "Baloo Bhaijaan 2"),
    # mono faces
    Face("IBM Plex Mono", "mono", "monospace", (100, 700), False,
         _m(1000, 1025, 275, 0, 516, 698, 600.0, None, None),
         (0.75, 0.45, 0.35, 0.5, 0.4)),
    Face("JetBrains Mono", "mono", "monospace", (100, 800), True,
         _m(1000, 1020, 300, 0, 550, 730, 600.0, None, None),
         (0.5, 0.3, 0.45, 0.1, 0.55)),
    # Arabic partners
    Face("IBM Plex Sans Arabic", "arabic", "sans-serif", (100, 700), False,
         _m(1000, 1085, 415, 0, 516, 698, 454.1, 675.7, 409.5)),
    Face("Noto Naskh Arabic", "arabic", "serif", (400, 700), True,
         _m(1000, 1069, 634, 0, 536, 714, 480.4, 644.4, 364.0)),
    Face("Readex Pro", "arabic", "sans-serif", (160, 700), True,
         _m(1000, 1000, 250, 0, 525, 700, 488.5, 763.9, 438.0)),
    Face("Tajawal", "arabic", "sans-serif", (200, 900), False,
         _m(1000, 643, 357, 200, 454, 633, 427.3, 716.4, 440.0)),
    Face("Noto Sans Arabic", "arabic", "sans-serif", (100, 900), True,
         _m(1000, 1374, 738, 0, 536, 714, 479.0, 727.0, 403.0)),
    Face("El Messiri", "arabic", "sans-serif", (400, 700), True,
         _m(1000, 1019, 544, 0, 480, 660, 430.5, 696.6, 480.0)),
    Face("Amiri", "arabic", "serif", (400, 700), False,
         _m(1000, 1124, 634, 0, 433, 646, 405.1, 673.3, 376.0)),
    Face("Baloo Bhaijaan 2", "arabic", "sans-serif", (400, 800), True,
         _m(1000, 1080, 632, 0, 460, 602, 435.4, 661.8, 379.5)),
    Face("Alexandria", "arabic", "sans-serif", (100, 900), True,
         _m(1000, 968, 251, 0, 531, 700, 509.3, 773.1, 514.0)),
)
BY_FAMILY: Mapping[str, Face] = MappingProxyType({f.family: f for f in FACES})

# The system faces a metric-matched fallback points at, measured the same
# way: (local() names in order, metrics).
FALLBACKS: Mapping[str, Tuple[Tuple[str, ...], Metrics]] = MappingProxyType({
    "sans-serif": (("Arial", "Helvetica", "Liberation Sans"),
                   _m(2048, 1854, 434, 67, 1062, 1467, 915.5, None, None)),
    "serif": (("Times New Roman", "Times", "Liberation Serif"),
              _m(2048, 1825, 443, 87, 916, 1356, 829.8, None, None)),
    "monospace": (("Courier New", "Courier", "Liberation Mono"),
                  _m(2048, 1705, 615, 0, 866, 1170, 1229.0, None, None)),
    "arabic": (("Tahoma", "Geeza Pro", "Noto Sans Arabic", "Arial"),
               _m(2048, 2049, 423, 0, 1117, 1489, 921.3, 1403.6, 810.0)),
})

# How much each place dimension counts when choosing a face for a role:
# formality, warmth, roundness, type personality, contrast.
WEIGHTS: Mapping[str, Tuple[float, float, float, float, float]] = MappingProxyType({
    "text": (1.0, 1.0, 0.5, 2.0, 0.25),
    "display": (1.5, 1.0, 1.0, 1.5, 1.0),
    "mono": (1.0, 1.0, 0.5, 2.0, 0.5),
})
# How far an Arabic face is set above the Latin size at the same step.
ARABIC_SCALE = (1.05, 1.15)


def place_of(axes: AxisValues) -> Tuple[float, float, float, float, float]:
    return (axes.formality, axes.warmth, character.roundness(axes), axes.type_personality,
            axes.contrast)


def distance(face: Face, axes: AxisValues) -> float:
    w = WEIGHTS[face.role]
    return sum(k * (a - b) ** 2 for k, a, b in zip(w, place_of(axes), face.place))


@dataclass(frozen=True)
class Choice:
    text: Face
    display: Face
    mono: Face
    arabic: Face
    arabic_display: Face

    def faces(self) -> Tuple[Face, ...]:
        """Every face the system names, each once, in role order."""
        out = []
        for f in (self.display, self.text, self.mono, self.arabic_display, self.arabic):
            if f not in out:
                out.append(f)
        return tuple(out)


def nearest(role: str, axes: AxisValues, exclude: Tuple[str, ...] = ()) -> Face:
    candidates = [f for f in FACES if f.role == role and f.family not in exclude]
    return min(candidates, key=lambda f: (round(distance(f, axes), 9), f.family))


def choose(axes: AxisValues) -> Choice:
    text = nearest("text", axes)
    display = nearest("display", axes, exclude=(text.family,))
    return Choice(text=text, display=display, mono=nearest("mono", axes),
                  arabic=BY_FAMILY[text.arabic], arabic_display=BY_FAMILY[display.arabic])


def arabic_scale(latin: Face, arabic: Face) -> float:
    """How much larger the Arabic face is set than the Latin one at the
    same step: half the gap between the Latin x-height and the Arabic
    letter body, both per em, so the two read at one size, within
    ARABIC_SCALE."""
    lx = latin.metrics.x_height / latin.metrics.upm
    ab = (arabic.metrics.arabic_body or 0) / arabic.metrics.upm
    raw = 1.0 + 0.5 * (lx / ab - 1.0) if ab else ARABIC_SCALE[0]
    return round(max(ARABIC_SCALE[0], min(ARABIC_SCALE[1], raw)), 3)


def fallback_overrides(face: Face) -> Dict[str, str]:
    """The @font-face descriptors that make a local system face take the
    web face's width and vertical metrics, so text does not shift when the
    web face arrives: size-adjust, ascent-override, descent-override and
    line-gap-override, as percentages."""
    kind = "arabic" if face.role == "arabic" else face.generic
    _, fb = FALLBACKS[kind]
    m = face.metrics
    if kind == "arabic":
        ratio = (m.arabic_avg or 0) / m.upm / ((fb.arabic_avg or 1) / fb.upm)
    else:
        ratio = (m.latin_avg or 0) / m.upm / ((fb.latin_avg or 1) / fb.upm)

    def pct(v: float) -> str:
        return f"{v * 100:.2f}%"

    return {"size-adjust": pct(ratio), "ascent-override": pct(m.ascent / m.upm / ratio),
            "descent-override": pct(m.descent / m.upm / ratio),
            "line-gap-override": pct(m.line_gap / m.upm / ratio)}


def fallback_name(face: Face) -> str:
    return f"{face.family} Fallback"


def css2_family(face: Face, weights: Tuple[int, ...]) -> str:
    """The family parameter for the Google Fonts CSS2 API: a weight range
    for a variable face, the weights used for a static one."""
    name = face.family.replace(" ", "+")
    if face.variable:
        return f"{name}:wght@{face.weights[0]}..{face.weights[1]}"
    return f"{name}:wght@" + ";".join(str(w) for w in sorted(set(weights)))
