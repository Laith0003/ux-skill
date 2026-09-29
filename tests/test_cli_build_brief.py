"""The brief's headline on system build (the landing display fits its
longest word), and the record an unchanged build writes into a folder
built before the record existed, so --force can later tell the engine's
files from the owner's edits."""
import json

import pytest

click = pytest.importorskip("click")
from click.testing import CliRunner  # noqa: E402

from engine.cli.main import cli  # noqa: E402
from engine.existing.record import RECORD, read_record  # noqa: E402
from engine.foundations.emit import InputError, brief_words, unread_lines  # noqa: E402


def _runner():
    try:
        return CliRunner(mix_stderr=False)
    except TypeError:
        return CliRunner()


def _run(*args):
    result = _runner().invoke(cli, ["--no-pretty", *args])
    payload = json.loads(result.stdout) if result.stdout.strip().startswith("{") else None
    return result, payload


def test_the_headline_gives_its_longest_word_per_script():
    assert brief_words(None) is None and brief_words({"tone": ["calm"]}) is None
    assert brief_words({"headline": "Pay anyone in seconds"}) == {"latin": 7}
    assert brief_words({"headline": ["Well-made", "مرحبا "
                                                  "بالعالم"]}) \
        == {"latin": 4, "arabic": 7}
    assert brief_words({"answers": {"headline": "Go far"}}) == {"latin": 3}
    assert unread_lines({"tone": ["calm"], "headline": "Go far"}) == []


@pytest.mark.parametrize("value, message", [
    (4, "brief field headline is 4; give the page's headline as text, for example "
        '"headline": "Pay anyone in seconds", or a list of the page\'s headlines'),
    ("12 !", "brief field headline is '12 !', which has no word; give the page's headline as "
             'text, for example "headline": "Pay anyone in seconds"'),
    ("a" * 41, "brief field headline has the word aaaaaaaaaaaaaaaaaaaa... of 41 letters; the "
               "display fits words of up to 40, so break it or write the headline as the page "
               "shows it"),
])
def test_a_headline_that_cannot_be_read_names_the_field_and_the_fix(value, message):
    with pytest.raises(InputError) as exc:
        brief_words({"headline": value})
    assert str(exc.value) == message


def _fit(folder):
    doc = json.loads((folder / "tokens.json").read_text(encoding="utf-8"))
    return doc["type"]["fit-word"]["latin"]["$value"]


def test_the_briefs_headline_sizes_the_display_on_system_build(tmp_path):
    brief = tmp_path / "brief.json"
    brief.write_text(json.dumps({"tone": ["calm"], "headline": "Pay anyone in seconds"}),
                     encoding="utf-8")
    result, _ = _run("system", "build", "--brand", "#3366FF", "--brief", str(brief), "--out",
                     str(tmp_path / "a"))
    assert result.exit_code == 0 and _fit(tmp_path / "a") == 7
    brief.write_text(json.dumps({"tone": ["calm"]}), encoding="utf-8")
    result, _ = _run("system", "build", "--brand", "#3366FF", "--brief", str(brief), "--out",
                     str(tmp_path / "c"))
    assert result.exit_code == 0 and _fit(tmp_path / "c") == 13
    brief.write_text(json.dumps({"tone": ["calm"], "headline": ["Go", 4]}), encoding="utf-8")
    bad, _ = _run("system", "build", "--brand", "#3366FF", "--brief", str(brief), "--out",
                  str(tmp_path / "b"))
    assert bad.exit_code == 2 and "--brief field headline is ['Go', 4]; give the page's " \
        "headline as text" in bad.stderr


def test_an_unchanged_build_of_an_older_folder_writes_the_record(tmp_path):
    out = tmp_path / "ds"
    args = ("system", "build", "--brand", "#3366FF", "--out", str(out))
    first, _ = _run(*args)
    assert first.exit_code == 0 and read_record(out)
    # A folder built before the record existed has none.
    (out / RECORD).unlink()
    again, payload = _run(*args)
    assert again.exit_code == 0 and payload["status"] == "unchanged"
    assert payload["message"].endswith(f"Recorded the files in {out / RECORD}, so --force can "
                                       "tell them from files you edit.")
    assert "tokens.json" in read_record(out)
    # With the record in place, nothing more is written.
    third, payload = _run(*args)
    assert third.exit_code == 0 and "Recorded" not in payload["message"]
