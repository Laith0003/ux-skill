"""yamlite may refuse a document, but it never reads one differently from a
full YAML reader. A seeded generator writes documents over the subset and
over the forms at its edges; each either reads exactly as PyYAML reads it
or raises YamlError. The one allowed difference is documented: an unquoted
date such as 2026-09-25 reads as text, where PyYAML returns a date."""
import datetime
import random

import pytest

from engine.contracts.yamlite import YamlError, loads

DOCUMENTS = 2000
SEED = 20260925

WORDS = [
    "button", "color.action.primary", "label", "leading-icon", "x", "primary", "a_b", "1.4.3",
    "it's", "Start with a verb", "one two three", "x#y", "v2", "-x", "path/to/file", "100%",
    "\u0645\u0631\u062d\u0628\u0627", "12px", "e3", "inf", "_", "_1", "0X1F", "a?b", "x[1]",
    "x:y", "x,y", "x}y", "a - b", "http://x.y/z", "1.", "00.5", "0.5", "-1.25", "+5", "-0",
    "0", "1500", "2026-09-25", "---", "tRUE", "nULL",
    # a quote inside a plain value is text, and a ' #' after it is a comment
    'Say "Item #3" now', "x 'y # z'", "b,'c # d'", "x 'y", 'Order "#1234"', "it's # note",
    # other readers keep a Unicode space at the edge of a plain value
    "b\u00a0", "\u00a0b", "\u3000x", "x\u2003", "\u202fx\u205f",
]
EDGES = [
    "1:23", "12:30", "-1:23", "1:30.5", "012", "09", "00", "+07", "0x10", "0o17", "0b101",
    "1_000", "1_", "1_000.5", ".inf", "-.inf", ".NaN", ".nan", "1e3", "1.5e3", "1.5e+3",
    "-1e-3", ".5", "-.5", "+.5", "._", "2026-09-25T10:00:00Z", "2026-09-25 10:00:00", "=",
    "<<", "?q", "? q", ":b", "- a", "-", ",x", "]", "}x", "x:", "a: b", "yes", "No", "on",
    "OFF", "y", "N", "null", "Null", "~", "true", "False", "TRUE", "&a", "*a", "!t", "|", ">",
    "%x", "@x", "`x", "[#]", "#x",
]
QUOTED = ["a: b", "# not", "[x]", "{y}", "yes", "12:30", "012", "?q", "- a", "", "it's",
          "tab\there", "1e3", ".inf", "on"]
KEYS = ["name", "role", "part", "rtlBehavior", "a", "b_c", "x.y", "k-1", "values", "default"]
ODD_KEYS = ["'my key'", '"a: b"', "''", "on", "null", "True", "y", "my key", "a b", "1",
            "'on'", '"12:30"', "a ", "-k", "k:v"]


