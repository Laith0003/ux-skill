"""Writes bench/labels/guide.json: the model-made labelling criteria, one per
rule and pass. Edit the criteria here, run it, then python -m bench label.
Run from the repository root: python bench/labels/build_guide.py
"""
import json
H = r"<<<HERE>>>"
BLK = r"[^{}]*"          # inside the same CSS block
def X(match, label, why=""): return {"match": match, "label": label, "why": why}
def A(token, fp=(), why_tp="", default="cantTell"):
    """Excerpt view: FP patterns first, then TP when the token shows."""
    return {"default": default, "why": "excerpt does not show the match",
            "unless": [X(m, "FP", w) for m, w in fp] + ([X(token, "TP", why_tp)] if token else [])}
def B(rules, default="cantTell", why="context does not decide it"):
    return {"default": default, "why": why, "unless": [X(*r) for r in rules]}

G = {}
def rule(rid, a, b, note=""): G[rid] = {"a": a, "b": b, "note": note}

rule("href-empty-hash", A(r"href=[\"']#[\"']", why_tp="bare # link"),
     B([(H + r"<a\b[^>]*href=[\"']#[\"']", "TP", "the link at the match points at a bare #"),
        (H + r"[^<]*href=[\"']#[\"']", "TP", "bare # link at the match")]))
rule("img-no-dimensions",
     A(r"<img\b(?![^>]*\bwidth=)[^>]*>|<img\b(?![^>]*\bheight=)[^>]*>",
       fp=[(r"<img\b(?=[^>]*\bwidth=)(?=[^>]*\bheight=)[^>]*>", "both attributes in the tag")]),
     B([(H + r"<img\b(?=[^>]*\bwidth=)(?=[^>]*\bheight=)[^>]*>", "FP", "the tag has width and height"),
        (H + r"<img\b[^>]*>", "TP", "the tag lacks width or height")]))
rule("image-format-jpg-no-webp-avif", A(r"<img\b[^>]*\.(jpe?g|png)"),
     B([(r"<picture\b(?:(?!</picture>).)*" + H, "FP", "inside a picture element"),
        (H + r"<img\b[^>]*src=[\"'][^\"']*\.(jpe?g|png)", "TP", "a jpg or png img outside picture; the rule covers both")]))
rule("outline-none-no-focus-visible",
     A(r":focus(?!-visible)[^{]*\{[^}]*outline:\s*(0|none)",
       fp=[(r":focus-visible", "focus-visible in the excerpt"),
           (r":focus[^{]*\{[^}]*outline:\s*(0|none)[^}]*box-shadow", "a box-shadow ring replaces it")]),
     B([(r":focus-visible[^{}]*\{" + BLK + H, "FP", "the selector is focus-visible"),
        (r":focus(?!-visible)[^{}]*\{" + BLK + H + BLK + r"box-shadow:\s*(?!none)", "FP", "a box-shadow ring in the same focus block replaces the outline"),
        (r":focus(?!-visible)[^{}]*\{" + BLK + r"box-shadow:\s*(?!none)" + BLK + H, "FP", "a box-shadow ring in the same focus block replaces the outline"),
        (r":focus(?!-visible)[^{}]*\{" + BLK + H + BLK + r"(border-color|background|text-decoration:\s*underline)", "FP", "a visible focus change in the same block"),
        (r":focus(?!-visible)[^{}]*\{" + BLK + H, "TP", "a :focus rule removes the outline with no ring in its block"),
        (r"[^{}]*\{" + BLK + H, "TP", "the outline is removed for every state of a focusable element and nothing in the block replaces it; often a dialog that takes programmatic focus, so usefulness is low")]))
