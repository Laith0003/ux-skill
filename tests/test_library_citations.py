"""Every book citation in the shipped guidance points at the library.

Guidance cites a book by its library code and page (``B46 p.193``), never by
author. A code must be one of B01 to B96 and must be one that
research/library/topics/ actually uses, so a citation can always be traced to
a lesson. A code with no page is not a citation a reader can check.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Set

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "research" / "library" / "topics"
SHIPPED = ("references", "commands", "agents", "data", "engine", "figma-skill")
SUFFIXES = {".md", ".json", ".py", ".txt", ".yaml", ".yml", ".html"}
FIRST, LAST = 1, 96

# A code is B and two or three digits, not part of a word, a hex color or a
# hyphenated name. Its page follows as "p." or "pp." and a number.
CODE = re.compile(r"(?<![#\w-])B(\d{2,3})(?![\w-])")
PAGE = re.compile(r"\s+pp?\.\s*\d")


def library_codes(topics: Path = TOPICS) -> Set[str]:
    """Every code the library's topic files cite."""
    codes: Set[str] = set()
    for f in sorted(topics.glob("*.md")):
        codes |= {f"B{m.group(1)}" for m in CODE.finditer(f.read_text(encoding="utf-8"))}
    return codes


def citation_problems(text: str, where: str, known: Set[str]) -> List[str]:
    """One message per bad citation in `text`, each naming the place, the
    code and the fix."""
    out = []
    for number, line in enumerate(text.splitlines(), 1):
        for m in CODE.finditer(line):
            code, n = f"B{m.group(1)}", int(m.group(1))
            at = f"{where}:{number}"
            if not FIRST <= n <= LAST or len(m.group(1)) != 2:
                out.append(f"{at} cites {code}; library codes run B01 to B96 "
                           f"(research/library/ACKNOWLEDGEMENTS.md). Fix the code or cite the standard.")
            elif code not in known:
                out.append(f"{at} cites {code}, which no lesson in research/library/topics/ uses. "
                           f"Cite a code the topics use for this lesson.")
            elif not PAGE.match(line, m.end()):
                out.append(f"{at} cites {code} with no page. Add the page as '{code} p.<page>'.")
    return out


def _shipped_files() -> Iterable[Path]:
    for top in SHIPPED:
        for p in sorted((ROOT / top).rglob("*")):
            if p.is_file() and p.suffix in SUFFIXES and "__pycache__" not in p.parts:
                yield p


def test_the_library_uses_codes_in_range():
    known = library_codes()
    assert known, "research/library/topics/ cites no codes; the library is missing"
    bad = sorted(c for c in known if not FIRST <= int(c[1:]) <= LAST)
    assert not bad, f"topics cite {bad}; codes run B01 to B96"


def test_every_shipped_citation_is_a_library_code_with_a_page():
    known = library_codes()
    problems = []
    for p in _shipped_files():
        problems += citation_problems(p.read_text(encoding="utf-8", errors="replace"),
                                      str(p.relative_to(ROOT)), known)
    assert not problems, "\n".join(problems)


@pytest.mark.parametrize("text,fault", [
    ("Group the rest (B97 p.12).", "library codes run B01 to B96"),
    ("Group the rest (B00 p.12).", "library codes run B01 to B96"),
    ("Group the rest (B100 p.12).", "library codes run B01 to B96"),
    ("Group the rest (B50 p.12).", "which no lesson in research/library/topics/ uses"),
    ("Group the rest (B46).", "with no page"),
])
def test_a_bad_citation_is_named_with_its_fix(text, fault):
    known = {"B46"}
    problems = citation_problems(text, "references/x.md", known)
    assert len(problems) == 1 and fault in problems[0], problems
    assert problems[0].startswith("references/x.md:1 cites ")


@pytest.mark.parametrize("text", [
    "Six hues at most (B46 p.193-194, 746-747; B46 pp. 12).",
    "Accent #B46 and #B4612A, A4 and B5 paper, a B2B shop, the B46-grid.",
    "WCAG 2.2 SC 2.2.1 decides this one.",
])
def test_good_citations_and_lookalikes_pass(text):
    assert citation_problems(text, "references/x.md", {"B46"}) == []
