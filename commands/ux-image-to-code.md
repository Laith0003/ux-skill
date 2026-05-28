---
name: ux-image-to-code
description: Take a design reference image (PNG/JPG/WebP), extract its dominant palette + canvas polarity + type signal via pure Pillow CV, match the result against the v2 palettes/styles manifests, and run the recommender on the synthetic brief. Returns the closest palette, the closest style, and a full recommended design system grounded in what the image actually shows.
allowed-tools: Bash, Read, Write
disable-model-invocation: false
---

# /ux-image-to-code — turn a design image into a generated system

**Pure CV. No multimodal LLM.**

Hand the engine a screenshot or a design reference; it returns a Brief, a closest-match palette, a closest-match style, and a full Recommendation. No vision model is called. Every signal is computed deterministically from pixels via Pillow.

## When to use

- You have a reference design (a competitor screenshot, a Dribbble shot, a Figma export) and you want the engine to build something in that direction.
- You want to "anchor" `/ux-recommend` on a real image instead of a typed brief.
- You want to verify the engine's read on a design before generating code.

## When to skip

- The reference is text (a written brief, a PRD) → use `/ux-discover` + `/ux-recommend`.
- You already have a saved discovery → just run `/ux-recommend`.
- You want pixel-perfect cloning → this is a HINT generator, not a copy-paste tool.

## How it runs

```bash
python3 -m engine.cli.main image-extract path/to/reference.png
```

What happens, step by step:

1. **Decode + downsample** — Pillow opens the image and resizes the long edge to 512px to keep quantization fast.
2. **Quantize to 5 colors** — `Image.quantize(colors=5, method=MAXCOVERAGE)` finds the dominant tones. (This is a deterministic palette reduction, equivalent in shape to a small k-means but without sklearn.)
3. **Canvas polarity** — average luminance under the sRGB curve. Above 0.5 is light; below is dark.
4. **Type polarity** — ratio of `EDGE_ENHANCE_MORE` variance to `EMBOSS` variance. High ratio leans serif, low leans sans, between is `unknown`. (Heuristic — see Limitations.)
5. **Aspect + density** — `FIND_EDGES` followed by binarization gives a coarse "edge fraction." Lots of edges → dense layout (dashboard, dense editorial). Few edges → airy hero.
6. **Match against manifests** — for each palette in `data/palettes.json`, sum the nearest-neighbour distances between the extracted 5 colors and the palette's canvas/surface/ink/primary anchors. Lowest sum wins.
7. **Style fit** — bias styles whose id/category contains "dark"/"cinema"/"luxe" for dark canvas, "swiss"/"editorial"/"minimal" for light canvas. Boost styles that appear in the matched palette's `compatible_styles`.
8. **Synthetic Brief → recommend** — pack the hints into a `Brief` and run the 5-parallel-search recommender to produce a complete system.

## Usage

### One-shot

```bash
python3 -m engine.cli.main image-extract docs/screenshots/cursor-running-ux.png
```

Returns JSON with `brief`, `hints`, and `recommendation`. Saves to `.ux/last-image-extract.json` by default.

### Skip the recommender (hints only)

```bash
python3 -m engine.cli.main image-extract reference.png --no-recommendation
```

Useful when you just want to see what the engine reads off an image without committing to a full recommendation.

### From an MCP host (Claude Desktop, Cursor, Windsurf)

```jsonc
{
  "tool": "ux_image_extract",
  "arguments": {
    "path": "/abs/path/to/reference.png",
    "with_recommendation": true
  }
}
```

### Direct Python

```python
from engine.image_extract import image_to_brief
from engine.recommender import Brief, recommend

result = image_to_brief("reference.png")
print(result["hints"]["matched_palette_name"])    # e.g. "Linear Graphite"
print(result["hints"]["matched_style_name"])      # e.g. "Monochrome Precise"

# Synthetic brief is Brief-shaped, so it slots straight into recommend().
rec = recommend(Brief(**result["brief"]))
print(rec.style["id"])
```

## Output shape

```jsonc
{
  "image": "docs/screenshots/cursor-running-ux.png",
  "brief": {
    "project_type": "",
    "industry": "",
    "audience": [],
    "tone": ["dark", "cinematic", "spacious", "airy"],
    "must_have": ["dark-mode"],
    "forbidden": ["yellow", "amber", "gold", "cream", "coral", "cormorant"],
    "stack": "",
    "region": ""
  },
  "hints": {
    "dominant_colors": ["#000000", "#065b6b", "#973165", "#ffd031", "#29db43"],
    "canvas_polarity": "dark",
    "type_polarity": "serif",
    "aspect": {
      "aspect_ratio": 1.6,
      "width": 1600,
      "height": 1000,
      "density": 0.0234,
      "orientation": "landscape"
    },
    "matched_palette_id": "dark-monokai",
    "matched_palette_name": "Monokai",
    "matched_style_id": "dark-mode-luxe",
    "matched_style_name": "Dark Mode Luxe"
  },
  "recommendation": {
    "style": { "...": "..." },
    "palette": { "...": "..." },
    "type_pair": { "...": "..." },
    "motion": [],
    "components": [],
    "brand_exemplars": [],
    "guardrails": [],
    "rationale": ["Industry: ...", "Style: ...", "Palette: ..."]
  },
  "saved_to": ".ux/last-image-extract.json"
}
```

## Chaining

The result chains naturally into the rest of the pipeline:

- `/ux-design` — uses the saved `.ux/last-image-extract.json` recommendation to generate code.
- `/ux-system` — generates a full design system from the recommendation.
- `/ux-component <name>` — generates one component using the matched style.

## Limitations (read these)

This is a HEURISTIC pipeline, not a vision model. Be honest about what it can and cannot tell you:

- **Type polarity is a guess.** We sample edge-filter variance ratios; that correlates with serif vs sans-serif but is not OCR. Treat the result as a hint, not ground truth.
- **The matched palette is the closest in our manifest, not the closest globally.** If your reference uses colors no v2 palette covers, the match will pick the least-bad neighbour.
- **No layout reconstruction.** The engine reads color/light/edge density. It does NOT read grid structure, component boundaries, or copy. If you want layout, give it a brief, not an image.
- **No multimodal LLM is consulted.** That is the point — this stays cheap, deterministic, and offline.

## Why this exists

Visual reference is how most designers think. Until now, ux-skill could only take a typed brief. Now you can hand it a screenshot and it will say "the engine sees: dark canvas, blue-graphite tones, sans-serif type — closest match is Linear Graphite + Monochrome Precise. Generating with those tokens..."

Faster than answering 10 questions when you already know what you want.

## Default forbidden list

The synthetic brief auto-populates `forbidden` with the project-wide taste guardrails: `yellow`, `amber`, `gold`, `cream`, `coral`, `cormorant`. The image extraction is for COLOR and POLARITY hints; the forbidden palette/type vocabulary is a separate policy decision the engine respects regardless of what the image suggests.

If you actually want a yellow design (you don't), override:

```bash
python3 -m engine.cli.main image-extract ref.png
# Then edit .ux/last-image-extract.json and remove items from brief.forbidden
python3 -m engine.cli.main recommend --brief-file .ux/last-image-extract.json
```
