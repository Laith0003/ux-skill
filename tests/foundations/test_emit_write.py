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
