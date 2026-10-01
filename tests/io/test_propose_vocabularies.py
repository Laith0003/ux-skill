"""propose() reads the common naming vocabularies: a system written in
plain names (background, foreground, primary, border, ring), on- pairs,
brand names, bg, fg and border families, or text names gets its core text,
surface, action, border and focus roles proposed. Names only, never a
look: each proposal says by "name" and which vocabulary matched."""
import json

from engine.foundations.tokens import Token, TokenSet
from engine.io.adapter import RoleMap, dump_mapping, parse_mapping, propose
from engine.io.css_in import import_css
from engine.io.enhance import enhance
from engine.io.report import Source
from engine.io.tailwind_in import import_tailwind_css

CORE = ("color.text.default", "color.surface.page", "color.action.primary",
        "color.line.subtle", "color.focus.ring")

# Invented systems, one per vocabulary, each with a dark class.
PLAIN = """:root {
  --background: #ffffff;
  --foreground: #16181d;
  --card: #ffffff;
  --card-foreground: #16181d;
  --popover: #ffffff;
  --muted: #f2f3f5;
  --muted-foreground: #5b606b;
  --accent: #eef0f4;
  --primary: #1f4fd6;
  --primary-foreground: #ffffff;
  --secondary: #eef0f4;
  --destructive: #c42b2b;
  --destructive-foreground: #ffffff;
  --border: #d9dce1;
  --input: #8a8f99;
  --ring: #1f4fd6;
}
.dark {
  --background: #111318;
  --foreground: #f4f5f7;
}
"""
ON_PAIRS = """:root {
  --surface: #fcfcfd;
  --on-surface: #1a1c20;
  --on-surface-variant: #50545c;
  --primary: #2f5bd3;
  --on-primary: #ffffff;
  --error: #b3261e;
  --on-error: #ffffff;
  --outline: #787d86;
  --outline-variant: #c9ccd2;
}
"""
FAMILIES = """:root {
  --bg-default: #ffffff;
  --bg-subtle: #f6f7f9;
  --bg-emphasis: #1c1f24;
  --fg-default: #1c1f24;
  --fg-muted: #5c616b;
  --fg-on-emphasis: #ffffff;
  --fg-link: #1d56c9;
  --border-default: #d4d7dd;
  --border-focus: #1d56c9;
  --brand: #1d56c9;
  --brand-hover: #1847a8;
  --on-brand: #ffffff;
}
"""
TEXT_NAMES = """:root {
  --text-primary: #17191e;
  --text-secondary: #5a5f69;
  --text-disabled: #a1a5ad;
  --surface-page: #ffffff;
  --surface-raised: #ffffff;
  --action-primary: #2450c8;
  --line-subtle: #d6d9de;
  --focus-ring: #2450c8;
}
"""


def _imported(text, name="theme.css"):
    return import_css(text, Source(name, "css", "0" * 64, len(text)))


def _roles(mapping):
    return {r: (m.token, m.vocabulary) for r, m in mapping.roles.items()}


def test_plain_names_map_the_core_roles_and_their_foreground_pairs():
    mapping = propose(_imported(PLAIN).tokens)
    assert _roles(mapping) == {
        "color.surface.page": ("background", "plain names"),
        "color.surface.card": ("card", "plain names"),
        "color.surface.sunken": ("muted", "plain names"),
        "color.surface.raised": ("popover", "plain names"),
        "color.text.default": ("foreground", "plain names"),
        "color.text.muted": ("muted-foreground", "plain names"),
        "color.text.on-action": ("primary-foreground", "plain names"),
        "color.text.on-danger": ("destructive-foreground", "plain names"),
        "color.action.primary": ("primary", "plain names"),
        "color.action.danger": ("destructive", "plain names"),
        "color.line.subtle": ("border", "plain names"),
        "color.line.input": ("input", "plain names"),
        "color.focus.ring": ("ring", "plain names")}
    assert all(m.by == "name" for m in mapping.roles.values())
    assert set(CORE) <= set(mapping.roles)


