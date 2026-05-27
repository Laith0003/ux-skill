"""Loader for the v2 data manifests.

The engine reads JSON manifests from ``data/`` and caches them in-memory.
Each manifest has a top-level ``_meta`` block and an ``entries`` list.

Public surface
--------------
``load(manifest)``           -- load a single manifest by short name
``load_all()``               -- preload every manifest (used by the CLI)
``DATA_DIR``                 -- absolute path to the data directory
``MANIFESTS``                -- the canonical short-name list
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = (Path(__file__).resolve().parent.parent / "data").resolve()

MANIFESTS: List[str] = [
    "styles",
    "palettes",
    "type-pairs",
    "components",
    "industries",
    "chart-types",
    "tech-stacks",
    "ux-guidelines",
    "motion-presets",
    "anti-patterns",
]


@lru_cache(maxsize=None)
def load(manifest: str) -> Dict[str, Any]:
    """Load a single manifest by short name (e.g. ``styles``)."""
    path = DATA_DIR / f"{manifest}.json"
    if not path.exists():
        return {"_meta": {"entries": 0, "missing": True}, "entries": []}
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    # Tolerate either a list or a {_meta, entries} shape
    if isinstance(payload, list):
        return {"_meta": {"entries": len(payload)}, "entries": payload}
    return payload


def load_all() -> Dict[str, Dict[str, Any]]:
    """Load every known manifest. Returns ``{short_name: payload}``."""
    return {m: load(m) for m in MANIFESTS}


def load_brands() -> List[Dict[str, Any]]:
    """Load all brand specs from ``data/brands/*.json``."""
    brand_dir = DATA_DIR / "brands"
    if not brand_dir.exists():
        return []
    out: List[Dict[str, Any]] = []
    for path in sorted(brand_dir.glob("*.json")):
        if path.name == "_index.json":
            continue
        with path.open("r", encoding="utf-8") as f:
            out.append(json.load(f))
    return out


def stats() -> Dict[str, int]:
    """Counts per manifest. Used by ``ux stats`` and CI smoke tests."""
    result: Dict[str, int] = {}
    for m in MANIFESTS:
        payload = load(m)
        result[m] = len(payload.get("entries", []))
    result["brands"] = len(load_brands())
    return result
