"""Measure before defining: the enhance report.

enhance() reads an imported system (in its own names), checks it through
the naming adapter's view, and, given a scan of the product's code,
measures what the code actually does against it:

- tokens not found in the code read, directly or through a token that is
  found; when the scan skipped files or saw values it could not measure,
  the report says so beside the list, and it never tells the owner to
  remove a token on the scan's word alone. A custom property that defines
  one of the system's tokens is its definition, not a use;
- raw values a token already holds (use the token), matched within the
  family the value is written in (a z-index is never matched to a
  weight), and only to a token named for that family (an equal 12px in a
  token named for nothing is a coincidence, not a swap); a color only to
  a token named for how the use applies it (never a border token for a
  background, never the color on one named surface such as on-brand).
  Error pages and email templates are shown where the app's stylesheet
  may not load: their raw values are not listed, and the files are named
  once;
- values written many ways (#fff, #FFF and white), and how many raw
  values each family carries (a corner written 3px, 4px and 6px);
- names that lie: every use contradicts the name (a background token only
  ever used as text, a hover token never used on hover), and names with
  stray uses, where some uses match the name and some do not. A name with
  "on" before a word (on-surface, onPrimary) is a foreground, the color on
  that surface, by the common convention, unless a background or fill word
  comes before it (action-on-brand is a fill for use on a brand surface)
  and no text word does (button-fg-on-color is a foreground). A custom
  property that passes a token on neither keeps nor breaks its promise;
- references to tokens the system does not have (a var() to a custom
  property the code declares itself is the code's own, listed apart with
  a count; one the source holds in an entry the import did not read, such
  as a property set only under a density or theme block, is named as
  unread, not missing), and what the scan could not measure (files it
  skipped, values it saw but does not read, with the scanner's reason and
  fix, and classes that name no token).

Structure lists what is wrong with the system itself. How the engine
layers its own systems (a semantic token aliases a primitive, a primitive
holds no mode) is told at most once, as a note, since a flat system or a
layer whose values switch by mode works as it is; the engine's rule on
which axes each of its foundations varies on is not applied to names that
are not its roles.

The report says how many of the engine's roles the mapping covers, which
ones the owner left out and which ones are not mapped at all, so a mapping
that maps nothing never passes as a clean gate. Then what the owner should
confirm (reading faces, breakpoints, modes the mapping lacks; reduced
motion kept as separate twin tokens, or as a prefers-reduced-motion block
in the code, is reported as present, not as a missing mode) and every
decision the engine made without them (mappings by name, entries a merge
proposed, values read with a note), so they can reverse it.

The system is fixed input: the report measures and proposes, and never
changes a value, refills an entry the owner left out, or writes a file.
"""
from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from engine.foundations.build import FOUNDATIONS, SystemCheck, check_system
from engine.foundations.modes import AXES
from engine.foundations.tokens import AliasError, TokenSet, alias_target, is_alias
from engine.foundations.validate import validate
from engine.io.adapter import (
    AXIS_LEFT_OUT, ROLE_LEFT_OUT, ROLE_TYPES, VOCABULARY_EXAMPLES, Mapping, deleted_axes,
    reduced_pairs, reduced_twins, their_names, view)
from engine.io.report import Imported
from engine.io.scan import (
    FAMILY_WORDS, LINE_WORDS, RADIUS_WORDS, SPACE_WORDS, Scan, Usage, _norm, canonical)

# Family of a use -> the token types that can hold its value. A
# line-height is a number, or a length when written with a unit.
FAMILY_TYPES: Dict[str, Tuple[str, ...]] = {
    "color": ("color",), "space": ("dimension",), "radius": ("dimension",),
    "border": ("dimension",), "type-size": ("dimension",), "tracking": ("dimension",),
    "leading": ("number",), "weight": ("fontWeight", "number"), "z": ("number",),
    "duration": ("duration",), "motion": ("cubicBezier",), "shadow": ("shadow",),
    "font": ("fontFamily",)}
# Name words and the use they promise.
TEXT_WORDS = ("text", "fg", "foreground")
BG_WORDS = ("bg", "background", "surface", "canvas", "backdrop")
# Words that name a fill: before "on" they make the name a background for
# use on that surface (action-on-brand, the button fill on a brand band).
FILL_WORDS = ("action", "button", "btn", "fill", "cta")
# The words that name a family (LINE_WORDS, SPACE_WORDS, RADIUS_WORDS,
# FAMILY_WORDS) live in scan, which reads class names by them too.
# The state a name promises. Only hover is held against the code: the
# scanner reads it from :hover and hover: wherever it is set. Active,
# pressed, selected and current it reads from pseudo-classes, the common
# classes and ARIA attributes, but a product may set them in forms it does
# not read (data-state=on, .open), so a use outside them is no proof; and a
# focus ring is often set at rest and shown on focus.
STATE_WORDS = {"hover": "hover"}
_BG_PROPS = re.compile(r"background(-color)?$|bg$")
_TEXT_PROPS = re.compile(r"(color|caret-color|fill|stroke|text-decoration-color)$|text$")
_LINE_PROPS = re.compile(r"(border|outline|ring|divide)(-.*)?$|box-shadow$")
_NUMBER = re.compile(r"-?\d+(\.\d+)?$")
# The engine's own fix on a contrast finding (move to a step of its ramp,
# and a hint about its seed) does not apply to a system it did not make.
_MOVE = re.compile(r" Move \S+ to a step with more contrast against \S+\.(?: .*)?$")
_THEIR_FIX = (" Change the value of one of them in your system, or map the role to a token "
              "with more contrast.")
READING_ROLES = ("type.text.body", "type.text.body-small", "type.text.fine")
# Pages shown where the app's stylesheet and custom properties may not load:
# error pages (a folder named errors, or 404.html) and email templates (a
# folder named emails or mail, or a file named for email). Their raw
# values are not listed; the report names the files once.
_STANDALONE_DIRS = ("errors", "error", "emails", "email", "mail", "mails", "newsletters",
                    "newsletter")
_STANDALONE_STEMS = re.compile(r"(40[0-9]|50[0-9x]|error|maintenance|offline)$|.*e-?mail",
                               re.I)
# How many names a folded line shows before "and N more".
FEW = 6
# The longest line the gate prints; a longer one wraps, a finding under its
# bullet.
WIDTH = 160


def _and(items: Sequence[str]) -> str:
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _few(items: Sequence[str], n: int = FEW) -> str:
    """The items, comma separated, or the first n and how many more."""
    items = list(items)
    if len(items) <= n + 1:
        return ", ".join(items)
    return f"{', '.join(items[:n])} and {len(items) - n} more"


def _and_few(items: Sequence[str], n: int) -> str:
    """The items joined with "and", or the first n and how many more."""
    items = list(items)
    return _and(items if len(items) <= n + 1 else items[:n] + [f"{len(items) - n} more"])


