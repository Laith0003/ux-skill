"""The component contract schema and its structural checks.

A contract says what a component is made of (parts, each with how it
behaves under right to left), which variants and states it supports
(variant values are exhaustive; states come from one fixed list), which
semantic role each part binds per variant and state, which contrast
pairings it needs, the surfaces it may sit on, its accessibility
minimums, copy rules per state, do and do not lists, and where it came
from (provenance). Governance: agents author at experimental; ready needs
the objective thresholds in PROMOTION; deprecated names a replacement.

These checks read the contract alone. bind.py checks it against a built
token set. Every problem names the contract, the field and the fix.
"""
from __future__ import annotations

import datetime
import math
import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, List, Mapping, Optional, Sequence, Tuple, Union

from engine.contracts.yamlite import YamlError, loads

STATUSES: Tuple[str, ...] = ("experimental", "ready", "deprecated")
CATEGORIES: Tuple[str, ...] = ("action", "input", "selection", "container", "overlay",
                               "feedback")
# Categories a person operates directly: they need a target size, a focus
# state and a focus ring.
INTERACTIVE: Tuple[str, ...] = ("action", "input", "selection")
# The fixed state list, in the order a contract lists them.
STATES: Tuple[str, ...] = ("default", "hover", "pressed", "focus", "selected", "disabled",
                           "loading", "error", "empty")
# States whose words change, so each needs copy rules when declared.
WORDED_STATES: Tuple[str, ...] = ("default", "loading", "error", "empty")
RTL_BEHAVIORS: Tuple[str, ...] = ("logical", "mirror", "fixed")
# Every property a binding may set, with the token type its role must have.
# border-width and border-color draw every side of a part. divider-width and
# divider-color draw one side only: the side where a part inside a group
# meets the rest of the group (the inline end of a part at the start, the
# inline start of a part at the end, the end edge of a sticky column); its
# other sides lie on the group's own edge. edge-weight is the full weight of
# a part's edge in a state: the border keeps border-width, and the difference
# is drawn inside it as an inset box-shadow in the border color (never an
# outline, which the focus ring owns), so a heavier edge never moves the layout.
PROPERTY_TYPES: Mapping[str, str] = MappingProxyType({
    "fill": "color", "text": "color", "icon": "color", "border-color": "color",
    "focus-ring": "color", "divider-color": "color",
    "border-width": "dimension", "focus-ring-width": "dimension", "divider-width": "dimension",
    "edge-weight": "dimension",
    "focus-ring-offset": "dimension", "border-style": "strokeStyle",
    "radius": "dimension", "padding-inline": "dimension", "padding-block": "dimension",
    "gap": "dimension", "stack-gap": "dimension", "min-size": "dimension",
    "max-width": "dimension",
    "font": "typography", "font-weight": "fontWeight",
    "shadow": "shadow", "layer": "number",
    "transition-duration": "duration", "transition-curve": "cubicBezier",
    "enter-duration": "duration", "enter-curve": "cubicBezier", "enter-distance": "dimension",
    "exit-duration": "duration", "exit-curve": "cubicBezier", "exit-distance": "dimension",
    "direction-sign": "number",
})
# The WCAG criteria a contract pairing may cite, with the ratio each sets.
# Any other floor is the contract's own and says so ("system").
CRITERIA: Mapping[str, float] = MappingProxyType({"1.4.3": 4.5, "1.4.6": 7.0, "1.4.11": 3.0})
# How messages list the criteria a pairing may cite.
_CITABLE = "'1.4.3' (text, 4.5:1), '1.4.6' (text, 7:1, AAA), '1.4.11' (non-text, 3:1)"
_WCAG_NUMBER = re.compile(r"[1-4]\.[0-9]+\.[0-9]+")
SYSTEM = "system"
# Bound roles that carry meaning by color, so the contract names a second cue.
COLOR_SIGNALS: Tuple[str, ...] = ("color.status.", "color.action.danger", "color.line.selected",
                                  "color.surface.selected", "border.active")
