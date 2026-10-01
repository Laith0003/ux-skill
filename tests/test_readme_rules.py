"""The README's rule catalogue is generated from data/anti-patterns.json, so
the count and the tables cannot drift from the rules the linter runs."""
import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
RULES = json.loads((ROOT / "data" / "anti-patterns.json").read_text(encoding="utf-8"))["entries"]

_spec = importlib.util.spec_from_file_location("readme_rules", ROOT / "scripts" / "readme_rules.py")
readme_rules = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(readme_rules)

CATEGORIES = {"A11y", "Color", "Content", "Depth", "Layout", "Motion", "Performance",
              "Quality", "Typography", "Visual"}


def test_every_rule_sits_in_a_known_category():
    unknown = sorted({r["category"] for r in RULES} - CATEGORIES)
    assert not unknown, f"category {unknown} is not one of {sorted(CATEGORIES)}; use one of those"


def test_the_readme_tables_match_the_rules():
    start, end = readme_rules.START, readme_rules.END
    assert start in README and end in README
    block = README[README.index(start) + len(start):README.index(end)]
    assert block == readme_rules.render(RULES), "run python scripts/readme_rules.py"


def test_every_rule_is_listed_once_in_the_readme():
    start, end = readme_rules.START, readme_rules.END
    block = README[README.index(start) + len(start):README.index(end)]
    ids = re.findall(r"^\| \w+ \| `([^`]+)` \|", block, re.M)
    assert sorted(ids) == sorted(r["id"] for r in RULES)


@pytest.mark.parametrize("change,message", [
    ({"severity": "info"}, "rule demo-rule has severity 'info'; use one of critical, high, "
                           "medium, low"),
    ({"category": None}, "rule demo-rule has no category; give it a category as text"),
    ({"name": ""}, "rule demo-rule has no name; give it a name as text"),
])
def test_a_rule_the_catalogue_cannot_place_is_named_with_the_fix(change, message):
    rule = {"id": "demo-rule", "name": "Demo", "category": "Color", "severity": "low", **change}
    with pytest.raises(ValueError) as exc:
        readme_rules.render([rule])
    assert str(exc.value) == f"data/anti-patterns.json: {message}"


def test_the_readme_states_the_rule_count_and_no_other():
    n = len(RULES)
    assert f"badge/anti--patterns-{n}-" in README
    assert f"## The {n} anti-AI-slop rules" in README
    # The notes on earlier releases state the count each one shipped with.
    current = README[:README.index("### New in v3.1")] + README[README.index("## What is ux-skill"):]
    stale = sorted(set(re.findall(r"\b(\d{3}) (?:deterministic |regex |anti-pattern )*rules\b",
                                  current)) - {str(n)})
    assert not stale, f"the README states {stale} rules; the linter runs {n}"


def test_the_category_counts_match_the_rules():
    cover = readme_rules.coverage(RULES)
    assert f"Rules cover {cover}." in README
    assert f"| `categories` | {cover} |" in README
    assert f"| `entries` | {len(RULES)} |" in README