class _Gen:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.edges = 0.0  # how often a scalar, key or value is an edge form

    def scalar(self, flow):
        rng = self.rng
        if rng.random() < self.edges:
            return rng.choice(EDGES)
        k = rng.randrange(10)
        if k == 0:
            return rng.choice(["null", "~", "true", "false", "True"])
        if k == 1:
            return str(rng.randint(-500, 5000))
        if k == 2:
            return f"{rng.randint(0, 99)}.{rng.randint(0, 99)}"
        if k == 3:
            return "'" + rng.choice(QUOTED + WORDS).replace("'", "''") + "'"
        if k == 4:
            return '"' + rng.choice(["a: b", 'say \\"hi\\"', "tab\\there", "# x", "no", "\\/",
                                     "12:30", "?q"]) + '"'
        word = rng.choice(WORDS)
        if flow and rng.random() < 0.7 and any(c in word for c in ",[]{}# '"):
            word = "plain"
        return word

    def key(self):
        return self.rng.choice(ODD_KEYS if self.rng.random() < self.edges else KEYS)

    def flow(self, depth):
        rng = self.rng
        r = rng.random()
        if depth > 2 or r < 0.5:
            return self.scalar(True)
        if r < 0.75:
            return "[" + ", ".join(self.flow(depth + 1) for _ in range(rng.randint(0, 3))) + "]"
        keys = rng.sample(KEYS, rng.randint(0, 3))
        sep = ":" if rng.random() < self.edges / 2 else ": "
        return "{" + ", ".join(f"{k}{sep}{self.flow(depth + 1)}" for k in keys) + "}"

    def value(self):
        v = self.flow(0)
        r = self.rng.random()
        if r < 0.1:
            v += " # c"
        elif r < 0.1 + self.edges / 2:
            v = self.rng.choice(["- " + v, "-   - " + v, "\t" + v, v + "\t# c", "? " + v])
        return v

    def block(self, indent, depth, lines):
        rng = self.rng
        if depth > 3 or rng.random() < 0.3:
            return
        if rng.random() < 0.6:
            for k in rng.sample(KEYS, rng.randint(1, 4)):
                if rng.random() < self.edges:
                    k = rng.choice(ODD_KEYS)
                if rng.random() < 0.5:
                    lines.append(" " * indent + f"{k}: {self.value()}")
                else:
                    lines.append(" " * indent + f"{k}:")
                    if rng.random() < 0.3:
                        self.seq(indent, depth + 1, lines)
                    else:
                        self.block(indent + rng.choice([2, 4]), depth + 1, lines)
        else:
            self.seq(indent, depth, lines)

    def seq(self, indent, depth, lines):
        rng = self.rng
        for _ in range(rng.randint(1, 3)):
            r = rng.random()
            if r < 0.45 or depth > 3:
                lines.append(" " * indent + "- " + self.value())
            elif r < 0.45 + self.edges:
                lines.append(" " * indent + rng.choice(["- - ", "-   - ", "- -"]) +
                             self.scalar(False))
            elif r < 0.8:
                keys = [self.key() for _ in range(rng.randint(1, 3))]
                lines.append(" " * indent + f"- {keys[0]}: {self.value()}")
                for k in keys[1:]:
                    lines.append(" " * (indent + 2) + f"{k}: {self.value()}")
            else:
                lines.append(" " * indent + "-")
                self.block(indent + 2, depth + 1, lines)

    def document(self):
        rng = self.rng
        # A third of the documents keep to the subset; the rest reach its edges.
        self.edges = rng.choice([0.0, 0.03, 0.12])
        lines = []
        while not lines:
            r = rng.random()
            if r < 0.1:
                lines.append(self.value())
            elif r < 0.5:
                for _ in range(rng.randint(1, 4)):
                    lines.append(f"{self.key()}: {self.value()}")
            self.block(0, 0, lines)
        return "\n".join(lines) + "\n"


