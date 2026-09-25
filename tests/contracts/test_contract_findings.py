"""The form, display and navigation contracts hold what they rely on.

Each test below pins one review finding on the twelve contracts from
Tasks 17 and 18: shapes that never turn round, targets that wrap the glyph
and its label, one edge per field group, the prefix's direction, focus on
every part a person operates, and every edge, ring and track measured on
every surface the contract names, in every color context, over the seed
sweep (13 brands, 3 axis sets, both scripts).
"""
import re
from pathlib import Path

import pytest

from engine.contracts.bind import validate_contracts
from engine.contracts.library import seed_contracts
from engine.contracts.precedence import resolve
from engine.contracts.schema import PLACEMENT
from engine.foundations import build_system
from engine.foundations.color_math import contrast
from engine.foundations.modes import contexts
from engine.synthesizer.axes import AxisValues
from tests.contracts.test_seeds import AXES, BRANDS

ROOT = Path(__file__).resolve().parents[2]
GUIDANCE = ROOT / "engine" / "rulepack" / "guidance"
DECISIONS = ROOT / "engine" / "rulepack" / "decisions"
SEEDS = {c.name: c for c in seed_contracts()}
RING = ("focus-ring", "focus-ring-width", "focus-ring-offset")
# The softest corner the axes reach, where chips and controls are pills.
SOFT = AxisValues(0.5, 0.5, 0.5, 1.0, 0.0, 0.5, 0.5)
# Edge colors that mark a control's boundary or state, so each needs 3:1
# (WCAG 1.4.11) against whatever it sits on. color.line.subtle is the quiet
# edge of a container and is not one of them.
CONTROL_EDGES = ("color.line.input", "color.line.selected", "color.line.danger",
                 "color.line.accent", "color.action.primary-edge")


def _role(name, part, prop, variant=None, states=("default",)):
    winners = resolve(SEEDS[name], variant or {}, states).get((part, prop), ())
    assert len(winners) <= 1, (name, part, prop, winners)
    return winners[0].role if winners else None


def _paired(name, fg, bg, minimum=3.0):
    c = SEEDS[name]
    return any(r.fg == fg and r.minimum >= minimum
               and (r.bg == bg or (r.bg == "surfaces" and bg in c.surfaces))
               for r in c.contrast)


def _systems():
    for brand in BRANDS:
        for axes in AXES:
            for arabic in (True, False):
                yield brand, axes, build_system(axes, brand, arabic=arabic).tokens


def _color_contexts(ts):
    return contexts([a for a in ("scheme", "contrast") if a in ts.axes], ts.axes)


# T17 I1: shapes and targets ------------------------------------------------

@pytest.mark.parametrize("axes", AXES + (SOFT,))
def test_a_check_box_stays_square_and_a_field_of_lines_never_becomes_a_stadium(axes):
    ts = build_system(axes, "#3366FF").tokens
    box = _role("checkbox", "box", "radius")
    assert box == "radius.box"
    size = ts.resolve(_role("checkbox", "box", "min-size"))
    px = size["value"] * (16 if size["unit"] == "rem" else 1)
    # Half the box or more reads as a circle, and a round box is a radio.
    assert ts.resolve(box)["value"] * 2 < px, axes
    for name, variant in (("textarea", {}), ("text-field", {"lines": "multiple"})):
        role = _role(name, "input", "radius", variant)
        assert role == "radius.area", name
        assert ts.resolve(role)["value"] < 999, (name, axes)
    assert _role("text-field", "input", "radius", {"lines": "single"}) == "radius.control"


@pytest.mark.parametrize("name,glyph", [("checkbox", "box"), ("radio", "dot")])
def test_the_target_wraps_the_glyph_and_its_label_and_the_glyph_is_icon_sized(name, glyph):
    c = SEEDS[name]
    assert _role(name, glyph, "min-size") == "type.icon.size.control"
    assert _role(name, "target", "min-size") == "layout.target.min"
    assert not any(b.role == "layout.target.min" for b in c.tokens if b.part != "target")
    assert {p.name: p.rtl_behavior for p in c.parts}["target"] == "logical"
    assert any("target" in line and "label" in line for line in c.do), name


