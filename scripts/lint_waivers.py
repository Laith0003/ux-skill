"""Wrap quoted text in a page with ux-lint-off regions that name the rules it trips.

Some pages quote the fingerprints they document: the rule catalog, "before"
code samples, a taxonomy post. The linter would flag the quotes as if the page
shipped them. `wrap_quoted` lints the page, and around each quoted element that
trips a rule it writes

    <!-- ux-lint-off rule-a, rule-b -->...quoted element...<!-- ux-lint-on -->

naming exactly the rules found there, nothing else. The comments are inserted
inline, so line numbers do not move. Elements that trip nothing stay unwrapped.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.linter import lint  # noqa: E402

OFF, ON = "<!-- ux-lint-off {} -->", "<!-- ux-lint-on -->"


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def wrap_quoted(html: str, patterns: Iterable[str], suffix: str = ".html") -> str:
    """Wrap every match of ``patterns`` (regexes for whole quoted elements) that
    trips a rule. Returns the new page text."""
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / ("page" + suffix)
        probe.write_text(html, encoding="utf-8")
        findings = lint([str(probe)]).findings
    by_line = {}
    for f in findings:
        by_line.setdefault(f.line, set()).add(f.rule_id)

    spans: List[Tuple[int, int, str]] = []
    for pat in patterns:
        for m in re.finditer(pat, html, re.S):
            first, last = _line_of(html, m.start()), _line_of(html, m.end())
            ids = set()
            for n in range(first, last + 1):
                ids |= by_line.get(n, set())
            if ids:
                spans.append((m.start(), m.end(), ", ".join(sorted(ids))))
    for start, end, ids in sorted(spans, reverse=True):
        html = html[:start] + OFF.format(ids) + html[start:end] + ON + html[end:]
    return html