def _dates_as_text(value):
    if isinstance(value, dict):
        return {k: _dates_as_text(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_dates_as_text(v) for v in value]
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def _compare(yaml, documents, strict=False):
    """Each document read by both readers. A refusal counts as agreement
    unless `strict`: then only when PyYAML refuses the document too, for
    the forms yamlite reads in full, such as block text."""
    counts = {"same": 0, "refused": 0}
    wrong = []
    for doc in documents:
        try:
            ours = loads(doc)
        except YamlError as exc:
            if strict:
                try:
                    theirs = yaml.safe_load(doc)
                except yaml.YAMLError:
                    pass
                else:
                    wrong.append((doc, f"yamlite refused it ({exc}); PyYAML read {theirs!r}"))
                    continue
            counts["refused"] += 1
            continue
        except Exception as exc:  # noqa: BLE001  any other error is reported as a failure
            wrong.append((doc, f"raised {type(exc).__name__}: {exc}"))
            continue
        try:
            theirs = _dates_as_text(yaml.safe_load(doc))
        except yaml.YAMLError as exc:
            wrong.append((doc, f"yamlite read {ours!r}; PyYAML refused it: {exc}"))
            continue
        if ours == theirs and repr(ours) == repr(theirs):
            counts["same"] += 1
        else:
            wrong.append((doc, f"yamlite read {ours!r}; PyYAML read {theirs!r}"))
    return counts, wrong


def test_every_generated_document_reads_as_pyyaml_reads_it_or_is_refused():
    yaml = pytest.importorskip("yaml")
    gen = _Gen(SEED)
    documents = [gen.document() for _ in range(DOCUMENTS)]
    counts, wrong = _compare(yaml, documents)
    assert wrong == [], wrong[:5]
    # Not vacuous: most documents read, and the edges are refused.
    assert counts["same"] >= DOCUMENTS // 3 and counts["refused"] >= DOCUMENTS // 4, counts


def test_an_unquoted_date_is_the_one_documented_difference():
    yaml = pytest.importorskip("yaml")
    assert loads("a: 2026-09-25") == {"a": "2026-09-25"}
    assert yaml.safe_load("a: 2026-09-25") == {"a": datetime.date(2026, 9, 25)}


def test_spaces_past_a_block_indent_are_text_as_pyyaml_reads_them():
    yaml = pytest.importorskip("yaml")
    documents = [
        "a: |\n  x\n    \n  y\n", "a: |\n  x\n   \n  y\n", "a: |\n  x\n  y\n    \n",
        "a: |+\n  x\n    \nb: 1\n", "a: >\n  x\n    \n  y\n", "a: |-\n  x\n     \n  y\n   \n",
        "- |\n  x\n    \n  y\n", "a: |\n  x\n\n  y\n",
    ]
    counts, wrong = _compare(yaml, documents, strict=True)
    assert wrong == [] and counts["same"] == len(documents)


def _block_documents(seed, count):
    """Block text over its edges: lines of spaces longer and shorter than
    the indentation, before, among and after the text, every header, and a
    document that ends with or without a final line break."""
    rng = random.Random(seed)
    heads = ["", "-", "+", "1", "2", "2-", "+3"]
    places = {"a: ": 2, "- ": 2, "- a: ": 4, "k:\n  a: ": 4}
    out = []
    for _ in range(count):
        place = rng.choice(sorted(places))
        indent = places[place]
        lines = []
        for _ in range(rng.randint(1, 5)):
            if rng.random() < 0.4:
                lines.append(" " * (indent + rng.choice([0, 0, 1, 2])) + rng.choice(["x", "y z"]))
            else:
                lines.append(" " * rng.randint(0, indent + 4))
        tail = rng.choice(["\n", "", "\nb: 1\n" if place == "a: " else "\n"])
        out.append(place + rng.choice("|>") + rng.choice(heads) + "\n" + "\n".join(lines)
                   + tail)
    return out


def test_block_text_reads_as_pyyaml_reads_it_or_is_refused():
    yaml = pytest.importorskip("yaml")
    named = [
        # A line of spaces longer than the indentation keeps its spaces past it.
        "a: |\n  x\n    \n", "a: |+\n  x\n   \n", "a: >+\n  x\n   \n",
        # The last line has no line break after it, so the text has none.
        "a: |\n  x\n    ", "- |\n  x", "- |1\n  ",
        # Keep chomping keeps the breaks there are, and no more.
        "a: |+\n", "a: |+\n\n", "- |+\n \n",
        # Block text that ends the document with no final line break is read once.
        "a: |\n  x", "- |\n  x", "a: >\n  x", "k:\n  a: |\n    x", "a: |\n  x\n  y",
    ]
    counts, wrong = _compare(yaml, named + _block_documents(SEED, 3000), strict=True)
    assert wrong == [], wrong[:5]
    assert counts["same"] >= 1500, counts


def test_a_blank_line_deeper_than_the_first_line_of_block_text_is_refused():
    # Every YAML reader refuses it: the first line of text sets the indent.
    with pytest.raises(YamlError, match=r"line 2: this line of spaces before the block text "
                                        r"holds more spaces than its first line"):
        loads("a: |\n    \n  x\n", "c.yaml")


def test_a_long_document_of_block_texts_reads_in_time():
    import time
    doc = "".join(f"k{i}: |\n  line {i}\n" for i in range(20000))
    start = time.perf_counter()
    assert loads(doc)["k3999"] == "line 3999\n"
    # Each block reads to its own end, never through the rest of the file.
    assert time.perf_counter() - start < 2