def test_every_line_under_a_field_keeps_its_gap_from_the_field_and_its_ring():
    # The ring draws outside the field; a line under it with no gap touches
    # the ring (seen on the textarea counter in the contact sheets).
    for c in SEEDS.values():
        for part in ("helper", "counter", "message"):
            if any(p.name == part for p in c.parts):
                assert any(b.part == part and b.property == "stack-gap" for b in c.tokens), \
                    (c.name, part)


# T17 I2, I3 and radius.md:35: the field with a prefix ----------------------

@pytest.mark.parametrize("position", ["start", "end"])
@pytest.mark.parametrize("state", ["default", "hover", "focus", "error", "disabled"])
def test_a_field_with_a_prefix_draws_one_edge_and_one_divider(position, state):
    got = resolve(SEEDS["input-prefix"], {"position": position}, ("default", state))
    edged = sorted({part for part, prop in got if prop in ("border-width", "border-color")})
    assert edged == ["group"], (position, state)
    affix = "prefix" if position == "start" else "suffix"
    other = "suffix" if position == "start" else "prefix"
    assert {prop for part, prop in got if part == affix} >= {"divider-width", "divider-color"}
    assert not any(part == other for part, _ in got), (position, state)
    # One shape: the group has the corner and clips its parts, and no part
    # inside it rounds or squares a corner of its own.
    radii = {part: b[0].role for (part, prop), b in got.items() if prop == "radius"}
    assert radii == {"group": "radius.control"}
    if state == "error":
        assert _role("input-prefix", "group", "border-color", {"position": position},
                     ("default", state)) == "color.line.danger"


def test_the_prefix_leads_a_left_to_right_run_and_a_suffix_follows_the_page():
    parts = {p.name: p.rtl_behavior for p in SEEDS["input-prefix"].parts}
    assert parts == {"label": "logical", "group": "logical", "run": "fixed", "prefix": "fixed",
                     "input": "fixed", "suffix": "logical", "message": "logical"}
    do = SEEDS["input-prefix"].do
    assert any(line.startswith("With position start") and "+962 791234567" in line
               for line in do)
    assert any(line.startswith("With position end") and "page's direction" in line
               for line in do)


def test_radius_guidance_and_the_contracts_agree():
    text = (GUIDANCE / "radius.md").read_text(encoding="utf-8")
    assert "| A check box's box | radius.box |" in text
    assert "| A field of several lines | radius.area |" in text
    assert "| A field with a prefix or a suffix | one shape: radius.control on the group" in text
    assert "- `radius.chip`: small tags, badges and chips; a pill in soft brands. Never a " \
           "check box" in text
    chips = {c.name for c in SEEDS.values() for b in c.tokens if b.role == "radius.chip"}
    assert chips == {"badge", "chip"}
    assert not any(b.role == "radius.joined" for b in SEEDS["input-prefix"].tokens)


# T17 I4, T18 I5, I6: focus on every part a person operates ----------------

def test_every_part_a_person_operates_shows_focus():
    # A part sized to the target is one a person presses; it draws its own
    # ring in the focus state. The checkbox and radio target wraps the glyph
    # and the label, and the ring sits on the glyph.
    missing = []
    for c in SEEDS.values():
        for part in sorted({b.part for b in c.tokens if b.property == "min-size"
                            and b.role == "layout.target.min"}):
            ringed = part if part != "target" else {"checkbox": "box", "radio": "dot"}[c.name]
            props = {b.property for b in c.tokens if b.part == ringed and b.state == "focus"}
            if not set(RING) <= props:
                missing.append((c.name, part))
    assert missing == []
    for name, part in (("date", "previous"), ("date", "next"), ("date", "button"),
                       ("chip", "remove"), ("nav", "menu-button")):
        assert _role(name, part, "min-size", {"kind": "input", "layout": "collapsed"}) \
            == "layout.target.min", (name, part)


