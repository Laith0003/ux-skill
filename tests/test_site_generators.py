"""The site generators must not bring lint findings back into docs/.

Each test regenerates one page into a temp folder and lints it: no critical or
high finding, and none of the findings the site was cleaned of (inline style
declarations, `outline: none`, a generic CTA label).
"""
import importlib.util
from pathlib import Path

import pytest

from engine.linter import lint

ROOT = Path(__file__).resolve().parent.parent
BLOCKING = {"critical", "high"}
CLEANED = {"inline-style-attribute", "outline-none-no-focus-visible", "generic-cta-text",
           "heading-skip-h1-h3"}


def _load_script(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _bad(path):
    findings = lint([str(path)]).findings
    return [f"{f.rule_id} {Path(f.file).name}:{f.line} {f.excerpt.strip()[:90]}"
            for f in findings if f.severity in BLOCKING or f.rule_id in CLEANED]


def test_system_pack_preview_lints_clean(tmp_path):
    from engine.generator.system_pack import pack_system
    from engine.synthesizer import synthesize

    class Brief:
        industry, tone, audience = "luxury-fashion", ["luxury"], []
        must_have, forbidden, reference_brands, strict = [], [], [], False

    res = pack_system(synthesize(Brief()), name="Probe", description="A probe system.",
                      concept="Generated in a test.", out_dir=str(tmp_path), slug="probe")
    root = Path(res["dir"])
    assert _bad(root) == []
    preview = (root / "preview.html").read_text(encoding="utf-8")
    assert "Get started" not in preview
    assert "outline: none" not in (root / "css" / "tokens.css").read_text(encoding="utf-8")


def test_wide_spacing_scale_gets_phone_padding():
    from engine.generator.system_pack import _preview_phone_padding
    assert "padding-inline:var(--space-xs)" in _preview_phone_padding(
        {"spacing": {"scale": [12, 24, 36, 48, 72, 108]}})
    assert _preview_phone_padding({"spacing": {"scale": [6, 12, 18, 24, 36, 54]}}) == ""


@pytest.mark.parametrize("script", ["build-brands-page.py", "build-anti-patterns-page.py",
                                    "build-commands-page.py"])
def test_catalog_page_regenerates_lint_clean(tmp_path, script):
    mod = _load_script(script)
    if script == "build-brands-page.py":
        page = mod.build_html(*mod.load_index())
    elif script == "build-commands-page.py":
        page = mod.build_html(mod.collect())
    else:
        rules, version = mod.load_rules()
        page = mod.waive_quotes(mod.build_html(rules, version), rules)
        # regions name the rules they waive, and every one is closed
        assert "ux-lint-disable -->" not in page and page.count("ux-lint-off") == page.count("ux-lint-on")
    out = tmp_path / "page.html"
    out.write_text(page, encoding="utf-8")
    assert _bad(out) == []


def test_catalog_waivers_never_hide_template_markup(tmp_path):
    """Review of #45, W1: an inline style added to the card template, on the
    permalink or inside a quoted field, still reports after a rebuild."""
    mod = _load_script("build-anti-patterns-page.py")
    rules, version = mod.load_rules()
    page = mod.build_html(rules, version)
    page = page.replace('class="ap-anchor"', 'class="ap-anchor" style="color:red"')
    page = page.replace('<span class="ap-sub">Why bad</span>',
                        '<span class="ap-sub" style="color:red">Why bad</span>')
    page = mod.waive_quotes(page, rules)
    out = tmp_path / "page.html"
    out.write_text(page, encoding="utf-8")
    styled = [f for f in lint([str(out)]).findings if f.rule_id == "inline-style-attribute"]
    lines = page.splitlines()
    assert sum('class="ap-anchor"' in lines[f.line - 1] for f in styled) == len(rules)
    assert sum('class="ap-why"' in lines[f.line - 1] for f in styled) >= len(rules) - 5
    # the chrome is never inside a region
    for f in styled:
        assert "ux-lint-off" not in lines[f.line - 1] or "inline-style-attribute" not in lines[f.line - 1]
