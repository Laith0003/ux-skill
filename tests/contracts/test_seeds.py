"""The seed contracts: six experimental contracts that read cleanly and
bind to every generated system."""
import re
from pathlib import Path

import pytest

from engine.contracts import validate_contracts
from engine.contracts.library import SEED_DIR, load_folder, seed_contracts, seed_sources
from engine.contracts.schema import ContractError
from engine.contracts.yamlite import loads
from engine.foundations import build_system
from engine.synthesizer.axes import AxisValues

ROOT = Path(__file__).resolve().parents[2]
NAMES = ("button", "card", "dialog", "selectable-row", "status-banner", "text-field")
BRANDS = ("#3366FF", "#6B4423", "#FFD400", "#E11D48", "#16A34A", "#0EA5E9", "#7C3AED",
          "#F97316", "#111827", "#F5F5F5", "#00FFFF", "#FF00FF",
          # A near-gray brand whose selected surface matches a card in dark high
          # contrast: the ghost button's hover needs its edge there.
          "#E7EEE7")
AXES = (AxisValues(*[0.5] * 7), AxisValues(0.1, 0.9, 0.2, 0.3, 0.4, 0.5, 0.6),
        AxisValues(0.9, 0.1, 0.8, 0.7, 0.6, 0.5, 0.4))


def test_the_six_seeds_load_and_are_experimental():
    seeds = seed_contracts()
    assert tuple(c.name for c in seeds) == NAMES
    assert all(c.status == "experimental" for c in seeds)
    assert {c.name: c.variant_product() for c in seeds} == {
        "button": 6, "card": 2, "dialog": 2, "selectable-row": 2, "status-banner": 4,
        "text-field": 2}
    assert all(c.provenance.node is None and c.provenance.drift == () for c in seeds)


@pytest.mark.parametrize("brand", BRANDS)
@pytest.mark.parametrize("axes", AXES)
@pytest.mark.parametrize("arabic", [True, False])
def test_every_seed_binds_to_every_generated_system(brand, axes, arabic):
    ts = build_system(axes, brand, arabic=arabic).tokens
    assert validate_contracts(seed_contracts(), ts) == []


def test_interactive_seeds_meet_the_minimums():
    for c in seed_contracts():
        if c.interactive:
            assert c.a11y.target == "layout.target.min", c.name
            assert "focus" in c.states and "disabled" in c.states, c.name
        assert c.a11y.label == "localized"


def test_every_part_says_how_it_behaves_right_to_left():
    behaviors = {(c.name, p.name): p.rtl_behavior for c in seed_contracts() for p in c.parts}
    assert behaviors[("selectable-row", "chevron")] == "mirror"
    assert behaviors[("dialog", "scrim")] == "fixed"
    assert behaviors[("button", "spinner")] == "fixed"


def test_containers_that_match_their_surface_declare_an_edge():
    for name in ("card", "dialog", "text-field"):
        c = next(c for c in seed_contracts() if c.name == name)
        assert any(b.property == "border-width" and b.role == "border.outline"
                   and not b.when and b.state is None for b in c.tokens), name


def test_rings_on_tinted_fills_pin_three_to_one():
    pinned = [(c.name, r.bg) for c in seed_contracts() for r in c.contrast if r.high is not None
              and r.fg == "color.focus.ring"]
    assert pinned == [("selectable-row", "color.surface.selected")] + [
        ("status-banner", f"color.status.{s}.soft")
        for s in ("info", "success", "warning", "danger")]


def test_the_seed_files_read_the_same_in_a_full_yaml_reader():
    yaml = pytest.importorskip("yaml")
    for name, text in seed_sources().items():
        assert loads(text, name) == yaml.safe_load(text), name


def test_seed_files_ship_with_the_package():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'"engine\.contracts" = \["seed/\*\.yaml"\]', pyproject)
    assert sorted(p.stem for p in SEED_DIR.glob("*.yaml")) == list(NAMES)


def test_load_folder_names_every_problem_and_an_empty_folder(tmp_path):
    with pytest.raises(ContractError, match="holds no .yaml contract"):
        load_folder(tmp_path)
    (tmp_path / "a.yaml").write_text("name: b\n", encoding="utf-8")
    (tmp_path / "c.yaml").write_text("name: c\n\tx: 1\n", encoding="utf-8")
    with pytest.raises(ContractError) as err:
        load_folder(tmp_path)
    assert [p.rule for p in err.value.problems] == ["missing-key", "yaml"]
