"""MASTER.md persistence — write, read, list.

This module captures the current recommended design system as a single
``<project_root>/.ux/design-system/MASTER.md`` file with YAML frontmatter
and human-readable Markdown body. Individual generated pages land under
``<project_root>/.ux/design-system/pages/<page_name>.md``.

Design decisions
----------------
- Frontmatter is strictly flat (three scalar keys). We hand-roll the
  ``key: value`` parser/writer rather than pulling in PyYAML.
- ``last_updated`` is the only timestamp; we re-use the previous value when
  the substantive body is byte-identical so ``save_master`` is idempotent
  for the standing-rule of "same input → same output bytes."
- ``project`` defaults to ``brief["project"]`` if present, otherwise the
  basename of ``project_root``.
- ``## Pages persisted`` is snapshot from ``list_pages()`` at write time so
  the document stays in sync without manual maintenance.

Public surface
--------------
``save_master(project_root, recommendation, brief) -> str``
``save_page(project_root, page_name, brief, output) -> str``
``load_master(project_root) -> dict | None``
``list_pages(project_root) -> list[str]``
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine import __version__

# Marker that frontmatter is delimited by --- lines
_FM_DELIM = "---"
_FM_LINE_RE = re.compile(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$")


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _design_system_dir(project_root: str) -> Path:
    return (Path(project_root) / ".ux" / "design-system").resolve()


def _master_path(project_root: str) -> Path:
    return _design_system_dir(project_root) / "MASTER.md"


def _pages_dir(project_root: str) -> Path:
    return _design_system_dir(project_root) / "pages"


def _slugify(name: str) -> str:
    """Normalise a page name into a safe filename stem (no extension)."""
    stem = name.strip().lower()
    stem = re.sub(r"\.md$", "", stem)
    stem = re.sub(r"[^a-z0-9._-]+", "-", stem)
    stem = re.sub(r"-+", "-", stem).strip("-")
    return stem or "untitled"


# ---------------------------------------------------------------------------
# Value formatting helpers (defensive — handle both list and str)
# ---------------------------------------------------------------------------


def _format_value(value: Any) -> str:
    """Format a brief value into a human-readable Markdown string."""
    if value is None:
        return "—"
    if isinstance(value, list):
        cleaned = [str(v).strip() for v in value if str(v).strip()]
        return ", ".join(cleaned) if cleaned else "—"
    if isinstance(value, dict):
        # Render small dicts as comma-separated key=value pairs.
        return ", ".join(f"{k}={v}" for k, v in value.items()) or "—"
    text = str(value).strip()
    return text or "—"


def _get_brief(brief: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Brief lookup with None coalescing — `.get(key)` returning None still
    yields ``default``."""
    if not isinstance(brief, dict):
        return default
    value = brief.get(key)
    return default if value in (None, "", []) else value


# ---------------------------------------------------------------------------
# Frontmatter (flat YAML) — write + parse
# ---------------------------------------------------------------------------


def _yaml_escape(value: str) -> str:
    """Quote a frontmatter value if it could be ambiguous on read.

    We keep it simple: quote when the value contains ``:`` or starts/ends
    with whitespace or a quote character. Always wrap in double quotes and
    escape embedded double quotes with a backslash.
    """
    text = str(value)
    needs_quote = (
        ":" in text
        or text != text.strip()
        or text.startswith(('"', "'"))
        or text.endswith(('"', "'"))
    )
    if needs_quote:
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def _yaml_unescape(value: str) -> str:
    """Reverse of ``_yaml_escape`` for a single line value."""
    text = value.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ('"', "'"):
        inner = text[1:-1]
        return inner.replace('\\"', '"').replace("\\\\", "\\")
    return text


def _write_frontmatter(meta: Dict[str, str]) -> str:
    """Render the YAML frontmatter block (including delimiters)."""
    lines = [_FM_DELIM]
    for key, value in meta.items():
        lines.append(f"{key}: {_yaml_escape(value)}")
    lines.append(_FM_DELIM)
    return "\n".join(lines) + "\n"


