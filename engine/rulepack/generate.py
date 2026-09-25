"""Write the AI rule pack from a built token set, the contracts, the
decision records and the guidance.

The pack is a folder of markdown (and the contract YAML) that an agent or
a person loads one path at a time:

    rule-pack/README.md                   the router: which file for which task
    rule-pack/<foundation>/architecture.md  layers, principles, roles, choices, modes,
                                            how to change it, its decisions and contracts
    rule-pack/<foundation>/reference.md     every token as built, per mode
    rule-pack/<foundation>/audit.md         the audit procedure: classify and cite
    rule-pack/<foundation>/handoff.md       the handoff contract for developers
    rule-pack/content.md, direction.md      content and right-to-left rules
    rule-pack/contracts/<name>.yaml         the component contracts, as written
    rule-pack/decisions/                    the decision records and HISTORY.md

Every heading is fixed (the *_HEADINGS tuples), every value comes from the
build, and nothing depends on the clock, so the same system gives the same
bytes.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Union

from engine.contracts.bind import pairings_of, validate_contracts
from engine.contracts.library import SEED_DIR, load_folder
from engine.contracts.schema import Binding, Contract, ContractError
from engine.foundations.build import FOUNDATIONS
from engine.foundations.foundation import Foundation
from engine.foundations.gate import (
    HIGH_FLOOR, HIGH_NON_TEXT, HIGH_TEXT, WCAG_RATIOS, Pairing, required)
from engine.foundations.modes import CSS_AXES, FOUNDATION_AXES, contexts, parse, sparse
from engine.foundations.tokens import TokenSet, alias_target, is_alias
from engine.foundations.values import TYPES, TYPOGRAPHY_FIELDS, css_names
from engine.rulepack.guidance import (
    GUIDANCE_DIR, SHARED, Guidance, RoleEntry, catalog_by_foundation, guidance_problems,
    load_guidance, role_catalog)
from engine.rulepack.records import RECORDS_DIR, Record, RecordError, load_records, record_sources

PACK = "rule-pack"
FILES: Tuple[str, ...] = ("architecture.md", "reference.md", "audit.md", "handoff.md")
ARCHITECTURE_HEADINGS: Tuple[str, ...] = ("Summary", "Layers", "Principles", "Roles",
                                          "Choosing", "Modes", "Changing the system",
                                          "Decisions", "Contracts")
REFERENCE_HEADINGS: Tuple[str, ...] = ("Semantic roles", "Primitives")
COLOR_REFERENCE_HEADINGS: Tuple[str, ...] = REFERENCE_HEADINGS + ("Pairings",)
AUDIT_HEADINGS: Tuple[str, ...] = ("Before you audit", "Scope", "What the gate checks",
                                   "Beyond the gate", "Classify and cite", "Severity", "Report")
HANDOFF_HEADINGS: Tuple[str, ...] = ("Inputs", "CSS custom properties", "Using the roles",
                                     "Implementation notes", "Common mistakes",
                                     "What a handoff does not do")
README_HEADINGS: Tuple[str, ...] = ("Load one path per task", "Foundations", "Contracts",
                                    "Rules for every task")

# The WCAG criteria at level AAA that a check or pairing may cite; the
# gate applies each only where the system chose to.
AAA: Tuple[str, ...] = ("1.4.6", "1.4.8", "2.3.3", "2.5.5")
# The usage.do openings that say which binding wins when two apply at
# once: one for a state over no state and more conditions over fewer, one
# for two states at once.
PRECEDENCE_OPENINGS: Tuple[str, str] = ("Apply the binding for a state",
                                        "When two states apply at once")


class RulePackError(ValueError):
    """The rule pack cannot be written; `problems` names every reason and
    its fix."""

    def __init__(self, problems: Sequence[str]):
        self.problems: Tuple[str, ...] = tuple(problems)
        super().__init__("\n".join(self.problems))


def _fmt(type_: str, value: Any) -> str:
    """A resolved value as CSS would print it; a typography composite as
    its five fields."""
    if type_ == "typography":
        parts = []
        for key, (field_type, css) in TYPOGRAPHY_FIELDS.items():
            text = TYPES[field_type].css(value[key])
            if field_type == "fontFamily":
                text = text.split(",")[0].strip()
            parts.append(f"{css} {text}")
        return ", ".join(parts)
    return TYPES[type_].css(value)


def _cell(text: str) -> str:
    return text.replace("|", "/")


def _context_label(mode: str, ts: TokenSet) -> str:
    return sparse(mode, ts.axes) or "base"


def _foundation_contexts(f: Foundation, ts: TokenSet) -> List[str]:
    return contexts([a for a in FOUNDATION_AXES.get(f.name, ()) if a in ts.axes], ts.axes)


def _varies(ts: TokenSet, path: str) -> List[str]:
    """The axes a token's overrides actually use, in axis order."""
    used = {a for key in ts.get(path).modes for a in parse(key, ts.axes)}
    return [a for a in ts.axes if a in used]


