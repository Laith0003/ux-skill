"""The release checks in scripts/release_checks.py, run as tests: 600 sampled
briefs build, every gallery and fixture system round-trips through DTCG,
CSS, Tailwind and Figma with no mismatch, a build's digest is the same under
several PYTHONHASHSEED values, and the wheel ships engine/io and
engine/foundations and nothing private."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("release_checks",
                                               ROOT / "scripts" / "release_checks.py")
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)

BRIEFS = rc.sample_briefs()
CHUNK = 50


def test_the_sample_is_600_briefs_from_a_fixed_seed():
    assert len(BRIEFS) == rc.SAMPLES == 600
    assert BRIEFS == rc.sample_briefs()
    assert len({b for b, _ in BRIEFS}) > 590


@pytest.mark.parametrize("start", range(0, rc.SAMPLES, CHUNK))
def test_every_sampled_brief_builds(start):
    assert rc.check_briefs(BRIEFS[start:start + CHUNK]) == []


@pytest.mark.parametrize("label", rc.labels())
def test_every_system_round_trips_through_every_format(label):
    problems, counts = rc.round_trip(label, rc.system(label))
    assert problems == []
    assert all(n > 1000 for n in counts.values()), counts


def _fixture():
    from engine.foundations import build_system
    from engine.synthesizer.axes import AxisValues
    brand, axes = rc.FIXTURES[0]
    return build_system(AxisValues(*axes), brand).tokens


def _read(text, reader, name, fmt):
    import hashlib

    from engine.io.report import Source
    data = text.encode()
    return reader(text, Source(path=name, format=fmt, sha256=hashlib.sha256(data).hexdigest(),
                               size=len(data))).tokens


def test_a_mismatch_is_named():
    from engine.foundations.tokens import Token
    ts = _fixture()
    other = _fixture()
    del other._tokens["space.4"]
    other.add(Token("space.4", "dimension", {"value": 99, "unit": "px"}))
    problems, _ = rc._compare("fixture", "dtcg", ts, other)
    hit = [p for p in problems if p.startswith("fixture dtcg: space.4 ")]
    assert hit and "wrote 16.0 and read back 99.0" in hit[0]


def test_a_token_dropped_on_the_way_back_is_named():
    ts = _fixture()
    back = _fixture()
    # A token no other token points at, so the rest still resolve.
    leaf = "space.control.padding-inline"
    assert ts.has(leaf) and not any(f"{{{leaf}}}" in str(t.value) for t in ts.tokens())
    del back._tokens[leaf]
    problems, _ = rc._compare("fixture", "dtcg", ts, back)
    assert f"fixture dtcg: {leaf} was written and nothing was read back for it" in problems


def test_a_token_read_back_that_was_never_written_is_named():
    from engine.foundations.tokens import Token
    ts = _fixture()
    back = _fixture()
    back.add(Token("space.invented", "dimension", {"value": 3, "unit": "px"}))
    problems, _ = rc._compare("fixture", "dtcg", ts, back)
    assert ("fixture dtcg: read back space.invented, which stands for no token the export "
            "wrote") in problems


def test_a_text_style_field_lost_on_the_way_back_is_named():
    from engine.foundations import to_css
    from engine.io.css_in import import_css
    ts = _fixture()
    text = "\n".join(line for line in to_css(ts).split("\n")
                     if not line.strip().startswith("--type-text-display-line-height:"))
    problems, _ = rc._compare("fixture", "css", ts, _read(text, import_css, "tokens.css", "css"))
    assert "fixture css: type.text.display lost lineHeight on the way back" in problems


def test_a_tailwind_role_written_wrong_is_named():
    import re

    from engine.io.tailwind_in import import_tailwind_css
    from engine.io.tailwind_out import roles_set, to_tailwind
    ts = _fixture()
    text = re.sub(r"(  --spacing-control-gap: )[^;]+;", r"\g<1>77px;", to_tailwind(ts, roles=True),
                  count=1)
    back = _read(text, import_tailwind_css, "theme.css", "tailwind")
    problems, _ = rc._compare("fixture", "tailwind", roles_set(ts), back)
    assert any(p.startswith("fixture tailwind: spacing-control-gap in ") and "77.0" in p
               for p in problems)


def test_figma_leaves_out_only_what_its_export_names_as_skipped():
    import json

    from engine.io.figma_in import import_figma
    from engine.io.figma_out import as_export, to_figma
    ts = _fixture()
    figma = to_figma(ts)
    back = _read(json.dumps(as_export(figma)), import_figma, "variables.json", "figma")
    skipped = {s["token"] for s in figma["skipped"]}
    assert skipped and rc._compare("fixture", "figma", ts, back, skipped)[0] == []
    missed = rc._compare("fixture", "figma", ts, back)[0]
    assert {p.split(": ")[1].split(" ")[0] for p in missed} == skipped


def test_a_gallery_entry_that_cannot_be_built_fails_the_round_trip(tmp_path, monkeypatch):
    (tmp_path / "broken.json").write_text('{"id": "broken", "brand": "#3366FF"}',
                                          encoding="utf-8")
    monkeypatch.setattr(rc, "GALLERY", tmp_path)
    assert rc.gallery_problems() == [
        "data/gallery/broken.json has no axes; rebuild it with python scripts/build_gallery.py"]


def test_the_build_digest_is_stable_across_hash_seeds():
    assert rc.check_digest() == []


def test_the_wheel_rules_name_what_is_missing_and_what_is_private():
    problems = rc.check_wheel_names(["engine/io/read.py", "PLAN-4.0.md", "engine/x.pyc"])
    assert any("engine/foundations/" in p for p in problems)
    assert any("PLAN-4.0.md" in p for p in problems) and any(".pyc" in p for p in problems)
    assert rc.check_wheel_names(["engine/io/read.py", "engine/foundations/build.py"]) == []


def test_the_wheel_is_built_from_the_tracked_sources_only(tmp_path):
    names = rc.tracked_files()
    if not names:
        pytest.skip("not a git checkout, so the build uses the checkout itself")
    assert "engine/__init__.py" in names and not any(n.startswith("build/") for n in names)
    tree = rc.source_tree(tmp_path)
    assert (tree / "engine" / "__init__.py").is_file() and not (tree / "build").exists()


def test_the_built_wheel_ships_the_engine_and_nothing_private():
    # Only a machine without the build backend skips; a failing build fails.
    if importlib.util.find_spec("setuptools") is None:
        pytest.skip("setuptools is not installed, so no wheel can be built here")
    assert rc.check_wheel() == []
