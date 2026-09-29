"""The system commands the CLI (uxskill system import, enhance, extend,
export; uxskill contracts check) and the MCP tools share. Each reads first,
returns a small result with a status (a key of EXIT), and writes only when
given an out folder, after the intake step, through the safe writer.
Every InputError names the input by the caller's label and says the fix.

A source is one file, several read as one system (the tokens file first,
then each stylesheet that adds to it), or a project folder, read as the
set system detect finds (engine.io.read). A system the engine did not
write is never rewritten: extend writes its additions in an extension
file beside it and the rest into out, and export writes into out only.
Who owns the source comes from its ownership record, never its names,
and every result says which marker decided it.

A mapping.json the owner already has is merged in memory with the
proposal (adapter.merge: the owner's entries win) and never replaced
unless the engine wrote it and force is given; the result lists what the
proposal adds that the file does not have.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.errors import InputError
from engine.io.adapter import ROLE_TYPES, dump_mapping, load_mapping, merge, propose
from engine.io.adapter import Mapping as RoleMapping
from engine.io.read import read_sources
from engine.io.report import Folded, Imported, fold, owned_by

# Every status a system command reports, with the exit code the CLI gives:
# the build's statuses (written and unchanged 0; refused, failed and error
# 1), plus read, reported, built and passed (0) and blocked (1, an
# extension that did not pass; only its report was written).
EXIT: Dict[str, int] = {"read": 0, "reported": 0, "built": 0, "passed": 0, "written": 0,
                        "unchanged": 0, "blocked": 1, "failed": 1, "refused": 1, "error": 1}
TARGETS: Tuple[str, ...] = ("css", "tailwind", "figma", "dtcg")
# How each input is named in messages: the CLI's flags. The MCP tools pass
# their own argument names.
CLI: Dict[str, str] = {
    "from": "--from", "format": "--format", "out": "--out", "force": "--force",
    "replace_client": "--replace-client-files", "mapping": "--mapping", "add": "--add",
    "add_role": "--add-role", "to": "--to", "brand": "--brand", "axes": "--axes",
    "brief": "--brief", "tokens": "--tokens", "latin_only": "--latin-only",
    "scheme": "--scheme", "figma_mode": "--figma-mode"}
MAPPING = "mapping.json"


def parse_modes(pairs: Sequence[str], label: str = "--figma-mode") -> Dict[str, str]:
    """collection=mode pairs as a mapping, for a Figma collection with more
    than two modes. Raises InputError naming the pair and the fix."""
    out: Dict[str, str] = {}
    for pair in pairs:
        collection, sep, mode = str(pair).partition("=")
        if not sep or not collection.strip() or not mode.strip():
            raise InputError(f"{label} {pair} needs the form collection=mode, for example "
                             "Type=SM")
        out[collection.strip()] = mode.strip()
    return out


def _read(source: Any, fmt: str, second_modes: Optional[Mapping[str, str]],
          labels: Mapping[str, str], label: str = "from") -> Imported:
    return read_sources(source, fmt, labels[label], second_modes, labels["figma_mode"])


def _write(out: Any, files: Dict[str, str], imported: Imported, force: bool,
           labels: Mapping[str, str], replace_client: bool = False) -> Dict[str, Any]:
    from engine.foundations.emit import check_out_dir
    from engine.io.intake import write_with_intake
    folder = check_out_dir(out, labels["out"])
    return write_with_intake(folder, files, imported.report, force=force,
                             replace_client=replace_client, force_label=labels["force"],
                             replace_label=labels["replace_client"], out_label=labels["out"])


def _not_read(imported: Imported) -> List[Dict[str, Any]]:
    """The Not read list as the report prints it: folded when long, each
    line with how many entries it stands for."""
    return [{"where": i.where, "name": i.name, "message": i.message,
             "count": len(i.items) if isinstance(i, Folded) else 1}
            for i in fold(imported.report.not_read)]


def _read_result(status: str, imported: Imported) -> Dict[str, Any]:
    report = imported.report
    return {"status": status, "format": report.source.format,
            "source": report.source.to_dict(),
            "also_read": [a.to_dict() for a in report.also_read],
            "owned_by": owned_by(imported), "ownership": report.ownership}


def _mapping(imported: Imported, mapping: Any,
             labels: Mapping[str, str]) -> Tuple[RoleMapping, List[str], str]:
    """The mapping to read the system through, the notes on what the
    proposal adds to the owner's file, and the file's name: the owner's
    file merged with a proposal from names (the owner's entries win), or
    the proposal alone."""
    proposed = propose(imported.tokens)
    if not mapping:
        return proposed, [], MAPPING
    name = str(mapping)
    merged, notes = merge(proposed, load_mapping(mapping, labels["mapping"]), name)
    return merged, notes, name


def _theirs(folder: Path, mapping: RoleMapping, text: str, force: bool,
            labels: Mapping[str, str]) -> Optional[Tuple[List[str], str]]:
    """When `folder` already holds a mapping.json other than `text` that is
    kept: the notes on what `mapping` adds to it, and a sentence saying it
    was kept. None when mapping.json can be written: there is none, it is
    the same, or the engine wrote it and force replaces it."""
    from engine.existing.record import engine_wrote
    path = folder / MAPPING
    if not path.is_file():
        return None
    try:
        if path.read_text(encoding="utf-8") == text:
            return None
    except (OSError, UnicodeDecodeError):
        pass
    if force and engine_wrote(folder, MAPPING):
        return None
    _, notes = merge(mapping, load_mapping(path, f"{labels['out']} {MAPPING}"), str(path))
    return notes, (f"{path} was kept as it is, since it differs from the proposal and "
                   f"ux-skill does not replace a mapping you may have edited; add what the "
                   "mapping notes name to it to use them.")


def run_import(source: Any, *, fmt: str = "auto", out: Any = None, force: bool = False,
               second_modes: Optional[Mapping[str, str]] = None,
               labels: Mapping[str, str] = CLI) -> Dict[str, Any]:
    """Read a system, report what was read and propose a mapping. With out,
    write import-report.md and mapping.json; a mapping.json out already
    holds is kept, and the result lists what the proposal adds to it."""
    imported = _read(source, fmt, second_modes, labels)
    report = imported.report
    proposed = propose(imported.tokens)
    result = _read_result("read", imported)
    result.update({
        "entries": report.entries, "tokens": report.tokens, "mode_values": report.mode_values,
        "axes": {a: list(v) for a, v in report.axes.items()},
        "renamed": len(report.renamed), "notes": len(report.notes),
        "mapped": len(report.mapped), "not_read_count": len(report.not_read),
        "not_read": _not_read(imported),
        "mapping": {"roles": len(proposed.roles),
                    "mapped": sum(1 for m in proposed.roles.values() if m.token is not None),
                    "of": len(ROLE_TYPES), "axes": len(proposed.axes)},
        "report": report.markdown()})
    if out is None:
        return result
    from engine.foundations.emit import check_out_dir
    folder = check_out_dir(out, labels["out"])
    text = dump_mapping(proposed)
    files = {"import-report.md": report.markdown()}
    kept = _theirs(folder, proposed, text, force, labels)
    if kept is None:
        files[MAPPING] = text
    result["mapping_kept"] = kept is not None
    result["mapping_notes"] = kept[0] if kept else []
    result.update(_write(folder, files, imported, force, labels))
    if kept is not None and result["status"] in ("written", "unchanged"):
        result["message"] += " " + kept[1]
    return result


def _count(d: Optional[Mapping[str, Any]], key: str) -> Optional[int]:
    return None if d is None else len(d[key])


def run_enhance(source: Any, *, fmt: str = "auto", mapping: Any = None,
                scan: Sequence[Any] = (), out: Any = None, force: bool = False,
                second_modes: Optional[Mapping[str, str]] = None,
                labels: Mapping[str, str] = CLI) -> Dict[str, Any]:
    """Measure a system and, given code folders, what the code uses. A
    report only; with out it is written as enhance-report.md and
    enhance.json. A mapping file is merged with a proposal first."""
    from engine.io.enhance import enhance
    from engine.io.scan import scan as scan_code
    imported = _read(source, fmt, second_modes, labels)
    maps, notes, name = _mapping(imported, mapping, labels)
    report = imported.report
    scanned = scan_code(list(scan), imported.tokens,
                        exclude=[report.source.path, *(a.path for a in report.also_read)]) \
        if scan else None
    done = enhance(imported, maps, scanned, merge_notes=notes, mapping_name=name)
    data = done.to_dict()
    gate, m, d = data["gate"], data["mapping"], data["drift"]
    result = _read_result("reported", imported)
    result.update({
        "summary": {
            "gate_measured": gate["measured"], "gate_passed": gate["passed"],
            "findings": len(gate["findings"]), "structure": len(data["structure"]),
            "mapped": m["mapped"], "of": m["of"], "mapping_notes": len(notes),
            "unused": _count(d, "unused"),
            "raw_values": None if d is None else sum(len(v) for v in d["distinct"].values()),
            "raw_with_token": _count(d, "raw_with_token"),
            "spellings": _count(d, "spellings"), "lies": _count(d, "lies"),
            "missing": _count(d, "missing"), "unknown_classes": _count(d, "unknown_classes"),
            "not_measured": _count(d, "not_read")},
        "mapping_notes": list(notes),
        "report": done.markdown()})
    if out is not None:
        files = {"enhance-report.md": done.markdown(),
                 "enhance.json": json.dumps(data, indent=2, ensure_ascii=False) + "\n"}
        result.update(_write(out, files, imported, force, labels))
    return result


def _roles(pairs: Sequence[str], label: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for pair in pairs:
        role, sep, token = str(pair).partition("=")
        if not sep or not role.strip() or not token.strip():
            raise InputError(f"{label} {pair} needs the form role=token, for example "
                             "color.focus.ring=brand-700")
        out[role.strip()] = token.strip()
    return out


def run_extend(source: Any, *, out: Any, fmt: str = "auto", mapping: Any = None,
               add: Sequence[str] = (), add_role: Sequence[str] = (),
               contracts: Sequence[Any] = (), brand: Any = None, axes: Any = None,
               brief: Any = None, latin_only: bool = False, force: bool = False,
               replace_client: bool = False,
               second_modes: Optional[Mapping[str, str]] = None,
               labels: Mapping[str, str] = CLI) -> Dict[str, Any]:
    """Extend a system (engine.io.extend) and write it through
    extend.write_extended: the system itself when the engine wrote it, else
    an extension file beside it, and the font files beside it too (the only
    place they load from); mapping.json, extend-report.md and the contracts
    into out. Both folders are checked before either is written. A blocked
    result writes only its report. The brief is read as a system build
    reads it: it places the axes, its structured fields shape what is
    generated and decide the scripts, its headline sizes the display, and
    its unread words are listed."""
    from engine.foundations.emit import (
        brief_audience, brief_words, check_out_dir, choose_axes, parse_brand, resolve_arabic,
        unread_lines)
    from engine.io.extend import extend, write_extended
    folder = check_out_dir(out, labels["out"])
    imported = _read(source, fmt, second_modes, labels)
    maps, notes, name = _mapping(imported, mapping, labels)
    roles = _roles(add_role, labels["add_role"])
    axis_values, axes_source = choose_axes(brief, axes, brief_label=labels["brief"],
                                           axes_label=labels["axes"])
    audience = brief_audience(brief, labels["brief"])
    arabic = resolve_arabic(latin_only, audience, labels["latin_only"])
    words = brief_words(brief, labels["brief"])
    brand_hex = parse_brand(brand, labels["brand"]) if brand is not None else None
    done = extend(imported, maps, foundations=list(add), roles=roles,
                  contracts=list(contracts), axes=axis_values, axes_source=axes_source,
                  brand=brand_hex, arabic=arabic, audience=audience,
                  unread=unread_lines(brief, labels["brief"]), mapping_name=name, words=words)
    kept = None
    if not done.problems and MAPPING in done.files:
        kept = _theirs(folder, done.mapping, done.files[MAPPING], force, labels)
        if kept is not None:
            done.files = {n: t for n, t in done.files.items() if n != MAPPING}
    result = _read_result("blocked" if done.problems else "built", imported)
    result.update({"added": len(done.added), "problems": list(done.problems),
                   "unread": list(done.unread), "load": done.load,
                   "mapping_kept": kept is not None,
                   "mapping_notes": [*notes, *(kept[0] if kept else [])],
                   "report": done.files["extend-report.md"]})
    outcome = write_extended(done, imported, out=folder, force=force,
                             replace_client=replace_client, force_label=labels["force"],
                             replace_label=labels["replace_client"], out_label=labels["out"])
    if done.problems and outcome["status"] in ("written", "unchanged"):
        outcome["status"] = "blocked"
    if kept is not None and outcome["status"] in ("written", "unchanged"):
        outcome["message"] += " " + kept[1]
    result.update(outcome)
    return result


def _header(imported: Imported) -> List[str]:
    """The comment an export of a system the engine did not write opens
    with: where it came from, and every entry the import did not read
    (folded when long) with how to write it so it is read, and every color
    mapped into sRGB. Empty for the engine's own system."""
    if imported.owned:
        return []
    report = imported.report
    names = [Path(report.source.path).name, *(Path(a.path).name for a in report.also_read)]
    shown = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
    lines = [f"Written by ux-skill from {shown}, which it did not write and leaves as "
             f"{'it is' if len(names) == 1 else 'they are'}."]
    n = len(report.not_read)
    if n:
        lines.append(f"{n} {'entry was' if n == 1 else 'entries were'} not read on the way in "
                     f"and {'is' if n == 1 else 'are'} not below; each with how to write it so "
                     "it can be read:")
        lines += [f"  {i.where} {i.name}: {i.message}".replace(" :", ":")
                  for i in fold(report.not_read)]
    if report.mapped:
        lines.append("Colors outside sRGB are read as the sRGB color named:")
        lines += [f"  {m.where} {m.name}: {m.original}, read as {m.hex}" for m in report.mapped]
    return lines


def run_export(source: Any, *, to: str, fmt: str = "auto", out: Any = None,
               force: bool = False, include_files: bool = False, scheme: Optional[str] = None,
               second_modes: Optional[Mapping[str, str]] = None,
               labels: Mapping[str, str] = CLI) -> Dict[str, Any]:
    """A system in another format, written into out only (never over its
    source): tokens.css, tailwind-theme.css, the Figma variables files or
    tokens.json. A stylesheet keeps the scheme it opens; tokens.json holds
    none, so `scheme` sets it (system when left out). An export of a system
    the engine did not write opens with a comment listing every entry the
    import did not read (stylesheets), or says how many in the result
    (JSON, which holds no comment)."""
    from engine.foundations.export import SCHEME_DEFAULTS, dump_dtcg, to_css
    from engine.io.figma_out import figma_files
    from engine.io.tailwind_out import in_roles, to_tailwind
    if to not in TARGETS:
        raise InputError(f"{labels['to']} is {to}; pass css, tailwind, figma or dtcg")
    if scheme is not None and scheme not in SCHEME_DEFAULTS:
        raise InputError(f"{labels['scheme']} is {scheme}; pass light, dark or system")
    imported = _read(source, fmt, second_modes, labels)
    ts = imported.tokens
    opens = scheme or imported.scheme
    header = _header(imported)
    if to == "css":
        files = {"tokens.css": to_css(ts, scheme=opens, forms=imported.forms, header=header)}
    elif to == "tailwind":
        text = to_tailwind(ts, imported.forms, imported.resets or None, scheme=opens,
                           roles=in_roles(imported), variant=imported.variant)
        head = "".join(f" * {line}".rstrip().replace("*/", "* /") + "\n" for line in header)
        files = {"tailwind-theme.css": f"/*\n{head} */\n{text}" if header else text}
    elif to == "figma":
        files = figma_files(ts)
    else:
        files = {"tokens.json": dump_dtcg(ts)}
    result = _read_result("built", imported)
    n = len(imported.report.not_read)
    result.update({
        "to": to, "not_read": n,
        "files": [{"name": k, "bytes": len(t.encode("utf-8"))} for k, t in files.items()]})
    if n and to in ("figma", "dtcg"):
        result["note"] = (f"{n} {'entry' if n == 1 else 'entries'} of the source "
                          f"{'was' if n == 1 else 'were'} not read and {'is' if n == 1 else 'are'}"
                          f" not in these files; run system import on it to see each with how "
                          "to write it so it can be read.")
    if include_files:
        result["texts"] = dict(files)
    if out is not None:
        result.update(_write(out, files, imported, force, labels))
    return result


def run_contracts_check(folder: Any, source: Any, *, fmt: str = "auto", mapping: Any = None,
                        second_modes: Optional[Mapping[str, str]] = None,
                        labels: Mapping[str, str] = CLI) -> Dict[str, Any]:
    """Check a folder of contracts against a system in any format the
    importers read (told from the file, as for the system commands),
    through `mapping` when given; a system that does not use the engine's
    role names and has no mapping is read through one proposed from names,
    and a note says so."""
    from engine.contracts.check import check_contracts
    imported = _read(source, fmt, second_modes, labels, "tokens")
    notes: List[str] = []
    if not mapping and not any(imported.tokens.has(r) for r in ROLE_TYPES):
        mapping = propose(imported.tokens)
        notes.append(f"No {labels['mapping']} was given and the system does not use the "
                     "engine's role names, so its roles were read through a mapping proposed "
                     "from names; run system import with an out folder to write it as "
                     f"{MAPPING}, confirm it, and pass it as {labels['mapping']}.")
    done = check_contracts(folder, imported, mapping,
                           mapping_name=str(mapping) if isinstance(mapping, (str, Path))
                           else MAPPING if mapping else None)
    return {"status": "passed" if done.passed else "failed",
            "contracts": [c.name for c in done.contracts],
            "problems": [{"contract": p.contract, "rule": p.rule, "message": p.message}
                         for p in done.problems],
            "lines": list(done.lines), "notes": [*notes, *done.notes]}