def _parse_frontmatter(text: str) -> Optional[Dict[str, str]]:
    """Parse a leading ``---``-delimited block. Returns None if absent."""
    if not text.startswith(_FM_DELIM):
        return None
    # Find the closing delimiter on its own line.
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FM_DELIM:
        return None
    meta: Dict[str, str] = {}
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == _FM_DELIM:
            return meta
        match = _FM_LINE_RE.match(line)
        if match:
            key, raw = match.group(1), match.group(2)
            meta[key] = _yaml_unescape(raw)
    # No closing delimiter — treat as missing frontmatter.
    return None


def _strip_frontmatter(text: str) -> str:
    """Return the body (everything after the closing ``---``)."""
    if not text.startswith(_FM_DELIM):
        return text
    lines = text.splitlines(keepends=True)
    out: List[str] = []
    started = False
    closed = False
    for idx, line in enumerate(lines):
        if line.rstrip("\n").strip() == _FM_DELIM:
            if not started:
                started = True
                continue
            if not closed:
                closed = True
                continue
        if closed:
            out.append(line)
    if not closed:
        return text
    # Drop a single leading newline so the body section starts cleanly.
    body = "".join(out)
    return body.lstrip("\n")


# ---------------------------------------------------------------------------
# Body rendering
# ---------------------------------------------------------------------------


def _render_brief_section(brief: Dict[str, Any]) -> str:
    lines = ["## Brief", ""]

    fields = [
        ("project_type", "Project type"),
        ("audience", "Audience"),
        ("primary_goal", "Primary goal"),
        ("tone", "Tone"),
        ("must_have", "Must have"),
        ("forbidden", "Forbidden"),
        ("reference_brands", "Reference brands"),
        ("stack", "Stack"),
        ("region", "Region"),
        ("success_metric", "Success metric"),
    ]
    for key, label in fields:
        lines.append(f"- **{label}:** {_format_value(_get_brief(brief, key))}")
    lines.append("")
    return "\n".join(lines)


def _render_style(style: Optional[Dict[str, Any]]) -> str:
    if not isinstance(style, dict) or not style:
        return "### Style\n\n- (none picked)\n"
    name = style.get("name") or style.get("id") or "—"
    lines = [f"### Style: {name}", ""]
    if style.get("id"):
        lines.append(f"- **id:** {style['id']}")
    philosophy = style.get("philosophy") or style.get("description")
    if philosophy:
        lines.append(f"- **philosophy:** {philosophy}")
    if style.get("category"):
        lines.append(f"- **category:** {style['category']}")
    when = style.get("when_to_use")
    if when:
        lines.append(f"- **when to use:** {_format_value(when)}")
    exemplars = style.get("exemplars") or style.get("compatible_brands")
    if exemplars:
        lines.append(f"- **exemplars:** {_format_value(exemplars)}")
    tokens = style.get("tokens")
    if isinstance(tokens, dict) and tokens:
        token_keys = ", ".join(sorted(tokens.keys()))
        lines.append(f"- **tokens:** {token_keys}")
    lines.append("")
    return "\n".join(lines)


def _render_palette(palette: Optional[Dict[str, Any]]) -> str:
    if not isinstance(palette, dict) or not palette:
        return "### Palette\n\n- (none picked)\n"
    name = palette.get("name") or palette.get("id") or "—"
    lines = [f"### Palette: {name}", ""]
    if palette.get("id"):
        lines.append(f"- **id:** {palette['id']}")
    if palette.get("tone"):
        lines.append(f"- **tone:** {_format_value(palette['tone'])}")
    colors = palette.get("colors")
    if isinstance(colors, dict) and colors:
        for key in sorted(colors.keys()):
            value = colors[key]
            if isinstance(value, str):
                lines.append(f"- **{key}:** `{value}`")
    contrast = palette.get("contrast_scores") or palette.get("contrast")
    if isinstance(contrast, dict) and contrast:
        scores = ", ".join(f"{k}={v}" for k, v in sorted(contrast.items()))
        lines.append(f"- **contrast:** {scores}")
    lines.append("")
    return "\n".join(lines)


