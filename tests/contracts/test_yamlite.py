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
    ("a: 0.5", {"a": 0.5}),
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


@pytest.mark.parametrize("text,expected", [
    ("'my key': 1", {"my key": 1}),
    ('"a": 1\nb: 2', {"a": 1, "b": 2}),
    ("'': 1", {"": 1}),
    ("'a b':\n  c: d", {"a b": {"c": "d"}}),
    ("'it''s': x", {"it's": "x"}),
    ('"a: b": [1]', {"a: b": [1]}),
    ("- 'a b': 1\n  c: 2", [{"a b": 1, "c": 2}]),
    ('- "x": [1]\n- z', [{"x": [1]}, "z"]),
    ("k:\n  - 'a b': 1", {"k": [{"a b": 1}]}),
    ("'just text'", "just text"),
    ('"a: b"', "a: b"),
    ("- 'x'\n- \"a: b\"", ["x", "a: b"]),
])
def test_a_quoted_key_works_on_every_line(text, expected):
    assert loads(text) == expected


@pytest.mark.parametrize("plain,quoted", [
    ("my key: 1", "'my key': 1"),
    ("a:\n  b: 1\n  my key: 2", "a:\n  b: 1\n  'my key': 2"),
    ("- my key: 1", "- 'my key': 1"),
    ("a: {my key: 1}", "a: {'my key': 1}"),
])
def test_the_advice_for_a_key_that_is_not_simple_works(plain, quoted):
    with pytest.raises(YamlError, match="is not a simple key; use letters, digits, '_', '.' "
                                        "and '-', or quote it"):
        loads(plain)
    assert loads(quoted)


# Plain values a YAML 1.1 reader (PyYAML) or a YAML 1.2 reader (core schema)
# types as a number, a date and time or a special value. yamlite refuses each
# rather than reading it another way, and the quoted form reads as text.
OTHER_READINGS = [
    "1:23", "12:30", "190:20:30", "-1:23", "1:30.5", "1_0:30",
    "012", "09", "00", "-012", "+07", "0_1",
    "0x10", "-0x1", "0o17", "0b101", "0x_1",
    "1_000", "1_000.5", "1_", "+1_0", "1_0e+3", "-_1", "+_",
    ".inf", "-.inf", "+.Inf", ".INF", ".nan", ".NaN", ".NAN",
    "1e3", "1E3", "1.5e3", "1.5e+3", "1.5e-3", "-1e-3", "1.e+3",
    ".5", "-.5", "+.5", ".5e3", "._", "._5",
    "2026-09-25T10:00:00Z", "2026-09-25 10:00:00", "2026-9-5t1:02:03.5",
    "=", "<<",
]


@pytest.mark.parametrize("value", OTHER_READINGS)
@pytest.mark.parametrize("template", ["a: {}", "- {}", "a: [{}]", "a: {{k: {}}}", "{}"])
def test_a_value_other_readers_type_differently_is_refused_by_line(value, template):
    with pytest.raises(YamlError) as err:
        loads(template.format(value), source="x.yaml")
    message = str(err.value)
    assert message.startswith(f"x.yaml line 1: the plain value {value!r} reads as "), message
    assert " in other YAML readers; quote it" in message
    assert loads("a: '" + value + "'") == {"a": value}


@pytest.mark.parametrize("value,expected", [
    ("0", 0), ("-0", 0), ("+5", 5), ("1500", 1500), ("0.5", 0.5), ("-1.25", -1.25),
    ("1.", 1.0), ("00.5", 0.5), ("1.4.3", "1.4.3"), ("2026-09-25", "2026-09-25"),
    ("12px", "12px"), ("100%", "100%"), ("v2", "v2"), ("e3", "e3"), ("inf", "inf"),
    ("_", "_"), ("_1", "_1"), ("0X1F", "0X1F"), ("-x", "-x"), ("x:y", "x:y"), ("a?b", "a?b"),
    ("x[1]", "x[1]"),
])
def test_values_every_reader_types_alike_still_read(value, expected):
    assert loads(f"a: {value}") == {"a": expected}


