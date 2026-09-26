"""Measure before defining: the enhance report.

enhance() reads an imported system (in its own names), checks it through
the naming adapter's view, and, given a scan of the product's code,
measures what the code actually does against it:

- tokens not found in the code read, directly or through a token that is
  found; when the scan skipped files or saw values it could not measure,
  the report says so beside the list, and it never tells the owner to
  remove a token on the scan's word alone;
- raw values a token already holds (use the token), matched within the
  family the value is written in (a z-index is never matched to a weight);
- values written many ways (#fff, #FFF and white), and how many raw
  values each family carries (a radius written eleven ways);
- names that lie: every use contradicts the name (a background token only
  ever used as text, a hover token never used on hover), and names with
  stray uses, where some uses match the name and some do not. A name with
  "on" before a word (on-surface, onPrimary) is a foreground, the color on
  that surface, by the common convention, unless a background or fill word
  comes before it (action-on-brand is a fill for use on a brand surface);
- references to tokens the system does not have (a var() to a custom
  property the code declares itself is the code's own, listed apart with
  a count), and what the scan could not measure (files it skipped, values
  it saw but does not read, with the scanner's reason and fix, and classes
  that name no token).

The report says how many of the engine's roles the mapping covers, which
ones the owner left out and which ones are not mapped at all, so a mapping
that maps nothing never passes as a clean gate. Then what the owner should
confirm (reading faces, breakpoints, modes the mapping lacks) and every
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
    AXIS_LEFT_OUT, ROLE_LEFT_OUT, ROLE_TYPES, Mapping, deleted_axes, their_names, view)
from engine.io.report import Imported
from engine.io.scan import Scan, Usage, canonical

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
LINE_WORDS = ("border", "line", "stroke", "outline", "divider", "ring", "separator")
SPACE_WORDS = ("space", "spacing", "gap", "padding", "margin", "gutter", "inset")
RADIUS_WORDS = ("radius", "rounded", "corner")
# Words that name a family: a raw value is matched only to tokens named for
# its own family or for none of the others (a z-index of 400 is not a
# weight token that holds 400, nor a 16px padding a radius token).
FAMILY_WORDS = {"space": SPACE_WORDS, "radius": RADIUS_WORDS, "border": LINE_WORDS,
                "weight": ("weight", "bold"), "z": ("z", "layer", "zindex")}
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
    family, and whether its name says that family."""
    if family not in FAMILY_WORDS:
        return True, False
    words = set(_words(path))
    own = bool(words & set(FAMILY_WORDS[family]))
    other = any(words & set(w) for f, w in FAMILY_WORDS.items() if f != family)
    return own or not other, own


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
    named for the family first."""
    out: List[Tuple[bool, str]] = []
    for kind in _kinds(u):
        for path in held.get((kind, _key(u.value)), []):
            fits, own = _fits(path, u.family)
            if fits:
                out.append((not own, path))
    return [p for _, p in sorted(out, key=lambda x: x[0])]


def _not_read(entry: Any) -> Tuple[str, int, str, str, str]:
    file, line, kind, text = tuple(entry)[:4]
    return file, line, kind, text, getattr(entry, "why", "") or ""


def drift(ts: TokenSet, scanned: Scan) -> Drift:
    """What the code does against the system (see the module docstring)."""
    d = Drift(files=scanned.files, skipped=list(scanned.skipped),
              unknown_classes=list(scanned.unknown_classes),
              not_read=[_not_read(x) for x in getattr(scanned, "not_read", ())])
    usages = scanned.usages
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
    for u in usages:
        if u.kind != "raw":
            continue
        groups.setdefault((u.family, _key(u.value)), []).append(u)
        values = d.distinct.setdefault(u.family, [])
        if u.value not in values:
            values.append(u.value)
            d.first_seen[(u.family, u.value)] = u.where()
    for uses in groups.values():
        tokens = _holders(held, uses[0])
        if tokens:
            d.raw_with_token.append(RawWithToken(uses[0].value, tokens, uses))
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
        if u.kind == "token":
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
    brand surface)."""
    on = words.index("on") if "on" in words[:-1] else -1
    if on != -1:
        if any(w in BG_WORDS + FILL_WORDS for w in words[:on]):
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
        wrong += [(u, state, f"used outside {state}") for u in uses
                  if state not in u.state.split(",") and u not in seen]
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
        """Whether the gate measured anything: a mapping that maps no role
        leaves it nothing, and that is never a pass."""
        return bool(self.check.foundations)

    def to_dict(self) -> Dict[str, Any]:
        d = self.drift
        m = self.mapping
        report = self.check.report
        return {
            "source": self.imported.report.source.to_dict(),
            "import": {"entries": self.imported.report.entries,
                       "tokens": self.imported.report.tokens,
                       "not_read": len(self.imported.report.not_read)},
            "mapping": {"roles": {r: x.token for r, x in m.roles.items()},
                        "axes": {a: x.source for a, x in m.axes.items()},
                        "mapped": len(self.mapped()), "of": len(ROLE_TYPES),
                        "by_name": [r for r, x in m.roles.items()
                                    if x.token is not None and x.by == "name"],
                        "left_out": self.left_out(),
                        "axes_left_out": self.axes_left_out(),
                        "not_mapped": self.not_mapped(),
                        "merge_notes": list(self.merge_notes)},
            "structure": list(self.structure),
            "gate": {"measured": self.measured,
                     "passed": report.passed if self.measured else None,
                     "pairs_checked": report.checked,
                     "rules_checked": report.rules_checked,
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
                "own": [{"name": n, "uses": list(w)} for n, w in d.own.items()],
                "skipped": [{"file": f, "why": w} for f, w in d.skipped],
                "unknown_classes": [{"where": f"{f}:{n}", "class": c}
                                    for f, n, c in d.unknown_classes],
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

    def _gate(self, source: str) -> List[str]:
        if not self.measured:
            return [("No role is mapped, so the gate had nothing to measure and nothing here "
                     "passed; map roles to your tokens in mapping.json to check them.")]
        report = self.check.report
        head = report.summary().splitlines()[0]
        line = f"Checked {_and(self.check.foundations)}: {head}"
        if report.checked == 0:
            line = (f"Checked {_and(self.check.foundations)}. No contrast pair was measured, "
                    "since each needs both of its roles mapped, so the verdict covers the rule "
                    f"checks only: {head}")
        if self.findings:
            line += f" Each finding names our role, then your token in {source}."
        out = textwrap.wrap(line, WIDTH, break_long_words=False, break_on_hyphens=False)
        if self.findings:
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
        for miss in d.missing:
            lines.append(f"- {miss.where} references {miss.value}, which the system does not "
                         "have; add it to the system, or point the reference at a token it "
                         "has.")
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

    @staticmethod
    def _unread(d: Drift) -> List[str]:
        """What the scan did not read or measure, each with the fix."""
        lines = []
        for file, why in d.skipped:
            # The scanner writes a reason as what the file is or cannot do.
            lines.append(f"- {file} {_sentence(why)}" if why[:1].islower()
                         else f"- {file} was not read: {_sentence(why)}")
        for file, line, kind, written, why in d.not_read:
            if why:
                lines.append(f"- {file}:{line} was not measured ({kind}): {_sentence(why)}")
            else:
                lines.append(f"- {file}:{line} writes {_brief(written)} ({kind}), which the "
                             "scan does not measure; check it by hand, or write it in a form "
                             "the scan reads (a longhand property or a var() to a token).")
        for file, line, cls in d.unknown_classes:
            lines.append(f"- {file}:{line} uses the class {cls}, which names no token in the "
                         "system; add the token to the system, or use a class that names one "
                         "it has.")
        return lines


def _reading_face(checked: TokenSet, role: str) -> Optional[str]:
    try:
        face = checked.resolve(role)["fontFamily"]
    except (AliasError, KeyError, TypeError, ValueError):
        return None
    return face if isinstance(face, str) else (face[0] if face else None)


def _confirm(mapping: Mapping, checked: TokenSet, foundations: Sequence[str],
             deleted: Sequence[str] = ()) -> List[str]:
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
    if "motion" not in mapping.axes and "motion" not in deleted:
        out.append("The system has no reduced-motion mode in the mapping, so the motion checks "
                   "under reduced motion did not run; if it has one, map it as the motion axis "
                   "in mapping.json.")
    if "scheme" not in mapping.axes and "scheme" not in deleted:
        out.append("The system has no dark mode in the mapping, so dark was not checked; if it "
                   "has one, map it as the scheme axis in mapping.json.")
    return out


def _owner_notes(mapping: Mapping, name: str) -> List[str]:
    """The notes view() gives for the owner's "not mapped" entries, which
    the report lists itself under How it was checked."""
    return [ROLE_LEFT_OUT.format(role=r, name=name)
            for r, m in mapping.roles.items() if m.token is None] \
        + [AXIS_LEFT_OUT.format(axis=a, name=name)
           for a, m in mapping.axes.items() if m.source is None]


def _finding(text: str, mapping: Mapping) -> str:
    """A gate message in the system's names; a set with no mode axis
    prints an empty context, which is dropped."""
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
    structure = ([p.message for p in validate(ts)] if checked is not ts
                 else [p.message for p in result.problems])
    report = result.report
    findings = [_finding(_MOVE.sub(_THEIR_FIX, f.message()), mapping) for f in report.findings]
    findings += [_finding(f"{c.message} (in {c.mode})" if c.mode else c.message, mapping)
                 for c in report.failures]
    decisions = [f"{r} is mapped to {m.token} by name only; confirm it in {mapping_name}."
                 for r, m in mapping.roles.items() if m.by == "name" and m.token is not None]
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
    return Enhanced(imported, mapping, result, structure,
                    drift(ts, scanned) if scanned is not None else None,
                    _confirm(mapping, checked, result.foundations, list(deleted_axes(ts, mapping))),
                    decisions, findings,
                    list(merge_notes))
