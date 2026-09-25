"""The version the public site states, read from pyproject.toml.

Generators import this instead of writing a version by hand, and
tests/test_site_version.py checks every page against it. `claims(html)` lists
each place a page states the current version: the structured data, the hero
pill, the version footer, the catalogue eyebrows, the head metadata and the
hero numeral. Release posts and the roadmap's plan list are history, not
claims about the current version, so they are not read.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterator, List, Tuple

ROOT = Path(__file__).resolve().parent.parent


def version() -> str:
    """Full version, for example 3.2.1."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    return re.search(r'^version\s*=\s*"([^"]+)"', text, re.M).group(1)


def line() -> str:
    """Release line, for example 3.2."""
    return ".".join(version().split(".")[:2])


# (label, regex with the version in group 1)
_VISIBLE = [
    ("hero pill", r'class="pill"><span class="d"></span>v(\d+(?:\.\d+)+)'),
    ("version footer", r'(?:&middot;|·) v(\d+(?:\.\d+)+) (?:&middot;|·) 20\d\d</span>'),
    ("catalogue eyebrow", r'class="top__eyebrow">[^<]*(?:·|&middot;) v(\d+(?:\.\d+)+)'),
    ("preview footer", r'\] uxskill v(\d+(?:\.\d+)+)'),
    ("hero numeral", r'<div class="three" aria-hidden="true">(\d+\.\d+)</div>'),
    ("og image alt", r'giant (\d+\.\d+) numeral'),
    ("roadmap eyebrow", r'Roadmap (?:·|&middot;) v(\d+(?:\.\d+)+)'),
]
_HEAD = [
    ("head title", r'<title>[^<]*\bux-?skill(?: roadmap ·)? v(\d+(?:\.\d+)+)'),
    ("head meta", r'<meta (?:name|property)="(?:description|og:[a-z:]+|twitter:[a-z:]+)" '
                  r'content="[^"]*?\bux-?skill(?: roadmap ·)? v(\d+(?:\.\d+)+)'),
    ("head meta", r'<meta (?:name|property)="(?:description|og:[a-z:]+|twitter:[a-z:]+)" '
                  r'content="v(\d+(?:\.\d+)+) stable'),
]


def _jsonld(html: str) -> Iterator[dict]:
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        for obj in data if isinstance(data, list) else data.get("@graph", [data]):
            if isinstance(obj, dict):
                yield obj


def claims(html: str, is_release_post: bool = False) -> List[Tuple[str, str]]:
    """(label, version) for every current-version claim in a page."""
    out: List[Tuple[str, str]] = []
    for obj in _jsonld(html):
        kind, name = obj.get("@type"), str(obj.get("name", "")).lower()
        if kind == "SoftwareApplication" and name in ("uxskill", "ux-skill", "ux-mcp") and "softwareVersion" in obj:
            out.append(("SoftwareApplication.softwareVersion", obj["softwareVersion"]))
            m = re.match(r"v(\d+(?:\.\d+)+)", str(obj.get("description", "")))
            if m:
                out.append(("SoftwareApplication.description", m.group(1)))
        if kind == "TechArticle" and str(obj.get("url", "")).endswith("CHANGELOG.md"):
            about = obj.get("about") or {}
            if "softwareVersion" in about:
                out.append(("TechArticle.about.softwareVersion", about["softwareVersion"]))
            for v in re.findall(r"v(\d+(?:\.\d+)+)", str(obj.get("headline", ""))):
                out.append(("TechArticle.headline", v))
            for v in re.findall(r"ux-skill (\d+\.\d+\.\d+)", str(obj.get("description", ""))):
                out.append(("TechArticle.description", v))
    for label, rx in _VISIBLE:
        out += [(label, v) for v in re.findall(rx, html)]
    if not is_release_post:
        head = html.split("</head>", 1)[0]
        for label, rx in _HEAD:
            out += [(label, v) for v in re.findall(rx, head)]
    return out


def agrees(stated: str) -> bool:
    """A claim agrees when it is the full version, or the release line when it
    names only major.minor."""
    return stated == version() or (stated.count(".") == 1 and stated == line())