def test_the_remove_button_is_round_so_its_ring_fits_inside_a_pill_chip():
    # Seen in the soft contact sheet: a square ring around the remove icon
    # cut across the pill chip's curve.
    assert _role("chip", "remove", "radius", {"kind": "input"}) == "radius.pill"


def test_the_active_option_in_an_open_list_is_visible():
    for prop, role in (("fill", "color.surface.sunken"), ("border-width", "border.outline"),
                       ("border-color", "color.line.input"), ("focus-ring", "color.focus.ring")):
        assert _role("select", "option", prop, states=("default", "focus")) == role, prop
    assert any("aria-activedescendant" in line for line in SEEDS["select"].do)


def test_a_select_says_what_loads_and_what_is_empty_and_marks_a_disabled_option():
    c = SEEDS["select"]
    assert {"loading", "empty"} <= set(c.states)
    assert dict(c.copy)["loading"] and dict(c.copy)["empty"]
    for state in ("loading", "empty"):
        assert _role("select", "notice", "text", states=("default", state)) == \
            "color.text.muted"
    assert any("notice" in line and "loading" in line and "empty" in line for line in c.do)
    assert _role("select", "spinner", "icon", states=("default", "loading")) == \
        "color.text.muted"
    assert _paired("select", "color.text.muted", "color.surface.raised", 4.5)
    assert any("disabled option" in line and "color.text.disabled" in line for line in c.do)
    assert _role("select", "chevron", "icon", states=("default", "disabled")) == \
        "color.text.disabled"


def test_a_calendar_marks_today_and_days_out_of_range():
    c = SEEDS["date"]
    assert any("out of range" in line and "color.text.disabled" in line
               and "aria-disabled" in line for line in c.do)
    assert any("today" in line.lower() and "aria-current" in line for line in c.do)
    assert _role("date", "button", "icon", states=("default", "disabled")) == \
        "color.text.disabled"


def test_the_table_takes_focus_on_its_rows_and_its_scrolling_region():
    for part, variant in (("row", {}), ("region", {"layout": "scroll"})):
        for prop in RING:
            assert _role("table", part, prop, variant, ("default", "focus")) is not None, part
    assert {p.name: p.rtl_behavior for p in SEEDS["table"].parts}["select"] == "logical"
    assert any("select part" in line and "checkbox contract" in line
               for line in SEEDS["table"].do)


def test_the_open_menu_is_a_raised_layer_measured_where_it_sits():
    nav = SEEDS["nav"]
    v = {"layout": "collapsed"}
    assert _role("nav", "menu", "fill", v) == "color.surface.raised"
    assert _role("nav", "menu", "layer", v) == "elevation.order.dropdown"
    assert _role("nav", "menu", "shadow", v) == "elevation.popover"
    assert _role("nav", "menu", "fill", {"layout": "inline"}) is None
    assert "color.surface.raised" in nav.surfaces
    for fg in ("color.text.default", "color.text.link", "color.line.selected",
               "color.focus.ring"):
        assert _paired("nav", fg, "color.surface.raised"), fg
    text = " ".join(nav.do)
    for word in ("aria-expanded", "aria-controls", "Escape", "button contract"):
        assert word in text, word


# T17 I5, T18 I1: control edges on every surface, in every context ----------

def test_every_control_edge_and_ring_is_paired_with_every_surface():
    # An edge or a ring on the component's outer part sits on the surfaces
    # it names; one on a part inside a filled container (a dialog's close,
    # a banner's dismiss) is paired with that container's fill instead.
    unpaired = []
    for c in SEEDS.values():
        inner = {b.role for b in c.tokens if b.property == "fill"}
        for b in c.tokens:
            if b.state == "disabled":
                continue
            if b.property in ("border-color", "divider-color") and b.role in CONTROL_EDGES \
                    or b.property == "focus-ring":
                on_fill = any(_paired(c.name, b.role, f) for f in inner
                              if f not in c.surfaces and not any(
                                  x.part == b.part and x.role == f for x in c.tokens))
                # a binding under a placement variant sits on the surface it
                # names (decisions/fills-on-every-placement.md)
                where = dict(b.when).get(PLACEMENT)
                surfaces = (f"color.surface.{where}",) if where and where != "default" \
                    else c.surfaces
                for s in surfaces:
                    if not _paired(c.name, b.role, s) and not on_fill:
                        unpaired.append((c.name, b.label(), s))
    assert sorted(set(unpaired)) == []


