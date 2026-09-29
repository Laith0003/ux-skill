"""system detect on projects shaped like real ones: token files outside
the conventional folders, an action color not named primary, languages
set in templates, translucent colors, a face for figures, and two sources
that set one token to different values. Every project here is invented."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

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
    _write(tmp_path, "resources/css/app-tokens.css", ROOT_TOKENS)
    found = detect_existing_system(tmp_path)
    assert _paths(found)["resources/css/app-tokens.css"] == "css-foundation"
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


def test_an_action_color_named_accent_is_the_primary_when_nothing_says_primary(
        tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --ink: #111111; --accent: #0F766E; "
                                          "--accent-hover: #115E59; --paper: #FFFFFF; }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert (declared["primary"], declared["primary_token"]) == ("#0F766E", "--accent")
    assert declared["primary_why"] == (
        "--accent is the only primary candidate; its name says accent, an action color, and no "
        "color is named primary or brand.")


def test_a_brand_fill_name_is_a_primary_candidate(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --bg-brand: #7C3AED; --bg-page: #FFFFFF; "
                                          "--text-default: #111111; }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert (declared["primary"], declared["primary_token"]) == ("#7C3AED", "--bg-brand")


# A component library's shape: a dark primary, a near-white accent used
# only on hover, and button variants written in a cva call.
SHADCN_SHAPE = {
    "app/globals.css": (":root {\n  --background: #FFFFFF;\n  --foreground: #09090B;\n"
                        "  --primary: #18181B;\n  --primary-foreground: #FAFAFA;\n"
                        "  --accent: #F4F4F5;\n  --accent-foreground: #18181B;\n}\n"),
    "components/ui/button.tsx": (
        'const buttonVariants = cva("inline-flex items-center", {\n'
        '  variants: { variant: {\n'
        '    default: "bg-primary text-primary-foreground hover:bg-primary/90",\n'
        '    ghost: "hover:bg-accent hover:text-accent-foreground",\n'
        '    link: "text-primary underline-offset-4 hover:underline",\n'
        "  } },\n});\n"),
    "app/page.tsx": ('<Button className="hover:bg-accent">One</Button>\n'
                     '<Button className="hover:bg-accent focus:bg-accent">Two</Button>\n'
                     '<a className="text-primary" href="/more">More</a>\n'),
}


def test_a_primary_name_wins_over_a_hover_tint_named_accent(tmp_path: Path) -> None:
    for rel, text in SHADCN_SHAPE.items():
        _write(tmp_path, rel, text)
    declared = detect_existing_system(tmp_path)["declared"]
    assert (declared["primary"], declared["primary_token"]) == ("#18181B", "--primary")
    assert declared["primary_candidates"] == [
        {"token": "--primary", "value": "#18181B", "paints": 2},
        {"token": "--accent", "value": "#F4F4F5", "paints": 0}]
    assert declared["primary_why"] == (
        "--primary was chosen because its name says primary; --accent was left out: --accent "
        "(#F4F4F5) is a tint of the page, a hover or surface fill.")


def test_hover_and_focus_paints_are_not_counted(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --paper: #FFFFFF; --action: #0F766E; "
                                          "--cta: #7C3AED; }\n"
                                          ".btn:hover { background: var(--cta); }\n"
                                          ".btn { background: var(--action); }")
    _write(tmp_path, "src/Page.jsx", '<button className="bg-action hover:bg-cta '
                                     'focus-visible:bg-cta">Go</button>\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["primary_token"] == "--action"
    assert declared["primary_candidates"] == [
        {"token": "--action", "value": "#0F766E", "paints": 2},
        {"token": "--cta", "value": "#7C3AED", "paints": 0}]


def test_among_action_colors_the_one_buttons_are_filled_with_wins(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --paper: #FFFFFF; --accent: #0F766E; "
                                          "--interactive: #7C3AED; }")
    _write(tmp_path, "resources/views/home.blade.php",
           '<button class="rounded bg-interactive text-white">Save</button>\n'
           '<a class="text-interactive" href="/next">Next</a>\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["primary_token"] == "--interactive"
    assert declared["primary_why"] == (
        "--interactive is the color the code paints buttons and links with at rest: 2 uses in "
        "button and link styles and markup, over --accent (0).")


def test_without_any_use_the_best_action_name_is_chosen_and_the_owner_is_asked(
        tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --accent: #0F766E; --action: #7C3AED; "
                                          "--paper: #FFFFFF; }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["primary_token"] == "--accent"
    assert declared["primary_why"] == (
        "--accent was chosen because its name says accent, an action color, and no color is "
        "named primary or brand; the code paints no button or link with it or with --action at "
        "rest, so confirm it is the action color.")


@pytest.mark.parametrize("css", [
    "--primary: #F97316; --primary-foreground: #FFFFFF;",
    "--brand: #0EA5E9;",
    "--color-primary: #22C55E; --color-on-primary: #FFFFFF;",
    "--brand: #FACC15; --ink: #111111;",
    "--primary: #F4F4F5;",
], ids=["orange", "sky", "green", "yellow", "near-white"])
def test_a_color_named_primary_or_brand_is_read_whatever_its_contrast(
        tmp_path: Path, css: str) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --paper: #FFFFFF; --gap: 4px; %s }" % css)
    declared = detect_existing_system(tmp_path)["declared"]
    name, value = css.split(";")[0].split(": ")
    assert (declared["primary_token"], declared["primary"]) == (name.strip(), value.strip())
    assert "primary_note" not in declared


def test_a_light_action_color_carries_dark_text(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --paper: #FFFFFF; --gap: 4px; --accent: #FACC15; }")
    assert detect_existing_system(tmp_path)["declared"]["primary_token"] == "--accent"


def test_a_near_white_tint_as_the_only_action_color_is_not_declared(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ":root { --paper: #FFFFFF; --accent: #F4F4F5; "
                                          "--ink: #111111; }")
    declared = detect_existing_system(tmp_path)["declared"]
    assert "primary" not in declared
    assert declared["primary_note"] == (
        "no color is named primary or brand, and no action color can carry a button's text: "
        "--accent (#F4F4F5) is a tint of the page, a hover or surface fill; name the action "
        "color primary, or pass it as the brand primary by hand.")


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
        {"path": "packages/tokens/tokens.css", "line": 1, "token": "--brand", "value": "#7C3AED",
         "selector": ":root"},
        {"path": "resources/css/app.css", "line": 2, "token": "--brand", "value": "#0F766E",
         "selector": ":root"}]
    assert entry["wins"] == "resources/css/app.css"
    assert entry["why"] == (
        "--brand is #7C3AED in packages/tokens/tokens.css:1 and #0F766E in "
        "resources/css/app.css:2; resources/css/app.css:2 wins: it imports "
        "packages/tokens/tokens.css and sets it again after, which silently undoes the value at "
        "packages/tokens/tokens.css:1; remove the second declaration at resources/css/app.css:2, "
        "or change it at packages/tokens/tokens.css:1")


def test_two_unrelated_stylesheets_leave_the_winner_open(tmp_path: Path) -> None:
    _write(tmp_path, "styles/a-tokens.css", ":root { --brand: #7C3AED; --ink: #111; --gap: 4px }")
    _write(tmp_path, "styles/b-tokens.css", ":root { --brand: #0F766E; --ink: #111111; "
                                             "--gap: 4px }")
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == ""
    assert entry["why"].endswith(
        "styles/a-tokens.css:1 and styles/b-tokens.css:1 set it with equal weight and neither loads "
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
        "--color-primary is #0F766E in styles/theme.css:1 and #7C3AED in MASTER.md:5; "
        "styles/theme.css:1 wins: it is the only stylesheet that sets it; the page shows its "
        "value; MASTER.md:5 only describes the palette, so correct the document or the token")


def test_two_spellings_of_one_value_are_no_disagreement(tmp_path: Path) -> None:
    _write(tmp_path, "styles/a-tokens.css", ":root { --brand: #7c3aed; --ink: #111; --gap: 4px }")
    _write(tmp_path, "styles/b-tokens.css", ":root { --brand: rgb(124 58 237); --ink: #111111; "
                                             "--gap: 4px }")
    assert "disagreements" not in detect_existing_system(tmp_path)["declared"]


# ---------------------------------------------------------------- fix round: real shapes

SYSTEM_TOKENS = ":root {\n  --brand: #7C3AED;\n  --muted: #6B7280;\n  --space-2: 8px;\n}\n"
COMPONENTS = "".join(f".card-{i} {{ padding: 8px; border-radius: 4px; }}\n" for i in range(20))


def test_an_app_stylesheet_that_redeclares_among_component_rules_is_named(
        tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/tokens.css", SYSTEM_TOKENS)
    _write(tmp_path, "resources/css/app.css",
           '@import "../../packages/tokens/tokens.css";\n:root { --muted: #9CA3AF; }\n'
           + COMPONENTS)
    found = detect_existing_system(tmp_path)
    assert "resources/css/app.css" not in _paths(found)  # not a token file itself
    [entry] = found["declared"]["disagreements"]
    assert (entry["token"], entry["wins"]) == ("--muted", "resources/css/app.css")
    assert "it imports packages/tokens/tokens.css and sets it again after" in entry["why"]


def test_a_theme_block_redeclared_by_the_app_is_named_with_its_theme(tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/tokens.css",
           SYSTEM_TOKENS + '[data-theme="dark"] {\n  --muted: #9CA3AF;\n}\n')
    _write(tmp_path, "src/app.css", '@import "../packages/tokens/tokens.css";\n'
                                    "[data-theme=dark] { --muted: #A1A1AA; }\n" + COMPONENTS)
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert (entry["token"], entry["theme"], entry["wins"]) == (
        "--muted", "[data-theme=dark]", "src/app.css")
    assert entry["why"].startswith("--muted under [data-theme=dark] is #9CA3AF in "
                                   "packages/tokens/tokens.css:7 and #A1A1AA in src/app.css:2; ")


def test_a_package_name_import_resolves_through_the_workspace(tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/package.json", json.dumps({"name": "@lantern/tokens"}))
    _write(tmp_path, "packages/tokens/tokens.css", SYSTEM_TOKENS)
    _write(tmp_path, "apps/web/app/globals.css",
           '@import "@lantern/tokens/tokens.css";\n:root { --brand: #0F766E; }\n' + COMPONENTS)
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == "apps/web/app/globals.css"
    assert "it imports packages/tokens/tokens.css" in entry["why"]


def test_a_package_import_that_cannot_be_resolved_is_said_so(tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/tokens.css", SYSTEM_TOKENS)
    _write(tmp_path, "apps/web/app/globals.css",
           '@import "@lantern/tokens/tokens.css";\n:root { --brand: #0F766E; }\n' + COMPONENTS)
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == ""
    assert "neither loads the other" not in entry["why"]
    assert entry["why"].endswith(
        "apps/web/app/globals.css imports @lantern/tokens/tokens.css, which could not be "
        "resolved here, so which one the page loads last is not known; keep one value")


def test_an_unlayered_system_beats_an_override_inside_a_layer(tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/tokens.css", SYSTEM_TOKENS)
    _write(tmp_path, "src/app.css", '@import "../packages/tokens/tokens.css";\n'
                                    "@layer base {\n  :root { --muted: #9CA3AF; }\n}\n"
                                    + COMPONENTS)
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == "packages/tokens/tokens.css"
    assert ("it is set outside any cascade layer, which beats the value inside a layer in "
            "src/app.css:3 whatever the order") in entry["why"]


def test_a_widget_stylesheet_alone_is_not_a_system(tmp_path: Path) -> None:
    _write(tmp_path, "resources/css/datepicker.css",
           ".dp { --dp-bg: #FFFFFF; --dp-text: #222222; --dp-accent: #E11D48; --dp-radius: 6px; }")
    _write(tmp_path, "src/button.css",
           ".btn { --btn-bg: #0F766E; --btn-fg: #FFFFFF; --btn-pad: 8px; }")
    assert detect_existing_system(tmp_path)["found"] is False


def test_a_theme_named_class_still_counts(tmp_path: Path) -> None:
    _write(tmp_path, "src/themes.css", ".theme-harbor { --accent: #0F766E; --ink: #111111; "
                                       "--paper: #FFFFFF; }\n.dark { --ink: #F4F4F5; }")
    assert _paths(detect_existing_system(tmp_path))["src/themes.css"] == "css-foundation"


def test_images_never_starve_the_walk(tmp_path: Path, monkeypatch) -> None:
    from engine.existing import detect
    monkeypatch.setattr(detect, "_MAX_FILES", 5)
    for i in range(12):
        _write(tmp_path, f"public/img/photo-{i:02d}.png", "")
    _write(tmp_path, "resources/css/app-tokens.css", ROOT_TOKENS)
    assert detect_existing_system(tmp_path)["found"] is True


def test_a_sass_stylesheet_with_a_root_block_is_read(tmp_path: Path) -> None:
    _write(tmp_path, "resources/sass/app.scss", "$gap: 4px;\n" + ROOT_TOKENS)
    assert _paths(detect_existing_system(tmp_path))["resources/sass/app.scss"] == \
        "css-foundation"


def test_a_language_switcher_does_not_set_the_direction(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ROOT_TOKENS)
    _write(tmp_path, "src/pages/index.astro",
           '<html lang="en"><a lang="ar" dir="rtl" href="/ar">\u0639\u0631\u0628\u064a</a></html>\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["languages"] == ["en"] and "direction" not in declared


def test_locale_files_and_a_dynamic_dir_set_the_language(tmp_path: Path) -> None:
    _write(tmp_path, "styles/theme.css", ROOT_TOKENS)
    _write(tmp_path, "messages/ar.json", json.dumps({"hello": ARABIC}))
    _write(tmp_path, "messages/en.json", json.dumps({"hello": "Hello"}))
    _write(tmp_path, "app/[locale]/layout.tsx",
           'export default ({ locale }) => <html lang={locale} '
           'dir={locale === "ar" ? "rtl" : "ltr"}></html>\n')
    declared = detect_existing_system(tmp_path)["declared"]
    assert declared["languages"] == ["ar", "en"]
    assert declared["direction"] == "rtl"


def test_a_theme_named_widget_is_not_a_system(tmp_path: Path) -> None:
    _write(tmp_path, "src/toggle.css",
           ".theme-toggle { --t-bg: #FFFFFF; --t-fg: #111111; --t-knob: #0F766E; }\n"
           ".dark-switch { --s-bg: #111111; --s-fg: #FFFFFF; --s-gap: 4px; }\n")
    _write(tmp_path, "src/widget.css",
           "[data-mode=compact] { --w-gap: 4px; --w-pad: 8px; --w-edge: #D0D5DD; }\n")
    assert detect_existing_system(tmp_path)["found"] is False


def test_an_import_that_resolves_outside_the_compared_files_is_named(tmp_path: Path) -> None:
    _write(tmp_path, "packages/tokens/tokens.css", SYSTEM_TOKENS)
    _write(tmp_path, "node_modules/@lantern/tokens/tokens.css", SYSTEM_TOKENS)
    _write(tmp_path, "apps/web/app/globals.css",
           '@import "@lantern/tokens/tokens.css";\n:root { --brand: #0F766E; }\n' + COMPONENTS)
    [entry] = detect_existing_system(tmp_path)["declared"]["disagreements"]
    assert entry["wins"] == ""
    assert ("apps/web/app/globals.css imports @lantern/tokens/tokens.css, which resolves to "
            "node_modules/@lantern/tokens/tokens.css, not to either of these files") in entry["why"]
