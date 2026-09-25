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
  product_type     app, software, marketing-site, editorial, commerce, marketplace or
                   local-service (aliases in PRODUCT_ALIASES)

Beside them the brief may carry a character object: what a word the engine
does not read means, as nudges of -0.3 to 0.3 on the seven axes, applied
after the words (engine.synthesizer.axes.NUDGE_LIMIT).
"""
from __future__ import annotations

import re
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
# What the product is: the product the page sells, never the page itself
# (a landing page for an app is "app"; the page kind is project_type). One
# closed vocabulary, shared with the page-sequence picker: both import
# PRODUCT_TYPES, PRODUCT_ALIASES and product_type_of from here. An alias is
# accepted, mapped and reported; any other value is refused.
PRODUCT_TYPES: Tuple[str, ...] = ("app", "software", "marketing-site", "editorial", "commerce",
                                  "marketplace", "local-service")
PRODUCT_ALIASES: Mapping[str, str] = MappingProxyType({
    "saas": "software", "web-app": "software", "mobile-app": "app", "shop": "commerce",
    "store": "commerce", "b2b-marketplace": "marketplace", "b2c-marketplace": "marketplace",
    "service": "local-service"})
# BOOK_DEPTH says how far each is read like a book, 0 to 1, a per-type
# factor like AGES, never a table of faces: a product people use in tasks
# (app, software, commerce, marketplace, local-service) is 0, a marketing
# site with no product of its own sits between, and an editorial product
# is read at length. The face choice multiplies it into a book target that
# is continuous in type personality and formality (fonts.book_target).
BOOK_DEPTH: Mapping[str, float] = MappingProxyType({
    "app": 0.0, "software": 0.0, "commerce": 0.0, "marketplace": 0.0, "local-service": 0.0,
    "marketing-site": 0.5, "editorial": 1.0})
PRODUCT_FIX = ("say the product the page sells, not the page: a landing page for an app is "
               '"app", and the page kind goes in project_type')


def product_type_of(value: Any, label: str = "brief") -> str:
    """The product type a word names: one of PRODUCT_TYPES, or the type an
    alias in PRODUCT_ALIASES maps to, case and spaces aside ("Web app" is
    software). Anything else raises AudienceError naming the field, the
    values, the aliases and the fix."""
    word = "-".join(value.strip().lower().split()) if isinstance(value, str) else None
    if word in PRODUCT_TYPES:
        return word
    if word in PRODUCT_ALIASES:
        return PRODUCT_ALIASES[word]
    aliases = ", ".join(f"{k} as {v}" for k, v in PRODUCT_ALIASES.items())
    raise AudienceError(f"{label} field product_type is {value!r}; use one of "
                        f"{', '.join(PRODUCT_TYPES)} (read too: {aliases}); {PRODUCT_FIX}")
# Language subtags written in Arabic script.
ARABIC_LANGUAGES: Tuple[str, ...] = ("ar", "fa", "ur", "ps", "ckb", "sd", "ug")
# The member languages of the Arabic-script macrolanguages above, as the
# IANA language subtag registry lists them (Macrolanguage: ar, fa, ps), so
# a variety such as Egyptian (arz) or Levantine (apc) reads as Arabic.
# ajp is kept though the registry now points it at apc.
MACROLANGUAGE_MEMBERS: Mapping[str, Tuple[str, ...]] = MappingProxyType({
    "ar": ("aao", "abh", "abv", "acm", "acq", "acw", "acx", "acy", "adf", "aeb", "aec", "afb",
           "ajp", "apc", "apd", "arb", "arq", "ars", "ary", "arz", "auz", "avl", "ayh", "ayl",
           "ayn", "ayp", "pga", "shu", "ssh"),
    "fa": ("pes", "prs"),
    "ps": ("pbt", "pbu", "pst")})
# ISO 15924 script subtags for Arabic script: Arabic, and its Nastaliq form.
ARABIC_SCRIPTS: Tuple[str, ...] = ("arab", "aran")
# The language tokens.css also switches the Arabic styles on, besides
# dir="rtl": [lang|="ar"] matches "ar" and every "ar-" tag.
SELECTOR_LANGUAGE = "ar"
FIELDS: Tuple[str, ...] = ("age", "languages", "primary_script", "default_scheme",
                           "reading_context", "brand_role", "product_type")


def _either(choices: Tuple[str, ...]) -> str:
    return ", ".join(choices[:-1]) + " or " + choices[-1]


# The structured fields and their allowed values, for the CLI help and the
# MCP descriptions: a host that never reads the command doc learns them here.
FIELDS_HELP = (
    "The brief also takes seven structured fields, filled from its plain words (free text is "
    f"never read for them): age ({_either(tuple(AGES))}), languages (language tags, the main "
    'one first, such as ["ar-JO", "en"]), primary_script '
    f"({_either(SCRIPTS)}), default_scheme ({_either(SCHEMES)}), reading_context "
    f"({_either(READING)}), brand_role ({_either(BRAND_ROLES)}), product_type "
    f"({_either(PRODUCT_TYPES)}: the product the page sells, not the page; a product people "
    "use leans the faces to sans, an editorial product may take a serif). For example \"many readers are over 60\" is \"age\": "
    '"older-adults". A character object passes what a word the engine does not read means, '
    "as nudges from -0.3 to 0.3 on the axes warmth, contrast, density, geometry, formality, "
    'motion and type_personality, applied after the words: "sturdy" might be "character": '
    '{"contrast": 0.1, "geometry": -0.1}.')
# A language tag: a primary subtag of two or three letters, then subtags.
TAG = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$")
# Language names a brief may hold by mistake, and the tag to give instead.
# Only the error message reads it; a name is never taken as a tag.
NAME_TAGS: Mapping[str, str] = MappingProxyType({
    "arabic": "ar", "english": "en", "french": "fr", "spanish": "es", "german": "de",
    "persian": "fa", "farsi": "fa", "urdu": "ur", "pashto": "ps", "kurdish": "ckb",
    "turkish": "tr", "hebrew": "he", "hindi": "hi", "chinese": "zh", "japanese": "ja",
    "korean": "ko", "russian": "ru", "portuguese": "pt", "italian": "it", "dutch": "nl",
    "indonesian": "id", "malay": "ms"})


def script_subtag(tag: str) -> Optional[str]:
    """The script subtag of a language tag, lower case, or None: the first
    subtag of four letters after the language and any extended language
    subtags of three letters."""
    for part in tag.split("-")[1:]:
        if len(part) == 3 and part.isalpha():
            continue
        return part.lower() if len(part) == 4 and part.isalpha() else None
    return None


def writes_arabic(tag: str) -> bool:
    """Whether a language tag is written in Arabic script: its script
    subtag says so when it has one (so ar-Latn is Latin and pa-Arab is
    Arabic); otherwise its language is an Arabic-script language or a
    member of one of their macrolanguages."""
    script = script_subtag(tag)
    if script is not None:
        return script in ARABIC_SCRIPTS
    lang = tag.split("-")[0].lower()
    return lang in ARABIC_LANGUAGES or any(lang in m for m in MACROLANGUAGE_MEMBERS.values())


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
    product_type: Optional[str] = None
    # The alias the brief wrote, when it wrote one ("saas" for software).
    product_alias: Optional[str] = None
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
    def book_depth(self) -> Optional[float]:
        """How far the product is read like a book (BOOK_DEPTH), or None
        when the brief does not say what the product is."""
        return BOOK_DEPTH[self.product_type] if self.product_type else None

    @property
    def arabic(self) -> Optional[bool]:
        """True or False when the brief names languages, True when it sets
        the primary script to Arabic, None otherwise (the build keeps its
        default)."""
        if not self.languages:
            return True if self.primary_script == "arabic" and "primary_script" in self.given \
                else None
        return self.primary_script == "arabic" or any(writes_arabic(t) for t in self.languages)

    def to_dict(self) -> Dict[str, Any]:
        return {"age": self.age, "languages": list(self.languages),
                "primary_script": self.primary_script, "default_scheme": self.default_scheme,
                "reading_context": self.reading_context, "brand_role": self.brand_role,
                "product_type": self.product_type}


def _choice(brief: Mapping[str, Any], key: str, choices: Tuple[str, ...], label: str,
            default: Optional[str]) -> Optional[str]:
    value = brief.get(key)
    if value in (None, ""):
        return default
    if not isinstance(value, str) or value.strip().lower() not in choices:
        raise AudienceError(f"{label} field {key} is {value!r}; use one of "
                            f"{', '.join(choices)}")
    return value.strip().lower()


def _check_tags(langs: List[str], label: str) -> None:
    """Every entry is a language tag. A language name points to its tag."""
    for t in langs:
        if TAG.match(t):
            continue
        if t.lower() in NAME_TAGS:
            example = ", ".join(f'"{NAME_TAGS.get(x.lower(), x)}"' for x in langs)
            raise AudienceError(f'{label} field languages holds "{t}", a language name; give its '
                                f'tag "{NAME_TAGS[t.lower()]}", for example "languages": '
                                f"[{example}]")
        raise AudienceError(f'{label} field languages holds "{t}", which is not a language tag; '
                            "give a tag of two or three letters and optional subtags, for "
                            'example "languages": ["ar-JO", "en"]')


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
        if not isinstance(langs, list) or not all(isinstance(t, str) for t in langs):
            raise AudienceError(f"{label} field languages is {langs!r}; give language tags, for "
                                'example "languages": ["ar-JO", "en"]')
        _check_tags([t.strip() for t in langs], label)
        languages = tuple(t.strip() for t in langs)
    script_default = "latin"
    if languages and writes_arabic(languages[0]):
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
        product_type=product_type_of(brief["product_type"], label)
        if brief.get("product_type") not in (None, "") else None,
        product_alias=_alias_of(brief.get("product_type")),
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


def _glance_words(a: Audience, axes: Optional[Any]) -> str:
    """What glance reading did: the score it added to bento, the
    composition people scan, and whether the page starts from it."""
    from engine.foundations.composition import GLANCE_BONUS, choose
    from engine.synthesizer.axes import AxisValues
    win = choose(axes if axes is not None else AxisValues(*[0.5] * 7), a).name
    lead = f"Bento, the composition people scan, scores {GLANCE_BONUS:.2f} higher, and the page "
    return lead + ("starts from it" if win == "bento" else f"still starts from {win}")


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
        out.append(Effect(_glance_words(a, axes), "the brief says people glance at it"))
    if "languages" in a.given:
        if a.arabic:
            out.append(Effect("Arabic faces, sizes and right to left styles are built",
                              f"the brief names {', '.join(a.languages)}"))
            for tag in a.languages:
                if writes_arabic(tag) and tag.split("-")[0].lower() != SELECTOR_LANGUAGE:
                    out.append(Effect(
                        f'Mark text in {tag} with dir="rtl"',
                        'tokens.css switches to the Arabic styles on dir="rtl" or on a lang of '
                        f'{SELECTOR_LANGUAGE} and its subtags, and "{tag}" is neither'))
        else:
            out.append(Effect("The system is Latin only",
                              f"the brief names {', '.join(a.languages)}, none written in "
                              "Arabic script"))
    if a.primary_script == "arabic" and a.arabic and (
            "primary_script" in a.given or "languages" in a.given):
        out.append(Effect('Set dir="rtl" and the lang attribute on the html element',
                          "the primary script is Arabic, so pages open right to left"))
    if "default_scheme" in a.given and a.default_scheme != "system":
        out.append(Effect(f"tokens.css opens in {a.default_scheme} mode and sets color-scheme; "
                          f"data-theme still switches it",
                          f"the brief sets {a.default_scheme} as the default scheme"))
    if a.brand_role:
        out.append(Effect(f"The brand's role is {a.brand_role}", "the brief names it"))
    if a.product_alias:
        out.append(Effect(f'product_type "{a.product_alias}" is read as {a.product_type}',
                          "the engine and the page-sequence picker share one vocabulary"))
    if a.product_type:
        out.append(_product_effect(a, axes))
    return out


def _alias_of(value: Any) -> Optional[str]:
    word = "-".join(value.strip().lower().split()) if isinstance(value, str) else None
    return word if word in PRODUCT_ALIASES else None


def _product_effect(a: Audience, axes: Optional[Any]) -> Effect:
    """What the product type did to the faces at these axes: the lean read
    from the faces chosen, and the Arabic faces only when Arabic ships."""
    from engine.foundations import fonts
    from engine.synthesizer.axes import AxisValues
    at = axes if axes is not None else AxisValues(*[0.5] * 7)
    choice = fonts.choose(at, a.book_depth)
    target = fonts.book_target(at, a.book_depth or 0.0)
    shown = [choice.display, choice.text] + ([choice.arabic, choice.arabic_display]
                                             if a.arabic is not False else [])
    serif = sum(fonts.bookish(f) for f in shown)
    lean = "serif" if serif == len(shown) else ("sans" if not serif else "sans and serif")
    what = (f"The faces lean {lean}, with a book target of {target:.2f}: display "
            f"{choice.display.family} ({choice.display.generic}), text {choice.text.family}")
    if a.arabic is not False:
        what += (f", Arabic {choice.arabic.family} ({choice.arabic.generic}), Arabic display "
                 f"{choice.arabic_display.family} ({choice.arabic_display.generic})")
    reason = ("a product people use in tasks wants interface faces, not book faces"
              if not a.book_depth else
              "the product is read more like a book the more editorial it is, and the target "
              "grows with type personality and formality")
    name = a.product_type.replace("-", " ")
    noun = name if name.endswith(("app", "software", "site", "service", "marketplace")) \
        else f"{name} product"
    article = "" if name == "software" else ("an " if noun[0] in "aeiou" else "a ")
    return Effect(what, f"the brief says the product is {article}{noun}, and {reason}")


# How a person passes what the engine could not read from free text.
HOW_TO_PASS = (
    'age ("children", "teens", "adults", "all-ages", "older-adults")',
    'languages (tags such as ["ar-JO", "en"]) and primary_script ("latin" or "arabic")',
    'default_scheme ("light", "dark" or "system")',
    'reading_context ("glance", "task", "long-read" or "on-the-go")',
    'brand_role ("fill", "accent" or "edge")',
    'product_type ("' + '", "'.join(PRODUCT_TYPES[:-1]) + '" or "' + PRODUCT_TYPES[-1]
    + '", the product the page sells)',
)