def test_a_tailwind_theme_prefix_is_read_through():
    text = ('@import "tailwindcss";\n@theme {\n  --color-background: #ffffff;\n'
            '  --color-foreground: #111111;\n  --color-primary: #2b4fd0;\n'
            '  --color-border: #dddddd;\n  --color-ring: #2b4fd0;\n}\n')
    ts = import_tailwind_css(text, Source("app.css", "tailwind", "0" * 64, len(text))).tokens
    assert _roles(propose(ts)) == {
        "color.surface.page": ("color-background", "plain names"),
        "color.text.default": ("color-foreground", "plain names"),
        "color.action.primary": ("color-primary", "plain names"),
        "color.line.subtle": ("color-border", "plain names"),
        "color.focus.ring": ("color-ring", "plain names")}


def test_on_pairs_map_the_color_on_each_surface():
    # With no background, surface is the page.
    assert _roles(propose(_imported(ON_PAIRS).tokens)) == {
        "color.surface.page": ("surface", "plain names"),
        "color.text.default": ("on-surface", "on- pairs"),
        "color.text.muted": ("on-surface-variant", "on- pairs"),
        "color.text.on-action": ("on-primary", "on- pairs"),
        "color.text.on-danger": ("on-error", "on- pairs"),
        "color.action.primary": ("primary", "plain names"),
        "color.action.danger": ("error", "on- pairs"),
        "color.line.subtle": ("outline-variant", "on- pairs"),
        "color.line.input": ("outline", "on- pairs")}


def test_bg_fg_and_border_families_and_brand_names_map():
    assert _roles(propose(_imported(FAMILIES).tokens)) == {
        "color.surface.page": ("bg-default", "bg, fg and border families"),
        "color.surface.sunken": ("bg-subtle", "bg, fg and border families"),
        "color.surface.inverse": ("bg-emphasis", "bg, fg and border families"),
        "color.text.default": ("fg-default", "bg, fg and border families"),
        "color.text.muted": ("fg-muted", "bg, fg and border families"),
        "color.text.inverse": ("fg-on-emphasis", "bg, fg and border families"),
        "color.text.link": ("fg-link", "bg, fg and border families"),
        "color.text.on-action": ("on-brand", "brand names"),
        "color.action.primary": ("brand", "brand names"),
        "color.action.primary-hover": ("brand-hover", "brand names"),
        "color.line.subtle": ("border-default", "bg, fg and border families"),
        "color.focus.ring": ("border-focus", "bg, fg and border families")}


def test_text_names_and_the_roles_own_words_map():
    assert _roles(propose(_imported(TEXT_NAMES).tokens)) == {
        "color.surface.page": ("surface-page", "role names"),
        "color.surface.raised": ("surface-raised", "role names"),
        "color.text.default": ("text-primary", "text names"),
        "color.text.muted": ("text-secondary", "text names"),
        "color.text.disabled": ("text-disabled", "role names"),
        "color.action.primary": ("action-primary", "role names"),
        "color.line.subtle": ("line-subtle", "role names"),
        "color.focus.ring": ("focus-ring", "role names")}


def test_a_name_that_means_different_things_in_different_systems_is_left_to_the_owner():
    # accent is a hover fill in one vocabulary and the brand color in
    # another, and secondary names no role; neither is proposed.
    mapping = propose(_imported(PLAIN).tokens)
    assert "accent" not in {m.token for m in mapping.roles.values()}
    assert "secondary" not in {m.token for m in mapping.roles.values()}


def test_a_name_that_holds_another_type_is_not_proposed():
    ts = _imported(":root { --border: 1px; --ring: 3px; --foreground: #111111; }\n").tokens
    assert _roles(propose(ts)) == {"color.text.default": ("foreground", "plain names")}