rule("full-viewport-width-overflow", A(None),
     B([(r"position:\s*fixed" + BLK + H, "FP", "a fixed element does not widen the page"),
        (H + BLK + r"position:\s*fixed", "FP", "a fixed element does not widen the page"),
        (r"modal-fullscreen[^{}]*\{" + BLK + H, "FP", "a dialog inside a fixed, scrolling modal"),
        (r"(vw-100|min-vw-100)[^{}]*\{" + BLK + H, "FP", "a utility class no element on the page uses"),
        (H + r"[^{}]*position:\s*relative[^{}]*left:\s*calc\(-50vw", "TP", "a full-bleed element at 100vw, which overflows by the scrollbar width"),
        (H + r";?\s*(min-)?width:\s*100vw", "TP", "an element at 100vw, which overflows by the scrollbar width")]))
rule("inline-style-attribute", A(r"style=[\"']", fp=[(r"style=[\"']\s*--[\w-]+:[^;\"']*;?\s*[\"']", "only a custom property")]),
     B([(H + r"[^>]*style=[\"']\s*(--[\w-]+:[^;\"']*;?\s*)+[\"']", "FP", "only custom properties, which the rule allows"),
        (H + r"[^>]*style=", "TP", "a static inline style")]))
rule("timing-300ms-default", A(r"(?<![\d.])0?\.3s\b|\b300ms\b"),
     B([(H + r"[^;}]*((?<![\d.])0?\.3s\b|\b300ms\b)", "TP", "a 300ms transition or animation"),
        (H, "FP", "no 300ms value at the match")]))
rule("h-screen-no-dvh-fallback", A(r"100vh", fp=[(r"100dvh", "dvh in the excerpt")]),
     B([(r"100dvh" + BLK + H, "FP", "the block also sets 100dvh"),
        (H + BLK + r"100dvh", "FP", "the block also sets 100dvh"),
        (H + r"[^;}]*100vh", "TP", "100vh with no dvh in its block"),
        (H, "cantTell", "")]))
rule("text-ink-at-low-alpha", A(r"rgba?\([^)]*,\s*0?\.[0-6]\d*\s*\)"),
     B([(r"(:disabled|\[disabled\]|\.disabled|aria-disabled)[^{}]*\{" + BLK + H, "FP", "disabled controls are outside the contrast requirement"),
        (H + r"color:\s*rgba?\(", "TP", "text color at low alpha")]))
rule("button-no-type", A(r"<button\b(?![^>]*\btype=)[^>]*>", fp=[(r"^\s*<button\b[^>]*\btype=", "type set")]),
     B([(H + r"<button\b[^>]*\btype=", "FP", "type is set"),
        (H + r"<button\b", "TP", "no type attribute")]))
rule("transition-duration-500ms-or-longer", A(None),
     B([(r"position:\s*fixed" + BLK + H, "FP", "a fixed control sliding in, not a hover or press answer"),
        (H + r".{0,500}:hover", "TP", "a hover rule for the same component follows, so the hover answers late"),(r"(carousel|modal|offcanvas|collapse|toast|progress|fade|slide|panel|menu|nav)[^{}]*\{" + BLK + H, "FP", "a panel or slide movement, not a hover or press answer"),
        (r"(:hover|:focus|:active|button|\.btn|\ba\b)[^{}]*\{" + BLK + H, "TP", "a state change that answers late"),
        (H, "cantTell", "")]))
rule("lorem-ipsum-leak", A(r"lorem\s+ipsum"), B([(H + r".{0,40}lorem", "TP", "lorem ipsum copy")]))
rule("placeholder-token-shipped", A(r"lorem\s+ipsum|\{\{[^}]*\}\}|\{TODO"),
     B([(H + r".{0,40}(lorem|\{\{|\{TODO)", "TP", "the rule's pattern lists lorem ipsum as a placeholder token")]),
     note="duplicates lorem-ipsum-leak on lorem copy")
