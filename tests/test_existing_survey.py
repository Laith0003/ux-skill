"""system detect on projects shaped like real ones: token files outside
the conventional folders, an action color not named primary, languages
set in templates, translucent colors, a face for figures, and two sources
that set one token to different values. Every project here is invented."""
from __future__ import annotations

import json
from pathlib import Path

from engine.existing import detect_existing_system

# Arabic words, written as escapes so the file stays ASCII.
ARABIC = "\u0645\u0631\u062d\u0628\u0627 \u0628\u0643 \u0641\u064a \u0645\u062d\u0641\u0638\u062a\u0643"


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _paths(found):
    return {s["path"]: s["kind"] for s in found["sources"]}


ROOT_TOKENS = (":root {\n  --ink: #1E2329;\n  --paper: #FFFFFF;\n  --action: #0F766E;\n"
               "  --space-2: 8px;\n}\n")


# ---------------------------------------------------------------- token files by content


def test_an_assets_folder_beside_the_system_is_read(tmp_path: Path) -> None:
    _write(tmp_path, "assets/brand/palette.json", json.dumps({"color": {
        "$type": "color", "brand": {"$value": "#0F766E"}, "ink": {"$value": "#1E2329"},
        "paper": {"$value": "#FFFFFF"}}}))
    found = detect_existing_system(tmp_path)
    assert found["found"] is True
    assert _paths(found)["assets/brand/palette.json"] == "tokens"
    assert found["declared"]["primary"] == "#0F766E"


def test_an_apps_own_token_stylesheet_is_read(tmp_path: Path) -> None:
    _write(tmp_path, "resources/css/wallet-tokens.css", ROOT_TOKENS)
    found = detect_existing_system(tmp_path)
    assert _paths(found)["resources/css/wallet-tokens.css"] == "css-foundation"
    assert found["declared"]["primary"] == "#0F766E"


def test_the_theme_block_of_a_main_stylesheet_is_read(tmp_path: Path) -> None:
    theme = "".join(f"  --color-tone-{i}: #1{i}2{i}3{i};\n" for i in range(6))
    rules = "".join(f".card-{i} {{ padding: 8px; margin: 0; color: red; }}\n" for i in range(8))
    _write(tmp_path, "resources/css/app.css",
           f"@import 'tailwindcss';\n@theme {{\n{theme}  --color-brand: #7C3AED;\n}}\n{rules}")
    found = detect_existing_system(tmp_path)
    assert _paths(found)["resources/css/app.css"] == "css-foundation"
    assert found["declared"]["primary"] == "#7C3AED"


def test_a_marketing_sites_globals_are_read(tmp_path: Path) -> None:
    _write(tmp_path, "apps/site/app/globals.css", ROOT_TOKENS)
    _write(tmp_path, "src/styles/brand.css", ":root { --brand: #7C3AED; --gap: 4px; "
                                              "--edge: #D0D5DD; }")
    paths = _paths(detect_existing_system(tmp_path))
    assert paths["apps/site/app/globals.css"] == "css-foundation"
    assert paths["src/styles/brand.css"] == "css-foundation"


def test_a_component_stylesheet_with_a_few_properties_is_not_a_system(tmp_path: Path) -> None:
    rules = "".join(f".row-{i} {{ padding: 8px; color: #333; }}\n" for i in range(10))
    _write(tmp_path, "src/components/table.css", f":root {{ --row: 40px; --gap: 4px; "
                                                  f"--edge: #EEE; }}\n{rules}")
    assert detect_existing_system(tmp_path)["found"] is False


def test_token_files_under_docs_examples_and_tests_are_not_the_system(tmp_path: Path) -> None:
    for folder in ("docs/theming", "examples/basic", "tests/fixtures"):
        _write(tmp_path, f"{folder}/tokens.css", ROOT_TOKENS)
    assert detect_existing_system(tmp_path)["found"] is False


# ---------------------------------------------------------------- the primary