@pytest.mark.parametrize("text,line,start", [
    ("- - a", 1, "'- a' starts with '- '"),
    ("k:\n  -   - c", 2, "'- c' starts with '- '"),
    ("a: - b", 1, "'- b' starts with '- '"),
    ("a: -", 1, "'-' starts with '- '"),
    ("- -", 1, "'-' starts with '- '"),
    ("- a: - b", 1, "'- b' starts with '- '"),
])
def test_a_list_opened_on_the_line_of_another_is_refused(text, line, start):
    with pytest.raises(YamlError) as err:
        loads(text, source="x.yaml")
    assert str(err.value) == (
        f"x.yaml line {line}: {start}, which other YAML readers read as a list inside this "
        "one; put the list on its own lines, one '- item' each, or quote the value")


@pytest.mark.parametrize("text,message", [
    ("a: [?q]", "'?q' starts with '?', which marks a key in other YAML readers; quote the value"),
    ("a: [? q]", "'? q' starts with '?'"),
    ("a: {k: ?q}", "'?q' starts with '?'"),
    ("a: ? b", "'? b' starts with '?'"),
    ("a: [:b]", "':b' starts with ':'"),
    ("a: ]", "']' starts with ']', which YAML keeps for [...] and {...}; quote the value"),
    ("a: }x", "'}x' starts with '}'"),
    ("a: ,x", "',x' starts with ','"),
    ("a: [a?b]", "'a?b' holds '?', which ends a plain value inside [...] or {...} in other "
                 "YAML readers; quote the value"),
    ("a: {k: b]}", "'b]' holds ']'"),
    ("a: [b}]", "'b}' holds '}'"),
    ("a: [x:]", "'x:' holds ': ' inside a plain value"),
    ("a: {k:b}", "key 'k' in a {...} map needs a space after its ':'; write k: value"),
    ("a:\tb", "a tab sits outside quotes; use spaces, or put the text in quotes"),
    ("a: b\t# c", "a tab sits outside quotes"),
    ("- \ta", "a tab sits outside quotes"),
    ("on: 1", "the key 'on' reads as a yes or no in other YAML readers; quote it as 'on'"),
    ("null: 1", "the key 'null' reads as null in other YAML readers; quote it as 'null'"),
    ("True: 1", "the key 'True' reads as true or false in other YAML readers; quote it as "
                "'True'"),
    ("a: {yes: 1}", "the key 'yes' reads as a yes or no"),
    ("- n: 1", "the key 'n' reads as a yes or no"),
    ("a : 1", "key 'a' has a space before its ':'; remove the space"),
])
def test_other_forms_yaml_reads_differently_are_refused(text, message):
    with pytest.raises(YamlError) as err:
        loads(text, source="x.yaml")
    assert str(err.value).startswith("x.yaml line 1: " + message), str(err.value)


@pytest.mark.parametrize("text,expected", [
    ("a: 'b\tc'", {"a": "b\tc"}),
    ("a: \"?q\"", {"a": "?q"}),
    ("'on': 1", {"on": 1}),
    ("a: {'yes': 1, 'k': '12:30'}", {"a": {"yes": 1, "k": "12:30"}}),
    ("\ufeffa: 1", {"a": 1}),
    ("a: 1\r\nb: 2\rc: 3", {"a": 1, "b": 2, "c": 3}),
])
def test_quoting_and_line_ends_read_as_other_readers_read_them(text, expected):
    assert loads(text) == expected


@pytest.mark.parametrize("char", ["\x00", "\x07", "\x0b", "\x0c", "\x1b", "\x7f", "\x85",
                                  "\u2028", "\u2029", "\ufeff"])
def test_a_control_character_is_refused_by_line(char):
    with pytest.raises(YamlError) as err:
        loads(f"a: 1\nb: x{char}y\nc: 2", source="x.yaml")
    assert str(err.value) == (
        f"x.yaml line 2: character U+{ord(char):04X} is a control character or a line "
        "separator; remove it")


# YAML 1.2 core schema: integers and floats (the spec's regular expressions).
_CORE_12 = re.compile(r"[-+]?[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+|[-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)"
                      r"([eE][-+]?[0-9]+)?|[-+]?\.(inf|Inf|INF)|\.(nan|NaN|NAN)")