rule("tooltip-on-required-info", A(r"title=", fp=[(r"alt=\"([^\"]+)\"[^>]*title=\"\1\"|title=\"([^\"]+)\"[^>]*alt=\"\2\"", "title repeats the alt")]),
     B([(r"alt=\"([^\"]+)\"[^>]*title=\"\1\"|title=\"([^\"]+)\"[^>]*alt=\"\2\"", "FP", "the title repeats the alt text, so nothing is hidden in it"),
        (H, "TP", "copy only in title")]))
rule("focusable-at-opacity-zero", A(None),
     B([(r"(backdrop|is-preload|\.fade)[^{}]*\{" + BLK + H, "FP", "a backdrop, a preload start state or a faded panel that is also display: none"),(r"input[^{}]*\{" + BLK + H, "FP", "a native checkbox or radio kept focusable under a custom control, the accessible pattern"),
        (r"(checkbox|radio)" + BLK + H, "FP", "a native checkbox or radio kept focusable under a custom control"),
        (r":hover" + BLK + H + "|" + H + r".{0,400}:hover", "FP", "revealed on hover: the rule leaves that to hover-only-card-actions"),
        (H, "cantTell", "")]))
rule("inline-svg-no-aria", A(r"<svg\b(?![^>]*aria-)(?![^>]*role=)[^>]*>", fp=[(r"^\s*<svg\b[^>]*aria-hidden", "aria-hidden set")]),
     B([(H + r"<svg\b[^>]*(aria-hidden|aria-label|role=\"img\")", "FP", "named or hidden"),
        (H + r"<svg\b[^>]*class=\"[^\"]*d-none", "FP", "a hidden sprite of symbols"),
        (H + r"<svg\b[^>]*>\s*<title", "FP", "has a title"),
        (H + r"<svg\b", "TP", "an svg with no name and not hidden")]))
rule("animating-layout-properties", A(r"transition:[^;]*\b(width|height|top|left|right|bottom|margin|padding|max-height)\b"),
     B([(H + r"transition:[^;}]*\b(width|height|top|left|right|bottom|margin|padding|max-height)\b", "TP", "transitions a layout property")]))
rule("input-purpose-missing", A(r"<input\b(?![^>]*autocomplete)[^>]*type=\"(email|tel)\"",
                                fp=[(r"^\s*<input\b[^>]*autocomplete=", "autocomplete set")]),
     B([(H + r"<input\b[^>]*autocomplete=", "FP", "autocomplete is set"),
        (H + r"<input\b[^>]*type=[\"']?(checkbox|radio|submit|button|search)", "FP", "not a personal-data field"),
        (H + r"<input\b", "TP", "a personal-data field with no autocomplete")]))
rule("generic-cta-text", A(r">\s*(learn more|get started|click here|read more)\s*<"),
     B([(H + r".{0,200}?>\s*(learn more|get started|click here)\s*<", "TP", "generic call to action")]))
rule("target-blank-no-noopener", A(r"target=[\"']_blank", fp=[(r"rel=[\"'][^\"']*noopener", "noopener set")]),
     B([(H + r"<a\b[^>]*rel=[\"'][^\"']*noopener", "FP", "noopener set"),
        (H + r"<a\b[^>]*target=[\"']_blank", "TP", "no noopener; browsers now imply it, so the risk is low")]))
rule("imagery-mandatory-missing", A(None),
     B([(r"<title>[^<]*(dashboard|checkout|sign.?in|log.?in|account|settings|docs|documentation|installation|album|blog|product|pour-over|create your|\u0627\u0644\u0625\u0639\u062f\u0627\u062f\u0627\u062a)", "FP", "not a landing page"),
        (r"<title>[^<]*pricing", "cantTell", "a pricing page; the rule names landing pages"),
        (r"<title>", "TP", "a landing page with no photograph")]))
rule("display-line-height-under-floor", A(None), B([], default="TP", why="the measured line height sits under the engine's display floor; the floor is house taste"))
rule("infinite-animation-without-reduced-motion", A(r"infinite"),
     B([(H + r"[^;}]*infinite", "TP", "an infinite animation with no reduced-motion override found")]))
