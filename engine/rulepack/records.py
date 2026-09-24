"""Decision records: one file per deliberate choice a designer could take
for an oversight, so it is checked before it is changed.

A record is markdown with a front matter block and five fixed sections:

    ---
    id: ring-offset
    title: The focus ring clears the surfaces, not the fill
    status: active
    areas: [color, border]
    supersedes: null
    superseded_by: null
    ---

    # The focus ring clears the surfaces, not the fill

    ## Context
    ## Decision
    ## Why
    ## What it touches
    ## Consequences

HISTORY.md routes to every record in one hop. Records state each decision
as it stands; the words in CORRECTION_WORDS tell a history of changes, which
an agent reading the record as context would take for the current rule, so
a record holding them is refused.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from engine.contracts.yamlite import YamlError, loads

RECORDS_DIR = Path(__file__).resolve().parent / "decisions"
HISTORY = "HISTORY.md"
HEADINGS: Tuple[str, ...] = ("Context", "Decision", "Why", "What it touches", "Consequences")
STATUSES: Tuple[str, ...] = ("active", "superseded")
AREAS: Tuple[str, ...] = ("color", "space", "radius", "border", "elevation", "motion", "layout",
                          "type", "contracts", "content", "direction", "output")
FRONT_KEYS: Tuple[str, ...] = ("id", "title", "status", "areas", "supersedes", "superseded_by")
# Words that tell how a rule changed instead of what it is.
CORRECTION_WORDS: Tuple[str, ...] = (
    "we used to", "it used to", "used to be", "no longer", "previously", "originally",
    "anymore", "any more", "was changed",
    "we changed", "we removed", "we fixed", "was fixed", "the old", "now uses", "earlier version",
    "at first", "turned out",
)

_ID = re.compile(r"[a-z][a-z0-9]*(-[a-z0-9]+)*")
_LINK = re.compile(r"\]\(([^)]+)\)")


@dataclass(frozen=True)
class RecordProblem:
    record: str
    rule: str
    message: str


class RecordError(ValueError):
    """Records that cannot be read; `problems` holds every reason."""

    def __init__(self, problems: Sequence[RecordProblem]):
        self.problems: Tuple[RecordProblem, ...] = tuple(problems)
        super().__init__("\n".join(p.message for p in self.problems))


@dataclass(frozen=True)
class Record:
    id: str
    title: str
    status: str
    areas: Tuple[str, ...]
    supersedes: Optional[str]
    superseded_by: Optional[str]
    sections: Tuple[Tuple[str, str], ...]
    text: str

    def section(self, heading: str) -> str:
        return dict(self.sections)[heading]


def _front(text: str) -> Tuple[Optional[str], str]:
    """(front matter text, body) when the file opens with a --- block."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, text


def _sections(body: str) -> Tuple[List[str], List[Tuple[str, str]]]:
    """(H1 titles, [(H2 heading, its text)]) in order."""
    titles: List[str] = []
    sections: List[Tuple[str, str]] = []
    current: Optional[str] = None
    buf: List[str] = []
    for line in body.split("\n"):
        if line.startswith("# "):
            titles.append(line[2:].strip())
            continue
        if line.startswith("## "):
            if current is not None:
                sections.append((current, "\n".join(buf).strip()))
            current, buf = line[3:].strip(), []
            continue
        if current is not None:
            buf.append(line)
    if current is not None:
        sections.append((current, "\n".join(buf).strip()))
    return titles, sections


def read_record(text: str, source: str) -> Tuple[Optional[Record], List[RecordProblem]]:
    """Read one record. Returns the record (None when it cannot be built)
    and every problem, each naming the record and the fix."""
    stem = Path(source).stem
    problems: List[RecordProblem] = []

    def add(rule: str, message: str) -> None:
        problems.append(RecordProblem(stem, rule, f"{source}: {message}"))

    front_text, body = _front(text)
    if front_text is None:
        add("front-matter", "the file does not open with a front matter block between two "
                            "'---' lines; start it with id, title, status, areas, supersedes "
                            "and superseded_by")
        return None, problems
    try:
        front: Any = loads(front_text, source)
    except YamlError as exc:
        add("front-matter", f"the front matter does not read ({exc})")
        return None, problems
    if not isinstance(front, dict) or set(front) != set(FRONT_KEYS):
        keys = sorted(front) if isinstance(front, dict) else front
        add("front-matter", f"the front matter has {keys}; give it exactly "
                            f"{', '.join(FRONT_KEYS)}")
        return None, problems
    rid, title, status, areas = front["id"], front["title"], front["status"], front["areas"]
    if rid != stem or not (isinstance(rid, str) and _ID.fullmatch(rid)):
        add("id", f"id is {rid!r}; use the file name without .md, a lowercase name with '-'")
    if not (isinstance(title, str) and title.strip()):
        add("title", "title is empty; state the decision in one line")
        title = ""
    if status not in STATUSES:
        add("status", f"status is {status!r}; use active or superseded")
    if not (isinstance(areas, list) and areas and all(a in AREAS for a in areas)):
        add("areas", f"areas is {areas!r}; list one or more of {list(AREAS)}")
        areas = []
    for key in ("supersedes", "superseded_by"):
        value = front[key]
        if value is not None and not (isinstance(value, str) and _ID.fullmatch(value)):
            add(key, f"{key} is {value!r}; name a record id or write null")
    if status == "superseded" and front["superseded_by"] is None:
        add("superseded_by", "a superseded record names the record that replaces it in "
                             "superseded_by")
    if status == "active" and front["superseded_by"] is not None:
        add("superseded_by", "an active record has no superseded_by; set status to superseded "
                             "or clear it")
    titles, sections = _sections(body)
    if titles != [title]:
        add("title", f"the body's heading is {titles}; open the body with one '# {title}' line")
    headings = [h for h, _ in sections]
    if headings != list(HEADINGS):
        add("headings", f"the sections are {headings}; use exactly {', '.join(HEADINGS)}, in "
                        "that order")
    for heading, content in sections:
        if heading in HEADINGS and not content:
            add("empty-section", f"the {heading} section is empty; write it")
    lowered = body.lower()
    for word in CORRECTION_WORDS:
        if re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", lowered):
            add("history", f"'{word}' tells how the rule changed; state the decision as it "
                           "stands, and let HISTORY.md route to what came before")
    if "\u2014" in text or "\u2013" in text or re.search(r"\s--\s", body):
        add("dash", "the record holds an em dash, an en dash or '--'; use a period, a comma or a "
                    "colon")
    if problems:
        return None, problems
    return Record(rid, title.strip(), status, tuple(areas), front["supersedes"],
                  front["superseded_by"], tuple(sections), text), problems