def test_a_token_named_as_the_role_itself_still_wins():
    ts = _imported(":root { --foreground: #111111; --color-text-default: #222222; }\n").tokens
    assert propose(ts).roles["color.text.default"] == RoleMap("color-text-default", "name")


def test_the_vocabulary_is_written_to_the_mapping_and_read_back():
    mapping = propose(_imported(PLAIN).tokens)
    doc = json.loads(dump_mapping(mapping))
    assert doc["roles"]["color.text.default"] == {"token": "foreground", "by": "name",
                                                  "vocabulary": "plain names"}
    assert parse_mapping(dump_mapping(mapping), "mapping.json") == mapping


def test_a_proposal_from_a_vocabulary_is_measured_and_named_in_the_decisions():
    imported = _imported(PLAIN)
    result = enhance(imported, propose(imported.tokens))
    gate = result.to_dict()["gate"]
    assert gate["measured"] and gate["pairs_checked"] > 0
    assert ("13 color roles are mapped by name only, through the plain names vocabulary "
            "(background, foreground, primary, border, input, ring and the -foreground pairs): "
            "color.surface.page to background, color.surface.card to card, color.surface.sunken "
            "to muted and 10 more; confirm them in mapping.json. The JSON report lists each."
            ) in result.decisions


# ---------------------------------------------------------------- prefixes

def _prefixed(mapping):
    return {r: (m.token, m.vocabulary, m.prefix) for r, m in mapping.roles.items()}


MD = ("primary", "on-primary", "surface", "on-surface", "on-surface-variant", "outline",
      "outline-variant", "error", "on-error")
MD_EXPECT = {
    "color.surface.page": ("surface", "plain names"),
    "color.text.default": ("on-surface", "on- pairs"),
    "color.text.muted": ("on-surface-variant", "on- pairs"),
    "color.text.on-action": ("on-primary", "on- pairs"),
    "color.text.on-danger": ("on-error", "on- pairs"),
    "color.action.primary": ("primary", "plain names"),
    "color.action.danger": ("error", "on- pairs"),
    "color.line.subtle": ("outline-variant", "on- pairs"),
    "color.line.input": ("outline", "on- pairs")}


def test_a_prefix_most_color_names_share_is_read_through_and_reported():
    text = ":root {\n" + "".join(f"  --md-sys-color-{n}: #{i:02x}3355;\n"
                                 for i, n in enumerate(MD)) + "  --md-sys-shape-corner: 4px;\n}\n"
    mapping = propose(_imported(text).tokens)
    assert _prefixed(mapping) == {r: (f"md-sys-color-{t}", v, "md-sys-color")
                                  for r, (t, v) in MD_EXPECT.items()}


def test_a_dtcg_prefix_is_read_through_too():
    from engine.io.dtcg_in import import_dtcg
    doc = {"md": {"sys": {"color": {n: {"$type": "color", "$value": f"#{i:02x}3355"}
                                    for i, n in enumerate(MD)}}}}
    text = json.dumps(doc)
    ts = import_dtcg(text, Source("tokens.json", "dtcg", "0" * 64, len(text))).tokens
    assert _prefixed(propose(ts)) == {r: (f"md.sys.color.{t}", v, "md.sys.color")
                                      for r, (t, v) in MD_EXPECT.items()}