def _count(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def _brief(text: str, limit: int = 60) -> str:
    """Written text on one line, cut at `limit` characters."""
    flat = " ".join(str(text).split())
    return flat if len(flat) <= limit else flat[:limit - 3] + "..."


def _sentence(text: str) -> str:
    return text if text.endswith(".") else text + "."


def _words(path: str) -> List[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", path)
    return [w.lower() for w in re.split(r"[.\-/_ ]+", spaced) if w]


def _prop_class(prop: str) -> str:
    """How a use applies a color: background, text or border. A Tailwind
    utility (bg-ink) is read by its prefix."""
    for candidate in (prop, prop.split("-", 1)[0]):
        if _BG_PROPS.match(candidate):
            return "background"
        if _LINE_PROPS.match(candidate):
            return "border"
        if _TEXT_PROPS.match(candidate):
            return "text"
    return ""


def _key(value: str) -> str:
    """A canonical value as a lookup key: hex colors in one case."""
    return value.upper() if value.startswith("#") else value


def _kinds(u: Usage) -> Tuple[str, ...]:
    """The token types that could hold a raw use's value: its family's, or
    for a use in no known family, what its canonical form says."""
    if u.family == "leading" and u.value.endswith("px"):
        return ("dimension",)
    if u.family in FAMILY_TYPES:
        return FAMILY_TYPES[u.family]
    if u.value.startswith("#"):
        return ("color",)
    if u.value.endswith("px"):
        return ("dimension",)
    if u.value.endswith("ms"):
        return ("duration",)
    return ("number",) if _NUMBER.match(u.value) else ()


def _fits(path: str, family: str) -> Tuple[bool, bool]:
    """(fits, named for it): whether a token may hold a raw value of the
    family, and whether its name says that family. In a family its name
    can say (space, radius, border, type size, weight, z), only a token
    named for it fits: an equal value in a token named for nothing (2px,
    0, 12px) is a coincidence, not a swap."""
    if family not in FAMILY_WORDS:
        return True, False
    own = bool(set(_words(path)) & set(FAMILY_WORDS[family]))
    return own, own


def _name_class(path: str) -> str:
    """How a color token's name says it is applied: text, background or
    border, "pair" for the color on one named surface (on-brand,
    text-on-brand), or "" when the name says none."""
    words = _words(path)
    if "on" in words[:-1]:
        return "pair"
    if any(w in words for w in TEXT_WORDS):
        return "text"
    if any(w in words for w in BG_WORDS):
        return "background"
    if any(w in words for w in LINE_WORDS):
        return "border"
    return ""


def _color_fits(path: str, use: str) -> bool:
    """Whether a color token may be offered for a raw color applied as
    `use` (text, background, border or ""): one named for another
    application never is (a border token for a transparent background),
    nor one named for the color on a surface, since the scan cannot tell
    which surface a value sits on (white text on a photo is not on-brand)."""
    named = _name_class(path)
    return named != "pair" and (not named or named == use)


@dataclass(frozen=True)
class RawWithToken:
    value: str
    tokens: List[str]
    uses: List[Usage]


@dataclass(frozen=True)
class Spelling:
    value: str
    texts: List[str]
    uses: List[Usage]


@dataclass(frozen=True)
class Lie:
    token: str
    message: str


@dataclass(frozen=True)
class Missing:
    value: str
    where: str


@dataclass
class Drift:
    # Tokens not found in the code read (see complete).
    unused: List[str] = field(default_factory=list)
    # type -> (tokens, tokens found in use)
    totals: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    raw_with_token: List[RawWithToken] = field(default_factory=list)
    spellings: List[Spelling] = field(default_factory=list)
    # family -> the raw values it carries, in the order first seen
    distinct: Dict[str, List[str]] = field(default_factory=dict)
    # Every use contradicts the name.
    lies: List[Lie] = field(default_factory=list)
    missing: List[Missing] = field(default_factory=list)
    # (family, value) -> where it is first written raw
    first_seen: Dict[Tuple[str, str], str] = field(default_factory=dict)
    # What the scan read and what it could not.
    files: int = 0
    skipped: List[Tuple[str, str]] = field(default_factory=list)
    unknown_classes: List[Tuple[str, int, str]] = field(default_factory=list)
    # (file, line, kind, text, why) for values the scan saw but could not
    # measure; why is the scanner's reason and fix, or ""
    not_read: List[Tuple[str, int, str, str, str]] = field(default_factory=list)
    # Some uses match the name and some do not.
    strays: List[Lie] = field(default_factory=list)
    # --name -> where each var() to it is, for the custom properties the
    # code declares itself: the code's own, not tokens the system lacks.
    own: Dict[str, List[str]] = field(default_factory=dict)
    # Error pages and email templates the scan read, whose raw values are
    # not listed (see _standalone).
    standalone: List[str] = field(default_factory=list)
    # References to names the system's source holds in an entry the import
    # did not read (a property set only under a density or theme block):
    # --name -> (where each reference is, the entry's place and message).
    unread_refs: Dict[str, Tuple[List[str], str, str]] = field(default_factory=dict)

    @property
    def complete(self) -> bool:
        """Whether the scan read files and measured everything in them: no
        file skipped, no value seen and left unmeasured. Only then does a
        token not found mean no code read uses it."""
        return self.files > 0 and not self.skipped and not self.not_read


def _refs(ts: TokenSet, path: str) -> List[str]:
    t = ts.get(path)
    out: List[str] = []

    def leaves(v: Any) -> None:
        if isinstance(v, dict):
            for x in v.values():
                leaves(x)
        elif isinstance(v, list):
            for x in v:
                leaves(x)
        elif is_alias(v):
            out.append(alias_target(v))
    for v in [t.value, *t.modes.values()]:
        leaves(v)
    return out


def _held(ts: TokenSet) -> Dict[Tuple[str, str], List[str]]:
    """(type, canonical value) -> the tokens that hold it, semantic ones
    first."""
    held: Dict[Tuple[str, str], List[str]] = {}
    for t in sorted(ts.tokens(), key=lambda t: t.layer != "semantic"):
        try:
            value = canonical(t.type, ts.resolve(t.path))
        except (AliasError, KeyError, TypeError, ValueError):
            continue
        held.setdefault((t.type, _key(value)), []).append(t.path)
    return held


def _holders(held: Dict[Tuple[str, str], List[str]], u: Usage) -> List[str]:
    """The tokens that hold a raw use's value within its family, those
    named for the family first; a color only from a token whose name fits
    how the use applies it."""
    out: List[Tuple[bool, str]] = []
    for kind in _kinds(u):
        for path in held.get((kind, _key(u.value)), []):
            fits, own = _fits(path, u.family)
            if u.family == "color":
                fits = _color_fits(path, _prop_class(u.prop))
            if fits:
                out.append((not own, path))
    return [p for _, p in sorted(out, key=lambda x: x[0])]


def _standalone(file: str) -> bool:
    """Whether a file is an error page or an email template."""
    parts = re.split(r"[\\/]", file)
    stem = parts[-1].split(".", 1)[0]
    return any(p.lower() in _STANDALONE_DIRS for p in parts[:-1]) \
        or bool(_STANDALONE_STEMS.fullmatch(stem))


def _not_read(entry: Any) -> Tuple[str, int, str, str, str]:
    file, line, kind, text = tuple(entry)[:4]
    return file, line, kind, text, getattr(entry, "why", "") or ""


def drift(ts: TokenSet, scanned: Scan) -> Drift:
    """What the code does against the system (see the module docstring)."""
    d = Drift(files=scanned.files, skipped=list(scanned.skipped),
              unknown_classes=list(scanned.unknown_classes),
              not_read=[_not_read(x) for x in getattr(scanned, "not_read", ())])
    # A custom property that defines one of the system's own tokens (the
    # system's stylesheet in the scan) is its definition, not a use: the
    # tokens it points at are reached through it only when it is used.
    own = {_norm(t.path) for t in ts.tokens()}
    usages = [u for u in scanned.usages
              if not (u.kind == "token" and u.prop.startswith("--") and _norm(u.prop[2:]) in own)]
    reached, todo = set(), [u.value for u in usages if u.kind == "token"]
    while todo:
        path = todo.pop()
        if path in reached or not ts.has(path):
            continue
        reached.add(path)
        todo += _refs(ts, path)
    d.unused = [t.path for t in ts.tokens() if t.path not in reached]
    for t in ts.tokens():
        total, hit = d.totals.get(t.type, (0, 0))
        d.totals[t.type] = (total + 1, hit + (t.path in reached))

    held = _held(ts)
    groups: Dict[Tuple[str, str], List[Usage]] = {}
    d.standalone = sorted({u.file for u in usages if _standalone(u.file)})
    for u in usages:
        if u.kind != "raw" or u.file in d.standalone:
            continue
        groups.setdefault((u.family, _key(u.value)), []).append(u)
        values = d.distinct.setdefault(u.family, [])
        if u.value not in values:
            values.append(u.value)
            d.first_seen[(u.family, u.value)] = u.where()
    for uses in groups.values():
        # Uses of one color applied differently can hold different tokens:
        # each application gets its own line when they do.
        parts: Dict[Tuple[str, ...], List[Usage]] = {}
        for u in uses:
            parts.setdefault(tuple(_holders(held, u)), []).append(u)
        for tokens, part in parts.items():
            if tokens:
                d.raw_with_token.append(RawWithToken(uses[0].value, list(tokens), part))
        texts: List[str] = []
        for u in uses:
            if u.text not in texts:
                texts.append(u.text)
        if len(texts) > 1:
            d.spellings.append(Spelling(uses[0].value, texts, uses))
    declared = set(getattr(scanned, "declared", ()))
    for u in usages:
        if u.kind == "missing" and u.value in declared:
            d.own.setdefault(u.value, []).append(u.where())
    d.missing = [Missing(u.value, u.where()) for u in usages
                 if u.kind == "missing" and u.value not in declared]
    by_token: Dict[str, List[Usage]] = {}
    for u in usages:
        # A custom property that points at a token (--link-hover:
        # var(--primary-hover)) passes it on; it does not apply it, so it
        # neither keeps nor breaks the name's promise.
        if u.kind == "token" and not u.prop.startswith("--"):
            by_token.setdefault(u.value, []).append(u)
    for t in ts.tokens():
        found = _lie(t.path, by_token.get(t.path, []))
        if found:
            message, every = found
            (d.lies if every else d.strays).append(Lie(t.path, message))
    return d


# (what the name is for, whether a use keeps that promise, how it breaks it)
_Promise = Tuple[str, Callable[[Usage], bool], Callable[[Usage], str]]


def _color_promise(named: str, against: Tuple[str, ...], how: str) -> _Promise:
    """A color name broken only by a use in a class it clearly is not (a
    text color as a background); a border use of a text or surface color is
    common and not held against it."""
    return (named, lambda u: u.family != "color" or _prop_class(u.prop) not in against,
            lambda u: how.format(_prop_class(u.prop)))


def _promise(words: List[str]) -> Optional[_Promise]:
    """What a token's name promises about how it is used. "on" before a
    word names the color on that surface: a foreground, whatever follows,
    unless a background or fill word comes first (bg-on-dark is a
    background for use on dark, action-on-brand the fill of a button on a
    brand surface), and a text word before it wins over both
    (action-fg-on-color and button-text-on-color are foregrounds)."""
    on = words.index("on") if "on" in words[:-1] else -1
    if on != -1:
        if any(w in BG_WORDS + FILL_WORDS for w in words[:on]) \
                and not any(w in TEXT_WORDS for w in words[:on]):
            return _color_promise("backgrounds", ("text",), "used for {} color")
        return _color_promise("the color on a surface", ("background",), "used as a {}")
    if any(w in words for w in TEXT_WORDS):
        return _color_promise("text", ("background",), "used as a {}")
    if any(w in words for w in BG_WORDS):
        return _color_promise("backgrounds", ("text",), "used for {} color")
    if any(w in words for w in LINE_WORDS):
        return _color_promise("edges", ("background",), "used as a {}")
    if any(w in words for w in SPACE_WORDS):
        return ("spacing", lambda u: u.family in ("space", ""),
                lambda u: f"used for {u.family}")
    if any(w in words for w in RADIUS_WORDS):
        return ("corners", lambda u: u.family in ("radius", ""),
                lambda u: f"used for {u.family}")
    return None


def _lie(path: str, uses: List[Usage]) -> Optional[Tuple[str, bool]]:
    """How a token's name misstates its uses, and whether every use does;
    None when none does."""
    if not uses:
        return None
    words = _words(path)
    wrong: List[Tuple[Usage, str, str]] = []
    promise = _promise(words)
    if promise:
        named, ok, how = promise
        wrong += [(u, named, how(u)) for u in uses if not ok(u)]
    state = next((STATE_WORDS[w] for w in words if w in STATE_WORDS), None)
    if state:
        seen = [w for w, _, _ in wrong]
        # A rule whose selector list also names the state (.btn:hover,
        # .btn:focus-visible) gives its other uses the same style on
        # purpose; they keep the name's promise.
        beside = {(u.file, u.line, u.prop) for u in uses if state in u.state.split(",")}
        wrong += [(u, state, f"used outside {state}") for u in uses
                  if state not in u.state.split(",") and u not in seen
                  and (u.file, u.line, u.prop) not in beside]
    if not wrong:
        return None
    first, named, how = wrong[0]
    more = f" and {len(wrong) - 1} more" if len(wrong) > 1 else ""
    good = len(uses) - len(wrong)
    return (f"is named for {named} but is {how} at {first.where()}{more}; {good} of its "
            f"{len(uses)} uses match its name"), good == 0


# ---------------------------------------------------------------- report


@dataclass
class Enhanced:
    imported: Imported
    mapping: Mapping
    check: SystemCheck
    structure: List[str]
    drift: Optional[Drift]
    confirm: List[str]
    decisions: List[str]
    findings: List[str]
    merge_notes: List[str] = field(default_factory=list)
    # Mapped roles whose token cannot be resolved, so the gate could not
    # measure them; Structure says why.
    unresolved: List[str] = field(default_factory=list)
    # The mapping file, as the messages name it.
    mapping_name: str = "mapping.json"

    def mapped(self) -> List[str]:
        return [r for r, m in self.mapping.roles.items() if m.token is not None]

    def left_out(self) -> List[str]:
        """Roles the owner kept out of the check with a "not mapped" entry."""
        return [r for r, m in self.mapping.roles.items() if m.token is None]

    def not_mapped(self) -> List[str]:
        """Roles the mapping does not name at all."""
        return [r for r in ROLE_TYPES if r not in self.mapping.roles]

    def axes_left_out(self) -> List[str]:
        return [a for a, m in self.mapping.axes.items() if m.source is None]

    @property
    def measured(self) -> bool:
        """Whether the gate measured anything: a mapping that maps no role,
        mapped roles none of which could be checked, or checks that found
        nothing to apply to leave it nothing, and that is never a pass."""
        return not self.why_not_measured()

    def why_not_measured(self) -> str:
        """Why the gate measured nothing, or "" when it measured something."""
        if not self.mapped():
            return "no role is mapped"
        if not self.check.foundations:
            return "no mapped role could be checked"
        report = self.check.report
        if report.checked + report.rules_checked == 0:
            return "no check applied to the mapped roles"
        return ""

    def to_dict(self) -> Dict[str, Any]:
        d = self.drift
        m = self.mapping
        report = self.check.report
        return {
            "source": self.imported.report.source.to_dict(),
            "import": {"entries": self.imported.report.entries,
                       "tokens": self.imported.report.tokens,
                       "not_read": len(self.imported.report.not_read)},
            "mapping": {"roles": {r: (x.token if x.fields is None else
                                      {k: f.token for k, f in x.fields.items()})
                                  for r, x in m.roles.items()},
                        "axes": {a: x.source for a, x in m.axes.items()},
                        "mapped": len(self.mapped()), "of": len(ROLE_TYPES),
                        "by_name": [r for r, x in m.roles.items()
                                    if x.token is not None and x.by == "name"],
                        "vocabularies": {r: x.vocabulary for r, x in m.roles.items()
                                         if x.vocabulary},
                        "left_out": self.left_out(),
                        "axes_left_out": self.axes_left_out(),
                        "not_mapped": self.not_mapped(),
                        "merge_notes": list(self.merge_notes)},
            "structure": list(self.structure),
            "gate": {"measured": self.measured,
                     "why": self.why_not_measured(),
                     "passed": report.passed if self.measured else None,
                     "pairs_checked": report.checked,
                     "rules_checked": report.rules_checked,
                     "unresolved": list(self.unresolved),
                     "findings": list(self.findings),
                     "foundations": list(self.check.foundations)},
            "drift": None if d is None else {
                "files": d.files,
                "complete": d.complete,
                "unused": list(d.unused),
                "totals": {k: list(v) for k, v in d.totals.items()},
                "raw_with_token": [{"value": r.value, "tokens": r.tokens,
                                    "uses": [u.where() for u in r.uses]}
                                   for r in d.raw_with_token],
                "spellings": [{"value": s.value, "texts": s.texts,
                               "uses": [u.where() for u in s.uses]} for s in d.spellings],
                "distinct": {k: list(v) for k, v in d.distinct.items()},
                "lies": [{"token": x.token, "message": x.message} for x in d.lies],
                "strays": [{"token": x.token, "message": x.message} for x in d.strays],
                "missing": [{"value": x.value, "where": x.where} for x in d.missing],
                "unread_refs": [{"name": n, "uses": list(w), "where": at, "why": why}
                                for n, (w, at, why) in d.unread_refs.items()],
                "own": [{"name": n, "uses": list(w)} for n, w in d.own.items()],
                "standalone": list(d.standalone),
                "skipped": [{"file": f, "why": w} for f, w in d.skipped],
                "unknown_classes": [{"where": f"{u[0]}:{u[1]}", "class": u[2],
                                     "looked_in": list(getattr(u, "looked_in", ())),
                                     "near": getattr(u, "near", "")}
                                    for u in d.unknown_classes],
                "not_read": [{"where": f"{f}:{n}", "kind": k, "text": t, "why": w}
                             for f, n, k, t, w in d.not_read]},
            "confirm": list(self.confirm),
            "decisions": list(self.decisions),
        }

    def markdown(self) -> str:
        report = self.imported.report
        s = report.source
        lines = ["# Enhance report", "",
                 ("This report measures the system and the code as they are. It changes "
                  "nothing; the owner decides what should be."), "",
                 "## What was read", "",
                 (f"{s.path} ({s.format}, sha256 {s.sha256[:12]}): {report.tokens} tokens "
                  f"from {report.entries} entries, {len(report.not_read)} not read. The import "
                  "report lists each entry."), "",
                 "## How it was checked", ""]
        lines += self._how()
        lines += ["", "## Structure", ""]
        lines += [f"- {_sentence(p)}" for p in self.structure] or ["No structural problem."]
        lines += ["", "## Gate", ""]
        lines += self._gate(s.path)
        lines += ["", "## What the code uses", ""]
        lines += self._code(s.path)
        lines += ["", "## For the owner to confirm", ""]
        lines += [f"- {c}" for c in self.confirm] or ["Nothing."]
        lines += ["", "## Decisions made without you", ""]
        lines += [f"- {_sentence(c)}" for c in self.decisions] or ["None."]
        return "\n".join(lines) + "\n"

    def check_lines(self, source: str) -> List[str]:
        """How the system was checked and the gate's verdict, without the
        findings: the mapping per foundation, then the verdict line, or
        that nothing was measured. `source` is the system's file."""
        return [*self._how(), "", *self._gate(source, findings=False)]

    def _gate(self, source: str, findings: bool = True) -> List[str]:
        why = self.why_not_measured()
        if why == "no role is mapped":
            return [("Not measured: no role is mapped, so the gate had nothing to measure and "
                     f"nothing here passed; map roles to your tokens in {self.mapping_name} to "
                     "check them.")]
        if why:
            n = len(self.mapped())
            roles = "the 1 mapped role" if n == 1 else f"none of the {n} mapped roles"
            could = "could not be checked" if n == 1 else "could be checked"
            if why != "no mapped role could be checked":
                could = "gave the gate no check to apply"
            return [(f"Not measured: {roles} {could} (see Structure and the decisions), so the "
                     "gate had nothing to measure and nothing here passed.")]
        report = self.check.report
        head = report.summary().splitlines()[0]
        line = f"Checked {_and(self.check.foundations)}: {head}"
        unresolved = _and_few(self.unresolved, FEW) if self.unresolved else ""
        mistyped = [f.message.split(" ", 1)[0] for f in report.failures
                    if f.check == "role-types"]
        if unresolved:
            why = f"{unresolved} could not be resolved (see Structure)"
        elif mistyped:
            why = (f"{_and_few(mistyped, FEW)} {'is' if len(mistyped) == 1 else 'are'} not of "
                   f"the type {'its role expects' if len(mistyped) == 1 else 'their roles expect'}"
                   " (see below)")
        else:
            why = "each needs both of its roles mapped"
        if report.checked == 0:
            line = (f"Checked {_and(self.check.foundations)}. No contrast pair was measured, "
                    f"since {why}, so the verdict covers the rule checks only: {head}")
        elif unresolved:
            it = "it" if len(self.unresolved) == 1 else "they"
            line += (f" The pairs and rules that need {unresolved} were not measured, since "
                     f"{it} could not be resolved (see Structure).")
        if self.findings and findings:
            line += f" Each finding names our role, then your token in {source}."
        out = textwrap.wrap(line, WIDTH, break_long_words=False, break_on_hyphens=False)
        if self.findings and findings:
            out.append("")
            for f in self.findings:
                out += textwrap.wrap(f, WIDTH, initial_indent="- ", subsequent_indent="  ",
                                     break_long_words=False, break_on_hyphens=False)
        return out

    def _how(self) -> List[str]:
        m = self.mapping
        mapped = self.mapped()
        by_name = sum(1 for r in mapped if m.roles[r].by == "name")
        axes = [a for a, x in m.axes.items() if x.source is not None]
        lines = [(f"Mapped {len(mapped)} of {len(ROLE_TYPES)} roles the engine checks "
                  f"({by_name} by name, {len(mapped) - by_name} by you), and {len(axes)} of "
                  f"{len(AXES)} mode axes. Only mapped roles are measured; map more in "
                  "mapping.json to check more."), "",
                 "| Foundation | Mapped | Left out by you | Not mapped |", "|---|---|---|---|"]
        left, missing = set(self.left_out()), set(self.not_mapped())
        per: Dict[str, Tuple[int, List[str]]] = {}
        for f in FOUNDATIONS:
            roles = list(f.role_types)
            hit = sum(1 for r in roles if r in mapped)
            out = sum(1 for r in roles if r in left)
            none = [r for r in roles if r in missing]
            lines.append(f"| {f.name} | {hit} of {len(roles)} | {out} | {len(none)} |")
            if none:
                per[f.name] = (len(roles), none)
        lines.append("")
        if left:
            lines.append(f"- Left out by you ({len(left)}): {_few(self.left_out())}.")
        if self.axes_left_out():
            lines.append(f"- Axes left out by you ({len(self.axes_left_out())}): "
                         f"{', '.join(self.axes_left_out())}.")
        if missing:
            lines.append(f"- Not mapped at all ({len(missing)}); map each one you have a "
                         "token for, or write {\"token\": null, \"by\": \"owner\"} to keep it "
                         "out. The JSON report lists every one:")
            lines += [f"  - {name}: {len(none)} of {total}, such as {_few(none, 2)}"
                      for name, (total, none) in per.items()]
        else:
            lines.append("- Every role is named in the mapping.")
        return lines

    def _code(self, source: str) -> List[str]:
        d = self.drift
        if d is None:
            return [("No code was scanned, so nothing here says which tokens are used; pass "
                     "the folders that hold the product's code with --scan.")]
        if d.files == 0:
            return [("No file was read, so nothing was measured: no token is known to be used "
                     "or unused. Pass the folders that hold the product's code with --scan.")] \
                + self._unread(d)
        read = f"the {_count(d.files, 'file', 'files')} read"
        gaps = []
        if d.skipped:
            gaps.append(f"{_count(len(d.skipped), 'file was', 'files were')} not read")
        if d.not_read:
            gaps.append(f"{_count(len(d.not_read), 'place was', 'places were')} not measured")
        lines = [f"Read {_count(d.files, 'file', 'files')}."]
        if gaps:
            lines[0] += (f" {_and(gaps).capitalize()}; each is listed at the end of this "
                         "section, and what is below covers only what was read.")
        if d.standalone:
            k = len(d.standalone)
            what = _count(k, "file is an error page or an email template",
                          "files are error pages or email templates")
            lines.append(f"- {what} ({_and_few(d.standalone, FEW)}). "
                         f"{'It is' if k == 1 else 'They are'} "
                         "shown where the app's stylesheet and custom properties may not load, so "
                         f"{'its' if k == 1 else 'their'} raw values are not listed here.")
        lines.append("")
        total = sum(t for t, _ in d.totals.values())
        if d.unused:
            line = (f"- {len(d.unused)} of {total} tokens were not found in {read}: "
                    f"{_few(d.unused, 12)}. They are defined in {source}; ")
            if d.complete:
                line += ("if no code outside the scan uses them, removing them is your call; "
                         "scan any other code first.")
            else:
                line += (f"{_and(gaps)} (listed below), so scan those too or confirm by hand "
                         "before removing any.")
            lines.append(line)
        for kind, (count, hit) in d.totals.items():
            lines.append(f"- {kind}: {hit} of {count} tokens found in use.")
        for r in d.raw_with_token:
            wheres = _few([u.where() for u in r.uses])
            lines.append(f"- {r.value} is written raw {len(r.uses)} "
                         f"time{'' if len(r.uses) == 1 else 's'} ({wheres}); the system "
                         f"holds it as {_and_few(r.tokens, 3)}, so use a token.")
        for sp in d.spellings:
            first: Dict[str, str] = {}
            for u in sp.uses:
                first.setdefault(u.text, u.where())
            written = _few([f"{t} at {first[t]}" for t in sp.texts])
            lines.append(f"- {sp.value} is written {len(sp.texts)} ways: {written}; pick one, "
                         "or better, use a token that holds it.")
        for family, values in d.distinct.items():
            if len(values) > 1:
                shown = _few(values, 12)
                seen = _few([d.first_seen[(family, v)] for v in values], 3)
                lines.append(f"- {family} is written as {len(values)} raw values: {shown}. "
                             f"First seen at {seen}; move each onto a {family} token, or add "
                             "one for a value the design keeps.")
        for lie in d.lies:
            lines.append(f"- {lie.token} {lie.message}; rename it for how it is used, or use a "
                         "token named for that use there.")
        lines += _missing(d.missing)
        for ref, (wheres, at, why) in d.unread_refs.items():
            lines.append(f"- {ref} ({_few(wheres, 3)}) is in {source}, so it is not missing, but "
                         f"it was not read as a token: at {at} it {_sentence(why)}")
        if d.own:
            k, n = len(d.own), sum(len(w) for w in d.own.values())
            names = _few([f"{name} ({_few(w, 3)})" for name, w in d.own.items()])
            lines.append(f"- The code declares {_count(k, 'custom property', 'custom properties')} "
                         f"of its own and references {'it' if k == 1 else 'them'} "
                         f"{_count(n, 'time', 'times')}: {names}. "
                         f"{'It is' if k == 1 else 'They are'} the code's own, not "
                         f"{'a token' if k == 1 else 'tokens'} the system lacks; if "
                         f"{'it holds' if k == 1 else 'one holds'} a value the design keeps, "
                         f"move it into {source} as a token.")
        if d.strays:
            lines += ["", ("These names match some of their uses and not others; each line says "
                           "where a use does not match:"), ""]
            for stray in d.strays:
                lines.append(f"- {stray.token} {stray.message}; where it does not, use a token "
                             "named for that use.")
        unread = self._unread(d)
        if d.strays and unread:
            lines += ["", "What the scan did not read or measure:", ""]
        return lines + unread

    def _unread(self, d: Drift) -> List[str]:
        """What the scan did not read or measure, each with the fix. Repeats
        fold: files skipped for one reason, places not measured of one kind
        and classes looked up in one namespace each become one line with a
        count and a few examples; to_dict() keeps every entry."""
        lines: List[str] = []
        skipped: Dict[str, List[str]] = {}
        for file, why in d.skipped:
            skipped.setdefault(why, []).append(file)
        groups = list(skipped.items())
        for why, files in groups[:FEW]:
            # The scanner writes a reason as what the file is or cannot do.
            if len(files) == 1:
                lines.append(f"- {files[0]} {_sentence(why)}" if why[:1].islower()
                             else f"- {files[0]} was not read: {_sentence(why)}")
            else:
                lines.append(f"- {len(files)} files were not read ({_few(files, 3)}): "
                             + (f"each {_sentence(why)}" if why[:1].islower()
                                else _sentence(why)))
        if len(groups) > FEW:
            rest = sum(len(f) for _, f in groups[FEW:])
            lines.append(f"- {_count(rest, 'more file was', 'more files were')} not read for "
                         f"{_count(len(groups) - FEW, 'other reason', 'other reasons')}; the "
                         "JSON report lists each file with its reason and fix.")
        kinds: Dict[str, List[Tuple[str, int, str, str, str]]] = {}
        for entry in d.not_read:
            kinds.setdefault(entry[2], []).append(entry)
        for kind, entries in kinds.items():
            file, line, _, written, why = entries[0]
            if len(entries) == 1:
                lines.append(_unmeasured(file, line, kind, written, why))
                continue
            wheres = _few([f"{f}:{n}" for f, n, _, _, _ in entries], 3)
            example = (_sentence(why) if why else
                       f"it writes {_brief(written)}, which the scan does not measure.")
            lines.append(f"- {len(entries)} places were not measured ({kind}), at {wheres}. "
                         f"At {file}:{line}, {example} Check each by hand, or write it in a "
                         "form the scan reads; the JSON report gives each one's reason and "
                         "fix.")
        lines += self._classes(d)
        return lines

    def _classes(self, d: Drift) -> List[str]:
        """Unknown classes, one line per namespace and reason: a lone class
        says where it is used; more say how many and show a few."""
        reasons: Dict[Tuple[Tuple[str, ...], str, str], Tuple[str, str, str]] = {}
        # (namespaces, reason) -> class -> (its reason, where it is used)
        groups: Dict[Tuple[Tuple[str, ...], str],
                     Dict[str, Tuple[Tuple[str, str, str], List[str]]]] = {}
        for entry in d.unknown_classes:
            key = (tuple(getattr(entry, "looked_in", ())), getattr(entry, "name", ""),
                   getattr(entry, "near", ""))
            if key not in reasons:
                reasons[key] = self._class_reason(*key)
            reason = reasons[key]
            uses = groups.setdefault((key[0], reason[0]), {})
            uses.setdefault(entry[2], (reason, []))[1].append(f"{entry[0]}:{entry[1]}")
        lines = []
        for uses in groups.values():
            if len(uses) == 1:
                cls, ((_, single, _), wheres) = next(iter(uses.items()))
                at = (wheres[0] if len(wheres) == 1
                      else f"{wheres[0]} and {len(wheres) - 1} more places")
                lines.append(f"- {at} {'uses' if len(wheres) == 1 else 'use'} the class "
                             f"{cls}{single}")
                continue
            total = sum(len(w) for _, w in uses.values())
            (_, _, plural), _ = next(iter(uses.values()))
            shown = _few([f"{c} ({w[0]}{f' and {len(w) - 1} more' if len(w) > 1 else ''})"
                          for c, (_, w) in uses.items()], FEW)
            lines.append(f"- {total} uses of {len(uses)} classes"
                         + plural.replace("{shown}", shown))
        return lines

    def _class_reason(self, looked: Tuple[str, ...], name: str,
                      near: str) -> Tuple[str, str, str]:
        """(reason, the fix for one class, the fix for many): why a class
        names no token, with the namespaces it was looked up in and a token
        of its name the system has outside them or holds in the source
        without reading it. The plural form takes {shown}, the classes."""
        if not looked or not name:
            return ("system",
                    ", which names no token in the system; add the token to the system, or "
                    "use a class that names one it has.",
                    " name no token in the system: {shown}; add a token for each value the "
                    "design keeps, or use classes that name tokens it has. The JSON report "
                    "lists every use.")
        where = (f"the {looked[0]} namespace" if len(looked) == 1 else
                 f"the {', '.join(looked[:-1])} or {looked[-1]} namespaces")
        them = "it" if len(looked) == 1 else "them"
        head = f", which names no token in {where}"
        many = f" name no token in {where}: {{shown}}"
        if near:
            return ("near", f"{head}; the system has {near}, outside {them}: rename it "
                    f"{looked[0]}-{name} so the class reads it, or use a class that names a "
                    "token the system has.",
                    f"{many}; the system has each under a name outside {them} (such as {near} "
                    f"for {name}): rename each into {where} so the "
                    "class reads it, or use classes that name tokens the system has. The JSON "
                    "report lists every use.")
        wanted = {_norm(f"{space}.{name}") for space in looked}
        source = self.imported.report.source.path
        for item in self.imported.report.not_read:
            key = _norm(item.name)
            if key in wanted or key == _norm(name) or key.endswith("." + _norm(name)):
                return ("unread", f"{head}; {source} holds {item.name} at {item.where}, which was "
                        "not read (the import report says how to write it): fix that entry so "
                        "the class reads it.",
                        f"{many}; {source} holds each in an entry that was not read (such as "
                        f"{item.name} at {item.where}; the import report says how to write "
                        "each): fix those entries so the classes read them. The JSON report "
                        "lists every use.")
        return ("none", f"{head}; add {looked[0]}-{name} to the system, or use a class that "
                "names a token it has.",
                f"{many}; add a token for each value the design keeps (such as "
                f"{looked[0]}-{name}), or use classes that name tokens the system has. The "
                "JSON report lists every use.")


def _missing(missing: Sequence[Missing]) -> List[str]:
    """References to tokens the system lacks: one line per name, or, past
    FEW names, one line for all with a count and a few."""
    names: Dict[str, List[str]] = {}
    for miss in missing:
        names.setdefault(miss.value, []).append(miss.where)
    if len(names) > FEW:
        shown = _few([f"{n} ({w[0]}{f' and {len(w) - 1} more' if len(w) > 1 else ''})"
                      for n, w in names.items()], FEW)
        return [f"- The code references {len(names)} names the system does not have, "
                f"{_count(len(missing), 'time', 'times')}: {shown}; add each to the system, or "
                "point the references at tokens it has. The JSON report lists every use."]
    lines = []
    for name, wheres in names.items():
        if len(wheres) == 1:
            lines.append(f"- {wheres[0]} references {name}, which the system does not have; add "
                         "it to the system, or point the reference at a token it has.")
        else:
            lines.append(f"- {name} is referenced {len(wheres)} times ({_few(wheres, 3)}), and "
                         "the system does not have it; add it to the system, or point the "
                         "references at a token it has.")
    return lines


def _unmeasured(file: str, line: int, kind: str, written: str, why: str) -> str:
    if why:
        return f"- {file}:{line} was not measured ({kind}): {_sentence(why)}"
    return (f"- {file}:{line} writes {_brief(written)} ({kind}), which the scan does not "
            "measure; check it by hand, or write it in a form the scan reads (a longhand "
            "property or a var() to a token).")


def _reading_face(checked: TokenSet, role: str) -> Optional[str]:
    try:
        face = checked.resolve(role)["fontFamily"]
    except (AliasError, KeyError, TypeError, ValueError):
        return None
    return face if isinstance(face, str) else (face[0] if face else None)


def _reduced_motion(ts: TokenSet, mapping: Mapping, scanned: Optional[Scan],
                    source: str, name: str) -> str:
    """What the report says of reduced motion when the mapping reads no
    motion axis: present through separate twin tokens, present in the
    code's own reduced-motion block, or missing."""
    twins = reduced_twins(ts, mapping)
    if twins:
        pairs = {base: twin for base, twin in twins.values()}
        shown = _and_few([f"{t} for {b}" for b, t in pairs.items()], 3)
        return (f"The system has reduced motion as separate tokens ({shown}), read as the "
                "reduced-motion values of their base tokens, so the motion checks ran under "
                "reduced motion; confirm each pair.")
    pairs = reduced_pairs(ts)
    if pairs:
        shown = _and_few([f"{t} for {b}" for b, t in pairs.items()], 3)
        return (f"The system has reduced motion as separate tokens ({shown}), but no mapped role "
                f"reads them; map the motion roles to their base tokens in {name} to check them "
                "under reduced motion.")
    blocks = list(getattr(scanned, "reduced_motion", ()) or ())
    if blocks:
        every = [b for b in blocks if "*" in b[2]]
        file, line, _ = (every or blocks)[0]
        what = "for everything " if every else ""
        return (f"The code turns motion down {what}in a prefers-reduced-motion block at "
                f"{file}:{line}, so reduced motion is present, though not as a mode of the "
                "system: the motion checks under reduced motion ran on no token. To check them, "
                f"give {source} a reduced-motion mode or reduced tokens, and map them in {name}.")
    return ("The system has no reduced-motion mode in the mapping, so the motion checks under "
            "reduced motion did not run; if it has one, map it as the motion axis in "
            f"{name}.")


def _dark(ts: TokenSet, scanned: Optional[Scan], source: str, name: str) -> str:
    """What the report says when the mapping reads no dark scheme: that the
    source read has none, and where the code sets dark values for its
    tokens when a second source holds them."""
    own = {_norm(t.path) for t in ts.tokens()}
    sets = [(p, f, n) for p, f, n in getattr(scanned, "dark", ()) or ()
            if _norm(p[2:]) in own]
    if not sets:
        return (f"{source}, the source read, has no dark mode in the mapping, so dark was not "
                f"checked; if another file holds its dark values, import it with {source}, and "
                f"if the system has a dark mode, map it as the scheme axis in {name}.")
    files = list(dict.fromkeys(f for _, f, _ in sets))
    names = list(dict.fromkeys(p for p, _, _ in sets))
    where = _and_few([f"{p} at {f}:{n}" for p, f, n in sets], 3)
    return (f"{source}, the source read, has no dark mode, but {_and_few(files, 3)} "
            f"{'sets' if len(files) == 1 else 'set'} dark values for "
            f"{_count(len(names), 'of its tokens', 'of its tokens')} ({where}): the dark mode is "
            f"in a second source. Import it with {source}, then map the scheme axis in {name} "
            "to check dark.")


def _confirm(mapping: Mapping, checked: TokenSet, foundations: Sequence[str],
             deleted: Sequence[str] = (), motion: str = "", dark: str = "") -> List[str]:
    out = []
    for role in READING_ROLES:
        first = _reading_face(checked, role) if checked.has(role) else None
        if first:
            out.append(f"{role} (your {mapping.roles[role].token}) is set in {first}; confirm "
                       "it is a face made for running text, not a display face."
                       if role in mapping.roles else
                       f"{role} is set in {first}; confirm it is a face made for running "
                       "text, not a display face.")
    breakpoints = [r for r in ROLE_TYPES if r.startswith("layout.breakpoint.")
                   and checked.has(r)]
    if breakpoints:
        values = []
        for r in breakpoints:
            v = checked.resolve(r)
            values.append(f"{r} {v['value']:g}{v['unit']}" if isinstance(v, dict) else r)
        checked_how = (" (the gate checked reflow at 320px against them)"
                       if "layout" in foundations else "")
        out.append(f"The breakpoints are {', '.join(values)}; confirm they are the ones the "
                   f"product ships{checked_how}.")
    else:
        out.append("No breakpoint is mapped, so reflow at 320px was not checked; map "
                   "layout.breakpoint.tablet to your first breakpoint to check it.")
    # An axis the owner left out on purpose is not asked for again, nor one
    # deleted from the mapping, which the decisions already name.
    if "motion" not in mapping.axes and "motion" not in deleted and motion:
        out.append(motion)
    if "scheme" not in mapping.axes and "scheme" not in deleted and dark:
        out.append(dark)
    return out


# How the engine layers its own systems: a semantic token aliases a
# primitive, a primitive holds a literal and no mode, and each foundation
# varies only on its own axes. A system it did not make is layered its own
# way, which works as it is: these are told once, never per token.
_LAYERING = ("semantic-literal", "semantic-to-semantic", "primitive-modes", "primitive-alias")
_OWN_NAMING = ("axis-not-allowed",)


def _their_structure(problems: Sequence[Any]) -> List[str]:
    """Structure problems of an imported system: the engine's layering
    told once as a note, its axis-per-foundation rule dropped (the
    system's names are not the engine's roles, and a mode value that
    differs from the base is the system working), everything else as
    it is."""
    out: List[str] = []
    layered: List[str] = []
    for p in problems:
        if p.rule in _OWN_NAMING:
            continue
        if p.rule in _LAYERING:
            if p.token not in layered:
                layered.append(p.token)
            continue
        out.append(p.message)
    if layered:
        out.append(f"The system is layered its own way: {len(layered)} "
                   f"{'token holds' if len(layered) == 1 else 'tokens hold'} a value of "
                   f"{'its' if len(layered) == 1 else 'their'} own or point at another token "
                   f"that is not a primitive (such as {_few(layered, 3)}). The engine's own "
                   "systems alias primitives, but a flat system, or a layer whose values switch "
                   "by mode, works as it is, so nothing here needs to change")
    return out


def _split_unread(d: Drift, imported: Imported) -> None:
    """Move each reference to a name the source holds in an entry the
    import did not read (set only under a density or theme block, or on a
    component) out of the missing list: the system has it, unread."""
    unread = {item.name: item for item in imported.report.not_read
              if item.name.startswith("--")}
    keep: List[Missing] = []
    for miss in d.missing:
        item = unread.get(miss.value)
        if item is None:
            keep.append(miss)
            continue
        wheres, _, _ = d.unread_refs.setdefault(miss.value, ([], item.where, item.message))
        wheres.append(miss.where)
    d.missing = keep


def _owner_notes(mapping: Mapping, name: str) -> List[str]:
    """The notes view() gives for the owner's "not mapped" entries, which
    the report lists itself under How it was checked."""
    return [ROLE_LEFT_OUT.format(role=r, name=name)
            for r, m in mapping.roles.items() if m.token is None] \
        + [AXIS_LEFT_OUT.format(axis=a, name=name)
           for a, m in mapping.axes.items() if m.source is None]


def _break(ts: TokenSet, path: str, chain: Tuple[str, ...] = ()) -> Optional[List[str]]:
    """Why a token does not resolve, one clause per hop, following its base
    value and every mode override; None when it resolves."""
    if path in chain:
        return ["which closes a loop"]
    if not ts.has(path):
        return ["which is not defined"]
    t = ts.get(path)
    for value in [t.value, *t.modes.values()]:
        for target in _alias_leaves(value):
            rest = _break(ts, target, chain + (path,))
            if rest is not None:
                return [f"{path} aliases {target}"] + rest
    return None


def _alias_leaves(value: Any) -> List[str]:
    if isinstance(value, dict):
        return [x for v in value.values() for x in _alias_leaves(v)]
    if isinstance(value, list):
        return [x for v in value for x in _alias_leaves(v)]
    return [alias_target(value)] if is_alias(value) else []


def _unresolved(ts: TokenSet, checked: TokenSet, mapping: Mapping, source: str,
                name: str) -> Dict[str, str]:
    """Each mapped role view() left out because its token cannot be
    resolved, with the reason in the system's names and the fix."""
    out: Dict[str, str] = {}
    if checked is ts:
        return out
    for role, m in mapping.roles.items():
        if m.token is None or checked.has(role) or not ts.has(m.token):
            continue
        clauses = _break(ts, m.token)
        if clauses is None:
            continue
        missing = clauses[-2].rsplit(" ", 1)[-1] if clauses[-1] == "which is not defined" else ""
        fix = (f"define {missing} in {source}, or map {role} to a token that resolves in {name}"
               if missing else f"point one of them at a value in {source}, or map {role} to a "
               f"token that resolves in {name}")
        out[role] = (f"{role} (your {m.token}) cannot be resolved: {', '.join(clauses)}; {fix}")
    return out


def _by_name(mapping: Mapping, name: str) -> List[str]:
    """The roles mapped by name only, one line per foundation: a lone role
    by itself, more with a count and a few (the JSON report lists each)."""
    per: Dict[str, List[Tuple[str, str]]] = {}
    vocabularies: Dict[str, List[str]] = {}
    for role, m in mapping.roles.items():
        if m.by == "name" and m.token is not None:
            foundation = role.split(".", 1)[0]
            per.setdefault(foundation, []).append((role, m.token))
            if m.vocabulary and m.vocabulary not in vocabularies.setdefault(foundation, []):
                vocabularies[foundation].append(m.vocabulary)
    lines = []
    for foundation, pairs in per.items():
        through = _through(vocabularies.get(foundation, []))
        if len(pairs) == 1:
            role, token = pairs[0]
            lines.append(f"{role} is mapped to {token} by name only{through}; confirm it in "
                         f"{name}.")
            continue
        same = sum(1 for r, t in pairs if _norm(r) == _norm(t))
        shown = _few([r if _norm(r) == _norm(t) else f"{r} to {t}" for r, t in pairs], 3)
        each = (", each to the token of the same name" if same == len(pairs) else
                f", {same} of them to the token of the same name" if same else "")
        lines.append(f"{len(pairs)} {foundation} roles are mapped by name only{each}{through}: "
                     f"{shown}; confirm them in {name}. The JSON report lists each.")
    return lines


def _through(vocabularies: Sequence[str]) -> str:
    """Which naming vocabularies the proposals matched, as a clause."""
    if not vocabularies:
        return ""
    if len(vocabularies) == 1:
        v = vocabularies[0]
        return f", through the {v} vocabulary ({VOCABULARY_EXAMPLES.get(v, v)})"
    return f", through the {_and(list(vocabularies))} vocabularies"


_ROLE_TYPE_FIX = re.compile(r"; point it at a (\w+) token(, for example .*)?$")


def _mapped_fix(failure: Any, name: str) -> Any:
    """A role-types failure with the fix an imported set takes: map the role
    to one of the owner's tokens of that type in the mapping file, never a
    literal value."""
    if failure.check != "role-types":
        return failure
    message = _ROLE_TYPE_FIX.sub(
        lambda m: f"; map the role to one of your {m.group(1)} tokens in {name}", failure.message)
    return type(failure)(failure.check, failure.criterion, failure.mode, message)


def _finding(text: str, mapping: Mapping,
             twins: Optional[Dict[str, Tuple[str, str]]] = None) -> str:
    """A gate message in the system's names; a set with no mode axis
    prints an empty context, which is dropped. For a role read under
    reduced motion from a twin token, the fix names the twin, since the
    system has no override to change."""
    for role, (_, twin) in (twins or {}).items():
        if text.startswith(role + " "):
            text = (text.replace("with a motion:reduced override", f"in your {twin}")
                    .replace("its motion:reduced override", f"your {twin}"))
    return their_names(text.replace(" ()", ""), mapping)


def enhance(imported: Imported, mapping: Mapping, scanned: Optional[Scan] = None, *,
            merge_notes: Sequence[str] = (), mapping_name: str = "mapping.json") -> Enhanced:
    """The enhance report on an imported system (see the module docstring).
    `merge_notes` are the notes adapter.merge() gave when the mapping was
    merged with the owner's file; `mapping_name` is that file, as the
    messages name it. Raises InputError (from view) for a mapping that
    names a token or mode the system lacks."""
    ts = imported.tokens
    checked, notes = view(ts, mapping, mapping_name)
    result = check_system(checked, structure=checked is ts)
    structure = (_their_structure(validate(ts)) if checked is not ts
                 else [p.message for p in result.problems])
    unresolved = _unresolved(ts, checked, mapping, imported.report.source.path, mapping_name)
    structure += list(unresolved.values())
    notes = [n for n in notes if not any(
        n.startswith(f"{r} reads {mapping.roles[r].token}, which cannot be resolved (")
        for r in unresolved)]
    report = result.report
    twins = reduced_twins(ts, mapping)
    findings = [_finding(_MOVE.sub(_THEIR_FIX, f.message()), mapping) for f in report.findings]
    findings += [_finding(f"{c.message} (in {c.mode})" if c.mode else c.message, mapping, twins)
                 for c in (_mapped_fix(c, mapping_name) for c in report.failures)]
    decisions = _by_name(mapping, mapping_name)
    for axis, m in mapping.axes.items():
        if m.by == "name" and m.source is not None:
            values = ""
            if any(ours != theirs for ours, theirs in m.values.items()):
                values = " (" + ", ".join(f"{ours} is {theirs}"
                                          for ours, theirs in m.values.items()) + ")"
            decisions.append(f"{axis} is read from {m.source} by name only{values}; confirm "
                             f"it in {mapping_name}.")
    decisions += list(merge_notes)
    renamed, noted = len(imported.report.renamed), len(imported.report.notes)
    if renamed:
        decisions.append(f"{_count(renamed, 'name was', 'names were')} changed on the way in; "
                         "the import report lists each one.")
    if noted:
        decisions.append(f"{_count(noted, 'entry was', 'entries were')} read with a note; the "
                         "import report lists each one.")
    owner = set(_owner_notes(mapping, mapping_name))
    decisions += [n for n in notes if n not in owner]
    measured = drift(ts, scanned) if scanned is not None else None
    if measured is not None:
        _split_unread(measured, imported)
    return Enhanced(imported, mapping, result, structure, measured,
                    _confirm(mapping, checked, result.foundations, list(deleted_axes(ts, mapping)),
                             _reduced_motion(ts, mapping, scanned, imported.report.source.path,
                                             mapping_name),
                             _dark(ts, scanned, imported.report.source.path, mapping_name)),
                    decisions, findings,
                    list(merge_notes), list(unresolved), mapping_name)
