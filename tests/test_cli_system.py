"""`uxskill system build`: the 4.0 foundations engine on the command line.

Runs in process through click's CliRunner, in a tmp folder, with plain JSON
output (--no-pretty) as the slash commands read it. One subprocess test
proves the module entry point wires the group.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

click = pytest.importorskip("click")
from click.testing import CliRunner  # noqa: E402

import engine.foundations.color as color_module  # noqa: E402
from engine.cli.main import cli  # noqa: E402
from engine.foundations.emit import NEUTRAL, make_system  # noqa: E402
from engine.synthesizer.axes import compute_axes  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FILES = ("tokens.json", "tokens.css", "system-report.md")


def _runner():
    """stderr apart from stdout on every supported click: 8.1 (the last
    release for Python 3.9) needs mix_stderr=False; 8.2 removed the option
    and always keeps them apart."""
    try:
        return CliRunner(mix_stderr=False)
    except TypeError:
        return CliRunner()


def _run(*args):
    result = _runner().invoke(cli, ["--no-pretty", "system", "build", *args])
    payload = None
    if result.stdout.strip().startswith("{"):
        payload = json.loads(result.stdout)
    return result, payload


def test_build_writes_the_three_files(tmp_path):
    out = tmp_path / "ds"
    result, payload = _run("--brand", "#3366FF", "--out", str(out))
    assert result.exit_code == 0, result.output
    assert payload["status"] == "written" and payload["passed"] is True
    assert payload["written"] == list(FILES) and payload["conflicts"] == []
    assert payload["gate"].startswith("WCAG gate passed: ")
    assert payload["axes_source"].startswith("neutral default")
    expected = make_system("#3366FF", NEUTRAL, payload["axes_source"])
    for name in FILES:
        assert (out / name).read_text(encoding="utf-8") == expected.files[name]


def test_brief_places_the_axes_and_the_report_says_so(tmp_path):
    brief = tmp_path / "brief.json"
    brief.write_text(json.dumps({"answers": {"industry": "healthcare", "tone": ["calm"]}}),
                     encoding="utf-8")
    result, payload = _run("--brand", "3366ff", "--brief", str(brief), "--out", str(tmp_path / "o"))
    assert result.exit_code == 0, result.output
    assert payload["brand"] == "#3366FF"
    assert payload["axes"] == compute_axes({"industry": "healthcare", "tone": ["calm"]}).to_dict()
    report = (tmp_path / "o" / "system-report.md").read_text(encoding="utf-8")
    assert "Axes: from the brief (industry: healthcare; tone: calm)." in report


def test_axes_flag_and_latin_only(tmp_path):
    result, payload = _run("--brand", "#6B4423", "--axes", "0.2,0.8,0.9,0.1,0.7,0.3,0.6",
                           "--latin-only", "--out", str(tmp_path))
    assert result.exit_code == 0, result.output
    assert payload["axes"]["density"] == 0.9 and payload["arabic"] is False
    assert payload["axes_source"] == "set by hand (--axes)"
    assert "type-face-arabic" not in (tmp_path / "tokens.css").read_text(encoding="utf-8")


def test_second_identical_run_changes_nothing(tmp_path):
    _run("--brand", "#3366FF", "--out", str(tmp_path))
    before = {n: (tmp_path / n).stat().st_mtime_ns for n in FILES}
    result, payload = _run("--brand", "#3366FF", "--out", str(tmp_path))
    assert result.exit_code == 0
    assert payload["status"] == "unchanged" and payload["unchanged"] == list(FILES)
    assert {n: (tmp_path / n).stat().st_mtime_ns for n in FILES} == before


def test_a_different_file_is_never_overwritten_without_force(tmp_path):
    (tmp_path / "tokens.css").write_text("/* hand edited */\n", encoding="utf-8")
    result, payload = _run("--brand", "#3366FF", "--out", str(tmp_path))
    assert result.exit_code == 1
    assert payload["status"] == "refused" and payload["conflicts"] == ["tokens.css"]
    assert payload["written"] == [], "a refused run writes nothing, so it lists nothing written"
    assert str(tmp_path / "tokens.css") in payload["message"]
    assert "--force" in payload["message"] and "--out" in payload["message"]
    assert (tmp_path / "tokens.css").read_text(encoding="utf-8") == "/* hand edited */\n"
    assert not (tmp_path / "tokens.json").exists()

    result, payload = _run("--brand", "#3366FF", "--out", str(tmp_path), "--force")
    assert result.exit_code == 0 and payload["status"] == "written"
    assert "tokens.css" in payload["written"]
    assert (tmp_path / "tokens.css").read_text(encoding="utf-8").startswith(":root {")


def test_gate_failure_exits_1_writes_nothing_and_prints_every_finding(tmp_path, monkeypatch):
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    out = tmp_path / "ds"
    result, payload = _run("--brand", "#FFD400", "--out", str(out))
    assert result.exit_code == 1
    assert payload["status"] == "failed" and payload["passed"] is False
    assert payload["gate"].startswith("WCAG gate failed: ")
    assert payload["findings"], payload
    for f in payload["findings"]:
        assert set(f) == {"subject", "context", "message"}
        assert f["subject"] and f["message"]
    assert not out.exists()


def test_a_failed_build_tells_the_user_what_to_change_and_every_finding(tmp_path, monkeypatch):
    monkeypatch.setattr(color_module, "_solve_group", lambda *args, **kwargs: None)
    result, payload = _run("--brand", "#FFD400", "--out", str(tmp_path / "ds"))
    assert result.exit_code == 1
    message = payload["message"]
    assert message.startswith("Nothing was written")
    assert "brand color" in message and "axes" in message and "brief" in message
    assert "fix each finding" not in message.lower()
    err = result.stderr
    assert not err.lstrip().startswith("{")
    assert err.startswith("No design system was built for #FFD400: the WCAG gate found "
                          f"{len(payload['findings'])} problems")
    assert "What to change" in err and "darker or more saturated brand color" in err
    assert "fix each finding" not in err.lower()
    findings = err.split("Findings\n", 1)[1].strip().splitlines()
    assert len(findings) == len(payload["findings"])
    for line, f in zip(findings, payload["findings"]):
        assert line.startswith("- ") and f["subject"].split(" on ")[0] in line
    assert "scheme:" not in err


def test_a_validation_failure_says_to_report_it(tmp_path, monkeypatch):
    from engine.foundations import ValidationError
    from engine.foundations.validate import Problem

    def broken(*args, **kwargs):
        raise ValidationError([Problem("space.4", "bad-value", "space.4 is 'x'; use a dimension")])
    monkeypatch.setattr("engine.foundations.emit.build_system", broken)
    result, payload = _run("--brand", "#3366FF", "--out", str(tmp_path / "ds"))
    assert result.exit_code == 1 and payload["status"] == "failed"
    assert "report it" in payload["message"] and "fix each finding" not in payload["message"]
    assert "structural rule" in result.stderr and "space.4" in result.stderr
    assert not (tmp_path / "ds").exists()


def _snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes() if p.is_file() else "folder")
            for p in sorted(root.rglob("*"))}


def test_a_write_error_exits_1_and_changes_nothing(tmp_path, monkeypatch):
    import errno

    import engine.foundations.emit as emit
    for name in FILES:
        (tmp_path / name).write_text("old\n", encoding="utf-8")
    before = _snapshot(tmp_path)

    def full(*args):
        raise OSError(errno.ENOSPC, "No space left on device")
    monkeypatch.setattr(emit, "_place", full)
    result, payload = _run("--brand", "#3366FF", "--out", str(tmp_path), "--force")
    assert result.exit_code == 1
    assert payload["status"] == "error" and payload["written"] == []
    assert "No space left on device" in payload["message"]
    assert "nothing in" in payload["message"] and "was changed" in payload["message"]
    assert payload["message"] in result.stderr
    assert _snapshot(tmp_path) == before


@pytest.mark.skipif(os.name == "nt" or (hasattr(os, "geteuid") and os.geteuid() == 0),
                    reason="needs POSIX permissions and a non-root user")
def test_a_read_only_out_folder_exits_1(tmp_path):
    out = tmp_path / "ro"
    out.mkdir()
    out.chmod(0o500)
    try:
        result, payload = _run("--brand", "#3366FF", "--out", str(out))
    finally:
        out.chmod(0o700)
    assert result.exit_code == 1 and payload["status"] == "error"
    assert str(out) in payload["message"] and "Permission denied" in payload["message"]
    assert list(out.iterdir()) == []


def test_a_folder_in_place_of_a_file_exits_1(tmp_path):
    (tmp_path / "tokens.css").mkdir()
    result, payload = _run("--brand", "#3366FF", "--out", str(tmp_path))
    assert result.exit_code == 1 and payload["status"] == "error"
    assert f"{tmp_path / 'tokens.css'} is a folder" in payload["message"]
    assert not (tmp_path / "tokens.json").exists()


@pytest.mark.parametrize("args,needle", [
    (["--brand", "blue"], "--brand is 'blue', which is not a hex color"),
    (["--brand", "#3366FF", "--axes", "0.5,0.5"], "--axes has 2 values"),
    (["--brand", "#3366FF", "--axes", "0.5,0.5,0.5,0.5,0.5,0.5,2"],
     "--axes gives type_personality as '2'"),
])
def test_bad_input_exits_2_and_names_the_flag(tmp_path, args, needle):
    result, _ = _run(*args, "--out", str(tmp_path / "o"))
    assert result.exit_code == 2
    assert needle in result.stderr
    assert not (tmp_path / "o").exists()


def test_brief_and_axes_together_are_refused(tmp_path):
    brief = tmp_path / "b.json"
    brief.write_text('{"industry": "saas"}', encoding="utf-8")
    result, _ = _run("--brand", "#3366FF", "--brief", str(brief),
                     "--axes", "0.5,0.5,0.5,0.5,0.5,0.5,0.5", "--out", str(tmp_path / "o"))
    assert result.exit_code == 2
    assert "both --brief and --axes were given; pass one" in result.stderr


def test_bad_brief_and_out_name_the_flag(tmp_path):
    brief = tmp_path / "b.json"
    brief.write_text("{oops", encoding="utf-8")
    result, _ = _run("--brand", "#3366FF", "--brief", str(brief), "--out", str(tmp_path / "o"))
    assert result.exit_code == 2 and f"--brief {brief} is not valid JSON" in result.stderr

    missing = tmp_path / "nope.json"
    result, _ = _run("--brand", "#3366FF", "--brief", str(missing), "--out", str(tmp_path / "o"))
    assert result.exit_code == 2 and f"--brief {missing} cannot be read" in result.stderr

    a_file = tmp_path / "taken"
    a_file.write_text("x", encoding="utf-8")
    result, _ = _run("--brand", "#3366FF", "--out", str(a_file))
    assert result.exit_code == 2 and "is a file, not a folder" in result.stderr


def test_brand_and_out_are_required():
    result = _runner().invoke(cli, ["--no-pretty", "system", "build", "--out", "x"])
    assert result.exit_code == 2 and "--brand" in result.stderr
    result = _runner().invoke(cli, ["--no-pretty", "system", "build", "--brand", "#3366FF"])
    assert result.exit_code == 2 and "--out" in result.stderr


def test_module_entry_point_runs_system_build(tmp_path):
    env = {**os.environ, "PYTHONPATH": str(ROOT), "UX_SKILL_NO_HINT": "1"}
    r = subprocess.run([sys.executable, "-m", "engine.cli.main", "--no-pretty", "system",
                        "build", "--brand", "#3366FF", "--out", str(tmp_path)],
                       cwd=str(tmp_path), env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["status"] == "written"
    assert (tmp_path / "tokens.json").exists()


def test_the_command_reports_the_shared_statuses():
    # One table in emit.py names every status and its exit code; the CLI
    # exits by it and the /ux-system doc test reads it. emit.write_outcome
    # gives every status, for the CLI and for ux_system_build with out.
    from engine.foundations.emit import STATUS_EXIT, STATUSES
    assert STATUSES == ("written", "unchanged", "refused", "failed", "error")
    assert {s: STATUS_EXIT[s] for s in STATUSES} == {
        "written": 0, "unchanged": 0, "refused": 1, "failed": 1, "error": 1}
    import inspect

    import engine.cli.main as main_module
    from engine.foundations.emit import write_outcome
    outcome = inspect.getsource(write_outcome)
    for status in STATUSES:
        assert f'"{status}"' in outcome, status
    source = Path(main_module.__file__).read_text(encoding="utf-8")
    block = source[source.index("def system_build_cmd"):source.index("# -------- ux version")]
    assert "write_outcome(" in block
    assert "sys.exit(1)" not in block, "exit through STATUS_EXIT, not a literal code"


def test_help_says_system_pack_is_3x_and_points_at_system_build():
    result = _runner().invoke(cli, ["--help"])
    line = next(line for line in result.stdout.splitlines() if "system-pack" in line)
    assert "3.x" in line and "system build" in line, line


def test_rule_pack_flag_writes_the_pack_beside_the_three_files(tmp_path):
    out = tmp_path / "ds"
    result, payload = _run("--brand", "#3366FF", "--out", str(out), "--rule-pack")
    assert result.exit_code == 0, result.output
    assert payload["written"][:3] == list(FILES)
    assert "rule-pack/README.md" in payload["written"]
    assert (out / "rule-pack" / "color" / "audit.md").is_file()
    assert (out / "rule-pack" / "contracts" / "button.yaml").is_file()
    assert (out / "rule-pack" / "decisions" / "HISTORY.md").is_file()
    again, payload = _run("--brand", "#3366FF", "--out", str(out), "--rule-pack")
    assert again.exit_code == 0 and payload["status"] == "unchanged"


def test_without_the_flag_no_rule_pack_is_written(tmp_path):
    out = tmp_path / "ds"
    result, _ = _run("--brand", "#3366FF", "--out", str(out))
    assert result.exit_code == 0
    assert sorted(p.name for p in out.iterdir()) == sorted(FILES)


# A pack beside tokens it was not built from is reported as stale, named
# with its folder and the fix, and never touched.
def _pack_bytes(out):
    root = out / "rule-pack"
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file()}


def test_a_pack_left_beside_other_tokens_is_reported_stale_and_kept(tmp_path):
    import hashlib
    out = tmp_path / "ds"
    result, payload = _run("--brand", "#3366FF", "--out", str(out), "--rule-pack")
    assert payload["stale_rule_pack"] is None
    manifest = json.loads((out / "rule-pack" / "built-from.json").read_text(encoding="utf-8"))
    assert manifest == {"tokens.json": {
        "sha256": hashlib.sha256((out / "tokens.json").read_bytes()).hexdigest()}}
    before = _pack_bytes(out)
    # The same tokens without the flag: the pack matches, nothing is said.
    result, payload = _run("--brand", "#3366FF", "--out", str(out))
    assert payload["status"] == "unchanged" and payload["stale_rule_pack"] is None
    assert "rule pack" not in payload["message"]
    # Other tokens, forced, without the flag: written, the pack kept and
    # named as stale in the message, the JSON and the report.
    result, payload = _run("--brand", "#FFD400", "--out", str(out), "--force")
    assert result.exit_code == 0 and payload["status"] == "written"
    folder = out / "rule-pack"
    assert payload["stale_rule_pack"] == str(folder)
    assert f"{folder} holds a rule pack built from other tokens" in payload["message"]
    assert "Build again with --rule-pack to replace it, or remove" in payload["message"]
    report = (out / "system-report.md").read_text(encoding="utf-8")
    assert "## Rule pack" in report and "remove rule-pack/" in report
    assert str(tmp_path) not in report
    assert _pack_bytes(out) == before
    # Built again the same way: unchanged, still stale.
    again, payload = _run("--brand", "#FFD400", "--out", str(out))
    assert payload["status"] == "unchanged" and payload["stale_rule_pack"] == str(folder)
    # Refused: nothing is written, so the pack still matches what is there.
    refused, payload = _run("--brand", "#3366FF", "--out", str(out))
    assert payload["status"] == "refused" and payload["stale_rule_pack"] is None
    # Rebuilt with the flag: the pack follows the tokens again.
    fresh, payload = _run("--brand", "#FFD400", "--out", str(out), "--rule-pack", "--force")
    assert payload["status"] == "written" and payload["stale_rule_pack"] is None
    assert "## Rule pack" not in (out / "system-report.md").read_text(encoding="utf-8")


def test_a_pack_without_its_digest_cannot_be_matched_and_is_reported(tmp_path):
    out = tmp_path / "ds"
    (out / "rule-pack").mkdir(parents=True)
    (out / "rule-pack" / "README.md").write_text("# mine\n", encoding="utf-8")
    result, payload = _run("--brand", "#3366FF", "--out", str(out))
    assert payload["status"] == "written"
    assert payload["stale_rule_pack"] == str(out / "rule-pack")
    assert "it has no built-from.json" in payload["message"]
    assert (out / "rule-pack" / "README.md").read_text(encoding="utf-8") == "# mine\n"


def test_no_pack_folder_reports_nothing(tmp_path):
    result, payload = _run("--brand", "#3366FF", "--out", str(tmp_path / "ds"))
    assert payload["stale_rule_pack"] is None
    assert "## Rule pack" not in (tmp_path / "ds" / "system-report.md").read_text(
        encoding="utf-8")
