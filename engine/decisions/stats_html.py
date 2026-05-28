"""Render a local HTML view of the per-install decisions stats.

Writes ``.ux/stats.html`` — a self-contained, single-file dashboard the user
can open in a browser. Shows what their local install has learned.

**No telemetry. No network. Local file only.**

The page contains:
  - Total decisions logged
  - Per-command breakdown
  - Top brands picked
  - Lint score histogram + median
  - Acceptance rate
  - Per-industry usage
  - Mode distribution (pure_synthesis / brand_anchor / strict_brand)
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict

from engine.decisions import stats as _stats


def _bar(value: int, max_v: int, w: int = 200) -> str:
    if max_v <= 0:
        pct = 0
    else:
        pct = int((value / max_v) * w)
    return (f'<span class="bar"><span class="fill" '
            f'style="width:{pct}px"></span></span>')


def _section_dict(title: str, d: Dict[str, int]) -> str:
    if not d:
        return f"<h2>{html.escape(title)}</h2><p class='empty'>No data yet.</p>"
    items = sorted(d.items(), key=lambda kv: -kv[1])
    max_v = max(d.values()) if d else 0
    rows = []
    for k, v in items:
        rows.append(
            "<li>"
            f"<span class='label'>{html.escape(str(k))}</span>"
            f"{_bar(v, max_v)}"
            f"<span class='value'>{v}</span>"
            "</li>"
        )
    return (f"<h2>{html.escape(title)}</h2>"
            f"<ul class='ranked'>{''.join(rows)}</ul>")


def render_html(stats_payload: Dict[str, Any]) -> str:
    total = stats_payload.get("total_decisions", 0)
    by_cmd = stats_payload.get("by_command", {})
    by_industry = stats_payload.get("by_industry", {})
    by_ui_type = stats_payload.get("by_ui_type", {})
    by_mode = stats_payload.get("by_mode", {})
    top_brands = stats_payload.get("top_brands", {})
    median = stats_payload.get("lint_score_median")
    mean = stats_payload.get("lint_score_mean")
    accepted = stats_payload.get("accepted_count", 0)
    acc_rate = stats_payload.get("acceptance_rate")

    median_str = "—" if median is None else f"{median:.1f}"
    mean_str = "—" if mean is None else f"{mean:.1f}"
    rate_str = "—" if acc_rate is None else f"{int(acc_rate * 100)}%"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ux-skill — your install's local stats</title>
<style>
  :root {{
    --canvas: #07080a;
    --surface: #0e1014;
    --ink: #f6f7f9;
    --body: #c0c3c9;
    --muted: #8a8f96;
    --accent: #cc785c;
    --hairline: rgba(255,255,255,0.08);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: var(--canvas); color: var(--ink);
    font-family: -apple-system, system-ui, sans-serif; line-height: 1.5; }}
  .wrap {{ max-width: 920px; margin: 0 auto; padding: clamp(20px, 4vw, 56px); }}
  header {{ margin-bottom: 36px; padding-bottom: 24px; border-bottom: 1px solid var(--hairline); }}
  h1 {{ font-size: clamp(28px, 4vw, 44px); letter-spacing: -0.02em; margin-bottom: 8px; }}
  .lede {{ color: var(--body); max-width: 60ch; }}
  .pillrow {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }}
  .pill {{ display: inline-block; padding: 4px 12px; border: 1px solid var(--hairline);
    border-radius: 999px; font-family: ui-monospace, monospace; font-size: 11.5px;
    color: var(--body); letter-spacing: 0.05em; }}
  .pill b {{ color: var(--ink); font-weight: 700; }}
  h2 {{ font-size: 18px; margin-top: 36px; margin-bottom: 16px; color: var(--ink); }}
  .empty {{ color: var(--muted); font-style: italic; padding: 6px 0; }}
  ul.ranked {{ list-style: none; }}
  ul.ranked li {{ display: grid; grid-template-columns: minmax(0, 1fr) 220px 60px;
    align-items: center; gap: 12px; padding: 6px 0; border-bottom: 1px solid var(--hairline);
    font-family: ui-monospace, monospace; font-size: 13px; }}
  .label {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--body); }}
  .value {{ text-align: right; color: var(--ink); font-weight: 700; }}
  .bar {{ display: inline-block; height: 6px; width: 200px; background: rgba(255,255,255,0.04);
    border-radius: 3px; overflow: hidden; }}
  .fill {{ display: block; height: 100%; background: var(--accent); }}
  footer {{ margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--hairline);
    color: var(--muted); font-family: ui-monospace, monospace; font-size: 11.5px; }}
  a {{ color: var(--accent); }}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>What your install has learned</h1>
<p class="lede">A live readout of <code>.ux/decisions.jsonl</code> + <code>~/.uxskill/decisions.jsonl</code>. No telemetry — this is local. Every <code>recommend</code> / <code>design</code> / <code>lint</code> / <code>evolve</code> call writes one line to the ledger. The recommender re-ranks based on this data once you have &gt;= 3 prior decisions in a bucket.</p>
<div class="pillrow">
  <span class="pill"><b>{total}</b> decisions</span>
  <span class="pill">lint score median: <b>{median_str}</b></span>
  <span class="pill">lint score mean: <b>{mean_str}</b></span>
  <span class="pill">accepted: <b>{accepted}</b> / {total}</span>
  <span class="pill">acceptance rate: <b>{rate_str}</b></span>
</div>
</header>

{_section_dict("By command", by_cmd)}
{_section_dict("By mode (synthesis dispatch)", by_mode)}
{_section_dict("Top brands picked", top_brands)}
{_section_dict("By industry", by_industry)}
{_section_dict("By UI type", by_ui_type)}

<footer>
  ux-skill v2.1 &middot; local stats &middot; MIT &middot; no telemetry &middot; no network &middot;
  re-run <code>uxskill stats --html</code> to refresh
</footer>
</div>
</body>
</html>
"""


def write_stats_html(out_path: Path = Path(".ux/stats.html")) -> Path:
    """Render the stats HTML and write to .ux/stats.html. Returns the path."""
    payload = _stats()
    out = render_html(payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    return out_path