def _tokens_of(ts: TokenSet, f: Foundation, layer: str) -> List[Any]:
    return [t for t in ts.tokens() if t.layer == layer and t.path.split(".", 1)[0] == f.name]


def _criterion_words(criterion: str) -> str:
    if criterion == "system":
        return "our rule"
    if criterion.startswith(HIGH_FLOOR):
        return f"our floor over WCAG {criterion[len(HIGH_FLOOR):]}"
    if criterion in WCAG_RATIOS or criterion[:1].isdigit():
        return f"WCAG {criterion}" + (" (AAA)" if criterion in AAA else "")
    return criterion


def _axis_words(axis: str, ts: TokenSet) -> str:
    """How one axis is set on the page, from the attribute and media
    feature tokens.css writes for it."""
    values = ts.axes[axis]
    attr, media = CSS_AXES.get(axis, (f"data-{axis}", ""))
    others = " or ".join(f'{attr}="{v}"' for v in values[1:])
    text = f"{axis} ({', '.join(values)}): {others} on the html element"
    if media:
        text += f", or the media query {media} unless {attr}=\"{values[0]}\" is set"
    return text


_HIGH_MODE = "contrast:high"


def _high_cell(p: Pairing, ts: TokenSet) -> str:
    """The minimum a pairing must meet under high contrast, and whose it is."""
    high, criterion = required(p, _HIGH_MODE, ts.axes)
    if p.high is not None:
        return f"{high:g}:1 (pinned)"
    if criterion.startswith(HIGH_FLOOR):
        return f"{high:g}:1 (our floor)"
    return f"{high:g}:1 (WCAG {criterion}{', AAA' if criterion in AAA else ''})"


def _pairing_source(p: Pairing) -> str:
    """A contract pairing with a floor of its own gets the contract's name
    as its criterion (bind._pairings); that floor is ours."""
    return "our floor" if p.criterion.startswith("the ") else _criterion_words(p.criterion)


def contract_pairing_rows(contracts: Sequence[Contract]) -> List[Tuple[str, Pairing]]:
    """(contract name, pairing) for every pairing the contracts declare,
    each once per contract, in the order they declare them."""
    out: List[Tuple[str, Pairing]] = []
    for name, p in pairings_of(contracts):
        if (name, p) not in out:
            out.append((name, p))
    return out


def _compatible(a: Binding, b: Binding) -> bool:
    ours, theirs = dict(a.when), dict(b.when)
    return all(ours[k] == theirs[k] for k in ours.keys() & theirs.keys())


def _meetings(contract: Contract) -> List[Tuple[Binding, Binding]]:
    """Pairs of bindings of one part and property, naming different roles,
    that can apply at once: no variant they both set takes two values."""
    out = []
    tokens = contract.tokens
    for i, a in enumerate(tokens):
        for b in tokens[i + 1:]:
            if (a.part, a.property) == (b.part, b.property) and a.role != b.role \
                    and _compatible(a, b):
                out.append((a, b))
    return out


def state_pairs(contract: Contract) -> List[Tuple[str, str]]:
    """The pairs of states whose bindings can meet that way, in the order
    of the contract's states."""
    order = {s: i for i, s in enumerate(contract.states)}
    pairs = []
    for a, b in _meetings(contract):
        if a.state and b.state and a.state != b.state:
            pair = tuple(sorted((a.state, b.state), key=lambda s: order.get(s, len(order))))
            if pair not in pairs:
                pairs.append(pair)
    return sorted(pairs, key=lambda q: (order.get(q[0], 0), order.get(q[1], 0)))


