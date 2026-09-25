"""A focus ring on a parent counts when the stylesheet and the page are separate files.

Each folder under ``tests/lint_corpus/crossfile`` holds a stylesheet that removes
an input's outline and draws the ring on its parent with ``:focus-within``, and
one or more pages. The ring covers the input only when every page that links the
stylesheet puts the input inside that parent, so the linter reads the pages that
load the stylesheet: the pages in the lint set, and the ones beside the
stylesheet or one folder above it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from engine.linter.core import lint, lint_text, stylesheet_pages

CROSS = Path(__file__).resolve().parent / "lint_corpus" / "crossfile"
OUT = "outline-none-no-focus-visible"


def _out_lines(target: Path) -> list:
    report = lint([target], "high")
    return sorted({f.line for f in report.findings if f.rule_id == OUT and f.file.endswith(".css")})


@pytest.mark.parametrize("target,lines", [
    # The page wraps the input in the ring's parent: clean.
    ("wrapped", []),
    ("wrapped/styles.css", []),
    ("nested/css/site.css", []),
    ("nested", []),
    ("rooted", []),
    ("rooted/assets/app.css", []),
    # A stylesheet two folders below its page, linted alone: the walk reaches the project root.
    ("deep/assets/css/site.css", []),
    ("deep", []),
    # A root-relative link names the root sheet, never a same-named sheet in a sub folder.
    ("rootlink/sub/styles.css", [2]),
    # The input sits outside the parent, or no page loads the stylesheet: the removal is bare.
    ("unwrapped", [2]),
    ("unwrapped/styles.css", [2]),
    ("unlinked", [2]),
    ("unlinked/styles.css", [2]),
    # One page of two leaves the input outside: a keyboard user there sees no ring.
    ("twopages", [2]),
    ("twopages/styles.css", [2]),
])
def test_parent_ring_across_files(target, lines):
    assert _out_lines(CROSS / target) == lines, (
        f"crossfile/{target}: {OUT} should fire on lines {lines}. "
        f"The parent ring check reads the pages that link the stylesheet (engine/linter/core.py stylesheet_pages)"
    )


def test_the_stylesheet_alone_still_fires_without_pages():
    """lint_text with no pages cannot see the markup, so the removal stays flagged."""
    css = (CROSS / "wrapped" / "styles.css").read_text(encoding="utf-8")
    assert any(f.rule_id == OUT for f in lint_text("styles.css", css))


def test_lint_text_takes_the_pages_as_text():
    css = (CROSS / "wrapped" / "styles.css").read_text(encoding="utf-8")
    page = (CROSS / "wrapped" / "index.html").read_text(encoding="utf-8")
    bad = (CROSS / "unwrapped" / "index.html").read_text(encoding="utf-8")
    assert not any(f.rule_id == OUT for f in lint_text("styles.css", css, pages=[("index.html", page)]))
    assert any(f.rule_id == OUT for f in lint_text("styles.css", css, pages=[("index.html", bad)]))


def test_stylesheet_pages_finds_only_the_pages_that_link_it():
    names = lambda css, extra=(): sorted(p.name for p in stylesheet_pages(css, extra))
    assert names(CROSS / "twopages" / "styles.css") == ["a.html", "b.html"]
    assert names(CROSS / "unlinked" / "styles.css") == []
    assert names(CROSS / "nested" / "css" / "site.css") == ["index.html"]
    assert names(CROSS / "rooted" / "assets" / "app.css") == ["index.html"]
    assert names(CROSS / "deep" / "assets" / "css" / "site.css") == ["index.html"]
    assert names(CROSS / "rootlink" / "sub" / "styles.css") == []


def test_lint_reads_each_page_once(monkeypatch):
    """The lint run reads a page once, however many stylesheets it links."""
    from pathlib import Path as _P
    reads = []
    real = _P.read_text

    def counting(self, *a, **k):
        if self.suffix == ".html":
            reads.append(self.resolve())
        return real(self, *a, **k)
    monkeypatch.setattr(_P, "read_text", counting)
    lint([CROSS / "twopages"], "high")
    assert len(reads) == len(set(reads)), sorted(reads)


@pytest.mark.parametrize("sheet,fires", [("wrapped/styles.css", False), ("unwrapped/styles.css", True),
                                         ("deep/assets/css/site.css", False)])
def test_the_write_hook_reads_the_pages_too(sheet, fires):
    """The hook lints one written stylesheet; it reads the pages up to the project root."""
    hook = Path(__file__).resolve().parent.parent / "bin" / "ux-lint-hook.py"
    css = CROSS / sheet
    root = CROSS / sheet.split("/")[0]
    payload = {"session_id": "test", "hook_event_name": "PostToolUse", "tool_name": "Write",
               "tool_input": {"file_path": str(css)}, "cwd": str(root)}
    env = {k: v for k, v in os.environ.items() if k not in ("UXSKILL_LINT_ON_WRITE", "CLAUDE_PROJECT_DIR")}
    result = subprocess.run([sys.executable, str(hook)], input=json.dumps(payload),
                            capture_output=True, text=True, env=env, timeout=60)
    assert (OUT in result.stdout + result.stderr) is fires, result.stdout + result.stderr
