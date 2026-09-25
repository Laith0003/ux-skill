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


@pytest.mark.parametrize("script", ["build-brands-page.py", "build-anti-patterns-page.py"])
def test_catalog_page_regenerates_lint_clean(tmp_path, script):
    mod = _load_script(script)
    if script == "build-brands-page.py":
        page = mod.build_html(*mod.load_index())
    else:
        page = mod.build_html(*mod.load_rules())
    out = tmp_path / "page.html"
    out.write_text(page, encoding="utf-8")
    assert _bad(out) == []
