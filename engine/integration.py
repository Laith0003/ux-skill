"""Cross-reference wiring — Phase 1B integration.

After data agents fill the 12 manifests, this script walks them and fills
the `compatible_*` arrays based on tag overlap heuristics. Idempotent —
safe to re-run as data grows.

Heuristics
----------
- `style.compatible_palettes` = palettes whose `tone` overlaps with
  style.category / tokens.color / philosophy keywords.
- `style.compatible_type_pairs` = type-pairs whose `character` overlaps with
  style.category / philosophy keywords.
- `palette.compatible_styles` = inverse of the above.
- `component.compatible_styles` = styles whose category contains the
  component's category (loose match).
- `industry.recommended_styles` = styles whose `compatible_industries`
  contains the industry id (preserves agent intent).

Invocation
----------
    python -m engine.integration
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set

from engine.data_loader import DATA_DIR


def _normalize(text: str) -> Set[str]:
    """Lowercase + tokenise into words."""
    return set(re.findall(r"[a-z]+", text.lower()))


def _all_tags(entry: Dict[str, Any], fields: List[str]) -> Set[str]:
    """Collect tag-like tokens from a set of fields on an entry."""
    out: Set[str] = set()
    for field in fields:
        value = entry.get(field)
        if isinstance(value, str):
            out |= _normalize(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    out |= _normalize(item)
        elif isinstance(value, dict):
            for v in value.values():
                if isinstance(v, str):
                    out |= _normalize(v)
    return out


def _load(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def wire_styles_to_palettes_and_types() -> Dict[str, int]:
    styles_path = DATA_DIR / "styles.json"
    palettes_path = DATA_DIR / "palettes.json"
    types_path = DATA_DIR / "type-pairs.json"

    if not styles_path.exists() or not palettes_path.exists() or not types_path.exists():
        return {"wired_palettes": 0, "wired_types": 0}

    styles = _load(styles_path)
    palettes = _load(palettes_path)
    types = _load(types_path)

    wired_palettes = 0
    wired_types = 0

    for style in styles.get("entries", []):
        style_tags = _all_tags(style, ["category", "philosophy", "when_to_use", "tokens"])

        if not style.get("compatible_palettes"):
            matched = []
            for palette in palettes.get("entries", []):
                ptags = _all_tags(palette, ["name", "tone"])
                if style_tags & ptags:
                    matched.append(palette["id"])
                    if len(matched) >= 5:
                        break
            if matched:
                style["compatible_palettes"] = matched
                wired_palettes += 1

        if not style.get("compatible_type_pairs"):
            matched = []
            for tp in types.get("entries", []):
                ttags = _all_tags(tp, ["name", "character"])
                if style_tags & ttags:
                    matched.append(tp["id"])
                    if len(matched) >= 5:
                        break
            if matched:
                style["compatible_type_pairs"] = matched
                wired_types += 1

    _save(styles_path, styles)
    return {"wired_palettes": wired_palettes, "wired_types": wired_types}


def wire_palettes_to_styles() -> Dict[str, int]:
    styles_path = DATA_DIR / "styles.json"
    palettes_path = DATA_DIR / "palettes.json"

    if not styles_path.exists() or not palettes_path.exists():
        return {"wired": 0}

    styles = _load(styles_path)
    palettes = _load(palettes_path)

    wired = 0
    for palette in palettes.get("entries", []):
        if palette.get("compatible_styles"):
            continue
        ptags = _all_tags(palette, ["name", "tone"])
        matched = []
        for style in styles.get("entries", []):
            stags = _all_tags(style, ["category", "philosophy"])
            if ptags & stags:
                matched.append(style["id"])
                if len(matched) >= 5:
                    break
        if matched:
            palette["compatible_styles"] = matched
            wired += 1

    _save(palettes_path, palettes)
    return {"wired": wired}


def wire_components_to_styles() -> Dict[str, int]:
    styles_path = DATA_DIR / "styles.json"
    components_path = DATA_DIR / "components.json"

    if not styles_path.exists() or not components_path.exists():
        return {"wired": 0}

    styles = _load(styles_path)
    components = _load(components_path)

    wired = 0
    style_index = [(s["id"], _all_tags(s, ["category", "philosophy", "when_to_use"]))
                   for s in styles.get("entries", [])]

    for comp in components.get("entries", []):
        if comp.get("compatible_styles"):
            continue
        ctags = _all_tags(comp, ["category", "purpose"])
        # Components are broadly compatible — pick top-tag-overlap styles up to 10
        scored = [(sid, len(ctags & stags)) for sid, stags in style_index]
        scored.sort(key=lambda x: x[1], reverse=True)
        matched = [sid for sid, score in scored if score > 0][:10]
        if not matched:
            # Fall back to "general-purpose" styles (minimalist, editorial)
            matched = [sid for sid, _ in style_index
                       if "minimalist" in sid or "editorial" in sid][:5]
        if matched:
            comp["compatible_styles"] = matched
            wired += 1

    _save(components_path, components)
    return {"wired": wired}


def main() -> Dict[str, Any]:
    """Run all wiring passes. Returns a summary dict."""
    summary: Dict[str, Any] = {}
    summary["styles"] = wire_styles_to_palettes_and_types()
    summary["palettes"] = wire_palettes_to_styles()
    summary["components"] = wire_components_to_styles()
    return summary


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
