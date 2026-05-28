"""`ux` / `uxskill` command-line entry point.

Subcommands
-----------
``ux init``             -- detect IDEs and install for all
``ux install <ide>``    -- install for a specific IDE
``ux recommend``        -- run the 5-parallel-search engine
``ux lint``             -- run the anti-AI-slop linter
``ux discover``         -- run the 10-field discovery flow
``ux generate``         -- emit tokens + manifest from a recommendation
``ux persist save``     -- write MASTER.md from a recommendation + brief
``ux persist save-page``-- write a per-page .md from a brief + output
``ux persist load``     -- read MASTER.md back as JSON
``ux persist list``     -- list page names persisted under pages/
``ux stats``            -- show data manifest counts
``ux version``          -- print version
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import List, Optional

try:
    import click
except ImportError:  # pragma: no cover - allow `python -m engine.cli.main version`
    click = None  # type: ignore

# Ensure parent of `engine` is on sys.path when invoked as a script
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from engine import __version__
from engine.data_loader import stats as data_stats, load
from engine.recommender import recommend as run_recommend, Brief
from engine.linter import lint as run_lint
from engine.discovery import FIELDS, DiscoveryState, next_question, record, is_complete, serialize
from engine.generator import generate as run_generate
from engine.installer import install as run_install, detect_ides, SUPPORTED
from engine.persist import save_master, save_page, load_master, list_pages


def _emit(payload, pretty: bool) -> None:
    if pretty:
        try:
            from rich.console import Console
            from rich.json import JSON
            Console().print(JSON.from_data(payload))
            return
        except ImportError:
            pass
    print(json.dumps(payload, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# click-less fallback for `python engine/cli/main.py version`
# ---------------------------------------------------------------------------

def _fallback(argv: List[str]) -> int:
    if not argv or argv[0] in ("version", "-v", "--version"):
        print(__version__)
        return 0
    if argv[0] == "stats":
        print(json.dumps(data_stats(), indent=2))
        return 0
    print("Install `click` for the full CLI:  pip install click rich", file=sys.stderr)
    return 2


if click is None:                          # pragma: no cover
    def cli() -> int:
        return _fallback(sys.argv[1:])
else:
    @click.group(invoke_without_command=True)
    @click.option("--pretty/--no-pretty", default=True, help="Rich output (default) or plain JSON.")
    @click.version_option(__version__, "-v", "--version")
    @click.pass_context
    def cli(ctx: click.Context, pretty: bool) -> None:
        """ux-skill v2 — design intelligence for AI coding."""
        ctx.ensure_object(dict)
        ctx.obj["pretty"] = pretty
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    # -------- ux init ----------------------------------------------------

    @cli.command("init")
    @click.option("--root", default=".", help="Project root.")
    @click.option("--dry-run", is_flag=True, help="Show what would be written without writing.")
    @click.option("--global", "global_install", is_flag=True,
                  help="Install at the user level (~/.config/ux-skill) instead of the project root.")
    @click.option("--offline", is_flag=True,
                  help="Skip any network calls. Fail fast if the engine needs to fetch.")
    @click.pass_context
    def init_cmd(ctx, root: str, dry_run: bool, global_install: bool, offline: bool) -> None:
        """Detect IDEs in the project root and install for each.

        --global  : install at ~/.config/ux-skill (Pro Max parity)
        --offline : skip all network calls; use only local manifests
        """
        if global_install:
            root = str(Path.home() / ".config" / "ux-skill")
            Path(root).mkdir(parents=True, exist_ok=True)
        if offline:
            import os
            os.environ["UX_SKILL_OFFLINE"] = "1"
        detected = detect_ides(Path(root))
        if not detected:
            detected = ["claude-code"]
        reports = [run_install(t, root, dry_run).to_dict() for t in detected]
        _emit({
            "detected": detected,
            "installs": reports,
            "mode": {"global": global_install, "offline": offline},
            "root": root,
        }, ctx.obj["pretty"])

    # -------- ux install -------------------------------------------------

    @cli.command("install")
    @click.argument("target", type=click.Choice(SUPPORTED, case_sensitive=False))
    @click.option("--root", default=".")
    @click.option("--dry-run", is_flag=True)
    @click.option("--global", "global_install", is_flag=True,
                  help="Install at ~/.config/ux-skill instead of project root.")
    @click.option("--offline", is_flag=True, help="Skip network; use local manifests only.")
    @click.pass_context
    def install_cmd(ctx, target: str, root: str, dry_run: bool,
                    global_install: bool, offline: bool) -> None:
        """Install for a specific IDE."""
        if global_install:
            root = str(Path.home() / ".config" / "ux-skill")
            Path(root).mkdir(parents=True, exist_ok=True)
        if offline:
            import os
            os.environ["UX_SKILL_OFFLINE"] = "1"
        report = run_install(target, root, dry_run)
        _emit(report.to_dict(), ctx.obj["pretty"])

    # -------- ux recommend -----------------------------------------------

    @cli.command("recommend")
    @click.option("--project-type", default="")
    @click.option("--industry", default="")
    @click.option("--audience", multiple=True)
    @click.option("--tone", multiple=True)
    @click.option("--must-have", multiple=True)
    @click.option("--forbidden", multiple=True)
    @click.option("--stack", default="")
    @click.option("--region", default="")
    @click.option("--brief-file", type=click.Path(exists=True), help="JSON brief file.")
    @click.pass_context
    def recommend_cmd(ctx, project_type, industry, audience, tone, must_have, forbidden,
                      stack, region, brief_file) -> None:
        """Run the 5-parallel-search recommender."""
        if brief_file:
            payload = json.loads(Path(brief_file).read_text(encoding="utf-8"))
            brief = Brief(**payload)
        else:
            brief = Brief(
                project_type=project_type,
                industry=industry,
                audience=list(audience),
                tone=list(tone),
                must_have=list(must_have),
                forbidden=list(forbidden),
                stack=stack,
                region=region,
            )
        rec = run_recommend(brief)
        _emit(rec.to_dict(), ctx.obj["pretty"])

    # -------- ux lint ----------------------------------------------------

    @cli.command("lint")
    @click.argument("paths", nargs=-1, type=click.Path(exists=True))
    @click.option("--threshold", default="high",
                  type=click.Choice(["low", "medium", "high", "critical"]),
                  help="Lowest severity that causes a non-zero exit.")
    @click.pass_context
    def lint_cmd(ctx, paths, threshold) -> None:
        """Run the anti-AI-slop linter."""
        report = run_lint(paths or ["."], severity_threshold=threshold)
        _emit(report.to_dict(), ctx.obj["pretty"])
        sys.exit(report.exit_code)

    # -------- ux discover ------------------------------------------------

    @cli.command("discover")
    @click.option("--load-state", type=click.Path(exists=True),
                  help="Resume from a saved discovery JSON.")
    @click.option("--save", type=click.Path(), default=".ux/last-discovery.json")
    @click.pass_context
    def discover_cmd(ctx, load_state, save) -> None:
        """Interactive 10-field discovery flow. The forcing function."""
        if load_state:
            payload = json.loads(Path(load_state).read_text(encoding="utf-8"))
            state = DiscoveryState(answers=payload.get("answers", {}))
        else:
            state = DiscoveryState()

        while not is_complete(state):
            q = next_question(state)
            if q is None:
                break
            click.echo(click.style(f"\n[{q['id']}] {q['label']}", bold=True))
            click.echo(click.style(f"  hint: {q['hint']}", fg="bright_black"))
            value = click.prompt("  >", default="", show_default=False)
            record(state, q["id"], value)

        save_path = Path(save)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(serialize(state), indent=2, ensure_ascii=False), encoding="utf-8")
        click.echo(f"\nDiscovery saved to {save_path}")
        _emit(serialize(state), ctx.obj["pretty"])

    # -------- ux generate ------------------------------------------------

    @cli.command("generate")
    @click.option("--brief-file", type=click.Path(exists=True), required=False)
    @click.option("--out-dir", default="./.ux/generated")
    @click.pass_context
    def generate_cmd(ctx, brief_file, out_dir) -> None:
        """Emit tokens + manifest from a recommendation."""
        if brief_file:
            brief_payload = json.loads(Path(brief_file).read_text(encoding="utf-8"))
            brief = Brief(**brief_payload)
        else:
            brief = Brief()
        rec = run_recommend(brief)
        bundle = run_generate(rec, brief, out_dir)
        _emit(bundle.to_dict(), ctx.obj["pretty"])

    # -------- ux persist -------------------------------------------------

    @cli.group("persist")
    @click.pass_context
    def persist_grp(ctx) -> None:
        """Write/read MASTER.md and per-page state under .ux/design-system/."""

    def _load_recommendation_dict(rec_path: Optional[str], brief_obj: Brief) -> dict:
        if rec_path and Path(rec_path).exists():
            return json.loads(Path(rec_path).read_text(encoding="utf-8"))
        rec = run_recommend(brief_obj)
        return rec.to_dict()

    def _load_brief_dict(brief_path: Optional[str]) -> dict:
        if not brief_path:
            return {}
        path = Path(brief_path)
        if not path.exists():
            return {}
        payload = json.loads(path.read_text(encoding="utf-8"))
        # Discovery files wrap answers under "answers"; recommend briefs are flat.
        if isinstance(payload, dict) and "answers" in payload and isinstance(payload["answers"], dict):
            return dict(payload["answers"])
        return payload if isinstance(payload, dict) else {}

    def _brief_dict_to_dataclass(brief_dict: dict) -> Brief:
        keep = {
            "project_type", "industry", "audience", "tone",
            "must_have", "forbidden", "stack", "region",
        }
        kwargs = {k: v for k, v in brief_dict.items() if k in keep}
        # Defensive: Brief expects list fields as lists.
        for list_field in ("audience", "tone", "must_have", "forbidden"):
            value = kwargs.get(list_field)
            if isinstance(value, str):
                kwargs[list_field] = [v.strip() for v in value.split(",") if v.strip()]
        return Brief(**kwargs)

    @persist_grp.command("save")
    @click.option("--project-root", default=".", help="Project root that owns the .ux/ directory.")
    @click.option("--from-recommendation", "from_recommendation",
                  default=".ux/last-recommendation.json",
                  help="Path to a recommendation JSON.")
    @click.option("--from-brief", "from_brief",
                  default=".ux/last-discovery.json",
                  help="Path to a discovery JSON (or any brief dict).")
    @click.pass_context
    def persist_save_cmd(ctx, project_root, from_recommendation, from_brief) -> None:
        """Write MASTER.md from a saved recommendation + brief."""
        brief_dict = _load_brief_dict(from_brief)
        brief_obj = _brief_dict_to_dataclass(brief_dict)
        rec_dict = _load_recommendation_dict(from_recommendation, brief_obj)
        path = save_master(project_root, rec_dict, brief_dict)
        _emit({"path": path}, ctx.obj["pretty"])

    @persist_grp.command("save-page")
    @click.argument("name")
    @click.option("--project-root", default=".")
    @click.option("--from-brief", "from_brief", default=".ux/last-discovery.json")
    @click.option("--from-output", "from_output", default="",
                  help="Path to a generator output JSON (manifest.json or bundle.to_dict()).")
    @click.pass_context
    def persist_save_page_cmd(ctx, name, project_root, from_brief, from_output) -> None:
        """Write .ux/design-system/pages/<name>.md."""
        brief_dict = _load_brief_dict(from_brief)
        output: dict = {}
        if from_output and Path(from_output).exists():
            payload = json.loads(Path(from_output).read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                output = payload
        path = save_page(project_root, name, brief_dict, output)
        _emit({"path": path}, ctx.obj["pretty"])

    @persist_grp.command("load")
    @click.option("--project-root", default=".")
    @click.pass_context
    def persist_load_cmd(ctx, project_root) -> None:
        """Read MASTER.md back as JSON."""
        data = load_master(project_root)
        if data is None:
            _emit({"path": None, "error": "no MASTER.md at this project root"}, ctx.obj["pretty"])
            sys.exit(1)
        _emit(data, ctx.obj["pretty"])

    @persist_grp.command("list")
    @click.option("--project-root", default=".")
    @click.pass_context
    def persist_list_cmd(ctx, project_root) -> None:
        """List page names persisted under pages/."""
        names = list_pages(project_root)
        _emit({"pages": names, "count": len(names)}, ctx.obj["pretty"])

    # -------- ux stats ---------------------------------------------------

    @cli.command("stats")
    @click.pass_context
    def stats_cmd(ctx) -> None:
        """Show data manifest counts."""
        _emit({"version": __version__, "counts": data_stats()}, ctx.obj["pretty"])

    # -------- ux version -------------------------------------------------

    @cli.command("version")
    def version_cmd() -> None:
        click.echo(__version__)


if __name__ == "__main__":
    if click is None:
        sys.exit(_fallback(sys.argv[1:]))
    cli()
