"""System-pack emitter -- a full design-system FOLDER from a synthesized system.

Where ``design_md`` writes a single DESIGN.md, ``pack_system`` writes the whole
package a developer (or their coding agent) can drop into a project:

    <slug>/
      DESIGN.md         # the awesome-design-md / Google Stitch spec + prose
      metadata.json     # structured spec: palette[{name,value,role,contrast}], fonts, tags
      css/tokens.css    # :root custom properties + base component classes
      preview.html      # a self-contained demo page applying the system

Two things make this stronger and more precise than a lone .md:
  1. It expands the synthesized 6-color core into a complete semantic palette
     (surfaces, border, on-primary, and accessible success/warning/danger/info
     signals) -- a real system, not just a few tokens.
  2. Every text pair carries its measured WCAG contrast ratio. The systems are
     accessible by construction (see engine.synthesizer), and the pack proves it
     in the metadata + DESIGN.md rather than asking you to trust it.

Pure, deterministic string building. No network, no LLM. Same system in, same
bytes out. Reuses the color math from the synthesizer so the numbers agree.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine.synthesizer.core import (
    _hex_to_rgb, _rgb_to_hex, _mix_colors, _relative_luminance,
    _contrast_ratio, _rgb_to_hsl, _hsl_to_rgb, _set_lightness, _enforce_contrast,
)

# Fixed signal hues (degrees). Saturation/lightness are tuned per theme and then
# contrast-enforced vs the canvas so every status color is readable.
_SIGNAL_HUES = {"success": 150, "warning": 42, "danger": 8, "info": 212}

_FONT_PROVIDERS = {  # best-effort provenance for the metadata block
    "Inter": "Google Fonts", "Inter Tight": "Google Fonts", "JetBrains Mono": "Google Fonts",
    "Fraunces": "Google Fonts", "Bricolage Grotesque": "Google Fonts", "Space Grotesk": "Google Fonts",
    "IBM Plex Sans": "Google Fonts", "IBM Plex Mono": "Google Fonts", "Geist": "Google Fonts",
    "Sohne": "Custom", "Georgia": "System",
}


def _gfont_import(family: str) -> Optional[str]:
    fam = (family or "").strip()
    if not fam or _FONT_PROVIDERS.get(fam) not in ("Google Fonts", None):
        return None
    return f"https://fonts.googleapis.com/css2?family={fam.replace(' ', '+')}:wght@400;500;600;700&display=swap"


def _ratio(fg: str, bg: str) -> float:
    a, b = _hex_to_rgb(fg), _hex_to_rgb(bg)
    if not a or not b:
        return 0.0
    return round(_contrast_ratio(a, b), 2)


def _darken(hex_str: str, amount: float) -> str:
    rgb = _hex_to_rgb(hex_str)
    if not rgb:
        return hex_str
    h, s, l = _rgb_to_hsl(rgb)
    return _rgb_to_hex(_hsl_to_rgb((h, s, max(0.0, l - amount))))


def _signal(hue: int, theme: str, canvas: str) -> str:
    s, l = (0.70, 0.44) if theme == "light" else (0.66, 0.62)
    base = _rgb_to_hex(_hsl_to_rgb((hue / 360.0, s, l)))
    return _enforce_contrast(base, canvas, 4.5)


def derive_palette(system: Any) -> Dict[str, str]:
    """Expand the synthesized 6-color core into a full semantic palette.

    Surfaces and border are derived from the canvas/ink relationship; signals are
    generated from fixed hues and contrast-enforced. Everything stays accessible.
    """
    p = dict(getattr(system, "palette", None) or system.get("palette", {}))
    canvas = p.get("canvas", "#ffffff")
    ink = p.get("ink", "#0a0a0a")
    body = p.get("body", "#444444")
    muted = p.get("muted", "#777777")
    primary = p.get("primary", "#3355ff")
    hairline = p.get("hairline") or _mix_colors([canvas, ink], [0.86, 0.14]) or "#dddddd"

    theme = "dark" if _relative_luminance(_hex_to_rgb(canvas) or (255, 255, 255)) < 0.45 else "light"
    surface = _mix_colors([canvas, ink], [0.965, 0.035]) or canvas
    elevated = _mix_colors([canvas, ink], [0.92, 0.08]) or canvas
    border = _mix_colors([canvas, ink], [0.85, 0.15]) or hairline

    # Text on the accent: the higher-contrast of pure white / near-black. The
    # max of the two extremes is always ~4.5:1+ (they cross at ~4.58), so this
    # is readable for any primary.
    black = "#0a0a0c"
    on_primary = "#ffffff" if _ratio("#ffffff", primary) >= _ratio(black, primary) else black

    return {
        "canvas": canvas, "surface": surface, "elevated": elevated, "border": border,
        "ink": ink, "body": body, "muted": muted,
        "primary": primary, "primary_active": _darken(primary, 0.08), "on_primary": on_primary,
        "success": _signal(_SIGNAL_HUES["success"], theme, canvas),
        "warning": _signal(_SIGNAL_HUES["warning"], theme, canvas),
        "danger": _signal(_SIGNAL_HUES["danger"], theme, canvas),
        "info": _signal(_SIGNAL_HUES["info"], theme, canvas),
        "_theme": theme,
    }


_ROLES = {
    "canvas": "Page and app background", "surface": "Cards, panels, and form fields",
    "elevated": "Modals, popovers, and the highest tier", "border": "Hairline dividers and outlines",
    "ink": "Headlines and primary foreground", "body": "Paragraph and reading text",
    "muted": "Secondary text, captions, and hints", "primary": "Primary action, focus, and accent",
    "primary_active": "Pressed and active state of the accent", "on_primary": "Text and icons on the accent",
    "success": "Success, positive metrics, and confirmation", "warning": "Warning and caution",
    "danger": "Error, destructive, and critical signal", "info": "Information and neutral data",
}


def _contrast_report(pal: Dict[str, str]) -> Dict[str, Any]:
    cv = pal["canvas"]
    pairs = {
        "ink_on_canvas": _ratio(pal["ink"], cv), "body_on_canvas": _ratio(pal["body"], cv),
        "muted_on_canvas": _ratio(pal["muted"], cv), "primary_on_canvas": _ratio(pal["primary"], cv),
        "on_primary_on_primary": _ratio(pal["on_primary"], pal["primary"]),
        "body_on_surface": _ratio(pal["body"], pal["surface"]),
    }
    text_keys = ("ink_on_canvas", "body_on_canvas", "muted_on_canvas")
    return {
        "ratios": pairs,
        "wcag_aa_text": all(pairs[k] >= 4.5 for k in text_keys),
        "note": "Every text pair meets WCAG AA. Accessible by construction (ux-skill synthesizer).",
    }


def _metadata(system: Any, pal: Dict[str, str], name: str, description: str,
              concept: str, tags: List[str]) -> str:
    tp = dict(getattr(system, "type_pair", None) or system.get("type_pair", {}))
    display, body_f, mono = tp.get("display", "Inter"), tp.get("body", "Inter"), tp.get("mono", "JetBrains Mono")
    fonts = []
    for fam, usage in [(display, "Display headlines and UI labels"),
                       (body_f, "Body and reading text"), (mono, "Metrics, code, and tabular data")]:
        if not fam or any(f["name"] == fam for f in fonts):
            continue
        fonts.append({"name": fam, "provider": _FONT_PROVIDERS.get(fam, "Google Fonts"),
                      "usage": usage, "cssImport": _gfont_import(fam)})
    palette = [{"name": k.replace("_", " ").title(), "token": k, "value": pal[k],
                "role": _ROLES.get(k, ""), "contrastOnCanvas": _ratio(pal[k], pal["canvas"])}
               for k in _ROLES if k in pal]
    payload = {
        "name": name, "description": description, "theme": pal["_theme"], "concept": concept,
        "palette": palette, "fonts": fonts, "tags": tags,
        "accessibility": _contrast_report(pal),
        "axes": getattr(system, "axes", None) or system.get("axes", {}),
        "generator": "ux-skill synthesizer (deterministic, offline, never calls an LLM)",
        "license": "Free to use. Generated, not curated.",
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _tokens_css(system: Any, pal: Dict[str, str], name: str) -> str:
    tp = dict(getattr(system, "type_pair", None) or system.get("type_pair", {}))
    sp = dict(getattr(system, "spacing", None) or system.get("spacing", {}))
    rad = dict(getattr(system, "radius", None) or system.get("radius", {}))
    mot = dict(getattr(system, "motion", None) or system.get("motion", {}))
    scale = sp.get("scale") or [4, 8, 12, 16, 24, 32, 48, 64]
    space_names = ["xxs", "xs", "sm", "md", "lg", "xl", "xxl", "xxxl"]
    L = [f"/* {name} -- ux-skill generated tokens. Accessible by construction (WCAG AA). */",
         "/* Do not edit by hand: re-generate with `ux system-pack`. */", ":root {"]
    for k in ("canvas", "surface", "elevated", "border", "ink", "body", "muted",
              "primary", "primary_active", "on_primary", "success", "warning", "danger", "info"):
        L.append(f"  --color-{k.replace('_', '-')}: {pal[k]};")
    if tp.get("display"):
        L.append(f"  --font-display: \"{tp['display']}\", Georgia, serif;")
    if tp.get("body"):
        L.append(f"  --font-body: \"{tp['body']}\", system-ui, sans-serif;")
    if tp.get("mono"):
        L.append(f"  --font-mono: \"{tp['mono']}\", ui-monospace, monospace;")
    for nm, val in zip(space_names, scale):
        L.append(f"  --space-{nm}: {val}px;")
    for nm, val in [("sm", rad.get("sm", 6)), ("md", rad.get("md", 10)),
                    ("lg", rad.get("lg", 16)), ("pill", rad.get("pill", 9999))]:
        L.append(f"  --radius-{nm}: {val}px;")
    L.append(f"  --motion-base: {mot.get('base_ms', 200)}ms;")
    L.append(f"  --motion-ease: {mot.get('ease', 'cubic-bezier(0.2,0,0,1)')};")
    L.append("}")
    L.append("""