@pytest.mark.parametrize("value", OTHER_READINGS)
def test_each_refused_value_is_typed_by_another_reader(value):
    """A refusal is never arbitrary: PyYAML types the value, or the YAML 1.2
    core schema does, or it is a number with '_', which 1.1 and some 1.2
    readers accept."""
    yaml = pytest.importorskip("yaml")
    try:
        read = yaml.safe_load("a: " + value)["a"]
    except yaml.YAMLError:
        read = None
    assert read != value or _CORE_12.fullmatch(value) or "_" in value, value


# A quote is a quoted scalar only where a value starts. Inside a plain value
# it is a character, so a ' #' after it still starts a comment.
QUOTE_INSIDE_PLAIN = [
    ('- Say "Item #3" in the title', ['Say "Item']),
    ("a: x 'y # z'", {"a": "x 'y"}),
    ("a: b,'c # d'", {"a": "b,'c"}),
    ("a: x 'y", {"a": "x 'y"}),
    ('a: Order "#1234"', {"a": 'Order "#1234"'}),
    ("a: it's # a note", {"a": "it's"}),
    ("a: [x, 'y # z'] # c", {"a": ["x", "y # z"]}),
    ("a: {k: 'v # w', 'j # 2': u}", {"a": {"k": "v # w", "j # 2": "u"}}),
    ("- 'a # b'\n- [\"c # d\"]", ["a # b", ["c # d"]]),
    ("'k # 1': v # c", {"k # 1": "v"}),
    ("a:\n  - x \"y\" # z", {"a": ['x "y"']}),
]


@pytest.mark.parametrize("text,expected", QUOTE_INSIDE_PLAIN)
def test_a_quote_inside_a_plain_value_is_text_and_a_comment_still_starts(text, expected):
    assert loads(text) == expected


@pytest.mark.parametrize("text,expected", QUOTE_INSIDE_PLAIN)
def test_a_quote_inside_a_plain_value_reads_as_pyyaml_reads_it(text, expected):
    yaml = pytest.importorskip("yaml")
    assert yaml.safe_load(text) == expected


def test_a_tab_after_a_quote_inside_a_plain_value_is_refused():
    with pytest.raises(YamlError, match="line 1: a tab sits outside quotes"):
        loads('a: x "y\tz"')


# Only the space character is trimmed at the edges of a plain value; other
# readers keep a no-break or ideographic space, so yamlite keeps it too.
UNICODE_SPACES = [
    ("a: b\u00a0", {"a": "b\u00a0"}),
    ("a: \u00a0b", {"a": "\u00a0b"}),
    ("a: [\u3000b]", {"a": ["\u3000b"]}),
    ("a: [b\u2003, c]", {"a": ["b\u2003", "c"]}),
    ("a: b\u202f # c", {"a": "b\u202f"}),
    ("- \u1680x\u205f", ["\u1680x\u205f"]),
    ("a: {k: \u205fv}", {"a": {"k": "\u205fv"}}),
    ("a: x\u200b", {"a": "x\u200b"}),
]


@pytest.mark.parametrize("text,expected", UNICODE_SPACES)
def test_a_unicode_space_at_the_edge_of_a_plain_value_is_kept(text, expected):
    assert loads(text) == expected


@pytest.mark.parametrize("text,expected", UNICODE_SPACES)
def test_a_unicode_space_reads_as_pyyaml_reads_it(text, expected):
    yaml = pytest.importorskip("yaml")
    assert yaml.safe_load(text) == expected


@pytest.mark.parametrize("text", ["a: [#]", "a: [a,#b]", "a: {k: [#]}"])
def test_a_flow_value_starting_with_a_hash_is_refused(text):
    with pytest.raises(YamlError, match="line 1: '#.*' starts with '#', which starts a comment "
                                        "in other YAML readers; quote the value"):
        loads(text)


@pytest.mark.parametrize("text,line", [
    ("'a' : 1", 1), ("b: 2\n'a b' : 1", 2), ("- 'a' : 1", 1), ('- "a"  : 1', 1),
])
def test_a_space_between_a_quoted_key_and_its_colon_is_named(text, line):
    with pytest.raises(YamlError) as err:
        loads(text, source="x.yaml")
    assert str(err.value).startswith(f"x.yaml line {line}: key ")
    assert str(err.value).endswith("has a space before its ':'; remove the space")