def _render_type_pair(type_pair: Optional[Dict[str, Any]]) -> str:
    if not isinstance(type_pair, dict) or not type_pair:
        return "### Type pair\n\n- (none picked)\n"

    def _slot(slot: Optional[Dict[str, Any]]) -> str:
        if not isinstance(slot, dict):
            return "—"
        family = slot.get("family") or slot.get("name") or "—"
        weights = slot.get("weights") or slot.get("weight")
        if weights:
            return f"{family} ({_format_value(weights)})"
        return family

    display = _slot(type_pair.get("display"))
    body = _slot(type_pair.get("body"))
    mono = _slot(type_pair.get("mono"))
    title = f"{display} x {body} x {mono}"
    lines = [f"### Type pair: {title}", ""]
    if type_pair.get("id"):
        lines.append(f"- **id:** {type_pair['id']}")
    lines.append(f"- **display:** {display}")
    lines.append(f"- **body:** {body}")
    lines.append(f"- **mono:** {mono}")
    if type_pair.get("character"):
        lines.append(f"- **character:** {_format_value(type_pair['character'])}")
    lines.append("")
    return "\n".join(lines)


def _render_motion(motion: List[Dict[str, Any]]) -> str:
    motion = motion or []
    lines = [f"### Motion presets ({len(motion)})", ""]
    if not motion:
        lines.append("- (none picked)")
        lines.append("")
        return "\n".join(lines)
    for m in motion:
        name = m.get("name") or m.get("id") or "—"
        bits = []
        tokens = m.get("tokens")
        if isinstance(tokens, dict):
            easing = tokens.get("easing") or tokens.get("ease")
            duration = tokens.get("duration") or tokens.get("duration_ms")
            if easing:
                bits.append(str(easing))
            if duration:
                bits.append(f"{duration}")
        detail = f" ({', '.join(bits)})" if bits else ""
        lines.append(f"- {name}{detail}")
    lines.append("")
    return "\n".join(lines)


def _render_components(components: List[Dict[str, Any]]) -> str:
    components = components or []
    lines = [f"### Components ({len(components)})", ""]
    if not components:
        lines.append("- (none picked)")
        lines.append("")
        return "\n".join(lines)
    for c in components:
        name = c.get("id") or c.get("name") or "—"
        category = c.get("category")
        suffix = f" — {category}" if category else ""
        lines.append(f"- {name}{suffix}")
    lines.append("")
    return "\n".join(lines)


def _render_brand_exemplars(brands: List[Dict[str, Any]]) -> str:
    brands = brands or []
    lines = [f"### Brand exemplars ({len(brands)})", ""]
    if not brands:
        lines.append("- (none picked)")
        lines.append("")
        return "\n".join(lines)
    for b in brands:
        bid = b.get("id") or b.get("name") or "—"
        category = b.get("category") or b.get("industry")
        suffix = f" — {category}" if category else ""
        lines.append(f"- {bid}{suffix}")
    lines.append("")
    return "\n".join(lines)


def _render_guardrails(guardrails: List[Dict[str, Any]]) -> str:
    guardrails = guardrails or []
    by_cat: Dict[str, int] = {}
    by_sev: Dict[str, int] = {}
    for g in guardrails:
        cat = g.get("category") or "uncategorised"
        sev = g.get("severity") or "unspecified"
        by_cat[cat] = by_cat.get(cat, 0) + 1
        by_sev[sev] = by_sev.get(sev, 0) + 1
    lines = [f"### Anti-pattern guardrails ({len(guardrails)} active)", ""]
    if by_sev:
        sev_summary = ", ".join(f"{k}={v}" for k, v in sorted(by_sev.items()))
        lines.append(f"- **by severity:** {sev_summary}")
    if by_cat:
        cat_summary = ", ".join(f"{k}={v}" for k, v in sorted(by_cat.items()))
        lines.append(f"- **by category:** {cat_summary}")
    if not by_sev and not by_cat:
        lines.append("- (none active)")
    lines.append("")
    return "\n".join(lines)


