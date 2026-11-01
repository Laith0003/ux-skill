"""Every file in the contracts package and its tests is ASCII; anything
else is written as an escape such as \\u201c."""
from pathlib import Path

import engine.contracts

PACKAGE = Path(engine.contracts.__file__).parent
TESTS = Path(__file__).parent
ROOTS = (PACKAGE, TESTS)


def _files():
    return sorted(p for root in ROOTS for p in root.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts)


def test_the_package_and_tests_have_files_to_check():
    names = {p.name for p in _files()}
    assert {"__init__.py", "yamlite.py", "schema.py", "test_ascii.py",
            "test_schema.py"} <= names


def test_every_file_under_engine_contracts_and_tests_contracts_is_ascii():
    found = []
    for path in _files():
        for number, line in enumerate(path.read_bytes().split(b"\n"), 1):
            bad = [b for b in line if b > 0x7F]
            if bad:
                found.append(f"{path.parent.name}/{path.name} line {number}")
    assert found == [], f"non-ASCII bytes in {found}; write them as escapes such as \\u201c"
