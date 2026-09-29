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
