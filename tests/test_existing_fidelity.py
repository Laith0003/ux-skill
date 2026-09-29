"""system detect on a mature system shaped like a real one: a token file,
foundation stylesheets, a site's globals holding the dark stage with the
root written twice, a Tailwind 3 preset that maps names to custom
properties, and an RTL site. Every project here is invented."""
from __future__ import annotations

import shutil
from pathlib import Path

from engine.existing import detect_existing_system

FIXTURE = Path(__file__).parent / "fixtures" / "mature_system"


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _paths(found):
    return {s["path"]: s["kind"] for s in found["sources"]}


# ---------------------------------------------------------------- the root written twice


def test_a_doubled_root_is_the_root_never_a_component(tmp_path: Path) -> None:
    _write(tmp_path, "styles/tokens.css", ":root { --brand: #7C3AED; --ink: #111111; "
                                          "--gap: 4px }")
    _write(tmp_path, "app/globals.css",
           ':root:root[data-theme="dark"] {\n  --ink: #EEEEEE;\n  --brand: #A78BFA;\n'
           "  --gap: 4px;\n}\n.hero { color: red; }\n")
    found = detect_existing_system(tmp_path)
    assert _paths(found)["app/globals.css"] == "css-foundation"


def test_the_more_specific_root_wins_and_both_lines_are_named(tmp_path: Path) -> None:
    _write(tmp_path, "styles/tokens.css", ":root {\n  --brand: #7C3AED;\n  --ink: #111111;\n"
                                          "  --gap: 4px;\n}\n")
    _write(tmp_path, "app/globals.css", "html:root {\n  --brand: #0F766E;\n}\n"
                                        ":root { --ink: #111111; --gap: 4px; --edge: #DDD }\n")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == "app/globals.css"
    assert entry["values"][1]["selector"] == "html:root"
    assert "app/globals.css:2 wins" in entry["why"]
    assert ("it sets it on html:root, which outranks :root in styles/tokens.css:2 whatever "
            "the order") in entry["why"]


def test_a_doubled_root_outranks_a_later_file(tmp_path: Path) -> None:
    _write(tmp_path, "styles/a-tokens.css", ":root:root { --brand: #7C3AED; --ink: #111; "
                                            "--gap: 4px }")
    _write(tmp_path, "styles/b-tokens.css", ":root { --brand: #0F766E; --ink: #111; "
                                            "--gap: 4px }")
    _write(tmp_path, "index.html", '<html lang="en"><head>'
                                   '<link rel="stylesheet" href="styles/a-tokens.css">'
                                   '<link rel="stylesheet" href="styles/b-tokens.css">'
                                   "</head></html>")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == "styles/a-tokens.css"


def test_a_token_file_that_agrees_with_the_page_is_not_named(tmp_path: Path) -> None:
    _write(tmp_path, "tokens/tokens.json",
           '{"brand": {"$type": "color", "primary": {"$value": "#0B5F4A"}, '
           '"ink": {"$value": "#111111"}, "paper": {"$value": "#FFFFFF"}}}')
    _write(tmp_path, "styles/foundations.css", ":root { --brand-primary: #0B5F4A; "
                                               "--brand-ink: #111111; --gap: 4px }")
    _write(tmp_path, "DESIGN.md", "# Palette\n\n| Token | Value |\n|---|---|\n"
                                  "| `brand.primary` | #0C6150 |\n")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert "tokens/tokens.json" not in entry["why"].split("; ", 1)[1]
    assert "DESIGN.md:5 only describes the palette" in entry["why"]


# ---------------------------------------------------------------- the dark scheme


def test_the_dark_stage_in_a_sites_globals_is_reported(tmp_path: Path) -> None:
    shutil.copytree(FIXTURE, tmp_path / "p")
    declared = detect_existing_system(tmp_path / "p")["declared"]
    assert declared["dark"] == [{"path": "site/app/globals.css", "line": 5,
                                 "selector": ':root:root[data-theme="dark"]',
                                 "properties": 4}]


def test_a_dark_scheme_under_the_media_query_is_reported(tmp_path: Path) -> None:
    _write(tmp_path, "styles/tokens.css",
           ":root { --ink: #111; --paper: #fff; --gap: 4px }\n"
           "@media (prefers-color-scheme: dark) {\n  :root { --ink: #eee; --paper: #111 }\n}\n")
    [dark] = detect_existing_system(tmp_path)["declared"]["dark"]
    assert dark["selector"] == "@media (prefers-color-scheme: dark) :root"
    assert (dark["line"], dark["properties"]) == (3, 2)


def test_a_system_with_no_dark_values_reports_none(tmp_path: Path) -> None:
    _write(tmp_path, "styles/tokens.css", ":root { --ink: #111; --paper: #fff; --gap: 4px }")
    assert "dark" not in detect_existing_system(tmp_path)["declared"]
