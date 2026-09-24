"""yamlite reads the YAML subset contracts use and refuses the rest by
line, with the fix."""
import re

import pytest

from engine.contracts.yamlite import MAX_DEPTH, MAX_DIGITS, YamlError, loads

DOC = """\
# a contract-shaped document
name: button
status: experimental   # agents author here
count: 3
ratio: 4.5
criterion: "1.4.3"
flag: true
empty:
none: null
parts:
  - name: container
    rtlBehavior: logical
  - name: label
    rtlBehavior: logical
states: [default, hover, focus]
tokens:
  - {part: container, property: fill, role: color.action.primary, when: {emphasis: primary}}
  - {part: label, property: text, role: color.text.on-action}
copy:
  default:
  - Start with a verb
  - "Keep it short: one line"
  - it's plain text with an apostrophe
usage: {do: [one, two], dont: []}
provenance:
  figma:
    node: '12:345'
    lastVerified: 2026-09-25
  drift: []
"""


def test_reads_the_supported_subset():
    assert loads(DOC) == {
        "name": "button", "status": "experimental", "count": 3, "ratio": 4.5,
        "criterion": "1.4.3", "flag": True, "empty": None, "none": None,
        "parts": [{"name": "container", "rtlBehavior": "logical"},
                  {"name": "label", "rtlBehavior": "logical"}],
        "states": ["default", "hover", "focus"],
        "tokens": [{"part": "container", "property": "fill", "role": "color.action.primary",
                    "when": {"emphasis": "primary"}},
                   {"part": "label", "property": "text", "role": "color.text.on-action"}],
        "copy": {"default": ["Start with a verb", "Keep it short: one line",
                             "it's plain text with an apostrophe"]},
        "usage": {"do": ["one", "two"], "dont": []},
        "provenance": {"figma": {"node": "12:345", "lastVerified": "2026-09-25"}, "drift": []},
    }


NESTED = """\
variants:
  - name: emphasis
    values:
      - primary
      - secondary
    default: primary
  -
    name: intent
    values: [neutral, danger]
    default: neutral
a11y:
  cue: "the verb, and an icon # not a comment"
"""


def test_reads_blocks_nested_inside_list_items():
    assert loads(NESTED) == {
        "variants": [{"name": "emphasis", "values": ["primary", "secondary"],
                      "default": "primary"},
                     {"name": "intent", "values": ["neutral", "danger"], "default": "neutral"}],
        "a11y": {"cue": "the verb, and an icon # not a comment"}}


def test_matches_a_full_yaml_reader_on_the_subset():
    yaml = pytest.importorskip("yaml")
    assert loads(NESTED) == yaml.safe_load(NESTED)
    parsed = yaml.safe_load(DOC)
    # A full reader turns an unquoted date into a date object; yamlite keeps text.
    figma = parsed["provenance"]["figma"]
    figma["lastVerified"] = str(figma["lastVerified"])
    assert loads(DOC) == parsed


@pytest.mark.parametrize("text,expected", [
    ("a: 'it''s'", {"a": "it's"}),
    ('a: "say \\"hi\\"\\n"', {"a": 'say "hi"\n'}),
    ("a: ~", {"a": None}),
    ("a: -3", {"a": -3}),
    ("a: .5", {"a": 0.5}),
    ("a: 1.4.3", {"a": "1.4.3"}),
    ("a: x#y", {"a": "x#y"}),
    ("a: [ ]", {"a": []}),
    ("a: {}", {"a": {}}),
    ("a: [[1, 2], {b: c}]", {"a": [[1, 2], {"b": "c"}]}),
    ("a:\n- x\n- z", {"a": ["x", "z"]}),
    ("- a\n- b", ["a", "b"]),
    ("", None),
    ("# only a comment\n", None),
])
def test_scalars_and_shapes(text, expected):
    assert loads(text) == expected


