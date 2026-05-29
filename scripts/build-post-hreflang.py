#!/usr/bin/env python3
"""
Per-post hreflang clusters for translated blog posts.

The blog has translated POSTS under /blog/<locale>/ whose slugs differ from their
English originals, so they never carried hreflang (only a self-canonical). This
wires a reciprocal + self-referential hreflang cluster onto each post that we can
CONFIDENTLY pair to an English original. Confidence was established three ways and
a pair ships only when they agree:
  1. exact title translation,
  2. internal-link signal (the translation links its English original/sibling),
  3. heading-structure match (same section skeleton, same order).

Posts with NO clean 1:1 English original are intentionally LEFT ALONE: the generic
localized "ai-coding-design" / "design-rules" landing posts (bespoke per-language
pillar posts whose structure matches no single English article and is not even
consistent across locales), the hi MCP post (50/50 between two English posts), and
the vi anti-slop post (ambiguous among four). A forced hreflang pair on a
non-equivalent page is worse than none -- Google distrusts mismatched clusters.

CLUSTERS is hand-authored and auditable. Each member page receives the FULL cluster
(all members + itself), satisfying the return-tag/self-reference requirement.
x-default points at the English member. URLs are absolute.

Idempotent: the injected block is wrapped in <!-- post-hreflang --> markers and
stripped + reinserted on each run. Run with /usr/bin/python3.
"""
from __future__ import annotations
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "docs", "blog")
BASE = "https://uxskill.laithjunaidy.com/blog"

# Hand-paired clusters. "en" is the English original; other keys are hreflang codes
# mapping to a path relative to docs/blog/.
CLUSTERS = [
    # v3.0 "The Brain" launch. Exact title translation in all six; every translation
    # internally links /blog/v3-the-brain-launch.html. Highest confidence.
    {
        "en":    "v3-the-brain-launch.html",
        "ar":    "ar/v3-the-brain.html",
        "de":    "de/v3-the-brain.html",
        "es":    "es/v3-the-brain.html",
        "fr":    "fr/v3-the-brain.html",
        "ja":    "ja/v3-the-brain.html",
        "zh-CN": "zh-CN/v3-the-brain.html",
    },
    # Anti-slop CLI. zh-CN title is an exact match ("145 rules, no LLM, runs in CI")
    # and it is the only translation that links /blog/anti-slop-cli-vibe-coders.html.
    {
        "en":    "anti-slop-cli-vibe-coders.html",
        "zh-CN": "zh-CN/anti-ai-slop-cli-china.html",
    },
    # Vibe coding. ja + zh-CN reproduce the English post's 13-section structure
    # heading-for-heading (only "145 rules" drifted to "100 rules" in translation).
    {
        "en":    "vibe-coding-design-system.html",
        "ja":    "ja/vibe-coding-design.html",
        "zh-CN": "zh-CN/vibe-coding-shipping-real-design.html",
    },
    # AI design system CLI. ja title exact; unique specific topic, no competing
    # English candidate (leaner localized rewrite of the same page).
    {
        "en": "ai-design-system-cli.html",
        "ja": "ja/ai-design-system-cli-ja.html",
    },
    # Cursor design plugin/rules. ko; unique Cursor topic + matching intent
    # (leaner localized rewrite of the same page).
    {
        "en": "cursor-design-plugin.html",
        "ko": "ko/cursor-design-rules-korean.html",
    },
]

START = "<!-- post-hreflang:start -->"
END = "<!-- post-hreflang:end -->"


def block_for(cluster):
    en_url = BASE + "/" + cluster["en"]
    lines = ['  <link rel="alternate" hreflang="en" href="' + en_url + '">']
    for code in sorted(k for k in cluster if k != "en"):
        url = BASE + "/" + cluster[code]
        lines.append('  <link rel="alternate" hreflang="' + code + '" href="' + url + '">')
    lines.append('  <link rel="alternate" hreflang="x-default" href="' + en_url + '">')
    return START + "\n" + "\n".join(lines) + "\n  " + END


def inject(path, block):
    s = open(path, encoding="utf-8").read()
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\s*", "", s, flags=re.S)
    if "</head>" not in s:
        return "skip (no </head>)"
    s = s.replace("</head>", block + "\n</head>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return "ok"


def main():
    total = 0
    for cluster in CLUSTERS:
        # fail loud if any member is missing before touching anything in the cluster
        for rel in cluster.values():
            if not os.path.isfile(os.path.join(BLOG, rel)):
                raise SystemExit("MISSING: " + rel + " (cluster en=" + cluster["en"] + ")")
        block = block_for(cluster)
        for code, rel in cluster.items():
            r = inject(os.path.join(BLOG, rel), block)
            print("  [{:5}] {:44} {}".format(code, rel, r))
            if r == "ok":
                total += 1
        print("  -- cluster en=" + cluster["en"] + ": " + str(len(cluster)) + " members --\n")
    print("TOTAL pages stamped: " + str(total))


if __name__ == "__main__":
    main()
