"""Review probes for the structural rules, kept as fixtures with exact lines.

Each file under ``tests/lint_corpus/probes`` came from a review of the
precision pass. ``EXPECT`` names, per file, the rules under test and the exact
lines each must fire on (an empty list means the rule must stay quiet). A
file may hold both a clean and a dirty case, which is why lines are compared
and not just "fired or not".
"""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.linter.core import lint_text

PROBES = Path(__file__).resolve().parent / "lint_corpus" / "probes"

IMG = "imagery-mandatory-missing"
OUT = "outline-none-no-focus-visible"
PH = "placeholder-as-label"
SKIP = "screen-reader-only-without-class"
SVG = "inline-svg-no-aria"
IMP = "css-import-render-blocking"

EXPECT = {
    # imagery: landing versus document or app, decided by structure
    "i1-landing-form.html": {IMG: [1]},
    "i2-landing-divs.html": {IMG: [1]},
    "i3-one-section.html": {IMG: [1]},
    "i4-leadgen.html": {IMG: []},
    "i5-articles.html": {IMG: [1]},
    "i6-two-sections-table.html": {IMG: [1]},
    "i7-docs.html": {IMG: []},
    # outline removal: a ring counts only when it covers the same element
    "o1-ring-elsewhere.css": {OUT: [2]},
    "o2-same-tag-other-context.css": {OUT: [2]},
    "o3-shared-generic-class.css": {OUT: []},
    "o4-focus-within-unrelated.css": {OUT: [2]},
    "o5-global-star.css": {OUT: [2]},
    "o6-weak-ring.css": {OUT: [1]},
    "o7-focus-visible-none.css": {OUT: [1]},
    "o8-transparent.css": {OUT: [1]},
    "o9-hover-ring.css": {OUT: [1]},
    "o10-has.html": {OUT: [4]},
    "o11-clean.css": {OUT: []},
    "o12-list.css": {OUT: [2]},
    "o13-print-ring.css": {OUT: [1]},
    "o14-bare-tags.css": {OUT: [2]},
    "o15-has-wrong-ancestor.html": {OUT: [3]},
    "o16-focus-within-bare.html": {OUT: [3]},
    "o17-border-none.css": {OUT: [1, 2]},
    "o18-inline-class-ring-unrelated.html": {OUT: [1]},
    "o19-scss-nested.scss": {OUT: [2]},
    "o20-inline-classes.html": {OUT: [1, 2]},
    "o21.html": {OUT: [3, 4, 5]},
    # placeholder as the only label
    "ph1-id-only.html": {PH: [2]},
    "ph2-label-no-for.html": {PH: [2]},
    "ph3-labelledby-self.html": {PH: [1]},
    "ph4-labelledby-empty-target.html": {PH: [2]},
    "ph5-aria-label-empty.html": {PH: [1, 2]},
    "ph6-label-closed-before.html": {PH: [2]},
    "ph7-component.tsx": {PH: [4, 5, 7]},
    "ph8-jsx-htmlfor.tsx": {PH: []},
    "ph9-label-for-in-comment.html": {PH: [2]},
    "ph10-labelledby-id-only-in-comment.html": {PH: [2]},
    "ph11-wrap-sibling.html": {PH: [2]},
    "ph12.vue": {PH: [4]},
    "ph13.tsx": {PH: [3, 4, 5]},
    # skip link: the first link to its target, before the target
    "s1-ltr.html": {SKIP: [2]},
    "s2-rtl.html": {SKIP: [2]},
    "s3-logo-first.html": {SKIP: [2]},
    "s4-body-attrs-script.html": {SKIP: [3]},
    "s5-component.tsx": {SKIP: [3]},
    "s6-skip-class-visible.html": {SKIP: [2]},
    "s7-content-first-link.html": {SKIP: [2]},
    "s8-link-in-head-comment.html": {SKIP: [3]},
    # SVG under an aria-hidden ancestor
    "v1.html": {SVG: [2, 3, 5]},
    "v2.tsx": {SVG: [5, 6]},
    "v3.html": {SVG: [5]},
    # @import: content decides first, the name only when the file cannot be read
    "imp/a1.css": {IMP: [1]},
    "imp/a2.css": {IMP: [1]},
    "imp/a3.css": {IMP: [1]},
    "imp/a4.css": {IMP: []},
    "imp/a5.css": {IMP: [1]},
    "imp/a6.css": {IMP: [1]},
    "imp/a7.css": {IMP: [1]},
    "imp/a8.css": {IMP: [2]},
    "imp/a9.css": {IMP: [2]},
    "imp/a10.html": {IMP: [1, 2]},
    "imp/base.css": {IMP: []},
    "imp/palette.css": {IMP: []},
    "imp/tokens.css": {IMP: []},
    # other review probes
    "misc/d1.tsx": {"div-onclick-no-role": [3, 4]},
    "misc/e1.html": {"emoji-in-ui": [1, 2, 5]},
    "misc/g1.css": {
        "chrome-y-multi-stop-gradient": [1],
        "animating-layout-properties": [3, 4],
        "body-font-weight-bold-or-700-keyword": [5],
        "body-text-shadow-on-prose": [6],
        "body-cursor-pointer-default": [],
    },
    "misc/h1.css": {"hover-only-card-actions": [1]},
    "misc/h2.css": {"hover-only-card-actions": []},
    "misc/s.htm": {"image-format-jpg-no-webp-avif": [1], "arbitrary-z-index-9999": [2]},
    "misc/s.svelte": {"image-format-jpg-no-webp-avif": [1], "arbitrary-z-index-9999": [2]},
}


def test_every_probe_file_has_an_expectation():
    files = {str(p.relative_to(PROBES)) for p in PROBES.rglob("*") if p.is_file()}
    missing = sorted(files - set(EXPECT))
    stale = sorted(set(EXPECT) - files)
    assert not missing, f"probe files with no entry in EXPECT: {missing}. Add the rule and lines they must fire on"
    assert not stale, f"EXPECT names files that do not exist: {stale}. Remove them or restore the file"


@pytest.mark.parametrize("name", sorted(EXPECT))
def test_probe(name):
    path = PROBES / name
    findings = lint_text(str(path), path.read_text(encoding="utf-8"))
    for rule_id, lines in EXPECT[name].items():
        got = sorted({f.line for f in findings if f.rule_id == rule_id})
        assert got == sorted(lines), (
            f"probes/{name}: {rule_id} fired on lines {got}, expected {sorted(lines)}. "
            f"Fix the rule's pattern or its post check in engine/linter/structure.py"
        )
