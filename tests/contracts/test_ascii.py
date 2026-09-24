"""Every file in the contracts package is ASCII; anything else is written
as an escape such as \\u201c."""
from pathlib import Path

import engine.contracts

PACKAGE = Path(engine.contracts.__file__).parent


def _files():
    return sorted(p for p in PACKAGE.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts)


def test_the_package_has_files_to_check():
    names = {p.name for p in _files()}
    assert {"__init__.py", "yamlite.py", "schema.py"} <= names


def test_every_file_under_engine_contracts_is_ascii():
    found = []
    for path in _files():
        for number, line in enumerate(path.read_bytes().split(b"\n"), 1):
            bad = [b for b in line if b > 0x7F]
            if bad:
                found.append(f"{path.relative_to(PACKAGE)} line {number}")
    assert found == [], f"non-ASCII bytes in {found}; write them as escapes such as \\u201c"
