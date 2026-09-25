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
RUL = "decorative-accent-ruler"
HAM = "nav-equal-hamburger-desktop"

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
    # The engine's own token file: custom properties, color-scheme, media and
    # selector blocks and @property descriptors. Its name says nothing.
    "imp/b1.css": {IMP: []},
    "imp/layer-a.css": {IMP: []},
    "imp/b2.css": {IMP: [1]},
    "imp/layer-b.css": {IMP: []},
    # A token layer (mostly custom-property definitions) is judged on its
    # definitions only by rules written for token definitions; its usage
    # lines, and a page's own stylesheet, keep every rule.
    "tokdef/client-tokens.css": {
        "timing-300ms-default": [23],
        "cubic-bezier-material-only": [23],
        "glow-shadow-zero-offset": [5],
        "default-font-only": [6],
    },
    "tokdef/page.css": {
        "timing-300ms-default": [1, 2],
        "cubic-bezier-material-only": [1, 3],
    },
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
    # Round 3. H3: a ring with no tag, class or id on its subject covers any
    # element in its context and specificity decides; :not(:focus-visible)
    # removals are safe; rings under another media query, a weaker outline
    # against !important, and outline classes on an inline removal do not
    # count. See KNOWN_GAPS for the two lines that still pass wrongly.
    "r3/h3-app.html": {OUT: [6, 13]},
    "r3/h3-blog.html": {OUT: [4]},
    "r3/h3-docs.html": {OUT: [8]},
    "r3/imp/main.css": {IMP: [1]},
    "r3/imp/base.css": {IMP: []},
    "r3/imp/tokens.css": {IMP: []},
    # Round 3. H4: landing pages fire, docs pages and app shells do not.
    "r3/h4-docs-a.html": {IMG: []},
    "r3/h4-docs-b.html": {IMG: []},
    "r3/h4-docs-c-landing-table.html": {IMG: [1]},
    "r3/h4-app-a-dashboard.html": {IMG: []},
    "r3/h4-app-b-chat.html": {IMG: []},
    "r3/h4-app-c-spa-root.html": {IMG: []},
    "r3/h4-app-d-form-wrapper.html": {IMG: [1]},
    "r3/h4-blog-a-hero-css.html": {IMG: []},
    "r3/h4-blog-b-astro-image.astro": {IMG: []},
    "r3/h4-blog-c-landing-in-article.html": {IMG: [1]},
    # An eyebrow is text only: every build of a line, dash or dot beside it
    # fires, and real separators (hr, table rules, a card edge, a full-width
    # underline, list and icon marks) stay clean.
    "ruler/r1-pseudo-logical.css": {RUL: [2]},
    "ruler/r2-pseudo-border.css": {RUL: [1, 7]},
    "ruler/r3-label-edge.css": {RUL: [1, 2, 3]},
    "ruler/r4-background-line.css": {RUL: [3]},
    "ruler/r5-dash-content.css": {RUL: [1, 2]},
    "ruler/r6-heading-underline.css": {RUL: [1]},
    "ruler/r7-empty-span.html": {RUL: [1, 3, 6]},
    "ruler/r8-svg.html": {RUL: [1, 2, 4]},
    "ruler/r9-text-dash.html": {RUL: [1, 3]},
    "ruler/r10-tailwind.html": {RUL: [1, 2, 4]},
    "ruler/r11-component.tsx": {RUL: [3]},
    "ruler/c1-separators.html": {RUL: []},
    # A menu button is judged in any language and by structure, and passes
    # when any CSS hides it at desktop width (1280px): a plain media query in
    # a <style> or a linked stylesheet, a hidden ancestor, a Tailwind or
    # Bootstrap breakpoint class, or the hidden attribute on its menu.
    "nav/n1-linked-css.html": {HAM: []},
    "nav/n1.css": {HAM: []},
    "nav/n2-hidden-above-1024.html": {HAM: []},
    "nav/n3-em-query.html": {HAM: []},
    "nav/n4-arabic.html": {HAM: [2]},
    "nav/n5-arabic-hidden.html": {HAM: []},
    "nav/n6-tailwind.html": {HAM: [3]},
    "nav/n7-structural.html": {HAM: [2]},
    "nav/n8-dropdown.html": {HAM: []},
    "nav/n9-wide-only.html": {HAM: [4]},
    "nav/n10-parent-hidden.html": {HAM: []},
    "nav/n11-close-in-menu.html": {HAM: []},
    "nav/n12-bootstrap.html": {HAM: []},
    "nav/n13-component.tsx": {HAM: [5]},
    # The first review's probes, with neutral copy. Every form of the ruler
    # it named fires; the separators, icons, table headers, badges and
    # sidebar links it listed stay clean. b5 is a known gap (KNOWN_GAPS).
    # l3's second line fires on the older h-px class pattern, on a list
    # item's dash bullet; it did before this rule's post check too.
    "ruler/rv-d-a1-eyebrow-px.css": {RUL: [2]},
    "ruler/rv-d-a2-label-tokens.css": {RUL: [2]},
    "ruler/rv-d-a3-tag-rem.css": {RUL: [1]},
    "ruler/rv-d-a4-calc-width.css": {RUL: [1]},
    "ruler/rv-d-a5-flex-basis.css": {RUL: [1]},
    "ruler/rv-d-a6-var-rule-length.css": {RUL: [1]},
    "ruler/rv-d-a7-camel-eyebrow.css": {RUL: [1]},
    "ruler/rv-d-a8-border-top.css": {RUL: [1]},
    "ruler/rv-d-a9-nested.scss": {RUL: [3]},
    "ruler/rv-d-b1-span-first.html": {RUL: [1]},
    "ruler/rv-d-b2-tw-sibling.html": {RUL: [1]},
    "ruler/rv-d-b3-i-after.html": {RUL: [1]},
    "ruler/rv-d-b4-div-rule.html": {RUL: [1]},
    "ruler/rv-d-b5-no-eyebrow-class.html": {RUL: []},
    "ruler/rv-d-b6-data-attr.html": {RUL: [1]},
    "ruler/rv-d-b7-jsx.tsx": {RUL: [2]},
    "ruler/rv-d-c1-border-left.css": {RUL: [1]},
    "ruler/rv-d-c2-inline-start-token.css": {RUL: [1]},
    "ruler/rv-d-c3-tw.html": {RUL: [1]},
    "ruler/rv-d-c4-longhands.css": {RUL: [1]},
    "ruler/rv-d-c5-inset-shadow.css": {RUL: [1]},
    "ruler/rv-d-d1-shorthand.css": {RUL: [1]},
    "ruler/rv-d-d2-longhands.css": {RUL: [1]},
    "ruler/rv-d-d3-pseudo-gradient.css": {RUL: [1]},
    "ruler/rv-d-d4-url-line.css": {RUL: [1]},
    "ruler/rv-d-e1-svg-line.html": {RUL: [1]},
    "ruler/rv-d-e2-svg-path-sibling.html": {RUL: [1]},
    "ruler/rv-d-e3-svg-rect-after.html": {RUL: [1]},
    "ruler/rv-d-e4-img-line.html": {RUL: [1]},
    "ruler/rv-d-f1-span-dot.html": {RUL: [1]},
    "ruler/rv-d-f2-pseudo-dot.css": {RUL: [1]},
    "ruler/rv-d-f3-content-bullet.css": {RUL: [1]},
    "ruler/rv-d-f4-typed.html": {RUL: [1, 2]},
    "ruler/rv-d-f5-tw-dot.html": {RUL: [1]},
    "ruler/rv-c-h1-hr.html": {RUL: []},
    "ruler/rv-c-h2-hr-styled.css": {RUL: []},
    "ruler/rv-c-h3-hr-after-eyebrow.html": {RUL: []},
    "ruler/rv-c-i1-star-svg.html": {RUL: []},
    "ruler/rv-c-i2-icon-fonts.html": {RUL: []},
    "ruler/rv-c-i3-mask-icon.css": {RUL: []},
    "ruler/rv-c-i4-lucide-minus.html": {RUL: []},
    "ruler/rv-c-k1-card-accent.css": {RUL: []},
    "ruler/rv-c-k2-callout-tw.html": {RUL: []},
    "ruler/rv-c-k3-eyebrow-underline.css": {RUL: []},
    "ruler/rv-c-l1-li-dot.css": {RUL: []},
    "ruler/rv-c-l2-item-dash.css": {RUL: []},
    "ruler/rv-c-t1-table.css": {RUL: []},
    "ruler/rv-c-t2-tw-th.html": {RUL: []},
    "ruler/rv-c-t3-th-sort.html": {RUL: []},
    "ruler/rv-c-l3-li-dash.html": {RUL: [2]},
    "ruler/rv-e-x1-status-badge.html": {RUL: []},
    "ruler/rv-e-x2-sidebar-active.html": {RUL: []},
    "ruler/rv-e-x3-pill-eyebrow.css": {RUL: []},
    # Menu buttons named in words, visible or spoken, in English and Arabic;
    # a state class such as is-closed does not read as a close button.
    "nav/rv-h-h01-en-aria.html": {HAM: [3]},
    "nav/rv-h-h02-ar-aria.html": {HAM: [2]},
    "nav/rv-h-h03-en-visible-text.html": {HAM: [1]},
    "nav/rv-h-h04-ar-visible-text.html": {HAM: [1]},
    "nav/rv-h-h05-glyph.html": {HAM: [1]},
    "nav/rv-h-h06-closed-class.html": {HAM: [1]},
    "nav/rv-h-h07-ar-no-aria.html": {HAM: [1]},
    "nav/rv-h-h08-desktop-hidden-ok.html": {HAM: []},
    "nav/rv-h-h09-tw-md-hidden-ok.html": {HAM: []},
    "nav/rv-h-h10-tw-xl-shown.html": {HAM: [1]},
    "nav/rv-h-h11-ar-tw-ok.html": {HAM: []},
    "nav/rv-h-h12-ar-hidden-media-ok.html": {HAM: []},
    "nav/rv-h-h13-disclosure-class.html": {HAM: [1]},
    # A page stylesheet padded with custom properties is not a token layer.
    "tokdef/rv-t-page-inline.css": {"cubic-bezier-material-only": [2], "transition-property-all": [2]},
    "tokdef/rv-t-page-plain.css": {"cubic-bezier-material-only": [3], "transition-property-all": [10]},
    "tokdef/rv-t-page-padded.css": {"cubic-bezier-material-only": [3], "transition-property-all": [22]},
}

