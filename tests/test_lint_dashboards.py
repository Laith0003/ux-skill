"""Precision on dashboards as admin templates ship them: a Tailwind 4 build
wraps its utilities in @layer, composes every shadow from custom
properties, and a reset gives buttons a pointer only while they are not
disabled; a menu swaps its focus outline for a fill; a checkbox draws its
mark on a pseudo-element. Each case pairs what the rule must stop reporting
with what it must still report."""
from engine.linter.core import lint_text


def _ids(text: str, name: str = "page.html"):
    return [f.rule_id for f in lint_text(name, text)]


PAGE = """<!doctype html><html lang="en"><head><style>
{css}
</style></head><body><main><h1>Orders</h1>{body}</main></body></html>"""


# ------------------------------------------------ utilities inside @layer

LAYERED = r"""
@layer utilities {
  .rounded-2xl { border-radius: 1rem; }
  .backdrop-blur { backdrop-filter: blur(8px); }
}
"""


def test_a_layered_utility_no_element_uses_is_not_reported():
    ids = _ids(PAGE.format(css=LAYERED, body="<p>Today</p>"))
    assert "border-radius-2xl-default" not in ids


def test_a_layered_utility_an_element_uses_is_still_reported():
    ids = _ids(PAGE.format(css=LAYERED, body='<div class="rounded-2xl"><p>Today</p></div>'))
    assert "border-radius-2xl-default" in ids


# ------------------------------------------------ shadows made of custom properties

PLUMBING = """
.shadow-sm { --tw-shadow: 0 1px 3px 0 #0000001a; box-shadow: var(--tw-inset-shadow),
  var(--tw-inset-ring-shadow), var(--tw-ring-offset-shadow), var(--tw-ring-shadow),
  var(--tw-shadow); }
"""
LAYERS = """
.card { box-shadow: 0 1px 1px #0001, 0 2px 2px #0001, 0 4px 4px #0001, 0 8px 8px #0001,
  0 16px 16px #0001; }
"""


def test_a_shadow_made_only_of_custom_properties_is_not_counted_as_layers():
    ids = _ids(PAGE.format(css=PLUMBING, body='<div class="shadow-sm"><p>a</p></div>'))
    assert "box-shadow-multilayer-default" not in ids


def test_five_drawn_layers_are_still_reported():
    ids = _ids(PAGE.format(css=LAYERS, body='<div class="card"><p>a</p></div>'))
    assert "box-shadow-multilayer-default" in ids


# ------------------------------------------------ pointer on controls that are not disabled

def test_a_pointer_only_while_not_disabled_is_not_reported():
    css = 'button:not(:disabled), [type="button"]:not(:disabled) { cursor: pointer; }'
    ids = _ids(PAGE.format(css=css, body='<button type="button">Save</button>'))
    assert "cursor-pointer-on-disabled" not in ids


def test_a_pointer_on_a_disabled_control_is_still_reported():
    css = "button:disabled { cursor: pointer; }"
    ids = _ids(PAGE.format(css=css, body='<button type="button" disabled>Save</button>'))
    assert "cursor-pointer-on-disabled" in ids


# ------------------------------------------------ a focus fill in place of the outline

def test_a_focus_rule_that_fills_the_control_is_a_visible_indicator():
    css = ".menu-button:focus-visible { outline: none; background-color: #dbe4ff; }"
    ids = _ids(PAGE.format(css=css, body='<button type="button" class="menu-button">Go</button>'))
    assert "outline-none-no-focus-visible" not in ids


def test_a_focus_rule_that_only_removes_the_outline_is_still_reported():
    css = ".menu-button:focus-visible { outline: none; }"
    ids = _ids(PAGE.format(css=css, body='<button type="button" class="menu-button">Go</button>'))
    assert "outline-none-no-focus-visible" in ids


# ------------------------------------------------ a pseudo-element at opacity 0

def test_a_pseudo_element_at_opacity_zero_is_never_a_hidden_control():
    css = ".check::before { content: ''; opacity: 0; }"
    ids = _ids(PAGE.format(css=css, body='<input type="checkbox" class="check" aria-label="a">'))
    assert "focusable-at-opacity-zero" not in ids


def test_a_control_at_opacity_zero_is_still_reported():
    css = ".check { opacity: 0; }"
    ids = _ids(PAGE.format(css=css, body='<input type="checkbox" class="check" aria-label="a">'))
    assert "focusable-at-opacity-zero" in ids


# ------------------------------------------------ review: what still counts as no indicator

import pytest  # noqa: E402


