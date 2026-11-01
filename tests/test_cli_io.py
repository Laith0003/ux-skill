"""`uxskill system import|enhance|extend|export` and `uxskill contracts
check`: thin wiring over engine.io.commands, with plain JSON on stdout, the
exit code by status, and a bad input as a usage error that names the flag."""
import json

import pytest

click = pytest.importorskip("click")
from click.testing import CliRunner  # noqa: E402

from engine.cli.main import cli  # noqa: E402
from engine.contracts.library import SEED_DIR  # noqa: E402
from engine.foundations.build import build_system  # noqa: E402
from engine.foundations.export import dump_dtcg  # noqa: E402
from engine.synthesizer.axes import AxisValues  # noqa: E402

THEME = ":root { --ink: #1b1d22; --paper: #fdfdfb; --text-body: var(--ink); }\n"


def _runner():
    try:
        return CliRunner(mix_stderr=False)
    except TypeError:
        return CliRunner()


def _run(*args):
    result = _runner().invoke(cli, ["--no-pretty", *args])
    payload = json.loads(result.stdout) if result.stdout.strip().startswith("{") else None
    return result, payload


def _source(tmp_path):
    f = tmp_path / "theme.css"
    f.write_text(THEME, encoding="utf-8")
    return f


def _tokens(tmp_path, name="tokens.json", **kw):
    f = tmp_path / name
    f.write_text(dump_dtcg(build_system(AxisValues(*[0.5] * 7), "#3366FF", **kw).tokens),
                 encoding="utf-8")
    return f


def test_the_system_group_lists_the_new_commands():
    result = _runner().invoke(cli, ["system", "--help"])
    for name in ("build", "import", "enhance", "extend", "export"):
        assert f"  {name} " in result.output


def test_import_prints_the_result_and_writes_with_out(tmp_path):
    src = _source(tmp_path)
    result, payload = _run("system", "import", "--from", str(src))
    assert result.exit_code == 0 and payload["status"] == "read"
    result, payload = _run("system", "import", "--from", str(src), "--out",
                           str(tmp_path / "out"))
    assert result.exit_code == 0 and payload["status"] == "written"
    assert (tmp_path / "out" / "mapping.json").is_file()


def test_from_repeats_to_read_a_stylesheet_with_the_system(tmp_path):
    src = _source(tmp_path)
    dark = tmp_path / "globals.css"
    dark.write_text(".dark { --text-body: var(--paper); }\n", encoding="utf-8")
    result, payload = _run("system", "import", "--from", str(src), "--from", str(dark))
    assert result.exit_code == 0 and payload["also_read"][0]["path"] == str(dark)
    assert payload["axes"] == {"scheme": ["light", "dark"]}


def test_enhance_takes_code_folders(tmp_path):
    src = _source(tmp_path)
    code = tmp_path / "code"
    code.mkdir()
    (code / "a.css").write_text(".x { color: var(--text-body); }\n", encoding="utf-8")
    result, payload = _run("system", "enhance", "--from", str(src), "--scan", str(code))
    assert result.exit_code == 0 and payload["summary"]["unused"] == 1  # paper
    assert "unknown_classes" in payload["summary"]


def test_extend_exits_1_when_blocked_and_names_a_bad_flag(tmp_path):
    src = _source(tmp_path)
    ok, payload = _run("system", "extend", "--from", str(src), "--add", "radius", "--out",
                       str(tmp_path / "a"))
    assert ok.exit_code == 0 and payload["status"] == "written"
    assert (tmp_path / "theme-ext.css").is_file()
    blocked, payload = _run("system", "extend", "--from", str(src), "--add-role",
                            "color.surface.page=ink", "--out", str(tmp_path / "b"))
    assert blocked.exit_code == 1 and payload["status"] == "blocked"
    bad, _ = _run("system", "extend", "--from", str(src), "--add-role", "ink", "--out",
                  str(tmp_path / "c"))
    assert bad.exit_code == 2
    assert "--add-role ink needs the form role=token" in bad.stderr


def test_export_to_figma_and_a_bad_figma_mode(tmp_path):
    tokens = _tokens(tmp_path)
    result, payload = _run("system", "export", "--from", str(tokens), "--to", "figma", "--out",
                           str(tmp_path / "fig"))
    assert result.exit_code == 0 and payload["status"] == "written"
    bad, _ = _run("system", "import", "--from", str(tokens), "--figma-mode", "Type")
    assert bad.exit_code == 2 and "--figma-mode Type needs the form collection=mode" in bad.stderr
    other, _ = _run("system", "import", "--from", str(tokens), "--figma-mode", "Type=SM")
    assert other.exit_code == 2 and "--figma-mode is for a Figma variables export" in other.stderr


def test_contracts_check_exits_by_the_result(tmp_path):
    tokens = _tokens(tmp_path)
    result, payload = _run("contracts", "check", str(SEED_DIR), "--tokens", str(tokens))
    assert result.exit_code == 0 and payload["status"] == "passed"
    small = _tokens(tmp_path, "small.json", foundations=("color",))
    result, payload = _run("contracts", "check", str(SEED_DIR), "--tokens", str(small))
    assert result.exit_code == 1 and payload["status"] == "failed" and payload["problems"]


def test_extend_names_the_brief_fields_and_export_takes_the_scheme(tmp_path):
    from engine.foundations.audience import FIELDS
    text = " ".join(_runner().invoke(cli, ["system", "extend", "--help"]).output.split())
    assert all(name in text for name in FIELDS) and "headline" in text
    tokens = _tokens(tmp_path)
    result, payload = _run("system", "export", "--from", str(tokens), "--to", "css",
                           "--scheme", "dark", "--out", str(tmp_path / "out"))
    assert result.exit_code == 0 and payload["status"] == "written"
    assert ':root:not([data-theme="light"]) {' in (tmp_path / "out" / "tokens.css").read_text()
