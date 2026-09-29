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
   backup is never overwritten by a later one. Force replaces only a file
   the engine wrote that still matches (engine.existing.record: listed in
   the folder's record at its digest, or carrying the engine's stamp);
   any other file is replaced only when the caller also passes
   replace_client;
4. records the sources, the files written and the backups in
   <out>/.uxskill/intake/<intake id>.json, adding to the record a
   write from the same sources made before, and each file written, with
   its digest, in the folder's record of what the engine wrote.

Every file name must be a plain path below the out folder and outside
.uxskill/ (emit.check_name).

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

from engine.existing.record import RECORD, engine_wrote, record_text
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


def _flatten(sources: Any) -> List[Source]:
    """Every Source in `sources`, in order: a report gives its source and
    its also_read. Raises InputError naming what was passed and the fix."""
    fix = ("pass the import's report, its Source, or a list of them (read_source and every "
           "importer give one)")
    if isinstance(sources, (Source, ImportReport)):
        items: List[Any] = [sources]
    elif isinstance(sources, (str, bytes, os.PathLike)) or not hasattr(sources, "__iter__"):
        raise InputError(f"sources is {sources!r}, not a Source; {fix}")
    else:
        items = list(sources)
    found: List[Source] = []
    for item in items:
        if isinstance(item, ImportReport):
            found.extend([item.source, *item.also_read])
        elif isinstance(item, Source):
            found.append(item)
        else:
            raise InputError(f"sources holds {item!r}, not a Source; {fix}")
    return found


def _once(sources: List[Source]) -> List[Source]:
    """`sources` with a path given twice kept once; the digest check runs
    on every one first, so the copies agree."""
    seen: Dict[str, Source] = {}
    for s in sources:
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
        return {"sources": [], "backed_up": {}, "writes": [], "replaced": {}}
    try:
        record = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, ValueError) as exc:
        reason = getattr(exc, "strerror", None) or "it is not JSON"
        raise InputError(f"{path} cannot be read as an intake record ({reason}), so nothing was "
                         "written; move it away and repeat the step") from None
    shape = {"sources": list, "backed_up": dict, "writes": list, "replaced": dict}
    if not isinstance(record, dict) or any(not isinstance(record.get(k), t)
                                           for k, t in shape.items()):
        raise InputError(f"{path} is not an intake record (it needs sources and writes lists "
                         "and backed_up and replaced objects), so nothing was written; move it "
                         "away and repeat the step")
    return record