# What ready needs, in words; promotion_problems checks each.
PROMOTION: Tuple[str, ...] = (
    "provenance.figma.node names the component in the source file",
    "provenance.figma.lastVerified is the date it was last read, as YYYY-MM-DD",
    "provenance.figma.variantCount equals the product of the variant value counts",
    "provenance.drift is empty",
)

REQUIRED_KEYS: Tuple[str, ...] = ("name", "status", "category", "description", "parts",
                                  "variants", "states", "tokens", "contrast", "surfaces",
                                  "a11y", "copy", "usage", "provenance")
OPTIONAL_KEYS: Tuple[str, ...] = ("replacement",)
# The variant that places a part on a surface other than the contract's own:
# any value but "default" names color.surface.<value>, which the part's
# bindings under it sit on and its pairings may name.
PLACEMENT = "surface"

_NAME = re.compile(r"[a-z][a-z0-9]*(-[a-z0-9]+)*")
_ROLE = re.compile(r"[a-z][a-z0-9-]*(\.[a-z0-9-]+)+")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


@dataclass(frozen=True)
class ContractProblem:
    contract: str
    rule: str
    message: str


class ContractError(ValueError):
    """A contract that cannot be read; `problems` holds every reason."""

    def __init__(self, problems: Sequence[ContractProblem]):
        self.problems: Tuple[ContractProblem, ...] = tuple(problems)
        super().__init__("\n".join(p.message for p in self.problems))


@dataclass(frozen=True)
class Part:
    name: str
    rtl_behavior: str


@dataclass(frozen=True)
class Variant:
    name: str
    values: Tuple[str, ...]
    default: str


@dataclass(frozen=True)
class Binding:
    part: str
    property: str
    role: str
    when: Tuple[Tuple[str, str], ...] = ()
    state: Optional[str] = None

    def label(self) -> str:
        """How messages name the binding: part.property with its conditions."""
        conditions = [f"{k}={v}" for k, v in self.when] + ([self.state] if self.state else [])
        return f"{self.part}.{self.property}" + (f" ({', '.join(conditions)})"
                                                 if conditions else "")


@dataclass(frozen=True)
class ContrastRule:
    fg: str
    bg: str
    minimum: float
    criterion: str
    high: Optional[float] = None


@dataclass(frozen=True)
class A11y:
    target: str
    label: str
    cue: str


@dataclass(frozen=True)
class Provenance:
    node: Optional[str]
    variant_count: Optional[int]
    last_verified: Optional[str]
    drift: Tuple[str, ...]


@dataclass(frozen=True)
class Contract:
    name: str
    status: str
    category: str
    description: str
    replacement: Optional[str]
    parts: Tuple[Part, ...]
    variants: Tuple[Variant, ...]
    states: Tuple[str, ...]
    tokens: Tuple[Binding, ...]
    contrast: Tuple[ContrastRule, ...]
    surfaces: Tuple[str, ...]
    a11y: A11y
    copy: Tuple[Tuple[str, Tuple[str, ...]], ...]
    do: Tuple[str, ...]
    dont: Tuple[str, ...]
    provenance: Provenance

    @property
    def interactive(self) -> bool:
        return self.category in INTERACTIVE

    def variant_product(self) -> int:
        """How many variant combinations the enums allow: the count a
        design file's component set holds when it is exhaustive."""
        n = 1
        for v in self.variants:
            n *= len(v.values)
        return n

    def roles(self) -> Tuple[str, ...]:
        """Every role the contract binds, in first-use order."""
        seen: List[str] = []
        for b in self.tokens:
            if b.role not in seen:
                seen.append(b.role)
        return tuple(seen)


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _a(word: str) -> str:
    return ("an " if word[:1] in "aeiou" else "a ") + word


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) \
        and math.isfinite(value)


class _Checker:
    """Collects problems for one contract while it is read."""

    def __init__(self, name: str):
        self.name = name
        self.problems: List[ContractProblem] = []

    def add(self, rule: str, message: str) -> None:
        self.problems.append(ContractProblem(self.name, rule, f"{self.name}: {message}"))

    def texts(self, value: Any, field: str, what: str) -> Tuple[str, ...]:
        if not isinstance(value, list) or not value or not all(_is_text(v) for v in value):
            self.add("bad-list", f"{field} is {value!r}; write a list of one or more {what}")
            return ()
        return tuple(v.strip() for v in value)