def test_the_checked_box_edge_is_the_selected_line():
    for checked in ("on", "mixed"):
        assert _role("checkbox", "box", "border-color", {"checked": checked}) == \
            "color.line.selected"


def test_the_progress_track_is_measured_on_every_surface():
    assert _role("progress", "track", "border-color") == "color.line.input"
    assert _role("progress", "track", "border-width") == "border.outline"
    for s in SEEDS["progress"].surfaces:
        assert _paired("progress", "color.line.input", s), s


@pytest.mark.parametrize("brand", BRANDS)
def test_edges_that_mark_a_control_clear_three_to_one_on_every_named_surface(brand):
    # The measurement behind the pairings, for the edges the reviews found
    # below 3:1: the checked box's edge and the empty progress track.
    for axes in AXES:
        ts = build_system(axes, brand).tokens
        for name, fg in (("checkbox", "color.line.selected"), ("progress", "color.line.input"),
                         ("table", "color.line.input"), ("input-prefix", "color.line.input")):
            for s in SEEDS[name].surfaces:
                for mode in _color_contexts(ts):
                    ratio = contrast(ts.resolve(fg, mode), ts.resolve(s, mode))
                    assert ratio >= 3, (brand, name, fg, s, mode, round(ratio, 2))


# T18 I2: the progress value keeps the page's direction ---------------------

def test_the_progress_value_is_words_in_the_page_direction():
    parts = {p.name: p.rtl_behavior for p in SEEDS["progress"].parts}
    assert parts["value"] == "logical"
    assert any("never wrap the whole value" in line for line in SEEDS["progress"].do)


# T18 I3: stripes and hover on the surfaces the table names ---------------

def test_stripes_and_a_hovered_striped_row_show_on_every_surface_the_table_names():
    table = SEEDS["table"]
    assert table.surfaces == ("color.surface.card",)
    striped = {"rows": "striped"}
    assert _role("table", "row", "fill", striped) == "color.surface.stripe"
    assert _role("table", "row", "border-color", striped, ("default", "hover")) == \
        "color.line.input"
    for bg in ("color.surface.stripe", "color.surface.sunken", "color.surface.card"):
        assert _paired("table", "color.line.input", bg), bg
    worst = 9.0
    for _, _, ts in _systems():
        for mode in _color_contexts(ts):
            stripe = ts.resolve("color.surface.stripe", mode)
            for s in table.surfaces:
                worst = min(worst, contrast(stripe, ts.resolve(s, mode)))
    assert worst > 1.0


# T18 I4: the phone layout is bound -----------------------------------------

def test_the_phone_layout_is_bound():
    table = SEEDS["table"]
    layout = next(v for v in table.variants if v.name == "layout")
    assert layout.values == ("grid", "scroll", "stacked") and layout.default == "grid"
    scroll = {"layout": "scroll"}
    assert _role("table", "sticky", "layer", scroll) == "elevation.order.sticky"
    assert _role("table", "sticky", "divider-width", scroll) is not None
    assert _role("table", "sticky", "divider-color", scroll) == "color.line.input"
    for states, variant, fill in (
            (("default",), scroll, "color.surface.card"),
            (("default",), {"layout": "scroll", "rows": "striped"}, "color.surface.stripe"),
            (("default", "hover"), scroll, "color.surface.sunken"),
            (("default", "selected"), scroll, "color.surface.selected")):
        # The sticky cell takes its row's fill, so cells never show through.
        assert _role("table", "sticky", "fill", variant, states) == fill == \
            (_role("table", "row", "fill", variant, states) or "color.surface.card"), states
    assert _role("table", "sticky", "fill", {"layout": "grid"}) is None
    stacked = {"layout": "stacked"}
    assert _role("table", "label", "font", stacked) == "type.text.label"
    assert _role("table", "label", "text", stacked) == "color.text.muted"
    parts = {p.name: p.rtl_behavior for p in table.parts}
    assert parts["sticky"] == parts["region"] == parts["label"] == "logical"
    text = " ".join(table.do)
    for words in ("four columns or fewer", "tabindex", "inline start", "aria-labelledby",
                  "first header cell sticks"):
        assert words in text, words


