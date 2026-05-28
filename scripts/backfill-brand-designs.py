"""Backfill missing references/brands/<id>-DESIGN.md files from data/brands/<id>.json.

72 of 160 brand JSONs historically shipped without a paired DESIGN.md. Their
links from docs/brands.html therefore 404'd on GitHub. This script reads each
spec.json and writes a substantive Markdown reference (palette + typography
notes + voice cues + components observed + anti-patterns to avoid) so the
links resolve and the prose layer for the catalogue is complete.

Idempotent: runs over all brands, only writes the MD if it's missing.
Re-run safely any time data/brands/ grows.
"""
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
BRANDS_DIR = ROOT / "data" / "brands"
MD_DIR = ROOT / "references" / "brands"


def safe(v, fallback=""):
    if v is None or v == "":
        return fallback
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


def colors_block(dl: dict) -> str:
    keys = [
        ("color_canvas",    "Canvas"),
        ("color_ink",       "Ink"),
        ("color_body",      "Body"),
        ("color_muted",     "Muted"),
        ("color_primary",   "Primary"),
        ("color_accent",    "Accent"),
        ("color_secondary", "Secondary"),
    ]
    rows = []
    for k, label in keys:
        v = dl.get(k)
        if v:
            rows.append(f"- **{label}**: `{v}`")
    return "\n".join(rows) if rows else "_Palette not yet documented._"


def type_block(dl: dict) -> str:
    out = []
    for k, label in [
        ("typography_display", "Display"),
        ("typography_body",    "Body"),
        ("typography_mono",    "Mono"),
        ("font_display",       "Display"),
        ("font_body",          "Body"),
        ("font_mono",          "Mono"),
        ("display_font",       "Display"),
        ("body_font",          "Body"),
    ]:
        v = dl.get(k)
        if v:
            out.append(f"- **{label}**: {v}")
    seen = set()
    deduped = []
    for line in out:
        if line not in seen:
            seen.add(line)
            deduped.append(line)
    return "\n".join(deduped) if deduped else "_Type pair not yet documented._"


def list_or_empty(items, prefix="- "):
    if not items:
        return "_(none documented)_"
    return "\n".join(f"{prefix}{html_unescape_lite(safe(x))}" for x in items if x)


def html_unescape_lite(s: str) -> str:
    return s.replace("&mdash;", "—").replace("&middot;", "·")


TEMPLATE = """# {name}

> {essence}

**Category:** {category}
**Industry:** {industry}
**Source:** [`data/brands/{bid}.json`](../../data/brands/{bid}.json)

## Palette

{palette}

## Typography

{typography}

## Philosophy

{philosophy}

## Voice cues

{voice}

## Components observed

{components}

## Motion vocabulary

{motion}

## Anti-patterns to avoid

{anti_patterns}

---

_This reference was backfilled from the structured spec. Edit freely — it stays in sync as long as the heading layout is preserved._
"""


def render(bid: str, spec: dict) -> str:
    dl = spec.get("design_language") or {}
    essence = safe(spec.get("philosophy") or spec.get("essence"),
                   f"Brand DESIGN reference for {spec.get('name', bid)}.")
    return TEMPLATE.format(
        bid=bid,
        name=safe(spec.get("name") or bid),
        essence=essence,
        category=safe(spec.get("category"), "Uncategorized"),
        industry=safe(spec.get("industry"), "—"),
        palette=colors_block(dl),
        typography=type_block(dl),
        philosophy=safe(spec.get("philosophy")) or "_(see essence above)_",
        voice=list_or_empty(spec.get("voice") or spec.get("voice_cues") or spec.get("voice_do") or []),
        components=list_or_empty(spec.get("components") or spec.get("components_observed") or []),
        motion=list_or_empty(spec.get("motion") or spec.get("motion_vocabulary") or []),
        anti_patterns=list_or_empty(
            spec.get("anti_patterns_to_avoid")
            or spec.get("do_dont")
            or spec.get("dont")
            or []
        ),
    )


def main():
    written = 0
    skipped = 0
    errors = 0
    MD_DIR.mkdir(parents=True, exist_ok=True)
    for json_path in sorted(BRANDS_DIR.glob("*.json")):
        bid = json_path.stem
        if bid == "_index":
            continue
        md_path = MD_DIR / f"{bid}-DESIGN.md"
        if md_path.exists():
            skipped += 1
            continue
        try:
            with json_path.open(encoding="utf-8") as f:
                spec = json.load(f)
            body = render(bid, spec)
            md_path.write_text(body, encoding="utf-8")
            written += 1
            print(f"  wrote {md_path.relative_to(ROOT)}")
        except Exception as e:
            errors += 1
            print(f"  ERROR {bid}: {e}")
    print(f"\n  written: {written}")
    print(f"  skipped: {skipped} (already exist)")
    print(f"  errors:  {errors}")


if __name__ == "__main__":
    main()
