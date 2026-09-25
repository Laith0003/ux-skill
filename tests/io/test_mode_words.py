"""One mode-word matcher for every importer: whole words only, and the
contrast and motion values (Standard, High, Reduced) read only where the
axis's own name is written beside them."""
import pytest

from engine import io
from engine.io import figma_in, markdown_in
from engine.io.mode_words import axis_of, words


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
])
def test_an_axis_is_named_by_whole_words(names, context, want):
    assert axis_of(names, context) == want


def test_both_importers_use_the_shared_matcher():
    assert markdown_in.axis_of is axis_of and figma_in.axis_of is axis_of
    assert io.axis_of is axis_of
