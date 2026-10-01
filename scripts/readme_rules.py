"""Write the README's rule catalogue from data/anti-patterns.json.

The catalogue sits between two markers in README.md. Each category gets a
table, largest category first; inside a table the rules run from critical to
low, then by id. Re-run after adding or changing a rule:

    python scripts/readme_rules.py

tests/test_readme_rules.py fails when the README and the rules disagree.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
RULES = ROOT / "data" / "anti-patterns.json"
START = "<!-- rules:start -->\n"
END = "<!-- rules:end -->"
SEVERITY = ("critical", "high", "medium", "low")


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def check(rules: Sequence[Mapping[str, str]]) -> None:
    """Raise ValueError naming the rule, the field and the fix for a rule the
    catalogue cannot place: no id, no name, no category, or a severity
    outside SEVERITY."""
    for i, r in enumerate(rules):
        rid = r.get("id") or f"entry {i}"
        for field in ("id", "name", "category"):
            if not isinstance(r.get(field), str) or not r.get(field):
                raise ValueError(f"data/anti-patterns.json: rule {rid} has no {field}; give it "
                                 f"a {field} as text")
        if r.get("severity") not in SEVERITY:
            raise ValueError(f"data/anti-patterns.json: rule {rid} has severity "
                             f"{r.get('severity')!r}; use one of {', '.join(SEVERITY)}")


def coverage(rules: Sequence[Mapping[str, str]]) -> str:
    """Each category with its rule count, largest first, as the README
    states it in prose."""
    check(rules)
    counts: Dict[str, int] = defaultdict(int)
    for r in rules:
        counts[r["category"]] += 1
    return ", ".join(f"{c} ({n})" for c, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def render(rules: Sequence[Mapping[str, str]]) -> str:
    """The markdown between the markers."""
    check(rules)
    groups: Dict[str, List[Mapping[str, str]]] = defaultdict(list)
    for r in rules:
        groups[r["category"]].append(r)
    out: List[str] = []
    for cat in sorted(groups, key=lambda c: (-len(groups[c]), c)):
        members = sorted(groups[cat], key=lambda r: (SEVERITY.index(r["severity"]), r["id"]))
        word = "rule" if len(members) == 1 else "rules"
        out += ["", f"#### {cat} ({len(members)} {word})", "",
                "| Severity | Rule ID | Name |", "|---|---|---|"]
        out += [f"| {r['severity']} | `{r['id']}` | {_cell(r['name'])} |" for r in members]
    return "\n".join(out[1:]) + "\n\n"


def main() -> None:
    rules = json.loads(RULES.read_text(encoding="utf-8"))["entries"]
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"README.md: the markers {START.strip()} and {END} are missing; "
                         "put them around the rule tables")
    head, rest = text.split(START, 1)
    tail = rest.split(END, 1)[1]
    README.write_text(head + START + render(rules) + END + tail, encoding="utf-8")


if __name__ == "__main__":
    main()
