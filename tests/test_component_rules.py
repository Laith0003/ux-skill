"""Edge cases of the component rules that the review found: which hidden
control a hover reveals, which controls open a menu, focus-within as a
reveal, transition classes by their framework spelling, and JSX values."""
import pytest

from engine.linter.core import lint_text


def _ids(text, name="page.css"):
    return {f.rule_id for f in lint_text(name, text)}


def test_a_hidden_control_revealed_inside_its_card_is_still_a_hover_reveal():
    css = ".actions { opacity: 0; }\n.card:hover .actions { opacity: 1; }\n"
    assert "hover-only-card-actions" in _ids(css)


@pytest.mark.parametrize("cls", ["read-more", "menu-card", "overflow-x"])
def test_a_name_that_only_contains_menu_words_opens_no_menu(cls):
    css = (f".card .{cls} {{ opacity: 0; }}\n.card:hover .{cls} {{ opacity: 1; }}\n"
           f".card:focus-within .{cls} {{ opacity: 1; }}\n"
           f"@media (hover: none) {{ .card .{cls} {{ opacity: 1; }} }}\n")
    assert "hover-only-card-actions" not in _ids(css)


def test_a_menu_trigger_still_needs_its_open_state():
    css = (".card .more-menu { opacity: 0; }\n.card:hover .more-menu { opacity: 1; }\n"
           ".card:focus-within .more-menu { opacity: 1; }\n"
           "@media (hover: none) { .card .more-menu { opacity: 1; } }\n")
    assert "hover-only-card-actions" in _ids(css)


def test_focus_within_on_the_container_is_a_reveal():
    css = ".toolbar .menu { opacity: 0; }\n.toolbar:focus-within .menu { opacity: 1; }\n"
    assert "focusable-at-opacity-zero" not in _ids(css)


@pytest.mark.parametrize("sel", [".text-center .btn", ".exit-button", ".presenter .menu",
                                 ".appearance-panel .btn"])
def test_ordinary_names_are_not_transition_classes(sel):
    assert "focusable-at-opacity-zero" in _ids(f"{sel} {{ opacity: 0; }}\n")


@pytest.mark.parametrize("sel", [".fade-enter-from .btn", ".fade-leave-to .btn",
                                 ".modal-exit-active .btn", ".v-enter .menu"])
def test_framework_transition_classes_are_skipped(sel):
    assert "focusable-at-opacity-zero" not in _ids(f"{sel} {{ opacity: 0; }}\n")


def test_jsx_values_of_disabled_and_aria_disabled_are_read():
    tsx = ('export const M = () => (<ul role="menu">\n'
           '<li><button role="menuitem" disabled={false}>Rename</button></li>\n'
           '<li role="menuitem" aria-disabled={true}>Archive</li>\n</ul>);\n')
    lines = [f.line for f in lint_text("menu.tsx", tsx)
             if f.rule_id == "menu-row-disabled-without-reason"]
    assert lines == [3]
