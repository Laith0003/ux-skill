"""The benchmark's own code: statistics, keys, determinism, capture, seeded
set, labels, report, diff, sample and ablation. Static passes only; the
render pass is exercised by python -m bench run, not here."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from bench import (
    PAGES,
    SEEDED,
    ablate,
    capture,
    core,
    label,
    manifest,
    report,
    sample,
    seeded,
    stats,
)
from bench import diff as bdiff


# Statistics ---------------------------------------------------------------


@pytest.mark.parametrize(
    "k,n,lo",
    [
        (35, 35, 0.90),
        (52, 53, 0.90),
        (67, 69, 0.90),
        (45, 50, 0.79),
        (10, 10, 0.72),
        (18, 20, 0.70),
    ],
)
def test_wilson_lower_bounds_match_the_eval_table(k, n, lo):
    assert round(stats.wilson(k, n)[0], 2) == lo


def test_wilson_rejects_impossible_counts_and_handles_zero():
    assert stats.wilson(0, 0) == (0.0, 1.0)
    with pytest.raises(ValueError, match="k=5 must lie between 0 and n=3"):
        stats.wilson(5, 3)


@pytest.mark.parametrize(
    "tp,fp,pages,tier",
    [
        (35, 0, 5, "blocking-candidate"),
        (35, 0, 4, "advisory"),
        (34, 0, 9, "advisory"),
        (52, 1, 12, "blocking-candidate"),
        (45, 5, 9, "advisory"),
        (18, 2, 9, "info"),
        (3, 3, 3, "below-info"),
        (0, 0, 0, "unmeasured"),
    ],
)
def test_tier_follows_the_plan_thresholds(tp, fp, pages, tier):
    assert stats.tier(tp, fp, pages) == tier


def test_no_rule_is_ever_blocking_yet():
    tiers = {stats.tier(tp, fp, pg) for tp in (0, 40, 400) for fp in (0, 1) for pg in (0, 5, 50)}
    assert "blocking" not in tiers


def test_alpha_matches_the_published_nominal_example():
    # Krippendorff (2011), four coders, twelve units, nominal: alpha = 0.743.
    raw = [
        [1, 1, None, 1],
        [2, 2, 3, 2],
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [2, 2, 2, 2],
        [1, 2, 3, 4],
        [4, 4, 4, 4],
        [1, 1, 2, 1],
        [2, 2, 2, 2],
        [None, 5, 5, 5],
        [None, None, 1, 1],
        [None, None, 3, None],
    ]
    units = [[None if v is None else str(v) for v in u] for u in raw]
    assert round(stats.alpha(units), 3) == 0.743


def test_alpha_is_undefined_when_every_label_is_the_same():
    assert stats.alpha([["TP", "TP"], ["TP", "TP"]]) is None
    assert stats.agreement([["TP", "TP"], ["TP", "FP"], ["TP", None]]) == (1, 2)


# Keys and determinism -----------------------------------------------------


def _f(**kw):
    base = {
        "pass": "static",
        "rule": "r",
        "severity": "medium",
        "category": "c",
        "file": "p/index.html",
        "line": 3,
        "excerpt": "x",
    }
    base.update(kw)
    return base


def test_keys_are_stable_and_count_repeats():
    rows = [_f(), _f(), _f(line=4)]
    a = [f["key"] for f in core.key_findings("p", rows)]
    b = [f["key"] for f in core.key_findings("p", list(reversed(rows)))]
    assert a == b
    assert len(set(a)) == 3 and a[0].endswith("#1") and a[1].endswith("#2")


def test_render_keys_ignore_measured_values():
    one = core.key_findings(
        "p", [_f(**{"pass": "render", "line": 0, "excerpt": "a.btn: hover reaches half at 178ms"})]
    )
    two = core.key_findings(
        "p", [_f(**{"pass": "render", "line": 0, "excerpt": "a.btn: hover reaches half at 96ms"})]
    )
    assert one[0]["key"] == two[0]["key"]


def _static_run(page_id: str):
    entry = next(p for p in manifest.load()["pages"] if p["id"] == page_id)
    html, own, bases = core._page_inputs(entry)
    return core._one(page_id, html, own, bases, render=False)


@pytest.mark.parametrize("page_id", ["a-gen-01", "a-gen-07", "d-bs-checkout-rtl", "d-uk-2"])
def test_same_page_and_engine_give_the_same_findings_twice(page_id):
    first, second = _static_run(page_id), _static_run(page_id)
    assert first["errors"] == [] and first["findings"]
    assert first == second


def test_seeded_run_is_deterministic():
    one = core.run(render=False, seeded=True)
    two = core.run(render=False, seeded=True)
    assert one["pages"] == two["pages"]


# Manifest and frozen pages ------------------------------------------------


def test_manifest_is_well_formed_and_every_page_matches_its_hash():
    data = manifest.load()
    assert manifest.problems(data) == []
    for p in data["pages"]:
        files = p["files"]
        rels = [files["html"], *files["own"], *files["vendor"]]
        if p["redistributable"]:
            assert capture.files_sha256(PAGES, rels) == p["sha256"], p["id"]


def test_manifest_problems_name_the_page_and_the_field():
    bad = {"pages": [{"id": "x", "origin": "robot", "split": "dev", "redistributable": "yes"}]}
    msgs = manifest.problems(bad)
    assert any("x: field licence is missing" in m for m in msgs)
    assert any("origin 'robot'" in m for m in msgs)
    assert any("redistributable must be true or false" in m for m in msgs)


def test_holdout_split_is_stratified_and_never_moves():
    data = {
        "pages": [{"id": f"a{i}", "origin": "ai-generated"} for i in range(10)]
        + [{"id": f"d{i}", "origin": "designer"} for i in range(10)]
    }
    manifest.assign_splits(data)
    for origin in ("ai-generated", "designer"):
        assert sum(p["split"] == "holdout" for p in data["pages"] if p["origin"] == origin) == 3
    before = {p["id"]: p["split"] for p in data["pages"]}
    data["pages"].append({"id": "a10", "origin": "ai-generated"})
    manifest.assign_splits(data)
    assert all(p["split"] == before[p["id"]] for p in data["pages"] if p["id"] in before)


def test_family_members_share_a_side_of_the_split():
    data = manifest.load()
    fam = manifest.families(data["pages"])
    sides = {}
    for p in data["pages"]:
        sides.setdefault(fam[p["id"]], set()).add(p["split"])
    split = {f: s for f, s in sides.items() if len(s) > 1}
    assert not split, f"families on both sides of the split: {sorted(split)}"
    assert fam["d-bs-album"] == fam["d-bs-album-rtl"]


def test_no_licence_excluded_crest_in_any_committed_page():
    found = []
    for page in sorted(PAGES.glob("*/index.html")):
        text = page.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"<svg\b[^>]*>", text, re.S):
            if re.search(r"govuk-footer__crown|govuk-header__logo|govuk-logo", m.group(0)):
                found.append(f"{page.parent.name}: {m.group(0)[:60]}")
    assert not found, f"OGL-excluded crest or logo still stored: {found}"


def test_no_committed_page_carries_a_script():
    found = [str(p.relative_to(PAGES)) for p in sorted(PAGES.rglob("*.html"))
             if re.search(r"<script\b", p.read_text(encoding="utf-8", errors="replace"), re.I)]
    assert not found, f"script elements in stored pages: {found}; strip them in capture.py"


def test_capture_strips_inline_and_external_scripts():
    html = ('<head><script async src="https://example.net/tag.js"></script>'
            '<script>window.dataLayer=[];</script><SCRIPT type="module" src="/a.js"/></head>'
            '<p>kept</p>')
    out, _files, _roles, notes = capture.freeze_html(html, "https://site.example.org/", {},
                                                     get=lambda u: b"")
    assert "<script" not in out.lower() and "<p>kept</p>" in out
    assert any("removed 3 script element" in n for n in notes)


def test_manifest_requires_attribution_and_keeps_closed_pages_out():
    bad = {"pages": [{"id": "a-gen-01", "origin": "designer", "licence": "x", "url": "u",
                      "capture_date": "d", "sha256": "s", "split": "dev",
                      "redistributable": False}]}
    msgs = manifest.problems(bad)
    assert any("field attribution is missing" in m for m in msgs)
    assert any("not redistributable but bench/pages/a-gen-01 exists" in m for m in msgs)


# Capture ------------------------------------------------------------------


def test_freeze_rewrites_stylesheets_and_drops_integrity():
    html = (
        '<link href="/a/app.css" rel="stylesheet" integrity="sha384-x" crossorigin="anonymous">'
        '<link rel="stylesheet" href="https://cdn.example.net/lib.min.css">'
        '<link rel="icon" href="/f.ico"><svg class="govuk-logo"><path/></svg>'
    )
    bodies = {
        "https://site.example.org/a/app.css": b"a{}",
        "https://cdn.example.net/lib.min.css": b"b{}",
    }
    out, _files, roles, notes = capture.freeze_html(
        html,
        "https://site.example.org/page",
        {"strip": [r"<svg[^>]*govuk-logo.*?</svg>"]},
        get=lambda u: bodies[u],
    )
    own, vendor = roles["own"][0], roles["vendor"][0]
    assert f'href="../_css/{own}"' in out and "integrity" not in out and "crossorigin" not in out
    assert own.endswith("-app.css") and vendor.endswith("-lib.min.css")
    assert 'href="/f.ico"' in out and "govuk-logo" not in out
    assert any("removed 1 match" in n for n in notes)


# Seeded set ---------------------------------------------------------------


def test_seeded_pages_match_the_spec():
    plants = json.loads((SEEDED / "plants.json").read_text(encoding="utf-8"))["pages"]
    expected = 1 + sum(
        2 + len(s.get("more", [])) + len(s.get("more_twins", [])) for s in seeded.SPEC
    )
    assert len(plants) == expected
    for row in plants:
        path = SEEDED / "pages" / row["file"]
        assert path.exists(), row["file"]
        assert path.read_text(encoding="utf-8") == seeded.page(row["id"], _parts(row)), row["id"]


def _parts(row):
    if row["kind"] == "base":
        return {}
    spec = next(s for s in seeded.SPEC if s["rule"] == row["rule"] and s["pass"] == row["pass"])
    kind, n = re.match(r".*\.(fault|twin)(\d+)$", row["id"]).groups()
    first = spec[kind]
    extra = spec.get("more" if kind == "fault" else "more_twins", [])
    return ([first] + list(extra))[int(n) - 1]


def test_recall_counts_found_faults_and_twin_fires():
    result = {
        "render": False,
        "pages": {
            "base": {"findings": []},
            "href-empty-hash.fault1": {"findings": [{"rule": "href-empty-hash"}]},
            "href-empty-hash.fault2": {"findings": []},
            "href-empty-hash.twin1": {"findings": [{"rule": "href-empty-hash"}]},
        },
    }
    r = seeded.recall(result)["href-empty-hash"]
    assert r["found"] == 1 and r["twin_fired"] == 1
    assert seeded.recall(result)["horizontal-overflow"]["skipped"] == "render pass did not run"


# Labels -------------------------------------------------------------------


def test_guide_labels_and_patterns_are_valid():
    guide = json.loads(label.GUIDE.read_text(encoding="utf-8"))
    for rule, crit in guide["rules"].items():
        for side in ("a", "b"):
            c = crit[side]
            assert c["default"] in label.VALUES, rule
            for ex in c.get("unless", []):
                re.compile(ex["match"])
                assert ex["label"] in label.VALUES, rule


def test_apply_takes_the_first_matching_exception():
    crit = {
        "default": "TP",
        "unless": [
            {"match": "focus-visible", "label": "FP"},
            {"match": "focus", "label": "cantTell"},
        ],
    }
    assert label._apply(crit, "a:focus-visible{}", "t")[0] == "FP"
    assert label._apply(crit, "a:focus{}", "t")[0] == "cantTell"
    assert label._apply(crit, "a{}", "t")[0] == "TP"
    with pytest.raises(label.LabelError, match="label 'yes' is not one of"):
        label._apply({"default": "yes"}, "x", "rule-x pass a")


def test_every_labelled_finding_is_marked_model_made():
    rows = label.load()
    assert rows, "bench/labels/labels.jsonl is empty; run python -m bench label"
    assert all(r["model_made"] is True for r in rows.values())


# Report, diff, sample, ablation ------------------------------------------


def _tiny_run(tmp_path):
    f = core.key_findings("a-gen-01", [_f(rule="href-empty-hash", file="a-gen-01/index.html")])
    run = {
        "engine": {"git": "x"},
        "render": False,
        "render_note": "off",
        "twice": True,
        "nondeterministic": [],
        "pages": {"a-gen-01": {"findings": f, "errors": []}},
    }
    path = tmp_path / "run.json"
    path.write_text(json.dumps(run))
    return run, path


def test_report_lists_every_rule_and_is_reproducible(tmp_path):
    run, path = _tiny_run(tmp_path)
    labels = tmp_path / "labels.jsonl"
    labels.write_text(
        json.dumps(
            {
                "key": run["pages"]["a-gen-01"]["findings"][0]["key"],
                "final": "TP",
                "pass_a": "TP",
                "pass_b": "TP",
                "model_made": True,
            }
        )
        + "\n"
    )
    one = report.build(path, tmp_path / "none.json", labels)
    two = report.build(path, tmp_path / "none.json", labels)
    assert one == two
    rules = report.all_rules()
    table = one.split("## Every rule", 1)[1]
    for rid in rules:
        assert f"| {rid} |" in table, rid
    assert "model-made" in one


def test_diff_counts_new_and_lost_per_rule():
    a = {
        "engine": {},
        "pages": {"p": {"findings": [{"key": "k1", "rule": "r1"}, {"key": "k2", "rule": "r2"}]}},
    }
    b = {
        "engine": {},
        "pages": {"p": {"findings": [{"key": "k2", "rule": "r2"}, {"key": "k3", "rule": "r1"}]}},
    }
    d = bdiff.compare(a, b)
    assert d["totals"] == {"base": 2, "head": 2, "new": 1, "lost": 1}
    assert d["rules"] == [{"rule": "r1", "new": 1, "lost": 1, "kept": 0}]


def test_sample_is_stratified_and_repeatable():
    labels = {
        f"k{i}": {"key": f"k{i}", "rule": f"r{i % 7}", "final": "TP", "page": "p"}
        for i in range(200)
    }
    one = sample.draw(labels, 50, 5)
    assert [r["key"] for r in one] == [r["key"] for r in sample.draw(labels, 50, 5)]
    assert len(one) == 50 and {r["rule"] for r in one[:7]} == {f"r{i}" for i in range(7)}
    with pytest.raises(ValueError, match="no labelled findings"):
        sample.draw({}, 50, 5)


def test_ablation_switches_off_prose_and_keeps_roles_and_checks():
    text = "# T\n\n## Summary\n\nLong prose.\n\n## Roles\n\n- `a.b`: x\n\n{arabic} ## Arabic type\n\nAr.\n"
    out = ablate.switch_off(text)
    assert "Long prose." not in out and "- `a.b`: x" in out and "{arabic} ## Arabic type" in out
    rows = ablate.run("motion")
    assert rows[0]["build_error"] == ""
    assert rows[0]["files_changed"] and all("/motion/" in f for f in rows[0]["files_changed"])
    with pytest.raises(ValueError, match="--pack 'nope' is not a guidance pack"):
        ablate.run("nope")


def test_render_pass_is_deterministic_on_a_seeded_page():
    if core.render_available():
        pytest.skip(core.render_available())
    page = SEEDED / "pages" / "text-low-contrast.fault1.html"
    runs = [core.render_findings(page, (SEEDED / "pages",)) for _ in range(2)]
    if runs[0][1]:
        pytest.skip(f"no browser for the render pass: {runs[0][1]}")
    keys = [[f["key"] for f in core.key_findings("p", rf)] for rf, _ in runs]
    assert keys[0] == keys[1]
    assert "text-low-contrast" in {f["rule"] for f in runs[0][0]}
