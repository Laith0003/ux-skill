"""One mode-word matcher for every importer: whole words only, and the
contrast and motion values (Standard, High, Reduced) read only where the
axis's own name is written beside them."""
import pytest

from engine import io
from engine.io import adapter, dtcg_in, figma_in, markdown_in
from engine.io.mode_words import axis_of, is_base, mode_of, words


def test_words_are_whole_and_split_at_camel_case():
    assert words("darkMode") == {"dark", "mode"}
    assert words("High-contrast (AA)") == {"high", "contrast", "aa"}
    assert words("Darkness") == {"darkness"}


@pytest.mark.parametrize("names, context, want", [
    (["Light", "Dark"], [], ("scheme", 0)),
    (["Dark mode", "Light mode"], [], ("scheme", 1)),
    (["Dark"], [], ("scheme", -1)),
    (["Standard", "High"], [], None),
    (["Standard", "High"], ["Contrast"], ("contrast", 0)),
    (["Standard", "High contrast"], [], ("contrast", 0)),
    (["High"], [], None),
    (["High contrast"], [], ("contrast", -1)),
    (["Standard", "Reduced"], [], None),
    (["Standard", "Reduced"], ["Motion"], ("motion", 0)),
    (["Reduced motion"], [], ("motion", -1)),
    (["Comfortable", "Compact"], [], ("density", 0)),
    (["Light", "Darkness"], [], None),
    (["Highlight"], ["contrast"], None),
    (["Lightness", "Dark"], [], None),
    # A base word (default, base, value, standard) stands opposite a
    # non-base value as that axis's base.
    (["Default", "Dark"], [], ("scheme", 0)),
    (["Dark", "Default"], [], ("scheme", 1)),
    (["Value", "Dark"], [], ("scheme", 0)),
    (["Base", "Compact"], [], ("density", 0)),
    (["Standard", "Dark mode"], [], ("scheme", 0)),
    (["Default", "High"], ["Contrast"], ("contrast", 0)),
    (["Default", "High"], [], None),
    (["Default", "Base"], [], None),
    # The words the CSS media queries use for the non-base values.
    (["Base", "Reduce"], ["data-motion"], ("motion", 0)),
    (["Base", "More"], ["data-contrast"], ("contrast", 0)),
])
def test_an_axis_is_named_by_whole_words(names, context, want):
    assert axis_of(names, context) == want


@pytest.mark.parametrize("name, context, want", [
    ("Dark", [], "scheme"), ("High contrast", [], "contrast"), ("High", [], None),
    ("High", ["Contrast"], "contrast"), ("Light", [], None), ("Default", [], None),
    ("Brand", [], None), ("Reduced motion", [], "motion"),
])
def test_one_name_places_into_the_axis_whose_non_base_value_it_is(name, context, want):
    assert mode_of(name, context) == want


@pytest.mark.parametrize("name, want", [
    ("Light", True), ("Default", True), ("Value", True), ("Base", True), ("Standard", True),
    ("LTR", True), ("Light (default)", True), ("Dark", False), ("Dark (default)", False),
    ("Brand", False),
])
def test_a_base_name_is_a_base_value_or_a_base_word(name, want):
    assert is_base(name) is want


def test_every_importer_and_the_adapter_use_the_shared_matcher():
    assert dtcg_in.axis_of is axis_of and adapter.axis_of is axis_of


def test_both_importers_use_the_shared_matcher():
    assert markdown_in.axis_of is axis_of and figma_in.axis_of is axis_of
    assert io.axis_of is axis_of
