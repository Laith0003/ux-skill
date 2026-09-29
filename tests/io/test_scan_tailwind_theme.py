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
    ts.add(Token("radius.md", "dimension", {"value": 8, "unit": "px"}))
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
    assert ("rounded-card", "radius.md") in tokens
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
