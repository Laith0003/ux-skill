"""Who the system is for: the structured brief fields beside the seven
axes, what the engine does with each, and why.

The host AI fills these fields from the plain words of a brief ("many
patients are over 60" is "age": "older-adults"); the engine never parses
free text for them. Each field maps to numbers the foundations read (body
size, target size, the ring, density, line height, measure, which scheme
comes first, which scripts ship) and to one line in system-report.md that
says what changed and why.

Fields:
  age              children, teens, adults, all-ages, older-adults
  languages        language tags, such as ["ar-JO", "en"]
  primary_script   latin or arabic (read from the first language when left out)
  default_scheme   light, dark or system
  reading_context  glance, task, long-read or on-the-go
  brand_role       fill, accent or edge
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Optional, Tuple

# How much each age band leans toward larger text and targets, 0 to 1.
AGES: Mapping[str, float] = MappingProxyType({
    "children": 0.5, "teens": 0.0, "adults": 0.0, "all-ages": 0.5, "older-adults": 1.0})
SCRIPTS: Tuple[str, ...] = ("latin", "arabic")
SCHEMES: Tuple[str, ...] = ("light", "dark", "system")
READING: Tuple[str, ...] = ("glance", "task", "long-read", "on-the-go")
BRAND_ROLES: Tuple[str, ...] = ("fill", "accent", "edge")
# Language subtags written in Arabic script.
ARABIC_LANGUAGES: Tuple[str, ...] = ("ar", "fa", "ur", "ps", "ckb", "sd", "ug")
FIELDS: Tuple[str, ...] = ("age", "languages", "primary_script", "default_scheme",
                           "reading_context", "brand_role")


class AudienceError(ValueError):
    """A structured field holds a value the engine does not read; the
    message names the field, the value and the choices."""


@dataclass(frozen=True)
class Effect:
    """One change the brief made, and why, in the report's words."""
    what: str
    why: str

    def line(self) -> str:
        return f"{self.what}: {self.why}"


@dataclass(frozen=True)
class Audience:
    age: str = "adults"
    languages: Tuple[str, ...] = ()
    primary_script: str = "latin"
    default_scheme: str = "system"
    reading_context: str = "task"
    brand_role: Optional[str] = None
    given: Tuple[str, ...] = field(default=(), compare=False)

    @property
    def age_factor(self) -> float:
        return AGES[self.age]

    @property
    def body_px(self) -> int:
        """Body text size: 16px, and up to 18px for older readers."""
        return 16 + int(2 * self.age_factor + 0.5)

    @property
    def target_px(self) -> int:
        """The comfortable minimum target: 44px, larger for older readers
        and for use on the go."""
        return 44 + int(4 * self.age_factor + 0.5) + (4 if self.reading_context == "on-the-go"
                                                      else 0)

    @property
    def ring_extra(self) -> int:
        """Extra focus ring width in px for readers who lean on it."""
        return 1 if self.age_factor >= 0.5 else 0

    @property
    def refuse_compact(self) -> bool:
        """Compact density shrinks text spacing and targets; it is not
        offered to older or mixed-age readers."""
        return self.age_factor >= 0.5

    @property
    def leading_extra(self) -> float:
        return 0.1 if self.reading_context == "long-read" else 0.0

    @property
    def measure_rem(self) -> int:
        return 34 if self.reading_context == "long-read" else 38

    @property
    def arabic(self) -> Optional[bool]:
        """True or False when the brief names languages, None when it does
        not (the build keeps its default)."""
        if not self.languages:
            return None
        return self.primary_script == "arabic" or any(
            t.split("-")[0].lower() in ARABIC_LANGUAGES for t in self.languages)

    def to_dict(self) -> Dict[str, Any]:
        return {"age": self.age, "languages": list(self.languages),
                "primary_script": self.primary_script, "default_scheme": self.default_scheme,
                "reading_context": self.reading_context, "brand_role": self.brand_role}


def _choice(brief: Mapping[str, Any], key: str, choices: Tuple[str, ...], label: str,
            default: Optional[str]) -> Optional[str]:
    value = brief.get(key)
    if value in (None, ""):
        return default
    if not isinstance(value, str) or value.strip().lower() not in choices:
        raise AudienceError(f"{label} field {key} is {value!r}; use one of "
                            f"{', '.join(choices)}")
    return value.strip().lower()


