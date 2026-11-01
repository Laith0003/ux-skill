"""Lint judges the page, not the client's own design system.

Two builds inside existing systems showed the linter scoring the client's own
system files as if they were generated output, a single-hue scrim flagged as a
chrome gradient, the button contract's spinner flagged as the default loader,
and the responsive verifier writing every page's screenshots under the same
names. Every system and page here is invented.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from engine.linter.core import lint, lint_text, system_files

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "client_system"
# A token the linter flags inside the client's own token file: a default face.
TOKEN_SLOP = "\n:root { --font-display: Inter; }\n"
# A page rule the linter flags as high: a rainbow gradient.
SLOP = "\n.promo { background: linear-gradient(90deg, #ff0000, #ff8800, #ffee00, #00cc44); }\n"
RAINBOW = "chrome-y-multi-stop-gradient"


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    root = tmp_path / "client"
    shutil.copytree(FIXTURE, root)
    (root / "package.json").write_text('{"name": "client"}', encoding="utf-8")
    color = root / "design-system" / "foundation" / "color.css"
    color.write_text(color.read_text(encoding="utf-8") + TOKEN_SLOP, encoding="utf-8")
    return root


def _ids(findings, name):
    return {f.rule_id for f in findings if Path(f.file).name == name}


def test_the_clients_system_files_are_reported_apart(project: Path) -> None:
    report = lint([project], severity_threshold="high")
    assert any(Path(f).name == "color.css" for f in report.system_files)
    assert "default-font-only" in _ids(report.system_findings, "color.css")
    assert not _ids(report.findings, "color.css"), "a system file's findings never reach the page's list"
    out = report.to_dict()
    assert out["system"]["files"] and out["system"]["findings"]
    assert "do not lower" in out["system"]["note"]


def test_system_files_never_lower_the_score_or_trip_the_exit(project: Path) -> None:
    pages = [p for p in (project / "site").rglob("*") if p.suffix in (".html", ".css")]
    alone = lint(pages, severity_threshold="high")
    whole = lint([project], severity_threshold="high")
    assert whole.score == alone.score
    assert whole.exit_code == alone.exit_code
    assert whole.files_scanned == alone.files_scanned


def test_without_a_system_every_file_counts(tmp_path: Path) -> None:
    page = tmp_path / "styles.css"
    page.write_text(SLOP, encoding="utf-8")
    report = lint([tmp_path], severity_threshold="high")
    assert not report.system_files and "system" not in report.to_dict()
    assert RAINBOW in _ids(report.findings, "styles.css")
    assert report.exit_code == 1


# Files the page or the agent wrote stay scored, even where detect reads
# their tokens: the three shapes that slipped through before.


def _scored(project: Path, rel: str, text: str) -> None:
    path = project / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    report = lint([project], severity_threshold="high")
    assert path.resolve() not in {Path(f).resolve() for f in report.system_files}, rel
    return report


def test_an_app_globals_with_a_theme_block_and_page_rules_is_scored(project: Path) -> None:
    text = (":root {\n  --background: #ffffff;\n  --foreground: #111827;\n  --accent: #0b6e4f;\n"
            "  --muted: #f3f4f6;\n  --border: #e5e7eb;\n  --ring: #0b6e4f;\n}\n"
            "body { background: var(--background); color: var(--foreground); }" + SLOP)
    report = _scored(project, "src/app/globals.css", text)
    assert RAINBOW in _ids(report.findings, "globals.css")
    assert report.exit_code == 1


def test_the_extension_file_beside_the_system_is_scored(project: Path) -> None:
    text = (":root {\n  --harbor-hero-glow: 0 0 40px rgba(28, 100, 217, 0.6);\n"
            "  --harbor-band: #0f2744;\n  --harbor-gap-xl: 7.5rem;\n}\n")
    report = _scored(project, "design-system/foundation/harbor-ext.css", text)
    assert "glow-shadow-zero-offset" in _ids(report.findings, "harbor-ext.css")


def test_a_page_stylesheet_with_a_root_block_is_scored(project: Path) -> None:
    text = (":root { --page-gap: 6rem; --page-ink: #1e2329; --page-band: #eef2f7; }\n"
            ".hero { padding-block: var(--page-gap); }" + SLOP)
    report = _scored(project, "design-system/foundation/landing.css", text)
    assert RAINBOW in _ids(report.findings, "landing.css")


def test_a_file_the_engine_wrote_is_never_the_clients_system(project: Path) -> None:
    from engine.existing.detect import stamp_digest
    from engine.existing.record import RECORD, file_digest
    folder = project / "design-system" / "foundation"
    stamped = folder / "spacing.css"
    stamped.write_text(stamp_digest("---\n:root{--space-1:4px;--space-2:8px;--space-3:12px}\n"),
                       encoding="utf-8")
    listed = folder / "motion.css"
    body = ":root{--motion-fast:120ms;--motion-base:200ms;--motion-slow:320ms}\n"
    listed.write_text(body, encoding="utf-8")
    record = project / "design-system" / RECORD
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps({"files": {"foundation/motion.css": file_digest(body)}}),
                      encoding="utf-8")
    color = folder / "color.css"
    theirs = system_files([stamped, listed, color])
    assert stamped.resolve() not in theirs and listed.resolve() not in theirs
    assert color.resolve() in theirs


# ------------------------------------------------------------- scrims


@pytest.mark.parametrize("css,fires", [
    ((".m::after{background:linear-gradient(180deg, rgba(10,20,30,0) 0%, rgba(10,20,30,.3) 40%, "
      "rgba(10,20,30,.6) 70%, rgba(10,20,30,.9) 100%)}"), False),
    (".m::after{background:linear-gradient(to top, #0a141ee6, #0a141e99 40%, #0a141e33 70%, transparent)}",
     False),
    (".m::after{background:linear-gradient(0deg, black, rgb(0 0 0 / .5) 40%, #0008 70%, transparent)}", False),
    ((".m::after{background:linear-gradient(180deg, rgba(10,20,30,0), rgba(10,20,30,.3), "
      "rgba(200,20,30,.6), rgba(10,20,30,.9))}"), True),
    (".m{background:linear-gradient(90deg, #ff0000, #ff8800, #ffee00, #00cc44)}", True),
    (".m{background:linear-gradient(90deg, var(--a), var(--a), var(--a), var(--a))}", True),
])
def test_a_single_hue_scrim_is_not_a_chrome_gradient(css, fires):
    fired = "chrome-y-multi-stop-gradient" in {f.rule_id for f in lint_text("a.css", css)}
    assert fired is fires


# ------------------------------------------------------------- the button contract's spinner

_SPINNER = (".btn[aria-busy=true] .btn__spinner{border:2px solid currentColor;"
            "border-top-color:transparent;border-radius:50%;animation:spin .7s linear infinite}")
_LOADER = (".loader{border:4px solid #eee;border-top:4px solid #333;border-radius:50%;"
           "animation:spin 1s linear infinite}")


def _spins(path: Path) -> bool:
    return "loader-spinner-border-default" in {
        f.rule_id for f in lint_text(str(path), path.read_text(encoding="utf-8"))}


def _contract(root: Path, spinner: bool = True) -> Path:
    from engine.contracts.library import SEED_DIR
    folder = root / "design-system" / "rule-pack" / "contracts"
    folder.mkdir(parents=True, exist_ok=True)
    seed = (SEED_DIR / "button.yaml").read_text(encoding="utf-8")
    path = folder / "button.yaml"
    path.write_text(seed if spinner else seed.replace("  - {name: spinner, rtlBehavior: fixed}\n", ""),
                    encoding="utf-8")
    return path


def _sheet(root: Path, text: str, name: str = "button.css") -> Path:
    css = root / "src" / name
    css.parent.mkdir(parents=True, exist_ok=True)
    css.write_text(text, encoding="utf-8")
    return css


def test_the_button_contracts_spinner_is_not_the_default_loader(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    _contract(tmp_path)
    assert not _spins(_sheet(tmp_path, _SPINNER))
    assert _spins(_sheet(tmp_path, _LOADER, "page.css"))


def test_without_a_contract_of_its_own_the_spinner_is_a_finding(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    assert _spins(_sheet(tmp_path, _SPINNER))


def test_a_selector_list_that_also_styles_a_page_loader_keeps_the_finding(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    _contract(tmp_path)
    both = (".loader, .btn .spinner{border:2px solid #eee;border-top-color:#333;"
            "border-radius:50%;animation:spin 1s linear infinite}")
    assert _spins(_sheet(tmp_path, both))


def test_a_project_contract_without_a_spinner_keeps_the_finding(tmp_path: Path) -> None:
    import os

    from engine.contracts.schema import load_contract
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    contract = _contract(tmp_path)
    css = _sheet(tmp_path, _SPINNER)
    assert not _spins(css)
    _contract(tmp_path, spinner=False)
    stat = contract.stat()
    os.utime(contract, (stat.st_atime, stat.st_mtime + 5))
    assert "spinner" not in {p.name for p in load_contract(contract).parts}
    assert _spins(css), "a changed contract is read again"


# ------------------------------------------------------------- screenshots per page


@pytest.mark.skipif(shutil.which("node") is None, reason="the verifier is a Node script")
def test_screenshots_are_named_by_page_so_pages_never_overwrite_each_other(tmp_path: Path) -> None:
    script = (ROOT / "scripts" / "shot-names.mjs").as_uri()
    targets = ["en/index.html", "ar/index.html", "pricing.html", "https://example.test/features/split",
               "https://example.test/"]
    code = (f"import {{ shotName }} from {json.dumps(script)};"
            f"console.log(JSON.stringify({json.dumps(targets)}.map((t) => shotName(t, 360, "
            f"{json.dumps(str(tmp_path))}))));")
    out = subprocess.run(["node", "--input-type=module", "-e", code], capture_output=True, text=True,
                         timeout=60, check=False)
    assert out.returncode == 0, out.stderr
    names = json.loads(out.stdout)
    assert names == ["verify-en-index-360.png", "verify-ar-index-360.png", "verify-pricing-360.png",
                     "verify-example-test-features-split-360.png", "verify-example-test-360.png"]
    assert len(set(names)) == len(names)


def _run_verifier(script: Path, *args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    import os
    return subprocess.run(["node", str(script), *args], capture_output=True, text=True, timeout=60,
                          check=False, env={**os.environ, **(env or {})})


@pytest.mark.skipif(shutil.which("node") is None, reason="the verifier is a Node script")
def test_the_verifier_runs_through_a_symlink_and_never_passes_silently(tmp_path: Path) -> None:
    real = ROOT / "scripts" / "verify-responsive.mjs"
    link = tmp_path / "verify.mjs"
    link.symlink_to(real)
    plugin = tmp_path / "plugin"
    plugin.symlink_to(ROOT)
    page = tmp_path / "page.html"
    page.write_text("<!doctype html><title>x</title><p>x</p>", encoding="utf-8")
    for script in (link, plugin / "scripts" / "verify-responsive.mjs"):
        out = _run_verifier(script)
        assert out.returncode == 2 and "DEGRADED" in out.stdout and "no target" in out.stdout, script
        out = _run_verifier(script, str(page), "360", str(tmp_path),
                            env={"CHROME_BIN": str(tmp_path / "no-chrome")})
        assert out.returncode == 2, (script, out.stdout, out.stderr)
        assert "DEGRADED" in out.stdout and "Chrome" in out.stdout, out.stdout