def _render_rationale(rationale: List[str]) -> str:
    lines = ["## Rationale", ""]
    if not rationale:
        lines.append("- (none provided)")
    else:
        for line in rationale:
            lines.append(f"- {line}")
    lines.append("")
    return "\n".join(lines)


def _render_pages_section(pages: List[str]) -> str:
    lines = ["## Pages persisted", ""]
    if not pages:
        lines.append("- (auto-populated as pages are added)")
    else:
        for name in pages:
            lines.append(f"- {name}")
    lines.append("")
    return "\n".join(lines)


def _render_body(
    recommendation: Dict[str, Any],
    brief: Dict[str, Any],
    pages: List[str],
) -> str:
    rec = recommendation or {}
    sections = [
        "# Design system — MASTER",
        "",
        _render_brief_section(brief or {}),
        "## Recommendation",
        "",
        _render_style(rec.get("style")),
        _render_palette(rec.get("palette")),
        _render_type_pair(rec.get("type_pair")),
        _render_motion(rec.get("motion") or []),
        _render_components(rec.get("components") or []),
        _render_brand_exemplars(rec.get("brand_exemplars") or []),
        _render_guardrails(rec.get("guardrails") or []),
        _render_rationale(rec.get("rationale") or []),
        _render_pages_section(pages),
    ]
    return "\n".join(sections).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def _utc_now_iso() -> str:
    """ISO 8601 UTC timestamp with second precision and trailing ``Z``."""
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_project_name(project_root: str, brief: Dict[str, Any]) -> str:
    name = _get_brief(brief, "project")
    if name:
        return str(name)
    resolved = Path(project_root).resolve()
    return resolved.name or "untitled"


def save_master(project_root: str, recommendation: Dict[str, Any], brief: Dict[str, Any]) -> str:
    """Write ``<project_root>/.ux/design-system/MASTER.md``.

    Idempotent: re-using the existing ``last_updated`` timestamp when the
    substantive body has not changed. Returns the absolute path written.
    """
    target = _master_path(project_root)
    target.parent.mkdir(parents=True, exist_ok=True)

    pages = list_pages(project_root)
    project_name = _resolve_project_name(project_root, brief)
    body = _render_body(recommendation or {}, brief or {}, pages)

    # Idempotency: if body matches, reuse the old timestamp so the bytes are
    # bit-for-bit identical. Anything else is a real change.
    last_updated = _utc_now_iso()
    if target.exists():
        previous = target.read_text(encoding="utf-8")
        previous_meta = _parse_frontmatter(previous) or {}
        previous_body = _strip_frontmatter(previous)
        same_project = previous_meta.get("project") == project_name
        same_version = previous_meta.get("ux_skill_version") == __version__
        if previous_body == body and same_project and same_version:
            last_updated = previous_meta.get("last_updated", last_updated)

    meta = {
        "project": project_name,
        "last_updated": last_updated,
        "ux_skill_version": __version__,
    }
    payload = _write_frontmatter(meta) + "\n" + body
    target.write_text(payload, encoding="utf-8")
    return str(target)