def read_audience(brief: Optional[Mapping[str, Any]], label: str = "brief") -> Audience:
    """The structured fields of a brief (a discovery file's answers are
    read the same way). Missing fields keep their defaults; a field with a
    value the engine does not read raises AudienceError naming it."""
    if brief is None:
        return Audience()
    if isinstance(brief.get("answers"), dict):
        brief = brief["answers"]
    langs = brief.get("languages")
    if langs in (None, "", []):
        languages: Tuple[str, ...] = ()
    else:
        if isinstance(langs, str):
            langs = [s.strip() for s in langs.split(",") if s.strip()]
        if not isinstance(langs, list) or not all(
                isinstance(t, str) and t.replace("-", "").isalnum() for t in langs):
            raise AudienceError(f"{label} field languages is {langs!r}; give language tags, for "
                                'example "languages": ["ar-JO", "en"]')
        languages = tuple(t.strip() for t in langs)
    script_default = "latin"
    if languages and languages[0].split("-")[0].lower() in ARABIC_LANGUAGES:
        script_default = "arabic"
    given = tuple(k for k in FIELDS if brief.get(k) not in (None, "", []))
    return Audience(
        age=_choice(brief, "age", tuple(AGES), label, "adults") or "adults",
        languages=languages,
        primary_script=_choice(brief, "primary_script", SCRIPTS, label, script_default)
        or script_default,
        default_scheme=_choice(brief, "default_scheme", SCHEMES, label, "system") or "system",
        reading_context=_choice(brief, "reading_context", READING, label, "task") or "task",
        brand_role=_choice(brief, "brand_role", BRAND_ROLES, label, None),
        given=given)


def _ring_words(a: Audience, axes: Optional[Any]) -> str:
    """What the age did to the focus ring at these axes: the pixels it
    added, or that the ring was already the widest standard ring."""
    from engine.foundations.border import ring_px
    if axes is None:
        return f"the focus ring is {a.ring_extra}px wider"
    wider = ring_px(axes, a.ring_extra) - ring_px(axes)
    if wider >= a.ring_extra:
        return f"the focus ring is {wider}px wider"
    std = ring_px(axes, a.ring_extra)
    return (f"the focus ring stays {std}px, already the widest standard ring for this contrast "
            f"({std + 1}px under high contrast)")


def effects(a: Audience, axes: Optional[Any] = None) -> List[Effect]:
    """What each field the brief set changed, and why. With the axes, the
    ring line states the ring the build made at them."""
    out: List[Effect] = []
    if "age" in a.given and a.age_factor:
        out.append(Effect(
            f"Body text is {a.body_px}px, targets are at least {a.target_px}px, "
            f"{_ring_words(a, axes)}" + (", and compact density is not offered"
                                          if a.refuse_compact else ""),
            f"the brief says the readers are {a.age.replace('-', ' ')}, who need larger text, "
            "larger targets and a focus ring they can find"))
    if a.reading_context == "on-the-go" and "reading_context" in a.given:
        out.append(Effect(f"Targets are at least {a.target_px}px",
                          "the brief says the product is used on the go, one handed"))
    if a.reading_context == "long-read":
        out.append(Effect(f"Body line height is 0.1 taller and the reading measure is "
                          f"{a.measure_rem}rem", "the brief says people read at length"))
    if a.reading_context == "glance":
        out.append(Effect("The page composition favors scanning",
                          "the brief says people glance at it"))
    if "languages" in a.given:
        if a.arabic:
            out.append(Effect("Arabic faces, sizes and right to left styles are built",
                              f"the brief names {', '.join(a.languages)}"))
        else:
            out.append(Effect("The system is Latin only",
                              f"the brief names {', '.join(a.languages)}, none written in "
                              "Arabic script"))
    if a.primary_script == "arabic" and ("primary_script" in a.given or "languages" in a.given):
        out.append(Effect('Set dir="rtl" and the lang attribute on the html element',
                          "the primary script is Arabic, so pages open right to left"))
    if "default_scheme" in a.given and a.default_scheme != "system":
        out.append(Effect(f"tokens.css opens in {a.default_scheme} mode and sets color-scheme; "
                          f"data-theme still switches it",
                          f"the brief sets {a.default_scheme} as the default scheme"))
    if a.brand_role:
        out.append(Effect(f"The brand's role is {a.brand_role}", "the brief names it"))
    return out


# How a person passes what the engine could not read from free text.
HOW_TO_PASS = (
    'age ("children", "teens", "adults", "all-ages", "older-adults")',
    'languages (tags such as ["ar-JO", "en"]) and primary_script ("latin" or "arabic")',
    'default_scheme ("light", "dark" or "system")',
    'reading_context ("glance", "task", "long-read" or "on-the-go")',
    'brand_role ("fill", "accent" or "edge")',
)
