"""Safe by default: a file that exists and differs is never replaced
without force, one conflict stops every write, and an identical file is
left untouched."""
import os

import pytest

from engine.foundations.emit import (
    InputError, WritePlan, check_out_dir, conflict_message, plan_writes, write_files,
)

FILES = {"tokens.json": "{}\n", "tokens.css": ":root {}\n", "system-report.md": "# r\n"}


def test_writes_every_file_into_a_new_folder(tmp_path):
    out = tmp_path / "ds" / "nested"
    plan = write_files(out, FILES)
    assert plan == WritePlan(("tokens.json", "tokens.css", "system-report.md"), (), ())
    for name, text in FILES.items():
        assert (out / name).read_text(encoding="utf-8") == text


def test_identical_files_are_left_untouched(tmp_path):
    write_files(tmp_path, FILES)
    old = 1_000_000_000
    for name in FILES:
        os.utime(tmp_path / name, (old, old))
    plan = write_files(tmp_path, FILES)
    assert plan == WritePlan((), ("tokens.json", "tokens.css", "system-report.md"), ())
    for name in FILES:
        assert (tmp_path / name).stat().st_mtime == old


def test_one_conflict_stops_every_write(tmp_path):
    (tmp_path / "tokens.css").write_text("/* mine */\n", encoding="utf-8")
    plan = write_files(tmp_path, FILES)
    assert plan.conflicts == ("tokens.css",)
    assert plan.write == ("tokens.json", "system-report.md")
    assert (tmp_path / "tokens.css").read_text(encoding="utf-8") == "/* mine */\n"
    assert not (tmp_path / "tokens.json").exists()
    assert not (tmp_path / "system-report.md").exists()


def test_force_replaces_only_what_differs(tmp_path):
    (tmp_path / "tokens.css").write_text("/* mine */\n", encoding="utf-8")
    (tmp_path / "tokens.json").write_text("{}\n", encoding="utf-8")
    plan = write_files(tmp_path, FILES, force=True)
    assert plan == WritePlan(("system-report.md", "tokens.css"), ("tokens.json",), ())
    assert (tmp_path / "tokens.css").read_text(encoding="utf-8") == ":root {}\n"


def test_plan_writes_does_not_write(tmp_path):
    plan = plan_writes(tmp_path / "missing", FILES)
    assert plan.write == tuple(FILES) and not (tmp_path / "missing").exists()


def test_a_folder_in_the_way_is_named(tmp_path):
    (tmp_path / "tokens.css").mkdir()
    with pytest.raises(InputError) as exc:
        plan_writes(tmp_path, FILES)
    assert str(exc.value).startswith(f"{tmp_path / 'tokens.css'} is a folder")


def test_conflict_message_names_each_file_and_both_fixes(tmp_path):
    one = conflict_message(tmp_path, WritePlan((), (), ("tokens.css",)))
    assert one == (f"Nothing was written: {tmp_path / 'tokens.css'} already exists with "
                   "different content. Pass --force to replace it, or pass a different --out "
                   "folder.")
    two = conflict_message(tmp_path, WritePlan((), (), ("tokens.json", "tokens.css")),
                           force_flag="force=true", out_flag="out")
    assert "tokens.json" in two and "already exist with" in two
    assert "Pass force=true to replace them" in two and "a different out folder" in two


def test_check_out_dir(tmp_path):
    assert check_out_dir(tmp_path / "new") == tmp_path / "new"
    f = tmp_path / "file.txt"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(InputError, match=r"^--out .*file\.txt is a file, not a folder"):
        check_out_dir(f, label="--out")
    with pytest.raises(InputError, match="^--out is missing"):
        check_out_dir("", label="--out")


# Every filesystem error names the path and the fix; none escapes as a
# traceback.
POSIX_USER = os.name == "posix" and hasattr(os, "geteuid") and os.geteuid() != 0
needs_permissions = pytest.mark.skipif(
    not POSIX_USER, reason="file permissions are not enforced here (Windows, or root)")


def _can_symlink(tmp_path):
    try:
        (tmp_path / ".probe").symlink_to(tmp_path)
    except (OSError, NotImplementedError):
        return False
    (tmp_path / ".probe").unlink()
    return True


def test_out_folder_inside_a_file_is_named(tmp_path):
    f = tmp_path / "afile"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(InputError) as exc:
        check_out_dir(f / "sub" / "ds", label="--out")
    assert str(exc.value) == (
        f"--out {f / 'sub' / 'ds'} is inside {f}, which is a file, so the folder cannot be "
        f"made; pass a folder path that is not inside a file, for example "
        f"{tmp_path / 'design-system'}")


