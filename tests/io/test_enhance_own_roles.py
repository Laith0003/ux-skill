"""An engine-built system comes back through its own exports with no false
finding in its own names: every color role used the way the engine means it
is neither a name that lies nor a name with stray uses."""
import pytest

from engine.foundations import build_system
from engine.foundations.export import dump_dtcg, to_css
from engine.io import Source, enhance, import_css, import_dtcg, propose, scan
from engine.io.adapter import ROLE_TYPES
from engine.synthesizer.axes import AxisValues


def v(role):
    return f"var(--{role.replace('.', '-')})"


# Each engine color role used as the engine means it: surfaces and fills
# as backgrounds, text and the color on a fill as text, lines as edges,
# hover fills on hover, focus rings on focus.
APP = f"""body {{ background: {v('color.surface.page')}; color: {v('color.text.default')}; }}
.card {{ background: {v('color.surface.card')}; border: 1px solid {v('color.line.subtle')}; }}
.sunken {{ background: {v('color.surface.sunken')}; }}
.raised {{ background: {v('color.surface.raised')}; }}
.inverse {{ background: {v('color.surface.inverse')}; color: {v('color.text.inverse')}; }}
.selected {{ background: {v('color.surface.selected')}; border-color: {v('color.line.selected')}; }}
.tint {{ background: {v('color.surface.tint')}; }}
.band {{ background: {v('color.surface.band')}; }}
.stripe:nth-child(odd) {{ background: {v('color.surface.stripe')}; }}
.header {{ background: {v('color.surface.header')}; }}
code {{ background: {v('color.surface.code')}; color: {v('color.syntax.plain')}; }}
.muted {{ color: {v('color.text.muted')}; }}
a {{ color: {v('color.text.link')}; }}
.accent {{ color: {v('color.text.accent')}; }}
.support {{ color: {v('color.text.support')}; }}
.btn {{ background: {v('color.action.primary')}; color: {v('color.text.on-action')}; }}
.btn-edge {{ border-color: {v('color.action.primary-edge')}; }}
.btn:hover {{ background: {v('color.action.primary-hover')}; }}
.btn:active {{ background: {v('color.action.primary-pressed')}; }}
.btn:disabled {{ background: {v('color.action.disabled')}; color: {v('color.text.disabled')}; }}
.danger {{ background: {v('color.action.danger')}; color: {v('color.text.on-danger')}; }}
.danger:hover {{ background: {v('color.action.danger-hover')}; }}
.danger:active {{ background: {v('color.action.danger-pressed')}; }}
.brand {{ background: {v('color.surface.brand')}; color: {v('color.text.on-brand')}; }}
.brand .btn {{ background: {v('color.action.on-brand')}; }}
.brand .btn span {{ color: {v('color.text.on-brand-action')}; }}
.brand .btn:hover {{ background: {v('color.action.on-brand-hover')}; }}
.brand .btn:active {{ background: {v('color.action.on-brand-pressed')}; }}
@media (prefers-color-scheme: dark) {{
  .btn:hover {{ background: {v('color.action.primary-hover')}; }}
  .brand .btn:hover {{ background: {v('color.action.on-brand-hover')}; }}
}}
.input {{ border: 1px solid {v('color.line.input')}; }}
.input[aria-invalid=true] {{ border-color: {v('color.line.danger')}; }}
.quote {{ border-inline-start: 4px solid {v('color.line.accent')}; }}
.input:focus-visible {{ outline-color: {v('color.focus.ring')}; }}
.band :focus-visible {{ outline-color: {v('color.focus.ring-inverse')}; }}
.overlay {{ background: {v('color.scrim')}; }}
.hero::after {{ background: {v('color.media.veil')}; }}
.hero h1 {{ color: {v('color.text.on-media')}; }}
.kw {{ color: {v('color.syntax.keyword')}; }}
.str {{ color: {v('color.syntax.string')}; }}
.num {{ color: {v('color.syntax.number')}; }}
.fn {{ color: {v('color.syntax.function')}; }}
.comment {{ color: {v('color.syntax.comment')}; }}
.deco-a {{ background: {v('color.decorative.brand')}; }}
.deco-b {{ background: {v('color.decorative.support')}; }}
.deco-c {{ background: {v('color.decorative.neutral')}; }}
.illo path {{ stroke: {v('color.illustration.line')}; }}
.logo {{ fill: {v('color.logo')}; }}
""" + "".join(
    f".{s}-note {{ background: {v(f'color.status.{s}.soft')}; "
    f"color: {v(f'color.status.{s}.text')}; }}\n"
    f".{s}-badge {{ background: {v(f'color.status.{s}.strong')}; "
    f"color: {v(f'color.status.{s}.on-strong')}; }}\n"
    for s in ("danger", "warning", "success", "info")) + f"""
.photo::after {{ background: {v('imagery.scrim')}; color: {v('imagery.on-scrim')}; }}
.photo-tint {{ background: {v('imagery.tint')}; }}
"""

SYSTEMS = [(0.2, "#3366FF", False, "light"), (0.5, "#E0457B", True, "dark"),
           (0.8, "#0F8A5F", False, "dark"), (0.35, "#FFD500", True, "light")]


def test_the_stylesheet_uses_every_engine_color_role():
    used = {r for r, t in ROLE_TYPES.items() if t == "color" and v(r) in APP}
    missing = sorted(r for r, t in ROLE_TYPES.items() if t == "color")
    missing = [r for r in missing if r not in used and not r.startswith("imagery.duotone")]
    assert missing == []


@pytest.mark.parametrize("level,brand,arabic,scheme", SYSTEMS)
def test_our_own_roles_used_as_intended_are_never_named_as_lies(tmp_path, level, brand,
                                                                 arabic, scheme):
    (tmp_path / "app.css").write_text(APP, encoding="utf-8")
    ts = build_system(AxisValues(*[level] * 7), brand, arabic=arabic).tokens
    for imported in (import_css(to_css(ts, scheme=scheme),
                                Source("tokens.css", "css", "0" * 64, 1)),
                     import_dtcg(dump_dtcg(ts), Source("tokens.json", "dtcg", "0" * 64, 1))):
        report = enhance(imported, propose(imported.tokens),
                         scan([tmp_path], imported.tokens))
        d = report.drift
        assert [x.token for x in d.lies] == [], [x.message for x in d.lies]
        assert [x.token for x in d.strays] == [], [x.message for x in d.strays]
        assert d.missing == []


@pytest.mark.parametrize("name", ["action-on-brand", "button-on-dark", "cta-on-inverse",
                                  "brand-fill-on-dark", "fill-on-media"])
def test_a_fill_word_before_on_names_a_background(tmp_path, name):
    imported = import_css(f":root {{ --{name}: #222222; }}\n",
                          Source("tokens.css", "css", "0" * 64, 1))
    (tmp_path / "app.css").write_text(f".a {{ background: var(--{name}); }}\n"
                                      f".b {{ color: var(--{name}); }}\n", encoding="utf-8")
    d = enhance(imported, propose(imported.tokens), scan([tmp_path], imported.tokens)).drift
    assert d.lies == []
    assert [(x.token, x.message) for x in d.strays] == [
        (name, "is named for backgrounds but is used for text color at app.css:2; 1 of its "
               "2 uses match its name")]