@pytest.mark.parametrize("css", [
    ".m:focus-visible { outline: none; background: transparent; }",
    ".m:focus-visible{outline:none;background:transparent}",
    ".m:focus-visible { outline: none; text-decoration: none; }",
    ".m:focus-visible { outline: none; color: inherit; }",
    ".m:focus-visible { outline: none; background-color: #0000; }",
    ".m:focus-visible { outline: none; background-color: rgba(0, 0, 0, 0); }",
    ".m:focus-visible { outline: none; background-color: var(--x, transparent); }",
    ".m:focus-visible { outline: none; background-color: var(--undefined); }",
])
def test_a_clear_or_unreadable_fill_is_no_focus_indicator(css):
    ids = _ids(PAGE.format(css=css, body='<button type="button" class="m">Go</button>'))
    assert "outline-none-no-focus-visible" in ids, css


def test_a_fill_through_a_defined_custom_property_is_an_indicator():
    css = (":root { --accent: #dbe4ff; }\n"
           ".m:focus-visible { outline: none; background-color: var(--accent); }")
    ids = _ids(PAGE.format(css=css, body='<button type="button" class="m">Go</button>'))
    assert "outline-none-no-focus-visible" not in ids


def test_a_fill_in_a_separate_focus_rule_covers_the_removal():
    css = (".m:focus-visible { outline: none; }\n"
           ".m:focus-visible { background-color: #dbe4ff; }")
    ids = _ids(PAGE.format(css=css, body='<button type="button" class="m">Go</button>'))
    assert "outline-none-no-focus-visible" not in ids


@pytest.mark.parametrize("css", ["my-el::part(button) { opacity: 0; }",
                                 "::slotted(a) { opacity: 0; }"])
def test_part_and_slotted_select_real_elements(css):
    assert "focusable-at-opacity-zero" in _ids(css, "widget.css"), css


def test_a_shadow_held_in_a_custom_property_counts_its_layers():
    five = "0 1px 1px #0001, 0 2px 2px #0001, 0 4px 4px #0001, 0 8px 8px #0001, 0 16px 16px #0001"
    css = f":root {{ --elev: {five}; }}\n.c {{ box-shadow: var(--elev); }}"
    ids = _ids(PAGE.format(css=css, body='<div class="c"><p>a</p></div>'))
    assert "box-shadow-multilayer-default" in ids
    one = [f"--e{i}: 0 {i}px {i}px #0001;" for i in range(1, 6)]
    css = (":root { " + " ".join(one) + " }\n"
           ".c { box-shadow: var(--e1), var(--e2), var(--e3), var(--e4), var(--e5); }")
    ids = _ids(PAGE.format(css=css, body='<div class="c"><p>a</p></div>'))
    assert "box-shadow-multilayer-default" in ids


def test_tailwinds_empty_shadow_layers_draw_nothing():
    css = (":root { --tw-inset-shadow: 0 0 #0000; --tw-inset-ring-shadow: 0 0 #0000;"
           " --tw-ring-offset-shadow: 0 0 #0000; --tw-ring-shadow: 0 0 #0000; }\n" + PLUMBING)
    ids = _ids(PAGE.format(css=css, body='<div class="shadow-sm"><p>a</p></div>'))
    assert "box-shadow-multilayer-default" not in ids


@pytest.mark.parametrize("sel", ["button:not(*:disabled)", "button:not(.x, :disabled)",
                                 "button:not( :disabled)"])
def test_every_negated_disabled_passes(sel):
    ids = _ids(PAGE.format(css=f"{sel} {{ cursor: pointer; }}",
                           body='<button type="button">Save</button>'))
    assert "cursor-pointer-on-disabled" not in ids, sel


def test_a_disabled_beside_a_negated_one_is_still_reported():
    css = "button:not(:disabled), a:disabled { cursor: pointer; }"
    ids = _ids(PAGE.format(css=css, body='<button type="button">Save</button>'))
    assert "cursor-pointer-on-disabled" in ids


def test_a_brace_in_a_quoted_selector_still_finds_its_rule():
    css = '@layer utilities { .rounded-2xl[data-a="{"] { border-radius: 1rem; } }'
    from pathlib import Path

    from engine.linter.core import FileContext
    from engine.linter.structure import rule_at
    from engine.linter.views import FileViews
    text = PAGE.format(css=css, body="<p>a</p>")
    ctx = FileContext(Path("page.html"), text, FileViews("page.html", text))
    view = ctx.views.get("css")
    block = rule_at(ctx, view, view.text.index(".rounded-2xl"))
    assert block is not None and block.selectors == ['.rounded-2xl[data-a="{"]']
