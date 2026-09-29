"""The intake step before any write into a system someone already has.

write_with_intake() writes an extended or exported system into a folder,
and before anything else it:

1. re-reads every source the import read (the report's source, each file
   in its also_read, or several sources passed at once) and refuses to go
   on when any of them is no longer what was imported, since the result
   was built from what was read;
2. copies each source, byte for byte, into
   <out>/.uxskill/backup/<intake id>/source/, each file under its path
   below the folder the sources share;
3. when forced to replace a file that differs, copies that file, byte for
   byte, into <out>/.uxskill/backup/<its own digest>/replaced/, so a
   backup is never overwritten by a later one. Force replaces a file the
   engine wrote; a file in a folder that holds a client's design system is
   replaced only when the caller also passes replace_client, unless it
   carries the engine's digest and still matches it;
4. records the sources, the files written and the backups in
   <out>/.uxskill/intake/<intake id>.json, adding to the record a
   write from the same sources made before.

Everything, backups included, goes through emit.write_files: all or
nothing, and identical files left alone. The intake id of one source is
its digest; of several, the digest of each one's path below the shared
folder and digest, in the order given. Digests are the first twelve hex
digits of sha256; no time stamps, so the same step twice writes the same
bytes.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple, Union

from engine.existing import client_files_in, is_ux_skill_file
from engine.foundations.errors import InputError
from engine.io.report import ImportReport, Source

INTAKE_DIR = ".uxskill"

Sources = Union[Source, ImportReport, Iterable[Union[Source, ImportReport]]]


def _short(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def _source_files(source: Source) -> List[Path]:
    """The files a source stands for: the file, or a folder's rule files
    sorted by name, as the markdown importer reads them."""
    p = Path(source.path).expanduser()
    return sorted(f for f in p.glob("*.md") if f.is_file()) if p.is_dir() else [p]


def source_digest(source: Source) -> str:
    """The digest the source has now, taken the way its importer took it: a
    file's bytes, or for a folder of rule files each file's name and bytes
    in name order. Raises OSError when a file cannot be read."""
    p = Path(source.path).expanduser()
    if not p.is_dir():
        return hashlib.sha256(p.read_bytes()).hexdigest()
    h = hashlib.sha256()
    for f in _source_files(source):
        h.update(f.name.encode("utf-8") + b"\0" + f.read_bytes())
    return h.hexdigest()


def _flatten(sources: Sources) -> List[Source]:
    """Every Source in `sources`: a report gives its source and also_read,
    in that order; a path read twice is kept once."""
    items = [sources] if isinstance(sources, (Source, ImportReport)) else list(sources)
    found: List[Source] = []
    for item in items:
        if isinstance(item, ImportReport):
            found.extend([item.source, *item.also_read])
        else:
            found.append(item)
    seen: Dict[str, Source] = {}
    for s in found:
        seen.setdefault(os.path.abspath(Path(s.path).expanduser()), s)
    return list(seen.values())


def _layout(sources: List[Source]) -> Tuple[str, List[Tuple[Source, Path, str]]]:
    """The intake id, and each source's files with the path each backup
    takes below source/: its path below the folder all the sources share."""
    files = [(s, f) for s in sources for f in _source_files(s)]
    places = [os.path.abspath(f) for _, f in files]
    tops = [os.path.abspath(Path(s.path).expanduser()) for s in sources]
    folders = [t if Path(t).is_dir() else os.path.dirname(t) for t in tops]
    try:
        base = os.path.commonpath(folders)
    except ValueError:
        # Sources on different drives share no folder: each keeps its digest.
        base = ""
    rel = [Path(os.path.relpath(p, base)).as_posix() if base else
           f"{_short(p.encode('utf-8'))}/{Path(p).name}" for p in places]
    if len(sources) == 1:
        sid = sources[0].sha256[:12]
    else:
        names = [Path(os.path.relpath(t, base)).as_posix() if base else
                 _short(t.encode("utf-8")) for t in tops]
        lines = "".join(f"{n}\0{s.sha256}\n" for n, s in zip(names, sources))
        sid = _short(lines.encode("utf-8"))
    return sid, [(s, f, r) for (s, f), r in zip(files, rel)]


def _outcome(status: str, message: str, written=(), unchanged=(), conflicts=(),
             backup: str = "", replaced=None) -> Dict[str, Any]:
    return {"status": status, "written": list(written), "unchanged": list(unchanged),
            "conflicts": list(conflicts), "message": message, "backup": backup,
            "replaced": dict(replaced or {})}


def _earlier(path: Path) -> Dict[str, Any]:
    """The record a write from the same sources left, or an empty one.
    Raises InputError naming the file and the fix when it cannot be read."""
    if not path.exists():
        return {"writes": [], "replaced": {}}
    try:
        record = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, ValueError) as exc:
        reason = getattr(exc, "strerror", None) or "it is not JSON"
        raise InputError(f"{path} cannot be read as an intake record ({reason}), so nothing was "
                         "written; move it away and repeat the step") from None
    if not isinstance(record, dict) or not isinstance(record.get("writes"), list) \
            or not isinstance(record.get("replaced"), dict):
        raise InputError(f"{path} is not an intake record (it needs a writes list and a "
                         "replaced object), so nothing was written; move it away and repeat "
                         "the step")
    return record


def write_with_intake(out_dir: Any, files: Mapping[str, str], sources: Sources, *,
                      force: bool = False, replace_client: bool = False,
                      force_label: str = "--force",
                      replace_label: str = "--replace-client-files",
                      out_label: str = "--out") -> Dict[str, Any]:
    """Write `files` into out_dir after the intake step (see the module
    docstring). `sources` is a Source, an ImportReport (its source and every
    file in also_read) or a list of either. The labels name the caller's
    inputs in messages. Returns status (a key of emit.STATUS_EXIT),
    written, unchanged, conflicts, message, the backup folder of the
    sources and replaced (each replaced file and where its backup is)."""
    from engine.foundations.emit import conflict_message, plan_writes, write_files

    out = Path(out_dir).expanduser()
    every = _flatten(sources)
    if not every:
        return _outcome("error", "sources is empty, so nothing was written; pass the import's "
                                 "report or every Source the files were built from")
    for source in every:
        try:
            now = source_digest(source)
        except OSError as exc:
            return _outcome("error", f"{source.path} cannot be read again "
                                     f"({exc.strerror or exc}), so nothing was written; put it "
                                     "back or import the system again, and repeat the step")
        if now != source.sha256:
            return _outcome("error", f"{source.path} changed after it was read, so nothing was "
                                     "written; import it again and repeat the step")
    inside = [n for n in files if Path(n).parts[:1] == (INTAKE_DIR,)]
    if inside:
        return _outcome("error", f"files names {', '.join(inside)}, inside {INTAKE_DIR}/, which "
                                 "holds the intake backups, so nothing was written; write "
                                 f"{'that file' if len(inside) == 1 else 'those files'} under "
                                 "another name")
    sid, layout = _layout(every)
    backup = f"{INTAKE_DIR}/backup/{sid}"
    try:
        plan = plan_writes(out, files)
    except InputError as exc:
        return _outcome("error", str(exc))
    if not plan.write and not plan.conflicts:
        return _outcome("unchanged", f"{out} already holds these files; nothing changed.",
                        unchanged=plan.unchanged,
                        backup=backup if (out / backup).is_dir() else "")
    if plan.conflicts and not force:
        return _outcome("refused", conflict_message(out, plan, force_label, out_label),
                        unchanged=plan.unchanged, conflicts=plan.conflicts)
    if plan.conflicts and not replace_client:
        # A client's file, unless it carries the engine's own digest and
        # still matches it: an extension file the engine wrote beside it.
        theirs = [n for n in client_files_in(out, {n: files[n] for n in plan.conflicts})
                  if not is_ux_skill_file(out / n)]
        if theirs:
            one = len(theirs) == 1
            return _outcome("refused", (
                f"Nothing was written: {out} holds a design system ux-skill did not build, and "
                f"{', '.join(str(out / n) for n in theirs)} would be replaced. An existing "
                f"design system is fixed input: pass a different {out_label} folder, or pass "
                f"{replace_label} as well as {force_label} to replace "
                f"{'it' if one else 'them'} after a backup."),
                unchanged=plan.unchanged, conflicts=theirs)
    extra: Dict[str, Union[str, bytes]] = {}
    backed_up: Dict[str, str] = {}
    for source, f, rel in layout:
        where = f"{backup}/source/{rel}"
        try:
            extra[where] = f.read_bytes()
        except OSError as exc:
            return _outcome("error", f"{f} cannot be read again ({exc.strerror or exc}), so "
                                     "nothing was written; put it back or import the system "
                                     "again, and repeat the step")
        p = Path(source.path)
        backed_up[str(p / f.name) if p.expanduser().is_dir() else str(p)] = where
    replaced: Dict[str, str] = {}
    for name in plan.conflicts:
        try:
            old = (out / name).read_bytes()
        except OSError as exc:
            return _outcome("error", f"{out / name} cannot be read ({exc.strerror or exc}), so "
                                     "it cannot be backed up and nothing was written; make it "
                                     "readable and repeat the step")
        where = f"{INTAKE_DIR}/backup/{_short(old)}/replaced/{name}"
        extra[where] = old
        replaced[name] = where
    record_name = f"{INTAKE_DIR}/intake/{sid}.json"
    try:
        earlier = _earlier(out / record_name)
    except InputError as exc:
        return _outcome("error", str(exc))
    record = {"sources": [s.to_dict() for s in every], "backed_up": backed_up,
              "writes": list(dict.fromkeys([*earlier["writes"], *files])),
              "replaced": {**earlier["replaced"], **replaced}}
    extra[record_name] = json.dumps(record, indent=2) + "\n"
    try:
        # Every file of `files` that differs was allowed above; the record
        # may differ from an earlier one, which it extends.
        done = write_files(out, {**extra, **files}, force=True)
    except InputError as exc:
        return _outcome("error", str(exc))
    names = ", ".join(n for n in done.write if n in files)
    them = "the source is" if len(every) == 1 else "the sources are"
    message = f"Wrote {names} to {out}; {them} backed up in {out / backup}"
    if replaced:
        message += f" and each replaced file under {out / INTAKE_DIR / 'backup'}"
    return _outcome("written", message + ".", written=done.write, unchanged=done.unchanged,
                    backup=backup, replaced=replaced)
