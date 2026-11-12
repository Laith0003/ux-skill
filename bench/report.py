"""Write bench/report.md: every rule with counts, precision, interval, recall
and the tier its labels support. ``python -m bench report``.

The report is generated; edit this file, never report.md. It carries no
timestamp, so the same run, labels and seeded run give the same bytes.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from bench import BENCH, OUT, REPORT, ROOT
from bench import core, label, manifest as mf, seeded, stats

TARGET = {"ai-generated": 50, "ai-found": 50, "designer": 100}
TARGET_TOTAL = 200
MIN_FOR_RATE = 3  # labelled findings a rule needs before it enters the false positive top list
# Engine problems the bench found that are not a rule's precision. Filed here
# until Phase 2 or 3 picks them up; lint rules are not changed in Phase 1.
FILED = [
    "Render timing is wall-clock: state-answers-late fires on a control near its threshold in "
    "one run and not the next. The determinism section lists the pages where it happened in "
    "this run; the finding keys ignore the measured value, so only an appearing or vanishing "
    "finding counts.",
    "Static excerpts show the first 200 characters of the line, not the match. On minified CSS "
    "and one-line HTML the excerpt never shows what fired (most of the excerpt-view cantTell "
    "labels, and most negative alphas, come from this). Phase 2's selector field fixes it.",
    "The stored pages carry no scripts and the render pass blocks the network, so no image or "
    "web font from another host loads; image-broken fires on every remote image and icon "
    "links can collapse. Phase 2's network blocking has to choose what counts as a finding "
    "then.",
    "placeholder-token-shipped matches lorem ipsum, so every lorem-ipsum-leak finding is "
    "counted twice.",
    "imagery-mandatory-missing fires on pages that are not landing pages (sign-in, settings, "
    "dashboards, blog, a plain content page) and on the seeded base page.",
    "Seeded misses: img with width but no height, a textarea named only by its placeholder, "
    "transition shorthand with no property (transition: 0.2s, which means all), and an SVG "
    "image stretched out of shape.",
]
# Rules whose findings on this corpus are an artifact of freezing it: images
# and photos are not stored, so every remote image fails to load at render.
CAPTURE_ARTIFACTS = {
    "image-broken": "images are not stored with the frozen pages, so every remote image is "
    "broken by construction",
    "photo-grade-off": "photos are not stored with the frozen pages",
}


def all_rules() -> Dict[str, Dict[str, str]]:
    data = json.loads((ROOT / "data" / "anti-patterns.json").read_text(encoding="utf-8"))
    out = {
        e["id"]: {"severity": e["severity"], "category": e["category"], "pass": "static"}
        for e in data["entries"]
    }
    try:
        from engine.render.core import _RULES

        for rid, r in _RULES.items():
            out.setdefault(
                rid, {"severity": r["severity"], "category": r["category"], "pass": "render"}
            )
    except Exception:  # render extra missing: static rules only
        pass
    return out


def _pct(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x:.2f}"


def corpus_section(manifest: Dict[str, Any]) -> List[str]:
    pages = manifest["pages"]
    rows = Counter((p["origin"], p["licence"]) for p in pages)
    out = [
        "## Corpus",
        "",
        "| Origin | Licence | Pages | Redistributable | Dev | Holdout | Right to left |",
        "|---|---|---|---|---|---|---|",
    ]
    for (origin, lic), n in sorted(rows.items()):
        sel = [p for p in pages if p["origin"] == origin and p["licence"] == lic]
        out.append(
            f"| {origin} | {lic} | {n} | {sum(p['redistributable'] for p in sel)} | "
            f"{sum(p['split'] == 'dev' for p in sel)} | "
            f"{sum(p['split'] == 'holdout' for p in sel)} | "
            f"{sum(p.get('direction') == 'rtl' for p in sel)} |"
        )
    n_gen = sum(p["origin"] == "ai-generated" for p in pages)
    if n_gen:
        out += ["", f"The {n_gen} ai-generated pages were made by one model (claude-opus-5-5) in "
                    "the session that built this bench, after it had read the ux-skill plan, "
                    "research and engine files. They are not a clean without-ux-skill set; one "
                    "tool and one run per brief, so they stand in for AI output, not for the "
                    "five-tool sample PLAN-5.0 asks for."]
    total = len(pages)
    redis = sum(p["redistributable"] for p in pages)
    out += [
        "",
        "Gap to the PLAN-5.0 target:",
        "",
        "| Origin | Target | Have | Gap |",
        "|---|---|---|---|",
    ]
    by_origin = Counter(p["origin"] for p in pages)
    for origin, target in TARGET.items():
        have = by_origin.get(origin, 0)
        out.append(f"| {origin} | {target} | {have} | {max(0, target - have)} |")
    out.append(f"| all | {TARGET_TOTAL} | {total} | {max(0, TARGET_TOTAL - total)} |")
    rtl = sum(p.get("direction") == "rtl" for p in pages)
    out += [
        "",
        f"Redistributable: {redis} of {total} "
        f"({100 * redis / max(total, 1):.0f} percent; target at least 60). "
        f"Right to left pages: {rtl} (target at least 15). "
        f"Split: {sum(p['split'] == 'dev' for p in pages)} dev, "
        f"{sum(p['split'] == 'holdout' for p in pages)} holdout "
        "(target 140 and 60).",
        "",
    ]
    return out


def _count(findings: List[Dict[str, Any]], labels: Dict[str, Dict[str, Any]]):
    """Per rule: findings fired, pages hit, label counts, label pairs, and the
    pages that hold a labelled TP or FP finding."""
    fired: Counter = Counter(f["rule"] for f in findings)
    pages_hit: Dict[str, set] = defaultdict(set)
    lab: Dict[str, Counter] = defaultdict(Counter)
    units: Dict[str, List[List[Optional[str]]]] = defaultdict(list)
    lab_pages: Dict[str, set] = defaultdict(set)
    for f in findings:
        page = f["key"].split("|")[0]
        pages_hit[f["rule"]].add(page)
        r = labels.get(f["key"])
        if not r or not r.get("final"):
            lab[f["rule"]]["unlabelled"] += 1
            continue
        lab[f["rule"]][r["final"]] += 1
        units[f["rule"]].append([r.get("pass_a"), r.get("pass_b")])
        if r["final"] in ("TP", "FP"):
            lab_pages[f["rule"]].add(page)
    return fired, pages_hit, lab, units, lab_pages


INDEPENDENCE = (
    "Labels are not independent per finding: both passes and every tiebreak were written "
    "by one model, several rules' context-view criteria restate the engine's own pattern, "
    "and rule-wide tiebreaks settle many rows at once. Tiers here are upper bounds."
)


def build(
    run_path: Optional[Path] = None,
    seeded_path: Optional[Path] = None,
    labels_path: Optional[Path] = None,
    ablation: Optional[List[Dict[str, Any]]] = None,
) -> str:
    run = core.load_run(run_path or OUT / "run.json")
    sp = seeded_path or OUT / "seeded.json"
    seeded_run = core.load_run(sp) if sp.exists() else None
    labels = label.load(labels_path) if labels_path else label.load()
    manifest = mf.load()
    rules = all_rules()
    findings = core.all_findings(run)

    split_of = {p["id"]: p["split"] for p in manifest["pages"]}
    dev = [f for f in findings if split_of.get(f["key"].split("|")[0]) == "dev"]
    hold = [f for f in findings if split_of.get(f["key"].split("|")[0]) == "holdout"]
    fired, pages_hit, lab, units, lab_pages = _count(dev, labels)
    recall = seeded.recall(seeded_run) if seeded_run else {}

    eng = run["engine"]
    out = [
        "# ux-bench report",
        "",
        "Generated by `python -m bench report`; do not edit by hand. Every label in this "
        "report is model-made: two passes and a tiebreak written by a model, not yet "
        "confirmed by a person (bench/sample.py draws the 50 findings to confirm). Read every "
        "precision below as provisional. " + INDEPENDENCE + " Precision, tiers and the rule "
        "table use the dev split only; the holdout split has its own section.",
        "",
        f"Engine: git {eng.get('git') or 'unknown'}, rules file sha256 "
        f"{eng.get('anti_patterns_sha256')}, Python {eng.get('python')}. Render pass: "
        f"{'on' if run.get('render') else 'off (' + run.get('render_note', '') + ')'}. "
        f"Seeded run: {'present' if seeded_run else 'missing'}"
        + (f", render {'on' if seeded_run.get('render') else 'off'}" if seeded_run else "")
        + ".",
        "",
    ]
    out += corpus_section(manifest)

    # Determinism and crashes.
    out += ["## Determinism", ""]
    if run.get("twice"):
        nd = run.get("nondeterministic", [])
        out.append(f"Every page was run twice. {len(nd)} page(s) gave different findings.")
        if nd:
            out += ["", "| Page | Only in run 1 | Only in run 2 |", "|---|---|---|"]
            for d in nd:
                r1 = sorted({k.split("|")[2] for k in d["only_first"]})
                r2 = sorted({k.split("|")[2] for k in d["only_second"]})
                out.append(
                    f"| {d['page']} | {', '.join(r1) or 'none'} | {', '.join(r2) or 'none'} |"
                )
            out += [
                "",
                "Filed: the render timing checks measure in wall-clock time, so a "
                "control near the threshold fires on one run and not the next. Finding "
                "keys use the element, not the measured value, so a moving number alone "
                "does not count as a difference; a finding that appears and disappears "
                "does.",
            ]
    else:
        out.append("This run was not repeated; run `python -m bench run --twice` to check.")
    out.append("")
    out += ["## Engine crashes and render failures", ""]
    errs = [(pid, e) for pid, p in sorted(run["pages"].items()) for e in p["errors"]]
    if not errs:
        out.append(
            "None on this corpus: the static linter and the render pass finished on every page."
        )
    else:
        out += ["| Page | Pass | Error | Status |", "|---|---|---|---|"]
        for pid, e in errs:
            out.append(f"| {pid} | {e['pass']} | {e['error'][:160].replace('|', '/')} | filed |")
    out.append("")

    out += ["## Filed from this run", ""] + [f"- {x}" for x in FILED] + [""]

    # Summary.
    tot = Counter()
    for c in lab.values():
        tot.update(c)
    n_lab = tot["TP"] + tot["FP"]
    lo, hi = stats.wilson(tot["TP"], n_lab)
    out += [
        "## Summary (dev split)",
        "",
        "| Findings | Labelled TP | Labelled FP | cantTell | Unlabelled | Micro precision | "
        "Wilson 95 |",
        "|---|---|---|---|---|---|---|",
        f"| {len(dev)} | {tot['TP']} | {tot['FP']} | {tot['cantTell']} | "
        f"{tot['unlabelled']} | {_pct(tot['TP'] / n_lab if n_lab else None)} | "
        f"{stats.fmt_interval(lo, hi) if n_lab else 'n/a'} |",
        "",
    ]
    tiers = Counter()
    for rid in rules:
        c = lab.get(rid, Counter())
        tiers[stats.tier(c["TP"], c["FP"], len(lab_pages.get(rid, ())))] += 1
    out += [
        "Tiers the labels support (labels not independent per finding, so these are upper "
        "bounds; no rule can be more than a blocking candidate until usefulness is labelled "
        f"and a person confirms the label sample, and a candidate needs labelled findings on at "
        f"least {stats.MIN_PAGES} pages), over all "
        + str(len(rules))
        + " rules: "
        + ", ".join(f"{k} {v}" for k, v in sorted(tiers.items()))
        + ". No rule's severity "
        "is changed by this report; a high or critical rule whose labels do not reach blocking "
        "candidate is listed as a demotion candidate for Phase 2.",
        "",
    ]

    # Top false positive rates.
    rated = []
    for rid, c in lab.items():
        n = c["TP"] + c["FP"]
        if n >= MIN_FOR_RATE:
            rated.append((c["FP"] / n, n, rid, c))
    rated.sort(key=lambda x: (-x[0], -x[3]["FP"], x[2]))
    out += [
        f"## Highest false positive rates, dev split (at least {MIN_FOR_RATE} labelled findings)",
        "",
        "| Rule | Severity now | TP | FP | Precision | Wilson 95 |",
        "|---|---|---|---|---|---|",
    ]
    for rate, n, rid, c in rated[:10]:
        lo, hi = stats.wilson(c["TP"], n)
        out.append(
            f"| {rid} | {rules.get(rid, {}).get('severity', '?')} | {c['TP']} | {c['FP']} "
            f"| {c['TP'] / n:.2f} | {stats.fmt_interval(lo, hi)} |"
        )
    out.append("")

    # Recall summary.
    if recall:
        planted = sum(r["planted"] for r in recall.values() if not r.get("skipped"))
        found = sum(r["found"] for r in recall.values() if not r.get("skipped"))
        twins = sum(r["twin_fired"] for r in recall.values() if not r.get("skipped"))
        n_tw = sum(r["twins"] for r in recall.values() if not r.get("skipped"))
        missed = sorted(
            f"{k} ({r['found']}/{r['planted']})"
            for k, r in recall.items()
            if not r.get("skipped") and r["found"] < r["planted"]
        )
        noisy = sorted(k for k, r in recall.items() if not r.get("skipped") and r["twin_fired"])
        lo, hi = stats.wilson(found, planted)
        out += [
            "## Recall on the seeded-defect set",
            "",
            f"{found} of {planted} planted faults found over "
            f"{sum(1 for r in recall.values() if not r.get('skipped'))} rules "
            f"({found / max(planted, 1):.2f}, Wilson 95 {stats.fmt_interval(lo, hi)}). "
            f"Near-miss twins: {twins} of {n_tw} drew the rule they imitate.",
            "",
            "Missed: " + (", ".join(missed) or "none") + ".",
            "",
            "Fired on a near-miss twin: " + (", ".join(noisy) or "none") + ".",
            "",
        ]
        skipped = sorted(k for k, r in recall.items() if r.get("skipped"))
        if skipped:
            out += ["Not run (render pass off for the seeded run): " + ", ".join(skipped) + ".", ""]
        base = seeded_run["pages"].get("base", {}).get("findings", []) if seeded_run else []
        if base:
            out += [
                "Rules that fire on the plain base page every seeded page shares: "
                + ", ".join(sorted({f["rule"] for f in base}))
                + ".",
                "",
            ]

    # Per-rule table.
    out += [
        "## Every rule",
        "",
        "Fired: findings on the corpus. Pages: corpus pages it fired on. Precision is TP "
        "over TP plus FP, cantTell left out. Tier: what the labels support, at most blocking "
        "candidate (precision at least 0.95, Wilson lower bound at least 0.90, labelled "
        f"findings on at least {stats.MIN_PAGES} pages); labels are not independent per "
        "finding, so read it as an upper bound. Alpha: "
        "Krippendorff's alpha between the two passes (pairs in brackets); n/a when every "
        "pair gave the same single value. Recall: planted faults found on the seeded set; "
        "twin: near-miss twins it fired on.",
        "",
        "| Rule | Severity now | Pass | Fired | Pages | TP | FP | cantTell | Precision | "
        "Wilson 95 | Tier (upper bound; labels not independent) | Alpha | Recall | Twin | Note |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    order = sorted(rules, key=lambda r: (-fired.get(r, 0), r))
    for rid in order:
        meta = rules[rid]
        c = lab.get(rid, Counter())
        n = c["TP"] + c["FP"]
        lo, hi = stats.wilson(c["TP"], n)
        t = stats.tier(c["TP"], c["FP"], len(lab_pages.get(rid, ())))
        a = stats.alpha(units.get(rid, []))
        pairs = len(units.get(rid, []))
        rc = recall.get(rid)
        if rc and rc.get("skipped"):
            rec, twin = "not run", ""
        elif rc:
            rec, twin = f"{rc['found']}/{rc['planted']}", f"{rc['twin_fired']}/{rc['twins']}"
        else:
            rec, twin = "", ""
        notes = []
        if rid in CAPTURE_ARTIFACTS and fired.get(rid):
            notes.append("capture artifact: " + CAPTURE_ARTIFACTS[rid])
        if meta["severity"] in ("critical", "high") and t != "blocking-candidate" and n:
            notes.append("demotion candidate")
        if c["unlabelled"]:
            notes.append(f"{c['unlabelled']} unlabelled")
        out.append(
            f"| {rid} | {meta['severity']} | {meta['pass']} | {fired.get(rid, 0)} | "
            f"{len(pages_hit.get(rid, ()))} | {c['TP']} | {c['FP']} | {c['cantTell']} | "
            f"{_pct(c['TP'] / n if n else None)} | "
            f"{stats.fmt_interval(lo, hi) if n else 'n/a'} | {t} | "
            f"{_pct(a)}{f' ({pairs})' if pairs else ''} | {rec} | {twin} | {'; '.join(notes)} |"
        )
    out.append("")

    h_fired, h_pages, h_lab, _u, _lp = _count(hold, labels)
    h_tot = Counter()
    for c in h_lab.values():
        h_tot.update(c)
    hn = h_tot["TP"] + h_tot["FP"]
    hlo, hhi = stats.wilson(h_tot["TP"], hn)
    out += [
        "## Holdout split",
        "",
        f"{len({f['key'].split('|')[0] for f in hold})} pages, {len(hold)} findings, "
        f"{h_tot['TP']} TP, {h_tot['FP']} FP, {h_tot['cantTell']} cantTell; micro precision "
        f"{_pct(h_tot['TP'] / hn if hn else None)} "
        f"({stats.fmt_interval(hlo, hhi) if hn else 'n/a'}). Rule authors tune on dev only; "
        "this split is read once per release. Its labels were written with the same criteria, "
        "so it checks that the dev numbers carry over, not the labelling.",
        "",
        "| Rule | Fired | Pages | TP | FP | cantTell | Precision | Wilson 95 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for rid in sorted(h_fired, key=lambda r: (-h_fired[r], r)):
        c = h_lab.get(rid, Counter())
        n = c["TP"] + c["FP"]
        lo, hi = stats.wilson(c["TP"], n)
        out.append(
            f"| {rid} | {h_fired[rid]} | {len(h_pages[rid])} | {c['TP']} | {c['FP']} | "
            f"{c['cantTell']} | {_pct(c['TP'] / n if n else None)} | "
            f"{stats.fmt_interval(lo, hi) if n else 'n/a'} |"
        )
    out.append("")

    if ablation:
        from bench import ablate

        out += [
            "## Ablation: guidance packs switched off",
            "",
            "Engine half only: the rule pack an agent reads, built with each guidance pack "
            "switched off (prose sections reduced to one line; Roles and Checks kept), "
            "compared file by file with the full build. The generation half, pages built "
            "from the ten briefs with and without each pack, needs an AI coding tool run "
            f"per brief and pack ({len(ablate.generation_plan(['b'] * 10, [r['pack'] for r in ablation]))} "
            "runs) and is not run here.",
            "",
            ablate.table(ablation),
            "",
        ]

    diff = OUT / "diff.json"
    if diff.exists():
        d = json.loads(diff.read_text(encoding="utf-8"))
        t = d["totals"]
        out += [
            "## Version diff",
            "",
            f"`python bench/diff.py` ({d['refs']['base']} against {d['refs']['head']}, render "
            f"{'on' if all(d.get('render', [])) else 'off'}): {t['base']} findings before, "
            f"{t['head']} after, {t['new']} new, {t['lost']} lost.",
            "",
            "| Rule | New | Lost | Kept |",
            "|---|---|---|---|",
        ]
        out += [f"| {r['rule']} | {r['new']} | {r['lost']} | {r['kept']} |" for r in d["rules"]]
        out.append("")

    out += [
        "## Not measured yet",
        "",
        "- Usefulness precision (would a designer change it) is not labelled; every "
        "precision above is detection precision.",
        "- Labels are model-made and the two passes were written by the same model with "
        "different evidence (excerpt against surrounding source), so alpha here measures how "
        "much context changes a reading, not agreement between independent people.",
        "- Recall on real pages (exhaustive annotation of a 60-page subsample by three "
        "raters) is not done; recall above is on planted faults only.",
        "- No found-in-the-wild AI pages and no non-redistributable pages yet; the larger "
        "pool of 1,000 to 2,000 pages for rules that fire rarely is not built.",
        "",
    ]
    return "\n".join(out)


__all__ = ["build", "all_rules", "REPORT", "BENCH"]
