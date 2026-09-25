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
from engine.foundations.modes import contexts
from engine.synthesizer.axes import AxisValues

ROOT = Path(__file__).resolve().parents[2]
NAMES = ("badge", "button", "card", "checkbox", "chip", "date", "dialog", "faq-accordion",
         "input-prefix", "link", "nav", "progress", "radio", "select", "selectable-row",
         "site-footer", "status-banner", "table", "text-field", "textarea")
BRANDS = ("#3366FF", "#6B4423", "#FFD400", "#E11D48", "#16A34A", "#0EA5E9", "#7C3AED",
          "#F97316", "#111827", "#F5F5F5", "#00FFFF", "#FF00FF",
          # A near-gray brand whose selected surface matches a card in dark high
          # contrast: the ghost button's hover needs its edge there.
          "#E7EEE7")
AXES = (AxisValues(*[0.5] * 7), AxisValues(0.1, 0.9, 0.2, 0.3, 0.4, 0.5, 0.6),
        AxisValues(0.9, 0.1, 0.8, 0.7, 0.6, 0.5, 0.4))


def test_the_seeds_load_and_are_experimental():
    seeds = seed_contracts()
    assert tuple(c.name for c in seeds) == NAMES
    assert all(c.status == "experimental" for c in seeds)
    assert {c.name: c.variant_product() for c in seeds} == {
        "badge": 6, "button": 18, "card": 2, "checkbox": 3, "chip": 2, "date": 1, "dialog": 2,
        "faq-accordion": 1, "input-prefix": 2, "link": 2, "nav": 2, "progress": 2, "radio": 2, "select": 1,
        "selectable-row": 2, "site-footer": 1, "status-banner": 4, "table": 6, "text-field": 2, "textarea": 2}
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
            # a link is never disabled: it is there or it is not
            assert "focus" in c.states and ("disabled" in c.states or c.name == "link"), c.name
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
    assert pinned == [("chip", "color.surface.selected"),
                      ("selectable-row", "color.surface.selected")] + [
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


def _seed(name):
    return next(c for c in seed_contracts() if c.name == name)


def _bound(c, part, prop, variant, state):
    """The binding that applies to `part.prop` for one variant and state: a
    binding for the state beats a stateless one, then the one with more
    conditions wins. None when nothing applies."""
    fits = [b for b in c.tokens if b.part == part and b.property == prop
            and all(variant.get(k) == v for k, v in b.when)
            and b.state in (None, state)]
    if not fits:
        return None
    return max(fits, key=lambda b: (b.state is not None, len(b.when))).role


def test_secondary_and_ghost_buttons_are_complete_in_every_state():
    c = _seed("button")
    for emphasis in ("secondary", "ghost"):
        for intent in ("neutral", "danger"):
            v = {"emphasis": emphasis, "intent": intent}
            assert _bound(c, "container", "fill", v, "pressed") \
                == _bound(c, "container", "fill", v, "hover") is not None, v
            for state in c.states:
                width = _bound(c, "container", "border-width", v, state)
                color = _bound(c, "container", "border-color", v, state)
                edged = emphasis == "secondary" or state in ("hover", "pressed")
                assert (width is not None, color is not None) == (edged, edged), (v, state)
                if edged:
                    assert width == "border.outline", (v, state)
                    assert (color == "color.text.disabled") == (state == "disabled"), (v, state)
            assert _bound(c, "label", "text", v, "disabled") == "color.text.disabled"


def _all_contexts(ts):
    return contexts(list(ts.axes), ts.axes)


@pytest.mark.parametrize("name,part,surface", [("dialog", "close", "color.surface.raised"),
                                               ("status-banner", "dismiss", None)])
def test_close_and_dismiss_are_specified_targets(name, part, surface):
    c = _seed(name)
    assert "focus" in c.states and c.a11y.target == "layout.target.min"
    role = {b.property: b.role for b in c.tokens if b.part == part and b.state is None}
    focus = {b.property for b in c.tokens if b.part == part and b.state == "focus"}
    assert focus == {"focus-ring", "focus-ring-width", "focus-ring-offset"}
    assert role["min-size"] == "layout.target.min"
    for brand in BRANDS[:3]:
        ts = build_system(AXES[0], brand).tokens
        # WCAG 2.5.8 sets 24 by 24 CSS px; the bound role meets it in every context.
        for mode in _all_contexts(ts):
            size = ts.resolve(role["min-size"], mode)
            assert size["unit"] == "px" and size["value"] >= 24, (brand, mode)
    backgrounds = [surface] if surface else [
        b.role for b in c.tokens if b.part == "container" and b.property == "fill"]
    for bg in backgrounds:
        assert any(r.fg == role["icon"] and r.bg == bg and r.minimum == 3
                   and r.criterion == "1.4.11" for r in c.contrast), (name, bg)


def test_the_status_banner_draws_an_edge_paired_on_every_surface():
    c = _seed("status-banner")
    edge = {b.property: b.role for b in c.tokens
            if b.part == "container" and not b.when and b.state is None}
    assert edge["border-width"] == "border.outline"
    assert edge["border-color"].startswith("color.line.")
    assert any(r.fg == edge["border-color"] and r.bg == "surfaces" and r.minimum == 3
               and r.criterion == "1.4.11" and r.high is None for r in c.contrast)


def test_the_unchecked_box_has_a_boundary_on_every_row_fill_it_sits_on():
    c = _seed("selectable-row")
    v = {"selection": "multiple"}
    assert _bound(c, "leading", "border-width", v, "default") in ("border.outline",
                                                                   "border.emphasis")
    line = _bound(c, "leading", "border-color", v, "default")
    assert line == "color.line.input"
    for state in ("default", "hover", "pressed", "focus"):
        assert _bound(c, "leading", "border-color", v, state) == line, state
    assert _bound(c, "leading", "border-color", v, "selected") == "color.line.selected"
    assert _bound(c, "leading", "border-color", v, "disabled") == "color.text.disabled"
    assert _bound(c, "leading", "border-color", {"selection": "single"}, "default") is None
    # The unchecked box sits on the list's surfaces (default, focus) and on
    # the hover and pressed fill; each pairing is 3:1 under WCAG 1.4.11.
    row_fills = {_bound(c, "container", "fill", v, s) for s in ("hover", "pressed")}
    for bg in ["surfaces"] + sorted(row_fills):
        assert any(r.fg == line and r.bg == bg and r.minimum == 3 and r.criterion == "1.4.11"
                   for r in c.contrast), bg


def test_the_card_says_in_which_high_contrast_its_fill_meets_the_page():
    card = next(c for c in seed_contracts() if c.name == "card")
    line = next(d for d in card.do if d.startswith("Keep an edge on every card"))
    assert "in light high contrast the card and the page are the same color" in line
    for brand in BRANDS:
        ts = build_system(AXES[0], brand).tokens
        light = [ts.resolve(r, "contrast:high") for r in ("color.surface.card",
                                                          "color.surface.page")]
        dark = [ts.resolve(r, "scheme:dark,contrast:high") for r in ("color.surface.card",
                                                                     "color.surface.page")]
        assert light[0] == light[1] and dark[0] != dark[1], brand


def _binding(contract, part, prop, state=None, when=()):
    return next((b.role for b in contract.tokens if (b.part, b.property, b.state) ==
                 (part, prop, state) and b.when == tuple(when)), None)


def test_a_field_is_readable_and_its_label_is_never_smaller_than_its_value():
    field = next(c for c in seed_contracts() if c.name == "text-field")
    assert _binding(field, "helper", "font") == "type.text.body-small"
    assert _binding(field, "message", "font", "error") == "type.text.body-small"
    assert _binding(field, "label", "font") == "type.text.ui-large"
    assert _binding(field, "helper", "text") != _binding(field, "placeholder", "text")
    assert _binding(field, "input", "border-width", "hover") is None
    assert _binding(field, "input", "edge-weight", "hover") == "border.emphasis"
    assert _binding(field, "input", "max-width") is None
    assert _binding(field, "label", "stack-gap") == "space.field.label-gap"
    assert any("never moves the submit button" in line for line in field.do)
    for axes in AXES:
        ts = build_system(axes, "#3366FF").tokens
        for mode in ("", "direction:rtl"):
            label = ts.resolve("type.text.ui-large", mode)["fontSize"]
            value = ts.resolve("type.text.body", mode)["fontSize"]
            assert label == value


def test_a_card_keeps_its_body_readable_and_its_inner_corners_whole():
    card = next(c for c in seed_contracts() if c.name == "card")
    assert _binding(card, "body", "text") == "color.text.default"
    assert _binding(card, "meta", "text") == "color.text.muted"
    assert any("never below 0" in line and "radius.joined" in line for line in card.do)


def test_a_banner_reads_at_body_size_and_allows_an_error_summary():
    banner = next(c for c in seed_contracts() if c.name == "status-banner")
    assert _binding(banner, "title", "font") == _binding(banner, "body", "font") == \
        "type.text.body"
    assert _binding(banner, "title", "font-weight") == "type.strong"
    assert any("error summary" in line for line in banner.dont)


def test_a_button_has_a_large_size_and_a_view_is_defined():
    button = next(c for c in seed_contracts() if c.name == "button")
    large = (("size", "large"),)
    assert _binding(button, "container", "min-size", when=large) == "layout.target.large"
    assert _binding(button, "label", "font", when=large) == "type.text.ui-large"
    assert any("A view is what one screen shows without scrolling" in line for line in button.do)
