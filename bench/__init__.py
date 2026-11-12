"""ux-bench: the frozen corpus and the per-rule precision and recall report.

Layout (all paths relative to this folder):

- manifest.json: one entry per page (id, origin, licence, redistributable,
  url, capture date, sha256, split, page type, direction, and for generated
  pages the brief and the generator).
- sources.json: what capture.py fetched for the designer-built pages.
- briefs/: the ten fixed briefs the generated pages were built from.
- pages/<id>/index.html: the frozen redistributable pages.
- pages/_css/: every stored stylesheet, once, named by content hash. The
  manifest lists per page which are its own (linted with the page) and which
  are vendor files (a framework or icon set: read only by the render pass).
- pages/NOTICE: the licence text for every source the pages come from.
- private/<id>/: snapshots that may not be redistributed. Never committed;
  the manifest keeps their url, date, sha256, findings and labels.
- expected/<id>.json: the golden findings, rewritten only by
  ``python -m bench run --update-expected``.
- labels/labels.jsonl: one row per finding key with two labelling passes and a
  tiebreak, all marked model-made until a person confirms a sample.
- seeded/: small pages with planted faults mapped to rule ids, and their
  clean twins, for recall.

Run ``python -m bench --help`` from the repository root.
"""

from __future__ import annotations

from pathlib import Path

BENCH = Path(__file__).resolve().parent
ROOT = BENCH.parent
MANIFEST = BENCH / "manifest.json"
PAGES = BENCH / "pages"
PRIVATE = BENCH / "private"
EXPECTED = BENCH / "expected"
LABELS = BENCH / "labels" / "labels.jsonl"
SEEDED = BENCH / "seeded"
OUT = BENCH / "out"
REPORT = BENCH / "report.md"

__all__ = [
    "BENCH",
    "ROOT",
    "MANIFEST",
    "PAGES",
    "PRIVATE",
    "EXPECTED",
    "LABELS",
    "SEEDED",
    "OUT",
    "REPORT",
]