def test_a_brand_prefix_and_a_ds_color_prefix_are_read_through():
    acme = _imported(":root {\n  --acme-bg-default: #ffffff;\n  --acme-fg-default: #111111;\n"
                     "  --acme-fg-muted: #555555;\n  --acme-border-default: #dddddd;\n"
                     "  --acme-brand: #2244cc;\n  --acme-radius-sm: 4px;\n}\n")
    assert _prefixed(propose(acme.tokens)) == {
        "color.surface.page": ("acme-bg-default", "bg, fg and border families", "acme"),
        "color.text.default": ("acme-fg-default", "bg, fg and border families", "acme"),
        "color.text.muted": ("acme-fg-muted", "bg, fg and border families", "acme"),
        "color.action.primary": ("acme-brand", "brand names", "acme"),
        "color.line.subtle": ("acme-border-default", "bg, fg and border families", "acme"),
        # A radius read through the prefix too: names only, of the role's type.
        "radius.chip": ("acme-radius-sm", "scale names", "acme")}
    ds = _imported(":root {\n  --ds-color-background: #ffffff;\n  --ds-color-foreground: #111111;"
                   "\n  --ds-color-primary: #2244cc;\n  --ds-color-border: #dddddd;\n"
                   "  --ds-color-ring: #2244cc;\n}\n")
    assert _prefixed(propose(ds.tokens)) == {
        "color.surface.page": ("ds-color-background", "plain names", "ds-color"),
        "color.text.default": ("ds-color-foreground", "plain names", "ds-color"),
        "color.action.primary": ("ds-color-primary", "plain names", "ds-color"),
        "color.line.subtle": ("ds-color-border", "plain names", "ds-color"),
        "color.focus.ring": ("ds-color-ring", "plain names", "ds-color")}


def test_camel_case_words_are_read_as_words():
    ts = _imported(":root {\n  --fgColor-default: #111111;\n  --fgColor-muted: #555555;\n"
                   "  --bgColor-default: #ffffff;\n  --borderColor-default: #dddddd;\n}\n").tokens
    assert _prefixed(propose(ts)) == {
        "color.surface.page": ("bgColor-default", "bg, fg and border families", ""),
        "color.text.default": ("fgColor-default", "bg, fg and border families", ""),
        "color.text.muted": ("fgColor-muted", "bg, fg and border families", ""),
        "color.line.subtle": ("borderColor-default", "bg, fg and border families", "")}


def test_the_prefix_is_kept_in_the_mapping_and_named_in_the_decisions():
    text = ":root {\n" + "".join(f"  --ds-color-{n}: #{i:02x}3355;\n"
                                 for i, n in enumerate(("background", "foreground"))) + "}\n"
    imported = _imported(text)
    mapping = propose(imported.tokens)
    doc = json.loads(dump_mapping(mapping))
    assert doc["roles"]["color.text.default"] == {
        "token": "ds-color-foreground", "by": "name", "vocabulary": "plain names",
        "prefix": "ds-color"}
    assert parse_mapping(dump_mapping(mapping), "mapping.json") == mapping
    decisions = enhance(imported, mapping).decisions
    assert ("2 color roles are mapped by name only, through the plain names vocabulary "
            "(background, foreground, primary, border, input, ring and the -foreground pairs), "
            "after the prefix ds-color that the system's color names share: color.surface.page "
            "to ds-color-background, color.text.default to ds-color-foreground; confirm them in "
            "mapping.json. The JSON report lists each.") in decisions


def test_names_the_vocabularies_know_but_give_no_role_are_named_for_the_owner():
    imported = _imported(PLAIN)
    decisions = enhance(imported, propose(imported.tokens)).decisions
    assert ("The system has names the vocabularies know but give no role, so they were not "
            "proposed: card-foreground, accent and secondary; if one plays one of the engine's "
            "roles, map it in mapping.json.") in decisions


def test_merge_never_proposes_a_token_the_owner_sent_to_another_role():
    from engine.io.adapter import Mapping, merge
    ts = _imported(PLAIN).tokens
    owner = Mapping(roles={"color.text.default": RoleMap("primary", "owner")})
    merged, _ = merge(propose(ts), owner)
    assert merged.roles["color.text.default"] == RoleMap("primary", "owner")
    assert "color.action.primary" not in merged.roles


# ---------------------------------------------------------------- a mature system's names