def load_master(project_root: str) -> Optional[Dict[str, Any]]:
    """Read MASTER.md back into a structured dict, or None if absent.

    The returned dict has top-level keys ``meta`` (frontmatter values) and
    ``body`` (the raw Markdown body). For programmatic access, additional
    parsed fields are best derived from the recommendation JSON that fed
    ``save_master`` — this loader stays intentionally simple.
    """
    target = _master_path(project_root)
    if not target.exists():
        return None
    text = target.read_text(encoding="utf-8")
    meta = _parse_frontmatter(text) or {}
    body = _strip_frontmatter(text)
    return {
        "meta": meta,
        "body": body,
        "path": str(target),
        "pages": list_pages(project_root),
    }


def save_page(
    project_root: str,
    page_name: str,
    brief: Dict[str, Any],
    output: Dict[str, Any],
) -> str:
    """Write a per-page persistence file under ``pages/``.

    ``output`` is a free-form dict describing the generated artifact —
    typically the bundle from ``engine.generator.generate`` plus any lint
    findings and design decisions. Returns the absolute path written.
    """
    pages_dir = _pages_dir(project_root)
    pages_dir.mkdir(parents=True, exist_ok=True)

    stem = _slugify(page_name)
    target = pages_dir / f"{stem}.md"

    body_sections: List[str] = []
    body_sections.append(f"# Page — {page_name.strip() or stem}")
    body_sections.append("")
    body_sections.append(_render_brief_section(brief or {}))

    body_sections.append("## Output")
    body_sections.append("")
    output = output or {}
    files = output.get("files_written") or output.get("files") or []
    if files:
        body_sections.append("### Files")
        body_sections.append("")
        for f in files:
            body_sections.append(f"- `{f}`")
        body_sections.append("")
    summary = output.get("summary") or {}
    if isinstance(summary, dict) and summary:
        body_sections.append("### Summary")
        body_sections.append("")
        for key in sorted(summary.keys()):
            body_sections.append(f"- **{key}:** {_format_value(summary[key])}")
        body_sections.append("")

    findings = output.get("lint") or output.get("findings") or []
    if isinstance(findings, list) and findings:
        body_sections.append(f"### Lint findings ({len(findings)})")
        body_sections.append("")
        for finding in findings:
            if isinstance(finding, dict):
                sev = finding.get("severity") or "—"
                name = finding.get("rule") or finding.get("name") or finding.get("id") or "—"
                where = finding.get("file") or finding.get("path") or ""
                location = f" — {where}" if where else ""
                body_sections.append(f"- [{sev}] {name}{location}")
            else:
                body_sections.append(f"- {finding}")
        body_sections.append("")

    decisions = output.get("decisions") or []
    if isinstance(decisions, list) and decisions:
        body_sections.append("### Decisions")
        body_sections.append("")
        for d in decisions:
            body_sections.append(f"- {d}")
        body_sections.append("")

    new_body = "\n".join(body_sections).rstrip() + "\n"

    # Idempotency for pages: same body + same project + same version → reuse
    # the previous timestamp so re-saves are byte-identical.
    last_updated = _utc_now_iso()
    project_name = _resolve_project_name(project_root, brief)
    if target.exists():
        previous = target.read_text(encoding="utf-8")
        previous_meta = _parse_frontmatter(previous) or {}
        previous_body = _strip_frontmatter(previous)
        same_project = previous_meta.get("project") == project_name
        same_version = previous_meta.get("ux_skill_version") == __version__
        if previous_body == new_body and same_project and same_version:
            last_updated = previous_meta.get("last_updated", last_updated)

    meta = {
        "project": project_name,
        "page": stem,
        "last_updated": last_updated,
        "ux_skill_version": __version__,
    }
    payload = _write_frontmatter(meta) + "\n" + new_body
    target.write_text(payload, encoding="utf-8")
    return str(target)


def list_pages(project_root: str) -> List[str]:
    """Return the slugged names of pages persisted under ``pages/``."""
    pages_dir = _pages_dir(project_root)
    if not pages_dir.exists():
        return []
    out: List[str] = []
    for path in sorted(pages_dir.glob("*.md")):
        out.append(path.stem)
    return out
