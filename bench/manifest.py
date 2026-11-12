"""Read, check and write bench/manifest.json."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

from bench import MANIFEST, PAGES, PRIVATE

ORIGINS = ("ai-generated", "ai-found", "designer")
SPLITS = ("dev", "holdout")
REQUIRED = (
    "id", "origin", "licence", "attribution", "redistributable", "url", "capture_date",
    "sha256", "split",
)
# Share of pages held out, assigned by a hash of the id so it never moves.
HOLDOUT_SHARE = 0.3


class ManifestError(ValueError):
    """The manifest is malformed; the message names the page, the field and the fix."""


def split_for(page_id: str) -> str:
    """A split for a page added on its own: a hash of the id, so it never moves."""
    h = int(hashlib.sha256(page_id.encode()).hexdigest()[:8], 16)
    return "holdout" if (h % 1000) / 1000 < HOLDOUT_SHARE else "dev"


def families(pages: List[Dict[str, Any]]) -> Dict[str, str]:
    """Page id to family id. A family is pages that must sit on one side of
    the split: a left-to-right page and its right-to-left twin (same id but
    for an -rtl suffix), and pages that share a stored stylesheet, own or
    vendor. Holding out one of them while tuning on its twin would leak."""
    parent = {p["id"]: p["id"] for p in pages}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def join(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    by_css: Dict[str, str] = {}
    for p in pages:
        twin = p["id"][:-4] if p["id"].endswith("-rtl") else None
        if twin and twin in parent:
            join(p["id"], twin)
        files = p.get("files") or {}
        for css in [*files.get("own", []), *files.get("vendor", [])]:
            if css in by_css:
                join(p["id"], by_css[css])
            else:
                by_css[css] = p["id"]
    return {pid: find(pid) for pid in parent}


def assign_splits(data: Dict[str, Any], reset: bool = False) -> None:
    """Stratified, family-aware assignment. Within each origin, families are
    ranked by a hash of their id and held out whole while the holdout stays
    within HOLDOUT_SHARE of the origin's pages; a family too big to fit stays
    in dev. A page joining a family that already has a split takes it, and
    pages that have a split keep it unless ``reset`` is set, so the holdout
    does not move once set."""
    fam = families(data["pages"])
    if reset:
        for p in data["pages"]:
            p.pop("split", None)
    by_origin: Dict[str, List[Dict[str, Any]]] = {}
    for p in data["pages"]:
        by_origin.setdefault(p["origin"], []).append(p)
    for pages in by_origin.values():
        side: Dict[str, str] = {}
        for p in pages:
            if p.get("split") in SPLITS:
                side.setdefault(fam[p["id"]], p["split"])
        target = round(HOLDOUT_SHARE * len(pages))
        held = sum(1 for p in pages if side.get(fam[p["id"]]) == "holdout")
        members: Dict[str, List[Dict[str, Any]]] = {}
        for p in pages:
            members.setdefault(fam[p["id"]], []).append(p)
        for f in sorted(members, key=lambda f: hashlib.sha256(f.encode()).hexdigest()):
            if f in side:
                continue
            size = len(members[f])
            if held + size <= target:
                side[f] = "holdout"
                held += size
            else:
                side[f] = "dev"
        for p in pages:
            p["split"] = side[fam[p["id"]]]


def load(path: Path = MANIFEST) -> Dict[str, Any]:
    if not path.exists():
        return {"version": 1, "pages": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save(data: Dict[str, Any], path: Path = MANIFEST) -> None:
    assign_splits(data)
    data["pages"] = sorted(data["pages"], key=lambda p: p["id"])
    path.write_text(json.dumps(data, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")


def upsert(data: Dict[str, Any], entry: Dict[str, Any]) -> None:
    old = next((p for p in data["pages"] if p["id"] == entry["id"]), None)
    if old and old.get("split") in SPLITS:
        entry["split"] = old["split"]
    pages = [p for p in data["pages"] if p["id"] != entry["id"]]
    pages.append(entry)
    data["pages"] = pages


def page_dir(entry: Dict[str, Any]) -> Path:
    return (PAGES if entry["redistributable"] else PRIVATE) / entry["id"]


def problems(data: Dict[str, Any]) -> List[str]:
    """Every malformed entry, each naming the page, the field and the fix."""
    out: List[str] = []
    seen = set()
    for p in data.get("pages", []):
        pid = p.get("id", "<no id>")
        for k in REQUIRED:
            if k not in p:
                out.append(f"{pid}: field {k} is missing; add it to the manifest entry")
        if pid in seen:
            out.append(f"{pid}: id appears twice; give each page its own id")
        seen.add(pid)
        if p.get("origin") not in ORIGINS:
            out.append(f"{pid}: origin {p.get('origin')!r} is not one of {ORIGINS}")
        if p.get("split") not in SPLITS:
            out.append(f"{pid}: split {p.get('split')!r} is not one of {SPLITS}")
        if not isinstance(p.get("redistributable"), bool):
            out.append(f"{pid}: redistributable must be true or false")
        if p.get("redistributable") is False and (PAGES / pid).exists():
            out.append(f"{pid}: not redistributable but bench/pages/{pid} exists; move the "
                       "snapshot to bench/private/ and keep only url, date, hash and labels")
        if p.get("origin") == "ai-generated" and not p.get("generator", {}).get("brief"):
            out.append(f"{pid}: generator.brief is missing; name the brief the page was built from")
    return out
