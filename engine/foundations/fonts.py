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

When the brief says what the product is (audience.BOOK_DEPTH), one more
dimension counts: how bookish a face is (a serif is, a sans is not)
against a book target, the depth times the mean of type personality and
formality (book_target). An app aims at 0, so its display face leans sans
and its Arabic face moves off a book partner to the nearest interface face;
an editorial product aims high, so a humanist, formal brief may take a
serif. Without a product type the dimension counts for nothing and every
Arabic face is the one drawn beside its Latin face.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict, List, Mapping, Optional, Tuple

from engine.foundations import character
from engine.synthesizer.axes import AxisValues

if TYPE_CHECKING:  # pragma: no cover
    from engine.foundations.tokens import TokenSet

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
    # A static face: every weight it ships, one file each. Empty for a
    # variable face, which ships every weight between its two ends.
    stops: Tuple[int, ...] = ()

    @property
    def slug(self) -> str:
        return self.family.lower().replace(" ", "-")

    def clamp(self, weight: int) -> int:
        """The weight the face draws for `weight`: within the range of a
        variable face; the nearest weight a static face ships, the heavier
        of two at the same distance."""
        if self.stops:
            return min(self.stops, key=lambda s: (abs(s - weight), -s))
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
         (0.75, 0.45, 0.35, 0.5, 0.4), stops=(100, 200, 300, 400, 500, 600, 700)),
    Face("JetBrains Mono", "mono", "monospace", (100, 800), True,
         _m(1000, 1020, 300, 0, 550, 730, 600.0, None, None),
         (0.5, 0.3, 0.45, 0.1, 0.55)),
    # Arabic partners
    Face("IBM Plex Sans Arabic", "arabic", "sans-serif", (100, 700), False,
         _m(1000, 1085, 415, 0, 516, 698, 454.1, 675.7, 409.5),
         stops=(100, 200, 300, 400, 500, 600, 700)),
    Face("Noto Naskh Arabic", "arabic", "serif", (400, 700), True,
         _m(1000, 1069, 634, 0, 536, 714, 480.4, 644.4, 364.0)),
    Face("Readex Pro", "arabic", "sans-serif", (160, 700), True,
         _m(1000, 1000, 250, 0, 525, 700, 488.5, 763.9, 438.0)),
    Face("Tajawal", "arabic", "sans-serif", (200, 900), False,
         _m(1000, 643, 357, 200, 454, 633, 427.3, 716.4, 440.0),
         stops=(200, 300, 400, 500, 700, 800, 900)),
    Face("Noto Sans Arabic", "arabic", "sans-serif", (100, 900), True,
         _m(1000, 1374, 738, 0, 536, 714, 479.0, 727.0, 403.0)),
    Face("El Messiri", "arabic", "sans-serif", (400, 700), True,
         _m(1000, 1019, 544, 0, 480, 660, 430.5, 696.6, 480.0)),
    Face("Amiri", "arabic", "serif", (400, 700), False,
         _m(1000, 1124, 634, 0, 433, 646, 405.1, 673.3, 376.0), stops=(400, 700)),
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
# How much the book dimension counts against the place (book_cost), and what
# an Arabic face that is not the one drawn beside the Latin face costs
# (arabic_cost). Both apply only when the brief gives a product type.
BOOK_WEIGHT = 2.0
PARTNER_GAP = 0.5
# How far an Arabic face is set above the Latin size at the same step.
ARABIC_SCALE = (1.05, 1.15)


def place_of(axes: AxisValues) -> Tuple[float, float, float, float, float]:
    return (axes.formality, axes.warmth, character.roundness(axes), axes.type_personality,
            axes.contrast)


def distance(face: Face, axes: AxisValues) -> float:
    w = WEIGHTS[face.role]
    return sum(k * (a - b) ** 2 for k, a, b in zip(w, place_of(axes), face.place))


def bookish(face: Face) -> float:
    """1 for a face drawn for books (a serif, in Latin or Arabic), 0 for an
    interface face."""
    return 1.0 if face.generic == "serif" else 0.0


def book_target(axes: AxisValues, depth: float) -> float:
    """How bookish the faces should be, 0 to 1: the product's book depth
    times the mean of type personality and formality. Continuous in both
    axes; 0 for an app or software, whatever the axes."""
    return character.clamp(depth * 0.5 * (axes.type_personality + axes.formality))


def book_cost(face: Face, axes: AxisValues, depth: Optional[float]) -> float:
    """BOOK_WEIGHT times the squared gap between the face's bookishness and
    the book target; 0 when the brief gives no product type."""
    if depth is None:
        return 0.0
    return BOOK_WEIGHT * (bookish(face) - book_target(axes, depth)) ** 2