def test_an_action_color_named_accent_is_the_primary(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --ink: #111111; --accent: #0F766E; "
                                          "--accent-hover: #115E59; --paper: #FFFFFF; }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert (declared["primary"], declared["primary_token"]) == ("#0F766E", "--accent")
    assert declared["primary_why"] == ("--accent is the only primary candidate; its name says "
                                       "accent, an action color.")


def test_a_brand_fill_name_is_a_primary_candidate(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --bg-brand: #7C3AED; --bg-page: #FFFFFF; "
                                          "--text-default: #111111; }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert (declared["primary"], declared["primary_token"]) == ("#7C3AED", "--bg-brand")


def test_the_color_buttons_and_links_use_wins_over_a_primary_name(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --primary: #1E2329; --accent: #0F766E; "
                                          "--paper: #FFFFFF; }\n"
                                          ".btn { background: var(--accent); }\n"
                                          "a:hover { color: var(--accent); }")
    _write(tmp_path, "resources/views/home.blade.php",
           '<button class="rounded bg-accent text-white">Save</button>\n'
           '<a class="text-accent" href="/next">Next</a>\n'
           '<h1 class="text-primary">Title</h1>\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert (declared["primary"], declared["primary_token"]) == ("#0F766E", "--accent")
    assert declared["primary_candidates"] == [
        {"token": "--primary", "value": "#1E2329", "paints": 0},
        {"token": "--accent", "value": "#0F766E", "paints": 4}]
    assert declared["primary_why"] == (
        "--accent is the color the code paints buttons and links with: 4 uses in button and "
        "link styles and markup, over --primary (0).")


def test_without_any_use_the_best_name_is_chosen_and_the_owner_is_asked(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --accent: #0F766E; --brand: #7C3AED; "
                                          "--paper: #FFFFFF; }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["primary_token"] == "--brand"
    assert declared["primary_why"] == (
        "--brand was chosen because its name says brand; the code paints no button or link "
        "with it or with --accent, so confirm it is the action color.")


# ---------------------------------------------------------------- languages


def test_a_blade_view_with_arabic_text_sets_the_language(tmp_path: Path) -> None:
    _write(tmp_path, "resources/css/tokens.css", ROOT_TOKENS)
    _write(tmp_path, "resources/views/layouts/app.blade.php",
           '<html lang="{{ app()->getLocale() }}" dir="rtl">\n<body>@yield("main")</body>\n')
    _write(tmp_path, "resources/views/home.blade.php", f"<main><h1>{ARABIC}</h1></main>\n")
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["languages"] == ["ar"]
    assert declared["direction"] == "rtl"


def test_jsx_vue_and_svelte_templates_set_the_language(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ROOT_TOKENS)
    _write(tmp_path, "app/layout.tsx", 'export default () => <html lang="ar" dir="rtl">'
                                       '<body /></html>\n')
    _write(tmp_path, "src/Hero.vue", f"<template><p>{ARABIC}</p></template>\n")
    _write(tmp_path, "src/Nav.svelte", '<html lang="en"><nav>Home</nav></html>\n')
    assert detect_existing_system(tmp_path)["declared"]["languages"] == ["ar", "en"]


def test_a_language_switcher_alone_does_not_make_a_page_arabic(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ROOT_TOKENS)
    _write(tmp_path, "src/Footer.jsx", '<a href="/ar">\u0639\u0631\u0628\u064a</a>\n')
    assert "languages" not in detect_existing_system(tmp_path)["declared"]


# ---------------------------------------------------------------- values


def test_rgba_keeps_its_alpha(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --accent: #0F766E; --scrim: rgba(17, 24, 39, "
                                          "0.5); --hairline: rgb(17 24 39 / 12%); }")
    colors = detect_existing_system(tmp_path)["declared"]["colors"]
    assert colors["scrim"] == "#11182780"
    assert colors["hairline"] == "#1118271F"


def test_a_translucent_color_is_never_the_primary(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --primary: rgba(15, 118, 110, 0.4); "
                                          "--accent: #0F766E; --paper: #FFFFFF; }")
    assert detect_existing_system(tmp_path)["declared"]["primary_token"] == "--accent"


def test_a_face_for_figures_is_reported(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ':root { --accent: #0F766E; --font-sans: "Inter Text", '
                                          'sans-serif; --font-numeric: "Grid Mono", monospace; }')
    fonts = detect_existing_system(tmp_path)["declared"]["fonts"]
    assert fonts == {"display": "Inter Text", "body": "Inter Text", "data": "Grid Mono"}


def test_a_face_set_on_table_cells_is_reported_with_where(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css",
           ':root { --accent: #0F766E; --font-body: "Inter Text", sans-serif; '
           '--font-alt: "Ledger Face", monospace; }\n'
           "td, .amount { font-family: var(--font-alt); }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["fonts"]["data"] == "Ledger Face"
    assert declared["data_font_from"] == "td, .amount in theme.css"


def test_a_face_a_table_class_names_is_reported(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css",
           ':root { --accent: #0F766E; --font-body: "Inter Text", sans-serif; '
           '--font-ledger: "Ledger Face", monospace; }')
    _write(tmp_path, "src/Report.tsx", '<table className="font-ledger w-full"></table>\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["fonts"]["data"] == "Ledger Face"
    assert declared["data_font_from"] == "font-ledger on <table> in Report.tsx"


def test_a_font_list_opening_with_platform_keywords_or_a_var_names_its_face(
        tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css",
           ":root { --accent: #0F766E; --font-display: var(--font-a), \"Rubik\", sans-serif; "
           "--font-sans: -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif; }")
    fonts = detect_existing_system(tmp_path)["declared"]["fonts"]
    assert fonts == {"display": "Rubik", "body": "system-ui"}


# ---------------------------------------------------------------- disagreements


def test_an_app_file_that_redeclares_a_token_after_importing_the_system_is_named(
        tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/tokens.css",
           ":root { --brand: #7C3AED; --ink: #111111; --space-2: 8px; }")
    _write(tmp_path, "resources/css/app.css",
           '@import "../../packages/tokens/tokens.css";\n'
           ":root { --brand: #0F766E; --paper: #FFFFFF; --edge: #D0D5DD; }")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["token"] == "--brand"
    assert entry["values"] == [
        {"path": "packages/tokens/tokens.css", "token": "--brand", "value": "#7C3AED"},
        {"path": "resources/css/app.css", "token": "--brand", "value": "#0F766E"}]
    assert entry["wins"] == "resources/css/app.css"
    assert entry["why"] == (
        "--brand is #7C3AED in packages/tokens/tokens.css and #0F766E in resources/css/app.css; "
        "resources/css/app.css wins: it imports packages/tokens/tokens.css and sets it again "
        "after, which silently undoes the value there; remove the second declaration, or change "
        "it in packages/tokens/tokens.css")


def test_two_unrelated_stylesheets_leave_the_winner_open(tmp_path: Path) -> None:
    _write(tmp_path, "styles/a-tokens.css", ":root { --brand: #7C3AED; --ink: #111; --gap: 4px }")
    _write(tmp_path, "styles/b-tokens.css", ":root { --brand: #0F766E; --ink: #111111; "
                                             "--gap: 4px }")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == ""
    assert entry["why"].endswith(
        "styles/a-tokens.css and styles/b-tokens.css set it with equal weight and neither loads "
        "the other, so the stylesheet the page loads last wins; keep one value, or import one "
        "file from the other so the order is written down")


def test_a_page_that_links_both_decides_the_winner(tmp_path: Path) -> None:
    _write(tmp_path, "styles/a-tokens.css", ":root { --brand: #7C3AED; --ink: #111; --gap: 4px }")
    _write(tmp_path, "styles/b-tokens.css", ":root { --brand: #0F766E; --ink: #111; --gap: 4px }")
    _write(tmp_path, "index.html", '<html lang="en"><head>'
                                   '<link rel="stylesheet" href="styles/b-tokens.css">'
                                   '<link rel="stylesheet" href="styles/a-tokens.css">'
                                   "</head></html>")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == "styles/a-tokens.css"
    assert "it loads after styles/b-tokens.css" in entry["why"]


def test_root_outranks_html_whatever_the_order(tmp_path: Path) -> None:
    _write(tmp_path, "styles/a-tokens.css", ":root { --brand: #7C3AED; --ink: #111; --gap: 4px }")
    _write(tmp_path, "styles/b-tokens.css", "html { --brand: #0F766E; --ink: #111; --gap: 4px }")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == "styles/a-tokens.css"
    assert "it sets it on :root, which outranks html in styles/b-tokens.css" in entry["why"]


def test_a_curated_palette_that_contradicts_the_tokens_is_named(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --color-primary: #0F766E; --ink: #111; "
                                          "--gap: 4px }")
    _write(tmp_path, "MASTER.md", "# Palette\n\n| Token | Value |\n|---|---|\n"
                                  "| `color.primary` | #7C3AED |\n")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["token"] == "--color-primary"
    assert entry["wins"] == "styles/theme.css"
    assert entry["why"] == (
        "--color-primary is #0F766E in styles/theme.css and #7C3AED in MASTER.md; "
        "styles/theme.css wins: it is the only stylesheet that sets it; the page shows its "
        "value; MASTER.md only describes the palette, so correct the document or the token")


def test_two_spellings_of_one_value_are_no_disagreement(tmp_path: Path) -> None:
    _write(tmp_path, "styles/a-tokens.css", ":root { --brand: #7c3aed; --ink: #111; --gap: 4px }")
    _write(tmp_path, "styles/b-tokens.css", ":root { --brand: rgb(124 58 237); --ink: #111111; "
                                             "--gap: 4px }")
    assert "disagreements" not in detect_existing_system(tmp_path)["declared"]
