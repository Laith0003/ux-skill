"""Unit tests for engine.persist — MASTER.md persistence.

Covers:
- save_master writes the expected file shape (frontmatter + body)
- save → load roundtrip preserves project + body
- save_page creates the pages/ directory on demand
- list_pages returns the persisted page names
- save_master is idempotent: same inputs → same bytes (timestamp preserved)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from engine.persist import save_master, save_page, load_master, list_pages


def _make_brief() -> Dict[str, Any]:
    return {
        "project": "test-loyalty",
        "project_type": "landing",
        "audience": ["B2C", "mobile-first", "MENA region"],
        "primary_goal": "Trial signup",
        "tone": ["warm", "editorial", "trustworthy"],
        "must_have": ["dark-mode", "rtl-arabic", "a11y-AA"],
        "forbidden": ["brutalism", "purple-gradients", "emoji-in-ui"],
        "reference_brands": ["Stripe", "Linear", "Mercury"],
        "stack": "nextjs-15-app-router",
        "region": "mena",
        "success_metric": "Signup CR > 4%",
    }


def _make_recommendation() -> Dict[str, Any]:
    return {
        "style": {
            "id": "monochrome-precise",
            "name": "Monochrome Precise",
            "philosophy": "Black is chrome, white is canvas, negative space is the system.",
            "category": "minimalist",
            "tokens": {"color": "monochrome", "motion": "minimal"},
            "exemplars": ["stripe", "linear"],
        },
        "palette": {
            "id": "linear-graphite",
            "name": "Linear Graphite",
            "tone": ["precise", "calm"],
            "colors": {
                "background": "#0e0f12",
                "foreground": "#f4f5f7",
                "accent": "#5e6ad2",
            },
            "contrast_scores": {"fg_on_bg": 16.4},
        },
        "type_pair": {
            "id": "cormorant-inter-jetbrains",
            "name": "Cormorant Garamond x Inter x JetBrains Mono",
            "display": {"family": "Cormorant Garamond", "weights": [400, 500]},
            "body": {"family": "Inter", "weights": [400, 500, 600]},
            "mono": {"family": "JetBrains Mono", "weights": [400]},
            "character": ["editorial", "precise"],
        },
        "motion": [
            {"id": "fade-up-12px", "name": "fade-up-12px",
             "tokens": {"easing": "cubic-bezier(0.16, 1, 0.3, 1)", "duration": "360ms"}},
            {"id": "slide-in", "name": "slide-in",
             "tokens": {"easing": "ease-out", "duration": "240ms"}},
        ],
        "components": [
            {"id": "stat-card-magnetic", "category": "data-display"},
            {"id": "command-palette", "category": "navigation"},
        ],
        "brand_exemplars": [
            {"id": "stripe", "category": "Fintech Infrastructure"},
            {"id": "linear", "category": "Developer Tools"},
        ],
        "guardrails": [
            {"id": "no-purple-blue-gradient", "name": "No purple-to-blue gradient",
             "severity": "high", "category": "color"},
            {"id": "no-emoji-icons", "name": "No emoji as icons",
             "severity": "high", "category": "iconography"},
            {"id": "min-tap-target", "name": "Minimum tap target 44px",
             "severity": "critical", "category": "accessibility"},
        ],
        "rationale": [
            "Industry: Fintech — Neobank",
            "Style: Monochrome Precise",
            "Palette: Linear Graphite",
        ],
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_save_master_writes_file(tmp_path: Path) -> None:
    """save_master writes MASTER.md with frontmatter + body at the expected
    location and returns the absolute path."""
    project_root = tmp_path
    path = save_master(str(project_root), _make_recommendation(), _make_brief())

    written = Path(path)
    assert written.exists(), f"expected {written} to exist"
    assert written.name == "MASTER.md"
    assert written.parent.name == "design-system"
    assert written.parent.parent.name == ".ux"

    text = written.read_text(encoding="utf-8")
    # YAML frontmatter is present
    assert text.startswith("---\n")
    head, sep, body = text.partition("\n---\n")
    assert "project: test-loyalty" in head
    assert "last_updated:" in head
    assert "ux_skill_version:" in head
    # Body has expected sections
    assert "# Design system — MASTER" in body
    assert "## Brief" in body
    assert "## Recommendation" in body
    assert "### Style: Monochrome Precise" in body
    assert "### Palette: Linear Graphite" in body
    assert "## Rationale" in body
    assert "## Pages persisted" in body


def test_save_master_roundtrip(tmp_path: Path) -> None:
    """save_master → load_master returns a dict with the meta and body
    matching what we wrote."""
    project_root = tmp_path
    brief = _make_brief()
    rec = _make_recommendation()

    path = save_master(str(project_root), rec, brief)
    loaded = load_master(str(project_root))

    assert loaded is not None, "load_master should return data after save_master"
    assert isinstance(loaded, dict)
    assert loaded.get("path") == path

    meta = loaded.get("meta") or {}
    assert meta.get("project") == "test-loyalty"
    assert meta.get("ux_skill_version"), "ux_skill_version must be in frontmatter"
    assert meta.get("last_updated"), "last_updated must be in frontmatter"

    body = loaded.get("body") or ""
    assert "# Design system — MASTER" in body
    assert "Monochrome Precise" in body
    assert "Linear Graphite" in body

    # No pages yet
    assert loaded.get("pages") == []


def test_save_page_creates_pages_directory(tmp_path: Path) -> None:
    """save_page writes to .ux/design-system/pages/<slug>.md and creates
    the pages directory if missing."""
    project_root = tmp_path
    pages_dir = project_root / ".ux" / "design-system" / "pages"
    assert not pages_dir.exists(), "pages dir must not exist before save_page"

    output = {
        "files_written": ["src/pages/landing.tsx", "src/styles/tokens.css"],
        "summary": {"style": "monochrome-precise", "guardrails": 35},
        "lint": [
            {"severity": "high", "rule": "no-purple-blue-gradient",
             "file": "src/pages/landing.tsx"},
        ],
        "decisions": ["Hero uses Cormorant Garamond at clamp(64px, 8vw, 96px)."],
    }
    path = save_page(str(project_root), "landing", _make_brief(), output)

    assert pages_dir.exists() and pages_dir.is_dir()
    written = Path(path)
    assert written.exists()
    assert written.parent == pages_dir
    assert written.suffix == ".md"
    assert written.stem == "landing"

    text = written.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "page: landing" in text
    assert "# Page — landing" in text
    assert "src/pages/landing.tsx" in text
    assert "no-purple-blue-gradient" in text
    assert "Cormorant Garamond" in text


def test_list_pages_returns_names(tmp_path: Path) -> None:
    """list_pages returns sorted stems of every .md under pages/."""
    project_root = tmp_path
    # Empty: returns []
    assert list_pages(str(project_root)) == []

    save_page(str(project_root), "landing", _make_brief(), {})
    save_page(str(project_root), "Pricing Page", _make_brief(), {})
    save_page(str(project_root), "dashboard.md", _make_brief(), {})

    names = list_pages(str(project_root))
    assert isinstance(names, list)
    # Slugged names — Pricing Page → pricing-page, dashboard.md → dashboard
    assert sorted(names) == names, "results must be sorted"
    assert "landing" in names
    assert "pricing-page" in names
    assert "dashboard" in names
    assert len(names) == 3


def test_save_master_idempotent(tmp_path: Path) -> None:
    """Saving the same content twice yields byte-identical files (the
    timestamp is preserved when the substantive body is unchanged)."""
    project_root = tmp_path
    brief = _make_brief()
    rec = _make_recommendation()

    path_1 = save_master(str(project_root), rec, brief)
    bytes_1 = Path(path_1).read_bytes()

    # Slight delay would not matter; the implementation reuses the timestamp.
    path_2 = save_master(str(project_root), rec, brief)
    bytes_2 = Path(path_2).read_bytes()

    assert path_1 == path_2
    assert bytes_1 == bytes_2, "same input must produce byte-identical output"

    # And the master correctly reflects the persisted pages on re-save: if we
    # add a page and re-save, the bytes should change.
    save_page(str(project_root), "landing", brief, {})
    path_3 = save_master(str(project_root), rec, brief)
    bytes_3 = Path(path_3).read_bytes()
    assert bytes_3 != bytes_1, "adding a page should invalidate the body"

    # But re-saving once more with the same state must be idempotent again.
    bytes_3_again = Path(save_master(str(project_root), rec, brief)).read_bytes()
    assert bytes_3 == bytes_3_again, "re-save after change must still be byte-stable"