# T18 I7: guidance lines the contracts contradicted -------------------------

def test_table_rows_follow_border_guidance():
    border = (GUIDANCE / "border.md").read_text(encoding="utf-8")
    assert "a striped row takes border.outline" in border
    assert _role("table", "row", "border-width") == "border.separator"
    assert _role("table", "row", "border-color") == "color.line.subtle"
    assert _role("table", "row", "border-width", {"rows": "striped"}) == "border.outline"


def test_the_bar_grows_with_the_expand_role_and_a_long_spinner_can_stop():
    assert _role("progress", "bar", "transition-duration") == "motion.expand.duration"
    assert _role("progress", "bar", "transition-curve") == "motion.expand.curve"
    assert any("longer than 5 seconds" in line and "pauses or cancels" in line
               for line in SEEDS["progress"].do)


def test_a_standalone_link_underlines_its_words_not_its_target_box():
    # Seen in the contact sheets: an underline drawn as the 44px target's
    # bottom edge floats a line away from the words.
    assert _role("link", "text", "min-size", {"context": "standalone"}) == "layout.target.min"
    assert _role("link", "underline", "border-width") == "border.outline"
    assert any("under the words" in line and "text-decoration" in line
               for line in SEEDS["link"].do)


def test_a_chip_is_not_called_a_tag():
    assert not re.search(r"\btag\b", SEEDS["chip"].description)


# T17 I6: the record states each control's own rules -----------------------

def _record_rows(record):
    text = (DECISIONS / f"{record}.md").read_text(encoding="utf-8")
    rows = [line.strip("|").split("|") for line in text.splitlines()
            if line.startswith("| ") and not line.startswith("| Control")
            and not line.startswith("|---")]
    return {r[0].strip(): [cell.strip() for cell in r[1:]] for r in rows}


def test_the_form_record_states_what_each_contract_binds():
    rows = _record_rows("form-contracts-per-control")
    assert sorted(rows) == ["checkbox", "date", "input-prefix", "radio", "select", "textarea"]
    for name, (label, hover, icon, reserved, target) in rows.items():
        c = SEEDS[name]
        label_part = "legend" if name == "radio" else "label"
        assert f"`{_role(name, label_part, 'font')}`" == label, name
        hover_props = {b.property for b in c.tokens if b.state == "hover"}
        assert (hover == "edge") == (hover_props == {"edge-weight"}), name
        assert (icon == "yes") == any(b.part == "icon" and b.state == "error"
                                      for b in c.tokens), name
        assert (reserved == "yes") == any("Reserve one line" in d for d in c.do), name
        target_part = "target" if name in ("checkbox", "radio") else None
        parts = {b.part for b in c.tokens if b.role == "layout.target.min"}
        assert target in {", ".join(sorted(parts))}, name
        if target_part:
            assert parts == {target_part}


def test_the_superseded_records_name_their_replacements():
    for old, new in (("form-contracts", "form-contracts-per-control"),
                     ("display-and-navigation-contracts", "display-contracts-measured"),
                     ("radius-roles", "radius-roles-by-shape")):
        text = (DECISIONS / f"{old}.md").read_text(encoding="utf-8")
        assert "status: superseded" in text and f"superseded_by: {new}" in text, old


# The sweep: every contract still binds everywhere --------------------------

def test_the_twelve_contracts_bind_on_the_softest_corner():
    for brand in BRANDS:
        ts = build_system(SOFT, brand).tokens
        assert validate_contracts(seed_contracts(), ts) == [], brand