def test_out_folder_expands_a_home_folder(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    assert check_out_dir("~/ds") == tmp_path / "ds"


def test_out_folder_that_is_a_broken_link_is_named(tmp_path):
    if not _can_symlink(tmp_path):
        pytest.skip("symbolic links are not available here")
    link = tmp_path / "ds"
    link.symlink_to(tmp_path / "gone")
    with pytest.raises(InputError) as exc:
        check_out_dir(link, label="--out")
    assert str(exc.value).startswith(
        f"--out {link} is a link to {tmp_path / 'gone'}, which does not exist; ")
    assert "remove the link" in str(exc.value)


def test_a_broken_link_in_place_of_a_file_is_named(tmp_path):
    if not _can_symlink(tmp_path):
        pytest.skip("symbolic links are not available here")
    (tmp_path / "tokens.css").symlink_to(tmp_path / "gone.css")
    with pytest.raises(InputError) as exc:
        write_files(tmp_path, FILES)
    assert str(exc.value).startswith(
        f"{tmp_path / 'tokens.css'} is a link to {tmp_path / 'gone.css'}, which does not exist; "
        "remove the link")
    assert not (tmp_path / "tokens.json").exists()


def test_a_link_is_never_written_through(tmp_path):
    if not _can_symlink(tmp_path):
        pytest.skip("symbolic links are not available here")
    shared = tmp_path / "shared.css"
    shared.write_text(FILES["tokens.css"], encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    (out / "tokens.css").symlink_to(shared)
    plan = write_files(out, FILES)
    assert plan.unchanged == ("tokens.css",)
    shared.write_text("/* edited */\n", encoding="utf-8")
    with pytest.raises(InputError) as exc:
        write_files(out, FILES, force=True)
    assert str(exc.value).startswith(f"{out / 'tokens.css'} is a link to {shared}; ")
    assert shared.read_text(encoding="utf-8") == "/* edited */\n"


@needs_permissions
def test_an_unreadable_file_is_named(tmp_path):
    target = tmp_path / "tokens.css"
    target.write_text("/* mine */\n", encoding="utf-8")
    target.chmod(0)
    try:
        with pytest.raises(InputError) as exc:
            write_files(tmp_path, FILES)
    finally:
        target.chmod(0o644)
    assert str(exc.value).startswith(f"{target} exists but cannot be read (Permission denied)")
    assert "or write the system into a different folder" in str(exc.value)
    assert not (tmp_path / "tokens.json").exists()


@needs_permissions
def test_a_read_only_folder_is_named(tmp_path):
    out = tmp_path / "ro"
    out.mkdir()
    out.chmod(0o555)
    try:
        with pytest.raises(InputError) as exc:
            write_files(out, FILES)
        assert list(out.iterdir()) == []
    finally:
        out.chmod(0o755)
    assert str(exc.value).startswith(f"{out} cannot be written (Permission denied)")
    assert "pass a folder you can write to" in str(exc.value)


@needs_permissions
def test_a_folder_that_cannot_be_made_is_named(tmp_path):
    parent = tmp_path / "ro"
    parent.mkdir()
    parent.chmod(0o555)
    try:
        with pytest.raises(InputError) as exc:
            write_files(parent / "ds", FILES)
    finally:
        parent.chmod(0o755)
    assert str(exc.value).startswith(f"{parent / 'ds'} cannot be made (Permission denied)")
    assert not (parent / "ds").exists()


def test_writing_nothing_makes_no_folder(tmp_path):
    assert write_files(tmp_path / "new", {}) == WritePlan((), (), ())
    assert not (tmp_path / "new").exists()


# All or nothing: every file is staged in a folder inside the out folder,
# then moved into place. A failure at any step leaves the folder exactly as
# it was, never a mix of two systems.
import errno  # noqa: E402

import engine.foundations.emit as emit  # noqa: E402

OLD = {"tokens.json": '{"old": 1}\n', "tokens.css": "/* old */\n",
       "system-report.md": "# old\n"}


def _snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes() if p.is_file() else "folder")
            for p in sorted(root.rglob("*"))}


def _fail_on_call(real, n):
    calls = []

    def wrapper(*args):
        calls.append(args)
        if len(calls) == n:
            raise OSError(errno.ENOSPC, "No space left on device")
        return real(*args)
    return wrapper


def _write_old(folder):
    folder.mkdir(parents=True, exist_ok=True)
    for name, text in OLD.items():
        (folder / name).write_text(text, encoding="utf-8")


def test_a_failure_while_staging_leaves_the_folder_as_it_was(tmp_path, monkeypatch):
    _write_old(tmp_path)
    before = _snapshot(tmp_path)
    monkeypatch.setattr(emit, "_stage", _fail_on_call(emit._stage, 2))
    with pytest.raises(InputError) as exc:
        write_files(tmp_path, FILES, force=True)
    assert str(exc.value) == (
        f"{tmp_path / 'tokens.css'} could not be written (No space left on device), so nothing "
        f"in {tmp_path} was changed; free some space or pass a folder you can write to")
    assert _snapshot(tmp_path) == before


def test_a_failure_while_moving_into_place_restores_every_file(tmp_path, monkeypatch):
    _write_old(tmp_path)
    before = _snapshot(tmp_path)
    monkeypatch.setattr(emit, "_place", _fail_on_call(emit._place, 2))
    with pytest.raises(InputError, match="so nothing in .* was changed"):
        write_files(tmp_path, FILES, force=True)
    assert _snapshot(tmp_path) == before


def test_a_failure_keeps_identical_files_untouched(tmp_path, monkeypatch):
    (tmp_path / "tokens.json").write_text(FILES["tokens.json"], encoding="utf-8")
    old = 1_000_000_000
    os.utime(tmp_path / "tokens.json", (old, old))
    before = _snapshot(tmp_path)
    monkeypatch.setattr(emit, "_place", _fail_on_call(emit._place, 2))
    with pytest.raises(InputError):
        write_files(tmp_path, FILES)
    assert _snapshot(tmp_path) == before
    assert (tmp_path / "tokens.json").stat().st_mtime == old


def test_a_failure_in_a_new_folder_leaves_no_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(emit, "_stage", _fail_on_call(emit._stage, 2))
    with pytest.raises(InputError):
        write_files(tmp_path / "new" / "ds", FILES)
    assert list(tmp_path.iterdir()) == []


def test_a_forced_write_leaves_only_the_three_files(tmp_path):
    _write_old(tmp_path)
    plan = write_files(tmp_path, FILES, force=True)
    assert set(plan.write) == set(FILES)
    assert _snapshot(tmp_path) == {name: text.encode("utf-8") for name, text in FILES.items()}
