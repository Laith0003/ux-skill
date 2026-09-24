"""Per-foundation guidance, written once in our words, and the role
catalog built from it.

Each foundation has guidance/<foundation>.md with the H2 sections in
SECTIONS, in order. Two of them are read line by line:

- Roles: one bullet per semantic role, "- `role.path`: what it is for".
  A path may hold `<name>` for one segment, so one line can describe a
  family such as `color.status.<status>.text`.
- Checks: one bullet per check the foundation's gate runs,
  "- `check-id`: what it guards".

role_catalog joins those descriptions with each role's type (from the
foundation's role_types or the token) and the axes it varies on, for every
semantic role in a built token set. guidance_problems says what is
missing or stale against the build: a role with no description, a
description that matches no role, a check with no line.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple, Union

from engine.foundations.build import FOUNDATIONS
from engine.foundations.modes import FOUNDATION_AXES
from engine.foundations.tokens import TokenSet

GUIDANCE_DIR = Path(__file__).resolve().parent / "guidance"
SECTIONS: Tuple[str, ...] = ("Summary", "Principles", "Roles", "Choosing", "Modes",
                             "Changing the system", "Audit scope", "Checks", "Beyond the gate",
                             "Handoff notes", "Common mistakes")
# Guidance that belongs to no one foundation; each file has its own sections.
SHARED: Mapping[str, Tuple[str, ...]] = {
    "content": ("Summary", "Error messages", "Empty states", "Buttons and actions",
                "Destructive confirmations", "Labels and helper text", "Numbers, dates and "
                "currency", "Audit checks"),
    "direction": ("Summary", "Direction is a mode", "Mirroring", "Arabic type", "Length and "
                  "layout", "Numbers and fixed runs", "Audit checks"),
}
_BULLET = re.compile(r"^- `([^`]+)`: (.+)$")


@dataclass(frozen=True)
class Guidance:
    name: str
    title: str
    sections: Tuple[Tuple[str, str], ...]
    roles: Tuple[Tuple[str, str], ...]
    checks: Tuple[Tuple[str, str], ...]

    def section(self, heading: str) -> str:
        return dict(self.sections)[heading]


@dataclass(frozen=True)
class RoleEntry:
    path: str
    foundation: str
    type: str
    axes: Tuple[str, ...]
    description: str


class GuidanceError(ValueError):
    """Guidance that cannot be read; the message names the file and the fix."""


def _split(text: str, source: str) -> Tuple[str, List[Tuple[str, str]]]:
    title = ""
    sections: List[Tuple[str, str]] = []
    current: Optional[str] = None
    buf: List[str] = []
    for line in text.split("\n"):
        if line.startswith("# ") and not title and current is None:
            title = line[2:].strip()
        elif line.startswith("## "):
            if current is not None:
                sections.append((current, "\n".join(buf).strip()))
            current, buf = line[3:].strip(), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections.append((current, "\n".join(buf).strip()))
    if not title:
        raise GuidanceError(f"{source} has no '# ' title line; open it with the foundation's "
                            "name")
    return title, sections


def _bullets(body: str, source: str, heading: str) -> Tuple[Tuple[str, str], ...]:
    out: List[Tuple[str, str]] = []
    for line in body.split("\n"):
        if not line.strip():
            continue
        m = _BULLET.match(line)
        if not m:
            raise GuidanceError(f"{source}: the {heading} section line {line!r} is not "
                                "\"- `name`: description\"; write one bullet per entry")
        if any(k == m.group(1) for k, _ in out):
            raise GuidanceError(f"{source}: {m.group(1)} is described twice under {heading}; "
                                "keep one line")
        out.append((m.group(1), m.group(2).strip()))
    return tuple(out)


def read_guidance(text: str, source: str, sections: Sequence[str] = SECTIONS) -> Guidance:
    """Read one guidance file. Raises GuidanceError naming the file and the fix."""
    title, found = _split(text, source)
    headings = [h for h, _ in found]
    if headings != list(sections):
        raise GuidanceError(f"{source} has the sections {headings}; use exactly "
                            f"{', '.join(sections)}, in that order")
    empty = [h for h, body in found if not body]
    if empty:
        raise GuidanceError(f"{source}: the {', '.join(empty)} section is empty; write it")
    body = dict(found)
    roles = _bullets(body["Roles"], source, "Roles") if "Roles" in body else ()
    checks = _bullets(body["Checks"], source, "Checks") if "Checks" in body else ()
    return Guidance(Path(source).stem, title, tuple(found), roles, checks)


def load_guidance(name: str, folder: Union[str, Path] = GUIDANCE_DIR) -> Guidance:
    """The guidance for a foundation, or for a shared topic in SHARED."""
    path = Path(folder) / f"{name}.md"
    if not path.exists():
        raise GuidanceError(f"{path} does not exist; write guidance for {name} with the "
                            f"sections {', '.join(SHARED.get(name, SECTIONS))}")
    return read_guidance(path.read_text(encoding="utf-8"), path.name,
                         SHARED.get(name, SECTIONS))


def _pattern(key: str) -> "re.Pattern[str]":
    return re.compile("^" + re.sub(r"<[a-z-]+>", "[a-z0-9-]+",
                                   re.escape(key).replace(r"\<", "<").replace(r"\>", ">")) + "$")


def describe(path: str, guidance: Guidance) -> Optional[str]:
    """The description whose key matches `path`: an exact key first, else
    the one pattern that matches."""
    exact = dict(guidance.roles).get(path)
    if exact is not None:
        return exact
    matches = [d for k, d in guidance.roles if "<" in k and _pattern(k).match(path)]
    return matches[0] if len(matches) == 1 else None


def _semantic(ts: TokenSet, foundation: str) -> List[str]:
    return [t.path for t in ts.tokens()
            if t.layer == "semantic" and t.path.split(".", 1)[0] == foundation]


def role_catalog(ts: TokenSet, folder: Union[str, Path] = GUIDANCE_DIR) -> Tuple[RoleEntry, ...]:
    """Every semantic role in `ts`, in build order, with its foundation,
    type, the axes it may vary on and its description."""
    out: List[RoleEntry] = []
    for f in FOUNDATIONS:
        roles = _semantic(ts, f.name)
        if not roles:
            continue
        g = load_guidance(f.name, folder)
        for path in roles:
            out.append(RoleEntry(path, f.name, f.role_types.get(path, ts.get(path).type),
                                 tuple(FOUNDATION_AXES.get(f.name, ())),
                                 describe(path, g) or ""))
    return tuple(out)


def guidance_problems(ts: TokenSet, folder: Union[str, Path] = GUIDANCE_DIR) -> List[str]:
    """What the guidance misses or keeps that the build does not have: a
    role with no description, a role key or check line that matches
    nothing, a check with no line. Each message names the file and the fix."""
    out: List[str] = []
    for f in FOUNDATIONS:
        roles = _semantic(ts, f.name)
        if not roles:
            continue
        g = load_guidance(f.name, folder)
        source = f"{f.name}.md"
        for path in roles:
            if describe(path, g) is None:
                out.append(f"{source}: {path} has no description under Roles; add "
                           f"\"- `{path}`: what it is for\"")
        for key, _ in g.roles:
            if not any((key == p) or ("<" in key and _pattern(key).match(p)) for p in roles):
                out.append(f"{source}: the Roles line for {key} matches no role in the "
                           "build; remove it or fix the path")
        ids = [c.id for c in f.checks]
        described = dict(g.checks)
        for cid in ids:
            if cid not in described:
                out.append(f"{source}: the check {cid} has no line under Checks; add "
                           f"\"- `{cid}`: what it guards\"")
        for cid in described:
            if cid not in ids:
                out.append(f"{source}: the Checks line for {cid} names no check of {f.name}; "
                           "remove it or fix the id")
    for name in SHARED:
        try:
            load_guidance(name, folder)
        except GuidanceError as exc:
            out.append(str(exc))
    return out


def catalog_by_foundation(catalog: Sequence[RoleEntry]) -> Dict[str, List[RoleEntry]]:
    out: Dict[str, List[RoleEntry]] = {}
    for entry in catalog:
        out.setdefault(entry.foundation, []).append(entry)
    return out
