"""The private guards find the private source from any checkout: a main
checkout, a linked worktree, or a detached worktree far from both. When they
skip, the reason says where they looked and how to point them."""
import subprocess

from tests.foundations.test_no_licensed_text import _find_private_source, _skip_reason


def _git(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def test_the_private_source_is_found_beside_the_main_checkout(tmp_path):
    # A detached worktree lives far from the main checkout. The guards must
    # still find the private folder that sits beside the main checkout.
    main = tmp_path / "code" / "repo"
    main.mkdir(parents=True)
    _git("init", "-q", cwd=main)
    _git("-c", "user.email=t@example.invalid", "-c", "user.name=t",
         "commit", "-q", "--allow-empty", "-m", "start", cwd=main)
    private = tmp_path / "code" / "held"
    private.mkdir()
    (private / "private-terms.txt").write_text("", encoding="utf-8")
    worktree = tmp_path / "elsewhere" / "wt"
    _git("worktree", "add", "-q", "--detach", str(worktree), cwd=main)

    found, looked = _find_private_source(worktree, {})
    assert found == private.resolve()
    assert main.resolve().parent in looked

    named = tmp_path / "named"
    found, looked = _find_private_source(worktree, {"UXSKILL_PRIVATE_SOURCE": str(named)})
    assert found == named and looked == []


def test_a_skip_names_where_it_looked_and_the_variable_to_set(tmp_path):
    lone = tmp_path / "lone" / "repo"
    lone.mkdir(parents=True)
    found, looked = _find_private_source(lone, {})
    assert found is None
    reason = _skip_reason(looked)
    assert str(lone.resolve().parent) in reason
    assert "UXSKILL_PRIVATE_SOURCE" in reason
