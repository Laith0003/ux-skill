"""The engine's record of the files it wrote into a folder.

Every write the engine makes into a folder (system build, and the intake
step before an extend or export) also writes RECORD there: each file's
name and the first twelve hex digits of the sha256 of the bytes it wrote.
A file is the engine's while its bytes still match that digest, or while
it carries the engine's own digest stamp and still matches it
(detect.is_ux_skill_file). A person's edit changes the bytes, so the file
becomes theirs and force alone never replaces it.

The record keeps what earlier writes listed and adds or updates the files
of this write, sorted by name, so the same write gives the same bytes. A
record that cannot be read counts as empty: it only ever grants
ownership, so losing it makes the engine more careful, never less.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Union

from engine.existing.detect import is_ux_skill_file

# Inside the folder the intake step keeps its backups in.
RECORD = ".uxskill/files.json"


def file_digest(data: Union[str, bytes]) -> str:
    """The first twelve hex digits of the sha256 of a file's bytes; text is
    taken as UTF-8, as the writer puts it on disk."""
    raw = data.encode("utf-8") if isinstance(data, str) else data
    return hashlib.sha256(raw).hexdigest()[:12]


def read_record(out_dir: Any) -> Dict[str, str]:
    """The files the record in out_dir lists, name to digest; empty when
    there is no record or it cannot be read."""
    try:
        doc = json.loads((Path(out_dir) / RECORD).read_bytes().decode("utf-8"))
    except (OSError, ValueError):
        return {}
    files = doc.get("files") if isinstance(doc, dict) else None
    if not isinstance(files, dict):
        return {}
    return {k: v for k, v in files.items() if isinstance(k, str) and isinstance(v, str)}


def record_text(out_dir: Any, files: Mapping[str, Union[str, bytes]]) -> str:
    """The record out_dir will hold once `files` are written: what it lists
    now, with each of `files` added at the digest of its new bytes."""
    listed = {**read_record(out_dir), **{n: file_digest(d) for n, d in files.items()}}
    return json.dumps({"files": dict(sorted(listed.items()))}, indent=2) + "\n"


def engine_wrote(out_dir: Any, name: str) -> bool:
    """True when the file `name` in out_dir is the engine's: its bytes match
    the digest the record lists for it, or it carries the engine's digest
    stamp and still matches it."""
    path = Path(out_dir) / name
    if is_ux_skill_file(path):
        return True
    listed = read_record(out_dir).get(name)
    if listed is None:
        return False
    try:
        return path.is_file() and file_digest(path.read_bytes()) == listed
    except OSError:
        return False


def record_unchanged(out_dir: Any, files: Mapping[str, Union[str, bytes]]) -> bool:
    """Write the record for a folder built before the record existed, when
    a build finds every file in it unchanged: each of `files` must be on
    disk with exactly those bytes, and the folder must hold no record yet.
    Returns True when the record was written; False, writing nothing, when
    a file differs or is missing, a record exists, or it cannot be
    written."""
    out = Path(out_dir)
    if not files or (out / RECORD).exists():
        return False
    for name, data in files.items():
        raw = data.encode("utf-8") if isinstance(data, str) else data
        try:
            if (out / name).read_bytes() != raw:
                return False
        except OSError:
            return False
    try:
        (out / RECORD).parent.mkdir(exist_ok=True)
        (out / RECORD).write_text(record_text(out, files), encoding="utf-8")
    except OSError:
        return False
    return True
