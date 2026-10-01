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