def _arabic_place(face: Face) -> Tuple[float, ...]:
    """An Arabic face's place: the mean place of the Latin faces drawn to
    sit beside it."""
    partners = [f.place for f in FACES if f.arabic == face.family]
    if not partners:
        return (0.5,) * 5
    return tuple(sum(p[i] for p in partners) / len(partners) for i in range(5))


def arabic_cost(face: Face, latin: Face, axes: AxisValues, depth: float) -> float:
    """What an Arabic face costs beside a Latin one: PARTNER_GAP unless it
    is the face drawn beside it, its place's weighted distance from the
    Latin face's place, its book_cost, and BOOK_WEIGHT times the squared
    gap between its bookishness and the Latin face's, so a sans Latin face
    never pairs with a book Arabic face."""
    w = WEIGHTS["text"]
    gap = sum(k * (a - b) ** 2 for k, a, b in zip(w, _arabic_place(face), latin.place))
    return (0.0 if face.family == latin.arabic else PARTNER_GAP) + gap \
        + book_cost(face, axes, depth) + BOOK_WEIGHT * (bookish(face) - bookish(latin)) ** 2


def arabic_for(latin: Face, axes: AxisValues, depth: Optional[float] = None) -> Face:
    """The Arabic face beside a Latin face: the one drawn beside it when the
    brief gives no product type, else the lowest arabic_cost, ties by name."""
    if depth is None:
        return BY_FAMILY[latin.arabic]
    candidates = [f for f in FACES if f.role == "arabic"]
    return min(candidates, key=lambda f: (round(arabic_cost(f, latin, axes, depth), 9),
                                          f.family))


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


def nearest(role: str, axes: AxisValues, exclude: Tuple[str, ...] = (),
            depth: Optional[float] = None) -> Face:
    candidates = [f for f in FACES if f.role == role and f.family not in exclude]
    return min(candidates, key=lambda f: (round(distance(f, axes) + book_cost(f, axes, depth),
                                                9), f.family))