# Lines that still pass although they should fire. Each is pinned at its
# current result so a change in either direction is noticed; move a line into
# EXPECT when the gap is closed.
KNOWN_GAPS = {
    "r3/h3-blog.html": {OUT: (6, "a later .share .share-link:focus-visible { box-shadow: none } cancels the ring")},
    "r3/h3-docs.html": {OUT: (6, "a .toc > a ring is read as .toc a; child combinators are not compared")},
    "ruler/rv-d-b5-no-eyebrow-class.html": {RUL: (1, "a label with no eyebrow class and no uppercase, tracked utilities is not read as an eyebrow")},
}


def test_known_gaps_are_still_open():
    for name, rules in KNOWN_GAPS.items():
        path = PROBES / name
        findings = lint_text(str(path), path.read_text(encoding="utf-8"))
        for rule_id, (line, why) in rules.items():
            fired = any(f.rule_id == rule_id and f.line == line for f in findings)
            assert not fired, (
                f"probes/{name}:{line} now fires {rule_id} ({why}). The gap is closed: "
                f"add line {line} to EXPECT and remove it from KNOWN_GAPS"
            )


# The reviewer's isolated H3 cases, one stylesheet each.
ISO = [
    ("global-fv", "button { outline: none; }\n:focus-visible { outline: 2px solid #06c; }\n", False),
    ("star-fv", "a, button { outline: none; }\n*:focus-visible { outline: 2px solid #06c; }\n", False),
    ("desc-universal", ".post-body a { outline: none; }\n.post-body :focus-visible { outline: 2px solid #06c; }\n", False),
    ("where", ".icon-btn { outline: none; }\n:where(.btn, .icon-btn):focus-visible { outline: 2px solid #06c; }\n", False),
    ("is", ".icon-btn { outline: none; }\n:is(.btn, .icon-btn):focus-visible { outline: 2px solid #06c; }\n", False),
    ("has-bare", ".tabs [role=tab] { outline: none; }\n.tabs:has(:focus-visible) { box-shadow: 0 0 0 2px #06c; }\n", False),
    ("not-fv alone", "button:focus:not(:focus-visible) { outline: none; }\n", False),
    ("important", ".doc a { outline: none !important; }\n.doc a:focus-visible { outline: 2px solid #06c; }\n", True),
    ("important both", ".doc a { outline: none !important; }\n.doc a:focus-visible { outline: 2px solid #06c !important; }\n", False),
    ("dark-only", ".cta { outline: none; }\n@media (prefers-color-scheme: dark) { .cta:focus-visible { outline: 2px solid white; } }\n", True),
    ("zero-shadow", ".z { outline: none; }\n.z:focus-visible { box-shadow: 0 0 0 0 #06c; }\n", True),
    ("star vs specific", "*:focus-visible { outline: 2px solid blue; }\n.search input:focus { outline: none; }\n", True),
    ("global ring weaker", ":focus-visible { outline: 2px solid blue; }\nbutton:focus { outline: none; }\n", True),
    ("global shadow ring", "button:focus { outline: none; }\n:focus-visible { box-shadow: 0 0 0 3px blue; }\n", False),
]


@pytest.mark.parametrize("name,css,should_fire", ISO, ids=[c[0] for c in ISO])
def test_isolated_outline_case(name, css, should_fire):
    fired = any(f.rule_id == OUT for f in lint_text("x.css", css))
    assert fired is should_fire, f"{name}: expected {'a finding' if should_fire else 'no finding'}"


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