# A field's hover and error never move the layout ----------------------------

FIELDS = {"text-field": "input", "textarea": "input", "date": "input", "select": "trigger",
          "input-prefix": "group"}


@pytest.mark.parametrize("name,part", sorted(FIELDS.items()))
def test_a_field_draws_its_heavier_edge_inside_its_border(name, part):
    # A 2px border on hover shifts the layout by a pixel on each side. The
    # border keeps its resting width in every state; the extra weight is
    # edge-weight, drawn inside it as an inset shadow or an outline.
    resting = _role(name, part, "border-width")
    assert resting == "border.outline"
    for state in ("hover", "error"):
        assert _role(name, part, "border-width", states=(state,)) == resting, (name, state)
        assert _role(name, part, "edge-weight", states=(state,)) == "border.emphasis", (name, state)
    assert any("edge-weight" in line and "inset" in line for line in SEEDS[name].do), name


def test_edge_weight_is_a_dimension_the_schema_names():
    from engine.contracts.schema import PROPERTY_TYPES
    assert PROPERTY_TYPES["edge-weight"] == "dimension"
    text = (GUIDANCE / "border.md").read_text(encoding="utf-8")
    assert "edge-weight" in text and "inset" in text


# The FAQ accordion and the site footer --------------------------------------

def test_the_faq_question_is_the_whole_row_and_the_answer_reads_as_body_text():
    assert SEEDS["faq-accordion"].status == "experimental"
    assert _role("faq-accordion", "question", "min-size") == "layout.target.min"
    assert _role("faq-accordion", "question", "font") == "type.text.heading-3"
    assert _role("faq-accordion", "answer", "font") == "type.text.body"
    assert _role("faq-accordion", "answer", "max-width") == "layout.measure.text"
    assert _role("faq-accordion", "answer", "enter-duration") == "motion.expand.duration"
    assert _role("faq-accordion", "item", "border-width") == "border.separator"
    assert _role("faq-accordion", "question", "focus-ring", states=("focus",)) == "color.focus.ring"
    assert any("aria-expanded" in line and "aria-controls" in line for line in SEEDS["faq-accordion"].do)


def test_the_footer_binds_the_logo_role_and_keeps_links_at_the_target_size():
    assert SEEDS["site-footer"].status == "experimental"
    assert _role("site-footer", "logo", "icon") == "color.logo"
    assert _paired("site-footer", "color.logo", "color.surface.page")
    assert _role("site-footer", "link", "min-size") == "layout.target.min"
    assert _role("site-footer", "region", "padding-block") == "layout.footer.padding-block"
    assert _role("site-footer", "divider", "border-width") == "border.separator"
    assert _role("site-footer", "legal", "font") == "type.text.fine"
    assert _role("site-footer", "link", "focus-ring", states=("focus",)) == "color.focus.ring"


@pytest.mark.parametrize("name", ["faq-accordion", "site-footer"])
def test_the_new_contracts_bind_on_every_generated_system(name):
    contract = [SEEDS[name]]
    for brand, _axes, ts in _systems():
        assert validate_contracts(contract, ts) == [], (name, brand)


def test_the_footer_sits_on_the_page_where_its_logo_is_measured():
    # color.logo is held at 3:1 against the page only; on the sunken surface
    # it falls below that for some brands, so the footer does not offer it.
    assert SEEDS["site-footer"].surfaces == ("color.surface.page",)


@pytest.mark.parametrize("name", ["nav", "site-footer"])
def test_a_logo_that_links_home_has_a_target_and_a_ring(name):
    assert _role(name, "logo", "min-size") == "layout.target.min"
    for prop in RING:
        assert _role(name, "logo", prop, states=("focus",)) is not None, (name, prop)


def test_edge_weight_is_never_drawn_as_an_outline():
    text = (GUIDANCE / "border.md").read_text(encoding="utf-8")
    assert "--color-line-danger" in text and "Never draw it with an outline" in text
    assert not any("negative offset" in line for c in SEEDS.values() for line in c.do)
