"""Wrap quoted text in a page with ux-lint-off regions for an allowed set of rules.

Some pages quote the fingerprints they document: the rule catalog, "before"
code samples, a taxonomy post. The linter would flag the quotes as if the page
shipped them. `wrap_quoted` lints the page and, around a quoted element, writes

    <!-- ux-lint-off rule-a, rule-b -->...quoted element...<!-- ux-lint-on -->

A rule is named only when both hold:
  - a finding for it starts in the element's text or at the element's own
    opening tag, never at other markup around or inside the quote, and
  - the caller allows it for that element (an allowlist chosen from what the
    element quotes, never from what happens to fail).

The comments are inserted inline, so line numbers do not move. An element
with nothing to waive stays unwrapped. Existing regions are removed first, so
the function can run on its own output.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable, List, Set, Tuple, Union

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.linter import lint  # noqa: E402

OFF, ON = "<!-- ux-lint-off {} -->", "<!-- ux-lint-on -->"
REGION = re.compile(r"<!-- ux-lint-(?:off [^>]*|on) -->")
Allow = Union[Set[str], Callable[[str, int], Set[str]]]


def lint_findings(files: dict) -> dict:
    """Lint {name: text} in one pass; returns {name: [Finding, ...]}."""
    out = {name: [] for name in files}
    with tempfile.TemporaryDirectory() as tmp:
        paths = {}
        for name, text in files.items():
            path = Path(tmp) / name
            path.write_text(text, encoding="utf-8")
            paths[str(path)] = name
        for f in lint([tmp]).findings:
            out[paths[f.file]].append(f)
    return out


def _text_positions(html: str, start: int, end: int) -> List[Tuple[int, int]]:
    """Spans of [start, end) that are text, not tags."""
    spans, pos = [], start
    for tag in re.finditer(r"<[^>]*>", html[start:end]):
        a, b = start + tag.start(), start + tag.end()
        if a > pos:
            spans.append((pos, a))
        pos = b
    if pos < end:
        spans.append((pos, end))
    return spans


def wrap_quoted(html: str, elements: Iterable[Tuple[str, Allow]], suffix: str = ".html") -> str:
    """``elements``: (regex for a whole quoted element, allowed rule ids). The
    allowlist is a set, or a function of (html, element start) returning one."""
    html = REGION.sub("", html)
    findings = lint_findings({"page" + suffix: html})["page" + suffix]
    line_starts = [0] + [m.end() for m in re.finditer("\n", html)]
    hits = [(line_starts[f.line - 1] + max(f.column, 1) - 1, f.rule_id) for f in findings]

    spans = []
    for pattern, allow in elements:
        for m in re.finditer(pattern, html, re.S):
            allowed = allow(html, m.start()) if callable(allow) else allow
            text = _text_positions(html, m.start(), m.end())
            # A match may start in the text, or at the element's own opening
            # tag (a heading rule matches from <h2); never at markup inside it.
            ids = {rule for pos, rule in hits
                   if rule in allowed and (pos == m.start() or any(a <= pos < b for a, b in text))}
            if ids:
                spans.append((m.start(), m.end(), ", ".join(sorted(ids))))
    for start, end, ids in sorted(spans, reverse=True):
        html = html[:start] + OFF.format(ids) + html[start:end] + ON + html[end:]
    return html