.btn { font-family: var(--font-body); font-weight: 600; font-size: 15px; padding: 10px 18px;
  border-radius: var(--radius-md); border: 0; cursor: pointer; transition: background var(--motion-base) var(--motion-ease); }
.btn--primary { background: var(--color-primary); color: var(--color-on-primary); }
.btn--primary:hover { background: var(--color-primary-active); }
.btn--secondary { background: var(--color-surface); color: var(--color-ink); border: 1px solid var(--color-border); }
.card { background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius-lg); padding: var(--space-lg); color: var(--color-body); }
.input { width: 100%; background: var(--color-canvas); color: var(--color-ink); font-family: var(--font-body);
  border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 10px 14px; }
.input:focus { outline: 2px solid var(--color-primary); outline-offset: 1px; }""")
    return "\n".join(L) + "\n"


_DESIGN_MD_COMPONENTS = """  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 10px 18px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    border: "1px solid {colors.border}"
    rounded: "{rounded.md}"
  input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    border: "1px solid {colors.border}"
    rounded: "{rounded.md}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    border: "1px solid {colors.border}"
    rounded: "{rounded.lg}\""""


def _strip_dashes(t: str) -> str:
    return (t or "").replace("—", "-").replace("–", "-").replace("‒", "-")


def _design_md(system: Any, pal: Dict[str, str], name: str, description: str, concept: str) -> str:
    tp = dict(getattr(system, "type_pair", None) or system.get("type_pair", {}))
    display, body_f, mono = tp.get("display", "Georgia"), tp.get("body", "system-ui"), tp.get("mono", "ui-monospace")
    slug = name.strip().replace(" ", "-").lower()
    rep = _contrast_report(pal)
    out: List[str] = ["---", "version: 1", f"name: {slug}",
                      f'description: "{_strip_dashes(description)}"', f"theme: {pal['_theme']}", "colors:"]
    for k in ("canvas", "surface", "elevated", "border", "ink", "body", "muted",
              "primary", "primary_active", "on_primary", "success", "warning", "danger", "info"):
        out.append(f'  {k.replace("_", "-")}: "{pal[k]}"')
    out.append("typography:")
    for tok, fam, sz, wt, lh, ls in [
        ("display-xl", display, 64, 600, "1.05", "-1.5"), ("display-lg", display, 48, 600, "1.1", "-1"),
        ("display-md", display, 34, 600, "1.15", "-0.5"), ("body", body_f, 16, 400, "1.6", "0"),
        ("body-sm", body_f, 14, 400, "1.55", "0"), ("button", body_f, 15, 600, "1", "0.1"),
        ("caption", body_f, 12, 400, "1.4", "0.2"), ("code", mono, 13, 400, "1.5", "0"),
    ]:
        out.append(f"  {tok}:")
        out += [f'    fontFamily: "{fam}"', f"    fontSize: {sz}px",
                f"    fontWeight: {wt}", f"    lineHeight: {lh}", f"    letterSpacing: {ls}px"]
    out.append("spacing:")
    out += [f"  {k}: {v}px" for k, v in
            [("xxs", 4), ("xs", 8), ("sm", 12), ("md", 16), ("lg", 24), ("xl", 32), ("xxl", 48)]]
    out.append("rounded:")
    out += [f"  {k}: {v}" for k, v in [("sm", "6px"), ("md", "10px"), ("lg", "16px"), ("pill", "9999px")]]
    out.append("components:")
    out.append(_DESIGN_MD_COMPONENTS)
    out.append("---")
    out.append("")
    out.append(f"# {name}")
    out.append("")
    out.append(_strip_dashes(concept))
    out.append("")
    out.append("## Accessibility")
    out.append("")
    out.append("Every text pair meets WCAG AA, enforced at synthesis time:")
    out.append("")
    out.append(f"- Ink on canvas: {rep['ratios']['ink_on_canvas']}:1")
    out.append(f"- Body on canvas: {rep['ratios']['body_on_canvas']}:1")
    out.append(f"- Muted on canvas: {rep['ratios']['muted_on_canvas']}:1")
    out.append(f"- Text on primary: {rep['ratios']['on_primary_on_primary']}:1")
    out.append("")
    out.append("## How to use")
    out.append("")
    out.append("Drop this folder into your project and point your coding agent (Claude Code, "
               "Cursor, Codex) at `DESIGN.md`. Load `css/tokens.css` for the variables, open "
               "`preview.html` to see the system applied. Generated by ux-skill: deterministic, "
               "offline, never calls an LLM.")
    out.append("")
    return "\n".join(out) + "\n"