def _date_ok(value: str) -> bool:
    if not _DATE.fullmatch(value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _parts(c: _Checker, raw: Any) -> Tuple[Part, ...]:
    if not isinstance(raw, list) or not raw:
        c.add("bad-parts", f"parts is {raw!r}; list each part as {{name, rtlBehavior}}, for "
                           "example - {name: container, rtlBehavior: logical}")
        return ()
    out: List[Part] = []
    for i, item in enumerate(raw):
        where = f"parts[{i}]"
        if not isinstance(item, dict) or set(item) != {"name", "rtlBehavior"}:
            c.add("bad-parts", f"{where} is {item!r}; give it exactly name and rtlBehavior")
            continue
        name, rtl = item["name"], item["rtlBehavior"]
        if not (isinstance(name, str) and _NAME.fullmatch(name)):
            c.add("bad-parts", f"{where}.name is {name!r}; use a lowercase name with '-', "
                               "for example leading-icon")
            continue
        if rtl not in RTL_BEHAVIORS:
            c.add("bad-rtl", f"part {name} has rtlBehavior {rtl!r}; use logical (placed with "
                             "logical properties), mirror (the glyph flips under rtl) or fixed "
                             "(never flips, such as a phone number)")
        if any(p.name == name for p in out):
            c.add("bad-parts", f"part {name} is listed twice; keep one")
            continue
        out.append(Part(name, rtl if rtl in RTL_BEHAVIORS else "logical"))
    return tuple(out)


def _variants(c: _Checker, raw: Any) -> Tuple[Variant, ...]:
    if not isinstance(raw, list):
        c.add("bad-variants", f"variants is {raw!r}; list each as {{name, values, default}}, "
                              "or write [] when the component has none")
        return ()
    out: List[Variant] = []
    for i, item in enumerate(raw):
        where = f"variants[{i}]"
        if not isinstance(item, dict) or set(item) != {"name", "values", "default"}:
            c.add("bad-variants", f"{where} is {item!r}; give it exactly name, values and "
                                  "default")
            continue
        name, values, default = item["name"], item["values"], item["default"]
        if not (isinstance(name, str) and _NAME.fullmatch(name)):
            c.add("bad-variants", f"{where}.name is {name!r}; use a lowercase name with '-'")
            continue
        if not (isinstance(values, list) and len(values) >= 2
                and all(isinstance(v, str) and _NAME.fullmatch(v) for v in values)
                and len(set(values)) == len(values)):
            c.add("bad-variants", f"variant {name} values are {values!r}; list every value the "
                                  "component supports, at least two, each a distinct lowercase "
                                  "name")
            continue
        if default not in values:
            c.add("bad-variants", f"variant {name} default is {default!r}; pick one of "
                                  f"{values}")
            continue
        if any(v.name == name for v in out):
            c.add("bad-variants", f"variant {name} is listed twice; keep one")
            continue
        out.append(Variant(name, tuple(values), default))
    return tuple(out)


def _states(c: _Checker, raw: Any, category: Any) -> Tuple[str, ...]:
    if not isinstance(raw, list) or not raw:
        c.add("bad-states", f"states is {raw!r}; list the states it supports from {list(STATES)}")
        return ("default",)
    for i, s in enumerate(raw):
        if not isinstance(s, str):
            c.add("bad-states", f"states[{i}] is {s!r}; write each state as one word from "
                                f"{list(STATES)}")
    raw = [s for s in raw if isinstance(s, str)]
    unknown = [s for s in raw if s not in STATES]
    if unknown:
        c.add("bad-states", f"states {unknown} are not in the fixed list; use only "
                            f"{list(STATES)}")
    if len(set(raw)) != len(raw):
        c.add("bad-states", "states lists a state twice; keep each once")
    states = tuple(s for s in STATES if s in raw)
    if "default" not in states:
        c.add("bad-states", "states has no default; every component has a default state, so "
                            "add it")
    if category in INTERACTIVE and "focus" not in states:
        c.add("bad-states", f"{_a(category)} component is operated directly, so it needs a "
                            "focus state; add focus to states")
    return states


def _when(c: _Checker, raw: Any, where: str,
          variants: Tuple[Variant, ...]) -> Tuple[Tuple[str, str], ...]:
    if raw is None:
        return ()
    if not isinstance(raw, dict) or not raw:
        c.add("bad-binding", f"{where}.when is {raw!r}; write a map of variant to value, for "
                             "example {emphasis: primary}")
        return ()
    names = {v.name: v for v in variants}
    out: List[Tuple[str, str]] = []
    for key, value in raw.items():
        if key not in names:
            c.add("bad-binding", f"{where}.when names {key!r}, which is not a variant; use one "
                                 f"of {sorted(names) or 'no variant (declare it first)'}")
        elif value not in names[key].values:
            c.add("bad-binding", f"{where}.when sets {key} to {value!r}; use one of "
                                 f"{list(names[key].values)}")
        else:
            out.append((key, value))
    order = [v.name for v in variants]
    return tuple(sorted(out, key=lambda kv: order.index(kv[0])))


def _role_ok(c: _Checker, role: Any, where: str) -> bool:
    if isinstance(role, str) and role.startswith(("#", "{")):
        c.add("not-a-role", f"{where} is {role!r}; bind a semantic role by its path, for example "
                            "color.action.primary, never a hex or an alias")
        return False
    if not (isinstance(role, str) and _ROLE.fullmatch(role)):
        c.add("not-a-role", f"{where} is {role!r}; write a semantic role path such as "
                            "color.text.default")
        return False
    return True


def _tokens(c: _Checker, raw: Any, parts: Tuple[Part, ...], variants: Tuple[Variant, ...],
            states: Tuple[str, ...]) -> Tuple[Binding, ...]:
    if not isinstance(raw, list) or not raw:
        c.add("bad-binding", f"tokens is {raw!r}; list each binding as {{part, property, role}}, "
                             "with optional when and state")
        return ()
    part_names = {p.name for p in parts}
    out: List[Binding] = []
    for i, item in enumerate(raw):
        where = f"tokens[{i}]"
        if not isinstance(item, dict) or not {"part", "property", "role"} <= set(item) \
                or not set(item) <= {"part", "property", "role", "when", "state"}:
            c.add("bad-binding", f"{where} is {item!r}; give it part, property and role, and "
                                 "optionally when and state")
            continue
        ok = True
        if not isinstance(item["part"], str) or item["part"] not in part_names:
            c.add("bad-binding", f"{where}.part is {item['part']!r}; use one of the declared "
                                 f"parts {sorted(part_names)}")
            ok = False
        if not isinstance(item["property"], str) or item["property"] not in PROPERTY_TYPES:
            c.add("bad-binding", f"{where}.property is {item['property']!r}; use one of "
                                 f"{sorted(PROPERTY_TYPES)}")
            ok = False
        ok = _role_ok(c, item["role"], f"{where}.role") and ok
        before = len(c.problems)
        when = _when(c, item.get("when"), where, variants)
        ok = ok and len(c.problems) == before
        state = item.get("state")
        if state is not None and state not in states:
            c.add("bad-binding", f"{where}.state is {state!r}; use a declared state, one of "
                                 f"{list(states)}")
            ok = False
        if not ok:
            continue
        b = Binding(item["part"], item["property"], item["role"], when, state)
        if any((o.part, o.property, o.when, o.state) == (b.part, b.property, b.when, b.state)
               for o in out):
            c.add("duplicate-binding", f"{b.label()} is bound twice; keep one binding for it")
            continue
        out.append(b)
    return tuple(out)


def _contrast(c: _Checker, raw: Any, tokens: Tuple[Binding, ...],
              surfaces: Tuple[str, ...]) -> Tuple[ContrastRule, ...]:
    if not isinstance(raw, list):
        c.add("bad-contrast", f"contrast is {raw!r}; list each pairing as {{fg, bg, minimum, "
                              "criterion}}, or write [] when the component sets no color")
        return ()
    bound = {b.role for b in tokens}
    placed = {f"color.surface.{v}" for b in tokens for k, v in b.when
              if k == PLACEMENT and v != "default"}
    out: List[ContrastRule] = []
    for i, item in enumerate(raw):
        where = f"contrast[{i}]"
        keys = {"fg", "bg", "minimum", "criterion"}
        if not isinstance(item, dict) or not keys <= set(item) or not set(item) <= keys | {"high"}:
            c.add("bad-contrast", f"{where} is {item!r}; give it fg, bg, minimum and criterion, "
                                  "and optionally high")
            continue
        fg, bg, minimum, criterion = item["fg"], item["bg"], item["minimum"], item["criterion"]
        high = item.get("high")
        ok = _role_ok(c, fg, f"{where}.fg")
        ok = (bg == "surfaces" or _role_ok(c, bg, f"{where}.bg")) and ok
        if not (_is_number(minimum) and minimum >= 1):
            c.add("bad-contrast", f"{where}.minimum is {minimum!r}; write a ratio of 1 or more, "
                                  "such as 4.5")
            ok = False
        if not isinstance(criterion, str) or (criterion not in CRITERIA and criterion != SYSTEM):
            what = (", which is not a criterion this schema knows a contrast ratio for"
                    if isinstance(criterion, str) and _WCAG_NUMBER.fullmatch(criterion) else "")
            c.add("bad-contrast", f"{where}.criterion is {criterion!r}{what}; cite {_CITABLE} "
                                  "or system for a floor of your own")
            ok = False
        elif criterion in CRITERIA and _is_number(minimum) and minimum != CRITERIA[criterion]:
            c.add("bad-contrast", f"{where} cites WCAG {criterion} with {minimum:g}:1, but "
                                  f"{criterion} sets {CRITERIA[criterion]:g}:1; use that ratio, "
                                  "or cite system for a floor of your own")
            ok = False
        pair = f"{where} ({fg} on {bg})"
        if high is not None and not (_is_number(high) and high >= 1):
            c.add("bad-contrast", f"{where}.high is {high!r}; write the high-contrast ratio, 1 "
                                  "or more")
            ok = False
        elif high is not None and criterion in CRITERIA and high < CRITERIA[criterion]:
            c.add("bad-contrast", f"{pair} cites WCAG {criterion} with high {high:g}:1, but "
                                  f"{criterion} sets {CRITERIA[criterion]:g}:1 in every "
                                  "contrast mode; raise high to at least "
                                  f"{CRITERIA[criterion]:g}, or cite system for a floor of "
                                  "your own")
            ok = False
        elif high is not None and _is_number(minimum) and high < minimum:
            c.add("bad-contrast", f"{pair} sets high {high:g}:1, below its minimum of "
                                  f"{minimum:g}:1; high contrast never lowers a floor, so raise "
                                  f"high to at least {minimum:g}")
            ok = False
        if criterion == SYSTEM and high is None:
            c.add("bad-contrast", f"{where} sets a system floor with no high; write high, the "
                                  "ratio it needs under high contrast, so it is never raised "
                                  "without being meant")
            ok = False
        if isinstance(fg, str) and fg not in bound:
            c.add("unbound-pairing", f"{where}.fg {fg} is not bound in tokens; pair only roles "
                                     "the component uses, or bind it")
            ok = False
        if isinstance(bg, str) and bg != "surfaces" and bg not in bound and bg not in surfaces \
                and bg not in placed:
            c.add("unbound-pairing", f"{where}.bg {bg} is neither bound in tokens nor listed in "
                                     "surfaces; pair only roles the component uses or sits on")
            ok = False
        if bg == "surfaces" and not surfaces:
            c.add("unbound-pairing", f"{where}.bg is surfaces, but surfaces is empty; list the "
                                     "surfaces the component sits on")
            ok = False
        if ok:
            out.append(ContrastRule(fg, bg, float(minimum), criterion,
                                    None if high is None else float(high)))
    return tuple(out)


def _a11y(c: _Checker, raw: Any, category: Any, tokens: Tuple[Binding, ...],
          states: Tuple[str, ...]) -> A11y:
    if not isinstance(raw, dict) or set(raw) != {"target", "label", "cue"}:
        c.add("bad-a11y", f"a11y is {raw!r}; give it exactly target, label and cue")
        return A11y("none", "localized", "none")
    target, label, cue = raw["target"], raw["label"], raw["cue"]
    if category in INTERACTIVE:
        if target == "none" or not _role_ok(c, target, "a11y.target"):
            if target == "none":
                c.add("bad-a11y", f"{_a(category)} component is a target, so a11y.target "
                                  "names the role that sets its minimum size, such as "
                                  "layout.target.min")
        elif not any(b.property == "min-size" and b.role == target for b in tokens):
            c.add("bad-a11y", f"a11y.target is {target}, but no part binds min-size to it; bind "
                              "min-size on the part a person presses")
        if "focus" in states:
            for prop in ("focus-ring", "focus-ring-width", "focus-ring-offset"):
                if not any(b.property == prop and b.state == "focus" for b in tokens):
                    c.add("bad-a11y", f"{_a(category)} component shows focus, but no binding "
                                      f"sets {prop} in the focus state; bind it")
    elif target != "none":
        _role_ok(c, target, "a11y.target")
    if label != "localized":
        c.add("bad-a11y", f"a11y.label is {label!r}; write localized: every accessible name is "
                          "in the product's language, icon-only parts included")
    signals = sorted({b.role for b in tokens if b.role.startswith(COLOR_SIGNALS)})
    if not _is_text(cue):
        c.add("bad-a11y", f"a11y.cue is {cue!r}; name the second cue besides color, or write "
                          "none when the component shows no meaning by color")
        cue = "none"
    elif signals and cue.strip() == "none":
        c.add("bad-a11y", f"the component binds {', '.join(signals)}, which carry meaning by "
                          "color; a11y.cue must name the second cue (an icon, the words, a "
                          "heavier edge)")
    return A11y(target if isinstance(target, str) else "none", label, cue.strip())


def _copy(c: _Checker, raw: Any,
          states: Tuple[str, ...]) -> Tuple[Tuple[str, Tuple[str, ...]], ...]:
    if not isinstance(raw, dict):
        c.add("bad-copy", f"copy is {raw!r}; map each state to its list of copy rules")
        return ()
    out: List[Tuple[str, Tuple[str, ...]]] = []
    for state, rules in raw.items():
        if state not in states:
            c.add("bad-copy", f"copy names {state!r}, which is not a declared state; use one of "
                              f"{list(states)}")
            continue
        texts = c.texts(rules, f"copy.{state}", "copy rules")
        for rule in texts:
            if len(rule) > 1 and rule[0] in "\"'\u201c" and rule[-1] in "\"'\u201d":
                c.add("copy-is-a-string", f"copy.{state} holds the literal {rule}; copy holds "
                                          "rules, not strings: say what the words do, for "
                                          "example Start with a verb that names the result")
        out.append((state, texts))
    given = {s for s, _ in out}
    for state in WORDED_STATES:
        if state in states and state not in given:
            c.add("bad-copy", f"the {state} state changes what the component says, so copy "
                              f"needs rules for {state}")
    order = list(STATES)
    return tuple(sorted(out, key=lambda kv: order.index(kv[0])))


def _provenance(c: _Checker, raw: Any) -> Provenance:
    empty = Provenance(None, None, None, ())
    if not isinstance(raw, dict) or set(raw) != {"figma", "drift"} \
            or not isinstance(raw["figma"], dict) \
            or set(raw["figma"]) != {"node", "variantCount", "lastVerified"}:
        c.add("bad-provenance", f"provenance is {raw!r}; write figma: {{node, variantCount, "
                                "lastVerified}} and drift: [], with null for what is not "
                                "known yet")
        return empty
    figma = raw["figma"]
    node, count, verified, drift = (figma["node"], figma["variantCount"],
                                    figma["lastVerified"], raw["drift"])
    if node is not None and not _is_text(node):
        c.add("bad-provenance", f"provenance.figma.node is {node!r}; write the node id as text, "
                                "such as '12:345', or null")
        node = None
    if count is not None and not (isinstance(count, int) and not isinstance(count, bool)
                                  and count >= 1):
        c.add("bad-provenance", f"provenance.figma.variantCount is {count!r}; write the number "
                                "of variants the design file's component set holds, or null")
        count = None
    if verified is not None and not (isinstance(verified, str) and _date_ok(verified)):
        c.add("bad-provenance", f"provenance.figma.lastVerified is {verified!r}; write the date "
                                "it was last read as YYYY-MM-DD, or null")
        verified = None
    if not isinstance(drift, list) or not all(_is_text(d) for d in drift):
        c.add("bad-provenance", f"provenance.drift is {drift!r}; list each difference between "
                                "the contract and the design file as text, or write []")
        drift = []
    return Provenance(node, count, verified, tuple(d.strip() for d in drift))


def promotion_problems(contract: Contract) -> List[ContractProblem]:
    """What stands between the contract and ready, one problem per unmet
    threshold in PROMOTION."""
    c = _Checker(contract.name)
    p = contract.provenance
    if p.node is None:
        c.add("promotion", "provenance.figma.node is null; ready needs the node of the "
                           "component in the design file, so read it there first")
    if p.last_verified is None:
        c.add("promotion", "provenance.figma.lastVerified is null; ready needs the date the "
                           "node was last read")
    if p.variant_count != contract.variant_product():
        c.add("promotion", f"provenance.figma.variantCount is {p.variant_count}, but the variant "
                           f"enums allow {contract.variant_product()}; ready needs the design "
                           "file to hold every combination, so settle the difference in the "
                           "file or the enums")
    if p.drift:
        c.add("promotion", f"provenance.drift lists {len(p.drift)} difference"
                           f"{'' if len(p.drift) == 1 else 's'}; ready needs none, so resolve "
                           "each in the design file or the contract")
    return c.problems


def contract_problems(data: Any, source: str) -> Tuple[Optional[Contract], List[ContractProblem]]:
    """Read one contract's data. Returns the contract (None when it cannot
    be built) and every structural problem. `source` is the file name or
    a label; a name that differs from a .yaml file's stem is a problem."""
    label = data.get("name") if isinstance(data, dict) and isinstance(data.get("name"), str) \
        else Path(source).stem
    c = _Checker(label)
    if data is None:
        c.add("not-a-map", f"{source} is empty; write the contract's fields: "
                           f"{', '.join(REQUIRED_KEYS)}")
        return None, c.problems
    if not isinstance(data, dict):
        held = ("a list" if isinstance(data, list) else "text" if isinstance(data, str)
                else "true or false" if isinstance(data, bool)
                else "a number" if isinstance(data, (int, float)) else type(data).__name__)
        c.add("not-a-map", f"{source} holds {held}; a contract is a map of "
                           f"{', '.join(REQUIRED_KEYS)}")
        return None, c.problems
    missing = [k for k in REQUIRED_KEYS if k not in data]
    unknown = [k for k in data if k not in REQUIRED_KEYS + OPTIONAL_KEYS]
    if missing:
        c.add("missing-key", f"missing {', '.join(missing)}; every contract has "
                             f"{', '.join(REQUIRED_KEYS)}")
    if unknown:
        what = "is not a contract field" if len(unknown) == 1 else "are not contract fields"
        c.add("unknown-key", f"{', '.join(map(repr, unknown))} {what}; "
                             f"use only {', '.join(REQUIRED_KEYS + OPTIONAL_KEYS)}")
    if missing:
        return None, c.problems
    name = data["name"]
    if not (isinstance(name, str) and _NAME.fullmatch(name)):
        c.add("bad-name", f"name is {name!r}; use a lowercase name with '-', such as text-field")
    elif source.endswith(".yaml") and Path(source).stem != name:
        c.add("bad-name", f"name is {name!r} but the file is {Path(source).name}; name the file "
                          f"{name}.yaml or change the name")
    status, category = data["status"], data["category"]
    if status not in STATUSES:
        c.add("bad-status", f"status is {status!r}; use {', '.join(STATUSES)} (agents author at "
                            "experimental)")
    if category not in CATEGORIES:
        c.add("bad-category", f"category is {category!r}; use one of {list(CATEGORIES)}")
    replacement = data.get("replacement")
    if status == "deprecated" and not (isinstance(replacement, str) and _NAME.fullmatch(replacement)
                                       and replacement != name):
        c.add("replacement", f"a deprecated contract names its replacement; set replacement to "
                             f"the contract to use instead of {name}")
    if status != "deprecated" and replacement is not None:
        c.add("replacement", f"replacement is set but status is {status}; only a deprecated "
                             "contract names a replacement, so remove it")
    description = data["description"]
    if not _is_text(description):
        shown = "empty" if isinstance(description, str) or description is None \
            else repr(description)
        c.add("bad-description", f"description is {shown}; say in one line what the "
                                 "component does and when to use it")
    parts = _parts(c, data["parts"])
    variants = _variants(c, data["variants"])
    states = _states(c, data["states"], category)
    tokens = _tokens(c, data["tokens"], parts, variants, states)
    surfaces_raw = data["surfaces"]
    if not isinstance(surfaces_raw, list):
        c.add("bad-surfaces", f"surfaces is {surfaces_raw!r}; list the surface roles the "
                              "component may sit on, or write []")
        surfaces: Tuple[str, ...] = ()
    else:
        surfaces = tuple(s for i, s in enumerate(surfaces_raw)
                         if _role_ok(c, s, f"surfaces[{i}]"))
    contrast = _contrast(c, data["contrast"], tokens, surfaces)
    a11y = _a11y(c, data["a11y"], category, tokens, states)
    copy = _copy(c, data["copy"], states)
    usage = data["usage"]
    if not isinstance(usage, dict) or set(usage) != {"do", "dont"}:
        c.add("bad-usage", f"usage is {usage!r}; give it do and dont, each a list of short "
                           "rules")
        do: Tuple[str, ...] = ()
        dont: Tuple[str, ...] = ()
    else:
        do = c.texts(usage["do"], "usage.do", "rules")
        dont = c.texts(usage["dont"], "usage.dont", "rules")
    provenance = _provenance(c, data["provenance"])
    if c.problems:
        return None, c.problems
    contract = Contract(name, status, category, data["description"].strip(), replacement,
                        parts, variants, states, tokens, contrast, surfaces, a11y, copy, do,
                        dont, provenance)
    if provenance.variant_count is not None \
            and provenance.variant_count != contract.variant_product() and not provenance.drift:
        c.add("variant-count", f"provenance.figma.variantCount is {provenance.variant_count} but "
                               f"the variant enums allow {contract.variant_product()}; a "
                               "mismatch is drift, so record it in provenance.drift, never "
                               "change the count to fit")
    if status == "ready":
        c.problems.extend(promotion_problems(contract))
    return (None if c.problems else contract), c.problems


def read_contract(text: str, source: str = "<contract>") -> Contract:
    """Read a contract from YAML text. Raises ContractError with every
    problem, a YAML error included."""
    try:
        data = loads(text, source)
    except YamlError as exc:
        raise ContractError([ContractProblem(Path(source).stem, "yaml", str(exc))]) from None
    contract, problems = contract_problems(data, source)
    if contract is None:
        raise ContractError(problems)
    return contract


def load_contract(path: Union[str, Path]) -> Contract:
    """Read a contract file. Raises ContractError naming the file."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ContractError([ContractProblem(p.stem, "unreadable",
                                             f"{p} cannot be read ({type(exc).__name__}); save it "
                                             "as UTF-8 text in a folder you can read")]) from None
    return read_contract(text, p.name)
