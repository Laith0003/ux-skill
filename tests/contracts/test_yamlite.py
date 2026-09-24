"""yamlite reads the YAML subset contracts use and refuses the rest by
line, with the fix."""
import pytest

from engine.contracts.yamlite import YamlError, loads

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