def choose(axes: AxisValues, depth: Optional[float] = None) -> Choice:
    """The faces for these axes; `depth` is the product's book depth
    (audience.Audience.book_depth), None when the brief does not say."""
    text = nearest("text", axes, depth=depth)
    display = nearest("display", axes, exclude=(text.family,), depth=depth)
    return Choice(text=text, display=display, mono=nearest("mono", axes),
                  arabic=arabic_for(text, axes, depth),
                  arabic_display=arabic_for(display, axes, depth))


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
    for a variable face; for a static one, the weights used, each snapped
    to one the face ships, since the API refuses the whole link for a
    weight a static family does not have."""
    name = face.family.replace(" ", "+")
    if face.variable:
        return f"{name}:wght@{face.weights[0]}..{face.weights[1]}"
    return f"{name}:wght@" + ";".join(str(w) for w in sorted({face.clamp(w) for w in weights}))


# The style name a font file gives each weight, in its full name and its
# PostScript name.
STYLE_NAMES: Mapping[int, str] = MappingProxyType({
    100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium",
    600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"})


def local_names(face: Face, weight: int) -> Tuple[str, ...]:
    """The names local() looks for to find one installed weight of a
    static face: its full name and its PostScript name ("Tajawal Bold",
    "Tajawal-Bold"). A family name alone would match the Regular file at
    every weight. A variable face gets none: an installed copy may hold a
    single weight."""
    if face.variable:
        return ()
    style = STYLE_NAMES[face.clamp(weight)]
    return (f"{face.family} {style}", f"{face.family.replace(' ', '')}-{style}")


# The Arabic blocks an Arabic face covers, so a page loads it only when it
# shows Arabic.
ARABIC_RANGE = "U+0600-06FF, U+0750-077F, U+08A0-08FF, U+FB50-FDFF, U+FE70-FEFF"


def faces_in(ts: "TokenSet") -> List[Tuple[str, Face]]:
    """(face token, face) for every type.face.* token whose first family is
    in the catalog, in token order, each face once."""
    out: List[Tuple[str, Face]] = []
    seen = set()
    for t in ts.tokens():
        if t.path.startswith("type.face.") and t.type == "fontFamily":
            first = t.value[0] if isinstance(t.value, list) else t.value
            face = BY_FAMILY.get(first)
            if face and face.family not in seen:
                seen.add(face.family)
                out.append((t.path, face))
    return out


def weights_in(ts: "TokenSet") -> Tuple[int, ...]:
    return tuple(sorted(int(t.value) for t in ts.tokens()
                        if t.path.startswith("type.weight.") and t.type == "fontWeight"))


def cdn_url(ts: "TokenSet") -> str:
    """One Google Fonts CSS2 link for every face the system names."""
    used = weights_in(ts)
    params = "&".join("family=" + css2_family(f, tuple(f.clamp(w) for w in used))
                      for _, f in faces_in(ts))
    return f"{CDN}?{params}&display=swap"


_PRECONNECT = ('<link rel="preconnect" href="https://fonts.googleapis.com">',
               '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')


def link_tags(ts: "TokenSet") -> List[str]:
    """The page head tags that load every face from Google Fonts."""
    return [*_PRECONNECT, f'<link rel="stylesheet" href="{cdn_url(ts)}">']


def fonts_css(ts: "TokenSet") -> str:
    """fonts.css: a metric-matched fallback face per face, and nothing
    that loads the faces themselves, so the file is the same whichever
    way the page loads them (the Google Fonts link, or
    fonts-self-host.css). The Arabic fallbacks cover only the Arabic
    blocks, so Latin letters, digits and spaces in an Arabic run reach the
    Latin face next in the stack."""
    lines = [
        "/* Metric-matched fallback faces for this design system. Each gives a",
        "   system font the web face's width and height, so text keeps its size",
        "   and line breaks while the face loads. This file does not load the",
        "   faces; load them one of two ways, each together with this file, and",
        "   link both before tokens.css. Edit neither file.",
        "   1. From Google Fonts: add to the page head",
        *[f"      {tag}" for tag in link_tags(ts)],
        "   2. Self-hosted: link fonts-self-host.css and put the files it names",
        "      in a fonts/ folder beside it.",
        "   Every face is under the SIL Open Font License 1.1. */",
    ]
    for _, face in faces_in(ts):
        kind = "arabic" if face.role == "arabic" else face.generic
        names = FALLBACKS[kind][0]
        lines += ["", "@font-face {", f'  font-family: "{fallback_name(face)}";',
                  "  src: " + ", ".join(f'local("{n}")' for n in names) + ";"]
        lines += [f"  {k}: {v};" for k, v in fallback_overrides(face).items()]
        if kind == "arabic":
            lines.append(f"  unicode-range: {ARABIC_RANGE};")
        lines.append("}")
    return "\n".join(lines) + "\n"


def self_host_css(ts: "TokenSet") -> str:
    """fonts-self-host.css: an @font-face per face and weight file, loading
    from the fonts/ folder beside it with font-display swap. A static face
    looks for the reader's installed copy of each weight first, by that
    weight's own names; a variable face loads its one file. Arabic faces
    cover only the Arabic blocks, so a page without Arabic never downloads
    them."""
    used = weights_in(ts)
    lines = [
        "/* The faces of this design system, self-hosted. Link this file and",
        "   fonts.css before tokens.css, and put the WOFF2 files named below in a",
        "   fonts/ folder beside this file: convert the TTF files from each",
        "   family's Google Fonts download, and give each the name below. Edit",
        "   nothing here. To load the faces from Google Fonts instead, leave this",
        "   file out and use the link in fonts.css.",
        "   Every face is under the SIL Open Font License 1.1. */",
    ]
    for _, face in faces_in(ts):
        if face.variable:
            srcs = [(f"fonts/{face.slug}.woff2", f"{face.weights[0]} {face.weights[1]}", ())]
        else:
            srcs = [(f"fonts/{face.slug}-{w}.woff2", str(w), local_names(face, w))
                    for w in sorted({face.clamp(w) for w in used})]
        for url, weight, names in srcs:
            src = ", ".join([*(f'local("{n}")' for n in names), f'url("{url}") format("woff2")'])
            lines += ["", "@font-face {", f'  font-family: "{face.family}";', f"  src: {src};",
                      f"  font-weight: {weight};", "  font-style: normal;",
                      "  font-display: swap;"]
            if face.role == "arabic":
                lines.append(f"  unicode-range: {ARABIC_RANGE};")
            lines.append("}")
    return "\n".join(lines) + "\n"


def loading_lines(ts: "TokenSet") -> List[str]:
    """The report's lines on the faces: each face, what it is for, the
    weights the tokens use and its license."""
    used = weights_in(ts)
    role_words = {"type.face.display": "display", "type.face.text": "text",
                  "type.face.mono": "mono", "type.face.arabic": "Arabic text",
                  "type.face.arabic-display": "Arabic display"}
    roles: Dict[str, List[str]] = {}
    for t in ts.tokens():
        if t.path in role_words:
            first = t.value[0] if isinstance(t.value, list) else t.value
            roles.setdefault(first, []).append(role_words[t.path])
    out = []
    for _, face in faces_in(ts):
        ws = sorted({face.clamp(w) for w in used})
        out.append(f"{face.family} ({' and '.join(roles.get(face.family, []))}), weights "
                   f"{', '.join(str(w) for w in ws)}, {LICENSE}.")
    return out
