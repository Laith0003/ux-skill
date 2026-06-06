"""DESIGN.md emitter tests (the awesome-design-md / Google Stitch standard output).

The feature shipped without tests; these lock the contract: 8 keys, colors sourced
from the palette with the rename rules, brand-name handling, and the no-dash house rule.
"""
from engine.generator import design_md
from engine.generator.core import _emit_design_md
from engine.recommender.core import Recommendation, Brief, recommend


def _rec():
    return Recommendation(
        style={"id": "swiss", "name": "Swiss International"},
        palette={"id": "amber", "name": "Amber", "colors": {
            "primary": "#f59e0b", "primary_active": "#d97706", "danger": "#ef4444"}},
        type_pair={"display": {"family": "Fraunces"}, "body": {"family": "Inter"},
                   "mono": {"family": "JetBrains Mono"}},
    )


def test_emit_has_all_eight_design_md_keys():
    md = _emit_design_md(_rec())
    for key in ("version:", "name:", "description:", "colors:",
                "typography:", "spacing:", "rounded:", "components:"):
        assert key in md, f"DESIGN.md missing required key: {key}"


def test_colors_come_from_palette_with_rename_rules():
    md = _emit_design_md(_rec())
    assert '"#f59e0b"' in md                          # primary value from the palette
    assert "primary-active:" in md                    # underscore -> hyphen
    assert "error:" in md and "danger:" not in md     # danger renamed to error


def test_name_uses_brand_when_present_not_the_dict():
    md = _emit_design_md(_rec(), Brief(project_type="landing", brand={"name": "Acme Co"}))
    assert "name: acme-co-design-analysis" in md      # brand name, sanitized
    assert "{'name'" not in md                        # not a stringified dict (the bug fix)


def test_falls_back_to_project_type_then_default():
    assert "name: landing-design-analysis" in _emit_design_md(_rec(), Brief(project_type="landing"))
    assert "name: ux-skill-design-analysis" in _emit_design_md(_rec(), None)


def test_no_em_or_en_dashes_house_rule():
    md = _emit_design_md(_rec())
    assert "—" not in md and "–" not in md and "‒" not in md


def test_design_md_writes_file_and_returns_summary(tmp_path):
    out = tmp_path / "sub" / "DESIGN.md"
    result = design_md(_rec(), None, str(out))
    assert out.exists() and isinstance(result, dict)
    content = out.read_text(encoding="utf-8")
    assert content.startswith("---") and content.rstrip().endswith("---")


def test_integration_real_recommendation_emits_structure():
    rec = recommend(Brief(project_type="landing", tone=["bold"]))
    md = _emit_design_md(rec, None)
    assert "colors:" in md and "typography:" in md and "components:" in md


def test_frontmatter_is_valid_yaml_when_pyyaml_available():
    import pytest
    yaml = pytest.importorskip("yaml")
    md = _emit_design_md(_rec())
    data = yaml.safe_load(md.split("---")[1])
    assert {"version", "name", "description", "colors", "typography",
            "spacing", "rounded", "components"}.issubset(data.keys())
