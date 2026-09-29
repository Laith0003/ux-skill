"""The engine's record of the files it wrote into a folder: system build
writes it beside the system, each file with the digest of its bytes, and a
file is the engine's while it still matches."""
import hashlib
import json

from engine.existing import stamp_digest
from engine.existing.record import RECORD, engine_wrote, file_digest, read_record, record_text
from engine.foundations.emit import NEUTRAL, NEUTRAL_SOURCE, make_system, write_outcome


def _digest(data):
    return hashlib.sha256(data).hexdigest()[:12]


def test_a_build_records_every_file_it_wrote_with_its_digest(tmp_path):
    system = make_system("#3366ff", NEUTRAL, NEUTRAL_SOURCE, rule_pack=True)
    outcome = write_outcome(system, tmp_path)
    assert outcome["written"] == [*system.files, RECORD]
    doc = json.loads((tmp_path / RECORD).read_text(encoding="utf-8"))
    assert list(doc) == ["files"]
    assert doc["files"] == {n: _digest(system.files[n].encode("utf-8"))
                            for n in sorted(system.files)}
    assert all(engine_wrote(tmp_path, n) for n in system.files)


def test_a_build_with_nothing_new_writes_nothing(tmp_path):
    system = make_system("#3366ff", NEUTRAL, NEUTRAL_SOURCE)
    write_outcome(system, tmp_path)
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert write_outcome(system, tmp_path)["status"] == "unchanged"
    assert {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == before


def test_a_build_without_the_rule_pack_keeps_the_packs_entries(tmp_path):
    with_pack = make_system("#3366ff", NEUTRAL, NEUTRAL_SOURCE, rule_pack=True)
    write_outcome(with_pack, tmp_path)
    other = make_system("#6b4423", NEUTRAL, NEUTRAL_SOURCE)
    assert write_outcome(other, tmp_path, force=True)["status"] == "written"
    listed = read_record(tmp_path)
    assert listed["rule-pack/README.md"] == _digest(
        with_pack.files["rule-pack/README.md"].encode("utf-8"))
    assert listed["tokens.css"] == _digest(other.files["tokens.css"].encode("utf-8"))


def test_the_same_build_into_two_folders_writes_the_same_record(tmp_path):
    system = make_system("#3366ff", NEUTRAL, NEUTRAL_SOURCE)
    write_outcome(system, tmp_path / "one")
    write_outcome(system, tmp_path / "two")
    assert (tmp_path / "one" / RECORD).read_bytes() == (tmp_path / "two" / RECORD).read_bytes()


def test_a_file_is_the_engines_only_while_it_matches(tmp_path):
    (tmp_path / "a.css").write_text("a\n", encoding="utf-8")
    (tmp_path / "b.md").write_text(stamp_digest("# b\n"), encoding="utf-8")
    (tmp_path / "c.css").write_text("c\n", encoding="utf-8")
    (tmp_path / RECORD).parent.mkdir()
    (tmp_path / RECORD).write_text(record_text(tmp_path, {"a.css": "a\n"}), encoding="utf-8")
    assert engine_wrote(tmp_path, "a.css") and engine_wrote(tmp_path, "b.md")
    assert not engine_wrote(tmp_path, "c.css") and not engine_wrote(tmp_path, "missing.css")
    (tmp_path / "a.css").write_text("a edited\n", encoding="utf-8")
    assert not engine_wrote(tmp_path, "a.css")


def test_a_record_that_cannot_be_read_grants_nothing(tmp_path):
    (tmp_path / "a.css").write_text("a\n", encoding="utf-8")
    (tmp_path / RECORD).parent.mkdir()
    for text in ("not json", "[]", '{"files": []}', '{"files": {"a.css": 1}}'):
        (tmp_path / RECORD).write_text(text, encoding="utf-8")
        assert read_record(tmp_path) == {} and not engine_wrote(tmp_path, "a.css")


def test_the_digest_is_twelve_hex_digits_of_the_bytes():
    assert file_digest("a\n") == file_digest(b"a\n") == _digest(b"a\n")
    assert len(file_digest(b"")) == 12