@pytest.mark.parametrize("text,message", [
    ("a:\n\tb: c", "x.yaml line 2: a tab indents this line; indent with spaces"),
    ("a: &anchor x", "x.yaml line 1: '&anchor x' starts with '&', which marks an anchor, alias, "
                     "tag or multi-line text this reader does not support; quote the value or "
                     "keep it on one line"),
    ("a: |", "x.yaml line 1: '|' starts with '|'"),
    ("a: yes", "x.yaml line 1: the plain word 'yes' reads as a yes or no in other YAML readers; "
               "write true or false, or quote it as 'yes'"),
    ("a: b: c", "x.yaml line 1: 'b: c' holds ': ' inside a plain value; quote the value"),
    ("a: 1\na: 2", "x.yaml line 2: key 'a' appears twice in one map; keep one"),
    ("a: {b: 1, b: 2}", "x.yaml line 1: key 'b' appears twice in one {...} map; keep one"),
    ("a: [1, 2", "x.yaml line 1: a [...] list is not closed with ']'; close it on the same line"),
    ("a: 'open", "x.yaml line 1: a ' quote is never closed; close it on the same line"),
    ("---\na: 1", "x.yaml line 1: '---' is a document marker or directive; a contract is one "
                  "document, so remove the line"),
    ("a:\n  b: 1\n    c: 2", "x.yaml line 3: this line is indented deeper than the key before "
                           "it allows; line it up with its siblings"),
    ("a: 1\n- b", "x.yaml line 2: a '- item' sits among 'key: value' lines; put the list under "
                  "a key"),
    ("my key: 1", "x.yaml line 1: 'my key' is not a simple key; use letters, digits, '_', '.' "
                  "and '-', or quote it"),
    ("a: 1\nb:c", "x.yaml line 2: 'b:c' is not a 'key: value' line or a '- item' line; fix "
                  "its indentation or add the ':'"),
    ('a: "\\q"', "x.yaml line 1: '\\q' is not an escape this reader knows"),
    ("a: 'x' y", "x.yaml line 1: 'y' follows a complete value; remove it or quote the whole "
                 "value"),
    ("  a: 1", "x.yaml line 1: the first line is indented; start the document at the left edge"),
])
def test_refuses_what_it_does_not_support_by_line_with_the_fix(text, message):
    with pytest.raises(YamlError) as err:
        loads(text, source="x.yaml")
    assert str(err.value).startswith(message)


def test_refuses_a_non_string():
    with pytest.raises(TypeError, match="x.yaml is bytes; pass the YAML as text"):
        loads(b"a: 1", source="x.yaml")


def _block_maps(n):
    """n block maps, each nested under the key before it."""
    return "\n".join("  " * i + ("k:" if i < n - 1 else "k: 1") for i in range(n))


def _block_lists(n):
    """n block lists, each the only item of the one before it."""
    return "\n".join("  " * i + ("-" if i < n - 1 else "- 1") for i in range(n))


def _maps_then_flow(n):
    """n - 2 block maps whose last key holds two flow lists."""
    m = n - 2
    return "\n".join("  " * i + ("k:" if i < m - 1 else "k: [[1]]") for i in range(m))


@pytest.mark.parametrize("make", [
    lambda n: "[" * n + "]" * n,
    lambda n: "a: " + "[" * (n - 1) + "]" * (n - 1),
    lambda n: "{k: " * n + "1" + "}" * n,
    _block_maps,
    _block_lists,
    _maps_then_flow,
])
def test_nesting_is_capped_with_the_line_and_the_fix(make):
    assert MAX_DEPTH == 64
    loads(make(MAX_DEPTH), source="x.yaml")
    for depth in (MAX_DEPTH + 1, 500):
        with pytest.raises(YamlError) as err:
            loads(make(depth), source="x.yaml")
        assert re.fullmatch(r"x\.yaml line \d+: this value nests more than 64 lists and maps "
                            r"deep; flatten it", str(err.value)), str(err.value)


@pytest.mark.parametrize("text", [
    "a: " + "9" * (MAX_DIGITS + 1),
    "a: -" + "9" * (MAX_DIGITS + 1),
    "a: [" + "9" * 5000 + "]",
    "a: " + "1" * 400 + ".5",
    "a: 0." + "5" * 400,
])
def test_a_number_with_too_many_digits_is_refused_by_line(text):
    with pytest.raises(YamlError) as err:
        loads(text, source="x.yaml")
    message = str(err.value)
    assert message.startswith("x.yaml line 1: the number ") and message.endswith(
        f"has more than {MAX_DIGITS} digits; quote it if it is text, or shorten it")
    assert len(message) < 200


def test_the_longest_number_allowed_still_reads():
    assert loads("a: " + "9" * MAX_DIGITS) == {"a": int("9" * MAX_DIGITS)}
