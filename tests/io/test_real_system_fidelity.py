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
    assert "at tokens.json:9 (:root)" in note.message
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


# ---------------------------------------------------------------- extend


def _pair_system(tmp_path):
    import json as _json
    (tmp_path / "tokens.json").write_text(_json.dumps({
        "brand": {"$type": "color", "primary": {"$value": "#0B5F4A"},
                  "canvas": {"$value": "#FBFAF7"}, "ink": {"$value": "#1B1F24"}}},
        indent=2), encoding="utf-8")
    (tmp_path / "site.css").write_text(":root {\n  --ring-color: #1F6FEB;\n}\n",
                                       encoding="utf-8")
    return read_sources([tmp_path / "tokens.json", tmp_path / "site.css"])


def test_imagery_is_generated_from_the_systems_own_primary(tmp_path):
    from engine.io.adapter import Mapping, RoleMap
    from engine.io.extend import extend
    imported = _pair_system(tmp_path)
    mapped = extend(imported, Mapping({"color.action.primary": RoleMap("brand.primary", "owner")}),
                    foundations=("imagery",))
    assert str(mapped.tokens.resolve("imagery.tint")).upper().startswith("#0B5F4A")
    # Not mapped, the primary the names say is read, and the report says so.
    named = extend(imported, Mapping(), foundations=("imagery",))
    assert str(named.tokens.resolve("imagery.tint")).upper().startswith("#0B5F4A")
    assert any("read from your brand.primary, whose name says it is the primary" in d
               for d in named.decisions)


def test_no_mode_axis_is_added_unless_asked(tmp_path):
    from engine.io.adapter import Mapping
    from engine.io.extend import extend
    imported = _pair_system(tmp_path)
    quiet = extend(imported, Mapping(), foundations=("imagery", "motion"))
    assert "contrast" not in quiet.tokens.axes and "motion" not in quiet.tokens.axes
    said = [d for d in quiet.decisions if d.startswith("Your system has no ")]
    assert said == [
        "Your system has no contrast mode, so the additions hold their values at contrast "
        "standard only and add no contrast axis; to add one, ask for it with --add-mode "
        "contrast.",
        "Your system has no motion mode, so the additions hold their values at motion "
        "standard only and add no motion axis; to add one, ask for it with --add-mode motion."]
    asked = extend(imported, Mapping(), foundations=("imagery",), modes=("contrast",))
    assert "contrast" in asked.tokens.axes


def test_an_unknown_mode_to_add_names_the_choices(tmp_path):
    import pytest

    from engine.foundations.errors import InputError
    from engine.io.adapter import Mapping
    from engine.io.extend import extend
    with pytest.raises(InputError) as exc:
        extend(_pair_system(tmp_path), Mapping(), foundations=("imagery",), modes=("dark",))
    assert str(exc.value) == ("--add-mode names dark, which is not a mode axis extend adds; use "
                              "contrast, motion or density")


def test_the_load_line_names_exactly_the_files_the_extension_points_at(tmp_path):
    from engine.io.adapter import Mapping
    from engine.io.extend import extend
    imported = _pair_system(tmp_path)
    one = extend(imported, Mapping(), roles={"color.focus.ring": "brand.primary"})
    assert one.load.startswith("Read tokens-ext.json with tokens.json: list tokens-ext.json "
                               "after it among the token files your tools read, since its "
                               "tokens point by name at tokens in tokens.json (brand.primary).")
    other = extend(imported, Mapping(), roles={"color.focus.ring": "ring-color"})
    assert other.load.startswith(
        "Read tokens-ext.json with site.css: list tokens-ext.json after it among the token "
        "files your tools read, since its tokens point by name at tokens in site.css "
        "(ring-color). A token it points at in a stylesheet resolves only where that "
        "stylesheet is read too.")


def test_the_result_says_where_each_file_went_and_why(tmp_path):
    from engine.io.commands import run_extend
    _pair_system(tmp_path)
    out = tmp_path / "out"
    result = run_extend([tmp_path / "tokens.json", tmp_path / "site.css"], out=out,
                        add=["imagery"])
    where = result["where"]
    assert where["beside"]["files"] == ["tokens-ext.json"]
    assert where["out"]["files"] == ["mapping.json", "extend-report.md"]
    assert where["out"]["why"] == (
        "--out holds the report and the mapping, with its own .uxskill folder: the record of "
        "the files ux-skill wrote there and a backup of the sources read")
    # The out folder holds exactly what the result says.
    assert sorted(p.name for p in out.iterdir()) == sorted(
        [*where["out"]["files"], where["out"]["intake"]])
    assert (f"tokens-ext.json went beside tokens.json in {tmp_path}, since an extension loads "
            "next to the file it extends") in result["message"]
    report = (out / "extend-report.md").read_text()
    assert "tokens-ext.json goes beside tokens.json, where an extension loads from" in report
    assert "go into the out folder, with its own .uxskill folder" in report


def test_a_utility_looks_in_its_own_namespace_before_colors(tmp_path):
    from engine.existing import survey
    from engine.foundations.tokens import Token, TokenSet
    from engine.io.scan import scan
    from engine.io.tailwind_config import read_theme
    (tmp_path / "tailwind.config.js").write_text(
        "module.exports = { theme: { extend: {\n"
        "  colors: { primary: 'var(--brand-primary)' },\n"
        "  textColor: { primary: 'var(--brand-text-primary)' },\n} } }\n", encoding="utf-8")
    page = tmp_path / "index.html"
    page.write_text('<button class="bg-primary">Go</button><a class="text-primary" href="/">'
                    "Home</a>", encoding="utf-8")
    ts = TokenSet({})
    ts.add(Token("brand.primary", "color", "#0B5F4A"))
    ts.add(Token("brand.text-primary", "color", "#1B1F24"))
    uses = {u.prop: u.value for u in scan([tmp_path], ts).usages}
    assert uses == {"bg-primary": "brand.primary", "text-primary": "brand.text-primary"}
    theme = read_theme([tmp_path])
    assert survey.button_paints(["--brand-primary", "--brand-text-primary"], [page], theme) \
        == {"--brand-primary": 1, "--brand-text-primary": 1}


def test_utilities_are_never_spellings_of_a_literal(tmp_path):
    from engine.foundations.tokens import TokenSet
    from engine.io.enhance import drift
    from engine.io.scan import scan
    (tmp_path / "tailwind.config.js").write_text("module.exports = {}\n", encoding="utf-8")
    (tmp_path / "a.html").write_text('<p class="bg-white text-white border-2">x</p>',
                                     encoding="utf-8")
    (tmp_path / "a.css").write_text(".x { color: #fff; border-width: 2px; }\n"
                                    ".y { color: #FFFFFF; }\n", encoding="utf-8")
    d = drift(TokenSet({}), scan([tmp_path], TokenSet({})))
    # Only the two literal texts of white are spellings; no utility is one.
    assert [(s.value, s.texts) for s in d.spellings] == [("#FFFFFF", ["#fff", "#FFFFFF"])]
