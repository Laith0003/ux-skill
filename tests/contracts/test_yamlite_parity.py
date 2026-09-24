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


def _compare(yaml, documents):
    counts = {"same": 0, "refused": 0}
    wrong = []
    for doc in documents:
        try:
            ours = loads(doc)
        except YamlError:
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