rule("placeholder-as-label", A(r"<(input|textarea)\b(?![^>]*aria-label)[^>]*placeholder="),
     B([(H + r"<(input|textarea)\b[^>]*aria-label", "FP", "named by aria-label"),
        (H + r"<(input|textarea)\b[^>]*\bid=\"([^\"]+)\".{0,300}for=\"\2\"", "FP", "a label for it follows"),
        (r"for=\"([^\"]+)\"[^<]*</label>\s*" + H + r"<(input|textarea)\b[^>]*\bid=\"\1\"", "FP", "a label for it precedes"),
        (H + r"<(input|textarea)\b", "TP", "placeholder is the only name")]))
rule("heading-skip-h1-h3", A(r"<h[12]\b"), B([(H + r"<h[12]\b", "TP", "a lower heading follows with the level between missing")]))
rule("negative-margin-pull-left-right", A(r"margin-(left|right):\s*-(?:[4-9]\d|\d{3,})px", fp=[(r"margin-(left|right):\s*-(?:[0-3]?\d)px", "a small gutter offset")]),
     B([(H + r"margin-(left|right):\s*-(?:[4-9]\d|\d{3,})px", "TP", "a large negative side margin"),
        (H + r"margin-(left|right):\s*-", "FP", "a small gutter offset, not a pull")]))
rule("generic-class-container-wrapper-only", A(r"class=\"(inner|wrapper|box|container)\""), B([(H + r"<div class=\"(inner|wrapper|box)\"", "TP", "only a generic class")]))
rule("css-import-render-blocking", A(r"@import"), B([(H + r"@import", "TP", "an @import")]))
rule("hover-only-card-actions", A(None),
     B([(r"#menu" + BLK + H, "FP", "a menu close control shown with the menu, not on hover"),
        (H + r".{0,600}:hover" + BLK + r"opacity:\s*1", "cantTell", "an overlay revealed on hover; whether it holds an action needs the page"),
        (H, "FP", "not revealed by hover")]))
rule("focusable-inside-aria-hidden", A(r"aria-hidden=\"true\""),
     B([(r"<div\b[^>]*class=\"[^\"]*\bmodal\b[^>]*" + H, "FP", "a closed modal is display: none, so nothing inside it takes focus"),
        (H, "TP", "")]))
rule("body-font-weight-bold-or-700-keyword", A(None),
     B([(r"(^|[},;])\s*(body|p|li)\s*\{" + BLK + H, "TP", "a bare body, p or li rule set bold"),
        (H, "FP", "a classed, nested or marker selector (a title, a date line, a callout, a list counter), not body copy")]))
for r in ("emoji-in-ui", "lone-emoji-as-icon", "icon-emoji-stamp"):
    rule(r, A(r"&#1[23]\d{4};|&#9\d{3};|[\u2600-\u27bf]|[\U0001F300-\U0001FAFF]"),
         B([(H + r".{0,60}(&#1[23]\d{4};|&#9\d{3};|[\U0001F300-\U0001FAFF])", "TP", "an emoji used as an icon")]))
rule("emoji-bullet-marker", A(None), B([(r"content:\s*\"\u2714\"", "FP", "a print-only check mark drawn in CSS, not an emoji bullet"), (H, "cantTell", "")]))
rule("padding-shorthand-4-vals-zero-first", A(r"padding:\s*0\s+(\S+)\s+\S+\s+\1"),
     B([(H + r"padding:\s*0\s+(\S+)\s+\S+\s+\1\b", "TP", "right equals left, so three values do"), (H, "FP", "")]))
rule("display-table-for-layout", A(None),
     B([(H + r"\}?\s*\.display-table", "FP", "a utility class no element on the page uses"),
        (H + r".{0,300}display:\s*table-cell", "TP", "table cells used to lay out a row of boxes"),
        (H, "FP", "a clearfix, a legend that must wrap or a shrink-to-fit box, not table layout")]))
