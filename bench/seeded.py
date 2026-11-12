"""The seeded-defect set: small pages with one planted fault each, mapped to
the rule that should find it, and a near-miss clean twin for every one.

A fault page holds exactly one planted fault. Its twin is the same page with
the fault replaced by something that looks like it and is fine. Recall per
rule is planted faults found over planted faults. A twin on which the rule
still fires is a near-miss false positive, reported beside the recall.

The pages are written by ``python -m bench seed`` from SPEC below and
committed, so the set is frozen like the corpus. Each new check adds its
fault and twin here (PLAN-5.0 Phase 1).

Faults were written for this set, not copied from tests/lint_corpus, so the
recall is not the unit fixtures measured again.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from bench import SEEDED

BASE = """<!DOCTYPE html>
<html{html_attr}>
<head>
<meta charset="utf-8">
{viewport}
<title>Seeded page {sid}</title>
<style>
body {{ margin: 0; color: #1a1a1a; background: #ffffff; line-height: 1.5; }}
main {{ max-width: 40rem; margin: 0 auto; padding: 1.5rem; }}
{style}
</style>
</head>
<body>
<main>
<h1>Field guide to street trees</h1>
<p>Notes on the trees planted along the east side of the river, block by block.</p>
{body}
</main>
</body>
</html>
"""
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'
SVG_ICON = (
    '<svg width="16" height="16" viewBox="0 0 16 16"{aria}><path d="M2 8h12M8 2v12" '
    'stroke="currentColor" stroke-width="2" fill="none"/></svg>'
)
SQUARE = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' "
    "height='100'%3E%3Crect width='100' height='100' fill='%23557755'/%3E%3C/svg%3E"
)

# rule id, pass, fault parts, twin parts, and optional "more" faults written
# another way and "more_twins". Parts: style, body, html_attr, viewport.
SPEC: List[Dict[str, Any]] = [
    {
        "rule": "href-empty-hash",
        "pass": "static",
        "fault": {"body": '<p><a href="#">Read the planting schedule</a></p>'},
        "twin": {
            "body": '<p><a href="#schedule">Read the planting schedule</a></p>'
            '<h2 id="schedule">Schedule</h2><p>Spring and autumn.</p>'
        },
    },
    {
        "rule": "img-no-dimensions",
        "pass": "static",
        "fault": {"body": f'<img src="{SQUARE}" alt="A young oak in a planting pit">'},
        "twin": {
            "body": f'<img src="{SQUARE}" width="100" height="100" '
            'alt="A young oak in a planting pit">'
        },
    },
    {
        "rule": "placeholder-as-label",
        "pass": "static",
        "fault": {
            "body": '<form><input type="email" name="email" placeholder="Email" '
            'autocomplete="email"><button type="submit">Subscribe</button></form>'
        },
        "twin": {
            "body": '<form><label for="em">Email</label><input id="em" type="email" '
            'name="email" placeholder="name@example.org" autocomplete="email">'
            '<button type="submit">Subscribe</button></form>'
        },
    },
    {
        "rule": "button-no-type",
        "pass": "static",
        "fault": {"body": "<button>Show more trees</button>"},
        "twin": {"body": '<button type="button">Show more trees</button>'},
    },
    {
        "rule": "viewport-no-zoom",
        "pass": "static",
        "fault": {
            "viewport": '<meta name="viewport" content="width=device-width, '
            'initial-scale=1, maximum-scale=1, user-scalable=no">'
        },
        "twin": {
            "viewport": '<meta name="viewport" content="width=device-width, '
            'initial-scale=1, user-scalable=yes">'
        },
    },
    {
        "rule": "lang-attribute-missing",
        "pass": "static",
        "fault": {"html_attr": ""},
        "twin": {"html_attr": ' lang="en-GB"'},
    },
    {
        "rule": "outline-none-no-focus-visible",
        "pass": "static",
        "fault": {
            "style": ".more:focus { outline: none; }",
            "body": '<p><a class="more" href="/trees">All trees</a></p>',
        },
        "twin": {
            "style": ".more:focus { outline: none; }\n"
            ".more:focus-visible { outline: 2px solid #1a4d2e; outline-offset: 2px; }",
            "body": '<p><a class="more" href="/trees">All trees</a></p>',
        },
    },
    {
        "rule": "target-blank-no-noopener",
        "pass": "static",
        "fault": {
            "body": '<p><a href="https://example.org/canopy" target="_blank">Canopy data</a></p>'
        },
        "twin": {
            "body": '<p><a href="https://example.org/canopy" target="_blank" '
            'rel="noopener noreferrer">Canopy data</a></p>'
        },
    },
    {
        "rule": "emoji-in-ui",
        "pass": "static",
        "fault": {
            "body": '<p><button type="button" class="icon-btn">&#128640; Launch map</button></p>'
        },
        "twin": {
            "body": '<p><button type="button" class="icon-btn">'
            + SVG_ICON.format(aria=' aria-hidden="true"')
            + " Launch map</button></p>"
        },
    },
    {
        "rule": "lorem-ipsum-leak",
        "pass": "static",
        "fault": {"body": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>"},
        "twin": {"body": "<p>Plane trees tolerate compacted soil better than most species.</p>"},
    },
    {
        "rule": "generic-cta-text",
        "pass": "static",
        "fault": {"body": '<p><a class="btn" href="/volunteer">Learn more</a></p>'},
        "twin": {
            "body": '<p><a class="btn" href="/volunteer">Volunteer for a planting day</a></p>'
        },
    },
    {
        "rule": "heading-skip-h1-h3",
        "pass": "static",
        "fault": {"body": "<h3>Species</h3><p>Oak, plane, lime.</p>"},
        "twin": {"body": "<h2>Species</h2><p>Oak, plane, lime.</p>"},
    },
    {
        "rule": "inline-style-attribute",
        "pass": "static",
        "fault": {"body": '<p style="color: #555; margin-top: 2rem">Updated in spring.</p>'},
        "twin": {
            "style": ".meter { width: var(--filled); height: 4px; background: #1a4d2e; }",
            "body": '<div class="meter" style="--filled: 40%"></div>',
        },
    },
    {
        "rule": "h-screen-no-dvh-fallback",
        "pass": "static",
        "fault": {
            "style": ".cover { min-height: 100vh; }",
            "body": '<section class="cover"></section>',
        },
        "twin": {
            "style": ".cover { min-height: 100vh; min-height: 100dvh; }",
            "body": '<section class="cover"></section>',
        },
    },
    {
        "rule": "transition-property-all",
        "pass": "static",
        "fault": {
            "style": ".btn { transition: all 0.2s ease-out; }",
            "body": '<p><a class="btn" href="/map">Open the map</a></p>',
        },
        "twin": {
            "style": ".btn { transition: background-color 0.2s ease-out; }",
            "body": '<p><a class="btn" href="/map">Open the map</a></p>',
        },
    },
    {
        "rule": "arbitrary-z-index-9999",
        "pass": "static",
        "fault": {
            "style": ".notice { position: relative; z-index: 9999; }",
            "body": '<p class="notice">Planting resumes in March.</p>',
        },
        "twin": {
            "style": ".notice { position: relative; z-index: 20; }",
            "body": '<p class="notice">Planting resumes in March.</p>',
        },
    },
    {
        "rule": "purple-to-blue-gradient",
        "pass": "static",
        "fault": {
            "style": ".band { background: linear-gradient(90deg, #7c3aed, #2563eb); "
            "height: 3rem; }",
            "body": '<div class="band"></div>',
        },
        "twin": {
            "style": ".band { background: linear-gradient(90deg, #1e3a8a, #1d4ed8); "
            "height: 3rem; }",
            "body": '<div class="band"></div>',
        },
    },
    {
        "rule": "text-align-justify-web",
        "pass": "static",
        "fault": {"style": "p { text-align: justify; }"},
        "twin": {"style": "p { text-align: start; }"},
    },
    {
        "rule": "fake-name-john-doe",
        "pass": "static",
        "fault": {"body": "<table><tr><th>Volunteer</th></tr><tr><td>John Doe</td></tr></table>"},
        "twin": {"body": "<table><tr><th>Volunteer</th></tr><tr><td>Maya Iqbal</td></tr></table>"},
    },
    {
        "rule": "testimonial-fake-five-stars",
        "pass": "static",
        "fault": {
            "body": '<blockquote class="testimonial"><div class="stars">&#9733;&#9733;&#9733;'
            "&#9733;&#9733;</div><p>Our street is cooler.</p></blockquote>"
        },
        "twin": {
            "body": '<blockquote class="testimonial"><p>Our street is cooler.</p>'
            "<cite>Resident, River Street</cite></blockquote>"
        },
    },
    {
        "rule": "infinite-animation-without-reduced-motion",
        "pass": "static",
        "fault": {
            "style": "@keyframes sway { to { transform: rotate(3deg); } }\n"
            ".leaf { display: inline-block; animation: sway 2s ease-in-out infinite alternate; }",
            "body": '<p><span class="leaf">Leaf</span></p>',
        },
        "twin": {
            "style": "@keyframes sway { to { transform: rotate(3deg); } }\n"
            ".leaf { display: inline-block; animation: sway 2s ease-in-out infinite alternate; }\n"
            "@media (prefers-reduced-motion: reduce) { .leaf { animation: none; } }",
            "body": '<p><span class="leaf">Leaf</span></p>',
        },
    },
    {
        "rule": "animating-layout-properties",
        "pass": "static",
        "fault": {
            "style": ".drawer { width: 0; overflow: hidden; transition: width 0.3s ease-out; }\n"
            ".drawer.open { width: 20rem; }",
            "body": '<div class="drawer"></div>',
        },
        "twin": {
            "style": ".drawer { transform: translateX(-100%); transition: transform 0.3s ease-out; }\n"
            ".drawer.open { transform: none; }",
            "body": '<div class="drawer"></div>',
        },
    },
    {
        "rule": "input-purpose-missing",
        "pass": "static",
        "fault": {
            "body": '<form><label for="e2">Email</label><input id="e2" type="email" '
            'name="email"><button type="submit">Send</button></form>'
        },
        "twin": {
            "body": '<form><label for="e2">Email</label><input id="e2" type="email" '
            'name="email" autocomplete="email"><button type="submit">Send</button></form>'
        },
    },
    {
        "rule": "inline-svg-no-aria",
        "pass": "static",
        "fault": {"body": "<p>" + SVG_ICON.format(aria="") + " Planted</p>"},
        "twin": {"body": "<p>" + SVG_ICON.format(aria=' aria-hidden="true"') + " Planted</p>"},
    },
    {
        "rule": "default-font-only",
        "pass": "static",
        "fault": {"style": "body { font-family: Inter, system-ui, sans-serif; }"},
        "twin": {
            "style": "body { font-family: Inter, system-ui, sans-serif; }\n"
            "h1, h2 { font-family: Fraunces, Georgia, serif; }"
        },
    },
    {
        "rule": "placeholder-token-shipped",
        "pass": "static",
        "fault": {"body": "<p>Questions? Write to {{CONTACT_EMAIL}}.</p>"},
        "twin": {"body": "<p>Questions? Write to trees@example.org.</p>"},
    },
    {
        "rule": "glow-shadow-zero-offset",
        "pass": "static",
        "fault": {
            "style": ".card { box-shadow: 0 0 40px rgba(124, 58, 237, 0.5); }",
            "body": '<div class="card"><p>Oak</p></div>',
        },
        "twin": {
            "style": ".card { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12); }",
            "body": '<div class="card"><p>Oak</p></div>',
        },
    },
    {
        "rule": "hairline-border-heavy-shadow",
        "pass": "static",
        "fault": {
            "style": ".card { border: 1px solid #e5e5e5; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25); }",
            "body": '<div class="card"><p>Lime</p></div>',
        },
        "twin": {
            "style": ".card { border: 1px solid #e5e5e5; }",
            "body": '<div class="card"><p>Lime</p></div>',
        },
    },
    {
        "rule": "focusable-at-opacity-zero",
        "pass": "static",
        "fault": {
            "style": ".menu { opacity: 0; }",
            "body": '<nav class="menu"><a href="/trees">Trees</a></nav>',
        },
        "twin": {
            "style": ".menu { opacity: 0; visibility: hidden; }",
            "body": '<nav class="menu"><a href="/trees">Trees</a></nav>',
        },
    },
    # Render checks: need Playwright.
    {
        "rule": "horizontal-overflow",
        "pass": "render",
        "fault": {
            "style": ".strip { width: 1400px; height: 2rem; background: #1a4d2e; }",
            "body": '<div class="strip"></div>',
        },
        "twin": {
            "style": ".strip { width: 1400px; max-width: 100%; height: 2rem; background: #1a4d2e; }",
            "body": '<div class="strip"></div>',
        },
    },
    {
        "rule": "text-overflows-its-box",
        "pass": "render",
        "fault": {
            "style": ".tag { display: block; width: 6rem; white-space: nowrap; overflow: visible; }",
            "body": '<p class="tag">Platanus-x-hispanica-London-plane-specimen</p>',
        },
        "twin": {
            "style": ".tag { display: block; width: 6rem; overflow-wrap: anywhere; }",
            "body": '<p class="tag">Platanus-x-hispanica-London-plane-specimen</p>',
        },
    },
    {
        "rule": "input-text-zooms",
        "pass": "render",
        "fault": {
            "style": ".q { font-size: 13px; }",
            "body": '<form><label for="q">Search</label><input id="q" class="q" type="search" '
            'name="q" autocomplete="off"></form>',
        },
        "twin": {
            "style": ".q { font-size: 16px; }",
            "body": '<form><label for="q">Search</label><input id="q" class="q" type="search" '
            'name="q" autocomplete="off"></form>',
        },
    },
    {
        "rule": "text-low-contrast",
        "pass": "render",
        "fault": {
            "style": ".faint { color: #b0b0b0; }",
            "body": '<p class="faint">Survey data from the 2025 count.</p>',
        },
        "twin": {
            "style": ".faint { color: #595959; }",
            "body": '<p class="faint">Survey data from the 2025 count.</p>',
        },
    },
    {
        "rule": "target-too-small",
        "pass": "render",
        "fault": {
            "style": ".tiny { width: 14px; height: 14px; padding: 0; margin: 0; border: 0; }",
            "body": '<p><button type="button" class="tiny" aria-label="Previous"></button>'
            '<button type="button" class="tiny" aria-label="Next"></button></p>',
        },
        "twin": {
            "style": ".tiny { width: 24px; height: 24px; padding: 0; margin: 0 4px; border: 0; }",
            "body": '<p><button type="button" class="tiny" aria-label="Previous"></button>'
            '<button type="button" class="tiny" aria-label="Next"></button></p>',
        },
    },
    {
        "rule": "image-distorted",
        "pass": "render",
        "fault": {
            "style": ".ph { width: 300px; height: 100px; }",
            "body": f'<img class="ph" src="{SQUARE}" width="100" height="100" alt="Planting pit">',
        },
        "twin": {
            "style": ".ph { width: 300px; height: 100px; object-fit: cover; }",
            "body": f'<img class="ph" src="{SQUARE}" width="100" height="100" alt="Planting pit">',
        },
    },
    {
        "rule": "focus-ring-missing",
        "pass": "render",
        "fault": {
            "style": ".go { outline: none; border: 0; background: #1a4d2e; color: #fff; padding: 0.75rem 1rem; }\n"
            ".go:focus { outline: none; }",
            "body": '<p><button type="button" class="go">Find a tree</button></p>',
        },
        "twin": {
            "style": ".go { border: 0; background: #1a4d2e; color: #fff; padding: 0.75rem 1rem; }\n"
            ".go:focus-visible { outline: 3px solid #b8860b; outline-offset: 2px; }",
            "body": '<p><button type="button" class="go">Find a tree</button></p>',
        },
    },
    {
        "rule": "infinite-animation-under-reduced-motion",
        "pass": "render",
        "fault": {
            "style": "@keyframes sway { to { transform: rotate(3deg); } }\n"
            ".leaf { display: inline-block; animation: sway 2s ease-in-out infinite alternate; }",
            "body": '<p><span class="leaf">Leaf</span></p>',
        },
        "twin": {
            "style": "@keyframes sway { to { transform: rotate(3deg); } }\n"
            ".leaf { display: inline-block; animation: sway 2s ease-in-out infinite alternate; }\n"
            "@media (prefers-reduced-motion: reduce) { .leaf { animation: none; } }",
            "body": '<p><span class="leaf">Leaf</span></p>',
        },
    },
]

# Second and third ways of writing the same fault, and further near misses.
MORE: Dict[str, Dict[str, List[Dict[str, str]]]] = {
    "href-empty-hash": {
        "more": [
            {"body": "<nav><a class='nav-link' href='#'>Map</a></nav>"},
            {"body": '<p><a href="#" role="button" class="close">Close</a></p>'},
        ],
        "more_twins": [{"body": '<p><a href="#top">Back to top</a></p>'}],
    },
    "img-no-dimensions": {"more": [{"body": f'<img alt="An oak" src="{SQUARE}" width="100">'}]},
    "placeholder-as-label": {
        "more": [
            {
                "body": '<form><textarea name="note" placeholder="Your note"></textarea>'
                '<button type="submit">Send</button></form>'
            }
        ],
        "more_twins": [
            {
                "body": '<form><input type="search" name="q" aria-label="Search trees" '
                'placeholder="Oak, plane, lime"></form>'
            }
        ],
    },
    "button-no-type": {
        "more": [{"body": '<p><button class="btn" onclick="history.back()">Back</button></p>'}]
    },
    "target-blank-no-noopener": {
        "more": [{"body": '<p><a target="_blank" href="https://example.org/map">Map</a></p>'}]
    },
    "outline-none-no-focus-visible": {
        "more": [
            {
                "style": ".more:focus { outline: 0; }",
                "body": '<p><a class="more" href="/trees">All trees</a></p>',
            }
        ],
        "more_twins": [
            {
                "style": ".field input:focus { outline: none; }\n"
                ".field:focus-within { box-shadow: 0 0 0 3px #1a4d2e; }",
                "body": '<div class="field"><label for="f1">Street</label>'
                '<input id="f1" name="street" autocomplete="street-address"></div>',
            }
        ],
    },
    "transition-property-all": {
        "more": [
            {
                "style": ".btn { transition: 0.2s ease-out; }",
                "body": '<p><a class="btn" href="/map">Open the map</a></p>',
            }
        ]
    },
    "h-screen-no-dvh-fallback": {
        "more": [{"style": ".hero { height: 100vh; }", "body": '<section class="hero"></section>'}]
    },
    "lorem-ipsum-leak": {"more": [{"body": "<h2>Lorem Ipsum</h2><p>Plane trees.</p>"}]},
    "generic-cta-text": {
        "more": [{"body": '<p>For the schedule, <a href="/schedule">click here</a>.</p>'}]
    },
    "default-font-only": {"more": [{"style": 'body { font-family: "Geist", sans-serif; }'}]},
    "fake-name-john-doe": {"more": [{"body": "<ul><li>Jane Doe, volunteer</li></ul>"}]},
    "inline-svg-no-aria": {
        "more_twins": [
            {
                "body": '<p><svg role="img" aria-labelledby="t1" width="16" height="16" '
                'viewBox="0 0 16 16"><title id="t1">Planted</title><path '
                'd="M2 8h12" stroke="currentColor"/></svg></p>'
            }
        ]
    },
    "heading-skip-h1-h3": {"more": [{"body": "<h2>Species</h2><h4>Oak</h4><p>Native.</p>"}]},
    "emoji-in-ui": {"more": [{"body": '<nav><a href="/map">&#128205; Map</a></nav>'}]},
    "text-align-justify-web": {
        "more": [
            {
                "style": ".lead { text-align: justify; }",
                "body": '<p class="lead">Notes on trees.</p>',
            }
        ]
    },
}
for _spec in SPEC:
    _spec.update(MORE.get(_spec["rule"], {}) if _spec["pass"] == "static" else {})


def page(sid: str, parts: Dict[str, str]) -> str:
    return BASE.format(
        sid=sid,
        html_attr=parts.get("html_attr", ' lang="en"'),
        viewport=parts.get("viewport", VIEWPORT),
        style=parts.get("style", ""),
        body=parts.get("body", ""),
    )


def build() -> Dict[str, Any]:
    """Write every fault page, its twin and the base page, and plants.json."""
    pages_dir = SEEDED / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    for old in pages_dir.glob("*.html"):
        old.unlink()
    rows: List[Dict[str, Any]] = []
    (pages_dir / "base.html").write_text(page("base", {}), encoding="utf-8")
    rows.append({"id": "base", "file": "base.html", "kind": "base", "rule": None, "pass": "both"})
    seen = set()
    for spec in SPEC:
        rule = spec["rule"]
        stem = rule if rule not in seen else f"{rule}-{spec['pass']}"
        seen.add(rule)
        variants = [("fault", spec["fault"]), ("twin", spec["twin"])]
        variants += [("fault", v) for v in spec.get("more", [])]
        variants += [("twin", v) for v in spec.get("more_twins", [])]
        count: Dict[str, int] = {}
        for kind, parts in variants:
            count[kind] = count.get(kind, 0) + 1
            sid = f"{stem}.{kind}{count[kind]}"
            (pages_dir / f"{sid}.html").write_text(page(sid, parts), encoding="utf-8")
            rows.append(
                {"id": sid, "file": f"{sid}.html", "kind": kind, "rule": rule, "pass": spec["pass"]}
            )
    data = {
        "note": "Written by python -m bench seed from bench/seeded.py; do not edit by hand.",
        "pages": rows,
    }
    (SEEDED / "plants.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    return data


def recall(result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Per planted rule: faults planted, found, and twins it still fired on.
    A rule that fires on the base page is reported as noise, since it would
    fire on every fault page whatever was planted."""
    plants = json.loads((SEEDED / "plants.json").read_text(encoding="utf-8"))["pages"]
    fired = {pid: {f["rule"] for f in page["findings"]} for pid, page in result["pages"].items()}
    base = fired.get("base", set())
    out: Dict[str, Dict[str, Any]] = {}
    for row in plants:
        if row["kind"] == "base":
            continue
        r = out.setdefault(
            row["rule"],
            {
                "pass": row["pass"],
                "planted": 0,
                "found": 0,
                "twins": 0,
                "twin_fired": 0,
                "on_base": False,
            },
        )
        r["on_base"] = row["rule"] in base
        got = row["rule"] in fired.get(row["id"], set())
        if row["kind"] == "fault":
            r["planted"] += 1
            r["found"] += got
        else:
            r["twins"] += 1
            r["twin_fired"] += got
    if not result.get("render"):
        for r in out.values():
            if r["pass"] == "render":
                r["skipped"] = "render pass did not run"
    return out
