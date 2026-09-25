"""Rules that judge structure, not just a pattern, measured on both sides.

``tests/lint_corpus/cases/<rule-id>/clean`` holds files the rule must stay
quiet on, and ``cases/<rule-id>/dirty`` holds files it must flag. A file whose
name starts with ``_`` supports another fixture (for example, a stylesheet
that a dirty fixture imports) and is not judged itself.

Every rule with a ``post`` check in ``data/anti-patterns.json`` needs both
kinds, so a structural waiver can never be widened into silence unnoticed.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.linter.core import _compile_rules, _scope_matches, lint_text

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(__file__).resolve().parent / "lint_corpus"
CASES = CORPUS / "cases"
ENTRIES = json.loads((ROOT / "data" / "anti-patterns.json").read_text(encoding="utf-8"))["entries"]
RULE_IDS = {e["id"] for e in ENTRIES}
POST_RULES = sorted(e["id"] for e in ENTRIES if e["detection"].get("post"))
HOOK_SUFFIXES = (".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".blade.php")


def _case_files():
    for p in sorted(CASES.rglob("*")):
        if p.is_file() and not p.name.startswith("_"):
            rule, kind = p.relative_to(CASES).parts[:2]
            yield pytest.param(p, rule, kind, id=str(p.relative_to(CASES)))


def _fired(path: Path) -> set:
    return {f.rule_id for f in lint_text(str(path), path.read_text(encoding="utf-8"))}


@pytest.mark.parametrize("path,rule_id,kind", list(_case_files()))
def test_case_fixture(path, rule_id, kind):
    assert kind in ("clean", "dirty"), f"{path}: put the file under clean/ or dirty/"
    fired = rule_id in _fired(path)
    if kind == "dirty":
        assert fired, f"{path.relative_to(CORPUS)}: {rule_id} did not fire. Tighten its post check in engine/linter/structure.py"
    else:
        assert not fired, f"{path.relative_to(CORPUS)}: {rule_id} fired on a clean case. Fix its pattern or post check"


def test_case_folders_name_real_rules():
    unknown = sorted(p.name for p in CASES.iterdir() if p.is_dir() and p.name not in RULE_IDS)
    assert not unknown, f"tests/lint_corpus/cases has folders for unknown rules: {unknown}. Rename them to a rule id"


@pytest.mark.parametrize("rule_id", POST_RULES)
def test_every_structural_rule_has_clean_and_dirty_cases(rule_id):
    for kind in ("clean", "dirty"):
        folder = CASES / rule_id / kind
        files = [p for p in folder.glob("*") if p.is_file() and not p.name.startswith("_")] if folder.is_dir() else []
        assert files, f"{rule_id} has a post check but no {kind} case: add tests/lint_corpus/cases/{rule_id}/{kind}/<file>"


def test_every_post_check_exists():
    from engine.linter.structure import POST_CHECKS

    for e in ENTRIES:
        name = e["detection"].get("post")
        if name:
            assert name in POST_CHECKS, f"{e['id']}: post check {name!r} is not in engine/linter/structure.py POST_CHECKS"


def test_every_clean_ui_file_is_in_scope_for_most_rules():
    rules = _compile_rules()
    for p in sorted((CORPUS / "clean").rglob("*")):
        if not p.is_file() or not p.name.lower().endswith(HOOK_SUFFIXES):
            continue
        in_scope = sum(_scope_matches(p, r["scope"]) for r in rules)
        assert in_scope >= 50, (
            f"{p.relative_to(CORPUS)} is in scope for only {in_scope} rules, so a clean result proves little. "
            f"Map its extension in SCOPE_ALIASES in engine/linter/core.py"
        )


# ---------------------------------------------------------------------------
# Recall probes: each fired on the linter before the precision pass, and must
# keep firing. Each quiet twin must stay quiet.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,snippet,rule_id,should_fire", [
    ("a.html", '<input id="email" type="email" placeholder="Email address">', "placeholder-as-label", True),
    ("a.html", '<label for="email">Email</label><input id="email" placeholder="you@x.com">',
     "placeholder-as-label", False),
    ("a.html", '<input aria-labelledby="missing" placeholder="Search">', "placeholder-as-label", True),
    ("a.css", ".btn:focus-visible{outline:2px solid}\n.search input:focus{outline:none;}",
     "outline-none-no-focus-visible", True),
    ("a.css", "button:focus{outline:none;}\nbutton:focus-visible{outline:2px solid blue}",
     "outline-none-no-focus-visible", False),
    ("a.html", '<button type="button"><span>&#x1F680; Launch</span></button>', "emoji-in-ui", True),
    ("a.html", '<div class="card-title">&#x2728; Features</div>', "emoji-in-ui", True),
    ("a.html", "<p>Shipped it today &#x1F389;</p>", "emoji-in-ui", False),
    ("a.css", ".a { transition: max-height 300ms; }", "animating-layout-properties", True),
    ("a.css", ".a { transition: min-width 200ms; }", "animating-layout-properties", True),
    ("a.css", ".a { transition: opacity 200ms, transform 200ms; }", "animating-layout-properties", False),
    ("a.css", ".a { background: linear-gradient(90deg, #ff0000, #ff8800, #ffee00, #00cc44); }",
     "chrome-y-multi-stop-gradient", True),
    ("a.css", ".a { background: linear-gradient(90deg, #111, #333, #555); }", "chrome-y-multi-stop-gradient", False),
    ("a.css", "body.dark { font-weight: 700 }", "body-font-weight-bold-or-700-keyword", True),
    ("a.css", "pre { font-weight: 700 }", "body-font-weight-bold-or-700-keyword", False),
    ("a.css", "p.lead { text-shadow: 0 1px 2px #000 }", "body-text-shadow-on-prose", True),
    ("a.css", "picture { text-shadow: 0 1px 2px #000 }", "body-text-shadow-on-prose", False),
    ("a.css", "p.intro { letter-spacing: 0.4em }", "body-letter-spacing-too-wide", True),
    ("a.css", "body.app { cursor: pointer }", "body-cursor-pointer-default", True),
    ("a.css", "p.hero { font-weight: 900 }", "font-weight-numeric-100-or-900-on-body", True),
    ("a.tsx", '<div role="presentation" onClick={go}>x</div>', "div-onclick-no-role", True),
    ("a.tsx", '<div role="none" onClick={go}>x</div>', "div-onclick-no-role", True),
    ("a.tsx", '<div role="button" tabIndex={0} onClick={go} onKeyDown={key}>x</div>', "div-onclick-no-role", False),
    ("a.tsx", '<div role="tab" tabIndex={0} onClick={go} onKeyDown={key}>x</div>', "div-onclick-no-role", False),
    ("a.html", '<span aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M0 0h24"/></svg></span>',
     "inline-svg-no-aria", False),
    ("a.svelte", '<img src="a.jpg">\n<div style="z-index: 9999">x</div>', "image-format-jpg-no-webp-avif", True),
    ("a.svelte", '<img src="a.jpg">\n<div style="z-index: 9999">x</div>', "arbitrary-z-index-9999", True),
    ("a.htm", '<img src="a.jpg">', "image-format-jpg-no-webp-avif", True),
])
def test_recall_probe(tmp_path, name, snippet, rule_id, should_fire):
    path = tmp_path / name
    path.write_text(snippet, encoding="utf-8")
    assert (rule_id in _fired(path)) is should_fire


def test_picture_lookup_is_linear(tmp_path):
    """``skip_inside`` used to slice the file for every match; 20,000 images
    must lint in well under the hook's timeout."""
    import time

    body = "".join(f'<img src="p{i}.jpg" alt="Photo {i}">\n' for i in range(20000))
    text = f"<!doctype html><html><body>\n<picture><img src=\"a.jpg\" alt=\"a\"></picture>\n{body}</body></html>\n"
    start = time.perf_counter()
    findings = lint_text("big.html", text)
    elapsed = time.perf_counter() - start
    hits = [f for f in findings if f.rule_id == "image-format-jpg-no-webp-avif"]
    assert len(hits) == 20000, f"expected one finding per bare <img>, got {len(hits)}"
    assert elapsed < 5, f"linting 20,000 images took {elapsed:.1f} s; skip_inside must use a precomputed range lookup"