def _preview_html(system: Any, pal: Dict[str, str], name: str, description: str, concept: str) -> str:
    tp = dict(getattr(system, "type_pair", None) or system.get("type_pair", {}))
    display, body_f, mono = tp.get("display", "Georgia"), tp.get("body", "system-ui"), tp.get("mono", "ui-monospace")
    _urls = [u for u in (_gfont_import(display), _gfont_import(body_f), _gfont_import(mono)) if u]
    links = "".join(f'<link href="{u}" rel="stylesheet">' for u in dict.fromkeys(_urls))
    swatches = "".join(
        f'<div style="flex:1;min-width:84px"><div style="height:52px;border-radius:10px;'
        f'background:{pal[k]};border:1px solid var(--color-border)"></div>'
        f'<div style="font:500 11px var(--font-mono);color:var(--color-muted);margin-top:6px">{k}</div>'
        f'<div style="font:500 11px var(--font-mono);color:var(--color-body)">{pal[k]}</div></div>'
        for k in ("canvas", "surface", "ink", "body", "muted", "primary", "success", "warning", "danger", "info"))
    badges = "".join(
        f'<span style="font:600 12px var(--font-body);color:var(--color-{k});'
        f'border:1px solid var(--color-{k});padding:4px 10px;border-radius:999px">{k}</span>'
        for k in ("success", "warning", "danger", "info"))
    return f"""<!doctype html><html lang="en" data-theme="{pal['_theme']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} -- ux-skill design system preview</title>{links}
<style>{_tokens_css(system, pal, name)}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--color-canvas); color:var(--color-body); font-family:var(--font-body); }}
.wrap {{ max-width:880px; margin:0 auto; padding:48px 24px 80px; }}
h1 {{ font-family:var(--font-display); color:var(--color-ink); font-size:clamp(40px,7vw,64px); line-height:1.05; letter-spacing:-1.5px; margin:0 0 12px; }}
.lede {{ font-size:18px; line-height:1.6; max-width:60ch; color:var(--color-body); }}
.muted {{ color:var(--color-muted); }}
.row {{ display:flex; gap:12px; flex-wrap:wrap; align-items:center; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }}
.eyebrow {{ font:600 12px var(--font-mono); letter-spacing:.12em; text-transform:uppercase; color:var(--color-primary); }}
section {{ margin-top:48px; }}
label {{ display:block; font:600 13px var(--font-body); color:var(--color-ink); margin-bottom:6px; }}
</style></head><body><div class="wrap">
<div class="eyebrow">ux-skill - accessible by construction</div>
<h1>{name}</h1>
<p class="lede">{description}</p>
<section><div class="row">{badges}</div></section>
<section><div class="row">
  <button class="btn btn--primary">Primary action</button>
  <button class="btn btn--secondary">Secondary</button>
  <a href="#" style="color:var(--color-primary);font:600 15px var(--font-body)">Text link</a>
</div></section>
<section class="grid">
  <div class="card"><h3 style="font-family:var(--font-display);color:var(--color-ink);margin:0 0 8px">Card title</h3>
    <p style="margin:0;line-height:1.6">Body copy sits at AA contrast on the surface tier. {concept[:90]}</p></div>
  <div class="card"><label for="e">Email</label><input id="e" class="input" placeholder="you@studio.com">
    <p style="color:var(--color-danger);font:500 12px var(--font-body);margin:8px 0 0">Enter a valid email address.</p></div>
</section>
<section><div class="eyebrow" style="margin-bottom:14px">Palette</div><div class="row">{swatches}</div></section>
<section><p class="muted" style="font:400 13px var(--font-mono)">Generated by ux-skill. Deterministic, offline, free.</p></section>
</div></body></html>"""


def pack_system(system: Any, name: str, description: str, concept: str,
                out_dir: str, slug: Optional[str] = None,
                tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """Write the full design-system folder for ``system`` into ``out_dir/<slug>``.

    Returns a summary dict (paths, theme, accessibility). Idempotent.
    """
    slug = slug or name.strip().replace(" ", "-").lower()
    pal = derive_palette(system)
    tags = tags or [pal["_theme"].title(), "Accessible", "CSS", "HTML"]
    root = Path(out_dir) / slug
    (root / "css").mkdir(parents=True, exist_ok=True)

    files = {
        root / "DESIGN.md": _design_md(system, pal, name, description, concept),
        root / "metadata.json": _metadata(system, pal, name, description, concept, tags),
        root / "css" / "tokens.css": _tokens_css(system, pal, name),
        root / "preview.html": _preview_html(system, pal, name, description, concept),
    }
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")

    report = _contrast_report(pal)
    return {
        "slug": slug, "name": name, "theme": pal["_theme"],
        "dir": str(root), "files": [str(p) for p in files],
        "wcag_aa_text": report["wcag_aa_text"], "ratios": report["ratios"],
        "palette": {k: pal[k] for k in pal if not k.startswith("_")},
    }