def overlaps(contract: Contract) -> Tuple[bool, bool]:
    """Whether two bindings of one part and property, naming different
    roles, can apply at once, as (one with a state and one without, or
    with more variant conditions than the other; two different states)."""
    conditions = states = False
    for a, b in _meetings(contract):
        if a.state and b.state and a.state != b.state:
            states = True
        elif (a.when, a.state) != (b.when, b.state):
            conditions = True
    return conditions, states


def precedence_lines(contract: Contract) -> List[str]:
    """The usage.do lines in which the contract says which binding wins."""
    return [line for line in contract.do if line.startswith(PRECEDENCE_OPENINGS)]


def _precedence_problems(contracts: Sequence[Contract]) -> List[str]:
    out = []
    for c in contracts:
        lines = precedence_lines(c)
        for needed, opening in zip(overlaps(c), PRECEDENCE_OPENINGS):
            if needed and not any(line.startswith(opening) for line in lines):
                out.append(f"{c.name}: two of its bindings for one part and property can apply "
                           f"at once, and usage.do does not say which wins; add a line that "
                           f"starts \"{opening}\"")
    return out


# ------------------------------------------------------------- architecture

def _architecture(f: Foundation, g: Guidance, ts: TokenSet, entries: Sequence[RoleEntry],
                  records: Sequence[Record], contracts: Sequence[Contract]) -> str:
    prims = _tokens_of(ts, f, "primitive")
    families: Dict[str, int] = {}
    for t in prims:
        families[t.path.rsplit(".", 1)[0]] = families.get(t.path.rsplit(".", 1)[0], 0) + 1
    axes = [a for a in FOUNDATION_AXES.get(f.name, ()) if a in ts.axes]
    lines = [f"# {g.title} architecture", "", "## Summary", "", g.section("Summary"), "",
             "## Layers", "",
             f"Two layers (decisions/two-layers.md): {len(prims)} primitives hold literal "
             f"values and never vary by mode; {len(entries)} semantic roles alias them, and "
             "only roles carry per-mode values. Components bind roles, never primitives.", "",
             "Primitive families: " + ", ".join(f"{name} ({n})" for name, n in families.items())
             + ".", "",
             ("Roles vary on " + ", ".join(axes) + "." if axes
              else "Roles vary on no mode axis."), "",
             "## Principles", "", g.section("Principles"), "", "## Roles", ""]
    lines += [f"- `{e.path}` ({e.type}): {e.description}" for e in entries]
    lines += ["", "## Choosing", "", g.section("Choosing"), "", "## Modes", "",
              g.section("Modes"), "", "## Changing the system", "",
              g.section("Changing the system"), "", "## Decisions", "",
              "Check these before changing what they decide; each is a deliberate choice.", ""]
    mine = [r for r in records if f.name in r.areas]
    lines += [f"- [{r.title}](../decisions/{r.id}.md)" for r in mine] or ["- None yet."]
    lines += ["", "## Contracts", ""]
    prefix = f.name + "."
    bound = [(c, [r for r in c.roles() if r.startswith(prefix)]) for c in contracts]
    bound = [(c, roles) for c, roles in bound if roles]
    lines += [f"- [{c.name}](../contracts/{c.name}.yaml) ({c.status}): binds "
              + ", ".join(f"`{r}`" for r in roles) + "." for c, roles in bound] \
        or ["- No contract binds these roles yet."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- reference

def _reference(f: Foundation, g: Guidance, ts: TokenSet, entries: Sequence[RoleEntry],
               contracts: Sequence[Contract]) -> str:
    modes = _foundation_contexts(f, ts)
    labels = [_context_label(m, ts) for m in modes]
    lines = [f"# {g.title} reference", "",
             f"Every {g.title.lower()} token in this system as built. Values are resolved for "
             "each mode; the role column says what each is for, and architecture.md says when "
             "to use it.", "", "## Semantic roles", "",
             "| Role | Type | Points at | " + " | ".join(labels) + " |",
             "|---|---|---|" + "---|" * len(labels)]
    for e in entries:
        raw = ts.raw(e.path, "")
        points = f"`{alias_target(raw)}`" if is_alias(raw) else "one primitive per field"
        values = [_cell(_fmt(ts.get(e.path).type, ts.resolve(e.path, m))) for m in modes]
        lines.append(f"| `{e.path}` | {e.type} | {points} | " + " | ".join(values) + " |")
    lines += ["", "What each role is for:", ""]
    lines += [f"- `{e.path}`: {e.description}" for e in entries]
    lines += ["", "## Primitives", "", "| Primitive | Value |", "|---|---|"]
    lines += [f"| `{t.path}` | {_cell(_fmt(t.type, t.value))} |"
              for t in _tokens_of(ts, f, "primitive")]
    if f.name == "color":
        lines += ["", "## Pairings", "",
                  "The gate measures every pairing below in every scheme and contrast context "
                  "and refuses the system if one falls short. Under high contrast a minimum of "
                  f"4.5:1 or more rises to {HIGH_TEXT:g}:1 (WCAG 1.4.6) and a lower one to "
                  f"{HIGH_NON_TEXT:g}:1, our floor, unless the pairing pins its own (marked "
                  "pinned).", "",
                  "| Foreground | Background | Minimum | High contrast | Source |",
                  "|---|---|---|---|---|"]
        for p in f.pairings:
            lines.append(f"| `{p.fg}` | `{p.bg}` | {p.minimum:g}:1 | {_high_cell(p, ts)} | "
                         f"{_criterion_words(p.criterion)} |")
        lines += ["", "Contracts add these pairings for the components they describe. The rule "
                      "pack measured each in every scheme and contrast context against these "
                      "tokens before it was written. Their minimums rise under high contrast the "
                      "same way, unless the contract pins its own (marked pinned).", "",
                  "| Contract | Foreground | Background | Minimum | High contrast | Source |",
                  "|---|---|---|---|---|---|"]
        for name, p in contract_pairing_rows(contracts):
            lines.append(f"| {name} | `{p.fg}` | `{p.bg}` | {p.minimum:g}:1 | "
                         f"{_high_cell(p, ts)} | {_pairing_source(p)} |")
    return "\n".join(lines) + "\n"


# -------------------------------------------------------------------- audit

def _audit(f: Foundation, g: Guidance, ts: TokenSet) -> str:
    title = g.title
    checks = dict(g.checks)
    lines = [f"# {title} audit", "",
             f"Use this file to check a {title.lower()} system, or screens built on it, against "
             "its rules. It classifies and cites; it does not redesign.", "",
             "## Before you audit", "",
             "- Work from the built files, tokens.json or tokens.css, and the contracts. If they "
             "are not available, ask for them; never estimate a value.",
             "- Resolve every role in every mode first. A role that does not resolve is a "
             "blocking finding that names the role; go on with every role that does.",
             "- Note which modes the product ships. Audit every mode it ships, and say in the "
             "report which modes were audited.",
             "- When asked to skip part of the audit, run it anyway and mark what the person "
             "asked to skip.", "",
             "## Scope", "", g.section("Audit scope"), "", "## What the gate checks", "",
             "The build runs these checks on every system and refuses to write one that fails, "
             "so a system straight from the build passes them. Run them again after any hand "
             "edit.", "", "| Check | Source | What it guards |", "|---|---|---|"]
    for c in f.checks:
        lines.append(f"| `{c.id}` | {_criterion_words(c.criterion)} | "
                     f"{_cell(checks[c.id].rstrip('.'))} |")
    lines.append("| `role-types` | our rule | every role has the type its checks read |")
    if any(c.criterion in AAA for c in f.checks):
        lines += ["", "A check that cites an AAA criterion blocks like the others: the system "
                      "applies it where it chose to (decisions/aaa-criteria-that-block.md)."]
    if f.pairings:
        n = len(_foundation_contexts(f, ts))
        lines += ["", f"The gate also measures {len(f.pairings)} contrast pairings in {n} "
                      "contexts each; reference.md lists them under Pairings."]
    lines += ["", "## Beyond the gate", "",
              "These need the screens or the product, not only the tokens:", "",
              g.section("Beyond the gate"), "", "## Classify and cite", "",
              "1. Name the element and the contract it matches (../contracts/). No matching "
              "contract is itself a finding: a missing contract.",
              "2. Match its variant and state against that contract.",
              "3. Cite the rule it breaks: a contract field, a role in reference.md, a check "
              "above, a decision record, or a line in ../content.md or ../direction.md. No "
              "citation, no finding.",
              "4. End with a system trace: the role, contract or rule that was missing or "
              "broken. \"No role exists for this\" is a valid trace; it is how the system "
              "grows.", "",
              "## Severity", "",
              "Severity is frequency times impact times persistence: how often people meet it, "
              "how much it stops them, and whether it stays until someone fixes it.", "",
              "| Level | When |", "|---|---|",
              "| blocking | fails WCAG at level A or AA; or fails a check the gate runs or a "
              "contract pairing, AAA criteria and our floors included |",
              "| serious | frequent, or stops some people with a workaround; or misses an AAA "
              "criterion the system does not apply |",
              "| minor | rare and does not stop the task; or passes within 10 percent of a "
              "minimum |", "",
              "Every finding has a level. A value that cannot be measured is reported as "
              "unmeasured, never as a pass.", "",
              "## Report", "",
              "```",
              f"{title} audit: <what was audited>; modes <the modes audited>",
              "[<level>] <role or element>: <what is wrong> (cites <rule>). Fix: <the change>. "
              "Trace: <role, contract or rule>.",
              "Summary: <n> blocking, <n> serious, <n> minor; skipped: <what and why>",
              "```", "",
              "After a fix, run the same check on the same element. It passes under the same "
              "rule, or the finding stays open."]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ handoff

def _handoff(f: Foundation, g: Guidance, ts: TokenSet, entries: Sequence[RoleEntry]) -> str:
    title = g.title
    axes = [a for a in FOUNDATION_AXES.get(f.name, ()) if a in ts.axes]
    lines = [f"# {title} handoff", "",
             f"Use this file to hand the {title.lower()} tokens to developers. It documents "
             "what is built; it does not audit or redesign.", "", "## Inputs", "",
             "- tokens.css and tokens.json from the build are the source. Never retype a "
             "value; link or import the files.",
             "- CSS custom properties are the default output and tokens.css already holds "
             "them; produce another format only when someone asks for it.",
             "- If a file is missing, ask for it; never estimate a value.", "",
             "## CSS custom properties", "",
             "| Role | Custom property | Varies on |", "|---|---|---|"]
    for e in entries:
        props = ", ".join(f"`{p}`" for p in css_names(e.path, ts.get(e.path).type))
        lines.append(f"| `{e.path}` | {props} | {', '.join(_varies(ts, e.path)) or 'nothing'} |")
    lines += [""]
    if axes:
        lines += ["Modes switch on the html element, never on a part of the page:", ""]
        lines += [f"- {_axis_words(a, ts)}" for a in axes]
    else:
        lines += ["These values are the same in every mode."]
    lines += ["", "## Using the roles", ""]
    lines += [f"- `{e.path}`: {e.description}" for e in entries]
    lines += ["", "## Implementation notes", "", g.section("Handoff notes"), "",
              "## Common mistakes", "", g.section("Common mistakes"), "",
              "## What a handoff does not do", "",
              "- It does not change a value, suggest a redesign or add a role; those go to the "
              "system owner and a new build.",
              "- It does not write a primitive into a component; components use the role "
              "properties above.",
              "- It does not produce formats nobody asked for."]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------- readme

def _readme(foundations: Sequence[Tuple[Foundation, Guidance]],
            contracts: Sequence[Contract]) -> str:
    lines = ["# Rule pack", "",
             "The rules of this design system for agents and people, generated from the built "
             "tokens, the component contracts and the decision records. The files state what "
             "is true now; the reasons are in decisions/. Paths cited in the files, such as "
             "decisions/two-layers.md, are relative to this folder.", "",
             "## Load one path per task", "",
             "Load the files for your task, then stop: loading everything crowds out the "
             "work.", "", "| Task | Load |", "|---|---|",
             "| Build or change a screen | contracts/ for each component, then "
             "<foundation>/architecture.md for each foundation it touches |",
             "| Pick a token | <foundation>/reference.md |",
             "| Review or audit | <foundation>/audit.md for each foundation in scope, plus "
             "content.md and direction.md |",
             "| Hand tokens to developers | <foundation>/handoff.md |",
             "| Write copy | content.md |",
             "| Build right to left | direction.md |",
             "| Question a rule | decisions/HISTORY.md, then the one record it points to |", "",
             "## Foundations", ""]
    for f, g in foundations:
        links = ", ".join(f"[{name[:-3]}]({f.name}/{name})" for name in FILES)
        lines.append(f"- {g.title}: {links}")
    lines += ["", "## Contracts", ""]
    lines += [f"- [{c.name}](contracts/{c.name}.yaml) ({c.status}): {c.description}"
              for c in contracts]
    met = [c for c in contracts if any(overlaps(c))]
    if met:
        lines += ["", "In these contracts two bindings of one part and property, naming "
                      "different roles, can both match. Each says in usage.do which one wins, "
                      "in the lines below; the states that can meet that way are listed with "
                      "it.", ""]
        for c in met:
            pairs = "; ".join(f"{a} and {b}" for a, b in state_pairs(c))
            lines.append(f"- {c.name}" + (f" (states that meet: {pairs})" if pairs else "")
                         + ":")
            lines += [f"  - {r}" for r in precedence_lines(c)]
    lines += ["", "## Rules for every task", "",
              "- The token files are the source. Never edit a generated value; change the "
              "inputs and build again.",
              "- Components bind semantic roles only, never a primitive or a literal.",
              "- Every finding cites a rule. No citation, no finding.",
              "- Agents write contracts at experimental. Only the owner promotes one to ready, "
              "when its provenance meets the thresholds in the contract schema.",
              "- Check the decision records before changing what they decide."]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------- pack

def build_rule_pack(ts: TokenSet, *, contracts_dir: Union[str, Path] = SEED_DIR,
                    records_dir: Union[str, Path] = RECORDS_DIR,
                    guidance_dir: Union[str, Path] = GUIDANCE_DIR) -> Dict[str, str]:
    """Every rule pack file for a built token set: path under PACK to text,
    in a fixed order. Raises RulePackError naming every problem when the
    guidance, a contract or a record does not fit the build."""
    problems = list(guidance_problems(ts, guidance_dir))
    try:
        contracts = load_folder(contracts_dir)
    except ContractError as exc:
        problems += [p.message for p in exc.problems]
        contracts = ()
    problems += [p.message for p in validate_contracts(contracts, ts)]
    problems += _precedence_problems(contracts)
    try:
        records = load_records(records_dir)
    except RecordError as exc:
        problems += [p.message for p in exc.problems]
        records = ()
    if problems:
        raise RulePackError(problems)
    by_foundation = catalog_by_foundation(role_catalog(ts, guidance_dir))
    guides = [(f, load_guidance(f.name, guidance_dir)) for f in FOUNDATIONS
              if f.name in by_foundation]
    files: Dict[str, str] = {f"{PACK}/README.md": _readme(guides, contracts)}
    for f, g in guides:
        entries = by_foundation[f.name]
        files[f"{PACK}/{f.name}/architecture.md"] = _architecture(f, g, ts, entries, records,
                                                                  contracts)
        files[f"{PACK}/{f.name}/reference.md"] = _reference(f, g, ts, entries, contracts)
        files[f"{PACK}/{f.name}/audit.md"] = _audit(f, g, ts)
        files[f"{PACK}/{f.name}/handoff.md"] = _handoff(f, g, ts, entries)
    for name in SHARED:
        files[f"{PACK}/{name}.md"] = (Path(guidance_dir) / f"{name}.md").read_text(
            encoding="utf-8")
    for path in sorted(Path(contracts_dir).glob("*.yaml")):
        files[f"{PACK}/contracts/{path.name}"] = path.read_text(encoding="utf-8")
    for name, text in record_sources(records_dir).items():
        files[f"{PACK}/decisions/{name}"] = text
    return files
