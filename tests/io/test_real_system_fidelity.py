"""Reading a mature system shaped like a real one: several sources read
as the browser reads them, the root written twice, an RTL root. Every
system here is invented."""
from __future__ import annotations

import shutil
from pathlib import Path

from engine.io.adapter import propose
from engine.io.css_in import import_css
from engine.io.read import read_sources, read_system
from engine.io.report import Source

FIXTURE = Path(__file__).parent.parent / "fixtures" / "mature_system"


def _css(text: str, name: str = "site.css"):
    return import_css(text, Source(name, "css", "0" * 64, len(text)))


# ---------------------------------------------------------------- an RTL root


RTL_SITE = """:root {
  direction: rtl;
  --gap-start: 16px;
  --arrow: "\\2190";
}
[dir="ltr"] {
  --gap-start: 24px;
  --arrow: "\\2192";
}
"""


def test_a_root_that_reads_right_to_left_is_the_base():
    imported = _css(RTL_SITE)
    assert imported.tokens.axes["direction"] == ("rtl", "ltr")
    assert imported.tokens.get("gap-start").modes == {"direction:ltr": {"value": 24,
                                                                        "unit": "px"}}
    note = next(i for i in imported.report.notes if i.name == '[dir="ltr"]')
    assert "with rtl, what :root holds, as its base and ltr as its mode" in note.message


def test_an_rtl_based_axis_maps_each_value_to_itself():
    axis = propose(_css(RTL_SITE).tokens).axes["direction"]
    assert (axis.source, axis.values) == ("direction", {"ltr": "ltr", "rtl": "rtl"})


def test_a_root_with_no_direction_keeps_the_root_as_its_base():
    imported = _css(RTL_SITE.replace("  direction: rtl;\n", ""))
    assert imported.tokens.axes["direction"] == ("base", "ltr")


def test_pages_that_read_right_to_left_make_rtl_the_base(tmp_path):
    root = tmp_path / "site"
    (root / "styles").mkdir(parents=True)
    (root / "styles" / "tokens.css").write_text(
        ":root { --gap-start: 16px; --ink: #111111; --paper: #FFFFFF; }\n"
        '[dir="ltr"] { --gap-start: 24px; }\n', encoding="utf-8")
    (root / "index.html").write_text('<html lang="ar" dir="rtl"><body></body></html>',
                                     encoding="utf-8")
    imported = read_system(root)
    assert imported.tokens.axes["direction"] == ("rtl", "ltr")
    assert any("the root holds the rtl values" in i.message for i in imported.report.notes)


# ---------------------------------------------------------------- the dark stage


def test_a_sites_globals_with_a_doubled_root_bring_the_dark_stage(tmp_path):
    shutil.copytree(FIXTURE, tmp_path / "p")
    p = tmp_path / "p"
    imported = read_sources([p / "tokens" / "tokens.json", p / "site" / "app" / "globals.css"])
    assert imported.tokens.get("brand.canvas").modes == {"scheme:dark": "#0E1113"}
    # html:root outranks the token file's :root: the page shows the globals' value.
    assert imported.tokens.get("brand.primary").value == "#0A6B53"
    note = next(i for i in imported.report.notes if i.name == "--brand-primary")
    assert note.where == "globals.css:13"
    assert "on :root at tokens.json:9" in note.message
    assert not [i for i in imported.report.not_read if "doubled" in i.message]


# ---------------------------------------------------------------- the enhance report


def _enhanced(tmp_path, extra=None):
    import json

    from engine.io.commands import run_enhance
    shutil.copytree(FIXTURE, tmp_path / "p")
    p = tmp_path / "p"
    for rel, text in (extra or {}).items():
        (p / rel).write_text(text, encoding="utf-8")
    result = run_enhance([p, p / "site" / "app" / "globals.css"], scan=[p / "site"],
                         out=tmp_path / "out")
    return result, json.loads((tmp_path / "out" / "enhance.json").read_text())


def test_the_summary_counts_what_the_report_body_says(tmp_path):
    result, data = _enhanced(tmp_path, {
        "site/components/Badge.tsx":
            'export const Badge = () => <span className="text-surface">New</span>;\n',
        "site/components/Note.tsx":
            'export const Note = () => <p className="text-canvas" style={{color: "var(--x-ink)"}}>'
            "x</p>;\n"})
    summary, body = result["summary"], result["report"]
    named_for = [line for line in body.splitlines() if " is named for " in line]
    # brand.surface lies on every use; brand.canvas on some of them.
    assert summary["lies"] == len(named_for) == 2
    assert (summary["lies_every_use"], summary["strays"]) == (1, 1)
    assert summary["missing"] == 1 and summary["missing_uses"] == 1
    assert "references --x-ink, which the system does not have" in body
    assert summary["unused"] == len(data["drift"]["unused"])


def test_the_report_names_every_source_read_in_order(tmp_path):
    result, _ = _enhanced(tmp_path)
    head = result["report"].split("## How it was checked")[0]
    assert "Read together with it, in this order:" in head
    assert head.index("foundations.css") < head.index("globals.css")


def test_a_mature_system_is_measured_with_pairs_through_names_alone(tmp_path):
    result, data = _enhanced(tmp_path)
    gate = data["gate"]
    assert gate["measured"] and gate["pairs_checked"] > 0
    assert result["summary"]["gate_measured"] is True
    assert data["mapping"]["mapped"] >= 20


def test_an_on_color_is_never_offered_for_a_background_or_for_text(tmp_path):
    from engine.foundations.tokens import Token, TokenSet
    from engine.io.enhance import drift
    from engine.io.scan import scan
    ts = TokenSet({})
    for path in ("primary-foreground", "brand-fg", "on-primary", "text-on-brand"):
        ts.add(Token(path, "color", "#FFFFFF"))
    ts.add(Token("text-default", "color", "#FFFFFF"))
    (tmp_path / "hero.html").write_text(
        '<section style="background: #ffffff"><h1 style="color: #fff">Over the photo</h1>'
        "</section>", encoding="utf-8")
    d = drift(ts, scan([tmp_path], ts))
    offered = {tuple(r.tokens) for r in d.raw_with_token}
    # Only the text color named for text is offered, and only for the text.
    assert offered == {("text-default",)}
    [raw] = d.raw_with_token
    assert [u.prop for u in raw.uses] == ["color"]
