"""The scanner reads classes through the project's own Tailwind theme: a
Tailwind 3 config and its presets, read as text and never run, and a
Tailwind 4 @theme block. Classes keep their breakpoint and state
prefixes as context, their sign and their opacity; a class the project's
CSS defines is its own. Every project here is invented."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from engine.foundations.tokens import Token, TokenSet
from engine.io.commands import run_enhance
from engine.io.scan import scan
from engine.io.tailwind_config import read_theme

FIXTURE = Path(__file__).parent.parent / "fixtures" / "mature_system"


def _ts() -> TokenSet:
    ts = TokenSet({})
    for path, value in (("brand.canvas", "#FBFAF7"), ("brand.surface", "#FFFFFF"),
                        ("brand.primary", "#0B5F4A"), ("brand.on-primary", "#FFFFFF"),
                        ("brand.text-primary", "#1B1F24")):
        ts.add(Token(path, "color", value))
    ts.add(Token("radius.medium", "dimension", {"value": 8, "unit": "px"}))
    return ts


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------- the config, read as text


def test_a_preset_mapping_names_to_custom_properties_is_read_without_running_it():
    theme = read_theme([FIXTURE / "site"])
    assert theme.files == ["../tailwind.config.js", "../tokens/tailwind-preset.js"]
    assert theme.get("colors", "primary").var == "brand-primary"
    assert theme.get("colors", "primary-foreground").var == "brand-on-primary"
    assert theme.get("colors", "ink-muted").var == "brand-text-secondary"
    assert theme.get("fontFamily", "display").var == "type-family-display"
    assert theme.get("maxWidth", "prose").value == "68ch"
    [(file, line, text, why)] = theme.not_read
    assert (file, line, text) == ("../tokens/tailwind-preset.js", 20, "gutter(4)")
    assert why.startswith("is computed in JavaScript, so its value is not read")


def test_theme_replaces_a_presets_namespace_and_extend_adds_to_it(tmp_path):
    _write(tmp_path, "preset.js", "module.exports = { theme: { colors: { ink: '#111111' }, "
                                  "extend: { spacing: { gutter: '24px' } } } }\n")
    _write(tmp_path, "tailwind.config.ts",
           "import preset from './preset'\n"
           "export default {\n  presets: [preset],\n"
           "  theme: {\n    colors: { paper: 'var(--paper)' },\n"
           "    extend: { spacing: { rail: '8px' } },\n  },\n} satisfies Config\n")
    theme = read_theme([tmp_path])
    assert theme.get("colors", "ink") is None
    assert theme.get("colors", "paper").var == "paper"
    assert {n for (ns, n) in theme.entries if ns == "spacing"} == {"gutter", "rail"}


def test_spreads_package_presets_and_computed_keys_are_listed_not_guessed(tmp_path):
    _write(tmp_path, "tailwind.config.js",
           "const colors = require('tailwindcss/colors')\n"
           "module.exports = {\n  presets: [require('@acme/ui-preset')],\n"
           "  theme: { extend: {\n    colors: { ...colors, [key]: '#fff', brand: colors.blue },\n"
           "  } },\n}\n")
    theme = read_theme([tmp_path])
    texts = [t for _, _, t, _ in theme.not_read]
    assert texts == ["preset @acme/ui-preset", "...colors", "[key]: '#fff'", "colors.blue"]
    assert theme.entries == {}


def test_a_v4_theme_block_in_a_stylesheet_reaches_the_token(tmp_path):
    _write(tmp_path, "app.css", "@import 'tailwindcss';\n@theme {\n"
                                "  --color-canvas: var(--brand-canvas);\n}\n")
    _write(tmp_path, "page.html", '<main class="bg-canvas">x</main>')
    found = scan([tmp_path], _ts())
    [use] = [u for u in found.usages if u.prop == "bg-canvas"]
    assert (use.kind, use.value) == ("token", "brand.canvas")


# ---------------------------------------------------------------- classes through the theme


def test_utilities_the_preset_names_reach_their_tokens(tmp_path):
    shutil.copytree(FIXTURE, tmp_path / "p")
    found = scan([tmp_path / "p" / "site"], _ts())
    tokens = {(u.prop, u.value) for u in found.usages if u.kind == "token"}
    assert ("bg-primary", "brand.primary") in tokens
    assert ("text-primary-foreground", "brand.on-primary") in tokens
    assert ("bg-canvas", "brand.canvas") in tokens
    assert ("rounded-card", "radius.medium") in tokens
    assert not {u.cls for u in found.unknown_classes} & {"bg-primary", "bg-canvas",
                                                        "rounded-card", "text-ink"}


def test_prefixes_are_context_never_another_spelling(tmp_path):
    _write(tmp_path, "tailwind.config.js", "module.exports = {}\n")
    _write(tmp_path, "a.html", '<p class="md:z-10 z-10 hover:z-10">x</p>')
    found = scan([tmp_path], TokenSet({}))
    uses = [u for u in found.usages if u.family == "z"]
    assert {u.text for u in uses} == {"z-10"}
    assert sorted(u.state for u in uses) == ["", "", "hover"]


def test_a_negative_class_keeps_its_sign(tmp_path):
    _write(tmp_path, "tailwind.config.js", "module.exports = {}\n")
    _write(tmp_path, "a.html", '<p class="-z-10">x</p><p class="z-10">y</p>')
    found = scan([tmp_path], TokenSet({}))
    assert sorted(u.value for u in found.usages if u.family == "z") == ["-10", "10"]


def test_an_opacity_modifier_is_part_of_the_color(tmp_path):
    _write(tmp_path, "tailwind.config.js", "module.exports = {}\n")
    _write(tmp_path, "a.html", '<p class="bg-white/80 text-white bg-black/[0.5]">x</p>')
    found = scan([tmp_path], TokenSet({}))
    assert [u.value for u in found.usages if u.family == "color"] == [
        "#FFFFFFCC", "#FFFFFF", "#00000080"]


def test_a_class_the_projects_css_defines_is_not_a_missing_token(tmp_path):
    _write(tmp_path, "tailwind.config.js", "module.exports = {}\n")
    _write(tmp_path, "site.css", ".bg-navy-deep { background-color: #0A1A2F; }\n")
    _write(tmp_path, "a.html", '<section class="bg-navy-deep bg-ocean">x</section>')
    found = scan([tmp_path], TokenSet({}))
    assert [u.cls for u in found.unknown_classes] == ["bg-ocean"]


# ---------------------------------------------------------------- a stylesheet passed as a source


def test_a_source_stylesheets_own_rules_count_as_uses(tmp_path):
    shutil.copytree(FIXTURE, tmp_path / "p")
    p = tmp_path / "p"
    run_enhance([p / "tokens" / "tokens.json", p / "styles" / "foundations.css"],
                scan=[p / "site"], out=tmp_path / "out")
    drift = json.loads((tmp_path / "out" / "enhance.json").read_text())["drift"]
    # body paints the canvas, the text and the body face; .card reaches
    # brand.surface through surface-raised, and the hairline directly.
    for used in ("brand.canvas", "brand.surface", "brand.hairline", "type.family-body",
                 "surface-raised"):
        assert used not in drift["unused"]
    # Its definitions are not uses: status.danger is defined there and
    # used nowhere.
    assert "status.danger" in drift["unused"]


def test_lines_inside_a_config_wrapper_are_the_files_own(tmp_path):
    _write(tmp_path, "tailwind.config.ts",
           "import { defineConfig } from 'x'\n\nexport default defineConfig({\n"
           "  theme: {\n    extend: {\n      colors: {\n        ink: 'var(--ink)',\n"
           "      },\n      spacing: { rail: makeScale() },\n    },\n  },\n})\n")
    theme = read_theme([tmp_path])
    assert theme.get("colors", "ink").line == 7
    assert [(line, text) for _, line, text, _ in theme.not_read] == [(9, "makeScale()")]


def _preset_project(tmp_path, where):
    preset = ("module.exports = {\n  theme: {\n"
              + ("    extend: {\n      spacing: { gutter: 'var(--space-gutter)' },\n    },\n"
                 if where == "extend" else "    spacing: { gutter: 'var(--space-gutter)' },\n")
              + "  },\n};\n")
    _write(tmp_path, "design/preset.js", preset)
    _write(tmp_path, "tailwind.config.js", "module.exports = {\n"
                                           "  presets: [require('./design/preset')],\n};\n")
    _write(tmp_path, "src/page.html",
           '<main class="px-6 inset-0 -mt-1.5 p-px md:gap-4 px-gutter">x</main>')
    ts = TokenSet({})
    ts.add(Token("space.gutter", "dimension", {"value": 20, "unit": "px"}))
    return scan([tmp_path / "src"], ts)


def test_tailwinds_default_spacing_steps_are_raw_values_when_a_preset_extends_them(tmp_path):
    found = _preset_project(tmp_path, "extend")
    assert found.unknown_classes == []
    used = {(u.prop, u.kind, u.value) for u in found.usages}
    assert {("px-6", "raw", "24px"), ("inset-0", "raw", "0px"), ("-mt-1.5", "raw", "-6px"),
            ("p-px", "raw", "1px"), ("gap-4", "raw", "16px"),
            ("px-gutter", "token", "space.gutter")} <= used
    assert all(u.family == "space" for u in found.usages)


def test_a_theme_not_read_in_full_keeps_no_default_step(tmp_path):
    # A preset from a package, or a spread, may replace the scale: no guess.
    ts = TokenSet({})
    for case, config in (
            ("package", "module.exports = {\n  presets: [require('some-preset')],\n"
                        "  theme: { extend: { spacing: { rail: '2px' } } },\n};\n"),
            ("spread", "const base = require('./base');\nmodule.exports = {\n"
                       "  theme: { ...base, extend: { spacing: { rail: '2px' } } },\n};\n")):
        root = tmp_path / case
        _write(root, "tailwind.config.js", config)
        _write(root, "src/page.html", '<main class="md:flex px-6">x</main>')
        found = scan([root / "src"], ts)
        assert [u.cls for u in found.unknown_classes] == ["px-6"], case
        assert not read_theme([root / "src"]).keeps("spacing")


def test_a_v4_spacing_base_sets_each_step(tmp_path):
    _write(tmp_path, "app.css", "@import 'tailwindcss';\n@theme {\n  --spacing: 2px;\n"
                                "  --color-ink: #111111;\n}\n")
    _write(tmp_path, "page.html", '<main class="px-6 p-px">x</main>')
    used = {(u.prop, u.kind, u.value) for u in scan([tmp_path], TokenSet({})).usages}
    assert {("px-6", "raw", "12px"), ("p-px", "raw", "1px")} <= used
    # A base this reader cannot read as a length gives no px value; it says why.
    _write(tmp_path, "app.css", "@import 'tailwindcss';\n@theme {\n"
                                "  --spacing: var(--unit);\n  --color-ink: #111111;\n}\n")
    found = scan([tmp_path], TokenSet({}))
    assert not [u for u in found.usages if u.prop == "px-6"]
    [missed] = [n for n in found.not_read if n.text == "px-6"]
    assert "--spacing" in missed.why and "app.css:3" in missed.why and "0.25rem" in missed.why


def test_a_preset_that_replaces_the_spacing_scale_leaves_no_default_step(tmp_path):
    found = _preset_project(tmp_path, "theme")
    assert sorted({u.cls for u in found.unknown_classes}) == [
        "-mt-1.5", "gap-4", "inset-0", "p-px", "px-6"]


def test_a_v4_theme_that_resets_spacing_leaves_no_default_step(tmp_path):
    _write(tmp_path, "app.css", "@import 'tailwindcss';\n@theme {\n  --spacing-*: initial;\n"
                                "  --spacing-gutter: var(--space-gutter);\n}\n")
    _write(tmp_path, "page.html", '<main class="px-6 px-gutter">x</main>')
    ts = TokenSet({})
    ts.add(Token("space.gutter", "dimension", {"value": 20, "unit": "px"}))
    found = scan([tmp_path], ts)
    assert [u.cls for u in found.unknown_classes] == ["px-6"]
    theme = read_theme([tmp_path], [tmp_path / "app.css"])
    assert theme.replaced == ["spacing"] and ("spacing", "*") not in theme.entries
    # Without the reset, a step is Tailwind's own: 0.25rem each.
    _write(tmp_path, "app.css", "@import 'tailwindcss';\n@theme {\n"
                                "  --spacing-gutter: var(--space-gutter);\n}\n")
    found = scan([tmp_path], ts)
    assert found.unknown_classes == []
    assert ("px-6", "raw", "24px") in {(u.prop, u.kind, u.value) for u in found.usages}


def test_a_v4_theme_block_is_read_in_tailwinds_own_namespaces(tmp_path):
    # text-shadow is a namespace of its own; a duration is in none.
    _write(tmp_path, "app.css", "@import 'tailwindcss';\n@theme {\n"
                                "  --text-shadow-soft: 0 1px 2px #0003;\n"
                                "  --duration-quick: 150ms;\n  --text-body: 1rem;\n}\n")
    theme = read_theme([tmp_path], [tmp_path / "app.css"])
    assert sorted(theme.entries) == [("text", "body"), ("text-shadow", "soft")]
    # The duration is never passed over in silence: it is listed with the fix.
    [(file, line, text, why)] = theme.not_read
    assert (file, line, text) == ("app.css", 4, "--duration-quick")
    assert why.startswith("is outside Tailwind 4's theme namespaces, so no utility reads it")
    assert "duration-[var(--duration-quick)]" in why


def test_a_transition_duration_in_a_v4_theme_is_listed_with_the_fix(tmp_path):
    _write(tmp_path, "app.css", "@import 'tailwindcss';\n@theme {\n"
                                "  --transition-duration-slow: var(--motion-slow);\n}\n")
    _write(tmp_path, "page.html", '<main class="md:flex duration-slow">x</main>')
    found = scan([tmp_path], TokenSet({}))
    [missed] = [n for n in found.not_read if n.text == "--transition-duration-slow"]
    assert missed.line == 3 and "duration-[var(--transition-duration-slow)]" in missed.why