rule("repeated-action-same-name", A(None), B([]))
rule("text-align-justify-web", A(r"text-align:\s*justify", fp=[(r"\.text-(align-)?justify\s*\{", "a utility class")]),
     B([(r"\.text-(align-)?justify[^{}]*\{" + BLK + H, "FP", "a utility class no element on the page uses"),
        (H + r"text-align:\s*justify", "TP", "justified text")]))
rule("loader-spinner-border-default", A(r"spinner"), B([(H + r".{0,200}spinner-border", "TP", "the border-spin recipe"), (H, "cantTell", "")]))
rule("grid-cols-3-1fr-default", A(r"repeat\(3,\s*1fr\)"), B([(H + r".{0,80}repeat\(3,\s*1fr\)", "TP", "")], default="TP"))
rule("screen-reader-only-without-class", A(r"skip", fp=[(r"(govuk-skip-link|usa-skipnav)", "the design system's own skip-link class hides it until focus")]),
     B([(H + r"<a\b[^>]*(govuk-skip-link|usa-skipnav|skip-link|visually-hidden|sr-only)", "FP", "a skip-link class that hides it until focus")], default="TP"))
rule("cursor-not-allowed-no-visual", A(None),
     B([(r"disabled[^{}]*\{" + BLK + H + r".{0,600}disabled[^{}]*\{[^}]*(opacity|color|background)", "FP", "the disabled state has a visual change"),
        (r"(opacity|color|background)" + BLK + H, "FP", "the block changes the look"),
        (H + BLK + r"(opacity|color|background)", "FP", "the block changes the look"),
        (H, "cantTell", "")]))
