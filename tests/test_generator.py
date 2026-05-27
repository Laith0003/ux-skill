"""Generator smoke tests — Recommendation → emitted bundle."""
from pathlib import Path

from engine.recommender import recommend, Brief
from engine.generator import generate


def test_generate_writes_files(tmp_path: Path):
    rec = recommend(Brief())
    bundle = generate(rec, Brief(), str(tmp_path))
    assert (tmp_path / "tokens.css").exists()
    assert (tmp_path / "manifest.json").exists()
    assert "tokens.css" in bundle.files_written[0]


def test_generated_tokens_has_guardrail_header(tmp_path: Path):
    rec = recommend(Brief())
    generate(rec, Brief(), str(tmp_path))
    css = (tmp_path / "tokens.css").read_text()
    assert "ux-skill v2" in css
    assert ":root" in css