def history_problems(records: Sequence[Record], history: str) -> List[RecordProblem]:
    """HISTORY.md links every record exactly once and nothing else."""
    out: List[RecordProblem] = []
    links = _LINK.findall(history)
    ids = {r.id for r in records}
    for link in sorted(set(links)):
        if not link.endswith(".md") or link[:-3] not in ids:
            out.append(RecordProblem(HISTORY, "history-link",
                                     f"{HISTORY}: links {link}, which is not a record; link "
                                     "each record as (id.md)"))
        elif links.count(link) > 1:
            out.append(RecordProblem(HISTORY, "history-link",
                                     f"{HISTORY}: links {link} {links.count(link)} times; "
                                     "route to each record once"))
    for r in records:
        if f"{r.id}.md" not in links:
            out.append(RecordProblem(r.id, "history-missing",
                                     f"{HISTORY}: {r.id} is not listed; add a line "
                                     f"- [{r.title}]({r.id}.md) under its chapter"))
    if "\u2014" in history or "\u2013" in history or re.search(r"\s--\s", history):
        out.append(RecordProblem(HISTORY, "dash", f"{HISTORY}: holds an em dash, an en dash or "
                                                  "'--'; use a period, a comma or a colon"))
    return out


def _chain_problems(records: Sequence[Record]) -> List[RecordProblem]:
    by_id = {r.id: r for r in records}
    out: List[RecordProblem] = []
    for r in records:
        if r.superseded_by is not None:
            nxt = by_id.get(r.superseded_by)
            if nxt is None or nxt.supersedes != r.id:
                out.append(RecordProblem(r.id, "supersede-chain",
                                         f"{r.id}.md: superseded_by names {r.superseded_by}, "
                                         f"which must exist and name {r.id} in supersedes"))
        if r.supersedes is not None:
            old = by_id.get(r.supersedes)
            if old is None or old.superseded_by != r.id or old.status != "superseded":
                out.append(RecordProblem(r.id, "supersede-chain",
                                         f"{r.id}.md: supersedes names {r.supersedes}, which "
                                         f"must exist, be superseded and name {r.id} in "
                                         "superseded_by"))
    return out


def check_folder(folder: Union[str, Path] = RECORDS_DIR) -> Tuple[Tuple[Record, ...],
                                                                   List[RecordProblem]]:
    """Every record in `folder` and every problem across them and HISTORY.md."""
    root = Path(folder)
    records: List[Record] = []
    problems: List[RecordProblem] = []
    for f in sorted(root.glob("*.md")):
        if f.name == HISTORY:
            continue
        record, found = read_record(f.read_text(encoding="utf-8"), f.name)
        problems += found
        if record is not None:
            records.append(record)
    if not records and not problems:
        problems.append(RecordProblem(root.name, "no-records",
                                      f"{root} holds no decision record; pass the decisions "
                                      "folder"))
    problems += _chain_problems(records)
    history = root / HISTORY
    if history.exists():
        problems += history_problems(records, history.read_text(encoding="utf-8"))
    else:
        problems.append(RecordProblem(HISTORY, "history-missing",
                                      f"{root} has no {HISTORY}; add one that links every "
                                      "record"))
    return tuple(records), problems


def load_records(folder: Union[str, Path] = RECORDS_DIR) -> Tuple[Record, ...]:
    """Every record, sorted by id. Raises RecordError with every problem."""
    records, problems = check_folder(folder)
    if problems:
        raise RecordError(problems)
    return records


def record_sources(folder: Union[str, Path] = RECORDS_DIR) -> Dict[str, str]:
    """Each record file's name and text, HISTORY.md included, sorted by name."""
    return {f.name: f.read_text(encoding="utf-8") for f in sorted(Path(folder).glob("*.md"))}
