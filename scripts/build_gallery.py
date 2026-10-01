"""Build the gallery: one foundations system per brand spec.

    python scripts/build_gallery.py           # write data/gallery/<id>.json
    python scripts/build_gallery.py --check   # name every entry that drifted

For every spec in data/brands (every JSON file whose name does not start
with "_") the script writes data/gallery/<id>.json with the spec's id and
name, the brand color, the seven axes, whether the Arabic face and scale
are built, the axes source in one plain sentence, and a digest of the built
tokens so a change in the engine shows in review. Each entry is built with
make_system, which validates and gates every mode (light, dark, high
contrast, compact, rtl and reduced motion); an entry that fails is never
written, and the script exits 1 naming the spec and the finding. The output
is deterministic: sorted keys, ASCII, a final newline, no timestamps.

Only the spec's design_language places anything. Its other fields (prose,
signals, pages, whatever else it holds) are never read.

The brand color.
The primary carries the main action when it reaches 3:1 against the canvas
(WCAG 1.4.11, the contrast a control needs to be seen). When it does not,
the brand color is the accent (any color_accent field holding one color)
with the most contrast against the canvas, if that accent reaches 3:1.
Otherwise the primary stays, and the engine derives the action color from
it. The canvas is color_canvas, or white when the spec states none. A color
written with an alpha channel (#RRGGBBAA) is read over the canvas.

The axes.
Each axis is a continuous function of the spec's own facts. A fact the
spec does not state leaves its axis at 0.5, and the source sentence says
so. clamp() keeps a value within 0 to 1. chroma(c) is a color's sRGB
chroma, its largest channel minus its smallest over 255 (0 for a grey, 1
for a pure hue); it is used instead of OKLCH chroma because it moves by at
most 1/255 when a channel moves by one step, where OKLCH chroma jumps near
black. Hue is the OKLCH hue, and coolness() is the engine's own
(character.py): 1 near the cool hue anchor, 0 on the warm side. A hue only
counts in proportion to its chroma, so a grey says nothing about warmth.

- warmth = clamp(0.5 + 0.7 * lean(primary, 0.4) + 0.3 * lean(canvas, 0.1)),
  where lean(c, full) = (0.5 - coolness(hue)) * clamp(chroma(c) / full):
  the primary's hue counts fully from chroma 0.4, a tinted canvas's from
  chroma 0.1.
- contrast = clamp(0.15 + 0.35 * ln(ratio) / ln(21) + 0.35 * loud
  + 0.3 * (1 - depth)), where ratio is the ink's contrast ratio on the
  canvas, loud is the highest chroma among the primary and the accents,
  and depth = ln(canvas contrast on black) / ln(21), 0 for a black page and
  1 for a white one: strong ink, a loud color and a dark page each add
  drama.
- density = clamp(0.5 - 0.25 * log2(base / 4)), where base is the spacing
  base in px (the first number of "spacing"): 4 sits at 0.5, 8 at 0.25,
  2 at 0.75.
- geometry = 1 - exp(-mean(min(r, 32)) / 14) over the stated radii in px;
  a pill radius such as 999 counts as 32, beyond which a corner no longer
  changes how a control reads.
- formality = (prior + sum of known faces' formality) / (1 + known), where
  prior = clamp(1 - 0.7 * chroma(primary) - 0.3 * clamp(chroma(ink) /
  0.4)): a restrained palette with neutral ink reads formal. A known face
  is a display or body face found in the engine's measured face catalog
  (engine/foundations/fonts.py), which brings its measured place.
- motion = the mean of clamp(ln(d / 100) / ln(12)) over every duration d
  in ms the motion signature states in numbers (ms, s or seconds): 100ms
  sits at 0 and 1200ms and longer at 1, so a spec that states only quick
  hovers is still and one that states long fades or loops is kinetic.
- type_personality = (0.5 + sum of known faces' type personality) /
  (1 + known): the faces' measured place where the catalog has them.

Axes are rounded to four decimals before the build, so the entry builds
exactly what it records. The Arabic face and scale are built for every
entry (arabic true), so the rtl mode is gated with its own faces.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.foundations import character  # noqa: E402
from engine.foundations.color_math import (  # noqa: E402
    contrast, hex_to_oklch, hex_to_rgb, rgb_to_hex)
from engine.foundations.emit import make_system  # noqa: E402
from engine.foundations.fonts import FACES  # noqa: E402
from engine.synthesizer.axes import AXIS_NAMES, AxisValues  # noqa: E402

SPECS = ROOT / "data" / "brands"
GALLERY = ROOT / "data" / "gallery"
ACTION_RATIO = 3.0
WHITE = "#FFFFFF"
# Constants of the formulas in the module docstring.
PRIMARY_FULL, CANVAS_FULL, INK_FULL = 0.4, 0.1, 0.4
RADIUS_CAP = 32.0
RADIUS_SCALE = 14.0
MOTION_FLOOR_MS, MOTION_TOP_MS = 100.0, 1200.0
# A number in seconds reads as a duration only up to this many seconds: an
# interface moves in well under that, so "911s" in prose is a count, not a
# duration.
SECONDS_CAP = 10.0
_DURATION = re.compile(r"(\d+(?:\.\d+)?)\s*-?\s*(ms|seconds?|secs?|s)\b", re.I)
_NUMBER = re.compile(r"\d+(?:\.\d+)?")
_COLOR = re.compile(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})")
_FACES = {f.family.lower(): f for f in FACES if f.role != "arabic"}
# Spec paths shown in messages and in each entry.
_SPEC_DIR = "data/brands"


class GalleryError(ValueError):
    """A spec the gallery cannot read or build; the message names the spec,
    the field and the fix."""


# ---------------------------------------------------------------- reading


def load_specs(folder: Path = SPECS) -> List[Tuple[str, Dict[str, Any]]]:
    """(id, spec) for every spec file, in file name order."""
    out = []
    for f in sorted(folder.glob("*.json")):
        if f.name.startswith("_"):
            continue
        spec = json.loads(f.read_text(encoding="utf-8"))
        if spec.get("id") != f.stem:
            raise GalleryError(f"{_SPEC_DIR}/{f.name}: id is {spec.get('id')!r}; set it to "
                               f"{f.stem!r}, the file's name")
        out.append((f.stem, spec))
    return out


def _sid(spec: Mapping[str, Any]) -> str:
    return str(spec.get("id", "the spec"))


def _design(spec: Mapping[str, Any]) -> Mapping[str, Any]:
    dl = spec.get("design_language")
    if not isinstance(dl, Mapping):
        raise GalleryError(f"{_sid(spec)}: design_language is missing; add an object with "
                           "color_primary and the other design facts")
    return dl


def _color(value: Any, over: str = WHITE) -> Optional[str]:
    """A color as #RRGGBB, or None when the value is not one color. An
    alpha channel is read over `over`."""
    if not isinstance(value, str):
        return None
    m = _COLOR.fullmatch(value.strip())
    if not m:
        return None
    digits = m.group(1)
    if len(digits) != 8:
        return rgb_to_hex(hex_to_rgb("#" + digits))
    alpha = int(digits[6:], 16) / 255.0
    top, under = hex_to_rgb("#" + digits[:6]), hex_to_rgb(over)
    return rgb_to_hex(tuple(round(a * alpha + b * (1 - alpha)) for a, b in zip(top, under)))


def _canvas(dl: Mapping[str, Any]) -> str:
    return _color(dl.get("color_canvas")) or WHITE


def _primary(spec: Mapping[str, Any]) -> str:
    dl = _design(spec)
    hex_ = _color(dl.get("color_primary"), _canvas(dl))
    if hex_ is None:
        raise GalleryError(f"{_sid(spec)}: design_language.color_primary is "
                           f"{dl.get('color_primary')!r}, which is not one color; write it as "
                           "#RRGGBB, for example #2F6B4F")
    return hex_


def _accents(dl: Mapping[str, Any]) -> List[Tuple[str, str]]:
    """(field, color) for every color_accent field holding one color, in
    field name order."""
    canvas = _canvas(dl)
    out = []
    for key in sorted(dl):
        if key.startswith("color_accent"):
            hex_ = _color(dl[key], canvas)
            if hex_ is not None:
                out.append((key, hex_))
    return out


def brand_hex(spec: Mapping[str, Any]) -> Tuple[str, str]:
    """The brand color and the sentence that says why (module docstring)."""
    dl = _design(spec)
    primary, canvas = _primary(spec), _canvas(dl)
    ratio = contrast(primary, canvas)
    if ratio >= ACTION_RATIO:
        return primary, (f"The primary {primary} reaches {ratio:.2f}:1 on the canvas {canvas}, "
                         f"at least the 3:1 a control needs, so it carries the action.")
    ranked = sorted(((contrast(h, canvas), k, h) for k, h in _accents(dl)),
                    key=lambda x: (-x[0], x[1]))
    if ranked and ranked[0][0] >= ACTION_RATIO:
        best, key, hex_ = ranked[0]
        return hex_, (f"The primary {primary} reaches only {ratio:.2f}:1 on the canvas {canvas}, "
                      f"under the 3:1 a control needs, so the accent {key} {hex_} at "
                      f"{best:.2f}:1 carries the action.")
    return primary, (f"The primary {primary} reaches only {ratio:.2f}:1 on the canvas {canvas} "
                     f"and no accent reaches 3:1, so the primary stays and the engine derives "
                     f"the action color from it.")


# ---------------------------------------------------------------- axes


def _clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


def _chroma(hex_: str) -> float:
    """sRGB chroma: the largest channel minus the smallest, over 255."""
    rgb = hex_to_rgb(hex_)
    return (max(rgb) - min(rgb)) / 255.0


def _lean(hex_: str, full: float) -> float:
    _, _, hue = hex_to_oklch(hex_)
    return (0.5 - character.coolness(hue)) * _clamp(_chroma(hex_) / full)


def _radii(dl: Mapping[str, Any]) -> List[float]:
    raw = dl.get("radius")
    if not isinstance(raw, list):
        return []
    return [float(r) for r in raw if isinstance(r, (int, float)) and not isinstance(r, bool)
            and r >= 0]


def _spacing_base(dl: Mapping[str, Any]) -> Optional[float]:
    raw = dl.get("spacing")
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return float(raw) if raw > 0 else None
    m = _NUMBER.search(raw) if isinstance(raw, str) else None
    return float(m.group()) if m and float(m.group()) > 0 else None


def _durations(dl: Mapping[str, Any]) -> List[float]:
    text = dl.get("motion_signature")
    if not isinstance(text, str):
        return []
    out = []
    for number, unit in _DURATION.findall(text):
        seconds = unit.lower() != "ms"
        if seconds and float(number) > SECONDS_CAP:
            continue
        ms = float(number) * (1000.0 if seconds else 1.0)
        if ms > 0:
            out.append(ms)
    return out


def _faces(dl: Mapping[str, Any]) -> List[Any]:
    """The catalog faces among the display and body faces, each once."""
    faces = dl.get("type")
    out: List[Any] = []
    if isinstance(faces, Mapping):
        for role in ("display", "body"):
            name = faces.get(role)
            face = _FACES.get(name.strip().lower()) if isinstance(name, str) else None
            if face is not None and face not in out:
                out.append(face)
    return out


def _ms(values: Sequence[float]) -> str:
    return ", ".join(f"{v:g}ms" for v in values)


def _px(values: Sequence[float]) -> str:
    return ", ".join(f"{v:g}" for v in values) + "px"


def spec_axes(spec: Mapping[str, Any]) -> Tuple[AxisValues, str]:
    """The seven axes from the spec's design facts, rounded to four
    decimals, and the axes source in one sentence (module docstring)."""
    dl = _design(spec)
    primary, canvas = _primary(spec), _canvas(dl)
    ink = _color(dl.get("color_ink"), canvas)
    if ink is None:
        ink = max(("#000000", WHITE), key=lambda h: contrast(h, canvas))
    loudest = max([primary] + [h for _, h in _accents(dl)], key=_chroma)

    warmth = _clamp(0.5 + 0.7 * _lean(primary, PRIMARY_FULL) + 0.3 * _lean(canvas, CANVAS_FULL))
    contrast_axis = _clamp(0.15 + 0.35 * math.log(contrast(ink, canvas)) / math.log(21.0)
                           + 0.35 * _chroma(loudest)
                           + 0.3 * (1.0 - math.log(contrast(canvas, "#000000"))
                                    / math.log(21.0)))
    base = _spacing_base(dl)
    density = 0.5 if base is None else _clamp(0.5 - 0.25 * math.log2(base / 4.0))
    radii = _radii(dl)
    geometry = 0.5 if not radii else _clamp(
        1.0 - math.exp(-sum(min(r, RADIUS_CAP) for r in radii) / len(radii) / RADIUS_SCALE))
    faces = _faces(dl)
    prior = _clamp(1.0 - 0.7 * _chroma(primary) - 0.3 * _clamp(_chroma(ink) / INK_FULL))
    formality = (prior + sum(f.place[0] for f in faces)) / (1 + len(faces))
    personality = (0.5 + sum(f.place[3] for f in faces)) / (1 + len(faces))
    durations = _durations(dl)
    span = math.log(MOTION_TOP_MS / MOTION_FLOOR_MS)
    motion = 0.5 if not durations else sum(
        _clamp(math.log(d / MOTION_FLOOR_MS) / span) for d in durations) / len(durations)

    values = dict(warmth=warmth, contrast=contrast_axis, density=density, geometry=geometry,
                  formality=formality, motion=motion, type_personality=personality)
    axes = AxisValues(**{a: round(values[a], 4) + 0.0 for a in AXIS_NAMES})

    parts = [f"warmth from the hue and chroma of the primary {primary} and the canvas {canvas}",
             f"contrast from the ink {ink} on that canvas, its depth and the chroma of {loudest}",
             f"density from its {base:g}px spacing base" if base is not None
             else "density at 0.5 since it states no spacing base",
             f"geometry from its radii {_px(radii)}" if radii
             else "geometry at 0.5 since it states no radius",
             "formality from the chroma of its primary and ink"
             + (f" and the measured place of {' and '.join(f.family for f in faces)}"
                if faces else ""),
             f"motion from its stated durations {_ms(durations)}" if durations
             else "motion at 0.5 since its motion signature states no duration",
             f"type personality from the measured place of "
             f"{' and '.join(f.family for f in faces)}" if faces
             else "type personality at 0.5 since neither face is in the engine's catalog"]
    source = (f"Read from {_SPEC_DIR}/{_sid(spec)}.json: " + "; ".join(parts) + ".")
    return axes, source


# ---------------------------------------------------------------- entries


def _digest(tokens_json: str) -> Dict[str, Any]:
    """A short digest of the built tokens: a hash of tokens.json and a few
    values a reviewer can read."""
    from engine.foundations.export import from_dtcg
    ts = from_dtcg(json.loads(tokens_json))

    def value(path: str, ctx: str = "") -> Any:
        v = ts.resolve(path, ctx)
        if isinstance(v, dict) and set(v) == {"value", "unit"}:
            return f"{v['value']:g}{v['unit']}"
        if isinstance(v, list):
            return v[0]
        return v

    return {
        "action": {"dark": value("color.action.primary", "scheme:dark"),
                   "light": value("color.action.primary")},
        "face": {"display": value("type.face.display"), "text": value("type.face.text")},
        "page": {"dark": value("color.surface.page", "scheme:dark"),
                 "light": value("color.surface.page")},
        "radius_control": value("radius.control"),
        "state_duration": value("motion.state.duration"),
        "tokens": len(list(ts.tokens())),
        "tokens_sha256": hashlib.sha256(tokens_json.encode("utf-8")).hexdigest()[:16],
    }


def entry(spec: Mapping[str, Any]) -> Dict[str, Any]:
    """The gallery entry for one spec, built and gated. Raises GalleryError
    naming every finding when the system does not pass."""
    brand, why = brand_hex(spec)
    axes, source = spec_axes(spec)
    out = make_system(brand, axes, source, arabic=True)
    if not out.passed:
        lines = "; ".join(f.line() for f in out.findings[:5])
        raise GalleryError(f"{_sid(spec)}: the system from brand {brand} and axes "
                           f"{axes.to_dict()} fails the gate ({lines}); change the rule in "
                           f"scripts/build_gallery.py that chose the failing input, never the "
                           f"spec's id")
    return {"arabic": True, "axes": axes.to_dict(), "axes_source": source, "brand": brand,
            "brand_rule": why, "digest": _digest(out.files["tokens.json"]),
            "id": _sid(spec), "name": str(spec.get("name", _sid(spec))),
            "spec": f"{_SPEC_DIR}/{_sid(spec)}.json"}


def dump(data: Mapping[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def build_all(specs: Optional[Sequence[Tuple[str, Mapping[str, Any]]]] = None) -> Dict[str, str]:
    """{file name: text} for every spec."""
    return {f"{sid}.json": dump(entry(spec)) for sid, spec in (specs or load_specs())}


def check(folder: Path, built: Mapping[str, str]) -> List[str]:
    """Every entry that differs from what the script builds, is missing, or
    has no spec, each with the fix."""
    problems = []
    on_disk = {f.name for f in folder.glob("*.json")} if folder.is_dir() else set()
    for name in sorted(built):
        path = folder / name
        if name not in on_disk:
            problems.append(f"{path} is missing; run python scripts/build_gallery.py")
        elif path.read_bytes() != built[name].encode("ascii"):
            problems.append(f"{path} differs from what the specs build; run python "
                            f"scripts/build_gallery.py and review the diff")
    for name in sorted(on_disk - set(built)):
        problems.append(f"{folder / name} has no spec in {_SPEC_DIR}; delete it or add the spec")
    return problems


def write(folder: Path, built: Mapping[str, str]) -> List[str]:
    """Write every entry, remove entries with no spec, and return the names
    written or removed."""
    folder.mkdir(parents=True, exist_ok=True)
    changed = []
    for name, text in sorted(built.items()):
        path = folder / name
        data = text.encode("ascii")
        if not path.is_file() or path.read_bytes() != data:
            path.write_bytes(data)
            changed.append(name)
    for path in sorted(folder.glob("*.json")):
        if path.name not in built:
            path.unlink()
            changed.append(path.name)
    return changed


def main(argv: Sequence[str]) -> int:
    args = list(argv)
    unknown = [a for a in args if a != "--check"]
    if unknown:
        print(f"unknown argument {unknown[0]!r}; run with no argument to write the gallery, "
              f"or with --check to compare it")
        return 2
    try:
        built = build_all()
    except GalleryError as exc:
        print(exc)
        return 1
    if "--check" in args:
        problems = check(GALLERY, built)
        print(f"gallery: {'ok' if not problems else f'{len(problems)} problems'} over "
              f"{len(built)} specs")
        for p in problems:
            print(f"  {p}")
        return 1 if problems else 0
    changed = write(GALLERY, built)
    print(f"gallery: {len(built)} entries, {len(changed)} written or removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