def test_a_mature_systems_core_roles_are_mapped_by_name_only():
    from pathlib import Path

    from engine.io.read import read_system
    fixture = Path(__file__).parent.parent / "fixtures" / "mature_system" / "tokens"
    roles = {r: m.token for r, m in propose(read_system(fixture / "tokens.json").tokens)
             .roles.items()}
    assert roles == {
        "color.surface.page": "brand.canvas", "color.surface.card": "brand.surface",
        "color.text.default": "brand.text-primary", "color.text.muted": "brand.text-secondary",
        "color.text.on-action": "brand.on-primary", "color.action.primary": "brand.primary",
        "color.focus.ring": "brand.focus", "color.hairline": "brand.hairline",
        "color.status.danger.text": "status.danger",
        "color.status.warning.text": "status.warning",
        "color.status.success.text": "status.success",
        "radius.chip": "radius.small", "radius.control": "radius.medium",
        "radius.pill": "radius.pill",
        "motion.state.duration": "motion.duration-fast",
        "motion.reveal.duration": "motion.duration-base",
        "layout.breakpoint.tablet": "layout.breakpoint-md",
        "layout.breakpoint.laptop": "layout.breakpoint-lg",
        "type.face.display": "type.family-display", "type.face.text": "type.family-body",
        "type.face.mono": "type.family-data",
        "type.text.display": "fontSize type.size-display",
        "type.text.body": "fontSize type.size-body"}


def test_type_size_names_map_the_size_of_their_type_roles():
    ts = TokenSet({})
    for path, px in (("type.size-body", 16), ("type.size-display", 56), ("type.size-h1", 40),
                     ("font-size-label", 13), ("text-size-fine", 12), ("type.size-lead", 20),
                     ("type.size-small", 14), ("size-body-small", 14), ("size-base", 16)):
        ts.add(Token(path, "dimension", {"value": px, "unit": "px"}))
    ts.add(Token("type.size-code", "color", "#111111"))   # a size name on a color: not read
    proposed = propose(ts)
    fields = {r: {k: (f.token, f.by) for k, f in m.fields.items()}
              for r, m in proposed.roles.items()}
    # Only a name that says type, font or text and a text role's own name.
    assert fields == {
        "type.text.display": {"fontSize": ("type.size-display", "name")},
        "type.text.heading-1": {"fontSize": ("type.size-h1", "name")},
        "type.text.body": {"fontSize": ("type.size-body", "name")},
        "type.text.label": {"fontSize": ("font-size-label", "name")},
        "type.text.fine": {"fontSize": ("text-size-fine", "name")}}
    assert all(m.vocabulary == "type size names" for m in proposed.roles.values())
    # Written field by field, and read back the same.
    doc = json.loads(dump_mapping(proposed))
    assert doc["roles"]["type.text.body"] == {
        "fields": {"fontSize": {"token": "type.size-body", "by": "name"}}}
    assert parse_mapping(dump_mapping(proposed), "mapping.json").roles["type.text.body"].fields == \
        proposed.roles["type.text.body"].fields


def test_a_bare_size_name_is_left_to_the_owner_with_a_note():
    from engine.io.adapter import unclaimed_sizes
    ts = TokenSet({})
    for path in ("size-body-small", "size-display", "sizes.label", "type.size-body", "size-md"):
        ts.add(Token(path, "dimension", {"value": 14, "unit": "px"}))
    proposed = propose(ts)
    assert list(proposed.roles) == ["type.text.body"]
    assert [t for t, _ in unclaimed_sizes(ts, proposed)] == [
        "size-body-small", "size-display", "sizes.label"]
    imported = import_css(":root {\n  --ink: #111111;\n  --size-display: 56px;\n}\n",
                          Source("theme.css", "css", "0" * 64, 1))
    done = enhance(imported, propose(imported.tokens))
    [line] = [d for d in done.decisions if "size-display" in d]
    assert "type.text.display" in line and "fontSize" in line and "mapping.json" in line


def test_a_scale_name_maps_only_a_token_of_the_roles_type():
    ts = TokenSet({})
    ts.add(Token("radius.medium", "color", "#111111"))
    ts.add(Token("motion.duration-fast", "dimension", {"value": 4, "unit": "px"}))
    assert propose(ts).roles == {}