rule("transition-property-all", A(r"transition:\s*all"), B([(H + r".{0,40}transition:\s*all", "TP", "")], default="TP"))
rule("viewport-no-zoom", A(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(\.0)?\b"), B([], default="TP", why="the viewport blocks zoom"))
rule("arbitrary-z-index-9999", A(r"z-index:\s*9{4,}"), B([(H + r"z-index:\s*9{4,}", "TP", "")]))
rule("lang-attribute-missing", A(r"<html(?![^>]*\blang=)"), B([(H + r"<html(?![^>]*\blang=)", "TP", ""), (H, "FP", "")]))
rule("unsplash-photo-id-no-alt", A(r"unsplash[^\"]*\"\s*alt=\"\"|alt=\"\"[^>]*unsplash"), B([(H + r"<img\b[^>]*alt=\"\"", "TP", "an empty alt on a stock photo")]))
rule("aspect-ratio-1-1-default", A(None), B([], default="FP", why="one square image or a utility among several ratios, not square everywhere"))
rule("one-action-several-labels", A(None), B([]))
rule("nav-equal-hamburger-desktop", A(None), B([], default="FP", why="the menu button is hidden at desktop widths by the page's own CSS, or the match is a dropdown"))
rule("select-without-label", A(r"<select\b(?![^>]*aria-label)"),
     B([(H + r"<select\b[^>]*aria-label", "FP", "named by aria-label"),
        (H + r"<select\b[^>]*\bid=\"([^\"]+)\".{0,300}for=\"\1\"|for=\"([^\"]+)\".{0,300}" + H + r"<select\b[^>]*\bid=\"\2\"", "FP", "a label points at it"),
        (H + r"<select\b", "TP", "no label is tied to the select")]))
rule("img-no-alt", A(r"<img\b(?![^>]*\balt=)"), B([(H + r"<img\b(?![^>]*\balt=)", "TP", "")]))
rule("link-without-href", A(None), B([(H + r"<a\b[^>]*(disabled|aria-disabled)", "FP", "a disabled link, which has no href on purpose"), (H, "TP", "")]))
rule("decorative-accent-ruler", A(None), B([(r"(popover|document-list-child|tooltip|arrow)[^{}]*\{" + BLK + H, "FP", "a list marker or popover arrow, not an ornament"), (H, "cantTell", "")]))
rule("glow-shadow-zero-offset", A(r"box-shadow:\s*0\s+0\s+\d"), B([(H + r"box-shadow:\s*0\s+0\s+\d", "TP", "")], default="TP"))
rule("flex-center-center-default", A(None), B([], default="TP", why="flex with both axes centred"))
rule("all-caps-large", A(None), B([]))
rule("font-family-monospace-fallback-default", A(r"monospace"), B([], default="TP", why="monospace with no named face"))
rule("href-javascript-void", A(r"href=\"javascript:"), B([], default="TP", why="a javascript: link"))
rule("default-font-only", A(r"font-family:\s*['\"]?(Inter|Geist)"), B([], default="TP", why="Inter alone on the page"))
rule("fake-name-john-doe", A(r">\s*(John|Jane) Doe\s*<", fp=[(r"placeholder=\"(John|Jane) Doe\"", "an example in a placeholder hint, not shipped data")]),
     B([(H + r"[^<>]{0,40}placeholder=\"(John|Jane) Doe\"|placeholder=\"(John|Jane) Doe\"[^<>]{0,10}" + H, "FP", "a placeholder hint"),
        (H, "TP", "a placeholder name shipped as data")]))
rule("animation-duration-too-long", A(r"animation:[^;]*\b1\.\d+s"),
     B([(r"prefers-reduced-motion" + r"[^@]*" + H, "FP", "slows a spinner under reduced motion on purpose"), (H, "TP", "")]))
rule("anchor-no-href-as-button", A(None), B([(H + r"<a\b[^>]*(disabled|aria-disabled)", "FP", "a disabled link"), (H, "TP", "")]))
rule("cta-text-tap-continue-go", A(None), B([(H + r"<a\b[^>]*class=\"next\"", "FP", "pagination; Next is clear there"), (H, "cantTell", "")]))
rule("cta-arrow-rightward-bouncing", A(None), B([], default="FP", why="an arrow with no bounce animation"))
rule("footer-built-with-love-coffee", A(None), B([], default="FP", why="a feature card, not a footer credit"))
rule("video-without-captions", A(r"<video\b[^>]*muted"), B([(H + r"<video\b[^>]*muted", "FP", "a muted product demo loop has no speech to caption")], default="TP"))
rule("aria-hidden-on-interactive", A(r"\bhidden\b[^>]*aria-hidden|aria-hidden[^>]*\bhidden\b"),
     B([(H + r"<\w+\b[^>]*\shidden\s[^>]*aria-hidden", "FP", "the hidden attribute removes it from the focus order")], default="TP"))
rule("iframe-without-title", A(r"<noscript>", fp=[(r"<noscript><iframe[^>]*googletagmanager", "a tag-manager fallback inside noscript")]),
     B([(r"<noscript>\s*" + H, "FP", "a hidden tag-manager fallback, never shown"), (H, "TP", "")]))
rule("layout-family-repeated", A(None), B([]))
rule("font-system-only", A(r"font-family:\s*-apple-system"), B([], default="TP", why="a system stack and nothing chosen"))
for r in ("card-glow-purple-shadow", "hairline-border-heavy-shadow", "hero-text-arbitrary-90px", "body-text-shadow-on-prose",
          "letterspacing-tracking-tight-display", "scale-1-1-on-card-hover", "cta-text-read-more", "title-case-headlines",
          "event-listener-no-passive-on-scroll", "purple-to-blue-gradient", "testimonial-fake-five-stars", "border-radius-2xl-default"):
    rule(r, A(None), B([], default="TP", why="the condition is present at the match"))
rule("animated-grain-noise-no-perf-class", A(None), B([], default="cantTell", why="a glitch text effect named noise, not a grain layer"))
rule("dark-text-on-dark-card", A(None), B([], default="FP", why="utility class definitions, no card at the match"))
rule("fixed-height-text-block", A(None), B([(r"li div\{" + BLK + H, "FP", "a 44px tile around one letter cannot overflow")], default="cantTell"))
rule("numbered-placeholder-classname", A(None), B([], default="FP", why="a class generated by the CMS, not a placeholder name"))
rule("scroll-to-top-button-everywhere", A(None), B([]))
rule("inline-style-display-none-no-aria", A(None), B([], default="FP", why="display: none already removes it from assistive technology"))
# Render checks. Pass A reads the measured message; pass B reads the message
# with the head of the page, where web fonts and background photos show.
FONTS = r"fonts\.googleapis|@font-face|use\.typekit"
def RA(default="TP", why="the measured message states the condition"):
    return {"default": default, "why": why, "unless": []}
for r in ("text-low-contrast", "accent-text-low-contrast"):
    rule(r, RA(), B([(r"#ffffff on #ffffff", "FP", "white on white: the engine measured the page behind a caption, not the slide it sits on"),
                     (r"^p\.text-white-75.*<title>Creative", "cantTell", "masthead text on a background photo that is not stored"),
                     (r"^\S*\.text-(black|white)-(50|75)\b", "TP", "text set at low alpha on purpose by a utility class"),
                     ("computed:faded-text", "cantTell", "the measured ratio is well under what the two colours give, so the text was measured faded, as in a preload state a blocked script would lift"),
                     (r"^\S*\b(masthead|hero|banner|cover)\b.*" + H + r".{0,6000}background(-image)?:[^;]*url\(", "cantTell", "hero text on a photo that is not stored")],
                    default="TP", why="flat colours on both sides of the measurement"))
rule("text-overflows-its-box", RA(), B([(H + r".{0,6000}(" + FONTS + r"|<link[^>]*stylesheet)", "cantTell", "the page loads web fonts, blocked in the frozen render; fallback fonts change widths")], default="TP", why="system fonts only, so the measured width holds"))
for r in ("image-broken", "photo-grade-off", "image-distorted"):
    rule(r, RA("cantTell", "images are not stored with the frozen pages"), B([], default="cantTell", why="images are not stored with the frozen pages"))
rule("render-failed", RA("cantTell", "the page did not render"), B([], default="cantTell", why="the page did not render"))
rule("focus-ring-missing", RA(), B([(r"^\S*\.usa-focus\b", "FP", "the usa-focus class shows the focused style at rest, as a demo, so focus adds no change"),
                                    (H + r"ux-bench: script elements removed", "cantTell", "the original page ran scripts; they were removed from the frozen copy")],
                                   default="TP", why="the original page had no scripts, so the frozen render is the page"))
rule("target-too-small", RA(), B([(r"target is [0-4]x[0-4]px", "cantTell", "an icon link collapsed because its icon font is not stored"),
                                  (H + r"ux-bench: script elements removed", "cantTell", "the original page ran scripts; they were removed from the frozen copy")],
                                 default="TP", why="the original page had no scripts, so the frozen render is the page"))
for r in ("state-answers-late", "press-moves-under-reduced-motion", "focus-ring-clipped", "focus-obscured",
          "focus-lost-after-escape", "input-text-zooms", "horizontal-overflow", "centered-text-off-center",
          "first-screen-covered", "color-over-budget", "infinite-animation-under-reduced-motion", "moving-content-without-pause"):
    rule(r, RA(), B([(H + r"ux-bench: script elements removed", "cantTell", "the original page ran scripts, removed from the frozen copy, which can change this measurement")],
                    default="TP", why="the original page had no scripts, so the frozen render is the page"))

json.dump({"note": "Model-made labelling criteria, one per rule and pass. Read bench/label.py for the method.",
           "rules": G}, open(__import__("pathlib").Path(__file__).with_name("guide.json"), "w"), indent=1, ensure_ascii=True)
print(len(G))