def write_with_intake(out_dir: Any, files: Mapping[str, str], sources: Sources, *,
                      force: bool = False, replace_client: bool = False,
                      force_label: str = "--force",
                      replace_label: str = "--replace-client-files",
                      out_label: str = "--out", plan_only: bool = False,
                      beside: str = "", own: str = "") -> Dict[str, Any]:
    """Write `files` into out_dir after the intake step (see the module
    docstring). `sources` is a Source, an ImportReport (its source and every
    file in also_read) or a list of either. The labels name the caller's
    inputs in messages. Returns status (a key of emit.STATUS_EXIT),
    written, unchanged, conflicts, message, the backup folder of the
    sources and replaced (each replaced file and where its backup is).
    With plan_only nothing is written: the outcome is the refusal or error
    the write would give, or status "planned" (or "unchanged") when it
    would go ahead, so a caller writing into two folders can check both
    first. `beside` names the source when out_dir is its folder, where an
    extension file has to sit: a refusal then says to rename the file in
    the way rather than to pass another out folder, which would not move
    it. `own` names the engine's own system when out_dir is its folder and
    it is written again in place: a refusal then says force rewrites it
    after a backup."""
    from engine.foundations.emit import check_name, conflict_message, plan_writes, write_files

    out = Path(out_dir).expanduser()
    try:
        every = _flatten(sources)
    except InputError as exc:
        return _outcome("error", str(exc))
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
    every = _once(every)
    try:
        for name in files:
            check_name(out, name, (INTAKE_DIR,))
    except InputError as exc:
        return _outcome("error", str(exc))
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

    def in_the_way(names: List[str]) -> str:
        """Why another out folder is no fix for files beside the source."""
        one = len(names) == 1
        return (f"{'it sits' if one else 'they sit'} beside {beside}, where the extension has "
                f"to load from, so {out_label} does not move {'it' if one else 'them'}")

    if plan.conflicts and not force:
        if own:
            one = len(plan.conflicts) == 1
            return _outcome("refused", (
                f"Nothing was written: {', '.join(str(out / n) for n in plan.conflicts)} "
                f"{'differs' if one else 'differ'} from what the extension writes. {own} is "
                "the system ux-skill wrote, and extend writes it again in place with the files "
                f"built from it; pass {force_label} to rewrite "
                f"{'it' if one else 'them'} after a backup."),
                unchanged=plan.unchanged, conflicts=plan.conflicts)
        if beside:
            one = len(plan.conflicts) == 1
            return _outcome("refused", (
                f"Nothing was written: {', '.join(str(out / n) for n in plan.conflicts)} "
                f"already {'exists' if one else 'exist'} with different content, and "
                f"{in_the_way(plan.conflicts)}. Pass {force_label} to replace "
                f"{'it' if one else 'them'} after a backup, or rename your "
                f"file{'' if one else 's'} of that name."),
                unchanged=plan.unchanged, conflicts=plan.conflicts)
        return _outcome("refused", conflict_message(out, plan, force_label, out_label),
                        unchanged=plan.unchanged, conflicts=plan.conflicts)
    if plan.conflicts and not replace_client:
        # Force replaces only a file the engine wrote that still matches:
        # listed in the folder's record at its digest, or stamped.
        theirs = [n for n in plan.conflicts if not engine_wrote(out, n)]
        if theirs:
            one = len(theirs) == 1
            return _outcome("refused", (
                f"Nothing was written: {', '.join(str(out / n) for n in theirs)} "
                f"{'was' if one else 'were'} not written by ux-skill, or changed since, and "
                f"{force_label} replaces only files ux-skill wrote. Pass {replace_label} as well "
                f"as {force_label} to replace {'it' if one else 'them'} after a backup, or "
                + (f"rename your file{'' if one else 's'} of that name: "
                   f"{in_the_way(theirs)}." if beside else
                   f"pass a different {out_label} folder.")),
                unchanged=plan.unchanged, conflicts=theirs)
    if plan_only:
        return _outcome("planned", f"{out} can take these files.", unchanged=plan.unchanged,
                        conflicts=plan.conflicts)
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
    now = [s.to_dict() for s in every]
    record = {"sources": [*earlier["sources"], *[d for d in now if d not in earlier["sources"]]],
              "backed_up": {**earlier["backed_up"], **backed_up},
              "writes": list(dict.fromkeys([*earlier["writes"], *files])),
              "replaced": {**earlier["replaced"], **replaced}}
    extra[record_name] = json.dumps(record, indent=2) + "\n"
    extra[RECORD] = record_text(out, files)
    try:
        # Only the files allowed above and the two records, which extend
        # earlier ones, may be replaced; a file that changed since is not.
        done = write_files(out, {**extra, **files}, force=True,
                           replace={*plan.conflicts, record_name, RECORD})
    except InputError as exc:
        return _outcome("error", str(exc))
    if done.conflicts:
        one = len(done.conflicts) == 1
        return _outcome("refused", (
            f"Nothing was written: {', '.join(str(out / n) for n in done.conflicts)} "
            f"changed while the step ran, so {'it' if one else 'they'} could not be backed up; "
            "repeat the step."), unchanged=done.unchanged, conflicts=done.conflicts)
    names = ", ".join(n for n in done.write if n in files)
    them = "the source is" if len(every) == 1 else "the sources are"
    message = f"Wrote {names} to {out}; {them} backed up in {out / backup}"
    if replaced:
        message += f" and each replaced file under {out / INTAKE_DIR / 'backup'}"
    return _outcome("written", message + ".", written=done.write, unchanged=done.unchanged,
                    backup=backup, replaced=replaced)
