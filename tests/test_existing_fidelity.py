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


# ---------------------------------------------------------------- through the Tailwind theme


PRESET = ("module.exports = {\n  theme: {\n    extend: {\n"
          "      colors: { cta: 'var(--color-brand)' },\n"
          "      fontFamily: { tabular: 'var(--type-family-alt)' },\n"
          "    },\n  },\n};\n")


def _themed(tmp_path: Path) -> Path:
    _write(tmp_path, "styles/tokens.css",
           ':root {\n  --color-primary: #0B5F4A;\n  --color-brand: #7C3AED;\n'
           '  --paper: #FFFFFF;\n  --type-family-display: "Newsreader", serif;\n'
           '  --type-family-body: "Inter", sans-serif;\n'
           '  --type-family-alt: "IBM Plex Mono", monospace;\n}\n')
    _write(tmp_path, "tailwind.config.js", "module.exports = { presets: [require('./preset')] }\n")
    _write(tmp_path, "preset.js", PRESET)
    return tmp_path


def test_a_utility_the_theme_maps_counts_as_a_button_paint(tmp_path: Path) -> None:
    _themed(tmp_path)
    _write(tmp_path, "src/Button.tsx",
           'export const Button = () => <button className="bg-cta px-4">Go</button>;\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["primary_token"] == "--color-brand"
    assert {c["token"]: c["paints"] for c in declared["primary_candidates"]} == {
        "--color-primary": 0, "--color-brand": 1}


def test_a_font_class_the_theme_maps_on_a_table_is_the_data_face(tmp_path: Path) -> None:
    _themed(tmp_path)
    _write(tmp_path, "src/Stats.tsx",
           'export const Stats = () => <table><td className="font-tabular">4</td></table>;\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["fonts"]["data"] == "IBM Plex Mono"
    assert declared["data_font_from"] == "font-tabular on <td> in Stats.tsx"


def test_a_mature_system_reports_its_data_face_languages_and_direction(tmp_path: Path) -> None:
    shutil.copytree(FIXTURE, tmp_path / "p")
    declared = detect_existing_system(tmp_path / "p")["declared"]
    assert declared["fonts"]["data"] == "IBM Plex Mono"
    assert declared["languages"] == ["ar", "en", "fr"]
    assert declared["direction"] == "rtl"
    [primary] = [d for d in declared["disagreements"] if d["token"] == "--brand-primary"]
    assert primary["wins"] == "site/app/globals.css"
    assert {v["path"]: v["line"] for v in primary["values"]} == {
        "styles/foundations.css": 8, "site/app/globals.css": 13, "tokens/tokens.json": 9,
        "DESIGN.md": 7}
