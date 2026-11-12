"""Two labelling passes and a tiebreak for every finding on the corpus.

Every label here is model-made. A person confirms a 50-finding sample
(bench/sample.py) before any number built on them is trusted.

The two passes see different evidence, so their agreement measures how
clear-cut a rule's condition is, not only how consistent one reader is:

- Pass A, the excerpt view: the rule's text and the finding's excerpt
  alone, as a rater sees a finding in a queue.
- Pass B, the context view: the lines around the finding in its file (seven
  lines each side), where what makes a hit fine or not usually sits: a
  focus-visible rule two lines down, a rel attribute on the next line, a
  reduced-motion block.

Both passes are written as per-rule criteria in labels/guide.json, set by
reading the distinct findings of each rule on the dev split. A criterion is
a default label and ordered exceptions, each a regular expression with the
reason it flips the label. Writing them as data keeps every label
reproducible and every judgment open to review.

Where the passes disagree, labels/tiebreak.json holds the third reading,
made by looking at the finding in its page. It is looked up by finding key,
then by ``rule|pattern`` for a group of identical hits, then by
``rule|A>B`` for one kind of disagreement on a rule (pass A said A, pass B
said B), then by ``rule|*``. An entry gives a label, or ``follow: a`` or
``follow: b`` when reading the pages showed one pass right for that kind of
disagreement. A disagreement with no tiebreak is reported as unresolved and
its final label is cantTell. When both passes say cantTell, a tiebreak
entry, if there is one, is the third reading that decides it.

Labels: TP (the condition the rule names is present), FP (it is not),
cantTell (the frozen page cannot show it, or the rule's text does not decide
it). This is detection precision; usefulness ("would a designer change it")
is not labelled yet.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from bench import BENCH, LABELS, PAGES, PRIVATE, SEEDED

GUIDE = BENCH / "labels" / "guide.json"
TIEBREAK = BENCH / "labels" / "tiebreak.json"
VALUES = ("TP", "FP", "cantTell")
CONTEXT = 7


class LabelError(ValueError):
    """The guide or tiebreak file is malformed; the message names the rule and the fix."""


def _load(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _check_label(value: str, where: str) -> str:
    if value not in VALUES:
        raise LabelError(f"{where}: label {value!r} is not one of {VALUES}; fix it in the file")
    return value


def _luminance(hexcolor: str) -> float:
    rgb = [int(hexcolor[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def faded_text(text: str) -> bool:
    """True when a contrast message reports a ratio well under what its two
    colours give: the text was measured through an opacity, such as a
    preload state a blocked script would lift."""
    m = re.search(r"#([0-9a-f]{6}) on #([0-9a-f]{6}) measures ([\d.]+):1", text, re.I)
    if not m:
        return False
    a, b = _luminance(m.group(1)), _luminance(m.group(2))
    ratio = (max(a, b) + 0.05) / (min(a, b) + 0.05)
    return float(m.group(3)) < ratio * 0.85


# Checks a regular expression cannot make, named in guide.json as "computed:<name>".
COMPUTED = {"faded-text": faded_text}


def _apply(crit: Optional[Dict[str, Any]], text: str, where: str) -> Tuple[Optional[str], str]:
    """The label a criterion gives ``text``, and the reason. (None, '') when
    the rule has no criterion for this pass."""
    if not crit:
        return None, ""
    for i, ex in enumerate(crit.get("unless", [])):
        if ex["match"].startswith("computed:"):
            fn = COMPUTED.get(ex["match"][len("computed:") :])
            if fn is None:
                raise LabelError(
                    f"{where} exception {i}: unknown check {ex['match']!r}; use one of "
                    f"{', '.join('computed:' + k for k in COMPUTED)}"
                )
            if fn(text):
                return _check_label(ex["label"], where), ex.get("why", "")
            continue
        try:
            hit = re.search(ex["match"], text, re.I | re.S)
        except re.error as exc:
            raise LabelError(f"{where} exception {i}: bad pattern {ex['match']!r}: {exc}") from exc
        if hit:
            return _check_label(ex["label"], where), ex.get("why", "")
    return _check_label(crit["default"], where), crit.get("why", "")


HERE = "<<<HERE>>>"
_TEXTS: Dict[Path, Tuple[str, List[int]]] = {}


SCRIPTS_REMOVED = "<!-- ux-bench: script elements removed from this page -->"


def context(finding: Dict[str, Any], base: Path, before: int = 300, after: int = 500,
            scripts_removed: bool = False) -> str:
    """The source around the finding with HERE marking where the rule
    matched: ``before`` characters before the match and ``after`` from it,
    across lines. Pass B criteria read the selector or tag at HERE and the
    rest of its block. The excerpt itself when the finding has no line
    (render findings the engine could not place in the source)."""
    path = base / finding["file"]
    if finding.get("pass") == "render":
        # The measured message, then the head of the page: whether it loads
        # web fonts or sets photos as backgrounds decides some readings.
        head = path.read_text(encoding="utf-8", errors="replace")[:6000] if path.exists() else ""
        # The stored page has no scripts; the manifest says whether the
        # original had some, which can change what the render measured.
        flag = SCRIPTS_REMOVED + "\n" if scripts_removed else ""
        return finding["excerpt"] + "\n" + HERE + flag + head
    if finding.get("line", 0) <= 0 or not path.exists():
        return finding["excerpt"]
    if path not in _TEXTS:
        text = path.read_text(encoding="utf-8", errors="replace")
        starts = [0]
        for i, ch in enumerate(text):
            if ch == "\n":
                starts.append(i + 1)
        _TEXTS[path] = (text, starts)
    text, starts = _TEXTS[path]
    line = finding["line"] - 1
    if line >= len(starts):
        return finding["excerpt"]
    off = min(len(text), starts[line] + max(0, finding.get("column", 1) - 1))
    return text[max(0, off - before) : off] + HERE + text[off : off + after]


def group_of(finding: Dict[str, Any]) -> str:
    """``rule|pattern``: the finding's identity with digits and spaces folded,
    so identical hits on many pages share one tiebreak."""
    from bench.core import identity

    sig = re.sub(r"\s+", " ", identity(finding).strip().lower())
    sig = re.sub(r"\d+", "0", sig)[:120]
    return f"{finding['rule']}|{sig}"


def label_all(
    result: Dict[str, Any], manifest: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Rows for labels.jsonl, and the disagreements left without a tiebreak."""
    guide, ties = _load(GUIDE), _load(TIEBREAK)
    rules = guide.get("rules", {})
    storage = {p["id"]: (PAGES if p["redistributable"] else PRIVATE) for p in manifest["pages"]}
    stripped = {p["id"] for p in manifest["pages"]
                if any("script element" in n for n in p.get("notes", []))}
    rows, open_ = [], []
    for pid, page in sorted(result["pages"].items()):
        base = storage.get(pid, PAGES)
        for f in page["findings"]:
            crit = rules.get(f["rule"], {})
            a, why_a = _apply(crit.get("a"), f["excerpt"], f"{f['rule']} pass a")
            b, why_b = _apply(crit.get("b"), context(f, base, scripts_removed=pid in stripped),
                              f"{f['rule']} pass b")
            row = {
                "key": f["key"],
                "page": pid,
                "rule": f["rule"],
                "pass": f["pass"],
                "pass_a": a,
                "pass_b": b,
                "tiebreak": None,
                "final": None,
                "why": why_b or why_a,
                "model_made": True,
            }
            if a is None or b is None:
                row["final"] = None  # not labelled yet
            elif a == b and a != "cantTell":
                row["final"] = a
            else:
                t = (
                    ties.get(f["key"])
                    or ties.get(group_of(f))
                    or ties.get(f"{f['rule']}|{a}>{b}")
                    or ties.get(f"{f['rule']}|*")
                )
                if t:
                    chosen = {"a": a, "b": b}.get(t.get("follow", ""), t.get("label"))
                    row["tiebreak"] = _check_label(chosen, f"tiebreak {f['key']}")
                    row["final"] = row["tiebreak"]
                    row["why"] = t.get("why", row["why"])
                elif a == b:  # both passes could not decide and no third reading exists
                    row["final"] = "cantTell"
                else:
                    row["final"] = "cantTell"
                    open_.append(
                        {
                            "key": f["key"],
                            "group": group_of(f),
                            "a": a,
                            "b": b,
                            "excerpt": f["excerpt"][:200],
                        }
                    )
            rows.append(row)
    return rows, open_


def write(rows: Iterable[Dict[str, Any]], path: Path = LABELS) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=True, sort_keys=True) + "\n")
            n += 1
    return n


def load(path: Path = LABELS) -> Dict[str, Dict[str, Any]]:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["key"]] = r
    return out


__all__ = ["label_all", "write", "load", "context", "group_of", "LabelError", "SEEDED"]
