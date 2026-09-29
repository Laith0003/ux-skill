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
# A line the linter flags as high: a rainbow gradient in the client's own file.
SLOP = "\n.promo { background: linear-gradient(90deg, #ff0000, #ff8800, #ffee00, #00cc44); }\n"


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    root = tmp_path / "client"
    shutil.copytree(FIXTURE, root)
    (root / "package.json").write_text('{"name": "client"}', encoding="utf-8")
    color = root / "design-system" / "foundation" / "color.css"
    color.write_text(color.read_text(encoding="utf-8") + SLOP, encoding="utf-8")
    return root


def _ids(findings, name):
    return {f.rule_id for f in findings if Path(f.file).name == name}


def test_the_clients_system_files_are_reported_apart(project: Path) -> None:
    report = lint([project], severity_threshold="high")
    assert any(Path(f).name == "color.css" for f in report.system_files)
    assert "chrome-y-multi-stop-gradient" in _ids(report.system_findings, "color.css")
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
    assert "chrome-y-multi-stop-gradient" in _ids(report.findings, "styles.css")
    assert report.exit_code == 1


def test_a_file_ux_skill_wrote_is_never_the_clients_system(project: Path) -> None:
    from engine.existing.detect import stamp_digest
    ours = project / "design-system" / "foundation" / "extension.css"
    ours.write_text(stamp_digest("---\n/* engine extension */\n:root{--x:1px}\n"), encoding="utf-8")
    theirs = system_files([ours, project / "design-system" / "foundation" / "color.css"])
    assert ours.resolve() not in theirs
    assert (project / "design-system" / "foundation" / "color.css").resolve() in theirs


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


def test_the_button_contracts_spinner_is_not_the_default_loader(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    css = tmp_path / "button.css"
    css.write_text(_SPINNER, encoding="utf-8")
    assert not _spins(css)
    page = tmp_path / "page.css"
    page.write_text(_LOADER, encoding="utf-8")
    assert _spins(page)


def test_a_project_contract_without_a_spinner_keeps_the_finding(tmp_path: Path) -> None:
    from engine.contracts.library import SEED_DIR
    from engine.contracts.schema import load_contract
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    contracts = tmp_path / "design-system" / "rule-pack" / "contracts"
    contracts.mkdir(parents=True)
    seed = (SEED_DIR / "button.yaml").read_text(encoding="utf-8")
    no_spinner = contracts / "button.yaml"
    no_spinner.write_text(seed.replace("  - {name: spinner, rtlBehavior: fixed}\n", ""), encoding="utf-8")
    assert "spinner" not in {p.name for p in load_contract(no_spinner).parts}
    css = tmp_path / "src" / "button.css"
    css.parent.mkdir()
    css.write_text(_SPINNER, encoding="utf-8")
    assert _spins(css)


# ------------------------------------------------------------- screenshots per page


@pytest.mark.skipif(shutil.which("node") is None, reason="the verifier is a Node script")
def test_screenshots_are_named_by_page_so_pages_never_overwrite_each_other(tmp_path: Path) -> None:
    script = (ROOT / "scripts" / "verify-responsive.mjs").as_uri()
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
